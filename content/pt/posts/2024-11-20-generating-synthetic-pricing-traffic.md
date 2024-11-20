---
title: "Gerando Tráfego Sintético de Pricing"
subtitle: "Tráfego sintético não é dado falso. É pressão controlada nas suposições que o seu dado de produção, por definição, não exercita."
author: helio
layout: post
date: 2024-11-20T10:00:00+00:00
series:
  - pricing-engineering
series_order: 8
categories:
  - Engineering
  - Pricing
  - Architecture
tags:
  - pricing
  - traffic-generation
  - load-testing
  - architecture
  - go
  - simulation
description: "Tráfego de produção carrega o viés da semana passada. Tráfego sintético carrega os cenários que você precisa testar antes deles acontecerem. Esse post é sobre gerar de propósito."
---

O primeiro teste de carga que rodei contra um engine de pricing novo usou quatro milhões de requests do log de produção. O plano era simples: replayar ontem, ver se o engine novo aguenta. O plano funcionou. O engine aguentou. A gente shippou.

Dois dias depois um mercado único spikeu tráfego em 8x do normal por causa de um feriado, e o engine caiu. O replay tinha carregado o mix de mercados de ontem. Ontem não tinha tido o spike do feriado. O teste tinha sido cuidadoso sobre uma pergunta que a gente já tinha respondido e silencioso sobre a que precisávamos responder.

Esse é o resto desse post. Tráfego de produção é o default errado pra testar um sistema de pricing, porque tráfego de produção é o mix de input *de ontem*. O sistema de pricing tem que sobreviver ao mix *de amanhã* — e às mudanças de regra que o time tá pra shippar, e ao mercado que a empresa tá pra entrar, e ao modo de falha que o engenheiro tá preocupado às 2 da manhã. Nenhum desses tá no log de prod.

