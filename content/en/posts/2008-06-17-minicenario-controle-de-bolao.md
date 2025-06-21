---
title: "Mini-scenario: Lottery Pool Control System"
author: helio
layout: post
date: 2008-06-17T02:14:52+00:00
categories: ["Events", "Leadership"]
series: "UML Mini-scenarios"
subtitle: Managing lottery pools with automated participant tracking and payment control
tags:
  - mini-scenarios
  - uml-series
---

> **Series: UML Mini-scenarios** | **Part 2 of 4** > _Developed during Master's in Web Systems Projects_

**Continuing this series**, here is the second mini-scenario developed under the guidance of Professor Osmar Fernandes Jr. After exploring a web classifieds system, we now model a different domain: lottery pool management.

This scenario demonstrates how UML can capture more complex business rules, involving financial control, automatic notifications, and participant management.

## Scenario

Jairo works in the IT department of a large company. He and his friends often organize betting pools for Mega-Sena, Quina, and other lottery games. Until now, Jairo has managed everything with Excel spreadsheets — tracking bet numbers, participants, emails for communication, and who has paid their share.

This manual process takes considerable time, so Jairo decided to develop a system to automate the process with the following features:

- Register participants for each pool, including email and extension.
- Register betting pools with the value per share, number of shares, the tickets placed (with numbers), game type (Mega-Sena, Quina, etc.), contest number, and draw date.
- Track who has paid their share.
- Automatically generate a web page with draw data, participants, shares, and bet numbers. The HTML file is sent via email.
- Allow participants to acquire more than one share.
- Generate a list of participants who haven't paid yet.
- Ensure the total amount of shares matches the total bet amount.
- Reuse a specific bet in other pools.

All operations are performed by Jairo, identified in the system as the **Pool Manager**.

## Use Case Diagram

![Diagrama Casos Uso Bolão](/uploads/2008/07/controle-bolao.png)

This **UML Use Case Diagram** shows the available system actions from the perspective of the primary user — the Pool Manager:

- **Manage participants per pool**: add or remove participants.
- **Track payment of shares**: record who has paid.
- **Generate HTML file**: automate the summary page with pool info.
- **Send email**: triggered after HTML generation.
- **View available game types**: see which games are supported.
- **Manage pool** and **manage bets**: core setup actions.
- **Acquire share**: when a participant joins a pool.

### Quick glossary:

- **Use Case**: represents a user action or goal (e.g., "Track payment of shares").
- **<<include>>**: one use case always calls another (e.g., "Send email" is always part of "Generate HTML file").
- **<<extend>>**: represents optional or conditional actions (e.g., "Manage bets" extends "Manage pool").

## Conclusion

This second scenario illustrates how apparently simple systems can involve complex business rules. Compared to the [web classifieds system](../2008-06-13-minicenario-classificados-na-web/), here we have greater integration between functionalities and more rigorous financial controls.

UML modeling helps us organize these complexities in a clear and understandable way.

---

### **Series Navigation**

- **Introduction**: [Why UML Still Matters](../2008-06-10-uml-introduction-use-case-series/)
- **Previous**: [Part 1 - Web Classifieds](../2008-06-13-minicenario-classificados-na-web/)
- **Current**: Part 2 - Betting Pool Control
- **Next**: [Part 3 - Construction Control](../2008-06-21-minicenario-controle-de-obras/)
- **Complete series**: [Web Classifieds](../2008-06-13-minicenario-classificados-na-web/) | [Construction Control](../2008-06-21-minicenario-controle-de-obras/) | [Parking System](../2008-06-25-diagrama-de-casos-de-uso-estacionamento/)
