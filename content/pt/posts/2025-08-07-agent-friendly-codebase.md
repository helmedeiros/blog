---
title: "Está na Hora de um Codebase Amigável para Agentes"
categories:
  - AI
  - Engineering
  - Software Architecture
date: 2025-08-07
tags:
  - ai
  - arquitetura-de-software
  - refatoracao
  - clean-code
  - arquitetura-hexagonal
  - testing
  - developer-experience
description: "Por que a estrutura do repositório, a arquitetura hexagonal e loops rápidos de feedback importam mais do que prompts espertos ao trabalhar com agentes de IA."
subtitle: "Pare de reescrever prompts. Comece a corrigir seu repositório."
---

Um "codebase amigável para agentes" não é um repositório onde uma IA consegue escrever código. Essa parte já é fácil. A parte desconfortável é saber se um agente de IA consegue fazer o trabalho que você realmente quer que seja feito: realizar uma mudança que atravessa múltiplos arquivos, executar os checks corretos, interpretar falhas, iterar e produzir um diff pequeno o suficiente para revisão e seguro o suficiente para merge.

Depois de construir alguns projetos pequenos e forçar agentes a percorrer os mesmos fluxos repetidamente, parei de pensar em termos de "capacidade de IA para escrever código" e comecei a pensar em "usabilidade do repositório". O agente é mais um colaborador. Um colaborador rápido, sim. Mas também um colaborador que se perde facilmente e que amplifica qualquer ambiguidade estrutural que você deixe espalhada pelo caminho.

Este post é o que eu gostaria que alguém tivesse me dito antes de eu gastar horas reescrevendo prompts em vez de corrigir a estrutura do repositório.

## A ideia central: seu repositório é uma interface

Quando falo em "agent-friendly", não estou falando de magia específica de IA. Estou falando de algo próximo à experiência clássica de desenvolvimento, mas com uma diferença importante: humanos sobrevivem a conhecimento tribal, scripts pela metade e convenções inconsistentes porque podem perguntar para outras pessoas ou "sentir" o sistema. Agentes não sentem. Eles identificam padrões e seguem instruções. Se essas instruções são implícitas, desatualizadas ou espalhadas, o agente vai produzir mudanças que parecem plausíveis, mas que estão erradas daquelas formas entediantes que custam tempo.

Um codebase amigável para agentes é aquele em que:

1. O agente consegue descobrir com confiabilidade onde a mudança deve acontecer.
2. O agente consegue realizar a mudança sem causar efeitos colaterais em cascata.
3. O agente consegue validar a mudança sem que você vire o executor manual de testes.
4. O agente consegue explicar o que mudou de uma forma que um revisor humano consiga confiar.

Se qualquer um desses pontos falhar, o que você tem não é "aceleração com IA". O que você tem é um novo tipo de trabalho repetitivo: ajuste de prompt, despejo repetido de contexto e verificação manual.

## O que aprendi forçando agentes em fluxos reais

### Legibilidade vence esperteza

A primeira armadilha em que caí foi assumir que o agente "ia se virar". Às vezes ele se vira. Mas "às vezes" não é estratégia.

O que funcionou melhor foi reduzir agressivamente o número de lugares plausíveis onde uma mudança poderia viver. Na prática, isso significa ser opinativo sobre estrutura e nomenclatura, mesmo que pareça rígido. Agentes são excelentes em seguir convenções; são medianos em descobrir convenções implícitas.

Em um repositório bagunçado, o agente tende a fazer uma de duas coisas:

Ele encontra um arquivo parecido, copia o padrão e diverge sutilmente da arquitetura pretendida.

Ou ele toca arquivos demais porque não consegue distinguir o que é lógica de domínio do que é código de cola.

Ambos os cenários produzem diffs que parecem ocupados e "inteligentes", mas que são difíceis de revisar e quebram de formas inesperadas.

### Um caminho dourado vale mais do que dez parágrafos de README

