---
title: "Mini Scenario: WORK CONTROL"
date: 2008-07-12
slug: minicenario-controle-de-obras
draft: false
language: en
---

In this third mini-conference we have:
Álvaro is expanding his residence. Every day there's a demand for material purchases. As such, he developed a small application that controls these requests and purchases to build a base for future quotes.
The application has a product catalog containing: name, description, sales unit (Kg, ml, or m; indicating weight, volume, or length) and the value of the sales unit (e.g., 1.5).
Each purchase request is registered with its items. Each item has: the product and quantity. When each item is acquired, the application updates the request with the unit price of purchase, payment method (cash, check, credit card), date of purchase, and location of purchase.

The controls offered by the application are:
- When a new request is made, it's possible to get a list of the three smallest prices already paid for the same product, including the location where it was purchased;
- The list of purchases is printed from the items that haven't been closed. From all open purchase requests;
- A request can be canceled;
- When all items in a request have been purchased, the system automatically updates the status of that request to "closed";
- A list should be generated of all products already purchased, with their summary and total value.
USAGE SCENARIO DIAGRAM