# State Summary Performance Inquiry Lineage Report

## Purpose

This report preserves the current inquiry lineage for the slow `seedstate` and
local-observation performance investigation.

It is a situation report for follow-on implementation work.

It is not a reconciliation, ontology proposal, frontier, schema proposal,
runtime redesign, storage redesign, or implementation patch.

## Original issue

The operator reported that `seedstate` was unreasonably slow.

Baseline timings before event batching:

```text
observe local, old:  4m6.931s
state summary, old: 4m16.743s
```

The first working theory was that both local observation and state summary were
slow because the observation/evidence/fact path wrote too many SQLite commits.

## Boundary documents used

The work was bounded by:

- `docs/current_observation_evidence_change_event_implementation_audit.md`
- `docs/current_observation_evidence_change_event_implementation_findings.md`
- `docs/corroboration_and_fact_promotion_reconciliation.md`
- `docs/source_definitions_and_entrypoint_observation_reconciliation.md`
- `docs/source_navigation_without_grep_audit.md`

The key boundary was:

```text
event granularity != transaction granularity
```

So the implementation path could improve transaction behavior, but could not
collapse observations, evidence, facts, or events.

## First implementation result

A generalized EventLedger batch interface was added:

```text
EventLedger.append_many(events)
SQLiteEventLedger.append_many(events)
```

This preserved one Event row per Event while allowing SQLite to persist multiple
events in one transaction.

Post-patch timings:

```text
observe now:  1m48.761s
summary now: 4m26.430s
```

This proved SQLite commit overhead was real, but the fix was incomplete for
local observation and did not address state-summary time.

## Observe profiling finding

Profiled `--observe-local-host` after the patch:

```text
73138880 function calls in 131.019 seconds
9641 calls observations.py:60(ingest)         129.234s cumulative
9641 calls events.py:168(append_many)         120.798s cumulative
9641 calls sqlite3.Connection.__exit__         94.132s cumulative
28923 calls events.py:291(_reserve_payload_ids) 15.668s cumulative
```

Finding:

```text
append_many exists,
but ObservationIngestor.ingest() still calls it once per observation.
```

Current likely shape:

```text
9641 observations
  -> 9641 ingest() calls
  -> 9641 append_many() calls
  -> 9641 SQLite transactions
```

Desired shape:

```text
9641 observations
  -> one batch ingest path
  -> same individual observation/evidence/fact events
  -> one or few append_many() calls
  -> one or few SQLite transactions
```

## State-summary profiling finding

Profiled `--state-summary`:

```text
938296092 function calls in 438.858 seconds
projected_state_from_args                       304.212s cumulative
project_state_with_cache                        292.926s cumulative
StateProjector.project                          285.339s cumulative
StateProjector.apply                            281.122s cumulative
```

Finding:

```text
that run missed or rebuilt the projection cache and replayed 28923 events.
```

Later repeated `seedstate` runs without new observation took about 55 seconds,
which suggests the profile run likely built the full State projection cache and
later runs used a cache hit.

However, 55 seconds for a cache hit is still too slow.

Likely reason:

```text
the existing projection cache stores full projected State,
then seedstate still loads/deserializes full State and computes the summary.
```

## Important distinction

There are two separate performance problems.

### Problem 1: observe-local-host

The ledger batch API exists, but the ingestion path batches only per
observation. It needs a batch-ingest path that collects all generated events and
persists them through one or few `append_many()` calls.

### Problem 2: seedstate

The existing projection cache is a full State cache. It helps avoid replay, but
cache-hit summary still costs roughly 55 seconds. A compact read-model cache may
be needed later.

These should not be fixed in the same patch.

## Source-navigation gap discovered

During investigation, the operator had to grep for:

```text
project_state_with_cache
SQLiteProjectionStore
state_summary
build_state_summary
--state-summary
```

That exposed a separate gap preserved in:

```text
docs/source_navigation_without_grep_audit.md
```

Current relationship observation is import-only, which answers dependency
questions but not ownership, entrypoint, dispatch, or call-path questions.

This gap does not block the performance fix, but explains why the investigation
needed manual grep.

## Boundaries preserved

The investigation preserved:

```text
transaction batching != event batching
EventLedger history != projection cache
full State projection != compact summary projection
summary cache != authority
grep capability != repository self-knowledge
imports != ownership
definitions != invocation
entrypoints != capability authority
```

## Recommended next implementation slice

Implement observation-batch persistence without semantic observation batching.

Target behavior:

```text
same observations
same evidence
same facts
same event count
same event order
same projected state
fewer SQLite transactions
```

Suggested shape:

```text
ObservationIngestor.ingest_many(observations)
    builds the same per-observation event sequence
    collects all events
    calls ledger.append_many(all_events)
```

`ObservationIngestor.ingest(observation)` may remain for compatibility and may
delegate to the batch path for one observation.

## Follow-up after ingestion batching

After ingestion batching is fixed and measured, separately investigate the
summary-side cache shape:

```text
event ledger
  -> full State projection cache
      -> compact state-summary projection/cache
```

Small read-model caches should depend on the full projection cache validity and
must not become authority over event history.

## Final finding

The original performance issue split into two findings:

```text
observe-local-host remains slow because append_many is still invoked once per observation.

seedstate remains slow because cache misses replay all events, and cache hits still load enough full-State material to be expensive.
```

The next safe implementation move is the ingestion-side batch path.
