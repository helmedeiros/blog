---
title: "A System of product recommendation based on graphs: Titan, Cassandra, Redis and Hadoop in production"
date: 2014-04-10
slug: um-sistema-de-recomendacao-de-produtos-baseado-em-grafos-titan-cassandra-redis-e-hadoop-em-producao
draft: false
language: en
---

Big data is like teenage sex: everyone talks about it, nobody really knows how to do it, everyone thinks everyone else is doing it, so everyone claims they are doing it..
The largest companies are trying to discover and help the company at the intersection between what people want, and what the company wants them to buy. In this context, Andre Fatala and Renato Pedigoni bring a case from Magazine Luiza.
To work with persistent graphs, it was decided between two options: Neo4j and TITAN, and based on CAP they decided to work with Cassandra. To interact with the graph, they chose Gremlin, which is a DSL part of TinkerPop that runs on JVM. To work with nodes, we must create vertices, using Gremlin it would be something:
vert1 = g.addVertex();
vert1.type = "visitante";
Gremlin allows configuring what direction each edge is linked, imagining recommendations like "who saw, also saw" we would have the initial node as the product visited by the consumer with edges pointing to each session where the client visited and which other products he saw. After that Gremlin starts quantifying all times this flow was performed and begins to quantify it. A final edge can be drawn representing the "who saw, also saw".
Fauno is a graph analysis mechanism based on Hadoop for analyzing graphs represented through a multi-machine computing cluster. It allows using the graphical traversal language Gremlin and operates on the distributed graph database Titan, or on HDFS through various text and binary formats.
The company has used Fauno, Rexster, Cassandra, and all other technologies to disseminate all data to the business team that uses big-data
- Hadoop and the Big Data Ecosystem
- Building a Data Science Program at NASA/JPL with Visual Analytics
- Data Science in Real-Time with Storm
- How Impala has Pushed HDFS in New Ways
- Hadoop and the Big Data Ecosystem
- Building a Data Science Program at NASA/JPL with Visual Analytics
- Data Science in Real-Time with Storm
- How Impala has Pushed HDFS in New Ways