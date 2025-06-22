---
title: "SOLID Principles and the Mess We're In"
date: 2019-05-04T14:00:00-03:00
author: Helio Medeiros
subtitle: Escape microservices hell by applying SOLID principles at system level—transforming distributed chaos into bounded contexts with clear responsibilities and sustainable architecture
tags:
  [
    "solid principles",
    "microservices",
    "system design",
    "architecture",
    "software engineering",
    "distributed systems",
    "bounded contexts",
    "domain-driven design",
  ]
categories: ["Technology", "Architecture"]
---

We've been here before. The industry goes through cycles. Centralization, decentralization. Monoliths, microservices. But if you're reading this, you're probably navigating through a microservices transformation or, worse, living with the aftermath of a poorly executed one. And you're wondering how we ended up in a distributed mess.

To understand that, let's step back a bit. Object orientation taught us to split our problems into small pieces that interact through message passing. These objects are lightweight, reusable, and chatty. That works fine within a process. But put a network between those objects and everything changes.

Martin Fowler once said: "The First Law of Distributed Object Design: Don't."

So how did we get from that to a world where every architecture deck has a slide titled "Our Microservices Landscape"?

## Why Microservices, Anyway?

Microservices, for all the hype and vague definitions, do one thing well: they force boundaries. Instead of thousands of classes mashed together, you (ideally) get independently deployable units with their own teams, lifecycles, and responsibilities.

The key word here is _ideally_. In reality, most companies went from monoliths with no boundaries to distributed systems with no boundaries. All the coupling, now with latency.

The benefits of microservices exist—but only when they're treated as coarse-grained services, not distributed objects. That's where SOLID principles come in.

## Bounded Contexts and the Curse of "Micro"

When services are too small, they become what objects were: dependent, chatty, fragile. If you're rolling out three services just to rename a field, you've built a distributed object system, not a service-oriented one.

The solution isn't to abandon modularity, but to reframe how we define modules. Enter Bounded Contexts—an idea from Domain-Driven Design that encourages us to cluster models, vocabulary, and behavior into clear boundaries.

Start with language. If your team says "booking" in one place and "order" in another to mean the same thing, you've found a boundary. If "user" means five different things across your codebase, draw the lines.

Bounded Contexts give us a natural place to apply SOLID.

## Applying SOLID to Microservices

Let's not treat SOLID as a class-level concern. Think of it as a **systemic design heuristic**. Here's how each principle can help tame your microservice hell:

| Principle | System Interpretation                                                    | Example                                                                   |
| --------- | ------------------------------------------------------------------------ | ------------------------------------------------------------------------- |
| SRP       | Each service should do one thing well                                    | Don't combine payment processing and customer support in the same service |
| OCP       | Add new behaviors without changing existing contracts                    | Use feature flags, API versioning                                         |
| LSP       | Replace old services with new ones without breaking consumers            | Blue-green deploys with backward-compatible responses                     |
| ISP       | Clients shouldn't be forced to depend on data or logic they don't need   | Create specialized APIs for frontend/mobile/reporting needs               |
| DIP       | Services depend on abstractions (events, contracts), not implementations | Publish domain events, don't make direct RPC calls                        |

## Smells Revisited

The usual suspects—rigidity, fragility, immobility, viscosity—are present in spades in microservices.

- **Rigidity**: Service A changing breaks Service B? You're not versioning correctly.
- **Fragility**: Feature flags mixed with config toggles and conditional logic? Time to rethink your release strategy.
- **Immobility**: Want to reuse logic from a service but it's tied to Kafka, Postgres, and a metrics backend? Extract the domain, leave the infrastructure.
- **Viscosity**: New endpoints pile up because the right abstraction is too painful to change? That's architectural viscosity.

The same principles that made your code more maintainable apply here. But now, the cost of breaking them isn't just a failing unit test—it's a production incident.

## The Growth Path

Startups don't need microservices. They need product validation.

Scale-ups need to survive complexity and entropy. That's when you move from throwing code into the void to crafting systems with boundaries. SOLID isn't enough, but it's foundational.

Web-scale companies have different problems—performance, cost, latency—but guess what? They also need boundaries. They just draw them around failure domains and infrastructure tiers.

## Final Thought

Microservices aren't a goal. They're a trade-off. If you design your systems without principles, you'll just scale your chaos.

Bounded Contexts give you the vocabulary. SOLID gives you the discipline.

Without both, you're not building systems—you're building distributed regrets.
