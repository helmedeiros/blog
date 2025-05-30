---
title: "Caelum Day in Rio – Part 4: NoSQL with Nico Steppat"
date: 2009-11-11T14:00:00+00:00
draft: false
author: Helio Medeiros
subtitle: "Discovering the world of Not Only SQL databases"
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

Continuing the Caelum Day in Rio series, today I'm writing about **Nico Steppat's** presentation, which introduced many of us (myself included) to the world of **NoSQL**.

## Why "NoSQL"?

Nico began by clarifying that "NoSQL" doesn't mean "no SQL," but rather **"not only SQL."** The goal is to use non-relational databases when the relational model doesn't fit the problem.

That made a lot of sense in scenarios involving high scalability and performance needs — like social networks, recommendation engines, or any system with massive read/write operations.

Until then, I had mostly worked with relational databases like **MySQL, Oracle, SQL Server, and PostgreSQL**. This was my first time seeing serious alternatives explained.

## Categories of NoSQL Databases

Nico laid out the main types of NoSQL systems:

- **Document-oriented (e.g., CouchDB, MongoDB)** — Store data as flexible JSON or XML documents.
- **Key-value stores (e.g., Redis, Riak)** — Lightning fast and great for caching or session state.
- **Columnar (e.g., Cassandra, HBase)** — Inspired by Google's BigTable, optimized for huge datasets.
- **Graph databases (e.g., Neo4j)** — Built for relationships, ideal for things like social networks.

## What Caught My Attention

- The idea of **modeling for efficient reads**, not strict normalization.
- That many major companies already rely on these databases — like Facebook, Twitter, Amazon.
- And that **consistency can be eventual**, configurable, or even optional — which breaks away from the ACID mindset.

## I Left With More Questions Than Answers (And That's Great)

The talk wasn't too technical, and that was the point. It challenged me to ask:

- Is my relational model always the right fit?
- Could I use NoSQL for specific parts of a system?
- How do you test and version something that's schema-less?

## Ready to Try It Out

I want to take a side project with lots of reads and try modeling it in MongoDB or CouchDB. Not to replace SQL — but to see what it's like thinking this way.

**Next up in this series:** Rafael Martinelli's talk on Flex at DClick!
