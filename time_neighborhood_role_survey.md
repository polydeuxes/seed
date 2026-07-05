# Time Neighborhood Role Survey

## Survey boundary

This is exactly one bounded Survey of previously visible Time terrain. It increases local observational resolution by asking what role each surveyed Time neighborhood appears to perform according to recurring implementation evidence.

This survey does not recover bridges, topology, ownership, districts, competencies, runtime behavior, scheduling, physiology, implementation recommendations, slices, or the Town Clock. It does not compare neighborhoods. Repository authority wins.

## Neighborhood 1: Event preservation time

### Recurring implementation evidence

- `Event` carries a timezone-aware `timestamp` defaulted by `utc_now()` plus event identity, kind, actor, workspace, payload, session, causation, and correlation fields.
- `EventLedger.append()` creates an `Event` and stores it.
- `EventLedger.list()` returns stored events in append order, optionally scoped to a workspace.
- `EventLedger.extend()` / `append_many()` accept pre-built events while preserving the supplied event order and rejecting duplicate event IDs.
- `SQLiteEventLedger` persists event timestamp text in the `events` table and exposes the same public ledger shape.
- Temporal audits repeatedly characterize `Event.timestamp` as preservation time, not automatically occurrence time for external reality.

### Recurring implementation surfaces

- `seed_runtime/models.py`: `utc_now()` and `Event`.
- `seed_runtime/events.py`: `EventLedger`, `SQLiteEventLedger`, event append/list/extend behavior.
- `docs/temporal_reasoning_audit.md`: event timestamp and append-order characterization.
- `docs/time_provenance_and_temporal_authority_audit.md`: preservation-time distinction.
- `tests/test_temporal_characterization.py`: append-order and out-of-order timestamp characterization.

### Received artifacts

- Event kind, workspace ID, payload, actor, session/causation/correlation IDs, and optional externally constructed event objects.
- If the caller does not supply a timestamp, the event model receives a generated UTC timestamp.

### Locally performed work

- Constructs or accepts event records.
- Rejects duplicate event IDs.
- Stores events in append order and indexes them by ID and workspace.
- Persists timestamp-bearing events in SQLite when the SQLite ledger is used.

### Emitted artifacts

- Stored `Event` objects.
- Append-ordered event lists.
- Workspace-scoped event lists.

### Preserved artifacts

- Event IDs, kinds, payloads, actor/session/causation/correlation metadata, workspace scope, and event timestamps.
- Externally supplied event order when extending from caller-provided events.

### Observable local role

This neighborhood appears to preserve timestamped event records as ledger history and expose them in stored order, while treating event timestamp as event preservation metadata rather than proof of external occurrence time.

### Preserved unknowns

- Whether any event timestamp is authoritative occurrence time for an external condition remains unsupported locally.
- Whether preservation time should be further classified by clock authority remains not implemented here.
- Whether this neighborhood is central, infrastructural, or the Town Clock is not surveyed.

### Unsupported conclusions

- Event timestamp owns all Time semantics.
- Event timestamp orders projection input by clock time.
- Event persistence recovers external occurrence time.
- The ledger is a temporal database or historical as-of query surface.

### Confidence

High for append-order timestamped event preservation; low for any stronger temporal authority conclusion.

## Neighborhood 2: Observation time intake

### Recurring implementation evidence

- `Observation` requires `observed_at` and accepts optional `expires_at`, confidence, metadata, dimensions, source type, subject, predicate, and value.
- `ObservationIngestor.ingest_many()` iterates caller-provided observations and produces observation, evidence, and optional fact events for each observation.
- `observation_to_evidence()` and `observation_to_fact()` derive downstream artifacts from the observation while preserving observation provenance fields.
- Local host and Prometheus collectors capture Seed collection time as `observed_at` for produced observations.
- Manual CLI observations use ingestion-time UTC for `observed_at`.
- JSON observations can carry source-provided `observed_at`; otherwise they use the current JSON default behavior.

### Recurring implementation surfaces

