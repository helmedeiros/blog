---
title: "Padrões Comportamentais: Coordenando Responsabilidades com Flexibilidade"
author: helio
layout: post
date: 2008-07-08 03:27:57+00:00
categories:
  - Architecture

subtitle: "Projete interações inteligentes de objetos e workflows—domine padrões Observer, Strategy, Command e State que transformam sistemas rígidos e acoplados em arquiteturas flexíveis e orientadas a eventos que se adaptam a regras de negócio em mudança"
---

> **Série: Padrões de Projeto e Análise** | **Parte 4 de 4** > _Desenvolvido durante o Mestrado em Projetos de Sistemas Web_

**Chegamos ao capítulo final** desta série de padrões de projeto. Depois de construir ([Padrões de Criação](../2008-07-04-padroes-de-criacao/)) e estruturar ([Padrões Estruturais](../2008-07-06-padroes-estruturais/)) seus objetos, o próximo desafio é fazer com que eles interajam.

Depois de construir (Criação) e estruturar (Estrutural) seus objetos, o próximo desafio é fazer com que eles interajam.
**Padrões de Projeto Comportamentais** tratam de **como os objetos se comunicam**, distribuem responsabilidades e reagem a eventos de maneira flexível e de fácil manutenção.

Esses padrões ajudam a reduzir lógicas condicionais complexas, evitam acoplamentos rígidos e aumentam a clareza do sistema.

## O Que São Padrões Comportamentais?

Eles descrevem maneiras comuns de **objetos interagirem e cooperarem**, sem conhecer os detalhes internos uns dos outros.

Use quando:

- Você precisa alterar o comportamento de objetos em tempo de execução
- Quer evitar blocos grandes de `if/else` ou `switch/case`
- Deseja manter responsabilidades claras e interações modulares

## Tipos de Padrões Comportamentais

### Chain of Responsibility (Cadeia de Responsabilidade)

Passa uma solicitação por uma cadeia de manipuladores até que um possa processá-la.

- **Intenção**: Evitar acoplamento entre remetente e receptor.
- **Use quando**: Há uma sequência de verificações ou validações.

<img src="/uploads/2008/07/chain-of-responsibility-pattern.png" alt="Diagrama UML de Chain of Responsibility" class="behavioral-pattern-img">

```java
abstract class Handler {
    protected Handler next;
    public void setNext(Handler next) { this.next = next; }
    public void handle(Request req) {
        if (canHandle(req)) process(req);
        else if (next != null) next.handle(req);
    }
}
```

### Command (Comando)

Encapsula uma solicitação como objeto.

- **Intenção**: Parametrizar ações, agendar ou desfazer operações.
- **Use quando**: Você precisa de histórico de ações ou fila de tarefas.

<img src="/uploads/2008/07/command-pattern.png" alt="Diagrama UML de Command" class="behavioral-pattern-img">

```java
interface Command {
    void execute();
}

class LightOnCommand implements Command {
    Light light;
    void execute() { light.turnOn(); }
}
```

### Iterator (Iterador)

Fornece uma maneira de acessar elementos de uma coleção sequencialmente.

- **Intenção**: Separar a lógica de iteração da estrutura da coleção.
- **Use quando**: Você quer iteração padronizada sobre coleções diferentes.

<img src="/uploads/2008/07/iterator-pattern.png" alt="Diagrama UML de Iterator" class="behavioral-pattern-img">

```java
interface Iterator<T> {
    boolean hasNext();
    T next();
}
```

### Mediator (Mediador)

Centraliza a comunicação entre objetos.

- **Intenção**: Reduzir acoplamento entre componentes.
- **Use quando**: Há comunicação complexa entre muitos objetos.

<img src="/uploads/2008/07/mediator-pattern.png" alt="Diagrama UML de Mediator" class="behavioral-pattern-img">

```java
interface Mediator {
    void notify(Component sender, String event);
}
```

### Memento (Memento)

Captura e restaura o estado interno de um objeto.

- **Intenção**: Permitir "desfazer" sem expor o estado interno.
- **Use quando**: Você precisa de checkpoints e recuperação.

<img src="/uploads/2008/07/memento-pattern.png" alt="Diagrama UML de Memento" class="behavioral-pattern-img">

```java
class EditorMemento {
    private String content;
    public String getContent() { return content; }
}
```

### Observer (Observador)

Notifica objetos dependentes quando o estado de um sujeito muda.

