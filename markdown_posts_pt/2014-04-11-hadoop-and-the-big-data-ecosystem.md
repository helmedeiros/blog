---
title: "Hadoop and the Big Data Ecosystem"
date: 2014-04-11
slug: hadoop-and-the-big-data-ecosystem
tags:
  - big-data
draft: false
language: pt
---

Porque devemos nos preocupar? Assim começou o keynote do Todd Lipcon… Talvez porque ao longo dos últimos anos, as empresas têm visto uma explosão no volume, variedade e velocidade dos dados que eles têm de lidar todos os dias. Esta tem sido uma bênção e uma maldição. Ao mesmo tempo que a explosão de dados nos permitiu gerar novos tipos de aplicativos e insights altamente inteligentes, os desenvolvedores descobriram que a geração anterior de ferramentas de gerenciamento de dados e frameworks desmoronavam quando tentando trabalhar e manter terabytes ou petabytes de dados muitas vezes mal-estruturados.
Quando Todd era uma criança ele encontrou um programa que se fazia passar por uma pessoa respondendo, e depois de algumas perguntas ele descobriu que o programa era muito burro. Apresentando-o a seu pai, foi desafiado, tentou melhorá-lo mas com tal idade, não conseguiu ir muito a frente. Passados 20 anos depois ele vê o watson respondendo todos estas perguntas… a diferença? Big data!!
Voltando um pouco no tempo ele começou a mostrar os primeiros passos de um caminho, que passavam pela indexação recursiva e morosa e sem sombra de dúvida por equipamentos e software proprietário de grandes empresas.
Isso começou a mudar com a google, eles criaram seu proprio storage e uma infraestrutura de processamento, o MapReduce surgiu aí baseado na premissa do KISS. Estas tecnologias ainda estão a todo vapor até os dias atuais, eles nunca os venderam, mas escreveram vários papers que deram origem a várias legais que estão por aí.
O Hadoop surgiu um tempo depois com o Doug Cutting, que tinha problemas bem parecidos com os que a google tinha, lendo os papers do google encontrou uma boa estratégia para trabalhar com grandes arquivos de forma distribuída.
O Hadoop é um armazenador e processador de dados escaláveis, que podem trabalhar sobre qualquer maquinário. As maquinas dentro do esquema Hadoop são conhecidos como nodes, e o processamento sobre estes dados distribuídos em nós é totalmente transparente como se não houvesse realmente distinção entre local e remoto.
Uma das partes fundamentais do Hadoop é o HDFS, ele permite trabalharmos com arquivos grandes repartindo-os em blocos de tamanhos máximos, e replicando-os para que eles possam permitir redundância, para evitar a perda de informações ou interrupção no processamento em caso de falhas.
Outra parte fundamental é o MapReduce, um modelo de programação que tem duas partes principais, instruções para realizar transformações, parseamento, ou filtrar dados, esta sempre roda antes e sempre devolve resultados; e instruções para sumarizar os dados. Estas instruções trazem muita simplicidade ao trabalho diário processando um registro por vez, não existe necessidade em realizar I/O explicitamente e ele é bem escalonável.
Reducing Soft kitties!!
Neste momento o Todd nos apresentou um MapReduce sobre um domínio simples, para contagem de palavras na música infantil abaixo, entrando em detalhes em como poderíamos conquistar velocidade para este modelo nos fazendo da implementação de MapReduce do Hadoop.
> Soft kitty,Warm kitty,Little ball of fur.Happy kitty,Sleepy kitty,Purr Purr Purr

Alguns frameworks foram citados:
Spark: é um framework que trabalha MapReduce, suporta várias linguagens e tem um shell interactive. Comparando códigos de Maps feitos no Hadoop e com o Spark temos uma redução em níveis de 10x na quantidade de linhas necessárias. Os ganhos também vão em termos de velocidade processamentos;
Sqoop: facilitara a troca eficiente de massas de dados entre Apache Hadoop e storages de dados estruturados, tais como bancos de dados relacionais;
Flume: permite a importação de dados para o HDFS enquanto ele são gerados em uma quantidade qualquer de máquinas.
big-data
- __
- __
- __
- __
- __
- __

- Building a Data Science Program at NASA/JPL with Visual Analytics
- Data Science em Tempo Real com Storm
- How Impala has Pushed HDFS in New Ways
- Um Sistema de recomendação de produtos baseado em grafos: Titan, Cassandra, Redis e Hadoop em produção

- Building a Data Science Program at NASA/JPL with Visual Analytics
- Data Science em Tempo Real com Storm
- How Impala has Pushed HDFS in New Ways
- Um Sistema de recomendação de produtos baseado em grafos: Titan, Cassandra, Redis e Hadoop em produção