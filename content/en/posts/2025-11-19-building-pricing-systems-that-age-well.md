---
title: "Building Pricing Systems That Age Well"
subtitle: "The maintenance work is real. We have been doing it by hand. This post is the shape of pushing it into the decision engine so the year-three operator does not depend on the year-one engineer remembering."
author: helio
layout: post
date: 2025-11-19T10:00:00+00:00
series:
  - pricing-engineering
series_order: 12
categories:
  - Engineering
  - Pricing
  - Architecture
tags:
  - pricing
  - maintainability
  - lifecycle
  - architecture
  - observability
  - operations
description: "Pricing systems do not fail when they are built. They fail in year three, when nobody remembers why half the rules exist. The team I worked with has been holding the lifecycle together by hand — quarterly reviews, manual retirements, ad-hoc migration scripts. This post is what I have been exploring to push that work into the decision engine itself."
---

There is a rule somewhere in every pricing system that has been firing for years and that nobody on the team understands.

Mine was called `legacy_compensation_override`, last edited in 2019, firing on about 0.3% of traffic. Nobody on the team that owned the pricing engine in 2023 had been there in 2019. The commit message said "see TICKET-1481"; the ticket system had been migrated twice and TICKET-1481 no longer resolved. The rule was deterministic, inspectable, and tested. The only thing nobody could answer was whether it should still exist. We left it alone. It is probably still firing.

That is one of three rules I have personally been afraid to delete. Across teams I have worked with, the number is much larger. The pattern is the same: the rule was correct when it was written, the world it was written for has changed, the author has moved on, and there is no procedure for retiring it that the current team trusts. The rule outlives the reason for the rule.

The team I worked with on pricing has been holding this kind of decay back by hand. We ran quarterly ownership reviews on a spreadsheet. We tracked deprecations in a Slack channel and a tracking doc. We wrote migration scripts case by case when a schema needed to change. The practices worked, mostly, while we remembered them and while the people who built them were still around. They worked less well when somebody who did not run the original review had to take over the next one.

This post is what I have been exploring since: how to push these practices from the team's hands into the decision engine itself, so the year-three operator does not depend on the year-one engineer remembering to look at the spreadsheet. The practices are real. The automation is the design half I have not finished building, and writing it down is the cheapest way to figure out what I have missed.

## Five currencies that age

A pricing system pays five kinds of debt over time. Each one compounds quietly. Each one has to be designed against — and most of them, on the platform I worked on, were being held back by manual hygiene rather than by anything the engine itself did.

**Stale rules.** Rules nobody owns, nobody reviews, and nobody dares retire. The compounding factor is fear: every dead rule somebody is afraid to delete makes the next dead rule slightly safer to leave alone. The cost is in investigation time — every incident has to consider every rule that could possibly have fired, including the ones nobody understands.

**Schema drift.** The YAML schema from year one is not the schema from year three. New fields are added. Old fields stop being meaningful. The loader carries parsers for every version it has ever seen, because somewhere in the repo is a file that has not been touched since 2021 and still has to load. The compounding factor is loader complexity.

**Ownership decay.** The team that wrote the rule moves to another team. The product owner moves to another product. The metadata still says `owner: pricing-de`, but pricing-de was reorganised eighteen months ago and no longer exists. The compounding factor is escalation friction — questions about old rules route to nobody.

**Constraint inflation.** Regulatory ceilings are added. Fairness floors are added. Per-customer caps are added. Each constraint is correct individually; in aggregate, they tighten the decision space until rules that used to fire freely no longer can. The compounding factor is silent suppression — rules stop firing not because they were retired but because constraints clipped them.

**Telemetry erosion.** The dashboards from year one no longer match the system in year three. The alerts that mattered at launch are now false positives. The graphs that mattered at quarter end were optimised for last year's mix. The compounding factor is operational blindness — the team operates on dashboards that no longer describe the system.

Each of these is a category of decay. None of them is dramatic. All of them, together, are why pricing systems become illegible in year five.

