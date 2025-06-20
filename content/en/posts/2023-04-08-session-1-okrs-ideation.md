---
title: "OKRA Session #1: Cultivating Team-Driven OKRs from Company Soil"
categories: ["Architecture", "Management"]
date: 2023-04-08
description: "The third post in the OKRA series, guiding teams through the process of drafting team OKRs from company strategy, with practical facilitation tips and real-world patterns."
series: ["okra"]
series_order: 3
---

## 1. When Company OKRs Are Clear, It's Time to Draft Team OKRs

Session #1 starts once company-level OKRs have been presented. The goal isn't to debate those objectives—it's to translate them into something the team can act on. Often, this session is the first time all perspectives meet: product, design, engineering, data, and customer operations. We use it to map our contributions, spot misalignment early, and draft an OKR set the team will refine and own.

We don't see OKRs as compliance artifacts or roadmap theatre. We treat this moment as the one where empowered product teams connect deeply with leadership vision—the golden thread. This is when our hypotheses take shape, grounded in technology constraints, business understanding, and customer insight.

OKRs don't start with goals. They start with constraints, customer pain, and limited capacity. And from there, we shape what impact is realistic, measurable, and strategically aligned.

| Input                  | Output                                  |
| ---------------------- | --------------------------------------- |
| Company OKRs           | Shared understanding of strategy        |
| Team product areas     | Draft contributions mapped to each goal |
| Customer pains & gains | Relevant Key Results with clear intent  |

If you skip this session, you often end up writing OKRs that sound nice but lack grounding. This is where we fix that.

## 2. The Ideation Flow: From Contribution to Hypothesis

This session has a flow—and every step plays a part:

1. **Listen First**: A stakeholder presents the company's OKRs. Team members write down ideas for contribution silently.
2. **Cluster and Clarify**: After ideas are collected, the group reads them aloud, clusters duplicates, and refines similar inputs.
3. **Pair Up for Value Mapping**: In pairs, team members write how the customer will benefit from this OKR (pains/gains).
4. **Define Metrics**: Pairs also list what measurable signals will show if the objective is being achieved.
5. **Validate with Hypotheses**: Each pair writes what must be true for this goal to work. These are testable assumptions.

```markdown
Objective: Improve match reliability in urban areas
KR1: 80% of matches created have at least 6 confirmed players 12h before start
KR2: 95% of matches send an automatic reminder 24h before kickoff
Hypothesis: If users receive timely reminders, they will confirm earlier and attend more reliably.
```

## 3. Patterns We've Seen That Help or Hurt

In teams where Session #1 worked well, a few things were always true:

- There was strong facilitation to timebox each step.
- Engineering and Product both shared ideas—not just PMs.
- Trade-offs were flagged early (e.g., tech debt vs. delivery)
- People spoke in terms of _users_ and _metrics_, not features.

When it didn't work:

- Ideas were vague or disconnected from company goals
- The loudest voice shaped the OKRs too early
- No space was given to validate if the Key Results were feasible

| Behavior                      | Outcome                                           |
| ----------------------------- | ------------------------------------------------- |
| Focusing on impact not output | Objectives feel inspiring but are still realistic |
| Hypothesis before metric      | KRs make more sense and are easier to test        |
| Ignoring blockers             | Plans break down during implementation            |

We encourage teams to build OKRs that validate learning—not deliverables. This is where innovation begins: not from guesses, but from small bets supported by real-world signals.

## 4. Facilitation Guide for Session #1

This is a session that benefits from structure. Here's a proven path:

1. **Company OKRs Presentation** — Stakeholder or PM shares the quarter's direction.
2. **Silent Contribution Round** — Everyone writes how the team might contribute (sticky notes or docs).
3. **Read & Cluster** — Go around reading notes aloud and grouping overlapping ideas.
4. **Blocker Check** — Ask each person to name any risk or dependency tied to their contribution.
5. **Value & Hypothesis Pairs** — Break into pairs and write customer pain/gain, metrics, and hypotheses.

```bash
# Session layout suggestion
okra/
├── session-1/
│   ├── draft-objectives.md
│   ├── pains-gains.md
│   ├── metrics.md
│   └── hypotheses.md
```

## 5. What to Bring Into the Next Session

By the end of Session #1, the team should have:

- A small set of draft Objectives that connect to company goals
- 1–3 Key Results per Objective, with hypotheses and initial metrics
- Known blockers and dependencies that might impact feasibility

```markdown
Objective: Build trust in player ratings
KR: 70% of players receive at least one rating per match
Hypothesis: If players feel their feedback is visible, they'll participate more actively in rating others.
```
