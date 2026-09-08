# Answer Composition Slice 005

## selected architectural boundary

Supporting Evidence != Limitations inside `InquiryArtifactVisibility` composition.

## implementation evidence

`seed_runtime/inquiry_artifacts.py` exposed each inquiry artifact through the public `InquiryArtifactVisibility` compatibility object. The object carried `evidence` and `limitations` together, while `to_json_dict()` converted both into the unchanged public JSON shape. The same module also kept the diagnostic boundary separate in `BOUNDARY`, so the remaining compression in this slice was not the diagnostic boundary itself; it was the artifact-local supporting evidence and limitations material being authored directly inside the compatibility object.

## before

The `ARTIFACTS` registry constructed `InquiryArtifactVisibility` entries directly. For each entry, supporting evidence and limitations were adjacent fields on the public compatibility object, so implementation-local answer composition was not directly observable before the compatibility handoff.

## after

The module now has implementation-local `_InquiryArtifactEvidencePayload` and `_InquiryArtifactLimitationsPayload` records plus `_artifact_visibility_from_payloads(...)`. Selected inquiry artifact rows now compose support and limitation payloads first, then hand them into the unchanged `InquiryArtifactVisibility` compatibility object.

## boundary made explicit

Supporting evidence is now represented by `_InquiryArtifactEvidencePayload`; limitations are now represented by `_InquiryArtifactLimitationsPayload`. `_artifact_visibility_from_payloads(...)` is the compatibility handoff point.

## compatibility preserved

No.

No compatibility boundary changed. The public dataclass fields, formatter behavior, CLI flags, JSON keys, diagnostic inventory, diagnostic shape-audit behavior, and read-only boundary remain unchanged.

## files changed

- `seed_runtime/inquiry_artifacts.py`
- `tests/test_inquiry_artifacts.py`
- `answer_composition_slice_005.md`

## LOC changed

`git diff --stat` before commit reported `2 files changed, 75 insertions(+), 13 deletions(-)` for implementation and tests; this report file is additive documentation for the slice.

## tests executed

- `pytest -q tests/test_inquiry_artifacts.py`
- `pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

## remaining compressed answer-composition boundaries

- Additional `InquiryArtifactVisibility` rows still author evidence and limitations directly and can be recovered in future slices if implementation evidence justifies continuing in this owner.
- `ReasoningPathAudit` still has a public compatibility object carrying evidence, conclusions, consumers, story impact, unknowns, and boundary together after its existing conclusion/lineage payload handoff.
- `SelectionPathAudit` still has a public compatibility object carrying result, lineage, unknowns, and boundary together after its existing result/lineage payload handoff.
- Other bounded answer surfaces should not be projected into this slice without fresh implementation evidence.
