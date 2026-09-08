---
doc_type: audit
status: active
domain: temporal authority
defines:
  - temporal provenance
  - temporal authority
  - time kinds
depends_on:
  - temporal_reasoning_audit.md
  - event_and_change_reconciliation.md
  - observation_evidence_change_event_reconciliation.md
  - current_observation_evidence_change_event_implementation_findings.md
  - prometheus_observation_boundary_reconciliation.md
related:
  - occurrence_time_and_temporal_claim_reconciliation.md
  - learning_and_knowledge_change_reconciliation.md
  - contradiction_discovery_and_visibility_reconciliation.md
---

# Time Provenance And Temporal Authority Audit

## Purpose

This audit investigates a temporal boundary exposed by the discussion of events,
observations, changes, Prometheus samples, and clock authority.

The core question is:

```text
What time is Seed actually recording?

Whose clock supplied it?

What kind of time is it?
```

This is a documentation-only audit.

It does not modify code, schemas, Prometheus ingestion, observation ingestion,
event persistence, projection, tests, or runtime behavior.

## Documents And Code Reviewed

- `docs/temporal_reasoning_audit.md`
- `docs/event_and_change_reconciliation.md`
- `docs/observation_evidence_change_event_reconciliation.md`
- `docs/current_observation_evidence_change_event_implementation_findings.md`
- `docs/prometheus_observation_boundary_reconciliation.md`
- `seed_runtime/observation_sources.py`
- `scripts/seed_local.py`

## Central Finding

Seed has temporal fields, but it does not yet fully model temporal provenance or
temporal authority.

The existing temporal audit correctly documents that Seed carries time in events,
observations, evidence, facts, support, approvals, authorizations, and projection
snapshots. It also documents that event replay order is append order, while some
fact selection uses `observed_at`.

The newly exposed gap is different:

```text
A timestamp is not self-authorizing.
```

A timestamp has a source, a clock, a scope, and a meaning.

Seed currently records several timestamps, but it does not consistently preserve:

```text
which clock supplied the timestamp
whether the timestamp is occurrence time, observation time, knowledge time, or preservation time
whether the timestamp was asserted by a source, assigned by Seed, derived, or normalized
how reliable that time is
```

## Core Ontological Distinction

The key distinction is:

```text
Occurrence
        != Observation
        != Knowledge
        != Preservation
```

A service may crash at 12:00.

Prometheus may scrape evidence at 12:05.

Seed may ingest the observation at 12:06.

Seed may persist the event at 12:06:01.

Those are four different temporal claims.

## Time Kinds

### Occurrence Time

Occurrence time is when the thing in reality happened.

Example:

```text
The service crashed at 12:00.
```

Seed usually does not directly know occurrence time.

Occurrence time must be inferred, asserted by a source, or derived from logs or
other evidence.

### Observation Time

Observation time is when a source observed or sampled something.

Example:

```text
Prometheus sample timestamp
local host collection time
SSH command read time
operator report time
```

Observation time may come from the source clock or from Seed's collection clock.

### Knowledge Time

Knowledge time is when Seed became justified in using the support.

This is close to ingestion time or evidence construction time, but it is not
identical to occurrence time.

### Preservation Time

Preservation time is when Seed recorded something in its ledger.

This is represented by `Event.timestamp` in the current implementation.

## Current Implementation: Local Host Observation

`LocalHostObservationSource.collect()` captures one `observed_at` value from
`datetime.now(timezone.utc)` at the start of collection and passes that same time
to all observations produced by that collection run.

This is a Seed/client local collection timestamp.

It is not the occurrence time of each underlying host condition.

For example:

```text
/etc/hosts contains mapping X
```

was likely true before collection began.

Seed records when it observed the mapping, not when the mapping came into
existence.

## Current Implementation: CLI Observations

Manual CLI observations use `utc_now()` at ingestion time to set `observed_at`.

That means:

```text
--observe SUBJECT PREDICATE VALUE
```

records the time Seed accepted the CLI observation, not necessarily when the
operator first observed the underlying condition or when the condition occurred.

## Current Implementation: JSON Observations

JSON observations can carry their own `observed_at`; otherwise they default to a
fixed `DEFAULT_JSON_OBSERVED_AT` value.

This means imported observations can preserve source-provided observation time,
but the code does not separately classify whether that time was source-asserted,
defaulted, normalized, or derived.

## Current Implementation: Prometheus Observation

`PrometheusObservationSource.collect()` captures one `observed_at` value from
`datetime.now(timezone.utc)` before querying Prometheus and passes that same time
to observations produced from all allowlisted Prometheus queries.

The Prometheus vector result includes a `value` array. The code validates that it
exists and reads the sample value from `value[1]`.

The code does not currently preserve or use `value[0]`, the Prometheus sample
timestamp.

Therefore the Prometheus sample timestamp is effectively discarded, and Seed
substitutes its own collection time as `Observation.observed_at`.

This is the clearest current temporal authority bug.

## Why Prometheus Time Matters

Prometheus vector samples include a sample timestamp and a sample value.

Those are not equivalent.

The sample timestamp answers:

```text
When does Prometheus say this sample is from?
```

Seed's collection time answers:

```text
When did Seed query Prometheus?
```

The event timestamp answers:

```text
When did Seed preserve the resulting event?
```

