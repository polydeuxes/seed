# Executive Summary

Seed has an explicit but narrow temporal model today:

- The source of temporal history is the append-only `EventLedger` / `SQLiteEventLedger` event stream.
- Events have ledger timestamps and are listed in append order.
- Observations, evidence, facts, fact support, approvals, execution authorizations, projection snapshots, and several read-only views carry timestamps or expiry fields.
- `StateProjector` builds a latest-current `State` by replaying all events for a workspace in ledger append order.
- Current fact selection is not a full temporal reasoner. It is projection logic over the projected latest state, using predicate semantics, confidence, support count, inferred/observed status, `observed_at`, and fact id as deterministic tie-breakers depending on the query path.
- Measurement predicates have special latest-current behavior: projected state retains only the latest sample by `Fact.observed_at` plus fact id by default, while debug/read-only history can retain more samples by increasing `measurement_history_limit`.
- Durable facts are retained in projected state; conflicting durable single-cardinality values are not automatically deleted or resolved.
- Expired facts are still stored in projected `State.facts`, but default support/current/conflict queries exclude them. Staleness is a read-time expiry view plus deterministic refresh recommendations; it does not mutate facts, lower stored confidence, or append refresh events.
- `ProjectionStore` is a cache for one latest-current projection snapshot per workspace/projection name/version. It is invalidated by latest event id mismatch, not by timestamp comparison, and it does not store historical projections.

The main temporal gap is that Seed can answer "what is true now?" and "why now?" from the latest projection, but cannot answer as-of questions such as "what was true at event N?" or "what was true at timestamp T?" through a supported API or CLI. Because projection already replays ordered events deterministically, the smallest safe next step is documentation plus characterization tests that explicitly pin event-order/current-state behavior, out-of-order timestamp behavior, and measurement latest-current semantics before designing any read-only as-of projection helper.

# Current Temporal Model

## Timestamps that exist

Seed currently carries time in these places:

- `Event.timestamp`: defaults to timezone-aware UTC via `utc_now()` when an event model is created.
- `Observation.observed_at`: timestamp for the external observation.
- `Evidence.observed_at`: timestamp for a source payload supporting facts.
- `Fact.observed_at`: timestamp for the observation/fact claim.
- `Fact.expires_at`: optional fact expiry timestamp.
- `FactSupport.observed_at`: first observed timestamp for durable aggregate support, or current sample timestamp for measurements.
- `FactSupport.latest_observed_at`: latest observed timestamp for durable aggregate support, or current sample timestamp for measurements.
- `FactSupport.expires_at`: aggregate/support expiry metadata.
- `Approval.expires_at`: optional approval expiry checked against wall-clock UTC.
- `ExecutionAuthorization.expires_at`: authorization expiry, normalized from payload or event timestamp during projection.
- `ProjectionSnapshot.last_event_created_at`: timestamp of the latest event when the snapshot was produced.
- `ProjectionSnapshot.created_at`: timestamp when the snapshot was saved.
- Evidence graph nodes expose `created_at` from evidence/fact observation time in read-only views.

## Models that carry time

Temporal fields are first-class on core event, observation, evidence, and fact models:

- `Event` includes `timestamp`, causation, correlation, session, actor, workspace, and payload metadata.
- `Observation` includes `observed_at` and optional `expires_at`.
- `Evidence` includes `observed_at`.
- `Fact` includes `observed_at` and optional `expires_at`.
- `FactSupport` exposes aggregate/current-sample observation timestamps and expiry state.
- Projection cache snapshots include latest event time and snapshot creation time.

Derived projection dataclasses also carry fact observation time where relevant, such as projected relationships and alias edges. These are provenance timestamps, not projection-as-of timestamps.

## Events and historical order

`EventLedger` is append-only in memory: it stores events in a list, indexes by id, and returns events in append order. `SQLiteEventLedger` persists events in an `events` table and returns them ordered by SQLite `rowid`. Both ledgers preserve externally supplied event order in `extend()` and reject duplicate event ids.

