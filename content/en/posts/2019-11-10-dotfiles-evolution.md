---
title: "Dotfiles 2019: Back to Personal"
author: helio
layout: post
date: 2019-11-10T10:00:00+00:00
categories: ["Technology", "Management"]
tags:
  - dotfiles
  - terminal
  - workflow
  - personal
  - simplification
  - back-to-basics
  - individual-craft
  - personal-reset
---

## After the Team Setup, the Personal Reset

In 2018, I had adjusted my dotfiles to work better within a team. I created a `common.zsh`, added friendly comments, and tried to make things more shareable.

But this year, I've missed something: the speed and precision of a terminal setup that was mine alone.

So I made a decision: simplify. Reclaim what I actually used. Strip out anything built for an audience I no longer had to serve.

That's what this update is about.

## Removing `common.zsh`: A Bold Subtraction

The most telling change? I deleted `common.zsh`.

Not because it broke anything — but because it didn't serve my workflow anymore. I wasn't onboarding new teammates. I was solving new problems, in new projects, and needed dotfiles that stayed out of my way.

With `common.zsh` gone, I re-centered configuration inside `.zshrc.symlink`, making each include statement explicit and purposeful:

```zsh
source "$ZSH/exports.zsh"
source "$ZSH/aliases.zsh"
source "$ZSH/functions.zsh"
```

| Before            | After           |
| ----------------- | --------------- |
| Indirect includes | Direct includes |
| Shared-first      | Personal-first  |
| More flexible     | More deliberate |

This reset made everything easier to debug — and easier to own.

## Smarter Defaults, Not More of Them

I didn't add more aliases or utilities. I trimmed them.

But the ones I kept were meaningful:

```zsh
alias gst='git status'
alias gco='git checkout'
alias gcm='git commit -m'
```

These weren't for show. They were tuned to my day-to-day flow.

And I kept core safety features:

```zsh
alias cp='cp -i'
alias mv='mv -i'
alias rm='rm -i'
```

| Alias   | Purpose                    |
| ------- | -------------------------- |
| `gst`   | Fast Git status            |
| `gco`   | Git checkout               |
| `gcm`   | Commit with message        |
| `rm -i` | Prevent accidental deletes |

Less guesswork. More muscle memory.

## Cleaner PATH and Export Handling

One big improvement: I cleaned up PATH management.

```zsh
export PATH="$HOME/bin:$PATH"
```

That's it.

I removed older exports for Ruby, Node, Python, and other tools. Those environments are now managed per-project using tools like `asdf` or `direnv`, where config belongs with the code — not in my shell.

| Before                | After              |
| --------------------- | ------------------ |
| Global language paths | Project-scoped env |
| Do-everything shell   | Just launch-ready  |

It was about trust: trusting each project to configure itself. The shell just needs to stay ready.

## Prompt Still Minimal, Still Mine

No prompt change this time. Still using `vcs_info`, still fast, still quiet:

```zsh
autoload -Uz vcs_info
precmd() { vcs_info }
PROMPT='%n@%m %1~ ${vcs_info_msg_0_}%# '
```

I didn't touch it because it works. A good prompt fades into the background and leaves you focused on what matters.

## A Setup That Feels Like Home Again

This year's dotfiles update wasn't flashy. It was a deep breath. A return to a shell that reflected how I work — not how I wanted others to work with me.

It helped me:

- Start faster every day
- Avoid unnecessary overhead
- Reduce friction when debugging
- Feel at home on any machine

That's the point.

→ [Check the diff on GitHub](https://github.com/helmedeiros/dotfiles/compare/8303f8a805e3713e44298b4b976d24cea964f4c8...f496fe8a1ab4a7a040e825f3b34c7d2d17dcb324)
