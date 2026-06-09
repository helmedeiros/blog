---
title: "Matching Rules at Scale"
subtitle: "Most rule engine bugs are not in the actions. They are in the way the engine decided which rule was supposed to fire."
author: helio
layout: post
date: 2025-08-20T10:00:00+00:00
series:
  - building-pricing-systems
series_order: 4
categories:
  - Engineering
  - Pricing
  - Architecture
tags:
  - pricing
  - business-rules
  - rule-engine
  - matching
  - architecture
  - algorithms
description: "Matching semantics decide which rule fires when more than one could. This post walks the four common policies, the operators they support, and the bugs each one hides."
---

A customer once got charged a 5% markup on top of a 3% markup, on the same booking, on the same line item.

Both rules were correct. Both rules matched the facts. The engineer who wrote the second rule had not noticed the first one existed; the engineer who wrote the first one had moved teams a year before. The engine was an old in-house thing that evaluated every rule in insertion order, applied every matching action, and combined them additively. Neither author was wrong. The system was.

That conversation, with a refund attached, is where I learned that *matching* is the part of a rule engine that most teams build twice. The first version is whatever the first author thought "matching" meant. The second version is what the system actually needed. The action layer above and the loader layer below take most of the credit; matching takes most of the bugs.

This post is about the four matching policies that a real engine has to choose between, the operators each one supports, and the shape of the bug each one hides. The reference, again, is [`bre-go`](https://github.com/helmedeiros/bre-go), which ships four adapters behind the same `engine.Engine` port: insertion-order all-match, insertion-order first-match, priority-ordered first-match, and an indexed sub-linear matcher.

## The four matching policies

You can plot every rule engine on two axes: how many matches it acts on, and how it picks among them.

| Policy | Acts on | Resolves ties via | Reads like |
| --- | --- | --- | --- |
| Insertion-order first-match | The first rule that matches | Position in the file | A decision table |
| Insertion-order all-match | Every rule that matches | None — every match acts | A pipeline of effects |
| Priority-ordered first-match | The matching rule with the highest priority | An integer ladder | A precedence policy |
| Specificity-ordered | The most specific matching rule | Count of conditions, or weighted | A conceptual hierarchy |

Each of these is a different bet about how the rules in your system relate to each other. If you pick the wrong one, no amount of clever rule authoring will save you.

### Insertion-order first-match

The simplest engine reads rules top-down and returns on the first match. `bre-go`'s `engine/firstmatch` adapter does exactly this: evaluate in insertion order, return on the first matching rule, never evaluate the rest.

This is what most people imagine when they say "a rule fires." It is what a decision table does. It is what every router I have ever debugged does. The mental model is small.

The bug is positional dependency. Reorder the file and the answer changes. A rule that fires for German short-lead-time bookings has to be above the rule that fires for *all* German bookings, or the second one will eat the first. Engineers who add a new rule at the bottom of the file often discover, six months later, that it has never fired. The file order is now load-bearing, and nobody told the YAML.

```yaml
# Order matters here. The second rule will never fire.
- id: germany_markup
  when: { market: { eq: DE } }
  then: { type: set_markup, value: 2.0 }

- id: germany_short_lead_time_markup
  when:
    market: { eq: DE }
    days_to_departure: { lt: 7 }
  then: { type: set_markup, value: 3.0 }
```

First-match is a fine choice when the rules genuinely have a natural order — routing tables, fallback chains, override hierarchies. It is a poor choice when the rules are independent policies that happened to be written in the same file. The team has to know which world it is in.

### Insertion-order all-match

The dual policy: walk every rule, accumulate every match, run every action. `bre-go`'s `engine/inmemory` adapter is the canonical shape — every rule that matches contributes; the listener counts matches; the last action wins on `Output`; every match appears in `Matched`.

This is what you want when rules are *additive* policies. Three markups can stack. Six tags can apply. The matching layer's job is just to find everything; the action layer's job is to combine.

The bug is collision. Two rules that each set the same field with different values silently collide; the engine has to choose one and the choice is implicit. The customer charged twice in the story above? All-match engine, accumulating markups, no collision detection.

All-match works well when the actions are *commutative*. Adding tags is commutative; order doesn't matter. Setting a price is not commutative; the last write wins, and "last" depends on insertion order, which depends on the file the team has been editing for two years. The same positional dependency the first-match policy has, now baked into the result instead of the decision to evaluate.

### Priority-ordered first-match

Priority replaces "position in the file" with "integer in the rule." `bre-go`'s `engine/priority` adapter walks rules from highest Priority down; ties break on registration order; the first match wins.

This is what most production systems eventually settle on for *decision* engines: choose one rule, choose it deterministically, let the rule author state the precedence explicitly.

```yaml
- id: compliance_markup_override
  priority: 1000
  when: { regulated_market: { eq: true } }
  then: { type: set_markup, value: 0.0 }

- id: germany_short_lead_time_markup
  priority: 500
  when:
    market: { eq: DE }
    days_to_departure: { lt: 7 }
  then: { type: set_markup, value: 3.0 }

- id: germany_baseline_markup
  priority: 100
  when: { market: { eq: DE } }
  then: { type: set_markup, value: 2.0 }
```

The bug here is more subtle. Priority is a number, and numbers are negotiable. The engineer who wants their rule "almost as important as compliance" will quietly file a rule at 999. The engineer who wants their experiment "above the baseline but not too far" will pick 437. After two years the priority field looks like the floor of a bar at closing time.

The defence, from Post 2: priority is an integer ladder, not a free integer. The ladder has named tiers. New rules go into a tier. Inter-tier ties are surfaced at registration time. The discipline is on the loader, not on the engine.

### Specificity-ordered

The seductive idea: *the most specific rule wins*. Specificity is intuitive. A rule with three conditions is more specific than a rule with one; the three-condition rule should beat the one-condition rule, because it describes a narrower world.

This is the matching policy CSS uses. It is also the matching policy nobody implements in business rule engines, because once you try to define "specific" precisely, you discover it is two different things.

**Specificity by condition count.** Three conditions beats one condition. Simple to compute. Fails the moment one of the conditions is a tautology like `enabled: true`. The author can now win the contest by adding meaningless terms.

**Specificity by weighted dimensions.** Each condition field has a weight; you sum the weights of the matched conditions. This works but the weights are now governance — exactly the problem priority had, except weights are per-field instead of per-rule. The loader has to enforce the weight table. The change-management process has to surface weight edits as policy changes.

I have never built a specificity-ordered engine for production. I have *thought* about building one twice. Both times the team that wanted it discovered, halfway through the design, that what they actually wanted was priority with better hygiene around the ladder. The intuition of specificity is right; the operational properties are wrong.

## The operators the matcher has to support

A matching policy is only as expressive as the operators its conditions support. Pick too few and the rule authors will smuggle expressions into the action layer. Pick too many and the index can't help you.

### Equality

`market == DE`. The cheapest condition there is. Every rule engine supports it. Every index is built around it.

In `bre-go`'s indexed engine, equality conditions are *bucket-key contributors*. The engine walks the typed Condition tree at `Build()`, finds every `StringCondition{Op: OpEq}` and `SetCondition{Op: OpIn}` clause, and uses those fields to build the bucket keys. At Execute time, the matcher hashes the request's fact values and looks up the bucket. The result is sub-linear in the number of rules: at 10 000 rules, equality-dominated matching is hundreds of times faster than the linear adapter on the same input.

### Set membership

`market IN (DE, FR, IT)`. The natural extension of equality. Same indexing story: the engine fans out one rule into multiple bucket keys (DE → rule, FR → rule, IT → rule). `bre-go`'s indexed engine accepts this as long as the fan-out stays below a cap (1024 by default); above that, it returns `FanoutTooLargeError` because the index would consume more memory than it saves.

The bug is the fan-out you don't see coming. A condition that says `customer_segment IN (...)` with five values is fine. The same condition six months later, after marketing added every segment they could think of, is sixty values. The condition still validates. The bucket count multiplies. The index quietly becomes a memory hog. Loader-level diagnostics earn their keep here.

### Inequality and negation

`flagged != true`. `currency NOT IN (BRL, ARS)`. These are *post-filter* conditions in `bre-go`'s indexed engine: the engine cannot use them to narrow the candidate set, so it evaluates them after the bucket lookup against the candidates the indexed terms produced. Adding a negation does not make the rule un-indexable as long as the rule still has at least one indexable term; pure-post-filter rules are rejected with `ErrNoIndexableTerms` because they would force the matcher into a linear walk.

The shape that follows from this is *rules need at least one positive equality or set-membership term to be sub-linear*. That is a constraint the rule authors will resist. It is also the constraint that turns a rule engine from O(N) into O(K).

### Ranges

`days_to_departure < 7`. `amount BETWEEN 100 AND 500`. Numeric and date ranges. `bre-go`'s `engine/parser.RangeCondition` is inclusive over `float64`, with `math.Inf(±1)` available for half-open intervals.

Ranges are post-filter, like negations. The index doesn't help; the matcher walks the candidate set and evaluates each rule's range against the request's numeric facts. The cost is small in practice, because the candidate set has already been narrowed by the equality terms — but only if the rule has at least one equality term. A rule that is *only* a range is a linear-walk rule.

### Wildcards

`market: *`. A condition that matches any value. There are two ways to model this.

The wrong way: a special operator `Any` that the matcher has to handle as a separate case. This works but it bifurcates the matching path.

The right way: don't store the field at all. A condition that matches any value is *the absence of a condition*. The rule doesn't constrain that field; the matcher doesn't look at that field for that rule. `bre-go`'s parser produces no Condition node for a missing field, which makes the matcher's job trivially uniform: every condition that exists is checked; every field not mentioned is by definition unconstrained.

This is the operator decision that pays off most quietly. The team doesn't have to debate "what counts as a wildcard" — there is no wildcard; there are conditions and absent conditions. The matcher logic stays small.

## Multi-dimensional matching

Real pricing rules touch many fields at once. A single rule that says *Germany AND rail AND short-lead-time AND mobile* has four dimensions. The matcher has to find the rules whose dimensions all match the request.

The linear approach is to walk every rule and evaluate every condition. At 100 rules this is fine. At 1000 rules it is starting to hurt. At 10 000 rules it is the bottleneck.

The indexed approach is to build the cross-product of bucket keys. For each equality and set-membership term, the engine builds a hash bucket. At Execute time, the matcher hashes the request's facts and looks up the candidate rules. The candidate set is small. Post-filter conditions are evaluated against the candidates.

{{< plantuml title="The indexed matcher: hash buckets narrow the candidate set, post-filters refine it" >}}
@startuml
skinparam shadowing false
skinparam componentStyle rectangle
skinparam defaultFontName "Helvetica"

rectangle "Request facts\nmarket=DE\nchannel=rail\ndays=4\ndevice=mobile" as F

rectangle "Bucket index\n(built at Engine.Build)" as B {
  rectangle "market=DE\n→ {R1, R7, R12}" as B1
  rectangle "channel=rail\n→ {R7, R12, R18}" as B2
  rectangle "device=mobile\n→ {R7, R12, R20}" as B3
}

rectangle "Candidate set\nintersection: {R7, R12}" as C
rectangle "Post-filter\ndays_to_departure < 7\n→ {R7}" as PF
rectangle "Match\nR7" as M

F --> B
B --> C
C --> PF
PF --> M
@enduml
{{< /plantuml >}}

The shape of the win, from `bre-go`'s scientific reports: at 10 000 rules, indexed matching using the v0.16 binary snapshot format is 2.93× faster than the linear adapter loaded from CSV. At 100 000 rules the gap widens. The numbers move with workload shape — wide buckets help less than narrow ones — but the asymptotic behaviour is the design choice.

The design cost is the constraint on the rule authors: every rule needs at least one indexable term. The runtime gain is the constraint paying for itself.

## Tie-breaking when two rules match

The other half of matching is what happens when more than one rule matches. The four policies above each handle this differently, and they each have a failure mode.

| Policy | Tie-break rule | Failure mode |
| --- | --- | --- |
| Insertion-order first-match | The earlier rule wins | Reorder breaks behaviour silently |
| Insertion-order all-match | All matches act | Conflicting actions collide on the same field |
| Priority-ordered first-match | Higher priority wins; insertion order is the fallback | Priority drifts into governance |
| Specificity-ordered | More specific wins | "Specific" is two different things |

The dishonest defence is to pretend the failure mode does not exist. The honest defence is to surface the failure to the team at load time.

### Conflict detection at registration

The two policies that need conflict detection most are all-match and priority-ordered first-match. The check is the same: *for any pair of rules, can both match the same request?* If yes, the engine has to know how to resolve, and the team has to know which one will fire.

`bre-go`'s `engine/indexed.Engine.Diagnose()` does a tier-1 version of this. It scans rule pairs and reports rules that can never fire because an earlier higher-priority rule already shadows them. The check is conservative — it skips pairs where the shadow candidate has post-filter terms, so false positives are zero by design.

The cost of running Diagnose at startup is O(N² × F) where F is the average post-filter count. At 1000 rules this is milliseconds. At 100 000 rules it is seconds, which is why Diagnose is a startup or admin endpoint check, not a per-request one.

The benefit is non-negotiable: the team finds out about shadowing before production does. A dead rule is a rule that wasted somebody's time to author and will waste somebody else's time to investigate when "it should have fired."

### Conflict resolution as policy

The cases Diagnose cannot catch — two rules that both legitimately match because they were designed to — need an explicit resolution policy. The cleanest shape I have seen:

```yaml
resolution:
  fields:
    markup_percentage: sum   # additive markups stack
    base_price:        last  # last write wins, ordered by priority
    provider:          fail  # collision is a registration error
```

The resolution policy turns implicit behaviour into explicit policy. The team agrees, in writing, what happens when two rules touch the same field. The engine refuses to load a rule set that violates the policy.

This is one of those design moves that looks like extra work and turns out to be the cheapest possible insurance. The customer charged twice in the opening anecdote? The story ends with us adding a `provider: fail` line to the equivalent file. Two new rules in conflict are now a CI failure, not a refund.

## The bug shape: where matching goes wrong

Three patterns account for most of the matching bugs I have shipped or watched ship.

**The shadow.** Rule B is identical to a subset of rule A's conditions. A fires first, B never fires. Six months later, when somebody disables A, B starts firing — and the system behaves differently than anyone expects. The fix is conflict detection at load time. The defence is to enforce that every rule must be reachable.

**The reorder.** Rule order changed in a refactor. A first-match adapter changes behaviour. Nothing in the test suite caught it because the tests were written against a specific order. The fix is to mark every test fixture with the policy assumption it relies on. The defence is to discourage first-match for rules that are not naturally ordered.

**The collision.** Two rules both set the same field. The all-match engine picks one of them. The picked one is a function of insertion order, which is a function of authoring history. The fix is the resolution policy above. The defence is to surface field collisions as a load-time error.

Each of these bugs is cheap to prevent and expensive to debug. The cost of prevention is one engineering pass over the matcher; the cost of the debug is whatever the customer thought they were paying for. The asymmetry is large enough that the matcher deserves more attention than the action layer almost always gets.

## The engineering lesson

The action layer of a rule engine is glamorous. It is where the markups are computed, where the experiments are applied, where the decision is *made*. It is also where most engineers focus the design effort. The action layer is where the meeting goes.

The matcher is unglamorous. It looks like it does nothing: it picks rules from a list. Picking rules from a list is not the work — *deciding which rules to pick from which list* is the work, and that decision is the matching policy.

Pick a matching policy explicitly. Surface its failure mode in the loader. Build conflict detection at startup. Make the engine refuse to load a rule set that violates the resolution policy. None of these are runtime concerns. They are all loader-time concerns. By the time a request arrives, the matching policy has already been validated, the conflicts have already been caught, and the resolution rules have already been agreed.

That is what scale means in this context. Scale is not 100 000 rules per second. Scale is 10 000 rules edited by 30 people over five years, with the system still behaving the way the team agreed it would. The matcher is what makes that survivable.

## What comes next

The next post is the evaluation pipeline — the engine as a sequence of stages that take loaded rules and request facts and produce a result. Matching is one of those stages. So is condition evaluation, action execution, result composition, and explanation. The pipeline is what turns the matcher's "these rules fire" into a result the caller can act on.

After that, the testing post takes the whole pipeline apart and shows how to write tests that protect the behaviour, not the implementation. And the post after that is explainability, which loops back here: every conflict detected at load time becomes a line in the explanation, every shadow rule becomes a warning, every priority decision becomes a recorded reason.

For now, the matcher is the architecture decision. Most of the rule engines I have seen fail in production failed in the matching layer, not in the actions. The matcher is the one part of the engine that has to be honest about its tradeoffs, because it cannot fake them. Pick first-match if your rules are ordered. Pick all-match if your actions are additive. Pick priority if your team can hold an integer ladder. Skip specificity until you are ready to defend the weight table.

The customer charged twice eventually got their refund. The engine got a resolution policy. The two engineers who wrote those original rules never met. The system stopped letting that mistake happen, which is what a matcher is for.
