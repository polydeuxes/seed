---
title: Responsibility ownership organization reconciliation
date: 2026-06-26
status: observational reconciliation
---

# Responsibility ownership organization reconciliation

## Question

Does the current implementation already organize architectural concepts around responsibility ownership rather than object classification?

## Short answer

Yes, mostly. The implementation is best described as **responsibility-oriented with mixed object vocabulary**. The strongest implementation pattern is not a generic object taxonomy; it is a set of bounded services, inventories, projection stages, and diagnostic surfaces that each declare or encode a responsibility and a boundary. Object/class names still matter, but they usually name an implementation holder for a scoped responsibility rather than a category in an object hierarchy.

Ownership can be treated as an observable, implementation-backed property when it is supported by one or more of these existing evidence forms:

- `__seed_arch__` owner metadata on runtime/execution/projection artifacts.
- Service/dataclass boundaries that state what the artifact does and does not do.
- Diagnostic inventory rows that declare CLI surface behavior, record scope, event-ledger writes, cluster mutation, and state/file use.
- Question surface inventory rows that bind a question family to one surface, one answer responsibility, and one authority boundary.
- Projection-shape stages that expose consumes, produces, influences, non-influences, and authority boundaries.
- Tests that assert these fields and boundaries remain visible.

The implementation does **not** support treating ownership as a free-standing truth merely because a noun appears in prose. Recent rejected concepts generally failed because they duplicated an existing owner, lacked an implementation artifact, were presentation vocabulary only, or were metadata attached to another owner.

## Commands executed

```text
pwd
rg --files -g 'AGENTS.md' -g '!venv' -g '!node_modules'
git status --short
cat AGENTS.md
rg -n "Observation Sources|Question Families|Documentation Structure|Runtime Responsibility|Diagnostic Inventory|Question Surface Inventory|State Projection|Decision Production|Projection|Execution|ownership|owner" . -g '!*.pyc' -g '!__pycache__'
find seed_runtime -maxdepth 1 -type f | sort | sed -n '1,160p'
find docs -maxdepth 1 -type f | sort | sed -n '1,120p'
sed -n '1,220p' seed_runtime/observation_sources.py
sed -n '1,220p' seed_runtime/question_surface_inventory.py
sed -n '1,180p' seed_runtime/documentation_structure.py
sed -n '1,180p' seed_runtime/runtime.py
sed -n '180,380p' seed_runtime/runtime.py
sed -n '1,220p' seed_runtime/execution.py
sed -n '1,180p' seed_runtime/decisions.py
sed -n '1,160p' seed_runtime/projection_store.py
sed -n '1,160p' seed_runtime/state.py
rg -n "__seed_arch__|class StateProjector|def project\(|DIAGNOSTIC_INVENTORY|DiagnosticInventoryEntry|QuestionSurfaceInventoryRow\(|answer_responsibility|authority_boundary|record_scope|mutates_cluster" seed_runtime tests docs/*responsibility* docs/*reconciliation* docs/*investigation* | head -n 240
python scripts/seed_local.py --question-surface-inventory --json
python scripts/seed_local.py --diagnostic-inventory --json
python scripts/seed_local.py --projection-shape --json
python scripts/seed_local.py --diagnostic-shape-audit --json
sed -n '1,220p' seed_runtime/diagnostic_inventory.py
sed -n '1,180p' seed_runtime/projection_shape.py
sed -n '1,160p' seed_runtime/container_ownership_authority.py
sed -n '1,160p' seed_runtime/service_ownership_authority.py
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

## Files inspected

- `AGENTS.md`
- `seed_runtime/observation_sources.py`
- `seed_runtime/question_surface_inventory.py`
- `seed_runtime/documentation_structure.py`
- `seed_runtime/runtime.py`
- `seed_runtime/execution.py`
- `seed_runtime/decisions.py`
- `seed_runtime/projection_store.py`
- `seed_runtime/state.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `seed_runtime/projection_shape.py`
- `seed_runtime/container_ownership_authority.py`
- `seed_runtime/service_ownership_authority.py`
- `tests/test_question_surface_inventory.py`
- `tests/test_projection_shape.py`
- `tests/test_container_ownership_authority.py`
- `tests/test_service_ownership_authority.py`
- `tests/test_diagnostic_inventory.py`
- `tests/test_diagnostic_shape_audit.py`
- `docs/runtime_responsibility_reconciliation.md`
- `docs/question_family_artifact_reconciliation.md`
- `docs/question_ownership_responsibility_reconciliation.md`
- `docs/answer_responsibility_artifact_reconciliation.md`
- `docs/concept_promotion_model_reconciliation.md`
- `docs/ask_question_family_dispatch_reconciliation.md`
- `docs/tool_vocabulary_reconciliation.md`

