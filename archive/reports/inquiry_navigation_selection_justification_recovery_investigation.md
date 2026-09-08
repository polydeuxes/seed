# Inquiry Navigation Selection Justification Recovery Investigation

## Executive answer

The repository already has an implementation-backed bounded competency for explaining **some** selection decisions: `selection_path_audit`. It answers why an already-implemented selection target was selected by preserving the selected value, candidate set, selection factors, non-selected candidates, supporting evidence, outcome, unknowns, and read-only boundary.

That competency is **not** a general inquiry-target selector and does **not** currently compare all eligible `QuestionFamily` candidates to choose the next inquiry surface. Bounded ask selection in `question_surface_inventory` is exact map-backed dispatch after a caller has already supplied a `QuestionFamily`; it does not rank or reject competing inquiry surfaces. `InquiryOrientation` only finds related material by lexical overlap and does not select the inquiry target.

Therefore the recovered answer is:

- **Implemented selection explanation exists** for explicit targets handled by `selection_path_audit`.
- **Competing candidates are preserved** inside the specific pressure/current-focus selection lineage, not as a repository-wide set of eligible inquiry surfaces.
- **The evidence for “stronger than alternatives” is currently pressure-audit ordering**: descending score, then category name, plus each candidate’s reason/evidence.
- **The implementation stops** at read-only explanation/visibility. It does not mutate selection behavior, record facts, write the event ledger, change cluster state, infer targets, or plan next work.
- **Selection justification is currently an implementation competency**, not yet a standalone responsibility family for inquiry target selection.

## Implementation evidence reviewed

Primary implementation evidence:

- `seed_runtime/selection_path_audit.py`
- `seed_runtime/question_surface_inventory.py`
- `seed_runtime/inquiry_orientation.py`
- `scripts/seed_local.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`

Primary test evidence:

- `tests/test_selection_path_audit.py`
- `tests/test_question_surface_inventory.py`

Architectural and recovery reports reviewed as secondary evidence:

- `answer_composition_projection_navigation_audit.md`
- `selection_path_answer_composition_completion_audit.md`
- `responsibility_family_completion_inquiry_audit.md`
- `architectural_inquiry_orientation_surface_audit.md`
- `question_bounded_work_invocation_investigation.md`
- `question_bounded_work_invocation_slice_002.md`
- `question_bounded_work_invocation_slice_003.md`
- `question_bounded_work_invocation_slice_004.md`
- `inquiry_identity_ontology_investigation.md`
- `inquiry_subject_resolution_investigation.md`
- `inquiry_anchor_dependency_head_investigation.md`
- `responsibility_to_inquiry_boundary_audit.md`
- `responsibility_family_vs_competency_recovery_investigation.md`
- `responsibility_evaluation_competency_recovery_investigation.md`
- `evidence_interpretation_competency_recovery_investigation.md`

Implementation and tests were treated as stronger authority than architectural prose.

## Current selection behavior

### Exact inquiry-family dispatch

`question_surface_inventory` declares the bounded ask dispatch map from exact `QuestionFamily` strings to existing surfaces. The entry relevant to this investigation is:

```text
selection explanation -> selection_path
```

The same module declares that `selection explanation` requires the caller to provide a `target` argument. This is important: bounded ask does not infer the target or select the selection surface from prose. It selects a dispatch surface only after the exact family has already been supplied and eligibility has already passed.

The bounded work selection function confirms the boundary. It checks that eligibility corresponds to the same question family, rejects non-permitted eligibility, selects the dispatch surface from the static map, forwards required surface args when present, and returns a `BoundedWorkSelectionResult`. Its docstring states that it does not decide eligibility, dispatch execution, answer composition, rendering, or evidence semantics.

### Selection-path target handling

`build_selection_path_audit(state, target, repo_root=...)` is the implementation point that explains selection for a supplied target. It normalizes the target and obtains pressure and operational-story evidence. It then recognizes these implemented selection targets:

- `current_focus`
- `primary_pressure`
- the current operational story focus
- a target matching one of the pressure categories

For those targets, the selected item is derived from the first pressure candidate when pressure candidates exist, and the result is assembled from pressure selection lineage.

If the target is not an implemented selection surface, the builder returns `selected="unknown"`, `selection_factors=["unknown"]`, no selected evidence, and an explicit unknown explaining that no implementation-backed selection evidence was discovered.

### CLI path

