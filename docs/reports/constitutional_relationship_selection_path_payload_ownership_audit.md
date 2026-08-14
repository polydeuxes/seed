# Selection Path Payload Ownership Audit

## Scope

This is one bounded Payload Ownership Audit. It does not recover implementation, recover a slice, introduce a new framework, or modify existing implementation slices.

The inspection started at the implementation immediately adjacent to:

- `_SelectionPathPayloads`
- `_pressure_selection_payloads(...)`
- `_selection_path_from_payloads(...)`
- `_selection_path_from_payload_bundle(...)`

Expansion was limited to directly consumed payload artifacts, directly called helper/producers, and adjacent tests that prove the current ownership shape.

## Adjacent implementation evidence

`_SelectionPathPayloads` is a four-member bundle artifact. It carries only result, reason, supporting-evidence, and lineage payloads.

The unsupported branch enters the payload layer by calling `_selection_path_from_payloads(...)` with separately prepared result, reason, support, and lineage payloads. `_selection_path_from_payloads(...)` wraps those already-prepared members into `_SelectionPathPayloads` and delegates to `_selection_path_from_payload_bundle(...)`.

The implemented pressure-selection path enters the same bundle layer through `_pressure_selection_payloads(...)`. That helper selects the first pressure item, obtains typed Unknown payloads, and returns `_SelectionPathPayloads` from narrower payload producers for result, reason, support, and lineage.

`_selection_path_from_payload_bundle(...)` is the compatibility construction handoff. It reads the already-composed bundle fields and constructs `SelectionPathAudit`, including candidates, selection factors, non-selected candidates, supporting evidence, outcome, and public Unknown dictionaries.

## Payload responsibilities inspected

### 1. Candidate integration

**Implementation evidence**

Candidate integration is represented by `_SelectionCandidateSetPayload`, `_candidate_set_from_pressures(...)`, `_ranked_pressure_candidates(...)`, `_pressure_candidate_row(...)`, and `_pressure_selection_lineage_payload(...)`.

For implemented pressure selections, `_pressure_selection_lineage_payload(...)` places `_candidate_set_from_pressures(pressures)` into `_SelectionLineagePayload.candidate_set`. `_selection_path_from_payload_bundle(...)` later projects `payloads.lineage.candidate_set.candidates` into the public audit candidates field.

Adjacent tests already exercise this as an owned payload/helper surface: candidate set separation, ranked candidate ownership, candidate row ownership, pressure-candidate public-name projection, pressure-selection lineage ownership, and payload-bundle ownership are all tested.

**Required answers**

1. **Independent implementation-local producer exposed?** Yes, `_candidate_set_from_pressures(...)` is exposed as an implementation-local producer for candidate-set payloads, with `_pressure_candidate_row(...)`, `_ranked_pressure_candidates(...)`, and `_pressure_candidate_public_name(...)` as direct helper evidence.
2. **Independent implementation-local artifact/helper exposed?** Yes. `_SelectionCandidateSetPayload` is the artifact; `_candidate_set_from_pressures(...)` and its row/ranking helpers are the helpers.
3. **Would recovering this responsibility reduce ownership compression?** No. The producer/helper/artifact are already exposed and already tested; another recovery would duplicate an already visible ownership boundary.
4. **Or is the responsibility already lawfully owned?** Yes. Candidate integration is lawfully owned by the already recovered lineage and payload-bundle producers, with the narrower candidate-set producer already visible under that ownership.

**Candidate producer(s), if any**

- `_candidate_set_from_pressures(...)`
- `_ranked_pressure_candidates(...)`
- `_pressure_candidate_row(...)`
- `_pressure_candidate_public_name(...)`

**Candidate artifact/helper(s), if any**

- `_SelectionCandidateSetPayload`

### 2. Factor integration

**Implementation evidence**

Factor integration is represented by `_SelectionFactorPayload`, `_selection_factors_from_pressures(...)`, `_unsupported_target_factor_payload(...)`, `_pressure_selection_lineage_payload(...)`, and `_unsupported_target_lineage_payload(...)`.

