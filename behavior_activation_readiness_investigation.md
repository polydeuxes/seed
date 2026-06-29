# Behavior Activation Readiness Investigation

## Scope

This is a bounded implementation investigation. It does not implement behavior, recover additional ownership, add runtime surfaces, add planners, add automation, change compatibility boundaries, or register new diagnostics.

The question is not whether the completed families are architecturally interesting. The question is whether implementation evidence shows that recovered ownership has now reached a point where additional recovery in the same family would likely provide diminishing returns and where future work could begin exercising behavior through the recovered owners.

Repository authority wins. The evidence below is drawn from implementation files and completed recovery/audit reports.

## Implementation evidence reviewed

Primary completed families and completion evidence reviewed:

- `operational_responsibility_slice_001.md` through `operational_responsibility_slice_006.md`.
- `execution_visibility_slice_001.md` through `execution_visibility_slice_005.md`.
- `observation_derived_capability_slice_001.md` through `observation_derived_capability_slice_005.md`.
- `answer_composition_slice_001.md` through `answer_composition_slice_004.md`.
- `answer_composition_family_completion_audit.md`.
- `projection_influence_lineage_slice_001.md` through `projection_influence_lineage_slice_003.md`.
- `projection_influence_lineage_family_completion_audit.md`.
- `read_model_ownership_slice_001.md` through `read_model_ownership_slice_005.md`.
- `read_model_ownership_family_completion_audit.md`.
- `responsibility_family_completion_inquiry_audit.md`.
- `implementation_responsibility_family_inventory_audit.md`.
- `implementation_responsibility_family_stack_audit.md`.
- `architectural_recovery_methodology_characterization.md`.
- `read_model_dependency_graph_investigation.md`.
- `evidence_contract_family_investigation.md`.
- `documentation_code_agreement_investigation.md`.
- `methodology_as_inquiry_subject_investigation.md`.

Representative implementation evidence reviewed:

- `seed_runtime/registry.py` for registered operation catalog ownership.
- `seed_runtime/tool_needs.py` for capability need resolution and recommendation handoff.
- `seed_runtime/execution.py` for execution recording and post-execution knowledge extraction handoff.
- `seed_runtime/execution_status.py` for status emission and visibility ownership.
- `seed_runtime/diagnostic_inventory.py` and diagnostic shape-audit tests for visibility compatibility surfaces.
- `seed_runtime/capability_inventory.py`, `seed_runtime/capability_candidates.py`, `seed_runtime/capability_verification.py`, and `seed_runtime/capability_promotion_readiness.py` for read-only capability derivation.
- `seed_runtime/operational_story.py`, `seed_runtime/inquiry_orientation.py`, `seed_runtime/reference_selection.py`, `seed_runtime/reasoning_path_audit.py`, and `seed_runtime/selection_path_audit.py` for answer and context-preserving surfaces.
- `seed_runtime/state.py` for projection influence lineage, replay/finalization/publication, and the terminal projection-state handoff.
- `seed_runtime/read_model_ownership.py`, `seed_runtime/state_views.py`, `seed_runtime/state_summary_views.py`, and `seed_runtime/fact_index.py` for read-model construction, dependency identity, cache lookup, construction, and cache publication.

## Readiness classification

| Completed family | Stop additional same-family recovery? | Ready to begin behavior work? | Natural behavioral consumer | Confidence |
| --- | --- | --- | --- | --- |
| Operational Responsibility | Yes, for the recovered execution chain. | Yes, but only through already separated operation lifecycle boundaries. | Safer operation lifecycle behavior: policy/pending-action lifecycle, operation selection prerequisites, execution-result handling, and post-execution evidence flow. | Medium-high |
| Execution Visibility | Yes, for the recovered visibility chain. | Yes, but behavior should remain observational/read-only unless explicitly operational. | Operational observability behavior: diagnostic consistency checks, status/timing/cache interpretation, run health, and operator-facing visibility answers. | Medium |
| Observation-Derived Capability | Yes, for the read-only recovered chain. | Partially: ready for read-only capability behavior, not writable admission/promotion behavior. | Capability recommendation, verification explanation, promotion-readiness explanation, inventory consumers, and operation-selection context. | Medium-high for read-only behavior; medium-low for writable behavior |
| Answer Composition | Yes, for representative reusable answer composition. | Yes, for composing existing bounded answers; no for retrofitting every inquiry surface. | Context-preserving answer behavior: explanation composition, bounded response normalization, support/boundary/limitation propagation. | High for representative behavior; medium for broad rollout |
| Projection Influence Lineage | Yes, for conservative projection/replay lineage. | Yes, but only if behavior consumes the lineage to explain or safely bound projection behavior; not enough for selective replay yet. | Projection explanation, replay target justification visibility, invalidation reasoning, downstream read-model dependency handoff. | Medium-high |
| Read-Model Ownership | Yes, for individual dependent read-model lifecycle ownership. | Yes. This is the strongest behavior-activation opportunity. | Read-model cache reuse behavior, dependency-aware rebuild decisions, state-summary/fact-index build orchestration, and read-model freshness explanation. | High |

