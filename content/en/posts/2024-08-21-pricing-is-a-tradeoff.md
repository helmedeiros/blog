---
title: "Pricing Is a Tradeoff"
categories:
  - Engineering
  - Experimentation
  - Pricing
  - Product
date: 2024-08-21
tags:
  - pricing
  - optimization
  - decision-making
  - monetization
  - experimentation
  - product-strategy
description: "Why the hardest pricing question isn't what should we charge — it's what are we willing to sacrifice?"
subtitle: "Pricing isn't the art of finding the highest price. It's the discipline of choosing which tradeoffs matter."
---

For a few years I was working on a pricing platform — the part of the system that decides what to charge a customer, and when. By the time I sat down to write this, the platform had already gone through several reframings. We had moved rules out of code into a business rules engine. We had stopped shipping pricing changes blind and started treating them as experiments. We had stopped pretending the "average customer" was a useful concept. And we had learned that different customer groups responded to price along curves, not points.

For a long time, underneath all of that, I still thought pricing was a search problem. Find the right price. Apply it. Measure the outcome. Move on.

Each lesson chipped away at that belief. Pricing rules were hypotheses. Customers weren't averages. Responses formed curves. Eventually a different realisation emerged.

The hardest pricing question wasn't *what should we charge?*

It was *what are we trying to optimise?*

That question changed how I thought about pricing. Because every pricing decision is a tradeoff.

## The easy optimisation

Imagine your only objective is revenue.

The problem appears straightforward. Raise prices. Earn more per booking. Celebrate.

Reality is less cooperative. Customers react. Demand changes. Competitors exist. Trust matters.

What looks like an optimisation problem quickly becomes a balancing act. The mistake is assuming there is a single number waiting to be discovered. There usually isn't. There are multiple outcomes moving in different directions.

## Revenue versus conversion

This is the first tradeoff most pricing teams encounter.

A higher price often means more revenue per transaction. At the same time, it may reduce conversion.

{{< plantuml title="The first tradeoff: revenue per booking against booking rate" >}}
@startuml
skinparam shadowing false
start
:Higher price;
:Higher revenue per booking;
:Lower booking rate;
stop
@enduml
{{< /plantuml >}}

The difficult question isn't whether conversion drops. The difficult question is whether the additional revenue compensates for that drop.

And even that is often too simplistic. Because conversion is rarely the only thing we care about.

## Revenue versus trust

One lesson that surprised me was how often customer trust appeared in pricing discussions.

Engineers like measurable metrics. Trust isn't always easy to measure. But customers feel it immediately. A fee that appears unexpectedly. A pricing rule that feels unfair. A sudden increase that customers can't explain.

These things affect behaviour. Not always today. Sometimes months later.

Trust behaves like a long-term asset. Revenue behaves like a short-term signal. Good pricing systems need to consider both.

## Revenue versus retention

A close cousin of the trust tradeoff is retention. They are related, but they show up in the data differently.

Trust is about how a customer feels. Retention is about whether they come back.

A pricing change can win the booking and lose the customer. The first transaction looks healthy. Average order value goes up. The dashboard tells a clean story. Then, six months later, the cohort that experienced the change books less often than the cohort that didn't — and nobody was watching that signal when the change shipped.

Revenue happens at the moment of the sale. Retention happens between sales. The two metrics live on completely different timescales, which makes them easy to weigh unevenly. Short-term revenue gets the spotlight. Long-term retention pays the bill.

Good pricing systems learn to wait — and to keep measuring after the win.

## Revenue versus simplicity

As pricing capabilities evolve, another tradeoff appears.

Complex strategies often outperform simple ones. At least in theory. A more sophisticated model can capture more signals, more context, more nuance.

But complexity creates costs. Can engineers explain the result? Can product managers understand the reasoning? Can analysts validate the outcome? Can stakeholders trust the recommendation?

Sometimes a slightly worse but understandable solution creates more value than a better solution nobody understands.

## Every objective produces a different answer

One exercise I found useful was asking the same question with different objectives.

Suppose we have a pricing decision. Depending on what we're optimising for, the same situation can produce very different answers:

| Objective | Likely answer |
| --- | --- |
| Maximise revenue | Push price upward where the curve tolerates it |
| Maximise conversion | Hold price down, even at the cost of margin |
| Maximise long-term customer value | Sacrifice some short-term revenue to keep trust and retention |

The price itself doesn't determine success. The objective does.

Pricing teams often spend too much time discussing numbers and too little time discussing objectives.

## The tradeoff hidden inside every experiment

A pattern I kept seeing in pricing experiments: one variant would increase revenue while another would improve conversion.

The interesting part was never the experiment. The interesting part was the conversation afterwards.

*Which result should we prefer?*

There is no universally correct answer. The answer depends on context. A company trying to grow market share may optimise differently from a company trying to improve profitability. A new product may optimise differently from a mature one. The same experiment can produce different decisions depending on the business objective.

Experiments reveal tradeoffs. They don't remove them.

## Local optimisation versus global optimisation

Another lesson took me longer to learn.

Improving one part of a system does not necessarily improve the whole system.

Imagine a customer segment that tolerates higher prices. Optimising that segment might increase revenue. But what if the change affects customer perception elsewhere? What if it creates operational complexity? What if it makes future experimentation harder?

Local improvements can create global costs. Pricing decisions exist inside larger systems. The best decision for one metric isn't always the best decision for the business.

## Constraints are not limitations

Engineers often treat constraints as obstacles.

Pricing taught me to see them differently. Constraints are what make optimisation meaningful.

Without constraints, the answer is usually trivial:

> Maximise revenue → raise prices.

Constraints force better questions:

> Maximise revenue, while maintaining conversion, while protecting trust, while remaining explainable, while supporting future experiments.

Now the problem becomes interesting.

The most valuable pricing conversations I participated in were rarely about numbers. They were about constraints.

## What I learned

The biggest shift in my thinking happened when I stopped viewing pricing as a search for the correct value.

There is rarely a single correct value. There are tradeoffs. Objectives. Constraints. Competing outcomes.

Pricing isn't the art of finding the highest price. It is the discipline of choosing which tradeoffs matter.

That realisation made experimentation more valuable. It made segmentation more useful. And it made customer behaviour more understandable. Because the purpose of all those capabilities was never finding an answer. It was helping us make better decisions.

## Closing reflection

If you walked into a pricing discussion expecting to leave with a number, you usually left disappointed. The number was the easy part. The hard part was naming the constraints that made the number defensible.

The teams that handled pricing tradeoffs best weren't the teams with the best models or the boldest opinions. They were the teams who had practised the conversation. Who had made the same kind of decision often enough that they could disagree about it without making it personal. Who had a shared sense of which sacrifices the company was actually willing to accept, and which ones it only pretended to.

A tradeoff that nobody in the room can name isn't a decision. It's a wish.
