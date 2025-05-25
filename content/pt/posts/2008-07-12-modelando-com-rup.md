---
title: Mascarando a aproximação BDUF com template RUP ?
author: helio
layout: post
date: 2008-07-12T09:24:51+00:00
categories:
  - RUP
tags:
  - Atividade
  - BDUF
  - Disciplina
  - RUP
  - template
---
Tivemos um debate nos últimos dias em nossa classe de Pós-Graduação sobre, <a href="http://en.wikipedia.org/wiki/Big_Design_Up_Front" title="Big Design Up Front" target="_blank">BDUF</a>, e se seria possível reduzir a bagagem de documentos não compiláveis, através da composição de novos templates junto ao RUP, endeusado por alguns profissionais da escola do escopo fechado. O Rational Unified Process(RUP) é um processo de engenharia de software,  que oferece uma abordagem baseada em disciplinas para atribuir tarefas e responsabilidades dentro de uma organização de desenvolvimento; guiado pelos princípios <a href="http://www.ibm.com/developerworks/rational/library/oct05/kroll/index.html" title="ABCDE" target="_blank">ABCDE</a> do <a href="http://www.devx.com/ibm/Article/30308" title="Business Driven Development" target="_blank">BDD</a> que garante um processo adaptável, com gerência de níveis de prioridade e colaboração entre membros do time. Sendo assim, tentamos elaborar este template que coube bem às nossas necessidades diárias.

**Disciplina**: Ambiente

**Atividade**: Preparar ambiente do projeto

**Tarefa**: Elaborar o caso de desenvolvimento

**Artefato**: Plano de desenvolvimento de Software

**Artefatos Inclusos**:

  * [Artefato: Guia de Modelagem de Caso de Uso][1]
  * [Artefato: Guia de Interface do Usuário][2]
  * <u>[<u>Artefato: Plano de Gerenciamento de Riscos</u>][3]</u>
  * [Artefato: Guia de Teste][4]
  * <u>[<u>Artefato: Plano de Garantia de Qualidade</u>][5]</u>

**Disciplina**: Modelagem de Negócio

**Atividade**:

  * [Explorar automação de processos][6]

**Artefato**:

  * [Visão do negócio][7]

**Disciplina**: Requisitos

**Atividade**:

  * [Definir o sistema][8]

**Tarefa**:

  * [Desenvolver Visão][9]

**Artefato**:

  * [Visão][10]

**Disciplina**: Gerenciamento de Projeto

**Atividade**:

  * Identificar e analisar riscos
  * Planejar fases e iterações
  * Selecionar equipe
  * Compilar plano de desenvolvimento de software
  * Revisão da Aprovação do projeto
  * Programar e atribuir trabalho

**Artefato**:

  * [Plano de Desenvolvimento de Software][11]

**Disciplina**: Análise e Design

**Atividade**:

  * [Realizar Síntese Arquitetural][12]

**Tarefa:**

  * <a href="http://www.wthreex.com/rup/process/activity/ac_arcan.htm" target="_blank">Análise arquitetural</a>

**Artefato**:

  * [Arquitetura de Referência][13]
  * [Documento de Arquitetura de Software][14]

 [1]: http://www.wthreex.com/rup/process/artifact/ar_ucmgl.htm
 [2]: http://www.wthreex.com/rup/process/artifact/ar_uigls.htm
 [3]: http://www.wthreex.com/rup/process/artifact/ar_riskpl.htm
 [4]: http://www.wthreex.com/rup/process/artifact/ar_tstgl.htm
 [5]: http://www.wthreex.com/rup/process/artifact/ar_qapl.htm
 [6]: http://www.wthreex.com/rup/process/workflow/busmodel/wfs_prep.htm
 [7]: http://www.wthreex.com/rup/process/artifact/ar_bvsio.htm
 [8]: http://www.wthreex.com/rup/process/workflow/requirem/wfs_defs.htm
 [9]: http://www.wthreex.com/rup/process/activity/ac_dvisn.htm
 [10]: http://www.wthreex.com/rup/process/artifact/ar_vsion.htm
 [11]: http://www.wthreex.com/rup/process/artifact/ar_sdp.htm
 [12]: http://www.wthreex.com/rup/process/workflow/ana_desi/wfs_archsyn.htm
 [13]: http://www.wthreex.com/rup/process/artifact/ar_refarch.htm
 [14]: http://www.wthreex.com/rup/process/artifact/ar_sadoc.htm