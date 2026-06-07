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
description: "O objetivo nunca foi achar o maior preço possível. Era entender como o comportamento do cliente muda quando o preço muda."
subtitle: "Sensibilidade a preço não é rótulo. É relação."
---

Por alguns anos, trabalhei numa plataforma de pricing — a parte do sistema que decide o que cobrar de um cliente, e quando. A maior parte do que tornou aquilo uma plataforma de verdade aconteceu fora dos holofotes: tiramos regra do código pra um motor de regras de negócio, paramos de subir mudança de pricing no escuro e começamos a tratar como experimento, e paramos de fingir que "cliente médio" era um conceito útil.

Cada uma dessas mudanças respondia uma pergunta. Cada uma também escancarava a próxima.

Quando a gente aceitou que cliente diferente se comportava diferente, o desdobramento óbvio veio na hora. *Quão* diferente? E, mais importante, *a partir de que ponto uma mudança de pricing começa a afetar o comportamento do cliente?*

Se cliente valoriza coisas diferentes — conveniência, confiança, flexibilidade, custo — então também não reage a preço da mesma forma. Cada grupo tem o próprio limiar, a própria resposta, a própria curva.

Essa pergunta levou a gente pra uma das áreas mais interessantes de pricing.

Sensibilidade a preço.

## O que sensibilidade a preço significa, no fundo

Quando as pessoas ouvem o termo pela primeira vez, costumam imaginar duas categorias:

> Sensível a preço. Insensível a preço.

A realidade raramente é tão simples.

Sensibilidade a preço não é rótulo. É relação. Uma relação entre uma mudança de preço e uma mudança de comportamento do cliente.

Pra alguns grupos de cliente, um aumento pequeno de preço produz uma queda significativa de conversão. Pra outros, o mesmo aumento tem impacto quase imperceptível. A sacada importante é que sensibilidade vive num espectro.

O objetivo não é classificar cliente. É entender o formato da resposta dele.

## Por que A/B test não bastava

Nossos primeiros experimentos costumavam comparar duas alternativas.

> Variante A = 5%. Variante B = 6%. Qual performa melhor?

Útil. Mas só diz qual opção venceu. Diz muito pouco sobre comportamento do cliente.

Em algum momento, a gente passou a fazer perguntas diferentes. Em vez de comparar dois valores, introduziu vários níveis — 0%, 3%, 6%, 9%, 12% — e reformulou a pergunta:

> Como o comportamento do cliente evolui quando o preço muda?

A mudança era sutil. Mudou completamente o que dava pra aprender.

## A gente parou de procurar vencedor

Uma das maiores mudanças na nossa mentalidade de experimentação foi sair da ideia de que todo experimento precisava de um vencedor.

Experimento antigo parecia competição. Controle vs variante. No fim, a gente esperava veredito claro. Mantém. Remove. Segue em frente.

Experimento de sensibilidade a preço era diferente. O objetivo não era escolher vencedor. Era entender curva.

Um resultado podia dizer pra gente:

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

Esse padrão vale muito mais do que qualquer resultado de experimento isolado.

## Cliente diferente, curva diferente

Essa foi uma das descobertas mais importantes.

A mesma mudança de pricing podia produzir resultados completamente diferentes dependendo do grupo de cliente. Dois grupos simplificados deixam isso claro:

| Grupo | Reação a um aumento de preço |
| --- | --- |
| Grupo A | Conversão cai rapidinho |
| Grupo B | Conversão mal se altera |

Se a gente só olha pra média, perde o que de fato tá acontecendo. Um grupo pode ser extremamente sensível. O outro pode mal perceber. O resultado médio não descreve nenhum dos dois.

Mais um lembrete de que comportamento do cliente raramente cabe direitinho em uma métrica só. Os insights mais valiosos costumam aparecer quando a gente olha por baixo da média.

## Receita é só metade da equação

Um erro comum em discussão de pricing é focar só em receita.

Receita importa. Mas é só um lado da história. Uma mudança de pricing pode aumentar o valor ganho por compra ao mesmo tempo em que reduz o número de compras.

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

O desafio é entender onde essas curvas se cruzam. Baixo demais e valor fica na mesa. Alto demais e o comportamento do cliente muda de um jeito que machuca o negócio.

Sensibilidade a preço ajuda a identificar essa relação. Não perfeitamente. Mas muito mais precisamente do que a intuição sozinha.

## A surpresa era a parte mais valiosa

Os experimentos que ficaram comigo raramente foram os que confirmavam nossas suposições. Foram os que desafiavam.

O grupo de cliente que a gente esperava ser muito sensível, às vezes não era. O grupo que a gente achava que ia tolerar preço maior, às vezes reagia forte. Mudança que parecia arriscada, às vezes não tinha efeito mensurável. Mudança que parecia insignificante, às vezes gerava mudança importante de comportamento.

Esses momentos eram valiosos porque revelavam buraco nos nossos modelos mentais.

O objetivo de experimentar nunca foi provar que a gente estava certo. Era descobrir onde a gente estava errado.

## Sensibilidade é, no fundo, sobre valor

Com o tempo, parei de pensar em sensibilidade a preço como conceito de pricing. Comecei a pensar como conceito de valor.

Cliente não reage a preço isolado. Reage a preço em relação ao valor que percebe.

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

É por isso que dois clientes podem ver a mesma oferta e se comportar diferente. Não estão reagindo ao mesmo preço. Estão reagindo a percepções diferentes de valor.

Essa percepção conectou várias das lições de trabalho anterior. Regra. Experimento. Segmentação. Tudo eram tentativas de entender melhor como cliente percebe valor.

## O que aprendi

O objetivo nunca foi achar o maior preço possível. Era entender como o comportamento do cliente muda quando o preço muda.

Sensibilidade a preço deu pra gente uma linguagem pra essa relação. Ajudou a sair de opinião. Ajudou a sair de média. E ajudou a entender que comportamento do cliente costuma ser mais nuançado do que as primeiras suposições sugerem.

O output mais valioso não era um número. Era um entendimento melhor do comportamento do cliente.

## Reflexão final

Quanto mais a gente ia aprendendo sobre sensibilidade a preço, mais visível ficava a pergunta por baixo.

Se grupo diferente de cliente responde a preço de forma diferente — e se essas respostas descrevem um formato, não um ponto só — então o trabalho de pricing não é escolher um valor. É escolher um valor *pra um contexto*, e ser honesto sobre a curva por baixo dele.

As melhores decisões de pricing que a gente entregou não vieram das curvas mais sofisticadas. Vieram das mais honestas. A gente desenhava pequeno. Desenhava com frequência. Sabia a qual segmento cada curva se referia. E topava apagar uma curva que tinha deixado de explicar alguma coisa.

Esse hábito, mais do que qualquer número específico, era o ativo.
