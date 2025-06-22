---
title: "Do Modelo ao Código: RUP e Arquiteturas em Camadas"
author: helio
layout: post
date: 2008-07-25 08:00:00+00:00
categories: ["Architecture"]

subtitle: Construa a ponte entre modelos e código funcionando—descubra como o processo de transformação modelo-para-código do RUP transforma diagramas UML abstratos em arquitetura de software concreta e mantível
---

A maioria dos esforços de modelagem falha porque ficam presos na abstração.
Diagramas se acumulam. A documentação envelhece. E ninguém conecta isso ao código real.

Mas essa não é a proposta original do RUP.

O Rational Unified Process incentiva a modelagem para _apoiar o desenvolvimento_, não para substituí-lo. Quando bem aplicado, ele se encaixa perfeitamente com uma **arquitetura em camadas** e ajuda times a tomarem melhores decisões de design, sem se perderem na teoria.

Vamos explorar como os modelos do RUP se alinham ao código que realmente escrevemos.

---

## Do Modelo de Análise para a Camada de Domínio

O **Modelo de Análise** captura responsabilidades do sistema sob a ótica de negócio. Ele define o que o sistema faz, usando realizações de casos de uso e classes conceituais.

### Mapeamento para o Código

| Elemento de Análise               | Equivalente no Código             |
| --------------------------------- | --------------------------------- |
| Entidade (substantivo de negócio) | Classe de domínio / entidade      |
| Fronteira                         | Controlador / endpoint de API     |
| Controle                          | Serviço de aplicação / handler    |
| Associação                        | Campo ou referência               |
| Herança                           | Polimorfismo em objetos de modelo |

### Exemplo

Uma realização de caso de uso `Compra` pode envolver:

- `Usuario` (Entidade)
- `CheckoutController` (Fronteira)
- `CompraService` (Controle)

Esses elementos se encaixam em uma estrutura orientada ao domínio.

---

## Do Modelo de Design para Serviços e Adaptadores

Enquanto o modelo de análise define o **o quê**, o **Modelo de Design** esclarece o **como**.

Ele introduz classes concretas, lógica de interação e escolhas tecnológicas — fazendo a ponte entre o conceito e a implementação.

### Mapeamento para Camadas

- **Classes de controle** → Camada de serviço
- **Classes de fronteira** → Controllers, APIs, Views
- **Classes de entidade** → Modelos de domínio e persistência
- **Padrões de projeto** → Fábricas, Builders, Adaptadores

### Diagrama

{{< plantuml title="Interação do Serviço de Compra" >}}
@startuml
actor Usuario
boundary CheckoutController
control CompraService
entity Carrinho

Usuario --> CheckoutController : iniciarCheckout()
CheckoutController --> CompraService : processar(carrinho)
CompraService --> Carrinho : calcularTotal()
@enduml
{{< /plantuml >}}

Esse diagrama de sequência pode orientar diretamente a estrutura de classes e serviços.

---

## Do Modelo de Componentes para os Pipelines de Deploy

O **Modelo de Componentes** descreve como as partes do sistema são empacotadas e implantadas. Pense nisso como seu **mapa de entrega**.

Cada componente pode representar:

- um microsserviço
- um módulo
- uma biblioteca compartilhada

Quando definido cedo, esse modelo orienta CI/CD, fronteiras de artefatos e a responsabilidade pelos testes.

### Exemplo

{{< plantuml title="Arquitetura de Componentes" >}}
@startuml
package "Gestão de Clientes" {
[ClienteService] --> [UsuarioRepository]
[ClienteService] --> [PagamentoAdapter]
}

package "Gestão de Pedidos" {
[PedidoService] --> [PedidoRepository]
}

[ClienteService] ..> [PedidoService] : chama
@enduml
{{< /plantuml >}}

Cada pacote pode corresponder a:

- um módulo Maven
- um serviço implantável
- um repositório Git

---

## Do Caso de Uso ao Código: Um Fluxo Real

Vamos começar com um caso de uso: **Cancelar Reserva**

### Passo 1: Diagrama de Caso de Uso

{{< plantuml title="Caso de Uso Cancelar Reserva" >}}
@startuml
actor Passageiro
usecase "Cancelar Reserva" as UC1
Passageiro --> UC1
@enduml
{{< /plantuml >}}

### Passo 2: Diagrama de Sequência

{{< plantuml title="Sequência Cancelar Reserva" >}}
@startuml
actor Passageiro
boundary ReservaController
control ReservaService
entity Reserva

Passageiro --> ReservaController : cancelar(reservaId)
ReservaController --> ReservaService : cancelar(reservaId)
ReservaService --> Reserva : marcarComoCancelada()
@enduml
{{< /plantuml >}}

### Passo 3: Esqueleto de Código

```java
@RestController
public class ReservaController {
    @PostMapping("/cancelar")
    public ResponseEntity<?> cancelar(@RequestBody CancelarRequest request) {
        reservaService.cancelar(request.getReservaId());
        return ResponseEntity.ok().build();
    }
}

@Service
public class ReservaService {
    public void cancelar(String reservaId) {
        Reserva reserva = reservaRepository.findById(reservaId);
        reserva.marcarComoCancelada();
        reservaRepository.save(reserva);
    }
}
```

---

## Considerações Finais

O RUP nunca foi sobre diagramas por obrigação. Quando usado com disciplina, seus modelos se tornam **ferramentas para pensar**, não burocracia.

Ao alinhar o Modelo de Análise com sua camada de domínio, o Modelo de Design com serviços e adaptadores, e o Modelo de Componentes com a estrutura de entrega, você obtém um **mapa coerente do conceito até a produção**.

Modelar não te atrasa — o que atrasa é a falta de conexão entre visão e execução.
