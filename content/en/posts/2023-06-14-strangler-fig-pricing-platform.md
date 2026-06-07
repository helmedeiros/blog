---
title: "Before Building a Pricing Platform, We Had to Stop Replacing and Start Growing"
categories:
  - Architecture
  - Engineering
date: 2023-06-14
tags:
  - strangler-fig
  - pricing
  - platform-engineering
  - modernization
  - legacy-systems
  - software-architecture
  - rule-engines
series:
  - pricing-platform
series_order: 1
description: "Why our first move toward a new pricing platform was understanding the present, not replacing it."
subtitle: "Why our first move toward a new pricing platform was understanding the present, not replacing it."
---

The system was working.

That was the problem.

Pricing was producing revenue every day. Customers were booking. Markups, fees, and add-ons were flowing through services that nobody had touched in years. And buried inside that working system was the assumption that any of it could be safely replaced.

It couldn't. Not in one move. Not without breaking trust we hadn't earned the right to spend.

I joined a new team inside the company where I was working. The mission sounded straightforward on paper: evolve our pricing capabilities. The reality was considerably more complex. Pricing was not a single system. It was a collection of decisions spread across services, repositories, integrations, operational processes, and years of accumulated business knowledge. Fees were calculated in one place. Markups in another. Add-ons followed different paths. Some pricing decisions happened close to customer-facing applications, while others were buried deep inside backend services.

The challenge wasn't building something new.

The challenge was building something new without breaking what already worked.

## The temptation of the big rewrite

Whenever teams discover architectural complexity, there is often a natural instinct to start over.

The logic seems reasonable. We know the problems. We know the limitations. We have newer technologies available. Why not simply replace the old solution with a modern platform?

In practice, those conversations rarely survive contact with reality.

A pricing system is not just software. It is encoded business knowledge. Every rule represents a decision someone made years ago. Every exception exists because a customer, partner, operator, regulator, or market demanded it. Many of those decisions are not documented. Some are not even remembered. The system becomes a living museum of business evolution.

| Assumption | Reality |
| --- | --- |
| We know exactly what the current system does | Much of the behavior exists only in code |
| Rebuilding is mostly a technical effort | Rebuilding is primarily a business discovery effort |
| New technology reduces risk | Rewrites often introduce new risks |
| Legacy behavior is fully understood | Hidden dependencies emerge continuously |

This was one of my first observations after joining the team. Before discussing future capabilities, we first needed to understand the present. Not just the code. The business.

## Understanding the future before changing the present

One of the most valuable lessons I learned during that period was that architecture conversations should not start with architecture. They should start with outcomes.

Before creating a new pricing platform, we spent time understanding where the company wanted to be years into the future. Questions started appearing everywhere:

- What pricing capabilities would we need in three years?
- How quickly should new pricing experiments be launched?
- Who should own pricing decisions?
- How configurable should rules become?
- What should require engineering involvement?
- What should become self-service?
- How would we support new products and monetization models?

Only after discussing these questions could we evaluate the systems that already existed. This wasn't about technology. It was about creating a shared picture of the destination.

The real challenge wasn't replacing software. It was creating enough understanding of the future that we could recognize which parts of the present should survive.

## Discovering pricing capabilities hidden across the organization

As we mapped the existing landscape, we discovered pricing logic spread across multiple places. Some capabilities were obvious. Others were hidden. A simple markup could involve several services. A fee could depend on data generated elsewhere. An add-on might have its own operational process entirely separate from the rest of the pricing flow.

The work started to resemble archaeology. Every repository revealed another layer of business decisions. Every service exposed assumptions nobody had documented. Every conversation uncovered another dependency.

A simplified view looked something like this:

{{< plantuml title="Pricing logic scattered across existing systems" >}}
@startuml
skinparam shadowing false
skinparam componentStyle rectangle

[Customer Request] as REQ
package "Existing Systems" {
  [Markups] as M
  [Fees] as F
  [Add-ons] as A
}
[Final Price] as FP

REQ --> M
REQ --> F
REQ --> A
M --> FP
F --> FP
A --> FP
@enduml
{{< /plantuml >}}

The goal wasn't to centralize everything immediately. The goal was first to understand what actually existed.

## Why the Strangler Fig pattern made sense

Around that time, one architectural approach consistently surfaced in discussions: the Strangler Fig pattern.

