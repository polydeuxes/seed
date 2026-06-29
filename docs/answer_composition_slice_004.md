# Answer Composition Slice 004

## selected architectural boundary

Boundary != Limitations

This slice selected the recovered Answer Composition boundary between authority constraints and communicated incompleteness or unavailable authority.

## implementation evidence

Reviewed implementation evidence around Operational Story composition, inquiry orientation, inquiry artifacts, bounded answer responsibility investigations, uncertainty investigations, answer limitation investigations, and existing answer payloads:

- `seed_runtime/operational_story.py` already exposed private implementation-local payloads for answer, reasoning, supporting evidence, and boundary before handoff into the unchanged public `OperationalStory` compatibility object.
- `OperationalStory` still carries both `unknowns` and `boundary` as public compatibility fields.
- `_compose_operational_story_payloads(...)` constructed `unknowns` and previously assigned them to `_OperationalStoryAnswerPayload` while separately constructing `_OperationalStoryBoundaryPayload`.
- `format_operational_story(...)` renders `Unknowns:` separately from `Boundary:`, proving the public surface already distinguished incompleteness from authority constraints.
- `seed_runtime/inquiry_artifacts.py` uses `limitations` on artifact visibility records while separately preserving a surface-level read-only boundary.
- Existing investigations characterize strong answer surfaces as preserving answer material, support, unknowns or limitations, and authority boundaries without treating those responsibilities as identical.

## before

Before this slice, Operational Story had a private `_OperationalStoryBoundaryPayload`, but limitation-like material remained compressed into `_OperationalStoryAnswerPayload` as `unknowns`.

That meant the implementation transition from boundary to limitations was visible only at the public `OperationalStory` field level and renderer level. Inside composition ownership, boundary construction was explicit, while limitations were still owned by answer payload construction.

Boundary and limitations were previously mixed by adjacency and asymmetric ownership in `_compose_operational_story_payloads(...)`: `boundary` had its own implementation-local payload, but `unknowns` were accumulated in the same construction path as bounded answer material and handed off as `answer_payload.unknowns`.

## after

This slice adds one private implementation-local payload:

```text
_OperationalStoryLimitationsPayload
```

`_compose_operational_story_payloads(...)` now returns five implementation-local payloads:

- `_OperationalStoryAnswerPayload`;
- `_OperationalStoryReasoningPayload`;
- `_OperationalStorySupportingEvidencePayload`;
- `_OperationalStoryBoundaryPayload`;
- `_OperationalStoryLimitationsPayload`.

`build_operational_story(...)` still performs the same compatibility handoff into the unchanged public `OperationalStory`, but now reads `unknowns` from `limitations_payload.unknowns` instead of `answer_payload.unknowns`.

## boundary made explicit

The recovered boundary made explicit is:

```text
Boundary
    !=
Limitations
```

Boundary remains responsible for answering:

```text
What conclusions are justified by this answer?
```

Limitations now have private implementation-local ownership for answering:

```text
What remains unknown, unsupported, or outside repository authority?
```

## compatibility preserved

No compatibility boundary changed.

The public `OperationalStory` dataclass remains unchanged. `operational_story_json(...)` still emits the same keys and values. `format_operational_story(...)` still renders the same text. There were no renderer changes, CLI changes, schema changes, JSON changes, event changes, ledger changes, presentation refactors, vocabulary migrations, boundary behavior changes, or limitation behavior changes.

## files changed

- `seed_runtime/operational_story.py`
- `tests/test_operational_story.py`
- `answer_composition_slice_004.md`

## LOC changed

Implementation and test diff before this report:

```text
seed_runtime/operational_story.py | 16 ++++++++++++----
tests/test_operational_story.py   |  7 +++++++
2 files changed, 19 insertions(+), 4 deletions(-)
```

This report was then added as the required deliverable.

## tests executed

```text
pytest -q tests/test_operational_story.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

Result:

```text
50 passed in 7.06s
```

## remaining compressed answer-composition boundaries

Remaining possible future Answer Composition compression points, subject to implementation evidence in future slices:

- `InquiryOrientationView` still carries note, related material, uncertainty, and authority boundary in one public view object.
- `InquiryArtifactVisibility` still carries classification, evidence, and limitations in one public artifact visibility record.
- `ReasoningPathAudit` still carries derivation evidence, conclusions, consumers, story impact, unknowns, and boundary in one audit object.
- `SelectionPathAudit` still carries selected answer, candidate set, selection factors, evidence, outcome, unknowns, and boundary in one audit object.

This slice stops after making exactly one recovered architectural boundary directly observable.

## questions answered with implementation evidence

1. Where were boundary and limitations previously mixed?

   They were mixed in Operational Story composition ownership: `_OperationalStoryBoundaryPayload` already owned authority boundary construction, but limitation-like `unknowns` were still built into `_OperationalStoryAnswerPayload` and handed off as `answer_payload.unknowns`.

2. Which recovered architectural boundary became more explicit?

   `Boundary != Limitations` became explicit through a new private `_OperationalStoryLimitationsPayload`, separate from `_OperationalStoryBoundaryPayload`.

3. How does the implementation now better reflect the recovered inquiry architecture?

   The implementation now gives authority constraints and incompleteness/unavailable-authority material separate implementation-local ownership before handoff into the unchanged public `OperationalStory`, matching the recovered inquiry distinction between bounded authority and communicated limitations.

4. Did any compatibility boundary change?

   No.
