---
title: "O Que Eu Construiria Diferente Hoje"
subtitle: "Os melhores sistemas de pricing não são os mais sofisticados. São os que o time consegue entender, testar, explicar, e mudar com segurança."
author: helio
layout: post
date: 2026-05-20T10:00:00+00:00
series:
  - pricing-engineering
series_order: 14
categories:
  - Engineering
  - Pricing
  - Architecture
tags:
  - pricing
  - rule-engine
  - architecture
  - retrospective
  - lessons-learned
description: "A passada de fechamento da série. Se eu fosse começar uma plataforma de pricing hoje, com o benefício de tudo que a primeira vez me ensinou, é esse o formato que eu construiria — e a ordem em que construiria."
---

Esse é o post pro qual a série tava se preparando. Treze posts de arquitetura, lição, erro, e a higiene manual que a gente segurou na mão. A pergunta que quero responder aqui é a menor: se eu fosse começar uma plataforma de pricing hoje, sabendo o que sei agora, o que construiria, e em que ordem?

A resposta comprime a maior parte do que veio antes. Tem pouca novidade nesse post — a maior parte é o inverso dos erros do último post, e as costuras arquiteturais dos posts antes daquele. O que é novo é a *sequência*. A lição da série não são só os componentes; é a ordem em que os componentes entram.

## O formato num frame só

Antes da sequência, o destino. A plataforma de pricing que eu construiria hoje tem seis componentes que sustentam a carga:

1. Um **modelo Rule tipado** que é o contrato entre intenção autoral e execução em runtime.
2. Uma **rule store em disco** com schema versionado, loader que é a fronteira, e reload fail-closed.
3. Um **rule engine** com política de matching explícita, evaluator, executor, e composer. Um por preocupação; interface nomeada.
4. Uma **explicação por Execute** que carrega o bastante pro engenheiro, operador, dono de produto e auditor num artefato só.
5. Um **caminho shadow** que roda candidato ao lado do ativo em tráfego real, assíncrono, com pipeline de divergência.
6. Um **gerador de tráfego sintético** que produz fixture reproduzível a partir de cenário escrito pelo time.

Quando a plataforma é pedida pra crescer, mais dois componentes entram:

7. Uma **simulação por replay** que casa snapshot e fixture num diff determinístico.
8. Um **decision engine** acima do rule engine que coordena regra com modelo, restrição e experimento.

Os seis primeiros existem na plataforma desde o primeiro mês. Os dois últimos chegam quando o rule engine começa a ser pedido pra fazer coisa que não devia ser pedido pra fazer, não antes.

Em volta de tudo, a disciplina de *operabilidade* do Post 12 — owner, data de revisão, procedimento de aposentadoria, dashboard que envelhece — tem que ser desenhada desde o começo, mesmo que boa parte da implementação seja manual no começo.

## A ordem em que eu construiria

A arquitetura é o *o quê*. A sequência é o *quando*. A sequência é onde eu mais mudaria.

**Semana um: o modelo Rule.** Antes de qualquer matcher, escreve o struct Rule do Post 2 e passa por três revisores. Faz o modelo carregar o que toda camada posterior vai precisar — Name, Description, Tags, Condition, Action, Priority, Enabled — e *nada mais*. Metadado vai num sidecar. O struct é o contrato; toda outra promessa do sistema vai depender desse aqui estar certo.

**Semana dois: o loader.** Schema YAML versionado desde a linha um. Loader que valida, falha fechado, troca atomicamente. O loader não tem que fazer tudo desde o dia um — ferramenta de migração versionada vem depois — mas o *formato* do loader tem que estar certo, porque o loader é a fronteira.

**Semana três: o engine, um matcher.** Escolhe a política de matching de propósito, sabendo se as regras são independentes ou em camadas. Pra maioria das superfícies de pricing, é o padrão indexed first-match-by-priority do Post 4. O engine sobe com um matcher, um composer, e um resultado tipado. O pipeline do Post 5 é explícito — recebe, casa, avalia, executa, compõe — mesmo que cada estágio seja uma linha só.

