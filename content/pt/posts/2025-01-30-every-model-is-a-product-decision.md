---
title: "Todo Modelo É uma Decisão de Produto"
categories:
  - Data
  - Engineering
  - Pricing
  - Product
date: 2025-01-30
tags:
  - pricing
  - modelos-de-pricing
  - estrategia-de-produto
  - tomada-de-decisao
  - monetizacao
  - funcoes-objetivo
description: "A parte mais importante de um modelo de pricing não é o algoritmo. É a função objetivo."
subtitle: "Um modelo de pricing nunca é neutro. O que ele otimiza é uma decisão de produto vestida de matemática."
---

Existe uma frase específica que costumava fazer meus ombros relaxarem em reuniões de pricing: *o modelo é objetivo*.

Soava justo. A recomendação vinha dos dados. O algoritmo seguia regras mensuráveis. Comparado a uma sala de pessoas discutindo preço, qualquer coisa guiada por observação histórica soava como evolução.

Quanto mais tempo eu trabalhei com modelos de pricing, mais aquela palavra me incomodou. Não porque os modelos estivessem errados — a maioria deles era melhor do que as regras que substituíam. Porque *objetivo* era a palavra errada para o que eles estavam fazendo.

Todo modelo carregava suposições. Todo modelo embutia prioridades. Todo modelo refletia uma visão particular de como o sucesso se parecia. A matemática era honesta. A escolha do que maximizar não era neutra de jeito nenhum.

Um modelo de pricing não é, antes de tudo, um artefato técnico. É uma decisão de produto vestida de matemática.

## A ilusão da objetividade

A maior parte das conversas sobre modelos começa pela mecânica. Quais sinais incluir. Como ponderá-los. Onde colocar os limiares. Quão rápido a decisão precisa ser. Quão bem a versão nova se saiu contra a anterior.

Esses tópicos importam. Mas não é ali que as decisões mais importantes acontecem.

Imagine dois times. Os dois têm acesso aos mesmos dados. Os dois usam o mesmo algoritmo. Os dois observam os mesmos clientes. E ainda assim podem produzir recomendações completamente diferentes.

Por quê?

Porque eles otimizam para resultados diferentes. O algoritmo pode ser idêntico. O objetivo, não.

Eu vivi isso dentro do nosso próprio time mais de uma vez. O nosso product manager tinha recebido a missão de fazer receita crescer no trimestre. O nosso parceiro de finanças tinha recebido a missão de proteger retenção até o fim do ano. A gente tinha os mesmos dados, as mesmas recomendações na mesa, e uma noção silenciosamente diferente do que sucesso significava. Os dois lados eram honestos. Os dois estavam fazendo o que alguém na organização tinha pedido. Ninguém tinha pedido que a gente reconciliasse os dois antes de começar a construir.

O trabalho interessante acontecia na sala acima do trabalho de modelagem — aquela em que alguém decidia o que sucesso deveria parecer. Quando o dado chegava no notebook, essa decisão já tinha sido tomada. O modelo só estava, com muita eficiência, executando ela.

## A função objetivo é a estratégia

Uma forma útil de pensar em um modelo de pricing é como a parte de baixo de uma pilha bem mais alta:

{{< plantuml title="O modelo é a parte visível. O objetivo é a parte que sustenta o peso." >}}
@startuml
skinparam shadowing false
skinparam componentStyle rectangle

[Estratégia de negócio] as BS
[Função objetivo] as OF
[Modelo] as M
[Decisão] as D

BS --> OF
OF --> M
M --> D
@enduml
{{< /plantuml >}}

A maior parte dos times gasta seu tempo discutindo as duas caixas de baixo. A alavancagem mora no topo.

Antes de um modelo recomendar qualquer coisa, alguém precisa responder a uma pergunta difícil. *O que estamos tentando otimizar?* Essa resposta determina tudo o que vem depois.

## Objetivos diferentes criam modelos diferentes

Suponha exatamente o mesmo cliente, exatamente a mesma jornada e exatamente o mesmo histórico de dados. Agora imagine três objetivos de negócio diferentes.

| Objetivo | Resultado provável |
| --- | --- |
| Maximizar receita de curto prazo | Preços mais altos onde a demanda parece resiliente |
| Maximizar conversão | Preços menores para reduzir atrito |
| Maximizar valor de longo prazo do cliente | Equilibrar receita contra retenção e confiança |

O modelo não está escolhendo entre esses objetivos. A organização está. O modelo apenas operacionaliza a escolha.

É por isso que desacordos sobre pricing costumam ser conversas de estratégia disfarçadas. As pessoas brigam por números. O que estão de fato brigando é por prioridades.

