---
title: "Still Learning, Still Winning: Why Git Keeps Surprising Me"
date: 2015-06-13T10:00:00-03:00
author: Helio Medeiros
subtitle: Discover how joining ThoughtWorks transformed my Git understanding from individual mastery to collective craft—where advanced techniques become shared rituals and continuous learning drives excellence
tags: ["git", "version-control", "software-craft", "learning", "thoughtworks"]
categories: ["Development"]
---

## A New Chapter, A New Standard

By August 2014, I had joined ThoughtWorks. And even though I had already been using Git for years—writing posts, leading teams, automating everything—I felt like I was starting over.

Why? Because I was suddenly surrounded by some of the most brilliant technicians I had ever worked with. Most were younger than me. Many were just a few years into their careers. But they had been learning the right way from day one. Pair programming, TDD, short-lived branches, rebasing before merge, semantic commits—it wasn't theory. It was their normal.

And that changed everything for me. Git became not just a tool—but a shared language. A ritual. A signal of discipline and pride in craft.

## Mastery Through Collective Learning

The biggest surprise wasn't a Git command. It was how much more Git could be when shared in a team of strong practitioners.

```bash
git rebase -i HEAD~3
```

Before, this was something I used when I messed up. At ThoughtWorks, it was how people shaped their commits before ever pushing code. They didn't just write "good enough" commit messages—they crafted storylines. Reviewing history felt like reading a well-edited journal, not a noisy backlog.

I learned new aliases. I saw interactive rebases used like editing film. I picked up tricks like:

```bash
git commit --fixup <sha>
git rebase -i --autosquash
```

| Command                       | Purpose                              |
| ----------------------------- | ------------------------------------ |
| `rebase -i`                   | Reorder, squash, or edit commits     |
| `--fixup` + `--autosquash`    | Clean up commits before review/merge |
| `log --graph --oneline --all` | Visualize branch structure           |

And the most important lesson? Don't wait to clean up history. Write clean code _and_ clean history from the start.

## Git as a Reflection of Thoughtfulness

At ThoughtWorks, Git wasn't a step—it was a craft. People didn't just know commands. They **understood** why we rebase, why we squash, why merge commits were avoided unless truly necessary.

Even conflict resolution looked different. Instead of blame, we debugged with curiosity. Instead of rushing a push, we took time to refine the story we were telling in the repo.

We had hooks. We had CI. But more than anything, we had **care**.

```bash
git show <sha>
```

Didn't just show a diff. It showed intent. What changed, why it mattered, and what came before.

That's the kind of Git I want to use. The one that reflects my thinking, not just my typing.

| Practice              | Impact on Collaboration           |
| --------------------- | --------------------------------- |
| Short-lived branches  | Fast feedback, fewer merge issues |
| Clean commit messages | Easier reviews and debugging      |
| Regular rebasing      | Linear history, clarity           |

## Git, Revisited

Looking back, Git taught me more than branching strategies or stash tricks. It taught me to slow down and think. To respect history. To communicate through commits.

Joining ThoughtWorks opened my eyes to what happens when you work with people who already treat Git as part of their craft. I wasn't teaching anymore—I was learning again. And that's the best kind of growth.

Git still surprises me. Not because I don't know enough, but because I keep working with people who show me how much more it can do when used with purpose.

So yes—I'm still learning. And that's exactly why I'm still winning.
