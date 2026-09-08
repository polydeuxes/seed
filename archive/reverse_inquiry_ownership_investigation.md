# Reverse Inquiry Ownership Investigation

## Implementation summary

This investigation is observational. It characterizes the implementation-backed relationship among Question Family, bounded dispatch surface, CLI inquiry surface, and implementation entry point. It does not redesign bounded `ask`, introduce routing, planning, semantic matching, or new aliases.

The current implementation already preserves the forward relationship in three places:

1. `BOUNDED_ASK_DISPATCH_SURFACES` maps exact Question Family strings to dispatch-surface attribute names.
2. `build_question_surface_inventory()` stores each Question Family with its surface name and CLI flag.
3. `apply_bounded_ask_dispatch()` uses the exact Question Family to set the corresponding existing CLI surface attribute, after eligibility and parameter validation.

Implementation entry points are separately declared in diagnostic shape-audit specs for the dispatch surfaces that are also diagnostic/audit-like operational surfaces. The CLI then executes those surfaces through the same evaluator/build function and formatter/JSON path used by direct CLI invocation.

## Relationship table

| Question Family | Bounded status | Dispatch surface | CLI inquiry surface | Implementation entry point |
| --- | --- | --- | --- | --- |
| operational pressure | eligible_now | `ops_brief` | `--ops-brief` | `seed_runtime/ops_brief.py::build_ops_brief` |
| current operational explanation | eligible_now | `operational_story` | `--operational-story` | `seed_runtime/operational_story.py::build_operational_story` |
| derivation explanation | eligible_with_parameters | `reasoning_path` | `--reasoning-path` | `seed_runtime/reasoning_path_audit.py::build_reasoning_path_audit` |
| selection explanation | eligible_with_parameters | `selection_path` | `--selection-path` | `seed_runtime/selection_path_audit.py::build_selection_path_audit` |
| knowledge reachability | eligible_now | `knowledge_reachability_audit` | `--knowledge-reachability-audit` | `seed_runtime/knowledge_reachability.py::build_knowledge_reachability_audit_result` |
| capability pressure | eligible_now | `capability_needs` | `--capability-needs` | `seed_runtime/capability_needs.py::build_capability_needs` |
| ownership ambiguity | eligible_now | `ownership_discrepancies` | `--ownership-discrepancies` | `seed_runtime/ownership_discrepancies.py::build_ownership_discrepancies` |
| observation domain coverage | eligible_now | `observation_domains` | `--observation-domains` | `seed_runtime/observation_domains.py::build_observation_domains` |
| observation permission state | eligible_now | `observation_permission` | `--observation-permission` | `seed_runtime/observation_permission.py::build_observation_permission` |
| authority-constrained container ownership | eligible_now | `container_ownership_authority` | `--container-ownership-authority` | `seed_runtime/container_ownership_authority.py::evaluate_container_ownership_authority_slice` |
| authority-constrained service ownership | eligible_now | `service_ownership_authority` | `--service-ownership-authority` | `seed_runtime/service_ownership_authority.py::evaluate_service_ownership_authority_slice` |
| listener endpoint reachability | eligible_now | `listener_endpoint_authority` | `--listener-endpoint-authority` | `seed_runtime/listener_endpoint_authority.py::evaluate_listener_endpoint_authority_slice` |
| surface inventory | diagnostic_only | none | `--diagnostic-inventory` | diagnostic inventory surface; not bounded-ask dispatch |
| surface shape validation | diagnostic_only | none | `--diagnostic-shape-audit` | diagnostic shape-audit surface; not bounded-ask dispatch |
| source definition/import lookup | not_dispatchable | none | `--source-navigation` | not in bounded dispatch map |
| inquiry orientation | not_dispatchable | none | `--inquiry-orientation` | not in bounded dispatch map |
| projection shape visibility | eligible_now | `projection_shape` | `--projection-shape` | `seed_runtime/projection_shape.py::build_projection_shape` |

## Reverse relationship table

For bounded-dispatch surfaces, the reverse relationship is observable by inverting the existing dispatch and inventory rows. No semantic matching is required.

