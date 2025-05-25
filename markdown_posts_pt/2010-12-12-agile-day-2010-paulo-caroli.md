---
title: "AGILE DAY 2010 – Paulo Caroli"
date: 2010-12-12
slug: agile-day-2010-paulo-caroli
tags:
  - agile
draft: false
language: pt
---

No último dia 29 de novembro tivemos durante a tarde do Agile Day 2010 Porto Alegre uma excelente transferência de experiências conduzida pelo Paulo Caroli da ThoughtWorks, com sua palestra A LINHA DE MONTAGEM DE SW representada como cartões na parede.
Paulo Caroli Agile Day Porto Alegre 2010
A apresentação foi iniciada evidenciando Taylor e suas contribuições ao aumento da eficiência industrial, com uma ressalva a uma de suas teorias de gerência, a scientific management, que em linhas gerais integrava a lógica produtiva a especialização de cada operário, aproveitando estas vantagens empregando-as em um determinado ponto no caminho para a construção desejada. A este conjunto de pontos e o seu entre fluxo no caminho de se objetivar um sucesso foi dado o nome de WORKFLOW, e é aí que entra a importância do Taylor nesta apresentação.
Para o Caroli este workflow foi ressaltado um pouco adiante por Frederick Brooks que ressaltou que o objetivo deste fluxo, para equipes de TI, seria apenas criar um produto de software; o que não sua visão é incompleto uma vez que não ressalta a melhoria do processo de desenvolvimento. Outro ponto de ressalva foi o tamanho de cada etapa dos workflows, que segundo Caroli, quando muito grandes não são interessantes para abordagem diretamente na parede, sendo excelente então a simplificação ou o ataque por etapa com a estratégia de Card Wall.
Para o entendimento de workflows foi apresentado logo a seguir um conjunto de fotos, sobre as quais foram tecidos comentários cada uma delas com uma característica das linhas de montagens, mas sempre um ponto em comum, FEEDBACK e AMBIENTE INFORMATIVO. Dentre estes flows foi aberto um adendo para exemplificar o processo realizado pela starbucks, uma vez que este é um processo simples, claro e visível.
Na Starbucks é fácil, aos clientes, a verificação há todo tempo sobre a velocidade e a previsão de seu atendimento. Se existe fila, sei quantas pessoas precisam ser atendidas antes de mim, não existem pessoas sentadas esperando os seus pedidos, em seguida a sua compra existe uma fila de copos até a sua execução pelo barista.
Este workflow representado em um card wall tornaria tão simples sua verificação, quanto a já existente em chão de fábrica, visualizável como definido anteriormente. Neste card wall dividiríamos nossas etapas em raias (Na fila, caixa, barista e bebida pronta) e faríamos representações das pessoas e copos no mesmo. Sendo assim, qualquer pessoa pode rápidamente saber quantas pessoas faltam ser atendidas em qualquer uma das fases instantaneamente.
Dentro do universo de software, temos a algum tempo estas idéis aplicadas, todo software tem um conjunto de fases, e mesmo que hoje em dia realizemos críticas a modelos clássicos como o cascata, as fases ainda são a mesma, mas em pequenas dosagens que fazem toda a diferença mas isso não vem ao caso. Então tendo Analise, Design, Codificação, Teste e Read To GO, colocando estas etapas na parede temos nosso workflow na parede! Para o Paulo Caroli a fase de quality assurance esta em todo o processo isso é um atributo da equipe!
O Caroli apresentou logo em seguida o card wall para software mais utilizado por ele tem, que é composto por backlog, in dev, in quality control e Read To significa off, e esclareceu que para se trabalhar efetivamente esta técnica deve-se trabalhar o formato de pull, então todos puxam uma tarefa e movimenta quando estão livres e não ao contrário, nenhum gerente aponta, o time decide e ele sabe quando receber novas entradas!
Para trabalharmos de forma pareada o card wall apresenta quando devemos separar duplas, criá-las! O objetivo é eliminar problemas; o trabalho tem que acontecer o mais rápido possível, não devemos parar, e com card walls os gargalos estão visíveis na parede! Existem casos em que algum responsável esta ausente, esse é um gargalo… então não deixe tornar isto visível! Holding, idle! Todos devem estar visíveis.
Dentro deste contexto entram em cena os Waiting stages e os action stages! Para o Paulo é muito importante deixarmos visíveis também quais das etapas de nosso workflow devem ser prioridades, quais delas realmente representam um momento em que algo não pode ser alterado por um tempo, para o não permitir acúmulos! Etapas marcadas como Waiting stages devem permitir pausas e estas por sua vez não serão preocupantes, fazem parte do fluxo. Em contrapartida etapas marcadas como action stages devem fornecer uma preocupação extra enquanto a longas permanências e acúmulos.
Os card walls também ajudam o time a entender seu próprio progresso, detalhando ainda mais suas métricas. Um time pode realizar dois projetos com a mesma velocidade, mas vivenciando situações completamente diferentes durantes suas iterações. Enquanto em um estes podem completar todo o trabalho apenas no último dia sobre trancos e barrancos, o outro podem conseguir construir com a mesma velocidade mas em pequenas e confortáveis conclusões diárias. Para tal o time utilizara-se de três medidas o bandwidth, latency e o throughtput que são nesta ordem a quantidade de stories ou tarefas que você consegue fazer simultaneamente (O kanban define o limite do seu bandwidth por etapa), o tempo que cada uma destas demora até que seja concluída e por fim a vazão, que leva em consideração a quantidade de tempo na passagem de uma etapa para a outra, muito usada para a quantidade de conclusões diárias.
Métricas no card wall - Paulo Caroli
*Vale a pena ler o artigo do Caroli sobre como eles desenvolveram uma tática ecologicamente sustentável, mas socio-higienicamente desfavorável para evidenciar de forma automatizada o latency. Latency and banana
Em seguida o Paulo apresentou efetivamente a adição no card wall de limites, que segundo ele auxiliam na consciência coletiva juntamente ao pull system, promovendo uma movimentação constante no time para actionstages mediante a impossibilidade de promover uma tarefa devido a um limite existente.
Segundo Paulo os limites ainda podem ser agregados à uma sequência de priorização por elevação no card wall, onde quanto mais próxima do topo do quadro uma story está mais prioritária a mesma é, para que possamos trabalhar ainda mais a reatividade do time as mudanças do processo e do fluxo de forma auto organizada! Oque está mais elevado é mais importante, cada membro do time só executa uma tarefa por vez, existe um limite em algumas etapas! Então tudo flui prioritariamente e ninguém trabalha fora da ordem necessária!
Em um card wall podem existir também abaixo do granularidade de user stories, as tasks. O cardwall trabalha com stories, que são divididas em tarefas, então dentro de cada uma das fases teríamos o desenvolvimento em novas raias como to do, doing e done! Vejam o blog do Alisson Vale, que fala um pouco mais sobre esta técnica de sub-representação.
Outra sub-divisão que rondam os card walls e que são realidade em qualquer projeto de software, mesmo aquelas com qualidade superior a 90%, são os BUGS. Para o Caroli este devem ser evidenciados e priorizados! Quando existem muitos bugs este devem ser elevados a uma nova raia que deve ser tratados com regras de uma passing lane, você deve deixá-la sempre desocupada e só usá-la em momentos críticos, quem está nela está sempre em uma velocidade maior e é sempre prioritário!
A apresentação do Apulo acabou com um conjunto de perguntas sobre as quais enfatizou-se a refatoração dos card walls, adaptando durante os tempos coletivamente em sua equipe. Tente aproveitar as outras dimensões do seu quadro! Complemente-o com outras tecnologias!
Slides da Linha de Montagem de Software
agile
- __
- __
- __
- __
- __
- __

- Agile: Unlocking our Human Potential – Patrick Kua
- AgileBR bem vindo!!
- Agile Portfolio Planning: Managing Your Project Portfolio – Johanna Rothman
- Bem vindo ao Agile Brazil 2012
- The role of Agile analysis in Continuous Delivery – Jenny Wong e Danilo Sato

- Agile: Unlocking our Human Potential – Patrick Kua
- AgileBR bem vindo!!
- Agile Portfolio Planning: Managing Your Project Portfolio – Johanna Rothman
- Bem vindo ao Agile Brazil 2012
- The role of Agile analysis in Continuous Delivery – Jenny Wong e Danilo Sato