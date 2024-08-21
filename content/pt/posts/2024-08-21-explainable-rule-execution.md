---
title: "Execução Explicável de Regras"
subtitle: "Um sistema de pricing que não consegue explicar uma decisão não consegue ser operado com segurança. A explicação não é apoio de debug. É o contrato do sistema com todo mundo que precisa confiar nele."
author: helio
layout: post
date: 2024-08-21T10:00:00+00:00
series:
  - pricing-engineering
series_order: 7
categories:
  - Engineering
  - Pricing
  - Architecture
tags:
  - pricing
  - business-rules
  - rule-engine
  - explainability
  - observability
  - compliance
description: "Explicação não é log. É um artefato estruturado pra qual todo estágio do engine contribui, e o contrato que o sistema faz com operador, auditor e cliente."
---

O e-mail chegou às 9:42 numa terça do time jurídico. Um regulador de mercado queria, por escrito, a resposta a uma pergunta sobre um cliente: *por que essa reserva específica foi precificada desse jeito nessa data específica?*

A reserva tinha onze meses. O time dono do rule set tinha rodado parcialmente. O arquivo de regra tinha sido editado quarenta e seis vezes desde então. Log de produção tinha rolado fora trinta dias antes. O dashboard mostrava um número pra aquele dia, mas não o caminho que produziu.

A gente respondeu o regulador. Levou dois engenheiros quatro dias. Puxamos o git log do arquivo de regra, reconstruímos o estado naquela data, fizemos replay da reserva contra o engine reconstruído, produzimos a explicação, e traduzimos num parágrafo que um não-engenheiro conseguia ler. A reserva real do cliente não era a que precisávamos defender; a *categoria* de decisão era a que importava, e em algum momento a gente defendeu.

O que a gente não tinha, no dia em que aquele e-mail chegou, era um sistema que respondesse a pergunta sozinho. Toda peça da resposta existia em algum lugar. Nenhuma das peças tava conectada. A explicação, o artefato que a gente vinha sinalizando ao longo dos últimos cinco posts, era a costura que faltava.

Esse post é como essa costura fica quando é construída de propósito.

## As quatro audiências de uma explicação

O erro que cometi na primeira vez que construí explicabilidade num rule engine foi desenhar pra uma audiência só — o engenheiro debugando às 3 da manhã — e parar. Essa audiência é a mais barulhenta, mas é a que menos precisa de explicabilidade, porque o engenheiro lê o source.

Tem quatro audiências, e a explicação tem que servir todas sem desabar no menor denominador comum.

O **engenheiro** quer profundidade. Quais regras foram consideradas, quais dispararam, por que cada uma disparou ou não, qual foi o resultado de cada ação, onde o tempo foi gasto. O engenheiro lê JSON e fica tranquilo com nome de campo que não significa nada sem contexto.

O **operador** quer sinal. Qual snapshot do rule store serviu essa request? Tinha alguma regra desabilitada? A resposta foi normal ou anômala comparada com o tráfego vizinho? O operador não quer ler cada avaliação; quer saber se algo parece fora.

O **dono de produto ou de domínio** quer verificar o acordo. O sistema fez o que a gente disse que faria? As regras que escrevemos se comportaram como esperado? O dono de produto lê o nome da regra e o resultado; não lê chave de bucket.

O **auditor ou regulador** quer trilha de papel. Dado um cliente e uma data, que decisão foi tomada, por qual regra, com qual intenção, dona por qual time, com qual data de revisão? O auditor quer exatamente os campos chatos de metadado que o Post 1 defendeu não serem opcionais.

Cada audiência lê um subconjunto diferente do mesmo artefato. O trabalho da explicação é ser o mesmo artefato pra todas, com visões diferentes em cima. Um registro estruturado único, consultado de quatro jeitos diferentes.

## O schema, por inteiro

O Post 5 esboçou a Explanation. Esse post preenche. O schema abaixo é em que cheguei depois de três iterações.

