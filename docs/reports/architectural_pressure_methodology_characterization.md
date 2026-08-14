# Architectural Pressure Methodology Characterization

## Executive answer

Architectural pressure is the implementation condition that makes architectural recovery necessary: one implementation owner is carrying multiple bounded responsibilities such that the responsibilities cannot yet be independently reasoned about, implemented, tested, evolved, completed, or safely handed to downstream owners.

Repository evidence supports the candidate definition with one important refinement:

```text
Implementation Pressure exists when
one implementation owner or corridor
contains multiple bounded responsibilities
whose boundary-crossing evidence, authority, compatibility contract,
or stopping point is not yet independently visible enough for safe local change.
```

Compressed ownership is therefore the strongest implementation-backed cause of recovery. Pressure is observed through concrete implementation evidence: overloaded methods, dataclasses, report shapes, cache/build paths, event corridors, diagnostic payloads, inventory unions, and repeated manual reconstruction. Recovery relieves pressure by extracting or naming one bounded owner or owner handoff at a time while preserving public behavior and proving the preserved boundary with tests or completion audits.

Pressure is gone for a family when no recurring same-family compressed owner remains and any remaining pressure points to adjacent ownership, unsupported behavior, conservative compatibility limits, or a frontier rather than another slice. Residual pressure becomes frontier pressure when it is no longer a local implementation compression that can be relieved by one compatibility-preserving slice, but instead names a future autonomy, evaluation, review, authority, optimization, or capability question requiring additional evidence before implementation.

Repository evidence strongly supports pressure as a recurring invariant behind architectural recovery. It does **not** support treating every pressure signal as implementation authority, every compression as meaningful pressure, or every residual pressure as a next slice.

Repository authority wins.

## Methodology evidence reviewed

Primary methodology evidence reviewed:

- `docs/architectural_recovery_methodology_characterization.md`
- `recovery_to_frontier_promotion_characterization.md`
- `responsibility_recovery_evaluation_readiness_investigation.md`
- `responsibility_family_completion_inquiry_audit.md`
- `implementation_responsibility_family_stack_audit.md`
- `responsibility_authority_frontier_reconciliation.md`

Primary completed-family and slice evidence reviewed:

- `operational_responsibility_slice_003.md`
- `execution_visibility_slice_005.md`
- `observation_derived_capability_slice_005.md`
- `projection_influence_lineage_family_completion_audit.md`
- `read_model_ownership_family_completion_audit.md`
- `timing_visibility_current_facts_completion_audit.md`
- `docs/answer_composition_family_completion_audit.md`

Primary pressure investigations reviewed:

- `docs/repository_pressure_inventory.md`
- `docs/pressure_source_observation.md`
- `docs/operator_pressure_as_evidence_observation.md`
- `docs/pressure_visibility_and_preservation_observation.md`
- `docs/pressure_precursor_and_work_activation_observation.md`
- `docs/pressure_transformation_investigation.md`
- `docs/pressure_integration_and_orphaned_pressure_investigation.md`
- `docs/historical_inquiry_pressure_investigation.md`
- `docs/inquiry_closure_satisfaction_and_residual_pressure_investigation.md`
- `docs/surviving_pressure_after_decomposition_observation.md`
- `docs/handoff_pressure_transition_observation.md`
- `docs/future_state_consequence_pressure_selection_observation.md`

Primary counterexample / negative evidence reviewed:

- `responsibility_evaluation_competency_recovery_investigation.md`
- `evidence_interpretation_competency_recovery_investigation.md`
- `docs/operator_pressure_as_evidence_observation.md`
- `projection_influence_lineage_family_completion_audit.md`
- `read_model_ownership_family_completion_audit.md`
- `docs/architectural_recovery_methodology_characterization.md`
- `recovery_to_frontier_promotion_characterization.md`

## Implementation-backed definition of pressure

### Strongest supported definition

Architectural implementation pressure exists when all of the following are true:

