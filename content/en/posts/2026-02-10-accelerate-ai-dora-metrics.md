---
title: "Accelerate Meets AI: Using DORA Metrics to Observe, Align, and Improve Engineering Collaboration"
categories:
  - AI
  - Engineering
  - Leadership
date: 2026-02-10
tags:
  - ai
  - dora-metrics
  - accelerate
  - engineering-leadership
  - productivity
  - coaching
description: "AI does not fail the team. The team fails to adapt around it. Here is what I learned using DORA metrics and adoption stages to guide that adaptation on my own teams."
subtitle: "What I learned leading teams through AI adoption"
---

A few weeks ago, one of my engineers said something in a 1:1 that stuck with me.

"I am using AI every day. But I am not sure we are actually getting better."

He was not complaining. He was being honest. And he was right to question it, because the feeling on the team was mixed. Some people were moving faster. Others felt like the ground had shifted underneath them. We had more AI usage than ever, but the delivery signals were not clearly improving.

That conversation forced me to ask a harder question: **how do I actually know if AI is helping my teams — and not just keeping us busy?**

I did not have a good answer at first. What I had was a hunch that the metrics I already trusted — DORA metrics from *Accelerate* — could help me see what was really going on. So I went back to them. Not as theory. As a way to stop guessing and start observing.

## What I saw when I stopped assuming

On my teams, AI had already changed how people worked. Engineers were using agents for planning, debugging, test creation, documentation. The workflow had shifted. That part was not in question.

But the shift was uneven. Some people had rewired their entire way of working. Others were copy-pasting suggestions and editing them into shape. A few had quietly gone back to doing things manually because the AI output kept needing too much correction.

I noticed this not because anyone reported it, but because the delivery numbers told a different story than the conversations. People said AI was helping. The metrics were flat.

That gap between perception and reality is where I decided to dig in.

## Going back to DORA — not as theory, but as signal

I went back to the four DORA metrics because they answer the question I actually cared about: are we delivering value fast, safely, and sustainably?

| Metric | What it told me |
| --- | --- |
| Lead Time | How long work sat between commit and production |
| Deployment Frequency | Whether we were actually shipping, or just coding |
| Change Failure Rate | Whether speed was costing us stability |
| Time to Restore | How fast we recovered when something broke |

The point was not to benchmark against industry standards. It was to watch the trend on my own teams. If AI was genuinely improving how we worked, I should see lead time going down, deploy frequency going up, and failure rates not getting worse.

> DORA did not tell me whether my team was using AI. It told me whether AI was making our system better.

In several conversations with other managers, I heard the same frustration: "My team is using AI, but I cannot tell if it is helping." That is exactly the gap DORA fills. It gives you something observable to point at instead of trading impressions.

Here is what our DORA tracking actually looks like — each metric mapped to a threshold the team calibrates together:

![DORA metrics overview — Lead Time, Deployment Frequency, Change Fail Percentage, and Recovery Time tracked across the team](/uploads/2025/03/dora-metrics-overview-detail.png)

## Making the invisible visible

The first thing I learned is that without metrics, every conversation about AI drifts into opinion. "I feel slow." "AI helps me." "We are busy." Those are sentiments. I needed signals.

We started simple. Nothing elaborate — just enough visibility to shift the conversation from impressions to patterns.

```bash
git log --pretty=format:'%h %ad %s' --date=short > commits.txt
```

From there, we could see lead time per pull request, deployment frequency per week, and who was shipping what. The change in how people talked about work was almost immediate:

| Before | After |
| --- | --- |
| "I feel slow" | "Lead time increased this sprint" |
| "AI helps" | "AI reduced average cycle time by 20%" |
| "We are busy" | "We are not shipping" |

That shift mattered. Nobody felt blamed. People started using a shared language for what was actually happening, and our retros got sharper because we had something concrete to look at instead of arguing about feelings.

We consolidated everything into a single dashboard — deployment velocity, experiment status, DORA snapshot, and contributor patterns in one place:

![Team dashboard showing DORA snapshot, deployment velocity, experiment status, and top contributors](/uploads/2025/03/dora-dashboard-team-overview.png)

From there, I could drill into Lead Time specifically. The aggregate number was useful, but the trend told a better story:

![Lead Time for Changes — weekly aggregate p50 at 1.2 days, with p99 trend over time](/uploads/2026/01/dora-lead-time-overview.png)

The real value came from the PR-level data underneath. Ninety-five merged PRs with their repo, lead time, and category. When I sat down with an engineer and opened this view, the coaching conversation practically led itself:

![PR logs showing 95 merged PRs with repository, lead time, and category breakdown](/uploads/2026/01/dora-lead-time-pr-logs.png)

One thing I did not expect: separating lead time by context made a big difference. When someone was away, the numbers spiked — and treating that the same as regular flow would have been misleading:

![Lead Time in Away Mode — p50 at 19.9 hours, showing a different pattern from regular flow](/uploads/2026/01/dora-lead-time-away-mode.png)

Filtering by primary services gave us the clearest picture of where the actual delivery work lived:

![Lead Time for primary applications and services — p50 at 1.5 days across core repos](/uploads/2026/01/dora-lead-time-primary-services.png)

## People were at different stages — and that was the point

Once I had the system view, the next thing I needed was the human view.

