---
title: "Testando Regras de Negócio"
subtitle: "Teste que prende as entranhas do engine apodrece. Teste que prende o comportamento de negócio sobrevive a todo refactor que você shippar."
author: helio
layout: post
date: 2025-10-22T10:00:00+00:00
series:
  - building-pricing-systems
series_order: 6
categories:
  - Engineering
  - Pricing
  - Architecture
tags:
  - pricing
  - business-rules
  - testing
  - golden-tests
  - property-based-testing
  - go
description: "A maioria dos testes de rule engine protege detalhe de implementação e deixa o comportamento de negócio drifar silenciosamente. Esse post é sobre os tipos de teste que pegam o bug que importa."
---

O badge de CI ficou verde por quatorze meses. O dashboard mostrava a mesma coisa.

Aí alguém perguntou por que uma reserva alemã específica tinha sido cobrada de 5% de markup em vez de 3%, e a resposta acabou sendo que o engine tinha calculado markup errado por nove meses. Não catastroficamente errado. Cem pontos-base de fora numa fatia de tráfego em que ninguém tinha pensado em alarmar. A suíte de teste, com 11 000 linhas àquela altura, tinha passado todo esse tempo.

Eu li teste por teste daquela suíte. Cada um era um teste perfeitamente razoável. Testavam que o matcher retornava as regras que devia. Testavam que a ação rodava. Testavam que o loader rejeitava YAML malformado. Nenhum testava que, dada uma reserva alemã dentro de uma janela curta, o cliente era cobrado de 3%.

A suíte tava protegendo o engine. Não tava protegendo o comportamento de negócio. Essa distinção é o resto desse post.

## Duas camadas, duas intenções

Um sistema de regras tem duas camadas que parecem iguais no código e se comportam completamente diferente quando você tenta testar.

A camada do engine — matcher, evaluator, executor, composer — é o que roda as regras. É majoritariamente estável. Muda quando alguém refatora uma estrutura de dado, troca um adaptador ou sobe uma interface. Quando a camada do engine muda, os testes que prendem as entranhas dela quebram.

A camada das regras — o que cada regra deve fazer pro negócio — é o que muda direto. Regra nova entra. Regra velha é editada. Priority é renegociada. Quando a camada das regras muda, os testes que prendem o comportamento de negócio *não devem* quebrar, a não ser que a mudança nas regras seja também mudança no acordo de negócio.

A suíte de 11 000 linhas era quase inteiramente teste da camada do engine. Não tinha nada protegendo o acordo de negócio. O engine podia se refatorar com confiança e o dashboard podia estar errado, e os dois podiam estar simultaneamente bem na visão de mundo da suíte.

O enquadramento em que cheguei: a camada do engine merece *unit test e teste de propriedade*. A camada das regras merece *teste comportamental e teste golden*. Os dois têm tempos de vida diferentes e formatos diferentes.

## Teste comportamental: o contrato que o negócio assinou

O primeiro teste que você deve escrever pra qualquer regra é o teste que prende o que o negócio acordou.

```go
func TestGermanShortLeadTimeMarkup(t *testing.T) {
    t.Parallel()
    store := loadRuleStore(t, "fixtures/2025-q3.yaml")

    ex := exec.New[Booking, Price](store.Engine())
    price, matched, err := ex.Execute(context.Background(), Booking{
        Market:           "DE",
        DaysToDeparture:  4,
        Channel:          "rail",
        BasePrice:        100.00,
    })

    if err != nil {
        t.Fatalf("execute: %v", err)
    }
    if !slices.Contains(matched, "short_lead_time_markup_de") {
        t.Errorf("esperava short_lead_time_markup_de disparar; veio %v", matched)
    }
    if price.Markup != 3.0 {
        t.Errorf("esperava markup 3.0; veio %.2f", price.Markup)
    }
}
```

Esse teste se lê como uma frase em que o time concordou. *Pra uma reserva alemã de trem a quatro dias da partida, o short-lead-time markup dispara e aplica 3%.* Não importa qual adaptador o engine usa. Não importa como o matcher é implementado. Não importa se a ação é função ou entrada de catálogo tipada. Importa que, dado os facts que o negócio acordou serem interessantes, o engine produz a resposta que o negócio acordou estar correta.

