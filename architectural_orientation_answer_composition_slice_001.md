# Architectural Orientation Answer Composition Slice 001

## Selected architectural boundary

```text
Architectural Orientation Answer
    !=
Architectural Orientation Rendering
```

This slice selected exactly one recovered boundary: answer composition is now implementation-local and explicit before handoff to the existing inquiry orientation compatibility view and renderer.

## Implementation evidence

- `seed_runtime/inquiry_orientation.py` already built related material by deterministic token matching against projected fact supports and source-navigation matches.
- `seed_runtime/inquiry_orientation.py` already rendered the public `InquiryOrientationView` in `format_inquiry_orientation(...)`.
- `architectural_orientation_answer_composition_audit.md` concluded that architectural orientation should become an inquiry answer with `answer`, `reason`, `support`, `boundary`, and `limitations`, and that the next work should be answer composition rather than rendering.
- Prior Operational Story answer-composition slices established the compatibility-preserving pattern: compose implementation-local payloads first, then hand off into the unchanged public compatibility object.

## Before

`build_inquiry_orientation(...)` directly selected related material, chose uncertainty, and constructed the public `InquiryOrientationView` consumed by `format_inquiry_orientation(...)`.

That compressed architectural-orientation answer composition with the rendering-facing view shape:

```text
matching + answer meaning + uncertainty/boundary handoff
    -> InquiryOrientationView
    -> format_inquiry_orientation(...)
```

The public view remained correct, but the implementation did not make an implementation-local composed answer object directly observable.

## After

This slice added a private implementation-local `_ArchitecturalOrientationAnswer` with the required inquiry answer shape:

```text
answer
reason
support
boundary
limitations
```

`build_inquiry_orientation(...)` now calls `_compose_architectural_orientation_answer(...)` and performs a compatibility-preserving handoff into the unchanged public `InquiryOrientationView`.

No renderer, CLI, formatter, JSON, schema, event, ledger, registry, planner, or workflow behavior was added.

## Boundary made explicit

The recovered boundary is now directly observable in implementation:

```text
_ArchitecturalOrientationAnswer
    !=
InquiryOrientationView / format_inquiry_orientation(...)
```

The answer object composes existing implementation-backed evidence only:

- `answer`: existing `RelatedMaterial` matches;
- `reason`: deterministic lexical overlap against existing projected fact supports and source-navigation matches;
- `support`: existing per-match support strings;
- `boundary`: existing `AUTHORITY_BOUNDARY`;
- `limitations`: existing uncertainty text selected from existing match/no-match outcomes.

## Compatibility preserved

No compatibility boundary changed.

Expected answer:

```text
No.
```

The public `InquiryOrientationView` dataclass remains unchanged. `format_inquiry_orientation(...)` remains unchanged. Existing behavior and rendered output remain unchanged.

## Files changed

- `seed_runtime/inquiry_orientation.py`
- `tests/test_inquiry_orientation.py`
- `architectural_orientation_answer_composition_slice_001.md`

## LOC changed

From `git diff --numstat` before this report file was added:

```text
33 insertions, 5 deletions  seed_runtime/inquiry_orientation.py
27 insertions, 0 deletions  tests/test_inquiry_orientation.py
```

Report file added separately as this deliverable.

## Tests executed

```text
pytest -q tests/test_inquiry_orientation.py
```

Result:

```text
11 passed in 0.56s
```

## Remaining compressed architectural-orientation answer-composition boundaries

This slice intentionally stops after one recovered boundary.

Remaining compression, if future repository evidence selects it, includes whether the single `_ArchitecturalOrientationAnswer` should later be decomposed into separate private payloads for answer, reason, support, boundary, and limitations. That decomposition was not performed here because the selected boundary was only:

```text
Architectural Orientation Answer
    !=
Architectural Orientation Rendering
```

## Questions answered with implementation evidence

### 1. Where were architectural orientation answer composition and rendering previously mixed?

They were mixed in `build_inquiry_orientation(...)`, where deterministic related-material selection and uncertainty/boundary handoff were constructed directly as the public rendering-facing `InquiryOrientationView` consumed by `format_inquiry_orientation(...)`.

### 2. Which recovered architectural boundary became more explicit?

```text
Architectural Orientation Answer
    !=
Architectural Orientation Rendering
```

The private `_ArchitecturalOrientationAnswer` now composes answer material before the unchanged public view/rendering handoff.

### 3. How does the implementation now better reflect the recovered inquiry architecture?

The implementation now has an implementation-local answer object shaped as:

```text
answer
reason
support
boundary
limitations
```

That object is composed from existing evidence before compatibility handoff, matching the recovered inquiry pattern without introducing a runtime surface.

### 4. Did any compatibility boundary change?

No.
