---
title: "Construindo Sistemas de Pricing que Envelhecem Bem"
subtitle: "O trabalho de manutenção é real. A gente vinha fazendo na mão. Esse post é o formato de empurrar isso pra dentro do decision engine pra que o operador do ano três não dependa do engenheiro do ano um lembrando."
author: helio
layout: post
date: 2025-11-19T10:00:00+00:00
series:
  - pricing-engineering
series_order: 12
categories:
  - Engineering
  - Pricing
  - Architecture
tags:
  - pricing
  - maintainability
  - lifecycle
  - architecture
  - observability
  - operations
description: "Sistema de pricing não falha quando é construído. Falha no terceiro ano, quando ninguém lembra por que metade das regras existe. O time com quem trabalhei vinha segurando o ciclo de vida na mão — revisão trimestral, aposentadoria manual, script de migração ad-hoc. Esse post é o que venho explorando pra empurrar esse trabalho pra dentro do decision engine."
---

Tem uma regra em algum lugar de todo sistema de pricing que vem disparando há anos e que ninguém no time entende.

A minha se chamava `legacy_compensation_override`, última edição em 2019, disparando em uns 0,3% do tráfego. Ninguém no time dono do engine de pricing em 2023 tava lá em 2019. A mensagem de commit dizia "ver TICKET-1481"; o sistema de ticket tinha sido migrado duas vezes e TICKET-1481 já não resolvia mais. A regra era determinística, inspecionável e testada. A única coisa que ninguém conseguia responder era se deveria continuar existindo. A gente deixou em paz. Provavelmente ainda tá disparando.

Essa é uma de três regras que eu, pessoalmente, tive medo de deletar. Entre os times com quem trabalhei, o número é bem maior. O padrão é o mesmo: a regra estava correta quando foi escrita, o mundo pra qual foi escrita mudou, o autor se foi, e não tem procedimento de aposentadoria que o time atual confie. A regra sobrevive à razão da regra.

O time com quem trabalhei em pricing vinha segurando esse tipo de degradação na mão. Rodávamos revisão trimestral de ownership numa planilha. Rastreávamos deprecação num canal de Slack e num doc de tracking. Escrevíamos script de migração caso a caso quando um schema precisava mudar. As práticas funcionavam, mais ou menos, enquanto a gente lembrava delas e enquanto quem construiu seguia por perto. Funcionavam menos bem quando alguém que não tinha rodado a revisão original precisava tocar a próxima.

Esse post é o que venho explorando desde então: como empurrar essas práticas das mãos do time pra dentro do próprio decision engine, pra que o operador do ano três não dependa do engenheiro do ano um lembrar de olhar a planilha. As práticas são reais. A automação é a metade-design que eu não terminei de construir, e escrever é o jeito mais barato de descobrir o que ainda não vi.

## Cinco moedas que envelhecem

Sistema de pricing paga cinco tipos de dívida ao longo do tempo. Cada uma se acumula em silêncio. Cada uma tem que ser desenhada contra — e na maioria delas, na plataforma em que trabalhei, vinha sendo segurada por higiene manual em vez de por algo que o engine em si fizesse.

**Regra parada.** Regra que ninguém é dono, ninguém revisa, e ninguém ousa aposentar. O fator que acumula é medo: toda regra morta que alguém tem medo de deletar deixa a próxima regra morta um pouquinho mais segura de deixar em paz. O custo é em tempo de investigação — todo incidente precisa considerar toda regra que poderia ter disparado, incluindo as que ninguém entende.

**Schema drifa.** O schema YAML do ano um não é o schema do ano três. Campo novo é adicionado. Campo velho deixa de ter significado. O loader carrega parser pra toda versão que já viu, porque em algum lugar do repo tem um arquivo que não é tocado desde 2021 e ainda tem que carregar. O fator que acumula é complexidade do loader.

**Ownership apodrece.** O time que escreveu a regra muda pra outro time. O dono de produto muda pra outro produto. O metadado ainda diz `owner: pricing-de`, mas pricing-de foi reorganizado dezoito meses atrás e nem existe mais. O fator que acumula é atrito de escalação — pergunta sobre regra velha rota pra ninguém.

