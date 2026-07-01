# Question to Inquiry Transition Characterization

## Executive answer

Repository evidence supports a transition discipline, but it does **not** fully earn a new first-class constitutional object named `Potential Question`.

The strongest supported characterization is:

```text
observation / preserved note / operator concern
    may expose possible bounded questions
    but does not itself start a running inquiry
        ↓
exact operator-supplied QuestionFamily or preserved inquiry note
        ↓
implementation-backed eligibility / boundary checks
        ↓
map-backed bounded-work selection or surface-local orientation
        ↓
dispatch / answer-surface execution
        ↓
evidence collection and answer composition inside the selected surface
```

For the motivating `.` case, the repository shows that a preserved note can naturally allow multiple possible human questions, but Seed does not semantically enumerate, authorize, or spawn them. The implemented path records the raw note, then `Inquiry Orientation` performs only deterministic lexical overlap against existing projected read models. With no qualifying tokens or related state, it reports absence and stops. That is evidence that an observation does **not** immediately become a running inquiry into all possible interpretations.

Therefore Model B is more faithful than Model A **only if renamed and weakened**:

```text
Observation / preserved note
    ↓
possible questions visible to the operator or document author, not a runtime queue
    ↓
registered exact QuestionFamily or surface-local inquiry note
    ↓
implementation-backed eligibility and required-argument checks
    ↓
map-backed selection / dispatch request
    ↓
running answer surface
    ↓
surface-local evidence collection and answer composition
    ↓
answer
```

The repository does **not** support introducing new runtime objects, question queues, automatic inquiry spawning, a planner, or a scheduler. Existing architecture already explains most of the transition through registered question families, bounded-work eligibility, bounded-work selection, dispatch requests, and surface-local evidence collection.

## Repository evidence reviewed

Representative evidence reviewed:

- `constitution.md`, especially the rules that pressure or operator concern is only orientation evidence until repository evidence supports a bounded inquiry or implementation change, and that inquiry answers one bounded question while preserving observation, evidence, conclusion, authority, and stop condition.
- `bounded_question_discipline_investigation.md`, which finds local recurring bounded-question discipline but rejects a universal Question abstraction or uniform question pipeline.
- `runtime_question_recovery_characterization.md`, which characterizes mature recovery as terminating in runtime-owned question or answer surfaces, not in a general semantic question interpreter.
- `candidate_inquiry_reconciliation.md`, which rejected first-class candidate-inquiry ownership and moved the pressure toward bounded inquiry discipline.
- `inquiry_eligibility_characterization.md`, which identifies an evidence-strength check before selection but states that `InquiryEligibility` is not a separately implemented runtime subsystem.
- `operator_methodological_selection_characterization.md`, which finds pre-inquiry selection activity but not a single implementation-owned competency that selects the next bounded inquiry before `QuestionFamily -> Eligibility -> Dispatch`.
- `inquiry_subject_resolution_investigation.md`, which says public bounded inquiry starts from exact question-family identity and that subject acquisition remains distributed across question-family inventory, CLI dispatch, required surface args, and surface-local rules.
- `null_to_repository_orientation_experiment.md`, which records the `.` experiment and shows the note did not become facts, commands, repository structure, or selected observer work.
- `seed_runtime/question_surface_inventory.py`, which implements exact question-family maps, eligibility, selection, dispatch request, and dispatch execution.
- `scripts/seed_local.py`, which enforces `ask --question-family <exact-question-family>` and applies eligibility, argument validation, selection, and dispatch.
- `seed_runtime/inquiry_orientation.py`, which records inquiry notes outside the event ledger and builds read-only orientation views by collecting lexical-overlap evidence.
- `tests/test_question_surface_inventory.py` and `tests/test_inquiry_orientation.py`, which preserve the separation among eligibility, selection, dispatch, and read-only orientation behavior.

## Potential question characterization

The repository supports a weak, non-runtime sense of potential questions:

