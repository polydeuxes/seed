# Surveyor Implementation Slice 001

Recovered exactly one implementation-local ownership boundary: **bounded related-material selection for Inquiry Orientation**.

This campaign began from the implementation immediately adjacent to the current Surveyor implementation evidence: the existing Inquiry Orientation implementation in `seed_runtime/inquiry_orientation.py` and its tests in `tests/test_inquiry_orientation.py`. The constitutional characterization oriented the investigation only by identifying Surveyor as pre-recovery and bounded; it did not select the boundary. The implementation selected the boundary because `_collect_inquiry_orientation_evidence(...)` still collected source evidence and also performed the downstream output-bounding step by deduplicating related material and applying `_MAX_RELATED_ITEMS` before producing `_InquiryOrientationEvidence`.

## Selected boundary

The selected boundary is the transfer of **deduplication and maximum related-material selection** from evidence collection into selected-material preparation.

This is intentionally narrow. It does not redesign Surveyor, Inquiry Orientation, recovery, orientation, CLI behavior, JSON output, diagnostics, schemas, event-ledger behavior, or public compatibility. It only makes the already-existing implementation-local boundary observable: raw collected orientation evidence is collected first, then the selected-material helper owns the bounded related-material slice consumed by answer composition.

## Implementation evidence

Implementation evidence exposed the boundary directly:

- `_collect_inquiry_orientation_evidence(...)` already had a single collection responsibility: gather fact-support matches and source-navigation matches for note tokens.
- `_InquiryOrientationEvidence` already represented collected evidence as `related_material`.
- `_prepare_inquiry_orientation_selected_material(...)` already represented the next step: prepare selected related material and support strings before answer construction.
- The compressed body in `_collect_inquiry_orientation_evidence(...)` previously also called `_dedupe_related(...)` and sliced to `_MAX_RELATED_ITEMS`, which are selection responsibilities rather than evidence-collection responsibilities.
- Existing tests already proved the composition chain from request, evidence, selected material, answer, view, and renderer. The new test adds the missing proof that evidence can contain the unbounded collected rows while selected material owns the deduped and capped related-material slice.

## Before

Before this slice, `_collect_inquiry_orientation_evidence(...)` performed two responsibilities:

1. collected related material from projected fact supports and source navigation; and
2. deduplicated and capped that material to the public related-material limit.

That compressed the evidence producer and the selected-material producer into one local function body. `_prepare_inquiry_orientation_selected_material(...)` preserved support strings, but it received material that had already been selected.

## After

After this slice:

1. `_collect_inquiry_orientation_evidence(...)` only collects fact-support and source-navigation matches and returns `_InquiryOrientationEvidence`.
2. `_select_inquiry_orientation_related_material(...)` performs the bounded related-material selection by deduplicating collected evidence and applying `_MAX_RELATED_ITEMS`.
3. `_prepare_inquiry_orientation_selected_material(...)` consumes the selected related material and preserves support strings for answer composition.

Runtime output remains unchanged because the same `_dedupe_related(...)` ordering and `_MAX_RELATED_ITEMS` cap are still applied before answer composition and view construction.

## Recovered producer

The recovered producer is `_prepare_inquiry_orientation_selected_material(...)`, supported by the new local helper `_select_inquiry_orientation_related_material(...)`.

It now owns the selected related-material slice that answer composition consumes.

## Recovered artifact/helper

The recovered helper is `_select_inquiry_orientation_related_material(...)`.

It carries the recovered boundary by accepting `_InquiryOrientationEvidence` and returning the bounded `list[RelatedMaterial]` selected through the existing dedupe and cap behavior.

## Recovered consumer

The immediate consumer is `_prepare_inquiry_orientation_selected_material(...)`, which uses the bounded selected material to construct `_InquiryOrientationSelectedMaterial` and preserve support strings.

Downstream consumers remain unchanged:

- `_prepare_inquiry_orientation_answer(...)` consumes `_InquiryOrientationSelectedMaterial`;
- `_compose_inquiry_orientation_answer(...)` returns the same answer artifact shape;
- `build_inquiry_orientation(...)` returns the same `InquiryOrientationView` shape;
- `format_inquiry_orientation(...)` renders the same output sections.

## Compatibility preserved

Did any compatibility boundary change?

```text
No.
```

Public compatibility is preserved:

- no CLI flag changed;
- no JSON shape changed;
- no diagnostic surface changed;
- no schema changed;
- no event-ledger behavior changed;
- no record behavior changed;
- no public dataclass field changed;
- no renderer section changed;
- no ordering or maximum related-material behavior changed.

## Files changed

- `seed_runtime/inquiry_orientation.py`
- `tests/test_inquiry_orientation.py`
- `surveyor_implementation_slice_001.md`

## LOC changed

Staged diffstat is:

```text
seed_runtime/inquiry_orientation.py  |  20 +++--
surveyor_implementation_slice_001.md | 137 +++++++++++++++++++++++++++++++++++
tests/test_inquiry_orientation.py    |  38 ++++++++++
3 files changed, 188 insertions(+), 7 deletions(-)
```

Staged numstat is:

```text
13	7	seed_runtime/inquiry_orientation.py
137	0	surveyor_implementation_slice_001.md
38	0	tests/test_inquiry_orientation.py
```

## Tests executed

```text
python -m pytest -q tests/test_inquiry_orientation.py
```

Result:

```text
16 passed
```

## Remaining compressed responsibilities

The following responsibilities remain intentionally outside this slice because exactly one implementation-local ownership boundary was recovered:

- fact-support match construction inside `_fact_matches(...)`;
- source-navigation match construction inside `_source_navigation_matches(...)`;
- token normalization inside `_note_tokens(...)`;
- related-material dedupe ordering inside `_dedupe_related(...)`;
- answer reason selection;
- authority-boundary selection;
- limitation/uncertainty selection;
- answer artifact construction;
- view construction;
- text rendering.

No additional Surveyor capability, investigator, planner, workflow, registry, methodology redesign, orientation redesign, or recovery redesign was introduced.
