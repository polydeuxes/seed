# External Orientation Slice 001

## Selected architectural boundary

Recovered boundary:

```text
External Material
        !=
External Orientation
```

Selected recurring owner:

```text
Given externally supplied material, produce the bounded orientation required by downstream implementation.
```

This slice recovers only the implementation-local ownership boundary between externally supplied material and bounded orientation. It does not recover question dispatch, inquiry execution, evidence interpretation, fact construction, observation construction, planning, authority promotion, schema changes, runtime redesign, ledger changes, or behavior changes.

## Implementation evidence

Multiple implementation surfaces already separate externally supplied material from downstream implementation-backed work:

1. `seed_runtime/inquiry_orientation.py`
   - `record_inquiry_note(...)` accepts raw operator prose and preserves it in an isolated JSONL probe store.
   - `build_inquiry_orientation(...)` consumes the preserved note and returns an `InquiryOrientationView` with related material, uncertainty, and an authority boundary.
   - `_collect_architectural_orientation_evidence(...)` and `_compose_architectural_orientation_answer(...)` show a local orientation composition seam before rendering.
   - Tests prove the note is not projected into runtime state and that orientation does not create actions, plans, ownership claims, or authority claims.

2. `seed_runtime/source_navigation.py`
   - `build_source_navigation(state, query)` accepts an operator query, normalizes it, and projects source-navigation rows from existing fact support only.
   - The produced `SourceNavigationView` is bounded navigation output: it uses projected `defines` and `imports` facts and explicitly avoids runtime behavior, ownership authority, semantic relevance, file inspection, parsing, call graph claims, or dependency correctness claims.

3. `seed_runtime/question_surface_inventory.py`
   - Bounded ask eligibility and selection separate operator-provided question-family text from lawful dispatch.
   - `BoundedWorkEligibilityResult`, `BoundedWorkSelectionResult`, and `BoundedWorkDispatchRequest` already represent successive bounded artifacts after external text is checked against implementation-backed maps.
   - The implementation rejects unknown or diagnostic-only question families rather than treating external phrasing as authority.

4. `seed_runtime/operational_surface_inventory.py`
   - CLI arguments and manual input flags are classified as implementation-backed operational surfaces or manual inputs.
   - This classifies surface shape and visibility; it does not turn manual input into execution authority.

5. `seed_runtime/diagnostic_inventory.py`
   - Diagnostic surfaces are registry entries with explicit record scope, ledger-write, cluster-fact, and mutation boundaries.
   - This preserves operational visibility while keeping diagnostics bounded and non-authoritative with respect to cluster truth unless explicitly declared.

6. `scripts/seed_local.py`
   - `--record-inquiry-note` captures raw operator prose.
   - `--inquiry-orientation` later renders bounded orientation for a selected note.
   - `apply_bounded_ask_dispatch(...)` maps `ask --question-family ...` through implementation-backed eligibility and dispatch seams instead of free-text intent.

## Before

External material and External Orientation were previously mixed at several seams:

- Inquiry notes mixed raw operator testimony with the first orientation-specific matching step inside the inquiry-orientation flow.
- Source navigation accepted a raw query and immediately performed bounded lookup and formatting-oriented view construction.
- Bounded ask accepted operator-provided question-family text and then performed eligibility, selection, and dispatch mutation in a tightly adjacent CLI path.
- Operational and diagnostic inventories classified CLI and diagnostic surfaces, but the shared ownership boundary was implicit: external/manual/diagnostic visibility material was classified before downstream use without becoming repository authority.

The recurring implementation behavior existed, but the ownership name was compressed into subsystem-specific terms such as inquiry note, query, question family, operational surface, manual input, and diagnostic entry.

## After

The recurring boundary is now directly observable in this report as a single implementation-local ownership slice:

```text
External Material -> bounded External Orientation -> downstream implementation-backed surface
```

The recovered owner is limited to orientation. It may preserve, classify, navigate, display, reject, or admit externally supplied material into bounded inquiry/visibility surfaces. It does not decide truth, intent, ownership, planning, dispatch legality beyond existing eligibility maps, or authority promotion.

## Recovered producer

Recovered producer:

```text
External Orientation producer
```

Implementation-backed producer examples already present:

- `build_inquiry_orientation(...)` produces bounded inquiry orientation from a preserved inquiry note.
- `build_source_navigation(...)` produces bounded source navigation from an operator query and projected source facts.
- `bounded_work_eligibility_for_question_family(...)` produces eligibility orientation for exact question-family text.
- `build_operational_surface_classification_audit(...)` produces classification orientation for CLI surfaces and manual input flags.
- `DIAGNOSTIC_INVENTORY` entries produce registered diagnostic surface orientation for operational visibility.

