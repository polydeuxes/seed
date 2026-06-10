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
| How should natural-language requests be treated? | `natural_language_observation_and_intent_derivation_reconciliation.md`, `operator_intent_question_and_claim_interface_reconciliation.md` |
| How should agency or attribution be handled? | `agency_and_attribution_reconciliation.md` |
| How should continuation across handoffs be preserved? | `handoff_document_boundary_reconciliation.md`, `handoff_template_and_continuation_protocol_reconciliation.md` |

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

Currentness and frontier ownership remain in `architectural_status_and_next_frontier.md`.

## Knowledge Integrity

Concern: how Seed characterizes reliability, support, conflict, contradiction, staleness, confidence, and verification limits for projected knowledge.

Start with:

* `knowledge_maintenance_reconciliation.md`
* `projection_integrity_summary_characterization.md`
* `projection_integrity_drilldown_characterization.md`
* `knowledge_representation_map.md`
* `knowledge_representation_reconciliation.md`

## Language / Operator Interface

Concern: how Seed treats natural language, operator intent, questions, and attribution without making interpretation, agency, or environmental truth overclaims.

Start with:

* `natural_language_observation_and_intent_derivation_reconciliation.md`
* `operator_intent_question_and_claim_interface_reconciliation.md`
* `agency_and_attribution_reconciliation.md`

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
