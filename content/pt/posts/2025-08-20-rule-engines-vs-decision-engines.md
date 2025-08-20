---
title: "Rule Engine vs Decision Engine"
subtitle: "Rule engine responde o que casa. Decision engine responde o que deve acontecer. O gap entre essas duas perguntas é onde a maioria das plataformas de pricing cresce."
author: helio
layout: post
date: 2025-08-20T10:00:00+00:00
series:
  - pricing-engineering
series_order: 11
categories:
  - Engineering
  - Pricing
  - Architecture
tags:
  - pricing
  - rule-engine
  - decision-engine
  - architecture
  - models
  - constraints
description: "Rule engine casa regra contra fact e roda ação. Decision engine coordena regra com modelo, restrição, política e experimento pra produzir uma decisão única explicada. Esse post é sobre o gap entre os dois e quando cada um é a ferramenta certa."
---

Teve uma terça de manhã em que tentei expressar uma decisão única de pricing como uma regra única e descobri que precisava de três.

A decisão era pequena em termos de negócio: *aplica um markup base, mas limita por um budget de fairness por cliente, mas sobrepõe os dois se tem experimento ativo pra esse cliente, e nunca ultrapassa o teto regulatório nesse mercado*. O dono de produto tinha descrito numa frase. Quando estava na rule store eram três regras com priority cuidadosamente afinada, uma quarta regra pro teto regulatório, um bloco de comentário explicando a dependência entre elas, e uma previsão em bloco de comentário de que "a gente vai se arrepender disso".

A previsão tava certa. Seis semanas depois o experimento mudou de formato, uma priority precisou se mexer, e a trava de fairness interagiu com o markup novo de um jeito que o rule engine não conseguia ver. Pegamos no shadow mode antes de shippar. O fix era estrutural, não local — não precisava editar uma regra; precisava de uma camada acima do rule engine que *coordenasse* o output da regra com o output do modelo, a restrição, e o contexto do experimento. O time vinha construindo um rule engine por meses. A gente tinha acabado de descobrir que o que precisava de verdade era um decision engine.

É disso que trata o resto desse post. Rule engine responde *o que casa*. Decision engine responde *o que deve acontecer*. O gap entre essas duas perguntas é onde a maioria das plataformas de pricing cresce.

## O que o rule engine é, num frame

O rule engine, depois de dez posts de desenho cuidadoso, tem contrato apertado:

```
Execute(ctx, facts) → Result
```

Facts entram. O matcher encontra as regras cujas condições são satisfeitas pelos facts. O evaluator confirma. O executor roda a ação de cada regra. O composer combina os outputs das ações num resultado, segundo a política de resolução.

O rule engine é bom em uma coisa específica: *rodar regra declarada de forma determinística e explicável*. Não é bom nas coisas dos dois lados dessa coisa única.

Não decide *quais regras sequer considerar*. O rule set inteiro é carregado; o engine matcheia sobre tudo. Se você quer considerar regra de forma condicional — digamos, só as regras de overlay de experimento quando um experimento tá ativo — dá pra codificar isso como parte do matching, mas o engine em si não tem noção de *contextos* do jeito que um decision engine tem.

Não coordena os *outputs* com nada fora do engine. O composer combina output de regras, mas não de um modelo que mora em outro serviço. Se o markup deveria ser o *mínimo* entre o que o rule engine produz e o que um modelo de elasticidade recomenda, o rule engine não expressa isso sozinho.

Não impõe *restrição externa* que as regras não codificam. Um teto regulatório que deveria valer sobre toda combinação possível de regra tem que ser re-codificado como regra no engine, o que significa que mudança no teto agora é edição de regra, o que significa que a restrição e a regra colapsaram pra mesma camada.

A terça de manhã que descrevi foi o momento em que esses três limites se cruzaram. A decisão tinha múltiplos inputs — regras, modelo, restrição, contexto de experimento — e o rule engine só enxergava um. O rule engine da plataforma tava funcionando perfeitamente. A plataforma não tinha decision engine.

## O que um decision engine adiciona

Um decision engine fica *acima* de um rule engine. Seu contrato é mais largo:

```
Decide(ctx, context) → Decision + Explanation
```

Onde `context` não é só facts — é o pacote de inputs de que a decisão precisa, e facts é um deles:

- Os **facts da request** (o que o rule engine consome).
- Um conjunto de **rule sets** pra avaliar (possivelmente mais de um; possivelmente condicional).
- **Outputs de modelo** que a decisão deveria considerar (elasticidade, forecast de demanda, score de fraude).
- **Restrições** que a decisão final tem que satisfazer (teto regulatório, budget de fairness, nunca-faz).
- **Política** sobre como combinar o acima (rules-first, model-first, otimização-restrita).
- **Contexto de experimento** que pode moldar quais regras, qual modelo, qual política.

