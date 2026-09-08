# Operator Methodological Selection Characterization

## Executive answer

A recurring **pre-inquiry selection activity** exists, but the repository evidence does **not** show a single implementation-owned competency that selects the next bounded inquiry before `QuestionFamily -> Eligibility -> Dispatch`.

The recurring work currently performed by the operator is best characterized as:

```text
review unresolved architectural pressure and prior inquiry evidence
↓
identify which evidence-bearing artifact is most relevant now
↓
bound the next question narrowly enough to avoid planner/goal/motivation claims
↓
choose a QuestionFamily or investigation subject manually
↓
invoke implementation that only begins after that choice is supplied
```

The repository already preserves portions of this work as **visibility and traceability artifacts**: pressure audits, frontier/handoff documents, reference-selection and selection-path audits, question-family registration, diagnostic inventory and shape-audit contracts, completion audits, and readiness investigations. Those artifacts expose candidate sets, constraints, implementation boundaries, alternatives, unknowns, and stopping criteria.

However, the operator still performs the decisive pre-inquiry methodological work: deciding which unresolved pressure should become the next bounded investigation, choosing the bounded subject, deciding whether the evidence is sufficient to start an inquiry, and mapping that subject into an exact bounded ask or report task. Existing implementation either explains an already-supplied target, selects among candidates inside a bounded domain, or dispatches an exact `QuestionFamily` supplied by the caller.

Therefore, the answer to whether implementation evidence justifies recovering a new ownership family is:

```text
Insufficient implementation evidence.
```

The evidence supports **multiple adjacent implementation-visible competencies** around selection traceability, bounded ask dispatch, reference selection, pressure visibility, readiness evaluation, and completion stopping. It does not support recovering exactly one new family that owns pre-inquiry next-investigation selection.

## Implementation evidence reviewed

This audit reviewed representative recent architectural characterization and implementation surfaces, prioritizing code and tests over prose where both existed.

### Recent characterization and audit artifacts

- `architectural_maturity_localization_characterization.md` characterizes the recent trajectory as known-family localization, compatibility-preserving slices, completion/reassignment, and bounded frontier audits rather than autonomous architectural discovery.
- `architectural_competency_transition_characterization.md` distinguishes implementation-visible competencies from methodological ones and describes selection justification as bounded visibility, not general inquiry-target selection.
- `pressure_audit_responsibility_characterization.md`, `pressure_audit_smallest_owner_investigation.md`, and pressure visibility investigations characterize pressure as visibility or evidence classification, not direct next-work authority.
- Family completion reports, including answer composition, read-model ownership, projection influence lineage, projection diagnostics, reasoning path, and selection path completion audits, act as stopping/reassignment evidence.
- `architectural_frontier_hit_list.md`, `docs/active_edge_frontier.md`, and `docs/current_work_position_frontier.md` preserve unresolved frontiers and current attention labels, but do not implement autonomous selection.
- `responsibility_recovery_evaluation_readiness_investigation.md` and `slice_evaluation_readiness_investigation.md` provide readiness criteria for bounded evaluation.
- `question_family_registration_boundary_audit.md`, `bounded_question_discipline_investigation.md`, and bounded inquiry slice reports describe bounded ask registration and dispatch boundaries.
- `inquiry_navigation_selection_justification_recovery_investigation.md` and `docs/reference_selection_traceability_investigation.md` describe selection traceability pressures around existing surfaces.

### Implementation surfaces reviewed

- `seed_runtime/question_surface_inventory.py` preserves exact bounded ask families, dispatch surfaces, required surface arguments, eligibility, selection, and dispatch request construction. Its dispatch map includes exact family-to-surface mappings and explicitly requires `target` for `selection explanation`.
- `seed_runtime/selection_path_audit.py` preserves selection-path visibility for a supplied target, including selected result, candidates, factors, non-selected candidates, evidence, outcome, unknowns, and read-only boundary.
- `seed_runtime/reference_selection.py` preserves implementation-selected comparison references for the bounded `history` domain and returns explicit unsupported-domain output elsewhere.
- Diagnostic inventory and shape-audit code register operational surfaces and prove that read-only visibility surfaces remain visible without recording or mutation.
- Tests around reference selection, inquiry artifacts, investigation path audits, bounded ask dispatch, and diagnostic inventory/shape audit preserve these surface boundaries.

