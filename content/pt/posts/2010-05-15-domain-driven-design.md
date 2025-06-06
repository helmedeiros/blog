---
title: "Domain-Driven Design na Prática: Construindo Software que Fala Negócio"
author: helio
layout: post
date: 2010-05-15T14:30:22+00:00
description: "Reflexões sobre a décima primeira e última aula de Engenharia de Software, explorando os princípios de Domain-Driven Design e sua aplicação prática no desenvolvimento de software real."
categories:
  - Arquitetura
  - Design
  - DDD
  - Educação
tags:
  - Engenharia de Software
  - Domain-Driven Design
  - Arquitetura
  - Modelagem
  - Lógica de Negócio
  - Linguagem Ubíqua
  - UnP
  - Ensino
  - software-engineering-series
---

> **Série: Fundamentos de Engenharia de Software** | **Parte 11 de 13** > _Ministrada na Universidade Potiguar (UnP) em 2010_

**Na décima primeira aula** da disciplina de Engenharia de Software da Universidade Potiguar (UnP), marcamos uma mudança de tom: não estávamos mais apenas modelando — estávamos enfrentando a complexidade dos sistemas reais de frente. Era hora de dar ao código uma espinha dorsal, uma linguagem comum e uma estratégia para evolução. É aí que o **Domain-Driven Design (DDD)** entra em cena.

## Modelar não é desenhar. É decidir.

Começamos com a técnica parecida com CRC (Classe–Responsabilidade–Colaboração), um método rápido e informal para distribuir responsabilidades entre objetos. Dei à turma histórias reais — como "registrar a entrada de um veículo no estacionamento" — e pedi que modelassem sob pressão de tempo.

Essas atividades vão além do desenho. Elas dizem respeito à **tomada de decisão**: o que importa nesse cenário? O que não importa? Quais classes preciso? O que deve ficar fora do modelo de domínio? Para muitos alunos, foi a primeira vez que entenderam que modelar não é sobre beleza, mas sobre clareza.

Facilitadores podem aplicar essa prática como uma negociação de significado. Pergunte à equipe: "O que estamos realmente tentando dizer aqui?"

## Escolhendo a Arquitetura Certa

Exploramos abordagens arquiteturais como **Table Module**, **Transaction Script** e **Domain Model** — e discutimos quando usar cada uma. Não era um teste de pureza, mas um exercício de adequação.

Os alunos mapearam os níveis de decisão em três dimensões: _O que fazer?_, _Como fazer?_ e _Com que estrutura?_ Isso nos levou ao padrão de Arquitetura em Camadas: dividindo o sistema em Camada de Apresentação, Aplicação, Domínio e Infraestrutura.

Fizemos um exercício onde os grupos simulavam a movimentação de uma funcionalidade entre camadas, caso uma regra de negócio mudasse. O ponto não era decorar padrões, e sim **dar mobilidade** à arquitetura.

## Camadas que Falam

A maioria dos devs ouve "camadas" e pensa em retângulos no PowerPoint. Eu queria que os alunos vissem essas camadas como **canais de comunicação**. A camada de Aplicação não contém regras de negócio — ela coordena. A de Domínio não sabe de banco de dados — ela expressa significado.

Adicionei um desafio: simular uma mudança de estratégia de preço e mapear quais camadas seriam afetadas e por quê. O famoso "efeito dominó". Isso mostrou dependências e reforçou o princípio da separação de responsabilidades.

## O Poder da Linguagem Ubíqua

DDD é sobre linguagem. A **linguagem ubíqua** não é um luxo — é o eixo. Discutimos como termos ambíguos ("ruído sintático" e "ruído semântico") prejudicam a clareza, mesmo que o código compile.

Propus que os alunos reescrevessem histórias de usuário com substantivos e verbos mais precisos, extraídos de discussões reais sobre o domínio. Em seguida, criaram glossários curtos. Times reais podem usar essa dinâmica para quebrar silos e alinhar entendimento.

Mensagem central: se você não domina a linguagem, ela dominará o seu design.

## Blocos de Construção do Modelo

Exploramos os blocos táticos do DDD: **Entidade**, **Objeto de Valor**, **Repositório**, **Serviço**, **Agregado**, **Módulo** e **Fábrica**. Cada conceito foi ligado a exemplos do estacionamento.

Usamos um jogo de associação: cada mesa recebeu cartões com comportamentos típicos (ex: "precisa manter estado" ou "não possui identidade") e teve que identificar o conceito correto.

O objetivo era mais do que decorar — era **reconhecer padrões** que se repetem na prática.

## Conclusão: DDD é Foco, Não Fantasia

O recado final foi direto: DDD não é mágica. Nem difícil. Mas é exigente. Requer escuta, questionamento, consistência e um vocabulário claro entre todas as partes envolvidas.

Seja você aluno, dev ou facilitador, DDD começa com a pergunta: _Sabemos exatamente o que queremos dizer quando falamos dessa funcionalidade?_ Se a resposta for "não muito", o trabalho de design só está começando.

---

_Publicado como parte do diário de aula da disciplina de Engenharia de Software. Hoje aprendemos que Domain-Driven Design não é sobre padrões complexos — é sobre construir software que fala a linguagem do negócio que serve._

## Conclusão da Série

---

### **Navegação da Série**

- **Introdução**: [Parte 1 - Por que Engenharia de Software?](../2010-02-24-software-engineering-purpose/)
- **Anterior**: [Parte 10 - XP na Prática](../2010-05-08-applying-xp-strategies/)
- **Atual**: Parte 11 - Domain-Driven Design
- **Próxima**: [Parte 12 - Requisitos & Testes](../2010-05-22-requirements-validation-tests/)
- **Série completa**: [Por que Engenharia de Software?](../2010-02-24-software-engineering-purpose/) | [Domando a Complexidade](../2010-03-02-complexity-process/) | [Modelo Cascata](../2010-03-10-waterfall-model/) | [Modelos Evolucionários](../2010-03-18-evolutionary-models/) | [Mentalidade Ágil](../2010-03-26-agile-mindset/) | [Scrum Produtividade](../2010-04-03-scrum-productivity/) | [Ciclo Scrum](../2010-04-11-scrum-cycle/) | [XP Qualidade & Coragem](../2010-04-19-xp-quality-courage/) | [XP Princípios & Práticas](../2010-05-01-xp-principles-practices/) | [XP na Prática](../2010-05-08-applying-xp-strategies/) | [Domain-Driven Design](../2010-05-15-domain-driven-design/) | [Requisitos & Testes](../2010-05-22-requirements-validation-tests/) | [Testes de Software](../2010-05-29-software-testing/)
