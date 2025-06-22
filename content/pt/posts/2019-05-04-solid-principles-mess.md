---
title: "Princípios SOLID e a Bagunça em que Estamos"
date: 2019-05-04T14:00:00-03:00
author: Helio Medeiros
subtitle: Escape do inferno dos microsserviços aplicando princípios SOLID em nível de sistema—transformando caos distribuído em contextos delimitados com responsabilidades claras e arquitetura sustentável
tags:
  [
    "princípios solid",
    "microsserviços",
    "design de sistemas",
    "arquitetura",
    "engenharia de software",
    "sistemas distribuídos",
    "bounded contexts",
    "domain-driven design",
  ]
categories: ["Technology", "Architecture"]
---

Já passamos por isso. A indústria é cíclica. Centralização, descentralização. Monolitos, microsserviços. Mas se você está lendo isso, provavelmente está passando por uma transformação para microsserviços ou, pior ainda, lidando com as consequências de uma mal executada. E está se perguntando: como chegamos a esse caos distribuído?

Para entender isso, precisamos recuar um pouco. A orientação a objetos nos ensinou a dividir os problemas em pedaços pequenos que interagem por mensagens. Esses objetos são leves, reutilizáveis e verborrágicos. Isso funciona dentro de um processo. Mas coloque uma rede entre eles e tudo muda.

Martin Fowler já disse: "A primeira lei do design de objetos distribuídos: Não faça."

Então como fomos parar em um mundo onde todo slide de arquitetura tem um diagrama intitulado "Nosso Landscape de Microsserviços"?

## Por que Microsserviços, afinal?

Microsserviços, apesar do hype e das definições vagas, fazem bem uma coisa: forçam limites. Em vez de milhares de classes agrupadas, você (idealmente) tem unidades implantáveis com seus próprios times, ciclos de vida e responsabilidades.

A palavra-chave é _idealmente_. Na prática, muitas empresas passaram de monolitos sem limites para sistemas distribuídos sem limites. Todo o acoplamento, agora com latência.

Os benefícios existem — mas só quando tratamos os microsserviços como serviços de granularidade grossa, não como objetos distribuídos. É aí que os princípios SOLID entram.

## Bounded Contexts e a Maldição do "Micro"

Serviços pequenos demais se tornam como objetos: dependentes, verborrágicos e frágeis. Se você precisa alterar três serviços só para renomear um campo, criou um sistema distribuído de objetos, não um sistema orientado a serviços.

A solução não é abandonar modularidade, mas repensar o que é um módulo. Entra em cena o conceito de Bounded Context — da modelagem estratégica do Domain-Driven Design — que nos incentiva a agrupar modelos, vocabulário e comportamento dentro de limites claros.

Comece pela linguagem. Se sua equipe diz "reserva" em um lugar e "pedido" em outro para significar a mesma coisa, você encontrou um limite. Se "usuário" significa cinco coisas diferentes no seu sistema, trace as linhas.

Bounded Contexts nos dão o espaço natural para aplicar SOLID.

## Aplicando SOLID em Microsserviços

Não trate SOLID como algo de classe. Veja como um **heurístico sistêmico de design**. Veja como cada princípio ajuda a domar seu inferno de microsserviços:

| Princípio | Interpretação Sistêmica                            | Exemplo                                             |
| --------- | -------------------------------------------------- | --------------------------------------------------- |
| SRP       | Cada serviço deve fazer bem uma única coisa        | Não misture cobrança com suporte ao cliente         |
| OCP       | Adicione comportamento sem alterar contratos       | Use versionamento de API e feature flags            |
| LSP       | Substitua serviços sem quebrar consumidores        | Deploys blue-green com respostas compatíveis        |
| ISP       | Clientes não devem depender do que não usam        | APIs especializadas para mobile, frontend etc.      |
| DIP       | Serviços dependem de contratos, não implementações | Publique eventos de domínio, evite chamadas diretas |

## Revisitando os Cheiros

Os velhos conhecidos — rigidez, fragilidade, imobilidade, viscosidade — estão todos presentes nos microsserviços.

- **Rigidez**: Mudança no Serviço A quebra o Serviço B? Falta versionamento.
- **Fragilidade**: Feature flags e configs misturadas? Reavalie sua estratégia de release.
- **Imobilidade**: Quer reutilizar lógica mas ela está acoplada ao Kafka, Postgres e Prometheus? Extraia o domínio.
- **Viscosidade**: Endpoints se acumulam porque mudar a abstração é doloroso? Isso é viscosidade arquitetural.

Os mesmos princípios que melhoram seu código também funcionam aqui. Mas agora o preço de ignorá-los não é só um teste quebrado — é um incidente em produção.

## A Jornada de Crescimento

Startups não precisam de microsserviços. Elas precisam validar produto.

Scale-ups precisam sobreviver à entropia. É aqui que SOLID começa a importar.

Empresas em escala global têm problemas diferentes — performance, custo, latência — mas também precisam de limites. Só que eles se desenham em torno de confiabilidade e infraestrutura.

## Consideração Final

Microsserviços não são objetivo. São troca.

Se você desenha sistemas sem princípios, só vai escalar o caos.

Bounded Contexts te dão o vocabulário. SOLID te dá a disciplina.

Sem os dois, você não está construindo sistemas — está distribuindo arrependimentos.
