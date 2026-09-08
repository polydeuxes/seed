# Implementation Responsibility Family Stack Audit

## Scope

This is a bounded implementation audit. It does not recover another responsibility
family, perform implementation slices, propose runtime surfaces, or change CLI,
renderer, schema, JSON, event, or ledger behavior.

The central question is whether the repository can derive architectural
relationships between the completed implementation responsibility families using
implementation evidence.

Repository authority wins: this audit treats slice reports, completion audits,
existing implementation seams, and tests referenced by those reports as evidence.
It does not treat architectural preference, historical terminology, or operator
memory as authority.

## Evidence reviewed

Primary evidence:

- `responsibility_family_completion_inquiry_audit.md`
- `implementation_responsibility_family_inventory_audit.md`
- `answer_composition_family_completion_audit.md`
- `inquiry_lineage_family_vocabulary_audit.md`
- `architectural_inquiry_orientation_surface_audit.md`
- `architectural_orientation_answer_composition_audit.md`
- `implementation_evidence_primary_architectural_object_audit.md`
- `operational_responsibility_slice_001.md` through
  `operational_responsibility_slice_006.md`
- `execution_visibility_slice_001.md` through
  `execution_visibility_slice_005.md`
- `observation_derived_capability_slice_001.md` through
  `observation_derived_capability_slice_005.md`
- `answer_composition_slice_001.md` through `answer_composition_slice_004.md`
- `inquiry_lineage_slice_001.md` through `inquiry_lineage_slice_004.md`
- Implementation files named by those audits, including `seed_runtime/execution.py`,
  `seed_runtime/tool_validation.py`, `seed_runtime/tool_execution_policy.py`,
  `seed_runtime/tool_needs.py`, `seed_runtime/registry.py`,
  `seed_runtime/execution_status.py`, `seed_runtime/observation_sources.py`,
  `seed_runtime/capability_candidates.py`, `seed_runtime/capability_inventory.py`,
  `seed_runtime/operational_story.py`, and `seed_runtime/reference_selection.py`.

## Completed responsibility families

| Family | Completion status used by this audit | Bounded completion evidence |
| --- | --- | --- |
| Operational Responsibility | Implementation complete for the recovered chain. | Six slices separate recommendation, selection, validation, policy authorization, execution realization, execution recording, and post-execution knowledge extraction. |
| Execution Visibility | Implementation complete for the recovered chain. | Five slices separate status emission/consumption, timing, cache visibility, diagnostics, state-build visibility, and projection-cache diagnostics. |
| Observation-Derived Capability | Implementation complete for the read-only recovered chain. | Five slices separate observed evidence, verification, promotion readiness, inventory, and executable operation contract metadata. |
| Answer Composition | Implementation complete for the recovered answer-composition chain. | Four slices plus completion audit separate answer material, reasoning, support, boundary, and limitations across answer surfaces. |
| Inquiry Lineage | Completed bounded implementation slices, but family vocabulary remains less stable than the four named completion families. | Four slices separate result/choice/conclusion from the lineage that explains or bounds it; the fourth slice explicitly says cross-surface family vocabulary was not stabilized. |

## Implementation relationships

### Relationship summary

The implementation evidence supports a **composition graph with compatibility
handoffs**, not a strict universal layer cake.

The strongest supported flow is:

```text
Operational Responsibility
  produces completed execution records and post-execution evidence
  -> Observation-Derived Capability can inspect/project admitted capability evidence
  -> Operational Responsibility can consume executable operation contract metadata
     and registered capability labels for recommendation/selection/execution
```

A second supported flow is:

```text
Operational Responsibility / Projection / Diagnostics / Inquiry Surfaces
  produce records, status, facts, cache/timing data, answers, choices, and conclusions
  -> Execution Visibility, Answer Composition, and Inquiry Lineage expose those
     records with responsibility-preserving boundaries
```

The evidence does **not** prove that every family sits above or below every other
family. Several families are intentionally orthogonal: Execution Visibility does
not own operational execution; Answer Composition does not own the underlying
facts or execution; Inquiry Lineage does not own answer correctness; and
Observation-Derived Capability does not own runtime operation realization.

## Per-family relationship analysis

### Operational Responsibility

