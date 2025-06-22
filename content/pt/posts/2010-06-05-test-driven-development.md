---
title: "Desenvolvimento Orientado a Testes: Construindo a Coisa Certa da Forma Certa"
author: helio
date: 2010-06-05 14:30:22+00:00
description:
  Reflexões sobre a décima quarta aula de Engenharia de Software, explorando
  o Desenvolvimento Orientado a Testes como uma metodologia de design que vai além
  dos testes para moldar como pensamos sobre construir software.
categories: ["Development"]
tags:
  - Engenharia de Software
  - Desenvolvimento Orientado a Testes
  - TDD
  - Vermelho-Verde-Refatoração
  - TDD de Aceitação
  - ATDD
  - Design
  - Qualidade
  - UnP
  - Ensino
  - serie-engenharia-software
subtitle: Domine o ciclo vermelho-verde-refatorar—descubra como TDD transforma teste de pensamento posterior em ferramenta de design, criando confiança, melhor arquitetura e documentação viva através de prática disciplinada
---

> **Série: Fundamentos da Engenharia de Software** | **Parte 14 de 19** > _Ministrada na Universidade Potiguar (UnP) em 2010_

Nesta aula, exploramos o **Desenvolvimento Orientado a Testes (TDD)** para além das frases prontas. Focamos em seu impacto na qualidade do software, na evolução do código e na mentalidade de que testar não é uma fase, mas sim uma forma de projetar. Não foi uma aula sobre sintaxe, mas sobre **como pensar como alguém que projeta com propósito e validação**.

TDD não é escrever testes. É desenhar com confiança e clareza.

## O Problema Certo, da Forma Certa

Começamos analisando uma armadilha comum em projetos de software: criar soluções sofisticadas para problemas mal definidos. O TDD quebra esse ciclo ao forçar a definição do comportamento esperado antes da lógica. Isso coloca a clareza na frente da complexidade.

Os alunos foram desafiados a refatorar um método existente apenas após escrever testes que falhavam. A ideia era **repensar o design a partir dos testes**.

Um dos exemplos:

```java
@Test
public void testCalculateTotalWithDiscount() {
    Cart cart = new Cart();
    cart.add(new Product("Livro", 50));
    cart.applyDiscount("ESTUDANTE10");

    assertEquals(45, cart.getTotal());
}
```

Antes mesmo de codificar `applyDiscount`, os alunos precisavam decidir:

- Como um desconto será representado?
- Quem tem direito a ele?
- Qual o estado final correto?

## Vermelho-Verde-Refatore

Estudamos o ciclo central do TDD: **Vermelho-Verde-Refatore**. Os alunos praticaram cada passo com clareza:

1. **Vermelho**: Escreva um teste que falha.
2. **Verde**: Escreva o mínimo código necessário para passar.
3. **Refatore**: Melhore o código sem alterar seu comportamento.

Um exercício inicial envolvia validação de string:

```python
def test_should_not_allow_empty_username():
    with pytest.raises(ValueError):
        User(username="")

# Implemente só o necessário:
class User:
    def __init__(self, username):
        if username == "":
            raise ValueError("Username obrigatório")
```

A refatoração veio depois: extração de validação, adição de restrições, remoção de duplicações.

## Atividades Práticas e Ciclos Reais

Introduzi uma kata de sala de aula: um sistema de precificação para tipos de ingressos (estudante, normal, idoso). Cada aluno escrevia um teste, fazia-o passar e refatorava—e passava para o próximo membro do grupo.

Com isso, o código nascia e evoluía com **restrições deliberadas**, não com superengenharia. Em 30 minutos, tínhamos um motor de preços com quatro regras, sem duplicações e 100% coberto por testes.

Outro exercício envolveu lógica de calculadora em terminal:

```ruby
describe Calculator do
  it "adds two numbers" do
    calc = Calculator.new
    expect(calc.add(2, 3)).to eq(5)
  end
end
```

Mesmo exemplos simples ensinam como esclarecer o comportamento por meio de testes, e não por adivinhação de requisitos futuros.

## Acceptance TDD: Construindo a Coisa Certa

Além do design orientado a testes, abordamos o **Acceptance TDD (ATDD)**—validar que o que estamos construindo realmente resolve a necessidade do usuário. Os alunos escreveram testes de aceitação para uma funcionalidade de busca com restrições como "retornar no máximo 10 resultados em menos de 1 segundo".

Perceberam que o próprio teste se tornava um **artefato de requisito**, alinhando desenvolvedores, QA e usuários.

Discutimos os riscos de não ter esse alinhamento: funcionalidades mal compreendidas, testadas apenas superficialmente ou construídas sem validar o real valor.

Facilitadores podem aplicar esse exercício durante refinamento de backlog: se você não consegue transformar a necessidade em um teste executável, ainda não entendeu o requisito.

---

## Considerações Finais

O objetivo desta aula não foi ensinar TDD como metodologia, mas fazer com que os alunos **internalizassem** esse ciclo como estratégia de design e feedback.

TDD ajuda desenvolvedores a se manterem focados: sem saltos grandes, sem código desperdiçado. É um ciclo de descoberta e simplificação. E num mundo onde qualquer mudança traz risco, **projetar testando é o seu corrimão.**

<div style="margin-bottom: 20px;">
<iframe src="https://www.slideshare.net/slideshow/embed_code/key/xBnDqOwtdg2Njq?startSlide=1" width="597" height="486" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px;max-width: 100%;" allowfullscreen></iframe> <div style="margin-bottom:5px"><strong> <a href="https://pt.slideshare.net/slideshow/unp-eng-software-aula-27/4487762" title="UnP Eng. Software - Aula 27" target="_blank">UnP Eng. Software - Aula 27</a> </strong> from <strong> <a href="https://www.slideshare.net/heliomedeiros" target="_blank">Hélio Medeiros</a> </strong></div></div>

---

_Postado como parte do diário do curso de Engenharia de Software. Hoje aprendemos que TDD não é apenas sobre testes—é sobre projetar com confiança e construir sistemas que evoluem através de passos deliberados e validados._

---

### **Navegação da Série**

- **Introdução**: [Parte 1 - Por que Engenharia de Software?](../2010-02-24-software-engineering-purpose/)
- **Anterior**: [Parte 13 - Testando Software](../2010-05-29-software-testing/)
- **Próxima**: [Parte 15 - Testes Unitários com JUnit](../2010-06-12-junit-unit-testing/)
- **Atual**: Parte 14 - Desenvolvimento Orientado a Testes
- **Série completa**: [Por que Engenharia de Software?](../2010-02-24-software-engineering-purpose/) | [Domando a Complexidade](../2010-03-02-complexity-process/) | [Modelo Cascata](../2010-03-10-waterfall-model/) | [Modelos Evolutivos](../2010-03-18-evolutionary-models/) | [Mentalidade Ágil](../2010-03-26-agile-mindset/) | [Produtividade Scrum](../2010-04-03-scrum-productivity/) | [Ciclo Scrum](../2010-04-11-scrum-cycle/) | [XP Qualidade & Coragem](../2010-04-19-xp-quality-courage/) | [XP Princípios & Práticas](../2010-05-01-xp-principles-practices/) | [XP na Prática](../2010-05-08-applying-xp-strategies/) | [Domain-Driven Design](../2010-05-15-domain-driven-design/) | [Requisitos & Testes](../2010-05-22-requirements-validation-tests/) | [Testando Software](../2010-05-29-software-testing/) | Desenvolvimento Orientado a Testes | [Testes Unitários com JUnit](../2010-06-12-junit-unit-testing/)
