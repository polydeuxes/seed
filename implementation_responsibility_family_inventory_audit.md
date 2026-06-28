# Implementation Responsibility Family Inventory Audit

## Scope

This is a bounded implementation audit. It does not begin another responsibility
family, perform architectural recovery, add runtime surfaces, add CLI behavior,
create registries, create metadata, create priority queues, create roadmaps,
create planning systems, or maintain a manual work list.

The question is whether repository evidence can answer:

```text
What is the next implementation responsibility family?
```

using implementation evidence rather than architectural preference or operator
memory.

## Evidence basis

Reviewed recurring implementation-backed evidence rather than isolated wording:

- `inquiry_lineage_architectural_projection_slice_methodology.md`
- `responsibility_family_completion_inquiry_audit.md`
- `answer_composition_family_completion_audit.md`
- `architectural_orientation_answer_composition_audit.md`
- `operational_responsibility_slice_001.md` through
  `operational_responsibility_slice_006.md`
- `execution_visibility_slice_001.md` through
  `execution_visibility_slice_005.md`
- `observation_derived_capability_slice_001.md` through
  `observation_derived_capability_slice_005.md`
- `answer_composition_slice_001.md` through
  `answer_composition_slice_004.md`
- `architectural_orientation_answer_composition_slice_001.md`
- `docs/execution_visibility_investigation.md`
- `docs/answer_composition_visibility_investigation.md`
- `docs/answer_composition_self_knowledge_investigation.md`
- `docs/context_preservation_surface_investigation.md`
- `docs/reasoning_chain_visibility_investigation.md`
- `docs/repository_observation_implementation_inventory_audit.md`
- selected implementation/test names referenced by those audits and slices.

The maturity classifications used here are limited to the requested vocabulary:

```text
implementation complete
ready for projection
requires additional recovery
insufficient evidence
```

## Repository-derived maturity rule

A family is treated as `implementation complete` only when repeated slices have
already made the recovered boundaries explicit in implementation, preserved
compatibility, and reached a natural stopping point for that recovered chain.

A family is treated as `ready for projection` when evidence repeatedly appears in
implementation surfaces, investigations, and partial slices, and when the next
work can make an already-recovered compressed boundary explicit without another
architectural recovery pass.

A family `requires additional recovery` when evidence exists but ownership has
not stabilized enough to identify one bounded implementation slice.

A family has `insufficient evidence` when the vocabulary exists primarily as
presentation or prose and recurring implementation ownership is not observable.

## Identified responsibility families

| Family | Maturity classification | Representative implementation | Representative investigations/audits | Current ownership signal |
| --- | --- | --- | --- | --- |
| Operational Responsibility | implementation complete | `ToolRegistry`, `ToolNeedService`, `ToolValidationService`, `ToolExecutionPolicyService`, `ToolExecutor` responsibility seams described by the six operational slices | `responsibility_family_completion_inquiry_audit.md`; operational slices 001-006 | Stable recovered chain from capability recommendation through post-execution knowledge extraction. |
| Execution Visibility | implementation complete | `ExecutionStatusEmitter` / consumers, observation ingestion diagnostics, cache-debug timing/status paths, current-facts and state-build visibility seams | `responsibility_family_completion_inquiry_audit.md`; `docs/execution_visibility_investigation.md`; execution visibility slices 001-005 | Stable recovered chain from status emission through projection-cache diagnostics. |
| Observation-Derived Capability | implementation complete | `CapabilityCandidate`, capability verification/promotion readiness/inventory builders, executable operation contract handoff | `responsibility_family_completion_inquiry_audit.md`; observation-derived capability slices 001-005 | Stable read-only chain from observed evidence through capability inventory and executable operation contract separation. |
| Answer Composition | implementation complete | `operational_story`, `inquiry_orientation`, and supporting bounded answer surfaces such as `reasoning_path`, `selection_path`, `reference_selection`, and `inquiry_artifacts` | `answer_composition_family_completion_audit.md`; `docs/answer_composition_visibility_investigation.md`; answer composition slices 001-004; architectural orientation answer-composition slice 001 | Stable five-part answer/reason/support/boundary/limitations pattern proven in more than one surface. |
| Context Preservation / Reasoning-Chain Visibility | ready for projection | `reasoning_path_audit`, `selection_path_audit`, `reference_selection`, `operational_story`, `projection_shape`, `capability_relationship`, diagnostic inventory/shape audit | `docs/context_preservation_surface_investigation.md`; `docs/reasoning_chain_visibility_investigation.md`; `answer_composition_family_completion_audit.md` recommendation | Recurring preservation of reason, selection frame, alternatives, support, boundaries, and unknowns; implementation ownership is visible but still compressed across answer surfaces. |
| Repository Observation Acquisition | requires additional recovery | source relationship extraction primitives and relationship facts; absent `--observe-repository` operator path | `docs/repository_observation_implementation_inventory_audit.md`; repository observation/source relationship investigations | Adapter evidence exists, but acquisition workflow ownership is not stabilized across traversal, filtering, ingestion, command, and query surfaces. |
| Responsibility-Family Status Inquiry | requires additional recovery | no dedicated runtime inquiry surface; existing evidence lives in slice reports and audits | `responsibility_family_completion_inquiry_audit.md`; `architectural_orientation_answer_composition_audit.md` | The answer can be manually composed from evidence, but implementing such a surface is explicitly forbidden for this task and would need separate operational-surface work. |
| Presentation-only orientation vocabulary | insufficient evidence | labels such as active edge, current work position, continuation, and source navigation when unsupported by implementation reachability | `AGENTS.md`; orientation/frontier documents; presentation vocabulary warnings | Vocabulary exists, but repository instructions warn that presentation labels are not automatically knowledge. |

