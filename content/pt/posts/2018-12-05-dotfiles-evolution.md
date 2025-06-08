---
title: "Dotfiles 2018: Do Pessoal ao Compartilhado"
author: helio
layout: post
date: 2018-12-05T10:00:00+00:00
categories:
  - Dotfiles
  - Onboarding
  - Ferramentas de Desenvolvedor
  - Ambiente de Desenvolvimento
  - Setup de Ambiente
tags:
  - dotfiles
  - onboarding
  - teamwork
  - collaboration
  - shared-environment
  - goeuro
  - common-zsh
  - multi-language
---

## Da Autonomia ao Alinhamento

Como já contei antes, tinha acabado de entrar na GoEuro. Isso significava não só trocar de laptop — mas adaptar-se à forma como outra cultura de engenharia pensava sobre ambientes, padrões e onboarding.

Cheguei com um setup de dotfiles minimalista e enxuto que vinha refinando há cinco anos. Funcionava. Mas não foi feito para times.

Lá eles tinham muitas convenções. Os engenheiros compartilhavam expectativas comuns de configuração: ferramentas, linguagens, linters, estruturas de diretório, comportamentos de prompt. E pela primeira vez, ao invés de resistir ao alinhamento, eu o abracei.

Essa atualização é onde meus dotfiles evoluíram de ofício pessoal para base compartilhada.

## Introduzindo `common.zsh`

A maior mudança foi estrutural: adicionei `zsh/common.zsh` — um arquivo pensado para centralizar toda configuração de ambiente compartilhada pelo time.

Antes disso, mantinha minha configuração ultra-modular. Mas isso dificultava fazer onboarding de alguém rapidamente — ou compartilhar configs entre vários membros do time.

Com `common.zsh`, movi tudo que era genérico para um só lugar:

```zsh
export EDITOR=vim
export PATH="$HOME/bin:$PATH"
```

Scripts compartilhados como setup do `rbenv` ou caminhos do pyenv foram adicionados aqui também. Comentários deixavam claro quais partes eram portáveis.

| Arquivo         | Propósito                            |
| --------------- | ------------------------------------ |
| `common.zsh`    | Setup base para qualquer máquina dev |
| `aliases.zsh`   | Apenas lógica local/atalhos          |
| `functions.zsh` | Helpers praticamente inalterados     |

Ao invés de defender minhas manias, comecei a curar o que era útil para o time.

## Trabalhando com Várias Linguagens

Na GoEuro, não usava mais apenas bash ou zsh. Precisava de Ruby, Node, Python — frequentemente em paralelo.

Então adicionei verificações de inicialização para:

```zsh
# Ruby
export PATH="$HOME/.rbenv/bin:$PATH"
eval "$(rbenv init -)"

# Node (nvm ou gerenciador de versão)
# Python (pyenv)
```

Eram pequenas, opcionais e comentadas — mas tornavam minha máquina mais adaptável a projetos com necessidades específicas de linguagem.

Não queria que os dotfiles _dominassem_ o ambiente. Queria que eles o _habilitassem_.

## Ainda Meu Prompt, Mas Mais Rápido

O prompt continuou minimal — mas cortei ainda mais ruído de inicialização.

Ao invés de carregar temas automaticamente ou configs completos do `oh-my-zsh`, simplifiquei:

```zsh
autoload -Uz vcs_info
precmd() { vcs_info }
PROMPT='%n@%m %1~ ${vcs_info_msg_0_}%# '
```

É enxuto, mostra status do Git, e não atrapalha.

Também garanti que a lógica do prompt carregasse **depois** das ferramentas compartilhadas, para que conflitos de PATH não quebrassem nada. Sutilezas — mas que pouparam minutos ao longo das semanas.

## Melhor para Outros, Não Só para Mim

Meu script de instalação não mudou muito — já era simples, e isso era bom. Mas comecei a pensar mais nas pessoas clonando o repo.

Então eu:

- Adicionei comentários inline melhores
- Agrupei lógica em blocos reconhecíveis
- Fiz do `common.zsh` um padrão seguro para qualquer um

Essas mudanças não eram só sobre polimento — eram sobre responsabilidade. Compartilhar dotfiles significava que alguém mais poderia lê-los, confiar neles ou depender deles.

E eu queria tornar isso um pouco mais fácil.

## 2018 Foi o Ano do Ofício Compartilhado

Entrar na GoEuro me deu a chance de evoluir meu ambiente de um ritual solo para uma ferramenta colaborativa.

Não perdi o que tornava o setup meu — apenas abri espaço para que funcionasse para outros também.

Agora, olho para meus dotfiles e pergunto:

- Um colega de time conseguiria entender isso?
- Um novo contratado se beneficiaria disso?
- Consigo instalar isso num Mac aleatório e me sentir em casa?

Se a resposta for sim, então fiz o suficiente.

→ [Veja o diff completo no GitHub](https://github.com/helmedeiros/dotfiles/compare/5f3b4f4f5377e2354d0bc2d674d9a414e6bd3c58...8303f8a805e3713e44298b4b976d24cea964f4c8)
