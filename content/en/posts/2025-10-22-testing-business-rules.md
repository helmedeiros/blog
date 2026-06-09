---
title: "Testing Business Rules"
subtitle: "Tests that pin the engine's internals will rot. Tests that pin the business behaviour will outlive every refactor you ship."
author: helio
layout: post
date: 2025-10-22T10:00:00+00:00
series:
  - building-pricing-systems
series_order: 6
categories:
  - Engineering
  - Pricing
  - Architecture
tags:
  - pricing
  - business-rules
  - testing
  - golden-tests
  - property-based-testing
  - go
description: "Most rule engine tests protect implementation details and quietly let business behaviour drift. This post is about the kinds of tests that catch the bugs that actually matter."
---

The CI badge was green for fourteen months. The dashboard showed the same.

Then somebody asked a question about why a particular German booking had been charged a 5% markup instead of 3%, and the answer turned out to be that the engine had been computing markups wrong for nine months. Not catastrophically wrong. Off by a hundred basis points on a slice of traffic that nobody had thought to alert on. The test suite, by then 11 000 lines long, had been passing the whole time.

I read every test in that suite. Every one of them was a perfectly reasonable test. They tested that the matcher returned the rules they should. They tested that the action ran. They tested that the loader rejected malformed YAML. None of them tested that, given a German booking inside a short lead-time window, the customer was charged 3%.

The suite was protecting the engine. It wasn't protecting the business behaviour. That distinction is the rest of this post.

## Two layers, two intents

A rule system has two layers that look the same in code and behave completely differently when you try to test them.

The engine layer — matcher, evaluator, executor, composer — is what runs the rules. It is mostly stable. It changes when somebody refactors a data structure, swaps an adapter, or upgrades an interface. When the engine layer changes, the tests that pin its internals break.

The rules layer — what each rule is supposed to do for the business — is what changes constantly. New rules get added. Old rules get edited. Priorities get renegotiated. When the rules layer changes, the tests that pin the business behaviour should *not* break unless the change to the rules is also a change to the business agreement.

The 11 000 line suite was almost entirely tests of the engine layer. There was nothing protecting the business agreement. The engine could refactor itself confidently and the dashboard could be wrong, and both could be simultaneously fine in the test suite's worldview.

The framing I have settled on: the engine layer earns *unit tests and property tests*. The rules layer earns *behavioural tests and golden tests*. The two have different lifespans and different shapes.

## Behavioural tests: the contract the business signed

The first test you should write for any rule is the test that pins what the business agreed to.

```go
func TestGermanShortLeadTimeMarkup(t *testing.T) {
    t.Parallel()
    store := loadRuleStore(t, "fixtures/2025-q3.yaml")

    ex := exec.New[Booking, Price](store.Engine())
    price, matched, err := ex.Execute(context.Background(), Booking{
        Market:           "DE",
        DaysToDeparture:  4,
        Channel:          "rail",
        BasePrice:        100.00,
    })

    if err != nil {
        t.Fatalf("execute: %v", err)
    }
    if !slices.Contains(matched, "short_lead_time_markup_de") {
        t.Errorf("expected short_lead_time_markup_de to fire; got %v", matched)
    }
    if price.Markup != 3.0 {
        t.Errorf("expected markup 3.0; got %.2f", price.Markup)
    }
}
```

This test reads like a sentence the team agreed on. *For a German rail booking four days from departure, the short-lead-time markup fires and applies 3%.* It does not care which adapter the engine uses. It does not care how the matcher is implemented. It does not care whether the action is a function or a typed catalogue entry. It cares that, given the facts the business agreed are interesting, the engine produces the answer the business agreed is correct.

It is also the test that survives every refactor. When somebody swaps the linear matcher for the indexed one, this test keeps passing. When the engine grows a new stage, this test keeps passing. When the loader changes its YAML schema, this test only fails if the rule's authored intent changes — which is exactly when you *want* it to fail.

Three properties make this test useful:

**The facts are realistic.** The Booking struct is what the call site actually produces. Not a synthetic `map[string]string` with three fields. The test is downstream of the typed exec wrapper so it exercises the marshaller as well.

**The assertion is the business agreement.** *Charge 3%.* Not *the matcher returns rule index 7*. The first will outlive the engine; the second will break the next time somebody changes how rules are indexed internally.

