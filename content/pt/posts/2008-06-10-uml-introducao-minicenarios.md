---
title: "Por que UML Ainda Importa: Uma Linguagem Compartilhada para Projetar Sistemas"
author: helio
layout: post
date: 2008-06-10T10:00:00+00:00
categories:
  - UML
tags:
  - mini-scenarios
  - uml-series
---

> **Série: Mini-cenários UML** | **Introdução** > _Desenvolvido durante o Mestrado em Projetos de Sistemas Web_

# Por que UML Ainda Importa: Uma Linguagem Compartilhada para Projetar Sistemas

Antes de mergulharmos na série com quatro minicenários — **Classificados Web**, **Controle de Bolão**, **Gestão de Estacionamento** e **Controle de Obras** — vale uma pausa para entender _como_ escolhemos representar esses sistemas.

A resposta: **UML** — Linguagem de Modelagem Unificada.

Não usamos UML porque está na moda. Usamos porque ela **força precisão**, **evita ambiguidades** e **acelera a tomada de decisão**.

> Se uma imagem vale mais que mil palavras, um diagrama UML vale mais que cem idas e voltas.

Em todos os cenários da série, usamos UML como **ferramenta comum de modelagem**. Isso garante que qualquer pessoa consiga rapidamente entender o sistema, identificar onde está a complexidade e discutir decisões relevantes — mesmo sem contexto prévio.

Este post é o ponto de partida: apresenta os tipos de diagramas e notações que usaremos ao longo da série.

---

## 🧠 O Que a UML Traz Para o Jogo

UML não é uma metodologia. Ela não dita _como_ construir seu sistema. Em vez disso, oferece uma **caixa de ferramentas de diagramas** para expressar o sistema por diferentes perspectivas.

Aqui estão os dois principais tipos que usaremos na série:

---

## 🎯 Diagramas de Casos de Uso

Presentes nos quatro minicenários, esses diagramas respondem à pergunta:
**O que os usuários podem fazer no sistema?**

- **Atores** (bonecos): representam pessoas ou sistemas que interagem com o sistema.
- **Casos de uso** (elipses): representam funcionalidades oferecidas.
- **Associações** (linhas): conectam atores aos casos de uso.
- **<<include>>**: indica que um caso sempre chama outro. (ex: "Publicar Anúncio" inclui "Cadastrar Contato")
- **<<extend>>**: representa lógica opcional ou condicional. (ex: "Anúncio Destaque" estende "Manter Anúncio")

Esse tipo de diagrama é ideal para alinhar **requisitos com stakeholders**. Não é técnico demais — é sobre entendimento comum.

---

## 🗃️ Diagramas de Classes

Usados no cenário de Classificados Web, descrevem a **estrutura de dados** e os **relacionamentos** do sistema.

- **Classes** (retângulos): representam entidades como `Anúncio`, `Usuário`, `SeçãoInteresse`.
- **Atributos**: dados mantidos por cada classe (ex: `email: String`).
- **Métodos**: comportamentos do sistema (ex: `adicionarInteresse()`).
- **Associações**:
  - `1`, `0..1`, `0..*`: multiplicidade (ex: um anúncio pode pertencer a várias seções).
  - Setas: indicam direção e posse da relação.
- **Herança**: como `AnúncioDestaque` herdando de `Anúncio`.

Esses diagramas são essenciais para **modelagem de domínio**, **banco de dados** e **refinamento da arquitetura**.

---

## 💬 Por Que Usamos UML Nesses Casos

A verdade é simples: diagramas sem padrão criam silos.

Quando bem aplicada, a UML:

- **Acelera onboarding**
- **Torna reuniões mais produtivas**
- **Conecta tech com produto**
- **Documenta sistemas sem virar textão**

Não é necessário usar todos os tipos de diagrama, nem ferramentas sofisticadas. Basta seguir a **notação e lógica**. Até um rascunho no papel pode ser claro se usar os conceitos da UML.

---

## 🔍 O Que Vem a Seguir

Nos próximos quatro posts, vamos abordar:

1. Um sistema de **classificados online** com anúncios pagos e seções de interesse
2. Um gerenciador de **bolões de loteria**
3. Um **sistema de controle de obras** com histórico de preços e comparações
4. Um **estacionamento** com impressão de ticket e controle de faturamento

Todos com o mesmo modelo: **diagrama de casos de uso** para comportamento, e quando necessário, **diagrama de classes** para estrutura.

Começar com UML é garantir que qualquer leitor consiga acompanhar o raciocínio — mesmo sem nunca ter visto o projeto antes.

---

### **📚 Navegação da Série**

- **Atual**: Introdução - Por que UML Ainda Importa
- **Próximo**: [Parte 1 - Classificados Web](../2008-06-13-minicenario-classificados-na-web/)
- **Série completa**: [Classificados Web](../2008-06-13-minicenario-classificados-na-web/) | [Controle de Bolão](../2008-06-17-minicenario-controle-de-bolao/) | [Controle de Obras](../2008-06-21-minicenario-controle-de-obras/) | [Estacionamento](../2008-06-25-diagrama-de-casos-de-uso-estacionamento/)

Fique ligado.
