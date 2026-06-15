# Current Implementation Audit: Execution, Observation, Projection, Cache, Index, and Capability Inspection

Date: 2026-06-15

## Scope and method

This is an audit-only repository evidence review. It does not implement fixes, alter behavior, or propose remediation. Evidence came from direct source and test review plus targeted test execution.

Pull status: the repository has no configured `origin` remote in this checkout, so `git fetch origin main` / `git pull --ff-only origin main` could not complete. The audit therefore reflects the current local branch contents.

## Evidence reviewed

Primary implementation files reviewed:

- `seed_runtime/execution_status.py`
- `seed_runtime/observations.py`
- `seed_runtime/observation_sources.py`
- `seed_runtime/state.py`
- `seed_runtime/projection_store.py`
- `seed_runtime/fact_index.py`
- `seed_runtime/state_views.py`
- `seed_runtime/state_summary_views.py`
- `seed_runtime/capability_candidates.py`
- `seed_runtime/capability_inventory.py`
- `seed_runtime/capability_verification.py`
- `seed_runtime/verification_evidence.py`
- `seed_runtime/capability_promotion_readiness.py`

Representative tests reviewed and/or executed:

- `tests/test_execution_status.py`
- `tests/test_observations.py`
- `tests/test_observation_sources.py`
- `tests/test_state_projector.py`
- `tests/test_projection_store.py`
- `tests/test_fact_index.py`
- `tests/test_state_views.py`
- `tests/test_state_summary_views.py`
- `tests/test_capability_candidates.py`
- `tests/test_capability_inventory.py`
- `tests/test_capability_verification_inspection.py`
- `tests/test_verification_evidence.py`
- `tests/test_capability_promotion_readiness.py`

## Evidence classification

### Measured findings

- Targeted audit tests passed locally: `python -m pytest tests/test_execution_status.py tests/test_observations.py tests/test_observation_sources.py tests/test_state_projector.py tests/test_projection_store.py tests/test_fact_index.py tests/test_state_views.py tests/test_state_summary_views.py tests/test_capability_candidates.py tests/test_capability_inventory.py tests/test_capability_verification_inspection.py tests/test_verification_evidence.py tests/test_capability_promotion_readiness.py`.
- LOC changed by this task: one new audit document, no implementation files modified.

### Repository-supported findings

1. Execution status currently owns transient operator-visible activity status only. It defines `ExecutionStatus`, consumer types, CLI rendering, progress cadence, and observation producer lifecycle messages. Its documentation explicitly says it does not define observation semantics, create observations, append events, or derive facts.
2. Observation ingestion currently owns conversion of `Observation` objects into observation events, evidence events, and optional fact events. It appends these in ledger batches while preserving per-observation event ordering.
3. Observation sources currently own collection/adaptation of external or repository information into `Observation` objects and are documented as unaware of ledger, projection, and ingestion internals.
4. Projection construction currently belongs to `StateProjector`: it reads ledger events, applies supported event kinds into `State`, and rebuilds derived projection indexes in `finalize`.
5. Projection replay with cache currently belongs to `project_state_with_cache`: it loads compatible snapshots, returns exact hits, performs incremental replay when snapshot conditions allow, otherwise performs full replay and saves a snapshot.
6. Cache authority is separated from event authority in documentation: event ledgers own append-only history; projection stores own reusable snapshots derived from events.
7. State-summary snapshots and fact-index snapshots are dependent caches keyed by state projection version and state last event id, and the SQLite store joins them back to the state projection snapshot before returning them.
8. Derived fact indexes currently own exact subject/predicate read-model lookup acceleration from already-projected state. They are explicitly not event authority, projection authority, fact mutation, observation creation, or view cache.
9. Capability inspection surfaces are read-only and layered: candidate inspection preserves evidence-derived package candidates; verification evidence acquisition checks local PATH metadata without running binaries; verification inspection joins candidates to existing capability inventory; promotion-readiness inspection joins candidates to verification evidence without creating facts.
10. Capability verification inventory derives status from projected `capability_verified` facts and fact support. Missing verification facts yield `unverified`; expired verification facts yield `stale`.

### Implementation observations