```go
type Explanation struct {
    // Identidade e rastreabilidade
    CorrelationID  string    `json:"correlation_id"`
    RequestID      string    `json:"request_id"`
    SnapshotID     string    `json:"snapshot_id"`     // hash do estado do engine
    SchemaVersion  int       `json:"explanation_version"`
    OccurredAt     time.Time `json:"occurred_at"`
    Duration       time.Duration `json:"duration_ns"`

    // O que entrou
    Facts          map[string]string `json:"facts"`

    // O que aconteceu, estágio por estágio
    CandidateSet   []RuleRef          `json:"candidates"`     // output do matcher
    Evaluations    []EvaluationRecord `json:"evaluations"`    // outcome por regra
    Actions        []ActionRecord     `json:"actions"`         // output por regra disparada
    Composition    CompositionRecord  `json:"composition"`     // política de resolução aplicada

    // O que saiu
    Result         json.RawMessage    `json:"result"`

    // O que o operador deve se importar
    Warnings       []Warning          `json:"warnings,omitempty"`
}

type EvaluationRecord struct {
    Rule         RuleRef `json:"rule"`
    Outcome      Outcome `json:"outcome"`       // fired, failed_condition, disabled, errored
    FailedAt     string  `json:"failed_at,omitempty"`     // "when.days_to_departure.lt"
    EvalDuration time.Duration `json:"eval_duration_ns"`
}

type ActionRecord struct {
    Rule           RuleRef `json:"rule"`
    Output         json.RawMessage `json:"output"`
    Err            string `json:"err,omitempty"`
    Latency        time.Duration `json:"latency_ns"`
}

type CompositionRecord struct {
    Policy   string                       `json:"policy"`
    PerField map[string]CompositionTrace  `json:"per_field"`
}

type CompositionTrace struct {
    FinalValue        json.RawMessage `json:"final_value"`
    ContributingRules []string        `json:"contributing_rules"`
    Strategy          string          `json:"strategy"`  // sum, last, first, fail
}

type RuleRef struct {
    Name         string `json:"name"`
    Version      string `json:"version"`       // sha do git do arquivo, ou hash de rule_id
    Owner        string `json:"owner"`
    Description  string `json:"description"`
    Priority     int    `json:"priority"`
    Enabled      bool   `json:"enabled"`
}

type Warning struct {
    Code     string `json:"code"`     // SHADOWED_RULE, EMPTY_CANDIDATE_SET, etc.
    Message  string `json:"message"`
    Severity string `json:"severity"` // info, warn
}
```

Três propriedades desse schema que merecem viver em produção.

**Todo registro aponta de volta pra fonte.** `RuleRef` carrega Owner, Description e uma Version. O consumidor da explicação não precisa também carregar o arquivo de regra pra saber o que a regra significava. O campo Version é crítico: quando o arquivo de regra evolui, a explicação ainda referencia a regra *como ela era no momento do Execute*.

**Latência mora por estágio.** `EvalDuration` por avaliação, `Latency` por ação, e `Duration` pelo Execute inteiro. Tempo cumulativo total esconde onde o tempo foi gasto; latência por estágio torna o comportamento do engine observável sem profiler externo.

**Warning é de primeira classe.** Uma regra sombreada que disparou mesmo assim, um conjunto candidato suspeitosamente vazio, um passo de composição que bateu numa política `fail` — cada um vira um Warning que o dashboard do operador expõe. O dashboard não precisa parsear a explicação inteira; conta warning por código e plota a taxa.

## Uma explicação real, ponta a ponta

É assim que uma Explanation fica pro cenário alemão de última hora que tô usando ao longo da série:

```json
{
  "correlation_id": "c1b9a4e7-21d8-4d0e-9a2a-1cb5a7e4f0b1",
  "request_id": "req-2024-08-21T10:14:33Z-7b3f",
  "snapshot_id": "sha256:7b3f...e91d",
  "explanation_version": 2,
  "occurred_at": "2024-08-21T10:14:33.012Z",
  "duration_ns": 412330,

  "facts": {
    "market": "DE",
    "channel": "rail",
    "days_to_departure": "4",
    "device": "mobile",
    "regulated_market": "false"
  },

  "candidates": [
    {"name": "compliance_markup_override", "version": "7b3f", "owner": "compliance",
     "description": "0% markup em mercado regulado", "priority": 1000, "enabled": true},
    {"name": "short_lead_time_markup_de", "version": "7b3f", "owner": "pricing-de",
     "description": "3% markup em DE com menos de 7 dias", "priority": 500, "enabled": true},
    {"name": "germany_baseline_markup", "version": "7b3f", "owner": "pricing-de",
     "description": "2% markup baseline em toda DE", "priority": 100, "enabled": true}
  ],

  "evaluations": [
    {"rule": {"name": "compliance_markup_override"}, "outcome": "failed_condition",
     "failed_at": "when.regulated_market.eq", "eval_duration_ns": 1850},
    {"rule": {"name": "short_lead_time_markup_de"}, "outcome": "fired",
     "eval_duration_ns": 4210},
    {"rule": {"name": "germany_baseline_markup"}, "outcome": "fired",
     "eval_duration_ns": 1320}
  ],

  "actions": [
    {"rule": {"name": "short_lead_time_markup_de"}, "output": {"markup_percentage": 3.0},
     "latency_ns": 8120},
    {"rule": {"name": "germany_baseline_markup"}, "output": {"markup_percentage": 2.0},
     "latency_ns": 6210}
  ],

  "composition": {
    "policy": "additive_with_compliance_override",
    "per_field": {
      "markup_percentage": {
        "final_value": 5.0,
        "contributing_rules": ["short_lead_time_markup_de", "germany_baseline_markup"],
        "strategy": "sum"
      }
    }
  },

  "result": {"markup_percentage": 5.0},

  "warnings": []
}
```

