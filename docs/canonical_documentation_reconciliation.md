# Canonical Documentation Reconciliation

# Executive Summary

Seed's documentation set is valuable but now contains several document families with different lifecycle roles: active architecture, active methodology, active vocabularies, roadmap/status boards, generated architecture artifacts, audits, reconciliations, characterizations, inventories, and RuntimeLoop-era historical records.

This reconciliation is documentation-only. It does not move, delete, rename, archive, or rewrite any existing document, and it does not change Runtime, ToolExecutor, EventLedger, ProjectionStore, execution behavior, orchestration, provider integrations, or observation implementation.

The conservative finding is:

- The active canonical set remains the one identified by `docs/documentation_architecture_audit.md`: `README.md`, `docs/architecture.md`, `docs/invariants.md`, `docs/state.md`, `docs/logic_model.md`, `docs/function_blocks.md`, active methodology/vocabulary documents, `docs/knowledge_acquisition_status.md`, `docs/reasoning_roadmap.md`, and generated architecture outputs.
- Several audit and reconciliation documents have successfully served their purpose. Their conclusions have been promoted into canonical architecture, vocabularies, methodology, invariants, the README, or the roadmap. They should remain available as historical evidence until humans perform an explicit archive step.
- Some historical documents still hold unique knowledge that has not been fully promoted, especially detailed fit analysis, inventories, quarantine rationale, exact gap lists, and implementation-specific characterization details. These are not ready to archive without a promotion pass.
- Generated artifacts under `docs/generated/architecture/` should be classified as `GENERATED`; they are authoritative as code-derived outputs but should not be edited manually.
- The main lifecycle risk is duplicate truth: active architecture and historical audits can both look authoritative unless documents are labeled by lifecycle state.

Recommended next step: add a small documentation index or lifecycle register that labels each document as canonical, generated, roadmap/status, historical, or archive candidate before moving or archiving anything.


## Document Classification Table