- Coupling exists between projection cache logic and projection semantics through serialized `State` payloads. `project_state_with_cache` uses `state_from_payload` and `state_to_payload`, then delegates event application to `StateProjector` when replay is required.
- Incremental replay is conditional. The implementation only takes the incremental path when a snapshot deserializes, has no `inferred_facts`, the snapshot event id is found in the current event list, and the projector supports `project_from_state`.
- `StateProjector.apply` updates relationships immediately for fact events, while `finalize` later rebuilds alias resolution, inferred facts, retained measurement history, supports, relationships, entity types, graph issues, aliases, and conflicts. This is duplicated computation in the implementation shape, but the repository evidence reviewed does not by itself prove a correctness problem.
- Capability candidate inspection may use `DerivedFactIndex` when supplied; otherwise it scans `state.facts` directly for `package_installed`. The index is therefore an optional read acceleration/input surface, not the only source of candidate evidence.
- Verification evidence acquisition uses repository-defined candidate-to-binary mappings and filesystem metadata from PATH. It does not append events, create observations, create facts, evaluate policy, or execute binaries.
- State summary contains presentation-only classifications and boundary notes for areas such as filesystem categories, shared-storage candidates, and topology ambiguity. These are implementation-level read-model semantics, not fact authority by themselves.

### Hypotheses preserved separately

The following remain hypotheses/operator concerns, not findings from this audit:

- Recent changes caused boundary drift.
- Projection caching caused stale or incorrect read-model visibility.
- State-summary caching caused stale or incorrect read-model visibility.
- Derived indexes caused responsibility drift or correctness drift.
- Execution status caused lifecycle semantics to move into status reporting.
- Capability candidate, verification, evidence acquisition, or promotion-readiness surfaces are being used as execution authority.
- Performance regressions exist or do not exist.
- Status regressions exist or do not exist.

## Area-by-area current implementation shape

### Execution status

What exists:

- Renderer-independent status records, consumers, CLI rendering, bounded progress cadence, and observation producer lifecycle phase helpers.

Authority boundaries:

- Status consumers observe transient status. They do not own execution state.
- Observation lifecycle helpers emit vocabulary for collection, normalization, ingestion, and completion only.

Documented assumptions:

- Execution status is non-authoritative activity visibility.
- Observation producer lifecycle does not define observation semantics, create observations, append events, or derive facts.

Implementation-only assumptions:

- Progress cadence thresholds are local implementation choices.
- Phase names are stable by convention in tests and call sites, but this audit did not find a central phase registry.

Proven by tests:

- Targeted execution-status tests pass, proving the tested transient behavior and consumer semantics under test fixtures.

Inferred but not proven:

- All operator-visible long-running paths consistently use the status vocabulary. This was not exhaustively proven.

### Observation ingestion and sources

What exists:

- `Observation` validation, `ObservationIngestor`, observation-to-evidence conversion, observation-to-fact conversion, optional suppression for a Prometheus `node_uname_info` OS fact promotion case, and observation source adapters.

Authority boundaries:

- Sources collect observations and remain unaware of ledger/projection/fact-ingestion internals.
- Ingestion appends ledger events and performs conversion to evidence/facts.
- Projection later interprets appended events into state.

Documented assumptions:

- Ingestion batches persistence only; each observation still produces its own observation/evidence/optional fact events in repeated-ingest order.
- Sources expose stable identity and provenance type while not owning ledger/projector internals.

Implementation-only assumptions:

- The Prometheus-specific suppression rule is encoded in ingestion implementation. This audit did not find a broad policy document for that exact exception in the reviewed scope.

Proven by tests:

- Targeted observation and source tests pass for current fixtures.

Inferred but not proven:

- Every observation source preserves the same boundary equally; only representative files/tests were reviewed.

### Projection construction and replay

What exists:

- `StateProjector.project` starts from empty `State` and replays ledger events.
- `StateProjector.project_from_state` applies later events to a supplied snapshot state and then finalizes.
- `StateProjector.apply` handles entity, observation, evidence, fact, goal, tool need, approval, authorization, proposal, handoff, pending action, action plan, and tool registration event kinds.
- `finalize` rebuilds derived projection indexes after event application.

Authority boundaries:

