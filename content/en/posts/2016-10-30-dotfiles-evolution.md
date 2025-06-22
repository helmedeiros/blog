---
title: "Dotfiles Refinement: Cleaner, Smarter, Faster"
author: helio
layout: post
date: 2016-10-30 10:00:00+00:00
categories:
  - Development
tags:
  - dotfiles
  - terminal
  - automation
  - zsh
  - bash
  - refactoring
  - simplification
  - loader
  - functions
subtitle: Transform your shell into a pluggable architecture—introducing loader patterns, focused functions, and a minimal prompt that gets out of your way while boosting productivity
---

## A Year Later, A Simpler Setup

Since my last update in 2015, I've had time to live with the modular dotfiles system. It worked. Onboarding was faster, the install scripts were smarter, and I had shell support for both Bash and Zsh.

But even well-organized setups can start to rot. Too many aliases, too many `.zshrc` conditionals, and a few copy-pasted hacks started to creep in. By late 2016, I felt the need to simplify.

So this wasn't a rebuild. It was a focused refinement. Fewer features, clearer structure, and a setup I could actually understand six months later.

This post documents how I tightened the screws.

## From Organized to Loadable

My 2015 setup was topic-based, with folders like `bash/`, `zsh/`, `git/`, and an install script to symlink everything. But each shell file still sourced other files explicitly:

```zsh
source "$DOTFILES/zsh/aliases.zsh"
source "$DOTFILES/zsh/functions.zsh"
```

Now, I've introduced a loader pattern. In `zsh/load.zsh`:

```zsh
for config_file ($ZSH/*.zsh); do
  source $config_file
done
```

This small shift makes everything cleaner. Adding new functionality is just dropping a `.zsh` file in the folder. No need to edit multiple files to register it.

| Before                  | After                         |
| ----------------------- | ----------------------------- |
| Manual `source` entries | Automatic loader via loop     |
| Hardcoded dependencies  | Drop-in config structure      |
| More friction to extend | Easily pluggable architecture |

It feels like dependency injection, but for your shell.

## Smaller, More Focused Functions

The biggest win from this cycle was cutting. I rewrote most of my shell functions:

- `extract` for decompressing archives
- `take` for creating and entering directories
- `path-append` for safely editing `$PATH`

Each function lives in its own file under `zsh/functions/`. This means I can test, replace, or remove one without affecting the rest.

```zsh
# extract.zsh
extract() {
  case $1 in
    *.tar.bz2)   tar xjf $1     ;;
    *.tar.gz)    tar xzf $1     ;;
    *.bz2)       bunzip2 $1     ;;
    *.rar)       unrar x $1     ;;
    *.gz)        gunzip $1      ;;
    *.tar)       tar xf $1      ;;
    *.tbz2)      tar xjf $1     ;;
    *.tgz)       tar xzf $1     ;;
    *.zip)       unzip $1       ;;
    *.Z)         uncompress $1  ;;
    *)           echo "don't know how to extract '$1'..." ;;
  esac
}
```

| Function      | Purpose                            |
| ------------- | ---------------------------------- |
| `extract`     | Decompress any common archive type |
| `take`        | `mkdir && cd` in one               |
| `path-append` | Safely extend PATH                 |

Writing functions as standalone files was the change I didn't know I needed.

## A Prompt That Gets Out of the Way

I used to tinker with the prompt a lot. In 2015, I had a verbose, colored PS1 setup showing time, path, Git branch, and exit code. It was useful — but noisy.

Now I use a much simpler prompt. Just the essentials:

```zsh
autoload -Uz vcs_info
precmd() { vcs_info }
PROMPT='%n@%m %1~ ${vcs_info_msg_0_}%# '
```

This prompt:

- Uses `vcs_info` to show Git state when needed
- Shows user, host, and current directory
- Keeps the screen focused on the command, not decorations

| Prompt Element | Description                    |
| -------------- | ------------------------------ |
| `%n`           | Username                       |
| `%m`           | Hostname                       |
| `%1~`          | Truncated path (last dir only) |
| `vcs_info`     | Git branch/status              |

More signal, less noise.

## Install Script Now Even Dumber (in a Good Way)

The original `install.sh` grew too smart. It had conditionals, dependency checks, platform switches. Now it's dumber — but better.

```bash
find * -name "*.symlink" | while read file; do
  ln -sf "$file" "$HOME/.$(basename "$file" ".symlink")"
done
```

I moved platform-specific setups elsewhere. This lets `install.sh` do just one job: create symlinks. It's composable now.

| Old `install.sh`     | New `install.sh`   |
| -------------------- | ------------------ |
| Multi-purpose script | Just symlinks      |
| Conditional logic    | Clean loop         |
| OS-dependent         | Portable + minimal |

This script now runs the same on every machine. Predictability > cleverness.

## What I've Learned

This update wasn't about adding — it was about subtracting. Every improvement came from asking: _what can I remove?_

Instead of building a framework, I've built a system that:

- Has no magic
- Is easy to onboard into
- Can grow without friction
- Looks boring (and that's a feature)

I'm not chasing perfection. Just stability and sanity.

→ [Check out the diff on GitHub](https://github.com/helmedeiros/dotfiles/compare/88cb13bf0ee8913ce50d5bc0fb475b07486ca3a2...c43d38d05f219c91d026c87638922ffc092d8335)
