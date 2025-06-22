---
title: "Caelum Day no Rio – Parte 3: RESTful APIs com Sergio Junior e Luiz Costa"
date: 2009-11-10T14:00:00+00:00
draft: false
author: Helio Medeiros
subtitle: "Desbloqueie o verdadeiro poder da arquitetura REST—vá além de APIs HTTP simples para descobrir HATEOAS e design dirigido por hipermídia que torna serviços web verdadeiramente autodescritivos e evolutivos"
tags:
  [
    "Caelum Day",
    "RESTful APIs",
    "REST",
    "Sergio Junior",
    "Luiz Costa",
    "Restfulie",
    "HATEOAS",
    "HTTP",
    "Hipermídia",
    "Design de APIs",
    "Java",
    "Série",
    "Rio de Janeiro",
  ]
categories: [ "Events"]
series: "Caelum Day 2009"
---

Continuando a série de posts sobre o Caelum Day no Rio, hoje quero compartilhar minhas impressões sobre a palestra de **Sergio Junior e Luiz Costa** sobre **RESTful APIs**.

## Desmistificando REST

Antes dessa palestra, eu já tinha ouvido falar sobre REST, mas de forma superficial. A apresentação começou esclarecendo que **REST não é apenas usar HTTP com verbos como GET e POST**, mas sim uma arquitetura que valoriza recursos bem definidos, uso adequado dos verbos HTTP e, principalmente, **hipermídia como motor do estado da aplicação (HATEOAS)**.

## Introdução ao Restfulie

Eles apresentaram o **Restfulie**, uma biblioteca desenvolvida pela Caelum para facilitar a criação de APIs RESTful em Java. O que me chamou atenção foi como o Restfulie:

- **Simplifica a serialização** de objetos para XML ou JSON
- **Adiciona links de navegação** nas respostas, permitindo que o cliente descubra dinamicamente as próximas ações disponíveis
- **Integra-se facilmente com o VRaptor**, que já conheci na palestra anterior

Por exemplo, ao retornar um pedido, a API pode incluir links para "pagar" ou "cancelar" o pedido, guiando o cliente pelas possíveis transições de estado.

## Exemplo Prático

Eles mostraram um exemplo onde um recurso "Pedido" inclui links para ações relacionadas:

```xml
<pedido>
  <produto>Curso de Java</produto>
  <link rel="pagamento" href="http://exemplo.com/pedidos/1/pagar"/>
  <link rel="cancelamento" href="http://exemplo.com/pedidos/1/cancelar"/>
</pedido>
```

No cliente, seria possível seguir esses links para realizar as ações correspondentes, sem precisar conhecer previamente as URLs.

## Explore o Restfulie

O Restfulie é open source e você pode explorar a biblioteca de hipermídia no GitHub:
[Restfulie no GitHub](https://github.com/caelum/restfulie)

## Impressões Finais

A palestra foi esclarecedora e me fez perceber que construir APIs RESTful vai além de mapear URLs para métodos. Trata-se de **projetar uma interface que guia o cliente através dos estados possíveis**, tornando a aplicação mais intuitiva e flexível.

Saí da sala motivado a estudar mais sobre REST e a experimentar o Restfulie em projetos futuros.

**No próximo post:** falarei sobre a palestra do Nico Steppat sobre NoSQL. Até lá!
