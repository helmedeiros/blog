---
title: "Testes Unitários com JUnit: Clareza Antes da Complexidade"
author: helio
date: 2010-06-12 14:30:22+00:00
description:
  Reflexões sobre a décima quinta e última aula de Engenharia de Software,
  explorando testes unitários com JUnit como uma abordagem estruturada para validação,
  ciclos de feedback e melhoria de design.
categories: ["Development"]
tags:
  - Engenharia de Software
  - Testes Unitários
  - JUnit
  - Automação de Testes
  - Test Fixtures
  - Casos de Teste
  - Design
  - Qualidade
  - UnP
  - Ensino
  - serie-engenharia-software
subtitle: Construa confiança através de teste unitário disciplinado—descubra como JUnit, estrutura de teste e verificação sistemática criam redes de segurança que habilitam refatoração sem medo e evolução confiável de código
---

> **Série: Fundamentos da Engenharia de Software** | **Parte 15 de 19** > _Ministrada na Universidade Potiguar (UnP) em 2010_

Nesta aula, expandimos nosso estudo sobre TDD com foco nos **testes unitários**, utilizando o JUnit para mostrar como a validação estruturada transforma lógica vaga em comportamento previsível. A proposta não era apenas testar, mas construir laços de feedback, melhorar o design e reduzir surpresas durante o desenvolvimento.

Quis que a turma entendesse: testar cedo não é apenas programar com defesa. É guiar o desenvolvimento pela intenção.

---

## Antes dos Frameworks: Testes Crus e Seus Limites

Começamos voltando no tempo, para antes do JUnit. Demonstrei como testar um método que calcula raízes quadradas com Java puro. Utilizamos a classe `Calculadora`:

```java
public final class Calculadora {
    public static int qualARaiz(int x) {
        int guess = 1;
        while (guess * guess < x) {
            guess++;
        }
        return guess;
    }
}
```

E testamos manualmente:

```java
public static void main(String[] args) {
    System.out.println(Calculadora.qualARaiz(0));
    System.out.println(Calculadora.qualARaiz(9));
    System.out.println(Calculadora.qualARaiz(100));
}
```

Qual o problema? Não há verificação automática de falhas. É frágil, manual e não escalável.

---

## Entra o JUnit: Nomenclatura, Fixtures e Automação

Apresentamos o JUnit—framework criado por Kent Beck. Definimos os termos-chave:

- **Fixture**: dados preparados para os testes
- **Test Case**: método de validação
- **Test Suite**: conjunto de testes
- **Test Runner**: executa e reporta os testes

A turma escreveu seu primeiro teste anotado:

```java
@Test
public void testCalculaRaiz() {
    assertEquals(3, Calculadora.qualARaiz(9));
    assertEquals(10, Calculadora.qualARaiz(100));
}
```

Discutimos o poder de bons nomes e estrutura clara. Testes bem escritos se tornam **documentação executável**.

---

## Exemplos com Aritmética e Condições

Expandimos com nova lógica de negócio:

```java
public class Aritmetica {
    public static int soma(int i, int j) {
        return i + j;
    }

    public static boolean isPositivo(int numero) {
        return numero > 0;
    }
}
```

E os testes:

```java
@Test
public void testSoma() {
    assertEquals(4, Aritmetica.soma(2,2));
    assertEquals(-15, Aritmetica.soma(-10, -5));
}

@Test
public void testIsPositivo() {
    assertTrue(Aritmetica.isPositivo(5));
    assertFalse(Aritmetica.isPositivo(-10));
}
```

Aqui, os alunos aprenderam que métodos com **responsabilidade única** facilitam a validação. E que **booleans** ajudam a evidenciar falhas rapidamente.

---

## Modelando Comportamento com Contador

Na segunda parte, introduzimos um exemplo mais prático: um `Contador` para filas.

```java
public class Contador {
    private int count = 0;

    public int increment() {
        return ++count;
    }

    public int decrement() {
        return --count;
    }
}
```

E os testes:

```java
@Before
public void setUp() {
    counter = new Contador();
}

@Test
public void testIncrementa() {
    assertEquals(1, counter.increment());
    assertEquals(2, counter.increment());
}

@Test
public void testDecrementa() {
    assertEquals(-1, counter.decrement());
}
```

Os alunos aplicaram o uso do `@Before` para isolar a criação do objeto. Aprenderam que testes independentes aumentam a confiabilidade.

---

## Atividade e Aprendizado

Finalizamos com um desafio: implementar e testar uma classe que valida elegibilidade para votar. Cada equipe teve que definir:

- O que caracteriza um usuário válido
- Quais regras se aplicam
- Como testar bordas e restrições

Na revisão entre times, entenderam a **diferença entre testar lógica e testar comportamento**. E perceberam como a estrutura de testes influencia na manutenção e colaboração.

Facilitadores podem usar esse modelo em treinamentos, mentorias ou programas de integração. Basta escolher uma classe simples, definir os comportamentos e testá-los com clareza.

<div style="margin-bottom: 20px;">
<iframe src="https://www.slideshare.net/slideshow/embed_code/key/KgnPDn6r42boUg?startSlide=1" width="597" height="486" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px;max-width: 100%;" allowfullscreen></iframe> <div style="margin-bottom:5px"><strong> <a href="https://pt.slideshare.net/slideshow/unp-eng-software-aula-28/4487801" title="UnP Eng. Software - Aula 28" target="_blank">UnP Eng. Software - Aula 28</a> </strong> from <strong> <a href="https://www.slideshare.net/heliomedeiros" target="_blank">Hélio Medeiros</a> </strong></div></div>

---

_Postado como parte do diário do curso de Engenharia de Software. Hoje aprendemos que testes unitários com JUnit não são apenas sobre capturar bugs—são sobre construir sistemas que comunicam sua intenção claramente e evoluem com segurança._

---

### **Navegação da Série**

- **Introdução**: [Parte 1 - Por que Engenharia de Software?](../2010-02-24-software-engineering-purpose/)
- **Anterior**: [Parte 14 - Desenvolvimento Orientado a Testes](../2010-06-05-test-driven-development/)
- **Próxima**: [Parte 16 - TDD Avançado: Pensando com Testes](../2010-06-19-tdd-avancado-pensando-com-testes/)
- **Atual**: Parte 15 - Testes Unitários com JUnit
- **Série completa**: [Por que Engenharia de Software?](../2010-02-24-software-engineering-purpose/) | [Domando a Complexidade](../2010-03-02-complexity-process/) | [Modelo Cascata](../2010-03-10-waterfall-model/) | [Modelos Evolutivos](../2010-03-18-evolutionary-models/) | [Mentalidade Ágil](../2010-03-26-agile-mindset/) | [Produtividade Scrum](../2010-04-03-scrum-productivity/) | [Ciclo Scrum](../2010-04-11-scrum-cycle/) | [XP Qualidade & Coragem](../2010-04-19-xp-quality-courage/) | [XP Princípios & Práticas](../2010-05-01-xp-principles-practices/) | [XP na Prática](../2010-05-08-applying-xp-strategies/) | [Domain-Driven Design](../2010-05-15-domain-driven-design/) | [Requisitos & Testes](../2010-05-22-requirements-validation-tests/) | [Testando Software](../2010-05-29-software-testing/) | [Desenvolvimento Orientado a Testes](../2010-06-05-test-driven-development/) | [Testes Unitários com JUnit](../2010-06-12-junit-unit-testing/) | [TDD Avançado: Pensando com Testes](../2010-06-19-tdd-avancado-pensando-com-testes/)