- **Intenção**: Criar dependência reativa um-para-muitos.
- **Use quando**: Você quer arquitetura orientada a eventos.

<img src="/uploads/2008/07/observer-pattern.png" alt="Diagrama UML de Observer" class="behavioral-pattern-img">

```java
interface Observer {
    void update();
}

class Subject {
    List<Observer> observers;
    void notifyAll() {
        for (Observer obs : observers) obs.update();
    }
}
```

### State (Estado)

Altera o comportamento de um objeto conforme seu estado.

- **Intenção**: Representar estados como objetos separados.
- **Use quando**: Há lógica condicional baseada em estado.

<img src="/uploads/2008/07/state-pattern.png" alt="Diagrama UML de State" class="behavioral-pattern-img">

```java
interface State {
    void handle(Context context);
}
```

### Strategy (Estratégia)

Define uma família de algoritmos intercambiáveis.

- **Intenção**: Separar a lógica do algoritmo do contexto.
- **Use quando**: Você quer trocar comportamentos em tempo de execução.

<img src="/uploads/2008/07/strategy-pattern.png" alt="Diagrama UML de Strategy" class="behavioral-pattern-img">

```java
interface SortStrategy {
    void sort(List data);
}

class QuickSort implements SortStrategy { ... }
class MergeSort implements SortStrategy { ... }
```

### Template Method (Método Template)

Define a estrutura de um algoritmo e permite que subclasses implementem os passos.

- **Intenção**: Preservar o esqueleto do processo com personalização.
- **Use quando**: Há lógica comum com variações específicas.

<img src="/uploads/2008/07/template-method-pattern.png" alt="Diagrama UML de Template Method" class="behavioral-pattern-img">

```java
abstract class DataParser {
    public final void parse() {
        readData();
        processData();
        writeData();
    }
    protected abstract void readData();
    protected abstract void processData();
    protected abstract void writeData();
}
```

### Visitor (Visitante)

Separa operações da estrutura de objetos que as recebe.

- **Intenção**: Adicionar operações sem modificar as classes alvo.
- **Use quando**: Há múltiplas operações diferentes sobre uma estrutura de objetos.

<img src="/uploads/2008/07/visitor-pattern.png" alt="Diagrama UML de Visitor" class="behavioral-pattern-img">

```java
interface Visitor {
    void visit(Book book);
    void visit(Fruit fruit);
}
```

## Tabela Comparativa

| Padrão                  | Melhor Uso                             | Evita                                  |
| ----------------------- | -------------------------------------- | -------------------------------------- |
| Chain of Responsibility | Lógica sequencial com fallback         | Condições aninhadas                    |
| Command                 | Histórico de ações, botões de UI       | Acoplamento entre remetente e ação     |
| Iterator                | Acesso padronizado a coleções          | Lógica de iteração acoplada            |
| Mediator                | Comunicação entre muitos componentes   | Dependências cruzadas                  |
| Memento                 | Desfazer operações                     | Exposição de estado interno            |
| Observer                | Atualizações reativas                  | Gerenciamento manual de dependências   |
| State                   | Comportamentos baseados em estado      | Switch/case extensos                   |
| Strategy                | Algoritmos flexíveis                   | Lógica fixa no código                  |
| Template Method         | Processo com variação em etapas        | Duplicação de lógica em subclasses     |
| Visitor                 | Operações sobre hierarquias de objetos | Poluição de classes com lógica externa |

## Considerações Finais

Padrões comportamentais fornecem as **regras de interação** entre os objetos do seu sistema. Promovem clareza, extensibilidade e modularidade em como a lógica é executada e coordenada.

Com os três grupos explorados — Criação, Estrutural e Comportamental — temos agora uma base sólida para projetar software que equilibra flexibilidade, clareza e evolução contínua.

---

### **Navegação da Série**

- **Introdução**: [Padrões de Análise](../2008-07-01-padroes-de-analise/)
- **Anterior**: [Parte 3 - Padrões Estruturais](../2008-07-06-padroes-estruturais/)
- **Atual**: Parte 4 - Padrões Comportamentais (Final)
- **Série completa**: [Padrões de Análise](../2008-07-01-padroes-de-analise/) | [Padrões de Projeto Overview](../2008-07-02-padroes-de-projeto-detalhado/) | [Padrões de Criação](../2008-07-04-padroes-de-criacao/) | [Padrões Estruturais](../2008-07-06-padroes-estruturais/)
