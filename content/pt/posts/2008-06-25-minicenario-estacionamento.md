---
author: helio
categories:
- Events
- Architecture
date: 2008-06-25 02:48:10+00:00
dsq_thread_id:
- 4969844895
layout: post
subtitle: Design de sistema de estacionamento através de cenários UML
tags:
- mini-scenarios
- uml-series
title: 'Minicenário: ESTACIONAMENTO'
---

> **Série: Mini-cenários UML** | **Parte 4 de 4** > _Desenvolvido durante o Mestrado em Projetos de Sistemas Web_

**Chegamos ao cenário final** desta série de mini-cenários UML desenvolvidos sob orientação do Professor Osmar Fernandes Jr. Após explorarmos [classificados web](../2008-06-13-minicenario-classificados-na-web/), [controle de bolão](../2008-06-17-minicenario-controle-de-bolao/) e [controle de obras](../2008-06-21-minicenario-controle-de-obras/), agora modelamos um sistema de estacionamento.

Este último cenário demonstra como a UML pode capturar operações em tempo real, cálculos automáticos e regras de negócio baseadas em tempo e contexto.

## Cenário

Bruno e seu pai compraram um terreno e vão inaugurar um estacionamento. Para ajudar, a irmã de Bruno está desenvolvendo um sistema para controle de entradas, saídas e faturamento.

Quando o veículo entra no estacionamento, o **atendente** observa a **placa**, o **modelo** e a **cor** do carro e cadastra essas informações no sistema.

A **hora de entrada** é gerada automaticamente no momento do cadastro.

Depois de estacionar, o cliente recebe um **ticket impresso** com:

- Número da placa
- Modelo e cor do veículo
- Data e hora de entrada

Na saída, o cliente entrega o ticket e o sistema calcula o **tempo de permanência**. Com base nisso, aplica-se uma **tabela de preços** — que varia entre dias úteis e fins de semana.

O sistema também permite considerar **promoções** específicas conforme a época do ano.

## Diagrama de Casos de Uso

<img src="/uploads/2008/07/estacionamento.png" alt="Diagrama de Casos de Uso Estacionamento" height="425" width="656" />

O **Atendente** é o principal ator e realiza as seguintes ações no sistema:

- **Registrar entrada/saída**: captura os dados do veículo e gera a fatura.
- **Manter veículo**: editar informações já cadastradas.
- **Gerar ticket impresso**: entregue ao cliente na entrada.
- **Manter tabela de preços**: ajustar valores conforme dia da semana.
- **Manter promoções**: aplicar descontos conforme o período.
- **Calcular faturamento**: baseado nas entradas e saídas registradas.
- **Gerar relatório de faturamento**: usado para controle interno.

### Glossário rápido:

- **<<include>>**: indica que um caso de uso sempre executa outro (ex: "Registrar entrada" inclui "Gerar ticket impresso").
- **<<extend>>**: representa uma execução opcional, baseada em condições específicas (ex: aplicar promoção na fatura).

## Conclusão da Série

Este sistema de estacionamento encerra nossa série de mini-cenários UML, demonstrando como diferentes domínios de negócio podem ser modelados com clareza e precisão.

**Ao longo desta série, exploramos**:

1. **[Classificados Web](../2008-06-13-minicenario-classificados-na-web/)**: Sistema com múltiplos atores e notificações automáticas
2. **[Controle de Bolão](../2008-06-17-minicenario-controle-de-bolao/)**: Gestão financeira e controle de participantes
3. **[Controle de Obras](../2008-06-21-minicenario-controle-de-obras/)**: Histórico de preços e relatórios comparativos
4. **Estacionamento**: Operações em tempo real e cálculos automáticos

Cada cenário ilustra aspectos diferentes da modelagem UML, desde casos de uso simples até relacionamentos complexos entre classes e atores. A modelagem com **casos de uso UML** permite mapear claramente as responsabilidades e ações do sistema, independentemente do domínio.

---

### **Navegação da Série**

- **Introdução**: [Por que UML Ainda Importa](../2008-06-10-uml-introducao-minicenarios/)
- **Anterior**: [Parte 3 - Controle de Obras](../2008-06-21-minicenario-controle-de-obras/)
- **Atual**: Parte 4 - Estacionamento (Final)
- **Série completa**: [Classificados Web](../2008-06-13-minicenario-classificados-na-web/) | [Controle de Bolão](../2008-06-17-minicenario-controle-de-bolao/) | [Controle de Obras](../2008-06-21-minicenario-controle-de-obras/)