---
title: "Controle de Versão: Não Programe Sem Isso"
date: 2010-06-26 09:00:00-03:00
tags:
  - engenharia de software
  - controle de versão
  - git
  - svn
  - colaboração
  - desenvolvimento
categories:

  - Leadership
series: Aulas de Engenharia de Software
slug: controle-versao-fundacao-essencial
summary:
  "Nesta aula, mergulhamos em um dos pilares do desenvolvimento profissional:
  controle de versão. Mais do que explicar comandos do Git, buscamos mostrar o impacto
  real na manutenção, colaboração e rastreabilidade de projetos. Controle de versão
  não é opcional. É engenharia básica."
subtitle: Nunca mais programe sem controle de versão—descubra como Git, estratégias de branching e disciplina de commit criam redes de segurança, habilitam colaboração e preservam a história das suas decisões
---

**Aulas de Engenharia de Software - Parte 17 de 19**

Nesta aula, mergulhamos em um dos pilares do desenvolvimento profissional: **controle de versão**. Mais do que explicar comandos do Git, buscamos mostrar o impacto real na manutenção, colaboração e rastreabilidade de projetos. Controle de versão não é opcional. É engenharia básica. É o que separa o improviso da prática profissional.

## O Caos Sem Controle

Começamos com uma simulação comum: dois desenvolvedores editando arquivos manualmente e trocando por e-mail. Logo, uma mudança sobrescreve a outra, bugs surgem, e ninguém sabe quem alterou o quê.

Aqui vai um "controle de versão" rudimentar:

```bash
cp index.html index.html.old
cp index.html index-backup.html
rm index.html
mv index-novo.html index.html
```

Isto é insustentável e altamente propenso a falhas.

## Centralizado vs Distribuído

Estudamos dois modelos: o **centralizado** (como SVN) e o **distribuído** (como Git). No modelo centralizado, todos sincronizam com um repositório único. No modelo distribuído, cada desenvolvedor trabalha localmente e sincroniza quando desejar.

### Centralizado (estilo SVN):

```bash
svn checkout http://exemplo.com/projeto
svn commit -m "Adicionada funcionalidade X"
svn update
```

### Distribuído (Git):

```bash
git clone https://github.com/usuario/projeto.git
git commit -am "Adicionada funcionalidade X"
git pull origin main
git push origin main
```

Os alunos perceberam rapidamente a autonomia que o Git oferece: commits offline, branches locais e colaboração entre pares.

## Conceitos Fundamentais

Mapeamos as vantagens reais do Git:

- **Histórico**: Cada alteração é rastreada.
- **Colaboração**: Evita sobrescrita com mesclagens controladas.
- **Rollback**: Permite voltar a versões anteriores.
- **Exploração**: Branches para testar ideias sem afetar a linha principal.

Usamos o comando abaixo para demonstrar hashes únicos:

```bash
echo "teste" | git hash-object --stdin
# retorna: e9650474cb4169f840a1d6c057c44eac80d3e72c
```

Cada hash de 40 dígitos representa uma versão imutável e segura.

## Merge: Sem Pânico

Simulamos um conflito entre branches e resolvemos com:

```bash
git merge funcionalidade-x
# CONFLICT (content): Merge conflict in main.java
```

Resolvemos juntos, finalizamos o commit e limpamos o ambiente. Foi a primeira vez que muitos alunos entenderam que conflito de merge **não é erro**, mas sim **sinal de colaboração ativa**.

## Atividade Prática

Encerramos com um exercício guiado em dupla. Um aluno criou o repositório, o outro fez um fork. Desenvolveram uma pequena funcionalidade e abriram um pull request com revisão mútua.

Facilitadores podem aplicar esse exercício em qualquer turma ou equipe. Use tarefas simples e garanta que a colaboração aconteça via versionamento — e não por mensagens ou e-mails.

Essa aula deixou claro: controle de versão é uma linguagem de comunicação. Entre você, seu time e o seu eu do futuro.

---

_Este post é a **Parte 17 de 19** na série "Aulas de Engenharia de Software"_

**Anterior:** [TDD Avançado: Pensando com Testes](/pt/posts/2010-06-19-tdd-avancado-pensando-com-testes/) (Parte 16)
**Próximo:** [A Sala de Aula Como Aprendizado: Reflexões de Um Semestre](/pt/posts/2010-07-03-sala-aula-aprendizado-reflexoes/) (Parte 18)
