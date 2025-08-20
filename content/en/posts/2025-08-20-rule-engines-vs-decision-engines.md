---
title: "Rule Engines vs Decision Engines"
subtitle: "A rule engine answers what matches. A decision engine answers what should happen. The gap between those two questions is where most pricing platforms grow up."
author: helio
layout: post
date: 2025-08-20T10:00:00+00:00
series:
  - pricing-engineering
series_order: 11
categories:
  - Engineering
  - Pricing
  - Architecture
tags:
  - pricing
  - rule-engine
  - decision-engine
  - architecture
  - models
  - constraints
description: "A rule engine matches rules against facts and runs actions. A decision engine coordinates rules with models, constraints, policies, and experiments to produce a single explained decision. This post is about the gap between the two and when each is the right tool."
---

There was a Tuesday morning when I tried to express a single pricing decision as a single rule and discovered I needed three.

The decision was small in business terms: *apply a base markup, but cap it by a per-customer fairness budget, but override both if an active experiment is running for this customer, and never exceed the regulatory ceiling in this market*. The product owner had described it in one sentence. By the time it was in the rule store it was three rules with carefully tuned priorities, a fourth rule for the regulatory ceiling, a comment block explaining the dependency between them, and a comment-block prediction that "we will regret this."

The prediction was right. Six weeks later the experiment changed shape, a priority needed to move, and the fairness cap interacted with the new markup in a way that the rule engine could not see. We caught it in shadow mode before it shipped. The fix was structural, not local — we did not need to edit one rule; we needed a layer above the rule engine that could *coordinate* the rule outputs with the model output, the constraint, and the experiment context. The team had been building a rule engine for months. We had just discovered that what we actually needed was a decision engine.

That is the rest of this post. A rule engine answers *what matches*. A decision engine answers *what should happen*. The gap between those two questions is where most pricing platforms grow up.

## What the rule engine is, in one frame

The rule engine, after ten posts of careful design, has a tight contract:

```
Execute(ctx, facts) → Result
```

Facts go in. The matcher finds the rules whose conditions are satisfied by the facts. The evaluator confirms them. The executor runs each rule's action. The composer combines the action outputs into a result, per a resolution policy.

The rule engine is good at one specific thing: *running declared rules deterministically and explainably*. It is not good at the things on either side of that one thing.

It does not decide *which rules to even consider*. The whole rule set is loaded; the engine matches over everything. If you want to consider rules conditionally — say, only the experiment-overlay rules when an experiment is active — you can encode that as part of the matching, but the engine itself does not have a notion of *contexts* the way a decision engine does.

It does not coordinate the *outputs* with anything outside the engine. The composer can combine outputs from rules but not from a model that lives in another service. If the markup should be the *minimum* of what the rule engine produces and what an elasticity model recommends, the rule engine cannot express that on its own.

It does not enforce *external constraints* the rules do not encode. A regulatory ceiling that should hold across every possible rule combination has to be re-encoded as a rule in the engine, which means changes to the ceiling are now rule edits, which means the constraint and the rule have collapsed into the same layer.

The Tuesday morning I described was the moment those three limits intersected. The decision had multiple inputs — rules, model, constraint, experiment context — and the rule engine could only see one of them. The platform's rule engine was working perfectly. The platform did not have a decision engine.

## What a decision engine adds

A decision engine sits *above* a rule engine. Its contract is wider:

```
Decide(ctx, context) → Decision + Explanation
```

Where `context` is not just facts — it is the bundle of inputs the decision needs, of which facts are one:

- The **request facts** (what the rule engine consumes).
- A set of **rule sets** to evaluate (possibly more than one; possibly conditional).
- **Model outputs** the decision should consider (elasticity, demand forecast, fraud score).
- **Constraints** the final decision must satisfy (regulatory ceiling, fairness budget, never-do).
- **Policy** about how to combine the above (rules-first, model-first, constrained-optimisation).
- **Experiment context** that may shape which rules and which model and which policy.

A decision engine accepts that bundle, coordinates the components, and emits a single decision with a single explanation. The rule engine is one of several inputs.

{{< plantuml title="A decision engine coordinates rules with the other inputs to a real decision" >}}
@startuml
skinparam shadowing false
skinparam componentStyle rectangle
skinparam defaultFontName "Helvetica"

rectangle "Request\nfacts + correlation_id" as R

rectangle "Decision engine" as DE {
  rectangle "Context builder\nfacts + experiment + segment" as CB
  rectangle "Rule engine\n(bre-go)\nmatches & evaluates" as RE
  rectangle "Model service\nelasticity, demand,\nfraud score" as MS
  rectangle "Constraint check\nregulatory, fairness,\nbudget" as CC
  rectangle "Policy composer\ncombines according to\nactive policy" as PC
}

rectangle "Decision\n+ explanation" as D

R --> CB
CB --> RE
CB --> MS
RE --> PC
MS --> PC
PC --> CC
CC --> D
@enduml
{{< /plantuml >}}

The four components above the dashed line are inputs; the components below it are the decision engine's work. The rule engine is the leftmost input, not the centre. The decision engine's centre is the policy composer that turns "here is what each input says" into "here is what the system will do."

