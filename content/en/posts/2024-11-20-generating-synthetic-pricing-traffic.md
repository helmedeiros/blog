---
title: "Generating Synthetic Pricing Traffic"
subtitle: "Synthetic traffic is not fake data. It is controlled pressure on assumptions your production data cannot, by definition, exercise."
author: helio
layout: post
date: 2024-11-20T10:00:00+00:00
series:
  - pricing-engineering
series_order: 8
categories:
  - Engineering
  - Pricing
  - Architecture
tags:
  - pricing
  - traffic-generation
  - load-testing
  - architecture
  - go
  - simulation
description: "Production traffic carries last week's biases. Synthetic traffic carries the scenarios you need to test before they happen. This post is about generating it deliberately."
---

The first load test I ran against a new pricing engine used four million requests from production logs. The plan was simple: replay yesterday, see if the new engine handles it. The plan worked. The engine handled it. We shipped.

Two days later a single market spiked traffic to 8x normal because of a holiday, and the engine fell over. The replay had carried yesterday's mix of markets. Yesterday had not had the holiday spike. The test had been thorough about a question we had already answered and silent about the one we needed to answer.

That is the rest of this post. Production traffic is the wrong default for testing a pricing system, because production traffic is *yesterday's* mix of inputs. The pricing system has to survive *tomorrow's* mix — and the rule changes the team is about to ship, and the market the company is about to enter, and the failure mode the engineer is worried about at 2am. None of those exist in the prod logs.

