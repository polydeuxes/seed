# Implementation Artifact Explanation Grammar Investigation

## Implementation summary

This investigation treats implementation artifacts as the starting point and asks what each artifact can truthfully say about itself from existing code, registries, diagnostics, and prior repository investigations. The repository already has an explanation grammar, but it is distributed across artifact declarations, static inventories, diagnostic registries, projection stages, read-model builders, and operator views. The strongest implementation-backed answer is therefore not a new relationship ontology. It is a composed explanation shape whose fields recur as responsibility, ownership/owner, consumed inputs, produced outputs, consumers, preservation/cache behavior, authority boundary, and known unknowns or visibility stops.

The implementation does not attach all of those fields uniformly to every artifact. Some artifacts carry rich local self-description through dataclass fields and `__seed_arch__`; some can explain themselves only when combined with inventories or shape-audit specifications; and some are primarily presentation/read-model surfaces whose explanation is bounded by CLI functions and tests rather than artifact-local metadata.

## Representative artifact explanations

| Artifact | Smallest truthful self-explanation currently supported | Implementation evidence |
| --- | --- | --- |
| `ProjectionStore` | Backend-independent projection cache that owns reusable projected-state, summary, and derived-index snapshots derived from the event ledger; it loads, saves, and clears snapshots but is not event history. | `seed_runtime/projection_store.py` module docstring separates ledger ownership from projection-store ownership; `ProjectionStore` protocol docstring, `__seed_arch__`, and snapshot APIs name owner, layer, summary, edges, load/save/clear state snapshots, summary snapshots, and derived-index snapshots. |
| `StateProjector` | State-projection owner that rebuilds current inspectable `State` by reading append-only ledger events, applying them, and finalizing derived indexes with catalogs and graph validation. | `StateProjector` docstring and `__seed_arch__` name owner/layer/summary/edges; constructor consumes `EventLedger` and catalogs; `project`, `project_from_state`, and `finalize` materialize events, replay them, and rebuild projection indexes. |
| `RuntimeTraceReader` | Read-only runtime-run reconstruction from append-only events; it consumes an event reader, filters events for a workspace/run, snapshots them, and produces `RuntimeTrace` with event slices and summary without replay or mutation. | `seed_runtime/runtime_trace.py` module docstring, `EventReader`, `RuntimeTrace`, and `RuntimeTraceReader.trace()` define the read-only event dependency, ordered event output, run summary, and non-replay/non-mutation boundary. |
| `ExecutionStatusConsumer` | A transient status observer interface; consumers render, record, or ignore renderer-independent non-authoritative activity visibility without owning execution state. | `ExecutionStatus` and `ExecutionStatusConsumer` docstrings define non-authoritative activity visibility and consumption; `NullExecutionStatusConsumer`, `RecordingExecutionStatusConsumer`, and `CliExecutionStatusConsumer` prove do-nothing, in-memory, and CLI-rendering consumers. |
| `QuestionSurfaceInventoryRow` | Static read-only mapping from a question family to an answering surface, flag, answer responsibility, authority boundary, bounded ask status, implementation reason, diagnostic linkage, and relationship status. | `QuestionSurfaceInventoryRow` fields and `build_question_surface_inventory()` rows encode family, examples, surface, answer responsibility, authority boundary, notes, dispatch metadata, formatter, diagnostic inventory/spec names, and relationship status. |
| `DiagnosticInventoryEntry` | Registry declaration for one operational diagnostic CLI surface, including flags, projected-state/repo-file dependencies, JSON/record support, record scope, emitted facts, ledger writes, cluster mutation, diagnostic reads, and description. | `DiagnosticInventoryEntry` fields and `DIAGNOSTIC_INVENTORY` rows encode dependencies, recording boundary, mutation boundary, and descriptions for diagnostic surfaces. |
| `ProjectionShapeStage` / projection shape | Read-only stage explanation for projection: each stage states what it consumes, produces, influences, does not influence, and what authority boundary it has. | `ProjectionShapeStage` fields and `PROJECTION_SHAPE_STAGES` entries define stage, consumes, produces, influences, does-not-influence, boundary, and confidence. |
| `ReasoningPathAudit` | Read-only derivation-path explanation for a domain/subject, carrying evidence, intermediate conclusions, derived conclusions, consumers, story impact, unknowns, and a no-record/no-ledger/no-cluster boundary. | `ReasoningPathAudit` dataclass fields and `build_reasoning_path_audit()` build from implemented diagnostic surfaces only. |
| `SelectionPathAudit` | Read-only selection explanation for a target, carrying selected item, candidates, factors, non-selected alternatives, evidence, outcome, unknowns, and a no-record/no-ledger/no-cluster boundary. | `SelectionPathAudit` fields and `build_selection_path_audit()` derive selection evidence from pressure audit and operational story, returning unknowns when target is not implemented. |
| `ProjectedStateConsumer` | No single artifact with this exact name was found. The repository does imply projected-state consumers through CLI/state views, diagnostics, and `uses_projected_state` declarations, but visibility is distributed rather than artifact-local. | `DiagnosticInventoryEntry.uses_projected_state`, question-surface rows, state-build/current-facts CLI paths, and docs/audit findings identify consumers of projected state. |
| `RelationshipCatalog` | Read-only topology vocabulary defining directed relationships Seed can project from facts; it owns relationship names/kinds, endpoint types, and predicate derivation mapping with unique relationship names. | `RelationshipDefinition` and `RelationshipCatalog` docstrings/fields/load/get/for_predicate/list methods plus uniqueness validation support this explanation. |
| `OperationalSurfaceInventory` | Operational surface inventory exists as a tested inventory/audit surface rather than a single core class in `seed_runtime`; it classifies CLI surfaces and validates diagnostic visibility. | `tests/test_operational_surface_inventory.py` covers inventory/audit behavior, and diagnostic inventory/shape audit provide registry-backed surface declarations. |
| `KnowledgeReachability` | Audit result explaining whether candidates are preserved, projected, present in read models, inquiry-oriented, rendered, and where first loss occurs, with metadata for timings, counts, cache, indexes, truncation, and limits. | `KnowledgeReachabilityRow`, `KnowledgeReachabilityMetadata`, and `KnowledgeReachabilityAuditResult` fields encode reachability stages and audit metadata. |
| `StateBuild` | State-build is a CLI/read-model surface, not a single model class. It builds projected state and summary/read-model accounting, can use dependent summary cache, and renders cache status/debug timing. | `scripts/seed_local.py` state-build flag declarations and state-build helper/formatter functions define the surface; projection-store tests prove cache hit/miss behavior. |
| `CurrentFacts` | Current-facts is a CLI/read-model surface over projected facts, with a cache-debug report that explains state-cache path and fact-index/read-model timing. It is not an artifact-local class except for `CurrentFactsTimingReport`. | `CurrentFactsTimingReport`, `_TimingProjectionStore`, `_current_facts_timing_from_args()`, and current-facts CLI declarations define output, cache status, store-operation timings, and read-only timing boundary. |