1. **One owner or corridor carries more than one bounded responsibility.** The owner may be a method, dataclass, report shape, CLI path, cache/build corridor, event corridor, inventory builder, projection path, or diagnostic structure.
2. **The responsibilities are already behaviorally present.** Recovery does not invent them; it finds responsibilities already operating inside the implementation.
3. **Their boundary is not independently visible.** The implementation cannot show, test, audit, or reason about each responsibility without mentally reconstructing hidden handoffs.
4. **The compression affects safe evolution.** The local owner is difficult to change because compatibility, authority, evidence, or downstream consumption is ambiguous.
5. **A compatibility-preserving boundary is plausible.** The repository's demonstrated recovery pattern separates or names one local owner/handoff without changing public behavior.

Short form:

```text
pressure = behaviorally real responsibility plurality
           compressed inside one implementation owner
           with insufficient independent boundary visibility
```

This modifies the candidate definition only by broadening "one implementation owner" to "one owner or corridor" and by making boundary-crossing evidence, authority, and compatibility part of what cannot yet be independently reasoned about.

### What pressure is not

Pressure is not merely:

- repeated vocabulary;
- operator pain by itself;
- an architectural preference;
- a broad frontier question;
- a missing abstraction;
- a large method with only one responsibility;
- an adjacent unsolved problem after a family is complete;
- a document that names a concept without executable or completion-audit evidence.

## Pressure creation

### 1. Compression of neighboring implementation responsibilities

The clearest pressure source is a local owner that already performs multiple bounded responsibilities.

Operational Responsibility shows this directly. Before recovery, `_execute_allowed_tool_call()` both recorded execution lifecycle events and realized the registered callable by resolving, invoking, and validating it. The slice identified this as compression because execution realization appeared inline inside the event-recording corridor even though surrounding services already distinguished policy, execution, recording, and fact extraction.

Execution Visibility shows the same pattern in a report shape. `StateSummaryCacheDebugReport` carried state-build visibility and projection-cache diagnostic evidence in one return shape. Pressure existed because one report owned both user-facing state-build visibility fields and projection-cache diagnostic fields.

Observation-Derived Capability shows pressure at an inventory-universe construction point. `_inventory_capabilities()` accumulated registered executable operation contract labels, requested capabilities, and admitted capability subjects in one function body, so capability inventory presentation and executable operation contract derivation were correct but compressed.

### 2. Hidden handoff chains

Projection Influence Lineage shows pressure when an ordered chain exists but is hidden inside one projection path. Recovery exposed lineage recovery, replay scope assessment, replay selection justification, replay selection, replay execution, finalization, and publication as a direct implementation chain instead of leaving the whole sequence compressed inside `project_from_state(...)`.

Read-Model Ownership shows pressure when repeated cache/build paths contain a lifecycle whose boundaries are not independently named. The recovered lifecycle is projection publication, construction inputs, dependency identity, cache lookup, construction, and cache publication.

### 3. Repeated manual reconstruction

Pressure also appears when repository work repeatedly reconstructs the same relationship. Inquiry closure evidence distinguishes implemented from resolved: implementation preserves a relationship, while resolution means reconstruction pressure substantially decreases. If a relationship continues to be manually reconstructed after implementation, residual pressure remains.

### 4. Operator pain as an orientation signal, not cause authority

Operator pressure can create investigation pressure by showing where the system hurts. The cache investigation preserved this distinction: slow `seed --state-build` was real pressure, but not sufficient authority for the root cause or implementation direction. Instrumentation localized the implementation target to repeated relationship projection during fact-event replay rather than generic cache work.

## Observable implementation evidence that creates pressure

Repository evidence supports these pressure indicators:

| Evidence type | What it demonstrates | Example |
| --- | --- | --- |
| Overloaded method corridor | Multiple responsibilities are executed in one local path | `_execute_allowed_tool_call()` recorded events and realized registered operations before recovery. |
| Overloaded report/dataclass | One shape carries fields from separate owners | `StateSummaryCacheDebugReport` mixed state-build visibility and projection-cache diagnostics. |
| Inventory union or aggregator | Presentation and source derivation are compressed | `_inventory_capabilities()` mixed operation contracts, requested needs, and admitted capabilities. |
| Hidden decision chain | Ordered handoffs exist but are not visible as owners | Projection influence lineage through publication was hidden in `project_from_state(...)`. |
| Repeated cache/build lifecycle | Lookup, identity, construction, and publication are adjacent but unnamed | State summary and fact index read-model paths. |
| Repeated reconstruction | A relationship must be re-derived in investigations | `pressure -> observation-space gap`, `question -> answering surface`, or `answer -> next investigation`. |
| Completion-audit residuals | Same-family pressure is gone, but adjacent pressure remains classified | Read-model dependency graph, cache invalidation, timing visibility, projection builder dependencies. |
| Measured operational pain | A surface is interrupting use and deserves inquiry | Slow state-build cold path leading to instrumentation. |