Eu costumava acreditar que documentação era a resposta. Ela ajuda, mas não da forma que eu imaginava.

Agentes não precisam de mais prosa sobre o sistema. Eles precisam de um pequeno conjunto de comandos estáveis — um "caminho dourado" — e arquivos que funcionem como pontos de entrada claros para o trabalho. Quando isso não existe, o agente inventa fluxos. E fluxos inventados são frágeis.

O que reduziu falhas de forma consistente foi ter um conjunto de comandos que sempre funcionam em uma máquina limpa, mais um arquivo de contrato curto dizendo quais comandos rodar e quais limites não cruzar.

Este é o padrão que passei a usar por padrão em projetos pequenos:

```bash
make bootstrap
make test
make lint
make run
```

Por baixo, esses comandos podem chamar o que você quiser. O ponto não é o Make. O ponto é que o repositório tem um sistema operacional previsível para colaboradores, humanos ou agentes.

### "Funciona na minha máquina" vira "funciona no meu prompt"

Humanos sofrem com "funciona na minha máquina". Agentes sofrem com "funciona no meu prompt".

Se a única forma de chegar à mudança correta é escrever o prompt perfeito, com um parágrafo inteiro de contexto adicional, você não está construindo software amigável para agentes. Você está construindo um sistema dependente de prompt. Isso não escala nem dentro de um único time, porque prompts mudam. Pessoas mudam. Agentes mudam. Ferramentas mudam.

A correção é entediante: fazer o repositório carregar o contexto.

Um teste simples que passei a usar é:

Se eu apagar o histórico do chat e rodar a tarefa novamente com um agente "limpo", ele ainda consegue ter sucesso apenas lendo o repositório?

Quando a resposta é "sim", o repositório está fazendo o trabalho. Quando é "não", sou eu que estou fazendo o trabalho.

### Arquitetura hexagonal é um multiplicador para agentes

A melhoria arquitetural mais consistente que observei, em múltiplos projetos, foi migrar para um design hexagonal (ports and adapters). Não porque está na moda, mas porque ele reduz o espaço de busca das mudanças e barateia a validação.

Arquitetura em camadas pode ser limpa. Muitos times entregam ótimos sistemas com ela. O problema é que, na prática, muitas arquiteturas em camadas viram "camadas só no nome". Fronteiras se misturam. Lógica de domínio vaza para controllers e persistência. Infraestrutura sobe camadas. Quando um agente entra nesse ambiente, ele faz o que um engenheiro júnior faria: segue o caminho mais curto para "fazer funcionar", mesmo que isso coloque lógica no lugar errado.

Arquitetura hexagonal torna mais difícil fazer a coisa errada por acidente e mais fácil identificar onde uma mudança pertence.

### Como agentes se comportam em arquiteturas em camadas

Uma arquitetura em camadas típica encoraja um fluxo como:

Controller -> Service -> Repository -> Database

Em teoria, lógica de domínio pertence ao service. Na prática, vejo services virarem mistura de orquestração com regras aleatórias, repositories acumularem decisões e controllers receberem "só mais esse caso especial".

Um agente que recebe a tarefa "adicionar funcionalidade X" normalmente:
1. Começa pelo controller, porque é o ponto de entrada.
2. Procura um método de service parecido.
3. Se não encontrar algo com o formato exato, cria um novo método.
4. Se faltar dado, altera repository ou mapeamento de entidade.
5. Espalha validações onde for mais conveniente.

O código compila. Testes superficiais passam. Mas a coerência arquitetural se deteriora.

O pior é que arquiteturas em camadas frequentemente levam a estratégias de teste mais pesadas do que o necessário. Se regras de domínio estão acopladas a framework web ou persistência, validar mudanças exige testes de integração. Agentes conseguem rodar esses testes, mas são mais lentos e produzem falhas mais ruidosas. O loop de iteração fica caro.

