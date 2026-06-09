---
title: "Desenhando um Modelo de Regra"
subtitle: "O struct Rule é o contrato entre intenção de negócio e execução em runtime. Erra o contrato, e toda camada acima paga o preço."
author: helio
layout: post
date: 2025-06-18T10:00:00+00:00
series:
  - building-pricing-systems
series_order: 2
categories:
  - Engineering
  - Pricing
  - Architecture
tags:
  - pricing
  - business-rules
  - rule-engine
  - go
  - type-systems
  - architecture
description: "Desenhar o tipo Rule em memória é o momento em que você assume um contrato. Esse post abre o Rule, Condition e Action do bre-go pra mostrar onde os trade-offs moram."
---

Tem uma hora, três dias depois de começar a montar uma rule store, em que alguém do time fala: *bota um `map[string]interface{}` e segue.*

É uma sugestão tentadora. O mapa é flexível. O mapa aceita qualquer coisa. O mapa não quebra quando alguém adicionar um campo novo no próximo trimestre. O time tá correndo e o mapa é a estrutura mais barata de tipar.

O mapa também vai tornar inútil todo teste que você escrever.

Esse post é sobre o modelo de regra — a representação em memória de uma regra — e por que acertar essa peça é a escolha mais consequente do resto do engine. Tudo que vem depois, do matching ao armazenamento à explicabilidade, recebe o modelo de regra como input. Se o modelo não tem forma, nenhuma dessas camadas consegue fazer o trabalho. Se o modelo tá super-formatado, o sistema deixa de conseguir expressar o que o negócio quer de verdade. O trabalho desse post é encontrar a linha.