É também o teste que sobrevive a todo refactor. Quando alguém troca o matcher linear pelo indexed, esse teste segue passando. Quando o engine ganha um estágio novo, esse teste segue passando. Quando o loader muda o schema YAML, esse teste só falha se a intenção autoral da regra muda — que é exatamente quando você *quer* que ele falhe.

Três propriedades tornam esse teste útil:

**Os facts são realistas.** O struct Booking é o que o call-site de fato produz. Não um `map[string]string` sintético com três campos. O teste tá downstream do wrapper exec tipado, então exercita o marshaller também.

**A asserção é o acordo de negócio.** *Cobra 3%.* Não *o matcher retorna a regra índice 7*. A primeira sobrevive ao engine; a segunda quebra na próxima vez que alguém muda como as regras são indexadas por dentro.

**O fixture é nomeado pela versão do rule set.** `2025-q3.yaml`. Quando as regras mudam no próximo trimestre, um fixture novo é adicionado; o teste velho ainda passa contra o fixture velho; o time vê de relance qual teste prende qual acordo.

## Teste table-driven pra largura

O teste comportamental acima prende um cenário. O negócio tem dezenas, e escrever cada um na mão é como a suíte fica tediosa e como cenário é esquecido.

Teste table-driven é o formato certo:

```go
func TestPricingScenarios(t *testing.T) {
    store := loadRuleStore(t, "fixtures/2025-q3.yaml")
    ex := exec.New[Booking, Price](store.Engine())

    tests := []struct {
        name           string
        booking        Booking
        expectMatched  []string
        expectMarkup   float64
    }{
        {
            name:          "DE short lead-time, reserva trem",
            booking:       Booking{Market: "DE", DaysToDeparture: 4, Channel: "rail"},
            expectMatched: []string{"short_lead_time_markup_de", "germany_baseline_markup"},
            expectMarkup:  5.0, // 3% curto + 2% baseline, política sum
        },
        {
            name:          "DE long lead-time, reserva trem",
            booking:       Booking{Market: "DE", DaysToDeparture: 21, Channel: "rail"},
            expectMatched: []string{"germany_baseline_markup"},
            expectMarkup:  2.0,
        },
        {
            name:          "FR baseline",
            booking:       Booking{Market: "FR", DaysToDeparture: 14, Channel: "rail"},
            expectMatched: []string{"france_baseline_markup"},
            expectMarkup:  1.5,
        },
        {
            name:          "compliance override bate em tudo",
            booking:       Booking{Market: "DE", DaysToDeparture: 4, RegulatedMarket: true},
            expectMatched: []string{"compliance_markup_override"},
            expectMarkup:  0.0,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel()
            price, matched, err := ex.Execute(context.Background(), tt.booking)
            if err != nil { t.Fatalf("execute: %v", err) }

            if !equalStringSets(matched, tt.expectMatched) {
                t.Errorf("matched difere:\n  veio:    %v\n  esperava: %v", matched, tt.expectMatched)
            }
            if math.Abs(price.Markup-tt.expectMarkup) > 0.001 {
                t.Errorf("markup difere: veio %.2f, esperava %.2f", price.Markup, tt.expectMarkup)
            }
        })
    }
}
```

A tabela é a superfície de teste que o time de produto revisa. Os nomes leem como título de ticket. O booking é a request. A expectativa é o acordo. Quando cenário novo aparece num PR, o diff é uma linha. Quando cenário muda de sentido, o diff é uma coluna numa linha.

Teste table-driven carrega uma armadilha: a tentação de botar detalhe de implementação na tabela. No momento em que a tabela começa a checar *em quais buckets o engine indexed hasheou*, a tabela parou de ser artefato de negócio. Mantenha a tabela do lado do acordo — fact entra, decisão sai.

## Teste golden pra explicação

O estágio Execute do Post 5 produz uma Explanation. A Explanation é o segundo artefato que vale prender, porque mudança na Explanation é mudança no que o time consegue debugar.

O padrão:

