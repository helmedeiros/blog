---
title: "De 3 Horas para 10 Minutos: Como Automatizamos a Criação de User Stories"
categories:
  - AI
  - Agile
  - Engineering Management
date: 2025-07-28
tags:
  - historias-usuario
  - coaching-agil
  - gpts
  - gestao-produto
  - colaboracao-time
  - genai
  - automacao
description: "Como transformamos a criação de histórias de usuário de horas para minutos usando um GPT customizado—incorporando expertise de coaching ágil em uma ferramenta de IA que escala consistência entre times."
subtitle: "Construindo um GPT customizado que reduziu nosso tempo de escrita de histórias em 90% enquanto melhorou qualidade e consistência entre equipes."
---

## Onde Tudo Começou

Quando nossa equipe se formou, reunimos pessoas talentosas de diferentes empresas, cada uma com seus próprios backgrounds ágeis e formas de abordar user stories. Alguns haviam trabalhado em ambientes com critérios de aceitação detalhados, outros em startups de ritmo acelerado onde conversas aconteciam na pressa, e outros ainda tinham experiência com vários formatos de histórias e estilos de colaboração.

Essa diversidade era uma força, mas também significava que precisávamos nos alinhar em nossa abordagem para colaboração e expectativas compartilhadas sobre valor de negócio e cliente. Tivemos que encontrar nosso ritmo como equipe—estabelecendo como escreveríamos histórias, que nível de detalhe funcionava para nosso contexto, e como garantir que todos tivessem o contexto necessário para trabalhar de forma autônoma enquanto permaneciam conectados ao impacto no cliente que estávamos tentando criar.

## Trazendo Agilidade: Pequeno, Valioso, Testável

Vindo da ThoughtWorks—um dos berços das grandes práticas ágeis—eu sabia que user stories poderiam ser mais do que tarefas de marcação. Elas poderiam ser a espinha dorsal de descoberta de produto, entrega e alinhamento entre tech e negócio.

Ao longo dos anos, orientei minha equipe sobre:

- Escrever histórias pequenas, independentes e testáveis
- Usar hipóteses centradas no cliente
- Incluir critérios de aceitação que focam em como o sucesso seria percebido
- Definir claramente "pronto" e "concluído"

Tentamos múltiplos formatos e atribuímos responsabilidades de escrita de histórias para engenheiros, gerentes de produto ou duplas. Investimos em sessões de treinamento e momentos de coaching ao longo dos trimestres.

Mas um avanço veio recentemente—com IA.

## Do Coaching para Automação

Conforme começamos a explorar mais oportunidades de automação com GenAI, uma nova ideia emergiu: e se escrever uma user story bem estruturada e centrada no cliente pudesse levar menos de um minuto?

E se pudéssemos incorporar o conhecimento de gestão de produto e coaching ágil em uma ferramenta—para que qualquer pessoa da equipe pudesse começar com um excelente rascunho de história que segue nossa Definição de Pronto?

Isso levou ao nascimento do nosso **User Storyteller GPT**.

## O Que São os GPTs da OpenAI?

GPTs são agentes de IA customizáveis construídos sobre o ChatGPT. Eles podem receber:

- Instruções e definições de papel (ex: "Você é um coach Ágil especialista")
- Arquivos de exemplo e APIs
- Acesso a ferramentas como navegador ou interpretador de código