**Restrição infla.** Teto regulatório é adicionado. Piso de fairness é adicionado. Cap por cliente é adicionado. Cada restrição é correta individualmente; em agregado, apertam o espaço de decisão até regras que costumavam disparar livremente não conseguirem mais. O fator que acumula é supressão silenciosa — regra para de disparar não porque foi aposentada, mas porque restrição cortou.

**Telemetria erode.** Os dashboards do ano um não casam mais com o sistema do ano três. Os alarmes que importavam no lançamento agora são falso positivo. Os gráficos que importavam no fim de trimestre foram otimizados pro mix do ano passado. O fator que acumula é cegueira operacional — o time opera com dashboard que não descreve mais o sistema.

Cada uma dessas é categoria de degradação. Nenhuma é dramática. Todas, juntas, são por que sistema de pricing fica ilegível no ano cinco.

## Regra parada: desenhe pra aposentadoria

O que a gente fazia, no time com quem trabalhei, era carregar a disciplina na cabeça. Sabíamos quais regras eram antigas. Sabíamos em quais não tínhamos visto disparar. Uma vez por trimestre, alguém (muitas vezes eu) caminhava pela rule store numa planilha, pedia aos times donos pra confirmar o que ainda queriam, e podava. Funcionava. Também dependia de eu lembrar de começar a revisão, dos times certos responderem e-mail, e de ninguém no time que entrasse depois pular um trimestre.

O formato que venho explorando empurraria isso pra dentro do artefato da regra e do loader. Três propriedades da regra, do Post 1, mereceriam o destaque.

**`review_after`.** Toda regra carregaria uma data até a qual tem que ser olhada. A data não é prazo; é *prompt*. Quando o loader nota uma regra cujo `review_after` passou, emite um warning. O warning aparece no dashboard. O time dono recebe notificação. A regra não para de disparar — isso seria outro tipo de bug — mas o sistema oficialmente pediu ao time pra confirmar se a regra ainda é desejada.

```yaml
metadata:
  created: 2023-02-15
  ticket: PRICE-1473
  owner: pricing-de
  review_after: 2023-08-15
```

A parte difícil é a cultural: o time tem que de fato agir no prompt. A metade-sistemas do problema é tornar o prompt impossível de ignorar, o que a planilha de revisão manual nunca chegou a ser.

**Observabilidade de hit rate.** Regra que não dispara há seis meses é candidata à aposentadoria. O time teria que saber quais regras dispararam e quais não. O log de explicação do Post 7 já carrega a informação — todo Execute grava o nome das regras que dispararam — mas na plataforma em que trabalhei, a gente consultava ad-hoc quando queria saber, não em cadência. O formato que eu construiria é um job diário que agrega sobre as explicações e produz um relatório de *zero-fire*.

```
REGRAS ZERO-FIRE (últimos 90 dias)
regra                                 último disparo    owner
legacy_compensation_override          2024-03-12        pricing-de (vago)
italian_summer_2023_promotion         2024-08-30        marketing
weekend_routing_fallback              nunca             platform

REGRAS ÓRFÃS (owner sem mapeamento atual de time)
regra                                 owner declarado
legacy_compensation_override          pricing-de
holiday_promotion_2022                pricing-experiments
```

Regra que não dispara num trimestre não está necessariamente errada; pode ser a rede de segurança que ativa uma vez por ano. Mas regra que não dispara num trimestre *e* cujo `review_after` passou *e* cujo owner não existe mais é regra que o time quase certamente consegue aposentar.

**Aposentadoria como operação de primeira classe.** O padrão que venho esboçando faz de *desabilitar* uma regra uma operação de primeira classe, com metadado que sobrevive ao disable. Do Post 2, `Enabled: false`. Regra desabilitada não dispara; ainda aparece no log de explicação como "disabled" pra que investigação consiga ver; carrega `disabled_at` e `disabled_by` e uma razão. Depois de noventa dias desabilitada sem incidente, a regra pode ser apagada inteira.

```yaml
- id: legacy_compensation_override
  enabled: false
  disabled_at: 2024-11-19
  disabled_by: pricing-platform
  disabled_reason: |
    Não disparou em 90 dias. Time owner original (pricing-de)
    reorganizado no Q2 2023. Nenhum stakeholder ativo
    identificado. Desabilitando agora; deleção agendada pra
    2025-02-17 se não aparecer regressão.
```

