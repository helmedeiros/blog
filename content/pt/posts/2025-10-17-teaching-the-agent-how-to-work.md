---
title: "Ensinando o Agente a Trabalhar: Claude Code, Skills e Colaboração Agêntica"
categories:
  - AI
  - Engineering
  - Software Architecture
date: 2025-10-17
tags:
  - ai
  - claude-code
  - fluxos-agenticos
  - clean-code
  - arquitetura-hexagonal
  - developer-experience
  - engenharia-de-workflow
description: "Uma vez que seu codebase está pronto para agentes, o próximo desafio é ensinar o agente a se comportar. Skills transformam disciplina de engenharia em protocolos executáveis."
subtitle: "Arquitetura define onde a lógica pertence. Skills definem como a mudança acontece."
---

No artigo anterior, argumentei que produtividade com agentes não é principalmente um problema de ferramenta. É um problema de arquitetura.

Se o seu repositório é ambíguo, agentes amplificam ambiguidade. Se as fronteiras são porosas, eles replicam os padrões errados. Se a validação é lenta ou inconsistente, a iteração se torna cara.

Aquele artigo foi sobre estrutura.

Este é sobre comportamento.

Porque, uma vez que seu codebase está preparado para agentes, surge uma nova pergunta: como ensinar o agente a se comportar como um engenheiro disciplinado dentro dessa estrutura?

Para responder isso, precisamos falar sobre Claude Code e sobre o conceito de skills.

## O que Claude Code realmente é

A maioria dos desenvolvedores já utilizou ferramentas de IA baseadas em chat que geram trechos de código. Esse modelo de interação é essencialmente conversacional. Você descreve um problema, o modelo sugere uma solução, e você aplica manualmente.

Claude Code opera de maneira diferente.

Ele é uma interface agêntica construída sobre um modelo de linguagem. Em vez de apenas produzir texto, ele pode interagir diretamente com o seu repositório. Ele lê arquivos, modifica-os, executa comandos de terminal, inspeciona resultados de testes e itera com base nas falhas.

Essa diferença é significativa.

Você deixa de colaborar com um gerador de sugestões e passa a trabalhar com um loop autônomo que pode:

1. Inspecionar o estado atual do sistema.
2. Propor uma mudança.
3. Validar essa mudança executando comandos.
4. Refinar a alteração com base no feedback.
5. Produzir um diff estruturado.

Isso move a IA de assistência para participação. E quando o sistema participa ativamente, disciplina de workflow deixa de ser opcional.

## O problema invisível: deriva comportamental

Em Março, quando comecei a usar Claude Code em projetos reais, percebi algo sutil.

Mesmo em um repositório bem estruturado, o comportamento do agente variava de sessão para sessão.

Às vezes fazia mudanças mínimas e precisas. Às vezes tocava arquivos demais. Às vezes colocava lógica corretamente no domínio. Às vezes introduzia comportamento em adaptadores porque era o caminho mais curto para fazer os testes passarem.

Nada era catastrófico. Mas era inconsistente.

E inconsistência gera fricção.

Times humanos também enfrentam isso. Intenção arquitetural se degrada com o tempo. Convenções enfraquecem. Padrões se tornam opcionais.

Com agentes, essa deriva acontece mais rápido, porque eles amplificam padrões existentes. Eles não "sentem" que algo está levemente fora do lugar. Eles reproduzem o que encontram.

Foi nesse momento que ficou claro: arquitetura limita _onde_ a mudança acontece. Mas algo precisa limitar _como_ a mudança acontece.

## Skills como contratos comportamentais

No começo deste mês, Claude Code introduz o conceito de skills.

Uma skill não é uma feature. Não é um template de prompt. É um protocolo de execução reutilizável que passa a fazer parte do contexto operacional do agente.

Para entender isso, ajuda pensar em colaboração humana.

Quando você integra um novo engenheiro sênior ao time, você não apenas dá acesso ao repositório. Você explica:

- Como o time aborda mudanças.
- Em que ordem o código costuma ser alterado.
- Como validação deve acontecer.
- O que significa considerar algo "pronto".

Uma skill codifica essa explicação uma única vez.

Em vez de repetir instruções comportamentais em cada prompt, você as define estruturalmente. A partir daí, elas moldam como o agente executa tarefas.

Isso transforma a interação de ajustes conversacionais para disciplina operacional.

## Por que isso não é prompt engineering

Prompt engineering foca em redação. Tenta guiar o resultado por meio de melhor formulação.

