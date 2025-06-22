---
title: Hadoop and the Big Data Ecosystem
author: helio
layout: post
date: 2014-04-11 13:36:05+00:00
embed:
  - This is the default text
seo_follow:
  - "false"
seo_noindex:
  - "false"
dsq_thread_id:
  - 4969853650
categories:
  - Agile
  - Technology
  - Events
tags:
  - big data
  - hadoop
  - qconsp
  - Todd Lipcon
subtitle: Navegue pela evolução do ecossistema Hadoop—das origens do MapReduce do Google aos frameworks modernos como Spark, Sqoop e Flume que lidam com terabytes de dados com princípios KISS
---

Porque devemos nos preocupar? Assim começou o keynote do <a title="Todd Lipcon" href="https://twitter.com/tlipcon" target="_blank">Todd Lipcon</a>&#8230; Talvez porque ao longo dos últimos anos, as empresas têm visto uma explosão no volume, variedade e velocidade dos dados que eles têm de lidar todos os dias. Esta tem sido uma bênção e uma maldição. Ao mesmo tempo que a explosão de dados nos permitiu gerar novos tipos de aplicativos e insights altamente inteligentes, os desenvolvedores descobriram que a geração anterior de ferramentas de gerenciamento de dados e frameworks desmoronavam quando tentando trabalhar e manter terabytes ou petabytes de dados muitas vezes mal-estruturados.

Quando Todd era uma criança ele encontrou um programa que se fazia passar por uma pessoa respondendo, e depois de algumas perguntas ele descobriu que o programa era muito burro. Apresentando-o a seu pai, foi desafiado, tentou melhorá-lo mas com tal idade, não conseguiu ir muito a frente. Passados 20 anos depois ele vê o <a title="Watson" href="http://en.wikipedia.org/wiki/Watson_(computer)" target="_blank">watson</a> respondendo todos estas perguntas&#8230; a diferença? <a title="Big Data" href="http://en.wikipedia.org/wiki/Big_data" target="_blank">Big data</a>!!

Voltando um pouco no tempo ele começou a mostrar os primeiros passos de um caminho, que passavam pela indexação recursiva e morosa e sem sombra de dúvida por equipamentos e software proprietário de grandes empresas.

Isso começou a mudar com a google, eles criaram seu proprio storage e uma infraestrutura de processamento, o <a title="MapReduce" href="http://en.wikipedia.org/wiki/MapReduce" target="_blank">MapReduce</a> surgiu aí baseado na premissa do <a title="Keep it simple stupid" href="http://en.wikipedia.org/wiki/KISS_principle" target="_blank">KISS</a>. Estas tecnologias ainda estão a todo vapor até os dias atuais, eles nunca os venderam, mas escreveram vários papers que deram origem a várias legais que estão por aí.

O <a title="Hadoop" href="http://hadoop.apache.org/" target="_blank">Hadoop</a> surgiu um tempo depois com o <a title="Doug Cutting" href="https://twitter.com/cutting" target="_blank">Doug Cutting</a>, que tinha problemas bem parecidos com os que a google tinha, lendo os papers  do google encontrou uma boa estratégia para trabalhar com grandes arquivos de forma distribuída.

O Hadoop é um armazenador e processador de dados escaláveis, que podem trabalhar sobre qualquer maquinário. As maquinas dentro do esquema Hadoop são conhecidos como nodes, e o processamento sobre estes dados distribuídos em nós é totalmente transparente como se não houvesse realmente distinção entre local e remoto.

Uma das partes fundamentais do Hadoop é o <a title="Hadoop Distributed File System" href="http://hadoop.apache.org/docs/r1.2.1/hdfs_design.html" target="_blank">HDFS</a>, ele permite trabalharmos com arquivos grandes repartindo-os em blocos de tamanhos máximos, e replicando-os para que eles possam permitir redundância, para evitar a perda de informações ou interrupção no processamento em caso de falhas.

Outra parte fundamental é o MapReduce, um modelo de programação que tem duas partes principais, instruções para realizar transformações, parseamento, ou filtrar dados, esta sempre roda antes e sempre devolve resultados; e instruções para sumarizar os dados. Estas instruções trazem muita simplicidade ao trabalho diário processando um registro por vez, não existe necessidade em realizar I/O explicitamente e ele é bem escalonável.<figure id="attachment_849" style="width: 468px" class="wp-caption aligncenter">

[<img class="size-full wp-image-849" alt="Reducing Soft kitties!!" src="/uploads/2014/04/mapreduce.jpg" width="468" height="240" srcset="/uploads/2014/04/mapreduce.jpg 468w, /uploads/2014/04/mapreduce-300x153.jpg 300w" sizes="(max-width: 468px) 100vw, 468px" />][1]<figcaption class="wp-caption-text">Reducing Soft kitties!!</figcaption></figure>

Neste momento o Todd nos apresentou um MapReduce sobre um domínio simples, para contagem de palavras na música infantil abaixo, entrando em detalhes em como poderíamos conquistar velocidade para este modelo nos fazendo da implementação de MapReduce do Hadoop.

> Soft kitty,

> Warm kitty,

> Little ball of fur.

> Happy kitty,

> Sleepy kitty,

> Purr Purr Purr

Alguns frameworks foram citados:

<p style="padding-left: 30px">
  <strong><a title="Apache Spark" href="http://spark.apache.org/" target="_blank">Spark</a>:</strong> é um framework  que trabalha MapReduce, suporta várias linguagens e tem um shell interactive. Comparando códigos de Maps feitos no Hadoop e com o Spark temos uma redução em níveis de 10x na quantidade de linhas necessárias. Os ganhos também vão em termos de velocidade processamentos;
</p>

<p style="padding-left: 30px">
  <strong><a title="Apache Sqoop" href="http://sqoop.apache.org/" target="_blank">Sqoop</a>:</strong> facilitara a troca eficiente de massas de dados entre Apache Hadoop e storages de dados estruturados, tais como bancos de dados relacionais;
</p>

<p style="padding-left: 30px">
  <span style="line-height: 1.5em"><strong><a title="Apache Flume" href="http://flume.apache.org/" target="_blank">Flume</a>:</strong> permite a importação de dados para o HDFS enquanto ele são gerados em uma quantidade qualquer de máquinas.</span>
</p>

[1]: /uploads/2014/04/mapreduce.jpg
