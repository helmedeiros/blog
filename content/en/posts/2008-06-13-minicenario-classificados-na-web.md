---
author: helio
categories:
- Events
- Architecture
date: 2008-06-13 01:57:56+00:00
layout: post
series: UML Mini-scenarios
subtitle: Modeling web classifieds system using UML mini-scenarios
tags:
- mini-scenarios
- uml-series
title: 'Mini-scenario: Web Classifieds'
---

> **Series: UML Mini-scenarios** | **Part 1 of 4** > _Developed during Master's in Web Systems Projects_

As part of my Master's in Web Systems Projects, I created four mini-scenarios under the guidance of Professor Osmar Fernandes Jr. This series explores different business domains through UML modeling, demonstrating how use cases and class diagrams can capture real-world requirements.

**In this first scenario**, I present a web-based classifieds system imagined by Dalila to share with her friends from school, her neighborhood, and a local club.

## Description

Dalila offers a simple service: anyone can post classified ads online.

The pricing model is straightforward:

- **R$2.00** for a **basic ad**: up to 20 words.
- **R$5.00** for a **featured ad**: up to 50 words _plus_ an image.

Each ad remains active for 15 days.

> Note: Some fields **don't count** toward the word limit — like product value, title, contact name, phone numbers (up to 2), and a note about availability (e.g., "from 6pm to 8pm").

Subscribers receive a **daily summary** of the site's new listings via email. Users can also define **interest areas**, so they get notified of relevant ads without having to visit the site.

## Use Case Diagram

![Diagrama Casos Uso Classificados Web](/uploads/2008/07/classificado-na-web.png)

This UML **Use Case Diagram** shows how actors (users or systems) interact with the system:

- **Anunciante (Advertiser)**: Can create, update, and publish ads.
- **Cliente (Client)**: Can browse ads, subscribe, and receive updates.
- **Mail Server**: Sends email notifications with ads.

### Quick glossary:

- **Use Case**: A user goal represented as an action (e.g., "Publicar Anúncio").
- **<<include>>**: Means this functionality is always required as part of another use case (like "Cadastrar Anúncio" always needing "Manter Informações do Produto").
- **<<extend>>**: Means this functionality is optional or conditional (e.g., "Manter Anúncio Destaque" extends "Manter Anúncio").

## Class Diagram

![Diagrama de Classes Classificados Web](/uploads/2008/07/classificado-na-web-diagrama-de-classe.png)

This **Class Diagram** represents the system's structure using classes, their attributes, methods, and relationships.

### Key Elements:

- **Anúncio**: The ad object, containing title, value, dates, contact, and notes.
- **AnúncioDestaque**: Inherits from `Anúncio` and adds an image.
- **Seção de Interesse**: Allows grouping ads by category (e.g., Jobs, Electronics).
- **Cliente & Assinante**: A client can subscribe and receive email summaries.
- **Usuário**: The system user, with login credentials.
- **Associations** like `0..*`, `1`, `0..1`: Show how many instances relate to each other (e.g., one client can have multiple interest sections).

## Conclusion

This first scenario demonstrates how an apparently simple system can involve multiple actors and complex relationships. UML modeling helps us capture both the interactions (use cases) and the data structure (classes) required.

---

### **Series Navigation**

- **Introduction**: [Why UML Still Matters](../2008-06-10-uml-introduction-use-case-series/)
- **Current**: Part 1 - Web Classifieds
- **Next**: [Part 2 - Betting Pool Control](../2008-06-17-minicenario-controle-de-bolao/)
- **Complete series**: [Betting Pool Control](../2008-06-17-minicenario-controle-de-bolao/) | [Construction Control](../2008-06-21-minicenario-controle-de-obras/) | [Parking System](../2008-06-25-diagrama-de-casos-de-uso-estacionamento/)