## When a rule engine is enough

The honest answer is: most of the time, longer than you would expect.

A rule engine is enough when:

**The decision can be expressed as a deterministic function of facts.** No model. No external service call. The conditions name fields; the actions set values; the result is the composition. Pricing markups in stable markets often fit this shape. Routing decisions usually fit. Many compliance overrides fit.

**The set of inputs that govern the decision is closed.** The team owns every field the rule reads. There is no fact that lives somewhere else (a model service, a real-time signal). Closed input sets are dramatically simpler to reason about than open ones, and a rule engine handles them gracefully.

**The composition policy is simple.** Additive, last-wins, priority-ordered. The composer from Post 5 handles all three with a configuration line each. If your decision is "stack these markups" or "the most specific override wins," a rule engine is the right tool.

**Latency budget is tight.** The rule engine is in-process. A decision engine that calls a model service over the network is in-process *plus* a few hundred microseconds at p50 and several milliseconds at p99. Some pricing surfaces cannot afford the budget.

These four conditions describe the steady state of many pricing systems. A pricing team that ships a clean rule engine and never grows past it is not wasting opportunity; they are matching their tool to their problem.

## When the decision engine becomes necessary

Four signals that the rule engine is being asked to do more than its contract:

**A model output should influence the decision.** The team has a price-sensitivity model whose output should inform the markup but not determine it on its own. Within a rule engine, this becomes either *a rule that consults the model inside its action* (which breaks determinism and explainability) or *a separate service that runs the model and the rule engine and stitches the results* (which is, by another name, a decision engine).

**A constraint must hold across all rule outcomes.** A regulatory cap. A fairness floor. A maximum total discount per customer per quarter. Inside a rule engine, the constraint becomes a rule, which means the constraint's authority and the rule's authority are now the same layer — and the team that owns the constraint and the team that owns the rules may not be the same team. A decision engine separates the constraint into its own check, with its own owner.

**The set of rule sets is conditional.** Experiment A overrides certain rules for certain customers. Experiment B's overrides are different. The matching layer of the rule engine can encode the experiment context as a fact, but the *governance* of which experiments are live, which customers they affect, and what they override is now in the rule store. A decision engine pulls the experiment context out into its own component.

**The decision has to compose inputs from different layers.** The output is *the minimum of A, B, and C, capped by D, biased by E*. The rule engine can compute A. The model service computes B. C is a configured cap. D is a regulatory value from a compliance service. E is an experiment lift. None of these alone are the answer; the answer is what the composer makes of them together.

When two or more of these signals appear, the platform is no longer a rule engine that wants to grow. It is a decision engine that has been deferred. The Tuesday morning incident was the moment the platform I had been building crossed that line, and the rule engine kept working but stopped being sufficient.

## The seams that earn their way in

Three seams the decision engine has to manage. Each one is a place the platform either gets architecture or gets technical debt.

### Rules + models

A model output is not the same shape as a rule output. The rule engine produces a structured result with provenance: *short_lead_time_markup_de set markup to 3% at priority 500*. The model produces a number with confidence: *elasticity_v3 estimates markup of 2.7% with 90% CI [2.4, 3.0]*.

The decision engine has to coordinate them. The cleanest pattern I have seen in practice — though, like the lab in Post 10, this one I have explored in design more than in production — is to make the model output a *fact* that the rule engine consumes, and then encode the policy of how the rule and the model interact as part of the rule itself.

```yaml
- id: markup_with_elasticity_bias
  intent: |
    Apply the rule-defined markup, but lean it 30% toward the
    elasticity model's recommendation. The rule remains the
    business contract; the model is one of its inputs.
  when:
    market: { eq: DE }
    days_to_departure: { lt: 7 }
  then:
    type: blended_markup
    base: 3.0
    bias_field: model.elasticity_v3.markup
    weight: 0.30
```

The rule's *intent* is the contract the team owns. The model's value is the *bias*. The composer applies a deterministic blend. The explanation can carry both the rule's intent and the model's value side by side, so the auditor can see which one drove which fraction of the final number.

The risk in this pattern is the model becoming a hidden author of rules the team did not write. The defence is to keep the rule explicitly in control: the rule says *what to do with* the model; it never delegates the decision to the model.

### Rules + constraints

A constraint is a rule that the team did not write, that must hold regardless of which rules did fire. A regulatory cap. A never-discount-below-cost floor. A fairness bound.

Encoding these as rules inside the rule engine is tempting and a long-term mistake. The constraint has different ownership (legal, compliance, finance), different change cadence (slower), and different failure mode (a violation is a regulatory event, not a service event).

