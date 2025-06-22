---
title: "Caelum Day in Rio – Part 3: RESTful APIs with Sergio Junior and Luiz Costa"
date: 2009-11-10T14:00:00+00:00
draft: false
author: Helio Medeiros
subtitle: "Unlock the true power of REST architecture—move beyond simple HTTP APIs to discover HATEOAS and hypermedia-driven design that makes web services truly self-describing and evolvable"
tags:
  [
    "Caelum Day",
    "RESTful APIs",
    "REST",
    "Sergio Junior",
    "Luiz Costa",
    "Restfulie",
    "HATEOAS",
    "HTTP",
    "Hypermedia",
    "API Design",
    "Java",
    "Series",
    "Rio de Janeiro",
  ]
categories: ["Events", "Technology", "API Design", "Web Development"]
series: "Caelum Day 2009"
---

> **Series: Caelum Day 2009** | **Part 3 of 7** > _Comprehensive coverage of cutting-edge talks from Rio's premier Java event_

**Continuing the Caelum Day in Rio series**, today I want to share my impressions from **Sergio Junior and Luiz Costa's** talk on **RESTful APIs**.

## Demystifying REST

Before this talk, I had only a vague understanding of REST. They made it clear that **REST is not just about using HTTP verbs like GET and POST**, but about an architecture that emphasizes well-defined resources, proper use of HTTP methods, and most importantly, **hypermedia as the engine of application state (HATEOAS)**.

## Introduction to Restfulie

They introduced **Restfulie**, a library developed by Caelum to make it easier to build RESTful APIs in Java. What stood out to me was how Restfulie:

- **Simplifies object serialization** to XML or JSON
- **Adds navigational links** to responses so the client can discover the next available actions
- **Integrates smoothly with VRaptor**, which I had just seen in the previous session

For example, when returning an order, the API might include links to "pay" or "cancel" that guide the client through available transitions.

## Practical Example

They showed an example where a "Pedido" (Order) resource includes links to related actions:

```xml
<pedido>
  <produto>Curso de Java</produto>
  <link rel="payment" href="http://example.com/pedidos/1/pay"/>
  <link rel="cancel" href="http://example.com/pedidos/1/cancel"/>
</pedido>
```

On the client side, you could follow these links to trigger corresponding actions, without needing to know the URLs beforehand.

## Explore Restfulie

Restfulie is open source and you can explore the hypermedia library on GitHub:
[Restfulie on GitHub](https://github.com/caelum/restfulie)

## Final Thoughts

The talk really opened my eyes to the idea that building RESTful APIs is not just about mapping URLs to methods. It's about **designing an interface that guides the client through possible states**, making the application more intuitive and flexible.

I left the room inspired to study REST further and to try out Restfulie in future projects.

**Next in the series:** Nico Steppat's talk on NoSQL. See you soon!

---

### **Series Navigation**

- **Introduction**: [Caelum Day Overview](../2009-11-07-caelum-day-intro/)
- **Previous**: [Part 2 - VRaptor 3 Framework](../2009-11-09-caelum-day-part2-vraptor3/)
- **Current**: Part 3 - RESTful APIs
- **Next**: [Part 4 - NoSQL Databases](../2009-11-11-caelum-day-part4-nosql/)
- **Complete series**: [Cloud Computing](../2009-11-08-caelum-day-part1-cloud-fabio-kung/) | [VRaptor 3](../2009-11-09-caelum-day-part2-vraptor3/) | [NoSQL](../2009-11-11-caelum-day-part4-nosql/) | [Flex](../2009-11-12-caelum-day-part5-flex/) | [Java Persistence](../2009-11-13-caelum-day-part6-java-persistence/) | [Technical Leadership](../2009-11-14-caelum-day-final-leadership-phillip-calcado/)
