---
title: "Unit Testing with JUnit: Clarity Before Complexity"
author: helio
date: 2010-06-12T14:30:22+00:00
description: "Reflections on the fifteenth and final Software Engineering lecture, exploring unit testing with JUnit as a structured approach to validation, feedback loops, and design improvement."
categories:
  - Testing
  - Unit Testing
  - Education
tags:
  - Software Engineering
  - Unit Testing
  - JUnit
  - Test Automation
  - Test Fixtures
  - Test Cases
  - Design
  - Quality
  - UnP
  - Teaching
  - software-engineering-series
---

> **Series: Software Engineering Fundamentals** | **Part 15 of 17** > _Delivered at Universidade Potiguar (UnP) in 2010_

In this lecture, we built on our previous exploration of TDD by diving deeper into **unit testing**, using JUnit to demonstrate how structured validation turns vague logic into predictable behavior. It was not just about testing—it was about creating feedback loops, improving design, and building safer systems with fewer surprises.

I wanted the class to realize: testing early isn't just defensive programming. It's a way to guide development through intent.

---

## Before Frameworks: Raw Testing and Its Limits

To begin, we returned to a time before JUnit. I demonstrated how a method that calculates square roots can be tested using plain Java. We used this `Calculadora` class:

```java
public final class Calculadora {
    public static int qualARaiz(int x) {
        int guess = 1;
        while (guess * guess < x) {
            guess++;
        }
        return guess;
    }
}
```

And tested it manually:

```java
public static void main(String[] args) {
    System.out.println(Calculadora.qualARaiz(0));
    System.out.println(Calculadora.qualARaiz(9));
    System.out.println(Calculadora.qualARaiz(100));
}
```

The problem? There's no way to automatically detect failures or track test results over time. It's fragile, manual, and quickly becomes a bottleneck.

---

## Enter JUnit: Naming, Fixtures, and Automation

We then introduced JUnit—the Java testing framework co-created by Kent Beck. We defined the core components:

- **Fixture**: setup data used in tests
- **Test Case**: a single method validation
- **Test Suite**: collection of test cases
- **Test Runner**: tool to execute and report

The class wrote its first annotated test:

```java
@Test
public void testCalculateRoot() {
    assertEquals(3, Calculadora.qualARaiz(9));
    assertEquals(10, Calculadora.qualARaiz(100));
}
```

We discussed the importance of naming and structure. When tests describe behavior and fail clearly, they become executable documentation.

---

## Building Examples with Arithmetic and Conditions

We added new business logic using the `Aritmetica` class:

```java
public class Aritmetica {
    public static int soma(int i, int j) {
        return i + j;
    }

    public static boolean isPositivo(int numero) {
        return numero > 0;
    }
}
```

And tested it with:

```java
@Test
public void testAddition() {
    assertEquals(4, Aritmetica.soma(2,2));
    assertEquals(-15, Aritmetica.soma(-10, -5));
}

@Test
public void testIsPositive() {
    assertTrue(Aritmetica.isPositivo(5));
    assertFalse(Aritmetica.isPositivo(-10));
}
```

Here, students learned that **a single responsibility** in a method makes it easier to validate. And **booleans** can't lie—tests reveal logic flaws immediately.

---

## Modeling Behavior with the Counter Class

In the second half of the class, we introduced a practical modeling example: a `Contador` used in a queue system.

```java
public class Contador {
    private int count = 0;

    public int increment() {
        return ++count;
    }

    public int decrement() {
        return --count;
    }
}
```

And its corresponding tests:

```java
@Before
public void setUp() {
    counter = new Contador();
}

@Test
public void testIncrement() {
    assertEquals(1, counter.increment());
    assertEquals(2, counter.increment());
}

@Test
public void testDecrement() {
    assertEquals(-1, counter.decrement());
}
```

Students practiced creating tests that maintain state across executions. The **setUp** method was introduced to isolate test logic from instantiation noise.

---

## Activities and Takeaways

We ended with a group challenge: implement and test a class for validating voting eligibility based on age and citizenship. Each team had to define:

- What a valid user looks like
- Which rules apply
- How to test edge cases and constraints

Through peer review, students saw the **difference between testing logic and behavior**. They gained insight on how test structure improves maintainability and collaboration.

Any team or facilitator can replicate this lesson in onboarding or skill growth sessions. Just start with a simple class, define behaviors, and test intentionally.

<div style="margin-bottom: 20px;">
<iframe src="https://www.slideshare.net/slideshow/embed_code/key/KgnPDn6r42boUg?startSlide=1" width="597" height="486" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px;max-width: 100%;" allowfullscreen></iframe> <div style="margin-bottom:5px"><strong> <a href="https://pt.slideshare.net/slideshow/unp-eng-software-aula-28/4487801" title="UnP Eng. Software - Aula 28" target="_blank">UnP Eng. Software - Aula 28</a> </strong> from <strong> <a href="https://www.slideshare.net/heliomedeiros" target="_blank">Hélio Medeiros</a> </strong></div></div>

---

_Posted as part of the Software Engineering course journal. Today we learned that unit testing with JUnit isn't just about catching bugs—it's about building systems that communicate their intent clearly and evolve safely._

---

### **Series Navigation**

- **Introduction**: [Part 1 - Why Software Engineering?](../2010-02-24-software-engineering-purpose/)
- **Previous**: [Part 14 - Test-Driven Development](../2010-06-05-test-driven-development/)
- **Next**: [Part 16 - Advanced TDD: Thinking in Tests](../2010-06-19-advanced-tdd-thinking-tests/)
- **Current**: Part 15 - Unit Testing with JUnit
- **Complete series**: [Why Software Engineering?](../2010-02-24-software-engineering-purpose/) | [Taming Complexity](../2010-03-02-complexity-process/) | [Waterfall Model](../2010-03-10-waterfall-model/) | [Evolutionary Models](../2010-03-18-evolutionary-models/) | [Agile Mindset](../2010-03-26-agile-mindset/) | [Scrum Productivity](../2010-04-03-scrum-productivity/) | [Scrum Cycle](../2010-04-11-scrum-cycle/) | [XP Quality & Courage](../2010-04-19-xp-quality-courage/) | [XP Principles & Practices](../2010-05-01-xp-principles-practices/) | [XP in Practice](../2010-05-08-applying-xp-strategies/) | [Domain-Driven Design](../2010-05-15-domain-driven-design/) | [Requirements & Testing](../2010-05-22-requirements-validation-tests/) | [Software Testing](../2010-05-29-software-testing/) | [Test-Driven Development](../2010-06-05-test-driven-development/) | [Unit Testing with JUnit](../2010-06-12-junit-unit-testing/) | [Advanced TDD: Thinking in Tests](../2010-06-19-advanced-tdd-thinking-tests/)
