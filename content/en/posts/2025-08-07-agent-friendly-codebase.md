---
title: "It is time for Agent-Friendly Codebase"
categories:
  - AI
  - Engineering
  - Software Architecture
date: 2025-08-07
tags:
  - ai
  - software-architecture
  - refactoring
  - clean-code
  - hexagonal-architecture
  - testing
  - developer-experience
description: "Why repo structure, hexagonal architecture, and fast feedback loops matter more than clever prompts when working with AI coding agents."
subtitle: "Stop rewriting prompts. Start fixing your repository."
---

An "agent-friendly codebase" is not a codebase where an AI can write code. That part is already easy. The uncomfortable bit is whether an AI agent can do the job you actually want done: make a change that spans multiple files, run the right checks, interpret failures, iterate, and produce a diff that is small enough to review and safe enough to merge.

After building a handful of small projects and pushing agents through the same workflows over and over, I stopped thinking in terms of "AI coding ability" and started thinking in terms of "repo usability." The agent is another contributor. A fast one, yes. But also a contributor that can get lost easily, and that will happily amplify whatever ambiguity you leave lying around.

This post is what I wish someone had told me before I spent hours rewriting prompts instead of fixing the structure of the repository.

## The core idea: your repo is an interface

When I say "agent-friendly," I am not talking about AI-specific magic. I am talking about something close to classic developer experience, with a twist: a human can survive tribal knowledge, half-working scripts, and inconsistent conventions because humans can ask other humans, or "feel" their way through a messy system. Agents do not feel. They pattern-match and they follow instructions. If the instructions are implicit, outdated, or scattered, the agent will produce changes that look plausible but are wrong in the boring ways that cost you time.

An agent-friendly codebase is one where:

1. The agent can reliably discover where the change should happen.
2. The agent can change it without cascading side effects.
3. The agent can validate the change without you becoming the test runner.
4. The agent can explain what it changed in a way that a human reviewer can trust.

If any of those fail, what you get is not "AI acceleration." What you get is a new kind of toil: prompt fiddling, repeated context dumping, and manual verification.

## What I learned by brute-forcing agents through real workflows

### Legibility beats cleverness

The first trap I fell into was assuming the agent would "figure it out." It will, sometimes. But "sometimes" is not a strategy.

What worked best was aggressively reducing the number of plausible places where a change could live. In practice, this means being opinionated about structure and naming, even if it feels rigid. Agents are excellent at following a convention; they are mediocre at discovering one.

In a messy repo, the agent tends to do one of two things:

It finds a similar file, copies a pattern, and subtly diverges from the intended architecture.

Or it touches too many files because it can't tell what is core logic versus glue code.

Both failure modes produce diffs that look busy and "smart," but review badly and break unexpectedly.

### One golden path is worth ten README paragraphs

I used to believe documentation was the answer. It helps, but not in the way I thought.

Agents do not need more prose about the system. They need a small number of stable "golden path" commands and files that serve as the primary entrypoints for work. When those are missing, agents compensate by inventing workflows, and invented workflows are fragile.

What consistently reduced failures was a set of commands that always work on a clean machine, plus a short contract file that tells the agent which commands to run and which boundaries not to cross.

Here is the pattern I now default to in small projects:

```bash
make bootstrap
make test
make lint
make run
```

Under the hood, those can call whatever you want. The point is not Make. The point is that the repo has a predictable operating system for contributors, human or agent.

### "Works on my machine" becomes "works on my prompt"

Humans suffer from "works on my machine." Agents suffer from "works on my prompt."

If the only way to get the right change is to craft the perfect prompt with a paragraph of context, you are not building agent-friendly software. You are building a prompt-dependent system. That does not scale, even within one team, because prompts drift. People drift. Agents drift. Tooling drift is relentless.

The fix is boring: make the repo itself carry the context.

A good litmus test I now use is:

If I delete the chat history and re-run the task with a fresh agent, can the agent still succeed by reading only the repository?

When the answer is "yes," the repo is doing the work. When the answer is "no," I am doing the work.

### Hexagonal architecture is an agent multiplier

The most consistent architectural improvement I saw, across multiple projects, was moving toward a hexagonal design (ports and adapters). Not because it is fashionable, but because it constrains the search space of changes and makes validation cheaper.

A layered architecture can be clean. Many teams ship great software with it. The problem is that many layered architectures in the wild become "layered in name only." Boundaries blur. Domain logic leaks into controllers and persistence. Infrastructure concerns bleed upward. When an agent enters that environment, it does what a junior engineer would do: it follows the shortest path to "make it work," which often means placing logic in the wrong place because the repo does not enforce the intended separation.