| Document | Classification | Rationale |
| --- | --- | --- |
| `README.md` | KEEP | Active top-level product thesis, knowledge-first framing, document map, and runtime architecture summary. |
| `docs/architecture.md` | KEEP | Active canonical ownership and component-boundary summary. |
| `docs/invariants.md` | KEEP | Active test-backed architecture invariant source. |
| `docs/state.md` | KEEP | Active projected-state, state-view, evidence-graph, contradiction, and confidence semantics. |
| `docs/logic_model.md` | KEEP | Active logic-layer model and architecture drift guidance. |
| `docs/function_blocks.md` | KEEP | Active bridge between architectural functions and implementation areas. |
| `docs/architecture_principles.md` | KEEP | Active secondary architecture direction; overlaps with canonical docs but remains useful. |
| `docs/capability_extension_methodology.md` | KEEP | Active process for growing capabilities safely from evidence-backed knowledge. |
| `docs/capability_verification_vocabulary.md` | KEEP | Active vocabulary for capability verification states and boundaries. |
| `docs/explanation_contract_vocabulary.md` | KEEP | Active vocabulary for read-only explanations and explanation fields. |
| `docs/knowledge_classification_vocabulary.md` | KEEP | Active vocabulary for knowledge classes. |
| `docs/knowledge_acquisition_status.md` | KEEP | Active status board for observation/knowledge acquisition slices. |
| `docs/reasoning_roadmap.md` | KEEP | Active reasoning roadmap. |
| `docs/rule_inventory.md` | KEEP | Active inventory of deterministic rules and catalogs. |
| `docs/codex_prompt_protocol.md` | KEEP | Active protocol for Seed work prompts; documentation-only guardrail against architecture drift. |
| `docs/generated/architecture/architecture_graph.json` | GENERATED | Generated architecture graph; do not edit manually. |
| `docs/generated/architecture/runtime_ownership.dot` | GENERATED | Generated DOT ownership graph; do not edit manually. |
| `docs/generated/architecture/runtime_ownership.mmd` | GENERATED | Generated Mermaid ownership graph; do not edit manually. |
| `docs/architecture_visualization_phase1.md` | PROMOTE THEN ARCHIVE | Design record for generated architecture infrastructure; promote durable generated-artifact lifecycle rules first. |
| `docs/documentation_architecture_audit.md` | PROMOTE THEN ARCHIVE | Its canonical-set and lifecycle findings remain active until represented in a lifecycle index/register. |
| `docs/availability_vocabulary_audit.md` | PROMOTE THEN ARCHIVE | Mostly promoted, but confirm availability/reachability/local-observability vocabulary completeness. |
| `docs/capability_verification_audit.md` | PROMOTE THEN ARCHIVE | Mostly promoted into vocabulary/invariants; confirm no unique semantic inventory remains. |
| `docs/capability_verification_fit_audit.md` | PROMOTE THEN ARCHIVE | Still holds detailed verification model-fit rationale. |
| `docs/capability_verification_reconciliation.md` | PROMOTE THEN ARCHIVE | Decisions mostly promoted; archive only after final gap check. |
| `docs/contradiction_handling_audit.md` | PROMOTE THEN ARCHIVE | Still holds nuanced contradiction behavior and gaps. |
| `docs/temporal_reasoning_audit.md` | PROMOTE THEN ARCHIVE | Still holds nuanced temporal/staleness/projection behavior. |
| `docs/self_observation_audit.md` | PROMOTE THEN ARCHIVE | Still holds generated-architecture/self-observation inventory and roadmap detail. |
| `docs/explainability_audit.md` | PROMOTE THEN ARCHIVE | Mostly promoted; confirm no unique gaps before archive. |
| `docs/explainability_inventory_audit.md` | PROMOTE THEN ARCHIVE | Exact explanation-surface inventory should be mined first. |
| `docs/explainability_contract_characterization.md` | PROMOTE THEN ARCHIVE | Mostly promoted into vocabulary; keep until behavior gaps are tracked elsewhere. |
| `docs/explainability_reconciliation.md` | PROMOTE THEN ARCHIVE | Mostly absorbed by explanation vocabulary; verify remaining roadmap gaps. |
| `docs/local_network_observation_audit.md` | PROMOTE THEN ARCHIVE | Local read-only source constraints may still need promotion. |
| `docs/local_observation_roadmap_audit.md` | PROMOTE THEN ARCHIVE | Mostly promoted to knowledge status; confirm planned-slice constraints. |
| `docs/local_observation_roadmap_reconciliation.md` | PROMOTE THEN ARCHIVE | Mostly promoted to knowledge status; archive after confirmation. |
| `docs/roadmap_reconciliation.md` | PROMOTE THEN ARCHIVE | Matrix should be checked against active reasoning roadmap before archive. |
| `docs/tool_execution_ownership_audit.md` | PROMOTE THEN ARCHIVE | Ownership conclusion is promoted; archive after confirmation. |
| `docs/pending_action_lifecycle_inventory.md` | PROMOTE THEN ARCHIVE | May contain unique pending-action lifecycle ownership detail. |
| `docs/policy_pending_action_inventory.md` | PROMOTE THEN ARCHIVE | May contain unique policy/pending-action relationship detail. |
| `docs/recommendation_selection_boundary.md` | PROMOTE THEN ARCHIVE | Contains detailed recommendation-selection boundary decisions not fully canonicalized. |
| `docs/audit/capability_operation_vocabulary_audit.md` | PROMOTE THEN ARCHIVE | Vocabulary conclusions are mostly promoted; confirm completeness. |
| `docs/audit/context_knowledge_consolidation.md` | PROMOTE THEN ARCHIVE | Still holds duplicate-concept and consolidation analysis. |
| `docs/audit/core_mvp_inventory_audit.md` | PROMOTE THEN ARCHIVE | Still holds Core MVP graph and quarantine summary. |
| `docs/audit/planning_execution_artifact_quarantine.md` | PROMOTE THEN ARCHIVE | Quarantine conclusion promoted; archive after final confirmation. |
| `docs/runtime_runtime_loop_responsibility_audit.md` | ARCHIVE | Historical RuntimeLoop duplication audit superseded by canonical Runtime ownership. |
| `docs/runtime_reassessment.md` | ARCHIVE | Historical Runtime vs RuntimeLoop reassessment superseded. |
| `docs/runtime_parity_inventory.md` | ARCHIVE | Historical RuntimeLoop parity inventory. |
| `docs/runtime_loop_thin_runtime_plan.md` | ARCHIVE | Historical RuntimeLoop extraction plan. |
| `docs/capability_ownership_matrix.md` | ARCHIVE | Explicit stale/quarantined RuntimeLoop-era ownership matrix. |
| `docs/ask_question_refuse_inventory.md` | ARCHIVE | Explicit stale/quarantined RuntimeLoop-era inventory. |
| `docs/retry_parse_failure_inventory.md` | ARCHIVE | Historical retry/parse inventory. |
| `docs/state_patch_inventory.md` | ARCHIVE | Historical state-patch inventory with old runtime framing. |

# Canonical Document Review

The canonical review focuses on documents that currently define Seed for contributors.

