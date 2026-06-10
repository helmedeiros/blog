---
title: "HTTP Caching for APIs: Cache-Control, Validators, and Conditional Requests"
date: 2013-04-26T14:00:00-03:00
author: Helio Medeiros
subtitle: Stop reinventing caching inside your application—the HTTP spec already gave you freshness, validators, conditional requests, and intermediary caches that have been working since 1997 and will outlive your stack
tags:
  [
    "HTTP",
    "caching",
    "REST",
    "performance",
    "architecture",
    "ETag",
    "Cache-Control",
  ]
categories: ["Engineering", "Architecture"]
---

## Why I Gave This Talk

<iframe class="speakerdeck-iframe" frameborder="0" src="https://speakerdeck.com/player/dd3dfd402ba601312b7a2e0cb471b9bd" title="HTTP Caching for APIs" allowfullscreen="true" allow="web-share" style="border: 0px; background: padding-box padding-box rgba(0, 0, 0, 0.1); margin: 0px; padding: 0px; border-radius: 6px; box-shadow: rgba(0, 0, 0, 0.2) 0px 5px 40px; width: 100%; height: auto; aspect-ratio: 560 / 315;" spellcheck="false" data-ratio="1.7777777777777777"></iframe>

When this talk was first put together, the framing was about caching in a particular Java stack. I'm rewriting it here because the part that actually matters — and the part that has aged well — has nothing to do with the framework. It's HTTP.

If you serve resources over HTTP, the spec already gave you a caching system. It was designed in the 90s, it's been refined for thirty years, and it'll keep working long after whatever runtime you're on today is gone. The trick is knowing which headers to send and which conversations they unlock between your server, your clients, and every intermediary cache in between.

## Caching Is a Conversation

The mental model that fixes most caching confusion: a cache is not a feature on your server. A cache is a **negotiated agreement** between the server, the client, and any cache that sits between them.

When the server returns a response, it tells the cache: "here's the data, and here are the rules under which you can hand it back to someone else." When the client (or an intermediary) wants the resource again, it can either trust the rules or come back to check.

Two distinct mechanisms drive that conversation. Mixing them up is where most bugs come from.

## Freshness: How Long the Cache Can Skip the Server

A fresh response can be served from cache without asking the server at all. The server controls this with **`Cache-Control`** directives on the response:

- **`max-age=N`** — the response is fresh for N seconds.
- **`public`** / **`private`** — can shared caches (CDNs, proxies) store it, or only the end user's browser?
- **`no-cache`** — store it, but always revalidate with the server before reusing.
- **`no-store`** — don't store it at all (sensitive data, one-off responses).
- **`must-revalidate`** — once stale, you must revalidate; do not serve stale.

```http
Cache-Control: public, max-age=300, must-revalidate
```

That single header says: "anyone can cache this for five minutes; after that, come back and ask."

Freshness is the fast path. The cache hands the response back with no network round-trip to the origin. The trade-off is the same as any cache: if the underlying data changes within `max-age`, clients see the old version until it expires.

## Validation: Checking Without Re-Downloading

When the response is _stale_ — or when the client just wants to be sure — caches don't have to re-download the full body. They can ask the server "do you have a newer version?" with a **conditional request**. The server answers with either the new body (`200 OK`) or a tiny `304 Not Modified`.

There are two validators the server can send on the original response, and the client echoes one back to check:

**ETag** — an opaque identifier the server computes from the resource (a hash, a version number, anything that changes when the resource changes).

```http
# server -> client
ETag: "a15505b34a"

# client -> server (later)
If-None-Match: "a15505b34a"
```

If the ETag still matches, the server replies `304 Not Modified` with no body. The cache uses what it already has.

**Last-Modified** — a timestamp of when the resource last changed.

```http
# server -> client
Last-Modified: Fri, 26 Apr 2013 14:00:00 GMT

# client -> server (later)
If-Modified-Since: Fri, 26 Apr 2013 14:00:00 GMT
```

Same idea, weaker guarantee (one-second resolution; doesn't distinguish edits inside the same second).

Use ETags when you can compute one cheaply. Use `Last-Modified` when you already have a timestamp and don't want to compute a hash. Use both if you have both — clients will pick.

## Putting Them Together

Freshness and validation aren't either-or. They work as a pipeline.

1. Client asks for a resource.
2. Server returns body + `Cache-Control: max-age=300` + `ETag`.
3. For the next 5 minutes, caches serve the stored body directly — no server contact.
4. After 5 minutes, the next request triggers a **conditional GET** with `If-None-Match: <etag>`.
5. If nothing changed, the server returns `304 Not Modified` (tiny). Cache resets its freshness window.
6. If something changed, the server returns `200 OK` with a new body and a new `ETag`.

Most of the traffic stays in step 3. The rest is cheap.

## The Header That Saves You: `Vary`

Caches key responses by URL. Two clients hitting the same URL get the same cached body — unless the response varies by request header. Say your API serves the same `/account` URL in JSON and XML based on `Accept`, or in English and Portuguese based on `Accept-Language`. Without telling the cache about it, the first response gets stored and served to everyone, in the wrong format.

```http
Vary: Accept, Accept-Language
```

This tells the cache: "store separate copies keyed by these request headers." Skipping `Vary` is one of the most common subtle caching bugs in APIs.

## What Not to Cache

A few responses you should explicitly mark uncacheable, even when caching feels "fine":

- Authenticated user data, unless you're sure `Cache-Control: private` is enough and your auth setup never lets a shared cache see it.
- Anything with one-shot side effects (tokens, OTPs, signed URLs that expire).
- Error responses you don't want stuck (`Cache-Control: no-store` on 500s is usually right).
- Anything where the cost of stale data is higher than the cost of a round trip.

When in doubt: `Cache-Control: no-store`. It's a small performance loss and a real correctness win.

## What This Buys You

Three concrete things, all of which compound over time:

**Bandwidth.** Conditional GETs send headers and not bodies. For a heavy resource served at scale, that's a multiple-order-of-magnitude reduction.

**Latency.** Freshness lets caches respond locally. A cached response from the user's ISP is two orders of magnitude faster than your origin server.

**Capacity.** Every request a cache absorbs is a request your origin doesn't have to serve. The cheapest way to scale an API is to need less of it.

## What I'd Stress to Anyone Designing an API Today

Three things.

First, **decide caching at design time**, not after performance becomes a problem. The choice of `max-age`, the choice of validator, the decision to send `Vary` — these are part of the API contract, not an optimization step.

Second, **don't reinvent freshness inside your service**. Whatever in-process cache you're tempted to build, HTTP already gave you a better one — at the edge, in the browser, in every CDN. Use it first.

Third, **be honest about staleness**. Every cache trades freshness for speed. Name the trade for each endpoint and document it. `max-age=300` is a contract with everyone downstream of you; behave like it.

## Closing

This was a talk that, when I gave it, sat inside a particular runtime. The runtime will keep changing. The headers won't. `Cache-Control`, `ETag`, `Last-Modified`, conditional GETs, `Vary` — that's the cache layer that's been waiting in the spec the whole time. Use it.

---

Follow me: [@helmedeiros](https://twitter.com/helmedeiros)
