---
title: "Dotfiles 2019: De Volta ao Pessoal"
author: helio
layout: post
date: 2019-11-10T10:00:00+00:00
categories: ["Technology", "Agile"]
tags:
  - dotfiles
  - terminal
  - workflow
  - personal
  - simplification
  - back-to-basics
  - individual-craft
  - personal-reset
---

## Depois da Configuração Compartilhada, o Retorno ao Essencial

Em 2018, ajustei meus dotfiles para funcionar melhor em equipe. Criei um `common.zsh`, adicionei comentários amigáveis e tentei deixar tudo mais compartilhável.

Mas este ano, eu senti falta de algo: a velocidade e a precisão de um terminal feito só pra mim.

Então tomei uma decisão: simplificar. Recuperar só o que eu realmente usava. Eliminar tudo que existia só para servir a um público que eu não precisava mais atender.

Essa atualização foi exatamente sobre isso.

## Removendo o `common.zsh`: Uma Subtração Intencional

A mudança mais marcante? Deletei o `common.zsh`.

Não porque algo quebrou — mas porque ele não servia mais meu fluxo de trabalho. Eu não estava mais onboardeando ninguém. Estava resolvendo problemas diferentes, em projetos novos, e precisava que os dotfiles não atrapalhassem.

Com o fim do `common.zsh`, refoquei toda a configuração dentro do `.zshrc.symlink`, com includes diretos e intencionais:

```zsh
source "$ZSH/exports.zsh"
source "$ZSH/aliases.zsh"
source "$ZSH/functions.zsh"
```

| Antes                 | Depois              |
| --------------------- | ------------------- |
| Includes indiretos    | Includes explícitos |
| Foco no compartilhado | Foco no pessoal     |
| Mais flexível         | Mais deliberado     |

Essa mudança tornou tudo mais fácil de depurar — e de manter sob meu controle.

## Padrões Inteligentes, Não Mais Complexos

Não adicionei mais aliases ou funções. Cortei.

Mas os que ficaram tinham propósito:

```zsh
alias gst='git status'
alias gco='git checkout'
alias gcm='git commit -m'
```

Eles refletem meu fluxo real de trabalho.

E mantive os recursos de segurança essenciais:

```zsh
alias cp='cp -i'
alias mv='mv -i'
alias rm='rm -i'
```

| Alias   | Finalidade                 |
| ------- | -------------------------- |
| `gst`   | Git status rápido          |
| `gco`   | Trocar de branch           |
| `gcm`   | Commit com mensagem        |
| `rm -i` | Evitar deleções acidentais |

Menos tentativa e erro. Mais memória muscular.

## PATH e Exports Mais Limpos

Uma melhoria importante: limpei a forma como gerencio o PATH.

```zsh
export PATH="$HOME/bin:$PATH"
```

Só isso.

Removi os exports antigos para Ruby, Node, Python e outros. Esses ambientes agora são gerenciados por projeto com ferramentas como `asdf` ou `direnv`. Onde a configuração deve estar: no projeto, não no shell.

| Antes                     | Depois                   |
| ------------------------- | ------------------------ |
| PATH global por linguagem | Ambiente por projeto     |
| Shell que tenta tudo      | Shell só pronto para uso |

Confiança: confio que cada projeto configure o que precisa. Meu shell só precisa estar pronto.

## Prompt Minimalista, Ainda Meu

Nada mudou no prompt. Ainda uso `vcs_info`, ainda rápido, ainda silencioso:

```zsh
autoload -Uz vcs_info
precmd() { vcs_info }
PROMPT='%n@%m %1~ ${vcs_info_msg_0_}%# '
```

Não toquei porque funciona. Um bom prompt desaparece e te deixa focar no que interessa.

## Um Setup Que Voltou a Ser Meu

A atualização dos dotfiles em 2019 não foi chamativa. Foi um suspiro. Um retorno a um shell que reflete meu jeito de trabalhar — e não o que eu achava que os outros precisavam.

Me ajudou a:

- Começar o dia mais rápido
- Evitar sobrecarga desnecessária
- Reduzir fricção ao depurar problemas
- Sentir que estou em casa em qualquer máquina

Esse é o objetivo.

→ [Veja o diff no GitHub](https://github.com/helmedeiros/dotfiles/compare/8303f8a805e3713e44298b4b976d24cea964f4c8...f496fe8a1ab4a7a040e825f3b34c7d2d17dcb324)
