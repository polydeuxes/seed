# Implementation Assumptions Reconciliation

## Scope and boundary

This reconciliation investigates whether implementation assumptions are already preserved as observable implementation-backed evidence. It is observational only: it does not introduce an assumption registry, assumption engine, governance process, policy layer, or new architecture methodology.

Repository authority wins. The evidence below is limited to implementation, tests, CLI-visible JSON/read models, and existing documentation structure where it describes or exposes implemented behavior.

## Commands executed

```text
pwd
rg --files -g 'AGENTS.md' -g '!venv' -g '!node_modules'
git status --short
cat AGENTS.md
rg --files | sed -n '1,120p'
rg -n "diagnostic|question|Question|inventory|ledger|append|projection|project|runtime|authority|observation|read-only|deterministic|exact|bounded|static|request|response" seed tests *.md | head -n 240
rg --files seed_runtime scripts docs | head -n 200
sed -n '1,220p' seed_runtime/events.py
sed -n '1,220p' seed_runtime/state.py
sed -n '1,220p' seed_runtime/question_surface_inventory.py
sed -n '1,180p' seed_runtime/diagnostic_inventory.py
sed -n '180,420p' seed_runtime/diagnostic_inventory.py
sed -n '1,220p' seed_runtime/diagnostic_shape_audit.py
sed -n '1,180p' seed_runtime/runtime.py
sed -n '1,160p' seed_runtime/observations.py
sed -n '160,340p' seed_runtime/observations.py
sed -n '180,420p' seed_runtime/runtime.py
python scripts/seed_local.py --diagnostic-inventory --json | head -c 2000
python scripts/seed_local.py --diagnostic-shape-audit --json | head -c 2000
python scripts/seed_local.py --question-surface-inventory --json | head -c 2000
```

One exploratory `rg` command included a non-existent `seed` path and returned `rg: seed: No such file or directory`; the same command still inspected `tests` and top-level Markdown files.

## Files inspected