Not everyone on my teams was at the same place with AI. One engineer had already moved to multi-agent CLI workflows and was generating pull requests at a pace I had not seen before. Another was still cautious, using Copilot suggestions but reviewing every line as if it were a junior developer's code. Both were being responsible. Both needed different support.

I borrowed Steve Yegge's AI adoption stages as a way to talk about this without it feeling like judgment:

| Stage | What it looks like on my teams |
| --- | --- |
| 1 | Curious but not yet using AI in daily work |
| 2 | Using an IDE agent, but with guard rails up |
| 3 | Trusting the agent more, accepting suggestions with less friction |
| 4 | AI is the default workflow in the IDE |
| 5 | Working with a single CLI-based agent |
| 6 | Running multi-agent workflows from the terminal |
| 7 | Managing many agents, but manually coordinating them |
| 8 | Building custom orchestrators across workflows |

The moment I started mapping my engineers to this spectrum, the conversation changed. It stopped being about who was "good at AI" and started being about where each person needed support to move forward. One manager I spoke with recently adopted the same framing and told me it was the first time his team talked about AI adoption without it feeling like pressure.

## What happens when people skip stages

I have seen this go wrong — on other teams and, honestly, in early moments on my own.

When I pushed one of my teams to start pairing with multi-agent workflows before most of the engineers had even gotten comfortable with single-agent patterns, the feedback was fast and clear:

- "This is chaotic"
- "I do not trust the output"
- "It is making me slower, not faster"

That was on me. I had skipped stages because I was excited about what was possible. What I learned is that AI adoption follows the same rule as any significant change: trust is built through small wins, not big mandates. The engineers who moved fastest were the ones who had time to experiment, fail in small ways, and build confidence at their own pace.

> The real risk is not slow adoption. It is forced adoption that burns trust.

A manager I talk with regularly put it well: "I stopped asking my team to use AI more and started asking what is still slowing them down. The AI conversation happened naturally after that."

## Setting goals we could actually see

Once I had the DORA signals and the adoption map, I could set goals that were grounded in what was real — not aspirational targets pulled from a strategy deck.

I organized them around three things that mattered to my teams:

**AI usage** — not mandates, but clear expectations for growth:

- Use AI for planning, debugging, and documentation as a baseline
- Apply AI-assisted testing in at least one workflow per sprint
- Deliver one full story per sprint with meaningful AI agent involvement

I wrote these as SMART goals connecting each person's growth to the direction we were heading:

![SMART goal: Using AI as a practical support tool to improve efficiency and quality in daily engineering work](/uploads/2025/03/smart-goal-ai-practical-support.png)

![SMART goal: Regular use of AI tools for technical exploration, planning, debugging, and documentation](/uploads/2025/03/smart-goal-ai-tools-usage.png)

**Delivery quality** — keeping ourselves honest:

- PR coverage at 80% or above
- Lead time under one week
- Deployment frequency weekly or better

These tied directly to the same DORA metrics we were already tracking, so there was no gap between the goal and the measurement:

![SMART goal: Ensuring quality and efficient deliveries through PR coverage and DORA metrics](/uploads/2025/03/smart-goal-dora-pr-coverage.png)

**Collaboration** — making sure the learning did not stay in one person's head:

- Use multi-agent workflows in at least one story per sprint
- Run knowledge-sharing sessions on what was working
- Reduce average lead time by 25% over the quarter

I structured this dimension as an OKR with measurable key results, because I wanted the team to own the outcome together:

![OKR: Accelerate delivery through multi-agent AI collaboration with measurable key results](/uploads/2025/03/okr-multi-agent-collaboration.png)

What made these goals work is that every one of them was observable. We could measure progress, discuss it in retros, and adjust without the conversation becoming personal.

## Coaching people, not stages

The table below is how I think about where to focus when someone is ready to move:

| Transition | What I focused on |
| --- | --- |
| Stage 1 to 2 | Showing what was possible — pairing sessions, demos, low-risk tasks |
| Stage 2 to 3 | Creating safety — letting them experiment without performance pressure |
| Stage 3 to 4 | Building ownership — stepping back and letting AI become their default |
| Stage 4 to 5 | Expanding scope — introducing CLI-based agents for broader tasks |
| Stage 5 and beyond | Multiplying impact — teaching others, building reusable workflows |

The engineer I mentioned at the beginning — the one who said "I am using AI every day but I am not sure we are getting better" — was at stage 3. He was productive but not yet trusting the agent enough to let it lead. Three weeks after our conversation, with a clearer goal and the right pairing partner, he moved to stage 5. His lead time dropped noticeably. More importantly, he started sharing what worked with the rest of the team.

That is what I care about. Not frameworks. Not adoption percentages. Whether the people on my teams are learning faster and delivering with more confidence.

## What I am still learning

I do not have this figured out. AI is changing fast enough that what works today might not work in six months. Some of my goals will probably need to be rewritten. Some of my assumptions about stages will turn out to be wrong.

But I am clearer on one thing now than I was before. The teams that are getting better are not the ones adopting AI the fastest. They are the ones that can see what is happening, talk about it honestly, and adjust without losing speed or trust.

DORA gives me the system view. The stages give me the human view. Together, they replaced guessing with something I can actually act on.

If you are leading a team through this same transition, the question I would start with is not "how do we use more AI?" It is simpler and more honest: **what is actually happening on your team right now — and how do you know?**
