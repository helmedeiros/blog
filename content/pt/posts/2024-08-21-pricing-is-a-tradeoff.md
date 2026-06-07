---
title: "Pricing É um Trade-off"
categories:
  - Engineering
  - Experimentation
  - Pricing
  - Product
date: 2024-08-21
tags:
  - pricing
  - otimizacao
  - tomada-de-decisao
  - monetizacao
  - experimentacao
  - estrategia-de-produto
description: "Por que a pergunta mais difícil em pricing não é o que devemos cobrar — é o que estamos dispostos a sacrificar?"
subtitle: "Pricing não é a arte de achar o maior preço. É a disciplina de escolher quais trade-offs importam."
---

Por alguns anos, trabalhei em uma plataforma de pricing — a parte do sistema que decide o que cobrar de um cliente, e quando. Quando sentei para escrever isto, a plataforma já tinha passado por várias mudanças de enquadramento. Tínhamos tirado regras do código para um motor de regras de negócio. Tínhamos parado de subir mudanças de pricing no escuro e começado a tratá-las como experimentos. Tínhamos parado de fingir que "cliente médio" era um conceito útil. E tínhamos aprendido que grupos diferentes de clientes respondiam a preço ao longo de curvas, não pontos.

Por muito tempo, mesmo por baixo de tudo isso, eu ainda achava que pricing era um problema de busca. Encontrar o preço certo. Aplicar. Medir o resultado. Seguir.

Cada lição arrancava um pedaço dessa crença. Regras de pricing eram hipóteses. Clientes não eram médias. Respostas formavam curvas. Em algum momento, surgiu uma percepção diferente.

A pergunta mais difícil em pricing não era *o que devemos cobrar?*

Era *o que estamos tentando otimizar?*

Essa pergunta mudou como eu pensava sobre pricing. Porque toda decisão de pricing é um trade-off.

## A otimização fácil

Imagine que seu único objetivo é receita.

O problema parece direto. Subir preços. Ganhar mais por compra. Comemorar.

A realidade é menos cooperativa. Clientes reagem. A demanda muda. Concorrentes existem. Confiança importa.

O que parece um problema de otimização vira rapidamente um malabarismo. O erro é supor que existe um único número esperando para ser descoberto. Normalmente não existe. Existem múltiplos resultados se movendo em direções diferentes.

## Receita versus conversão

Esse é o primeiro trade-off que a maioria dos times de pricing encontra.

Um preço mais alto frequentemente significa mais receita por transação. Ao mesmo tempo, pode reduzir conversão.

{{< plantuml title="O primeiro trade-off: receita por compra contra taxa de compra" >}}
@startuml
skinparam shadowing false
start
:Preço mais alto;
:Receita maior por compra;
:Taxa de compra menor;
stop
@enduml
{{< /plantuml >}}

A pergunta difícil não é se a conversão cai. A pergunta difícil é se a receita adicional compensa essa queda.

E mesmo isso frequentemente é simplista demais. Porque conversão raramente é a única coisa com a qual nos importamos.

## Receita versus confiança

Uma lição que me surpreendeu foi com que frequência confiança do cliente aparecia em discussões de pricing.

Engenheiros gostam de métricas mensuráveis. Confiança nem sempre é fácil de medir. Mas clientes sentem imediatamente. Uma fee que aparece inesperadamente. Uma regra de pricing que parece injusta. Um aumento súbito que o cliente não consegue explicar.

Essas coisas afetam comportamento. Nem sempre hoje. Às vezes meses depois.

Confiança se comporta como ativo de longo prazo. Receita se comporta como sinal de curto prazo. Bons sistemas de pricing precisam considerar os dois.

## Receita versus retenção

Um primo próximo do trade-off de confiança é retenção. Eles são relacionados, mas aparecem nos dados de forma diferente.

Confiança é sobre como o cliente se sente. Retenção é sobre se ele volta.

Uma mudança de pricing pode ganhar a compra e perder o cliente. A primeira transação parece saudável. O ticket médio sobe. O dashboard conta uma história limpa. Aí, seis meses depois, a coorte que passou pela mudança compra menos do que a coorte que não passou — e ninguém estava olhando para esse sinal quando a mudança subiu.

Receita acontece no momento da venda. Retenção acontece entre vendas. As duas métricas vivem em escalas de tempo completamente diferentes, o que torna fácil pesá-las de forma desigual. Receita curta ganha o holofote. Retenção longa paga a conta.

