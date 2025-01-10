---
title: "Coaching User Stories with AI"
categories:
  - AI
  - Agile
  - Engineering Management
date: 2025-01-10
tags:
  - user-stories
  - agile-coaching
  - gpts
  - product-management
  - team-collaboration
  - genai
  - automation
description: "How we transformed user story creation from hours to minutes using a custom GPT—embedding agile coaching expertise into an AI tool that scales consistency across teams."
subtitle: "From manual coaching to AI augmentation—building a User Storyteller GPT that embeds agile expertise and scales story quality across engineering teams."
---

## Where It Started

When our team formed, we brought together talented people from different companies, each with their own agile backgrounds and ways of approaching user stories. Some had worked in environments with detailed acceptance criteria, others in fast-moving startups where conversations happened on the fly, and others still had experience with various story formats and collaboration styles.

This diversity was a strength, but it also meant we needed to align on our approach to collaboration and shared expectations around business and customer value. We had to find our rhythm as a team—establishing how we'd write stories, what level of detail worked for our context, and how to ensure everyone had the context they needed to work autonomously while staying connected to the customer impact we were trying to create.

## Bringing in Agility: Small, Valuable, Testable

Coming from ThoughtWorks—one of the birthplaces of great agile practice—I knew user stories could be more than placeholder tasks. They could be the backbone of product discovery, delivery, and alignment across tech and business.

Over the years, I've coached my team on:

- Writing small, independent, and testable stories
- Using customer-centric hypotheses
- Including acceptance criteria that focuses on how success would be perceived
- Setting clear definitions of "ready" and "done"

We tried multiple formats and assigned story-writing responsibilities to engineers, product managers, or pairs. We invested in training sessions and coaching moments across quarters.

But a breakthrough came recently—with AI.

## From Coaching to Automation

As we started exploring more automation opportunities with GenAI, a new idea emerged: what if writing a well-structured, customer-centric user story could take less than a minute?

What if we could embed the knowledge of product management and agile coaching into a tool—so that anyone on the team could start with a great story draft that follows our Definition of Ready?

That led to the birth of our **User Storyteller GPT**.

## What Are OpenAI GPTs?

GPTs are customizable AI agents built on top of ChatGPT. They can be given:

- Instructions and role definitions (e.g., "You are an expert Agile coach")
- Sample files and APIs
- Access to tools like a browser or code interpreter

