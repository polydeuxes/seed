# Selection Topology Pass 002

## Repository state examined

- `git rev-parse HEAD`: `128d09de3634695f44ae1fa1259cfcfe0732ad18`.
- `git status --short`: no output before this pass.
- PR 1743 is present in the surveyed checkout as `128d09d Characterize foundational Book of Seed kinds (#1743)`.
- `book_of_seed/characterization_pass_001.md` exists.

Repository evidence remains authoritative. Characterization Pass 001 bounded this pass by preserving that a selection artifact is not the act of selection, direct construction is not selection occurrence, selection is not authorization, execution, or inquiry opening, and read-only or non-mutating status does not by itself erase constitutional occurrence or movement.

## Selectors compared

Primary comparison:

- `seed_runtime/constitutional_view_selection.py::select_constitutional_views(...)`
- `seed_runtime/advancement_need_consideration_selection.py::select_advancement_need_for_consideration(...)`

Discriminating comparison used only as needed:

- `seed_runtime/closed_choice_selection_binding.py::bind_closed_choice_selection(...)`
- `seed_runtime/goal_inquiry_consideration_selection.py::select_goal_for_inquiry_consideration(...)`
- `seed_runtime/examination_work_selection.py::select_examination_work(...)`
- `seed_runtime/operational_realization_selection.py::select_operational_realization(...)`
- `seed_runtime/contextual_interpretation_selection.py::select_contextual_interpretation(...)`

## `select_constitutional_views(...)`

### Candidate set consumed

The selector consumes a `ConstitutionalQuestionProjection` and a tuple of `ConstitutionalCapabilityProjection` records. The practical candidate set is the supplied registered view capability projections, each with a `registered_view_name`, exact `capability_keys`, compatibility answer, and read-only boundary flags. The bounded question contributes exact `selection_keys`, not raw operator text or semantic intent.

### Focus evidence or rule

The focusing rule is deterministic exact-key comparison: `question_keys.intersection(capability.capability_keys)`. A matching capability key selects the registered view name; unsupported requested keys are preserved as uncertainty. There is no ranking, heuristic scoring, semantic judgment, evidence discovery, planning, or orchestration.

### Assertion produced

`SelectedConstitutionalViews` asserts that, for one bounded question ID and the supplied capability projections, these registered view names matched exact requested selection keys. It also asserts unsupported selection uncertainty, a narrow compatibility answer derived from selected capability answers, and boundary notes limiting the output to registered view names for composition.

### Standing effects

Selection success gives selected registered view names representation-standing for the constitutional view composition request. It makes those names acceptable as requested views for the composition adapter. It does not establish that the underlying constitutional views are newly true, does not admit new knowledge, does not open inquiry, and does not authorize or execute work.

### What remains unchanged

The raw bounded question, immutable constitutional views, read-model registrations, repository state, event ledger, cluster, and unselected registered views remain unchanged. Non-selected capability projections are not rejected; they simply did not match the exact requested keys.

### Selected subject

The selector selects read-model representations: registered constitutional view names matching exact keys. It does not select a standing-bearing advancement subject, a meaning, a movement, or an operational realization.

### Lawful non-selection

Yes. If no capability projection matches the exact requested keys, `selected_view_names` is empty and uncertainty includes both unsupported keys and a no-match note. This is a lawful artifact state, not an exception or authorization failure.

### Candidate-set identity and lineage validation

Identity validation is narrow. The selected artifact preserves `bounded_question_id`, but the function does not validate an external candidate-set fingerprint, provenance lineage, or that each capability projection belongs to a particular registered source lineage beyond the supplied projection fields. Its warrant is bounded to exact comparison over the caller-supplied projections.

### Downstream purpose boundary and artifact reuse

The safe downstream purpose is constitutional view composition through `selected_constitutional_views_to_composition_request(...)`, which passes only `selected_view_names` to `constitutional_view_composition_request(...)`. Reuse by another consumer would require that consumer to accept registered view names selected by exact-key comparison; the artifact does not carry a general warrant for other purposes.

### Lens, act, or both

Under the Book grammar, this owner is a read-only representation-selection act that also functions as a lens over supplied projections. It is lens-like because it exposes a bounded representation without mutating standing of the sources. It is still an act because a bounded choice occurs: exact keys choose zero or more registered view names and preserve unsupported keys. Read-only status does not prove that no constitutional occurrence happened.

### Distinction from ranking, admission, authorization, routing, and execution

It does not order candidates, admit evidence or knowledge, grant permission, select a route, or execute a tool. Exact deterministic comparison is not semantic judgment.

## `select_advancement_need_for_consideration(...)`

