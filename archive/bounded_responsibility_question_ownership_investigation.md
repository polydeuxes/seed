# Bounded Responsibility Question Ownership Investigation

## Implementation summary

This implementation investigation used current app output and implementation files to ask whether Seed already preserves enough implementation-backed evidence to answer:

```text
Which bounded responsibility owns this question?
```

The answer is **partially yes**. For the 17 current Question Family rows, the implementation already preserves a row-level `answer_responsibility`, a primary `surface`, an `authority_boundary`, and a canonical diagnostic relationship when one exists. For the 13 families in bounded `ask` dispatch, Seed can also traverse an implementation-backed path from exact `Question Family` to `dispatch_surface` to the implementation surface. For two diagnostic-only families, Seed preserves the owning diagnostic surfaces but intentionally does not make them bounded ask dispatch targets. For two not-dispatchable families, implementation evidence stops at the Question Surface Inventory row: there is a named surface and answer responsibility, but no bounded ask dispatch mapping and no diagnostic inventory/shape-audit relationship.

No new inventory, Question Family, CLI surface, responsibility category, or runtime work taxonomy was added. This document records findings only.

## Documents reviewed

- `docs/question_ownership_responsibility_reconciliation.md`
- `docs/question_family_inclusion_evidence_investigation.md`
- `docs/work_responsibility_reconciliation.md`
- `docs/bounded_ask_question_family_eligibility_audit.md`
- `docs/answer_responsibility_implementation_characterization.md`
- `docs/answer_responsibility_auditability_investigation.md`
- `docs/responsibility_ownership_organization_reconciliation.md`
- `docs/local_cli_responsibility_boundary_audit.md`
- `docs/repository_navigation_question_surface_discoverability_investigation.md`

## Implementation files inspected

