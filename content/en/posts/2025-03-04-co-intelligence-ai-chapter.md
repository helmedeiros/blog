---
title: "Co-Intelligence: Living, Working, and Rubber Ducking with AI"
categories:
  - AI
  - Productivity
  - Engineering Management
date: 2025-03-04
tags:
  - ai
  - co-intelligence
  - productivity
  - engineering-practices
  - rubber-ducking
  - workflow
  - automation
  - collaboration
---

On March 4, 2025, I delivered a keynote at the Omio Engineering AI Chapter about something I had been exploring—not just intellectually but through daily practice. The talk was titled **"Co-Intelligence: Living, Working, and Rubber Ducking with AI"** and was not about predicting the far future of artificial general intelligence or automating away jobs. Instead, I focused on what's already changing in how I code, debug, learn, and make decisions—when AI isn't just a tool, but a consistent thinking partner.

We're at a strange moment in engineering. Every week brings new capabilities from copilots and assistants, but most teams still treat them as sidekicks, not collaborators. This talk was my attempt to challenge that mindset.

Here are the full slides from the keynote:

<iframe class="speakerdeck-iframe" frameborder="0" src="https://speakerdeck.com/player/39ec661d8d5e44d39aac7dda2af62f90" title="Co-Intelligence-Living-Working-and-Rubber-Ducking-with-AI" allowfullscreen="true" style="border: 0px; background: padding-box padding-box rgba(0, 0, 0, 0.1); margin: 0px; padding: 0px; border-radius: 6px; box-shadow: rgba(0, 0, 0, 0.2) 0px 5px 40px; width: 100%; height: auto; aspect-ratio: 560 / 315;" data-ratio="1.7777777777777777"></iframe>

## Rubber Ducking Reimagined

If you've ever talked to a rubber duck to debug code, you already understand half of the idea. The duck doesn't solve anything—it forces you to slow down, explain clearly, and catch what you were missing. Now imagine the duck responds, questions your assumptions, and sometimes finds bugs you didn't even know existed.

That's how I see co-intelligence in practice. Explaining your plan, refactoring idea, or vague error to an LLM creates a conversation loop that makes your thinking sharper. It's not about automation. It's about **augmentation**.

In one example I shared during the talk, we went from a vague Jira ticket title to a concrete list of edge cases and implementation notes—just by asking GPT to act like a senior engineer doing a kickoff. Another session showed how a test that flaked intermittently became stable again after the AI simulated multiple failure paths and helped us hypothesize the root cause.

In another case, we used GPT to walk through a chaotic postmortem log and reframe it as a sequence of causal questions: _"What changed in the last deploy?"_, _"What was different in prod vs staging?"_ It wasn't just summarizing — it was helping us ask better follow-up questions. The kind a calm SRE would ask on-call at 3am. We're not there yet, but it's not far-fetched to imagine AI owning part of the on-call assistant role: parsing logs, connecting alerts to known issues, or even proposing playbook steps before we do.

## When the Tools Change, the Process Must Follow

If the way we work hasn't changed in the last year, it's not because AI hasn't improved. It's because we haven't let it change us.

I argued that the invisible friction of daily engineering work—clarifying stories, debugging flaky systems, onboarding onto messy stacks—can be drastically reduced when AI is part of your flow. But that requires more than installing a plugin.

It demands a rethinking of team rituals. Do we still need traditional refinement meetings if engineers are pre-refining with GPT before standups? What's the role of a senior mentor when a junior developer can simulate a pair programming session with Claude or ChatGPT? How do we ensure code quality and traceability when some commits are co-authored by an assistant?

None of these are solved problems, but pretending they don't exist creates tech debt in the way we lead teams.

## The Human Remains in Charge—But Not Alone

One of the most resonant parts of the talk was the walk-through of a co-designed internal tool. Starting from a blank prompt, we asked an LLM to first simulate a product manager and define the user's pain point. Then it shifted into a designer's voice and described three layout options. From there, we generated an API stub and acceptance criteria. Finally, we role-played a QA engineer probing the app's limits.

Each persona was a shallow mimic, but together they formed a **fast, cross-functional loop** that we used to get feedback before a single commit.

This process didn't eliminate collaboration with real humans—it made it faster to reach the first draft worth discussing.

One learning we keep bumping into is this: the real power of these tools comes when you stop treating them like answer engines and start using them as structure engines. At first, I wrote prompts that begged for "just the right code." But what worked better was asking, _"Can you help me frame this?"_ or _"What questions am I not asking yet?"_ Prompting, it turns out, isn't just technical — it's reflective. The best engineers I've seen working with AI treat it like a whiteboard session, not a vending machine.

## A Culture Shift Is Already Underway

At Omio, we're gradually shifting our engineering culture to reflect this. Engineers are encouraged to experiment with prompt workflows for planning, testing, and documentation. We've created dedicated Slack channels to share best prompts. We're also tracking where AI saves us time—and where it creates ambiguity.

The early results are promising. We've seen onboarding times drop. We've seen more thoughtful architectural discussions emerge after engineers rubber-duck their ideas before writing RFCs. Most importantly, we've seen a growing sense that learning never stops—not when you can ask an infinite number of questions to a machine that's patient, fast, and always available.

## It Starts with a Question

The keynote ended on a simple note: If you've ever pasted an error message into ChatGPT, you've already started this journey.

The only question that remains is **how far you're willing to take it**.

Are you using AI to reduce toil, or to rethink your process? Are you asking it to complete code, or to critique your decisions? Are you seeing it as a tool—or as a rubber duck with infinite patience and a few superpowers?

So here's a challenge: take one task this week—debugging, story planning, even naming a function—and instead of asking _"How do I solve this?"_, ask _"How would I solve this with AI?"_ Let it challenge you. Let it reflect something back. That's the shift. It's not replacing your thinking. It's helping you think with better mirrors.

---

I'd love to hear your take. What part of your workflow would change if you stopped treating AI like a shortcut and started treating it like a colleague?
