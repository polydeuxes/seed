# Executive Summary

Seed's recent architecture work has reconciled the major documentation questions around the current knowledge lifecycle:

```text
Knowledge Acquisition
↓
Knowledge Integrity
↓
Knowledge Selection
↓
Response
```

The strongest current finding is that Seed is not missing a family of engines. The repository already has evidence-backed acquisition, projected integrity signals, deterministic selection/context surfaces, and distributed response surfaces. Recent audits mostly found behavior before vocabulary, unclear ownership before reconciliation, and fragmented composition before cross-links. Those gaps have now been substantially addressed for Integrity, Selection, Response, and Response Caveats through characterization, reconciliation, and vocabulary documents.

The next highest-value frontier is **Knowledge Acquisition expansion**, not another recursive audit chain and not Runtime implementation. Acquisition still has concrete, bounded, read-only candidates such as Users, Groups, Packages, Systemd Units, Schedules, Certificates, Process Markers, and Container Markers. Those candidates fit the established observation-to-evidence-to-fact-to-projection architecture and can add useful knowledge without changing Runtime, ToolExecutor, EventLedger ownership, ProjectionStore ownership, providers, projections, or response behavior.

Recommended priority:

1. **Knowledge Acquisition expansion** through narrow read-only observation slices.
2. **Documentation maintenance** to keep completed audit findings discoverable.
3. **Future investigation** only where a concrete unanswered operator question exists.
4. **No Runtime implementation** from this audit.

# Purpose

This document performs a documentation-only Architectural Status And Next-Frontier Reconciliation.

It answers:

- which major architectural concerns are effectively reconciled;
- which audit chains are complete;
- which negative findings should be preserved;
- which open questions remain evidence-supported;
- whether caveat-specific audit chains should continue;
- whether the next frontier should be more audits, documentation maintenance, acquisition expansion, or runtime implementation.

# Scope

In scope:

- current status of Knowledge Acquisition, Knowledge Integrity, Knowledge Selection, Response, and Response Caveats;
- completed audit chains and unresolved audit questions;
- negative architectural findings worth preserving;
- evidence-supported open architectural questions;
- acquisition roadmap and backlog references;
- low-risk documentation maintenance opportunities;
- rejection criteria for starting additional audit chains;
- recommendation for the next frontier.

Out of scope:

- implementing observations;
- implementing caveats;
- implementing summaries, inventories, navigation, routes, adapters, schema classes, read models, or engines;
- Runtime, ToolExecutor, EventLedger, ProjectionStore, provider, or model-client changes;
- projection mutation;
- event appends;
- parallel truth, response, caveat, selection, or integrity systems.

# Files Inspected

Required files inspected:

- `docs/response_characterization.md`
- `docs/response_vocabulary.md`
- `docs/response_reconciliation.md`
- `docs/response_caveat_characterization.md`
- `docs/response_caveat_vocabulary.md`
- `docs/selection_rationale_characterization.md`
- `docs/selection_rationale_vocabulary.md`
- `docs/selection_rationale_reconciliation.md`
- `docs/selection_rationale_summary_characterization.md`
- `docs/backlog_and_status_reconciliation.md`
- `docs/reasoning_roadmap.md`
- `docs/knowledge_acquisition_status.md`
- `docs/knowledge_acquisition_and_selection.md`
- `docs/knowledge_classification_vocabulary.md`
- `docs/knowledge_lifecycle_reconciliation.md`

Additional roadmap, backlog, handoff, status, architecture, future-work, audit, reconciliation, and frontier-planning documents inspected:

- `docs/architecture.md`
- `docs/architecture_principles.md`
- `docs/architectural_findings_characterization.md`
- `docs/canonical_documentation_reconciliation.md`
- `docs/context_composition_reconciliation.md`
- `docs/context_composition_vocabulary.md`
- `docs/documentation_architecture_audit.md`
- `docs/explainability_audit.md`
- `docs/explainability_contract_characterization.md`
- `docs/explainability_inventory_audit.md`
- `docs/explainability_reconciliation.md`
- `docs/explanation_contract_vocabulary.md`
- `docs/knowledge_maintenance_reconciliation.md`
- `docs/local_observation_roadmap_audit.md`
- `docs/local_observation_roadmap_reconciliation.md`
- `docs/projection_integrity_drilldown_characterization.md`
- `docs/projection_integrity_summary_characterization.md`
- `docs/promotion_backlog_review.md`
- `docs/roadmap_and_methodology_reconciliation.md`
- `docs/roadmap_reconciliation.md`
- `docs/self_observation_reconciliation.md`
- `docs/why_not_explanation_characterization.md`
- `docs/why_not_vocabulary.md`