1. An observation, note, pressure item, or concern can make more than one bounded question imaginable.
2. Those possible questions are not automatically eligible, selected, dispatched, or evidence-bearing.
3. Current implementation does not represent them as a queue, planner state, object family, or semantic enumeration.
4. In implemented bounded ask, the first explicit question identity is an exact registered `QuestionFamily` string supplied by the operator.
5. In inquiry orientation, the first preserved input is a raw inquiry note, not a classified question. The implementation explicitly refuses to treat that note as a fact, claim, goal, requirement, authorization, command, or instruction.

The `.` example supports this weak characterization. A human can ask whether `.` is punctuation, a path, a repository, malformed input, shorthand, or the current working directory. But the repository evidence shows no implemented step that turns those alternatives into running inquiries. The null-state experiment records only one preserved note and an orientation question about deterministic related material, then stops when no supportable overlap exists.

This is enough to say:

```text
Potential question != running inquiry
```

It is not enough to say:

```text
Potential Question is a recovered constitutional owner
```

## Inquiry characterization

The repository supports a stronger characterization of inquiry than of potential question.

Constitutionally, inquiry is bounded work that answers one bounded question and preserves observation, evidence, classification or conclusion, authority, and stop condition. Operationally, several surfaces instantiate that discipline locally:

- `ask --question-family` requires an exact registered family.
- Unknown families are rejected rather than interpreted from prose.
- Diagnostic-only families are rejected as bounded ask answer surfaces.
- Parameterized families require explicit operator-provided surface arguments.
- Eligibility is separate from selection.
- Selection is separate from dispatch request construction.
- Dispatch execution mutates the CLI namespace to invoke an existing answering surface.
- Surface-local answer code then gathers evidence and composes or renders the answer.

Inquiry Orientation is a different but related form. It begins from a preserved inquiry note, not from an exact question family. Its implementation builds a bounded read-only orientation view and collects only deterministic lexical matches against projected facts and source-navigation matches. It does not route, execute tools, mutate state, call providers, append events, create facts, infer operator intent, or select a next observer.

## Transition analysis

### Does one observation constitutionally permit multiple possible questions?

Yes, in the weak sense that an observation or operator concern can be orientation evidence from which multiple bounded questions may be considered. The constitution says pressure, pressure reports, operator concerns, or residual pressure are orientation evidence until repository evidence supports a bounded inquiry or implementation change. It does not say one observation creates exactly one question.

The `.` experiment also demonstrates that the observation permits multiple possible external interpretations while the implementation authorizes none of them automatically.

### Are those questions already inquiries?

No. Existing implementation requires a further boundary before work runs:

- exact question-family identity must exist in the inventory;
- bounded-work eligibility must permit execution;
- required surface args must be provided where applicable;
- map-backed selection must choose an existing surface;
- dispatch must invoke that surface;
- or, for inquiry orientation, a preserved note must be explicitly recorded or selected and the orientation surface must be invoked.

Possible questions therefore are not already running inquiries.

### Must they first earn eligibility?

For `ask --question-family`, yes. The function `bounded_work_eligibility_for_question_family(...)` consumes an exact `question_family` and returns `eligible_now`, `eligible_with_parameters`, `diagnostic_only`, or `not_dispatchable`. Selection raises if eligibility is not permitted.

For inquiry orientation, the comparable gate is not named eligibility. It is a surface-local boundary: a non-empty inquiry note must be preserved, selected, and then rendered by a read-only orientation surface that limits itself to lexical evidence. That path does not prove a universal `Inquiry Eligibility` object.

### When does a question become an inquiry?

The repository supports two answers depending on surface:

1. For bounded ask, a question-family becomes a running inquiry only after exact family lookup, eligibility, required-argument validation, selection, dispatch request construction, and dispatch execution into an answering surface.
2. For inquiry orientation, the inquiry begins in the implemented sense when an inquiry note is preserved or selected and `build_inquiry_orientation(...)` is invoked to collect repository evidence for that note. Even then, the inquiry is read-only orientation, not semantic interpretation or routing.

Constitutionally, a question becomes inquiry when it is bounded work that can answer one bounded question while preserving evidence, conclusion, authority, and stop condition. Implementation evidence maps that point to dispatch or surface invocation, not to mere observation.

### What responsibility performs the transition?

There is no single universal responsibility.

