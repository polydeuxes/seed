# Implementation Grammar Visibility Audit

## Scope

This is a bounded implementation audit. It does not implement grammar, a grammar
observer, a runtime surface, CLI behavior, renderer behavior, schema behavior,
JSON behavior, event behavior, ledger behavior, vocabulary migration, or another
responsibility-family slice.

The central question is:

```text
Can Seed observe architectural grammar directly from implementation evidence?
```

Repository authority wins. This audit begins from recurring implementation
structures in completed slices, completion audits, family stack evidence,
compatibility handoff classification, inquiry-lineage vocabulary evidence,
implementation responsibility inventory evidence, and implementation family
relationships. It does not begin from preferred terminology.

## Evidence reviewed

Primary audit and slice evidence:

- `responsibility_family_completion_inquiry_audit.md`
- `implementation_responsibility_family_inventory_audit.md`
- `implementation_responsibility_family_stack_audit.md`
- `compatibility_handoff_classification_audit.md`
- `inquiry_lineage_family_vocabulary_audit.md`
- `operational_responsibility_slice_001.md` through
  `operational_responsibility_slice_006.md`
- `execution_visibility_slice_001.md` through
  `execution_visibility_slice_005.md`
- `observation_derived_capability_slice_001.md` through
  `observation_derived_capability_slice_005.md`
- `answer_composition_slice_001.md` through `answer_composition_slice_004.md`
- `inquiry_lineage_slice_001.md` through `inquiry_lineage_slice_004.md`

Representative implementation evidence checked:

- `seed_runtime/registry.py`
- `seed_runtime/tool_needs.py`
- `seed_runtime/tool_validation.py`
- `seed_runtime/tool_execution_policy.py`
- `seed_runtime/execution.py`
- `seed_runtime/execution_status.py`
- `seed_runtime/capability_candidates.py`
- `seed_runtime/capability_inventory.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `seed_runtime/operational_story.py`
- `seed_runtime/selection_path_audit.py`
- `seed_runtime/reasoning_path_audit.py`
- `seed_runtime/reference_selection.py`
- `seed_runtime/projection_shape.py`

## Summary answer

Yes, Seed can already observe architectural grammar directly from implementation
evidence, if grammar is treated as recurring implementation relation shape rather
than as a new engine, observer, registry, or vocabulary authority.

The strongest implementation-backed grammar form is:

```text
A != B
```

It appears across completed responsibility families before stable family
vocabulary appears. It is joined by recurring, implementation-backed relation
forms:

```text
A owns B
A produces B
A consumes B
A hands off to B
A preserves B
A bounds B
A derives B
A selects B
A explains B
A observes B
A does not own B
```

The repository does not yet support every plausible grammar form. In particular,
this audit found insufficient evidence for treating grammar itself as an owner,
for treating compatibility handoff as a first-class responsibility family, or for
claiming a universal layer relationship between all families.

## Observed grammar forms

### 1. `A != B`

#### Implementation coverage

High. This is the dominant recovered implementation grammar across all completed
responsibility families.

Representative completed-family forms include:

```text
Capability Recommendation != Operation Selection
Operation Selection != Registered Operation Validation
Registered Operation Validation != Policy Authorization
Policy Authorization != Execution Realization
Execution Realization != Execution Recording
Execution Recording != Post-Execution Knowledge Extraction
```

```text
Status Emission != Status Consumption
Execution Status != Execution Timing
Execution Timing != Cache Visibility
Execution Visibility != Execution Diagnostics
State Build Visibility != Projection Cache Diagnostics
```

```text
Observed Evidence != Executable Operation Contract
Observed Evidence != Capability Verification
Capability Verification != Capability Promotion
Capability Promotion != Capability Inventory
Capability Inventory != Executable Operation Contract
```

```text
Answer != Reason
Answer Material != Supporting Evidence
Answer Material != Authority Boundary
Answer Material != Limitations
```

```text
Outcome != Lineage Frame
Selection Result != Selection Lineage
Derived Conclusion != Derivation Lineage
Reference Choice != Comparison Lineage
```

#### Representative implementations

- `ToolRegistry` remains the registered operation service boundary while private
  index ownership is isolated behind implementation-local catalog mechanics.
- `ToolValidationService.select_operation()` separates selected operation
  resolution from capability recommendation and provider selection.
- `ToolExecutionPolicyService.evaluate_with_state_factory()` separates registered
  operation validation from policy authorization.
- `ToolExecutor._record_completed_tool_call(...)` and
  `ToolExecutor._extract_post_execution_knowledge(...)` separate execution
  recording from post-execution interpretation.
- `ExecutionStatusEmitter` and execution-status consumers separate status
  production from consumption.
- `_CapabilityInventorySources` separates admitted capability state, requested
  capability needs, and executable operation contract labels before composing an
  inventory universe.
- `_SelectionResultPayload` / `_SelectionLineagePayload`,
  `_DerivedConclusionPayload` / `_DerivationLineagePayload`, and
  `_ReferenceChoicePayload` / `_ComparisonLineagePayload` separate result-like
  material from lineage material before compatibility handoff.

#### Recurrence

Very high. The same grammar form appears in operational execution, execution
visibility, observation-derived capability, answer composition, and inquiry
lineage. It appears at different scales: private helper extraction, service
boundary separation, diagnostic declaration/conformance separation, public
compatibility object assembly, and family completion audits.

#### Ownership consistency

High. In reviewed cases, `A != B` does not mean two labels are merely different.
It means the implementation has distinct ownership pressure: one concern owns a
service boundary, selected result, event, evidence, declaration, or answer part;
the other owns validation, authorization, interpretation, lineage, conformance,
limitations, or presentation context.

#### Lexicon dependence

Low. The exact vocabulary often changes after the implementation boundary is
made explicit. The grammar is observable from structure: separate payloads,
separate service calls, record-before-extract sequencing, separate inventory
source groups, and compatibility-preserving handoff functions.

#### Counterexamples

- Remaining compressed boundaries show `A != B` is not automatically true just
  because a prose distinction is attractive. Pending-action lifecycle, projection
  result/influence lineage, writable capability admission, and progress cadence
  timing still need bounded recovery before being treated as implemented grammar.
- Public compatibility objects can still combine separated concerns after private
  implementation ownership has been made explicit. The public object alone is
  not enough; the implementation-local handoff is the evidence.

#### Confidence

High.

### 2. `A owns B`

#### Implementation coverage

High for completed-family internals; medium as a universal grammar because some
relationships are intentionally handoffs or observations rather than ownership.

#### Representative implementations

- Operational Responsibility owns the registered-operation path from capability
  recommendation through post-execution knowledge extraction.
- `ToolRegistry` owns the registered operation service boundary, while the
  private index owns storage, duplicate rejection, sorted views, visibility
  filtering, and capability filtering.
- Execution Visibility owns diagnostic visibility contracts and shape checks, not
  each diagnostic domain's meaning.
- Observation-Derived Capability owns read-only capability inventory and
  verification/promotion-readiness inspection, not executable tool realization.
- Answer Composition owns answer/reason/support/boundary/limitations assembly,
  not source fact truth.
- Inquiry Lineage owns result/lineage separation, not operational policy or
  capability truth.

#### Recurrence

High. Ownership language appears in every family completion audit and slice, but
it is strongest when a concrete implementation object, helper, payload, service,
or function owns fields and behavior.

#### Ownership consistency

High where implementation boundaries exist. Low where names are presentation-only
or where the repository warns that vocabulary is not knowledge.

#### Lexicon dependence

Medium-low. Ownership is supported by code boundaries and tests more than by
names. However, ownership grammar still depends on identifying implementation
artifacts accurately.

#### Counterexamples

Compatibility Handoff is recurring but does not independently own artifacts,
decisions, durable behavior, or invariants. It is therefore a counterexample to
promoting a recurring pattern into an owner.

#### Confidence

High for concrete implementation artifacts; medium for abstract family labels.

### 3. `A produces B` and `A consumes B`

#### Implementation coverage

High. Production/consumption is observable in event recording, capability
inventory source union, visibility diagnostics, answer composition, and lineage
surfaces.

#### Representative implementations

- Execution recording produces completed tool-call events; post-execution
  extraction consumes completed events.
- Registered operation contract metadata produces executable capability labels;
  capability inventory consumes those labels as one source beside admitted facts
  and requested capabilities.
- Execution, observation ingestion, state build, and projection cache paths
  produce status/timing/cache evidence; execution-visibility diagnostics consume
  that evidence.
- Answer Composition consumes facts, diagnostics, inventories, inquiry artifacts,
  and boundaries to produce bounded answer surfaces.
- Inquiry Lineage consumes candidates, evidence, alternatives, limitations, and
  authority boundaries to produce lineage-bearing results.

#### Recurrence

High across family stack relationships.

#### Ownership consistency

High when paired with `A owns B` and `A does not own B`. The producer of an
artifact is not always the owner of downstream interpretation. This is especially
visible in completed-event extraction and capability inventory source union.

#### Lexicon dependence

Low. Production and consumption are visible through function calls, source
collections, payload construction, event append/read paths, and deterministic
formatting.

#### Counterexamples

The family stack audit does not prove a universal upstream/downstream order for
every family. Several families consume evidence opportunistically without forming
a strict layer cake.

#### Confidence

High.

### 4. `A hands off to B`

#### Implementation coverage

High as a recurring architectural pattern; not supported as an independent
responsibility family.

#### Representative implementations

- Completed operational event handoff: execution recording appends the completed
  event before post-execution extraction observes it.
- Capability inventory source union: admitted capability facts, requested needs,
  and registered operation contract labels remain separated before inventory
  presentation.
- Diagnostic inventory/shape audit: diagnostic declarations and implementation
  conformance rows are compared without taking over diagnostic domain behavior.
- Operational Story payload handoff: private answer/reason/support/boundary/
  limitations payloads map into the unchanged public compatibility object.
- Reference Selection payload handoff: reference choice and comparison lineage
  payloads map into the unchanged public `ReferenceSelection` object.

#### Recurrence

High. It recurs across durable events, read-only inventories, diagnostics,
answer payloads, and lineage payloads.

#### Ownership consistency

High when classified as a pattern. Low if promoted into a family. The handoff
preserves owners; it does not become the owner.

#### Lexicon dependence

Low. The form is visible from sequencing and compatibility-preserving assembly,
even when the stable name for the surrounding family is unsettled.

#### Counterexamples

Compatibility Handoff itself was classified as a recurring architectural pattern,
not a first-class responsibility family. This prevents over-reading recurrence as
ownership.

#### Confidence

High as a pattern; low as a family.

### 5. `A preserves B`

#### Implementation coverage

High. Compatibility preservation is a repeated implementation constraint.

#### Representative implementations

- Operational slices preserve manifest keys, event names, CLI flags, JSON
  payloads, runtime APIs, and serialized models while separating internals.
- Inquiry-lineage slices preserve public compatibility objects while introducing
  private payload separation.
- Diagnostic inventory/shape audit preserves read-only diagnostic boundaries such
  as record scope, event-ledger behavior, and mutation flags.

#### Recurrence

Very high. Nearly every bounded slice reports no public compatibility change.

#### Ownership consistency

High. Preservation is a constraint on implementation change, not a new domain
owner.

#### Lexicon dependence

Low. Preservation is proven by unchanged tests, unchanged public objects, and
explicit compatibility notes.

#### Counterexamples

A preserved public object can hide newly separated implementation responsibilities.
Therefore public shape alone cannot disprove grammar; implementation-local
payloads and handoffs must be reviewed.

#### Confidence

High.

### 6. `A bounds B`, `A explains B`, `A derives B`, and `A selects B`

#### Implementation coverage

Medium-high. These forms are most visible in answer composition and inquiry
lineage.

#### Representative implementations

- `_DerivationLineagePayload` owns evidence, consumers, story impact, and
  unknowns that explain or bound derived conclusions.
- `_SelectionLineagePayload` owns candidates, selection factors, non-selected
  alternatives, evidence, and unknowns that explain or bound selection results.
- `_ComparisonLineagePayload` owns rationale, alternative references, and
  limitations that explain or bound a selected reference.
- Operational Story answer payloads separate answer material from reasoning,
  supporting evidence, authority boundary, and limitations.

#### Recurrence

Medium-high. These forms recur across multiple inquiry surfaces, but less broadly
than `A != B`, ownership, production/consumption, and preservation.

#### Ownership consistency

High inside lineage and answer surfaces. Medium outside those surfaces because
not every family explains, bounds, derives, or selects in the same way.

#### Lexicon dependence

Medium-low. The exact family term `Inquiry Lineage` stabilized only after
multiple result/lineage specializations; however, selection, derivation,
comparison, boundary, and limitation structures were visible first.

#### Counterexamples

`projection_shape` still exposes products beside consumption/influence/authority
fields without a private projection-result/influence-lineage handoff. The grammar
is visible but not fully recovered there.

#### Confidence

Medium-high.

### 7. `A observes B`

#### Implementation coverage

Medium-high. Observation is implementation-backed in Execution Visibility,
Observation-Derived Capability, diagnostic shape audits, and post-execution fact
extraction.

#### Representative implementations

- Execution Visibility observes execution, state-build, timing, cache, and
  diagnostic behavior without authorizing or executing operations.
- Observation-Derived Capability observes evidence and verification payloads
  without silently admitting cluster truth.
- Diagnostic shape audit observes implementation conformance against diagnostic
  declarations.
- Post-execution extraction observes a durable completed event rather than
  mutating execution recording ownership.

#### Recurrence

High in visibility and capability families; medium across all families.

#### Ownership consistency

High when paired with non-ownership boundaries. Observation is not mutation or
admission unless a specific implementation explicitly owns that behavior.

#### Lexicon dependence

Low. The grammar appears in read-only diagnostics, record scopes, mutation flags,
and evidence-inspection builders.

#### Counterexamples

Diagnostic findings must not silently become cluster truth. Writable admission or
cluster mutation requires separate implementation evidence.

#### Confidence

Medium-high.

### 8. `A does not own B`

#### Implementation coverage

High. Negative ownership is a recurring guardrail in family relationships and
compatibility handoffs.

#### Representative implementations

- Execution Visibility does not own operational authorization or execution.
- Answer Composition does not own source fact truth, cluster mutation, ledger
  writes, or capability admission.
- Inquiry Lineage does not own answer correctness, operational policy, capability
  truth, or execution status emission.
- Observation-Derived Capability does not own runtime operation realization.
- Compatibility Handoff does not own independent repository decisions or durable
  artifacts.

#### Recurrence

High. Negative ownership appears wherever families are orthogonal or where a
handoff crosses an ownership boundary.

#### Ownership consistency

High. The repository repeatedly uses non-ownership to prevent presentation,
compatibility, or diagnostic surfaces from becoming truth owners.

#### Lexicon dependence

Low. The form is visible from absence of mutation, read-only flags, unchanged
compatibility objects, and separation between producers and downstream consumers.

#### Counterexamples

Negative ownership cannot be inferred from a name alone. For example, a surface
that says `diagnostic` must still be checked for `record_scope`, ledger writes,
and mutation behavior.

#### Confidence

High.

## Relationship to responsibility recovery

Responsibility recovery can be explained by observed grammar.

The recurring recovery pattern was not primarily a naming exercise. It repeatedly
followed this implementation grammar:

```text
compressed concern
-> identify A != B
-> identify what A owns and what B owns
-> isolate one ownership boundary in implementation
-> preserve public compatibility
-> hand off through existing public surfaces where needed
-> stop before recovering a new family
```

This grammar explains why completed responsibility families could be bounded:
completion arrived when every recovered `A != B` boundary in the family chain had
implementation evidence, while remaining compression belonged to adjacent or
future families.

It also explains why compatibility handoff remained a pattern rather than a
family. Handoff appeared whenever an artifact crossed from one owner to another
or into a preserved public object, but the handoff never became the owner of the
artifact, decision, or durable behavior.

## Relationship to vocabulary stabilization

The evidence supports the observation:

```text
Stable vocabulary followed stable implementation grammar.
```

Examples:

- Operational Responsibility stabilized after repeated separations in the
  registered-operation path: recommendation, selection, validation,
  authorization, realization, recording, and extraction.
- Execution Visibility stabilized after repeated separations among status,
  timing, cache visibility, diagnostics, state-build visibility, and projection
  cache diagnostics.
- Observation-Derived Capability stabilized after evidence, verification,
  promotion readiness, inventory, and executable contract metadata were separated
  in implementation.
- Answer Composition stabilized after answer material, reasoning, support,
  authority boundary, and limitations recurred across surfaces.
- Inquiry Lineage vocabulary remained intentionally unstable even after several
  result/lineage forms existed, and only later became justified by recurrence
  across outcome, selection, derivation, and reference comparison surfaces.

The strongest counterexample investigation found no reviewed case where stable
family vocabulary legitimately preceded implementation grammar. The repository
contains presentation-only vocabulary warnings, and the implementation
responsibility inventory explicitly treats unsupported orientation labels as
insufficient evidence.

## Counterexamples: grammar before vocabulary

The most valuable counterexamples are cases where grammar was stable while
vocabulary remained unstable:

1. Inquiry-lineage slices showed `Outcome != Lineage Frame`,
   `Selection Result != Selection Lineage`, `Derived Conclusion != Derivation
   Lineage`, and `Reference Choice != Comparison Lineage` before cross-surface
   family vocabulary was stabilized.
2. Compatibility handoff recurred across events, inventories, diagnostics,
   answers, and lineage payloads before being classified. Its recurrence did not
   justify a family name; it justified a pattern classification.
3. Answer composition first appeared as repeated separation of answer material,
   reasoning, support, boundary, and limitations. The stable vocabulary followed
   the repeated payload grammar.
4. Capability evidence and executable operation contracts were separated before
   the read-only observation-derived capability chain could be described as a
   completed family.

These cases show that grammar can be observed independently of stable vocabulary.

## Unsupported grammar

The reviewed implementation evidence does not support these claims:

```text
Grammar owns repository behavior.
```

No implementation object, registry, engine, observer, schema, or runtime surface
owns grammar as a first-class domain.

```text
Every recurring handoff is a responsibility family.
```

Compatibility Handoff recurs but owns no independent decisions, durable
artifacts, behavior, or invariants.

```text
All responsibility families form one universal layer cake.
```

The family stack evidence supports a composition graph with compatibility
handoffs and orthogonal responsibilities, not a strict total order.

```text
Presentation vocabulary is implementation knowledge.
```

Repository instructions and inventory evidence explicitly reject unsupported
presentation labels as authority.

```text
Projection influence lineage is fully recovered.
```

`projection_shape` still carries result and influence-lineage pressure in the
same public stage shape without a private implementation-local recovery.

```text
Writable capability admission is recovered.
```

Observation-Derived Capability is complete for the read-only chain, not for a
future writable promotion/admission writer.

## Evaluation table

| Grammar form | Implementation coverage | Recurrence | Ownership consistency | Lexicon dependence | Confidence |
| --- | --- | --- | --- | --- | --- |
| `A != B` | High | Very high | High | Low | High |
| `A owns B` | High for concrete artifacts; medium for abstract labels | High | High when implementation-local | Medium-low | High/Medium |
| `A produces B` | High | High | High with downstream non-ownership | Low | High |
| `A consumes B` | High | High | High when source ownership remains upstream | Low | High |
| `A hands off to B` | High as pattern | High | High as pattern; low as family | Low | High as pattern |
| `A preserves B` | High | Very high | High as constraint | Low | High |
| `A bounds B` | Medium-high | Medium-high | High in answer/lineage surfaces | Medium-low | Medium-high |
| `A derives B` | Medium-high | Medium | High in reasoning-path surfaces | Medium-low | Medium-high |
| `A selects B` | Medium-high | Medium | High in selection/reference surfaces | Medium-low | Medium-high |
| `A explains B` | Medium-high | Medium-high | High in lineage/answer surfaces | Medium-low | Medium-high |
| `A observes B` | Medium-high | High in visibility/capability | High when read-only | Low | Medium-high |
| `A does not own B` | High | High | High | Low | High |

## Can architectural grammar already be observed?

Yes. Architectural grammar is already observable as recurring implementation
relation shape:

- separation of ownership (`A != B`);
- concrete ownership (`A owns B`);
- producer/consumer flow (`A produces B`, `A consumes B`);
- compatibility-preserving transfer (`A hands off to B`, `A preserves B`);
- lineage and answer relations (`A explains/bounds/derives/selects B`);
- read-only visibility (`A observes B`);
- negative ownership (`A does not own B`).

The observation is bounded: Seed can observe these forms manually from existing
implementation evidence, but the repository has not implemented a grammar
observer and this audit does not recommend implementing one as part of this
change.

## Can responsibility recovery be explained by observed grammar?

Yes. Completed responsibility families repeatedly became recoverable when the
implementation exposed enough relation grammar to identify ownership boundaries,
make one boundary explicit, preserve compatibility, and stop. The same grammar
also explains why some areas remain future work: the implementation still shows
compression or lacks private ownership separation.

## Is there sufficient evidence to justify making grammar observable later?

Yes, with constraints.

A future implementation step could make grammar observable only if it remains
read-only, implementation-backed, and bounded by existing evidence. It should not
invent a grammar engine, infer vocabulary from presentation labels, or promote
unsupported grammar into repository truth.

## Recommended next implementation step

Do not implement a grammar engine next.

The next natural implementation capability, if requested in a future bounded
slice, is a read-only, evidence-backed inventory/audit that reports already
observable grammar forms from existing implementation evidence. The smallest
safe path would be:

1. Define an implementation-owned source of grammar observations from already
   explicit artifacts such as diagnostic inventory entries, shape-audit specs,
   private payload pairs, and family audit evidence.
2. Keep every row tied to representative implementation evidence.
3. Mark unsupported and compressed forms explicitly.
4. Preserve read-only diagnostic boundaries: no cluster mutation, no event-ledger
   writes unless scoped as diagnostic runs, and no vocabulary migration.
5. Add tests proving the surface appears in diagnostic inventory and is checked
   by diagnostic shape audit if it becomes an operational diagnostic surface.

This recommended next step is intentionally future-facing. This audit itself does
not add that surface.

## Final confidence

High that Seed already exposes architectural grammar in implementation evidence.

High that `A != B`, ownership, production/consumption, handoff, preservation,
observation, and non-ownership are implementation-backed grammar forms.

Medium-high that explain/bound/derive/select forms are implementation-backed
outside inquiry and answer surfaces.

High that grammar stabilized before vocabulary in the reviewed family recovery
history.

Medium that a future read-only grammar visibility surface can be implemented
safely, because the surface would need careful diagnostic inventory and shape-audit integration to avoid creating invisible operational behavior.