| Document | Classification | Rationale |
| --- | --- | --- |
| `README.md` | KEEP | Active product thesis and top-level knowledge-first architecture. Mostly current. Contains a document map that still points readers to some audit/reconciliation documents as current reading, so it has minor lifecycle/outdated-framing risk. |
| `docs/architecture.md` | KEEP | Active concise component boundary document. It accurately identifies Runtime as canonical, ToolExecutor as execution owner, EventLedger as historical source of truth, ProjectionStore as projection cache, and RuntimeLoop as deprecated/experimental. |
| `docs/invariants.md` | KEEP | Active test-backed invariant document. It is still central for runtime, projection, execution, capability, observation, and verification constraints. |
| `docs/state.md` | KEEP | Active state/read-model semantics for State Views, Evidence Graph, contradiction detection, and confidence aggregation. No later document fully supersedes it. |
| `docs/logic_model.md` | KEEP | Active logic-layer description. It includes current architecture drift warnings and explicitly rejects RuntimeLoop/planning artifacts as current-core architecture. |
| `docs/function_blocks.md` | KEEP | Active functional decomposition bridging architecture and implementation. It still carries useful ownership structure. |
| `docs/architecture_principles.md` | KEEP | Active secondary principles document. It overlaps with README and architecture, but still captures direction and boundaries. Candidate for future consolidation, not archival. |
| `docs/capability_extension_methodology.md` | KEEP | Active methodology for safe capability growth from gap to narrow fact to observation/evidence/projection. Later work reinforces rather than supersedes it. |
| `docs/capability_verification_vocabulary.md` | KEEP | Active vocabulary. Conclusions from verification audits/reconciliation have been promoted here. |
| `docs/explanation_contract_vocabulary.md` | KEEP | Active explanation vocabulary. It is the promoted target for explainability audit, inventory, characterization, and reconciliation work. |
| `docs/knowledge_classification_vocabulary.md` | KEEP | Active vocabulary separating identity, description, configuration, topology, state, event, policy, capability, availability, temporal, health, recommendation, and execution knowledge. |
| `docs/knowledge_acquisition_status.md` | KEEP | Active status board for observation-slice planning. It should remain mutable and current, not archived. |
| `docs/reasoning_roadmap.md` | KEEP | Active roadmap for reasoning capabilities. It should remain active until replaced by a newer roadmap. |
| `docs/rule_inventory.md` | KEEP | Active inventory of deterministic rules. It is referenced by explanation/roadmap work and is not merely historical. |
| `docs/codex_prompt_protocol.md` | KEEP | Active documentation-only work-prompt protocol that helps prevent Seed architecture drift during future changes. |
| `docs/architecture_visualization_phase1.md` | PROMOTE THEN ARCHIVE | Current design record for generated architecture artifacts. It still contains methodology and generator rationale; promote durable generation policy into a documentation index or generated-artifacts section before archiving. |
| `docs/generated/architecture/architecture_graph.json` | GENERATED | Code-derived architecture graph with an explicit generated/do-not-edit banner. Must remain generated rather than manually edited. |
| `docs/generated/architecture/runtime_ownership.dot` | GENERATED | Code-derived DOT graph with generated/do-not-edit banner. Must remain generated rather than manually edited. |
| `docs/generated/architecture/runtime_ownership.mmd` | GENERATED | Code-derived Mermaid graph with generated/do-not-edit banner. Must remain generated rather than manually edited. |

Findings:

- Current canonical architecture is no longer tool-first. It is knowledge-first: observations, evidence, facts, projected state, explanation, and only then capability resolution or execution.
- RuntimeLoop-era framing is actively quarantined/deprecated in the canonical architecture, but several historical documents still include RuntimeLoop detail and can appear current without lifecycle labels.
- Planner/workflow/action-plan framing is not current-core architecture. Where it appears, it should remain historical unless explicitly reintroduced through canonical architecture.
- Capability-first framing has mostly been corrected: capability resolution is downstream of projected knowledge and does not imply execution, verification, or availability.
- README's document map is useful but may over-promote audit/reconciliation documents by listing them in the current reading order. This is a promotion/planning issue, not an emergency.

# Audit Review

Audit-family documents are mostly historical evidence. Some conclusions are already promoted; some still hold detailed implementation knowledge worth mining before archival.

