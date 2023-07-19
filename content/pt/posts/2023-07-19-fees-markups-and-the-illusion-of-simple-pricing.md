---
title: "Fees, Markups e a Ilusão do Pricing Simples"
categories:
  - Architecture
  - Engineering
  - Pricing
date: 2023-07-19
tags:
  - pricing
  - markups
  - fees
  - product-engineering
  - monetizacao
  - motor-de-regras
description: "Por que um único markup nunca anda sozinho, e por que mudar um preço raramente é só mudar um número."
subtitle: "Por que mudar um preço raramente é só mudar um número."
---

Quando entrei em um time de pricing, achei que entendia pricing.

Tinha passado anos construindo sistemas distribuídos, trabalhando perto de times de produto e apoiando iniciativas de negócio. Pricing parecia simples em comparação com alguns dos desafios de plataforma que eu já tinha visto.

Então segui um único markup pelo sistema.

Ele cruzou múltiplos serviços. Dependia de acordos comerciais. Se comportava diferente dependendo do mercado. Interagia com fees existentes. Era medido por analistas, configurado por product managers, implementado por engenheiros e escrutinado por stakeholders de negócio.

Aquele foi o momento em que percebi que pricing não é um cálculo.

Pricing é um sistema.

## O erro que cometi nas primeiras semanas

Meu modelo mental se parecia com isto:

```text
preco_final = preco_base + ajuste
```

Simples. Elegante. Completamente errado.

A realidade era muito mais parecida com isto:

```text
preco_final =
    preco_base
  + fees
  + markups
  + ajustes de parceiro
  + promoções
  + add-ons
  + experimentos
  + comportamento específico de mercado
```

| O que eu esperava | Realidade |
| --- | --- |
| Um preço | Múltiplas decisões de pricing |
| Um dono | Múltiplos stakeholders |
| Problema técnico | Problema sociotécnico |
| Lógica estática | Experimentação contínua |
| Cálculo simples | Sistema distribuído de decisões |

A surpresa real não era a equação. Eram as pessoas que apareciam ao redor dela.

## Fees e markups não são a mesma coisa

Um dos primeiros conceitos que precisei entender foi a diferença entre fees e markups. Eles soam parecidos. Às vezes compartilham os mesmos caminhos de código. Não são a mesma coisa.

Uma fee normalmente é explícita. O cliente costuma vê-la no resumo da compra — booking fees, service fees, processing fees, operational fees. Uma fee não é só um mecanismo de receita. É também um mecanismo de confiança do cliente. No momento em que um recibo lê "taxa de serviço", o leitor para para julgar se aquilo é justo.

Um markup é diferente. Um markup modifica o preço subjacente do produto antes que o cliente o veja. O cliente raramente vê o markup em si; ele vê o preço que o markup produziu.

| Preço base | Markup | Preço final |
| --- | --- | --- |
| €100 | €5 | €105 |

Em sistemas de produção, markups dependem de um fan-in de variáveis. Cada variável é um ponto de entrada para um experimento futuro, uma exceção futura, um incidente futuro.

{{< plantuml title="De quantas variáveis um único markup realmente depende" >}}
@startuml
skinparam shadowing false
skinparam componentStyle rectangle

object Markup {
  mercado
  rota
  provedor
  moeda
  dispositivo
  antecedência
  segmento do cliente
  experimento
}
@enduml
{{< /plantuml >}}

Esse fan-in é o motivo pelo qual "mudar o markup" quase nunca significa "editar uma linha".

## Por que regras de pricing ficam bagunçadas

Todo sistema de pricing começa limpo.

Aí a realidade chega. Um mercado específico precisa de uma regra diferente. Um acordo com parceiro exige tratamento especial. Um experimento entra em produção e fica. Um regulador muda as restrições. Um segmento de cliente se comporta de forma inesperada. Cada um desses eventos deixa um depósito no código.

Uma entrada típica de regras acaba parecendo isto:

```yaml
country: DE
provider: train
lead_time: < 7 days
markup: 2.5%
```

Depois aparece outra exceção. Depois outro experimento. Depois outro acordo comercial. Três anos depois, o "arquivo" de regras virou um sistema de configuração por si só.

Isso não é má engenharia. É evolução de negócio expressa através de software.

## As quatro conversas que todo time de pricing precisa ter

As primeiras semanas me ensinaram que trabalho de pricing não é gargalado por código. É gargalado por alinhamento.

| Papel | Pergunta central |
| --- | --- |
| Product manager | Por que devemos mudar o pricing? |
| Analista | Como vamos medir sucesso? |
| Engenheiro | Como podemos implementar isso com segurança? |
| Stakeholder de negócio | Que resultado esperamos? |

Bons times de pricing aprendem a fazer essas conversas acontecerem continuamente, não uma vez por mudança. A mudança que pula uma conversa é a mudança que aparece como incidente duas semanas depois.

## Construir uma mudança de pricing com segurança

Quando essas quatro conversas ganham ritmo, uma mudança de pricing passa a parecer menos com um deploy e mais com um experimento:

{{< plantuml title="Uma mudança segura de pricing é um ciclo de feedback, não um deploy" >}}
@startuml
skinparam shadowing false
start
:Hipótese;
:Análise;
:Definição de regra;
:Implementação;
:Experimento;
:Observação;
:Decisão;
stop
@enduml
{{< /plantuml >}}

A forma importa. Cada passo existe para manter o próximo honesto. Pule "observação" e "decisão" vira chute. Pule "análise" e "hipótese" é só uma opinião. Mudanças de pricing afetam receita. Sistemas de receita merecem ciclos de feedback.

## O que eu gostaria de ter sabido no primeiro dia

Pricing não é matemática. Pricing é tomada de decisão.

Toda regra de pricing tem história. Todo número tem um dono. Toda mudança precisa de observabilidade. E sistemas de receita exigem humildade.

A mudança que de fato destravou o resto do trabalho não foi técnica. Foi de tom: parar de tratar pricing como um serviço de backend para ser otimizado e começar a tratá-lo como um produto com usuários — usuários internos, na maior parte, mas ainda assim usuários.

## Reflexão final

Quando parei de ver pricing como uma coleção de cálculos, outra percepção surgiu. Pricing estava se comportando menos como um serviço de backend e mais como um produto. O product manager, o analista, o time que conversa com parceiros, o time financeiro — todos eles estavam fazendo perguntas diferentes ao sistema, e todos esperavam respostas coerentes.

A pergunta que vale a pena fazer no primeiro dia não é *"como o preço é calculado aqui?"*. É *"quem decide que esse preço muda, e como saberíamos que funcionou?"*.

Responda isso, e o resto da arquitetura começa a se encaixar.
