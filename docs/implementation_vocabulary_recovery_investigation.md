# Implementation Vocabulary Recovery Investigation

This investigation used the app and repository implementation as authority. It does not rename, normalize, refactor, or modify implementation code.

## Implementation summary

Seed already preserves a broad implementation language around bounded questions, diagnostic/operational surfaces, event authority, projected state, read-model consumers, runtime trace, transient execution status, audit snapshots, derivation/selection explanation, and knowledge reachability. The strongest convergence is structural rather than lexical: surfaces repeatedly expose owners or owner-like entries, consumers, contributors/evidence, support/consume relationships, boundaries, authority, and read-only/no-mutation declarations. The strongest divergence is surface-local vocabulary: `question_family`, `surface`, `diagnostic`, `stage`, `consumer_kind`, `owner`, `authority_boundary`, `boundary`, `record_scope`, `mutates_cluster`, `writes_event_ledger`, `evidence`, `consumers`, `supports`, and `influences` often describe adjacent parts of the same implementation explanation chain but are not exposed through one shared relationship schema.

## Commands executed

- `pwd && find .. -name AGENTS.md -print && git status --short`
- `cat AGENTS.md && git status --short && rg -n "diagnostic-inventory|diagnostic-shape-audit|knowledge-reachability|runtime trace|execution status|projection cache|reasoning path|selection path|state build|current facts|Question|Answer Owner|Supporting Contributors|Authority Boundary|implementation trait|audit snapshot|read model" -S .`
- `sed -n '1,460p' seed_runtime/question_surface_inventory.py`
- `sed -n '1,340p' seed_runtime/diagnostic_inventory.py`
- `sed -n '1,300p' seed_runtime/diagnostic_shape_audit.py`
- `sed -n '1,180p' seed_runtime/runtime_trace.py`
- `sed -n '1,140p' seed_runtime/execution_status.py`
- `sed -n '1,260p' seed_runtime/projection_shape.py`
- `python -m scripts.seed_local --question-surface-inventory --json > /tmp/q.json`
- `python -m scripts.seed_local --diagnostic-inventory --json > /tmp/d.json`
- `python -m scripts.seed_local --diagnostic-shape-audit --json > /tmp/s.json`
- `python -m scripts.seed_local --projection-shape --json > /tmp/p.json`
- `python -m scripts.seed_local --implementation-trait-characterization --json > /tmp/t.json`
- `sed -n '1,260p' seed_runtime/reasoning_path_audit.py`
- `sed -n '1,180p' seed_runtime/selection_path_audit.py`
- `sed -n '1,120p' seed_runtime/knowledge_reachability.py`
- `sed -n '1,160p' seed_runtime/fact_index.py`
- `sed -n '1,120p' seed_runtime/projection_store.py`
- `sed -n '1,110p' seed_runtime/audit_snapshots.py`
- `sed -n '1,120p' seed_runtime/projected_state_consumers.py`

## Implementation concepts recovered

