---
title: "Regras Como Dado, Não Código"
subtitle: "Mover regra pra YAML é a parte fácil. Deixar o loader confiável é onde mora o trabalho."
author: helio
layout: post
date: 2023-08-16T10:00:00+00:00
series:
  - pricing-engineering
series_order: 3
categories:
  - Engineering
  - Pricing
  - Architecture
tags:
  - pricing
  - business-rules
  - rule-engine
  - yaml
  - json
  - schema
  - architecture
description: "Regra como dado só vira ideia útil quando o loader valida, versiona e falha de forma segura. Esse post trata o loader como a fronteira que ele de fato é."
---

A primeira vez que uma edição de regra subiu pra produção sem deploy, o time comemorou.

Foi uma mudança pequena. Markup de 3% virou 4% pra um segmento de mercado. Alguém abriu o YAML, mudou o número, o pipeline pegou, o serviço fez hot-reload, o próximo request precificou com o valor novo. Cinco minutos da ideia à produção. A gente tirou print do dashboard e pinou no canal.

Seis semanas depois alguém colou uma regex no campo `markup_percentage` sem querer. A string passou no parse do YAML — YAML aceita `"^[A-Z0-9]+$"` como valor sem reclamar — e o loader entregou pro engine uma regra cuja ação tinha regex onde devia ter número. O engine, defensivamente, retornou zero. Toda reserva daquele segmento perdeu o markup pelas próximas seis horas, até um gráfico drifar o suficiente pra acordar alguém. O fix levou noventa segundos. A investigação consumiu boa parte de um sábado.

Essa história é o resto desse post. Regra como dado só vira ideia útil quando o loader é tratado como a fronteira que ele de fato é.

## Por que "regra como código" para de funcionar

O post anterior abriu o struct Rule e defendeu que o formato em memória é o contrato. Esse contrato funciona bem enquanto toda mudança de regra passa pelo `git`. Você escreve Go, muda um literal de struct, sobe um binário. O compilador pega typo. Teste roda antes da mudança chegar em prod. A cadência das edições de regra é a cadência dos deploys, e a maioria dos times vive bem com isso por um tempo.

O ponto de quebra chega quando a frequência de edição de regra ultrapassa a cadência de deploy que o time consegue manter limpa. Em sistema de pricing isso vem rápido. Um time que queria shippar duas mudanças de regra por trimestre acaba querendo shippar três por semana. As branches se multiplicam. A release note ganha uma seção "mudanças de regra" que ninguém lê. Reverter um deploy passa a significar reverter código não relacionado junto com a regra. O deploy vira o lugar onde edição de regra vai morrer.

É aí que aparece o YAML. Alguém escreve um loader. As regras saem do arquivo Go e vão pra uma pasta.

O que sai junto, se você não tiver cuidado, é toda garantia que o compilador te dava de graça.

## O que você perde quando a regra sai da árvore de código

Três coisas, principalmente.

**Você perde validação de schema.** O compilador que recusava `markup_percentage: "^[A-Z0-9]+$"` foi embora. Ninguém lê o YAML além do loader, e o loader, por padrão, aceita o que o YAML decide ser válido.

**Você perde análise estática.** A IDE que pintava nome de campo errado foi embora. O revisor que pegava tipo errado num pull request foi embora. O arquivo de regra virou o caderno pessoal de alguém até você botar um schema em cima.

**Você perde atomicidade.** Deploy de código é um evento. Reload de YAML são N eventos — um por arquivo, um por erro de parse, um por falha de validação. O sistema tem que decidir, em tempo real, o que fazer com cada um.

Cada uma dessas dá pra recuperar. Basta *construir o loader como peça de engenharia*, não como uma chamada de `yaml.Unmarshal` enfiada no startup do serviço. O trabalho do resto desse post é descrever esse loader.

## O arquivo de regra: pequeno o bastante pra ler, estruturado o bastante pra validar

O formato do arquivo de regra é a primeira coisa com que o loader trabalha. Tem uma tentação, quando o time concorda no YAML, de jogar todo campo possível no topo e deixar o loader decidir qual importa. Aguenta. O formato do arquivo é a sua única API.