| Field | Implementation-backed finding |
| --- | --- |
| Primary responsibility | Owns the registered-operation path from capability recommendation through operation selection, validation, policy authorization, execution realization, execution recording, and post-execution knowledge extraction. |
| Primary produced artifact | Tool-call lifecycle records, especially `tool.call.started`, `tool.call.completed`, failed/denied/pending results, and completed-event handoff to fact extraction. |
| Primary consumed artifact | Registered `ToolSpec` / `ToolRegistry` operation metadata, capability recommendations, selected operation name/arguments, policy state, and callable implementation output. |
| Upstream families | Observation-Derived Capability is upstream where admitted capability knowledge and executable operation contract labels inform capability inventory/recommendation context. Execution Visibility is not upstream for behavior; it observes status. |
| Downstream families | Observation-Derived Capability consumes completed execution evidence when post-execution facts become projected capability evidence. Execution Visibility observes status/diagnostics around execution. Answer Composition and Inquiry Lineage can describe operational results and lineage but do not execute them. |
| Orthogonal families | Answer Composition and Inquiry Lineage are orthogonal to operation realization: they explain, bound, or preserve choices/results rather than authorize or run tools. |
| Shared implementation boundaries | `ToolExecutor` is the cross-family handoff point where execution recording hands completed events to `FactExtractionService.observe_tool_result()` without making recording own knowledge extraction. Capability inventory/contract metadata touches operation selection through registered operation labels but does not own execution. |

Evidence strength: high for the recovered operational chain; medium for broader
operational architecture because pending action lifecycle and runtime-loop
compression remain explicitly outside the completed chain.

### Execution Visibility

| Field | Implementation-backed finding |
| --- | --- |
| Primary responsibility | Makes execution status, timing, cache state, state-build visibility, and diagnostic visibility observable without changing the operational behavior being observed. |
| Primary produced artifact | Status events/updates, timing rows, cache-debug rows, diagnostic inventory rows, diagnostic shape-audit rows, and read-only visibility reports. |
| Primary consumed artifact | Execution lifecycle transitions, observation ingestion phases, state-build/projection-cache metadata, current-facts cache status, and diagnostic registry/spec data. |
| Upstream families | Operational Responsibility and state/projection paths are upstream as sources of lifecycle and cache/timing material. Observation-Derived Capability can be upstream when capability diagnostics are visible surfaces. |
| Downstream families | Answer Composition may consume visibility evidence when explaining what is known, unsupported, or bounded. Inquiry Lineage may preserve why a visible result was selected or derived. |
| Orthogonal families | Execution Visibility is intentionally orthogonal to Operational Responsibility authority: observing status, timing, and diagnostics does not authorize, select, or execute operations. It is also orthogonal to Observation-Derived Capability admission: visibility does not by itself verify capability truth. |
| Shared implementation boundaries | Diagnostic inventory/shape-audit surfaces are shared compatibility boundaries for operational visibility. Cache/timing/status handoffs cross state-build and projection-cache ownership but preserve read-only diagnostic behavior. |

Evidence strength: high for visibility separation; medium for any claim that
visibility is a layer above all families, because several visibility surfaces are
sidecars to operational, projection, and diagnostic paths rather than a single
central stack layer.

### Observation-Derived Capability

| Field | Implementation-backed finding |
| --- | --- |
| Primary responsibility | Turns observed evidence into read-only capability candidates, verification/promotion readiness, capability inventory, and separated executable operation contract metadata. |
| Primary produced artifact | `CapabilityCandidate`, verification inspection rows, promotion readiness rows, capability inventory entries, admitted capability state, and executable operation contract state. |
| Primary consumed artifact | Projected facts such as admitted `capability_verified` facts, observed package/evidence facts, requested capability needs, and registered `ToolSpec` capability labels. |
| Upstream families | Operational Responsibility is upstream when completed tool execution produces evidence. Projection/state is upstream because admitted facts are consumed from projected state. |
| Downstream families | Operational Responsibility is downstream where operation recommendation/selection can use registered operation capability labels and inventory-like capability context. Answer Composition can explain capability readiness and limitations. |
| Orthogonal families | Execution Visibility is orthogonal unless a capability surface is being diagnosed; visibility does not admit capability knowledge. Inquiry Lineage is orthogonal unless explaining a selected capability conclusion or reference. |
| Shared implementation boundaries | Capability inventory is a compatibility handoff that intentionally unions admitted repository capability knowledge, requested capabilities, and executable operation contract labels. This union crosses observed-knowledge and registered-operation metadata ownership without collapsing them. |

Evidence strength: high for the read-only capability chain; medium for writable
promotion/admission lifecycle because writable verified fact creation and
admission writers remain outside the completed family.

