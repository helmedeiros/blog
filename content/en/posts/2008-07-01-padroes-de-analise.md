---
title: Analysis Patterns
author: helio
layout: post
date: 2008-07-01 03:27:57+00:00
categories:
  - Architecture
series: Design Patterns and Analysis
subtitle: Discover the hidden patterns that make great software tick—explore Martin Fowler's analysis patterns that capture recurring business logic and domain knowledge into reusable, battle-tested solutions
---

> **Series: Design Patterns and Analysis** | **Introduction** > _Developed during Master's in Web Systems Projects_

<style>
.analysis-pattern-img {
  display: block;
  margin: 20px auto;
  max-width: 600px;
  width: 100%;
  height: auto;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
</style>

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

<img src="/uploads/2008/07/picture-2.png" alt="Analysis Pattern - Party" class="analysis-pattern-img">

### Quantity and Unit

Represents a numeric value tied to a unit (e.g., 20 km).

- `Quantity` wraps the value and unit
- Supports operations like `+`, `-`, `*`, `/` between compatible quantities

<img src="/uploads/2008/07/picture-5.png" alt="Analysis Pattern - Quantity" class="analysis-pattern-img">

### Conversion Ratio

Allows transforming a `Quantity` from one unit to another.

- `ConversionRatio` links two units via a multiplier
- Used in operations like `convertTo(Unit)`

<img src="/uploads/2008/07/picture-6.png" alt="Analysis Pattern - Conversion Ratio" class="analysis-pattern-img">

### Compound Units

Models composite units like km/h or $/m².

- Represents combinations of multiple `Unit` instances
- Supports more advanced measurement systems

<img src="/uploads/2008/07/compound-units-1.png" alt="Analysis Pattern - Compound Units Basic" class="analysis-pattern-img">

<img src="/uploads/2008/07/compound-units-2.png" alt="Analysis Pattern - Compound Units Detailed" class="analysis-pattern-img">

### Organizational Hierarchies

Models hierarchical structures recursively.

- `Organization` can have a `parent` and multiple `subsidiaries`
- Ideal for modeling regions, divisions, offices, etc.

<img src="/uploads/2008/07/picture-3.png" alt="Analysis Pattern - Organization Hierarchies" class="analysis-pattern-img">

### Organization Structure

Makes explicit the type of organizational relationship.

- Defines `Organization Structure Type` (e.g., subsidiary, joint venture)
- Decouples the relationship from the entities involved

<img src="/uploads/2008/07/picture-4.png" alt="Analysis Pattern - Organization Structure" class="analysis-pattern-img">

## Conclusion

Analysis patterns help us visualize, discuss, and build more robust systems aligned with real-world domains. They are reusable, precise, and often save hours of discussion.

In future posts, we'll explore how **design patterns** complement these concepts during implementation.

---

### **Series Navigation**

- **Current**: Introduction - Analysis Patterns
- **Next**: [Part 1 - Design Patterns Overview](../2008-07-02-padroes-de-projeto-detalhado/)
- **Complete series**: [Design Patterns Overview](../2008-07-02-padroes-de-projeto-detalhado/) | [Creational Patterns](../2008-07-04-padroes-de-criacao/) | [Structural Patterns](../2008-07-06-padroes-estruturais/) | [Behavioral Patterns](../2008-07-08-padroes-comportamentais/)
