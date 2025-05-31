---
title: "Behavioral Design Patterns: Coordinating Responsibilities with Flexibility"
author: helio
layout: post
date: 2008-07-08T03:27:57+00:00
categories:
  - Design Patterns
---

> **Series: Design Patterns and Analysis** | **Part 4 of 4** > _Developed during Master's in Web Systems Projects_

**We've reached the final chapter** of this design patterns series. Once your objects are built ([Creational Patterns](../2008-07-04-padroes-de-criacao/)) and structured ([Structural Patterns](../2008-07-06-padroes-estruturais/)), the next challenge is interaction.

**Behavioral Design Patterns** are all about **how objects communicate**, distribute responsibilities, and respond to events in a flexible, maintainable way.

These patterns help reduce complex conditional logic, prevent tight coupling, and increase clarity.

## What Are Behavioral Patterns?

They describe common ways for **objects to interact and cooperate**, without knowing too much about each other's internal details.

Use them when:

- You need to change the behavior of objects at runtime
- You want to avoid bloated switch/case blocks or chained if-else
- You want to keep responsibilities focused and interactions modular

## Types of Behavioral Patterns

### Chain of Responsibility

Passes a request along a chain of handlers until one can process it.

- **Intent**: Avoid coupling sender and receiver of a request.
- **Use When**: You have a sequence of handlers with fallback logic.

<img src="/uploads/2008/07/chain-of-responsibility-pattern.png" alt="UML Diagram of Chain of Responsibility" class="behavioral-pattern-img">

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

### Command

Encapsulates a request as an object.

- **Intent**: Parameterize actions with objects, queue operations, support undo.
- **Use When**: You need action history or task scheduling.

<img src="/uploads/2008/07/command-pattern.png" alt="UML Diagram of Command" class="behavioral-pattern-img">

```java
interface Command {
    void execute();
}

class LightOnCommand implements Command {
    Light light;
    void execute() { light.turnOn(); }
}
```

### Iterator

Provides a way to access elements of a collection sequentially.

- **Intent**: Decouple iteration logic from the collection itself.
- **Use When**: You want standard iteration across different structures.

<img src="/uploads/2008/07/iterator-pattern.png" alt="UML Diagram of Iterator" class="behavioral-pattern-img">

```java
interface Iterator<T> {
    boolean hasNext();
    T next();
}
```

### Mediator

Centralizes communication between objects.

- **Intent**: Reduce coupling between components by introducing a mediator object.
- **Use When**: You have complex many-to-many communication.

<img src="/uploads/2008/07/mediator-pattern.png" alt="UML Diagram of Mediator" class="behavioral-pattern-img">

```java
interface Mediator {
    void notify(Component sender, String event);
}
```

### Memento

Captures and restores an object's internal state.

- **Intent**: Provide undo functionality without exposing internal state.
- **Use When**: You need checkpoint and restore operations.

<img src="/uploads/2008/07/memento-pattern.png" alt="UML Diagram of Memento" class="behavioral-pattern-img">

```java
class EditorMemento {
    private String content;
    public String getContent() { return content; }
}
```

### Observer

Notifies dependent objects when a subject changes state.

- **Intent**: One-to-many dependency without tight coupling.
- **Use When**: You want event-driven architecture.

<img src="/uploads/2008/07/observer-pattern.png" alt="UML Diagram of Observer" class="behavioral-pattern-img">

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

### State

Changes an object's behavior when its state changes.

- **Intent**: Represent different states as objects.
- **Use When**: You have complex conditional logic dependent on state.

<img src="/uploads/2008/07/state-pattern.png" alt="UML Diagram of State" class="behavioral-pattern-img">

```java
interface State {
    void handle(Context context);
}
```

### Strategy

Defines a family of interchangeable algorithms.

- **Intent**: Separate algorithm logic from the context where it's used.
- **Use When**: You want to switch behavior at runtime.

<img src="/uploads/2008/07/strategy-pattern.png" alt="UML Diagram of Strategy" class="behavioral-pattern-img">

```java
interface SortStrategy {
    void sort(List data);
}

class QuickSort implements SortStrategy { ... }
class MergeSort implements SortStrategy { ... }
```

### Template Method

Defines the skeleton of an algorithm, letting subclasses implement steps.

- **Intent**: Preserve the structure of an operation but allow customization.
- **Use When**: You want base logic with overridable hooks.

<img src="/uploads/2008/07/template-method-pattern.png" alt="UML Diagram of Template Method" class="behavioral-pattern-img">

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

### Visitor

Separates operations from the objects on which they operate.

- **Intent**: Add operations to object structures without modifying them.
- **Use When**: You need to perform multiple unrelated operations on a structure.

<img src="/uploads/2008/07/visitor-pattern.png" alt="UML Diagram of Visitor" class="behavioral-pattern-img">

```java
interface Visitor {
    void visit(Book book);
    void visit(Fruit fruit);
}
```

## Comparison Table

| Pattern                 | Best For                          | Helps Avoid                        |
| ----------------------- | --------------------------------- | ---------------------------------- |
| Chain of Responsibility | Sequential fallback logic         | Nested conditionals                |
| Command                 | Action history, UI buttons        | Tight sender-receiver coupling     |
| Iterator                | Standard traversal of collections | Mixing logic and data structure    |
| Mediator                | Simplifying object communication  | Complex dependencies               |
| Memento                 | Undo functionality                | Leaky internal state               |
| Observer                | Event systems, reactive updates   | Manual dependency management       |
| State                   | Dynamic behavior changes          | Bloated switch statements          |
| Strategy                | Swappable algorithms              | Hardcoded logic                    |
| Template Method         | Custom steps in fixed process     | Duplicated code in subclasses      |
| Visitor                 | Operations on object hierarchies  | Polluting classes with extra logic |

## Final Thoughts

Behavioral patterns provide the **rules of interaction** for objects in your system. They promote clarity, extensibility, and modularity in how logic is executed and coordinated.

With all three categories explored — Creational, Structural, Behavioral — we now have a solid foundation for software design that balances flexibility, clarity, and evolution.

---

### **Series Navigation**

- **Introduction**: [Analysis Patterns](../2008-07-01-padroes-de-analise/)
- **Previous**: [Part 3 - Structural Patterns](../2008-07-06-padroes-estruturais/)
- **Current**: Part 4 - Behavioral Patterns (Final)
- **Complete series**: [Analysis Patterns](../2008-07-01-padroes-de-analise/) | [Design Patterns Overview](../2008-07-02-padroes-de-projeto-detalhado/) | [Creational Patterns](../2008-07-04-padroes-de-criacao/) | [Structural Patterns](../2008-07-06-padroes-estruturais/)