The reference for the rest of the series shifts to [`traffic-gen`](https://github.com/helmedeiros/traffic-gen), a small Go binary I maintain that synthesises pricing request shapes at configurable QPS and persona mixes. It is the second of the two repos this series is built around. Where `bre-go` is about evaluating rules, `traffic-gen` is about giving the engine inputs to evaluate.

## Why production data is the wrong default

Three things go wrong when production logs become the input to your testing strategy.

**They carry yesterday's distribution.** The booking mix in your logs is the mix that already happened. The mix you need to handle is the one that is about to happen — different season, different campaign, different competitor pricing, different regulatory shift. A test that replays last week's distribution proves the engine survived last week. It is silent about everything else.

**They are scrubbed of the fields you actually need.** Customer ID is gone. Email is gone. Payment method is gone. Anything PII-shaped has been redacted by the logging pipeline, which means the conditions the rule engine matches on — segment, device, channel — are partial. Your replay is replaying a fragment of the request, and the fragment is not always the part the rules cared about.

**They lack the scenarios you need to stress.** The new market launches on Tuesday. The new rule fires only on weekends in Q4. The compliance override has never actually triggered in production. None of these scenarios are in the prod logs because, by definition, they have not happened yet. Testing them requires synthesising them.

The first time you discover this, the instinct is to go back to the log pipeline and ask for more retention, less redaction, better volume. That is the wrong fix. The right fix is to stop using prod logs as the test input and start generating traffic that shapes itself around the question you are trying to answer.

## What synthetic traffic actually is

Synthetic traffic is *generated* request shapes, with controlled distributions, that the system under test consumes as if they were real. The word "synthetic" carries a connotation of "fake," which is the wrong reading. The right reading is *deliberately shaped*. Each request is plausible — it has the same fields as a real request, the same types, the same ranges — but the *mix* is decided by the team, not by what production happened to produce.

A traffic generator has three jobs:

**Produce realistic request shapes.** The Request struct matches the engine's contract. Markets are real ISO codes. Days-to-departure are non-negative. Channels are the channels the engine knows about. A request that does not validate against the production schema is a request that exercises the engine's *validation* path, which is a different test from the one you wanted.

**Sample from a controlled distribution.** Each field has a distribution. Market is a weighted choice across the markets the team operates in. Days-to-departure is a long-tailed distribution centred on the typical lead time. Channel mix is weighted toward whichever channel the team is focusing on this quarter. The shape of the distribution is the test's hypothesis.

**Drive load at a configurable rate.** Requests per second. Burst patterns. Sustained load. The QPS knob is decoupled from the generation knob — the generator can produce twice as many shapes as the poster sends, with the poster picking the ones it sends, or the poster can replay a small generator output at high rate. `traffic-gen`'s hexagonal architecture separates these two concerns: `Generator` produces Request shapes; `Poster` sends them at QPS. They tune independently.

A request that comes out of the generator is indistinguishable from a real one at the wire. What is different is the *mix*. The mix is the experiment.

## Distributions: shape over noise

The most common mistake in traffic generation is to model every field as a uniform random sample over its allowed range. Uniform random produces traffic that looks like nothing real has ever looked like. The matcher hits its rare branches at uniform rate; rare bugs come out. Common bugs do not.

What you usually want is the *shape* of production — not the data, the shape — overlaid with the scenario you want to stress.

A useful taxonomy:

| Field | Shape in production | Useful generator |
| --- | --- | --- |
| `market` | Heavily weighted toward 3-5 markets, long tail | Weighted choice, configurable per scenario |
| `days_to_departure` | Long-tailed; median ~21, 5% of bookings under 7 | Log-normal or Weibull, parameterised |
| `channel` | Bimodal: web and mobile dominate, others <5% | Weighted choice |
| `customer_segment` | Long-tail of segments, top 5 = 80% of traffic | Power-law sample |
| `base_price` | Right-skewed, occasional very high values | Log-normal |
| `regulated_market` | Binary, rare (~2% in production) | Bernoulli, configurable rate |

Each distribution is one of a small set of standard shapes — uniform, weighted-choice, Bernoulli, log-normal — parameterised to produce the mix the test calls for. The generator's job is to make these parameters explicit knobs.

```yaml
# A scenario file the team can review.
name: "Q4 holiday spike on DE rail"
qps: 5000
duration: 10m

facts:
  market:
    type: weighted_choice
    weights:
      DE: 0.55          # 8x normal — this is the stress
      FR: 0.15
      IT: 0.15
      ES: 0.10
      _other: 0.05

  channel:
    type: weighted_choice
    weights:
      rail:  0.65
      bus:   0.20
      ferry: 0.15

  days_to_departure:
    type: log_normal
    median: 14
    sigma: 0.8
    min: 0

  device:
    type: weighted_choice
    weights:
      mobile: 0.75      # mobile-heavy holiday traffic
      web:    0.25

  regulated_market:
    type: bernoulli
    p: 0.02
```

This file is a hypothesis the team has agreed on. *In Q4, DE rail traffic spikes 8x and tilts mobile.* The engine consumes the generated traffic and produces explanations; the test asserts what should be true under that load.

A YAML scenario is a different thing from a YAML rule. The rule says what the engine should do. The scenario says what the world is doing. Both have the same property — versioned, reviewable, owned — but they evolve on different schedules.

## Personas: making the abstraction concrete

A persona is a named pattern of facts that produces a recognisable kind of request. Personas exist because "weighted choice over markets and devices" is unmemorable; "Berlin commuter on mobile" is not.

The shape:

```yaml
personas:
  - name: berlin_commuter
    weight: 0.35
    facts:
      market: DE
      channel: rail
      device: mobile
      days_to_departure:
        type: weighted_choice
        weights: { 0: 0.40, 1: 0.30, 2: 0.20, 3: 0.10 }
      base_price:
        type: log_normal
        median: 25
        sigma: 0.3

  - name: italian_holiday_planner
    weight: 0.15
    facts:
      market: IT
      channel: ferry
      device: web
      days_to_departure:
        type: log_normal
        median: 45
        sigma: 0.4
      base_price:
        type: log_normal
        median: 120
        sigma: 0.6

  - name: cross_border_business
    weight: 0.10
    facts:
      market:
        type: weighted_choice
        weights: { DE: 0.4, FR: 0.4, NL: 0.2 }
      channel: rail
      device: web
      days_to_departure:
        type: weighted_choice
        weights: { 1: 0.5, 2: 0.3, 3: 0.2 }
      base_price:
        type: log_normal
        median: 180
        sigma: 0.5
```

Three personas with weights that sum to less than 1 are intentional: the remaining 0.4 of traffic comes from a default "long-tail" persona that uses the broader distributions. The team can now talk about the test in human terms: *the Q4 scenario is 35% Berlin commuters, 15% Italian holiday planners, 10% cross-border business, and a 40% long tail*.

Personas are the abstraction that lets product and engineering have the same conversation. The product owner reads "Berlin commuter" and knows what scenario they are looking at. The engineer reads "Berlin commuter" and sees the distribution. The test runs the same code regardless.

In `traffic-gen`, personas are a layer on top of the `randommix` generator: each persona is a named bundle of field-level distributions; the mix is a weighted choice across persona generators.

## Scenarios: traffic, rules, and an expected outcome

A scenario is a complete experiment. It packages a traffic shape, a rule set, and an expectation. Running the scenario is a deterministic activity; reading the output is a comparison against the expectation.

```yaml
scenario: q4_de_holiday_spike
description: |
  Validates that the DE rail short-lead-time markup stays correct
  under 8x normal market weighting, that the indexed matcher's
  bucket distribution stays healthy, and that p99 Execute latency
  stays under 5ms.

traffic: scenarios/q4_de_holiday_spike.yaml   # the personas + distributions
rules:   fixtures/2024-q4-candidate.yaml      # the candidate rule set
duration: 10m
qps: 5000

expectations:
  result:
    - field: markup_percentage
      assertion: |
        For all Berlin commuter requests with days_to_departure < 7,
        the result must include short_lead_time_markup_de and
        germany_baseline_markup. Sum must be 5.0%.

  performance:
    - p50_execute_ms: { lt: 1.0 }
    - p99_execute_ms: { lt: 5.0 }
    - candidate_set_size_p99: { lt: 20 }

  rule_hygiene:
    - shadowed_rule_warnings: { eq: 0 }
    - failed_action_rate: { lt: 0.001 }
```

This file is the test plan. The traffic generator drives the load. The engine produces explanations. A scenario runner aggregates over the explanations and asserts the expectations. The output is pass / fail, with a structured diff when something violates an expectation.

The discipline that makes scenarios useful is that they live in version control, are reviewed in PRs, and are run on every release. A scenario that has run cleanly for six months and starts failing tomorrow is the team's earliest possible warning that something has shifted — in the rule set, in the engine, or in the team's understanding of the world.

## Reproducibility: seeds and fixtures

A traffic generator that produces different output every run is a generator you cannot debug. The shape that has aged best for me is a generator that takes a seed and produces *identical* requests, in the same order, every run with the same seed.

```sh
git clone https://github.com/helmedeiros/traffic-gen
cd traffic-gen

# Reproducible run: every request is determined by the seed.
./traffic-gen \
  --scenario scenarios/q4_de_holiday_spike.yaml \
  --seed 20241120 \
  --target http://localhost:8080/price \
  --qps 5000 \
  --duration 10m
```

The seed is the difference between a test you can debug and a test that mocks you. If a request triggers a bug on Tuesday, the same seed reproduces it on Wednesday. The bug is repeatable; the investigation is bounded; the regression test you write to pin the fix can hard-code the seed and reproduce the offending request indefinitely.

A second pattern that pays off: capture the first N requests as a fixture file. The fixture is a binary or JSON dump of the first 1000 requests the generator produced under a given seed. The fixture is small (a few MB), version-controllable, and exactly reproducible across machines. Tests that should run on every PR use the fixture; load tests that run nightly use the generator with the seed.

```go
// traffic-gen exposes a Capture mode for fixture generation.
gen := traffic.NewGenerator(scenario, traffic.WithSeed(20241120))
fixture := traffic.Capture(gen, 1000)
fixture.WriteFile("testdata/q4_holiday_first_1000.bin")
```

In `traffic-gen`, the `Generator` and `Poster` ports are separated specifically so the same generator output can feed a Poster (for live runs against a service), a Capture (for fixture generation), and a Replay sink (for the shadow-mode work in the next post). Each output mode is one adapter behind one port; the generator does not need to know which is on the other side.

## The architecture: hexagonal, by design

`traffic-gen`'s design is a single shape carried across three boundaries.

{{< plantuml title="traffic-gen: generator produces shapes, sinks consume them, QPS knob lives on the sink" >}}
@startuml
skinparam shadowing false
skinparam componentStyle rectangle
skinparam defaultFontName "Helvetica"

rectangle "Scenario file\n(personas, distributions)" as SF
rectangle "Generator port\nproduce(seed) → Request" as G
rectangle "randommix adapter\nweighted choice + log-normal" as GA

rectangle "Sink port\nconsume(Request)" as S
rectangle "HTTP Poster\nPOST to target URL\nQPS-controlled" as SP
rectangle "Fixture Capture\nwrite to disk" as SF2
rectangle "Replay sink\n(used in post 9, 10)" as SR

SF --> GA
GA ..|> G
G  --> S
S  <|.. SP
S  <|.. SF2
S  <|.. SR
@enduml
{{< /plantuml >}}

Two properties earn their way in.

**The QPS knob is on the sink, not the generator.** The generator produces shapes as fast as it can; the sink decides how fast to send. This separation is what lets the same generator drive a live load test at 10 000 QPS and a deterministic fixture capture at no QPS at all. Generators that try to do their own rate-limiting end up bottlenecked on time.Sleep loops, which is not the bottleneck you want when you are testing 10 000 QPS.

**The sink is an interface, not an HTTP client.** The HTTP poster is one adapter. The fixture capture is another. The replay sink — which the next post leans on — is a third. Each sink is a small file behind the same interface. The generator does not need to know which sink is on the other side; the test does not need to know how the generator produced its shapes.

The cost is two extra packages on day one. The benefit is that the same code drives load tests, fixture generation, and replay all the way through the simulation post in this series.

## What "controlled pressure" actually means

The framing I have settled on, after a few cycles of getting this wrong, is that synthetic traffic is *controlled pressure on system assumptions*.

A pricing engine has assumptions baked into it. The matcher assumes that most rules will have at least one indexable term. The composer assumes that resolution conflicts will be rare. The loader assumes that rule files will be small. Each assumption is correct on yesterday's traffic. Each assumption could be wrong on tomorrow's.

Synthetic traffic is the way to put pressure on each assumption deliberately. A scenario file that says "what happens when 60% of traffic is in a new market with no rules yet?" is the way to discover that the matcher's empty-candidate-set warning path was never exercised. A scenario that says "what happens when the rule file grows to 10 000 rules?" is the way to discover that the indexed engine's Build time crosses a service-level threshold the team didn't know existed.

The output of these scenarios is not "the engine passed." The output is *which assumption the engine has, and whether the assumption survives the pressure*. A scenario the engine passes is one assumption confirmed. A scenario the engine fails is one assumption to redesign.

```
# A typical output of a scenario run, on the team's CI:
scenario        q4_de_holiday_spike
duration        10m0s
total_requests  3_000_000

result_assertion          PASS  (3_000_000 / 3_000_000 match)
p50_execute_ms            PASS  (0.41ms,  threshold 1.0ms)
p99_execute_ms            FAIL  (6.82ms,  threshold 5.0ms)
candidate_set_size_p99    PASS  (12,      threshold 20)
shadowed_rule_warnings    PASS  (0)
failed_action_rate        PASS  (0.0001)

ARTIFACTS
  - sampled explanations (1 in 10_000):      120 records
  - p99 outlier explanations (top 1%):       30_000 records
  - histogram of candidate set sizes:        attached
  - rule hit-count distribution:             attached
```

The p99 failure becomes an investigation: which rule's evaluation is slow? Which condition is the bottleneck? Is it the index's bucket size, the composer's per-field loop, or the action callback? The next layer of artifacts — the sampled explanations and the per-stage latency from Post 7 — is where the answer lives.

## Anti-patterns I have shipped and watched ship

Three traffic-generation mistakes that look reasonable and aren't.

**The "uniform random" generator.** Every field sampled uniformly over its range. Looks fair. Looks unbiased. Produces traffic that exercises rare branches at rare rates, dominant branches at moderate rates, and the actual production distribution at zero rate. The bugs that ship to production are the bugs in the dominant branches; uniform-random will not find them.

**The "amplified prod log" generator.** Take yesterday's logs, multiply by 10, replay. Identical to the load test in the opening anecdote. Carries the same biases as production; finds the same bugs production has already found. Useful for performance regression; useless for scenario exploration.

**The "every test team writes their own" generator.** Each team writes a small synthetic generator for their own service. The generators all produce slightly different schemas, slightly different distributions, slightly different defaults. Shadow-mode comparisons across services become impossible because the inputs are not aligned. A shared generator, even a minimal one, removes a class of cross-service confusion.

The first one is a bug in the distribution model. The second is a bug in the choice of input. The third is a bug in ownership. Each has cost teams quarters of effort that a slightly more deliberate design would have saved.

## What the team gets when this is built

Three durable benefits.

**The team can pose questions in advance.** *What happens if next week's launch puts 60% of traffic in a new market?* becomes a scenario file, not a prayer. The scenario runs against a candidate rule set; the team sees the impact before the launch.

**The team can reproduce production-like load deterministically.** *Run the Q4 scenario at seed 20241120* produces the same 3 million requests every time. Performance regressions become measurable. The "the engine got slower" complaint becomes the "p99 went from 4.1ms to 5.8ms between commits X and Y" claim.

**The team can connect traffic to explanation.** Every synthetic request produces an explanation. The traffic generator carries metadata about which persona produced each request. The aggregator can answer "for Berlin commuters, what was the median markup?" — and the answer is a query against the explanation store, not a guess from the dashboard.

The cost is a small Go binary, a YAML scenario format, a Go interface for the sink, and a discipline of writing the scenarios down. Modest. The benefit is the rest of this series — shadow mode, replay-based simulation, and the impact-assessment workflow that ties all of them together.

## What comes next

The next post is shadow mode — running a candidate pricing path alongside the active one, on the same live request, comparing the outputs without affecting the customer. Shadow mode is what closes the loop between traffic generation and production. The generator can stress test the candidate offline; shadow mode tests the candidate online, on the actual mix of traffic, before the candidate becomes the active path.

The post after that is replay-based simulation, which ties `bre-go` and `traffic-gen` together formally: a stored snapshot of the engine, a captured fixture of traffic, and a candidate rule set produce a deterministic comparison of outcomes. That comparison is the rule reviewer's tool — the way to ask "what does this change actually do?" and get a structured, reproducible answer.

For now, the lesson is the framing. Production traffic is the wrong default because it carries the past. Synthetic traffic is the right default because it can carry the future the team is preparing for. The traffic generator is a small piece of code with an outsized role: it is the system that tells the engine what is about to be true.

The replay-of-yesterday load test from the opening anecdote was, after that incident, retired. We kept it around for one thing — a regression test against the bug it had missed. Then we built scenarios for the holidays we knew were coming, the markets we knew were launching, and the rules we knew were being added. The next traffic spike came on schedule. The engine handled it. We didn't take a screenshot.
