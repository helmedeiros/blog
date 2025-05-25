---
title: 1ª Semana de LightningTalks e FishBowls no TecnoPUC
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
Aconteceu há algumas horas o [4º dia][1] da [1ª Semana de LightningTalks e FishBowls no TecnoPUC][2] onde apresentei a Lightning Talk [ Test Driven Development &#8211; Em busca de feedback útil e concreto][3], que abordava o conceito de feedback validado na construção de software.

Muito se tem falado por equipes e comunidades por onde transito sobre testes e [QA][4], mas aparentemente muitas delas ainda estão correndo e lutando as mesmas batalhas todos os dias. Quando digo as mesmas, não falo a alto nível como falta de especificação dos [critérios de aceitação][5] ou negligenciar completamente a opinião final do usuário, e sim de [bugs][6] nos softwares, tipo a empresa X no produto Y já entregou 3 versões este ano com o &#8220;botão de enviar&#8221; totalmente invisível ao cliente. Como podemos ainda cometer estes tipos de erro? Lembram aquele velho ditado fazer errado uma vez, tudo bem! Mas cometer o mesmo erro &#8230;

Muitas empresas tem se mantido congelados na estratégia inicial de [cenários][7] de teste, onde os mesmos funcionam como [checklists][8] intermináveis de ações que devem ser repetidas sempre que uma versão for ser lançada, e cada erro encontrado aparentemente está sendo adicionado neste documento. Ótimo para um primeiro passo, mas a anos-luz de iniciarmos a arranhar a superfície da eficiência. Aqui não se trata de por quanto tempo iremos nos lembrar de executar, por que a falha acontecerá e será evidente na única vez que você esquece-lo. Planos são ótimos pontos de partida, mas você deve estar pronto para evoluí-lo a qualquer custo.

> Todos tem um plano, até serem socados na cara
> 
> <p style="text-align: right">
>   -Mike Tyson
> </p>

É muito difícil seguir um script com perfeição quando se tem tanto a perder, ou a impactar ao mínimo erro. Neste ponto que stress e execução dos testes entram no que foi definido como [relações diretas de influência][9], de forma que quanto maior o stress, menor atenção e qualidade na realização dos testes, e  assim a incerteza sobre a qualidade dos testes gera mais stress sobre o que pode acontecer ([Gráfico de influência de Gerald Weinberg][10]). Neste ponto o stress pode ser ainda mais destruidor, imagine quantas vezes um hotfix furou toda a lista de priorizações e, após os 30min mais alucinantes de desenvolvimento foi direto a produção porque não havia tempo para ser testado, uma alteração tão pequena não poderia gerar maiores problemas&#8230; OUTRO ERRO APARECEU!

O Desenvolvimento Orientado a Testes ou TDD, é uma técnica para desenvolvimento de software, criada/apresentada pelo [Kent Beck][11], que nos direciona ao trabalho baseado em escolhas conscientes e minimamente viáveis, estimulando o aumento na confiança sobre oque está sendo entregue. O TDD trabalha a ordem e o modo que entregamos novas funcionalidades, automatizando nossas listas de critérios de aceitação ou funcionalidades internas do sistema, com pequenos passos seguros que permitem num curto tempo a execução destes planos, assim como crescimentos de aplicações de forma a sabermos quando tudo está certo ou não!! Valores como [CORAGEM][12] e [FEEDBACK][13] da [Extreme Programming][14] são reforçados, quanto mais você anda com feedback constante sobre o efeito de suas alterações no resto do código, maior sua coragem para abraçar mudanças e realmente evoluir sua aplicação.

<p style="text-align: center">
  [slideshare id=14055677&doc=testdrivendevelopment-embuscadefeedbackutileconcreto-120823190008-phpapp02]
</p>

 [1]: http://jorgekotickaudy.wordpress.com/2012/08/23/2308-4o-dia-semana/ "4º dia"
 [2]: http://jorgekotickaudy.wordpress.com/2012/08/14/1a-semana-de-lightningtalks-e-fishbowls-no-tecnopuc/ "1ª Semana de Lightining talks e Fishbowls no Tecnopuc"
 [3]: /apresentacoes/ "Apresentações"
 [4]: http://pt.wikipedia.org/wiki/Garantia_da_qualidade "Quality Assurance"
 [5]: http://blog.scrumhalf.com.br/2011/10/criterios-de-aceitacao-das-user-stories/ "Critérios de Aceitação"
 [6]: http://pt.wikipedia.org/wiki/Bug "Bug"
 [7]: http://pt.wikipedia.org/wiki/Cen%C3%A1rio_(software) "Cenários de Teste"
 [8]: http://en.wikipedia.org/wiki/Checklist "checklist"
 [9]: http://my.safaribooksonline.com/book/software-engineering-and-development/software-testing/0321146530/patterns-for-test-driven-development/app01 "Influence diagram"
 [10]: http://my.safaribooksonline.com/book/software-engineering-and-development/software-testing/0321146530/patterns-for-test-driven-development/app01 "Gerald Weinberg - Influence Graph"
 [11]: http://en.wikipedia.org/wiki/Kent_Beck "Kent Beck"
 [12]: http://improveit.com.br/xp/valores/coragem "Valores XP - Coragem"
 [13]: http://improveit.com.br/xp/valores/feedback "Valores XP - Feedback"
 [14]: http://pt.wikipedia.org/wiki/Programa%C3%A7%C3%A3o_extrema "Programação Extrema"