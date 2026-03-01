---
title: "Quando o Agente Pergunta de Volta: Planejamento Interativo e Limites de Especificação"
categories:
  - AI
  - Engineering
  - Software Architecture
date: 2025-10-30
tags:
  - ai
  - claude-code
  - fluxos-agenticos
  - planejamento
  - arquitetura-de-software
  - developer-experience
description: "Plan Mode e perguntas interativas transformam a colaboração com agentes de correção reativa para alinhamento preventivo. Clareza de especificação antes da execução é o investimento de qualidade mais barato que existe."
subtitle: "Ambiguidade de especificação é o último gargalo. Planejamento interativo é como você resolve isso."
---

Pedi ao agente para adicionar uma nova regra de validação. A arquitetura estava limpa. A skill estava carregada. O agente seguiu o protocolo perfeitamente: domínio primeiro, testes depois, adaptadores por último.

E construiu a coisa errada.

Não catastroficamente errada. O código compilou, os testes passaram, e o diff estava organizado. Mas a regra que ele implementou não era a regra que eu queria. Eu assumi que "validar entrada" significava rejeitar campos vazios. O agente assumiu que significava aplicar restrições de formato. Ambas as interpretações eram plausíveis. Nenhum de nós tinha verificado.

Esse momento esclareceu algo que eu vinha circulando por semanas: estrutura e comportamento são necessários, mas não são suficientes. A terceira camada é **clareza de intenção**.

## Onde isso se encaixa na série

No primeiro artigo, argumentei que um [codebase amigável para agentes]({{< ref "2025-08-07-agent-friendly-codebase" >}}) reduz a ambiguidade sobre *onde* as mudanças pertencem. Arquitetura hexagonal, comandos padrão, loops de feedback rápidos — tudo isso restringe o espaço de busca para que agentes naveguem um repositório sem adivinhar.

No segundo, explorei como [Skills do Claude Code]({{< ref "2025-10-17-teaching-the-agent-how-to-work" >}}) codificam *como* as mudanças acontecem. Protocolos de execução, gates de validação, resumos de diff por camada — skills transformam disciplina de engenharia em comportamento repetível.

Este artigo aborda a lacuna que permanece mesmo quando ambas as camadas estão funcionando: **o que exatamente deve ser construído**.

| Camada | Pergunta que responde | Mecanismo |
| --- | --- | --- |
| Estrutura | Onde a mudança pertence? | Arquitetura, fronteiras, comandos padrão |
| Comportamento | Como a mudança deve acontecer? | Skills, protocolos de execução, validação |
| Intenção | O que exatamente deve ser construído? | Plan Mode, perguntas interativas |

Estrutura restringe localização. Comportamento restringe processo. Mas nenhum dos dois restringe significado. E significado é onde os erros mais caros se escondem.

## O que é o Plan Mode na prática

O Claude Code introduziu o [Plan Mode](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview) para separar intenção de execução.

Em vez de editar arquivos imediatamente, o agente analisa o repositório e propõe um plano estruturado antes de tocar no codebase. Você ativa com um simples atalho de teclado, e todo o modelo de interação muda.

![Plan Mode ativado no Claude Code — o agente analisa antes de agir](/uploads/2025/10/plan-mode-on.png)

Isso espelha algo que engenheiros experientes fazem instintivamente: eles refinam o ticket antes de escrever código. Perguntam "o que você realmente quis dizer?" antes de abrir um editor. Questionam critérios de aceite ambíguos.

O Plan Mode dá aos agentes essa mesma pausa.

Na prática, quando ativo o Plan Mode para um pedido de funcionalidade, o agente lê a estrutura do repositório, identifica arquivos relevantes e propõe uma sequência de mudanças — sem executar nenhuma delas. Posso revisar o plano, ajustá-lo ou rejeitá-lo inteiramente antes que uma única linha mude.

> A mudança não é apenas segurança. É alinhamento.

Um plano é uma hipótese sobre o que a mudança deveria ser. Revisar um plano é mais barato que revisar um diff, e rejeitar um plano não custa nada.

## A Ferramenta de Perguntas Interativas

Na versão 2.0.22, o Claude Code lançou duas capacidades relacionadas: uma ferramenta de perguntas interativas e questionamento mais frequente no Plan Mode. A entrada no changelog é enganosamente breve para algo que muda tanto o modelo de interação.

![Claude Code v2.0.22 changelog — ferramenta de perguntas interativas e melhorias no plan mode](/uploads/2025/10/claude-code-changelog-2-0-22.png)

A mudança real veio quando o Claude Code adicionou a capacidade do agente **fazer perguntas de esclarecimento** antes de finalizar um plano.

Isso não é uma conveniência menor. Muda o modelo de interação fundamentalmente.

Em vez de o agente adivinhar requisitos ambíguos, ele para e pergunta. Limites de escopo, casos extremos, restrições de compatibilidade, regras de precedência — o tipo de coisa que engenheiros experientes levantam em revisões de design, o agente agora consegue levantar antes de escrever código.

![A Ferramenta de Perguntas Interativas — esclarecimento estruturado antes da execução](/uploads/2025/10/interactive-question-tool.png)

As perguntas não são genéricas. São contextuais. O agente lê o codebase, identifica potenciais ambiguidades no pedido e faz perguntas direcionadas sobre as decisões específicas que precisa tomar.

Veja como uma interação típica se parece quando peço ao agente para "adicionar validação de entrada no fluxo de cadastro":

