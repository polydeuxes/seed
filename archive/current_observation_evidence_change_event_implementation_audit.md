# Current Observation Evidence Change Event Implementation Audit

## Purpose

Recent reconciliations established the conceptual distinctions:

```text
Observation
Evidence
Claim
Change
Event
```

The next question is implementation-oriented:

```text
Does the current implementation preserve these distinctions?

Or are some of them collapsed together in practice?
```

This audit investigates the implementation boundary rather than introducing new architecture.

## Central Finding

A conceptual distinction and an implementation distinction are not the same thing.

Seed may architecturally distinguish:

```text
Observation
Evidence
Change
Event
```

while still implementing some of them through shared structures.

Therefore the next task is inspection rather than redesign.

## Questions To Answer

### Observation Boundary

Determine:

```text
What structure currently represents observations?
```

Examples:

```text
ObservationFact
ObservationRecord
ObservationEnvelope
ObservationEvent
```

or repository equivalents.

Determine:

```text
What is preserved?
What provenance exists?
What identity exists?
```

## Evidence Boundary

Determine:

```text
Where does evidence begin?
```

Questions:

```text
Is evidence explicitly represented?

Is evidence merely inferred from observations?

Can multiple observations support one claim?

Can one observation support multiple claims?
```

## Claim Boundary

Determine:

```text
Where do observations become claims?
```

Identify:

```text
promotion boundaries
claim creation boundaries
relationship creation boundaries
```

## Change Boundary

Determine:

```text
How is change represented?
```

Questions:

```text
Is change explicit?

Is change derived?

Does every observation create change?

Does every promoted claim create change?
```

## Event Boundary

Determine:

```text
What is an event in the current implementation?
```

Questions:

```text
Does an event preserve observation?
Does an event preserve change?
Does an event preserve both?
```

## Observation Count Versus Event Count

The motivating concern was:

```text
~10,000 observations
```

Determine:

```text
How many events were produced?
```

and:

```text
Why?
```

## Ingestion Path

Audit the path:

```text
collect
    ↓
ingest
    ↓
append
    ↓
persist
```

Determine:

```text
what object travels through the path
what transformations occur
what preservation occurs
```

## Commit Behavior

Determine:

```text
observation -> event -> commit
```

versus:

```text
observation batch -> event -> commit
```

or other actual implementation behavior.

The goal is understanding, not optimization.

## Reconciliation Check

Evaluate implementation against the conceptual chain:

```text
Observation
    ↓
Evidence
    ↓
Claim
    ↓
Change
    ↓
Event
```

For each edge identify:

```text
implemented
partially implemented
collapsed
missing
```

## Non-Goals

Do not:

- redesign the event model;
- redesign evidence;
- redesign ingestion;
- redesign storage;
- optimize SQLite;
- implement batching.

This is an audit only.

## Expected Deliverable

Create a report describing:

```text
current implementation shape
current preservation unit
current event unit
current evidence representation
collapsed boundaries
missing boundaries
surprising findings
```

## Final Question

Answer explicitly:

```text
When Seed reports 10,000 observations,
what exactly is being preserved,
what exactly is changing,
and what exactly becomes an event?
```

That answer should be grounded in repository implementation rather than architectural intent.
