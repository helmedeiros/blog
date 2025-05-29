---
title: Padrões de Análise
author: helio
layout: post
date: 2008-07-01T03:27:57+00:00
categories:
  - Padrões de Análise
---

Algumas semanas atrás, durante a aula de Modelagem Orientada a Objetos e UML com o professor Osmar Fernandes Jr., fomos introduzidos aos **Padrões de Análise de Software**. Este post resume esse conceito e mostra como ele nos ajuda a modelar estruturas de negócio recorrentes com clareza.

## Por que isso importa

À medida que sistemas e processos crescem em complexidade, surgem milhares de regras, entidades e relacionamentos. Os **padrões de análise** nos ajudam a:

- Compartilhar soluções reutilizáveis
- Formalizar conceitos do domínio
- Evitar reinventar a roda em novos módulos ou sistemas

## O que são Padrões de Análise

No livro [Analysis Patterns: Reusable Object Models](https://martinfowler.com/books/ap.html), Martin Fowler define esses padrões como **modelos conceituais reutilizáveis**. Cada padrão representa **uma combinação de classes, atributos e relacionamentos** que aparecem repetidamente em diferentes domínios de negócio.

Eles permitem que ideias complexas sejam comunicadas visualmente e com consistência.

## Exemplos com UML

### Party

Define um supertipo genérico para pessoas e organizações.

- Evita duplicação de lógica entre entidades que compartilham relacionamentos (ex: endereço, telefone)
- Útil para modelar qualquer "ator" no sistema

![Analysis Pattern - Party](/uploads/2008/07/picture-2.png)

### Quantity e Unit

Representa um valor numérico com uma unidade (ex: 20 km).

- `Quantity` encapsula valor e unidade
- Suporta operações como `+`, `-`, `*`, `/` entre quantidades compatíveis

![Analysis Pattern - Quantity](/uploads/2008/07/picture-5.png)

### Conversion Ratio

Permite transformar uma `Quantity` de uma unidade para outra.

- `ConversionRatio` liga duas unidades com um fator multiplicador
- Usado em operações como `convertTo(Unit)`

![Analysis Pattern - Quantity](/uploads/2008/07/picture-6.png)

### Compound Units

Modela unidades compostas como km/h ou R$/m².

- Representa combinações de múltiplas `Unit`
- Suporta sistemas mais avançados de medição

**[Imagem: Diagrama UML de Compound Units aqui]**

### Hierarquias Organizacionais

Modela estruturas hierárquicas de forma recursiva.

- `Organization` pode ter um `parent` e várias `subsidiaries`
- Ideal para modelar regiões, divisões, escritórios, etc.

![Analysis Pattern - Organization Hierarchies](/uploads/2008/07/picture-3.png)

### Estrutura Organizacional

Explicita o tipo de relacionamento organizacional.

- Define `Organization Structure Type` (ex: subsidiária, joint venture)
- Separa o relacionamento das entidades envolvidas

![Analysis Pattern - Organization Structure](/uploads/2008/07/picture-4.png)

## Conclusão

Padrões de análise ajudam a visualizar, discutir e construir sistemas mais robustos e alinhados com o mundo real. Eles são reutilizáveis, precisos e economizam horas de discussão.

Em posts futuros, vamos explorar como os **padrões de projeto (design patterns)** complementam esses conceitos na implementação.
