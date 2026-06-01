---
title: "Pricing É um Esporte Coletivo"
categories:
  - Engineering
  - Pricing
  - Product
date: 2023-08-24
tags:
  - pricing
  - product-management
  - analytics
  - engineering
  - experimentacao
  - monetizacao
description: "Por que decisões de pricing bem-sucedidas emergem de produto, analytics, engenharia e negócio trabalhando juntos — e não de uma única disciplina."
subtitle: "Pricing vive na interseção entre produto, analytics, engenharia e negócio."
---

Uma das maiores surpresas depois de entrar em um time de pricing não foi a complexidade das regras de pricing.

Foi descobrir quantas pessoas precisavam estar envolvidas para mudar uma única regra.

Antes de trabalhar com sistemas de pricing, eu supunha que a maior parte das mudanças de pricing era técnica. Um stakeholder de negócio identificaria uma oportunidade, um product manager priorizaria, engenheiros implementariam, e o sistema produziria um preço diferente.

A realidade era consideravelmente mais complicada.

Um único experimento de pricing podia exigir alinhamento entre stakeholders comerciais, analistas, product managers, engenheiros e times operacionais. Cada um via a mesma mudança por uma lente diferente. Cada um se importava com riscos diferentes. Cada um media sucesso de forma diferente.

Quanto mais tempo eu passava em pricing, mais eu percebia que sistemas de pricing bem-sucedidos não são construídos por disciplinas isoladas.

Eles são construídos por colaboração.

## A armadilha do engenheiro

Um dos primeiros erros que cometi foi tratar pricing como um problema técnico.

Meu modelo mental se parecia com isto:

{{< plantuml title="Como eu achava que uma mudança de pricing acontecia" >}}
@startuml
skinparam shadowing false
start
:Mudança de pricing;
:Nova regra;
:Deploy;
:Nova receita;
stop
@enduml
{{< /plantuml >}}

O processo real se parecia mais com isto:

{{< plantuml title="Como uma mudança de pricing realmente acontece" >}}
@startuml
skinparam shadowing false
start
:Oportunidade de negócio;
:Análise de impacto no cliente;
:Hipótese de pricing;
:Estratégia de medição;
:Desenho técnico;
:Rollout seguro;
:Resultados do experimento;
:Decisão de negócio;
stop
@enduml
{{< /plantuml >}}

A diferença entre esses dois fluxos é onde a maior parte da complexidade de pricing realmente vive.

Não está no motor de regras. Está nas conversas que precisam acontecer antes de alguém tocar no motor de regras.

## O que o product manager traz

Os melhores product managers com quem trabalhei nunca começavam por uma porcentagem.

Começavam por um problema.

Em vez de perguntar *"devemos aumentar este markup em 2%?"*, perguntavam *"que comportamento do cliente queremos influenciar?"* — ou *"que resultado de negócio queremos atingir?"*

Essa distinção importa. Decisões de pricing devem emergir de hipóteses, não de números arbitrários.

| Responsabilidade de produto | Por que importa |
| --- | --- |
| Definir o problema do cliente | Evita mudanças aleatórias de pricing |
| Construir hipóteses | Cria expectativas mensuráveis |
| Priorizar oportunidades | Foca o esforço de engenharia |
| Alinhar stakeholders | Cria entendimento compartilhado |

A contribuição real do PM não é a priorização. É o enquadramento que faz o resto do time concordar com o que "sucesso" significa antes de alguém escrever código.

## O que o analista traz

Se product managers definem hipóteses, analistas definem confiança.

Uma lição que aprendi rápido é que mudanças de pricing sem medição não são experimentos. São apenas mudanças em produção com passos a mais.

Todo experimento de pricing precisa de respostas honestas para perguntas como estas:

- Qual métrica estamos otimizando?
- Quais guardrails protegem a experiência do cliente?
- Por quanto tempo o experimento deve rodar?
- Qual o tamanho mínimo da amostra?
- Como "sucesso" se parece de fato?

Sem essas respostas, times confundem ruído com aprendizado com facilidade. Sistemas de pricing geram uma quantidade enorme de dados. O desafio não é produzir dados. É transformar dados em uma decisão na qual o time esteja disposto a agir.

## O que o engenheiro traz

Engenheiros contribuem com muito mais do que implementação.

Os engenheiros de pricing mais fortes com quem trabalhei perguntavam constantemente coisas como:

- Conseguimos explicar este preço?
- Conseguimos fazer rollback com segurança?
- Conseguimos medir o impacto?
- Conseguimos testar antes de expor o cliente?
- Conseguimos suportar variações futuras sem reescrever tudo?

Essas perguntas frequentemente influenciam o sucesso de uma iniciativa de pricing mais do que a própria regra.

Uma boa regra de pricing entregue sem segurança ainda pode gerar incidentes.

Uma ideia mediana de pricing entregue com segurança ainda pode gerar aprendizado valioso.

O valor real da engenharia não é a velocidade da entrega. É a segurança do caminho até a entrega.

## Por que contexto de negócio importa

Um dos erros mais fáceis que engenheiros podem cometer é supor que decisões de pricing são puramente matemáticas.

Elas não são.

Sistemas de pricing são fortemente moldados por contexto de negócio — acordos comerciais, relacionamento com provedores, restrições regulatórias, expectativas de mercado, comportamento sazonal e posicionamento competitivo. Uma regra que faz sentido técnico perfeito pode ser completamente incompatível com a realidade do negócio.

