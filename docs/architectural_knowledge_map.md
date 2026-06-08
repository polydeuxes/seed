# Architectural Knowledge Map

## Purpose

This document is a lightweight navigation map for Seed's architectural knowledge.

It exists to reduce rediscovery cost.

It is not:

* a source of truth
* a registry
* an inventory
* a runtime model
* a governance process
* a replacement for canonical documents

Canonical findings remain owned by the underlying characterization, vocabulary, reconciliation, roadmap, status, and implementation documents.

See also:

* `docs/architectural_status_and_next_frontier.md`
* `docs/architectural_findings_preservation.md`
* `docs/reasoning_roadmap.md`
* `docs/knowledge_representation_map.md`
* `docs/knowledge_representation_reconciliation.md`

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
Fact
        ↓
Projected Knowledge Structures
```

Claim-justification branch:

```text
Fact
        ↓
Support Relationship
        ↓
Claim
```

Additional documentation concern:

```text
Architectural Findings
```

Architectural Findings preserves what Seed has learned about itself.

---

# Status Overview

| Concern                  | Status                   | Current Finding                                                                                              |
| ------------------------ | ------------------------ | ------------------------------------------------------------------------------------------------------------ |
| Knowledge Acquisition    | Active frontier          | Architecturally stable; capability growth remains valuable.                                                  |
| Knowledge Integrity      | Stable                   | Characterized, reconciled, summary/navigation implemented where justified.                                   |
| Knowledge Selection      | Stable                   | Characterized, vocabulary established, reconciled; Selection Rationale Summary not justified.                |
| Response                 | Complete enough          | Characterized, vocabulary established, reconciled; implementation not justified.                             |
| Response Caveats         | Complete enough / paused | Characterized and vocabulary established; further caveat audits paused unless new operator questions emerge. |
| Knowledge Representation | Emerging / reconciled    | Existing projected structures remain valid; Claim Support adds a claim-justification branch.                 |
| Architectural Findings   | Partially reconciled     | Preservation exists; discoverability, authority, and supersession remain weaker than preservation.           |

---

# Knowledge Representation

## Canonical Documents

* `docs/knowledge_representation_map.md`
* `docs/knowledge_representation_reconciliation.md`
* `docs/claim_support_frontier.md`
* `docs/claim_support_characterization.md`
* `docs/claim_support_design.md`

## Related Frontier Documents

* `docs/documentation_observation_frontier.md`
* `docs/documentation_observation_characterization.md`
* `docs/documentation_observation_design.md`
* `docs/repository_observation_frontier.md`
* `docs/repository_observation_characterization.md`
* `docs/repository_observation_design.md`
* `docs/repository_reconciliation_frontier.md`
* `docs/repository_reconciliation_characterization.md`

## Major Findings

* The process layer describes how knowledge moves.
* The representation layer describes what knowledge is.
* Existing projected knowledge structures remain valid.
* Claim Support adds a claim-justification branch.
* `FactSupport` and Claim Support should not be collapsed.

Canonical distinction:

```text
Evidence supports facts.

Facts support claims.
```

## Rejected Concepts

* `ReasoningEngine`
* `InferenceEngine` as claim support
* `TruthEngine`
* `ClaimStore`
* `SupportStore`
* automatic claim-to-claim reasoning chains

---

# Knowledge Acquisition

## Canonical Documents

* `docs/knowledge_acquisition_status.md`
* `docs/knowledge_acquisition_and_selection.md`
* `docs/knowledge_classification_vocabulary.md`
* `docs/repository_observation_source_design.md`
* `docs/self_observation_reconciliation.md`

## Major Findings

* Acquisition answers: `What do we know?`
* The acquisition path is:

```text
Observation
    ↓
Evidence
    ↓
Fact
    ↓
