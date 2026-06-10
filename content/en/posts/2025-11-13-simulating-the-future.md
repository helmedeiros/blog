---
title: "Simulating the Future"
categories:
  - Data
  - Engineering
  - Pricing
  - Product
date: 2025-11-13
tags:
  - pricing
  - simulation
  - experimentation
  - pricing-models
  - decision-making
  - platform-engineering
series:
  - lessons-from-a-pricing-platform
series_order: 12
description: "How my pricing team built simulation in three iterations — replay, shadow mode, and the habits we kept — and what each one taught us about trusting a recommendation before customers ever saw it."
subtitle: "Simulation doesn't reduce uncertainty. It moves uncertainty somewhere the team can argue about it before customers do."
---

Pricing engineers learn a particular kind of patience early — the kind where the experiments look promising, the dashboards are green, the model's recommendation is plausible, and you still don't push the button.

The reason you don't push it is asymmetry. Once a price change reaches a customer, it costs more to learn from than it did to ship. Revenue moves. Conversion moves. Partner relationships and customer trust move on their own timescales. By the time the cost shows up, the change has been live for weeks. Shipping is the cheap part. Recovering from a bad change is the expensive part.

My team spent a surprising amount of energy on the question that lives in the gap between *we think this is good* and *we are willing to let customers see it*. We were a small pricing crew — a handful of engineers, a product manager, an analyst — agile by necessity and build-measure-learn by reflex. The way we approached this gap was the way we approached everything else. Start with the cheapest thing that could tell us something. Measure what it told us. Throw it out and build the next thing when it stopped earning its place.

When we wanted to estimate the impact of a candidate change before customers saw it, there was a hierarchy of evidence available, with a real cost attached to each step. Opinion was free and weak. Offline replay was cheap — a script and a sample of past traffic — and immediately informative. Shadow mode required real infrastructure and produced production-shaped numbers. Canary or A/B exposure was the strongest evidence available, and the most expensive, because the cost of being wrong landed on real customers. We worked through that hierarchy in order: staying at the cheapest level that could answer the question in front of us, and only escalating when that level visibly stopped earning its place.

The capability we eventually built — simulation — didn't arrive all at once. It arrived in the shape of three increasingly expensive experiments, each one solving a problem the previous one had exposed.

## Iteration 1: replaying yesterday's traffic

The first version was the simplest thing that could possibly work. We took a sample of historical search traffic — a week, then a month — and ran it through the candidate decision logic offline. Same inputs, new outputs. None of it touched a customer. We just compared the outputs to what we had actually charged at the time.

{{< plantuml title="Iteration 1 — replay historical traffic through new logic, compare to what we actually charged" >}}
@startuml
skinparam shadowing false
start
:Historical traffic;
:New decision logic;
:Predicted outcomes;
stop
@enduml
{{< /plantuml >}}

The goal wasn't to predict the future. It was to make abstract conversations concrete. Questions that had circulated as opinion now had answers we could put a number against:

- Which customers would be affected?
- How different would the prices be?
- Which segments would move the most?
- How large was the expected impact, in aggregate and at the tails?
- Were there outliers nobody had planned for?

Practically, every candidate run produced three views of the same data — a distribution of divergence across all decisions, a per-segment breakdown of which markets and products moved most, and a tail report of the largest outliers. None of those views needed production infrastructure. A laptop, the historical sample, and the candidate code were enough.

The value of that first version turned out to be mostly social. Our pricing reviews changed shape inside one quarter. Before replay, the review sounded like *I think this is safe, I think it's risky, I think it's worth trying*. After, it sounded like *here is who would be affected, here is how much prices change, here are the three segments where the candidate diverges most from current behaviour*. We didn't stop disagreeing. We stopped disagreeing about possibilities and started disagreeing about evidence — which is a much more useful kind of disagreement.

For a quarter, that was enough.

## The problem with believing yesterday's traffic too much

Then the second quarter happened, and the simulator started lying to us.

The first time the offline simulator misled us, the lesson was small. The candidate looked safe in replay; in production, latency spiked at peak hours in a way the offline runs hadn't surfaced. We hadn't simulated load. Honest miss.

The second time the lesson was bigger. We replayed traffic from a slow week. The recommendation looked stable. We rolled it out. The first weekend it touched real demand, the distribution of inputs shifted just enough to push a segment outside the part of the curve the simulator had even tested. The output we had measured was honest. The data we had fed it was thin.

The third time, we caught the mistake in advance and were proud of ourselves. The candidate diverged sharply from current behaviour in one market. The simulator screamed. We held the rollout. A week of analysis later, the divergence turned out to be the candidate doing the right thing — current behaviour had been wrong for months. The simulator wasn't lying. It was telling us we didn't agree with our own current logic.

What we took away from those three episodes was a single rule, more useful than any specific finding. *A simulation is not reality.* It is a structured way of asking *given everything we already know, what would have happened?* That sentence has the word *known* in it twice. It can't answer questions about things we haven't observed yet — load, customer reaction, market shift, our own logic being quietly broken. It also can't tell us which of its answers we should trust. It can only put numbers on a screen.

We needed something that ran in current conditions, on current traffic, while customers were still seeing what they were used to seeing.

