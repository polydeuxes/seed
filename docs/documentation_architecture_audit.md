# Documentation Architecture Audit

# Executive Summary

Seed's documentation now contains a useful but crowded mix of canonical architecture, generated architecture output, active methodology, vocabularies, status boards, roadmaps, audits, reconciliations, characterizations, inventories, and stale RuntimeLoop-era records.

The smallest documentation architecture that defines Seed today is:

1. `README.md` for the product thesis, knowledge-first framing, and top-level principles.
2. `docs/architecture.md` for the current component boundaries and runtime ownership model.
3. `docs/invariants.md` for test-backed architectural invariants.
4. `docs/state.md` and `docs/logic_model.md` for projected-state, evidence, confidence, contradiction, and logic-model semantics.
5. `docs/function_blocks.md` for the functional decomposition that bridges architecture and implementation.
6. `docs/capability_extension_methodology.md` for the safe process for adding capabilities.
7. Canonical vocabulary documents: `docs/knowledge_classification_vocabulary.md`, `docs/capability_verification_vocabulary.md`, and `docs/explanation_contract_vocabulary.md`.
8. `docs/knowledge_acquisition_status.md` for the active knowledge-acquisition status board.
9. `docs/reasoning_roadmap.md` for the active roadmap.
10. `docs/generated/architecture/*` as generated, code-derived architecture artifacts that are authoritative as generated outputs but must not be edited manually.

Most audit, reconciliation, characterization, and inventory documents should be treated as historical evidence. They remain valuable for tracing why current boundaries exist, but they should not be required reading for contributors trying to understand the current architecture. Several of them already carry explicit stale/quarantined notices and are strong archive candidates.

This audit does not promote content, archive files, rename documents, or change runtime behavior. It inventories and classifies the documentation set, identifies promotion opportunities, proposes an information architecture, and recommends the smallest safe next step: add a documentation index/reconciliation pass that declares canonical, generated, roadmap/status, and archive sections before moving files.

# Documentation Inventory

Inventory scope: `README.md`, root historical markdown files discovered during the audit, all files under `docs/`, and generated architecture files under `docs/generated/architecture/`.