The CLI invokes selection-path behavior only when `--selection-path` is explicitly supplied. It builds the audit from projected state and the supplied target, then renders JSON or human output. This preserves the implementation boundary: selection explanation is a diagnostic surface, not an implicit planner or automatic inquiry router.

## Current justification behavior

`SelectionPathAudit` is the current implementation-backed object that preserves selection justification. Its fields include:

- `target`
- `selected`
- `candidates`
- `selection_factors`
- `non_selected`
- `evidence`
- `outcome`
- `unknowns`
- `boundary`

The pressure/current-focus path gives the strongest current evidence for selecting one surface over another. It records the candidate set by enumerating pressure items with rank, score, reason, and evidence. It records the selection factor as:

```text
pressure audit orders candidates by descending score, then category name
```

It records non-selected candidates from all pressure candidates after the selected item. For each non-selected candidate, the reason is computed relative to the selected item. Therefore the repository can answer:

- why the selected pressure/current-focus target won;
- what alternatives were visible;
- why those alternatives were not selected;
- which evidence supports the decision.

That answer is bounded to the implemented pressure/current-focus selection path. It is not evidence that Seed has a generic inquiry-surface ranking engine.

## Current stopping point

The implementation terminates at read-only selection explanation.

`SelectionPathAudit.boundary` declares:

- `mode="read_only_selection_audit"`
- `records_facts=False`
- `writes_event_ledger=False`
- `mutates_cluster=False`

The diagnostic inventory repeats that `selection_path` supports JSON, does not support record, has `record_scope="none"`, does not emit diagnostic or cluster facts, does not write the event ledger, and does not mutate the cluster.

Tests preserve this stopping point by proving that selection-path output does not change operational-story selection and does not write events or mutate projected facts.

The stopping point is also visible in the unknown-target path. When target-specific selection logic is unavailable, the implementation returns an explicit unknown instead of inferring a target, creating a planner, ranking unrelated surfaces, or fabricating justification.

## Implementation-backed competency

The recovered competency is:

> **Selection Justification Visibility**: bounded read-only work that consumes already-implemented selection evidence, preserves selected result, candidates, factors, non-selected alternatives, support, outcome, unknowns, and authority boundary, and renders that material without changing the underlying selection behavior.

This competency is implementation-backed by:

- `SelectionPathAudit` as the public evidence/visibility object;
- private result, reason, supporting-evidence, and lineage payloads as local compatibility handoff structure;
- `_from_pressure_selection(...)` as the currently implemented selection-justification producer for pressure/current-focus selection;
- the CLI `--selection-path` surface;
- diagnostic inventory and diagnostic shape-audit registrations;
- tests proving visible candidates, factors, alternatives, evidence, unknowns, no recording, no event writes, no cluster mutation, and no behavioral change to operational story.

## Responsibility family assessment

Selection justification is **currently a competency, not a full responsibility family** for inquiry target selection.

Reasons:

1. The implemented selection-path owner is a surface-specific diagnostic/audit owner, not a family-spanning chain from inquiry candidate generation through candidate comparison, selection, rejection, and downstream answer composition.
2. `question_surface_inventory` preserves bounded ask dispatch and eligibility, but the dispatch selection is exact-map lookup after the caller supplies a question family. It does not preserve competing eligible `QuestionFamily` candidates or reject alternatives.
3. `InquiryOrientation` collects related material by lexical overlap and preserves uncertainty/boundary. It does not select a target and does not compare eligible inquiry surfaces.
4. Existing prose reports repeatedly describe inquiry navigation and answer composition boundaries, but implementation authority still comes from the surface-specific code and tests above.

A responsibility family may emerge later if implementation adds a recurring chain that preserves eligible inquiry candidates, compares them, selects one, explains rejected alternatives, hands off to the selected surface, and stops before answer composition. That chain is not currently implemented as a general family.

## Counterexamples

The following counterexamples were actively checked:

### Manual operator judgment

Bounded ask requires exact `QuestionFamily` strings and, for selection explanation, an explicit `target`. This means the operator/caller supplies the identity that starts dispatch. There is no implemented free-text judgment that chooses the inquiry target.

### Hard-coded investigation order

`BOUNDED_ASK_DISPATCH_SURFACES` is a static map. It is dispatch evidence, not a ranked investigation order. The map can prove surface eligibility and dispatch destination, but not why one eligible inquiry family should be selected over another.

