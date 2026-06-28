# Architectural Recoverability Inquiry Audit

## Scope

This is a bounded implementation audit. It does not implement a runtime surface, CLI flag, diagnostic, registry, planner, priority engine, automatic slice generator, architecture registry, recoverability registry, manual scoring system, metadata database, or another projection slice.

The question is whether Seed already contains enough repository evidence to answer:

```text
Is this architectural distinction
recoverable
from implementation evidence?
```

before asking:

```text
Should this become
the next projection slice?
```

Repository authority wins. This audit treats implementation slices, existing inquiry audits, investigations, tests named by those artifacts, and implementation owners named by those artifacts as evidence. It does not treat conversation history, architectural preference, operator memory, or presentation vocabulary alone as authority.

## Short answer

Yes, partially and boundedly.

Recoverability has become an implementation-backed inquiry in the current architectural-projection lineage, but it is not yet a runtime surface and it is not a universal architecture oracle.

Seed can already determine whether a candidate architectural distinction is recoverable when repository evidence can show all of the following:

```text
candidate distinction
supporting implementation owner or call path
current compressed ownership
observable compatibility-preserving separation path
tests, generated architecture output, or existing audit evidence that can preserve behavior
boundary showing why this is implementation evidence rather than vocabulary preference
```

That recoverability check naturally precedes visibility inquiry. The existing projection slices did not begin by asking what should be projected next in the abstract. They repeatedly began by recovering a boundary and implementation evidence, then asking where that already-recovered boundary remained invisible in implementation.

The recurring methodology is therefore better described as:

```text
Recoverability

↓

Visibility

↓

Inquiry

↓

Architectural Projection Slice
```

rather than as a remembered architectural principle. The limitation is that Seed currently answers this by reading repository artifacts and implementation, not by a dedicated `seed` inquiry command.

## Evidence reviewed

This audit reviewed repository-local evidence only:

- `architectural_visibility_gap_inquiry_audit.md`.
- `architectural_inquiry_orientation_surface_audit.md`.
- `responsibility_family_completion_inquiry_audit.md`.
- `inquiry_lineage_architectural_projection_slice_methodology.md`.
- `incremental_state_evolution_architecture_investigation.md`.
- `operational_responsibility_slice_001.md` through `operational_responsibility_slice_006.md`.
- `execution_visibility_slice_001.md` through `execution_visibility_slice_005.md`.
- `observation_derived_capability_slice_001.md` through `observation_derived_capability_slice_005.md`.
- `answer_composition_slice_001.md` through `answer_composition_slice_004.md` and `architectural_orientation_answer_composition_slice_001.md` as later slice-family countercheck evidence.

## What recoverability means in current repository terms

A distinction is recoverable when the repository can derive it from implementation evidence before any projection work is attempted.

Recoverability is stronger than noticing a useful label. The label must be anchored in implementation evidence such as:

- a function, class, helper, dataclass, service, event path, projection stage, diagnostic report, or read model that already owns part of the distinction;
- a call site or data shape where two responsibilities are currently compressed;
- a bounded compatibility-preserving separation that can make one boundary explicit;
- tests or generated architecture evidence capable of proving behavior did not change;
- a reason the distinction belongs to implementation and not only to presentation vocabulary.

Recoverability is weaker than implementation. A recoverable distinction may still be invisible, unprojected, or not selected. It only means Seed can answer that the distinction is grounded enough to become the subject of a visibility or projection inquiry.

## Relationship between recoverability, visibility, inquiry, and projection slices

The repository evidence supports this ordering:

```text
Recoverability
    Can implementation evidence show that the distinction exists?

Visibility
    Is the recovered distinction currently explicit or invisible/compressed in implementation?

Inquiry
    Is the invisible/compressed recovered distinction bounded enough to ask as a read-only question?

Projection Slice
    Is there exactly one compatibility-preserving implementation change that can make the boundary explicit and stop?
```

