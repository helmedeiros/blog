---
title: "Antes de Construir uma Plataforma de Pricing, Precisávamos Parar de Substituir e Começar a Crescer"
categories:
  - Architecture
  - Engineering
date: 2023-06-14
tags:
  - strangler-fig
  - pricing
  - plataforma
  - modernizacao
  - sistemas-legados
  - arquitetura-de-software
  - motor-de-regras
description: "Por que o primeiro passo em direção a uma nova plataforma de pricing foi entender o presente, não substituí-lo."
subtitle: "Por que o primeiro passo em direção a uma nova plataforma de pricing foi entender o presente, não substituí-lo."
---

O sistema estava funcionando.

Esse era o problema.

Pricing produzia receita todos os dias. Clientes estavam comprando. Markups, fees e add-ons fluíam por serviços que ninguém tocava há anos. E, enterrada dentro desse sistema funcionando, estava a suposição de que qualquer parte dele poderia ser substituída com segurança.

Não podia. Não de uma só vez. Não sem quebrar uma confiança que ainda não tínhamos o direito de gastar.

Entrei em um novo time dentro da empresa onde eu trabalhava. A missão parecia simples no papel: evoluir nossas capacidades de pricing. A realidade era consideravelmente mais complexa. Pricing não era um único sistema. Era uma coleção de decisões espalhadas por serviços, repositórios, integrações, processos operacionais e anos de conhecimento de negócio acumulado. Fees eram calculadas em um lugar. Markups em outro. Add-ons seguiam caminhos diferentes. Algumas decisões de pricing aconteciam perto de aplicações voltadas para o cliente, enquanto outras estavam enterradas em serviços de backend.

O desafio não era construir algo novo.

O desafio era construir algo novo sem quebrar o que já funcionava.

## A tentação do grande rewrite

Sempre que times descobrem complexidade arquitetural, costuma haver um instinto natural de começar do zero.

A lógica parece razoável. Conhecemos os problemas. Conhecemos as limitações. Temos tecnologias mais novas disponíveis. Por que não simplesmente substituir a solução antiga por uma plataforma moderna?

Na prática, essas conversas raramente sobrevivem ao contato com a realidade.

Um sistema de pricing não é apenas software. É conhecimento de negócio codificado. Cada regra representa uma decisão que alguém tomou anos atrás. Cada exceção existe porque um cliente, parceiro, operador, regulador ou mercado a exigiu. Muitas dessas decisões não estão documentadas. Algumas nem são lembradas. O sistema vira um museu vivo da evolução do negócio.

| Suposição | Realidade |
| --- | --- |
| Sabemos exatamente o que o sistema atual faz | Grande parte do comportamento existe apenas no código |
| Reconstruir é principalmente um esforço técnico | Reconstruir é principalmente um esforço de descoberta de negócio |
| Tecnologia nova reduz risco | Rewrites frequentemente introduzem novos riscos |
| O comportamento legado é totalmente compreendido | Dependências ocultas aparecem continuamente |

Essa foi uma das minhas primeiras observações depois de entrar no time. Antes de discutir capacidades futuras, primeiro precisávamos entender o presente. Não apenas o código. O negócio.

## Entender o futuro antes de mudar o presente

Uma das lições mais valiosas que aprendi naquele período é que conversas sobre arquitetura não deveriam começar pela arquitetura. Elas deveriam começar pelos resultados.

Antes de criar uma nova plataforma de pricing, gastamos tempo entendendo onde a empresa queria estar nos próximos anos. Perguntas começaram a aparecer em todo lugar:

- Quais capacidades de pricing precisaríamos em três anos?
- Quão rápido novos experimentos de pricing deveriam ser lançados?
- Quem deveria ser dono das decisões de pricing?
- Quão configuráveis as regras deveriam se tornar?
- O que deveria exigir envolvimento de engenharia?
- O que deveria virar self-service?
- Como suportaríamos novos produtos e modelos de monetização?

Só depois de discutir essas perguntas é que conseguíamos avaliar os sistemas que já existiam. Isso não era sobre tecnologia. Era sobre criar uma imagem compartilhada do destino.

O verdadeiro desafio não era substituir software. Era criar entendimento suficiente do futuro para reconhecer quais partes do presente deveriam sobreviver.

## Descobrindo capacidades de pricing escondidas pela organização

