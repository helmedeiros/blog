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
description: "Por que o primeiro passo pra uma nova plataforma de pricing foi entender o presente, não substituir."
subtitle: "Por que o primeiro passo pra uma nova plataforma de pricing foi entender o presente, não substituir."
---

O sistema estava funcionando.

Esse era o problema.

Pricing gerava receita todo dia. Cliente comprava. Markup, fee e add-on rodavam por serviços que ninguém tocava havia anos. E enterrada dentro desse sistema que funcionava tinha uma suposição: que qualquer pedaço dele dava pra substituir sem dor.

Não dava. Não de uma vez. Não sem quebrar uma confiança que a gente ainda nem tinha conquistado.

Entrei num time novo na empresa em que eu trabalhava. No papel, a missão parecia simples — evoluir as capacidades de pricing. Na prática, bem mais cabeluda. Pricing não era um sistema. Era um amontoado de decisões espalhadas por serviços, repositórios, integrações, processos operacionais e anos de conhecimento de negócio que ninguém tinha escrito direito em lugar nenhum. Fee calculava num canto. Markup em outro. Add-on seguia o próprio caminho. Algumas decisões aconteciam perto das aplicações que o cliente via; outras estavam enterradas lá no fundo do backend.

O desafio não era construir coisa nova.

Era construir coisa nova sem quebrar o que já tava de pé.

## A tentação do grande rewrite

Sempre que um time esbarra em complexidade de arquitetura, vem aquele instinto natural de começar do zero.

A lógica parece fazer sentido. A gente conhece os problemas. Conhece as limitações. Tem tecnologia mais nova à disposição. Por que não trocar a solução antiga por uma plataforma moderna?

Na prática, essas conversas raramente sobrevivem ao contato com a realidade.

Um sistema de pricing não é só software. É conhecimento de negócio em forma de código. Cada regra representa uma decisão que alguém tomou anos atrás. Cada exceção existe porque um cliente, parceiro, operador, regulador ou mercado pediu. Boa parte dessas decisões não tá documentada. De algumas, ninguém mais lembra. O sistema vira um museu vivo da evolução do negócio.

| Suposição | Realidade |
| --- | --- |
| Sabemos exatamente o que o sistema atual faz | Boa parte do comportamento existe só no código |
| Reconstruir é, no fundo, esforço técnico | Reconstruir é, no fundo, esforço de descoberta de negócio |
| Tecnologia nova reduz risco | Rewrite costuma introduzir risco novo |
| O comportamento legado tá bem entendido | Dependência escondida aparece sem parar |

Essa foi uma das primeiras coisas que percebi quando entrei no time. Antes de discutir capacidade futura, a gente precisava entender o presente. Não só o código. O negócio.

## Entender o futuro antes de mudar o presente

Uma das maiores lições daquele período foi que conversa sobre arquitetura não deveria começar pela arquitetura. Tinha que começar pelo resultado.

Antes de criar uma nova plataforma de pricing, a gente gastou tempo entendendo onde a empresa queria estar dali a alguns anos. Pergunta apareceu por todo canto:

- Quais capacidades de pricing a gente ia precisar dali a três anos?
- Quanto tempo a gente devia levar pra lançar um experimento novo?
- Quem ia ser dono das decisões de pricing?
- Até onde as regras precisavam ser configuráveis?
- O que ia precisar de mão de engenharia?
- O que devia virar self-service?
- Como a gente ia dar suporte a produto e modelo de monetização novos?

Só depois de discutir essas perguntas é que dava pra avaliar os sistemas que já existiam. A questão nem era tecnologia. Era criar uma imagem compartilhada do destino.

O desafio real não era substituir software. Era criar entendimento suficiente do futuro pra reconhecer quais pedaços do presente deviam sobreviver.

## Descobrindo capacidades de pricing escondidas pela organização

À medida que a gente ia mapeando o cenário, encontrou lógica de pricing espalhada por todo canto. Algumas capacidades eram óbvias. Outras estavam escondidas. Um markup simples podia envolver vários serviços. Uma fee podia depender de dado gerado em outro lugar. Um add-on podia ter um processo operacional próprio, totalmente separado do resto do fluxo.

O trabalho começou a parecer arqueologia. Cada repositório revelava mais uma camada de decisão de negócio. Cada serviço expunha suposição que ninguém tinha documentado. Cada conversa descobria mais uma dependência.

Uma visão simplificada ficava mais ou menos assim:

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

O objetivo não era centralizar tudo logo de cara. Era primeiro entender o que de fato existia.

## Por que o padrão Strangler Fig fazia sentido

Nessa época, uma abordagem de arquitetura aparecia direto nas conversas: o padrão Strangler Fig.

A ideia vem da natureza. A figueira estranguladora cresce em volta de uma árvore. Não substitui a árvore da noite pro dia. Vai envolvendo aos poucos, absorvendo as responsabilidades dela e, com o tempo, acaba virando a estrutura principal. Martin Fowler depois popularizou essa metáfora pra modernização de software.

O padrão parece simples (e não é):