## Family findings

### Operational Responsibility

#### Implementation evidence

The recovered operational chain is implementation-backed by six slices:

```text
Capability Recommendation != Operation Selection
Operation Selection != Registered Operation Validation
Registered Operation Validation != Policy Authorization
Policy Authorization != Execution Realization
Execution Realization != Execution Recording
Execution Recording != Post-Execution Knowledge Extraction
```

Representative implementation ownership includes `ToolRegistry` as registered
operation catalog ownership, `ToolNeedService` and `_CapabilityResolution` as
capability/recommendation separation, `ToolValidationService.select_operation()`
as operation selection, `ToolExecutionPolicyService.evaluate_with_state_factory()`
as authorization boundary, and `ToolExecutor` seams for realization, recording,
and post-execution knowledge extraction.

#### Representative implementation slices

- `operational_responsibility_slice_001.md` through
  `operational_responsibility_slice_006.md`.

#### Recurring vocabulary

Capability recommendation, operation selection, registered operation validation,
policy authorization, execution realization, execution recording, and
post-execution knowledge extraction.

#### Remaining implementation gaps

Pending-action lifecycle, approved resumption versus fresh authorization,
policy-outcome recording, runtime-loop-specific evidence collection, and
action-plan top-provider choice remain adjacent compressed areas.

#### Maturity classification

`implementation complete` for the recovered operational chain. The adjacent
operational gaps do not invalidate completion of this bounded family; they are
counterexamples to claiming all operational architecture is complete.

### Execution Visibility

#### Implementation evidence

The recovered execution-visibility chain is implementation-backed by five
slices:

```text
Status Emission != Status Consumption
Execution Status != Execution Timing
Execution Timing != Cache Visibility
Execution Visibility != Execution Diagnostics
State Build Visibility != Projection Cache Diagnostics
```

Representative implementation includes status emission/consumption separation,
observation ingestion lifecycle status separated from timing diagnostics,
state-build and current-facts cache debug visibility, projection cache status,
and diagnostic shape/inventory boundaries that preserve read-only diagnostic
behavior.

#### Representative implementation slices

- `execution_visibility_slice_001.md` through
  `execution_visibility_slice_005.md`.

#### Recurring vocabulary

Status emission, status consumption, execution timing, cache visibility,
projection cache diagnostics, state-build visibility, diagnostic visibility, and
read-only timing evidence.

#### Remaining implementation gaps

Projection build diagnostics still pass replay/build phase evidence through some
cache paths, fact-index cache timing is adjacent to status reporting, knowledge
reachability metadata carries cache visibility and timing together, and progress
cadence timing remains mixed with status-emission throttling.

#### Maturity classification

`implementation complete` for the recovered execution-visibility chain. The
remaining gaps are valid future visibility-adjacent work only after a new family
is recovered.

### Observation-Derived Capability

#### Implementation evidence

The recovered observation-derived capability chain is implementation-backed by
five slices:

