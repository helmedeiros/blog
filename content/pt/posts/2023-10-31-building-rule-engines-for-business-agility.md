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
description: "Por que construímos um Business Rules Engine sobre Drools em vez de acoplar a plataforma de pricing diretamente a uma implementação de motor de regras."
subtitle: "Tecnologias mudam. Capacidades de negócio sobrevivem por muito mais tempo."
---

Quando começamos a discutir motores de regras, os sintomas já vinham aparecendo havia algum tempo.

Regras de pricing estavam se acumulando entre os serviços. Cada mercado precisava de uma exceção. Cada parceiro precisava de um ajuste. Cada experimento deixava para trás código que ninguém sabia ao certo como remover. A lógica de pricing virou o único lugar onde partes do negócio eram lembradas, e "explicar um preço" começava a exigir uma reunião.

Um motor de regras era o próximo passo óbvio. Antes de chegar em qual escolhemos, vale desacelerar no que um motor de regras é de fato, onde times usam e o que ele entrega quando você coloca um em pé.

## O que um motor de regras é, de fato

Um motor de regras é um software cujo único trabalho é avaliar decisões descritas como regras. As regras vivem separadas da aplicação que as usa. O motor recebe uma entrada — uma requisição, uma transação, uma sessão — roda as regras relevantes contra ela e devolve uma resposta.

O nome clássico dessa categoria é *business rules management system* (BRMS). O termo vem dos anos 90, quando empresas perceberam que as decisões de política enterradas dentro de aplicações enterprise mudavam mais rápido do que as próprias aplicações.

Três propriedades definem um motor de regras, em qualquer época e em qualquer stack:

- Regras são **declaradas**, não hardcoded.
- Regras são **avaliadas por um runtime separado do código chamador**.
- Regras podem ser **adicionadas, modificadas e removidas sem reescrever a aplicação**.

A última é a propriedade que importa. O resto é encanamento a serviço dela.

## Onde motores de regras aparecem

Pricing não é caso especial. Onde quer que uma decisão precise evoluir mais rápido do que o software ao redor dela, aparece um motor de regras:

- **Detecção de fraude** — declarar o que conta como suspeito; ajustar limiares sem redeploy.
- **Crédito e empréstimo** — codificar política de aprovação/recusa em um lugar auditável.
- **Subscrição de seguros** — aplicar regras de risco em vários produtos sem copy-paste de código por produto.
- **Compliance e regulação** — manter restrições estatutárias em um lugar que auditores conseguem ler.
- **Moderação de conteúdo** — expressar políticas de moderação que mudam conforme normas e regulações mudam.
- **Roteamento de workflow** — decidir para onde um caso, um ticket ou um documento vai a seguir.
- **Personalização** — expressar regras de segmento ao lado de scoring baseado em modelo.

O padrão se repete. Uma política de negócio precisa mudar mais rápido do que o sistema ao redor permite com facilidade. Um motor de regras tira a política da aplicação e a coloca em um lugar que o negócio consegue alcançar de verdade.

## Por que um time recorre a um

Os motivos pelos quais times adotam um motor de regras raramente são teóricos. Eles aparecem como atrito no dia a dia:

- Stakeholders de negócio querem uma mudança que um engenheiro precisa fazer deploy.
- Ninguém consegue explicar por que uma decisão específica saiu do jeito que saiu.
- Um experimento exige uma mudança de regra, mas mudar a regra significa rodar o pipeline de release do serviço inteiro.
- Uma política expirou, mas ninguém sabe ao certo onde ela mora.
- Dois times ficam se atropelando porque as regras deles tocam no mesmo código.

Um motor de regras não faz esses problemas desaparecerem. Ele os move para um lugar onde o time consegue resolver sem passar pelo ciclo de release da aplicação.

## O que um bom motor de regras te entrega

Quando está funcionando, um motor de regras entrega ao time algumas capacidades específicas:

| Capacidade | O que possibilita |
| --- | --- |
| Regras externalizadas | Mudar política sem redeploy do serviço consumidor |
| Formato declarativo | Ler regras como política, não como fluxo de controle |
| Resolução de conflito | Decidir prioridade e overrides entre regras de forma consistente |
| Simulação | Rejogar tráfego histórico contra um conjunto de regras candidato |
| Explicabilidade | Rastrear por que uma decisão específica saiu do jeito que saiu |
| Ciclo de vida | Versionar, depreciar e aposentar regras de forma deliberada |
| Trilha de auditoria | Mostrar quem mudou qual regra e quando |

"Avaliação rápida" não está no topo da lista. Performance importa, mas raramente é o motivo pelo qual times adotam um motor de regras. Os motivos são governança e ritmo de mudança. O runtime é o meio, não o fim.

## Por que um motor de regras era o próximo passo para a gente

Os padrões acima não eram hipotéticos para nosso time. Eram nossos tickets abertos.

Stakeholders esperando deploy. Experimentos travados atrás de pipelines de release. Ninguém conseguia responder rápido por que um markup específico tinha sido aplicado. Algumas regras tinham expirado mas continuavam no código, intocadas porque remover parecia mais arriscado do que manter. Dois times tinham começado a adicionar lógica de pricing em lugares que tocavam nos mesmos pedaços de código.

Cada um desses era um problema de governança disfarçado de problema de engenharia.

Teria sido fácil ler isso como "precisamos de um motor de regras" e parar por aí:

{{< plantuml title="A versão mais curta da história" >}}
@startuml
skinparam shadowing false
start
:Precisamos de regras;
:Precisamos de motor de regras;
stop
@enduml
{{< /plantuml >}}

Essa leitura é incompleta. A cadeia real era mais parecida com isto:

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

O negócio não pedia um motor de regras no abstrato. O negócio pedia velocidade. O motor de regras era o meio.

Então, quando começamos a avaliar implementações, os critérios vinham da cadeia — não só "consegue rodar regras rápido?", mas "ele ajuda a gente a evoluir essas regras com honestidade?".

## Drools como nossa escolha de implementação

Quando avaliamos opções, Drools se destacou rapidamente.

| Capacidade | Por que importava |
| --- | --- |
| Ecossistema maduro | Reduzia risco de implementação |
| Avaliação complexa de regras | Suportava cenários reais de pricing |
| Agenda management | Ajudava com resolução de conflitos entre regras |
| Performance | Adequado para decisões em tempo de busca |
| Open source | Evitava lock-in comercial |
| Expertise existente no mercado | Contratação e onboarding mais fáceis |

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

Quanto mais discutíamos, menos confortáveis ficávamos.

## O risco de deixar Drools virar o próximo monólito

Drools era uma escolha de tecnologia. Pricing era uma capacidade de negócio.

Essas duas coisas têm tempos de vida muito diferentes. Tecnologias mudam. Capacidades de negócio tendem a sobreviver por muito mais tempo.

Uma pergunta aparecia direto nas nossas revisões: *e se o motor de regras virar o próximo monólito?* Se a plataforma de pricing dependesse diretamente do Drools, toda decisão futura sobre pricing carregaria uma suposição sobre Drools. Todo teste precisaria de uma sessão do Drools. Todo onboarding começaria por conceitos do Drools. Toda migração seria uma reescrita acoplada.

Não estávamos preocupados com Drools falhar como produto. Estávamos preocupados com Drools dar certo como dependência.

A gente não tinha um contra-desenho pronto na época. Só sabíamos o suficiente para continuar fazendo a pergunta. A plataforma de pricing não deveria depender diretamente do Drools. Deveria depender de uma abstração que fosse nossa.

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

Em vez de expor Drools diretamente para o resto da plataforma de pricing, criamos uma camada interna que chamamos de Business Rules Engine.

O objetivo era simples. A plataforma de pricing deveria pedir decisões. Ela não deveria se importar com como aquelas decisões eram avaliadas.

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

