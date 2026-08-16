# Current Observation Evidence Change Event Implementation Findings

## Purpose

This document records the actual implementation findings for the audit scoped by:

- `docs/current_observation_evidence_change_event_implementation_audit.md`

It inspects the current code path around observation ingestion, evidence creation,
fact promotion, event persistence, projection, and commit behavior.

This is a documentation-only implementation audit.

It does not modify code, schemas, tests, ingestion, projection, event persistence,
or runtime behavior.

## Files Inspected

- `seed_runtime/observations.py`
- `seed_runtime/events.py`
- `seed_runtime/state.py`

## Central Finding

The current implementation explicitly separates observations, evidence, and
facts as model/event kinds, but it does not explicitly represent change as a
first-class persisted object in the inspected ingestion path.

The current hot path is approximately:

```text
ObservationIngestor.ingest(observation)
        ↓
observation_to_evidence(observation)
        ↓
observation_to_fact(observation, evidence)
        ↓
ledger.append("observation.observed")
        ↓
ledger.append("evidence.observed")
        ↓
ledger.append("fact.observed" or "fact.inferred")
```

For most observations, one ingested observation becomes three persisted events.

For fact-promotion-suppressed observations, one ingested observation becomes two
persisted events.

## Finding 1: Observation Is Explicit

`Observation` is a first-class model with:

```text
id
source_type
observed_at
subject
predicate
value
confidence
metadata
dimensions
expires_at
```

The ingestor appends an `observation.observed` event carrying the serialized
observation.

The StateProjector later applies `observation.observed` by reconstructing the
Observation and storing it in `state.observations`.

Implementation status:

```text
Observation: implemented explicitly
```

## Finding 2: Evidence Is Explicit But Directly Derived From Observation

`ObservationIngestor.observation_to_evidence()` creates an `Evidence` model from
an Observation.

The evidence payload preserves:

```text
observation_id
source_type
subject
predicate
value
metadata
dimensions
expires_at
```

The ingestor appends an `evidence.observed` event carrying the serialized
evidence plus observation metadata.

The StateProjector later applies `evidence.observed` by reconstructing Evidence
and storing it in `state.evidence`.

Implementation status:

```text
Evidence: implemented explicitly
Observation -> Evidence: implemented directly and one-to-one for this path
```

Important limitation:

The inspected path creates one evidence object from one observation. It does not
show a batch-level evidence object or multi-observation evidence composition in
this ingestion path.

## Finding 3: Fact Promotion Is Immediate For Most Observations

`ObservationIngestor.observation_to_fact()` converts an Observation and its
Evidence into a Fact.

The produced Fact contains:

```text
subject_id = observation.subject
predicate = observation.predicate
value = observation.value
dimensions = observation.dimensions
evidence_ids = [evidence.id]
source_type = observation.source_type
confidence = observation.confidence
observed_at = observation.observed_at
expires_at = observation.expires_at
inferred = observation.source_type == "inferred"
```

The ingestor appends either:

```text
fact.observed
```

or:

```text
fact.inferred
```

based on `fact.inferred`.

Implementation status:

```text
Evidence -> Fact: implemented directly and immediately for most observations
```

Architectural concern:

The current generic observation ingestion path still largely behaves as:

```text
Observation
        ↓
Evidence
        ↓
Fact
```

with little candidate/routing delay unless promotion is explicitly suppressed.

## Finding 4: Promotion Suppression Exists But Is Narrow

There is a suppression hook:

```text
_should_suppress_fact_promotion(observation)
```

Currently inspected behavior suppresses fact promotion only when:

```text
metadata.fact_promotion_suppressed is True
source_name == "prometheus"
prometheus_metric == "node_uname_info"
predicate == "os"
```

In that case, the observation and evidence are preserved, but no fact event is
created.

Implementation status:

```text
Candidate / no-promotion behavior: partially implemented, narrow special case
```

Architectural concern:

This is consistent with recent Prometheus boundary work, but it is not yet a
general routing/promotion architecture.

## Finding 5: Event Is Explicit And Used As Persistence Unit

`EventLedger.append()` creates an Event and stores it.

`SQLiteEventLedger.append()` creates an Event and calls `_insert(event)`.

`SQLiteEventLedger._insert()` inserts one row into the `events` table and commits
immediately.

The traceback from `seed --observe-local-host` matches this implementation:

```text
ingest
    -> ledger.append
        -> SQLiteEventLedger._insert
            -> connection.commit
```

Implementation status:

```text
Event: implemented explicitly
SQLite persistence: one commit per event insert
```

## Finding 6: One Observation Usually Produces Three Events

For a normal observation, the ingestor appends:

```text
1 observation.observed event
1 evidence.observed event
1 fact.observed or fact.inferred event
```

Therefore:

```text
1 observation
        -> 3 events
        -> 3 SQLite commits
```

for the common path.

For suppressed fact promotion:

```text
1 observation
        -> 2 events
        -> 2 SQLite commits
```

This explains why a 10,000-observation run can be slow and appear frozen.

