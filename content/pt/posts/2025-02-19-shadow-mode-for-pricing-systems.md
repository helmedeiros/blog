---
title: "Shadow Mode pra Sistemas de Pricing"
subtitle: "Shadow mode deixa a lógica nova estar errada em produção, em tráfego de produção, antes de um único cliente pagar pelo bug."
author: helio
layout: post
date: 2025-02-19T10:00:00+00:00
series:
  - pricing-engineering
series_order: 9
categories:
  - Engineering
  - Pricing
  - Architecture
tags:
  - pricing
  - shadow-mode
  - canary
  - architecture
  - observability
  - simulation
description: "Shadow mode roda lógica de pricing candidata ao lado do caminho ativo, na mesma request live, comparando output sem mudar o que o cliente paga. Esse post percorre o padrão, as armadilhas, e os relatórios de divergência que merecem a confiança pra fazer rollout."
---

O time tinha gastado seis semanas reescrevendo o composer de markup. A matemática era a mesma, as estruturas de dado mais rápidas, a suíte de teste verde. A gente tava se preparando pra shippar.

Rodamos shadow mode por dez dias antes.

Já no terceiro dia o relatório de divergência tinha sinalizado 0,42% das requests onde o composer novo devolvia um número diferente do velho. Não um número doidamente diferente — em geral dentro de um ou dois pontos-base. A gente cavou. A causa era um passo de arredondamento que um composer aplicava antes da soma e o outro aplicava depois. Nenhum dos dois tava "errado" no isolamento; o negócio nunca tinha sido perguntado sobre qual arredondamento preferia. O dono de produto escolheu a resposta que casava com o que os clientes tinham pago nos últimos três anos, o passo de arredondamento mudou de lugar no composer novo, e a divergência caiu pra 0,00%. A gente shippou no dia onze.

A gente também tinha descoberto, na mesma rodada de shadow, que o composer *velho* tinha um caminho de panic que ninguém nunca tinha exercitado em produção. Os logs de comparação do shadow expuseram uma request, a cada poucas horas, em que o composer velho devolvia o markup zero padrão por causa de um panic de ação numa regra que tratava correção de reembolso. O composer novo lidava com o mesmo panic devolvendo o resultado parcial, que era o correto. O bug na lógica velha era mais velho do que qualquer pessoa no time. Shadow mode mostrou pra gente comparando duas versões da verdade.

É disso que esse post trata. Shadow mode é a superfície de engenharia entre *a gente testou em CI* e *a gente roda pros clientes*. É o jeito mais barato de descobrir o que o código novo erra e o que o código velho vinha errando o tempo todo.

## O que shadow mode é

Shadow mode roda o caminho de pricing candidato ao lado do caminho ativo, na mesma request live, e compara os outputs. O cliente é servido pelo caminho ativo; o output do candidato é logado mas nunca devolvido. A comparação acontece de forma assíncrona, sobre o log de comparação, por um processo separado.

O ponto é dar exposição ao candidato com tráfego no formato de produção antes dele virar produção. Teste de CI exercita o candidato contra cenários que o time escreveu. Shadow mode exercita contra a cauda longa de inputs que o time não escreveu, não previu, e não conseguiria sintetizar.

Três propriedades definem o padrão.

**O caminho ativo não é afetado.** Os clientes são servidos por ele. A latência fica a mesma. O erro fica o mesmo. O caminho candidato roda *em paralelo*, não no lugar.

**O caminho candidato roda contra os mesmos facts.** Mesma request, mesmo correlation ID, mesma semântica de snapshot do engine (onde compartilha) ou um snapshot diferente em teste (onde não compartilha). Qualquer coisa que diverge entre os dois caminhos tem que ser atribuível *ao candidato*, não ao input.

**A comparação é offline.** A request devolve quando o caminho ativo devolve. O output do candidato é capturado e comparado depois. O cliente nunca espera pelo candidato.

Essas três propriedades são o contrato. São o que tornam shadow mode seguro de deixar ligado por semanas seguidas.

## A arquitetura

A fiação parece pequena de longe e ganha quase toda a complexidade nos detalhes.

{{< plantuml title="Shadow mode: caminho ativo serve; caminho candidato observa" >}}
@startuml
skinparam shadowing false
skinparam componentStyle rectangle
skinparam defaultFontName "Helvetica"

