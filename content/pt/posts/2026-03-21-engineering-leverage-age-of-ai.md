---
title: "O que muda quando testar fica mais barato"
categories:
  - AI
  - Engineering
  - Leadership
date: 2026-03-21
tags:
  - ia
  - lideranca-engenharia
  - produtividade
  - experimentacao
  - velocidade-de-aprendizado
  - design-de-times
description: "A verdadeira pergunta sobre IA em engenharia não é se ela ajuda a escrever código mais rápido. É o que muda quando o custo de iteração começa a cair."
subtitle: "Entregando mais sem precisar crescer o time"
---

A maioria dos times ainda faz a pergunta errada sobre IA.

Perguntam se ela ajuda o engenheiro a programar mais rápido.

Acho que isso não é nem perto do ponto principal.

A pergunta que realmente importa é: **o que muda dentro de um time quando iterar fica mais barato?**

Essa é a pergunta que não sai da minha cabeça faz um tempo. Não como teoria, mas como coisa prática mesmo. O escopo foi crescendo. A pressão por entrega e qualidade continuou lá. O time não cresceu no mesmo ritmo. A gente podia reagir do jeito clássico: desacelerar, aceitar mais atrito ou tentar convencer alguém de que precisava de mais gente. Em vez disso, a gente começou a olhar com mais atenção pra como trabalhava.

> Isso não é uma história sobre usar IA como atalho. É sobre mudar a forma de trabalhar pra aprender mais rápido sem baixar a barra.

Essa diferença importa. É fácil se distrair com demo bonita e promessa animada. É mais difícil, e mais útil, perguntar onde a IA realmente muda o custo do trabalho.

## O gargalo real não é escrever código

Por muito tempo, a gente em software tratou "escrever código mais rápido" como a principal forma de entregar mais. Se o código sai mais rápido, a entrega aumenta. Parece fazer sentido à primeira vista.

Mas trabalho de produto não é uma linha reta da ideia até a feature em produção. É um ciclo. O time forma uma hipótese, transforma ela em algo construível, implementa, valida, mede o resultado e decide o que fazer em seguida. É aí que a velocidade se ganha ou se perde.

```
Hipótese -> Especificação -> Implementação -> Validação -> Medição -> Decisão
```

O problema de verdade não é quantos arquivos mudam por dia. É o quanto custa percorrer esse ciclo com confiança.

Quando o ciclo fica pesado, o time desacelera. Não porque as pessoas são fracas ou as ideias são ruins. É porque aprender ficou caro.

É aí que a conversa fica interessante pra mim. A IA não deixou a gente mais sábio de repente. Ela não tirou a incerteza. Ela não eliminou os trade-offs. O que ela fez foi ajudar a reduzir o esforço em várias partes desse ciclo. E quando isso começa a acontecer, o efeito vai muito além de "programar mais rápido".

> A vantagem real não são respostas melhores. É que testar ficou mais barato.

## Por que aprender rápido importa mais do que ter boas ideias

A gente tem o hábito de romantizar ideias. Fala de estratégia, visão, criatividade. Tudo isso importa. Mas muitos times de produto não ficam abaixo do esperado porque faltam ideias. Ficam porque testar as ideias que têm é caro demais.

Quando testar é lento, tudo pesa mais. As discussões ficam mais longas. O escopo fica mais travado. As pessoas se apegam demais às próprias propostas. O risco parece maior do que é. Um único experimento começa a carregar um peso emocional enorme.

Quando testar fica mais barato, a postura do time muda. Pequenas apostas ficam mais fáceis de justificar. Decisões que dá pra reverter parecem mais naturais. O aprendizado começa a tomar o lugar da discussão.

O contraste é mais ou menos esse:

| Quando iterar é caro | Quando iterar fica mais barato |
| --- | --- |
| O time defende ideias por mais tempo | O time testa mais cedo |
| As apostas ficam maiores | As apostas ficam menores |
| Mudança parece arriscada | Mudança parece controlável |
| Aprender demora | O aprendizado acumula mais rápido |

