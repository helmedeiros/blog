---
title: Padrões de Análise
author: helio
layout: post
date: 2008-07-12T03:27:57+00:00
categories:
  - Padrões de Análise
---
Há algumas semanas, tive durante a aula de MODELAGEM ORIENTADA A OBJETOS E UML, ministrada pelo professor Osmar Fernandes Jr., uma breve introdução aos Padrões de Software, para Análise (Analysis Patterns) e Projetos (Design Patterns), sobre a qual me faço nesta página, abrindo um pequeno espaço a aqueles, que assim como eu estão iniciando os seus estudos na área.

Com a complexidade inerente aos processos, de negócios, ORGANIZACIONAIS, que se transformam dia-a-dia em milhares de níveis de código e modelagem, de novos módulos de trabalho, tornasse imprescindível o conhecimento de técnicas de modelagem conceitual.
  
Dentro deste contexto, nos deparamos com os Padrões de Software que, como dito anteriormente, subdivide-se principalmente em duas vertentes  que permitem o compartilhamento de soluções e conceituação de soluções formais, a problemas recorrentes no desenvolvimento de software.

Martin Fowler, em seu livro <a href="http://www.amazon.com/Analysis-Patterns-Reusable-Addison-Wesley-Technology/dp/0201895420" title="Analysis Patterns: Reusable Object Models" target="_blank">Analysis Patterns: Reusable Object Models</a>, define dentre os tipos de padões de software  os padrões de Análise. Estes padrões são um conjunto de classes  e associações que possue algum significado no contexto da aplicação, que quando reinterpretados para os processos da organização, permitem soluções claras e autenticadas sobre muitos aspectos.

Dentre os padrões de projeto estabelecidos pelo autor supracitado podemos ressaltar:

  * Party: Define um objeto parte como um supertipo para uma pessoa ou organização,  de maneira que a associação entre  informações fosse relativa às partes e não às pessoa ou organização diretamente.

![Analysis Pattern - Party][1]

  * Organization Hierarchies: Modela uma hierarquia organizacional através de uma estrutura recursiva. Estabelecendo relacionamentos entre entidades organizacionais através de regras.

![Analysis Pattern - Organization Hierarchies][2]

  * Organization Structure: Usa tipos para definir relacionamentos entre entidades organizacionais.

![Analysis Pattern - Organization Structure][3]

  * Quantity: Define um tipo de objeto que tem como parte numeros e unidades.

![Analysis Pattern - Quantity][4]

  * Conversation Ratio: Define um objeto de conversão entre unidades, e dá a quantidade uma operação, convertTo(Unit), que retorna uma nova quantidade na unidade.

![Analysis Pattern - Quantity][5]

  * Compound Units: Uma unidade composta é a combinação entre unidades atômicas, por exemplo milhas por hora. Uma operação de conversão sofisticada pode usar um conversor em uma unidade atômica para converter unidades compostas.

 [1]: /uploads/2008/07/picture-2.png
 [2]: /uploads/2008/07/picture-3.png
 [3]: /uploads/2008/07/picture-4.png
 [4]: /uploads/2008/07/picture-5.png
 [5]: /uploads/2008/07/picture-6.png