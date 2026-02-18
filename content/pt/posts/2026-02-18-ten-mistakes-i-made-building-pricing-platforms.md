---
title: "Dez Erros que Cometi Construindo Plataformas de Pricing"
subtitle: "Os erros caros nunca são sobre sintaxe. São sobre fronteira, comportamento e ownership — as partes que parecem bem até deixarem de parecer."
author: helio
layout: post
date: 2026-02-18T10:00:00+00:00
series:
  - pricing-engineering
series_order: 13
categories:
  - Engineering
  - Pricing
  - Architecture
tags:
  - pricing
  - retrospective
  - architecture
  - lessons-learned
  - rule-engine
description: "Uma retrospectiva pessoal. Dez coisas que errei construindo plataforma de pricing, o que cada uma custou, e o que faria diferente. O erro raramente é sobre sintaxe — é sobre qual problema você decide resolver primeiro."
---

A primeira vez que alguém me perguntou o que eu tinha aprendido construindo plataforma de pricing, dei uma lista de técnicas. Um ano depois percebi que as técnicas não eram a lição. A lição eram os *erros* dos quais as técnicas saíram, e os erros raramente eram sobre código. Eram sobre qual problema eu tinha decidido resolver primeiro, qual camada tinha tratado como fixa quando deveria ter sido flexível, e qual usuário eu tinha desenhado em silêncio à custa dos outros.

Esse post é dez desses erros. Alguns shippei mais de uma vez. Alguns ainda cometo, às vezes, nos cantos em que ainda não aprendi a reconhecer.

## 1. Comecei pelo engine em vez do modelo de regra

A primeira versão do meu primeiro rule engine tinha um matcher belamente desenhado e nenhum tipo Rule de verdade. A Rule era um `map[string]interface{}` porque era o formato de que o matcher precisava; todo o resto era *trabalho futuro*. Escrevi o matcher primeiro porque o matcher parecia a parte difícil.

O matcher não era a parte difícil. O tipo Rule era a parte difícil. Sem Rule tipada, o loader não conseguia validar. Os testes não conseguiam asserir nada além do que o matcher já sabia. A explicação não conseguia nomear os campos. O engine inteiro era uma função em torno de um dicionário sem formato, e toda camada que queria adicionar estrutura tinha que re-derivar das chaves que por acaso encontrasse.

A gente reconstruiu o tipo Rule seis meses depois. O matcher mal mudou; tudo em volta mudou. Se fosse começar agora, escreveria o struct Rule no dia um e não escreveria matcher até o struct sobreviver a uma semana de code review.

## 2. Tratei matching como simples

O primeiro matcher que shippei foi o óbvio: caminha o rule set em ordem de inserção, avalia cada condição, coleta cada match. Funcionou em 50 regras. Funcionou em 200. Engatinhou em 800 — quando o rule set já tinha um ano e re-arquitetar era doloroso.

O erro não foi o matcher linear. O erro foi *tratar matching como default* em vez de escolha deliberada de desenho. Eu não tinha perguntado se as regras eram independentes ou em camadas, se as ações compunham ou colidiam, se a ordem codificava precedência ou acidente. O matcher que escolhi não respondia nenhuma dessas perguntas porque eu não tinha feito as perguntas.

A reescrita de sexta à noite não foi o custo. O custo foi que, quando reescrevemos, dois anos de arquivo de regra codificavam suposição sobre ordem de avaliação que ninguém tinha documentado. Metade do trabalho de migração foi escavar qual regra dependia de semântica de ordem de inserção que não sabia que dependia.

## 3. Esqueci da explicabilidade

A primeira pergunta "por que esse cliente foi cobrado?" levou um dia e meio pra responder. Tínhamos log, mas o log dizia `engine.Execute completed` com um resultado e nenhum detalhe. Tínhamos o rule set, mas nenhuma ideia de quais regras tinham disparado. Tínhamos a request do cliente, mas precisávamos reconstruir o estado do engine do histórico do `git` porque não tínhamos carimbado o snapshot.