Using Seed collection time as observation time discards the source's temporal
claim.

That weakens temporal reasoning, measurement latest-current behavior, debugging,
and future federation.

## Relationship To Change

A change cannot usually be recorded at the moment it occurs unless Seed observes
that occurrence directly.

Most change knowledge is retrospective.

Seed can know:

```text
At time T_observed, evidence suggested condition C.
```

Seed may infer:

```text
The condition changed sometime before T_observed.
```

But it should not claim:

```text
The change occurred exactly at T_observed.
```

unless evidence supports that stronger claim.

## Relationship To Events

Events have preservation timestamps.

Events are Seed-facing historical records.

They are not automatically occurrence timestamps for the external reality being
observed.

This distinction matters because current implementation can produce:

```text
observation.observed event at Seed time T3
```

for an observation whose source timestamp was T2 and whose occurrence was likely
before T2.

## Relationship To Measurement Selection

The existing temporal audit documents that measurement latest-current behavior
uses `Fact.observed_at`.

If Prometheus sample timestamps are discarded and replaced with Seed collection
time, then measurement latest-current selection is based on Seed collection time,
not Prometheus sample time.

That may be acceptable for some live scrapes, but it is not source-faithful and
will fail for delayed, replayed, cached, remote, or federated samples.

## Temporal Authority Types

Seed should eventually distinguish timestamp authority such as:

```text
seed_local_clock
source_sample_clock
remote_seed_clock
operator_asserted_time
imported_document_time
log_record_time
derived_interval
unknown
```

These are not interchangeable.

## Temporal Metadata Needed

Future observations may need metadata such as:

```text
time_kind: observation_time | occurrence_time | preservation_time | knowledge_time
observed_at_source: seed_local_clock | prometheus_sample | operator_asserted | imported_payload
source_observed_at: <timestamp from source>
seed_collected_at: <timestamp from Seed collector>
source_clock_trusted: true/false/unknown
source_clock_identity: prometheus_server | remote_seed | local_host | operator
source_timestamp_raw: <raw timestamp if applicable>
```

The exact schema is future work.

The boundary is the important finding.

## Boundary Classification

### Correct Existing Behavior

Seed correctly has separate event timestamps and observation timestamps.

Seed correctly projects by append order rather than blindly sorting events by
timestamp.

Seed correctly carries `observed_at` on observations, evidence, facts, and support
structures.

### Missing Boundary

Seed does not consistently preserve temporal provenance.

It often records a timestamp without recording whose clock supplied it or what
kind of time it represents.

### Implementation Bug

Prometheus sample timestamps are currently discarded.

The code reads `value[1]` as the sample value but does not preserve `value[0]` as
source sample time.

## Non-Collapses

Seed must not collapse:

```text
Occurrence Time != Observation Time
Observation Time != Knowledge Time
Knowledge Time != Preservation Time
Source Timestamp != Seed Timestamp
Event Timestamp != External Occurrence Time
Prometheus Sample Time != Seed Collection Time
Remote Seed Time != Local Seed Time
Operator Report Time != Occurrence Time
```

## Recommended Next Implementation Direction

Do not redesign the entire temporal model first.

The safest implementation slice is Prometheus-specific:

```text
Preserve Prometheus sample timestamp as source temporal metadata.
```

A narrow implementation should:

1. Parse `value[0]` from Prometheus vector samples.
2. Preserve it as source-provided sample time.
3. Keep Seed collection time separately.
4. Decide explicitly whether `Observation.observed_at` should be source sample
   time or Seed collection time for Prometheus observations.
5. Add metadata so the choice is inspectable.
6. Add tests proving source sample timestamp is not discarded.

A conservative first step may keep `Observation.observed_at` as the Seed
collection time while adding:

```text
metadata.prometheus_sample_timestamp
metadata.source_observed_at
metadata.seed_collected_at
```

A stronger step may set `Observation.observed_at` to the Prometheus sample time
and preserve Seed collection time separately. That should be decided explicitly
against measurement-selection semantics.

## Suggested Regression Tests

Add tests proving:

1. Prometheus vector `value[0]` is parsed and preserved.
2. Prometheus vector `value[1]` remains the sample value.
3. Seed collection time remains available separately.
4. Event timestamp remains independent from Prometheus sample time.
5. Measurement latest-current behavior is explicit when source sample time and
   Seed collection time differ.
6. Delayed or out-of-order Prometheus samples do not silently inherit Seed query
   time as if it were sample time.

## Direct Answer

Seed currently knows several times, but not always what kind of time they are.

For Prometheus specifically, Seed currently knows when it queried Prometheus, but
it throws away when Prometheus says the sample occurred.

That means Seed currently cannot faithfully distinguish:

```text
Prometheus sampled this at T_source
```

from:

```text
Seed queried Prometheus at T_seed
```

This is a temporal authority boundary issue.

## Final Finding

The current temporal model is explicit but not provenance-rich enough.

The key missing boundary is temporal authority: Seed must preserve not only a
timestamp, but also whose clock supplied it and what kind of time it claims to
be.

Prometheus ingestion currently exposes the clearest defect because it discards
the source sample timestamp and uses Seed's collection time for observations.

The next safe implementation work should preserve Prometheus sample time without
collapsing it into event time, occurrence time, knowledge time, or local Seed
collection time.
