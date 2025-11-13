---
title: "Simulando o Futuro"
categories:
  - Data
  - Engineering
  - Pricing
  - Product
date: 2025-11-13
tags:
  - pricing
  - simulacao
  - experimentacao
  - modelos-de-pricing
  - tomada-de-decisao
  - platform-engineering
description: "Como o meu time de pricing construiu simulação em três iterações — replay, shadow mode e os hábitos que ficaram — e o que cada uma nos ensinou sobre confiar em uma recomendação antes do cliente ver."
subtitle: "Simulação não reduz a incerteza. Move a incerteza para um lugar onde o time consegue discutir antes do cliente ver."
---

Engenheiros de pricing aprendem cedo um tipo específico de paciência — aquela em que os experimentos parecem promissores, os dashboards estão verdes, a recomendação do modelo é plausível, e mesmo assim você não aperta o botão.

A razão de você não apertar é assimetria. Quando uma mudança de preço chega no cliente, custa mais aprender com ela do que custou subi-la. Receita se move. Conversão se move. Relacionamento com parceiros e confiança do cliente se movem nas próprias escalas de tempo. Quando o custo aparece, a mudança já está no ar há semanas. Subir é a parte barata. Se recuperar de uma mudança ruim é a parte cara.

O meu time gastava uma quantidade surpreendente de energia na pergunta que vive no espaço entre *acho que isso é bom* e *estamos dispostos a deixar o cliente ver*. A gente era um time pequeno de pricing — um punhado de engenheiros, um product manager, um analista — ágil por necessidade e build-measure-learn por reflexo. A forma como abordamos essa lacuna foi a mesma com que abordamos tudo o mais. Começar pela coisa mais barata que pudesse nos dizer alguma coisa. Medir o que ela disse. Jogar fora e construir a próxima quando deixasse de pagar o próprio lugar.

Quando a gente queria estimar o impacto de uma candidata antes do cliente ver, tinha uma hierarquia de evidências disponível, com um custo real ligado a cada degrau. Opinião era de graça, e fraca. Replay offline era barato — um script e uma amostra de tráfego passado — e imediatamente informativo. Shadow mode exigia infraestrutura de verdade e produzia números com a cara da produção. Exposição canary ou A/B era a evidência mais forte disponível, e a mais cara, porque o custo de estar errado caía em cima de clientes reais. A gente percorria essa hierarquia em ordem: ficava no degrau mais barato que conseguisse responder a pergunta na nossa frente, e só subia para o próximo quando aquele degrau visivelmente deixava de pagar o lugar.

A capacidade que acabamos construindo — simulação — não chegou de uma vez. Chegou no formato de três experimentos cada vez mais caros, cada um resolvendo um problema que o anterior tinha exposto.

## Iteração 1: rejogar o tráfego de ontem

A primeira versão foi a coisa mais simples que poderia funcionar. Pegamos uma amostra de tráfego histórico de busca — uma semana, depois um mês — e rodamos pela lógica de decisão candidata, offline. Mesmos inputs, novas saídas. Nada disso encostou em um cliente. A gente só comparou as saídas com o que de fato tínhamos cobrado na época.

{{< plantuml title="Iteração 1 — rejogar tráfego histórico pela nova lógica, comparar com o que de fato cobramos" >}}
@startuml
skinparam shadowing false
start
:Tráfego histórico;
:Nova lógica de decisão;
:Resultados previstos;
stop
@enduml
{{< /plantuml >}}

O objetivo não era prever o futuro. Era tornar conversas abstratas concretas. Perguntas que circulavam como opinião agora tinham respostas contra as quais conseguíamos colocar um número:

- Quais clientes seriam afetados?
- Quanto os preços mudariam?
- Quais segmentos se moveriam mais?
- Qual o impacto esperado, no agregado e nas pontas?
- Tinha outliers que ninguém tinha planejado?

Na prática, cada rodada da candidata produzia três visões do mesmo dado — uma distribuição da divergência no conjunto de decisões, um recorte por segmento mostrando quais mercados e produtos se moviam mais, e um relatório de cauda com os maiores outliers. Nenhuma dessas visões precisava de infraestrutura de produção. Um laptop, a amostra histórica e o código da candidata bastavam.

O valor dessa primeira versão acabou sendo majoritariamente social. As nossas revisões de pricing mudaram de forma em um trimestre. Antes do replay, a revisão soava assim: *acho que é seguro, acho que é arriscado, acho que vale tentar*. Depois, soava assim: *aqui está quem seria afetado, aqui está o quanto os preços mudam, aqui estão os três segmentos onde a candidata mais se afasta do comportamento atual*. A gente não parou de discordar. Parou de discordar sobre possibilidades e passou a discordar sobre evidências — que é um tipo de desacordo muito mais útil.

