---
doc_type: observation
status: exploratory
domain: classification coverage diagnostic
defines:
  - live classification coverage unknown contributor observation
  - classification coverage diagnostic boundary
related:
  - diagnostic_result_self_observation.md
  - graph_issue_orientation_audit.md
  - source_navigation_entity_typing_graph_issue_audit.md
introduced_by: classification coverage diagnostic follow-up 2026-06-19
---

# Live Classification Coverage Unknown Contributor Observation

## Status

Exploratory observation only.

This document records a live-system diagnostic finding. It does not propose fixes, redesign entity types, redesign predicates, create an ontology proposal, or create a remediation plan.

## Observation

Seed's live classification coverage diagnostic showed broad unknown-entity coverage, with graph issues dominated by unknown endpoints and top unknown predicates spanning source observation, imports, local host facts, listener facts, and Prometheus-shaped facts.

The diagnostic result made unknown contributors visible as an implementation diagnostic concern: Seed can observe many entities, while the current projection classified comparatively few of them at that diagnostic boundary.

## Boundaries

- Unknown does not mean wrong.
- A classification gap does not mean ontology failure.
- A graph issue does not mean relationship authority failure.
- A diagnostic result is not permanent truth.

## Non-Goals

This observation does not propose classification fixes, relationship changes, predicate changes, entity-type changes, or architectural reconciliation.
