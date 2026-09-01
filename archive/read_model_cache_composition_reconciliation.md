# Read Model Cache Composition Reconciliation

## Purpose

Recent performance work added and validated several cache layers:

```text
Event Ledger
    ↓
Full State Projection Cache
    ↓
Dependent State-Summary Cache
```

Later inspection commands exposed a remaining scalability problem.

A command such as:

```text
seed --capability-candidates ssh
```

can build or load the full State cache, but a later `seedstate` may still spend significant time building the dependent state-summary cache.

That reveals a broader question:

```text
How should Seed compose caches when there may eventually be hundreds or thousands of read-model views?
```

This reconciliation investigates cache composition boundaries.

It is documentation-only.

It does not implement runtime behavior, change cache invalidation, introduce schemas, modify projection semantics, or propose view-specific optimizations.

## Evidence Basis

This reconciliation follows from repository work around:

- EventLedger authority;
- State projection and projection cache;
- incremental projection replay;
- state-summary dependent read-model cache;
- current-facts and capability inspection command performance;
- execution-status visibility for cache/projection work;
- read-only capability candidate, verification, evidence, and promotion-readiness inspection surfaces;
- repository findings that derived surfaces must not become authority.

Repository authority wins if this document diverges from higher-authority reconciliations.

## Central Question

What cache structure allows Seed to support many read-model views without making every new view cache miss pay the cost of full State deserialization and full view recomputation?

## Current Shape

The current shape is roughly:

```text
Event Ledger
    ↓
Full State Projection Cache
    ↓
View-specific computation
    ↓
Optional View Cache
```

This works for a small number of views.

It becomes less scalable when there are many operator-facing views, including:

```text
state summary
current facts
fact support
capability candidates
capability verification
verification evidence
promotion readiness
repository relationship views
future source-navigation views
future documentation views
```

Each view may otherwise be tempted to derive itself independently from the full State object.

## Central Finding

The repository should distinguish at least three cache/read-model roles:

```text
Projection Cache
    preserves reusable projected State derived from EventLedger

Derived Index Cache
    preserves reusable intermediate indexes derived from projected State

View Cache
    preserves final operator-facing read-model output or compact view payloads
```

These roles should not collapse.

## Projection Cache

The projection cache answers:

```text
What is the reusable projected State at a known event/version boundary?
```

It depends on EventLedger authority.

It preserves full projected state semantics.

It should not be treated as a view cache.

```text
Projection Cache != View Cache
Projection Cache != Event Authority
```

## Derived Index Cache

A derived index cache answers:

```text
What reusable intermediate structures can support many views?
```

Examples may include:

```text
facts by subject/predicate
facts by predicate
facts by source type
facts by evidence id
entities by kind
aliases by canonical entity
capability evidence index
relationship index
observation source index
measurement-current index
```

A derived index cache is not the source of truth.

It is a reusable read-model substrate.

```text
Derived Index Cache != Projection Authority
Derived Index Cache != View Output
```

## View Cache

A view cache answers:

```text
What final read-model output should this operator-facing command display?
```

Examples:

```text
state-summary payload
capability-candidates JSON
capability-verification JSON
current-facts filtered output
repository source navigation view
```

A view cache should remain dependent on projection/index validity.

```text
View Cache != Source Of Truth
View Cache != Projection Authority
```

## Why Warming Every View Does Not Scale

A tactical fix would be:

```text
when full State cache is built,
also warm the state-summary cache
```

That may solve one symptom.

But generalized across many views it becomes:

```text
new view slow?
    ↓
warm it too
```

That does not scale.

It can produce unnecessary work, wasted storage, and unpredictable write amplification.

## Better Shape

A more scalable shape is:

```text
Event Ledger
    ↓
Full State Projection Cache
    ↓
Derived Index Cache(s)
    ↓
View Cache(s)
```

Then a new view can build from indexes rather than scanning and deserializing all full State structures independently.

Example:

```text
Full State
    ↓
fact index by subject/predicate
    ↓
current-facts view
```

```text
Full State
    ↓
capability evidence index
    ↓
capability-candidates view
    ↓
capability-verification view
    ↓
promotion-readiness view
```

```text
Full State
    ↓
entity summary index
    ↓
state-summary view
```

## Cache Composition Boundary

Cache composition asks:

```text
Which derived structures can safely support multiple views?
```

It does not ask:

```text
Which view should be eagerly warmed?
```

It also does not ask:

```text
Should cache output become authority?
```

## Authority Boundary

The authority chain remains:

```text
EventLedger
    ↓
State Projection
    ↓
Derived Indexes
    ↓
Views
```

Each lower layer is derived.

No derived index or view cache should be treated as independent truth.

## Freshness Boundary

Every derived cache must remain anchored to a projection version and event boundary.

The minimum validity shape appears to be:

```text
workspace_id
projection_name / index_name / view_name
version
state_projection_version
state_last_event_id
created_at
```

This reconciliation does not define a schema.

It only records that derived caches must remain dependent on the authoritative projection/event boundary.

## Strongest Finding

The strongest finding is:

```text
Full State cache hits can still be expensive when every view miss requires full State deserialization and independent scanning.
```

Therefore the next scaling problem is not only projection replay.

It is read-model derivation composition.

## Strongest Distinction

The strongest distinction is:

```text
Projection Cache
    !=
Derived Index Cache
    !=
View Cache
```

Projection caches preserve projected State.

Derived index caches preserve reusable intermediate read models.

View caches preserve final operator-facing read models.

## Strongest Risk

The strongest risk is ad hoc view warming.

If each new view receives its own independent cache and warming path, Seed may accumulate many fragile, duplicated, expensive read-model derivations.

That would make new capabilities harder to add and harder to reason about.

## Relationship To Capability Views

Capability work makes the problem visible.

The current chain includes:

```text
capability candidates
capability verification
verification evidence
promotion readiness
```

These views share underlying evidence relationships.

They likely should not each rediscover the same facts independently.

This suggests a possible reusable intermediate:

```text
capability evidence index
```

This reconciliation does not implement or require that index.

It only observes that capability read-models are a strong candidate for cache composition pressure.

## Relationship To State Summary

The state-summary cache solved repeated summary requests.

It does not solve the first summary miss after another command has already built the full State cache.

That miss still may pay full State load/deserialization plus summary computation.

This shows why dependent view caches alone are insufficient as the number of views grows.

## Relationship To Execution Status

Execution status now makes cache behavior visible.

That visibility is important because it lets operators distinguish:

```text
cache miss and projection replay
```

from:

```text
cache hit but expensive read-model derivation
```

This reconciliation depends on that distinction.

## Non-Goals

This reconciliation does not:

- implement derived index caches;
- define schemas;
- change projection cache behavior;
- change summary cache behavior;
- add new caches;
- warm existing caches;
- optimize projection replay;
- alter authority boundaries;
- define cache eviction;
- define storage topology.

## Implementation Implications

If implementation follows, the safest first slice is likely an audit or inventory of expensive view derivations.

A bounded implementation might then introduce one reusable derived index that supports multiple existing views, such as a fact index by subject/predicate or a capability evidence index.

Any implementation should prove:

```text
index output is derived
index validity depends on State projection event/version
views remain equivalent
cache misses are cheaper or shared
```

## Final Finding

Seed should avoid treating every read-model cache as an independent one-off optimization.

The scalable cache model is compositional:

```text
Event Ledger
    ↓
Projection Cache
    ↓
Derived Index Cache(s)
    ↓
View Cache(s)
```

This preserves authority while giving future read-model views a shared substrate, reducing the pressure to make every new view pay the full cost of State deserialization and independent scanning.
