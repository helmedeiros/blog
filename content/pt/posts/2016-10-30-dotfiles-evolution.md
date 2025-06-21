---
title: 'Refinando Meus Dotfiles: Mais Limpo, Mais Esperto, Mais Simples'
author: helio
layout: post
date: 2016-10-30 10:00:00+00:00
categories:
- Technology
- Leadership
tags:
- dotfiles
- terminal
- automação
- zsh
- bash
- refatoração
- simplificação
- loader
- functions
subtitle: Conceitos e práticas de desenvolvimento de software
---

## Um Ano Depois, Um Setup Mais Simples

Desde minha última atualização em 2015, vivi bastante com o sistema modular dos dotfiles. Funcionou bem. O onboarding ficou mais rápido, os scripts de instalação ficaram mais inteligentes e eu tinha suporte tanto para Bash quanto para Zsh.

Mas até setups bem organizados começam a se degradar. Muitos aliases, muitos `if` no `.zshrc`, e alguns hacks copiados começaram a aparecer. No final de 2016, senti a necessidade de simplificar.

Não foi uma reconstrução. Foi um refinamento focado. Menos recursos, estrutura mais clara, e um setup que eu realmente conseguiria entender seis meses depois.

Este post documenta como eu apertei os parafusos.

## De Organizado para Carregável

Em 2015 eu tinha uma estrutura por tópicos: `bash/`, `zsh/`, `git/`, e um script de instalação com symlinks. Mas cada arquivo ainda fazia `source` de outros arquivos explicitamente:

```zsh
source "$DOTFILES/zsh/aliases.zsh"
source "$DOTFILES/zsh/functions.zsh"
```

Agora uso um padrão de carregamento automático. Em `zsh/load.zsh`:

```zsh
for config_file ($ZSH/*.zsh); do
  source $config_file
done
```

Essa mudança simplifica tudo. Para adicionar algo novo, basta criar um arquivo `.zsh` na pasta. Não é mais necessário editar vários lugares.

| Antes               | Depois                     |
| ------------------- | -------------------------- |
| `source` manual     | Loader automático com loop |
| Dependências fixas  | Estrutura plugável         |
| Difícil de estender | Fácil de manter e expandir |

É como injeção de dependência — para o shell.

## Funções Mais Pequenas e Focadas

O maior ganho foi cortar o excesso. Reescrevi várias funções shell:

- `extract` para descompactar arquivos
- `take` para criar e entrar em diretórios
- `path-append` para ajustar `$PATH` de forma segura

Cada função vive em seu próprio arquivo em `zsh/functions/`. Assim, posso testá-las, substituí-las ou removê-las isoladamente.

```zsh
# extract.zsh
extract() {
  case $1 in
    *.tar.bz2)   tar xjf $1     ;;
    *.tar.gz)    tar xzf $1     ;;
    *.bz2)       bunzip2 $1     ;;
    *.rar)       unrar x $1     ;;
    *.gz)        gunzip $1      ;;
    *.tar)       tar xf $1      ;;
    *.tbz2)      tar xjf $1     ;;
    *.tgz)       tar xzf $1     ;;
    *.zip)       unzip $1       ;;
    *.Z)         uncompress $1  ;;
    *)           echo "não sei como extrair '$1'..." ;;
  esac
}
```

| Função        | Finalidade                              |
| ------------- | --------------------------------------- |
| `extract`     | Descompactar arquivos                   |
| `take`        | `mkdir && cd` de uma vez                |
| `path-append` | Adicionar caminho ao PATH com segurança |

Separar funções em arquivos isolados foi uma revolução simples e poderosa.

## Um Prompt Que Sai do Caminho

Eu costumava brincar muito com o prompt. Em 2015, tinha um PS1 colorido, com hora, caminho, branch Git e código de saída. Útil — mas poluído.

Hoje uso algo bem mais simples:

```zsh
autoload -Uz vcs_info
precmd() { vcs_info }
PROMPT='%n@%m %1~ ${vcs_info_msg_0_}%# '
```

Esse prompt:

- Usa `vcs_info` para mostrar o estado do Git
- Mostra usuário, host e diretório atual
- Mantém o foco no comando, não na decoração

| Elemento do Prompt | Descrição                       |
| ------------------ | ------------------------------- |
| `%n`               | Nome do usuário                 |
| `%m`               | Nome do host                    |
| `%1~`              | Caminho resumido (última pasta) |
| `vcs_info`         | Estado do repositório Git       |

Menos barulho. Mais sinal.

## Script de Instalação Mais Simples (E Isso É Bom)

O `install.sh` anterior ficou esperto demais. Checava dependências, fazia lógica condicional, mudava conforme o SO. Agora ele é mais burro — e melhor.

```bash
find * -name "*.symlink" | while read file; do
  ln -sf "$file" "$HOME/.$(basename "$file" ".symlink")"
done
```

Move o que é específico de plataforma para outro lugar. O `install.sh` agora só cria os links. Faz uma coisa só — e bem feita.

| Antigo `install.sh` | Novo `install.sh`       |
| ------------------- | ----------------------- |
| Script multifunção  | Apenas cria symlinks    |
| Lógica condicional  | Loop limpo e previsível |
| Dependente de SO    | Portável e direto       |

Agora funciona igual em qualquer máquina. Previsível > inteligente.

## O Que Aprendi

Essa atualização foi menos sobre adicionar — mais sobre remover. Toda melhoria veio da pergunta: _o que eu posso cortar?_

Ao invés de um framework, tenho agora um sistema que:

- Não tem mágica
- É fácil de entender
- Cresce sem fricção
- Parece chato (e isso é ótimo)

Não busco perfeição. Só estabilidade e sanidade.

→ [Veja o diff no GitHub](https://github.com/helmedeiros/dotfiles/compare/88cb13bf0ee8913ce50d5bc0fb475b07486ca3a2...c43d38d05f219c91d026c87638922ffc092d8335)