This differs from choosing a slice through architectural intuition. A slice becomes justified only after the distinction has crossed recoverability and visibility checks.

## Determination matrix

| Determination | Answer | Reason | Supporting implementation evidence | Boundary | Limitations |
| --- | --- | --- | --- | --- | --- |
| Recoverability status | Yes, boundedly derivable. | Existing successful slices repeatedly start with a recovered boundary plus implementation evidence before making a change. | The lineage methodology names the recurring pattern as recovering a boundary, recovering implementation evidence, identifying compressed ownership, making one boundary explicit, preserving compatibility, and stopping. The family completion audit lists recovered chains with concrete owners such as `ToolValidationService.select_operation()`, `ToolExecutionPolicyService.evaluate_with_state_factory()`, `ExecutionStatusEmitter`, `ObservationIngestionDiagnostics`, `_ExecutableOperationContractState`, and `_CapabilityInventorySources`. | Recoverability applies only to distinctions with implementation owners or compressed call paths. | No dedicated runtime command currently composes recoverability status. Arbitrary vocabulary remains unsupported. |
| Supporting implementation evidence | Yes. | The repository contains repeated evidence structures: selected boundary, implementation evidence, before/after separation, files changed, tests executed, generated architecture output, and remaining compressed boundaries. | Slice reports for operational responsibility, execution visibility, and observation-derived capability preserve those sections. The completion audit summarizes the implementation owners and tests named by those slices. | Evidence must be repository-local and implementation-backed. | Reports are structured prose, not a machine-readable recoverability schema. |
| Visibility status | Yes, after recoverability. | Visibility audits can determine whether a recovered boundary is explicit or still compressed because slices and audits name implementation owners and remaining compressed ownership. | The visibility gap audit distinguishes implemented recovered boundaries from remaining compressed boundaries across operational responsibility, execution visibility, and observation-derived capability. | Visibility is about recovered architecture that is implementation-invisible, not about inventing new architecture. | Visibility cannot be evaluated for a distinction that has not first been recovered from implementation evidence. |
| Inquiry readiness | Yes, when repeated recoverable distinctions expose a bounded question. | The repository already formed read-only inquiry candidates from implementation-backed slice evidence: family completion, orientation, and visibility gaps. | The responsibility-family completion audit derives status from slice families. The orientation audit derives active family, current boundary, implemented boundaries, remaining compressed boundaries, stopping point, confidence, and recommended next inquiry from existing artifacts. | Inquiry readiness supports a read-only question, not a planner or work queue. | Existing answers require reading repository evidence manually. A future surface would need to compose evidence without storing manual state. |
| Projection-slice readiness | Yes, but only after recoverability and visibility. | Successful projection slices select one recovered boundary, make one implementation-local boundary explicit, preserve behavior, and stop. | Latest slices show terminal examples: execution recording separated from post-execution knowledge extraction, state-build visibility separated from projection-cache diagnostics, and capability inventory separated from executable operation contract metadata. | Slice readiness requires one boundary and one compatibility-preserving implementation change. | Remaining compressed boundaries are not automatically next slices; they still need recoverability and visibility checks. |

## Supporting implementation evidence by family

### Operational Responsibility

Recoverable operational distinctions are supported because the implementation already exposed a repeated chain of owners and handoffs:

```text
Capability Recommendation != Operation Selection
Operation Selection != Registered Operation Validation
Registered Operation Validation != Policy Authorization
Policy Authorization != Execution Realization
Execution Realization != Execution Recording
Execution Recording != Post-Execution Knowledge Extraction
```

The recoverability evidence is not the vocabulary alone. It is the implementation ownership summarized in the completion audit: `ToolRegistry`, `ToolNeedService` / `_CapabilityResolution`, `ToolValidationService.select_operation()`, `ToolExecutionPolicyService.evaluate_with_state_factory()`, `ToolExecutor._realize_registered_operation()`, `ToolExecutor._execute_allowed_tool_call()`, and `ToolExecutor._extract_post_execution_knowledge()`.