| O que o agente pergunta | O que revela |
| --- | --- |
| "A validação deve rejeitar campos vazios, validar formato, ou ambos?" | Ambiguidade de escopo |
| "Erros de validação devem bloquear o envio ou mostrar avisos inline?" | Suposição de UX |
| "Existem padrões de validação no codebase que eu deva seguir?" | Restrição de consistência |
| "Isso se aplica a requisições de API, envios de formulário, ou ambos?" | Definição de fronteira |

Cada uma dessas perguntas representa uma suposição que eu teria feito implicitamente. E cada suposição implícita é um ciclo potencial de retrabalho.

## Limites de especificação: onde o custo real se esconde

Pedidos de funcionalidade carregam bagagem invisível. Toda vez que alguém escreve "adicionar funcionalidade X," existem suposições implícitas sobre comportamento, propriedade, casos extremos e restrições que nunca chegam à descrição.

Sem esclarecimento, o agente preenche essas lacunas com **padrões plausíveis**. Padrões plausíveis são perigosos justamente porque parecem razoáveis. O código compila. Os testes passam. O diff está limpo. E então alguém revisa e diz: "Não era isso que eu queria."

Comecei a rastrear esses desalinhamentos. O padrão era consistente:

| Categoria | Exemplo de suposição | Custo de errar |
| --- | --- | --- |
| **Escopo** | "Todos os usuários" vs. "apenas premium" | Retrabalho com feature flag |
| **Tratamento de erros** | Falha silenciosa vs. erro explícito | Incidente em produção |
| **Propriedade de dados** | Quem escreve vs. quem lê | Dor de migração |
| **Compatibilidade** | Breaking change vs. retrocompatível | Pressão para rollback |

Esses não são casos extremos. São o *núcleo* do que torna uma especificação completa. E são exatamente o tipo de coisa que perguntas interativas trazem à tona antes que o código exista.

> Não se trata de tornar o agente mais inteligente. Se trata de tornar a especificação explícita.

## De planejamento linear para baseado em diálogo

Fluxos de trabalho anteriores com IA eram lineares: inserir um prompt, receber a saída, corrigir o que está errado, repetir. O ciclo de correção era o mecanismo primário de qualidade.

O planejamento interativo introduz diálogo *antes* da execução.

| Fluxo linear | Fluxo baseado em diálogo |
| --- | --- |
| Prompt -> Código -> Revisão -> Correção | Prompt -> Perguntas -> Plano Refinado -> Código -> Revisão |
| Ambiguidade aparece na revisão | Ambiguidade aparece no planejamento |
| Correção é o mecanismo de qualidade | Esclarecimento é o mecanismo de qualidade |
| Caro: mudanças já existem | Barato: nenhum código escrito ainda |

A diferença está em *quando* a ambiguidade é resolvida. Em um fluxo linear, você descobre o desalinhamento depois que o agente já produziu um diff. Em um fluxo dialogado, descobre antes que qualquer arquivo mude.

Na prática, agora uso o Plan Mode como padrão para qualquer tarefa que toque mais de uma camada arquitetural. O overhead é mínimo — alguns segundos lendo e respondendo perguntas. A economia é substancial: menos diffs rejeitados, menos ciclos de "não era isso que eu queria" e menos troca de contexto entre revisar código e re-explicar intenção.

## Por que isso importa agora

À medida que agentes ganham a capacidade de modificar sistemas maiores — abrangendo múltiplos arquivos, múltiplos serviços, múltiplas preocupações — o custo da ambiguidade de especificação cresce de forma não-linear. Uma suposição errada em uma mudança de um único arquivo custa um ciclo de revisão. Uma suposição errada em uma mudança transversal custa uma tarde inteira.

Correção após implementação é cara. Esclarecimento antes da implementação é barato.

> Perguntas interativas introduzem fricção produtiva no momento certo — antes do código existir, quando mudar de direção não custa nada.

Esse é o mesmo insight que move desenvolvimento orientado a testes, revisões de design e registros de decisão arquitetural. Quanto mais cedo você identifica uma divergência entre intenção e execução, mais barato é corrigir. O planejamento interativo aplica esse princípio à colaboração humano-agente.

## Juntando as peças

Quando olho para como meu fluxo de trabalho evoluiu ao longo desta série, o padrão é claro:

```text
Estrutura do Repositório → Skills de Execução → Clareza de Especificação
        (onde)                   (como)                  (o quê)
```

Cada camada reduz uma classe diferente de erros:

- **Estrutura** impede que o agente coloque lógica no lugar errado.
- **Skills** impedem que o agente siga o processo errado.
- **Plan Mode + Perguntas** impedem que o agente construa a coisa errada.

Nenhuma dessas camadas é suficiente sozinha. Um repositório perfeitamente estruturado com ótimas skills ainda produz resultado errado se a especificação for ambígua. Um agente que faz ótimas perguntas mas opera em um codebase caótico ainda produz diffs confusos.

As camadas se compõem. E quando se alinham, a interação deixa de ser correção reativa e passa a ser colaboração proativa.

## Reflexão final

Um prompt unilateral assume completude. Diz: "Eu te contei tudo que você precisa saber." Essa suposição quase sempre está errada.

Um plano interativo assume imperfeição. Diz: "Vamos descobrir o que eu realmente quero dizer antes de você começar a construir."

Quando agentes participam do esclarecimento de intenção, a colaboração se torna orientada por alinhamento, não por correção. A conversa deixa de ser "conserte o que você fez" e passa a ser "vamos concordar sobre o que fazer."

Isso não é uma funcionalidade de uma ferramenta. É o início de uma engenharia orientada por especificação — e muda como eu penso sobre cada tarefa que entrego a um agente.