Um formato que funciona, modelado num rule store de pricing:

```yaml
version: 1
rules:
  - id: short_lead_time_markup_de
    name: "DE short lead-time markup"
    description: "markup de 3% em reservas Alemanha com menos de 7 dias"
    owner: pricing-de
    intent: |
      Capturar demanda em reservas de janela curta na Alemanha,
      onde restrição de capacidade reduz a sensibilidade a preço.
      Revisado no Q1.
    priority: 500
    enabled: true
    when:
      market:
        eq: DE
      days_to_departure:
        lt: 7
    then:
      type: set_markup
      value: 3.0
    metadata:
      ticket: PRICE-1473
      experiment: ELAST-2023-Q3
      review_after: 2024-02-16
```

Algumas coisas nesse formato parecem pequenas e merecem o destaque.

O `version: 1` no topo do arquivo é o primeiro ponto de decisão do loader. No dia em que o schema mudar — e vai — o loader precisa saber qual schema aplicar. Versionar o formato do arquivo é o que deixa o time adicionar campo sem quebrar carga histórica.

O bloco `when` usa operador explícito (`eq`, `lt`) em vez de valor solto. O formato solto parece mais limpo (`market: DE`), mas torna todo operador implícito, e operador implícito é como `market: "DE,FR"` acaba interpretado por metade do time como "DE OR FR" e pela outra metade como a string literal "DE,FR". Operador explícito custa cinco caracteres e remove uma categoria de bug.

O bloco `then` usa ação tipada (`type: set_markup, value: 3.0`) em vez de valor livre. É a mesma decisão que o Post 2 tomou pro modelo em memória. O catálogo de tipos de ação é o catálogo de efeitos colaterais que o engine sabe executar. Um campo YAML com tipo de ação desconhecido é um que o loader rejeita pelo nome.

O bloco `metadata` carrega tudo que o engine não precisa mas todo mundo precisa. Não é opcional na prática. É opcional no schema só porque o YAML não devia falhar no parse quando um arquivo antigo não tem `review_after`; o *trabalho* do loader, em separado, é emitir um warning quando ver isso.

## O loader é a fronteira

Eis o formato de um loader que merece o nome. É mais do que um `yaml.Unmarshal`:

```
ARQUIVO EM DISCO
     │
     ▼
┌────────────────────────────────────────────┐
│ 1. PARSE                                   │
│    yaml/json → []RawRule                   │
│    fail-fast em erro de sintaxe            │
└────────────────────────────────────────────┘
     │
     ▼
┌────────────────────────────────────────────┐
│ 2. VALIDAR POR REGRA                       │
│    schema, tipo, campo obrigatório,        │
│    tipo de ação ∈ catálogo conhecido       │
│    coletar erro com índice da regra        │
└────────────────────────────────────────────┘
     │
     ▼
┌────────────────────────────────────────────┐
│ 3. VALIDAR O CONJUNTO                      │
│    nome único, sanidade de priority,       │
│    detecção de regra morta, alcançabilidade│
└────────────────────────────────────────────┘
     │
     ▼
┌────────────────────────────────────────────┐
│ 4. COMPILAR                                │
│    raw → engine.Rule (Condition tipada,    │
│    callback de Action amarrado por nome)   │
└────────────────────────────────────────────┘
     │
     ▼
┌────────────────────────────────────────────┐
│ 5. TROCAR                                  │
│    substituição atômica do engine que tá   │
│    rodando — ou falha fechada              │
└────────────────────────────────────────────┘
```

Cada um dos cinco passos tem um modo de falha diferente. Cada um precisa ser desenhado pra isso.

### Parse: falha rápido, falha alto

Erro de parse de YAML ou JSON é o erro mais barato de detectar e o mais alto pra reportar. O loader deve recusar prosseguir se o arquivo tá malformado. Não tem recuperação inteligente — arquivo malformado é arquivo que o operador não quis shippar.

