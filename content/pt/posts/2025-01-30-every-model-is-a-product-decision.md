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
series:
  - pricing-platform
series_order: 11
description: "A parte mais importante de um modelo de pricing não é o algoritmo. É a função objetivo."
subtitle: "Modelo de pricing nunca é neutro. O que ele otimiza é decisão de produto vestida de matemática."
---

Existe uma frase específica que costumava fazer meus ombros relaxarem em reunião de pricing: *o modelo é objetivo*.

Soava justo. A recomendação vinha do dado. O algoritmo seguia regra mensurável. Comparado a uma sala de pessoas discutindo preço, qualquer coisa guiada por observação histórica parecia evolução.

Quanto mais tempo eu trabalhei com modelo de pricing, mais aquela palavra me incomodou. Não porque o modelo estivesse errado — a maioria deles era melhor do que as regras que substituíam. Porque *objetivo* era a palavra errada pro que eles estavam fazendo.

Todo modelo carregava suposição. Todo modelo embutia prioridade. Todo modelo refletia uma visão particular de como o sucesso se parecia. A matemática era honesta. A escolha do que maximizar não era neutra de jeito nenhum.

Um modelo de pricing não é, antes de tudo, artefato técnico. É decisão de produto vestida de matemática.

## A ilusão da objetividade

A maior parte das conversas sobre modelo começa pela mecânica. Quais sinais incluir. Como ponderar eles. Onde colocar os limiares. Quão rápido a decisão precisa ser. Quão bem a versão nova se saiu contra a anterior.

Esses tópicos importam. Mas não é ali que as decisões mais importantes acontecem.

Imagine dois times. Os dois têm acesso ao mesmo dado. Os dois usam o mesmo algoritmo. Os dois observam os mesmos clientes. E ainda assim podem produzir recomendações completamente diferentes.

Por quê?

Porque otimizam pra resultado diferente. O algoritmo pode ser idêntico. O objetivo, não.

Eu vivi isso dentro do nosso próprio time mais de uma vez. O nosso product manager tinha recebido a missão de fazer receita crescer no trimestre. O nosso parceiro de finanças tinha recebido a missão de proteger retenção até o fim do ano. A gente tinha os mesmos dados, as mesmas recomendações na mesa, e uma noção silenciosamente diferente do que sucesso significava. Os dois lados eram honestos. Os dois estavam fazendo o que alguém na organização tinha pedido. Ninguém tinha pedido pra gente reconciliar os dois antes de começar a construir.

O trabalho interessante acontecia na sala acima do trabalho de modelagem — aquela em que alguém decidia o que sucesso devia parecer. Quando o dado chegava no notebook, essa decisão já tinha sido tomada. O modelo só estava, com muita eficiência, executando ela.

## A função objetivo é a estratégia

Uma forma útil de pensar num modelo de pricing é como a parte de baixo de uma pilha bem mais alta:

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

A maior parte dos times gasta tempo discutindo as duas caixas de baixo. A alavancagem mora no topo.

Antes do modelo recomendar qualquer coisa, alguém precisa responder uma pergunta difícil. *O que a gente tá tentando otimizar?* Essa resposta determina tudo o que vem depois.

## Objetivo diferente cria modelo diferente

Suponha exatamente o mesmo cliente, exatamente a mesma jornada e exatamente o mesmo histórico de dado. Agora imagine três objetivos de negócio diferentes.

| Objetivo | Resultado provável |
| --- | --- |
| Maximizar receita de curto prazo | Preço mais alto onde a demanda parece resiliente |
| Maximizar conversão | Preço menor pra reduzir atrito |
| Maximizar valor de longo prazo do cliente | Equilibrar receita contra retenção e confiança |

O modelo não tá escolhendo entre esses objetivos. A organização tá. O modelo só operacionaliza a escolha.

É por isso que desacordo sobre pricing costuma ser conversa de estratégia disfarçada. As pessoas brigam por número. O que estão de fato brigando é por prioridade.

## Modelo herda os trade-offs

Modelo de pricing não dissolve os trade-offs por baixo dele. Codifica. Um modelo que maximiza receita pode recomendar algo bem diferente de um modelo que prioriza retenção do cliente — e nenhum dos dois é, necessariamente, errado: estão resolvendo problemas diferentes.

