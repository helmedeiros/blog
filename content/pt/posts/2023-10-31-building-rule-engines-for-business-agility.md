---
title: "Construindo Motores de Regras para Agilidade de Negócio"
categories:
  - Architecture
  - Engineering
  - Pricing
  - Platform
date: 2023-10-31
tags:
  - pricing
  - motor-de-regras
  - drools
  - business-rules-engine
  - monetizacao
  - platform-engineering
series:
  - pricing-platform
series_order: 5
description: "Por que a gente construiu um Business Rules Engine em cima do Drools em vez de acoplar a plataforma de pricing direto numa implementação de motor de regras."
subtitle: "Tecnologia muda. Capacidade de negócio sobrevive por muito mais tempo."
---

Quando a gente começou a discutir motor de regras, os sintomas já vinham aparecendo havia um tempo.

Regra de pricing estava se acumulando entre os serviços. Cada mercado precisava de uma exceção. Cada parceiro precisava de um ajuste. Cada experimento deixava pra trás código que ninguém sabia ao certo como remover. A lógica de pricing tinha virado o único lugar onde partes do negócio eram lembradas, e "explicar um preço" começava a exigir uma reunião.

Um motor de regras era o próximo passo óbvio. Antes de chegar em qual a gente escolheu, vale desacelerar pra olhar o que é um motor de regras, onde ele é usado e o que ele entrega quando você bota um em pé.

## O que é um motor de regras, no fundo

Um motor de regras é um software cujo único trabalho é avaliar decisões descritas como regras. As regras vivem separadas da aplicação que usa elas. O motor recebe uma entrada — uma requisição, uma transação, uma sessão — roda as regras relevantes contra ela e devolve uma resposta.

O nome clássico dessa categoria é *business rules management system* (BRMS). O termo vem dos anos 90, quando empresas perceberam que as decisões de política enterradas dentro de aplicação enterprise mudavam mais rápido que a própria aplicação.

Três propriedades definem um motor de regras, em qualquer época e em qualquer stack:

- Regra é **declarada**, não hardcoded.
- Regra é **avaliada por um runtime separado do código chamador**.
- Regra pode ser **adicionada, modificada e removida sem reescrever a aplicação**.

A última é a que importa. O resto é encanamento a serviço dela.

## Onde motor de regras aparece

Pricing não é caso especial. Onde quer que uma decisão precise mudar mais rápido que o software ao redor dela, aparece motor de regras:

- **Detecção de fraude** — declarar o que conta como suspeito; ajustar limiar sem redeploy.
- **Crédito e empréstimo** — codificar política de aprovação/recusa num lugar auditável.
- **Subscrição de seguros** — aplicar regra de risco em vários produtos sem copy-paste de código por produto.
- **Compliance e regulação** — manter restrição estatutária num lugar que auditor consegue ler.
- **Moderação de conteúdo** — expressar política de moderação que muda conforme norma e regulação mudam.
- **Roteamento de workflow** — decidir pra onde um caso, ticket ou documento vai depois.
- **Personalização** — expressar regra de segmento ao lado de scoring baseado em modelo.

O padrão se repete. Uma política de negócio precisa mudar mais rápido do que o sistema ao redor permite com facilidade. Um motor de regras tira a política da aplicação e bota num lugar que o negócio consegue alcançar de verdade.

## Por que o time recorre a um

Os motivos pelos quais o time adota um motor de regras raramente são teóricos. Aparecem como atrito no dia a dia:

- Stakeholder de negócio quer uma mudança que o engenheiro precisa fazer deploy.
- Ninguém consegue explicar por que uma decisão específica saiu do jeito que saiu.
- Um experimento exige uma mudança de regra, mas mudar a regra significa rodar o pipeline de release do serviço inteiro.
- Uma política expirou, mas ninguém sabe ao certo onde ela mora.
- Dois times vivem se atropelando porque as regras deles tocam no mesmo código.

Motor de regras não faz esses problemas sumirem. Move pra um lugar onde o time consegue resolver sem passar pelo ciclo de release da aplicação.

## O que um bom motor de regras te entrega

Quando tá funcionando, um motor de regras entrega ao time algumas capacidades específicas:

| Capacidade | O que possibilita |
| --- | --- |
| Regras externalizadas | Mudar política sem redeploy do serviço consumidor |
| Formato declarativo | Ler regra como política, não como fluxo de controle |
| Resolução de conflito | Decidir prioridade e override entre regras de forma consistente |
| Simulação | Rejogar tráfego histórico contra um conjunto de regras candidato |
| Explicabilidade | Rastrear por que uma decisão específica saiu do jeito que saiu |
| Ciclo de vida | Versionar, depreciar e aposentar regra de forma deliberada |
| Trilha de auditoria | Mostrar quem mudou qual regra e quando |

