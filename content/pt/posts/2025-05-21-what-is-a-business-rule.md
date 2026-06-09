---
title: "O Que É Uma Regra de Negócio?"
subtitle: "Um markup de 3% parece igualzinho em código e em config — até a hora de explicar quem mudou, quando, e por quê."
author: helio
layout: post
date: 2025-05-21T10:00:00+00:00
series:
  - building-pricing-systems
series_order: 1
categories:
  - Engineering
  - Pricing
  - Architecture
tags:
  - pricing
  - business-rules
  - rule-engine
  - monetization
  - decision-systems
  - architecture
description: "Regra de negócio não é um if. É uma decisão que alguém precisa ter dono, auditar e explicar — e essa responsabilidade molda tudo que a gente constrói em volta."
---

Tem uns anos, peguei uma discussão de trinta minutos no Slack sobre se um markup de 3% pra reservas de última hora na Alemanha devia ficar num arquivo Go ou num YAML de config.

Os engenheiros tavam discutindo cadência de deploy. A PM tava discutindo dono da decisão. Ninguém na thread tava discutindo a pergunta que realmente importava, que era: quando esse número mudar no próximo trimestre, quem é o responsável por explicar a mudança?

Olhando hoje, foi nessa conversa que essa série começa. Regra de negócio não é um if. O if é o que a gente escreve *depois* que já sabe quem decidiu, quais são os inputs, o que a decisão significa, e como auditar. O if é a parte mais barata do sistema. Tudo em volta é o trabalho de verdade.

## A versão ingênua sempre parece razoável

A primeira versão de qualquer regra parece tranquila. Alguém escreve isso:

```go
func ApplyMarkup(market string, daysToDeparture int) float64 {
    if market == "DE" && daysToDeparture < 7 {
        return 0.03
    }
    return 0
}
```

É código bom. Roda. O teste passa. Sobe na sexta de tarde.

Duas semanas depois chega a segunda regra. Também Alemanha, também última hora, só que agora pra trem, e só no mobile. A função ganha o segundo branch. Seis meses depois são nove branches, três feature flags entrelaçadas no meio, e pelo menos um dev que evita silenciosamente mexer naquele arquivo porque o teste "se comporta estranho" quando você reordena qualquer coisa.

É nessa hora que a gente descobre que aquela regra nunca foi uma função. Era uma decisão que alguém no negócio tomou, e a função é o fóssil dessa decisão — precisa no momento em que foi escrita, mas sem nenhum dos contextos que permitiriam um leitor futuro raciocinar sobre ela. O sistema não tem ideia de que o markup de 3% é o mesmo tipo de coisa que a regra de trem-mobile. Pro runtime, são branches consecutivos. Pro negócio, são duas políticas separadas que mudam em ritmos diferentes e precisam ser auditadas por pessoas diferentes.

Aí piora quando o segundo time aparece. Marketing quer adicionar uma regra pra campanha. Receita quer outra regra que só dispara se o cliente abandonou um carrinho ontem. Cada um deles chega na porta do engenheiro pedindo "uma mudança pequena." Cada mudança pequena mexe na mesma função. A função vira o acerto de contas de três departamentos, e ninguém mais consegue ler.

## Três lugares onde essa mesma decisão pode morar

Tem um exercício útil que eu faço com os times quando aparece a pergunta "onde a regra vai morar?". A gente pega uma mudança proposta — digamos, o markup pra reservas de trem de última hora — e pergunta o que acontece se ela for parar em cada um de três lugares.

**Inline no código.**

- *O que é:* a regra é um branch de uma função no caminho quente.
- *Por que sim:* baixa cerimônia. Você lê a regra lendo o código. Teste é fácil.
- *Por que não:* herda a cadência de deploy do serviço. Toda mudança vira code review. O histórico da regra vive no `git blame`, ou seja, a linha do "por quê" some no momento em que o autor original esquece.

**Como config de runtime.**

- *O que é:* a regra é uma entrada num YAML ou JSON que o serviço carrega no boot.
- *Por que sim:* produto consegue mudar sem deploy. Auditoria é o histórico do arquivo. Teste pode rodar o serviço com um fixture de config.
- *Por que não:* config virou load-bearing pra regra de negócio sem ninguém perceber. Uma chave faltando no YAML é uma mudança tarifária em produção. Não tem schema, a menos que alguém tenha escrito um. E sem modelo, o arquivo vira uma sequência longa de strings mágicas.