- Ledger event history is documented as authority for incremental projection.
- Projection produces inspectable state and derived projection indexes.

Documented assumptions:

- Incremental projection reuses derived state only as an optimization and requires events after the snapshot in ledger order.

Implementation-only assumptions:

- Unknown event kinds are ignored by falling through `apply` without an error.
- The implementation uses current wall-clock time during execution authorization projection to mark proposals executable when non-expired; this audit did not classify whether that is intended architecture or a known temporal behavior.

Proven by tests:

- Targeted projector and projection-store tests pass for current fixtures.

Inferred but not proven:

- Full replay and incremental replay are equivalent for all possible event histories. Existing targeted tests support this in covered cases but do not exhaustively prove it.

### Caches and cache usage

What exists:

- In-memory and SQLite projection stores for state snapshots, state-summary snapshots, and derived fact-index snapshots.
- State projection cache load/save, exact cache hit return, incremental replay, full replay, and cache rebuild.

Authority boundaries:

- Caches own reusable snapshots, not event history.
- Dependent summary/index snapshots must match state projection version and state last event id.

Documented assumptions:

- Projection stores are derived from event ledgers.
- Summary snapshots are dependent read-model snapshots derived from a valid state snapshot.
- Derived index snapshots are for matching state projections.

Implementation-only assumptions:

- Exceptions while loading state snapshots are swallowed and treated as misses.
- Incremental replay is disabled when the snapshot already contains inferred facts.

Proven by tests:

- Targeted projection-store and fact-index tests pass for current fixtures.

Inferred but not proven:

- Cache invalidation is sufficient across every schema/semantic evolution. Version constants support invalidation but do not prove all future changes will update them.

### Derived indexes and read models

What exists:

- `DerivedFactIndex` maps subject/predicate to fact ids from projected `FactSupport` subjects.
- State views build deterministic read-only views from already-built state.
- State-summary helpers aggregate operator-facing summary semantics from projected state.

Authority boundaries:

- Derived indexes and views read projected state. They do not create observations, mutate facts, or append events.

Documented assumptions:

- The fact index is cacheable and is not event authority, projection authority, fact mutation, observation creation, or a view cache.
- State views are deterministic projections of an already-built `State` and do not query the ledger or decide business semantics.

Implementation-only assumptions:

- Some summary classifications are embedded directly in helper functions rather than external catalogs.

Proven by tests:

- Targeted state-view, state-summary, and fact-index tests pass for current fixtures.

Inferred but not proven:

- All read models have explicit documentation for each classification decision. The audit found explicit boundary text in some areas, but not a single complete authority map.

### Capability inspection surfaces

What exists:

- Capability candidates from `package_installed` facts.
- Capability inventory from projected tools, tool needs, and `capability_verified` facts.
- Verification evidence acquisition from PATH executable metadata.
- Verification inspection joining candidates, inventory, and acquired verification evidence.
- Promotion-readiness inspection joining candidate support and verification evidence.

Authority boundaries:

- Candidate is not capability proof, permission, selection, policy evaluation, planning, or execution.
- Verification evidence is not verification, selection, permission, policy approval, planning, or tool invocation.
- Verification inspection derives status from existing inventory/facts only.
- Promotion readiness does not create `capability_verified` facts or execute anything.

Documented assumptions:

- Missing `capability_verified` facts produce unverified inventory entries.
- Expired verification facts produce stale entries.

Implementation-only assumptions:

- Candidate mappings from package names to capability names and verification mappings from capabilities to binary names are encoded in module constants.

Proven by tests:

- Targeted capability candidate, inventory, verification inspection, verification evidence, and promotion-readiness tests pass for current fixtures.

Inferred but not proven:

- No CLI or runtime path treats these inspection outputs as authority. Tests reviewed assert read-only behavior for many surfaces, but this audit did not exhaustively trace every consumer.

## Responsibility and coupling summary

### Where responsibilities currently exist

