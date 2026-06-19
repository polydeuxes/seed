# Architectural Knowledge Map

## Purpose

This document is a lightweight map of Seed's architectural knowledge. It reduces rediscovery cost by showing how major concerns relate and where the owning documents live.

It owns orientation and routing only. It does not own current status, active frontier, roadmap sequencing, preserved findings, rejected-concept rationale, lifecycle definitions, or canonical architecture content.

For authority boundaries, see `documentation_authority_reconciliation.md` and `documentation_boundary_enforcement_reconciliation.md`.

---

# Current Architectural Frame

Process layer:

```text
Knowledge Acquisition
        ↓
Knowledge Integrity
        ↓
Knowledge Selection
        ↓
Response
```

Representation layer:

```text
Observation
        ↓
Evidence
        ↓
Claim
        ↓
Fact / Relationship
        ↓
Projected Knowledge Structures
        ↓
Learning / Contradiction / Future-Claim Assessment
```

Language and continuation boundary layer:

```text
Language Observation
        ↓
Interpretation
        ↓
Attribution Claim

Handoff
        ↓
Continuation Alignment
```

Additional documentation concern:

```text
Foundational Ontology
Architectural Findings
```

Emerging meta-architecture frontiers:

```text
Knowledge Navigation
Operations
Operation Attribution
Relationship
Inquiry
Selection / Attention
Active Edge
Object / Role / Operation
Concept Stability
Explanatory Load
Observation Surface / Blind Spots
Observable Domain Consumer / Activity
Persistence / Continuity / Current Work Position
Handoff / Continuation Lineage
View / Lens / Orientation
Descriptive Language / Authority Formation
Surface / Bounded Consequence
Operator Entrypoint Pressure
```

These frontiers are routed here for discovery only. They are characterized or emerging; they are not reconciled architecture, canonical ontology, roadmap authority, or implementation direction.

For the current status of these concerns and the active frontier, see `architectural_status_and_next_frontier.md`.

---

# Authority Routing