```text
Observed Evidence != Executable Operation Contract
Observed Evidence != Capability Verification
Capability Verification != Capability Promotion
Capability Promotion != Capability Inventory
Capability Inventory != Executable Operation Contract
```

Representative implementation includes `CapabilityCandidate`, verification
evidence acquisition, capability verification inspection, promotion readiness
inspection, capability inventory construction from admitted projected capability
facts, and executable operation contract state separated from inventory sources.

#### Representative implementation slices

- `observation_derived_capability_slice_001.md` through
  `observation_derived_capability_slice_005.md`.

#### Recurring vocabulary

Observed evidence, executable operation contract, capability verification,
capability promotion, promotion readiness, capability inventory, and admitted
repository capability knowledge.

#### Remaining implementation gaps

Writable `capability_verified` fact creation, verification fact authority,
promotion/admission writers, provider-reported capability state versus
independently verified state, and public contract-derivation APIs remain outside
the completed read-only chain.

#### Maturity classification

`implementation complete` for the read-only observation-derived capability chain.
The writable promotion/admission lifecycle is not complete and would need a
separate family recovery.

### Answer Composition

#### Implementation evidence

The recovered answer-composition family is implementation-backed by four answer
composition slices plus an architectural-orientation answer-composition slice.
The recurring implementation shape is:

```text
Repository Knowledge
↓
Answer Composition
  Answer
  Reason
  Supporting Evidence
  Boundary
  Limitations
↓
Compatibility Object
↓
Rendering
```

Representative implementation evidence includes `operational_story`, where
private payloads separate answer, reasoning, supporting evidence, boundary, and
limitations before handoff to the stable `OperationalStory` compatibility object,
and `inquiry_orientation`, where `_ArchitecturalOrientationAnswer` separates the
same five-part shape before handoff to `InquiryOrientationView`.

Other bounded answer surfaces show compatible partial patterns:
`reasoning_path`, `selection_path`, `reference_selection`, `inquiry_artifacts`,
and `question_surface_inventory`.

#### Representative implementation slices

- `answer_composition_slice_001.md` through
  `answer_composition_slice_004.md`.
- `architectural_orientation_answer_composition_slice_001.md`.

#### Recurring vocabulary

Answer, reason, supporting evidence, boundary, limitations, compatibility
handoff, rendering, bounded answer surface, question family, and authority
boundary.

#### Remaining implementation gaps

Several answer-like surfaces still use domain-specific public dataclasses rather
than an implementation-local five-part answer payload. This prevents a universal
retrofit claim, but it does not prevent recognizing the recovered family as
complete for its bounded representative implementations.

#### Maturity classification

`implementation complete` for the recovered answer-composition responsibility.
The family completion audit explicitly supports stopping answer-composition
slices as the active family.

### Context Preservation / Reasoning-Chain Visibility

#### Implementation evidence

This is the strongest candidate for the next implementation responsibility
family because evidence recurs across independent implemented surfaces rather
than only in documents.

Representative implementations already preserve parts of a larger responsibility:

- `reasoning_path_audit` preserves observed evidence, intermediate conclusions,
  derived conclusions, consumers, story impact, unknowns, and read-only
  boundaries.
- `selection_path_audit` preserves candidates, selected item, selection factors,
  non-selected candidates, evidence, outcome, unknowns, and read-only
  boundaries.
- `reference_selection` preserves selected reference, rationale, alternatives,
  limitations, and authority boundary.
- `operational_story` preserves focus, pressure, support, constraints,
  investigation path, observed outcomes, unknowns, and boundary.
- `projection_shape` preserves consumes, produces, influences, does-not-influence,
  authority boundary, and confidence.
- `diagnostic_inventory` and `diagnostic_shape_audit` preserve operational
  surface contracts and implementation conformance context.

The recurring responsibility is not merely answer composition. It is preserving
the context that makes a selected, derived, translated, or summarized answer
interpretable: reason, comparison frame, alternatives, support chain, ownership
boundary, authority boundary, unknowns, and non-selected remainder.

#### Representative investigations

- `docs/context_preservation_surface_investigation.md` identifies recurring
  preserved context types: reasoning context, selection context, reference
  context, operational context, component context, projection context,
  diagnostic governance context, authority/boundary context, and observation
  domain context.
- `docs/reasoning_chain_visibility_investigation.md` identifies chain-preserving
  surfaces and chain-fragmenting surfaces, including representative chains from
  ownership discrepancies to capability needs and from pressure candidates to
  operational story focus.