For implemented pressure selections, `_selection_factors_from_pressures(...)` returns the pressure-ordering factor when pressures exist and `unknown` when they do not. Unsupported target selection separately produces its factor payload through `_unsupported_target_factor_payload(...)`. Both paths hand the factor payload into `_SelectionLineagePayload`, and `_selection_path_from_payload_bundle(...)` projects `payloads.lineage.factors.selection_factors` into the public audit.

Adjacent tests already prove factor payload separation from candidate-set and Unknown payloads and prove pressure-selection lineage ownership.

**Required answers**

1. **Independent implementation-local producer exposed?** Yes, `_selection_factors_from_pressures(...)` is exposed for implemented pressure-selection factors, and `_unsupported_target_factor_payload(...)` is exposed for unsupported-target factors.
2. **Independent implementation-local artifact/helper exposed?** Yes. `_SelectionFactorPayload` is the artifact; the two factor-producing helpers are exposed.
3. **Would recovering this responsibility reduce ownership compression?** No. The factor payload and producer/helper boundary is already separate from candidate-set, non-selected, and Unknown responsibilities.
4. **Or is the responsibility already lawfully owned?** Yes. Factor integration is lawfully owned by the already recovered lineage payload assembly and compatibility construction paths.

**Candidate producer(s), if any**

- `_selection_factors_from_pressures(...)`
- `_unsupported_target_factor_payload(...)`

**Candidate artifact/helper(s), if any**

- `_SelectionFactorPayload`

### 3. Non-selected integration

**Implementation evidence**

Non-selected integration is represented by `_SelectionNonSelectedPayload`, `_non_selected_from_pressures(...)`, `_non_selected_pressure_candidates(...)`, `_non_selected(...)`, `_non_selected_reason(...)`, `_unsupported_target_non_selected_payload(...)`, `_pressure_selection_lineage_payload(...)`, and `_unsupported_target_lineage_payload(...)`.

For implemented pressure selections, `_pressure_selection_lineage_payload(...)` passes the selected item into `_non_selected_from_pressures(...)`. That producer excludes the first pressure candidate through `_non_selected_pressure_candidates(...)`, shapes rows with `_non_selected(...)`, and explains each row through `_non_selected_reason(...)`. Unsupported targets separately return an empty non-selected payload. `_selection_path_from_payload_bundle(...)` projects `payloads.lineage.non_selected.non_selected` into the public audit.

Adjacent tests already prove non-selected payload separation, non-selected candidate helper ownership, non-selected reason helper ownership, pressure-selection lineage ownership, and pressure-selection payload bundle ownership.

**Required answers**

1. **Independent implementation-local producer exposed?** Yes, `_non_selected_from_pressures(...)` is exposed for implemented pressure selections, with `_unsupported_target_non_selected_payload(...)` exposed for unsupported targets.
2. **Independent implementation-local artifact/helper exposed?** Yes. `_SelectionNonSelectedPayload` is the artifact; `_non_selected_from_pressures(...)`, `_non_selected_pressure_candidates(...)`, `_non_selected(...)`, and `_non_selected_reason(...)` are helper/producers.
3. **Would recovering this responsibility reduce ownership compression?** No. It is already separated into artifact, producer, row helper, candidate-filter helper, and reason helper.
4. **Or is the responsibility already lawfully owned?** Yes. Non-selected integration is lawfully owned by existing lineage construction and bundle compatibility construction.

**Candidate producer(s), if any**

- `_non_selected_from_pressures(...)`
- `_unsupported_target_non_selected_payload(...)`
- `_non_selected_pressure_candidates(...)`
- `_non_selected(...)`
- `_non_selected_reason(...)`

**Candidate artifact/helper(s), if any**

- `_SelectionNonSelectedPayload`

### 4. Supporting-evidence integration

**Implementation evidence**

