---
title: "Swarming the Codebase: Orchestrated Execution with Multiple Claude Code Agents"
categories:
  - AI
  - Engineering
  - Software Architecture
date: 2025-11-23
tags:
  - ai
  - claude-code
  - agentic-workflows
  - git
  - git-worktree
  - swarming
  - developer-experience
description: "When one agent is not enough, swarming with git worktree turns parallel AI execution from chaos into structured collaboration. Isolation is the primitive. Git is the orchestrator."
subtitle: "Parallel agents without isolation is not acceleration. It is entropy."
---

I had three features to ship. Each one was well-scoped: a new domain policy, a validation rule, and an adapter for an external API. The codebase was clean. The skills were loaded. The agent contract was in place.

So I did what felt natural. I opened three terminal panes, started Claude Code in each one, and pointed them at the same repository.

Within minutes, two agents edited the same file. One overwrote the other's changes. The third agent ran tests that failed because the working directory was in a state neither of them expected.

That was the moment I understood: the bottleneck was no longer about teaching one agent how to work. It was about teaching multiple agents how to coexist.

## Where this fits in the series

In the [first article]({{< ref "2025-08-07-agent-friendly-codebase" >}}), I argued that an agent-friendly codebase reduces ambiguity about _where_ changes belong. Hexagonal architecture, golden commands, fast feedback loops.

In the [second]({{< ref "2025-10-17-teaching-the-agent-how-to-work" >}}), I explored how skills encode _how_ changes unfold. Execution protocols, validation gates, layered diff summaries.

In the [third]({{< ref "2025-10-30-interactive-planning-specification-boundaries" >}}), I addressed _what_ should be built through Plan Mode and interactive questioning.

This article addresses the next challenge: **how do you scale execution when one agent is not enough?**

| Layer         | Question it answers                          | Mechanism                                                  |
| ------------- | -------------------------------------------- | ---------------------------------------------------------- |
| Structure     | Where does the change belong?                | Architecture, boundaries, golden commands                  |
| Behavior      | How should the change unfold?                | Skills, execution protocols, validation                    |
| Intent        | What exactly should be built?                | Plan Mode, interactive questioning                         |
| **Execution** | **How do multiple agents work in parallel?** | **Git worktree, branch isolation, controlled integration** |

Each layer solved a different class of problems. But none of them addressed concurrency. And concurrency is where the next friction hides.

## What swarming means in practice

In traditional software teams, swarming refers to multiple engineers collaborating on the same problem simultaneously. Everyone converges, communicates, and integrates in real time.

In agentic systems, swarming means orchestrating multiple AI agents to work in parallel on the same repository, with controlled boundaries and coordinated integration.

This is not about chaos. It is about **structured parallelism**.

The distinction matters. Throwing more agents at a problem without isolation does not produce more output. It produces more conflicts, more broken state, and more time spent untangling what went wrong.

> Swarming is not about more agents. It is about more agents with boundaries.

## Running multiple Claude Code instances

Claude Code runs in the terminal. That makes parallelism mechanically simple.

Using tmux, I create a session and split it into panes:

```bash
tmux new-session -s swarm
```

Each pane gets its own Claude instance:

```bash
claude
```

Three panes, three agents, three concurrent streams of work. The setup takes seconds.

But here is the problem: all three agents share the same working directory. They read the same files. They write to the same files. They run tests against the same state.

That is not parallelism. That is a race condition.

## Git worktree as the isolation primitive

The solution is deceptively simple. `git worktree` allows multiple working directories attached to the same repository, each tracking a different branch.

```bash
git worktree add ../feature-policy feature/policy
git worktree add ../feature-validation feature/validation
git worktree add ../feature-adapter feature/adapter
```

Now each Claude instance operates in its own directory, on its own branch, with its own file state. No agent can accidentally overwrite another agent's work.

| Without worktree                   | With worktree                         |
| ---------------------------------- | ------------------------------------- |
| Agents share one working directory | Each agent gets an isolated directory |
| File writes conflict silently      | File writes are branch-scoped         |
| Test runs reflect mixed state      | Test runs reflect single-branch state |
| Integration is accidental          | Integration is deliberate             |

