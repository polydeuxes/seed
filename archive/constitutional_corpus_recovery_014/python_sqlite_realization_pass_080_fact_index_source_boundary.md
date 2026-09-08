# Python–SQLite realization pass 080 — Fact-index source boundary

Pass 080 consumes the corrected implementation after legacy cache reuse was removed.

## Selected boundary

The smallest next boundary is: SQLite-preserved state projection snapshot → SQLite-preserved derived fact-index snapshot → Python fact-index cache consumer.

## Repository evidence

`derived_index_snapshots` already stores a read-model cache keyed by state projection version and last event. Before this pass, SQLite loading joined to the state row only by workspace, projection version, and event id. That allowed a derived fact-index row to be consumed even when its source state row had widened consumer standing or mutating testimony. The fact index is a downstream read model, so it cannot lawfully be stronger than its source projection.

## Implementation

`SQLiteProjectionStore.load_derived_index_snapshot` now requires the joined state projection row to retain derived projection standing, Python state-projection producer boundary, snapshot-preservation-only occurrence kind, read-model-cache-only consumer limit, and `mutates_cluster=0`. No derived-index schema, universal envelope, ORM layer, or Book change was added.

## Lost limit recovered

The recovered limit is source-boundary eligibility for a downstream read-model cache. Version/event identity is still necessary but no longer sufficient when the source state projection row is outside the read-model cache boundary.

## Tests

A focused SQLite fact-index test proves that a cached derived index misses when the source projection row is changed to `consumer_limit='cluster_truth'`, then rebuilds without changing the indexed content. Existing fact-index and projection-store tests continue to prove cache hits, misses, stale behavior, and non-mutation boundaries.

## Remaining Unknowns

Derived-index rows still do not carry their own source-boundary columns; the selected repository evidence only required source-row gating at load time. Other read models and diagnostics may still need separate ownership recovery. The Python–SQLite realization is not complete.
