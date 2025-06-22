---
title: "Caelum Day in Rio – Part 4: NoSQL with Nico Steppat"
date: 2009-11-11T14:00:00+00:00
draft: false
author: Helio Medeiros
subtitle: "Challenge everything you know about data storage—explore the revolutionary NoSQL movement that abandons ACID guarantees for massive scale, flexibility, and performance in the emerging big data era"
tags:
  [
    "Caelum Day",
    "NoSQL",
    "Nico Steppat",
    "CouchDB",
    "MongoDB",
    "Redis",
    "Cassandra",
    "Neo4j",
    "Database",
    "Scalability",
    "Document Database",
    "Key-Value Store",
    "Graph Database",
    "Series",
    "Rio de Janeiro",
  ]
categories: ["Events", "Technology", "Database", "NoSQL"]
series: "Caelum Day 2009"
---

> **Series: Caelum Day 2009** | **Part 4 of 7** > _Comprehensive coverage of cutting-edge talks from Rio's premier Java event_

**Continuing the Caelum Day in Rio series**, today I'm writing about **Nico Steppat's** presentation that completely challenged everything I thought I knew about databases. As someone who's only worked with **MySQL, Oracle, and PostgreSQL**, hearing about "NoSQL" was like discovering a parallel universe.

## Wait, "No SQL"? Really?

Nico started by clearing up the confusion - "NoSQL" doesn't mean "no SQL," but rather **"not only SQL."** The idea is to use different types of databases when the traditional relational model just doesn't fit your problem.

This makes perfect sense when you think about modern applications - social networks with millions of users, recommendation engines, real-time analytics. The rigid table structure that works great for accounting software might not be the best fit for everything.

## Types of NoSQL That Blew My Mind

Nico explained the main categories, and each one sounds like it could solve problems I've been struggling with:

- **Document-oriented (CouchDB, MongoDB)** — Store data as flexible JSON-like documents instead of rigid rows
- **Key-value stores (Redis, Riak)** — Lightning fast lookups, perfect for caching and session data
- **Columnar (Cassandra, HBase)** — Inspired by Google's BigTable, designed for massive datasets
- **Graph databases (Neo4j)** — Built specifically for highly connected data like social networks

## This Changes Everything

What really got me thinking:

- You can **model for how you read data**, not just how you store it efficiently
- Companies like Facebook, Twitter, and Amazon are already betting big on these technologies
- **Consistency doesn't always have to be immediate** — sometimes "eventually consistent" is good enough

This last point really challenges the ACID mindset I've been trained on.

## So Many Questions

The talk was more about opening minds than diving deep into implementation, which I think was perfect. I left with a head full of questions:

- When should I choose NoSQL over traditional relational databases?
- Could I use different types of databases for different parts of the same application?
- How do you even test and deploy something that doesn't have a fixed schema?
- What about data integrity and transactions?

## Ready to Experiment

I'm definitely going to set up MongoDB or CouchDB on my laptop and try modeling some data differently. Not to replace everything I know about SQL, but to understand when and how these tools might be useful.

The examples Nico showed of document-based storage for content management systems were particularly compelling.

**Next up in this series:** Rafael Martinelli's talk on Flex at DClick!

---

### **Series Navigation**

- **Introduction**: [Caelum Day Overview](../2009-11-07-caelum-day-intro/)
- **Previous**: [Part 3 - RESTful APIs](../2009-11-10-caelum-day-part3-restful-apis/)
- **Current**: Part 4 - NoSQL Databases
- **Next**: [Part 5 - Flex Framework](../2009-11-12-caelum-day-part5-flex/)
- **Complete series**: [Cloud Computing](../2009-11-08-caelum-day-part1-cloud-fabio-kung/) | [VRaptor 3](../2009-11-09-caelum-day-part2-vraptor3/) | [RESTful APIs](../2009-11-10-caelum-day-part3-restful-apis/) | [Flex](../2009-11-12-caelum-day-part5-flex/) | [Java Persistence](../2009-11-13-caelum-day-part6-java-persistence/) | [Technical Leadership](../2009-11-14-caelum-day-final-leadership-phillip-calcado/)