The mental model is straightforward: each worktree is a sandbox. Each sandbox has its own branch. The agents never touch each other's sandboxes.

What surprised me was how natural this felt. It mirrors how experienced engineers work on a team: everyone has their own branch, their own local state, and integration happens through pull requests, not through shared mutation.

## Git as the orchestrator

Once each agent operates in an isolated worktree, Git stops being just version control. It becomes the orchestration layer.

Git serves four roles simultaneously:

- **Isolation mechanism** — worktrees keep agents separated.
- **Integration boundary** — merges happen deliberately, not accidentally.
- **Conflict detector** — when two agents touch overlapping concerns, Git surfaces the conflict at merge time, not at edit time.
- **Rollback mechanism** — if an agent produces a bad result, discarding a branch is trivial.

This is not a new workflow. It is the same branch-based collaboration that human teams have used for years. The difference is that the "team members" are AI agents executing in parallel, and the cycle time is minutes instead of days.

> Git does not care whether the committer is a human or an agent. That is exactly what makes it the right orchestration primitive.

## The workflow in practice

Here is how a typical swarming session looks for me now:

```text
1. Decompose the task into independent work units
2. Create a worktree and branch for each unit
3. Start a Claude instance in each worktree
4. Let agents execute in parallel
5. Review each branch independently
6. Merge branches into main through pull requests
```

The decomposition step is critical. Swarming only works when the work units are genuinely independent. If two agents need to modify the same file or the same domain entity, the merge will be painful regardless of isolation.

In a hexagonal architecture, independence maps naturally to architectural boundaries:

| Work unit            | Architectural layer | Why it is independent                 |
| -------------------- | ------------------- | ------------------------------------- |
| New domain policy    | Domain              | Pure logic, no adapter dependencies   |
| Validation rule      | Application         | Uses existing ports, no new adapters  |
| External API adapter | Adapter             | Implements an existing port interface |

When the architecture supports clean separation, swarming becomes a natural extension of the design.

## Discipline is non-negotiable

Parallel agents amplify drift if structure is weak.

Without clear architectural boundaries, agents wander. Without small commits, reviewing each branch becomes expensive. Without deterministic tests, you cannot trust that a passing test in one worktree means the change is correct. Without CI parity, local success becomes a false signal.

The prerequisites are the same ones from every article in this series:

- Clear architectural boundaries
- Small, focused commits
- Deterministic tests
- CI parity with local commands

Swarming does not relax these requirements. It makes them more urgent. A single undisciplined agent produces one mess. Three undisciplined agents produce three messes that conflict with each other.

> Swarming collapses into entropy the moment constraints stop being respected.

## What swarming is not

It is tempting to see swarming as a way to "throw more compute at the problem." That framing misses the point.

Swarming is not about speed at any cost. It is about **safe parallelism**. The goal is not to produce more code faster. The goal is to produce more _correct_ code concurrently, with each stream of work independently verifiable.

If the decomposition is wrong, swarming makes things worse. If the architecture does not support clean boundaries, swarming exposes every seam. If the agents lack skills and contracts, swarming multiplies behavioral drift.

This is not a shortcut. It is an amplifier. And amplifiers are only as good as the signal they receive.

## Looking ahead

This is still primitive orchestration. Each agent operates independently, with no awareness of what the others are doing. The decomposition is manual. The coordination is Git-mediated. The review is branch-by-branch.

The next step is specialization: I read that Anthropic released sub-agents, and that looks interesting way to handle specific concerns within a larger task, coordinated by a primary agent that understands the full scope. Not just parallel execution, but hierarchical execution.

But that is a different time to learn and article to write.

For now, the lesson is this: the same principles that make a codebase agent-friendly for one agent — structure, skills, intent clarity — are exactly what make it possible for multiple agents to work in parallel without destroying each other's progress.

Swarming is not about more agents.

It is about structured parallelism. And structured parallelism starts with isolation.