É por isso que times de pricing precisam de comunicação constante entre stakeholders técnicos e não técnicos. Sem isso, toda proposta técnica "limpa" vira uma reunião em que alguém explica lentamente por que a versão limpa não pode ser entregue.

## Construindo ownership compartilhado

Os times de pricing mais bem-sucedidos eventualmente desenvolvem uma linguagem compartilhada.

| Conceito | Visão de produto | Visão de analytics | Visão de engenharia |
| --- | --- | --- | --- |
| Markup | Alavanca de receita | Variável de experimento | Avaliação de regra |
| Fee | Experiência do cliente | Impacto em conversão | Configuração |
| Experimento | Hipótese | Teste estatístico | Mecanismo de rollout |
| Regra de pricing | Decisão de negócio | Variável observável | Lógica executável |

Quando times compartilham vocabulário, as discussões ficam significativamente mais produtivas. Sem linguagem compartilhada, conversas de pricing são exercícios de tradução. Com ela, viram decisões.

Mas vocabulário é só metade do ownership. A outra metade é ser honesto sobre o ciclo do qual o time é, de fato, responsável.

## O ciclo que o time de pricing é dono

Seria fácil ler este post como uma lista de papéis. Não é bem isso.

Papéis descrevem quem aparece. Ownership descreve pelo que o time é responsável. E o time de pricing — engenheiros, product managers, analistas, parceiros de negócio — é dono de mais do que um backlog de features.

Somos donos de um ciclo.

{{< plantuml title="O ciclo que o time de pricing é dono" >}}
@startuml
skinparam shadowing false

state Entender
state Responder
state Conduzir
state Construir
state Medir
state Aprender

[*] --> Entender
Entender --> Responder
Responder --> Conduzir
Conduzir --> Construir
Construir --> Medir
Medir --> Aprender
Aprender --> Entender
@enduml
{{< /plantuml >}}

Cada passo no ciclo é algo de que o time é dono — não delega para cima, não fica esperando, não empurra para outra função. Se um deles quebra, o ciclo deixa de ser ciclo e vira uma rua de mão única para fora do time.

| Verbo | O que o time de pricing é dono | Como parece quando falta |
| --- | --- | --- |
| Entender | O contexto de negócio, os clientes e o sistema existente — não só o código | "Não sabemos por que aquela regra existe" |
| Responder | As oportunidades, incidentes e pedidos que chegam do negócio e da produção | "Pricing é uma caixa-preta; ninguém retorna" |
| Conduzir | Direção proativa, não só trabalho reativo — propor o que testar a seguir | "Só mexemos em pricing quando alguém pede" |
| Construir | Implementação segura, reversível e observável da mudança | "Subimos. Tomara que funcione." |
| Medir | Instrumentação honesta do impacto, incluindo as partes que falham | "O dashboard está no roadmap de outro time" |
| Aprender | Agir no que os dados mostram, inclusive desligar e reescrever | "Rodamos o experimento mas nunca decidimos" |

Repare que isto não é um processo que o time *segue*. É uma postura que o time *mantém*. Um time de pricing que só constrói é um time de entrega das ideias dos outros. Um time de pricing que é dono do ciclo inteiro é o time em que você confia o próximo problema, mais difícil.

Isto não é uma hierarquia. É um contrato.

## A reunião que eu queria ter tido desde o primeiro dia

Quando um time aceita ownership desse ciclo, uma prática mantém o time honesto.

Uma revisão recorrente de pricing. Não uma reunião de status. Uma reunião de aprendizado.

Algo como:

1. O que mudou?
2. Por que mudamos?
3. O que aconteceu?
4. O que nos surpreendeu?
5. O que devemos fazer a seguir?

O objetivo não é culpa. O objetivo é o time se manter responsável pelo próprio ciclo — fechar a distância entre o que decidimos e o que de fato aconteceu. Sistemas de pricing melhoram quando times conectam decisões e resultados continuamente, e quando não precisam esperar um incidente para fazer isso.

## O que aprendi

A maior lição dos meus primeiros anos trabalhando com sistemas de pricing é que pricing não é uma disciplina de negócio nem uma disciplina técnica.

Ele vive na interseção dos dois mundos — e o time de pricing precisa viver lá também, sendo dono de cada passo entre entender o negócio e aprender com o resultado.

Bons times de pricing entendem clientes. Respondem a oportunidades. Conduzem direção. Constroem com cuidado. Medem com honestidade. Aprendem em voz alta. Nenhum desses passos é opcional. Nenhum pertence a outra pessoa.

## Reflexão final

Conforme a nossa colaboração melhorava, outro desafio surgiu. As próprias regras estavam ficando mais difíceis de entender. Cada experimento bem-sucedido introduzia novas condições, novas exceções e nova lógica de negócio. O problema difícil não era mais o alinhamento entre pessoas — era o alinhamento entre regras.

Se você está entrando em um sistema de pricing hoje, a pergunta mais útil no início não é *"como esse preço é calculado?"*. É *"quem é dono do ciclo em torno desse número — entender, responder, conduzir, construir, medir, aprender — e onde ele está quebrado?"*

A matemática é a parte fácil. O acordo é o sistema. O ownership do ciclo é o time.