O registro inteiro são 60 linhas de JSON pra um Execute. Carrega o bastante pro engenheiro, pro operador, pro dono de produto e pro auditor.

O engenheiro lê `evaluations` e `actions` e vê o caminho do engine.

O operador varre `warnings` e `duration_ns` e confirma que a request foi normal.

O dono de produto lê `composition.per_field.markup_percentage.contributing_rules` e confirma que o acordo segurou.

O auditor lê `facts`, `candidates[*].owner` e `result` e tem um parágrafo defensável.

Um artefato. Quatro visões. Sem passo de tradução.

## O modelo de custo

O custo de uma Explanation é o custo que mais engenheiro teme e mais superestima.

Uma Explanation populada pra um engine de 100 regras tá na ordem de 5–15 KB de JSON, dominada pelo conjunto candidato e pelos registros de avaliação. A geração leva microssegundos — os registros já são produzidos pelo stack de listener do Post 5; emissão é `json.Marshal` sobre um struct tipado. O overhead do hot-path, quando a explicação é emitida, é um percentual de um dígito do tempo de Execute.

O custo que dói não é geração. É *armazenamento*. Em 10 000 QPS, explicação completa pesa 50 MB/s, 4 TB/dia, 120 TB/mês. Nenhum sistema retém isso indefinidamente.

Três estratégias, em sofisticação crescente, lidam com o custo.

**Sampling.** Um percentual fixo das requests recebe explicação completa; o resto não recebe nada. Útil pra visibilidade de engenharia no caminho médio. Inútil pra auditoria — a request que te perguntam é, pela lei de Murphy, sempre fora da amostra.

**Emissão em camada.** Toda request recebe uma explicação minúscula (5 linhas: snapshot ID, nome da regra disparada, resultado). Requests anômalas, requests sinalizadas por warning, requests de cliente de alto valor, e uma amostra de requests normais recebem explicação completa. O sinal é preservado; o custo é limitado.

**Replay sob demanda.** Toda request guarda o *mínimo* necessário pra reproduzir: snapshot ID, facts, correlation ID. A explicação completa é gerada de um replay contra o snapshot guardado quando perguntam. Isso funciona porque o engine é determinístico (a primeira propriedade do Post 1 se justifica aqui) e porque o `ExportSnapshot` / `LoadSnapshot` do `bre-go` faz do snapshot um artefato de primeira classe.

A arquitetura que eu acabo escolhendo na maioria das vezes é a terceira, sobreposta à segunda:

- Hot path emite explicação minúscula por request (snapshot ID, regras que dispararam, resultado) em amostra de 100%.
- Hot path emite explicação completa em amostra de 1%, mais sob demanda pra requests carregando uma flag `?debug=1` do call site.
- Cold path consegue regerar a explicação completa a partir de `(snapshot_id, facts, correlation_id)` via replay, até o tempo de retenção do snapshot.

Retenção de snapshot é a restrição real de capacidade. Um snapshot é pequeno (arquivo binário, KBs a MBs). Manter todo snapshot que o engine já serviu é barato. Com o snapshot retido e os facts logados, a explicação completa é reconstruída a qualquer momento.

