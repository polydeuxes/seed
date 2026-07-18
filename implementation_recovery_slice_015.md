# Implementation Recovery Slice 015

## Bounded campaign goal

Continue recovering the implementation realization of Seed's internal constitutional process while preserving the governing interaction distinction:

```text
the operator supplies testimony, goals, constraints, and corrections
Seed establishes bounded meaning
Seed composes applicable views internally
Seed originates and asks bounded questions internally
```

This slice recovers exactly one implementation-local boundary and does not promote operator-facing Question Family, presentation, view, or dispatch access into the canonical Seed road.

## Relevant Book neighborhood

Smallest relevant Book neighborhood:

- `book_of_seed/04-inquiry-and-examination/questions-and-inquiry.md`: question-shaped text, operator ask text, public answer families, eligibility, selection, dispatch, answer, and completion remain separate standings.
- `book_of_seed/01-grammar-and-standing/lenses-views-and-roads.md`: a lens or representation may expose or compose a bounded representation without becoming a constitutional road, answer, or evidence sufficiency.
- `book_of_seed/01-grammar-and-standing/external-and-constitutional-grammar.md`: implementation and CLI grammars remain external grammar unless a bounded distinction is separately warranted.

The Book orients only the constitutional distinction. Implementation evidence determines the mechanics, owner, artifact, consumer, compatibility behavior, and runtime behavior.

## Constitutional distinction

The selected distinction is:

```text
operator-requested presentation compatibility handoff
!= constitutional question origination
!= inquiry standing
!= Seed-composed canonical view
!= dispatch execution
!= answer standing
```

A bounded ask `--presentation` path may apply an already prepared presentation handoff to the CLI namespace and clear the compatibility `ask` message. That local act does not establish that the operator selected a canonical internal Seed view, that the question family is applicable as inquiry, that the presentation is an answer, or that the containing road is canonical.

## Frontier-applicability evidence

The bounded campaign goal requires preserving the operator/Seed interaction distinction, especially where operator-facing Question Family and presentation access might be mistaken for internal question origination or internal view composition.

Implementation evidence exposes an eligible seam in `scripts.seed_local.apply_bounded_ask_dispatch(...)`:

- exact QuestionFamily admission and bounded eligibility are already separate implementation owners;
- `bounded_work_presentation_handoff_for_eligibility(...)` prepares a presentation handoff only after permitted eligibility;
- `apply_bounded_work_presentation_handoff(...)` applies the handoff to the CLI namespace;
- `clear_bounded_ask_presentation_message(...)` clears the compatibility ask message;
- the same apply-and-clear sequence was duplicated in both the `eligible_with_parameters` presentation branch and the `eligible_now` presentation branch.

This neighborhood is connected to the campaign goal because it is an operator-facing presentation path for exact QuestionFamily bounded ask, and the Book distinguishes question surfaces from inquiry standing and representation/lens output from constitutional roads or answers.

## Rejected mechanically adjacent candidates

No additional CLI, inquiry system, Question Family system, view system, diagnostic surface, or dispatch system was selected merely because it is adjacent in the call chain.

The immediately adjacent dispatch handoff was already recovered in Slice 014. The next eligible seam was not chosen because it was numerically next; it was chosen because the Book-relevant presentation boundary has concrete implementation evidence and a repeated local responsibility.

## Selected implementation neighborhood

Selected neighborhood:

```text
scripts.seed_local.apply_bounded_ask_dispatch(...)
↓
bounded_work_presentation_handoff_for_eligibility(...)
↓
apply_bounded_ask_presentation_handoff(...)
↓
apply_bounded_work_presentation_handoff(...)
↓
clear_bounded_ask_presentation_message(...)
```

## Containing-road classification

```text
compatibility-only
```

Bounded reason: the selected local seam lives in the public `ask --question-family ... --presentation` CLI compatibility path. This classification is limited to the implicated containing path and does not establish that the wider inquiry road, view road, Question Family road, or CLI road is canonical internal Seed road.

## Selected realization seam

Concrete seam under Fidelity review:

```text
apply_bounded_ask_presentation_handoff(args, presentation_handoff)
```

The seam consumes an already prepared `BoundedWorkPresentationHandoff`, applies the existing presentation handoff to the CLI namespace, clears the bounded ask compatibility message, and returns the existing message-clear artifact.

## Applicable Fidelity invariants

The selected seam carries or endangers these local invariants:

- It may consume only an already prepared presentation handoff.
- It may apply the existing presentation handoff to the CLI namespace.
- It may clear the compatibility `ask` message after the presentation handoff.
- It must not decide exact QuestionFamily lookup.
- It must not decide bounded eligibility or inquiry standing.
- It must not validate or select dispatch surfaces or surface values.
- It must not execute dispatch.
- It must not compose a constitutional view or answer.
- It must not establish evidence sufficiency, knowledge, fact, completion, or containing-road canonicity.
- It must preserve runtime and CLI compatibility behavior.

## Bounded Fidelity classification

```text
faithful within scope
```

