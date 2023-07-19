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
series:
  - lessons-from-a-pricing-platform
series_order: 2
description: "Por que um único markup nunca anda sozinho, e por que mudar um preço raramente é só mudar um número."
subtitle: "Por que mudar um preço raramente é só mudar um número."
---

Quando entrei num time de pricing, achei que entendia pricing.

Tinha passado anos construindo sistema distribuído, trabalhando perto de time de produto, dando suporte a iniciativa de negócio. Pricing parecia tranquilo perto de alguns desafios de plataforma que eu já tinha visto.

Aí segui um markup só pelo sistema.

Ele passava por vários serviços. Dependia de acordo comercial. Se comportava diferente dependendo do mercado. Esbarrava com fee que já existia. Era medido por analista, configurado por product manager, implementado por engenheiro e questionado por stakeholder de negócio.

Foi naquele momento que caiu a ficha: pricing não é um cálculo.

Pricing é um sistema.

## O erro que cometi nas primeiras semanas

Meu modelo mental era mais ou menos esse:

```text
preco_final = preco_base + ajuste
```

Simples. Elegante. Errado do início ao fim.

A realidade era bem mais parecida com isso aqui:

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
| Um preço | Várias decisões de pricing |
| Um dono | Vários stakeholders |
| Problema técnico | Problema sociotécnico |
| Lógica estática | Experimentação contínua |
| Cálculo simples | Sistema distribuído de decisão |

A surpresa de verdade não era a equação. Eram as pessoas que apareciam em volta dela.

## Fee e markup não são a mesma coisa

Um dos primeiros conceitos que precisei entender foi a diferença entre fee e markup. Soam parecido. Às vezes compartilham caminho de código. Não são a mesma coisa.

Uma fee normalmente é explícita. O cliente costuma ver ela no resumo da compra — booking fee, service fee, processing fee, operational fee. Fee não é só mecanismo de receita. É também mecanismo de confiança. No instante em que um recibo mostra "taxa de serviço", o leitor para um segundo pra julgar se aquilo é justo.

Markup é outra história. Ele modifica o preço do produto antes do cliente ver. O cliente raramente vê o markup em si; vê o preço que o markup produziu.

| Preço base | Markup | Preço final |
| --- | --- | --- |
| €100 | €5 | €105 |

Em sistema de produção, markup depende de um monte de variável. Cada uma é uma porta de entrada pra um experimento futuro, uma exceção futura, um incidente futuro.

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

É por causa desse leque que "mudar o markup" quase nunca quer dizer "editar uma linha".

## Por que regra de pricing fica bagunçada

Todo sistema de pricing começa limpo.

Aí a realidade chega. Um mercado específico precisa de uma regra diferente. Um acordo com parceiro pede tratamento especial. Um experimento entra em produção e fica. Um regulador muda a restrição. Um segmento de cliente se comporta de um jeito que ninguém esperava. Cada um desses eventos deixa um depósito no código.

Uma entrada de regra acaba ficando mais ou menos assim:

```yaml
country: DE
provider: train
lead_time: < 7 days
markup: 2.5%
```

Aí aparece outra exceção. Depois mais um experimento. Depois mais um acordo comercial. Três anos depois, o "arquivo" de regras virou um sistema de configuração por conta própria.

Não é má engenharia. É evolução de negócio expressa em forma de código.

## As quatro conversas que a gente vivia precisando ter

As primeiras semanas me ensinaram que trabalho de pricing não trava por código. Trava por alinhamento.

| Papel | Pergunta central |
| --- | --- |
| Product manager | Por que a gente devia mudar o pricing? |
| Analista | Como vamos medir sucesso? |
| Engenheiro | Como dá pra implementar isso com segurança? |
| Stakeholder de negócio | Que resultado a gente espera? |

A gente aprendeu a fazer essas conversas acontecerem o tempo todo, não uma vez por mudança. A mudança que pulava uma delas era a que aparecia como incidente duas semanas depois.

## Construir uma mudança de pricing com segurança

Quando essas quatro conversas pegam ritmo, uma mudança de pricing começa a parecer menos com deploy e mais com experimento:

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

A forma importa. Cada passo existe pra manter o próximo honesto. Pula "observação" e "decisão" vira chute. Pula "análise" e "hipótese" vira opinião. Mudança de pricing mexe com receita. Sistema de receita merece ciclo de feedback.

## O que eu queria ter sabido no primeiro dia

Pricing não é matemática. Pricing é tomada de decisão.

Toda regra de pricing tem história. Todo número tem um dono. Toda mudança precisa de observabilidade. E sistema de receita exige humildade.

A mudança que destravou o resto do trabalho não foi técnica. Foi de tom: parar de tratar pricing como um serviço de backend pra ser otimizado e começar a tratar como produto, com usuário — usuário interno, na maior parte, mas ainda assim usuário.

## Reflexão final

Quando parei de ver pricing como uma coleção de cálculos, caiu outra ficha. Pricing estava se comportando menos como serviço de backend e mais como produto. O product manager, o analista, o time que falava com parceiro, o financeiro — todos estavam fazendo perguntas diferentes pro sistema, e todos esperavam resposta coerente.

A pergunta que vale a pena fazer no primeiro dia não é *"como o preço é calculado aqui?"*. É *"quem decide que esse preço muda, e como a gente saberia que funcionou?"*.

Responde isso, e o resto da arquitetura começa a se encaixar.