{{< plantuml title="Emissão em camada: barato por padrão, completo sob demanda, reproduzível pra sempre" >}}
@startuml
skinparam shadowing false
skinparam componentStyle rectangle
skinparam defaultFontName "Helvetica"

rectangle "Hot path\nExecute(ctx, facts)" as HP
rectangle "Explicação tiny\nemitida 100%\n(5 linhas / request)" as T
rectangle "Explicação completa\nemitida 1% + sob demanda" as F
rectangle "Snapshot store\nestado do engine\nretido 12 meses" as S
rectangle "Fact log\nfacts da request\nretido 12 meses" as L
rectangle "Serviço de replay\nreproduz explicação\ndepois" as R
actor "Auditor\nou engenheiro" as A

HP --> T
HP --> F
HP --> S
HP --> L
A  --> R : "explica request X"
R  --> S : carrega snapshot
R  --> L : carrega facts
R  --> A : explicação completa
@enduml
{{< /plantuml >}}

## Trace ID como espinha da explicação

Explicação conecta com o resto do sistema pelo correlation ID. O `engine.WithCorrelationID(ctx, id)` do `bre-go` põe o ID no contexto; o engine lê do `ConditionContext` e `ActionContext`; a explicação carimba como primeiro campo.

O correlation ID é o que deixa um serviço atravessar trinta linhas de log lá embaixo e a explicação seguir sendo a mesma conversa. O engenheiro de suporte vê o trace ID no tooling dele; o rule engine sabe esse mesmo ID; a explicação é consultável por ele.

Três regras que tornam correlation ID útil na prática:

**Gera na borda, propaga pra dentro.** O gateway de API ou o call site gera o ID; o engine nunca inventa um. ID gerado pelo engine é um que mais nada consegue conectar.

**Inclui em toda superfície de observabilidade.** A métrica, a linha de log, a explicação, o registro do snapshot. Se o ID tá em três de quatro superfícies, o auditor ainda não consegue conectar.

**Distingue correlation de request ID.** Correlation é sessão — jornada do cliente, workflow, batch. Request é uma chamada. Vários Execute na mesma jornada do cliente compartilham um correlation ID; cada um tem o próprio request ID. A explicação carrega os dois.

O custo é uma string no schema. O benefício é que toda pergunta posterior — *o que mais aconteceu nessa sessão do cliente?* — tem resposta.

## Log e explicação: quando cada um dispara

Um erro comum é despejar a explicação dentro de um structured log e chamar de observabilidade. É mais útil pensar log e explicação como dois artefatos diferentes com dois tempos de vida diferentes.

**Log é evento time-series.** Vai pro agregador de log. É sampleado, derrubado sob carga, e rolado fora depois de semanas. Bom pra "o que aconteceu na última hora?" e ruim pra "o que aconteceu com essa request há onze meses?"

**Explicação é artefato endereçado.** Chaveada pelo request ID. Guardada num data store (ou reproduzível de um snapshot). Boa pra "o que aconteceu com *essa* request?" e ruim pra "qual a taxa de warning?"

Os dois precisam um do outro. A linha de log carrega o request ID e o snapshot ID; a explicação carrega o contexto completo. O dashboard lê o log e plota a taxa; o investigador lê a explicação e reconstrói o caminho.

Um formato simples:

```go
// Na hora do Execute, emite uma linha de log.
log.Info("rule.engine.execute",
    "correlation_id", explanation.CorrelationID,
    "request_id", explanation.RequestID,
    "snapshot_id", explanation.SnapshotID,
    "fired_count", len(explanation.Actions),
    "duration_ms", explanation.Duration.Milliseconds(),
    "warning_count", len(explanation.Warnings),
)

// Em separado, emite a explicação completa pra explanation store
// (síncrono pra tráfego sampleado, assíncrono pra debug-flagado).
explanationStore.Put(ctx, explanation)
```

A linha de log é suficiente pra dashboard e alerta. A explicação é suficiente pra investigação. Nenhuma é suficiente sozinha.

## O workflow de investigação

A razão pra construir explicabilidade é tornar investigação barata. O workflow de investigação, quando o sistema é bem construído, é:

1. Suporte ao cliente sinaliza uma reserva com um correlation ID.
2. O engenheiro consulta a explanation store: `explanationStore.Get(correlation_id)`.
3. Se a explicação tá na store (sampleada ou debug-flagada), retorna na hora.
4. Se não, o serviço de replay é invocado: carrega o snapshot a partir do snapshot ID embutido na linha de log original, carrega os facts do fact log, e roda o engine de novo pra reconstruir a explicação.
5. O engenheiro lê a explicação e responde a pergunta.

