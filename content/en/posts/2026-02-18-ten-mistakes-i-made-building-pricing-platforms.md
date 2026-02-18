---
title: "Ten Mistakes I Made Building Pricing Platforms"
subtitle: "The expensive mistakes are never about syntax. They are about boundaries, behaviour, and ownership — the parts that look fine until they don't."
author: helio
layout: post
date: 2026-02-18T10:00:00+00:00
series:
  - pricing-engineering
series_order: 13
categories:
  - Engineering
  - Pricing
  - Architecture
tags:
  - pricing
  - retrospective
  - architecture
  - lessons-learned
  - rule-engine
description: "A personal retrospective. Ten things I got wrong while building pricing platforms, what each one cost, and what I would do differently. The mistakes are rarely about syntax — they are about which problem you decide to solve first."
---

The first time somebody asked me what I had learned from building pricing platforms, I gave them a list of techniques. A year later I realised the techniques were not the lesson. The lesson was the *mistakes* the techniques came out of, and the mistakes were rarely about code. They were about which problem I had decided to solve first, which layer I had treated as fixed when it should have been flexible, and which user I had quietly designed for at the expense of the others.

This post is ten of those mistakes. Some of them I have shipped more than once. Some of them I am still making, sometimes, in the corners where I have not learned to recognise them.

## 1. I started with the engine instead of the rule model

The first version of my first rule engine had a beautifully designed matcher and no real Rule type. The Rule was a `map[string]interface{}` because that was the shape the matcher needed; everything else was *future work*. I wrote the matcher first because the matcher felt like the hard part.

The matcher was not the hard part. The Rule type was the hard part. Without a typed Rule, the loader could not validate. The tests could not assert anything beyond what the matcher already knew. The explanation could not name the fields. The whole engine was a function around a shapeless dictionary, and every layer that wanted to add structure had to re-derive it from the keys it happened to find.

We rebuilt the Rule type six months in. The matcher hardly changed; everything around it did. If I were starting now, I would write the Rule struct on day one and not write a matcher until the struct had survived a week of code review.

## 2. I treated matching as simple

The first matcher I shipped was the obvious one: walk the rule set in insertion order, evaluate each condition, collect every match. It worked at 50 rules. It worked at 200. It crawled at 800 — by which point the rule set was a year old and re-architecting was painful.

The mistake was not the linear matcher. The mistake was *treating matching as a default* rather than a deliberate design choice. I had not asked whether the rules were independent or layered, whether the actions composed or collided, whether the ordering encoded precedence or accident. The matcher I picked answered none of those questions because I had not asked them.

The Friday-night rewrite was not the cost. The cost was that, by the time we rewrote, two years of rule files encoded assumptions about evaluation order that nobody had documented. Half the migration work was excavating which rule was relying on insertion-order semantics it did not know it was relying on.

## 3. I forgot explainability

The first "why was this customer charged?" question took us a day and a half to answer. We had logs, but the logs said `engine.Execute completed` with a result and no detail. We had the rule set, but no idea which rules had fired. We had the customer's request, but had to reconstruct the engine state from `git` history because we had not stamped the snapshot.

That day and a half taught me that explainability is not a debug aid. It is the system's contract with the operator, the auditor, the product owner, and the engineer. I had built the engine for one user — the engineer — and not realised the system had four users, and that the engineer was the one who needed explainability *least* because they could read the source.

Every pricing engine I have built since produces an explanation per Execute, sampled or full, stored or replayable. The cost of explainability is one struct and a listener. The cost of not having it is every escalation taking a day and a half.

## 4. I let priority become hidden governance

When the priority field was first proposed, somebody asked what numbers we should use. I said "use any integer; whatever feels right." Two years later the priority field looked like the floor of a bar at closing time. Some rules were at 1000 because they were "very important." Some were at 999 because they were "almost as important as compliance." A few were at 437 because somebody had thought hard for ten minutes and produced a number.

