---
title: "Building a Rule Evaluation Engine"
subtitle: "An engine that runs in one opaque step is an engine you cannot debug. Make the stages explicit and the bugs have nowhere to hide."
author: helio
layout: post
date: 2025-09-24T10:00:00+00:00
series:
  - building-pricing-systems
series_order: 5
categories:
  - Engineering
  - Pricing
  - Architecture
tags:
  - pricing
  - business-rules
  - rule-engine
  - architecture
  - observability
  - go
description: "A rule engine is a pipeline. This post pulls the pipeline into named stages — load, validate, match, evaluate, execute, compose, explain — and shows how the boundaries become observability."
---

The escalation arrived at 11:14pm: *the markup rule fired on the wrong customer*.

It hadn't. Three of us spent the next forty-five minutes proving that. The fact set was correct. The rule was correct. The action ran with the inputs we expected. The result was what the rule said it should be. The customer was the one we expected to charge.

What had actually happened was that the rule fired, the action executed, and the *downstream consumer* mapped the result onto a different field than the one the team had agreed on. The bug was three layers above the engine. We spent forty-five minutes proving the engine wasn't lying because the engine had no way to prove it. Execute went in; a number came out; the middle was a black box.

The next morning we pulled the engine apart into stages. From then on, every Execute produced a record that named the matched rules, the evaluated conditions, the actions executed, and the result composed. The next time somebody escalated, the answer took two minutes.

That is the rest of this post. An engine that runs in one opaque step is an engine you cannot debug. An engine with explicit stages is an engine that explains itself.

## The pipeline

A rule engine is a pipeline. Read it backwards from `Execute(ctx, facts) → Result`:

```
Facts in
   │
   ▼
┌──────────────────────────────────────────┐
│ Load        (covered in post 3)          │
└──────────────────────────────────────────┘
   │
   ▼
┌──────────────────────────────────────────┐
│ Validate    (covered in post 3)          │
└──────────────────────────────────────────┘
   │
   ▼
┌──────────────────────────────────────────┐
│ Receive facts                            │
│   normalise, type-check, complete        │
└──────────────────────────────────────────┘
   │
   ▼
┌──────────────────────────────────────────┐
│ Match                                    │
│   candidate set ← matcher.Match(facts)   │
└──────────────────────────────────────────┘
   │
   ▼
┌──────────────────────────────────────────┐
│ Evaluate                                 │
│   for each candidate: condition.Eval     │
│   accumulate post-filter results         │
└──────────────────────────────────────────┘
   │
   ▼
┌──────────────────────────────────────────┐
│ Execute                                  │
│   action(facts) for every fired rule     │
└──────────────────────────────────────────┘
   │
   ▼
┌──────────────────────────────────────────┐
│ Compose                                  │
│   combine action outputs per policy      │
└──────────────────────────────────────────┘
   │
   ▼
┌──────────────────────────────────────────┐
│ Explain                                  │
│   emit record of every decision boundary │
└──────────────────────────────────────────┘
   │
   ▼
Result + Explanation out
```

Each stage is a function. Each stage has inputs and outputs. Each stage can be tested without the others. Each stage can fail with a typed error that names *which* stage failed, not just *that* something failed.

This is the design rule for the rest of the post: **every boundary in the pipeline is observable**. The team can ask the engine "what happened at this point?" and the engine has an answer.

## Receive facts: the contract at the edge

Facts are what the engine evaluates against. The `Execute` signature defines what the engine accepts:

```go
// engine.Engine.Execute is the public hot-path entry point.
func (e *Engine) Execute(ctx context.Context, in Request) (Result, error)
```

In `bre-go`, `Request` carries `Input` as `interface{}` and optional callbacks for `ConditionContext` and `ActionContext`. The wrapper `exec.Executor[In, Out]` adds typed input and output. The shape is the same, the bridge is wider.

Before matching can start, three things have to be true about the facts:

**They have to be complete enough.** A condition that references `days_to_departure` is silently broken if the request didn't carry that field. The matcher doesn't know whether the field is "absent" or "set to nil" — and the answer changes the semantics. The receive stage normalises missing fields to absent (which the matcher treats as not-constrained) or rejects the request (when the field is required for the rule set the engine is currently serving).

