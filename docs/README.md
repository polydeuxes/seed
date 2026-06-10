# Seed Documentation Map

This directory contains Seed's architectural thesis, status documents, reconciliations, vocabularies, audits, and implementation-facing design notes.

This file is the documentation navigation authority. It is a map, not an encyclopedia: it routes readers to the documents that own each answer without restating their full arguments.

---

## Start Here

1. [`../README.md`](../README.md) — repository orientation: what Seed is, what it owns, what it does not own, and where a new contributor should begin.
2. [`seed.md`](seed.md) — concise architectural thesis / constitutional statement for Seed's observation, evidence, fact, relationship, projection, authority, and operator invariants.
3. [`architectural_status_and_next_frontier.md`](architectural_status_and_next_frontier.md) — current architectural status, active frontier, and current priorities.
4. [`architectural_knowledge_map.md`](architectural_knowledge_map.md) — concern map and routing to owning documents across acquisition, integrity, selection, response, and architectural findings.

---

## Foundational Reconciliation Chain

Use this chain when changing architecture, projection semantics, identity handling, fact promotion, or relationship promotion.

1. [`entity_identity_derivation_reconciliation.md`](entity_identity_derivation_reconciliation.md) — entity identity derivation and the boundary between resemblance, relationship, alias, and equivalence.
2. [`evidence_trust_and_source_authority_reconciliation.md`](evidence_trust_and_source_authority_reconciliation.md) — evidence trust and source authority distinctions.
3. [`corroboration_and_fact_promotion_reconciliation.md`](corroboration_and_fact_promotion_reconciliation.md) — corroboration and fact promotion rules.
4. [`relationship_promotion_reconciliation.md`](relationship_promotion_reconciliation.md) — relationship promotion and the rule that relationships must not overclaim identity.

Related boundary case law:

* [`fact_confidence_and_corroboration_reconciliation.md`](fact_confidence_and_corroboration_reconciliation.md) — fact confidence, support strength, and corroboration details.
* [`relationship_fact_reconciliation.md`](relationship_fact_reconciliation.md) — fact/relationship boundary preservation.
* [`principal_identity_reconciliation.md`](principal_identity_reconciliation.md) — principal identity boundary reasoning.

---

## Alignment / Architectural Foundations

Use these papers for alignment-sensitive work, handoffs, and broad architecture boundary preservation. They are not all required for basic repository orientation.

* [`documentation_authority_and_seed_thesis_reconciliation.md`](documentation_authority_and_seed_thesis_reconciliation.md) — authority model for README, `seed.md`, this documentation map, and reconciliation documents.
* [`architectural_documentation_alignment_reconciliation.md`](architectural_documentation_alignment_reconciliation.md) — audit of authoritative documentation alignment after the claim, operator, projection, temporal, explanation, and causality reconciliations.
* [`documentation_authority_reconciliation.md`](documentation_authority_reconciliation.md) — documentation ownership boundaries.
* [`documentation_boundary_enforcement_reconciliation.md`](documentation_boundary_enforcement_reconciliation.md) — enforcement of documentation boundaries.
* [`boundary_preservation_as_architectural_principle.md`](boundary_preservation_as_architectural_principle.md) — boundary preservation as an architectural principle.
* [`active_context_and_working_set_reconciliation.md`](active_context_and_working_set_reconciliation.md) — active context and working-set alignment.
* [`operator_pain_as_frontier_signal.md`](operator_pain_as_frontier_signal.md) — operator pain as a frontier signal.
* [`finding_applicability_index.md`](finding_applicability_index.md) — applicability index for architectural findings.
* [`self_model_and_alignment_architecture_reconciliation.md`](self_model_and_alignment_architecture_reconciliation.md) — self-model and alignment architecture.
* [`implementation_prompt_alignment_reconciliation.md`](implementation_prompt_alignment_reconciliation.md) — implementation prompt alignment.
* [`handoff_alignment_guardrails_reconciliation.md`](handoff_alignment_guardrails_reconciliation.md) — handoff guardrails.

---

## Observation Frontiers

Use these for acquisition-focused work. Observation documents should preserve source boundaries, avoid mutation, and avoid promoting claims beyond available evidence.