**The fixture is named after the rule set version.** `2025-q3.yaml`. When the rules change next quarter, a new fixture is added; the old test still passes against the old fixture; the team can see at a glance which test pins which agreement.

## Table-driven tests for breadth

The behavioural test above pins one scenario. The business has dozens of them, and writing each one out by hand is how the suite grows tedious and how scenarios get forgotten.

Table-driven tests are the right shape:

```go
func TestPricingScenarios(t *testing.T) {
    store := loadRuleStore(t, "fixtures/2025-q3.yaml")
    ex := exec.New[Booking, Price](store.Engine())

    tests := []struct {
        name           string
        booking        Booking
        expectMatched  []string
        expectMarkup   float64
    }{
        {
            name:          "DE short lead-time rail booking",
            booking:       Booking{Market: "DE", DaysToDeparture: 4, Channel: "rail"},
            expectMatched: []string{"short_lead_time_markup_de", "germany_baseline_markup"},
            expectMarkup:  5.0, // 3% short-lead + 2% baseline, sum policy
        },
        {
            name:          "DE long lead-time rail booking",
            booking:       Booking{Market: "DE", DaysToDeparture: 21, Channel: "rail"},
            expectMatched: []string{"germany_baseline_markup"},
            expectMarkup:  2.0,
        },
        {
            name:          "FR baseline booking",
            booking:       Booking{Market: "FR", DaysToDeparture: 14, Channel: "rail"},
            expectMatched: []string{"france_baseline_markup"},
            expectMarkup:  1.5,
        },
        {
            name:          "compliance override beats everything",
            booking:       Booking{Market: "DE", DaysToDeparture: 4, RegulatedMarket: true},
            expectMatched: []string{"compliance_markup_override"},
            expectMarkup:  0.0,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel()
            price, matched, err := ex.Execute(context.Background(), tt.booking)
            if err != nil { t.Fatalf("execute: %v", err) }

            if !equalStringSets(matched, tt.expectMatched) {
                t.Errorf("matched mismatch:\n  got:    %v\n  expect: %v", matched, tt.expectMatched)
            }
            if math.Abs(price.Markup-tt.expectMarkup) > 0.001 {
                t.Errorf("markup mismatch: got %.2f, expect %.2f", price.Markup, tt.expectMarkup)
            }
        })
    }
}
```

The table is the test surface the product team can review. The names read like ticket titles. The booking is the request. The expectation is the agreement. When a new scenario shows up in a PR, the diff is one row. When a scenario changes meaning, the diff is one column in one row.

Table-driven tests carry one trap: the temptation to put implementation details into the table. The moment the table starts asserting *which buckets the indexed engine hashed into*, the table has stopped being a business artifact. Keep the table on the side of the agreement — facts in, decision out.

## Golden tests for the explanation

The Execute stage from Post 5 produces an Explanation. The Explanation is the second artifact worth pinning, because changes to the Explanation are changes to what the team can debug with.

The pattern:

```go
func TestPricingExplanationsGolden(t *testing.T) {
    store := loadRuleStore(t, "fixtures/2025-q3.yaml")
    engine := store.Engine()

    cases, err := filepath.Glob("testdata/scenarios/*.json")
    if err != nil { t.Fatal(err) }

    for _, scenario := range cases {
        name := strings.TrimSuffix(filepath.Base(scenario), ".json")
        t.Run(name, func(t *testing.T) {
            req := loadRequest(t, scenario)
            result, explanation, err := engine.ExecuteWithExplanation(context.Background(), req)
            if err != nil { t.Fatalf("execute: %v", err) }

            got := canonicaliseExplanation(result, explanation)
            golden := "testdata/golden/" + name + ".json"

            if *update {
                writeJSON(t, golden, got)
                return
            }
            wantBytes, err := os.ReadFile(golden)
            if err != nil { t.Fatalf("read golden: %v", err) }

            if diff := jsonDiff(wantBytes, got); diff != "" {
                t.Errorf("explanation diff (-want +got):\n%s\n\nrun with -update to accept", diff)
            }
        })
    }
}
```

The golden file looks like this:

```json
{
  "result": {
    "markup_percentage": 5.0,
    "matched": ["short_lead_time_markup_de", "germany_baseline_markup"]
  },
  "evaluations": [
    {"rule": "compliance_markup_override", "outcome": "failed_condition", "failed_at": "when.regulated_market.eq"},
    {"rule": "short_lead_time_markup_de", "outcome": "fired"},
    {"rule": "germany_baseline_markup", "outcome": "fired"},
    {"rule": "france_baseline_markup", "outcome": "failed_condition", "failed_at": "when.market.eq"}
  ],
  "composer": "additive_with_compliance_override",
  "snapshot": "sha256:7b3f...e91d"
}
```