**Semana quatro: a explicação.** Todo Execute produz uma Explanation. A primeira versão é pequena — snapshot ID, nome das regras que dispararam, resultado, latência por estágio — mas tem o schema em que a versão completa vai crescer. Desse momento em diante, toda escalada tem um artefato pra puxar.

**Semana cinco: tráfego sintético.** Antes de ter tráfego de produção pra carregar contra, a plataforma tem um arquivo de cenário, uma seed, e um gerador que produz fixture. O fixture é o input que a suíte de teste usa. O fixture é também o que a próxima camada — shadow — e a depois — replay — vão consumir.

**Semana seis: shadow mode.** O engine candidato roda ao lado do ativo no tráfego sintético primeiro, num sample de tráfego real depois. O log de comparação existe a partir dessa semana. O pipeline de divergência é pequeno mas real. Toda mudança de regra a partir desse ponto passa pelo shadow antes de ir pra live.

Essas seis semanas são a plataforma de pricing mínima viável que eu construiria. Nada do trabalho é heroico. Tudo ali se justifica.

Depois da semana seis, os próximos investimentos são *guiados pela demanda*. A maior parte do tempo, a plataforma fica nesse formato por bastante tempo. Em algum momento, tem que crescer.

**Quando o rule engine entorta, replay.** A primeira vez que o time discorda se uma mudança candidata é segura, constrói o runner de replay do Post 10. O trabalho de snapshot tá no `bre-go`; o trabalho de fixture tá no `traffic-gen`; o runner que casa os dois é a peça que ninguém escreveu ainda. O diff do replay é o que encerra a próxima discordância.

**Quando as regras não conseguem mais expressar a decisão, o decision engine.** A primeira vez que você encontra regra que consulta serviço externo na ação, ou regra cuja priority codifica restrição, ou regra cuja condição codifica pertencimento a experimento, você tem o sinal. Envolve o rule engine. Extrai restrição pra própria camada. Costura de modelo e experimento vem depois.

**Quando a higiene manual de ciclo de vida começa a escapar, automação.** O dia em que alguém que não rodou a revisão trimestral original tem que rodar a próxima é o dia em que a planilha para de bastar. O padrão de automação do Post 12 — warning de `review_after`, relatório de zero-fire, diretório de owner, scheduler de aposentadoria — é o que leva a prática pra dentro do sistema.

## As escolhas que eu não faria

O mesmo formato inverte nas escolhas a evitar.

Não construiria o matcher antes do modelo Rule estar definido. O matcher é downstream do modelo em tudo que importa; acertar o modelo primeiro torna o matcher pior.

Não escolheria política de matching por default. As quatro políticas do Post 4 são apostas diferentes sobre como as regras interagem; o default errado é mais caro do que o trabalho ligeiramente mais pesado de escolher de propósito.

Não postergaria a explicação. Todo dia sem explicação é um dia em que a próxima escalada custa um dia e meio. O custo de embutir é um struct e um listener; o custo de não ter é ilimitado.

Não testaria o estado interno do matcher. Teste de contagem de bucket, distribuição de hash, e ordem de avaliação é teste contra implementação do engine, não contra comportamento. A suíte de 11 000 linhas do Post 6 é o conto de advertência.

Não confiaria em tráfego de produção pra testar o futuro. O mix de ontem é a pergunta de ontem. A plataforma tem que ser exercitada contra as perguntas que ainda não fizeram ao time, e é pra isso que cenário serve.

Não construiria o decision engine antes do rule engine ter sido operado. Decision engine prematuro é imposto que todo time que toca o sistema paga, e os padrões que o time acaba precisando não são os padrões que o arquiteto chutou de antemão.

