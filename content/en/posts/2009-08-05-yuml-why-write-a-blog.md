---
title: "yUML – Why Write a Blog?"
date: 2009-08-05T12:03:24+02:00
draft: false
tags: ["UML", "blogging", "documentation", "software-design", "yUML"]
categories: ["Architecture"]
---

For some time now, I've been trying to develop the habit of not just reading great _posts_, but writing them too. Many of those I read emphasize the importance of sharing knowledge — and that's what I'm picking up again in this post.

A new web service recently launched that reinforces this idea of collaborative technical content: [yUML](https://yuml.me/).

If you've never heard of it: **yUML is an online tool that lets you generate UML diagrams directly from plain text.** It's a game changer for anyone writing about software design and wanting to illustrate ideas without heavy tools.

## Context: UML on This Blog

If you landed here out of curiosity, you may want to read my previous post first:

👉 [UML – Introduction with Mini-Scenarios](https://blog.heliomedeiros.com/pt/posts/2008-06-10-uml-introducao-minicenarios/)

In that post, I explored use case and class diagrams to model real-life situations like online classifieds or lottery pools. With yUML, the goal is to make those visualizations even simpler, directly embedded in your content.

## Example 1: Class Diagram

```text
[Customer]1-0..*[Order]
[Order]<>-1[Payment]
```

Visualization:

![Class](https://yuml.me/diagram/scruffy/class/[Customer]1-0..*[Order],[Order]<>-1[Payment])

This diagram shows:

- One customer can have zero or many orders.
- Each order has exactly one payment with aggregation (strong relationship).

## Example 2: Use Case Diagram

```text
[Customer]-(Browse Products)
[Customer]-(Place Order)
[Customer]-(Cancel Order)
```

Visualization:

![Use Case](<https://yuml.me/diagram/scruffy/usecase/[Customer]-(Browse%20Products),[Customer]-(Place%20Order),[Customer]-(Cancel%20Order)>)

This represents the main actions a customer can perform in a simple order management system.

## Example 3: Activity Diagram

```text
(start)->(Validate Info)->(Create Account)->(Send Email)->(end)
```

Visualization:

![Activity](<https://yuml.me/diagram/scruffy/activity/(start)-(Validate%20Info)-(Create%20Account)-(Send%20Email)-(end)>)

A basic registration workflow in activity format.

## Why Use yUML?

- It lets you **embed real diagrams in blogs, markdown files, or presentations**.
- You write plain text, and the tool renders a clean visual.
- Perfect for **incremental explanation**, no need to export or upload images manually.

## Final Thoughts

More than a tool tip, this post is an invitation: if you have something worth sharing, make it visual. Diagrams like the ones in my [UML introduction post](https://blog.heliomedeiros.com/pt/posts/2008-06-10-uml-introducao-minicenarios/) can now be published with just a few lines of text using yUML.

Whether you're designing, writing, or simply exploring — write, share, and draw. Knowledge grows when it's diagrammed.
