---
title: "What Is a Business Rule?"
subtitle: "A markup of 3% looks the same in code and in config — until somebody has to explain who changed it, when, and why."
author: helio
layout: post
date: 2025-05-21T10:00:00+00:00
series:
  - building-pricing-systems
series_order: 1
categories:
  - Engineering
  - Pricing
  - Architecture
tags:
  - pricing
  - business-rules
  - rule-engine
  - monetization
  - decision-systems
  - architecture
description: "A business rule isn't an if statement. It's a decision somebody owns, audits, and has to explain — and that ownership shapes everything you build around it."
---

A few years back I sat through a thirty-minute Slack argument about whether a 3% markup for short-lead-time bookings in Germany should live in a Go file or in a YAML config.

The engineers were arguing about deploy cadence. The product manager was arguing about ownership. Nobody in the thread was arguing about the question that mattered, which was: when this number changes next quarter, who is responsible for explaining the change?

That conversation is, looking back, where this series begins. A business rule is not an if statement. The if statement is what you write down *after* you already know who decided, what the inputs are, what the decision means, and how you'll audit it. The if statement is the cheapest part of the system. Everything around it is the work.

## The naive version always looks reasonable

The first version of any rule looks fine. Somebody writes this:

```go
func ApplyMarkup(market string, daysToDeparture int) float64 {
    if market == "DE" && daysToDeparture < 7 {
        return 0.03
    }
    return 0
}
```

This is good code. It runs. The test passes. It ships on a Friday afternoon.

Two weeks later a second rule arrives. Also Germany, also short lead time, but only for rail, and only on mobile. The function grows a second branch. Six months later you have nine branches, three feature flags woven through them, and at least one developer who quietly avoids the file because the test suite "behaves weird" when you reorder anything.

This is the moment you discover that the rule was never really a function. It was a decision somebody in the business made, and the function is a fossil of that decision — accurate at the moment of writing, but stripped of every piece of context that would let a later reader reason about it. The system has no idea that the 3% markup is the same kind of thing as the rail-mobile rule. To the runtime, they are consecutive branches. To the business, they are separate policies that change on different cadences and need to be audited by different people.

It gets worse when the second team shows up. Marketing wants to add a rule for a campaign. Revenue wants a different rule that fires only if the customer abandoned a cart yesterday. Each one of them shows up at the engineer's door asking for "a small change." Each small change touches the same function. The function becomes a settlement of grudges from three departments, and nobody can read it anymore.

## Three places this same decision could live

There is a useful exercise I run with teams when the question of "where does the rule go?" comes up. We take a single proposed change — say, the markup for short-lead-time rail bookings — and we ask what happens if it lives in each of three places.

**Inline in code.**

- *What:* the rule is one branch of one function on the hot path.
- *Why:* low ceremony. You can read the rule by reading the code. Tests are easy.
- *Why not:* it inherits the deploy cadence of the service. Any change is a code review. The history of the rule is in `git blame`, which means the why-line is gone the moment the original author forgets.

**As a runtime config.**

- *What:* the rule is one entry in a YAML or JSON file the service loads at startup.
- *Why:* product can change it without a deploy. Auditing is the file history. Tests can drive the service from a config fixture.
- *Why not:* config is now invisibly business-load-bearing. A missing key in YAML is a tariff change in production. There is no schema unless somebody writes one. And without a model, the file becomes a long sequence of magic strings.

**As a rule, in a rule store, evaluated by an engine.**

- *What:* the rule is a typed artifact with conditions, actions, metadata, and an explicit owner, loaded by a rule engine that knows how to match and explain.
- *Why:* the rule carries enough context to be read by a non-engineer. It can be tested, versioned, and retired. The engine takes care of the things that are easy to get wrong: ordering, matching semantics, explainability.
- *Why not:* you now have to build (or adopt) the engine. The artifact has to be designed. The vocabulary has to be agreed.

Most teams, in my experience, end up in option 2 by accident. They start in option 1, panic at the deploy cadence, and bolt YAML on the side without ever designing what is in the YAML. The structure of the file becomes whatever the first engineer happened to type. A year later it is a thousand lines of strings nobody trusts.

This series is about getting deliberately to option 3 without pretending the work in option 1 didn't teach us anything.

## What a rule has to carry

If I had to define a business rule in one sentence, I'd say it is *a decision the business expresses in a form the system can evaluate*. Pull that sentence apart and a rule has to carry at least six things.