O JSON loader do `bre-go` (`engine/json.Loader[RC]`) retorna um `LoadError` cujo `Index` é `-1` pra falha em nível de documento (JSON quebrado, tipo errado no topo) e indexado em zero pra falha por regra. Essa distinção importa: falha em nível de documento quer dizer *nada nesse arquivo é confiável*. Falha por regra quer dizer *a terceira regra tá ruim; o resto pode ou não estar*. O loader deve tratar esses dois casos diferentes, e eles têm que ser distinguíveis no erro.

### Validar por regra: schema é o contrato

Validação por regra é onde o compilador volta. O loader confere que todo campo obrigatório tá presente, todo tipo bate, todo operador no bloco `when` é um que o parser conhece, todo tipo de ação no bloco `then` é um que o registro de ação conhece.

Aqui também é onde o valor monetário que entrou como string é rejeitado. O validador diz que `markup_percentage` tem que ser número; o loader retorna erro apontando linha 17, arquivo `de_markup.yaml`, índice 2. O operador recebe uma mensagem em que dá pra agir. O engine nunca vê a regra ruim.

Um formato útil de falha:

```go
type RuleLoadError struct {
    File      string
    RuleIndex int    // -1 pra nível de documento
    RuleID    string // "" se nem deu pra parsear o id
    Field     string // "then.value", "when.days_to_departure.lt"
    Message   string
    Cause     error
}
```

O custo de carregar File, RuleIndex, RuleID e Field é um struct. A economia, toda vez que algo falha, é a diferença entre "o loader falhou" e "o loader falhou porque a regra 2 em `de_markup.yaml` botou `then.value` como string". O operador não precisa ler o seu código.

### Validar o conjunto: regra não existe sozinha

Depois que cada regra é individualmente válida, o conjunto tem que ser válido como um todo. É onde o loader pega as falhas que nenhuma regra sozinha detecta:

- Duas regras com o mesmo nome. O engine não distingue em runtime; o loader tem que recusar antes de carregar.
- Uma regra cujas condições nunca casam porque uma regra anterior de prioridade maior já cobre os facts dela. O `engine/indexed.Engine.Diagnose()` do `bre-go` encontra isso estaticamente; o loader pode chamar depois do compile e emitir warning.
- Uma regra cuja ação referencia um nome de callback que o registro de ação não conhece. É o equivalente em YAML de função indefinida.
- Uma regra cuja priority tá no tier errado da escada de prioridade.

Cada uma dessas é uma classe de bug que pega o time uma vez e molda o loader dali pra frente.

### Compilar: de RawRule pra engine.Rule

O passo de compile é onde a árvore Condition tipada é construída a partir do bloco `when` parseado, onde o callback de ação é amarrado por nome a partir do catálogo, e onde a regra é normalizada pro formato que o engine consome.

```go
func compileRule(raw RawRule, actions ActionCatalogue) (engine.Rule, error) {
    cond, err := buildCondition(raw.When)
    if err != nil {
        return engine.Rule{}, fmt.Errorf("when: %w", err)
    }
    act, err := actions.Bind(raw.Then.Type, raw.Then.Params)
    if err != nil {
        return engine.Rule{}, fmt.Errorf("then: %w", err)
    }
    return engine.Rule{
        Name:        raw.ID,
        Description: raw.Description,
        Tags:        raw.Tags,
        Condition:   cond,
        Action:      act,
        Priority:    raw.Priority,
        Enabled:     raw.Enabled,
    }, nil
}
```

O passo de compile é onde o entendimento de schema do loader encontra o entendimento de runtime do engine. Separar a validação dele é o que deixa o loader produzir erros úteis na camada certa: erro de validação fala de YAML, erro de compile fala do engine.

### Trocar: atômico ou falha fechada

O último passo é o que a maioria dos times subestima. O loader acabou de produzir um engine novo. Agora ele tem que virar o engine que o serviço em execução consulta — e essa troca tem que acontecer sem mudança de comportamento observável além da edição da regra.

O hot path:

```go
type RuleStore struct {
    engine atomic.Value // segura *engine.Engine
}

func (s *RuleStore) Reload(ctx context.Context) error {
    raw, err := s.loader.Load(ctx)
    if err != nil {
        // O engine que tá rodando continua. Falha do loader não é
        // falha de runtime. O reload vira no-op até a fonte ser
        // arrumada.
        return fmt.Errorf("load: %w", err)
    }
    next, err := s.compile(raw)
    if err != nil {
        return fmt.Errorf("compile: %w", err)
    }
    s.engine.Store(next)
    return nil
}

func (s *RuleStore) Execute(ctx context.Context, in Facts) (Result, error) {
    return s.engine.Load().(*engine.Engine).Execute(ctx, in)
}
```

