---
title: Requisitos, Validação e o Papel dos Testes
author: helio
date: 2010-05-22 14:30:22+00:00
description: Reflexões sobre a décima segunda e última aula de Engenharia de Software,
  explorando engenharia de requisitos, práticas de validação e a conexão crítica entre
  requisitos claros e testes eficazes.
categories: ["Development"]
tags:
- Engenharia de Software
- Engenharia de Requisitos
- Validação
- Testes
- TDD
- Garantia de Qualidade
- User Stories
- Critérios de Aceitação
- UnP
- Ensino
- software-engineering-series
subtitle: Conceitos e práticas de desenvolvimento de software
---

> **Série: Fundamentos de Engenharia de Software** | **Parte 12 de 19** > _Ministrada na Universidade Potiguar (UnP) em 2010_

Foi nessa aula que decidi unir dois temas que costumam ser ensinados separadamente no início da formação em engenharia de software: **engenharia de requisitos** e **testes de software**. Muitos estudantes os veem como trilhas diferentes, mas na prática, são dois lados do mesmo espelho. Não é possível escrever testes significativos sem requisitos claros, nem avaliar qualidade sem saber o que foi pedido.

## Definindo o Problema Antes da Solução

Abrimos a aula revisitando a ideia de **visão de produto**. Pedi aos alunos que a escrevessem em linguagem natural, sem UML ou pseudocódigo. Um único parágrafo. Algo que a avó deles pudesse ler e entender.

Por quê? Porque se você não consegue explicar o problema sem usar a linguagem da solução, provavelmente ainda não entendeu o problema.

Essa abordagem constrói uma base para colaboração com stakeholders que não falam a linguagem técnica—e ensina engenheiros a focar em **valor, não em funcionalidades**.

## Requisitos que Não Escondem a Verdade

Usei novamente a definição de McConnell: "requisitos descrevem em detalhe o que o sistema deve fazer." Mas fomos além, analisando o que torna um requisito realmente útil:

- Evita suposições.
- Dá chance de validação com o usuário.
- Reduz a margem de interpretação pessoal.

Distinguimos requisitos **funcionais** e **não funcionais** e desafiei os times a escolherem um app real (rastreador de ônibus, editor de fotos, carrinho de e-commerce) e reescrever um de cada tipo com base nas diretrizes de Sommerville.

Um dos grupos percebeu que não conseguia especificar metas de desempenho sem antes entrevistar usuários sobre suas expectativas. Esse momento foi ouro—mostrou que a elicitação real começa _depois_ de você achar que já terminou.

## Elicitar Requisitos Não é um Roteiro—É um Diálogo

Exploramos cinco técnicas clássicas de elicitação de requisitos:

- Brainstorming
- Entrevistas
- Sessões JAD
- Planning Poker
- Jogo de Planejamento (XP)

Mas destaquei: não existe bala de prata. O **melhor** método de elicitação é aquele que funciona com seu stakeholder, sua cultura e maturidade do time. Para equipes iniciantes, recomendei parear devs com usuários reais em conversas estruturadas.

Os alunos praticaram entrevistas em duplas e tentaram converter as falas em requisitos formais. As interpretações equivocadas foram oportunidades de aprendizado: seu ouvido não ouve o que seus filtros inconscientes não deixam passar.

## Validando e Verificando Desde o Início

Discutimos como **validar** requisitos com perguntas como:

- São realistas?
- Estão completos?
- São mensuráveis e testáveis?
- São consistentes?

Introduzimos o princípio de "falhar rápido": se seus requisitos não passam nesses testes, pare de codar. Corrija-os antes. Do contrário, você só está transferindo risco para o time de testes ou suporte.

Pedi que os grupos revisassem suas últimas entregas usando esses critérios. Alguns perceberam que sua última "user story" sequer tinha critérios de aceitação testáveis. Mais um ótimo momento de aprendizado.

## Conectando Requisitos e Testes

Encerramos com um ponto central: mostrar que testes não são **a fase final**, mas o ciclo de feedback que valida se os requisitos estavam claros.

Abordamos:

- O que torna um requisito testável
- Tipos de teste: unitário, integração, UI, desempenho
- O conceito de **TDD** e sua ligação com clareza de requisito

Usei um exemplo simples:

**Requisito:** "O usuário deve receber um e-mail até 2 minutos após o cadastro."

Escrevemos um teste que simula o cadastro e valida o envio do e-mail. A mensagem foi clara: um requisito só está claro quando é testável. Se você não consegue escrever o teste, precisa reescrever o requisito.

## Além da Aula

O que espero que tenham levado não foi só como escrever bons requisitos, mas como _identificar ambiguidades_, _fazer perguntas mais certeiras_ e _criar alinhamento logo no início_.

Qualquer facilitador—numa empresa ou universidade—pode replicar esse formato. Basta pegar uma user story real, decompor em requisitos, validar, e escrever os testes.

Não é waterfall. É **ser deliberado com os fundamentos**.

<div style="margin-bottom: 20px;">
<iframe src="https://www.slideshare.net/slideshow/embed_code/key/2cRKFh4w7E7J6J?startSlide=1" width="597" height="486" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px;max-width: 100%;" allowfullscreen></iframe> <div style="margin-bottom:5px"><strong> <a href="https://pt.slideshare.net/slideshow/unp-eng-software-aula-25/4328153" title="UnP Eng. Software - Aula 25" target="_blank">UnP Eng. Software - Aula 25</a> </strong> from <strong> <a href="https://www.slideshare.net/heliomedeiros" target="_blank">Hélio Medeiros</a> </strong></div></div>

---

_Publicado como parte do diário da disciplina de Engenharia de Software. Hoje aprendemos que requisitos e testes não são disciplinas separadas — são práticas complementares que garantem que construamos a coisa certa, do jeito certo._

---

### **Navegação da Série**

- **Introdução**: [Parte 1 - Por que Engenharia de Software?](../2010-02-24-software-engineering-purpose/)
- **Anterior**: [Parte 11 - Domain-Driven Design](../2010-05-15-domain-driven-design/)
- **Atual**: Parte 12 - Requisitos & Testes
- **Próxima**: [Parte 13 - Testes de Software](../2010-05-29-software-testing/)
- **Série completa**: [Por que Engenharia de Software?](../2010-02-24-software-engineering-purpose/) | [Domando a Complexidade](../2010-03-02-complexity-process/) | [Modelo Cascata](../2010-03-10-waterfall-model/) | [Modelos Evolucionários](../2010-03-18-evolutionary-models/) | [Mentalidade Ágil](../2010-03-26-agile-mindset/) | [Scrum Produtividade](../2010-04-03-scrum-productivity/) | [Ciclo Scrum](../2010-04-11-scrum-cycle/) | [XP Qualidade & Coragem](../2010-04-19-xp-quality-courage/) | [XP Princípios & Práticas](../2010-05-01-xp-principles-practices/) | [XP na Prática](../2010-05-08-applying-xp-strategies/) | [Domain-Driven Design](../2010-05-15-domain-driven-design/) | [Requisitos & Testes](../2010-05-22-requirements-validation-tests/) | [Testes de Software](../2010-05-29-software-testing/)
