---
title: 'Dotfiles: Setup, Backup, and Productivity'
author: helio
layout: post
date: 2013-06-05 10:00:00+00:00
categories:
- Technology
- Agile
tags:
- dotfiles
- zsh
- oh-my-zsh
- shell
- terminal
- productivity
- git
- mackup
- configuration
subtitle: Software development concepts and practices
---

## Getting Serious About My Setup

This week I finally took the time to clean up, version, and share my dotfiles. I've been tweaking my terminal and development environment for a while, but after reinstalling macOS and forgetting half of what I had configured, I knew I couldn't keep relying on muscle memory and scattered gists.

So I built a flat dotfiles setup with the basics: `.aliases`, `.functions`, `.exports`, and a `.zshrc` that sources everything. It's not fancy, but it works. And most importantly, it's versioned.

Dotfiles are those hidden files like `.zshrc`, `.gitconfig`, `.vimrc` that live in your home folder. They're small, powerful, and totally personal. Treating them like code—stored in Git and pushed to GitHub—makes them portable and sustainable.

This post is part documentation, part time capsule. I'll walk through what I've done, the tools I'm using, and how I plan to bootstrap a fresh macOS setup without panic next time.

## One Level, Many Files

Instead of organizing by topic into subfolders like `git/`, `zsh/`, or `system/`, I kept everything flat. Here's what my repo looks like:

```
~/.dotfiles/
├── .aliases
├── .functions
├── .exports
├── .gitconfig
├── .gitignore_global
├── .zshrc
└── install.sh
```

Everything is sourced manually from `.zshrc`:

```zsh
source $DOTFILES/.aliases
source $DOTFILES/.exports
source $DOTFILES/.functions
```

I considered nesting things in folders like other people do, but for now, I prefer the simplicity of a single level. Fewer moving parts.

| File       | Role                                 |
| ---------- | ------------------------------------ |
| .aliases   | Shorthand commands                   |
| .exports   | PATH and environment variables       |
| .functions | Custom shell functions               |
| .zshrc     | Main config, sources everything else |
| install.sh | Setup script to symlink everything   |

Keeping it simple makes it easier to tweak and grow over time.

## My Shell: Zsh with Oh My Zsh

I'm using Zsh as my shell, and it already feels like a big upgrade from bash. Better completions, shared history across tabs, and easier customization.

To manage Zsh config, I installed Oh My Zsh. It takes care of plugin management, themes, and provides sane defaults. In my `.zshrc`, I'm currently using:

```zsh
plugins=(git ruby bundler)
ZSH_THEME="robbyrussell"
```

One thing I like about Oh My Zsh is how easy it is to browse others' setups and borrow ideas. It also works nicely with Mackup (which I'll get to soon).

My `.zshrc` is short and readable:

```zsh
export DOTFILES="$HOME/.dotfiles"
source $DOTFILES/.aliases
source $DOTFILES/.exports
source $DOTFILES/.functions
```

| Plugin  | What It Helps With         |
| ------- | -------------------------- |
| git     | Git shortcuts & completion |
| ruby    | Ruby-related helpers       |
| bundler | Bundler workflow           |

Zsh became something I genuinely enjoy improving.

## Bootstrap with install.sh and Mackup

I added an `install.sh` script to automate setup. It creates symlinks from my dotfiles to the home folder and installs Oh My Zsh if it's missing:

```bash
ln -s $DOTFILES/.aliases ~/.aliases
ln -s $DOTFILES/.zshrc ~/.zshrc
```

It's simple, but it saves time. I still install Homebrew manually, but I'm thinking of adding a `Brewfile` soon.

To sync application preferences like Terminal.app and iTerm2, I'm using Mackup. It stores preferences in Dropbox and symlinks them on new machines:

```bash
mackup backup
mackup restore
```

| Tool       | Purpose                       |
| ---------- | ----------------------------- |
| install.sh | Local symlinks & config setup |
| Mackup     | App preferences backup/sync   |

Together, these steps make a fresh mac setup far less intimidating.

## Sharing and Learning from Others

Publishing my dotfiles on GitHub felt weirdly satisfying: [helmedeiros/dotfiles](https://github.com/helmedeiros/dotfiles). It's not a framework or anything fancy, but it's mine—and that's the point.

I've already started checking out other people's dotfiles for inspiration. Some have clever functions, zsh themes I didn't know about, or better ways to manage plugins. It's a low-key way to keep learning.

Forking dotfiles isn't copying—it's collaborating. And having my own repo means I can try stuff and roll it back without fear.

Things I've learned:

- Use `.local` files for machine-specific secrets
- Ignore Dropbox and system files with `.gitignore`
- Document everything, even aliases

This is the most fun I've had with terminal config since switching to Zsh.

## Looking Ahead

I'm just getting started, but already dotfiles have made my setup more reliable, portable, and fun to work on.

Still on my TODO:

- Add a Brewfile for Homebrew packages
- Auto-install Homebrew from `install.sh`
- Sync Terminal.app preferences with Mackup
- Write a real README

It's not done, but it's mine. And now it's versioned.

[Check it out on GitHub →](https://github.com/helmedeiros/dotfiles)