### Como agentes se comportam em arquiteturas hexagonais

Arquitetura hexagonal muda a superfície de trabalho.

Em vez de perguntar "em qual camada isso vai?", você pergunta "isso é comportamento de domínio ou preocupação de adaptador?".

O desenho tende a ser:
- **Domínio (puro):** entidades, value objects, políticas, casos de uso
- **Portas (interfaces):** o que o domínio precisa do mundo externo
- **Adaptadores (impuros):** handlers web, persistência, mensageria, APIs externas

Em um repositório que realmente respeita essas fronteiras, um agente tende a:
1. Encontrar o caso de uso responsável pelo comportamento.
2. Modificar a lógica de domínio em poucos arquivos.
3. Se precisar de I/O novo, definir uma porta.
4. Implementar o adaptador separadamente.
5. Atualizar a composição no ponto de wiring.

O resultado são diffs menores e mais claros. E, mais importante, validação local mais simples, porque o núcleo de domínio é testável sem infraestrutura.

A parte que me surpreendeu é que arquitetura hexagonal não apenas deixa o sistema "mais limpo". Ela facilita instruir o agente. Você consegue dizer em uma frase como navegar o sistema:

"Quando mudar regra de negócio, mude primeiro domínio e caso de uso. Adaptadores devem ser finos."

Agentes seguem isso. Estruturas hexagonais tornam violações mais visíveis.

### O mecanismo de enforcement: compilação e fricção de testes

O benefício real da arquitetura hexagonal não é o diagrama. É a fricção.

Se você organiza o repositório de forma que o pacote de domínio não dependa de frameworks web, bibliotecas de banco ou clientes externos, o agente não consegue importar algo errado sem o build reclamar. Isso é agent-friendly. Intenção arquitetural vira guardrail.

Em Go, por exemplo:

```bash
/internal
  /domain
    money.go
    asset.go
    capitalization_policy.go
  /app
    classify_task.go
    process_sprint.go
    ports.go
  /adapters
    /jira
      client.go
    /persistence
      sqlite_repo.go
    /cli
      commands.go
/cmd/assetcap
  main.go
```

O ponto crucial não é só a pasta. É a regra: domínio e app não importam adaptadores. O composition root faz o wiring.

Quando isso é verdade, revisar diffs de agentes deixa de ser debate de gosto e vira verificação objetiva de restrições.

### Um pequeno exemplo: "regras de classificação" em camadas vs hexagonal

Digamos que estou construindo o assetcap e quero classificar issues do Jira em capitalizáveis vs não-capitalizáveis com base em labels e tipo de issue, e quero ajustar as regras.

Em uma arquitetura em camadas, o agente pode implementar a lógica dentro do adaptador de cliente Jira ou na camada de persistência, porque é ali que o dado ganha forma. O código funciona, mas agora a classificação está acoplada ao Jira.

Em hexagonal, classificação é uma política de domínio. O adaptador do Jira mapeia issues para uma representação de domínio, e a política decide.

Isso leva ao tipo de testes que agentes escrevem e mantêm bem:

```go
func TestClassificationPolicy(t *testing.T) {
  policy := NewClassificationPolicy()

  issue := Issue{
    Type:  "Story",
    Labels: []string{"platform", "capex"},
  }

  got := policy.Classify(issue)
  if got != Capitalizable {
    t.Fatalf("expected Capitalizable, got %v", got)
  }
}
```

Esse teste roda em milissegundos, sem cliente Jira, sem mocks HTTP, sem banco. Esse loop curto é um multiplicador de força para agentes porque permite iteração rápida com sinais claros de falha.

Arquitetura em camadas pode chegar ao mesmo ponto, mas na prática, times frequentemente não mantêm regras de domínio isoladas. Hexagonal faz do isolamento a postura padrão.

### O arquivo "agent contract" virou inegociável