actor "Cliente" as C
rectangle "Gateway de API\nrequest com correlation_id" as G
rectangle "Serviço de pricing" as S
rectangle "Engine ativo\n(snapshot N)" as A
rectangle "Engine candidato\n(snapshot N+1)\n— async, fire-and-forget" as N
rectangle "Log de comparação\n(result ativo, result candidato,\ncorrelation_id, hash dos facts)" as L
rectangle "Pipeline de divergência\nagrega, classifica,\nemite relatório" as D

C  --> G : request
G  --> S : facts + correlation_id
S  --> A : Execute (sync)
A  --> S : Result
S  --> C : Response
S  -[#888]-> N : Execute (async)
A  -[#888]-> L : grava ativo
N  -[#888]-> L : grava candidato
L  --> D
D  -[#888]-> S : ajustes de feature flag (lento)
@enduml
{{< /plantuml >}}

Uma implementação ingênua chama o candidato no caminho da request, bloqueia até ele terminar, e aí compara. Essa implementação tá errada duas vezes: dobrou a latência do cliente, e qualquer panic no candidato agora é um panic na request do cliente. Um formato mais seguro:

```go
// Handler do serviço de pricing.
func (h *Handler) Price(ctx context.Context, req Request) (Response, error) {
    facts, err := h.facts.Build(ctx, req)
    if err != nil {
        return Response{}, err
    }

    // Caminho ativo: síncrono, voltado pro cliente.
    activeResult, err := h.activeEngine.Execute(ctx, facts)
    if err != nil {
        return Response{}, err
    }

    // Caminho candidato: async, nunca bloqueia a resposta.
    if h.shadow.Enabled(ctx, req) {
        go h.runShadow(ctx, req, facts, activeResult)
    }

    return responseFromResult(activeResult), nil
}

func (h *Handler) runShadow(parent context.Context, req Request,
    facts Facts, activeResult Result) {
    // Desacopla do ctx da request pra que shutdown não cancele;
    // limita com timeout próprio pra que candidato lento não empilhe.
    ctx, cancel := context.WithTimeout(
        context.Background(),
        h.shadow.Timeout,
    )
    defer cancel()
    ctx = engine.WithCorrelationID(ctx, engine.CorrelationIDFromContext(parent))

    defer func() {
        if r := recover(); r != nil {
            h.shadow.Metrics.PanicCount.Inc()
            log.Warn("candidato do shadow deu panic",
                "correlation_id", engine.CorrelationIDFromContext(parent),
                "panic", r)
        }
    }()

    candidateResult, err := h.candidateEngine.Execute(ctx, facts)
    if err != nil {
        h.shadow.Metrics.ErrorCount.Inc()
        return
    }

    h.shadow.Log.Record(ShadowRecord{
        CorrelationID: engine.CorrelationIDFromContext(parent),
        Facts:         facts.Hash(),
        Active:        activeResult,
        Candidate:     candidateResult,
        OccurredAt:    time.Now(),
    })
}
```

Três detalhes nesse código merecem o destaque.

**A goroutine do shadow tem contexto próprio.** Não herda o contexto da request. Se o contexto da request é cancelado (deadline estourado, cliente desconectado), o shadow ainda devia rodar até o fim — senão você sub-conta exatamente as requests que mais quer investigar. O contexto novo carrega timeout próprio pra que candidato pateticamente lento não acumule goroutine.

**O shadow se recupera de panic.** Panic no candidato não pode crashar o serviço. O recover emite uma métrica e uma linha de log; a request do cliente, que já voltou, fica intocada.

**Erro no candidato é gravado mas não exposto.** O caminho ativo devolveu. O candidato falhou. O time precisa saber que falhou — essa é a métrica — mas a experiência do cliente não pode ser acoplada a isso.

## O que o log de comparação carrega

O log de comparação é o artefato que o pipeline de divergência lê. Tem que carregar o bastante pra investigar, pouco o bastante pra guardar.

```go
type ShadowRecord struct {
    CorrelationID string        `json:"correlation_id"`
    OccurredAt    time.Time     `json:"occurred_at"`
    FactsHash     string        `json:"facts_hash"`     // sha256(canonical(facts))
    ActiveSnapshot    string    `json:"active_snapshot"`
    CandidateSnapshot string    `json:"candidate_snapshot"`

    Active    ResultSummary `json:"active"`
    Candidate ResultSummary `json:"candidate"`

    Divergence Divergence    `json:"divergence,omitempty"`
}

type ResultSummary struct {
    Result      json.RawMessage `json:"result"`
    FiredRules  []string        `json:"fired_rules"`
    LatencyNs   int64           `json:"latency_ns"`
}

type Divergence struct {
    Kind        string   `json:"kind"`         // result, fired_rules, latency_outlier
    Fields      []string `json:"fields,omitempty"` // pra kind=result: que campos diferem
    Severity    string   `json:"severity"`     // info, warn, alert
    Description string   `json:"description"`
}
```

O registro carrega o *resumo*, não a Explanation completa. A Explanation completa do Post 7 é guardada na explanation store pros dois caminhos; o trabalho do shadow record é ser pequeno o bastante pra varrer em agregado e apontar pras explicações quando uma investigação começa.

O hash dos facts é o que deixa o pipeline de divergência agrupar requests similares sem guardar as requests. Dois registros com o mesmo hash de facts que produziram resultado diferente são exatamente os registros que valem investigar. O hash é canonicalizado — chaves ordenadas, valores normalizados — pra que ruído de ponto flutuante em campo float não quebre o agrupamento.

## Os quatro tipos de divergência

Nem toda diferença entre ativo e candidato é bug. O pipeline de divergência deve classificar, não só reportar.

**Igual.** Mesmo resultado, mesmas regras disparadas. O candidato se comportou como o ativo. É o resultado mais comum e o que o time espera.

**Funcionalmente igual, mecanicamente diferente.** Mesmo resultado, regras disparadas diferentes. O candidato chegou na mesma resposta por um rule set diferente. É o que acontece quando um refactor consolida duas regras numa, ou quando uma regra é renomeada. Não é bug, mas é mudança que o time deve aprovar.

**Resultado diferente, esperado.** A mudança no candidato era de propósito pra mudar o resultado num subconjunto de requests. A divergência é o *sinal* da mudança funcionando. O time devia conseguir prever o formato e a taxa dessa divergência antes da rodada de shadow começar.

**Resultado diferente, inesperado.** Mesmos facts, decisão diferente, sem razão documentada. É o bug pra qual shadow mode foi construído. Toda divergência inesperada é investigação: carrega as duas explicações, compara estágio por estágio, identifica onde os caminhos se separaram.

```go
func classify(active, candidate ResultSummary,
    expectedChanges []ExpectedChange) Divergence {
    if equalResults(active.Result, candidate.Result) {
        if equalRules(active.FiredRules, candidate.FiredRules) {
            return Divergence{Kind: "equal"}
        }
        return Divergence{
            Kind: "funcionalmente_igual_regras_diferentes",
            Description: fmt.Sprintf(
                "ativo disparou %v; candidato disparou %v",
                active.FiredRules, candidate.FiredRules),
            Severity: "info",
        }
    }
    // Resultado difere. Era esperado?
    for _, ec := range expectedChanges {
        if ec.Matches(active, candidate) {
            return Divergence{
                Kind: "result_diff_esperado",
                Description: ec.Reason,
                Severity: "info",
            }
        }
    }
    return Divergence{
        Kind: "result_diff_inesperado",
        Fields: diffFields(active.Result, candidate.Result),
        Description: "investigar",
        Severity: "alert",
    }
}
```

Divergências esperadas são *registradas* por quem propôs o candidato. O formato é pequeno: *pra reservas alemãs de trem de última hora, espere o markup mudar de 5% pra 5,5%, +/- ruído*. O pipeline de divergência subtrai essas expectativas da contagem total de divergência, então a taxa de divergência *inesperada* vira a métrica que o time observa.

## O relatório de divergência

Depois de classificada, divergência precisa ser agregada num relatório que o time lê. O formato que envelheceu melhor pra mim:

```
Rodada de shadow: pricing-engine v0.18.4 (candidato)
                  contra pricing-engine v0.18.3 (ativo)
Duração:          240h (10 dias)
Tráfego:          52.143.891 requests

Resultado              Quantidade       Taxa
igual                  51.876.412       99,49%
fun_eq_regras_diff     192.030          0,37%
diff_esperado          64.221           0,12%
diff_inesperado        9.847            0,019%
erro_candidato         1.381            0,003%

DIVERGÊNCIA INESPERADA, por assinatura
  candidato dispara R7 + R12; ativo só R7              6.142 (62%)
  candidato seta markup_percentage = 0; ativo != 0     2.103 (21%)
  candidato omite compliance_markup_override           1.098 (11%)
  candidato dá panic no callback de ação                 504 (5%)

QUEBRA POR PERSONA das divergências inesperadas
  berlin_commuter           4.201 (43%)
  italian_holiday_planner   2.809 (29%)
  cross_border_business     1.420 (14%)
  long_tail                 1.417 (14%)

0,1% MAIS LENTAS DAS EXECUÇÕES DO CANDIDATO
  mediana (geral)    0,42ms
  p99   (geral)      2,81ms
  p99,9 (geral)      7,20ms
  p99,9 (DE rail short-lead)  14,30ms   ← investigar

ARTEFATOS
  divergence_signatures.csv
  sampled_explanations/{active,candidate}/*.json
  latency_outliers.csv
```

A primeira tabela é o número manchete: com que frequência o candidato bateu com o ativo. A segunda tabela agrupa divergências por assinatura — o *tipo* de diferença — pra que o time não tenha que investigar 9 847 registros individuais e sim quatro classes de diferença. A quebra por persona conecta as divergências de volta ao formato de tráfego do post anterior: se 43% das divergências inesperadas são berlinenses indo trabalhar, o candidato tem problema com esse cenário em específico.

A cauda de latência tá incluída porque shadow mode é o primeiro lugar onde regressão de performance no candidato fica visível. O candidato roda no mesmo hardware do ativo; latência é diretamente comparável; outlier no p99,9 do candidato é alerta que vale levantar antes do candidato virar ativo.

## Feature flag como botão de pânico

O caminho do shadow tem que ser controlável em runtime. Três controles que importam:

**On/off.** Uma flag única liga ou desliga o caminho do shadow inteiro. Quando o candidato começa a dar panic, o operador desliga sem deploy. A flag é a diferença entre rollback silencioso e incidente de 3 da manhã.

**Sampling.** Um botão de percentual que diz *que fração das requests deve rodar o candidato*. No rollout você começa em 0,1% e sobe pra 100% ao longo de poucos dias. Sampling também controla o custo da rodada de shadow — em 10 000 QPS, rodar o candidato em 100% do tráfego é o dobro do custo do engine; em 5% mal aparece.

**Filtro por persona ou facts.** A flag consegue mirar um subconjunto do tráfego — *só reservas DE rail*, *só request com uma feature flag específica de cima*, *só correlation ID terminando em 0-3*. É o que deixa o time focar o shadow no cenário em que o candidato deve atuar, sem pagar por rodar em toda request.

```go
type ShadowFlag struct {
    Enabled    bool      `flag:"shadow_enabled"`
    SampleRate float64   `flag:"shadow_sample_rate"` // 0.0 a 1.0
    Filter     string    `flag:"shadow_filter"`      // expressão CEL nos facts
}

func (s *Shadow) Enabled(ctx context.Context, req Request) bool {
    f := s.flags.Current()
    if !f.Enabled {
        return false
    }
    if !sampledIn(req, f.SampleRate) {
        return false
    }
    if f.Filter != "" && !matchesFilter(req, f.Filter) {
        return false
    }
    return true
}
```

Os valores da flag são por si só uma peça pequena de política. Ficam no mesmo tipo de sistema que guarda as regras. O on/off e a taxa de sample mudam direto; o filtro muda quando o time estreita o foco. Os defaults — desligado, 0% de sample, sem filtro — são deliberadamente conservadores: o candidato roda só quando o time ligou explicitamente.

## O que você aprende com shadow mode que não aprende em lugar nenhum

Três coisas, em ordem crescente de valor.

**Você aprende que o candidato funciona.** A grande maioria das rodadas de shadow termina com o time confiante de que o candidato bate com o ativo na cauda longa de requests que CI não cobriu. Essa confiança não é de graça — tem que ser ganha, e shadow é o único lugar pra ganhar com input real — mas em regime permanente é a coisa mais barata que shadow faz.

**Você aprende onde o candidato difere.** Quando o candidato é refactor ou otimização, *igual* é o resultado certo e divergência é regressão. Quando o candidato é mudança deliberada, divergência é o *sinal* e igualdade é a regressão. Shadow mode te diz qual dos dois tá acontecendo, request por request.

**Você aprende o que o *ativo* vinha fazendo errado o tempo todo.** Essa é a surpresa que paga shadow mode várias vezes. O caso de abertura foi um exemplo: o composer velho tinha um caminho de panic que o novo arrumou. Já vi pelo menos três outras rodadas de shadow expor bug antigo no ativo que os logs de comparação trouxeram à tona — uma regra que vinha disparando no conjunto errado de cliente por um ano, uma ação que vinha engolindo erro em silêncio, um tier de priority que tava sendo invertido por um bug de ordenação. Cada um era bug que o time pagava sem saber.

O enquadramento vale dizer direto: shadow mode não é teste do candidato. É *comparação* entre duas versões da verdade, e a comparação lança luz nas duas.

## Erros comuns

Três padrões que shippei ou vi shippar.

**Rodar shadow numa fatia não representativa.** Sample de 0,1% do tráfego por uma semana soa prudente. Também são mal mil requests. Um bug que dispara em uma a cada dez mil é invisível nesse sample. O candidato shippa, o bug aparece em produção, e o time culpa "shadow não pegou" quando shadow simplesmente não recebeu exposição o bastante. A cura é subir o sample rate e rodar o shadow tempo suficiente pra cobrir as caudas lentas do formato de tráfego.

**Deixar o candidato atrasar o cliente.** Um time entrou em pânico com o custo alto do shadow e moveu o caminho do candidato pra goroutine da request pra reusar o contexto. De repente o candidato tava bloqueando a resposta. A latência subiu. O candidato foi roll-backado não por divergência, mas por sincronia. O formato que previne isso é o contrato da seção de arquitetura: candidato roda em goroutine separada com contexto próprio, ponto.

**Não registrar divergência esperada.** Um time lançou uma mudança deliberada de regra como shadow e viu 18% das requests divergir. O time entrou em pânico e rollback, aí percebeu que a divergência era exatamente a mudança que tinham pedido. O fix é o registro de mudanças esperadas: todo candidato que deve se comportar diferente tem que declarar *onde* e *quanto*, antes da rodada de shadow começar. Aí a taxa de divergência inesperada vira significativa.

## Onde shadow termina e a próxima coisa começa

Shadow mode é a metade live da exposição pré-produção do candidato. A metade offline é simulação por replay — rodar o candidato contra um fixture capturado de tráfego, com os dois engines determinísticos, com a comparação reproduzível. Shadow é o que o candidato precisa sobreviver na selva; replay é o que precisa sobreviver no laboratório.

Os dois são complementares. Shadow te diz o que o candidato faz em tráfego real ao custo de rodar tráfego real. Replay te diz o que o candidato faz num fixture conhecido ao custo de preparar o fixture. O próximo post junta os dois: um fixture capturado pelo `traffic-gen`, um snapshot guardado pelo `bre-go`, um rule set candidato, e um diff determinístico dos dois outputs. O output desse loop é o que torna mudança de regra revisável como código, não como esperança.

## A lição

A lição de engenharia, depois de sete rollouts de shadow de complexidade variada, é essa. Shadow mode deixa a lógica nova estar errada em produção, em tráfego de produção, antes de um único cliente pagar pelo bug. Faz isso rodando o candidato ao lado do ativo, de forma assíncrona, comparando output, classificando divergência, e expondo as inesperadas pro time.

O custo é a arquitetura: uma goroutine por request shadowada, um log de comparação, um pipeline de divergência, uma feature flag. A primeira versão são umas poucas centenas de linhas de código. A versão completa é um serviço pequeno com um dashboard. O benefício acumula: todo candidato é exposto a tráfego no formato de produção antes de shippar, todo ativo é implicitamente auditado por ser comparado, e todo rollout começa com um relatório de divergência em vez de uma esperança.

A reescrita do composer do caso de abertura shippou no dia onze sem mudança visível pro cliente. O bug de panic do composer velho ganhou ticket próprio e foi arrumado na semana seguinte. A rodada de shadow tinha custado umas três horas de engenheiro em dez dias. O bug que ela pegou no ativo vinha precificando silenciosamente uma correção de reembolso errado a cada poucas horas, por dois anos e meio. Shadow mode se pagou nessa comparação única; tudo depois tem sido lucro.
