---
title: "Ensinando Histórias de Usuário com o Apoio da IA"
categories:
  - AI
  - Agile
  - Engineering Management
date: 2025-01-10
tags:
  - historias-usuario
  - coaching-agil
  - gpts
  - gestao-produto
  - colaboracao-time
  - genai
  - automacao
description: "Como transformamos a criação de histórias de usuário de horas para minutos usando um GPT customizado—incorporando expertise de coaching ágil em uma ferramenta de IA que escala consistência entre times."
subtitle: "Do coaching manual à amplificação com IA—construindo um User Storyteller GPT que incorpora expertise ágil e escala qualidade de histórias entre times de engenharia."
---

## Onde Tudo Começou

Quando nosso time se formou, reunimos pessoas talentosas vindas de diferentes empresas, cada uma com seu próprio background ágil e formas de abordar histórias de usuário. Alguns tinham trabalhado em ambientes com critérios de aceitação detalhados, outros em startups ágeis onde conversas aconteciam de forma mais fluida, e outros ainda tinham experiência com vários formatos de histórias e estilos de colaboração.

Essa diversidade era uma força, mas também significava que precisávamos nos alinhar sobre nossa abordagem de colaboração e expectativas compartilhadas em torno do valor para negócio e clientes. Tínhamos que encontrar nosso ritmo como time—estabelecendo como escreveríamos histórias, que nível de detalhe funcionaria para nosso contexto, e como garantir que todos tivessem o contexto necessário para trabalhar com autonomia enquanto permaneciam conectados ao impacto no cliente que estávamos tentando criar.

## Trazendo Agilidade: Pequenas, Valiosas e Testáveis

Vindo da ThoughtWorks—um dos berços do movimento ágil—sabia que histórias de usuário poderiam ser muito mais do que tarefas soltas. Elas podiam ser a espinha dorsal da descoberta e entrega de produto.

Ao longo dos anos, conduzi o time por uma jornada que envolveu:

- Escrever histórias pequenas, independentes e testáveis
- Usar hipóteses centradas no cliente
- Incluir critérios de aceitação que mostram como o sucesso será percebido
- Criar definições claras de "pronto" e "feito"

Testamos vários formatos e estratégias, atribuindo responsabilidades de escrita para engenheiros, PMs ou duplas. Fizemos treinamentos e sessões de coaching.

Mas um novo capítulo começou com a automação.

## Da Mentoria à Automação

Com a chegada da GenAI em nossas rotinas, surgiu uma ideia: e se escrever uma boa história de usuário levasse menos de um minuto?

E se pudéssemos embutir o conhecimento de produto e agilidade dentro de uma ferramenta acessível a qualquer pessoa da equipe?

Assim nasceu o **User Storyteller GPT**.

## O que são os GPTs da OpenAI?

GPTs são agentes personalizados que você pode criar na plataforma do ChatGPT. Eles permitem:

- Definir instruções e papéis (ex: "Você é um coach ágil")
- Usar arquivos, APIs e ferramentas como navegador e interpretador de código
- Criar automações com lógica contextual

Para criar seu GPT:

