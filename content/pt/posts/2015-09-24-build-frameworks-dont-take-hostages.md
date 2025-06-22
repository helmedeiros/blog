---
title: "Faça Frameworks, Não Faça Reféns"
date: 2015-09-24T14:00:00-03:00
author: Helio Medeiros
subtitle: Cure a frameworkitis escolhendo ferramentas com intenção—avaliando adaptabilidade sobre tendências, construindo para clareza sobre esperteza, e criando frameworks que apoiam equipes ao invés de aprisioná-las
tags:
  [
    "frameworks",
    "arquitetura",
    "design de software",
    "desenvolvimento",
    "tdc",
    "frameworkite",
  ]
categories: [ "Architecture", "Events"]
---

## Sobre o Que Era Essa Palestra

Essa palestra não era contra frameworks. Era um alerta.

Nos últimos dez anos, vimos uma explosão de frameworks em todas as linguagens. Mas junto com essa explosão, veio um efeito colateral perigoso: desenvolvedores pararam de perguntar "por quê?" e começaram a apenas seguir o "como". Frameworks viraram dogma. E pior: viraram prisões.

Eu chamei isso de **Frameworkite**.

Essa palestra é sobre como chegamos aqui, o que interpretamos errado e o que precisamos fazer para criar ferramentas que apoiem os times — em vez de aprisioná-los.

## O Que os Frameworks Deveriam Ser

Quando Erich Gamma e o Gang of Four apresentaram os design patterns, a ideia era simples: incentivar a reutilização, reduzir a duplicação e construir sistemas com blocos testados. Os frameworks nasceram disso. Eles deveriam **abstrair problemas repetitivos** para que pudéssemos focar no que realmente importa.

Mas, em algum ponto do caminho, paramos de tratar frameworks como ferramentas. Começamos a tratá-los como fundação, como arquitetura, como sistema.

E com isso, esquecemos o primeiro princípio do bom software: **você deve construir para o seu problema**, não em torno da abstração dos outros.

## Como Avaliar um Framework (Ao Invés de Só Adotar)

Muitas vezes escolhemos frameworks pelo hype, não pela adequação. Mas escolher um framework é uma decisão estratégica. Ela define a curva de aprendizado do time, o código, a flexibilidade.

O que devemos observar, então?

Primeiro, a adaptabilidade. Um bom framework se molda ao seu problema. Um ruim obriga você a moldar seu problema ao framework.

Segundo, a simplicidade. Se são necessários três arquivos, dois decoradores e um diagrama de ciclo de vida pra explicar um endpoint, isso não é poder — é complexidade.

Terceiro, princípios arquiteturais. O código segue os princípios SOLID? Há sinais de inversão de controle? Se não, provavelmente é uma colagem acoplada e mágica, difícil de manter.

Por fim, a comunidade. Porque sejamos honestos: você não está só adotando código, está entrando numa tribo. Frameworks com comunidades ativas, honestas e experimentais sobrevivem mais do que alternativas isoladas, mesmo que tecnicamente melhores.

## O Ecossistema Molda o Framework

Frameworks não surgem no vácuo. Eles são artefatos culturais.

Frameworks em Java geralmente refletem rigor corporativo. Em JavaScript, tendem à experimentação e velocidade. Ruby trouxe elegância e DSLs. Python valorizou clareza e ciência.

A maturidade, filosofia e dores de uma comunidade moldam os frameworks que ela cria. Por isso, avalie também o **DNA da linguagem de origem**.

## O Mundo Mudou. As Ferramentas Nem Tanto.

De 2013 a 2015, a escala dos sistemas digitais mudou radicalmente. Mais usuários, mais dispositivos, mais dados, mais concorrência, mais exceções.

Mas a maioria dos frameworks continuou vendendo as mesmas promessas com as mesmas abstrações. Poucos se adaptaram. E sejamos francos: a maioria de nós nem teve tempo de parar e repensar. O negócio pressionava. Releases não esperavam.

A gente remendou. Hackeou. Empilhou abstrações. E começamos a ver cada vez mais sistemas onde os devs estavam **usando ferramentas que não entendiam para resolver problemas que não sabiam nomear**.

## Usando um Framework? Fique Atento.

É tentador simplesmente "pegar o full-stack" e seguir em frente. Mas, toda vez que fizer isso, pergunte:

- Esse framework me permite descrever _o que_ quero resolver ou me força a seguir um _como_?
- Estou usando um ecossistema modular que me dá escolha ou um monólito que me prende?
- O framework evolui na direção que preciso ou vai me forçar a fazer gambiarras daqui a seis meses?

Não se trata de evitar frameworks. Mas de usá-los **com clareza e intenção**.

## Criando um Framework? Vá com Calma.

Agora inverta a lógica.

Se você está criando ou estendendo um framework, está moldando o futuro de outra pessoa. Isso é sério.

Não presuma que conhece todos os casos de uso. Construa o núcleo primeiro. E permita que outras pessoas adicionem o que quiserem **sem precisar hackear o core**.

Não force acoplamentos desnecessários. Deixe que desenvolvedores possam plugar, sobrescrever ou até sair.

E acima de tudo, escreva código que as pessoas entendam. Esperteza envelhece mal. Clareza sobrevive.

## Existe Cura Para a Frameworkite?

Sim. Mas não é fácil. E não vem numa caixa.

O primeiro passo é **lembrar que frameworks são apenas ferramentas**. Eles não são linguagens. Não são arquiteturas. São auxiliares. Trate-os assim.

Prefira bibliotecas e toolkits que permitem montar soluções ao invés de frameworks que tentam controlar tudo.

Seja cético. Leia o código. Teste. Quebre. Entenda o que acontece. Nunca leve algo à produção só porque "todo mundo usa".

E se tudo falhar: **elimine a mágica**. Mágica é ótima até quebrar — depois vira armadilha. Prefira transparência a truques.

## Pensamento Final

Você pode criar frameworks incríveis. Pode usar ótimos também. Mas faça isso com propósito. Faça com consciência. E nunca esqueça:

**Um bom framework apoia seu time. Um ruim o mantém refém.**

_Apresentado no TDC Porto Alegre — 24 de Setembro de 2015, na trilha de Arquitetura._
Me siga: [@helmedeiros](https://twitter.com/helmedeiros)
