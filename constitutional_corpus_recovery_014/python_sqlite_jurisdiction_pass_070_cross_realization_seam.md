# Python–SQLite Jurisdiction Pass 070 — Cross-realization Seam Recovery

Repository authority wins. This pass consumes pass 069 and selects one concrete seam for pass 071.

## Candidate A — Python event append to durable SQLite event row

- **Producer / act:** `SQLiteEventLedger.append` creates a bounded `Event` and inserts it.
- **Before crossing:** Python `Event` with ID, kind, workspace, actor, timestamp, payload, and causation/correlation fields.
- **Standing before crossing:** runtime event assertion prepared for recording.
- **SQLite representation:** `events` row with serialized payload.
- **Consumer:** `list_events`, `StateProjector`, services reading event history.
- **Standing after crossing:** recorded event assertion; not fact truth, external occurrence proof, or warrant.
- **Authority added:** only durable recording occurrence for the event row.
- **Provenance/scope:** workspace and payload fields; actor/session/correlation where present.
- **Unknowns / negative authority:** payload dimensions remain local; row existence is not truth.
- **Read-only or mutation:** appending mutates ledger, not necessarily cluster state.
- **Lawful stop:** already has focused tests for durability, ordering, ID continuation, and projection.
- **Cross-examination:** risk remains payload compression, but selected pass did not find a missing producer/consumer handoff requiring schema change here.

## Candidate B — SQLite event history to Python projected State

- **Producer / act:** SQLite ledger preserves event rows; `StateProjector` replays them.
- **Before crossing:** durable rows ordered by insertion.
- **Standing before crossing:** recorded assertions.
- **Python representation:** `State` projection with entities, facts, evidence, observations, relationships, plans, approvals, and authorizations.
- **Consumer:** read models, services, CLI summaries.
- **Standing after crossing:** recoverable current projection under projection rules.
- **Authority added:** none beyond projection standing.
- **Unknowns / negative authority:** replay does not verify every event payload or source claim.
- **Read-only or mutation:** projection is read-only over ledger.
- **Lawful stop:** existing projection tests cover replay and cache invalidation.
- **Cross-examination:** not selected because the crossing already has a bounded consumer and the missing limit was narrower in cache preservation.

## Candidate C — Python projected State to SQLite projection snapshot and back

- **Producer / act:** `project_state_with_cache` asks `StateProjector` for a Python `State` and `_save_state_snapshot` serializes it.
- **Before crossing:** Python projected state, derived from event history.
- **Standing before crossing:** derived projection/read model, not source truth.
- **SQLite representation:** `projection_snapshots` row keyed by workspace and projection name/version, last event, state JSON, created time.
- **Consumer:** later `project_state_with_cache` load/materializes the row into Python state when current event boundary matches.
- **Standing after crossing:** reusable derived read-model cache only.
- **Authority added:** no truth, warrant, admission, fact establishment, renewed projection act, event occurrence, or cluster mutation authority.
- **Provenance/scope:** workspace, projection name/version, last event ID and timestamp.
- **Unknowns / negative authority:** row existence alone must not claim projection act occurrence or current truth; rehydration must not re-establish authority.
- **Read-only or mutation:** saving mutates cache storage; loading should not mutate ledger or cluster.
- **Lawful stop:** if last event/version mismatch or payload fails, rebuild instead of strengthening stale row.
- **Cross-examination:** selected because current implementation had a real Python producer, SQLite preservation boundary, Python consumer, and tests, but the durable row did not explicitly carry standing/occurrence/mutation limits.

## Candidate D — SQLite witness support binding to Python diagnostics

- **Producer / act:** witness SQL views classify represented evidence/provenance support.
- **Before crossing:** fixture-local SQL rows and query results.
- **Python representation:** none in production.
- **Consumer:** shell verification and reports.
- **Lawful stop:** not selected because there is no evidenced production Python consumer/producer boundary.

## Selected seam

Pass 071 selects **Python projected State → SQLite projection snapshot preservation → Python cache consumer**. It belongs across both realization districts because Python owns the projection act and typed state materialization, while SQLite owns durable/reusable preservation across process boundaries. Keeping it wholly in Python would lose durable cache evidence; keeping it wholly in SQLite would make SQL appear to own projection interpretation. The missing distinction is not that SQLite could store more data, but that the existing durable cache row needed to preserve its limited standing and occurrence boundary explicitly.