Discovery commands used:

- `rg --files docs`
- `rg -n "Recommended outcome|Recommended|not justified|not.*justified|complete|stable|pause|future|Users|Groups|Packages|Systemd|Observation|Engine|Implemented|Partially|Architecturally|Vocabulary|Reconciled|Characterized|Knowledge Acquisition|Knowledge Integrity|Knowledge Selection|Response Caveat|Caveat" docs/*.md docs/audit/*.md`

# Architectural Status

| Concern | Classification | Evidence-supported finding |
| --- | --- | --- |
| Knowledge Acquisition | **Implemented / Partially Complete / Architecturally Stable** | The acquisition pipeline is established as Observation → Evidence → Fact → Projection. Several local observation slices are implemented, and the remaining work is concrete expansion rather than architectural uncertainty. |
| Knowledge Integrity | **Reconciled / Implemented / Architecturally Stable** | Integrity is established as a read-only projected knowledge concern covering support, conflicts, contradictions, staleness, graph issues, confidence, verification limits, and disclosure. Summary and navigation surfaces exist without creating an `IntegrityEngine`. |
| Knowledge Selection | **Reconciled / Vocabulary Established / Architecturally Stable** | Context Composition and Selection Rationale have characterization, vocabulary, and reconciliation coverage. Selection Rationale Summary implementation was explicitly rejected as not justified. |
| Response | **Reconciled / Vocabulary Established / Partially Complete / Architecturally Stable** | Response is a distributed communication concern across Runtime envelopes, CLI output, explanations, integrity summaries, capability inventories, state/context views, contradictions, evidence, confidence, and issue outputs. Response is partially reconciled because caveat and cross-surface composition language remains fragmented, but implementation is not justified. |
| Response Caveats | **Characterized / Vocabulary Established / Architecturally Stable For Now** | Caveat sources and signals are real and distributed. Vocabulary now exists. Additional caveat implementation is not justified; more caveat audits should pause unless a concrete operator question appears. |

## Knowledge Acquisition

Knowledge Acquisition is the most concrete remaining capability frontier. `docs/knowledge_acquisition_status.md` lists implemented local observation slices including Identity, Mount, Kernel / CPU / Memory, Local Network, Storage Topology, Listening Port, and Local Host observations. It also lists planned slices such as Users, Groups, Package, Systemd, Schedule, Certificate, Process Marker, and Container Marker observations.

Status: **Implemented and Partially Complete**. Architecturally stable, but capability growth remains valuable.

## Knowledge Integrity

Knowledge Integrity has been reconciled as the preferred term for the concern previously explored as maintenance. The current concern is read-only and asks whether projected knowledge can safely be relied on. Existing structures already include fact support, fact conflicts, contradictions, staleness, graph validation, confidence, capability verification status, and explanation exposure.

Status: **Reconciled, Implemented, and Architecturally Stable**. Additional implementation is not justified by status alone.

## Knowledge Selection

Knowledge Selection is now well-covered. Context Composition vocabulary defines selection, relevance, priority, budgets, and ordering boundaries. Selection Rationale characterization, vocabulary, reconciliation, and summary characterization establish that rationale information exists and is distributed. The summary characterization rejects new summary/inventory/navigation/read-model/runtime implementation.

Status: **Reconciled and Architecturally Stable**. Future work should be documentation maintenance unless new evidence appears.

## Response

Response has characterization, vocabulary, and reconciliation. The current conclusion is that Response exists as a distributed concern and is partially reconciled. Existing response behavior and communication surfaces are sufficient to answer many operator questions. The remaining gaps are vocabulary/composition/caveat consistency gaps, not missing response engines or runtime paths.

