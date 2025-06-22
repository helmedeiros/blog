---
title: "Structural Design Patterns: Composing Objects with Purpose"
author: helio
layout: post
date: 2008-07-06 03:27:57+00:00
categories:
  - Architecture
  - Technology
series: Design Patterns and Analysis
subtitle: "Build elegant system architectures through composition—master Adapter, Bridge, Decorator, and Facade patterns that solve the complex challenge of connecting incompatible components into cohesive, maintainable systems"
---

> **Series: Design Patterns and Analysis** | **Part 3 of 4** > _Developed during Master's in Web Systems Projects_

**Continuing our series**, after exploring how to build objects with flexibility using [Creational Patterns](../2008-07-04-padroes-de-criacao/), it's time to understand how to structure them for better collaboration.
**Structural Design Patterns** focus on **how classes and objects are combined** to form larger structures — without unnecessary complexity or tight coupling.

## What Are Structural Patterns?

Structural patterns describe ways to **compose objects and classes into larger systems**, ensuring that changes in one part do not ripple destructively through the codebase.

They help with:

- Adapting interfaces that weren't designed to work together
- Adding responsibilities dynamically
- Hiding internal complexity behind simpler interfaces

## Types of Structural Patterns

### Adapter

Converts the interface of a class into another expected by the client.

- **Intent**: Bridge between incompatible interfaces.
- **Use When**: You want to reuse an existing class but its interface doesn't match.

<img src="/uploads/2008/07/adapter-pattern.png" alt="UML Diagram of Adapter" class="structural-pattern-img">

```java
class RoundHole {
    boolean fits(RoundPeg peg) { ... }
}

class SquarePegAdapter extends RoundPeg {
    private SquarePeg peg;
    double getRadius() { ... } // converts square to round logic
}
```

### Bridge

Decouples an abstraction from its implementation so they can evolve independently.

- **Intent**: Split logic into abstraction and implementation layers.
- **Use When**: You want to vary both abstractions and implementations.

<img src="/uploads/2008/07/bridge-pattern.png" alt="UML Diagram of Bridge" class="structural-pattern-img">

```java
interface Device {
    void enable();
    void disable();
}

class Remote {
    protected Device device;
    public void togglePower() {
        if (device.isEnabled()) device.disable();
        else device.enable();
    }
}
```

### Composite

Composes objects into tree structures and treats them uniformly.

- **Intent**: Treat individual objects and compositions the same way.
- **Use When**: You work with recursive structures like UI trees or file systems.

<img src="/uploads/2008/07/composite-pattern.png" alt="UML Diagram of Composite" class="structural-pattern-img">

```java
interface Graphic {
    void draw();
}

class CompoundGraphic implements Graphic {
    private List<Graphic> children;
    void draw() {
        for (Graphic child : children) child.draw();
    }
}
```

### Decorator

Adds responsibilities to objects dynamically.

- **Intent**: Wrap an object to extend its behavior.
- **Use When**: You want to avoid subclass explosion and keep things flexible.

<img src="/uploads/2008/07/decorator-pattern.png" alt="UML Diagram of Decorator" class="structural-pattern-img">

```java
interface DataSource {
    void writeData(String data);
}

class CompressionDecorator implements DataSource {
    private DataSource wrappee;
    void writeData(String data) {
        wrappee.writeData(compress(data));
    }
}
```

### Facade

Provides a simplified interface to a complex subsystem.

- **Intent**: Hide complexity and expose only what's necessary.
- **Use When**: You need a clean API over complex internals.

<img src="/uploads/2008/07/facade-pattern.png" alt="UML Diagram of Facade" class="structural-pattern-img">

```java
class VideoConverter {
    public File convert(String filename, String format) {
        // interacts with many video-related classes internally
    }
}
```

### Flyweight

Shares common parts of state across many objects to save memory.

- **Intent**: Use sharing to support large numbers of fine-grained objects efficiently.
- **Use When**: You need to manage many objects with similar data (e.g., game tiles, fonts).

<img src="/uploads/2008/07/flyweight-pattern.png" alt="UML Diagram of Flyweight" class="structural-pattern-img">

```java
class TreeType {
    String texture;
    void draw(int x, int y) { ... }
}
```

### Proxy

Acts as a placeholder for another object to control access, lazy load, or log.

- **Intent**: Control access to an object.
- **Use When**: You need extra logic around the real object without changing it.

<img src="/uploads/2008/07/proxy-pattern.png" alt="UML Diagram of Proxy" class="structural-pattern-img">

```java
class ImageProxy implements Image {
    private RealImage realImage;
    void display() {
        if (realImage == null) realImage = new RealImage();
        realImage.display();
    }
}
```

## Comparison Table

| Pattern   | Purpose                                  | Best For                             |
| --------- | ---------------------------------------- | ------------------------------------ |
| Adapter   | Interface conversion                     | Legacy code, integration             |
| Bridge    | Separate abstraction from implementation | UI frameworks, device control        |
| Composite | Recursive tree structure                 | Graphics, UIs, folders               |
| Decorator | Add behavior without subclassing         | I/O streams, logging                 |
| Facade    | Simplify subsystem usage                 | API gateways, libraries              |
| Flyweight | Share objects for memory efficiency      | Rendering engines, games             |
| Proxy     | Access control                           | Virtual proxies, protection, caching |

## Final Thoughts

Structural patterns help us **compose systems with elegance**, enabling adaptation, extension, and simplification of architecture without creating a domino effect of changes.

Next up, we'll explore **Behavioral Patterns** — how to coordinate responsibilities and workflows flexibly.

---

### **Series Navigation**

- **Introduction**: [Analysis Patterns](../2008-07-01-padroes-de-analise/)
- **Previous**: [Part 2 - Creational Patterns](../2008-07-04-padroes-de-criacao/)
- **Current**: Part 3 - Structural Patterns
- **Next**: [Part 4 - Behavioral Patterns](../2008-07-08-padroes-comportamentais/)
- **Complete series**: [Analysis Patterns](../2008-07-01-padroes-de-analise/) | [Design Patterns Overview](../2008-07-02-padroes-de-projeto-detalhado/) | [Creational Patterns](../2008-07-04-padroes-de-criacao/) | [Behavioral Patterns](../2008-07-08-padroes-comportamentais/)