## Iteration 2: shadow mode on production traffic

The second version was an architectural step. We wired the candidate logic into the live request path — in parallel to the existing logic, asynchronously, off the critical path — and recorded every output without ever returning it to the customer.

{{< plantuml title="Iteration 2 — candidate runs alongside current logic on real traffic, observed but never returned" >}}
@startuml
skinparam shadowing false
skinparam componentStyle rectangle

[Customer request] as REQ
[Current decision] as OLD
[Candidate decision] as NEW
[Customer response] as RESP
[Comparison log\n(outputs + latency)] as LOG

REQ --> OLD : sync
REQ ..> NEW : shadow / async
OLD --> RESP
OLD --> LOG
NEW --> LOG
@enduml
{{< /plantuml >}}

Nothing changed for the customer. Everything changed for our learning. The candidate now ran on the real distribution of inputs, in the real environment, at real concurrency, against the real intra-day patterns. It could be wrong in production-shaped ways. We could measure those wrongs in production-shaped numbers.

The plumbing was not exotic. Every request carried an ID we propagated through both paths so we could pair the candidate's output with the active one. The pair landed in a comparison log that a downstream job joined and summarised. A feature flag controlled which percentage of which markets the candidate ran against, so we could start small, ramp gradually, and turn the whole thing off in seconds if anything misbehaved. The dashboards we watched most closely were divergence over time, p50/p99 latency for the candidate compared with the active path, and any gap in error rate between the two.

Shadow mode is also where we learned that two implementations of the *same* business intent can diverge in surprising ways once they meet production traffic. Some divergences were bugs in the candidate. Some were undocumented behaviour in the current logic that turned out to be intentional and had to be ported. Some were market-specific overrides living in a config file nobody had mentioned. And some were quietly different opinions, inside our own team, about what the intent had actually been all along.

The shadow phase cost more than offline replay had. The infrastructure was real. The capacity planning was real. The comparison dashboards were real. We had to convince ourselves the spend was worth it — not in revenue but in confidence — and the argument that kept winning was the same one. We could no longer afford to learn from changes only after they had reached customers.

## What the simulator was really for

By the time we were a year into shadow mode, the slow surprise had landed. The simulator had become more useful for alignment than for forecasting.

The forecast was always going to be approximate. The conversation around the forecast was the durable part. Once we shared a view of how the candidate would behave — in numbers, on this week's traffic, in front of everyone — pricing reviews stopped being debates about competing intuitions and started being debates about whose reading of the evidence held up. We disagreed less about *whether* and more about *for whom*. That kind of disagreement was the one we actually needed to have.

The other surprise was that we started running the simulator to make ourselves uncomfortable on purpose. The runs we learned most from were never the ones that confirmed what we already believed. They were the ones that exposed something we hadn't considered. By the second year, we caught ourselves judging the simulator not by accuracy but by how often it surprised us. A simulator that confirmed everything we already believed wasn't doing its job. It was an echo.

## What we kept

Three iterations in, offline replay had been retired. Shadow mode was the working system. A few habits stuck, and turned out to matter more than the infrastructure underneath them.

We always kept *what we have observed* and *what we would expect* in the same view, side by side. When they converged, we knew the candidate was acting as advertised. When they diverged, our reflex wasn't "the simulator is wrong"; it was *what is the customer doing that our assumptions don't cover?*

We routinely deleted simulator scenarios that hadn't taught us anything in two quarters. A scenario that always passes is a slow drag on attention, not a safety net. Lifecycle was non-negotiable.

And we refused to let the simulator be unsurprising. The moment a pricing review started agreeing with it every time, someone on the team was assigned to find a scenario it would fail on. The simulator was a conversation we were having with our own assumptions. A conversation nobody could lose was a conversation that had stopped teaching us anything.

## When this recipe wouldn't have worked

The sequence we ran — offline replay first, shadow mode when replay stopped teaching, habits on top — isn't universal. It worked for us because of conditions that aren't always true.

Shadow mode's whole value is *real distribution at real concurrency*. A system with sparse traffic would have struggled to get a useful sample out of shadow within a reasonable timeframe, and offline replay alone might have remained enough. A decision with no customer-visible outcome would have lost shadow's biggest advantage — the fact that we could be wrong loudly without anyone outside the team noticing. A decision that fundamentally changes downstream state, like inventory allocation, would have made shadow harder still, because a shadow path can't actually take the action it's recommending; we would have had to simulate the side-effect, which puts us back in offline territory.

Underneath all of that, shadow mode lives or dies on the data pipeline that joins active and candidate outputs reliably. Without that pipeline working, we would have spent more on shadow infrastructure than the evidence it produced was worth. The right move there is to stay on offline replay and invest in the data engineering before adding the second layer.

## Closing reflection

Simulation doesn't reduce uncertainty. It moves uncertainty to a place where the team can argue about it before customers do.

That's not nothing. It's also not certainty. Three iterations and two architectures later, what kept our simulator honest wasn't any particular technique. It was our willingness to let the simulator be wrong out loud, in front of stakeholders, before customers got the chance to be wrong about it on our behalf.

A simulator nobody is allowed to be surprised by stops being useful within a quarter. The one we ended up trusting was the one we kept trying, and failing, to break.
