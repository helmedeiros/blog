---
title: "How Impala has Pushed HDFS in New Ways"
date: 2014-04-10
slug: how-impala-has-pushed-hdfs-in-new-ways
tags:
  - big-data
draft: false
language: pt
---

Como Impala e a Cloudera tem ajudado a comunidade nos últimos anos, nada melhor que o Aaron para falar sobre isso commiter do Hadoop, vamos ver como funciona HDFS, impala e como o último tem sido alterado para atender novos requisitos.
Quando as pessoas falam sobre Hadoop, uma parte esta atrelada ao HDFS (Hadoop Distributed File System). Este é utilizado apenas como um file-system distribuído, ele foi única e exclusivamente para trabalhar com blocos de dados grandes que precisam ser rápidos para uma boa performance de MapReduce.
Cada cluster HDFS é composto por clusters com vários nodos, eles armazenam metadados e dados. Existem block maps e file system metadados e estes organizam todo o fluxo de acesso.
O Impala é uma engine de propósito geral para processamento de queries em HQL (Hive Query Language), ela funciona tanto para processamento analítico como em tempo de execução. Ele roda de forma distribuida em clusters, e podemos submeter queries com ODBC /JDBC.
Quando fazemos um deploy do Impala em nosso ambiente o que temos por baixo dos panos são dois daemons, o impalad e o statestored. O impalad lida com todos os requestes dos clientes; o statestored trata com todos os estados necessários ao funcionamento dos _daemons. _Cada requisição ao Impala é feita via odbc/jdbc , estas requisições são paralisadas por meio de planos de execução.
arquitetura da cloudera impala
Quais são as melhorias trazidas pelo Impala ao HDFS?
Primeiro o Impala está preocupado com queries de baixa latência e para isso ser feito não a como excluir o fato dos cenários distribuídos, como replicas co-alocadas bloqueadas, pela leitura local versus velocidade de rede. Impala adicionou uma funcionalidade que especifica que um conjunto de dados deve saber onde estão suas replicas.
Atualmente a vazão dos discos não são tão rápidos que possamos, acessá-los para realizar o processamento dos arquivos em tempo real, com o peso dos arquivos, para tal _Impala _facilitou ao HDFS ler diretamente da memória principal de forma otimizada.
Por estas e outras melhorias _impala _se coloca 5-10x mais rápido que o Hive para queries simples e 20-50x em queries complexas com joins.
big-data
- __
- __
- __
- __
- __
- __

- Hadoop and the Big Data Ecosystem
- Building a Data Science Program at NASA/JPL with Visual Analytics
- Data Science em Tempo Real com Storm
- Um Sistema de recomendação de produtos baseado em grafos: Titan, Cassandra, Redis e Hadoop em produção

- Hadoop and the Big Data Ecosystem
- Building a Data Science Program at NASA/JPL with Visual Analytics
- Data Science em Tempo Real com Storm
- Um Sistema de recomendação de produtos baseado em grafos: Titan, Cassandra, Redis e Hadoop em produção