---
title: "O Ciclo de Vida de uma Regra de Pricing"
categories:
  - Engineering
  - Governance
  - Pricing
  - Product
date: 2026-06-07
tags:
  - pricing
  - rule-engine
  - governanca
  - experimentacao
  - platform-engineering
  - product-management
series:
  - lessons-from-a-pricing-platform
series_order: 13
description: "O que o meu time teve que aprender sobre regra de pricing depois que ela entra no ar — ownership, expiração, deleção e governança como respondibilidade."
subtitle: "Uma plataforma de pricing não é uma coleção de regras. É a memória institucional de cada decisão em que o negócio apostou ou da qual recuou."
---

Uma revisão de pricing, quarta-feira de tarde. Alguém apontou pro dashboard e perguntou por que o markup pra um produto específico na Alemanha era 3,7%. Não 3, não 4. Especificamente 3,7.

A sala ficou quieta.

A regra estava no ar havia quase dois anos. Aplicava em um pedaço importante das compras naquele mercado. Ninguém na sala tinha introduzido. O ticket original linkado no commit estava arquivado. A thread do Slack referenciada no ticket não existia mais, porque alguém tinha podado canais antigos. O product manager que tinha sido dono do experimento que produziu a regra tinha mudado de time. A analista que tinha medido tinha saído da empresa.

A regra continuava rodando. Continuava mexendo em dinheiro de verdade. E ninguém naquela reunião conseguia explicar por quê.

Voltei pro registro de regras naquela semana e rodei uma contagem. A gente tinha um pouco mais de seiscentas regras em produção. Perguntei pro time quantas dessas a gente conseguia explicar com confiança — origem, dono, propósito atual, última revisão. O número honesto ficava lá pelos trezentos e poucos. O resto, simplesmente, tava ali.

Esse foi o dia em que o meu time caiu na real do problema. A gente tinha passado anos construindo uma plataforma de pricing — um Business Rules Engine, uma infraestrutura de experimentação, trabalho em segmentação, simuladores pra avaliar mudança antes do cliente ver. Cada um desses pedaços tinha respondido uma pergunta real na hora. Nenhum deles tratava do que acontece com a regra depois que ela entra no ar.

## A gente tinha tratado ownership como pergunta de criação

Não era falta de cuidado. A gente tinha ownership. O processo de PR da plataforma exigia reviewer em toda regra. O registro interno carregava quem tinha introduzido cada regra, quando ela tinha entrado, de qual experimento tinha vindo. A gente rodava esse processo com disciplina havia anos.

E não tinha ajudado.

O motivo ficou óbvio na hora que a gente nomeou. Toda peça de ownership que a gente tinha construído estava amarrada em *criação*. Quem pode adicionar uma regra. Quem revisa a adição. Quem assina o experimento que produz ela. Nada disso passava do momento em que a regra entrava no ar. Depois disso, a regra era da plataforma — ou seja, de ninguém específico.

Era essa a lacuna. Ownership era pergunta de criação pra gente. Tinha que virar pergunta de ciclo de vida.

{{< plantuml title="O ciclo de vida de uma regra, do jeito que a gente teve que modelar" >}}
@startuml
skinparam shadowing false
state "Criada" as C
state "Rodando em produção" as R
state "Em revisão" as Rev
state "Aposentada" as Ret

[*] --> C : Observação → Hipótese
C --> R : Deploy
R --> Rev : Expiração / sinal / evento
Rev --> R : Manter ou mudar
Rev --> Ret : Aposentar
Ret --> [*]
@enduml
{{< /plantuml >}}

O diagrama parece óbvio agora. Na época, o lado direito dele — *Em revisão*, *Aposentada* — era a parte que não existia como conceito de primeira classe na plataforma. A gente tinha Criada. Tinha Rodando. O resto a gente deixava na conta da boa intenção.

## Iteração 1: data de expiração

A intervenção mais barata que dava pra tentar era uma data de expiração.

A gente mudou o registro pra que toda regra nova exigisse um `expires_at`. De uma semana a um ano, dependendo pra que a regra existia. Quando a data chegava, a regra não se autodeletava — isso teria sido frágil demais pra código que mexe com receita — mas ela acendia no dashboard, e o dono recebia uma notificação perguntando se era pra manter, mudar ou aposentar.

Só isso aposentou dezenas de regras no primeiro trimestre. A maioria era experimento que tinha graduado em código permanente sem ninguém ter decidido que devia. Algumas eram overrides específicos de mercado cujos mercados, depois, tinham se unificado. Algumas eram patches de incidente que ninguém lembrava direito.

Mas a intervenção veio com um efeito de segundo nível que a gente não tinha previsto. Quando a expiração batia, o caminho de menor resistência era esticar — bumpar a data, deixar a regra rodando, seguir em frente. Alguns donos esticaram a mesma regra quatro ou cinco vezes seguidas, cada extensão carregando menos contexto que a anterior. O mecanismo forçador tava funcionando. A força não tava forte o bastante.

