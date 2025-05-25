---
title: "Miniature: POOL CONTROL"
author: helio
layout: post
date: 2008-07-12T02:14:52+00:00
url: /2008/07/12/minicenario-controle-de-bolao/
categories:
  - UML
---

Continuing the session, we'll go to the second Minicenário.
Jairo works in the Department of Informatics at a large company. He and his friends are always making MegaSena, Quina, and other types of games. Jairo always controls on an Excel spreadsheet the numbers bet, plus the people who entered the pool, their emails (to receive the bet numbers) and whether they paid their shares. However, this has been taking him a considerable amount of time. So, he thought about developing an application that meets the following functionalities:
  * Allow each participant to be registered for each pool, with their ramals and emails;
  * For each made pool, register the share value, number of shares, the cards bet (with their number relationships), the game type (MegaSena, Quina etc.), the contest number and the date when the draw will be held;
  * Control who paid each share;
  * Generate automatically a Web page with the draw data, pool participants with their shares and bet numbers. The HTML file for this page will be sent by email;
  * Each participant can acquire more than one share;
  * Generate a list of participants who have not yet paid;
  * The application must verify if the total shares is equal to the total bet;
  * A certain bet may be used in other pools.
Consider that all operations are performed by Jairo, who can be identified as Pool Manager.
**USE CASE DIAGRAM**
![Use Case Diagram Pool][1]
 [1]: http://www.helmed.net/blog/wp-content/uploads/2008/07/controle-bolao.png