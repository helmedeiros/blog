---
title: "Caelum Day no Rio – Parte 4: NoSQL com Nico Steppat"
date: 2009-11-11T14:00:00+00:00
draft: false
author: Helio Medeiros
subtitle: "Desafie tudo que você sabe sobre armazenamento de dados—explore o movimento revolucionário NoSQL que abandona garantias ACID por escala massiva, flexibilidade e performance na era emergente de big data"
tags:
  [
    "Caelum Day",
    "NoSQL",
    "Nico Steppat",
    "CouchDB",
    "MongoDB",
    "Redis",
    "Cassandra",
    "Neo4j",
    "Banco de Dados",
    "Escalabilidade",
    "Document Database",
    "Key-Value Store",
    "Graph Database",
    "Series",
    "Rio de Janeiro",
  ]
categories: ["Events", "Architecture"]
series: "Caelum Day 2009"
---

Dando continuidade à série de posts sobre o Caelum Day no Rio, hoje quero comentar sobre a palestra do **Nico Steppat**, que nos apresentou o mundo do **NoSQL** — um termo que, pra muitos ali na sala (inclusive eu), era algo completamente novo.

## Por Que "NoSQL"?

Nico começou explicando que o termo "NoSQL" não significa "sem SQL", mas sim **"não apenas SQL"**. A ideia é usar bancos de dados que não seguem o modelo relacional tradicional quando isso não faz sentido para o problema que estamos resolvendo.

Isso faz muito sentido em sistemas onde performance e escalabilidade horizontal são essenciais — como redes sociais, sistemas de recomendação e grandes volumes de leitura/escrita simultâneos.

## Tipos de Bancos NoSQL

Nico compartilhou uma visão bem clara sobre as diferentes categorias de bancos NoSQL:

- **Documentais (ex: CouchDB, MongoDB)** — armazenam dados como documentos JSON/XML.
- **Chave-valor (ex: Redis, Riak)** — extremamente rápidos, ideais para caching.
- **Colunar (ex: Cassandra, HBase)** — inspirados no BigTable do Google.
- **Grafos (ex: Neo4j)** — perfeitos para dados altamente relacionais, como redes sociais.

## O que Me Chamou Atenção

- A ideia de **modelar dados pensando em leitura eficiente**, e não em normalização.
- Que muitos desses bancos já são usados por grandes empresas como Facebook, Amazon e Twitter.
- O fato de que **não existe um modelo único de consistência** — eventualmente consistente, consistente sob demanda, etc.

## Saí Com Muitas Perguntas (E Isso É Ótimo)

A palestra foi mais provocativa do que técnica, e acho que essa era a intenção. Saí pensando:

- Será que meu modelo relacional é o mais adequado para todos os casos?
- Dá pra usar NoSQL em partes específicas do sistema?
- Como testar e versionar esquemas quando não há "esquema"?

## Quero Testar

Quero pegar um projeto pessoal com muitos dados de leitura e tentar modelar algo em MongoDB ou CouchDB. Não para substituir tudo, mas para entender esse novo jeito de pensar.

**No próximo post:** Flex com Rafael Martinelli da DClick!
