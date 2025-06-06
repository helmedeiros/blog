---
title: "TDD Avançado: Pensando com Testes"
date: 2010-06-19T09:00:00-03:00
tags:
  [
    "engenharia de software",
    "tdd",
    "testes",
    "java",
    "junit",
    "desenvolvimento",
  ]
categories: ["Engenharia de Software"]
series: ["Aulas de Engenharia de Software"]
slug: "tdd-avancado-pensando-com-testes"
summary: "Nesta aula, aprofundamos o uso de Test-Driven Development (TDD), mostrando que ele é mais do que uma técnica — é uma forma de pensar. Utilizando um sistema real de template de e-mails, desenvolvemos tudo partindo de testes. Cada linha foi uma decisão validada, cada falha evitada antes de acontecer."
---

**Aulas de Engenharia de Software - Parte 16 de 16**

![Placeholder para imagem atual](caminho/para/imagem-placeholder.jpeg)

Nesta aula, aprofundamos o uso de Test-Driven Development (TDD), mostrando que ele é mais do que uma técnica — é uma forma de pensar. Utilizando um sistema real de template de e-mails, desenvolvemos tudo partindo de testes. Cada linha foi uma decisão validada, cada falha evitada antes de acontecer.

---

## Dos Requisitos aos Testes

O desafio era simples: criar um sistema que envia e-mails usando templates com variáveis como `${primeiroNome}` e `${sobreNome}`. Em vez de começar a codar, montamos uma **lista de testes necessários**.

Convertendo tarefas vagas em validações claras:

```java
@Test
public void substituiUmaVariavel() {
    Template template = new Template("Olá, ${nome}");
    template.set("nome", "Leitor");
    assertEquals("Olá, Leitor", template.formar());
}
```

Esse teste é mais do que unitário — ele define o comportamento do sistema.

---

## Começar no Vermelho

O teste falha porque a classe Template não existe. Então criamos apenas o necessário para compilar:

```java
public class Template {
    public Template(String texto) {}
    public void set(String var, String valor) {}
    public String formar() {
        return null;
    }
}
```

Depois, fazemos ele passar com valor fixo:

```java
public String formar() {
    return "Olá, Leitor";
}
```

Mas já adicionamos outro teste para evitar trapaças.

---

## Triangulação e Primeira Refatoração

Escrevemos um novo teste:

```java
@Test
public void substituiComOutroValor() {
    Template template = new Template("Olá, ${nome}");
    template.set("nome", "Convidado");
    assertEquals("Olá, Convidado", template.formar());
}
```

E refatoramos:

```java
public class Template {
    private String texto;
    private Map<String, String> valores = new HashMap<>();

    public Template(String texto) {
        this.texto = texto;
    }

    public void set(String var, String valor) {
        valores.put(var, valor);
    }

    public String formar() {
        String resultado = texto;
        for (var entrada : valores.entrySet()) {
            String regex = "\$\{" + entrada.getKey() + "\}";
            resultado = resultado.replaceAll(regex, entrada.getValue());
        }
        return resultado;
    }
}
```

A cada novo teste, o código fica mais genérico.

---

## Programação por Intenção

Falamos sobre **programar por intenção**: escrever código como se ele já existisse. Pensar primeiro no uso, depois na implementação. Isso força foco no "_o quê_" e não no "_como_".

Esse estilo favorece clareza e coesão.

---

## Antecipando e Tratando Falhas

E se uma variável não for atribuída?

```java
@Test(expected=ValorNaoRecebidoException.class)
public void erroSeVariavelNaoAtribuida() {
    new Template("Olá, ${nome}").formar();
}
```

Corrigimos com:

```java
if (resultado.matches(".*\$\{.+\}.*")) {
    throw new ValorNaoRecebidoException();
}
```

Testes também servem para proteger. Negligenciar erros é negar robustez.

---

## Refatoração Final e Aprendizados

