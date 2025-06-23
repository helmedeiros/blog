---
title: "Automate to Elevate: How Git Hooks and CI Made My Work Count"
date: 2014-04-13T10:00:00-03:00
author: Helio Medeiros
subtitle: Discover how Git hooks and Jenkins CI transformed chaotic Java enterprise development into a disciplined, automated workflow that caught errors early and built team confidence
tags:
  [
    "git",
    "automation",
    "git-hooks",
    "jenkins",
    "java",
    "maven",
    "jpa",
    "ejb",
    "continuous-integration",
  ]
categories: ["Development"]
---

## It's Not Just About Writing Code

In 2015, at RBS, our stack was 100% Java. We used JPA, EJB, and Maven—enterprise-style. But our feedback loops didn't match the complexity. You'd code a business feature, commit, and pray it didn't break something three modules away. Builds were long. Tests were sometimes skipped. And broken flows weren't always visible until later.

We had Jenkins running, but the discipline wasn't there. People forgot to run tests. Different machines had different settings. CI became a lottery.

What changed my game was introducing Git hooks and using Jenkins with purpose. Those two things made every commit a checkpoint, and every merge a moment of clarity—not chaos.

## Git Hooks for Java Projects

Java projects, especially large ones, benefit enormously from early feedback. And Git hooks helped enforce it right at commit time.

```bash
.git/hooks/pre-commit
```

I created a script like this:

```bash
#!/bin/sh
mvn clean verify
```

It ran the entire Maven lifecycle up to integration tests. That included compilation, unit tests, and static analysis tools like Checkstyle and PMD.

I also set up:

- `commit-msg` to ensure messages followed our `[JIRA-ID] Description` format
- `pre-push` to run `mvn verify` again just in case

| Hook         | Purpose                                  |
| ------------ | ---------------------------------------- |
| `pre-commit` | Catch syntax errors, test failures early |
| `commit-msg` | Enforce JIRA-compliant commit message    |
| `pre-push`   | Final check before sharing with Jenkins  |

It wasn't fancy—but it was powerful. No one merged broken code "by accident" anymore.

## Jenkins, Maven, and Continuous Integration

Jenkins was already there, but underused. We invested (thanks Lincolm and Andre) time to:

- Standardize `pom.xml` profiles so builds worked identically everywhere
- Run jobs per branch, not just `main`
- Integrate SonarQube for code quality
- Gate merges with Maven + test coverage thresholds

And Jenkins jobs weren't just triggers—they were truth. If your build broke, it blocked release. If SonarQube failed, it was treated like a bug.

| Jenkins Role        | Value Delivered                                 |
| ------------------- | ----------------------------------------------- |
| Build automation    | Consistency across dev environments             |
| Code quality checks | Static analysis via Maven plugins and SonarQube |
| Test execution      | Verified real behavior, not just local config   |

Together with Git hooks, Jenkins gave us layered safety. It wasn't about control—it was about confidence.

## Small Scripts, Big Confidence

In an enterprise Java setting with EJB and JPA, complexity is a given. Automation was how we handled it.

Git hooks ensured my commits were ready. Jenkins ensured they worked in the real world. Together, they made my contributions not only faster to review—but easier to trust.

This wasn't about being clever. It was about being consistent. In a team with many moving parts, consistency beats everything.

If you're in a Java shop and not automating your Maven flows yet—start. If you haven't wired Git to work for you—do it. Your future self will thank you.

Automate to elevate. Every step matters.
