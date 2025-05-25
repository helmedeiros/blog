---
title: ""
author: helio
layout: post
date: 2008-07-12T02:14:52+00:00
url: /2008/07/12/minicenario-controle-de-bolao/
categories:
  - UML
---

Continuing the session, let's go to the second Minicenário.

Jairo works in the Department of Informatics for a large company.

He and his friends are always making pools for MegaSena, Quina, and other types of games.

Jairo always controls the numbers bet on using an Excel spreadsheet, including the people who entered the pool, their emails (to receive the numbers bet on) and whether they paid their shares.

However, this has been taking up a considerable amount of his time.

Therefore, he thought about developing an application that meets the following functionalities:

 - Allows each participant to be registered for each pool, with their aliases and emails;

 - For each pool made, register the value of the share, number of shares, the cards bet on (with their relationship of numbers), the type of game (MegaSena, Quina etc.), the drawing number, and the date when the drawing will be held;

 - Control who has paid for each share;

 - Generate an automatically-generated Web page with the drawing data, pool participants with their shares, and the numbers bet on.

The HTML file for this page will be sent by email;

 - Each participant can acquire more than one share;

 - Generate a list of participants who have not yet paid;

 - The application must verify if the total amount of shares is equal to the total bet on;

 - A certain bet may be used in other pools.

Consider that all operations are performed by Jairo, who can be identified as the Pool Manager. **USAGE SCENARIO DIAGRAM** ![Diagrama Casos Uso Bolão][1]

[1]: /uploads/2008/07/controle-bolao.png