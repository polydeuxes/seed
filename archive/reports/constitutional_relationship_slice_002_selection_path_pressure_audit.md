# Constitutional Relationship Slice 002 Implementation Pressure Audit

Repository authority wins.

## Scope

This is one bounded Implementation Pressure Audit for the preserved boundary:

```text
A competent local producer preserves
a bounded constitutional profile.

A bounded downstream consumer uses
only that preserved profile
within its local role.
```

No implementation was modified. This audit does not recover another constitutional characterization, introduce an artifact framework, introduce a universal profile type, invent a producer or consumer, infer implementation from constitutional prose, or recommend architectural redesign.

## Inspected implementation

Implementation inspection began adjacent to warrant, reliance, inquiry-artifact, diagnostic, answer-composition, and typed-unknown surfaces, then stopped at the first implementation-local manifestation with sufficient producer/artifact/consumer evidence.

Inspected evidence:

- `seed_runtime/inquiry_artifacts.py`
  - `InquiryArtifactVisibility` preserves artifact identity, classification, evidence, and limitations.
  - `_InquiryArtifactEvidencePayload` and `_InquiryArtifactLimitationsPayload` preserve support and limits before `_artifact_visibility_from_payloads(...)` composes the public visibility object.
  - This is relevant, but the evidence/limitations split is already locally named and tested as compatibility handoff.
- `seed_runtime/typed_unknowns.py`
  - `TypedUnknownRecord` preserves `unknown_type`, `area`, and `reason`, then projects to the existing public unknown shape with `area` and `reason` only.
  - This is relevant, but it is a typed Unknown preservation boundary rather than the strongest adjacent producer/profile/consumer compression for this audit.
- `seed_runtime/diagnostic_inventory.py`
  - `DiagnosticInventoryEntry` preserves diagnostic identity, CLI flags, state/repo-file consumption, JSON/record support, record scope, diagnostic/cluster fact emission, event-ledger behavior, mutation boundary, diagnostic-fact reads, and description.
  - `_produce_known_diagnostic_surface_definition(...)` constructs a known diagnostic-surface definition from entry-local boundary, consumption, and shape-registration identifications.
  - `_DiagnosticSurfaceConsumptionIdentification` carries a bounded consumption profile and `_prepare_diagnostic_surface_consumption_text(...)` consumes only its `declared_consumption` mapping for rendering.
  - This is relevant, but recent implementation already decomposes several local declaration/extraction/rendering responsibilities in this file.
- `seed_runtime/reasoning_path_audit.py`
  - `_DerivedConclusionPayload`, `_DerivationSupportingEvidencePayload`, and `_DerivationLineagePayload` separately carry derived conclusions, support, consumers/story impact, and typed Unknowns before public `ReasoningPathAudit` composition.
  - This is relevant, but the producer/consumer boundary is broader and less immediately bounded than the selection-path manifestation below.
- `seed_runtime/selection_path_audit.py`
  - The implementation constructs a selection result from local pressure/focus evidence, candidate sets, non-selected alternatives, support, outcome, and typed Unknowns.
  - `_SelectionPathPayloads` is a bounded profile artifact carrying only the fields consumed by the public audit constructor path.
  - `_selection_path_from_payload_bundle(...)` is an exact downstream consumer that uses the payload bundle to construct `SelectionPathAudit` without assuming authority outside that bundle.

## Candidate producer

The candidate producer is `_pressure_selection_payloads(...)` in `seed_runtime/selection_path_audit.py`.

It currently constructs the bounded local profile by combining:

- selected result from `_pressure_selection_result_payload(selected)`;
- outcome/reason profile from `_pressure_selection_reason_payload(selected, focus)`;
- supporting evidence from `_pressure_selection_supporting_evidence_payload(selected_item)`;
- lineage from `_pressure_selection_lineage_payload(pressures, selected_item, unknowns)`;
- Unknown preservation through `_selection_unknowns_from_pressures(pressures)` and the typed Unknown path.

Adjacent producers also construct the same artifact for other local cases:

- `_selection_path_from_payloads(...)` constructs `_SelectionPathPayloads` for unsupported targets from separate result, reason, support, and lineage payloads.
- `_from_pressure_selection(...)`, `_from_pressure_category_selection(...)`, and `_from_focus_selection(...)` route implemented target cases into the pressure-selection payload path.

For this audit, `_pressure_selection_payloads(...)` is the strongest candidate because it is the exact local producer that preserves selected identity, evidence/support, lineage, non-selected alternatives, outcome, and Unknowns for an implemented selection path.

## Candidate artifact

The candidate artifact is `_SelectionPathPayloads` in `seed_runtime/selection_path_audit.py`.

It carries a bounded profile made from:

- `_SelectionResultPayload`: selected identity;
- `_SelectionReasonPayload`: outcome/reason fields;
- `_SelectionSupportingEvidencePayload`: supporting evidence;
- `_SelectionLineagePayload`: candidate set, selection factors, non-selected alternatives, and Unknowns;
- `_SelectionUnknownPayload`: typed Unknown records before public projection.

