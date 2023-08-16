---
title: "Rules as Data, Not Code"
subtitle: "Moving rules into YAML is the easy part. Making the loader trustworthy is where the work is."
author: helio
layout: post
date: 2023-08-16T10:00:00+00:00
series:
  - pricing-engineering
series_order: 3
categories:
  - Engineering
  - Pricing
  - Architecture
tags:
  - pricing
  - business-rules
  - rule-engine
  - yaml
  - json
  - schema
  - architecture
description: "Rules as data is a meaningful idea only when the loader validates, versions, and fails safely. This post walks through the loader as the boundary it deserves to be."
---

The first time a rule edit shipped to production without a deploy, the team cheered.

It was a small change. A markup of 3% became a markup of 4% for one market segment. Somebody opened the YAML, edited the number, the pipeline picked it up, the service hot-reloaded, the next request priced with the new value. Five minutes from idea to production. We took a screenshot of the dashboard and pinned it in the channel.

Six weeks later somebody pasted a regex into the `markup_percentage` field by accident. The string passed YAML parsing fine — YAML is happy to give you `"^[A-Z0-9]+$"` as a value — and the loader handed the engine a rule whose action contained a regex where a number should have been. The engine, defensively, returned zero. Every booking in that segment lost the markup for the next six hours, until a graph drifted enough to wake somebody up. The fix took ninety seconds. The investigation took most of a Saturday.

That story is the rest of this post. Rules as data is a meaningful idea only when the loader is treated as the boundary it actually is.

## Why "rules as code" stops working

The previous post pulled the Rule struct apart and argued the in-memory shape is the contract. That contract works fine when every change to a rule goes through `git`. You write Go, you change a struct literal, you ship a binary. The compiler catches typos. Tests run before the change reaches prod. The cadence of rule edits is the cadence of deploys, and most teams can live with that for a while.

The break point arrives when the rate of rule edits exceeds the deploy cadence the team can keep clean. In pricing systems this happens fast. A team that wanted to ship two rule changes per quarter ends up wanting to ship three changes per week. The branches multiply. The release notes grow a "rule changes" section that nobody reads. Reverting a deploy means reverting unrelated code along with the rule. The deploy starts being the place where rule edits go to die.

That is the moment the YAML appears. Somebody writes a loader. The rules move out of the Go file and into a folder.

What also moves out, if you are not careful, is every guarantee the compiler used to give you for free.

## What you lose when rules leave the source tree

Three things, mostly.

**You lose schema enforcement.** The compiler that used to refuse `markup_percentage: "^[A-Z0-9]+$"` is gone. Nothing reads the YAML except the loader, and the loader, by default, accepts whatever YAML decides is valid.

**You lose static analysis.** The IDE that used to highlight a misspelled field name is gone. The reviewer who used to catch the wrong type in a pull request is gone. The rule file is now somebody's personal notepad until you put a schema on top of it.

**You lose atomicity.** A code deploy is one event. A YAML reload is N events — one per file, one per parse error, one per validation failure. The system has to decide, in real time, what to do with each of them.

Each of these is recoverable. They are recoverable by *building the loader as a piece of engineering*, not as a `yaml.Unmarshal` call buried inside service startup. The job of the rest of this post is to lay out what that loader looks like.

## The rule file: small enough to read, structured enough to validate

The shape of the rule file is the first thing the loader works with. There is a temptation, when the team agrees on YAML, to dump every possible field at the top level and let the loader figure out which ones matter. Resist it. The shape of the file is your only API.

A workable shape, modelled on a pricing rule store:

```yaml
version: 1
rules:
  - id: short_lead_time_markup_de
    name: "DE short lead-time markup"
    description: "3% markup on Germany bookings under 7 days from departure"
    owner: pricing-de
    intent: |
      Capture demand on short-window bookings in Germany where
      capacity constraints reduce price sensitivity. Reviewed in Q1.
    priority: 500
    enabled: true
    when:
      market:
        eq: DE
      days_to_departure:
        lt: 7
    then:
      type: set_markup
      value: 3.0
    metadata:
      ticket: PRICE-1473
      experiment: ELAST-2023-Q3
      review_after: 2024-02-16
```

A few things in this shape that look small and earn their way in.

The `version: 1` at the top of the file is the loader's first decision point. The day the schema changes — and it will — the loader needs to know which schema to apply. Versioning the file format is what lets the team add fields without breaking historical loads.