| Implementation entry point | CLI inquiry surface | Dispatch surface | Question Family |
| --- | --- | --- | --- |
| `seed_runtime/ops_brief.py::build_ops_brief` | `--ops-brief` | `ops_brief` | operational pressure |
| `seed_runtime/operational_story.py::build_operational_story` | `--operational-story` | `operational_story` | current operational explanation |
| `seed_runtime/reasoning_path_audit.py::build_reasoning_path_audit` | `--reasoning-path` | `reasoning_path` | derivation explanation |
| `seed_runtime/selection_path_audit.py::build_selection_path_audit` | `--selection-path` | `selection_path` | selection explanation |
| `seed_runtime/knowledge_reachability.py::build_knowledge_reachability_audit_result` | `--knowledge-reachability-audit` | `knowledge_reachability_audit` | knowledge reachability |
| `seed_runtime/capability_needs.py::build_capability_needs` | `--capability-needs` | `capability_needs` | capability pressure |
| `seed_runtime/ownership_discrepancies.py::build_ownership_discrepancies` | `--ownership-discrepancies` | `ownership_discrepancies` | ownership ambiguity |
| `seed_runtime/observation_domains.py::build_observation_domains` | `--observation-domains` | `observation_domains` | observation domain coverage |
| `seed_runtime/observation_permission.py::build_observation_permission` | `--observation-permission` | `observation_permission` | observation permission state |
| `seed_runtime/container_ownership_authority.py::evaluate_container_ownership_authority_slice` | `--container-ownership-authority` | `container_ownership_authority` | authority-constrained container ownership |
| `seed_runtime/service_ownership_authority.py::evaluate_service_ownership_authority_slice` | `--service-ownership-authority` | `service_ownership_authority` | authority-constrained service ownership |
| `seed_runtime/listener_endpoint_authority.py::evaluate_listener_endpoint_authority_slice` | `--listener-endpoint-authority` | `listener_endpoint_authority` | listener endpoint reachability |
| `seed_runtime/projection_shape.py::build_projection_shape` | `--projection-shape` | `projection_shape` | projection shape visibility |

## Required questions

### 1. Does every bounded dispatch surface correspond to exactly one Question Family?

Yes. The observed bounded dispatch map contains 13 dispatch surfaces, and every dispatch-surface value is unique. No exception was observed.

### 2. Does every Question Family correspond to exactly one dispatch surface?

No. Among 17 Question Families, 13 have a bounded dispatch surface. Four exceptions are implementation-backed by status:

- `surface inventory` is `diagnostic_only` and points to `--diagnostic-inventory`, not bounded-ask dispatch.
- `surface shape validation` is `diagnostic_only` and points to `--diagnostic-shape-audit`, not bounded-ask dispatch.
- `source definition/import lookup` is `not_dispatchable` and has no bounded dispatch mapping.
- `inquiry orientation` is `not_dispatchable` and has no bounded dispatch mapping.

### 3. Does every dispatch surface correspond to exactly one CLI inquiry surface?

Yes for every bounded dispatch surface observed in the inventory. Each dispatch-surface name appears in exactly one inventory row, and that row contains exactly one `surface_flag`. No bounded dispatch surface mapped to multiple CLI inquiry surfaces in the Question Surface Inventory.

### 4. Are there any one Question Family to multiple dispatch surfaces relationships?

No. Each dispatchable Question Family has one value in `BOUNDED_ASK_DISPATCH_SURFACES`. Parameterized families still map to one dispatch surface; they additionally require exact `--surface-args` counts.

### 5. Are there any multiple Question Families to one dispatch surface relationships?

No. Inverting `BOUNDED_ASK_DISPATCH_SURFACES` produced no dispatch-surface value with more than one Question Family.

### 6. Are any inquiry surfaces implementation-backed but absent from the current Question Surface Inventory?

Yes. The diagnostic shape-audit implementation specs include many implementation-backed CLI surfaces absent from the Question Surface Inventory, including `classification_coverage`, `documentation_structure`, `operational_surface_inventory`, `visibility_coverage_audit`, `component_audit`, `architecture_conformance_audit`, `operational_graph`, `observation_utilization`, `capability_relationship`, `investigation_path`, `impact_audit`, `history_brief`, `reference_selection`, `repository_state_observation`, `snapshot_policy_audit`, `pressure_audit`, `correlation_audit`, `inquiry_artifacts`, and `privilege_discovery`.

This does not prove they should be added to the Question Surface Inventory. It only shows that implementation-backed operational/diagnostic CLI surfaces and Question Surface Inventory rows are not coextensive.

### 7. Can an operator determine: I know this inquiry surface. Which Question Family owns it?

Partially, using existing relationships alone. The data needed for bounded-dispatch surfaces already exists because the inventory row stores `surface_flag`, `surface`, and `question_family`, while the dispatch map stores `question_family -> dispatch_surface`. An operator can determine ownership by inspecting `seed --question-surface-inventory` / `seed ask --question-families` output or JSON and matching an exact CLI flag.

However, there is no dedicated reverse lookup presentation in the current implementation. Reverse lookup would need new visibility if the desired operator workflow is direct lookup by known inquiry surface. It would not need new routing or semantic ownership information for the 13 bounded dispatch surfaces.

### 8. If a reverse lookup were exposed, would it simply surface existing implementation relationships, or introduce a new architectural responsibility?

