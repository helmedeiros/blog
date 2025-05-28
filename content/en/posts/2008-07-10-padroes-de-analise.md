---
title: "Analysis Patterns"
author: helio
layout: post
date: 2008-07-10T03:27:57+00:00
categories:
  - Padrões Análise
---

A few weeks ago, I had a brief introduction to Software Patterns for Analysis and Projects during my Object-Oriented Modeling (MODELAGEM ORIENTADA A OBJETOS) and UML class taught by Professor Osmar Fernandes Jr.

This was an overview of patterns that opened up a small space for those who, like me, are starting their studies in this field.

With the inherent complexity of business processes, which transform daily into thousands of levels of code and modeling, new work modules, it becomes essential to know conceptual modeling techniques.

Within this context, we encounter Software Patterns that, as mentioned earlier, subdivide mainly into two branches that allow for sharing solutions and formalizing solutions to recurring problems in software development.

Martin Fowler, in his book <a href="http://www.amazon.com/Analysis-Patterns-Reusable-Addison-Wesley-Technology/dp/0201895420" title="Analysis Patterns:

Reusable Object Models" target="\_blank">Analysis Patterns:

Reusable Object Models</a>, defines the patterns of analysis among the types of software patterns.

These patterns are a set of classes and associations that have some meaning in the context of the application, which when reinterpreted for organizational processes, allow clear and authentic solutions on many aspects.

Among the established project patterns by the above-mentioned author, we can highlight:

- Party:

Defines an object part as a supertype for a person or organization, so that associations between information are relative to parties rather than directly to people or organizations. ![Analysis Pattern

- Party][1]

- Organization Hierarchies:

Models an organizational hierarchy through a recursive structure.

Establishing relationships between organizational entities through rules. ![Analysis Pattern

- Organization Hierarchies][2]

- Organization Structure:

Uses types to define relationships between organizational entities. ![Analysis Pattern

- Organization Structure][3]

- Quantity:

Defines an object type that has parts consisting of numbers and units. ![Analysis Pattern

- Quantity][4]

- Conversation Ratio:

Defines a conversion object between units, giving quantity an operation convertTo(Unit) that returns a new quantity in the unit. ![Analysis Pattern

- Quantity][5]

- Compound Units:

A composite unit is the combination of atomic units, for example, miles per hour.

A sophisticated conversion operation can use a converter in an atomic unit to convert composite units.

Note that I left the <a href="http://www.amazon.com/Analysis-Patterns-Reusable-Addison-Wesley-Technology/dp/0201895420" title="Analysis Patterns:

Reusable Object Models" target="\_blank">Analysis Patterns:

Reusable Object Models</a>, [Analysis Pattern

- Party][1], [Analysis Pattern

- Organization Hierarchies][2], [Analysis Pattern

- Organization Structure][3], and [Analysis Pattern

- Quantity][4] placeholders exactly as written, as instructed.

[2]: /uploads/2008/07/picture-3.png
[3]: /uploads/2008/07/picture-4.png
[1]: /uploads/2008/07/picture-2.png
[5]: /uploads/2008/07/picture-6.png
[4]: /uploads/2008/07/picture-5.png