Conforme mapeávamos o cenário existente, descobrimos lógica de pricing espalhada por vários lugares. Algumas capacidades eram óbvias. Outras estavam escondidas. Um markup simples podia envolver vários serviços. Uma fee podia depender de dados gerados em outro lugar. Um add-on podia ter um processo operacional próprio, completamente separado do resto do fluxo de pricing.

O trabalho começou a parecer arqueologia. Cada repositório revelava mais uma camada de decisões de negócio. Cada serviço expunha suposições que ninguém tinha documentado. Cada conversa descobria mais uma dependência.

Uma visão simplificada era mais ou menos assim:

{{< plantuml title="Lógica de pricing espalhada pelos sistemas existentes" >}}
@startuml
skinparam shadowing false
skinparam componentStyle rectangle

[Requisição do Cliente] as REQ
package "Sistemas Existentes" {
  [Markups] as M
  [Fees] as F
  [Add-ons] as A
}
[Preço Final] as FP

REQ --> M
REQ --> F
REQ --> A
M --> FP
F --> FP
A --> FP
@enduml
{{< /plantuml >}}

O objetivo não era centralizar tudo imediatamente. O objetivo primeiro era entender o que realmente existia.

## Por que o padrão Strangler Fig fazia sentido

Por volta daquele período, uma abordagem arquitetural aparecia consistentemente nas discussões: o padrão Strangler Fig.

A ideia vem da natureza. A figueira estranguladora cresce ao redor de uma árvore existente. Ela não substitui a árvore da noite para o dia. Em vez disso, gradualmente a envolve, absorve suas responsabilidades e, eventualmente, se torna a estrutura principal. Martin Fowler depois popularizou essa metáfora na modernização de software.

O padrão é enganosamente simples:

1. Deixar o sistema existente rodando.
2. Construir novas capacidades ao redor dele.
3. Redirecionar comportamento gradualmente.
4. Aposentar componentes antigos um de cada vez.

O que tornava a ideia atrativa não era elegância. Era redução de risco.

| Grande Rewrite | Strangler Fig |
| --- | --- |
| Evento grande de entrega | Entrega contínua |
| Tempo longo até gerar valor | Valor incremental cedo |
| Alta incerteza | Aprendizado contínuo |
| Rollback difícil | Caminhos de rollback mais fáceis |
| Exige entendimento completo antecipado | Permite que o entendimento emerja |

Isso não é sobre evitar mudança. É sobre tornar a mudança sustentável.

## Anatomia de uma migração Strangler Fig

O padrão é fácil de desenhar em um quadro branco e difícil de aplicar em produção. No nosso caso, a forma mais útil de entendê-lo foi percorrer uma única capacidade e rastrear o que de fato precisava acontecer, passo a passo.

Uma fee, por exemplo.

No sistema original, fees eram calculadas dentro do serviço de busca. O mesmo monólito que retornava os resultados de viagem também decidia quanto cobrar por eles. A lógica tinha sido adicionada incrementalmente ao longo dos anos, às vezes para um mercado, às vezes para um parceiro, às vezes para uma campanha cuja documentação ninguém mais conseguia encontrar. Ela era pequena o suficiente para ninguém ter reservado tempo para extraí-la. E crítica o suficiente para ninguém querer ser a pessoa que a quebrasse.

Esse é o ponto de partida típico do Strangler Fig. Não é sobre sistemas obviamente apodrecidos. É sobre sistemas que estão silenciosamente no centro.

A migração se desdobrou em estágios, e cada estágio existia para responder a uma pergunta diferente.

**Estágio 1. Introduzir uma emenda.**

A primeira mudança não tinha nada a ver com o novo serviço. Ela foi feita dentro do próprio monólito de busca. Extraímos o cálculo de fee inline para trás de uma interface interna — uma única chamada de função pela qual o resto do código de busca passava a ter que ir. Nada de comportamento mudou. Nada de ownership mudou. Não estávamos resolvendo o problema ainda. Estávamos criando um lugar onde o problema poderia ser resolvido depois.

Uma emenda é a menor unidade de opcionalidade. Sem ela, nenhuma migração é possível. Com ela, cada passo seguinte vira uma escolha.

**Estágio 2. Subir o novo serviço.**

Então construímos um serviço de fee separado. Mesmos inputs. Mesmas saídas esperadas. Nenhuma funcionalidade nova. Nenhuma melhoria. Nada de "já que estamos aqui". Esse é o passo que engenheiros mais querem pular, porque parece duplicação. É duplicação. Esse é o ponto.

