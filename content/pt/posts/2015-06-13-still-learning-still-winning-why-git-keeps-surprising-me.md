---
title: "Aprendendo e Vencendo: Por Que o Git Ainda Me Surpreende"
date: 2015-06-13T10:00:00-03:00
author: Helio Medeiros
subtitle: Descubra como entrar na ThoughtWorks transformou meu entendimento do Git de domínio individual para ofício coletivo—onde técnicas avançadas se tornam rituais compartilhados e o aprendizado contínuo impulsiona a excelência
tags: ["git", "controle-de-versao", "aprendizado-continuo", "thoughtworks"]
categories: ["Development"]
---

## Um Novo Capítulo, Um Novo Padrão

Em Agosto de 2014, comecei a trabalhar na ThoughtWorks. E mesmo já usando Git há anos—escrevendo posts, liderando times, automatizando tudo—me senti recomeçando.

Por quê? Porque passei a trabalhar com alguns dos técnicos mais brilhantes que já conheci. A maioria mais nova que eu. Muitos com poucos anos de carreira. Mas todos com boas práticas desde o início. Pair programming, TDD, branches curtos, rebase antes do merge, commits semânticos—não era teoria. Era rotina.

Isso mudou tudo. O Git deixou de ser só uma ferramenta. Virou linguagem compartilhada. Ritual. Um sinal de disciplina e cuidado com o código.

## Aprendizado Coletivo Leva ao Domínio

A maior surpresa não foi um comando novo. Foi perceber o quanto o Git pode crescer quando compartilhado com um time maduro.

```bash
git rebase -i HEAD~3
```

Antes, eu usava isso só pra corrigir erro. Na ThoughtWorks, era assim que se moldava o histórico _antes_ de compartilhar. Os commits não eram "bons o bastante"—eram pensados como capítulos. Ler `git log` parecia ler um diário bem editado, não um rascunho barulhento.

Aprendi novos aliases. Vi o rebase interativo ser usado como edição de vídeo. Peguei truques como:

```bash
git commit --fixup <sha>
git rebase -i --autosquash
```

| Comando                       | Pra que serve                      |
| ----------------------------- | ---------------------------------- |
| `rebase -i`                   | Reordenar, agrupar, editar commits |
| `--fixup` + `--autosquash`    | Limpar histórico antes do merge    |
| `log --graph --oneline --all` | Visualizar estrutura de branches   |

E o maior aprendizado? Não espere pra limpar o histórico. Escreva código limpo _e_ histórico limpo desde o começo.

## Git Como Reflexo do Pensamento

Na ThoughtWorks, o Git não era só um passo no processo—era parte do cuidado com o código. As pessoas não sabiam só os comandos. Elas **entendiam** por que fazemos rebase, por que squash, por que evitar merge commits quando possível.

Até resolver conflitos era diferente. Em vez de culpar, a gente investigava com curiosidade. Em vez de apressar o push, refinávamos a história que o repositório iria contar.

Tínhamos hooks. Tínhamos CI. Mas acima de tudo, tínhamos **intenção**.

```bash
git show <sha>
```

Não era só um diff. Era contexto. Mostrava o que mudou, por que, e como se conectava ao que veio antes.

Esse é o tipo de Git que quero usar. Aquele que reflete o que penso, não só o que digito.

| Prática          | Impacto na Colaboração                    |
| ---------------- | ----------------------------------------- |
| Branches curtos  | Feedback rápido, menos conflitos de merge |
| Mensagens limpas | Revisão e debug mais fáceis               |
| Rebase frequente | Histórico linear, mais clareza            |

## Git, Revisitado

Olhando pra trás, o Git me ensinou mais do que estratégias de branch ou comandos obscuros. Me ensinou a pensar. A respeitar o histórico. A me comunicar por meio dos commits.

Entrar na ThoughtWorks abriu meus olhos pro que acontece quando se trabalha com gente que já trata o Git como parte do ofício. Deixei de ser o que ensina. Voltei a ser quem aprende. E isso é a melhor forma de crescer.

O Git ainda me surpreende. Não porque sei pouco. Mas porque sigo cercado de pessoas que mostram até onde ele pode ir quando usado com propósito.

Sim—sigo aprendendo. E é por isso que sigo vencendo.
