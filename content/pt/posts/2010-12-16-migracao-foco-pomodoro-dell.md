---
title: "Foco Total, Pomodoro e Migração com Confiança"
author: helio
layout: post
date: 2010-12-16T18:00:00+00:00
slug: migracao-foco-pomodoro-dell
categories:
  - Carreira
  - Desenvolvimento
  - Porto Alegre
  - Produtividade
tags:
  - Dell
  - Stefanini
  - Pomodoro
  - Migração
  - TDD
  - Mentoria
  - Eduardo Mathias
  - Carlos Eduardo Maciel
  - OSB
  - BPEL
  - ESB
description: "Como usar a Técnica Pomodoro e commits pequenos para migrar serviços legados com confiança na Dell, com apoio de mentoria técnica."
keywords:
  - tecnica pomodoro
  - migracao servicos legados
  - dell stefanini
  - commits pequenos
  - mentoria tecnica
  - eduardo mathias
  - carlos eduardo maciel
  - tdd java
series: "Vida em Porto Alegre"
---

> **Série: Vida em Porto Alegre** | **Parte 2 de 5** > _Descobrindo uma nova cidade e uma nova carreira_

Existe algo discretamente poderoso em entrar no ritmo certo. Aquele estado em que sua mente para de vagar, as distrações somem, e você está totalmente dedicado a uma coisa: entregar um trabalho excelente. Esse foi o meu dezembro na Dell.

### Pomodoro para Trabalho Profundo

Migrar serviços legados não é glamoroso — é trabalhoso, detalhado e muitas vezes cheio de armadilhas sutis. Em novembro, mergulhei de cabeça em uma dessas migrações. O domínio era novo, a responsabilidade era alta, e as camadas de tecnologia (OSB, BPEL, ESB) transformavam a tarefa em uma maratona mental. Mas a estratégia que mais me ajudou foi **foco com tempo limitado**. Usei a **Técnica Pomodoro** — blocos de 25 minutos de concentração, seguidos por pausas curtas.

O Pomodoro me ajudou a **respeitar a complexidade sem ser dominado por ela**. Ao dividir o trabalho em pedaços focados, enfrentei uma migração enorme de forma incremental, validando cada mudança com calma. Nada de pressa, nada de código pela metade — apenas progresso com propósito.

### Coaching Faz Diferença

Nada disso aconteceu sozinho. Tive um apoio incrível do meu gerente, **Eduardo Mathias**, que manteve nossas prioridades claras e sempre incentivou a clareza em vez da correria. E nosso tech lead, **Carlos Eduardo Maciel**, fez o que grandes tech leads sabem fazer: fez as perguntas certas, orientou decisões de design e demonstrou disciplina ao entregar código bem testado.

Esse tipo de mentoria me fez crescer. Conversas na hora certa tornaram mais fácil tomar decisões — e me deram espaço para evoluir.

### Commits Pequenos, Avanço Seguro

Outra técnica que funcionou muito bem: **commits pequenos e frequentes**. Cada melhoria isolada tornava o code review mais simples, os testes mais seguros e o acompanhamento do progresso mais transparente. Combinado com uma **pirâmide de testes balanceada** — desde testes unitários rápidos até integrações mais esporádicas — eu podia entregar com confiança.

```java
// Exemplo de mudança pequena e segura
if (user.hasPermission("EXPORT")) {
    exporter.export(user.getData());
}
```

Sem drama, sem regressões, sem apagar incêndios. Apenas avanços consistentes.

### Lições que Levo Comigo

Depois de um mês e meio na Dell, posso afirmar: rápido não é sinônimo de descuidado. É sinônimo de método, apoio e intenção. É criar um ambiente onde a qualidade surge naturalmente — com ferramentas, hábitos e pessoas que elevam o padrão todos os dias.

Se você está enfrentando um projeto complexo, recomendo:

- Use **Pomodoro** para blocos de foco
- Faça **commits pequenos** com frequência
- Construa uma **pirâmide de testes** que sustente seu fluxo
- E, se tiver sorte como eu, aprenda com pessoas como Matias e Cadu.

Vamos construir software que dure — e curtir o processo enquanto fazemos isso.

---

**Navegação da Série Vida em Porto Alegre:**

- [Nova Cidade, Novo Código, Novo Idioma](../2010-11-15-primeira-semana-dell-porto-alegre/) (Parte 1)
- **Atual**: Parte 2 - Foco Total, Pomodoro e Migração com Confiança
- **Próximo**: [Final de Semana de Release, Automação e o Valor da Liderança de Verdade](../2011-01-30-final-de-semana-de-release-dell/) (Parte 3)
- [Além do Java: Aprendendo OSB, ESB e BPEL no Segundo Trimestre na Dell](../2011-04-25-aprendizado-osb-esb-bpel-dell/) (Parte 4)
- [Trabalho Remoto, Resiliência e o Poder da Amizade](../2011-10-15-trabalho-remoto-resiliencia-e-amizade/) (Parte 5)

**Esta série documenta minha mudança para Porto Alegre e os primeiros passos na Dell/Stefanini**, explorando os desafios de trabalhar em um ambiente multinacional, aprender novas tecnologias enterprise e adaptar-se a uma nova cidade.