Um decision engine aceita esse pacote, coordena os componentes, e emite uma decisão única com uma explicação única. O rule engine é um de vários inputs.

{{< plantuml title="Um decision engine coordena regra com os outros inputs de uma decisão real" >}}
@startuml
skinparam shadowing false
skinparam componentStyle rectangle
skinparam defaultFontName "Helvetica"

rectangle "Request\nfacts + correlation_id" as R

rectangle "Decision engine" as DE {
  rectangle "Context builder\nfacts + experimento + segmento" as CB
  rectangle "Rule engine\n(bre-go)\ncasa & avalia" as RE
  rectangle "Serviço de modelo\nelasticidade, demanda,\nscore de fraude" as MS
  rectangle "Check de restrição\nregulatório, fairness,\nbudget" as CC
  rectangle "Policy composer\ncombina conforme\npolítica ativa" as PC
}

rectangle "Decisão\n+ explicação" as D

R --> CB
CB --> RE
CB --> MS
RE --> PC
MS --> PC
PC --> CC
CC --> D
@enduml
{{< /plantuml >}}

Os quatro componentes acima da linha tracejada são input; os componentes abaixo dela são o trabalho do decision engine. O rule engine é o input mais à esquerda, não o centro. O centro do decision engine é o policy composer que transforma "olha aqui o que cada input diz" em "olha aqui o que o sistema vai fazer".

## Quando rule engine é suficiente

A resposta honesta é: na maior parte do tempo, mais tempo do que você esperaria.

Um rule engine é suficiente quando:

**A decisão consegue ser expressa como função determinística dos facts.** Sem modelo. Sem chamada a serviço externo. As condições nomeiam campo; as ações setam valor; o resultado é a composição. Markup de pricing em mercado estável em geral cabe nesse formato. Decisão de roteamento em geral cabe. Muito override de compliance cabe.

**O conjunto de inputs que governa a decisão é fechado.** O time é dono de todo campo que a regra lê. Não tem fact que more em outro lugar (serviço de modelo, sinal em tempo real). Conjunto de input fechado é dramaticamente mais simples de raciocinar do que conjunto aberto, e o rule engine lida com isso de forma elegante.

**A política de composição é simples.** Aditiva, last-wins, ordenada por priority. O composer do Post 5 trata os três com uma linha de configuração cada. Se sua decisão é "empilha esses markups" ou "o override mais específico ganha", rule engine é a ferramenta certa.

**O orçamento de latência é apertado.** O rule engine é in-process. Um decision engine que chama um serviço de modelo via rede é in-process *mais* algumas centenas de microssegundos em p50 e vários milissegundos em p99. Algumas superfícies de pricing não conseguem pagar o orçamento.

Essas quatro condições descrevem o regime permanente de muitos sistemas de pricing. Um time de pricing que shippa um rule engine limpo e nunca cresce além dele não tá desperdiçando oportunidade; tá casando a ferramenta com o problema.

## Quando o decision engine vira necessário

Quatro sinais de que o rule engine tá sendo pedido pra fazer mais do que o contrato dele:

**Um output de modelo deveria influenciar a decisão.** O time tem um modelo de sensibilidade a preço cujo output deveria informar o markup, mas não determinar sozinho. Dentro de um rule engine, isso vira ou *uma regra que consulta o modelo dentro da ação* (o que quebra determinismo e explicabilidade) ou *um serviço separado que roda o modelo e o rule engine e costura os resultados* (o que é, por outro nome, um decision engine).

**Uma restrição precisa valer sobre todos os resultados de regra.** Um teto regulatório. Um piso de fairness. Um desconto máximo total por cliente por trimestre. Dentro de um rule engine, a restrição vira uma regra, o que significa que a autoridade da restrição e a autoridade da regra agora são a mesma camada — e o time dono da restrição e o time dono das regras podem não ser o mesmo time. Um decision engine separa a restrição no próprio check, com o próprio dono.

**O conjunto de rule sets é condicional.** Experimento A sobrepõe certas regras pra certos clientes. Os overrides do Experimento B são diferentes. A camada de matching do rule engine consegue codificar o contexto de experimento como fact, mas a *governança* de quais experimentos estão vivos, quais clientes afetam, e o que sobrepõem agora tá na rule store. Um decision engine puxa o contexto de experimento pra um componente próprio.

**A decisão tem que compor input de camadas diferentes.** O output é *o mínimo de A, B e C, limitado por D, enviesado por E*. O rule engine computa A. O serviço de modelo computa B. C é um cap configurado. D é um valor regulatório de um serviço de compliance. E é um lift de experimento. Nenhum sozinho é a resposta; a resposta é o que o composer faz dos três juntos.

