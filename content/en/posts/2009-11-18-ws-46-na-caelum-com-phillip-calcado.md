---
title: "WS-46 with Phillip Calçado: My First True Dive into Domain-Driven Design"
author: helio
layout: post
date: 2009-11-18 23:37:20+00:00
dsq_thread_id: null
categories:
  - Architecture
tags:
  - Caelum
  - DDD
  - Domain-Driven Design
  - Phillip Calçado
  - Rio
  - WS-46
  - Modeling
  - Ubiquitous Language
  - Architecture
subtitle: Transform your modeling mindset with a DDD master—discover how Phillip Calçado's workshop reveals the power of ubiquitous language, domain modeling, and thinking beyond code patterns
---

On November 17, 2009, I finally joined a workshop that felt like a turning point in my career as a developer. I attended **Caelum's WS-46 training** on Domain-Driven Design (DDD) led by none other than **Phillip Calçado** — a name I had followed for years through his blog and talks.

This wasn't a workshop about frameworks or Java syntax. It was about **how to think, model, and communicate when building software for real businesses**. And for someone like me, deeply interested in clean code, design patterns, and object-oriented programming — but with no prior mentorship in DDD — it was a crash course in a different way of seeing systems.

## The Opening: What, How, and Which?

Phillip began the course not with patterns, but with three deceptively simple questions:

- **What** are we building?
- **How** are we expected to build it?
- **Which** trade-offs are acceptable?

This approach framed the workshop and made it clear that design starts with understanding—not code. We were grouped into teams to model a real-world system (a parking lot), based only on user stories. No pre-made classes. No diagrams. Just conversations and decisions.

## Language is the Model

One of the most repeated concepts in the workshop was the **Ubiquitous Language**. It's not a fancy glossary — it's a discipline of making every class name, method, and diagram reflect a shared language between developers and domain experts.

Phillip quoted from Eric Evans and stressed that a model is only useful if it's **implemented in code and spoken in meetings**. Without this, we fall back into translating specs and code, which leads to bugs and misunderstandings.

> "The greatest value of a domain model is that it provides a language to connect developers and business experts."

## The Modeling Sprint

For four hours, we worked only on domain modeling. No code, no patterns. Just sketching, refining, renaming, and arguing over concepts. Only _after_ we had some shared understanding did we introduce building blocks like:

| Building Block | Purpose                                                |
| -------------- | ------------------------------------------------------ |
| Entity         | Object with identity that evolves over time            |
| Value Object   | Stateless, immutable object defined by attributes      |
| Aggregate      | Cluster of associated objects, governed by a root      |
| Repository     | Interface to access and store aggregates               |
| Service        | Operation that doesn't naturally fit a specific entity |

## Lifecycle, Identity, and the Fake ID Problem

Phillip showed us the risks of designing entities without real identity. He referenced his classic post ["Don't Trust Fake IDs"](http://philcalcado.com/2009/10/12/dont-trust-fake-ids/) and explained the consequences of letting databases dictate our design.

> "If you don't know who an object is without the database, it's not an entity — it's just a row."

This sparked big debates in our group. Should a `ParkingTicket` be an entity or a value object? It depended on the behavior we wanted to model — and _that_ was the lesson.

## Layered Architecture in Practice

We explored a classic DDD layering structure, but emphasized behavior and flow over frameworks:

| Layer          | Role                                                     |
| -------------- | -------------------------------------------------------- |
| Domain         | Contains the heart of business logic and invariants      |
| Application    | Coordinates use cases and domain interaction             |
| Infrastructure | Interfaces to technical concerns: database, queues, APIs |
| Presentation   | UI, REST, messaging                                      |

Phillip was skeptical of overengineering. He insisted we add a layer only if it served the **domain clarity**, not just because a book or framework said so.

## When You Can't Talk About DDD

One brilliant takeaway was that **you don't need to name the patterns** to apply DDD. Phillip often avoids saying "Entity" or "Aggregate" on client teams. Instead, he helps model object lifecycles and responsibilities naturally.

This was liberating. I could start using DDD _without waiting for a greenfield project_ or a team fluent in the jargon.

## What the Industry Gets Wrong

Inspired by his blog post ["Nevermind Domain-Driven Design"](https://philcalcado.com/2010/03/22/nevermind_domain_driven_design.html), Phillip explained how the industry obsesses over repositories and anti-corruption layers — while ignoring the **core idea** of language and model alignment.

This led to my favorite quote of the day:

> "If all you got from DDD was a Repository class, you missed the point."

## Example: A Parking Lot System (UML)

Here's a simplified version of the model we refined during the workshop:

![Parking Lot Domain Model](https://yuml.me/diagram/scruffy/class/[ParkingLot]1-*%3E[Slot],[Slot]0..1-%3E[Vehicle],[ParkingTicket]^-[ValueObject],[Customer]1-*%3E[ParkingTicket])

The discussion about whether `ParkingTicket` was a value object or entity taught us to always ask: **What do we want to guarantee about this object in our domain?**

## Design as Conversation

More than code, DDD became about conversations. What we name a class, how we validate input, when we expose methods — all of it reflects what we understand from the domain expert.

I began to see code less as instructions and more as **documentation of understanding**. DDD forces us to keep asking _why_ something exists in the model.

## Final Thoughts

This was one of the best technical workshops I ever attended. Not because of the slides (there weren't many) or tools (we barely touched an IDE). But because it gave me **a way to think and model** — not just code.

Phillip was generous, funny, patient, and always tying theory back to practice. He proved that DDD is not a religion or silver bullet. It's a mindset — one that starts with listening and naming, not coding.

If you ever have the chance to learn with him, don't miss it.

---

_Posted the day after the WS-46 training in Rio. Still buzzing with ideas._