| Concept | Primary owner | Supporting contributors | Primary consumers | Authority boundary | Implementation responsibility | Evidence |
|---|---|---|---|---|---|---|
| Bounded question surface inventory | `question_surface_inventory` | bounded ask dispatch maps, diagnostic inventory, shape specs | `ask --question-families`, operators, shape/visibility checks | read-only inventory; diagnostic-only rows are not dispatch | Preserve question family to answering surface, flag, responsibility, bounded status, dispatch metadata, formatter, diagnostic linkage | `QuestionSurfaceInventoryRow`, `BOUNDED_ASK_DISPATCH_SURFACES`, canonical diagnostic alias enrichment |
| Diagnostic inventory registry | `DIAGNOSTIC_INVENTORY` | surface declarations | diagnostic shape audit, projected-state consumers, tests/operators | static declaration; records and mutates flags declare boundaries | Preserve declared diagnostic/operational surface behavior, flags, record scope, ledger writes, cluster mutation | 48 app-reported entries in `/tmp/d.json`; registry includes diagnostic inventory and shape audit |
| Diagnostic shape audit | `IMPLEMENTATION_SPECS` and shape audit builder | module paths, build/format/json functions, CLI flags, markers | diagnostic inventory contract, tests/operators | read-only static implementation audit; does not execute targets | Compare declared registry shape with implementation-backed specs | App returned 432 shape-audit rows in `/tmp/s.json` |
| Projected state and projection stages | `StateProjector` / projection shape | event ledger, facts, alias resolver, catalogs, graph checks | current fact views, integrity/read models, projection store | projection-boundary / derivation-bearing / selection-bearing / validation-only / explanatory-only | Rebuild deterministic state and expose stages, consumes, produces, influences, non-influences | `PROJECTION_SHAPE_STAGES` and `build_projection_shape` |
| Projection cache/store | `ProjectionStore` | event ledger, `State`, state summary, derived indexes | state loading, cache debug, fact index | cache, not source of truth; snapshots derived from events | Persist reusable projection snapshots and dependent derived index snapshots | `ProjectionStore.__seed_arch__`, `ProjectionSnapshot`, `DerivedIndexSnapshot` |
| Dependent read-model cache / fact index | `DerivedFactIndex` | projected `State`, projection store | exact current-fact lookup | cacheable derived read model; not event/projection authority | Build and optionally save facts-by-subject/predicate lookup | `fact_index.py` module docstring and `load_or_build_fact_index` |
| Runtime trace | `RuntimeTraceReader` | event ledger reader, runtime events | runtime inquiry/operators/tests | read-only reconstruction; no replay/mutation | Reconstruct one run from append-only events: input, decision, policy, tool, assistant, errors, summary | `runtime_trace.py` classes and `trace()` |
| Execution status | `ExecutionStatus` and consumers | producers such as projection cache/fact index/observation lifecycle | CLI, tests, future renderers | transient, renderer-independent, non-authoritative | Emit and render activity phases/progress without owning execution state | `execution_status.py` docstrings and consumers |
| Audit snapshots | `audit_snapshots` helpers | commands, payloads, git metadata, event/projection metadata | audit list/compare/impact surfaces | local artifact; snapshot kind limited; best-effort git metadata | Save/read local `.audit/seed` snapshots for supported kinds | `SUPPORTED_KINDS`, `create_audit_snapshot` |
| Knowledge reachability | `knowledge_reachability` audit | event payloads, projected state, docs, source, inquiry/rendered surfaces | operators deciding whether vocabulary is implementation-backed | read-only audit over preserved/projected/read-model/inquiry/rendered evidence | Classify whether terms can be reached from preserved/projected/read-model/inquiry/rendered evidence | `DEFAULT_SEEDS`, `STAGES`, source budgets |
| Reasoning path / derivation explanation | `reasoning_path_audit` | ownership discrepancies, capability needs, pressure audit, privilege discovery, operational story | bounded derivation explanation, tests/operators | read-only reasoning audit; no facts/events/mutation | Explain evidence, intermediate conclusions, derived conclusions, consumers, story impact | `ReasoningPathAudit` and builder |
| Selection path / selection explanation | `selection_path_audit` | pressure audit, operational story | bounded selection explanation, tests/operators | read-only selection audit; no facts/events/mutation | Explain selected item, candidates, factors, non-selected alternatives, evidence, outcome | `SelectionPathAudit` and builder |
| Projected state consumers | `projected_state_consumers` inventory | diagnostic inventory, static surface sets | operators/diagnostic contract | read-only; no records/events/mutation/provider acquisition | Classify surfaces by consumer kind and evidence-source consumption | `ProjectedConsumerRow`, `STATIC_INVENTORY_SURFACES`, `INQUIRY_SURFACES`, etc. |
| Implementation trait characterization | `implementation_trait_characterization` | question surface inventory, concern registry | explainability/audit consumers | read-only surface characterization | Distinguish recurring implementation traits from metadata/containers | app output `/tmp/t.json` and module concern registry |
| Current facts | `State` current fact access and derived fact index | fact supports, predicate cardinality, alias resolver | environment inventory generated toolkit, fact views, explanation builders | projected read model, not event authority | Return current facts allowed by predicate cardinality | `State.get_current_facts`; generated environment inventory operation |
| Operational surfaces/read models | individual diagnostic builders | diagnostic inventory, state, repo files, event ledger, runtime input | CLI/operator-facing answers | mostly read-only; registry declares exceptions | Present operational graph, pressure, story, ownership, observations, capability, history, impact, etc. | 48 diagnostic inventory entries and projected-state consumer inventory |

