---
title: "Dotfiles 2021: Preparing to Scale Myself"
author: helio
layout: post
date: 2021-05-07T10:00:00+00:00
categories: ["Technology"]
tags:
  - dotfiles
  - remote-work
  - bootstrap
  - scaling
  - portability
  - simplification
  - repeatability
  - developer-experience
---

## Two Years Later, Same Tools, New Intent

By 2021, I hadn't added much to my dotfiles in terms of features — but I had changed how I used them.

Two things had shifted: remote work became default, and my personal setup was being copied more often — either by teammates, collaborators, or simply across machines.

So I decided to make one thing clear: this system had to scale _me_. That meant less mess, less magic, and more repeatability.

This update is quiet. But it's purposeful.

## Introducing `bootstrap.zsh`: Start With Clarity

The major addition this cycle is a new file: `bootstrap.zsh`.

Its job? Encapsulate all environment bootstrapping in one place. Not aliases, not functions — just the pieces that set the stage for everything else to work.

```zsh
# bootstrap.zsh
export DOTFILES="$HOME/.dotfiles"
export PATH="$HOME/bin:$PATH"
```

This file made `.zshrc.symlink` cleaner, more focused, and easier to read.

| File             | Responsibility                     |
| ---------------- | ---------------------------------- |
| `.zshrc.symlink` | Just sources the bootstrap         |
| `bootstrap.zsh`  | Sets up environment variables      |
| `aliases.zsh`    | Shortcut logic (still lightweight) |

It made the repo feel intentional again.

## Simplified `.zshrc.symlink`

I rewrote `.zshrc.symlink` to be almost empty:

```zsh
source "$DOTFILES/bootstrap.zsh"
source "$DOTFILES/aliases.zsh"
source "$DOTFILES/functions.zsh"
```

No logic. No conditionals. Just includes.

This decoupling made it trivial to debug or reuse pieces individually.
Want just the `aliases.zsh` on a disposable VM? Easy. Want to test bootstrap on a clean machine? Go ahead.

## Reconfirming Priorities: Simplicity and Portability

With more remote setups and multiple laptops in play, portability mattered.

This update didn't add complexity — it removed assumptions. Gone are any hardcoded user paths, host-specific tweaks, or machine-only logic.

Everything sources from `$DOTFILES`. Everything assumes the simplest path.

```zsh
export PATH="$HOME/bin:$PATH"
```

This line does more than it looks. It says: "I don't need a framework — I just need to not trip over myself."

## A Shell That Boots Faster and Thinks Less

I didn't touch the prompt. Still `vcs_info`, still silent, still mine:

```zsh
autoload -Uz vcs_info
precmd() { vcs_info }
PROMPT='%n@%m %1~ ${vcs_info_msg_0_}%# '
```

What I _did_ do was strip out runtime logic that didn't need to run every boot. Bootstrap is about setup — once it's stable, the terminal just loads fast.

Fewer conditionals. Fewer if/else paths. More confidence that it just works.

## No Reinvention. Just Rebooting With Care.

There's no big bang in this post. No shiny new CLI trick or fuzzy finder. Just a careful rebuild of the foundation.

2021 was about:

- Sharing my setup without friction
- Rebooting cleanly on new environments
- Decoupling logic for better reuse
- Scaling what works — and ditching what doesn't

→ [See the diff on GitHub](https://github.com/helmedeiros/dotfiles/compare/f496fe8a1ab4a7a040e825f3b34c7d2d17dcb324...2f3256ec7595f125e946958c6820305fb939943b)