For bounded ask, transition is distributed across:

- `Question Surface Inventory` for registered family identity;
- `bounded_work_eligibility_for_question_family(...)` for permission status;
- `scripts/seed_local.py::apply_bounded_ask_dispatch(...)` for CLI enforcement and required-argument validation;
- `bounded_work_selection_for_question_family(...)` for map-backed surface selection;
- `bounded_work_dispatch_request_for_selection(...)` and `execute_bounded_work_dispatch(...)` for invocation;
- the selected answer surface for evidence collection and answer composition.

For inquiry orientation, transition is performed by the inquiry-note/orientation surface:

- `record_inquiry_note(...)` preserves raw prose outside the event ledger;
- `select_inquiry_note(...)` chooses a preserved note;
- `build_inquiry_orientation(...)` invokes bounded read-only orientation;
- `_collect_architectural_orientation_evidence(...)` starts lexical evidence acquisition.

### Does Inquiry Eligibility consume questions or inquiries?

The implemented bounded-work eligibility function consumes an exact `QuestionFamily` string, not a running inquiry. Its dataclass records `question_family`, `bounded_status`, `permitted`, required args, and reason. It intentionally does not include dispatch surface fields. Selection consumes the eligibility result afterward.

The broader `inquiry_eligibility_characterization.md` speaks of candidate inquiry, boundary, family, vocabulary, or implementation direction, but it also says no separately implemented runtime subsystem named `InquiryEligibility` exists. Therefore the implementation-backed answer is: eligibility consumes registered question-family identity for bounded ask, and repository evidence / claim-strength proposals in document-level methodology. It does not consume already-running inquiries.

### Does Methodological Selection choose questions or eligible inquiries?

For bounded ask, map-backed selection chooses bounded work for an eligible exact `QuestionFamily`. It does not choose among free-form potential questions. The selection function requires a permitted eligibility result and returns a dispatch surface and surface value.

For broader Methodological Selection, repository evidence is weaker. The characterization finds pre-inquiry selection activity but not a single implemented competency that selects the next bounded inquiry before `QuestionFamily -> Eligibility -> Dispatch`. Thus, the repository supports selection among eligible or implemented candidates only within local surfaces. It does not support an architecture-wide chooser of potential questions.

### When does evidence acquisition begin?

Evidence acquisition begins inside the selected or invoked surface, not at the moment an observation makes questions imaginable.

In Inquiry Orientation, `_collect_architectural_orientation_evidence(...)` tokenizes the preserved note and collects related fact/source-navigation matches. For `.` there are no sufficiently meaningful matches, so the output reports no deterministic related material and no supportable lexical overlap.

For bounded ask, dispatch execution sets the relevant CLI surface flag/value. The selected surface then runs its own implementation-specific evidence gathering. The dispatch layer explicitly does not decide evidence semantics or answer composition.

### What implementation event marks the beginning of a running inquiry?

For bounded ask, the strongest implementation event is `execute_bounded_work_dispatch(...)` mutating the CLI namespace according to a `BoundedWorkDispatchRequest`, after eligibility and selection have already succeeded. This is the first generic event in the bounded-ask pipeline that performs invocation of selected bounded work.

For inquiry orientation, the strongest implementation event is `build_inquiry_orientation(...)` calling `_compose_architectural_orientation_answer(...)`, which calls `_collect_architectural_orientation_evidence(...)`. Recording the note preserves possible inquiry material, but evidence-bearing orientation begins when the orientation view is built.

## Comparative analysis

### Model A

```text
Observation
↓
Question
↓
Inquiry
```

Model A is too compressed for the implementation evidence. It hides:

- exact registered family lookup;
- unknown-family rejection;
- diagnostic-only rejection;
- required-argument validation;
- eligibility result shape;
- selection result shape;
- dispatch request shape;
- dispatch execution;
- surface-local evidence acquisition;
- orientation boundaries for raw notes.

It also risks implying that an observation creates a question and that a question naturally becomes an inquiry without authority or bounded initiation. Counterevidence from `.` rejects that implication.

### Model B

