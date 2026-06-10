---
title: "Structured Logs: Stop Writing Sentences, Start Writing Data"
date: 2017-06-15T14:00:00-03:00
author: Helio Medeiros
subtitle: Treat your logs as the queryable system surface they actually are—events with fields, correlation identifiers across services, and the difference between a log line you can read and one you can answer questions with
tags:
  [
    "observability",
    "structured logging",
    "correlation ids",
    "distributed systems",
    "production",
  ]
categories: ["Engineering"]
---

## Why I Gave This Talk

<iframe class="speakerdeck-iframe" frameborder="0" src="https://speakerdeck.com/player/a15505b34ade437c9b20a104c8860a3b" title="Structured Logs" allowfullscreen="true" allow="web-share" style="border: 0px; background: padding-box padding-box rgba(0, 0, 0, 0.1); margin: 0px; padding: 0px; border-radius: 6px; box-shadow: rgba(0, 0, 0, 0.2) 0px 5px 40px; width: 100%; height: auto; aspect-ratio: 560 / 420;" spellcheck="false" data-ratio="1.3333333333333333"></iframe>

Almost every production incident I've ever joined started the same way: someone shared a log line, somebody else wrote a regex to extract a field, and ten minutes later we were debating whether the timestamps in two different services were even in the same timezone.

This talk is about why we shouldn't be writing logs that need a regex.

## A Log Line Is an Event

The mental flip is small but it changes everything. A log line isn't a sentence describing what happened — it's an **event** with a shape. The moment you treat it as an event, two things follow:

- It has **fields**, not words. `user_id`, `request_id`, `latency_ms`, `outcome`.
- It is **queryable**, not searchable. You filter by field value, not by hoping the word "error" appears.

Unstructured logs are sentences. Structured logs are data.

```text
# unstructured
2017-06-15 14:02:11 user 8131 hit /checkout and got 500 in 842ms

# structured
{"ts":"2017-06-15T14:02:11Z","app":"checkout","user_id":8131,
 "path":"/checkout","status":500,"latency_ms":842,
 "trace_id":"7f2c…","event":"request.completed"}
```

The second one isn't "more verbose." It's _readable by a machine_, which means it's readable at scale.

## Fields Worth Having on Every Line

The minimum useful event shape, in my experience:

- **`ts`** — timestamp in UTC, ISO 8601. Always UTC. Time zones in logs are a tax you pay every incident.
- **`app`** / **`service`** — which service emitted this.
- **`event`** — a stable, low-cardinality name (e.g. `request.completed`, `payment.captured`). Not a sentence.
- **`level`** — info / warn / error.
- **`trace_id`** / **`correlation_id`** — the identifier that follows one user action across services (more on this below).
- **`outcome`** / **`status`** — did the thing succeed.

Everything else is context. Add freely, but keep these six honest.

## Correlation IDs: The One Field That Changes Debugging

When a single user click touches five services, five services produce logs. The only way to stitch them back together is to give that click an identifier at the edge and propagate it through every internal call.

Call it `trace_id`, `correlation_id`, `request_id` — pick one and stay consistent. Generate it at the first hop (load balancer, gateway, frontend). Pass it forward on every HTTP header, every queue message, every downstream call. Log it as a field on every line.

The first time you grep a single ID and watch the entire user journey unfold across services in chronological order, you stop wanting unstructured logs.

## Logs vs Metrics vs Traces

Structured logs are not a replacement for metrics or distributed traces — they're a different cut of the same truth.

- **Metrics** answer "is the system healthy right now?" Aggregates over time. Cheap to store, hard to slice after the fact.
- **Traces** answer "where did this one request spend its time?" A causal tree across services.
- **Logs** answer "what exactly happened in this event?" High fidelity, high cardinality, expensive at volume.

Structured logs are the cardinality budget you spend when you actually need to know _which_ user, _which_ payload, _which_ branch of the code path. Don't try to make logs do metrics' job; do feel free to ship them with the same identifiers traces use, so you can pivot between them.

## What Goes Wrong When You Don't Do This

Three patterns I see often.

**Logs as console.log.** Developers print sentences while building, and the sentences ship. Production debugging becomes archaeology.

**Sensitive data leaking in.** Once a log line is unstructured, nobody knows what's in it. Emails, tokens, payload bodies — they sneak in because there's no schema saying "this field, not that one."

**Cardinality explosions.** Free-form messages with unique substrings (timestamps in the message, IDs concatenated into strings) blow up indexes and bills. Fields with stable names and dynamic values are cheap; sentences with embedded values are expensive.

## What to Change Tomorrow Morning

If you take one thing from this talk:

1. Pick a structured format. JSON if your stack supports it, key-value if not.
2. Decide on the six fields above. Document them. Defend them.
3. Generate a correlation ID at the edge and propagate it.
4. Stop printing sentences. Emit events.

You don't need a new vendor. You don't need a rewrite. You need a habit.

## Closing

The teams I've worked with that took structured logging seriously didn't get better dashboards. They got faster incidents. The thing you measure most is the time from "something is wrong" to "I know what."

That time is mostly spent _reading_ logs. Make them readable.

---

Follow me: [@helmedeiros](https://twitter.com/helmedeiros)
