# Constitutional Relationship Selection Path Completion Audit

## Scope and implementation inspected

This is exactly one bounded Implementation Completion Audit for the Selection Path implementation family. It does not recover implementation, recover another slice, introduce frameworks, introduce registries, introduce engines, introduce planners, introduce schedulers, introduce workflows, or redesign architecture.

Inspection was limited to implementation immediately adjacent to:

- `build_selection_path_audit(...)`
- `_selection_target_selection(...)`
- `_pressure_selection_payloads(...)`
- `_selection_path_from_payloads(...)`
- `_selection_path_from_payload_bundle(...)`

Expansion was limited to directly adjacent helpers and artifacts naturally reached from those functions: source input preparation, target selection, focus/category branch handoff, unsupported-target handoff, pressure-selection payload bundle production, lineage payload production, payload-member producers, and public compatibility construction.

## Implementation evidence inspected

`build_selection_path_audit(...)` currently owns only the top-level read-only audit orchestration: resolve repository root, normalize the requested target, collect pressure/focus inputs, ask `_selection_target_selection(...)` for the implemented route classification, dispatch focus selections to `_from_focus_selection(...)`, dispatch pressure-category selections to `_from_pressure_category_selection(...)`, and dispatch unsupported targets to `_unsupported_target_selection(...)`.

`_selection_target_selection(...)` owns the route classification artifact `_SelectionTargetSelection`. It checks focus-selection recognition first, then pressure-category recognition, then returns unsupported selection. It does not produce payload members, select pressure evidence rows, construct public audits, record facts, write the event ledger, or mutate cluster state.

`_pressure_selection_payloads(...)` is the implemented pressure-selection payload-bundle producer. It selects the first pressure item, obtains typed Unknown payloads from pressure availability, and composes `_SelectionPathPayloads` from narrower result, reason, support, and lineage producers.

`_selection_path_from_payloads(...)` is the compatibility adapter for callers that already hold separate result, reason, support, and lineage payloads. It wraps those members in `_SelectionPathPayloads` and delegates construction to `_selection_path_from_payload_bundle(...)`.

`_selection_path_from_payload_bundle(...)` is the public compatibility construction handoff. It constructs `SelectionPathAudit` from an already-composed payload bundle and converts typed Unknown records to public dictionaries. The default boundary on `SelectionPathAudit` remains read-only: `records_facts=false`, `writes_event_ledger=false`, and `mutates_cluster=false`.

## Recovered implementation progression

The current implementation shows the following implementation-local progression already recovered before this audit:

1. Repository-root preparation is separated into `_selection_path_repo_root(...)`.
2. Pressure/focus source input collection is separated into `_selection_path_inputs(...)` and `_SelectionPathInputs`.
3. Selection-target resolution is separated into `_selection_target_selection(...)` and `_SelectionTargetSelection`.
4. Focus selected-result production is separated into `_focus_selection_result(...)`, `_FocusSelectionResult`, and selected-name helpers.
5. Pressure-category selected-result production is separated into `_pressure_category_selection_result(...)`, `_PressureCategorySelectionResult`, and selected-name helpers.
6. Supported pressure-selection payload bundle composition is separated into `_pressure_selection_payloads(...)` and `_SelectionPathPayloads`.
7. Unsupported-target payload bundle composition is separated through `_unsupported_target_selection(...)`, unsupported result/reason/support/factor/non-selected/Unknown helpers, and `_unsupported_target_lineage_payload(...)`.
8. Payload-bundle compatibility construction is separated into `_selection_path_from_payloads(...)` and `_selection_path_from_payload_bundle(...)`.
9. The completed Payload Ownership Audit inspected candidate integration, factor integration, non-selected integration, supporting-evidence integration, lineage integration, and typed Unknown production/integration individually and found those responsibilities already exposed as named artifacts, named producers, and lawful existing ownership.

This progression reaches the same constitutional completion condition previously recovered for Inquiry Orientation and Reasoning Path: the remaining implementation is not a still-compressed same-family ownership boundary, but a set of stable surface responsibilities and compatibility handoffs.

