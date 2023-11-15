---
title: "Casando Regras em Escala"
subtitle: "A maioria dos bugs de rule engine não tá na ação. Tá no jeito como o engine decidiu qual regra deveria disparar."
author: helio
layout: post
date: 2023-11-15T10:00:00+00:00
series:
  - pricing-engineering
series_order: 4
categories:
  - Engineering
  - Pricing
  - Architecture
tags:
  - pricing
  - business-rules
  - rule-engine
  - matching
  - architecture
  - algorithms
description: "Semântica de matching decide qual regra dispara quando mais de uma poderia. Esse post caminha pelas quatro políticas comuns, os operadores que cada uma suporta, e o bug que cada uma esconde."
---

Um cliente uma vez foi cobrado de um markup de 5% por cima de um markup de 3%, na mesma reserva, na mesma linha.

As duas regras estavam corretas. As duas regras casaram com os facts. O engenheiro que escreveu a segunda regra não tinha visto que a primeira existia; o engenheiro que escreveu a primeira tinha trocado de time um ano antes. O engine era uma coisa caseira velha que avaliava toda regra em ordem de inserção, aplicava toda ação que casasse, e combinava de forma aditiva. Nenhum dos autores tava errado. O sistema tava.

Essa conversa, com um reembolso pendurado, foi onde eu aprendi que *matching* é a parte do rule engine que a maioria dos times constrói duas vezes. A primeira versão é o que o primeiro autor achou que "casar" significava. A segunda versão é o que o sistema precisava de verdade. A camada de ação acima e o loader abaixo pegam a maior parte do crédito; o matching pega a maior parte dos bugs.