- `seed_runtime/observations.py`: `Observation` and `ObservationIngestor`.
- `seed_runtime/observation_sources.py`: provider/local collection-time observation construction.
- `scripts/seed_local.py`: CLI observation ingestion and expiry handling.
- `docs/time_provenance_and_temporal_authority_audit.md`: local host, CLI, JSON, and Prometheus observation-time findings.
- `tests/test_observation_sources.py`: observation timestamp metadata and exported expiry coverage.

### Received artifacts

- Canonical observation records from user, discovery, provider, imported, or inferred sources.
- Source type, observed timestamp, optional expiry timestamp, subject, predicate, value, confidence, dimensions, and metadata.

### Locally performed work

- Validates observation confidence and secret-free observation data.
- Carries caller-supplied observation time into downstream evidence/fact construction.
- Emits one observation event per input observation during ingestion.
- Allows metadata to preserve collection/source context when collectors provide it.

### Emitted artifacts

- `observation.observed` events.
- Evidence records derived from observations.
- Optional fact records derived from observations when promotion is not suppressed.

### Preserved artifacts

- Observation `observed_at`, `expires_at`, source type, subject, predicate, value, confidence, metadata, and dimensions.
- Suppression metadata that can prevent fact promotion while still preserving the observation/evidence path.

### Observable local role

This neighborhood appears to receive time-stamped observations and preserve observation-time metadata while translating each observation into recordable observation/evidence/fact-shaped artifacts.

### Preserved unknowns

- Whether an observation timestamp is source-supplied, Seed-collected, defaulted, normalized, or operator-asserted is not consistently modeled.
- Whether an observation timestamp is occurrence time remains unsupported unless source evidence explicitly supports it.
- Prometheus sample time preservation remains an identified gap in the audited evidence.

### Unsupported conclusions

- Observation time is always occurrence time.
- Source clocks and Seed collection clocks are equivalent.
- Observation ingestion owns clock authority classification.
- Every observation should become cluster truth.

### Confidence

High for observation-time preservation and ingestion translation; medium for collector-specific authority classification because current implementation is uneven; low for occurrence-time claims.

## Neighborhood 3: Evidence provenance time

### Recurring implementation evidence

- `Evidence` carries `observed_at`, source, kind, payload, confidence, workspace ID, and evidence ID.
- `ObservationIngestor` creates evidence from observations and emits `evidence.observed` events.
- Temporal and representation audits repeatedly describe evidence as provenance payload with observed time and source context.
- Evidence graph/read-only surfaces use evidence/fact observation time as created-time style metadata.

### Recurring implementation surfaces

- `seed_runtime/evidence.py`: `Evidence` model.
- `seed_runtime/observations.py`: observation-to-evidence ingestion.
- `docs/temporal_reasoning_audit.md`: evidence timestamp inventory.
- `representation_contract_boundary_investigation.md`: evidence provenance contract.
- `docs/explainability_inventory_audit.md`: temporal metadata fit for evidence/support surfaces.

### Received artifacts

- Observation-derived payloads and provenance context.
- Source names, evidence kind, confidence, workspace scope, and observed timestamp.

### Locally performed work

- Represents a source payload as a timestamped provenance record.
- Carries observation-derived payload fields without making every payload field canonical fact truth.
- Supports later fact provenance by giving facts evidence IDs to cite.

### Emitted artifacts

- Evidence objects.
- `evidence.observed` event payloads.
- Evidence IDs that facts and read-only explanations can reference.

### Preserved artifacts

- Source, kind, payload, confidence, workspace ID, and observed timestamp.
- Payload-level observation fields, including temporal fields when included by the observation conversion path.

### Observable local role

This neighborhood appears to preserve timestamped provenance for observed source payloads so later state claims and explanations can cite what support was observed and when it was observed.

### Preserved unknowns

- Evidence time does not classify occurrence, knowledge, source-sample, or preservation authority by itself.
- Evidence payload preservation does not prove fact correctness.
- Evidence does not locally decide as-of semantics.

### Unsupported conclusions

- Evidence observed time is source occurrence time.
- Evidence payloads automatically become current truth.
- Evidence owns temporal reasoning, selection, or projection semantics.

### Confidence

High for timestamped provenance preservation; low for stronger temporal semantics.