Aquele dia e meio me ensinou que explicabilidade não é apoio de debug. É o contrato do sistema com o operador, com o auditor, com o dono de produto e com o engenheiro. Eu tinha construído o engine pra um único usuário — o engenheiro — e não percebido que o sistema tinha quatro, e que o engenheiro era o que precisava *menos* de explicabilidade porque conseguia ler o source.

Todo engine de pricing que construí desde então produz uma explicação por Execute, sampleada ou completa, guardada ou reproduzível. O custo de explicabilidade é um struct e um listener. O custo de não ter é toda escalada levando um dia e meio.

## 4. Deixei priority virar governança escondida

Quando o campo priority foi proposto, alguém perguntou que números usar. Eu disse "qualquer inteiro; o que parecer certo". Dois anos depois o campo priority parecia o chão de um bar perto do fechamento. Algumas regras estavam em 1000 porque eram "muito importantes". Algumas em 999 porque eram "quase tão importantes quanto compliance". Algumas em 437 porque alguém tinha pensado dez minutos e produzido um número.

O erro foi tratar priority como *valor* em vez de *artefato de governança*. Priority não é aritmética; é política. O inteiro é a superfície; a política é em qual tier a regra mora, qual time é dono do tier, o que conflito significa quando acontece dentro do tier. Sem uma escada explícita de tier nomeada, toda decisão de priority era negociação, e a negociação ia pra quem gritava mais alto.

O fix foi uma escada de quatro tier — compliance, receita, experimento, default — com regra colocada de propósito. O fix foi fácil. A lição foi mais difícil: qualquer número que acaba virando política precisa ser governado como política, por mais inocente que pareça na entrada.

## 5. Testei implementação em vez de comportamento

A suíte de teste de 11 000 linhas do Post 6 era real. Passou por quatorze meses enquanto o engine silenciosamente produzia markup errado. A maior parte daquelas 11 000 linhas testava o estado interno do matcher: contagem de bucket, distribuição de hash, a ordem em que condições eram avaliadas. Poucas testavam *quanto o cliente foi cobrado*.

Quando refatoramos o matcher indexed, todo teste quebrou. Nada da quebra correspondia a mudança de comportamento. O cliente continuava sendo cobrado o mesmo número; o matcher só chegava lá por uma estrutura de bucket diferente. Gastamos seis semanas atualizando teste que testava a coisa errada — e nessas seis semanas, uma mudança real de comportamento passou despercebida porque o teste que precisávamos nunca tinha sido escrito.

A lição, numa frase: teste que quebra quando você refatora mas o comportamento não muda é teste que não devia ter sido escrito. Teste que passa quando você refatora mas o comportamento regride em silêncio é bug na suíte.

## 6. Confiei no tráfego médio

O primeiro teste de carga que rodei num pricing engine novo usou quatro milhões de requests do log de produção. O plano era replayar ontem e confirmar que o engine aguentava. O plano funcionou. O engine aguentou. A gente shippou. Dois dias depois um único mercado spikou tráfego em 8x por causa de feriado, e o engine caiu.

O replay tinha carregado o mix de ontem. O mix de ontem não tinha tido spike de feriado. Eu tinha testado o engine numa pergunta que já tinha respondido e não na que precisava responder.

O fix foi tráfego sintético com cenário explícito pros casos com que eu me preocupava. A lição é mais geral: tráfego de produção é a distribuição *de ontem*. É o default errado pra testar amanhã. Tráfego sintético, com as hipóteses do time sobre amanhã codificadas como cenário, é o default certo. Tráfego de produção é teste de regressão pra comportamento passado, não teste de estresse pra formato futuro.

## 7. Ignorei regra parada