## Implementation vocabulary matrix

| Concept | Terms currently used | Surfaces / locations |
|---|---|---|
| Bounded question surface | question family, answering Seed surface, surface, surface_flag, dispatch_surface, bounded_status, required_surface_args, human_formatter, answer_responsibility, authority_boundary, relationship_status, canonical diagnostic surface | CLI `--question-surface-inventory`, JSON fields, formatter, `ask --question-families`, tests/docs |
| Diagnostic registry | diagnostic, diagnostic inventory, operational surfaces, diagnostic/test-like operational surfaces, cli_flags, record_scope, mutates_cluster, writes_event_ledger | `--diagnostic-inventory`, registry dataclass/json, AGENTS operational visibility contract |
| Shape audit | diagnostic shape audit, implementation spec, shape mismatch, build_function, format_function, json_function, module_path, repo_file_markers | `--diagnostic-shape-audit`, shape specs/tests |
| Projection | state build, projection shape, projection stage, event_replay, alias_projection, current_fact_selection, influences, does_not_influence, authority boundary | `--projection-shape`, `ProjectionShapeStage`, docs and tests |
| Projection cache | projection cache, projection store, projected-state snapshots, state projection, state summary, snapshot, derived index snapshot | `projection_store.py`, `--current-facts-cache-debug`, execution status phases |
| Read models | read model, cacheable derived read model, derived index, current facts, consumers, projected-state consumers | `fact_index.py`, `projected_state_consumers.py`, generated toolkit |
| Runtime trace | runtime trace, event snapshot, read-only reconstruction, user_input_event, decision_record, policy_event, tool_event, assistant_event, error_events, summary | `runtime_trace.py`, tests/docs |
| Execution status | execution status, operator feedback, transient progress, phase, message, consumer, lifecycle | `execution_status.py`, CLI stderr rendering, tests/docs |
| Audit snapshots | audit snapshot, snapshot kind, before/after comparison, local operational audit snapshots, impact audit | `audit_snapshots.py`, `--audit-snapshot`, `--audit-snapshots`, `--audit-compare`, `--impact-audit` |
| Knowledge reachability | knowledge reachability, Preserved, Projected, Read Model, Inquiry Orientation, Rendered, presentation label, repository concept | `--knowledge-reachability-audit`, `knowledge_reachability.py`, AGENTS warning |
| Reasoning path | reasoning path, derivation explanation, observed evidence, intermediate conclusions, derived conclusions, consumers, story impact | `--reasoning-path`, question row, audit dataclass, human formatter |
| Selection path | selection path, selection explanation, selected, candidate set, selection factors, non-selected candidates, evidence, outcome | `--selection-path`, question row, audit dataclass, human formatter |

## Same concept, multiple terms

| Concept | Current terms | Surfaces | Implementation reason |
|---|---|---|---|
| Bounded answer surface | question family / surface / dispatch_surface / diagnostic_inventory_name / diagnostic_shape_spec_name | question inventory, diagnostic inventory, shape audit | Question inventory must join user-facing questions to executable dispatch and diagnostic visibility contracts; `knowledge_reachability_audit -> knowledge_reachability` proves explicit aliasing exists. |
| Read-only operational view | diagnostic, audit, inventory, surface, story, brief, graph, path | diagnostic inventory flags and many CLI surfaces | The registry treats many operator-visible views as diagnostic/test-like operational surfaces even when human labels are not “diagnostic.” |
| Projection-derived cache | projection store / projection cache / snapshot / derived index / read model | projection store, fact index, current-facts cache debug | The implementation distinguishes source-of-truth events from rebuildable reusable projections and dependent indexes. |
| Explanation of why | reasoning path / derivation explanation / selection path / selection explanation / operational story | question inventory, reasoning/selection audits, operational story | “Why” is decomposed into derivation evidence, selection candidates/factors, and composed operational story rather than one owner. |
| Boundary | authority_boundary / boundary / record_scope / writes_event_ledger / mutates_cluster / records_facts / provider_acquisition | question rows, diagnostic registry, reasoning/selection audits, projected-state consumers | Different surfaces expose boundary as prose, booleans, or enum-like values based on their local contract. |