Visibility then follows: some boundaries are now explicit, while pending-action creation vs policy denial routing, approved pending-action resumption vs fresh authorization, and RuntimeLoop-specific result recording vs evidence event-id collection remain compressed.

Projection-slice readiness was justified for the implemented chain because each distinction had both an implementation owner and a compatibility-preserving separation path. It is not justified for the remaining compressed boundaries until they are individually recovered as bounded distinctions.

### Execution Visibility

Recoverable execution-visibility distinctions are supported by a chain of status, timing, cache, diagnostic, and state-build responsibilities:

```text
Status Emission != Status Consumption
Execution Status != Execution Timing
Execution Timing != Cache Visibility
Execution Visibility != Execution Diagnostics
State Build Visibility != Projection Cache Diagnostics
```

The recoverability evidence includes `ExecutionStatusEmitter`, `ExecutionStatusConsumer`, observation ingestion diagnostics, cache-debug shape, state-summary cache debug reporting, projection timings, projection counters, and tests preserving diagnostic output where behavior was touched.

Visibility inquiry naturally follows because the repository can identify remaining compressed evidence: projection build diagnostics through cache-building paths, cache status adjacent to replay/build timing, fact-index timing adjacent to cache-status reporting, knowledge-reachability metadata carrying cache visibility and timing together, and progress cadence timing mixed with status throttling.

This family is the clearest evidence that recoverability precedes visibility. The distinction must first be recoverable from implementation status/timing/cache paths before the repository can say it is implementation-invisible.

### Observation-Derived Capability

Recoverable capability distinctions are supported by a chain that separates observed evidence, verification, promotion readiness, inventory, and executable operation contract metadata:

```text
Observed Evidence != Executable Operation Contract
Observed Evidence != Capability Verification
Capability Verification != Capability Promotion
Capability Promotion != Capability Inventory
Capability Inventory != Executable Operation Contract
```

The recoverability evidence includes `CapabilityCandidate`, verification-evidence acquisition, `build_capability_verification_inspection()`, `build_capability_promotion_readiness_inspection()`, `build_capability_inventory()`, projected `capability_verified` facts, `_ExecutableOperationContractState`, and `_CapabilityInventorySources`.

The current boundary is important: this evidence supports a read-only observation-derived capability chain. It does not support claiming a complete writable capability-promotion lifecycle, because durable verification fact creation and promotion/admission authority remain outside the implemented read-only path.

### Incremental State Evolution countercheck

The incremental state investigation shows a useful non-slice example. It recovers several distinctions from implementation evidence without implementing a projection slice:

```text
append-only event authority
snapshot-plus-tail replay
dependent read-model cache invalidation
affected scope
projection dependency
incremental read model
dirty scope
```

The investigation also draws boundaries around unsupported conclusions: there is no per-subject dirty set, no declared projection dependency graph, no partial answer refresh, and no partial recomputation engine. That is recoverability behavior: the report can say which distinctions are implementation-recoverable and which remain only suggested or unsupported.

This is evidence that recoverability can be an inquiry before visibility and before projection. The investigation asks what current implementation supports, then refuses to promote unsupported vocabulary into architecture.

## Counterexamples and failure modes

The repository evidence also shows where projection should not proceed.

### Conversation history is not evidence

A distinction is not recoverable merely because recent implementation work or conversation names it. The audits repeatedly reject operator memory and preferred labels as authority. The required authority is implementation evidence.

### Presentation vocabulary is not evidence

Terms that appear in output, docs, or operator-facing presentation are not automatically repository knowledge. The AGENTS instructions explicitly warn that presentation labels such as continuation, current work position, source navigation, active edge, storage topology, state build, and projection cache may exist only as visibility or presentation labels unless implementation evidence proves reachability.

### Remaining compressed boundaries are not automatic slices

Latest slice reports list remaining compressed boundaries, but those lists are not a planner. They are counterexamples and future investigation candidates. Each candidate must still pass recoverability and visibility checks before it can justify a projection slice.