1. Acesse [chat.openai.com](https://chat.openai.com)
2. Clique em "Explore GPTs" e depois em "Create"
3. Siga o assistente e descreva a função e o comportamento desejado

Não precisa programar. Basta saber descrever claramente o que deseja que o agente faça.

## Construindo Através da Iteração: O Processo de Refinamento

Criar nosso User Storyteller GPT não foi um prompt único—foram múltiplas sessões de refinamento. Como qualquer boa prática ágil, iteramos baseado em feedback e resultados.

O processo começou simples: "Ajude a escrever histórias de usuário." Mas esse pedido genérico produziu resultados genéricos. Através de vários ciclos de refinamento, desenvolvemos instruções abrangentes que incorporam as práticas específicas da nossa equipe, formatos e padrões de qualidade.

Aqui está o prompt central que evoluiu através de nossas sessões de ajuste:

> Este GPT é uma combinação de product manager e engenheiro. Deve ser capaz de escrever histórias de usuário, documentar dívida técnica e identificar e descrever bugs. Deve fornecer informações claras, concisas e acionáveis, considerando tanto perspectivas de negócio quanto técnicas. As respostas devem ser estruturadas, orientadas a detalhes e escritas em tom amigável, técnico e profissional. Sempre escreva como se fosse parte do time resolvendo os problemas. Quando precisar de esclarecimentos, peça mais detalhes, mas faça suposições educadas quando o nível de confiança for até 50%.

Então adicionamos formatos específicos em markdown para cada tipo de documento—histórias de usuário, dívida técnica e bugs—completos com nossas checklists de Definition of Ready. Incorporamos os princípios INVEST (Independent, Negotiable, Valuable, Estimable, Small, Testable) e referenciamos o manifesto ágil para garantir que os resultados alinhassem com nossa filosofia de desenvolvimento.

O insight fundamental: **ferramentas de IA se tornam poderosas quando são treinadas nas práticas específicas do seu time, não em templates genéricos**. Cada sessão de refinamento fez o GPT melhor em entender nosso contexto, nossos padrões e nossa forma de trabalhar.

Essa abordagem iterativa significou que, quando implantamos, o GPT já estava produzindo resultados que pareciam vir de um membro experiente do time que entendia nossos processos profundamente.

### Os Formatos Detalhados que Incorporamos

Para mostrar o nível de especificidade, aqui estão alguns dos templates em markdown que construímos no GPT:

**Para Histórias de Usuário:**

```
## Background
Conte uma pequena história sobre o problema enfrentado...

## User Story
**As a** *Role* performing some *Action*
**I'd like to** *Desired Outcome*
**So that I** get the value delivered by the story

## Acceptance Criteria
### Scenario 1: Title
**Given** ...
**When** ...
**Then** ...

## Definition of Ready
1. A história tem pelo menos um cenário reproduzível?
2. O design está pronto e anexado?
3. O copy está pronto?
4. As traduções estão prontas?
```

**Para Dívida Técnica:**

```
## The Debt
> Compartilhe a narrativa, mindset e debates feitos durante a sessão de Tech Debt

## How this pay would help?
- Compartilhe qual é a dor sentida e como isso a resolve

## Tech notes
- Compartilhe dicas sobre como resolver o problema ou direções a explorar
```

Esses formatos estruturados garantem consistência e completude em toda documentação do time, independente de quem cria o rascunho inicial.

## Como Tornamos Nosso GPT Ainda Mais Impactante

Embora nosso GPT inicial fosse útil, o verdadeiro avanço veio quando começamos a alimentá-lo com conhecimento específico do domínio sobre nossos sistemas e comportamentos de clientes. Aqui está como evoluímos nosso User Storyteller GPT de um assistente genérico de escrita para um verdadeiro especialista de domínio:

### Nossa Jornada com a Biblioteca de Critérios de Aceitação

No início da nossa jornada, criamos o que chamamos de "Biblioteca de Critérios de Aceitação"—uma coleção de passos repetíveis que representam comportamentos comuns de clientes em nossa plataforma de viagem. Em vez de escrever critérios de aceitação do zero toda vez, identificamos padrões que continuavam aparecendo em nossas features da Omio:

- **Padrões de Fluxo de Reserva**: "Dado que um usuário selecionou cidades de partida e chegada, Quando clica em buscar, Então resultados devem aparecer em até 3 segundos ordenados por horário de partida"
- **Padrões de Tratamento de Erro**: "Dado informações de pagamento inválidas, Quando usuário submete reserva, Então mensagem de erro clara aparece com destaque específico do campo"
- **Padrões Específicos para Mobile**: "Dado que usuário está em dispositivo móvel, Quando visualiza resultados de busca, Então scroll infinito carrega próximos 20 resultados automaticamente"

### Transformando Padrões em Inteligência do GPT

Esta Biblioteca de Critérios de Aceitação se tornou a base para a evolução do nosso GPT. Fizemos upload dela como base de conhecimento, o que transformou como o GPT operava:

- **Sugestões Contextuais**: Em vez de critérios de aceitação genéricos, agora sugere cenários específicos para fluxos de reserva de viagem
- **Linguagem Consistente**: Usa nossa terminologia estabelecida para jornadas de cliente e lógica de negócio
- **Comportamentos Reais de Usuário**: Referencia padrões reais que observamos através de testes A/B e pesquisa de cliente
- **Contexto Específico da Omio**: Entende nossa plataforma de transporte multimodal e diferenças regionais

### O Que Adicionamos Além do Básico

Após ver o poder do conhecimento específico do domínio, continuamos alimentando nosso GPT com mais contexto:

**Nossa Arquitetura de Sistema**: Incluímos nosso mapa de microsserviços, documentação de API e requisitos de performance. Agora quando alguém pede uma história sobre funcionalidade de busca, o GPT automaticamente considera as limitações do nosso serviço de busca, estratégias de cache e o fato de que agregamos dados de múltiplos provedores de transporte.

**Inteligência de Jornada do Cliente**: Fizemos upload dos nossos achados de pesquisa de usuário, dados de funil de conversão e padrões de tickets de suporte. Isso significa que o GPT pode sugerir casos extremos baseados em pontos de dor reais de clientes que documentamos, não cenários teóricos.

**Contexto de Lógica de Negócio**: Nossos algoritmos de precificação, requisitos de compliance regionais e regras de negócio específicas de mercado foram para o GPT. Agora ele sugere histórias que automaticamente consideram implicações de GDPR para mercados europeus ou diferentes métodos de pagamento para várias regiões.

**Padrões de Qualidade**: Nossos checklists de Definition of Done, frameworks de teste e registros de decisões arquiteturais tornaram-se parte do conhecimento do GPT. Agora ele sugere critérios de aceitação que se alinham com nossas práticas de engenharia e nos lembra sobre benchmarks de performance ou requisitos de acessibilidade.

### A Evolução: Genérico → Contextual → Preditivo

1. **Genérico**: "Escreva uma história de usuário sobre funcionalidade de busca"
2. **Contextual**: "Escreva uma história de usuário sobre busca multi-cidade que considera nosso fluxo de reserva, inclui critérios de aceitação específicos para mobile, e aborda requisitos de performance para nossos mercados europeus"
3. **Preditivo**: GPT sugere cenários relacionados que você pode ter perdido baseado em features similares no seu sistema

Esta progressão transforma IA de um assistente de escrita em um especialista de domínio que entende seu produto, seus clientes e suas restrições técnicas.

## Experimente Nosso User Storyteller GPT

Desenvolvemos este GPT para combinar clareza de engenharia com pensamento de produto, tornando a criação, revisão e refinamento de histórias de usuário, bugs e dívida técnica mais eficiente e padronizada. Quer experimentar como isso funciona? Você pode testar nosso [User Storyteller GPT](https://chatgpt.com/g/g-f2TkClaas-user-storyteller) diretamente.

![Interface do User Storyteller GPT](/uploads/2025/01/user-storyteller.png)

A interface fornece prompts iniciais úteis para cenários comuns—desde escrever histórias de usuário para novas features até documentar débito técnico e descrever bugs. Cada interação aproveita o conhecimento de domínio e padrões de formatação que incorporamos através do nosso processo iterativo de ajuste.

### Nossa Jornada: De Horas para Minutos

Após implementar essa abordagem em nosso time Pricing/Premium (Helio Medeiros, Ahmed Naser, Brijesh Prasad, Georgii Maltsev, Pernelle Naidoo, Santhosh Balakrishnan, Talita Roberti), aqui está como a criação de histórias de usuário evoluiu:

**Junho 2022**: Líderes de milestone criando histórias → **2-3 horas cada**, qualidade inconsistente, dependente das habilidades individuais do engenheiro

**Janeiro 2023**: EM facilitando sessões OKRA, criando épicos com histórias de usuário → **1-2 horas cada**, estrutura melhorada

**Junho 2023**: Time treinado em melhores práticas de histórias de usuário, nova cadência Scrum → **2-3 horas cada**, conteúdo e formato consistentes

**Junho 2024**: Após novos membros do time → **2-3 horas cada**, volta para conteúdo inconsistente, nem todos contribuindo proativamente

**Janeiro 2025**: GPT Storyteller introduzido → **10-20 minutos cada**, conteúdo e formato consistentes, adoção proativa

**O Impacto**: Passamos de gastar 2-3 horas por história com resultados inconsistentes para 10-20 minutos com outputs consistentes e de alta qualidade—uma **redução de 90% no tempo** enquanto melhoramos dramaticamente a qualidade e adoção do time.

### Quando o GPT Precisa de Orientação Humana

Embora nosso User Storyteller GPT tenha melhorado dramaticamente nosso fluxo de trabalho, não é mágica. Todas as histórias de usuário ainda requerem validação e revisão. O GPT tem dificuldades particulares com:

**Cenários de Teste A/B**: Ao criar histórias para novos experimentos, o GPT não entende completamente como variações de teste impactam comportamento do cliente e funis de conversão. Por exemplo, critérios de aceitação como:

```
Cenário 3: Rastreamento de analytics quando cliente aceita oferta de upgrade premium
Dado que pesquisei rotas de trem entre Paris e Amsterdam para este fim de semana
E fui atribuído ao experimento premium-upgrade-flow na variante B
E prossigo para a página de Opções de Pagamento com uma tarifa padrão
E vejo a promoção de Premium Upgrade
Quando clico para adicionar o Premium Upgrade à minha reserva
Então um evento de conversão deve ser enviado para nossa plataforma de analytics
```

O GPT frequentemente perde a lógica nuanceada de atribuição de experimento e requisitos de rastreamento de conversão que são cruciais para medição de testes A/B.

**Lógica de Segmentação de Cliente**: Novas regras de segmentação ou customizações regionais precisam de supervisão humana para garantir que critérios de aceitação capturem as implicações nuanceadas do fluxo do cliente. Por exemplo:

```
Cenário 4: Oferta de seguro viagem para residentes de países elegíveis
Dado que estou procurando uma rota de trem de Berlim para Praga através do nosso app móvel
E declarei a Alemanha como meu país de residência no meu perfil
E a Alemanha faz parte da lista de países elegíveis para seguro TravelGuard
Quando chego à página de Complementos durante o checkout
Então a opção de seguro TravelGuard deve ser exibida como disponível para compra
```

O GPT tem dificuldades com a interação complexa entre residência declarada do cliente, regras de elegibilidade regulatória, parcerias de seguradoras e disponibilidade dinâmica de features baseada em frameworks legais.

**A Realidade**: Mesmo com essas limitações, as mudanças e refinamentos que precisamos fazer são tipicamente **4x menores** comparado às nossas histórias pré-GPT. Em vez de reescrever seções inteiras, geralmente estamos apenas ajustando critérios de aceitação específicos ou adicionando casos extremos que o GPT perdeu.

### Como Começar

1. **Acesse o GPT** – Clique no link do GPT customizado acima
2. **Escolha um prompt inicial** – Use um modelo ou descreva sua ideia
3. **Gere e revise a resposta** – O GPT devolve um rascunho estruturado
4. **Inclua no fluxo de trabalho** – Cole no Jira, Confluence ou onde preferir
5. **Itere e melhore** – Ajuste conforme feedback ou implementação

Mais do que automação, isso é aumento de capacidade. A IA pode ser sua co-piloto ágil.

Se seu time está começando a escrever histórias melhores ou quer escalar a consistência entre squads, criar ou usar um GPT assim pode ser o próximo passo.
