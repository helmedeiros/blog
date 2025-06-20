---
title: "Real-time Data Science with Storm"
author: helio
layout: post
date: 2014-04-10T18:32:54+00:00
embed: 
seo_follow: 
seo_noindex: 
dsq_thread_id: 
categories: ["Technology", "Events"]
tags:
  - big data
  - data scientist
  - Fabiane Nardon
  - qconsp
  - storm
---

Today we know that we have a lot of data, and from there, we discover that this data isn't just a box with several others.

You apply statistical processors, something about artificial intelligence, and in the end, we have an output with the expected data.

In 2012, <a title="Fabiane Nardon @twitter" href="https://twitter.com/fabianenardon" target="_blank">Fabiane</a> applications were more or less like a pile of data that was processed in batches at the end.

It seems that for a long time, this processing or the need to relate them and process them was minor.

And as time went by, the age of the content decreased until it became "real-time".

When we think about processing in the "era of real-time", things are quite different from the "batch era".

The processing time may not be important, the output may not reflect current information, and processing is finite

 - batches come in, are processed, and end.

When we talk about "real-time", processing should be fast, the input is a stream, and it's usually infinite.

Imagine the difference in processing our past financial year, and how positive your social media campaigns are.

To make this happen, it's not possible to do so without thinking about scalability.

Imagining this scenario, Fabiane believes that you could think of <a title="Apache Storm" href="http://storm.incubator.apache.org/" target="_blank">Apache Storm</a>.

Storm is an Apache project since 2013, which can be used in commercial projects, scalable, fault-tolerant, and can be used with any programming language.

The Storm architecture consists of a stream, for example, an access log to web pages that are thrown into a <a title="Publish Subscriber" href="http://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern" target="_blank">PubSub</a> <a title="Redis" href="http://redis.io/" target="_blank">Redis</a>, read, and stored in cache; then we have the spout that is responsible for picking up these data from the stream and sending them to the bolts.

To create a spout in Java, you extend <a title="JavaDoc" href="https://storm.incubator.apache.org/apidocs/backtype/storm/topology/base/BaseRichSpout.html" target="_blank">BaseRichSpout</a> and implement the nextTuple method, which can pick up from pubsub and then emit using a collector; you still need to specify what data will be sent outside.

Next, we have the bolt that transforms the data, processes it, and produces a new stream, which can write to a database, etc.

To implement in Java, you extend <a title="Java Doc" href="https://storm.incubator.apache.org/apidocs/backtype/storm/topology/base/BaseRichBolt.html" target="_blank">BaseRichBolt</a> and implement the execute method to put your business rules.

Spouts and bolts are aggregated through topologies.

Topologies allow combining the number of spouts and bolts so that we can achieve the fastest possible processing by making parallelism.

Parallelism, as we know, can be something very risky, which is why Storm allows realizing types of aggregations, such as:

 1. **Shuffle grouping**:

Tuples are distributed randomly across all tasks in a way that each bolt is guaranteed to receive an equal number of tuples;

 2. <strong style="line-height: 1.5em">Fields grouping</strong><span style="line-height: 1.5em">:

The stream is divided by the specified fields in the aggregation.

For example, if the stream is aggregated by the "user-id" field, tuples with the same "user-id" will always go to the same task but with different tuples;</span>

 3. **All grouping**:

The stream is replicated across all tasks of the bolt.

Use this aggregation with caution.

 4. **Global grouping**:

The entire stream goes to a single task of the bolt.

Specifically, it goes to the task with the smallest ID.

 5. **None grouping**:

This aggregation specifies that you don't care how the stream is aggregated.

 6. **Direct grouping**:

A stream aggregated in this way means that the producer of the tuple decides which consumer will receive this tuple.

Direct aggregations can only be declared on streams that have been declared as direct streams;

 7. **Local or shuffle grouping**:

If the target bolt has one or more tasks in the same work process, tuples will be shuffled to only those tasks.

Otherwise, it acts like a normal shuffle. <span style="line-height: 1.5em">The data is large, constant creation, and necessary processing.

How do you process 1 million tuples per day?

Do you have this amount of data?

Do you really need to process them in real-time or can we do them in batches?

Consider the STORM!</span> Note that there are several texts throughout the translation, which should be replaced with actual values depending on the context.