## Similar terminology representing different concepts

| Similar terms | Distinct concepts | Evidence |
|---|---|---|
| `projection_shape`, `projection_store`, `projection cache`, `ProjectedConsumerRow` | stage visibility, snapshot persistence, operator cache phases, consumer classification | Projection shape does not build state; projection store persists snapshots; projected consumers classify surfaces. |
| `reasoning_path` vs `selection_path` | derivation from evidence/conclusions/consumers vs candidate ordering/selected outcome | Separate dataclasses, builders, CLI args, question families, and outputs. |
| `runtime trace` vs `execution status` | durable event reconstruction vs transient non-authoritative progress visibility | Runtime trace reads events; execution status consumers do not own execution state and may do nothing. |
| `audit snapshot` vs `ProjectionSnapshot` | local operational audit artifact vs cached projected state | Different modules, storage roots, metadata, and supported kinds. |
| `current facts` vs `FactSupport`/derived fact index | selected projected facts vs support aggregates/index cache | Fact index derives from state and support; it is not authority. |
| `diagnostic inventory` vs `question surface inventory` | registry of operational surfaces vs question-family answering surface map | App reports 48 diagnostic entries but 17 question rows, and projected-state docs note overlap without coextensiveness. |

## Implementation relationship matrix

| Concept | supports | supported_by | consumes | consumed_by | preserves | preserved_by | answers | answered_by |
|---|---|---|---|---|---|---|---|---|
| Question surface inventory | bounded ask visibility, relationship discovery | diagnostic inventory, shape specs, dispatch maps | registry/spec names | operators, tests, reverse inquiry docs | question-to-surface metadata | source code static rows | which question surface answers a family | row surface/flag/responsibility |
| Diagnostic inventory | visibility contract, consumer inventory, shape audit | registry entries | surface declarations | shape audit, projected-state consumers, tests | declared operational behavior | static registry | which diagnostics exist | `--diagnostic-inventory` |
| Shape audit | contract checking | implementation specs and registry | module/function/flag specs | operators/tests | mismatch evidence | static code scan/specs | whether declarations match shape | `--diagnostic-shape-audit` |
| Projection shape | projection explanation | implementation-backed stage list | event ledger/facts/catalogs in stage declarations | question inventory, operators | stage relationships | static `PROJECTION_SHAPE_STAGES` | what projection build exposes | `--projection-shape` |
| Projection store/cache | faster state loading, derived indexes | event ledger and StateProjector | event-derived state payloads | state loading, fact index, debug surface | snapshots | SQLite/in-memory store implementations | whether cache has usable snapshot | cache debug/status |
| Runtime trace | execution explanation | event ledger | append-only events | runtime question docs/tests | ordered event snapshots | event ledger | what happened in a run | runtime trace summary |
| Execution status | operator feedback | producers emitting phases | transient statuses | CLI/testing consumers | no durable facts by default | in-memory consumer only if chosen | what is happening now | rendered status |
| Audit snapshots | before/after comparison, impact audit | commands/payloads/git/events metadata | local artifacts | audit list/compare/impact | local audit artifacts | `.audit/seed` | what was captured | snapshot metadata/payload |
| Knowledge reachability | vocabulary authority checks | events, state, docs, source, inquiry/rendered surfaces | multiple evidence sources | operators, AGENTS policy | reachability rows | app audit output | whether term is reachable | staged reachability evidence |
| Reasoning path | derivation explanation | ownership, capability, pressure, privilege, story | implemented diagnostic builders | bounded ask/operators | derivation evidence in output | current state/builders | where conclusion came from | reasoning audit |
| Selection path | selection explanation | pressure audit, operational story | pressure candidates/story focus | bounded ask/operators | selection candidates/factors/outcome | current state/builders | why selected | selection audit |
| Projected-state consumers | visibility of consumption | diagnostic inventory static sets | diagnostic flags/surface names | operators/contract tests | consumer-kind rows | static classifications | who consumes projected/read sources | consumer inventory |