When somebody changes the engine, this test surfaces every change in observable behaviour. New explanation fields are visible in the diff. Re-ordered evaluations are visible. A near-miss that used to be reported and now isn't, is visible.

The risk with golden tests is that engineers learn to run `-update` reflexively. The defence is to make the diff readable: canonicalise the JSON, sort the keys, format numbers consistently. A diff that says *one number changed* is one a reviewer will read. A diff that re-orders every key is one a reviewer will rubber-stamp.

I keep one rule: a golden update is its own commit. Never the same commit as the code change that produced it. The reviewer of the code change reviews the code; the reviewer of the golden update reviews the diff. Conflating them is how regressions sneak in.

## Property-based tests for invariants

Behavioural tests pin specific scenarios. Property tests pin invariants — statements that should be true for *every* input.

Three invariants I have always written for a rule engine:

**The candidate set is a superset of the fired set.** Whatever the matcher returns must include every rule the evaluator fires. The evaluator can drop rules from the candidate set; it must not invent rules.

**The Result obeys the resolution policy.** If the policy says markups are summed, then for any set of fired rules, the Result's markup must equal the sum of the individual rule outputs. If the policy says one wins, the Result must be exactly one of the individual outputs.

**Disabled rules never fire.** For any rule set and any facts, a rule with `enabled: false` must never appear in the fired set.

In Go with `gopter` or a similar generator:

```go
func TestCandidateSetIsSuperset(t *testing.T) {
    properties := gopter.NewProperties(nil)

    properties.Property("candidate set ⊇ fired set", prop.ForAll(
        func(facts Facts) bool {
            engine := buildEngine(arbitraryRuleSet(50))
            candidates, fired, _ := engine.ExecuteForTesting(facts)

            candidateSet := toSet(candidates)
            for _, r := range fired {
                if !candidateSet.Contains(r) {
                    return false
                }
            }
            return true
        },
        genFacts(),
    ))

    properties.TestingRun(t)
}
```

The shape of property tests is foreign at first. The test does not say *given this fact, expect this rule*. It says *given any fact, this relationship holds*. The generator produces hundreds of fact sets per test run; the engine answers each one; the invariant is checked across all of them.

The bugs property tests catch are the bugs you didn't think to write a unit test for. The fact set that has fifteen markets and a negative days_to_departure. The rule set with a circular priority dependency. The Facts map with a duplicated key. These are not bugs you would have specified upfront; they are bugs the engine has to handle anyway.

`gopter`'s `MinSuccessfulTests` defaults to 100; for rule engines I push it to 1000 because the generators are cheap and the engine is fast. A single run that catches a counterexample once is worth a thousand runs that confirm the invariant. The counterexample is recorded as a regression test (more on that below) and the engine is fixed.

## Mutation-style tests: confidence in the suite

The 11 000 line suite passed for fourteen months and missed the bug. The question that should have surfaced sooner is *would these tests fail if I broke the engine?*

Mutation testing answers that question directly. The mutation tool changes one operator at a time in the engine code — flips `<` to `<=`, replaces `+` with `-`, changes `&&` to `||` — and runs the test suite against each mutated version. A mutation that the suite catches is good; a mutation the suite misses is a hole in the suite.

In Go, `gremlins` or `go-mutesting` are the usual tools:

```sh
# Run mutation testing on the engine package.
gremlins unleash ./engine/...
```

A typical output:

```
package engine/indexed/
  mutated 142 statements
  killed 119 (84%)
  lived  23
    engine/indexed/matcher.go:87 — `==` → `!=` lived
    engine/indexed/matcher.go:103 — `<` → `<=` lived
    ...
```

23 surviving mutations is 23 places where the suite cannot tell if the engine is right or wrong. Each one is either a missing test or a bug-tolerant test. The next pull request closes the gap one mutation at a time.

The cost is runtime. Mutation testing on a small package is seconds; on a real codebase it is hours. The discipline I have settled on: run mutation testing on the engine packages weekly, not on every PR. The signal is "is the suite getting better or worse at catching mutations?", which is a slow-changing metric.