The `when` block uses explicit operators (`eq`, `lt`) rather than bare values. The bare-value form looks cleaner (`market: DE`) but it makes every operator implicit, and implicit operators are how `market: "DE,FR"` ends up being interpreted by half the team as "DE OR FR" and by the other half as the literal string "DE,FR". Explicit operators cost five characters and remove a category of bug.

The `then` block uses a typed action (`type: set_markup, value: 3.0`) rather than a free-form value. This is the same decision Post 2 made for the in-memory model. The catalogue of action types is the catalogue of side effects the engine knows how to execute. A YAML field with an unknown action type is one the loader can reject by name.

The `metadata` block carries everything the engine doesn't need but everyone else does. It is not optional in practice. It is optional in the schema only because the YAML shouldn't fail to parse when an old file is missing a `review_after`; the loader's *job*, separately, is to emit a warning when it sees one.

## The loader is the boundary

Here is the shape of a loader that earns its name. It is more than a `yaml.Unmarshal`:

```
ON-DISK FILE
     │
     ▼
┌────────────────────────────────────────────┐
│ 1. PARSE                                   │
│    yaml/json → []RawRule                   │
│    fail-fast on syntax error               │
└────────────────────────────────────────────┘
     │
     ▼
┌────────────────────────────────────────────┐
│ 2. VALIDATE PER RULE                       │
│    schema, types, required fields,         │
│    action type ∈ known catalogue           │
│    collect errors with rule index          │
└────────────────────────────────────────────┘
     │
     ▼
┌────────────────────────────────────────────┐
│ 3. VALIDATE THE SET                        │
│    unique names, priority sanity,          │
│    dead-rule detection, reachability       │
└────────────────────────────────────────────┘
     │
     ▼
┌────────────────────────────────────────────┐
│ 4. COMPILE                                 │
│    raw → engine.Rule (typed Condition,     │
│    Action callback bound by name)          │
└────────────────────────────────────────────┘
     │
     ▼
┌────────────────────────────────────────────┐
│ 5. SWAP                                    │
│    atomic replacement of the running       │
│    engine — or fail closed                 │
└────────────────────────────────────────────┘
```

Each of the five steps has a different failure mode. Each one has to be designed for.

### Parse: fail fast, fail loud

YAML or JSON parse errors are the cheapest errors to detect and the loudest to report. The loader should refuse to proceed if the file is malformed. There is no clever recovery — a malformed file is a file the operator did not mean to ship.

`bre-go`'s JSON loader (`engine/json.Loader[RC]`) returns a `LoadError` whose `Index` is `-1` for document-level failures (broken JSON, wrong top-level type) and 0-indexed for per-rule failures. That distinction matters: a document-level failure means *nothing in this file is trustworthy*. A per-rule failure means *the third rule is bad; the rest may or may not be*. The loader should handle those two cases differently, and they have to be distinguishable in the error.

### Validate per rule: schema is the contract

Per-rule validation is where the compiler comes back. The loader checks that every required field is present, every type matches, every operator in the `when` block is one the parser knows, every action type in the `then` block is one the action registry knows about.

This is also where the dollar amount that wandered in as a string gets rejected. The validator says `markup_percentage` must be a number; the loader returns an error pointing at line 17, file `de_markup.yaml`, rule index 2. The operator gets a message they can act on. The engine never sees the bad rule.

A useful failure shape:

```go
type RuleLoadError struct {
    File      string
    RuleIndex int    // -1 for document-level
    RuleID    string // "" if we couldn't even parse the id
    Field     string // "then.value", "when.days_to_departure.lt"
    Message   string
    Cause     error
}
```

The cost of carrying File, RuleIndex, RuleID, and Field is one struct. The savings, every time something fails, is the difference between "the loader failed" and "the loader failed because rule 2 in `de_markup.yaml` set `then.value` to a string". The operator does not have to read your code.

### Validate the set: rules don't exist alone

Once every rule is individually valid, the set has to be valid as a whole. This is where the loader catches the failures that no single rule can detect:

- Two rules with the same name. The engine can't tell them apart at runtime; the loader has to refuse before they're loaded.
- A rule whose conditions can never match because an earlier higher-priority rule already covers its facts. `bre-go`'s `engine/indexed.Engine.Diagnose()` finds these statically; the loader can call it post-compile and surface a warning.
- A rule whose action references a callback name the action registry doesn't know. This is the YAML equivalent of an undefined function.
- A rule whose priority is on the wrong tier of the priority ladder.

