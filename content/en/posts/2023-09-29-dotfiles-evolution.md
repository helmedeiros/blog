---
title: "Dotfiles 2023: Durable by Design"
author: helio
layout: post
date: 2023-09-29 10:00:00+00:00
categories:
  - Development
tags:
  - dotfiles
  - infrastructure
  - durability
  - portability
  - trust
  - refinement
  - developer-tools
  - shell-configuration
subtitle: Software development concepts and practices
---

## Quiet Refinement, Serious Intent

This year, my dotfiles aren't about exploration anymore. They are infrastructure.

I wasn't adding much. I wasn't removing much. I was refining the system that had to work across any machine, at any time, with zero surprises.

This update may look small — but every change is about trust.

## `$DOTFILES` Becomes the Anchor

The most consistent improvement: I rewired every include path to rely on the `$DOTFILES` variable.

```zsh
source "$DOTFILES/bootstrap.zsh"
source "$DOTFILES/aliases.zsh"
source "$DOTFILES/functions.zsh"
```

No relative paths. No assumptions. Whether cloned, symlinked, or mirrored, this setup now loads the same way everywhere.

| Before                    | After                            |
| ------------------------- | -------------------------------- |
| `source ./aliases.zsh`    | `source "$DOTFILES/aliases.zsh"` |
| Relative and brittle      | Absolute and portable            |
| Depends on current folder | Depends on known root            |

This small shift made every shell session more predictable.

## Order, Not Chaos

Another improvement: sourcing order is now deliberate.

1. Set base paths and environment with `bootstrap.zsh`
2. Load shortcuts from `aliases.zsh`
3. Load helpers from `functions.zsh`

This structure existed before — but now it's explicit and enforced.

```zsh
source "$DOTFILES/bootstrap.zsh"
source "$DOTFILES/aliases.zsh"
source "$DOTFILES/functions.zsh"
```

You read this and know exactly what runs first. That's the goal.

## Sharpening Functions for Reuse

The functions file wasn't bloated. But I took time to clean up naming, scope, and portability.

Every function now:

- Assumes nothing about external state
- Can run on a clean machine
- Behaves the same across OSes

It's not a framework. It's a sharp toolbox.

```zsh
# Example: Git branch cleanup
function delete_merged_branches() {
  git branch --merged | grep -v '\*' | grep -v 'main' | xargs -n 1 git branch -d
}
```

This type of tool belongs in dotfiles — simple, scoped, and repeatable.

## The Philosophy Is the Product

By 2023, I'm not chasing dotfiles features. I'm maintaining a system that lets me:

- Onboard any new machine in minutes
- Share a working shell with colleagues
- Feel zero friction when context-switching

There's nothing shiny here. That's the point.

→ [Compare the diff on GitHub](https://github.com/helmedeiros/dotfiles/compare/2f3256ec7595f125e946958c6820305fb939943b...97d0e1ba1555acefca52bfdc3a0c9fec2a95282d)
