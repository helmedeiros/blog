---
title: "Explainable Rule Execution"
subtitle: "A pricing system that cannot explain a decision cannot be safely operated. The explanation is not a debug aid. It is the system's contract with everyone who has to trust it."
author: helio
layout: post
date: 2024-08-21T10:00:00+00:00
series:
  - pricing-engineering
series_order: 7
categories:
  - Engineering
  - Pricing
  - Architecture
tags:
  - pricing
  - business-rules
  - rule-engine
  - explainability
  - observability
  - compliance
description: "An explanation is not a log. It is a structured artifact every stage of the engine contributes to, and the contract the system makes with operators, auditors, and customers."
---

The email arrived at 9:42 on a Tuesday from the legal team. A market regulator wanted, in writing, the answer to one question for one customer: *why was this specific booking priced this way on this specific date?*

The booking was eleven months old. The team that owned the rule set had partly turned over. The rule file had been edited forty-six times since. Production logs had rolled off thirty days ago. The dashboard showed a number for that day but not the path that produced it.

We answered the regulator. It took two engineers four days. We pulled the git log of the rule file, reconstructed the state on that date, replayed the booking against the reconstructed engine, produced the explanation, and translated it into a paragraph a non-engineer could read. The customer's actual booking was not the one we needed to defend; the *category* of decision was the one that mattered, and we eventually defended it.

What we did not have, the day that email arrived, was a system that could answer the question on its own. Every piece of the answer existed somewhere. None of the pieces were connected. The explanation, the artifact we kept hinting at across the last five posts, was the missing seam.

This post is what that seam looks like when it is built deliberately.

## The four audiences for an explanation

The mistake I made the first time I built explainability into a rule engine was to design it for one audience — the engineer debugging at 3am — and stop. That audience is the loudest, but it is the one that needs explainability the least, because the engineer can read the source.

There are four audiences, and the explanation has to serve all of them without collapsing into the lowest common denominator.

The **engineer** wants depth. Which rules were considered, which fired, why each one did or didn't, what the result of every action was, where time was spent. The engineer can read JSON and is fine with field names that mean nothing without context.

The **operator** wants signal. Which snapshot of the rule store served this request? Were any rules disabled? Was the response normal or anomalous compared to nearby traffic? The operator does not want to read every evaluation; they want to know whether something looks off.

The **product or domain owner** wants to verify the agreement. Did the system do what we said it would? Were the rules we wrote behaving as intended? The product owner reads the rule names and the result; they do not read the bucket key.

The **auditor or regulator** wants a paper trail. Given a customer and a date, what decision was made, by which rule, with which intent, owned by which team, with which review date? The auditor wants exactly the boring metadata fields Post 1 argued were not optional.

Each audience reads a different subset of the same artifact. The job of the explanation is to be the same artifact for all of them, with different views layered on top. A single structured record, queried four different ways.

## The schema, in full

Post 5 sketched the Explanation. This post fills it in. The schema below is the one I have settled on after three iterations.

```go
type Explanation struct {
    // Identity and traceability
    CorrelationID  string    `json:"correlation_id"`
    RequestID      string    `json:"request_id"`
    SnapshotID     string    `json:"snapshot_id"`     // engine state hash
    SchemaVersion  int       `json:"explanation_version"`
    OccurredAt     time.Time `json:"occurred_at"`
    Duration       time.Duration `json:"duration_ns"`

    // What came in
    Facts          map[string]string `json:"facts"`

    // What happened, stage by stage
    CandidateSet   []RuleRef          `json:"candidates"`     // matcher output
    Evaluations    []EvaluationRecord `json:"evaluations"`    // per-rule outcome
    Actions        []ActionRecord     `json:"actions"`         // per-fired-rule output
    Composition    CompositionRecord  `json:"composition"`     // resolution policy applied

    // What came out
    Result         json.RawMessage    `json:"result"`

    // What the operator should care about
    Warnings       []Warning          `json:"warnings,omitempty"`
}

type EvaluationRecord struct {
    Rule         RuleRef `json:"rule"`
    Outcome      Outcome `json:"outcome"`       // fired, failed_condition, disabled, errored
    FailedAt     string  `json:"failed_at,omitempty"`     // "when.days_to_departure.lt"
    EvalDuration time.Duration `json:"eval_duration_ns"`
}

type ActionRecord struct {
    Rule           RuleRef `json:"rule"`
    Output         json.RawMessage `json:"output"`
    Err            string `json:"err,omitempty"`
    Latency        time.Duration `json:"latency_ns"`
}

type CompositionRecord struct {
    Policy   string                       `json:"policy"`
    PerField map[string]CompositionTrace  `json:"per_field"`
}

type CompositionTrace struct {
    FinalValue     json.RawMessage `json:"final_value"`
    ContributingRules []string     `json:"contributing_rules"`
    Strategy       string          `json:"strategy"`  // sum, last, first, fail
}

type RuleRef struct {
    Name         string `json:"name"`
    Version      string `json:"version"`       // git sha of the rule file, or rule_id hash
    Owner        string `json:"owner"`
    Description  string `json:"description"`
    Priority     int    `json:"priority"`
    Enabled      bool   `json:"enabled"`
}

type Warning struct {
    Code     string `json:"code"`     // SHADOWED_RULE, EMPTY_CANDIDATE_SET, etc.
    Message  string `json:"message"`
    Severity string `json:"severity"` // info, warn
}
```

