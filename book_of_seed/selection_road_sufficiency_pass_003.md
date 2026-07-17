# Selection Road Sufficiency Pass 003

## Repository state examined

- `git rev-parse HEAD`: `79a9a0850b3a37cedfa2d1c3bde20dce5ce91003`.
- `git status --short`: no output before this pass.
- PR 1744 is present in the surveyed checkout as `79a9a08 (HEAD -> work) Add selection topology pass 002 (#1744)`.
- `book_of_seed/selection_topology_pass_002.md` exists.

Repository evidence controls this pass. Book chapters and boundary notes are treated as testimony unless function bodies, artifact fields, validation branches, identity generation, candidate construction, lineage preservation, tests, or direct consumers support them.

## Primary roads compared

### Road A: constitutional view selection to composition

```text
select_constitutional_views(...)
→ SelectedConstitutionalViews
→ selected_constitutional_views_to_composition_request(...)
→ build_constitutional_view_composition(...)
```

This road is a representation-selection road. It chooses registered constitutional read-model view names for bounded composition.

### Road B: advancement-need consideration selection to inquiry-frontier consumers

```text
select_advancement_need_for_consideration(...)
→ AdvancementNeedConsiderationSelection
→ preserve_inquiry_frontier_boundary_testimony(...)
→ assemble_bounded_inquiry_frontier(...)
```

This road is a consideration-selection road. It selects one already-visible and already-established advancement-need reference for bounded focus, then later consumers preserve or assemble inquiry-frontier material only if the selected subject remains identity-bound.

## Producer-side assertions and warrants

### Road A producer assertion

`select_constitutional_views(...)` establishes this bounded assertion only:

```text
for this bounded_question_id, these registered view names have capability keys
that exactly intersect the question projection's requested selection keys;
unsupported requested keys remain uncertain; the output is read-only and non-mutating.
```

The warrant is implementation-local:

- `project_constitutional_question(...)` carries the bounded question ID and exact caller-declared `selection_key` fields into `ConstitutionalQuestionProjection`.
- `project_constitutional_capabilities(...)` regenerates capability projections from registered read-model contracts and builders.
- `_capability_keys_from_source(...)` maps concrete registered view artifact types to exact capability keys: process, governance, and fidelity.
- `select_constitutional_views(...)` uses set intersection between `question_projection.selection_keys` and each `capability.capability_keys`; matched projections contribute `registered_view_name`, unmatched requested keys become `unsupported selection key: ...`, and empty selection becomes explicit uncertainty.
- The producer sets read-only/non-mutating/event-ledger flags from the input projections and then returns `mutates_cluster=False` and `writes_event_ledger=False`.

The producer does not assert semantic relevance, candidate-set completeness beyond the supplied capability projections, capability-projection lineage, priority, authority, inquiry opening, or downstream movement.

### Road B producer assertion

`select_advancement_need_for_consideration(...)` establishes this bounded assertion in the selected state:

```text
for this exact advancement-need reference set and exact focus evidence,
one visible selectable reference, already bound to the same need set, selected goal,
goal establishment, bounded horizon, need family, native projection, and native lineage,
is selected for bounded consideration.
```

In non-selected states it instead establishes why exact focus selection did not succeed: no focus evidence, missing identity, ambiguity, conflict, reference mismatch, absent reference, duplicate lineage conflict, or non-selectable reference.

The warrant is identity- and lineage-heavy:

- `_selection_id(...)` computes a stable selection ID from `reference_set.reference_set_id` and every focus-evidence field used by the selector.
- The candidate universe is `reference_set.references`, produced by `project_advancement_need_reference_set(...)` from supplied family projections in one `GoalAdvancementNeedSet`.
- The selector rejects missing, ambiguous, conflicting, and non-exact focus evidence before selecting.
- It requires exact focus evidence to name one reference ID.
- It requires focus evidence to match the reference set's `need_set_id`, `selection_id`, `goal_establishment_id`, and `horizon_id`, and to carry family, native projection ID, and native lineage.
- It requires exactly one visible reference with the named ID.
- It rejects mismatched family/projection/lineage, duplicate-lineage conflicts, and non-selectable references.
- It selects only references whose native bucket and standing made them selectable in the reference set.