The mistake was treating priority as a *value* rather than a *governance artifact*. Priority is not arithmetic; it is policy. The integer is the surface; the policy is which tier the rule belongs in, which team owns the tier, what conflicts mean when they happen inside the tier. Without an explicit ladder of named tiers, every priority decision was a negotiation, and the negotiations went to whoever shouted loudest.

The fix was a four-tier ladder — compliance, revenue, experiment, default — with rules placed deliberately. The fix was easy. The lesson was harder: any number that ends up as policy needs to be governed as policy, no matter how innocuous it looks on the way in.

## 5. I tested implementation instead of behaviour

The 11 000-line test suite from Post 6 was real. It passed for fourteen months while the engine quietly produced wrong markups. Most of those 11 000 lines tested the matcher's internal state: bucket counts, hash distributions, the order in which conditions were evaluated. Few of them tested *what the customer was charged*.

When we refactored the indexed matcher, every test broke. None of the breakage corresponded to a behaviour change. The customer was still charged the same number; the matcher just got there through a different bucket structure. We spent six weeks updating tests that were testing the wrong thing — and during those six weeks, an actual behaviour change slipped through because the test we needed had never been written.

The lesson, in one sentence: a test that breaks when you refactor but the behaviour does not change is a test that should not have been written. A test that passes when you refactor but the behaviour silently regresses is a bug in the suite.

## 6. I trusted average traffic

The first load test I ran on a new pricing engine used four million requests from production logs. The plan was to replay yesterday and confirm the engine handled it. The plan worked. The engine handled it. We shipped. Two days later a single market spiked traffic 8x because of a holiday, and the engine fell over.

The replay had carried yesterday's mix. Yesterday's mix had not had a holiday spike. I had tested the engine on a question I had already answered and not on the one I needed to answer.

The fix was synthetic traffic with explicit scenarios for the cases I was worried about. The lesson is more general: production traffic is *yesterday's* distribution. It is the wrong default for testing tomorrow. Synthetic traffic, with the team's hypotheses about tomorrow encoded as scenarios, is the right default. Production traffic is a regression test for past behaviour, not a stress test for future shape.

## 7. I ignored stale rules

I knew there were rules nobody could explain. They had been firing for years. They were not causing trouble. I left them alone because they were "working," and I had real work to do.

Six months later one of those rules interacted with a new rule we had shipped — the conditions overlapped, the actions stacked, and the result was a 0.5% markup overcharge on a slice of customers we had not bothered to consider because the old rule had been silent on them for two years. The postmortem recommended a "retirement procedure." The retirement procedure did not exist. It existed only because of the postmortem.

The lesson is in two parts. The first part: rules that nobody understands are debt that compounds; ignoring them is paying interest. The second part: a *procedure* for retiring rules has to exist before the rule you want to retire arrives, because the moment you need it, you do not have time to design it.

## 8. I made simulation too late

Shadow mode was the third thing I built. The first thing was the engine, the second was the rule loader, the third — finally — was shadow mode. By then we had been shipping rule changes for eighteen months by intuition, observation, and a small amount of prayer. Several of those changes shipped behaviours we did not intend.

I have wanted shadow mode since week one of every pricing platform I have worked on since. The lesson is not that shadow mode is hard; it is that *the case for shadow mode is invisible until you have lived without it*. Until your first surprise rollout, shadow mode looks like infrastructure overhead. After your first surprise rollout, it looks like the thing you should have built first.

I would not build a pricing platform now without shadow as a week-one component. Even a crude version — log the active and the candidate side by side, compare offline — earns its keep the first time the candidate is wrong in a way nobody predicted.

## 9. I overbuilt before I had learned

The opposite mistake. On a project that came right after a hard incident, I designed the decision engine in advance — context, model integration, constraint layer, experiment overlay, the whole shape from Post 11. I built it before the rule engine underneath had been operated for six months.

The decision engine sat unused for most of its first year. The patterns I had baked in did not match the patterns the rule engine actually grew into. By the time the team needed decision-engine capabilities, half my early decisions were wrong and the other half were costing us nothing because we were not using them.

