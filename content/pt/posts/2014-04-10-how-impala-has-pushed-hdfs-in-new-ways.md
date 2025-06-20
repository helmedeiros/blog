---
title: How Impala has Pushed HDFS in New Ways
author: helio
layout: post
date: 2014-04-10T16:05:02+00:00
embed:
  - This is the default text
seo_follow:
  - 'false'
seo_noindex:
  - 'false'
categories: ["Technology", "Architecture"]
tags:
  - aaron myers
  - cloudera
  - impala
  - qconsp
---
Como Impala e a [Cloudera][1] tem ajudado a comunidade nos últimos anos, nada melhor que o <a title="Aaron Myers" href="https://twitter.com/atm" target="_blank">Aaron</a> para falar sobre isso commiter do <a title="Hadoop" href="http://hadoop.apache.org/" target="_blank">Hadoop</a>, vamos ver como funciona <a title="HDFS" href="http://hadoop.apache.org/docs/r1.2.1/hdfs_design.html" target="_blank">HDFS</a>, impala e como o último tem sido alterado para atender novos requisitos.

Quando as pessoas falam sobre Hadoop, uma parte esta atrelada ao HDFS (Hadoop Distributed File System). Este é utilizado apenas como um file-system distribuído, ele foi única e exclusivamente para trabalhar com blocos de dados grandes que precisam ser rápidos para uma boa performance de <a title="MapReduce" href="http://en.wikipedia.org/wiki/MapReduce" target="_blank">MapReduce</a>.

Cada cluster HDFS é composto por clusters com vários nodos, eles armazenam metadados e dados. Existem block maps e file system metadados e estes organizam todo o fluxo de acesso.

O <a title="Impala" href="http://en.wikipedia.org/wiki/Cloudera_Impala" target="_blank">Impala</a> é uma engine de propósito geral para processamento de queries em HQL (Hive Query Language), ela funciona tanto para processamento analítico como em tempo de execução.   Ele roda de forma distribuida em clusters, e podemos submeter queries com <a title="Open Database Connectivity" href="http://en.wikipedia.org/wiki/ODBC" target="_blank">ODBC</a> /<a title="Java Database Connectivity" href="http://en.wikipedia.org/wiki/JDBC" target="_blank">JDBC</a>.

Quando fazemos um deploy do Impala em nosso ambiente o que temos por baixo dos panos são dois daemons, o impalad e o _statestored_. O _impalad_ lida com todos os requestes dos clientes; o _statestored _ trata com todos os estados necessários ao funcionamento dos _daemons. _Cada requisição ao _Impala é feita via odbc/jdbc_, estas requisições são paralisadas por meio de planos de execução.<figure id="attachment_831" style="width: 468px" class="wp-caption aligncenter">

[<img class="size-full wp-image-831" alt="arquitetura da cloudera impala" src="/uploads/2014/04/cloudera_impala.jpg" width="468" height="240" srcset="/uploads/2014/04/cloudera_impala.jpg 468w, /uploads/2014/04/cloudera_impala-300x153.jpg 300w" sizes="(max-width: 468px) 100vw, 468px" />][2]<figcaption class="wp-caption-text">arquitetura da cloudera impala</figcaption></figure> 

Quais são as melhorias trazidas pelo Impala ao HDFS?

Primeiro o Impala está preocupado com queries de baixa latência e para isso ser feito não a como excluir o fato dos cenários distribuídos, como replicas co-alocadas bloqueadas, pela leitura local versus velocidade de rede. Impala adicionou uma funcionalidade que especifica que um conjunto de dados deve saber onde estão suas replicas.

Atualmente a vazão dos discos não são tão rápidos que possamos, acessá-los para realizar o processamento dos arquivos em tempo real, com o peso dos arquivos, para tal  _Impala _facilitou ao HDFS ler diretamente da memória principal de forma otimizada.

Por estas e outras melhorias _impala _se coloca 5-10x mais rápido que o <a title="Hive" href="http://hive.apache.org/" target="_blank"><em>Hive</em></a> para queries simples e 20-50x em queries complexas com joins.

 [1]: http://www.cloudera.com/content/cloudera/en/home.html "cloudera"
 [2]: /uploads/2014/04/cloudera_impala.jpg