No new engine, framework, schema, ledger behavior, or runtime behavior was introduced.

## Recovered artifact, if any

A recurring artifact already exists, but only as subsystem-local shapes rather than one new cross-cutting type:

```text
bounded orientation result
```

Concrete existing artifacts include:

- `InquiryOrientationView`
- `_ArchitecturalOrientationEvidence`
- `_ArchitecturalOrientationAnswer`
- `SourceNavigationView`
- `BoundedWorkEligibilityResult`
- `BoundedWorkSelectionResult`
- `BoundedWorkDispatchRequest`
- `OperationalSurfaceClassificationAudit`
- `DiagnosticInventoryEntry`

No new shared `ExternalOrientationRequest`, `ExternalOrientationContext`, `BoundedOrientationInput`, or `ExternalOrientationResult` was added because implementation evidence does not yet require a cross-subsystem type. The recurring artifact is observable as bounded orientation results consumed by existing downstream surfaces.

## Consumer of the artifact

Existing consumers remain unchanged:

- Inquiry rendering consumes `InquiryOrientationView` via `format_inquiry_orientation(...)`.
- Source-navigation rendering consumes `SourceNavigationView` via `format_source_navigation(...)`.
- Bounded ask dispatch consumes `BoundedWorkEligibilityResult`, `BoundedWorkSelectionResult`, and `BoundedWorkDispatchRequest` through `scripts/seed_local.py`.
- Operational visibility rendering consumes `OperationalSurfaceClassificationAudit` and inventory rows.
- Diagnostic inventory and shape-audit paths consume `DiagnosticInventoryEntry` declarations.

## Compatibility preserved

No compatibility boundary changed.

- No CLI flags changed.
- No schema changed.
- No ledger behavior changed.
- No diagnostic registry behavior changed.
- No inquiry behavior changed.
- No source-navigation behavior changed.
- No bounded ask behavior changed.
- No runtime behavior changed.

## Files changed

- Added `external_orientation_slice_001.md`.

## LOC changed

- Added 199 lines.
- Removed 0 lines.
- Net change: +199 lines.

## Tests executed

Commands executed:

```text
python scripts/seed_local.py --question-surface-inventory
python scripts/seed_local.py --operational-surface-classification-audit
python scripts/seed_local.py --diagnostic-inventory
pytest -q tests/test_inquiry_orientation.py tests/test_source_navigation.py tests/test_operational_surface_inventory.py tests/test_diagnostic_inventory.py
```

## Remaining compressed External Orientation responsibilities

The remaining compressed responsibilities are intentionally not redesigned in this slice:

- Cross-subsystem naming remains subsystem-local.
- Inquiry orientation still owns its existing evidence and answer composition seam.
- Source navigation still owns its bounded query normalization and source-fact matching.
- Bounded ask still owns exact question-family eligibility, selection, and dispatch request creation.
- Operational surface inventory still owns CLI/manual-input classification.
- Diagnostic inventory still owns diagnostic surface declarations.

The next slice, if supported by future implementation evidence, could consider whether a shared artifact name is warranted. Current evidence is sufficient for a recurring boundary but insufficient to justify a new cross-cutting type.

## Questions

### 1. Where were External Material and External Orientation previously mixed?

They were mixed where subsystem-specific external inputs were immediately handled by bounded orientation work: raw inquiry notes in inquiry orientation, source-navigation queries in source navigation, exact question-family strings in bounded ask, manual CLI inputs in operational surface classification, and diagnostic CLI surface declarations in diagnostic inventory.

### 2. Which recovered architectural boundary became more explicit?

The boundary between externally supplied material and bounded External Orientation became explicit:

```text
External Material -> External Orientation
```

External material may be preserved, classified, navigated, displayed, rejected, or admitted into bounded surfaces without becoming repository authority.

### 3. What implementation artifact is now produced, if any, and who consumes it?

No new cross-cutting artifact was introduced. Existing bounded orientation artifacts are now recognized as members of the same recurring ownership family: `InquiryOrientationView`, `SourceNavigationView`, bounded work eligibility/selection/dispatch request results, operational surface classification audit rows, and diagnostic inventory entries.

Existing renderers, CLI dispatch paths, inventory paths, and diagnostic shape-audit paths consume those artifacts.

### 4. Did implementation evidence suggest a more precise responsibility name?

Bounded External Orientation.

### 5. Did any compatibility boundary change?

No.
