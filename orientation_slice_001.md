# Orientation Slice 001

## Selected architectural boundary

Recovered boundary:

```text
External Orientation
        !=
Orientation
```

Selected recurring owner:

```text
Given a bounded orientation-producing surface, classify the implementation-local source of the orientation without generating the orientation itself.
```

This slice recovers only the implementation-local ownership boundary between the existing External Orientation specialization and a broader, still-unstabilized Orientation responsibility. It does not introduce an orientation engine, framework, registry, schema, CLI flag, JSON shape, ledger behavior, routing framework, planner, scheduler, diagnostic redesign, pressure redesign, question redesign, or runtime redesign.

Repository authority wins: the broader Orientation family remains provisional. The implementation evidence supports one narrow owner for orientation-source specialization, not a universal orientation framework.

## Implementation evidence

The reviewed implementation shows that orientation-producing surfaces already exist with different source responsibilities:

1. `external_orientation_slice_001.md`
   - The previous slice recovered `External Material != External Orientation`.
   - Its bounded artifacts include `InquiryOrientationView`, `SourceNavigationView`, bounded ask eligibility/selection/dispatch request records, operational surface classification rows, and diagnostic inventory entries.
   - That report explicitly avoided adding a cross-subsystem type and preserved subsystem-local ownership.

2. `seed_runtime/inquiry_orientation.py`
   - `record_inquiry_note(...)` preserves raw operator prose in an isolated inquiry-note store.
   - `build_inquiry_orientation(...)` produces `InquiryOrientationView` from the preserved external note.
   - `_ArchitecturalOrientationEvidence` and `_ArchitecturalOrientationAnswer` are implementation-local seams for evidence collection and answer composition before rendering.
   - This remains external-orientation evidence because the source material is externally supplied operator prose.

3. `seed_runtime/source_navigation.py`
   - `build_source_navigation(state, query)` accepts an operator query and produces a bounded `SourceNavigationView` from projected source facts.
   - The output is orientation-like navigation, but the implementation boundary is still query-driven and bounded by existing `defines` and `imports` facts.
   - This is external-orientation evidence, not proof that all source navigation owns the broader family.

4. `seed_runtime/question_surface_inventory.py`
   - `BoundedWorkEligibilityResult`, `BoundedWorkSelectionResult`, and `BoundedWorkDispatchRequest` distinguish exact operator-provided question-family text from implementation-backed bounded work.
   - The same file also marks some families as diagnostic-only and refuses to treat unknown text as dispatch authority.
   - This evidence distinguishes an external question-family specialization from diagnostic-only and non-dispatchable orientations.

5. `seed_runtime/operational_surface_inventory.py`
   - Operational surface classification distinguishes CLI flags, manual inputs, diagnostic inputs, and recordable outputs.
   - The classification is an orientation-producing surface about operational visibility, but it does not generate downstream execution or repository truth.
   - This supports source-specialization ownership rather than a generic orientation redesign.

6. `seed_runtime/diagnostic_inventory.py` and `seed_runtime/diagnostic_shape_audit.py`
   - `DiagnosticInventoryEntry` declarations preserve diagnostic-surface boundaries such as record scope, ledger writes, cluster fact emission, projected-state reads, and cluster mutation.
   - `DiagnosticShapeAuditRow` compares declared diagnostic shape to observed implementation markers.
   - These are diagnostic-orientation surfaces: they orient operators and tests around diagnostic shape without being external material orientation.

7. `seed_runtime/pressure_audit.py`
   - `PressureAudit` and `PressureItem` aggregate pressure from diagnostic shape, ownership discrepancy, capability pressure, and predicate pressure inputs.
   - The audit recommends inspection commands, but does not plan, repair, record, or mutate state.
   - This supports pressure-based orientation as a specialization distinct from External Orientation.

8. `seed_runtime/observation_domains.py`
   - `ObservationDomainReport` classifies observation domains and includes a read-only, non-mutating boundary.
   - This is orientation around observation-domain coverage and pressure, not externally supplied material.

