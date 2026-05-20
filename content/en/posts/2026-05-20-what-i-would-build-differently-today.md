---
title: "What I Would Build Differently Today"
subtitle: "The best pricing systems are not the most sophisticated. They are the ones the team can understand, test, explain, and change safely."
author: helio
layout: post
date: 2026-05-20T10:00:00+00:00
series:
  - pricing-engineering
series_order: 14
categories:
  - Engineering
  - Pricing
  - Architecture
tags:
  - pricing
  - rule-engine
  - architecture
  - retrospective
  - lessons-learned
description: "The closing pass of the series. If I were starting a pricing platform today, with the benefit of everything the first time taught me, this is the shape I would build — and the order I would build it in."
---

This is the post the series was preparing for. Thirteen posts of architecture, lessons, mistakes, and the manual hygiene we held together by hand. The question I want to answer here is the smallest one: if I were starting a pricing platform today, knowing what I know now, what would I build, and in what order?

The answer compresses most of what came before. There is little new in this post — most of it is the inverse of the mistakes from the last one, and the architectural seams from the posts before that. What is new is the *sequence*. The lessons of the series are not just the components; they are the order in which the components earn their way in.

## The shape in one frame

Before the sequence, the destination. The pricing platform I would build today has six load-bearing components:

1. A **typed Rule model** that is the contract between authored intent and runtime execution.
2. A **rule store on disk** with versioned schema, a loader that is the boundary, and a fail-closed reload.
3. A **rule engine** with an explicit matching policy, an evaluator, an executor, and a composer. One per concern; named interfaces.
4. An **explanation per Execute** that carries enough for engineer, operator, product owner, and auditor in one artifact.
5. A **shadow path** that runs a candidate alongside the active on real traffic, asynchronously, with a divergence pipeline.
6. A **synthetic traffic generator** that produces reproducible fixtures from team-authored scenarios.

When the platform is asked to grow up, two more components join:

7. A **replay-based simulation** that pairs snapshots and fixtures into a deterministic diff.
8. A **decision engine** above the rule engine that coordinates rules with models, constraints, and experiments.

The first six exist on the platform from the first month. The last two arrive when the rule engine starts being asked to do things it should not be asked to do, not before.

Around all of it, the *operability* discipline from Post 12 — owners, review dates, retirement procedures, dashboards that age — has to be designed in from the start, even if much of the implementation is manual at first.

## The order I would build it in

The architecture is the *what*. The sequence is the *when*. The sequence is where I would change the most.

**Week one: the Rule model.** Before any matcher, write the Rule struct from Post 2 and run it past three reviewers. Make the model carry what every later layer will need — Name, Description, Tags, Condition, Action, Priority, Enabled — and *no more*. Metadata goes in a sidecar. The struct is the contract; every other commitment in the system will depend on this one being right.

**Week two: the loader.** A YAML schema versioned from line one. A loader that validates, fails closed, swaps atomically. The loader does not have to do everything from day one — versioned migration tools come later — but the *shape* of the loader has to be right, because the loader is the boundary.

**Week three: the engine, one matcher.** Pick a matching policy on purpose, knowing whether the rules are independent or layered. For most pricing surfaces, this is the indexed first-match-by-priority pattern from Post 4. The engine ships with one matcher, one composer, and a typed result. The pipeline from Post 5 is explicit — receive, match, evaluate, execute, compose — even if every stage is a one-liner.

**Week four: the explanation.** Every Execute produces an Explanation. The first version is small — snapshot ID, fired rule names, result, latency per stage — but it has the schema the full version will grow into. From this moment, every escalation has an artifact to reach for.

**Week five: synthetic traffic.** Before there is production traffic to load-test against, the platform has a scenario file, a seed, and a generator that produces a fixture. The fixture is the input the test suite uses. The fixture is also what the next layer — shadow — and the layer after that — replay — will consume.

**Week six: shadow mode.** The candidate engine runs alongside the active on the synthetic traffic first, on a sample of real traffic second. The comparison log exists from this week. The divergence pipeline is small but real. Every rule change from this point forward goes through shadow before it goes live.

These six weeks are the minimum-viable pricing platform I would build. None of the work is heroic. All of it earns its way in.

After week six, the next investments are *demand-driven*. Most of the time, the platform stays in this shape for a long time. Some of the time, it has to grow up.

**When the rule engine bends, replay.** The first time the team disagrees about whether a candidate change is safe, build the replay runner from Post 10. The snapshot work is in `bre-go`; the fixture work is in `traffic-gen`; the runner that pairs them is the piece nobody has written yet. The replay diff is what ends the next disagreement.