## Recurring explanation fields already implied by implementation

The recurring fields are implementation-backed but not universally colocated:

- **Identity / what am I:** class names, protocol names, dataclass names, CLI surface names, and row names recur across `ProjectionStore`, `StateProjector`, trace/status artifacts, inventories, projection shape, reasoning/selection audits, relationship catalog, and reachability rows.
- **Responsibility / summary:** `__seed_arch__["summary"]`, docstrings, inventory descriptions, question `answer_responsibility`, and diagnostic `description` recur.
- **Owner / ownership:** explicit `__seed_arch__["owner"]` appears on `ProjectionStore` and `StateProjector`; docs and inventories repeat ownership language for caches, projection, and catalogs. Many read-model surfaces instead expose responsibility, not owner.
- **Inputs consumed:** projection shape stages use `consumes`; `StateProjector` consumes ledger events and catalogs; `RuntimeTraceReader` consumes events; diagnostic rows identify projected-state/repo-file dependencies; current-facts timing wraps projection-store loads.
- **Outputs produced:** projection shape stages use `produces`; `StateProjector` produces `State`; trace produces `RuntimeTrace`; question and diagnostic inventories produce JSON dicts; reachability produces rows/metadata; state-build/current-facts produce rendered read models.
- **Consumers / consumer impact:** `ReasoningPathAudit.consumers`, `ProjectionStore.__seed_arch__` edges, `StateProjector.__seed_arch__` edges, question rows, and diagnostic inventories identify downstream surfaces, though not always under the same field name.
- **Preservation / cache:** `ProjectionStore` snapshots, `StateBuild` summary cache, current-facts fact-index cache, and reachability cache metadata recur as preservation-like fields.
- **Authority boundary:** question rows, diagnostic rows, projection stages, reasoning/selection audits, runtime trace docstrings, execution status docstrings, and architecture docs all encode read-only, projection, identity-resolution, selection-bearing, derivation-bearing, no-ledger, and no-cluster boundaries.
- **Unknowns / visibility stops:** reasoning and selection audits carry `unknowns`; reachability carries `first_loss`; diagnostic inventories expose unsupported JSON/recording; investigation docs identify distributed visibility.

