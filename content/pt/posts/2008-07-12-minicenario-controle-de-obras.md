---
title: 'Minicenário: CONTROLE DE OBRAS'
author: helio
layout: post
date: 2008-07-12T09:24:08+00:00
url: /2008/07/12/minicenario-controle-de-obras/
categories:
  - UML

---
Neste terceiro minicenário temos que:

Álvaro está fazendo uma ampliação de sua residência. Todo dia existe demanda de compra de materail. Sendo assim, ele desenvolveu uma pequena aplica˜çao que controla essa demanda de solicitações e as compras efetuadas, de forma a montar uma base de cotaçnao para as compras futuras.

Aplicação possui um cadastro de produtos, contendo: nome,descrição, medida de venda do produto(Kg, ml ou m; indicando peso, volume ou comprimento) e valor da medida de venda(ex.: 1,5).

A cada solicitação de compra cadastram-se os itens dessa solicitação. Cada item possui: o produto e a qauntidade. Quando cada item é adquirido, atualiza-se a solicitação com o preço unitário de compra, a forma de pagamento (dinheiro,chque,cheque pr´ou cartão), a data de compra e o local da compra.

São controles oferecidos pela aplicação:

  * Quando há uma nova solicitação, é possível obter de item a lista dos três menores preços que já foram pagos para o referido produto, incluindo na listagem o local onde foi comprado;
  * A lista de  compras é impressa a partir dos itens que não foram fechados. De todas as solicitaçnoes de compra que estejam com status em aberto;
  * Uma solicitação pode ser cancelada;
  * Quando todos os itens de uma solicitação tiverem sido comprados, o sistema atualiza automaticamnete o status dessa solicitação para&#8221;fechado&#8221;;
  * Deve ser emitida uma listagem de todos os produtos já comprados, com seu somatorio e o valor;

DIAGRAMA DE CASOS DE USO

<img src="/uploads/2008/07/controle-de-obras.png" alt="Minicenário: CONTROLE DE OBRAS" height="426" width="642" />