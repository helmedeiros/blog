---
title: "Mini-scenario: Lottery Pool Control System"
author: helio
layout: post
date: 2008-07-12T02:14:52+00:00
categories:
  - UML
---

# Mini-scenario: Betting Pool Management

Continuing this series, here is the second Mini-scenario.

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

Organizing betting pools is common, but doing it manually can be inefficient. The proposed system automates all critical steps — from registration to financial tracking — and even handles email notifications. This way, Jairo saves time, avoids errors, and keeps the fun of lottery pools alive without the management headache.

In upcoming posts, I'll present more practical mini-scenarios developed throughout the course.
