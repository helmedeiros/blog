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
series:
  - pricing-platform
series_order: 3
description: "Por que decisão de pricing que dá certo nasce de produto, analytics, engenharia e negócio trabalhando juntos — e não de uma disciplina sozinha."
subtitle: "Pricing vive na interseção entre produto, analytics, engenharia e negócio."
---

Uma das maiores surpresas depois que entrei num time de pricing não foi a complexidade das regras.

Foi descobrir quanta gente precisava estar envolvida pra mudar uma regra só.

Antes de mexer com sistema de pricing, eu achava que a maior parte das mudanças era técnica. Um stakeholder de negócio identificava uma oportunidade, um product manager priorizava, engenheiro implementava, e o sistema produzia um preço diferente.

A realidade era bem mais bagunçada.

Um experimento de pricing podia precisar de alinhamento entre stakeholder comercial, analista, product manager, engenheiro e time operacional. Cada um via a mesma mudança por uma lente diferente. Cada um se preocupava com risco diferente. Cada um media sucesso de um jeito.

Quanto mais tempo eu passava em pricing, mais ia caindo a ficha de que sistema de pricing que dá certo não é construído por disciplina isolada.

É construído por colaboração.

## A armadilha do engenheiro

Um dos primeiros erros que cometi foi tratar pricing como problema técnico.

Meu modelo mental era mais ou menos esse:

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

O processo real era mais parecido com isso:

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

A diferença entre esses dois fluxos é onde mora a maior parte da complexidade de pricing.

Não está no motor de regras. Está nas conversas que precisam acontecer antes de alguém tocar no motor de regras.

## O que o product manager traz

Os melhores product managers com quem trabalhei nunca começavam por uma porcentagem.

Começavam por um problema.

No lugar de perguntar *"a gente devia aumentar esse markup em 2%?"*, perguntavam *"que comportamento do cliente a gente quer influenciar?"* — ou *"que resultado de negócio a gente quer atingir?"*

Essa distinção importa. Decisão de pricing tem que nascer de hipótese, não de número solto.

| Responsabilidade de produto | Por que importa |
| --- | --- |
| Definir o problema do cliente | Evita mudança aleatória de pricing |
| Construir hipóteses | Cria expectativa mensurável |
| Priorizar oportunidades | Foca o esforço de engenharia |
| Alinhar stakeholders | Cria entendimento compartilhado |

A contribuição de verdade do PM não é a priorização. É o enquadramento que faz o resto do time concordar com o que "sucesso" significa antes de alguém escrever código.

## O que o analista traz

Se product manager define hipótese, analista define confiança.

Uma lição que aprendi rápido é que mudança de pricing sem medição não é experimento. É mudança em produção com passo a mais.

Todo experimento de pricing precisa de resposta honesta pra perguntas como essas:

- Qual métrica a gente tá otimizando?
- Quais guardrails protegem a experiência do cliente?
- Por quanto tempo o experimento deve rodar?
- Qual o tamanho mínimo da amostra?
- Como é que "sucesso" se parece, na prática?

Sem essas respostas, é fácil confundir ruído com aprendizado. Sistema de pricing gera uma quantidade enorme de dado. O desafio não é produzir dado. É transformar dado em uma decisão que o time topa agir.

## O que o engenheiro traz

Engenheiro entrega muito mais do que implementação.

Os engenheiros de pricing mais fortes do time perguntavam o tempo todo coisas como:

- A gente consegue explicar esse preço?
- A gente consegue fazer rollback com segurança?
- A gente consegue medir o impacto?
- A gente consegue testar antes de expor o cliente?
- A gente consegue suportar variação futura sem reescrever tudo?

Essas perguntas costumam influenciar o sucesso de uma iniciativa de pricing mais do que a própria regra.

Uma regra boa entregue sem segurança ainda gera incidente.

Uma ideia mediana entregue com segurança ainda gera aprendizado valioso.

O valor de verdade da engenharia não é velocidade de entrega. É segurança do caminho até a entrega.

## Por que contexto de negócio importa

Um dos erros mais fáceis que engenheiro comete é supor que decisão de pricing é só matemática.

Não é.

Sistema de pricing é fortemente moldado por contexto de negócio — acordo comercial, relacionamento com provedor, restrição regulatória, expectativa de mercado, comportamento sazonal, posicionamento competitivo. Uma regra que faz sentido técnico perfeito pode ser totalmente incompatível com a realidade do negócio.

É por isso que pricing exige comunicação constante entre stakeholder técnico e não técnico. Sem isso, toda proposta técnica "limpa" vira uma reunião em que alguém explica devagarinho por que a versão limpa não vai pra produção.