- Execution status: transient visibility and progress/status vocabulary.
- Observation sources: collect/adapt external or repository evidence into observations.
- Observation ingestion: convert observations to evidence/facts and append events.
- Projection construction: replay ledger events into state and rebuild derived projection structures.
- Projection cache: persist/load reusable state snapshots and dependent summary/index snapshots.
- Derived indexes: accelerate read-only fact lookup from projected state.
- Read models: deterministic views and summaries over already-projected state.
- Capability inspection: read-only preservation, evidence acquisition, verification interpretation, and promotion-readiness explanation.

### Where coupling currently exists

- Observation lifecycle status is coupled to observation producer phase names but not to observation semantics.
- Observation ingestion is coupled to event kinds and fact/evidence schema.
- Projection cache is coupled to state serialization/deserialization shape.
- State projector is coupled to event-kind payload schemas and derived projection helpers.
- Derived fact index is coupled to `State.fact_supports` and `State.get_current_facts` semantics.
- Capability candidates are coupled to package-installed facts and optional fact-index lookup.
- Verification and promotion-readiness inspections are coupled to capability candidates and verification evidence acquisition.

### Duplicated, ambiguous, or undocumented responsibilities

- Duplicated computation: relationship projections are updated during fact event application and rebuilt during finalization. This is an implementation observation, not a finding of incorrectness.
- Ambiguous authority surface: state-summary helper classifications include careful boundary text, but the repository evidence reviewed does not provide a single central authority matrix for all summary classifications.
- Undocumented implementation details: Prometheus-specific fact promotion suppression and hard-coded capability/package/binary mappings appear implementation-owned in the reviewed files.
- Documented responsibility not fully proven by implementation evidence: read-only/no-authority boundaries are heavily documented and tested for selected surfaces; this audit did not prove every downstream consumer preserves those boundaries.

## Alignment, divergence, and uncertainty

### Alignments

- Execution status documentation aligns with implementation: it emits/consumes transient status and does not append events or create observations/facts.
- Observation source documentation aligns with source interfaces: sources collect observations and do not require ledger/projector internals.
- Projection cache documentation aligns with implementation: cache snapshots are derived and validated by version/event identity.
- Derived fact index documentation aligns with implementation: it is built from projected state and returns fact ids/facts without mutation.
- Capability inspection boundary notes align with implementation in reviewed modules: functions return dataclass inspection results and do not append ledger events.

### Divergences or partial divergences

- The audit found implementation-only constants/rules for capability mappings, binary mappings, and a Prometheus suppression exception. They may be intentional, but their authority basis was not fully documented in the reviewed files.
- `StateProjector.apply` silently ignores unknown event kinds. This may be intentional compatibility behavior, but the reviewed evidence did not establish a documented authority rule for unknown event handling.
- Some read-model classification responsibilities are documented locally in helper docstrings/boundary strings rather than in a centralized architecture document.

### Uncertainty remains

- Whether every runtime/CLI consumer treats inspection outputs as non-authoritative.
- Whether cache version constants have been updated for every semantic change historically.
- Whether incremental replay equivalence holds for all event histories and future projection changes.
- Whether all operator concerns correspond to real behavioral drift; this audit did not assume or prove drift.

## Final question: based on repository evidence alone

### What do we know?

- The current implementation separates transient status, observation collection, ingestion, projection, caches, derived indexes, read models, and capability inspection into distinct modules with documented boundaries.
- Event ledger history is documented and implemented as the authority for projection replay; caches are reusable derived snapshots.
- Capability inspection surfaces are implemented as read-only dataclass-producing functions over projected state and local metadata inspection.
- Targeted tests for the audited areas pass in this checkout.

### What do we think?

- The implementation shape is intentionally boundary-preserving in many audited areas, because docstrings, boundary notes, and tests repeatedly state and exercise non-authority behavior.
- Some responsibilities are embedded as implementation constants or helper-level semantics rather than centralized policy, which may increase operator uncertainty even if no defect exists.
- Projection cache and derived index behavior appears designed as optimization/read acceleration, not authority, but exhaustive semantic equivalence was not proven.

### What do we not yet know?

- Whether unreviewed consumers accidentally promote inspection/read-model outputs into authority.
- Whether all recent repository work is reflected in tests sufficient to prove boundary preservation end-to-end.
- Whether implementation-only assumptions should be documented as architecture, remain implementation details, or be changed; this audit does not propose fixes.