The recovered seam is faithful within the selected local scope because it makes the recurring post-presentation compatibility handoff directly observable without changing behavior or claiming constitutional authority. It preserves the Book-oriented distinctions between question surface, inquiry standing, presentation/lens output, answer standing, dispatch, and canonical constitutional road.

## Implementation evidence

Implementation evidence supporting the seam:

- `BoundedWorkPresentationHandoff` carries only `question_family`, `question_family_explanation`, and `reason`.
- `bounded_work_presentation_handoff_for_eligibility(...)` requires permitted eligibility before preparing presentation handoff input.
- `apply_bounded_work_presentation_handoff(...)` only sets `args.question_family_explanation` and returns the presentation application result.
- `clear_bounded_ask_presentation_message(...)` only clears `args.message` and returns a message-clear artifact.
- `scripts.seed_local.apply_bounded_ask_dispatch(...)` duplicated the same apply-and-clear sequence in both presentation branches before this slice.
- The new regression test proves the recovered helper consumes a prepared handoff, applies presentation namespace state, clears the message, and does not return presentation explanation, dispatch surface, or surface value fields.

## Before

`apply_bounded_ask_dispatch(...)` owned all of the following in each presentation branch:

```text
prepare presentation handoff
apply presentation handoff to CLI namespace
clear bounded ask message
return from compatibility path
```

The post-presentation compatibility handoff was compressed into the larger bounded ask CLI compatibility path and duplicated across parameterized and non-parameterized eligible branches.

## After

`apply_bounded_ask_presentation_handoff(...)` owns only:

```text
consume an already prepared BoundedWorkPresentationHandoff
apply existing presentation handoff to the CLI namespace
clear existing bounded ask presentation message
return existing message-clear result
```

`apply_bounded_ask_dispatch(...)` still owns the surrounding bounded ask CLI compatibility flow and delegates the local post-presentation handoff in both presentation branches.

## Recovered or corrected owner

Recovered owner:

```text
apply_bounded_ask_presentation_handoff(...)
```

No unfaithful boundary crossing required runtime correction.

## Recovered artifact/helper

Recovered helper:

```text
apply_bounded_ask_presentation_handoff(args, presentation_handoff)
```

Input artifact:

```text
BoundedWorkPresentationHandoff
```

Returned artifact:

```text
BoundedAskPresentationMessageClearResult
```

No new framework, engine, registry, universal question owner, universal view composer, inquiry architecture, schema, diagnostic surface, recordable output, event-ledger behavior, or cluster mutation was introduced.

## Recovered consumer

Consumer:

```text
scripts.seed_local.apply_bounded_ask_dispatch(...)
```

It consumes the recovered helper in the `eligible_with_parameters` presentation branch and the `eligible_now` presentation branch.

## Negative authority

The recovered owner and artifact do not possess authority to:

- originate or admit inquiry;
- decide exact QuestionFamily lookup;
- determine bounded eligibility;
- validate required operator surface args;
- select dispatch surface or selected surface value;
- construct dispatch requests;
- execute dispatch;
- apply dispatch-result compatibility;
- compose a canonical internal Seed view;
- establish answer standing, evidence sufficiency, knowledge, fact, completion, or retirement;
- write the event ledger;
- mutate cluster state;
- make the public CLI path canonical constitutional grammar;
- classify the containing road as internal Seed road.

## Compatibility treatment

Implicated compatibility:

```text
constitutionally neutral
```

The public `ask --question-family ... --presentation` compatibility behavior is preserved. Compatibility remains implementation evidence and does not become constitutional authority.

## Runtime behavior treatment

Runtime behavior did not change. The same underlying actions occur for presentation paths:

```text
apply_bounded_work_presentation_handoff(...)
clear_bounded_ask_presentation_message(...)
```

The code now gives that local sequence an implementation owner.

## Files changed

- `seed_runtime/question_surface_inventory.py`
- `scripts/seed_local.py`
- `tests/test_question_surface_inventory.py`
- `implementation_recovery_slice_015.md`

## LOC changed

Before this report file was added, git diff reported:

```text
scripts/seed_local.py                      | 13 +++----------
seed_runtime/question_surface_inventory.py | 21 +++++++++++++++++++++
tests/test_question_surface_inventory.py   | 27 +++++++++++++++++++++++++++
3 files changed, 51 insertions(+), 10 deletions(-)
```

Including this report, the operation adds one narrow helper, one direct regression test, rewires the existing caller to use the helper, and adds this implementation-slice report.

## Tests executed

```text
pytest -q tests/test_question_surface_inventory.py
```

Result:

```text
65 passed in 36.26s
```

## Remaining compressed responsibilities

Untouched adjacent responsibilities include:

- exact QuestionFamily lookup;
- bounded eligibility classification;
- operator surface argument validation;
- selected dispatch surface preparation;
- selected surface value preparation;
- dispatch request construction;
- dispatch namespace mutation;
- dispatch result production;
- knowledge-reachability JSON dispatch compatibility;
- non-presentation dispatch handoff;
- general question-family explanation composition and rendering;
- diagnostic inventory and shape-audit surfaces;
- event-ledger and cluster-state behavior.