A **decision** — the business outcome the rule produces. A markup. A discount. A routing choice. The thing the rule exists to make happen.

A set of **conditions** — the inputs that gate the decision. Market, channel, lead time, customer segment, time of day. The shape under which the decision applies.

A set of **actions** — what concretely happens when the conditions match. Set a markup value. Choose a provider. Suppress an experiment. The action is what the engine executes; the conditions are what the engine matches against.

**Metadata** — the bookkeeping that lets a human reason about the rule later. Who wrote it. When. For what reason. Which ticket. Which experiment. Without metadata, the rule is anonymous, and an anonymous rule is one you cannot safely retire.

**Ownership** — the team or person responsible for the rule's continued correctness. This is rarely written in code, but it has to live somewhere or the rule will outlive everyone who understood it.

And **intent** — the why. The condition is *what* the rule looks for. The intent is what the rule is trying to express. A rule with a condition but no intent is impossible to maintain, because any later change has nothing to be checked against.

{{< plantuml title="A business rule is six artifacts, not one" >}}
@startuml
skinparam shadowing false
skinparam componentStyle rectangle
skinparam defaultFontName "Helvetica"

rectangle "Business rule" as R {
  rectangle "Decision\nthe outcome" as D
  rectangle "Conditions\nwhen it applies" as C
  rectangle "Actions\nwhat happens" as A
  rectangle "Metadata\nwhen, where, ticket" as M
  rectangle "Ownership\nwho answers for it" as O
  rectangle "Intent\nwhy it exists" as I
}

C --> D : gates
A --> D : produces
M ..> D : describes
O ..> D : answers "who"
I ..> D : answers "why"
@enduml
{{< /plantuml >}}

Here is the same German short-lead-time markup, written as something that carries those parts:

```yaml
id: short_lead_time_markup_de
name: "DE short lead-time markup"
intent: |
  Capture demand on short-window bookings in Germany where
  capacity constraints reduce price sensitivity. The team
  reviewed the elasticity curve in Q1 and agreed to keep
  3% until the next demand review.
owner: pricing-de
when:
  market: DE
  days_to_departure:
    less_than: 7
then:
  markup_percentage: 3.0
metadata:
  created: 2025-05-21
  ticket: PRICE-1473
  experiment: ELAST-2025-Q1
  review_after: 2025-11-21
```

There is no engine yet. No loader. No matcher. But the shape of the artifact is already different from the if statement. The intent is visible. The owner is visible. The review date is visible. The condition is the smallest part.

## Rule vs code vs configuration vs model

People who have only seen rules in one form tend to flatten the distinction between rules, configuration, and models. It is worth pulling them apart, because each of them changes through a different organ of the company, and conflating them is how that organ atrophies.

| Form | Changes via | Audited via | Tested with | Owned by |
| --- | --- | --- | --- | --- |
| Code | Pull request, deploy | Git history, code review | Unit and integration tests | Engineering |
| Configuration | Config push, often without deploy | Config history if you kept one | Smoke tests, usually weak | Engineering or platform |
| Rule | Rule edit, often through a UI or pipeline | Rule history, explanation logs | Behavioural tests against facts | Business / domain team |
| Model | Retrain, redeploy weights | Training data lineage, evaluation metrics | Offline scoring, online monitoring | Data science |

A rule is not configuration. Configuration tunes a system that already knows what it does. A rule *expresses what the system should do*. The fact that both end up in a YAML file is a surface coincidence — a coincidence so convincing that I have seen entire teams ship rules as config for years without ever realising what was missing.

A rule is also not a model. A model learns its decision from data; a rule states its decision from intent. They both map inputs to outputs, but only one of them can be argued with at the level of policy. A markup of 3% is a position somebody can defend in a meeting. A markup of 2.74 from a gradient boost is a number you have to ground in evaluation data before anyone defends it. Both belong in a pricing system. Conflating them is how you end up with policies you cannot explain.

The model question matters because every team that builds a rule engine eventually meets the team that wants to put a model behind it. The cleanest way I've seen this work is to keep the rule as the *contract* — the thing the business owns, the thing that is explained — and let the model be one of the action implementations behind the contract. The rule says "apply the segmented markup for this customer"; the model decides what the markup value is. The rule still owns the why.

## The four properties a rule has to have

A rule is useful only when it is deterministic, inspectable, testable, and explainable. Each one of these earns its way in.

### 1. Deterministic

Given the same inputs, the same rule produces the same output. This is non-negotiable. The moment a rule depends on hidden state or wall-clock time without naming those as inputs, it stops being a rule and becomes a bug that hides for weeks.

