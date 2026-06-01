---
title: "Pricing Is a Team Sport"
categories:
  - Engineering
  - Pricing
  - Product
date: 2023-08-24
tags:
  - pricing
  - product-management
  - analytics
  - engineering
  - experimentation
  - monetization
description: "Why successful pricing decisions emerge from product, analytics, engineering, and business working together — not from any single discipline."
subtitle: "Pricing lives in the intersection of product, analytics, engineering, and business."
---

One of the biggest surprises after joining a pricing team wasn't the complexity of the pricing rules.

It was discovering how many people needed to be involved to change a single one.

Before working on pricing systems, I assumed most pricing changes were technical. A business stakeholder would identify an opportunity, a product manager would prioritize it, engineers would implement it, and the system would produce a different price.

Reality was considerably more complicated.

A single pricing experiment could require alignment between commercial stakeholders, analysts, product managers, engineers, and operational teams. Everyone viewed the same change through a different lens. Everyone cared about different risks. Everyone measured success differently.

The more time I spent working on pricing, the more I realized that successful pricing systems are not built by individual disciplines.

They are built through collaboration.

## The engineer's trap

One of the first mistakes I made was treating pricing as a technical problem.

My mental model looked something like this:

{{< plantuml title="What I thought a pricing change looked like" >}}
@startuml
skinparam shadowing false
start
:Pricing change;
:New rule;
:Deploy;
:New revenue;
stop
@enduml
{{< /plantuml >}}

The actual process looked more like this:

{{< plantuml title="What a pricing change actually looks like" >}}
@startuml
skinparam shadowing false
start
:Business opportunity;
:Customer impact analysis;
:Pricing hypothesis;
:Measurement strategy;
:Technical design;
:Safe rollout;
:Experiment results;
:Business decision;
stop
@enduml
{{< /plantuml >}}

The difference between those two flows is where most pricing complexity actually lives.

It isn't in the rule engine. It's in the meetings that have to happen before anyone touches the rule engine.

## What the product manager brings

The best product managers I worked with never started with a percentage.

They started with a problem.

Instead of asking *"should we increase this markup by 2%?"*, they asked *"what customer behavior are we trying to influence?"* — or *"what business outcome are we trying to achieve?"*

That distinction matters. Pricing decisions should emerge from hypotheses, not from arbitrary numbers.

| Product responsibility | Why it matters |
| --- | --- |
| Define customer problem | Prevents random pricing changes |
| Build hypotheses | Creates measurable expectations |
| Prioritize opportunities | Focuses engineering effort |
| Align stakeholders | Creates shared understanding |

The real PM contribution isn't the prioritization. It's the framing that makes the rest of the team agree on what "success" means before anyone writes code.

## What the analyst brings

If product managers define hypotheses, analysts define confidence.

One lesson I learned quickly is that pricing changes without measurement are not experiments. They are just production changes with extra steps.

Every pricing experiment needs honest answers to questions like these:

- What metric are we optimizing?
- What guardrails protect the customer experience?
- How long should the experiment run?
- How large must the sample be?
- What would "success" actually look like?

Without those answers, teams can easily mistake noise for learning. Pricing systems generate enormous amounts of data. The challenge isn't producing the data. It's turning the data into a decision the team is willing to act on.

## What the engineer brings

Engineers contribute much more than implementation.

The strongest pricing engineers I worked with constantly asked questions like these:

- Can we explain this price?
- Can we roll this back safely?
- Can we measure its impact?
- Can we test it before exposing customers?
- Can we support future variations without rewriting everything?

These questions often influence the success of a pricing initiative more than the pricing rule itself.

A good pricing rule deployed unsafely can still create incidents.

A mediocre pricing idea deployed safely can still generate valuable learning.

The real engineering value isn't the speed of delivery. It's the safety of the delivery path.

## Why business context matters

One of the easiest mistakes engineers can make is assuming pricing decisions are purely mathematical.

They are not.

Pricing systems are heavily shaped by business context — commercial agreements, provider relationships, regulatory constraints, market expectations, seasonal behavior, and competitive positioning. A rule that makes perfect technical sense may be completely incompatible with business reality.

