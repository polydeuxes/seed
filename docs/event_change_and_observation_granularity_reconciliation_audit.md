# Event Change And Observation Granularity Reconciliation Audit

## Purpose

This audit compares:

- docs/event_and_change_reconciliation.md
- docs/observation_batching_and_event_granularity_reconciliation.md

The goal is to determine whether the newer observation batching work conflicts
with the existing Event/Change architecture or whether the two documents are
examining different boundaries of the same system.

## Motivation

The batching reconciliation emerged from a practical observation.

A local host observation run produced approximately:

```text
10,000 observations
```

This naturally raised questions about:

```text
event granularity
transaction granularity
observation granularity
evidence granularity
```

However, Seed already contains an Event/Change reconciliation.

Therefore the correct question is:

```text
Did the batching work rediscover an existing boundary?

Or did it discover an adjacent one?
```

## Central Finding

The two reconciliations approach the system from opposite directions.

The Event/Change reconciliation approaches from preservation.

The Observation Batching reconciliation approaches from acquisition.

They appear complementary rather than contradictory.

## Direction Of Analysis

Event/Change asks:

```text
What happened?
What changed?
What should be preserved?
```

Observation Batching asks:

```text
What was collected?
How many observations were produced?
What is the unit of acquisition?
```

These are not identical questions.

## Candidate Shape

The emerging combined shape appears to be:

```text
Collection Activity
        ↓
Observation Batch
        ↓
Observations
        ↓
Evidence
        ↓
Claims / Relationships
        ↓
Change
        ↓
Event
```

This is not asserted as architecture.

It is the candidate shape suggested by the two documents together.

## Observation And Event Are Different

The batching reconciliation established:

```text
Observation
        != Event
```

This appears compatible with Event/Change thinking.

A package observation:

```text
nginx installed
```

is not obviously an event.

It is an observed statement.

The event architecture appears concerned with preservation of change, not with
raw acquisition cardinality.

## Collection Activity And Event Are Different

The batching reconciliation also established:

```text
Collection Activity
        != Event
```

Example:

```text
package inventory run
```

may produce hundreds of observations.

The inventory run itself is an activity.

The observations are acquisition results.

Neither necessarily determines event granularity.

## Observation Batch And Event Are Different

The strongest new finding is likely:

```text
Observation Batch
        != Event
```

An observation batch exists because acquisition often has natural grouping:

```text
one /etc/hosts read
one package scan
one Prometheus query
```

Event architecture may choose to preserve that grouping.

But the grouping itself is not automatically an event.

## Storage Optimization Does Not Resolve Architecture

A key risk discovered during the batching discussion:

```text
many observations
        ↓
performance concern
        ↓
batching implementation
```

can accidentally become:

```text
many observations
        ↓
one event
```

without architectural justification.

The Event/Change reconciliation protects against this.

Storage optimization and event semantics should remain independent decisions.

## Evidence Appears To Be The Missing Edge

The batching reconciliation repeatedly encountered:

```text
Observation
        ↓
Evidence
```

while the Event/Change work focuses more heavily on:

```text
Change
        ↓
Event
```

This suggests the two reconciliations may be connected through evidence.

Possible relationship:

```text
Observation
        supports
Evidence

Evidence
        supports
Claim

Claim
        contributes to
Change

Change
        preserved by
Event
```

This edge has not yet been fully reconciled.

## Replay Implications

A future replay system may care about:

```text
events
changes
```

while an explanation system may care about:

```text
evidence
observations
```

This further suggests that observation count and event count need not be equal.

## The Real Question Discovered

The batching discussion started with:

```text
How many commits should SQLite perform?
```

The deeper question became:

```text
What is the architectural unit of preservation?
```

The Event/Change reconciliation already occupies part of that territory.

The batching reconciliation therefore appears to have found a missing adjacent
boundary rather than a contradiction.

## Architectural Invariants

```text
Collection Activity != Observation
Observation Batch != Observation
Observation != Evidence
Observation != Event
Collection Activity != Event
Transaction Batch != Observation Batch
Storage Optimization != Semantic Collapse
```

Additional candidate invariant:

```text
Event preserves change.
Observation records acquisition.
```

This candidate requires validation against the authoritative Event/Change
reconciliation.

## Recommended Next Audit

The next useful audit is likely not storage batching.

The next useful audit is:

```text
Observation
        ↔ Evidence
        ↔ Change
        ↔ Event
```

Specifically:

```text
How does observed support become preserved change?
```

This appears to be the missing edge connecting the two document families.

## Final Finding

The batching reconciliation does not appear to conflict with the Event/Change
reconciliation.

Instead, the two documents examine different layers of the same system.

Event/Change views the architecture from preservation and historical change.

Observation Batching views the architecture from acquisition and provenance.

The missing connection is likely the path through evidence and claim formation.

Before implementing batching, transaction optimization, or event aggregation,
Seed should reconcile how observations, evidence, change, and events relate so
that performance improvements do not accidentally redefine the unit of
preservation.