| Reader question | Owning document family |
| --- | --- |
| Where should I start? | `README.md` |
| How do major concerns relate? | This map |
| What is current? | `architectural_status_and_next_frontier.md` |
| What is the active frontier? | `architectural_status_and_next_frontier.md` |
| What was learned or rejected? | `architectural_findings_preservation.md` plus scoped characterization and reconciliation documents |
| What is planned or sequenced? | `reasoning_roadmap.md` |
| What is canonical architecture? | `architecture.md` plus scoped canonical documents |
| What are lifecycle/documentation roles? | `documentation_lifecycle_reconciliation.md`, `documentation_authority_reconciliation.md`, and `documentation_boundary_enforcement_reconciliation.md` |
| What do foundational terms mean? | `ontology.md` for concise vocabulary; `foundational_ontology_reconciliation.md` for the audit |
| What do scoped terms mean? | Scoped `*_vocabulary.md` documents |
| Why was a scoped decision made? | Scoped `*_reconciliation.md` documents |
| How should natural-language requests be treated? | `natural_language_observation_and_intent_derivation_reconciliation.md`, `operator_intent_question_and_claim_interface_reconciliation.md`, `input_inspection_boundary_reconciliation.md` |
| How should agency or attribution be handled? | `agency_and_attribution_reconciliation.md` |
| How should continuation across handoffs be preserved? | `handoff_document_boundary_reconciliation.md`, `handoff_template_and_continuation_protocol_reconciliation.md`, `handoff_consumption_activation_reconciliation.md`, `handoff_bootstrap_and_summary_reconciliation.md`, `continuation_context_and_working_state_reconciliation.md`, `bootstrap_invariants.md` |
| How should cross-Seed imports or federation be treated? | `cross_seed_provenance_and_federation_reconciliation.md` |
| How should learning or knowledge change be represented? | `learning_and_knowledge_change_reconciliation.md` |
| How should contradictions be discovered or exposed? | `contradiction_discovery_and_visibility_reconciliation.md` |
| How should predictions and future claims be handled? | `prediction_forecasting_and_future_claims_reconciliation.md` |
| Where are Prometheus observation and endpoint identity boundaries? | `prometheus_observation_boundary_reconciliation.md`, `prometheus_endpoint_identity_boundary_audit.md` |
| How do I move from a question to concepts, architecture, documentation, repository structure, and implementation artifacts? | `knowledge_navigation_layers_frontier.md` |
| Where are emerging operation, attribution, relationship, inquiry, derivation, and handoff-lineage frontiers routed? | `operations_frontier.md`, `operation_attribution_frontier.md`, `relationship_frontier.md`, `inquiry_frontier.md`, `derivation_frontier.md`, `handoff_and_continuation_lineage_frontier.md`, and `future_frontiers.md` |
| Where are current documentation navigation hygiene findings? | `navigation_hygiene_audit.md` |
| Where are recent View, lens, orientation, inquiry, and unresolvedness investigations routed? | `participant_orientation_view_selection_observation.md`, `view_branch_continuity_reconciliation.md`, `lens_view_reconciliation.md`, `lens_orientation_and_dashboard_observation.md`, `inquiry_as_bridge_observation.md`, and `unresolvedness_observation.md` |
| Where are descriptive-language, `defines`, and authority-formation questions routed? | `promotion_and_reconciliation_observation.md`, `role_of_descriptive_vocabulary_observation.md`, `descriptive_language_vs_authority_observation.md`, `defines_authority_reconciliation_observation.md`, `defines_relationship_reconciliation_audit.md`, `authority_formation_pattern_observation.md`, and `authority_owner_observation.md` |
| Where are repository surfaces, bounded consequence, state-summary scope, and operator-entrypoint pressure routed? | `repository_surface_inventory_observation.md`, `bounded_consequence_discipline_observation.md`, `state_summary_decomposition_audit.md`, and `operator_entrypoint_pressure_audit.md` |
| Where are graph issue orientation and source-navigation entity typing audit findings routed? | `graph_issue_orientation_audit.md` and `source_navigation_entity_typing_graph_issue_audit.md` |
| What could the documentation lineage observation see, and what remained blind? | `observation_surface_and_blind_spot_audit.md` |
| Where is the distinction between bounded observable domains, acquisition paths, and inspection/view consumers observed? | `observable_domain_consumer_activity_observation.md`, `host_observation_reconciliation.md`, and `host_observation_composability_audit.md` |
| What appears to continue when artifact, inquiry, observation, and discovery-path lineage are discussed? | `lineage_distinction_observation.md` |
| What kinds of things do recent investigations appear to preserve? | `preservation_surface_observation.md` |
| What does activation failure look like when the answer is available, found, and read? | `working_state_activation_failure_observation.md` |
| Where is understanding visible to operators today? | `understanding_visibility_existing_surface_audit.md`, `operator_surface_family_observation.md`, `operator_understanding_surface_observation.md`, `operator_surface_activation_against_knowledge_and_understanding_audit.md` |
| Where does repository inquiry observe interaction or participation as possible evidence? | `interaction_as_evidence_observation.md` |
| Where do concepts appear to accumulate explanatory responsibility, shift load, or survive by remaining bounded? | `explanatory_load_observation.md` |
| Where are emerging operation, attribution, inquiry, attention, object/role/operation, persistence, continuity, current work position, active edge, derivation, and handoff-lineage frontiers routed? | `operations_frontier.md`, `operation_attribution_frontier.md`, `inquiry_frontier.md`, `selection_and_attention_frontier.md`, `attention_trigger_frontier.md`, `attention_target_frontier.md`, `object_role_and_operation_frontier.md`, `persistence_frontier.md`, `continuity_frontier.md`, `current_work_position_frontier.md`, `active_edge_frontier.md`, `concept_stability_audit.md`, `derivation_frontier.md`, `handoff_and_continuation_lineage_frontier.md`, and `future_frontiers.md` |

---

# Concern Map

## Foundational Ontology

Concern: Seed's stable architectural vocabulary and the boundaries between concepts.

Start with:

* `seed.md`
* `ontology.md`
* `foundational_ontology_reconciliation.md`

## Knowledge Acquisition

Concern: how Seed obtains evidence-backed knowledge.

Start with:

* `knowledge_acquisition_status.md`
* `knowledge_acquisition_and_selection.md`
* `knowledge_classification_vocabulary.md`
* `repository_observation_source_design.md`
* `self_observation_reconciliation.md`
* `local_observation_roadmap_reconciliation.md`

Currentness and frontier ownership remain in `architectural_status_and_next_frontier.md`. Prometheus implementation return work should route through `prometheus_observation_boundary_reconciliation.md` and `prometheus_endpoint_identity_boundary_audit.md` for `up` semantics, endpoint/host/service separation, `provides` overload, filesystem summary noise, mounted/shared storage identity, and alias/endpoint projection issues.

## Cross-Seed Provenance / Federation

Concern: how Seed imports, preserves, scopes, and explains foreign evidence without turning federation into truth transfer or import into verification.

