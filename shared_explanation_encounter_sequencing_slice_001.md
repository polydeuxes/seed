# Shared Explanation Encounter Sequencing Slice 001

This slice adds the bounded read-only responsibility:

```text
SharedExplanationPresentationAdmission
+
explicit presentation-local sequencing evidence
→ SharedExplanationEncounterSequencing
```

The implementation preserves constitutional derivation order separately from operator encounter order. It only consumes admitted projections plus explicit presentation-local sequencing evidence. It does not reopen membership or admission, infer order from tuple position, timestamps, IDs, severity, or stage order, rank constitutional stages or blockers, deduplicate, compose a final view, authorize, execute, write events, or mutate cluster state.

## Implementation

- `seed_runtime/shared_explanation_encounter_sequencing.py` defines `PresentationLocalSequencingEvidence` and `SharedExplanationEncounterSequencing`.
- `sequence_shared_explanation_encounters(...)` preserves `constitutional_derivation_projection_refs` from the admission artifact while producing separate `encounter_sequence_projection_refs` from explicit `encounter_order` evidence.
- Optional roles are limited to supported labels and are emitted only when supplied by evidence.
- Unknowns, conflicts, duplicates, non-members, belonging-but-unadmitted projections, and admitted-but-unsequenced projections remain visible.
- The artifact is read-only and reports `writes_event_ledger=false` and `mutates_cluster=false`.

## Tests

Focused tests in `tests/test_shared_explanation_encounter_sequencing.py` prove:

- admitted projections can be reordered for operator comprehension while source identity and lineage remain intact;
- constitutional derivation order is not overwritten by encounter order;
- no composed view or constitutional rank is produced;
- non-admitted evidence is ignored rather than used to reopen admission;
- unknowns, conflicts, duplicates, and unsequenced admitted projections remain visible;
- optional roles are not invented and unsupported roles are refused;
- JSON and text output preserve the read-only, non-mutating boundary.
