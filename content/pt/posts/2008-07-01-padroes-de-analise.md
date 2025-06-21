---
title: Padrões de Análise
author: helio
layout: post
date: 2008-07-01 03:27:57+00:00
categories:
- Architecture
subtitle: Padrões de design para desenvolvimento de software
---

> **Série: Padrões de Projeto e Análise** | **Introdução** > _Desenvolvido durante o Mestrado em Projetos de Sistemas Web_

<style>
.analysis-pattern-img {
  display: block;
  margin: 20px auto;
  max-width: 600px;
  width: 100%;
  height: auto;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
</style>

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

<img src="/uploads/2008/07/picture-2.png" alt="Analysis Pattern - Party" class="analysis-pattern-img">

### Quantity e Unit

Representa um valor numérico com uma unidade (ex: 20 km).

- `Quantity` encapsula valor e unidade
- Suporta operações como `+`, `-`, `*`, `/` entre quantidades compatíveis

<img src="/uploads/2008/07/picture-5.png" alt="Analysis Pattern - Quantity" class="analysis-pattern-img">

### Conversion Ratio

Permite transformar uma `Quantity` de uma unidade para outra.

- `ConversionRatio` liga duas unidades com um fator multiplicador
- Usado em operações como `convertTo(Unit)`

<img src="/uploads/2008/07/picture-6.png" alt="Analysis Pattern - Conversion Ratio" class="analysis-pattern-img">

### Compound Units

Modela unidades compostas como km/h ou R$/m².

- Representa combinações de múltiplas `Unit`
- Suporta sistemas mais avançados de medição

<img src="/uploads/2008/07/compound-units-1.png" alt="Analysis Pattern - Compound Units Basic" class="analysis-pattern-img">

<img src="/uploads/2008/07/compound-units-2.png" alt="Analysis Pattern - Compound Units Detailed" class="analysis-pattern-img">

### Hierarquias Organizacionais

Modela estruturas hierárquicas de forma recursiva.

- `Organization` pode ter um `parent` e várias `subsidiaries`
- Ideal para modelar regiões, divisões, escritórios, etc.

<img src="/uploads/2008/07/picture-3.png" alt="Analysis Pattern - Organization Hierarchies" class="analysis-pattern-img">

### Estrutura Organizacional

Explicita o tipo de relacionamento organizacional.

- Define `Organization Structure Type` (ex: subsidiária, joint venture)
- Separa o relacionamento das entidades envolvidas

<img src="/uploads/2008/07/picture-4.png" alt="Analysis Pattern - Organization Structure" class="analysis-pattern-img">

## Conclusão

Padrões de análise ajudam a visualizar, discutir e construir sistemas mais robustos e alinhados com o mundo real. Eles são reutilizáveis, precisos e economizam horas de discussão.

Em posts futuros, vamos explorar como os **padrões de projeto (design patterns)** complementam esses conceitos na implementação.

---

### **Navegação da Série**

- **Atual**: Introdução - Padrões de Análise
- **Próximo**: [Parte 1 - Padrões de Projeto Overview](../2008-07-02-padroes-de-projeto-detalhado/)
- **Série completa**: [Padrões de Projeto Overview](../2008-07-02-padroes-de-projeto-detalhado/) | [Padrões de Criação](../2008-07-04-padroes-de-criacao/) | [Padrões Estruturais](../2008-07-06-padroes-estruturais/) | [Padrões Comportamentais](../2008-07-08-padroes-comportamentais/)
