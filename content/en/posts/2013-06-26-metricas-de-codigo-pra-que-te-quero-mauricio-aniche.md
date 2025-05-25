---
title: "Code metrics, what I want them for? -Mauricio Aniche"
author: helio
layout: post
date: 2013-06-26T18:56:30+00:00
url: /2013/06/26/metricas-de-codigo-pra-que-te-quero-mauricio-aniche/
embed: 
seo_follow: 
seo_noindex: 
dsq_thread_id: 
categories:
  - Ageis
  - Eventos
  - Metodologias
---

Making decisions is very complicated and in software, we live by guesswork.

In code, we should stop doing this.

Which part of the code should be started with coverage or tests, the easiest class, the most well-known one, the one with more dependencies?

Aniche advocates that just as business decisions are supported by data mining, we should do the same with our code data.

Software is rotting!

We need to think about metrics; we need to go beyond our perception.

Saying what is a beautiful or ugly code is difficult, even because perceiving or defining or unanimous indexes is difficult.

Each person has their own ideal number, so why not perform gradual improvements?

Let's take the average and pull the ones far above up to the average, right?

What is the maximum number of methods for a class, so that it can be considered beautiful?

Again, each person may find or define their own metric for a class (PMD defines that classes with many attributes are God).

How many responsibilities does a class have?

A class with 10 methods could have many responsibilities?

In an OOP world, we have attributes and methods.

If a class has 4 attributes and 2 methods, if method 1 changes 2 attributes and method 2 changes the other 2 attributes, this metric can help us talk about cohesion and responsibilities...

And that's absolute?

We need to look at the couplings between classes; I need to know how many classes I depend on and how many depend on me... maybe these couplings are good... or not?

Still within the topic of coupling, we have co-changes, which are couplings we can't see.

Every time I change an object or mbean and don't change the JSP, I get errors.

This also needs to be observed closely.

Look at the number of metrics we have.

Can we combine them?

We have implementation metrics, class project... there are studies on these results, and with certainty, we should use it.

We can see which files are more committed, who is responsible for the commits.

We can potentialize quality, utilize knowledge.

Who generated more bugs when?

We can discover who fixed something, what day that was, and maybe we can do something about it.

Many risks can be minimized by understanding these metrics a little better.

A picture is worth more than a thousand words!

Discover what's under your hood, and do that with graphs.

We can analyze quickly and understand what happens.

Look at [CodeCity][1], use DSM, Matrix Pyramid, see Kiviat, JDpendent, JavaNCSS, Eclipse Metrics!

Not everything is perfect, but it's worth testing!!

[1]: http://www.inf.usi.ch/phd/wettel/codecity.html "code city"