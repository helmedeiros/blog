---
title: "Analysis Patterns"
date: 2008-07-12
slug: padroes-de-analise
draft: false
language: en
---

A few weeks ago, I had a brief introduction to Software Patterns for Analysis and Design during my Object-Oriented Modeling (UML) class taught by Professor Osmar Fernandes Jr., which I'll be expanding on here. This small space is intended for those who, like me, are just starting their studies in this area.

Given the inherent complexity of business processes that transform daily into thousands of code levels and modeling new work modules, it's essential to know conceptual modeling techniques.
Within this context, we encounter Software Patterns that primarily subdivide into two main branches, allowing the sharing of solutions and formal conception of solutions for recurring problems in software development.
Martin Fowler, in his book Analysis Patterns: Reusable Object Models, defines analysis patterns as a type of software pattern. These patterns are a set of classes and associations that have some meaning within the application context, which when reinterpreted for organizational processes, enable clear and authenticated solutions for many aspects.

Among the established project patterns by the aforementioned author, we can highlight:
- Party: Defines an object part as a supertype for a person or organization, allowing information association to be relative to parties rather than individuals or organizations directly.
- Organization Hierarchies: Models an organizational hierarchy through recursive structure. Establishes relationships between organizational entities using rules.
- Organization Structure: Uses types to define relationships between organizational entities.
- Quantity: Defines an object type that has parts numbers and units.
- Conversation Ratio: Defines a conversion object between units, giving quantity an operation convertTo(Unit) that returns a new quantity in the unit.
- Compound Units: A compound unit is the combination of atomic units, for example miles per hour. Sophisticated conversion operations can use an atomic unit converter to convert composite units.