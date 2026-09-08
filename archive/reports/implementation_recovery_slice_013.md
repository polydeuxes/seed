# Implementation Recovery Slice 013

## Selected boundary

Recovered exactly one implementation-local ownership boundary immediately adjacent to the post-dispatch bounded-work handoff recovered in slice 012:

```text
BoundedWorkDispatchResult
↓
apply_knowledge_reachability_json_dispatch_compatibility(...)
↓
apply_bounded_work_dispatch_result(...)
```

The selected boundary is the narrow knowledge-reachability `--json` compatibility toggle after an already executed bounded-work dispatch result exists.

## Relevant Book neighborhood

Smallest relevant Book neighborhood:

- `book_of_seed/01-grammar-and-standing/external-and-constitutional-grammar.md`, especially the boundary that realization languages, serialization, persistence, cache, and implementation grammars remain external grammar, and that cross-seam consumption must carry authority limits and negative authority rather than converting carrier vocabulary into constitutional standing.
- `book_of_seed/07-operational-realization/execution-and-recording.md`, especially the distinction between invocation, completed execution, execution result, recording, and established fact.

This operation did not survey or rewrite the Book.

## Implicated Book branches

- External Grammar.
- Internal Constitutional Grammar.
- Fidelity.

## Constitutional distinction being preserved

The distinction preserved is:

```text
compatibility carrier != authority
post-dispatch result consumption != execution warrant
JSON presentation compatibility != constitutional standing
successful CLI routing != established fact
```

The existing `--json` and `knowledge_reachability_audit_json` names are CLI and compatibility grammar. They may continue to drive the implementation's existing dispatch pathway, but they do not become constitutional authority, knowledge, warrant, evidence examination, or completion.

## External grammar encountered

External, compatibility, framework, and implementation grammar encountered:

- CLI namespace attributes: `json_output` and `knowledge_reachability_audit_json`.
- CLI-facing dispatch family text: `knowledge reachability`.
- Python dataclass and helper names: `BoundedWorkDispatchResult`, `apply_bounded_work_dispatch_result(...)`, and `apply_knowledge_reachability_json_dispatch_compatibility(...)`.
- Compatibility aliasing from the older `knowledge_reachability_audit_json` surface to the bounded ask path.

These remain implementation-local carrier vocabulary only.

## Implementation evidence

Adjacent implementation evidence showed that:

- `execute_bounded_work_dispatch(...)` now applies the selected request to the CLI namespace and returns `bounded_work_dispatch_result_for_request(...)`.
- `BoundedWorkDispatchResult` carries only `question_family`, `dispatch_surface`, `surface_value`, and a reason string.
- `apply_bounded_work_dispatch_result(...)` still combined generic post-dispatch result consumption with one narrow compatibility branch: if the result question family is `knowledge reachability` and `args.json_output` is true, set `args.knowledge_reachability_audit_json` true and clear `args.json_output`.
- Tests already asserted that this compatibility branch is specific to knowledge reachability and does not alter non-compatibility JSON dispatches.

That made one directly observable ownership seam: the knowledge-reachability JSON compatibility toggle was compressed inside generic post-dispatch result consumption.

## Bounded Fidelity classification

Faithful within scope.

The realization preserves the relevant distinction because it treats the compatibility toggle as post-dispatch CLI compatibility after an implementation-backed dispatch result exists. It does not claim that `--json`, the compatibility flag, or the question-family label supplies constitutional standing, warrant, evidence examination, or cluster truth.

## Before

`apply_bounded_work_dispatch_result(...)` owned both:

```text
consume BoundedWorkDispatchResult
maybe apply knowledge-reachability JSON compatibility toggle
return BoundedWorkDispatchResult
```

The narrow compatibility predicate and namespace mutation were present but not locally owned.

## After

`apply_knowledge_reachability_json_dispatch_compatibility(...)` owns only the existing compatibility toggle:

```text
if dispatch_result.question_family == "knowledge reachability"
   and args.json_output:
    args.knowledge_reachability_audit_json = True
    args.json_output = False
return dispatch_result
```

`apply_bounded_work_dispatch_result(...)` now consumes the dispatch result by delegating to that compatibility helper and returning the same result.

## Recovered producer or corrected owner

Recovered producer:

```text
apply_knowledge_reachability_json_dispatch_compatibility(...)
```

It owns the post-dispatch knowledge-reachability JSON compatibility toggle only.

## Recovered artifact/helper

Recovered helper:

```text
apply_knowledge_reachability_json_dispatch_compatibility(...)
```

Artifact crossing the boundary:

```text
BoundedWorkDispatchResult
```

No new framework, engine, registry, universal compatibility system, dispatcher, schema, diagnostic surface, event-ledger behavior, or constitutional owner was introduced.

## Recovered consumer

`apply_bounded_work_dispatch_result(...)` consumes the helper result.

## Negative authority

The recovered helper does not possess constitutional standing. It does not establish knowledge reachability, authorize inquiry, execute bounded work, verify evidence, create warrant, record an event, mutate cluster truth, select a question family, choose a dispatch surface, render JSON generally, or prove completion.

## Compatibility classification

Constitutionally neutral compatibility.

## Compatibility treatment

Compatibility remained unchanged. The public CLI representation and namespace behavior are preserved: knowledge-reachability bounded ask with `--json` still sets `knowledge_reachability_audit_json` and clears the general `json_output` flag, while unrelated JSON bounded asks keep `json_output` true.

