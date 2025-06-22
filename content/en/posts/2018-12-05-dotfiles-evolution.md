---
title: "Dotfiles 2018: From Personal to Shared"
author: helio
layout: post
date: 2018-12-05 10:00:00+00:00
categories:
  - Development
tags:
  - dotfiles
  - onboarding
  - teamwork
  - collaboration
  - shared-environment
  - goeuro
  - common-zsh
  - multi-language
subtitle: Evolve your personal development setup into team-friendly shared foundation—balancing individual craft with collaborative onboarding through common configurations and thoughtful documentation
---

## From Autonomy to Alignment

As I've told before, I had just joined GoEuro. That meant not just switching laptops — it meant adapting to how another engineering culture thought about environments, defaults, and onboarding.

I arrived with a minimal, lean dotfiles setup I'd been refining for five years. It worked. But it wasn't made for teams.

Here they have many conventions. Engineers shared common setup expectations: tools, languages, linters, directory structures, prompt behaviors. And for once, instead of resisting alignment, I embraced it.

This update is where my dotfiles evolved from personal craft to shared foundation.

## Introducing `common.zsh`

The biggest change was structural: I added `zsh/common.zsh` — a file meant to centralize all team-shared environment setup.

Before this, I'd kept my config ultra-modular. But that made it hard to onboard someone quickly — or share configs between multiple team members.

With `common.zsh`, I moved everything generic into one place:

```zsh
export EDITOR=vim
export PATH="$HOME/bin:$PATH"
```

Shared scripts like `rbenv` setup or pyenv paths were added here too. Comments made it clear which parts were portable.

| File            | Purpose                        |
| --------------- | ------------------------------ |
| `common.zsh`    | Base setup for any dev machine |
| `aliases.zsh`   | Only local/shortcut logic      |
| `functions.zsh` | Mostly untouched helpers       |

Instead of defending my quirks, I started curating what was helpful for the team.

## Working Across Languages

At GoEuro, I wasn't just using bash or zsh anymore. I needed Ruby, Node, Python — often in parallel.

So I added startup checks for:

```zsh
# Ruby
export PATH="$HOME/.rbenv/bin:$PATH"
eval "$(rbenv init -)"

# Node (nvm or version manager)
# Python (pyenv)
```

These were small, optional, and commented — but they made my machine more adaptable to projects with language-specific needs.

I didn't want dotfiles to _own_ the environment. I wanted them to _enable_ it.

## Still My Prompt, But Faster

The prompt stayed minimal — but I trimmed even more startup noise.

Instead of auto-sourcing themes or full `oh-my-zsh` configs, I simplified:

```zsh
autoload -Uz vcs_info
precmd() { vcs_info }
PROMPT='%n@%m %1~ ${vcs_info_msg_0_}%# '
```

It's lean, shows Git status, and doesn't get in my way.

I also ensured prompt logic loaded **after** shared tooling, so PATH conflicts wouldn't break things. Subtle stuff — but it saved minutes over weeks.

## Better for Others, Not Just for Me

My install script didn't change much — it was already dumb, and that was good. But I started thinking more about people cloning the repo.

So I:

- Added better inline comments
- Grouped logic into recognizable chunks
- Made `common.zsh` a safe default for anyone

These changes weren't just about polish — they were about responsibility. Sharing dotfiles meant someone else might read them, trust them, or depend on them.

And I wanted to make that a little easier.

## 2018 Was the Year of Shared Craft

Joining GoEuro gave me the chance to evolve my environment from a solo ritual into a collaborative tool.

I didn't lose what made the setup mine — I just made space for it to work for others too.

Now, I look at my dotfiles and ask:

- Could a teammate understand this?
- Would a new hire benefit from it?
- Can I install this on a random Mac and feel at home?

If the answer is yes, then I've done enough.

→ [See the full diff on GitHub](https://github.com/helmedeiros/dotfiles/compare/5f3b4f4f5377e2354d0bc2d674d9a414e6bd3c58...8303f8a805e3713e44298b4b976d24cea964f4c8)