## Artifact-specific explanation fields

- `QuestionSurfaceInventoryRow` uniquely carries operator question examples, bounded ask status, dispatch surface, required surface args, formatter, canonical diagnostic surface, and relationship status.
- `DiagnosticInventoryEntry` uniquely carries operational diagnostic facts such as `supports_record`, `record_scope`, `emits_diagnostic_facts`, `emits_cluster_facts`, `writes_event_ledger`, `mutates_cluster`, and `reads_diagnostic_facts`.
- `ProjectionShapeStage` uniquely carries `influences`, `does_not_influence`, and a projection-stage `authority_boundary` literal.
- `ReasoningPathAudit` uniquely carries derivation-specific `intermediate_conclusions`, `derived_conclusions`, `story_impact`, and subject/domain scope.
- `SelectionPathAudit` uniquely carries `selected`, `candidates`, `selection_factors`, `non_selected`, and outcome.
- `KnowledgeReachabilityRow` uniquely carries preservation/projection/read-model/inquiry/render booleans and `first_loss`.
- `ProjectionStore` uniquely carries snapshot identity/version/last-event/cache payload fields.
- `ExecutionStatusConsumer` uniquely carries transient status phases, message, counts, completion, and rendering cadence.
- `RuntimeTraceReader` uniquely carries run-id/workspace event reconstruction and runtime event categories.

## Explanation coverage matrix

| Artifact | Can answer "what am I" | Responsibility | Owner | Consumes | Produces | Consumer visibility | Preservation | Authority/boundary | Coverage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ProjectionStore | Yes | Yes | Yes | Partial | Yes | Partial | Yes | Yes | Strong |
| StateProjector | Yes | Yes | Yes | Yes | Yes | Partial | No | Yes | Strong |
| RuntimeTraceReader | Yes | Yes | No | Yes | Yes | Partial | No | Yes | Strong but owner absent |
| ExecutionStatusConsumer | Yes | Yes | No | Yes | Partial | Yes | No | Yes | Partial/strong |
| QuestionSurfaceInventoryRow | Yes | Yes | No | Partial | Yes | Yes | No | Yes | Strong as inventory row |
| DiagnosticInventoryEntry | Yes | Yes | No | Yes | Yes | Yes | Record boundary only | Yes | Strong as diagnostic row |
| ProjectionShapeStage | Yes | Yes by stage | No | Yes | Yes | Influences | No | Yes | Strong as projection stage |
| ReasoningPathAudit | Yes | Yes | No | Yes | Yes | Yes | No | Yes | Strong for derivation |
| SelectionPathAudit | Yes | Yes | No | Yes | Yes | Yes | No | Yes | Strong for selection |
| ProjectedStateConsumer | No exact artifact | Distributed | No | Yes by rows/functions | Yes by surfaces | Yes | No | Partial | Partial/distributed |
| RelationshipCatalog | Yes | Yes | Catalog owner implied | Yes | Yes | StateProjector | Preserves vocabulary | Yes | Strong vocabulary, weak consumers local |
| OperationalSurfaceInventory | Surface/test-backed | Yes | No | Yes | Yes | Yes | No | Yes | Partial/distributed |
| KnowledgeReachability | Yes | Yes | No | Yes | Yes | Yes via loss | Cache metadata | Yes | Strong audit result |
| StateBuild | CLI surface | Yes | No | Yes | Yes | Operator output | Summary cache | Yes | Partial/distributed |
| CurrentFacts | CLI surface/report | Yes | No | Yes | Yes | Operator output | Fact-index/state cache | Yes | Partial/distributed |

## Explanation composition findings

Implementation explanations naturally compose through the listed relationship families, but not as a universal relationship schema. The strongest recurring composition is:

1. **Artifact identity and responsibility** from class/protocol/dataclass docstrings, inventory rows, and `__seed_arch__` summaries.
2. **Input/output shape** from methods, dataclass fields, projection shape stages, and CLI builders.
3. **Authority/boundary** from diagnostic inventory, question inventory, projection shape authority literals, and audit boundary dicts.
4. **Consumption/consumer paths** from `consumes`/`produces`/`influences`, `ReasoningPathAudit.consumers`, CLI flags, and diagnostic `uses_projected_state` declarations.
5. **Preservation/cache** from projection snapshots, summary snapshots, derived-index snapshots, and cache/timing reports.