* [`knowledge_acquisition_status.md`](knowledge_acquisition_status.md) — acquisition status and current acquisition framing.
* [`knowledge_acquisition_and_selection.md`](knowledge_acquisition_and_selection.md) — acquisition/selection relationship.
* [`local_observation_roadmap_reconciliation.md`](local_observation_roadmap_reconciliation.md) — local observation roadmap and constraints.
* [`local_host_observation_entity_boundary_reconciliation.md`](local_host_observation_entity_boundary_reconciliation.md) — local host entity boundaries.
* [`local_users_observation_vocabulary_audit.md`](local_users_observation_vocabulary_audit.md) — local users observation vocabulary.
* [`local_package_observation_vocabulary_audit.md`](local_package_observation_vocabulary_audit.md) — local package observation vocabulary.
* [`local_package_observation_adapter_boundary_audit.md`](local_package_observation_adapter_boundary_audit.md) — package adapter boundary.
* [`local_network_observation_audit.md`](local_network_observation_audit.md) — local network observation audit.
* [`listening_port_observation.md`](listening_port_observation.md) — listening-port observation.
* [`storage_topology_observation.md`](storage_topology_observation.md) — storage topology observation.
* [`prometheus_observation_boundary_reconciliation.md`](prometheus_observation_boundary_reconciliation.md) — Prometheus observation boundary.
* [`prometheus_endpoint_identity_boundary_audit.md`](prometheus_endpoint_identity_boundary_audit.md) — Prometheus endpoint identity boundary.
* [`repository_observation_frontier.md`](repository_observation_frontier.md) — repository observation frontier.
* [`repository_observation_source_design.md`](repository_observation_source_design.md) — repository observation source design.
* [`documentation_observation_frontier.md`](documentation_observation_frontier.md) — documentation observation frontier.
* [`self_observation_reconciliation.md`](self_observation_reconciliation.md) — self-observation boundary reasoning.

---

## Operator Surfaces / Read Models

Use these for operator-facing views and read-only projections. These surfaces explain or summarize projected knowledge; they must not mutate evidence, facts, relationships, projections, or hosts.

* State summary — [`state_summary_authority_reconciliation.md`](state_summary_authority_reconciliation.md), [`state_summary_cli_boundary_audit.md`](state_summary_cli_boundary_audit.md), [`state.md`](state.md)
* Impact — [`impact_overview_authority_reconciliation.md`](impact_overview_authority_reconciliation.md), [`entity_impact_drilldown_reconciliation.md`](entity_impact_drilldown_reconciliation.md)
* Fact support — [`claim_support_frontier.md`](claim_support_frontier.md), [`claim_support_design.md`](claim_support_design.md), [`evidence_strength_and_claim_strength_reconciliation.md`](evidence_strength_and_claim_strength_reconciliation.md)
* Graph issues — [`read_model_inventory_and_authority_reconciliation.md`](read_model_inventory_and_authority_reconciliation.md), [`state.md`](state.md), [`why_not_vocabulary.md`](why_not_vocabulary.md)
* Entity types — [`entity_type_catalog/core.json`](../entity_type_catalog/core.json), [`self_observation_audit.md`](self_observation_audit.md)
* Relationships — [`relationship_catalog/core.json`](../relationship_catalog/core.json), [`relationship_promotion_reconciliation.md`](relationship_promotion_reconciliation.md), [`relationship_observation_v0_reconciliation.md`](relationship_observation_v0_reconciliation.md)

---

## Additional Routing

* Current status and active frontier: [`architectural_status_and_next_frontier.md`](architectural_status_and_next_frontier.md)
* Concern routing: [`architectural_knowledge_map.md`](architectural_knowledge_map.md)
* Preserved findings and rejected concepts: [`architectural_findings_preservation.md`](architectural_findings_preservation.md)
* Roadmap sequencing: [`reasoning_roadmap.md`](reasoning_roadmap.md)
* Canonical architecture overview: [`architecture.md`](architecture.md)
* Architecture principles: [`architecture_principles.md`](architecture_principles.md)
* Knowledge representation: [`knowledge_representation_map.md`](knowledge_representation_map.md), [`knowledge_representation_reconciliation.md`](knowledge_representation_reconciliation.md)
* Selection and context: [`context_composition_reconciliation.md`](context_composition_reconciliation.md), [`selection_rationale_reconciliation.md`](selection_rationale_reconciliation.md)
* Response: [`response_reconciliation.md`](response_reconciliation.md), [`response_characterization.md`](response_characterization.md), [`response_vocabulary.md`](response_vocabulary.md)
* Capability boundaries: [`capability_gap_and_operator_bridge_reconciliation.md`](capability_gap_and_operator_bridge_reconciliation.md), [`capability_acquisition_reconciliation.md`](capability_acquisition_reconciliation.md), [`capability_verification_reconciliation.md`](capability_verification_reconciliation.md)

Historical reconciliation, characterization, audit, and vocabulary documents remain part of the record. Do not delete them merely because their conclusions have been routed through this map.
