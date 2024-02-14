---
title: "Construindo um Engine de Avaliação de Regras"
subtitle: "Engine que roda em um passo opaco é engine que você não consegue debugar. Deixa os estágios explícitos e o bug não tem onde se esconder."
author: helio
layout: post
date: 2024-02-14T10:00:00+00:00
series:
  - pricing-engineering
series_order: 5
categories:
  - Engineering
  - Pricing
  - Architecture
tags:
  - pricing
  - business-rules
  - rule-engine
  - architecture
  - observability
  - go
description: "Rule engine é pipeline. Esse post abre o pipeline em estágios nomeados — load, validate, match, evaluate, execute, compose, explain — e mostra como as fronteiras viram observabilidade."
---

A escalada chegou às 23:14: *a regra de markup disparou no cliente errado*.

Não tinha disparado. Os três da gente passaram os próximos quarenta e cinco minutos provando isso. O fact set tava correto. A regra tava correta. A ação rodou com os inputs que a gente esperava. O resultado foi o que a regra dizia que devia ser. O cliente era o que a gente esperava cobrar.

O que tinha acontecido de verdade foi que a regra disparou, a ação executou, e o *consumidor lá embaixo* mapeou o resultado num campo diferente do que o time tinha acordado. O bug tava três camadas acima do engine. A gente gastou quarenta e cinco minutos provando que o engine não tava mentindo porque o engine não tinha como provar. Execute entrou; um número saiu; o meio era uma caixa preta.

Na manhã seguinte a gente abriu o engine em estágios. Dali pra frente, todo Execute produzia um registro que nomeava as regras que casaram, as condições avaliadas, as ações executadas, e o resultado composto. A próxima vez que alguém escalou, a resposta levou dois minutos.

É esse o resto desse post. Engine que roda em um passo opaco é engine que você não consegue debugar. Engine com estágios explícitos é engine que se explica sozinho.

## O pipeline

Rule engine é pipeline. Lê de cabeça pra rabo a partir de `Execute(ctx, facts) → Result`:

```
Facts entram
   │
   ▼
┌──────────────────────────────────────────┐
│ Load        (coberto no post 3)          │
└──────────────────────────────────────────┘
   │
   ▼
┌──────────────────────────────────────────┐
│ Validate    (coberto no post 3)          │
└──────────────────────────────────────────┘
   │
   ▼
┌──────────────────────────────────────────┐
│ Receber facts                            │
│   normalizar, conferir tipo, completar   │
└──────────────────────────────────────────┘
   │
   ▼
┌──────────────────────────────────────────┐
│ Match                                    │
│   candidato ← matcher.Match(facts)       │
└──────────────────────────────────────────┘
   │
   ▼
┌──────────────────────────────────────────┐
│ Evaluate                                 │
│   pra cada candidato: condition.Eval     │
│   acumular resultado pós-filtro          │
└──────────────────────────────────────────┘
   │
   ▼
┌──────────────────────────────────────────┐
│ Execute                                  │
│   action(facts) pra toda regra que disparou │
└──────────────────────────────────────────┘
   │
   ▼
┌──────────────────────────────────────────┐
│ Compose                                  │
│   combinar output das ações por política │
└──────────────────────────────────────────┘
   │
   ▼
┌──────────────────────────────────────────┐
│ Explain                                  │
│   emitir registro de cada fronteira      │
└──────────────────────────────────────────┘
   │
   ▼
Result + Explanation saem
```

Cada estágio é uma função. Cada estágio tem input e output. Cada estágio se testa sem os outros. Cada estágio falha com erro tipado que nomeia *qual* estágio falhou, não só *que* algo falhou.

Essa é a regra de design pro resto do post: **toda fronteira do pipeline é observável**. O time pergunta pro engine "o que aconteceu nesse ponto?" e o engine tem resposta.

## Receber facts: o contrato na borda

Facts são o que o engine usa pra avaliar. A assinatura do `Execute` define o que o engine aceita:

```go
// engine.Engine.Execute é o ponto de entrada do hot-path público.
func (e *Engine) Execute(ctx context.Context, in Request) (Result, error)
```

No `bre-go`, `Request` carrega `Input` como `interface{}` e callbacks opcionais pra `ConditionContext` e `ActionContext`. O wrapper `exec.Executor[In, Out]` adiciona input e output tipados. O formato é o mesmo, a ponte é mais larga.

Antes do matching começar, três coisas têm que ser verdade sobre os facts:

**Têm que ser completos o bastante.** Uma condição que referencia `days_to_departure` quebra em silêncio se a request não trouxe esse campo. O matcher não sabe se o campo "tá ausente" ou "tá em nil" — e a resposta muda a semântica. O estágio de recepção normaliza campo ausente como não-restringido (que o matcher trata como sem constraint) ou rejeita a request (quando o campo é obrigatório pro rule set que o engine tá servindo).

**Têm que ser do tipo certo.** `market` é string. `days_to_departure` é número. `enabled` é bool. O estágio de recepção é onde isso é convertido, validado, e carimbado no formato canônico que o engine indexed quer. O engine indexed do `bre-go` trabalha contra `map[string]string`, então esse estágio marshalla todo campo tipado pra representação string.

**Têm que ser baratos de ler.** O matcher vai ler o mesmo campo várias vezes em várias regras. O estágio de recepção converte a request crua num mapa de facts uma vez. Leituras subsequentes são lookup de hash O(1).

Um formato útil:

```go
type Facts struct {
    raw      map[string]string  // em string, pronto pro matcher
    original interface{}        // pros callbacks de ActionContext
    received time.Time          // quando essa request entrou no engine
}

func receive(in Request) (Facts, error) {
    raw, err := marshalFacts(in.Input)
    if err != nil {
        return Facts{}, fmt.Errorf("receive: %w", err)
    }
    return Facts{
        raw:      raw,
        original: in.Input,
        received: time.Now(),
    }, nil
}
```

Recepção é o primeiro lugar onde o Execute pode falhar. Falha de recepção *não* é falha de runtime — é falha de cliente. A Request não trouxe o que o engine precisava. O engine retorna erro; nenhuma regra é avaliada; nenhum listener dispara como se uma regra tivesse casado.

## Match: dos facts pro conjunto candidato

Match foi o assunto do Post 4. Aqui ele se acomoda no pipeline.

```go
type Matcher interface {
    Match(facts Facts) []RuleRef
}
```

O matcher devolve um *conjunto candidato*: as regras cujas condições indexáveis são consistentes com os facts. O conjunto candidato é pequeno (sub-linear na contagem de regras, num matcher indexed) e ainda não leva em conta as condições pós-filtro.

O contrato aqui é estreito. O matcher não avalia condição completa; não roda ação; não compõe nada. Entrega pro próximo estágio uma lista de regras pra considerar.

No adaptador indexed do `bre-go`:

```go
// Pseudocódigo do indexed.Engine.Execute, simplificado.
candidates := e.index.Lookup(facts.raw)
// candidates é o conjunto das regras cujos termos indexáveis
// hashearam nos buckets em que essa request também hasheou.
```

O conjunto candidato é a primeira fronteira observável do pipeline. O tamanho do conjunto candidato é uma métrica que vale acompanhar — mostra se o índice tá fazendo o trabalho. Conjunto candidato consistentemente grande quer dizer que as regras não estão bem indexadas e o matcher tá degradando pra linear. Conjunto candidato consistentemente vazio pra tráfego vivo quer dizer que as regras estão estreitas demais, e muito esforço tá sendo desperdiçado.

## Evaluate: do conjunto candidato pras regras que casaram

O evaluator caminha cada regra candidata e avalia a árvore Condition inteira contra os facts. Aqui é onde condições pós-filtro (negação, faixa, condição tipada custom registrada pelo hook de pós-filtro) são avaliadas.

```go
type Evaluator interface {
    Evaluate(candidates []RuleRef, facts Facts) []RuleRef
}
```

