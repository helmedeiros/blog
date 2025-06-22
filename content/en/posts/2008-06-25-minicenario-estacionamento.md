---
author: helio
categories:
  - Architecture
date: 2008-06-25 02:48:10+00:00
dsq_thread_id: null
layout: post
series: UML Mini-scenarios
subtitle: "Design a complete parking management solution—master UML use case modeling for ticket generation, space tracking, payment processing, and customer flow optimization in commercial parking facilities"
tags:
  - mini-scenarios
  - uml-series
title: "Mini-scenario: PARKING"
---

> **Series: UML Mini-scenarios** | **Part 4 of 4** > _Developed during Master's in Web Systems Projects_

**We've reached the final scenario** in this UML mini-scenarios series developed under the guidance of Professor Osmar Fernandes Jr. After exploring [web classifieds](../2008-06-13-minicenario-classificados-na-web/), [betting pool control](../2008-06-17-minicenario-controle-de-bolao/), and [construction control](../2008-06-21-minicenario-controle-de-obras/), we now model a parking system.

This final scenario demonstrates how UML can capture real-time operations, automatic calculations, and business rules based on time and context.

## Scenario

When a vehicle enters the parking lot, the **attendant** records the **license plate**, **car model**, and **color** into the system.

The **entry time** is automatically generated at the moment of registration.

After parking, the customer receives a **printed ticket** showing:

- License plate number
- Vehicle model and color
- Entry date and time

Upon return, the customer hands over the ticket. The system calculates the **length of stay** and applies the correct **pricing table**, which may vary between weekdays and weekends.

The system also allows for special **promotions**, depending on the time of year.

## Use Case Diagram

<img src="/uploads/2008/07/estacionamento.png" alt="Usage Case Diagram Parking Lot" height="425" width="656" />

The **Attendant** is the primary actor and interacts with the system through the following actions:

- **Register entry/exit**: logs vehicle data and generates billing info.
- **Maintain vehicle**: updates or corrects vehicle information.
- **Print ticket**: given to the customer upon entry.
- **Manage pricing table**: configure different rates for weekdays and weekends.
- **Manage promotions**: add discounts based on specific periods.
- **Calculate revenue**: based on all registered activity.
- **Generate billing report**: for internal use.

### Quick glossary:

- **<<include>>**: indicates one use case is always triggered as part of another (e.g., "Register entry" includes "Print ticket").
- **<<extend>>**: represents optional behavior, conditionally executed (e.g., applying a promotion when generating an invoice).

## Series Conclusion

This parking system concludes our UML mini-scenarios series, demonstrating how different business domains can be modeled with clarity and precision.

**Throughout this series, we explored**:

1. **[Web Classifieds](../2008-06-13-minicenario-classificados-na-web/)**: System with multiple actors and automatic notifications
2. **[Betting Pool Control](../2008-06-17-minicenario-controle-de-bolao/)**: Financial management and participant control
3. **[Construction Control](../2008-06-21-minicenario-controle-de-obras/)**: Price history and comparative reports
4. **Parking System**: Real-time operations and automatic calculations

Each scenario illustrates different aspects of UML modeling, from simple use cases to complex relationships between classes and actors. **UML use case modeling** clearly outlines system responsibilities and interactions, regardless of the domain.

---

### **Series Navigation**

- **Introduction**: [Why UML Still Matters](../2008-06-10-uml-introduction-use-case-series/)
- **Previous**: [Part 3 - Construction Control](../2008-06-21-minicenario-controle-de-obras/)
- **Current**: Part 4 - Parking System (Final)
- **Complete series**: [Web Classifieds](../2008-06-13-minicenario-classificados-na-web/) | [Betting Pool Control](../2008-06-17-minicenario-controle-de-bolao/) | [Construction Control](../2008-06-21-minicenario-controle-de-obras/)