The strongest indicators are implementation-local and executable. The weakest are vocabulary-only or prose-only.

## Pressure relief

Recovery relieves implementation pressure by making one boundary independently visible without redesigning the system.

The recurring relief shape is:

```text
compressed owner
↓
select one boundary
↓
introduce/nickname one local owner or handoff
↓
preserve public compatibility
↓
prove unchanged behavior and new boundary
↓
classify remaining compression
```

Examples:

- Operational Responsibility relieved pressure by moving callable resolution/invocation/output validation into `_realize_registered_operation()` while `_execute_allowed_tool_call()` retained event recording and result shaping.
- Execution Visibility relieved pressure by splitting `StateSummaryCacheDebugReport` into private state-build visibility and projection-cache diagnostic payloads while preserving legacy accessors and formatter behavior.
- Observation-Derived Capability relieved pressure by separating admitted capability knowledge, executable operation contracts, and requested capabilities into inventory sources before building the same deterministic union.
- Projection Influence Lineage relieved pressure by exposing the full local chain from lineage recovery through publication.
- Read-Model Ownership relieved pressure by naming each lifecycle boundary and using request/result handoffs for construction inputs, dependency identity, cache lookup, construction, and cache publication.

Pressure relief is not proven by a nicer name. It is proven when the implementation can change locally, tests can target the boundary, public behavior remains stable, and completion audits can identify whether same-family compression still exists.

## When pressure is eliminated

Pressure is eliminated for a bounded family when:

1. The previously compressed responsibilities have independent local owners or handoffs.
2. Downstream consumers still receive the same public behavior, payloads, events, CLI/JSON shapes, cache semantics, or rendering.
3. Tests or audits preserve the recovered boundary.
4. Counterexamples fail to show recurring same-family compression.
5. Remaining pressure is classified as adjacent, unsupported, historical, residual, or frontier rather than another same-family slice.

Read-Model Ownership is the clearest example. Its completion audit concluded no recurring compressed boundary remains inside the family, while cache composition, invalidation policy, timing/debug instrumentation, read-model selection, and projection-builder dependencies belong elsewhere.

Projection Influence Lineage is another strong example. Its completion audit concluded no recurring compressed owner remains inside the family. Remaining limitations are conservative full replay/finalization behavior or downstream read-model/cache pressure, not another projection-lineage ownership slice.

## When pressure remains

Pressure remains when one of these conditions persists:

- a relationship is still manually reconstructed;
- adjacent responsibilities still share an implementation corridor;
- a recovered owner exposes a downstream dependency or authority question;
- instrumentation shows the implementation target has moved;
- completion audit finds concrete adjacent compression outside the completed family;
- the same question reappears with little narrowing;
- the implementation preserves a relationship but follow-up investigations continue around coverage, limitations, boundaries, or unknowns.

Residual pressure does not mean the previous recovery failed. Repository evidence supports a distinction between implemented and resolved. A relationship can be implemented while pressure remains active around neighboring questions.

## Residual pressure classification

Repository evidence supports these classifications:

### Active pressure

Pressure is active when reconstruction continues, the same question reappears, new investigations expose the same gap, or operational use continues to surface the problem.

### Partially resolved pressure

Pressure is partially resolved when implementation exists and the central pressure is reduced, but follow-up work remains around boundaries, limitations, coverage, or extensions.

### Residual pressure

Residual pressure remains after the core question is addressed but secondary pressures persist. It is often the output of a completion audit.

### Historical pressure

