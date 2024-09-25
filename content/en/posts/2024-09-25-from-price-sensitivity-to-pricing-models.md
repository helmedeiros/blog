---
title: "From Price Sensitivity to Pricing Models"
categories:
  - Data
  - Engineering
  - Pricing
  - Product
date: 2024-09-25
tags:
  - pricing
  - pricing-models
  - experimentation
  - monetization
  - decision-making
  - product-strategy
description: "Understanding customer behaviour wasn't enough. We needed a way to make pricing decisions consistently at scale."
subtitle: "A model isn't smarter than the learning process that produced it. It just makes that learning easier to apply repeatedly."
---

A pricing platform can know a lot about its customers and still be unable to act on it.

That sounds wrong the first time you read it. Knowledge is supposed to translate into action. But after a couple of years working on a platform that decided what to charge customers and when, the gap between the two was visible from the inside.

By then the system had absorbed enough lessons to be dangerous. The "average customer" had stopped being a useful concept. Customer responses to price had stopped looking like single numbers and started looking like curves. And every change had stopped feeling like a single decision and started feeling like a stack of tradeoffs — revenue against conversion, trust, retention, simplicity.

What the system didn't have was a way to apply any of it consistently.

Understanding a curve and acting on a curve are two different things.

## The limit of human decision-making

Imagine a world with a single customer type. One response curve. One objective. One pricing decision.

Humans are remarkably good at reasoning about that kind of problem.

Now imagine hundreds of meaningful customer contexts. Different behaviours. Different tradeoffs. Different responses to value.

The challenge changes.

The problem is no longer understanding the customer. The problem is applying what we have learned consistently.

That was the point where pricing stopped feeling like a rules problem and started feeling like a decision-making problem.

## A rule tells you what to do

Rules are excellent when the world is reasonably predictable.

> If X, then Y.

That structure is easy to explain. Easy to test. Easy to govern.

But rules have limits. As more signals become relevant, the number of combinations grows quickly.

A rule-based system can *describe* complexity. Eventually it struggles to *reason* about it.

The challenge was no longer expressing business decisions. It was deciding among thousands of possible outcomes.

## A model tells you what is likely to happen

This is where pricing models entered the conversation.

Not because modelling was fashionable. Not because the organisation wanted more technology. Because the learning system had accumulated more knowledge than the rules layer could express by hand.

A useful way to think about a model is as a compression of everything the team has learned so far:

{{< plantuml title="A model is a compression of what the organisation has learned" >}}
@startuml
skinparam shadowing false
skinparam componentStyle rectangle

[Experiments] as E
[Customer behaviour] as CB
[Historical outcomes] as HO
[Price sensitivity] as PS
[Model] as M
[Prediction] as P

E --> M
CB --> M
HO --> M
PS --> M
M --> P
@enduml
{{< /plantuml >}}

The model doesn't replace learning. The model is a representation of learning. It compresses thousands of observations into something that can help make a decision.

## Models are not magic

One misconception I encountered repeatedly was the belief that a model somehow discovers truth.

Reality is less dramatic.

A model only knows what the organisation has already learned. Poor experiments create poor data. Poor data creates poor models. Poor models create poor decisions.

The model isn't smarter than the learning process that produced it. It simply makes that learning easier to apply repeatedly.

That distinction matters because it keeps the focus on the quality of the feedback loop, not the sophistication of the algorithm.

## Consistency became more valuable than intelligence

One lesson surprised me.

The biggest benefit of a pricing model wasn't intelligence. It was consistency.

Humans are inconsistent. Different people interpret the same information differently. Priorities change. Context gets forgotten. Rules accumulate exceptions.

A model applies the same reasoning framework every time. That doesn't guarantee a perfect answer. It does create a predictable process.

And predictable processes are easier to improve than unpredictable ones.

## Every model embeds tradeoffs

Tradeoffs don't disappear when a model arrives. They get encoded.

A model can't optimise everything simultaneously. Some objective has to be chosen — revenue, conversion, customer value, retention, profitability — and the model simply operationalises that priority.

That means disagreements about pricing are often disagreements about objectives, not disagreements about algorithms. The mathematics usually comes later. The strategic choices come first.

## The first model is rarely the final model

Another lesson worth sharing is that the first successful model is usually simple.

That is a feature, not a limitation.

Simple models are easier to explain. Easier to validate. Easier to challenge. Easier to trust.

Many teams jump directly toward sophistication. The better question is usually:

> What is the simplest model that improves decision quality?

Complexity is easy to add later. Trust is much harder to add later.

## Models create new risks

Pricing models solve some problems and introduce others.

A stale model can become detached from reality. An overfit model can learn patterns that don't generalise. A successful model can influence customer behaviour and gradually invalidate its own assumptions.

The result is another important realisation.

Models aren't products. Models are living systems. They require monitoring, validation, review, retirement.

The lifecycle never disappears. It simply moves to a different layer of the platform.

## What I learned

The most important thing pricing models gave us wasn't automation. It was leverage.

A team can only argue about so many pricing decisions in a quarter. A model is what lets a few honest opinions about value, willingness to pay, and segmentation become the basis for thousands of consistent decisions a day. Done well, the model doesn't replace human judgment. It carries human judgment forward at scale.

Done badly, it carries the wrong judgments forward at the same scale. Models are leverage in both directions.

## Closing reflection

Understanding customer behaviour was difficult. Turning that understanding into consistent decisions was harder. Pricing models helped bridge that gap.

The warning I would give a younger version of myself is to be honest about when a model is earned. A team that has not yet had its segmentation challenged, has not yet been forced to choose between revenue and retention, has not yet seen its experiments fail in ways that hurt — that team has nothing to compress. Putting a model on top of an untested mental model doesn't accelerate good decisions. It industrialises whichever assumptions happened to be loudest in the room.

The interesting question, then, isn't when a team is ready to build a model. It's whether the team has been wrong enough times to know what its model is *for*.
