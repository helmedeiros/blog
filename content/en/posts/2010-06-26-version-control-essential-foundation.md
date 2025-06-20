---
title: "Version Control: Don't Code Without It"
date: 2010-06-26T09:00:00-03:00
tags:
  [
    "software engineering",
    "version control",
    "git",
    "svn",
    "collaboration",
    "development",
  ]
categories: ["Technology", "Agile"]
series: "Software Engineering Lectures"
slug: "version-control-essential-foundation"
summary: "In this lecture, we turned to a topic that every developer ignores at their own risk: version control. But we didn't just walk through Git commands—we explored the reasoning, pitfalls, and project-saving habits that come from disciplined usage. Version control isn't optional; it's foundational."
---

**Software Engineering Lectures - Part Part 17 of 19**

In this lecture, we turned to a topic that every developer ignores at their own risk: **version control**. But we didn't just walk through Git commands—we explored the reasoning, pitfalls, and project-saving habits that come from disciplined usage. Version control isn't optional; it's foundational. It protects you from yourself, your teammates, and time.

## The Problem Without Control

To demonstrate the chaos of unmanaged code, I started with a common scenario: two developers manually editing files and sending them via email or copying over a shared drive. Unsurprisingly, one overwrites the other, bugs emerge, and no one knows who broke what—or when.

Here's a literal example of "version control" without a tool:

```bash
cp index.html index.html.old
cp index.html index-backup.html
rm index.html
mv index-new.html index.html
```

That's not sustainable. It's an invitation for disaster.

## Centralized vs Distributed Systems

We explored two primary approaches: **centralized** (like SVN) and **distributed** (like Git). In centralized systems, there's one authoritative repo and everyone must sync to it. In distributed systems, each developer works independently and syncs changes later.

We wrote down basic commands from both:

### Centralized (SVN-like):

```bash
svn checkout http://example.com/project
svn commit -m "Added feature X"
svn update
```

### Distributed (Git):

```bash
git clone https://github.com/user/project.git
git commit -am "Added feature X"
git pull origin main
git push origin main
```

Students quickly saw the flexibility Git provides—offline commits, local branches, and peer-to-peer collaboration. It's no surprise it dominates modern workflows.

## Concepts That Matter

A key activity in class was mapping how Git supports critical engineering needs:

- **History**: Every change tracked.
- **Collaboration**: Merge branches without overwriting others.
- **Rollback**: Restore previous stable versions.
- **Exploration**: Branches for experimentation without risk.

We even generated SHA hashes to explain their uniqueness:

```bash
echo "test" | git hash-object --stdin
# returns: e9650474cb4169f840a1d6c057c44eac80d3e72c
```

A 40-digit hash replaces "version 3.2.1" with cryptographic certainty.

## Merge, Don't Panic

We simulated a team with conflicting changes. Then resolved the merge using:

```bash
git merge feature-x
# CONFLICT (content): Merge conflict in main.java
```

We walked through conflict resolution, commit finalization, and safe cleanup. It demystified what most beginners fear.

The lesson: a merge conflict isn't a failure—it's an opportunity to **synchronize intent** across teammates.

## Activities and Practice

We ended with a guided pair programming session. One student created a repo, the other forked it. They implemented a small feature, opened a pull request, and reviewed each other's work.

Facilitators can replicate this with any team or classroom. Start with a bug fix task, assign roles, and enforce collaboration through version control—not shared drives or messages.

This class made clear: version control is a communication tool. Not just with code, but with history, with teams, and with your future self.

---

_This post is **Part Part 17 of 19** in the series "Lectures on Software Engineering"_

**Previous:** [Advanced TDD: Thinking in Tests](/en/posts/2010-06-19-advanced-tdd-thinking-tests/) (Part 16)
**Next:** [The Classroom as a Learning Ground: Reflections from a Semester](/en/posts/2010-07-03-classroom-learning-reflections/) (Part 18)
