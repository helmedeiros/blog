---
title: "Understanding Price Sensitivity"
categories:
  - Engineering
  - Experimentation
  - Pricing
  - Product
date: 2024-07-17
tags:
  - pricing
  - price-elasticity
  - experimentation
  - monetization
  - customer-behavior
  - product-discovery
series:
  - lessons-from-a-pricing-platform
series_order: 8
description: "The goal was never finding the highest possible price. The goal was understanding how customer behaviour changes as price changes."
subtitle: "Price sensitivity isn't a label. It's a relationship."
---

For a few years I was working on a pricing platform — the part of the system that decides what to charge a customer, and when. Most of what made it a real platform happened off the page: we had moved rules out of code into a business rules engine, we had stopped shipping pricing changes blind and started treating them as experiments, and we had stopped pretending the "average customer" was a useful concept.

Each of those moves answered a question. Each of them also exposed the next one.

Once we accepted that different customers behaved differently, the obvious follow-up was inescapable. *How* differently? And, more importantly, *at what point does a pricing change start affecting customer behaviour?*

If customers value different things — convenience, confidence, flexibility, cost — then they don't react to price the same way either. Each group has its own threshold, its own response, its own curve.

That question led us into one of the most interesting areas of pricing.

Price sensitivity.

## What price sensitivity actually means

When people first hear the term, they often imagine two categories:

> Price sensitive. Price insensitive.

Reality is rarely that simple.

Price sensitivity isn't a label. It is a relationship. A relationship between a change in price and a change in customer behaviour.

For some customer groups, a small increase in price produces a significant drop in conversion. For others, the same increase has almost no measurable impact. The important realisation is that sensitivity exists on a spectrum.

The goal isn't to classify customers. The goal is to understand the shape of their response.

## Why A/B tests were not enough

Our early experiments often compared two alternatives.

> Variant A = 5%. Variant B = 6%. Which performs better?

This is useful. But it only tells us which option won. It tells us very little about customer behaviour.

Eventually we started asking different questions. Instead of comparing two values, we introduced multiple levels — 0%, 3%, 6%, 9%, 12% — and rephrased the question:

> How does customer behaviour evolve as price changes?

That shift was subtle. It completely changed what we could learn.

## We stopped looking for winners

One of the biggest changes in our experimentation mindset was moving away from the idea that every experiment needed a winner.

Early experiments looked like competitions. Control vs variant. At the end, we expected a clear verdict. Keep it. Remove it. Move on.

Price sensitivity experiments were different. The goal wasn't selecting a winner. It was understanding a curve.

A result might tell us:

{{< plantuml title="A price-sensitivity curve: the answer is the pattern, not any single value" >}}
@startuml
skinparam shadowing false

object PriceChange0 as " 0%  "
object PriceChange3 as " 3%  "
object PriceChange6 as " 6%  "
object PriceChange9 as " 9%  "
object PriceChange12 as " 12% "

object Impact0 as "No impact"
object Impact3 as "No impact"
object Impact6 as "Small impact"
object Impact9 as "Significant impact"
object Impact12 as "Severe impact"

PriceChange0 --> Impact0
PriceChange3 --> Impact3
PriceChange6 --> Impact6
PriceChange9 --> Impact9
PriceChange12 --> Impact12
@enduml
{{< /plantuml >}}

No individual value is the answer. The answer is the pattern.

That pattern is much more valuable than any single experiment result.

## Different customers, different curves

This was one of the most important discoveries.

The same pricing change could produce completely different outcomes depending on the customer group. Two simplified groups make the point:

| Group | Reaction to a price increase |
| --- | --- |
| Group A | Conversion drops quickly |
| Group B | Conversion barely changes |

If we only look at the average, we miss what is actually happening. One group may be extremely sensitive. The other may barely notice. The average result describes neither.

This was another reminder that customer behaviour rarely fits neatly into a single metric. The most valuable insights often appear when we look beneath the average.

## Revenue is only half the equation

A common mistake in pricing discussions is focusing exclusively on revenue.

Revenue matters. But revenue is only one side of the story. A pricing change can increase the amount earned per booking while simultaneously reducing the number of bookings.

That creates a balancing act:

{{< plantuml title="The trade-off a pricing change runs straight into" >}}
@startuml
skinparam shadowing false
start
:Higher price;
:Higher revenue per booking;
:Potentially lower demand;
stop
@enduml
{{< /plantuml >}}

The challenge is understanding where those curves intersect. Too low and value is left on the table. Too high and customer behaviour changes in ways that damage the business.

Price sensitivity helps identify that relationship. Not perfectly. But much more accurately than intuition alone.

## The surprises were the most valuable part

The experiments that stayed with me were rarely the ones that confirmed our assumptions. They were the ones that challenged them.

The customer group we expected to be highly sensitive sometimes was not. The group we thought would tolerate higher prices sometimes reacted strongly. Changes that looked risky occasionally produced no measurable effect. Changes that looked insignificant sometimes generated meaningful behavioural shifts.

Those moments were valuable because they revealed gaps in our mental models.

The goal of experimentation was never proving we were right. It was discovering where we were wrong.

## Sensitivity is really about value

Over time, I stopped thinking about price sensitivity as a pricing concept. I started thinking about it as a value concept.

Customers don't react to prices in isolation. They react to prices relative to the value they perceive.

{{< plantuml title="Sensitivity is the gap between price and perceived value" >}}
@startuml
skinparam shadowing false
start
:Perceived value;
:Willingness to pay;
:Customer decision;
stop
@enduml
{{< /plantuml >}}

That is why two customers can see the same offer and behave differently. They aren't reacting to the same price. They are reacting to different perceptions of value.

This realisation connected many of the lessons from earlier work. Rules. Experiments. Segmentation. They were all attempts to better understand how customers perceive value.

## What I learned

The goal was never finding the highest possible price. The goal was understanding how customer behaviour changes as price changes.

Price sensitivity gave us a language for that relationship. It helped us move beyond opinions. It helped us move beyond averages. And it helped us understand that customer behaviour is often more nuanced than our first assumptions suggest.

The most valuable output wasn't a number. It was a better understanding of customer behaviour.

## Closing reflection

The more we learned about price sensitivity, the more visible the question underneath became.

If different customer groups respond differently to price — and if those responses describe a shape, not a single point — then the pricing job isn't picking a value. It is picking a value *for a context*, and being honest about the curve underneath it.

The best pricing decisions we shipped did not come from the most sophisticated curves. They came from the most honest ones. We drew them small. We drew them often. We knew which segment each curve referred to. And we were willing to delete a curve that had stopped explaining anything.

That habit, more than any specific number, was the asset.