**They have to be the right type.** `market` is a string. `days_to_departure` is a number. `enabled` is a bool. The receive stage is where these are converted, validated, and stamped with whichever canonical form the indexed engine wants. `bre-go`'s indexed engine works against `map[string]string`, so this stage marshals every typed field into its string representation.

**They have to be cheap to read.** The matcher will read the same field many times across many rules. The receive stage converts the raw request into a fact map once. Subsequent reads are O(1) hash lookups.

A useful shape:

```go
type Facts struct {
    raw      map[string]string  // string-form, ready for the matcher
    original interface{}        // for ActionContext callbacks
    received time.Time          // when this request entered the engine
}

func receive(in Request) (Facts, error) {
    raw, err := marshalFacts(in.Input)
    if err != nil {
        return Facts{}, fmt.Errorf("receive: %w", err)
    }
    return Facts{
        raw:      raw,
        original: in.Input,
        received: time.Now(),
    }, nil
}
```

The receive stage is the first place an Execute can fail. A receive failure is *not* a runtime failure — it is a client failure. The Request did not carry what the engine needed. The engine returns an error; no rules are evaluated; no listeners fire as if a rule had matched.

## Match: from facts to a candidate set

Match is the stage Post 4 was about. Here it sits inside the pipeline.

```go
type Matcher interface {
    Match(facts Facts) []RuleRef
}
```

The matcher returns a *candidate set*: the rules whose indexable conditions are consistent with the facts. The candidate set is small (sub-linear in the rule count, for an indexed matcher) and it does not yet account for post-filter conditions.

The contract here is narrow. The matcher does not evaluate full conditions; it does not run actions; it does not compose anything. It hands the next stage a list of rules to consider.

In `bre-go`'s indexed adapter:

```go
// Pseudocode of indexed.Engine.Execute, simplified.
candidates := e.index.Lookup(facts.raw)
// candidates is the set of rules whose indexable terms hashed into
// the buckets this request also hashed into.
```

The candidate set is the first observable boundary in the pipeline. The size of the candidate set is a metric worth tracking — it shows whether the index is doing its job. A candidate set that is consistently large means the rules are not well-indexed and the matcher is degrading toward linear. A candidate set that is consistently empty for live traffic means the rules are too narrow, and a lot of effort is being wasted.

## Evaluate: from candidate set to matched rules

The evaluator walks every candidate rule and evaluates the full Condition tree against the facts. This is where post-filter conditions (negations, ranges, custom typed conditions registered through the post-filter hook) get evaluated.

```go
type Evaluator interface {
    Evaluate(candidates []RuleRef, facts Facts) []RuleRef
}
```

The output is the subset of the candidate set that actually fires. The evaluator is the first stage that knows whether a given rule's full condition is true for these facts.

It is also where every "almost matched" is recorded. A rule whose indexable terms matched but whose range did not is interesting. It tells the team that the rule was a near miss — and a near miss is exactly the kind of thing an explanation log needs.

```go
type EvaluationRecord struct {
    Rule      RuleRef
    Outcome   Outcome  // OutcomeFired, OutcomeFailedCondition, OutcomeDisabled
    FailedAt  string   // "when.days_to_departure.lt" if a clause failed
}
```

A simple matcher just returns the fired rules. A useful matcher returns the fired rules *and* the evaluation records for the rules that didn't fire. The second one costs slightly more in memory; it pays back the first time somebody asks "why didn't rule X fire?"

In `bre-go`, this is what the listener interface is for. `OnRuleMatched` fires per match; the structured telemetry listener can be hooked to record condition outcomes; the listener-driven approach keeps the hot path lean and the observability story rich for callers who opt in.

## Execute: run the actions

Once the rule set is known, the action runs. The action takes the facts (and optionally an `ActionContext` carrying the correlation ID, the listener handle, and whatever else the caller asked for) and returns whatever the action's type signature says it returns.

```go
type ActionResult struct {
    Rule    RuleRef
    Output  interface{} // whatever this action returned
    Err     error       // typed if action panicked
    Latency time.Duration
}

func (e *Engine) executeActions(ctx context.Context,
    fired []RuleRef, facts Facts) []ActionResult {
    results := make([]ActionResult, 0, len(fired))
    for _, r := range fired {
        start := time.Now()
        out, err := r.Action(facts.original) // with panic recovery
        results = append(results, ActionResult{
            Rule:    r,
            Output:  out,
            Err:     err,
            Latency: time.Since(start),
        })
    }
    return results
}
```

