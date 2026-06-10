# Architectural Status And Next Frontier

## Purpose

This document owns Seed's current architectural status, active frontier, and current priorities across major concerns.

It may reference completed findings as context, but preservation belongs in `architectural_findings_preservation.md`. Roadmap sequencing belongs in `reasoning_roadmap.md`. Concern mapping belongs in `architectural_knowledge_map.md`. Authority and boundary rules are governed by `documentation_authority_reconciliation.md` and `documentation_boundary_enforcement_reconciliation.md`.

---

# Executive Summary

Seed's major lifecycle documentation is stable enough to shift active architecture attention away from recursive audits and toward bounded Knowledge Acquisition expansion. Foundational ontology, attribution, natural-language observation, and handoff continuation boundaries have now been reconciled and routed through the documentation map.

Current recommended priority:

1. **Knowledge Acquisition expansion** through narrow, read-only observation slices.
2. **Documentation maintenance** only where it keeps completed findings discoverable and authority boundaries clear.
3. **Future investigation** only where a concrete unanswered operator question exists.
4. **No Runtime implementation** from the completed audit chains.

---

# Architectural Status

| Concern | Current classification | Current finding |
| --- | --- | --- |
| Knowledge Acquisition | **Implemented / Partially Complete / Architecturally Stable** | The claim-centric Observation → Evidence → Claim → Fact / Relationship → Projection frame is established. Remaining value is concrete capability growth through bounded local observation slices. |
| Knowledge Integrity | **Reconciled / Implemented / Architecturally Stable** | Integrity is a read-only projected-knowledge concern covering support, conflicts, contradictions, staleness, graph issues, confidence, verification limits, and disclosure. |
| Knowledge Selection | **Reconciled / Vocabulary Established / Architecturally Stable** | Context Composition and Selection Rationale are covered by characterization, vocabulary, and reconciliation. New summary/runtime implementation is not currently justified. |
| Response | **Reconciled / Vocabulary Established / Partially Complete / Architecturally Stable** | Response is a distributed communication concern across existing response, context, explanation, integrity, capability, evidence, contradiction, confidence, and issue surfaces. |
| Response Caveats | **Characterized / Vocabulary Established / Stable For Now** | Caveat signals are real and distributed. Vocabulary exists. Additional caveat work should pause unless a concrete operator question appears. |

For preserved audit-chain outcomes and rejected concepts, see `architectural_findings_preservation.md`.

---

# Active Frontier

Recommended next frontier: **Knowledge Acquisition expansion**.

The strongest current candidates are bounded, read-only observation slices that add new evidence-backed claims without changing Runtime, ToolExecutor, EventLedger ownership, ProjectionStore ownership, providers, response behavior, selection behavior, integrity semantics, or policy behavior.

Highest-value near-term candidates:

1. **Users Observation**
2. **Groups Observation**
3. **Package Observation**
4. **Systemd Observation**

Use `knowledge_acquisition_status.md` and `local_observation_roadmap_reconciliation.md` for acquisition-slice details and constraints.

---

# Current Priorities

## 1. Knowledge Acquisition expansion

Proceed through narrow observation slices that:

- use read-only local evidence;
- record observations through the established observation path;
- emit bounded evidence-backed claims, including normalized facts where supported;
- avoid execution, network probing, provider calls, Runtime routing, ToolExecutor integration, health inference, ownership inference, and mutation;
- preserve caveats and limitations through existing Integrity, Selection, and Response surfaces.

## 2. Documentation maintenance

Maintenance should reduce duplicate authority and keep completed findings discoverable. It should not create new document categories, registries, inventories, or additional architecture systems.

Current maintenance should follow `documentation_authority_reconciliation.md` and `documentation_boundary_enforcement_reconciliation.md`. Supported maintenance frontiers include turning the handoff template into a concrete artifact, applying natural-language observation boundaries to implementation, clarifying automatic observation refresh boundaries, and generated wiki/projection documentation only where existing reconciliation documents already support that work.

## 3. Future investigation

Start future investigations only when a concrete operator question is important, recurring, and not answered by existing documents or surfaces.

---

# Paused Or Non-Current Work

The following are not active frontiers unless new evidence appears:

- recursive Response Caveat audits without a concrete operator question;
- Selection Rationale Summary implementation;
- Response engine or universal formatter work;
- Integrity, Selection, Context, Explainability, Caveat, Planner, Workflow, or Reasoning engines;
- Runtime or ToolExecutor integration as a default fix;
- projection mutation, event appends, truth arbitration, provider calls, execution, verification, refresh, repair, planning, workflow orchestration, language-as-environmental-truth, attribution-as-consciousness, capability-as-agency, or handoff-as-architecture from this documentation work.

Detailed preservation and rejection rationale belongs in `architectural_findings_preservation.md` and scoped reconciliation documents.

---

# Non-Goals

This document does not:

- implement observations;
- implement caveats, summaries, inventories, navigation, routes, adapters, schema classes, read models, or engines;
- modify Runtime, ToolExecutor, EventLedger, ProjectionStore, providers, projections, acquisition logic, selection behavior, response behavior, policy behavior, or tests;
- mutate projections or append events;
- create parallel truth, response, caveat, selection, explanation, integrity, or context systems;
- start a new audit chain;
- preserve the full rejected-concept list or completed finding rationale.

---

# Conclusion

Current architectural status points to bounded Knowledge Acquisition expansion as the active frontier. Preservation, roadmap sequencing, and concern mapping remain available through their owning documents rather than being restated here.