1. Deixar o sistema existente rodando.
2. Construir capacidade nova ao redor dele.
3. Redirecionar comportamento aos poucos.
4. Tirar do ar componente antigo, um de cada vez.

O que tornava a ideia atraente não era elegância. Era redução de risco.

| Grande rewrite | Strangler Fig |
| --- | --- |
| Evento grande de entrega | Entrega contínua |
| Tempo longo até gerar valor | Valor incremental cedo |
| Alta incerteza | Aprendizado contínuo |
| Rollback difícil | Caminhos de rollback mais fáceis |
| Exige entendimento completo antecipado | Permite que o entendimento apareça aos poucos |

A questão não é evitar mudança. É tornar mudança sustentável.

## Anatomia de uma migração Strangler Fig

O padrão é fácil de desenhar num quadro branco e difícil de aplicar em produção. No nosso caso, a forma mais útil de entender foi pegar uma capacidade só e rastrear o que de fato precisava acontecer, passo a passo.

Uma fee, por exemplo.

No sistema original, a fee era calculada dentro do serviço de busca. O mesmo monólito que devolvia os resultados de viagem também decidia quanto cobrar por eles. A lógica tinha sido adicionada aos poucos ao longo dos anos — às vezes pra um mercado, às vezes pra um parceiro, às vezes pra uma campanha cuja documentação ninguém mais achava. Era pequena o bastante pra ninguém ter separado tempo pra tirar de lá. E crítica o bastante pra ninguém querer ser a pessoa que ia quebrar.

Esse é o ponto de partida típico do Strangler Fig. Não são os sistemas obviamente apodrecidos. São os sistemas que estão silenciosamente no centro.

A migração foi acontecendo em estágios, e cada estágio existia pra responder uma pergunta diferente.

**Estágio 1. Introduzir uma emenda.**

A primeira mudança não tinha nada a ver com o serviço novo. Foi feita dentro do próprio monólito de busca. A gente extraiu o cálculo da fee inline e colocou atrás de uma interface interna — uma única chamada de função pela qual o resto do código de busca passou a ter que ir. Nenhum comportamento mudou. Nenhum ownership mudou. A gente ainda não estava resolvendo o problema. Estava criando um lugar onde o problema podia ser resolvido depois.

Uma emenda é a menor unidade de opcionalidade. Sem ela, migração nenhuma é possível. Com ela, cada passo seguinte vira uma escolha.

**Estágio 2. Subir o serviço novo.**

Aí a gente construiu um serviço de fee separado. Mesmos inputs. Mesmas saídas esperadas. Nenhuma funcionalidade nova. Nenhuma melhoria. Nada de "já que estamos aqui". É o passo que mais dá vontade de pular, porque parece duplicação. É duplicação. Essa é a sacada.

O serviço novo ainda não tinha permissão pra ser mais inteligente que o antigo. O único trabalho dele era produzir o mesmo número.

**Estágio 3. Rodar em shadow.**

É aqui que o padrão começa a se pagar. Cada requisição de busca continuava passando pela emenda, continuava chamando a lógica de fee inline antiga e continuava devolvendo aquele resultado pro cliente. Só que, em paralelo — de forma assíncrona, fora do caminho crítico — a emenda também chamava o serviço novo de fee com os mesmos inputs e registrava tanto a saída quanto o tempo.

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

O que a fase de shadow respondeu era simples e brutal:

- Pro mesmo input, o serviço novo retorna a mesma fee que o código antigo? Sempre? Em quais mercados? Pra quais produtos? Em quais bordas?
- E faz isso rápido o bastante pra que o cliente não perceba a mudança de latência de cauda quando a gente fizer o cutover?

A primeira pergunta protege a receita. A segunda protege a experiência. A gente não abria tráfego enquanto as duas não estivessem verdes.

Na prática, as primeiras semanas de execução em shadow são humilhantes. A "mesma lógica" que a gente escreveu no serviço novo diverge do monólito de formas pequenas e constrangedoras. Uma etapa de arredondamento acontece meio milissegundo antes. Uma conversão de moeda usa um cache de taxa um pouquinho diferente. Um override específico de mercado que vivia num arquivo de configuração que ninguém mencionou simplesmente sumiu. Cada divergência é um pedaço de conhecimento de negócio que ninguém se lembrou de escrever.

Não é um problema pra esconder. É justamente pra isso que o shadow existe.

**Estágio 4. Ajustar até a paridade.**

Cada divergência era triada. Algumas eram bug real no serviço novo. Algumas eram comportamento não documentado do antigo que se revelava intencional e precisava ser portado. Algumas eram comportamento não documentado que, na verdade, era acidente esquecido, e o negócio decidia deixar pra trás.

Pra performance valia a mesma coisa. O tráfego em shadow expunha onde o serviço novo era mais lento que o caminho inline — o cold start de um processo separado, um hop de rede desnecessário, uma escolha de serialização que importava no p99 mas não no p50. Nada disso aparece em load test contra um caminho feliz. Só aparece quando tráfego de produção, no formato de produção, passa pelas duas implementações ao mesmo tempo.

