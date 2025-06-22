---
title: "Padrões Estruturais: Compondo Objetos com Propósito"
author: helio
layout: post
date: 2008-07-06 03:27:57+00:00
categories:
  - Architecture

subtitle: "Construa arquiteturas de sistema elegantes através de composição—domine padrões Adapter, Bridge, Decorator e Facade que resolvem o desafio complexo de conectar componentes incompatíveis em sistemas coesos e mantíveis"
---

> **Série: Padrões de Projeto e Análise** | **Parte 3 de 4** > _Desenvolvido durante o Mestrado em Projetos de Sistemas Web_

**Continuando nossa série**, depois de entender como criar objetos com flexibilidade usando os [Padrões de Criação](../2008-07-04-padroes-de-criacao/), é hora de estruturar esses objetos de forma colaborativa e escalável.
Os **Padrões Estruturais** se concentram em **como as classes e objetos são combinados** para formar estruturas maiores — sem acoplamento desnecessário ou complexidade excessiva.

## O Que São Padrões Estruturais?

Padrões estruturais descrevem formas de **compor objetos e classes em sistemas maiores**, garantindo que mudanças em uma parte não causem efeitos colaterais destrutivos no restante do código.

Eles ajudam a:

- Adaptar interfaces que não foram projetadas para funcionar juntas
- Adicionar responsabilidades dinamicamente
- Esconder complexidade interna por trás de interfaces simples

## Tipos de Padrões Estruturais

### Adapter (Adaptador)

Converte a interface de uma classe em outra esperada pelo cliente.

- **Intenção**: Fazer ponte entre interfaces incompatíveis.
- **Use quando**: Você quer reutilizar uma classe existente, mas sua interface não é compatível.

<img src="/uploads/2008/07/adapter-pattern.png" alt="Diagrama UML do Adapter" class="structural-pattern-img">

```java
class RoundHole {
    boolean fits(RoundPeg peg) { ... }
}

class SquarePegAdapter extends RoundPeg {
    private SquarePeg peg;
    double getRadius() { ... }
}
```

### Bridge (Ponte)

Desacopla uma abstração de sua implementação para que ambos possam evoluir separadamente.

- **Intenção**: Separar lógica em camadas de abstração e implementação.
- **Use quando**: Deseja variar tanto abstrações quanto implementações.

<img src="/uploads/2008/07/bridge-pattern.png" alt="Diagrama UML do Bridge" class="structural-pattern-img">

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

### Composite (Composto)

Compõe objetos em estruturas de árvore e os trata de forma uniforme.

- **Intenção**: Tratar objetos individuais e composições da mesma forma.
- **Use quando**: Você lida com estruturas recursivas como árvores de UI ou sistemas de arquivos.

<img src="/uploads/2008/07/composite-pattern.png" alt="Diagrama UML do Composite" class="structural-pattern-img">

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

### Decorator (Decorador)

Adiciona responsabilidades a objetos dinamicamente.

- **Intenção**: Envolver um objeto para estender seu comportamento.
- **Use quando**: Deseja evitar herança excessiva e manter flexibilidade.

<img src="/uploads/2008/07/decorator-pattern.png" alt="Diagrama UML do Decorator" class="structural-pattern-img">

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

### Facade (Fachada)

Fornece uma interface simplificada para um subsistema complexo.

- **Intenção**: Esconder a complexidade e expor apenas o necessário.
- **Use quando**: Precisa de uma API limpa sobre uma lógica interna complexa.

<img src="/uploads/2008/07/facade-pattern.png" alt="Diagrama UML do Facade" class="structural-pattern-img">

```java
class VideoConverter {
    public File convert(String filename, String format) {
        // interage com várias classes internas de vídeo
    }
}
```

### Flyweight (Peso-Mosca)

Compartilha partes comuns de estado entre muitos objetos para economizar memória.

- **Intenção**: Compartilhar dados para suportar grandes quantidades de objetos com eficiência.
- **Use quando**: Há muitos objetos com dados similares (ex: peças de jogo, fontes).

<img src="/uploads/2008/07/flyweight-pattern.png" alt="Diagrama UML do Flyweight" class="structural-pattern-img">

```java
class TreeType {
    String texture;
    void draw(int x, int y) { ... }
}
```

### Proxy

Serve como substituto de outro objeto para controlar acesso, fazer carregamento tardio ou registrar atividades.

- **Intenção**: Controlar o acesso a um objeto.
- **Use quando**: Precisa de lógica adicional sem alterar o objeto real.

<img src="/uploads/2008/07/proxy-pattern.png" alt="Diagrama UML do Proxy" class="structural-pattern-img">

```java
class ImageProxy implements Image {
    private RealImage realImage;
    void display() {
        if (realImage == null) realImage = new RealImage();
        realImage.display();
    }
}
```

## Tabela Comparativa

| Padrão    | Propósito                             | Melhor Uso                                 |
| --------- | ------------------------------------- | ------------------------------------------ |
| Adapter   | Conversão de interface                | Integração com código legado               |
| Bridge    | Separar abstração da implementação    | UI modular, controle de dispositivos       |
| Composite | Estrutura recursiva em árvore         | Gráficos, interfaces, sistemas de arquivos |
| Decorator | Adicionar comportamento dinamicamente | Streams, logging, compressão               |
| Facade    | Simplificar uso de subsistemas        | APIs externas, bibliotecas internas        |
| Flyweight | Compartilhamento eficiente de objetos | Renderização, jogos                        |
| Proxy     | Controle de acesso                    | Lazy load, cache, segurança                |

## Considerações Finais

Os padrões estruturais nos ajudam a **compor sistemas com elegância**, permitindo adaptar, estender e simplificar a arquitetura sem criar um efeito dominó de mudanças.

No próximo post, vamos explorar os **Padrões Comportamentais** — como coordenar responsabilidades e fluxos de trabalho de maneira flexível.

---

### **Navegação da Série**

- **Introdução**: [Padrões de Análise](../2008-07-01-padroes-de-analise/)
- **Anterior**: [Parte 2 - Padrões de Criação](../2008-07-04-padroes-de-criacao/)
- **Atual**: Parte 3 - Padrões Estruturais
- **Próximo**: [Parte 4 - Padrões Comportamentais](../2008-07-08-padroes-comportamentais/)
- **Série completa**: [Padrões de Análise](../2008-07-01-padroes-de-analise/) | [Padrões de Projeto Overview](../2008-07-02-padroes-de-projeto-detalhado/) | [Padrões de Criação](../2008-07-04-padroes-de-criacao/) | [Padrões Comportamentais](../2008-07-08-padroes-comportamentais/)
