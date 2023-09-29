---
title: "Dotfiles 2023: Durabilidade por Design"
author: helio
layout: post
date: 2023-09-29T10:00:00+00:00
categories:
  - Dotfiles
  - Configuração de Desenvolvedor
  - Shell
  - Portabilidade
  - Prática
tags:
  - dotfiles
  - infrastructure
  - durability
  - portability
  - trust
  - refinement
  - developer-tools
  - shell-configuration
---

## Refinamento Silencioso, Intenção Séria

Este ano, meus dotfiles não são mais sobre experimentação. São infraestrutura.

Eu não estou adicionando muito. Nem removendo muito. Estava refinando um sistema que precisava funcionar em qualquer máquina, a qualquer momento, sem surpresas.

Essa atualização parece pequena — mas cada mudança é sobre confiança.

## `$DOTFILES` se Torna a Âncora

A melhoria mais consistente: reescrevi todos os paths para usar a variável `$DOTFILES`.

```zsh
source "$DOTFILES/bootstrap.zsh"
source "$DOTFILES/aliases.zsh"
source "$DOTFILES/functions.zsh"
```

Nada de caminhos relativos. Nenhuma suposição. Clonado, linkado ou espelhado — o setup agora carrega sempre da mesma forma.

| Antes                  | Depois                           |
| ---------------------- | -------------------------------- |
| `source ./aliases.zsh` | `source "$DOTFILES/aliases.zsh"` |
| Relativo e frágil      | Absoluto e portátil              |
| Depende da pasta atual | Depende de raiz conhecida        |

Essa pequena mudança tornou cada sessão de terminal mais previsível.

## Ordem, Não Caos

Outra melhoria: a ordem de sourcing agora é deliberada.

1. Define paths base e ambiente com `bootstrap.zsh`
2. Carrega atalhos com `aliases.zsh`
3. Carrega utilitários com `functions.zsh`

Essa estrutura já existia — agora está explícita e respeitada.

```zsh
source "$DOTFILES/bootstrap.zsh"
source "$DOTFILES/aliases.zsh"
source "$DOTFILES/functions.zsh"
```

Você lê isso e sabe exatamente o que roda primeiro. Esse é o objetivo.

## Funções Mais Afiadas para Reuso

O arquivo de funções não estava inflado. Mas dediquei tempo para limpar nomes, escopo e portabilidade.

Agora, cada função:

- Não depende de estado externo
- Funciona em uma máquina limpa
- Se comporta igual em qualquer sistema

Não é um framework. É uma caixa de ferramentas precisa.

```zsh
# Exemplo: limpar branches já mesclados
function delete_merged_branches() {
  git branch --merged | grep -v '\*' | grep -v 'main' | xargs -n 1 git branch -d
}
```

Esse tipo de utilitário pertence aos dotfiles — simples, focado e reaproveitável.

## A Filosofia É o Produto

Em 2023, não estou mais atrás de novidades nos dotfiles. Estou mantendo um sistema que me permite:

- Subir qualquer máquina nova em minutos
- Compartilhar meu shell com colegas
- Trocar de contexto sem fricção

Não tem nada chamativo aqui. E é exatamente esse o ponto.

→ [Compare o diff no GitHub](https://github.com/helmedeiros/dotfiles/compare/2f3256ec7595f125e946958c6820305fb939943b...97d0e1ba1555acefca52bfdc3a0c9fec2a95282d)