| Document | Classification | Rationale |
| --- | --- | --- |
| `docs/documentation_architecture_audit.md` | PROMOTE THEN ARCHIVE | Its canonical-set finding is the direct basis for this reconciliation. Promote the lifecycle categories/index recommendation before archiving. |
| `docs/availability_vocabulary_audit.md` | PROMOTE COMPLETE → ARCHIVE CANDIDATE | Core non-implication boundaries appear in README, methodology, invariants, and knowledge status. Keep until humans confirm all vocabulary terms needed for availability/reachability/local observability are promoted. |
| `docs/capability_verification_audit.md` | PROMOTE COMPLETE → ARCHIVE CANDIDATE | Verification boundaries have been promoted into verification vocabulary and invariants. Detailed semantic inventory may remain useful as historical evidence. |
| `docs/capability_verification_fit_audit.md` | PROMOTE THEN ARCHIVE | Contains detailed model-fit analysis for verification as facts/evidence/support/staleness/contradiction. Not all detailed fit rationale appears in canonical docs. |
| `docs/contradiction_handling_audit.md` | PROMOTE THEN ARCHIVE | Current contradiction behavior is partly promoted into state, logic model, and roadmap. Detailed audit findings and test characterization should be promoted or summarized first. |
| `docs/temporal_reasoning_audit.md` | PROMOTE THEN ARCHIVE | Current temporal semantics are partly promoted, but this document still carries detailed timestamp, projection-order, staleness, and expiry characterization. |
| `docs/self_observation_audit.md` | PROMOTE THEN ARCHIVE | Generated architecture/self-observation conclusions are partly active. Still carries broad inventory and roadmap material that should be promoted into generated-artifact lifecycle docs. |
| `docs/explainability_audit.md` | PROMOTE COMPLETE → ARCHIVE CANDIDATE | Main conclusions have converged into explanation vocabulary and reconciliation. Keep until final confirmation that unique gaps are represented. |
| `docs/explainability_inventory_audit.md` | PROMOTE THEN ARCHIVE | Contains exact explanation-producing surface inventory. Promote any unique surface/gap inventory into vocabulary or roadmap before archive. |
| `docs/local_network_observation_audit.md` | PROMOTE THEN ARCHIVE | Local network observation boundaries are partly reflected in knowledge status and methodology. Detailed local-source constraints may need promotion before archive. |
| `docs/local_observation_roadmap_audit.md` | PROMOTE COMPLETE → ARCHIVE CANDIDATE | Observation roadmap conclusions appear in knowledge acquisition status and local observation reconciliation. Archive only after confirming no unique planned-slice constraints remain. |
| `docs/tool_execution_ownership_audit.md` | PROMOTE COMPLETE → ARCHIVE CANDIDATE | Ownership conclusion is promoted into architecture and invariants: ToolExecutor owns execution. Historical RuntimeLoop overlap details are not canonical. |
| `docs/runtime_runtime_loop_responsibility_audit.md` | ARCHIVE | Historical Runtime/RuntimeLoop responsibility duplication audit. Current canonical docs already deprecate RuntimeLoop. |
| `docs/runtime_reassessment.md` | ARCHIVE | Historical Runtime vs RuntimeLoop reassessment. Current architecture supersedes it. |
| `docs/runtime_parity_inventory.md` | ARCHIVE | Historical parity inventory with RuntimeLoop-era assumptions. Useful only as evidence. |
| `docs/runtime_loop_thin_runtime_plan.md` | ARCHIVE | Historical plan for RuntimeLoop extraction. Superseded by canonical Runtime ownership. |
| `docs/capability_ownership_matrix.md` | ARCHIVE | Explicit stale/quarantined RuntimeLoop-era ownership matrix. |
| `docs/ask_question_refuse_inventory.md` | ARCHIVE | Explicit stale/quarantined RuntimeLoop-era inventory. |
| `docs/retry_parse_failure_inventory.md` | ARCHIVE | Historical inventory. Canonical Runtime retry/parse behavior should live in runtime docs/tests if needed. |
| `docs/state_patch_inventory.md` | ARCHIVE | Historical state patch inventory with old Runtime/RuntimeLoop framing. |
| `docs/pending_action_lifecycle_inventory.md` | PROMOTE THEN ARCHIVE | Pending-action lifecycle knowledge may remain useful for ownership docs. Promote durable lifecycle boundaries before archive. |
| `docs/policy_pending_action_inventory.md` | PROMOTE THEN ARCHIVE | Policy/pending-action relationship may carry unique historical lifecycle details. Promote only stable ownership facts. |
| `docs/audit/capability_operation_vocabulary_audit.md` | PROMOTE COMPLETE → ARCHIVE CANDIDATE | Capability/operation vocabulary was promoted into capability verification vocabulary, methodology, architecture, and README. |
| `docs/audit/context_knowledge_consolidation.md` | PROMOTE THEN ARCHIVE | Context/explanation/knowledge consolidation still has useful canonical component mapping and duplicate-concept analysis. |
| `docs/audit/core_mvp_inventory_audit.md` | PROMOTE THEN ARCHIVE | Strong Core MVP inventory and quarantine summary; should be mined for a concise current architecture/index before archive. |
| `docs/audit/planning_execution_artifact_quarantine.md` | PROMOTE COMPLETE → ARCHIVE CANDIDATE | Quarantine conclusion is reflected in invariants/logic model, but the inventory is useful until an archive index exists. |

Audit findings:

- Availability, capability verification, tool execution ownership, capability/operation vocabulary, and planning quarantine audits have largely completed their promotion job.
- Temporal, contradiction, explainability inventory, self-observation, local network observation, and Core MVP audits still hold detailed knowledge that should not be discarded prematurely.
- RuntimeLoop-era audit/inventory records are no longer active architecture and are archive candidates once humans are comfortable preserving them as history.

# Reconciliation Review