| Document | Category | Status | Authoritative | Archive candidate | Notes |
| --- | --- | --- | --- | --- | --- |
| `README.md` | Canonical | Current | Yes | No | Product definition, core thesis, knowledge-first architecture, and top-level design principles. |
| `01-architecture.md` | Historical Audit | Superseded root architecture draft | No | Yes | Root-level architecture narrative references additional numbered docs that are not present; useful as historical framing only. |
| `09-pseudocode.md` | Historical Audit | Superseded root pseudocode sketch | No | Yes | Implementation sketch, explicitly not production code; should not compete with current docs or code. |
| `docs/architecture.md` | Canonical | Current | Yes | No | Current boundary-oriented component architecture and ownership model. |
| `docs/architecture_principles.md` | Canonical | Current but partially overlapping | Yes, secondary | No | Architecture direction and principles; overlaps with `README.md` and `docs/architecture.md`. Candidate for consolidation into canonical architecture set or index. |
| `docs/architecture_visualization_phase1.md` | Methodology | Current design record | Partially | No | Explains why architecture diagrams are generated and how generation should work. |
| `docs/ask_question_refuse_inventory.md` | Historical Audit | Stale/quarantined | No | Yes | RuntimeLoop-era inventory with explicit stale warning. |
| `docs/audit/capability_operation_vocabulary_audit.md` | Historical Audit | Historical with canonical conclusions | No, except conclusions awaiting promotion | Yes, after promotion review | Audit of capability/operation vocabulary; promote any durable vocabulary deltas before archive. |
| `docs/audit/context_knowledge_consolidation.md` | Historical Reconciliation | Historical reconciliation | No, except conclusions awaiting promotion | Yes, after promotion review | Consolidation audit for context/explanation/knowledge views. |
| `docs/audit/core_mvp_inventory_audit.md` | Historical Audit | Valuable current-context evidence | No, except conclusions awaiting promotion | Partial | Strong historical summary of Core MVP after quarantine; should be mined for canonical boundaries. |
| `docs/audit/planning_execution_artifact_quarantine.md` | Historical Audit | Current quarantine evidence | No, except quarantine conclusions | Partial | Useful until quarantine status is represented in canonical architecture or archive index. |
| `docs/availability_vocabulary_audit.md` | Historical Audit | Historical vocabulary audit | No, except vocabulary awaiting promotion | Yes, after promotion review | Availability terms and non-implication boundaries should be promoted if not already captured. |
| `docs/capability_extension_methodology.md` | Methodology | Current | Yes | No | Active process for extending capabilities safely. |
| `docs/capability_ownership_matrix.md` | Historical Audit | Stale/quarantined | No | Yes | Explicit RuntimeLoop-era stale warning. |
| `docs/capability_verification_audit.md` | Historical Audit | Historical audit | No | Yes, after promotion review | Source material for verification vocabulary and boundaries. |
| `docs/capability_verification_fit_audit.md` | Historical Audit | Historical fit analysis | No | Yes, after promotion review | Explores whether verified capability fits facts/evidence/status models. |
| `docs/capability_verification_reconciliation.md` | Historical Reconciliation | Historical reconciliation | No | Yes, after promotion review | Decision record for verification inventory; canonical outcomes should live in vocabulary/status docs. |
| `docs/capability_verification_vocabulary.md` | Vocabulary | Current | Yes | No | Canonical verification terminology and non-implication boundaries. |
| `docs/codex_prompt_protocol.md` | Methodology | Current contributor/process guidance | Yes, for prompts | No | Prompt protocol, not system architecture; should live under methodology/contributor docs. |
| `docs/contradiction_handling_audit.md` | Historical Audit | Historical audit | No | Yes, after promotion review | Contradiction model audit; durable terms should live in `docs/state.md`/`docs/invariants.md`. |
| `docs/explainability_audit.md` | Historical Audit | Historical audit | No | Yes, after promotion review | Broad explainability surface audit. |
| `docs/explainability_contract_characterization.md` | Characterization | Historical characterization | No | Yes, after promotion review | Characterizes explanation surfaces and contract shape. |
| `docs/explainability_inventory_audit.md` | Historical Audit | Historical audit | No | Yes, after promotion review | Inventory of explanation-producing surfaces. |
| `docs/explainability_reconciliation.md` | Historical Reconciliation | Historical reconciliation | No | Yes, after promotion review | Reconciles explainability docs into contract vocabulary. |
| `docs/explanation_contract_vocabulary.md` | Vocabulary | Current | Yes | No | Canonical explanation-contract vocabulary. |
| `docs/function_blocks.md` | Canonical | Current | Yes | No | Functional decomposition of Seed's architecture. |
| `docs/generated/architecture/architecture_graph.json` | Generated | Current if regenerated from code | Yes, as generated source artifact | No | Machine-readable generated architecture graph; edit generator/source metadata instead of this file. |
| `docs/generated/architecture/runtime_ownership.dot` | Generated | Current if regenerated from code | Yes, as generated render artifact | No | Generated Graphviz DOT ownership graph; do not edit manually. |
| `docs/generated/architecture/runtime_ownership.mmd` | Generated | Current if regenerated from code | Yes, as generated render artifact | No | Generated Mermaid ownership graph; do not edit manually. |
| `docs/invariants.md` | Canonical | Current | Yes | No | Canonical invariant list paired with tests. |
| `docs/knowledge_acquisition_status.md` | Status | Current | Yes | No | Active board for known, missing, inferred, recommended, and unverified knowledge. |
| `docs/knowledge_classification_vocabulary.md` | Vocabulary | Current | Yes | No | Canonical knowledge-status/classification vocabulary. |
| `docs/local_network_observation_audit.md` | Historical Audit | Historical audit | No | Yes, after promotion review | Local-network observation boundaries and no-reachability conclusions. |
| `docs/local_observation_roadmap_audit.md` | Historical Audit | Historical roadmap audit | No | Yes, after promotion review | Audit of local host observation roadmap. |
| `docs/local_observation_roadmap_reconciliation.md` | Historical Reconciliation | Historical reconciliation | No | Yes, after promotion review | Reconciliation of local observation roadmap outcomes. |
| `docs/logic_model.md` | Canonical | Current | Yes | No | Logic model for evidence, facts, relationships, rules, and projections. |
| `docs/pending_action_lifecycle_inventory.md` | Historical Audit | Stale/quarantined | No | Yes | RuntimeLoop-era pending-action lifecycle inventory with stale warning. |
| `docs/policy_pending_action_inventory.md` | Historical Audit | Stale/quarantined | No | Yes | RuntimeLoop-era policy/pending-action inventory with stale warning. |
| `docs/reasoning_roadmap.md` | Roadmap | Current | Yes | No | Active reasoning roadmap. |
| `docs/recommendation_selection_boundary.md` | Characterization | Historical design report with possible current conclusions | Partially | Partial | Boundary report; promote selection terminology/decisions if still active, then archive as design record. |
| `docs/retry_parse_failure_inventory.md` | Historical Audit | Stale/quarantined | No | Yes | RuntimeLoop-era retry/parse-failure inventory with stale warning. |
| `docs/roadmap_reconciliation.md` | Historical Reconciliation | Historical roadmap reconciliation | No | Yes, after promotion review | Tracks completed roadmap items and unresolved gaps; active conclusions should move to roadmap/status. |
| `docs/rule_inventory.md` | Status | Current inventory | Yes, for rules | No | Active inventory of deterministic rules/catalogs. |
| `docs/runtime_loop_thin_runtime_plan.md` | Historical Audit | Stale/quarantined | No | Yes | RuntimeLoop-era plan with stale warning. |
| `docs/runtime_parity_inventory.md` | Historical Audit | Stale/quarantined | No | Yes | Runtime parity inventory with stale warning. |
| `docs/runtime_reassessment.md` | Historical Audit | Stale/quarantined | No | Yes | Runtime vs RuntimeLoop reassessment with stale warning. |
| `docs/runtime_runtime_loop_responsibility_audit.md` | Historical Audit | Stale/quarantined | No | Yes | Runtime/RuntimeLoop responsibility duplication audit with stale warning. |
| `docs/self_observation_audit.md` | Historical Audit | Historical audit | No | Yes, after promotion review | Self-observation architecture audit. |
| `docs/state.md` | Canonical | Current | Yes | No | Canonical projected-state, evidence graph, contradiction, and confidence semantics. |
| `docs/state_patch_inventory.md` | Historical Audit | Stale/quarantined | No | Yes | RuntimeLoop-era state-patch inventory with stale warning. |
| `docs/temporal_reasoning_audit.md` | Characterization | Historical characterization | No | Yes, after promotion review | Temporal model and characterization-test status. |
| `docs/tool_execution_ownership_audit.md` | Historical Audit | Stale/quarantined | No | Yes | ToolExecutor ownership audit with explicit current boundary warning. |

