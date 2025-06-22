---
title: "Padrões de Criação: Construindo Objetos com Flexibilidade"
author: helio
layout: post
date: 2008-07-04 03:27:57+00:00
categories: ["Architecture"]

subtitle: "Domine a arte da criação flexível de objetos—descubra como padrões Factory, Builder, Singleton e Prototype resolvem o desafio fundamental de construir objetos desacoplados, testáveis e adaptáveis à mudança"
---

> **Série: Padrões de Projeto e Análise** | **Parte 2 de 4** > _Desenvolvido durante o Mestrado em Projetos de Sistemas Web_

**Continuando nossa série**, após entender a [importância dos padrões de projeto](../2008-07-02-padroes-de-projeto-detalhado/), agora exploramos a primeira categoria específica. Os padrões de criação resolvem um dos problemas mais fundamentais do design orientado a objetos.

Os padrões de criação resolvem um dos problemas mais fundamentais do design orientado a objetos:
**Como criamos objetos de forma flexível, desacoplada e testável?**

Neste post, vamos explorar com mais profundidade a primeira categoria dos padrões de projeto — os **Padrões de Criação** — e entender suas ideias centrais, estruturas e quando aplicá-los em sistemas reais.

## O Que São Padrões de Criação?

Esses padrões **encapsulam o processo de criação de objetos**, escondendo as complexidades da instanciação e tornando o código mais flexível para mudanças.

Eles ajudam a evitar:

- Uso excessivo de `new` espalhado pelo código
- Alto acoplamento com classes concretas
- Problemas na configuração e duplicação de objetos

## Tipos de Padrões de Criação

### Factory Method

Cria objetos por meio de uma interface de fábrica em vez de instanciar diretamente com `new`.

- **Intenção**: Definir uma interface para criação de objetos, deixando que subclasses decidam qual classe instanciar.
- **Use quando**: Deseja delegar a criação para subclasses.

<img src="/uploads/2008/07/factory-method-pattern.png" alt="Diagrama UML do Factory Method" class="creational-pattern-img">

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

Agrupa diversas fábricas relacionadas em uma única interface.

- **Intenção**: Fornecer uma interface para criar famílias de objetos relacionados sem especificar suas classes concretas.
- **Use quando**: Precisa garantir consistência na criação de objetos em diferentes variações (ex: temas de interface).

<img src="/uploads/2008/07/abstract-factory-pattern.png" alt="Diagrama UML do Abstract Factory" class="creational-pattern-img">

```java
interface GUIFactory {
    Button createButton();
    Checkbox createCheckbox();
}
```

### Builder

Separa a construção de um objeto complexo da sua representação.

- **Intenção**: Construir objetos passo a passo, com o mesmo processo mas diferentes representações.
- **Use quando**: O objeto tem muitos parâmetros ou etapas de montagem.

<img src="/uploads/2008/07/builder-pattern.png" alt="Diagrama UML do Builder" class="creational-pattern-img">

```java
class CarBuilder {
    CarBuilder setSeats(int count);
    CarBuilder setEngine(Engine engine);
    Car build();
}
```

### Prototype

Clona objetos existentes em vez de criar novos do zero.

- **Intenção**: Usar uma instância prototípica como base para novas cópias.
- **Use quando**: A criação é cara ou a configuração do objeto é complexa.

<img src="/uploads/2008/07/prototype-pattern.png" alt="Diagrama UML do Prototype" class="creational-pattern-img">

```java
abstract class Shape {
    public Shape clone() {
        return (Shape) this.clone();
    }
}
```

### Singleton

Garante que apenas uma instância da classe exista e fornece acesso global a ela.

- **Intenção**: Controlar a instanciação e garantir que só exista um objeto da classe.
- **Use com cuidado**: Pode introduzir estado global e dificultar testes.

<img src="/uploads/2008/07/singleton-pattern.png" alt="Diagrama UML do Singleton" class="creational-pattern-img">

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

## Tabela Comparativa

| Padrão           | Responsabilidade              | Melhor Uso                             |
| ---------------- | ----------------------------- | -------------------------------------- |
| Factory Method   | Delegar criação às subclasses | Frameworks, sistemas de plugins        |
| Abstract Factory | Criar famílias de produtos    | Temas de UI, conectores de banco       |
| Builder          | Construção passo a passo      | Configurações complexas, APIs fluentes |
| Prototype        | Clonar instâncias existentes  | Otimização, árvores de objetos         |
| Singleton        | Garantir uma instância única  | Logs, configurações, cache             |

## Considerações Finais

Os padrões de criação moldam o **ponto de partida** de qualquer objeto no sistema.
Eles parecem simples, mas influenciam diretamente a flexibilidade, testabilidade e reutilização da arquitetura.

No próximo post, vamos explorar os **Padrões Estruturais** — como compor objetos em estruturas maiores com clareza.

---

### **Navegação da Série**

- **Introdução**: [Padrões de Análise](../2008-07-01-padroes-de-analise/)
- **Anterior**: [Parte 1 - Padrões de Projeto Overview](../2008-07-02-padroes-de-projeto-detalhado/)
- **Atual**: Parte 2 - Padrões de Criação
- **Próximo**: [Parte 3 - Padrões Estruturais](../2008-07-06-padroes-estruturais/)
- **Série completa**: [Padrões de Análise](../2008-07-01-padroes-de-analise/) | [Padrões de Projeto Overview](../2008-07-02-padroes-de-projeto-detalhado/) | [Padrões Estruturais](../2008-07-06-padroes-estruturais/) | [Padrões Comportamentais](../2008-07-08-padroes-comportamentais/)
