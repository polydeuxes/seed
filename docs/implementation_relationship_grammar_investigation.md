# Implementation Relationship Grammar Investigation

This implementation investigation used existing Seed app surfaces and implementation files to recover the relationship grammar already exposed by the repository. It does not rename relationships, introduce a shared relationship schema, or modify implementation behavior.

## Implementation summary

Seed already exposes a coherent structural grammar across independently implemented surfaces. The vocabulary differs by subsystem, but the recurring implementation structure is stable:

`bounded subject/surface -> owner or answering responsibility -> supporting evidence/contributors -> authority/boundary -> produced answer/output -> consumers/impact -> unknowns/gaps`.

This conclusion is implementation-backed by the app outputs and files inspected below. The strongest evidence is not a single canonical relationship vocabulary; it is the repeated presence of ownership/answer responsibility, support/evidence, consumption/production, authority/boundary, derivation/selection, preservation/recording, and explicit non-mutation boundaries across question inventory, diagnostic inventory, projection shape, projected consumers, reasoning path, selection path, runtime trace, execution status, and catalog relationship projection.

## Recovered relationship inventory

| Relationship exposed by implementation | Meaning recovered from implementation | Representative evidence |
| --- | --- | --- |
| `answer_responsibility` / answers | The surface responsible for answering a bounded question family. | `QuestionSurfaceInventoryRow.answer_responsibility`; app output from `--question-surface-inventory --json`. |
| `surface` / answering surface | The implementation surface associated with a question family or diagnostic row. | `QuestionSurfaceInventoryRow.surface`; `DiagnosticInventoryEntry.name`. |
| `dispatch_surface` | The implementation target used by bounded ask routing. | `BOUNDED_ASK_DISPATCH_SURFACES` and `QuestionSurfaceInventoryRow.dispatch_surface`. |
| `required_surface_args` | Parameters required before a bounded question can dispatch. | `BOUNDED_ASK_REQUIRED_SURFACE_ARGS`. |
| `authority_boundary` / `boundary` | The read/record/mutate/authority constraints defining what the surface may claim or do. | Question rows, diagnostic inventory fields, projected consumer boundary, reasoning and selection audit boundary dicts. |
| `supports_json` / `json_support` / `json_capable` | Output capability relationships between surface and JSON renderability. | Diagnostic inventory, question inventory, operational surface/trait characterization. |
| `supports_record` / `record_scope` | Whether a diagnostic can record, and the scoped subject of that recording. | Diagnostic inventory and diagnostic shape audit. |
| `emits_diagnostic_facts` / `emits_cluster_facts` | Whether recordable output remains diagnostic or becomes cluster fact output. | Diagnostic inventory entries. |
| `writes_event_ledger` / `mutates_cluster` | Boundary relationship distinguishing append-only diagnostic recording from cluster mutation. | Diagnostic inventory, projected consumers, selection/reasoning boundaries. |
| `uses_projected_state` / `uses_repo_files` / `uses_static_inventory` / `uses_event_ledger` / `uses_runtime_input` / `uses_live_observation` | Consumption/source relationships between surfaces and evidence classes. | Diagnostic inventory and projected-state consumers. |
| `reads_diagnostic_facts` | Consumption of diagnostic facts by a diagnostic/authority surface. | Diagnostic inventory. |
| `consumes` | Projection-stage input relationship. | Projection shape stages. |
| `produces` | Projection-stage output relationship. | Projection shape stages. |
| `influences` | Downstream projection-stage impact relationship. | Projection shape stages. |
| `does_not_influence` | Negative authority/impact boundary. | Projection shape stages. |
| `consumers` | Downstream surfaces that consume or report a derived conclusion. | Reasoning path audit. |
| `evidence` / `supporting_*` | Support relationship tying conclusions, status, candidates, or capabilities to facts/evidence. | Capability inventory/verification; reasoning path; selection path; confidence. |
| `intermediate_conclusions` / `derived_conclusions` | Derivation relationship between evidence and conclusions. | Reasoning path audit. |
| `candidates` / `selected` / `non_selected` / `selection_factors` | Selection grammar: candidate set, selected outcome, non-selected alternatives, factors. | Selection path audit. |
| `user_input_event`, `decision_record`, `policy_event`, `tool_event`, `assistant_event`, `error_events` | Runtime trace relationship from event ledger to reconstructed runtime phases. | Runtime trace. |
| `causation_id` / `correlation_id` / `run_id` | Runtime event membership/causal relationship used to associate events with a run. | Runtime trace membership logic. |
| `consume(status)` | Transient execution-status consumer relationship. | Execution status consumer protocol and implementations. |
| `depends_on`, `member_of`, `alias_of`, `monitored_by`, `provides`, `runs_on`, `related_to`, `belongs_to_domain`, `defines` | Catalog-projected entity/document relationships derived from predicates. | Relationship catalog. |
| `defined/import depends_on` | Repository/document observation relationship limited to static imports or front matter. | Relationship observation and documentation observation. |
| `classified_by` / concern classification | Trait-to-concern classification relationship. | Implementation trait characterization. |

