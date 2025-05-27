---
title: "Build Frameworks, Don't Take Hostages"
date: 2015-09-24T14:00:00-03:00
author: Helio Medeiros
subtitle: "Presented at TDC Porto Alegre — September 24, 2015, as part of the Architecture Track"
tags:
  [
    "frameworks",
    "architecture",
    "software design",
    "development",
    "tdc",
    "frameworkitis",
  ]
categories: ["Technology", "Architecture"]
---

## What This Talk Was Really About

This wasn't a talk against frameworks. It was a wake-up call.

Over the past decade, we've seen an explosion of frameworks across every language ecosystem. But with this explosion came a dangerous side effect: developers stopped asking why, and started following how. Frameworks became dogma. And worse, they became prisons.

I called this disease **Frameworkitis**.

This talk was about how we got here, what we've misunderstood, and what we need to do to create tools that support teams — not trap them.

## What Frameworks Were Supposed to Be

When Erich Gamma and the Gang of Four introduced design patterns, the idea was simple: encourage reuse, reduce duplication, and build systems from proven building blocks. Frameworks emerged from that mindset. They were supposed to **abstract repetitive problems** so we could focus on what really mattered.

But somewhere along the way, we stopped treating frameworks as tools. We started treating them as the foundation, the architecture, the system itself.

And with that, we forgot the first principle of good software: **you build for your problem**, not around someone else's abstraction.

## How to Evaluate a Framework (Instead of Just Adopting It)

Too often, we pick frameworks by trend, not fit. But choosing a framework is a strategic decision. It shapes your team's learning curve, your codebase, your flexibility.

So what should we actually look for?

First, adaptability. A good framework bends to your problem. A bad one forces you to rewrite your problem to fit its shape.

Second, simplicity. If it takes three files, two decorators, and a lifecycle diagram to explain one endpoint, that's not power — that's complexity.

Third, architectural values. Is the code following SOLID principles? Are there signs of inversion of control? If not, you're probably dealing with tightly coupled glue and magic rather than maintainable design.

Finally, community. Because let's be honest: you're not just buying into code, you're joining a tribe. A framework with an active, honest, and experimental community will outlive better-designed but isolated alternatives.

## The Ecosystem Shapes the Framework

Frameworks don't appear in a vacuum. They are cultural artifacts.

Java frameworks often mirror enterprise rigor. JavaScript ones lean toward experimentation and rapid iteration. Ruby brought elegance and DSL fluency. Python emphasized readability and science.

The maturity, philosophy, and pain points of a language's community will define what kind of frameworks it produces. So don't just evaluate the framework. Evaluate the **DNA of its origin**.

## The World Changed. Our Tools Didn't Keep Up.

From 2013 to 2015, the scale of digital systems changed drastically. We got more users, more devices, more data, more concurrency, more edge cases.

Yet most frameworks kept selling the same promises with the same abstractions. Few adapted to the new reality. And honestly? Most of us didn't have time to stop and rethink. Business kept pushing. Releases didn't wait.

So we patched. We hacked. We stacked abstractions on abstractions. And we started seeing more and more codebases where developers were **using tools they didn't understand to solve problems they couldn't name**.

## When You're Using a Framework, Stay Awake

It's tempting to just "pick the full-stack one" and move on. But every time you do that, ask:

- Does this framework let me describe _what_ I want to solve, or does it force me to define _how_?
- Am I using a modular ecosystem where I can compose what I need, or am I locked into an all-or-nothing monolith?
- Is the framework evolving in the direction I need, or will I be building workarounds in six months?

The goal isn't to avoid frameworks. The goal is to use them **with clarity and intent**.

## When You're Creating One, Be Careful

Now flip the script.

If you're designing or extending a framework, you're responsible for someone else's future. That's a big deal.

Don't assume you know all their use cases. Build for your core first. If someone wants to add more features, make sure they can — **without hacking into the internals**.

Don't force coupling where none is needed. Let developers plug in, override, or walk away.

And above all, write code people can read. Cleverness ages poorly. Clarity lasts.

## So... Is There a Cure for Frameworkitis?

Yes. But it's not easy. And it doesn't come in a box.

The first step is **remembering that frameworks are just tools**. They are not languages. They are not architectures. They are helpers. Treat them like that.

Prefer libraries and toolkits that let you assemble solutions over monolithic frameworks that try to own your stack.

Be skeptical. Read the source. Try the tool. Break it. Understand what happens. Never go into production with something just because "everyone's using it."

And finally, if all else fails: **delete the magic**. Magic is great until it breaks — then it becomes a trap. Transparency over cleverness, every time.

## Final Thought

You can build amazing frameworks. You can even use some fantastic ones. But do it with purpose. Do it with awareness. And never forget:

**A good framework supports your team. A bad one takes them hostage.**

_Originally presented at TDC Porto Alegre — September 24, 2015, as part of the Architecture Track._
Follow me: [@helmedeiros](https://twitter.com/helmedeiros)