Reconciliation documents bridge audits and canonical docs. Some still carry active decisions; others have been absorbed.

| Document | Classification | Rationale |
| --- | --- | --- |
| `docs/roadmap_reconciliation.md` | PROMOTE THEN ARCHIVE | Contains implemented/partial/missing reasoning capability matrix. Active roadmap information should live in `docs/reasoning_roadmap.md`; detailed reconciliation evidence can become historical. |
| `docs/capability_verification_reconciliation.md` | PROMOTE COMPLETE → ARCHIVE CANDIDATE | Decision to model verification as inventory-only/no execution has been promoted into vocabulary, invariants, methodology, and README principles. |
| `docs/explainability_reconciliation.md` | PROMOTE COMPLETE → ARCHIVE CANDIDATE | Converged into `docs/explanation_contract_vocabulary.md`; keep only until any remaining gap list is represented in roadmap/status docs. |
| `docs/local_observation_roadmap_reconciliation.md` | PROMOTE COMPLETE → ARCHIVE CANDIDATE | Local observation roadmap conclusions are reflected in `docs/knowledge_acquisition_status.md`. |
| `docs/documentation_architecture_audit.md` | PROMOTE THEN ARCHIVE | Functions like a reconciliation of documentation architecture. Its lifecycle proposal remains active until this reconciliation/index is adopted. |
| `docs/audit/context_knowledge_consolidation.md` | PROMOTE THEN ARCHIVE | Reconciliation-style document that still carries duplicate-concept analysis and consolidation sequencing. |

Reconciliation findings:

- Active architectural decisions from capability verification and explainability reconciliations have mostly been absorbed into vocabularies and invariants.
- Roadmap reconciliation is more historical now that `docs/reasoning_roadmap.md` exists, but it still carries useful matrix detail.
- Documentation architecture audit remains active only until a lifecycle register/index is created.

# Characterization Review

Characterization documents are useful as evidence of current behavior, but they should not compete with canonical docs.

| Document | Classification | Rationale |
| --- | --- | --- |
| `docs/explainability_contract_characterization.md` | PROMOTE COMPLETE → ARCHIVE CANDIDATE | Characterization informed the explanation vocabulary. Keep as historical evidence unless exact behavior gaps are not yet tracked elsewhere. |
| `docs/temporal_reasoning_audit.md` | PROMOTE THEN ARCHIVE | Also serves as temporal characterization. Detailed current-state/staleness behavior remains useful and should be summarized canonically before archive. |
| `docs/contradiction_handling_audit.md` | PROMOTE THEN ARCHIVE | Also serves as contradiction characterization. Promote stable contradiction semantics and remaining gaps first. |
| `docs/capability_verification_fit_audit.md` | PROMOTE THEN ARCHIVE | Also serves as model-fit characterization for future verification. Promote stable fit constraints before archive. |

Characterization findings:

- Explainability characterization has largely become historical evidence after vocabulary promotion.
- Temporal and contradiction characterizations remain useful references because they describe nuanced behavior that is easy to oversimplify.
- Characterizations should be cited as evidence during promotions but should not remain the primary source of truth for current architecture.

# Promotion Inventory

## Promotion Table

