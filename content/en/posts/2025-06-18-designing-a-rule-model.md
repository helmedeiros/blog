---
title: "Designing a Rule Model"
subtitle: "The Rule struct is the contract between business intent and runtime execution. Get the contract wrong and every other layer pays for it."
author: helio
layout: post
date: 2025-06-18T10:00:00+00:00
series:
  - building-pricing-systems
series_order: 2
categories:
  - Engineering
  - Pricing
  - Architecture
tags:
  - pricing
  - business-rules
  - rule-engine
  - go
  - type-systems
  - architecture
description: "Designing the in-memory Rule type is the moment you commit to a contract. This post pulls bre-go's Rule, Condition, and Action apart and shows where the tradeoffs live."
---

There is a moment, three days into building a rule store, when somebody on the team says: *just make it a `map[string]interface{}`.*

It's a tempting suggestion. The map is flexible. The map will accept anything. The map will not break when somebody adds a new field next quarter. The team is moving fast and the map is the cheapest data structure to type.

The map will also make every test you write useless.

This post is about the rule model — the in-memory representation of a rule — and why getting it right is the single most consequential design choice in the rest of the engine. Everything that comes later, from matching to storage to explainability, takes the rule model as input. If the model is shapeless, none of those layers can do their job. If the model is over-shaped, the system stops being able to express what the business actually wants. The job of this post is to find the line.

The reference code I'll be pulling from is [`bre-go`](https://github.com/helmedeiros/bre-go). The Rule struct shape, the Condition / Action types, and the parser tree all live there.

## What goes into a Rule

The smallest useful Rule type carries five things: an identity, the gate (when it applies), the body (what it does), the lifecycle (whether it is on and in what order), and the metadata (the bookkeeping that makes the rule readable after the original author leaves).

Here is what that looks like in Go, modelled on `bre-go`'s `inmemory.Rule`:

```go
// Rule is the in-memory contract a business rule has to honour.
type Rule struct {
    Name        string   // stable identity. Used everywhere — logs, tests, explanations.
    Description string   // a sentence. What this rule is trying to express.
    Tags        []string // ownership, category, lifecycle. Cheap to query.
    Condition   Condition
    Action      Action
    Priority    int  // higher = considered first in priority-ordered engines
    Enabled     bool // off-switch without a deploy
}
```

The struct is intentionally narrow. No timestamps. No history. No "owner" field. That is on purpose: those things belong in metadata, and metadata belongs in a separate concern that can evolve without touching the type the engine consumes. The engine should not need to know that `created_by: helio` exists. The engine should need to know that the rule has a Name, has a Condition, has an Action, has a Priority, and has an Enabled flag.

Already there are decisions baked into this struct that are worth pulling out.

**Name as identity, not ID.** The Name is what shows up everywhere: in matched-rule listeners, in test failures, in the explanation log. It has to be human-readable. A UUID gives you uniqueness; it gives you nothing else. The Name has to be enforced unique at registration time — `bre-go`'s `inmemory.AddRule` returns `ErrEmptyRuleName` and `ErrDuplicateRuleName` for exactly that reason.

**Description as a sentence.** Not a doc-comment. Not a multi-paragraph essay. One sentence the rule has to fit into. If you can't fit the rule into one sentence, the rule is doing two things, and the second one needs its own rule.

**Tags as the cheap query layer.** Once you have more than a hundred rules, you will need to ask the system questions like *show me every active rule owned by pricing-DE that wasn't reviewed in the last six months*. Tags are how you answer those questions without building a query DSL.

**Priority and Enabled as runtime knobs, not policy.** These two fields exist because runtime needs them, not because business cares about them. Priority is the engine's way of resolving conflicts when multiple rules match; Enabled is the team's way of turning a rule off without redeploying. They have to be in the type because the engine needs them, but they should be invisible to the rule author when possible.

{{< plantuml title="The Rule struct: identity, gate, body, runtime, bookkeeping" >}}
@startuml
skinparam shadowing false
skinparam componentStyle rectangle
skinparam defaultFontName "Helvetica"

rectangle "Rule" as R {
  rectangle "Identity\nName, Description, Tags" as ID
  rectangle "Gate\nCondition" as G
  rectangle "Body\nAction" as B
  rectangle "Runtime\nPriority, Enabled" as RT
}

