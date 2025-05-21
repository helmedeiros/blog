---
title: "Replay-Based Simulation"
subtitle: "Replay turns pricing discussions from opinions into observable differences. I haven't built the lab yet. This is the shape I have been studying."
author: helio
layout: post
date: 2025-05-21T10:00:00+00:00
series:
  - pricing-engineering
series_order: 10
categories:
  - Engineering
  - Pricing
  - Architecture
tags:
  - pricing
  - simulation
  - replay
  - rule-engine
  - architecture
  - go
description: "Replay-based simulation would pair a stored engine snapshot with a captured traffic fixture and a candidate rule set, producing a deterministic diff. This post is the design I have been working through, informed by bre-go and traffic-gen but not yet wired into a pricing system I have shipped."
---

There was a meeting on a Wednesday afternoon in April when two senior people on the pricing team disagreed about whether a proposed markup change would lift revenue or hurt conversion. The disagreement was real — both of them had defensible models in their heads. It had been going for thirty-five minutes.

I asked, half out loud, whether we could replay the change against last quarter's traffic and just *see* who was right.

We couldn't. We didn't have the lab. We had the engine snapshots — `bre-go` produces them — and we had the rough shape of a traffic generator in mind, but we did not yet have the runner that paired the two and produced the diff. The meeting stretched past its hour, ended with a tentative agreement to roll out cautiously, and turned into a series of follow-up conversations over the next few weeks.

That afternoon is when I started studying replay seriously. This post is what I have been working through since. It is not a postmortem on a system we built and operated. It is the design I have been turning over — what the lab would have to look like, what artifacts it would produce, what workflows it would enable — informed by the snapshot work in `bre-go` and the traffic shape from the previous post, but not yet wired together in any pricing system I have owned. The previous post on shadow mode covered the live half of pre-production validation. This post is the offline half I have been trying to figure out how to build well.

## What the lab would require

A replay session needs three artifacts and one piece of code.