Start with:

* `cross_seed_provenance_and_federation_reconciliation.md`
* `evidence_trust_and_source_authority_reconciliation.md`
* `corroboration_and_fact_promotion_reconciliation.md`

## Knowledge Integrity

Concern: how Seed characterizes reliability, support, conflict, contradiction, staleness, confidence, and verification limits for projected knowledge.

Start with:

* `knowledge_maintenance_reconciliation.md`
* `projection_integrity_summary_characterization.md`
* `projection_integrity_drilldown_characterization.md`
* `knowledge_representation_map.md`
* `knowledge_representation_reconciliation.md`
* `learning_and_knowledge_change_reconciliation.md`
* `contradiction_discovery_and_visibility_reconciliation.md`
* `prediction_forecasting_and_future_claims_reconciliation.md`

## Language / Operator Interface

Concern: how Seed treats natural language, intake semantics, operator intent, questions, and attribution without making interpretation, agency, or environmental truth overclaims.

Start with:

* `natural_language_observation_and_intent_derivation_reconciliation.md`
* `operator_intent_question_and_claim_interface_reconciliation.md`
* `agency_and_attribution_reconciliation.md`

## Relationship Semantics

Concern: how connection claims become represented relationships without turning observation, projection, or source vocabulary into unrestricted graph truth.

Start with:

* `relationship_fact_reconciliation.md`
* `relationship_promotion_reconciliation.md`
* `relationship_observation_v0_reconciliation.md`


## Knowledge Navigation

Concern: how Seed, contributors, and operators navigate from questions to concepts, architectural boundaries, documentation, repository structure, and implementation artifacts.

Start with:

* `knowledge_navigation_layers_frontier.md`
* `knowledge_and_understanding_distinction_observation.md`
* `documentation_observation_frontier.md`
* `repository_observation_frontier.md`
* `architectural_knowledge_map.md`
* `navigation_hygiene_audit.md`
* `source_navigation_surface_reconciliation.md`
* `repository_orientation_audit.md`
* `source_navigation_entity_typing_graph_issue_audit.md`
* `understanding_visibility_existing_surface_audit.md`

This is currently a frontier characterization, not a reconciliation or implementation plan. It records structural navigation, architectural navigation, and knowledge navigation as related but non-identical layers.


## Emerging Meta-Architecture Frontiers

Concern: recently characterized or emerging questions about navigation, operations, operation attribution, relationship ontology, inquiry, attention, active-edge pressure, object/role/operation boundaries, concept stability, persistence, continuity, current work position, view/lens/orientation boundaries, descriptive-language promotion pressure, authority formation, bounded-consequence discipline, operator-entrypoint pressure, derivation, handoff/continuation lineage, observed documentation lineage, discovery-path preservation, lineage distinction, documentation compression, explanatory-load pressure, understanding-as-claim pressure, knowledge-and-understanding distinction pressure, decompression-shaped learning, and observation-surface limits.

Start with:

* `knowledge_navigation_layers_frontier.md`
* `derivation_frontier.md`
* `operations_frontier.md`
* `operation_attribution_frontier.md`
* `relationship_frontier.md`
* `handoff_and_continuation_lineage_frontier.md`
* `inquiry_frontier.md`
* `selection_and_attention_frontier.md`
* `attention_trigger_frontier.md`
* `attention_target_frontier.md`
* `active_edge_frontier.md`
* `participant_orientation_view_selection_observation.md`
* `view_branch_continuity_reconciliation.md`
* `object_role_and_operation_frontier.md`
* `concept_stability_audit.md`
* `promotion_and_reconciliation_observation.md`
* `role_of_descriptive_vocabulary_observation.md`
* `descriptive_language_vs_authority_observation.md`
* `defines_authority_reconciliation_observation.md`
* `defines_relationship_reconciliation_audit.md`
* `authority_formation_pattern_observation.md`
* `authority_owner_observation.md`
* `repository_orientation_audit.md`
* `repository_surface_inventory_observation.md`
* `bounded_consequence_discipline_observation.md`
* `state_summary_decomposition_audit.md`
* `operator_entrypoint_pressure_audit.md`
* `graph_issue_orientation_audit.md`
* `source_navigation_entity_typing_graph_issue_audit.md`
* `documentation_lineage_observation.md`
* `observation_surface_and_blind_spot_audit.md`
* `discovery_path_preservation_observation.md`
* `lineage_distinction_observation.md`
* `preservation_surface_observation.md`
* `documentation_compression_observation.md`
* `understanding_claim_and_decompression_observation.md`
* `bounty_board_and_investigation_selection_observation.md`
* `persistence_frontier.md`
* `continuity_frontier.md`
* `current_work_position_frontier.md`
* `relation_of_use_observation.md`
* `future_frontiers.md`