Por um trimestre, isso bastou.

## O problema de acreditar demais no tráfego de ontem

Aí veio o segundo trimestre, e o simulador começou a mentir para a gente.

A primeira vez em que o simulador offline nos enganou, a lição foi pequena. A candidata parecia segura no replay; em produção, a latência subiu nos horários de pico de uma forma que as rodadas offline não tinham mostrado. A gente não tinha simulado carga. Erro honesto.

A segunda vez, a lição foi maior. Rejogamos tráfego de uma semana fraca. A recomendação parecia estável. Subimos. O primeiro fim de semana em que encostou em demanda real, a distribuição de inputs deslocou só o suficiente para empurrar um segmento para fora da parte da curva que o simulador tinha sequer testado. A saída que tínhamos medido era honesta. O dado com que tínhamos alimentado era ralo.

A terceira vez, pegamos o erro com antecedência e ficamos orgulhosos. A candidata divergia fortemente do comportamento atual em um mercado. O simulador gritou. Seguramos o rollout. Uma semana de análise depois, a divergência se revelou ser a candidata fazendo a coisa certa — o comportamento atual estava errado havia meses. O simulador não estava mentindo. Ele estava nos dizendo que a gente não concordava com a própria lógica atual.

O que tiramos desses três episódios foi uma regra única, mais útil do que qualquer descoberta específica. *Uma simulação não é a realidade.* Ela é uma forma estruturada de perguntar *dado tudo o que a gente já sabe, o que teria acontecido?* Essa frase tem a palavra *sabe* duas vezes. Ela não consegue responder perguntas sobre coisas que ainda não observamos — carga, reação do cliente, deslocamento de mercado, a nossa própria lógica estando silenciosamente quebrada. Ela também não consegue dizer em quais respostas dela a gente deveria confiar. Ela só coloca números numa tela.

A gente precisava de algo que rodasse em condições atuais, em tráfego atual, enquanto o cliente continuava vendo o que estava acostumado a ver.

## Iteração 2: shadow mode em tráfego de produção

A segunda versão foi um passo arquitetural. Plugamos a lógica candidata no caminho de requisição ao vivo — em paralelo à lógica existente, de forma assíncrona, fora do caminho crítico — e registramos cada saída sem nunca devolver para o cliente.

{{< plantuml title="Iteração 2 — a candidata roda em paralelo à lógica atual em tráfego real, observada mas nunca devolvida" >}}
@startuml
skinparam shadowing false
skinparam componentStyle rectangle

[Requisição do cliente] as REQ
[Decisão atual] as OLD
[Decisão candidata] as NEW
[Resposta ao cliente] as RESP
[Log de comparação\n(saídas + latência)] as LOG

REQ --> OLD : sync
REQ ..> NEW : shadow / async
OLD --> RESP
OLD --> LOG
NEW --> LOG
@enduml
{{< /plantuml >}}

Nada mudou para o cliente. Tudo mudou para o nosso aprendizado. A candidata agora rodava na distribuição real de inputs, no ambiente real, em concorrência real, contra os padrões reais ao longo do dia. Ela podia estar errada de formas com a cara da produção. A gente podia medir esses erros em números com a cara da produção.

O encanamento não era exótico. Cada requisição carregava um ID que a gente propagava pelos dois caminhos para conseguir parear a saída da candidata com a saída ativa. O par caía em um log de comparação que um job downstream juntava e resumia. Uma feature flag controlava em que porcentagem de quais mercados a candidata rodava, então a gente conseguia começar pequeno, abrir gradualmente e desligar tudo em segundos se algo se comportasse mal. Os dashboards que a gente mais acompanhava eram divergência ao longo do tempo, latência p50/p99 da candidata comparada à ativa, e qualquer diferença na taxa de erro entre as duas.

Shadow mode também é onde aprendemos que duas implementações do *mesmo* intento de negócio podem divergir de formas surpreendentes quando encostam em tráfego de produção. Algumas divergências eram bugs na candidata. Algumas eram comportamentos não documentados da lógica atual que se revelaram intencionais e precisaram ser portados. Algumas eram overrides específicos de mercado vivendo em um arquivo de configuração que ninguém tinha mencionado. E algumas eram, silenciosamente, opiniões diferentes dentro do nosso próprio time sobre qual era o intento, no fundo.

