---
title: "Mike Keith – Java EE 6: Uma Grande Evolução"
author: helio
layout: post
date: 2009-11-20 14:22:51+00:00
idptt_tweeted:
  - 1
series: TDC Rio 2009
categories:
  - Events
  - Technology
tags:
  - EJB 3.1
  - Eventos
  - Global Code
  - J2EE
  - Mike Keith
  - TDC 2009
subtitle: Testemunhe o renascimento do Java EE—descubra como anotações, servlets assíncronos e EJBs leves finalmente fazem o desenvolvimento Java empresarial parecer moderno, produtivo e livre de XML
---

> **Série: TDC Rio 2009** | **Parte 1 de 2** > _Insights fundamentais da maior conferência Java do Brasil_

![Foto da palestra do Mike Keith](/uploads/2009/11/dsc00699.jpg)

A palestra de **Mike Keith** começou por volta das 11h, logo após o coffee break, com um tom leve e descontraído. Ele abriu brincando sobre o tempo entre os lançamentos das versões Java — algo que gerava expectativas (e frustrações) constantes. Um dos slides logo no início estampava a frase provocativa:

> "Ou você não se importa porque acha que a Microsoft vai matar o Java."

A provocação arrancou risos e um pouco de desconforto — mas serviu de gancho para mostrar como, apesar das críticas, o **Java EE 6** trazia sim avanços sólidos e relevantes.

## Java EE 6: Mais modular, menos XML

Mike apresentou as principais novidades da nova especificação. Uma das mais comentadas foi a **redução da verbosidade**, especialmente em relação ao uso de XML. Com a chegada de **anotações (@Annotation)** no lugar de configurações externas, o código se torna mais direto e mais fácil de manter.

```java
@WebServlet("/minhaRota")
public class MeuServlet extends HttpServlet {
    // ...
}
```

Antes, isso exigiria várias linhas no `web.xml`. Agora, está tudo embutido no próprio código.

## Anotações e modularização: o fim do "acoplamento obscuro"

A nova abordagem com **anotações** também torna mais claro **quais dependências e comportamentos estão em jogo** em cada classe. Isso combate o famoso acoplamento oculto, onde as configurações externas escondiam o que estava acontecendo.

Essa mudança também ajuda quem usa frameworks como Spring, Struts, ou JSF, onde anotações já estavam se tornando padrão.

## Servlets Assíncronos (Async Processing)

Outro ponto que me chamou atenção foi a introdução de **processamento assíncrono nos Servlets**. Isso significa que não precisamos mais bloquear a thread do servidor para esperar uma operação longa (como uma chamada de API ou acesso a banco lento).

> Em termos simples, o servidor pode "entregar outra tarefa" enquanto espera pela resposta — algo que melhora muito o desempenho sob carga.

Mike demonstrou isso comentando que, apesar do ganho, é necessário cuidado para não cair em armadilhas de concorrência ou complexidade desnecessária.

## EJB 3.1: A reabilitação?

Confesso: quando ele mencionou **EJB**, achei que o auditório ia bocejar. Mas Mike trouxe uma visão moderna com o **EJB 3.1**, agora mais leve e pragmático. Algumas melhorias que ele comentou:

- Possibilidade de usar **EJBs fora de um contêiner completo de aplicação**
- Redução no uso obrigatório de interfaces
- Mais integração com ambientes "Java SE" (sem servidor)

A sala ficou mais atenta do que eu esperava — talvez por ver que o EJB estava finalmente se tornando mais acessível para quem evitava por puro trauma de versões antigas.

## JPA e a conversa da tarde

A parte sobre **JPA (Java Persistence API)** foi mencionada brevemente na palestra, mas gerou tanto interesse que acabou virando tema de uma conversa à parte no período da tarde.

JPA, para quem não conhece, é a especificação padrão para mapeamento objeto-relacional em Java. Em vez de escrever SQL direto, usamos classes Java para representar entidades e persistência.

## Injeção de Dependência (JSR 330)

Outro tópico foi a **JSR 330**, que trata de **injeção de dependência** — ou seja, como uma classe "recebe" seus componentes prontos, sem ter que criá-los manualmente. Isso já era comum em frameworks como Spring, mas agora fazia parte da especificação oficial.

> A ideia aqui é diminuir o acoplamento e facilitar testes, ao evitar `new` e deixar a responsabilidade de criação para o contêiner.

## Conclusão otimista

Mike fechou sua fala com otimismo. Disse que muitas das melhorias já estavam disponíveis em versões beta ou em especificações abertas — com previsão de se tornarem oficiais em **dezembro de 2009**.

Para mim, ficou claro que o Java EE 6 não era apenas uma nova versão. Era um sinal de que a plataforma estava ouvindo a comunidade e tentando **ser mais leve, moderna e produtiva**.

---

_Publicado no mesmo dia da palestra de Mike Keith no TDC Rio 2009._

---

### **Navegação da Série**

- **Atual**: Parte 1 - Mike Keith - Java EE 6: Uma Grande Evolução
- **Próximo**: [Parte 2 - Rod Johnson sobre tendências Java EE e os próximos 5 anos](../2009-11-25-rod-johnson-tendencias-em-java-ee-como-serao-os-proximos-5-anos/)
- **Série completa**: [Série TDC Rio 2009](/pt/series/tdc-rio-2009/)
