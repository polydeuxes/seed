# Implementation Recovery Slice 014

## Selected boundary

Recovered exactly one implementation-local ownership boundary immediately adjacent to the Slice 013 post-dispatch JSON compatibility owner:

```text
BoundedWorkDispatchResult
↓
apply_bounded_work_dispatch_result(...)
↓
clear_bounded_ask_dispatch_message(...)
↓
apply_bounded_ask_dispatch_handoff(...)
```

The selected boundary is the post-dispatch bounded-ask handoff that consumes an already executed bounded-work dispatch result, applies existing compatibility handling, and clears the compatibility `ask` message.

## Relevant Book neighborhood

Smallest relevant Book neighborhood:

- `book_of_seed/01-grammar-and-standing/external-and-constitutional-grammar.md`: realization and implementation grammars remain external grammar; a recovered distinction may receive standing while the carrier grammar remains external.
- `book_of_seed/07-operational-realization/execution-and-recording.md`: invocation, completed execution, execution result, recording, and established fact remain separate.

This operation used the Book only for orientation. Implementation evidence determined the local mechanics.

## Campaign-frontier applicability

Current campaign frontier:

```text
bounded ask exact QuestionFamily path
→ bounded eligibility
→ surface args / value / dispatch surface selection
→ dispatch request
→ namespace dispatch execution
→ dispatch result production
→ knowledge-reachability JSON compatibility owner recovered in Slice 013
```

Candidate implementation neighborhood:

```text
scripts.seed_local.apply_bounded_ask_dispatch(...)
```

Immediately after the Slice 013 compatibility helper was consumed, `apply_bounded_ask_dispatch(...)` still performed the same two-step post-dispatch handoff in both the `eligible_with_parameters` branch and the `eligible_now` branch:

```text
apply_bounded_work_dispatch_result(args, dispatch_result)
clear_bounded_ask_dispatch_message(args, dispatch_result)
```

Constitutional distinction allegedly realized:

```text
post-dispatch handoff != dispatch execution
post-dispatch compatibility/message cleanup != inquiry authority
operator invocation carrier != established fact
```

Concrete realization seam:

```text
apply_bounded_ask_dispatch_handoff(args, dispatch_result)
```

The seam is eligible because it is not selected by slice numbering alone: it directly consumes the Slice 013 owner and the already existing message-clear helper at the next local boundary in the bounded-ask dispatch path.

## Containing-road classification

The containing road is classified as:

```text
compatibility-only
```

Bounded reason: the selected local seam lives in the public `ask --question-family` CLI compatibility path that maps exact question-family text to existing implementation surfaces. This does not establish that the larger inquiry road, Question Family system, CLI, or view system is canonical internal Seed road.

## Constitutional distinction

The local distinction exposed at the seam is:

```text
completed bounded-work dispatch result consumption
!= dispatch execution
!= answer composition
!= inquiry origination
!= constitutional authority
```

The handoff may consume an implementation dispatch result and perform compatibility cleanup. It may not become a constitutional question owner, execution warrant, rendering owner, or evidence authority.

## Implementation evidence

Implementation evidence supporting the seam:

- `BoundedWorkDispatchResult` carries only `question_family`, `dispatch_surface`, `surface_value`, and `reason`.
- `apply_bounded_work_dispatch_result(...)` delegates to the Slice 013 knowledge-reachability JSON compatibility helper.
- `clear_bounded_ask_dispatch_message(...)` clears the compatibility `ask` message after dispatch handoff and returns only a message-clear result.
- `scripts.seed_local.apply_bounded_ask_dispatch(...)` duplicated the result-compatibility and message-clear sequence in both dispatch branches.
- Tests now assert the recovered handoff consumes a dispatch result, preserves the knowledge-reachability JSON compatibility behavior, clears the message, and does not carry dispatch surface, surface value, or required surface args in the returned message-clear artifact.

## Bounded Fidelity classification

```text
faithful within scope
```

