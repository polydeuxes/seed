# Question Family Inclusion Evidence Investigation

This observational investigation uses current implementation output only. It does not propose promotion rules or new Question Families.

## Commands executed

- `python scripts/seed_local.py --question-surface-inventory --json`
- `python scripts/seed_local.py --diagnostic-inventory --json`
- `python scripts/seed_local.py --diagnostic-shape-audit --json`
- `pytest -q tests/test_question_surface_inventory.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

## Implementation summary

- Current Question Family inventory contains 17 rows.
- Diagnostic inventory contains 44 implementation-backed diagnostic or operational inquiry surfaces.
- 31 diagnostic inventory rows are implementation-backed inquiry surfaces outside the Question Surface Inventory by surface-name comparison.
- The inventory itself preserves CLI surface, answer responsibility, boundary, JSON support, human formatter name, bounded eligibility, dispatch surface when mapped, required surface arguments when mapped, and an implementation reason.
- Diagnostic registration and shape-audit specs preserve additional implementation validation for diagnostic surfaces, including record/event-ledger/cluster-mutation shape.

## Question Family implementation evidence

| Surface/family | Implementation surface | CLI inquiry surface | Dispatch surface | Bounded eligibility | Required args | Human formatter | JSON | Answer responsibility | Boundary | Authority/expectation set | Diagnostic registration | Implementation validation |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| operational pressure | ops_brief | --ops-brief | ops_brief | eligible_now | absent | format_ops_brief | yes | present | present | present | yes | yes |
| current operational explanation | operational_story | --operational-story | operational_story | eligible_now | absent | format_operational_story | yes | present | present | present | yes | yes |
| derivation explanation | reasoning_path | --reasoning-path | reasoning_path | eligible_with_parameters | domain, subject | format_reasoning_path | yes | present | present | present | yes | yes |
| selection explanation | selection_path | --selection-path | selection_path | eligible_with_parameters | target | format_selection_path | yes | present | present | present | yes | yes |
| knowledge reachability | knowledge_reachability | --knowledge-reachability-audit | knowledge_reachability_audit | eligible_now | absent | format_knowledge_reachability | yes | present | present | present | yes | yes |
| capability pressure | capability_needs | --capability-needs | capability_needs | eligible_now | absent | format_capability_needs | yes | present | present | present | yes | yes |
| ownership ambiguity | ownership_discrepancies | --ownership-discrepancies | ownership_discrepancies | eligible_now | absent | format_ownership_discrepancies | yes | present | present | present | yes | yes |
| observation domain coverage | observation_domains | --observation-domains | observation_domains | eligible_now | absent | format_observation_domains | yes | present | present | present | yes | yes |
| observation permission state | observation_permission | --observation-permission | observation_permission | eligible_now | absent | format_observation_permission | yes | present | present | present | yes | yes |
| authority-constrained container ownership | container_ownership_authority | --container-ownership-authority | container_ownership_authority | eligible_now | absent | format_container_ownership_authority | yes | present | present | present | yes | yes |
| authority-constrained service ownership | service_ownership_authority | --service-ownership-authority | service_ownership_authority | eligible_now | absent | format_service_ownership_authority | yes | present | present | present | yes | yes |
| listener endpoint reachability | listener_endpoint_authority | --listener-endpoint-authority | listener_endpoint_authority | eligible_now | absent | format_listener_endpoint_authority | yes | present | present | present | yes | yes |
| surface inventory | diagnostic_inventory | --diagnostic-inventory | absent | diagnostic_only | absent | format_diagnostic_inventory | yes | present | present | present | no | no |
| surface shape validation | diagnostic_shape_audit | --diagnostic-shape-audit | absent | diagnostic_only | absent | format_diagnostic_shape_audit | yes | present | present | present | no | no |
| source definition/import lookup | source_navigation | --source-navigation | absent | not_dispatchable | absent | format_source_navigation | yes | present | present | present | no | no |
| inquiry orientation | inquiry_orientation | --inquiry-orientation | absent | not_dispatchable | absent | format_inquiry_orientation | yes | present | present | present | no | no |
| projection shape visibility | projection_shape | --projection-shape | projection_shape | eligible_now | absent | format_projection_shape | yes | present | present | present | yes | yes |

## Implementation-backed inquiry surfaces outside the Question Surface Inventory

| Surface/family | Implementation surface | CLI inquiry surface | Dispatch surface | Bounded eligibility | Required args | Human formatter | JSON | Answer responsibility | Boundary | Authority/expectation set | Diagnostic registration | Implementation validation |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| classification_coverage | --classification-coverage | absent | absent | absent | absent | varies/unknown | no | description present | diagnostic boundary present | diagnostic registry | yes | yes |
| graph_issue_summary | --graph-issue-summary | absent | absent | absent | absent | varies/unknown | no | description present | diagnostic boundary present | diagnostic registry | yes | yes |
| documentation_structure | --documentation-structure, --document, --missing-front-matter, --missing-trailing-newline, --empty-sections, --sections, --links, --code-fences, --recurrence, --rare, --missing-common-sections, --outliers, --skeletons, --where, --membership, --limit, --top, --summary-only, --min-count, --max-count | absent | absent | absent | absent | varies/unknown | yes | description present | diagnostic boundary present | diagnostic registry | yes | yes |
| audit_snapshot | --audit-snapshot | absent | absent | absent | absent | varies/unknown | no | description present | diagnostic boundary present | diagnostic registry | yes | yes |
| audit_snapshots | --audit-snapshots | absent | absent | absent | absent | varies/unknown | no | description present | diagnostic boundary present | diagnostic registry | yes | yes |
| audit_compare | --audit-compare | absent | absent | absent | absent | varies/unknown | yes | description present | diagnostic boundary present | diagnostic registry | yes | yes |
| operational_surface_inventory | --operational-surface-inventory | absent | absent | absent | absent | varies/unknown | yes | description present | diagnostic boundary present | diagnostic registry | yes | yes |
| visibility_coverage_audit | --visibility-coverage-audit | absent | absent | absent | absent | varies/unknown | yes | description present | diagnostic boundary present | diagnostic registry | yes | yes |
| operational_surface_classification_audit | --operational-surface-classification-audit | absent | absent | absent | absent | varies/unknown | yes | description present | diagnostic boundary present | diagnostic registry | yes | yes |
| consumer_audit | --consumer-audit | absent | absent | absent | absent | varies/unknown | yes | description present | diagnostic boundary present | diagnostic registry | yes | yes |
| emitter_consumer_audit | --emitter-consumer-audit, --include-rendered | absent | absent | absent | absent | varies/unknown | yes | description present | diagnostic boundary present | diagnostic registry | yes | yes |
| emitter_attribution_audit | --emitter-attribution-audit, --include-rendered | absent | absent | absent | absent | varies/unknown | yes | description present | diagnostic boundary present | diagnostic registry | yes | yes |
| component_audit | --component-audit | absent | absent | absent | absent | varies/unknown | yes | description present | diagnostic boundary present | diagnostic registry | yes | yes |
| architecture_conformance_audit | --architecture-conformance-audit | absent | absent | absent | absent | varies/unknown | yes | description present | diagnostic boundary present | diagnostic registry | yes | yes |
| operational_graph | --operational-graph | absent | absent | absent | absent | varies/unknown | yes | description present | diagnostic boundary present | diagnostic registry | yes | yes |
| operational_graph_taxonomy | --operational-graph-taxonomy | absent | absent | absent | absent | varies/unknown | yes | description present | diagnostic boundary present | diagnostic registry | yes | yes |
| operational_graph_confidence | --operational-graph-confidence, --exclude-aggregate | absent | absent | absent | absent | varies/unknown | yes | description present | diagnostic boundary present | diagnostic registry | yes | yes |
| observation_utilization | --observation-utilization | absent | absent | absent | absent | varies/unknown | yes | description present | diagnostic boundary present | diagnostic registry | yes | yes |
| capability_relationship | --capability-relationship | absent | absent | absent | absent | varies/unknown | yes | description present | diagnostic boundary present | diagnostic registry | yes | yes |
| investigation_path | --investigation-path | absent | absent | absent | absent | varies/unknown | yes | description present | diagnostic boundary present | diagnostic registry | yes | yes |
| current_facts_cache_debug | --current-facts-cache-debug | absent | absent | absent | absent | varies/unknown | no | description present | diagnostic boundary present | diagnostic registry | yes | yes |
| impact_audit | --impact-audit | absent | absent | absent | absent | varies/unknown | yes | description present | diagnostic boundary present | diagnostic registry | yes | yes |
| history_brief | --history-brief | absent | absent | absent | absent | varies/unknown | yes | description present | diagnostic boundary present | diagnostic registry | yes | yes |
| reference_selection | --reference-selection | absent | absent | absent | absent | varies/unknown | yes | description present | diagnostic boundary present | diagnostic registry | yes | yes |
| repository_state_observation | --observe-repository | absent | absent | absent | absent | varies/unknown | yes | description present | diagnostic boundary present | diagnostic registry | yes | yes |
| snapshot_policy_audit | --snapshot-policy-audit | absent | absent | absent | absent | varies/unknown | yes | description present | diagnostic boundary present | diagnostic registry | yes | yes |
| pressure_audit | --pressure-audit | absent | absent | absent | absent | varies/unknown | yes | description present | diagnostic boundary present | diagnostic registry | yes | yes |
| correlation_audit | --correlation-audit | absent | absent | absent | absent | varies/unknown | yes | description present | diagnostic boundary present | diagnostic registry | yes | yes |
| question_surface_inventory | --question-surface-inventory, ask --question-families | absent | absent | absent | absent | varies/unknown | yes | description present | diagnostic boundary present | diagnostic registry | yes | yes |
| inquiry_artifacts | --inquiry-artifacts | absent | absent | absent | absent | varies/unknown | yes | description present | diagnostic boundary present | diagnostic registry | yes | yes |
| privilege_discovery | --privilege-discovery | absent | absent | absent | absent | varies/unknown | yes | description present | diagnostic boundary present | diagnostic registry | yes | yes |

## Shared implementation characteristics

- Every current Question Family row has a CLI inquiry surface, answer responsibility, authority boundary, JSON support set to true, a human formatter name, bounded eligibility status, and implementation reason.
- Every current Question Family has tests covering the inventory surface and bounded-dispatch consistency through the question surface inventory tests.
- Every diagnostic inventory surface outside the Question Surface Inventory has a declared CLI flag, description, JSON support declaration, record scope, event-ledger and mutation declarations, and diagnostic registration.
- Many outside surfaces also have diagnostic shape-audit implementation specs, which is a stronger implementation-validation relationship than inventory membership alone.

## Distinguishing implementation characteristics

- Bounded ask dispatch is preserved only for thirteen Question Families. Surface inventory and surface shape validation are diagnostic-only. Source definition/import lookup and inquiry orientation have no bounded ask dispatch mapping in the current implementation.
- Required surface arguments are preserved only for derivation explanation and selection explanation. Other required-argument behavior may be described in notes, but it is not captured in `required_surface_args`.
- Diagnostic inventory rows preserve operational shape declarations such as `supports_record`, `record_scope`, `writes_event_ledger`, and `mutates_cluster`; Question Family rows preserve boundary text but do not normalize those operational shape fields per family.
- Diagnostic shape-audit specs preserve build/format/json function validation by diagnostic surface. Question Family rows preserve formatter names as strings but do not validate each family formatter directly unless the surface is also in the diagnostic shape audit.

## Implementation-backed inconsistencies

- The source definition/import lookup and inquiry orientation Question Families are marked `not_dispatchable` even though they have CLI surfaces and human formatter names.
- Some Question Family notes say an explicit argument is required, but `required_surface_args` is absent unless the family is in the bounded ask required-args map.
- Outside diagnostic surfaces frequently have most operational shape evidence shared with diagnostic Question Families, but they have no question-family row, examples, answer-responsibility field in question-family form, bounded status, or implementation reason.

## Required questions

1. Shared by every current Question Family: CLI flag, implementation surface, example questions, answer responsibility, boundary, JSON support, human formatter name, bounded status, and implementation reason are present in every row.
2. Partial characteristics: dispatch surface, bounded eligibility level, and required args vary according to bounded ask maps and diagnostic-only family set.
3. Outside surfaces with most similar characteristics are diagnostic surfaces with CLI flags, JSON support, descriptions, diagnostic registration, and shape-audit specs, especially operational_surface_inventory, visibility_coverage_audit, operational_surface_classification_audit, inquiry_artifacts, privilege_discovery, operational_graph, and investigation_path. They resemble diagnostic Question Families operationally, without implying promotion.
4. Outside surfaces clearly lack Question Family-specific characteristics: no row-level example questions, no question-family answer-responsibility field, no bounded status, no bounded dispatch surface, no required surface args in bounded ask form, and no implementation reason.
5. Inclusion is partially implementation-backed. The implementation explains current rows after membership exists, but not all inclusion decisions are derivable from shared implementation characteristics because outside surfaces can preserve many similar characteristics.
6. Missing visibility relationships are: a normalized inclusion criterion, a link from diagnostic/operational inquiry surfaces to non-membership rationale, and a validated relationship showing why a surface with similar CLI/JSON/formatter/diagnostic evidence is not a Question Family.
7. Question Family inclusion is not fully recoverable from implementation evidence alone; additional visibility would be required to distinguish inventory membership from similar implementation-backed inquiry surfaces without relying on the manually maintained inventory.
8. The repository distinguishes implementation-backed inquiry surface from Question Family through inventory membership and bounded ask maps. It does not expose a general implementation-backed discriminator proving that all and only current inventory members are Question Families.

## Conclusion

Question Family inclusion is currently **partially implementation-backed**: current rows preserve substantial implementation evidence, but comparison with outside implementation-backed inquiry surfaces shows some inclusion decisions remain implicit.

## Files inspected

- `AGENTS.md`
- `seed_runtime/question_surface_inventory.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `scripts/seed_local.py`
- `tests/test_question_surface_inventory.py`
- `tests/test_diagnostic_inventory.py`
- `tests/test_diagnostic_shape_audit.py`

## Files changed

- `docs/question_family_inclusion_evidence_investigation.md`

## Tests run

- `pytest -q tests/test_question_surface_inventory.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

## LOC changed

- Added this investigation document.
