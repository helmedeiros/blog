---
title: 'WS-46 com Phillip Calçado: Meu Primeiro Mergulho Real em Domain-Driven Design'
author: helio
layout: post
date: 2009-11-18 23:37:20+00:00
dsq_thread_id:
- 4969844886
categories:
- Architecture
- Technology
tags:
- Caelum
- DDD
- Domain-Driven Design
- Phillip Calçado
- Rio
- WS-46
- Modelagem
- Linguagem Ubíqua
- Arquitetura
subtitle: Conceitos e práticas de desenvolvimento de software
---

No dia 17 de novembro de 2009, participei de um workshop que se tornou um divisor de águas na minha trajetória como desenvolvedor. Foi o curso **WS-46 da Caelum sobre Domain-Driven Design (DDD)** com **Phillip Calçado** — nome que eu já acompanhava havia tempos, seja pelo blog ou pelas apresentações.

Não era um curso sobre frameworks ou sobre como usar melhor o Java. Era um curso sobre **como pensar, modelar e se comunicar ao construir software de verdade**. Para alguém como eu, apaixonado por clean code, padrões de projeto e programação orientada a objetos — mas sem experiência prática ou mentoria em DDD — foi um choque de realidade e aprendizado.

## A Abertura: O quê, como e qual?

Phillip abriu o curso com três perguntas simples, mas profundas:

- **O quê** estamos construindo?
- **Como** esperam que façamos isso?
- **Qual** decisão podemos tomar frente aos compromissos do projeto?

Essa abordagem moldou todo o workshop. Fomos divididos em grupos para modelar um sistema real (um estacionamento), apenas com histórias de usuário. Sem classes prontas. Sem diagrama pronto. Só conversa, análise e decisões.

## A linguagem é o modelo

Um dos conceitos mais repetidos durante o curso foi o de **linguagem ubíqua**. Não é apenas um glossário técnico — é uma disciplina em que todos os nomes de classes, métodos e diagramas devem refletir o mesmo vocabulário compartilhado com os especialistas do negócio.

Phillip reforçou que um modelo só é útil se for **implementado em código e usado em reuniões**. Do contrário, caímos na velha armadilha de traduzir requisitos, o que gera bugs e má comunicação.

> "O maior valor de um modelo de domínio é fornecer uma linguagem que conecta desenvolvedores e especialistas."

## Sprint de Modelagem

Durante mais de quatro horas, só modelamos. Sem código. Sem padrão. Só rascunhos, discussões, refatorações e redefinições.

Só **depois** de termos um entendimento comum, começamos a trabalhar com os blocos:

| Bloco de Construção | Propósito                                                |
| ------------------- | -------------------------------------------------------- |
| Entidade            | Objeto com identidade que evolui ao longo do tempo       |
| Objeto de Valor     | Imutável, definido por seus atributos                    |
| Agregado            | Agrupamento de objetos governado por uma raiz            |
| Repositório         | Interface para acessar e persistir agregados             |
| Serviço             | Operação que não se encaixa naturalmente em uma entidade |

## Ciclo de Vida e o Problema do ID Falso

Phillip abordou o problema de projetar entidades sem identidade real. Ele referenciou seu post clássico ["Don't Trust Fake IDs"](http://philcalcado.com/2009/10/12/dont-trust-fake-ids/) e mostrou como deixar o banco ditar o design é um erro.

> "Se você não sabe quem é um objeto sem o banco, ele não é uma entidade — é só uma linha."

No nosso grupo, discutimos se `TicketDeEstacionamento` deveria ser entidade ou objeto de valor. A resposta dependia do comportamento que queríamos representar — e _esse_ era o aprendizado.

## Arquitetura em Camadas na Prática

Exploramos a estrutura tradicional de camadas do DDD, mas sempre focando no comportamento e no fluxo — e não no framework.

| Camada         | Papel                                                       |
| -------------- | ----------------------------------------------------------- |
| Domínio        | Coração da lógica de negócio e das invariantes              |
| Aplicação      | Coordena os casos de uso e a interação com o domínio        |
| Infraestrutura | Interface com banco de dados, APIs, filas, mensageria, etc. |
| Apresentação   | Interface com usuário (UI, REST, eventos...)                |

Phillip era cético com overengineering. Só adicionava camada se ela ajudasse na **clareza do domínio**.

## Quando Não Dá Pra Falar de DDD

Um dos aprendizados mais libertadores: você não precisa usar termos como "Aggregate" ou "Entidade" para aplicar DDD. Muitas vezes, Phillip evita esses termos com clientes e foca em **modelar responsabilidades e fluxos naturais**.

Isso me deu confiança para começar a aplicar os conceitos mesmo em projetos que não eram "greenfield".

## O Erro Comum do Mercado

Com base em seu texto ["Nevermind Domain-Driven Design"](https://philcalcado.com/2010/03/22/nevermind_domain_driven_design.html), ele criticou a obsessão da indústria por repositórios e camadas técnicas, ignorando a essência: **a linguagem e o modelo alinhado com o negócio**.

> "Se tudo que você levou do DDD foi uma classe Repository, você perdeu o ponto."

## Exemplo: Sistema de Estacionamento (UML)

Aqui está um modelo simplificado baseado no exercício do curso:

![Modelo de Domínio do Estacionamento](https://yuml.me/diagram/scruffy/class/[Estacionamento]1-*%3E[Vaga],[Vaga]0..1-%3E[Veículo],[TicketDeEstacionamento]^-[ObjetoValor],[Cliente]1-*%3E[TicketDeEstacionamento])

Discutimos profundamente se o ticket era uma entidade. A resposta dependia do que queríamos **garantir** no nosso domínio.

## Design como Conversa

Mais do que código, DDD virou uma forma de conversar. Nome de classe, regra de validação, método público — tudo comunica o que entendemos do domínio.

Comecei a enxergar código não só como instrução, mas como **documentação de entendimento**.

## Considerações Finais

Esse foi um dos melhores cursos técnicos que já participei. Não por slides (quase não teve), nem por ferramentas (mal abrimos a IDE). Mas porque me ensinou **uma forma de pensar e modelar**.

Phillip foi generoso, claro, provocativo. Mostrou que DDD não é religião nem bala de prata. É postura — começa com escuta, nomeação e iteração, não com framework.

Se tiver oportunidade de fazer um curso com ele, vá.

---

_Postado no dia seguinte ao curso WS-46, ainda empolgado com tudo que aprendi._
