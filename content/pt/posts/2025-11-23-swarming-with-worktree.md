---
title: "Swarmando o Codebase: Execução Orquestrada com Múltiplos Agentes Claude Code"
categories:
  - AI
  - Engineering
  - Software Architecture
date: 2025-11-23
tags:
  - ai
  - claude-code
  - fluxos-agenticos
  - git
  - git-worktree
  - swarming
  - developer-experience
description: "Quando um agente não basta, swarming com git worktree transforma execução paralela de IA de caos em colaboração estruturada. Isolamento é o primitivo. Git é o orquestrador."
subtitle: "Agentes em paralelo sem isolamento não é aceleração. É entropia."
---

Eu tinha três funcionalidades para entregar. Cada uma bem delimitada: uma nova política de domínio, uma regra de validação e um adaptador para uma API externa. O codebase estava limpo. As skills estavam carregadas. O contrato do agente estava funcionando.

Então fiz o que parecia natural. Abri três painéis no terminal, iniciei o Claude Code em cada um e apontei todos para o mesmo repositório.

Em minutos, dois agentes editaram o mesmo arquivo. Um sobrescreveu as mudanças do outro. O terceiro agente rodou testes que falharam porque o diretório de trabalho estava em um estado que nenhum dos dois esperava.

Foi nesse momento que entendi: o gargalo não era mais sobre ensinar um agente a trabalhar. Era sobre ensinar múltiplos agentes a coexistir.

## Onde isso se encaixa na série

No [primeiro artigo]({{< ref "2025-08-07-agent-friendly-codebase" >}}), argumentei que um codebase amigável para agentes reduz a ambiguidade sobre *onde* as mudanças pertencem. Arquitetura hexagonal, comandos padrão, loops de feedback rápidos.

No [segundo]({{< ref "2025-10-17-teaching-the-agent-how-to-work" >}}), explorei como skills codificam *como* as mudanças acontecem. Protocolos de execução, gates de validação, resumos de diff por camada.

No [terceiro]({{< ref "2025-10-30-interactive-planning-specification-boundaries" >}}), abordei *o que* deve ser construído através do Plan Mode e perguntas interativas.

Este artigo trata do próximo desafio: **como escalar a execução quando um agente não é suficiente?**

| Camada | Pergunta que responde | Mecanismo |
| --- | --- | --- |
| Estrutura | Onde a mudança pertence? | Arquitetura, fronteiras, comandos padrão |
| Comportamento | Como a mudança deve acontecer? | Skills, protocolos de execução, validação |
| Intenção | O que exatamente deve ser construído? | Plan Mode, perguntas interativas |
| **Execução** | **Como múltiplos agentes trabalham em paralelo?** | **Git worktree, isolamento por branch, integração controlada** |

Cada camada resolveu uma classe diferente de problemas. Mas nenhuma delas tratou de concorrência. E concorrência é onde a próxima fricção se esconde.

## O que swarming significa na prática

Em times tradicionais de software, swarming significa múltiplos engenheiros colaborando simultaneamente no mesmo problema. Todos convergem, se comunicam e integram em tempo real.

Em sistemas agenticos, swarming significa orquestrar múltiplos agentes de IA trabalhando em paralelo no mesmo repositório, com fronteiras controladas e integração coordenada.

Não se trata de caos. Trata-se de **paralelismo estruturado**.

A distinção importa. Jogar mais agentes em um problema sem isolamento não produz mais resultado. Produz mais conflitos, mais estado quebrado e mais tempo desfazendo o que deu errado.

> Swarming não é sobre mais agentes. É sobre mais agentes com fronteiras.

## Executando múltiplas instâncias do Claude Code

Claude Code roda no terminal. Isso torna o paralelismo mecanicamente simples.

Com tmux, crio uma sessão e divido em painéis:

```bash
tmux new-session -s swarm
```

Cada painel recebe sua própria instância do Claude:

```bash
claude
```

Três painéis, três agentes, três fluxos concorrentes de trabalho. A configuração leva segundos.

Mas aqui está o problema: os três agentes compartilham o mesmo diretório de trabalho. Leem os mesmos arquivos. Escrevem nos mesmos arquivos. Rodam testes contra o mesmo estado.

Isso não é paralelismo. É uma condição de corrida.

## Git worktree como primitivo de isolamento

A solução é enganosamente simples. `git worktree` permite múltiplos diretórios de trabalho ligados ao mesmo repositório, cada um acompanhando uma branch diferente.

```bash
git worktree add ../feature-policy feature/policy
git worktree add ../feature-validation feature/validation
git worktree add ../feature-adapter feature/adapter
```

Agora cada instância do Claude opera em seu próprio diretório, em sua própria branch, com seu próprio estado de arquivos. Nenhum agente pode acidentalmente sobrescrever o trabalho de outro.

| Sem worktree | Com worktree |
| --- | --- |
| Agentes compartilham um diretório | Cada agente tem um diretório isolado |
| Escritas em arquivo conflitam silenciosamente | Escritas são delimitadas por branch |
| Testes refletem estado misturado | Testes refletem estado de uma única branch |
| Integração é acidental | Integração é deliberada |