O novo serviço não tinha permissão de ser mais inteligente que o antigo ainda. Seu único trabalho era produzir o mesmo número.

**Estágio 3. Rodar em shadow.**

Aqui é onde o padrão começa a dar retorno. Cada requisição de busca continuava passando pela emenda, continuava chamando a lógica de fee inline antiga e continuava retornando aquele resultado para o cliente. Mas, em paralelo — de forma assíncrona, fora do caminho crítico — a emenda também chamava o novo serviço de fee com os mesmos inputs e registrava tanto as saídas quanto os tempos.

O cliente não via nada diferente. O time de dados via tudo.

{{< plantuml title="Execução em shadow: o cliente vê o caminho antigo, o novo é observado" >}}
@startuml
skinparam shadowing false
skinparam componentStyle rectangle

[Requisição de Busca] as REQ
[Emenda no Monólito de Busca] as SEAM
[Lógica de Fee Inline\n(monólito)] as OLD
[Novo Serviço de Fee\n(shadow)] as NEW
[Log de Comparação\n(saídas + latência)] as CMP
[Resposta ao Cliente] as RESP

REQ --> SEAM
SEAM --> OLD : sync
SEAM ..> NEW : async / shadow
OLD --> RESP
OLD --> CMP
NEW --> CMP
@enduml
{{< /plantuml >}}

O que a fase de shadow nos deixou responder era simples e brutal:

- Para o mesmo input, o novo serviço retorna a mesma fee que o código antigo? Sempre? Em quais mercados? Para quais produtos? Em quais bordas?
- E ele faz isso rápido o bastante para que os clientes não percebam a mudança de latência de cauda quando fizermos o cutover?

A primeira pergunta protege a receita. A segunda protege a experiência. Não tínhamos permissão para abrir tráfego enquanto as duas não estivessem verdes.

Na prática, as primeiras semanas de execução em shadow são humilhantes. A "mesma lógica" que você escreveu no novo serviço diverge do monólito de formas pequenas e constrangedoras. Uma etapa de arredondamento acontece meio milissegundo antes. Uma conversão de moeda usa um cache de taxa ligeiramente diferente. Um override específico de mercado que vivia em um arquivo de configuração que ninguém mencionou está silenciosamente ausente. Cada divergência é um pedaço de conhecimento de negócio que ninguém se lembrou de escrever.

Isso não é um problema para ser escondido. Esse é o motivo inteiro do shadow existir.

**Estágio 4. Ajustar até a paridade.**

Cada divergência era triada. Algumas eram bugs reais no novo serviço. Algumas eram comportamentos não documentados do antigo que se revelaram intencionais e precisaram ser portados. Algumas eram comportamentos não documentados que se revelaram acidentes esquecidos, e o negócio decidiu não os carregar para frente.

A performance recebia o mesmo tratamento. O tráfego em shadow expunha onde o novo serviço era mais lento do que o caminho inline — o cold start de um processo separado, um hop de rede desnecessário, uma escolha de serialização que importava no p99 mas não no p50. Nada disso é visível em um load test contra um caminho feliz. Só é visível quando tráfego de produção, no formato de produção, passa pelas duas implementações ao mesmo tempo.

Não passávamos adiante enquanto o relatório de comparação não mostrasse duas coisas no mesmo dashboard: paridade de saídas dentro de uma tolerância aceita, e latência dentro de um budget aceito.

| Fase | Tráfego no novo serviço | O que observávamos | Critério de saída |
| --- | --- | --- | --- |
| Shadow | 0% (espelhado async) | Paridade de saídas, p50/p99 vs antigo | Taxa de paridade acima da meta em todos os mercados |
| Canary | 1% | Conversão, receita por sessão, taxa de erro | Sem regressão estatisticamente significativa |
| Rampa | 10% → 25% → 50% | Mesmas métricas, em amostra maior | Estável por dois ciclos de negócio |
| Cutover | 100% | Mesmas métricas, mais remoção de código morto | Caminho de fee antigo deletado do monólito |

**Estágio 5. Subir a rampa atrás de uma flag.**

Só depois da paridade e da performance se manterem é que começamos a rotear tráfego real para o novo serviço, e ainda assim, atrás de uma feature flag que poderíamos desligar em segundos. Pequena porcentagem primeiro. Esperar. Olhar as métricas de negócio, não só as técnicas. Aumentar. Esperar. Aumentar.