The realization is faithful within the selected local scope because it preserves the Book-oriented distinctions between execution result, compatibility cleanup, and constitutional authority. The recovered helper only composes existing post-dispatch implementation responsibilities after dispatch has already executed. It does not authorize or execute work, establish truth, create records, render answers, infer inquiry, or promote CLI vocabulary into constitutional grammar.

## Before

`apply_bounded_ask_dispatch(...)` owned all of the following in each dispatch branch:

```text
select bounded work
construct dispatch request
execute dispatch
apply post-dispatch compatibility
clear bounded ask message
return from compatibility path
```

The post-dispatch handoff was duplicated and compressed into the larger CLI compatibility path.

## After

`apply_bounded_ask_dispatch_handoff(...)` owns only:

```text
consume already executed BoundedWorkDispatchResult
apply existing post-dispatch compatibility handling
clear existing bounded ask dispatch message
return existing message-clear result
```

`apply_bounded_ask_dispatch(...)` still owns the surrounding CLI compatibility flow and now delegates the local post-dispatch handoff in both dispatch branches.

## Recovered or corrected owner

Recovered owner:

```text
apply_bounded_ask_dispatch_handoff(...)
```

No correction of runtime behavior was required.

## Recovered artifact/helper

Recovered helper:

```text
apply_bounded_ask_dispatch_handoff(args, dispatch_result)
```

Input artifact:

```text
BoundedWorkDispatchResult
```

Returned artifact:

```text
BoundedAskDispatchMessageClearResult
```

No new registry, framework, engine, universal view composer, universal question owner, schema, diagnostic surface, event-ledger behavior, or inquiry architecture was introduced.

## Recovered consumer

Consumer:

```text
scripts.seed_local.apply_bounded_ask_dispatch(...)
```

It consumes the helper in the `eligible_with_parameters` dispatch branch and the `eligible_now` dispatch branch.

## Negative authority

The recovered helper does not possess authority to:

- admit or originate inquiry;
- choose a question family;
- determine bounded eligibility;
- validate surface arguments;
- select a dispatch surface or surface value;
- construct or execute dispatch requests;
- render JSON generally;
- compose answers or views;
- inspect evidence;
- establish knowledge or cluster truth;
- write the event ledger;
- mutate cluster state;
- deprecate or redefine public CLI compatibility.

## Compatibility treatment

Compatibility behavior was preserved. The public CLI path still maps eligible exact question-family bounded asks to the same existing surfaces, preserves the Slice 013 knowledge-reachability JSON compatibility behavior, and clears the `ask` message after dispatch.

## Runtime behavior treatment

Runtime behavior did not change. The same underlying functions execute in the same order for the selected handoff:

```text
apply_bounded_work_dispatch_result(...)
clear_bounded_ask_dispatch_message(...)
```

The code now gives that sequence a local owner.

## Files changed

- `seed_runtime/question_surface_inventory.py`
- `scripts/seed_local.py`
- `tests/test_question_surface_inventory.py`
- `implementation_recovery_slice_014.md`

## LOC changed

Before this report file was added, git diff reported:

```text
scripts/seed_local.py                      |  9 +++------
seed_runtime/question_surface_inventory.py | 20 ++++++++++++++++++++
tests/test_question_surface_inventory.py   | 28 ++++++++++++++++++++++++++++
3 files changed, 51 insertions(+), 6 deletions(-)
```

Including this report, the operation adds one narrow helper, one direct regression test, rewires the existing caller to use the helper, and adds this implementation-slice report.

## Tests executed

```text
pytest -q tests/test_question_surface_inventory.py
```

Result:

```text
64 passed in 51.12s
```

## Required questions

1. **What is the smallest relevant Book neighborhood?**

   External and Constitutional Grammar plus Execution and Recording, limited to external implementation carriers and the distinction between execution result consumption, compatibility cleanup, recording, and established fact.