Não é sobre ser imprudente. É sobre reduzir o custo de descobrir o que é verdade.

É por isso que eu sempre volto pra **velocidade de aprendizado**. Não como slogan, mas como uma medida prática de quão rápido um time consegue transformar incerteza em clareza.

## Onde a IA entrou de verdade no ciclo

Uma das formas mais fáceis de usar IA mal é jogá-la só na parte de código e achar que resolveu. Isso gera screenshot bonita, mas raramente muda como o time trabalha de fato.

O que fez diferença pra gente foi colocar a IA em várias etapas do ciclo. Não em todo lugar de forma cega, mas nos pontos onde o trabalho repetitivo, previsível ou cansativo estava travando a gente.

O padrão ficou mais ou menos assim:

```
Ideia -> Estruturar a história -> Quebrar em tarefas -> Implementar -> Validar -> Analisar -> Documentar
```

Na etapa de **hipótese**, a IA ajudou a questionar suposições e abrir o leque de soluções. Não porque ela trouxe a resposta certa, mas porque forçou a olhar ângulos que a gente ia ignorar.

```
Prompt: "Me dê 5 formas alternativas de reduzir fricção nesta etapa do funil
        sem mudar preço nem adicionar uma nova tela."
```

Na etapa de **especificação**, a IA ajudou a transformar ideias brutas em rascunhos de user stories, critérios de aceitação e tarefas de Jira que o time depois refinava junto.

```
Prompt: "Quebre este experimento em tarefas de frontend, backend, analytics e QA
        com critérios de aceitação iniciais."
```

Na etapa de **implementação**, agentes de código ajudaram com a estrutura inicial, sugestões de refatoração e expansão de testes. O ganho não foi "assumir o volante". Foi tirar o peso da página em branco e de boa parte do trabalho repetitivo dos primeiros rascunhos.

Na etapa de **validação**, a IA ajudou a levantar casos de borda e revisar a lógica antes mesmo do code review começar.

```
Prompt: "Liste edge cases prováveis para esta mudança no checkout
        e sugira testes que capturariam regressões."
```

Na etapa de **medição**, a IA ajudou a rascunhar SQL, estruturar resumos de experimento e acelerar a primeira passada de análise.

```
Prompt: "Escreva uma query SQL para comparar conversão, taxa de abandono
        e taxa de erro antes e depois deste experimento."
```

E na etapa de **documentação**, ela ajudou a registrar o que a gente estava aprendendo pra o conhecimento não ficar preso na cabeça de duas ou três pessoas.

> Não é sobre automação. É sobre ampliar o que o time consegue fazer.

Esse jeito de pensar me mantém honesto. A IA pode acelerar o trabalho, mas o time ainda precisa de julgamento, contexto, responsabilidade e cuidado.

## A fricção interna era o problema que a gente não tinha nomeado ainda

Uma coisa foi ficando mais clara enquanto a gente empurrava por mais agilidade nos experimentos. Os clientes não eram os únicos sofrendo com atrito. A gente também.

Parte desse atrito era fácil de ignorar porque tinha virado normal. Setup repetitivo. Passos manuais de validação. Debug lento. Dependência de pessoas que tinham contexto que os outros ainda não tinham. Espera longa pra entender o que tinha acontecido. Análises frágeis. Pequenas taxas constantes sobre o progresso.

Nenhum desses problemas parecia dramático sozinho. Juntos, eles travavam o sistema.

Essa foi uma das viradas de chave mais úteis pra mim:

> Clientes sentem atrito no funil. Times sentem atrito na execução.

Quando comecei a enxergar melhor o atrito interno, parei de tratar ele como ruído de fundo. Passei a tratar como problema de produto. Algo observável. Algo que dava pra melhorar.

Essa mudança alterou a conversa. A gente não estava só perguntando como melhorar o produto. Também estava perguntando como melhorar a forma que usávamos pra melhorar o produto.

## Uma regra simples que deixou tudo mais claro

Com o tempo, uma regra prática foi se mostrando cada vez mais útil:

> Se uma tarefa é repetitiva e previsível, ela é candidata a acelerar.