```go
func TestPricingExplanationsGolden(t *testing.T) {
    store := loadRuleStore(t, "fixtures/2025-q3.yaml")
    engine := store.Engine()

    cases, err := filepath.Glob("testdata/scenarios/*.json")
    if err != nil { t.Fatal(err) }

    for _, scenario := range cases {
        name := strings.TrimSuffix(filepath.Base(scenario), ".json")
        t.Run(name, func(t *testing.T) {
            req := loadRequest(t, scenario)
            result, explanation, err := engine.ExecuteWithExplanation(context.Background(), req)
            if err != nil { t.Fatalf("execute: %v", err) }

            got := canonicaliseExplanation(result, explanation)
            golden := "testdata/golden/" + name + ".json"

            if *update {
                writeJSON(t, golden, got)
                return
            }
            wantBytes, err := os.ReadFile(golden)
            if err != nil { t.Fatalf("lê golden: %v", err) }

            if diff := jsonDiff(wantBytes, got); diff != "" {
                t.Errorf("explanation difere (-quer +veio):\n%s\n\nroda com -update pra aceitar", diff)
            }
        })
    }
}
```

O arquivo golden fica assim:

```json
{
  "result": {
    "markup_percentage": 5.0,
    "matched": ["short_lead_time_markup_de", "germany_baseline_markup"]
  },
  "evaluations": [
    {"rule": "compliance_markup_override", "outcome": "failed_condition", "failed_at": "when.regulated_market.eq"},
    {"rule": "short_lead_time_markup_de", "outcome": "fired"},
    {"rule": "germany_baseline_markup", "outcome": "fired"},
    {"rule": "france_baseline_markup", "outcome": "failed_condition", "failed_at": "when.market.eq"}
  ],
  "composer": "additive_with_compliance_override",
  "snapshot": "sha256:7b3f...e91d"
}
```

Quando alguém muda o engine, esse teste expõe toda mudança no comportamento observável. Campo novo na explicação aparece no diff. Avaliação reordenada aparece. Um quase-match que costumava ser reportado e agora não é, aparece.

O risco com teste golden é engenheiro aprender a rodar `-update` por reflexo. A defesa é deixar o diff legível: canonicalizar o JSON, ordenar as chaves, formatar número de forma consistente. Diff que diz *um número mudou* é diff que o revisor lê. Diff que reordena toda chave é diff que o revisor carimba.

Eu mantenho uma regra: update de golden é commit próprio. Nunca o mesmo commit da mudança de código que produziu o update. O revisor da mudança revisa o código; o revisor do update revisa o diff. Confundir é como regressão entra escondida.

## Teste de propriedade pra invariante

Teste comportamental prende cenário específico. Teste de propriedade prende invariante — afirmação que deveria ser verdade pra *todo* input.

Três invariantes que sempre escrevi pra rule engine:

**O conjunto candidato é superset do conjunto que disparou.** O que o matcher retorna tem que incluir toda regra que o evaluator dispara. O evaluator pode tirar regra do conjunto candidato; não pode inventar regra.

**O Result obedece a política de resolução.** Se a política diz que markup é somado, então pra qualquer conjunto de regras disparadas, o markup do Result tem que ser igual à soma dos outputs individuais. Se a política diz que uma ganha, o Result tem que ser exatamente um dos outputs individuais.

**Regra desabilitada nunca dispara.** Pra qualquer rule set e quaisquer facts, regra com `enabled: false` nunca pode aparecer no conjunto que disparou.

Em Go com `gopter` ou gerador similar:

```go
func TestCandidateSetIsSuperset(t *testing.T) {
    properties := gopter.NewProperties(nil)

    properties.Property("conjunto candidato ⊇ disparado", prop.ForAll(
        func(facts Facts) bool {
            engine := buildEngine(arbitraryRuleSet(50))
            candidates, fired, _ := engine.ExecuteForTesting(facts)

            candidateSet := toSet(candidates)
            for _, r := range fired {
                if !candidateSet.Contains(r) {
                    return false
                }
            }
            return true
        },
        genFacts(),
    ))

    properties.TestingRun(t)
}
```

O formato do teste de propriedade é estranho no começo. O teste não diz *dado esse fact, espere essa regra*. Diz *dado qualquer fact, essa relação se mantém*. O gerador produz centenas de fact sets por rodada; o engine responde cada um; a invariante é conferida em todos.