O output é o subconjunto do conjunto candidato que de fato dispara. O evaluator é o primeiro estágio que sabe se a condição completa de uma regra é verdade pra esses facts.

É também onde todo "quase casou" é registrado. Uma regra cujos termos indexáveis bateram mas a faixa não, é interessante. Diz pro time que a regra foi quase um match — e quase um match é exatamente o tipo de coisa que o log de explicação precisa.

```go
type EvaluationRecord struct {
    Rule      RuleRef
    Outcome   Outcome  // OutcomeFired, OutcomeFailedCondition, OutcomeDisabled
    FailedAt  string   // "when.days_to_departure.lt" se uma cláusula falhou
}
```

Um matcher simples só retorna as regras que dispararam. Um matcher útil retorna as regras que dispararam *e* os registros de avaliação das que não dispararam. O segundo custa um pouquinho mais de memória; paga de volta na primeira vez que alguém pergunta "por que a regra X não disparou?"

No `bre-go`, é pra isso que serve a interface de listener. `OnRuleMatched` dispara por match; o structured telemetry listener pode ser hookado pra gravar outcome de condição; a abordagem listener-driven mantém o hot-path enxuto e a história de observabilidade rica pros callers que adotam.

## Execute: rodar as ações

Depois que o conjunto de regras é conhecido, a ação roda. A ação pega os facts (e opcionalmente um `ActionContext` carregando o correlation ID, o handle do listener, e o que mais o caller pediu) e devolve o que a assinatura de tipo da ação disser que devolve.

```go
type ActionResult struct {
    Rule    RuleRef
    Output  interface{} // o que essa ação devolveu
    Err     error       // tipado se a ação deu panic
    Latency time.Duration
}

func (e *Engine) executeActions(ctx context.Context,
    fired []RuleRef, facts Facts) []ActionResult {
    results := make([]ActionResult, 0, len(fired))
    for _, r := range fired {
        start := time.Now()
        out, err := r.Action(facts.original) // com recover de panic
        results = append(results, ActionResult{
            Rule:    r,
            Output:  out,
            Err:     err,
            Latency: time.Since(start),
        })
    }
    return results
}
```

Duas escolhas de design nesse loop merecem o destaque.

**Ação roda depois do matching, nunca durante.** O estágio de match e o estágio de ação são separados por uma lista explícita. O engine conhece o conjunto completo de regras que dispararam antes de qualquer ação rodar. Isso é o que deixa a detecção de conflito acontecer nas colisões de campo que o Post 4 abordou: o engine vê que R7 e R12 querem setar `markup_percentage` ao mesmo tempo, e a política de resolução decide o que fazer — *antes* de qualquer ação rodar.

**Panic de ação é capturado e tipado.** O listener `OnExecutionErrored` do `bre-go` recebe um `ActionPanicError` carregando o nome da regra e o valor do panic. Panic numa ação não derruba o engine; produz um resultado tipado em volta do qual o próximo estágio compõe. O engine ainda devolve um Result; o Result reporta que R7 deu panic e foi excluída.

É onde o instinto de engenharia briga com pragmatismo. O instinto diz: *se alguma coisa deu errado, falha o Execute inteiro*. O pragmatismo diz: *se R7 deu panic mas R12 e R18 dispararam limpas, o caller provavelmente ainda consegue tomar decisão*. O meio-termo em que o `bre-go` chega é deixar o caller ver o que aconteceu e escolher: a regra falha aparece na explicação; o Result carrega o conjunto parcial; o caller pode rebaixar pra um default seguro se não gostar do parcial.

## Compose: combinar output das ações por política

Compose é o estágio que transforma N outputs de ação num Result. É onde a política de resolução do Post 4 de fato roda.

```go
type Composer interface {
    Compose(actions []ActionResult) Result
}

// Um composer concreto pra um engine de pricing:
type pricingComposer struct {
    policy ResolutionPolicy // sum, last, fail por campo
}

func (c *pricingComposer) Compose(actions []ActionResult) Result {
    var r Result
    for _, a := range actions {
        if a.Err != nil {
            r.Failed = append(r.Failed, a.Rule)
            continue
        }
        r = c.policy.Apply(r, a.Output, a.Rule)
    }
    return r
}
```