**Como regra, num rule store, avaliada por um engine.**

- *O que é:* a regra é um artefato tipado com condições, ações, metadados e dono explícito, carregado por um rule engine que sabe matchear e explicar.
- *Por que sim:* a regra carrega contexto suficiente pra ser lida por quem não é engenheiro. Pode ser testada, versionada e aposentada. O engine cuida das coisas que são fáceis de errar: ordem, semântica de matching, explicabilidade.
- *Por que não:* agora você tem que construir (ou adotar) o engine. O artefato precisa ser desenhado. O vocabulário precisa ser combinado.

A maioria dos times, na minha experiência, vai parar na opção 2 sem querer. Começam na opção 1, surtam com a cadência de deploy, e enfiam YAML do lado sem nunca ter desenhado o que vai dentro do YAML. A estrutura do arquivo vira o que o primeiro engenheiro digitou. Um ano depois são mil linhas de string que ninguém confia.

Essa série é sobre chegar de forma deliberada na opção 3 sem fingir que o trabalho na opção 1 não ensinou nada.

## O que uma regra precisa carregar

Se eu tivesse que definir regra de negócio numa frase só, ia dizer que é *uma decisão que o negócio expressa numa forma que o sistema consegue avaliar*. Desmontando essa frase, uma regra carrega no mínimo seis coisas.

Uma **decisão** — o resultado de negócio que a regra produz. Um markup. Um desconto. Uma escolha de roteamento. A coisa pela qual a regra existe.

Um conjunto de **condições** — os inputs que decidem se a regra vale. Mercado, canal, tempo até a partida, segmento de cliente, hora do dia. O formato sob o qual a decisão se aplica.

Um conjunto de **ações** — o que concretamente acontece quando a condição bate. Setar um valor de markup. Escolher um provedor. Suprimir um experimento. A ação é o que o engine executa; a condição é contra o que o engine compara.

**Metadado** — a contabilidade que permite uma pessoa raciocinar sobre a regra depois. Quem escreveu. Quando. Por qual motivo. Qual ticket. Qual experimento. Sem metadado, a regra é anônima, e regra anônima é regra que não se aposenta com segurança.

**Ownership** — o time ou a pessoa responsável por manter a regra correta. Raramente fica escrito em código, mas precisa morar em algum lugar, senão a regra vai sobreviver a todo mundo que entendia ela.

E **intenção** — o porquê. A condição é *o que* a regra procura. A intenção é *o que* a regra está tentando expressar. Regra com condição e sem intenção é impossível de manter, porque qualquer mudança futura não tem contra o que ser conferida.

{{< plantuml title="Uma regra de negócio são seis artefatos, não um" >}}
@startuml
skinparam shadowing false
skinparam componentStyle rectangle
skinparam defaultFontName "Helvetica"

rectangle "Regra de negócio" as R {
  rectangle "Decisão\no resultado" as D
  rectangle "Condições\nquando se aplica" as C
  rectangle "Ações\no que acontece" as A
  rectangle "Metadado\nquando, onde, ticket" as M
  rectangle "Ownership\nquem responde" as O
  rectangle "Intenção\npor que existe" as I
}

C --> D : gateia
A --> D : produz
M ..> D : descreve
O ..> D : responde "quem"
I ..> D : responde "por quê"
@enduml
{{< /plantuml >}}

O mesmo markup alemão de última hora, escrito como coisa que carrega essas partes:

```yaml
id: short_lead_time_markup_de
name: "DE short lead-time markup"
intent: |
  Capturar demanda em reservas de janela curta na Alemanha,
  onde a restrição de capacidade reduz a sensibilidade a
  preço. O time revisou a curva de elasticidade no Q1 e
  acordou manter 3% até a próxima revisão de demanda.
owner: pricing-de
when:
  market: DE
  days_to_departure:
    less_than: 7
then:
  markup_percentage: 3.0
metadata:
  created: 2025-05-21
  ticket: PRICE-1473
  experiment: ELAST-2025-Q1
  review_after: 2025-11-21
```