```text
Observation
↓
Potential Questions
↓
Inquiry Eligibility
↓
Eligible Inquiry
↓
Methodological Selection
↓
Running Inquiry
↓
Evidence-bearing Inquiry
↓
Answer
```

Model B better captures the separation between possible questions and running evidence-bearing work, but its names overstate repository evidence.

Supported after correction:

```text
Observation / preserved note / concern
↓
possible bounded questions, usually operator-visible rather than runtime-owned
↓
exact registered QuestionFamily or preserved inquiry note
↓
eligibility / boundary / required-argument checks where implemented
↓
map-backed selection or explicit surface invocation
↓
dispatch / answer-surface execution
↓
surface-local evidence collection
↓
answer composition / rendering
```

Unsupported as written:

- `Potential Questions` as a first-class runtime object;
- `Eligible Inquiry` as a separately implemented object;
- `Methodological Selection` as a universal chooser before all inquiries;
- `Running Inquiry` as a uniform runtime state across all surfaces;
- automatic promotion from observation to inquiry.

Therefore the repository more strongly supports a weakened Model B than Model A, but it does not recover every Model B boundary as stable architecture.

## Counterexamples and compression evidence

### Counterexample: bounded ask can feel immediate from exact operator input

When the operator supplies `ask --question-family "observation domain coverage"`, the CLI quickly reaches eligibility, selection, and dispatch. This can look like `Question -> Inquiry`. But the code still performs exact family validation, eligibility, selection, dispatch request construction, and dispatch execution. It is immediate only because the operator already supplied the registered family and any required parameters are absent.

### Counterexample: many lower-level responsibilities have implicit questions

`bounded_question_discipline_investigation.md` reports that Observation, Evidence, Fact promotion, and Fact support answer bounded questions inferred from implementation shapes and handoffs, not explicit `QuestionFamily` rows. This weakens claims that every inquiry must pass through named QuestionFamily eligibility.

### Counterexample: `ObservationIngestor` can create observation, evidence, and fact events in one batch

The same investigation notes that observation, evidence, and fact promotion often occur together, with promotion mostly implicit except suppression cases. This is a real compression: some implementation paths perform bounded work without a rich deliberative eligibility/selection stage. However, that compression concerns observation/fact processing, not semantic question interpretation from `.`.

### Counterexample: Inquiry Orientation begins from an `InquiryNoteRecord`, not a `QuestionFamily`

Inquiry Orientation does not consume a registered question family. It consumes a preserved note. This proves that registered question-family eligibility is not universal. But Inquiry Orientation still does not treat the note as a command, route, fact, or selected observer; it is explicitly read-only and bounded.

### Evidence against no distinction between question and inquiry

The strongest evidence against collapsing question and inquiry is the bounded-ask implementation:

- eligibility result lacks dispatch surface;
- selection requires permitted eligibility;
- selection result lacks `permitted` and `bounded_status`;
- dispatch request is separate from selection;
- dispatch execution is separate from evidence semantics and answer composition;
- CLI rejects unknown families and diagnostic-only families.

The `.` experiment is also strong evidence: many questions are imaginable, but none become repository traversal, facts, or selected observers without explicit bounded invocation.

## Supported conclusions

1. **Potential question differs from running inquiry.** Supported in the weak sense that observations may make possible questions imaginable while implementation requires bounded initiation before work runs.
2. **One observation can permit multiple possible questions.** Supported constitutionally and experimentally, but only as operator/document-visible possibility, not as runtime enumeration.
3. **A question becomes inquiry only after bounded initiation.** For bounded ask, this means exact family lookup, eligibility, required-argument validation, selection, dispatch request, and dispatch execution. For inquiry orientation, this means invoking the orientation surface over a preserved note.
4. **No single universal responsibility performs the transition.** Transition is distributed across inventory, CLI dispatch, eligibility, selection, dispatch, and selected surfaces, with inquiry orientation as a separate surface-local path.
5. **Inquiry Eligibility consumes exact question-family identity in the implemented bounded-ask path.** It does not consume already-running inquiries.
6. **Methodological Selection does not choose arbitrary potential questions.** Implemented selection chooses map-backed bounded work after eligibility or explains implemented candidate selection within local surfaces.
7. **Evidence acquisition begins in selected/invoked surfaces.** For inquiry orientation this is `_collect_architectural_orientation_evidence(...)`; for bounded ask it occurs after dispatch inside the target surface.
8. **Existing architecture already explains the transition without a new runtime boundary.** The repository has enough evidence for a characterization, not for new objects.