## Stale rules: design for retirement

What we did, in the team I worked with, was carry the discipline in our heads. We knew which rules were old. We knew which ones we had not seen fire. Once a quarter, somebody (often me) walked through the rule store in a spreadsheet, asked the owning teams to confirm what they still wanted, and pruned. It worked. It also depended on me remembering to start the review, on the right teams answering email, and on nobody on the team who took over after me skipping a quarter.

The shape I have been exploring would push this into the rule artifact and the loader. Three properties of the rule, from Post 1, would earn their way in.

**`review_after`.** Every rule would carry a date by which it must be looked at. The date is not a deadline; it is a *prompt*. When the loader notices a rule whose `review_after` has passed, it emits a warning. The warning appears in the dashboard. The owning team gets a notification. The rule does not stop firing — that would be a different kind of bug — but the system has officially asked the team to confirm the rule is still wanted.

```yaml
metadata:
  created: 2023-02-15
  ticket: PRICE-1473
  owner: pricing-de
  review_after: 2023-08-15
```

The hard part is the cultural one: the team has to actually act on the prompt. The systems half of the problem is making the prompt unmissable, which the manual spreadsheet review never quite was.

**Hit-rate observability.** A rule that has not fired in six months is a candidate for retirement. The team would have to know which rules have fired and which have not. The explanation log from Post 7 already carries the information — every Execute records the rule names that fired — but on the platform I worked on, we queried it ad hoc when we wanted to know, not on a schedule. The shape I would build is a daily job that aggregates over the explanations and produces a *zero-fire* report.

```
ZERO-FIRE RULES (last 90 days)
rule                                  last fired       owner
legacy_compensation_override          2024-03-12       pricing-de (vacant)
italian_summer_2023_promotion         2024-08-30       marketing
weekend_routing_fallback              never            platform

OWNERLESS RULES (owner has no current team mapping)
rule                                  declared owner
legacy_compensation_override          pricing-de
holiday_promotion_2022                pricing-experiments
```

A rule that has not fired in a quarter is not necessarily wrong; it may be the safety net that activates once a year. But a rule that has not fired in a quarter *and* whose `review_after` has passed *and* whose owner no longer exists is a rule the team can almost certainly retire.

**Retirement as a first-class operation.** The pattern I have been sketching makes *disabling* a rule a first-class operation, with metadata that survives the disable. From Post 2, `Enabled: false`. A disabled rule does not fire; it still appears in the explanation log as "disabled" so investigations can see it; it carries a `disabled_at` and `disabled_by` and a reason. After ninety days of being disabled with no incident, the rule can be deleted entirely.

```yaml
- id: legacy_compensation_override
  enabled: false
  disabled_at: 2024-11-19
  disabled_by: pricing-platform
  disabled_reason: |
    Not fired in 90 days. Original owner team (pricing-de) reorganised
    in Q2 2023. No active stakeholder identified. Disabling now;
    deletion scheduled for 2025-02-17 if no regression appears.
```

The two-stage retirement — disable, then delete — is the practical answer to the team's fear. Disabling is reversible. Deleting after ninety days of disabled is a procedure, not a leap. We have made this kind of decision in retros several times. What I want is for the system itself to surface the candidate, schedule the disable, and remind the team when the deletion date arrives, instead of relying on someone reopening the spreadsheet.

## Schema evolution: keep the version, retire the parser

Post 3 introduced `version: 1` at the top of every rule file. The discipline it enabled is what makes schema evolution survivable over years. We had this — every rule file carried a version. What we did not have was a migration tool. Each schema change was its own migration script, written ad hoc by whoever was making the change, and reviewed by a small group of engineers who had context.

Three rules I have come to believe in as I think about the design:

**Every schema change should be additive first.** A new field is optional with a default. A renamed field is supported under both names for one schema version. A removed field is deprecated for one schema version before being removed. The loader runs at the same version for files at both schemas; old files keep loading. We tried to follow this in spirit; the design would enforce it.