rectangle "Metadata\n(separate concern)" as MD

ID --> RT : shapes lifecycle
G  --> B  : when matched, run
MD ..> R  : describes, doesn't bind
@enduml
{{< /plantuml >}}

## Condition: function or typed expression?

The Condition is the most consequential type in the rule model. It is the thing the matcher looks at. The shape of the Condition determines whether matching can be sub-linear, whether rules can be serialized, whether the rule can be inspected without running, and whether two rules can be compared statically.

There are two common shapes, and they have very different futures.

### The function shape

The function shape is what every engineer reaches for first:

```go
type Condition func(in interface{}) bool
```

This is `bre-go`'s most permissive shape, used by `engine/inmemory` and the `conditions` package:

```go
import "github.com/helmedeiros/bre-go/engine/conditions"

rule := inmemory.Rule{
    Name:        "high-value-clean-usd",
    Description: "approve high-value USD orders that are not flagged",
    Tags:        []string{"approval"},
    Condition: conditions.And(
        func(in interface{}) bool { return in.(Order).Amount > 100 },
        func(in interface{}) bool { return in.(Order).Currency == "USD" },
        conditions.Not(func(in interface{}) bool { return in.(Order).Flagged }),
    ),
    Action: func(interface{}) interface{} { return "approve" },
}
```

This is wonderful for an engineer writing the rule in Go. The condition is literal code. The compiler checks it. There is no parser, no DSL, no schema.

It is also, as soon as the rule has to leave the engineer's machine, completely opaque. You cannot serialize a `func(in interface{}) bool`. You cannot ask the matcher "which rules look at the `market` field?" You cannot tell a product manager "here is what the rule says." All you have is the source code.

The function shape works when every rule will be authored by an engineer and shipped with a deploy. The moment that stops being true, you need a typed shape underneath the function shape.

### The typed expression shape

The typed shape replaces the function with a tree of inspectable nodes. `bre-go`'s `engine/parser` package is built around this:

```go
// A condition tree the engine can read, serialize, and analyse.
type Condition interface {
    Eval(in map[string]string) bool
}

type StringCondition struct {
    Field string
    Op    Op       // OpEq, OpNeq
    Value string
}

type SetCondition struct {
    Field  string
    Op     Op       // OpIn, OpNotIn
    Values []string
}

type AndCondition struct{ Children []Condition }
type OrCondition  struct{ Children []Condition }
type NotCondition struct{ Child Condition }
type RangeCondition struct {
    Field    string
    Min, Max float64
}
```

The same "high-value clean USD" rule, in the typed shape, would look like this:

```go
rule := indexed.Rule{
    Name: "high-value-clean-usd",
    Match: parser.AndCondition{Children: []parser.Condition{
        parser.RangeCondition{Field: "amount", Min: 100.01, Max: math.Inf(+1)},
        parser.StringCondition{Field: "currency", Op: parser.OpEq, Value: "USD"},
        parser.StringCondition{Field: "flagged", Op: parser.OpNeq, Value: "true"},
    }},
    Action: func(interface{}) interface{} { return "approve" },
}
```

The condition is now something you can walk. You can ask it which fields it touches. You can build a hash bucket key from it. You can compare two rules and detect that one shadows the other. You can serialize it to JSON and reload it.

`bre-go`'s `engine/indexed` adapter uses exactly this. It walks the typed Condition at `Build()` time, classifies each clause as indexable (equality, IN), or post-filter (NEQ, NOT IN, range), and builds a hash bucket structure that turns Execute from O(N rules) into O(K hash lookups + small post-filter set). Pre-Build, the engine accepts AddRule; post-Build, it refuses further mutation and serves Execute concurrently from an immutable snapshot held in `sync/atomic.Value`.

You don't get any of that with a `func(in interface{}) bool`. The typed shape unlocks an entire category of runtime work.

### The tradeoff

