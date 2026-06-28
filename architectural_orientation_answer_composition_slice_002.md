# Architectural Orientation Answer Composition Slice 002

## Selected architectural boundary

Recovered exactly one implementation boundary:

```text
Evidence Collection
    !=
Architectural Orientation Answer Composition
```

The slice is implementation-local and compatibility-preserving. It does not add a CLI, registry, planner, renderer, schema, event, JSON shape, ledger behavior, family-status behavior, inquiry field, evidence field, or architectural subsystem.

## Implementation evidence

- `build_inquiry_orientation()` remains the compatibility adapter from composed answer material into the existing `InquiryOrientationView` shape.
- `_ArchitecturalOrientationAnswer` already represented answer composition material with `answer`, `reason`, `support`, `boundary`, and `limitations`.
- Before this slice, `_compose_architectural_orientation_answer()` also performed repository evidence collection by tokenizing the inquiry note and directly calling fact-support and source-navigation match collectors.
- `_fact_matches()` and `_source_navigation_matches()` remain the repository-evidence mechanisms. This slice only moved their orchestration behind an implementation-local evidence handoff.

## Before

Repository evidence collection and architectural orientation answer composition were mixed inside `_compose_architectural_orientation_answer()`:

```text
_compose_architectural_orientation_answer
    -> tokenize inquiry note
    -> collect projected fact-support matches
    -> collect source-navigation matches
    -> dedupe and bound related material
    -> compose answer/reason/support/boundary/limitations
```

That compressed the evidence-primary path because the function that composed the answer also owned the evidence collection handoff.

## After

Evidence collection is now represented by `_ArchitecturalOrientationEvidence` and `_collect_architectural_orientation_evidence()` before answer composition:

```text
_collect_architectural_orientation_evidence
    -> tokenize inquiry note
    -> collect projected fact-support matches
    -> collect source-navigation matches
    -> dedupe and bound related material
    -> return implementation-local evidence payload

_compose_architectural_orientation_answer
    -> receive implementation-local evidence payload
    -> compose answer/reason/support/boundary/limitations
```

The public orientation view remains unchanged:

```text
build_inquiry_orientation
    -> _compose_architectural_orientation_answer
    -> InquiryOrientationView
```

## Boundary made explicit

The recovered boundary is directly observable in implementation:

- `_ArchitecturalOrientationEvidence` contains collected repository material only.
- `_collect_architectural_orientation_evidence()` owns the evidence handoff.
- `_compose_architectural_orientation_answer()` composes the existing answer payload from that evidence.
- The test proves the evidence payload is not an answer payload and that composed answer material remains the same material rendered through the existing view.

## Compatibility preserved

No compatibility boundary changed.

Expected answer: No.

The existing CLI, rendering, JSON behavior, event ledger behavior, schema shape, authority boundary text, uncertainty text, related-material selection, and orientation output remain unchanged.

## Files changed

- `seed_runtime/inquiry_orientation.py`
  - Added `_ArchitecturalOrientationEvidence`.
  - Added `_collect_architectural_orientation_evidence()`.
  - Updated `_compose_architectural_orientation_answer()` to consume the evidence payload instead of collecting evidence inline.
- `tests/test_inquiry_orientation.py`
  - Updated the existing answer-composition separation test to prove evidence collection is a separate implementation-local payload before answer composition.
- `architectural_orientation_answer_composition_slice_002.md`
  - Preserved this implementation-backed report.

## LOC changed

From `git diff --stat`:

```text
architectural_orientation_answer_composition_slice_002.md | 125 +++++++++++++++++++++
seed_runtime/inquiry_orientation.py                |  25 ++++-
tests/test_inquiry_orientation.py                  |  10 +-
3 files changed, 155 insertions(+), 5 deletions(-)
```

## Tests executed

```text
pytest -q tests/test_inquiry_orientation.py
```

Result:

```text
11 passed
```

## Remaining compressed answer-composition boundaries

This slice intentionally stops after one recovered boundary.

Remaining compressed boundaries were not changed. Possible future implementation evidence to inspect, without treating this report as a plan or registry, includes whether other inquiry or architectural answer paths still combine:

```text
repository evidence lookup
answer material composition
presentation/view compatibility adaptation
```

No new surface, vocabulary migration, semantics, or architectural concept was introduced here.
