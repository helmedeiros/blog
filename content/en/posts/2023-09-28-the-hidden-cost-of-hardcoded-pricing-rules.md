---
title: "The Hidden Cost of Hardcoded Pricing Rules"
categories:
  - Architecture
  - Engineering
  - Pricing
date: 2023-09-28
tags:
  - pricing
  - rule-engines
  - technical-debt
  - monetization
  - software-architecture
description: "Why hardcoded pricing rules feel responsible until they aren't, and what really pushes a team to ask for a rule engine."
subtitle: "Hardcoded rules were never the real problem. They were a symptom."
---

The first pricing rule I remember worrying about did not look dangerous.

It was small. A market-specific condition, a percentage adjustment, and a few lines of code. Nothing about it suggested that it would become part of a much larger problem.

```java
if (market.equals("DE")) {
    markup = BigDecimal.valueOf(2.5);
}
```

At the time, it felt like a responsible engineering decision. The business wanted a change. The implementation was straightforward. The rule had tests. The deployment was safe.

That is how most hardcoded pricing rules begin.

They are not born as technical debt.

They are born as delivery.

## Every pricing rule starts small

The challenge is that pricing systems rarely stay small.

A simple market rule becomes a provider-specific rule.

```java
if (market.equals("DE") && provider.equals("rail")) {
    markup = BigDecimal.valueOf(3.0);
}
```

Then a lead-time condition appears.

```java
if (market.equals("DE")
        && provider.equals("rail")
        && daysBeforeDeparture < 7) {
    markup = BigDecimal.valueOf(4.0);
}
```

Then an experiment arrives.

```java
if (market.equals("DE")
        && provider.equals("rail")
        && daysBeforeDeparture < 7
        && experimentEnabled("summer_2023")) {
    markup = BigDecimal.valueOf(1.8);
}
```

Individually, every change makes sense.

Collectively, they create a system that becomes increasingly difficult to explain.

## Why hardcoded rules feel good initially

Hardcoded rules optimize for speed.

| Benefit | Why teams like it | Future cost |
| --- | --- | --- |
| Fast implementation | Immediate business value | Slower future changes |
| Easy testing | Local validation | Global behavior remains unclear |
| Familiar workflow | Pull-request driven | Business knowledge stays hidden in code |
| Simple deployment | No additional platform needed | Every change requires engineering involvement |

The problem isn't that these benefits are false. The problem is that they are real.

That is why teams continue adding rules long after the system has become difficult to evolve. Each rule passes the bar that made the last one feel reasonable.

## The pricing engineer's nightmare

Eventually someone asks a simple question.

*Why is this markup 3.2%?*

Or: *which experiment introduced this rule?*

Or: *does this condition still matter?*

The code can usually tell us what happens. It rarely tells us why.

> Question: Why is the markup 3.2%?  
> Code answer: Because this condition matched.  
> Business answer: Nobody is sure.

This is where pricing systems accumulate hidden complexity. The rule survives not because anyone defended it but because removing it feels riskier than keeping it. Risk asymmetry preserves rules long after their reason for existing has expired.

## Rules are business decisions before they are code

A pricing rule normally starts as a business hypothesis.

> Customers booking close to departure may tolerate higher markups.

Or:

> This provider behaves differently and needs a dedicated strategy.

Only later does that idea become executable logic. The path from hypothesis to production looks like this:

{{< plantuml title="A pricing rule is a business decision long before it is code" >}}
@startuml
skinparam shadowing false
start
:Business decision;
:Pricing hypothesis;
:Rule definition;
:Code;
:Production behavior;
stop
@enduml
{{< /plantuml >}}

The mistake we kept making was preserving only the last step. The code survived. The hypothesis was lost. The business decision became folklore.

One of the most important lessons I learned was that pricing teams should preserve more than the code. They should preserve the reasoning.

## Logic is not policy

Pricing logic explains how something happens. Pricing policy explains why it should happen.

A mature pricing platform makes both visible.

```yaml
id: short_lead_time_markup
owner: pricing-team
reason: Increase revenue on short lead-time bookings
metric: revenue_per_search
conditions:
  market: DE
  provider: rail
  days_before_departure: "< 7"
action:
  markup: 4.0
```

The value of this structure isn't the YAML. The value is that ownership, intent, metrics, and conditions become explicit — and therefore reviewable, debatable, and removable.

A hardcoded rule answers the question *what does this do?* A policy-shaped rule answers the question *why does this exist, and how would we know it stopped being a good idea?*

## Rule interaction is where complexity hides

Most pricing problems aren't caused by individual rules. They are caused by rule interaction.

Picture four rules stacked on the same booking:

- Rule A: add 3%
- Rule B: remove 1%
- Rule C: add 2%
- Rule D: cap at 5%

Questions emerge fast:

- Which rule executes first?
- Can rules override each other?
- Can multiple rules apply at once?
- How do we explain the final result to a customer support agent looking at one specific booking?

Revenue systems require answers to these questions before incidents occur. Once an incident happens, you discover the answers in the worst possible way.

## When engineers start asking for a rule engine

Engineers rarely ask for a rule engine because they want a rule engine.

They ask for one because they can no longer answer basic operational questions.

- Which rules are active?
- Who owns them?
- Why do they exist?
- Can we simulate them?
- Can we disable them without a deployment?
- Can we explain a final price?

At that point, the problem isn't implementation. It's governance.

| Pain | Missing capability |
| --- | --- |
| Rules are hard to find | Discoverability |
| Rules are hard to explain | Traceability |
| Rules are risky to change | Validation |
| Rules require deployments | Runtime control |
| Rules stay forever | Lifecycle management |

This isn't a tooling problem. It's a maturity problem the tooling is being asked to make legible.

## The lifecycle matters more than the syntax

A pricing rule has a lifecycle:

{{< plantuml title="A pricing rule has a lifecycle, not just a creation date" >}}
@startuml
skinparam shadowing false
start
:Opportunity;
:Hypothesis;
:Rule creation;
:Validation;
:Launch;
:Measurement;
:Decision;
:Retirement;
stop
@enduml
{{< /plantuml >}}

Most hardcoded systems are optimized for creation. Very few are optimized for retirement.

That imbalance becomes expensive over time. The cost is not paid by the engineer who added the rule. It is paid by the team that inherits the system three years later and cannot tell which of the 600 rules can be removed.

## What I learned

Hardcoded rules were never the real problem.

They were a symptom.

The real challenge was unmanaged business complexity. Markets evolve. Experiments accumulate. Commercial agreements change. Customer behavior shifts. And eventually the code becomes the only place where the organization remembers how pricing works.

That is when teams start thinking about rule engines — not because rule engines are interesting, but because business complexity finally becomes impossible to ignore.

## Closing reflection

Eventually we stopped asking *how do we write pricing rules?* and started asking *how do we manage hundreds of them safely?*

That question changed everything. It moved the conversation away from code and toward ownership, explainability, observability, governance, and the lifecycle of every rule the system carries.

We under-budgeted the cost of a pricing rule at the moment we added it, basically every time. The cost showed up later — in the engineer who had to explain a price during an incident, in the analyst who couldn't tell which experiment a rule belonged to, in the operations partner who quietly worked around a condition nobody was willing to remove. The bill arrived. It just arrived somewhere else.

A good test of our pricing system, then, wasn't how fast we could add a rule. It was how confidently we could delete one.
