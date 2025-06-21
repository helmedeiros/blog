---
title: 'Dotfiles 2017: Cutting Even Deeper'
author: helio
layout: post
date: 2017-10-09 10:00:00+00:00
categories:
- Technology
tags:
- dotfiles
- shell
- zsh
- minimalism
- refactoring
- aliases
- simplification
- pruning
subtitle: Software development concepts and practices
---

## One Year Later: Time to Prune

My dotfiles is stable. They are modular, sourced dynamically, backed by a dumb install script that just works. But I start to feel a new kind of friction: knowing that some things were still there... just because they always had been.

So this update was about honesty. I walked through every file and asked myself: do I still use this? Would I miss it if it were gone?

Spoiler: most of the time, the answer was "no."

## No More Magic: Goodbye load.zsh

One of the first things to go was `load.zsh`. It used to scan and load every `.zsh` file in a folder. That worked — until it didn't.

Over time, I'd accumulated stray `.zsh` scripts that got sourced without much intention. They weren't wrong. But they weren't needed either.

So I got rid of the magic loader. Now, each file is explicitly sourced via `.zshrc.symlink`. It's clear, deliberate, and easier to trace.

```zsh
source "$ZSH/aliases.zsh"
source "$ZSH/functions.zsh"
source "$ZSH/prompt.zsh"
```

| Old Pattern     | New Pattern     |
| --------------- | --------------- |
| `load.zsh` loop | Direct `source` |
| Auto-includes   | Explicit config |
| Easy to forget  | Hard to ignore  |

This refactor made it obvious which files mattered — and which didn't.

## Safer Aliases by Default

This version also introduced safer CLI behavior. Simple things that protect me from myself.

```bash
alias cp='cp -i'
alias mv='mv -i'
alias rm='rm -i'
```

It's annoying the first time. But after a few months, you realize: maybe overwriting or deleting files silently was never a good idea.

Combined with `alias ls='ls -GFh'`, I now have:

- readable directory listings
- protected file operations
- consistent behavior across machines

| Alias   | Purpose                 |
| ------- | ----------------------- |
| `cp -i` | Prompt before overwrite |
| `mv -i` | Prompt before move      |
| `rm -i` | Prompt before delete    |

Safer by default. Less regret.

## One Zsh to Rule Them All

I removed macOS-specific tweaks, paths, and helpers.
Not because they were bad — but because they weren't being used.

I also consolidated shell config back into `zshrc.symlink`, simplifying platform checks and customizations.

```zsh
export PATH="$HOME/bin:$PATH"
source "$ZSH/aliases.zsh"
source "$ZSH/functions.zsh"
```

There's no platform branching. No "if Darwin then..." conditions. If something breaks on Linux, I'll fix it — but I'm not optimizing prematurely.

This cleaned-up `.zshrc.symlink` is now just:

- Exports
- Aliases
- Functions
- Prompt

It's readable. And more importantly, it's obvious where things live.

## Pruned. Sharpened. Ready.

2017's update wasn't flashy. It was careful.

I removed `load.zsh`. I removed old helpers. I removed folder structures I didn't use. I removed tools I didn't need. And every removal made the setup feel lighter — more mine.

This setup now:

- Starts faster
- Has fewer hidden surprises
- Onboards new machines quicker
- Is easier to debug

That's what dotfiles are about. Not showing off — but making your environment disappear so you can focus on the work.

→ [Check out the full diff](https://github.com/helmedeiros/dotfiles/compare/c43d38d05f219c91d026c87638922ffc092d8335...5f3b4f4f5377e2354d0bc2d674d9a414e6bd3c58)