| Source | Target | Information | Status |
| --- | --- | --- | --- |
| `docs/documentation_architecture_audit.md` | future documentation index/lifecycle register | Canonical/generated/status/historical/archive categories and smallest canonical reading set. | Needs promotion |
| `docs/availability_vocabulary_audit.md` | `docs/knowledge_classification_vocabulary.md`, `docs/capability_extension_methodology.md`, `docs/invariants.md` | Availability vs reachability vs observability vs provider/local configuration boundaries. | Mostly promoted; verify completeness |
| `docs/capability_verification_audit.md` | `docs/capability_verification_vocabulary.md`, `docs/invariants.md` | Requested/known/candidate/provider-recommended capabilities are unverified by default. | Promotion complete |
| `docs/capability_verification_fit_audit.md` | `docs/capability_verification_vocabulary.md`, `docs/reasoning_roadmap.md` | Fact/evidence/support/staleness/contradiction fit constraints for future verification. | Needs selective promotion |
| `docs/capability_verification_reconciliation.md` | `docs/capability_verification_vocabulary.md`, `docs/invariants.md`, `README.md` | Inventory-only verification foundation; no runtime/tool/provider/shell verification execution. | Promotion complete |
| `docs/explainability_audit.md` | `docs/explanation_contract_vocabulary.md` | Explanation surfaces and read-only explanation boundary. | Promotion complete |
| `docs/explainability_inventory_audit.md` | `docs/explanation_contract_vocabulary.md`, `docs/reasoning_roadmap.md` | Exact explanation-producing surfaces and missing unified contract gaps. | Needs selective promotion |
| `docs/explainability_contract_characterization.md` | `docs/explanation_contract_vocabulary.md` | Explanation contract fields/statuses/extensions. | Promotion complete |
| `docs/explainability_reconciliation.md` | `docs/explanation_contract_vocabulary.md`, `docs/reasoning_roadmap.md` | Converged explanation capabilities and remaining gaps. | Mostly promoted; verify gaps |
| `docs/local_network_observation_audit.md` | `docs/knowledge_acquisition_status.md`, `docs/capability_extension_methodology.md` | Local network observation must be read-only and must not imply reachability/availability. | Mostly promoted; verify local-source details |
| `docs/local_observation_roadmap_audit.md` | `docs/knowledge_acquisition_status.md` | Planned local observation slices and deferred inference/provider/execution boundaries. | Promotion complete |
| `docs/local_observation_roadmap_reconciliation.md` | `docs/knowledge_acquisition_status.md` | Roadmap reconciliation for local observation work. | Promotion complete |
| `docs/roadmap_reconciliation.md` | `docs/reasoning_roadmap.md` | Implemented/partial/missing reasoning capabilities matrix. | Needs selective promotion/confirmation |
| `docs/contradiction_handling_audit.md` | `docs/state.md`, `docs/logic_model.md`, `docs/reasoning_roadmap.md` | Conservative contradiction semantics and unresolved gaps. | Needs selective promotion |
| `docs/temporal_reasoning_audit.md` | `docs/state.md`, `docs/logic_model.md`, `docs/reasoning_roadmap.md` | Event ordering, current-state projection, measurement/latest-current, expiry/staleness semantics. | Needs selective promotion |
| `docs/self_observation_audit.md` | future generated-artifacts lifecycle/index, `docs/architecture_visualization_phase1.md` | Self-observation assets, generated architecture graph, ownership metadata, documentation inventory. | Needs selective promotion |
| `docs/tool_execution_ownership_audit.md` | `docs/architecture.md`, `docs/invariants.md` | ToolExecutor owns registered operation execution; Runtime/RuntimeLoop overlap is historical. | Promotion complete |
| `docs/audit/capability_operation_vocabulary_audit.md` | `docs/capability_verification_vocabulary.md`, `docs/capability_extension_methodology.md`, `README.md` | Capability vs registered operation vs provider/handoff vs tool need vocabulary. | Promotion complete |
| `docs/audit/context_knowledge_consolidation.md` | `docs/architecture.md`, `docs/state.md`, `docs/explanation_contract_vocabulary.md` | Canonical component map and duplicate/overlapping concept cleanup. | Needs selective promotion |
| `docs/audit/core_mvp_inventory_audit.md` | `docs/architecture.md`, `docs/reasoning_roadmap.md`, future lifecycle index | Core MVP graph, runtime-reachable/read-only paths, quarantined artifacts. | Needs selective promotion |
| `docs/audit/planning_execution_artifact_quarantine.md` | `docs/invariants.md`, `docs/logic_model.md` | Planning/execution artifacts are quarantined and not current-core architecture. | Promotion complete |
| `docs/architecture_visualization_phase1.md` | future generated-artifacts lifecycle/index | Generated architecture policy and generation pipeline rationale. | Needs promotion |
| `docs/pending_action_lifecycle_inventory.md` | `docs/architecture.md` or future pending-action lifecycle doc | Stable pending-action ownership/lifecycle facts only. | Needs review |
| `docs/policy_pending_action_inventory.md` | `docs/architecture.md` or future policy/pending-action lifecycle doc | Stable policy/pending-action relationship facts only. | Needs review |

# Archive Readiness Analysis

## Archive Readiness Table