Não assumiria que engenheiros são os únicos usuários. A rule store é pro dono de produto que precisa editar markup, pro auditor que precisa ler regra, pro operador que precisa entender decisão. Ergonomia de engenharia vem depois.

Não otimizaria pra criação e ignoraria aposentadoria. Toda regra que entra tem que ter um jeito de sair. O procedimento de aposentadoria existe antes da regra que precisa aposentar chegar.

## Os dois repos de referência, de novo

O código Go dessa série mora em [`bre-go`](https://github.com/helmedeiros/bre-go) e [`traffic-gen`](https://github.com/helmedeiros/traffic-gen). Os dois são extratos open-source de padrões que tive que aprender num sistema de pricing em produção cujo código eu não posso mostrar. O formato do contrato mapeia entre stacks; o que tá nesses repos é a *forma* da lição, não a *substância* do sistema de produção que ensinou.

Se eu fosse começar hoje, os dois repos abertos seriam uma das primeiras decisões de que eu não me arrependeria. Ter um lugar pra escrever o desenho numa linguagem e formato que qualquer pessoa consegue ler é o que tornou os padrões sobrevivíveis entre trocas de contexto — incluindo essa série em si. O sistema do trabalho não podia ser compartilhado. O sistema no aberto podia. A lição vive nos dois.

## A compressão

Se eu tivesse que comprimir a série inteira num parágrafo, seria esse.

Plataforma de pricing não é rule engine; é o sistema de componentes em volta do rule engine — loader, explicação, shadow, geração de tráfego, replay, decision engine, ciclo de vida. O rule engine é o centro do desenho e a menor parte do trabalho. Os erros mais caros são sobre qual componente você constrói primeiro, qual usuário você constrói pra, e qual disciplina você posterga porque não parece urgente. Os melhores sistemas de pricing não são os mais sofisticados. São os que o time consegue entender, testar, explicar e mudar com segurança. O resto é implementação.

## Pra que essa série serviu

A série anterior de pricing — [Lições de uma Plataforma de Pricing](/pt/series/lessons-from-a-pricing-platform/) — era sobre o trabalho de estratégia, produto e time por trás das decisões de pricing. Essa foi sobre o trabalho de engenharia embaixo. As duas são irmãs. Cada uma sozinha é incompleta; as duas juntas são o formato do que pricing de fato exige.

Se você leu as duas, leu boa parte do que sei escrever sobre pricing. Se construir uma plataforma de pricing depois de ler, não vai evitar todo erro do Post 13 — esses são o custo de fazer o trabalho — mas vai reconhecer os que tá pra cometer, e vai ter um lugar pra consultar o que fazer quando acontecerem.

É o máximo que uma série de posts consegue fazer. Não pode cometer os erros por você; só consegue nomear antes do tempo. A plataforma que você construir vai ser a sua. A esperança é que algumas costuras dela segurem porque a costura de outra pessoa não segurou, e você leu sobre antes de ter que viver.

## A lição

Os melhores sistemas de pricing são os que o time consegue entender, testar, explicar e mudar com segurança. Toda decisão arquitetural dessa série foi, no fim, uma decisão a serviço de um desses quatro verbos. O struct Rule é o que torna o sistema *compreensível*. A suíte de teste comportamental é o que torna *testável*. A explicação é o que torna *explicável*. A disciplina de shadow, replay e ciclo de vida é o que torna *mudável com segurança*.

Construa pros quatro verbos primeiro. Tudo o mais é engenharia. Na primeira vez que você shippa uma plataforma de pricing vai errar alguns deles; na segunda, com o benefício da primeira, vai acertar mais. Na terceira talvez acerte a maioria e descubra que o *quinto* verbo — o que essa série não cobriu — é a próxima coisa pra aprender.

Eu ainda não sei qual é o quinto verbo. Quando souber, vai ter outra série. Por enquanto, os quatro são os que consigo nomear com confiança, e os sete componentes acima são o formato que eu construiria pra honrá-los.

A série termina aqui. O trabalho, claro, não.