## Preserved Unknowns

Preserved Unknowns:

- whether the larger bounded ask path is a transitional, historical, mixed, or differently classified road beyond this compatibility-only local finding;
- whether any operator-facing Question Family presentation path corresponds to an internal constitutional road in contexts outside this seam;
- whether the question-family explanation output has answer standing in any separate consumer boundary;
- whether presentation vocabulary should receive constitutional standing outside implementation-attributed compatibility.

## Unresolved containing-road standing

The containing road remains unresolved beyond the bounded classification:

```text
public bounded ask presentation compatibility path = compatibility-only within this slice
larger inquiry/view/Question Family road = Unknown
```

## Required questions

1. **What is the bounded campaign goal?**

   Continue recovering the implementation realization of Seed's internal constitutional process while preserving the distinction that the operator supplies testimony, goals, constraints, and corrections, while Seed establishes bounded meaning, composes applicable views internally, and originates bounded questions internally.

2. **What is the smallest relevant Book neighborhood?**

   Questions and Inquiry plus Lenses, Views, and Constitutional Roads, with External and Constitutional Grammar as the boundary preventing implementation/CLI vocabulary from becoming constitutional authority.

3. **What constitutional distinction currently requires implementation realization?**

   Operator-requested presentation compatibility handoff is not inquiry origination, inquiry standing, Seed-composed canonical view, dispatch execution, answer standing, or constitutional road standing.

4. **Which implementation neighborhood is eligible for that distinction?**

   The bounded ask presentation branches in `scripts.seed_local.apply_bounded_ask_dispatch(...)`, supported by `BoundedWorkPresentationHandoff`, `apply_bounded_work_presentation_handoff(...)`, and `clear_bounded_ask_presentation_message(...)`.

5. **What evidence connects that neighborhood to the campaign goal?**

   It is an operator-facing exact QuestionFamily `--presentation` path, and implementation evidence shows it applies a presentation handoff and clears the compatibility ask message after eligibility, while Book evidence distinguishes question surfaces and presentation/lens outputs from inquiry standing, answers, and constitutional roads.

6. **Is the selected neighborhood eligible because of constitutional applicability, or only mechanically adjacent to Slice 014?**

   It is eligible because of constitutional applicability. Slice 014 adjacency established locality only; the selected seam was recovered because the operator-facing presentation boundary directly carries the Book-relevant distinction and a repeated implementation-local responsibility.

7. **What is the containing-road classification?**

   Compatibility-only for the public bounded ask presentation path within this slice.

8. **What concrete realization seam is under Fidelity review?**

   `apply_bounded_ask_presentation_handoff(args, presentation_handoff)`.

9. **What applicable invariants does that seam carry or endanger?**

   It may consume a prepared presentation handoff, apply it to the CLI namespace, and clear the ask message; it may not decide lookup, eligibility, argument validation, dispatch selection, dispatch execution, answer composition, evidence sufficiency, knowledge, fact, or road canonicity.

10. **What bounded Fidelity classification is supported?**

    Faithful within scope.

11. **What responsibilities were previously compressed?**

    Applying the presentation handoff and clearing the bounded ask message were compressed into each presentation branch of the larger CLI compatibility function.

12. **Which single implementation-local ownership boundary became directly observable?**

    The post-presentation bounded ask compatibility handoff became directly observable.

13. **Is the recovered responsibility ownership, orchestration, cleanup, translation, selection, preservation, consumption, or another implementation-local act?**

    It is local handoff consumption plus compatibility cleanup. It is not translation, selection, preservation, or constitutional orchestration.

14. **What owner carries it?**

    `apply_bounded_ask_presentation_handoff(...)`.

15. **What artifact or helper carries the boundary, if any?**

    The helper `apply_bounded_ask_presentation_handoff(...)` carries the boundary; it consumes `BoundedWorkPresentationHandoff` and returns `BoundedAskPresentationMessageClearResult`.

16. **Who consumes it?**

    `scripts.seed_local.apply_bounded_ask_dispatch(...)` consumes it in both bounded ask presentation branches.

17. **What authority does the recovered owner or artifact not possess?**

    It does not possess authority over inquiry origination, inquiry standing, QuestionFamily applicability, dispatch selection or execution, answer standing, evidence sufficiency, knowledge establishment, event recording, cluster mutation, or containing-road canonicity.

18. **What compatibility boundary is implicated?**

    The public `ask --question-family ... --presentation` CLI compatibility boundary.

19. **Did compatibility or runtime behavior change?**

    No. The same namespace update and message clear occur in the same presentation paths.

20. **What containing-road standing remains unresolved?**

    The larger inquiry, view, Question Family, and bounded ask roads remain Unknown beyond this local compatibility-only classification.

21. **What adjacent responsibilities remain untouched?**

    Lookup, eligibility, surface argument validation, dispatch surface/value selection, dispatch request construction, dispatch execution, dispatch result handling, JSON dispatch compatibility, rendering, diagnostics, recording, and cluster mutation remain untouched.

```text
The Book orients.

Implementation testifies.

Fidelity governs the crossing.
```