Each of these is a class of bug that catches teams once and shapes the loader from then on.

### Compile: from RawRule to engine.Rule

The compile step is where the typed Condition tree is built from the parsed `when` block, where the action callback is bound by name from the catalogue, and where the rule is normalised into the shape the engine consumes.

```go
func compileRule(raw RawRule, actions ActionCatalogue) (engine.Rule, error) {
    cond, err := buildCondition(raw.When)
    if err != nil {
        return engine.Rule{}, fmt.Errorf("when: %w", err)
    }
    act, err := actions.Bind(raw.Then.Type, raw.Then.Params)
    if err != nil {
        return engine.Rule{}, fmt.Errorf("then: %w", err)
    }
    return engine.Rule{
        Name:        raw.ID,
        Description: raw.Description,
        Tags:        raw.Tags,
        Condition:   cond,
        Action:      act,
        Priority:    raw.Priority,
        Enabled:     raw.Enabled,
    }, nil
}
```

The compile step is where the loader's understanding of the schema meets the engine's understanding of the runtime. Splitting it out of the validation step is what lets the loader produce useful errors at the right layer: a validation error talks about YAML, a compile error talks about the engine.

### Swap: atomic or fail-closed

The last step is the one most teams underestimate. The loader has just produced a new engine. It now has to be the engine the running service consults — and that swap has to happen without observable behaviour change other than the rule edit.

The hot path:

```go
type RuleStore struct {
    engine atomic.Value // holds *engine.Engine
}

func (s *RuleStore) Reload(ctx context.Context) error {
    raw, err := s.loader.Load(ctx)
    if err != nil {
        // Existing engine keeps running. Loader failure is not a runtime
        // failure. The reload is a no-op until the source is fixed.
        return fmt.Errorf("load: %w", err)
    }
    next, err := s.compile(raw)
    if err != nil {
        return fmt.Errorf("compile: %w", err)
    }
    s.engine.Store(next)
    return nil
}

func (s *RuleStore) Execute(ctx context.Context, in Facts) (Result, error) {
    return s.engine.Load().(*engine.Engine).Execute(ctx, in)
}
```

Two things in this snippet are doing more work than they look like.

The reload is *fail-closed*. If anything in the loader pipeline fails, the running engine keeps serving traffic with the rule set it already has. The system does not degrade because somebody pushed a typo. It also does not silently apply a partial reload — the new engine is built completely or not at all.

The swap is *atomic*. The `sync/atomic.Value` stores a pointer to the entire engine. The Execute path reads the pointer once per call. No request sees a half-loaded rule set. This is exactly the pattern `bre-go`'s indexed adapter uses internally for its post-Build snapshot.

{{< plantuml title="The loader is the boundary between authored intent and runtime behaviour" >}}
@startuml
skinparam shadowing false
skinparam componentStyle rectangle
skinparam defaultFontName "Helvetica"

actor "Operator" as O
rectangle "Rule files\n(YAML / JSON)" as F
rectangle "Loader\nparse → validate → compile" as L
rectangle "Running engine\n(snapshot N)" as E1
rectangle "New engine\n(snapshot N+1)" as E2
rectangle "Request path\nExecute(ctx, facts)" as R

