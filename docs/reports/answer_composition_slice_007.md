# Answer Composition Slice 007

## selected inquiry surface

`SelectionPathAudit`.

## selected recovered boundary

```text
Reason
    !=
Supporting Evidence
```

## implementation evidence

Fresh implementation review showed that `SelectionPathAudit` had already made the selected answer and reason/outcome explicit through `_SelectionResultPayload` and `_SelectionReasonPayload`.

The remaining implementation-local compression was in the compatibility handoff payload for selection lineage: `_SelectionLineagePayload` owned candidate lineage fields and also owned the public `evidence` field that supports the outcome. That meant supporting evidence was still bundled with candidate/selection lineage before `_selection_path_from_payloads(...)` constructed the unchanged public `SelectionPathAudit` object.

The public audit object and formatter already exposed `Evidence:` separately from `Outcome:`, so this slice only made the implementation ownership handoff match the already-visible composition boundary.

## before

`_SelectionLineagePayload` owned:

```text
candidates
selection_factors
non_selected
evidence
unknowns
```

`_selection_path_from_payloads(...)` copied `lineage.evidence` into `SelectionPathAudit.evidence`, while `_SelectionReasonPayload` copied `reason.outcome` into `SelectionPathAudit.outcome`.

## after

This slice adds one private implementation-local payload:

```text
_SelectionSupportingEvidencePayload
```

`_SelectionSupportingEvidencePayload` owns:

```text
evidence
```

`_SelectionLineagePayload` now owns only:

```text
candidates
selection_factors
non_selected
unknowns
```

`_selection_path_from_payloads(...)` now accepts separate result, reason, supporting-evidence, and lineage payloads, then performs the same compatibility handoff into the unchanged public `SelectionPathAudit` object.

## boundary made explicit

The reason/outcome material remains represented by `_SelectionReasonPayload`.

The supporting evidence material is now represented by `_SelectionSupportingEvidencePayload`.

This makes the recovered boundary explicit inside the Selection Path implementation:

```text
Reason
    !=
Supporting Evidence
```

## compatibility preserved

No.

No compatibility boundary changed. The public `SelectionPathAudit` dataclass fields, JSON keys, formatter sections, CLI behavior, diagnostic inventory registration, diagnostic shape-audit behavior, event behavior, ledger behavior, and read-only mutation boundary remain unchanged.

## files changed

- `seed_runtime/selection_path_audit.py`
- `tests/test_selection_path_audit.py`
- `answer_composition_slice_007.md`

## LOC changed

Implementation and test diff before this report:

```text
seed_runtime/selection_path_audit.py | 15 +++++++++----
tests/test_selection_path_audit.py   | 41 +++++++++++++++++++++++++++++++++++-
2 files changed, 51 insertions(+), 5 deletions(-)
```

This report was then added as the required deliverable.

## tests executed

```text
pytest -q tests/test_selection_path_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

Result:

```text
53 passed in 27.44s
```

## remaining composition ownership inside SelectionPathAudit

`SelectionPathAudit` still carries the public compatibility object with selected answer, reason/outcome, supporting evidence, lineage, unknowns, and boundary together. That public object remains intentionally unchanged for compatibility.

Inside the implementation handoff, result, reason, supporting evidence, and selection lineage are now separate private payloads. Remaining possible local pressure, subject to future implementation evidence, is the recovered downstream boundary between supporting evidence and boundary/limitations material: unknowns and the read-only boundary still meet the public compatibility object without a further private composition payload.

## remaining inquiry surfaces

Remaining possible future Answer Composition compression points, subject to fresh implementation evidence:

- Additional `InquiryArtifactVisibility` rows still author evidence and limitations directly, even though selected rows now use evidence and limitations payloads.
- `ReasoningPathAudit` still carries derivation evidence, conclusions, consumers, story impact, unknowns, and boundary in one public audit object after its existing conclusion/lineage payload handoff.
- `SelectionPathAudit` may still have local pressure around supporting evidence versus boundary/limitations material, but this slice stopped after one recovered ownership transition.
- `InquiryOrientationView` still carries note, related material, uncertainty, and authority boundary in one public view object after its existing implementation-local answer composition handoff.

## questions answered with implementation evidence

1. Where did SelectionPathAudit still compress an already-recovered Answer Composition boundary?

   `SelectionPathAudit` compressed supporting evidence into `_SelectionLineagePayload`, so evidence was handed off as lineage rather than as its own supporting-evidence owner.

2. Which recovered boundary became more explicit?

   `Reason != Supporting Evidence` became explicit through `_SelectionReasonPayload` and `_SelectionSupportingEvidencePayload`.

3. How does the implementation now better reflect the recovered inquiry composition grammar?

   The Selection Path implementation now composes selected answer, reason/outcome, supporting evidence, and selection lineage as separate private payloads before handing the same values into the unchanged public compatibility object.

4. Did any compatibility boundary change?

   No.
