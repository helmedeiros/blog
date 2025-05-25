---
title: "Mini scenario: WORK CONTROL"
author: helio
layout: post
date: 2008-07-12T09:24:08+00:00
url: /2008/07/12/minicenario-controle-de-obras/
categories:
  - UML
---

This third minicenarium has that:
Álvaro is doing an expansion of his residence. There is daily demand for material purchase. Therefore, he developed a small application that controls the demand for requests and purchases, in order to build a base for future purchases.

Application has a product catalog containing: name, description, sales measurement (Kg, ml or m; indicating weight, volume or length) and measurement value price (e.g., 1.5).
Each purchase request is registered with the items from that request. Each item has: the product and quantity. When each item is acquired, the request is updated with the unit purchase price, payment method (cash, check, credit card), date of purchase, and location of purchase.

The application offers controls:

* When a new request is made, it's possible to get a list of the three smallest prices paid for the referenced product, including the location where it was purchased;
* The purchase list is printed from the items that have not been closed. From all open purchase requests;
* A request can be cancelled;
* When all items in a request have been purchased, the system automatically updates the status of that request to "closed";
* A summary report should be issued for all products already purchased, with their total and value;