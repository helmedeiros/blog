---
title: "Da Sensibilidade a Preço aos Modelos de Pricing"
categories:
  - Data
  - Engineering
  - Pricing
  - Product
date: 2024-09-25
tags:
  - pricing
  - modelos-de-pricing
  - experimentacao
  - monetizacao
  - tomada-de-decisao
  - estrategia-de-produto
description: "Entender o comportamento do cliente não bastava. A gente precisava de uma forma de tomar decisões de pricing com consistência em escala."
subtitle: "Um modelo não é mais esperto que o processo de aprendizado que o produziu. Ele só torna esse aprendizado mais fácil de aplicar repetidamente."
---

Uma plataforma de pricing pode saber muito sobre os próprios clientes e ainda assim não conseguir agir sobre isso.

Soa errado da primeira vez que você lê. Conhecimento, em tese, vira ação. Mas depois de alguns anos trabalhando em uma plataforma que decidia o que cobrar dos clientes e quando, a distância entre os dois ficava visível de dentro.

Nessa altura, o sistema já tinha absorvido lições o bastante para se tornar perigoso. O "cliente médio" tinha deixado de ser um conceito útil. A resposta do cliente ao preço tinha deixado de parecer um número e passado a parecer uma curva. E toda mudança tinha deixado de soar como uma única decisão e passado a soar como uma pilha de trade-offs — receita contra conversão, confiança, retenção, simplicidade.

O que o sistema não tinha era uma forma de aplicar nada disso de forma consistente.

Entender uma curva e agir sobre uma curva são duas coisas diferentes.

## O limite da tomada de decisão humana

Imagine um mundo com um único tipo de cliente. Uma curva de resposta. Um objetivo. Uma decisão de pricing.

Humanos são notavelmente bons em raciocinar sobre esse tipo de problema.

Agora imagine centenas de contextos de cliente que importam. Comportamentos diferentes. Trade-offs diferentes. Respostas diferentes a valor.

O desafio muda.

O problema não é mais entender o cliente. O problema é aplicar o que a gente aprendeu de forma consistente.

Foi nesse ponto que pricing parou de parecer um problema de regras e começou a parecer um problema de tomada de decisão.

## Uma regra te diz o que fazer

Regras são excelentes quando o mundo é razoavelmente previsível.

> Se X, então Y.

Essa estrutura é fácil de explicar. Fácil de testar. Fácil de governar.

Mas regras têm limite. Conforme mais sinais ficam relevantes, o número de combinações cresce rápido.

Um sistema baseado em regras consegue *descrever* complexidade. Em algum momento ele tem dificuldade em *raciocinar* sobre ela.

O desafio já não era mais expressar decisões de negócio. Era escolher entre milhares de resultados possíveis.

## Um modelo te diz o que provavelmente vai acontecer

Foi aqui que modelos de pricing entraram na conversa.

Não porque modelagem estava na moda. Não porque a organização queria mais tecnologia. Porque o sistema de aprendizado tinha acumulado mais conhecimento do que a camada de regras conseguia expressar à mão.

Uma forma útil de pensar em um modelo é como uma compressão de tudo o que o time aprendeu até ali:

{{< plantuml title="Um modelo é uma compressão do que a organização aprendeu" >}}
@startuml
skinparam shadowing false
skinparam componentStyle rectangle

[Experimentos] as E
[Comportamento do cliente] as CB
[Resultados históricos] as HO
[Sensibilidade a preço] as PS
[Modelo] as M
[Previsão] as P

E --> M
CB --> M
HO --> M
PS --> M
M --> P
@enduml
{{< /plantuml >}}

O modelo não substitui o aprendizado. O modelo é uma representação do aprendizado. Ele comprime milhares de observações em algo que ajuda a tomar uma decisão.

## Modelos não são mágica

Uma ideia equivocada que eu encontrava repetidamente era a crença de que um modelo, de alguma forma, descobre a verdade.

A realidade é menos dramática.