Two design choices in this loop earn their way in.

**Actions run after matching, never during.** The match stage and the action stage are separated by an explicit list. The engine knows the full set of fired rules before any action runs. This is what allows conflict detection on the field collisions Post 4 talked about: the engine sees that R7 and R12 both want to set `markup_percentage`, and the resolution policy decides what to do — *before* either action runs.

**Action panics are caught and typed.** `bre-go`'s `OnExecutionErrored` listener receives an `ActionPanicError` carrying the rule name and the panic value. A panic in one action does not take down the engine; it produces a typed result the next stage can compose around. The engine still returns a Result; the Result reports that R7 panicked and was excluded.

This is where engineering instinct fights pragmatism. The instinct says: *if anything went wrong, fail the whole Execute*. The pragmatism says: *if rule R7 panicked but R12 and R18 fired cleanly, the caller can probably still make a decision*. The compromise `bre-go` lands on is to let the caller see what happened and choose: the failed rule appears in the explanation; the Result carries the partial set; the caller can downgrade to a safe default if it doesn't like the partial.

## Compose: combine action outputs per policy

Compose is the stage that turns N action outputs into one Result. It is where the resolution policy from Post 4 actually runs.

```go
type Composer interface {
    Compose(actions []ActionResult) Result
}

// A concrete composer for a pricing engine:
type pricingComposer struct {
    policy ResolutionPolicy // sum, last, fail per field
}

func (c *pricingComposer) Compose(actions []ActionResult) Result {
    var r Result
    for _, a := range actions {
        if a.Err != nil {
            r.Failed = append(r.Failed, a.Rule)
            continue
        }
        r = c.policy.Apply(r, a.Output, a.Rule)
    }
    return r
}
```

The composer is where additive markups stack, where last-write-wins resolves, where conflicts the loader didn't catch get raised as Execute-time errors. The composer is also the layer most engineers initially fold into the engine itself — and the layer that pays the most when it is pulled out.

A composer that is its own stage can be tested with synthetic action results. The test does not need to spin up the matcher or the evaluator. The test gives the composer a list of `ActionResult{}` values and asserts the composed Result. This is what makes resolution-policy changes auditable.

## Explain: the boundary that pays for the rest

The explanation is the artifact every other stage feeds.

```go
type Explanation struct {
    CorrelationID string
    ReceivedAt    time.Time
    Facts         Facts
    CandidateSet  []RuleRef
    Evaluations   []EvaluationRecord
    Actions       []ActionResult
    Result        Result
    Composer      string  // which policy
    Snapshot      string  // engine snapshot ID at the moment of Execute
}
```

The explanation is what makes the next escalation take two minutes instead of forty-five. It records every boundary in the pipeline. The candidate set tells the team whether the index helped. The evaluations tell the team which rules were near misses. The actions tell the team which rules fired and what they returned. The result tells the team what the composer produced.

The expensive bit is that the explanation has to be cheap to produce. In `bre-go`, the listener-driven model means the explanation is opt-in: hot paths that don't need it pay nothing; investigations that do need it can be replayed against the engine snapshot the original Execute used, producing the same explanation deterministically. This is what the `ExportSnapshot` / `LoadSnapshot` work in v0.15 / v0.16 was about — explainability isn't only about emitting records *now*; it's about being able to reproduce the engine state later.

{{< plantuml title="The pipeline as observable boundaries — each stage emits a record the explanation reads" >}}
@startuml
skinparam shadowing false
skinparam componentStyle rectangle
skinparam defaultFontName "Helvetica"

actor "Caller" as C
rectangle "Receive\nfacts.raw,\nfacts.original" as R
rectangle "Match\ncandidate set" as M
rectangle "Evaluate\nfired + near-miss" as E
rectangle "Execute\naction outputs" as X
rectangle "Compose\nResult" as CMP
rectangle "Explanation\n(records every stage)" as EX

C  --> R : Request
R  --> M : Facts
M  --> E : []RuleRef
E  --> X : []RuleRef (fired)
X  --> CMP : []ActionResult
CMP --> C : Result

R  ..> EX : received
M  ..> EX : candidate set
E  ..> EX : evaluations
X  ..> EX : action outputs
CMP ..> EX : composer + result
EX --> C : Explanation
@enduml
{{< /plantuml >}}