## Current operator selection workflow

The repository evidence supports the following current workflow before executable inquiry starts.

### 1. Inspect unresolved pressure and recent stopping points

The operator reviews pressure-bearing artifacts such as frontier hit lists, active-edge/current-work-position reports, pressure audits, completion audits, and readiness investigations. These artifacts identify unresolved concerns, adjacent-family handoffs, unsupported conclusions, and places where prior work stopped.

This inspection is recurring and repository-supported, but the **choice of which pressure to act on next** is not implementation-selected. Pressure artifacts inform selection; they do not own it.

### 2. Compare candidate artifacts and authority boundaries

The operator compares which artifacts are relevant to the next question: recent characterization reports, completion audits, implementation files, tests, diagnostic registries, and counterexample surfaces. Existing reference-selection implementation shows that the repository can preserve selected reference, rationale, alternatives, limitations, and authority boundary inside a bounded domain. It does not generalize to choosing the next investigation.

### 3. Decide whether the next work is implementation-backed or methodological

The operator applies recurring criteria:

- Is there a concrete implementation seam?
- Is there an existing surface, payload, registry, CLI, or test?
- Are candidates and rejected alternatives visible?
- Does the work preserve compatibility?
- Does the work stop before unsupported planner/goal/motivation claims?
- Is remaining pressure same-family, adjacent-family, or unsupported?

Readiness and completion artifacts support this analysis. The final judgment remains methodological unless implementation evidence already owns the decision.

### 4. Bound the next inquiry

The operator turns broad pressure into a bounded question or report task. For executable bounded ask, implementation starts only after an exact `QuestionFamily` and any required arguments have been supplied. For characterization work, the operator supplies the subject and scope directly.

### 5. Invoke an implementation surface or create a characterization artifact

Once a bounded family, target, domain, or report scope is selected, implementation can run existing code paths: question-family eligibility/dispatch, selection-path explanation for a supplied target, reference selection for a supplied domain, diagnostic inventory, diagnostic shape audit, knowledge reachability, pressure audit, and related read-only surfaces.

## Recurring artifacts informing selection

The recurring artifacts participating in operator selection are:

| Artifact type | What it contributes | Implementation-selected next inquiry? |
| --- | --- | --- |
| Pressure audits and pressure visibility reports | Candidate pressures, scores, evidence, visibility boundaries, unsupported interpretations. | No. Pressure can order pressure candidates inside implemented surfaces, but not select the next investigation globally. |
| Frontier and current-position documents | Current attention, active edge, future frontier, unresolved work labels. | No. These are preservation and presentation artifacts unless implementation evidence says otherwise. |
| Completion audits | Stop criteria, same-family completion, adjacent-family reassignment, unsupported next claims. | No. They constrain future work but do not choose it. |
| Readiness investigations | Evidence criteria for whether recovery/evaluation/slice work is ready. | No. They support judgment; they are not a selector. |
| Question-family registration | Exact bounded ask inventory, eligibility status, dispatch destination, required args. | Only after `QuestionFamily` is supplied. It does not pick the family from unresolved pressure. |
| Selection-path audit | Candidate set, selection factors, non-selected alternatives, support, boundary for a supplied target. | Only inside implemented target handling. It does not choose the next inquiry target. |
| Reference-selection audit | Selected comparison reference, alternatives, rationale, authority boundary for a supplied domain. | Only inside bounded reference-selection domains. It does not select the next investigation. |
| Diagnostic inventory and shape audit | Operational visibility obligations for new/changed diagnostics. | No. They enforce visibility, not next-work selection. |
| Implementation files and tests | Strongest authority for what exists, what is dispatched, and what is read-only. | They constrain selection and counterexamples; they do not currently replace operator choice. |

## Implementation-visible responsibilities

The following responsibilities are implementation-visible today.

### Exact question-family inventory and bounded dispatch

`BOUNDED_ASK_DISPATCH_SURFACES` maps exact bounded question-family strings to existing surfaces, including `selection explanation -> selection_path`. `BOUNDED_ASK_REQUIRED_SURFACE_ARGS` separately states that `selection explanation` requires a `target` argument. This proves dispatch begins after the family and target are provided, not before.

