---
title: "Feature Injection: Discovering and Delivering Testable Value"
date: 2014-11-10T14:00:00-03:00
author: Helio Medeiros
subtitle: Stop letting features pull you into building first and learning later—hunt the value, inject it into your work, and detail it by example so every story you ship is testable from the start
tags:
  [
    "feature injection",
    "BDD",
    "hypotheses",
    "product discovery",
    "agile",
    "lean",
  ]
categories: ["Events", "Agile"]
---

## What This Talk Was About

<iframe class="speakerdeck-iframe" frameborder="0" src="https://speakerdeck.com/player/73e2ed004b390132413f0a4dd3cf94f0" title="Feature Injection - discovering and delivering testable value" allowfullscreen="true" allow="web-share" style="border: 0px; background: padding-box padding-box rgba(0, 0, 0, 0.1); margin: 0px; padding: 0px; border-radius: 6px; box-shadow: rgba(0, 0, 0, 0.2) 0px 5px 40px; width: 100%; height: auto; aspect-ratio: 560 / 315;" spellcheck="false" data-ratio="1.7777777777777777"></iframe>

For most of my career I'd seen teams build features first and ask about value later. We'd take a backlog, slice it by layer, estimate it, and ship it. Somewhere between the kickoff and the release we'd stop asking the question we should've been asking the entire time: _who is this for, what behavior are we trying to change, and how will we know if it worked?_

This talk was about flipping that habit. The technique has a name — **Feature Injection** — and it comes from Chris Matts. The shape is simple: don't start from features and hope value shows up. Start from value, inject it into the work, and let the features fall out by example.

## Hunt the Value

Before any user story, before any acceptance criterion, there's a business outcome someone is trying to move. Hunting the value means making that outcome explicit: a number that should go up or down, a behavior we expect a real user to do, a problem we believe is worth solving.

If you can't name the outcome, you're not hunting yet. You're just listing features.

I asked teams to write the outcome before they wrote the story. Almost every time, the act of writing the outcome killed two or three "obvious" features that had no business being on the board.

## Inject the Value

Once the outcome is named, work flows backwards into it. You ask: what does the system need to do so this outcome can happen? That answer is the feature. The feature exists **because of the value**, not the other way around.

This is where Feature Injection separates itself from layered backlogs. You're not picking work because it's the next sliced ticket. You're picking work because, without it, the value can't land.

Stories written this way come pre-loaded with two things normal stories miss: a stakeholder who actually cares about the outcome, and a way to measure whether the outcome moved.

## Detail by Example

The last step is the one most teams skip. Once you have a feature that ties to a value, you describe how it behaves through **concrete examples** — the same shape BDD has been preaching for years.

```text
Given a reader has saved an article
When the reader returns the next day
Then the saved article appears at the top of their feed
```

Examples like this do three jobs at once: they specify the behavior, they become the acceptance test, and they become the conversation starter with product and QA before a line of code gets written.

When you detail by example, "done" stops being a vibe and starts being a checklist anyone can verify.

## Assumptions Are Hypotheses

Every story I write today carries an unstated belief: that the user will care, that the metric will move, that the behavior we expect is the behavior we'll see. Feature Injection asks you to write that belief down on purpose.

A story becomes a hypothesis. A release becomes an experiment. A metric becomes feedback, not vanity.

This is how you earn the right to say "we're learning" instead of "we're shipping."

## Fail Fast, Succeed Faster

The point of all this isn't process for its own sake. It's tightening the loop between idea and evidence.

When the value is named, the feature is small, the example is concrete, and the metric is measurable, you find out you're wrong in days instead of quarters. Being wrong fast is the prize. Being wrong slowly is what kills product teams.

## Closing Thought

Feature Injection isn't a methodology you adopt — it's a habit you build. Hunt before you build. Inject value into the work. Detail it by example. Let the metric tell you whether you were right.

The teams I've seen do this well don't end up with bigger backlogs. They end up with shorter ones, and with the confidence that what's still on the board is worth the time.

---

_Talk material from late 2014, sharpened from work at ThoughtWorks Brasil and conversations across the Brazilian agile community._
Follow me: [@helmedeiros](https://twitter.com/helmedeiros)
