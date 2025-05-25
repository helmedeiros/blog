---
title: "Big Data ecosystem Hadoop."
date: 2014-04-11
slug: hadoop-and-the-big-data-ecosystem
draft: false
language: en
---

Why should we worry? That's how Todd Lipcon started his keynote... Maybe because over the past few years, companies have seen an explosion in the volume, variety, and speed of data they need to handle every day. This has been a blessing and a curse. On the one hand, the data explosion allowed us to generate new types of applications and highly intelligent insights, but developers found that the previous generation of data management tools and frameworks collapsed when trying to work with terabytes or petabytes of often poorly structured data.

When Todd was a kid, he found a program that pretended to be a person answering, and after asking some questions, he discovered that the program was very dumb. He presented it to his father, who challenged him to improve it, but at that age, he couldn't go very far ahead. Twenty years later, he saw Watson responding to all these questions... the difference? Big data!!

Going back in time a bit, he started showing the first steps of a path that passed through recursive and slow indexing without any shadow of doubt by proprietary equipment and software from large companies.

That's when Google came along and created its own storage and infrastructure for processing, MapReduce emerged based on the KISS premise. These technologies are still going strong to this day; they never sold them, but wrote several papers that gave rise to many laws that are out there.

Hadoop emerged later with Doug Cutting, who had similar problems to those Google had, reading Google's papers and finding a good strategy for working with large files in a distributed manner.

Hadoop is an scalable data storage and processing system that can work on any hardware. The machines inside the Hadoop scheme are known as nodes, and processing these distributed data on nodes is completely transparent, as if there were no real distinction between local and remote.

One of the fundamental parts of Hadoop is HDFS; it allows us to work with large files by breaking them down into blocks of maximum size and replicating them so they can allow for redundancy, to prevent information loss or interruption in processing in case of failures.

Another fundamental part is MapReduce, a programming model that has two main parts: instructions to perform transformations, parsing, or filtering data, which always runs before and always returns results; and instructions to summarize the data. These instructions bring a lot of simplicity to daily work processing one record at a time, there is no need to explicitly perform I/O and it's well scalable.

Reducing Soft kitties!!

At this moment Todd presented a MapReduce on a simple domain for counting words in the children's song below, going into details on how we could conquer speed for this model by implementing Hadoop's MapReduce.

> Soft kitty, Warm kitty, Little ball of fur. Happy kitty, Sleepy kitty, Purr Purr Purr

Some frameworks were mentioned:
Spark: it's a framework that works with MapReduce, supports multiple languages and has an interactive shell. Comparing codes for Maps made in Hadoop and with Spark we have a reduction of 10x in the number of lines necessary. The gains also go in terms of processing speed;
Sqoop: facilitates efficient data transfer between Apache Hadoop and structured storage systems such as relational databases;
Flume: allows importing data to HDFS while it's being generated on any number of machines.

big-data
- Building a Data Science Program at NASA/JPL with Visual Analytics
- Real-time Data Science with Storm
- How Impala has Pushed HDFS in New Ways
- A Product Recommendation System based on Graphs: Titan, Cassandra, Redis and Hadoop in Production
- Building a Data Science Program at NASA/JPL with Visual Analytics
- Real-time Data Science with Storm
- How Impala has Pushed HDFS in New Ways
- A Product Recommendation System based on Graphs: Titan, Cassandra, Redis and Hadoop in Production