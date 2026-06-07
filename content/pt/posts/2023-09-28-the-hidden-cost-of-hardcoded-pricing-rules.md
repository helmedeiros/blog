---
title: "O Custo Escondido de Regras de Pricing Hardcoded"
categories:
  - Architecture
  - Engineering
  - Pricing
date: 2023-09-28
tags:
  - pricing
  - motor-de-regras
  - divida-tecnica
  - monetizacao
  - arquitetura-de-software
description: "Por que regra hardcoded parece responsável até deixar de parecer, e o que de fato faz um time pedir um motor de regras."
subtitle: "Regra hardcoded nunca foi o problema de verdade. Era sintoma."
---

A primeira regra de pricing com a qual me lembro de me preocupar não parecia perigosa.

Era pequena. Uma condição específica de mercado, um ajuste percentual e poucas linhas de código. Nada nela sugeria que ia virar parte de um problema bem maior.

```java
if (market.equals("DE")) {
    markup = BigDecimal.valueOf(2.5);
}
```

Na época, parecia uma decisão de engenharia responsável. O negócio queria uma mudança. A implementação era direta. A regra tinha teste. O deploy era seguro.

É assim que a maioria das regras hardcoded de pricing começa.

Não nasce como dívida técnica.

Nasce como entrega.

## Toda regra de pricing começa pequena

O problema é que sistema de pricing raramente continua pequeno.

Uma regra simples de mercado vira uma regra específica de provedor.

```java
if (market.equals("DE") && provider.equals("rail")) {
    markup = BigDecimal.valueOf(3.0);
}
```

Depois aparece uma condição de antecedência.

```java
if (market.equals("DE")
        && provider.equals("rail")
        && daysBeforeDeparture < 7) {
    markup = BigDecimal.valueOf(4.0);
}
```

Depois chega um experimento.

```java
if (market.equals("DE")
        && provider.equals("rail")
        && daysBeforeDeparture < 7
        && experimentEnabled("summer_2023")) {
    markup = BigDecimal.valueOf(1.8);
}
```

Cada mudança, isolada, faz sentido.

Juntas, criam um sistema cada vez mais difícil de explicar.

## Por que regra hardcoded parece boa no começo

Regra hardcoded otimiza pra velocidade.

| Benefício | Por que o time gosta | Custo futuro |
| --- | --- | --- |
| Implementação rápida | Valor de negócio imediato | Mudança futura mais lenta |
| Teste fácil | Validação local | Comportamento global continua opaco |
| Workflow familiar | Direcionado por pull request | Conhecimento de negócio fica escondido no código |
| Deploy simples | Não precisa de plataforma adicional | Toda mudança exige mão de engenharia |

O problema não é esses benefícios serem falsos. O problema é que eles são reais.

É por isso que a gente continuava adicionando regra muito depois do sistema ter ficado difícil de evoluir. Cada regra passava pela mesma barra que tinha feito a anterior parecer razoável.

## O pesadelo do engenheiro de pricing

Uma hora alguém faz uma pergunta simples.

*Por que esse markup é 3,2%?*

Ou: *qual experimento introduziu essa regra?*

Ou: *essa condição ainda importa?*

O código normalmente consegue dizer o que acontece. Raramente diz por quê.

> Pergunta: Por que o markup é 3,2%?  
> Resposta do código: Porque essa condição bateu.  
> Resposta do negócio: Ninguém tem certeza.

É aqui que sistema de pricing acumula complexidade escondida. A regra sobrevive não porque alguém defendeu, mas porque remover parece mais arriscado que manter. Assimetria de risco preserva regra muito depois do motivo dela ter expirado.

## Regra é decisão de negócio antes de ser código

Uma regra de pricing normalmente começa como hipótese de negócio.

> Cliente que compra perto da partida pode tolerar markup maior.

Ou:

> Esse provedor se comporta diferente e precisa de uma estratégia dedicada.

Só depois é que essa ideia vira lógica executável. O caminho da hipótese até produção parece com isso:

{{< plantuml title="Uma regra de pricing é uma decisão de negócio muito antes de ser código" >}}
@startuml
skinparam shadowing false
start
:Decisão de negócio;
:Hipótese de pricing;
:Definição de regra;
:Código;
:Comportamento em produção;
stop
@enduml
{{< /plantuml >}}

O erro que a gente continuava cometendo era preservar só o último passo. O código sobrevivia. A hipótese se perdia. A decisão de negócio virava folclore.

Uma das lições mais importantes que aprendi foi que time de pricing deveria preservar mais do que código. Deveria preservar o raciocínio.

## Lógica não é política