## Runtime behavior treatment

Runtime behavior remained unchanged. The same predicate, assignments, return object, CLI behavior, JSON behavior, diagnostics, schemas, and event-ledger behavior are preserved.

## Files changed

- `seed_runtime/question_surface_inventory.py`
- `tests/test_question_surface_inventory.py`
- `implementation_recovery_slice_013.md`

## LOC changed

Before this report file was added, git diff reported:

```text
seed_runtime/question_surface_inventory.py | 27 ++++++++++++---
tests/test_question_surface_inventory.py   | 54 ++++++++++++++++++++++++++++++
2 files changed, 77 insertions(+), 4 deletions(-)
```

Current line-oriented change count before staging: 23 insertions and 4 deletions in `seed_runtime/question_surface_inventory.py`, 54 insertions in `tests/test_question_surface_inventory.py`, and this 287-line report file.

Including this report, the operation adds one narrow helper, one direct regression test, and this implementation-slice report.

## Tests executed

```text
pytest -q tests/test_question_surface_inventory.py
```

Result:

```text
63 passed in 50.86s
```

## Required questions

1. **What is the smallest relevant Book neighborhood?**

   The smallest relevant neighborhood is External and Constitutional Grammar plus Execution and Recording, limited to compatibility/external carrier vocabulary and post-dispatch result boundaries.

2. **Which Book branches are implicated?**

   External Grammar, Internal Constitutional Grammar, and Fidelity.

3. **What constitutional distinction must survive in this implementation area?**

   Compatibility carrier is not authority; post-dispatch result consumption is not execution warrant; JSON presentation compatibility is not constitutional standing or established knowledge.

4. **What external grammar, compatibility grammar, framework grammar, or model-generated grammar is present?**

   CLI flags and namespace names, dispatch family text, Python helper/dataclass names, and the legacy `knowledge_reachability_audit_json` compatibility surface.

5. **What implementation evidence is immediately adjacent to the most recently recovered slice?**

   Slice 012 recovered namespace update before dispatch-result production. The next adjacent implementation is `apply_bounded_work_dispatch_result(...)`, which consumed a dispatch result while still owning a narrow knowledge-reachability JSON compatibility toggle.

6. **What bounded Fidelity result is supported?**

   Faithful within scope.

7. **What responsibilities were previously compressed?**

   Generic post-dispatch result consumption and the knowledge-reachability `--json` compatibility toggle were compressed inside `apply_bounded_work_dispatch_result(...)`.

8. **Which implementation-local boundary became directly observable?**

   The post-dispatch knowledge-reachability JSON compatibility toggle became directly observable.

9. **If the realization is faithful, what producer now owns the recovered responsibility?**

   `apply_knowledge_reachability_json_dispatch_compatibility(...)`.

10. **If the realization is unfaithful, what smallest correction restores the constitutional distinction?**

    Not applicable; the bounded classification is faithful within scope.

11. **What artifact or helper carries the recovered boundary, if any?**

    The helper is `apply_knowledge_reachability_json_dispatch_compatibility(...)`; the crossing artifact is `BoundedWorkDispatchResult`.

12. **Who consumes it?**

    `apply_bounded_work_dispatch_result(...)` consumes the helper result.

13. **What constitutional standing does the artifact or helper not possess?**

    It does not possess authority, warrant, evidence standing, knowledge standing, execution authorization, cluster-truth standing, or completion standing.

14. **What compatibility boundary is implicated?**

    The legacy knowledge-reachability JSON bounded-ask compatibility path.

15. **Is that compatibility neutral, unfaithful, or Unknown?**

    Neutral.

16. **Did compatibility remain unchanged, adapt without public-shape change, narrow, become quarantined, require removal, or remain Unknown?**

    Compatibility remained unchanged.

17. **Did runtime behavior change?**

    No.

18. **If behavior changed, was the change strictly required by the bounded Fidelity correction?**

    Not applicable; behavior did not change.

19. **Did the operation reveal bounded Book projection pressure?**

    No bounded Book projection pressure required correction. The Book orients the distinction, but implementation evidence determines this helper boundary.

20. **What remaining compressed responsibilities or Unknowns were deliberately left untouched?**

    General JSON rendering, diagnostic JSON formatting, inventory aliases, dispatch request construction, dispatch execution, message clearing, presentation clearing, answer composition, schema, event-ledger behavior, and semantic routing remain untouched. Whether other bounded-work compatibility branches should later receive local helpers remains Unknown until adjacent implementation evidence is selected.

## Remaining compressed responsibilities

Remaining compressed responsibilities were deliberately left untouched:

- general JSON output behavior;
- diagnostic JSON rendering;
- question-family lookup and eligibility;
- bounded-work selection;
- dispatch request construction;
- dispatch execution;
- post-dispatch message clearing;
- post-presentation message clearing;
- presentation handoff production and consumption;
- answer composition;
- diagnostic inventory and diagnostic shape audit surfaces;
- schema and event ledger behavior;
- semantic routing.

## Preserved Unknowns

Preserved Unknowns:

- Whether any other compatibility branch deserves a recovered local helper.
- Whether the Book should later say more about CLI compatibility carriers.
- Whether the legacy `knowledge_reachability_audit_json` compatibility name should ever be deprecated.

## Bounded Book projection pressure

No Book correction was made. No Book wording was treated as an implementation owner. Any difference between Book vocabulary and Python helper names remains a projection/realization difference rather than a constitutional conflict.
