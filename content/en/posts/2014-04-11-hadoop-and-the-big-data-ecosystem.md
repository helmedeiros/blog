---
title: Hadoop and the Big Data Ecosystem
author: helio
layout: post
date: 2014-04-11 13:36:05+00:00
embed: null
seo_follow: null
seo_noindex: null
dsq_thread_id: null
categories:
  - Technology
  - Agile
tags:
  - big data
  - hadoop
  - qconsp
  - Todd Lipcon
subtitle: Navigate the Hadoop ecosystem evolution—from Google's MapReduce origins to modern frameworks like Spark, Sqoop, and Flume that handle terabytes of data with KISS principles
---

Why should we worry?

That's how it started with the keynote from <a title="Todd Lipcon" href="https://twitter.com/tlipcon" target="_blank">Todd Lipcon</a>...

Perhaps because over the last few years, companies have seen an explosion in volume, variety, and speed of data that they need to handle every day.

This has been a blessing and a curse.

At the same time that the data explosion allowed us to generate new types of applications and highly intelligent insights, developers found that the previous generation of data management tools and frameworks collapsed when trying to work with terabytes or petabytes of often poorly structured data.

When Todd was a child, he found a program that pretended to be a person answering questions, and after asking some questions, he discovered that the program was very stupid.

Presenting it to his father, he was challenged, tried to improve it but couldn't go too far with his age.

Twenty years later, he saw the <a title="Watson" href="http://en.wikipedia.org/wiki/Watson_(computer)" target="_blank">watson</a> responding to all these questions... the difference? <a title="Big Data" href="http://en.wikipedia.org/wiki/Big_data" target="_blank">Big data</a>!!

Going back a bit in time, he started showing the first steps of a path that passed through recursive and sluggish indexing and no doubt about proprietary equipment and software from large companies.

This started to change with Google; they created their own storage and infrastructure processing.

The <a title="MapReduce" href="http://en.wikipedia.org/wiki/MapReduce" target="_blank">MapReduce</a> emerged based on the premise of <a title="Keep it simple stupid" href="http://en.wikipedia.org/wiki/KISS_principle" target="_blank">KISS</a>.

These technologies are still fully operational until today, they never sold them but wrote several papers that gave rise to various laws that are out there.

The <a title="Hadoop" href="http://hadoop.apache.org/" target="_blank">Hadoop</a> emerged later with <a title="Doug Cutting" href="https://twitter.com/cutting" target="_blank">Doug Cutting</a>, which had similar problems to those Google had, reading Google's papers found a good strategy for working with large files in a distributed manner.

Hadoop is a scalable data storage and processing system that can work on any machine.

The machines within the Hadoop scheme are known as nodes, and processing these distributed data on nodes is completely transparent, as if there were no real distinction between local and remote.

One of the fundamental parts of Hadoop is the <a title="Hadoop Distributed File System" href="http://hadoop.apache.org/docs/r1.2.1/hdfs_design.html" target="_blank">HDFS</a>, which allows us to work with large files by dividing them into blocks of maximum size and replicating them so that they can allow redundancy, to avoid information loss or interruption in processing in case of failures.

Another fundamental part is MapReduce, a programming model that has two main parts: instructions for performing transformations, parsing, or filtering data, which always runs before and always returns results; and instructions for summarizing data.

These instructions bring great simplicity to daily work processing one record at a time, without the need to perform explicit I/O and it is well scalable.

At this moment, Todd presented a MapReduce example on a simple domain, counting words in the children's song below, going into details on how we could conquer speed for this model by implementing Hadoop's MapReduce. > Soft kitty, > Warm kitty, > Little ball of fur. > Happy kitty, > Sleepy kitty, > Purr Purr Purr Some frameworks were mentioned:

<p style="padding-left: 30px">
 <strong><a title="Apache Spark" href="http://spark.apache.org/" target="_blank">Spark</a>:</strong> is a framework that works with MapReduce, supports multiple languages, and has an interactive shell.

Comparing codes made in Hadoop and Spark, we have a reduction of 10x in the number of lines required.

The gains also go in terms of processing speed;

</p>

<p style="padding-left: 30px">
 <strong><a title="Apache Sqoop" href="http://sqoop.apache.org/" target="_blank">Sqoop</a>:</strong> will facilitate efficient exchange of large amounts of data between Apache Hadoop and structured data storage, such as relational databases;
</p>

<p style="padding-left: 30px">
 <span style="line-height: 1.5em"><strong><a title="Apache Flume" href="http://flume.apache.org/" target="_blank">Flume</a>:</strong> allows importing data to the HDFS while it is generated on any number of machines.</span>
</p>
 <figure id="attachment_849" style="width: 468px" class="wp-caption aligncenter"> [<img class="size-full wp-image-849" alt="Reducing Soft kitties!!" src="/uploads/2014/04/mapreduce.jpg" width="468" height="240" srcset="/uploads/2014/04/mapreduce.jpg 468w, /uploads/2014/04/mapreduce-300x153.jpg 300w" sizes="(max-width: 468px) 100vw, 468px" />][1]<figcaption class="wp-caption-text">Reducing Soft kitties!!</figcaption></figure>

[1]: /uploads/2014/04/mapreduce.jpg