**Every schema version should have an explicit retirement date.** The schema's term file (`schemas/v2.md`) would carry the version, the introduction date, and the `retire_after` date. After the retirement date, the loader would refuse to load files at that version; the team has to migrate. We did not have this — old versions stayed loadable indefinitely, and the loader carried parsers it should have been able to retire.

**Migration should be tooling, not manual labour.** A migration tool reads files at version N and writes files at version N+1. The tool is written when the new schema version ships. Teams owning old files run the tool, review the diff, commit the migrated file. This is what I would build first, because it is the missing piece our ad-hoc scripts kept rebuilding.

```sh
# Migrate every file in the rules/ directory from v1 to v2.
$ ruleset-migrate --from v1 --to v2 rules/

  migrated rules/de-markups.yaml         v1 → v2
  migrated rules/fr-markups.yaml         v1 → v2
  unchanged rules/compliance-de.yaml     already v2
  failed   rules/legacy-experiments.yaml could not parse v1

Summary: 14 migrated, 3 unchanged, 1 failed
```

A migration tool is the contract between schema versions. As long as it exists and runs, the team can change the schema without trapping any historical file. The day the schema changes without a corresponding migration tool is the day the schema starts collecting unintentional dialects — which is roughly what happened on our system more than once.

## Ownership: name it, prove it

The `owner` field is the rule's claim about who answers for it. The claim has to be true for the rule to be defensible. On the platform I worked on, the claim was sometimes true and sometimes a fossil of a team that had been reorganised. We knew which was which because we held the mapping in our heads. The hand-off, when somebody new took over, was a conversation, not an artifact.

The system that would earn the claim has two pieces.

**A live owner directory.** A small service or file that maps owner identifiers (`pricing-de`, `marketing-eu`, `platform`) to the current team. The mapping has to be kept current — every team reorganisation updates the directory. The loader cross-references; a rule whose `owner` is not in the current directory generates a warning at load time.

```yaml
# owners.yaml — versioned, reviewed, current
pricing-de:
  team: Pricing Germany
  manager: maria.santos@example.com
  slack: #pricing-de
  active: true
  successor: null    # if reorganised: who inherits

pricing-experiments:
  team: Pricing Experiments
  manager: null
  slack: #pricing-experiments
  active: false
  successor: pricing-platform
```

When a team is dissolved, the `successor` field would capture who inherits its rules. The loader, finding a rule owned by an inactive team, redirects the warning to the successor. The original ownership is preserved in the metadata; the live escalation goes somewhere a human reads. We did this informally — somebody on the platform team always inherited the orphans — but we did not have a way to *prove* the inheritance to a new operator. The directory is the proof.

**Periodic ownership review.** Once a quarter, every team is sent the list of rules it owns. The team confirms which it still wants, which it would retire, which it inherited and does not recognise. The output is a small ticket-list — disable these three, transfer these two to another team, keep the rest. Quarterly cadence is fast enough to catch reorganisations and slow enough not to be a tax.

We ran this review by hand for several quarters. It was the single most useful operational ritual the team had. It was also the one most likely to be skipped when somebody new took over and did not know it was a thing. The automation I would build for it is small: a scheduled job that walks the rule store, groups by owner, and emails each owning team their list with a deadline. The hard part is the cultural review; the system can carry the cadence.

## Deprecation: process, not goodbye

Retiring a rule is a decision. Retiring a *rule type* — a whole class of action, a schema field, a composition policy — is a project. Deprecation is the discipline that gets you from "we should not be using this anymore" to "we are not using this anymore" without breaking customers in the middle.

We have done this in our system by hand. Each deprecation lived in a tracking document, with a manual count of remaining uses pulled from log queries every couple of weeks, and a rough sense of when the deletion would land. The work was real; it just was not structured machinery.

The four phases I would automate:

**1. Announce.** The deprecation is published. The reason is published. The replacement is published. The retirement date is published. The dashboard adds a metric for usage of the deprecated thing.