## Neighborhood 4: Fact and support temporal qualification

### Recurring implementation evidence

- `Fact` carries `observed_at`, optional `expires_at`, confidence, source type, evidence IDs, dimensions, and inference metadata.
- `FactSupport` carries first/latest observed timestamps, expiry metadata, predicate semantics, and support kind.
- `is_fact_expired()` evaluates optional expiry against a comparison time, normalizing naive timestamps to UTC.
- Durable fact support aggregates support, while measurement fact support uses current-sample semantics.
- Current fact queries exclude expired facts by default unless `include_expired` is requested.

### Recurring implementation surfaces

- `seed_runtime/facts.py`: `Fact`, `FactSupport`, `is_fact_expired()`, measurement and stale capability metadata.
- `seed_runtime/state.py`: support selection, current fact queries, stale fact views.
- `docs/temporal_reasoning_audit.md`: fact/support timestamp and expiry characterization.
- `tests/test_fact_support_aggregation.py`: support timestamp/expiry behavior.
- `tests/test_temporal_characterization.py`: durable support/provenance, expiry filtering, and stale characterization.

### Received artifacts

- Fact claims with source type, observed timestamp, optional expiry, evidence IDs, dimensions, confidence, and inferred/source-fact metadata.
- Predicate metadata that can classify support as durable or measurement.

### Locally performed work

- Normalizes fact confidence according to source type defaults when needed.
- Evaluates expiry for current/stale filtering.
- Aggregates or selects support with observed/latest observed timestamps.
- Distinguishes aggregate support from current-sample support at the support-record level.

### Emitted artifacts

- Fact objects.
- Fact support records.
- Current fact lists and selected best facts through state query methods.
- Stale fact lists and deterministic stale-refresh recommendation records.

### Preserved artifacts

- Fact IDs, evidence links, source type, observed timestamp, expiry timestamp, dimensions, confidence, inferred/source metadata, and support temporal metadata.
- Expired facts remain stored in projected facts even when excluded from default current-support views.

### Observable local role

This neighborhood appears to qualify facts and fact support with observation and expiry time so current, stale, durable, and measurement-shaped support can be surfaced without deleting preserved fact records.

### Preserved unknowns

- Expiry does not prove a fact became false at the expiry timestamp.
- Latest support does not create an as-of timeline.
- Refresh recommendations do not prove an operational refresh occurred.

### Unsupported conclusions

- Fact support owns all current-state truth.
- Expired facts mutate into false facts.
- Fact timestamps supply complete temporal history.
- Stale refresh recommendation is scheduling or execution behavior.

### Confidence

High for fact/support temporal qualification and stale filtering; low for stronger historical or operational claims.

## Neighborhood 5: Projection replay and latest-current state

### Recurring implementation evidence

- `StateProjector.project()` builds `State` by reading ledger events for a workspace.
- `project_from_state()` materializes event input, sets `state.last_event_id` as each event is replayed, applies each event, and finalizes derived indexes.
- Temporal characterization says replay order is ledger append order, not event timestamp order.
- Current state is the result after every listed event for the workspace has been replayed.
- Tests cover append-order projection, out-of-order event timestamp non-reordering, and deterministic latest projection.

### Recurring implementation surfaces

- `seed_runtime/state.py`: `StateProjector.project()`, `project_from_state()`, `finalize()`.
- `seed_runtime/events.py`: append-ordered event lists supplied to projection.
- `docs/temporal_reasoning_audit.md`: projection replay and current-state characterization.
- `docs/state.md`: current-state temporal semantics.
- `tests/test_temporal_characterization.py`: projection ordering and determinism tests.

### Received artifacts

- Append-ordered ledger events for one workspace.
- Existing projected state only when caller invokes incremental projection with a supplied state and following events.
- Predicate, relationship, entity-type, and inference catalogs used during finalization.

### Locally performed work

- Replays event effects into a projected state.
- Records the last replayed event ID.
- Rebuilds derived indexes after event application.
- Finalizes visible latest-current projection outputs.

### Emitted artifacts

