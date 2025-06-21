---
title: "Why UML Still Matters: A Shared Language for Software Design"
subtitle: "Introduction to UML modeling through practical mini-scenarios"
author: helio
layout: post
date: 2008-06-10T10:00:00+00:00
categories: ["Architecture", "Events"]
series: "UML Mini-scenarios"
tags:
  - mini-scenarios
  - uml-series
---

> **Series: UML Mini-scenarios** | **Introduction** > _Developed during Master's in Web Systems Projects_

Before we dive into the series of four mini-scenarios — **Web Classifieds**, **Betting Pool Control**, **Parking Lot Management**, and **Construction Control** — let's pause for a moment to understand _how_ we chose to describe them.

The answer: **UML** — Unified Modeling Language.

We don't use UML because it's trendy. We use it because it **forces precision**, **prevents ambiguity**, and **speeds up decision-making**.

> If a picture is worth a thousand words, a UML diagram is worth a hundred back-and-forths.

Across all scenarios, we use UML as a **common modeling tool**. Why? Because with it, even if you enter the conversation cold, you can quickly grasp what's happening, where the complexity lies, and what decisions are on the table.

This post sets the foundation — it introduces the types of diagrams and notations we use consistently across the series.

## What UML Brings to the Table

UML is not a methodology. It doesn't tell you _how_ to build your system. Instead, it gives you a **toolbox of diagrams** to express your system from different angles.

Here are the two main types we'll use throughout the series:

## Use Case Diagrams

Used in all four posts, these diagrams answer a simple question:
**What can users do with the system?**

- **Actors** (stick figures): represent people or systems interacting with your app.
- **Use cases** (ellipses): represent what the system offers.
- **Associations** (lines): link actors to use cases.
- **<<include>>**: means one use case always calls another. (e.g., "Publish Ad" includes "Register Contact")
- **<<extend>>**: shows optional/conditional logic. (e.g., "Highlight Ad" extends "Create Ad")

Use Case Diagrams are ideal for aligning **requirements with stakeholders**. They're not for technical depth — they're for shared understanding.

## Class Diagrams

Featured in the Web Classifieds scenario, class diagrams describe system **data structures** and **relationships**.

- **Classes** (rectangles): represent entities like `Ad`, `User`, `InterestSection`.
- **Attributes**: data each class holds (e.g., `email: String`).
- **Methods**: system behavior (e.g., `addInterest()`).
- **Associations**:
  - `1`, `0..1`, `0..*`: multiplicity (e.g., one ad can belong to multiple sections).
  - Arrows: direction and ownership of relationships.
- **Inheritance**: e.g., `FeaturedAd` inherits from `Ad`.

These diagrams are essential for **domain modeling**, **data modeling**, and architecture refinement.

## Why We Use UML in These Scenarios

Here's the truth: diagrams without standards create silos.

UML, when done right:

- **Enables faster onboarding**
- **Makes meetings efficient**
- **Bridges gaps between tech and product**
- **Documents architecture without becoming prose-heavy**

You don't need to use all UML diagrams. You don't even need a UML tool. Just stick to the **notation and structure** — even hand-drawn diagrams can do the job.

## What's Next

Over the next four posts, we'll walk through:

1. A **web-based classifieds system** with subscribers and paid ads
2. A **betting pool tracker** for lottery coordination
3. A **construction control system** with price history and comparisons
4. A **parking lot manager** with ticket printing and billing

Each will follow the same modeling approach: use case diagrams for behavior, and when needed, class diagrams for structure.

By starting with UML, we guarantee that anyone reading can follow the logic — even if they've never seen the project before.

### **Series Navigation**

- **Current**: Introduction - Why UML Still Matters
- **Next**: [Part 1 - Web Classifieds](../2008-06-13-minicenario-classificados-na-web/)
- **Complete series**: [Web Classifieds](../2008-06-13-minicenario-classificados-na-web/) | [Betting Pool Control](../2008-06-17-minicenario-controle-de-bolao/) | [Construction Control](../2008-06-21-minicenario-controle-de-obras/) | [Parking System](../2008-06-25-diagrama-de-casos-de-uso-estacionamento/)

Stay tuned.