The lesson is timing. Build the layer that is *bending*, not the one that might bend in the future. A pricing platform that needs a decision engine reveals itself; you do not have to guess. A pricing platform that does not need one yet does not benefit from having one, and the architectural cost of carrying it is paid every day.

## 10. I assumed engineers were the only users

The rule store was a YAML file in a `git` repo. The schema was loosely documented. The error messages assumed familiarity with the loader's source code. The dashboards were built for the on-call engineer. None of this was unreasonable — engineers had built the system, engineers were operating it, engineers were the users I had in mind.

Then product wanted to edit a markup. Marketing wanted to launch an experiment. Compliance wanted to read a rule before signing off. None of them could. Every rule edit routed through engineering, queueing every change, slowing every decision, and centralising authority in the team that did not want it. The system had been built for one user — the engineer — and the engineer was, surprisingly, the user who needed it the *least*.

The fix took quarters. The fix was making the rule the artifact, not the file: a UI for editing, an API for reading, an audit log for reviewing, error messages that named *what was wrong with the rule* and not *which line of the loader failed*. The lesson, which I keep finding new corners of, is that the artifact's audience is wider than the team that builds it. Designing for the wider audience first is what makes the team's role sustainable later.

## The shape underneath the mistakes

Ten mistakes is a list. The shape underneath the list is shorter:

I built for the wrong user. I built before I had learned. I treated *defaults* as decisions. I treated *decisions* as defaults. I let governance live in fields the system did not police. I optimised for creation and ignored retirement. I tested what was easy and not what mattered. I trusted what I had seen and not prepared for what I had not.

Several of these are mistakes the architectural posts of this series have been trying to teach around — and the most useful ones to write down are the ones the series has not yet covered directly. The narrow Rule struct, the explicit matching policy, the explanation-first design, the priority ladder, the behavioural test suite, the synthetic traffic, the retirement procedure, the shadow-first rollout, the build-when-bending rule, the artifact for the non-engineer: each one is the antidote to one of the mistakes above, and each one is a habit I keep having to renew because the mistake keeps wanting to come back.

## A note on what would be the eleventh

The honest mistake list never ends at ten. The eleventh, in my list, is one I am still living through and have not yet learned to name well: assuming the previous incident is the next incident. Every postmortem I have written tightened the system against the failure mode that just happened. The next failure was usually a different one. The defences accumulated — explanation, replay, shadow, lifecycle hygiene — but the cycle of "incident, harden, surprise, incident" did not stop.

I do not know what to do with that yet. I think part of the answer is in the post-mortem ratio between *deep defence* (against the kind of failure that just happened) and *broad coverage* (against the kind that has not). I have leaned heavily toward depth in my career. I am trying to lean more toward breadth in the platforms I am building now.

## What comes next

The final post in this series is the closing pass — what I would build differently today, with the full benefit of these ten mistakes and the architectural posts that have come before. It is the shortest post of the series because, by now, much of the answer is compression.

What I want to say upfront, before that post: the mistakes above are the cost of building a real pricing platform. Some of them are unavoidable; some are signals that the people doing the work have not done it before. Both kinds are valuable. The team that has paid for these mistakes is the team that can build the next pricing platform faster — not because they will avoid the mistakes, but because they will recognise them sooner.

## The lesson

The mistakes are rarely about syntax. They are about which problem you decide to solve first, which layer you treat as fixed when it should be flexible, which user you quietly design for, and which discipline you defer because it does not feel urgent. The corrections, when they come, are usually structural: the type that should have been narrower, the matcher that should have been chosen on purpose, the explanation that should have been a first-class output, the retirement procedure that should have existed before you needed it.

I have shipped most of these mistakes more than once. The expensive ones I have shipped recently; the cheap ones I now spot in the first design review. The most useful thing I can do for somebody else building a pricing platform is to name these mistakes openly, so that when they encounter the same pattern, they recognise it as a pattern and not as a problem unique to their system.

The next post is the positive form: not the mistakes, but the build I would attempt if I were starting today with what I now know. Most of what I would do differently is in the negatives above. The positive shape is what falls out when you put the negatives in series.
