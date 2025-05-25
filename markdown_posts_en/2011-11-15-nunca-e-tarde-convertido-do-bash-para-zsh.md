---
title: "It's never too late! Converted from Bash to ZSH!"
date: 2011-11-15
slug: nunca-e-tarde-convertido-do-bash-para-zsh
draft: false
language: en
---

After using zsh for a good time, I recently presented it to a friend who was surprised, and after talking about it a bit, the idea of learning more and sharing... I was influenced by the oh-my-zsh wave for some time, but ended up not contributing anything. Who knows now?!?!

Starting from scratch, I believe that most of us have encountered a command-line shell at some point in our lives. The shell is an interface to the system's operational functions, typically accessed through Terminal or iTerm2 on MacOS. There are many shells to choose from, and most operating systems/distributions end up "facilitating" this choice by setting some standard. For a long time, I only knew the most popular one, GNU Bourne Again Shell or bash, which is an excellent choice when you need to repeat commands that are already in your history, to start some container or view logs... but terrible when you're using Git and RVM (1) for the branch I'm on and (2) to see the version of Ruby and gems) or learning new commands and utilizing new DevOps techniques (I recently took the Egenial Imersão Sys Deploy course).

## zsh?

The Z-shell or zsh is one of the most complete shells in terms of functionality and usability among those available on Darwin, which comes with tsch as default since v.7.0 present on Mac Os X Panther. The zsh team does an excellent job explaining and advocating for their work, but like everyone else, I have my own preferences.

1. Spell checker: Who never wrote _rmv, fnd, mkdr _or any other command incorrectly? The zsh has a spell-checker that scans and presents the most correct option between commands and sub-commands. Was I wrong to let it correct me?
zsh: correct ‘rmv’ to ‘rvm’ [nyae]?

1. Tab completion: Most shells like bash have tab completion, but none as simple or friendly as zsh. Whether in terms of configuration or usability, zsh gives a bath. It presents a navigable menu of sub-commands and options for filling in, such as the list of directories when executing an ls, or the list of processes when executing a kill.

2. Sharing history: Keeping history between sessions instead of overwriting it, there's nothing worse than losing the history of executed commands because a session had been overwritten, zsh keeps the history of multiple sessions.

3. Globbing. The zsh has taken great care with its wildcards, and the results are incredible _ls git*~flow _or ls (GOL|TAM)POA , always take a look at the zsh introduction.

4. Creating functions with aliases. The zsh allows the creation of functions called by its aliases, in an easy and agile way.