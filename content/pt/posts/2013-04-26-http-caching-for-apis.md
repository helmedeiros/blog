---
title: "Cache HTTP em APIs: Cache-Control, Validators e Requisições Condicionais"
date: 2013-04-26T14:00:00-03:00
author: Helio Medeiros
subtitle: Pare de reinventar cache dentro da aplicação—a spec do HTTP já te deu frescor, validators, requisições condicionais e caches intermediários que tão funcionando desde 1997 e vão sobreviver à tua stack
tags:
  [
    "HTTP",
    "cache",
    "REST",
    "performance",
    "arquitetura",
    "ETag",
    "Cache-Control",
  ]
categories: ["Engineering", "Architecture"]
---

## Por Que Eu Dei Essa Palestra

<iframe class="speakerdeck-iframe" frameborder="0" src="https://speakerdeck.com/player/dd3dfd402ba601312b7a2e0cb471b9bd" title="Cache HTTP em APIs" allowfullscreen="true" allow="web-share" style="border: 0px; background: padding-box padding-box rgba(0, 0, 0, 0.1); margin: 0px; padding: 0px; border-radius: 6px; box-shadow: rgba(0, 0, 0, 0.2) 0px 5px 40px; width: 100%; height: auto; aspect-ratio: 560 / 315;" spellcheck="false" data-ratio="1.7777777777777777"></iframe>

Quando essa palestra foi montada, o recorte era cache numa stack Java específica. Tô reescrevendo aqui porque a parte que de fato importa — e que envelheceu bem — não tem nada a ver com framework. É HTTP.

Se você serve recurso por HTTP, a spec já te deu um sistema de cache. Foi desenhado nos anos 90, foi refinado por trinta anos, e vai continuar funcionando depois que qualquer runtime que você usa hoje morrer. O truque é saber quais cabeçalhos mandar e que conversas eles destravam entre teu servidor, teus clientes, e todos os caches intermediários no meio.

## Cache É uma Conversa

O modelo mental que arruma a maior parte da confusão sobre cache: cache não é feature do teu servidor. Cache é um **acordo negociado** entre servidor, cliente e qualquer cache que tá no meio.

Quando o servidor devolve a resposta, ele fala pro cache: "tá aqui o dado, e tá aqui as regras de como você pode entregar isso pra outra pessoa". Quando o cliente (ou intermediário) quer o recurso de novo, ou confia nas regras, ou volta pra conferir.

Dois mecanismos distintos dirigem essa conversa. Misturar os dois é onde a maior parte dos bugs nasce.

## Frescor: Quanto Tempo o Cache Pode Pular o Servidor

Resposta fresca pode ser servida do cache sem perguntar nada pro servidor. O servidor controla isso com diretivas de **`Cache-Control`** na resposta:

- **`max-age=N`** — a resposta tá fresca por N segundos.
- **`public`** / **`private`** — caches compartilhados (CDN, proxy) podem guardar, ou só o navegador do usuário final?
- **`no-cache`** — guarda, mas sempre revalida com o servidor antes de reusar.
- **`no-store`** — não guarda (dado sensível, resposta de uso único).
- **`must-revalidate`** — quando ficar velho, é obrigado revalidar; não pode servir velho.

```http
Cache-Control: public, max-age=300, must-revalidate
```

Esse cabeçalho sozinho diz: "qualquer um pode cachear isso por cinco minutos; depois disso, volta e pergunta".

Frescor é o caminho rápido. O cache devolve a resposta sem round-trip de rede pra origem. O trade-off é o de qualquer cache: se o dado mudar dentro do `max-age`, os clientes vão ver a versão velha até expirar.

## Validação: Conferir Sem Baixar de Novo

Quando a resposta tá _velha_ — ou quando o cliente só quer ter certeza — caches não precisam baixar o corpo inteiro de novo. Eles podem perguntar pro servidor "tem versão nova?" com uma **requisição condicional**. O servidor responde com o corpo novo (`200 OK`) ou com um `304 Not Modified` minúsculo.

Existem dois validators que o servidor pode mandar na resposta original, e o cliente devolve um deles pra conferir:

**ETag** — identificador opaco que o servidor calcula a partir do recurso (um hash, um número de versão, qualquer coisa que muda quando o recurso muda).

```http
# servidor -> cliente
ETag: "a15505b34a"

# cliente -> servidor (depois)
If-None-Match: "a15505b34a"
```

Se o ETag ainda bate, o servidor responde `304 Not Modified` sem corpo. O cache usa o que já tem.