Nem toda tarefa repetitiva deve ser automatizada. Nem toda tarefa previsível vale otimizar. Mas essa regra ajudou a perceber onde o tempo estava sendo gasto sem muito retorno.

Na prática, ficou assim:

| Atividade repetitiva | Como a IA ajudou |
| --- | --- |
| Escrever user stories | Primeira estrutura e critérios de aceitação |
| Quebrar trabalho em tarefas | Decomposição inicial em tarefas de Jira |
| Expandir testes | Casos de borda extras e cobertura de cenários |
| Revisar riscos | Apontar pontos cegos e regressões prováveis |
| Rascunhar queries de análise | Pontos de partida em SQL pra revisar experimentos |
| Escrever resumos | Primeiros rascunhos de recap de experimento |

Não era trabalho glamouroso. Era algo melhor: trabalho útil.

E trabalho útil, quando se repete o suficiente, muda o ritmo de entrega do time.

## Construindo ferramenta enquanto eu continuava liderando

Em certo ponto, a agilidade nos experimentos expôs outro problema. Debug e validação estavam demorando demais. A gente conseguia desenhar e lançar experimentos, mas entender o comportamento e ler os resultados ainda tinha atrito demais.

Aí ficou a escolha clássica. Esperar um investimento maior de plataforma. Pedir mais gente. Ou construir algo menor a gente mesmo.

A gente construiu.

Enquanto eu seguia gerenciando o time e apoiando o fluxo geral do trabalho, comecei a fazer vibe coding de uma ferramenta leve em Go pra debug, focada em visibilidade e análise. O objetivo não era criar uma plataforma polida. Era remover um gargalo que já estava custando velocidade.

Essa parte importa pra mim porque fica na interseção entre liderança e construção. Não acho que gerir time deva significar se afastar demais de como o trabalho acontece na prática. Às vezes, a coisa de maior retorno que uma liderança pode fazer é remover diretamente uma trava estrutural.

A ferramenta ajudou a inspecionar fluxos mais rápido, validar suposições com menos cerimônia e reduzir parte da dependência entre times quando precisávamos de respostas rápidas. Ela também virou algo que outras pessoas puderam usar depois, e é assim que muitas ferramentas internas pequenas acabam se justificando.

```bash
# Exemplo de uma mentalidade de debug leve
odebug inspect --flow checkout --experiment EXP-142
odebug trace --session 8f31a2
odebug compare --before control --after variant-a
```

Quero deixar claro aqui. Isso não é história de heroísmo. Não é "olha o que uma pessoa construiu de madrugada". Essa não é a lição que me interessa.

A lição é mais simples.

> Uma ferramenta leve pode criar bastante retorno quando tira um atrito recorrente do caminho do time.

E a IA tornou mais fácil construir esse tipo de ferramenta pequena e prática do que era antes.

## O que "10x mais produtivo" é e o que não é

Eu tomo cuidado com expressão como "produtividade 10x" porque é fácil de usar errado. Pode soar como marketing. E também pode reduzir um sistema complexo a uma frase rasa sobre indivíduos.

Não acho que a versão interessante de 10x seja sobre um engenheiro digitando mais rápido que outro.

A versão mais honesta é sobre **o ritmo de entrega do time como um todo**.

Isso significa fazer perguntas diferentes:

- A gente está entregando experimentos com mais frequência?
- A gente está validando com mais segurança?
- A gente está gastando menos tempo com atrito que dava pra evitar?
- A gente está aprendendo mais rápido sem baixar a barra de qualidade?

Essa mudança importa porque tira a conversa da mitologia individual e leva pra como o time funciona.

Uma forma mais concreta de pensar nisso:

| Foco em produtividade individual | Foco no ritmo do time |
| --- | --- |
| Gerar código mais rápido | Ciclo mais rápido entre hipótese e decisão |
| Mais linhas alteradas | Mais experimentos concluídos com segurança |
| Velocidade pessoal | Velocidade de aprendizado do time |
| Eficiência isolada | Ganho compartilhado |