The most uncomfortable part of mutation testing is that it makes the suite's actual coverage visible. Line coverage was 92% in the 11 000 line suite. Mutation kill rate was 41%. Most of the lines were *executed* by tests; only some of them were *checked*. That gap is the invisible failure mode every rule engine suite has, and the only way to see it is to mutate.

## Regression tests: the bug, immortalised

Every production bug deserves a test that pins the fix.

```go
// PRICE-1820: a German rail booking 4 days out was charged 3%
// markup but the explanation log showed only the baseline rule
// firing. Fixed in commit 7b3f...e91d by repairing the indexed
// matcher's bucket key construction for compound conditions.
//
// This test must continue to pass forever.
func TestPRICE_1820_ShortLeadTimeMatchesIndexedAdapter(t *testing.T) {
    t.Parallel()
    store := loadRuleStore(t, "fixtures/PRICE-1820.yaml")
    engine := store.IndexedEngine()

    booking := Booking{Market: "DE", DaysToDeparture: 4, Channel: "rail"}
    result, explanation, err := engine.ExecuteWithExplanation(context.Background(), booking)
    if err != nil { t.Fatal(err) }

    matchedNames := matchedNames(explanation)
    if !slices.Contains(matchedNames, "short_lead_time_markup_de") {
        t.Errorf("short_lead_time_markup_de must fire on this fact set; got %v", matchedNames)
    }
    if result.Markup != 5.0 {
        t.Errorf("expected combined markup 5.0; got %.2f", result.Markup)
    }
}
```

Three properties of a regression test that matter:

**It names the bug.** Not "TestMatchesShortLeadTime" — `TestPRICE_1820_…`. The name is the ticket. The test is the contract that the ticket stays closed.

**It pins the minimum facts that reproduce.** A regression test that needs a 200-line fixture is a regression test that will be deleted in a refactor. The minimum reproduction is the asset.

**It includes a comment that says why it exists.** The comment is the postmortem. The next engineer who reads the test should understand both what it asserts and what business pain it prevented.

Regression tests accumulate. After two years a rule engine has a regression file with a hundred entries. They are slow to run. They are also the only tests that catch the bug somebody re-introduces in 2027 because they didn't know about 2025. The accumulation is the point.

## What not to test

Three categories of test waste engineering attention and earn the team nothing:

**Tests for the engine's internal data structures.** *Asserting that the indexed engine has 17 buckets after loading these 50 rules* is a test for `bre-go`'s problem, not yours. If the engine changes how it indexes, the test breaks; the business behaviour did not change; the suite's signal has gone down.

**Tests for the engine's listeners.** *Asserting that OnRuleMatched fires exactly N times* is testing the engine. The engine's own test suite has those tests. The application suite should test the business outcome the listener-emitted record describes, not the listener mechanism.

**Tests that lock in implementation choices the team hasn't agreed to.** *Asserting that R7 has priority 437* is locking in a value that probably shouldn't have been 437 to begin with. The right test is *R7 takes precedence over R3*. That assertion survives the priority refactor.

The general rule: tests that break when the engine refactors but the business behaviour does not change are tests that should not have been written. Tests that pass when the engine refactors but the business behaviour silently regresses are bugs in the suite.

## Loader tests: the negative space

Most teams test that the loader successfully loads good files. Few teams test that the loader correctly *rejects* bad ones. The negative space is where the loader tests pay back.

```go
func TestLoaderRejectsBadFiles(t *testing.T) {
    cases := []struct {
        name        string
        file        string
        wantErrPart string
    }{
        {"unknown action type", "bad/unknown_action.yaml", "unknown action type"},
        {"non-numeric markup", "bad/string_markup.yaml", "then.value must be number"},
        {"duplicate rule name", "bad/duplicate_name.yaml", "ErrDuplicateRuleName"},
        {"missing schema version", "bad/no_version.yaml", "schema version"},
        {"shadowed rule", "bad/dead_rule.yaml", "rule never fires"},
    }

    for _, tt := range cases {
        t.Run(tt.name, func(t *testing.T) {
            _, err := loader.Load(tt.file)
            if err == nil {
                t.Fatal("expected error; got nil")
            }
            if !strings.Contains(err.Error(), tt.wantErrPart) {
                t.Errorf("error %q does not contain %q", err, tt.wantErrPart)
            }
        })
    }
}
```

