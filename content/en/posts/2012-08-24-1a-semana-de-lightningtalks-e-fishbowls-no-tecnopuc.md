---
title: "First Week of Lightning Talks and Fishbowls at TecnoPUC"
author: helio
layout: post
date: 2012-08-24T12:06:34+00:00
embed:
seo_follow:
seo_noindex:
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

A few hours ago at the [4º dia][1] of [1ª Semana LightningTalks e FishBowls TecnoPUC][2], I presented a Lightning Talk [ Test Driven Development &#8211; Em busca de feedback útil e concreto][3], which addressed the concept of validated feedback in software construction.

There has been a lot of talk among teams and communities I've passed through about tests and [QA][4], but apparently many of them are still running and struggling with the same battles every day.

When I say the same, I'm not talking about high-level issues like lack of specification of [critérios de aceitação][5] or completely ignoring user opinions, but rather about [bugs][6] in software, such as company X's product Y, which has already released 3 versions this year with the "send" button entirely invisible to customers.

How can we still make these types of mistakes?

Remember that old saying: making a mistake once is fine!

But committing the same mistake...

Many companies have been stuck in their initial strategy of [cenários][7] testing, where they function as endless loops of actions that need to be repeated every time a new version is released, and each error found seems to be added to this document.

Great for a first step, but a light-year away from starting to scratch the surface of efficiency.

Here it's not about how long we'll remember to execute; because failure will happen and will be evident in the one time you forget.

Plans are great starting points, but you must be ready to evolve them at any cost. > Everyone has a plan until they get punched in the face > > > -Mike Tyson It's very difficult to follow a script with perfection when there's so much at stake or minimal room for error.

At this point, stress and test execution enter what was defined as [relações diretas de influência][9], making it so that the more stress, the less attention and quality in executing tests, and thus uncertainty about the quality of tests generates more stress over what might happen ([Gráfico de influência Gerald Weinberg][10]).

At this point, stress can be even more destructive, imagine how many times a hotfix ruined the entire list of priorities and, after 30 minutes of frantic development, it was straight to production because there wasn't time to test, a small change that couldn't possibly cause bigger problems...

ANOTHER ERROR APPEARS!

Test-Driven Development (TDD) is a software development technique created/presented by [Kent Beck][11], which directs us to work based on conscious choices and minimally viable options, stimulating confidence in what's being delivered.

TDD works the order and manner in which we deliver new functionalities, automating our acceptance criteria or internal system functions with small, safe steps that allow for quick execution of these plans, just like growing applications to know when everything is correct or not!!

Values such as [CORAGEM][12] and **MD_Ref_12** of [Extreme Programming][14] are reinforced, the more you walk with constant feedback about the effect of your changes on the rest of the code, the greater your courage to embrace changes and really evolve your application.

<p style="text-align: center">
 <div style="margin-bottom: 20px;">
<iframe src="https://www.slideshare.net/slideshow/embed_code/key/ePHVpNd1rPPUEh" width="597" height="486" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen></iframe>
</iframe>
<div style="margin-bottom:5px">
    <strong><a href="//www.slideshare.net/heliomedeiros" target="_blank">View more presentations from Hélio Medeiros</a></strong>
</div>
</div>
</p>

[2]: http://jorgekotickaudy.wordpress.com/2012/08/14/1a-semana-de-lightningtalks-e-fishbowls-no-tecnopuc/ "1ª Semana de Lightining talks e Fishbowls no Tecnopuc"
[3]: /apresentacoes/ "Apresentações"
[1]: http://jorgekotickaudy.wordpress.com/2012/08/23/2308-4o-dia-semana/ "4º dia"
[5]: http://blog.scrumhalf.com.br/2011/10/criterios-de-aceitacao-das-user-stories/ "Critérios de Aceitação"
[12]: http://improveit.com.br/xp/valores/coragem "Valores XP - Coragem"
[6]: http://pt.wikipedia.org/wiki/Bug "Bug"
[14]: http://pt.wikipedia.org/wiki/Programa%C3%A7%C3%A3o_extrema "Programação Extrema"
[4]: http://pt.wikipedia.org/wiki/Garantia_da_qualidade "Quality Assurance"
[9]: http://my.safaribooksonline.com/book/software-engineering-and-development/software-testing/0321146530/patterns-for-test-driven-development/app01 "Influence diagram"
[10]: http://my.safaribooksonline.com/book/software-engineering-and-development/software-testing/0321146530/patterns-for-test-driven-development/app01 "Gerald Weinberg - Influence Graph"
[7]: http://pt.wikipedia.org/wiki/Cen%C3%A1rio_(software) "Cenários de Teste"
[11]: http://en.wikipedia.org/wiki/Kent_Beck "Kent Beck"
