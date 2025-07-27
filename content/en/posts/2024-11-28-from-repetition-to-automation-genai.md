---
title: "From Repetition to Automation with GenAI"
categories:
  - AI
  - Productivity
  - Engineering Management
date: 2024-11-28
tags:
  - automation
  - genai
  - productivity
  - workflows
  - gpts
  - google-apps-script
  - sprint-automation
description: "Transform repetitive tasks into smart automation using GenAI—from recognizing patterns in your work to building practical workflows with GPTs and Google Apps Script."
subtitle: "When repetition becomes a signal for automation—discover how to move from manual tasks to intelligent workflows that scale your intent."
---

At some point, I realized I was typing the same prompts again and again. Different day, same setup. Same structure. Same edits. Over time, this became my first breakthrough—not because I discovered a clever prompt, but because I noticed a pattern in my work.

This post is about that moment: when repetition becomes a signal. And how that signal, if followed, can lead to thoughtful automation.

## My Love for Organization Systems

I've always been drawn to organization and time management tools. For more than 10 years now, I've been using the [Bullet Journal method](https://bulletjournal.com/pages/story)—a mindfulness practice designed as a productivity system created by Ryder Carroll. What I love most about this analog approach is how it lets me quickly jump between years and see what patterns emerge across days, months, and entire years. The physical act of writing creates a searchable archive of my thoughts, decisions, and recurring themes.

Through my Bullet Journal practice, I can flip back through months of entries and spot the same challenges, the same types of meetings, the same decision points appearing over and over. This long-term view is what first made me aware of my repetitive prompting patterns with AI tools. The Bullet Journal taught me to look for patterns—and one of its foundational practices is exactly what I recommend as the first step toward automation.

## Step 1: Understand Your Routine with a Time Journal

Before you automate anything, you need to understand where your time and energy go.

A time journal is a simple reflection tool. For three to five days, write down what you do every 30 to 60 minutes. For each entry, note:

- What you did
- How long it took
- How it made you feel (energized, drained, productive, distracted)
- Whether it felt essential, repetitive, or creative

This helps build awareness of your patterns—what's worth automating, and what's already working well.

## Step 2: Identify Repetition and Automation Opportunities

When you review your time journal, certain patterns will emerge that reveal automation goldmines. As an engineer, you might notice that every Monday morning you spend 30 minutes manually checking server logs, formatting deployment reports, or writing similar status updates to stakeholders. As a manager, you may discover that you're constantly drafting similar emails—onboarding instructions for new team members, sprint retrospective summaries, or project update requests that follow the same structure but with different details.

The key insight here is distinguishing between valuable repetition and energy-draining repetition. Code reviews, for instance, are repetitive but require human judgment and teaching moments. However, the administrative scaffolding around code reviews—creating tickets, updating project boards, or sending reminder emails—often follows predictable patterns that can be automated.

Look especially for work that has consistent input-output relationships. When you find yourself thinking "I've written something like this before" or "This follows the same format as last time," you've found a candidate for automation. The question isn't whether the task is important, but whether the mechanical parts of that important task can be handled by AI while you focus on the strategic, creative, or interpersonal elements that truly require your expertise.

## Step 3: Adopt an AI-First Mindset

Before you can effectively automate with AI, you need to understand its capabilities and limitations through deliberate practice. This is where enters "AI-First Mindset"—a learning approach that has been crucial for my automation success.

My setup is simple but intentional: I work with two displays. On my main screen, I handle my regular workflow. On the second display, I actively invite AI into every step of my routine, no matter how small or seemingly inappropriate. Writing an email? AI gets a look. Planning a meeting agenda? AI provides input. Reviewing code? AI offers a perspective. Even mundane tasks like organizing files or scheduling—everything gets the AI treatment.

This isn't about replacing my judgment or making AI do all the work. It's about building a deep understanding of where AI collaboration makes sense and where it doesn't. Some interactions teach me that AI excels at certain patterns I hadn't considered. Others reveal limitations that save me from future automation mistakes. Sometimes I discover that an approach works today but needs refinement, so I note it for revisiting in a week or month as models improve.

This practice has been invaluable for automation because it gives me real data about AI's strengths and weaknesses across the full spectrum of my work. When I later identify repetitive tasks worth automating, I already know from experience how AI handles similar contexts, what prompting patterns work, and where human oversight remains essential.

The AI-First Mindset isn't about blind adoption—it's about informed partnership. By deliberately experimenting with AI across your entire workflow, you build the intuition needed to automate effectively and avoid the common trap of automating the wrong things or automating them poorly.

## Step 4: Automating with AI the Right Way

Automating everything at once rarely works. Start with a smaller step, and build from there.

**Divide and Conquer**
Break larger workflows into small steps. AI may not be able to do the full job, but it can often take care of one meaningful part.

**Automate Incrementally**
Begin with a draft or suggestion step. Add polish and more functionality later.

**Allow Manual Steps**
Semi-automated workflows are still efficient. You can leave review points, manual approvals, or triggers.

**Think in Pipelines**
Consider the process in stages:

1. A trigger occurs (such as closing a sprint)
2. Data is collected
3. A summary or output is generated
4. It is formatted
5. It is shared

Each of these can be built separately.

## Step 5: Tools That Make Automation Accessible

You don't need to be a professional developer to get started with automation today. There are tools built specifically to work with Generative AI.

### OpenAI GPTs

GPTs are custom versions of ChatGPT that you can build inside the ChatGPT interface. You can give them instructions, define their purpose, and even upload files or enable them to call APIs or use tools like a browser or code interpreter.

To build your first GPT:

1. Go to chat.com and click "Explore GPTs"
2. Choose "Create a GPT"
3. Use the guided builder to describe what you want the GPT to do
4. Optionally upload files, configure APIs, or define its tone and behavior

No coding is required. However, understanding how to write clear prompts and describe roles or tasks is key.

### Google Apps Script

Google Apps Script is a lightweight programming environment based on JavaScript that connects and automates tools in Google Workspace like Gmail, Google Sheets, Calendar, and more.

To build your first script:

1. Go to script.google.com
2. Create a new project
3. Use the editor to write your logic (you can find templates online)
4. Authorize the script and set up triggers (like time-based or event-based)

Some familiarity with JavaScript helps, but many automations can be copied and adapted from community examples.

## A Practical Example: Sprint Summary Emails

Let's say your team works in Jira, and you want to keep stakeholders informed when sprints are completed.

**Workflow:**

1. When a sprint closes in Jira, Google Apps Script detects it via webhook or a time-based check.
2. It gathers:
   - Sprint name and timeline
   - List of completed stories
   - Goals that were targeted
3. This information is sent to a GPT with a prompt such as:
   - "Summarize this sprint for business stakeholders, focusing on progress toward goals and any major scope changes."
4. The GPT returns a clear summary written in your tone.
5. Apps Script formats and sends the summary email to a predefined distribution list.

This saves time and ensures consistent communication.

## From Analog Patterns to Digital Workflows

When I started typing the same prompts repeatedly, I didn't immediately think "automation." I thought "pattern." That's the Bullet Journal in me—ten years of handwritten entries teaching me to notice when today looks suspiciously like yesterday.

But here's what I've learned: the path from noticing repetition to building effective automation isn't just about the tools. It's about building the right relationship with AI first. My two-display approach taught me that AI collaboration is a skill that needs deliberate practice. You can't automate well what you don't understand, and you can't understand AI's capabilities without experimenting across your entire workflow.

The progression is clear: awareness leads to experimentation, experimentation builds intuition, and intuition enables smart automation. Skip any step, and you'll automate the wrong things or automate them poorly.

Start small. Pick one repetitive task from your time journal. Apply the AI-First Mindset to understand how AI handles that type of work. Then build your first simple automation—even if it just drafts an email or formats a report. The goal isn't to replace yourself; it's to amplify your intent and free up mental space for the work that truly requires your uniquely human skills.

The tools are ready. The question isn't whether AI will change how we work—it's whether we'll be intentional about how we let it change us. Choose curiosity over comfort. Choose experimentation over efficiency. Choose learning over shortcuts.

Your future self will thank you for starting today.