A aposentadoria em dois estágios — desabilita, depois apaga — é a resposta prática pro medo do time. Desabilitar é reversível. Apagar depois de noventa dias desabilitada é procedimento, não salto. Tomamos esse tipo de decisão em retro várias vezes. O que eu quero é que o próprio sistema exponha o candidato, agende o disable, e lembre o time quando a data de deleção chegar, em vez de depender de alguém reabrir a planilha.

## Evolução de schema: mantém a versão, aposenta o parser

O Post 3 introduziu `version: 1` no topo de todo arquivo de regra. A disciplina que isso habilitou é o que torna evolução de schema sobrevivível por anos. A gente tinha isso — todo arquivo de regra carregava versão. O que a gente não tinha era ferramenta de migração. Cada mudança de schema era seu próprio script de migração, escrito ad-hoc por quem tava fazendo a mudança, revisado por um grupo pequeno de engenheiros que tinha contexto.

Três regras em que vim acreditar enquanto penso no desenho:

**Toda mudança de schema deveria ser aditiva primeiro.** Campo novo é opcional com default. Campo renomeado é suportado nos dois nomes por uma versão de schema. Campo removido é depreciado por uma versão de schema antes de ser removido. O loader roda na mesma versão pra arquivo nos dois schemas; arquivo velho segue carregando. A gente tentava seguir no espírito; o desenho imporia.

**Toda versão de schema deveria ter data explícita de aposentadoria.** O arquivo de termo do schema (`schemas/v2.md`) carregaria a versão, a data de introdução, e a data de `retire_after`. Depois da data de aposentadoria, o loader recusaria carregar arquivo daquela versão; o time tem que migrar. A gente não tinha isso — versão antiga ficava carregável indefinidamente, e o loader carregava parser que já podia ter sido dispensado.

**Migração deveria ser ferramenta, não trabalho manual.** Uma ferramenta de migração lê arquivo na versão N e escreve arquivo na versão N+1. A ferramenta é escrita quando a versão nova do schema sobe. Times donos de arquivo velho rodam a ferramenta, revisam o diff, commitam o arquivo migrado. Isso é o que eu construiria primeiro, porque é a peça que faltava e que nossos scripts ad-hoc ficavam reconstruindo.

```sh
# Migra todo arquivo no diretório rules/ de v1 pra v2.
$ ruleset-migrate --from v1 --to v2 rules/

  migrado rules/de-markups.yaml          v1 → v2
  migrado rules/fr-markups.yaml          v1 → v2
  inalterado rules/compliance-de.yaml    já v2
  falha   rules/legacy-experiments.yaml  não parseou v1

Resumo: 14 migrados, 3 inalterados, 1 falhou
```

Uma ferramenta de migração é o contrato entre versões de schema. Enquanto existir e rodar, o time consegue mudar o schema sem prender nenhum arquivo histórico. O dia em que o schema muda sem ferramenta de migração correspondente é o dia em que o schema começa a juntar dialeto não intencional — que é mais ou menos o que aconteceu no nosso sistema mais de uma vez.

## Ownership: nomeia, prova

O campo `owner` é a afirmação da regra sobre quem responde por ela. A afirmação tem que ser verdade pra que a regra seja defensável. Na plataforma em que trabalhei, a afirmação era às vezes verdadeira e às vezes fóssil de um time que tinha sido reorganizado. A gente sabia qual era qual porque carregava o mapeamento na cabeça. A passagem, quando alguém novo entrava, era conversa, não artefato.

O sistema que ganharia a afirmação tem duas peças.

**Um diretório vivo de owner.** Um serviço pequeno ou arquivo que mapeia identificador de owner (`pricing-de`, `marketing-eu`, `platform`) pro time atual. O mapeamento tem que ser mantido atualizado — toda reorganização de time atualiza o diretório. O loader faz cross-reference; regra cujo `owner` não tá no diretório atual gera warning no load.

