# Hybrid cache pass 074 — State-summary source boundary

## Selected path and consumer

Selected path: Python state projection → SQLite `projection_snapshots` boundary testimony → SQLite `state_summary_snapshots` source-limit testimony → Python `load_summary_snapshot` operator-summary cache consumer.

Selected consumer: `SQLiteProjectionStore.load_summary_snapshot` as used by state-build summary cache consumers.

## Before and after jurisdiction split

Before pass 074, a summary cache row was eligible when its projection name/version and source state version/event matched a state snapshot row. The consumer did not check whether the source projection row still testified to derived projection snapshot standing, Python state projection producer boundary, preservation-only occurrence evidence, read-model-only consumer limit, and non-mutating behavior.

After pass 074, SQLite preserves both the state projection boundary and summary source-limit testimony, while Python owns the eligibility decision. The row is eligible only when the state row has the expected bounded boundary, the summary row records matching inherited source limits, the summary artifact remains `derived_summary_snapshot`, the summary consumer limit is `operator_summary_cache_only`, and neither source nor summary testimony is mutation-bearing.

## SQLite-preserved testimony

`state_summary_snapshots` now preserves:

- `artifact_standing=derived_summary_snapshot`
- `source_artifact_standing=derived_projection_snapshot`
- `source_producer_boundary=python_state_projection`
- `source_occurrence_evidence_kind=snapshot_preservation_only`
- `source_consumer_limit=read_model_cache_only`
- `consumer_limit=operator_summary_cache_only`
- `mutates_cluster=0`

Legacy summary rows receive explicit compatibility defaults during migration.

## Python-owned eligibility decision

`load_summary_snapshot` joins the summary row to the source state row and admits the cache only when the source row and summary row jointly satisfy the operator-summary cache contract. Ineligible rows become cache misses rather than new constitutional claims.

## Answers

- Eligible standing: derived summary snapshot for operator summary cache use.
- Lawful rejection standing: cache miss / rebuild path; no proof of malice or corruption beyond the failed boundary.
- Schema changes: bounded columns added only to `state_summary_snapshots`.
- Compatibility answer: existing valid cache-hit, stale-cache, incremental-replay, and full-rebuild state behavior remains compatible.
- Legacy-row answer: old summary rows migrate to explicit compatibility testimony and remain eligible only under the same joined checks.
- Occurrence answer: summary rows inherit snapshot-preservation-only limits and do not claim renewed occurrence.
- Ledger and mutation answer: rejection and rehydration do not append ledger events and do not mutate cluster state.

## Changed files and symbols

- `seed_runtime/projection_store.py`: `SummarySnapshotBoundary`, summary snapshot boundary fields, summary migration, summary save/load SQL checks, and projection snapshot eligibility helper.
- `tests/test_projection_store.py`: added behavioral tests for incompatible projection boundaries, strengthened standing, widened consumer limits, mutation-bearing testimony, summary source-limit preservation/rejection, and legacy summary compatibility.

## Remaining pressures

- Downstream compression remains for `derived_index_snapshots` source-limit preservation.
- Python-only pressures remain in complete consumer contracts and status/rejection reason reporting.
- SQLite-only pressures remain unsupported because SQLite still must not interpret projection authority.
- Cross-realization Unknowns remain for complete owner maps, all read models, diagnostic recording topologies, and witness-to-runtime production consumers.

## Tests executed

Recorded in the final response for this implementation pass.
