---
author: helio
categories: ["Architecture"]
date: 2008-06-17 02:14:52+00:00
layout: post
subtitle: "Simplifique a gestão de bolões em grupo com automação inteligente—projete um sistema modelado em UML que gerencia registro de participantes, controle de pagamentos, distribuição de prêmios e elimina o caos da coordenação manual"
tags:
  - mini-scenarios
  - uml-series
title: "Minicenário: CONTROLE DE BOLÃO"
---

> **Série: Mini-cenários UML** | **Parte 2 de 4** > _Desenvolvido durante o Mestrado em Projetos de Sistemas Web_

**Dando continuidade à série**, este é o segundo mini-cenário desenvolvido sob orientação do Professor Osmar Fernandes Jr. Após explorarmos um sistema de classificados web, agora vamos modelar um domínio diferente: o controle de bolões de loteria.

Este cenário demonstra como a UML pode capturar regras de negócio mais complexas, envolvendo controle financeiro, notificações automáticas e gestão de participantes.

## Cenário

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

Este segundo cenário ilustra como sistemas aparentemente simples podem envolver regras de negócio complexas. Comparado ao [sistema de classificados](../2008-06-13-minicenario-classificados-na-web/), aqui temos maior integração entre funcionalidades e controles financeiros mais rigorosos.

A modelagem UML nos ajuda a organizar essas complexidades de forma clara e compreensível.

---

### **Navegação da Série**

- **Introdução**: [Por que UML Ainda Importa](../2008-06-10-uml-introducao-minicenarios/)
- **Anterior**: [Parte 1 - Classificados Web](../2008-06-13-minicenario-classificados-na-web/)
- **Atual**: Parte 2 - Controle de Bolão
- **Próximo**: [Parte 3 - Controle de Obras](../2008-06-21-minicenario-controle-de-obras/)
- **Série completa**: [Classificados Web](../2008-06-13-minicenario-classificados-na-web/) | [Controle de Obras](../2008-06-21-minicenario-controle-de-obras/) | [Estacionamento](../2008-06-25-diagrama-de-casos-de-uso-estacionamento/)
