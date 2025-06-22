---
title: "SOLID Principles in a Microservices World"
date: 2018-05-01T14:00:00-03:00
author: Helio Medeiros
subtitle: Apply SOLID principles to microservices architecture—identifying system smells and designing cohesive, maintainable distributed systems with clear boundaries and stable contracts
tags:
  [
    "solid principles",
    "microservices",
    "system design",
    "architecture",
    "software engineering",
    "distributed systems",
  ]
categories: ["Technology", "Architecture"]
---

In the early days of our careers, most of us learn about SOLID principles as if they only apply to object-oriented programming and class design. But these principles go far beyond clean code inside a single repository. They help structure thinking in systems, especially when those systems scale into microservices.

Let's explore this with a practical analogy: a digital newspaper portal.

## The Portal as Microservices

Consider a large-scale digital portal structured into the following high-level features:

- **Live News**
- **Weather**
- **Entertainment**
- **Lifestyle**
- **Sports**

Each of these areas contains services like breaking news, celebrity updates, weather radar, fitness tips, or player profiles. At a first glance, this looks modular. But we know modularity is not a guarantee of clarity.

The portal is now built with dozens of distributed services. The frontend fetches data from different APIs. Teams are organized by verticals. And yet… changes still ripple through the system. Incidents still occur. Releases are slow. What's going on?

## Common Smells in Microservices

Let's list typical design smells and what they look like in this microservices environment:

| Smell                   | Microservices Manifestation                                                                                                              |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| **Rigidity**            | Altering one service (e.g. `Weather Radar`) forces coordinated changes in others (`Weather Alerts`) due to shared contracts or payloads. |
| **Fragility**           | Updating `Celebrity News` breaks `Red Carpet Coverage`, as both rely on tightly-coupled data schemas.                                    |
| **Immobility**          | Want to reuse `Box Office Charts` in a new app? Too many hard dependencies on legacy service layers.                                     |
| **Viscosity**           | It's easier to add a new endpoint in `Sports` than refactor `Live Scores`, so tech debt grows.                                           |
| **Needless Complexity** | Using 5 services where one would do. Exaggerated message queues, over-engineered pipelines.                                              |
| **Needless Repetition** | `Current Weather`, `Forecast`, and `Weather Alerts` each duplicate logic about location parsing.                                         |
| **Opacity**             | Who calls what? Why is the alert triggered? Logs don't help. Dashboards don't clarify. Nobody knows.                                     |

These issues are _not_ exclusive to classes or code. They're signs of poor **system design**. And just like in a monolith, the answer begins with **principles**.

## SOLID for Microservices

Let's reframe SOLID for systems—not classes.

| Principle | In Classes                                      | In Microservices                                                    |
| --------- | ----------------------------------------------- | ------------------------------------------------------------------- |
| SRP       | A class has a single reason to change           | A service has a single responsibility and functional cohesion       |
| OCP       | Open for extension, closed for modification     | API contract remains stable; new behavior via versions or endpoints |
| LSP       | Subtypes substitute base types correctly        | New service versions or contracts must be backward compatible       |
| ISP       | Don't force clients to depend on unused methods | Specific APIs per client type; avoid overly generic endpoints       |
| DIP       | Depend on abstractions, not concretions         | Use interfaces or events instead of hardcoded direct calls          |

## Practical Examples

**Smell: Fragility between `Celebrity News` and `Red Carpet Coverage`**

These services share a giant data model. Changes in the celebrity schema break consumers. That violates LSP.

**Fix (LSP + ISP)**: Expose only specific data needed by `Red Carpet` via DTOs. Create `/v2/celebrity` endpoints and allow migration.

---

**Smell: Immobility in `Box Office Charts`**

Service logic is tied to rendering and public API. You can't reuse its calculation logic elsewhere.

**Fix (SRP + DIP)**: Extract domain logic into a separate reusable layer. Expose via events or functions. API is just a consumer now.

---

**Smell: Viscosity in `Live Scores`**

Refactoring is painful. Easier to patch with a new endpoint.

**Fix (SRP + OCP)**: Model cases better. Add optional parameters instead of duplicating logic. Test via consumer-driven contracts.

## Conclusion

SOLID isn't just for OOP lovers. It's a critical lens for systems design. Microservices don't solve bad design. Principles do.
