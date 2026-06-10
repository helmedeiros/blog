---
title: "Logs Estruturados: Pare de Escrever Frases, Comece a Escrever Dados"
date: 2017-06-15T14:00:00-03:00
author: Helio Medeiros
subtitle: Trate teus logs como a superfície consultável do sistema que eles de fato são—eventos com campos, identificadores de correlação atravessando serviços, e a diferença entre uma linha de log que dá pra ler e uma que dá pra responder pergunta com
tags:
  [
    "observabilidade",
    "logs estruturados",
    "correlation id",
    "sistemas distribuídos",
    "produção",
  ]
categories: ["Engineering"]
---

## Por Que Eu Dei Essa Palestra

<iframe class="speakerdeck-iframe" frameborder="0" src="https://speakerdeck.com/player/a15505b34ade437c9b20a104c8860a3b" title="Logs Estruturados" allowfullscreen="true" allow="web-share" style="border: 0px; background: padding-box padding-box rgba(0, 0, 0, 0.1); margin: 0px; padding: 0px; border-radius: 6px; box-shadow: rgba(0, 0, 0, 0.2) 0px 5px 40px; width: 100%; height: auto; aspect-ratio: 560 / 420;" spellcheck="false" data-ratio="1.3333333333333333"></iframe>

Quase todo incidente de produção que eu já entrei começou do mesmo jeito: alguém compartilhou uma linha de log, outra pessoa escreveu um regex pra extrair um campo, e dez minutos depois a gente tava discutindo se os timestamps de dois serviços diferentes tavam pelo menos no mesmo timezone.

Essa palestra é sobre por que a gente não deveria estar escrevendo log que precisa de regex.

## Uma Linha de Log É um Evento

A virada mental é pequena, mas muda tudo. Linha de log não é frase descrevendo o que aconteceu — é **evento** com forma. No segundo em que você trata como evento, duas coisas seguem:

- Tem **campos**, não palavras. `user_id`, `request_id`, `latency_ms`, `outcome`.
- É **consultável**, não pesquisável. Você filtra por valor de campo, não torcendo pra palavra "erro" aparecer.

Log não-estruturado é frase. Log estruturado é dado.

```text
# não-estruturado
2017-06-15 14:02:11 usuário 8131 acessou /checkout e recebeu 500 em 842ms

# estruturado
{"ts":"2017-06-15T14:02:11Z","app":"checkout","user_id":8131,
 "path":"/checkout","status":500,"latency_ms":842,
 "trace_id":"7f2c…","event":"request.completed"}
```

O segundo não é "mais verboso". Ele é _legível por máquina_, o que quer dizer legível em escala.

## Campos Que Valem a Pena Ter em Toda Linha

A forma mínima útil de evento, na minha experiência:

- **`ts`** — timestamp em UTC, ISO 8601. Sempre UTC. Timezone em log é imposto que você paga em todo incidente.
- **`app`** / **`service`** — qual serviço emitiu.
- **`event`** — nome estável, de baixa cardinalidade (ex.: `request.completed`, `payment.captured`). Não é frase.
- **`level`** — info / warn / error.
- **`trace_id`** / **`correlation_id`** — o identificador que segue uma ação do usuário através dos serviços (mais sobre isso abaixo).
- **`outcome`** / **`status`** — a coisa deu certo ou não.

Tudo mais é contexto. Adiciona à vontade, mas mantém esses seis honestos.

## Correlation ID: O Campo Que Muda Como Você Debuga

Quando um clique do usuário toca cinco serviços, cinco serviços geram log. A única forma de costurar de volta é dar pra esse clique um identificador na borda e propagar ele em toda chamada interna.

Chama de `trace_id`, `correlation_id`, `request_id` — escolhe um e fica consistente. Gera no primeiro hop (load balancer, gateway, frontend). Passa adiante em todo header HTTP, toda mensagem de fila, toda chamada downstream. Loga como campo em toda linha.

A primeira vez que você dá grep num ID só e vê a jornada inteira do usuário se desenrolar entre serviços em ordem cronológica, você para de querer log não-estruturado.

## Logs vs Métricas vs Traces

Log estruturado não substitui métrica nem trace distribuído — é um corte diferente da mesma verdade.

- **Métricas** respondem "o sistema tá saudável agora?" Agregados ao longo do tempo. Baratas de armazenar, difíceis de fatiar depois.
- **Traces** respondem "onde essa requisição gastou tempo?" Uma árvore causal entre serviços.
- **Logs** respondem "o que exatamente aconteceu nesse evento?" Alta fidelidade, alta cardinalidade, caros em volume.

Log estruturado é o orçamento de cardinalidade que você gasta quando precisa de fato saber _qual_ usuário, _qual_ payload, _qual_ branch do código. Não tenta fazer log virar métrica; mas pode (e deve) emitir com os mesmos identificadores do trace, pra pivotar entre eles.

## O Que Dá Errado Quando Você Não Faz Isso

Três padrões que vejo sempre.

**Log como console.log.** Pessoa imprime frase durante o desenvolvimento, e a frase vai pra prod. Debug em produção vira arqueologia.

**Dado sensível vazando.** Quando a linha é livre, ninguém sabe o que tá nela. Email, token, corpo de payload — vão se esgueirando porque não tem schema dizendo "esse campo, não aquele".

**Explosão de cardinalidade.** Mensagens livres com substring única (timestamp na própria mensagem, ID concatenado em string) detonam índice e conta. Campo com nome estável e valor dinâmico é barato; frase com valor embutido é caro.

## O Que Mudar Amanhã de Manhã

Se você levar uma coisa dessa palestra:

1. Escolha um formato estruturado. JSON se a stack permite, key-value se não.
2. Decida os seis campos acima. Documenta. Defende.
3. Gera um correlation ID na borda e propaga.
4. Para de imprimir frase. Emite evento.

Não precisa de fornecedor novo. Não precisa de reescrita. Precisa de hábito.

## Pra Fechar

Os times que eu vi levando log estruturado a sério não ganharam dashboard mais bonito. Ganharam incidente mais rápido. A coisa que você mais mede é o tempo entre "tem algo errado" e "eu sei o quê".

Esse tempo é mais gasto _lendo_ log. Faz eles legíveis.

---

Me segue: [@helmedeiros](https://twitter.com/helmedeiros)
