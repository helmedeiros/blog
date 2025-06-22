---
title: "Testing Software: Fidelity, Quality, and System Evolution"
author: helio
date: 2010-05-29 14:30:22+00:00
description:
  Reflections on the thirteenth Software Engineering lecture, exploring
  software testing as a strategic design activity embedded throughout real development
  processes.
categories:
  - Development
tags:
  - Software Engineering
  - Software Testing
  - Unit Testing
  - Integration Testing
  - Test-Driven Development
  - Quality Assurance
  - Test Pyramid
  - UnP
  - Teaching
  - software-engineering-series
series: Software Engineering Fundamentals
subtitle: Master comprehensive testing strategies—discover how unit, integration, and system testing work together to create robust verification pyramids that catch bugs early and build user confidence
---

> **Series: Software Engineering Fundamentals** | **Part Part 13 of 19** > _Delivered at Universidade Potiguar (UnP) in 2010_

In this lecture, we dived into **Software Testing**—not as a boring list of types or QA certifications, but as a creative, strategic activity embedded in every stage of real software development. I reminded the class that testing isn't a gatekeeping step, it's part of the design process. Every good engineer should see testing as part of their toolkit, not someone else's responsibility.

We started with a provocative idea: _"Testing doesn't prove a system works. It proves that it doesn't always fail."_ That resonated because it shifts the burden: we're not chasing perfection, we're designing confidence.

## Testing as a Tool for Understanding

We introduced testing as a **learning mechanism**. Students were asked to list five reasons why testing matters. Among their answers: "to discover bugs," "to verify if the system works," "to gain confidence."

We discussed how tests help expose **ambiguities in requirements**, **flaws in integration**, and even **usability holes**. I showed how a test-first mindset clarifies scope before you write the first line of code.

Here's a basic unit test for a class that calculates delivery time:

```java
@Test
public void testExpressDeliveryCalculation() {
    DeliveryCalculator calculator = new DeliveryCalculator();
    int days = calculator.calculate("express", 120);
    assertEquals(1, days);
}
```

This simple test forces you to define what "express delivery" means and what rules drive its calculation. A good test reveals missing business logic before it becomes customer frustration.

## Types of Tests and When to Use Them

We covered various test types: **unit, integration, system, acceptance, UI, performance, security**. But instead of giving definitions, I challenged each team to match a test type to a bug they had faced in the past. It created lively conversations.

We talked about test responsibility too:

- **Developers** write unit and integration tests.
- **Test teams** handle system, UI, and exploratory testing.
- **Users** validate via acceptance testing.

To reinforce this, we wrote a functional test for login flow:

```python
def test_user_login():
    user = create_user("maria@example.com", "secure123")
    response = client.post("/login", data={"email": "maria@example.com", "password": "secure123"})
    assert response.status_code == 200
    assert b"Welcome, Maria" in response.data
```

Functional tests like this one focus on what the system should do, regardless of internal implementation.

## Building Trust Through Testing

I introduced the class to the **"Testing Ice Cream Cone"** problem—too many UI tests, too few unit tests. We reflected on the **Test Pyramid** and how to balance effort for speed and reliability.

Students analyzed a system they were building and proposed how to refactor tests following a more scalable approach. One group realized they had no performance tests, even though their app relied on fast response time.

We then discussed how to evolve a test suite to support system growth. I introduced this TDD-style test for an evolving pricing rule:

```ruby
describe PricingEngine do
  it "applies 10% discount for students" do
    price = PricingEngine.new(base: 100, user_type: "student").final_price
    expect(price).to eq(90)
  end
end
```

Even a single failing test like this one can steer architectural decisions and refactoring.

## Exercises That Make Testing Tangible

To wrap the session, I split the class into test squads. Each team had to build a minimal test suite for a fake e-commerce feature using only:

- One requirement
- One user flow
- One key constraint (e.g., response time < 2s)

They shared strategies, tool choices, and how tests helped them find bugs they didn't even know existed. We ended by compiling a list of **"bugs found through tests"**—a visual reminder that tests are not a cost, but a lens.

Facilitators can apply the same exercise in onboarding, retrospectives, or hackathons. It encourages teams to take ownership of testing—not as checklist, but as insight.

<div style="margin-bottom: 20px;">
<iframe src="https://www.slideshare.net/slideshow/embed_code/key/2djxpcSYwJnMsu?startSlide=1" width="597" height="486" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px;max-width: 100%;" allowfullscreen></iframe> <div style="margin-bottom:5px"><strong> <a href="https://pt.slideshare.net/slideshow/un-p-aula-26/4328245" title="UnP Eng. Software - Aula 26" target="_blank">UnP Eng. Software - Aula 26</a> </strong> from <strong> <a href="https://www.slideshare.net/heliomedeiros" target="_blank">Hélio Medeiros</a> </strong></div></div>

---

_Posted as part of the Software Engineering course journal. Today we learned that testing isn't about proving perfection—it's about designing confidence and building systems that evolve gracefully._

---

### **Series Navigation**

- **Introduction**: [Part 1 - Why Software Engineering?](../2010-02-24-software-engineering-purpose/)
- **Previous**: [Part 12 - Requirements & Testing](../2010-05-22-requirements-validation-tests/)
- **Next**: [Part 14 - Test-Driven Development](../2010-06-05-test-driven-development/)
- **Current**: Part 13 - Software Testing
- **Complete series**: [Why Software Engineering?](../2010-02-24-software-engineering-purpose/) | [Taming Complexity](../2010-03-02-complexity-process/) | [Waterfall Model](../2010-03-10-waterfall-model/) | [Evolutionary Models](../2010-03-18-evolutionary-models/) | [Agile Mindset](../2010-03-26-agile-mindset/) | [Scrum Productivity](../2010-04-03-scrum-productivity/) | [Scrum Cycle](../2010-04-11-scrum-cycle/) | [XP Quality & Courage](../2010-04-19-xp-quality-courage/) | [XP Principles & Practices](../2010-05-01-xp-principles-practices/) | [XP in Practice](../2010-05-08-applying-xp-strategies/) | [Domain-Driven Design](../2010-05-15-domain-driven-design/) | [Requirements & Testing](../2010-05-22-requirements-validation-tests/) | Software Testing | [Test-Driven Development](../2010-06-05-test-driven-development/) | [Unit Testing with JUnit](../2010-06-12-junit-unit-testing/)