### No preserved competing inquiry candidates

For inquiry surfaces generally, competing eligible `QuestionFamily` candidates are not preserved. The preserved competing candidates exist inside `SelectionPathAudit` for pressure/current-focus selection, not across all eligible inquiry targets.

### Selection without justification

Exact bounded-work dispatch does select a surface from the map, but its reason is only “selected bounded ask dispatch surface” or “selected parameterized bounded ask dispatch surface.” That is sufficient for dispatch visibility, not for comparing inquiry alternatives.

### Planner-only behavior

No planner implementation was found. The current implementation either dispatches exact families, or returns read-only audit/orientation output from existing evidence.

### Answer composition instead of navigation

`selection_path_audit` has answer-like rendering and compatibility handoff, but the actual selection-justification evidence remains candidate/factor/alternative lineage. It is not merely answer composition, and answer composition does not select the target.

### Surface dispatch without comparison

This counterexample is real for bounded ask. `bounded_work_selection_for_question_family(...)` dispatches one exact family to one surface without preserving rejected eligible alternatives. That disproves the hypothesis that generic inquiry target selection justification is already implemented.

## Questions answered

### 1. Where is inquiry target selection currently observable?

It is observable in two different, bounded senses:

1. **Question-family to surface dispatch** is observable in `question_surface_inventory`: exact `QuestionFamily` values map to dispatch surfaces, including `selection explanation -> selection_path`.
2. **Selection explanation for a supplied target** is observable in `selection_path_audit`: `build_selection_path_audit(...)` handles implemented targets and returns selected result, candidates, factors, alternatives, evidence, outcome, unknowns, and boundary.

There is no implementation evidence for a general inquiry-target selector that chooses among all eligible inquiry surfaces.

### 2. Where are competing inquiry targets preserved?

Competing targets are not preserved as a general inquiry-candidate set. The closest implemented preservation is inside `SelectionPathAudit.candidates` and `SelectionPathAudit.non_selected`, where pressure/current-focus selection candidates and rejected alternatives are retained.

For bounded ask, `QuestionSurfaceInventoryRow` preserves known families and their eligibility/dispatch status, but not a per-inquiry candidate set or rejection rationale.

### 3. What evidence currently determines that one inquiry surface is stronger than another?

For the implemented selection-path pressure/current-focus case, strength is determined by pressure-audit ordering: candidates are ordered by descending score, then category name. Candidate rows preserve score, reason, and evidence.

For generic inquiry surfaces, no implementation-backed “stronger than another eligible inquiry surface” evidence exists. Exact dispatch chooses by supplied `QuestionFamily`, not comparison.

### 4. Where does implementation currently terminate?

It terminates at read-only visibility/explanation:

- no recording;
- no event-ledger writes;
- no cluster mutation;
- no operational-story selection change;
- no target inference;
- no generic planner;
- explicit unknown for unsupported targets.

### 5. Is selection justification already a recurring implementation competency?

Yes, but boundedly. It is a recurring competency in the sense that implementation preserves selected result, reason/outcome, evidence support, lineage/candidates, alternatives, unknowns, and boundaries in `selection_path_audit`, and related recovery reports identify similar evidence-interpretation and responsibility-evaluation patterns.

It is not yet a general inquiry navigation responsibility family.

### 6. Does a recurring implementation responsibility family emerge?

Not for generic inquiry target selection. The evidence supports a competency named here as **Selection Justification Visibility**, but not a complete responsibility family. A family would require recurring ownership seams across candidate discovery, eligibility, comparison, selected target, rejected alternatives, dispatch handoff, and termination. Current code does not preserve that chain for inquiry targets.

### 7. If no family emerges, what competency does the implementation actually demonstrate?

It demonstrates bounded selection-justification visibility: explain an already-implemented selection using preserved candidates, ordering factors, selected outcome, non-selected alternatives, supporting evidence, unknowns, and read-only authority boundaries.

## Recommended next investigation

The next investigation should be:

```text
inquiry_target_candidate_preservation_boundary_investigation.md
```

Recommended central question:

```text
Does any current implementation preserve a per-inquiry candidate set of eligible QuestionFamily targets before exact bounded ask dispatch, or is candidate preservation limited to surface-specific audits such as selection_path?
```

This should remain an investigation only. It should not introduce planners, scoring engines, new abstractions, CLI changes, schemas, JSON changes, renderer changes, event changes, or behavior changes.
