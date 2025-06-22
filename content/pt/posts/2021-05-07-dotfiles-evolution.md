---
title: "Dotfiles 2021: Preparando Para Escalar a Mim Mesmo"
author: helio
layout: post
date: 2021-05-07 10:00:00+00:00
categories:
  - Technology
  - Architecture
tags:
  - dotfiles
  - remote-work
  - bootstrap
  - scaling
  - portability
  - simplification
  - repeatability
  - developer-experience
subtitle: Transforme seu ambiente de desenvolvimento pessoal em um sistema escalável e portável—com clareza de bootstrap, estrutura simplificada e compartilhamento sem atrito
---

## Dois Anos Depois, Mesmas Ferramentas, Nova Intenção

Em 2021, eu não adicionei muitas funcionalidades aos meus dotfiles — mas mudei a forma como os usava.

Duas coisas mudaram: o trabalho remoto se tornou padrão, e meu setup pessoal começou a ser copiado com mais frequência — por colegas, colaboradores ou apenas entre máquinas minhas.

Então eu quis deixar uma coisa clara: esse sistema precisava escalar _a mim_. Isso significava menos bagunça, menos mágica e mais repetibilidade.

Essa atualização é silenciosa. Mas cheia de propósito.

## Introduzindo `bootstrap.zsh`: Comece Com Clareza

A principal adição desse ciclo foi um novo arquivo: `bootstrap.zsh`.

Sua função? Encapsular todo o bootstrapping do ambiente em um único lugar. Nada de aliases, nada de funções — apenas o que prepara o ambiente para o restante funcionar.

```zsh
# bootstrap.zsh
export DOTFILES="$HOME/.dotfiles"
export PATH="$HOME/bin:$PATH"
```

Esse arquivo deixou o `.zshrc.symlink` mais limpo, mais focado, e mais fácil de entender.

| Arquivo          | Responsabilidade               |
| ---------------- | ------------------------------ |
| `.zshrc.symlink` | Apenas faz os includes         |
| `bootstrap.zsh`  | Define variáveis de ambiente   |
| `aliases.zsh`    | Lógica de atalhos (ainda leve) |

Deu ao repositório uma sensação de intenção renovada.

## `.zshrc.symlink` Mais Simples

Reescrevi o `.zshrc.symlink` para ser praticamente vazio:

```zsh
source "$DOTFILES/bootstrap.zsh"
source "$DOTFILES/aliases.zsh"
source "$DOTFILES/functions.zsh"
```

Sem lógica. Sem condicionais. Apenas includes.

Essa separação tornou trivial debugar ou reutilizar pedaços individualmente.
Quer só o `aliases.zsh` em uma VM descartável? Fácil. Quer testar o bootstrap em uma máquina limpa? Vai fundo.

## Reconfirmando Prioridades: Simplicidade e Portabilidade

Com mais setups remotos e vários laptops em uso, portabilidade passou a importar mais.

Essa atualização não adicionou complexidade — removeu suposições. Nada de paths com nome de usuário, ajustes por host ou lógica específica por máquina.

Tudo parte de `$DOTFILES`. Tudo assume o caminho mais simples.

```zsh
export PATH="$HOME/bin:$PATH"
```

Essa linha diz mais do que parece. Ela diz: "não preciso de um framework — só preciso não tropeçar em mim mesmo."

## Um Shell Que Inicia Rápido e Pensa Menos

Não mexi no prompt. Ainda é `vcs_info`, ainda silencioso, ainda meu:

```zsh
autoload -Uz vcs_info
precmd() { vcs_info }
PROMPT='%n@%m %1~ ${vcs_info_msg_0_}%# '
```

O que _eu_ fiz foi remover lógica de runtime que não precisava rodar a cada boot. Bootstrap é sobre preparar — depois que funciona, o terminal só precisa carregar rápido.

Menos condicionais. Menos caminhos alternativos. Mais confiança de que tudo simplesmente funciona.

## Sem Reinvenção. Apenas um Reboot Cuidadoso.

Não tem fogos de artifício nesse post. Nenhuma nova ferramenta incrível ou CLI obscura. Apenas uma reconstrução cuidadosa da fundação.

2021 foi sobre:

- Compartilhar meu setup sem atrito
- Reinicializar máquinas com facilidade
- Separar lógica para melhor reutilização
- Escalar o que funciona — e abandonar o que não precisa

→ [Veja o diff no GitHub](https://github.com/helmedeiros/dotfiles/compare/f496fe8a1ab4a7a040e825f3b34c7d2d17dcb324...2f3256ec7595f125e946958c6820305fb939943b)
