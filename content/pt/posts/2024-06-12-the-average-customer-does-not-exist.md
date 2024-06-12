---
title: "O Cliente Médio Não Existe"
categories:
  - Engineering
  - Experimentation
  - Pricing
  - Product
date: 2024-06-12
tags:
  - pricing
  - segmentacao
  - experimentacao
  - product-discovery
  - elasticidade-de-preco
  - monetizacao
description: "Por que personas nos ajudaram a entender clientes, mas dimensões de comportamento nos ajudaram a entender pricing."
subtitle: "O cliente médio não existe. Otimizar por ele é otimizar por ninguém."
---

Por meses, rodamos experimentos de pricing procurando uma resposta única.

*Qual é o preço certo? Qual é o markup certo? Qual é a fee certa?*

Cada experimento parecia nos empurrar para o mesmo destino: encontrar o valor ótimo e aplicar em todo lugar.

Os dados continuavam discordando.

Dois clientes olhavam para a mesma jornada, a mesma rota, o mesmo provedor, o mesmo horário, o mesmo preço — e tomavam decisões completamente diferentes.

No começo, supusemos que precisávamos de mais dados. Eventualmente, percebemos que precisávamos de um modelo melhor de cliente.

A maior lição era surpreendentemente simples.

O cliente médio não existe.

## O perigo das médias

A maior parte das conversas sobre pricing começa com médias. Valor médio de compra. Conversão média. Receita média por busca. Comportamento médio do cliente.

Médias são úteis. Elas ajudam a resumir grandes quantidades de informação. O problema é que médias frequentemente descrevem ninguém.

Imagine um exemplo simples.

| Grupo de clientes A | Grupo de clientes B |
| --- | --- |
| Muito sensível a preço | Mal reage a preço |

Se você tirar a média dos dois grupos, pode concluir que clientes são moderadamente sensíveis a preço. Soa razoável. Está errado. A média esconde o comportamento que de fato importa. Um grupo precisa de uma estratégia de pricing completamente diferente da do outro.

Esse foi um dos primeiros sinais de que nossos experimentos estavam nos ensinando algo mais profundo do que se uma regra de pricing vencia ou perdia. Eles estavam revelando diferenças em como clientes percebiam valor.

## Personas ajudaram a gente a pensar

Como muitos times, frequentemente usávamos personas para falar de clientes.

Personas são úteis. Elas criam linguagem compartilhada. Ajudam product managers, analistas, designers e engenheiros a falarem de necessidades de clientes sem cair direto nos dados.

Um time pode discutir clientes que priorizam preço. Outros que priorizam conveniência. Outros que valorizam flexibilidade. Outros que se importam profundamente com confiança e informação.

Essas conversas são valiosas. Elas ajudam humanos a raciocinar sobre comportamento.

Mas personas nunca foram precisas o suficiente para guiar decisões de pricing. Um motor de pricing não consegue avaliar uma persona. Ele não consegue receber:

```json
{
  "persona": "Explorer"
}
```

e decidir o que fazer.

Sistemas de pricing precisam de algo mais concreto. Precisam de sinais.

## Personas contam histórias. Sinais guiam decisões.

Essa distinção foi ficando mais importante conforme nossas capacidades de experimentação amadureciam.

Humanos raciocinam por narrativas. Sistemas raciocinam por fatos observáveis.

O motor de pricing nunca viu arquétipos de cliente. Ele via contexto:

```json
{
  "trip_value": 250,
  "booking_context": "high_urgency",
  "customer_activity": "frequent",
  "journey_type": "round_trip",
  "market": "X"
}
```

Não porque aqueles sinais específicos fossem universalmente corretos, mas porque sistemas de pricing precisam de dimensões que possam ser medidas de forma consistente.

O motor raciocina por sinais. Humanos raciocinam por personas. Os dois são úteis. Eles resolvem problemas diferentes.

## O mundo real é feito de dimensões

Uma percepção mudou como eu pensava em segmentação.

Clientes não pertencem a um único segmento. Eles existem ao longo de muitas dimensões ao mesmo tempo. Um único cliente pode ser altamente sensível a preço, viajar com frequência, preferir conveniência a flexibilidade, estar comprando sob pressão de tempo e estar adquirindo uma viagem de valor mais alto, tudo ao mesmo tempo.