- `answer_composition_family_completion_audit.md` recommends this area after
  answer composition because multiple surfaces preserve derivation, selection,
  reference, operational context, and inquiry orientation.

#### Representative implementation slices

No dedicated context-preservation family slice exists yet. However, the completed
answer-composition and architectural-orientation slices provide adjacent
implementation evidence: they already made answer/reason/support/boundary/
limitations explicit and exposed the next compressed responsibility as preserving
interpretive context across surfaces.

#### Recurring vocabulary

Reasoning context, selection context, reference context, operational context,
projection context, diagnostic governance context, support chain, rationale,
alternatives, candidate set, non-selected candidates, comparison frame,
unknowns, limitations, and authority boundary.

#### Remaining implementation gaps

The evidence is currently distributed across surfaces. Ownership has not yet
been projected as a single family boundary. Likely compressed seams include:

```text
Answer Composition != Context Preservation
Selection Result != Selection Context
Derived Conclusion != Support Chain
Reference Choice != Comparison Frame
Projection Topology != Instance-Specific Reasoning Path
Diagnostic Contract != Interpretive Context
```

This audit does not choose the exact first slice. It only determines that the
family is mature enough for projection without further architectural recovery.

#### Maturity classification

`ready for projection`.

### Repository Observation Acquisition

#### Implementation evidence

Repository evidence supports source relationship observation primitives, such as
import and definition relationship extraction and relationship facts from
caller-provided source text. The repository also records an operator failure for
`seed --observe-repository .`, showing the operator-accessible acquisition path
is absent.

#### Representative investigations

- `docs/repository_observation_implementation_inventory_audit.md`.
- source relationship observation and repository observation source design
  documents referenced by that audit.

#### Recurring vocabulary

Observation adapter, observation source, acquisition workflow, operator command,
repository traversal, file filtering, ingestion, relationship facts, and
queryable projected repository knowledge.

#### Remaining implementation gaps

The current evidence does not stabilize ownership across repository root input,
file discovery/filtering, adapter invocation, observation/fact ingestion,
operator command, and queryable output.

#### Maturity classification

`requires additional recovery`.

### Responsibility-Family Status Inquiry

#### Implementation evidence

The repository can manually answer family status and completion from slices and
audits. A read-only inquiry surface was identified as naturally emerging in
`responsibility_family_completion_inquiry_audit.md`, but no dedicated runtime
surface currently exists.

#### Representative investigations

- `responsibility_family_completion_inquiry_audit.md`.
- `architectural_orientation_answer_composition_audit.md`.

#### Recurring vocabulary

Family status, family completeness, implemented boundaries, remaining compressed
boundaries, natural stopping point, confidence, and read-only inquiry surface.

#### Remaining implementation gaps

The evidence is sufficient for a future read-only implementation, but this task
explicitly forbids implementing runtime surfaces, CLI, registries, metadata, or
manual status tracking. Recommending this as the next family would collapse the
audit into the forbidden implementation direction.

#### Maturity classification

`requires additional recovery` for this task's purpose, because the operational
surface boundary itself would need to be specified separately and is explicitly
out of scope here.

### Presentation-only orientation vocabulary

#### Implementation evidence

Terms such as continuation, current work position, source navigation, active
edge, storage topology, state build, and projection cache recur in presentation
and orientation materials. Repository instructions explicitly warn that such
terms may exist only as visibility or presentation labels unless implementation
evidence, such as a knowledge reachability audit, supports promotion.

#### Representative investigations

Orientation, frontier, and presentation documents provide vocabulary pressure,
but not enough recurring implementation ownership for a responsibility family.

#### Remaining implementation gaps

Vocabulary has not stabilized into implementation ownership. Some terms map to
implemented surfaces in narrow contexts, but the broad presentation vocabulary
should not be promoted into the next family merely because it is familiar.

#### Maturity classification

`insufficient evidence` as a responsibility family.

## Counterexamples reviewed

### Vocabulary exists but recurring implementation evidence does not

Presentation-only orientation vocabulary is the strongest counterexample. It can
sound like an implementation family, but repository instructions explicitly deny
promotion from presentation vocabulary alone.

### Implementation evidence exists but ownership has not stabilized

Repository Observation Acquisition is the strongest counterexample. The source
relationship adapter evidence exists, but the acquisition workflow boundary is
not stabilized across traversal, ingestion, command, and queryable projection.

