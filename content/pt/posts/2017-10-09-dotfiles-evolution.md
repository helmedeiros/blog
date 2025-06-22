---
title: "Dotfiles 2017: Cortando Ainda Mais Fundo"
author: helio
layout: post
date: 2017-10-09 10:00:00+00:00
categories:
  - Development

tags:
  - dotfiles
  - shell
  - zsh
  - minimalismo
  - refatoração
  - aliases
  - simplificação
  - pruning
subtitle: Alcance clareza no terminal através de poda implacável—eliminando loaders mágicos, scripts não utilizados e complexidade de plataforma para criar um ambiente de desenvolvimento rápido, honesto e sustentável
---

## Um Ano Depois: Hora de Podar

Meus dotfiles estão estáveis. Modulares, com carregamento dinâmico, apoiados por um script de instalação simples que funcionam bem. Mas comecei a sentir uma nova fricção: saber que certas coisas ainda estam ali... só porque sempre estiveram.

Essa atualização foi sobre honestidade. Passei por cada arquivo e me perguntei: ainda uso isso? Sentiria falta se sumisse?

Spoiler: na maioria das vezes, a resposta foi "não."

## Sem Mágica: Adeus load.zsh

Uma das primeiras coisas a ir embora foi o `load.zsh`. Ele percorria e carregava todo arquivo `.zsh` na pasta. Funcionava — até parar de funcionar.

Com o tempo, acumulei scripts `.zsh` esquecidos que eram carregados sem muito critério. Eles não estavam errados. Mas também não eram necessários.

Removi o loader mágico. Agora, cada arquivo é incluído explicitamente no `.zshrc.symlink`:

```zsh
source "$ZSH/aliases.zsh"
source "$ZSH/functions.zsh"
source "$ZSH/prompt.zsh"
```

| Antes (`load.zsh`) | Depois (`source` direto) |
| ------------------ | ------------------------ |
| Loop automático    | Inclusão explícita       |
| Inclui tudo        | Escolhido a dedo         |
| Pode ser esquecido | Difícil de ignorar       |

Essa mudança deixou claro quais arquivos importam — e quais não.

## Aliases Mais Seguros por Padrão

Essa versão trouxe um comportamento de shell mais seguro. Coisas simples que me protegem de mim mesmo.

```bash
alias cp='cp -i'
alias mv='mv -i'
alias rm='rm -i'
```

Incomoda no começo. Mas depois de alguns meses, você percebe: talvez nunca tenha sido boa ideia sobrescrever ou apagar arquivos sem aviso.

Junto com `alias ls='ls -GFh'`, agora tenho:

- listagens legíveis
- operações protegidas
- comportamento consistente entre máquinas

| Alias   | Finalidade                        |
| ------- | --------------------------------- |
| `cp -i` | Confirmação antes de sobrescrever |
| `mv -i` | Confirmação antes de mover        |
| `rm -i` | Confirmação antes de deletar      |

Mais segurança, menos arrependimento.

## Um Zsh Para Todos os Casos

Removi ajustes específicos para macOS — caminhos, helpers, etc. Não porque eram ruins, mas porque não estavam sendo usados.

Consolidei a configuração shell no próprio `zshrc.symlink`, simplificando checagens de plataforma.

```zsh
export PATH="$HOME/bin:$PATH"
source "$ZSH/aliases.zsh"
source "$ZSH/functions.zsh"
```

Sem mais branches do tipo "se for Darwin, então...". Se quebrar no Linux, eu corrijo. Mas sem otimizar antes da hora.

O novo `zshrc.symlink` contém:

- Variáveis de ambiente
- Aliases
- Funções
- Prompt

Está legível. E o mais importante: é óbvio onde cada coisa vive.

## Podado. Afiado. Pronto.

A atualização de 2017 não foi chamativa. Foi cuidadosa.

Removi o `load.zsh`. Removi helpers antigos. Removi pastas que não usava mais. Removi ferramentas que não me serviam. E cada remoção deixou o setup mais leve — mais meu.

Agora o setup:

- Inicia mais rápido
- Tem menos surpresas escondidas
- Facilita onboarding em novas máquinas
- É mais fácil de depurar

É isso que os dotfiles devem ser. Não pra mostrar pro mundo — mas pra fazer o ambiente desaparecer e você focar no que importa.

→ [Veja o diff completo](https://github.com/helmedeiros/dotfiles/compare/c43d38d05f219c91d026c87638922ffc092d8335...5f3b4f4f5377e2354d0bc2d674d9a414e6bd3c58)