## The Execute function in one frame

Pull it all together and the engine looks like this:

```go
// engine.Engine.Execute, with the pipeline made explicit.
func (e *Engine) Execute(ctx context.Context, in Request) (Result, error) {
    facts, err := e.receive(in)
    if err != nil {
        return Result{}, fmt.Errorf("receive: %w", err)
    }

    // Boundary 1: candidate set
    candidates := e.matcher.Match(facts)
    e.listeners.OnCandidates(ctx, candidates)

    // Boundary 2: fired set
    fired, evals := e.evaluator.Evaluate(candidates, facts)
    for _, ev := range evals {
        e.listeners.OnEvaluation(ctx, ev)
    }

    // Boundary 3: action outputs
    actions := e.executeActions(ctx, fired, facts)
    for _, a := range actions {
        e.listeners.OnAction(ctx, a)
    }

    // Boundary 4: result
    result := e.composer.Compose(actions)
    e.listeners.OnFinished(ctx, result)

    return result, nil
}
```

What this code makes explicit is that every interesting moment in the engine is a function call with a named output. The listeners are the observability surface; the function calls are the unit-test seams. The pipeline has stopped being a flowchart on a whiteboard and become a sequence of typed boundaries.

## Testing the pipeline

This is the post where Post 6 starts to make sense. With stages this explicit, tests fit cleanly into four buckets.

**Unit tests per stage.** The matcher gets a fact map and asserts the candidate set. The evaluator gets a candidate set and asserts the fired set. The composer gets a list of action results and asserts the Result. Each test is small. Each test runs in microseconds. Each test names the stage in its filename.

**Integration tests for the pipeline.** Wire the real stages together against a known rule set. Pass realistic facts. Assert the Result. These catch the cross-stage bugs unit tests cannot: a matcher that produces a candidate set the evaluator can't traverse; an evaluator that fires a rule whose action the composer doesn't have a policy for.

**Golden tests for end-to-end behaviour.** Given a snapshot of the rule set and a fixture of facts, assert the Result and the Explanation. These tests pin the system to a behaviour the team has agreed on. When the test fails, the diff against the golden file is the story of what changed.

**Property tests for matchers and composers.** For any fact set, the candidate set is a superset of the fired set. For any action results, the composed Result obeys the resolution policy. These tests don't pin specific behaviours; they pin invariants. Property-based tests are the kind of test that finds the bug nobody wrote a test for.

The shape that makes these four buckets cheap is the pipeline itself. Stages with typed inputs and outputs are testable. Opaque engines are not.

## What the explicit pipeline buys

Three things, mostly.

**Debugging time drops.** The forty-five-minute escalation from the opening becomes a two-minute lookup. The explanation tells the team where in the pipeline the surprising thing happened.

**Performance work becomes targeted.** When p99 climbs, the listener-emitted latency-per-stage tells the team whether the bottleneck is matching, evaluating, or executing. Without stage boundaries, the only datum is "Execute is slow."

**Architectural changes become safe.** Swapping the matcher from linear to indexed is a swap at one boundary. Swapping the composer from last-write-wins to additive is a swap at one boundary. Each swap is a code review of one interface, not a re-architecture of the engine.

The cost is the interfaces. The engine ships with one Engine type and four internal interfaces — Matcher, Evaluator, Executor, Composer — each implemented by one concrete type. The interfaces feel like ceremony until the day somebody wants to test the composer without a real matcher in front of it.

## What comes next

The next post is testing — not in the abstract, but in the specific shape these stages enable. Table-driven tests for the matcher. Golden tests for end-to-end. Property-based tests for invariants. The vocabulary of testing a rule engine, once the engine has been pulled apart into named pieces.

The post after that is explainability — the artifact every stage in this post fed. Explainability is what turns the engine from a black box into a system the team can operate. It is also where the recorded boundaries from this post become the diff a postmortem reads.

For now, the lesson is the pipeline. A rule engine that runs in one step is an engine that cannot defend itself when something goes wrong. A rule engine made of stages is an engine the team can interrogate. The first kind of engine you can ship in a week. The second kind of engine you can keep running for five years.

The escalation that started this post never recurred. Not because the bug was rare. Because the next time somebody escalated, the engine produced an explanation and the conversation was over before the second cup of coffee.