A gente não passava adiante enquanto o relatório de comparação não mostrasse duas coisas no mesmo dashboard: paridade de saídas dentro de uma tolerância aceita, e latência dentro de um budget aceito.

| Fase | Tráfego no serviço novo | O que a gente observava | Critério de saída |
| --- | --- | --- | --- |
| Shadow | 0% (espelhado async) | Paridade de saídas, p50/p99 vs antigo | Taxa de paridade acima da meta em todos os mercados |
| Canary | 1% | Conversão, receita por sessão, taxa de erro | Sem regressão estatisticamente significativa |
| Rampa | 10% → 25% → 50% | Mesmas métricas, em amostra maior | Estável por dois ciclos de negócio |
| Cutover | 100% | Mesmas métricas, mais remoção de código morto | Caminho de fee antigo deletado do monólito |

**Estágio 5. Subir a rampa atrás de uma flag.**

Só depois da paridade e da performance se manterem é que a gente começou a rotear tráfego de verdade pro serviço novo, e mesmo assim, atrás de uma feature flag que dava pra desligar em segundos. Um pouquinho primeiro. Esperar. Olhar as métricas de negócio, não só as técnicas. Subir. Esperar. Subir.

A flag não é só uma rede de segurança. É um contrato com o resto da empresa. Ela diz: se algo parecer errado, a gente consegue botar o comportamento de ontem de volta, em produção, enquanto descobre por quê.

**Estágio 6. Remover o caminho antigo.**

Esse é o passo que fecha o ciclo. Quando o serviço novo de fee já servia 100% do tráfego por tempo suficiente pra cobrir sazonalidade e ciclos de parceiros, a gente deletou a lógica de fee inline do monólito de busca. A emenda ficou. O código legado, não.

Se pular esse passo, não fez migração Strangler Fig. Construiu um segundo sistema e manteve o primeiro. Isso não é modernização — é imposto.

A emenda, o shadow, o log de comparação, a feature flag, a rampa, a deleção. Cada um fazendo um trabalho diferente. Cada um se justificando ao reduzir uma categoria específica de risco.

## Manter a experiência idêntica enquanto a gente muda tudo por baixo

Uma das coisas que a gente mais tinha que cuidar era a experiência do cliente. O cliente não tava nem aí pra nossa arquitetura. Se importava em ver os preços certos. Em comprar sem dor de cabeça. Em confiar.

Ou seja, nosso primeiro objetivo não era inovação. Era compatibilidade.

Por um tempo, a plataforma nova precisava produzir as mesmas saídas que os sistemas existentes. Só depois de ganhar confiança é que a gente podia começar a introduzir capacidade nova.

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

A camada nova parecia redundante no começo. Alguns engenheiros questionaram o valor dela — e com razão. Por que construir uma coisa que se comporta exatamente igual?

Porque comportamento idêntico hoje cria liberdade amanhã.

## Arquitetura transitória não é desperdício

Uma lição que ficou comigo daquele período é que engenheiro costuma subestimar o valor da arquitetura temporária.

A gente gosta de solução permanente. Gosta de sistema limpo. Gosta de construir coisa que dura.

Mas modernização raramente é assim. Às vezes o componente mais valioso é justamente aquele feito pra desaparecer.

Camada de roteamento. Adaptador de compatibilidade. Serviço de migração. Caminho de execução em shadow. Dashboard de comparação. Feature flag cujo único trabalho é ser desligada um dia. Esses componentes podem ser deletados no futuro, mas é por causa deles que o progresso acontece.

Arquitetura transitória não é desperdício. É andaime. E é o andaime que muitas vezes deixa a gente construir algo maior com segurança.

O custo de verdade da modernização raramente é o código temporário. O custo de verdade vem de tentar evitar o código temporário e forçar uma migração arriscada no lugar.

## O que aprendi

Olhando pra trás, entrar no time de pricing me ensinou uma coisa que ainda hoje influencia como eu encaro mudança em larga escala.

A gente costuma imaginar transformação como substituição. Antigo vira novo. Legado vira moderno. Monolito vira plataforma.

A realidade costuma ser menos dramática. As transformações que vi dar mais certo lembravam mais jardinagem do que demolição. A gente cria espaço. Entende o ecossistema. Identifica o que precisa crescer. Tira restrição com cuidado. E, com o tempo, algo novo nasce em volta da estrutura existente.

No fundo, o padrão Strangler Fig não tem a ver com arquitetura de software. Tem a ver com respeitar a complexidade. Tem a ver com reconhecer que negócio não para enquanto engenheiro redesenha sistema. E tem a ver com reconhecer que o caminho mais seguro pro futuro é, na maioria das vezes, um passinho deliberado de cada vez.

A maior parte do Strangler Fig é trabalho sem glamour. Não se derruba nada. A gente coloca uma emenda onde não tinha, roteia uma cópia do tráfego por ela e depois passa alguns meses pra ganhar o direito de apagar um `if`. A emoção acaba na segunda semana.

O que sobra, depois que a emoção passa, é um sistema que o time consegue mudar sem prender a respiração. É esse o prêmio. O padrão é só o meio.