O --> F : edit
F --> L : pickup
L -[#red]-> O : fail-closed (validation error)
L --> E2 : compile success
E2 --> E1 : atomic swap
R --> E1 : reads pointer once
@enduml
{{< /plantuml >}}

## Schema evolution: changing the file shape without breaking history

The `version: 1` at the top of the file is what makes schema evolution survivable. When the schema needs to change — say, the `then` block grows a new operator, or `metadata` gains a required field — the loader can be taught to read both shapes.

The pattern that has aged best for me:

```go
type loader struct {
    versions map[int]ruleParser
}

func (l *loader) Load(b []byte) ([]engine.Rule, error) {
    var head struct{ Version int }
    if err := yaml.Unmarshal(b, &head); err != nil {
        return nil, fmt.Errorf("parse version: %w", err)
    }
    parser, ok := l.versions[head.Version]
    if !ok {
        return nil, fmt.Errorf("unknown schema version %d", head.Version)
    }
    return parser.Parse(b)
}
```

Three properties of this pattern are worth keeping.

It is *additive*. New schema versions register new parsers. Old files keep loading. The team that owns rules from two years ago does not have to migrate when the schema grows.

It is *explicit*. The version is in the file. The loader does not infer the schema by sniffing fields. A schema-sniffing loader works until it doesn't, usually at 2am.

It is *transient*. Migration from v1 to v2 is a one-time job. The v1 parser does not have to live forever — once every file is at v2, the v1 parser can be retired with a release note. The version field's job is to make that retirement deliberate, not to keep every parser alive indefinitely.

## Invalid rules: fail closed, never silent

The single most expensive mistake in a loader is treating an invalid rule as a missing rule. Both leave the engine without that rule. Only one of them tells the operator something is wrong.

The default I have settled on:

- Document-level failure (YAML / JSON malformed, schema version unknown): the entire file is rejected, the existing engine keeps running, the loader returns an error.
- Per-rule failure (validation error in one of N rules): the *whole file* is rejected. Not the rule. The file.

That last choice is the one teams push back on the most. Surely, the argument goes, the other rules in the file are still valid? Why throw them away?

Because partial loads make the system stop being explainable. If the operator edits file `de_markup.yaml` and one rule fails to validate, the question they want to answer is *what is the engine running right now?* If the loader rejected the file, the answer is the previous version of the file, in its entirety. If the loader rejected one rule, the answer is the new version of the file *minus one rule*, which is a rule set nobody wrote, nobody reviewed, and nobody can reconstruct from version control. The partial-load engine is a state no human approved.

A loud reject is a state somebody approved: the previous file. The cost is one rule that doesn't get its update until the operator fixes the typo. The benefit is a system that never silently runs a configuration no human authored.

## Versioning the rule store, not just the rules

Most teams version their rule files in `git`. That handles "what did this rule look like a month ago?" — well, more or less, because YAML diffs are infamous.

What `git` does not handle on its own is *what was the engine running at 14:32 on Tuesday?* For that you need a different kind of version: the version of the *snapshot* the engine had loaded at that moment.

A small but durable practice: stamp every successful reload with a snapshot ID, log it, expose it in `/healthz`. The snapshot ID can be a hash of the canonicalised, compiled rule set; it does not need to be sequential. What it needs to be is *reproducible from source*.

```go
type Snapshot struct {
    ID        string    // sha256 of canonicalised rules
    LoadedAt  time.Time
    Source    string    // commit sha, or file checksum
    RuleCount int
}
```

When something goes wrong in production, the question is not "what does the file say now?" The question is "what was loaded at 14:32?" The snapshot ID is the only thing that answers that without ambiguity. `bre-go`'s `ExportSnapshot` / `LoadSnapshot` are built for exactly this purpose: the engine can serialise its compiled state at any moment, and a replay session can load the same state to reproduce the decision.

## Observability of the data plane

A loader that works silently is a loader that is fooling you. The minimum signal surface I push teams to ship from day one:

- Counter: successful reloads, with the snapshot ID as a label.
- Counter: failed reloads, with the failure stage (parse / validate / compile / swap) and a short reason.
- Gauge: current snapshot ID, current rule count, current oldest review_after date in the active set.
- Log line per failed reload, including file, rule index, rule id, field, and reason.

These four signals turn a YAML file into something operable. Without them, the operator has to dig through service logs hoping the parser printed something useful. With them, the dashboard shows the rule store as a first-class component of the service.

## What we have agreed to so far

Three posts in, the contract is starting to take shape. The Rule struct from Post 2 is the in-memory shape. The schema from this post is the on-disk shape. The loader is the function that turns one into the other, and the loader is itself an engineering surface — validated, versioned, observable, fail-closed.

The next post moves from the loader to the matcher. With a typed Condition tree and a clean Rule set, the engine has to decide *which* rules match a given set of facts. That decision turns out to be the single most over-simplified part of most rule systems. First-match, all-match, priority-ordered, specificity-ordered — each one is a different bet about how rules interact. The fifth post takes that decision and builds the evaluation pipeline that turns matched rules into a result the caller can act on.

For now, the rule we agreed on is the loader. Rules as data is not a YAML file. Rules as data is a YAML file *plus a loader that treats authoring as the boundary it actually is*. The cheering when a rule edit ships without a deploy is real. The thing that makes the cheering safe to repeat the next morning is the loader.
