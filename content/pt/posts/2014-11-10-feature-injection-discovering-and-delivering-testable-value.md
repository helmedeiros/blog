---
title: "Feature Injection: Descobrindo e Entregando Valor Testável"
date: 2014-11-10T14:00:00-03:00
author: Helio Medeiros
subtitle: Pare de deixar as features te puxarem pra construir primeiro e aprender depois—cace o valor, injete ele no trabalho, e detalhe por exemplo pra que cada história que entra na sprint já saia testável
tags:
  [
    "feature injection",
    "BDD",
    "hipóteses",
    "descoberta de produto",
    "agile",
    "lean",
  ]
categories: ["Events", "Agile"]
---

## Sobre o que era essa palestra

<iframe class="speakerdeck-iframe" frameborder="0" src="https://speakerdeck.com/player/73e2ed004b390132413f0a4dd3cf94f0" title="Feature Injection - descobrindo e entregando valor testável" allowfullscreen="true" allow="web-share" style="border: 0px; background: padding-box padding-box rgba(0, 0, 0, 0.1); margin: 0px; padding: 0px; border-radius: 6px; box-shadow: rgba(0, 0, 0, 0.2) 0px 5px 40px; width: 100%; height: auto; aspect-ratio: 560 / 315;" spellcheck="false" data-ratio="1.7777777777777777"></iframe>

Por boa parte da minha carreira eu vi time construindo feature primeiro e perguntando sobre valor depois. A gente pegava o backlog, fatiava por camada, estimava e empurrava. Em algum lugar entre o kickoff e a release, parava de fazer a pergunta que deveria estar fazendo o tempo todo: _isso aqui é pra quem, que comportamento a gente quer mudar, e como a gente vai saber se funcionou?_

Essa palestra era sobre virar esse hábito de cabeça pra baixo. A técnica tem nome — **Feature Injection** — e veio do Chris Matts. A forma é simples: não começa pela feature torcendo pro valor aparecer. Começa pelo valor, injeta ele no trabalho, e deixa as features caírem por exemplo.

## Caçar o Valor

Antes de qualquer user story, antes de qualquer critério de aceite, tem um resultado de negócio que alguém tá tentando mover. Caçar o valor é deixar esse resultado explícito: um número que precisa subir ou descer, um comportamento que a gente espera de um usuário real, um problema que a gente acredita que vale a pena resolver.

Se você não consegue nomear o resultado, não tá caçando ainda. Tá só listando feature.

Eu pedia pros times escreverem o resultado antes da história. Quase toda vez, o ato de escrever o resultado matava duas ou três features "óbvias" que não tinham o que tá fazendo no quadro.

## Injetar o Valor

Uma vez que o resultado tá nomeado, o trabalho flui de trás pra frente em direção a ele. Você pergunta: o que o sistema precisa fazer pra esse resultado acontecer? Essa resposta é a feature. A feature existe **por causa do valor**, não o contrário.

É aqui que Feature Injection se separa de backlog fatiado por camada. Você não tá puxando trabalho porque é o próximo card. Você tá puxando porque, sem ele, o valor não acontece.

Histórias escritas assim já vêm com duas coisas que história normal perde: um stakeholder que se importa de verdade com o resultado, e uma forma de medir se o resultado se moveu.

## Detalhar por Exemplo

O último passo é o que mais time pula. Quando você já tem uma feature amarrada num valor, você descreve como ela se comporta através de **exemplos concretos** — a mesma forma que BDD vem pregando há anos.

```text
Dado que um leitor salvou um artigo
Quando o leitor volta no dia seguinte
Então o artigo salvo aparece no topo do feed dele
```

Exemplos assim fazem três trabalhos ao mesmo tempo: especificam o comportamento, viram o teste de aceite, e viram a conversa com produto e QA antes da primeira linha de código.

Quando você detalha por exemplo, "pronto" deixa de ser uma sensação e vira um checklist que qualquer um consegue verificar.

## Suposições São Hipóteses

Toda história que eu escrevo hoje carrega uma crença não dita: que o usuário vai se importar, que a métrica vai mexer, que o comportamento esperado é o que vai acontecer. Feature Injection pede pra você escrever essa crença de propósito.

Uma história vira uma hipótese. Uma release vira um experimento. Uma métrica vira feedback, não vaidade.

É assim que você ganha o direito de dizer "a gente tá aprendendo" em vez de "a gente tá entregando."

## Falhar Rápido, Acertar Mais Rápido

O ponto disso tudo não é processo por processo. É apertar o ciclo entre ideia e evidência.

Quando o valor tá nomeado, a feature tá pequena, o exemplo tá concreto e a métrica tá mensurável, você descobre que tava errado em dias em vez de trimestres. Estar errado rápido é o prêmio. Estar errado devagar é o que mata time de produto.

## Pra Fechar

Feature Injection não é uma metodologia que você adota — é um hábito que você constrói. Cace antes de construir. Injete valor no trabalho. Detalhe por exemplo. Deixa a métrica te dizer se você tava certo.

Os times que eu vi fazendo isso bem não terminam com backlog maior. Terminam com backlog menor, e com a confiança de que o que ainda tá lá no quadro vale o tempo.

---

_Material de palestra do fim de 2014, afiado no trabalho na ThoughtWorks Brasil e nas conversas com a comunidade ágil brasileira._
Me segue: [@helmedeiros](https://twitter.com/helmedeiros)
