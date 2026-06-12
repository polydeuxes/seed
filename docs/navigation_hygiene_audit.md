---
doc_type: audit
status: active
domain: documentation navigation hygiene
defines:
  - navigation hygiene audit snapshot
  - documentation routing findings
  - metadata coverage findings
depends_on:
  - index.md
  - architectural_knowledge_map.md
  - architectural_status_and_next_frontier.md
  - documentation_authority_reconciliation.md
  - documentation_lifecycle_reconciliation.md
related:
  - knowledge_navigation_layers_frontier.md
  - architectural_findings_preservation.md
  - finding_applicability_index.md
---

# Navigation Hygiene Audit

## Purpose

This audit records documentation navigation hygiene findings for the current repository state.
It is a routing and hygiene audit only. It does not replace the authority of reconciliation, frontier, status, ontology, architecture, or lifecycle documents.

The audit intentionally separates findings from fixes. Low-risk routing updates made with this audit are listed below, but unresolved findings remain findings rather than automatic corrections.

## Method

The repository was inspected directly from `docs/` content.

Audit checks used:

- enumerate `docs/*.md`;
- detect YAML-style front matter only when a document starts with `---` and has a closing `---` block;
- detect `depends_on:` and `related:` keys inside that front matter block;
- extract same-directory markdown references ending in `.md` from the three navigation/status surfaces;
- compare extracted references with existing `docs/*.md` filenames;
- count duplicated references on each navigation/status surface;
- identify filenames containing `frontier` that are absent from selected navigation surfaces.

## Snapshot Summary

| Check | Result |
| --- | --- |
| Markdown documents in `docs/` | 241 |
| Documents with detected front matter | 19 |
| Documents missing front matter | 222 |
| Documents missing dependency metadata | 222 |
| Documents missing related routing metadata | 224 |
| `docs/index.md` missing-file references | 0 |
| `docs/architectural_knowledge_map.md` missing-file references | 2 |
| `docs/architectural_status_and_next_frontier.md` missing-file references | 0 |
| Documents not reachable from `docs/index.md` | 34 |
| Documents not reachable from `docs/architectural_knowledge_map.md` | 171 |
| Frontier documents absent from `docs/index.md` | 5 |
| Frontier documents absent from `docs/architectural_knowledge_map.md` | 9 |

## Authority Boundary

This document is not a new source of architectural truth.

- If this audit conflicts with a reconciliation, the reconciliation wins.
- If this audit conflicts with `architectural_status_and_next_frontier.md`, the status document wins for current priority and frontier status.
- If this audit conflicts with `architectural_knowledge_map.md`, the map wins for intended concern routing until it is intentionally updated.
- Missing navigation or metadata should not be interpreted as evidence that a document is obsolete, unauthoritative, or superseded.

## Low-Risk Navigation Corrections Applied

This audit made only low-risk routing corrections for the new audit document itself:

- `index.md` now routes to `navigation_hygiene_audit.md` from documentation authority/navigation.
- `architectural_knowledge_map.md` now routes navigation hygiene questions to `navigation_hygiene_audit.md`.
- `architectural_status_and_next_frontier.md` now mentions this audit under documentation maintenance without changing the active frontier.

No broad automatic cleanup was applied to older documents.

## Findings

### 1. Front Matter Coverage Is Partial

Detected front matter is present in 19 of 241 markdown documents.

Documents with front matter:

- `attention_target_frontier.md`
- `attention_trigger_frontier.md`
- `foundational_ontology_reconciliation.md`
- `handoff_and_continuation_lineage_frontier.md`
- `host_observation_reconciliation.md`
- `index.md`
- `inquiry_frontier.md`
- `knowledge_navigation_layers_frontier.md`
- `navigation_hygiene_audit.md`
- `object_role_and_operation_frontier.md`
- `object_role_operation_consistency_audit.md`
- `object_role_operation_pressure_test.md`
- `occurrence_time_and_temporal_claim_reconciliation.md`
- `operation_attribution_frontier.md`
- `operations_frontier.md`
- `persistence_frontier.md`
- `prometheus_observation_boundary_reconciliation.md`
- `selection_and_attention_frontier.md`
- `time_provenance_and_temporal_authority_audit.md`

All other markdown documents in `docs/` are missing detected front matter under the audit rule.

This is a repository-wide convention gap, not a per-document correctness judgment. Many older authoritative documents predate the newer metadata pattern.

### 2. Dependency Metadata Coverage Follows Front Matter Coverage

Documents missing dependency metadata: 222.

In this snapshot, every document with detected front matter includes a `depends_on:` key. Therefore the dependency-metadata gap is equivalent to the front-matter gap.

