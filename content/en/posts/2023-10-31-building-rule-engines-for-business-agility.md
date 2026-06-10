---
title: "Building Rule Engines for Business Agility"
categories:
  - Architecture
  - Engineering
  - Pricing
  - Platform
date: 2023-10-31
tags:
  - pricing
  - rule-engine
  - drools
  - business-rules-engine
  - monetization
  - platform-engineering
series:
  - lessons-from-a-pricing-platform
series_order: 5
description: "Why we built a Business Rules Engine on top of Drools instead of coupling our pricing platform directly to a rule engine implementation."
subtitle: "Technologies change. Business capabilities survive much longer."
---

By the time we started discussing rule engines, the symptoms had been showing for a while.

Pricing rules were piling up across services. Every market needed an exception. Every partner needed a tweak. Every experiment left behind code that nobody was sure how to remove. The pricing logic was becoming the only place where parts of the business were remembered, and "explaining a price" was starting to require a meeting.

A rules engine was the obvious next step. Before we get to which one we picked, it helps to slow down on what a rules engine actually is, where teams use them, and what they hand you when you put one in.

## What a rules engine actually is

A rules engine is a piece of software whose only job is to evaluate decisions described as rules. The rules live separately from the application that uses them. The engine takes input — a request, a transaction, a session — runs the relevant rules against it, and returns an answer.

The classical name for this category is *business rules management system* (BRMS). The term comes from the 1990s, when companies discovered that the policy decisions buried inside enterprise applications kept changing faster than the applications themselves did.

Three properties define a rules engine, in any era and any stack:

- Rules are **declared**, not hardcoded.
- Rules are **evaluated by a runtime separate from the calling code**.
- Rules can be **added, modified, and removed without rewriting the application**.

The last property is the one that matters. Everything else is plumbing in service of it.

## Where rules engines show up

Pricing isn't a special case. Wherever a decision needs to evolve faster than the software around it, a rules engine shows up:

- **Fraud detection** — declare what counts as suspicious; tune thresholds without redeploying.
- **Credit and lending** — encode approve/decline policy in a place that can be audited.
- **Insurance underwriting** — apply risk rules across many products without copy-pasting code per product.
- **Compliance and regulation** — keep statutory constraints in a place auditors can read.
- **Content moderation** — express moderation policy that shifts as norms and regulations shift.
- **Workflow routing** — decide where a case, a ticket, or a document goes next.
- **Personalisation** — express segment-level rules alongside model-based scoring.

The pattern repeats. A business policy needs to change faster than the surrounding system would happily allow. A rules engine moves the policy out of the application and into a place the business can actually reach.

## Why a team reaches for one

The reasons teams adopt a rules engine are rarely theoretical. They show up as friction in everyday work:

- Business stakeholders want a change that an engineer has to deploy.
- Nobody can explain why a specific decision came out the way it did.
- An experiment requires a rule change, but changing the rule means re-running the whole service's release pipeline.
- A policy has expired, but nobody is sure where it lives.
- Two teams keep stepping on each other because their rules touch the same code.

A rules engine doesn't make those problems disappear. It moves them somewhere the team can address without going through the application's release cycle.

## What a good rules engine gives you

When it's working, a rules engine hands the team some specific capabilities:

| Capability | What it enables |
| --- | --- |
| Externalised rules | Change a policy without redeploying the consuming service |
| Declarative format | Read rules as policy, not as control flow |
| Conflict resolution | Decide priority and overrides between rules consistently |
| Simulation | Replay historical traffic through a candidate rule set |
| Explainability | Trace why a specific decision came out the way it did |
| Lifecycle | Version, deprecate, and retire rules deliberately |
| Audit trail | Show who changed which rule and when |

"Fast evaluation" isn't at the top of the list. Performance matters, but it's rarely the reason teams adopt a rules engine. The reasons are governance and pace of change. The runtime is the means, not the end.

## Why a rules engine was the next step for us

The patterns above weren't hypothetical for our team. They were our open tickets.

Stakeholders were waiting on deploys. Experiments were getting stuck behind release pipelines. Nobody could quickly answer why a specific markup had applied. A handful of rules had expired but were still in the codebase, untouched because removing them felt riskier than keeping them. Two teams had started adding pricing logic in places that touched the same code paths.

Every one of those was a governance problem dressed up as an engineering problem.

It would have been easy to read this as "we need a rule engine" and stop there:

{{< plantuml title="The shortest version of the story" >}}
@startuml
skinparam shadowing false
start
:Need rules;
:Need rule engine;
stop
@enduml
{{< /plantuml >}}

That reading is incomplete. The actual chain looked more like this:

{{< plantuml title="The actual chain: rule evaluation was only the last link" >}}
@startuml
skinparam shadowing false
start
:Need business agility;
:Need faster experiments;
:Need explainability;
:Need ownership;
:Need simulations;
:Need rule evaluation;
stop
@enduml
{{< /plantuml >}}

The business wasn't asking for a rule engine in the abstract. The business was asking for speed. The rule engine was the means.

So when we started evaluating implementations, the criteria came from the chain — not just "can it run rules quickly," but "does it help us evolve them honestly."

## Drools as our implementation choice

When we evaluated options, Drools immediately stood out.