Three properties of this schema earn it the right to live in production.

**Every record points back to source.** `RuleRef` carries Owner, Description, and a Version. A consumer reading the explanation does not have to also load the rule file to know what the rule meant. The Version field is critical: when the rule file evolves, the explanation still references the rule *as it was at the moment of Execute*.

**Latency lives per stage.** `EvalDuration` per evaluation, `Latency` per action, and `Duration` for the whole Execute. Cumulative wall time hides where time was spent; per-stage latency makes the engine's behaviour observable without an external profiler.

**Warnings are first-class.** A shadowed rule that fired anyway, a candidate set that was suspiciously empty, a composition step that hit a `fail` policy — each one becomes a Warning the operator's dashboard can surface. The dashboard does not have to parse the full explanation; it counts warnings by code and graphs the rate.

## A real explanation, end to end

Here is what an Explanation looks like for the German short-lead-time scenario I have been using throughout the series:

```json
{
  "correlation_id": "c1b9a4e7-21d8-4d0e-9a2a-1cb5a7e4f0b1",
  "request_id": "req-2024-08-21T10:14:33Z-7b3f",
  "snapshot_id": "sha256:7b3f...e91d",
  "explanation_version": 2,
  "occurred_at": "2024-08-21T10:14:33.012Z",
  "duration_ns": 412330,

  "facts": {
    "market": "DE",
    "channel": "rail",
    "days_to_departure": "4",
    "device": "mobile",
    "regulated_market": "false"
  },

  "candidates": [
    {"name": "compliance_markup_override", "version": "7b3f", "owner": "compliance",
     "description": "0% markup in regulated markets", "priority": 1000, "enabled": true},
    {"name": "short_lead_time_markup_de", "version": "7b3f", "owner": "pricing-de",
     "description": "3% markup on DE bookings under 7 days", "priority": 500, "enabled": true},
    {"name": "germany_baseline_markup", "version": "7b3f", "owner": "pricing-de",
     "description": "2% baseline markup on all DE bookings", "priority": 100, "enabled": true}
  ],

  "evaluations": [
    {"rule": {"name": "compliance_markup_override"}, "outcome": "failed_condition",
     "failed_at": "when.regulated_market.eq", "eval_duration_ns": 1850},
    {"rule": {"name": "short_lead_time_markup_de"}, "outcome": "fired",
     "eval_duration_ns": 4210},
    {"rule": {"name": "germany_baseline_markup"}, "outcome": "fired",
     "eval_duration_ns": 1320}
  ],

  "actions": [
    {"rule": {"name": "short_lead_time_markup_de"}, "output": {"markup_percentage": 3.0},
     "latency_ns": 8120},
    {"rule": {"name": "germany_baseline_markup"}, "output": {"markup_percentage": 2.0},
     "latency_ns": 6210}
  ],

  "composition": {
    "policy": "additive_with_compliance_override",
    "per_field": {
      "markup_percentage": {
        "final_value": 5.0,
        "contributing_rules": ["short_lead_time_markup_de", "germany_baseline_markup"],
        "strategy": "sum"
      }
    }
  },

  "result": {"markup_percentage": 5.0},

  "warnings": []
}
```

The whole record is 60 lines of JSON for one Execute. It carries enough for the engineer, the operator, the product owner, and the auditor.

The engineer reads `evaluations` and `actions` and sees the engine's path.

The operator scans `warnings` and `duration_ns` and confirms the request was normal.

The product owner reads `composition.per_field.markup_percentage.contributing_rules` and confirms the agreement held.

The auditor reads `facts`, `candidates[*].owner`, and `result` and has a defensible paragraph.

One artifact. Four views. No translation step.

## The cost model

The cost of an Explanation is the cost engineers most fear and most overestimate.

