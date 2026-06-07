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
series:
  - pricing-platform
series_order: 10
description: "Entender o comportamento do cliente não bastava. A gente precisava de um jeito de tomar decisão de pricing com consistência em escala."
subtitle: "Um modelo não é mais esperto que o processo de aprendizado que produziu ele. Só torna esse aprendizado mais fácil de aplicar repetidamente."
---

Uma plataforma de pricing pode saber muito sobre os próprios clientes e ainda assim não conseguir agir sobre isso.

Soa errado quando você lê pela primeira vez. Conhecimento, em tese, vira ação. Mas depois de alguns anos trabalhando numa plataforma que decidia o que cobrar do cliente e quando, a distância entre os dois ficava visível por dentro.

Nessa altura, o sistema já tinha absorvido lição o bastante pra se tornar perigoso. O "cliente médio" tinha deixado de ser um conceito útil. A resposta do cliente ao preço tinha deixado de parecer um número e passado a parecer uma curva. E toda mudança tinha deixado de soar como uma decisão e passado a soar como uma pilha de trade-offs — receita contra conversão, confiança, retenção, simplicidade.

O que o sistema não tinha era um jeito de aplicar nada disso de forma consistente.

Entender uma curva e agir sobre uma curva são duas coisas diferentes.

## O limite da tomada de decisão humana

Imagine um mundo com um tipo único de cliente. Uma curva de resposta. Um objetivo. Uma decisão de pricing.

Humano é notavelmente bom em raciocinar sobre esse tipo de problema.

Agora imagine centenas de contextos de cliente que importam. Comportamento diferente. Trade-off diferente. Resposta diferente a valor.

O desafio muda.

O problema não é mais entender o cliente. O problema é aplicar o que a gente aprendeu de forma consistente.

Foi nesse ponto que pricing parou de parecer problema de regras e começou a parecer problema de tomada de decisão.

## Regra te diz o que fazer

Regra é excelente quando o mundo é razoavelmente previsível.

> Se X, então Y.

Essa estrutura é fácil de explicar. Fácil de testar. Fácil de governar.

Mas regra tem limite. À medida que mais sinal vai ficando relevante, o número de combinações cresce rápido.

Um sistema baseado em regras consegue *descrever* complexidade. Em algum momento tem dificuldade de *raciocinar* sobre ela.

O desafio já não era mais expressar decisão de negócio. Era escolher entre milhares de resultados possíveis.

## Modelo te diz o que provavelmente vai acontecer

Foi aqui que modelo de pricing entrou na conversa.

Não porque modelagem estava na moda. Não porque a organização queria mais tecnologia. Porque o sistema de aprendizado tinha acumulado mais conhecimento do que a camada de regras conseguia expressar à mão.

Uma forma útil de pensar num modelo é como uma compressão de tudo o que o time aprendeu até ali:

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

O modelo não substitui o aprendizado. O modelo é uma representação do aprendizado. Comprime milhares de observações em algo que ajuda a tomar uma decisão.

## Modelo não é mágica

Uma ideia equivocada que eu encontrava direto era a crença de que o modelo, de algum jeito, descobre a verdade.

A realidade é menos dramática.

Modelo só sabe o que a organização já aprendeu. Experimento ruim cria dado ruim. Dado ruim cria modelo ruim. Modelo ruim cria decisão ruim.

O modelo não é mais esperto que o processo de aprendizado que produziu ele. Só torna esse aprendizado mais fácil de aplicar repetidamente.

Essa distinção importa porque mantém o foco na qualidade do ciclo de feedback, não na sofisticação do algoritmo.

## Consistência virou mais valiosa que inteligência

Uma lição me surpreendeu.

O maior benefício de um modelo de pricing não era inteligência. Era consistência.

Humano é inconsistente. Pessoa diferente interpreta a mesma informação de forma diferente. Prioridade muda. Contexto é esquecido. Regra acumula exceção.

Um modelo aplica o mesmo arcabouço de raciocínio toda vez. Isso não garante uma resposta perfeita. Mas cria um processo previsível.

E processo previsível é mais fácil de melhorar do que processo imprevisível.

## Todo modelo embute trade-off

Trade-off não desaparece quando o modelo chega. Ele fica codificado.

Modelo não consegue otimizar tudo ao mesmo tempo. Algum objetivo precisa ser escolhido — receita, conversão, valor do cliente, retenção, lucratividade — e o modelo simplesmente operacionaliza aquela prioridade.

Isso significa que desacordo sobre pricing costuma ser desacordo sobre objetivo, não sobre algoritmo. A matemática normalmente vem depois. A escolha estratégica vem antes.

## O primeiro modelo raramente é o modelo final

Outra lição que vale compartilhar é que o primeiro modelo que dá certo, normalmente, é simples.

Isso é feature, não limitação.

Modelo simples é mais fácil de explicar. Mais fácil de validar. Mais fácil de questionar. Mais fácil de confiar.

Muito time pula direto pra sofisticação. A pergunta melhor, em geral, é:

> Qual é o modelo mais simples que melhora a qualidade da decisão?

Complexidade é fácil de adicionar depois. Confiança é muito mais difícil de adicionar depois.

## Modelo cria risco novo

Modelo de pricing resolve alguns problemas e introduz outros.

Modelo desatualizado pode se descolar da realidade. Modelo overfitted pode aprender padrão que não generaliza. Modelo que deu certo pode influenciar o comportamento do cliente e, aos poucos, invalidar as próprias suposições.

O resultado é outra percepção importante.

Modelo não é produto. Modelo é sistema vivo. Exige monitoramento, validação, revisão, aposentadoria.

O ciclo de vida nunca desaparece. Só se move pra outra camada da plataforma.

## O que aprendi

A coisa mais importante que o modelo de pricing deu pra gente não foi automação. Foi alavancagem.

Um time só consegue discutir um certo número de decisões de pricing por trimestre. Modelo é o que faz com que algumas opiniões honestas sobre valor, disposição a pagar e segmentação virem a base pra milhares de decisões consistentes por dia. Bem feito, o modelo não substitui julgamento humano. Carrega esse julgamento adiante em escala.

Mal feito, carrega o julgamento errado adiante, na mesma escala. Modelo é alavancagem nas duas direções.

## Reflexão final

Entender o comportamento do cliente foi difícil. Transformar esse entendimento em decisão consistente foi mais difícil ainda. Modelo de pricing ajudou a fechar essa distância.

O alerta que eu daria a uma versão mais nova de mim é: seja honesto sobre quando o modelo já foi ganho. Um time que ainda não teve a própria segmentação questionada, que ainda não foi forçado a escolher entre receita e retenção, que ainda não viu os próprios experimentos falharem de formas que doeram — esse time não tem nada pra comprimir. Colocar um modelo em cima de um modelo mental que nunca foi testado não acelera decisão boa. Industrializa as suposições que por acaso estavam mais altas na sala.

A pergunta interessante, então, não é quando o time tá pronto pra construir um modelo. É se o time já errou o suficiente pra saber pra *que* o modelo serve.
