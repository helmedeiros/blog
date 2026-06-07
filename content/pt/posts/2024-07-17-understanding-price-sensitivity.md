---
title: "Entendendo Sensibilidade a Preço"
categories:
  - Engineering
  - Experimentation
  - Pricing
  - Product
date: 2024-07-17
tags:
  - pricing
  - elasticidade-de-preco
  - experimentacao
  - monetizacao
  - comportamento-do-cliente
  - product-discovery
description: "O objetivo nunca foi encontrar o maior preço possível. O objetivo era entender como o comportamento do cliente muda quando o preço muda."
subtitle: "Sensibilidade a preço não é um rótulo. É uma relação."
---

Por alguns anos, trabalhei em uma plataforma de pricing — a parte do sistema que decide o que cobrar de um cliente, e quando. A maior parte do que tornou aquilo uma plataforma de verdade aconteceu fora dos holofotes: tiramos regras do código para um motor de regras de negócio, paramos de subir mudanças de pricing no escuro e começamos a tratá-las como experimentos, e paramos de fingir que "cliente médio" era um conceito útil.

Cada uma dessas mudanças respondia a uma pergunta. Cada uma delas também escancarava a próxima.

Quando aceitamos que clientes diferentes se comportavam de forma diferente, o desdobramento óbvio era inevitável. *Quão* diferente? E, mais importante, *a partir de que ponto uma mudança de pricing começa a afetar o comportamento do cliente?*

Se clientes valorizam coisas diferentes — conveniência, confiança, flexibilidade, custo — então eles também não reagem a preço da mesma forma. Cada grupo tem o próprio limiar, a própria resposta, a própria curva.

Essa pergunta nos levou para uma das áreas mais interessantes de pricing.

Sensibilidade a preço.

## O que sensibilidade a preço de fato significa

Quando as pessoas ouvem o termo pela primeira vez, costumam imaginar duas categorias:

> Sensível a preço. Insensível a preço.

A realidade raramente é tão simples.

Sensibilidade a preço não é um rótulo. É uma relação. Uma relação entre uma mudança de preço e uma mudança de comportamento do cliente.

Para alguns grupos de clientes, um pequeno aumento de preço produz uma queda significativa de conversão. Para outros, o mesmo aumento tem impacto quase imperceptível. A percepção importante é que sensibilidade existe em um espectro.

O objetivo não é classificar clientes. O objetivo é entender o formato da resposta deles.

## Por que A/B tests não bastavam

Nossos primeiros experimentos costumavam comparar duas alternativas.

> Variante A = 5%. Variante B = 6%. Qual performa melhor?

Isso é útil. Mas só nos diz qual opção venceu. Diz muito pouco sobre comportamento do cliente.

Em algum momento, começamos a fazer perguntas diferentes. Em vez de comparar dois valores, introduzimos múltiplos níveis — 0%, 3%, 6%, 9%, 12% — e reformulamos a pergunta:

> Como o comportamento do cliente evolui quando o preço muda?

Essa mudança era sutil. Ela mudou completamente o que conseguíamos aprender.

## Paramos de procurar vencedores

Uma das maiores mudanças na nossa mentalidade de experimentação foi sair da ideia de que todo experimento precisava de um vencedor.

Experimentos antigos pareciam competições. Controle vs variante. No fim, esperávamos um veredito claro. Mantém. Remove. Segue em frente.

Experimentos de sensibilidade a preço eram diferentes. O objetivo não era escolher um vencedor. Era entender uma curva.

Um resultado podia nos dizer:

{{< plantuml title="Uma curva de sensibilidade: a resposta é o padrão, não nenhum valor individual" >}}
@startuml
skinparam shadowing false

object PriceChange0 as " 0%  "
object PriceChange3 as " 3%  "
object PriceChange6 as " 6%  "
object PriceChange9 as " 9%  "
object PriceChange12 as " 12% "

object Impact0 as "Sem impacto"
object Impact3 as "Sem impacto"
object Impact6 as "Impacto pequeno"
object Impact9 as "Impacto significativo"
object Impact12 as "Impacto severo"

PriceChange0 --> Impact0
PriceChange3 --> Impact3
PriceChange6 --> Impact6
PriceChange9 --> Impact9
PriceChange12 --> Impact12
@enduml
{{< /plantuml >}}

Nenhum valor individual é a resposta. A resposta é o padrão.

Esse padrão é muito mais valioso do que qualquer resultado de um experimento isolado.