## Family assessments

### 1. Operational Responsibility

#### Readiness conclusion

Operational Responsibility is ready for behavior work inside the recovered execution lifecycle, and additional same-family recovery should stop unless new implementation evidence identifies a genuinely recurring operational owner outside the completed chain.

#### Supporting implementation evidence

The completed operational chain separates registered operation catalog ownership, capability recommendation, validation, policy authorization, execution realization, durable execution recording, and post-execution knowledge extraction. The sixth slice identifies the terminal boundary: execution recording appends durable tool-call events, while post-execution extraction consumes a completed execution record and invokes fact extraction.

The implementation now makes that handoff explicit in `ToolExecutor._execute_allowed_tool_call`: the success path records a completed tool-call event, then passes the completed event to `_extract_post_execution_knowledge(...)`. This is not just prose; the code has distinct implementation-local responsibilities for recording and extraction.

The completion inquiry audit treats the natural termination point as the boundary after `Execution Recording != Post-Execution Knowledge Extraction`, because the central chain from recommendation through extraction has implementation-backed boundaries and compatibility-preserving slices.

#### Remaining architectural risks

Remaining operational pressure exists, but it is not evidence that the recovered family should continue slicing:

- Policy outcome recording versus pending-action lifecycle ownership remains adjacent.
- Operation selection prerequisites remain outside the execution chain.
- Writable capability admission and lifecycle behavior are outside the operational execution owner.

These are behavioral opportunities or future-family candidates, not reasons to keep recovering the same operational chain.

#### Behavioral opportunities

Natural behavior that could consume this recovered ownership:

- A pending-action lifecycle that consumes policy outcomes instead of hiding them inside execution.
- Safer operation selection using already separated registered operation and capability recommendation boundaries.
- Execution-result handling that can reason over `tool.call.completed` before fact extraction.
- Operator explanations that distinguish execution recording from diagnostic or knowledge mutation.

#### Confidence

Medium-high. The terminal ownership handoff is implementation-backed, and completion audits agree that same-family recovery has reached diminishing returns. Confidence is not absolute because policy lifecycle and selection prerequisites remain real adjacent pressure.

### 2. Execution Visibility

#### Readiness conclusion

Execution Visibility should resist additional ownership recovery for the completed status/timing/cache/diagnostic chain. It is ready for behavior only where behavior is explicitly observational or read-only.

#### Supporting implementation evidence

The recovered chain makes execution status, timing, cache state, state-build visibility, diagnostic inventory, and diagnostic shape-audit visibility observable without changing the operational behavior being observed. The completion inquiry audit identifies the natural termination point after `State Build Visibility != Projection Cache Diagnostics`, because status/timing/cache/diagnostic boundaries have implementation-backed slices and tests.

The family stack audit classifies Execution Visibility as implementation complete for the recovered chain and describes diagnostic inventory/shape-audit surfaces as shared compatibility boundaries that preserve read-only diagnostic behavior.

The repository-level operational visibility contract reinforces the implementation boundary: new or changed diagnostics must be registered in diagnostic inventory, checked by diagnostic shape audit, and remain `mutates_cluster=false` unless intentionally operational. That contract is evidence that visibility has become executable discipline, not merely documentation preference.

#### Remaining architectural risks

Execution Visibility has the highest risk of accidental behavior expansion because visibility surfaces can be mistaken for operational control. Remaining pressure around timing interpretation, cache debug, status surfaces, and diagnostic inventories should not be promoted into cluster mutation without explicit evidence.

#### Behavioral opportunities

Natural behavior that could consume this recovered ownership:

- Read-only run health summaries over existing status/timing/cache surfaces.
- Diagnostic consistency enforcement using the inventory and shape-audit compatibility boundaries.
- Operator-facing explanations that distinguish state-build visibility from projection-cache diagnostics.
- Recordable diagnostic runs that preserve `record_scope=diagnostic_run` and `mutates_cluster=false`.

