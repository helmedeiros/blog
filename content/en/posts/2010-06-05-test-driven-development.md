---
title: "Test-Driven Development: Building the Right Thing the Right Way"
author: helio
date: 2010-06-05T14:30:22+00:00
description: "Reflections on the fourteenth and final Software Engineering lecture, exploring Test-Driven Development as a design methodology that goes beyond testing to shape how we think about building software."
categories:
  - Testing
  - Development Methodology
  - Education
tags:
  - Software Engineering
  - Test-Driven Development
  - TDD
  - Red-Green-Refactor
  - Acceptance TDD
  - ATDD
  - Design
  - Quality
  - UnP
  - Teaching
  - software-engineering-series
---

> **Series: Software Engineering Fundamentals** | **Part 14 of 14** > _Delivered at Universidade Potiguar (UnP) in 2010_

In this session, we explored **Test-Driven Development (TDD)** beyond the usual catchphrases. We focused on its impact on software quality, code evolution, and how testing is not a phase—but a development mindset. This was not a class to teach syntax; it was about how to think like a developer who questions assumptions and encodes confidence.

TDD is not about writing tests. It's about designing with purpose.

---

## Getting to the Root: Correct Problem, Correct Solution

We began by analyzing a classic trap in software projects: building beautiful solutions for the wrong problem. TDD interrupts this by forcing you to define expected behavior before writing logic. This pushes clarity before complexity.

Students were asked to refactor an existing method only after writing failing tests. The goal was to make them **rethink design through tests** instead of the other way around.

Here's an example test we worked through:

```java
@Test
public void testCalculateTotalWithDiscount() {
    Cart cart = new Cart();
    cart.add(new Product("Book", 50));
    cart.applyDiscount("STUDENT10");

    assertEquals(45, cart.getTotal());
}
```

Before even coding `applyDiscount`, students needed to decide:

- What does a discount look like?
- Who qualifies for it?
- What's the correct final state?

---

## TDD's Cycle: Red-Green-Refactor

We then studied the cycle that anchors TDD: **Red-Green-Refactor**. Students practiced each step with precision:

1. **Red**: Write a failing test.
2. **Green**: Write the minimal code to make it pass.
3. **Refactor**: Improve code without changing behavior.

An early exercise involved string validation:

```python
def test_should_not_allow_empty_username():
    with pytest.raises(ValueError):
        User(username="")

# Start with red, implement just enough to pass:
class User:
    def __init__(self, username):
        if username == "":
            raise ValueError("Username required")
```

Refactoring came later: extracting validation, adding constraints, removing duplication.

---

## Activities That Reinforce the Loop

I introduced a classroom kata: a pricing system for ticket types (student, regular, senior). Each student wrote a single failing test, passed it, and refactored—then passed it to the next group member to repeat the cycle.

This created code that was born and evolved through **deliberate constraints**, not overengineering. At the end of 30 minutes, we had a pricing engine that handled four rules, had no duplication, and was fully covered by tests.

Another session exercise revolved around command-line calculator logic:

```ruby
describe Calculator do
  it "adds two numbers" do
    calc = Calculator.new
    expect(calc.add(2, 3)).to eq(5)
  end
end
```

Even simple examples teach how to clarify behavior through tests, not by guessing at future needs.

---

## Acceptance TDD: Ensuring We Build the Right Thing

While TDD focuses on design, we also covered **Acceptance TDD (ATDD)**—validating that what we build aligns with stakeholder expectations. Students wrote acceptance tests for a search feature with constraints like "must return no more than 10 results in under 1 second."

They quickly saw that the test itself became a **requirement artifact**, useful for alignment between devs, QA, and users.

We reviewed what happens when no such alignment exists: features built with misunderstood logic, poorly tested under edge conditions, or lacking validation for the true need.

Facilitators and team leads can use these techniques during backlog refinement. If you can't express the expected result as an executable test, you may not understand the need yet.

---

## Final Thoughts

My goal with this class wasn't just to teach TDD as a methodology—it was to make students internalize it as a feedback and design strategy.

TDD helps developers stay grounded: no big jumps, no wasted code. It's a loop of discovery and simplification. And in a world where every change introduces risk, **test-first design is your guardrail**.

