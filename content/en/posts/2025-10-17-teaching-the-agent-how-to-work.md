---
title: "Teaching the Agent How to Work: Claude Code, Skills, and Agentic Collaboration"
categories:
  - AI
  - Engineering
  - Software Architecture
date: 2025-10-17
tags:
  - ai
  - claude-code
  - agentic-workflows
  - clean-code
  - hexagonal-architecture
  - developer-experience
  - workflow-engineering
description: "Once your codebase is agent-ready, the next challenge is teaching the agent how to behave. Skills turn engineering discipline into executable protocols."
subtitle: "Architecture defines where logic belongs. Skills define how change unfolds."
---

In the previous article, I argued that agent productivity is not primarily a tooling problem. It is an architectural one.

If your repository is ambiguous, agents amplify ambiguity. If boundaries are porous, they replicate the wrong patterns. If validation is slow or inconsistent, iteration becomes expensive.

That article focused on structure.

This one focuses on behavior.

Because once your codebase is ready for agents, a new question appears: how do you teach the agent to behave like a disciplined engineer inside that structure?

To answer that, we need to talk about Claude Code and the idea of skills.

## What Claude Code actually is

Most developers are familiar with chat-based AI tools that generate code snippets. That interaction model is fundamentally conversational. You describe a problem, the model suggests a solution, and you manually apply it.

Claude Code operates differently.

It is an agent interface layered on top of a language model. Instead of only producing text, it can interact with your repository directly. It reads files, modifies them, executes shell commands, inspects test results, and iterates based on failures.

That difference matters.

You are no longer collaborating with a code suggestion engine. You are working with an autonomous loop that can:

1. Inspect the current state of your system.
2. Propose a change.
3. Validate that change by running commands.
4. Refine the change based on feedback.
5. Produce a structured diff.

This moves AI from assistance to participation. And once the system participates, workflow discipline is no longer optional.

## The hidden problem: behavioral drift

Back in March, when I started using Claude Code in real projects, something subtle happened.

Even in a well-structured repository, the agent's behavior varied from session to session.

Sometimes it made minimal, precise changes. Sometimes it over-touched files. Sometimes it placed logic correctly in the domain. Sometimes it slipped behavior into adapters because that was the shortest path to passing tests.

Nothing was catastrophically wrong. But the behavior was inconsistent.

And inconsistency is friction.

Human teams struggle with this too. Architectural intent decays over time. Conventions drift. Standards soften.

With agents, drift happens faster because they are pattern amplifiers. They do not "feel" that something is slightly off. They replicate what they see.

That is when I realized: architecture constrains _where_ changes happen. But something else must constrain _how_ changes happen.

## Skills as behavioral contracts

In the beggining of this month, Claude Code introduces the concept of [skills](https://code.claude.com/docs/en/skills).

A skill is not a feature request. It is not a prompt template. It is a reusable execution protocol that becomes part of the agent's operating context.

To understand this, it helps to think in terms of human collaboration.

Imagine onboarding a new senior engineer. You do not only give them access to the repository. You explain:

- How you approach changes.
- What order you prefer when modifying code.
- How you expect validation to happen.
- What "done" actually means.

A skill encodes that explanation once.

Instead of repeating behavioral instructions in every prompt, you define them structurally. From that point on, they shape how the agent executes tasks.

This shifts the interaction from conversational nudging to operational discipline.

## Why this is not prompt engineering

Prompt engineering focuses on phrasing. It attempts to guide output through better wording.

Skills focus on sequencing and constraint. They define the order of operations, validation gates, and architectural expectations.

When I had to repeatedly write something like:

> _Identify the use case first. Modify domain logic before adapters. Add tests. Run `make test` and `make lint`. Keep the diff small._

I was manually injecting discipline.

The moment I forgot to inject it, quality degraded.

That fragility does not scale.

Skills solve that by embedding discipline into the execution model itself.

## Designing skills with architectural awareness

Because my repositories follow hexagonal architecture, the skills I design reflect that structure.

Hexagonal architecture separates:

- **Domain logic** — pure, dependency-free.
- **Application coordination** — orchestrating use cases.
- **Ports** — interfaces defining boundaries.
- **Adapters** — infrastructure implementations.
- **Composition root** — where dependencies are wired.

This separation creates directional constraints: domain cannot depend on adapters.

Skills reinforce that constraint behaviorally.

> Instead of telling the agent _what_ to build, I tell it _how_ to move.

First locate the use case. Then modify domain logic. Then validate through unit tests. Only afterward update adapters. Only after validation finalize the diff.

This is operationalization of architectural intent.

## What a skill looks like in practice

Here is a simplified version of one of the skills I use:

```text
You are working in a repository that follows hexagonal architecture.

Execution protocol:

1. Identify the use case that owns the requested behavior.
2. Modify domain and application layers first.
3. Add or update unit tests covering the behavior.
4. Only then update adapters and wiring.
5. Run make test and make lint.
6. Ensure the diff is minimal and isolated.
7. Provide a summary grouped by architectural layer.
```

Notice that this does not describe a feature. It describes a workflow.

The workflow exists independently of the specific task. That independence is what makes it reusable.

## From personal habit to system constraint

In traditional development, engineering discipline lives in:

- Code reviews.
- Team agreements.
- Architectural documents.
- Institutional memory.

With agents, discipline must also live in executable form.

If discipline only lives in your head, the agent will not inherit it.

When I began publishing my skill set publicly in [clean-code-skills](https://github.com/helmedeiros/clean-code-skills), the intention was not to create something novel. It was to make my own habits explicit.

Minimal diffs. Domain-first changes. Validation before conclusion. Layered diff explanations.

These are not advanced ideas. They are consistent ones.

And consistency compounds.

## Agentic collaboration as a system

When repository structure and skills align, collaboration changes.

The interaction stops being reactive correction. It becomes intent plus protocol.

The agent reads the repository. The skill defines the sequence. CI enforces validation. The diff reflects architectural boundaries.

This is constrained autonomy.

Autonomy without constraint produces drift. Constraint without autonomy produces stagnation. What we want is disciplined iteration.

## Why this matters now

The industry conversation is still centered on models. Which model writes better code? Which one reasons better? Which one hallucinates less?

Those questions are valid, but incomplete.

Once agents can operate inside repositories, the limiting factor becomes workflow stability.

A strong model inside a chaotic workflow will produce chaotic iteration. A disciplined workflow amplifies even moderate capability.

> This is the shift from prompt engineering to workflow engineering.

Repositories encode structure. Skills encode behavior. CI encodes validation. The agent executes.

When those layers align, outcomes become repeatable.

## Closing reflection

An agent-friendly codebase makes safe change possible. Skills make disciplined change predictable.

If architecture defines where logic belongs, skills define how change unfolds.

The model did not become responsible.

We made responsibility executable.

{{< youtube CEvIs9y1uog >}}