O composer é onde markup aditivo empilha, onde last-write-wins resolve, onde conflito que o loader não pegou é levantado como erro em tempo de Execute. O composer é também a camada que a maioria dos engenheiros embute dentro do próprio engine no começo — e a camada que mais paga quando é puxada pra fora.

Composer que é seu próprio estágio se testa com resultados de ação sintéticos. O teste não precisa subir o matcher nem o evaluator. O teste dá pro composer uma lista de `ActionResult{}` e checa o Result composto. É isso que torna mudança de política de resolução auditável.

## Explain: a fronteira que paga pelas outras

A explicação é o artefato que todo outro estágio alimenta.

```go
type Explanation struct {
    CorrelationID string
    ReceivedAt    time.Time
    Facts         Facts
    CandidateSet  []RuleRef
    Evaluations   []EvaluationRecord
    Actions       []ActionResult
    Result        Result
    Composer      string  // qual política
    Snapshot      string  // ID do snapshot do engine no momento do Execute
}
```

A explicação é o que faz a próxima escalada levar dois minutos em vez de quarenta e cinco. Registra toda fronteira do pipeline. O conjunto candidato diz pro time se o índice ajudou. As avaliações dizem pro time quais regras quase casaram. As ações dizem quais regras dispararam e o que devolveram. O Result diz o que o composer produziu.

A parte cara é que a explicação tem que ser barata de produzir. No `bre-go`, o modelo listener-driven significa que a explicação é opt-in: hot-path que não precisa não paga nada; investigação que precisa pode ser reproduzida contra o snapshot do engine que o Execute original usou, produzindo a mesma explicação de forma determinística. Foi disso que o trabalho de `ExportSnapshot` / `LoadSnapshot` em v0.15 / v0.16 tratou — explicabilidade não é só sobre emitir registro *agora*; é sobre conseguir reproduzir o estado do engine depois.

{{< plantuml title="O pipeline como fronteiras observáveis — cada estágio emite um registro que a explicação lê" >}}
@startuml
skinparam shadowing false
skinparam componentStyle rectangle
skinparam defaultFontName "Helvetica"

actor "Caller" as C
rectangle "Receive\nfacts.raw,\nfacts.original" as R
rectangle "Match\nconjunto candidato" as M
rectangle "Evaluate\ncasou + quase casou" as E
rectangle "Execute\noutput das ações" as X
rectangle "Compose\nResult" as CMP
rectangle "Explanation\n(registra cada estágio)" as EX

C  --> R : Request
R  --> M : Facts
M  --> E : []RuleRef
E  --> X : []RuleRef (casaram)
X  --> CMP : []ActionResult
CMP --> C : Result

R  ..> EX : recebida
M  ..> EX : conjunto candidato
E  ..> EX : avaliações
X  ..> EX : output das ações
CMP ..> EX : composer + result
EX --> C : Explanation
@enduml
{{< /plantuml >}}

## A função Execute num único frame

Juntando tudo, o engine fica assim:

```go
// engine.Engine.Execute, com o pipeline explícito.
func (e *Engine) Execute(ctx context.Context, in Request) (Result, error) {
    facts, err := e.receive(in)
    if err != nil {
        return Result{}, fmt.Errorf("receive: %w", err)
    }

    // Fronteira 1: conjunto candidato
    candidates := e.matcher.Match(facts)
    e.listeners.OnCandidates(ctx, candidates)

    // Fronteira 2: conjunto que disparou
    fired, evals := e.evaluator.Evaluate(candidates, facts)
    for _, ev := range evals {
        e.listeners.OnEvaluation(ctx, ev)
    }

    // Fronteira 3: output das ações
    actions := e.executeActions(ctx, fired, facts)
    for _, a := range actions {
        e.listeners.OnAction(ctx, a)
    }

    // Fronteira 4: result
    result := e.composer.Compose(actions)
    e.listeners.OnFinished(ctx, result)

    return result, nil
}
```