In practice, this means the rule has to receive its facts. Not look them up. The same rule should be runnable in production, in a test, in a replay against last quarter's traffic, and in a notebook on a Tuesday afternoon. The engine is the thing that has the wall-clock and the database; the rule has only what the engine handed it.

This is the source of the most expensive bug I've shipped in a rule system. A rule fired on a customer "if they had not bought before." The check was a database call, made inside the action. In a quiet hour it was fast. During a regional outage it was slow, then it was wrong, then it cascaded. The fix was not in the rule. The fix was in the contract: customer history is a fact, and facts are passed in.

### 2. Inspectable

You can read the rule without running it. You can answer "what does this rule say?" without spinning up an engine, without loading prod facts, without grepping trace IDs. The rule is, by itself, a thing a non-engineer can look at.

Inspectability is what lets a domain team open a pull request against a rule and have a meaningful argument. If you have to be an engineer to read the rule, the rule is owned by engineering whether you wanted that or not.

### 3. Testable

You can write a test that says *given facts X, this rule should match and produce Y*. The test belongs to the rule, not to the engine. When the engine changes shape, the tests should still be useful.

The shape of a good rule test looks more like a behavioural assertion than like a unit test. *For a German short-lead-time booking, the short-lead-time markup should fire and contribute 3% to the total markup.* That sentence reads the same in code, in a doc, and in a Jira ticket. The rule test is the place those three converge.

### 4. Explainable

When the rule fires, the system can tell you why. When it doesn't fire, the system can tell you which condition failed. The next post but one in this series is dedicated to explainability, because it is the most under-built part of most rule systems — but it starts here, in the definition. If the rule's intent isn't written down, the explanation has nothing to reach for.

The first rule system I ever built was deterministic and inspectable. It was barely testable. It was not explainable at all. When a number looked wrong in production, the only way to investigate was to read the source and reason about it manually. Rules accumulated faster than anyone could review them, and we could not retire any of them safely. The system aged badly because explainability wasn't designed in from the start. That experience is most of the reason this series exists.

## Where rules go wrong over time

A rule is born clear. It rots in the same three ways every time.

It loses its intent. The author leaves. The ticket gets archived. The intent line in the YAML is the only thing keeping the rule alive, and nobody touches it because "it works." Five years later the rule is still firing, and nobody on the team knows why, so nobody dares retire it. This is how rule systems accumulate dead weight.

It outlives its conditions. The world changes. The market that needed the markup re-segments. The condition still matches, but the policy it was expressing is no longer true. The rule fires anyway, and somebody downstream pays for it.

It collides with another rule. Two rules match the same facts. One was written by pricing-DE, one by marketing. The engine picks one of them, somehow, and the other team finds out from a dashboard at midnight. We will come back to matching semantics in a few posts.

The defence against these failure modes is in the artifact itself — the metadata, the owner, the review date. A rule with an explicit `review_after` is a rule the team has agreed to look at. A rule with an explicit `owner` is a rule that has somebody to ask. A rule with an `intent` is a rule that can be evaluated against the world it was written for. Without those, the rule is anonymous, and anonymous rules don't get retired; they get worked around.

## A note on what comes next

I am deliberately not introducing a rule engine yet. The next post in this series is about the *rule model* — the in-memory representation, the field shapes, the tradeoff between typed structures and generic schemas. After that we'll move to storing rules as data, matching them at scale, building the evaluation pipeline, testing the whole thing, making it explainable, and then layering in synthetic traffic, shadow mode, and replay.

The reference codebase for the engine side of this series is [`bre-go`](https://github.com/helmedeiros/bre-go), a Go business rule engine I maintain. It implements four in-process engines behind one port — insertion-order all-match, insertion-order first-match, priority-ordered first-match, and an indexed sub-linear matcher — and it's where most of the code examples in the next post come from. The traffic and replay posts later in the series use [`traffic-gen`](https://github.com/helmedeiros/traffic-gen), a small Go binary that synthesises realistic pricing requests at configurable QPS and persona mixes.

The takeaway here is smaller than an engine. Before you write a single matcher, ask whether the artifact you are producing is actually a rule. A rule has a decision. A rule has conditions. A rule has actions. A rule has metadata. A rule has an owner. A rule has an intent.

If any of those is missing, what you have is an if statement somebody is going to have to explain in a year, without help. That is how most pricing systems quietly become unmaintainable. The rest of this series is about doing it the other way.