2. **What is the current bounded campaign frontier?**

   The bounded-ask exact QuestionFamily compatibility path immediately after Slice 013's post-dispatch knowledge-reachability JSON compatibility owner.

3. **Why is the selected implementation neighborhood eligible for that frontier?**

   It directly consumes the Slice 013 helper through `apply_bounded_work_dispatch_result(...)` and performs the immediately adjacent message-clear handoff in both bounded-ask dispatch branches.

4. **Is the containing road internal, compatibility-only, diagnostic, scaffolding, historical, deprecated, or Unknown?**

   Compatibility-only within this bounded finding. Larger-road standing remains unresolved.

5. **What constitutional distinction is exposed at the selected local seam?**

   Post-dispatch handoff is not dispatch execution, answer composition, inquiry origination, constitutional authority, or established fact.

6. **What implementation evidence supports the seam?**

   The dispatch result artifact, the Slice 013 compatibility helper, the message-clear helper, duplicated caller sequence, and the new regression test support the seam.

7. **What bounded Fidelity classification is warranted?**

   Faithful within scope.

8. **What responsibilities were previously compressed?**

   The larger bounded-ask CLI flow compressed post-dispatch compatibility application and bounded-ask message clearing into each dispatch branch.

9. **Which single implementation-local boundary became directly observable?**

   The post-dispatch bounded-ask handoff became directly observable.

10. **What owner now carries the recovered responsibility, or what smallest correction restores Fidelity?**

    `apply_bounded_ask_dispatch_handoff(...)` now carries the recovered responsibility. No Fidelity correction was required.

11. **What artifact or helper carries the boundary, if any?**

    Helper: `apply_bounded_ask_dispatch_handoff(...)`; input artifact: `BoundedWorkDispatchResult`; returned artifact: `BoundedAskDispatchMessageClearResult`.

12. **Who consumes it?**

    `scripts.seed_local.apply_bounded_ask_dispatch(...)` consumes it.

13. **What authority does the recovered owner or artifact not possess?**

    It does not possess inquiry, eligibility, selection, execution, answer, rendering, evidence, recording, cluster mutation, schema, diagnostic, or deprecation authority.

14. **What compatibility boundary is implicated?**

    The public `ask --question-family <exact-question-family>` bounded-ask dispatch compatibility path.

15. **Did compatibility or runtime behavior change?**

    No.

16. **What larger-road standing remains deliberately unresolved?**

    Whether the broader CLI, Question Family system, inquiry road, or view road is canonical internal Seed road remains deliberately unresolved.

17. **What adjacent responsibilities remain untouched?**

    Exact lookup, eligibility, refusal, surface-arg validation, selection, dispatch request construction, namespace mutation, result production, presentation handoff, JSON rendering, answer composition, diagnostics, schema, event ledger behavior, semantic routing, and public CLI grammar remain untouched.

## Remaining compressed responsibilities

Remaining compressed responsibilities deliberately left untouched:

- the non-QuestionFamily `ask` message validation path;
- exact QuestionFamily lookup and admission;
- bounded eligibility and refusal;
- surface-argument validation;
- selected dispatch surface/value production;
- dispatch request construction;
- namespace mutation and result production;
- presentation handoff production/consumption;
- answer composition and rendering;
- diagnostic inventory and shape audit linkage;
- schema and event-ledger behavior;
- semantic routing.

## Preserved Unknowns

Preserved Unknowns:

- Whether the broader `ask` surface is canonical internal road, compatibility-only, transitional, or mixed.
- Whether additional bounded-ask branch-level handoffs should be recovered later.
- Whether public QuestionFamily labels should receive a different long-term compatibility boundary.
- Whether any containing view or inquiry road needs future Fidelity correction.

## Unresolved containing-road standing

This slice does not classify the entire CLI, Question Family system, inquiry road, diagnostic road, or view road. It classifies only the selected local containing road as compatibility-only for this bounded seam and preserves larger standing as Unknown.