Lógica de pricing explica como algo acontece. Política de pricing explica por que deveria acontecer.

Uma plataforma de pricing madura deixa as duas coisas visíveis.

```yaml
id: short_lead_time_markup
owner: pricing-team
reason: Aumentar receita em compras com pouca antecedência
metric: revenue_per_search
conditions:
  market: DE
  provider: rail
  days_before_departure: "< 7"
action:
  markup: 4.0
```

O valor dessa estrutura não é o YAML. O valor é que ownership, intenção, métrica e condição ficam explícitos — e, portanto, revisáveis, discutíveis e removíveis.

Uma regra hardcoded responde a pergunta *o que isso faz?* Uma regra em formato de política responde *por que isso existe, e como a gente saberia que deixou de ser uma boa ideia?*

## Interação entre regras é onde a complexidade se esconde

A maior parte dos problemas de pricing não vem de regra individual. Vem da interação entre regras.

Imagine quatro regras empilhadas em cima da mesma compra:

- Regra A: adiciona 3%
- Regra B: tira 1%
- Regra C: adiciona 2%
- Regra D: limita em 5%

As perguntas aparecem rápido:

- Qual regra executa primeiro?
- Regra pode sobrescrever outra?
- Várias regras podem se aplicar ao mesmo tempo?
- Como a gente explica o resultado final pra um agente de atendimento olhando uma compra específica?

Sistema de receita precisa de resposta pra essas perguntas antes do incidente acontecer. Quando o incidente acontece, você descobre a resposta da pior forma possível.

## Quando o engenheiro começa a pedir um motor de regras

Engenheiro raramente pede um motor de regras porque quer um motor de regras.

Pede porque já não consegue mais responder pergunta operacional básica.

- Quais regras estão ativas?
- Quem é o dono delas?
- Por que elas existem?
- A gente consegue simular?
- A gente consegue desativar sem deploy?
- A gente consegue explicar um preço final?

Nesse ponto, o problema não é mais implementação. É governança.

| Dor | Capacidade que tá faltando |
| --- | --- |
| Regra é difícil de encontrar | Descoberta |
| Regra é difícil de explicar | Rastreabilidade |
| Regra é arriscada de mudar | Validação |
| Regra exige deploy | Controle em runtime |
| Regra fica pra sempre | Gestão de ciclo de vida |

Não é problema de ferramenta. É problema de maturidade que a ferramenta tá sendo chamada pra tornar visível.

## O ciclo de vida importa mais que a sintaxe

Toda regra de pricing tem um ciclo de vida:

{{< plantuml title="Uma regra de pricing tem ciclo de vida, não só data de criação" >}}
@startuml
skinparam shadowing false
start
:Oportunidade;
:Hipótese;
:Criação da regra;
:Validação;
:Lançamento;
:Medição;
:Decisão;
:Aposentadoria;
stop
@enduml
{{< /plantuml >}}

A maioria dos sistemas hardcoded é otimizada pra criação. Pouquíssimos são otimizados pra aposentadoria.

Esse desequilíbrio vai ficando caro com o tempo. O custo não é pago pelo engenheiro que adicionou a regra. É pago pelo time que herda o sistema três anos depois e não consegue dizer quais das 600 regras dá pra remover.

## O que aprendi

Regra hardcoded nunca foi o problema real.

Era sintoma.

O desafio real era complexidade de negócio não gerenciada. Mercado evolui. Experimento acumula. Acordo comercial muda. Comportamento do cliente muda. E, com o tempo, o código vira o único lugar onde a organização lembra como pricing funciona.

É nesse momento que o time começa a pensar em motor de regras — não porque motor de regras seja interessante, mas porque a complexidade do negócio finalmente fica impossível de ignorar.

## Reflexão final

Em algum momento, a gente parou de perguntar *como a gente escreve regra de pricing?* e passou a perguntar *como a gente gerencia centena delas com segurança?*

Essa pergunta mudou tudo. Tirou a conversa do código e levou pra ownership, explicabilidade, observabilidade, governança e ciclo de vida de cada regra que o sistema carrega.

A gente subdimensionava o custo de uma regra de pricing no momento em que a adicionava, basicamente toda vez. O custo aparecia depois — no engenheiro que precisava explicar um preço durante um incidente, no analista que não conseguia dizer a qual experimento uma regra pertencia, no parceiro de operações que silenciosamente contornava uma condição que ninguém topava remover. A conta chegava. Só chegava em outro lugar.

Um bom teste do nosso sistema de pricing, então, não era com que velocidade a gente conseguia adicionar uma regra. Era com que confiança a gente conseguia apagar uma.