Os bugs que teste de propriedade pega são os bugs em que você não pensou em escrever unit test. O fact set que tem quinze mercados e days_to_departure negativo. O rule set com dependência de priority circular. O Facts map com chave duplicada. Não são bugs que você teria especificado de antemão; são bugs que o engine tem que tratar de qualquer jeito.

O `MinSuccessfulTests` do `gopter` por padrão é 100; pra rule engine eu empurro pra 1000 porque os geradores são baratos e o engine é rápido. Uma rodada única que pega um contraexemplo vale mais que mil rodadas confirmando a invariante. O contraexemplo é gravado como teste de regressão (mais sobre isso abaixo) e o engine é arrumado.

## Teste em estilo mutação: confiança na suíte

A suíte de 11 000 linhas passou por quatorze meses e errou o bug. A pergunta que devia ter surgido antes é *esses testes falhariam se eu quebrasse o engine?*

Teste de mutação responde direto. A ferramenta de mutação muda um operador por vez no código do engine — vira `<` em `<=`, troca `+` por `-`, muda `&&` por `||` — e roda a suíte contra cada versão mutada. Mutação que a suíte pega é bom; mutação que a suíte deixa passar é buraco na suíte.

Em Go, `gremlins` ou `go-mutesting` são as ferramentas usuais:

```sh
# Roda teste de mutação no pacote do engine.
gremlins unleash ./engine/...
```

Um output típico:

```
package engine/indexed/
  mutou 142 instruções
  matou 119 (84%)
  vivos 23
    engine/indexed/matcher.go:87 — `==` → `!=` vivo
    engine/indexed/matcher.go:103 — `<` → `<=` vivo
    ...
```

23 mutações sobreviventes são 23 lugares onde a suíte não consegue dizer se o engine tá certo ou errado. Cada uma é teste faltando ou teste tolerante a bug. O próximo pull request fecha o buraco uma mutação por vez.

O custo é tempo de execução. Teste de mutação num pacote pequeno são segundos; num codebase real são horas. A disciplina em que cheguei: rodar teste de mutação nos pacotes do engine semanalmente, não em todo PR. O sinal é "a suíte tá ficando melhor ou pior em pegar mutação?", que é métrica de movimento lento.

A parte mais desconfortável do teste de mutação é tornar visível a cobertura real da suíte. Cobertura de linha era 92% na suíte de 11 000 linhas. Taxa de mutação morta era 41%. A maioria das linhas era *executada* por teste; só algumas eram *checadas*. Esse gap é o modo de falha invisível que toda suíte de rule engine tem, e o único jeito de ver é mutar.

## Teste de regressão: o bug, imortalizado

Todo bug de produção merece um teste que prende o fix.

```go
// PRICE-1820: reserva alemã de trem a 4 dias foi cobrada de 3% de
// markup mas o log de explicação mostrou só a regra baseline
// disparando. Arrumado no commit 7b3f...e91d corrigindo a
// construção de chave de bucket no matcher indexed pra condição
// composta.
//
// Esse teste tem que continuar passando pra sempre.
func TestPRICE_1820_ShortLeadTimeMatchesIndexedAdapter(t *testing.T) {
    t.Parallel()
    store := loadRuleStore(t, "fixtures/PRICE-1820.yaml")
    engine := store.IndexedEngine()

    booking := Booking{Market: "DE", DaysToDeparture: 4, Channel: "rail"}
    result, explanation, err := engine.ExecuteWithExplanation(context.Background(), booking)
    if err != nil { t.Fatal(err) }

    matchedNames := matchedNames(explanation)
    if !slices.Contains(matchedNames, "short_lead_time_markup_de") {
        t.Errorf("short_lead_time_markup_de tem que disparar nesse fact set; veio %v", matchedNames)
    }
    if result.Markup != 5.0 {
        t.Errorf("esperava markup combinado 5.0; veio %.2f", result.Markup)
    }
}
```

Três propriedades de um teste de regressão que importam:

**Nomeia o bug.** Não "TestMatchesShortLeadTime" — `TestPRICE_1820_…`. O nome é o ticket. O teste é o contrato de que o ticket fica fechado.

**Prende os facts mínimos que reproduzem.** Teste de regressão que precisa de fixture de 200 linhas é teste de regressão que vai ser deletado num refactor. A reprodução mínima é o ativo.

**Inclui comentário dizendo por que existe.** O comentário é o postmortem. O próximo engenheiro que ler o teste tem que entender o que ele checa e que dor de negócio preveniu.

Teste de regressão acumula. Depois de dois anos um rule engine tem arquivo de regressão com cem entradas. São lentos de rodar. São também os únicos testes que pegam o bug que alguém re-introduz em 2027 porque não soube de 2025. A acumulação é o ponto.

## O que não testar

Três categorias de teste desperdiçam atenção de engenharia e dão zero pro time:

**Teste das estruturas de dado internas do engine.** *Conferir que o engine indexed tem 17 buckets depois de carregar essas 50 regras* é teste do problema do `bre-go`, não seu. Se o engine muda como indexa, o teste quebra; o comportamento de negócio não mudou; o sinal da suíte caiu.

**Teste dos listeners do engine.** *Conferir que OnRuleMatched dispara exatamente N vezes* é testar o engine. A suíte do próprio engine tem esses testes. A suíte da aplicação deve testar o resultado de negócio que o registro emitido pelo listener descreve, não o mecanismo do listener.

**Teste que prende escolha de implementação que o time não acordou.** *Conferir que R7 tem priority 437* é prender um valor que provavelmente não devia ter sido 437 pra começar. O teste certo é *R7 tem precedência sobre R3*. Essa asserção sobrevive ao refactor de priority.

A regra geral: testes que quebram quando o engine refatora mas o comportamento de negócio não muda são testes que não deveriam ter sido escritos. Testes que passam quando o engine refatora mas o comportamento de negócio regride em silêncio são bugs na suíte.

## Teste de loader: o espaço negativo

A maioria dos times testa que o loader carrega arquivo bom com sucesso. Poucos testam que o loader *rejeita* arquivo ruim corretamente. O espaço negativo é onde o teste de loader paga de volta.

```go
func TestLoaderRejectsBadFiles(t *testing.T) {
    cases := []struct {
        name        string
        file        string
        wantErrPart string
    }{
        {"tipo de ação desconhecido", "bad/unknown_action.yaml", "unknown action type"},
        {"markup não-numérico", "bad/string_markup.yaml", "then.value must be number"},
        {"nome de regra duplicado", "bad/duplicate_name.yaml", "ErrDuplicateRuleName"},
        {"versão de schema ausente", "bad/no_version.yaml", "schema version"},
        {"regra sombreada", "bad/dead_rule.yaml", "rule never fires"},
    }

    for _, tt := range cases {
        t.Run(tt.name, func(t *testing.T) {
            _, err := loader.Load(tt.file)
            if err == nil {
                t.Fatal("esperava erro; veio nil")
            }
            if !strings.Contains(err.Error(), tt.wantErrPart) {
                t.Errorf("erro %q não contém %q", err, tt.wantErrPart)
            }
        })
    }
}
```

Cada linha é uma classe de bug que o loader devia pegar. Cada fixture de linha tá commitado no diretório testdata. Quando alguém muda o loader, esse teste impõe que as mensagens de rejeição não regridam silenciosamente.

O mais difícil desses é o caso *regra sombreada*. Testa o `engine/indexed.Engine.Diagnose()` contra um rule set onde uma regra provavelmente nunca dispara. O fixture é pequeno (duas regras) e a asserção é no diagnóstico, não no comportamento de runtime. É o teste que pega a regra morta silenciosa antes da produção pegar.

## Uma suíte de teste, no formato em que devia estar

Se eu fosse reconstruir a suíte de 11 000 linhas do zero, o formato seria:

```
testdata/
  fixtures/                   # rule sets, um por trimestre
    2025-q3.yaml
    2025-q4.yaml
  scenarios/                  # casos de negócio nomeados (request JSON)
    de-short-lead-rail.json
    fr-baseline.json
    compliance-override.json
  golden/                     # as explicações que a gente acordou
    de-short-lead-rail.json
    fr-baseline.json
  bad/                        # arquivos que o loader tem que rejeitar
    unknown_action.yaml
    string_markup.yaml
engine/
  matcher_test.go             # unit test pra um estágio
  evaluator_test.go
  composer_test.go
behaviour/
  pricing_scenarios_test.go   # teste comportamental table-driven
  golden_test.go              # golden de explicação
loader/
  loader_test.go              # teste positivo + negativo do loader
properties/
  invariants_test.go          # teste de propriedade
regressions/
  price_1820_test.go          # um arquivo por ticket
  price_1873_test.go
  ...
```

O formato é a lição. Os testes são organizados por *o que protegem*, não por *qual arquivo ficam ao lado*. O diretório behaviour protege o acordo de negócio. O diretório engine protege a mecânica do engine. O diretório regressions lembra o que doeu. O diretório properties prende invariante. Cada diretório tem tempo de vida diferente, audiência diferente, e razão diferente pra falhar.

{{< plantuml title="Duas camadas de teste, duas intenções, dois tempos de vida" >}}
@startuml
skinparam shadowing false
skinparam componentStyle rectangle
skinparam defaultFontName "Helvetica"

rectangle "Comportamento de negócio\n(sobrevive a refactor)" as BB {
  rectangle "Teste comportamental\n(cenário → resultado)" as B1
  rectangle "Explicação golden" as B2
  rectangle "Teste de regressão\n(bug imortalizado)" as B3
}

rectangle "Mecânica do engine\n(quebra com refactor)" as EM {
  rectangle "Unit test por estágio" as E1
  rectangle "Teste de propriedade\n(invariante)" as E2
  rectangle "Teste de mutação\n(saúde da suíte)" as E3
}

BB --> EM : depende mas não prende
EM ..> BB : fornece a superfície
@enduml
{{< /plantuml >}}

## O que o time ganha quando a suíte tá no formato certo

Três coisas.

**Refactor para de assustar.** Quando o teste comportamental é o contrato, trocar o matcher de linear pra indexed é CI verde, não semana santa. A mecânica do engine se move; o contrato de negócio segura.

**Review fica mais afiado.** PR que muda o rule set produz diff contra o teste comportamental. O time de produto lê o diff. O time de engenharia vê se o diff é intencional. A conversa é "o acordo mudou?" — não "o teste passou?"

**Bug vira professor.** Cada teste de regressão na suíte é um bug que nunca voltou. A memória coletiva do time sobre incidente passado tá codificada em código. Engenheiro novo lê o diretório de regressão e aprende com o que o sistema já foi mordido.

A suíte de 11 000 linhas não tinha nenhuma dessas propriedades. Tinha cobertura de linha alta e cobertura de negócio baixa. Os dashboards verdes e os markups errados. A reconstrução levou seis meses, terminou em 6 000 linhas, e pegou os próximos quatro quase-bugs antes da produção pegar.

## O que vem a seguir

O próximo post é explicabilidade — o artefato que essa camada inteira de teste assume. Todo teste comportamental checa um fato sobre a Explanation. Todo teste golden prende a Explanation. Todo teste de regressão tenta alcançar a Explanation. O próximo post é o que torna a Explanation digna de ser alcançada: como é estruturada, o que carrega, o que custa produzir, e que tipo de investigação habilita.

Depois disso a gente vai pra tráfego sintético. Teste é determinístico; produção não. Tráfego gerado é a ponte: é reproduzível como teste e tem formato de produção, e é o que torna a próxima camada de validação — shadow mode e replay — significativa.

Por enquanto, a lição é o contrato. Teste pra sistema de regra tem que proteger o acordo de negócio, não a implementação do engine. A camada do engine merece teste que mede mecânica; a camada das regras merece teste que prende comportamento. Quando os dois são confundidos, a suíte fica verde por quatorze meses e o cliente paga pelo gap.

Escreve o teste que o próximo engenheiro precisa pra entender. Prende os cenários que o time acordou. Imortaliza os bugs que você já pagou. O refactor do engine vai vir, e a suíte que sobrevive é a que sabia o que tava protegendo desde o começo.