#### Confidence

Medium. The read-only visibility chain is strong, but behavior activation must be carefully bounded so observational surfaces do not silently become operational authority.

### 3. Observation-Derived Capability

#### Readiness conclusion

Observation-Derived Capability should stop additional ownership recovery for the completed read-only chain. It is ready for read-only behavior that consumes capability evidence, verification, promotion readiness, inventory, and executable operation contract metadata. It is not ready for writable capability admission behavior without a separate investigation.

#### Supporting implementation evidence

The fifth slice makes the handoff from executable operation contract metadata into the capability inventory explicit through `_ExecutableOperationContractState` and `_CapabilityInventorySources`. The public `CapabilityInventoryEntry` remains a read-only presentation model, and the compatibility union of registered operation labels, requested capabilities, and admitted verification fact subjects is intentionally preserved.

The completion inquiry audit states that the natural termination point is after `Capability Inventory != Executable Operation Contract`, because the family has closed the loop between observed evidence, verification, promotion readiness, inventory, and executable contract metadata without changing behavior.

The family stack audit classifies evidence strength as high for the read-only capability chain and medium for writable admission/promotion behavior. That distinction is central: behavior may begin by consuming the recovered read-only chain, but not by pretending the repository has a completed writable capability lifecycle.

#### Remaining architectural risks

Risks and counterexamples:

- Capability inventory consumers remain separate from inventory construction.
- Writable promotion/admission remains outside the completed family.
- Operation selection prerequisites remain outside the inventory/contract handoff.
- The compatibility union can hide source distinctions if future behavior consumes it without preserving source evidence.

#### Behavioral opportunities

Natural behavior that could consume this recovered ownership:

- Capability recommendation explanations that cite observed evidence and executable operation contract labels separately.
- Promotion-readiness reports that remain read-only.
- Operation-selection context that consumes inventory sources without owning execution.
- Gap analysis between requested capabilities, admitted capability facts, and registered executable contracts.

#### Confidence

Medium-high for read-only behavior. Medium-low for writable behavior, because the repository intentionally distinguishes read-only readiness from admission or promotion writers.

### 4. Answer Composition

#### Readiness conclusion

Answer Composition should stop additional same-family recovery for the representative reusable layer. It is ready for behavior that composes bounded answers from existing material, but not for universal retrofitting of every inquiry-like surface.

#### Supporting implementation evidence

The family completion audit concludes that Answer Composition has become a reusable architectural layer for the currently projected responsibility. The strongest complete implementations are `OperationalStory` and `InquiryOrientationView`; both separate answer material, reasoning, support, boundary, limitations, and compatibility handoff.

In implementation, `build_operational_story(...)` delegates to `_compose_operational_story_payloads(...)`, receives answer/reasoning/supporting-evidence/boundary/limitations payloads, and then hands those payloads into the stable `OperationalStory` compatibility object. Rendering remains separate in `format_operational_story(...)` and does not own reasoning or selection.

The audit explicitly warns that several additional inquiry surfaces already compose bounded answers, but their responsibilities remain compressed in public dataclasses or builder logic. Those are counterexamples to universal completion, not evidence against the representative family.

#### Remaining architectural risks

Risks and counterexamples:

- `reference_selection`, `reasoning_path`, `selection_path`, and `inquiry_artifacts` already carry answer-like material, but not all have the full reusable implementation-local primitive.
- Universal normalization could become a compatibility migration rather than behavior.
- Answer composition could be confused with rendering unless behavior preserves the builder/formatter separation.

#### Behavioral opportunities

Natural behavior that could consume this recovered ownership:

- Context-preserving answers that consistently carry answer, reason, support, boundary, and limitations.
- Question-surface responses that reuse the representative composition shape where implementation evidence supports it.
- Explanation behavior that preserves unknowns and authority boundaries instead of flattening them into final prose.
- Comparison or recommendation answers that can expose why a result was selected and what remains outside scope.

#### Confidence

High for representative bounded answer behavior. Medium for broader rollout, because repository authority explicitly limits completion to representative surfaces rather than universal retrofitting.

### 5. Projection Influence Lineage

#### Readiness conclusion

Projection Influence Lineage should stop additional same-family recovery for the current conservative replay/projection behavior. It is ready for behavior that consumes lineage to explain, bound, or audit projection decisions. It is not ready for selective replay or dependency-changing behavior merely because lineage now exists.