### Answer Composition

| Field | Implementation-backed finding |
| --- | --- |
| Primary responsibility | Composes bounded answers by separating answer material, reasoning, support, boundary, and limitations before handing them into unchanged public answer surfaces. |
| Primary produced artifact | `OperationalStory` payloads, inquiry-orientation answer sections, answer JSON/text that includes answer, reasoning, supporting evidence, boundary, and unknowns/limitations. |
| Primary consumed artifact | Existing facts, diagnostics, inventory rows, inquiry artifacts, reasoning/selection evidence, operational story inputs, and repository authority boundaries. |
| Upstream families | Operational Responsibility, Execution Visibility, Observation-Derived Capability, and Inquiry Lineage can all be upstream as evidence sources or explanatory material. |
| Downstream families | Primarily operator-facing inquiry and presentation surfaces. It is not shown as downstream input to operation execution, capability admission, or diagnostic mutation. |
| Orthogonal families | Operational Responsibility is orthogonal because answer composition explains and bounds; it does not execute. Observation-Derived Capability is orthogonal because composed capability answers do not create admitted capability truth. Execution Visibility is orthogonal because answer text may consume visibility evidence but does not own status/timing production. |
| Shared implementation boundaries | Public answer compatibility objects such as `OperationalStory` remain stable while private payloads separate responsibility before handoff. Diagnostic and inquiry surfaces share answer/support/boundary/limitations vocabulary but do not prove a single runtime owner. |

Evidence strength: high for the answer-composition pattern; medium for claims that
answer composition consumes every family in a uniform way, because the evidence is
surface-specific.

### Inquiry Lineage

| Field | Implementation-backed finding |
| --- | --- |
| Primary responsibility | Separates a produced result, selection, conclusion, or reference choice from the lineage frame that explains how it was selected, derived, compared, bounded, or left incomplete. |
| Primary produced artifact | Private result/lineage payloads and public lineage surfaces such as reasoning-path audit, selection-path audit, reference selection, and related inquiry artifact visibility. |
| Primary consumed artifact | Candidate sets, selection factors, evidence paths, derived conclusions, alternative references, limitations, and authority boundaries. |
| Upstream families | Answer Composition is upstream when answer surfaces expose selected answer/result material. Execution Visibility and Observation-Derived Capability can be upstream when their outputs become selected conclusions or evidence paths. |
| Downstream families | Answer Composition can consume lineage as support/reasoning material. Operator-facing inquiry surfaces consume lineage to explain why a result is supported or bounded. |
| Orthogonal families | Operational Responsibility is orthogonal unless an operational result is being explained. Inquiry Lineage does not authorize operations, verify capabilities, or emit execution status. |
| Shared implementation boundaries | Public compatibility objects such as `ReferenceSelection` still combine choice, lineage, boundary, and mutation flags, while private payloads make choice/lineage handoff explicit. `projection_shape` remains a known compressed boundary where result and influence lineage still coexist. |

Evidence strength: high for the four recovered lineage boundaries; medium-low for
stabilized family naming, because `inquiry_lineage_slice_004.md` explicitly says
cross-surface family vocabulary remains insufficiently supported.

## Produced artifacts consumed by another family

Implementation-backed relationships:

1. **Completed operational execution records -> post-execution evidence / capability evidence.**
   Operational recording produces a durable completed event. Post-execution
   knowledge extraction consumes that event through `FactExtractionService`, and
   observation-derived capability surfaces later consume projected evidence or
   admitted capability facts.

2. **Registered operation contract labels -> capability inventory / operation context.**
   `ToolSpec` capability metadata is consumed by capability inventory as
   executable operation contract metadata. The same registered-operation metadata
   remains operational input for validation/selection/execution.

3. **Execution lifecycle/cache/timing data -> execution visibility diagnostics.**
   Status/timing/cache evidence is produced by execution, observation ingestion,
   state-build, and projection-cache paths, then consumed by visibility surfaces.

4. **Visibility, capability, operational, and inquiry evidence -> answer composition.**
   Answer surfaces consume existing implementation evidence, support, unknowns,
   and authority boundaries. The evidence supports consumption by specific answer
   surfaces, not a general claim that answer composition owns all upstream outputs.

5. **Answer/result/reference choices -> inquiry lineage.**
   Selection-path, reasoning-path, and reference-selection slices show produced
   selected results or choices being paired with separate lineage material.

Plausible but not fully proven relationships:

