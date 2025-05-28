---
title: "Minicenário: CONTROLE DE BOLÃO"
author: helio
layout: post
date: 2008-07-12T02:14:52+00:00
categories:
  - UML
---

# Minicenário: Controle de Bolão

Dando continuidade à sessão, este é o segundo Minicenário.

Jairo trabalha no Departamento de Informática de uma grande empresa. Ele e seus amigos estão sempre organizando bolões da Mega-Sena, Quina e outros jogos. Até então, Jairo controlava tudo via planilhas Excel: os números apostados, quem participou, e-mails para notificação, e quem já pagou sua cota.

Como isso consumia muito tempo, Jairo decidiu criar um sistema para automatizar esse processo com as seguintes funcionalidades:

- Cadastro de participantes, com e-mail e ramal.
- Cadastro de bolões, com valor da cota, número de cotas, cartões apostados (com os números), tipo de jogo (Mega-Sena, Quina...), número do concurso e data do sorteio.
- Controle de quem pagou cada cota.
- Geração automática de uma página web com os dados do bolão, participantes e suas apostas. A página HTML será enviada por e-mail.
- Permitir que um participante compre mais de uma cota.
- Geração de lista com participantes inadimplentes.
- Verificação se o total arrecadado bate com o valor das apostas.
- Reutilização de uma mesma aposta em diferentes bolões.

Todas essas operações são realizadas pelo Jairo, identificado no sistema como **Gestor do Bolão**.

## Diagrama de Casos de Uso

![Diagrama de Casos de Uso Bolão](/uploads/2008/07/controle-bolao.png)

Este **Diagrama de Casos de Uso UML** mostra as ações possíveis do sistema do ponto de vista do usuário principal, o Gestor do Bolão:

- **Manter participantes por bolão**: permite incluir ou remover pessoas do bolão.
- **Controlar pagamento de cotas**: registra quem já pagou sua parte.
- **Gerar arquivo HTML**: automatiza a página com os dados do bolão.
- **Enviar e-mail**: funcionalidade acoplada ao HTML para envio automático.
- **Consultar tipos de jogos**: lista os jogos disponíveis no sistema.
- **Manter bolão** e **manter apostas** são ações principais de gestão.
- **Adquirir cota**: usada quando um participante quer entrar em um bolão.

### Glossário rápido:

- **Caso de Uso**: representa uma ação ou objetivo do usuário (ex: "Controlar pagamento cotas").
- **<<include>>**: indica que um caso sempre inclui outro (ex: "Enviar e-mail" é incluído após "Gerar arquivo HTML").
- **<<extend>>**: representa uma ação opcional ou condicional (ex: "Manter apostas" estende "Manter bolão").

## Conclusão

A criação de bolões é uma prática comum, mas quando feita manualmente pode se tornar ineficiente. Este sistema proposto automatiza todos os passos críticos — do cadastro ao controle financeiro — e ainda gera e-mails automáticos. Com isso, Jairo ganha tempo e reduz erros, mantendo a diversão dos jogos sem o estresse da gestão.

Nos próximos posts, trarei mais minicenários práticos construídos ao longo do curso.