### A complete family still has adjacent gaps

Operational Responsibility, Execution Visibility, Observation-Derived
Capability, and Answer Composition all have adjacent gaps. Those gaps are not
failures of the completed recovered families. They are evidence that completion
must remain bounded to the recovered chain.

## Supported conclusions

1. Seed currently contains four implementation-complete responsibility families:
   Operational Responsibility, Execution Visibility, Observation-Derived
   Capability, and Answer Composition.
2. Completion is bounded to recovered implementation chains, not entire domains.
3. Context Preservation / Reasoning-Chain Visibility is the only reviewed
   candidate that is both recurring in implementation evidence and not already
   completed as a family.
4. Repository Observation Acquisition has real implementation evidence but still
   requires additional recovery before projection.
5. Presentation vocabulary alone is insufficient evidence for family selection.
6. The repository can answer the next-family question from evidence without a
   runtime registry, roadmap, priority queue, manual status board, or operator
   memory.

## Unsupported conclusions

1. Seed should begin a runtime inquiry surface for responsibility-family status
   as part of this task.
2. Seed should implement repository observation acquisition next merely because a
   CLI gap exists.
3. Seed should continue Answer Composition slices after the family completion
   audit says the recovered responsibility is complete enough to stop.
4. Seed should treat every answer-like surface as fully projected into the
   five-part answer-composition primitive.
5. Seed should promote presentation labels into preserved knowledge without
   implementation reachability evidence.
6. Seed should choose a next family based on architectural preference,
   novelty, operator memory, or document frequency alone.

## Recommended next implementation responsibility family

```text
Context Preservation / Reasoning-Chain Visibility
```

## Reason for recommendation

The recommendation emerges from recurring implementation evidence:

1. Completed Answer Composition made bounded answers explicit and then exposed
   the next compressed responsibility: preserving the context that lets those
   answers remain interpretable across surfaces.
2. `reasoning_path_audit`, `selection_path_audit`, `reference_selection`,
   `operational_story`, `projection_shape`, `capability_relationship`,
   `diagnostic_inventory`, and `diagnostic_shape_audit` already preserve pieces
   of context and reasoning chains.
3. Existing investigations identify the same recurring ownership pressure across
   independent surfaces: reason, support chain, candidate set, selected and
   non-selected alternatives, comparison frame, operational boundary, projection
   influence, diagnostic contract, unknowns, and authority limits.
4. The family is neither already complete nor merely vocabulary. It has
   implementation evidence strong enough to begin a bounded projection slice,
   while still retaining visible compressed boundaries.

The first projection slice should still be chosen by implementation evidence at
slice time. This audit only establishes the family as ready; it does not select
or implement a boundary.

## Confidence

`High` that the next family should not be Operational Responsibility, Execution
Visibility, Observation-Derived Capability, or Answer Composition, because each
has an implementation-backed completion audit or natural stopping point for its
recovered chain.

`High` that Context Preservation / Reasoning-Chain Visibility has recurring
implementation evidence across multiple independent surfaces.

`Medium` on the exact family label, because the repository uses overlapping
vocabulary such as context preservation, reasoning-chain visibility,
traceability, rationale, support, and selection context. The implementation
pressure is stable even if the final label should be bounded by the first slice.

## Acceptance answer

Which implementation responsibility families currently exist?

```text
Operational Responsibility
Execution Visibility
Observation-Derived Capability
Answer Composition
Context Preservation / Reasoning-Chain Visibility
Repository Observation Acquisition
Responsibility-Family Status Inquiry
Presentation-only Orientation Vocabulary
```

Which are complete?

```text
Operational Responsibility
Execution Visibility
Observation-Derived Capability
Answer Composition
```

Which are ready for projection?

```text
Context Preservation / Reasoning-Chain Visibility
```

Which still require recovery?

```text
Repository Observation Acquisition
Responsibility-Family Status Inquiry
```

Which have insufficient evidence?

```text
Presentation-only Orientation Vocabulary
```

Which should become the next implementation family?

```text
Context Preservation / Reasoning-Chain Visibility
```

Why?

```text
Because it is the only reviewed candidate with recurring implementation evidence,
representative investigations, visible compressed ownership, and no existing
completion audit, while counterexamples either lack stabilized ownership or rely
on presentation vocabulary rather than implementation evidence.
```
