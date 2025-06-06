---
title: "Advanced TDD: Thinking in Tests"
date: 2010-06-19T09:00:00-03:00
tags: ["software engineering", "tdd", "testing", "java", "junit", "development"]
categories: ["Software Engineering"]
series: ["Software Engineering Lectures"]
slug: "advanced-tdd-thinking-tests"
summary: "In this lecture, we explored how Test-Driven Development (TDD) evolves from a tool to a mindset. Through live coding and real requirements, we worked on building a dynamic email templating system—purely from tests. Each line written was a decision validated or a bug prevented."
---

**Software Engineering Lectures - Part 16 of 16**

![Placeholder for current image](path/to/image-placeholder.jpeg)

In this lecture, we explored how Test-Driven Development (TDD) evolves from a tool to a mindset. Through live coding and real requirements, we worked on building a dynamic email templating system—purely from tests. Each line written was a decision validated or a bug prevented. This session was not about coverage numbers. It was about clarity, feedback, and accountability.

---

## From Requirements to Tests

We started with a deceptively simple request: create a system that sends emails using templates and replaces variables like `${firstName}` and `${lastName}`. Most students wanted to jump straight to implementation. Instead, I asked them to **list the required tests first**.

We learned to convert vague tasks into crisp, executable validations:

```java
@Test
public void replacesSingleVariable() {
    Template template = new Template("Hello, ${name}");
    template.set("name", "Reader");
    assertEquals("Hello, Reader", template.render());
}
```

This is more than a unit test—it's a specification. With it, the design becomes intentional and the requirements unambiguous.

---

## Red First, Always

From this test, the compiler forces us forward: the class doesn't exist, the constructor is missing, the method is undefined. All of that is expected. We then build only enough code to satisfy the test.

Here's the initial implementation:

```java
public class Template {
    public Template(String text) {}
    public void set(String var, String value) {}
    public String render() {
        return null;
    }
}
```

Yes, this will fail. And that's the point. TDD begins at **red**.

Then we hardcode the expected result:

```java
public String render() {
    return "Hello, Reader";
}
```

It passes. Temporarily. But now we break it with a second test.

---

## Triangulation and the First Refactor

Next, we wrote a variation of the test to prove the hardcoded solution isn't enough.

```java
@Test
public void replacesWithDifferentValue() {
    Template template = new Template("Hello, ${name}");
    template.set("name", "Guest");
    assertEquals("Hello, Guest", template.render());
}
```

Now we need to remove hardcoded values and actually handle variables. Eventually, we reached this:

```java
public class Template {
    private String text;
    private Map<String, String> values = new HashMap<>();

    public Template(String text) {
        this.text = text;
    }

    public void set(String var, String value) {
        values.put(var, value);
    }

    public String render() {
        String result = text;
        for (var entry : values.entrySet()) {
            String regex = "\$\{" + entry.getKey() + "\}";
            result = result.replaceAll(regex, entry.getValue());
        }
        return result;
    }
}
```

We arrived here through **triangulation**: iteratively adding tests to force more generic solutions.

---

## Intentional Programming

We emphasized **programming by intention**—writing code that reads like it was meant to exist. TDD makes you imagine that ideal API before you even implement it. That mindset shift is huge.

This allowed us to focus on _what the code should do_ instead of _how it will do it_. A big difference. One drives maintainability. The other often leads to premature optimization.

---

## Predicting and Handling Failures

Once most tests passed, we revisited failure cases. What if a variable isn't set?

```java
@Test(expected=MissingValueException.class)
public void throwsErrorIfVariableMissing() {
    new Template("Hello, ${name}").render();
}
```

We added logic to detect unrendered placeholders and raise a custom exception:

```java
if (result.matches(".*\$\{.+\}.*")) {
    throw new MissingValueException();
}
```

Through this, students learned not just to validate happy paths, but also to **intentionally guard against faults**.

---

## Final Refactor and Learnings

We ended by cleaning up repeated `assertEquals(...)` calls using a helper method and `@Before` to share setup across tests. Our tests became readable, intentional, and expressive.

TDD doesn't start with tools. It starts with **mindset**. It challenges assumptions, narrows scope, and builds confidence.

Teaching students this way of thinking means they'll design not just for _correctness_, but for _resilience_.

Any team or facilitator can replicate this lesson in onboarding or skill growth sessions. Just start with a simple class, define behaviors, and test intentionally.

---

## Series Conclusion

And with this, we conclude our comprehensive journey through software engineering fundamentals. Over these 16 lectures, we've covered the complete spectrum from basic principles to advanced practices:

**Part 1 - [Why Software Engineering?](/en/posts/2010-02-24-software-engineering-purpose/)** - Understanding the discipline and its importance

**Part 2 - [Taming Complexity with Process](/en/posts/2010-03-02-complexity-process/)** - Managing software complexity through structured approaches

**Part 3 - [The Waterfall Model](/en/posts/2010-03-10-waterfall-model/)** - Traditional sequential development methodology

**Part 4 - [Evolutionary Development Models](/en/posts/2010-03-18-evolutionary-models/)** - Iterative and incremental approaches

**Part 5 - [The Agile Mindset](/en/posts/2010-03-26-agile-mindset/)** - Principles and values of agile development

**Part 6 - [Scrum and Productivity](/en/posts/2010-04-03-scrum-productivity/)** - Framework for agile project management

**Part 7 - [The Scrum Development Cycle](/en/posts/2010-04-11-scrum-cycle/)** - Detailed look at sprints and ceremonies

**Part 8 - [Extreme Programming: Quality and Courage](/en/posts/2010-04-19-xp-quality-courage/)** - XP values and mindset

**Part 9 - [XP Principles and Practices](/en/posts/2010-05-01-xp-principles-practices/)** - Core XP practices and techniques

**Part 10 - [Applying XP: Strategies in Practice](/en/posts/2010-05-08-applying-xp-strategies/)** - Real-world XP implementation

**Part 11 - [Domain-Driven Design](/en/posts/2010-05-15-domain-driven-design/)** - Modeling complex business domains

**Part 12 - [Requirements and Validation through Tests](/en/posts/2010-05-22-requirements-validation-tests/)** - Testing as requirements specification

**Part 13 - [Software Testing Fundamentals](/en/posts/2010-05-29-software-testing/)** - Testing types, levels, and strategies

**Part 14 - [Test-Driven Development](/en/posts/2010-06-05-test-driven-development/)** - TDD methodology and practices

**Part 15 - [Unit Testing with JUnit](/en/posts/2010-06-12-junit-unit-testing/)** - Practical unit testing implementation

**Part 16 - [Advanced TDD: Thinking in Tests](/en/posts/2010-06-19-advanced-tdd-thinking-tests/)** - TDD as mindset and design tool (Final)

This series has taken us from understanding the "why" of software engineering to mastering advanced development practices. The journey shows how the field evolved from rigid processes to adaptive methodologies, always keeping quality, collaboration, and customer value at the center.

The principles and practices covered here form the foundation for building robust, maintainable software systems that truly serve their users and stand the test of time.

---

**Navigation:**

- **Previous:** [Part 15 - Unit Testing with JUnit](/en/posts/2010-06-12-junit-unit-testing/)
- **Series:** [Software Engineering Lectures (16 parts)](/en/series/software-engineering-lectures/)