O código de referência sai de [`bre-go`](https://github.com/helmedeiros/bre-go). O formato do struct Rule, os tipos Condition / Action, e a árvore do parser estão todos lá.

## O que entra num Rule

O menor Rule útil carrega cinco coisas: identidade, gate (quando se aplica), corpo (o que faz), ciclo de vida (se tá ligado e em que ordem), e metadado (a contabilidade que deixa a regra legível depois que o autor original sai).

Em Go, modelado no `inmemory.Rule` do `bre-go`:

```go
// Rule é o contrato em memória que uma regra de negócio precisa honrar.
type Rule struct {
    Name        string   // identidade estável. Aparece em log, teste, explicação.
    Description string   // uma frase. O que essa regra tenta expressar.
    Tags        []string // owner, categoria, ciclo de vida. Barato de consultar.
    Condition   Condition
    Action      Action
    Priority    int  // maior = avaliado primeiro nos engines priorizados
    Enabled     bool // off-switch sem deploy
}
```

O struct é estreito de propósito. Sem timestamp. Sem histórico. Sem campo "owner". É intencional: essas coisas moram em metadado, e metadado mora numa preocupação separada que evolui sem mexer no tipo que o engine consome. O engine não precisa saber que `created_by: helio` existe. O engine precisa saber que a regra tem Name, tem Condition, tem Action, tem Priority, e tem flag Enabled.

Já tem decisão importante embutida nesse struct que vale destacar.

**Name como identidade, não ID.** O Name aparece em todo lugar: nos listeners de regra casada, em mensagem de teste falhando, no log de explicação. Tem que ser legível. UUID dá unicidade; não dá mais nada. O Name tem que ser único na hora do registro — o `inmemory.AddRule` do `bre-go` retorna `ErrEmptyRuleName` e `ErrDuplicateRuleName` exatamente por isso.

**Description como frase.** Não doc-comment. Não ensaio de parágrafos. Uma frase em que a regra cabe. Se você não consegue caber a regra numa frase, a regra tá fazendo duas coisas, e a segunda precisa da própria regra.

**Tags como camada de consulta barata.** Quando você passar de cem regras, vai precisar perguntar coisa do tipo *me mostra toda regra ativa do pricing-DE que não foi revisada nos últimos seis meses*. Tag é o jeito de responder sem montar uma DSL de consulta.

**Priority e Enabled como botões de runtime, não política.** Esses dois campos existem porque o runtime precisa, não porque o negócio se importa. Priority é o jeito do engine resolver conflito quando várias regras casam; Enabled é o jeito do time desligar uma regra sem subir versão. Têm que estar no tipo porque o engine precisa, mas devem ser invisíveis pro autor da regra quando dá.

{{< plantuml title="O struct Rule: identidade, gate, corpo, runtime, contabilidade" >}}
@startuml
skinparam shadowing false
skinparam componentStyle rectangle
skinparam defaultFontName "Helvetica"

rectangle "Rule" as R {
  rectangle "Identidade\nName, Description, Tags" as ID
  rectangle "Gate\nCondition" as G
  rectangle "Corpo\nAction" as B
  rectangle "Runtime\nPriority, Enabled" as RT
}

rectangle "Metadado\n(preocupação separada)" as MD

ID --> RT : molda ciclo de vida
G  --> B  : quando casa, executa
MD ..> R  : descreve, não amarra
@enduml
{{< /plantuml >}}

## Condition: função ou expressão tipada?

A Condition é o tipo mais consequente do modelo de regra. É a coisa que o matcher olha. O formato da Condition decide se o matching consegue ser sub-linear, se a regra consegue ser serializada, se a regra consegue ser inspecionada sem rodar, e se duas regras conseguem ser comparadas estaticamente.

Tem dois formatos comuns, e cada um tem um futuro bem diferente.

### O formato função

Função é o primeiro lugar pra onde todo engenheiro vai:

```go
type Condition func(in interface{}) bool
```

É o formato mais permissivo do `bre-go`, usado pelo `engine/inmemory` e pelo pacote `conditions`:

```go
import "github.com/helmedeiros/bre-go/engine/conditions"

rule := inmemory.Rule{
    Name:        "high-value-clean-usd",
    Description: "aprovar pedido USD de alto valor sem flag",
    Tags:        []string{"approval"},
    Condition: conditions.And(
        func(in interface{}) bool { return in.(Order).Amount > 100 },
        func(in interface{}) bool { return in.(Order).Currency == "USD" },
        conditions.Not(func(in interface{}) bool { return in.(Order).Flagged }),
    ),
    Action: func(interface{}) interface{} { return "approve" },
}
```

É maravilhoso pra um engenheiro escrever a regra em Go. A condição é código literal. O compilador confere. Sem parser, sem DSL, sem schema.

E é, no segundo em que a regra precisa sair da máquina do engenheiro, completamente opaco. Você não serializa `func(in interface{}) bool`. Você não consegue perguntar pro matcher "quais regras olham o campo `market`?" Você não consegue dizer pro PM "olha aqui o que essa regra faz." Tudo que você tem é o source.

Função funciona quando toda regra vai ser escrita por engenheiro e shippada com deploy. No momento em que isso deixa de ser verdade, você precisa de um formato tipado por baixo.

### O formato expressão tipada

O formato tipado troca a função por uma árvore de nós inspecionáveis. O pacote `engine/parser` do `bre-go` é construído em volta disso:

```go
// Uma árvore de condição que o engine consegue ler, serializar e analisar.
type Condition interface {
    Eval(in map[string]string) bool
}

type StringCondition struct {
    Field string
    Op    Op       // OpEq, OpNeq
    Value string
}

type SetCondition struct {
    Field  string
    Op     Op       // OpIn, OpNotIn
    Values []string
}

type AndCondition struct{ Children []Condition }
type OrCondition  struct{ Children []Condition }
type NotCondition struct{ Child Condition }
type RangeCondition struct {
    Field    string
    Min, Max float64
}
```

A mesma regra "high-value clean USD", no formato tipado, fica assim:

```go
rule := indexed.Rule{
    Name: "high-value-clean-usd",
    Match: parser.AndCondition{Children: []parser.Condition{
        parser.RangeCondition{Field: "amount", Min: 100.01, Max: math.Inf(+1)},
        parser.StringCondition{Field: "currency", Op: parser.OpEq, Value: "USD"},
        parser.StringCondition{Field: "flagged", Op: parser.OpNeq, Value: "true"},
    }},
    Action: func(interface{}) interface{} { return "approve" },
}
```

Agora a condição é coisa que você consegue caminhar. Você pergunta quais campos ela toca. Você monta uma chave de bucket de hash a partir dela. Você compara duas regras e detecta se uma sombreia a outra. Você serializa pra JSON e recarrega depois.

O adaptador `engine/indexed` do `bre-go` usa exatamente isso. Caminha a Condition tipada no momento do `Build()`, classifica cada cláusula como indexável (igualdade, IN) ou pós-filtro (NEQ, NOT IN, range), e monta uma estrutura de bucket de hash que vira o Execute de O(N regras) em O(K hash lookups + um conjunto pequeno de pós-filtros). Antes do Build, o engine aceita AddRule; depois do Build, recusa mutação e serve Execute concorrentemente a partir de um snapshot imutável guardado num `sync/atomic.Value`.

Nada disso vem de um `func(in interface{}) bool`. O formato tipado destrava uma categoria inteira de trabalho de runtime.

### O trade-off

| Preocupação | Função | Tipado |
| --- | --- | --- |
| Ergonomia do autor | Excelente — é só Go | Verboso — cada cláusula é um struct |
| Serialização | Impossível — código não marshalla | Nativa — JSON / YAML de cara |
| Análise estática | Nenhuma — opaco pro engine | Árvore caminhável, shadowing, dead-rule report |
| Performance de matching | Linear no número de regras | Sub-linear com o índice certo |
| Segurança em tempo de compilação | Total — Go confere | Parcial — operador conferido em runtime |
| Regras escritas por não-engenheiros | Impossível | Possível (UI ou DSL em cima da árvore) |

A resposta pragmática no `bre-go` é manter os dois: o adaptador inmemory aceita o formato função; o adaptador indexed exige o formato tipado; o pacote `engine/parser` compila uma DSL string (`"market == \"DE\" AND days_to_departure < 7"`) pro formato tipado pra quem não quer escrever `StringCondition{...}` na mão. O struct Rule é o mesmo formato nos dois; só muda o campo que segura a condição.

Essa decisão de pista dupla é, na minha experiência, a escolha de design mais libertadora num modelo de regra. Você oferece pro engenheiro o caminho rápido. Você oferece pra todo mundo o caminho estruturado. Não precisa escolher.

## Action: o contrato sai pra fora aqui

A Action é onde a regra encontra o resto do mundo. O engine avalia a condição e aí tem que fazer alguma coisa. Essa coisa tem dois formatos possíveis que espelham a decisão da Condition.

O formato função:

```go
type Action func(in interface{}) interface{}
```

O formato tipado, mais ou menos assim:

```go
type Action struct {
    Type   string                 // "set_markup", "choose_provider"
    Params map[string]interface{} // específico por tipo
}
```

Função é mais rápido de escrever e arbitrariamente expressivo. Tipado deixa você serializar, deixa você conferir no registro que todo tipo de ação é um que o runtime sabe executar, e deixa fazer coisa interessante depois — tipo catalogar toda ação usada no rule set inteiro, ou recusar qualquer regra cuja ação exigiria efeito colateral fora de banda que o engine não consegue reverter.

No `bre-go`, Action é `func(interface{}) interface{}` pros engines in-process. O wrapper exec `exec.Executor[In, Out]` adiciona input e output tipados em volta:

```go
ex := exec.New[Order, string](e)
decision, matched, err := ex.Execute(ctx, Order{
    Amount:   250,
    Currency: "USD",
})
```

Essa é a segunda escolha libertadora do modelo: manter o formato do engine uniforme, e deixar o caller envolver pra ergonomia. O engine trabalha em `interface{}` porque é o que deixa polimorfo. O caller trabalha em `Order` e `string` porque é o que deixa o call-site legível.

## Facts: o que o engine vê

Os facts são o dicionário contra o qual a regra é avaliada. A Condition lê facts; a Action recebe facts. Os facts são a superfície pública entre o caller e o engine.

Os dois formatos já são familiares:

```go
// Facts tipados — o call-site usa tipo de domínio real.
type Order struct {
    Amount   float64
    Currency string
    Flagged  bool
    Market   string
}

// Facts genéricos — o que o matcher compara de verdade.
type Facts map[string]string
```

O engine indexed do `bre-go` roda contra `map[string]string` porque é o formato que o parser produz e o formato a partir do qual chaves de bucket podem ser montadas. String é plana. Hasheia limpo. O matcher não precisa saber o que `currency` "significa de verdade"; precisa saber o que buscar.

Já o código de domínio quer `Order.Amount`. O wrapper exec tipado faz a ponte: o caller passa `Order`; um marshaller transforma em `map[string]string` (ou no formato que o engine quer); o engine casa; o resultado volta como `Result`, que o caller desembrulha em `Decision`. O marshaller é a camada chata que ninguém escreve a respeito; é também o único ponto em que o mundo tipado encontra o mundo genérico. Vale dar um nome a ele e uma suíte de testes.

{{< plantuml title="O contrato: tipado nas bordas, genérico no meio" >}}
@startuml
skinparam shadowing false
skinparam componentStyle rectangle
skinparam defaultFontName "Helvetica"

actor "Código do caller" as C
rectangle "exec.Executor[In, Out]\nwrapper tipado" as W
rectangle "engine.Engine\nin: interface{} / map[string]string\nout: Result" as E
rectangle "Rule\nName, Condition, Action,\nPriority, Enabled" as R

C  --> W : Order, ctx
W  --> E : Facts (map[string]string)
E  --> R : avalia
R  --> E : casou, resultado da ação
E  --> W : Result
W  --> C : Decision (string)
@enduml
{{< /plantuml >}}

## Priority e Enabled: os botões de runtime

Priority e Enabled são os dois campos que os engenheiros sempre querem adicionar depois. Nunca parecem críticos de cara; sempre viram críticos no segundo em que alguma coisa importa.

Priority resolve ordem. No adaptador priority-ordered first-match (`engine/priority` no bre-go), regras são avaliadas da maior Priority pra menor; empate é resolvido por ordem de registro. Isso não é luxo — no momento em que duas regras conseguem casar com o mesmo fact, *alguma coisa* vai ordenar elas, e você prefere que seja o inteiro na regra do que o `git blame` de quem adicionou o arquivo primeiro.

Um formato comum:

```go
// Priority é uma escada de inteiros, não um valor único.
const (
    PriorityCompliance int = 1000 // mandato legal — roda primeiro
    PriorityRevenue    int = 500  // regra de markup e desconto
    PriorityExperiment int = 100  // override de experimento A/B
    PriorityDefault    int = 0    // fallback / catch-all
)
```

A escada é curta de propósito. Engenheiro vai tentar negociar uma Priority de 437 porque a regra dele é *quase* compliance, mas não *bem*. A escada força ele a botar a regra num tier com intenção. Se duas regras empatam dentro de um tier, esse é o tipo de conflito que você quer ver na hora do registro, não em produção.

Enabled é o off-switch. O off-switch é o que transforma uma decisão de regra ruim numa ligação telefônica em vez de um rollback. Tem que estar no modelo da regra — não numa lista "regras desativadas" à parte, não num feature flag externo — porque em runtime o engine ainda precisa carregar a regra, decidir que tá off, e pular limpo sem afetar a semântica de matching das outras. Um `Enabled bool` no struct faz isso pelo custo de um campo.

Tem uma decisão sobre o Enabled que vale fazer cedo: regra desativada ainda aparece no log de explicação? Minha resposta sempre foi *sim*. Se uma regra tá desligada, a investigação lá embaixo precisa ver que estava desligada, não só ausente. Regra ausente e regra desligada parecem a mesma coisa pra quem lê o log sem telemetria; um "desligada" explícito é a gentileza que você deixa pro seu eu futuro às 3 da manhã.

## Metadado: fora do Rule, dentro do registro

Essa é a parte do modelo de regra que o engine não precisa. É a parte que todo mundo precisa.

```go
type RuleMetadata struct {
    Owner       string
    Intent      string
    Created     time.Time
    Author      string
    Ticket      string
    Experiment  string
    ReviewAfter time.Time
}
```

O `bre-go` mantém o Rule do engine limpo (Name, Condition, Action, Priority, Enabled) e deixa o metadado morar num `RuleInfo` lister que adaptadores aderem opcionalmente. A razão é simples: o matcher não precisa de um `ReviewAfter`. O log de explicação talvez. A UI de admin com certeza. A auditoria de compliance com absoluta certeza. O matcher não tem que pagar o custo de carregar campo que nunca lê.

Separar metadado do Rule tem um benefício duradouro: deixa o schema de metadado evoluir sem forçar reconstrução do engine. A gente adicionou um campo `Experiment` três meses depois do engine subir, e o código do engine não mudou.

## A metáfora do contrato

O modelo de Rule é o contrato entre intenção de negócio e execução em runtime. Desmonta essa frase e você tem as regras de design que produziram tudo acima.

O contrato é *estreito*. O tipo Rule carrega o que o engine precisa saber, e nada mais. Campo só do engine (Priority, Enabled) tá no tipo. Campo de metadado (Owner, Ticket) tá num sidecar. Conveniência de autoria (string de DSL, builder fluente) fica em cima do tipo, não dentro.

O contrato é *estável*. O `bre-go` tá no v0.19 e o formato do Rule mudou duas vezes. Cada mudança foi amarrada num ADR documentado. A questão não é que o struct nunca pode mudar; é que mudar tem procedimento, porque todo adaptador e todo teste depende dele.

O contrato é *tipado nas bordas*. O caller escreve `Order`. O engine lê `map[string]string`. O wrapper faz a ponte. Botar `interface{}` na fronteira é o que deixa o engine polimorfo; botar tipo em volta da fronteira é o que deixa o call-site legível.

O contrato é *explicável*. O Rule tem Name e Description. A Condition tem árvore que o engine consegue caminhar. A Action tem Type que o catálogo lista. Cada um deles é um compromisso pequeno que se acumula em "o sistema se explica" três posts à frente.

## O que vem a seguir

O próximo post pega o mesmo tipo Rule e faz a pergunta mais difícil: *como ele fica quando mora em disco?* É onde YAML e JSON voltam, onde versionamento aparece, onde validação de schema começa a importar, e onde a ideia de "regra como dado" ganha o nome.

O post seguinte entra na semântica de matching — first-match versus all-match, priority versus specificity, cláusula indexável versus pós-filtro, e o formato estranho do bug que você ganha quando dois adaptadores discordam sobre qual regra dispara.

Por enquanto, a lição é o contrato. Se o tipo Rule em memória carrega as coisas certas, toda camada acima e abaixo tem onde se apoiar. Se carrega demais, as camadas ficam pesadas. Se carrega de menos, as camadas ficam espertas. Desenhar o tipo Rule é o momento em que você decide qual tipo de erro tá disposto a cometer depois.

Eu prefiro o de menos. A tentação do mapa, por mais sedutora que seja, produz sistema que não envelhece. O struct estreito, desenhado devagar, envelhece.
