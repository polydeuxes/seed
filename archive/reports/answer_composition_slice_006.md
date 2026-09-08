# Answer Composition Slice 006

## selected inquiry surface

`SelectionPathAudit`.

## selected recovered boundary

```text
Answer
    !=
Reason
```

## implementation evidence

`seed_runtime/selection_path_audit.py` already exposed selection-path inquiry output through the public `SelectionPathAudit` compatibility object. Before this slice, the implementation had two private handoff payloads:

- `_SelectionResultPayload`, which carried both the selected answer and the outcome explanation.
- `_SelectionLineagePayload`, which carried candidates, selection factors, non-selected candidates, evidence, and unknowns.

That meant the surface had already separated result material from lineage material, but the selected answer and its reason/outcome remained compressed inside one implementation-local result payload.

The public compatibility object already exposed `selected` and `outcome` as separate fields, and the formatter already rendered `Selected:` separately from `Outcome:`. The remaining compression was therefore implementation-local, not public-schema or rendering behavior.

## before

`_SelectionResultPayload` owned both:

```text
selected
outcome
```

The compatibility handoff copied `result.selected` into `SelectionPathAudit.selected` and `result.outcome` into `SelectionPathAudit.outcome`. This compressed the recovered answer/reason distinction before the unchanged public audit object was constructed.

## after

This slice adds one private implementation-local payload:

```text
_SelectionReasonPayload
```

`_SelectionResultPayload` now owns only:

```text
selected
```

`_SelectionReasonPayload` owns:

```text
outcome
```

`_selection_path_from_payloads(...)` now accepts result, reason, and lineage payloads, then performs the same compatibility handoff into the unchanged `SelectionPathAudit` object.

## boundary made explicit

The selected answer is now represented by `_SelectionResultPayload`.

The reason/outcome material explaining that selected answer is now represented by `_SelectionReasonPayload`.

This makes the recovered boundary explicit inside the Selection Path implementation:

```text
Answer
    !=
Reason
```

## compatibility preserved

No.

No compatibility boundary changed. The public `SelectionPathAudit` dataclass fields, formatter sections, CLI behavior, JSON keys, diagnostic inventory registration, diagnostic shape-audit behavior, event behavior, ledger behavior, and read-only mutation boundary remain unchanged.

## files changed

- `seed_runtime/selection_path_audit.py`
- `tests/test_selection_path_audit.py`
- `answer_composition_slice_006.md`

## LOC changed

Implementation and test diff before this report:

```text
seed_runtime/selection_path_audit.py | 15 ++++++++++-----
tests/test_selection_path_audit.py   | 36 ++++++++++++++++++++++++++++++++++++
2 files changed, 46 insertions(+), 5 deletions(-)
```

This report was then added as the required deliverable.

## tests executed

```text
pytest -q tests/test_selection_path_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

Result:

```text
52 passed in 25.54s
```

## remaining inquiry surfaces still compressing the recovered Answer Composition grammar

Remaining possible future Answer Composition compression points, subject to fresh implementation evidence:

- Additional `InquiryArtifactVisibility` rows still author evidence and limitations directly, even though selected rows now use evidence and limitations payloads.
- `ReasoningPathAudit` still carries derivation evidence, conclusions, consumers, story impact, unknowns, and boundary in one public audit object after its existing conclusion/lineage payload handoff.
- `SelectionPathAudit` still carries the public compatibility object with result, reason/outcome, lineage, unknowns, and boundary together; this slice only separated the implementation-local answer/reason ownership transition.
- `InquiryOrientationView` still carries note, related material, uncertainty, and authority boundary in one public view object after its existing implementation-local answer composition handoff.

## questions answered with implementation evidence

1. Which inquiry surface still compressed an already-recovered Answer Composition boundary?

   `SelectionPathAudit` compressed the selected answer and outcome reason inside `_SelectionResultPayload`.

2. Which recovered boundary became more explicit?

   `Answer != Reason` became explicit through `_SelectionResultPayload` and `_SelectionReasonPayload`.

3. How does the implementation now better reflect the recovered inquiry composition grammar?

   The Selection Path implementation now composes the selected answer and the reason/outcome payload separately before handing both into the unchanged public compatibility object.

4. Did any compatibility boundary change?

   No.