"Avaliação rápida" não tá no topo da lista. Performance importa, mas raramente é o motivo pelo qual o time adota um motor de regras. Os motivos são governança e ritmo de mudança. O runtime é o meio, não o fim.

## Por que motor de regras era o próximo passo pra gente

Os padrões aí em cima não eram hipóteses pro nosso time. Eram nossos tickets abertos.

Stakeholder esperando deploy. Experimento travado atrás de pipeline de release. Ninguém conseguia responder rápido por que um markup específico tinha sido aplicado. Algumas regras tinham expirado mas continuavam no código, intocadas porque remover parecia mais arriscado que manter. Dois times tinham começado a adicionar lógica de pricing em lugares que tocavam nos mesmos pedaços de código.

Cada um desses era um problema de governança disfarçado de problema de engenharia.

Teria sido fácil ler isso como "a gente precisa de um motor de regras" e parar por aí:

{{< plantuml title="A versão mais curta da história" >}}
@startuml
skinparam shadowing false
start
:Precisamos de regras;
:Precisamos de motor de regras;
stop
@enduml
{{< /plantuml >}}

Essa leitura é incompleta. A cadeia real era mais parecida com isso aqui:

{{< plantuml title="A cadeia real: avaliação de regras era só o último elo" >}}
@startuml
skinparam shadowing false
start
:Precisamos de agilidade de negócio;
:Precisamos de experimentos mais rápidos;
:Precisamos de explicabilidade;
:Precisamos de ownership;
:Precisamos de simulações;
:Precisamos de avaliação de regras;
stop
@enduml
{{< /plantuml >}}

O negócio não pedia motor de regras no abstrato. O negócio pedia velocidade. O motor de regras era o meio.

Então, quando a gente começou a avaliar implementações, os critérios vinham da cadeia — não só "consegue rodar regra rápido?", mas "ele ajuda a gente a evoluir essas regras com honestidade?".

## Drools como nossa escolha de implementação

Quando a gente avaliou as opções, Drools se destacou rapidamente.

| Capacidade | Por que importava |
| --- | --- |
| Ecossistema maduro | Reduzia risco de implementação |
| Avaliação complexa de regras | Suportava cenário real de pricing |
| Agenda management | Ajudava com resolução de conflito entre regras |
| Performance | Adequado pra decisão em tempo de busca |
| Open source | Evitava lock-in comercial |
| Expertise no mercado | Contratação e onboarding mais fáceis |

Por um tempo, a arquitetura parecia direta.

{{< plantuml title="A arquitetura que quase entregamos" >}}
@startuml
skinparam shadowing false
skinparam componentStyle rectangle

[Plataforma de Pricing] as P
[Drools] as D

P --> D
@enduml
{{< /plantuml >}}

Quanto mais a gente discutia, menos confortáveis a gente ficava.

## O risco de deixar Drools virar o próximo monólito

Drools era escolha de tecnologia. Pricing era capacidade de negócio.

Essas duas coisas têm tempos de vida bem diferentes. Tecnologia muda. Capacidade de negócio costuma sobreviver por muito mais tempo.

Uma pergunta aparecia direto nas nossas revisões: *e se o motor de regras virar o próximo monólito?* Se a plataforma de pricing dependesse direto do Drools, toda decisão futura sobre pricing ia carregar uma suposição sobre Drools. Todo teste ia precisar de uma sessão do Drools. Todo onboarding ia começar por conceito do Drools. Toda migração ia ser uma reescrita acoplada.

A gente não tava preocupado com Drools falhar como produto. Tava preocupado com Drools dar certo como dependência.

A gente não tinha um contra-desenho pronto na época. Só sabia o suficiente pra continuar fazendo a pergunta. A plataforma de pricing não devia depender direto do Drools. Devia depender de uma abstração que fosse nossa.

{{< plantuml title="A arquitetura que entregamos no lugar" >}}
@startuml
skinparam shadowing false
skinparam componentStyle rectangle

[Plataforma de Pricing] as P
[Business Rules Engine] as BRE
[Drools] as D

P --> BRE
BRE --> D
@enduml
{{< /plantuml >}}

Essa camada do meio é o que tornou o resto da história possível. Não era um wrapper. Era um contrato que dizia: pricing decide o que perguntar, o motor decide como responder, e o time é dono da fronteira entre os dois.

## Apresentando o Business Rules Engine

Em vez de expor Drools direto pro resto da plataforma de pricing, a gente criou uma camada interna que chamou de Business Rules Engine.

