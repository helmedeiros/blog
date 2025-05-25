---
title: "Real-time Data Science with Storm"
date: 2014-04-10
slug: data-science-em-tempo-real-com-storm
draft: false
language: en
---

Today we know that we have a lot of data, and then we discover that these data aren't just a box or two, you apply statistical processors, something of artificial intelligence, and in the end we have an output with the expected data.

In 2012 Fabiane's applications were more or less just a pile of data, which was processed in batches with an output. It seems that for a long time, this processing or the need to relate and process them was smaller. And over time, the age of the content decreased until it became "real-time".

When we think about doing processing in "real-time" things are quite different from "batch". The processing time may not be important, the output may not reflect current information, and processing is finite, batches enter, are processed and end. When we talk about "real-time", processing should be fast, input is a stream and usually infinite. Imagine the difference in processing our past financial year, and how positive your social media campaigns are.

For this to happen it's not possible without thinking of scaling. Imagining this scenario, Fabiane believes you could think of Apache Storm.

Storm is an Apache project since 2013, which can be used in commercial projects, scalable, fault-tolerant, and can be used with any programming language.

Fabiane Nardon Coding
The Storm architecture is composed of a Stream, for example, an access log to web pages that are thrown into a PubSub Redis, read and stored in cache; then we have the spout that is responsible for picking up these data from the stream and sending them to the bolts. To make a spout in Java, you extend BaseRichSpout and implement the methods nextTuple, which can pick it up from pubsub and then emit using a collector; you also need to say what data will be sent outside.

Then we have the bolt that transforms the data, processes it, and produces a new stream, can write to a database and etc. To implement in Java, you extend BaseRichBolt and implement the execute method to put your business rules.

The Spouts and bolts are aggregated through topologies. Topologies allow us to combine the number of spouts and bolts so that we can achieve the fastest possible work, making parallelism.

Parallelism as we know can be something quite dangerous, for this Storm allows performing types of aggregations, which are:

1. Shuffle grouping: Tuples are distributed randomly throughout all tasks in a way that each bolt is guaranteed to get an equal number of tuples;
2. Fields grouping: The stream is divided by the specified fields in the aggregation. For example, if the stream is aggregated by the "user-id" field, tuples with the same "user-id" will always go to the same task, but with different tuples;
3. All grouping: The stream is replicated throughout all tasks of the bolt. Use this aggregation with care.
4. Global grouping: The entire stream goes to a single task of the bolt. Specifically, it goes to the task with the smallest ID.
5. None grouping: This aggregation specifies that you don't care how the stream is aggregated.
6. Direct grouping: A stream grouped in this way means that the producer of the tuple decides which consumer will receive this tuple. Direct aggregations can only be declared on streams that have been declared as direct streams;
7. Local or shuffle grouping: If the target bolt has one or more tasks in the same work process, tuples will be shuffled to only those tasks in process. Otherwise, it acts like a normal shuffle.

Data is large, constant creation and necessary processing. How do you process 1 million tuples per day? Do you have this amount of data? Do you really need to process them in real-time or can we make them batch? Consider STORM!

big-data