## Relationship meaning matrix

| Relationship family | Relationship terms | Producer/exposer | Consumer | Responsibility | Boundary |
| --- | --- | --- | --- | --- | --- |
| Answer ownership | `answer_responsibility`, `surface`, `dispatch_surface` | Question surface inventory | Bounded ask routing/tests/operators | Identify who answers a question family and which implementation surface dispatches. | Inventory/read-only; does not inspect answer payloads. |
| Authority | `authority_boundary`, `boundary`, `record_scope`, `mutates_cluster`, `writes_event_ledger` | Question inventory, diagnostic inventory, shape audit, projected consumers, path audits | Operators, shape audit tests, diagnostic inventory tests | Preserve what a surface may claim or mutate. | Read-only unless explicitly record-capable; diagnostic recording scoped to `diagnostic_run`. |
| Consumption | `uses_*`, `reads_diagnostic_facts`, `consumes` | Diagnostic inventory, projected consumers, projection shape | Consumer audits, operational explanations, projection stages | Declare evidence/input dependencies. | Declared source classes; no inference beyond registry evidence in projected-state consumers. |
| Production | `produces`, `emits_*`, runtime trace phase fields | Projection shape, diagnostic inventory, runtime trace | Views, graph validation, explanations | Identify outputs produced by stages/surfaces. | Projection outputs do not rewrite event ledger; diagnostic facts remain diagnostic unless declared otherwise. |
| Support/evidence | `evidence`, `supporting_fact_ids`, `supporting_evidence`, `support` | Capability inventory, capability verification, confidence, reasoning/selection audits | Explanation surfaces and tests | Tie status/conclusion to implementation evidence. | Support is preserved separately from execution authority. |
| Derivation | `intermediate_conclusions`, `derived_conclusions`, `derived_from_predicates` | Reasoning path, relationship catalog | Operational story, graph/projected relationship views | Explain how conclusions or relationships are derived. | Read-only reasoning; catalog derivation only from configured predicates. |
| Selection | `candidates`, `selected`, `non_selected`, `selection_factors`, `outcome` | Selection path audit | Operators/tests | Explain why one operational conclusion/focus was selected. | Read-only; target must match implemented selection surface. |
| Runtime membership | `run_id`, `correlation_id`, `causation_id`, typed events | Event ledger/runtime trace | Runtime trace reader | Reconstruct a run without replaying. | Read-only snapshots from append-only events. |
| Execution observation | `ExecutionStatusConsumer.consume`, `RecordingExecutionStatusConsumer.statuses` | Execution status emitters/producers | CLI/test consumers | Expose activity without owning execution state. | Transient and non-authoritative. |
| Catalog topology | `member_of`, `alias_of`, `runs_on`, `depends_on`, etc. | Relationship catalog projection | Graph validation/views | Project implementation-backed graph relationships. | Bound by catalog relationship definitions and derived predicates. |
| Trait classification | `CONCERN_BY_TRAIT`, `consumer_kind` | Implementation trait characterization/projected consumers | Operators/tests | Classify exposed fields by concern. | Read-only characterization of existing surfaces. |

## Relationship producer table

| Producer subsystem | Relationships produced/exposed |
| --- | --- |
| Question Families | `question_family`, `surface`, `surface_flag`, `answer_responsibility`, `authority_boundary`, `bounded_status`, `dispatch_surface`, `required_surface_args`, `json_support`, diagnostic mapping, `relationship_status`. |
| Diagnostic Inventory | `uses_projected_state`, `uses_repo_files`, `supports_json`, `supports_record`, `record_scope`, `emits_diagnostic_facts`, `emits_cluster_facts`, `writes_event_ledger`, `mutates_cluster`, `reads_diagnostic_facts`. |
| Diagnostic Shape Audit | Declared-vs-observed field relationships across diagnostic fields and implementation specs. |
| Projection Shape | Stage-level `consumes`, `produces`, `influences`, `does_not_influence`, `authority_boundary`. |
| Projected State Consumers | Surface-level source consumption classes and `consumer_kind`. |
| Runtime Trace | Run membership and runtime phase relationships from event ledger events. |
| Execution Status | Status producer-to-consumer relationship via `consume`. |
| Reasoning Path | Evidence, intermediate conclusion, derived conclusion, consumer, story impact, unknown relationships. |
| Selection Path | Candidate, selected, non-selected, factor, evidence, outcome relationships. |
| Relationship Catalog | Catalog relationship names, kinds, type bounds, and predicate derivation. |
| Implementation Trait Characterization | Trait-to-concern and field-to-surface exposure relationships. |
| Knowledge/relationship observation | Static import/document front-matter dependency relationships with explicit non-claims. |