| Concern | Function shape | Typed shape |
| --- | --- | --- |
| Author ergonomics | Excellent — it's just Go code | Verbose — every clause is a struct |
| Serialization | Impossible — code can't be marshalled | Native — JSON / YAML out of the box |
| Static analysis | None — opaque to the engine | Walkable tree, shadowing detection, dead-rule reports |
| Matching performance | Linear in rules | Sub-linear with the right index |
| Compile-time safety | Full — Go checks it | Partial — operators are runtime-checked |
| Rules authored by non-engineers | Impossible | Possible (through a UI or DSL on top of the tree) |

The pragmatic answer in `bre-go` is to keep both: the inmemory adapter accepts the function shape; the indexed adapter requires the typed shape; the `engine/parser` package compiles a string DSL (`"market == \"DE\" AND days_to_departure < 7"`) into the typed shape for callers who don't want to write `StringCondition{...}` by hand. The Rule struct is the same shape in both; only the field that holds the condition changes.

That dual-track decision is, in my experience, the single most freeing design choice in a rule model. You can offer engineers the fast path. You can offer everyone else the structured path. You don't have to pick.

## Action: the contract goes outward here

The Action is where the rule meets the rest of the world. The engine evaluates the condition and then has to do something. That something has two possible shapes that mirror the Condition decision.

The function shape:

```go
type Action func(in interface{}) interface{}
```

The typed shape, more like:

```go
type Action struct {
    Type   string                 // "set_markup", "choose_provider"
    Params map[string]interface{} // type-specific
}
```

The function shape is faster to write and arbitrarily expressive. The typed shape lets you serialize, lets you check at registration time that every action type is one the runtime knows how to execute, and lets you do interesting things later — like cataloguing every action used across the whole rule set, or rejecting any rule whose action would require an out-of-band side effect the engine can't reverse.

In `bre-go`, Action is `func(interface{}) interface{}` for the in-process engines. The exec wrapper `exec.Executor[In, Out]` adds typed input and output around that:

```go
ex := exec.New[Order, string](e)
decision, matched, err := ex.Execute(ctx, Order{
    Amount:   250,
    Currency: "USD",
})
```

That is the second freeing design choice in the model: keep the underlying engine shape uniform, and let the caller wrap it for ergonomics. The engine works in `interface{}` because that's what makes it polymorphic. The caller works in `Order` and `string` because that's what makes the call site readable.

## Facts: what the engine sees

The facts are the dictionary the rule evaluates against. The Condition reads facts; the Action receives them. The facts are the public surface between the caller and the engine.

The two shapes are familiar by now:

```go
// Typed facts — the call site uses real domain types.
type Order struct {
    Amount   float64
    Currency string
    Flagged  bool
    Market   string
}

// Generic facts — what the matcher actually compares against.
type Facts map[string]string
```

`bre-go`'s indexed engine works against `map[string]string` because that is the shape the parser produces and the shape the bucket keys can be built from. Strings are flat. They hash cleanly. The matcher does not need to know what `currency` "really" means; it needs to know what to look up.

Domain code, on the other hand, wants `Order.Amount`. The typed exec wrapper bridges the two: the caller passes `Order`; a marshaller turns it into `map[string]string` (or whatever shape the engine wants); the engine matches; the result comes back as `Result`, which the caller unwraps into `Decision`. The marshaller is the boring layer that nobody writes about; it is also the one place where the typed world meets the generic world. It is worth giving it a name and a test suite.

{{< plantuml title="The contract: typed at the edges, generic in the middle" >}}
@startuml
skinparam shadowing false
skinparam componentStyle rectangle
skinparam defaultFontName "Helvetica"

actor "Caller code" as C
rectangle "exec.Executor[In, Out]\ntyped wrapper" as W
rectangle "engine.Engine\nin: interface{} / map[string]string\nout: Result" as E
rectangle "Rule\nName, Condition, Action,\nPriority, Enabled" as R

C  --> W : Order, ctx
W  --> E : Facts (map[string]string)
E  --> R : evaluate
R  --> E : matched, action result
E  --> W : Result
W  --> C : Decision (string)
@enduml
{{< /plantuml >}}

## Priority and Enabled: the runtime knobs

Priority and Enabled are the two fields engineers always want to add later. They never look critical upfront; they always become critical the second something matters.