- A universal flow from Observation-Derived Capability into Operational
  Responsibility for every operation. Evidence supports capability labels and
  registered contract metadata, but operation execution still depends on
  `ToolRegistry`, validation, and policy rather than admitted capability facts
  alone.
- A universal flow from Execution Visibility into Answer Composition. Many answer
  surfaces can consume visibility evidence, but visibility is not shown as a
  required input for every composed answer.

## Orthogonal responsibilities

### Intentionally independent families

Implementation evidence supports the following independence boundaries:

- Execution Visibility observes execution/state/diagnostic behavior but does not
  authorize, mutate, or execute operations.
- Answer Composition communicates answer/support/boundary/limitations but does
  not create cluster truth, ledger events, capability admission, or operation
  execution.
- Inquiry Lineage preserves result lineage but does not decide operational policy,
  verify capability truth, or produce status/timing data.
- Observation-Derived Capability separates observed/admitted capability knowledge
  from executable operation contract metadata and does not own runtime callable
  realization.
- Operational Responsibility owns execution path responsibilities but not the
  explanation surfaces that later describe why an answer/result/reference is
  supported.

## Shared boundaries

### Shared compatibility handoffs

Implementation-backed handoffs recur across families:

| Handoff | Families touching it | Supported conclusion |
| --- | --- | --- |
| Completed tool-call event handed to fact extraction | Operational Responsibility; Observation-Derived Capability / projection evidence path | Execution recording and post-execution knowledge extraction are separated by a durable event handoff. |
| Capability inventory source union | Observation-Derived Capability; Operational Responsibility | Admitted capability knowledge and executable operation contract metadata are separated before compatibility union. |
| Diagnostic inventory and shape audit | Execution Visibility; Answer/diagnostic surfaces | New or changed diagnostic surfaces must stay visible and read-only unless intentionally operational. |
| Public answer compatibility objects | Answer Composition; Inquiry Lineage | Private payloads separate ownership while public objects preserve compatibility. |
| Reference/selection/reasoning public objects | Inquiry Lineage; Answer Composition | Result material and lineage material are separated before unchanged presentation objects. |

## Cross-family ownership

### Implementation boundaries crossing family ownership

Cross-family boundaries exist, but the evidence favors handoff ownership rather
than shared ownership:

- `ToolExecutor` crosses execution recording and knowledge extraction only through
  a completed-event handoff; it should not be read as a shared owner of all
  knowledge projection.
- Capability inventory crosses admitted capability knowledge, requested needs,
  and executable contract labels; it intentionally preserves those as separated
  sources before union.
- Diagnostic surfaces cross many subsystems, but diagnostic inventory/shape-audit
  metadata preserves whether they record, write the ledger, or mutate cluster
  state.
- Public answer and lineage objects cross compatibility boundaries, but private
  implementation payloads clarify local ownership before the public handoff.

## Supported architectural stack

The strongest implementation-backed architecture is a **bounded handoff stack**:

```text
1. Operational execution and observation produce records/evidence.
2. Projection/read-only capability surfaces derive admitted capability and
   executable-contract views from evidence and registry metadata.
3. Visibility surfaces expose status, timing, cache, and diagnostics around the
   above without owning their behavior.
4. Answer composition consumes existing evidence and authority boundaries to
   produce bounded answers.
5. Inquiry lineage preserves how selected results, conclusions, and references
   were derived or bounded.
```

This stack is supported only as a recurring composition order for the reviewed
surfaces. It is not a universal dependency rule. Execution Visibility can be a
sidecar to step 1 or projection rather than strictly above them. Inquiry Lineage
can appear inside answer-related surfaces rather than only after answer
composition. Observation-Derived Capability can both consume operational evidence
and provide operation-adjacent contract context, creating a controlled handoff
loop rather than cyclic ownership.

## Unsupported relationships and counterexamples

Unsupported conclusions:

- **A strict layered architecture.** The evidence shows sidecar visibility,
  compatibility handoffs, and bidirectional operational/capability adjacency.
- **Operational Responsibility owns capability truth.** It produces execution
  evidence, but capability admission and inventory are separated.
- **Observation-Derived Capability owns operation execution.** It can expose
  executable operation contract metadata, but `ToolExecutor`, validation, policy,
  and registry implementation own execution.
- **Execution Visibility owns diagnostic meaning.** It exposes status/timing/cache
  surfaces but does not by itself establish semantic correctness or capability
  admission.