# Documentation Categories

### Canonical

Canonical documents define Seed today and should be kept small, current, and internally consistent. Canonical documents should contain durable truths, component ownership, invariants, state semantics, and accepted architectural boundaries. Current canonical documents are:

- `README.md`
- `docs/architecture.md`
- `docs/architecture_principles.md` as a secondary principles document, though it overlaps with the README and could be consolidated
- `docs/invariants.md`
- `docs/state.md`
- `docs/logic_model.md`
- `docs/function_blocks.md`

### Generated

Generated documents are authoritative outputs of code and metadata, but they are not hand-authored source documents. Current generated documents are:

- `docs/generated/architecture/architecture_graph.json`
- `docs/generated/architecture/runtime_ownership.mmd`
- `docs/generated/architecture/runtime_ownership.dot`

The authoritative human-editable source for these outputs is `scripts/generate_architecture.py` plus the `__seed_arch__` metadata in runtime source files. The generated files should never be edited manually.

### Roadmap

Roadmap documents describe active direction, missing pieces, and sequencing. Current roadmap document:

- `docs/reasoning_roadmap.md`

Roadmap reconciliation and roadmap audit files are historical unless their open items are not represented in the active roadmap.

### Status

Status documents are active inventories or boards whose purpose is to describe current implementation/knowledge coverage rather than durable architecture. Current status documents are:

- `docs/knowledge_acquisition_status.md`
- `docs/rule_inventory.md`

### Methodology

Methodology documents describe how to work in Seed or how to extend the system safely. Current methodology documents are:

- `docs/capability_extension_methodology.md`
- `docs/codex_prompt_protocol.md`
- `docs/architecture_visualization_phase1.md`

`docs/architecture_visualization_phase1.md` is partly a design record, but it remains methodologically useful because it explains generated architecture documentation practice.

### Vocabulary

Vocabulary documents define named concepts and non-implication boundaries. Current vocabulary documents are:

- `docs/knowledge_classification_vocabulary.md`
- `docs/capability_verification_vocabulary.md`
- `docs/explanation_contract_vocabulary.md`

`docs/audit/capability_operation_vocabulary_audit.md` and `docs/availability_vocabulary_audit.md` are vocabulary audits, not canonical vocabularies, unless a future pass promotes their durable terms.

### Historical Audit

Historical audits record investigation evidence, source-file inventories, and point-in-time findings. They should not define current behavior unless their conclusions have been promoted into canonical documents. Examples include capability verification audits, explainability audits, local observation audits, contradiction handling audits, temporal audits, RuntimeLoop-era inventories, and ownership audits.

### Historical Reconciliation

Historical reconciliations record how earlier audits were resolved. They should remain traceable but should not force contributors to reconstruct current architecture from multiple reconciliation records. Examples:

- `docs/capability_verification_reconciliation.md`
- `docs/explainability_reconciliation.md`
- `docs/local_observation_roadmap_reconciliation.md`
- `docs/roadmap_reconciliation.md`
- `docs/audit/context_knowledge_consolidation.md`

### Characterization

Characterization documents describe observed behavior and test-backed behavior at a point in time. They are useful evidence but should not become competing architecture specs. Examples:

- `docs/explainability_contract_characterization.md`
- `docs/temporal_reasoning_audit.md`
- `docs/recommendation_selection_boundary.md`

### Archive Candidate

Archive candidates are documents that are stale, quarantined, superseded, or primarily historical. Archive candidates should remain available for traceability but should move out of the contributor's default reading path once durable content is promoted.

# Canonical Documentation Set

The smallest practical canonical set is:

| Role | Document(s) | Why canonical |
| --- | --- | --- |
| Entry point and product definition | `README.md` | Defines Seed as knowledge-first and sets global non-implication boundaries. |
| Component architecture | `docs/architecture.md` | Defines EventLedger, ProjectionStore, State, Evidence Graph, Runtime, ToolExecutor, ToolNeedService, and boundary flow. |
| Architecture invariants | `docs/invariants.md` | Captures non-negotiable architectural rules and maps to invariant tests. |
| State and logic semantics | `docs/state.md`, `docs/logic_model.md` | Define projected state, evidence, facts, relationships, contradictions, confidence, and inference model. |
| Functional decomposition | `docs/function_blocks.md` | Explains major function blocks without forcing readers into audits. |
| Extension methodology | `docs/capability_extension_methodology.md` | Defines how capabilities should be extended without unsafe execution or false verification. |
| Canonical vocabularies | `docs/knowledge_classification_vocabulary.md`, `docs/capability_verification_vocabulary.md`, `docs/explanation_contract_vocabulary.md` | Define terms that prevent duplicate or conflicting vocabulary. |
| Status board | `docs/knowledge_acquisition_status.md` | Active board for current known/missing/unverified/recommended knowledge. |
| Active roadmap | `docs/reasoning_roadmap.md` | Active roadmap for reasoning work. |
| Generated architecture | `docs/generated/architecture/*` | Code-derived ownership graph and render artifacts. |

`docs/architecture_principles.md` is currently canonical enough to keep visible, but it is a consolidation candidate because several principles now also appear in `README.md` and `docs/architecture.md`.

# Generated Documentation

Generated architecture documentation currently consists of:

- `docs/generated/architecture/architecture_graph.json`
- `docs/generated/architecture/runtime_ownership.mmd`
- `docs/generated/architecture/runtime_ownership.dot`

Findings:

1. The generated files are authoritative as generated artifacts because they are derived from runtime source metadata and the generator.
2. The generated files are not authoritative hand-edit surfaces. If a generated file is wrong, fix the source metadata or `scripts/generate_architecture.py`, then regenerate.
3. `runtime_ownership.mmd` and `runtime_ownership.dot` explicitly start with generated/do-not-edit banners.
4. `architecture_graph.json` carries generated metadata and should be treated the same way even though it is machine-readable.
5. Generated documentation should be grouped under a clearly labelled generated section in any future documentation index.
6. Generated output should be checked by tests that ensure the generator is deterministic, includes expected canonical ownership edges, and excludes quarantined `RuntimeLoop` nodes.