- `AGENTS.md`
- `README.md`
- `IMPLEMENTATION.md`
- `02-domain-model.md`
- `10-build-plan.md`
- `13-knowledge-and-evidence.md`
- `seed_runtime/events.py`
- `seed_runtime/state.py`
- `seed_runtime/runtime.py`
- `seed_runtime/observations.py`
- `seed_runtime/question_surface_inventory.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- CLI output from `scripts/seed_local.py --diagnostic-inventory --json`
- CLI output from `scripts/seed_local.py --diagnostic-shape-audit --json`
- CLI output from `scripts/seed_local.py --question-surface-inventory --json`

## Files changed

- `docs/implementation_assumptions_reconciliation.md`

## LOC changed

- Added one documentation report: 161 lines.

## Summary answer

Yes, the repository already preserves several implementation assumptions as observable evidence. The preservation is not centralized as an independent assumption artifact. Instead, assumptions are expressed through existing owners: event ledger storage rules, state projection code, static Question Surface Inventory rows, diagnostic inventory declarations, diagnostic shape-audit implementation specs, runtime routing metadata, observation ingestion events, and tests/CLI JSON surfaces.

The strongest conclusion is that assumptions are currently implementation properties owned elsewhere. The strongest contradiction to treating them as independent architectural artifacts is that there is no dedicated assumption model, registry, event kind, projection, CLI, or test suite for assumptions as first-class objects. Visibility exists when another owner exposes its own invariant or boundary.

## Assumption matrix

| Assumption | Implementation evidence | Current owner | Visibility | Projection support | Runtime support | Strongest supporting evidence | Strongest contradictory evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Append-only event history | `EventLedger` stores events by appending to `_events`, `_by_id`, and `_by_workspace`; duplicate IDs raise before storage. `SQLiteEventLedger` creates an `events` table and exposes the same append/list API. | Event ledger / event history | Directly visible in API behavior and tests; indirectly visible through docs and state rebuilding | Feeds `StateProjector` from ledger events | Runtime appends input, model decision, and response events | `EventLedger.__seed_arch__` declares owner `event_history` and edge to `StateProjector`; append/list APIs preserve append order | Append-only is a class behavior and documentation phrase, not an independently queryable assumption object |
| Deterministic projection | `StateProjector` is described as projection from append-only events; alias resolution is deterministic and built from explicit alias facts; docs and tests reference deterministic projection. | Projection / state projector | Observable through projected state, tests, cache rebuild/status, and CLI state views | Primary owner; projections derive facts, relationships, aliases, entity types, graph issues, and support aggregates | Runtime calls `projector.project(workspace_id)` before decision composition and during request-tool recommendations | State code uses frozen dataclasses and explicit derivation from facts/events; docs define `ProjectionStore` as rebuildable cache, not source of truth | Determinism is proven through projector behavior/tests, not surfaced as a standalone assumption row |
| Read-only diagnostic surfaces | `DiagnosticInventoryEntry` has `mutates_cluster`, `writes_event_ledger`, `supports_record`, and `record_scope`; entries repeatedly declare read-only/no mutation boundaries. | Diagnostic inventory | Directly observable via `seed --diagnostic-inventory --json`; shape-audit compares declared and observed fields | Many entries declare `uses_projected_state=true`; shape-audit also declares this field | Runtime is not the owner; diagnostic surfaces are CLI/read-model owners | Inventory JSON exposes `mutates_cluster=false`, `writes_event_ledger=false`, `record_scope=none` or `diagnostic_run` | Read-only status is attached to diagnostics, not to a generic assumption system |
| Exact structural matching | Documentation-structure diagnostic inventory description exposes exact section-label drilldown and membership; CLI flags include `--where` and `--membership`. | Documentation structure diagnostic | Observable through diagnostic inventory and documentation structure CLI JSON/human surfaces | No cluster projection support required; it is repository-file observation | No runtime support | Diagnostic inventory explicitly describes exact section-label structural drilldown/membership | Exactness belongs to documentation structure tooling; it is not generalized across repository concepts |
| Bounded inquiry dispatch | `BOUNDED_ASK_DISPATCH_SURFACES`, `BOUNDED_ASK_REQUIRED_SURFACE_ARGS`, and `bounded_status_for_question_family` derive eligibility from static maps; inventory rows carry `bounded_status`, `dispatch_surface`, and required args. | Question Surface Inventory / bounded ask | Directly observable via `seed --question-surface-inventory --json` | Some mapped surfaces use projected state; inventory itself is static/read-only | Runtime does not dispatch these questions directly; bounded ask maps route to surfaces | JSON output exposes `eligible_now`, `eligible_with_parameters`, `diagnostic_only`, dispatch surface, and implementation reason | The inventory says rows do not necessarily route operator questions; boundedness is an inventory property, not independent assumption architecture |
| Static Question Family inventory | `build_question_surface_inventory()` returns a fixed tuple of `QuestionSurfaceInventoryRow`; duplicate/orphan checks compare rows to dispatch maps. | Question Surface Inventory | Direct CLI JSON and tests | Projection support varies by surface; inventory is not projected from ledger | Runtime support is indirect; this is not the runtime loop | Static tuple plus validation helper makes question families inspectable and testable | Static inventory is code data; it does not preserve assumption history or evolution |
| Request/response runtime | `Runtime.handle_user_message()` appends `input.user_message`, projects state, composes decision input, requests one decision, validates it, routes answer/question/refusal/tool need/call tool/state patch, and appends response events. | Runtime orchestration | Observable through runtime tests, event ledger events, and runtime metadata | Runtime depends on projected state before decision and for recommendations | Primary support: runtime route implementation and `__seed_arch__` route/event metadata | Runtime `__seed_arch__` lists events and routes; code records input, proposed decision, and response events | Request/response is an implementation control flow, not a named repository artifact |
| Projection derived, not authority | Domain docs state facts are projected interpretations of evidence and `ProjectionStore` is cache, not source of truth; code derives Evidence and Facts from Observations and state from events. | Projection / evidence / observation ingestion | Observable through event payloads, state views, evidence/fact IDs, and docs | Primary support: FactSupport/projection structures derive from Facts/Evidence | Runtime uses projected state as decision context, not as event authority | Observation ingestion creates `observation.observed`, `evidence.observed`, and `fact.observed`/`fact.inferred` events with causation/provenance | Some docs are stronger than direct CLI; projection-derived status is not emitted as a single `assumption` field |
| Authority constrained | Diagnostic entries and question inventory rows repeatedly encode `authority_boundary`; authority evaluators exist for service/container/listener endpoint; runtime routes owner services without owning behavior. | Authority evaluator surfaces / runtime orchestration / Question Family | Observable through question inventory JSON, diagnostic inventory JSON, and authority CLI surfaces | Authority surfaces usually consume projected state and repo evidence | Runtime `__seed_arch__` says it routes decisions to owner services without owning their behavior | Inventory rows expose authority boundaries such as read-only/no recording/no mutation; diagnostic inventory exposes cluster mutation and event-ledger fields | Authority is preserved as boundaries and evaluator behavior, not as an independent authority-assumption artifact |
| Observation collection preserves provenance | `ObservationIngestor.ingest_many()` converts each Observation to Evidence and optional Fact, stores per-observation event metadata, and preserves observation source type, dimensions, expiry, confidence, and causation/correlation IDs. | Observation ingestion / evidence pipeline | Observable through ledger events and projected facts/evidence | Projector consumes fact/evidence events downstream | Runtime can receive projected facts from observation-derived events | Code emits ordered observation, evidence, and fact events; `observation_to_evidence()` includes original observation payload fields | The observation path is a data pipeline; the assumption is implicit in event shapes and tests rather than named |
| Diagnostic recording boundary | Diagnostic inventory records `record_scope`, `emits_diagnostic_facts`, `emits_cluster_facts`, `writes_event_ledger`, and `mutates_cluster`; shape audit compares those fields with implementation markers. | Diagnostic inventory / diagnostic shape audit | Directly observable via `--diagnostic-inventory --json` and `--diagnostic-shape-audit --json` | Diagnostic entries identify projected-state usage | Runtime not primary owner | Shape-audit JSON reports declared vs observed fields with status such as `consistent` | Boundary is a diagnostic contract, not an all-purpose assumption artifact |

## Direct observability

Assumptions can be directly observed when they appear as fields or stable shapes owned by existing surfaces:

- Diagnostic boundaries are directly visible as JSON fields: `mutates_cluster`, `writes_event_ledger`, `record_scope`, `supports_record`, `supports_json`, `uses_projected_state`, and `uses_repo_files`.
- Diagnostic shape preservation is directly visible as declared/observed/status rows from `--diagnostic-shape-audit --json`.
- Question-family boundedness is visible as `bounded_status`, `dispatch_surface`, `required_surface_args`, `json_support`, and `implementation_reason` from `--question-surface-inventory --json`.
- Runtime request/response assumptions are visible through runtime events and `Runtime.__seed_arch__` route/event metadata, but not through a dedicated assumption CLI.
- Projection-derived assumptions are visible through projected state shape, evidence/fact provenance, and tests, but not as a first-class assumption record.

## Existing owners

Implementation assumptions currently belong to existing owners:

- Event history owns append-only ordering and ID uniqueness.
- Projection owns deterministic derived state, aliases, relationships, graph validation, and FactSupport aggregation.
- Question Surface Inventory owns static bounded inquiry visibility.
- Documentation Structure owns exact section-label/document-shape observation.
- Runtime owns request/response routing and delegates behavior to owner services.
- Authority evaluators own bounded authority decisions for service/container/listener endpoint surfaces.
- Observation ingestion owns provenance-preserving observation/evidence/fact event creation.
- Diagnostic Inventory and Diagnostic Shape Audit own diagnostic visibility and recording/mutation boundaries.

## Independent artifact evaluation

Assumptions do not currently qualify as independent architectural artifacts. They are consistently expressed through existing implementation:

- There is no `Assumption` model, `assumption.*` event kind, assumption projection, assumption inventory, assumption CLI, or assumption test module.
- The same words appear as implementation-backed properties only when an owning surface needs them: event ledgers append, projectors derive, diagnostics declare mutation/recording boundaries, question inventory declares bounded dispatch, and runtime records request/response events.
- The observable unit is therefore the owner artifact, not an assumption artifact.

## Strongest contradictory evidence

The strongest contradictory evidence is that assumptions are mostly boundaries, implementation details, tests, comments, or prose:

- Append-only and deterministic are embodied in class behavior and tests, but are not queryable as assumption records.
- Read-only and mutates-cluster boundaries are diagnostic inventory fields; they are not global repository assumptions.
- Exact matching is scoped to documentation structure and structural membership surfaces.
- Request/response behavior is runtime control flow.
- Authority constrained behavior is preserved in evaluator surfaces and inventory row prose/fields.
- Projection-derived state is fundamental, but the repository exposes projections and provenance rather than exposing an `assumption=projection_derived` object.

## Repetition across unrelated implementation

Several assumptions recur across otherwise separate implementation areas, but the recurrence stays bounded to evidence:

- `read-only` / `mutates_cluster=false` appears in diagnostic inventory, question inventory authority boundaries, observation/domain authority surfaces, and documentation-oriented diagnostics.
- `bounded` appears in bounded ask dispatch, authority evaluators, diagnostic recording scope, and runtime delegation boundaries.
- `derived/projection` appears in state projection, FactSupport aggregation, decision context composition, diagnostics that consume projected state, and cache lifecycle docs.
- `static inventory` appears in Question Surface Inventory and Diagnostic Inventory, but they are separate inventories with separate owners.
- `exact` appears strongly in documentation structure and structural membership work; current evidence does not justify generalizing it to every matching surface.

## Acceptance answers

### Does the repository already preserve implementation assumptions as observable evidence?

Yes, but only through existing implementation owners. Observable evidence includes CLI JSON, inventory rows, diagnostic shape-audit rows, runtime metadata, event payloads, projection shapes, and tests.

### Are assumptions independent architectural artifacts, or implementation properties owned elsewhere?

They are implementation properties owned elsewhere. Current preservation is owner-local: ledger, projection, runtime, diagnostic inventory, question inventory, documentation structure, authority evaluators, and observation ingestion.

### What implementation-backed evidence currently makes an assumption observable?

An assumption becomes observable when an owning implementation emits or preserves it as:

- a public CLI JSON field,
- an inventory row,
- a shape-audit declared/observed/status row,
- a runtime event kind or route metadata,
- a projected state/evidence/fact shape,
- a deterministic test assertion,
- or a repository-file diagnostic result.

## Recommended bounded implementation slice

No assumption framework is recommended. The bounded slice, if implementation work is desired, is to add a diagnostic-only documentation report or test that cross-links existing visible fields to their current owners without changing runtime behavior. The smallest safe slice would be a test-backed extension of an existing inventory/shape-audit surface only if a specific current owner lacks visibility. Otherwise, this report is sufficient as an observational reconciliation.