The producer does not assert priority, primary blocker status, resolution, route, next action, inquiry opening, authority request, authorization, execution, recording, event-ledger write, or mutation.

## Artifact-preservation comparison

### Road A artifact preservation

`SelectedConstitutionalViews` preserves:

- `bounded_question_id`;
- selected registered view names;
- selection uncertainty, including unsupported keys and empty selection;
- a narrow compatibility answer derived from selected capability answers;
- read-only boundary notes and operational flags.

It intentionally omits:

- a candidate-set fingerprint;
- full capability-projection lineage;
- full non-selected registered views;
- full non-selected capability keys;
- the raw bounded question;
- immutable constitutional view artifacts;
- semantic or evidentiary basis beyond exact key matching.

Those omissions are not defects for this road because the direct adapter forwards only selected registered view names into a composition request, and composition independently validates that those names are registered before composing. The artifact is sufficient for the narrow assertion: selected registered names matched exact requested keys for this bounded composition purpose.

### Road B artifact preservation

`AdvancementNeedConsiderationSelection` preserves:

- stable `selection_id`;
- `reference_set_id`, `need_set_id`, selected goal ID, and `horizon_id`;
- focus evidence refs and provenance refs;
- selection state;
- the selected reference when selection succeeds;
- visible references and non-selected references;
- ambiguous IDs, missing-identity evidence refs, mismatch evidence refs, absent IDs, duplicate-lineage IDs, non-selectable IDs;
- unknowns and conflicts;
- negative authority/effect flags and boundary notes.

This preservation is necessary locally because later consumers receive a selected subject with bounded focus standing, not merely a representation name for rendering. The selected subject must remain traceable to the same native projection and lineage so that inquiry-frontier consumers do not accidentally attach testimony or frontier assembly to a different need.

### Direct test of pass-002 preservation language

Pass 002's broad language that selection results preserve selected and non-selected alternatives or a lawful non-selection reason is too strong if read as a universal artifact schema. Road A does not preserve the full non-selected candidate set, yet the road remains locally sufficient because its producer assertion and direct consumer purpose need only registered view-name selection plus composition-side registration validation. Road B preserves visible and non-selected references because its local contract makes subject identity and focus standing material.

The durable grammar supported by repository evidence is narrower:

```text
A selection result must preserve the bounded selection assertion and enough evidence
for its intended consumer to distinguish lawful selection from unsupported omission.
Preservation of all non-selected alternatives is selector-specific.
```

## Consumer-side validation comparison

### Road A consumer validation

`selected_constitutional_views_to_composition_request(...)` performs no validation beyond constructing a `ConstitutionalViewCompositionRequest` from `artifact.selected_view_names`. The substantive consumer validation occurs in `build_constitutional_view_composition(...)`, which builds a contract map from registered constitutional read-model contracts and rejects any requested view name that is not both registered and buildable.

Composition validates registered-name admissibility. It does not validate the original bounded question ID, requested selection keys, producer identity, capability-projection universe, unsupported keys, or whether the artifact came from `select_constitutional_views(...)`. Thus Road A's lawful reliance is narrow: composition can safely rely on the artifact as a source of explicit requested registered view names, not as a general proof of constitutional selection standing.

### Road B consumer validation

`preserve_inquiry_frontier_boundary_testimony(...)` validates that the selection is in selected state and that the selected reference exists and belongs to the inquiry family before preserving selected-need identity, native projection, native lineage, need set, selected-goal binding, horizon, and lineage-derived testimony/component/subject refs. If those conditions fail, it returns a testimony artifact with no selected inquiry subject.

`assemble_bounded_inquiry_frontier(...)` independently checks selected state and selected reference presence, then compares testimony identity back to the selected reference: selected reference ID, native projection ID, native lineage, need-set ID, selected-need selection ID, selected-goal ID, and horizon ID. It also requires operative clause families with established inquiry disposition and no material binding conflict before the frontier becomes established.

