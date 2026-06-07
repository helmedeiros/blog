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
description: "Por que a pergunta mais difícil em pricing não é o que cobrar — é o que a gente tá disposto a sacrificar?"
subtitle: "Pricing não é a arte de achar o maior preço. É a disciplina de escolher quais trade-offs importam."
---

Por alguns anos, trabalhei numa plataforma de pricing — a parte do sistema que decide o que cobrar de um cliente, e quando. Quando sentei pra escrever isso, a plataforma já tinha passado por várias mudanças de enquadramento. A gente tinha tirado regra do código pra um motor de regras de negócio. Tinha parado de subir mudança de pricing no escuro e começado a tratar como experimento. Tinha parado de fingir que "cliente médio" era um conceito útil. E tinha aprendido que grupo diferente de cliente respondia a preço ao longo de curva, não de ponto.

Por muito tempo, mesmo por baixo de tudo isso, eu ainda achava que pricing era problema de busca. Achar o preço certo. Aplicar. Medir o resultado. Seguir.

Cada lição arrancava um pedaço dessa crença. Regra de pricing era hipótese. Cliente não era média. Resposta formava curva. Em algum momento, surgiu uma percepção diferente.

A pergunta mais difícil em pricing não era *o que a gente deve cobrar?*

Era *o que a gente tá tentando otimizar?*

Essa pergunta mudou como eu pensava sobre pricing. Porque toda decisão de pricing é trade-off.

## A otimização fácil

Imagine que seu único objetivo é receita.

O problema parece direto. Subir preço. Ganhar mais por compra. Comemorar.

A realidade é menos cooperativa. Cliente reage. Demanda muda. Concorrente existe. Confiança importa.

O que parece problema de otimização vira rapidinho um malabarismo. O erro é supor que tem um número único esperando pra ser descoberto. Normalmente não tem. Tem vários resultados se movendo em direções diferentes.

## Receita versus conversão

Esse foi o primeiro trade-off com o qual a gente se deparou.

Preço mais alto costuma significar mais receita por transação. Ao mesmo tempo, pode reduzir conversão.

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

A pergunta difícil não é se a conversão cai. É se a receita adicional compensa essa queda.

E mesmo isso costuma ser simplista demais. Porque conversão raramente é a única coisa com a qual a gente se importa.

## Receita versus confiança

Uma lição que me surpreendeu foi com que frequência confiança do cliente aparecia em discussão de pricing.

Engenheiro gosta de métrica mensurável. Confiança nem sempre é fácil de medir. Mas cliente sente na hora. Uma fee que aparece do nada. Uma regra de pricing que parece injusta. Um aumento súbito que o cliente não consegue explicar.

Essas coisas afetam comportamento. Nem sempre hoje. Às vezes meses depois.

Confiança se comporta como ativo de longo prazo. Receita se comporta como sinal de curto prazo. Bom sistema de pricing precisa considerar os dois.

## Receita versus retenção

Um primo próximo do trade-off de confiança é retenção. São relacionados, mas aparecem nos dados de forma diferente.

Confiança é sobre como o cliente se sente. Retenção é sobre se ele volta.

Uma mudança de pricing pode ganhar a compra e perder o cliente. A primeira transação parece saudável. O ticket médio sobe. O dashboard conta uma história limpa. Aí, seis meses depois, a coorte que passou pela mudança compra menos do que a coorte que não passou — e ninguém estava olhando pra esse sinal quando a mudança subiu.

Receita acontece no momento da venda. Retenção acontece entre vendas. As duas métricas vivem em escalas de tempo completamente diferentes, o que torna fácil pesar uma mais do que a outra. Receita curta ganha o holofote. Retenção longa paga a conta.

Bom sistema de pricing aprende a esperar — e a continuar medindo depois da vitória.

## Receita versus simplicidade

À medida que as capacidades de pricing vão evoluindo, outro trade-off aparece.

Estratégia complexa costuma superar estratégia simples. Pelo menos na teoria. Um modelo mais sofisticado captura mais sinal, mais contexto, mais nuance.

