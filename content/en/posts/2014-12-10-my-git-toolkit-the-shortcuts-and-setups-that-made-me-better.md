---
title: "My Git Toolkit: The Shortcuts and Setups That Made Me Better"
date: 2014-12-10T10:00:00-03:00
author: Helio Medeiros
subtitle: Discover the aliases, scripts, and configurations that transformed my Git workflow from slow and painful to fast and fluid—learn how small customizations compound into major productivity gains
tags: ["git", "aliases", "productivity", "dotfiles", "developer-experience"]
categories: ["Development"]
---

## Tools Reflect Habits

Since we migrate this year, here at RBS to git+github, I had spent enough time with Git to realize one thing: my pain wasn't just about Git commands. It was about friction. The typing, the switching, the constant context-shifting. I wasn't using Git wrong—but I was using it _slow_.

I started looking for ways to remove that friction. And like most long-time terminal users, I ended up customizing my setup. I created aliases. I wrote scripts. I made my environment work the way I think. That's when things clicked. Git stopped being something I operated and started becoming something I _drove_.

What follows is my personal Git toolkit: the aliases, habits, and setups that stuck. Some of them still live in my dotfiles today — [helmedeiros/dotfiles](https://github.com/helmedeiros/dotfiles).

This isn't about clever hacks. It's about saving seconds that add up to hours, and making the easy path also the right one.

## Aliases I Use Every Day

The first major win was shortening the commands I used 50 times a day. Typing `git status` repeatedly is a form of slow torture. My solution?

```bash
alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gco='git checkout'
alias gb='git branch'
alias gd='git diff'
```

These basics became muscle memory. They lived in my shell configuration, and I started to chain them together without thinking.

Here's a simple example of my workflow:

```bash
gs
gd
ga -p
gc -m "Fix typo in validation message"
```

| Alias | Full Command   | Description                      |
| ----- | -------------- | -------------------------------- |
| `gs`  | `git status`   | Show working tree status         |
| `ga`  | `git add`      | Stage changes                    |
| `gc`  | `git commit`   | Commit staged changes            |
| `gco` | `git checkout` | Switch branches or files         |
| `gb`  | `git branch`   | List, create, or delete branches |
| `gd`  | `git diff`     | Show file differences            |

These may seem small. But they created flow. I no longer had to pause to type. My fingers stayed on the keyboard, and my mind stayed on the task.

## Making My Git Smarter

Beyond just saving keystrokes, I started teaching Git to work the way I thought. That meant creating compound commands and scripts for more complex workflows.

Some examples I added to my dotfiles:

```bash
alias gclean='git branch --merged | grep -v "\*" | xargs -n 1 git branch -d'
alias gundo='git reset --soft HEAD~1'
alias gfixup='git commit --fixup=HEAD && git rebase -i --autosquash HEAD~2'
```

| Alias    | Description                                                 |
| -------- | ----------------------------------------------------------- |
| `gclean` | Clean up merged branches                                    |
| `gundo`  | Undo the last commit (soft reset)                           |
| `gfixup` | Create a fixup commit and auto-squash into the previous one |

These helped me experiment safely and recover quickly. I also built workflows around `git stash`, `git log --oneline`, and `git rebase -i`.

Each alias removed a blocker. Not from Git—but from _me_. From the friction of switching mental contexts or making typos in long commands.

My `.gitconfig` and `.zshrc` became places I invested time once to save time daily.

## Customizing for Flow

If you find yourself typing the same long Git command multiple times per day—stop. Automate it. Alias it. Script it.

Productivity doesn't always come from learning new tools. Sometimes it comes from shaping old ones to fit you better.

Today, when I open a terminal, it feels like home. My Git setup doesn't just support my workflow—it accelerates it. And most of that is thanks to the toolkit I've built and refined over time.

Your mileage may vary. But the principle is universal: the more seamless your tools, the more space you have to think, create, and ship.

Explore your own Git pain points. Write them down. Then solve them one alias at a time.

And if you want to see my live setup, here it is: [helmedeiros/dotfiles](https://github.com/helmedeiros/dotfiles).