O que esse código deixa explícito é que todo momento interessante no engine é uma chamada de função com output nomeado. Os listeners são a superfície de observabilidade; as chamadas de função são as costuras de unit-test. O pipeline parou de ser um fluxograma no quadro e virou uma sequência de fronteiras tipadas.

## Testar o pipeline

Aqui é onde o Post 6 começa a fazer sentido. Com estágio tão explícito, teste se encaixa em quatro baldes.

**Unit test por estágio.** O matcher recebe um mapa de facts e a gente checa o conjunto candidato. O evaluator recebe um conjunto candidato e a gente checa o conjunto que disparou. O composer recebe uma lista de resultados de ação e a gente checa o Result. Cada teste é pequeno. Cada teste roda em microssegundos. Cada teste nomeia o estágio no nome do arquivo.

**Teste de integração pro pipeline.** Conecta os estágios reais contra um rule set conhecido. Passa facts realistas. Confere o Result. Esses pegam o bug entre estágios que unit test não pega: um matcher que produz conjunto candidato que o evaluator não consegue caminhar; um evaluator que dispara regra cuja ação o composer não tem política.

**Golden test pra comportamento ponta-a-ponta.** Dado um snapshot do rule set e um fixture de facts, a gente confere o Result e a Explanation. Esses testes prendem o sistema num comportamento que o time concordou. Quando o teste falha, o diff contra o arquivo golden é a história do que mudou.

**Teste de propriedade pra matcher e composer.** Pra qualquer fact set, o conjunto candidato é superset do conjunto que disparou. Pra qualquer resultado de ação, o Result composto obedece a política de resolução. Esses testes não prendem comportamento específico; prendem invariante. Teste de propriedade é o tipo de teste que acha bug que ninguém escreveu teste pra pegar.

O formato que torna esses quatro baldes baratos é o próprio pipeline. Estágio com input e output tipado se testa. Engine opaco não.

## O que o pipeline explícito te compra

Três coisas, principalmente.

**Tempo de debug cai.** A escalada de quarenta e cinco minutos do começo vira lookup de dois minutos. A explicação diz pro time onde no pipeline a coisa surpreendente aconteceu.

**Trabalho de performance vira focado.** Quando o p99 sobe, a latência por estágio emitida pelo listener diz pro time se o gargalo é match, evaluate ou execute. Sem fronteira de estágio, o único dado é "Execute tá lento".

**Mudança arquitetural vira segura.** Trocar o matcher de linear pra indexed é troca numa fronteira. Trocar o composer de last-write-wins pra aditivo é troca numa fronteira. Cada troca é code review de uma interface, não rearquitetura do engine.

O custo são as interfaces. O engine sobe com um tipo Engine e quatro interfaces internas — Matcher, Evaluator, Executor, Composer — cada uma implementada por um tipo concreto. As interfaces parecem cerimônia até o dia em que alguém quer testar o composer sem matcher de verdade na frente.

## O que vem a seguir

O próximo post é teste — não no abstrato, mas no formato específico que esses estágios habilitam. Teste table-driven pro matcher. Golden test pra ponta-a-ponta. Teste de propriedade pra invariante. O vocabulário de testar um rule engine, depois que o engine foi aberto em peças nomeadas.

O post seguinte é explicabilidade — o artefato que todo estágio desse post alimentou. Explicabilidade é o que vira o engine de uma caixa preta num sistema que o time consegue operar. É também onde as fronteiras registradas desse post viram o diff que um postmortem lê.

Por enquanto, a lição é o pipeline. Rule engine que roda em um passo é engine que não consegue se defender quando alguma coisa dá errado. Rule engine feito de estágios é engine que o time consegue interrogar. O primeiro tipo de engine você consegue shippar numa semana. O segundo tipo de engine você consegue manter rodando por cinco anos.

A escalada que começou esse post nunca se repetiu. Não porque o bug fosse raro. Porque na próxima vez que alguém escalou, o engine produziu uma explicação e a conversa acabou antes do segundo café.
