---
title: "Co-Inteligência: Vivendo, Trabalhando e Fazendo Rubber Ducking com IA"
categories:
  - AI
  - Productivity
  - Engineering Management
date: 2025-03-04
tags:
  - ia
  - co-inteligencia
  - produtividade
  - praticas-de-engenharia
  - rubber-ducking
  - fluxo-de-trabalho
  - automacao
  - colaboracao
---

No dia 4 de março de 2025, apresentei uma palestra no capítulo de IA da Engenharia da Omio sobre algo que venho explorando — não só de forma teórica, mas na prática do dia a dia. A palestra se chamava **"Co-Inteligência: Vivendo, Trabalhando e Fazendo Rubber Ducking com IA"**, e não falava sobre um futuro distante com inteligência artificial geral, nem sobre substituição de empregos. O foco era em como já está mudando a forma como eu programo, depuro, aprendo e tomo decisões.

Estamos em um momento estranho da engenharia. Toda semana surgem novas capacidades com copilotos e assistentes, mas a maioria dos times ainda trata essas ferramentas como ajudantes, não como colaboradoras. Essa palestra foi a minha tentativa de provocar uma mudança nesse comportamento.

Aqui estão os slides completos da apresentação:

<iframe class="speakerdeck-iframe" frameborder="0" src="https://speakerdeck.com/player/39ec661d8d5e44d39aac7dda2af62f90" title="Co-Intelligence-Living-Working-and-Rubber-Ducking-with-AI" allowfullscreen="true" style="border: 0px; background: padding-box padding-box rgba(0, 0, 0, 0.1); margin: 0px; padding: 0px; border-radius: 6px; box-shadow: rgba(0, 0, 0, 0.2) 0px 5px 40px; width: 100%; height: auto; aspect-ratio: 560 / 315;" data-ratio="1.7777777777777777"></iframe>

## Rubber Ducking Reimaginado

Se você já explicou um problema para um pato de borracha para depurar código, você entende metade da ideia. O pato não resolve nada — ele te força a desacelerar, explicar com clareza e perceber o que estava te escapando. Agora imagine se o pato responde, questiona suas premissas e às vezes encontra falhas que você nem sabia que existiam.

É assim que vejo a co-inteligência na prática. Explicar seu plano, uma ideia de refatoração ou um erro obscuro para um LLM cria um ciclo de conversa que torna seu pensamento mais afiado. Não se trata de automação. É sobre **aumentar a capacidade humana**.

Em um dos exemplos que compartilhei durante a apresentação, partimos de um título vago em um ticket do Jira para uma lista concreta de casos de borda e notas de implementação — apenas pedindo ao GPT para agir como um engenheiro sênior conduzindo um kickoff. Em outro momento, mostramos como um teste instável voltou a ser confiável após o modelo simular múltiplos caminhos de falha e nos ajudar a formular hipóteses para a causa raiz.

Em outro caso, usamos o GPT para examinar um log caótico de postmortem e transformá-lo em uma sequência de perguntas causais: _"O que mudou no último deploy?"_, _"O que havia de diferente em produção versus staging?"_ Não se tratava apenas de resumir — era sobre fazer as perguntas certas. Do tipo que um SRE calmo faria às 3 da manhã. Ainda não chegamos lá, mas não é absurdo imaginar que a IA venha a assumir parte do papel de assistente de plantão: analisando logs, conectando alertas a falhas conhecidas ou ...

## Quando as Ferramentas Mudam, o Processo Precisa Acompanhar

Se a forma como trabalhamos não mudou no último ano, não é porque a IA não evoluiu. É porque ainda não deixamos ela nos transformar.

Defendi que o atrito invisível do trabalho de engenharia — entender histórias, depurar sistemas instáveis, entrar em novos stacks — pode ser drasticamente reduzido quando a IA faz parte do seu fluxo. Mas isso exige mais do que instalar um plugin.

Exige repensar os rituais do time. Ainda precisamos de reuniões de refinamento tradicionais se engenheiros já fazem pré-refinamento com GPT? Qual o papel de um mentor sênior se um júnior pode simular uma sessão de pair programming com Claude ou ChatGPT? Como garantir qualidade e rastreabilidade quando alguns commits são co-escritos por um assistente?

Essas não são questões resolvidas, mas ignorá-las gera dívida técnica na forma como lideramos equipes.

## O Humano Continua no Comando — Mas Não Está Sozinho

Um dos momentos mais marcantes da apresentação foi a demonstração de como co-projetamos uma ferramenta interna. Começamos com um prompt em branco, pedimos ao LLM para simular um PM e definir a dor do usuário. Depois, ele virou designer e sugeriu três opções de layout. Em seguida, gerou uma API esqueleto e critérios de aceitação. Por fim, simulamos um QA explorando os limites da aplicação.

Cada persona era uma caricatura rasa, mas juntas criaram um **loop rápido e multifuncional** que usamos para receber feedback antes de escrever uma linha de código.

Esse processo não elimina a colaboração humana — ele só acelera o caminho até o primeiro rascunho que vale a pena discutir.

Uma lição recorrente: o verdadeiro poder dessas ferramentas aparece quando você para de tratá-las como mecanismos de resposta e começa a usá-las como mecanismos de estrutura. No início, eu pedia ao GPT "o código certo". Mas o que funcionava melhor era perguntar _"Você pode me ajudar a estruturar isso?"_ ou _"Quais perguntas ainda não estou fazendo?"_ Promptar, no fim das contas, é um exercício de reflexão. Os engenheiros que tiram mais proveito dessas IAs tratam o prompt como um quadro branco, não como uma...

## Uma Mudança de Cultura Já Está Acontecendo

Na Omio, estamos mudando a cultura de engenharia aos poucos. Estimulamos o uso da IA para planejamento, testes e documentação. Criamos canais de Slack para compartilhar prompts. E começamos a medir onde ela poupa tempo — e onde gera dúvidas.

Os primeiros resultados são animadores. Aumentamos a velocidade de onboarding. As discussões técnicas ficaram mais focadas. E, acima de tudo, há uma nova sensação de que aprender é constante — especialmente quando você pode fazer perguntas infinitas para uma máquina paciente e rápida que nunca se cansa.

## Tudo Começa com uma Pergunta

Terminei a palestra com uma provocação simples: se você já colou uma mensagem de erro no ChatGPT, você já começou essa jornada.

A única pergunta que resta é: **quão longe você está disposto a ir com isso?**

Você está usando IA só para reduzir tarefas repetitivas, ou para repensar como trabalha? Está pedindo para ela completar código, ou revisar suas decisões? Você a vê como uma ferramenta — ou como um pato de borracha com superpoderes e paciência infinita?

Aqui vai um desafio: escolha uma tarefa essa semana — depurar um bug, planejar uma história, até nomear uma função — e, em vez de perguntar _"Como resolvo isso?"_, pergunte _"Como eu resolveria isso com IA?"_ Deixe que ela desafie você. Deixe que ela reflita algo de volta. Essa é a mudança. Não é sobre pensar menos. É sobre pensar com melhores espelhos.

---

Quero ouvir de você. O que mudaria no seu dia a dia se você parasse de tratar a IA como atalho e começasse a tratá-la como colega?
