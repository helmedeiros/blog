---
title: "Domain-Driven Design in Practice: Building Software That Speaks Business"
author: helio
layout: post
date: 2010-05-15T14:30:22+00:00
description: "Reflections on the eleventh and final Software Engineering lecture, exploring Domain-Driven Design principles and their practical application in real-world software development."
categories:
  - Architecture
  - Design
  - DDD
  - Education
tags:
  - Software Engineering
  - Domain-Driven Design
  - Architecture
  - Modeling
  - Business Logic
  - Ubiquitous Language
  - UnP
  - Teaching
  - software-engineering-series
---

> **Series: Software Engineering Fundamentals** | **Part Part 11 of 19** > _Delivered at Universidade Potiguar (UnP) in 2010_

**In the eleventh lecture** of the Software Engineering course at Universidade Potiguar (UnP), we marked a shift in tone: we weren't just modeling anymore—we were confronting the complexity of real systems head-on. It was time to give code a backbone, a shared language, and a strategy for evolution. That's where **Domain-Driven Design (DDD)** enters the room.

## Modeling Isn't Drawing. It's Deciding.

We kicked off with the CRC-like technique (Class–Responsibility–Collaboration), a fast and informal method to sketch out how responsibilities get distributed across objects. I gave the class concrete user stories—like "register a vehicle's entry at the parking lot"—and asked them to model it under time constraints.

These activities are more than drawings. They're about **decision-making**: What matters in this scenario? What doesn't? Which classes do I need? What should stay outside the domain model? For many students, this was the first time they realized modeling wasn't about the best design—but about the clearest decision.

Facilitators can apply this by framing the modeling activity not as a drawing session, but as a negotiation of meaning. Ask your team: "What are we really trying to say here?"

## Choosing the Right Architectural Form

As we looked at different architectural approaches—**Table Module**, **Transaction Script**, and **Domain Model**—we discussed not only what they are, but when to use them. This wasn't a purity test. It was an exercise in fit-for-purpose thinking.

Students were prompted to map the decision levels in three dimensions: _What to do?_, _How to do it?_, and _With what structure?_ That's where we explored the Layered Architecture pattern: dividing software into Presentation, Application, Domain, and Infrastructure layers.

We used a small exercise to have each group reflect on how they'd move a feature from one layer to another if a business rule changed. The point wasn't to memorize patterns—it was to **build movement** into the architecture.

## Layers That Mean Something

Most devs hear "layered architecture" and picture rectangles in a PowerPoint. I wanted my students to see them as **communication channels**. The Application layer, for example, doesn't do business logic—it coordinates. The Domain layer doesn't care about databases—it embodies meaning.

I introduced how DDD encourages a clean layering structure and added an extra twist: each group had to **simulate a change** in business logic (e.g., switch pricing strategy) and outline which layers would be impacted and why. This simple "domino exercise" clarified dependencies and separation of concerns better than a diagram ever could.

## The Power of Ubiquitous Language

We turned to language. In DDD, **ubiquitous language** isn't a nice-to-have. It's the backbone. We examined how messy terminology ("syntactic noise" or "semantic noise") can kill clarity—even if the code compiles.

To make it practical, I had students rewrite user stories using more precise nouns and verbs pulled from domain discussions. Then, they created short glossaries. For teams in companies, this same exercise helps expose assumptions and silos—great for onboarding and alignment.

A key takeaway: if you don't control your language, your language will control your design.

## Building Blocks of the Model

We explored the core tactical building blocks of DDD: **Entity**, **Value Object**, **Repository**, **Service**, **Aggregate**, **Module**, and **Factory**. Each was mapped to a small snippet from our earlier parking lot examples.

We used a matching game where each table received cards with example behaviors (e.g., "must track state over time" or "has no identity and is immutable") and had to match them with the correct concept.

This helped the class build not just vocabulary—but **recognition patterns** they'll use in real-world codebases.

## Wrapping It Up: DDD is About Focus, Not Fantasy

What I wanted students to leave with is that DDD is not magic. It's not even difficult. But it is demanding. It requires teams to listen, challenge assumptions, speak the same language, and value consistency over cleverness.

Whether you're a student, developer, or facilitator, DDD begins by asking: _Do we even know what we mean when we say this feature exists?_ If the answer is "not really," that's where the real design begins.

---

_Posted as part of the Software Engineering course journal. Today we learned that Domain-Driven Design isn't about complex patterns — it's about building software that speaks the language of the business it serves._

## Series Conclusion

---

### **Series Navigation**

- **Introduction**: [Part 1 - Why Software Engineering?](../2010-02-24-software-engineering-purpose/)
- **Previous**: [Part 10 - XP in Practice](../2010-05-08-applying-xp-strategies/)
- **Current**: Part 11 - Domain-Driven Design
- **Next**: [Part 12 - Requirements & Testing](../2010-05-22-requirements-validation-tests/)
- **Complete series**: [Why Software Engineering?](../2010-02-24-software-engineering-purpose/) | [Taming Complexity](../2010-03-02-complexity-process/) | [Waterfall Model](../2010-03-10-waterfall-model/) | [Evolutionary Models](../2010-03-18-evolutionary-models/) | [Agile Mindset](../2010-03-26-agile-mindset/) | [Scrum Productivity](../2010-04-03-scrum-productivity/) | [Scrum Cycle](../2010-04-11-scrum-cycle/) | [XP Quality & Courage](../2010-04-19-xp-quality-courage/) | [XP Principles & Practices](../2010-05-01-xp-principles-practices/) | [XP in Practice](../2010-05-08-applying-xp-strategies/) | [Domain-Driven Design](../2010-05-15-domain-driven-design/) | [Requirements & Testing](../2010-05-22-requirements-validation-tests/) | [Software Testing](../2010-05-29-software-testing/)