<div style="margin-bottom: 20px;">
<iframe src="https://www.slideshare.net/slideshow/embed_code/key/xBnDqOwtdg2Njq?startSlide=1" width="597" height="486" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px;max-width: 100%;" allowfullscreen></iframe> <div style="margin-bottom:5px"><strong> <a href="https://pt.slideshare.net/slideshow/unp-eng-software-aula-27/4487762" title="UnP Eng. Software - Aula 27" target="_blank">UnP Eng. Software - Aula 27</a> </strong> from <strong> <a href="https://www.slideshare.net/heliomedeiros" target="_blank">Hélio Medeiros</a> </strong></div></div>
---

_Posted as part of the Software Engineering course journal. Today we learned that TDD isn't just about testing—it's about designing with confidence and building systems that evolve through deliberate, validated steps._

## Series Conclusion

This concludes our **Software Engineering Fundamentals** series, delivered at Universidade Potiguar (UnP) in 2010. Throughout these fourteen lectures, we explored the evolution from traditional process-heavy approaches to modern agile methodologies, culminating in sophisticated approaches that bridge design, requirements, validation, and quality through comprehensive testing practices and test-driven development.

**Throughout this series, we explored**:

1. **[Why Software Engineering?](../2010-02-24-software-engineering-purpose/)**: Building with purpose beyond code
2. **[Taming Complexity](../2010-03-02-complexity-process/)**: When process helps and when it hurts
3. **[Waterfall Model](../2010-03-10-waterfall-model/)**: When following the recipe fails
4. **[Evolutionary Models](../2010-03-18-evolutionary-models/)**: Learning to adapt and evolve
5. **[Agile Mindset](../2010-03-26-agile-mindset/)**: Less stress, more delivery
6. **[Scrum Productivity](../2010-04-03-scrum-productivity/)**: Finding your team's rhythm
7. **[Scrum Cycle](../2010-04-11-scrum-cycle/)**: From planning to working software
8. **[XP Quality & Courage](../2010-04-19-xp-quality-courage/)**: Quality through courage
9. **[XP Principles & Practices](../2010-05-01-xp-principles-practices/)**: Sustainable excellence
10. **[XP in Practice](../2010-05-08-applying-xp-strategies/)**: Real strategies for real teams
11. **[Domain-Driven Design](../2010-05-15-domain-driven-design/)**: Building software that speaks business
12. **[Requirements & Testing](../2010-05-22-requirements-validation-tests/)**: Clear specs, meaningful validation
13. **[Software Testing](../2010-05-29-software-testing/)**: Fidelity, quality, and system evolution
14. **Test-Driven Development**: Building the right thing the right way (Final)

Each lecture built upon previous concepts while introducing practical frameworks that remain relevant today. **Software engineering** is about more than following methodologies—it's about developing judgment, fostering collaboration, maintaining focus on delivering real value, and ultimately creating software that truly serves its intended purpose.

From understanding why software engineering matters to implementing test-driven development practices that ensure both quality and proper design, this journey demonstrates that great software comes from great teams, supported by thoughtful processes, sustained by continuous learning, guided by clear requirements, validated through strategic testing practices, and developed through disciplined, test-first approaches that build confidence into every line of code.

---

### **Series Navigation**

- **Introduction**: [Part 1 - Why Software Engineering?](../2010-02-24-software-engineering-purpose/)
- **Previous**: [Part 13 - Software Testing](../2010-05-29-software-testing/)
- **Current**: Part 14 - Test-Driven Development (Final)
- **Complete series**: [Why Software Engineering?](../2010-02-24-software-engineering-purpose/) | [Taming Complexity](../2010-03-02-complexity-process/) | [Waterfall Model](../2010-03-10-waterfall-model/) | [Evolutionary Models](../2010-03-18-evolutionary-models/) | [Agile Mindset](../2010-03-26-agile-mindset/) | [Scrum Productivity](../2010-04-03-scrum-productivity/) | [Scrum Cycle](../2010-04-11-scrum-cycle/) | [XP Quality & Courage](../2010-04-19-xp-quality-courage/) | [XP Principles & Practices](../2010-05-01-xp-principles-practices/) | [XP in Practice](../2010-05-08-applying-xp-strategies/) | [Domain-Driven Design](../2010-05-15-domain-driven-design/) | [Requirements & Testing](../2010-05-22-requirements-validation-tests/) | [Software Testing](../2010-05-29-software-testing/) | Test-Driven Development
