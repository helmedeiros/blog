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
series:
  - lessons-from-a-pricing-platform
series_order: 7
description: "Por que persona ajudou a gente a entender cliente, mas dimensão de comportamento ajudou a entender pricing."
subtitle: "O cliente médio não existe. Otimizar por ele é otimizar por ninguém."
---

Por meses, a gente rodou experimento de pricing procurando uma resposta única.

*Qual é o preço certo? Qual é o markup certo? Qual é a fee certa?*

Cada experimento parecia empurrar a gente pro mesmo destino: encontrar o valor ótimo e aplicar em todo canto.

O dado vivia discordando.

Dois clientes olhavam pra mesma jornada, a mesma rota, o mesmo provedor, o mesmo horário, o mesmo preço — e tomavam decisão completamente diferente.

No começo, a gente supôs que precisava de mais dado. Com o tempo, caiu a ficha de que o que faltava era um modelo melhor de cliente.

A maior lição era surpreendentemente simples.

O cliente médio não existe.

## O perigo das médias

A maior parte das conversas sobre pricing começa com média. Valor médio de compra. Conversão média. Receita média por busca. Comportamento médio do cliente.

Média é útil. Ajuda a resumir um monte de informação. O problema é que média costuma não descrever ninguém.

Imagine um exemplo simples.

| Grupo de clientes A | Grupo de clientes B |
| --- | --- |
| Muito sensível a preço | Mal reage a preço |

Se tirar a média dos dois, dá pra concluir que cliente é moderadamente sensível a preço. Soa razoável. Tá errado. A média esconde o comportamento que de fato importa. Um grupo precisa de uma estratégia de pricing completamente diferente da do outro.

Esse foi um dos primeiros sinais de que nossos experimentos estavam ensinando algo mais profundo do que se uma regra de pricing vencia ou perdia. Estavam revelando diferença em como cliente percebia valor.

## Persona ajudou a gente a pensar

A gente costumava usar persona pra falar de cliente.

Persona é útil. Cria linguagem compartilhada. Ajuda product manager, analista, designer e engenheiro a falar de necessidade do cliente sem cair direto no dado.

Um time pode discutir cliente que prioriza preço. Outro que prioriza conveniência. Outro que valoriza flexibilidade. Outro que se importa profundamente com confiança e informação.

Essas conversas são valiosas. Ajudam humano a raciocinar sobre comportamento.

Mas persona nunca foi precisa o suficiente pra guiar decisão de pricing. Um motor de pricing não consegue avaliar persona. Não dá pra receber:

```json
{
  "persona": "Explorer"
}
```

e decidir o que fazer.

Sistema de pricing precisa de algo mais concreto. Precisa de sinal.

## Persona conta história. Sinal guia decisão.

Essa distinção foi ficando mais importante à medida que nossa capacidade de experimentação ia amadurecendo.

Humano raciocina por narrativa. Sistema raciocina por fato observável.

O motor de pricing nunca viu arquétipo de cliente. Via contexto:

```json
{
  "trip_value": 250,
  "booking_context": "high_urgency",
  "customer_activity": "frequent",
  "journey_type": "round_trip",
  "market": "X"
}
```

Não porque aqueles sinais específicos fossem universalmente corretos, mas porque sistema de pricing precisa de dimensão que dá pra medir de forma consistente.

O motor raciocina por sinal. Humano raciocina por persona. Os dois são úteis. Resolvem problemas diferentes.

## O mundo real é feito de dimensão

Uma percepção mudou como eu pensava em segmentação.

Cliente não pertence a um segmento só. Ele existe ao longo de várias dimensões ao mesmo tempo. Um cliente pode ser muito sensível a preço, viajar com frequência, preferir conveniência a flexibilidade, estar comprando sob pressão de tempo e estar comprando uma viagem de valor mais alto, tudo de uma vez.

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

Essa distinção importa porque sistema de pricing raramente opera em uma dimensão por vez. A complexidade nasce da combinação.

## De cinco personas pra milhares de possibilidades

É aqui que muita conversa sobre segmentação fica enganosa.

Um punhado de personas pode bastar pra conversa de estratégia. Não basta pra decisão de pricing.

Cinco personas podem ajudar um time de produto a entender motivação de cliente. Uma plataforma de pricing precisa raciocinar sobre várias dimensões, cada uma com vários valores possíveis.

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

O número de combinações que importam cresce rápido. Não porque o time queira complexidade. Porque comportamento de cliente é complexo.

O desafio de pricing não é identificar cinco grupos. É descobrir quais combinações de características levam a respostas diferentes a valor e a preço.

## Segmento virou hipótese também

Uma lição inesperada foi que a própria segmentação virou hipótese.

No começo, era tentador tratar segmento como fato:

> Cliente que compra sob pressão de tempo se comporta diferente.

Soa razoável. Mas ainda é hipótese. Precisa de evidência.

A mesma mentalidade de aprendizado que a gente aplicava a regra de pricing acabou se aplicando à segmentação. Cada segmento virou pergunta:

- Esses clientes de fato se comportam diferente?
- Essa distinção importa?
- Ela justifica uma estratégia diferente?
- A gente consegue medir o impacto?

O objetivo nunca foi criar mais segmento. Foi descobrir quais distinções valiam a pena.

## Preço era só parte da história

Um erro que muito engenheiro comete ao entrar em pricing é supor que comportamento do cliente é, na maior parte, sobre preço.

Preço importa. Mas cliente raramente otimiza por preço sozinho. Otimiza por valor. E valor significa coisa diferente pra pessoa diferente.

- Pra alguns clientes, **valor ≈ menor custo**.
- Pra outros, **valor ≈ confiança**.
- Pra outros, **valor ≈ conveniência**.
- Pra outros, **valor ≈ flexibilidade**.

Quanto mais experimento a gente rodava, mais óbvio isso ficava. A gente não estava simplesmente medindo disposição a pagar. Estava aprendendo como cliente diferente percebe valor.

É um problema muito mais interessante.

## O que aprendi

A maior mudança não foi aprender que cliente se comporta diferente. A maioria das pessoas já acredita nisso.

A mudança maior foi perceber que essas diferenças podiam ser observadas, medidas, testadas e incorporadas em como a decisão de pricing era tomada.

Persona ajudou a gente a entender cliente. Dimensão ajudou a modelar cliente. Sistema de pricing ajudou a agir em cima desses modelos.

O cliente médio nunca existiu. E, quando a gente parou de otimizar por média, começou a aprender muito mais sobre as pessoas por trás dos números.

## Reflexão final

O Business Rules Engine ensinou a gente a expressar decisão de pricing. A experimentação ensinou a questionar essa decisão. A segmentação ensinou que nem todo cliente experimenta valor da mesma forma.

Eu lembro do momento em que o time parou de chamar aquilo de segmentação e começou a chamar de "servir pessoas diferentes". A mudança de vocabulário parecia cosmética. Não era. Quando a gente nomeou quem estava escolhendo *não* atender bem ao tratar todo mundo igual, o cliente médio não voltou mais. Todo gráfico que a gente desenhou depois tinha duas ou três linhas, porque todo gráfico em que a gente acreditava tinha duas ou três linhas.

A média é um número que um sistema consegue produzir. Um cliente, não.
