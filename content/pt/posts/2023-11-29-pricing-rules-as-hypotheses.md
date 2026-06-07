---
title: "Toda Regra de Pricing É uma Hipótese"
categories:
  - Engineering
  - Experimentation
  - Pricing
  - Product
date: 2023-11-29
tags:
  - pricing
  - experimentacao
  - ab-testing
  - elasticidade-de-preco
  - monetizacao
  - product-discovery
description: "A coisa mais valiosa que a nossa plataforma de pricing produzia não eram preços. Era aprendizado."
subtitle: "Uma regra de pricing não é uma decisão. É uma previsão. E previsões podem estar erradas."
---

O Business Rules Engine nos deu a capacidade de mudar pricing com segurança.

Ele não respondia a pergunta com a qual mais nos importávamos.

*A mudança foi de fato boa?*

Por um tempo, tratávamos regras de pricing como decisões. Aumentar um markup. Ajustar uma fee. Introduzir uma nova condição. Subir. Seguir em frente.

Quanto mais tempo passávamos em pricing, mais percebíamos que esse jeito de pensar era incompleto.

Uma regra de pricing não é uma decisão.

Uma regra de pricing é uma hipótese.

Essa distinção parece sutil. Acabou mudando como pensávamos sobre pricing, experimentação, analytics e desenvolvimento de produto.

## A ilusão de certeza

Considere uma mudança simples de pricing.

> Aumentar a service fee de 5% para 6%.

À primeira vista, parece uma decisão. Mas escondida dentro daquela frase tem uma suposição:

> Acreditamos que aumentar a service fee de 5% para 6% vai aumentar a receita sem reduzir conversão de forma significativa.

Isso não é uma decisão. É uma previsão. E previsões podem estar erradas.

Uma das lições mais úteis que aprendi em pricing é que sistemas de receita estão cheios de suposições disfarçadas de certeza. Supomos que o cliente vai tolerar uma fee. Supomos que um markup não vai afetar a demanda. Supomos que um mercado se comporta de forma parecida com outro. Supomos que clientes percebem algumas mudanças e ignoram outras.

Suposições só viram conhecimento quando a gente testa.

## Paramos de discutir porcentagens

Conversas iniciais de pricing costumavam soar assim:

> Esse markup deveria ser 3% ou 4%?
>
> Devemos aumentar o teto da service fee?

Essas conversas estavam focadas em outputs. Com o tempo, começamos a fazer perguntas diferentes:

> O que estamos tentando aprender?
>
> Qual comportamento do cliente esperamos mudar?
>
> O que nos faria acreditar que essa ideia está errada?

A conversa saiu de configuração para descoberta. Essa mudança de mentalidade acabou sendo mais importante do que qualquer modelo de pricing que construímos depois.

## Por que o Business Rules Engine não bastava

O Business Rules Engine resolvia muitos problemas. Ele dava ownership. Dava explicabilidade. Dava uma forma de separar capacidades de pricing da implementação do motor de regras por baixo.

Mas ele não gerava aprendizado.

A BRE avaliava uma regra. Ela não dizia se a regra devia existir. Para isso, era preciso outra coisa. Era preciso experimentação.

Começamos a construir as capacidades ao redor para conseguir aprender com decisões de pricing — sistemas de atribuição, tracking de experimentos, coleta de dados de comportamento, pipelines analíticos.

Não porque queríamos mais infraestrutura. Porque queríamos respostas melhores.

## A/B testing e elasticidade de preço são problemas diferentes

Uma lição que me surpreendeu foi a frequência com que se usa *A/B testing* e *elasticidade de preço* como se fossem a mesma coisa.

Elas são relacionadas. Respondem perguntas diferentes.

| | A/B testing | Elasticidade de preço |
| --- | --- | --- |
| Começa com | Uma decisão | Uma curiosidade |
| Setup | Dois variantes (ex.: 5% vs 6%) | Vários pontos (0%, 3%, 6%, 9%, …) |
| Pergunta | Qual performa melhor? | Como o comportamento do cliente muda quando o preço muda? |
| Resultado | Escolher um vencedor | Aprender o formato da curva de resposta |
| Melhor para | Escolher | Entender |

Uma é sobre escolher. A outra é sobre entender. A distinção importa porque entender o comportamento do cliente costuma ser mais valioso do que escolher entre dois variantes.

## Paramos de testar vencedores e começamos a aprender curvas

Essa foi uma das maiores transições da nossa jornada de pricing.

Os nossos primeiros experimentos eram quase todos comparações: A versus B. Em algum momento, começamos a rodar experimentos desenhados para revelar a sensibilidade do cliente ao preço.

Em vez de perguntar *"qual variante vence?"*, perguntávamos *"em que ponto o comportamento do cliente começa a mudar?"*

Essa pergunta abriu a porta para uma classe completamente diferente de insights. Descobrimos que nem todos os clientes reagem a mudanças de pricing da mesma forma. Alguns grupos eram altamente sensíveis. Outros mal reagiam. Mudanças que pareciam perigosas se revelavam com impacto quase nenhum. Outras que pareciam inofensivas produziam mudanças significativas de comportamento.

