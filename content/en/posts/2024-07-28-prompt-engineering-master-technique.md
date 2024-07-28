---
title: "Eighteen Days Later: Prompt Engineering & the MASTER Technique"
categories:
  - AI
  - Productivity
  - Engineering Management
date: 2024-07-28
tags:
  - prompt-engineering
  - ai-literacy
  - master-technique
  - genai
  - productivity
  - llm
description: "A deep dive into structured prompt engineering using the MASTER technique - moving from asking questions to designing conversations with AI."
subtitle: "Time flies when you're learning something cool - discovering how prompt engineering is design thinking, not magic, through the MASTER framework."
---

# Eighteen Days Later: Prompt Engineering & the MASTER Technique

## Time flies when you're learning something cool

It's been 18 days since I started this journey, and I have to say—time _really_ flies when you're learning something that feels both powerful and limitless.

The more I explore, the more impressed I am by the sheer volume and quality of available content—whether you're a beginner, a developer, or a team lead. Resources come in all forms: books, blog posts, courses, and tons of brilliant YouTube creators. And the best part? They approach the topic with depth at every level.

I've been reading Ethan Mollick's _Co-Intelligence_, a book that doesn't just tell you how AI works—it shows you how to work _with_ it. It's filled with practical ideas, critical reflections, and calls to action for knowledge workers.

For videos, I started with **Jeff Su**, who makes GenAI productivity simple and approachable. Then moved to **IBM Technology** for a systems-level understanding of LLMs, before getting deeper into tool usage with **Dave Ebbelaar** and **Thu Vu**, who cover prompts, agents, and model internals with clarity and substance.

## What I've learned: Prompting isn't magic—it's design

The biggest eye-opener? **Prompt engineering is not just about wording—it's about design thinking.** It's about structure, iteration, and intent. And that's where the **MASTER technique** has really clicked for me.

Let's break it down.

## The MASTER Technique

MASTER is a prompting framework that helps you make the most of your interaction with AI:

| Letter | Meaning                 | Why It Matters                         |
| ------ | ----------------------- | -------------------------------------- |
| M      | **Markdown**            | Structure your request clearly         |
| A      | **Act (Assign a Role)** | Gives the AI context and tone          |
| S      | **Specific**            | Reduces ambiguity, increases relevance |
| T      | **Threads**             | Keeps prompts focused and organized    |
| E      | **Examples**            | Shows the AI what good looks like      |
| R      | **Regenerate & Refine** | Reminds us AI is iterative, not final  |

## Why MASTER works

AI isn't a deterministic engine—it's a probability machine. Without structure, it makes assumptions that often don't match your goals. With **MASTER**, you shift the prompting from "asking a question" to "designing a conversation."

Let's say I want AI to help me create a user story:

```
## Role:
You are a senior product manager with expertise in agile development and user story writing.

## Task:
Write a user story for adding a notification system to our project management tool.

## Context:
- User: Development team members
- Goal: Stay updated on task assignments and status changes
- Format: Standard "As a... I want... So that..." structure
- Include acceptance criteria

## Example:
"As a development team member, I want to receive real-time notifications when tasks are assigned to me or when their status changes, so that I can respond quickly and stay aligned with project priorities.

Acceptance Criteria:
- Notifications appear within 5 seconds of the triggering event
- Users can customize notification preferences (email, in-app, Slack)
- Notifications include task title, project name, and direct link to the task"
```

The difference from a plain "Write me a user story for notifications"? Night and day.

## R is for Regenerate—and Reflect

Even with MASTER, **your first output won't be your best**. That's where the **R** comes in. Regenerating isn't just retrying—it's reflecting.

Ask yourself:

- Did the tone match my audience?
- Were the examples too generic?
- Did I give enough context?
- Should I add constraints or expectations?

It's a design loop: prompt → review → refine.

## Connecting the dots

When I link this technique to the things I'm reading and watching, I notice a pattern: **every expert treats AI not as an oracle, but as a collaborator.**

That's the vibe of _Co-Intelligence_. It's not about letting AI drive—it's about making it part of your team.

Jeff Su teaches you to automate without abdicating. IBM Tech explains the "why" behind the output. Dave Ebbelaar and Thu Vu show you how to combine reasoning, chaining, and tools like agents to _go further_—but always with intent.

## Takeaway for managers, devs, and teams

If you're just starting in GenAI, don't worry about getting every prompt right. Focus on **clarity, structure, and iteration**.

Try MASTER for your next:

- Jira story description
- Performance review draft
- Strategic document
- Data analysis prompt
- Email response

And don't forget: prompting is a skill. It gets better the more you do it—and it gets _deeper_ when you start treating AI not like a tool, but like a co-worker.

More soon.
