---
title: "Shadow Mode for Pricing Systems"
subtitle: "Shadow mode lets new logic be wrong in production, on production traffic, before a single customer pays for the bug."
author: helio
layout: post
date: 2025-02-19T10:00:00+00:00
series:
  - pricing-engineering
series_order: 9
categories:
  - Engineering
  - Pricing
  - Architecture
tags:
  - pricing
  - shadow-mode
  - canary
  - architecture
  - observability
  - simulation
description: "Shadow mode runs candidate pricing logic alongside the active path, on the same live request, comparing outputs without changing what the customer pays. This post walks the pattern, the pitfalls, and the divergence reports that earn the trust to roll out."
---

The team had spent six weeks rewriting the markup composer. The math was the same, the data structures were faster, the test suite was green. We were preparing to ship.

We ran shadow mode for ten days first.

By day three the divergence report had flagged 0.42% of requests where the new composer returned a different number from the old one. Not a wildly different number — typically within one or two basis points. We dug. The cause was a rounding step that one composer applied before summation and the other applied after. Neither was "wrong" in isolation; the business had never been asked which rounding it preferred. The product owner picked the answer that matched what customers had been paying for the last three years, the rounding step moved in the new composer, and the divergence dropped to 0.00%. We shipped on day eleven.

We had also discovered, in the same shadow run, that the *old* composer had a panic path nobody had ever exercised in production. The shadow comparison logs surfaced one request, every few hours, where the old composer returned the default zero markup because of an action panic in a rule that handled refund corrections. The new composer handled the same panic by returning the partial result, which was correct. The bug in the old logic was older than anyone on the team. Shadow mode showed it to us by comparing two versions of the truth.

That is what this post is about. Shadow mode is the engineering surface between *we tested it in CI* and *we run it for customers*. It is the cheapest way to discover both what the new code gets wrong and what the old code has been getting wrong all along.

## What shadow mode is

Shadow mode runs the candidate pricing path alongside the active path, on the same live request, and compares the outputs. The customer is served by the active path; the candidate path's output is logged but never returned. Comparison happens asynchronously, on the comparison log, by a separate process.

The point is to give the candidate path exposure to production-shaped traffic before it becomes the production path. CI tests exercise the candidate against scenarios the team wrote. Shadow mode exercises it against the long tail of inputs the team did not write, did not foresee, and could not synthesise.

Three properties define the pattern.

**The active path is unaffected.** Customers are served by it. Latency stays the same. Errors stay the same. The candidate path runs in addition, not instead.