Skills focam em sequência e restrição. Elas definem ordem de execução, gates de validação e expectativas arquiteturais.

Quando eu precisava escrever repetidamente algo como:

> _Identifique o caso de uso primeiro. Modifique o domínio antes dos adaptadores. Adicione testes. Execute `make test` e `make lint`. Mantenha o diff pequeno._

Eu estava injetando disciplina manualmente.

No momento em que esquecia de escrever isso, a qualidade diminuía.

Essa fragilidade não escala.

Skills resolvem isso ao embutir disciplina no próprio modelo de execução.

## Projetando skills com consciência arquitetural

Como meus repositórios seguem arquitetura hexagonal, as skills que crio refletem essa estrutura.

Arquitetura hexagonal separa:

- **Domínio** — lógica pura, sem dependências externas.
- **Coordenação de aplicação** — orquestração de casos de uso.
- **Portas** — interfaces que definem fronteiras.
- **Adaptadores** — implementações de infraestrutura.
- **Composition root** — onde dependências são conectadas.

Essa separação cria restrições direcionais: o domínio não depende de adaptadores.

As skills reforçam essa restrição no comportamento.

> Em vez de dizer ao agente _o que_ construir, eu defino _como_ se mover.

Primeiro localizar o caso de uso. Depois modificar a lógica de domínio. Depois validar com testes unitários. Só então atualizar adaptadores. E apenas após validação finalizar o diff.

Isso é a operacionalização da intenção arquitetural.

## Como uma skill se parece na prática

Uma versão simplificada de uma das skills que utilizo:

```text
Você está trabalhando em um repositório que segue arquitetura hexagonal.

Protocolo de execução:

1. Identifique o caso de uso responsável pelo comportamento solicitado.
2. Modifique primeiro as camadas de domínio e aplicação.
3. Adicione ou atualize testes unitários cobrindo o comportamento.
4. Só então atualize adaptadores e wiring.
5. Execute make test e make lint.
6. Garanta que o diff seja mínimo e isolado.
7. Forneça um resumo agrupado por camada arquitetural.
```

Perceba que isso não descreve uma funcionalidade. Descreve um fluxo de trabalho.

O fluxo existe independentemente da tarefa específica. É essa independência que o torna reutilizável.

## De hábito pessoal a restrição do sistema

No desenvolvimento tradicional, disciplina de engenharia vive em:

- Code reviews.
- Acordos de time.
- Documentação arquitetural.
- Memória institucional.

Com agentes, disciplina também precisa existir em forma executável.

Se a disciplina vive apenas na sua cabeça, o agente não a herdará.

Quando comecei a publicar meu conjunto de skills em [clean-code-skills](https://github.com/helmedeiros/clean-code-skills), a intenção não era criar algo inovador. Era tornar explícitos meus próprios hábitos.

Diffs mínimos. Mudanças começando pelo domínio. Validação antes da conclusão. Resumo arquitetural estruturado.

Não são ideias sofisticadas. São ideias consistentes.

E consistência acumula.

## Colaboração agêntica como sistema

Quando estrutura do repositório e skills estão alinhadas, a colaboração muda.

A interação deixa de ser correção reativa. Passa a ser intenção combinada com protocolo.

O agente lê o repositório. A skill define a sequência. O CI impõe validação. O diff respeita fronteiras arquiteturais.

Isso é autonomia com restrição.

Autonomia sem restrição gera deriva. Restrição sem autonomia gera estagnação. O objetivo é iteração disciplinada.

## Por que isso importa agora

A conversa da indústria ainda está centrada em modelos. Qual modelo escreve melhor? Qual raciocina melhor? Qual alucina menos?

Essas perguntas são válidas, mas incompletas.

Quando agentes operam dentro de repositórios reais, o fator limitante passa a ser estabilidade de workflow.

Um modelo forte dentro de um workflow caótico produzirá iteração caótica. Um workflow disciplinado amplifica mesmo capacidades moderadas.

> Essa é a transição de prompt engineering para workflow engineering.

Repositórios codificam estrutura. Skills codificam comportamento. CI codifica validação. O agente executa.

Quando essas camadas se alinham, os resultados se tornam repetíveis.

## Reflexão final

Um codebase amigável para agentes torna mudanças seguras possíveis. Skills tornam mudanças disciplinadas previsíveis.

Se arquitetura define onde a lógica pertence, skills definem como a mudança acontece.

O modelo não ficou mais responsável.

Nós tornamos a responsabilidade executável.