The event timestamp is stored, but event listing and projection order are append order / row insertion order, not timestamp order.

## What is considered current state

Current state is the `State` returned by `StateProjector.project(workspace_id)` after replaying every event currently listed for the workspace and then building derived indexes:

- `state.last_event_id` is the id of the last replayed event.
- entities, observations, evidence, facts, needs, plans, tools, approvals, and authorizations reflect the latest projection after all events are applied.
- fact support, relationships, entity types, graph issues, aliases, and conflicts are derived from the projected facts.
- default queries exclude expired facts unless they expose an explicit `include_expired` option.

For facts specifically, current belief is determined by `State.get_fact_support()`, `State.get_best_fact()`, and `State.get_current_facts()` using predicate cardinality and support-ranking rules. Single-cardinality durable predicates have one current belief only when there is an unambiguous strongest support. Multi-cardinality predicates can have multiple current values.

## What is historical but retained

Historical data retained today:

- The event ledger retains all appended events.
- SQLite ledger persists event rows and payloads.
- Projected state retains durable fact objects, including competing durable values.
- Projected state retains observations and evidence for retained facts.
- Projected state retains action/plan/status current objects, but not every intermediate object version as separate projected records.
- Measurement fact history is retained in the ledger but pruned from default projected state; projected debug history can retain more samples by setting `measurement_history_limit` above 1.
- Expired facts remain in `state.facts` and are available through stale/read-only views and `include_expired` queries, unless they are measurement samples pruned out of the projection.

## What is cached

`ProjectionStore` caches serialized projected `State` snapshots, keyed by workspace id, projection name, and projection version. The cache stores:

- `last_event_id`
- `last_event_created_at`
- serialized latest-current `State`
- snapshot `created_at`

It does not cache event ranges, timelines, historical projections, or as-of snapshots.

# Event Ordering and Projection Semantics

## Does projection depend on event append order?

Yes. `StateProjector.project()` iterates through `ledger.list_events(workspace_id)` and applies events in that order. The in-memory ledger returns list order; SQLite returns `ORDER BY rowid`. Therefore event append order is the projection replay order.

Some projected fields are explicitly last-write-wins by append order:

- upserted entities are assigned into `state.entities[entity.id]`.
- observations/evidence/facts are assigned into maps by id.
- tool need status changes update the current `ToolNeed` object if the need already exists.
- pending action and action plan status events update the existing projected object.
- tool registration assigns by tool name.
- `state.last_event_id` becomes the id of the last replayed event.

## Does projection depend on event timestamp?

Projection replay order does not depend on event timestamp. However, projected current fact behavior can depend on `Fact.observed_at`, and fact payload normalization uses `event.timestamp` as a fallback if a fact/observation/evidence payload lacks its own observed timestamp.

Important distinctions:

- Event order determines which events are applied and in what mutation/update sequence.
- Fact/evidence/observation `observed_at` is provenance time and is used by support aggregation, latest-current measurement selection, and deterministic tie-breakers.
- `Event.timestamp` is not used to sort projection input.

## What happens if timestamps are out of order?

If event timestamps are out of order, projection still replays events in append order. For facts, out-of-order `Fact.observed_at` values can affect current belief selection independently of event append order:

- Measurement latest-current selection uses the maximum `(fact.observed_at, fact.id)` among retained measurement samples.
- Measurement projection pruning retains the newest samples by `(fact.observed_at, fact.id)`.
- Durable aggregate support records sort supporting facts by `(observed_at, id)` and expose first/latest observed timestamps.
- Durable `get_best_fact()` tie-breaking among facts in the selected support uses confidence, observed-vs-inferred status, `observed_at`, and fact id.

So an older appended measurement event with a newer `observed_at` can become the current measurement sample. Conversely, a later appended event with an older `observed_at` will not become latest-current for measurement predicates solely because it was appended later.

## Is latest-current based on event order, timestamp, fact timestamp, or projection logic?

It depends on the object type:

