---
title: "yUML – Por que escrever um blog?"
date: 2009-08-05T12:03:24+02:00
draft: false
tags: ["UML", "blog", "documentação", "design-de-software", "yUML"]
categories: ["UML", "Ferramentas", "Blog"]
---

Venho tentando há algum tempo criar o hábito de, assim como leio ótimos _posts_, também escrevê-los. Em muitos desses textos vejo a ênfase na importância da disseminação do conhecimento — e é sobre isso que falo neste _post_ de retomada.

Recentemente, foi lançado um novo serviço web que reforça ainda mais essa ideia de compartilhamento técnico: o [yUML](https://yuml.me/).

Para quem nunca ouviu falar: **yUML é uma ferramenta online que permite gerar diagramas UML diretamente a partir de texto simples.** Isso facilita muito a vida de quem escreve sobre design de software e quer ilustrar ideias sem depender de ferramentas pesadas.

## Contexto: UML no Blog

Se você chegou aqui por curiosidade, recomendo antes dar uma olhada neste post anterior:

👉 [UML – Introdução com Minicenários](https://blog.heliomedeiros.com/pt/posts/2008-06-10-uml-introducao-minicenarios/)

Lá eu apresento diagramas de casos de uso e classes, usados para representar pequenos cenários da vida real, como classificados online ou controle de bolão. A ideia com o yUML é facilitar ainda mais essa visualização, de forma direta no blog.

## Exemplo 1: Diagrama de Classe

```text
[Cliente]1-*[Pedido]
[Pedido]++-1>[Pagamento]
```

Visualização:

![Classe](https://yuml.me/diagram/class/plain/[Cliente]1-*%5BPedido%5D,%20[Pedido]++-1%3E%5BPagamento%5D)

Esse exemplo representa:

- Um cliente pode ter vários pedidos.
- Um pedido tem exatamente um pagamento, e o pagamento depende do pedido para existir (composição).

## Exemplo 2: Diagrama de Caso de Uso

```text
[Cliente]-(Consultar Produtos),
[Cliente]-(Fazer Pedido),
[Cliente]-(Cancelar Pedido)
```

Visualização:

![Caso de Uso](<https://yuml.me/diagram/usecase/plain/[Cliente]-(Consultar%20Produtos),[Cliente]-(Fazer%20Pedido),[Cliente]-(Cancelar%20Pedido)>)

Isso modela os principais pontos de interação de um cliente com o sistema de pedidos.

## Exemplo 3: Diagrama de Atividades

```text
(start)->(Validar Dados)->(Criar Conta)->(Enviar Email)->(end)
```

Visualização:

![Atividades](<https://yuml.me/diagram/activity/plain/(start)->(Validar%20Dados)->(Criar%20Conta)->(Enviar%20Email)->(end)>)

Representa o fluxo de uma operação comum como cadastro de usuário.

## Por que usar o yUML?

- Ele permite **incluir diagramas reais em blogs, markdowns e apresentações**.
- Você escreve com texto, mas entrega visual.
- É ideal para **explicar conceitos de forma incremental**, sem precisar exportar imagens toda hora.

## Conclusão

Mais do que uma dica de ferramenta, este post é um convite: se você tem algo a compartilhar, torne isso visível. Diagramas como os que explorei [neste post de introdução à UML](https://blog.heliomedeiros.com/pt/posts/2008-06-10-uml-introducao-minicenarios/) agora podem ser publicados com facilidade com yUML.

Seja um classificador, um editor de reservas, ou só um curioso — escreva, compartilhe e desenhe. O conhecimento cresce quando é diagramado.