Road B consumers validate more because their local purpose depends on the selected subject's standing and lineage, not merely mechanical type acceptance.

## Candidate-set and selected-subject identity

### Road A

Candidate-set identity is implicit in the supplied `capability_projections` tuple and the registered contracts/builders used to produce it. No stable candidate-set fingerprint is preserved in `SelectedConstitutionalViews`. The selected-candidate identity is the tuple of registered view names. This is enough for composition because composition rechecks those names against registered contracts and builders and then rebuilds the contributing views.

The first unsupported assertion would appear if a caller treated `SelectedConstitutionalViews` as proof that the selected views were semantically best, complete against all possible constitutional views, lineaged to a specific capability-projection snapshot, authorized for another consumer, or sufficient for movement beyond composition. The implemented road itself does not make those assertions.

### Road B

Candidate-set identity is explicit: `reference_set_id` plus the `visible_references` snapshot and reference-set bindings to need set, selected goal, goal establishment, and horizon. Selected-candidate identity is the complete `AdvancementNeedReference` with reference ID, need-set ID, selection ID, goal-establishment ID, horizon ID, family, native projection ID, native lineage, native bucket, native standing, evidence refs, quality, visibility, selectability, and conflict state.

The first unsupported assertion would appear if a caller treated the selected need as priority, blocker, route, inquiry opening, authorization, or execution. The selector and consumers explicitly refuse those effects.

## Purpose boundaries

Road A encodes or implies a composition purpose. The adapter defaults `composition_purpose` to `bounded_explanation` and forwards only selected view names. Its result is suitable input for constitutional view composition, not reusable authority for unrelated selection families.

Road B encodes a consideration purpose. The selected need receives bounded focus standing for later inquiry-frontier preservation or assembly, but the artifact's own flags and boundary notes deny route selection, inquiry opening, authority request, authorization, execution, recording, event-ledger writes, and mutation.

## Safe and unsafe reuse

### Road A safe reuse

Safe reuse is limited to consumers that need explicit registered constitutional view names and independently validate registration/buildability. The evidence preventing unsafe reuse is composition-side rejection of unsupported names and the artifact's narrow fields and boundaries.

Unsafe reuse includes treating selected view names as semantic proof, capability completeness, general constitutional standing, authorization, or evidence that another consumer's candidate universe was selected from.

### Road B safe reuse

Safe reuse is limited to consumers that need one selected advancement-need reference and independently revalidate selected state, family, reference identity, need-set identity, selected-goal identity, horizon identity, native projection, and native lineage. Inquiry-frontier testimony and frontier assembly show this pattern.

Unsafe reuse includes bypassing those checks or using the selected need as if it were a priority, blocker, opened inquiry, selected source, selected observation, realization, authority request, authorization, execution, or recording.

## Direct-construction bypass analysis

### Road A

A mechanically constructed `SelectedConstitutionalViews` can bypass `select_constitutional_views(...)` and still satisfy the adapter because the adapter merely copies `selected_view_names` into a composition request. It can satisfy composition if the names are registered and buildable. That means consumer acceptance proves registered-name admissibility for composition, not that the producer-side exact-key selection occurred. Direct construction therefore weakens producer-side warrant but not composition's local registration check.

### Road B

A mechanically constructed `AdvancementNeedConsiderationSelection` can bypass `select_advancement_need_for_consideration(...)`. Later consumers partially defend against this by checking selected state, inquiry family, and identity consistency between selection and testimony. However, a forged internally consistent artifact with a selected reference could satisfy those consumer checks unless the consumer also had access to and revalidated the original reference set and focus evidence. The current direct consumers validate selected-subject coherence for their own purpose; they do not prove the producer act occurred. Therefore direct construction proves artifact constructibility, not selection occurrence.

## Universal obligations supported

Repository evidence supports these obligations across the compared roads:

- A selection road must have a bounded producer assertion.
- The selected subject or representation identity needed by the intended consumer must be preserved.
- The road must preserve enough basis, uncertainty, or refusal information for the intended consumer to avoid unsupported omission.
- The consumer must validate the invariants material to its own purpose; type acceptance alone is not lawful reliance.
- Selection purpose must remain bounded and must not become reusable authority automatically.
- Direct dataclass construction does not prove the producer-side selection act occurred.
- Selection does not itself authorize execution, recording, event-ledger writing, cluster mutation, or downstream movement unless the responsible boundary explicitly establishes that effect.

Repository evidence does not support a universal obligation to preserve a full candidate-set fingerprint, full non-selected alternatives, full lineage, producer identity, or a common selection envelope for every selection road.

## Subfamily-specific obligations supported

### Representation selection

Representation selection may be sufficient with exact selected representation identity, bounded requested-key basis, unsupported-key uncertainty, and consumer-side registration validation when the consumer only needs explicit registered representations for rendering or composition.

### Consideration selection

Consideration selection needs stronger subject-binding evidence: reference-set identity, need-set identity, selected goal, goal establishment, bounded horizon, family, native projection, native lineage, selection state, selected reference, visible/non-selected references or lawful non-selection state, and downstream identity revalidation. These obligations arise because the selected subject receives bounded focus standing.

### Other selection families

Meaning selection, work selection, realization selection, and closed-choice binding are not inventoried here. The comparison supports treating their obligations as local to candidate universe, effect, and consumer purpose rather than deriving them from a universal artifact schema.

## Standing-bearing terminology determination

`standing-bearing selection` should not be preserved as a settled durable selection subfamily. Repository evidence supports it as a cross-cutting property: some selections establish a kind of standing for the selected subject, and the required checks depend on what standing is established.

The comparison is decisive locally:

- A selected constitutional view name is suitable input for composition. It has representation suitability, not focus standing over a constitutional subject.
- A selected advancement need has bounded focus standing for consideration, subject to identity and lineage checks.

The more accurate durable terms are `representation selection`, `consideration selection`, and `selection standing` as a bounded effect/property of a selected subject. `Selection standing` remains distinct from authorization standing.

## Claims contradicted

- The claim that every selection result must preserve all non-selected alternatives is contradicted by Road A's sufficient narrow artifact and composition consumer.
- The claim that consumer acceptance of an artifact type proves producer-side selection occurrence is contradicted by both roads' direct-construction bypasses.
- The claim that richer artifacts are automatically more lawful is unsupported; Road B is richer because its consumer purpose requires subject standing and lineage, not because richness itself creates lawfulness.
- The claim that thin artifacts are automatically insufficient is contradicted by Road A's local composition contract.
- The claim that `standing-bearing selection` is a durable concordance category is unsupported; the supported durable concept is selection standing as a cross-cutting effect.

## Claims remaining unresolved

- Whether another Road B consumer revalidates the original reference set and focus evidence more completely than inquiry-frontier consumers remains outside this local pass.
- Whether future constitutional view consumers would require candidate-set fingerprints, capability-projection lineage, or preserved non-selected views remains consumer-specific and unresolved.
- Obligations for meaning selection, work selection, operational-realization selection, and closed-choice binding remain local hypotheses until separately surveyed.
- Producer identity as a universal obligation remains unsupported by the two primary roads; some future road may require it locally.

## Book chapters updated

- `book_of_seed/02-acts-and-constraints/selection-artifacts-and-selection-acts.md` updates the bounded resolution, distinctions, and failure modes to separate bounded selection assertion from selector-specific preservation of non-selected alternatives.
- `book_of_seed/01-grammar-and-standing/lenses-views-and-roads.md` updates road language to distinguish representation suitability from selection standing and consumer validation.
- `book_of_seed/01-grammar-and-standing/constructors-and-production-authority.md` updates constructor failure modes to include selection-artifact bypasses.
- `book_of_seed/03-goals-and-advancement/selection-and-authorization.md` updates selection standing language while preserving selection != authorization.
- `book_of_seed/concordance.md` replaces `standing-bearing selection` as a category with `selection standing` as a cross-cutting effect.

## Bounded resolution

Both roads require different but sufficient local contracts.