#### Supporting implementation evidence

The family completion audit concludes that Projection Influence Lineage is complete for the current conservative replay/projection implementation. The implementation exposes a chain from projection-influence evidence through replay assessment, target justification, target selection, replay execution, finalization, and projection publication.

The terminal handoff is projection publication: `_publish_finalized_projection(...)` returns `_ProjectionPublication(visible_state=request.finalized_state)`. The audit treats this as a finalized projected `State` being published unchanged, not as read-model construction, rendering, cache persistence, or consumer semantics.

Remaining limitations are explicitly conservative compatibility behavior: replay is always required, target selection always includes event replay and projection finalization, and publication is identity-preserving. The audit states these are not evidence of hidden same-family ownership.

#### Remaining architectural risks

Risks and counterexamples:

- Affected projection recovery is descriptive and incomplete for dependency authority.
- Selective replay, dirty projection invalidation, and dependency graph behavior would be behavior changes, not completed lineage behavior.
- Downstream read models and caches consume published state but are not owned by Projection Influence Lineage.

#### Behavioral opportunities

Natural behavior that could consume this recovered ownership:

- Projection explanation: why replay/finalization occurred and what influence evidence was considered.
- Conservative invalidation reasoning that remains compatible with full replay.
- Audit surfaces that show target justification without changing target selection.
- Downstream handoff to read-model construction and dependency identity.

#### Confidence

Medium-high. The chain is explicit and completion audit confidence is high, but behavior activation must not smuggle in selective replay or dependency authority.

### 6. Read-Model Ownership

#### Readiness conclusion

Read-Model Ownership is the strongest implementation opportunity for behavior activation. It should resist additional same-family ownership recovery because the individual dependent read-model lifecycle is complete. Future work should shift from recovery to behavior here first.

#### Supporting implementation evidence

The family completion audit states that implementation exposes the complete read-model lifecycle requested for this family: projection publication, construction inputs, dependency identity, cache lookup, construction, and cache publication.

The implementation-local module defines explicit lifecycle boundaries: `ReadModelConstructionInputs`, `ReadModelDependencyIdentity`, `ReadModelCacheLookupRequest`, `ReadModelCacheLookupResult`, `ReadModelConstructionRequest`, `ReadModelConstructionResult`, `ReadModelCachePublicationRequest`, and the corresponding helper functions. The module also states negative ownership constraints: read models consume already-published projected `State` and do not own replay, finalization, projection publication, event ledger behavior, projected-state cache behavior, rendering, scheduling, or lower-level persistence policy.

The family completion audit says both recurring dependent read-model paths reviewed in implementation--state summary and fact index--now traverse the same explicit lifecycle boundaries. The fifth slice reinforces that a completed read-model construction result is consumed by a cache-publication request and published through existing snapshot creation and cache-save behavior without changing payloads, cache keys, lookup decisions, or compatibility behavior.

The audit also says no additional implementation slice is justified inside this family now. Remaining pressure belongs to debug/timing instrumentation, cache policy/storage composition, read-model selection/composition, partial-refresh authority, dependency graph ownership, or upstream projection-builder dependency ownership.

#### Remaining architectural risks

Risks and counterexamples:

- Read-Model Dependency Graph investigation later concluded that dependency graph ownership does not yet justify a responsibility family. That means behavior should not depend on a mature graph abstraction.
- Cache policy/storage composition remains outside the read-model owner.
- Read-model selection/composition pressure remains separate from lifecycle ownership.
- Partial refresh authority and dependency-changing behavior remain speculative until implementation evidence supports them.

#### Behavioral opportunities

Natural behavior that could consume this recovered ownership:

- Dependency-aware cache reuse decisions over existing exact-match identity fields, without inventing a full dependency graph.
- Freshness/explanation behavior for why a state summary or fact index was reused or rebuilt.
- Shared build orchestration over state summary and fact index using the existing lifecycle boundaries.
- Safer cache publication behavior that consumes completed construction results rather than duplicating snapshot handoffs.
- Read-model behavior tests that exercise lifecycle decisions without altering projection publication or store policy.

#### Confidence

High. This family has explicit request/result boundaries, recurring consumers, shared lifecycle use in state summary and fact index, and a completion audit that identifies no remaining family-local compression.

## Which completed responsibility families are ready for behavior work?

Ready, with bounded scope:

1. **Read-Model Ownership** -- strongest readiness. It has explicit lifecycle owners, recurring consumers, and a completed individual read-model lifecycle.
2. **Answer Composition** -- ready for bounded answer behavior in surfaces with implementation-backed answer/reason/support/boundary/limitations material.
3. **Operational Responsibility** -- ready for operation-lifecycle behavior that consumes existing boundaries without adding hidden ownership.
4. **Observation-Derived Capability** -- ready for read-only capability behavior, not writable admission/promotion.
5. **Projection Influence Lineage** -- ready for explanatory or audit behavior, not selective replay.
6. **Execution Visibility** -- ready for read-only observational behavior, not operational control.

## Which completed families should continue resisting additional ownership recovery?

All six should resist additional same-family recovery unless new implementation evidence identifies a same-family compressed owner not already addressed.

The strongest stop signals are:

- Operational Responsibility reached the completed event-to-fact-extraction terminal handoff.
- Execution Visibility reached the state-build/projection-cache diagnostic boundary.
- Observation-Derived Capability reached the inventory/executable-contract handoff for the read-only chain.
- Answer Composition reached representative reusable answer-composition implementations and named universal retrofitting as out of scope.
- Projection Influence Lineage reached projection-state publication and handed downstream concerns to read models.
- Read-Model Ownership reached cache publication for completed read models and named remaining pressure outside the lifecycle owner.

## What kinds of behavior naturally follow each completed family?

| Family | Natural behavior |
| --- | --- |
| Operational Responsibility | Pending-action lifecycle, safer operation selection, execution-result handling, post-execution evidence flow explanations. |
| Execution Visibility | Read-only run health, diagnostic consistency, timing/cache/status interpretation, diagnostic-run recording with non-mutating scope. |
| Observation-Derived Capability | Capability recommendation explanations, read-only promotion readiness, inventory gap analysis, operation-selection context. |
| Answer Composition | Context-preserving answers, bounded response normalization, authority/unknown propagation, comparison and recommendation explanations. |
| Projection Influence Lineage | Projection decision explanations, conservative replay justification, invalidation reasoning, downstream handoff clarity. |
| Read-Model Ownership | Cache reuse/rebuild behavior, read-model freshness explanation, shared state-summary/fact-index lifecycle orchestration, safe cache publication. |

## Strongest implementation opportunity for the next development phase

**Read-Model Ownership offers the highest implementation leverage for the next phase of Seed's evolution.**

Reasons:

1. It has the clearest completed lifecycle: construction inputs, dependency identity, cache lookup, construction, and cache publication.
2. It has recurring existing consumers: state summary and fact index.
3. It sits immediately downstream of Projection Influence Lineage, so it can make already-published projected state useful without changing replay or projection behavior.
4. It can begin behavior with exact-match dependency identity and cache lifecycle explanations without requiring the not-yet-justified Read-Model Dependency Graph family.
5. It has strong negative ownership boundaries, reducing the risk that behavior accidentally absorbs replay, finalization, projection publication, lower-level persistence policy, or rendering.

The recommended next behavior should be small and implementation-backed: exercise read-model lifecycle behavior that explains or chooses cache reuse/rebuild for existing dependent read models using current exact-match dependency identity. It should not introduce a dependency graph, partial refresh, new runtime surface, or cache policy redesign unless a separate bounded investigation proves that authority.

## Recommended next action

Begin behavior work with **Read-Model Ownership**, constrained to existing implementation authority:

1. Select one existing dependent read model path, preferably state summary because it is operator-visible and already uses the recovered lifecycle.
2. Define the smallest behavior that consumes current lifecycle boundaries, such as a read-only explanation of cache lookup, construction, and publication decisions, or a focused cache reuse/rebuild decision test over existing exact-match identity.
3. Preserve the boundary that read-model ownership consumes published projected `State` and does not own projection replay, finalization, projection publication, dependency graph policy, lower-level storage policy, rendering, or CLI compatibility.
4. Add behavior tests only after the behavior task is explicitly selected; this investigation intentionally adds no behavior.

## Final answer to acceptance question

The recovered architecture that has most clearly earned the right to become useful is **Read-Model Ownership**. Implementation effort should shift from recovery to behavior where completed ownership is explicit, recurring, and already consumed. The highest-leverage next phase is behavior that uses the read-model lifecycle to make state-summary and fact-index construction/cache reuse more explainable and reliable while staying inside current exact-match dependency authority.