The idea comes from nature. A strangler fig grows around an existing tree. It does not replace the tree overnight. Instead, it gradually surrounds it, absorbs its responsibilities, and eventually becomes the primary structure. Martin Fowler later popularized this metaphor in software modernization.

The pattern is deceptively simple:

1. Leave the existing system running.
2. Build new capabilities around it.
3. Redirect behavior gradually.
4. Retire old components one piece at a time.

What made the idea attractive was not elegance. It was risk reduction.

| Big Rewrite | Strangler Fig |
| --- | --- |
| Large delivery event | Continuous delivery |
| Long time before value | Early incremental value |
| High uncertainty | Continuous learning |
| Difficult rollback | Easier rollback paths |
| Requires complete understanding upfront | Allows understanding to emerge |

This isn't about avoiding change. It's about making change survivable.

## Anatomy of a Strangler Fig migration

The pattern is easy to draw on a whiteboard and hard to apply in production. In our case, the most useful way to understand it was to walk through a single capability and trace what actually had to happen, step by step.

A fee, for example.

In the original system, fees were calculated inside the search service. The same monolith that returned travel results also decided how much to charge for them. The logic had been added incrementally over the years, sometimes for a market, sometimes for a partner, sometimes for a campaign nobody could find documentation for anymore. It was small enough that nobody had ever budgeted time to extract it. And critical enough that nobody wanted to be the person who broke it.

That's the typical Strangler Fig starting point. It isn't about systems that are obviously rotten. It's about systems that are quietly central.

The migration unfolded in stages, and each stage existed to answer a different question.

**Stage 1. Introduce a seam.**

The first move had nothing to do with the new service. It was inside the search monolith. We extracted the inline fee calculation behind an internal interface — a single function call that the rest of the search code had to go through. Nothing about behavior changed. Nothing about ownership changed. We were not solving the problem yet. We were creating a place where the problem could be solved later.

A seam is the smallest unit of optionality. Without it, no migration is possible. With it, every later step becomes a choice.

**Stage 2. Stand up the new service.**

Then we built a separate fee service. Same inputs. Same expected outputs. No new features. No improvements. No "while we're at it." This is the step engineers most often want to skip, because it feels like duplication. It is duplication. That's the point.

The new service was not allowed to be smarter than the old one yet. Its only job was to produce the same number.

**Stage 3. Run it in shadow.**

This is where the pattern starts paying off. Every search request still went through the seam, still called the old inline fee logic, and still returned that result to the customer. But in parallel — asynchronously, off the critical path — the seam also called the new fee service with the same inputs and recorded both outputs and timings.

The customer saw nothing different. The data team saw everything.

{{< plantuml title="Shadow execution: customer sees the old path, the new path is observed" >}}
@startuml
skinparam shadowing false
skinparam componentStyle rectangle

[Search Request] as REQ
[Seam in Search Monolith] as SEAM
[Inline Fee Logic\n(monolith)] as OLD
[New Fee Service\n(shadow)] as NEW
[Comparison Log\n(outputs + latency)] as CMP
[Response to Customer] as RESP

REQ --> SEAM
SEAM --> OLD : sync
SEAM ..> NEW : async / shadow
OLD --> RESP
OLD --> CMP
NEW --> CMP
@enduml
{{< /plantuml >}}

What the shadow phase let us answer was simple and brutal:

- For the same input, does the new service return the same fee as the old code? Always? In which markets? For which products? On which edges?
- And does it do so fast enough that customers would not notice the change in tail latency once we cut over?

The first question protects revenue. The second protects experience. We were not allowed to ramp traffic until both were green.

In practice, the first weeks of shadow execution are humbling. The "same logic" you wrote in the new service diverges from the monolith in tiny, embarrassing ways. A rounding step happens half a millisecond earlier. A currency conversion uses a slightly different rate cache. A market-specific override that lived in a config file nobody mentioned is silently absent. Every divergence is a piece of business knowledge that nobody remembered to write down.

That's not a problem to be hidden. That's the whole reason the shadow exists.

**Stage 4. Tune until parity.**

Each divergence got triaged. Some were real bugs in the new service. Some were undocumented behavior in the old one that turned out to be intentional and had to be ported. Some were undocumented behavior that turned out to be a forgotten accident, and the business decided not to carry it forward.

