---
title: "The Lifecycle of a Pricing Rule"
categories:
  - Engineering
  - Governance
  - Pricing
  - Product
date: 2026-06-07
tags:
  - pricing
  - rule-engine
  - governance
  - experimentation
  - platform-engineering
  - product-management
series:
  - pricing-platform
series_order: 13
description: "What my team had to learn about pricing rules after they shipped — ownership, expiration, deletion, and governance as answerability."
subtitle: "A pricing platform isn't a collection of rules. It's the institutional memory of every decision the business has ever doubled down on or backed away from."
---

A pricing review, a Wednesday afternoon. Somebody pointed at the dashboard and asked why the markup for a particular product in Germany was 3.7%. Not 3, not 4. Specifically 3.7.

The room went quiet.

The rule had been live for almost two years. It applied to a meaningful slice of bookings in that market. Nobody in the room had introduced it. The original ticket linked from the commit was archived. The Slack thread referenced in the ticket no longer existed, because somebody had pruned old channels. The product manager who had owned the experiment that produced the rule had moved teams. The analyst who had measured it had left the company.

The rule was still running. Still touching real money. And nobody in that meeting could explain why.

I went back to the rule registry that week and ran a count. We had a little over six hundred rules in production. I asked the team how many of those we could confidently explain — origin, owner, current purpose, last review. The honest number was somewhere in the high three hundreds. The rest were just there.

That was the day my team realised our problem. We had spent years building a pricing platform — a Business Rules Engine, an experimentation setup, segmentation work, simulators for evaluating changes before customers saw them. Each of those pieces had answered a real question at the time. None of them addressed what happens to a rule after it ships.

## We had treated ownership as a creation question

We weren't being negligent. We had ownership. The pricing platform's PR process required a reviewer on every rule. Our internal registry tracked who had introduced each rule, when it had landed, and which experiment it had come from. We had run that process with discipline for years.

It hadn't helped.

The reason became obvious once we named it. Every piece of ownership we had built was attached to *creation*. Who can add a rule. Who reviews the addition. Who signs off on the experiment that produces it. None of that ownership extended past the moment the rule went live. After that, the rule belonged to the platform — which is to say, to nobody specific.

That was the gap. Ownership was a creation question for us. It needed to be a lifecycle question.

{{< plantuml title="The lifecycle of a rule, as we eventually had to model it" >}}
@startuml
skinparam shadowing false
state "Created" as C
state "Running in production" as R
state "Up for review" as Rev
state "Retired" as Ret

[*] --> C : Observation → Hypothesis
C --> R : Deployment
R --> Rev : Expiration / signal / event
Rev --> R : Keep or change
Rev --> Ret : Retire
Ret --> [*]
@enduml
{{< /plantuml >}}

The diagram looks obvious in retrospect. At the time, the right-hand side of it — *Up for review*, *Retired* — was the part that didn't exist as a first-class concept in our platform. We had Created. We had Running. The rest we left to good intentions.

## Iteration 1: expiration dates

The cheapest intervention we could try was an expiration date.

We changed the registry so every new rule required an `expires_at`. Anywhere from a week to a year, depending on what the rule was for. When the date hit, the rule didn't auto-delete — that would have been too brittle for revenue-critical code — but it lit up in the dashboard, and the owner got a notification asking whether to keep it, change it, or retire it.

That alone retired dozens of rules in the first quarter. Most were experiments that had quietly graduated into permanent code without anyone deciding they should. A few were market-specific overrides whose markets had since unified. A couple were patches for incidents nobody fully remembered.

But the intervention came with a second-order problem we hadn't anticipated. When an expiration hit, the path of least resistance was to extend it — bump the date, leave the rule running, move on. Some owners extended the same rule four or five times in a row, each extension carrying less context than the last. The forcing function was working. The forcing wasn't strong enough.

## Iteration 2: counting retirement next to creation

The next iteration was about what we measured.

For two years, the platform's dashboard had reported how many rules we shipped per quarter. It was the metric the team and our stakeholders looked at. We added a second number next to it: how many rules we retired in the same period. It was a one-column change. It changed something about how we held pricing reviews.

A quarter where we shipped twelve rules and retired one started looking conspicuously different from a quarter where we shipped eight and retired six. The second one was a more useful platform. The metric finally said so out loud.

We also added one line to the rule-creation PR template:

> *What would have to be true for us to retire this rule?*

That question, asked at creation, did more for lifecycle hygiene than any process we built afterwards. A rule whose author couldn't answer it was a rule we already knew we wouldn't be able to retire later.

## Iteration 3: governance as answerability

The third iteration came from onboarding.

Two new engineers joined the team. We sat them down with the registry and asked them to spend a week trying to understand any twenty rules of their choice. They came back frustrated. The owner field told them who was responsible today, but not why the rule existed. The metric field told them what we said we'd measure, but not what we had actually seen. There was meant to be a comment somewhere from two years ago that explained the original hypothesis. They didn't find it.

Once we saw the platform through their eyes, the word *governance* finally meant something concrete. It wasn't approvals. It wasn't committees. It was being able to answer five questions about every rule still running in production:

- Why does this rule exist?
- Who owns it?
- When was it introduced?
- What outcome was it trying to create?
- Is it still working?

A team that can't answer those questions doesn't have governance. It has history. The two look identical from the outside. They diverge fast the moment something goes wrong.

We didn't formalise governance with a process. We required those five answers to exist — in plain language, in the registry, next to the rule itself — for every new rule. Old rules got the same treatment whenever somebody touched them. Within a year, you could read a rule and know not just what it did, but why we had bothered with it.

## The lifecycle moved with the platform

The lesson didn't stay neatly inside the rules layer. When we added models a year later, the same problem appeared one layer up. A model has assumptions. Assumptions age. The training data has a date stamp. The objective function reflects what the business cared about when the model was last refreshed. None of that survives without intervention.

When we added simulators, the lesson appeared one layer up again. Simulator scenarios get stale. The "edge cases nobody planned for" stop being edge cases when the platform's behaviour shifts. A scenario that catches nothing for two quarters is no longer a safety net.

Better technology hadn't removed the lifecycle problem. It moved it. Rules need review. Models need retraining. Experiments need conclusions. Simulators need retirement. Mature platforms acknowledge that instead of pretending the work can be automated away.

## What I learned

The mental shift wasn't really about rules. It was about duration.

For years, the team thought about a pricing change the way you think about a feature: adoption, launch, ramp, success. *Duration* was implicit. A rule lived until it didn't, and *didn't* rarely happened on purpose.

Once we started thinking about duration with the same seriousness we gave adoption — building it into the registry, into the PR template, into the dashboard, into the reviews — the platform stopped getting heavier as it got smarter. That single shift in posture mattered more than any of the three iterations on their own.

## Closing reflection

A pricing platform isn't a collection of rules. It's the institutional memory of every decision the business has ever doubled down on or backed away from. Without intervention, that memory frays. The decisions stay; the reasons leak.

The technical work is to keep the memory honest as time passes — so the system remembers not just what it does, but why it does it, and when that reason expires.

That is mostly the work nobody schedules. It happens between features, between launches, between incidents. Looking back, it's the work I'd most want a team I joined today to be already doing.