- Entity/tool/status-like objects: current value is mostly append-order last-write-wins into dictionaries or status updates.
- Durable facts: current belief is support-based projection logic. It considers confidence, support count, predicate cardinality, expiry filtering, inferred-vs-observed status for best fact selection, and `observed_at`/id tie-breakers inside selected support.
- Measurement facts: latest-current is based on projection logic over `Fact.observed_at` and fact id, not event append order.
- Expired facts: default current queries filter them out based on `Fact.expires_at` compared to wall-clock now.
- Projection cache validity: latest-current cache reuse is based on latest event id matching the snapshot, not timestamps.

## Is behavior deterministic?

Within a fixed ledger event order, fixed wall-clock for expiry comparisons, fixed catalogs, and fixed measurement history limit, projection behavior is deterministic. Tests already assert deterministic projection rebuilds and deterministic contradiction/measurement characterization. Expiry checks depend on current wall-clock time unless callers pass a fixed `now` to lower-level `is_fact_expired()`.

# Current vs Historical Facts

## How does Seed decide the current value of a fact?

Seed does not rewrite `state.facts` into one fact per predicate. Instead, it projects facts and derives support groups:

1. `State.get_fact_supports()` groups facts by subject, predicate, dimensions, and value for durable predicates.
2. Expired facts are excluded by default.
3. Measurement predicates group without value as a competing dimension, because repeated samples are a time series rather than durable contradictions.
4. `State.get_fact_support()` selects an unambiguous strongest support using support tie keys.
5. `State.get_best_fact()` chooses a representative fact from the selected support using confidence, observed-vs-inferred status, observed time, and fact id.
6. `State.get_current_facts()` returns one best fact for single-cardinality predicates or all current supported values for multi-cardinality predicates.

Single-cardinality durable conflicts with equal support remain ambiguous: Seed reports competing beliefs/conflicts rather than arbitrating truth automatically.

## Are old facts retained?

Durable old facts are retained in projected state. Competing durable values and duplicate support facts remain in `state.facts`, subject to the same expiry filtering in read APIs.

Measurement old facts are retained in the append-only event ledger, but default projected state keeps only the latest sample per measurement series. Debug/read-only projections can retain more measurement samples by increasing `measurement_history_limit`.

## Are old supports retained?

Fact supports are a projected current aggregate view, not an append-only support history. For durable facts, support groups contain all projected, non-expired supporting facts for a claim. For measurements, support records identify the current sample. Prior measurement support records are not retained in default projection; debug history can show prior samples as separate sample support records in CLI `--fact-support --include-history` because the CLI increases measurement history retention for that projection.

## Are overwritten values retained anywhere?

For durable facts with different fact ids, overwritten or competing values remain in `state.facts`, supports, and conflicts. For status-like objects updated in place by lifecycle events, prior statuses are retained only in the event ledger, not as separate projected versions. For a map assignment using the same id/name key, projection keeps the latest assigned object in state and prior versions are retained only in events.

## Are measurement histories retained?

Yes in the event ledger. In projected state:

- default projection retains one latest sample per measurement series.
- debug/history projection retains up to `measurement_history_limit` samples per series.
- CLI `--fact-support --include-history` sets the history limit to the number of workspace events, effectively retaining all projected measurement samples for that read.
- pruned measurement evidence/observations are removed from projected state, while the ledger remains untouched.

## Are debug histories retained?

Debug histories are retained only for that projection invocation when `measurement_history_limit` is increased. They are not a distinct durable timeline store.

## Difference between durable facts and measurements

Durable facts represent claims that can accumulate support and conflict with other single-cardinality values. Measurement facts represent volatile samples/time series. The predicate catalog marks canonical predicates as `durable_fact` or `measurement`, and a legacy measurement predicate set remains for raw/provider predicates.

Durable facts use aggregate support. Measurement facts use current-sample support, newest sample selection by observed time, and no durable fact-conflict detection among retained samples.

# Measurement Temporal Semantics

Measurement temporal behavior is Seed's strongest existing temporal special case:

- Measurement predicates are identified from predicate catalog metadata plus legacy predicate names.
- Projection retains measurement samples per canonical subject, predicate, and dimensions.
- The default `measurement_history_limit` is 1.
- Retention sorts samples by `(observed_at, id)` descending and keeps the configured limit.
- Fact support for measurements reports one `current_sample` support whose value/confidence/timestamps come from the latest sample by `(observed_at, id)`.
- Fact conflicts skip measurement predicates because retained samples are treated as history/time-series data, not competing durable claims.
- CLI fact support hides prior measurement samples by default and tells the operator to use `--include-history` when history is present in that projection.

This is latest-current sample handling, not a general time-series query engine. There is no supported query for "measurement value at timestamp T" or "measurement changed from A to B at event N."

# Staleness and Expiration

## What does stale mean today?

A stale fact is a projected fact whose `Fact.expires_at` is not `None` and is less than or equal to the current comparison time. `is_fact_expired()` normalizes naive timestamps to UTC for comparison. `State.get_stale_facts()` returns expired facts from projected state sorted by expiry time and fact id.

## Does stale remove a fact?

No for durable facts retained in projected state. Expired durable facts remain in `state.facts`, but default support, current-fact, best-fact, and conflict queries exclude them unless `include_expired=True` is requested where supported.

For measurement facts, expiry is not the only pruning mechanism. Old measurement samples can disappear from projected state due to measurement history pruning even if they are not expired. Those samples remain in the ledger.

## Does stale lower confidence?

No. Fact confidence is not rewritten when a fact expires. Expired facts are filtered out of default support/current/conflict views instead of receiving lower confidence.

## Does stale create recommendations?

Yes as a read-only deterministic view. `State.get_stale_fact_refresh_recommendations()` maps each stale projected fact's predicate to a capability using `recommended_capability_for_stale_fact()`, with a fallback capability of `knowledge_lookup`. This does not create tool needs, append events, execute providers, or mutate state.

## Is stale part of current projection or a separate read-only view?

Both in a limited sense:

- Expired facts remain part of projected `State.facts` when not otherwise pruned.
- Stale fact lists and refresh recommendations are read-only methods derived from current projection and wall-clock expiry checks.
- Default support/current/conflict views treat stale facts as non-current by filtering them out.

# Existing Temporal Query Coverage

| Question | Current coverage | Notes |
| --- | --- | --- |
| What is true now? | Already implemented | Latest projection plus current fact/best fact/state summary views answer current state with expiry filtering. |
| Why does Seed believe X now? | Already implemented | `ExplanationBuilder.why()` explains current/ambiguous beliefs from projected state, including support facts and conflicts. |
| What evidence supports X? | Already implemented | Evidence graph and why-fact views traverse projected fact evidence. |
| What conflicts with X? | Already implemented for current projection | Fact conflicts and explanation competing beliefs expose projected active conflicts. Expired facts require include-expired paths where available. |
| What changed recently? | Partially implemented | Event listing and runtime trace views show ordered historical events/runs, but there is no semantic state diff or fact timeline query. |
| When did X become true? | Missing | Support timestamps expose first/latest observation among current support, but Seed does not compute lifecycle transitions. |
| When did X stop being true? | Missing | There is expiry visibility and event history, but no fact lifecycle/tombstone/supersession timeline. |
| What was true at event N? | Missing | A caller could manually replay a prefix in custom code, but no supported read-only API/CLI exists. |
| What was true at timestamp T? | Missing | Projection does not order or filter by timestamp, and no timestamp-as-of query exists. |

CLI read-only paths currently include current state summary/views, current facts, best fact, fact support, explanation/why, evidence, contradictions, confidence, stale facts, stale refresh recommendations, events listing, and historical runtime trace/why-run for recorded traces. None of these are as-of projection interfaces.

# ProjectionStore Temporal Role

## Does ProjectionStore store historical projections or only latest-current snapshots?

Only latest-current snapshots. Both in-memory and SQLite stores are keyed by `(workspace_id, projection_name)`, and the SQLite schema has one primary key row per workspace/projection name. Version filtering is used on load, but saving uses upsert semantics for the same key.