### Whole-domain completion remains unsupported

Family completion is bounded to recovered chains. The repository does not support declaring all operational responsibility, all execution visibility, all capability lifecycle behavior, or all incremental state architecture complete.

### Manual inspiration is insufficient

Projection slices that depended only on architect intuition, manual inspiration, unstated reasoning, or non-recoverable distinctions would fail the recurring slice pattern. The existing methodology requires implementation evidence before a boundary becomes slice material.

## Has recoverability become another implementation-backed inquiry?

Yes, boundedly.

Recoverability has the same shape as the other implementation-backed inquiries that emerged from slice evidence. It can ask:

```text
Is this distinction recoverable from implementation evidence?
What implementation owner or call path supports it?
Where is the ownership compressed?
What compatibility boundary would have to remain unchanged?
What evidence would prove the distinction is not merely vocabulary?
What unsupported conclusions must be excluded?
```

That is an inquiry, not a registry. It is read-only, evidence-composing, and bounded by repository authority.

## Does recoverability naturally precede visibility inquiry?

Yes.

The visibility question is meaningful only after the distinction has been recovered. Otherwise Seed would be asking whether an invented or preferred distinction is visible. The architectural visibility gap audit already implies this boundary by asking where recovered architecture remains implementation-invisible, not where any desired architecture is missing.

The supported order is:

```text
recoverable distinction

↓

visible or invisible distinction

↓

active inquiry

↓

projection slice readiness
```

## Can projection slices now be justified through recoverability rather than architectural intuition?

Yes, for bounded slices in the current lineage.

The existing successful projection slices can be justified without appealing to intuition because they all exhibit:

- one recovered boundary;
- concrete implementation evidence;
- current compressed ownership;
- one compatibility-preserving implementation change;
- tests or generated architecture output preserving behavior;
- a stop condition.

However, recoverability does not choose priority, generate designs, or prove that a candidate must be implemented next. It only proves that a candidate distinction is grounded enough to become a visibility or projection inquiry.

## Supported conclusions

- Recoverability is now an implementation-backed inquiry in the current architectural-projection lineage.
- Recoverability naturally precedes visibility inquiry, because visibility gaps require already-recovered architecture.
- Existing projection slices can be justified through implementation recoverability rather than architectural intuition.
- The recurring methodology is now better represented as `Recoverability -> Visibility -> Inquiry -> Projection Slice`.
- Seed can determine recoverability manually from existing repository artifacts and implementation evidence for the responsibility-family slice lineage.
- Incremental state evolution shows recoverability can produce supported and unsupported conclusions without immediately producing a projection slice.
- A future recoverability inquiry should be read-only and evidence-composing if implemented.

## Unsupported conclusions

- Seed cannot currently answer recoverability through a dedicated CLI or runtime surface.
- Seed cannot determine recoverability for arbitrary architecture vocabulary without implementation evidence.
- Seed cannot use presentation terms as preserved knowledge unless implementation reachability proves them.
- Seed should not add a planner, priority engine, automatic slice generator, architecture registry, recoverability registry, manual scoring system, or metadata database.
- Seed cannot claim all remaining compressed boundaries are projection-slice-ready.
- Seed cannot claim whole-domain architectural completion from bounded recovered chains.

## Recommended next implementation step

Do not implement another projection slice solely from this audit.

The next implementation-backed step, if work continues, should be a read-only recoverability inquiry surface that composes existing repository evidence and answers one bounded question:

```text
Is this candidate architectural distinction recoverable from implementation evidence?
```

It should report:

```text
recoverability status
supporting implementation evidence
visibility status
inquiry readiness
projection-slice readiness
boundaries and limitations
```

It must not store manual recoverability state, rank future work, generate slices, introduce a registry, or mutate cluster truth. If implemented as a diagnostic or recordable surface, it must follow the repository diagnostic visibility contract and prove inventory, shape-audit, record-scope, event-ledger, and `mutates_cluster=false` behavior.