É isso que transformou a investigação de quatro dias da história de abertura em trinta minutos nos trimestres seguintes. O mesmo workflow, com os mesmos artefatos, atende escalada de engenharia, pergunta de produto, e pedido de auditoria.

O workflow tem um pré-requisito: snapshot tem que ser retido. O snapshot é o que torna o replay determinístico. Sem o snapshot, replay exige reconstruir o rule set do histórico do `git`, que funciona só se a compilação do rule set pelo engine é em si reproduzível a partir do source. (Em geral é, mas os dias em que você descobre que não é são os dias em que queria ter guardado o snapshot.)

## O que a explicação habilita

Três benefícios duradouros que pagam o investimento de engenharia.

**Postmortem fica mais rápido.** Todo incidente tem um request ID. Todo request ID tem uma explicação. O postmortem começa pela explicação; a análise de root cause é o diff entre o que a explicação mostrou e o que o time esperava.

**Suporte ao cliente para de escalar.** O agente respondendo "por que fui cobrado disso?" tem a explicação. O dono de produto não precisa ser paginado pra pergunta de rotina. O time de engenharia não precisa ser o primeiro ponto de contato pra curiosidade de pricing.

**Compliance vira problema de ferramenta, não de heroísmo.** Da próxima vez que o regulador perguntar, a resposta é uma query no banco, não quatro dias-engenheiro. A defensibilidade do sistema é propriedade embutida, não extraída.

O custo — schema, armazenamento, serviço de replay, retenção de snapshot — é real. Também é limitado. A primeira versão são poucas centenas de linhas de código. A versão completa são alguns milhares. O benefício se acumula em todo incidente, toda escalada, toda auditoria, enquanto o engine rodar.

## O que a explicação *não* faz

Duas coisas que pedem pra explicação fazer, e que ela não devia fazer.

**Não substitui o arquivo de regra.** O arquivo de regra é a intenção que o autor escreveu. A explicação é o resultado avaliado. Confundir os dois é como o time acaba "editando a explicação" pra arrumar um bug, o que não arruma nada e obscurece a próxima investigação.

**Não é a trilha de auditoria do engine.** A trilha de auditoria é o snapshot + o fact log + o histórico da regra no `git`. A explicação é a *visão* através disso, gerada pra uma request. Auditoria em mil requests são mil explicações, geradas contra os mesmos snapshots. A explicação não é o armazenamento; é a projeção.

Essas distinções soam pedantes até você ver um time tentando guardar toda explicação pra sempre como "a trilha de auditoria". O custo acumula, o schema começa a mudar, e o data store vira o componente mais caro do sistema. O modelo de replay-sob-demanda é o que mantém o custo são.

## O que vem a seguir

O próximo post é tráfego sintético — o jeito de dar pro engine inputs que ele ainda não viu, de propósito, pra encontrar os bugs que vai encontrar depois. Tráfego sintético é o que torna shadow mode e simulação por replay significativos nos dois posts seguintes. É também onde o segundo repositório de referência, [`traffic-gen`](https://github.com/helmedeiros/traffic-gen), entra na história.

Tráfego sintético e explicação são complementares. Tráfego produz request; o engine produz explicação. Uma sessão de replay contra um rule set candidato gera explicação pra cada request sintética, e a diferença entre a explicação candidata e a atual é a avaliação de impacto da regra candidata. Os próximos três posts são sobre fechar esse loop.

Por enquanto, a lição é o contrato. Um sistema de pricing que não consegue explicar uma decisão não consegue ser operado com segurança. A explicação é a promessa que o sistema faz pro operador, pro auditor, pro dono de produto e pro engenheiro — que o caminho que o engine pegou é recuperável. Essa promessa não é de graça, mas é o seguro mais barato que o engine carrega, e é a peça do sistema em que você vai estar feliz de ter superinvestido na primeira vez que um regulador faz uma pergunta.

O cliente da história de abertura não era, no fim, a pergunta. A categoria de decisão era. O próximo e-mail de regulador chegou sete meses depois. A resposta levou trinta minutos. O sistema, àquela altura, já não tava pedindo pra gente defender ele; tava se defendendo sozinho.