Hexagonal architecture makes it harder to do the wrong thing by accident, and easier to tell where a change belongs.

### How agents behave in layered architectures

A typical layered architecture encourages a flow like:

Controller -> Service -> Repository -> Database

In theory, domain logic belongs in services. In practice, I often see services become orchestration plus random business rules, repositories become query plus mapping plus decision-making, and controllers accumulate "just this one special case" logic.

An agent asked to "add feature X" will usually: 1. Start at the controller because it is the entrypoint. 2. Look for a service method that looks similar. 3. If the shape doesn't match, add a new method in the service. 4. If the data isn't available, modify the repository or entity mapping. 5. Sprinkle validation in whichever layer is easiest.

That produces code that compiles and passes superficial tests, but it is hard to reason about because the rules for where logic belongs are not explicit in the codebase. Even if you have a convention, the agent has to infer it from examples. If your examples are inconsistent, you get inconsistent output.

The worst part is that layered architecture often encourages test strategies that are heavier than they need to be. If your domain rules are welded to persistence or web frameworks, verifying a change becomes integration-test-heavy. Agents can run integration tests, but they are slow and failures are noisier, so the iteration loop becomes expensive.

### How agents behave in hexagonal architectures

Hexagonal architecture changes the work surface.

Instead of asking "which layer should this go in," you ask "is this domain behavior, or is it an adapter concern?"

The design tends to look like:
- **Domain (pure):** entities, value objects, policies, use cases
- **Ports (interfaces):** what the domain needs from the outside world
- **Adapters (impure):** web handlers, persistence, messaging, external APIs

In a repo that actually follows hexagonal boundaries, an agent asked to "add feature X" tends to: 1. Find the use case or application service that represents the behavior. 2. Modify domain logic in a small set of files. 3. If new I/O is required, add it behind a port. 4. Implement the adapter separately (web, persistence, API client). 5. Update wiring in composition root.

That yields smaller diffs with clearer intent. More importantly, it makes it easier for an agent to validate changes locally because the domain core is testable without infrastructure.

This is the part that surprised me: hexagonal architecture does not just make the system "cleaner." It makes it easier to instruct an agent because you can tell it, in a single sentence, how to navigate the system.

For example:

"When you change business rules, change the domain and the use case first. Adapters should be thin."

Agents follow that. Layered systems can support the same discipline, but hexagonal structures make violations more visually obvious.

### The enforcement mechanism: compilation and test friction

The practical benefit of hexagonal is not the diagram. It is the friction.

If you structure the repo so that the domain package has no dependency on web frameworks, database libraries, or clients, the agent cannot accidentally import the wrong thing without your build complaining. That is agent-friendly. It turns architectural intent into guardrails.

In Go, for instance, I like a layout that makes it difficult to "reach across" boundaries:

```bash
/internal
  /domain
    money.go
    asset.go
    capitalization_policy.go
  /app
    classify_task.go
    process_sprint.go
    ports.go
  /adapters
    /jira
      client.go
    /persistence
      sqlite_repo.go
    /cli
      commands.go
/cmd/assetcap
  main.go
```

A layered layout can look similar, but the crucial difference is that the domain and app layers should not import adapters. The composition root (often cmd/.../main.go) should wire everything.

When this is true, agents become dramatically easier to supervise. You are no longer reviewing whether the agent placed logic in the "right layer" based on taste. You are reviewing whether it respected a constraint that the system enforces.

### A small example: "classification rules" in layered vs hexagonal

Let's say I am building assetcap and I want to classify Jira issues into capitalizable vs non-capitalizable based on labels and issue type, and I want to tweak the rules.

In a layered architecture, the agent might implement the logic inside the Jira client adapter or inside the persistence layer because that is where the data is shaped. The code will work, but now classification is coupled to Jira.

In hexagonal, classification is a domain policy. The Jira adapter maps Jira issues into a domain representation, and the policy decides.

That leads to the kind of tests agents are good at writing and maintaining:

```go
func TestClassificationPolicy(t *testing.T) {
  policy := NewClassificationPolicy()

  issue := Issue{
    Type:  "Story",
    Labels: []string{"platform", "capex"},
  }

  got := policy.Classify(issue)
  if got != Capitalizable {
    t.Fatalf("expected Capitalizable, got %v", got)
  }
}
```

