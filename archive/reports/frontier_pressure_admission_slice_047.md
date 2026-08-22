# Frontier Pressure Admission Slice 047

## Selected boundary

Recovered exactly one implementation-local ownership boundary: **diagnostic-shape audit repository-root compatibility selection inside `pressure_audit`**.

## Implementation evidence

Investigation began immediately adjacent to Slice 046 in `seed_runtime/pressure_audit.py`. Slice 046 recovered pressure-audit item-section human-readable formatting through `_format_pressure_item_section(index, item)`, while `format_pressure_audit(audit)` continues to own whole-report assembly and summary behavior.

The pressure-audit formatting neighborhood is exhausted for this campaign: `_display_evidence(value)` already dispatches to the previously recovered mapping, collection, and scalar display helpers, and `_format_pressure_item_section(index, item)` owns one item section. Further display movement would be layout cleanup rather than a new implementation-local ownership boundary.

The next adjacent implementation evidence is `_diagnostic_shape_pressure(root)`. That producer still compressed diagnostic-shape pressure candidate construction with a repository-root compatibility selection:

- it decided whether the supplied root looked like the runnable repository root by checking for `scripts/seed_local.py`;
- it passed the accepted root or `None` to `build_diagnostic_shape_audit(repo_root=...)`;
- it summarized diagnostic-shape rows, scored pressure, refused zero-score output, and built the `Diagnostic Shape` pressure candidate.

The selected boundary is the compatibility-preserving root selection for the diagnostic-shape audit input. This is implementation-local, directly observable, and materially consumed by `_diagnostic_shape_pressure(root)`. It does not change pressure scoring, candidate admission, JSON output, human-readable output, diagnostic behavior, recording behavior, or mutation boundaries.

## Before

`_diagnostic_shape_pressure(root)` owned repository-root compatibility selection inline:

```python
shape_root = root if (root / "scripts" / "seed_local.py").exists() else None
```

That same function also executed and summarized the diagnostic-shape audit, computed score, refused non-positive pressure, assembled evidence through the existing `_diagnostic_shape_pressure_evidence(summary)` helper, and constructed the `_PressureItemCandidate`.

## After

`_diagnostic_shape_pressure(root)` still owns diagnostic-shape audit execution, summary scoring, zero-score refusal, reason text, recommended command, and candidate construction. It now delegates only the compatibility root selection to `_diagnostic_shape_audit_root(root)`.

`_diagnostic_shape_audit_root(root)` returns the root only when the runnable CLI marker `scripts/seed_local.py` exists; otherwise it returns `None`, preserving the previous fallback behavior exactly.

## Recovered producer

`_diagnostic_shape_audit_root(root)` owns diagnostic-shape audit repository-root compatibility selection.

## Recovered artifact/helper

Recovered helper:

```python
def _diagnostic_shape_audit_root(root: Path) -> Path | None:
    return root if (root / "scripts" / "seed_local.py").exists() else None
```

## Recovered consumer

`_diagnostic_shape_pressure(root)` consumes `_diagnostic_shape_audit_root(root)` as the `repo_root` argument source for `build_diagnostic_shape_audit(...)`.

## Compatibility preserved

No public compatibility, runtime behavior, CLI behavior, JSON output, human-readable output, diagnostic inventory, schema, event-ledger behavior, or read-only mutation boundary changed. The helper returns the same value that `_diagnostic_shape_pressure(root)` previously computed inline.

Expected compatibility answer:

```text
No.
```

## Files changed

- `seed_runtime/pressure_audit.py`
- `tests/test_pressure_audit.py`
- `frontier_pressure_admission_slice_047.md`

## LOC changed

Implementation and test diff before this report:

```text
seed_runtime/pressure_audit.py |  7 +++++--
tests/test_pressure_audit.py   | 13 +++++++++++++
2 files changed, 18 insertions(+), 2 deletions(-)
```

## Tests executed

- `python -m black seed_runtime/pressure_audit.py tests/test_pressure_audit.py` — passed; 2 files left unchanged.
- `pytest -q tests/test_pressure_audit.py` — passed; 17 tests.

## Required questions

1. **What responsibility was previously compressed?**

   Diagnostic-shape audit repository-root compatibility selection was compressed inside `_diagnostic_shape_pressure(root)` alongside audit execution, summary scoring, zero-score refusal, evidence consumption, reason text, recommended command, and pressure-candidate construction.

2. **Which implementation-local ownership boundary became directly observable?**

   The boundary between diagnostic-shape pressure candidate production and the compatibility decision for which repository root should be passed to `build_diagnostic_shape_audit(...)` became directly observable.

3. **What producer now owns the recovered responsibility?**

   `_diagnostic_shape_audit_root(root)` owns the recovered compatibility-selection responsibility.

4. **What artifact or helper carries the recovered boundary, if any?**

   `_diagnostic_shape_audit_root(root)` carries the boundary by returning `Path | None` for the diagnostic-shape audit `repo_root` argument.

5. **Who consumes it?**

   `_diagnostic_shape_pressure(root)` consumes the helper result when it calls `build_diagnostic_shape_audit(repo_root=...)`.

6. **Did any compatibility boundary change?**

   No.

7. **How does this respect the Slice 035 `selection_path_audit` stop marker?**

   This slice does not inspect, modify, or rely on `selection_path_audit`. It remains in `seed_runtime/pressure_audit.py`, outside the exhausted Slice 035 neighborhood, and no compatibility-preserving selection-path call-site update was required.

8. **How is this distinct from the recent upstream pressure-audit recoveries, especially Slice 036 through Slice 046?**

   - Slice 036 recovered pressure candidate admission/filtering/conversion/ordering; this slice does not touch `_admitted_pressure_items(...)`.
   - Slice 037 recovered consumer-predicate pressure source admission; this slice does not collect or fan out consumer audits.
   - Slices 038 through 042 recovered pressure evidence payload ownership for diagnostic-shape, ownership, capability, orphaned-predicate, and fragile-predicate candidates; this slice does not assemble pressure evidence.
   - Slices 043 through 045 recovered mapping, collection, and scalar evidence display formatting; this slice does not format evidence values.
   - Slice 046 recovered one pressure item-section formatter; this slice stops the display neighborhood and moves to the adjacent diagnostic-shape producer only because implementation evidence shows a real compatibility root-selection responsibility.

## Remaining compressed responsibilities

Remaining compression, if any, should continue to be selected only from implementation evidence. After this slice, `_diagnostic_shape_pressure(root)` still owns diagnostic-shape audit execution, summary scoring, zero-score refusal, reason text, recommended command, and candidate construction. `_diagnostic_shape_pressure_evidence(summary)` owns diagnostic-shape evidence payload projection, and `_diagnostic_shape_audit_root(root)` owns only compatibility root selection. No feature admission, acceptance, action, mutation, planning, prioritization, readiness evaluation, inquiry generation, route authority, scheduler, ontology, registry, or framework was introduced.

## Slice 035 stop-marker compliance

The exhausted `selection_path_audit` neighborhood remains closed. The selected boundary is in the adjacent `pressure_audit` producer path and does not change any selection-path implementation or tests.

## Distinction from recent upstream pressure-audit slices

This slice recovers a compatibility-input producer for the diagnostic-shape pressure source. It is not a re-slice of candidate admission, consumer-predicate source fan-out, evidence payload ownership, evidence display formatting, or pressure item-section formatting. The implementation evidence is the existing `scripts/seed_local.py` repository-root guard that was already present inline and is now owned by one local helper.