Status: **Reconciled, Vocabulary Established, and Partially Complete**. Architecturally stable enough to avoid implementation work.

## Response Caveats

Response Caveat Characterization and Response Caveat Vocabulary establish a useful caveat language. Caveats are communicated limitations, qualifications, warnings, uncertainty markers, status qualifiers, or non-guarantees attached to existing knowledge surfaces. They must not become a parallel truth system.

Status: **Vocabulary Established and Stable For Now**. Caveat audit work should pause unless a concrete unanswered operator question emerges.

# Completed Audit Chains

| Audit chain | Status | Resolution |
| --- | --- | --- |
| Explainability | **Resolved enough for now** | Audit, inventory audit, contract characterization, reconciliation, and Explanation Contract Vocabulary established explanation language and boundaries. No `ExplainabilityEngine` is justified. |
| Context Composition | **Resolved enough for now** | Reconciliation and Vocabulary v1 established context composition language, ownership, selection, relevance, priority, budgets, and non-goals. No `ContextEngine` is justified. |
| Projection Integrity Summary / Navigation | **Resolved enough for now** | Summary and drilldown/navigation characterizations established read-only integrity visibility. No `IntegrityEngine`, projection mutation, or truth repair is justified. |
| Selection Rationale | **Complete** | Characterization, Vocabulary v1, Reconciliation, and Summary Characterization establish distributed rationale and reject summary implementation. |
| Response | **Complete enough for current architecture** | Characterization, Vocabulary v1, and Reconciliation establish Response as distributed and partially reconciled. No `ResponseEngine`, universal formatter, Runtime integration, or ToolExecutor integration is justified. |
| Response Caveats | **Complete enough for now** | Characterization and Vocabulary establish caveat language. Additional caveat-specific audit chains are not currently justified. |
| Backlog and Status Reconciliation | **Complete for Selection Rationale handoff** | Selection Rationale is no longer a generic implementation backlog item; Response was identified as least-audited before Response docs were subsequently added. |
| Knowledge Lifecycle / Knowledge Integrity | **Resolved enough for now** | Lifecycle framing establishes Acquisition → Integrity → Selection → Response; Integrity is preferred over Maintenance. |

## Chains With Meaningful Unanswered Questions

The remaining meaningful questions are not broad architecture-audit questions. They are bounded future capability or documentation questions:

- Which acquisition slice should be implemented next?
- How should completed audit chains be cross-linked to prevent rediscovery?
- Do operators have a concrete recurring question about caveat grouping that existing surfaces and vocabulary cannot answer?
- Do future observation slices require new invariants after implementation?

# Major Architectural Findings

1. **Behavior often already exists before vocabulary.** Response, selection rationale, caveats, integrity signals, explanations, and context composition were already present across distributed surfaces.
2. **Vocabulary was the recurring gap.** Explanation Contract, Context Composition, Selection Rationale, Response, and Response Caveat vocabularies reduced ambiguity without requiring behavior changes.
3. **Ownership should remain local to source semantics.** Integrity signals, confidence, contradictions, capability verification, evidence, state, context, explanations, and response envelopes should keep their existing owners.
4. **Composition is useful but risky when centralized.** Cross-surface summaries can improve discoverability, but central engines or universal formatters risk duplicating local semantics.
5. **Implementation is often not justified by audit findings.** Selection Rationale Summary, Response implementation, caveat implementation, and engine creation were not supported by evidence.
6. **The lifecycle framing is now stable.** Acquisition creates evidence-backed projected knowledge; Integrity characterizes reliability signals; Selection chooses relevant projected knowledge; Response communicates selected knowledge and limitations.

# Negative Findings Worth Preserving

These findings should remain architectural memory because they prevent repeated rediscovery:

- **Selection Rationale Summary implementation is not justified.** Existing rationale surfaces answer most concrete questions; remaining aggregate questions would require new classifications, histories, inventories, or read models without demonstrated need.
- **Selection implementation is not justified.** Selection is already distributed across ContextComposer, ContextBudget, ordering helpers, DecisionContextView, State, Evidence Graph, Confidence, Contradictions, Capability Inventory, stale views, and explanations.
- **Response implementation is not justified.** Response behavior exists across Runtime response envelopes, CLI output, explanations, integrity summaries, capability inventories, state/context views, evidence, contradictions, confidence, and issue outputs.
- **Caveat implementation is not justified.** Caveat signals already exist in source surfaces; a universal caveat layer would duplicate semantics.
- **Engine creation is repeatedly rejected.** `ResponseEngine`, `SelectionEngine`, `IntegrityEngine`, `ExplainabilityEngine`, `ReasoningEngine`, `ContextEngine`, planners, workflow engines, universal formatters, and universal caveat layers are traps unless future evidence proves a specific unmet need.
- **Runtime integration is not a default solution.** Runtime owns routing and envelopes, not all selection, integrity, caveat, explanation, or response composition semantics.
- **ToolExecutor integration is not a default solution.** ToolExecutor owns registered-operation execution, not general verification, response composition, caveat generation, or truth selection.
- **Parallel truth systems must be avoided.** Caveats, response composition, rationale, and integrity visibility must not create alternative fact stores, hidden trust scores, automatic truth arbitration, contradiction repair, or projection mutation.

# Open Architectural Questions

Only evidence-supported open questions are listed here.

| Question | Classification | Why it remains open |
| --- | --- | --- |
| Which planned acquisition slice should come next: Users, Groups, Packages, Systemd, Schedule, Certificate, Process Marker, or Container Marker? | **Future capability concern / major** | Acquisition status and local observation roadmap preserve multiple meaningful candidates. Prioritization now matters more than more abstract audit. |
| How should completed audit chains be made discoverable across roadmap/status/handoff docs? | **Documentation concern / minor** | Many audit chains are complete, but future-work sections and status docs can still drift or duplicate old questions. |
| Do operators need caveat aggregation beyond vocabulary and per-surface caveat signals? | **Future investigation / minor** | Caveat vocabulary lists possible reconciliation, communication, aggregation, inventory, and surface-matrix docs, but no concrete unmet operator question currently justifies continuing. |
| Should future observation invariants become executable after new slices land? | **Documentation/test concern / minor** | Local observation roadmap lists invariants to consider when corresponding observations are implemented. They should not be implemented before the slices exist. |
| Is repository self-observation still a later acquisition candidate? | **Future capability concern / minor-to-major depending on roadmap** | Roadmap material treats repository observation as useful source material but later than safer local observation slices. |

# Response Caveat Status Assessment

Response Caveat work is **complete enough for now**.

Evidence:

- Response Caveat Characterization found that caveat information already exists but is scattered across integrity, evidence, capability, temporal, confidence, observation, selection, response, graph, and rationale surfaces.
- Response Caveat Vocabulary defines caveat, caveat source, signal, surface, producer, consumer, category, status, scope, limitation, qualification, uncertainty, warning, non-guarantee, and related non-goals.
- Both documents reject caveat implementation, caveat engines, universal caveat layers, Runtime integration, ToolExecutor integration, projection mutation, event appends, and parallel caveat systems.

Assessment:

- Additional caveat audits are **not currently justified** if they only subdivide vocabulary, create surface matrices, or seek universal aggregation without a concrete operator question.
- Caveat work should be **paused** as an active audit chain.
- Caveat findings should be **preserved** as architectural knowledge and used as guardrails for future Response, Selection, and Integrity documentation.

Future caveat work should restart only if maintainers identify a recurring question such as: "Given this answer, which caveats from support, contradiction, staleness, verification, and selection materially limit operator action, and where are they sourced?" Even then, the first step should be documentation-only source mapping, not implementation.

# Acquisition Frontier Assessment

Acquisition remains the highest-value frontier because it adds new facts while staying within established architecture.

## Still Meaningful Candidates