O modelo mental é direto: cada worktree é um sandbox. Cada sandbox tem sua própria branch. Os agentes nunca tocam nos sandboxes uns dos outros.

O que me surpreendeu foi como isso pareceu natural. Espelha como engenheiros experientes trabalham em time: cada um tem sua própria branch, seu próprio estado local, e a integração acontece por pull requests, não por mutação compartilhada.

## Git como orquestrador

Uma vez que cada agente opera em um worktree isolado, Git deixa de ser apenas controle de versão. Torna-se a camada de orquestração.

Git cumpre quatro papéis simultaneamente:

- **Mecanismo de isolamento** — worktrees mantêm agentes separados.
- **Fronteira de integração** — merges acontecem deliberadamente, não acidentalmente.
- **Detector de conflitos** — quando dois agentes tocam preocupações sobrepostas, Git revela o conflito no momento do merge, não no momento da edição.
- **Mecanismo de rollback** — se um agente produz um resultado ruim, descartar uma branch é trivial.

Esse não é um fluxo novo. É a mesma colaboração baseada em branches que times humanos usam há anos. A diferença é que os "membros do time" são agentes de IA executando em paralelo, e o tempo de ciclo é minutos em vez de dias.

> Git não se importa se quem fez o commit é humano ou agente. Isso é exatamente o que o torna o primitivo de orquestração certo.

## O fluxo na prática

Aqui está como uma sessão típica de swarming funciona para mim agora:

```text
1. Decompor a tarefa em unidades de trabalho independentes
2. Criar um worktree e uma branch para cada unidade
3. Iniciar uma instância do Claude em cada worktree
4. Deixar os agentes executarem em paralelo
5. Revisar cada branch independentemente
6. Integrar branches na main via pull requests
```

A etapa de decomposição é crítica. Swarming só funciona quando as unidades de trabalho são genuinamente independentes. Se dois agentes precisam modificar o mesmo arquivo ou a mesma entidade de domínio, o merge será doloroso independente do isolamento.

Em uma arquitetura hexagonal, independência se mapeia naturalmente para fronteiras arquiteturais:

| Unidade de trabalho | Camada arquitetural | Por que é independente |
| --- | --- | --- |
| Nova política de domínio | Domínio | Lógica pura, sem dependências de adaptador |
| Regra de validação | Aplicação | Usa portas existentes, sem novos adaptadores |
| Adaptador de API externa | Adaptador | Implementa uma interface de porta existente |

Quando a arquitetura suporta separação limpa, swarming se torna uma extensão natural do design.

## Disciplina é inegociável

Agentes paralelos amplificam deriva se a estrutura for fraca.

Sem fronteiras arquiteturais claras, agentes desviam. Sem commits pequenos, revisar cada branch se torna caro. Sem testes determinísticos, não dá para confiar que um teste passando em um worktree significa que a mudança está correta. Sem paridade com CI, sucesso local vira um sinal falso.

Os pré-requisitos são os mesmos de todos os artigos desta série:

- Fronteiras arquiteturais claras
- Commits pequenos e focados
- Testes determinísticos
- Paridade entre comandos locais e CI

Swarming não relaxa esses requisitos. Torna-os mais urgentes. Um único agente indisciplinado produz uma bagunça. Três agentes indisciplinados produzem três bagunças que conflitam entre si.

> Swarming colapsa em entropia no momento em que as restrições deixam de ser respeitadas.

## O que swarming não é

É tentador ver swarming como uma forma de "jogar mais computação no problema." Esse enquadramento perde o ponto.

Swarming não é velocidade a qualquer custo. É **paralelismo seguro**. O objetivo não é produzir mais código mais rápido. O objetivo é produzir mais código *correto* concorrentemente, com cada fluxo de trabalho independentemente verificável.

Se a decomposição estiver errada, swarming piora as coisas. Se a arquitetura não suportar fronteiras limpas, swarming expõe cada costura. Se os agentes não tiverem skills e contratos, swarming multiplica a deriva comportamental.

Isso não é um atalho. É um amplificador. E amplificadores são tão bons quanto o sinal que recebem.

## Próximo passo

Isso ainda é orquestração primitiva. Cada agente opera independentemente, sem consciência do que os outros estão fazendo. A decomposição é manual. A coordenação é mediada pelo Git. A revisão é branch por branch.

O próximo passo é especialização: li que a Anthropic lançou sub-agentes, e isso parece uma forma interessante de lidar com preocupações específicas dentro de uma tarefa maior, coordenados por um agente principal que compreende o escopo completo. Não apenas execução paralela, mas execução hierárquica.

Mas isso é um momento diferente para aprender e um artigo para escrever.

Por enquanto, a lição é esta: os mesmos princípios que tornam um codebase amigável para um agente — estrutura, skills, clareza de intenção — são exatamente o que torna possível múltiplos agentes trabalharem em paralelo sem destruir o progresso uns dos outros.

Swarming não é sobre mais agentes.

É sobre paralelismo estruturado. E paralelismo estruturado começa com isolamento.