Read these as a connected investigation cluster: inquiry exposes why work begins, attention asks why one unresolved possibility becomes active and what receives attention, active edge asks what currently pulls work forward among preserved concerns, view/lens/orientation work asks how participant position and selected view shape continuation without changing View authority, descriptive-language and `defines` work asks how useful language, metadata, and reconciliation pressure relate to authority without making promotion automatic, surface and bounded-consequence work asks how repository-facing surfaces constrain effect and responsibility, object/role/operation asks whether candidate concepts are durable things or contextual participation, persistence/continuity/current-work-position asks what survives change and what orientation must survive for active work to resume without collapsing into storage, identity, or implementation machinery, documentation lineage observes how these investigations generated follow-on documents without defining lineage as architecture, the observation-surface audit records what that lineage observation could and could not see, discovery-path preservation observes critique-driven understanding transitions, lineage distinction observes which artifact, inquiry, observation, and discovery-path surfaces appear distinct or overlapping, bounty-board/investigation-selection observation records how inquiry appears to have become active without treating the bounty board as roadmap authority, and relation-of-use observation records the boundary where preserved knowledge remains useful or becomes inert without defining ontology or implementation. These documents should be read as frontier/status/map routing, not as canonical architecture. Do not use this cluster to promote operations, inquiry, attention, active-edge, view, lens, orientation, authority owner, bounded consequence, object, role, persistence, continuity, current work position, derivation, lineage, critique, or discovery-retrospective concepts into the foundational ontology without a later reconciliation.

## Knowledge Selection

Concern: how Seed selects relevant projected knowledge for a response or decision context.

Start with:

* `context_composition_reconciliation.md`
* `context_composition_vocabulary.md`
* `selection_rationale_characterization.md`
* `selection_rationale_vocabulary.md`
* `selection_rationale_reconciliation.md`
* `selection_rationale_summary_characterization.md`

Implementation conclusions and rejected summaries are preserved in `architectural_findings_preservation.md` and scoped reconciliation documents.

## Response

Concern: how Seed communicates selected and characterized knowledge to operators.

Start with:

* `response_characterization.md`
* `response_vocabulary.md`
* `response_reconciliation.md`
* `response_caveat_characterization.md`
* `response_caveat_vocabulary.md`

Rejected response-engine and caveat-layer conclusions are preserved in `architectural_findings_preservation.md` and scoped response documents.

## Continuation / Handoff

Concern: how Seed preserves continuation alignment across handoff documents and protocols without treating handoffs as architecture authority.

Start with:

* `handoff_document_boundary_reconciliation.md`
* `handoff_template_and_continuation_protocol_reconciliation.md`
* `handoff_consumption_activation_reconciliation.md`
* `handoff_bootstrap_and_summary_reconciliation.md`
* `continuation_context_and_working_state_reconciliation.md`
* `bootstrap_invariants.md`
* `handoff_alignment_guardrails_reconciliation.md`
* `typed_projection_handoff_reconciliation.md`

## Architectural Findings

Concern: how Seed preserves completed audit outcomes, negative findings, rejected concepts, and historical conclusions.

Start with:

* `architectural_findings_characterization.md`
* `architectural_findings_vocabulary.md`
* `architectural_findings_reconciliation.md`
* `architectural_findings_preservation.md`

The consolidated rejected-concept summary belongs in `architectural_findings_preservation.md`. This map only routes to it.

---

# Canonical Architecture Pointers

Use these for current architecture content, not this map:

* `seed.md`
* `ontology.md`
* `architecture.md`
* `architecture_principles.md`
* `state.md`
* `invariants.md`
* `knowledge_acquisition_and_selection.md`
* `knowledge_lifecycle_reconciliation.md`
* `knowledge_maintenance_reconciliation.md`

Use `documentation_lifecycle_reconciliation.md` and `documentation_authority_reconciliation.md` for role and authority definitions.

---

# Roadmap And Status Pointers

* Current status and active frontier: `architectural_status_and_next_frontier.md`
* Roadmap sequencing and backlog context: `reasoning_roadmap.md`
* Acquisition slice details: `knowledge_acquisition_status.md` and `local_observation_roadmap_reconciliation.md`
* Preserved findings and rejected concepts: `architectural_findings_preservation.md`
