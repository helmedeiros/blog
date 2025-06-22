---
title: "Evolving My Dotfiles: From Flat to Modular"
author: helio
layout: post
date: 2015-12-01 10:00:00+00:00
categories:
  - Technology
  - Agile
tags:
  - dotfiles
  - productivity
  - terminal
  - automation
  - modular
  - zsh
  - bash
  - mackup
  - homebrew
subtitle: Scale from personal craft to team collaboration—building modular, topic-based dotfiles with shell-neutral support, smart bootstrapping, and reproducible environments through Mackup and Brewfile
---

## Two Years Later: Why I Revisited Everything

When I first published my dotfiles back in 2013, I was just trying to stop forgetting my setup. It worked. Having `.aliases`, `.exports`, `.functions`, and a `.zshrc` under version control saved me time every time I reinstalled my system.

But now, two years later, I've gone through more machines, helped onboard more teammates, and gotten tired of maintaining a spaghetti-like single-layer setup. I started hitting limits — hard to reuse, hard to explain, and harder to share. That's when I knew: time to refactor.

So I finally adopted a modular, topic-based structure. Inspired by Zach Holman's approach, this rewrite wasn't just cosmetic — it changed how I think about tooling, portability, and collaboration.

This post explains what changed, what stayed, and what I've learned.

## Flat Was Simple — But Too Simple

The 2013 version was flat, like this:

```
~/.dotfiles/
├── .aliases
├── .exports
├── .functions
├── .zshrc
└── install.sh
```

It worked because I was the only user. But over time, problems showed up:

- Too many unrelated things in the same file
- No clear boundaries between shells (bash vs zsh)
- Couldn't reuse sections in other contexts (onboarding, servers, CI)

Now I've switched to this structure:

```
~/.dotfiles/
├── bash/
├── git/
├── macos/
├── zsh/
└── install.sh
```

| Folder | Purpose                       |
| ------ | ----------------------------- |
| bash/  | Configs for bash shell        |
| zsh/   | Plugins, completions, aliases |
| git/   | `.gitconfig`, ignore rules    |
| macos/ | macOS-specific tweaks         |

Each one has its own `*.symlink` files or logic that installs only what's needed. It's now much easier to onboard a new dev or share parts of the setup.

## Smarter Bootstrap with install.sh

The new `install.sh` script became more than just `ln -s` loops. It now checks for dependencies, links only what's supported on the current system, and cleanly separates shells.

```bash
find * -name "*.symlink" | while read file; do
  ln -sf "$file" "$HOME/.$(basename "$file" ".symlink")"
done
```

It's tiny, but powerful. I no longer worry about overwriting files or hardcoding absolute paths. Everything lives in `dotfiles/` and gets pulled in on demand.

| Feature        | Benefit                            |
| -------------- | ---------------------------------- |
| `*.symlink`    | Declarative, cleaner install logic |
| Topical layout | Easier to understand and reuse     |
| Shell-aware    | Plays nice with both Zsh and Bash  |

This small script reduced onboarding from hours to minutes.

## Shell-Neutral and Cleaner Defaults

In 2013, my setup assumed Zsh. Now, I support Bash too. Files like `.bash_profile` and `.bashrc` now coexist with `.zshrc`, and shared logic (like exports and paths) lives in reusable chunks.

For example:

```bash
# exports.sh
export EDITOR=nvim
export PATH="$HOME/bin:$PATH"
```

This gets sourced by both `zshrc` and `bash_profile` as needed.

```bash
source "$DOTFILES/exports.sh"
```

I also removed noisy aliases and started organizing by intent:

| File            | Description                           |
| --------------- | ------------------------------------- |
| `aliases.zsh`   | Shortcuts like `gst` for `git status` |
| `functions.zsh` | Logic like `extract()` for archives   |
| `path.zsh`      | Order of PATH components              |

I don't tweak my prompt as much anymore — but when I do, it's isolated and optional.

## Supporting Tools: Mackup and Brewfile

Besides the dotfiles themselves, I added tooling to support system-level consistency. Two tools made the biggest impact:

- **Mackup**: backs up app preferences (Terminal, iTerm2, Sublime, etc.) to Dropbox. Works great after a clean install.
- **Brewfile**: defines CLI and GUI apps for macOS. Homebrew installs everything with one command:

```bash
brew bundle --file=~/dotfiles/Brewfile
```

Here's a snippet from my Brewfile:

```bash
brew 'git'
brew 'nvim'
cask 'iterm2'
```

This isn't just about convenience. It makes my local dev environment reproducible.

| Tool     | Role                                |
| -------- | ----------------------------------- |
| Mackup   | Backs up and restores app settings  |
| Brewfile | Scripted install of CLI + GUI tools |

Now I can go from zero to working setup in 30 minutes.

## What's Next

This setup is much closer to what I imagined when I first heard about dotfiles in 2013. It's modular, shareable, portable, and less dependent on me remembering how I wired things together.

There's still room to grow:

- Add setup for Linux systems
- Add tests or validation to the install process
- Publish a sample `onboarding.sh` for teammates

But today, I'm happy with it. It's no longer just about my terminal. It's about giving others a head start and sharing practices that scale beyond my own machine.

→ [Explore the evolution on GitHub](https://github.com/helmedeiros/dotfiles/compare/5af32427cc0fff55e4d3ee6e43ca0f94fbbd66f7...88cb13bf0ee8913ce50d5bc0fb475b07486ca3a2)