## Files changed

- `docs/responsibility_ownership_organization_reconciliation.md`

## LOC changed

- Added 211 lines in this report.

## Ownership matrix

| artifact | primary owner | owned responsibility | explicit boundary | projection | runtime role | strongest supporting evidence | strongest contradictory evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Observation Sources | Observation source adapters / collection service | Produce observations from bounded sources while staying unaware of ledger/projector/fact ingestion internals | `ObservationSource` protocol says sources expose identity/provenance and collect observations; repository/runtime sources are read-only adapters | Observations later enter projection through ingestion/projector, not owned by sources | Source collection only; not orchestration | Protocol docstring and source metadata (`name`, `source_type`, observation metadata) | Source collection service can normalize and write events, so collection and ingestion are adjacent and can look like shared ownership |
| Question Families | Question surface inventory row | Bind a question family to a surface, answer responsibility, authority boundary, bounded status, dispatch surface, and formatter metadata | Rows are static/read-only; notes repeatedly say inventory does not route/invoke recording | Question family is inventory metadata, not state projection | CLI presentation and bounded ask visibility | `QuestionSurfaceInventoryRow` fields and `build_question_surface_inventory()` rows | Dispatch map is in same module, so inventory owns visibility but also encodes routing-like metadata |
| Documentation Structure | Documentation structure observer | Observe mechanical Markdown structure only | Boundary constants reject prose interpretation, claims, authority inference, shape inference, event writes, and mutation | None except diagnostic/read-only output | CLI diagnostic/view | `BOUNDARY`, `RECURRENCE_BOUNDARY`, and `MEMBERSHIP_BOUNDARY` | The artifact is named around an object domain (`documentation`) though responsibility is structural observation |
| Runtime | Runtime orchestration | Route validated decisions to owner services and write response events | `__seed_arch__` says runtime routes without owning target behavior | Requests current projected state via `StateProjector` | Main orchestration loop | `Runtime.__seed_arch__`, `_route()` delegation to `ToolNeedService`, `ToolExecutor`, `StatePatchService` | Runtime writes several event kinds and constructs response envelopes, so broad event visibility can be mistaken for broad ownership |
| Execution | ToolExecutor / registered tool execution | Execute only registered operations after validation and policy checks | `__seed_arch__` owner `registered_tool_execution`; execution path requires registry, validation, policy, then records call events | Uses state projection for policy checks and fact extraction | Execution service called by runtime | `ToolExecutor.__seed_arch__`, `execute()`, `_execute_allowed_tool_call()` | Still uses `ToolSpec` and `tool.call.*` vocabulary, which can blur registered operation vs generic tool object |
| Decision Production / Validation | DecisionProducer protocol plus DecisionValidator | Decision producer creates decisions; validator enforces decision shape and tool-call validity | Validator accepts specific decision kinds and rejects unsupported/incomplete shapes | Validation uses current state for tool input validation | Runtime calls producer and validator before routing | `DecisionProducer` protocol and `DecisionValidator.validate()` | `StaticDecisionProducer` is minimal and production ownership is protocol-shaped rather than a rich artifact |
| Projection Cache | ProjectionStore | Store reusable projected-state snapshots derived from event ledger | Docstring separates EventLedger historical event ownership from ProjectionStore reusable snapshot ownership | Owns cached snapshots, summary snapshots, derived indexes | Used outside runtime loop for cached read models | `ProjectionStore.__seed_arch__`, protocol methods for load/save/clear snapshots | StateProjector builds state, so projection cache is delegated storage, not projection semantics |
| State Projection | StateProjector | Deterministically build current State from append-only events plus catalogs/inference | Projection diagnostics are optional and non-authoritative; projection stages say what they consume/produce/influence | Owns projected State construction | Supplies runtime current state and diagnostic surfaces | `state.py` projection classes and `projection_shape` stages | Projection produces many object collections, so output object classification is prominent |
| Diagnostic Inventory | DiagnosticInventoryEntry registry | Declare operational shape of diagnostic CLI surfaces | Explicit fields for projected-state use, repo-file use, JSON/record support, record scope, diagnostic facts, cluster facts, event-ledger writes, mutation | Inventory is static metadata, audited by shape audit | CLI inventory and audit | `DiagnosticInventoryEntry` fields and DIAGNOSTIC_INVENTORY rows | It is a registry of surfaces, not a universal owner registry |
| Question Surface Inventory | QuestionSurfaceInventoryRow registry | Declare answer responsibility and boundary for question families | `authority_boundary`, `bounded_status`, `dispatch_surface`, `implementation_reason`; diagnostic inventory marks read-only/non-mutating | Static presentation/answer inventory | CLI surface visibility | Tests require fields and parity with bounded asks | It may look like classification because `question_family` names categories |
| Projection Shape | ProjectionShapeStage inventory | Explain projection stage responsibility and authority boundary | Read-only boundary and per-stage consumes/produces/influences/does-not-influence | Directly describes projection | Diagnostic presentation only | `ProjectionShapeStage` dataclass and BOUNDARY | It describes stages, not owners by name |
| State Projection read models | Summary/derived index snapshots | Store dependent read-model snapshots tied to state projection versions and last event ids | Snapshot load methods require matching projection/version/last event | Cached projected summaries and derived indexes | None directly | `ProjectionStore` summary and derived-index methods | Ownership is implicit in method names and version coupling, not a separate owner field |

