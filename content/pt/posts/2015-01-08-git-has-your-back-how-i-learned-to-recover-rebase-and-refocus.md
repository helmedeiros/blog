---
title: "Git Te Cobre: Como Aprendi a Recuperar, Rebasear e Reencontrar o Foco"
date: 2015-01-08T10:00:00-03:00
author: Helio Medeiros
subtitle: Descubra como os comandos de recuperação do Git e rebase interativo transformaram minha relação com controle de versão—do medo e pânico para confiança e velocidade
tags: ["git", "recuperacao", "rebase", "produtividade", "debugging"]
categories: ["Development"]
---

## Quando o Pânico Encontra o Poder

Foi numa noite de janeiro que achei que tinha destruído tudo. Dei reset no branch errado e perdi um dia inteiro de trabalho. Fiquei parado olhando o terminal. As mãos gelaram. A primeira reação foi abrir o Slack e escrever: "ferrei tudo".

Mas antes de apertar enter, parei. Lembrei de algo que tinha visto semanas antes: `git reflog`. Um comando que eu nunca tinha usado. Digitei na esperança.

E lá estava. Um rastro de onde o HEAD tinha passado. Eu não estava perdido—só precisava de alguns comandos pra recuperar tudo. E esse momento mudou meu jeito de pensar.

O Git não era uma ameaça. Era uma máquina do tempo. E se eu aprendesse a usá-la, ia trabalhar com mais confiança do que nunca.

## Recuperar é uma Habilidade

Muita gente encara o Git como uma bomba-relógio. Mas ele é mais gentil do que parece—se você souber onde procurar.

Esses comandos viraram meus aliados:

```bash
git reflog
git reset --hard HEAD@{1}
git cherry-pick
git stash pop
```

| Comando            | Para Que Serve                            |
| ------------------ | ----------------------------------------- |
| `git reflog`       | Ver histórico de movimentação do HEAD     |
| `git reset --hard` | Voltar para um estado anterior conhecido  |
| `git cherry-pick`  | Recuperar commits específicos             |
| `git stash pop`    | Restaurar mudanças salvas temporariamente |

Esses comandos me deram poder sobre meus erros. Em vez de temer perda, comecei a explorar o histórico. Em vez de refazer tudo, aprendi com o que _quase_ perdi.

Isso mudou meu jeito de trabalhar. Fiquei mais ousado, mas também mais intencional. O Git me dava essa rede de segurança.

## Rebase Vale o Esforço

Rebase me dava medo. Só de ouvir "rebase interativo" eu travava. Mas chegou a hora. Meus PRs estavam confusos. Os commits fora de ordem. Os colegas perdiam tempo tentando entender o que importava.

Comecei com o básico:

```bash
git rebase -i HEAD~3
```

Aos poucos fui reescrevendo mensagens, agrupando commits e organizando o histórico.

| Tarefa                   | Operação no Rebase               |
| ------------------------ | -------------------------------- |
| Corrigir erros pequenos  | `reword`                         |
| Reordenar commits        | Mover linhas no editor do rebase |
| Agrupar trabalho similar | `fixup` ou `squash`              |
| Remover mudanças inúteis | `drop`                           |

No começo, era lento. Mas depois fez sentido. Rebase não era reescrever história—era _deixá-la mais clara_.

Hoje, não abro PR sem revisar meu histórico. É parte do meu respeito pelo tempo da equipe. E uma forma de liderar—mesmo no código.

## Git é Sobre Crescimento

O Git não guarda só seu código. Ele revela seu comportamento.

Você é cuidadoso? Bagunceiro? Repete os erros ou aprende com eles?

Aprender a recuperar me deu calma. Aprender rebase me deu clareza. Juntos, me deram velocidade.

Da próxima vez que algo der errado, não entre em pânico. Abre o terminal. Confie nas ferramentas. O Git te cobre.

Erros não são o fim. Com Git, são só um novo começo.
