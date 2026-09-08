# Hybrid testimony pass 076 — State snapshot boundary-origin seam

Pass 076 consumes pass 075 and selects one smallest Python–SQLite seam: `projection_snapshots` boundary testimony origin as consumed by the Python state-cache and summary-cache eligibility decisions.

## Concrete paths

### New producer-recorded snapshot → consumer

`project_state_with_cache` replays ledger events, `_save_state_snapshot` constructs a `ProjectionSnapshot`, and `SQLiteProjectionStore.save_snapshot` persists explicit boundary values. Present testimony: derived projection standing, Python state projection producer boundary, snapshot-preservation-only occurrence, read-model-only consumer limit, non-mutating cache. The consumer needs these limits plus evidence that the values came from the responsible current producer or an explicit compatibility basis. Lawful result: eligible cache input.

### Legacy migrated snapshot → consumer

A legacy row predates boundary columns. Migration supplies compatibility values via `ALTER TABLE ... DEFAULT`. Present testimony after migration is value compatibility, not original producer occurrence. The inference is that the row is shaped like the current cache contract because migration supplied compatibility defaults. Compatibility acceptance must not strengthen standing into historical producer proof. Lawful result: eligible only under bounded compatibility; prior producer occurrence remains Unknown.

### Incompatible snapshot → rejection → rebuild → newly preserved snapshot

If a row carries incompatible standing, mutating boundary, wrong consumer limit, corrupted payload, or insufficient origin, Python treats it as a miss. Rebuild replays ledger evidence and saves a fresh snapshot. Rebuild changes the new artifact's testimony origin to current producer-recorded preservation but does not prove the rejected row's historical producer. Persistence records a new snapshot preservation occurrence only; it does not append ledger events or mutate cluster state. Lawful result: cache miss and rebuild.

### Summary read-model path

`state_summary_snapshots` depends on matching state projection row testimony. Summary consumption requires source testimony alignment; summary row existence is insufficient. If summary source origin does not match the state row origin, the lawful result is summary cache miss.

## Selected seam

The selected seam is **state projection snapshot boundary testimony origin** across Python dataclass construction, SQLite schema/migration persistence, and Python cache eligibility. It involves both Python (`ProjectionSnapshotBoundary`, eligibility predicate, rebuild behavior) and SQLite (`projection_snapshots` schema/migration/defaults and summary join). It does not select `derived_index_snapshots` merely for lacking columns.

## Lawful distinction needed

The implementation needs a local marker sufficient to distinguish producer-recorded current snapshots, migration-inferred compatibility, and unknown/admin-supplied values. The marker must affect real consumer eligibility. Producer-recorded and migration-inferred may both be eligible, but for different standing; unknown/admin-supplied matching strings must not be silently treated as producer occurrence.