9. `seed_runtime/state.py`
   - Implementation-local projection seams such as `_ProjectionInfluenceLineage`, `_ReplayScopeAssessment`, `_ReplaySelectionJustification`, and `_ReplaySelection` orient projection work around state/replay visibility.
   - They are not external material orientation and do not justify stabilizing a generic Orientation framework.

10. Architectural reports reviewed
    - `docs/architectural_inquiry_orientation_surface_audit.md` describes architectural self-orientation as derivable from repository-local implementation evidence but not yet exposed as a runtime surface.
    - `orientation_guided_recovery_methodology_characterization.md`, `cross_domain_orientation_territory_recurrence_investigation.md`, and `constitutional_neighborhood_characterization_methodology.md` provide secondary evidence that orientation vocabulary recurs across investigations.
    - These reports support recurrence, but implementation files remain the authority for the narrow recovered boundary.

## Before

External Orientation and broader Orientation were previously mixed wherever orientation-like surfaces were discussed only through subsystem-specific labels:

- Inquiry orientation mixed externally supplied inquiry notes with the broader idea of architectural orientation.
- Source navigation mixed external query orientation with repository artifact/source visibility.
- Question-family eligibility mixed external question text with diagnostic-only and non-dispatchable question-surface visibility.
- Diagnostic inventory and shape audit mixed diagnostic-surface orientation with the broader language of operational visibility.
- Pressure audit mixed pressure-based orientation with inspection recommendation text.
- Observation-domain visibility mixed state/coverage orientation with operational pressure.
- Projection/state implementation seams mixed state/replay visibility with possible orientation vocabulary.

The compression was not behavioral. Existing code already kept these surfaces bounded. The missing boundary was ownership vocabulary for the recurring question:

```text
What kind of source produced this bounded orientation surface?
```

## After

The recurring boundary is now directly observable in this report:

```text
bounded orientation-producing surface
        -> orientation-source specialization
        -> existing subsystem-local consumer
```

The recovered owner answers only whether a bounded orientation-producing surface is sourced by a specialization such as:

- external material;
- internal insufficiency or implementation-local state;
- diagnostic shape or diagnostic inventory;
- pressure visibility;
- question eligibility;
- state/projection visibility;
- source navigation;
- architectural family position;
- another implementation-supported specialization.

The owner does not generate orientation, interpret evidence, decide operator intent, dispatch questions, repair pressure, promote authority, construct facts, plan, execute, mutate runtime state, alter schema, or change compatibility boundaries.

## Recovered producer

Recovered producer:

```text
Orientation source specialization classifier
```

This is a report-level recovered producer only. No new runtime producer was added because existing implementation evidence does not require a cross-cutting type or executable registry.

Implementation-backed producer examples remain subsystem-local:

- `build_inquiry_orientation(...)` produces external inquiry orientation.
- `build_source_navigation(...)` produces query-bounded source navigation orientation.
- `bounded_work_eligibility_for_question_family(...)` produces question-family eligibility orientation.
- `build_operational_surface_classification_audit(...)` produces operational surface classification orientation.
- `DIAGNOSTIC_INVENTORY` and `build_diagnostic_shape_audit(...)` produce diagnostic-surface orientation.
- `build_pressure_audit(...)` produces pressure-based orientation.
- `build_observation_domains(...)` produces observation-domain visibility orientation.
- Projection/replay helper records in `state.py` preserve implementation-local state/projection orientation.

## Recovered artifact, if any

No new implementation artifact is produced.

The recurring artifact is currently report-level only:

```text
Orientation source specialization record
```

It is not implemented as a new class, enum, registry row, JSON field, CLI output, or schema shape because the repository does not yet show a consumer that needs a shared runtime artifact.

Existing implementation artifacts remain unchanged and subsystem-local:

- `InquiryOrientationView`.
- `SourceNavigationView`.
- `BoundedWorkEligibilityResult`.
- `BoundedWorkSelectionResult`.
- `BoundedWorkDispatchRequest`.
- `OperationalSurfaceClassificationAudit`.
- `DiagnosticInventoryEntry`.
- `DiagnosticShapeAuditRow`.
- `PressureAudit` and `PressureItem`.
- `ObservationDomainReport` and `ObservationDomainEntry`.
- Projection/replay helper records in `state.py`.

## Consumer of the artifact

No new runtime consumer exists.

The consumer of this recovered artifact is the architectural recovery process represented by this report and later implementation-slice selection. Existing subsystem consumers remain unchanged:

- Inquiry formatting consumes `InquiryOrientationView`.
- Source-navigation formatting consumes `SourceNavigationView`.
- Bounded ask dispatch consumes bounded eligibility, selection, and dispatch request records.
- Operational visibility rendering consumes operational surface classification rows.
- Diagnostic inventory and shape-audit paths consume diagnostic inventory declarations and shape-audit rows.
- Pressure rendering consumes `PressureAudit`.
- Observation-domain rendering consumes `ObservationDomainReport`.
- State projection/replay internals consume their implementation-local helper records.

## Compatibility preserved

No compatibility boundary changed.

- No CLI flags changed.
- No JSON output changed.
- No schema changed.
- No ledger behavior changed.
- No diagnostic registry behavior changed.
- No diagnostic shape-audit behavior changed.
- No inquiry behavior changed.
- No source-navigation behavior changed.
- No bounded ask behavior changed.
- No pressure-audit behavior changed.
- No observation-domain behavior changed.
- No state/projection behavior changed.
- No runtime behavior changed.

## Files changed

- Added `orientation_slice_001.md`.

## LOC changed

- Added 261 lines.
- Removed 0 lines.
- Net change: +261 lines.

## Tests executed

Commands executed:

```text
python scripts/seed_local.py --diagnostic-inventory
python scripts/seed_local.py --diagnostic-shape-audit
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

## Remaining compressed Orientation responsibilities

The following responsibilities remain compressed and intentionally unrecovered:

- Whether a runtime `OrientationSourceKind` enum is needed.
- Whether a shared `OrientationSurfaceClassification` class is needed.
- Whether architectural family position should become a dedicated read-only surface.
- Whether source navigation is best treated as external-query orientation or repository-artifact orientation in a future implementation-backed slice.
- Whether pressure visibility, diagnostic shape mismatches, state/projection visibility, and question eligibility should share any runtime vocabulary.
- Whether implementation-local orientation source specialization should ever become visible in CLI or JSON output.

Current implementation evidence is sufficient to distinguish External Orientation as a specialization. It is insufficient to stabilize the broader Orientation family as a framework.

## Questions

### 1. Where were External Orientation and broader Orientation previously mixed?

They were mixed in subsystem-local orientation surfaces whose source specialization was implicit: external inquiry notes in inquiry orientation, external source-navigation queries in source navigation, exact question-family text in bounded ask, diagnostic declarations in diagnostic inventory, diagnostic implementation checks in shape audit, pressure rows in pressure audit, observation-domain coverage in observation domains, and state/projection helper records in state projection.

### 2. Which recovered architectural boundary became more explicit?

The boundary between External Orientation and broader Orientation became explicit:

```text
External Orientation
        !=
Orientation
```

External Orientation is preserved as one source specialization within recurring orientation-producing surfaces, not inflated into the whole family.

### 3. What implementation artifact is now produced, if any, and who consumes it?

No new implementation artifact is produced.

A report-level orientation source specialization record is now recoverable for architectural reasoning, but no runtime class, enum, registry row, CLI output, JSON field, schema shape, or ledger event was added. The architectural recovery process consumes the report-level artifact. Existing subsystem artifacts and consumers remain unchanged.

### 4. Did implementation evidence suggest a more precise responsibility name?

Orientation source specialization.

### 5. Did any compatibility boundary change?

No.