Eu sabia que tinha regra que ninguém conseguia explicar. Vinham disparando há anos. Não estavam causando problema. Deixei em paz porque "funcionavam", e eu tinha trabalho real pra fazer.

Seis meses depois uma daquelas regras interagiu com uma regra nova que shippamos — as condições sobrepuseram, as ações empilharam, e o resultado foi um overcharge de 0,5% de markup numa fatia de cliente que a gente não tinha se preocupado em considerar porque a regra velha tinha ficado silenciosa sobre eles por dois anos. O postmortem recomendou um "procedimento de aposentadoria". O procedimento de aposentadoria não existia. Passou a existir só por causa do postmortem.

A lição é em duas partes. A primeira: regra que ninguém entende é dívida que acumula; ignorar é pagar juros. A segunda: um *procedimento* de aposentar regra tem que existir antes da regra que você quer aposentar chegar, porque no momento em que você precisa, não tem tempo de desenhar.

## 8. Fiz simulação tarde demais

Shadow mode foi a terceira coisa que construí. A primeira foi o engine, a segunda foi o loader de regra, a terceira — finalmente — foi shadow mode. Quando chegou, vínhamos shippando mudança de regra por dezoito meses por intuição, observação, e um pouquinho de oração. Várias dessas mudanças shipparam comportamento que não tínhamos pretendido.

Tenho querido shadow mode desde a semana um de toda plataforma de pricing em que trabalhei desde então. A lição não é que shadow mode é difícil; é que *o caso de shadow mode é invisível até você ter vivido sem*. Até a primeira rollout surpresa, shadow mode parece overhead de infra. Depois da primeira rollout surpresa, parece a coisa que você devia ter construído primeiro.

Eu não construiria plataforma de pricing hoje sem shadow como componente de semana um. Mesmo uma versão crua — loga o ativo e o candidato lado a lado, compara offline — se paga na primeira vez que o candidato tá errado de um jeito que ninguém previu.

## 9. Construí demais antes de aprender

O erro oposto. Num projeto que veio logo depois de um incidente difícil, desenhei o decision engine antecipado — contexto, integração de modelo, camada de restrição, overlay de experimento, o formato inteiro do Post 11. Construí antes do rule engine embaixo ter sido operado por seis meses.

O decision engine ficou sem uso na maior parte do primeiro ano. Os padrões que tinha colocado não casavam com os padrões em que o rule engine de fato cresceu. Quando o time finalmente precisou de capacidade de decision engine, metade das minhas decisões antecipadas estavam erradas e a outra metade nos custava nada porque a gente não usava.

A lição é timing. Constrói a camada que tá *entortando*, não a que pode entortar no futuro. Plataforma de pricing que precisa de decision engine se revela; você não tem que adivinhar. Plataforma de pricing que ainda não precisa não se beneficia de ter um, e o custo arquitetural de carregar é pago todo dia.

## 10. Assumi que engenheiros eram os únicos usuários

A rule store era um arquivo YAML num repo `git`. O schema era documentado vagamente. As mensagens de erro assumiam familiaridade com o source do loader. Os dashboards eram construídos pro engenheiro de on-call. Nada disso era irracional — engenheiros tinham construído o sistema, engenheiros tavam operando, engenheiros eram os usuários que eu tinha em mente.

Aí produto quis editar um markup. Marketing quis lançar um experimento. Compliance quis ler uma regra antes de assinar. Nenhum deles conseguia. Toda edição de regra rotava por engenharia, enfileirando toda mudança, atrasando toda decisão, e centralizando autoridade no time que não a queria. O sistema tinha sido construído pra um usuário — o engenheiro — e o engenheiro era, surpreendentemente, o usuário que *menos* precisava.

O fix levou trimestres. O fix foi tornar a regra o artefato, não o arquivo: UI pra editar, API pra ler, audit log pra revisar, mensagem de erro que nomeasse *o que tava errado na regra* e não *qual linha do loader falhou*. A lição, e eu sigo encontrando cantos novos dela, é que a audiência do artefato é mais larga do que o time que constrói. Desenhar pra essa audiência mais larga primeiro é o que torna o papel do time sustentável depois.