Essas descobertas não viriam de um único A/B test. Elas exigiam experimentação desenhada para aprender, não para validar.

## O problema de atribuição em experimentos

Quando regras de pricing viram hipóteses, outro desafio aparece.

*Quem deveria ver qual versão?*

Todo experimento precisa de um mecanismo que atribua clientes de forma consistente:

{{< plantuml title="Sem atribuição consistente, resultado de experimento é ruído" >}}
@startuml
skinparam shadowing false
start
:Cliente;
:Atribuição;
:Variante de pricing;
:Resultado;
stop
@enduml
{{< /plantuml >}}

Sem atribuição confiável, experimentos ficam impossíveis de interpretar. Se clientes pulam aleatoriamente entre variantes, a medição vira ruído. Se as atribuições têm viés, os resultados enganam.

O desafio técnico de atribuição raramente é discutido fora dos times de experimentação, mas é uma das fundações que torna o aprendizado possível.

A regra em si é só metade do experimento. A estratégia de atribuição é a outra metade.

## Receita é uma métrica perigosa

Um dos erros mais fáceis em pricing é otimizar só por receita.

Receita importa. Mas receita raramente conta a história toda. Uma mudança de pricing pode aumentar receita ao mesmo tempo em que prejudica conversão. Pode aumentar receita ao mesmo tempo em que reduz satisfação do cliente. Pode melhorar um mercado e prejudicar outro. Pode criar ganhos de curto prazo e perdas de longo prazo.

É por isso que toda hipótese de pricing precisa de guardrails.

| Métrica primária | Guardrails típicos |
| --- | --- |
| Receita | Taxa de conversão |
| Receita de service fee | Taxa de finalização de compra |
| Margem | Satisfação do cliente |
| Attach rate | Taxa de cancelamento |

As decisões de pricing mais difíceis não são as em que uma métrica melhora. São as em que várias métricas se movem em direções diferentes.

## A parte mais difícil não era rodar os experimentos

A maior parte das pessoas imagina experimentação como um desafio técnico.

Na prática, rodar um experimento costumava ser a parte fácil. Entender os resultados era mais difícil.

Imagine dois variantes:

- **Variante A** aumenta receita um pouco e melhora conversão.
- **Variante B** aumenta receita significativamente, mas reduz conversão.

Qual ganha?

Essa não é uma pergunta de engenharia. É uma pergunta de negócio.

Experimentos não eliminam a tomada de decisão. Eles melhoram a qualidade da informação disponível para quem decide. O time ainda precisa decidir quais trade-offs importam.

## Os experimentos que mais nos ensinaram

Olhando para trás, os experimentos mais valiosos não foram os bem-sucedidos. Foram os que derrubaram nossas suposições.

Os que mostraram um mercado se comportando diferente do esperado. Os que revelaram segmentos de clientes que tínhamos ignorado. Os que demonstraram que uma ideia aparentemente óbvia estava, na verdade, errada.

Esses experimentos geraram o aprendizado mais valioso. E aprendizado compõe.

Uma mudança bem-sucedida de pricing cria valor uma vez. Uma lição sobre comportamento de cliente pode criar valor por anos.

## O que aprendi

A lição não era que clientes reagem a preço. Todo mundo já sabe disso.

A lição era que clientes diferentes reagem de forma diferente.

Quando entendemos isso, regras individuais de pricing pararam de parecer respostas. Começaram a parecer perguntas. Perguntas sobre comportamento do cliente. Perguntas sobre valor. Perguntas sobre disposição a pagar. Perguntas sobre trade-offs.

Esse enquadramento mudou também o trabalho do time. Não estávamos entregando mudanças de pricing. Estávamos rodando um ciclo de aprendizado:

{{< plantuml title="O time de pricing é dono de um ciclo de aprendizado, não de uma cadência de release" >}}
@startuml
skinparam shadowing false

state Hipótese
state Regra
state Atribuição
state Experimento
state Resultado
state Aprendizado

[*] --> Hipótese
Hipótese --> Regra
Regra --> Atribuição
Atribuição --> Experimento
Experimento --> Resultado
Resultado --> Aprendizado
Aprendizado --> Hipótese
@enduml
{{< /plantuml >}}

A coisa mais valiosa que a nossa plataforma de pricing produzia não eram preços.

Era aprendizado.

## Reflexão final

O motor de regras nos deu uma forma de expressar decisões. A experimentação nos deu uma forma de questioná-las. Juntos, criaram algo mais útil do que uma plataforma de pricing — um sistema de aprendizado.

O que a gente estava de fato aprendendo era que uma plataforma de pricing deixa de ser útil quando as pessoas que a operam param de ter curiosidade sobre o cliente por trás do preço. Ferramentas, regras, motores, dashboards — nada disso sobrevive a um time que decidiu que a resposta já é óbvia.

Tratar cada regra como uma hipótese era só uma forma de se recusar a ser esse time.