For the 13 bounded dispatch surfaces, it would simply surface existing implementation relationships. The implementation already has exact Question Family strings, exact dispatch-surface names, exact CLI flags, required surface arguments, and implementation entry points in shape specs. A reverse presentation could be built by deterministic inversion of existing maps and rows.

It would become a new architectural responsibility only if it attempted to classify arbitrary CLI surfaces into Question Families, infer missing Question Family ownership for the implementation-backed surfaces absent from the inventory, add fuzzy matching, or introduce new aliases. Those behaviors are not present in the current bounded-ask implementation evidence.

## Relationship cardinality analysis

Observed bounded-dispatch cardinalities:

| Relationship | Cardinality | Evidence-backed exceptions |
| --- | --- | --- |
| Question Family -> dispatch surface | 1 -> 1 for 13 dispatchable families | Four Question Families have no bounded dispatch surface: two `diagnostic_only`, two `not_dispatchable`. |
| Dispatch surface -> Question Family | 1 -> 1 | None observed. |
| Dispatch surface -> CLI inquiry surface | 1 -> 1 | None observed within Question Surface Inventory. |
| CLI inquiry surface -> dispatch surface | 1 -> 1 for dispatchable rows | Diagnostic-only and not-dispatchable rows have CLI flags without bounded dispatch surfaces. |
| Question Family -> CLI inquiry surface | 1 -> 1 across all 17 inventory rows | No duplicate `surface` values were observed. |
| Implementation entry point -> Question Family | 1 -> 1 for bounded dispatch surfaces with shape-audit specs | Diagnostic-only/not-dispatchable rows are outside bounded dispatch. Many shape-audit specs are outside Question Surface Inventory. |

## Implementation-backed inconsistencies

- The Question Surface Inventory and diagnostic shape-audit specs are overlapping but not identical registries. The inventory contains Question Families; the shape-audit specs contain many operational/diagnostic implementation-backed surfaces that are not Question Families.
- `surface inventory` and `surface shape validation` are inventory rows with CLI flags, but their bounded status is `diagnostic_only`; they are intentionally not dispatchable by bounded `ask`.
- `source definition/import lookup` and `inquiry orientation` are inventory rows with CLI flags, but their bounded status is `not_dispatchable`; they have no bounded dispatch mapping in the current implementation.
- Reverse ownership for dispatchable inquiry surfaces is implicit and exact, but not directly presented as a reverse lookup surface.

## Commands executed

- `pwd && rg --files -g 'AGENTS.md' -g '!/.git' && git status --short`
- `cat AGENTS.md && git status --short`
- `rg -n "Question Family|question family|bounded|dispatch surface|surface inventory|Question Surface|ask" .`
- `sed -n '1,430p' seed_runtime/question_surface_inventory.py && sed -n '1,260p' seed_runtime/bounded_ask.py 2>/dev/null || true && rg -n "QUESTION|bounded.*dispatch|question_family|--question-family|ask" seed_runtime tests/test_question_surface_inventory.py seed_local.py`
- `rg --files | rg 'seed_local|seed-local|cli|__main__' && rg -n "def main|question_family|BOUNDED_ASK_DISPATCH|ops_brief|service_ownership" .`
- `sed -n '2080,2190p' scripts/seed_local.py; sed -n '6200,6620p' scripts/seed_local.py; sed -n '130,190p' scripts/seed_local.py; sed -n '130,520p' seed_runtime/diagnostic_shape_audit.py`
- `python - <<'PY' ... PY` to build the relationship table from `build_question_surface_inventory()`, `BOUNDED_ASK_DISPATCH_SURFACES`, and `IMPLEMENTATION_SPECS`.

## Files inspected

- `AGENTS.md`
- `seed_runtime/question_surface_inventory.py`
- `scripts/seed_local.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `tests/test_question_surface_inventory.py`
- Existing related docs surfaced by repository search, including `docs/ask_question_family_dispatch_reconciliation.md`, `docs/bounded_ask_routing_reconciliation.md`, and `docs/question_family_artifact_reconciliation.md`.

## Files changed

- `docs/reverse_inquiry_ownership_investigation.md`

## LOC changed

- Added 157 lines.

## Tests run

- `pytest -q tests/test_question_surface_inventory.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

## Conclusion

Reverse inquiry ownership for current bounded dispatch surfaces is existing implementation visibility, not new architecture.

The existing implementation already contains the exact forward relationship from Question Family to dispatch surface to CLI inquiry surface to implementation entry point. Inverting that relationship for the 13 bounded dispatch surfaces would expose existing relationships. It would become new architecture only if it tried to assign Question Family ownership to implementation-backed surfaces currently absent from the Question Surface Inventory, or if it introduced semantic matching, aliases, routing, planning, or recommendations.