Authoritative generated content today:

- Runtime owns orchestration.
- Runtime reaches `ToolExecutor` only through `call_tool`.
- Runtime reaches `ToolNeedService` and recommendation ranking through `request_tool`.
- `ToolExecutor` owns registered operation execution.
- `EventLedger` feeds projection and remains event history.
- `ProjectionStore` is a projection cache, not event history.
- `CapabilityCatalog` provides metadata-backed provider/handoff recommendations.

# Historical Audit Review

Historical audits remain useful, but their role should be explicit:

| Audit family | Still useful? | Archive direction | Promotion need |
| --- | --- | --- | --- |
| RuntimeLoop/parity/state-patch/retry/pending-action inventories | Low for current readers; high for archaeology | Archive soon | Mostly none; current stale banners already identify non-canonical status. |
| Tool execution ownership audit | Medium | Archive after confirming `docs/architecture.md` and `docs/invariants.md` capture ToolExecutor ownership | Ensure `call_tool` is the only Runtime-to-ToolExecutor path in canonical docs. |
| Core MVP and planning/execution quarantine audits | High historical value | Archive after promotion | Promote compact quarantine statement and delete-candidate inventory into architecture or archive index. |
| Capability verification audits/reconciliation | Medium | Archive after promotion | Ensure vocabulary captures requested/known/candidate/provider-recommended/verified capability and non-implication boundaries. |
| Availability vocabulary audit | Medium | Archive after promotion | Promote availability vs recommendation vs reachability boundaries if missing. |
| Explainability audits/reconciliation/characterization | Medium | Archive after promotion | Ensure explanation contract vocabulary and state docs include surfaces, support links, and contradiction exposure. |
| Contradiction and temporal audits | Medium | Archive after promotion | Ensure state/invariants define conservative contradiction handling and current-vs-historical semantics. |
| Local observation and self-observation audits | Medium | Archive after promotion | Promote read-only/local/identity/mount/network boundary lessons to methodology or roadmap/status as needed. |
| Roadmap reconciliation | Medium | Archive after promotion | Move active open items into `docs/reasoning_roadmap.md` or status board. |
| Recommendation selection boundary report | Medium | Partial archive | Promote active selection boundary terminology if still desired. |

Documents with explicit stale/quarantined notices are the safest immediate archive candidates after an index exists:

- `docs/ask_question_refuse_inventory.md`
- `docs/capability_ownership_matrix.md`
- `docs/pending_action_lifecycle_inventory.md`
- `docs/policy_pending_action_inventory.md`
- `docs/retry_parse_failure_inventory.md`
- `docs/runtime_loop_thin_runtime_plan.md`
- `docs/runtime_parity_inventory.md`
- `docs/runtime_reassessment.md`
- `docs/runtime_runtime_loop_responsibility_audit.md`
- `docs/state_patch_inventory.md`
- `docs/tool_execution_ownership_audit.md`

# Promotion Analysis

Before archiving, perform a small promotion review. Do not move files until this review confirms that important conclusions are represented in canonical docs.