Não é sobre engenheiro-herói. É sobre construir um jeito de trabalhar que deixe o fluxo normal de engenharia acontecer com menos arrasto.

No nosso caso, os ganhos reais não foram mágicos. Apareceram em ciclos mais curtos, validação mais rápida, melhor visibilidade e estruturas mais reutilizáveis ao redor do trabalho.

## O que não mudou

Essa parte é importante porque protege o argumento inteiro de virar ingenuidade.

A gente não parou de revisar código com cuidado. Não removeu checks de CI. Não afrouxou as expectativas de qualidade. Não entregou responsabilidade pra um modelo. Não fez de conta que saída gerada por IA era confiável por padrão.

Essas proteções continuaram importando. Se for pra falar a verdade, passaram a importar ainda mais.

| O que ficou igual | Por que continuou importante |
| --- | --- |
| Fluxo de Git | Disciplina compartilhada e rastreabilidade |
| Checks de CI/CD | Rede de segurança confiável |
| Code review rigoroso | Julgamento humano nas mudanças críticas |
| Responsabilidade do time | O dono do trabalho continuou sendo a gente |
| Pensamento arquitetural | Velocidade ainda precisa de direção |

> A IA acelerou a execução. Ela não tirou a responsabilidade.

Essa frase resume o equilíbrio que eu quero preservar. Sem isso, a velocidade fica frágil.

## Na prática, o ganho foi acumulando

O que começou como algumas acelerações em tarefas isoladas foi mudando o ritmo do sistema.

Testar mais barato abriu espaço pra mais experimentos. Mais experimentos geraram mais aprendizado. Mais aprendizado aumentou a confiança. Essa confiança tornou mais fácil fazer apostas melhores. Com o tempo, o time não estava só andando mais rápido. Estava aprendendo de forma mais contínua.

O formato desse acúmulo ficou mais ou menos assim:

```
IA apoiando o ciclo
-> testar ficou mais barato
-> mais experimentos rodando
-> mais observações
-> decisões melhores
-> mais confiança
-> próximas apostas mais fortes
```

Gosto dessa forma de ver porque evita o hype. Não diz que a IA resolveu tudo. Só mostra como pequenas reduções de atrito podem se acumular num ganho real de operação.

É aí também que liderança volta pra conversa. Não precisa perguntar só se a IA está sendo usada. Isso é raso demais. A pergunta melhor é: onde iterar ainda está desnecessariamente caro?

Essa pergunta me levou a outras:

- Onde a gente ainda está fazendo trabalho manual que dava pra evitar?
- Onde o contexto está concentrado demais?
- Onde os atrasos vêm de incerteza e não de complexidade real?
- Que trabalho a gente está tolerando só porque virou hábito?

Essas me parecem perguntas melhores de quem quer de fato melhorar como o time trabalha.

## Uma reflexão mais ampla

Não acho que IA crie vantagem automaticamente. Ter acesso, por si só, não resolve nada. Muitos times têm acesso às mesmas ferramentas.

O que parece importar mais é se o time consegue mudar seus hábitos, seus fluxos e seus ciclos de decisão em torno dessa nova realidade. Isso é menos dramático do que a narrativa usual sobre IA, mas é mais útil.

Não é sobre substituir engenheiros. É sobre dar ao time mais formas de tirar o arrasto do ciclo de aprendizado.

E isso ainda não acabou. Não acho que a gente chegou num modelo final. Ainda tem muito pra aprender sobre quando confiar na aceleração, quando segurar e como evitar transformar conveniência em preguiça. Essas não são perguntas pequenas.

Mas eu tenho mais clareza agora sobre um ponto do que tinha antes:

> O benefício real da IA em engenharia não é escrever código. É ajudar a reduzir o custo de aprender.

Essa é a mudança que eu acho que vale perseguir.

Então talvez a pergunta pra levar pra sua própria semana não seja "como a IA pode me ajudar a andar mais rápido?". Talvez seja algo mais específico e mais honesto:

**Onde iterar ainda está caro demais na forma como você e seu time trabalham hoje?**