Um modelo só sabe o que a organização já aprendeu. Experimentos ruins criam dados ruins. Dados ruins criam modelos ruins. Modelos ruins criam decisões ruins.

O modelo não é mais esperto que o processo de aprendizado que o produziu. Ele só torna esse aprendizado mais fácil de aplicar repetidamente.

Essa distinção importa porque mantém o foco na qualidade do ciclo de feedback, não na sofisticação do algoritmo.

## Consistência virou mais valiosa que inteligência

Uma lição me surpreendeu.

O maior benefício de um modelo de pricing não era inteligência. Era consistência.

Humanos são inconsistentes. Pessoas diferentes interpretam a mesma informação de forma diferente. Prioridades mudam. Contexto é esquecido. Regras acumulam exceções.

Um modelo aplica o mesmo arcabouço de raciocínio toda vez. Isso não garante uma resposta perfeita. Mas cria um processo previsível.

E processos previsíveis são mais fáceis de melhorar do que processos imprevisíveis.

## Todo modelo embute trade-offs

Trade-offs não desaparecem quando um modelo chega. Eles ficam codificados.

Um modelo não consegue otimizar tudo ao mesmo tempo. Algum objetivo precisa ser escolhido — receita, conversão, valor do cliente, retenção, lucratividade — e o modelo simplesmente operacionaliza aquela prioridade.

Isso significa que desacordos sobre pricing costumam ser desacordos sobre objetivos, não sobre algoritmos. A matemática normalmente vem depois. As escolhas estratégicas vêm antes.

## O primeiro modelo raramente é o modelo final

Outra lição que vale compartilhar é que o primeiro modelo bem-sucedido normalmente é simples.

Isso é uma feature, não uma limitação.

Modelos simples são mais fáceis de explicar. Mais fáceis de validar. Mais fáceis de questionar. Mais fáceis de confiar.

Muitos times pulam direto para sofisticação. A pergunta melhor, em geral, é:

> Qual é o modelo mais simples que melhora a qualidade da decisão?

Complexidade é fácil de adicionar depois. Confiança é muito mais difícil de adicionar depois.

## Modelos criam riscos novos

Modelos de pricing resolvem alguns problemas e introduzem outros.

Um modelo desatualizado pode se descolar da realidade. Um modelo overfitted pode aprender padrões que não generalizam. Um modelo bem-sucedido pode influenciar o comportamento do cliente e, aos poucos, invalidar as próprias suposições.

O resultado é outra percepção importante.

Modelos não são produtos. Modelos são sistemas vivos. Eles exigem monitoramento, validação, revisão, aposentadoria.

O ciclo de vida nunca desaparece. Ele só se move para outra camada da plataforma.

## O que aprendi

A coisa mais importante que os modelos de pricing nos deram não foi automação. Foi alavancagem.

Um time só consegue discutir um certo número de decisões de pricing por trimestre. Um modelo é o que faz com que algumas opiniões honestas sobre valor, disposição a pagar e segmentação virem a base para milhares de decisões consistentes por dia. Bem feito, o modelo não substitui o julgamento humano. Ele carrega esse julgamento adiante em escala.

Mal feito, ele carrega o julgamento errado adiante, na mesma escala. Modelos são alavancagem nas duas direções.

## Reflexão final

Entender o comportamento do cliente foi difícil. Transformar esse entendimento em decisões consistentes foi mais difícil. Modelos de pricing ajudaram a fechar essa distância.

O alerta que eu daria a uma versão mais nova de mim é: seja honesto sobre quando um modelo está, de fato, ganho. Um time que ainda não teve a própria segmentação questionada, que ainda não foi forçado a escolher entre receita e retenção, que ainda não viu os próprios experimentos falharem de formas que doeram — esse time não tem nada para comprimir. Colocar um modelo em cima de um modelo mental que nunca foi testado não acelera decisões boas. Industrializa as suposições que por acaso estavam mais altas na sala.

A pergunta interessante, então, não é quando um time está pronto para construir um modelo. É se o time já errou o suficiente para saber para *que* o modelo serve.
