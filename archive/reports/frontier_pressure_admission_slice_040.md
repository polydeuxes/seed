# Frontier Pressure Admission Slice 040

## Selected boundary

Capability pressure evidence payload ownership.

## Implementation evidence

Investigation began in `seed_runtime/pressure_audit.py` immediately adjacent to the Slice 039 ownership-discrepancy pressure area. The ownership evidence aggregation boundary was already separated as `_ownership_pressure_evidence(rows)`, and the next implementation-local pressure producer, `_capability_pressure(state)`, still owned multiple responsibilities inline:

- selecting capability-need entries from `build_capability_needs(state)`;
- scoring zero-or-more capability pressure from subject occurrence counts;
- refusing zero-score pressure;
- selecting the top capability need for the reason text;
- assembling the capability evidence payload fields;
- constructing the `_PressureItemCandidate`.

The still-compressed responsibility supported by implementation evidence was the capability pressure evidence payload assembly: `capability need frequency`, `affected subjects`, and `affected diagnostics` were built inline inside `_capability_pressure(...)` even though the producer also owned scoring, refusal, reason construction, and candidate construction.

## Before

`_capability_pressure(state)` built the public capability pressure evidence dictionary inline while also selecting entries, calculating score, refusing zero-score output, choosing the top need for the reason, and constructing the pressure candidate.

## After

`_capability_pressure(state)` still owns entry selection, scoring, zero-score refusal, top-need selection, reason text, recommended command, and candidate construction. Capability evidence payload assembly is now owned by `_capability_pressure_evidence(entries)`, which returns the same payload shape as before.

## Required questions

1. **What responsibility was previously compressed?**

   Capability pressure evidence payload assembly was compressed inside `_capability_pressure(state)` alongside scoring, refusal, reason text, and candidate construction.

2. **Which implementation-local ownership boundary became directly observable?**

   The boundary between capability pressure candidate construction and capability evidence payload assembly became directly observable.

3. **What implementation and/or test change made the boundary observable?**

   The implementation added `_capability_pressure_evidence(entries)` and changed `_capability_pressure(state)` to consume it. The tests added `test_capability_pressure_evidence_is_owned_by_local_helper()` to exercise the helper directly.

4. **What producer now owns the recovered responsibility?**

   `_capability_pressure_evidence(entries)` owns capability evidence payload assembly.

5. **What artifact or helper carries the recovered boundary, if any?**

   `_capability_pressure_evidence(entries)` carries the recovered boundary.

6. **Who consumes it?**

   `_capability_pressure(state)` consumes it while constructing the `Capability` `_PressureItemCandidate`.

7. **Did any compatibility boundary change?**

   No.

8. **How does this respect the Slice 035 `selection_path_audit` stop marker?**

   This slice did not inspect, modify, or rely on `selection_path_audit`. It stays in `seed_runtime/pressure_audit.py`, outside the exhausted Slice 035 neighborhood.

9. **How is this distinct from Slice 036 pressure candidate admission?**

   Slice 036 recovered admission/filtering/conversion/ordering of candidate pressure items. This slice does not change admission and does not touch `_admitted_pressure_items(...)`; it only separates the capability evidence payload producer consumed before admission.

10. **How is this distinct from Slice 037 consumer-predicate pressure source admission?**

   Slice 037 recovered collecting consumer-predicate pressure candidates from a single consumer audit. This slice does not collect consumer-predicate sources and does not touch `_consumer_predicate_pressures(root)`; it separates capability evidence payload assembly from the capability pressure producer.

11. **How is this distinct from Slice 038 diagnostic-shape pressure evidence payload ownership?**

   Slice 038 recovered diagnostic-shape evidence payload ownership for diagnostic-shape audit summaries. This slice recovers the analogous but separate capability pressure evidence payload sourced from capability-need entries, not diagnostic-shape summaries.

12. **How is this distinct from Slice 039 ownership-discrepancy pressure evidence aggregation?**

   Slice 039 recovered ownership-discrepancy evidence aggregation for ownership discrepancy rows. This slice leaves `_ownership_pressure(...)` and `_ownership_pressure_evidence(rows)` unchanged and recovers the adjacent capability evidence payload boundary.

## Implementation files changed

- `seed_runtime/pressure_audit.py`

## Test files changed

- `tests/test_pressure_audit.py`

## Recovered producer

- `_capability_pressure_evidence(entries)`

## Recovered artifact/helper

- `_capability_pressure_evidence(entries)`

## Recovered consumer

- `_capability_pressure(state)`

## Compatibility preserved

No public compatibility, runtime behavior, CLI behavior, JSON output, human-readable output, diagnostic inventory, schema, event-ledger behavior, or read-only mutation boundary changed. The helper returns the same evidence dictionary that `_capability_pressure(state)` previously constructed inline.

Expected compatibility answer:

```text
No.
```

## LOC changed

- `seed_runtime/pressure_audit.py`: 18 inserted lines, 12 removed lines.
- `tests/test_pressure_audit.py`: 29 inserted lines.
- `frontier_pressure_admission_slice_040.md`: 144 inserted lines.

## Tests executed

```text
pytest -q tests/test_pressure_audit.py
```

Result: `10 passed`.

## Remaining compressed responsibilities

Remaining compression, if any, should be selected only from future implementation evidence. In the immediate pressure-audit area, capability pressure still owns entry selection, score computation, zero-score refusal, top-need reason selection, reason text, recommended command, and candidate construction. This slice does not claim those as recovered boundaries.

## Slice 035 stop marker

The slice respects the Slice 035 stop marker by avoiding the exhausted `selection_path_audit` neighborhood entirely. No compatibility-preserving call-site update in that neighborhood was required.

## Avoiding re-slice of Slice 036

The slice avoids re-slicing pressure candidate admission because `_admitted_pressure_items(...)` is unchanged and remains the owner of candidate filtering, conversion, and ordering.

## Avoiding re-slice of Slice 037

The slice avoids re-slicing consumer-predicate pressure source admission because `_consumer_predicate_pressures(root)`, `_orphaned_predicate_pressure(audit)`, and `_fragile_predicate_pressure(audit)` are unchanged.

## Avoiding re-slice of Slice 038

The slice avoids re-slicing diagnostic-shape pressure evidence payload ownership because `_diagnostic_shape_pressure_evidence(summary)` is unchanged and diagnostic-shape evidence remains owned there.

## Avoiding re-slice of Slice 039

The slice avoids re-slicing ownership-discrepancy pressure evidence aggregation because `_ownership_pressure_evidence(rows)` is unchanged and ownership row selection, scoring, refusal, and candidate construction remain in `_ownership_pressure(state)`.