Quando parei de tratar sucesso de agente como problema de prompt e comecei a tratar como problema de repositório, um artefato passou a se pagar sempre: um arquivo curto explicando como o trabalho acontece ali.

Pode se chamar AGENTS.md, CONTRIBUTING.md ou outro nome. O importante é ser curto, preciso e alinhado com CI.

Exemplo:

```md
# Agent Contract

## Intent

This repo follows hexagonal architecture.
Domain and application layers must not depend on adapters.

## Golden commands

- make bootstrap
- make test
- make lint
- make run

## Change rules

- Business rules live in /internal/domain and /internal/app.
- Adapters in /internal/adapters must stay thin.
- Do not introduce new patterns without updating docs/architecture.md.

## Tests

- Domain changes require unit tests in /internal/domain.
- Use-case changes require tests in /internal/app.
- Adapter changes require integration tests only when necessary.

## Forbidden

- Do not commit secrets.
- Do not modify production infrastructure without explicit instruction.
```

Isso não é redundância. É o que separa "agente como colaborador" de "agente como gerador de caos".

### O requisito oculto: você precisa de loops de feedback rápidos e confiáveis

Repositórios amigáveis para agentes não são só sobre estrutura. São sobre tornar a verificação barata.

Um repositório é hostil para agentes quando:
- testes são lentos e instáveis
- lint e formatação são inconsistentes
- o setup local é frágil
- CI faz coisas que scripts locais não fazem

Nessas condições, o agente vira um gerador de mudanças, não um colaborador. Ele produz código, mas você fica preso validando e reparando.

A melhoria mais rápida que fiz nos meus projetos foi alinhar comandos locais com CI. Parei de tratar CI como universo separado. Se CI roda ./gradlew check, meu comando local roda ./gradlew check. Se CI roda go test ./..., meu comando local roda go test ./.... Se CI precisa de container de banco, o fluxo local sobe o mesmo container com um comando.

Não é trabalho glamouroso. É o trabalho que torna todo o resto possível.

### Onde arquiteturas em camadas ainda vencem, e como mantê-las agent-friendly

Não estou dizendo que hexagonal é a única resposta. Arquiteturas em camadas podem ser perfeitamente amigáveis para agentes se você fizer duas coisas com disciplina:

Primeiro, tornar fronteiras aplicáveis. Se sua camada "service" pode importar repositories diretamente, e repositories podem chamar serviços externos, você não tem uma arquitetura em camadas; você tem uma sopa de dependências. Agentes vão nadar nela e trazer de volta o que encontrarem.

Segundo, tornar seu domínio testável sem infraestrutura. Se comportamento de domínio exige subir um banco de dados, seu loop de agente vai ser caro e ruidoso. Você ainda pode ter sucesso, mas vai gastar mais tempo.

Uma arquitetura em camadas que funciona bem com agentes tende a parecer "hexagonal na prática": regras de domínio isoladas, adaptadores finos, wiring nas bordas.

Nesse ponto, o debate se torna sobre nomenclatura e empacotamento, não sobre capacidade.

### A definição pragmática

Depois de repetir esses experimentos, minha definição ficou simples:

Um codebase é amigável para agentes quando oferece estrutura e feedback suficientes para que um agente faça mudanças corretas sem interpretação humana constante.

Estrutura significa:
- fronteiras claras
- poucos pontos válidos de entrada para mudança
- comandos padronizados

Feedback significa:
- testes rápidos de domínio
- lint e type check previsíveis
- paridade entre local e CI

Arquitetura hexagonal ajuda porque transforma "onde isso deve ir?" em restrição, não em debate. E restrições são exatamente o que agentes precisam.

### Pensamento final

A tentação é tratar produtividade com agentes como uma história de ferramenta. Não é.

Ferramentas importam.

Mas é o repositório que decide se o loop é estável.

O ganho real não veio porque o agente ficou mais inteligente.

Veio porque o codebase deixou de ser vago.
