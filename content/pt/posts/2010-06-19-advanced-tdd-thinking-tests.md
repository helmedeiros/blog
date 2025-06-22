---
title: "TDD Avançado: Pensando com Testes"
date: 2010-06-19 09:00:00-03:00
tags:
  - engenharia de software
  - tdd
  - testes
  - java
  - junit
  - desenvolvimento
categories: ["Development"]
series:
  - Aulas de Engenharia de Software
slug: tdd-avancado-pensando-com-testes
summary:
  Nesta aula, aprofundamos o uso de Test-Driven Development (TDD), mostrando
  que ele é mais do que uma técnica — é uma forma de pensar. Utilizando um sistema
  real de template de e-mails, desenvolvemos tudo partindo de testes. Cada linha foi
  uma decisão validada, cada falha evitada antes de acontecer.
subtitle: Eleve sua prática TDD além do básico—descubra como pensar em testes molda design, dirige decisões de arquitetura e cria documentação viva que evolui com seu entendimento
---

**Aulas de Engenharia de Software - Parte 16 de 19**

Nesta aula, aprofundamos o uso de Test-Driven Development (TDD), mostrando que ele é mais do que uma técnica — é uma forma de pensar. Utilizando um sistema real de template de e-mails, desenvolvemos tudo partindo de testes. Cada linha foi uma decisão validada, cada falha evitada antes de acontecer.

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

## Programação por Intenção

Falamos sobre **programar por intenção**: escrever código como se ele já existisse. Pensar primeiro no uso, depois na implementação. Isso força foco no "_o quê_" e não no "_como_".

Esse estilo favorece clareza e coesão.

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

## Refatoração Final e Aprendizados

Reduzimos duplicações usando `@Before` e métodos auxiliares. Os testes ficaram mais claros, reutilizáveis e expressivos.

TDD não é sobre ferramenta. É sobre mentalidade. É um guia para projetar com clareza e entregar com confiança.

Facilitadores podem usar esse modelo em treinamentos, mentorias ou programas de integração. Basta escolher uma classe simples, definir os comportamentos e testá-los com clareza.

---

**Navegação:**

- **Anterior:** [Parte 15 - Testes Unitários com JUnit](/pt/posts/2010-06-12-junit-unit-testing/)
- **Próxima:** [Parte 17 - Controle de Versão: Não Programe Sem Isso](/pt/posts/2010-06-26-controle-versao-fundacao-essencial/)
- **Série:** [Aulas de Engenharia de Software (17 partes)](/pt/series/aulas-de-engenharia-de-software/)
