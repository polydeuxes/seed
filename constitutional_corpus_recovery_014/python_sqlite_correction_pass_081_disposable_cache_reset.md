# Python SQLite Correction Pass 081 — Disposable Cache Reset

Repository authority wins.

## Correction

The event ledger is authoritative. SQLite projection, summary, index, and other read-model cache tables are disposable read models. Pass 081 removes the unsupported legacy/compatibility cache branch left by passes 075–080.

When a disposable cache table does not match the current schema, the implementation now drops the affected cache table and recreates the current schema. It does not interpret older cache schemas, migrate cache rows, add compatibility columns with `ALTER TABLE`, or preserve legacy cache standing.

## Replacement boundary

The smallest safe replacement boundary is the disposable cache table set owned by `SQLiteProjectionStore`:

- `projection_snapshots`;
- `state_summary_snapshots`;
- `derived_index_snapshots`.

If `projection_snapshots` is incompatible, dependent summary and derived-index caches are also discarded because their source projection cache standing is no longer current. Authoritative event tables are not modified or discarded.

## Preserved authority boundary

Rebuilds derive state from the surviving event ledger. Cache replacement and rebuild do not append false events and do not mutate cluster state. Current cache rows remain usable when their schema matches the current implementation.

## Superseded work

The legacy/compatibility cache standing, migration-inferred cache interpretation, and `ALTER TABLE` cache recovery claims from passes 075–080 are removed rather than preserved. Disposable cache recovery is now reset-and-rebuild only.

## Tests

Focused tests prove current schema reuse, incompatible schema replacement, event survival, ledger-derived rebuild equivalence, no false event appends, no cluster mutation, and summary cache recovery.