This test runs in milliseconds, with no Jira client, no mocks of HTTP, no database. That short loop is a force multiplier for agents because they can iterate quickly and get crisp failure signals.

Layered architecture can get you there too, but in practice, teams often do not keep domain rules isolated. Hexagonal makes isolation the default posture.

### The "agent contract" file became non-negotiable

Once I stopped treating agent success as a prompt problem and started treating it as a repo problem, one artifact kept paying off: a short file that says how work gets done here.

I have seen variants like AGENTS.md, CONTRIBUTING.md, and tool-specific rules files. The name matters less than the discipline: it must be short, accurate, and enforced by CI expectations.

Here is the minimal template I ended up with. This is not a manifesto. It is a contract.

```md
# Agent Contract

## Intent

This repo follows hexagonal architecture.
Domain and application layers must not depend on adapters.

## Golden commands

- make bootstrap
- make test
- make lint
- make run

## Change rules

- Business rules live in /internal/domain and /internal/app.
- Adapters in /internal/adapters must stay thin.
- Do not introduce new patterns without updating docs/architecture.md.

## Tests

- Domain changes require unit tests in /internal/domain.
- Use-case changes require tests in /internal/app.
- Adapter changes require integration tests only when necessary.

## Forbidden

- Do not commit secrets.
- Do not modify production infrastructure without explicit instruction.
```

I used to worry this was redundant. It is not. It is the difference between "agent as collaborator" and "agent as chaos engine."

### The hidden requirement: you need fast, trustworthy feedback loops

Agent-friendly repos are not just about structure. They are about making verification cheap.

A repo is hostile to agents when:
- tests are slow and flaky
- lint and formatting are inconsistent
- local setup is fragile
- CI does things that local scripts do not

In those conditions, the agent becomes a change generator, not a contributor. It will produce code, but you will be stuck validating and repairing.

The fastest improvement I made in my own projects was aligning local commands with CI. I stopped treating CI as a separate universe. If CI runs ./gradlew check, my local command runs ./gradlew check. If CI runs go test ./..., my local command runs go test ./.... If CI requires a database container, the local workflow should spin up the same container with one command.

This is not glamorous work. It is the work that makes everything else possible.

### Where layered architectures still win, and how to keep them agent-friendly

I am not claiming hexagonal is the only answer. Layered architectures can be perfectly agent-friendly if you do two things with discipline:

First, you make boundaries enforceable. If your "service" layer is allowed to import repositories directly, and repositories are allowed to call external services, you do not have a layered architecture; you have a dependency soup. Agents will swim in it and bring back whatever they catch.

Second, you make your domain testable without infrastructure. If domain behavior requires spinning up a database, your agent loop is going to be expensive and noisy. You can still succeed, but you will spend more time.

A layered architecture that behaves well with agents tends to look more like "hexagonal in practice" anyway: domain rules isolated, adapters thin, wiring at the edges.

At that point, the debate becomes mostly about naming and packaging, not about capability.

### A pragmatic definition

After repeating these experiments, I now define an agent-friendly codebase like this:

A codebase is agent-friendly when it gives an AI agent enough structure and feedback to make correct changes without constant human interpretation.

Structure means:
- clear boundaries where logic belongs
- minimal valid entrypoints for changes
- a small number of standard commands

Feedback means:
- fast tests for domain behavior
- predictable lint and type checks
- CI parity with local runs

Hexagonal architecture helps because it turns "where should this logic go?" into a constraint rather than a debate, and constraints are exactly what agents need.

### Prompts I keep reusing

When I want an agent to work well in a hexagonal repo, I use prompts that are more like process instructions than feature requests. I do not ask it to be clever. I ask it to respect the contract.

Here is one I reuse:

```
You are working in a repo that follows hexagonal architecture.
Make the smallest diff possible.

Steps:
1) Identify the use case that owns this behavior.
2) Implement domain/app changes first, with unit tests.
3) Only then update adapters and wiring.
4) Run the golden commands: make test, make lint.
5) Summarize the diff and explain why each change belongs in its layer.
```

In layered repos, I add one extra sentence:

```
Do not add business rules in controllers or repositories. Keep them in the service/domain layer and add unit tests.
```

The prompt helps, but the repo still has to deserve the agent.

### Closing thought

The temptation is to treat agent productivity as a tooling story. It is not. Tooling matters, but the repo decides whether your workflow is stable.

Once I started optimizing the codebase for agent comprehension and verification, the "AI productivity boost" stopped being a demo trick and became a repeatable outcome.

Not because the agent got smarter.

Because the codebase stopped being vague.