Esse post é sobre as quatro políticas de matching que um engine de verdade precisa escolher, os operadores que cada uma suporta, e o formato do bug que cada uma esconde. A referência, de novo, é o [`bre-go`](https://github.com/helmedeiros/bre-go), que entrega quatro adaptadores atrás da mesma porta `engine.Engine`: insertion-order all-match, insertion-order first-match, priority-ordered first-match, e um matcher indexed sub-linear.

## As quatro políticas de matching

Você plota qualquer rule engine em dois eixos: em quantos matches age, e como escolhe entre eles.

| Política | Age sobre | Resolve empate via | Lê que nem |
| --- | --- | --- | --- |
| Insertion-order first-match | A primeira regra que casa | Posição no arquivo | Uma decision table |
| Insertion-order all-match | Toda regra que casa | Nenhum — toda casada age | Um pipeline de efeitos |
| Priority-ordered first-match | A regra de maior priority que casa | Uma escada de inteiros | Uma política de precedência |
| Specificity-ordered | A regra mais específica que casa | Contagem de condições, ou peso | Uma hierarquia conceitual |

Cada uma é uma aposta diferente sobre como as regras do seu sistema se relacionam. Se você pega a errada, autoria esperta nenhuma salva.

### Insertion-order first-match

O engine mais simples lê regra de cima pra baixo e retorna no primeiro match. O adaptador `engine/firstmatch` do `bre-go` faz exatamente isso: avalia em ordem de inserção, retorna na primeira regra que casa, nunca avalia as outras.

É o que a maioria das pessoas imagina quando fala "a regra disparou". É o que decision table faz. É o que todo roteador que eu já debuguei faz. O modelo mental é pequeno.

O bug é dependência posicional. Reordena o arquivo e a resposta muda. Uma regra que dispara em reserva alemã de última hora tem que estar acima da regra que dispara em *toda* reserva alemã, ou a segunda come a primeira. Engenheiros que adicionam regra nova no fim do arquivo descobrem, seis meses depois, que ela nunca disparou. A ordem do arquivo agora é load-bearing, e ninguém avisou o YAML.

```yaml
# A ordem importa aqui. A segunda regra nunca vai disparar.
- id: germany_markup
  when: { market: { eq: DE } }
  then: { type: set_markup, value: 2.0 }

- id: germany_short_lead_time_markup
  when:
    market: { eq: DE }
    days_to_departure: { lt: 7 }
  then: { type: set_markup, value: 3.0 }
```

First-match é boa escolha quando as regras genuinamente têm ordem natural — tabela de roteamento, cadeia de fallback, hierarquia de override. É escolha ruim quando as regras são políticas independentes que por acaso foram escritas no mesmo arquivo. O time tem que saber em qual mundo tá.

### Insertion-order all-match

A política dual: caminha toda regra, acumula todo match, roda toda ação. O adaptador `engine/inmemory` do `bre-go` é o formato canônico — toda regra que casa contribui; o listener conta os matches; a última ação ganha no `Output`; todo match aparece em `Matched`.

É o que você quer quando regra é política *aditiva*. Três markups empilham. Seis tags se aplicam. O trabalho da camada de matching é só encontrar tudo; o trabalho da camada de ação é combinar.

O bug é colisão. Duas regras que setam o mesmo campo com valores diferentes colidem silenciosamente; o engine tem que escolher uma, e a escolha é implícita. O cliente cobrado duas vezes na história acima? Engine all-match, acumulando markup, sem detecção de colisão.

All-match funciona bem quando as ações são *comutativas*. Adicionar tag é comutativo; ordem não importa. Setar preço não é; o último write ganha, e "último" depende da ordem de inserção, que depende do arquivo que o time edita há dois anos. A mesma dependência posicional do first-match, agora cozida no resultado em vez da decisão de avaliar.

### Priority-ordered first-match

Priority substitui "posição no arquivo" por "inteiro na regra". O adaptador `engine/priority` do `bre-go` caminha as regras da maior Priority pra menor; empate é resolvido por ordem de registro; o primeiro match ganha.

É o que a maioria dos sistemas em produção acaba escolhendo pra engine de *decisão*: escolher uma regra, escolher de forma determinística, deixar o autor declarar a precedência explicitamente.

```yaml
- id: compliance_markup_override
  priority: 1000
  when: { regulated_market: { eq: true } }
  then: { type: set_markup, value: 0.0 }

- id: germany_short_lead_time_markup
  priority: 500
  when:
    market: { eq: DE }
    days_to_departure: { lt: 7 }
  then: { type: set_markup, value: 3.0 }

- id: germany_baseline_markup
  priority: 100
  when: { market: { eq: DE } }
  then: { type: set_markup, value: 2.0 }
```

O bug aqui é mais sutil. Priority é um número, e número é negociável. O engenheiro que quer a regra dele "quase tão importante quanto compliance" vai discretamente registrar uma com 999. O engenheiro que quer o experimento dele "acima da baseline mas não muito longe" vai botar 437. Depois de dois anos o campo priority parece o chão de um bar perto do fechamento.

A defesa, do Post 2: priority é escada de inteiros, não inteiro livre. A escada tem tiers nomeados. Regra nova entra num tier. Empate entre tiers aparece na hora do registro. A disciplina mora no loader, não no engine.

### Specificity-ordered

A ideia sedutora: *a regra mais específica ganha*. Especificidade é intuitiva. Uma regra com três condições é mais específica que uma com uma; a de três deveria ganhar da de uma, porque descreve um mundo mais estreito.

É a política de matching que o CSS usa. É também a política que ninguém implementa em rule engine de negócio, porque na hora em que você tenta definir "específico" com precisão, descobre que são duas coisas diferentes.

**Especificidade por contagem de condição.** Três condições ganham de uma. Simples de computar. Falha no momento em que uma das condições é tautologia tipo `enabled: true`. O autor agora ganha a competição adicionando termo sem sentido.

**Especificidade por dimensão ponderada.** Cada campo de condição tem peso; você soma os pesos das condições casadas. Funciona, mas os pesos agora são governança — exatamente o problema da priority, só que peso é por campo em vez de por regra. O loader tem que reforçar a tabela de pesos. O processo de change-management tem que tratar mudança de peso como mudança de política.

Eu nunca construí engine specificity-ordered pra produção. *Pensei* em construir umas duas vezes. Nas duas vezes, o time que queria descobriu, no meio do desenho, que o que queriam de verdade era priority com mais higiene em volta da escada. A intuição de especificidade é certa; as propriedades operacionais, erradas.

## Os operadores que o matcher precisa suportar

Política de matching é tão expressiva quanto os operadores das condições. Pegue poucos demais e os autores contrabandeiam expressão pra dentro da camada de ação. Pegue demais e o índice não consegue te ajudar.

### Igualdade

`market == DE`. A condição mais barata que existe. Todo rule engine suporta. Todo índice é construído em volta.

No engine indexed do `bre-go`, condições de igualdade são *contribuintes de chave de bucket*. O engine caminha a árvore Condition tipada no `Build()`, encontra toda cláusula `StringCondition{Op: OpEq}` e `SetCondition{Op: OpIn}`, e usa esses campos pra montar as chaves de bucket. Na hora do Execute, o matcher hashea os valores dos facts da request e olha o bucket. O resultado é sub-linear no número de regras: em 10 000 regras, matching dominado por igualdade é centenas de vezes mais rápido que o adaptador linear no mesmo input.

### Pertinência de conjunto

`market IN (DE, FR, IT)`. A extensão natural da igualdade. Mesma história de indexação: o engine fan-outa uma regra em várias chaves de bucket (DE → regra, FR → regra, IT → regra). O engine indexed do `bre-go` aceita isso enquanto o fan-out fica abaixo de um cap (1024 por padrão); acima disso, retorna `FanoutTooLargeError` porque o índice consumiria mais memória do que economiza.

O bug é o fan-out que você não vê chegando. Uma condição que diz `customer_segment IN (...)` com cinco valores tá tranquilo. A mesma condição seis meses depois, depois que marketing adicionou todo segmento que conseguiu pensar, são sessenta valores. A condição ainda valida. A contagem de bucket multiplica. O índice silenciosamente vira devorador de memória. Diagnóstico em nível de loader merece o destaque aqui.

### Desigualdade e negação

`flagged != true`. `currency NOT IN (BRL, ARS)`. São condições *pós-filtro* no engine indexed do `bre-go`: o engine não consegue usar pra estreitar o conjunto candidato, então avalia depois do lookup de bucket contra os candidatos que os termos indexados produziram. Adicionar negação não torna a regra não-indexável enquanto a regra ainda tiver pelo menos um termo indexável; regra puramente pós-filtro é rejeitada com `ErrNoIndexableTerms` porque forçaria o matcher num walk linear.

O formato que sai disso é *regra precisa de pelo menos um termo positivo de igualdade ou de pertinência pra ser sub-linear*. Essa é uma restrição que os autores vão resistir. É também a restrição que vira o engine de O(N) em O(K).

### Faixas

`days_to_departure < 7`. `amount BETWEEN 100 AND 500`. Faixas numéricas e de data. A `engine/parser.RangeCondition` do `bre-go` é inclusiva sobre `float64`, com `math.Inf(±1)` disponível pra intervalo semi-aberto.

Faixa é pós-filtro, igual negação. O índice não ajuda; o matcher caminha o conjunto candidato e avalia a faixa de cada regra contra os facts numéricos da request. O custo é pequeno na prática, porque o conjunto candidato já foi estreitado pelos termos de igualdade — mas só se a regra tiver pelo menos um termo de igualdade. Uma regra que é *só* uma faixa é uma regra de walk linear.

### Curinga

`market: *`. Uma condição que casa com qualquer valor. Tem dois jeitos de modelar.

O jeito errado: operador especial `Any` que o matcher tem que tratar como caso separado. Funciona mas bifurca o caminho de matching.

O jeito certo: não guarda o campo. Uma condição que casa com qualquer valor é *a ausência de condição*. A regra não restringe esse campo; o matcher não olha esse campo pra essa regra. O parser do `bre-go` não produz nó Condition pra campo ausente, o que deixa o trabalho do matcher uniforme demais pra dar errado: toda condição que existe é checada; todo campo não mencionado é por definição irrestrito.

É a decisão de operador que paga mais discretamente. O time não tem que debater "o que conta como curinga" — não tem curinga; tem condição e condição ausente. A lógica do matcher fica pequena.

## Matching multidimensional

Regra real de pricing toca vários campos ao mesmo tempo. Uma regra única que diz *Alemanha AND trem AND última hora AND mobile* tem quatro dimensões. O matcher tem que encontrar as regras cujas dimensões todas casam com a request.

A abordagem linear é caminhar toda regra e avaliar toda condição. Em 100 regras tá tranquilo. Em 1000 começa a doer. Em 10 000 é o gargalo.

A abordagem indexada é construir o produto cartesiano de chaves de bucket. Pra cada termo de igualdade e de pertinência, o engine constrói um bucket de hash. Na hora do Execute, o matcher hashea os facts da request e olha as regras candidatas. O conjunto candidato é pequeno. Condições pós-filtro são avaliadas contra os candidatos.

{{< plantuml title="O matcher indexed: bucket de hash estreita o candidato, pós-filtro refina" >}}
@startuml
skinparam shadowing false
skinparam componentStyle rectangle
skinparam defaultFontName "Helvetica"

rectangle "Facts da request\nmarket=DE\nchannel=rail\ndays=4\ndevice=mobile" as F

rectangle "Índice de bucket\n(construído no Engine.Build)" as B {
  rectangle "market=DE\n→ {R1, R7, R12}" as B1
  rectangle "channel=rail\n→ {R7, R12, R18}" as B2
  rectangle "device=mobile\n→ {R7, R12, R20}" as B3
}

rectangle "Conjunto candidato\nintersecção: {R7, R12}" as C
rectangle "Pós-filtro\ndays_to_departure < 7\n→ {R7}" as PF
rectangle "Match\nR7" as M

F --> B
B --> C
C --> PF
PF --> M
@enduml
{{< /plantuml >}}

O formato do ganho, dos relatórios científicos do `bre-go`: em 10 000 regras, matching indexed usando o formato de snapshot binário v0.16 é 2,93× mais rápido que o adaptador linear carregado de CSV. Em 100 000 regras o gap aumenta. Os números se movem com o formato do workload — bucket largo ajuda menos que estreito — mas o comportamento assintótico é a decisão de design.

O custo do desenho é a restrição sobre os autores: toda regra precisa de pelo menos um termo indexável. O ganho de runtime é a restrição se pagando.

## Desempate quando duas regras casam

A outra metade do matching é o que acontece quando mais de uma regra casa. As quatro políticas acima tratam isso de forma diferente, e cada uma tem um modo de falha.

| Política | Regra de desempate | Modo de falha |
| --- | --- | --- |
| Insertion-order first-match | A regra anterior ganha | Reordenar quebra comportamento em silêncio |
| Insertion-order all-match | Toda casada age | Ações em conflito colidem no mesmo campo |
| Priority-ordered first-match | Priority maior ganha; ordem de inserção é fallback | Priority drifta pra governança |
| Specificity-ordered | A mais específica ganha | "Específico" é duas coisas diferentes |

A defesa desonesta é fingir que o modo de falha não existe. A defesa honesta é expor a falha pro time na hora do load.

### Detecção de conflito no registro

As duas políticas que mais precisam de detecção de conflito são all-match e priority-ordered first-match. A checagem é a mesma: *pra qualquer par de regras, as duas conseguem casar com a mesma request?* Se sim, o engine tem que saber como resolver, e o time tem que saber qual vai disparar.

O `engine/indexed.Engine.Diagnose()` do `bre-go` faz uma versão tier-1 disso. Varre pares de regras e reporta as que nunca disparam porque uma regra anterior de prioridade maior já sombreia. A checagem é conservadora — pula pares onde a candidata sombra tem termo pós-filtro, então falso positivo é zero por desenho.

O custo de rodar Diagnose no startup é O(N² × F), onde F é a contagem média de pós-filtros. Em 1000 regras isso é milissegundos. Em 100 000 são segundos, por isso Diagnose é checagem de startup ou de endpoint admin, não de request.

O benefício é inegociável: o time descobre sombreamento antes da produção descobrir. Regra morta é regra que custou tempo pra escrever e vai custar tempo pra investigar quando "ela deveria ter disparado".

### Resolução de conflito como política

Os casos que o Diagnose não pega — duas regras que legitimamente casam porque foram desenhadas pra isso — precisam de política de resolução explícita. O formato mais limpo que vi:

```yaml
resolution:
  fields:
    markup_percentage: sum   # markup aditivo empilha
    base_price:        last  # último write ganha, ordenado por priority
    provider:          fail  # colisão é erro de registro
```

A política de resolução transforma comportamento implícito em política explícita. O time concorda, por escrito, o que acontece quando duas regras tocam o mesmo campo. O engine recusa carregar rule set que viola a política.

É uma daquelas decisões de desenho que parecem trabalho extra e viram o seguro mais barato possível. O cliente cobrado duas vezes no caso de abertura? A história termina com a gente adicionando uma linha `provider: fail` no arquivo equivalente. Duas regras novas em conflito agora são falha de CI, não reembolso.

## O formato do bug: onde matching dá errado

Três padrões respondem pela maioria dos bugs de matching que eu shippei ou vi shippar.

**A sombra.** A regra B é idêntica a um subconjunto das condições da A. A dispara primeiro, B nunca dispara. Seis meses depois, quando alguém desabilita A, B começa a disparar — e o sistema se comporta de um jeito que ninguém esperava. O fix é detecção de conflito no load. A defesa é exigir que toda regra seja alcançável.

**O reordenamento.** Ordem de regra mudou num refactor. Adaptador first-match muda comportamento. Nada na suíte de testes pegou porque os testes foram escritos contra uma ordem específica. O fix é marcar todo fixture de teste com a suposição de política em que se apoia. A defesa é desencorajar first-match pra regras que não são naturalmente ordenadas.

**A colisão.** Duas regras setam o mesmo campo. O engine all-match escolhe uma. A escolhida é função da ordem de inserção, que é função do histórico de autoria. O fix é a política de resolução acima. A defesa é tratar colisão de campo como erro de load.

Cada um desses bugs é barato de prevenir e caro de debugar. O custo da prevenção é uma passada de engenharia sobre o matcher; o custo do debug é o que o cliente achou que tava pagando. A assimetria é grande o bastante pra que o matcher mereça mais atenção do que a camada de ação quase sempre recebe.

## A lição de engenharia

A camada de ação de um rule engine é glamourosa. É onde o markup é computado, onde o experimento é aplicado, onde a decisão é *tomada*. É também onde a maioria dos engenheiros foca o esforço de design. A camada de ação é onde a reunião vai.

O matcher é desglamourizado. Parece não fazer nada: escolhe regra de uma lista. Escolher regra de uma lista não é o trabalho — *decidir qual regra pegar de qual lista* é o trabalho, e essa decisão é a política de matching.

Escolha a política de matching explicitamente. Exponha o modo de falha no loader. Construa detecção de conflito no startup. Faça o engine recusar carregar rule set que viola a política de resolução. Nenhuma dessas é preocupação de runtime. Todas são preocupação de load. Na hora que a request chega, a política de matching já foi validada, os conflitos já foram pegos, e as regras de resolução já foram acordadas.

É isso que escala significa nesse contexto. Escala não é 100 000 regras por segundo. Escala é 10 000 regras editadas por 30 pessoas em cinco anos, com o sistema ainda se comportando do jeito que o time acordou. O matcher é o que torna isso sobrevivível.

## O que vem a seguir

O próximo post é o pipeline de avaliação — o engine como sequência de estágios que pega regra carregada e fact de request e produz resultado. Matching é um desses estágios. Avaliação de condição, execução de ação, composição de resultado e explicação também são. O pipeline é o que transforma o "essas regras disparam" do matcher em resultado que o caller pode usar.

Depois disso, o post de teste desmonta o pipeline inteiro e mostra como escrever teste que protege o comportamento, não a implementação. E o post seguinte é explicabilidade, que volta a esse aqui: todo conflito detectado no load vira linha na explicação, toda regra sombra vira warning, toda decisão de priority vira motivo registrado.

Por enquanto, o matcher é a decisão de arquitetura. A maioria dos rule engines que vi falhar em produção falhou na camada de matching, não nas ações. O matcher é a única parte do engine que precisa ser honesta sobre os trade-offs dela, porque não consegue fingir. Pega first-match se as regras são ordenadas. Pega all-match se as ações são aditivas. Pega priority se o time consegue segurar uma escada de inteiros. Pula specificity até você estar pronto pra defender a tabela de pesos.

O cliente cobrado duas vezes em algum momento recebeu o reembolso. O engine ganhou uma política de resolução. Os dois engenheiros que escreveram aquelas regras originais nunca se encontraram. O sistema parou de deixar esse erro acontecer, que é pra isso que um matcher serve.