Dependency metadata is absent from every document not listed in the preceding "Documents with front matter" list.

### 3. Related Routing Metadata Has Two Additional Gaps

Documents missing related routing metadata: 224.

This includes all documents missing front matter plus these front-matter-bearing documents that do not define `related:`:

- `handoff_and_continuation_lineage_frontier.md`
- `object_role_operation_pressure_test.md`


### 4. `docs/index.md` Reachability Is Curated, Not Exhaustive

`index.md` references 206 unique documents and has 0 missing-file references.

Missing-file references from `index.md`:

- None found.


Documents not reachable from `index.md`:

- `alignment_semantics_reconciliation.md`
- `architecture_principles.md`
- `architecture_visualization_phase1.md`
- `ask_question_refuse_inventory.md`
- `attention_target_frontier.md`
- `attention_trigger_frontier.md`
- `availability_vocabulary_audit.md`
- `boundary_preservation_as_architectural_principle.md`
- `canonicalization_pass_v1.md`
- `capability_self_acquisition_readiness_audit.md`
- `conclusion_taxonomy_reconciliation.md`
- `context_composition_reconciliation.md`
- `context_composition_vocabulary.md`
- `documentation_observation_seed_characterization.md`
- `documentation_observation_v0_implementation_characterization.md`
- `function_blocks.md`
- `gap_classification_reconciliation.md`
- `invariants.md`
- `knowledge_change_and_revision_reconciliation.md`
- `local_network_impact_boundary_audit.md`
- `local_network_observation_audit.md`
- `logic_model.md`
- `object_role_and_operation_frontier.md`
- `object_role_operation_consistency_audit.md`
- `object_role_operation_pressure_test.md`
- `package_inventory_dependency_boundary_audit.md`
- `persistence_frontier.md`
- `reality_fact_and_claim_reconciliation.md`
- `recommendation_selection_boundary.md`
- `relationship_observation_v0_reconciliation.md`
- `repository_reconciliation_characterization.md`
- `retry_parse_failure_inventory.md`
- `selection_and_attention_frontier.md`
- `state_patch_inventory.md`


Because `index.md` states that it is a navigation aid rather than authority, this unreachable set should be treated as routing hygiene backlog rather than document invalidation.

### 5. `docs/architectural_knowledge_map.md` Reachability Is Much Less Exhaustive

`architectural_knowledge_map.md` references 72 unique document-like routes and has 2 extracted missing-file references.

Extracted missing-file references from `architectural_knowledge_map.md`:

- `_reconciliation.md`
- `_vocabulary.md`


The two extracted missing references are wildcard-style prose examples rather than intended concrete files. They are still visible to simple route-audit tooling and should be considered if future navigation tooling becomes stricter.

Documents not reachable from `architectural_knowledge_map.md`:

- `active_context_and_working_set_reconciliation.md`
- `adoption_decision_authority_reconciliation.md`
- `alignment_semantics_reconciliation.md`
- `architectural_documentation_alignment_reconciliation.md`
- `architecture_visualization_phase1.md`
- `ask_question_refuse_inventory.md`
- `assessment_recommendation_and_decision_reconciliation.md`
- `attention_target_frontier.md`
- `attention_trigger_frontier.md`
- `audit_chain_findings_preservation.md`
- `availability_vocabulary_audit.md`
- `backlog_and_status_reconciliation.md`
- `behavior_claim_reconciliation.md`
- `boundary_claim_reconciliation.md`
- `boundary_preservation_as_architectural_principle.md`
- `candidate_meaning_and_ambiguity_reconciliation.md`
- `canonical_documentation_reconciliation.md`
- `canonicalization_pass_v1.md`
- `capability_acquisition_reconciliation.md`
- `capability_authority_and_execution_boundary_reconciliation.md`
- `capability_extension_methodology.md`
- `capability_gap_and_operator_bridge_reconciliation.md`
- `capability_need_acquisition_reconciliation.md`
- `capability_ownership_matrix.md`
- `capability_self_acquisition_readiness_audit.md`
- `capability_verification_audit.md`
- `capability_verification_fit_audit.md`
- `capability_verification_reconciliation.md`
- `capability_verification_vocabulary.md`
- `causality_and_explanation_reconciliation.md`
- `claim_strength_and_assertion_semantics_reconciliation.md`
- `claim_support_characterization.md`
- `claim_support_design.md`
- `claim_support_frontier.md`
- `codex_prompt_protocol.md`
- `conclusion_taxonomy_reconciliation.md`
- `constraint_evidence_inventory.md`
- `continuation_constraints_and_consumer_capabilities_reconciliation.md`
- `contradiction_handling_audit.md`
- `current_observation_evidence_change_event_implementation_audit.md`
- `current_observation_evidence_change_event_implementation_findings.md`
- `dimensioned_fact_detail_rendering_audit.md`
- `documentation_architecture_audit.md`
- `documentation_authority_and_seed_thesis_reconciliation.md`
- `documentation_observation_characterization.md`
- `documentation_observation_design.md`
- `documentation_observation_seed_characterization.md`
- `documentation_observation_v0_implementation_characterization.md`
- `durable_lifecycle_reconciliation.md`
- `entity_identity_derivation_reconciliation.md`
- `entity_impact_drilldown_reconciliation.md`
- `event_and_change_reconciliation.md`
- `event_change_and_observation_granularity_reconciliation_audit.md`
- `evidence_strength_and_claim_strength_reconciliation.md`
- `execution_boundary_inventory_and_status_emission_audit.md`
- `execution_status_and_operator_feedback_reconciliation.md`
- `execution_status_emission_and_consumption_reconciliation.md`
- `existence_claim_reconciliation.md`
- `explainability_audit.md`
- `explainability_contract_characterization.md`
- `explainability_inventory_audit.md`
- `explainability_reconciliation.md`
- `explanation_contract_vocabulary.md`
- `fact_confidence_and_corroboration_reconciliation.md`
- `filesystem_measurement_visibility_regression_audit.md`
- `finding_applicability_index.md`
- `function_blocks.md`
- `gap_classification_reconciliation.md`
- `goal_policy_and_operator_authority_reconciliation.md`
- `goal_relevance_and_recommendation_generation_reconciliation.md`
- `host_observation_composability_audit.md`
- `host_observation_reconciliation.md`
- `impact_overview_authority_reconciliation.md`
- `implementation_prompt_alignment_reconciliation.md`
- `index.md`
- `input_act_decision_bridge.md`
- `input_act_vocabulary.md`
- `input_envelope_vocabulary.md`
- `input_inspection_reconciliation.md`
- `input_source_authority_reconciliation.md`
- `knowledge_change_and_revision_reconciliation.md`
- `language_candidate_routing_and_promotion_reconciliation.md`
- `listening_port_observation.md`
- `local_cli_responsibility_boundary_audit.md`
- `local_host_fact_surface_implementation_audit.md`
- `local_host_observation_entity_boundary_reconciliation.md`
- `local_network_impact_boundary_audit.md`
- `local_network_observation_audit.md`
- `local_observation_roadmap_audit.md`
- `local_package_observation_adapter_boundary_audit.md`
- `local_package_observation_vocabulary_audit.md`
- `local_resource_preflight_readiness_audit.md`
- `local_users_observation_vocabulary_audit.md`
- `logic_model.md`
- `object_role_and_operation_frontier.md`
- `object_role_operation_consistency_audit.md`
- `object_role_operation_pressure_test.md`
- `observation_batching_and_event_granularity_reconciliation.md`
- `observation_evidence_change_event_reconciliation.md`
- `observation_interpretation_and_reality_reconciliation.md`
- `observation_refresh_and_knowledge_freshness_reconciliation.md`
- `observation_vs_mutation_reconciliation.md`
- `occurrence_time_and_temporal_claim_reconciliation.md`
- `operation_support_boundary_reconciliation.md`
- `operator_interface_and_projection_authority_reconciliation.md`
- `operator_investigation_workflow_reconciliation.md`
- `operator_navigation_reconciliation.md`
- `operator_pain_as_frontier_signal.md`
- `operator_trial_plan.md`
- `ownership_claim_reconciliation.md`
- `package_inventory_dependency_boundary_audit.md`
- `pending_action_lifecycle_inventory.md`
- `persistence_frontier.md`
- `policy_pending_action_inventory.md`
- `principal_identity_reconciliation.md`
- `prometheus_acquisition_interpretation_routing_promotion_audit.md`
- `prometheus_boundary_cleanup_status_reconciliation.md`
- `prometheus_endpoint_top_entity_boundary_audit.md`
- `prometheus_host_endpoint_fact_attachment_audit.md`
- `prometheus_target_and_filesystem_identity_reconciliation.md`
- `promotion_backlog_review.md`
- `read_model_inventory_and_authority_reconciliation.md`
- `reality_fact_and_claim_reconciliation.md`
- `recommendation_selection_boundary.md`
- `relationship_fact_reconciliation.md`
- `relationship_observation_v0_reconciliation.md`
- `relationship_promotion_reconciliation.md`
- `repository_artifact_ontology_reconciliation.md`
- `repository_observation_characterization.md`
- `repository_observation_design.md`
- `repository_observation_language_boundary.md`
- `repository_observation_seed_characterization.md`
- `repository_observation_v0_implementation_characterization.md`
- `repository_reconciliation_characterization.md`
- `repository_reconciliation_frontier.md`
- `repository_reconciliation_seed_characterization.md`
- `repository_reconciliation_v0_implementation_characterization.md`
- `repository_reconciliation_v1_frontier.md`
- `retry_parse_failure_inventory.md`
- `roadmap_and_methodology_reconciliation.md`
- `roadmap_reconciliation.md`
- `rule_inventory.md`
- `runtime_loop_thin_runtime_plan.md`
- `runtime_parity_inventory.md`
- `runtime_reassessment.md`
- `runtime_runtime_loop_responsibility_audit.md`
- `selection_and_attention_frontier.md`
- `self_model_acquisition_architecture_reconciliation.md`
- `self_model_and_alignment_architecture_reconciliation.md`
- `self_model_architecture.md`
- `self_model_evidence_architecture_reconciliation.md`
- `self_observation_audit.md`
- `source_definitions_and_entrypoint_observation_reconciliation.md`
- `state_patch_inventory.md`
- `state_summary_authority_reconciliation.md`
- `state_summary_cli_boundary_audit.md`
- `state_summary_empty_operator_kind_buckets_audit.md`
- `state_summary_endpoint_prominence_audit.md`
- `state_summary_filesystem_projection_boundary_audit.md`
- `state_summary_top_entity_selection_audit.md`
- `storage_measurement_current_fact_regression_audit.md`
- `storage_topology_ambiguity_and_operator_clarification_reconciliation.md`
- `storage_topology_observation.md`
- `structure_claim_reconciliation.md`
- `supported_ground_recognition_reconciliation.md`
- `temporal_reasoning_audit.md`
- `time_provenance_and_temporal_authority_audit.md`
- `tool_execution_ownership_audit.md`
- `view_authority_and_surface_responsibility_reconciliation.md`
- `why_not_explanation_characterization.md`
- `why_not_vocabulary.md`


