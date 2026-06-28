# Answer Composition Slice 001

## Selected architectural boundary

Answer Composition boundary selected for this slice:

```text
Answer != Reason
```

The implementation-local slice was made in `seed_runtime/operational_story.py` because Operational Story already composes a bounded inquiry answer while also carrying support material that explains why that answer was selected.

## Implementation evidence

Reviewed implementation evidence:

- `seed_runtime/operational_story.py` composes a current operational story from pressure, capability, privilege, correlation, impact, and investigation-path surfaces.
- `seed_runtime/reasoning_path_audit.py` exposes derivation evidence, intermediate conclusions, derived conclusions, consumers, story impact, unknowns, and read-only boundaries.
- `seed_runtime/selection_path_audit.py` exposes selected answer material, candidate sets, factors, non-selected candidates, evidence, outcome, unknowns, and read-only boundaries.
- `seed_runtime/reference_selection.py` already separates selected reference from selection rationale, alternatives, authority boundary, and limitations.
- `seed_runtime/inquiry_orientation.py` exposes related material, support / why related, uncertainty, and authority boundary.
- `seed_runtime/inquiry_artifacts.py` exposes artifact classifications with evidence and limitations.
- Answer-composition investigations identify Operational Story, Inquiry Orientation, Reasoning Path Audit, Selection Path Audit, and Reference Selection as bounded answer-responsible surfaces.

The strongest implementation compression was in Operational Story: the same builder constructed final answer fields and reason/support fields directly into one `OperationalStory` return object.

## Before

Before this slice, `build_operational_story` directly assembled both bounded answer material and reason/support material into `OperationalStory` in one construction path:

- answer-like material: `focus`, `pressure`, `capabilities`, `constraints`, `correlation_gaps`, `impact`, `recent_changes`, `observed_outcomes`, `unknowns`;
- reason/support material: `supporting_evidence`, `investigation_path`.

The public object and rendered / JSON behavior were already correct, but implementation ownership compressed answer payload and reasoning payload in one return construction.

## After

`seed_runtime/operational_story.py` now has two implementation-local payloads:

```text
_OperationalStoryAnswerPayload
_OperationalStoryReasoningPayload
```

`_compose_operational_story_payloads(...)` returns both payloads, and `build_operational_story(...)` performs an explicit compatibility handoff into the unchanged public `OperationalStory` object.

## Boundary made explicit

The recovered boundary is private and implementation-local:

```text
bounded operational story answer material
```

is not the same implementation responsibility as:

```text
support material explaining the operational story answer
```

This makes `Answer != Reason` directly observable inside implementation without changing rendering, JSON, CLI, schema, event behavior, ledger behavior, or vocabulary.

## Compatibility preserved

No compatibility boundary changed.

The public `OperationalStory` dataclass remains the public compatibility object. `operational_story_json(...)` still serializes the same fields. `format_operational_story(...)` still renders the same sections. The CLI and diagnostic inventory / shape-audit contract are unchanged.

## Files changed

- `seed_runtime/operational_story.py`
- `tests/test_operational_story.py`
- `answer_composition_slice_001.md`

## LOC changed

Implementation/test diff before this report:

```text
seed_runtime/operational_story.py | 107 +++++++++++++++++++++++++++++++-------
tests/test_operational_story.py   |  64 +++++++++++++++++++++++
2 files changed, 151 insertions(+), 20 deletions(-)
```

## Tests executed

```text
pytest -q tests/test_operational_story.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

Result:

```text
50 passed in 8.94s
```

## Remaining compressed answer-composition boundaries

Remaining candidates were intentionally not changed in this slice:

- `InquiryOrientationView` still carries note, related material, uncertainty, and authority boundary in one public view object.
- `ReasoningPathAudit` still carries derivation evidence, conclusions, consumers, story impact, unknowns, and boundary in one audit object.
- `SelectionPathAudit` still carries selected answer, candidate set, selection factors, evidence, outcome, unknowns, and boundary in one audit object.
- `ReferenceSelection` already has visible selected-reference versus rationale separation, so it is less compressed than Operational Story.
- `InquiryArtifactVisibility` still carries classification, evidence, and limitations in one artifact visibility record.

These are possible future slices only if implementation evidence confirms a similarly compressed Answer Composition boundary. This slice stops after making exactly one recovered boundary explicit.
