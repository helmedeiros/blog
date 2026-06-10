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
series:
  - lessons-from-a-pricing-platform
series_order: 6
description: "A coisa mais valiosa que a nossa plataforma de pricing produzia não eram preços. Era aprendizado."
subtitle: "Uma regra de pricing não é decisão. É previsão. E previsão pode estar errada."
---

O Business Rules Engine deu pra gente a capacidade de mudar pricing com segurança.

Não respondia a pergunta com a qual a gente mais se importava.

*A mudança foi boa mesmo?*

Por um tempo, a gente tratava regra de pricing como decisão. Aumentar um markup. Ajustar uma fee. Introduzir uma condição nova. Subir. Seguir adiante.

Quanto mais tempo passava em pricing, mais ia caindo a ficha de que esse jeito de pensar era incompleto.

Regra de pricing não é decisão.

Regra de pricing é hipótese.

A diferença parece sutil. Mudou como a gente pensava sobre pricing, experimentação, analytics e desenvolvimento de produto.

## A ilusão de certeza

Considere uma mudança simples de pricing.

> Aumentar a service fee de 5% pra 6%.

À primeira vista, parece decisão. Mas escondida dentro daquela frase tem uma suposição:

> A gente acredita que aumentar a service fee de 5% pra 6% vai aumentar a receita sem reduzir conversão de forma significativa.

Isso não é decisão. É previsão. E previsão pode estar errada.

Uma das lições mais úteis que aprendi em pricing é que sistema de receita tá cheio de suposição disfarçada de certeza. A gente supõe que o cliente vai tolerar uma fee. Supõe que um markup não vai afetar a demanda. Supõe que um mercado se comporta parecido com outro. Supõe que cliente percebe algumas mudanças e ignora outras.

Suposição só vira conhecimento quando a gente testa.

## A gente parou de discutir porcentagem

Conversa inicial de pricing costumava soar assim:

> Esse markup devia ser 3% ou 4%?
>
> A gente devia aumentar o teto da service fee?

Essas conversas estavam focadas em output. Com o tempo, a gente passou a fazer perguntas diferentes:

> O que a gente tá tentando aprender?
>
> Qual comportamento do cliente a gente espera mudar?
>
> O que faria a gente acreditar que essa ideia tá errada?

A conversa saiu de configuração e foi pra descoberta. Essa mudança de mentalidade acabou sendo mais importante do que qualquer modelo de pricing que a gente construiu depois.

## Por que o Business Rules Engine não bastava

O Business Rules Engine resolvia muita coisa. Dava ownership. Dava explicabilidade. Dava uma forma de separar capacidade de pricing da implementação do motor de regras por baixo.

Mas não gerava aprendizado.

A BRE avaliava uma regra. Não dizia se a regra devia existir. Pra isso, era preciso outra coisa. Era preciso experimentação.

A gente começou a construir as capacidades ao redor pra conseguir aprender com decisão de pricing — sistema de atribuição, tracking de experimento, coleta de dado de comportamento, pipeline analítica.

Não porque a gente queria mais infraestrutura. Porque queria resposta melhor.

## A/B testing e elasticidade de preço são problemas diferentes

Uma lição que me surpreendeu foi a frequência com que se usa *A/B testing* e *elasticidade de preço* como se fossem a mesma coisa.

São relacionadas. Respondem perguntas diferentes.

| | A/B testing | Elasticidade de preço |
| --- | --- | --- |
| Começa com | Uma decisão | Uma curiosidade |
| Setup | Dois variantes (ex.: 5% vs 6%) | Vários pontos (0%, 3%, 6%, 9%, …) |
| Pergunta | Qual performa melhor? | Como o comportamento do cliente muda quando o preço muda? |
| Resultado | Escolher um vencedor | Aprender o formato da curva de resposta |
| Melhor pra | Escolher | Entender |

Uma é pra escolher. A outra é pra entender. A diferença importa porque entender comportamento do cliente costuma valer mais do que escolher entre dois variantes.

## A gente parou de testar vencedor e começou a aprender curva

Essa foi uma das maiores transições da nossa jornada de pricing.

Os primeiros experimentos eram quase todos comparação: A versus B. Em algum momento, a gente começou a rodar experimento desenhado pra revelar sensibilidade do cliente ao preço.

Em vez de perguntar *"qual variante vence?"*, a gente perguntava *"em que ponto o comportamento do cliente começa a mudar?"*

