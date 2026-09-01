# Python–SQLite Jurisdiction Pass 071 — Projection Snapshot Boundary

Repository authority wins.

## Selected seam

The implemented seam is: bounded Python state projection → bounded crossing artifact (`ProjectionSnapshot` with `ProjectionSnapshotBoundary`) → SQLite projection snapshot preservation → bounded Python cache consumer.

## Why both Python and SQLite are required

Python owns projection formation and materialization because the implementation evidence places replay, model construction, and read-model interpretation in `StateProjector` and `state_from_payload`. SQLite owns durable cache preservation because `SQLiteProjectionStore` already persists projection snapshots across process boundaries. The seam requires both: durability without projection authority would be inert storage, while Python-only projection would not preserve reusable snapshot evidence.

## Before and after jurisdiction split

- **Before:** `projection_snapshots` preserved workspace, projection name/version, last event, state JSON, and creation time. Tests proved cache reuse, invalidation, and clear/rebuild, but the row did not explicitly carry that it was derived, preservation-only, read-model-only, and non-mutating.
- **After:** `ProjectionSnapshotBoundary` is attached to saved and loaded snapshots, and SQLite rows have columns for `artifact_standing`, `producer_boundary`, `occurrence_evidence_kind`, `consumer_limit`, and `mutates_cluster`.

## Python producer and responsibility

`project_state_with_cache` and `_save_state_snapshot` remain responsible for forming a projection snapshot from Python `State`. This is not a renewed constitutional act when the row is later loaded.

## Crossing artifact

The crossing artifact is `ProjectionSnapshot` plus `ProjectionSnapshotBoundary` with these default limits:

- `artifact_standing=derived_projection_snapshot`
- `producer_boundary=python_state_projection`
- `occurrence_evidence_kind=snapshot_preservation_only`
- `consumer_limit=read_model_cache_only`
- `mutates_cluster=false`

## SQLite preservation or retrieval responsibility

`SQLiteProjectionStore` creates/migrates the additional boundary columns, stores them during snapshot save, and restores them during snapshot load. SQLite preserves boundary labels; it does not perform projection, establish facts, certify warrant, or claim event occurrence.

## Python consumer

`project_state_with_cache` consumes a loaded snapshot only when projection version and last event match and the payload materializes. The consumer may reuse cached read-model state; it may not treat rehydration as renewed authority.

## Schema and query changes

Only `projection_snapshots` changed. No universal constitutional schema, ORM identity map, Book mirror, EAV store, or witness-table normalization was added.

## Standing-preservation answer

Persistence and rehydration preserve `derived_projection_snapshot` standing and do not strengthen it to established fact, source truth, warrant, or current cluster mutation.

## Occurrence-preservation answer

A row evidences snapshot preservation only. It does not claim the original projection act occurred anew, does not append ledger events, and does not fabricate event occurrence from row existence.

## Compatibility answer

Compatibility is preserved by default values and migration of existing `projection_snapshots` tables. In-memory projection store snapshots use the same Python boundary default without requiring SQLite.

## Tests executed

- `pytest -q tests/test_projection_store.py`
- `pytest -q tests/test_persistence.py`
- `./witnesses/sqlite_constitutional_witness_slice_001/run_verification.sh`
- `git diff --check`

## Remaining compression and Unknowns

- State JSON still compresses many projected dimensions into one payload.
- Event payload JSON still carries heterogeneous constitutional material.
- SQLite witness support binding remains report-only with no production Python consumer.
- Complete owner maps for all read models and diagnostics remain Unknown.
- The boundary does not solve universal occurrence-recording topology, fact establishment, or consumer uptake proof.
