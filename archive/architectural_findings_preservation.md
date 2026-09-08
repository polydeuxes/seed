# Architectural Findings Preservation

## Purpose

This document preserves completed findings, negative findings, rejected concepts, deferred concepts, and durable historical conclusions from Seed's completed audit chains.

It owns preservation. It does not own current status, active frontier, roadmap sequencing, navigation, lifecycle definitions, or canonical architecture content. For currentness, see `architectural_status_and_next_frontier.md`. For roadmap sequencing, see `reasoning_roadmap.md`. For authority boundaries, see `documentation_authority_reconciliation.md` and `documentation_boundary_enforcement_reconciliation.md`.

---

# Preservation Summary

Recent architecture audit sequences converged on a durable finding: Seed usually did not need a new subsystem. The audited behavior already existed, ownership already existed, and composition often existed. The recurring gaps were vocabulary, discoverability, status, and handoff clarity.

This document preserves those conclusions so future work can start from settled architecture instead of rediscovering the same questions.

---

# Architectural Findings Worth Preserving

| Finding | Preservation guidance |
| --- | --- |
| Behavior already exists before implementation assumptions. | Inspect existing surfaces before proposing new code. Recent Response, Selection Rationale, Response Caveat, Projection Integrity, Context Composition, and Explainability work found distributed behavior before missing implementation. |
| Ownership before implementation. | Identify the existing owner of each semantic concern before introducing a new owner. |
| Composition before new subsystems. | Prefer cross-links, handoff notes, status tables, or documentation maps over engines, universal formatters, or centralized layers when existing surfaces already carry the semantics. |
| Audit before inventing. | Characterize existing behavior and boundaries before adding objects, routes, adapters, read models, schemas, or execution paths. |
| Implementation not justified is a valid outcome. | Record non-implementation conclusions as architecture knowledge, not incomplete work. |
| Negative findings are architectural findings. | Rejections such as “no engine,” “no summary,” “no Runtime integration,” and “no ToolExecutor integration” prevent architecture drift and should stay discoverable. |
| Vocabulary can be enough. | Stable terms can be sufficient when behavior and ownership already exist. |
| Runtime is not the default integration point. | Runtime owns routing and response envelopes; it is not the universal home for selection, integrity, caveats, explanations, or response composition semantics. |
| ToolExecutor is not the default integration point. | ToolExecutor owns registered-operation execution; it is not a verification, truth-selection, caveat, response, or rationale engine. |
| Acquisition creates; Integrity characterizes; Selection selects; Response communicates. | Preserve this lifecycle framing when adding future documentation or observation slices. |

---

# Completed Audit Sequences

Completed and paused audit sequences should be recorded as settled architectural memory, not as open implementation backlog.

| Audit sequence | Preserved status | Final handoff |
| --- | --- | --- |
| Explainability | Resolved enough for now. | Explanation behavior and ownership exist through existing explanation, evidence, confidence, conflict, and projection surfaces. No `ExplainabilityEngine` is justified. |
| Context Composition | Resolved enough for now. | Context composition vocabulary and reconciliation established distributed context selection, relevance, priority, and budget concepts. No `ContextEngine` is justified. |
| Knowledge Integrity | Resolved enough for now. | Integrity is a read-only projected-knowledge concern over support, conflict, staleness, confidence, graph issues, verification limits, and source limitations. |
| Projection Integrity Summary | Characterized and implemented where justified. | Summary work is read-only visibility over existing projected integrity signals, not a repair or truth engine. |
| Projection Integrity Navigation / Drilldown | Characterized and implemented where justified. | Navigation should remain linked to existing integrity structures and should not create a parallel truth system. |
| Selection Rationale | Complete. | Characterization, vocabulary, reconciliation, and summary characterization established distributed rationale. Selection Rationale Summary implementation is not currently justified. |
| Response | Complete enough for current architecture. | Response is a distributed operator-facing communication concern. No `ResponseEngine`, universal formatter, Runtime rewrite, or ToolExecutor integration is justified. |
| Response Caveats | Complete enough for now; paused. | Caveat vocabulary exists and caveat signals already live in source surfaces. Additional caveat-specific audit chains are not currently justified. |
| Backlog and Status Reconciliation | Complete for Selection Rationale handoff. | Selection Rationale should remain completed-audit / documentation-maintenance work, not generic implementation backlog. |
| Architectural Status and Next Frontier | Complete for current frontier choice. | Preserves the handoff that current frontier ownership belongs in `architectural_status_and_next_frontier.md`. |

Future current-status labels belong in `architectural_status_and_next_frontier.md`; this table preserves completed-chain outcomes.

---

# Negative Findings And Rejected Concepts

These negative findings block repeated rediscovery and protect accepted ownership boundaries:

- **Selection Rationale Summary implementation is not justified.** Existing rationale surfaces answer current concrete questions well enough; a first-class summary would require new classification, inventory, history, or read-model semantics without demonstrated operator need.
- **Selection Rationale Inventory, Navigation, and Drilldown are not justified as new runtime artifacts.** Documentation cross-links are acceptable; new read models, routes, schemas, adapters, or engines are not currently warranted.
- **Response implementation is not justified.** Response behavior already exists across response envelopes, CLI output, context/state views, explanations, integrity surfaces, capability surfaces, evidence, contradictions, confidence, and issue outputs.
- **Response Caveat implementation is not justified.** Caveat signals already exist in source surfaces; a universal caveat layer would duplicate source semantics and risk a parallel limitation system.
- **Repeated engine rejection is settled architectural memory.** The audit program repeatedly rejected `ReasoningEngine`, `IntegrityEngine`, `ExplainabilityEngine`, `SelectionEngine`, `ResponseEngine`, `ContextEngine`, planners, workflow engines, universal formatters, universal caveat layers, parallel truth systems, parallel response systems, and parallel caveat systems.
- **Runtime and ToolExecutor integration are not default fixes.** Neither owner should absorb selection, caveat, response, integrity, or explanation semantics merely because a future document wants a central place to look.
- **Parallel truth systems must be avoided.** Documentation, rationale, caveats, summaries, and responses must not introduce hidden trust scores, automatic contradiction repair, projection mutation, or independent fact stores.

Scoped reconciliation documents own detailed rationale for each rejection. This document preserves the consolidated rejected-concept memory.

---

# Frontier Handoff Reference

The current frontier is owned by `architectural_status_and_next_frontier.md`.

This preservation record keeps only the historical conclusion that completed audit chains handed off toward bounded Knowledge Acquisition expansion rather than recursive architecture decomposition, new engines, Runtime integration, ToolExecutor integration, projection mutation, or parallel truth systems.

For acquisition candidate details, use `knowledge_acquisition_status.md` and `local_observation_roadmap_reconciliation.md`. For roadmap sequencing, use `reasoning_roadmap.md`.

---

# Conclusion

The recent audit program produced durable architectural knowledge: Seed's next work should not default to another engine, planner, universal layer, or recursive audit chain. Future work should consult the current status/frontier document for active priorities and this preservation document for the settled findings that constrain them.
