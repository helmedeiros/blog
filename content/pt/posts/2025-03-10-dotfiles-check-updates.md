---
title: "Check-Updates: Mantendo Minha Máquina Honesta"
author: helio
layout: post
date: 2025-03-10T12:00:00+00:00
categories: ["Technology", "Leadership"]
tags:
  - dotfiles
  - maintenance
  - automation
  - homebrew
  - developer-hygiene
  - shell-scripts
  - updates
  - environment-management
---

## Uma Máquina Saudável é uma Máquina Produtiva

Manter um ambiente de desenvolvimento atualizado não é só instalar o patch mais recente do sistema — é evitar fricção.

Fricções como:

- Um CLI desatualizado que falha silenciosamente
- Dependências ausentes que quebram builds
- Patches de segurança que só entram quando é tarde demais

Então construí algo simples e visual nos meus dotfiles: `check-updates`.

Não é automático. Não é mágico. Mas me mantém honesto.

## O que o `check-updates` faz

No essencial, é um script que verifica atualizações de:

- Homebrew (packages e casks)
- Plugins e ferramentas Zsh
- Aplicativos da App Store (via `mas`)

E imprime um **resumo claro e colorido** toda vez que abro o terminal.

```zsh
🔍 Verificando por atualizações...
⬆️  Pacotes Homebrew: 2 desatualizados
⬆️  Casks Homebrew: 1 desatualizado
🧩 Plugins Zsh: atualizados
🛍️  App Store: 1 atualização disponível
✅ Verificação finalizada
```

Essa saída aparece logo abaixo do prompt — um lembrete diário, gentil, de onde estou.

## Onde Ele Vive nos Dotfiles

O script vive dentro da pasta `bin` dos meus dotfiles:

```bash
~/.dotfiles/bin/check-updates
```

E é chamado condicionalmente no `.zshrc.symlink`:

```zsh
# Roda verificação uma vez por dia (com cache)
if [ "$SHOULD_CHECK_UPDATES" = true ]; then
  ~/.dotfiles/bin/check-updates
fi
```

Uso um cache baseado em timestamp para evitar rodar mais de uma vez por dia. Uma checagem diária basta.

## Dentro do Script: Exemplo com Homebrew

Aqui está um trecho do script que verifica os pacotes do Homebrew:

```bash
BREW_OUTDATED=$(brew outdated)
if [ -n "$BREW_OUTDATED" ]; then
  echo "⬆️  Pacotes Homebrew: $(echo "$BREW_OUTDATED" | wc -l) desatualizados"
else
  echo "✅ Pacotes Homebrew: atualizados"
fi
```

Cada seção segue o mesmo padrão: verificar, contar, exibir.
A saída final é limpa — sem logs ou JSON, apenas linhas que me ajudam a agir.

## Por Que Isso Importa (E Por Que é Manual)

Esse script **não** faz atualizações automáticas. Eu não quero surpresas.

Quero **visibilidade**.

Ao ver o que está desatualizado, posso:

- Agendar atualizações no meu tempo
- Depurar problemas com mais confiança
- Saber o que mudou antes que algo quebre

E o script roda rápido. Sem travar. Sem interromper nada.

| Benefício             | Por Que Importa                           |
| --------------------- | ----------------------------------------- |
| Consciência           | Sei o que precisa de atenção              |
| Estabilidade          | Nada atualiza sozinho no meio do trabalho |
| Confiança no ambiente | Sei o estado das ferramentas              |

## Um Script, Menos Desperdício

Esse script não me custa nada — e já me poupou horas.

Toda vez que enfrento um bug causado por dependência desatualizada, lembro por que escrevi isso.

Não é glamouroso. Mas é uma das automações mais úteis que já fiz.

→ [Veja o script no GitHub](https://github.com/helmedeiros/dotfiles/blob/aefe0371e7b4f1e87008d6c593930b0d3c18532c/bin/check-updates)