- A projected `State` object for the workspace.
- Derived indexes inside the state, including fact supports, conflicts, aliases, inferred/observed partitions, relationships, entity types, and graph issues.

### Preserved artifacts

- Ledger event order as replay input.
- `last_event_id` in the projected state.
- Durable facts and preserved projected records according to projection behavior.

### Observable local role

This neighborhood appears to rebuild latest-current inspectable state from ledger events by replaying stored events in ledger order and finalizing derived indexes.

### Preserved unknowns

- It does not expose a supported as-of event or as-of timestamp projection API.
- Event timestamps do not order replay locally.
- Projection output does not establish a complete semantic timeline.

### Unsupported conclusions

- Projection replay is clock-time ordering.
- Latest-current state is historical as-of state.
- Projection owns external occurrence chronology.
- Projection finalization identifies the Town Clock.

### Confidence

High for latest-current append-order projection; low for as-of or chronology conclusions.

## Neighborhood 6: Measurement latest-current retention

### Recurring implementation evidence

- Measurement predicates are recognized by predicate catalog metadata or legacy measurement predicate names.
- `FactSupport` documents measurement predicates as volatile samples with latest current sample support rather than strengthening repeated values.
- `StateProjector.finalize()` retains measurement history with `_retain_projected_measurement_history()` before and after inference.
- The default `measurement_history_limit` is 1 and must be at least 1.
- Tests characterize latest-current measurement selection by `Fact.observed_at`, debug history retention, and projection pruning without ledger deletion.

### Recurring implementation surfaces

- `seed_runtime/facts.py`: `MEASUREMENT_PREDICATES`, `is_measurement_predicate()`, `FactSupport` measurement semantics.
- `seed_runtime/state.py`: measurement history retention and projection finalization.
- `docs/temporal_reasoning_audit.md`: measurement temporal semantics.
- `tests/test_temporal_characterization.py`: measurement latest-current and debug-history tests.
- `tests/test_observation_sources.py`: provider measurement observation coverage.

### Received artifacts

- Measurement-shaped facts with subject, predicate, dimensions, value, observed timestamp, evidence IDs, and source metadata.
- A measurement history retention limit.

### Locally performed work

- Identifies measurement predicates.
- Retains only the configured number of projected samples per measurement key.
- Builds current-sample support records for measurement facts.
- Leaves ledger history outside projection pruning.

### Emitted artifacts

- Projected measurement facts retained under the configured history limit.
- Measurement `FactSupport` records with `support_kind="current_sample"`.
- Optional debug/read-only history when retention limit is increased by caller/test setup.

### Preserved artifacts

- The selected measurement sample's observed/latest observed timestamp, evidence links, dimensions, source type, and confidence.
- Ledger-retained measurement events, even when projection keeps fewer measurement facts.

### Observable local role

This neighborhood appears to preserve volatile measurement facts as latest-current projected samples while keeping projection retention separate from ledger preservation.

### Preserved unknowns

- Latest-current sample selection is not an as-of timeline.
- Projection pruning does not prove source samples were deleted from the ledger.
- Measurement recency does not classify source clock authority by itself.

### Unsupported conclusions

- Measurement support is durable aggregate truth.
- Measurement projection is a time-series database.
- Measurement latest-current behavior owns scheduling, polling, or runtime collection.

### Confidence

High for latest-current measurement projection; low for historical/time-series conclusions.

## Neighborhood 7: Expiry, stale views, and refresh recommendations

### Recurring implementation evidence

- `Fact.expires_at`, `FactSupport.expires_at`, `Approval.expires_at`, and `ExecutionAuthorization.expires_at` appear as optional expiry fields.
- `is_fact_expired()` checks fact expiry against wall-clock UTC unless a caller supplies comparison time.
- Default current fact/support queries exclude expired facts.
- `State.get_stale_facts()` returns expired facts sorted by expiry time and fact ID.
- `State.get_stale_fact_refresh_recommendations()` maps stale fact predicates to deterministic capability names and reasons.
- Temporal audits say stale views are read-only and do not mutate facts, lower confidence, or append refresh events.

### Recurring implementation surfaces