**Last-Modified** — timestamp de quando o recurso foi modificado pela última vez.

```http
# servidor -> cliente
Last-Modified: Fri, 26 Apr 2013 14:00:00 GMT

# cliente -> servidor (depois)
If-Modified-Since: Fri, 26 Apr 2013 14:00:00 GMT
```

Mesma ideia, garantia mais fraca (resolução de um segundo; não diferencia edição dentro do mesmo segundo).

Usa ETag quando dá pra calcular barato. Usa `Last-Modified` quando você já tem o timestamp e não quer calcular hash. Usa os dois se tem os dois — o cliente escolhe.

## Juntando os Dois

Frescor e validação não são "um ou outro". Eles funcionam como pipeline.

1. Cliente pede o recurso.
2. Servidor devolve o corpo + `Cache-Control: max-age=300` + `ETag`.
3. Pelos próximos 5 minutos, caches servem o corpo guardado direto — sem contato com servidor.
4. Depois dos 5 minutos, a próxima requisição dispara um **GET condicional** com `If-None-Match: <etag>`.
5. Se nada mudou, o servidor devolve `304 Not Modified` (minúsculo). O cache reseta a janela de frescor.
6. Se mudou, o servidor devolve `200 OK` com corpo novo e ETag novo.

A maior parte do tráfego fica no passo 3. O resto é barato.

## O Cabeçalho Que Te Salva: `Vary`

Caches indexam resposta por URL. Dois clientes acessando a mesma URL recebem o mesmo corpo cacheado — exceto se a resposta variar por cabeçalho de requisição. Imagina que tua API serve a mesma URL `/account` em JSON e XML dependendo do `Accept`, ou em português e inglês dependendo do `Accept-Language`. Sem avisar o cache disso, a primeira resposta é guardada e servida pra todo mundo, no formato errado.

```http
Vary: Accept, Accept-Language
```

Isso diz pro cache: "guarda cópias separadas indexadas por esses cabeçalhos de requisição". Pular o `Vary` é um dos bugs de cache mais comuns e sutis em API.

## O Que Não Cachear

Algumas respostas que você deveria marcar explicitamente como não-cacheáveis, mesmo quando cache parece "ok":

- Dado de usuário autenticado, exceto se você tem certeza que `Cache-Control: private` basta e que tua configuração de auth nunca deixa cache compartilhado ver isso.
- Qualquer coisa com side effect de uso único (token, OTP, URL assinada que expira).
- Resposta de erro que você não quer presa (`Cache-Control: no-store` em 500 geralmente tá certo).
- Qualquer coisa onde o custo de dado velho é maior que o custo do round-trip.

Na dúvida: `Cache-Control: no-store`. Uma perda pequena de performance e um ganho real de corretude.

## O Que Isso Te Compra

Três coisas concretas, todas compostas no tempo:

**Banda.** GET condicional manda cabeçalho e não corpo. Pra recurso pesado servido em escala, isso é redução de várias ordens de grandeza.

**Latência.** Frescor deixa o cache responder local. Resposta cacheada no ISP do usuário é duas ordens de grandeza mais rápida que teu servidor de origem.

**Capacidade.** Toda requisição que um cache absorve é uma requisição que tua origem não precisa servir. O jeito mais barato de escalar uma API é precisar menos dela.

## O Que Eu Frisaria Pra Quem Tá Desenhando API Hoje

Três coisas.

Primeira: **decide cache no momento do desenho**, não depois que a performance virar problema. A escolha de `max-age`, a escolha de validator, a decisão de mandar `Vary` — são parte do contrato da API, não passo de otimização.

Segunda: **não reinventa frescor dentro do teu serviço**. Qualquer cache em processo que você tá tentado a montar, o HTTP já te deu um melhor — na borda, no navegador, em todo CDN. Usa primeiro.

Terceira: **seja honesto sobre dado velho**. Todo cache troca frescor por velocidade. Nomeia a troca pra cada endpoint e documenta. `max-age=300` é contrato com todo mundo downstream de você; se comporta como tal.

## Pra Fechar

Essa foi uma palestra que, quando dei, vivia dentro de um runtime específico. O runtime vai continuar mudando. Os cabeçalhos não vão. `Cache-Control`, `ETag`, `Last-Modified`, GET condicional, `Vary` — é a camada de cache que tava esperando na spec o tempo todo. Usa.

---

Me segue: [@helmedeiros](https://twitter.com/helmedeiros)
