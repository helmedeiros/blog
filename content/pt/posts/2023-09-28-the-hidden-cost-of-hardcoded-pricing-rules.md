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
description: "Por que regras de pricing hardcoded parecem responsáveis até deixarem de parecer, e o que de fato faz um time pedir um motor de regras."
subtitle: "Regras hardcoded nunca foram o problema real. Eram um sintoma."
---

A primeira regra de pricing com a qual me lembro de me preocupar não parecia perigosa.

Era pequena. Uma condição específica de mercado, um ajuste percentual e poucas linhas de código. Nada nela sugeria que viraria parte de um problema muito maior.

```java
if (market.equals("DE")) {
    markup = BigDecimal.valueOf(2.5);
}
```

Na época, parecia uma decisão de engenharia responsável. O negócio queria uma mudança. A implementação era direta. A regra tinha testes. O deploy era seguro.

É assim que a maioria das regras hardcoded de pricing começa.

Elas não nascem como dívida técnica.

Elas nascem como entrega.

## Toda regra de pricing começa pequena

O problema é que sistemas de pricing raramente continuam pequenos.

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

Individualmente, cada mudança faz sentido.

Coletivamente, elas criam um sistema cada vez mais difícil de explicar.

## Por que regras hardcoded parecem boas no início

Regras hardcoded otimizam para velocidade.

| Benefício | Por que o time gosta | Custo futuro |
| --- | --- | --- |
| Implementação rápida | Valor de negócio imediato | Mudanças futuras mais lentas |
| Teste fácil | Validação local | Comportamento global continua opaco |
| Workflow familiar | Direcionado por pull request | Conhecimento de negócio fica escondido no código |
| Deploy simples | Não precisa de plataforma adicional | Toda mudança exige envolvimento de engenharia |

O problema não é que esses benefícios sejam falsos. O problema é que eles são reais.

É por isso que times continuam adicionando regras muito depois do sistema ter ficado difícil de evoluir. Cada regra passa pela mesma barra que fez a anterior parecer razoável.

## O pesadelo do engenheiro de pricing

Eventualmente alguém faz uma pergunta simples.

*Por que esse markup é 3,2%?*

Ou: *qual experimento introduziu essa regra?*

Ou: *essa condição ainda importa?*

O código normalmente consegue dizer o que acontece. Ele raramente diz por quê.

> Pergunta: Por que o markup é 3,2%?  
> Resposta do código: Porque essa condição bateu.  
> Resposta do negócio: Ninguém tem certeza.

É aqui que sistemas de pricing acumulam complexidade escondida. A regra sobrevive não porque alguém a defendeu, mas porque remover parece mais arriscado do que manter. Assimetria de risco preserva regras muito depois do motivo de existir delas ter expirado.

## Regras são decisões de negócio antes de serem código

Uma regra de pricing normalmente começa como uma hipótese de negócio.

> Clientes que compram perto da partida podem tolerar markups maiores.

Ou:

> Esse provedor se comporta de forma diferente e precisa de uma estratégia dedicada.

Só depois é que essa ideia vira lógica executável. O caminho da hipótese até produção se parece com isto:

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

O erro que a maioria dos times comete é preservar só o último passo. O código sobrevive. A hipótese se perde. A decisão de negócio vira folclore.

Uma das lições mais importantes que aprendi foi que times de pricing deveriam preservar mais do que o código. Deveriam preservar o raciocínio.

## Lógica não é política

Lógica de pricing explica como algo acontece. Política de pricing explica por que deveria acontecer.

Uma plataforma de pricing madura torna as duas coisas visíveis.

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

O valor dessa estrutura não é o YAML. O valor é que ownership, intenção, métricas e condições ficam explícitos — e, portanto, revisáveis, discutíveis e removíveis.

Uma regra hardcoded responde à pergunta *o que isso faz?* Uma regra em formato de política responde *por que isso existe, e como saberíamos que deixou de ser uma boa ideia?*

## Interação entre regras é onde a complexidade se esconde

A maior parte dos problemas de pricing não é causada por regras individuais. É causada pela interação entre regras.

Imagine quatro regras empilhadas sobre a mesma compra:

- Regra A: adiciona 3%
- Regra B: remove 1%
- Regra C: adiciona 2%
- Regra D: limita em 5%

As perguntas aparecem rápido:

- Qual regra executa primeiro?
- Regras podem sobrescrever umas às outras?
- Várias regras podem se aplicar ao mesmo tempo?
- Como explicamos o resultado final para um agente de atendimento olhando uma compra específica?

Sistemas de receita precisam de respostas para essas perguntas antes do incidente acontecer. Quando o incidente acontece, você descobre as respostas da pior forma possível.

## Quando engenheiros começam a pedir um motor de regras

Engenheiros raramente pedem um motor de regras porque querem um motor de regras.

Pedem porque não conseguem mais responder perguntas operacionais básicas.

- Quais regras estão ativas?
- Quem é o dono delas?
- Por que elas existem?
- Conseguimos simular?
- Conseguimos desativar sem deploy?
- Conseguimos explicar um preço final?

Nesse ponto, o problema não é mais implementação. É governança.

| Dor | Capacidade ausente |
| --- | --- |
| Regras são difíceis de encontrar | Descoberta |
| Regras são difíceis de explicar | Rastreabilidade |
| Regras são arriscadas de mudar | Validação |
| Regras exigem deploy | Controle em runtime |
| Regras ficam para sempre | Gestão de ciclo de vida |

Isso não é um problema de ferramenta. É um problema de maturidade que a ferramenta está sendo chamada para tornar visível.

## O ciclo de vida importa mais que a sintaxe

Uma regra de pricing tem um ciclo de vida:

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

A maioria dos sistemas hardcoded é otimizada para criação. Pouquíssimos são otimizados para aposentadoria.

Esse desequilíbrio vai ficando caro com o tempo. O custo não é pago pelo engenheiro que adicionou a regra. É pago pelo time que herda o sistema três anos depois e não consegue dizer quais das 600 regras podem ser removidas.

## O que aprendi

Regras hardcoded nunca foram o problema real.

Elas eram um sintoma.

O desafio real era complexidade de negócio não gerenciada. Mercados evoluem. Experimentos acumulam. Acordos comerciais mudam. Comportamento do cliente muda. E, eventualmente, o código vira o único lugar onde a organização lembra como pricing funciona.

É nesse momento que times começam a pensar em motores de regras — não porque motores de regras sejam interessantes, mas porque a complexidade do negócio finalmente fica impossível de ignorar.

## Reflexão final

Eventualmente paramos de perguntar *como escrevemos regras de pricing?* e passamos a perguntar *como gerenciamos centenas delas com segurança?*

Essa pergunta mudou tudo. Tirou a conversa do código e levou para ownership, explicabilidade, observabilidade, governança e ciclo de vida de cada regra que o sistema carrega.

Se você está olhando para um código de pricing hoje e sentindo vontade de adicionar mais um `if`, a pergunta que vale a pena fazer não é *"essa regra está correta?"*. É *"se a gente adicionar isso, quem vai conseguir encontrar, explicar, medir e eventualmente remover?"*

A regra não é o custo. O sistema ao redor da regra é.
