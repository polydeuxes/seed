# Answer Composition Slice 002

## Selected architectural boundary

Answer Composition boundary selected for this slice:

```text
Reason != Supporting Evidence
```

The implementation-local slice was made in `seed_runtime/operational_story.py` because Operational Story already distinguished bounded answer material from reason/support material, and the next compressed responsibility was inside that reason/support material.

## Implementation evidence

Reviewed implementation evidence:

- `seed_runtime/operational_story.py` composes a current operational story from pressure, capability, privilege, correlation, impact, and investigation-path surfaces.
- `_OperationalStoryAnswerPayload` already separated answer material from support material after Slice 001.
- `_OperationalStoryReasoningPayload` still carried `supporting_evidence` together with `investigation_path`, compressing reason construction and supporting implementation evidence construction into one implementation-local payload.
- `build_operational_story(...)` still performs the compatibility handoff into the unchanged public `OperationalStory` object.
- `seed_runtime/reasoning_path_audit.py` distinguishes derivation evidence, conclusions, consumers, and story impact in one read-only audit surface.
- `seed_runtime/selection_path_audit.py` distinguishes selection factors from selected-pressure evidence in one read-only audit surface.
- `seed_runtime/reference_selection.py` already separates selected reference from selection rationale and alternative/reference authority evidence.
- `seed_runtime/inquiry_orientation.py` already exposes related material, support, why-related explanation, uncertainty, and authority boundary.
- `seed_runtime/inquiry_artifacts.py` exposes artifact classifications with implementation-backed evidence and limitations.

The implementation transition from reason to supporting implementation evidence was in Operational Story composition: investigation-path steps explain why the story has a route through implemented surfaces, while pressure reasons and pressure evidence are rendered as supporting evidence for that explanation.

## Before

Before this slice, Slice 001 had separated answer material from reason/support material, but the private reasoning payload still mixed two responsibilities:

```text
_OperationalStoryReasoningPayload
  supporting_evidence
  investigation_path
```

That meant the implementation-local reason payload owned both:

- reason material: `investigation_path`, which carries ordered implemented surfaces and the reasons those surfaces belong to the current investigation path;
- supporting implementation evidence material: `supporting_evidence`, which carries the primary pressure reason and implementation evidence key/value details.

Behavior was already correct, but the recovered architecture remained compressed inside one private payload.

## After

`seed_runtime/operational_story.py` now has a separate implementation-local supporting-evidence payload:

```text
_OperationalStoryReasoningPayload
  investigation_path

_OperationalStorySupportingEvidencePayload
  supporting_evidence
```

`_compose_operational_story_payloads(...)` now returns answer, reasoning, and supporting-evidence payloads. `build_operational_story(...)` performs the same compatibility handoff into the unchanged public `OperationalStory` object.

## Boundary made explicit

The recovered boundary is private and implementation-local:

```text
reason material explaining the story answer
```

is not the same implementation responsibility as:

```text
supporting implementation evidence for those reasons
```

This makes `Reason != Supporting Evidence` directly observable inside implementation without changing rendering, CLI, JSON, schemas, events, ledger behavior, presentation vocabulary, reasoning content, or evidence content.

## Compatibility preserved

No compatibility boundary changed.

The public `OperationalStory` dataclass remains unchanged. `operational_story_json(...)` still serializes the same fields. `format_operational_story(...)` still renders the same sections. CLI, diagnostic inventory, diagnostic shape-audit, event, ledger, schema, and JSON behavior are unchanged.

## Files changed

- `seed_runtime/operational_story.py`
- `tests/test_operational_story.py`
- `answer_composition_slice_002.md`

## LOC changed

Implementation/test diff before this report:

```text
seed_runtime/operational_story.py | 79 +++++++++++++++++++++++++--------------
tests/test_operational_story.py   | 41 ++++++++++++++++----
2 files changed, 84 insertions(+), 36 deletions(-)
```

## Tests executed

```text
pytest -q tests/test_operational_story.py
```

Result:

```text
6 passed in 8.97s
```

```text
pytest -q tests/test_operational_story.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

Result:

```text
50 passed in 8.73s
```

## Remaining compressed answer-composition boundaries

Remaining candidates were intentionally not changed in this slice:

- `InquiryOrientationView` still carries note, related material, uncertainty, support, why-related explanation, and authority boundary in one public view object.
- `ReasoningPathAudit` still carries evidence, conclusions, consumers, story impact, unknowns, and boundary in one audit object.
- `SelectionPathAudit` still carries selected answer, candidates, selection factors, selected evidence, outcome, unknowns, and boundary in one audit object.
- `InquiryArtifactVisibility` still carries classification, evidence, and limitations in one artifact visibility record.
- `ReferenceSelection` is less compressed because selected reference, selection rationale, alternatives, authority boundary, and limitations are already visibly separate, but future slices may still investigate whether any implementation ownership remains compressed.

This slice stops after making exactly one recovered boundary explicit.