- `seed_runtime/question_surface_inventory.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `scripts/seed_local.py`
- `tests/test_question_surface_inventory.py`
- `tests/test_diagnostic_inventory.py`
- `tests/test_diagnostic_shape_audit.py`

## Implementation evidence recovered

The direct implementation chain is:

```text
QuestionSurfaceInventoryRow.question_family
↓
QuestionSurfaceInventoryRow.surface / answer_responsibility / authority_boundary
↓
BOUNDED_ASK_DISPATCH_SURFACES, when present
↓
canonical_diagnostic_surface(...)
↓
DIAGNOSTIC_INVENTORY entry, when present
↓
IMPLEMENTATION_SPECS entry, when present
```

`QuestionSurfaceInventoryRow` is the strongest current owner-like artifact because it preserves `question_family`, examples, `surface`, CLI flag, `answer_responsibility`, `authority_boundary`, bounded status, dispatch surface, formatter name, canonical diagnostic surface, diagnostic inventory name, shape spec name, and relationship status.

Bounded ask dispatch is exact-family dispatch, not semantic routing. The CLI maps `ask --question-family` to an existing inquiry surface only when the family is in `BOUNDED_ASK_DISPATCH_SURFACES`; it rejects diagnostic-only and not-dispatchable families.

Diagnostic Inventory and Diagnostic Shape Audit add stronger operational evidence for surfaces that are registered diagnostics: declared JSON/record/event-ledger/mutation shape plus module/build/format/json/record implementation specs. They do not themselves introduce Question Family ownership.

## Responsibility relationship table

| Question Family | Answer responsibility | Responsibility owner evidence | Authority boundary | Dispatch surface | Canonical diagnostic surface | Diagnostic inventory entry | Diagnostic shape spec | Can Seed identify owner from implementation? |
|---|---|---|---|---|---|---|---|---|
| operational pressure | compact operational pressure and visibility summary | `ops_brief` surface row | read-only summary assembled from existing audits; no recording; no mutation | `ops_brief` | `ops_brief` | `ops_brief` | `ops_brief` | Yes: `ops_brief`. |
| current operational explanation | broad operational explanation from existing evidence, pressure, constraints, outcomes, and investigation path | `operational_story` surface row | read-only view; no recording; no event-ledger writes; no cluster mutation | `operational_story` | `operational_story` | `operational_story` | `operational_story` | Yes: `operational_story`. |
| derivation explanation | evidence-backed derivation path from source evidence through conclusions and consumers | `reasoning_path` surface row | read-only audit; no recording; no event-ledger writes; no cluster mutation | `reasoning_path` | `reasoning_path` | `reasoning_path` | `reasoning_path` | Yes: `reasoning_path`, with required `domain` and `subject`. |
| selection explanation | implementation-backed selection path with candidates, factors, alternatives, and outcome | `selection_path` surface row | read-only audit; no recording; no event-ledger writes; no cluster mutation | `selection_path` | `selection_path` | `selection_path` | `selection_path` | Yes: `selection_path`, with required `target`. |
| knowledge reachability | audits reachability across preserved, projected, read-model, inquiry, and rendered surfaces | `knowledge_reachability` surface row | read-only audit over projected and repository evidence; no recording; no mutation | `knowledge_reachability_audit` | `knowledge_reachability` | `knowledge_reachability` | `knowledge_reachability` | Yes: `knowledge_reachability`; dispatch uses the audited alias. |
| capability pressure | reports recorded diagnostic capability needs by subject | `capability_needs` surface row | read-only diagnostic-fact reader; no recording; no event-ledger writes; no cluster mutation | `capability_needs` | `capability_needs` | `capability_needs` | `capability_needs` | Yes: `capability_needs`. |
| ownership ambiguity | reports storage/service ownership candidates, conflicts, ambiguity, and capability needs | `ownership_discrepancies` surface row | read-only unless `--record` is supplied; default row describes non-recording use | `ownership_discrepancies` | `ownership_discrepancies` | `ownership_discrepancies` | `ownership_discrepancies` | Yes: `ownership_discrepancies`. |
| observation domain coverage | shows observation-domain coverage and gap visibility derived from existing evidence | `observation_domains` surface row | read-only surface; no recording; no event-ledger writes; no cluster mutation | `observation_domains` | `observation_domains` | `observation_domains` | `observation_domains` | Yes: `observation_domains`. |
| observation permission state | shows observation-domain permission classes, authority evidence, unknowns, and manual-invocation reasoning | `observation_permission` surface row | read-only visibility; no enforcement; no approval storage; no autonomous runtime behavior | `observation_permission` | `observation_permission` | `observation_permission` | `observation_permission` | Yes: `observation_permission`. |
| authority-constrained container ownership | evaluates container ownership reachability under the constrained authority profile | `container_ownership_authority` surface row | read-only evaluator; no provider acquisition; no permission creation; no execution; no mutation | `container_ownership_authority` | `container_ownership_authority` | `container_ownership_authority` | `container_ownership_authority` | Yes: `container_ownership_authority`. |
| authority-constrained service ownership | evaluates service ownership reachability under constrained authority and implementation inventory evidence | `service_ownership_authority` surface row | read-only evaluator; no provider acquisition; no execution; no event-ledger writes; no mutation | `service_ownership_authority` | `service_ownership_authority` | `service_ownership_authority` | `service_ownership_authority` | Yes: `service_ownership_authority`. |
| listener endpoint reachability | evaluates local TCP/UDP listener endpoint authority and reachability | `listener_endpoint_authority` surface row | read-only evaluator; no provider acquisition; no execution; no event-ledger writes; no mutation | `listener_endpoint_authority` | `listener_endpoint_authority` | `listener_endpoint_authority` | `listener_endpoint_authority` | Yes: `listener_endpoint_authority`. |
| surface inventory | lists diagnostic/test-like operational surfaces and declared behavior shape | `diagnostic_inventory` surface row | read-only static registry; no recording; no event-ledger writes; no cluster mutation | absent | `diagnostic_inventory` | `diagnostic_inventory` | `diagnostic_inventory` | Yes for the inventory question: `diagnostic_inventory`; not a bounded ask target. |
| surface shape validation | compares diagnostic registry declarations with static implementation shape | `diagnostic_shape_audit` surface row | read-only static implementation audit; no recording; no event-ledger writes; no cluster mutation | absent | `diagnostic_shape_audit` | `diagnostic_shape_audit` | `diagnostic_shape_audit` | Yes for the validation question: `diagnostic_shape_audit`; not a bounded ask target. |
| source definition/import lookup | looks up preserved imports and definitions from projected facts | `source_navigation` surface row | read-only projected-fact view; does not inspect repository files, parse source, or append events | absent | `source_navigation` | absent | absent | Partially: inventory names `source_navigation`, but bounded dispatch and diagnostic validation are absent. |
| inquiry orientation | renders a bounded read-only orientation view for an inquiry note | `inquiry_orientation` surface row | read-only orientation over existing inquiry note and projected state; no routing; no execution | absent | `inquiry_orientation` | absent | absent | Partially: inventory names `inquiry_orientation`, but bounded dispatch and diagnostic validation are absent. |
| projection shape visibility | shows implementation-backed projection stage shape | `projection_shape` surface row | read-only implementation-backed view; no recording; no event-ledger writes; no cluster mutation | `projection_shape` | `projection_shape` | `projection_shape` | `projection_shape` | Yes: `projection_shape`. |

## Question Family to responsibility mappings

Current implementation preserves these mappings directly in the Question Surface Inventory:

- `operational pressure` → `ops_brief` → compact operational pressure and visibility summary.
- `current operational explanation` → `operational_story` → broad operational explanation.
- `derivation explanation` → `reasoning_path` → evidence-backed derivation path.
- `selection explanation` → `selection_path` → implementation-backed selection path.
- `knowledge reachability` → `knowledge_reachability` → reachability audit across preserved/projected/read-model/inquiry/rendered surfaces.
- `capability pressure` → `capability_needs` → recorded diagnostic capability needs.
- `ownership ambiguity` → `ownership_discrepancies` → ownership candidates, conflicts, ambiguity, and capability needs.
- `observation domain coverage` → `observation_domains` → observation-domain coverage and gaps.
- `observation permission state` → `observation_permission` → permission classes, authority evidence, unknowns, and manual-invocation reasoning.
- `authority-constrained container ownership` → `container_ownership_authority` → constrained authority container-ownership reachability.
- `authority-constrained service ownership` → `service_ownership_authority` → constrained authority service-ownership reachability.
- `listener endpoint reachability` → `listener_endpoint_authority` → local TCP/UDP listener endpoint authority and reachability.
- `surface inventory` → `diagnostic_inventory` → diagnostic/test-like operational surface declaration shape.
- `surface shape validation` → `diagnostic_shape_audit` → diagnostic registry versus implementation shape validation.
- `source definition/import lookup` → `source_navigation` → projected import/definition lookup; not bounded-dispatchable today.
- `inquiry orientation` → `inquiry_orientation` → inquiry-note orientation view; not bounded-dispatchable today.
- `projection shape visibility` → `projection_shape` → implementation-backed projection stage visibility.

## Required question answers

### 1. Per-family preserved evidence

Every current Question Family preserves answer responsibility, a surface row, an authority boundary, a surface flag, bounded status, formatter name, canonical diagnostic surface field, diagnostic inventory field, diagnostic shape spec field, implementation reason, and relationship status. Dispatch surface is present only for the 13 bounded-dispatch families. Diagnostic Inventory and Diagnostic Shape Audit relationships are present for 15 families: all except `source definition/import lookup` and `inquiry orientation`.

### 2. Distinction or collapse among Question Family, Answer Surface, Bounded Responsibility, and Implementation Owner

The implementation distinguishes these concepts partially:

- `Question Family` is the row key in `QuestionSurfaceInventoryRow`.
- `Answer Surface` is the row's `surface` and CLI flag.
- `Bounded Responsibility` is currently a prose field, `answer_responsibility`, attached to the row.
- `Implementation Owner` is not a separate normalized field. In current implementation it collapses into the named `surface` and, when diagnostic-backed, the diagnostic shape spec's module/build/format/json functions.

Therefore, Seed can say which surface owns an answer responsibility, but it cannot independently name a separate owner object beyond the surface/module/spec chain.

### 3. Can Seed determine who owns answering each question?

Yes for 13 bounded-dispatch families: the exact family maps to one dispatch surface and that surface maps to diagnostic inventory and shape-audit evidence. Yes for the two diagnostic-only families if the question is about those diagnostics themselves, but not through bounded `ask`. Partially for `source definition/import lookup` and `inquiry orientation`: the inventory names an answering surface and responsibility, but implementation-backed evidence stops before bounded ask dispatch, Diagnostic Inventory registration, and Diagnostic Shape Audit validation.

### 4. Where responsibility is attached today

Responsibility today is attached primarily to **surface/subsystem pairs**:

- Question answer responsibility is attached to Question Surface Inventory rows by question family and surface.
- Diagnostic responsibility is attached to Diagnostic Inventory entries by diagnostic surface and CLI flag.
- Implementation shape responsibility is attached to Diagnostic Shape Audit specs by diagnostic name and module/functions.
- Runtime/service/projection responsibilities are documented and implemented separately in runtime, projection, event-ledger, tool-execution, observation, and pending-action code; those are not represented as Question Family rows unless surfaced by a current question-family inventory row.

The investigation did not find responsibility primarily attached to individual natural-language questions, views alone, formatters alone, projections alone, or read models alone. Formatters and read models contribute evidence to a surface's answer shape, but the owner-like artifact is the surface/subsystem row or implementation spec.

### 5. Shared bounded responsibilities

Multiple Question Families share the same broad bounded-responsibility pattern: a read-only diagnostic or inquiry surface owns an operator-facing answer while preserving no-record/no-mutation authority boundaries. However, current implementation does **not** normalize a shared responsibility category field across families. It preserves repeated responsibility text and repeated Diagnostic Inventory shape fields, not a distinct shared-responsibility object.

Implementation-backed sharing that can be stated safely:

- `derivation explanation`, `selection explanation`, `current operational explanation`, and `operational pressure` share operational-explanation contributors and are read-only answer surfaces, but each has its own surface owner.
- `authority-constrained container ownership`, `authority-constrained service ownership`, and `listener endpoint reachability` share constrained-authority evaluator shape and diagnostic validation, but each has its own surface owner.
- `surface inventory` and `surface shape validation` share diagnostic-visibility responsibility boundaries, but they remain distinct surfaces: declaration versus validation.

No stronger shared bounded-responsibility identity is implementation-normalized today.

### 6. Are all current responsibilities reachable through Question Family → Dispatch → Implementation?

No. The 13 bounded-dispatch families are reachable through that chain. Two diagnostic-only families intentionally stop before bounded dispatch, although their diagnostic implementation is reachable through Diagnostic Inventory and Diagnostic Shape Audit. Two Question Families stop at inventory row plus surface name because there is no bounded dispatch mapping and no diagnostic validation relationship.

Additionally, many diagnostic responsibilities are not Question Families and therefore are unreachable from current bounded inquiry. Examples include `classification_coverage`, `graph_issue_summary`, `documentation_structure`, `operational_surface_inventory`, `visibility_coverage_audit`, `consumer_audit`, `emitter_consumer_audit`, `component_audit`, `architecture_conformance_audit`, `operational_graph`, `observation_utilization`, `capability_relationship`, `investigation_path`, `impact_audit`, `history_brief`, `reference_selection`, `repository_state_observation`, `snapshot_policy_audit`, `pressure_audit`, `correlation_audit`, `question_surface_inventory`, `inquiry_artifacts`, `projected_state_consumers`, `implementation_trait_characterization`, and `privilege_discovery`.

### 7. Implementation-backed responsibilities with no Question Family or bounded inquiry path

Yes. Diagnostic Inventory preserves implementation-backed responsibilities for many operational surfaces that have no Question Family row and no bounded `ask` path. These responsibilities have CLI flags, diagnostic descriptions, JSON/record/event-ledger/mutation declarations, and often shape-audit specs, but no `QuestionSurfaceInventoryRow.question_family`, example questions, or bounded dispatch mapping.

This is evidence of implementation-backed operational responsibility, not evidence that those surfaces should become Question Families.

### 8. Where responsibility ownership is recovered from

Ownership is recovered from a combination:

1. Question Surface Inventory provides the row-level family-to-surface-to-responsibility mapping.
2. Bounded ask dispatch maps provide executable exact-family dispatch for 13 families.
3. Diagnostic Inventory provides operational shape and boundary declarations for registered surfaces.
4. Diagnostic Shape Audit provides module/function implementation validation for registered surfaces.
5. Implementation code and tests prove the CLI dispatch and inventory/audit consistency.
6. Documentation explains the interpretation, but recurring prose alone was not treated as implementation fact.

### 9. Enough evidence to answer the target question?

For a current exact Question Family in bounded ask dispatch, yes. The smallest truthful answer Seed could currently provide is:

```text
The bounded responsibility for <question_family> is owned by the <surface> answer surface, whose declared responsibility is <answer_responsibility>, within <authority_boundary>.
```

For diagnostic-only families, the truthful answer must add:

```text
This is a diagnostic visibility surface, not a bounded ask dispatch target.
```

For `source definition/import lookup` and `inquiry orientation`, implementation-backed evidence stops after the Question Surface Inventory row and surface name. The first missing implementation-backed relationship is bounded dispatch plus diagnostic inventory/shape-audit validation for those surfaces.

### 10. Does ownership compose with the recent relationship chain?

Mostly, but not universally. The chain composes for the 13 bounded-dispatch families that also have diagnostic inventory and shape-audit specs, and it composes diagnostically for the two diagnostic-only families without bounded `ask`. It does not compose for the two not-dispatchable families.

The actual implementation-backed ownership structure is therefore:

```text
Question Family
↓
Question Surface Inventory row
↓
Surface + answer_responsibility + authority_boundary
↓
optional bounded ask dispatch
↓
optional canonical diagnostic surface
↓
optional Diagnostic Inventory entry
↓
optional Diagnostic Shape Audit spec
↓
module/build/format/json implementation evidence
```

This differs slightly from a mandatory chain because dispatch and diagnostic validation are optional relationships in the current implementation.

## Shared responsibility findings

- Current sharing is by repeated surface shape and boundary, not by a normalized shared responsibility object.
- Read-only diagnostic/inquiry boundaries recur across many families.
- Authority-constrained evaluator shape recurs across container ownership, service ownership, and listener endpoint reachability.
- Explanation/selection/pressure surfaces share operational evidence contributors but remain separate answer owners.

## Unreachable responsibilities

Unreachable from current `Question Family → Dispatch → Implementation` means either no bounded dispatch or no Question Family row.

- Question Families without bounded dispatch: `surface inventory`, `surface shape validation`, `source definition/import lookup`, `inquiry orientation`.
- Question Families without diagnostic inventory/shape validation: `source definition/import lookup`, `inquiry orientation`.
- Diagnostic responsibilities with no Question Family row: `classification_coverage`, `graph_issue_summary`, `documentation_structure`, `audit_snapshot`, `audit_snapshots`, `audit_compare`, `operational_surface_inventory`, `visibility_coverage_audit`, `operational_surface_classification_audit`, `consumer_audit`, `emitter_consumer_audit`, `emitter_attribution_audit`, `component_audit`, `architecture_conformance_audit`, `operational_graph`, `operational_graph_taxonomy`, `operational_graph_confidence`, `observation_utilization`, `capability_relationship`, `investigation_path`, `current_facts_cache_debug`, `impact_audit`, `history_brief`, `reference_selection`, `repository_state_observation`, `snapshot_policy_audit`, `pressure_audit`, `correlation_audit`, `question_surface_inventory`, `inquiry_artifacts`, `projected_state_consumers`, `implementation_trait_characterization`, `privilege_discovery`.

## Implementation-backed gaps

- There is no separate normalized `implementation_owner` field for Question Families; owner currently collapses into surface plus diagnostic implementation spec where present.
- There is no normalized `bounded_responsibility` identifier distinct from prose `answer_responsibility`.
- There is no implementation-backed general discriminator proving why all and only current inventory rows are Question Families.
- `source_definition/import lookup` and `inquiry orientation` have inventory owner rows but no bounded ask dispatch and no diagnostic registry/shape-audit connection.
- Many diagnostic responsibilities are implementation-backed but not reachable as Question Families.

## Agreements with previous reconciliations

- The investigation agrees that responsibility, ownership, and authority are separate: responsibility is the answer contract, ownership is the primary surface/subsystem boundary, and authority is the constraint on what may be claimed.
- It agrees that contributors do not automatically become owners; the answer owner is the surface that emits the bounded answer shape.
- It agrees that critical/background/maintenance/optional work are not established implementation categories here.
- It agrees that Question Family inclusion is only partially recoverable from implementation evidence alone.
- It agrees that presentation vocabulary should not be promoted into knowledge or responsibility without implementation evidence.

## Contradictions discovered

No implementation contradiction was found against the recent reconciliations. The main precision point is that the chain from Question Family to Diagnostic Shape Audit is not mandatory for every current row; two rows lack diagnostic connections and two rows are diagnostic-only rather than bounded-dispatchable.

## Unresolved implementation questions

- Whether a future implementation should expose a separate `implementation_owner` or bounded-responsibility identifier is not answered by current code.
- Whether diagnostic-only surfaces should ever be ask-dispatchable is not answered by current code.
- Whether diagnostic responsibilities outside the Question Surface Inventory should remain outside Question Families is not derivable from implementation evidence alone.

## Commands executed

- `pwd && rg --files -g 'AGENTS.md' -g '!*.pyc' -g '!__pycache__' && git status --short`
- `cat AGENTS.md && rg -n "Question Family|Question Surface|Diagnostic Inventory|bounded|responsibility|authority|diagnostic-shape|diagnostic-inventory" -S .`
- `find . -maxdepth 3 -type f | sed 's#^./##' | sort | head -200`
- `rg -n "QUESTION|QuestionFamily|question_family|family|bounded ask|ask" seed_runtime tests docs/*question* docs/*responsibility* -S`
- `sed -n '1,460p' seed_runtime/question_surface_inventory.py && sed -n '1,260p' seed_runtime/diagnostic_inventory.py && sed -n '1,220p' seed_runtime/diagnostic_shape_audit.py`
- `python scripts/seed_local.py ask --question-families --json`
- `python scripts/seed_local.py --diagnostic-inventory --json`
- `python scripts/seed_local.py --diagnostic-shape-audit --json`
- `rg -n "BOUNDED_ASK|question_family|--question-family|dispatch_surface|operational_story|ops_brief|reasoning_path|selection_path" scripts/seed_local.py seed_runtime/question_surface_inventory.py tests/test_question_surface_inventory.py seed_runtime/diagnostic_inventory.py seed_runtime/diagnostic_shape_audit.py`
- `sed -n '1,140p' docs/question_ownership_responsibility_reconciliation.md && sed -n '1,120p' docs/question_family_inclusion_evidence_investigation.md && sed -n '1,120p' docs/work_responsibility_reconciliation.md`
- `python - <<'PY' ... build_question_surface_inventory responsibility table ... PY`
- `python - <<'PY' ... diagnostic responsibilities outside Question Families ... PY`

## Files changed

- `docs/bounded_responsibility_question_ownership_investigation.md`

## LOC changed

- Added this investigation document only.

## Tests run

- Not run. This is a documentation-only implementation investigation and does not change code, CLI surfaces, inventories, or executable behavior.

## Conclusion

Can the repository currently answer:

```text
Which bounded responsibility owns this question?
```

using implementation-backed evidence alone?

**Partially yes.** For current exact Question Families with bounded ask dispatch, Seed can answer from implementation-backed evidence alone: the owner is the mapped answer surface, with the row's answer responsibility and authority boundary, backed by diagnostic inventory and shape-audit specs. For diagnostic-only Question Families, Seed can identify the diagnostic owner but must say the family is not a bounded ask dispatch target. For `source definition/import lookup` and `inquiry orientation`, Seed can identify only the inventory-declared surface and responsibility; implementation-backed evidence stops before bounded dispatch and diagnostic validation. For diagnostic responsibilities outside the Question Surface Inventory, current implementation preserves responsibility but no Question Family or bounded inquiry path.
