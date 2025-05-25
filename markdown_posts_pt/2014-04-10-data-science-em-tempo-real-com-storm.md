---
title: "Data Science em Tempo Real com Storm"
date: 2014-04-10
slug: data-science-em-tempo-real-com-storm
tags:
  - big-data
draft: false
language: pt
---

Hoje sabemos que temos um monte de dados, e dai descobrimos que estes dados não é só uma caixinha mais várias, você aplica processadores estatísticos, algo de inteligência artificial, e no final temos uma saída com os dados que são esperados.
Em 2012 as aplicações da Fabiane eram mais ou menos, um acumulo de dados e que no final estes eram processados em batch com uma saída. Parece que durante muito tempo este processamento ou a necessidade em relacioná-los e processá-los era menor. E com o tempo a idade do conteúdo era cada vez menor até que ela ficou em “tempo real”.
Quando pensamos em fazer processamento na “era do tempo real” as coisas são bem diferentes da “era em batch”. O tempo de processamento pode não ser importante, a saída pode não refletir informações atuais e o processamento é finito, os lotes entram, são processado e acabam. Quando falamos em “tempo real” o processamento deverá ser rápido a entrada é um stream e normalmente é infinito. Imagine a diferença em processar o nosso ano financeiro passado, e quão positivas estão sendo suas campanhas nas redes sociais.
Para que isso aconteça não é possível fazê-lo sem pensar em escalar. Imaginando este cenário, a Fabiane então acredita que você poderia pensar em Apache Storm.
O Storm é um projeto Apache desde 2013, podendo ser usado em projetos comerciais, escaláveis, tolerante a falhas e pode ser usada com qualquer linguagem de programação.
Fabiane Nardon Coding
A arquitetura do storm é composta de um Stream, por exemplo um log de acesso a paginas web que são jogados em um PubSub Redis, são lidos e armazenados em cache; em seguida temos o spout que é responsável por pegar estes dados do stream e enviá-los para os bolts. Para fazer um spout em java você extends BaseRichSpout e implementa os métodos nextTuple, que pode pegar lá do pubsub e depois emit usando um collector; você ainda precisa dizer quais os dados que serão enviados para fora.
Em seguida temos o bolt que transforma os dados, processa e produz uma nova stream, pode gravar no banco de dados e etc. Para implementar em java você extends BaseRichBolt e implementa o método execute para colocar suas regras de negócio.
Os Spouts e bolts são agregados por meio de topologias. As topologias permitem combinar a quantidade de spouts e bolts para que possamos conseguir que o trabalho seja feito o mais rápido possível se fazendo de paralelismo.
O paralelismo como sabemos pode ser algo bem perigoso, para isso o Storm permite realizar tipos de agupamentos, são eles:
1. Shuffle grouping : Tuplas são distribuídos aleatoriamente em toda as tarefas do parafuso de uma forma tal que cada bolt está garantido para obter um número igual de tuplas;
2. Fields grouping : O stream é dividido pelos campos especificados no agrupamento. Por exemplo, se o stream é agrupado pelo campo “user- id” , tuplas com o mesmo “user- id” sempre irá para a mesma tarefa , mas com diferentes tuplas;
3. All grouping : O stream é replicado em todas as tarefas do bolt . Utilize este agrupamento com cuidado.
4. Global grouping : Todo o stream vai para uma só das tarefas do bolt . Especificamente , ele vai para a tarefa com o menor id.
5. None grouping : Este agrupamento especifica que você não se importa como o stream é agrupado.
6. Direct grouping : Um stream agrupados desta forma significa que o produtor da tupla decide qual tarefa de o consumidor receberá esta tupla. Agrupamentos diretas só podem ser declaradas em streams que tenham sido declarados como streams diretos;
7. Local or shuffle grouping : Se o bolt alvo tem uma ou mais tarefas no mesmo processo de trabalho , tuplas serão embaralhadas para apenas aquelas tarefas em processo. Caso contrário, age como um agrupamento normais shuffle.

Os dados são grandes, sua criação constante e o processamento necessário. Como se processa 1 milhão de tupulas por dia? Você tem esta quantidade de dados? Você realmente precisa processá-los em tempo real ou podemos fazê-los em batch? Considere o STORM!
big-data
- __
- __
- __
- __
- __
- __

- Hadoop and the Big Data Ecosystem
- Building a Data Science Program at NASA/JPL with Visual Analytics
- How Impala has Pushed HDFS in New Ways
- Um Sistema de recomendação de produtos baseado em grafos: Titan, Cassandra, Redis e Hadoop em produção

- Hadoop and the Big Data Ecosystem
- Building a Data Science Program at NASA/JPL with Visual Analytics
- How Impala has Pushed HDFS in New Ways
- Um Sistema de recomendação de produtos baseado em grafos: Titan, Cassandra, Redis e Hadoop em produção