| Document | Ready | Why |
| --- | --- | --- |
| `README.md` | Must Remain Active | Top-level product and architecture framing. |
| `docs/architecture.md` | Must Remain Active | Canonical ownership/boundary document. |
| `docs/invariants.md` | Must Remain Active | Test-backed architecture constraints. |
| `docs/state.md` | Must Remain Active | Canonical state/read-model semantics. |
| `docs/logic_model.md` | Must Remain Active | Canonical logic-layer and drift model. |
| `docs/function_blocks.md` | Must Remain Active | Canonical functional decomposition. |
| `docs/architecture_principles.md` | Must Remain Active | Active secondary principles; possible future consolidation. |
| `docs/capability_extension_methodology.md` | Must Remain Active | Active capability-growth methodology. |
| `docs/capability_verification_vocabulary.md` | Must Remain Active | Active vocabulary. |
| `docs/explanation_contract_vocabulary.md` | Must Remain Active | Active vocabulary. |
| `docs/knowledge_classification_vocabulary.md` | Must Remain Active | Active vocabulary. |
| `docs/knowledge_acquisition_status.md` | Must Remain Active | Active status board. |
| `docs/reasoning_roadmap.md` | Must Remain Active | Active roadmap. |
| `docs/rule_inventory.md` | Must Remain Active | Active deterministic-rule inventory. |
| `docs/codex_prompt_protocol.md` | Must Remain Active | Active prompt protocol/guardrail for future Seed work. |
| `docs/generated/architecture/architecture_graph.json` | Generated Artifact | Code-derived; do not edit manually. |
| `docs/generated/architecture/runtime_ownership.dot` | Generated Artifact | Code-derived; do not edit manually. |
| `docs/generated/architecture/runtime_ownership.mmd` | Generated Artifact | Code-derived; do not edit manually. |
| `docs/documentation_architecture_audit.md` | Needs Promotion First | Lifecycle/index recommendation remains active until represented elsewhere. |
| `docs/architecture_visualization_phase1.md` | Needs Promotion First | Generated-artifact lifecycle policy should be promoted before archive. |
| `docs/availability_vocabulary_audit.md` | Ready To Archive after confirmation | Conclusions mostly promoted; confirm no unique terminology remains. |
| `docs/capability_verification_audit.md` | Ready To Archive after confirmation | Conclusions promoted to vocabulary/invariants. |
| `docs/capability_verification_fit_audit.md` | Needs Promotion First | Contains detailed future-model fit constraints. |
| `docs/capability_verification_reconciliation.md` | Ready To Archive after confirmation | Decisions promoted; keep until gap check complete. |
| `docs/contradiction_handling_audit.md` | Needs Promotion First | Nuanced contradiction behavior/gaps still useful. |
| `docs/temporal_reasoning_audit.md` | Needs Promotion First | Nuanced temporal behavior/gaps still useful. |
| `docs/self_observation_audit.md` | Needs Promotion First | Self-observation/generated architecture inventory remains useful. |
| `docs/explainability_audit.md` | Ready To Archive after confirmation | Conclusions promoted to explanation vocabulary. |
| `docs/explainability_inventory_audit.md` | Needs Promotion First | Exact surfaces/gaps should be mined first. |
| `docs/explainability_contract_characterization.md` | Ready To Archive after confirmation | Vocabulary absorbed the contract. |
| `docs/explainability_reconciliation.md` | Ready To Archive after confirmation | Converged decisions promoted; verify gaps. |
| `docs/local_network_observation_audit.md` | Needs Promotion First | Local-source constraints may still be unique. |
| `docs/local_observation_roadmap_audit.md` | Ready To Archive after confirmation | Roadmap conclusions promoted to status board. |
| `docs/local_observation_roadmap_reconciliation.md` | Ready To Archive after confirmation | Reconciled roadmap promoted to status board. |
| `docs/roadmap_reconciliation.md` | Needs Promotion First | Capability matrix should be checked against reasoning roadmap. |
| `docs/tool_execution_ownership_audit.md` | Ready To Archive after confirmation | Ownership conclusions promoted. |
| `docs/runtime_runtime_loop_responsibility_audit.md` | Ready To Archive | Historical RuntimeLoop duplication audit. |
| `docs/runtime_reassessment.md` | Ready To Archive | Historical RuntimeLoop reassessment. |
| `docs/runtime_parity_inventory.md` | Ready To Archive | Historical RuntimeLoop parity inventory. |
| `docs/runtime_loop_thin_runtime_plan.md` | Ready To Archive | Historical RuntimeLoop plan. |
| `docs/capability_ownership_matrix.md` | Ready To Archive | Explicit stale/quarantined matrix. |
| `docs/ask_question_refuse_inventory.md` | Ready To Archive | Explicit stale/quarantined inventory. |
| `docs/retry_parse_failure_inventory.md` | Ready To Archive | Historical retry/parse inventory. |
| `docs/state_patch_inventory.md` | Ready To Archive | Historical state-patch inventory. |
| `docs/pending_action_lifecycle_inventory.md` | Needs Promotion First | May carry unique lifecycle ownership details. |
| `docs/policy_pending_action_inventory.md` | Needs Promotion First | May carry unique policy/pending-action lifecycle details. |
| `docs/recommendation_selection_boundary.md` | Needs Promotion First | Contains detailed recommendation-selection boundary decisions that may not be fully canonical. |
| `docs/audit/capability_operation_vocabulary_audit.md` | Ready To Archive after confirmation | Vocabulary conclusions promoted. |
| `docs/audit/context_knowledge_consolidation.md` | Needs Promotion First | Duplicate-concept analysis still useful. |
| `docs/audit/core_mvp_inventory_audit.md` | Needs Promotion First | Core MVP graph/quarantine summary should be mined. |
| `docs/audit/planning_execution_artifact_quarantine.md` | Ready To Archive after confirmation | Quarantine conclusion promoted. |

# Documentation Lifecycle Proposal

## Canonical