## Iteração 2: contar aposentadoria do lado da criação

A próxima iteração foi sobre o que a gente media.

Por dois anos, o dashboard da plataforma reportava quantas regras a gente entregava por trimestre. Era a métrica que o time e os stakeholders olhavam. A gente adicionou um número do lado dela: quantas regras a gente tinha aposentado no mesmo período. Foi mudança de uma coluna. Mudou algo em como a gente conduzia revisão de pricing.

Um trimestre em que a gente entregou doze regras e aposentou uma começou a parecer visivelmente diferente de um trimestre em que entregou oito e aposentou seis. O segundo era uma plataforma mais útil. A métrica finalmente dizia isso em voz alta.

A gente também adicionou uma linha no template de PR de criação de regra:

> *O que precisaria ser verdade pra a gente aposentar essa regra?*

Essa pergunta, feita no momento da criação, fez mais pela higiene de ciclo de vida do que qualquer processo que a gente construiu depois. Uma regra cuja pessoa autora não conseguia responder essa pergunta era uma regra que a gente já sabia que não ia conseguir aposentar depois.

## Iteração 3: governança como respondibilidade

A terceira iteração veio do onboarding.

Dois engenheiros novos entraram no time. A gente sentou eles na frente do registro e pediu pra passarem uma semana tentando entender vinte regras à escolha deles. Voltaram frustrados. O campo de dono dizia quem era responsável hoje, mas não por que a regra existia. O campo de métrica dizia o que a gente tinha dito que ia medir, mas não o que a gente de fato tinha observado. Era pra ter um comentário em algum canto, de dois anos atrás, que explicava a hipótese original. Não acharam.

Quando a gente viu a plataforma pelos olhos deles, a palavra *governança* finalmente significou alguma coisa concreta. Não era aprovação. Não era comitê. Era conseguir responder cinco perguntas sobre qualquer regra ainda rodando em produção:

- Por que essa regra existe?
- Quem é dono dela?
- Quando foi introduzida?
- Que resultado ela tava tentando criar?
- Ela ainda tá funcionando?

Um time que não consegue responder essas perguntas não tem governança. Tem história. Os dois parecem iguais de fora. Se separam rápido no momento em que algo dá errado.

A gente não formalizou governança com processo. Exigiu que essas cinco respostas existissem — em linguagem clara, no registro, do lado da própria regra — pra toda regra nova. Regra velha ganhava o mesmo tratamento sempre que alguém encostava nela. Em um ano, dava pra ler uma regra e saber não só o que ela fazia, mas por que a gente tinha topado fazer.

## O ciclo de vida se moveu com a plataforma

A lição não ficou direitinho dentro da camada de regras. Quando a gente adicionou modelo um ano depois, o mesmo problema apareceu uma camada acima. Modelo tem suposição. Suposição envelhece. O dado de treino tem data. A função objetivo reflete o que o negócio se importava na última vez que o modelo foi atualizado. Nada disso sobrevive sem intervenção.

Quando a gente adicionou simulador, a lição apareceu mais uma camada acima. Cenário de simulador fica velho. Os "edge cases que ninguém planejou" deixam de ser edge case quando o comportamento da plataforma muda. Cenário que não pega nada por dois trimestres já não é rede de segurança.

Tecnologia melhor não tinha removido o problema de ciclo de vida. Tinha movido. Regra precisa de revisão. Modelo precisa de retreino. Experimento precisa de conclusão. Simulador precisa de aposentadoria. Plataforma madura reconhece isso, em vez de fingir que o trabalho dá pra automatizar tudo embora.

## O que aprendi

A mudança mental, no fundo, não era sobre regra. Era sobre duração.

Por anos, o time pensava em mudança de pricing do jeito que se pensa em feature: adoção, lançamento, rampa, sucesso. *Duração* era implícita. Uma regra vivia até deixar de viver, e *deixar de viver* raramente acontecia de propósito.

Quando a gente começou a pensar em duração com a mesma seriedade que dava a adoção — colocando duração no registro, no template de PR, no dashboard, nas revisões — a plataforma parou de ficar mais pesada à medida que ficava mais inteligente. Essa mudança de postura, sozinha, importou mais do que qualquer uma das três iterações isoladamente.

## Reflexão final

Uma plataforma de pricing não é uma coleção de regras. É a memória institucional de cada decisão em que o negócio apostou ou da qual recuou. Sem intervenção, essa memória se desfia. As decisões ficam; os motivos vazam.

O trabalho técnico é manter essa memória honesta com o tempo — pra que o sistema lembre não só do que faz, mas de por que faz, e de quando esse motivo expirou.

Esse é, em boa parte, o trabalho que ninguém agenda. Acontece entre features, entre lançamentos, entre incidentes. Olhando pra trás, é o trabalho que eu mais queria ver um time que eu entrasse hoje já fazendo.