{{< plantuml title="Um cliente existe em várias dimensões de comportamento ao mesmo tempo" >}}
@startuml
skinparam shadowing false
skinparam componentStyle rectangle

object Cliente {
  sensibilidade a preço
  frequência de viagem
  preferência por flexibilidade
  pressão de tempo
  valor da viagem
  mercado
  tipo de jornada
  dispositivo
}
@enduml
{{< /plantuml >}}

Nenhuma dessas características define o cliente por completo. Juntas, elas começam a descrever comportamento.

Essa distinção importa porque sistemas de pricing raramente operam em uma dimensão por vez. A complexidade emerge das combinações.

## De cinco personas para milhares de possibilidades

É aqui que muitas discussões sobre segmentação ficam enganosas.

Um punhado de personas pode bastar para conversas de estratégia. Não basta para decisões de pricing.

Cinco personas podem ajudar um time de produto a entender motivações do cliente. Uma plataforma de pricing precisa raciocinar sobre muitas dimensões, cada uma com vários valores possíveis.

{{< plantuml title="Dimensões de comportamento compõem rápido em decisões de pricing" >}}
@startuml
skinparam shadowing false
start
:Dimensões de comportamento;
:Combinações;
:Segmentos;
:Decisões de pricing;
stop
@enduml
{{< /plantuml >}}

O número de combinações significativas cresce rápido. Não porque o time queira complexidade. Porque o comportamento do cliente é complexo.

O desafio de pricing não é identificar cinco grupos. O desafio é descobrir quais combinações de características levam a respostas diferentes a valor e a preço.

## Segmentos viraram hipóteses também

Uma lição inesperada foi que a própria segmentação virou uma hipótese.

No começo, era tentador tratar segmentos como fato:

> Clientes comprando sob pressão de tempo se comportam de forma diferente.

Soa razoável. Mas ainda é uma hipótese. Precisa de evidência.

A mesma mentalidade de aprendizado que aplicávamos a regras de pricing acabou se aplicando à segmentação. Cada segmento virou uma pergunta:

- Esses clientes de fato se comportam diferente?
- Essa distinção importa?
- Ela justifica uma estratégia diferente?
- A gente consegue medir o impacto?

O objetivo nunca foi criar mais segmentos. O objetivo foi descobrir quais distinções eram significativas.

## Preço era só parte da história

Um erro que muitos engenheiros cometem ao entrar em pricing é supor que o comportamento do cliente é, na maior parte, sobre preço.

Preço importa. Mas clientes raramente otimizam por preço sozinho. Eles otimizam por valor. E valor significa coisas diferentes para pessoas diferentes.

- Para alguns clientes, **valor ≈ menor custo**.
- Para outros, **valor ≈ confiança**.
- Para outros, **valor ≈ conveniência**.
- Para outros, **valor ≈ flexibilidade**.

Quanto mais experimentos rodávamos, mais óbvio isso ficava. A gente não estava simplesmente medindo disposição a pagar. Estávamos aprendendo como clientes diferentes percebem valor.

Esse é um problema muito mais interessante.

## O que aprendi

A maior mudança não foi aprender que clientes se comportam diferente. A maioria das pessoas já acredita nisso.

A mudança maior foi perceber que essas diferenças podem ser observadas, medidas, testadas e incorporadas em como decisões de pricing são tomadas.

Personas nos ajudaram a entender clientes. Dimensões nos ajudaram a modelar clientes. Sistemas de pricing nos ajudaram a agir sobre esses modelos.

O cliente médio nunca existiu. E, quando paramos de otimizar por médias, começamos a aprender muito mais sobre as pessoas por trás dos números.

## Reflexão final

O Business Rules Engine nos ensinou a expressar decisões de pricing. A experimentação nos ensinou a questioná-las. A segmentação nos ensinou que nem todo cliente experimenta valor da mesma forma.

Se você está tentado a subir uma mudança de pricing com base no que o cliente *médio* quer, a pergunta que vale a pena fazer não é *"qual valor a gente deveria escolher?"*. É *"quem, especificamente, a gente está optando por não atender bem ao tratar todo mundo igual?"*

A média é uma história sobre todos eles. Pricing tem que ser uma decisão sobre cada um deles.
