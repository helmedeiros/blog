---
title: "Creational Design Patterns: Building Objects with Flexibility"
author: helio
layout: post
date: 2008-07-04T03:27:57+00:00
categories:
  - Design Patterns
---

> **Series: Design Patterns and Analysis** | **Part 2 of 4** > _Developed during Master's in Web Systems Projects_

**Continuing our series**, after understanding the [importance of design patterns](../2008-07-02-padroes-de-projeto-detalhado/), we now explore the first specific category. Creational patterns solve one of the most fundamental problems in object-oriented design.

Creational patterns solve one of the most fundamental problems in object-oriented design:
**How do we create objects in a way that is flexible, decoupled, and testable?**

This post dives deeper into the first category of design patterns — **Creational Patterns** — and explores their key ideas, structure, and when to use them in real systems.

## What Are Creational Patterns?

These patterns **encapsulate the object creation process**, hiding the complexities of instantiation and making the code more flexible to change.

They help avoid:

- Hardcoding constructors (`new`) all over the system
- Tightly coupling your code to specific classes
- Problems in object configuration, duplication, or reuse

## Types of Creational Patterns

### Factory Method

Creates objects through a factory interface instead of calling constructors directly.

- **Intent**: Define an interface for creating an object, but let subclasses decide which class to instantiate.
- **Use When**: You want to delegate instantiation to subclasses.

<img src="/uploads/2008/07/factory-method-pattern.png" alt="UML Diagram of Factory Method" class="creational-pattern-img">

```java
abstract class Dialog {
    public void renderWindow() {
        Button okButton = createButton();
        okButton.render();
    }
    protected abstract Button createButton();
}
```

### Abstract Factory

Groups related factories together under a unified interface.

- **Intent**: Provide an interface for creating families of related or dependent objects without specifying their concrete classes.
- **Use When**: You want to ensure consistent object creation across multiple variants (e.g., LightThemeButton + LightThemeInput).

<img src="/uploads/2008/07/abstract-factory-pattern.png" alt="UML Diagram of Abstract Factory" class="creational-pattern-img">

```java
interface GUIFactory {
    Button createButton();
    Checkbox createCheckbox();
}
```

### Builder

Separates the construction of a complex object from its representation.

- **Intent**: Construct objects step-by-step using the same process, with different representations.
- **Use When**: You need to create objects with many configuration options or steps.

<img src="/uploads/2008/07/builder-pattern.png" alt="UML Diagram of Builder" class="creational-pattern-img">

```java
class CarBuilder {
    CarBuilder setSeats(int count);
    CarBuilder setEngine(Engine engine);
    Car build();
}
```

### Prototype

Clones existing objects instead of creating new ones from scratch.

- **Intent**: Specify the kinds of objects to create using a prototypical instance and clone it.
- **Use When**: Instantiation is costly, or object configuration is complex.

<img src="/uploads/2008/07/prototype-pattern.png" alt="UML Diagram of Prototype" class="creational-pattern-img">

```java
abstract class Shape {
    public Shape clone() {
        return (Shape) this.clone();
    }
}
```

### Singleton

Ensures only one instance of a class exists and provides global access to it.

- **Intent**: Control instantiation and provide one shared object.
- **Use With Caution**: It introduces global state and can hinder testability.

<img src="/uploads/2008/07/singleton-pattern.png" alt="UML Diagram of Singleton" class="creational-pattern-img">

```java
class Config {
    private static Config instance;
    private Config() {}

    public static Config getInstance() {
        if (instance == null) {
            instance = new Config();
        }
        return instance;
    }
}
```

## Comparison Table

| Pattern          | Responsibility                     | Best For                               |
| ---------------- | ---------------------------------- | -------------------------------------- |
| Factory Method   | Delegates creation to subclasses   | Frameworks, plugin systems             |
| Abstract Factory | Group creation of related products | Themed UI kits, database connectors    |
| Builder          | Step-by-step construction          | Complex configuration, fluent APIs     |
| Prototype        | Clone existing instance            | Performance optimization, object trees |
| Singleton        | Unique shared instance             | Logging, configuration, caches         |

## Final Thoughts

Creational patterns shape the **starting point** of any object in your system.
They may look simple, but they determine how flexible, testable, and reusable your entire architecture will be.

Next up, we'll explore **Structural Patterns** — and how to compose objects into larger systems cleanly.

---

### **Series Navigation**

- **Introduction**: [Analysis Patterns](../2008-07-01-padroes-de-analise/)
- **Previous**: [Part 1 - Design Patterns Overview](../2008-07-02-padroes-de-projeto-detalhado/)
- **Current**: Part 2 - Creational Patterns
- **Next**: [Part 3 - Structural Patterns](../2008-07-06-padroes-estruturais/)
- **Complete series**: [Analysis Patterns](../2008-07-01-padroes-de-analise/) | [Design Patterns Overview](../2008-07-02-padroes-de-projeto-detalhado/) | [Structural Patterns](../2008-07-06-padroes-estruturais/) | [Behavioral Patterns](../2008-07-08-padroes-comportamentais/)
