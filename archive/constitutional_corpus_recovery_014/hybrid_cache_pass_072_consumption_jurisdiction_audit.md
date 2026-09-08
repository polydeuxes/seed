# Hybrid cache pass 072 — Cache-consumption jurisdiction audit

Pass 072 audited Python consumption of SQLite-backed projection and read-model cache material. It made no runtime or schema change.

## Audited paths

| Path | Python producer | SQLite artifact | Boundary testimony | Python consumer | Current eligibility before pass 074 | Outcome / refusal | Tests |
| --- | --- | --- | --- | --- | --- | --- | --- |
| State projection snapshot full hit | `project_state_with_cache` / `_save_state_snapshot` | `projection_snapshots.state_json` | `artifact_standing`, `producer_boundary`, `occurrence_evidence_kind`, `consumer_limit`, `mutates_cluster` | `project_state_with_cache` materializes `state_from_payload` | Version and event horizon checked; boundary preserved but not consumer-governing | Hit if materializes and event matches; corrupt payload full rebuild | `tests/test_projection_store.py` |
| State projection incremental replay | same | same | same | `project_state_with_cache` starts from cached `State` then replays ledger tail | Version and event identity checked; inferred facts block incremental; boundary not yet governing | Incremental rebuild if last event is found | `tests/test_projection_store.py` |
| State stale / wrong version | same | same | same | same | Wrong version missed by store lookup; stale event misses hit and may incrementally replay | Miss, incremental, or full rebuild | `tests/test_projection_store.py` |
| Corrupted state payload | SQLite / memory store row | same | row boundary if SQLite | `state_from_payload` | Payload exception caught | Full rebuild | `tests/test_projection_store.py` |
| Legacy state snapshot | older `projection_snapshots` | row with migration defaults | defaulted boundary testimony | `load_snapshot` | Migration creates defaults | Compatibility cache use | `tests/test_projection_store.py` |
| Cache-status inspection | SQLite ledger/store inspection | `projection_snapshots` | available through `load_snapshot` | `format_state_cache_status_from_args` | Reports row/event match, does not replay | Hit/miss text; no rebuild | `tests/test_projection_store.py` |
| Summary snapshot | `projected_state_summary_from_args` | `state_summary_snapshots.summary_json` | before pass 074 only version/event source identity, no explicit source-boundary columns | CLI state-build summary consumer | Joined to matching state row but did not test state row boundary testimony or summary inheritance | Summary hit avoids state deserialization; miss rebuilds | `tests/test_projection_store.py`, `tests/test_seed_local_script.py` |
| Derived index snapshot | `seed_runtime.fact_index` and capability consumers | `derived_index_snapshots.index_json` | version/event source identity only | bounded fact-index/capability consumers | Joined to matching state row but no inherited source-boundary columns | Hit, stale miss, rebuild | `tests/test_fact_index.py`, capability tests |
| Schema migration | `SQLiteProjectionStore.__init__` | `projection_snapshots` boundary columns | default compatibility values | all loaders | state projection columns migrated; summary/index not yet | Compatibility | `tests/test_projection_store.py` |

## Distinctions recovered

- Row availability is not cache eligibility: a materializable `state_json` row can be stale, wrong-version, corrupt, or outside the consumer boundary.
- Preservation is not consumer authority: SQLite preserves boundary testimony but does not decide whether the current Python consumer can rely on it.
- Rehydration is not renewed projection authority: cache hit reconstructs a read-only `State`; it does not append ledger events or mutate cluster state.
- Derived read models cannot strengthen standing: summary and derived-index caches must remain no stronger than the state projection they consume.

## Unsupported topology

Before pass 074, unsupported or partially supported cases were: wrong producer boundary, strengthened artifact standing, widened consumer limit, mutation-bearing cache testimony, summary rows detached from source boundary, derived index rows detached from source boundary, and explicit legacy/default treatment for downstream summary rows.