A flag não é só uma rede de segurança. É um contrato com o resto da empresa. Ela diz: se algo parecer errado, conseguimos colocar o comportamento de ontem de volta, em produção, enquanto descobrimos por quê.

**Estágio 6. Remover o caminho antigo.**

Esse é o passo que fecha o ciclo. Quando o novo serviço de fee já servia 100% do tráfego por tempo suficiente para cobrir sazonalidade e ciclos de parceiros, deletamos a lógica de fee inline do monólito de busca. A emenda ficou. O código legado, não.

Se você pula esse passo, você não fez uma migração Strangler Fig. Você construiu um segundo sistema e manteve o primeiro. Isso não é modernização — é imposto.

A emenda, o shadow, o log de comparação, a feature flag, a rampa, a deleção. Cada um está fazendo um trabalho diferente. Cada um ganha seu lugar reduzindo uma categoria específica de risco.

## Manter a experiência idêntica enquanto mudamos tudo por baixo

Uma das restrições mais importantes que tínhamos era preservar a experiência do cliente. Os clientes não se importavam com nossa arquitetura. Eles se importavam em ver os preços certos. Eles se importavam em comprar com sucesso. Eles se importavam com confiança.

Isso significava que nosso primeiro objetivo não era inovação. Era compatibilidade.

Por um período de tempo, a nova plataforma precisava produzir as mesmas saídas que os sistemas existentes. Só depois de ganhar confiança poderíamos começar a introduzir novas capacidades.

Na prática, a jornada se parecia mais com isto:

{{< plantuml title="Crescendo uma nova camada de pricing ao redor do sistema existente" >}}
@startuml
skinparam shadowing false
skinparam componentStyle rectangle

[Sistema Atual de Pricing] as CPS
[Comportamento Existente] as EB
[Nova Camada de Pricing] as NPL
[Capacidades Futuras] as FC

CPS --> EB
EB --> NPL
NPL --> FC
@enduml
{{< /plantuml >}}

A nova camada inicialmente parecia redundante. Alguns engenheiros naturalmente questionavam seu valor. Por que construir algo que se comporta exatamente igual?

Porque comportamento idêntico hoje cria liberdade amanhã.

## Arquitetura transitória não é desperdício

Uma lição que ficou comigo daquele período é que engenheiros frequentemente subestimam o valor da arquitetura temporária.

Gostamos de soluções permanentes. Gostamos de sistemas limpos. Gostamos de construir coisas que duram.

Mas modernização raramente acontece assim. Às vezes o componente mais valioso é aquele desenhado para desaparecer.

Camadas de roteamento. Adaptadores de compatibilidade. Serviços de migração. Caminhos de execução em shadow. Dashboards de comparação. Feature flags cujo único trabalho é serem desligadas um dia. Esses componentes podem eventualmente ser deletados, mas eles tornam o progresso possível.

Arquitetura transitória não é desperdício. É andaime. E andaime é frequentemente o que nos permite construir algo maior com segurança.

O verdadeiro custo da modernização raramente é o código temporário. O verdadeiro custo vem de tentar evitar o código temporário e forçar uma migração arriscada no lugar.

## O que aprendi

Olhando para trás, entrar no time de pricing me ensinou algo que continua a influenciar como eu abordo mudanças em larga escala.

Frequentemente imaginamos transformação como substituição. Antigo vira novo. Legado vira moderno. Monolito vira plataforma.

A realidade normalmente é menos dramática. As transformações mais bem-sucedidas que eu vi se parecem mais com jardinagem do que com demolição. Você cria espaço. Você entende o ecossistema. Você identifica o que deve crescer. Você remove restrições com cuidado. E, com o tempo, algo novo emerge ao redor da estrutura existente.

O padrão Strangler Fig não é realmente sobre arquitetura de software. É sobre respeitar a complexidade. É sobre reconhecer que negócios não podem parar enquanto engenheiros redesenham sistemas. E é sobre reconhecer que o caminho mais seguro para o futuro é, frequentemente, um pequeno passo deliberado de cada vez.

Se você está olhando para um sistema que funciona mas que você já não consegue evoluir, a pergunta que vale a pena fazer não é *"como substituímos isso?"*. É *"onde podemos colocar a primeira emenda, e o que precisaríamos ver antes de confiar no novo caminho com um por cento do tráfego?"*.

Responda isso, e a migração se escreve sozinha.
