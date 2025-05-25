---
title: "Como a Impala Tem Empurrado o HDFS em Novas Direções"
date: 2014-04-10
slug: how-impala-has-pushed-hdfs-in-new-ways
draft: false
language: en
---

As Impala and Cloudera have helped the community over the years, nothing better than Aaron to talk about it committer of Hadoop, let's see how HDFS works, impala and how the latter has been modified to meet new requirements.

When people talk about Hadoop, a part is related to HDFS (Hadoop Distributed File System). This is used only as a distributed file system, it was unique and exclusively for working with large data blocks that need to be fast for good MapReduce performance.

Each HDFS cluster is composed of clusters with multiple nodes, they store metadata and data. There are block maps and file system metadata and these organize the entire access flow.
Impala is a general-purpose engine for processing queries in HQL (Hive Query Language), it works both for analytical processing and runtime execution. It runs distributedly in clusters, and we can submit queries with ODBC/JDBC.

When we deploy Impala to our environment what we have under the hood are two daemons, impalad and statestored. The impalad handles all client requests; the statestored deals with all necessary states for daemon functioning. Each request to Impala is made via odbc/jdbc, these requests are paused by means of execution plans.

Cloudera Impala architecture
What improvements have been brought by Impala to HDFS?
First, Impala is concerned with low-latency queries and for this not to exclude the fact that distributed scenarios, like co-located replicas blocked, local reading versus network speed. Impala added a feature specifying that a data set should know where its replicas are.
Currently disk throughput isn't as fast as we can access files in real-time processing with file weights, so Impala simplified HDFS reading directly from the main memory optimized.

By these and other improvements, Impala places 5-10x faster than Hive for simple queries and 20-50x for complex queries with joins.

big-data