- **Answer Composition owns lineage.** Answer surfaces may include reasoning and
  support, but Inquiry Lineage slices show separate result/lineage ownership.
- **Inquiry Lineage family vocabulary is fully stabilized.** The fourth lineage
  slice explicitly preserves insufficient evidence for cross-surface vocabulary.

Counterexamples to an assumed stack:

- Operational and capability responsibilities form a handoff loop: execution can
  produce evidence later consumed by capability surfaces, while registered
  operation contract labels are consumed by capability inventory and operation
  context. This is not cyclic ownership because each side owns different
  artifacts.
- Execution Visibility attaches to execution, ingestion, current facts,
  state-build, projection cache, and diagnostics. That breadth argues against a
  single vertical layer.
- Public compatibility objects intentionally combine fields from multiple
  responsibilities after private payload separation. That is compatibility
  compression, not proof of shared ownership.

## Missing implementation evidence

The repository does not yet provide enough evidence to conclude:

- a public, first-class dependency graph among all responsibility families;
- a stabilized Inquiry Lineage family name with the same confidence as the four
  completed family labels;
- a universal answer-composition consumer relation for every operational,
  visibility, capability, and lineage artifact;
- writable capability promotion/admission lifecycle ownership;
- pending-action lifecycle ownership inside the operational architecture;
- projection result versus influence lineage as a completed lineage boundary;
- a first-class family dedicated only to compatibility handoffs.

## Does evidence suggest a missing first-class responsibility family?

Yes, but only as a hypothesis.

Implementation-backed observation: every completed family repeatedly preserves
compatibility by separating private ownership from unchanged public objects,
events, JSON, diagnostics, or inventory rows. Examples include completed tool-call
handoff, capability inventory source union, diagnostic read-only contracts,
`OperationalStory` payload handoff, and `ReferenceSelection` payload handoff.

Architectural hypothesis: **Compatibility Handoff** may be a missing first-class
responsibility family between completed families.

Unsupported conclusion: the repository has not recovered this as its own family.
There is no bounded slice sequence proving compatibility handoff ownership across
independent surfaces. Treat it as the recommended next audit target, not as a
completed or named architecture component.

## Recommended next implementation step

Do not implement a runtime slice from this audit.

Recommended next bounded implementation audit:

```text
Can compatibility handoffs be recovered as a first-class responsibility family,
or are they only a recurring method used by unrelated responsibility families?
```

Acceptance for that future audit should require implementation evidence from at
least operational execution events, capability inventory source union, diagnostic
inventory/shape contracts, answer composition payloads, and inquiry lineage
payloads. It should explicitly avoid adding new runtime surfaces until a single
compressed ownership boundary is recovered.

## Confidence

| Conclusion | Confidence | Reason |
| --- | --- | --- |
| Completed families can be related by implementation artifacts and handoffs. | High | Multiple completion audits and slices identify produced/consumed artifacts and compatibility-preserving handoffs. |
| The architecture is a strict stack. | Low | Evidence shows sidecars, compatibility handoffs, and operational/capability adjacency rather than one-way layering. |
| The architecture is a bounded handoff graph with recurring composition order. | Medium-high | Strong recurring pattern, but not represented as a formal runtime graph. |
| Operational Responsibility, Execution Visibility, Observation-Derived Capability, and Answer Composition are completed for their recovered chains. | High | Existing completion/inventory audits classify them as implementation complete. |
| Inquiry Lineage is equally vocabulary-stable as the other completed labels. | Medium-low | Slices are implementation-backed, but the latest slice explicitly declines to stabilize cross-surface family vocabulary. |
| Compatibility Handoff is a missing first-class family. | Medium as hypothesis, low as conclusion | Recurs in evidence, but no dedicated family recovery exists. |

## Final answer

The repository can derive architectural relationships between completed
responsibility families, but only as implementation-backed handoffs and artifact
consumption relationships. The completed families compose into a bounded handoff
graph: operational execution produces records/evidence; observation-derived
capability consumes projected evidence and registered contract metadata;
execution visibility observes lifecycle/timing/cache/diagnostic behavior; answer
composition consumes evidence and boundaries to produce bounded answers; inquiry
lineage preserves how selected results, conclusions, or references were derived
or bounded.

The evidence does not support a universal layered architecture. The strongest
unsupported-but-plausible missing family is Compatibility Handoff, because every
completed family relies on private ownership separation before unchanged public
compatibility objects or records. That should be audited before any new runtime
slice is attempted.