A populated Explanation for a 100-rule engine is on the order of 5–15 KB of JSON, dominated by the candidate set and evaluation records. Generation takes microseconds — the records are already produced by the listener stack from Post 5; emission is `json.Marshal` over a typed struct. The hot-path overhead, when the explanation is emitted, is a low single-digit percent of Execute time.

The cost that bites is not generation. It is *storage*. At 10 000 QPS, full explanations weigh 50 MB/sec, 4 TB/day, 120 TB/month. No system retains that indefinitely.

Three strategies, in increasing sophistication, handle the cost.

**Sampling.** A fixed percentage of requests get full explanations; the rest get nothing. Useful for engineering visibility into the average path. Useless for auditing — the request you are asked about is, by Murphy's law, never in the sample.

**Tiered emission.** Every request gets a tiny explanation (5 lines: snapshot ID, fired rule names, result). Anomalous requests, requests flagged by warnings, requests for high-value customers, and a sample of normal requests get full explanations. The signal is preserved; the cost is bounded.

**Replay on demand.** Every request stores the *minimum* needed to reproduce: snapshot ID, facts, correlation ID. The full explanation is generated from a replay against the stored snapshot when asked. This works because the engine is deterministic (Post 1's first property earns its keep) and because `bre-go`'s `ExportSnapshot` / `LoadSnapshot` makes snapshots a first-class artifact.

The architecture I land on most often is the third one, layered over the second:

- Hot path emits a tiny explanation per request (snapshot ID, fired rules, result) at 100% sample.
- Hot path emits a full explanation at 1% sample, plus on demand for requests carrying a `?debug=1` flag from the call site.
- Cold path can regenerate the full explanation from `(snapshot_id, facts, correlation_id)` via replay, up to the snapshot retention window.

Snapshot retention is the actual capacity constraint. A snapshot is small (a binary file, KBs to MBs). Keeping every snapshot the engine ever served is cheap. With the snapshot retained and the facts logged, the full explanation can be reconstructed at any time.

{{< plantuml title="Tiered explanation emission: cheap by default, full on demand, replayable forever" >}}
@startuml
skinparam shadowing false
skinparam componentStyle rectangle
skinparam defaultFontName "Helvetica"

rectangle "Hot path\nExecute(ctx, facts)" as HP
rectangle "Tiny explanation\nemitted 100%\n(5 lines / request)" as T
rectangle "Full explanation\nemitted 1% + on demand" as F
rectangle "Snapshot store\nengine state\nretained 12 months" as S
rectangle "Fact log\nrequest facts\nretained 12 months" as L
rectangle "Replay service\nreproduces full\nexplanation later" as R
actor "Auditor\nor engineer" as A

HP --> T
HP --> F
HP --> S
HP --> L
A  --> R : "explain request X"
R  --> S : load snapshot
R  --> L : load facts
R  --> A : full explanation
@enduml
{{< /plantuml >}}

## Trace IDs as the spine of the explanation

Explanations connect to the rest of the system through the correlation ID. `bre-go`'s `engine.WithCorrelationID(ctx, id)` puts the ID in the context; the engine reads it from `ConditionContext` and `ActionContext`; the explanation stamps it as the first field.

The correlation ID is what lets a service span thirty downstream lines of log and the explanation be the same conversation. The customer support engineer sees the trace ID in their tooling; the rule engine knows that same ID; the explanation is queryable by it.

Three rules that make correlation IDs useful in practice:

**Generate at the edge, propagate inward.** The API gateway or the call site generates the ID; the engine never invents one. An engine-generated ID is one nothing else can connect to.

**Include in every observability surface.** The metric, the log line, the explanation, the snapshot record. If the ID is in three of four surfaces, the auditor still can't connect them.

**Distinguish correlation from request ID.** Correlation is a session — a customer journey, a workflow, a batch. Request is one call. Multiple Execute calls in the same customer journey share a correlation ID; each has its own request ID. The explanation carries both.

The cost is one string in the schema. The benefit is every later question — *what else happened in this customer's session?* — has an answer.

## Logs and explanations: when each fires

A common mistake is to dump the explanation into a structured log and call it observability. It is more useful to think of logs and explanations as two different artifacts with two different lifespans.

**Logs are time-series events.** They go to a log aggregator. They are sampled, dropped under load, and rolled off after weeks. They are good for "what happened in the last hour?" and bad for "what happened to this request eleven months ago?"

**Explanations are addressed artifacts.** They are keyed by request ID. They are stored in a data store (or replayable from a snapshot). They are good for "what happened to *this* request?" and bad for "what is the rate of warnings?"

The two need each other. The log line carries the request ID and the snapshot ID; the explanation carries the full context. The dashboard reads the logs and graphs the rates; the investigator reads the explanation and reconstructs the path.

A simple shape:

```go
// At Execute time, emit a log line.
log.Info("rule.engine.execute",
    "correlation_id", explanation.CorrelationID,
    "request_id", explanation.RequestID,
    "snapshot_id", explanation.SnapshotID,
    "fired_count", len(explanation.Actions),
    "duration_ms", explanation.Duration.Milliseconds(),
    "warning_count", len(explanation.Warnings),
)

// Separately, emit the full explanation to the explanation store
// (synchronously for sampled traffic, asynchronously for debug-flagged).
explanationStore.Put(ctx, explanation)
```

The log line is enough for dashboards and alerts. The explanation is enough for investigations. Neither is enough on its own.

## The investigation workflow

The reason to build explainability is to make investigations cheap. The investigation workflow, when the system is built right, is:

1. Customer support flags a booking with a correlation ID.
2. The engineer queries the explanation store: `explanationStore.Get(correlation_id)`.
3. If the explanation is in the store (sampled or debug-flagged), it returns immediately.
4. If not, the replay service is invoked: it loads the snapshot from the snapshot ID embedded in the original log line, loads the facts from the fact log, and runs the engine again to reconstruct the explanation.
5. The engineer reads the explanation and answers the question.

This is what made the four-day investigation in the opening anecdote a thirty-minute one in subsequent quarters. The same workflow, with the same artifacts, handles engineering escalations, product questions, and audit requests.

The workflow has one prerequisite: snapshots have to be retained. The snapshot is what makes replay deterministic. Without the snapshot, replay requires reconstructing the rule set from `git` history, which works only if the engine's compilation of the rule set is itself reproducible from source. (It usually is, but the days you discover it isn't are the days you wish you had stored the snapshot.)

