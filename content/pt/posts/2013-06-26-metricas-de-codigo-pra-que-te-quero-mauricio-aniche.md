---
title: Métricas de código, pra que te quero? -Mauricio Aniche
author: helio
layout: post
date: 2013-06-26 18:56:30+00:00
embed:
  - This is the default text
seo_follow:
  - "false"
seo_noindex:
  - "false"
dsq_thread_id:
  - 4969967005
categories:
  - Events
  - Architecture
  - Agile
subtitle: Pare de adivinhar e comece a medir—aprenda como usar métricas de código, análise de coesão e ferramentas de visualização como CodeCity para tomar decisões baseadas em dados sobre sua base de código
---

Tomar decisões é muito complicado e em software, na vida vivemos de achometro e em código devemos parar de fazer isso.

Qual parte do código deve ser iniciada a cobertura ou os testes, a classe mais fácil, a mais conhecida, a que possui mais dependentes. O Aniche defende que assim como decisões de negócio são apoiadas por mineração de dados devemos fazer o mesmo com os nossos dados sobre código.

Software apodrece! Precisamos pensar nas métricas, precisamos ir além da nossa percepção.

Dizer oque é um código bonito ou um código feio é difícil, até porque perceber ou definir ou unanimizar estes índices é difícil. Cada pessoa tem o seu número ideial, por que não realizarmos uma melhoria gradativa, vamos tirando média e puxando os muito acima para a média, ajuda?

Qual a quantidade de métodos máximo de uma classe, para que ela seja considerada bonita? Novamente cada pessoa pode encontrar ou definir sua própria métrica para uma classe DEUS(o PMD define que classes com muitas atribuições são DEUS).

Quantas responsabilidades uma classe tem? Uma classe com 10m poderia ter muitas responsabilidades? Num mundo O.O. temos atributos e métodos, se uma classe tem 4 atributos e 2 métodos, se o método 1 altera 2 atributos  e o 2 os outros 2 métodos, esta métrica pode nos ajudar a falar sobre coesão e responsabilidades? E isto é absoluto?

Precisamos olhar os acoplamentos das classes, preciso saber quantas classes eu dependo e quantas dependem de mim…. talvez estes acoplamentos sejam bons… ou não?

Ainda dentro do tópico de acoplamento temos as co-changes, que são acoplamentos que não podemos ver, toda vez que altero um objeto ou mbean e não altero a jsp, tenho erros, este também deve ser observado de perto.

Vê a quantidade de métricas que temos. Será que poderíamos combiná-las? Temos métricas de implementação, projeto de classes… existem estudos sobre estes resultados, e com toda certeza devemos usá-lo.

Podemos ver quais arquivos são mais comitados, quem são os responsáveis pelos comits. Podemos potencializar a qualidade, utilizar o conhecimento.

Quem e quando gerou mais bugs? Podemos descobrir quem corrigiu algo, que dia foi esse e quem sabe podemos fazer algo a respeito. Muitos riscos podem ser minimizados entendendo um pouco mais estas métricas.

Uma imagem vale mais que mil palavras! Descubra oque está por baixo do teu capô, e faça isso com gráficos, podemos analisar rapidamente e entender oque acontece. Olhe o [CodeCity][1], use DSM, Matrix Pyramid, veja o Kiviat, JDpendend, JavaNCSS, Eclipse Metrics! Nem tudo é perfeito mas vale testar!!

[1]: http://www.inf.usi.ch/phd/wettel/codecity.html "code city"
