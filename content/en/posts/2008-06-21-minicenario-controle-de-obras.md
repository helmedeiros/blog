---
title: "Mini-scenario: Construction Control"
author: helio
layout: post
date: 2008-06-21T09:24:08+00:00
categories:
  - UML
tags:
  - mini-scenarios
  - uml-series
---

> **Series: UML Mini-scenarios** | **Part 3 of 4** > _Developed during Master's in Web Systems Projects_

# Mini-scenario: Construction Control

**Continuing our series**, this is the third mini-scenario developed under the guidance of Professor Osmar Fernandes Jr. After exploring [web classifieds](../2008-06-13-minicenario-classificados-na-web/) and [betting pool control](../2008-06-17-minicenario-controle-de-bolao/), we now model a construction purchase control system.

This scenario demonstrates how UML can capture price history, automatic comparisons, and reports for decision-making.

## Scenario

Alvaro is expanding his residence. Every day there is a demand for material purchases. Therefore, he developed a small application that controls this demand for requests and purchases, in order to build a pricing basis for future purchases.

The application has a product registry, containing: name, description, sales measure of the product (Kg, ml or m; indicating weight, volume or length) and value of the sales measure (e.g., 1.5).

Each purchase request is registered with the items from that request. Each item has: the product and quantity. When each item is acquired, the request is updated with the unit price of purchase, payment method (cash, check, credit card), date of purchase, and location of purchase.

## System Controls

The controls offered by the application are:

- When there is a new purchase request, it's possible to obtain the list of the three smallest prices already paid for the referred product, including the location where it was purchased;
- The list of purchases is printed from the items that have not been closed, from all the purchase requests that are still open;
- A purchase request can be cancelled;
- When all the items in a purchase request have been bought, the system automatically updates the status of that request to "closed";
- A summary list of all products already purchased should be issued, along with their total and value;

## Use Case Diagram

<img src="/uploads/2008/07/controle-de-obras.png" alt="Mini-scenario: CONSTRUCTION CONTROL" height="426" width="642" />

This **UML Use Case Diagram** shows the main system functionalities from the perspective of the primary user, Alvaro:

- **Maintain products**: register and update material information
- **Maintain requests**: create and manage purchase orders
- **Register purchases**: update requests with actual purchase data
- **Query price history**: view the three lowest prices already paid
- **Generate reports**: issue lists of pending purchases and acquired products
- **Cancel requests**: when necessary

### Quick glossary:

- **Use Case**: represents a user action or goal (e.g., "Query price history").
- **<<include>>**: indicates one use case always includes another (e.g., "Register purchase" includes "Update request status").
- **<<extend>>**: represents optional or conditional action (e.g., "Cancel request" extends "Maintain requests").

## Conclusion

This third scenario illustrates how control systems can incorporate intelligence to support decisions. Unlike previous scenarios ([classifieds](../2008-06-13-minicenario-classificados-na-web/) and [betting pool](../2008-06-17-minicenario-controle-de-bolao/)), here the focus is on history and data comparison to optimize future purchases.

UML modeling helps us organize these functionalities clearly, showing how historical data can be transformed into useful information.

---

### **Series Navigation**

- **Introduction**: [Why UML Still Matters](../2008-06-10-uml-introduction-use-case-series/)
- **Previous**: [Part 2 - Betting Pool Control](../2008-06-17-minicenario-controle-de-bolao/)
- **Current**: Part 3 - Construction Control
- **Next**: [Part 4 - Parking System](../2008-06-25-diagrama-de-casos-de-uso-estacionamento/)
- **Complete series**: [Web Classifieds](../2008-06-13-minicenario-classificados-na-web/) | [Betting Pool Control](../2008-06-17-minicenario-controle-de-bolao/) | [Parking System](../2008-06-25-diagrama-de-casos-de-uso-estacionamento/)