Bons sistemas de pricing aprendem a esperar — e a continuar medindo depois da vitória.

## Receita versus simplicidade

Conforme as capacidades de pricing evoluem, outro trade-off aparece.

Estratégias complexas frequentemente superam estratégias simples. Pelo menos na teoria. Um modelo mais sofisticado captura mais sinais, mais contexto, mais nuance.

Mas complexidade tem custos. Engenheiros conseguem explicar o resultado? Product managers entendem o raciocínio? Analistas conseguem validar o resultado? Stakeholders confiam na recomendação?

Às vezes uma solução um pouco pior mas compreensível gera mais valor do que uma solução melhor que ninguém entende.

## Cada objetivo produz uma resposta diferente

Um exercício que achei útil foi fazer a mesma pergunta com objetivos diferentes.

Suponha uma decisão de pricing. Dependendo do que estamos otimizando, a mesma situação pode produzir respostas bem diferentes:

| Objetivo | Resposta provável |
| --- | --- |
| Maximizar receita | Empurrar o preço para cima onde a curva tolera |
| Maximizar conversão | Segurar o preço, mesmo ao custo de margem |
| Maximizar valor de longo prazo do cliente | Sacrificar parte da receita curta para preservar confiança e retenção |

O preço em si não determina sucesso. O objetivo determina.

Times de pricing costumam gastar tempo demais discutindo números e tempo de menos discutindo objetivos.

## O trade-off escondido em todo experimento

Um padrão que eu via direto em experimentos de pricing: uma variante aumentava receita enquanto outra melhorava conversão.

A parte interessante nunca era o experimento. A parte interessante era a conversa depois.

*Qual resultado deveríamos preferir?*

Não existe resposta universalmente correta. A resposta depende do contexto. Uma empresa tentando crescer market share pode otimizar diferente de uma empresa tentando melhorar lucratividade. Um produto novo pode otimizar diferente de um produto maduro. O mesmo experimento pode produzir decisões diferentes dependendo do objetivo de negócio.

Experimentos revelam trade-offs. Eles não os removem.

## Otimização local versus otimização global

Outra lição demorou mais para entrar.

Melhorar uma parte do sistema não necessariamente melhora o sistema inteiro.

Imagine um segmento de cliente que tolera preços mais altos. Otimizar aquele segmento pode aumentar receita. Mas e se a mudança afeta a percepção do cliente em outro lugar? E se cria complexidade operacional? E se torna experimentação futura mais difícil?

Melhorias locais podem criar custos globais. Decisões de pricing existem dentro de sistemas maiores. A melhor decisão para uma métrica nem sempre é a melhor decisão para o negócio.

## Restrições não são limitações

Engenheiros costumam tratar restrições como obstáculos.

Pricing me ensinou a vê-las de outra forma. Restrições são o que torna otimização significativa.

Sem restrições, a resposta normalmente é trivial:

> Maximizar receita → subir preços.

Restrições forçam perguntas melhores:

> Maximizar receita, mantendo conversão, protegendo confiança, permanecendo explicável, suportando experimentos futuros.

Agora o problema vira interessante.

As conversas de pricing mais valiosas das quais participei raramente eram sobre números. Eram sobre restrições.

## O que aprendi

A maior mudança no meu pensamento aconteceu quando parei de ver pricing como uma busca pelo valor correto.

Raramente existe um único valor correto. Existem trade-offs. Objetivos. Restrições. Resultados que competem.

Pricing não é a arte de achar o maior preço. É a disciplina de escolher quais trade-offs importam.

Essa percepção tornou a experimentação mais valiosa. Tornou a segmentação mais útil. E tornou o comportamento do cliente mais compreensível. Porque o propósito de todas essas capacidades nunca foi encontrar uma resposta. Era nos ajudar a tomar decisões melhores.

## Reflexão final

Se você entrava em uma discussão de pricing esperando sair com um número, normalmente saía decepcionado. O número era a parte fácil. A parte difícil era nomear as restrições que tornavam aquele número defensável.

Se você está olhando para uma decisão de pricing hoje e se sentindo puxado para o número maior, a pergunta que vale a pena fazer não é *"esse preço está certo?"*. É *"o que eu estou disposto a sacrificar para chamar de certo?"*

O número é o output. O trade-off é a decisão.