Ainda não tem engine. Não tem loader. Não tem matcher. Mas o formato do artefato já é diferente do if. A intenção tá visível. O dono tá visível. A data de revisão tá visível. A condição é a menor parte do bloco.

## Regra vs código vs configuração vs modelo

Quem só viu regra numa forma única costuma achatar a distinção entre regra, configuração e modelo. Vale a pena separar de novo, porque cada um deles muda por um órgão diferente da empresa, e confundir é como esse órgão atrofia.

| Forma | Muda via | Auditada via | Testada com | Dono |
| --- | --- | --- | --- | --- |
| Código | Pull request, deploy | Histórico do git, code review | Teste unitário e de integração | Engenharia |
| Configuração | Config push, geralmente sem deploy | Histórico da config, se você manteve | Smoke test, em geral fraco | Engenharia ou plataforma |
| Regra | Edição de regra, em geral via UI ou pipeline | Histórico da regra, log de explicação | Teste comportamental contra facts | Time de negócio / domínio |
| Modelo | Re-treino, redeploy de pesos | Linhagem do dado de treino, métrica de avaliação | Scoring offline, monitoramento online | Data science |

Regra não é configuração. Configuração tuna um sistema que já sabe o que faz. Regra *expressa o que o sistema deve fazer*. O fato de as duas acabarem num YAML é coincidência de superfície — uma coincidência convincente o bastante pra eu ter visto time inteiro shippar regra como config por anos sem nunca perceber o que tava faltando.

Regra também não é modelo. Modelo aprende a decisão a partir de dado; regra declara a decisão a partir de intenção. Os dois mapeiam input pra output, mas só um deles dá pra discutir no nível de política. Markup de 3% é uma posição que alguém defende numa reunião. Markup de 2,74 saindo de um gradient boost é número que precisa ser ancorado em dado de avaliação antes de qualquer pessoa defender. Os dois cabem num sistema de pricing. Confundir é como você acaba com política que não consegue explicar.

A questão do modelo importa porque todo time que constrói rule engine, em algum momento, encontra o time que quer botar modelo atrás dele. O jeito mais limpo que vi isso funcionar é manter a regra como o *contrato* — a coisa que o negócio é dono, a coisa que é explicada — e deixar o modelo ser uma das implementações de ação por trás do contrato. A regra diz "aplicar o markup segmentado pra esse cliente"; o modelo decide qual o valor do markup. A regra continua dona do porquê.

## As quatro propriedades que uma regra precisa ter

Regra só é útil quando é determinística, inspecionável, testável e explicável. Cada uma dessas propriedades ganha o lugar dela.

### 1. Determinística

Dado o mesmo input, a mesma regra produz o mesmo output. Não tem negociação. No momento em que a regra depende de estado escondido ou do relógio sem nomear isso como input, ela deixa de ser regra e vira bug que vai esconder por semanas.

Na prática isso quer dizer que a regra precisa *receber* os facts. Não consultar. A mesma regra tem que rodar em produção, num teste, num replay contra o tráfego do trimestre passado, e num notebook na terça à tarde. O engine é a coisa que tem o relógio e o banco; a regra só tem o que o engine entregou.

Esse é o gerador do bug mais caro que eu já shippei num sistema de regras. Uma regra disparava num cliente "se ele não tivesse comprado antes." O check era uma chamada de banco, feita dentro da ação. Em hora calma tava rápido. Numa indisponibilidade regional ficou lento, depois ficou errado, depois cascateou. O fix não foi na regra. O fix foi no contrato: histórico do cliente é um fact, e fact é passado pra dentro.

### 2. Inspecionável

Você consegue ler a regra sem rodar ela. Consegue responder "o que essa regra diz?" sem subir engine, sem carregar fact de produção, sem grepar trace ID. A regra é, por si só, uma coisa que pessoa não-engenheira consegue olhar.

Inspecionabilidade é o que permite um time de domínio abrir um pull request contra uma regra e ter uma discussão que faz sentido. Se precisa ser engenheiro pra ler a regra, a regra é dona da engenharia, queira você ou não.

### 3. Testável