A referência pro resto da série muda pra [`traffic-gen`](https://github.com/helmedeiros/traffic-gen), um binário Go pequeno que eu mantenho e que sintetiza formato de request de pricing em QPS e mix de persona configuráveis. É o segundo dos dois repositórios em volta dos quais a série foi construída. Onde o `bre-go` é sobre avaliar regra, o `traffic-gen` é sobre dar input pro engine avaliar.

## Por que dado de produção é o default errado

Três coisas dão errado quando log de produção vira o input da sua estratégia de teste.

**Carrega a distribuição de ontem.** O mix de reserva no seu log é o mix que já aconteceu. O mix que você precisa lidar é o que tá pra acontecer — estação diferente, campanha diferente, pricing diferente do concorrente, mudança regulatória diferente. Teste que replaya a distribuição da semana passada prova que o engine sobreviveu à semana passada. É silencioso sobre o resto.

**São raspados dos campos que você de fato precisa.** Customer ID se foi. E-mail se foi. Forma de pagamento se foi. Tudo que tem cara de PII foi censurado pelo pipeline de logging, o que quer dizer que as condições em que o rule engine matcheia — segmento, device, canal — estão parciais. O seu replay tá replayando fragmento da request, e o fragmento nem sempre é a parte que a regra ligava.

**Faltam os cenários que você precisa estressar.** O mercado novo abre na terça. A regra nova só dispara em fim de semana no Q4. O compliance override nunca de fato disparou em produção. Nenhum desses cenários tá no log de prod porque, por definição, ainda não aconteceram. Testar exige sintetizar.

Da primeira vez que você descobre, o instinto é voltar ao pipeline de log e pedir mais retenção, menos censura, mais volume. É o fix errado. O fix certo é parar de usar log de prod como input de teste e começar a gerar tráfego que se forma em volta da pergunta que você tá tentando responder.

## O que tráfego sintético de fato é

Tráfego sintético é formato de request *gerado*, com distribuição controlada, que o sistema sob teste consome como se fosse real. A palavra "sintético" carrega conotação de "falso", que é a leitura errada. A leitura certa é *deliberadamente formado*. Cada request é plausível — tem os mesmos campos de uma real, os mesmos tipos, as mesmas faixas — mas o *mix* é decidido pelo time, não pelo que a produção por acaso produziu.

Um gerador de tráfego tem três trabalhos:

**Produzir formato de request realista.** O struct Request bate com o contrato do engine. Os mercados são códigos ISO reais. Days-to-departure é não-negativo. Os canais são os que o engine conhece. Uma request que não valida contra o schema de produção é uma request que exercita o caminho de *validação* do engine, que é um teste diferente do que você queria.

**Samplear de uma distribuição controlada.** Cada campo tem uma distribuição. Mercado é escolha com peso entre os mercados em que o time opera. Days-to-departure é distribuição de cauda longa centrada no lead time típico. Mix de canal é com peso pro canal em que o time tá focando esse trimestre. O formato da distribuição é a hipótese do teste.

**Disparar carga numa taxa configurável.** Requests por segundo. Padrões de burst. Carga sustentada. O botão de QPS é desacoplado do botão de geração — o gerador produz duas vezes mais formato do que o poster manda, com o poster escolhendo o que manda, ou o poster replaya um output pequeno do gerador em taxa alta. A arquitetura hexagonal do `traffic-gen` separa essas duas preocupações: `Generator` produz formato de Request; `Poster` manda em QPS. Eles ajustam independente.

Uma request que sai do gerador é indistinguível de uma real no fio. O que é diferente é o *mix*. O mix é o experimento.

## Distribuição: formato em vez de ruído

O erro mais comum em geração de tráfego é modelar todo campo como sample uniforme aleatório sobre a faixa permitida. Uniforme aleatório produz tráfego que não tem cara de nada real. O matcher bate nos branches raros em taxa uniforme; bug raro aparece. Bug comum não.

O que você em geral quer é o *formato* de produção — não o dado, o formato — sobreposto com o cenário que você quer estressar.

Uma taxonomia útil:

| Campo | Formato em produção | Gerador útil |
| --- | --- | --- |
| `market` | Pesado em 3-5 mercados, cauda longa | Escolha com peso, configurável por cenário |
| `days_to_departure` | Cauda longa; mediana ~21, 5% das reservas abaixo de 7 | Log-normal ou Weibull, parametrizado |
| `channel` | Bimodal: web e mobile dominam, outros <5% | Escolha com peso |
| `customer_segment` | Cauda longa de segmento, top 5 = 80% do tráfego | Sample power-law |
| `base_price` | Assimétrico à direita, valores muito altos eventuais | Log-normal |
| `regulated_market` | Binário, raro (~2% em produção) | Bernoulli, taxa configurável |

Cada distribuição é uma de um conjunto pequeno de formas padrão — uniforme, escolha com peso, Bernoulli, log-normal — parametrizada pra produzir o mix que o teste pede. O trabalho do gerador é tornar esses parâmetros botões explícitos.

```yaml
# Um arquivo de cenário que o time revisa.
name: "Q4 holiday spike on DE rail"
qps: 5000
duration: 10m

facts:
  market:
    type: weighted_choice
    weights:
      DE: 0.55          # 8x do normal — é o estresse
      FR: 0.15
      IT: 0.15
      ES: 0.10
      _other: 0.05

  channel:
    type: weighted_choice
    weights:
      rail:  0.65
      bus:   0.20
      ferry: 0.15

  days_to_departure:
    type: log_normal
    median: 14
    sigma: 0.8
    min: 0

  device:
    type: weighted_choice
    weights:
      mobile: 0.75      # tráfego de feriado mobile-pesado
      web:    0.25

  regulated_market:
    type: bernoulli
    p: 0.02
```

Esse arquivo é uma hipótese que o time concordou. *No Q4, tráfego rail de DE spikeia 8x e tende a mobile.* O engine consome o tráfego gerado e produz explicação; o teste afirma o que deve ser verdade sob aquela carga.

YAML de cenário é coisa diferente de YAML de regra. A regra diz o que o engine deve fazer. O cenário diz o que o mundo tá fazendo. Os dois têm a mesma propriedade — versionado, revisável, com dono — mas evoluem em cadências diferentes.

## Persona: tornar a abstração concreta

Persona é um padrão nomeado de facts que produz um tipo reconhecível de request. Persona existe porque "escolha com peso sobre mercado e device" é fácil de esquecer; "berlinense indo no trabalho de mobile" não.

O formato:

```yaml
personas:
  - name: berlin_commuter
    weight: 0.35
    facts:
      market: DE
      channel: rail
      device: mobile
      days_to_departure:
        type: weighted_choice
        weights: { 0: 0.40, 1: 0.30, 2: 0.20, 3: 0.10 }
      base_price:
        type: log_normal
        median: 25
        sigma: 0.3

  - name: italian_holiday_planner
    weight: 0.15
    facts:
      market: IT
      channel: ferry
      device: web
      days_to_departure:
        type: log_normal
        median: 45
        sigma: 0.4
      base_price:
        type: log_normal
        median: 120
        sigma: 0.6

  - name: cross_border_business
    weight: 0.10
    facts:
      market:
        type: weighted_choice
        weights: { DE: 0.4, FR: 0.4, NL: 0.2 }
      channel: rail
      device: web
      days_to_departure:
        type: weighted_choice
        weights: { 1: 0.5, 2: 0.3, 3: 0.2 }
      base_price:
        type: log_normal
        median: 180
        sigma: 0.5
```

Três personas com pesos que somam menos que 1 é intencional: o 0.4 restante de tráfego vem de uma persona "cauda longa" padrão que usa as distribuições mais amplas. O time agora consegue falar do teste em termo humano: *o cenário Q4 é 35% berlinenses indo trabalhar, 15% italianos planejando férias, 10% negócios transfronteira, e 40% de cauda longa*.

Persona é a abstração que deixa produto e engenharia terem a mesma conversa. O dono de produto lê "berlinense indo trabalhar" e sabe que cenário tá olhando. O engenheiro lê "berlinense indo trabalhar" e vê a distribuição. O teste roda o mesmo código independente.

No `traffic-gen`, persona é uma camada em cima do gerador `randommix`: cada persona é um bundle nomeado de distribuição em nível de campo; o mix é uma escolha com peso entre geradores de persona.

## Cenário: tráfego, regra, e um resultado esperado

Um cenário é um experimento completo. Empacota um formato de tráfego, um rule set, e uma expectativa. Rodar o cenário é atividade determinística; ler o output é comparar contra a expectativa.

```yaml
scenario: q4_de_holiday_spike
description: |
  Valida que o markup de short-lead-time de DE rail fica correto
  sob 8x do peso normal de mercado, que a distribuição de bucket
  do matcher indexed segue saudável, e que o p99 de latência do
  Execute fica abaixo de 5ms.

traffic: scenarios/q4_de_holiday_spike.yaml   # personas + distribuição
rules:   fixtures/2024-q4-candidate.yaml      # o rule set candidato
duration: 10m
qps: 5000

expectations:
  result:
    - field: markup_percentage
      assertion: |
        Pra toda request de berlinense indo trabalhar com days_to_departure < 7,
        o resultado tem que incluir short_lead_time_markup_de e
        germany_baseline_markup. Soma tem que ser 5.0%.

  performance:
    - p50_execute_ms: { lt: 1.0 }
    - p99_execute_ms: { lt: 5.0 }
    - candidate_set_size_p99: { lt: 20 }

  rule_hygiene:
    - shadowed_rule_warnings: { eq: 0 }
    - failed_action_rate: { lt: 0.001 }
```

Esse arquivo é o plano de teste. O gerador de tráfego puxa a carga. O engine produz explicação. Um runner de cenário agrega sobre as explicações e checa as expectativas. O output é pass / fail, com diff estruturado quando algo viola uma expectativa.

A disciplina que torna cenário útil é que ele mora em version control, é revisado em PR, e roda em todo release. Um cenário que rodou limpo por seis meses e começa a falhar amanhã é o aviso mais cedo que o time tem de que alguma coisa drifou — no rule set, no engine, ou no entendimento que o time tem do mundo.

## Reprodutibilidade: seed e fixture

Um gerador de tráfego que produz output diferente em cada run é um gerador que você não consegue debugar. O formato que envelheceu melhor pra mim é um gerador que pega uma seed e produz requests *idênticas*, na mesma ordem, em todo run com a mesma seed.

```sh
git clone https://github.com/helmedeiros/traffic-gen
cd traffic-gen

# Run reproduzível: cada request é determinada pela seed.
./traffic-gen \
  --scenario scenarios/q4_de_holiday_spike.yaml \
  --seed 20241120 \
  --target http://localhost:8080/price \
  --qps 5000 \
  --duration 10m
```

A seed é a diferença entre um teste que você consegue debugar e um teste que zomba de você. Se uma request dispara um bug na terça, a mesma seed reproduz na quarta. O bug é repetível; a investigação é limitada; o teste de regressão que você escreve pra prender o fix consegue hardcodar a seed e reproduzir a request ofensora indefinidamente.

Um segundo padrão que paga de volta: capturar as primeiras N requests como arquivo de fixture. O fixture é dump binário ou JSON das primeiras 1000 requests que o gerador produziu sob uma seed dada. O fixture é pequeno (poucos MB), versionável, e exatamente reproduzível entre máquinas. Testes que devem rodar em todo PR usam o fixture; teste de carga que roda à noite usa o gerador com a seed.

```go
// traffic-gen expõe um modo Capture pra geração de fixture.
gen := traffic.NewGenerator(scenario, traffic.WithSeed(20241120))
fixture := traffic.Capture(gen, 1000)
fixture.WriteFile("testdata/q4_holiday_first_1000.bin")
```

No `traffic-gen`, as portas `Generator` e `Poster` são separadas justamente pra que o mesmo output do gerador alimente um Poster (pra rodar live contra um serviço), um Capture (pra geração de fixture), e um sink de Replay (pro trabalho de shadow mode no próximo post). Cada modo de output é um adaptador atrás de uma porta; o gerador não precisa saber quem tá do outro lado.

## A arquitetura: hexagonal, por desenho

O desenho do `traffic-gen` é um formato único carregado em três fronteiras.

{{< plantuml title="traffic-gen: gerador produz formato, sink consome, botão de QPS mora no sink" >}}
@startuml
skinparam shadowing false
skinparam componentStyle rectangle
skinparam defaultFontName "Helvetica"

rectangle "Arquivo de cenário\n(personas, distribuição)" as SF
rectangle "Porta Generator\nproduce(seed) → Request" as G
rectangle "Adaptador randommix\nweighted choice + log-normal" as GA

rectangle "Porta Sink\nconsume(Request)" as S
rectangle "HTTP Poster\nPOST pro target\ncontrolado por QPS" as SP
rectangle "Captura de fixture\nescreve em disco" as SF2
rectangle "Sink de Replay\n(usado nos posts 9, 10)" as SR

SF --> GA
GA ..|> G
G  --> S
S  <|.. SP
S  <|.. SF2
S  <|.. SR
@enduml
{{< /plantuml >}}

Duas propriedades merecem o destaque.

**O botão de QPS tá no sink, não no gerador.** O gerador produz formato o mais rápido que consegue; o sink decide quão rápido mandar. Essa separação é o que deixa o mesmo gerador puxar um teste de carga live em 10 000 QPS e uma captura determinística de fixture em zero QPS. Gerador que tenta fazer rate-limit próprio acaba gargalado em loop de time.Sleep, que não é o gargalo que você quer quando tá testando 10 000 QPS.

**O sink é interface, não cliente HTTP.** O HTTP poster é um adaptador. A captura de fixture é outro. O sink de replay — em que o próximo post se apoia — é um terceiro. Cada sink é um arquivo pequeno atrás da mesma interface. O gerador não precisa saber qual sink tá do outro lado; o teste não precisa saber como o gerador produziu o formato.

O custo é dois pacotes extras no dia um. O benefício é que o mesmo código puxa teste de carga, geração de fixture, e replay até o post de simulação dessa série.

## O que "pressão controlada" de fato significa

O enquadramento em que cheguei, depois de alguns ciclos de errar isso, é que tráfego sintético é *pressão controlada nas suposições do sistema*.

Um engine de pricing tem suposições embutidas. O matcher supõe que a maioria das regras vai ter pelo menos um termo indexável. O composer supõe que conflito de resolução vai ser raro. O loader supõe que arquivo de regra vai ser pequeno. Cada suposição tá correta no tráfego de ontem. Cada suposição pode estar errada no tráfego de amanhã.

Tráfego sintético é o jeito de botar pressão em cada suposição de propósito. Um arquivo de cenário que diz "o que acontece quando 60% do tráfego é num mercado novo sem regra?" é o jeito de descobrir que o caminho de warning do matcher pra conjunto candidato vazio nunca foi exercitado. Um cenário que diz "o que acontece quando o arquivo de regra cresce pra 10 000?" é o jeito de descobrir que o tempo de Build do engine indexed atravessa um limite de SLA que o time não sabia que existia.

O output desses cenários não é "o engine passou". O output é *qual suposição o engine tem, e se a suposição sobrevive à pressão*. Cenário em que o engine passa é uma suposição confirmada. Cenário em que o engine falha é uma suposição pra repensar.

```
# Output típico de uma rodada de cenário, no CI do time:
scenario        q4_de_holiday_spike
duration        10m0s
total_requests  3_000_000

result_assertion          PASS  (3_000_000 / 3_000_000 matcham)
p50_execute_ms            PASS  (0.41ms,  limite 1.0ms)
p99_execute_ms            FAIL  (6.82ms,  limite 5.0ms)
candidate_set_size_p99    PASS  (12,      limite 20)
shadowed_rule_warnings    PASS  (0)
failed_action_rate        PASS  (0.0001)

ARTEFATOS
  - explicações sampleadas (1 em 10_000):    120 registros
  - explicações de outlier de p99 (top 1%):  30_000 registros
  - histograma de tamanho de candidato:       anexo
  - distribuição de hit-count por regra:      anexa
```

A falha de p99 vira investigação: a avaliação de qual regra tá lenta? Qual condição é o gargalo? É o tamanho de bucket do índice, o loop por campo do composer, ou o callback de ação? A próxima camada de artefato — as explicações sampleadas e a latência por estágio do Post 7 — é onde a resposta mora.

## Antipadrões que shippei e vi shippar

Três erros de geração de tráfego que parecem razoáveis e não são.

**O gerador "uniforme aleatório".** Cada campo sampleado uniforme sobre a faixa. Parece justo. Parece sem viés. Produz tráfego que exercita branches raros em taxa rara, branches dominantes em taxa moderada, e a distribuição real de produção em taxa zero. Os bugs que shippam pra produção são os bugs nos branches dominantes; uniforme aleatório não vai achar.

**O gerador "log de prod amplificado".** Pega log de ontem, multiplica por 10, replaya. Idêntico ao teste de carga do caso de abertura. Carrega os mesmos vieses da produção; acha os mesmos bugs que a produção já achou. Útil pra regressão de performance; inútil pra exploração de cenário.

**O gerador "cada time escreve o próprio".** Cada time escreve um gerador sintético pequeno pro próprio serviço. Os geradores todos produzem schemas levemente diferentes, distribuições levemente diferentes, defaults levemente diferentes. Comparação de shadow mode entre serviços vira impossível porque os inputs não estão alinhados. Um gerador compartilhado, mesmo que mínimo, remove uma classe de confusão entre serviços.

O primeiro é bug no modelo de distribuição. O segundo é bug na escolha de input. O terceiro é bug de ownership. Cada um custou pros times trimestres de esforço que um desenho um pouco mais deliberado teria poupado.

## O que o time ganha quando isso tá construído

Três benefícios duradouros.

**O time consegue posicionar perguntas com antecedência.** *O que acontece se o lançamento da semana que vem botar 60% do tráfego num mercado novo?* vira arquivo de cenário, não oração. O cenário roda contra um rule set candidato; o time vê o impacto antes do lançamento.

**O time consegue reproduzir carga parecida com produção de forma determinística.** *Roda o cenário Q4 com seed 20241120* produz os mesmos 3 milhões de requests todo dia. Regressão de performance vira mensurável. A reclamação "o engine ficou mais lento" vira a afirmação "p99 foi de 4.1ms pra 5.8ms entre os commits X e Y".

**O time consegue conectar tráfego à explicação.** Toda request sintética produz uma explicação. O gerador de tráfego carrega metadado sobre qual persona produziu cada request. O agregador responde "pra berlinenses indo trabalhar, qual foi o markup mediano?" — e a resposta é query na explanation store, não chute no dashboard.

O custo é um binário Go pequeno, um formato YAML de cenário, uma interface Go pro sink, e a disciplina de escrever o cenário. Modesto. O benefício é o resto da série — shadow mode, simulação por replay, e o workflow de avaliação de impacto que amarra tudo.

## O que vem a seguir

O próximo post é shadow mode — rodar um caminho de pricing candidato ao lado do ativo, na mesma request live, comparando os outputs sem afetar o cliente. Shadow mode é o que fecha o loop entre geração de tráfego e produção. O gerador estressa o candidato offline; shadow mode testa o candidato online, no mix real de tráfego, antes do candidato virar o caminho ativo.

O post seguinte é simulação por replay, que amarra `bre-go` e `traffic-gen` formalmente: um snapshot guardado do engine, um fixture capturado de tráfego, e um rule set candidato produzem uma comparação determinística de resultado. Essa comparação é a ferramenta do revisor de regra — o jeito de perguntar "o que essa mudança de fato faz?" e ter uma resposta estruturada e reproduzível.

Por enquanto, a lição é o enquadramento. Tráfego de produção é o default errado porque carrega o passado. Tráfego sintético é o default certo porque consegue carregar o futuro pra qual o time tá se preparando. O gerador de tráfego é uma peça pequena de código com papel grande: é o sistema que diz pro engine o que tá pra ser verdade.

O teste de carga de replay-de-ontem do caso de abertura foi, depois daquele incidente, aposentado. A gente manteve por uma coisa só — teste de regressão contra o bug que ele tinha perdido. Aí a gente construiu cenário pros feriados que sabíamos que vinham, pros mercados que sabíamos que abriam, e pras regras que sabíamos que entravam. O próximo spike de tráfego veio na agenda. O engine aguentou. A gente não tirou print.