Repare no que está faltando. Nenhuma API do Drools. Nenhuma sessão do Drools. Nenhum conceito específico do Drools vazando para o código de pricing.

A assinatura de `evaluate` é a assinatura da capacidade de negócio. O que quer que coloquemos por baixo precisa honrá-la.

## Regras viraram ativos de negócio

Uma consequência inesperada da abstração foi que as regras pararam de parecer código. Elas passaram a parecer ativos de negócio.

```yaml
id: short_lead_time_markup
owner: pricing-team
reason: Aumentar receita em compras com pouca antecedência
metric: revenue_per_search
status: experiment
expires_at: 2024-01-31
```

Em vez de perguntar onde estava o código, as pessoas começaram a perguntar quem era dono da regra e por que ela existia. Essa mudança de pergunta é justamente o propósito da fronteira.

## Os benefícios inesperados

Quando a abstração se sustentou, quatro benefícios apareceram que não tínhamos desenhado.

### Testes melhores

A plataforma de pricing podia ser testada sem subir uma sessão do Drools. Os testes conversavam com a interface do Business Rules Engine e mocavam o motor por baixo. Testes unitários ficaram rápidos. Testes de integração ficaram honestos.

### Simulações mais fáceis

Como o motor aceitava requisições independentes de qualquer fluxo de produto, podíamos rejogar histórico através dele.

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

Manda as buscas dos últimos 30 dias para a BRE com uma regra candidata ativa, compara as saídas contra o baseline, e você tem uma estimativa crível de impacto sem expor um único cliente.

### Mudanças futuras mais seguras

Substituir o motor por baixo passou a ser possível. Não fácil. Mas possível. Só isso já valeria o custo da fronteira, porque todo motor que avaliamos tinha um roadmap que não controlávamos.

### Onboarding mais rápido

Engenheiros novos aprendiam conceitos de pricing primeiro. Não internals do Drools primeiro. A fronteira era uma ferramenta pedagógica tanto quanto uma técnica.

## O vazamento de abstração contra o qual lutamos sempre

Toda abstração vaza eventualmente.

Drools tinha features poderosas. Às vezes os times queriam usá-las diretamente. Isso criava tensão. O Business Rules Engine deveria expor essas capacidades, ou deveria permanecer independente?

Essa disputa nos forçou a pensar com cuidado sobre quais capacidades pertenciam a pricing e quais pertenciam ao Drools. A resposta normalmente era insatisfatória no momento e certa no longo prazo: se uma feature só fazia sentido em termos de Drools, ela não pertencia à interface da BRE. Se ela expressava uma decisão de negócio, pertencia.

A fronteira se sustentou porque continuamos defendendo.

## O que aprendi

Olhando para trás, Drools não foi a decisão que envelheceu melhor. A decisão que envelheceu melhor foi nos recusarmos a deixar a plataforma de pricing depender diretamente dele.

Tecnologias mudam. Capacidades de negócio sobrevivem por muito mais tempo.

O Business Rules Engine nos permitiu focar em decisões de pricing em vez de detalhes de implementação. Ele criou uma fronteira estável. E fronteiras estáveis costumam ser mais valiosas do que tecnologias perfeitas.

## Reflexão final

Eventualmente percebemos que não estávamos mais construindo features de pricing. Estávamos construindo capacidades de pricing.

Regras podiam ser criadas. Regras podiam ser simuladas. Regras podiam ser explicadas. Regras podiam ser medidas. Regras podiam ser aposentadas.

Essa percepção mudou como pensávamos em ownership. Mudou como pensávamos em experimentação. E mudou como pensávamos sobre o próprio pricing.

Pricing não estava mais se comportando como uma feature. Estava se comportando como um produto.

Se você está prestes a introduzir um motor de regras em um sistema que já funciona, a pergunta que vale a pena fazer não é *"qual motor devemos escolher?"*. É *"qual capacidade de negócio o nosso time precisa continuar sendo dono daqui a vinte deploys, independente do motor que estiver por baixo?"*

O motor é substituível. A capacidade é a fronteira.