## Relationship consumer table

| Consumer subsystem | Relationships consumed |
| --- | --- |
| Bounded ask/question inventory tests | Dispatch maps, answer responsibility, authority boundary, JSON/record support, relationship visibility status. |
| Diagnostic shape audit | Diagnostic inventory declarations and implementation spec markers. |
| Projected state consumer inventory | Diagnostic inventory source flags and static surface sets. |
| Projection finalization/views | Projection-stage products such as facts, relationships, entity type assertions, graph issues, supports. |
| Reasoning path | Ownership discrepancies, capability needs, pressure, privilege, and operational story outputs. |
| Selection path | Pressure audit candidates and operational story focus. |
| Runtime trace | Event ledger run/correlation/causation fields and typed runtime events. |
| Execution status consumers | Transient `ExecutionStatus` updates. |
| Graph/relationship views | Relationship catalog entries and predicate-derived relationship projections. |
| Trait characterization | Dataclass fields from diagnostic, projected consumer, question, and operational-surface inventories. |

## Equivalent relationships

These are implementation-equivalent in structural role, even when vocabulary differs:

1. **Answer ownership / responsibility**: `answer_responsibility`, answering `surface`, and `dispatch_surface` all identify the implementation that answers or routes a bounded question. They are not identical fields: `answer_responsibility` is semantic text, while `surface` and `dispatch_surface` are implementation identifiers.
2. **Evidence consumption**: diagnostic `uses_projected_state`, projected-consumer `sources`, and projection-stage `consumes` all encode input dependency; they differ by granularity.
3. **Operational boundary**: question `authority_boundary`, diagnostic `record_scope`/`mutates_cluster`/`writes_event_ledger`, projection `authority_boundary`, and path-audit `boundary` all constrain authority.
4. **Support/evidence**: `supporting_fact_ids`, `supporting_evidence`, `evidence`, and confidence support counts all serve the same structural role of grounding conclusions.
5. **Output/production**: projection `produces`, diagnostic `emits_*`, and runtime trace phase fields all identify produced observable outputs.

## Distinct relationships with similar names

1. **`supports_json` is not evidentiary support**. It means output capability, while `supporting_facts` and `supporting_evidence` mean justification.
2. **`supports_record` is not preservation support**. It declares a record-capable mode; `record_scope` defines where recorded diagnostic facts attach.
3. **`authority_boundary` differs from `authority` as ownership attribution**. Inventory boundaries constrain claims/actions; ownership-authority surfaces evaluate whether enough evidence exists to assert ownership.
4. **`consumes` in projection shape differs from `ExecutionStatusConsumer.consume`**. Projection `consumes` names data inputs; execution status `consume` observes transient progress updates.
5. **`depends_on` in relationship catalog/document metadata differs from runtime source consumption**. It is projected topology or documentation dependency, not a general implementation input edge.
6. **`influences` differs from `produces`**. Projection shape uses `influences` for downstream impact, while `produces` names direct stage outputs.
7. **`mutates_cluster=false` differs from `writes_event_ledger=false`**. Diagnostic inventory repeatedly separates append-only event writes from cluster mutation.

## Implicit relationship findings

| Implicit relationship | Evidence that it exists | Visibility end |
| --- | --- | --- |
| Answer owner to supporting contributors | Question inventory names answer responsibility; reasoning path separately names evidence/consumers. | No unified per-question contributor graph across all answer payloads. |
| Diagnostic inventory to shape-audit spec ownership | Shape audit keys specs by diagnostic name and compares declared fields. | Ownership is by matching name, not explicit owner edge. |
| Projection stage graph | Projection shape exposes consumes/produces/influences. | No single normalized graph object across all subsystems. |
| Runtime event causal graph | Runtime trace matches `run_id`, `causation_id`, and `correlation_id`. | Trace reconstructs one run; it does not expose arbitrary artifact explanations. |
| Consumer provenance | Projected-state consumers report source classes from inventory evidence. | Some surfaces still expose source class rather than exact field-level dependencies. |
| Responsibility graph | Existing responsibility investigations and question inventory expose owners/responsibilities. | Responsibility is distributed across docs/inventories, not a shared relationship schema. |