- `seed_runtime/facts.py`: expiry check and stale-refresh capability mapping.
- `seed_runtime/state.py`: stale fact and stale refresh recommendation methods; approval expiry checks.
- `seed_runtime/models.py`: approval and execution authorization expiry fields.
- `docs/temporal_reasoning_audit.md`: stale fact behavior.
- `tests/test_temporal_characterization.py`: stale fact filtering and recommendations.

### Received artifacts

- Facts/support/approvals/authorizations with optional expiry timestamps.
- Predicate names for stale fact recommendation mapping.
- Current comparison time, explicitly supplied or read from wall-clock UTC.

### Locally performed work

- Determines whether facts are expired for query filtering and stale reporting.
- Produces a sorted stale fact view.
- Produces deterministic recommendation records for stale facts.
- Filters expired approvals from approval lookup.

### Emitted artifacts

- Current fact/support query results that exclude expired facts by default.
- Stale fact lists.
- `StaleFactRefreshRecommendation` records.
- Approval lookup results that ignore expired approvals.

### Preserved artifacts

- Expired facts remain in projected facts unless measurement retention removes them from projection according to measurement rules.
- Expiry timestamps are preserved on fact/support records.
- Recommendation records preserve fact ID, subject, predicate, value, recommended capability, and reason.

### Observable local role

This neighborhood appears to expose expiry-based stale/current views and deterministic refresh hints while preserving expired artifacts as records rather than silently rewriting their truth value.

### Preserved unknowns

- Expiry does not establish when reality changed.
- Refresh hints do not execute or schedule refresh work.
- Wall-clock comparison can change read-time stale answers without ledger mutation.

### Unsupported conclusions

- Staleness equals falsity.
- Stale recommendations are operational scheduling.
- Expiry owns all temporal validity semantics.
- Approval expiry and fact expiry are one architectural authority.

### Confidence

High for expiry-filtered views and stale recommendations; low for operational or truth-transition conclusions.

## Neighborhood 8: Projection snapshot cache time

### Recurring implementation evidence

- `ProjectionSnapshot` carries workspace ID, projection name/version, `last_event_id`, `last_event_created_at`, serialized state payload, and `created_at`.
- `ProjectionStore` loads, saves, and clears latest projection snapshots by workspace/name/version.
- Temporal audits characterize `ProjectionStore` as a cache for one latest-current projection snapshot per workspace/projection/version.
- Cache validity is event-ID based, not timestamp based.
- Tests characterize latest-current cache behavior and that `ProjectionStore` does not change temporal semantics.

### Recurring implementation surfaces

- `seed_runtime/projection_store.py`: projection snapshot models and store protocol.
- `docs/temporal_reasoning_audit.md`: projection cache temporal role.
- `docs/context_composition_vocabulary.md`: projection cache language as current-state metadata.
- `tests/test_temporal_characterization.py`: projection store cache characterization.
- `tests/test_projection_store.py`: projection snapshot persistence behavior.

### Received artifacts

- Projected state payloads.
- Last event ID and last event timestamp metadata from the source projection.
- Snapshot creation time.
- Workspace/projection name/version keys.

### Locally performed work

- Stores reusable serialized latest-current state snapshots.
- Loads matching snapshots by exact projection version.
- Clears cached snapshots by workspace and optional projection name.

### Emitted artifacts

- Projection snapshots.
- Loaded serialized latest-current state payloads.
- Empty results when no exact matching snapshot exists.

### Preserved artifacts

- Snapshot `created_at`, `last_event_created_at`, `last_event_id`, projection name/version, workspace ID, and state payload.

### Observable local role

This neighborhood appears to preserve reusable latest-current projection snapshots with cache metadata, without changing projection temporal semantics.

### Preserved unknowns

- It does not store timelines, event ranges, historical projections, or as-of snapshots.
- Snapshot creation time does not become source observation time.
- Cache metadata does not identify clock authority beyond the stored fields.

### Unsupported conclusions

- Projection cache is a historical store.
- Snapshot timestamps determine truth ordering.
- Projection cache owns temporal reasoning.
- Projection cache is infrastructure in this survey's architectural sense.

### Confidence