### Candidate set consumed

The selector consumes one `AdvancementNeedReferenceSet`. Its visible candidates are the reference set's `references`, each binding need set, prior selection ID, goal establishment, horizon, family, native projection, native lineage, native bucket, native standing, visibility, selectability, and conflict state.

### Focus evidence or rule

The focusing evidence is explicit `NeedFocusEvidence` naming one exact visible advancement-need reference. The selector validates that the evidence references the same need set, selected goal, goal establishment, bounded horizon, need family, native projection, and native lineage. It refuses missing identity, ambiguity, conflict, absent references, duplicate lineage conflict, non-selectable references, and reference mismatches. Uniqueness, sufficiency reasons, standing labels, presentation order, family, wording similarity, severity, or selectable count do not select a need.

### Assertion produced

`AdvancementNeedConsiderationSelection` asserts a selection state over one exact reference set. In the selected state, it asserts that one established selectable native need reference is the selected reference for consideration, while preserving visible references and non-selected references. In non-selected states, it preserves why no exact focus selection succeeded.

### Standing effects

Selection success gives one already-established advancement-need reference bounded focus-standing for consideration. It establishes which native need may be carried to a next consideration boundary by consumers such as bounded inquiry frontier testimony. It does not make the need true, does not make it highest priority, does not select a resolution, next action, realization, or route, and does not open inquiry or request authority.

### What remains unchanged

The underlying `GoalAdvancementNeedSet`, native need projections, reference set, other visible references, need family standings, event ledger, cluster, and downstream movement authorities remain unchanged. Non-selected references remain visible alternatives, not rejected needs.

### Selected subject

The selector selects a subject for consideration: one exact advancement-need reference with lineage identity. It is not merely representation selection; it confers bounded focus-standing on an already-established need for one downstream consideration purpose.

### Lawful non-selection

Yes. `selection_state` includes `no_focus_evidence`, `missing_identity`, `ambiguous`, `conflict`, `reference_mismatch`, `absent_reference`, `duplicate_lineage_conflict`, and `non_selectable`. These lawful non-selection states preserve uncertainty and conflicts rather than inventing a selection from uniqueness or eligibility.

### Candidate-set identity and lineage validation

Yes. The selector checks the focus evidence against reference-set identity fields and native lineage fields, then checks that the named reference is present exactly once, not conflicted, and selectable. Candidate eligibility remains distinct from selection: a selectable unique candidate is still not selected without exact focus evidence.

### Downstream purpose boundary and artifact reuse

The selected artifact becomes authoritative only for bounded advancement-need consideration. Downstream consumers must validate the selected state and identity. For example, inquiry frontier boundary testimony requires a selected inquiry-family advancement need plus matching native lineage and separate frontier-boundary testimony; it does not treat the selection artifact as inquiry opening or authorization. Another consumer can safely reuse the artifact only if it accepts the same reference set, identity, lineage, state, and purpose boundary.

### Lens, act, or both

This owner is a read-only selection act over a reference-set lens. It consumes a projected reference set, but the selector itself changes bounded standing by declaring one reference selected for consideration when exact focus evidence validates. Non-mutating status does not make it merely a lens.

### Distinction from ranking, admission, authorization, routing, and execution

It does not rank needs, admit new need evidence, grant authority, route work, open inquiry, select operational realization, execute, record, write the event ledger, or mutate cluster state.

## Candidate-set and focus-evidence differences

The constitutional view selector consumes representation capability projections and focuses by exact deterministic overlap between requested keys and capability keys. Its selected candidates are registered view names, possibly many, and the output is bounded to composition inputs.

The advancement-need selector consumes visible advancement-need references derived from a need set and focuses by explicit evidence naming one exact reference with full identity and lineage. Its selected candidate is at most one already-established selectable need reference, and the output is bounded to consideration standing.

This difference is not only a difference in artifact fields. It changes the constitutional kind of selected subject and the warrant required for selection. Exact key comparison can warrant representation selection; bounded focus over an already-established need requires identity, lineage, and selectability checks because its result gives one subject consideration standing.

## Assertions produced

- `SelectedConstitutionalViews`: these registered view names match exact requested keys for one bounded question and are usable as composition inputs; unsupported keys remain uncertain.
- `AdvancementNeedConsiderationSelection`: this exact visible advancement-need reference is selected for consideration, or lawful non-selection preserves the reason no such focus standing was established.

## Standing effects

Shared standing effect: each selector produces a bounded selection result and preserves non-effects. Direct dataclass construction alone would not prove the validated act occurred.