That is why pricing teams need constant communication between technical and non-technical stakeholders. Without it, every "clean" technical proposal turns into a meeting where someone slowly explains why the clean version cannot ship.

## Building shared ownership

The most successful pricing teams eventually develop a shared language.

| Concept | Product view | Analytics view | Engineering view |
| --- | --- | --- | --- |
| Markup | Revenue lever | Experiment variable | Rule evaluation |
| Fee | Customer experience | Conversion impact | Configuration |
| Experiment | Hypothesis | Statistical test | Rollout mechanism |
| Pricing rule | Business decision | Observable variable | Executable logic |

When teams share vocabulary, discussions become significantly more productive. Without shared language, pricing conversations are translation exercises. With it, they become decisions.

But vocabulary is only the first half of ownership. The other half is being honest about the loop the team is actually accountable for.

## The loop the pricing team owns

It would be easy to read this post as a list of roles. That isn't quite right.

Roles describe who shows up. Ownership describes what the team is accountable for. And the pricing team — engineers, product managers, analysts, business partners — owns more than a feature backlog.

We own a loop.

{{< plantuml title="The loop the pricing team owns" >}}
@startuml
skinparam shadowing false

state Understand
state Respond
state Drive
state Build
state Measure
state Learn

[*] --> Understand
Understand --> Respond
Respond --> Drive
Drive --> Build
Build --> Measure
Measure --> Learn
Learn --> Understand
@enduml
{{< /plantuml >}}

Each step in the loop is something the team owns — not delegates upward, not waits for, not pushes onto another function. If any one of these breaks, the loop stops being a loop and becomes a one-way street out of the team.

| Verb | What the pricing team owns | What it looks like when it's missing |
| --- | --- | --- |
| Understand | The business context, the customers, and the existing system — not just the code | "We don't know why that rule exists" |
| Respond | The opportunities, incidents, and requests that arrive from the business and from production | "Pricing is a black box; nobody returns calls" |
| Drive | Proactive direction, not only reactive work — proposing what to test next | "We only change pricing when someone asks us to" |
| Build | Safe, reversible, observable implementation of the change | "It shipped. We hope it works." |
| Measure | Honest instrumentation of impact, including the parts that fail | "The dashboard is on someone else's roadmap" |
| Learn | Acting on what the data shows, including reverting and rewriting | "We ran the experiment but never decided" |

Notice that this isn't a process the team *follows*. It is a posture the team *holds*. A pricing team that only builds is a delivery team for someone else's ideas. A pricing team that owns the whole loop is the team that gets trusted with the next, harder problem.

This isn't a hierarchy. It's a contract.

## The meeting I wish we had from day one

Once a team accepts ownership of that loop, one practice keeps it honest.

A recurring pricing review. Not a status meeting. A learning meeting.

Something like:

1. What changed?
2. Why did we change it?
3. What happened?
4. What surprised us?
5. What should we do next?

The purpose isn't blame. The purpose is the team holding itself accountable to its own loop — closing the gap between what we decided and what actually happened. Pricing systems improve when teams continuously connect decisions with outcomes, and when they don't have to wait for an incident to do it.

## What I learned

The biggest lesson from my first years working on pricing systems is that pricing is neither a business discipline nor a technical discipline.

It lives in the intersection between both worlds — and the pricing team has to live there too, owning every step from understanding the business to learning from the result.

Great pricing teams understand customers. They respond to opportunities. They drive direction. They build with care. They measure honestly. They learn out loud. None of those is optional. None of those belongs to someone else.

## Closing reflection

As our collaboration improved, another challenge emerged. The rules themselves were becoming harder to understand. Every successful experiment introduced new conditions, new exceptions, and new business logic. The hard problem was no longer alignment between people — it was alignment between rules.

If you're joining a pricing system today, the most useful early question isn't *"how is this price calculated?"*. It's *"who owns the loop around this number — understand, respond, drive, build, measure, learn — and where is it broken?"*

The math is the easy part. The agreement is the system. The ownership of the loop is the team.