## Owner, consumer, contributor tables

### Owners

| Owner | Owns |
|---|---|
| `QuestionSurfaceInventoryRow` / inventory builder | question-family answer metadata and bounded status |
| `DIAGNOSTIC_INVENTORY` | diagnostic surface declaration contract |
| `IMPLEMENTATION_SPECS` | implementation shape expectations |
| `StateProjector` / projection shape | projection stages and state derivation visibility |
| `ProjectionStore` | reusable projected-state snapshots |
| `DerivedFactIndex` | fact lookup read-model cache |
| `RuntimeTraceReader` | run reconstruction from events |
| `ExecutionStatus` consumers | transient status rendering/recording |
| `audit_snapshots` | local audit artifacts |
| `knowledge_reachability` | term reachability classification |
| `reasoning_path_audit` | derivation explanation output |
| `selection_path_audit` | selection explanation output |
| `projected_state_consumers` | evidence-source consumption inventory |

### Consumers

| Consumer | Consumes |
|---|---|
| Operators/CLI | human and JSON surfaces |
| Bounded ask dispatch | question rows and dispatch maps |
| Diagnostic shape audit | diagnostic registry plus implementation specs |
| Projected-state consumer inventory | diagnostic inventory and static surface sets |
| Reasoning path | ownership/capability/pressure/privilege/story surfaces |
| Selection path | pressure audit and operational story |
| Runtime trace | event ledger |
| Fact index/current facts | projected State |
| Impact/audit compare | audit snapshots |
| Knowledge reachability | preserved, projected, read-model, inquiry, rendered sources |

### Contributors

| Contributor | Supports |
|---|---|
| Event ledger | runtime trace, projection, history, audit metadata |
| Projected State | facts, ownership/observation/pressure/capability surfaces |
| Static registries | inventory, shape, consumer, trait characterization |
| Repo files/docs | knowledge reachability, documentation/architecture audits |
| Audit snapshots | impact and comparison surfaces |
| Execution status producers | operator feedback without durable truth |
| Formatters/json functions | human and machine-readable operational answers |

## Support graph

```text
EventLedger -> StateProjector -> State -> read models/current facts -> operational diagnostics
EventLedger -> RuntimeTraceReader -> RuntimeTrace summary
State -> ownership/capability/pressure/privilege/story -> reasoning_path
State -> pressure_audit + operational_story -> selection_path
DIAGNOSTIC_INVENTORY -> diagnostic_shape_audit
IMPLEMENTATION_SPECS -> diagnostic_shape_audit
DIAGNOSTIC_INVENTORY -> projected_state_consumers
QuestionSurfaceInventory -> bounded ask dispatch -> existing CLI surfaces
ProjectionStore -> cached State / summaries / derived indexes
AuditSnapshots -> audit_compare / impact_audit
KnowledgeReachability <- events + projected state + read models + inquiry + rendered + source/docs
ExecutionStatus -> CLI/status consumers (transient only)
```

## Recurring implementation relationship patterns

Implementation-backed patterns already recur: owner/consumer/contributor, boundary/authority, read-only/no mutation, projection/cache/source-of-truth separation, build/format/json surface triplets, CLI flag to JSON/human formatter pairing, evidence to conclusion to consumer chains, selected vs non-selected candidate explanations, and support via static registries.

## Converging vocabulary