Discriminating standing effect: constitutional view selection establishes representation suitability for a downstream composition purpose; advancement-need consideration selection establishes bounded focus-standing for one already-established advancement need. The latter is standing-bearing selection in a way the former is not automatically, because it selects a constitutional subject for consideration rather than a representation to render.

## Non-selection behavior

Both permit lawful non-selection. Constitutional view selection returns an empty selected tuple with uncertainty when no registered view matches. Advancement-need consideration selection returns explicit non-selected states for missing, ambiguous, conflicting, absent, mismatched, duplicate-lineage, or non-selectable focus evidence. Neither may convert unique eligibility into selection.

## Downstream purpose boundaries

- `SelectedConstitutionalViews` is consumed by a composition adapter that forwards selected registered view names only. Consumer acceptance by composition does not create a producer-side warrant for any other consumer.
- `AdvancementNeedConsiderationSelection` is consumed by later advancement/inquiry owners only after selected state, family, reference, and lineage checks. It does not itself open downstream movement.

Selection result is not authorization and is not downstream movement opened. A selected artifact may be consumed later without making the selector responsible for every downstream occurrence.

## Shared constitutional characteristics

The inspected selectors support a shared higher-order selection grammar:

1. A bounded candidate set is supplied or projected before selection.
2. A rule, policy, or explicit evidence focuses the selection.
3. The result preserves selected and non-selected alternatives or a lawful non-selection reason.
4. Selection artifacts are distinct from the validated acts that produce them.
5. Read-only and non-mutating flags preserve side-effect boundaries but do not erase constitutional occurrence.
6. Selection is not ranking, admission, authorization, routing, execution, or recording unless an owner explicitly says so.

Closed-choice selection binding, goal consideration selection, examination work selection, operational realization selection, and contextual interpretation selection confirm the shared grammar while also showing that repository selection owners differ by subject and downstream boundary. Closed-choice binding binds a token inside one presented set; goal and advancement selectors focus subjects for consideration; examination and operational realization selectors apply policy to work or realization candidates; contextual interpretation selection chooses meaning from candidate-bound evidence.

## Discriminating differences

The evidence supports distinct subfamilies rather than a single undifferentiated selection act family:

- **Representation selection:** `select_constitutional_views(...)` selects zero or more registered read-model representations by exact key comparison for composition. It is lens-like and representation-bounded.
- **Consideration selection:** `select_advancement_need_for_consideration(...)` selects zero or one already-established advancement-need reference by explicit focus evidence, identity checks, and lineage checks for consideration. It gives a subject bounded focus-standing.
- **Meaning selection:** contextual interpretation selection selects one warranted interpretation candidate from explicit candidate-bound evidence and stops before admission or goal binding.
- **Policy/work or realization selection:** examination work and operational realization selection apply policy to eligible candidates and preserve future handoffs without authorizing or executing.
- **Closed-choice binding:** closed-choice selection binds a captured token to one exact presented choice set and stops before applying that choice to a goal or inquiry frontier.

These are not separate merely because dataclass fields differ; they differ in candidate-set identity, focus warrant, selected subject, and downstream authority boundary.

## Book chapters updated

- `book_of_seed/02-acts-and-constraints/selection-artifacts-and-selection-acts.md` now distinguishes shared selection grammar from representation, consideration, meaning, policy/work, realization, and closed-choice binding subfamilies.
- `book_of_seed/02-acts-and-constraints/acts-and-act-artifacts.md` now clarifies that read-only non-mutating selection may still be an occurrence, while direct construction remains insufficient.
- `book_of_seed/01-grammar-and-standing/lenses-views-and-roads.md` now corrects the overbroad claim that read-only selection or composition is not constitutional movement, replacing it with a narrower distinction between representation-lens selection and standing-bearing selection.
- `book_of_seed/03-goals-and-advancement/selection-and-authorization.md` now distinguishes representation selection from consideration selection and preserves that neither authorizes action.
- `book_of_seed/concordance.md` now indexes representation selection, consideration selection, and standing-bearing selection as durable distinctions supported by this pass.

## Remaining unresolved questions

- Whether every future repository selector can be classified under the subfamilies above remains unresolved; this pass intentionally did not build a repository-wide selection inventory.
- Whether representation selection can ever become standing-bearing for a non-composition consumer remains unresolved and would require consumer-side acceptance evidence.
- Whether operational realization selection creates constitutional movement beyond focus-standing remains unresolved here; this pass only confirms that it is distinct from authorization and execution.
- Whether the existing constitutional view selector should validate a candidate-set fingerprint or richer lineage remains an implementation question outside this characterization pass.

## Bounded resolution

shared higher-order family with distinct subfamilies supported
