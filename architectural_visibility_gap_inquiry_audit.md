# Architectural Visibility Gap Inquiry Audit

## Scope

This is a bounded implementation audit. It does not implement a runtime surface, CLI, registry, status database, priority list, planner, metadata store, or manually maintained architectural state.

The question is whether Seed already contains enough repository evidence to answer:

```text
Where is recovered architecture
still implementation-invisible?
```

Repository authority wins. This report treats implementation slices, existing inquiry audits, generated architecture evidence referenced by those audits, and tests named by those artifacts as evidence. It does not treat operator memory, preferred vocabulary, or conversation history as authority.

## Short answer

Yes, partially and boundedly.

Seed already exposes enough implementation evidence to identify architectural visibility gaps inside the existing responsibility-family projection work. The evidence is strongest for families that have repeated compatibility-preserving slices:

```text
Operational Responsibility
Execution Visibility
Observation-Derived Capability
```

For those families, Seed can derive:

```text
recovered boundary
implementation owner
visibility status
remaining compressed ownership
implementation evidence
confidence
```

from existing slice reports and audits without introducing a new manual queue or architectural registry.

However, Seed cannot yet answer this automatically through a dedicated inquiry surface, and it cannot derive visibility gaps for arbitrary architectural vocabulary that has not crossed into implementation-backed slice evidence.

## Evidence reviewed

This audit reviewed repository-local implementation artifacts only:

- `operational_responsibility_slice_001.md` through `operational_responsibility_slice_006.md`.
- `execution_visibility_slice_001.md` through `execution_visibility_slice_005.md`.
- `observation_derived_capability_slice_001.md` through `observation_derived_capability_slice_005.md`.
- `incremental_state_evolution_architecture_investigation.md`.
- `inquiry_lineage_architectural_projection_slice_methodology.md`.
- `responsibility_family_completion_inquiry_audit.md`.
- `architectural_inquiry_orientation_surface_audit.md`.

## What counts as architectural visibility evidence?

A visibility gap is implementation-backed when the repository shows all of the following:

1. A recovered architectural boundary already named by an implementation slice or audit.
2. A concrete implementation owner or call path where that boundary is currently explicit or compressed.
3. A compatibility-preserving implementation change, or a remaining-compression note produced by such a change.
4. Tests, generated architecture output, or diagnostic inventory evidence referenced by the slice when the change touched runnable or diagnostic behavior.
5. A reason the boundary is visibility work rather than a new domain concept.

A visibility gap is not implementation-backed when it depends on:

- operator intuition;
- conversation memory;
- unstated architectural preference;
- presentation vocabulary alone;
- a manually maintained future-work list;
- a label that has no implementation owner.

## Family 1: Operational Responsibility

### Implemented recovered boundaries

The repository already identifies an implemented operational chain:

```text
Capability Recommendation != Operation Selection
Operation Selection != Registered Operation Validation
Registered Operation Validation != Policy Authorization
Policy Authorization != Execution Realization
Execution Realization != Execution Recording
Execution Recording != Post-Execution Knowledge Extraction
```

Implementation owners are visible in the slice reports and completion audit:

- `ToolNeedService` and `_CapabilityResolution` own capability-resolution payload assembly while separating provider/handoff advisory metadata from registry-derived registered operation candidates.
- `ToolValidationService.select_operation()` owns operation selection and separates it from validation and recommendation concerns.
- `ToolExecutionPolicyService.evaluate_with_state_factory()` owns the validation-to-policy transition before execution.
- `ToolExecutor._realize_registered_operation()` owns registered callable realization and output validation.
- `ToolExecutor._execute_allowed_tool_call()` owns allowed-call event recording.
- `ToolExecutor._extract_post_execution_knowledge()` owns the post-completion knowledge-extraction handoff.

### Remaining compressed boundaries

Operational visibility gaps already emerge from slice evidence. The family completion audit preserves active compression around:

```text
Pending-action creation != Policy denial routing
Approved pending-action resumption != Fresh call authorization
Policy outcome recording != Pending-action lifecycle ownership
RuntimeLoop tool-result recording != RuntimeLoop evidence event-id collection
Action-plan top-provider choice != Operation selection
```

These are not a manual backlog. They are implementation-backed counterexamples to declaring the whole operational domain complete.

### Implementation-visible ownership

Ownership is implementation-visible where a private helper, service method, or service boundary now carries one responsibility:

