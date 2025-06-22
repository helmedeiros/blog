---
title:
  "Um Sistema de recomendação de produtos baseado em grafos: Titan, Cassandra,
  Redis e Hadoop em produção"
author: helio
layout: post
date: 2014-04-10 21:27:50+00:00
embed:
  - This is the default text
seo_follow:
  - "false"
seo_noindex:
  - "false"
dsq_thread_id:
  - 4969855984
categories:
  - Technology
  - Leadership
  - Events
tags:
  - big data
  - data scientist
subtitle: Construa sistemas de recomendação prontos para produção usando bancos de dados de grafos—implementando Titan, Cassandra, Redis e Hadoop com travessias Gremlin para descobrir padrões "quem viu, também viu" em escala
---

> Big data is like teenage sex: everyone talks about it, nobody really knows how to do it, everyone thinks everyone else is doing it, so everyone claims they are doing it..

As maiores empresas estão tentando descobrir e ajudar a empresa a a interseção entre oque as pessoas querem, e o que a empresa quer que as pessoas comprem. Neste contexto o [Andre Fatala][1] e o [Renato Pedigoni][2], trazem um case da [Magazine Luiza][3].

Para trabalhar com <a title="Teoria dos Grafos" href="http://en.wikipedia.org/wiki/Graph_theory" target="_blank">grafos</a> persistentes foi decidido entre dois o <a title="Neo4J" href="http://www.neo4j.org/" target="_blank">neo4j</a> e <a title="Titan" href="http://thinkaurelius.github.io/titan/" target="_blank">TITAN</a> e baseado no <a title="Teorema CAP" href="http://en.wikipedia.org/wiki/CAP_theorem" target="_blank">CAP</a> eles decidiram trabalhar com o <a title="Casandra" href="http://cassandra.apache.org/" target="_blank">Cassandra</a>. Para interagir com o grafo eles escolheram o <a title="Gremlin" href="https://github.com/tinkerpop/gremlin/wiki" target="_blank">Gremlin</a>, é uma <a title="DSL" href="http://en.wikipedia.org/wiki/Domain-specific_language" target="_blank">DSL</a> parte do tinkerPop que roda sobre a JVM. Para trabalhar com nós devemos criar os vertices, usando gremlin ficaria algo :

vert1 = g.addVertex();

vert1. tipo = &#8220;visitante&#8221;;

O gremlin permite configurar qual a direção que cada aresta esta ligada, imaginando recomendações do tipo &#8220;quem viu, também viu&#8221; teríamos o nó inicial o produto visitado pelo consumidor com arestas que apontam para cada sessão onde o cliente visitou e quais os outros produtos que ele viu. Após isso o gremlin começa a quantificar todas as vezes que este fluxo foi realizado e passa a quantificá-lo. Uma aresta final pode ser traçada que representaria o &#8220;quem viu, também viu&#8221;.

[Fauno][4] é um mecanismo de análise de gráficos baseados em Hadoop para analisar gráficos representados através de um cluster de computação multi-máquina. Ele permite usar a linguagem gráfica de travessia Gremlin e opera no banco de dados gráfico distribuído Titan, ou no HDFS através de vários formatos de texto e binários.

A empresa tem usado o Fauno, <a title="rexster" href="https://github.com/tinkerpop/rexster/wiki" target="_blank">Rexster</a>, cassandra e todas as demais tecnologias  e divulgar todos os dados para a equipe de negócio que utiliza

&nbsp;

[1]: http://qconsp.com/user/andre-fatala
[2]: http://qconsp.com/user/renato-pedigoni
[3]: http://www.magazineluiza.com.br/ "Magazine Luiza"
[4]: http://thinkaurelius.github.io/faunus/ "Faunus"