Projection
```

* Acquisition creates evidence-backed projected knowledge.
* Acquisition does not own explanation, integrity characterization, selection, response composition, provider execution, or truth arbitration.

## Implemented Local Observation Slices

* Identity Observation
* Mount Observation
* Kernel / CPU / Memory Observation
* Local Network Observation
* Storage Topology Observation
* Listening Port Observation
* Local Host Observation

## Current Frontier

Highest-value next slices:

1. Users Observation
2. Groups Observation
3. Package Observation
4. Systemd Observation

Additional planned slices:

* Schedule Observation
* Certificate Observation
* Process Marker Observation
* Container Marker Observation

---

# Knowledge Integrity

## Canonical Documents

* `docs/knowledge_maintenance_reconciliation.md`
* `docs/projection_integrity_summary_characterization.md`
* `docs/projection_integrity_drilldown_characterization.md`

## Major Findings

* Integrity answers: `Can this projected knowledge be safely interpreted?`
* Integrity characterizes knowledge; it does not determine truth.
* Integrity is read-only over projected knowledge.
* Existing integrity signals were already present before summary/navigation work.

## Implemented Composition

* Projection Integrity Summary v0
* Projection Integrity Navigation v0

## Rejected Concepts

* `IntegrityEngine`
* runtime-owned integrity system
* contradiction repair engine
* hidden truth-selection system
* projection mutation for integrity

---

# Knowledge Selection

## Canonical Documents

* `docs/context_composition_reconciliation.md`
* `docs/context_composition_vocabulary.md`
* `docs/selection_rationale_characterization.md`
* `docs/selection_rationale_vocabulary.md`
* `docs/selection_rationale_reconciliation.md`
* `docs/selection_rationale_summary_characterization.md`

## Major Findings

* Selection answers: `What projected knowledge matters now, and why?`
* Selection rationale already exists across distributed surfaces.
* Vocabulary was missing.
* Selection Rationale Summary implementation is not currently justified.
* Existing rationale surfaces are sufficient for current concrete questions.

## Rejected Concepts

* `SelectionEngine`
* `ContextEngine`
* Selection Rationale Summary implementation
* Selection Rationale Inventory implementation
* Selection Rationale Navigation implementation
* Selection runtime subsystem

---

# Response

## Canonical Documents

* `docs/response_characterization.md`
* `docs/response_vocabulary.md`
* `docs/response_reconciliation.md`
* `docs/explanation_contract_vocabulary.md`
* `docs/explainability_reconciliation.md`

## Major Findings

* Response answers: `How is selected knowledge communicated?`
* Response is communication, not knowledge creation.
* Response is broader than Explainability.
* Response behavior already exists across Runtime envelopes, CLI output, explanations, integrity summaries, capability inventories, state/context views, contradictions, evidence, confidence, and issue outputs.
* Response implementation is not justified by current evidence.

## Boundary

```text
Acquisition creates knowledge.
Integrity characterizes knowledge.
Selection chooses knowledge.
Response communicates knowledge.
```

## Rejected Concepts

* `ResponseEngine`
* universal formatter
* Runtime-owned response subsystem
* ToolExecutor response semantics
* parallel response system

---

# Response Caveats

## Canonical Documents

* `docs/response_caveat_characterization.md`
* `docs/response_caveat_vocabulary.md`

## Major Findings

* Caveats are communicated limitations, qualifications, warnings, uncertainty markers, status qualifiers, or non-guarantees.
* Caveat signals already exist across integrity, evidence, confidence, capability, temporal, observation, selection, response, graph, and rationale surfaces.
* Caveat vocabulary exists.
* Additional caveat-specific audit work is paused unless new evidence identifies a concrete unanswered operator question.

## Rejected Concepts

* `CaveatEngine`
* universal caveat layer
* caveat runtime subsystem
* caveat inventory implementation
* caveat navigation implementation
* parallel caveat system

---

# Architectural Findings

## Canonical Documents

* `docs/architectural_findings_characterization.md`
* `docs/architectural_findings_vocabulary.md`
* `docs/architectural_findings_reconciliation.md`
* `docs/architectural_findings_preservation.md`
* `docs/backlog_and_status_reconciliation.md`
* `docs/architectural_status_and_next_frontier.md`
* `docs/reasoning_roadmap.md`

## Major Findings

* Architectural findings already exist.
* Architectural memory already exists.
* Preservation mechanisms already exist.
* Discoverability is weaker than preservation.
* Authority is weaker than preservation.
* Supersession is weaker than preservation.

## Finding Categories

* Accepted Finding
* Rejected Concept
* Deferred Concept
* Open Question
* Current Frontier
* Architectural Lesson
* Non-Goal
* Status Update
* Historical Finding

---

# Repository-Wide Rejected Concepts

The following concepts have been repeatedly rejected unless future evidence identifies a concrete unmet need:

* `ExplainabilityEngine`
* `IntegrityEngine`
* `SelectionEngine`
* `ResponseEngine`
* `CaveatEngine`
* `ContextEngine`
* `ReasoningEngine`
* Planner
* WorkflowEngine
* Universal Formatter
* Universal Caveat Layer
* Architectural Registry
* Decision Database
* Architectural Runtime
* Runtime integration as a default solution
* ToolExecutor integration as a default solution
* parallel truth systems
* parallel response systems
* parallel caveat systems
* `ClaimStore`
* `SupportStore`
* claim-to-claim reasoning chains

---

# Current Frontier

The current frontier is **Knowledge Acquisition expansion**.

Priority:

1. Users Observation v1
2. Groups Observation v1
3. Package Observation v1
4. Systemd Observation v1

Additional emerging acquisition / reconciliation frontiers:

* Documentation Observation
* Repository Observation
* Repository Reconciliation
* Claim Support projection semantics

These should remain:

* narrow
* local
* read-only
* evidence-backed
* separate from inference
* separate from verification
* separate from execution
* separate from response composition
* separate from truth arbitration

---

# Documentation Maintenance Frontier

Low-risk documentation work:

* keep completed audit findings discoverable
* preserve negative findings
* cross-link roadmap/status/frontier documents
* avoid reopening completed audit chains without new evidence
* keep acquisition status current as new slices land

Do not create a separate heavy audit index unless discoverability materially degrades.

---

# Recurring Architectural Lessons

```text
Audit before inventing.

Ownership before implementation.

Composition before new subsystems.
```

Additional recurring lessons:

```text
Behavior often already exists.

Vocabulary is often missing.

Composition is often missing.

Ownership is often unclear.

Implementation not justified is a valid audit outcome.

Runtime is not the default integration point.

ToolExecutor is not the default integration point.
```

---

# Recommended Reading Order

For new sessions:

1. `docs/architectural_knowledge_map.md`
2. `docs/knowledge_representation_map.md`
3. `docs/knowledge_representation_reconciliation.md`
4. `docs/architectural_findings_preservation.md`
5. `docs/architectural_status_and_next_frontier.md`
6. `docs/reasoning_roadmap.md`
7. `docs/knowledge_acquisition_status.md`
8. concern-specific characterization/vocabulary/reconciliation docs only as needed

This order is meant to reduce context cost before deeper audit work.
