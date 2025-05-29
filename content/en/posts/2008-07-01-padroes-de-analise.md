---
title: "Analysis Patterns"
author: helio
layout: post
date: 2008-07-01T03:27:57+00:00
categories:
  - Padrões Análise
---

A few weeks ago, during our Object-Oriented Modeling and UML class with Professor Osmar Fernandes Jr., we were introduced to **Software Analysis Patterns**. This post summarizes that concept and shows how it helps us model recurring business structures with clarity.

## Why It Matters

As systems and business processes grow in complexity, they generate thousands of rules, entities, and relationships. **Analysis patterns** help us to:

- Share reusable solutions
- Formalize domain concepts
- Avoid reinventing the wheel in new modules or systems

## What Are Analysis Patterns

In his book [Analysis Patterns: Reusable Object Models](https://martinfowler.com/books/ap.html), Martin Fowler defines these patterns as **reusable conceptual models**. Each pattern represents **a combination of classes, attributes, and relationships** that occur repeatedly across different business domains.

They allow us to communicate complex ideas visually and with consistency.

## UML Examples

### Party

Defines a generic supertype for people and organizations.

- Avoids duplicated logic across entities that share the same relationships (e.g., address, phone)
- Useful for modeling any "actor" in a system

![Analysis Pattern - Party](/uploads/2008/07/picture-2.png)

### Quantity and Unit

Represents a numeric value tied to a unit (e.g., 20 km).

- `Quantity` wraps the value and unit
- Supports operations like `+`, `-`, `*`, `/` between compatible quantities

![Analysis Pattern - Quantity](/uploads/2008/07/picture-5.png)

### Conversion Ratio

Allows transforming a `Quantity` from one unit to another.

- `ConversionRatio` links two units via a multiplier
- Used in operations like `convertTo(Unit)`

![Analysis Pattern - Quantity](/uploads/2008/07/picture-6.png)

### Compound Units

Models composite units like km/h or $/m².

- Represents combinations of multiple `Unit` instances
- Supports more advanced measurement systems

**[Image: UML diagram for Compound Units here]**

### Organizational Hierarchies

Models hierarchical structures recursively.

- `Organization` can have a `parent` and multiple `subsidiaries`
- Ideal for modeling regions, divisions, offices, etc.

![Analysis Pattern - Organization Hierarchies](/uploads/2008/07/picture-3.png)

### Organization Structure

Makes explicit the type of organizational relationship.

- Defines `Organization Structure Type` (e.g., subsidiary, joint venture)
- Decouples the relationship from the entities involved

![Analysis Pattern - Organization Structure](/uploads/2008/07/picture-4.png)

## Conclusion

Analysis patterns help us visualize, discuss, and build more robust systems aligned with real-world domains. They are reusable, precise, and often save hours of discussion.

In future posts, we'll explore how **design patterns** complement these concepts during implementation.