Você consegue escrever um teste que diz *dado os facts X, essa regra deve matchear e produzir Y*. O teste pertence à regra, não ao engine. Quando o engine muda de formato, o teste continua útil.

A forma de um bom teste de regra parece mais com uma asserção comportamental do que com um teste unitário. *Pra uma reserva alemã de última hora, a regra de markup de última hora deve disparar e contribuir com 3% ao markup total.* Essa frase se lê igual no código, num doc e num ticket. O teste de regra é o ponto onde os três convergem.

### 4. Explicável

Quando a regra dispara, o sistema consegue dizer por quê. Quando não dispara, o sistema consegue dizer qual condição falhou. O post depois do próximo dessa série é dedicado a explicabilidade, porque é a parte mais sub-construída da maioria dos sistemas de regras — mas começa aqui, na definição. Se a intenção da regra não tá escrita, a explicação não tem onde se ancorar.

O primeiro sistema de regras que construí era determinístico e inspecionável. Era mal testável. Não era explicável. Quando um número aparecia errado em produção, o único jeito de investigar era ler o source e raciocinar na mão. Regra acumulava mais rápido do que dava pra revisar, e a gente não conseguia aposentar nenhuma com segurança. O sistema envelheceu mal porque explicabilidade não foi desenhada desde o começo. Essa experiência é boa parte da razão dessa série existir.

## Onde regra falha com o tempo

Regra nasce clara. Apodrece sempre dos mesmos três jeitos.

Perde a intenção. O autor sai. O ticket vai pro arquivo. A linha de intenção no YAML é a única coisa segurando a regra viva, e ninguém mexe porque "tá funcionando." Cinco anos depois a regra ainda dispara, e ninguém no time sabe por quê, então ninguém ousa aposentar. É assim que sistema de regras acumula peso morto.

Sobrevive às condições dela. O mundo muda. O mercado que precisava do markup re-segmenta. A condição ainda bate, mas a política que ela expressava já não é mais verdade. A regra dispara mesmo assim, e alguém lá embaixo paga por isso.

Colide com outra regra. Duas regras casam com os mesmos facts. Uma foi escrita por pricing-DE, a outra por marketing. O engine escolhe uma delas, de algum jeito, e o outro time descobre por um dashboard de madrugada. A gente volta na semântica de matching daqui a alguns posts.

A defesa contra esses modos de falha tá no próprio artefato — no metadado, no dono, na data de revisão. Regra com `review_after` explícito é regra que o time concordou em olhar. Regra com `owner` explícito é regra que tem alguém pra perguntar. Regra com `intent` é regra que pode ser confrontada com o mundo pra qual foi escrita. Sem isso, a regra é anônima, e regra anônima ninguém aposenta; só faz workaround em volta.

## Um aviso do que vem a seguir

Eu não tô introduzindo rule engine de propósito. O próximo post da série é sobre o *modelo de regra* — a representação em memória, o formato dos campos, o trade-off entre estrutura tipada e schema genérico. Depois passamos por guardar regra como dado, fazer matching em escala, montar o pipeline de avaliação, testar tudo, deixar explicável, e aí entram tráfego sintético, shadow mode e replay.

O codebase de referência pro lado do engine dessa série é [`bre-go`](https://github.com/helmedeiros/bre-go), um rule engine em Go que eu mantenho. Implementa quatro engines in-process atrás de uma porta — insertion-order all-match, insertion-order first-match, priority-ordered first-match, e um matcher indexed sub-linear — e é de onde vêm a maioria dos exemplos de código do próximo post. Os posts de tráfego e replay mais à frente usam [`traffic-gen`](https://github.com/helmedeiros/traffic-gen), um binário Go pequeno que sintetiza requisição realista de pricing em QPS e mix de persona configuráveis.

A lição daqui é menor do que um engine. Antes de você escrever uma única linha de matcher, pergunta se o artefato que você tá produzindo é mesmo uma regra. Regra tem decisão. Regra tem condição. Regra tem ação. Regra tem metadado. Regra tem dono. Regra tem intenção.

Se falta qualquer uma, o que você tem é um if que alguém vai ter que explicar daqui a um ano, sem ajuda. É assim que a maioria dos sistemas de pricing vira inmantível silenciosamente. O resto da série é sobre fazer do outro jeito.