The decision engine treats constraints as a separate stage. Rules produce a candidate decision. Constraints check the candidate. If the candidate violates a constraint, the decision engine either rejects (returning a safe default), clips (capping at the constraint's value), or escalates (logging and surfacing for review). Each behaviour is configurable per constraint.

```go
type Constraint interface {
    Check(decision Decision, ctx Context) ConstraintResult
}

type ConstraintResult struct {
    Violated  bool
    Action    string  // "reject", "clip", "escalate"
    ClipValue *float64
    Reason    string
}
```

The explanation carries the constraint result. An audit asking "was the regulatory cap respected?" reads the constraint check, not the rule trace. That separation is what lets compliance own the constraint without owning the rule store.

### Rules + experiments

Experiments are the third seam, and the one where pricing teams most often paper over with rule priorities.

The pattern I have settled on conceptually — and have wanted to build for a while — is to treat experiments as a *context layer* that the decision engine resolves before the rule engine even runs. The experiment context says: *for this request, the rules to consider are {standard rule set} plus {experiment overlay for ELAST-2025-Q3}, with the experiment's overlay taking precedence on the markup fields it touches*.

The rule engine then runs against the merged rule set. The decision engine records *which* experiment overlays were in scope, so the explanation carries the experiment provenance separately from the rule provenance. A request that was charged 4% because of an experiment can be distinguished, at the explanation level, from a request that was charged 4% because of a standard rule that happens to equal 4%.

```go
type ExperimentContext struct {
    ActiveOverlays []RuleSetRef   // overlay rule sets to merge in
    Treatments     map[string]string  // experiment → treatment arm
}
```

The experiment context lets product own the experiments without product owning the rule store. The rule store is the standard policy; the experiment overlay is the perturbation. Both are versioned, both are explainable, both are reproducible against the snapshot.

## When the migration is worth doing

Three pragmatic reasons to invest in the decision engine, and one reason to defer.

**It is worth doing** when the rule engine is being edited to express things it should not have to express. When you find rules that consult external services in their actions, or rules whose priority is being used as governance for constraints, or rules whose conditions encode experiment membership. Each of those is a deferred decision-engine concern leaking into the rule layer.

**It is worth doing** when explanations are getting harder to read. A rule engine explanation lists the rules that fired. A decision-engine explanation lists the rules, the model contributions, the constraint checks, and the experiment overlays. When an auditor's question requires reading the source code to answer, the explanation layer has been overloaded.

**It is worth doing** when the team is starting to draw architecture diagrams that show one component named "the engine" with arrows to everything. The "everything" is what the decision engine is supposed to coordinate. Drawing it as one box hides the seams; the bugs live in the seams.

**It is worth deferring** when the steady state genuinely is "facts in, action out." A team running a clean rule engine for a well-scoped pricing surface should not build a decision engine because the architecture pattern is fashionable. Premature decision engines are heavy, expensive, and a tax every team that touches the system has to pay. Build it when the rule engine is bending; not before.

## The migration path

The cleanest migration I have studied moves in three steps.

**Wrap, don't replace.** The decision engine becomes a new top-level entry point. Internally, it calls the existing rule engine. The first version does nothing the rule engine wasn't already doing — it just gives the team a place to add the next concern. A wrapper is cheap and lets the team validate the seam without rewriting.

**Lift constraints out first.** Constraints are the easiest concern to extract. They have clear ownership, simple semantics (check after, clip or reject), and they reduce the rule store's surface area immediately. The first thing a decision engine should do beyond what the rule engine did is enforce constraints.

**Add the model and experiment seams last.** These two require more design: how does the model value enter the explanation, how does the experiment overlay merge with the standard rule set, what does the audit trail look like. Building them third means the team has lived with the decision engine wrapper for a while and knows what the seam should feel like.

I would build it in that order if I were doing it now. The migration I lived through took a different order, with more pain and more rework. The lesson I keep is the same: extract the simpler seam first.

## The lesson

A rule engine answers *what matches*. A decision engine answers *what should happen*. The gap is real and not always worth crossing — but when it is worth crossing, the cost of pretending the rule engine is enough is paid in the kind of bug that takes shadow mode to catch and replay to defend.

The Tuesday morning incident was a small one. The fix happened in shadow, before customers saw it. But it was the first time I had to admit that the layer I had built — careful, correct, explainable — was no longer where the actual decision lived. The decision had moved up a level. The architecture had to follow.

Most of the value of the distinction is recognising it early. A team that names the difference between *what matches* and *what should happen* can defer the decision engine deliberately, knowing the day to build it will come. A team that does not name the difference will build a decision engine accidentally, by accreting concerns onto the rule engine until the rule engine is no longer recognisable as one.

## What comes next

The next post is about the long term. Pricing systems age. Rules accumulate. Engines get refactored. Constraints change. Experiments retire. The architectural layers in this series — rule model, loader, matcher, evaluator, explanation, shadow, replay, decision engine — all need lifecycles. The next post is about building those lifecycles in from the start, so the platform you ship in year one is still operable in year five.

After that we move to the retrospective half of the series. Ten mistakes I have shipped. What I would build differently today. The last two posts are about what this whole series has been preparing for: the second time you build a pricing platform, with everything the first time taught you.

For now, the lesson is the distinction. The rule engine and the decision engine are not the same thing. The first asks what fits; the second asks what should be. A pricing platform that grows to need the second one is a pricing platform doing well. The work is recognising the moment, building the seam, and not pretending the bigger question is just a harder version of the smaller one.
