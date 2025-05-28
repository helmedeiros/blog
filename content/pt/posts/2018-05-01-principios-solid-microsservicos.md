---
title: "Princípios SOLID no Mundo dos Microsserviços"
date: 2018-05-01T14:00:00-03:00
author: Helio Medeiros
subtitle: "Reinterpretando princípios clássicos de design para sistemas distribuídos"
tags:
  [
    "princípios solid",
    "microsserviços",
    "design de sistemas",
    "arquitetura",
    "engenharia de software",
    "sistemas distribuídos",
  ]
categories: ["Technology", "Architecture"]
---

No início da nossa carreira, aprendemos sobre os princípios SOLID como se fossem exclusivos da programação orientada a objetos. Mas esses princípios vão muito além do código limpo dentro de um único repositório. Eles ajudam a estruturar o pensamento em sistemas — especialmente quando esses sistemas escalam para microsserviços.

Vamos explorar isso com uma analogia prática: um portal digital de notícias.

## O Portal como Microsserviços

Imagine um grande portal digital estruturado com as seguintes áreas principais:

- **Notícias ao Vivo**
- **Previsão do Tempo**
- **Entretenimento**
- **Estilo de Vida**
- **Esportes**

Cada uma dessas áreas contém serviços como notícias urgentes, celebridades, radar meteorológico, dicas de saúde ou perfis de jogadores. À primeira vista, isso parece modular. Mas modularidade não é sinônimo de clareza.

O portal agora é composto por dezenas de serviços distribuídos. O frontend consome APIs variadas. As equipes se organizam por verticais. E mesmo assim... as mudanças ainda se espalham pelo sistema. Incidentes continuam. Releases atrasam. O que está errado?

## Maus Cheiros em Microsserviços

Veja como os cheiros clássicos de design aparecem nesse contexto:

| Mau Cheiro                     | Manifestação em Microsserviços                                                                                                          |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| **Rigidez**                    | Alterar um serviço (ex: `Radar Meteorológico`) obriga mudanças coordenadas em outros (`Alertas`) por causa de contratos compartilhados. |
| **Fragilidade**                | Atualizar `Notícias de Celebridades` quebra `Cobertura de Tapete Vermelho`, pois compartilham schemas de dados.                         |
| **Imobilidade**                | Reutilizar `Bilheteria` em outro app? Difícil, há muitas dependências herdadas.                                                         |
| **Viscosidade**                | É mais fácil criar um novo endpoint em `Esportes` do que refatorar `Placar ao Vivo`.                                                    |
| **Complexidade Desnecessária** | Uso exagerado de serviços, filas e pipelines para algo simples.                                                                         |
| **Repetição Desnecessária**    | `Clima Atual`, `Previsão`, `Alertas` repetem lógica de localização.                                                                     |
| **Opacidade**                  | Quem chama quem? Por que o alerta foi disparado? Logs e dashboards não ajudam.                                                          |

Esses problemas não são exclusivos de classes. São sintomas de um **design ruim de sistema**. E assim como num monólito, a resposta está nos **princípios**.

## SOLID para Microsserviços

Vamos reinterpretar os princípios para sistemas distribuídos:

| Princípio | Em Classes                                     | Em Microsserviços                                          |
| --------- | ---------------------------------------------- | ---------------------------------------------------------- |
| SRP       | Classe com uma única razão de mudar            | Serviço com uma responsabilidade coesa                     |
| OCP       | Aberto para extensão, fechado para modificação | Contrato da API estável; novos comportamentos via versão   |
| LSP       | Subtipos substituem supertipos                 | Versões e contratos devem ser retrocompatíveis             |
| ISP       | Cliente não deve depender do que não usa       | APIs específicas para cada tipo de consumidor              |
| DIP       | Depender de abstrações, não implementações     | Integração por eventos ou interfaces, não chamadas diretas |

## Exemplos Práticos

**Cheiro: Fragilidade entre `Notícias de Celebridades` e `Tapete Vermelho`**

Serviços compartilham modelo de dados. Mudança em um quebra o outro.

**Solução (LSP + ISP)**: Expôr apenas DTOs específicos para cada consumidor. Criar endpoint `/v2/celebrity`.

---

**Cheiro: Imobilidade em `Bilheteria`**

Lógica acoplada ao rendering e à API.

**Solução (SRP + DIP)**: Separar lógica de domínio em camada reutilizável. API apenas consome.

---

**Cheiro: Viscosidade em `Placar ao Vivo`**

Ninguém refatora. Só empilha endpoints.

**Solução (SRP + OCP)**: Modelagem clara. Evitar duplicações. Testar com contratos consumer-driven.

## Conclusão

SOLID não é para os fanáticos por OOP. É uma lente crítica para sistemas. Microsserviços não resolvem design ruim. Princípios resolvem.