## Clientes diferentes, curvas diferentes

Essa foi uma das descobertas mais importantes.

A mesma mudança de pricing podia produzir resultados completamente diferentes dependendo do grupo de clientes. Dois grupos simplificados deixam isso claro:

| Grupo | Reação a um aumento de preço |
| --- | --- |
| Grupo A | Conversão cai rapidamente |
| Grupo B | Conversão mal se altera |

Se a gente só olha para a média, perde o que de fato está acontecendo. Um grupo pode ser extremamente sensível. O outro pode mal perceber. O resultado médio não descreve nenhum dos dois.

Mais um lembrete de que o comportamento do cliente raramente cabe direitinho em uma única métrica. Os insights mais valiosos costumam aparecer quando a gente olha por baixo da média.

## Receita é só metade da equação

Um erro comum em discussões de pricing é focar exclusivamente em receita.

Receita importa. Mas receita é só um lado da história. Uma mudança de pricing pode aumentar o valor ganho por compra ao mesmo tempo em que reduz o número de compras.

Isso cria um equilíbrio:

{{< plantuml title="O trade-off em que uma mudança de pricing esbarra direto" >}}
@startuml
skinparam shadowing false
start
:Preço mais alto;
:Receita maior por compra;
:Demanda potencialmente menor;
stop
@enduml
{{< /plantuml >}}

O desafio é entender onde essas curvas se cruzam. Baixo demais e valor fica na mesa. Alto demais e o comportamento do cliente muda de forma que prejudica o negócio.

Sensibilidade a preço ajuda a identificar essa relação. Não perfeitamente. Mas muito mais precisamente do que a intuição sozinha.

## As surpresas foram a parte mais valiosa

Os experimentos que ficaram comigo raramente foram os que confirmavam nossas suposições. Foram os que as desafiavam.

O grupo de clientes que esperávamos ser muito sensível às vezes não era. O grupo que achávamos que toleraria preços maiores às vezes reagia fortemente. Mudanças que pareciam arriscadas às vezes não produziam efeito mensurável. Mudanças que pareciam insignificantes às vezes geravam mudanças importantes de comportamento.

Esses momentos eram valiosos porque revelavam lacunas nos nossos modelos mentais.

O objetivo de experimentar nunca foi provar que estávamos certos. Era descobrir onde estávamos errados.

## Sensibilidade é, no fundo, sobre valor

Com o tempo, parei de pensar em sensibilidade a preço como um conceito de pricing. Comecei a pensar nela como um conceito de valor.

Clientes não reagem a preços isolados. Eles reagem a preços relativos ao valor que percebem.

{{< plantuml title="Sensibilidade é a distância entre preço e valor percebido" >}}
@startuml
skinparam shadowing false
start
:Valor percebido;
:Disposição a pagar;
:Decisão do cliente;
stop
@enduml
{{< /plantuml >}}

É por isso que dois clientes podem ver a mesma oferta e se comportar de forma diferente. Eles não estão reagindo ao mesmo preço. Estão reagindo a percepções diferentes de valor.

Essa percepção conectou muitas das lições de trabalhos anteriores. Regras. Experimentos. Segmentação. Todas eram tentativas de entender melhor como clientes percebem valor.

## O que aprendi

O objetivo nunca foi encontrar o maior preço possível. O objetivo era entender como o comportamento do cliente muda quando o preço muda.

Sensibilidade a preço nos deu uma linguagem para essa relação. Nos ajudou a sair de opiniões. Nos ajudou a sair de médias. E nos ajudou a entender que o comportamento do cliente costuma ser mais nuançado do que as primeiras suposições sugerem.

O output mais valioso não era um número. Era um entendimento melhor do comportamento do cliente.

## Reflexão final

Quanto mais aprendíamos sobre sensibilidade a preço, mais visível ficava a pergunta por baixo.

Se grupos diferentes de clientes respondem a preço de forma diferente — e se essas respostas descrevem um formato, não um único ponto — então o trabalho de pricing não é escolher um valor. É escolher um valor *para um contexto*, e ser honesto sobre a curva por baixo dele.

As melhores decisões de pricing que entregamos não vieram das curvas mais sofisticadas. Vieram das mais honestas. Desenhávamos pequeno. Desenhávamos com frequência. Sabíamos a qual segmento cada curva se referia. E topávamos apagar uma curva que tinha deixado de explicar alguma coisa.

Esse hábito, mais do que qualquer número específico, era o ativo.
