---
title: "Minicenário: CLASSIFICADOS NA WEB"
author: helio
layout: post
date: 2008-06-13T01:57:56+00:00
categories:
  - UML
tags:
  - mini-scenarios
  - uml-series
---

> **Série: Mini-cenários UML** | **Parte 1 de 4** > _Desenvolvido durante o Mestrado em Projetos de Sistemas Web_

# Mini-cenário: Classificados Web

Como parte do meu Mestrado em Projetos de Sistemas Web, criei quatro mini-cenários sob orientação do Professor Osmar Fernandes Jr. Esta série explora diferentes domínios de negócio através da modelagem UML, demonstrando como casos de uso e diagramas de classes podem capturar requisitos do mundo real.

**Neste primeiro cenário**, apresento um sistema de classificados online imaginado por Dalila para compartilhar com amigos da escola, do bairro e de um clube local.

## Descrição

Dalila oferece um serviço simples: qualquer pessoa pode publicar anúncios classificados online.

O modelo de cobrança é direto:

- **R$2,00** para um **anúncio simples**: até 20 palavras.
- **R$5,00** para um **anúncio de destaque**: até 50 palavras _mais_ uma imagem.

Cada anúncio permanece no ar por 15 dias.

> Observação: Alguns campos **não contam** para o limite de palavras — como valor do produto, título, nome do contato, até dois telefones, e uma observação sobre disponibilidade (ex: "das 18h às 20h").

Assinantes recebem um **resumo diário** por e-mail com os novos anúncios do site. Os usuários também podem definir **áreas de interesse**, para receber avisos sem precisar acessar o site.

## Diagrama de Casos de Uso

![Diagrama de Casos de Uso Classificados Web](/uploads/2008/07/classificado-na-web.png)

Este **Diagrama de Casos de Uso UML** mostra como os atores (usuários ou sistemas) interagem com o sistema:

- **Anunciante**: Pode criar, atualizar e publicar anúncios.
- **Cliente**: Pode consultar anúncios, se inscrever e receber notificações.
- **Servidor de E-mail**: Envia notificações com anúncios por e-mail.

### Glossário rápido:

- **Caso de Uso**: Um objetivo do usuário, representado como uma ação (ex: "Publicar Anúncio").
- **<<include>>**: Indica que essa funcionalidade é sempre necessária como parte de outro caso de uso (ex: "Cadastrar Anúncio" sempre exige "Manter Informações do Produto").
- **<<extend>>**: Indica que essa funcionalidade é opcional ou condicional (ex: "Manter Anúncio Destaque" estende "Manter Anúncio").

## Diagrama de Classes

![Diagrama de Classes Classificados Web](/uploads/2008/07/classificado-na-web-diagrama-de-classe.png)

Este **Diagrama de Classes** representa a estrutura do sistema com classes, atributos, métodos e relacionamentos.

### Elementos-chave:

- **Anúncio**: Representa o anúncio, contendo título, valor, datas, contato e observações.
- **AnúncioDestaque**: Herda de `Anúncio` e adiciona uma imagem.
- **Seção de Interesse**: Agrupa anúncios por categoria (ex: Empregos, Eletrônicos).
- **Cliente & Assinante**: O cliente pode se inscrever e receber resumos por e-mail.
- **Usuário**: Usuário do sistema com login e senha.
- **Associações** como `0..*`, `1`, `0..1`: Mostram quantas instâncias se relacionam (ex: um cliente pode ter várias seções de interesse).

## Conclusão

Este primeiro cenário demonstra como um sistema aparentemente simples pode envolver múltiplos atores e relacionamentos complexos. A modelagem UML nos ajuda a capturar tanto as interações (casos de uso) quanto a estrutura de dados (classes) necessárias.

---

### **📚 Navegação da Série**

- **Introdução**: [Por que UML Ainda Importa](../2008-06-10-uml-introducao-minicenarios/)
- **Atual**: Parte 1 - Classificados Web
- **Próximo**: [Parte 2 - Controle de Bolão](../2008-06-17-minicenario-controle-de-bolao/)
- **Série completa**: [Controle de Bolão](../2008-06-17-minicenario-controle-de-bolao/) | [Controle de Obras](../2008-06-21-minicenario-controle-de-obras/) | [Estacionamento](../2008-06-25-diagrama-de-casos-de-uso-estacionamento/)
