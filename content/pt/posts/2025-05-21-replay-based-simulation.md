---
title: "Simulação por Replay"
subtitle: "Replay transformaria discussão de pricing de opinião em diferença observável. Eu não construí o laboratório ainda. Esse é o formato que eu venho estudando."
author: helio
layout: post
date: 2025-05-21T10:00:00+00:00
series:
  - pricing-engineering
series_order: 10
categories:
  - Engineering
  - Pricing
  - Architecture
tags:
  - pricing
  - simulation
  - replay
  - rule-engine
  - architecture
  - go
description: "Simulação por replay casaria um snapshot guardado do engine com um fixture capturado de tráfego e um rule set candidato, produzindo um diff determinístico. Esse post é o desenho que tô trabalhando, informado por bre-go e traffic-gen mas ainda não fiado em sistema de pricing que tenha shippado."
---

Teve uma reunião numa quarta de tarde em abril em que dois sêniores do time de pricing discordavam sobre se uma mudança proposta de markup ia subir receita ou prejudicar conversão. A discordância era real — os dois tinham modelos defensáveis na cabeça. Tinha trinta e cinco minutos rolando.

Eu perguntei, meio em voz alta, se a gente conseguia replayar a mudança contra o tráfego do trimestre passado e simplesmente *ver* quem tava certo.

Não dava. A gente não tinha o laboratório. Tinha os snapshots de engine — o `bre-go` produz — e tinha o formato aproximado de um gerador de tráfego na cabeça, mas ainda não tinha o runner que casava os dois e produzia o diff. A reunião passou da hora, terminou com um acordo cauteloso de rolar com calma, e virou uma série de conversas de follow-up nas semanas seguintes.

Aquela tarde foi quando comecei a estudar replay pra valer. Esse post é o que venho trabalhando desde então. Não é postmortem de sistema que a gente construiu e operou. É o desenho que venho virando do avesso — qual formato o laboratório teria que ter, que artefatos produziria, que workflows habilitaria — informado pelo trabalho de snapshot no `bre-go` e pelo formato de tráfego do post anterior, mas ainda não fiado em nenhum sistema de pricing que eu tenha sido dono. O post anterior, de shadow mode, cobriu a metade live da validação pré-produção. Esse post é a metade offline que venho tentando descobrir como construir bem.

## O que o laboratório exigiria

Uma sessão de replay precisa de três artefatos e uma peça de código.

