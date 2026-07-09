# Frontier Pressure Admission Slice 037

## Selected boundary

Recovered implementation-local ownership boundary: **consumer-predicate pressure source admission inside `pressure_audit`**.

This slice begins one implementation hop upstream from Slice 036's `_admitted_pressure_items(...)` boundary. The adjacent implementation evidence in `build_pressure_audit(...)` showed that pressure candidate admission was separated, but the two consumer-audit-derived pressure producers still each collected their own `build_consumer_audit(root)` source before producing orphaned-predicate and fragile-predicate candidates. The still-compressed responsibility was the local source handoff that admits the consumer audit once and fans it out to the two predicate-pressure candidate producers.

## Implementation evidence

- `build_pressure_audit(...)` constructs the public `PressureAudit` only after `_admitted_pressure_items(...)` receives candidate producers.
- Before this slice, consumer-predicate candidate production was adjacent to admission but compressed: `_orphaned_predicate_pressure(root)` and `_fragile_predicate_pressure(root)` each accepted `root` and independently called `build_consumer_audit(root)`.
- The candidate-specific helpers already owned their individual row filters and candidate payloads; the missing local boundary was the source admission/fan-out for consumer-predicate pressure candidates.

## Before

`build_pressure_audit(...)` passed `_orphaned_predicate_pressure(root)` and `_fragile_predicate_pressure(root)` directly to `_admitted_pressure_items(...)`. Each helper collected `build_consumer_audit(root)` independently before filtering observation predicates. The consumer audit source handoff was therefore not directly observable as an implementation-local producer.

## After

`build_pressure_audit(...)` now passes `*_consumer_predicate_pressures(root)` into `_admitted_pressure_items(...)`. `_consumer_predicate_pressures(root)` owns the single consumer-audit source collection and returns the orphaned-predicate and fragile-predicate candidate slots. `_orphaned_predicate_pressure(...)` and `_fragile_predicate_pressure(...)` now consume an already-collected `ConsumerAudit` and continue to own only their category-specific candidate filters and payloads.

## Implementation files changed

- `seed_runtime/pressure_audit.py`

## Test files changed

- `tests/test_pressure_audit.py`

## Recovered producer

`_consumer_predicate_pressures(root)` is the recovered producer. It collects the consumer audit once and produces the two consumer-predicate pressure candidate slots that are adjacent to pressure candidate admission.

## Recovered artifact/helper

`_consumer_predicate_pressures(root) -> tuple[_PressureItemCandidate | None, _PressureItemCandidate | None]` carries the recovered boundary.

## Recovered consumer

`build_pressure_audit(...)` consumes the helper output by expanding it into `_admitted_pressure_items(...)`, which continues to own filtering absent/non-positive candidates, converting admitted candidates, and score/category ordering.

## Compatibility preserved

No compatibility boundary changed.

- Public API shape is unchanged.
- CLI behavior is unchanged.
- JSON output is unchanged.
- Human-readable output is unchanged.
- Diagnostic inventory/shape behavior is unchanged.
- Event-ledger and cluster mutation behavior are unchanged; the pressure audit remains read-only.

Expected compatibility answer: `No.`

## LOC changed

Before adding this report, implementation/test diff was:

```text
seed_runtime/pressure_audit.py | 27 ++++++++++++++++++++-------
tests/test_pressure_audit.py   | 41 +++++++++++++++++++++++++++++++++++++++++
2 files changed, 61 insertions(+), 7 deletions(-)
```

## Tests executed

- `python -m black seed_runtime/pressure_audit.py tests/test_pressure_audit.py` — passed.
- `pytest -q tests/test_pressure_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py` — passed, 111 tests.

## Required questions

1. **What responsibility was previously compressed?**

   The consumer-audit source handoff for predicate-derived pressure candidates was compressed into the two predicate pressure helpers, each of which collected the consumer audit source independently before category-specific filtering.

2. **Which implementation-local ownership boundary became directly observable?**

   The boundary where `pressure_audit` admits one consumer audit source and fans it out into orphaned-predicate and fragile-predicate pressure candidate slots is now directly observable.

3. **What implementation and/or test change made the boundary observable?**

   Implementation now routes consumer-predicate candidate production through `_consumer_predicate_pressures(root)`. The new unit test proves the helper calls `build_consumer_audit(root)` once and returns the expected orphaned and fragile predicate candidate evidence from that single audit.

4. **What producer now owns the recovered responsibility?**

   `_consumer_predicate_pressures(root)` owns consumer-audit source collection for predicate pressure candidate production.

5. **What artifact or helper carries the recovered boundary, if any?**

   `_consumer_predicate_pressures(root)` carries the boundary.

6. **Who consumes it?**

   `build_pressure_audit(...)` consumes it by expanding the returned candidate slots into `_admitted_pressure_items(...)`.

7. **Did any compatibility boundary change?**

   No.

8. **How does this respect the Slice 035 `selection_path_audit` stop marker?**

   This slice does not touch `selection_path_audit`, selection-path route ordering, selection-path payloads, selected pressure evidence records, candidate rows, ranking, selected-name projection, target matching, unsupported-target helpers, or generic presentation formatting. The recovered boundary is in `pressure_audit`, one implementation hop upstream from the Slice 036 pressure admission boundary.

9. **How is this distinct from Slice 036 pressure candidate admission?**

   Slice 036 separated `_admitted_pressure_items(...)`, which owns filtering absent/non-positive candidates, converting admitted candidates, and final score/category ordering before `PressureAudit` construction. This slice does not change that admission rule. It separates the adjacent producer responsibility that collects the consumer audit source once and hands two consumer-predicate candidate slots to admission.

## Remaining compressed responsibilities

Remaining compression should continue to be selected only from current implementation evidence. After this slice, `_admitted_pressure_items(...)` owns candidate admission, `_consumer_predicate_pressures(...)` owns consumer-predicate source handoff, and the category-specific pressure helpers continue to own their own evidence, scoring, reason, and recommended-command candidate payloads. Broader pressure source orchestration in `build_pressure_audit(...)`, individual category evidence assembly, text formatting, JSON conversion, and diagnostic surfaces remain unchanged and are not claimed by this slice.

## Guardrail notes

This slice preserves read-only visibility. It does not implement Frontier Pressure Admission as a feature, lawful acceptance, action, mutation, route authority, readiness evaluation, planning, prioritization, inquiry generation, or any general constitutional abstraction.