## Subsystem relationship graph

```text
Question Families
  -> dispatch_surface -> Diagnostic / Inquiry / Projection surfaces
  -> answer_responsibility -> Bounded Answer
  -> authority_boundary -> allowed claims/actions

Diagnostic Inventory
  -> declares source use -> Projected State Consumers
  -> declares record/event/mutation boundary -> Diagnostic Shape Audit
  -> maps CLI surfaces -> Question Surface Inventory

Diagnostic Shape Audit
  -> consumes Diagnostic Inventory declarations
  -> consumes Implementation Specs
  -> produces consistency/warning/mismatch rows

Projection Shape
  -> consumes event_ledger/facts/catalogs/evidence
  -> produces facts/supports/relationships/entity assertions/graph issues
  -> influences views, validation, current-fact selection

Relationship Catalog
  -> derives relationships from predicates
  -> consumed by projection and graph validation

Reasoning Path
  -> consumes ownership discrepancies/capability needs/pressure/privilege/story
  -> produces evidence -> intermediate conclusions -> derived conclusions -> consumers/story impact

Selection Path
  -> consumes pressure candidates and operational story focus
  -> produces selected/non-selected/outcome explanation

Runtime Trace
  -> consumes event ledger run membership
  -> produces user-input/decision/policy/tool/assistant/error trace

Execution Status
  -> producers emit transient status
  -> consumers observe without owning execution state

Implementation Trait Characterization
  -> consumes inventory dataclass fields
  -> classifies traits into evidence_source, operational_boundary, dispatchability, implementation_capability
```

## Recurring relationship patterns

1. **Ownership/responsibility**: answer responsibility, service/container ownership authority, execution status non-ownership, diagnostic spec-by-name responsibility.
2. **Participation/contribution**: supporting facts/evidence, contributors in diagnostic descriptions, reasoning-path evidence and consumers.
3. **Dependency/consumption**: `uses_*`, `consumes`, `depends_on`, source classes.
4. **Production**: `produces`, `emits_*`, rendered outputs, runtime phase records.
5. **Preservation/recording**: event ledger, `record_scope`, diagnostic-run subjects, runtime trace snapshots.
6. **Authority/constraint**: `authority_boundary`, no-record/no-mutation boundaries, verification-not-execution-authority notes.
7. **Explanation/derivation**: reasoning path, relationship catalog `derived_from_predicates`, implementation trait meanings.
8. **Selection**: candidates, selected, non-selected, selection factors, current focus.
9. **Validation/audit**: diagnostic shape audit, graph issues, knowledge reachability unknowns.

## Explanation coverage for major subsystems

Seed can already partially answer:

- **What am I?** Yes for inventory rows, diagnostic entries, projection stages, runtime trace events, traits, and catalog relationships.
- **Who owns me?** Partially. Question answer responsibility and ownership-authority surfaces expose bounded owners/responsibilities, but not every artifact has a first-class owner edge.
- **Who answers through me?** Yes for question families via surface/dispatch mappings.
- **Who supports me?** Yes where fact/evidence support exists; incomplete for arbitrary inventory fields.
- **What do I support?** Partially through reasoning consumers, projection influences, and catalog projection; not universal.
- **Who consumes me?** Partially through projected-state consumers, projection influences, reasoning consumers, and consumer audits.
- **What do I consume?** Strong for diagnostic/projected/projection surfaces; weaker for arbitrary functions.
- **What do I preserve?** Strong for event ledger/runtime trace/record-scope boundaries; partial elsewhere.
- **What preserves me?** Strong for runtime event trace and recorded diagnostic facts; implicit for static inventories.
- **What authority constrains me?** Strong across diagnostics, question surfaces, path audits, projection stages.
- **What boundaries define me?** Strong for operational surfaces; less complete for arbitrary implementation artifacts.

Implementation visibility ends at arbitrary artifact explanation: current surfaces explain many registered/inventoried artifacts, but not every code symbol, output field, or prose concept without Codex-level repository inspection.

## Adversarial findings

If Seed had to explain any implementation artifact without Codex, the largest blockers would be:

1. **No universal artifact-to-owner edge**. Question families have answer responsibility, but many implementation artifacts expose only module/function names or registry membership.
2. **No universal artifact-to-consumer edge**. Projected-state consumers and consumer audits cover important surfaces/predicates, but not all functions, dataclass fields, or documents.
3. **No universal support graph for inventory fields**. Some rows expose implementation reasons, but many field meanings depend on static implementation structure rather than explicit support edges.
4. **Boundary vocabulary is recurring but distributed**. Boundaries are present in many places, but not emitted through one shared artifact explanation surface.
5. **Implicit relationship composition requires cross-surface reasoning**. Projection shape, question inventory, diagnostic inventory, and path audits each expose part of the graph.