Canonical documents are the current source of truth for architecture, boundaries, methodology, vocabulary, roadmap/status, and test-backed invariants. They should be few, stable, and easy to find.

Rules:

- Canonical documents may be edited manually.
- Canonical documents should avoid duplicating full audit histories.
- Canonical documents should reference historical/audit documents only when the history is needed.
- Canonical documents should be updated when a promoted conclusion changes the current architecture.

Examples: `README.md`, `docs/architecture.md`, `docs/invariants.md`, `docs/state.md`, `docs/logic_model.md`, `docs/function_blocks.md`, active vocabularies, active methodology, `docs/knowledge_acquisition_status.md`, and `docs/reasoning_roadmap.md`.

## Generated

Generated documents are code-derived artifacts that describe architecture or ownership. They are authoritative as generated outputs, not as hand-authored docs.

Rules:

- Generated documents should carry a generated/do-not-edit banner.
- Humans should change the generator or source metadata, not the generated artifact body.
- Generated documents should be regenerated in CI or by a documented command.
- Generated documents can be canonical references, but their lifecycle is separate from hand-authored docs.

Examples: `docs/generated/architecture/architecture_graph.json`, `docs/generated/architecture/runtime_ownership.dot`, and `docs/generated/architecture/runtime_ownership.mmd`.

## Historical

Historical documents are audits, reconciliations, characterizations, inventories, and design records that explain why current architecture exists. They should be preserved but not treated as active truth.

Rules:

- Historical documents should not be required reading for current architecture onboarding.
- Historical documents may contain stale terminology and should be labeled accordingly.
- Before archival, humans should confirm whether unique knowledge has been promoted.
- Historical documents should be cited when a promotion decision needs provenance.

Examples: most audit, reconciliation, characterization, and inventory documents.

## Archive

Archive is the lifecycle state for historical documents whose useful conclusions have been promoted or intentionally left as historical evidence.

Rules:

- Archiving should be a deliberate human step after a promotion inventory.
- Archive candidates should not be moved/deleted/renamed during this reconciliation.
- Archive status means “not active architecture,” not “worthless.”
- Archive decisions should preserve provenance and avoid losing nuanced rationale.

## Movement Between States

A conservative lifecycle flow should be:

```text
Audit / Characterization / Reconciliation
  -> Promotion Inventory
  -> Canonical Update or Explicit No-Promotion Decision
  -> Historical Label
  -> Archive Candidate
  -> Human Archive Action
```

Generated lifecycle should be separate:

```text
Source Code / Ownership Metadata / Generator
  -> Generated Artifact
  -> Regeneration / CI Check
```

This prevents audit accumulation, duplicate truth, competing vocabularies, and stale architecture by making each document's role explicit.

# Risks

- **Outdated framing risk:** RuntimeLoop-era documents (`runtime_*`, `ask_question_refuse_inventory`, `state_patch_inventory`, capability ownership matrix) can still look authoritative if discovered through search.
- **Duplicate truth risk:** README, architecture, architecture principles, roadmap reconciliation, and several audits repeat boundary language. Without lifecycle labels, contributors may not know which source wins.
- **Unique knowledge risk:** Temporal, contradiction, explainability inventory, self-observation, local network observation, pending-action, policy/pending-action, recommendation-selection, and Core MVP inventory documents may contain detailed knowledge not fully promoted.
- **Generated artifact risk:** Files under `docs/generated/architecture/` should probably never be edited manually; doing so would create drift from code-derived ownership metadata.
- **Vocabulary drift risk:** Availability, capability verification, explanation, and knowledge classification vocabularies are now separate. Future audits should promote into one of these rather than create another competing vocabulary unless there is a deliberate new concept.
- **Roadmap drift risk:** `docs/roadmap_reconciliation.md`, `docs/reasoning_roadmap.md`, and `docs/knowledge_acquisition_status.md` can diverge unless one is clearly the active roadmap/status source.
- **Archive timing risk:** Archiving before promotion could lose rationale for conservative non-execution, non-verification, non-availability, and read-only observation boundaries.

# Recommended Next Step

Do not archive, move, rename, delete, or rewrite large documents yet.

Recommended conservative next step:

1. Create a small documentation lifecycle index that lists each document as `canonical`, `generated`, `roadmap/status`, `historical`, or `archive candidate`.
2. Use the promotion table in this reconciliation to run targeted, source-by-source promotion checks.
3. Promote only short durable facts into canonical docs, not whole audit narratives.
4. Label RuntimeLoop-era records as historical/archive candidates so they do not compete with current Runtime architecture.
5. Treat generated architecture artifacts as generated-only and document the regeneration path instead of editing them by hand.
6. After the index and promotion checks, humans can decide whether to move/archive files in a later, separate change.

No runtime behavior, ToolExecutor behavior, observation behavior, orchestration behavior, provider integration, or feature implementation is recommended by this document.
