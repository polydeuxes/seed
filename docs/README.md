# Seed Documentation

This directory contains the architectural knowledge, audits, vocabularies, reconciliations, status reviews, roadmaps, and observation designs that describe how Seed works and why it works that way.

The repository has accumulated significant architectural knowledge over time. New readers should begin with the navigation documents below before diving into individual audit chains.

---

# Recommended Reading Order

## 1. Architectural Knowledge Map

Start here:

`architectural_knowledge_map.md`

Provides:

* architectural overview
* concern map
* canonical documents
* major findings
* rejected concepts
* current frontiers
* reading order

---

## 2. Architectural Findings Preservation

`architectural_findings_preservation.md`

Provides:

* completed audit findings
* negative findings
* rejected concepts
* deferred concepts
* preservation of major architectural conclusions

---

## 3. Architectural Status And Next Frontier

`architectural_status_and_next_frontier.md`

Provides:

* current repository status
* completed audit chains
* active architectural frontier
* capability-growth priorities

---

## 4. Reasoning Roadmap

`reasoning_roadmap.md`

Provides:

* historical roadmap
* concern evolution
* future work
* backlog context

---

# Architectural Concerns

Seed currently organizes architectural thinking around four primary concerns:

```text
Knowledge Acquisition
        ↓
Knowledge Integrity
        ↓
Knowledge Selection
        ↓
Response
```

Additional documentation concern:

```text
Architectural Findings
```

---

# Concern Reading Order

## Knowledge Acquisition

Primary documents:

* knowledge_acquisition_status.md
* knowledge_acquisition_and_selection.md
* knowledge_classification_vocabulary.md
* repository_observation_source_design.md
* self_observation_reconciliation.md

Current frontier:

* Users Observation
* Groups Observation
* Package Observation
* Systemd Observation

---

## Knowledge Integrity

Primary documents:

* knowledge_maintenance_reconciliation.md
* projection_integrity_summary_characterization.md
* projection_integrity_drilldown_characterization.md

Implemented composition:

* Projection Integrity Summary v0
* Projection Integrity Navigation v0

---

## Knowledge Selection

Primary documents:

* context_composition_reconciliation.md
* context_composition_vocabulary.md
* selection_rationale_characterization.md
* selection_rationale_vocabulary.md
* selection_rationale_reconciliation.md
* selection_rationale_summary_characterization.md

Important finding:

Selection Rationale Summary implementation is not currently justified.

---

## Response

Primary documents:

* response_characterization.md
* response_vocabulary.md
* response_reconciliation.md
* response_caveat_characterization.md
* response_caveat_vocabulary.md

Important finding:

Response exists primarily as communication of selected and characterized knowledge.

---

## Architectural Findings

Primary documents:

* architectural_findings_characterization.md
* architectural_findings_vocabulary.md
* architectural_findings_reconciliation.md

Important finding:

Architectural memory already exists; discoverability remains weaker than preservation.

---

# Rejected Concepts

The following concepts have been repeatedly evaluated and rejected unless future evidence identifies a concrete unmet need:

* ExplainabilityEngine
* IntegrityEngine
* SelectionEngine
* ResponseEngine
* CaveatEngine
* ContextEngine
* ReasoningEngine
* Planner
* WorkflowEngine
* Universal Formatter
* Architectural Registry
* Decision Database
* Architectural Runtime
* Parallel truth systems
* Parallel response systems

---

# Recurring Architectural Lessons

```text
Audit before inventing.

Ownership before implementation.

Composition before new subsystems.
```

Additional recurring findings:

```text
Behavior often already exists.

Vocabulary is often missing.

Composition is often missing.

Ownership is often unclear.

Implementation not justified is a valid outcome.
```
