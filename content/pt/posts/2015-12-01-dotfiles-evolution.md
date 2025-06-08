---
title: "Evoluindo Meus Dotfiles: Do Simples ao Modular"
author: helio
layout: post
date: 2015-12-01T10:00:00+00:00
categories:
  - Produtividade
  - Ferramentas
  - Ambiente de Desenvolvimento
  - Dotfiles
  - Automação
tags:
  - dotfiles
  - produtividade
  - terminal
  - automação
  - modular
  - zsh
  - bash
  - mackup
  - homebrew
---

## Dois Anos Depois: Por Que Revisei Tudo

Quando publiquei meus dotfiles em 2013, o objetivo era simples: parar de esquecer como configurar meu ambiente. E funcionou. Ter `.aliases`, `.exports`, `.functions` e um `.zshrc` versionados economizou tempo toda vez que reinstalei o sistema.

Mas dois anos depois, depois de trocar de máquina algumas vezes, ajudar colegas a se ambientar e cansar de manter aquele setup flat cheio de gambiarras, percebi que precisava refatorar. Era difícil de reaproveitar, difícil de explicar e mais difícil ainda de compartilhar.

Então decidi adotar uma estrutura modular baseada em tópicos. Inspirado no modelo do Zach Holman, essa reescrita não foi só estética — mudou minha forma de pensar sobre ferramentas, portabilidade e colaboração.

Esse post mostra o que mudou, o que ficou e o que aprendi no processo.

## Simples Demais Dá Trabalho

O setup de 2013 era plano, assim:

```
~/.dotfiles/
├── .aliases
├── .exports
├── .functions
├── .zshrc
└── install.sh
```

Funcionava porque só eu usava. Mas com o tempo, começaram os problemas:

- Muitos assuntos misturados nos mesmos arquivos
- Sem separação clara entre bash e zsh
- Difícil reaproveitar partes no onboarding ou em servidores

Agora o setup está assim:

```
~/.dotfiles/
├── bash/
├── git/
├── macos/
├── zsh/
└── install.sh
```

| Pasta  | Propósito                      |
| ------ | ------------------------------ |
| bash/  | Configurações do shell Bash    |
| zsh/   | Aliases, completions, plugins  |
| git/   | `.gitconfig`, regras de ignore |
| macos/ | Ajustes específicos do macOS   |

Cada uma tem arquivos `*.symlink` e lógica de instalação por sistema. Ficou muito mais fácil compartilhar e escalar.

## Bootstrap Mais Inteligente com install.sh

O novo `install.sh` faz mais do que apenas `ln -s`. Ele detecta dependências, instala só o necessário e separa bem o que é de cada shell.

```bash
find * -name "*.symlink" | while read file; do
  ln -sf "$file" "$HOME/.$(basename "$file" ".symlink")"
done
```

Simples, mas eficiente. Não preciso mais me preocupar com sobrescrever arquivos ou caminhos fixos. Tudo vive em `dotfiles/` e é puxado sob demanda.

| Funcionalidade | Benefício                       |
| -------------- | ------------------------------- |
| `*.symlink`    | Instalação declarativa e segura |
| Layout modular | Reutilizável e didático         |
| Shell-aware    | Suporte para Zsh e Bash         |

Onboarding agora leva minutos, não horas.

## Compatível com Vários Shells e Mais Limpo

Em 2013, tudo era Zsh. Agora também incluo suporte a Bash. Os arquivos `.bash_profile`, `.bashrc` e `.zshrc` coexistem, e a lógica comum (como variáveis de ambiente) vive em arquivos reutilizáveis.

Exemplo:

```bash
# exports.sh
export EDITOR=nvim
export PATH="$HOME/bin:$PATH"
```

Sendo usado assim:

```bash
source "$DOTFILES/exports.sh"
```

Além disso, reorganizei os aliases e funções por intenção:

| Arquivo         | Descrição                              |
| --------------- | -------------------------------------- |
| `aliases.zsh`   | Atalhos como `gst` para `git status`   |
| `functions.zsh` | Lógicas como `extract()` para .zip/tar |
| `path.zsh`      | Organização das entradas do PATH       |

O prompt virou algo opcional e separado — só mexo quando preciso.

## Ferramentas de Apoio: Mackup e Brewfile

Além dos dotfiles, adicionei ferramentas para manter a consistência do sistema. Duas se destacam:

- **Mackup**: faz backup das preferências de apps como Terminal, iTerm2, Sublime, etc. Funciona muito bem após uma instalação limpa.
- **Brewfile**: lista pacotes CLI e apps GUI. Com um comando, instalo tudo via Homebrew:

```bash
brew bundle --file=~/dotfiles/Brewfile
```

Exemplo do meu Brewfile:

```bash
brew 'git'
brew 'nvim'
cask 'iterm2'
```

Não é só conveniência. Isso garante reprodutibilidade.

| Ferramenta | Função                                      |
| ---------- | ------------------------------------------- |
| Mackup     | Backup/restauração de configurações de apps |
| Brewfile   | Instalação de CLI e apps de forma scriptada |

Hoje, levo 30 minutos do zero até um setup funcional.

## O Que Vem Agora

Esse setup está mais perto do que imaginei em 2013. Modular, portável, compartilhável e sem depender da minha memória para funcionar.

Ainda há o que evoluir:

- Suporte para Linux
- Testes e validação no `install.sh`
- Criar script de onboarding para novos devs

Mas estou satisfeito. Não é só sobre meu terminal. É sobre dar vantagem para quem começa comigo e espalhar boas práticas que escalam.

→ [Veja a evolução no GitHub](https://github.com/helmedeiros/dotfiles/compare/5af32427cc0fff55e4d3ee6e43ca0f94fbbd66f7...88cb13bf0ee8913ce50d5bc0fb475b07486ca3a2)