```yaml
# owners.yaml — versionado, revisado, atual
pricing-de:
  team: Pricing Alemanha
  manager: maria.santos@exemplo.com
  slack: #pricing-de
  active: true
  successor: null    # se reorganizado: quem herda

pricing-experiments:
  team: Pricing Experimentos
  manager: null
  slack: #pricing-experiments
  active: false
  successor: pricing-platform
```

Quando um time é dissolvido, o campo `successor` capturaria quem herda as regras dele. O loader, encontrando regra que pertence a time inativo, redireciona o warning pro sucessor. A ownership original é preservada no metadado; a escalação viva vai pra algum lugar que humano lê. A gente fazia isso informalmente — alguém do platform sempre herdava os órfãos — mas não tinha um jeito de *provar* a herança pra um operador novo. O diretório é a prova.

**Revisão periódica de ownership.** Uma vez por trimestre, todo time recebe a lista de regras de que é dono. O time confirma quais ainda quer, quais aposentaria, quais herdou e não reconhece. O output é uma lista pequena de ticket — desabilita essas três, transfere essas duas pra outro time, mantém o resto. Cadência trimestral é rápida o bastante pra pegar reorganização e lenta o bastante pra não ser imposto.

A gente rodou essa revisão na mão por vários trimestres. Era o ritual operacional mais útil que o time tinha. Era também o mais provável de ser pulado quando alguém novo entrava e não sabia que existia. A automação que eu construiria é pequena: um job agendado que caminha pela rule store, agrupa por owner, e manda e-mail pra cada time dono com a lista e um prazo. A parte difícil é a revisão cultural; o sistema consegue carregar a cadência.

## Deprecação: processo, não adeus

Aposentar uma regra é decisão. Aposentar um *tipo de regra* — uma classe inteira de ação, um campo de schema, uma política de composição — é projeto. Deprecação é a disciplina que te leva de "a gente não deveria estar usando isso mais" até "a gente não está usando isso mais" sem quebrar cliente no meio.

A gente fez isso no nosso sistema na mão. Cada deprecação morava num documento de tracking, com uma contagem manual de usos restantes puxada de query de log a cada duas semanas, e uma noção aproximada de quando a deleção ia chegar. O trabalho era real; só não era maquinaria estruturada.

As quatro fases que eu automatizaria:

**1. Anuncia.** A deprecação é publicada. A razão é publicada. O substituto é publicado. A data de aposentadoria é publicada. O dashboard ganha uma métrica de uso da coisa depreciada.

**2. Alerta.** O sistema emite warning toda vez que a coisa depreciada é usada. Warning carrega URL do documento de deprecação. A taxa de warning vira o KPI do time pra deprecação — a curva tem que cair antes da data de aposentadoria.

**3. Erro.** Algumas semanas antes da data de aposentadoria, warning vira erro. Teste falha. CI impede uso novo. Uso existente ainda funciona, mas o sistema fica mais alto sobre.

**4. Remove.** A data de aposentadoria chega. A coisa depreciada é deletada do codebase. A ferramenta de migração lá de cima desse post é a rede de segurança pra arquivo que ainda referencia a coisa deletada.

```
CRONOGRAMA DE DEPRECAÇÃO: tipo de ação `legacy_compensation`
  anunciada       2024-08-15
  warn  começa    2024-09-15
  erro  começa    2025-01-15
  data aposent.   2025-02-15

tendência de uso (últimos 90 dias)
  2024-08    2.481 usos/dia
  2024-09    1.890 usos/dia      (warning começa)
  2024-10    1.103 usos/dia
  2024-11      612 usos/dia
  2024-12      198 usos/dia
  2025-01       47 usos/dia      (erro começa)
  2025-02        2 usos/dia      (alvo: 0)
```

O cronograma seria publicado. A tendência seria pública. A conversa que leva à aposentadoria não é "deveríamos?" — isso aconteceu no anúncio — mas "está no caminho?". A decisão é tomada uma vez; o trabalho operacional é a curva. A gente tinha essa conversa mais ou menos do jeito certo, mas fazia a partir de um doc de tracking e de uma query que alguém precisava lembrar de rodar, não a partir de um dashboard que o sistema mantinha.

## Inflação de restrição: limite o limite