| Candidate | Meaningfulness | Fit |
| --- | --- | --- |
| Users Observation | **High** | Adds local identity/configuration facts from `/etc/passwd` or safe standard-library sources while avoiding NSS/network lookups and authentication claims. |
| Groups Observation | **High** | Complements Users with local group/membership configuration from `/etc/group` or safe standard-library sources. |
| Package Observation | **High** | Adds software inventory value if limited to readable package database files and identity/version facts; must avoid package-manager execution. |
| Systemd Observation | **High** | Adds service/unit inventory value if limited to read-only unit definitions/state and no `systemctl` execution or service health claims. |
| Schedule Observation | **Medium** | Useful for automation inventory; must avoid job-success inference and sensitive crontab overreach. |
| Certificate Observation | **Medium** | Useful for trust/configuration inventory; must avoid TLS/network validation and private-key exposure. |
| Process Marker Observation | **Medium** | Useful for state markers; must avoid sensitive command lines, broad process inspection, and management claims. |
| Container Marker Observation | **Medium** | Useful for local runtime-context markers; must avoid Docker/containerd/Podman/Kubernetes APIs and lifecycle claims. |
| Repository Observation Source | **Medium / Later** | Potentially useful for self-observation and drift detection, but should follow safer local observation slices unless explicitly prioritized. |

## Highest-Value Near-Term Candidates

1. **Users Observation** and **Groups Observation**: strong architecture fit, locally bounded, identity/configuration-oriented, and natural next steps after Identity Observation.
2. **Package Observation**: high operator value, but requires stricter privacy and source parsing boundaries.
3. **Systemd Observation**: high operator value, but must preserve the boundary between unit inventory, service state, service health, and management authority.

## Best Alignment With Current Architecture Maturity

The best-aligned next work is a narrow acquisition slice that:

- uses read-only local evidence;
- records observations through the existing observation ingestion path;
- emits bounded evidence-backed facts;
- avoids execution, network probing, provider calls, Runtime routing, ToolExecutor integration, health inference, ownership inference, and mutation;
- preserves caveats and limitations through existing Integrity, Selection, and Response surfaces.

Users or Groups Observation best matches these constraints.

# Backlog Prioritization Recommendations

Recommended backlog organization:

## Architecture Stable

Items that should be treated as stable architectural findings, not active implementation backlog:

- Explanation Contract Vocabulary and explainability reconciliation;
- Context Composition reconciliation and vocabulary;
- Projection Integrity Summary and Navigation characterization;
- Selection Rationale characterization, vocabulary, reconciliation, and summary characterization;
- Response characterization, vocabulary, and reconciliation;
- Response Caveat characterization and vocabulary;
- Knowledge Lifecycle and Knowledge Integrity reconciliation.

## Documentation Maintenance

Low-risk maintenance items:

- cross-link completed audit chains;
- update roadmap/status/handoff language to reflect completed sequences;
- add compact audit-sequence status tables;
- preserve negative findings in future architecture-status docs;
- prevent stale future-work sections from implying rejected implementations.

## Knowledge Acquisition

Primary active frontier:

- Users Observation;
- Groups Observation;
- Package Observation;
- Systemd Observation;
- Schedule Observation;
- Certificate Observation;
- Process Marker Observation;
- Container Marker Observation;
- repository observation source design only if explicitly prioritized.

## Capability Growth

Secondary frontier after acquisition slices or where capability boundaries need clarification:

- capability extension methodology maintenance;
- verification-status interpretation;
- checked-in `verify_*` operation semantics;
- provider recommendation and handoff boundaries.

## Future Investigation

Use only for evidence-supported questions:

- caveat aggregation needs;
- repository self-observation;
- future executable invariants after observations land;
- cross-run selection/rationale analytics if operators ask for it.

# Documentation Maintenance Opportunities

Low-risk improvements that should not become large implementation work:

1. Add a compact architecture-status table to a central handoff/status document.
2. Add cross-links from `docs/reasoning_roadmap.md` to completed Response and Response Caveat documents.
3. Add a small audit sequence index covering Explainability, Context Composition, Projection Integrity, Selection Rationale, Response, Response Caveats, and Knowledge Lifecycle.
4. Update stale wording that describes Selection Rationale, Response, or Caveats as generic future implementation work.
5. Preserve negative findings in future roadmap refreshes so rejected engines are not repeatedly reconsidered.
6. Cross-link acquisition candidates from `docs/knowledge_acquisition_status.md` and `docs/local_observation_roadmap_reconciliation.md`.
7. Add handoff language saying that additional architecture audits require a concrete unanswered operator question.

# Rejection Criteria For New Audit Chains

