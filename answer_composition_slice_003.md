# Answer Composition Slice 003

## selected architectural boundary

Supporting Evidence != Boundary

This slice selected the recovered Answer Composition boundary between implementation-backed support for a bounded answer and the authority limits on conclusions drawn from that support.

## implementation evidence

Reviewed implementation evidence around Operational Story composition, inquiry orientation, inquiry artifacts, and the prior Answer Composition slices:

- `seed_runtime/operational_story.py` already exposed private implementation-local payloads for answer, reasoning, and supporting evidence before handoff into the unchanged public `OperationalStory` compatibility object.
- `OperationalStory` carries both `supporting_evidence` and `boundary` as public compatibility fields.
- `_compose_operational_story_payloads(...)` constructed supporting evidence as a private payload, but the authority boundary remained inline in `build_operational_story(...)` during compatibility handoff.
- `seed_runtime/inquiry_orientation.py` keeps related material/support and `authority_boundary` on one public view object, while rendering them as separate sections.
- `seed_runtime/inquiry_artifacts.py` keeps artifact evidence and limitations on one public artifact visibility record, while preserving a separate surface-level read-only boundary.
- Prior Answer Composition slices established that public behavior stays compatible while implementation-local ownership can be separated before the public `OperationalStory` handoff.

## before

Before this slice, Operational Story had implementation-local payloads for:

- bounded answer material;
- reasoning material;
- supporting-evidence material.

However, the authority boundary was still constructed inline in `build_operational_story(...)` at the same compatibility handoff where `supporting_evidence_payload.supporting_evidence` was assigned into `OperationalStory`.

That meant the transition from supporting evidence to authority boundary was observable in public fields but not as a separate implementation-local ownership object. Supporting evidence construction had a private payload; authority boundary construction did not.

## after

This slice adds one private implementation-local payload:

```text
_OperationalStoryBoundaryPayload
```

`_compose_operational_story_payloads(...)` now returns four implementation-local payloads:

- `_OperationalStoryAnswerPayload`;
- `_OperationalStoryReasoningPayload`;
- `_OperationalStorySupportingEvidencePayload`;
- `_OperationalStoryBoundaryPayload`.

`build_operational_story(...)` still performs the same compatibility handoff into the unchanged public `OperationalStory`, but now reads the boundary from `boundary_payload.boundary` instead of constructing it inline.

## boundary made explicit

The recovered boundary made explicit is:

```text
implementation evidence supporting the story answer
    !=
authority limits on what the story may conclude
```

Supporting evidence remains responsible for answering:

```text
What implementation-backed authority supports this answer?
```

Boundary now has private implementation-local ownership for answering:

```text
What conclusions are explicitly outside that authority?
```

## compatibility preserved

No compatibility boundary changed.

The public `OperationalStory` dataclass remains unchanged. `operational_story_json(...)` still emits the same keys and values. `format_operational_story(...)` still renders the same text. There were no renderer changes, CLI changes, schema changes, JSON changes, event changes, ledger changes, presentation refactors, vocabulary migrations, boundary behavior changes, or evidence behavior changes.

## files changed

- `seed_runtime/operational_story.py`
- `tests/test_operational_story.py`
- `answer_composition_slice_003.md`

## LOC changed

Implementation and test diff before this report:

```text
seed_runtime/operational_story.py | 34 +++++++++++++++++++++++++---------
tests/test_operational_story.py   |  6 ++++++
2 files changed, 31 insertions(+), 9 deletions(-)
```

This report was then added as the required deliverable.

## tests executed

```text
pytest -q tests/test_operational_story.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

Result:

```text
50 passed in 8.60s
```

## remaining compressed answer-composition boundaries

Remaining possible future Answer Composition compression points, subject to implementation evidence in future slices:

- `InquiryOrientationView` still carries note, related material, uncertainty, and authority boundary in one public view object.
- `InquiryArtifactVisibility` still carries classification, evidence, and limitations in one public artifact visibility record.
- `ReasoningPathAudit` still carries derivation evidence, conclusions, consumers, story impact, unknowns, and boundary in one audit object.
- `SelectionPathAudit` still carries selected answer, candidate set, selection factors, evidence, outcome, unknowns, and boundary in one audit object.

This slice stops after making exactly one recovered architectural boundary directly observable.

## questions answered with implementation evidence

1. Where were supporting evidence and authority boundary previously mixed?

   They were mixed at the Operational Story compatibility handoff in `build_operational_story(...)`: supporting evidence already came from `_OperationalStorySupportingEvidencePayload`, while the authority boundary was still constructed inline in the `OperationalStory(...)` return object.

2. Which recovered architectural boundary became more explicit?

   `Supporting Evidence != Boundary` became explicit through a new private `_OperationalStoryBoundaryPayload`, separate from `_OperationalStorySupportingEvidencePayload`.

3. How does the implementation now better reflect the recovered inquiry architecture?

   The implementation now gives supporting evidence and authority boundary separate implementation-local ownership before handoff into the unchanged public `OperationalStory`, matching the recovered inquiry distinction between authority support and authority limits.

4. Did any compatibility boundary change?

   No.