The implementation therefore demonstrates an explanatory structure of **identity + responsibility + dependencies + outputs + consumers + preservation/cache + authority boundary + loss/unknowns**, with ownership present for some core state artifacts but not for every read model or audit result.

## Explanation failures and gaps

The main failures are not missing relationship types. They are visibility and attachment failures:

- **Distributed visibility:** State-build, current-facts, operational surface inventory, and projected-state consumers are implemented through CLI functions, registries, tests, and docs rather than a single artifact-local explanation record.
- **Implicit ownership:** Many artifacts have responsibility and boundaries but no explicit `owner` field. This is visible for trace/status/audit/read-model artifacts.
- **Implicit consumers:** `RelationshipCatalog` is consumed by `StateProjector`, but local catalog metadata does not list consumers. Read-model consumers often appear in CLI flags/tests rather than the artifact itself.
- **Boundary split:** Diagnostic boundaries are excellent for diagnostic registry rows, while projection boundaries live in projection shape stages and docstrings. A single artifact may need both to explain itself.
- **Class-vs-surface mismatch:** `StateBuild`, `CurrentFacts`, `OperationalSurfaceInventory`, and `ProjectedStateConsumer` are surfaces/roles rather than exact core classes. Their explanations require composing code paths, tests, and inventory entries.
- **Unknown/loss fields are localized:** `ReasoningPathAudit`, `SelectionPathAudit`, and `KnowledgeReachability` encode unknowns/loss directly; most core artifacts do not.

## Adversarial findings: "Explain yourself"

| Artifact group | Finding | Why |
| --- | --- | --- |
| Already can | `ProjectionStore`, `StateProjector`, `RuntimeTraceReader`, `ExecutionStatusConsumer`, `QuestionSurfaceInventoryRow`, `DiagnosticInventoryEntry`, `ProjectionShapeStage`, `ReasoningPathAudit`, `SelectionPathAudit`, `RelationshipCatalog`, `KnowledgeReachability` | Each has local fields/docstrings/methods sufficient to state identity, responsibility, inputs/outputs, and at least one boundary. |
| Partially can | `StateBuild`, `CurrentFacts`, `OperationalSurfaceInventory`, projected-state consumer role | Their explanations are real but composed from CLI declarations, helper functions, registries, tests, and docs rather than attached to one artifact. |
| Cannot as exact artifact | `ProjectedStateConsumer` as a named class/protocol; `StateBuild` and `CurrentFacts` as model classes | The exact artifact names are roles/surfaces; the implementation evidence exists under other names and functions. |

## Cause of explanation failures

The dominant cause is **distributed visibility**, followed by **implicit relationships** and **missing local ownership/consumer fields**. The evidence does not support the claim that failures primarily result from missing relationship kinds. Existing relationships already express ownership, responsibility, support, consumption, production, preservation, authority, boundary, derivation, selection, and consumer impact in different places. True implementation gaps are narrower: the absence of exact named artifacts for some roles and the absence of artifact-local explanation records for CLI/read-model surfaces.

## Implementation-backed boundaries

- Projection cache is not event history; event ledgers own append-only historical events while projection stores own reusable snapshots.
- State projection reads events and derives inspectable state; it does not own event creation.
- Runtime trace reconstructs recorded runs without replaying or mutating them.
- Execution status is transient, renderer-independent, and non-authoritative.
- Diagnostic surfaces declare recording, event-ledger writing, and cluster mutation boundaries in the registry.
- Reasoning and selection audits are read-only and do not record facts, write the event ledger, or mutate the cluster.
- Projection shape stages can be selection-bearing, derivation-bearing, validation-only, explanatory-only, identity-resolution, projection-boundary, or unknown, and explicitly state what does not influence the event ledger.

## Smallest common explanation grammar already recoverable

Without extending or normalizing the implementation, the smallest common grammar already recoverable is:

```text
artifact identity
responsibility / answer responsibility
owner when explicitly declared
inputs consumed / dependencies
outputs produced / records rendered
consumers or influenced surfaces when visible
preservation/cache behavior when relevant
authority and mutation boundary
unknowns, first-loss, or visibility stop when relevant
implementation evidence location
```

This is a composed implementation grammar, not a new universal schema. It is recoverable by composing existing `__seed_arch__`, dataclass fields, diagnostic inventory rows, question-surface inventory rows, projection-shape stages, audit result fields, CLI builders, and tests.

