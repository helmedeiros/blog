---
title: ""
author: helio
layout: post
date: 2012-08-24T12:06:34+00:00
url: /2012/08/24/1a-semana-de-lightningtalks-e-fishbowls-no-tecnopuc/
embed:
  - This is the default text
seo_follow:
  - 'false'
seo_noindex:
  - 'false'
categories:
  - Ageis
  - Apresentações
  - Eventos
  - Metodologias
  - Slides
tags:
  - coragem
  - extreme programming
  - Feedback
  - TDD
  - Test Driven Development
  - Testes
  - XP
---


A few hours ago at the [4º dia][1] of [1ª Semana de LightningTalks e FishBowls no TecnoPUC][2], I presented a Lightning Talk [ Test Driven Development &#8211; Em busca de feedback útil e concreto][3], which addressed the concept of validated feedback in software construction.

There has been a lot of talk among teams and communities I've passed through about tests and [QA][4], but apparently many of them are still running and struggling with the same battles every day. When I say the same, I'm not talking about high-level issues like lack of specification of [critérios de aceitação][5] or completely ignoring user opinions, but rather about [bugs][6] in software, such as company X's product Y, which has already released 3 versions this year with the "send" button entirely invisible to customers. How can we still make these types of mistakes? Remember that old saying: making a mistake once is fine! But committing the same mistake...

Many companies have been stuck in their initial strategy of [cenários][7] testing, where they function as endless loops of actions that need to be repeated every time a new version is released, and each error found seems to be added to this document. Great for a first step, but a light-year away from starting to scratch the surface of efficiency. Here it's not about how long we'll remember to execute; because failure will happen and will be evident in the one time you forget. Plans are great starting points, but you must be ready to evolve them at any cost.

> Everyone has a plan until they get punched in the face
>
> 
> -Mike Tyson

It's very difficult to follow a script with perfection when there's so much at stake or minimal room for error. At this point, stress and test execution enter what was defined as [relações diretas de influência][9], making it so that the more stress, the less attention and quality in executing tests, and thus uncertainty about the quality of tests generates more stress over what might happen ([Gráfico de influência de Gerald Weinberg][10]). At this point, stress can be even more destructive, imagine how many times a hotfix ruined the entire list of priorities and, after 30 minutes of frantic development, it was straight to production because there wasn't time to test, a small change that couldn't possibly cause bigger problems... ANOTHER ERROR APPEARS!

Test-Driven Development (TDD) is a software development technique created/presented by [Kent Beck][11], which directs us to work based on conscious choices and minimally viable options, stimulating confidence in what's being delivered. TDD works the order and manner in which we deliver new functionalities, automating our acceptance criteria or internal system functions with small, safe steps that allow for quick execution of these plans, just like growing applications to know when everything is correct or not!! Values such as [CORAGEM][12] and __MD_Ref_12__ of [Extreme Programming][14] are reinforced, the more you walk with constant feedback about the effect of your changes on the rest of the code, the greater your courage to embrace changes and really evolve your application.

<p style="text-align: center">
  [slideshare id=14055677&doc=testdrivendevelopment-embuscadefeedbackutileconcreto-120823190008-phpapp02]
</p>