**Um snapshot do engine ativo.** Quais regras estavam vivas, em que ordem, em que priority, com que ação. É o trabalho de v0.15 / v0.16 do [`bre-go`](https://github.com/helmedeiros/bre-go) — `ExportSnapshot` e `LoadSnapshot` produzem e consomem uma serialização do estado compilado do engine, endereçada por conteúdo, portável entre arquiteturas. Snapshot é pequeno (KBs a MBs) e barato de reter. Essa parte existe; é a promessa do engine pro resto do desenho.

**Um fixture capturado de tráfego.** Uma sequência reproduzível de requests, gerada sob uma seed conhecida pelo [`traffic-gen`](https://github.com/helmedeiros/traffic-gen) e guardada em disco. O fixture é o que tornaria o replay determinístico do lado do input: toda rodada veria as mesmas requests, na mesma ordem, com os mesmos valores de facts. O `traffic-gen` é desenhado pra isso — as portas `Generator` e `Poster` separam geração de emissão, e um terceiro sink (o modo Capture) escreve o fixture — mas ainda não rodei uma captura em escala de produção contra um workload de pricing real.

**Um rule set candidato.** O que é a mudança proposta. Um arquivo YAML que o time escreveu, validou e compilou, mas ainda não shippou. O candidato pode diferir do ativo por uma regra, por mudança de priority, ou por reescrita inteira — o desenho deveria lidar com os três do mesmo jeito.

**Um diff engine.** Um programa pequeno que carrega os dois snapshots, dirige os dois engines com o mesmo fixture, captura as explicações de ambos, e computa um diff: igual/diverge por request, deslocamento por campo, mudança de taxa de disparo por regra, impacto por persona, comparação de p99 de latência.

O diff é o artefato que tenho querido em toda reunião disputada de pricing desde abril. A discussão daquele dia não terminou porque tínhamos um número pra apontar; terminou porque dois sêniores concordaram em discordar com cuidado. Um replay teria dado à sala um número. É o propósito inteiro do desenho.

## A arquitetura que tô esboçando

A fiação do laboratório é o mesmo formato da fiação do shadow mode com o relógio de parede removido.

{{< plantuml title="Replay: dois engines, mesmo fixture, diff determinístico" >}}
@startuml
skinparam shadowing false
skinparam componentStyle rectangle
skinparam defaultFontName "Helvetica"

rectangle "Snapshot ativo\nsha256:7b3f...\n(bre-go ExportSnapshot)" as A
rectangle "Snapshot candidato\nsha256:9d12...\n(construído de candidate.yaml)" as N
rectangle "Fixture de tráfego\n3M de requests, seed 20250521\n(traffic-gen Capture)" as F
rectangle "Runner de replay\ncarrega os dois, dirige os dois,\ncaptura explicações" as R
rectangle "Relatório de diff\npor request, por campo,\npor persona, por regra" as D

A --> R
N --> R
F --> R
R --> D
@enduml
{{< /plantuml >}}

O runner de replay é pequeno. O formato que tenho no caderno:

```go
type ReplayRun struct {
    ActiveSnapshot    string  // caminho ou hash de conteúdo
    CandidateSnapshot string
    Fixture           string  // caminho pro arquivo de fixture capturado
    Sink              DiffSink // pra onde vai o diff por request
}

func (r *ReplayRun) Run(ctx context.Context) (Report, error) {
    active, err := indexed.LoadCompiledSnapshot(r.ActiveSnapshot, r.callbacks())
    if err != nil { return Report{}, fmt.Errorf("active: %w", err) }
    candidate, err := indexed.LoadCompiledSnapshot(r.CandidateSnapshot, r.callbacks())
    if err != nil { return Report{}, fmt.Errorf("candidate: %w", err) }

    fixture, err := traffic.OpenFixture(r.Fixture)
    if err != nil { return Report{}, fmt.Errorf("fixture: %w", err) }
    defer fixture.Close()

    report := NewReport(r.ActiveSnapshot, r.CandidateSnapshot, r.Fixture)
    for req := range fixture.Requests() {
        facts := factsFromRequest(req)

        activeResult, activeExp, _ := executeWithExplanation(ctx, active, facts)
        candidateResult, candidateExp, _ := executeWithExplanation(ctx, candidate, facts)

        diff := classify(activeResult, candidateResult, activeExp, candidateExp)
        report.Add(req, diff)
        r.Sink.Write(ReplayRecord{
            CorrelationID: req.CorrelationID,
            Persona:       req.Persona,
            Active:        summarise(activeResult, activeExp),
            Candidate:     summarise(candidateResult, candidateExp),
            Diff:          diff,
        })
    }
    return report.Finalize(), nil
}
```

Duas propriedades desse desenho têm que valer pra que o diff mereça confiança.

**Sem dependência de wall-clock.** O replay não pode consultar tempo. Os snapshots são imutáveis. O fixture é determinístico. Todo Execute é função pura de `(snapshot, facts) → result`. Uma segunda rodada do mesmo replay deveria produzir relatórios byte-idênticos. É isso que tornaria o diff um fato em vez de um snapshot.

**Os dois engines no mesmo caminho.** Mesmo Execute. Mesmo stack de listener. Mesmo schema de explicação. O diff seria computado sobre um output uniforme. Mudança no caminho do engine não deveria enviesar a comparação; o engine deveria ser o mesmo dos dois lados, só o snapshot diferindo.

O replay rodaria offline. Não teria botão de QPS. O runner consome o fixture o mais rápido que a máquina consegue rodar dois engines lado a lado. No laptop em que tô escrevendo, meu protótipo contra dado sintético roda um fixture de 3 milhões de requests em uns quatro minutos pra um engine de 100 regras. Num runner de CI com mais cores, minha estimativa de cabeça é noventa segundos. Não medi isso contra um workload de pricing real em escala.

## O que o diff mediria

Uma comparação de shadow mode é por-request e esquecida — loga o que aconteceu numa request live e agrega depois. Um diff de replay seria por-request *e* agregado desde o começo. O relatório que venho esboçando preenche cinco tabelas.

A primeira tabela é a manchete:

```
REPLAY  pricing-engine v0.18.4 (candidato)
        contra pricing-engine v0.18.3 (ativo)
Fixture q2_2025_seed_20250521.bin  (3.000.000 requests)

Resultado              Quantidade   Taxa
igual                  2.973.184    99,11%
fun_eq_regras_diff     18.294       0,61%
diff_esperado          7.610        0,25%
diff_inesperado        898          0,03%
erro_candidato         14           0,00%
```

A segunda é o deslocamento por campo. Pra cada campo que o resultado carrega, o diff calcularia como a distribuição de valor mudou entre ativo e candidato. Em pricing, é onde o impacto de receita de fato mora.

```
DESLOCAMENTOS POR CAMPO
campo                     média ativo    média candidato    Δ        Δ%
markup_percentage         3,42           3,48               +0,06    +1,75%
base_price                102,13         102,13              0,00     0,00%
provider                  (categórico)   (categórico)       —        —
```

A terceira é o impacto por persona. O fixture de tráfego carregaria metadado de persona; o diff agregaria sobre. É a tabela que tenho querido colocar na frente da reunião de abril.

```
IMPACTO POR PERSONA
persona                   rev/req ativo   rev/req candidato   Δ%
berlin_commuter           0,75            0,76                +1,3%
italian_holiday_planner   2,40            2,18                -9,2%   ← investigar
cross_border_business     3,21            3,27                +1,9%
long_tail                 1,04            1,05                +1,0%
```

A quarta é o diff de taxa de disparo por regra. Quais regras mudaram em frequência de disparo?

```
MUDANÇAS DE TAXA DE DISPARO POR REGRA (significativas)
regra                              taxa ativo   taxa candidato    Δ pp
short_lead_time_markup_de          0,124        0,124              0,00
italian_holiday_seasonal_markup    0,038        0,024             -1,40
spring_promotion_override          —            0,011             nova
```

A quinta é performance:

```
LATÊNCIA
                       p50 ativo     p50 candidato    Δ        p99 ativo   p99 cand   Δ
Execute total          0,41ms        0,43ms           +0,02    2,81ms      2,93ms     +0,12
matcher indexed        0,18ms        0,18ms            0,00    1,20ms      1,21ms     +0,01
composer               0,04ms        0,06ms           +0,02    0,21ms      0,31ms     +0,10
```

Cada uma das cinco tabelas responderia a uma pergunta que o time provavelmente vai fazer. A manchete diria se o candidato é amplamente seguro. Os deslocamentos por campo diriam o impacto em receita ou experiência. O impacto por persona diria onde o impacto cai. A taxa de disparo por regra diria por quê. A latência diria se o candidato é shippável do ponto de vista de performance.

A força caça-bug do relatório estaria na fatia inesperada. *0,03% de diff inesperado* sobre três milhões de requests são 898 requests; aquelas 898 são exatamente as que o time deveria investigar antes de shippar. Cada uma teria a explicação ativa, a explicação candidata, e os facts da request; carregar qualquer delas num debugger seria uma query contra o sink do replay.

## Determinismo, e o que ele pagaria

A propriedade mais consequente do desenho é determinismo. Mesmos snapshots, mesmo fixture, mesmo diff. Byte-idêntico, entre máquinas, entre semanas.

Três coisas que o determinismo pagaria.

**Review viraria diff.** Um PR que propõe mudança de regra poderia ser obrigado a incluir um relatório de replay. O revisor leria o diff. O revisor não precisaria raciocinar se a mudança é segura; leria o que a mudança *fez* contra o tráfego do trimestre passado. A heurística do revisor viraria "os impactos por persona são o que o autor afirmou?"

**Regressão viraria difícil de esconder.** Se um refactor do engine drifa o comportamento, um replay contra o snapshot existente expõe antes do refactor mergear. O time do engine poderia incluir uma rodada de replay no CI sobre um fixture pequeno; o teste seria uma asserção comportamental sobre milhões de requests em vez de um unit test sobre um caminho.

**Compliance viraria tratável.** Quando o regulador faz a mesma pergunta que o auditor fez no Post 7 — *por que esse cliente foi cobrado desse jeito?* — a resposta seria um replay contra o snapshot daquela data e os facts da request do fact log. A propriedade de reprodutibilidade que a explicação já carrega seria amarrada a um *input* reproduzível também.

O custo são o snapshot e o fixture. Snapshots são produzidos pelo engine automaticamente — `ExportCompiledSnapshot` do `bre-go` é 50% menor que o JSON e 2,93× mais rápido de carregar em 10 000 regras. Fixtures seriam produzidos pelo `traffic-gen` a partir de um arquivo de cenário e uma seed; pequenos (MBs pra centenas de milhares de requests), reproduzíveis, versionáveis.

Os dois inputs já existem como primitivas de engenharia. O runner que casa eles é o que ainda não construí.

## Detecção de outlier

Número agregado esconde outlier. Um deslocamento médio de 1,75% em markup pode ser 1,75% em toda a base ou 0% em 99% do tráfego e 175% de deslocamento em 1%. O sink do replay escreveria registro por request; o relatório caminharia neles buscando o segundo caso.

As passadas de outlier que tô planejando:

**Outlier por campo.** Pra cada campo no resultado, computa o delta por-request entre ativo e candidato. Ordena por delta absoluto. O top 0,1% é a cauda. A cauda é onde o pior comportamento do candidato moraria.

**Outlier por persona.** Pra cada persona, recomputa os números manchete (deslocamento médio, mudança de taxa de disparo). Persona cujo deslocamento médio passa de 2σ da média geral seria sinalizada.

**Outlier por regra.** Regra cuja taxa de disparo mudou mais que um threshold seria sinalizada. Regra que some inteira do candidato seria sinalizada. Regra nova que dispara acima de uma taxa de threshold seria sinalizada.

Essas passadas são baratas — no meu protótipo, da ordem de um minuto sobre um replay de 3 milhões de requests. As horas-engenheiro que poupariam na investigação, toda vez, são a razão de construir desde o começo em vez de pendurar depois.

## O que replay não faria

Três coisas que replay não resolve, e que às vezes eu me pego achando que talvez resolva.

**Replay não substituiria shadow mode.** O fixture é capturado de uma seed conhecida; carrega a distribuição que o time escolheu. Produção carrega a distribuição que o time não escolheu. Um candidato que passa em replay ainda pode se comportar mal na forma de input que só produção produz. Shadow mode pega isso. Replay é o laboratório; shadow mode é o campo.

**Replay não substituiria teste.** O diff de replay é agregado; a suíte de teste é por cenário. A suíte de teste diz *pra berlinense indo trabalhar a quatro dias da partida, o markup tem que ser 5%*. O replay diz *sobre três milhões de requests, o candidato sobe o markup médio em 0,06pp*. Os dois são úteis. Nenhum substitui o outro.

**Replay não substituiria pensar na mudança.** O diff é um snapshot de impacto. Não te diz se o impacto é o que o negócio quer. Um candidato que sobe receita em 1,3% e desloca mix em direção a italianos planejando férias em 9% pode ser um candidato que o time aprova; pode ser um que o time rejeita. O replay exporia o trade-off; o time ainda seria dono da decisão.

O enquadramento em que cheguei enquanto trabalho esse desenho: replay é o jeito de maior largura de banda de comunicar o impacto de uma mudança de regra pras pessoas que têm que aprovar. O diff é o artefato. O argumento que ele encerraria é o valor. A razão de eu ainda estar trabalhando nisso é que largura de banda é exatamente o que a reunião de abril não teve.

## O que esse relatório habilitaria

Três workflows que o desenho suportaria limpos, quando existir.

**Review de impacto pré-ship.** Todo rule set candidato produz um relatório de replay antes de mergear. A descrição do PR carrega a manchete e a tabela por persona. O revisor lê os dois. O merge acontece ou não. É o workflow que construiria primeiro.

**Retrospectiva trimestral.** No fim de cada trimestre, o time roda o snapshot *ativo* do fim do trimestre contra um *fixture capturado* do trimestre anterior. O diff é o impacto real das mudanças de regra que shipparam no trimestre, medido contra os inputs que essas mudanças deviam tratar. O relatório vira a evidência do time do que o trimestre realizou.

**Análise contrafactual.** "O que teria acontecido se a gente não tivesse shippado a regra X em março?" Desabilita a regra X no snapshot, replay contra o fixture do Q1, lê o diff. O contrafactual é o diff. A conversa que segue é ancorada em medição, não em memória.

Cada um desses workflows é baseado em opinião sem o laboratório. Cada um vira baseado em dado com ele. O replay faria as conversas de pricing do time virarem de "eu acho que isso vai" pra "o diff mostra que isso fez".

## O laboratório e o campo juntos

Um workflow limpo pra qualquer mudança de regra candidata viraria:

1. Escreve o candidato, com a nota de impacto esperado que vai junto.
2. Roda um replay contra o fixture do trimestre passado e o snapshot do trimestre passado. Compara o diff com a nota de impacto esperado. Se discordam, revisa o candidato ou revisa a expectativa.
3. Roda shadow mode em tráfego de produção por uma a duas semanas. Observa a taxa de divergência inesperada. Cava nos outliers.
4. Se o shadow concorda com o replay (ou a divergência tem explicação), promove o candidato a ativo. Snapshota o novo ativo. O ciclo recomeça com o próximo candidato.

```
candidate.yaml + active.snapshot
        │
        ▼
   ┌─────────┐        ┌──────────┐
   │ Replay  │ ─passa─▶│ Shadow  │ ─passa─▶ Promove
   │  (lab)  │        │ (campo)  │
   └─────────┘        └──────────┘
        │                  │
        │                  │
        ▼                  ▼
   relatório de diff   relatório de divergência
```

Os dois estágios pegariam bugs diferentes. Replay pegaria problema sistemático — regra que dispara errado sobre o fixture, política de composição que muda campo de jeito inesperado, regressão de performance sobre o caminho médio. Shadow pega problema contextual — regra que dispara errado num segmento de cliente que o fixture sub-representa, ação que depende de algo que só produção toca.

A combinação seria a resposta pra "isso tá seguro pra shippar?" Nenhum sozinho basta. Os dois juntos, na minha leitura, sim.

## O que vem a seguir

O próximo post dá o passo arquitetural pra cima: a diferença entre rule engine e decision engine, e quando cada um é a ferramenta certa. Replay foi o ato de fechamento da série do engine nas minhas notas — o momento em que regra, matcher, explicação e geração de tráfego se encontrariam. O próximo post pergunta o que vem quando regra não é suficiente: quando política, modelo, restrição e experimento têm que ser coordenados, e o formato simples de "facts entram, ação sai" de um engine tem que crescer pra algo mais.

Depois disso a gente vai pra manutenibilidade, os dez erros que shippei, e o que construiria diferente hoje. Os últimos três posts são a metade retrospectiva da série — menos sobre a próxima camada, mais sobre tudo que a gente construiu e os buracos, como esse, que ainda venho trabalhando.

## A lição

Replay transformaria discussão de pricing de opinião em diferença observável. Faria isso casando um snapshot guardado, um fixture capturado, e um rule set candidato num diff determinístico. O diff seria o artefato que o time revisa. O diff seria o artefato que o regulador vê. O diff seria o artefato em que a retrospectiva do próximo trimestre começa.

O custo são o snapshot, o fixture, e um runner pequeno. Os dois primeiros existem como primitiva. O runner é o que venho estudando — o que ele tem que computar, que relatório tem que emitir, que modo de falha tem que expor. Tenho protótipo contra dado sintético. Ainda não rodei contra um workload de pricing em produção.

A reunião de abril não terminou com um diff. Terminou com os dois ainda meio confiantes no próprio modelo, um plano cauteloso de rollout, e uma revisão de follow-up seis semanas depois. O número que tenho querido colocar naquela sala desde então é o que um replay produziria. Não construí pra um sistema de pricing em produção ainda. Estudei o bastante pra saber que formato teria, e escrever é o jeito mais barato de descobrir o que não vi.
