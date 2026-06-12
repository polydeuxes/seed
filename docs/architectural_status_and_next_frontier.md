# Architectural Status And Next Frontier

## Purpose

This document owns Seed's current architectural status, active frontier, and current priorities across major concerns.

It may reference completed findings as context, but preservation belongs in `architectural_findings_preservation.md`. Roadmap sequencing belongs in `reasoning_roadmap.md`. Concern mapping belongs in `architectural_knowledge_map.md`. Authority and boundary rules are governed by `documentation_authority_reconciliation.md` and `documentation_boundary_enforcement_reconciliation.md`.

---

# Executive Summary

Seed's major conceptual reconciliation pass is complete enough to return active attention from recursive architecture audits to bounded implementation work. Foundational ontology, handoff boundaries and template/protocol, handoff consumption/activation/compliance, agency and attribution, natural-language observation and intent derivation, cross-Seed provenance and federation, learning and knowledge change, contradiction discovery and visibility, and prediction/future-claim boundaries have now been reconciled and routed through the documentation map.

Current recommended priority:

1. **Bounded implementation work** over concrete observation/projection problems, starting with the Prometheus boundary issues already documented.
2. **Prometheus observation and projection cleanup** while preserving provenance and avoiding over-promotion.
3. **Documentation maintenance** only where it keeps completed findings and frontier routing discoverable while keeping authority boundaries clear.
4. **Future investigation** only where a concrete unanswered operator question exists. Characterized and emerging frontiers are inputs to future inquiry, not canonical architecture and not implementation-ready by default.

---

# Architectural Status

| Concern | Current classification | Current finding |
| --- | --- | --- |
| Foundational Ontology | **Reconciled / Vocabulary Established / Architecturally Stable** | Seed is claim-centric. `ontology.md` is the concise vocabulary reference; `foundational_ontology_reconciliation.md` owns the detailed audit. The ontology is not a schema. |
| Handoff / Continuation | **Reconciled / Architecturally Stable** | Handoffs preserve continuation alignment and authority boundaries. Safe continuation distinguishes availability, consumption, activation, and compliance; handoffs and activation are not architecture authority. |
| Language / Attribution | **Reconciled / Architecturally Stable** | Natural language is observation of communicative acts; interpretation derives candidate meaning; attribution is a supportable claim, not consciousness, desire, or agency. |
| Federation / Foreign Testimony | **Reconciled / Architecturally Stable** | Federation transfers evidence, provenance, and scoped testimony. It does not transfer truth, and import is not verification. |
| Learning / Knowledge Change | **Reconciled / Architecturally Stable** | Learning is cross-layer knowledge change that preserves support and history rather than replacing or erasing them. |
| Contradiction Discovery / Visibility | **Reconciled / Architecturally Stable** | Contradiction existence, discovery, projection, visibility, explanation, and resolution are distinct. Discovery does not create contradiction; visibility is not existence. |
| Prediction / Future Claims | **Reconciled / Architecturally Stable** | Predictions, forecasts, expectations, scenarios, consequences, and plans are future-oriented claims with support, uncertainty, scope, and authority boundaries. They are not observations or future facts. |
| Knowledge Acquisition | **Implemented / Partially Complete / Active Implementation Frontier** | The claim-centric Observation → Evidence → Claim → Fact / Relationship → Projection frame is established. Current value is concrete cleanup and bounded observation work, especially Prometheus observation/projection boundaries. |
| Knowledge Integrity | **Reconciled / Implemented / Architecturally Stable** | Integrity is a read-only projected-knowledge concern covering support, conflicts, contradictions, staleness, graph issues, confidence, verification limits, and disclosure. |
| Knowledge Selection | **Reconciled / Vocabulary Established / Architecturally Stable** | Context Composition and Selection Rationale are covered by characterization, vocabulary, and reconciliation. New summary/runtime implementation is not currently justified. |
| Knowledge Navigation | **Frontier Characterized / Not Reconciled / Not Implementation-Ready** | `knowledge_navigation_layers_frontier.md` records structural, architectural, and knowledge navigation as related but non-identical graph layers. Navigation is not authority, and the open question is whether repository, architecture, and knowledge graphs are independent or projections of a larger graph. |
| Derivation | **Frontier Characterized / Not Reconciled / Not Implementation-Ready** | `derivation_frontier.md` characterizes when represented support may justify newly represented propositions or relationships. It does not create a reasoning engine, schema, runtime, or canonical derivation ontology. |
| Operations | **Frontier Characterized / Not Reconciled / Not Implementation-Ready** | `operations_frontier.md` characterizes a possible operation layer and object/operation boundary. It must not be treated as canonical ontology or implementation direction. |
| Operation Attribution | **Frontier Characterized / Not Reconciled / Not Implementation-Ready** | `operation_attribution_frontier.md` separates actor participation, authority, responsibility, ownership, approval, adoption, execution, provenance, and explanation questions without settling a runtime model. |
| Handoff / Continuation Lineage | **Frontier Characterized / Not Reconciled / Not Implementation-Ready** | `handoff_and_continuation_lineage_frontier.md` characterizes working-knowledge and investigation-lineage preservation across handoffs while preserving that handoffs are not architecture authority. |
| Inquiry | **Exploratory Frontier / Not Reconciled / Not Implementation-Ready** | `inquiry_frontier.md` asks whether inquiry has objects, lifecycle, lineage, branches, and tensions distinct from claim-centered knowledge. It records evidence and questions without introducing an inquiry runtime or canonical ontology. |
| Response | **Reconciled / Vocabulary Established / Partially Complete / Architecturally Stable** | Response is a distributed communication concern across existing response, context, explanation, integrity, capability, evidence, contradiction, confidence, and issue surfaces. |

