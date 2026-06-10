---
title: "Fees, Markups, and the Illusion of Simple Pricing"
categories:
  - Architecture
  - Engineering
  - Pricing
date: 2023-07-19
tags:
  - pricing
  - markups
  - fees
  - product-engineering
  - monetization
  - rule-engines
series:
  - lessons-from-a-pricing-platform
series_order: 2
description: "Why a single markup never travels alone, and why changing a price is rarely just changing a number."
subtitle: "Why changing a price is rarely just changing a number."
---

When I joined a pricing team, I thought I understood pricing.

I had spent years building distributed systems, working closely with product teams, and supporting business initiatives. Pricing seemed straightforward compared to some of the platform challenges I had seen before.

Then I followed a single markup through the system.

It crossed multiple services. It depended on commercial agreements. It behaved differently depending on the market. It interacted with existing fees. It was measured by analysts, configured by product managers, implemented by engineers, and scrutinized by business stakeholders.

That was the moment I realized pricing is not a calculation.

Pricing is a system.

## The mistake I made during my first weeks

My mental model looked something like this:

```text
final_price = base_price + adjustment
```

Simple. Elegant. Completely wrong.

The reality looked much closer to this:

```text
final_price =
    base_price
  + fees
  + markups
  + partner adjustments
  + promotions
  + add-ons
  + experiments
  + market-specific behavior
```

| What I expected | Reality |
| --- | --- |
| One price | Multiple pricing decisions |
| One owner | Multiple stakeholders |
| Technical problem | Socio-technical problem |
| Static logic | Continuous experimentation |
| Simple calculation | Distributed decision system |

The real surprise wasn't the equation. It was who shows up around it.

## Fees and markups are not the same thing

One of the first concepts I had to understand was the difference between fees and markups. They sound similar. They sometimes share code paths. They are not the same.

A fee is usually explicit. The customer can often see it on their booking summary — booking fees, service fees, processing fees, operational fees. A fee is not only a revenue mechanism. It is also a customer trust mechanism. The moment a receipt reads "service fee," a reader stops to weigh whether it feels fair.

A markup is different. A markup modifies the underlying product price before the customer sees it. The customer rarely sees the markup itself; they see the price it produced.

| Base price | Markup | Final price |
| --- | --- | --- |
| €100 | €5 | €105 |

In production systems, markups depend on a fan-in of variables. Every variable is an entry point for a future experiment, a future exception, a future incident.

{{< plantuml title="What a single markup actually depends on" >}}
@startuml
skinparam shadowing false
skinparam componentStyle rectangle

object Markup {
  market
  route
  provider
  currency
  device
  lead time
  customer segment
  experiment
}
@enduml
{{< /plantuml >}}

That fan-in is the reason "change the markup" almost never means "edit one line."

## Why pricing rules become messy

Every pricing system starts clean.

Then reality arrives. A specific market needs a different rule. A partner agreement requires special handling. An experiment ships and stays. A regulator changes the constraints. A customer segment behaves unexpectedly. Each event leaves a deposit in the codebase.

A typical rule entry ends up looking like this:

```yaml
country: DE
provider: train
lead_time: < 7 days
markup: 2.5%
```

Then another exception appears. Then another experiment. Then another commercial agreement. Three years later, the rule "file" is a configuration system in its own right.

This isn't bad engineering. It is business evolution expressed through software.

## The four conversations we kept needing to have

The first weeks taught me that pricing work is not bottlenecked by code. It is bottlenecked by alignment.

| Role | Core question |
| --- | --- |
| Product manager | Why should we change pricing? |
| Analyst | How will we measure success? |
| Engineer | How can we implement this safely? |
| Business stakeholder | What outcome are we expecting? |

We learned to make these conversations happen continuously, not once per change. The change that skipped one of them was the change that surfaced as an incident two weeks later.

## Building a pricing change safely

Once those four conversations have a rhythm, a pricing change starts to look less like a deploy and more like an experiment:

{{< plantuml title="A safe pricing change is a feedback loop, not a deploy" >}}
@startuml
skinparam shadowing false
start
:Hypothesis;
:Analysis;
:Rule definition;
:Implementation;
:Experiment;
:Observation;
:Decision;
stop
@enduml
{{< /plantuml >}}

The shape matters. Every step exists to keep the next one honest. Skip "observation" and "decision" becomes guesswork. Skip "analysis" and "hypothesis" is just an opinion. Pricing changes affect revenue. Revenue systems deserve feedback loops.

## What I wish I had known on day one

Pricing is not mathematics. Pricing is decision-making.

Every pricing rule has history. Every number has an owner. Every change needs observability. And revenue systems demand humility.

The real shift, the one that made the rest of the work possible, wasn't technical. It was tonal: stop treating pricing as a backend service to be optimized, and start treating it as a product with users — internal users, mostly, but users nonetheless.

## Closing reflection

Once I stopped seeing pricing as a collection of calculations, another realization emerged. Pricing was behaving less like a backend service and more like a product. The product manager, the analyst, the partner-facing team, the finance team — they were all asking the system different questions, and they all expected coherent answers.

The question worth asking on day one isn't *"how does the price get calculated here?"* It's *"who decides this price changes, and how would they know it worked?"*

Answer that, and the rest of the architecture starts to fall into place.