Restrição é mais fácil de adicionar do que regra. Cada uma é correta individualmente. O agregado é o que vira problema. A gente adicionou restrição ao longo dos anos por razão legítima — cap regulatório, piso de fairness, desconto total máximo por cliente por trimestre — e nunca teve um momento em que alguém perguntou quais ainda importavam.

Duas práticas que eu construiria no sistema.

**Toda restrição tem owner e data de revisão.** Mesmo formato das regras. O cap regulatório de 2022 pode não ser o mesmo cap do ambiente regulatório de 2025. O piso de fairness de um conjunto de suposições de cliente pode não ser o piso certo pro próximo conjunto. Restrição herdaria a disciplina de ciclo de vida da regra.

**A pilha de restrição é observável.** Um dashboard mostraria, pra cada restrição, com que frequência ativou (cortou ou rejeitou) no último trimestre. Restrição que nunca ativa não tá fazendo trabalho; o time consegue investigar se o mundo mudou ou se a restrição sempre foi redundante. Restrição que ativa em 30% do tráfego é restrição que tá moldando o sistema de um jeito que a rule store não enxerga; o time tem que entender por quê.

```
ATIVAÇÃO DE RESTRIÇÃO (últimos 90 dias)
restrição                       ativou          % das decisões
regulatory_cap_de               412             0,014%
fairness_per_customer_quarter   1.820           0,061%
never_below_cost                23              0,001%
legacy_2022_compensation_floor  0               0,000%   ← investigar
max_total_discount              7.901           0,264%
```

A linha de zero ativação seria a restrição que ficou pra trás. Ou ficou pra trás gracilmente — o mundo passou — ou é bug que ninguém tá exercitando. De qualquer forma, restrição que não faz trabalho por 90 dias é restrição pra investigar, não pra deixar em paz. A gente tinha restrição que eu quase tenho certeza não tava fazendo trabalho, no nosso sistema, e não tinha jeito automatizado de expor; o desenho acima é o que teria pegado.

## Telemetria: construa pro leitor do ano três

Dashboard envelhece. O formato que sobrevive é o desenhado pra quem entra no time no ano três, não pra quem construiu o sistema no ano um.

Três propriedades de dashboard que envelheceram bem pra mim — e que a gente *fez*, no time, com disciplina variada:

**Cada painel nomeia o que mede, em palavras de negócio.** "p99 da latência do Execute, ms" é engenharia. "p99 do tempo de decisão de markup, ms" é o mesmo número, nomeado em palavra de negócio. O leitor do ano três não sabe o que é `Execute`. Sabe o que é uma decisão de markup. Alguns dos nossos painéis faziam isso. A maioria não.

**Todo painel tem superfície de anotação.** Quando uma restrição é mudada, quando uma regra é aposentada, quando um experimento sobe, os painéis carregam uma anotação marcando a data. A anotação é mecânica — o sistema de deploy escreve — mas humano consegue ler o gráfico e conectar a curva à causa sem escavar git. A gente fazia isso manualmente pra lançamento grande e quase nada pra cauda longa de mudança pequena.

**Painéis morrem explicitamente.** Painel que não é mais útil é deletado, não silenciosamente rebaixado pro fim da página. Dashboard com um painel importante e vinte parados é pior que dashboard com cinco painéis importantes. Deleção é prática. Esse foi o que a gente fez pior. Painel acumulou.

A mais difícil das três é a última. Deletar painel parece perda de informação. A informação tá no data store; o painel é a *interpretação*. Interpretação obsoleta atrapalha leitura; não preserva nada.

## O runbook: o manual de operação do ano três

Toda plataforma de pricing devia shippar com um runbook que o operador do ano três consegue ler. O runbook é a peça desse post que é quase inteiramente sobre prática em vez de automação — e é a que a gente acertou mais consistentemente.

Um formato útil:

```
RUNBOOK DA PLATAFORMA DE PRICING
================================
1. Visão geral da arquitetura          (uma página)
2. Os cinco componentes e seus donos
3. A explicação: como ler uma          (com exemplo anotado)
4. A snapshot store: como consultar um snapshot
5. Incidente comum e seu playbook:
   - "esse cliente foi cobrado errado"
   - "a rule store não carrega"
   - "taxa de divergência do shadow disparou"
   - "p99 do Execute cruzou o limite"
6. Status de deprecação (deprecações atuais e seus cronogramas)
7. Link do diretório de owner
8. Cadência de revisão trimestral
9. Como aposentar regra (procedimento de dois estágios)
10. Como adicionar restrição (rollout em quatro fases)
```

Runbook não é o conhecimento tribal do time; é a *transição* de tribal pra escrito. O teste de um runbook bom é se alguém que entrou no time ontem consegue resolver incidente de rotina lendo. O teste de um runbook ruim é se a pessoa em on-call tem que acordar alguém pra interpretar.

Escrevi vários. Os que envelheceram bem foram os escritos pelo operador, não pelo arquiteto. O arquiteto escreve o que o sistema *faz*. O operador escreve o que *fazer quando se comporta mal*. Os dois são valiosos. O segundo é pra que o runbook serve.

## Ciclo de vida como desenho, não depois

Se eu tivesse que comprimir esse post numa frase, é o subtítulo em prosa: o trabalho de manutenção é real, a gente vinha fazendo na mão, e a metade-design que venho explorando é como empurrar pra dentro do decision engine pra que a prática sobreviva às pessoas.

Concretamente, o que eu construiria:

- Toda regra carrega `review_after` e `owner` no momento em que é escrita. O loader emite warning quando a data de revisão passa. A gente fazia isso na mão.
- Todo schema tem `retire_after` e ferramenta de migração no momento em que sobe. A ferramenta de migração é a rede de segurança. A gente escrevia script caso a caso.
- Toda restrição tem o mesmo ciclo de vida que regra, com dashboard de ativação. A gente não rastreava isso.
- Todo painel de dashboard pode ser morto. Matar é prática. A gente fazia isso mal.
- Todo time tem revisão trimestral do que é dono, automatizada como e-mail agendado. A gente fazia na mão, irregularmente.
- O runbook é shippado com o sistema, não depois. A gente fazia bem.

Nada disso é dramático. Tudo isso se acumula. Plataforma de pricing construída com essas propriedades em mente desde o dia um é uma que, no ano cinco, ainda é operável por um time que não construiu. Plataforma de pricing construída sem é a plataforma que alguém vai ter que reescrever. A gente tava mais perto do segundo caso do que eu gostaria, travada por práticas manuais que dependiam das pessoas que conheciam.

## O que vem a seguir

O próximo post é uma retrospectiva pessoal: dez erros que shippei construindo plataforma de pricing. Vários deles são a falha cultural de não tornar as práticas desse post sistêmicas. Otimização prematura, abstração errada na camada errada, falsa confiança vinda de teste verde — e confiar que higiene manual escala quando o time roda.

O post final é o que eu construiria diferente hoje, com tudo que a primeira vez me ensinou. Esse é o post pra qual a série inteira tá se preparando. É também o mais curto, porque pela hora em que você leu tudo que veio antes, a resposta é principalmente compressão.

## A lição

Os sistemas de pricing que shippei e envelheceram bem tinham três coisas em comum. Tinham owner explícito. Tinham data de revisão. Tinham procedimento de aposentadoria. Os sistemas de pricing que envelheceram mal eram os que estavam *corretos* no lançamento e não foram desenhados pra ser *operáveis* no ano três.

A gente fez o trabalho de operabilidade no nosso sistema na mão. Era trabalho real, era trabalho bom, e era frágil porque dependia das pessoas que faziam. O desenho que venho escrevendo nesse post é a metade que carregaria o trabalho das pessoas pro sistema. Não terminei de construir. A razão de escrever é a mesma do Post 10: é o jeito mais barato de descobrir o que não vi antes de me comprometer a construir pra valer.

A regra de 2019 que ninguém explica é uma falha pequena. A rule store meio cheia de regra desse tipo é o modo de falha que plataforma de pricing escorrega em silêncio. A defesa é o ciclo de vida, e o ciclo de vida tem que morar em algum lugar — ou na cabeça do time, onde depende do time ficar, ou no sistema, onde sobrevive às pessoas. O trabalho é mover do primeiro lugar pro segundo.