## Unsupported conclusions

- `Potential Question` is a recovered first-class constitutional owner.
- Seed currently enumerates all possible questions from an observation.
- Seed has a question queue, planner, scheduler, or automatic inquiry spawner.
- Every observation immediately begins an inquiry.
- Every inquiry passes through `QuestionFamily` eligibility.
- `InquiryEligibility` is a separately implemented runtime subsystem.
- `MethodologicalSelection` is a universal next-inquiry chooser.
- A raw inquiry note is semantic intent, repository path, command, tool need, authorization, or runtime instruction.
- `.` alone authorizes repository traversal, filesystem interpretation, malformed-input diagnosis, shorthand interpretation, or current-working-directory interpretation.

## Direct answers to requested questions

### 1. Does the repository distinguish `Potential Question != Inquiry`?

Yes, but weakly. It distinguishes possible/operator-visible questions from bounded running work. It does not implement `Potential Question` as a first-class runtime or constitutional object.

### 2. Does one observation constitutionally permit multiple questions?

Yes. Repository discipline treats observations, pressure, and concerns as orientation evidence from which bounded inquiries may later be supported. The `.` example permits many possible human questions, but none are automatically authorized.

### 3. When does a question become an inquiry?

When it becomes bounded work under an implemented surface. For bounded ask, that is after exact question-family validation, eligibility, required-argument validation, selection, dispatch request construction, and dispatch execution. For inquiry orientation, that is when a preserved note is used to build a read-only orientation view.

### 4. What responsibility performs that transition?

No universal responsibility. Bounded ask distributes it across question-surface inventory, CLI dispatch, eligibility, selection, dispatch request, dispatch execution, and the selected surface. Inquiry Orientation performs its own note-to-orientation transition locally.

### 5. Does Inquiry Eligibility consume questions or inquiries?

In implemented bounded ask, it consumes exact question-family strings. It does not consume already-running inquiries. Broader document-level eligibility consumes candidate claims or candidate inquiry framings, but that is not a separate runtime subsystem.

### 6. Does Methodological Selection choose questions or eligible inquiries?

Implemented bounded-work selection chooses a dispatch surface for an eligible exact question family. Broader selection-path surfaces explain implemented candidate selection, not arbitrary potential-question choice. So the supported answer is: eligible/implemented candidates, not raw potential questions.

### 7. What implementation evidence marks the beginning of a running inquiry?

For bounded ask, `execute_bounded_work_dispatch(...)` consuming a `BoundedWorkDispatchRequest` after eligibility and selection is the strongest generic marker. For inquiry orientation, `build_inquiry_orientation(...)` leading to `_collect_architectural_orientation_evidence(...)` is the evidence-bearing start.

### 8. Is there sufficient repository evidence to recognize these as stable architectural distinctions?

There is sufficient evidence to recognize a stable **discipline**:

```text
possible question / concern / note != eligible bounded work != selected dispatch != evidence-bearing answer surface
```

There is insufficient repository evidence to recognize all proposed names as stable architectural objects, especially `Potential Question`, `Eligible Inquiry`, and `Running Inquiry` as first-class uniform boundaries.

## Confidence

- **High confidence** that an observation or note does not automatically become semantic inquiry or selected observer work.
- **High confidence** that bounded ask separates exact question-family identity, eligibility, selection, dispatch request, and dispatch execution.
- **High confidence** that Inquiry Orientation is read-only, lexical, and bounded around preserved notes.
- **Medium confidence** that the repository constitutionally permits multiple possible questions from one observation, because this is inferred from orientation-evidence and bounded-inquiry discipline rather than implemented enumeration.
- **Low confidence** in the specific names `Potential Question`, `Eligible Inquiry`, and `Running Inquiry` as recovered stable architecture. Existing architecture explains the transition without introducing those as new boundaries.