**The candidate path runs against the same facts.** Same request, same correlation ID, same engine snapshot semantics (where it shares them) or a different snapshot under test (where it doesn't). Anything that diverges between the two paths has to be attributable to *the candidate*, not to the inputs.

**The comparison is offline.** The request returns when the active path returns. The candidate's output is captured and compared later. The customer never waits for the candidate.

These three properties are the contract. They are what make shadow mode safe to leave on for weeks at a time.

## The architecture

The wiring looks small from a distance and earns most of its complexity in the details.

{{< plantuml title="Shadow mode: active path serves; candidate path observes" >}}
@startuml
skinparam shadowing false
skinparam componentStyle rectangle
skinparam defaultFontName "Helvetica"

actor "Customer" as C
rectangle "API gateway\nrequest with correlation_id" as G
rectangle "Pricing service" as S
rectangle "Active engine\n(snapshot N)" as A
rectangle "Candidate engine\n(snapshot N+1)\n— async, fire-and-forget" as N
rectangle "Comparison log\n(active result, candidate result,\ncorrelation_id, facts hash)" as L
rectangle "Divergence pipeline\naggregates, classifies,\nemits report" as D

C  --> G : request
G  --> S : facts + correlation_id
S  --> A : Execute (sync)
A  --> S : Result
S  --> C : Response
S  -[#888]-> N : Execute (async)
A  -[#888]-> L : record active
N  -[#888]-> L : record candidate
L  --> D
D  -[#888]-> S : feature flag adjustments (slow)
@enduml
{{< /plantuml >}}

A naive implementation invokes the candidate on the request path, blocks on its completion, then compares. That implementation is wrong twice: it has just doubled the customer's latency, and any panic in the candidate is now a panic in the customer's request. A safer shape:

```go
// Pricing service handler.
func (h *Handler) Price(ctx context.Context, req Request) (Response, error) {
    facts, err := h.facts.Build(ctx, req)
    if err != nil {
        return Response{}, err
    }

    // Active path: synchronous, customer-facing.
    activeResult, err := h.activeEngine.Execute(ctx, facts)
    if err != nil {
        return Response{}, err
    }

    // Candidate path: async, never blocks the response.
    if h.shadow.Enabled(ctx, req) {
        go h.runShadow(ctx, req, facts, activeResult)
    }

    return responseFromResult(activeResult), nil
}

func (h *Handler) runShadow(parent context.Context, req Request,
    facts Facts, activeResult Result) {
    // Decouple from the request context so shutdown doesn't cancel us;
    // bound with our own timeout so a slow candidate cannot pile up.
    ctx, cancel := context.WithTimeout(
        context.Background(),
        h.shadow.Timeout,
    )
    defer cancel()
    ctx = engine.WithCorrelationID(ctx, engine.CorrelationIDFromContext(parent))

    defer func() {
        if r := recover(); r != nil {
            h.shadow.Metrics.PanicCount.Inc()
            log.Warn("shadow candidate panicked",
                "correlation_id", engine.CorrelationIDFromContext(parent),
                "panic", r)
        }
    }()

    candidateResult, err := h.candidateEngine.Execute(ctx, facts)
    if err != nil {
        h.shadow.Metrics.ErrorCount.Inc()
        return
    }

    h.shadow.Log.Record(ShadowRecord{
        CorrelationID: engine.CorrelationIDFromContext(parent),
        Facts:         facts.Hash(),
        Active:        activeResult,
        Candidate:     candidateResult,
        OccurredAt:    time.Now(),
    })
}
```

Three details in this code earn their way in.

**The shadow goroutine has its own context.** It does not inherit the request context. If the request's context is cancelled (deadline exceeded, client disconnect), the shadow should still run to completion — otherwise it under-counts exactly the requests you most want to investigate. The new context carries a separate timeout so a pathologically slow candidate cannot accumulate goroutines.

**The shadow recovers from panics.** A panic in the candidate must not crash the service. The recovery emits a metric and a log line; the customer's request, which already returned, is untouched.

**Errors in the candidate are recorded but not surfaced.** The active path returned. The candidate failed. The team needs to know it failed — that is the metric — but the customer experience cannot be coupled to it.

## What the comparison log carries

The comparison log is the artifact the divergence pipeline reads. It has to carry enough to investigate, little enough to store.

```go
type ShadowRecord struct {
    CorrelationID string        `json:"correlation_id"`
    OccurredAt    time.Time     `json:"occurred_at"`
    FactsHash     string        `json:"facts_hash"`     // sha256(canonical(facts))
    ActiveSnapshot    string    `json:"active_snapshot"`
    CandidateSnapshot string    `json:"candidate_snapshot"`

    Active    ResultSummary `json:"active"`
    Candidate ResultSummary `json:"candidate"`

    Divergence Divergence    `json:"divergence,omitempty"`
}

type ResultSummary struct {
    Result      json.RawMessage `json:"result"`
    FiredRules  []string        `json:"fired_rules"`
    LatencyNs   int64           `json:"latency_ns"`
}

type Divergence struct {
    Kind        string   `json:"kind"`         // result, fired_rules, latency_outlier
    Fields      []string `json:"fields,omitempty"` // for kind=result: which fields differ
    Severity    string   `json:"severity"`     // info, warn, alert
    Description string   `json:"description"`
}
```

The record carries the *summary*, not the full Explanation. The full Explanation from Post 7 is stored in the explanation store for both paths; the shadow record's job is to be small enough to scan in aggregate and to point at the explanations when an investigation starts.

The facts hash is what lets the divergence pipeline group similar requests without storing the requests themselves. Two records with the same facts hash that produced different results are exactly the records worth investigating. The hash is canonicalised — sorted keys, normalised values — so floating-point noise in float fields does not break grouping.

## The four kinds of divergence

Not every difference between active and candidate is a bug. The divergence pipeline should classify, not just report.

**Equal.** Same result, same fired rules. The candidate behaved like the active. This is the most common outcome and the one the team is hoping for.

**Functionally equal, mechanically different.** Same result, different fired rules. The candidate reached the same answer through a different rule set. This is what happens when a refactor consolidates two rules into one, or when a rule is renamed. It is not a bug, but it is a change the team should approve.

**Different result, expected.** The change to the candidate was explicitly meant to change the result for a subset of requests. The divergence is the *signal* of the change working. The team should be able to predict the shape and rate of this divergence before the shadow run starts.

**Different result, unexpected.** Same facts, different decision, no documented reason. This is the bug shadow mode is built to find. Every unexpected divergence is an investigation: load both explanations, compare stage by stage, identify where the paths split.

```go
func classify(active, candidate ResultSummary,
    expectedChanges []ExpectedChange) Divergence {
    if equalResults(active.Result, candidate.Result) {
        if equalRules(active.FiredRules, candidate.FiredRules) {
            return Divergence{Kind: "equal"}
        }
        return Divergence{
            Kind: "functionally_equal_different_rules",
            Description: fmt.Sprintf(
                "active fired %v; candidate fired %v",
                active.FiredRules, candidate.FiredRules),
            Severity: "info",
        }
    }
    // Results differ. Was this expected?
    for _, ec := range expectedChanges {
        if ec.Matches(active, candidate) {
            return Divergence{
                Kind: "result_differs_expected",
                Description: ec.Reason,
                Severity: "info",
            }
        }
    }
    return Divergence{
        Kind: "result_differs_unexpected",
        Fields: diffFields(active.Result, candidate.Result),
        Description: "investigate",
        Severity: "alert",
    }
}
```

Expected divergences are *registered* by whoever proposed the candidate. The shape is small: *for German short-lead-time rail bookings, expect markup to change from 5% to 5.5%, +/- noise*. The divergence pipeline subtracts these expectations from the total divergence count, so the rate of *unexpected* divergence becomes the metric the team watches.

## The divergence report

Once classified, divergences need to be aggregated into a report the team reads. The shape that has aged best for me:

```
Shadow run: pricing-engine v0.18.4 (candidate)
            against pricing-engine v0.18.3 (active)
Duration:   240h (10 days)
Traffic:    52,143,891 requests

Outcome             Count            Rate
equal               51,876,412       99.49%
fun_eq_diff_rules   192,030          0.37%
diff_expected       64,221           0.12%
diff_unexpected     9,847            0.019%
candidate_error     1,381            0.003%

UNEXPECTED DIVERGENCES, by signature
  candidate fires R7 + R12; active fires R7 only        6,142 (62%)
  candidate sets markup_percentage = 0; active != 0     2,103 (21%)
  candidate omits compliance_markup_override            1,098 (11%)
  candidate panics in action callback                     504 (5%)

PERSONA BREAKDOWN of unexpected divergences
  berlin_commuter           4,201 (43%)
  italian_holiday_planner   2,809 (29%)
  cross_border_business     1,420 (14%)
  long_tail                 1,417 (14%)

SLOWEST 0.1% OF CANDIDATE EXECUTIONS
  median (overall)    0.42ms
  p99   (overall)     2.81ms
  p99.9 (overall)     7.20ms
  p99.9 (DE rail short-lead)  14.30ms   ← investigate

ARTIFACTS
  divergence_signatures.csv
  sampled_explanations/{active,candidate}/*.json
  latency_outliers.csv
```

The first table is the headline number: how often the candidate matched the active. The second table groups divergences by signature — the *kind* of mismatch — so the team is not investigating 9 847 individual records but four classes of mismatch. The persona breakdown links the divergences back to the traffic shape from the previous post: if 43% of unexpected divergences are Berlin commuters, the candidate has a problem with that scenario specifically.

The latency tail is included because shadow mode is the first place a performance regression in the candidate becomes visible. The candidate is running on the same hardware as the active; their latencies are directly comparable; an outlier in the candidate's p99.9 is a flag worth raising before the candidate becomes the active.

## Feature flags as the kill switch

The shadow path has to be controllable at runtime. Three controls that matter:

**On/off.** A single flag turns the shadow path on or off entirely. When the candidate starts panicking, the operator turns it off without a deploy. The flag is the difference between a quiet rollback and a 3am incident.

**Sampling.** A percentage knob that says *what fraction of requests should run the candidate*. At rollout you might start at 0.1% and ramp to 100% over a few days. Sampling is also what controls the cost of the shadow run — at 10 000 QPS, running the candidate on 100% of traffic is twice the engine cost; at 5% it is barely noticeable.

**Persona or facts filter.** The flag can target a subset of traffic — *only DE rail bookings*, *only requests with a specific feature flag from upstream*, *only correlation IDs ending in 0-3*. This is what lets the team focus the shadow on the scenario the candidate is meant to affect, without paying to run it on every request.

```go
type ShadowFlag struct {
    Enabled    bool      `flag:"shadow_enabled"`
    SampleRate float64   `flag:"shadow_sample_rate"` // 0.0 to 1.0
    Filter     string    `flag:"shadow_filter"`      // CEL expression on facts
}

func (s *Shadow) Enabled(ctx context.Context, req Request) bool {
    f := s.flags.Current()
    if !f.Enabled {
        return false
    }
    if !sampledIn(req, f.SampleRate) {
        return false
    }
    if f.Filter != "" && !matchesFilter(req, f.Filter) {
        return false
    }
    return true
}
```

The flag values are themselves a small piece of policy. They are stored in the same kind of system that stores rules. The on/off and sample rate change frequently; the filter changes when the team narrows the focus. The defaults — disabled, 0% sample, no filter — are deliberately conservative: the candidate runs only when the team has explicitly turned it on.

## What you learn from shadow mode that you cannot learn elsewhere

Three things, in increasing order of value.

**You learn that the candidate works.** The vast majority of shadow runs end with the team confident that the candidate matches the active on the long tail of requests CI did not cover. That confidence is not free — it has to be earned, and shadow is the only place to earn it on real inputs — but in steady state it is the cheapest thing shadow does.

**You learn where the candidate differs.** When the candidate is a refactor or an optimisation, *equal* is the right outcome and divergence is a regression. When the candidate is a deliberate change, divergence is the *signal* and equality is the regression. Shadow mode tells you which one is happening, request by request.

**You learn what the *active* has been doing wrong all along.** This is the surprise that pays for shadow mode many times over. The opening anecdote was one example: the old composer had a panic path the new one fixed. I have seen at least three other shadow runs reveal long-standing bugs in the active that the comparison logs surfaced — a rule that had been firing on the wrong set of customers for a year, an action that had been silently swallowing errors, a priority tier that was being inverted by a sorting bug. Each one was a bug the team had paid for without knowing.

The framing is worth stating directly: shadow mode is not a test of the candidate. It is a *comparison* between two versions of the truth, and the comparison shines light on both.

## Common mistakes

Three patterns I have shipped or watched ship.

**Running shadow on a non-representative slice.** Sampling 0.1% of traffic for a week sounds prudent. It is also barely a thousand requests. A bug that fires on one in ten thousand is invisible in that sample. The candidate ships, the bug surfaces in production, and the team blames "shadow didn't catch it" when shadow was simply not given enough exposure. The cure is to ramp sample rate and run the shadow long enough to cover the slow tails of the traffic shape.

**Letting the candidate slow the customer.** A team panicked at high shadow cost and moved the candidate path onto the request goroutine to reuse the context. Suddenly the candidate was blocking the response. Latency went up. The candidate was rolled back not because of divergence but because of synchrony. The shape that prevents this is the contract from the architecture section: candidate runs in a separate goroutine with its own context, period.

**Failing to register expected divergences.** A team rolled out a deliberate rule change as shadow and watched 18% of requests diverge. The team panicked and rolled back, then realised the divergence was exactly the change they had asked for. The fix is the expected-change registry: every candidate that is supposed to behave differently has to declare *where* and *how much*, before the shadow run starts. Then the unexpected divergence rate is meaningful.

## Where shadow ends and the next thing begins

Shadow mode is the live half of the candidate's pre-production exposure. The offline half is replay-based simulation — running the candidate against a captured fixture of traffic, with both engines deterministic, with the comparison reproducible. Shadow is what the candidate has to survive in the wild; replay is what it has to survive in the lab.

The two are complementary. Shadow tells you what the candidate does on real traffic at the cost of running real traffic. Replay tells you what the candidate does on a known fixture at the cost of preparing the fixture. The next post puts them together: a captured fixture from `traffic-gen`, a stored snapshot from `bre-go`, a candidate rule set, and a deterministic diff of the two outputs. The output of that loop is what makes rule changes reviewable as code, not as hope.

## The lesson

The engineering lesson, after seven shadow rollouts of varying complexity, is this. Shadow mode lets new logic be wrong in production, on production traffic, before a single customer pays for the bug. It does that by running the candidate alongside the active, asynchronously, comparing outputs, classifying divergences, and surfacing the unexpected ones to the team.

The cost is the architecture: a goroutine per shadowed request, a comparison log, a divergence pipeline, a feature flag. The first version is a few hundred lines of code. The full version is a small service with a dashboard. The benefit compounds: every candidate is exposed to production-shaped traffic before it ships, every active is implicitly audited by being compared, and every rollout starts with a divergence report instead of a hope.

The composer rewrite in the opening anecdote shipped on day eleven with no customer-visible change. The old composer's panic bug got its own ticket and was fixed the week after. The shadow run had cost an engineer about three hours of investigation time across ten days. The bug it caught in the active had been silently mispricing about one refund correction every few hours, for two and a half years. Shadow mode paid for itself in that single comparison; everything after has been the surplus.