Approximate implication:

```text
10,000 observations
        -> up to 30,000 events
        -> up to 30,000 SQLite commits
```

before considering other event types.

## Finding 7: Change Is Not First-Class In The Inspected Path

The inspected code does not create an explicit `change` model or `change.*`
event during observation ingestion.

StateProjector reconstructs state by applying events and then derives current
projection indexes such as:

```text
alias resolver
measurement history retention
inferred facts
fact supports
relationships
entity type assertions
graph issues
fact conflicts
```

This means change is mostly represented implicitly by:

```text
event sequence
projected state before/after
fact support selection
relationship projection
conflict projection
```

rather than as a preserved first-class object.

Implementation status:

```text
Change: not first-class in inspected ingestion path
Change: derivable from events/projection, but not explicitly persisted
```

## Finding 8: Projection Separates Current State From Event History

StateProjector reads all workspace events and applies them in order.

It preserves observations, evidence, and facts in state, then derives additional
projection surfaces.

It also retains projected measurement history using a measurement history limit,
showing that persisted event history and projected current state are distinct.

Implementation status:

```text
Event history: preserved in ledger
Current state: projected from ledger
Projection: implemented separately from raw events
```

## Reconciliation Check

Against the conceptual chain:

```text
Observation
    ↓
Evidence
    ↓
Claim / Fact
    ↓
Change
    ↓
Event
```

Current implementation appears to be:

```text
Observation
    implemented explicitly

Observation -> Evidence
    implemented directly, usually one-to-one

Evidence -> Fact
    implemented directly, usually immediate

Fact -> Change
    not explicit in inspected path

Change -> Event
    not explicit in inspected path

Event
    implemented explicitly as persistence/history unit
```

The actual implementation shape is closer to:

```text
Observation
    -> Evidence
    -> Fact

Observation/Event
Evidence/Event
Fact/Event

Projection derives current state and current support/conflict/relationship views
from event history.
```

## Boundary Collapses Or Tight Couplings

### Tight coupling: Observation to Evidence

Every ingested observation creates evidence immediately.

This is not necessarily wrong, but it is direct and one-to-one in the inspected
path.

### Tight coupling: Evidence to Fact

Most evidence immediately creates a fact.

This is a stronger architectural coupling than recent candidate/routing/promotion
reconciliations may eventually want.

### Collapse risk: Event as persistence for every layer

Observation, evidence, and fact are separate event kinds, but all are persisted as
ledger events.

This is clear and replayable, but expensive with one commit per event.

### Missing: explicit Change

Change is not first-class in the inspected path.

Repeated observations may produce new observation/evidence/fact events even when
they do not change projected current state.

## Direct Answer To The 10,000 Observation Question

When Seed reports approximately 10,000 observations from local host observation,
the current implementation likely preserves:

```text
~10,000 observation.observed events
~10,000 evidence.observed events
~10,000 fact.observed/fact.inferred events
```

for observations not suppressed from fact promotion.

What is changing?

```text
The event ledger grows.
The projected observation set grows.
The projected evidence set grows.
The projected fact set grows or updates current support.
Current-state projections may or may not materially change.
```

What becomes an event?

```text
Observation preservation becomes an event.
Evidence preservation becomes an event.
Fact preservation becomes an event.
```

What does not currently become an explicit event in the inspected path?

```text
Change itself.
Observation batch itself.
Collection activity itself.
Execution status itself.
```

## Performance Finding

The observed delay is consistent with implementation behavior.

The hot path likely performs:

```text
up to 3 append calls per observation
1 SQLite commit per append call
```

This is an implementation performance issue, not evidence that collection is
frozen.

## Implementation Implications

The safest near-term implementation work is probably not semantic batching.

The safest near-term implementation work is storage transaction batching or an
append-many API that preserves event granularity while reducing commit frequency.

However, this should be done carefully:

```text
transaction batching must not imply observation batching
transaction batching must not imply event semantic collapse
transaction batching must not erase event order
transaction batching must not erase causation/correlation
```

A separate implementation prompt should focus narrowly on SQLite commit batching
or bulk append behavior while preserving the existing event model.

## Suggested Regression Coverage For Future Implementation

Future performance work should prove:

1. Ingesting one normal observation still produces observation/evidence/fact
   events.
2. Ingesting a fact-promotion-suppressed observation still produces only
   observation/evidence events.
3. Event order remains stable.
4. Causation/correlation IDs remain stable.
5. State projection remains unchanged before and after transaction batching.
6. SQLite commit count or transaction behavior improves without changing event
   count.
7. Interrupt safety is understood and tested if transaction boundaries change.

## Final Finding

The current implementation does distinguish observations, evidence, facts, and
events as separate persisted structures, but it does not distinguish change as a
first-class persisted object in the inspected ingestion path.

For the current local host ingestion path, one observation usually produces three
separate events and, in SQLite, three separate commits.

The next bounded implementation opportunity is transaction batching or bulk event
append behavior that preserves existing event granularity while reducing commit
frequency and enabling execution-status feedback.
