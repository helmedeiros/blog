---
title: "Meu Kit Git: Os Atalhos e Ajustes Que Me Fizeram Melhor"
date: 2014-12-10T10:00:00-03:00
author: Helio Medeiros
subtitle: Descubra os aliases, scripts e configurações que transformaram meu fluxo Git de lento e doloroso para rápido e fluido—aprenda como pequenas customizações se transformam em grandes ganhos de produtividade
tags: ["git", "aliases", "produtividade", "dotfiles", "experiencia-dev"]
categories: ["Development"]
---

## Ferramentas Refletem Hábitos

Dado todo este tempo que estamos usando git+github aqui na RBS, eu já tinha usado Git o suficiente para perceber uma coisa: meu problema não era só com os comandos em si. Era com a fricção. Com digitar demais, mudar de contexto o tempo todo, e perder foco. Eu não usava Git "errado"—eu usava devagar.

Comecei a buscar formas de reduzir essa fricção. Como qualquer usuário frequente de terminal, fui ajustando meu setup. Criei aliases. Escrevi scripts. Tornei o ambiente mais parecido com a minha cabeça. Foi aí que tudo encaixou. O Git deixou de ser uma ferramenta para virar extensão da minha maneira de pensar.

O que compartilho aqui é meu kit pessoal: aliases, hábitos e configurações que me acompanham até hoje — muitos deles estão nos meus dotfiles: [helmedeiros/dotfiles](https://github.com/helmedeiros/dotfiles).

Não é sobre truques espertos. É sobre poupar segundos que viram horas. E tornar o caminho certo também o mais fácil.

## Aliases Que Uso Todo Dia

O primeiro grande ganho foi reduzir comandos repetitivos. Digitar `git status` cem vezes por dia é castigo. Minha solução?

```bash
alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gco='git checkout'
alias gb='git branch'
alias gd='git diff'
```

Esses comandos viraram memória muscular. Coloquei tudo no meu shell, e logo comecei a encadear os comandos sem pensar.

Meu fluxo básico virou:

```bash
gs
gd
ga -p
gc -m "Corrige erro de digitação na mensagem de validação"
```

| Alias | Comando Completo | Descrição                      |
| ----- | ---------------- | ------------------------------ |
| `gs`  | `git status`     | Mostra o status do repositório |
| `ga`  | `git add`        | Adiciona mudanças para staging |
| `gc`  | `git commit`     | Faz commit das mudanças staged |
| `gco` | `git checkout`   | Muda de branch ou arquivo      |
| `gb`  | `git branch`     | Lista ou manipula branches     |
| `gd`  | `git diff`       | Mostra diferenças nos arquivos |

Pode parecer pouco. Mas isso criou fluidez. Minhas mãos ficaram no teclado. Minha mente ficou no código.

## Tornando o Git Mais Inteligente

Além de economizar teclas, comecei a ensinar o Git a pensar como eu. Criei comandos compostos e scripts para fluxos mais complexos.

Alguns exemplos dos meus dotfiles:

```bash
alias gclean='git branch --merged | grep -v "\*" | xargs -n 1 git branch -d'
alias gundo='git reset --soft HEAD~1'
alias gfixup='git commit --fixup=HEAD && git rebase -i --autosquash HEAD~2'
```

| Alias    | Descrição                                               |
| -------- | ------------------------------------------------------- |
| `gclean` | Remove branches já mescladas                            |
| `gundo`  | Desfaz o último commit com soft reset                   |
| `gfixup` | Cria fixup commit e faz autosquash no rebase interativo |

Esses atalhos me deram segurança para experimentar e velocidade para corrigir.

Também construí fluxos com `git stash`, `git log --oneline` e `git rebase -i`.

Cada alias removia um obstáculo. Não do Git, mas meu. Do atrito de pensar demais para digitar algo longo ou mudar de contexto.

Meu `.gitconfig` e `.zshrc` viraram lugares onde invisto uma vez e ganho tempo todo dia.

## Customizar é Criar Fluidez

Se você digita o mesmo comando Git longo várias vezes por dia—pare. Automatize. Crie um alias. Escreva um script.

Produtividade nem sempre vem de aprender algo novo. Às vezes, vem de adaptar o que você já usa.

Hoje, abrir o terminal é confortável. Meu Git não só suporta meu fluxo—ele acelera. Isso é fruto do kit que fui refinando com o tempo.

Cada um tem seus próprios atritos. Observe os seus. Anote. Resolva um por um, com pequenos atalhos.

E se quiser ver como está meu setup hoje: [helmedeiros/dotfiles](https://github.com/helmedeiros/dotfiles).