Essa pergunta abriu a porta pra uma classe completamente diferente de insight. A gente descobriu que nem todo cliente reage a mudança de pricing da mesma forma. Alguns grupos eram muito sensíveis. Outros mal reagiam. Mudança que parecia perigosa se revelava com impacto quase nenhum. Outra que parecia inofensiva produzia mudança significativa de comportamento.

Esses achados não viriam de um A/B test só. Exigiam experimentação desenhada pra aprender, não pra validar.

## O problema de atribuição em experimento

Quando regra de pricing vira hipótese, outro desafio aparece.

*Quem deveria ver qual versão?*

Todo experimento precisa de um mecanismo que atribua cliente de forma consistente:

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

Sem atribuição confiável, experimento fica impossível de interpretar. Se cliente pula aleatoriamente entre variantes, a medição vira ruído. Se a atribuição tem viés, o resultado engana.

O desafio técnico de atribuição raramente é discutido fora do time de experimentação, mas é uma das fundações que torna o aprendizado possível.

A regra em si é só metade do experimento. A estratégia de atribuição é a outra metade.

## Receita é uma métrica perigosa

Um dos erros mais fáceis em pricing é otimizar só por receita.

Receita importa. Mas raramente conta a história toda. Uma mudança de pricing pode aumentar receita ao mesmo tempo em que prejudica conversão. Pode aumentar receita ao mesmo tempo em que reduz satisfação do cliente. Pode melhorar um mercado e prejudicar outro. Pode criar ganho de curto prazo e perda de longo prazo.

É por isso que toda hipótese de pricing precisa de guardrails.

| Métrica primária | Guardrails típicos |
| --- | --- |
| Receita | Taxa de conversão |
| Receita de service fee | Taxa de finalização de compra |
| Margem | Satisfação do cliente |
| Attach rate | Taxa de cancelamento |

As decisões de pricing mais difíceis não são aquelas em que uma métrica melhora. São aquelas em que várias métricas se movem em direções diferentes.

## A parte mais difícil não era rodar o experimento

A maioria das pessoas imagina experimentação como um desafio técnico.

Na prática, rodar o experimento costumava ser a parte fácil. Entender o resultado era mais difícil.

Imagine dois variantes:

- **Variante A** aumenta receita um pouco e melhora conversão.
- **Variante B** aumenta receita significativamente, mas reduz conversão.

Qual ganha?

Essa não é pergunta de engenharia. É pergunta de negócio.

Experimento não elimina tomada de decisão. Melhora a qualidade da informação disponível pra quem decide. O time ainda precisa decidir quais trade-offs importam.

## Os experimentos que mais ensinaram a gente

Olhando pra trás, os experimentos mais valiosos não foram os que deram certo. Foram os que derrubaram nossas suposições.

Os que mostraram um mercado se comportando diferente do esperado. Os que revelaram segmento de cliente que a gente tinha ignorado. Os que demonstraram que uma ideia que parecia óbvia, na real, estava errada.

Esses experimentos geraram o aprendizado mais valioso. E aprendizado compõe.

Uma mudança de pricing que dá certo cria valor uma vez. Uma lição sobre comportamento do cliente pode criar valor por anos.

## O que aprendi

A lição não era que cliente reage a preço. Todo mundo já sabe disso.

A lição era que cliente diferente reage diferente.

Quando isso caiu, regra individual de pricing parou de parecer resposta. Começou a parecer pergunta. Pergunta sobre comportamento do cliente. Pergunta sobre valor. Pergunta sobre disposição a pagar. Pergunta sobre trade-off.

Esse enquadramento mudou também o trabalho do time. A gente não estava entregando mudança de pricing. Estava rodando um ciclo de aprendizado:

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

O motor de regras deu pra gente uma forma de expressar decisão. A experimentação deu uma forma de questionar essa decisão. Juntos, criaram algo mais útil do que uma plataforma de pricing — um sistema de aprendizado.

O que a gente de fato estava aprendendo era que uma plataforma de pricing deixa de ser útil quando as pessoas que operam ela param de ter curiosidade sobre o cliente por trás do preço. Ferramenta, regra, motor, dashboard — nada disso sobrevive a um time que decidiu que a resposta já é óbvia.

Tratar cada regra como hipótese era só uma forma de se recusar a ser esse time.