## Remaining implementation responsibilities

The visible remaining responsibilities are:

| Responsibility | Current owner | Completion assessment |
| --- | --- | --- |
| Top-level audit orchestration | `build_selection_path_audit(...)` | Lawful orchestration; splitting would relocate route dispatch rather than recover a new owner. |
| Target route classification | `_selection_target_selection(...)` / `_SelectionTargetSelection` | Already recovered and locally owned. |
| Focus branch assembly | `_from_focus_selection(...)` plus focus result helpers | Already recovered and locally owned. |
| Pressure-category branch assembly | `_from_pressure_category_selection(...)` plus category result helpers | Already recovered and locally owned. |
| Unsupported-target refusal assembly | `_unsupported_target_selection(...)` plus unsupported payload helpers | Already recovered and locally owned. |
| Supported pressure-selection bundle production | `_pressure_selection_payloads(...)` / `_SelectionPathPayloads` | Already recovered and locally owned. |
| Candidate, factor, non-selected, support, lineage, and Unknown payload-member production | Payload-member dataclasses and helpers | Already lawfully owned according to the completed Payload Ownership Audit. |
| Public compatibility construction | `_selection_path_from_payloads(...)` and `_selection_path_from_payload_bundle(...)` | Already recovered compatibility handoff; further splitting would change no ownership pressure. |
| Public read-only audit representation | `SelectionPathAudit` | Stable compatibility object, not evidence of unowned implementation pressure. |

No implementation-local responsibility remains that is both adjacent and compressed in the same Selection Path family.

## Payload ownership audit summary

The completed Payload Ownership Audit materially changes this completion assessment because it removes the last plausible payload-layer candidates from consideration as recoverable pressure.

The audit found:

- candidate integration has `_SelectionCandidateSetPayload`, `_candidate_set_from_pressures(...)`, ranking helpers, row helpers, and public-name helpers;
- factor integration has `_SelectionFactorPayload`, `_selection_factors_from_pressures(...)`, and `_unsupported_target_factor_payload(...)`;
- non-selected integration has `_SelectionNonSelectedPayload`, `_non_selected_from_pressures(...)`, `_non_selected_pressure_candidates(...)`, `_non_selected(...)`, `_non_selected_reason(...)`, and `_unsupported_target_non_selected_payload(...)`;
- supporting-evidence integration has `_SelectionSupportingEvidencePayload`, `_pressure_selection_supporting_evidence_payload(...)`, `_selected_pressure_evidence(...)`, and `_unsupported_target_supporting_evidence_payload(...)`;
- lineage integration has `_SelectionLineagePayload`, `_pressure_selection_lineage_payload(...)`, and `_unsupported_target_lineage_payload(...)`;
- typed Unknown production/integration has `_SelectionUnknownPayload`, `_selection_unknowns_from_pressures(...)`, `_unsupported_target_unknown_payload(...)`, `preserve_typed_unknown(...)`, `TypedUnknownRecord`, and `typed_unknowns_to_public_dicts(...)`.

Therefore the remaining visible payload responsibilities represent already lawful ownership, not recoverable ownership pressure. Another payload slice would merely rename or relocate already-owned implementation.

## Candidate producer assessment

### Required question 1: What implementation-local responsibilities currently remain?

Current remaining responsibilities are orchestration, route classification, branch handoff, payload production, payload-member production, compatibility construction, public read-only representation, formatting, and generic target/candidate text helpers. Within the inspected neighborhood, all are either already locally owned or stable compatibility/presentation responsibilities.

### Required question 2: Does implementation expose another adjacent implementation-local producer?

Yes, the implementation exposes many adjacent producers, including `_selection_path_inputs(...)`, `_selection_target_selection(...)`, `_from_focus_selection(...)`, `_from_pressure_category_selection(...)`, `_unsupported_target_selection(...)`, `_pressure_selection_payloads(...)`, `_pressure_selection_lineage_payload(...)`, `_unsupported_target_lineage_payload(...)`, `_selection_path_from_payloads(...)`, and `_selection_path_from_payload_bundle(...)`.