`bounded_work_eligibility_for_question_family(...)` derives whether an exact family is currently executable, parameterized, diagnostic-only, or unmapped. `bounded_work_selection_for_question_family(...)` selects the dispatch surface from the exact map only after permitted eligibility is supplied. Its docstring explicitly limits responsibility to map-backed selection and excludes eligibility, dispatch execution, answer composition, rendering, and evidence semantics.

### Selection justification visibility for supplied targets

`SelectionPathAudit` preserves the selected item, candidate set, selection factors, non-selected alternatives, evidence, outcome, unknowns, and boundary. Its default boundary is `read_only_selection_audit`, with no fact recording, event-ledger writes, or cluster mutation.

`build_selection_path_audit(...)` accepts a `target`. It can explain implemented targets such as `current_focus`, `primary_pressure`, operational-story focus, or a pressure category match. Unknown targets produce `selected="unknown"`, `selection_factors=["unknown"]`, and an explicit unknown stating that no implementation-backed selection evidence was discovered.

For pressure/current-focus targets, `_from_pressure_selection(...)` exposes the implemented selection factor: pressure candidates are ordered by descending score, then category name.

### Reference selection for bounded domains

`ReferenceSelection` preserves domain, question, selected reference, selection rationale, alternative references, authority boundary, limitations, and no event/cluster mutation flags. `build_reference_selection(...)` supports `history`; unsupported domains return explicit unsupported-domain output. This is a bounded implementation-selected reference, not general next-inquiry selection.

### Operational visibility contracts

Diagnostic inventory and shape-audit registrations make operational surfaces visible and testable. This affects any new diagnostic, audit, probe, view, CLI flag, or recordable output, but it is a visibility contract rather than a selector for what inquiry should happen next.

### Read-only authority boundaries

Multiple surfaces preserve read-only boundaries: selection path, reference selection, question-family inventory, inquiry orientation, and readiness/evaluation-style diagnostics. They prove repository discipline around not converting diagnostic or methodological findings into cluster truth.

## Methodological responsibilities

The following responsibilities remain outside implementation ownership.

1. **Choosing the next unresolved architectural pressure to inspect.** Pressure and frontier artifacts inform this choice, but no implementation selects one as the next investigation.
2. **Converting broad pressure into a bounded investigation prompt.** The operator currently performs the narrowing from recurring concern to exact question scope.
3. **Choosing which repository artifacts are representative for a new characterization.** Existing reference-selection implementation is bounded to comparison references, not investigation corpus selection.
4. **Deciding whether a recurring habit is enough to justify a new owner.** Readiness artifacts provide criteria, but the final promotion decision is not automated.
5. **Mapping presentation vocabulary into or away from implementation-backed knowledge.** Repository instructions explicitly warn that terms such as continuation, current work position, active edge, and similar labels require implementation evidence before promotion.
6. **Determining when counterexamples are strong enough to stop recovery.** Completion audits model this discipline, but there is no general counterexample evaluator that selects next work.
7. **Selecting among multiple adjacent competencies.** Selection traceability, reference selection, pressure visibility, readiness evaluation, completion stopping, and bounded dispatch are related but independent implementation-visible competencies.

## Counterexamples reviewed

### Counterexample: next inquiry already selected entirely by implementation

Not supported. Exact bounded ask dispatch selects a surface only after the caller provides an exact `QuestionFamily` and any required surface args. The implementation does not generate competing inquiry candidates, rank them, select one next investigation, and preserve rejected alternatives before `QuestionFamily`.

### Counterexample: pressure directly selects the next investigation

Not supported. Selection-path implementation can order pressure candidates for supplied pressure/current-focus targets. That proves pressure ordering inside a bounded audit. It does not prove that pressure directly chooses the next architectural investigation or that all next-work selection is pressure-owned.

### Counterexample: `QuestionFamily` already owns methodological selection

Not supported. `QuestionFamily` registration owns exact-family inventory, eligibility, required args, and dispatch mapping. It does not own semantic interpretation of operator language, next-work pressure ranking, selection among investigations, or methodology for deciding which family should be asked next.

### Counterexample: no recurring operator behavior exists

Not supported. The repeated shape of recent reports shows recurring operator behavior: inspect pressure/frontiers/completion/readiness evidence, narrow scope, search counterexamples, preserve implementation boundaries, and decide whether evidence supports recovery or only characterization. The recurrence is methodological, not a single implemented owner.

### Counterexample: reference selection is general next-inquiry selection

