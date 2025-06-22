---
title: "Dotfiles: Setup, Backup e Produtividade"
author: helio
layout: post
date: 2013-06-05 10:00:00+00:00
categories:
  - Development
tags:
  - dotfiles
  - zsh
  - oh-my-zsh
  - shell
  - terminal
  - produtividade
  - git
  - mackup
  - configuração
subtitle: Construa seu primeiro repositório de dotfiles do zero—configurando controle de versão, criando configurações modulares e estabelecendo workflows de instalação que tornam o setup de ambiente repetível e compartilhável
---

## Levando a Sério Meu Setup

Essa semana eu finalmente tirei um tempo para organizar, versionar e compartilhar meus dotfiles. Já venho ajustando meu terminal e ambiente há um tempo, mas depois de reinstalar o macOS e esquecer metade do que eu usava, percebi que não dava pra continuar confiando só na memória e em gists espalhados.

Então criei um setup plano com o básico: `.aliases`, `.functions`, `.exports` e um `.zshrc` que carrega tudo. Não é nada rebuscado, mas funciona. E o mais importante: está versionado.

Dotfiles são arquivos escondidos como `.zshrc`, `.gitconfig`, `.vimrc` que vivem na sua home. Pequenos, poderosos, e totalmente pessoais. Tratar eles como código — guardados no Git e no GitHub — deixa tudo mais portável e confiável.

Esse post é um pouco documentação, um pouco cápsula do tempo. Vou mostrar o que já montei, quais ferramentas estou usando e como planejo configurar um novo macOS sem estresse da próxima vez.

## Tudo na Raiz, Vários Arquivos

Em vez de organizar por tópicos com subpastas como `git/`, `zsh/` ou `system/`, deixei tudo no mesmo nível. Meu repositório ficou assim:

```
~/.dotfiles/
├── .aliases
├── .functions
├── .exports
├── .gitconfig
├── .gitignore_global
├── .zshrc
└── install.sh
```

Tudo é carregado manualmente no `.zshrc`:

```zsh
source $DOTFILES/.aliases
source $DOTFILES/.exports
source $DOTFILES/.functions
```

Pensei em criar subpastas como vi em outros repositórios, mas por enquanto prefiro a simplicidade de deixar tudo plano. Menos arquivos e menos navegação.

| Arquivo    | Função                                    |
| ---------- | ----------------------------------------- |
| .aliases   | Atalhos de comando                        |
| .exports   | Variáveis de ambiente (como PATH)         |
| .functions | Funções personalizadas                    |
| .zshrc     | Configuração principal, carrega os outros |
| install.sh | Script para criar symlinks                |

Essa estrutura simples me ajuda a manter e evoluir com tranquilidade.

## Meu Shell: Zsh com Oh My Zsh

Uso o Zsh como shell e já sinto que foi uma evolução em relação ao bash. Melhor autocomplete, histórico entre abas, e bem mais flexível pra personalizar.

Pra gerenciar a configuração do Zsh, instalei o Oh My Zsh. Ele cuida do carregamento de plugins, temas e já traz boas práticas. No `.zshrc`, estou usando:

```zsh
plugins=(git ruby bundler)
ZSH_THEME="robbyrussell"
```

O que mais curto no Oh My Zsh é como ele facilita aprender com os outros. Dá pra ver setups no GitHub, copiar plugins e entender novas ideias. E ele funciona bem junto com o Mackup (vou falar dele logo abaixo).

Meu `.zshrc` ficou enxuto e claro:

```zsh
export DOTFILES="$HOME/.dotfiles"
source $DOTFILES/.aliases
source $DOTFILES/.exports
source $DOTFILES/.functions
```

| Plugin  | Função                              |
| ------- | ----------------------------------- |
| git     | Aliases e autocompletar do Git      |
| ruby    | Atalhos pra desenvolvimento em Ruby |
| bundler | Fluxo de trabalho com Bundler       |

O Zsh virou uma ferramenta que eu realmente gosto de ajustar e melhorar.

## Automação com install.sh e Mackup

Adicionei um script `install.sh` pra automatizar a configuração inicial. Ele cria symlinks dos arquivos da pasta `.dotfiles` para a home e instala o Oh My Zsh se precisar:

```bash
ln -s $DOTFILES/.aliases ~/.aliases
ln -s $DOTFILES/.zshrc ~/.zshrc
```

Simples, mas já economiza bastante tempo. Ainda instalo o Homebrew manualmente, mas estou pensando em adicionar um `Brewfile`.

Pra sincronizar preferências de apps como Terminal.app e iTerm2, estou usando o Mackup. Ele salva as configurações no Dropbox e cria symlinks na máquina nova:

```bash
mackup backup
mackup restore
```

| Ferramenta | Papel                                   |
| ---------- | --------------------------------------- |
| install.sh | Criação dos symlinks e setup do Zsh     |
| Mackup     | Backup e sincronização das preferências |

Com esses dois passos, instalar um novo macOS virou algo bem mais tranquilo.

## Compartilhando e Aprendendo

Publicar meus dotfiles no GitHub deu uma sensação boa: [helmedeiros/dotfiles](https://github.com/helmedeiros/dotfiles). Não é framework nem template — é o meu ambiente. E é isso que importa.

Já comecei a olhar os dotfiles de outras pessoas pra pegar ideias. Descobri funções legais, temas de Zsh diferentes, formas melhores de configurar plugins. Tudo isso me ajuda a melhorar meu próprio setup.

Forkar dotfiles não é copiar — é colaborar. Ter meu próprio repositório me permite testar coisas novas sem medo de quebrar tudo.

Alguns aprendizados:

- Use arquivos `.local` para segredos específicos da máquina
- Adicione `.gitignore` pra evitar sync de lixo de sistema
- Documente tudo, até os aliases

Foi a parte mais divertida de configurar meu terminal nos últimos tempos.

## Próximos Passos

Estou só começando, mas os dotfiles já deixaram meu setup mais confiável, portável e divertido de trabalhar.

Ainda quero:

- Adicionar um `Brewfile` com os pacotes do Homebrew
- Automatizar a instalação do Homebrew no `install.sh`
- Sincronizar preferências do Terminal.app com o Mackup
- Escrever um README decente

Não está finalizado, mas é meu. E agora está no Git.

[Veja no GitHub →](https://github.com/helmedeiros/dotfiles)