| Source document | Target canonical document | Information to promote |
| --- | --- | --- |
| `docs/audit/core_mvp_inventory_audit.md` | `README.md` or `docs/architecture.md` | Compact Core MVP path and explicit statement that Seed is not an internal workflow executor. |
| `docs/audit/planning_execution_artifact_quarantine.md` | `docs/architecture.md` and/or `docs/invariants.md` | Quarantined status of ActionPlan, HandoffPlan, ExecutionProposal, and ExecutionAuthorization on the canonical Runtime path. |
| `docs/tool_execution_ownership_audit.md` | `docs/invariants.md` | `call_tool` is the only Runtime path to `ToolExecutor`; `request_tool` is read-only capability resolution. |
| `docs/capability_verification_audit.md`, `docs/capability_verification_fit_audit.md`, `docs/capability_verification_reconciliation.md` | `docs/capability_verification_vocabulary.md` and `docs/knowledge_acquisition_status.md` | Verification lifecycle and distinction between requested, known, candidate, provider-recommended, and verified capabilities. |
| `docs/availability_vocabulary_audit.md` | `README.md`, `docs/knowledge_classification_vocabulary.md`, or a future `docs/availability_vocabulary.md` | Provider recommendation does not imply availability; local configuration does not imply reachability; observed endpoint metadata is not proof of success. |
| `docs/explainability_audit.md`, `docs/explainability_inventory_audit.md`, `docs/explainability_reconciliation.md`, `docs/explainability_contract_characterization.md` | `docs/explanation_contract_vocabulary.md` and `docs/state.md` | Explanation surfaces, support links, unsupported facts, contradiction exposure, and confidence limits. |
| `docs/contradiction_handling_audit.md` | `docs/state.md` and `docs/invariants.md` | Contradictions are surfaced conservatively and not resolved by confidence. |
| `docs/temporal_reasoning_audit.md` | `docs/state.md` and `docs/knowledge_classification_vocabulary.md` | Current projection vs historical event retention, timestamps, and staleness semantics. |
| `docs/local_network_observation_audit.md`, `docs/local_observation_roadmap_audit.md`, `docs/local_observation_roadmap_reconciliation.md`, `docs/self_observation_audit.md` | `docs/capability_extension_methodology.md`, `docs/knowledge_acquisition_status.md`, and `docs/reasoning_roadmap.md` | Observation-source boundaries, read-only local observation lessons, hostname/identity/mount/network distinctions, and remaining active roadmap items. |
| `docs/roadmap_reconciliation.md` | `docs/reasoning_roadmap.md` and `docs/knowledge_acquisition_status.md` | Active open roadmap items and completed-item status. |
| `docs/recommendation_selection_boundary.md` | `docs/capability_verification_vocabulary.md` or `docs/architecture.md` | Recommendation/capability-resolution selection terms if they remain accepted architecture. |
| `docs/audit/capability_operation_vocabulary_audit.md` | `README.md`, `docs/architecture.md`, `docs/capability_verification_vocabulary.md` | Durable capability vs operation vs provider/handoff operation vocabulary and non-execution boundaries. |

No promotion was performed in this audit because the task is inventory-only and the safe next step is to reconcile into a documentation index first.

# Proposed Documentation Architecture

Derived structure:

```text
README.md

docs/
  index.md                         # proposed; describes canonical, generated, roadmap, status, and archive locations

  architecture/
    architecture.md                # current docs/architecture.md
    architecture_principles.md     # current docs/architecture_principles.md, or folded into architecture.md
    invariants.md                  # current docs/invariants.md
    state.md                       # current docs/state.md
    logic_model.md                 # current docs/logic_model.md
    function_blocks.md             # current docs/function_blocks.md

  methodology/
    capability_extension_methodology.md
    codex_prompt_protocol.md
    architecture_visualization.md  # current architecture_visualization_phase1.md, if still desired

  vocabulary/
    knowledge_classification.md
    capability_verification.md
    explanation_contract.md
    availability.md                # proposed only if availability terms are promoted

  status/
    knowledge_acquisition_status.md
    rule_inventory.md

  roadmap/
    reasoning_roadmap.md

  generated/
    architecture/
      architecture_graph.json
      runtime_ownership.mmd
      runtime_ownership.dot

  archive/
    audits/
    reconciliations/
    characterizations/
    inventories/
    runtime_loop_quarantine/
```

This proposed structure separates documents by function rather than by creation history. It answers:

- What defines Seed? `README.md`, `docs/index.md`, and the canonical architecture/vocabulary/methodology set.
- What is generated? `docs/generated/architecture/*` and the generated section of `docs/index.md`.
- What is active roadmap? `docs/roadmap/reasoning_roadmap.md` plus status docs.
- What is historical context? `docs/archive/*`.

A full file move is intentionally not recommended as the first step because it would create churn and may break links. The first step should be an index/reconciliation pass, followed by promotion, then archive moves.

# Archive Candidates

### Strong immediate candidates

These already declare themselves stale/quarantined or are root-level superseded sketches:

- `01-architecture.md`
- `09-pseudocode.md`
- `docs/ask_question_refuse_inventory.md`
- `docs/capability_ownership_matrix.md`
- `docs/pending_action_lifecycle_inventory.md`
- `docs/policy_pending_action_inventory.md`
- `docs/retry_parse_failure_inventory.md`
- `docs/runtime_loop_thin_runtime_plan.md`
- `docs/runtime_parity_inventory.md`
- `docs/runtime_reassessment.md`
- `docs/runtime_runtime_loop_responsibility_audit.md`
- `docs/state_patch_inventory.md`
- `docs/tool_execution_ownership_audit.md`

Rationale: they describe RuntimeLoop-era, stale, quarantined, superseded, or explicitly non-current paths. They should remain available for archaeology, not current architecture discovery.

### Archive after promotion review

These contain likely-promotable conclusions and should not move until the promotion table above is checked:

- `docs/audit/capability_operation_vocabulary_audit.md`
- `docs/audit/context_knowledge_consolidation.md`
- `docs/audit/core_mvp_inventory_audit.md`
- `docs/audit/planning_execution_artifact_quarantine.md`
- `docs/availability_vocabulary_audit.md`
- `docs/capability_verification_audit.md`
- `docs/capability_verification_fit_audit.md`
- `docs/capability_verification_reconciliation.md`
- `docs/contradiction_handling_audit.md`
- `docs/explainability_audit.md`
- `docs/explainability_contract_characterization.md`
- `docs/explainability_inventory_audit.md`
- `docs/explainability_reconciliation.md`
- `docs/local_network_observation_audit.md`
- `docs/local_observation_roadmap_audit.md`
- `docs/local_observation_roadmap_reconciliation.md`
- `docs/recommendation_selection_boundary.md`
- `docs/roadmap_reconciliation.md`
- `docs/self_observation_audit.md`
- `docs/temporal_reasoning_audit.md`

Rationale: these are valuable historical evidence, but current contributors should not have to read them to determine accepted architecture.

# Documentation Risks

1. **Duplicate truth.** Runtime ownership, execution boundaries, capability non-implication, and observation-first framing appear in multiple documents. Duplicate truth increases the chance that one file drifts.
2. **Stale RuntimeLoop gravity.** Many historical docs discuss RuntimeLoop, parity, retry behavior, pending actions, state patches, and planning paths. Even with stale warnings, their presence near canonical docs can mislead contributors.
3. **Vocabulary scattering.** Capability, operation, provider/handoff, availability, verification, explanation, and knowledge-classification terms are spread across audits and canonical vocabularies. This creates competing definitions unless canonical vocabulary docs are clearly indexed.
4. **Generated/manual ambiguity.** Generated architecture artifacts are properly marked, but a top-level docs index should state that the generator and source metadata are the edit surfaces.
5. **Roadmap drift.** Reconciliation documents may contain completed, rejected, or open roadmap items not reflected in `docs/reasoning_roadmap.md` or status docs.
6. **Audit conclusions diverging from canonical docs.** Audits often contain precise source-derived conclusions. If those are not promoted, canonical docs can become less precise than historical evidence.
7. **Archive without promotion.** Moving documents too early could hide important boundaries around availability, verification, local observation, explainability, and quarantine status.
8. **Contributor onboarding cost.** Without an index, new contributors must infer document status from filenames and stale banners.

# Recommended Next Step

Smallest safe next step:

1. Create `docs/index.md` that labels each documentation area as canonical, generated, roadmap, status, methodology, vocabulary, or historical/archive.
2. In the same pass, add a short top-of-file status banner to canonical docs and to major historical families if missing.
3. Do a promotion pass for the table in this audit, limited to compact boundary statements and vocabulary deltas.
4. Only after promotion, move strong archive candidates into `docs/archive/` in a separate archive pass.

Do not do feature work, runtime work, observation implementation, provider integration, or architecture changes as part of the next step.

# Non-Goals

- No Runtime changes.
- No ToolExecutor changes.
- No EventLedger ownership changes.
- No ProjectionStore ownership changes.
- No behavior implementation.
- No observation implementation.
- No provider integration.
- No execution behavior, orchestration, LLM reasoning, or feature work.
- No promotion, file moves, archive moves, or canonical rewrites in this audit.
- No test changes unless documentation invariant tests require them.