Duas coisas nesse trecho fazem mais trabalho do que parecem.

O reload é *fail-closed*. Se qualquer coisa no pipeline do loader falhar, o engine que tá rodando segue servindo tráfego com o rule set que já tinha. O sistema não degrada porque alguém empurrou um typo. Também não aplica silenciosamente um reload parcial — o engine novo é construído por inteiro ou não é.

A troca é *atômica*. O `sync/atomic.Value` guarda um ponteiro pro engine inteiro. O caminho do Execute lê o ponteiro uma vez por chamada. Nenhum request vê um rule set carregado pela metade. É exatamente o padrão que o adaptador indexed do `bre-go` usa por dentro pro snapshot pós-Build.

{{< plantuml title="O loader é a fronteira entre intenção autoral e comportamento em runtime" >}}
@startuml
skinparam shadowing false
skinparam componentStyle rectangle
skinparam defaultFontName "Helvetica"

actor "Operador" as O
rectangle "Arquivos de regra\n(YAML / JSON)" as F
rectangle "Loader\nparse → valida → compila" as L
rectangle "Engine em execução\n(snapshot N)" as E1
rectangle "Engine novo\n(snapshot N+1)" as E2
rectangle "Caminho do request\nExecute(ctx, facts)" as R

O --> F : edita
F --> L : pickup
L -[#red]-> O : fail-closed (erro de validação)
L --> E2 : compile com sucesso
E2 --> E1 : troca atômica
R --> E1 : lê ponteiro uma vez
@enduml
{{< /plantuml >}}

## Evolução de schema: mudar o formato sem quebrar histórico

O `version: 1` no topo do arquivo é o que faz a evolução de schema ser sobrevivível. Quando o schema precisar mudar — digamos, o bloco `then` ganha um operador novo, ou `metadata` ganha um campo obrigatório — o loader pode ser ensinado a ler os dois formatos.

O padrão que envelheceu melhor pra mim:

```go
type loader struct {
    versions map[int]ruleParser
}

func (l *loader) Load(b []byte) ([]engine.Rule, error) {
    var head struct{ Version int }
    if err := yaml.Unmarshal(b, &head); err != nil {
        return nil, fmt.Errorf("parse version: %w", err)
    }
    parser, ok := l.versions[head.Version]
    if !ok {
        return nil, fmt.Errorf("unknown schema version %d", head.Version)
    }
    return parser.Parse(b)
}
```

Três propriedades desse padrão que vale manter.

É *aditivo*. Versões de schema novas registram parsers novos. Arquivo velho segue carregando. O time que é dono de regras de dois anos atrás não tem que migrar quando o schema cresce.

É *explícito*. A versão tá no arquivo. O loader não infere o schema cheirando os campos. Loader que cheira schema funciona até parar de funcionar, em geral às 2 da manhã.

É *transitório*. Migrar de v1 pra v2 é trabalho de uma vez. O parser v1 não tem que viver pra sempre — quando todo arquivo tiver em v2, o parser v1 pode ser aposentado com release note. O trabalho do campo de versão é tornar essa aposentadoria deliberada, não manter parser vivo indefinidamente.

## Regra inválida: falha fechada, nunca silenciosa

O erro mais caro num loader é tratar regra inválida como regra ausente. Os dois deixam o engine sem aquela regra. Só um dos dois avisa o operador que tem coisa errada.

O default que cheguei:

- Falha em nível de documento (YAML / JSON malformado, versão de schema desconhecida): o arquivo inteiro é rejeitado, o engine atual segue rodando, o loader retorna erro.
- Falha por regra (erro de validação numa das N regras): o *arquivo inteiro* é rejeitado. Não a regra. O arquivo.

Essa última escolha é a que mais time empurra de volta. Mas as outras regras do arquivo ainda são válidas, vão argumentar. Por que jogar fora?

Porque carga parcial faz o sistema parar de ser explicável. Se o operador edita `de_markup.yaml` e uma regra falha na validação, a pergunta que ele quer responder é *o que o engine tá rodando agora?* Se o loader rejeitou o arquivo, a resposta é a versão anterior do arquivo, inteira. Se o loader rejeitou uma regra, a resposta é a versão nova do arquivo *menos uma regra*, que é um rule set que ninguém escreveu, ninguém revisou, e ninguém reconstrói a partir do version control. O engine de carga parcial é um estado que nenhum humano aprovou.

Um reject alto é um estado que alguém aprovou: o arquivo anterior. O custo é uma regra que não recebe o update até o operador arrumar o typo. O benefício é um sistema que nunca roda silenciosamente uma configuração que nenhum humano escreveu.

## Versionar o rule store, não só as regras

A maioria dos times versiona os arquivos de regra no `git`. Isso resolve "como essa regra estava um mês atrás?" — mais ou menos, porque diff de YAML é famoso.

O que o `git` sozinho não resolve é *o que o engine tava rodando às 14:32 de terça?* Pra isso você precisa de outro tipo de versão: a versão do *snapshot* que o engine tinha carregado naquele momento.

Uma prática pequena mas duradoura: marca todo reload bem-sucedido com um ID de snapshot, loga, expõe no `/healthz`. O ID do snapshot pode ser um hash do rule set canonicalizado e compilado; não precisa ser sequencial. O que precisa é *reproduzível a partir da fonte*.

```go
type Snapshot struct {
    ID        string    // sha256 das regras canonicalizadas
    LoadedAt  time.Time
    Source    string    // sha do commit, ou checksum do arquivo
    RuleCount int
}
```

Quando alguma coisa dá errado em produção, a pergunta não é "o que o arquivo diz agora?" A pergunta é "o que tava carregado às 14:32?" O ID do snapshot é a única coisa que responde sem ambiguidade. `ExportSnapshot` / `LoadSnapshot` do `bre-go` foram construídos exatamente pra isso: o engine serializa o estado compilado a qualquer momento, e uma sessão de replay carrega o mesmo estado pra reproduzir a decisão.

## Observabilidade do plano de dados

Loader que funciona em silêncio é loader que tá te enganando. A superfície mínima de sinal que eu empurro pros times shippar desde o dia um:

- Counter: reloads com sucesso, com o ID do snapshot como label.
- Counter: reloads que falharam, com o estágio da falha (parse / valida / compila / troca) e uma razão curta.
- Gauge: ID do snapshot atual, contagem atual de regras, data de review_after mais antiga no conjunto ativo.
- Linha de log por reload falho, incluindo arquivo, índice da regra, id da regra, campo e razão.

Esses quatro sinais transformam um arquivo YAML em algo operável. Sem eles, o operador tem que escavar log de serviço esperando que o parser tenha printado algo útil. Com eles, o dashboard mostra o rule store como componente de primeira classe do serviço.

## O que a gente acordou até aqui

Três posts dentro, o contrato tá começando a tomar forma. O struct Rule do Post 2 é o formato em memória. O schema desse post é o formato em disco. O loader é a função que transforma um no outro, e o loader é por si só uma superfície de engenharia — validada, versionada, observável, falha fechada.

O próximo post sai do loader e vai pro matcher. Com uma árvore Condition tipada e um Rule set limpo, o engine tem que decidir *quais* regras casam com um conjunto de facts. Essa decisão acaba sendo a parte mais simplificada da maioria dos sistemas de regras. First-match, all-match, priority-ordered, specificity-ordered — cada um é uma aposta diferente sobre como as regras interagem. O quinto post pega essa decisão e constrói o pipeline de avaliação que transforma regras casadas em resultado que o caller usa.

Por enquanto, o que a gente acordou é o loader. Regra como dado não é um arquivo YAML. Regra como dado é um arquivo YAML *mais um loader que trata a autoria como a fronteira que ela de fato é*. A comemoração quando edição de regra sobe sem deploy é real. O que faz a comemoração ser segura de repetir na manhã seguinte é o loader.