For preserved audit-chain outcomes and rejected concepts, see `architectural_findings_preservation.md`.

---

# Active Frontier

Recommended next frontier: **bounded implementation cleanup**, beginning with the concrete Prometheus problems already identified by `prometheus_observation_boundary_reconciliation.md` and `prometheus_endpoint_identity_boundary_audit.md`.

Current Prometheus cleanup candidates:

1. separate `up` scrape-target semantics from host, service, and application availability;
2. preserve endpoint identity instead of collapsing endpoint identity into host identity;
3. split overloaded `provides` usage across endpoint role, service/application exposure, capability, and monitoring-system relationships;
4. reduce state-summary noise from filesystem measurements without dropping evidence;
5. distinguish mounted/shared storage identity from mount observations;
6. clean relationship and entity-type projections that expose unknown hosts because alias, endpoint, and host boundaries are blurred.

Implementation should preserve source scope, evidence support, relationship semantics, and projection humility. It should not over-promote endpoint evidence into host truth, service truth, storage identity, or capability ownership.

---

# Current Priorities

## 1. Prometheus observation/projection cleanup

Proceed through narrow changes that:

- keep Prometheus data scoped to its source vantage point;
- treat scrape success as endpoint-scoped evidence unless additional support exists;
- separate endpoint, host, service/component, monitoring system, capability, mount, and storage identities;
- preserve observations and evidence even when projections become less noisy;
- route unresolved relationship vocabulary questions through the existing Prometheus boundary documents rather than inventing broad new architecture.

## 2. Bounded Knowledge Acquisition work

Additional observation slices remain appropriate when they:

- use read-only evidence;
- record observations through the established observation path;
- emit bounded evidence-backed claims, including normalized facts or relationships where supported;
- avoid execution, provider calls, Runtime routing, ToolExecutor integration, health inference, ownership inference, and mutation;
- preserve caveats and limitations through existing Integrity, Selection, and Response surfaces.

## 3. Documentation maintenance

Maintenance should reduce duplicate authority and keep completed findings discoverable. `navigation_hygiene_audit.md` records current documentation navigation hygiene findings without replacing authoritative reconciliations. Maintenance should not create new document categories, registries, inventories, or additional architecture systems.

Supported later documentation frontiers include turning the handoff template into a concrete artifact, generated documentation/wiki projection, automatic observation refresh boundaries, natural-language/prose intake implementation notes where existing reconciliation documents already support that work, and careful follow-up on the characterized navigation, derivation, operations, operation-attribution, inquiry, and handoff-lineage frontiers. Follow-up should remain investigation unless a later reconciliation promotes specific conclusions.

## 4. Future investigation

Start future investigations only when a concrete operator question is important, recurring, and not answered by existing documents or surfaces.

---

# Paused Or Non-Current Work

The following are not active frontiers unless new evidence appears:

- recursive conceptual audits without a concrete operator or implementation question;
- implementation of repository, architecture, or knowledge graph unification before the knowledge-navigation frontier is reconciled;
- implementation of operation, inquiry, derivation, attribution, or continuation-lineage runtimes/schemas before those frontiers are reconciled;
- Selection Rationale Summary implementation;
- Response engine or universal formatter work;
- Integrity, Selection, Context, Explainability, Caveat, Planner, Workflow, or Reasoning engines;
- Runtime or ToolExecutor integration as a default fix;
- projection mutation, event appends, truth arbitration, provider calls, execution, verification, refresh, repair, planning, workflow orchestration, language-as-environmental-truth, interpretation-as-verification, attribution-as-consciousness, federation-as-truth-transfer, import-as-verification, learning-as-history-erasure, contradiction-discovery-as-contradiction-creation, visibility-as-existence, prediction-as-observation, plan-as-future-fact, projection-as-authority, capability-as-agency, or handoff-as-architecture from this documentation work.

Detailed preservation and rejection rationale belongs in `architectural_findings_preservation.md` and scoped reconciliation documents.

---

# Non-Goals

This document does not:

- implement observations;
- implement caveats, summaries, inventories, navigation, routes, adapters, schema classes, read models, or engines;
- modify Runtime, ToolExecutor, EventLedger, ProjectionStore, providers, projections, acquisition logic, selection behavior, response behavior, policy behavior, or tests;
- mutate projections or append events;
- create parallel truth, response, caveat, selection, explanation, integrity, ontology, handoff, or context systems;
- start a new audit chain;
- preserve the full rejected-concept list or completed finding rationale.

---

# Conclusion

Current architectural status points back to bounded implementation cleanup. The most concrete next work is Prometheus observation/projection cleanup under the already reconciled observation, endpoint identity, provenance, claim-promotion, and projection-authority boundaries.
