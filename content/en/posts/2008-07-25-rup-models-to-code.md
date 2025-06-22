---
title: "From Models to Code: RUP and Layered Architectures"
author: helio
layout: post
date: 2008-07-25 08:00:00+00:00
categories:
  - Architecture

subtitle: Bridge the gap between models and working code—discover how RUP's model-to-code transformation process turns abstract UML diagrams into concrete, maintainable software architecture
---

Most modeling efforts fail because they get stuck in abstraction.
Diagrams pile up. Documentation gets stale. No one connects them to code.

But that's not what RUP was built for.

Rational Unified Process encourages modeling to _support development_, not replace it. If used right, it maps cleanly to a **layered architecture** and helps teams make better design decisions without getting lost in theory.

Let's explore how RUP's models align with the code we actually write.

---

## From Analysis Model to Domain Layer

The **Analysis Model** captures system responsibilities from a business perspective. It defines what the system does, using use-case realizations and conceptual classes.

### Mapping to Code

| Analysis Element       | Code Equivalent               |
| ---------------------- | ----------------------------- |
| Entity (business noun) | Domain object / entity class  |
| Boundary               | Controller / API endpoint     |
| Control                | Application service / handler |
| Association            | Field or reference            |
| Inheritance            | Polymorphism in model objects |

### Example

A `Purchase` use case realization may involve:

- `User` (Entity)
- `CheckoutController` (Boundary)
- `PurchaseService` (Control)

These map cleanly to a domain-driven design structure.

---

## From Design Model to Services and Adapters

While the analysis model defines **what**, the **Design Model** clarifies **how**.

It introduces concrete classes, interaction logic, and technology choices—bridging the gap from concept to code.

### Mapping to Layers

- **Control classes** → Service layer
- **Boundary classes** → Controllers, APIs, Views
- **Entity classes** → Domain and persistence models
- **Design patterns** → Factories, Builders, Adapters applied here

### Diagram

{{< plantuml title="Purchase Service Interaction" >}}
@startuml
actor User
boundary CheckoutController
control PurchaseService
entity Cart

User --> CheckoutController : initiateCheckout()
CheckoutController --> PurchaseService : process(cart)
PurchaseService --> Cart : calculateTotal()
@enduml
{{< /plantuml >}}

This simple sequence diagram can directly inform class structure and service wiring.

---

## From Component Model to Deployment Pipelines

The **Component Model** describes how pieces of the system are packaged and deployed. Think of it as your **delivery blueprint**.

- Each component can map to:
  - a microservice
  - a module
  - a shared library

When defined early, this model informs CI/CD structure, artifact boundaries, and test ownership.

### Example

{{< plantuml title="Component Architecture" >}}
@startuml
package "Customer Management" {
[CustomerService] --> [UserRepository]
[CustomerService] --> [PaymentGatewayAdapter]
}

package "Order Management" {
[OrderService] --> [OrderRepository]
}

[CustomerService] ..> [OrderService] : calls
@enduml
{{< /plantuml >}}

Each package above might align with:

- a Maven module
- a deployable service
- a Git repo

---

## Real-World Flow: From Use Case to Code

Let's say you start with a use case: **Cancel Booking**

### Step 1: Use Case Diagram

Define actor → use case interaction.

{{< plantuml title="Cancel Booking Use Case" >}}
@startuml
actor Traveler
usecase "Cancel Booking" as UC1
Traveler --> UC1
@enduml
{{< /plantuml >}}

### Step 2: Sequence Diagram

{{< plantuml title="Cancel Booking Sequence" >}}
@startuml
actor Traveler
boundary BookingController
control BookingService
entity Booking

Traveler --> BookingController : cancel(bookingId)
BookingController --> BookingService : cancel(bookingId)
BookingService --> Booking : markAsCancelled()
@enduml
{{< /plantuml >}}

### Step 3: Code Skeleton

```java
@RestController
public class BookingController {
    @PostMapping("/cancel")
    public ResponseEntity<?> cancel(@RequestBody CancelRequest request) {
        bookingService.cancel(request.getBookingId());
        return ResponseEntity.ok().build();
    }
}

@Service
public class BookingService {
    public void cancel(String bookingId) {
        Booking booking = bookingRepository.findById(bookingId);
        booking.markAsCancelled();
        bookingRepository.save(booking);
    }
}
```

---

## Final Thoughts

RUP was never about diagrams for their own sake. When used with discipline, RUP's models become **tools for thinking**, not artifacts for compliance.

By aligning Analysis Models with the domain layer, Design Models with your services and adapters, and Component Models with your delivery structure, you get a **consistent map from idea to production**.

Modeling doesn't slow you down—_disconnect does_.