High for latest-current projection snapshot caching; low for historical or ownership claims.

## Neighborhood 9: Temporal authority vocabulary and source-time preservation gap

### Recurring implementation evidence

- Temporal authority audit distinguishes occurrence, observation, knowledge, and preservation time.
- The same audit identifies timestamp authority categories such as Seed local clock, source sample clock, operator asserted time, imported document time, derived interval, and unknown as needed future distinctions.
- Prometheus observation code currently reads the sample value but, according to the audit, does not preserve or use the Prometheus sample timestamp as `Observation.observed_at`.
- Local host and Prometheus collection use Seed collection time for observations.
- JSON observations may preserve source-provided observed time, but source-time classification is not separately modeled.

### Recurring implementation surfaces

- `docs/time_provenance_and_temporal_authority_audit.md`: temporal authority findings and metadata gap.
- `seed_runtime/observation_sources.py`: local host, Prometheus, and imported observation construction surfaces.
- `scripts/seed_local.py`: CLI/manual observation timestamp handling.
- `docs/prometheus_observation_boundary_reconciliation.md`: Prometheus observation boundary context.
- `tests/test_observation_sources.py`: collection-time and observation metadata tests.

### Received artifacts

- Timestamps embedded in events, observations, evidence, facts, support, provider samples, local collections, CLI observations, and imported payloads.
- Source payloads that may contain a timestamp distinct from Seed collection or preservation time.

### Locally performed work

- Documents and preserves the distinction that timestamps have source, clock, scope, and meaning.
- Identifies current implementation places where source time is substituted, preserved, defaulted, or discarded.
- Preserves the unsupported status of full temporal authority modeling.

### Emitted artifacts

- Audit-level temporal authority vocabulary.
- Gap statements for source-time preservation and classification.
- Candidate metadata fields for future consideration, without implementing them.

### Preserved artifacts

- The distinction between occurrence, observation, knowledge, and preservation time.
- The unsupported status of a complete timestamp-authority model.
- The identified Prometheus sample timestamp preservation gap.

### Observable local role

This neighborhood appears to make timestamp authority visible as an audit/preservation concern: it names what kinds of time may be present, records where current implementation preserves or loses source-time evidence, and refuses to treat timestamps as self-authorizing.

### Preserved unknowns

- Which clock supplied every timestamp is not consistently represented in current implementation.
- Whether source clocks are trusted remains unknown unless specific metadata supports it.
- Whether future temporal authority fields should be implemented is not answered by this survey.

### Unsupported conclusions

- Temporal authority vocabulary is implemented as a runtime model.
- Source sample time is universally preserved.
- Seed can infer occurrence time from observation or preservation time alone.
- This audit neighborhood owns Time architecture.

### Confidence

High for the documented authority gap and vocabulary; medium for implementation-local coverage of all sources; low for any implemented authority model claim.

## Survey coverage

This survey covered the surveyed Time neighborhoods visible in recurring implementation and audit evidence: event preservation time, observation time intake, evidence provenance time, fact/support temporal qualification, projection replay/latest-current state, measurement latest-current retention, expiry/stale views, projection snapshot cache time, and temporal authority/source-time gap preservation.

## Remaining unknown neighborhoods

- Whether additional Time neighborhoods exist outside the reviewed implementation and documentation evidence remains unknown.
- Whether interaction-temporal documents constitute a Time neighborhood in the same surveyed sense remains unknown.
- Whether approval/authorization expiry deserves a separate neighborhood rather than appearing only inside expiry surfaces remains unknown.
- Whether imported/log/operator asserted time has enough recurring implementation evidence for separate neighborhood treatment remains unknown.

## Remaining observational gaps

- Clock authority is not consistently modeled for every timestamp.
- Occurrence time, observation time, knowledge time, and preservation time are not consistently separated in implementation fields.
- Prometheus sample timestamp preservation remains an audited gap.
- As-of event projection, as-of timestamp projection, belief timelines, why-then explanations, and semantic what-changed timelines remain unsupported.
- No surveyed evidence identifies a Town Clock, bridge, topology, owner, implementation recommendation, competency, or runtime schedule.

Survey complete.