Quando dois ou mais desses sinais aparecem, a plataforma não é mais um rule engine que quer crescer. É um decision engine que tava postergado. A terça de manhã foi o momento em que a plataforma que eu vinha construindo cruzou essa linha, e o rule engine seguiu funcionando, mas deixou de ser suficiente.

## As costuras que merecem destaque

Três costuras que o decision engine tem que cuidar. Cada uma é um lugar em que a plataforma ou ganha arquitetura ou ganha dívida técnica.

### Regra + modelo

Um output de modelo não é do mesmo formato do output de regra. O rule engine produz um resultado estruturado com proveniência: *short_lead_time_markup_de setou markup pra 3% em priority 500*. O modelo produz um número com confiança: *elasticity_v3 estima markup de 2,7% com IC 90% [2,4; 3,0]*.

O decision engine tem que coordenar. O padrão mais limpo que vi na prática — embora, como o laboratório do Post 10, esse seja um que explorei mais no desenho do que em produção — é tornar o output do modelo um *fact* que o rule engine consome, e aí codificar a política de como regra e modelo interagem como parte da própria regra.

```yaml
- id: markup_with_elasticity_bias
  intent: |
    Aplica o markup definido pela regra, mas inclina 30% em
    direção à recomendação do modelo de elasticidade. A regra
    segue como contrato de negócio; o modelo é um dos inputs.
  when:
    market: { eq: DE }
    days_to_departure: { lt: 7 }
  then:
    type: blended_markup
    base: 3.0
    bias_field: model.elasticity_v3.markup
    weight: 0.30
```

A *intenção* da regra é o contrato de que o time é dono. O valor do modelo é o *viés*. O composer aplica uma mistura determinística. A explicação consegue carregar a intenção da regra e o valor do modelo lado a lado, pra que o auditor veja qual dos dois puxou qual fração do número final.

O risco no padrão é o modelo virar autor escondido de regra que o time não escreveu. A defesa é manter a regra explicitamente no controle: a regra diz *o que fazer com* o modelo; nunca delega a decisão pro modelo.

### Regra + restrição

Restrição é regra que o time não escreveu, que tem que valer independentemente de quais regras dispararam. Um cap regulatório. Um piso de nunca-descontar-abaixo-do-custo. Um limite de fairness.

Codificar essas como regras dentro do rule engine é tentador e é um erro de longo prazo. A restrição tem ownership diferente (jurídico, compliance, financeiro), cadência de mudança diferente (mais lenta), e modo de falha diferente (violação é evento regulatório, não evento de serviço).

O decision engine trata restrição como estágio separado. Regra produz uma decisão candidata. Restrição confere o candidato. Se o candidato viola uma restrição, o decision engine ou rejeita (devolvendo um default seguro), ou limita (cortando no valor da restrição), ou escala (logando e expondo pra revisão). Cada comportamento é configurável por restrição.

```go
type Constraint interface {
    Check(decision Decision, ctx Context) ConstraintResult
}

type ConstraintResult struct {
    Violated  bool
    Action    string  // "reject", "clip", "escalate"
    ClipValue *float64
    Reason    string
}
```

A explicação carrega o resultado da restrição. Uma auditoria perguntando "o cap regulatório foi respeitado?" lê o check de restrição, não o trace de regra. Essa separação é o que deixa compliance ser dono da restrição sem ser dono da rule store.

### Regra + experimento

Experimento é a terceira costura, e a que time de pricing mais frequentemente camufla com priority de regra.

O padrão em que cheguei conceitualmente — e que tenho querido construir faz tempo — é tratar experimento como *camada de contexto* que o decision engine resolve antes do rule engine sequer rodar. O contexto de experimento diz: *pra essa request, as regras a considerar são {rule set padrão} mais {overlay de experimento pra ELAST-2025-Q3}, com o overlay do experimento tendo precedência nos campos de markup que toca*.

O rule engine então roda contra o rule set mesclado. O decision engine grava *quais* overlays de experimento estavam em escopo, pra que a explicação carregue a proveniência do experimento separada da proveniência da regra. Uma request que foi cobrada de 4% por causa de um experimento consegue ser distinguida, no nível da explicação, de uma request que foi cobrada de 4% por causa de uma regra padrão que por acaso é igual a 4%.

```go
type ExperimentContext struct {
    ActiveOverlays []RuleSetRef         // rule sets de overlay pra mesclar
    Treatments     map[string]string    // experimento → braço de tratamento
}
```

O contexto de experimento deixa produto ser dono dos experimentos sem produto ser dono da rule store. A rule store é a política padrão; o overlay de experimento é a perturbação. Os dois são versionados, os dois são explicáveis, os dois são reproduzíveis contra o snapshot.

## Quando a migração vale a pena

