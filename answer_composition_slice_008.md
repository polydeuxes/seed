# Answer Composition Slice 008

## selected inquiry surface

`ReasoningPathAudit`.

## selected recovered boundary

`Reason != Supporting Evidence`.

The selected slice separates implementation-local supporting evidence from derivation lineage before the unchanged public `ReasoningPathAudit` compatibility handoff.

## implementation evidence

- `ReasoningPathAudit` publicly exposes `evidence`, `intermediate_conclusions`, `derived_conclusions`, `consumers`, `story_impact`, `unknowns`, and the read-only boundary.
- `_DerivedConclusionPayload` already separates intermediate and derived conclusion material from lineage material.
- Before this slice, `_DerivationLineagePayload` owned `evidence`, `consumers`, `story_impact`, and `unknowns` together.
- `_reasoning_path_from_payloads(...)` is the local compatibility handoff into the unchanged public `ReasoningPathAudit` object.
- The projection navigation audit identified `ReasoningPathAudit` as partially projected and recommended moving `evidence` out of `_DerivationLineagePayload` while preserving public JSON and text behavior.

## before

`_DerivationLineagePayload` compressed supporting evidence with downstream lineage and limitation responsibilities:

```text
_DerivationLineagePayload
  evidence
  consumers
  story_impact
  unknowns
```

The compatibility handoff populated public `ReasoningPathAudit.evidence` from `lineage.evidence`.

## after

Supporting evidence has its own implementation-local payload:

```text
_DerivationSupportingEvidencePayload
  evidence

_DerivationLineagePayload
  consumers
  story_impact
  unknowns
```

The compatibility handoff now composes public `ReasoningPathAudit.evidence` from `supporting_evidence.evidence`, while retaining consumers, story impact, and unknowns from lineage.

## boundary made explicit

`Reason != Supporting Evidence` is explicit inside `ReasoningPathAudit` construction:

- reason/conclusion material remains in `_DerivedConclusionPayload`;
- supporting evidence is now owned by `_DerivationSupportingEvidencePayload`;
- downstream consumers, operational-story impact, and unknowns remain in `_DerivationLineagePayload` for future slices only if implementation evidence supports them.

## compatibility preserved

No.

No compatibility boundary changed. The public `ReasoningPathAudit` dataclass fields, `to_json_dict()` shape, formatter sections, CLI behavior, diagnostic inventory behavior, shape-audit behavior, event-ledger behavior, and cluster mutation boundary remain unchanged.

## files changed

- `seed_runtime/reasoning_path_audit.py`
- `tests/test_reasoning_path_audit.py`
- `answer_composition_slice_008.md`

## LOC changed

Implementation/test diff before this report:

```text
seed_runtime/reasoning_path_audit.py | 18 ++++++++++++++----
tests/test_reasoning_path_audit.py   | 34 ++++++++++++++++++++++++++++++++++
2 files changed, 48 insertions(+), 4 deletions(-)
```

## tests executed

```text
pytest -q tests/test_reasoning_path_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
51 passed in 18.76s
```

## remaining composition ownership inside ReasoningPathAudit

After this slice, `ReasoningPathAudit` still has implementation-local compression outside the selected boundary:

- `_DerivationLineagePayload` still owns consumers, story impact, and unknowns together.
- The public audit still carries boundary directly through the compatibility object default.
- No consumer, story-impact, unknowns, or boundary ownership transition was performed in this slice.

## remaining inquiry surfaces

No other inquiry surface was changed.

Previously completed local projection remains outside this slice for:

- `OperationalStory`
- `InquiryOrientationView`
- `SelectionPathAudit`

`ReasoningPathAudit` remains the only inquiry surface changed here, and only the supporting-evidence ownership transition was projected.
