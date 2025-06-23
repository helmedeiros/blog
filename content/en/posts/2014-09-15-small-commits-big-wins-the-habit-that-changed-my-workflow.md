---
title: "Small Commits, Big Wins: The Habit That Changed My Workflow"
date: 2014-09-15T10:00:00-03:00
author: Helio Medeiros
subtitle: Transform your Git workflow from chaotic to purposeful—discover how small, meaningful commits improve code quality, collaboration, and debugging efficiency
tags: ["git", "workflow", "productivity", "software-development"]
categories: ["Development"]
---

## Why I Changed the Way I Commit

When I first started using Git, I treated it like a backup system. I would code for hours, then dump everything into a single commit: "WIP", "fix stuff", or worse—no message at all. I wasn't thinking in units of change. I was thinking in terms of time passed. Git wasn't helping me collaborate or understand my code; it was just a place to park it.

That began to change when I joined a project with stricter review practices. My massive commits were hard to understand, and reviewers struggled to follow what I had done. I was forced to slow down and think: what exactly did I change here, and why?

It turned out that making small, meaningful commits wasn't just a favor to my reviewers—it made me a better developer. I could track bugs faster, revert risky changes more safely, and reason about my code with more clarity.

Git went from being a passive tool to an active part of my development practice. Every commit became a design decision.

Let's explore the shift in mindset and the concrete habits that followed.

## Commits as Communication

A commit is not just a record of change—it's a message to your future self and to your team. When commits are small and well-scoped, they tell a story. That story can be read, reviewed, and even rewritten with intention.

```bash
git add src/module.js
git commit -m "Add input validation for empty fields"
```

Compare that to:

```bash
git commit -am "big update"
```

The first example is precise. The second is noise. And noise adds friction.

| Commit Style          | Clarity Level | Revert Safety | Review Difficulty |
| --------------------- | ------------- | ------------- | ----------------- |
| Small, scoped commits | High          | Easy          | Low               |
| Large, vague commits  | Low           | Risky         | High              |

Once I saw commits as a tool for communication, everything changed. I began to split changes into logical units—one bug fix, one refactor, one feature tweak per commit. It took discipline, but it paid off.

Reviewers gave more focused feedback. I made fewer mistakes. And when something went wrong, I could pinpoint it quickly by bisecting commits.

## Building the Habit

Changing how I committed code wasn't easy. It required a change in pace and mindset. At first, I had to remind myself to pause. To reflect on what I had changed. To think before I typed `git commit`.

I started by pairing `git diff` with `git add -p`:

```bash
git diff
git add -p
```

This gave me visibility into my changes and allowed me to stage only what mattered. Instead of thinking, "Is my task done?" I started thinking, "What unit of value have I finished?"

| Practice             | Benefit                     |
| -------------------- | --------------------------- |
| `git add -p`         | Stage changes interactively |
| Frequent commits     | Easier rollback and review  |
| Scoped commit titles | Improves team understanding |

I also began writing my commit messages like small headlines. Action + intent. For example: `Refactor user service to reduce duplication`.

Over time, it became muscle memory. I didn't have to think as hard—I just worked in small, clean increments.

That habit made me faster, not slower. Because debugging and reviewing became almost effortless.

## The Discipline That Pays Off

Many developers resist small commits because they feel like overhead. But the truth is, the time saved later—during reviews, bug hunts, or blame investigations—makes up for the effort tenfold.

Small commits encourage focus. They force you to break down work into manageable chunks. They align with how we _should_ think about software: as a series of small, thoughtful changes that build toward something larger.

So next time you're tempted to lump everything into one commit, pause. Ask yourself: What am I trying to say with this change? Who will read it later?

Write your history like someone will depend on it. Because one day, they will. And that person might be you.