- `_CapabilityResolution` makes recommendation payload ownership separable from registered operation candidate ownership.
- `ToolValidationService.select_operation()` makes selected registered operation ownership explicit.
- `ToolExecutionPolicyService` makes authorization ownership explicit before execution realization.
- `_realize_registered_operation()` makes callable realization explicit apart from event recording.
- `_extract_post_execution_knowledge()` makes extraction handoff explicit apart from completion recording.

### Implementation-invisible ownership

Ownership remains implementation-invisible where remaining-compression notes point to adjacent responsibilities still sharing one corridor or lifecycle:

- denial routing and pending-action creation;
- approved resume and fresh authorization;
- policy outcome recording and pending-action lifecycle;
- RuntimeLoop result recording and event-id collection;
- action-plan provider choice and operation-selection semantics.

### Confidence

High for the implemented recovered chain. Medium for broader operational visibility gaps, because the remaining compression is concrete and implementation-backed but not yet projected into one selected next slice.

## Family 2: Execution Visibility

### Implemented recovered boundaries

The repository already identifies an implemented execution-visibility chain:

```text
Status Emission != Status Consumption
Execution Status != Execution Timing
Execution Timing != Cache Visibility
Execution Visibility != Execution Diagnostics
State Build Visibility != Projection Cache Diagnostics
```

Implementation owners are visible in slice reports and the completion audit:

- `ExecutionStatusEmitter` owns producer-side status emission.
- `ExecutionStatusConsumer` owns consumption.
- observation ingestion diagnostics own timing rows and phase timing.
- cache visibility paths own cache labels and cache status.
- current-facts cache debug remains a read-only diagnostic surface.
- state-build visibility fields are separated from projection-cache diagnostic fields while preserving cache-debug shape.

### Remaining compressed boundaries

Execution-visibility gaps already emerge from repository evidence:

```text
Projection build diagnostics still pass replay/build phase evidence through cache-building paths
Projection cache status emission still meets projection replay/build timing at some cache call sites
Fact-index cache lookup/load timing remains adjacent to cache-status reporting
Knowledge-reachability metadata still carries cache visibility and timing fields together
Progress cadence timing remains mixed with status-emission throttling
```

These gaps answer the central question directly: recovered visibility distinctions exist, but some still remain compressed inside implementation paths that also do neighboring operational work.

### Implementation-visible ownership

Ownership is implementation-visible where status, timing, cache, diagnostic, and state-build responsibilities are now separated by concrete helpers or surfaces:

- emitter versus consumer;
- status versus phase timing;
- timing rows versus cache visibility labels;
- read-only diagnostic shape versus state mutation;
- state-build visibility versus projection-cache diagnostics.

### Implementation-invisible ownership

Ownership remains implementation-invisible where implementation paths still carry multiple visibility responsibilities together:

- projection replay/build timing through cache-building paths;
- cache status and replay/build timing at shared call sites;
- fact-index cache timing and cache-status reporting;
- knowledge-reachability cache visibility and timing metadata;
- progress cadence timing and status-emission throttling.

### Confidence

High for the implemented execution-visibility chain. Medium-high for visibility-gap inquiry as a natural next inquiry, because this family is itself visibility-oriented and its remaining compression is already expressed as visibility ownership gaps.

## Family 3: Observation-Derived Capability

### Implemented recovered boundaries

The repository already identifies an implemented observation-derived capability chain:

```text
Observed Evidence != Executable Operation Contract
Observed Evidence != Capability Verification
Capability Verification != Capability Promotion
Capability Promotion != Capability Inventory
Capability Inventory != Executable Operation Contract
```

Implementation owners are visible in slice reports and the completion audit:

- `CapabilityCandidate` and verification-evidence acquisition represent observed evidence without becoming executable operation contracts.
- verification inspection builders separate observed evidence payloads from verification-status interpretation.
- promotion-readiness inspection routes candidate evidence through verification payloads before applying readiness decisions.
- capability inventory consumes admitted `capability_verified` projection facts rather than creating them.
- `_ExecutableOperationContractState` and `_CapabilityInventorySources` make executable contract metadata and inventory-source ownership visible.

### Remaining compressed boundaries

Observation-derived capability gaps already emerge from repository evidence:

```text
Promotion-readiness inspection != Future durable capability_verified fact creation
Verification evidence acquisition != Verification fact authority
Capability inventory construction != Inventory consumers
Provider-reported capability state != Independently verified capability state
Registered operation contract derivation remains represented by ToolSpec capability metadata rather than a public contract-derivation API
```

These are visibility gaps because the repository already distinguishes the responsibilities, but some ownership is still compressed inside read-only inspection, inventory, provider-state, or ToolSpec metadata paths.

### Implementation-visible ownership

