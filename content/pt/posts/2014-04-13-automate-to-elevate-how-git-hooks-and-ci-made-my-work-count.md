---
title: "Automatizar Para Evoluir: Como Git Hooks e CI Deram Valor ao Meu Trabalho"
date: 2014-04-13T10:00:00-03:00
author: Helio Medeiros
subtitle: Descubra como Git hooks e Jenkins CI transformaram o desenvolvimento Java corporativo caótico em um fluxo automatizado e disciplinado que detecta erros cedo e constrói confiança no time
tags:
  [
    "git",
    "automacao",
    "git-hooks",
    "jenkins",
    "java",
    "maven",
    "jpa",
    "ejb",
    "integracao-continua",
  ]
categories: ["Development"]
---

## Não É Só Sobre Escrever Código

Desde de 2012, na RBS, trabalhávamos 100% com Java. Era JPA, EJB e Maven do começo ao fim. Mas os ciclos de feedback não acompanhavam essa complexidade. A gente implementava uma nova feature, fazia commit, e torcia pra não quebrar outro módulo escondido no sistema.

O Jenkins existia, mas sem disciplina. Uns rodavam teste. Outros não. Cada dev com um ambiente diferente. O CI era quase uma aposta.

O que mudou meu jogo foi colocar Git hooks e levar o Jenkins a sério. Esses dois elementos transformaram cada commit em checkpoint. E cada merge num momento de confiança—não de susto.

## Git Hooks em Projetos Java

Projetos Java, especialmente os maiores, precisam de feedback antecipado. Git hooks viraram minha primeira linha de defesa.

```bash
.git/hooks/pre-commit
```

Usei esse script:

```bash
#!/bin/sh
mvn clean verify
```

Ele rodava todo o ciclo do Maven até os testes de integração. Incluía compilação, testes unitários e análise estática com Checkstyle e PMD.

Também configurei:

- `commit-msg` para garantir padrão `[JIRA-ID] Descrição`
- `pre-push` rodando `mvn verify` novamente como última barreira

| Hook         | Para Que Serve                                |
| ------------ | --------------------------------------------- |
| `pre-commit` | Evitar commit quebrado ou sem teste           |
| `commit-msg` | Garantir padrão de mensagem com JIRA          |
| `pre-push`   | Verificação final antes de enviar pra Jenkins |

Nada disso era complexo—mas evitava problemas reais. Paramos de ver código quebrado indo parar na master.

## Jenkins, Maven e Integração Contínua

O Jenkins já existia, mas mal usado. Fizemos ajustes (obrigado Lincolm e Andre) como:

- Padronizar `pom.xml` com perfis pra builds iguais em todo lugar
- Rodar jobs por branch, não só na `main`
- Integrar SonarQube pra checar qualidade
- Usar cobertura de testes como gate pra merge

Jenkins virou referência. Quebrou o build? Trava merge. Falhou no Sonar? Vira bug.

| Papel do Jenkins      | Valor Entregue                         |
| --------------------- | -------------------------------------- |
| Build automatizado    | Consistência entre devs e ambientes    |
| Checagem de qualidade | Análise estática com Maven e SonarQube |
| Execução de testes    | Confirmação real, não só local         |

Combinado com os Git hooks, isso criou camadas de segurança. Não era sobre controle. Era sobre confiança.

## Scripts Pequenos, Confiança Gigante

Num projeto Java com EJB e JPA, complexidade vem no pacote. A automação foi a forma de domar isso.

Git hooks garantiam que o que eu commitava era válido. Jenkins validava no mundo real. Isso fez meu trabalho ser mais rápido de revisar, e mais confiável de integrar.

Não era sobre ser genial. Era sobre ser consistente. Num time grande, consistência é tudo.

Se você trabalha com Java e ainda não automatizou seus builds Maven—comece. Se ainda não usa Git a seu favor—faça. Seu eu do futuro vai agradecer.

Automatize pra evoluir. Cada passo conta.