## What the explanation makes possible

Three durable benefits that pay back the engineering investment.

**Postmortems get faster.** Every incident has a request ID. Every request ID has an explanation. The postmortem starts with the explanation; the root cause analysis is the diff between what the explanation showed and what the team expected.

**Customer support stops escalating.** The agent answering "why was I charged this?" has the explanation. The product owner does not have to be paged for routine questions. The engineering team does not have to be the first point of contact for pricing curiosity.

**Compliance becomes a tooling problem, not a heroics problem.** The next time a regulator asks, the answer is a database query, not four engineer-days. The defensibility of the system is a built-in property, not an extracted one.

The cost — schema, storage, replay service, snapshot retention — is real. It is also bounded. The first version is a few hundred lines of code. The full version is a few thousand. The benefit compounds across every incident, every escalation, every audit, for as long as the engine runs.

## What the explanation does *not* do

Two things the explanation is sometimes asked to do, and shouldn't.

**It is not a replacement for the rule file.** The rule file is the authored intent. The explanation is the evaluated outcome. Confusing them is how teams end up "editing the explanation" to fix a bug, which fixes nothing and obscures the next investigation.

**It is not the engine's audit trail.** The audit trail is the snapshot + the fact log + the rule history in `git`. The explanation is the *view* across those, generated for one request. An audit on a thousand requests is a thousand explanations, generated against the same snapshots. The explanation is not the storage; it is the projection.

These distinctions sound pedantic until you watch a team try to store every explanation forever as "the audit trail." The cost compounds, the schema starts changing, and the data store becomes the system's most expensive component. The replay-on-demand model is what keeps the cost sane.

## What comes next

The next post is synthetic traffic — the way to give the engine inputs it has not seen yet, on purpose, to find the bugs it will encounter later. Synthetic traffic is what makes shadow mode and replay-based simulation meaningful in the two posts after that. It is also where the second reference repo, [`traffic-gen`](https://github.com/helmedeiros/traffic-gen), enters the story.

Synthetic traffic and explanations are complementary. Traffic produces requests; the engine produces explanations. A replay session against a candidate rule set generates explanations for every synthetic request, and the difference between the candidate and current explanations is the impact assessment of the candidate rule. The next three posts are about closing that loop.

For now, the lesson is the contract. A pricing system that cannot explain a decision cannot be safely operated. The explanation is the system's promise to the operator, the auditor, the product owner, and the engineer — that the path the engine took is recoverable. That promise is not free, but it is the cheapest insurance the engine can carry, and it is the one piece of the system you will be glad you over-invested in the first time a regulator asks a question.

The customer in the opening anecdote was not, in the end, the question. The category of decision was. The next regulator email arrived seven months later. The answer took thirty minutes. The system, by then, was no longer asking us to defend it; it was defending itself.
