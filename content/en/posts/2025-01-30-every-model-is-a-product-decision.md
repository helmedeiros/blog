---
title: "Every Model Is a Product Decision"
categories:
  - Data
  - Engineering
  - Pricing
  - Product
date: 2025-01-30
tags:
  - pricing
  - pricing-models
  - product-strategy
  - decision-making
  - monetization
  - objective-functions
description: "The most important part of a pricing model isn't the algorithm. It's the objective function."
subtitle: "A pricing model is never neutral. Whatever it optimises for is a product decision dressed up as mathematics."
---

There is a particular phrase that used to make my shoulders relax in pricing meetings: *the model is objective*.

It sounded fair. The recommendation came from data. The algorithm followed measurable rules. Compared to a room of people arguing about prices, anything driven by historical observation felt like an upgrade.

The longer I worked with pricing models, the less comfortable that word made me. Not because the models were wrong — most of them were better than the rules they replaced. Because *objective* was the wrong word for what they were doing.

Every model carried assumptions. Every model embedded priorities. Every model reflected a particular view of what success looked like. The mathematics was honest. The choice of what to maximise wasn't neutral at all.

A pricing model is not primarily a technical artifact. It is a product decision in mathematical clothes.

## The illusion of objectivity

Most discussions about models begin with the mechanics. Which signals to include. How to weight them. Where the thresholds sit. How fast the decision has to be. How well the new version scored against the old one.

Those topics matter. They are not where the most important decisions happen.

Imagine two teams. Both have access to the same data. Both use the same algorithm. Both observe the same customers. They can still produce completely different recommendations.

Why?

Because they optimise for different outcomes. The algorithm may be identical. The objective is not.

I saw this happen more than once. Two pricing groups inside the same company would benchmark their models against each other, get into the weeds on logic and validation, and slowly realise they were arguing about different problems. One team had been told to grow revenue this quarter. The other had been told to protect retention through the end of the year. Both had built honest models. Both were doing exactly what they had been asked. Nobody had asked them to be doing the same thing.

The interesting work happened in the room above the modelling work — the one where somebody decided what success was supposed to look like. By the time the data was in the notebook, that decision had already been made. The model was just very efficiently carrying it out.

## The objective function is the strategy

A useful way to picture a pricing model is as the bottom half of a much taller stack:

{{< plantuml title="The model is the visible part. The objective is the load-bearing part." >}}
@startuml
skinparam shadowing false
skinparam componentStyle rectangle

[Business strategy] as BS
[Objective function] as OF
[Model] as M
[Decision] as D

BS --> OF
OF --> M
M --> D
@enduml
{{< /plantuml >}}

Most teams spend their time discussing the bottom two boxes. The leverage lives at the top.

Before a model can recommend anything, somebody has to answer a difficult question. *What are we trying to optimise?* That answer determines everything that follows.

## Different goals create different models

Suppose we have exactly the same customer, exactly the same journey, and exactly the same historical data. Now imagine three different business objectives.

| Objective | Likely outcome |
| --- | --- |
| Maximise short-term revenue | Higher prices where demand appears resilient |
| Maximise conversion | Lower prices to reduce friction |
| Maximise long-term customer value | Balance revenue against retention and trust |

The model is not choosing among these objectives. The organisation is. The model simply operationalises the choice.

This is why disagreements about pricing are often disguised strategy discussions. People argue about numbers. What they are really arguing about is priorities.

## Models inherit the tradeoffs

A pricing model doesn't dissolve the tradeoffs underneath it. It encodes them. A model that maximises revenue may recommend something very different from a model that prioritises retention, and neither is necessarily wrong — they are solving different problems.

That is why I stopped asking whether a model was *good* and started asking *good for what?*

## Accuracy is not the same as usefulness

One trap I saw repeatedly was the assumption that a more accurate model automatically creates more business value.

Sometimes it does. Sometimes it doesn't.

A model can improve prediction accuracy while making recommendations that are harder to explain. It can become more sophisticated while becoming less trusted. It can capture subtle patterns that nobody feels comfortable acting on. The result is a technically impressive system that struggles to influence decisions.

Accuracy matters. Usefulness matters too. The two don't always move together.

## Explainability is a product requirement

Pricing differs from many prediction problems in one important way: pricing decisions are highly visible.

Customers see them. Stakeholders challenge them. Support teams have to explain them. Product managers have to defend them.

At some point somebody asks:

> Why did the model recommend this?

If nobody can answer, trust begins to erode.

The harder part is that the right answer depends on who is asking. A customer-support agent on a call needs the one-sentence reason a specific price applied to a specific booking. A product manager reviewing weekly performance needs the dominant factors driving a segment. A finance lead reviewing the quarter needs assurance that the model isn't drifting away from the targets they signed up for. None of those needs is technical. All of them have to be designed for.

The teams that treated explainability as something to bolt on after the model landed consistently lost the trust battle. By the time the call from support came in, the answer they could give was either too vague to be useful or too technical to be repeated. The next time a price looked odd, the question stopped going to the team. It started going around them.

That doesn't mean every model has to be simple. It does mean every model needs an explanation strategy, designed alongside the model itself, with a defined audience for each level of detail.

Explainability isn't an engineering afterthought. It is part of the product.

## Every model reflects a worldview

Compare two pricing approaches that look identical from the outside, and you find different worldviews underneath. One assumes customers are highly price sensitive. Another assumes convenience matters more. One trusts short-term signals. Another waits for long-term ones. Those assumptions hide beneath the mathematics. They are still there.

The model reflects what the organisation believes about its customers — and quietly disqualifies the customers it doesn't.

## The best models changed slowly

The models that created the most value were rarely the most sophisticated. They were the ones that evolved steadily — a small improvement, a sharper signal, a refined objective, a cleaner feedback loop — long enough for trust to compound around them. The biggest breakthroughs came from accumulating understanding, not from replacing everything.

## What I learned

The most important part of a pricing model isn't the algorithm. It is the objective function.

The algorithm determines *how* the model learns. The objective determines *why* the model exists.

That distinction changed how I evaluate models. Instead of asking *"how accurate is this model?"*, I started asking *"what decision is this model helping us make?"* The second question turned out to be much more useful.

## Closing reflection

The danger of "the model is objective" is that it ends the conversation that needed to happen. Once a recommendation arrives wrapped in mathematics, it stops being argued with — and the strategic choice underneath it never gets named.

The teams I trusted most in pricing weren't the ones with the most accurate models. They were the ones who could state, in one sentence, what their model was optimising for, what it was deprioritising in order to do that, and who in the organisation had said yes to the trade. When that sentence didn't exist yet, the right move was usually to stop building and go find it.

A model without that sentence isn't objective. It's just somebody's preference, automated.