**When the rules can no longer express the decision, the decision engine.** The first time you find rules that consult external services in their actions, or rules whose priority encodes constraints, or rules whose conditions encode experiment membership, you have the signal. Wrap the rule engine. Extract constraints into their own layer. Model and experiment seams come after.

**When the manual lifecycle hygiene starts to slip, automation.** The day somebody who did not run the original quarterly review has to run the next one is the day the spreadsheet stops being enough. The automation pattern from Post 12 — `review_after` warnings, zero-fire reports, owner directory, retirement scheduler — is what carries the practice into the system.

## The choices I would not make

The same shape inverts into the choices to avoid.

I would not build the matcher before the Rule model is settled. The matcher is downstream of the model in every way that matters; getting it right first makes the model worse.

I would not pick a matching policy by default. The four policies from Post 4 are different bets about how rules interact; the wrong default is more expensive than the slightly heavier work of picking on purpose.

I would not defer the explanation. Every day without an explanation is a day where the next escalation costs a day and a half. The cost of building it in is one struct and a listener; the cost of not is unbounded.

I would not test the matcher's internal state. Tests against bucket counts, hash distributions, and evaluation order are tests against the engine's implementation, not its behaviour. The 11 000-line suite from Post 6 is the cautionary tale.

I would not trust production traffic to test for the future. Yesterday's mix is yesterday's question. The platform has to be exercised against the questions the team has not yet been asked, which is what scenarios are for.

I would not build the decision engine before the rule engine has been operated. Premature decision engines are a tax every team that touches the system pays, and the patterns the team eventually needs are not the patterns the architect guessed in advance.

I would not assume engineers are the only users. The rule store is for the product owner who needs to edit a markup, the auditor who needs to read a rule, the operator who needs to understand a decision. Engineering ergonomics come second.

I would not optimise for creation and ignore retirement. Every rule that goes in has to have a way to come out. The retirement procedure exists before the rule that needs retiring arrives.

## The two reference repos, again

The Go code in this series lives in [`bre-go`](https://github.com/helmedeiros/bre-go) and [`traffic-gen`](https://github.com/helmedeiros/traffic-gen). Both are open-source extracts of patterns I had to learn on a production pricing system whose code I cannot show. The shape of the contracts maps across stacks; what is in those repos is the *form* of the lessons, not the *substance* of the production system that taught them.

If I were starting today, the two open repos would be one of the first decisions I would not regret. Having a place to write the design down in a language and shape anyone can read is what made the patterns survivable across context switches — including this series itself. The system at work could not be shared. The system in the open could be. The lessons live in both.

## The compression

If I had to compress the entire series into one paragraph, this would be it.

A pricing platform is not a rule engine; it is the system of components around the rule engine — loader, explanation, shadow, traffic generation, replay, decision engine, lifecycle. The rule engine is the centre of the design and the smallest part of the work. The most expensive mistakes are about which component you build first, which user you build for, and which discipline you defer because it does not feel urgent. The best pricing systems are not the most sophisticated. They are the ones the team can understand, test, explain, and change safely. The rest is implementation.

## What this series was for

The previous pricing series — [Lessons from a Pricing Platform](/series/lessons-from-a-pricing-platform/) — was about the strategy, product, and team work behind pricing decisions. This one was about the engineering work beneath them. The two are siblings. Each one alone is incomplete; both together is the shape of what pricing actually requires.

If you have read both, you have read most of what I know how to write down about pricing. If you build a pricing platform after reading them, you will not avoid every mistake from Post 13 — those are the cost of doing the work — but you will recognise the ones you are about to make, and you will have a place to look up what to do when they happen.

That is the most a series of posts can do. It cannot make the mistakes for you; it can only name them ahead of time. The platform you build will be your own. The hope is that some of the seams in it will hold because someone else's seams did not, and you have read about it before you had to live through it.

## The lesson

The best pricing systems are the ones the team can understand, test, explain, and change safely. Every architectural decision in this series was, in the end, a decision in service of one of those four verbs. The Rule struct is what makes the system *understandable*. The behavioural test suite is what makes it *testable*. The explanation is what makes it *explainable*. The shadow, replay, and lifecycle disciplines are what make it *changeable safely*.

Build for those four verbs first. Everything else is engineering. The first time you ship a pricing platform you will get some of them wrong; the second time, with the benefit of the first, you will get more of them right. The third time you might get most of them right and find that the *fifth* verb — the one this series did not cover — is the next thing to learn.

I do not yet know what the fifth verb is. When I do, there will be another series. For now, the four are the ones I can name with confidence, and the seven components above are the shape I would build to honour them.

The series ends here. The work, of course, does not.