The artifact does not carry universal authority, diagnostic registration authority, event-ledger authority, cluster mutation authority, selection-framework authority, or constitutional characterization authority. It is implementation-local and exists only to feed the current selection-path audit composition.

## Candidate consumer

The candidate consumer is `_selection_path_from_payload_bundle(...)` in `seed_runtime/selection_path_audit.py`.

It consumes only the bounded `_SelectionPathPayloads` profile and constructs `SelectionPathAudit` by projecting:

- `payloads.result.selected` into `selected`;
- `payloads.lineage.candidate_set.candidates` into `candidates`;
- `payloads.lineage.factors.selection_factors` into `selection_factors`;
- `payloads.lineage.non_selected.non_selected` into `non_selected`;
- `payloads.support.evidence` into `evidence`;
- `payloads.reason.outcome` into `outcome`;
- `payloads.lineage.unknowns.unknowns` through `typed_unknowns_to_public_dicts(...)` into public Unknown dictionaries.

The public `SelectionPathAudit` then preserves the read-only compatibility boundary with `records_facts=False`, `writes_event_ledger=False`, and `mutates_cluster=False`.

## Compressed responsibility

The compressed responsibility is:

```text
selection-path profile preservation
```

More precisely, the implementation currently compresses the responsibility for preserving a bounded selection-profile handoff between local selection evidence construction and public audit composition.

That profile includes:

- selected subject/identity;
- supporting evidence;
- provenance-like lineage through candidate set, factors, non-selected alternatives, and pressure-derived source material;
- negative authority through non-selected alternatives;
- Unknowns through typed Unknown records;
- stop/non-promotion limits through unsupported-target handling and the read-only/no-record/no-ledger/no-mutation audit boundary.

The compressed responsibility is not selection itself, ranking itself, pressure audit ownership, operational-story ownership, diagnostic inventory registration, typed Unknown semantics, CLI formatting, JSON formatting, event recording, or cluster mutation. It is only the local preservation of the bounded profile that the downstream audit constructor consumes.

## Compatibility boundary

A behavior-preserving slice, if later requested, would need to preserve all current public behavior:

- `build_selection_path_audit(...)` returns the same `SelectionPathAudit` values for implemented focus/pressure targets and unsupported targets.
- `selection_path_audit_json(...)` remains the same public JSON shape.
- `format_selection_path_audit(...)` remains the same human-readable output shape.
- Unknowns remain projected through `typed_unknowns_to_public_dicts(...)` and do not expose `unknown_type` in the public compatibility shape unless a separate task changes that boundary.
- The audit remains read-only: no fact recording, no event-ledger writes, and no cluster mutation.
- No universal profile type, artifact framework, or constitutional model is introduced.

## Required questions

### 1. Does an implementation-local manifestation exist?

Yes.

The recurring local shape exists in `seed_runtime/selection_path_audit.py`:

```text
_pressure_selection_payloads(...)
→ _SelectionPathPayloads
→ _selection_path_from_payload_bundle(...)
```

### 2. What responsibility is compressed?

The compressed responsibility is bounded selection-path profile preservation between local selection evidence construction and public audit composition.

### 3. What exact producer currently constructs or preserves the profile?

The exact primary producer is `_pressure_selection_payloads(...)`.

It constructs `_SelectionPathPayloads` from selected identity, outcome/reason, supporting evidence, lineage, and typed Unknowns.

### 4. What artifact carries it?

The artifact is `_SelectionPathPayloads`.

It carries `_SelectionResultPayload`, `_SelectionReasonPayload`, `_SelectionSupportingEvidencePayload`, and `_SelectionLineagePayload`.

### 5. What exact consumer consumes it?

The exact consumer is `_selection_path_from_payload_bundle(...)`.

It consumes `_SelectionPathPayloads` to construct `SelectionPathAudit`.

### 6. Is the boundary ready for one behavior-preserving implementation slice?

Ready for implementation slice

## Readiness classification

Ready for implementation slice

## Preserved Unknowns

- It is Unknown whether an implementation slice is desirable now; this audit only classifies readiness.
- It is Unknown whether the repository wants a named local helper for selection-path profile preservation; no implementation was changed.
- It is Unknown whether the same producer/profile/consumer pressure should later be audited in `reasoning_path_audit.py` or `inquiry_artifacts.py`; this audit stopped at one bounded manifestation.
- It is Unknown whether a future slice should preserve the profile by renaming, extracting, or only testing the current boundary; this audit does not prescribe a design.

## Confidence

Confidence: high.

Reason: the candidate is implementation-local, has exact producer/artifact/consumer names, carries fields matching the requested subject/evidence/provenance/negative-authority/Unknown/stop-boundary pattern, and already preserves a read-only/no-record/no-ledger/no-mutation public audit boundary. The confidence is not absolute because no behavior-preserving implementation slice was performed and no runtime output comparison was required by this audit.

Implementation pressure audit complete.