Ownership is implementation-visible where evidence, verification, promotion readiness, inventory, and executable operation contract metadata are represented by separate builders or private state objects.

### Implementation-invisible ownership

Ownership remains implementation-invisible where future authority, consumer boundaries, independent verification state, or contract derivation are still represented indirectly by neighboring structures rather than an explicit implementation boundary.

### Confidence

High for the implemented read-only observation-derived chain. Medium for future writable or authority-changing gaps, because the current repository intentionally keeps promotion readiness and inventory read-only.

## Relationship to incremental state evolution

The incremental state investigation strengthens the visibility-gap hypothesis without creating a new slice. It shows that Seed already separates preserved event authority, projected state, projection cache behavior, dependent read models, execution/status visibility, observation/fact projection, and presentation composition.

It also identifies current global rebuild assumptions and remaining implementation gaps. Those gaps are not necessarily responsibility-family projection slices by themselves, but they show the same pattern:

```text
existing capability exists
architectural distinction exists
implementation visibility is partial
next work should make one boundary observable without changing authority
```

The strongest visibility evidence from that investigation is that execution status/progress emission is operational visibility, not State authority, and that affected scope and projection dependency can be recovered from current implementation. This supports visibility inquiry as read-only and evidence-derived, not as a planner.

## Relationship to architectural inquiry orientation

The architectural inquiry orientation audit already concluded that Seed can derive architectural self-orientation for bounded responsibility-family slices, including active family, current boundary, implemented boundaries, remaining compressed boundaries, natural stopping point, confidence, and next inquiry candidate.

Architectural Visibility Inquiry is narrower than architectural self-orientation:

- Self-orientation asks where Seed is within architectural evolution.
- Family completion asks whether a recovered family chain is complete.
- Visibility inquiry asks which recovered architectural distinctions remain compressed inside implementation.

The new inquiry therefore naturally emerges from existing orientation evidence, but it should not supersede it. It would consume the same repository evidence and answer a more specific question.

## Can Seed derive the requested fields today?

### Recovered boundary

Yes, for existing slice families. Recovered boundaries are named in slice reports and summarized by the family completion audit.

No, for arbitrary vocabulary that only appears in prose or presentation labels.

### Implementation owner

Yes, when a slice identifies the service, helper, method, builder, diagnostic, or read-only surface that owns the visible boundary.

Partially, when a remaining-compression note names a call path but does not yet isolate a single owner.

### Visibility status

Yes, by classifying boundaries as:

- implemented and visible;
- remaining compressed;
- unsupported by implementation evidence.

### Remaining compressed ownership

Yes, for the three responsibility families. Latest slice reports and the completion audit list concrete remaining compression.

No, as an exhaustive repository-wide map. There is no automatic derivation surface yet.

### Implementation evidence

Yes, because slice reports record implementation evidence, before/after compression, compatibility preservation, files changed, and tests or generated evidence.

### Confidence

Yes, boundedly. Confidence can be derived from evidence quality:

- high when a boundary has a completed compatibility-preserving slice and tests;
- medium when compression is concrete but not selected as a slice;
- low or unsupported when the term is only investigation prose or presentation vocabulary.

## Does Architectural Visibility Inquiry naturally emerge?

Yes.

A read-only Architectural Visibility Inquiry naturally emerges because existing artifacts already answer the core shape:

```text
visibility gap
reason
supporting implementation evidence
affected responsibility family
candidate next projection slice
```

without requiring manual tracking.

The inquiry would not recover architecture. It would inspect already recovered and implementation-backed boundaries, then identify which distinctions remain compressed inside implementation owners.

The inquiry should remain read-only. It should not create a priority list, planner, status registry, manual queue, metadata database, or new architectural state.

## Can the next architectural projection slice be derived from visibility evidence?

Yes, but only within a bounded family and only as a candidate.

The repository can derive candidate next slices from remaining-compression evidence. For example:

- Operational Responsibility points toward pending-action lifecycle boundaries.
- Execution Visibility points toward projection/fact-index/cache timing and status boundaries.
- Observation-Derived Capability points toward verification authority, provider-reported versus independently verified state, or operation-contract derivation boundaries.

The repository cannot yet choose a single global next slice without a repository-visible selector or inquiry scope. Choosing between families can still require operator intent unless a future read-only inquiry surface is explicitly scoped by family or by the strongest current evidence.

Therefore the next projection slice can be derived from visibility evidence after scope selection, but Seed should not pretend that global prioritization is implementation-backed today.

## Counterexamples and limitations

The audit found several places where identifying the next slice can still depend on operator input:

1. **Cross-family choice.** Existing evidence names multiple viable visibility gaps across three families. Selecting Operational Responsibility versus Execution Visibility versus Observation-Derived Capability is not determined by evidence alone.
2. **Adjacent-family boundaries.** Remaining compression often points outside a completed recovered chain. Calling it the next slice requires choosing a new bounded family.
3. **Investigation prose without slice implementation.** Incremental state evolution has strong architecture evidence, but not every stated gap has the same slice-backed status as the three completed families.
4. **Vocabulary instability.** Terms such as architectural visibility, work orientation, family completion, or projection status should not become repository authority merely because they name a useful report.
5. **No automatic surface.** Existing documents make the answer derivable, but Seed does not yet expose a stable read-only command or diagnostic that composes visibility gaps.

These counterexamples do not defeat the inquiry. They define its boundary: it can report evidence-backed visibility gaps, not choose all future work autonomously.

## Supported conclusions

- Seed can determine where recovered architecture remains implementation-invisible for the existing responsibility-family slice sequences.
- Visibility gaps already emerge from implementation evidence, especially from `Remaining compressed ... boundaries` sections in slice reports and from family completion/orientation audits.
- Implementation-visible ownership can be identified where slices introduced or named concrete owners such as services, private helpers, builders, diagnostic surfaces, or read-only inquiry paths.
- Implementation-invisible ownership can be identified where recovered boundaries remain compressed inside adjacent call paths or compatibility structures.
- Architectural Visibility Inquiry is a natural read-only inquiry over existing evidence.
- Visibility should become an inquiry surface only if it composes repository evidence; it should not become a manually remembered principle or manual state store.

## Unsupported conclusions

- Seed cannot claim all architectural visibility gaps are known repository-wide.
- Seed cannot select one global next projection slice without scoped intent or a repository-visible selector.
- Seed cannot treat presentation vocabulary as implementation evidence.
- Seed cannot infer a boundary is recovered merely because it appears in investigation prose.
- Seed should not implement a visibility registry, priority queue, planner, metadata database, or manual architectural status file.
- Seed should not treat visibility inquiry as authority to mutate cluster truth or diagnostic findings.

## Recommended next implementation step

Do not implement another responsibility slice yet.

The smallest implementation-backed next step is a read-only Architectural Visibility Inquiry surface that composes existing slice/audit evidence and reports, for a selected family or bounded set of families:

```text
recovered boundary
implementation owner
visibility status
remaining compressed ownership
implementation evidence
confidence
candidate next projection slice
```

If exposed as a diagnostic CLI or recordable output, that future implementation must follow the repository operational visibility contract: update diagnostic inventory, update diagnostic shape-audit specs, prove the surface appears in `seed --diagnostic-inventory`, prove it is checked by `seed --diagnostic-shape-audit`, preserve `record_scope=diagnostic_run` if recording, and prove read-only ledger writes remain `mutates_cluster=false`.

## Acceptance answers

### Can Seed determine where recovered architecture remains implementation-invisible?

Yes, within the existing responsibility-family projection evidence. It can identify implemented recovered boundaries, remaining compressed boundaries, implementation-visible ownership, implementation-invisible ownership, and confidence for Operational Responsibility, Execution Visibility, and Observation-Derived Capability.

### What implementation evidence supports that answer?

The evidence is the recurring slice corpus, family completion audit, architectural orientation audit, and incremental state investigation. Those artifacts name recovered boundaries, owners, compatibility-preserving implementation changes, tests, remaining compression, and unsupported claims.

### Does a read-only architectural visibility inquiry naturally emerge?

Yes. It naturally emerges as a composition of existing implementation-backed evidence. Its purpose would be to answer which recovered distinctions remain compressed inside implementation, not to recover new architecture or maintain a manual queue.

### Is visibility itself becoming an implementation-backed inquiry?

Yes, boundedly. Visibility is no longer only an architectural principle remembered by architects; the repository now contains enough repeated evidence to inquire into visibility gaps as implementation-backed facts. The inquiry remains bounded because it is strongest where slices and audits already exist.

### Can the next architectural projection slice be derived from visibility evidence rather than operator intuition?

Yes, after scope selection. Existing evidence can derive candidate next projection slices from remaining compressed ownership. It cannot yet select one global next slice across all families without operator intent or a repository-visible selector.

### Should visibility become another inquiry surface rather than an architectural principle remembered by architects?

Yes, if implemented as a read-only evidence composition surface. No, if that means creating manually maintained architectural state, a queue, planner, registry, or priority database.