A fase de shadow custou mais do que o replay offline tinha custado. A infraestrutura era real. O planejamento de capacidade era real. Os dashboards de comparação eram reais. A gente teve que se convencer de que valia a pena gastar — não em receita, mas em confiança — e o argumento que continuava ganhando era o mesmo. A gente não podia mais se dar ao luxo de aprender com mudanças só depois que elas tinham chegado no cliente.

## Para que o simulador, no fundo, servia

Quando estávamos um ano dentro de shadow mode, a surpresa lenta tinha chegado. O simulador tinha se tornado mais útil para alinhamento do que para previsão.

A previsão sempre ia ser aproximada. A conversa em torno da previsão era a parte durável. Quando a gente compartilhava uma visão de como a candidata ia se comportar — em números, no tráfego desta semana, na frente de todo mundo — as revisões de pricing paravam de ser debates entre intuições concorrentes e passavam a ser debates sobre qual leitura da evidência se sustentava. A gente discordava menos sobre *se* e mais sobre *para quem*. Esse era o tipo de desacordo que precisávamos ter.

A outra surpresa foi que a gente começou a rodar o simulador para se sentir desconfortável de propósito. As rodadas com as quais mais aprendemos nunca foram as que confirmaram o que a gente já acreditava. Foram as que expuseram algo em que não tínhamos pensado. No segundo ano, a gente se pegou julgando o simulador não pela acurácia, mas pela frequência com que ele nos surpreendia. Um simulador que confirma tudo o que a gente já acredita não está fazendo o trabalho dele. Ele é um eco.

## O que ficou

Três iterações depois, o replay offline tinha sido aposentado. Shadow mode era o sistema em produção. Alguns hábitos ficaram, e acabaram importando mais do que a infraestrutura por baixo deles.

A gente sempre manteve *o que observamos* e *o que esperaríamos* na mesma visualização, lado a lado. Quando os dois convergiam, a gente sabia que a candidata estava agindo como anunciado. Quando divergiam, o nosso reflexo não era "o simulador está errado". Era *o que o cliente está fazendo que as nossas suposições não cobrem?*

A gente apagava cenários do simulador rotineiramente quando eles deixavam de ensinar alguma coisa por dois trimestres. Um cenário que sempre passa é uma sobrecarga lenta de atenção, não uma rede de segurança. Ciclo de vida era inegociável.

E a gente se recusava a deixar o simulador ser previsível. No momento em que uma revisão de pricing começava a concordar com ele toda vez, alguém do time era designado a encontrar um cenário em que ele ia falhar. O simulador era uma conversa que estávamos tendo com as nossas próprias suposições. Uma conversa que ninguém pode perder é uma conversa que parou de ensinar.

## Quando essa receita não teria funcionado

A sequência que a gente rodou — replay offline primeiro, shadow mode quando o replay parou de ensinar, hábitos por cima — não é universal. Ela funcionou para a gente por causa de condições que nem sempre são verdadeiras.

O valor inteiro de shadow mode é *distribuição real em concorrência real*. Um sistema com tráfego esparso teria dificuldade de tirar uma amostra útil do shadow em tempo razoável, e replay offline talvez tivesse continuado bastando sozinho. Uma decisão sem desfecho visível para o cliente perderia a maior vantagem do shadow — o fato de a gente conseguir estar errado em voz alta sem que ninguém fora do time visse. Uma decisão que muda fundamentalmente o estado downstream, como alocação de inventário, tornaria o shadow ainda mais difícil, porque um caminho em shadow não consegue de fato executar a ação que está recomendando; teríamos que simular o efeito colateral, o que joga a gente de volta para território offline.

Por baixo de tudo isso, shadow mode vive ou morre na pipeline de dados que junta as saídas ativa e candidata de forma confiável. Sem essa pipeline funcionando, a gente teria gasto mais em infraestrutura de shadow do que a evidência produzida valia. O caminho certo nesse cenário é continuar no replay offline e investir na engenharia de dados antes de adicionar a segunda camada.

## Reflexão final

Simulação não reduz a incerteza. Ela move a incerteza para um lugar onde o time consegue discutir antes do cliente.

Não é pouco. Também não é certeza. Três iterações e duas arquiteturas depois, o que mantinha o nosso simulador honesto não era nenhuma técnica em particular. Era a nossa disposição de deixar o simulador estar errado em voz alta, na frente dos stakeholders, antes do cliente ter a chance de estar errado no nosso lugar.

Um simulador que ninguém pode ser surpreendido por para de ser útil em um trimestre. O que a gente acabou confiando foi o que continuamos tentando, e falhando, em quebrar.