**A snapshot of the active engine.** What rules were live, in which order, at what priority, with which actions. This is the v0.15 / v0.16 work in [`bre-go`](https://github.com/helmedeiros/bre-go) — `ExportSnapshot` and `LoadSnapshot` produce and consume a content-addressable, cross-architecture-portable serialisation of the engine's compiled state. A snapshot is small (KBs to MBs) and cheap to retain. This part exists; it is the engine's promise to the rest of the design.

**A captured fixture of traffic.** A reproducible sequence of requests, generated under a known seed by [`traffic-gen`](https://github.com/helmedeiros/traffic-gen) and stored to disk. The fixture is what would make the replay deterministic on the input side: every run would see the same requests, in the same order, with the same fact values. `traffic-gen` is shaped for this — its `Generator` and `Poster` ports separate generation from emission, and a third sink (the Capture mode) writes the fixture — but I have not yet driven a production-scale capture against a real pricing workload.

**A candidate rule set.** What the proposed change is. A YAML file the team has authored, validated, and compiled, but not yet shipped. The candidate may differ from the active by one rule, by a priority change, or by a full rewrite — the design should handle all three the same way.

**A diff engine.** A small program that loads the two snapshots, drives both engines with the same fixture, captures the explanations from both, and computes a diff: per-request equal/divergent, per-field shifts, per-rule fire rate changes, per-persona impact, p99 latency comparison.

The diff is the artifact I have wanted in every contentious pricing meeting since April. The argument that day did not end because we had a number to point at; it ended because two senior people agreed to disagree carefully. A replay would have given the room a number. That is the design's whole purpose.

## The architecture I have been sketching

The lab wiring is the same shape as shadow mode's wiring with the wall-clock removed.

{{< plantuml title="Replay: two engines, same fixture, deterministic diff" >}}
@startuml
skinparam shadowing false
skinparam componentStyle rectangle
skinparam defaultFontName "Helvetica"

rectangle "Active snapshot\nsha256:7b3f...\n(bre-go ExportSnapshot)" as A
rectangle "Candidate snapshot\nsha256:9d12...\n(built from candidate.yaml)" as N
rectangle "Traffic fixture\n3M requests, seed 20250521\n(traffic-gen Capture)" as F
rectangle "Replay runner\nloads both, drives both,\ncaptures explanations" as R
rectangle "Diff report\nper-request, per-field,\nper-persona, per-rule" as D

A --> R
N --> R
F --> R
R --> D
@enduml
{{< /plantuml >}}

The replay runner is small. The shape I have in my notebook:

```go
type ReplayRun struct {
    ActiveSnapshot    string  // path or content hash
    CandidateSnapshot string
    Fixture           string  // path to captured fixture file
    Sink              DiffSink // where the per-request diff goes
}

func (r *ReplayRun) Run(ctx context.Context) (Report, error) {
    active, err := indexed.LoadCompiledSnapshot(r.ActiveSnapshot, r.callbacks())
    if err != nil { return Report{}, fmt.Errorf("active: %w", err) }
    candidate, err := indexed.LoadCompiledSnapshot(r.CandidateSnapshot, r.callbacks())
    if err != nil { return Report{}, fmt.Errorf("candidate: %w", err) }

    fixture, err := traffic.OpenFixture(r.Fixture)
    if err != nil { return Report{}, fmt.Errorf("fixture: %w", err) }
    defer fixture.Close()

    report := NewReport(r.ActiveSnapshot, r.CandidateSnapshot, r.Fixture)
    for req := range fixture.Requests() {
        facts := factsFromRequest(req)

        activeResult, activeExp, _ := executeWithExplanation(ctx, active, facts)
        candidateResult, candidateExp, _ := executeWithExplanation(ctx, candidate, facts)

        diff := classify(activeResult, candidateResult, activeExp, candidateExp)
        report.Add(req, diff)
        r.Sink.Write(ReplayRecord{
            CorrelationID: req.CorrelationID,
            Persona:       req.Persona,
            Active:        summarise(activeResult, activeExp),
            Candidate:     summarise(candidateResult, candidateExp),
            Diff:          diff,
        })
    }
    return report.Finalize(), nil
}
```

Two properties of this design have to hold to make the diff worth trusting.

**No wall-clock dependency.** The replay must not consult time. The snapshots are immutable. The fixture is deterministic. Every Execute is a pure function from `(snapshot, facts) → result`. A second run of the same replay should produce byte-identical reports. That is what would make the diff a fact rather than a snapshot.

**Both engines on the same path.** Same Execute. Same listener stack. Same explanation schema. The diff would be computed on a uniform output. A change in the engine's path should not skew the comparison; the engine should be the same on both sides, only the snapshot differs.

The replay would run offline. There would be no QPS knob. The runner consumes the fixture as fast as the machine can run two engines side by side. On the laptop I write this on, my prototype against synthetic data runs a 3 million request fixture in about four minutes for a 100-rule engine. On a CI runner with more cores, my back-of-envelope estimate is ninety seconds. I have not measured this against a real pricing workload at scale.

## What the diff would measure

A shadow mode comparison is per-request and forgetful — it logs what happened on one live request and aggregates later. A replay diff would be per-request *and* aggregate from the start. The report I have been sketching fills five tables.

The first table is the headline:

```
REPLAY  pricing-engine v0.18.4 (candidate)
        against pricing-engine v0.18.3 (active)
Fixture q2_2025_seed_20250521.bin  (3,000,000 requests)

Outcome              Count       Rate
equal                2,973,184   99.11%
fun_eq_diff_rules    18,294      0.61%
diff_expected        7,610       0.25%
diff_unexpected      898         0.03%
candidate_error      14          0.00%
```

The second is the per-field shift. For every field the result carries, the diff would calculate how the value distribution shifted between active and candidate. For pricing, this is where revenue impact actually lives.

```
PER-FIELD SHIFTS
field                     active mean    candidate mean    Δ        Δ%
markup_percentage         3.42           3.48              +0.06    +1.75%
base_price                102.13         102.13             0.00     0.00%
provider                  (categorical)  (categorical)     —        —
```

The third is the per-persona impact. The traffic fixture would carry persona metadata; the diff would aggregate over it. This is the table I have wished I could put in front of the April meeting.

```
PER-PERSONA IMPACT
persona                   active rev/req   candidate rev/req   Δ%
berlin_commuter           0.75             0.76                +1.3%
italian_holiday_planner   2.40             2.18                -9.2%   ← investigate
cross_border_business     3.21             3.27                +1.9%
long_tail                 1.04             1.05                +1.0%
```

The fourth is the per-rule fire-rate diff. Which rules changed in how often they fire?

```
PER-RULE FIRE RATE CHANGES (significant only)
rule                              active rate    candidate rate    Δ pp
short_lead_time_markup_de         0.124          0.124              0.00
italian_holiday_seasonal_markup   0.038          0.024             -1.40
spring_promotion_override         —              0.011             new
```

The fifth is performance:

```
LATENCY
                       active p50    candidate p50    Δ        p99 active    p99 cand    Δ
overall Execute        0.41ms        0.43ms           +0.02    2.81ms        2.93ms      +0.12
indexed matcher        0.18ms        0.18ms            0.00    1.20ms        1.21ms      +0.01
composer               0.04ms        0.06ms           +0.02    0.21ms        0.31ms      +0.10
```

Each of the five tables would answer a question the team is likely to ask. The headline would tell you whether the candidate is broadly safe. The field shifts would tell you the revenue or experience impact. The persona impact would tell you where the impact lands. The rule fire-rate would tell you why. The latency would tell you whether the candidate is shippable from a performance perspective.

The bug-finding power of such a report would be in the unexpected slice. *0.03% diff unexpected* on three million requests is 898 requests; those 898 are exactly the requests the team should investigate before shipping. Each one would have the active explanation, the candidate explanation, and the request facts; loading any of them in a debugger would be one query against the replay sink.

## Determinism, and what it would earn

The single most consequential property of the design is determinism. Same snapshots, same fixture, same diff. Byte-identical, across machines, across weeks.

Three things determinism would earn.

**Reviews would become diffs.** A PR that proposes a rule change could be required to include a replay report. The reviewer would read the diff. The reviewer would not have to reason about whether the change is safe; they would read what the change *did* against last quarter's traffic. The reviewer's heuristic would become "are the per-persona impacts what the author claimed?"

**Regressions would become hard to hide.** If a refactor of the engine drifts behaviour, a replay against the existing snapshot would surface it before the refactor merged. The engine team could include a replay run in CI on a small fixture; the test would be a behavioural assertion across millions of requests rather than a unit test of one path.

**Compliance would become addressable.** When the regulator asks the same question the auditor asked in Post 7 — *why was this customer charged this way?* — the answer would be one replay against the snapshot from that date and the request facts from the fact log. The reproducibility property the explanation already carries would be bolted to a reproducible *input* too.

The cost is the snapshot and the fixture. Snapshots are produced by the engine automatically — `bre-go`'s `ExportCompiledSnapshot` is 50% smaller than the JSON form and 2.93× faster to load at 10 000 rules. Fixtures would be produced by `traffic-gen` from a scenario file and a seed; small (MBs for hundreds of thousands of requests), reproducible, and version-controllable.

Both inputs already exist as engineering primitives. The runner that pairs them is what I have not built.

## Outlier detection

Aggregate numbers hide outliers. A 1.75% mean shift in markup can be 1.75% across the board or 0% on 99% of traffic and a 175% shift on 1%. The replay sink would write per-request records; the report would walk them looking for the second case.

The outlier passes I have been planning:

**Field-level outliers.** For each field in the result, compute the per-request delta between active and candidate. Sort by absolute delta. The top 0.1% is the tail. The tail is where the candidate's worst behaviour lives.

**Persona-level outliers.** For each persona, recompute the headline numbers (mean shift, fire-rate change). A persona whose mean shift is more than 2σ from the overall mean would be flagged.

**Rule-level outliers.** A rule whose fire rate changed by more than a threshold would be flagged. A rule that disappears entirely from the candidate would be flagged. A new rule that fires more than a threshold rate would be flagged.

These passes are cheap — on my prototype, on the order of one minute over a 3 million request replay. The engineer-hours they would save during investigation, every time, are the reason to build them in from the start rather than bolt them on later.

## What replay would not do

Three things replay does not solve, that I sometimes catch myself thinking it might.

**Replay would not substitute for shadow mode.** The fixture is captured from a known seed; it carries the distribution the team chose. Production carries the distribution the team did not choose. A candidate that passes replay could still misbehave on the shape of input only production produces. Shadow mode is what catches that. Replay is the lab; shadow mode is the field.

**Replay would not substitute for tests.** The replay diff is aggregate; the test suite is per-scenario. The test suite says *for a Berlin commuter four days out, the markup must be 5%*. The replay says *across three million requests, the candidate raises mean markup by 0.06pp*. Both are useful. Neither replaces the other.

**Replay would not substitute for thinking about the change.** The diff is a snapshot of impact. It does not tell you whether the impact is what the business wants. A candidate that lifts revenue by 1.3% and shifts mix toward Italian holiday planners by 9% might be a candidate the team approves; it might be one the team rejects. The replay would surface the tradeoff; the team would still own the decision.

The framing I have settled on as I work through this design: replay is the highest-bandwidth way to communicate the impact of a rule change to the people who have to approve it. The diff is the artifact. The argument it ends is the value. The reason I am still working on it is that bandwidth is exactly what the April meeting did not have.

## What such a report would enable

Three workflows the design supports cleanly, once it exists.

**Pre-ship impact review.** Every candidate rule set produces a replay report before it merges. The PR description carries the headline and the per-persona table. The reviewer reads both. The merge happens or doesn't. This is the workflow I would build first.

**Quarterly retrospective.** At the end of each quarter, the team runs the *active* snapshot at quarter-end against a *captured fixture* of the previous quarter. The diff is the actual impact of the rule changes that shipped over the quarter, measured against the inputs the rule changes were meant to address. The report becomes the team's evidence of what the quarter accomplished.

**Counterfactual analysis.** "What would have happened if we had not shipped rule X in March?" Disable rule X in the snapshot, replay against Q1's fixture, read the diff. The counterfactual is the diff. The conversation that follows is grounded in measurement, not memory.

Each of these workflows is opinion-based without the lab. Each becomes data-based with it. The replay would make the team's pricing conversations turn from "I think this will" to "the diff shows this did."

## The lab and the field together

A clean workflow for any candidate rule change would become:

1. Author the candidate, write the expected-impact note that goes with it.
2. Run a replay against last quarter's fixture and last quarter's snapshot. Compare the diff to the expected-impact note. If they disagree, revise the candidate or revise the expectation.
3. Run shadow mode on production traffic for one to two weeks. Watch the unexpected divergence rate. Drill into the outliers.
4. If shadow agrees with replay (or the divergence is explained), promote the candidate to active. Snapshot the new active. The cycle begins again with the next candidate.

```
candidate.yaml + active.snapshot
        │
        ▼
   ┌─────────┐        ┌──────────┐
   │ Replay  │ ──pass──▶│ Shadow  │ ──pass──▶ Promote
   │  (lab)  │        │ (field)  │
   └─────────┘        └──────────┘
        │                  │
        │                  │
        ▼                  ▼
   diff report        divergence report
```

The two stages would catch different bugs. Replay would catch systematic problems — a rule that misfires across the fixture, a composition policy that changes a field unexpectedly, a performance regression across the average path. Shadow catches contextual problems — a rule that misfires on a customer segment the fixture under-represents, an action that depends on something only production touches.

The combination would be the answer to "is this safe to ship?" Neither alone is enough. Both together, in my reading, would be.

## What comes next

The next post takes the architectural step up: the difference between a rule engine and a decision engine, and when each is the right tool. Replay was the closing act of the engine series in my notes — the moment when the rules, the matcher, the explanation, and the traffic generation would all meet. The next post asks what comes when rules are not enough: when policies, models, constraints, and experiments have to be coordinated, and the simple "facts in, action out" shape of an engine has to grow into something more.

After that we move to maintainability, the ten mistakes I have shipped, and what I would build differently today. The last three posts are the retrospective half of the series — less about the next layer, more about everything we have built and the gaps, like this one, that I am still working through.

## The lesson

Replay would turn pricing discussions from opinions into observable differences. It would do that by pairing a stored snapshot, a captured fixture, and a candidate rule set into a deterministic diff. The diff would be the artifact the team reviews. The diff would be the artifact the regulator can be shown. The diff would be the artifact the next quarter's retrospective starts from.

The cost is the snapshot, the fixture, and a small runner. The first two exist as primitives. The runner is what I have been studying — what it has to compute, what reports it has to emit, what failure modes it has to surface. I have prototypes against synthetic data. I have not yet driven it against a production pricing workload.

The meeting in April did not end with a diff. It ended with both people still half-confident in their model, a cautious rollout plan, and a follow-up review six weeks later. The number I have wanted to put in that room since is the one a replay produces. I have not built it for a production pricing system yet. I have studied it enough to know what shape it would take, and writing it down is the cheapest way to find out what I have missed.