Mas complexidade tem custo. Engenheiro consegue explicar o resultado? Product manager entende o raciocínio? Analista consegue validar o resultado? Stakeholder confia na recomendação?

Às vezes uma solução um pouco pior, mas compreensível, gera mais valor do que uma solução melhor que ninguém entende.

## Cada objetivo produz uma resposta diferente

Um exercício que achei útil foi fazer a mesma pergunta com objetivos diferentes.

Suponha uma decisão de pricing. Dependendo do que a gente tá otimizando, a mesma situação pode produzir respostas bem diferentes:

| Objetivo | Resposta provável |
| --- | --- |
| Maximizar receita | Empurrar o preço pra cima onde a curva tolera |
| Maximizar conversão | Segurar o preço, mesmo ao custo de margem |
| Maximizar valor de longo prazo do cliente | Sacrificar parte da receita curta pra preservar confiança e retenção |

O preço em si não determina sucesso. O objetivo determina.

Time de pricing costuma gastar tempo demais discutindo número e tempo de menos discutindo objetivo.

## O trade-off escondido em todo experimento

Um padrão que eu via direto em experimento de pricing: uma variante aumentava receita enquanto outra melhorava conversão.

A parte interessante nunca era o experimento. Era a conversa depois.

*Qual resultado a gente devia preferir?*

Não existe resposta universalmente correta. A resposta depende do contexto. Uma empresa tentando crescer market share pode otimizar diferente de uma empresa tentando melhorar lucratividade. Um produto novo pode otimizar diferente de um produto maduro. O mesmo experimento pode produzir decisões diferentes dependendo do objetivo de negócio.

Experimento revela trade-off. Não remove.

## Otimização local versus otimização global

Outra lição demorou mais pra entrar.

Melhorar uma parte do sistema não necessariamente melhora o sistema inteiro.

Imagine um segmento de cliente que tolera preço mais alto. Otimizar aquele segmento pode aumentar receita. Mas e se a mudança afeta a percepção do cliente em outro canto? E se cria complexidade operacional? E se deixa experimentação futura mais difícil?

Melhoria local pode criar custo global. Decisão de pricing vive dentro de sistema maior. A melhor decisão pra uma métrica nem sempre é a melhor decisão pro negócio.

## Restrição não é limitação

Engenheiro costuma tratar restrição como obstáculo.

Pricing me ensinou a ver de outra forma. Restrição é o que torna otimização significativa.

Sem restrição, a resposta normalmente é trivial:

> Maximizar receita → subir preço.

Restrição força pergunta melhor:

> Maximizar receita, mantendo conversão, protegendo confiança, permanecendo explicável, suportando experimento futuro.

Agora o problema fica interessante.

As conversas de pricing mais valiosas das quais participei raramente eram sobre número. Eram sobre restrição.

## O que aprendi

A maior mudança no meu pensamento aconteceu quando parei de ver pricing como busca pelo valor correto.

Raramente existe um valor correto único. Existem trade-offs. Objetivos. Restrições. Resultado competindo com resultado.

Pricing não é a arte de achar o maior preço. É a disciplina de escolher quais trade-offs importam.

Essa percepção tornou a experimentação mais valiosa. Tornou a segmentação mais útil. E tornou o comportamento do cliente mais compreensível. Porque o propósito de todas essas capacidades nunca foi achar uma resposta. Era ajudar a gente a tomar decisão melhor.

## Reflexão final

Se você entrava numa discussão de pricing esperando sair com um número, normalmente saía decepcionado. O número era a parte fácil. A parte difícil era nomear as restrições que tornavam aquele número defensável.

O que a gente acabou ficando melhor em, quando ficou melhor em trade-off de pricing, não era um modelo melhor nem uma opinião mais forte. Era prática. A gente tinha tomado o mesmo tipo de decisão vezes o suficiente pra conseguir discordar sobre ela sem levar pro lado pessoal. A gente tinha uma noção compartilhada de quais sacrifícios a empresa de fato topava aceitar, e quais ela só fingia.

Um trade-off que ninguém na sala consegue nomear não é decisão. É desejo.
