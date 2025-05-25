---
title: "Como a Impala tem Empurrado o HDFS Novas Direções How Impala has Pushed HDFS in New Ways ("
author: helio
layout: post
date: 2014-04-10T16:05:02+00:00
embed: 
seo_follow: 
seo_noindex: 
categories:
  - Eventos
tags:
  - aaron myers
  - cloudera
  - impala
  - qconsp
---

As Impala and the [Cloudera][1] have helped the community over the past few years, nothing better than the <a title="Aaron Myers" href="https://twitter.com/atm" target="_blank">Aaron</a> to talk about it with <a title="Hadoop" href="http://hadoop.apache.org/" target="_blank">Hadoop</a>, let's see how it works with <a title="HDFS" href="http://hadoop.apache.org/docs/r1.2.1/hdfs_design.html" target="_blank">HDFS</a>, and how the latter has been modified to meet new requirements.

When people talk about Hadoop, a part of this is tied to HDFS (Hadoop Distributed File System).

This is used only as a distributed file system; it was unique and exclusively for working with large data blocks that need to be fast for good performance with <a title="MapReduce" href="http://en.wikipedia.org/wiki/MapReduce" target="_blank">MapReduce</a>.

Each HDFS cluster is composed of clusters with multiple nodes, which store metadata and data.

There are block maps and file system metadata that organize the entire access flow.

The <a title="Impala" href="http://en.wikipedia.org/wiki/Cloudera_Impala" target="_blank">Impala</a> is a general-purpose engine for query processing in HQL (Hive Query Language), it works for both analytical processing and real-time execution.

It runs distributed across clusters, and we can submit queries with <a title="Open Database Connectivity" href="http://en.wikipedia.org/wiki/ODBC" target="_blank">ODBC</a>/<a title="Java Database Connectivity" href="http://en.wikipedia.org/wiki/JDBC" target="_blank">JDBC</a>.

When we deploy Impala in our environment, what's behind the scenes are two daemons: impalad and _statestored_.

The _impalad_ handles all client requests; the _statestored_ deals with all necessary states for the operation of the _daemons_.

Each request to _Impala_ is made via odbc/jdbc_; these requests are paused by means of execution plans. <figure id="attachment_831" style="width: 468px" class="wp-caption aligncenter"> [<img class="size-full wp-image-831" alt="arquitetura da cloudera impala" src="/uploads/2014/04/cloudera_impala.jpg" width="468" height="240" srcset="/uploads/2014/04/cloudera_impala.jpg 468w, /uploads/2014/04/cloudera_impala-300x153.jpg 300w" sizes="(max-width: 468px) 100vw, 468px" />][2]<figcaption class="wp-caption-text">Cloudera Impala architecture</figcaption></figure> What are the improvements brought by Impala to HDFS?

First, Impala is concerned with low-latency queries and for this, it doesn't exclude distributed scenarios, such as co-located replicas blocked, by local reading versus network speed.

Impala added a feature that specifies where a data set should know its replicas.

Currently, disk throughput isn't as fast as we can access them to process files in real-time, with the weight of files, and for this _Impala_ has optimized HDFS to read directly from main memory.

By these and other improvements _Impala_ puts itself 5-10x faster than <a title="Hive" href="http://hive.apache.org/" target="_blank"><em>Hive</em></a> for simple queries and 20-50x for complex queries with joins.

[2]: /uploads/2014/04/cloudera_impala.jpg

[1]: http://www.cloudera.com/content/cloudera/en/home.html "cloudera"