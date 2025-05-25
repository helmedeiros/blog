---
title: Diagrama de Casos de Uso ESTACIONAMENTO
author: helio
layout: post
date: 2008-07-12T02:48:10+00:00
url: /2008/07/12/diagrama-de-casos-de-uso-estacionamento/
dsq_thread_id:
  - 4969844895
categories:
  - UML

---
O últmo cenário dentre os itens propostos seguem a seguinte regra de negócio.

Bruno e seu pai compraram um terreno e inaugurarão um estacionamento.

Para ajudar, a irmã de Bruno está desenvolvendo uma aplicação de controle de estacionamento.

Quando o veículo entra no estacionamento, o atendente observa sua placa e a mesma é cadatrada juntamente com o modelo  do veículo e sua cor.
  
A hora de entrada é gerada automaticamente, correspondendo ao momneto do cadastramento da placa.Após estacionar o veículo, o cliente pega o ticket onde está impresso: o número da placa, o modelo do veículo, a cor, a data e a hora da entrada.

Ao retornar ao estacionamento, o cliente entrega o ticket. O tempo de permanência é calculado. Considerando esse tempo de permanência, é aplicada a tabela de preços, sabendo-se que a tabela de sábado não é a mesma dos dias úteis e às vezes, dependendo da época do ano, os donos lançam promoções durante os dias úteis

**DIAGRAMA DE CASOS DE USO**
  
<img src="/uploads/2008/07/estacionamento.png" alt="Diagrama de Casos de Uso Estacionamento" height="425" width="656" />