**2. Warn.** The system emits a warning every time the deprecated thing is used. Warnings carry the deprecation document URL. The warning rate becomes the team's KPI for the deprecation — the curve has to go down before the retirement date.

**3. Error.** A small number of weeks before the retirement date, warnings become errors. Tests fail. The CI prevents new uses. Existing uses still work, but the system is louder about them.

**4. Remove.** The retirement date arrives. The deprecated thing is deleted from the codebase. The migration tool from earlier in this post is the safety net for files that still reference the deleted thing.

```
DEPRECATION SCHEDULE: action type `legacy_compensation`
  announced       2024-08-15
  warn  start     2024-09-15
  error start     2025-01-15
  retire date     2025-02-15

usage trend (last 90 days)
  2024-08    2,481 uses/day
  2024-09    1,890 uses/day      (warnings start)
  2024-10    1,103 uses/day
  2024-11      612 uses/day
  2024-12      198 uses/day
  2025-01       47 uses/day      (errors start)
  2025-02        2 uses/day      (target: 0)
```

The schedule would be published. The trend would be public. The conversation that leads to retirement is not "should we?" — that was had at announcement — but "are we on track?". The decision is made once; the operational work is the curve. We had this conversation roughly the right way, but we did it from a tracking document and a query somebody had to remember to run, not from a dashboard the system maintained.

## Constraint inflation: bound the bound

Constraints are easier to add than rules. Each one is correct individually. The aggregate is what becomes a problem. We added constraints over the years for legitimate reasons — regulatory caps, fairness floors, a maximum total discount per customer per quarter — and never had a moment when somebody asked which ones still mattered.

Two practices I would build into the system.

**Every constraint has an owner and a review date.** Same shape as rules. The regulatory cap from 2022 may not be the same cap as the regulatory environment of 2025. The fairness floor from one set of customer assumptions may not be the right floor for the next set. Constraints would inherit the rule-lifecycle discipline.

**The constraint stack is observable.** A dashboard would show, for each constraint, how often it activated (clipped or rejected) over the last quarter. A constraint that never activates is doing no work; the team can investigate whether the world changed or the constraint was always redundant. A constraint that activates on 30% of traffic is a constraint that is shaping the system in ways the rule store cannot see; the team has to understand why.

```
CONSTRAINT ACTIVATION (last 90 days)
constraint                      activated       % of decisions
regulatory_cap_de               412             0.014%
fairness_per_customer_quarter   1,820           0.061%
never_below_cost                23              0.001%
legacy_2022_compensation_floor  0               0.000%   ← investigate
max_total_discount              7,901           0.264%
```

The zero-activation row would be the constraint that has aged out. Either it has aged out gracefully — the world moved past it — or it is a bug nobody is exercising. Either way, a constraint that does no work for 90 days is a constraint to investigate, not to leave alone. We had constraints I am almost sure were doing no work, in our system, and we had no automated way to surface them; the design above is what would have caught them.

## Telemetry: build for the year-three reader

Dashboards age. The shape that survives is the one designed for someone who joins the team in year three, not someone who built the system in year one.

Three properties of dashboards that have aged well for me — and that we *did* in our team, with mixed discipline:

**Each panel names what it measures, in business words.** "p99 Execute latency, ms" is engineering. "p99 markup decision time, ms" is the same number, named in the business word. The year-three reader does not know what `Execute` is. They know what a markup decision is. Some of our panels did this. Most did not.

**Every panel has an annotation surface.** When a constraint is changed, when a rule is retired, when an experiment ships, the panels carry an annotation marking the date. The annotation is mechanical — the deployment system writes it — but a human can read the chart and connect the curve to the cause without spelunking through git. We did this manually for big launches and not at all for the long tail of small changes.

**Panels die explicitly.** A panel that is no longer useful is deleted, not silently demoted to the bottom of the page. A dashboard with one important panel and twenty stale ones is worse than a dashboard with five important panels. Deletion is a practice. This is the one we did worst. Panels accumulated.