This is expected to be larger than `index.md` because the knowledge map is explicitly lightweight and concern-oriented.

### 6. `docs/architectural_status_and_next_frontier.md` Has No Missing-File References

`architectural_status_and_next_frontier.md` references 16 unique documents and has no stale missing-file references under this audit's filename-existence check.

Missing-file references from `architectural_status_and_next_frontier.md`:

- None found.


The status document does not appear stale by broken-reference detection. It remains intentionally selective about active and paused frontier framing.

### 7. Frontier Documents Are Not Uniformly Routed Across Surfaces

Frontier documents absent from `index.md`:

- `attention_target_frontier.md`
- `attention_trigger_frontier.md`
- `object_role_and_operation_frontier.md`
- `persistence_frontier.md`
- `selection_and_attention_frontier.md`


Frontier documents absent from `architectural_knowledge_map.md`:

- `attention_target_frontier.md`
- `attention_trigger_frontier.md`
- `claim_support_frontier.md`
- `object_role_and_operation_frontier.md`
- `operator_pain_as_frontier_signal.md`
- `persistence_frontier.md`
- `repository_reconciliation_frontier.md`
- `repository_reconciliation_v1_frontier.md`
- `selection_and_attention_frontier.md`


This is the clearest navigation discoverability gap. The audit does not automatically promote these frontiers into current status or implementation readiness.

### 8. Duplicated Navigation Routes Exist

Duplicate markdown routes in `index.md`:

| Route | Count |
| --- | --- |
| `architectural_knowledge_map.md` | 2 |
| `architectural_status_and_next_frontier.md` | 2 |
| `canonical_documentation_reconciliation.md` | 2 |
| `derivation_frontier.md` | 2 |
| `documentation_authority_reconciliation.md` | 2 |
| `future_frontiers.md` | 2 |
| `handoff_and_continuation_lineage_frontier.md` | 2 |
| `inquiry_frontier.md` | 2 |
| `knowledge_navigation_layers_frontier.md` | 2 |
| `knowledge_representation_map.md` | 2 |
| `navigation_hygiene_audit.md` | 2 |
| `operation_attribution_frontier.md` | 2 |
| `operations_frontier.md` | 2 |
| `prometheus_target_and_filesystem_identity_reconciliation.md` | 2 |
| `state_summary_filesystem_projection_boundary_audit.md` | 2 |


Duplicate markdown routes in `architectural_knowledge_map.md`:

| Route | Count |
| --- | --- |
| `agency_and_attribution_reconciliation.md` | 2 |
| `architectural_findings_preservation.md` | 6 |
| `architectural_status_and_next_frontier.md` | 5 |
| `architecture.md` | 2 |
| `bootstrap_invariants.md` | 2 |
| `continuation_context_and_working_state_reconciliation.md` | 2 |
| `contradiction_discovery_and_visibility_reconciliation.md` | 2 |
| `cross_seed_provenance_and_federation_reconciliation.md` | 2 |
| `derivation_frontier.md` | 2 |
| `documentation_authority_reconciliation.md` | 3 |
| `documentation_boundary_enforcement_reconciliation.md` | 2 |
| `documentation_lifecycle_reconciliation.md` | 2 |
| `foundational_ontology_reconciliation.md` | 2 |
| `future_frontiers.md` | 2 |
| `handoff_and_continuation_lineage_frontier.md` | 2 |
| `handoff_bootstrap_and_summary_reconciliation.md` | 2 |
| `handoff_consumption_activation_reconciliation.md` | 2 |
| `handoff_document_boundary_reconciliation.md` | 2 |
| `handoff_template_and_continuation_protocol_reconciliation.md` | 2 |
| `inquiry_frontier.md` | 2 |
| `knowledge_acquisition_and_selection.md` | 2 |
| `knowledge_acquisition_status.md` | 2 |
| `knowledge_maintenance_reconciliation.md` | 2 |
| `knowledge_navigation_layers_frontier.md` | 3 |
| `learning_and_knowledge_change_reconciliation.md` | 2 |
| `local_observation_roadmap_reconciliation.md` | 2 |
| `natural_language_observation_and_intent_derivation_reconciliation.md` | 2 |
| `navigation_hygiene_audit.md` | 2 |
| `ontology.md` | 3 |
| `operation_attribution_frontier.md` | 2 |
| `operations_frontier.md` | 2 |
| `operator_intent_question_and_claim_interface_reconciliation.md` | 2 |
| `prediction_forecasting_and_future_claims_reconciliation.md` | 2 |
| `prometheus_endpoint_identity_boundary_audit.md` | 2 |
| `prometheus_observation_boundary_reconciliation.md` | 2 |
| `reasoning_roadmap.md` | 2 |
| `seed.md` | 2 |


Duplicate markdown routes in `architectural_status_and_next_frontier.md`:

| Route | Count |
| --- | --- |
| `architectural_findings_preservation.md` | 3 |


Most duplicates appear benign: front matter relationships plus body routes, start-here links plus topical links, or a document intentionally appearing in multiple topical sections. The two more actionable index duplicates are `prometheus_target_and_filesystem_identity_reconciliation.md` and `state_summary_filesystem_projection_boundary_audit.md`, which appear in both Prometheus/local observation and storage/filesystem topology sections.

## Major Findings

1. **Metadata adoption is incomplete.** Front matter and dependency metadata currently cover only 19 of 241 documents.
2. **Related routing metadata is slightly less complete than dependency metadata.** Two documents with front matter still lack `related:`.
3. **`index.md` has no broken file references but is not exhaustive.** 34 existing documents are not reachable from it.
4. **`architectural_knowledge_map.md` is intentionally selective but has broad non-reachability.** 171 existing documents are not directly reachable from it.
5. **The status document has no stale missing-file references.** No broken markdown routes were found in `architectural_status_and_next_frontier.md`.
6. **Several frontier documents are absent from main navigation surfaces.** This affects discoverability but does not change their authority or readiness.
7. **Duplicate routes are mostly contextual rather than conflicting.** No duplicated route was found that clearly creates an authority conflict, but future navigation tooling should distinguish intentional multi-section routing from accidental duplication.

## Recommended Follow-Up

- Decide whether front matter is now mandatory for all new documents only, or whether older authoritative documents should be gradually backfilled.
- Add `related:` to `handoff_and_continuation_lineage_frontier.md` and `object_role_operation_pressure_test.md` if their front matter should match the newer pattern.
- Consider routing the absent frontier documents from `index.md` and/or `architectural_knowledge_map.md` in a focused navigation pass.
- If route tooling is introduced, teach it to ignore prose wildcard examples such as scoped `*_vocabulary.md` and scoped `*_reconciliation.md`.
- Keep status updates separate from audit findings so that stale-reference repair does not accidentally change active frontier authority.

## Non-Goals

This audit does not:

- declare documents obsolete;
- reconcile architectural disagreements;
- promote frontier documents to canonical architecture;
- change implementation priorities;
- replace `index.md`, `architectural_knowledge_map.md`, or `architectural_status_and_next_frontier.md`;
- require automatic metadata backfill across the repository.
