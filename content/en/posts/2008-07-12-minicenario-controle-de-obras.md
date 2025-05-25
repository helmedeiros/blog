---
title: ""
author: helio
layout: post
date: 2008-07-12T09:24:08+00:00
categories:
  - UML
---

In this third minicenario we have that:

Alvaro is expanding his residence.

Every day there is a demand for material purchases.

Therefore, he developed a small application that controls this demand for requests and purchases, in order to build a pricing basis for future purchases.

The application has a product registry, containing: name, description, sales measure of the product (Kg, ml or m; indicating weight, volume or length) and value of the sales measure (e.g., 1.5).

Each purchase request is registered with the items from that request.

Each item has: the product and quantity.

When each item is acquired, the request is updated with the unit price of purchase, payment method (cash, check, credit card), date of purchase, and location of purchase.

The controls offered by the application are:

 - When there is a new purchase request, it's possible to obtain the list of the three smallest prices already paid for the referred product, including the location where it was purchased;

 - The list of purchases is printed from the items that have not been closed.

From all the purchase requests that are still open;

 - A purchase request can be cancelled;

 - When all the items in a purchase request have been bought, the system automatically updates the status of that request to "closed";

 - A summary list of all products already purchased should be issued, along with their total and value; USE CASE DIAGRAM <img src="" alt="Minicenario:

CONTROL OF CONSTRUCTION WORKS" height="426" width="642" />