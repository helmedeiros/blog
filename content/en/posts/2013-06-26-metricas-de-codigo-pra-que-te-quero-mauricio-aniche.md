---
title: "Metrics of code, why do I want you? - Mauricio Aniche"
date: 2013-06-26
slug: metricas-de-codigo-pra-que-te-quero-mauricio-aniche
draft: false
language: en
---

Deciding on code is very complicated and in software, we live by guesswork and should stop doing that.
Which part of the code should be started with coverage or testing, the easiest class, the most known, the one with the most dependencies. Aniche advocates for using data mining to support business decisions just as we should do with our code data.

Software is rotten! We need to think about metrics; we need to go beyond our perception.
Saying what makes a piece of code beautiful or ugly is hard, and even defining or agreeing on these indices is difficult. Each person has their own ideal number, so why not implement gradual improvement, taking the average and pulling those above it up, helps?

What's the maximum number of methods in a class for it to be considered beautiful? Again, each person may find or define their own metric for a class.
How many responsibilities does a class have? A class with 10 attributes might have many responsibilities? In an O.O. world, we have attributes and methods; if a class has 4 attributes and 2 methods, if method 1 changes 2 attributes and method 2 the other 2, this metric can help us talk about cohesion and responsibilities?

We need to look at the class couplings, I need to know how many classes I depend on and how many depend on me... maybe these couplings are good... or not?
Within the topic of coupling, we have co-changes, which are couplings we can't see; every time I change an object or MBean without changing JSP, I get errors. This also needs to be observed closely.

Look at the number of metrics we have. Can we combine them? We have implementation metrics, project class metrics... there are studies on these results, and with certainty we should use it.

We can see which files are most committed, who's responsible for commits. We can potentialize quality, utilize knowledge.
Who generated more bugs? We can discover who fixed something, what day that was, and who might be able to do something about it. Many risks can be minimized by understanding these metrics a little better.

A picture is worth more than a thousand words! Discover what's underneath your hood, and do that with graphs; we can quickly analyze and understand what's happening. Look at CodeCity, use DSM, Matrix Pyramid, see Kiviat, JDepend, JavaNCSS, Eclipse Metrics! Not everything is perfect, but it's worth trying!!