## O formato por baixo dos erros

Dez erros é lista. O formato por baixo da lista é mais curto:

Eu construí pro usuário errado. Construí antes de aprender. Tratei *default* como decisão. Tratei *decisão* como default. Deixei governança morar em campo que o sistema não policiava. Otimizei pra criação e ignorei aposentadoria. Testei o que era fácil e não o que importava. Confiei no que tinha visto e não me preparei pro que ainda não tinha.

Vários desses são erros que os posts arquiteturais dessa série vêm tentando ensinar a contornar — e os mais úteis de escrever são os que a série ainda não cobriu direto. O struct Rule estreito, a política de matching explícita, o desenho com explicação primeiro, a escada de priority, a suíte de teste comportamental, o tráfego sintético, o procedimento de aposentadoria, o rollout shadow-first, a regra de construir-quando-entortando, o artefato pro não-engenheiro: cada um é o antídoto pra um dos erros acima, e cada um é hábito que sigo tendo que renovar porque o erro segue querendo voltar.

## Uma nota sobre o que seria o décimo primeiro

A lista honesta de erros nunca termina em dez. O décimo primeiro, na minha lista, é um que ainda venho vivendo e ainda não aprendi a nomear bem: assumir que o incidente passado é o próximo incidente. Todo postmortem que escrevi apertou o sistema contra o modo de falha que tinha acabado de acontecer. A próxima falha em geral era diferente. As defesas se acumularam — explicação, replay, shadow, higiene de ciclo de vida — mas o ciclo de "incidente, endurece, surpresa, incidente" não parou.

Ainda não sei o que fazer com isso. Acho que parte da resposta tá no balanço, no postmortem, entre *defesa profunda* (contra o tipo de falha que acabou de acontecer) e *cobertura larga* (contra o tipo que ainda não). Eu vinha inclinando pesado pra profundidade na carreira. Tô tentando inclinar mais pra largura nas plataformas que tô construindo agora.

## O que vem a seguir

O post final dessa série é a passada de fechamento — o que eu construiria diferente hoje, com o benefício completo desses dez erros e dos posts arquiteturais que vieram antes. É o post mais curto da série porque, a essa altura, boa parte da resposta é compressão.

O que quero dizer antes daquele post: os erros acima são o custo de construir uma plataforma de pricing de verdade. Alguns são inevitáveis; alguns são sinal de que as pessoas fazendo o trabalho não fizeram antes. Os dois tipos são valiosos. O time que pagou esses erros é o que consegue construir a próxima plataforma de pricing mais rápido — não porque vai evitar os erros, mas porque vai reconhecê-los antes.

## A lição

Os erros raramente são sobre sintaxe. São sobre qual problema você decide resolver primeiro, qual camada você trata como fixa quando deveria ser flexível, qual usuário você desenha em silêncio, e qual disciplina você posterga porque não parece urgente. As correções, quando chegam, em geral são estruturais: o tipo que devia ter sido mais estreito, o matcher que devia ter sido escolhido de propósito, a explicação que devia ter sido output de primeira classe, o procedimento de aposentadoria que devia ter existido antes de você precisar.

Shippei a maior parte desses erros mais de uma vez. Os caros shippei recentemente; os baratos agora identifico na primeira revisão de design. A coisa mais útil que consigo fazer por alguém que tá construindo plataforma de pricing é nomear esses erros abertamente, pra que quando essa pessoa encontre o mesmo padrão, reconheça como padrão e não como problema único do sistema dela.

O próximo post é a forma positiva: não os erros, mas o build que eu tentaria se começasse hoje com o que sei agora. A maior parte do que faria diferente tá nos negativos acima. O formato positivo é o que sai quando você bota os negativos em série.