Historical pressure produced substantial repository-visible structure but no longer dominates current investigation activity because the relationship is now preserved and manual reconstruction is uncommon.

### Orphaned pressure

Orphaned pressure is unresolved pressure without a visible path into findings, conclusions, boundaries, next investigation, or another pressure. The evidence is weaker, but repeated reappearance without narrowing and isolated vocabulary are warning signs.

### Frontier pressure

Frontier pressure names a future bounded question that is not currently a same-family implementation compression. It may concern autonomy, review, readiness, capability acquisition, dependency authority, selective replay, invalidation policy, or evaluation criteria. It requires further investigation before implementation.

## Frontier relationship

Residual pressure becomes frontier pressure when it stops being locally sliceable as a compatibility-preserving ownership boundary and instead requires new evidence, evaluation criteria, or authority before implementation.

The transition pattern supported by `recovery_to_frontier_promotion_characterization.md` is:

```text
Recovery stops
↓
remaining pressure is classified
↓
unsupported / adjacent / already recovered pressure: move on
↓
repeated bounded future need connected to existing authority: frontier candidate
↓
frontier remains investigation/slice/audit scoped until implementation evidence justifies implementation
```

Examples:

- Projection Influence Lineage completed, but selective replay, dirty invalidation, cache dependency graphs, and read-model partial refresh remained frontier or adjacent pressure rather than another lineage slice.
- Read-Model Ownership completed, but dependency graph ownership became a recommended bounded audit because individual read-model lifecycle ownership was explicit while relationships among projected state, summaries, and derived indexes remained flat and repeated.
- Responsibility Recovery Evaluation Readiness found enough recovered architecture for a bounded read-only evaluation inquiry, but not for autonomous recovery, planning, semantic interpretation, or universal judgment.

Frontier pressure therefore preserves the pressure without over-promoting it into implementation.

## Counterexamples

### Compression without meaningful pressure

Repository evidence supports possible compression that does not justify recovery:

- Projection Influence Lineage still uses conservative full replay and full finalization. Replay assessment always requiring replay and selection always choosing full replay/finalization are limitations, but the audit treats them as compatibility behavior rather than same-family ownership compression.
- Read-Model Ownership notes direct save/decode operations in state-summary debug timing. That compression exists for measurement visibility, but it is debug/timing instrumentation pressure, not a recurring read-model lifecycle boundary.
- A large local structure may carry compatibility fields through legacy accessors. If the old shape is preserved only as an adapter over separated owners, the compression is compatibility surface, not active pressure.

Conclusion: compressed code shape is not enough. Pressure requires responsibility plurality whose hidden boundary affects reasoning, tests, evolution, or authority.

### Pressure without implementation compression

Repository evidence supports pressure signals that do not yet prove implementation compression:

- Operator pain is a pressure signal but not root-cause authority. The slow state-build experience oriented inquiry, while instrumentation was needed to find implementation cause.
- Evidence Interpretation and Responsibility Evaluation investigations found cross-cutting competencies and repeated review patterns, but explicitly rejected immediate implementation families without a concrete compression point, shared API, compatibility surface, or failing behavior.
- Frontier documents preserve unresolved pressure, but frontier status alone does not prove a local owner is compressed.

Conclusion: pressure can exist as inquiry, operational, or frontier pressure before it becomes implementation pressure.

### Recovery without relieving pressure

No strong evidence was found that completed responsibility recoveries failed to relieve their selected pressure. However, several recoveries left residual pressure by design:

- Projection Influence Lineage relieved lineage-chain compression but left selective replay and read-model/cache pressure.
- Read-Model Ownership relieved individual read-model lifecycle compression but left dependency graph, cache invalidation, timing visibility, and read-model selection pressure.
- Observation-Derived Capability relieved inventory/operation-contract compression but left operation selection prerequisites outside the slice.

Conclusion: recovery can relieve selected implementation pressure without eliminating all adjacent pressure. That is not failure if completion audit classifies the remainder accurately.

## Supported methodology

Repository evidence supports this pressure lifecycle:

```text
Compression
↓
Implementation Pressure
↓
Recovery
↓
Boundary / Handoff
↓
Slice
↓
Pressure Relief
↓
Completion Audit
↓
Residual Pressure Classification
↓
Move On or Frontier Preservation
```