However, exposure is not the same as recoverable compression. These producers are already named and already own bounded responsibilities. The audit found no adjacent producer that is both unowned and recoverably compressed.

### Required question 3: Does implementation expose another adjacent implementation-local artifact or helper whose recovery would reduce ownership compression?

No.

The adjacent artifacts and helpers are already doing bounded work: `_SelectionPathInputs`, `_SelectionTargetSelection`, `_FocusSelectionResult`, `_PressureCategorySelectionResult`, `_SelectionPathPayloads`, `_SelectionLineagePayload`, member payload dataclasses, route-match helpers, selected-result helpers, candidate helpers, non-selected helpers, evidence helpers, and Unknown helpers. Recovering any one of these now would not reduce ownership compression; it would duplicate a visible boundary or move code between already-owned helpers.

## Candidate artifact/helper assessment

The strongest remaining artifact candidates are `_SelectionPathPayloads`, `_SelectionLineagePayload`, and `SelectionPathAudit`.

- `_SelectionPathPayloads` is already the recovered supported/unsupported payload bundle artifact.
- `_SelectionLineagePayload` is already the recovered lineage grouping for candidate set, factors, non-selected candidates, and Unknown payloads.
- `SelectionPathAudit` is the stable public compatibility object and includes the read-only boundary. Its combined public shape is not evidence that private ownership remains compressed.

The strongest remaining helper candidates are `_selection_path_from_payloads(...)`, `_selection_path_from_payload_bundle(...)`, `_pressure_selection_lineage_payload(...)`, and `_unsupported_target_lineage_payload(...)`. Each already has a bounded role: adapter, compatibility constructor, implemented lineage grouping, and unsupported lineage grouping. No candidate helper shows new implementation pressure that would reduce ownership compression if sliced.

## Implementation pressure assessment

### Required question 4: Would another implementation slice recover ownership, or merely relocate already-owned implementation?

Another implementation slice in the inspected neighborhood would merely relocate already-owned implementation.

The only remaining visible pressure is observational: the public audit still contains many fields, and the implementation still has many helpers. Repository evidence shows those helpers already expose the ownership boundaries recovered by the campaign. The existence of a named helper, public field, or compatibility object is not enough to justify another slice.

### Required question 5: Does the completed Payload Ownership Audit materially change the completion assessment?

Yes.

Before the Payload Ownership Audit, candidate, factor, non-selected, supporting-evidence, lineage, and typed Unknown integration could have been plausible remaining payload-layer questions. After that audit, each remaining payload-member responsibility has been inspected individually and classified as already lawfully owned. That makes the completion assessment stronger: the payload layer no longer supplies a repository-backed reason to continue slicing Selection Path.

### Required question 6: Is the Selection Path implementation family complete?

Yes.

Within the inspected implementation neighborhood and using the completed Payload Ownership Audit as evidence for the remaining payload layer, the Selection Path implementation family is complete.

## Completion classification

```text
Implementation family complete
```

## Preserved Unknowns

- Whether future implementation changes outside this inspected neighborhood will create new Selection Path ownership pressure is unknown.
- Whether renderer, CLI, diagnostic inventory, diagnostic shape-audit, or unrelated operational-story neighborhoods contain their own future ownership pressure is unknown because they were outside this audit scope.
- Whether campaign documents name additional desired work is not authoritative unless implementation evidence in the inspected neighborhood supports it.
- Whether another surface should reuse Selection Path vocabulary is unknown; presentation vocabulary is not repository knowledge without implementation evidence.

## Confidence

High.

Confidence is high because the inspected implementation exposes named producers, named artifacts, bounded route classification, bounded branch handoffs, bounded payload-bundle production, bounded payload-member producers, and a bounded compatibility constructor. The completed Payload Ownership Audit individually exhausted the remaining plausible payload-member responsibilities and found already lawful ownership rather than recoverable pressure.

Selection Path implementation completion audit complete.