| Capability | Why it mattered |
| --- | --- |
| Mature ecosystem | Reduced implementation risk |
| Complex rule evaluation | Supported real pricing scenarios |
| Agenda management | Helped with rule conflict resolution |
| Performance | Suitable for search-time decisions |
| Open source | Avoided commercial lock-in |
| Existing expertise in the market | Easier hiring and onboarding |

For a while, the architecture looked straightforward.

{{< plantuml title="The architecture we almost shipped" >}}
@startuml
skinparam shadowing false
skinparam componentStyle rectangle

[Pricing Platform] as P
[Drools] as D

P --> D
@enduml
{{< /plantuml >}}

The more we discussed it, the less comfortable we became.

## The risk of letting Drools become the next monolith

Drools was a technology choice. Pricing was a business capability.

Those two things have very different lifespans. Technologies change. Business capabilities tend to survive much longer.

A question kept coming up in our reviews: *what happens if the rule engine becomes the next monolith?* If the pricing platform depended directly on Drools, then every future decision about pricing would carry a Drools assumption. Every test would need a Drools session. Every onboarding would start with Drools concepts. Every migration would be a coupled rewrite.

We weren't worried about Drools failing as a product. We were worried about Drools succeeding as a dependency.

We didn't have a polished counter-design at the time. We just knew enough to keep asking the question. The pricing platform should not depend directly on Drools. It should depend on an abstraction we owned.

{{< plantuml title="The architecture we shipped instead" >}}
@startuml
skinparam shadowing false
skinparam componentStyle rectangle

[Pricing Platform] as P
[Business Rules Engine] as BRE
[Drools] as D

P --> BRE
BRE --> D
@enduml
{{< /plantuml >}}

That middle layer is what made the rest of the story possible. It wasn't a wrapper. It was a contract that said: pricing decides what to ask, the engine decides how to answer, and the team owns the boundary between them.

## Introducing the Business Rules Engine

Rather than exposing Drools directly to the rest of the pricing platform, we created an internal layer we called the Business Rules Engine.

The goal was simple. The pricing platform should ask for decisions. It should not care how those decisions were evaluated.

```java
RuleRequest request =
    RuleRequest.builder()
        .market("DE")
        .provider("rail")
        .currency("EUR")
        .daysBeforeDeparture(5)
        .build();

RuleResult result =
    businessRulesEngine.evaluate(request);
```

Notice what is missing. No Drools API. No Drools session. No Drools-specific concepts leaking into pricing code.

The signature of `evaluate` is the signature of the business capability. Whatever we put underneath has to honour it.

## Rules became business assets

One unexpected consequence of the abstraction was that rules stopped looking like code. They started looking like business assets.

```yaml
id: short_lead_time_markup
owner: pricing-team
reason: Increase revenue on short lead-time bookings
metric: revenue_per_search
status: experiment
expires_at: 2024-01-31
```

Instead of asking where the code was, people started asking who owned the rule and why it existed. That shift in question is the whole point of the boundary.

## The unexpected benefits

Once the abstraction held, four benefits showed up that we hadn't designed for.

### Better testing

The pricing platform could be tested without standing up a Drools session. Tests talked to the Business Rules Engine interface and mocked the engine underneath. Unit tests stayed fast. Integration tests stayed honest.

### Easier simulations

Because the engine accepted requests independent of any product flow, we could replay history through it.

{{< plantuml title="Simulating revenue impact without booking anything" >}}
@startuml
skinparam shadowing false
start
:Last 30 days of searches;
:Business Rules Engine;
:Expected revenue impact;
stop
@enduml
{{< /plantuml >}}

Feed the last 30 days of searches into the BRE with a candidate rule enabled, compare outputs against the baseline, and you have a credible estimate of impact without exposing a single customer.

### Safer future changes

Replacing the underlying engine became possible. Not easy. But possible. That alone was worth the cost of the boundary, because every engine we evaluated had a roadmap we did not control.

### Faster onboarding

New engineers learned pricing concepts first. Not Drools internals first. The boundary was a teaching tool as much as a technical one.

## The abstraction leak we constantly fought

Every abstraction leaks eventually.

Drools had powerful features. Sometimes we wanted to reach for them directly. That created tension inside the team. Should the Business Rules Engine expose those capabilities, or should it remain independent?

That struggle forced us to think carefully about which capabilities belonged to pricing and which belonged to Drools. The answer was usually unsatisfying in the moment and right in the long run: if a feature only made sense in Drools terms, it didn't belong on the BRE interface. If it expressed a business decision, it did.

The boundary held because we kept defending it.

## What I learned

Looking back, Drools wasn't the decision that aged best. The decision that aged best was refusing to let our pricing platform depend directly on it.

Technologies change. Business capabilities survive much longer.

The Business Rules Engine allowed us to focus on pricing decisions instead of implementation details. It created a stable boundary. And stable boundaries are often more valuable than perfect technologies.

## Closing reflection

Eventually we realized we were no longer building pricing features. We were building pricing capabilities.

Rules could be created. Rules could be simulated. Rules could be explained. Rules could be measured. Rules could be retired.

That realization changed how we thought about ownership. It changed how we thought about experimentation. And it changed how we thought about pricing itself.

Pricing was no longer behaving like a feature. It was behaving like a product.

Years later, I can't tell you whether Drools was the right pick. I can tell you that the layer we built on top of it is still doing its job — translating pricing decisions into a vocabulary the team owns, regardless of whatever sits beneath. That was the part that mattered. The engine was a detail. The boundary was the work.
