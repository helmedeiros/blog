---
title: "Escrevendo Commits Que Falam: Minha Jornada até Mensagens Significativas"
date: 2014-10-12T10:00:00-03:00
author: Helio Medeiros
subtitle: Transforme seu histórico Git de notas crípticas em comunicação clara—descubra como mensagens de commit bem escritas melhoram colaboração, debugging e compreensão do código
tags: ["git", "comunicacao", "qualidade-de-codigo", "produtividade"]
categories: ["Development"]
---

## Quando "Corrigido" Não Era o Bastante

Nos meus primeiros dias com Git, minhas mensagens de commit eram como bilhetes vagos: curtas, descartáveis e sem contexto. "WIP", "corrigir bug", "atualizar código" — faziam sentido na hora, mas semanas depois, eram inúteis. E o pior: inúteis também para os outros.

Eu não percebia, mas estava sabotando meu próprio histórico. Meus commits não contavam história, nem explicavam intenção. Era uma chance perdida de documentar _por que_ mudei algo. E essa perda voltava para me assombrar em revisões, debugging e no onboarding de novos colegas.

Só fui mudar quando vi um engenheiro sênior escrevendo mensagens como "Clarifica o tratamento de erro quando a requisição falha". Seus commits pareciam um changelog com alma de documento técnico. Primeiro achei interessante. Depois, inspirador. Por fim, comecei a escrever melhor também.

Este post mostra essa virada: como parei de tratar commits como lixo temporário e comecei a vê-los como parte essencial do trabalho em equipe.

## Mensagens São Experiência de Usuário Para Devs

Uma boa mensagem de commit vai além da sintaxe. É um ato de empatia. Alguém vai ler aquilo. Talvez às pressas. Talvez às 3 da manhã. Uma boa mensagem guia. Uma ruim atrapalha.

```bash
# Boa
git commit -m "Corrige problema de overflow no rodapé mobile"

# Ruim
git commit -m "ajustes"
```

A primeira diz o que foi feito e onde. A segunda não diz nada. Qual você preferiria encontrar ao rodar um bisect?

| Estilo da Mensagem      | Clareza Imediata | Contexto | Útil no Histórico |
| ----------------------- | ---------------- | -------- | ----------------- |
| Específica e descritiva | Alta             | Forte    | Sim               |
| Genérica e vaga         | Baixa            | Fraco    | Não               |

Quando passei a ver commits como parte da experiência do desenvolvedor, tudo mudou. Passei a me perguntar: _que problema isso resolve? quem vai ler isso depois?_

Não era sobre escrever muito. Era sobre escrever com clareza.

## Minha Fórmula de Mensagem

Depois de muitos testes, cheguei a um formato que uso até hoje. Funciona em qualquer time ou projeto. Me ajuda a manter consistência, mesmo sob pressão.

**Minha fórmula:**

- **Verbo no imperativo** (ex: "Adiciona", "Corrige", "Remove")
- **O que mudou**, com contexto suficiente
- **Por que importa**, opcional no corpo

```bash
git commit -m "Adiciona timeout na chamada fetchUsuario para evitar travamentos"
```

Para commits maiores, uso várias linhas:

```bash
git commit

Adiciona lógica de retry na API de reservas

A API de reservas às vezes retorna 502, especialmente em horários de pico. Essa mudança adiciona backoff exponencial com retry para melhorar a estabilidade.
```

| Parte             | Propósito                                      |
| ----------------- | ---------------------------------------------- |
| Título (curto)    | Resume a mudança em até 50 caracteres          |
| Corpo (opcional)  | Explica o _porquê_ da mudança                  |
| Rodapé (opcional) | Referência de issue ou nota de breaking change |

Mesmo mensagens simples ganham valor com um pouco de estrutura. Elas mostram intenção. Elas mostram cuidado.

## Código É Uma Conversa

Código não fala por si só. Nunca completamente. O contexto por trás de uma linha—o motivo—fica na sua cabeça. A não ser que você escreva. Commit é o jeito mais leve de registrar esse raciocínio.

Eles não são pra você agora. São pro "você do futuro". Ou pro colega que ainda nem entrou no time. Ou pra pessoa que vai debugar algo crítico muito depois que você sair do projeto.

Boas mensagens de commit são uma das coisas mais simples e impactantes que você pode fazer. Melhoram onboarding, revisão, reversão e confiança.

Comece pequeno. Não busque perfeição. Só tente ser um pouco mais claro do que ontem. Lembre-se: seu histórico também é um produto.