These are implementation-backed gaps in visibility, not recommendations for implementation work.

## Implementation-backed gaps

- Relationship grammar is present but distributed across multiple inventories and audits.
- Equivalence between structurally similar relationships is recoverable by inspection, not represented as explicit repository knowledge.
- Some relationships are negative boundaries (`does_not_influence`, `mutates_cluster=false`) and are easy to lose if explanations only report positive edges.
- Runtime trace explains runs, but not all arbitrary artifacts involved in a run.
- Trait characterization classifies fields, but does not make every classified field a relationship edge.

## Commands executed

- `pwd && rg --files -g 'AGENTS.md' -g '!venv' -g '!node_modules' && git status --short`
- `cat AGENTS.md && rg --files`
- `rg --files seed_runtime`
- `rg -n "owner|consumer|contributor|support|preserv|authority|boundary|answer|implemented_by|classified_by|constrained_by|produces|produced_by|influences|selected_from|consumes|depends|participant|record_scope|mutates_cluster" seed_runtime tests relationship_catalog/core.json predicate_catalog/core.json`
- `find . -maxdepth 3 -type d | sort`
- `rg -n "implementation investigation|relationship grammar|responsibility investigation|files changed|LOC changed" .`
- `sed -n '1,220p' seed_runtime/question_surface_inventory.py`
- `sed -n '1,180p' seed_runtime/diagnostic_inventory.py`
- `sed -n '1,160p' seed_runtime/diagnostic_shape_audit.py`
- `sed -n '1,220p' seed_runtime/projection_shape.py`
- `sed -n '1,220p' seed_runtime/projected_state_consumers.py`
- `sed -n '1,180p' seed_runtime/runtime_trace.py`
- `sed -n '1,180p' seed_runtime/execution_status.py`
- `sed -n '1,220p' seed_runtime/reasoning_path_audit.py`
- `sed -n '1,160p' seed_runtime/selection_path_audit.py`
- `sed -n '1,220p' seed_runtime/implementation_trait_characterization.py`
- `sed -n '1,160p' relationship_catalog/core.json`
- `python scripts/seed_local.py --question-surface-inventory --json`
- `python scripts/seed_local.py --diagnostic-inventory --json`
- `python scripts/seed_local.py --projection-shape --json`
- `python scripts/seed_local.py --projected-state-consumers --json`
- `python scripts/seed_local.py --implementation-trait-characterization --json`
- `python scripts/seed_local.py --knowledge-reachability-audit-json`
- `python scripts/seed_local.py --reasoning-path ownership service --json`
- `python scripts/seed_local.py --selection-path current_focus --json`
- `python scripts/seed_local.py --diagnostic-shape-audit --json`

## Files inspected

- `AGENTS.md`
- `seed_runtime/question_surface_inventory.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `seed_runtime/projection_shape.py`
- `seed_runtime/projection_store.py`
- `seed_runtime/projected_state_consumers.py`
- `seed_runtime/runtime_trace.py`
- `seed_runtime/execution_status.py`
- `seed_runtime/reasoning_path_audit.py`
- `seed_runtime/selection_path_audit.py`
- `seed_runtime/implementation_trait_characterization.py`
- `seed_runtime/knowledge_reachability.py`
- `seed_runtime/operational_surface_inventory.py`
- `seed_runtime/audit_snapshots.py`
- `seed_runtime/state.py`
- `seed_runtime/facts.py`
- `seed_runtime/knowledge/relationship_observation.py`
- `seed_runtime/knowledge/documentation_observation.py`
- `relationship_catalog/core.json`
- representative tests named by `rg` output, especially question, diagnostic, projection, runtime, relationship, consumer, reasoning, selection, and audit tests.

## Files changed

- `docs/implementation_relationship_grammar_investigation.md`

## LOC changed

At report creation time: one new documentation file. No implementation files were modified.

## Tests run

No code tests were required for this documentation-only implementation investigation. App surfaces were run as listed in Commands executed. No diagnostic surface, recordable output, CLI flag, registry entry, implementation behavior, or shape-audit spec was changed.

## Conclusion

Yes. The repository already possesses a coherent implementation relationship grammar, with remaining work primarily involving recovering, making explicit, and consistently exposing relationships that already recur, rather than inventing new architectural concepts. The implementation evidence supports a structural grammar based on answer responsibility, support/evidence, consumption, production, preservation, authority/boundary, derivation, selection, and downstream consumer impact.