Supporting-evidence integration is represented by `_SelectionSupportingEvidencePayload`, `_pressure_selection_supporting_evidence_payload(...)`, `_selected_pressure_evidence(...)`, `_unsupported_target_supporting_evidence_payload(...)`, `_pressure_selection_payloads(...)`, `_selection_path_from_payloads(...)`, and `_selection_path_from_payload_bundle(...)`.

For implemented pressure selections, `_pressure_selection_payloads(...)` calls `_pressure_selection_supporting_evidence_payload(selected_item)`, which produces a support payload containing `_selected_pressure_evidence(selected_item)` when a selected item exists and an empty evidence list otherwise. Unsupported target selection produces empty supporting evidence through `_unsupported_target_supporting_evidence_payload(...)`. `_selection_path_from_payload_bundle(...)` projects `payloads.support.evidence` into the public audit evidence field.

Adjacent tests already prove reason/support separation, supporting-evidence helper ownership, selected-pressure evidence record ownership, and pressure-selection payload-bundle ownership.

**Required answers**

1. **Independent implementation-local producer exposed?** Yes, `_pressure_selection_supporting_evidence_payload(...)` is exposed for implemented pressure-selection support, and `_unsupported_target_supporting_evidence_payload(...)` is exposed for unsupported-target support.
2. **Independent implementation-local artifact/helper exposed?** Yes. `_SelectionSupportingEvidencePayload` is the artifact; `_pressure_selection_supporting_evidence_payload(...)` and `_selected_pressure_evidence(...)` are helper/producers.
3. **Would recovering this responsibility reduce ownership compression?** No. Supporting evidence is already separated from result, reason, lineage, candidate, factor, non-selected, and Unknown payloads.
4. **Or is the responsibility already lawfully owned?** Yes. Supporting-evidence integration is lawfully owned by the already recovered pressure-selection payload bundle and compatibility construction boundaries.

**Candidate producer(s), if any**

- `_pressure_selection_supporting_evidence_payload(...)`
- `_selected_pressure_evidence(...)`
- `_unsupported_target_supporting_evidence_payload(...)`

**Candidate artifact/helper(s), if any**

- `_SelectionSupportingEvidencePayload`

### 5. Lineage integration

**Implementation evidence**

Lineage integration is represented by `_SelectionLineagePayload`, `_pressure_selection_lineage_payload(...)`, `_unsupported_target_lineage_payload(...)`, `_pressure_selection_payloads(...)`, `_selection_path_from_payloads(...)`, and `_selection_path_from_payload_bundle(...)`.

For implemented pressure selections, `_pressure_selection_payloads(...)` calls `_pressure_selection_lineage_payload(pressures, selected_item, unknowns)`, and that helper groups the already-separated candidate-set, factor, non-selected, and Unknown payloads. Unsupported target selection calls `_unsupported_target_lineage_payload(pressures)`, which groups candidate-set, unsupported factor, unsupported non-selected, and unsupported Unknown payloads. `_selection_path_from_payload_bundle(...)` consumes lineage only after that grouping is complete.

Adjacent tests already prove pressure-selection lineage ownership, typed Unknown lineage ownership before public handoff, and payload-bundle ownership.

**Required answers**

1. **Independent implementation-local producer exposed?** Yes, `_pressure_selection_lineage_payload(...)` and `_unsupported_target_lineage_payload(...)` are exposed lineage producers.
2. **Independent implementation-local artifact/helper exposed?** Yes. `_SelectionLineagePayload` is the artifact; the implemented and unsupported lineage helpers are exposed.
3. **Would recovering this responsibility reduce ownership compression?** No. This exact ownership boundary is already explicit and already tested.
4. **Or is the responsibility already lawfully owned?** Yes. Lineage integration is lawfully owned by the already recovered lineage payload producers and then consumed by the already recovered payload-bundle compatibility path.

**Candidate producer(s), if any**

- `_pressure_selection_lineage_payload(...)`
- `_unsupported_target_lineage_payload(...)`

**Candidate artifact/helper(s), if any**

- `_SelectionLineagePayload`

### 6. Typed Unknown production/integration

**Implementation evidence**