The hardest of the three is the last one. Deleting a panel feels like losing information. The information is in the data store; the panel is the *interpretation*. An obsolete interpretation harms reading; it does not preserve anything.

## The runbook: the year-three operator's manual

Every pricing platform should ship with a runbook that the year-three operator can read. The runbook is the one piece of this post that is almost entirely about practice rather than automation — and it is the one we got most consistently right.

A useful shape:

```
PRICING PLATFORM RUNBOOK
========================
1. Architecture overview                (one page)
2. The five components and their owners
3. The explanation: how to read one     (with an annotated example)
4. The snapshot store: how to query a snapshot
5. Common incidents and their playbooks:
   - "this customer was charged wrong"
   - "the rule store will not load"
   - "shadow divergence rate spiked"
   - "p99 Execute latency crossed threshold"
6. Deprecation status (current deprecations and their schedules)
7. Owner directory link
8. Quarterly review cadence
9. How to retire a rule (the two-stage procedure)
10. How to add a constraint (the four-phase rollout)
```

The runbook is not the team's tribal knowledge; it is the *transition* from tribal to written. The test of a good runbook is whether somebody who joined the team yesterday can resolve a routine incident by reading it. The test of a bad runbook is whether the person on call has to wake someone up to interpret it.

I have written several. The ones that aged well were the ones written by the operator, not by the architect. The architect wrote what the system *does*. The operator wrote what to *do when it misbehaves*. Both are valuable. The second is the one the runbook is for.

## The lifecycle as design, not afterthought

If I had to compress this post into one sentence, it is the subtitle dressed plain: the maintenance work is real, we have been doing it by hand, and the design half I have been exploring is how to push it into the decision engine so the practice survives the people.

Concretely, what I would build:

- Every rule carries `review_after` and `owner` at the moment it is authored. The loader emits a warning when the review date passes. We did this manually.
- Every schema has `retire_after` and a migration tool at the moment it ships. The migration tool is the safety net. We wrote scripts case by case.
- Every constraint has the same lifecycle as a rule, with an activation dashboard. We did not track this.
- Every dashboard panel can be killed. Killing is a practice. We did this badly.
- Every team has a quarterly review of what it owns, automated as a scheduled email. We did this by hand, irregularly.
- The runbook is shipped with the system, not after it. We did this well.

None of this is dramatic. All of it compounds. A pricing platform built with these properties in mind from day one is one that, in year five, is still operable by a team that did not build it. A pricing platform built without them is the platform somebody else will have to rewrite. We were running closer to the second case than I would have liked, held back from it by the manual practices that depended on the people who knew them.

## What comes next

The next post is a personal retrospective: ten mistakes I have shipped while building pricing platforms. Several of them are the cultural failure to make the practices in this post systemic. Premature optimisation, wrong abstractions at the wrong layer, false confidence from green tests — and trusting manual hygiene to scale when the team turned over.

The final post is what I would build differently today, with everything the first time taught me. That is the post the whole series has been preparing for. It is also the shortest, because by the time you have read everything that came before, the answer is mostly compression.

## The lesson

The pricing systems I have shipped that aged well had three things in common. They had explicit owners. They had review dates. They had retirement procedures. The pricing systems that aged badly were the ones that were *correct* at launch and not designed to be *operable* in year three.

We did the operability work on our system by hand. It was real work, it was good work, and it was fragile because it depended on the people doing it. The design I have been writing toward in this post is the half that would carry the work from the people into the system. I have not finished building it. The reason for writing it down is the same as for Post 10: it is the cheapest way to find out what I have missed before I commit to building it for real.

The rule from 2019 that nobody can explain is a small failure. The rule store that is half-filled with such rules is the failure mode pricing platforms quietly slide into. The defence is the lifecycle, and the lifecycle has to live somewhere — either in the team's heads, where it depends on the team staying, or in the system, where it can outlast the people. The work is moving it from the first place to the second.