The most stable emerging vocabulary is: `surface`, `question_family`, `answer_responsibility`, `authority_boundary`, `boundary`, `consumer`, `evidence`, `projection`, `read model`, `snapshot`, `cache`, `record_scope`, `writes_event_ledger`, `mutates_cluster`, `supports`, `consumes`, `produces`, `influences`, `selected`, `candidates`, `outcome`, and `implementation evidence`. This is recovered only from existing code and app outputs.

## Diverging vocabulary and likely causes

| Divergence | Primary cause supported by repository evidence |
|---|---|
| question inventory vs diagnostic inventory coverage | true responsibility difference: question families are not coextensive with all operational/diagnostic CLI surfaces |
| authority prose vs boolean boundary fields | surface-local vocabulary and historical growth of local contracts |
| projection shape/store/cache/read-model terms | true conceptual differences plus surface-local vocabulary |
| reasoning/selection/story “why” terms | independent implementations for derivation, selection, and composed story |
| owner/consumer/support visibility | missing shared relationship visibility; relationships exist locally but not in one schema |
| presentation labels such as state build/projection cache | repository explicitly warns presentation vocabulary is not automatically knowledge and requires reachability evidence |

## Adversarial findings

If Seed were explaining his own implementation, inconsistent vocabulary would block truthful consistency in these places:

1. A user can ask from a question-family perspective, diagnostic-surface perspective, or CLI-flag perspective; the repository has the pieces to join them, but only question inventory rows expose the full chain and only for 17 rows.
2. Boundary answers vary between prose and booleans. A truthful answer must merge `authority_boundary`, `boundary`, `record_scope`, `writes_event_ledger`, and `mutates_cluster` without pretending they are the same field.
3. Projection explanations can confuse `projection_shape`, `ProjectionStore`, `projection cache`, current facts, and derived indexes unless the answer preserves responsibility boundaries.
4. “Why” explanations must not collapse reasoning path, selection path, and operational story. They answer different implementation questions.
5. Runtime visibility must not collapse runtime trace into execution status. One reconstructs durable events; the other is transient feedback.
6. Audit snapshots and projection snapshots share a word but are different storage responsibilities.
7. Knowledge reachability is the guardrail that prevents presentation vocabulary from being promoted to implementation truth without evidence.

## Implementation-backed gaps / where visibility stops

- There is no single implementation relationship schema that spans every owner, consumer, contributor, support edge, preservation edge, and answer edge.
- The diagnostic inventory and question surface inventory overlap but are not coextensive; many diagnostic surfaces have no question-family owner row.
- Some boundaries are only prose while others are structured booleans/enums.
- Runtime trace exists as a reader but is less prominent in the diagnostic inventory than registered operational surfaces.
- Supporting contributors are explicit in reasoning/selection/projection consumers but implicit for many other diagnostics.
- Implementation trait characterization identifies traits and non-traits, but it does not own question-family coverage.
- Knowledge reachability can classify terms but does not itself normalize vocabulary or create canonical concepts.

## Files inspected

- `AGENTS.md`
- `seed_runtime/question_surface_inventory.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `seed_runtime/runtime_trace.py`
- `seed_runtime/execution_status.py`
- `seed_runtime/projection_shape.py`
- `seed_runtime/reasoning_path_audit.py`
- `seed_runtime/selection_path_audit.py`
- `seed_runtime/knowledge_reachability.py`
- `seed_runtime/fact_index.py`
- `seed_runtime/projection_store.py`
- `seed_runtime/audit_snapshots.py`
- `seed_runtime/projected_state_consumers.py`
- representative tests found with `rg` for reasoning/selection paths and visibility contracts

## Files changed

- `docs/implementation_vocabulary_recovery_investigation.md`

## LOC changed

- Added this investigation document only. No implementation files were modified.

## Tests run

No code tests were required or run because this is an implementation investigation and documentation-only repository finding. App surfaces were run as listed in Commands executed.

## Conclusion

Yes. The repository already possesses the implementation concepts necessary for a coherent implementation language, with the remaining work primarily involving recovery, normalization, and relationship visibility, rather than invention of new architectural concepts. The evidence is strongest for existing concepts and relationships; it is weaker only where those relationships are implicit, surface-local, or split across separate inventories.