Performance got the same treatment. Shadow traffic exposed where the new service was slower than the inline path — the cold-start of a separate process, an unnecessary network hop, a serialization choice that mattered at p99 but not at p50. None of this is visible in a load test against a happy path. It is only visible when production traffic, in production shape, runs through both implementations at the same time.

We did not move on until the comparison report showed two things on the same dashboard: output parity within an accepted tolerance, and latency within an accepted budget.

| Phase | Traffic on new service | What we watched | Exit criterion |
| --- | --- | --- | --- |
| Shadow | 0% (mirrored async) | Output parity, p50/p99 latency vs old | Parity rate above target across all markets |
| Canary | 1% | Conversion, revenue per session, error rate | No statistically significant regression |
| Ramp | 10% → 25% → 50% | Same metrics, on a larger sample | Stable across two business cycles |
| Cutover | 100% | Same metrics, plus removal of dead code | Old fee path deleted from the monolith |

**Stage 5. Ramp behind a flag.**

Only after parity and performance held did we start routing real traffic to the new service, and even then, behind a feature flag we could turn off in seconds. Small percentage first. Wait. Watch the business metrics, not just the technical ones. Increase. Wait. Increase.

The flag is not just a safety net. It is a contract with the rest of the company. It says: if anything looks wrong, we can put yesterday's behavior back, in production, while we figure out why.

**Stage 6. Remove the old path.**

This is the step that closes the loop. Once the new fee service had been serving 100% of traffic for long enough to cover seasonality and partner cycles, we deleted the inline fee logic from the search monolith. The seam stayed. The legacy code did not.

If you skip this step, you have not done a Strangler Fig migration. You have built a second system and kept the first one. That isn't modernization — it's a tax.

The seam, the shadow, the comparison log, the feature flag, the ramp, the deletion. Each one is doing a different job. Each one earns its place by reducing a specific category of risk.

## Keeping the experience identical while changing everything underneath

One of the most important constraints we had was preserving customer experience. Customers did not care about our architecture. They cared about seeing the right prices. They cared about booking successfully. They cared about trust.

That meant our first objective was not innovation. It was compatibility.

For a period of time, the new platform needed to produce the same outputs as the existing systems. Only after earning confidence could we begin introducing new capabilities.

In practice, the journey looked closer to this:

{{< plantuml title="Growing a new pricing layer around the existing system" >}}
@startuml
skinparam shadowing false
skinparam componentStyle rectangle

[Current Pricing System] as CPS
[Existing Behavior] as EB
[New Pricing Layer] as NPL
[Future Capabilities] as FC

CPS --> EB
EB --> NPL
NPL --> FC
@enduml
{{< /plantuml >}}

The new layer initially looked redundant. Some engineers naturally questioned its value. Why build something that behaves exactly the same?

Because identical behavior today creates freedom tomorrow.

## Transitional architecture is not waste

One lesson that stayed with me from that period is that engineers often underestimate the value of temporary architecture.

We like permanent solutions. We like clean systems. We like building things that last.

But modernization rarely happens that way. Sometimes the most valuable component is the one designed to disappear.

Routing layers. Compatibility adapters. Migration services. Shadow execution paths. Comparison dashboards. Feature flags whose only job is to be turned off one day. These components may eventually be deleted, but they make progress possible.

Transitional architecture is not waste. It is scaffolding. And scaffolding is often what allows us to safely construct something larger.

The real cost of modernization is rarely the temporary code. The real cost comes from trying to avoid temporary code and forcing a risky migration instead.

## What I learned

Looking back, joining the pricing team taught me something that continues to influence how I approach large-scale change.

We often imagine transformation as replacement. Old becomes new. Legacy becomes modern. Monolith becomes platform.

Reality is usually less dramatic. The most successful transformations I've seen look more like gardening than demolition. You create space. You understand the ecosystem. You identify what should grow. You remove constraints carefully. And over time, something new emerges around the existing structure.

The Strangler Fig pattern isn't really about software architecture. It's about respecting complexity. It's about acknowledging that businesses cannot stop while engineers redesign systems. And it's about recognizing that the safest path to the future is often one small, deliberate step at a time.

Most of the Strangler Fig is unglamorous work. You don't get to demolish anything. You put a seam where there wasn't one, route a copy of the traffic through it, and then spend several months earning the right to delete an `if` statement. The thrill is gone by the second week.

What remains, after the thrill goes, is a system the team can change without holding its breath. That is the whole prize. The pattern is just the means.
