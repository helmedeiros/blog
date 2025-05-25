---
title: "Um Sistema de recomendação de produtos baseado em grafos: Titan, Cassandra, Redis e Hadoop em produção"
date: 2014-04-10
slug: um-sistema-de-recomendacao-de-produtos-baseado-em-grafos-titan-cassandra-redis-e-hadoop-em-producao
tags:
  - big-data
draft: false
language: pt
---

> Big data is like teenage sex: everyone talks about it, nobody really knows how to do it, everyone thinks everyone else is doing it, so everyone claims they are doing it..

As maiores empresas estão tentando descobrir e ajudar a empresa a a interseção entre oque as pessoas querem, e o que a empresa quer que as pessoas comprem. Neste contexto o Andre Fatala e o Renato Pedigoni, trazem um case da Magazine Luiza.
Para trabalhar com grafos persistentes foi decidido entre dois o neo4j e TITAN e baseado no CAP eles decidiram trabalhar com o Cassandra. Para interagir com o grafo eles escolheram o Gremlin, é uma DSL parte do tinkerPop que roda sobre a JVM. Para trabalhar com nós devemos criar os vertices, usando gremlin ficaria algo :
vert1 = g.addVertex();
vert1. tipo = “visitante”;
O gremlin permite configurar qual a direção que cada aresta esta ligada, imaginando recomendações do tipo “quem viu, também viu” teríamos o nó inicial o produto visitado pelo consumidor com arestas que apontam para cada sessão onde o cliente visitou e quais os outros produtos que ele viu. Após isso o gremlin começa a quantificar todas as vezes que este fluxo foi realizado e passa a quantificá-lo. Uma aresta final pode ser traçada que representaria o “quem viu, também viu”.
Fauno é um mecanismo de análise de gráficos baseados em Hadoop para analisar gráficos representados através de um cluster de computação multi-máquina. Ele permite usar a linguagem gráfica de travessia Gremlin e opera no banco de dados gráfico distribuído Titan, ou no HDFS através de vários formatos de texto e binários.
A empresa tem usado o Fauno, Rexster, cassandra e todas as demais tecnologias e divulgar todos os dados para a equipe de negócio que utiliza
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
- How Impala has Pushed HDFS in New Ways

- Hadoop and the Big Data Ecosystem
- Building a Data Science Program at NASA/JPL with Visual Analytics
- Data Science em Tempo Real com Storm
- How Impala has Pushed HDFS in New Ways