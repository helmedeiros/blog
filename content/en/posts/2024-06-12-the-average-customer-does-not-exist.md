---
title: "The Average Customer Does Not Exist"
categories:
  - Engineering
  - Experimentation
  - Pricing
  - Product
date: 2024-06-12
tags:
  - pricing
  - segmentation
  - experimentation
  - product-discovery
  - price-elasticity
  - monetization
description: "Why personas helped us understand customers, but behavioral dimensions helped us understand pricing."
subtitle: "The average customer doesn't exist. Optimising for one is optimising for nobody."
---

For months, we ran pricing experiments looking for a single answer.

*What is the right price? What is the right markup? What is the right fee?*

Every experiment seemed to push us toward the same destination: find the optimal value and apply it everywhere.

The data kept disagreeing.

Two customers would look at the same journey, the same route, the same provider, the same schedule, the same price — and make completely different decisions.

At first, we assumed we needed more data. Eventually, we realised we needed a better model of customers.

The biggest lesson was surprisingly simple.

The average customer does not exist.

## The danger of averages

Most pricing discussions start with averages. Average booking value. Average conversion. Average revenue per search. Average customer behaviour.

Averages are useful. They help summarise large amounts of information. The problem is that averages often describe nobody.

Picture a simple example.

| Customer group A | Customer group B |
| --- | --- |
| Very sensitive to price | Barely reacts to price |

Average the two groups together and you might conclude that customers are moderately sensitive to price. That sounds reasonable. It is also wrong. The average hides the behaviour that actually matters. One group needs a completely different pricing strategy from the other.

This was one of the first signs that our experiments were teaching us something deeper than whether a pricing rule won or lost. They were revealing differences in how customers perceived value.

## Personas helped us think

We often used personas when discussing customers.

Personas are useful. They create a shared language. They help product managers, analysts, designers, and engineers talk about customer needs without immediately diving into data.

A team might discuss customers who prioritise price. Others who prioritise convenience. Others who value flexibility. Others who care deeply about confidence and information.

Those conversations are valuable. They help humans reason about behaviour.

But personas were never precise enough to drive pricing decisions. A pricing engine cannot evaluate a persona. It cannot receive:

```json
{
  "persona": "Explorer"
}
```

and decide what to do.

Pricing systems need something more concrete. They need signals.

## Personas tell stories. Signals drive decisions.

This distinction became increasingly important as our experimentation capabilities matured.

Humans reason through narratives. Systems reason through observable facts.

The pricing engine never saw customer archetypes. It saw context:

```json
{
  "trip_value": 250,
  "booking_context": "high_urgency",
  "customer_activity": "frequent",
  "journey_type": "round_trip",
  "market": "X"
}
```

Not because those specific signals were universally correct, but because pricing systems need dimensions that can be measured consistently.

The engine reasons about signals. Humans reason about personas. Both are useful. They solve different problems.

## The real world is made of dimensions

One realisation changed how I thought about segmentation.

Customers do not belong to a single segment. They exist across many dimensions simultaneously. A single customer might be highly price sensitive, travel frequently, prefer convenience over flexibility, be booking under time pressure, and be purchasing a higher-value journey, all at once.

{{< plantuml title="A customer exists across many behavioural dimensions at once" >}}
@startuml
skinparam shadowing false
skinparam componentStyle rectangle

object Customer {
  price sensitivity
  travel frequency
  flexibility preference
  time pressure
  trip value
  market
  journey type
  device
}
@enduml
{{< /plantuml >}}

None of these characteristics fully defines the customer. Together, they begin describing behaviour.

That distinction matters because pricing systems rarely operate on one dimension at a time. The complexity emerges from combinations.

## From five personas to thousands of possibilities

This is where many discussions about segmentation become misleading.

A handful of personas can be enough for strategy discussions. They are not enough for pricing decisions.

Five personas might help a product team understand customer motivations. A pricing platform needs to reason about many dimensions, each with multiple possible values.

{{< plantuml title="Behavioural dimensions compound quickly into pricing decisions" >}}
@startuml
skinparam shadowing false
start
:Behavioural dimensions;
:Combinations;
:Segments;
:Pricing decisions;
stop
@enduml
{{< /plantuml >}}

The number of meaningful combinations grows quickly. Not because the team wants complexity. Because customer behaviour is complex.

The pricing challenge isn't identifying five groups. The challenge is discovering which combinations of characteristics lead to different responses to value and price.

## Segments became hypotheses too

One unexpected lesson was that segmentation itself became a hypothesis.

Early on, it was tempting to treat segments as facts:

> Customers booking under time pressure behave differently.

Sounds reasonable. But it is still a hypothesis. It needs evidence.

The same learning mindset we applied to pricing rules eventually applied to segmentation. Every segment became a question:

- Do these customers actually behave differently?
- Does this distinction matter?
- Does it justify a different strategy?
- Can we measure the impact?

The goal was never to create more segments. The goal was to discover which distinctions were meaningful.

## Price was only part of the story

One mistake many engineers make when entering pricing is assuming customer behaviour is mostly about price.

Price matters. But customers rarely optimise for price alone. They optimise for value. And value means different things to different people.

- For some customers, **value ≈ lowest cost**.
- For others, **value ≈ confidence**.
- For others, **value ≈ convenience**.
- For others, **value ≈ flexibility**.

The more experiments we ran, the more obvious this became. We were not simply measuring willingness to pay. We were learning how different customers perceived value.

That is a much more interesting problem.

## What I learned

The biggest shift was not learning that customers behave differently. Most people already believe that.

The bigger shift was realising that those differences can be observed, measured, tested, and incorporated into how pricing decisions are made.

Personas helped us understand customers. Dimensions helped us model customers. Pricing systems helped us act on those models.

The average customer never existed. And once we stopped optimising for averages, we started learning much more about the people behind the numbers.

## Closing reflection

The Business Rules Engine taught us how to express pricing decisions. Experimentation taught us how to challenge them. Segmentation taught us that not every customer experiences value in the same way.

I remember the moment the team stopped calling it segmentation and started calling it "serving different people." The vocabulary change sounded cosmetic. It wasn't. Once we named who we were choosing *not* to serve well by treating everyone the same, the average customer never came back. Every chart we drew afterwards had two or three lines on it, because every chart we believed had two or three lines on it.

The mean is a number a system can produce. A customer is not.