## Commands executed

- `pwd && rg --files -g 'AGENTS.md' -g '!**/.git/**' && git status --short`
- `cat AGENTS.md && rg "class ProjectionStore|ProjectionStore|StateProjector|RuntimeTraceReader|ExecutionStatusConsumer|QuestionSurfaceInventoryRow|DiagnosticInventoryEntry|ProjectionShape|ReasoningPath|SelectionPath|ProjectedStateConsumer|RelationshipCatalog|OperationalSurfaceInventory|KnowledgeReachability|StateBuild|CurrentFacts" -n .`
- `rg -n "class (ProjectionStore|SQLiteProjectionStore|InMemoryProjectionStore)|class StateProjector|class RuntimeTraceReader|class .*ExecutionStatusConsumer|class QuestionSurfaceInventoryRow|class DiagnosticInventoryEntry|class ProjectionShape|class ReasoningPath|class SelectionPath|class ProjectedStateConsumer|class RelationshipCatalog|class OperationalSurfaceInventory|KnowledgeReachability|class StateBuild|CurrentFacts" seed_runtime scripts tests docs -g '*.py' -g '*.md'`
- `sed -n '1,220p' seed_runtime/projection_store.py; sed -n '700,860p' seed_runtime/state.py; sed -n '1,90p' seed_runtime/runtime_trace.py; sed -n '1,80p' seed_runtime/execution_status.py`
- `sed -n '1,180p' seed_runtime/question_surface_inventory.py; sed -n '1,140p' seed_runtime/diagnostic_inventory.py; sed -n '1,120p' seed_runtime/projection_shape.py; sed -n '1,110p' seed_runtime/relationship_catalog.py`
- `sed -n '1,170p' seed_runtime/reasoning_path_audit.py; sed -n '1,150p' seed_runtime/selection_path_audit.py; sed -n '150,235p' seed_runtime/knowledge_reachability.py; sed -n '5020,5095p' scripts/seed_local.py`
- `rg -n "OperationalSurface|ProjectedStateConsumer|StateBuild|state-build|current-facts|RelationshipCatalog" seed_runtime scripts docs tests -g '*.py' -g '*.md'`
- `python scripts/seed_local.py --diagnostic-inventory >/tmp/diag_inv.txt && python scripts/seed_local.py --diagnostic-shape-audit >/tmp/diag_shape.txt && python scripts/seed_local.py --projection-shape >/tmp/proj_shape.txt && python scripts/seed_local.py --question-surface-inventory >/tmp/qsi.txt && wc -l /tmp/diag_inv.txt /tmp/diag_shape.txt /tmp/proj_shape.txt /tmp/qsi.txt`

## Files inspected

- `AGENTS.md`
- `seed_runtime/projection_store.py`
- `seed_runtime/state.py`
- `seed_runtime/runtime_trace.py`
- `seed_runtime/execution_status.py`
- `seed_runtime/question_surface_inventory.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/projection_shape.py`
- `seed_runtime/reasoning_path_audit.py`
- `seed_runtime/selection_path_audit.py`
- `seed_runtime/knowledge_reachability.py`
- `seed_runtime/relationship_catalog.py`
- `scripts/seed_local.py`
- `tests/test_operational_surface_inventory.py`
- selected prior investigation docs located by `rg`

## Files changed

- `docs/implementation_artifact_explanation_grammar_investigation.md`

## LOC changed

One documentation file was added. The file contains this investigation only and does not modify runtime implementation, tests, registries, diagnostic surfaces, relationship catalogs, or ontology vocabulary.

## Tests run

No implementation tests were required because this is an implementation investigation and does not change code. The app-backed checks run were diagnostic/read-only surfaces:

- `python scripts/seed_local.py --diagnostic-inventory`
- `python scripts/seed_local.py --diagnostic-shape-audit`
- `python scripts/seed_local.py --projection-shape`
- `python scripts/seed_local.py --question-surface-inventory`

## Conclusion

Yes. The repository already possesses a shared implementation explanation grammar, such that the remaining work is primarily making artifacts capable of explaining themselves through existing implementation relationships, rather than inventing new architectural concepts.

That grammar is not a universal relationship schema and should not be normalized beyond the evidence. It is a composed shape already present across implementation artifacts: identity, responsibility, optional owner, consumed inputs, produced outputs, consumer/influence visibility, preservation/cache behavior, authority boundary, and unknown/loss/visibility-stop fields.