## How does cache invalidation work?

`project_state_with_cache()` finds the current latest event by taking the final event returned by `ledger.list_events(workspace_id)`. It loads a snapshot for the workspace/projection/version and reuses it only if `snapshot.last_event_id == current_last_event_id`. Otherwise, it rebuilds projection and replaces the snapshot.

`last_event_created_at` is stored as metadata but is not used for invalidation. Snapshot `created_at` is also metadata.

## Does ProjectionStore change temporal semantics?

No. It is an optimization around `StateProjector`. A cache hit returns a serialized/deserialized latest-current `State`; a miss calls the projector and saves that result. It does not reorder events, filter events by time, or create as-of semantics.

One caveat: because staleness/approval checks are wall-clock based in state methods, a cached projected state can contain the same facts while read-time expiry calculations may produce different stale/current answers as time passes. The cache stores facts and supports as serialized state; cache validity is event-id based, not wall-clock-expiry based.

## Does it preserve or erase historical information?

ProjectionStore preserves only the information included in the serialized latest projection. It erases/prunes anything not in that projection snapshot, such as default-pruned measurement samples. The authoritative historical information remains in EventLedger/SQLiteEventLedger, not in ProjectionStore.

# Missing Concepts

| Concept | Classification | Rationale |
| --- | --- | --- |
| Current belief | Already implemented | `get_fact_support`, `get_best_fact`, `get_current_facts`, explanations, conflicts, and state views operate on latest projection. |
| Historical event retention | Already implemented | Event ledgers retain append-only events; SQLite persists rows and returns append order. |
| As-of event projection | Missing | No API/CLI to project a prefix ending at event id/N. |
| As-of timestamp projection | Missing | No API/CLI to project events up to a timestamp, and projection order is not timestamp order. |
| Fact lifecycle | Partially implemented | Facts have observed/expiry times and durable conflicts, but no lifecycle states such as active/superseded/retracted/tombstoned. |
| Belief timeline | Missing | No timeline of current belief transitions, ambiguity intervals, or confidence/support changes. |
| Measurement timeline | Partially implemented | Ledger retains all samples and debug projection can retain sample history; no first-class timeline/as-of query. |
| Stale fact handling | Already implemented | Expiry check, stale fact list, include-expired query options, and refresh recommendations exist. |
| Supersession | Partially implemented | Action plans have explicit superseded status; facts do not have supersession semantics. |
| Invalidation | Partially implemented | Projection cache invalidates by latest event id/version; facts are not invalidated except expiry filtering/read-only stale views. |
| Confidence over time | Missing | Current confidence/support is computed for latest projection only; no confidence timeline. |
| Why-now | Already implemented | ExplanationBuilder explains current/ambiguous projected belief and support. |
| Why-then | Missing | No as-of projection or historical explanation query. |
| What-changed | Partially implemented | Ordered event lists/traces exist, but no semantic diff/timeline inventory. |
| Temporal conflict explanation | Partially implemented | Current conflicts are explained; conflicts over time or conflict start/end are not modeled. |

# Recommended Smallest Next Step

The smallest safe next step is to add characterization tests only, not new behavior:

1. Pin that projection replay is event-append-order based, not event-timestamp based, for update/status-like objects and `state.last_event_id`.
2. Pin that measurement latest-current selection is based on `Fact.observed_at` plus fact id, not event append order.
3. Pin that durable current belief remains support/confidence based and does not treat later event timestamp as automatic truth.
4. Pin that ProjectionStore cache invalidation is latest-event-id/version based, not timestamp based.
5. Optionally add an `docs/as_of_projection_design.md` or a section in a future audit describing a read-only as-of-event projection helper design, but do not implement it yet.

This is intentionally smaller and safer than implementing an as-of projection API. It documents and locks down current semantics first, reducing the risk that future temporal work accidentally changes Runtime, ToolExecutor, StateProjector behavior, ProjectionStore ownership, or fact arbitration semantics.
