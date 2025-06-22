---
title: "Dotfiles 2025: Boot Fast, Adapt Smarter"
author: helio
layout: post
date: 2025-05-27 10:00:00+00:00
categories:

  - Agile
tags:
  - dotfiles
  - portability
  - multi-host
  - adaptation
  - profile-zsh
  - defensive-scripting
  - secrets-management
  - system-integration
subtitle: Learn how to structure dotfiles that work seamlessly across Mac, WSL, containers, and CI—with smart layering and defensive scripting
---

## New Contexts, Same Philosophy

This year I'm not trying to reinvent my shell. I'm preparing it to work _anywhere_.

With multiple machines, containers, and WSL in rotation, I needed a setup that stayed fast, stayed clean, and stayed consistent — regardless of the context.

So I added just enough layering to keep things flexible.

## Introducing `profile.zsh`: A New Top Layer

The biggest structural change this year: `profile.zsh`.

It runs **before** everything else. Its purpose: make system-level decisions. Nothing environment-specific lives in `.zshrc.symlink` anymore — it all starts here.

```zsh
# profile.zsh
export ZSH="$HOME/.zsh"
export DOTFILES="$HOME/.dotfiles"
```

It's the shell equivalent of BIOS config — base assumptions, no noise.

| Layer           | Responsibility                |
| --------------- | ----------------------------- |
| `profile.zsh`   | Paths, host info, assumptions |
| `bootstrap.zsh` | Path exports, base setup      |
| `aliases.zsh`   | Dev shortcuts                 |
| `functions.zsh` | Reusable utilities            |

## Reordering for Clarity and Safety

The `.zshrc.symlink` now reads like a boot plan:

```zsh
source "$DOTFILES/profile.zsh"
source "$DOTFILES/bootstrap.zsh"
source "$DOTFILES/aliases.zsh"
source "$DOTFILES/functions.zsh"
```

This order reflects intent:

1. Define your ground truth
2. Set up the shell
3. Add helpful commands

And because `$DOTFILES` and `$ZSH` are defined early, all paths work predictably.

## Defensive Scripting: Avoiding Setup Drift

One small tweak in `bootstrap.zsh` shows the shift:

```zsh
[ -z "$ZSH" ] && export ZSH="$HOME/.zsh"
```

These guards ensure things don't explode on machines with partial installs, or environments where not everything is mounted yet.

It's a small investment for a big gain: confidence.

## Modular Thinking for Multi-Host Life

This setup is no longer "my laptop's dotfiles."

It's my shell on:

- Mac
- WSL
- Remote dev containers
- CI debugging sessions

And it just works.

Each file serves a role. Each role is testable. Each assumption is written down.

```zsh
# WSL detection (example use case)
if grep -qEi "(Microsoft|WSL)" /proc/version; then
  export WSL=true
fi
```

Dotfiles aren't static anymore — they're adaptive.

## Referencing Secrets from External Repos

This year I also standardized how I source secrets from outside the dotfiles repo:

```zsh
# From personal secrets repo (outside version control here)
[ -f "$HOME/code/private-dotfiles/zsh/secrets.zsh" ] && source "$HOME/code/private-dotfiles/zsh/secrets.zsh"
```

This approach helps me:

- Keep my public config portable and safe
- Share dotfiles without worry
- Maintain multiple scopes of trust (personal, infra, clients)

Dotfiles don't need secrets — they just need to know _where_ to look.

## 2025 Is for Speed, Not Size

This post isn't long because the work wasn't loud.

It was:

- A reordering of responsibility
- A cleanup of mental model
- A preparation for environments I don't fully control

And it means I can spin up a new terminal and trust it'll be fast, sane, and mine.

→ [Compare the diff on GitHub](https://github.com/helmedeiros/dotfiles/compare/97d0e1ba1555acefca52bfdc3a0c9fec2a95282d...aefe0371e7b4f1e87008d6c593930b0d3c18532c)
