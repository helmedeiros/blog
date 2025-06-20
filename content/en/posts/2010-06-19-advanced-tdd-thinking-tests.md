---
title: "Advanced TDD: Thinking in Tests"
date: 2010-06-19T09:00:00-03:00
tags: ["software engineering", "tdd", "testing", "java", "junit", "development"]
categories: ["Technology", "Agile"]
series: "Software Engineering Lectures"
slug: "advanced-tdd-thinking-tests"
summary: "In this lecture, we explored how Test-Driven Development (TDD) evolves from a tool to a mindset. Through live coding and real requirements, we worked on building a dynamic email templating system—purely from tests. Each line written was a decision validated or a bug prevented."
---

**Software Engineering Lectures - Part Part 16 of 19**

In this lecture, we explored how Test-Driven Development (TDD) evolves from a tool to a mindset. Through live coding and real requirements, we worked on building a dynamic email templating system—purely from tests. Each line written was a decision validated or a bug prevented. This session was not about coverage numbers. It was about clarity, feedback, and accountability.

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

## Intentional Programming

We emphasized **programming by intention**—writing code that reads like it was meant to exist. TDD makes you imagine that ideal API before you even implement it. That mindset shift is huge.

This allowed us to focus on _what the code should do_ instead of _how it will do it_. A big difference. One drives maintainability. The other often leads to premature optimization.

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

## Final Refactor and Learnings

We ended by cleaning up repeated `assertEquals(...)` calls using a helper method and `@Before` to share setup across tests. Our tests became readable, intentional, and expressive.

TDD doesn't start with tools. It starts with **mindset**. It challenges assumptions, narrows scope, and builds confidence.

Teaching students this way of thinking means they'll design not just for _correctness_, but for _resilience_.

Any team or facilitator can replicate this lesson in onboarding or skill growth sessions. Just start with a simple class, define behaviors, and test intentionally.

---

**Navigation:**

- **Previous:** [Part 15 - Unit Testing with JUnit](/en/posts/2010-06-12-junit-unit-testing/)
- **Next:** [Part 17 - Version Control: Don't Code Without It](/en/posts/2010-06-26-version-control-essential-foundation/)
- **Series:** [Software Engineering Lectures (17 parts)](/en/series/software-engineering-lectures/)
