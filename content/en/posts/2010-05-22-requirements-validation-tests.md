---
title: Requirements, Validation, and the Role of Testing
author: helio
date: 2010-05-22 14:30:22+00:00
description:
  Reflections on the twelfth and final Software Engineering lecture, exploring
  requirements engineering, validation practices, and the critical connection between
  clear requirements and effective testing.
categories:
  - Development
  - Agile
tags:
  - Software Engineering
  - Requirements Engineering
  - Validation
  - Testing
  - TDD
  - Quality Assurance
  - User Stories
  - Acceptance Criteria
  - UnP
  - Teaching
  - software-engineering-series
series: Software Engineering Fundamentals
subtitle: Software development concepts and practices
---

> **Series: Software Engineering Fundamentals** | **Part Part 12 of 19** > _Delivered at Universidade Potiguar (UnP) in 2010_

It was in this class that I decided to bring together two key themes that often seem disconnected in early software training: **requirement engineering** and **software testing**. Many students see them as separate tracks, but in practice, they're two sides of the same mirror. We can't write meaningful tests without clear requirements, and we can't evaluate quality if we don't know what was requested in the first place.

## Defining the Problem Before the Solution

We opened the class revisiting the idea of a **product vision**. I challenged students to write it in natural language, not UML, not pseudo-code. A single paragraph. Something their grandmother could read and understand.

Why? Because if you can't explain the problem without relying on the solution's language, you probably don't understand it yet.

This approach builds the foundation for collaboration with stakeholders who don't speak tech—and trains engineers to focus on **value, not features**.

## Requirements That Don't Hide the Truth

I used McConnell's definition again: "requirements describe in detail what the system should do." But this time, we dove deeper into what makes a requirement useful:

- It avoids guessing.
- It gives users the chance to validate it.
- It leaves less room for personal interpretation.

We distinguished **functional** and **non-functional** requirements and challenged teams to pick an existing app (a bus tracker, a photo editor, an e-commerce cart) and rewrite one of each using Sommerville's guidelines.

One group realized they couldn't specify performance goals until they'd interviewed users about expected delays. That moment was gold—it showed that real elicitation starts _after_ you think you're done.

## Requirements Elicitation Isn't a Script—It's a Dialogue

We explored five classic techniques for gathering requirements:

- Brainstorming
- Interviews
- JAD sessions
- Planning Poker
- The "Planning Game" (XP style)

But I emphasized: there's no silver bullet. The **best** elicitation method is the one that works with your stakeholder, culture, and team maturity. For junior teams, I recommended pairing developers with real users in structured conversations.

Students practiced interviews in pairs and tried converting spoken needs into formal specs. The misinterpretations that followed were a learning opportunity: your ears can't hear what your assumptions filter out.

## Validating and Verifying Early and Often

The class discussed how to **validate** requirements by asking:

- Are they realistic?
- Are they complete?
- Can we measure and test them?
- Are they consistent?

We introduced "fail fast" principles: if your requirements can't pass these checks, stop coding. Fix them first. Otherwise, you're just transferring risk downstream to testers or support.

I asked teams to retro their last assignments using these validation criteria. Some realized that their last "user story" lacked any testable acceptance criteria. Another learning moment.

## Bridging Requirements and Tests

This class culminated in something powerful: showing how tests are **not the final phase**, but the feedback loop that validates if our requirements were ever clear.

We covered:

- What makes a requirement testable
- Types of testing: unit, integration, UI, performance
- The concept of **TDD** and its alignment with requirement clarity

I showed a simple example:

**Requirement:** "User must receive an email within 2 minutes of registration."

We then wrote a test to simulate a registration and assert the email arrived. It showed students: a requirement is only clear when it's testable. If you can't write the test, rewrite the requirement.

## Beyond the Lecture

What I hoped they took home wasn't just how to write better specs, but how to _detect vagueness_, _ask sharper questions_, and _create alignment early_.

Anyone facilitating teams—whether at a startup or university—can replicate this lesson format. Just start with a real user story, walk through its breakdown into requirements, validate it, and build the tests.

It's not waterfall. It's **just being deliberate** with the foundations.

<div style="margin-bottom: 20px;">
<iframe src="https://www.slideshare.net/slideshow/embed_code/key/2cRKFh4w7E7J6J?startSlide=1" width="597" height="486" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px;max-width: 100%;" allowfullscreen></iframe> <div style="margin-bottom:5px"><strong> <a href="https://pt.slideshare.net/slideshow/unp-eng-software-aula-25/4328153" title="UnP Eng. Software - Aula 25" target="_blank">UnP Eng. Software - Aula 25</a> </strong> from <strong> <a href="https://www.slideshare.net/heliomedeiros" target="_blank">Hélio Medeiros</a> </strong></div></div>

---

_Posted as part of the Software Engineering course journal. Today we learned that requirements and tests aren't separate disciplines — they're complementary practices that ensure we build the right thing, the right way._

---

### **Series Navigation**

- **Introduction**: [Part 1 - Why Software Engineering?](../2010-02-24-software-engineering-purpose/)
- **Previous**: [Part 11 - Domain-Driven Design](../2010-05-15-domain-driven-design/)
- **Current**: Part 12 - Requirements & Testing
- **Next**: [Part 13 - Software Testing](../2010-05-29-software-testing/)
- **Complete series**: [Why Software Engineering?](../2010-02-24-software-engineering-purpose/) | [Taming Complexity](../2010-03-02-complexity-process/) | [Waterfall Model](../2010-03-10-waterfall-model/) | [Evolutionary Models](../2010-03-18-evolutionary-models/) | [Agile Mindset](../2010-03-26-agile-mindset/) | [Scrum Productivity](../2010-04-03-scrum-productivity/) | [Scrum Cycle](../2010-04-11-scrum-cycle/) | [XP Quality & Courage](../2010-04-19-xp-quality-courage/) | [XP Principles & Practices](../2010-05-01-xp-principles-practices/) | [XP in Practice](../2010-05-08-applying-xp-strategies/) | [Domain-Driven Design](../2010-05-15-domain-driven-design/) | [Requirements & Testing](../2010-05-22-requirements-validation-tests/) | [Software Testing](../2010-05-29-software-testing/)