## Recently investigated concepts that did not become independent artifacts

| concept | outcome | implementation-backed reason |
| --- | --- | --- |
| Answer Responsibility | Not independent | Duplicate ownership / metadata only. The implemented field is `answer_responsibility` on `QuestionSurfaceInventoryRow`; no independent id, registry, or service owns it. It is observable as question-family metadata. |
| Runtime Responsibility | Not a runtime-activity artifact | Implementation-backed owner distinction rather than a current activity state. Existing `__seed_arch__` metadata and service boundaries distinguish owners; no single runtime-work-state projection owns it. |
| Actionability | Projection of inquiry state | The implementation treats actionability as derived/presented status rather than an independent owner. Evidence appears in bounded inquiry/state-view reports rather than an actionability service. |
| Presentation labels such as continuation/current work position/source navigation/active edge/storage topology/state build/projection cache | Not repository knowledge unless implementation-backed | Presentation vocabulary is explicitly guarded by AGENTS instructions and prior reconciliations; knowledge promotion requires implementation evidence such as reachability audit. |
| Answer composition ownership | Not separate from bounded surfaces | Question family/surface rows and concrete authority evaluators carry responsibilities and boundaries; no separate answer-composition owner is required by implementation. |
| Ownership support from a single fact class | Not accepted | Ownership reconciliation documents treat artifact/relationship/constraint evidence as helpful but insufficient alone; ownership support requires scoped converging evidence and competing-owner analysis. |

The repeated failure mode is therefore not one universal cause, but the dominant pattern is **duplicate ownership**: new nouns are rejected when an existing implementation owner already carries the responsibility.

## Shared, delegated, or conflicting ownership

Current implementation shows **delegated ownership**, not clear conflicting ownership, for the reviewed artifacts.

- Runtime delegates registered operation execution to `ToolExecutor`. Runtime owns routing and response envelopes; `ToolExecutor` owns execution checks and call events.
- Runtime delegates capability-gap/request-tool handling to `ToolNeedService` and recommendation/resolution helpers. Runtime does not own capability semantics.
- Observation sources produce observations; ingestion/projector own promotion into events/facts/state. This is adjacent and potentially ambiguous, but the protocol text keeps sources unaware of ledger/projector internals.
- ProjectionStore owns reusable snapshots, while StateProjector owns projected-state construction. This is delegated cache ownership, not conflicting projection ownership.
- Diagnostic inventory owns operational-shape declarations; individual diagnostic implementations own their concrete reports.
- Question surface inventory owns answer-responsibility metadata; concrete surfaces own actual report construction.

No reviewed implementation artifact showed two architectural owners asserting the same responsibility at the same scope. Ambiguity exists where service names, CLI names, and output objects use broader vocabulary than the owner metadata.

## Can ownership itself be observed?

Yes, within existing limits.

Observable ownership evidence currently includes:

- Owner metadata: `__seed_arch__` exists on Runtime, ToolExecutor, ProjectionStore, and related artifacts.
- Service boundaries: class/protocol docstrings and method routing show scoped responsibility and delegation.
- Inventory rows: diagnostic and question-surface inventories declare responsibility, boundaries, record scope, and mutation behavior.
- Diagnostic registration: `DIAGNOSTIC_INVENTORY` rows expose whether a surface records, writes event ledger, mutates cluster, reads diagnostic facts, or uses projected state/repo files.
- Tests: diagnostic inventory, diagnostic shape audit, question surface inventory, projection shape, and authority-slice tests assert these fields.
- Runtime actors/events: event kinds and actors expose runtime routing, model decisions, tool calls, and response events.
- Projection ownership: projection shape stages expose stage-level consumes/produces/influences and authority boundary.

