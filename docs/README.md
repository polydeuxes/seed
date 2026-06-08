# Seed Documentation

This directory contains the architectural knowledge, audits, vocabularies, reconciliations, status reviews, roadmaps, and observation designs that describe how Seed works and why it works that way.

The README is the documentation entry point. It owns navigation and orientation only; it does not own current status, active frontier, rejected-concept rationale, preserved findings, roadmap sequencing, lifecycle roles, or canonical architecture definitions.

For authority boundaries, see `documentation_authority_reconciliation.md` and `documentation_boundary_enforcement_reconciliation.md`.

---

# Start Here

1. `architectural_knowledge_map.md` — concern map and routing to the documents that own each answer.
2. `architectural_status_and_next_frontier.md` — current architectural status, active frontier, and current priorities.
3. `architectural_findings_preservation.md` — completed findings, negative findings, rejected concepts, and historical conclusions.
4. `reasoning_roadmap.md` — roadmap sequencing, backlog context, and concern evolution.

---

# Common Questions

| Question | Read |
| --- | --- |
| Where do I start? | `architectural_knowledge_map.md` |
| What is current? | `architectural_status_and_next_frontier.md` |
| What is the active frontier? | `architectural_status_and_next_frontier.md` |
| What was learned? | `architectural_findings_preservation.md` and the scoped `*_reconciliation.md` / `*_characterization.md` documents |
| What was rejected? | `architectural_findings_preservation.md` for the consolidated list; scoped reconciliations for rationale |
| What comes next? | `reasoning_roadmap.md`, with currentness checked against `architectural_status_and_next_frontier.md` |
| Which document owns which answer? | `documentation_authority_reconciliation.md` |
| How should boundaries be enforced? | `documentation_boundary_enforcement_reconciliation.md` |

---

# Concern Navigation

Seed's top-level lifecycle concerns are mapped in `architectural_knowledge_map.md` and governed by scoped documents.

| Concern | Primary starting points |
| --- | --- |
| Knowledge Acquisition | `knowledge_acquisition_status.md`, `knowledge_acquisition_and_selection.md`, `knowledge_classification_vocabulary.md` |
| Knowledge Integrity | `knowledge_maintenance_reconciliation.md`, `projection_integrity_summary_characterization.md`, `projection_integrity_drilldown_characterization.md` |
| Knowledge Selection | `context_composition_reconciliation.md`, `context_composition_vocabulary.md`, `selection_rationale_reconciliation.md`, `selection_rationale_vocabulary.md` |
| Response | `response_characterization.md`, `response_vocabulary.md`, `response_reconciliation.md`, `response_caveat_characterization.md`, `response_caveat_vocabulary.md` |
| Architectural Findings | `architectural_findings_characterization.md`, `architectural_findings_vocabulary.md`, `architectural_findings_reconciliation.md`, `architectural_findings_preservation.md` |

Use the map for routing. Use the status/frontier document for currentness. Use preservation for durable findings and rejected concepts.
