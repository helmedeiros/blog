---
title: "Check-Updates: Keeping My Machine Honest"
author: helio
layout: post
date: 2025-03-10 12:00:00+00:00
categories:
  - Development
tags:
  - dotfiles
  - maintenance
  - automation
  - homebrew
  - developer-hygiene
  - shell-scripts
  - updates
  - environment-management
subtitle: Build a simple script that gives you daily visibility into what needs updating—without the surprises of auto-updates
---

## A Healthy Machine is a Productive One

Keeping a dev machine updated isn't just about installing the latest OS patch — it's about avoiding friction.

Friction like:

- An outdated CLI that fails silently
- Missing system dependencies that crash builds
- Security patches that only apply once it's too late

So I built something simple and visual into my dotfiles: `check-updates`.

It's not flashy. It's not automatic. But it keeps me honest.

## What `check-updates` Does

At its core, it's a script that checks for updates across:

- Homebrew (packages and casks)
- Zsh plugins and tools
- Mac App Store apps (via `mas`)

And it prints out a **clear, colorful summary** every time I open a terminal.

```zsh
🔍 Checking for updates...
⬆️  Homebrew packages: 2 outdated
⬆️  Homebrew casks: 1 outdated
🧩 Zsh plugins: up-to-date
🛍️  App Store: 1 update available
✅ All checks completed
```

This output sits just below the prompt — a gentle, daily nudge that tells me where I stand.

## Where It Lives in the Dotfiles

The script lives inside the `bin` folder of my dotfiles:

```bash
~/.dotfiles/bin/check-updates
```

And it's sourced conditionally from `.zshrc.symlink`:

```zsh
# Run updates check once per day (cached)
if [ "$SHOULD_CHECK_UPDATES" = true ]; then
  ~/.dotfiles/bin/check-updates
fi
```

I use a timestamp-based cache to avoid re-checking multiple times a day. One hit per day is enough.

## Inside the Script: Homebrew Example

Here's one chunk from the script that checks Homebrew packages:

```bash
BREW_OUTDATED=$(brew outdated)
if [ -n "$BREW_OUTDATED" ]; then
  echo "⬆️  Homebrew packages: $(echo "$BREW_OUTDATED" | wc -l) outdated"
else
  echo "✅ Homebrew packages: up-to-date"
fi
```

Each section follows this format: check, count, display.
The final output is clean — not logs, not JSON, just one-liners that help me take action if needed.

## Why It Matters (And Why It's Manual)

This isn't an auto-updater. I don't want surprises.

I want visibility.

By seeing what's out of date, I can:

- Schedule upgrades on my terms
- Troubleshoot issues with more confidence
- Know what's changed before something breaks

And the script runs fast. No delay. No interruptions.

| Benefit              | Why It Matters                |
| -------------------- | ----------------------------- |
| Awareness            | I know what needs attention   |
| Stability            | No forced updates mid-session |
| Trust in environment | I know the state of my tools  |

## One Script, Less Waste

This script costs me nothing and saves me hours.

Every time I run into a bug caused by a dependency mismatch, I remember why I built this.

It's not glamorous. But it's one of the most practical pieces of automation I've ever written.

→ [See the script on GitHub](https://github.com/helmedeiros/dotfiles/blob/aefe0371e7b4f1e87008d6c593930b0d3c18532c/bin/check-updates){target="\_blank"}
