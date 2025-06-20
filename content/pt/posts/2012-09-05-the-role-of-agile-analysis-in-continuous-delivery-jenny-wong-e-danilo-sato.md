---
title: The role of Agile analysis in Continuous Delivery – Jenny Wong e Danilo Sato
author: helio
layout: post
date: 2012-09-05T17:45:08+00:00
embed:
  - This is the default text
seo_follow:
  - 'false'
seo_noindex:
  - 'false'
categories: ["Agile"]
tags:
  - '#AgileBR'
  - 2012
  - agile brazil
  - agilebrazil2012
  - continuos delivery
  - Danilo Sato
  - Jenny Wong
  - MVP
---
[<img class="aligncenter size-full wp-image-596" src="/uploads/2012/09/Screen-Shot-2012-09-05-at-3.07.27-PM.png" alt="" width="470" height="249" srcset="/uploads/2012/09/Screen-Shot-2012-09-05-at-3.07.27-PM.png 470w, /uploads/2012/09/Screen-Shot-2012-09-05-at-3.07.27-PM-300x158.png 300w" sizes="(max-width: 470px) 100vw, 470px" />][1]

O que é <a title="Continuos Delivery" href="http://en.wikipedia.org/wiki/Continuous_delivery" target="_blank">entrega continua</a>(continuos Delivery &#8211; CD)? Assim começou a apresentação! A seguir em palavras trocadas entre a <a title="Jenny Wong - Twitter" href="http://twitter.com/jenny_wong" target="_blank">Jenny</a> e o <a title="Danilo Sato - Blog" href="http://www.dtsato.com/blog/" target="_blank">Danilo</a>, vimos o que se seguiria, princípios de analise e engenharia envolvidos, definições e por fim princípios e atividades que podem ser utilizadas e testadas para realmente avançarmos nesta prática avançando de forma consciente as nossas entregas continuamente durante os seus dias e sprints.

Entrega contínua é uma estratégia de desenvolvimento de software que otimiza o seu processo de entrega para obter software de alta qualidade, de valor entregue o mais rápido possível, mas por mais incrível que pareça, como a maior parte das estratégias lidas por nós acabamos por nos aprofundar e priorizar práticas e passos de como ao invés dos porquês. Para o Danilo é perceptível a predominância sob os manuais e blogs que falam sobre CD, a abordagem de estratégias apenas em termos de engenharia com dicas e passo-a-passos tecnológicos que deixam um pouco de lado a questões de analise, produto e principalmente o valor relacionado a entrega, e é exatamente sob este aspecto que a analise ágil adentra o tópico sobre o qual precisamos refletir.

&nbsp;

Primeiro porque precisamos de CD, segundo o Danilo, apesar de termos quebrado o pensamento comum, trabalhando colaboração entre analistas e designs, iterações mais rápida, feedback continuo entre outros por meio de agile, ainda existe muito a ser trabalhado depois até realmente entregarmos algo em produção, que ainda nos faz demorar muito a chegar lá. Ai entra o CD e aí que se acumulam os aspectos técnicos, você automatiza tudo e está bem? Estamos entregando o certo mais rápido? Não adianta entregarmos mais rápido, trabalhando a construção de ciclos de feedback se não trabalharmos no crescimento rápido de valor. Então CD não só entregar, este não é o objetivo e deve ser sim entregar a coisa correta mais rápido, reduzir os riscos e realmente ter concluído o que foi iniciado. Baseado nisso foram apresentados alguns princípios que precisam ser considerados no caminho para a Entrega Conitnua.

Princípios:

#1 &#8211; Pensando além do software em funcionamento temos, que pensar o objetivo, qual o publico a que se destina o software, quais os critérios qualitativos que serão considerados no caminho do CD.

#2 &#8211; Passos pequenos e incrementais.

#3 &#8211; Gerenciamento do produto continuo, não podemos ver o trabalho como concluído quando entregamos o produto, existem vários outros processos que avançam alem das fronteiras da engenharia e da desenvolvimento do produto. Precisamos continuar recolhendo nas fases seguintes como números de vendas da equipe comercial entre outros para saber quando o produto realmente está concluindo.

#4 &#8211; Planejar a aposentadoria de funcionalidades no seu sistema, precisamos continuar analisando e removendo funcionalidades desnecessárias, não adianta corrermos entregarmos, monitorarmos e não voltarmos atrás removendo oque não é desejado.

#5 &#8211; Entregar VALOR não é igual a ter completo algo, como uma funcionalidade, evoluir pode ser um valor muito precioso para seu público.

Como podemos tornar isso prático?

Primeiro foi dito que devemos pensar em como LESS is More, então precisamos entregar o menor subconjunto para entregarmos os blocos menores ([Slicing and Dicing your stories][2] &#8211; Danilo e Jenny ).

Segundo devemos pensar e trabalhar o nosso <a title="Minimum viable product" href="http://en.wikipedia.org/wiki/Minimum_viable_product" target="_blank">MVP</a>, mas para Jenny muito tem se falado neste termo de forma altamente atrelada a códigos e engenharia, quando deveria ser aquilo que é o mínimo necessário em termos de produtos para validarmos juntos aos nossos clientes se eles realmente irão usá-los ou quere-lo, não precisa ser nem código , basta lembrar como o dropbox começou com um video que apontou os possíveis clientes, quem gostar pode se candidatar. Para a Jenny devemos sair de nossos prédios e começar a encarar nossos clientes de frente com pequenas e simples ferramentas existentes tentando descobrir oque é desejado antes de realmente fazer. Esta é uma forma de conseguirmos feedback evitando entregar realmente rápido o indesejados.

Terceiro precisamos manter nossos backlogs, qual a essência de cada suposição que existia por trás de cada um dos itens existentes lá. Gerenciá-lo e ver porque estamos deixando algo para depois pode sinalizar algo? Por fim precisamos &#8220;Podar não escovar o seu backlog&#8221;.

Quarto adicione a cada funcionalidade qual o feedback que você espera, e adicione-a a sua funcionalidade como uma só, vai se provar a funcionalidade por fim mais eficiente. Não devem ser ferramentas muito genéricas com <a title="Métricas de vaidade" href="http://techcrunch.com/2011/07/30/vanity-metrics/" target="_blank">métricas de vaidade</a>, e sim feedbacks que sejam visíveis, validáveis e com períodos representativos ao que se espera em termos de ação e re-ação.

Por fim foi sugerido um novo approach, com menos trabalho sendo realizado em grandes pacotes(<a title="Big Design Up Front" href="http://en.wikipedia.org/wiki/Big_Design_Up_Front" target="_blank">BDUF</a>) com suposições épicas sem validação, pesquisas envolvendo usuários, <a title="Guerilla Testing" href="http://www.slideshare.net/andybudd/guerilla-usability-testing" target="_blank">guerrilla testing</a>, analise de testes e muita colaboração, desta forma teremos a entrega de um produto mais relevante e com mais sentido ao que a entrega dos produtos de forma rápida realmente devem estar em termos, sucesso em continuamente entregar o que é desejado! Ou aprender e chegar lá o quanto antes!

Veja a apresentação a baixo:

<div style="margin-bottom:5px">
  <strong> <a href="http://www.slideshare.net/JennyWong8/role-of-agile-analysis-in-continuous-delivery" title="Role of Agile analysis in continuous delivery" target="_blank">Role of Agile analysis in continuous delivery</a> </strong> from <strong><a href="http://www.slideshare.net/JennyWong8" target="_blank">Jenny Wong</a></strong>
</div>

 [1]: /uploads/2012/09/Screen-Shot-2012-09-05-at-3.07.27-PM.png
 [2]: http://www.slideshare.net/JennyWong8/slicing-and-dicing-your-user-stories "Slicing and Dicing user stories"