## Modelos herdam os trade-offs

Um modelo de pricing não dissolve os trade-offs por baixo dele. Ele os codifica. Um modelo que maximiza receita pode recomendar algo bem diferente de um modelo que prioriza retenção do cliente — e nenhum dos dois é, necessariamente, errado: eles estão resolvendo problemas diferentes.

É por isso que parei de perguntar se um modelo era *bom* e passei a perguntar *bom para quê?*

## Acurácia não é o mesmo que utilidade

Uma armadilha que vi repetidamente foi supor que um modelo mais acurado, automaticamente, gera mais valor de negócio.

Às vezes gera. Às vezes não.

Um modelo pode melhorar a acurácia de previsão enquanto produz recomendações mais difíceis de explicar. Pode ficar mais sofisticado enquanto fica menos confiável. Pode capturar padrões sutis em que ninguém se sente à vontade para agir. O resultado é um sistema tecnicamente impressionante que tem dificuldade em influenciar decisões.

Acurácia importa. Utilidade importa também. As duas nem sempre andam juntas.

## Explicabilidade é um requisito de produto

Pricing se diferencia de muitos problemas de previsão em uma coisa importante: decisões de pricing são altamente visíveis.

Clientes veem. Stakeholders questionam. Times de atendimento têm que explicar. Product managers têm que defender.

Em algum momento, alguém pergunta:

> Por que o modelo recomendou isso?

Se ninguém consegue responder, a confiança começa a se desgastar.

A parte mais difícil é que a resposta certa depende de quem está perguntando. Um agente de atendimento em uma ligação precisa do motivo, em uma frase, de um preço específico em uma compra específica. Um product manager revisando performance da semana precisa dos fatores dominantes movendo um segmento. Um líder de finanças revisando o trimestre precisa de garantia de que o modelo não está se afastando das metas com as quais ele se comprometeu. Nenhuma dessas necessidades é técnica. Todas elas precisam ser desenhadas.

Sempre que tratávamos explicabilidade como algo para encaixar depois que o modelo já estava no ar, a gente perdia a batalha da confiança. Quando a ligação do atendimento chegava, a resposta que conseguíamos dar era ou vaga demais para ser útil, ou técnica demais para ser repetida. Da próxima vez que um preço parecesse estranho, a pergunta deixava de ir para a gente. Passava a contornar.

Isso não significa que todo modelo precise ser simples. Significa que todo modelo precisa de uma estratégia de explicação, desenhada junto com o próprio modelo, com um público definido para cada nível de detalhe.

Explicabilidade não é um afterthought de engenharia. Faz parte do produto.

## Todo modelo reflete uma visão de mundo

Compare duas abordagens de pricing que parecem idênticas por fora, e você encontra visões de mundo diferentes por baixo. Uma supõe que clientes são altamente sensíveis a preço. A outra supõe que conveniência importa mais. Uma confia em sinais de curto prazo. A outra espera os de longo prazo. Essas suposições se escondem por baixo da matemática. Elas continuam ali.

O modelo reflete o que a organização acredita sobre seus clientes — e silenciosamente desqualifica os clientes em quem ela não acredita.

## Os melhores modelos mudavam devagar

Os modelos que geravam mais valor raramente eram os mais sofisticados. Eram os que evoluíam de forma estável — uma melhoria pequena, um sinal mais afiado, um objetivo refinado, um ciclo de feedback mais limpo — tempo o bastante para a confiança acumular ao redor deles. Os maiores saltos vinham de acumular entendimento, não de substituir tudo.

## O que aprendi

A parte mais importante de um modelo de pricing não é o algoritmo. É a função objetivo.

O algoritmo determina *como* o modelo aprende. O objetivo determina *por que* o modelo existe.

Essa distinção mudou como eu avalio modelos. Em vez de perguntar *"quão acurado é esse modelo?"*, passei a perguntar *"que decisão esse modelo está nos ajudando a tomar?"*. A segunda pergunta acabou sendo muito mais útil.

## Reflexão final

O perigo de "o modelo é objetivo" é que essa frase encerra a conversa que precisava acontecer. Quando uma recomendação chega embrulhada em matemática, ela deixa de ser questionada — e a escolha estratégica por baixo dela nunca é nomeada.

O que mantinha o nosso modelo honesto, quando ele se mantinha honesto, era uma única frase. O que ele estava otimizando. O que ele estava desprioritizando para fazer isso. E quem na organização tinha dito sim a essa troca. Quando essa frase ainda não existia, a coisa certa em geral era parar de construir e ir procurar por ela.

Um modelo sem essa frase não é objetivo. É só a preferência de alguém, automatizada.