Três razões pragmáticas pra investir no decision engine, e uma razão pra postergar.

**Vale a pena** quando o rule engine tá sendo editado pra expressar coisa que não devia ter que expressar. Quando você encontra regra que consulta serviço externo na ação, ou regra cuja priority tá sendo usada como governança pra restrição, ou regra cuja condição codifica pertencimento a experimento. Cada um desses é preocupação de decision engine postergada vazando pra camada de regra.

**Vale a pena** quando explicação tá ficando mais difícil de ler. Explicação de rule engine lista as regras que dispararam. Explicação de decision engine lista regra, contribuição do modelo, check de restrição, e overlay de experimento. Quando a pergunta do auditor exige ler o source pra responder, a camada de explicação foi sobrecarregada.

**Vale a pena** quando o time começa a desenhar diagrama de arquitetura mostrando um componente chamado "o engine" com seta pra tudo. O "tudo" é o que o decision engine devia coordenar. Desenhar como uma caixa esconde a costura; os bugs moram na costura.

**Vale postergar** quando o regime permanente genuinamente é "fact entra, ação sai". Um time rodando um rule engine limpo pra uma superfície de pricing bem escopada não devia construir decision engine porque o padrão arquitetural tá na moda. Decision engine prematuro é pesado, caro, e imposto que todo time que toca o sistema paga. Constrói quando o rule engine começou a esticar; não antes.

## O caminho de migração

A migração mais limpa que estudei se move em três passos.

**Envolve, não substitui.** O decision engine vira um novo ponto de entrada de topo. Por dentro, chama o rule engine existente. A primeira versão não faz nada que o rule engine já não fizesse — só dá ao time um lugar pra adicionar a próxima preocupação. Wrapper é barato e deixa o time validar a costura sem reescrever.

**Tira a restrição primeiro.** Restrição é a preocupação mais fácil de extrair. Tem ownership clara, semântica simples (confere depois, limita ou rejeita), e reduz a superfície da rule store imediatamente. A primeira coisa que um decision engine deve fazer além do que o rule engine fazia é impor restrição.

**Adiciona as costuras de modelo e experimento por último.** Esses dois exigem mais desenho: como o valor do modelo entra na explicação, como o overlay do experimento mescla com o rule set padrão, como fica a trilha de auditoria. Construir terceiro significa que o time conviveu com o wrapper de decision engine por um tempo e sabe que formato a costura devia ter.

Faria nessa ordem se fosse fazer hoje. A migração que vivi seguiu uma ordem diferente, com mais dor e mais retrabalho. A lição que fica é a mesma: extrai a costura mais simples primeiro.

## A lição

Rule engine responde *o que casa*. Decision engine responde *o que deve acontecer*. O gap é real e nem sempre vale cruzar — mas quando vale, o custo de fingir que o rule engine basta é pago no tipo de bug que precisa de shadow mode pra pegar e replay pra defender.

A terça de manhã foi um incidente pequeno. O fix aconteceu no shadow, antes do cliente ver. Mas foi a primeira vez que tive que admitir que a camada que eu tinha construído — cuidadosa, correta, explicável — não era mais onde a decisão de fato morava. A decisão tinha subido um nível. A arquitetura precisava seguir.

A maior parte do valor da distinção é reconhecer cedo. Um time que nomeia a diferença entre *o que casa* e *o que deve acontecer* consegue postergar o decision engine de propósito, sabendo que o dia de construir vai chegar. Um time que não nomeia a diferença vai construir decision engine sem querer, acumulando preocupação no rule engine até o rule engine deixar de ser reconhecível como um.

## O que vem a seguir

O próximo post é sobre longo prazo. Sistema de pricing envelhece. Regra acumula. Engine é refatorado. Restrição muda. Experimento se aposenta. As camadas arquiteturais dessa série — modelo de regra, loader, matcher, evaluator, explicação, shadow, replay, decision engine — todas precisam de ciclo de vida. O próximo post é sobre construir esses ciclos desde o começo, pra que a plataforma que você shippa no ano um ainda seja operável no ano cinco.

Depois disso a gente vai pra metade retrospectiva da série. Dez erros que shippei. O que eu construiria diferente hoje. Os dois últimos posts são sobre o que essa série inteira tá preparando: a segunda vez que você constrói uma plataforma de pricing, com tudo que a primeira vez te ensinou.

Por enquanto, a lição é a distinção. Rule engine e decision engine não são a mesma coisa. O primeiro pergunta o que se encaixa; o segundo pergunta o que deveria ser. Uma plataforma de pricing que cresce a ponto de precisar do segundo é uma plataforma de pricing indo bem. O trabalho é reconhecer o momento, construir a costura, e não fingir que a pergunta maior é só uma versão mais difícil da menor.
