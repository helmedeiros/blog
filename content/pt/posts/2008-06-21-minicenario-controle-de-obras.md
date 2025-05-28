---
title: "Minicenário: CONTROLE DE OBRAS"
author: helio
layout: post
date: 2008-06-21T09:24:08+00:00
categories:
  - UML
tags:
  - mini-scenarios
  - uml-series
---

> **Série: Mini-cenários UML** | **Parte 3 de 4** > _Desenvolvido durante o Mestrado em Projetos de Sistemas Web_

# Minicenário: Controle de Obras

**Prosseguindo com nossa série**, este é o terceiro mini-cenário desenvolvido sob orientação do Professor Osmar Fernandes Jr. Após explorarmos [classificados web](../2008-06-13-minicenario-classificados-na-web/) e [controle de bolão](../2008-06-17-minicenario-controle-de-bolao/), agora modelamos um sistema de controle de compras para obras.

Este cenário demonstra como a UML pode capturar histórico de preços, comparações automáticas e relatórios para tomada de decisão.

## Cenário

Álvaro está fazendo uma ampliação de sua residência. Todo dia existe demanda de compra de material. Sendo assim, ele desenvolveu uma pequena aplicação que controla essa demanda de solicitações e as compras efetuadas, de forma a montar uma base de cotação para as compras futuras.

A aplicação possui um cadastro de produtos, contendo: nome, descrição, medida de venda do produto (Kg, ml ou m; indicando peso, volume ou comprimento) e valor da medida de venda (ex.: 1,5).

A cada solicitação de compra cadastram-se os itens dessa solicitação. Cada item possui: o produto e a quantidade. Quando cada item é adquirido, atualiza-se a solicitação com o preço unitário de compra, a forma de pagamento (dinheiro, cheque, cheque pré ou cartão), a data de compra e o local da compra.

## Controles do Sistema

São controles oferecidos pela aplicação:

- Quando há uma nova solicitação, é possível obter de item a lista dos três menores preços que já foram pagos para o referido produto, incluindo na listagem o local onde foi comprado;
- A lista de compras é impressa a partir dos itens que não foram fechados. De todas as solicitações de compra que estejam com status em aberto;
- Uma solicitação pode ser cancelada;
- Quando todos os itens de uma solicitação tiverem sido comprados, o sistema atualiza automaticamente o status dessa solicitação para "fechado";
- Deve ser emitida uma listagem de todos os produtos já comprados, com seu somatório e o valor;

## Diagrama de Casos de Uso

<img src="/uploads/2008/07/controle-de-obras.png" alt="Minicenário: CONTROLE DE OBRAS" height="426" width="642" />

Este **Diagrama de Casos de Uso UML** mostra as principais funcionalidades do sistema do ponto de vista do usuário principal, Álvaro:

- **Manter produtos**: cadastrar e atualizar informações dos materiais
- **Manter solicitações**: criar e gerenciar pedidos de compra
- **Registrar compras**: atualizar solicitações com dados da compra efetiva
- **Consultar histórico de preços**: visualizar os três menores preços já pagos
- **Gerar relatórios**: emitir listas de compras pendentes e produtos adquiridos
- **Cancelar solicitações**: quando necessário

### Glossário rápido:

- **Caso de Uso**: representa uma ação ou objetivo do usuário (ex: "Consultar histórico de preços").
- **<<include>>**: indica que um caso sempre inclui outro (ex: "Registrar compra" inclui "Atualizar status da solicitação").
- **<<extend>>**: representa uma ação opcional ou condicional (ex: "Cancelar solicitação" estende "Manter solicitações").

## Conclusão

Este terceiro cenário ilustra como sistemas de controle podem incorporar inteligência para apoiar decisões. Diferente dos cenários anteriores ([classificados](../2008-06-13-minicenario-classificados-na-web/) e [bolão](../2008-06-17-minicenario-controle-de-bolao/)), aqui o foco está no histórico e na comparação de dados para otimizar compras futuras.

A modelagem UML nos ajuda a organizar essas funcionalidades de forma clara, mostrando como dados históricos podem ser transformados em informação útil.

---

### **📚 Navegação da Série**

- **Introdução**: [Por que UML Ainda Importa](../2008-06-10-uml-introducao-minicenarios/)
- **Anterior**: [Parte 2 - Controle de Bolão](../2008-06-17-minicenario-controle-de-bolao/)
- **Atual**: Parte 3 - Controle de Obras
- **Próximo**: [Parte 4 - Estacionamento](../2008-06-25-diagrama-de-casos-de-uso-estacionamento/)
- **Série completa**: [Classificados Web](../2008-06-13-minicenario-classificados-na-web/) | [Controle de Bolão](../2008-06-17-minicenario-controle-de-bolao/) | [Estacionamento](../2008-06-25-diagrama-de-casos-de-uso-estacionamento/)
