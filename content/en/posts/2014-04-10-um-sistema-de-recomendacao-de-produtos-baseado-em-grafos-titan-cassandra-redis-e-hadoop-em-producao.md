---
title: "An Recommendation System for Products based on"
graphs: Titan, Cassandra, Redis and Hadoop in production"
author: helio
layout: post
date: 2014-04-10T21:27:50+00:00
url: /2014/04/10/um-sistema-de-recomendacao-de-produtos-baseado-em-grafos-titan-cassandra-redis-e-hadoop-em-producao/
embed: 
seo_follow: 
seo_noindex: 
dsq_thread_id: 
categories:
  - Eventos
tags:
  - big data
  - data scientist
---

Big data is like teenage sex: everyone talks about it, nobody really knows how to do it, everyone thinks everyone else is doing it, so everyone claims they are doing it..

The biggest companies are trying to find out and help the company figure out where the intersection is between what people want, and what the company wants people to buy.

In this context, [Andre Fatala][1] and [Renato Pedigoni][2], bring a case study from [Magazine Luiza][3].

To work with persistent <a title="Teoria dos Grafos" href="http://en.wikipedia.org/wiki/Graph_theory" target="_blank">grafos</a>, it was decided between two options: <a title="Neo4J" href="http://www.neo4j.org/" target="_blank">neo4j</a> and <a title="Titan" href="http://thinkaurelius.github.io/titan/" target="_blank">TITAN</a>, and based on <a title="Teorema CAP" href="http://en.wikipedia.org/wiki/CAP_theorem" target="_blank">CAP</a>, they decided to work with __HTML_Link_4__.

To interact with the graph, they chose <a title="Gremlin" href="https://github.com/tinkerpop/gremlin/wiki" target="_blank">Gremlin</a>, which is a <a title="DSL" href="http://en.wikipedia.org/wiki/Domain-specific_language" target="_blank">DSL</a> part of TinkerPop that runs on JVM.

To work with nodes, we need to create vertices using Gremlin, which would be something like: vert1 = g.addVertex(); vert1.type = "visitante"; Gremlin allows configuring the direction each edge is linked, imagining recommendations of the type "who saw, also saw".

We would have the initial node representing the product visited by the consumer, with edges pointing to each session where the customer visited and what other products they saw.

After that, Gremlin starts quantifying all the times this flow was executed and begins to quantify it.

A final edge can be drawn that represents "who saw, also saw". [Fauno][4] is a graph analysis mechanism based on Hadoop for analyzing graphs represented through a multi-machine computing cluster.

It allows using the Gremlin traversal language and operates on a distributed graph database Titan or on HDFS in various text and binary formats.

The company has used Fauno, <a title="rexster" href="https://github.com/tinkerpop/rexster/wiki" target="_blank">Rexster</a>, Cassandra, and all other technologies to reveal all data to the business team that uses it

[2]: http://qconsp.com/user/renato-pedigoni

[4]: http://thinkaurelius.github.io/faunus/ "Faunus"

[3]: http://www.magazineluiza.com.br/ "Magazine Luiza"

[1]: http://qconsp.com/user/andre-fatala