## Construindo ownership compartilhado

Em algum momento, o time de pricing vai desenvolver uma linguagem compartilhada.

| Conceito | Visão de produto | Visão de analytics | Visão de engenharia |
| --- | --- | --- | --- |
| Markup | Alavanca de receita | Variável de experimento | Avaliação de regra |
| Fee | Experiência do cliente | Impacto em conversão | Configuração |
| Experimento | Hipótese | Teste estatístico | Mecanismo de rollout |
| Regra de pricing | Decisão de negócio | Variável observável | Lógica executável |

Quando vocabulário é compartilhado, a discussão fica bem mais produtiva. Sem linguagem compartilhada, conversa de pricing vira exercício de tradução. Com ela, vira decisão.

Mas vocabulário é só metade do ownership. A outra metade é ser honesto sobre o ciclo do qual o time é, de fato, responsável.

## O ciclo que o time de pricing é dono

Seria fácil ler esse post como uma lista de papéis. Não é bem isso.

Papel descreve quem aparece. Ownership descreve pelo que o time é responsável. E o time de pricing — engenheiro, product manager, analista, parceiro de negócio — é dono de muito mais que um backlog de feature.

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

Cada passo no ciclo é algo de que o time é dono — não delega pra cima, não fica esperando, não empurra pra outra função. Se um deles quebra, o ciclo deixa de ser ciclo e vira rua de mão única pra fora do time.

| Verbo | O que o time de pricing é dono | Como parece quando falta |
| --- | --- | --- |
| Entender | O contexto de negócio, os clientes e o sistema existente — não só o código | "A gente não sabe por que aquela regra existe" |
| Responder | As oportunidades, incidentes e pedidos que chegam do negócio e da produção | "Pricing é caixa-preta; ninguém retorna" |
| Conduzir | Direção proativa, não só trabalho reativo — propor o que testar depois | "A gente só mexe em pricing quando alguém pede" |
| Construir | Implementação segura, reversível e observável da mudança | "Subimos. Tomara que dê certo." |
| Medir | Instrumentação honesta do impacto, inclusive das partes que falham | "O dashboard tá no roadmap de outro time" |
| Aprender | Agir no que o dado mostra, inclusive desligar e reescrever | "Rodamos o experimento mas nunca decidimos" |

Repare que isso não é um processo que o time *segue*. É uma postura que o time *mantém*. Um time de pricing que só constrói é um time de entrega das ideias dos outros. Um time de pricing que é dono do ciclo inteiro é o time em que você confia o próximo problema, mais difícil.

Não é hierarquia. É contrato.

## A reunião que eu queria ter tido desde o primeiro dia

Quando o time aceita ownership desse ciclo, uma prática mantém o time honesto.

Uma revisão recorrente de pricing. Não uma reunião de status. Uma reunião de aprendizado.

Algo como:

1. O que mudou?
2. Por que a gente mudou?
3. O que aconteceu?
4. O que surpreendeu a gente?
5. O que a gente faz agora?

O objetivo não é culpa. É o time se manter responsável pelo próprio ciclo — fechar a distância entre o que a gente decidiu e o que de fato aconteceu. Sistema de pricing melhora quando o time conecta decisão e resultado o tempo todo, e quando não precisa esperar um incidente pra fazer isso.

## O que aprendi

A maior lição dos meus primeiros anos com sistema de pricing é que pricing não é disciplina de negócio nem disciplina técnica.

Ele vive na interseção dos dois mundos — e o time de pricing precisa viver lá também, sendo dono de cada passo entre entender o negócio e aprender com o resultado.

A gente continuava voltando a entender os nossos clientes. Respondíamos a oportunidade. Conduzíamos direção. Construíamos com cuidado. Medíamos com honestidade. Aprendíamos em voz alta. Nenhum desses passos era opcional. Nenhum pertencia a outra pessoa.

## Reflexão final

À medida que a colaboração ia melhorando, outro desafio apareceu. As próprias regras estavam ficando mais difíceis de entender. Cada experimento que dava certo introduzia condição nova, exceção nova e lógica de negócio nova. O problema difícil não era mais o alinhamento entre pessoas — era o alinhamento entre regras.

Se você está entrando em um sistema de pricing hoje, a pergunta mais útil no começo não é *"como esse preço é calculado?"*. É *"quem é dono do ciclo em torno desse número — entender, responder, conduzir, construir, medir, aprender — e onde ele tá quebrado?"*

A matemática é a parte fácil. O acordo é o sistema. O ownership do ciclo é o time.