Do **not** start additional audit chains when any of the following conditions hold:

- no concrete unanswered operator question is identified;
- no ownership ambiguity remains;
- no composition ambiguity remains;
- no source semantics are unclear;
- the proposed work only expands vocabulary without changing understanding;
- the proposed work only recursively subdivides an already-characterized concern;
- existing surfaces already answer the question;
- the expected output is another summary/inventory/navigation layer without evidence of operator need;
- the work would duplicate existing Integrity, Selection, Response, Explainability, Context, Capability, Evidence, Confidence, Contradiction, or State surfaces;
- the work requires a new engine as a default solution;
- the work requires Runtime or ToolExecutor integration by default;
- the work implies projection mutation, event appends, truth arbitration, provider calls, execution, verification, refresh, repair, planning, or workflow orchestration;
- the work creates a parallel truth, response, caveat, selection, explanation, integrity, or context system.

Start a new audit chain only when:

- a concrete operator question is important and recurring;
- existing documents and surfaces cannot answer it;
- the uncertainty is about architecture, ownership, or composition rather than wording alone;
- the expected result can preserve existing source ownership and non-goals;
- documentation-only analysis is the smallest safe first step.

# Recommended Next Frontier

Recommended next frontier: **C. Knowledge Acquisition expansion**.

## Why Not A. Additional architecture audits?

Additional audits are now lower value. Recent audit chains repeatedly converged on the same pattern: behavior exists, vocabulary was missing, ownership needed clarification, composition was fragmented, and implementation was not justified. Continuing to recursively audit caveats, response subcategories, or rationale subcategories risks diminishing returns unless a concrete operator question appears.

## Why Not B. Documentation maintenance as the primary frontier?

Documentation maintenance is useful and should happen opportunistically, but it should not be the main frontier. The repository already has enough documentation to preserve the current architecture. Maintenance should support handoff and prevent drift, while active roadmap energy returns to useful knowledge growth.

## Why C. Knowledge Acquisition expansion?

Acquisition expansion is the best fit because:

- the pipeline is architecturally stable;
- the backlog contains concrete candidates;
- planned candidates add new operator value;
- the work can remain read-only, evidence-backed, and local;
- it exercises established vocabulary and boundaries rather than creating new conceptual layers;
- it avoids Runtime, ToolExecutor, EventLedger ownership, ProjectionStore ownership, provider, route, adapter, schema, engine, and projection mutation risks.

Best first candidates: **Users Observation** or **Groups Observation**, followed by **Package Observation** or **Systemd Observation** if maintainers want higher-value but higher-boundary-risk inventory.

## Why Not D. Runtime implementation?

Runtime implementation is not supported by this audit. Runtime is already canonical and owns routing/envelopes. The unresolved questions are not runtime-routing questions. Adding Runtime behavior would violate the repeated finding that documentation, vocabulary, and acquisition expansion are safer than central engines, universal response systems, or execution-linked caveat/selection behavior.

# Non-Goals

This document does not:

- implement observations;
- implement caveats;
- implement summaries;
- implement inventories;
- implement navigation;
- implement routes;
- implement adapters;
- implement schema classes;
- modify Runtime;
- modify ToolExecutor;
- modify EventLedger ownership;
- modify ProjectionStore ownership;
- mutate projections;
- append events;
- add provider behavior;
- add execution behavior;
- add read models;
- add engines;
- create parallel truth systems;
- create parallel response systems;
- create parallel caveat systems;
- start a new audit chain.

# Conclusion

Seed's architecture documentation has reached a stabilization point for the major lifecycle concerns. Acquisition, Integrity, Selection, Response, and Caveats now have enough characterization, vocabulary, and reconciliation to avoid defaulting to engines, Runtime integration, ToolExecutor integration, or parallel truth systems.

The architectural status is stable enough to pause recursive documentation audits. Caveat work should be preserved but paused. Selection Rationale should remain completed and non-implemented. Response should remain distributed and documentation-guided. Integrity should remain read-only over projected knowledge.

The next frontier should be **Knowledge Acquisition expansion**, preferably through a narrow read-only Users or Groups Observation slice, with documentation maintenance as a supporting activity and Runtime implementation explicitly out of scope.