Supported rules:

1. Start from implementation evidence, not vocabulary.
2. Identify one compressed owner or corridor.
3. Recover one boundary at a time.
4. Preserve compatibility.
5. Make the handoff independently visible.
6. Prove behavior and boundary through tests or audits.
7. Classify residual pressure.
8. Stop when remaining pressure changes ownership family.
9. Promote to frontier only when pressure is bounded, recurring, connected to authority, and not yet implementation-ready.

## Unsupported methodology

Repository evidence does not support:

- redesigning methodology around pressure vocabulary;
- implementing a pressure engine, planner, schema, or workflow;
- treating operator pain as implementation direction;
- treating recurring words as repository knowledge;
- implementing cross-family abstractions merely because handoff grammar recurs;
- continuing slices after same-family compression is gone;
- treating all residual pressure as frontier pressure;
- treating all frontier pressure as implementation-ready;
- assuming compression always creates meaningful architectural pressure;
- assuming pressure cannot exist outside implementation compression.

## Answers to the explicit questions

### 1. What is the strongest implementation-backed definition of architectural pressure?

Architectural pressure is behaviorally real responsibility plurality compressed inside one implementation owner or corridor, where the hidden boundary prevents independent reasoning, implementation, testing, evolution, authority assignment, or completion.

### 2. What observable implementation evidence creates pressure?

Overloaded methods, report shapes, inventory aggregators, cache/build corridors, hidden projection chains, repeated manual reconstruction, completion-audit residuals, and measured operational pain after it is connected to implementation evidence.

### 3. How does recovery relieve pressure?

Recovery relieves pressure by selecting one compressed boundary, creating or naming a local owner/handoff, preserving public compatibility, proving behavior, and classifying remaining pressure.

### 4. How is residual pressure classified?

As active, partially resolved, residual, historical, orphaned, adjacent, unsupported, or frontier pressure based on reconstruction frequency, relationship preservation, ownership family, evidence sufficiency, and connection to future bounded work.

### 5. When does residual pressure become a Frontier rather than another Slice?

When no same-family implementation compression remains, but a bounded recurring future need remains connected to existing authority and insufficient evidence. Frontier pressure is preserved for investigation, not implemented as the next local slice by default.

### 6. Does repository evidence support pressure as the driving invariant of architectural recovery?

Yes, with scope. The invariant is implementation pressure caused by compressed ownership, not pressure as generic pain, vocabulary, or desire. Completed families repeatedly start from compression, recover one boundary, relieve pressure, then stop or preserve residual pressure.

### 7. What implementation or documentation disproves that claim?

Nothing disproves the scoped claim for completed architectural recovery. But several documents disprove stronger versions: operator pressure is not implementation authority; Evidence Interpretation and Responsibility Evaluation are competencies without implementation compression; completed families leave residual pressure that should not automatically become another slice; and frontiers can originate from broader architectural pressure rather than a completed recovery.

## Confidence

Confidence is **high** that compressed ownership is the strongest implementation-backed cause of architectural recovery in this repository.

Confidence is **medium-high** that the pressure lifecycle above is the recurring methodology, because it appears across multiple completed families and completion audits.

Confidence is **medium** for pressure classifications outside implementation compression, because exploratory pressure documents are more observational and less executable than slice reports and completion audits.

Confidence is **low** for any universal abstraction, runtime pressure model, or automated selector. Repository evidence explicitly rejects those stronger claims.

## Recommendation

Adopt this characterization as documentation only. Do not implement new tooling, schema, diagnostics, workflow enforcement, or methodology automation from it.

Use the definition as a review lens for future recovery work:

```text
Find the compressed owner.
Prove the bounded responsibilities are behaviorally present.
Recover one local handoff.
Preserve compatibility.
Test the boundary.
Classify residual pressure.
Stop on ownership-family change.
```

If future work finds pressure without implementation compression, treat it as inquiry or frontier pressure until repository evidence identifies a local owner. If future work finds compression without pressure, preserve it as a counterexample rather than forcing a slice.