Qualquer pessoa pode criar um GPT visitando [chat.openai.com](https://chat.openai.com), clicando em "Explore GPTs" e selecionando "Create". Não é necessário programação. Você apenas descreve o trabalho da ferramenta, tom e permissões—e a interface te guia a partir daí.

## Construindo Através da Iteração: O Processo de Refinamento

Criar nosso User Storyteller GPT não foi um único prompt—foram múltiplas sessões de ajuste. Como qualquer boa prática ágil, iteramos baseado em feedback e resultados.

O processo começou simples: "Ajude a escrever user stories." Mas essa solicitação genérica produziu saídas genéricas. Através de vários ciclos de refinamento, desenvolvemos instruções abrangentes que incorporam as práticas específicas, formatos e padrões de qualidade da nossa equipe.

![Interface do User Storyteller GPT](/uploads/2025/01/storyteller-step1.png)
_A interface do User Storyteller GPT mostrando prompts iniciais e um exemplo de interação para criar user stories_

Aqui está o prompt central que evoluiu através de nossas sessões de ajuste:

> Este GPT é uma combinação de um gerente de produto e um engenheiro. Deve ser capaz de escrever user stories, documentar débito técnico e identificar e descrever bugs. Deve fornecer informações claras, concisas e acionáveis, considerando tanto perspectivas de negócio quanto técnicas. As respostas devem ser estruturadas, detalhadas e escritas em um tom amigável, técnico e profissional. Sempre escreva como se você fosse parte da equipe resolvendo os problemas. Quando esclarecimentos forem necessários, peça mais detalhes, mas faça suposições educadas quando o nível de confiança for de até 50%.

Então adicionamos formatos markdown específicos para cada tipo de documento—user stories, débito técnico e bugs—completos com nossas listas de verificação de Definição de Pronto. Incorporamos os princípios INVEST (Independente, Negociável, Valioso, Estimável, Pequeno, Testável) e referenciamos o manifesto Ágil para garantir que as saídas se alinhassem com nossa filosofia de desenvolvimento.

O insight chave: **ferramentas de IA se tornam poderosas quando são treinadas nas práticas específicas da sua equipe, não em templates genéricos**. Cada sessão de ajuste fez o GPT melhor em entender nosso contexto, nossos padrões e nossa forma de trabalhar.

Essa abordagem iterativa significou que, quando o implementamos, o GPT já estava produzindo saídas que pareciam vir de um membro experiente da equipe que entendia nossos processos profundamente.

### Os Formatos Detalhados que Incorporamos

Para mostrar o nível de especificidade, aqui estão alguns dos templates markdown que construímos no GPT:

**Para User Stories:**

```
## Background
Conte uma pequena história sobre o problema sendo enfrentado...

## User Story
**Como um** *Papel* executando alguma *Ação*
**Eu gostaria de** *Resultado Desejado*
**Para que eu** obtenha o valor entregue pela história

## Critérios de Aceitação
### Cenário 1: Título
**Dado** ...
**Quando** ...
**Então** ...

## Definição de Pronto
1. A História tem pelo menos um cenário reproduzível?
2. O design está pronto e anexado?
3. O copy está pronto?
4. As traduções estão prontas?
```

**Para Débito Técnico:**

```
## O Débito
> Compartilhe a narrativa, mentalidade e debates feitos durante a sessão de Tech Debt wall

## Como esse pagamento ajudaria?
- Compartilhe qual é a dor sentida e como isso a resolve

## Notas técnicas
- Compartilhe dicas sobre como resolver o problema ou direções a explorar
```

Esses formatos estruturados garantem consistência e completude em toda documentação da equipe, independentemente de quem cria o rascunho inicial.

{{< carousel basepath="/uploads/2025/01" images="storyteller-step2.png,storyteller-step2-1.png,storyteller-step2-2.png,storyteller-step2-3.png" titles="Passo 1: Iniciando uma nova user story com o User Storyteller GPT,Passo 2: GPT gera formato estruturado de história com background e critérios de aceitação,Passo 3: Cenários detalhados de critérios de aceitação com formato Dado-Quando-Então,Passo 4: História completa com checklist de Definição de Pronto incluído" >}}

## Adicionando Context Para Conseguir Ainda Mais Impacto

Embora nosso GPT inicial fosse útil, o verdadeiro avanço veio quando começamos a alimentá-lo com conhecimento específico do domínio sobre nossos sistemas e comportamentos de cliente. Aqui está como evoluímos nosso User Storyteller GPT de um assistente de escrita genérico para um verdadeiro especialista de domínio:

### Nossa Jornada da Biblioteca de Critérios de Aceitação

No início da nossa jornada, criamos o que chamamos de "Biblioteca de Critérios de Aceitação"—uma coleção de passos repetíveis que representam comportamentos comuns de clientes em nossa plataforma de viagem. Em vez de escrever critérios de aceitação do zero a cada vez, identificamos padrões que continuavam aparecendo em nossas funcionalidades da Omio:

- **Padrões de Fluxo de Reserva**: "Dado que um usuário selecionou cidades de partida e chegada, Quando clicam em pesquisar, Então resultados devem aparecer em 3 segundos ordenados por horário de partida"
- **Padrões de Tratamento de Erro**: "Dado informações de pagamento inválidas, Quando usuário submete reserva, Então mensagem de erro clara aparece com destaque específico do campo"
- **Padrões Específicos Mobile**: "Dado usuário em dispositivo mobile, Quando visualizando resultados de pesquisa, Então scroll infinito carrega próximos 20 resultados automaticamente"

### Transformando Padrões em Inteligência GPT

Esta Biblioteca de Critérios de Aceitação se tornou a fundação para a evolução do nosso GPT. A carregamos como uma base de conhecimento, o que transformou como o GPT operava:

- **Sugestões Contextuais**: Em vez de critérios de aceitação genéricos, agora sugere cenários específicos para fluxos de reserva de viagem
- **Linguagem Consistente**: Usa nossa terminologia estabelecida para jornadas de cliente e lógica de negócio
- **Comportamentos Reais de Usuário**: Referencia padrões reais que observamos através de testes A/B e pesquisa de cliente
- **Contexto Específico da Omio**: Entende nossa plataforma de transporte multimodal e diferenças regionais

### O Que Adicionamos Além do Básico

Depois de ver o poder do conhecimento específico de domínio, continuamos alimentando nosso GPT com mais contexto:

**Nossa Arquitetura de Sistema**: Incluímos nosso mapa de microsserviços, documentação de API e requisitos de performance. Agora quando alguém pede uma história sobre funcionalidade de busca, o GPT automaticamente considera nossas limitações de serviço de busca, estratégias de cache e o fato de que agregamos dados de múltiplos provedores de transporte.

**Inteligência de Jornada do Cliente**: Carregamos nossos achados de pesquisa de usuário, dados de funil de conversão e padrões de tickets de suporte. Isso significa que o GPT pode sugerir casos extremos baseados em pontos de dor reais de clientes que documentamos, não cenários teóricos.

**Contexto de Lógica de Negócio**: Nossos algoritmos de precificação, requisitos de conformidade regional e regras de negócio específicas de mercado entraram no GPT. Agora sugere histórias que automaticamente consideram implicações GDPR para mercados europeus ou diferentes métodos de pagamento para várias regiões.

**Padrões de Qualidade**: Nossas listas de verificação de Definição de Concluído, frameworks de teste e registros de decisões arquiteturais se tornaram parte do conhecimento do GPT. Agora sugere critérios de aceitação que se alinham com nossas práticas de engenharia e nos lembra sobre benchmarks de performance ou requisitos de acessibilidade.

### A Evolução: Genérico → Contextual → Preditivo

1. **Genérico**: "Escreva uma user story sobre funcionalidade de busca"
2. **Contextual**: "Escreva uma user story sobre busca multi-cidade que considera nosso fluxo de reserva, inclui critérios de aceitação específicos mobile e aborda requisitos de performance para nossos mercados europeus"
3. **Preditivo**: GPT sugere cenários relacionados que você pode ter perdido baseado em funcionalidades similares no seu sistema

Esta progressão transforma IA de um assistente de escrita em um especialista de domínio que entende seu produto, seus clientes e suas restrições técnicas.

## Experimente Nosso User Storyteller GPT

Projetamos este GPT para combinar pensamento de produto com clareza de engenharia, tornando criar, revisar e refinar user stories, bugs e débito técnico mais eficiente e padronizado. Quer experimentar como isso funciona? Você pode testar nosso [User Storyteller GPT](https://chatgpt.com/g/g-f2TkClaas-user-storyteller) diretamente.

![Interface do User Storyteller GPT](/uploads/2025/01/user-storyteller.png)

A interface fornece prompts iniciais úteis para cenários comuns—desde escrever user stories para novas funcionalidades até documentar débito técnico e descrever bugs. Cada interação aproveita o conhecimento de domínio e padrões de formatação que incorporamos através do nosso processo de ajuste iterativo.

### Nossa Jornada: De Horas para Minutos

Após implementar esta abordagem em nossa equipe Pricing/Premium (Helio Medeiros, Ahmed Naser, Brijesh Prasad, Georgii Maltsev, Pernelle Naidoo, Santhosh Balakrishnan, Talita Roberti), aqui está como nossa criação de user stories evoluiu:

**Junho 2022**: Líderes de milestone da equipe criando histórias → **3-4 horas**, qualidade inconsistente, dependente das habilidades individuais do engenheiro

**Janeiro 2023**: EM facilitando sessões OKRA, criando épicos com user stories → **1-2 horas**, estrutura melhorada

**Junho 2023**: Equipe treinada em melhores práticas de user stories, nova cadência Scrum → **2-3 horas**, conteúdo e formato consistentes

**Junho 2024**: Após novos membros se juntarem → **2-3 horas**, volta a conteúdo inconsistente, nem todos contribuindo proativamente

**Janeiro 2025**: GPT Storyteller introduzido → **10-20 minutos**, conteúdo e formato consistentes, adoção proativa

**O Impacto**: Passamos de gastar 2-3 horas com resultados inconsistentes para 10-20 minutos com saídas consistentes e de alta qualidade—uma **redução de 90% no tempo** enquanto melhoramos dramaticamente qualidade e adoção da equipe.

### Compartilhando O Que Aprendemos

Tem sido encorajador ver o User Storyteller GPT se espalhar organicamente dentro da Omio, com mais de 100 conversas acontecendo em diferentes equipes além do nosso grupo original Pricing/Premium.

![Uso do User Storyteller GPT](/uploads/2025/01/storyteller-being-used.png)
_Adoção interna na Omio mostrando 100+ conversas entre equipes_

Uma das principais razões pelas quais estou compartilhando nossa experiência abertamente é que acredito que outras equipes podem se beneficiar aprendendo como articular melhor o valor do cliente e os caminhos para alcançá-lo. A criação de user stories, em sua essência, é sobre entender o que os clientes realmente precisam e como podemos entregar esse valor de forma eficaz.

O processo de criar boas user stories força as equipes a pensar profundamente sobre problemas dos clientes, não apenas soluções técnicas. Quando usamos ferramentas como nosso GPT para acelerar as partes mecânicas da escrita de histórias, na verdade liberamos mais tempo para as conversas valiosas sobre impacto no cliente, valor de negócio e viabilidade técnica.

Se nossa abordagem ajudar mesmo algumas equipes a ter melhores conversas sobre valor do cliente e decisões de produto mais intencionais, então compartilhar nossos aprendizados terá valido a pena. A ferramenta em si é apenas um meio para um fim—o valor real está na disciplina de pensamento centrado no cliente que as boas user stories encorajam.

### Quando o GPT Precisa de Orientação Humana

Embora nosso User Storyteller GPT tenha melhorado dramaticamente nosso fluxo de trabalho, não é mágica. Todas as user stories ainda requerem validação e revisão. O GPT tem dificuldades particulares com:

**Cenários de Teste A/B**: Ao criar histórias para novos experimentos, o GPT não entende completamente como variações de teste impactam comportamento de cliente e funis de conversão. Por exemplo, critérios de aceitação como:

```
Cenário 3: Rastreamento analítico quando cliente aceita oferta de upgrade premium
Dado que procurei rotas de trem entre Paris e Amsterdam para este fim de semana
E fui atribuído ao experimento premium-upgrade-flow na variante B
E prossigo para a página de Opções de Pagamento com uma tarifa padrão
E vejo a promoção de Upgrade Premium
Quando clico para adicionar o Upgrade Premium à minha reserva
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

1. **Acesse o GPT** – Abra a ferramenta via o link GPT customizado acima
2. **Selecione um Prompt Inicial** – Escolha um template ou descreva sua ideia
3. **Gere e Revise a Saída** – O GPT retorna um rascunho estruturado de história
4. **Use no Seu Fluxo** – Cole no Jira ou Confluence
5. **Itere e Melhore** – Refine baseado em feedback ou necessidades de implementação

Isso não é apenas automação. É ampliação. IA pode ser seu co-piloto ágil.

Se sua equipe está apenas começando a escrever melhores user stories ou tentando escalar consistência entre equipes, considere construir ou pegar emprestado um GPT como este. Pode ser o início do seu próximo grande passo em documentação colaborativa.