Ownership is **not** observed as a single universal `owner` field everywhere. It is observed through a bundle of implementation-backed properties.

## Separation of ownership, projection, execution, and presentation

| concern | current separation | evidence | caveat |
| --- | --- | --- | --- |
| Ownership | Mostly separate | Owner metadata, service boundaries, inventory responsibility fields, authority boundaries | No universal owner registry |
| Projection | Separate | StateProjector/projection shape/projection store separate event replay, cache, summary, and derived-index responsibilities | Projected outputs are object collections, so classification vocabulary remains visible |
| Execution | Separate | ToolExecutor owns registered operation execution; runtime only routes `call_tool` decisions to it | Tool vocabulary still says `tool`, which can blur operation/catalog/execution |
| Presentation | Separate | CLI inventory/report surfaces are read-only and commonly non-recording/non-mutating; question inventory states it does not route operator questions | Some presentation labels can be mistaken for repository knowledge without reachability evidence |

## Strongest contradictory evidence

The strongest contradictory evidence is that the repository still uses object-oriented and category-oriented vocabulary at the implementation surface:

- Classes and dataclasses define many object-shaped records (`Observation`, `Fact`, `Entity`, `ToolSpec`, snapshot records, inventory rows).
- Question families are named categories and can look like a taxonomy.
- Projection emits object collections (`entities`, `facts`, `relationships`, `tools`, `approvals`, `pending_actions`) rather than owner-responsibility records.
- Diagnostic inventory is a registry of CLI surfaces, not a complete ownership registry.
- Some ownership evidence is metadata, not cluster truth; `__seed_arch__` is observable but not itself a projected fact in the reviewed implementation.
- Observation collection and ingestion are close enough that source production vs event/fact promotion can be ambiguous.
- Runtime writes response/model events, so event ownership can appear broader than its declared routing role.

These contradictions support a **mixed** characterization, but they do not overturn the responsibility-oriented pattern because the decisive boundaries are about what each artifact is responsible for, not merely what object class it belongs to.

## Characterization

Repository organization today is best described as:

> **Responsibility-oriented implementation with mixed object vocabulary.**

The implementation still uses object records and category names, but architectural status is earned by scoped responsibility, explicit boundary, implemented behavior, inventory registration, projection visibility, and tests. Concepts that duplicate an existing owner or exist only as presentation vocabulary tend not to become independent artifacts.

## Acceptance answers

### Has the repository already converged toward responsibility ownership as its organizing principle?

Yes, substantially. The reviewed areas repeatedly encode responsibility owners and boundaries: question families own bounded answer responsibility metadata; documentation structure owns structural observation; runtime owns orchestration; observation sources own observation production; execution owns registered operation execution; projection store owns projection snapshots; projection stages expose stage responsibilities; diagnostic inventory owns operational surface shape declarations.

### Can ownership be treated as an observable implementation-backed property?

Yes, but not as a single universal field. Ownership is observable when supported by implementation metadata, service boundaries, inventory rows, diagnostic registration, tests, runtime event routing, and projection-stage boundaries. A bare noun or prose label is insufficient.

### What implementation-backed evidence currently determines who owns a responsibility?

The strongest current determinants are:

1. Explicit `__seed_arch__` owner metadata where present.
2. Method-level behavior showing which component performs, delegates, or refuses a responsibility.
3. Inventory rows binding surfaces to responsibilities and authority boundaries.
4. Diagnostic inventory rows declaring operational shape and mutation/recording boundaries.
5. Projection-shape stage records declaring consumes, produces, influences, and authority boundary.
6. Tests that assert these fields and boundaries remain present.
7. Contradiction/absence evidence showing that candidate concepts have no independent artifact, no dispatch surface, no projection, or only metadata under another owner.

## Recommended bounded implementation slice

No redesign is recommended. If an implementation slice is needed, the smallest bounded slice is an **ownership-observation report generated from existing evidence only**: read `__seed_arch__`, diagnostic inventory rows, question-surface rows, and projection-shape stages; emit a read-only matrix with `record_scope=none`, `writes_event_ledger=false`, and `mutates_cluster=false`. This would not introduce an ownership framework; it would only expose already-existing owner evidence in one place.