Not supported. `reference_selection` demonstrates implementation-selected comparison references in bounded domains, especially `history`. Unsupported domains remain explicit. It does not select next investigations.

### Counterexample: selection path is general next-inquiry selection

Not supported. `selection_path` explains selection for a supplied target. Unknown targets return explicit unknowns instead of inferring a next inquiry. This is positive evidence against a hidden planner or general selector.

## Supported conclusions

### 1. Does a recurring pre-inquiry selection competency already exist?

Yes as a recurring **operator competency** and repository-supported methodology. No as a single implementation-owned next-inquiry selector.

The recurring competency is:

```text
methodological selection of the next bounded inquiry from unresolved evidence
```

It is performed by the operator using repository artifacts. Implementation preserves several sub-pieces, but not the complete selection responsibility.

### 2. What implementation evidence supports that conclusion?

Implementation supports the conclusion by showing where selection exists and where it stops:

- exact `QuestionFamily` dispatch maps exist only after the family is supplied;
- `selection explanation` requires an explicit `target`;
- selection-path audits explain implemented targets and return unknowns for unsupported targets;
- pressure ordering is preserved inside selection-path output, not as global next-work authority;
- reference selection supports bounded domains and returns unsupported-domain output elsewhere;
- read-only boundaries repeatedly prevent diagnostic findings from becoming operational truth.

### 3. What artifacts currently inform selection?

Selection is informed by pressure audits, pressure visibility investigations, frontier/current-position documents, completion audits, family completion reports, readiness investigations, question-family registration, bounded inquiry investigations, diagnostic inventory/shape-audit contracts, implementation files, and tests.

### 4. Which responsibilities are implementation-visible?

Implementation-visible responsibilities include exact bounded ask inventory, eligibility, dispatch surface lookup, selection-path visibility for supplied targets, reference-selection visibility for supplied domains, pressure candidate ordering inside implemented audits, diagnostic visibility registration, shape-audit validation, and read-only authority boundaries.

### 5. Which responsibilities remain purely methodological?

Purely methodological responsibilities include choosing the next pressure, deciding the next bounded investigation subject, selecting representative evidence for a new characterization, deciding whether recurring behavior is sufficient for ownership recovery, promoting or rejecting presentation vocabulary, and deciding whether counterexamples stop recovery.

### 6. Is there sufficient implementation evidence to justify a new ownership family?

```text
Insufficient implementation evidence.
```

The repository demonstrates multiple related implementation-visible competencies, but not one bounded implementation responsibility that selects the next inquiry before `QuestionFamily -> Eligibility -> Dispatch`.

## Unsupported conclusions

The following conclusions are not supported by repository evidence:

- Seed has a planner, goal system, motivation engine, autonomous work selector, LLM reasoning engine, or runtime redesign for choosing next work.
- Pressure directly chooses the next investigation.
- `QuestionFamily` owns semantic/methodological inquiry selection.
- `selection_path` selects next inquiries generally.
- `reference_selection` selects next inquiries generally.
- Frontier/current-position labels are implementation-backed knowledge of future work without additional evidence.
- A new ownership family should be recovered now.

## Confidence

Confidence is **moderate-high**.

Reasons for confidence:

- The strongest implementation surfaces have explicit boundaries that stop before next-inquiry selection.
- Unknown/unsupported paths are represented explicitly rather than inferred.
- Recent characterization reports consistently distinguish implementation-backed local competencies from broader methodology.
- Multiple counterexamples were found against general selection ownership.

Reasons confidence is not absolute:

- The repository has many prose investigations and evolving diagnostic surfaces; unreviewed newer slices may refine selection-adjacent behavior.
- Some frontier/current-position artifacts may preserve more continuity context than this audit needed to characterize.
- The audit was bounded to representative recent work, not an exhaustive proof over every file.

## Recommendation regarding implementation readiness

Do **not** recover ownership now.

The evidence supports preserving this as a characterization result and, if future work continues, looking for a smaller implementation-backed responsibility such as one of the following only if code/tests already demonstrate recurrence:

- candidate inquiry artifact inventory;
- evidence sufficiency gate for starting a bounded audit;
- traceable handoff from completion audit to adjacent-family candidate;
- corpus/reference selection for a bounded characterization.

At present, those are possible future investigation subjects, not recommendations to implement a planner or recover a new family.

The current readiness answer is:

```text
Insufficient implementation evidence.
```