Typed Unknown production/integration is represented by `_SelectionUnknownPayload`, `_selection_unknowns_from_pressures(...)`, `_unsupported_target_unknown_payload(...)`, `preserve_typed_unknown(...)`, `TypedUnknownRecord`, `typed_unknowns_to_public_dicts(...)`, `_pressure_selection_lineage_payload(...)`, `_unsupported_target_lineage_payload(...)`, and `_selection_path_from_payload_bundle(...)`.

For implemented pressure selections, `_pressure_selection_payloads(...)` obtains Unknowns once through `_selection_unknowns_from_pressures(pressures)` and passes that payload into `_pressure_selection_lineage_payload(...)`. That producer preserves an Evidence Gap only when no pressure candidates are available. Unsupported target selection produces an Implementation Unknown through `_unsupported_target_unknown_payload(...)`. `_selection_path_from_payload_bundle(...)` converts lineage Unknown records into the public audit shape through `typed_unknowns_to_public_dicts(...)`.

Adjacent tests already prove Unknown payload separation from candidate lineage, typed Unknown preservation before public handoff, and payload-bundle ownership.

**Required answers**

1. **Independent implementation-local producer exposed?** Yes, `_selection_unknowns_from_pressures(...)` is exposed for implemented pressure selections, and `_unsupported_target_unknown_payload(...)` is exposed for unsupported targets.
2. **Independent implementation-local artifact/helper exposed?** Yes. `_SelectionUnknownPayload` is the local artifact; `TypedUnknownRecord`, `preserve_typed_unknown(...)`, and `typed_unknowns_to_public_dicts(...)` are adjacent typed-Unknown preservation/conversion helpers.
3. **Would recovering this responsibility reduce ownership compression?** No. Production, transport through lineage, and public conversion are already separated and visible. A new slice would risk reclassifying existing lawful ownership as new ownership.
4. **Or is the responsibility already lawfully owned?** Yes. Typed Unknown production/integration is lawfully owned by existing Unknown payload producers, lineage integration, and compatibility construction.

**Candidate producer(s), if any**

- `_selection_unknowns_from_pressures(...)`
- `_unsupported_target_unknown_payload(...)`
- `preserve_typed_unknown(...)` as the typed Unknown record-preservation helper outside the Selection Path module
- `typed_unknowns_to_public_dicts(...)` as the public compatibility conversion helper outside the Selection Path module

**Candidate artifact/helper(s), if any**

- `_SelectionUnknownPayload`
- `TypedUnknownRecord`

## Implementation pressure assessment

The payload layer shows many visible responsibilities, but visibility is not the same as remaining recoverable compression. The immediate implementation evidence shows that candidate, factor, non-selected, supporting-evidence, lineage, and typed Unknown responsibilities are already represented by named artifacts and named helpers/producers.

The recovered progression already reaches compatibility construction. The remaining payload-member responsibilities are nested members consumed by already recovered producers rather than new unowned producers. Recovering them again would not reduce ownership compression; it would duplicate boundaries already exposed by implementation and tests.

The only pressure preserved by this audit is observational: future work should continue to use repository evidence before promoting any presentation vocabulary or campaign momentum into implementation ownership. No current adjacent implementation evidence justifies another Selection Path implementation slice inside this payload layer.

## Readiness classification

Implementation family complete

## Preserved Unknowns

- Whether a future change outside this inspected neighborhood will introduce a new payload-member responsibility is unknown. This audit did not inspect unrelated implementation neighborhoods.
- Whether broader rendering, CLI, diagnostic inventory, or operational-story neighborhoods contain separate future ownership pressure is unknown. They were outside this audit scope.
- Whether campaign documents outside the adjacent implementation evidence name additional desired boundaries is not authoritative for this audit unless backed by the inspected implementation.

## Confidence

High.

The adjacent implementation exposes named payload artifacts, named producers/helpers, and tests for each candidate responsibility. Repository evidence supports lawful existing ownership rather than another independently recoverable payload-layer implementation slice.

Selection Path payload ownership audit complete.
