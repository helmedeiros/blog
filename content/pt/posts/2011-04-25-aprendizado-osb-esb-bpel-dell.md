---
title: "Além do Java: Aprendendo OSB, ESB e BPEL no Segundo Trimestre na Dell"
date: 2011-04-25
series: "Life in Porto Alegre"
tags: ["Dell", "OSB", "ESB", "BPEL", "Java", "Oracle", "Aprendizado"]
---

_Esta é a Parte 4 de 4 da série [Life in Porto Alegre](/pt/series/life-in-porto-alegre/)._

Seis meses após minha chegada à Dell, estou no meio de uma das transições mais empolgantes da minha carreira. Nosso time está migrando lógicas que antes viviam em código Java tradicional para ferramentas de orquestração como **Oracle Service Bus (OSB)**. E não estou só assistindo — fui convidado a **liderar essa transformação**.

### Um Engenheiro Java em Território de Drag-and-Drop

Antes disso, escrevia todos os meus transformers, clients e parsers diretamente em Java. Tudo era código: mapeamentos, tratamento de falhas, validações, sequenciamento — tudo encapsulado em classes anotadas e muitos testes unitários. Eu tinha controle total da pilha, e adorava isso.

Agora estou entrando num mundo onde orquestração e transformação são **desenhadas visualmente**, e o comportamento é **configurado ao invés de codado**. No início, me pareceu abstrato, quase simplista demais. Mas com a mentoria do nosso tech lead **Carlos Eduardo (Cadu)**, muita leitura e prática, estou começando a ver a beleza disso tudo.

### O Que Mudou

Aqui vai um comparativo direto:

| Conceito               | Abordagem em Java                    | Abordagem com BPEL / OSB                |
| ---------------------- | ------------------------------------ | --------------------------------------- |
| Transformação de dados | POJO + bibliotecas de mapeamento     | XSLT ou mapeamento visual               |
| Chamada de serviços    | Clients manuais + tratamento de erro | Pipelines declarativos via proxy        |
| Gestão de erros        | Blocos try/catch                     | Handlers de falha configuráveis         |
| Testes                 | JUnit/TestNG                         | Simulações de fluxo + testes integrados |
| Deploy                 | WAR/EAR com CI                       | Artefatos via Console do WebLogic       |

A maior diferença? **Sair do código como lógica, e entrar na lógica como configuração**. Isso é poderoso — mas exige **uma mudança de mentalidade**.

### Os Prós (Até Agora)

- Onboarding mais rápido para quem não conhece o código
- Blocos reutilizáveis através de pipelines OSB
- Visibilidade centralizada dos fluxos de integração
- Menos código repetitivo para operações simples
- Estímulo a uma separação de responsabilidades mais clara

### E os Contras (Na Minha Perspectiva)

- Mais difícil de **depurar e rastrear**
- Ferramentas podem parecer **lentas ou engessadas**
- Lógica complexa pode ficar **espremida nos diagramas**
- Falta de **type safety** como no Java
- Difícil colaborar quando não dá pra fazer "diff" facilmente

Mas ainda estou aprendendo. Muito disso pode mudar com o tempo — e talvez já esteja mudando à medida que fico mais confortável com essas ferramentas.

### Me Apropriando, e Apoiando o Time

Neste trimestre, investi bastante tempo **habilitando o resto do time**. Fiz pareamentos, gravei tutoriais, construí pipelines de referência, documentei armadilhas — tudo faz parte da missão. E o melhor de tudo? Estou animado com isso.

```xml
<!-- Exemplo de pipeline no OSB -->
<service>
  <pipeline>
    <stage>
      <request>
        <replace var="body">
          <xslt>transformarCliente.xsl</xslt>
        </replace>
      </request>
    </stage>
  </pipeline>
</service>
```

```java
// Equivalente em Java para transformação de dados
Cliente paraCliente(XmlCliente entrada) {
    Cliente c = new Cliente();
    c.setId(entrada.getId());
    c.setNome(entrada.getNomeCompleto().toUpperCase());
    return c;
}
```

### Pensamento Final

Aprender OSB me lembrou de uma verdade essencial: **as ferramentas mudam, mas o pensamento de engenharia permanece**. Entradas e saídas claras. Limites bem definidos. Tratamento de falhas robusto. Logs eficientes. Isso vale tanto no código quanto na configuração.

Ainda amo Java. Mas estou abraçando esse novo conjunto de ferramentas com curiosidade e energia. E graças ao Cadu e ao time, nunca me senti tão preparado para aprender.

Mais em breve — essa jornada de transformação está só começando.

---

**Série Life in Porto Alegre:**

- [Parte 1: Nova Cidade, Novo Código, Novo Idioma](/pt/posts/2010-11-15-primeira-semana-dell-porto-alegre/)
- [Parte 2: Foco Total, Pomodoro e Migração com Confiança](/pt/posts/2010-12-16-migracao-foco-pomodoro-dell/)
- [Parte 3: Final de Semana de Release, Automação e o Valor da Liderança de Verdade](/pt/posts/2011-01-30-final-de-semana-de-release-dell/)
- **Parte 4: Além do Java: Aprendendo OSB, ESB e BPEL no Segundo Trimestre na Dell** _(você está aqui)_
