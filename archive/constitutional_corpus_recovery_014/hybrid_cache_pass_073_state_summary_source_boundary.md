# Hybrid cache pass 073 — Derived read-model seam recovery

Pass 073 consumed the pass 072 audit and examined evidence-backed seams where SQLite-preserved material later becomes Python input.

## Candidate seams

### 1. State snapshot → Python `State`

- Upstream standing: derived projection snapshot.
- Boundary testimony: projection snapshot columns in `projection_snapshots`.
- Consumer prerequisites: state projection name/version, event horizon, read-model-only consumer limit, non-mutating standing.
- Consumer-local act: `project_state_with_cache` decides hit, incremental replay, or rebuild.
- Stop condition: wrong boundary, corrupt payload, stale/missing event, or wrong version must not be silently consumed.

This seam already had durable testimony from pass 071 but needed consumer enforcement.

### 2. State snapshot → summary read model

- Upstream standing: derived projection snapshot.
- Boundary testimony: state projection row plus summary row source identity (`state_projection_version`, `state_last_event_id`).
- Consumer prerequisites: operator summary cache may consume only a read-model-only, preservation-only, non-mutating Python state projection source.
- Consumer-local act: `load_summary_snapshot` must decide whether the summary row is eligible for operator-summary cache use.
- New standing: the summary row may have derived summary snapshot standing for operator summary cache use, but it does not gain fact, occurrence, ledger, or cluster standing.
- Stop condition: mismatched source boundary, widened source limit, mutation-bearing source or summary testimony, stale event, wrong version, or legacy ambiguity outside explicit defaults.

This is the selected seam because it materially involves SQLite preservation and a later Python consumer, and because the downstream artifact is a real read model rather than a mechanical copy of the projection row.

### 3. State snapshot → derived fact index

- Upstream standing: derived projection snapshot.
- Boundary testimony: state row plus derived-index state version/event columns.
- Consumer prerequisites: fact-index query can consume only a bounded source projection.
- Consumer-local act: fact-index builder/load path chooses hit or rebuild.
- Stop condition: stale source or detached source boundary.

This remains a downstream pressure after pass 074.

## Selected implementation boundary

Selected boundary: `projection_snapshots` source boundary + `state_summary_snapshots` inherited source-limit testimony + Python-owned `load_summary_snapshot` operator-summary cache eligibility.

The selected implementation is deliberately not a universal cache-boundary table and does not copy `ProjectionSnapshotBoundary` into every table. It adds only the source-limit fields required for the summary consumer to prove that its cached read model remains bounded by the source state projection.