Priority resolves ordering. In the priority-ordered first-match adapter (`engine/priority` in bre-go), rules are evaluated highest-Priority first; ties break by registration order. This is not a luxury — the moment you have two rules that can both match the same facts, *something* is going to order them, and you would rather it be the integer in the rule than `git blame` of who added the file first.

A common shape:

```go
// Priority is an integer ladder, not a single value.
const (
    PriorityCompliance int = 1000 // legal mandates — must run first
    PriorityRevenue    int = 500  // markup and discount rules
    PriorityExperiment int = 100  // A/B experiment overrides
    PriorityDefault    int = 0    // fallback / catch-all
)
```

The ladder is short on purpose. Engineers will try to negotiate a Priority of 437 because their rule is *almost* compliance but not *quite*. The ladder forces them to put the rule in a tier with intent. If two rules end up tied inside a tier, that is the kind of conflict you want to surface at registration, not in production.

Enabled is the off-switch. The off-switch is what turns a regrettable rule decision into a phone call instead of a rollback. It has to be in the rule model — not in a separate "disabled rules" list, not in an external feature flag — because at runtime the engine still has to load the rule, decide it's off, and skip it cleanly without affecting matching semantics for the other rules. An `Enabled bool` on the struct does that for the cost of one field.

There is one decision around Enabled worth making early: does a disabled rule still appear in the explanation log? My answer has always been *yes*. If a rule is off, downstream investigation should be able to see that it was off, not just absent. Absent rules and disabled rules feel the same to anyone reading the log without telemetry; explicit "disabled" is the kindness you give your future self at 3am.

## Metadata: out of the Rule, into the registry

This is the part of the rule model that the engine does not need. It is the part that everyone else does.

```go
type RuleMetadata struct {
    Owner       string
    Intent      string
    Created     time.Time
    Author      string
    Ticket      string
    Experiment  string
    ReviewAfter time.Time
}
```

`bre-go` keeps the engine-facing Rule clean (Name, Condition, Action, Priority, Enabled) and lets metadata live in a `RuleInfo` lister that adapters opt into. The reason is simple: the matcher does not need a `ReviewAfter`. The explanation log might. The admin UI definitely does. The compliance audit absolutely does. The matcher should not pay the cost of carrying fields it never reads.

Splitting metadata out of the Rule has one durable benefit: it lets the metadata schema evolve without forcing an engine rebuild. We added an `Experiment` field three months after the engine shipped, and the engine code did not change.

## The contract metaphor

The Rule model is the contract between business intent and runtime execution. Pull that sentence apart and you get the design rules that produced everything above.

The contract is *narrow*. The Rule type carries what the engine has to know, and nothing else. Engine-only fields (Priority, Enabled) are in the type. Metadata fields (Owner, Ticket) are in a sidecar. Authoring conveniences (DSL strings, fluent builders) sit on top of the type, not inside it.

The contract is *stable*. `bre-go` ships at v0.19 and the Rule struct shape has changed twice. Each time the change was tied to a documented ADR. The point is not that the struct can never change; the point is that changing it has a procedure, because every adapter and every test depends on it.

The contract is *typed at the edges*. The caller writes `Order`. The engine reads `map[string]string`. The wrapper bridges. Putting `interface{}` at the boundary is what lets the engine be polymorphic; putting types around the boundary is what lets the call site be readable.

The contract is *explainable*. The Rule has a Name and a Description. The Condition has a tree the engine can walk. The Action has a Type the catalogue can list. Each of those is one tiny commitment that compounds into "the system can explain itself" three posts from now.

## What comes next

The next post takes the same Rule type and asks the harder question: *what does it look like when it lives on disk?* That is where YAML and JSON come back, where versioning shows up, where schema validation starts to matter, and where the "rules as data" idea earns its name.

The post after that goes into matching semantics — first-match versus all-match, priority versus specificity, indexable versus post-filter clauses, and the strange shape of the bug you get when two adapters disagree about which rule fires.

For now, the takeaway is the contract. If the in-memory Rule type carries the right things, every layer above and below it has something to stand on. If it carries too much, the layers get heavy. If it carries too little, the layers get clever. Designing the Rule type is the moment you decide which kind of mistake you are willing to make later.

I prefer too little. The map temptation, for all its appeal, makes a system that cannot age. The narrow struct, designed slowly, can.