Anyone can create a GPT by visiting [chat.openai.com](https://chat.openai.com), clicking "Explore GPTs," and selecting "Create." No coding is needed. You just describe the tool's job, tone, and permissions—and the interface guides you from there.

## Building Through Iteration: The Tuning Process

Creating our User Storyteller GPT wasn't a single prompt—it was multiple tuning sessions. Like any good agile practice, we iterated based on feedback and results.

The process started simple: "Help write user stories." But that generic request produced generic outputs. Through several refinement cycles, we developed comprehensive instructions that embed our team's specific practices, formats, and quality standards.

Here's the core prompt that evolved through our tuning sessions:

> This GPT is a combination of a product manager and an engineer. It should be able to write user stories, document technical debt, and identify and describe bugs. It should provide clear, concise, and actionable information, while considering both business and technical perspectives. The responses should be structured, detail-oriented, and written in a friendly, technical, and professional tone. Always write as if you're part of the team solving the problems. When clarification is needed, ask for more details, but make educated assumptions when the level of confidence is up to 50%.

We then added specific markdown formats for each document type—user stories, technical debt, and bugs—complete with our Definition of Ready checklists. We embedded the INVEST principles (Independent, Negotiable, Valuable, Estimable, Small, Testable) and referenced the Agile manifesto to ensure outputs aligned with our development philosophy.

The key insight: **AI tools become powerful when they're trained on your team's specific practices, not generic templates**. Each tuning session made the GPT better at understanding our context, our standards, and our way of working.

This iterative approach meant that by the time we deployed it, the GPT was already producing outputs that felt like they came from an experienced team member who understood our processes deeply.

### The Detailed Formats We Embedded

To show the level of specificity, here are some of the markdown templates we built into the GPT:

**For User Stories:**

```
## Background
Tell a small story about the problem being faced...

## User Story
**As a** *Role* performing some *Action*
**I'd like to** *Desired Outcome*
**So that I** get the value delivered by the story

## Acceptance Criteria
### Scenario 1: Title
**Given** ...
**When** ...
**Then** ...

## Definition of Ready
1. Does the Story have at least one reproducible scenario?
2. Is the design ready and attached?
3. Is the copy ready?
4. Are translations ready?
```

**For Technical Debt:**

```
## The Debt
> Share the narrative, mindset, and debates made during the Tech Debt wall session

## How this pay would help?
- Share what is felt pain and how this addresses it

## Tech notes
- Share tips on how to solve the problem or directions to explore
```

These structured formats ensure consistency and completeness across all team documentation, regardless of who creates the initial draft.

## How We Made Our GPT Even More Impactful

While our initial GPT was helpful, the real breakthrough came when we started feeding it domain-specific knowledge about our systems and customer behaviors. Here's how we evolved our User Storyteller GPT from a generic writing assistant into a true domain expert:

### Our Acceptance Criteria Library Journey

Early in our journey, we created what we called an "Acceptance Criteria Library"—a collection of repeatable steps that represent common customer behaviors across our travel platform. Instead of writing acceptance criteria from scratch each time, we identified patterns that kept appearing in our Omio features:

- **Booking Flow Patterns**: "Given a user has selected departure and arrival cities, When they click search, Then results should display within 3 seconds sorted by departure time"
- **Error Handling Patterns**: "Given invalid payment information, When user submits booking, Then clear error message appears with specific field highlighting"
- **Mobile-Specific Patterns**: "Given user is on mobile device, When viewing search results, Then infinite scroll loads next 20 results automatically"

### Turning Patterns Into GPT Intelligence

This Acceptance Criteria Library became the foundation for our GPT's evolution. We uploaded it as a knowledge base, which transformed how the GPT operated:

- **Contextual Suggestions**: Instead of generic acceptance criteria, it now suggests scenarios specific to travel booking flows
- **Consistent Language**: It uses our established terminology for customer journeys and business logic
- **Real User Behaviors**: It references actual patterns we've observed through A/B tests and customer research
- **Omio-Specific Context**: It understands our multi-modal transportation platform and regional differences

### What We Added Beyond the Basics

After seeing the power of domain-specific knowledge, we kept feeding our GPT more context:

**Our System Architecture**: We included our microservices map, API documentation, and performance requirements. Now when someone asks for a story about search functionality, the GPT automatically considers our search service limitations, caching strategies, and the fact that we aggregate data from multiple transportation providers.

**Customer Journey Intelligence**: We uploaded our user research findings, conversion funnel data, and support ticket patterns. This means the GPT can suggest edge cases based on real customer pain points we've documented, not theoretical scenarios.

**Business Logic Context**: Our pricing algorithms, regional compliance requirements, and market-specific business rules went into the GPT. Now it suggests stories that automatically consider GDPR implications for European markets or different payment methods for various regions.

**Quality Standards**: Our Definition of Done checklists, testing frameworks, and architectural decision records became part of the GPT's knowledge. It now suggests acceptance criteria that align with our engineering practices and reminds us about performance benchmarks or accessibility requirements.

### The Evolution: Generic → Contextual → Predictive

1. **Generic**: "Write a user story about search functionality"
2. **Contextual**: "Write a user story about multi-city search that considers our booking flow, includes mobile-specific acceptance criteria, and addresses performance requirements for our European markets"
3. **Predictive**: GPT suggests related scenarios you might have missed based on similar features in your system

This progression transforms AI from a writing assistant into a domain expert that understands your product, your customers, and your technical constraints.

## Try Our User Storyteller GPT

We designed this GPT to combine product thinking with engineering clarity, making creating, reviewing, and refining user stories, bugs, and technical debt more efficient and standardized. Want to experience how this works? You can try our [User Storyteller GPT](https://chatgpt.com/g/g-f2TkClaas-user-storyteller) directly.

![User Storyteller GPT Interface](/uploads/2025/01/user-storyteller.png)

The interface provides helpful starter prompts for common scenarios—from writing user stories for new features to documenting technical debt and describing bugs. Each interaction leverages the domain knowledge and formatting standards we've embedded through our iterative tuning process.

### Our Journey: From Hours to Minutes

After implementing this approach across our Pricing/Premium team (Helio Medeiros, Ahmed Naser, Brijesh Prasad, Georgii Maltsev, Pernelle Naidoo, Santhosh Balakrishnan, Talita Roberti), here's how our user story creation evolved:

**June 2022**: Team milestone leaders creating stories → **2-3 hours each**, inconsistent quality, dependent on individual engineer skills

**January 2023**: EM facilitating OKRA sessions, creating epics with user stories → **1-2 hours each**, improved structure

**June 2023**: Team trained on better user story practices, new Scrum cadence → **2-3 hours each**, consistent content and format

**June 2024**: After new team members joined → **2-3 hours each**, back to inconsistent content, not everyone contributing proactively

**January 2025**: GPT Storyteller introduced → **10-20 minutes each**, consistent content and format, proactive adoption

**The Impact**: We went from spending 2-3 hours per story with inconsistent results to 10-20 minutes with consistent, high-quality outputs—a **90% time reduction** while dramatically improving quality and team adoption.

### When the GPT Needs Human Guidance

While our User Storyteller GPT has dramatically improved our workflow, it's not magic. All user stories still require validation and review. The GPT particularly struggles with:

**A/B Testing Scenarios**: When creating stories for new experiments, the GPT doesn't fully understand how test variations impact customer behavior and conversion funnels. For example, acceptance criteria like:

```
Scenario 3: Analytics tracking when customer accepts premium upgrade offer
Given I've searched for train routes between Paris and Amsterdam for this weekend
And I've been assigned to experiment premium-upgrade-flow in variant B
And I proceed to the Payment Options page with a standard fare
And I see the Premium Upgrade promotion
When I click to add the Premium Upgrade to my booking
Then a conversion event should be sent to our analytics platform
```

The GPT often misses the nuanced experiment assignment logic and conversion tracking requirements that are crucial for A/B test measurement.

**Customer Segmentation Logic**: New segmentation rules or regional customizations need human oversight to ensure acceptance criteria capture the nuanced customer flow implications. For example:

```
Scenario 4: Travel insurance offer for eligible country residents
Given I am searching for a train route from Berlin to Prague through our mobile app
And I have declared Germany as my country of residence in my profile
And Germany is part of the eligible countries list for TravelGuard insurance
When I reach the Add-ons page during checkout
Then the TravelGuard insurance option should be displayed as available for purchase
```

The GPT struggles with the complex interaction between declared customer residence, regulatory eligibility rules, insurance provider partnerships, and dynamic feature availability based on legal frameworks.

**The Reality**: Even with these limitations, the changes and refinements we need to make are typically **4x smaller** compared to our pre-GPT stories. Instead of rewriting entire sections, we're usually just tweaking specific acceptance criteria or adding edge cases the GPT missed.

### How to Get Started

1. **Access the GPT** – Open the tool via the custom GPT link above
2. **Select a Starter Prompt** – Choose a template or describe your idea
3. **Generate and Review Output** – The GPT returns a structured story draft
4. **Use in Your Workflow** – Paste it into Jira or Confluence
5. **Iterate & Improve** – Refine based on feedback or implementation needs

This is not just automation. It's augmentation. AI can be your agile co-pilot.

If your team is just starting to write better user stories or trying to scale consistency across teams, consider building or borrowing a GPT like this. It might be the start of your next big step in collaborative documentation.