É por isso que parei de perguntar se um modelo era *bom* e passei a perguntar *bom pra quê?*

## Acurácia não é o mesmo que utilidade

Uma armadilha que vi direto foi supor que um modelo mais acurado, automaticamente, gera mais valor de negócio.

Às vezes gera. Às vezes não.

Um modelo pode melhorar acurácia de previsão enquanto produz recomendação mais difícil de explicar. Pode ficar mais sofisticado enquanto fica menos confiável. Pode capturar padrão sutil que ninguém se sente à vontade pra agir em cima. O resultado é um sistema tecnicamente impressionante que tem dificuldade de influenciar decisão.

Acurácia importa. Utilidade importa também. As duas nem sempre andam juntas.

## Explicabilidade é requisito de produto

Pricing se diferencia de muitos problemas de previsão em uma coisa importante: decisão de pricing é altamente visível.

Cliente vê. Stakeholder questiona. Time de atendimento tem que explicar. Product manager tem que defender.

Em algum momento, alguém pergunta:

> Por que o modelo recomendou isso?

Se ninguém consegue responder, a confiança começa a se desgastar.

A parte mais difícil é que a resposta certa depende de quem está perguntando. Um agente de atendimento numa ligação precisa do motivo, numa frase, de um preço específico numa compra específica. Um product manager revisando performance da semana precisa dos fatores dominantes movendo um segmento. Um líder de finanças revisando o trimestre precisa de garantia de que o modelo não tá se afastando das metas com as quais ele se comprometeu. Nenhuma dessas necessidades é técnica. Todas precisam ser desenhadas.

Sempre que a gente tratava explicabilidade como algo pra encaixar depois que o modelo já tava no ar, a gente perdia a batalha da confiança. Quando a ligação do atendimento chegava, a resposta que conseguíamos dar era ou vaga demais pra ser útil, ou técnica demais pra ser repetida. Da próxima vez que um preço parecesse estranho, a pergunta deixava de ir pra gente. Passava a contornar.

Isso não significa que todo modelo precise ser simples. Significa que todo modelo precisa de uma estratégia de explicação, desenhada junto com o próprio modelo, com um público definido pra cada nível de detalhe.

Explicabilidade não é afterthought de engenharia. Faz parte do produto.

## Todo modelo reflete uma visão de mundo

Compare duas abordagens de pricing que parecem idênticas por fora, e você encontra visões de mundo diferentes por baixo. Uma supõe que cliente é altamente sensível a preço. A outra supõe que conveniência importa mais. Uma confia em sinal de curto prazo. A outra espera o de longo prazo. Essas suposições se escondem por baixo da matemática. Continuam ali.

O modelo reflete o que a organização acredita sobre os clientes — e silenciosamente desqualifica os clientes em quem ela não acredita.

## Os melhores modelos mudavam devagar

Os modelos que geravam mais valor raramente eram os mais sofisticados. Eram os que evoluíam de forma estável — uma melhoria pequena, um sinal mais afiado, um objetivo refinado, um ciclo de feedback mais limpo — tempo o bastante pra confiança acumular ao redor deles. Os maiores saltos vinham de acumular entendimento, não de substituir tudo.

## O que aprendi

A parte mais importante de um modelo de pricing não é o algoritmo. É a função objetivo.

O algoritmo determina *como* o modelo aprende. O objetivo determina *por que* o modelo existe.

Essa distinção mudou como eu avalio modelo. Em vez de perguntar *"quão acurado é esse modelo?"*, passei a perguntar *"que decisão esse modelo tá ajudando a gente a tomar?"*. A segunda pergunta acabou sendo muito mais útil.

## Reflexão final

O perigo de "o modelo é objetivo" é que essa frase encerra a conversa que precisava acontecer. Quando uma recomendação chega embrulhada em matemática, ela deixa de ser questionada — e a escolha estratégica por baixo dela nunca é nomeada.

O que mantinha o nosso modelo honesto, quando ele se mantinha honesto, era uma frase única. O que ele estava otimizando. O que ele estava desprioritizando pra fazer isso. E quem na organização tinha dito sim a essa troca. Quando essa frase ainda não existia, a coisa certa em geral era parar de construir e ir procurar por ela.

Modelo sem essa frase não é objetivo. É só preferência de alguém, automatizada.
