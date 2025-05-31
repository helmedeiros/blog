---
title: "Mike Keith - Java EE 6: A Major Evolution"
author: helio
layout: post
date: 2009-11-20T14:22:51+00:00
idptt_tweeted:
series: "TDC Rio 2009"
categories:
  - Eventos
tags:
  - EJB 3.1
  - Eventos
  - Global Code
  - J2EE
  - Mike Keith
  - TDC 2009
---

> **Series: TDC Rio 2009** | **Part 1 of 2** > _Key insights from Brazil's premier Java conference_

![Mike Keith's talk](../../uploads/2009/11/dsc00699.jpg)

Mike Keith's talk started around 11 a.m., just after the coffee break. He kicked off with a light tone and a bit of humor about the long wait between Java version releases. One early slide showed a bold phrase:

> "Or maybe you don't care because Microsoft will kill Java anyway."

The jab got a few laughs — but also set the tone for a serious point: despite criticisms, **Java EE 6** was evolving, and this release brought real improvements that deserved attention.

## Java EE 6: More Modular, Less XML

Mike walked through some of the major updates in the new specification. One of the most welcome changes was the **reduction of XML configuration**. With the introduction of **annotations (@Annotation)**, a lot of previously external settings could now live directly in the code.

```java
@WebServlet("/myRoute")
public class MyServlet extends HttpServlet {
    // ...
}
```

Previously, this would have required a chunk of XML in `web.xml`. Now, it's all embedded and more intuitive.

## Annotations and Modularity: Ending Hidden Coupling

Annotations also helped expose **which behaviors and dependencies are active** in each class. This made hidden coupling — where key logic lived in invisible XML — far less likely.

This shift was also aligned with popular frameworks like Spring, JSF, and Struts, which had already embraced annotation-driven configuration.

## Asynchronous Servlets (Async Processing)

A particularly exciting update was the addition of **asynchronous support for Servlets**. Rather than blocking a server thread while waiting for a long-running task (like a remote API call), servlets could now offload the task and continue handling new requests.

> In plain terms: the server doesn't sit idle anymore — it gets more done with fewer resources.

Mike reminded us that while powerful, async servlets introduce complexity, and developers must take care to avoid race conditions and concurrency bugs.

## EJB 3.1: Time for a Comeback?

When Mike mentioned **EJB**, I expected some eye-rolling. But he surprised us with updates that made **EJB 3.1** feel relevant again — even modern.

Highlights included:

- **Lightweight EJBs** that could run outside full enterprise containers
- Optional use of interfaces
- Better integration with plain Java SE environments

The room seemed genuinely curious — maybe because EJB was finally shedding its baggage.

## JPA and Afternoon Discussions

While **JPA (Java Persistence API)** was only briefly discussed during the talk, the interest it generated was so strong that it became a side conversation later in the afternoon.

For those unfamiliar, JPA provides a standard for object-relational mapping in Java. Instead of raw SQL, we define Java classes and annotations that represent database entities.

## Dependency Injection (JSR 330)

Another highlight was **JSR 330**, which formalized the idea of **dependency injection** — a technique long popularized by Spring and others.

> The idea is to shift object creation to a container, reducing coupling and simplifying testing.

This marked another step toward aligning the Java EE platform with modern development practices.

---

## An Optimistic Outlook

Mike closed with an encouraging message: many of these new features were already available in beta or public spec drafts and were expected to become official by **December 2009**.

The takeaway was clear: **Java EE 6 wasn't just keeping up — it was cleaning up**. The platform was becoming more modular, productive, and responsive to developers' real needs.

---

_Posted the same day as Mike Keith's talk at TDC Rio 2009._

**Next in this series:** [Rod Johnson on Java EE trends and the next 5 years](/posts/2009-11-25-rod-johnson-tendencias-em-java-ee-como-serao-os-proximos-5-anos/)