Reduzimos duplicações usando `@Before` e métodos auxiliares. Os testes ficaram mais claros, reutilizáveis e expressivos.

TDD não é sobre ferramenta. É sobre mentalidade. É um guia para projetar com clareza e entregar com confiança.

Facilitadores podem usar esse modelo em treinamentos, mentorias ou programas de integração. Basta escolher uma classe simples, definir os comportamentos e testá-los com clareza.

---

## Conclusão da Série

E assim concluímos nossa jornada abrangente pelos fundamentos da engenharia de software. Ao longo destas 16 aulas, cobrimos todo o espectro desde princípios básicos até práticas avançadas:

**Parte 1 - [Por que Engenharia de Software?](/pt/posts/2010-02-24-software-engineering-purpose/)** - Compreendendo a disciplina e sua importância

**Parte 2 - [Domando a Complexidade com Processo](/pt/posts/2010-03-02-complexity-process/)** - Gerenciando complexidade através de abordagens estruturadas

**Parte 3 - [O Modelo Cascata](/pt/posts/2010-03-10-waterfall-model/)** - Metodologia tradicional de desenvolvimento sequencial

**Parte 4 - [Modelos de Desenvolvimento Evolutivo](/pt/posts/2010-03-18-evolutionary-models/)** - Abordagens iterativas e incrementais

**Parte 5 - [A Mentalidade Ágil](/pt/posts/2010-03-26-agile-mindset/)** - Princípios e valores do desenvolvimento ágil

**Parte 6 - [Scrum e Produtividade](/pt/posts/2010-04-03-scrum-productivity/)** - Framework para gerenciamento ágil de projetos

**Parte 7 - [O Ciclo de Desenvolvimento Scrum](/pt/posts/2010-04-11-scrum-cycle/)** - Visão detalhada de sprints e cerimônias

**Parte 8 - [Programação Extrema: Qualidade e Coragem](/pt/posts/2010-04-19-xp-quality-courage/)** - Valores e mentalidade XP

**Parte 9 - [Princípios e Práticas XP](/pt/posts/2010-05-01-xp-principles-practices/)** - Práticas e técnicas centrais do XP

**Parte 10 - [Aplicando XP: Estratégias na Prática](/pt/posts/2010-05-08-applying-xp-strategies/)** - Implementação do XP no mundo real

**Parte 11 - [Domain-Driven Design](/pt/posts/2010-05-15-domain-driven-design/)** - Modelagem de domínios de negócio complexos

**Parte 12 - [Requisitos e Validação através de Testes](/pt/posts/2010-05-22-requirements-validation-tests/)** - Testes como especificação de requisitos

**Parte 13 - [Fundamentos de Testes de Software](/pt/posts/2010-05-29-software-testing/)** - Tipos, níveis e estratégias de testes

**Parte 14 - [Test-Driven Development](/pt/posts/2010-06-05-test-driven-development/)** - Metodologia e práticas TDD

**Parte 15 - [Testes Unitários com JUnit](/pt/posts/2010-06-12-junit-unit-testing/)** - Implementação prática de testes unitários

**Parte 16 - [TDD Avançado: Pensando com Testes](/pt/posts/2010-06-19-tdd-avancado-pensando-com-testes/)** - TDD como mentalidade e ferramenta de design (Final)

Esta série nos levou desde compreender o "porquê" da engenharia de software até dominar práticas avançadas de desenvolvimento. A jornada mostra como o campo evoluiu de processos rígidos para metodologias adaptativas, sempre mantendo qualidade, colaboração e valor para o cliente no centro.

Os princípios e práticas abordados aqui formam a base para construir sistemas de software robustos e sustentáveis que verdadeiramente servem seus usuários e resistem ao teste do tempo.

---

**Navegação:**

- **Anterior:** [Parte 15 - Testes Unitários com JUnit](/pt/posts/2010-06-12-junit-unit-testing/)
- **Série:** [Aulas de Engenharia de Software (16 partes)](/pt/series/aulas-de-engenharia-de-software/)