O objetivo era simples. A plataforma de pricing devia pedir decisão. Não devia se importar com como aquelas decisões eram avaliadas.

```java
RuleRequest request =
    RuleRequest.builder()
        .market("DE")
        .provider("rail")
        .currency("EUR")
        .daysBeforeDeparture(5)
        .build();

RuleResult result =
    businessRulesEngine.evaluate(request);
```

Repara no que tá faltando. Nenhuma API do Drools. Nenhuma sessão do Drools. Nenhum conceito específico do Drools vazando pro código de pricing.

A assinatura de `evaluate` é a assinatura da capacidade de negócio. O que a gente colocar embaixo precisa honrar.

## Regra virou ativo de negócio

Uma consequência inesperada da abstração foi que as regras pararam de parecer código. Passaram a parecer ativo de negócio.

```yaml
id: short_lead_time_markup
owner: pricing-team
reason: Aumentar receita em compras com pouca antecedência
metric: revenue_per_search
status: experiment
expires_at: 2024-01-31
```

Em vez de perguntar onde tava o código, as pessoas começaram a perguntar quem era dono da regra e por que ela existia. Essa mudança de pergunta é justamente o propósito da fronteira.

## Os benefícios inesperados

Quando a abstração se sustentou, quatro benefícios apareceram que a gente não tinha desenhado.

### Testes melhores

A plataforma de pricing podia ser testada sem subir uma sessão do Drools. Os testes conversavam com a interface do Business Rules Engine e mocavam o motor por baixo. Teste unitário ficou rápido. Teste de integração ficou honesto.

### Simulações mais fáceis

Como o motor aceitava requisição independente de qualquer fluxo de produto, a gente podia rejogar histórico por ele.

{{< plantuml title="Simulando impacto em receita sem fechar nenhuma compra" >}}
@startuml
skinparam shadowing false
start
:Buscas dos últimos 30 dias;
:Business Rules Engine;
:Impacto esperado em receita;
stop
@enduml
{{< /plantuml >}}

Manda as buscas dos últimos 30 dias pra BRE com uma regra candidata ativa, compara as saídas contra o baseline, e tá feita uma estimativa crível de impacto sem expor um único cliente.

### Mudanças futuras mais seguras

Substituir o motor por baixo passou a ser possível. Não fácil. Mas possível. Só isso já valia o custo da fronteira, porque todo motor que a gente avaliou tinha um roadmap que a gente não controlava.

### Onboarding mais rápido

Engenheiro novo aprendia conceito de pricing primeiro. Não internals do Drools primeiro. A fronteira era ferramenta pedagógica tanto quanto técnica.

## O vazamento de abstração contra o qual a gente lutou sempre

Toda abstração vaza com o tempo.

Drools tinha features poderosas. Às vezes a gente queria buscar elas direto. Isso criava tensão dentro do time. O Business Rules Engine devia expor essas capacidades, ou devia permanecer independente?

Essa disputa forçou a gente a pensar com cuidado sobre quais capacidades eram de pricing e quais eram do Drools. A resposta normalmente era insatisfatória no momento e certa no longo prazo: se uma feature só fazia sentido em termos de Drools, ela não pertencia à interface da BRE. Se ela expressava uma decisão de negócio, pertencia.

A fronteira se sustentou porque a gente continuou defendendo.

## O que aprendi

Olhando pra trás, Drools não foi a decisão que envelheceu melhor. A decisão que envelheceu melhor foi a gente ter se recusado a deixar a plataforma de pricing depender direto dele.

Tecnologia muda. Capacidade de negócio sobrevive por muito mais tempo.

O Business Rules Engine deixou a gente focar em decisão de pricing em vez de detalhe de implementação. Criou uma fronteira estável. E fronteira estável costuma valer mais do que tecnologia perfeita.

## Reflexão final

Em algum momento, a gente percebeu que não estava mais construindo feature de pricing. Tava construindo capacidade de pricing.

Regra podia ser criada. Regra podia ser simulada. Regra podia ser explicada. Regra podia ser medida. Regra podia ser aposentada.

Essa percepção mudou como a gente pensava em ownership. Mudou como a gente pensava em experimentação. E mudou como a gente pensava sobre o próprio pricing.

Pricing já não tava se comportando como feature. Tava se comportando como produto.

Anos depois, eu não consigo te dizer se Drools foi a escolha certa. Posso te dizer que a camada que a gente construiu por cima dele continua fazendo o trabalho — traduzindo decisão de pricing pra um vocabulário do qual o time é dono, independente do que estiver embaixo. Essa foi a parte que importou. O motor era detalhe. A fronteira era o trabalho.
