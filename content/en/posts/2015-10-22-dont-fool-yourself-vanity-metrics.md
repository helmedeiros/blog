---
title: "Don't Fool Yourself: Vanity Metrics"
date: 2015-10-22T14:00:00-03:00
author: Helio Medeiros
subtitle: Three years after the first time I gave this talk—what I'd say differently now about vanity metrics, A/B testing, cohort analysis, and how to actually run an AAA report your team can act on
tags:
  [
    "vanity metrics",
    "A/B testing",
    "cohort analysis",
    "AAA report",
    "lean startup",
    "metrics",
  ]
categories: ["Leadership", "Agile"]
---

## Why I Gave This Talk Again

<iframe class="speakerdeck-iframe" frameborder="0" src="https://speakerdeck.com/player/c2d159acb0174943896e172f880f412f" title="Don't fool yourself - Vanity Metrics" allowfullscreen="true" allow="web-share" style="border: 0px; background: padding-box padding-box rgba(0, 0, 0, 0.1); margin: 0px; padding: 0px; border-radius: 6px; box-shadow: rgba(0, 0, 0, 0.2) 0px 5px 40px; width: 100%; height: auto; aspect-ratio: 560 / 315;" spellcheck="false" data-ratio="1.7777777777777777"></iframe>

I first gave a version of this talk at the end of 2012 — "Sucesso na medida certa." Three years later, the slide that aged the worst was the one I was proudest of at the time: a beautiful, climbing chart of signups, with no honest answer to "so what?" attached to it.

So I gave it again. Same theme, sharper question. **If you can't do anything to make a metric better — why are you tracking it?**

That question is the whole talk.

## What Vanity Metrics Really Are

A vanity metric isn't a fake number. It's a real number that doesn't change how you decide.

Total registered users. Cumulative downloads. Followers. Page views. They look like progress because they always go up. They have to — once a user signs up, they don't un-sign up. The metric isn't lying; it just isn't telling you anything you can act on.

The test I use is this: if this number went up 30% next week, what would I do? If the answer is "be happy," it's vanity. If the answer is "double down on the experiment that caused it," it's actionable.

## A/B Testing: Where Honesty Starts

If you don't isolate the change, you can't claim the result. That's it. That's the whole point of A/B testing.

In 2012 I had a team show me a quality improvement and a signup spike on the same slide. The next day, the marketing team showed the same spike under their banner ad. Both were right. Both were wrong. Without an A/B test, neither side could honestly say what caused what.

A/B testing isn't a tool you bolt on once a quarter. It's a habit. Every shipped change either has a counterfactual or it doesn't, and if it doesn't, the post-launch story is going to be a fight over credit.

## Cohort Analysis: The Picture the Average Hides

Aggregates lie by averaging. A user who signed up in January behaves nothing like one who signed up last week, and a cohort chart will show you that in 30 seconds while a dashboard total will hide it for a quarter.

Group your users by when they came in (or which experiment they hit, or which channel referred them). Then plot their behavior over time inside their own cohort.

What you'll usually see:

- Activation drops the further from launch you get
- Retention curves diverge by acquisition channel
- A "growing" total is often masking that new cohorts perform worse than old ones

If your total is up and your cohorts are down, you're burning your runway to grow the wrong way.

## The AAA Report: Actionable, Accessible, Auditable

The hardest part of this work isn't picking metrics. It's picking metrics _the team will actually act on_. I started calling that the **AAA Report**.

**Actionable**: every number has a decision attached. If the metric moves up, we do X. If it moves down, we do Y. If we don't know what we'd do either way, it doesn't belong on the report.

**Accessible**: anyone on the team can find it, read it, and explain it without a translator. If only one analyst understands the dashboard, the team isn't using it — the analyst is.

**Auditable**: the source is traceable. We can show how the number was computed, when it was last refreshed, and what its known caveats are. The number that wins an argument is the one nobody can poke holes in.

Two of the three aren't enough. An actionable report nobody can read is a private notebook. An accessible report nobody can verify is a story. Actionable, accessible, and auditable together is what gives a team the confidence to actually move based on what the data says.

## Genchi Genbutsu

Ohno's principle from the Toyota Production System: **go and see for yourself.** Don't infer the problem from a dashboard. Go to where the work happens — talk to the user, watch the funnel, sit with the person closing the ticket — and let what you see correct what you assumed.

Numbers tell you _where_ to look. Genchi Genbutsu tells you _what's actually there._

I still bring this up every time a team builds a beautiful dashboard and forgets they haven't talked to a customer in six weeks.

## What I'd Say Now That I Wouldn't Have in 2012

Three things.

First, a vanity metric on its own isn't dangerous — a vanity metric in a leadership review is. Up-and-to-the-right charts get rewarded. That's a culture problem, not a chart problem. Fix the room before you fix the slide.

Second, A/B tests are not the goal — learning is. If the test isn't going to change a decision regardless of outcome, you're not running a test, you're running a celebration.

Third, the AAA Report isn't a deliverable, it's a discipline. The first version will be wrong. The team gets it right by tightening it every retro for a year.

## Closing

> "Vanity metrics: good for feeling awesome, bad for action."

Don't fool yourself. Pick the numbers you'd be willing to be held to. Make them small. Make them actionable. Make them yours.

---

Follow me: [@helmedeiros](https://twitter.com/helmedeiros)
