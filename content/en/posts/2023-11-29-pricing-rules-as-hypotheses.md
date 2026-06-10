---
title: "Every Pricing Rule Is a Hypothesis"
categories:
  - Engineering
  - Experimentation
  - Pricing
  - Product
date: 2023-11-29
tags:
  - pricing
  - experimentation
  - ab-testing
  - price-elasticity
  - monetization
  - product-discovery
series:
  - lessons-from-a-pricing-platform
series_order: 6
description: "The most valuable thing our pricing platform produced wasn't prices. It was learning."
subtitle: "A pricing rule isn't a decision. It's a prediction. And predictions can be wrong."
---

The Business Rules Engine gave us the ability to change pricing safely.

It did not answer the question we cared about most.

*Was the change actually good?*

For a while, we treated pricing rules as decisions. Increase a markup. Adjust a fee. Introduce a new condition. Launch it. Move on.

The more time we spent working on pricing, the more we realized that this way of thinking was incomplete.

A pricing rule isn't a decision.

A pricing rule is a hypothesis.

That distinction sounds subtle. It ended up changing how we thought about pricing, experimentation, analytics, and product development.

## The illusion of certainty

Consider a simple pricing change.

> Increase service fee from 5% to 6%.

At first glance, it looks like a decision. But hidden inside that statement is an assumption:

> We believe increasing the service fee from 5% to 6% will increase revenue without significantly reducing conversion.

That isn't a decision. That's a prediction. And predictions can be wrong.

One of the most useful lessons I learned in pricing is that revenue systems are full of assumptions disguised as certainty. We assume customers will tolerate a fee. We assume a markup won't affect demand. We assume one market behaves similarly to another. We assume customers notice some changes and ignore others.

Assumptions only become knowledge when we test them.

## We stopped discussing percentages

Early pricing conversations often sounded like this:

> Should this markup be 3% or 4%?
>
> Should we increase the service fee cap?

Those conversations were focused on outputs. Over time, we started asking different questions:

> What are we trying to learn?
>
> Which customer behavior are we expecting to change?
>
> What would make us believe this idea was wrong?

The conversation shifted from configuration to discovery. That change in mindset turned out to be more important than any pricing model we later built.

## Why the Business Rules Engine wasn't enough

The Business Rules Engine solved many problems. It gave us ownership. It gave us explainability. It gave us a way to separate pricing capabilities from the underlying rule engine implementation.

But it did not create learning.

The BRE could evaluate a rule. It could not tell us whether the rule should exist. That required something else. It required experimentation.

We started building the surrounding capabilities necessary to learn from pricing decisions — assignment systems, experiment tracking, behavioral data collection, analytical pipelines.

Not because we wanted more infrastructure. Because we wanted better answers.

## A/B testing and price elasticity are different problems

One lesson that surprised me was how often people use *A/B testing* and *price elasticity* as if they were the same thing.

They are related. They answer different questions.

| | A/B testing | Price elasticity |
| --- | --- | --- |
| Starts with | A decision | A curiosity |
| Setup | Two variants (e.g. 5% vs 6%) | A range of points (0%, 3%, 6%, 9%, …) |
| Question | Which performs better? | How does customer behavior change as price changes? |
| Outcome | Pick a winner | Learn the shape of the response curve |
| Best for | Choosing | Understanding |

One is about choosing. The other is about understanding. The distinction matters because understanding customer behavior is often more valuable than choosing between two variants.

## We stopped testing winners and started learning curves

This was one of the biggest transitions in our pricing journey.

Our earliest experiments were mostly comparisons: A versus B. Eventually we started running experiments designed to reveal customer sensitivity to price.

Instead of asking *"which variant wins?"*, we asked *"at what point does customer behavior begin to change?"*

That question opened the door to a completely different class of insights. We discovered that not all customers react to pricing changes in the same way. Some groups were highly sensitive. Others barely reacted. Some changes that looked dangerous turned out to have almost no measurable impact. Others that looked harmless produced meaningful shifts in behavior.

Those discoveries could not have come from a single A/B test. They required experimentation designed to learn, not to validate.

## The experiment assignment problem

Once pricing rules become hypotheses, another challenge appears.

*Who should see which version?*

Every experiment needs a mechanism that assigns customers consistently:

{{< plantuml title="Without consistent assignment, experiment results are noise" >}}
@startuml
skinparam shadowing false
start
:Customer;
:Assignment;
:Pricing variant;
:Outcome;
stop
@enduml
{{< /plantuml >}}

Without reliable assignment, experiments become impossible to interpret. If customers move randomly between variants, measurements become noisy. If assignments are biased, results become misleading.

The technical challenge of assignment is rarely discussed outside experimentation teams, but it is one of the foundations that makes learning possible.

The rule itself is only half the experiment. The assignment strategy is the other half.

## Revenue is a dangerous metric

One of the easiest mistakes in pricing is optimizing for revenue alone.

Revenue matters. But revenue rarely tells the whole story. A pricing change might increase revenue while damaging conversion. It might increase revenue while reducing customer satisfaction. It might improve one market while hurting another. It might create short-term gains and long-term losses.

That is why every pricing hypothesis needs guardrails.

| Primary metric | Typical guardrails |
| --- | --- |
| Revenue | Conversion rate |
| Service fee revenue | Booking completion rate |
| Margin | Customer satisfaction |
| Attach rate | Cancellation rate |

The most difficult pricing decisions aren't the ones where one metric improves. They are the ones where multiple metrics move in different directions.

## The hardest part wasn't running experiments

Most people imagine experimentation as a technical challenge.

In practice, running an experiment was often the easy part. Understanding the results was harder.

Imagine two variants:

- **Variant A** increases revenue slightly and improves conversion.
- **Variant B** increases revenue significantly but reduces conversion.

Which one wins?

That isn't an engineering question. It is a business question.

Experiments do not eliminate decision-making. They improve the quality of the information available to decision-makers. The team still needs to decide which trade-offs matter.

## The experiments that taught us the most

Looking back, the most valuable experiments were not the successful ones. They were the experiments that disproved our assumptions.

The ones that showed a market behaving differently than expected. The ones that revealed customer segments we had overlooked. The ones that demonstrated that a seemingly obvious idea was actually wrong.

Those experiments generated the most learning. And learning compounds.

A successful pricing change creates value once. A lesson about customer behavior can create value for years.

## What I learned

The lesson wasn't that customers react to price. Everybody already knows that.

The lesson was that different customers react differently.

Once we understood that, individual pricing rules stopped looking like answers. They started looking like questions. Questions about customer behavior. Questions about value. Questions about willingness to pay. Questions about trade-offs.

That reframing meant the team's job changed too. We weren't shipping pricing changes. We were running a learning loop:

{{< plantuml title="The pricing team owns a learning loop, not a release cadence" >}}
@startuml
skinparam shadowing false

state Hypothesis
state Rule
state Assignment
state Experiment
state Result
state Learning

[*] --> Hypothesis
Hypothesis --> Rule
Rule --> Assignment
Assignment --> Experiment
Experiment --> Result
Result --> Learning
Learning --> Hypothesis
@enduml
{{< /plantuml >}}

The most valuable thing our pricing platform produced wasn't prices.

It produced learning.

## Closing reflection

The rule engine gave us a way to express decisions. Experimentation gave us a way to challenge them. Together they created something more useful than a pricing platform — a learning system.

What we were really learning was that a pricing platform stops being useful when the people running it stop being curious about the customer behind the price. Tools, rules, engines, dashboards — none of them survives a team that has decided the answer is already obvious.

Treating every rule as a hypothesis was just a way of refusing to be that team.