Each row is a class of bug the loader is meant to catch. Each row's fixture is committed in the testdata directory. When somebody changes the loader, this test enforces that the rejection messages do not silently regress.

The hardest of these is the *shadowed rule* case. It tests `engine/indexed.Engine.Diagnose()` against a rule set where one rule provably can never fire. The fixture is small (two rules) and the assertion is on the diagnostic, not on the runtime behaviour. This is the test that catches the silent dead rule before production does.

## A test suite, in the shape it should be

If I were rebuilding the 11 000 line suite from scratch, the shape would be:

```
testdata/
  fixtures/                   # rule sets, one per quarter
    2025-q3.yaml
    2025-q4.yaml
  scenarios/                  # named business cases (JSON requests)
    de-short-lead-rail.json
    fr-baseline.json
    compliance-override.json
  golden/                     # the explanations we agreed on
    de-short-lead-rail.json
    fr-baseline.json
  bad/                        # files the loader must reject
    unknown_action.yaml
    string_markup.yaml
engine/
  matcher_test.go             # unit tests for one stage
  evaluator_test.go
  composer_test.go
behaviour/
  pricing_scenarios_test.go   # table-driven behavioural tests
  golden_test.go              # explanation goldens
loader/
  loader_test.go              # positive + negative loader tests
properties/
  invariants_test.go          # property-based tests
regressions/
  price_1820_test.go          # one file per ticket
  price_1873_test.go
  ...
```

The shape is the lesson. Tests are organised by *what they protect*, not by *which file they live next to*. The behaviour directory protects the business agreement. The engine directory protects the engine mechanics. The regressions directory remembers what hurt. The properties directory pins invariants. Each directory has a different lifespan, a different audience, and a different reason to fail.

{{< plantuml title="Two test layers, two intents, two lifespans" >}}
@startuml
skinparam shadowing false
skinparam componentStyle rectangle
skinparam defaultFontName "Helvetica"

rectangle "Business behaviour\n(survives refactors)" as BB {
  rectangle "Behavioural tests\n(scenarios → outcomes)" as B1
  rectangle "Golden explanations" as B2
  rectangle "Regression tests\n(immortalised bugs)" as B3
}

rectangle "Engine mechanics\n(broken by refactors)" as EM {
  rectangle "Unit tests per stage" as E1
  rectangle "Property tests\n(invariants)" as E2
  rectangle "Mutation testing\n(suite health)" as E3
}

BB --> EM : depends on but does not pin
EM ..> BB : provides the surface
@enduml
{{< /plantuml >}}

## What the team gets when the suite has the right shape

Three things.

**Refactors stop being scary.** When the behavioural tests are the contract, swapping the matcher from linear to indexed is a green CI run, not a holy week. The engine mechanics can move; the business contract holds.

**Reviews get sharper.** A PR that changes the rule set produces a diff against the behavioural tests. The product team can read the diff. The engineering team can see whether the diff is intentional. The conversation is "did the agreement change?" — not "did the test pass?"

**Bugs become teachers.** Every regression test in the suite is a bug that never came back. The team's collective memory of past incidents is encoded in code. A new engineer can read the regression directory and learn what the system has been bitten by.

The 11 000 line suite had none of these properties. It had high line coverage and low business coverage. The dashboards were green and the markups were wrong. The rebuild took six months, ended at 6 000 lines, and caught the next four near-misses before production did.

## What comes next

The next post is explainability — the artifact this whole testing layer assumes. Every behavioural test asserts a fact about the Explanation. Every golden test pins the Explanation. Every regression test reaches for the Explanation. The next post is what makes the Explanation worth reaching for: how it is structured, what it carries, what it costs to produce, and what kinds of investigations it enables.

After that we move to synthetic traffic. Tests are deterministic; production is not. Generated traffic is the bridge: it is reproducible like a test and shaped like production, and it is what makes the next layer of validation — shadow mode and replay — meaningful.

For now, the lesson is the contract. Tests for a rule system have to protect the business agreement, not the engine's implementation. The engine layer earns tests that measure mechanics; the rules layer earns tests that pin behaviour. When the two are confused, the suite goes green for fourteen months and the customer pays for the gap.

Write the tests the next engineer needs to understand. Pin the scenarios the team agreed to. Immortalise the bugs you have already paid for. The engine refactor will come, and the suite that survives it is the one that knew what it was protecting in the first place.
