# Constitutional Relationship Next Implementation Pressure Survey

## Scope and discipline

This is one Implementation Pressure Survey. It does not recover implementation, does not recover a slice, and does not modify existing recovery campaigns. The survey inspects implementation neighborhoods immediately adjacent to the previously recovered Inquiry Orientation and Reasoning Path constitutional relationship work, then stops at repository evidence.

## Implementation neighborhoods surveyed

### Selection Path

Selection Path is implementation-adjacent because it consumes Operational Story and Pressure Audit outputs to explain implemented selection behavior. The builder imports `build_operational_story` and `build_pressure_audit`, then gathers both in `_selection_path_inputs(...)` before target-specific selection handling. Evidence: `build_selection_path_audit(...)` normalizes a target, obtains `_SelectionPathInputs`, supports current-focus and pressure-category targets, and returns an explicit unsupported-target audit otherwise.

Implementation evidence observed:

- Public compatibility artifact: `SelectionPathAudit` exposes `target`, `selected`, `candidates`, `selection_factors`, `non_selected`, `evidence`, `outcome`, `unknowns`, and a read-only boundary.
- Candidate producer/helper chain: `_selection_path_inputs(...)`, `_target_matches_focus_selection(...)`, `_target_matches_pressure_category(...)`, `_selected_pressure_item(...)`, `_candidate_set_from_pressures(...)`, `_selection_factors_from_pressures(...)`, `_non_selected_from_pressures(...)`, and `_selected_pressure_evidence(...)` already exist.
- Compressed implementation-local responsibilities recur around result, reason/outcome, support, candidate set, factors, non-selected candidate explanation, unknowns, lineage, and compatibility handoff.
- Tests already pin the surface, JSON shape, read-only boundary, compatibility handoff, unsupported-target unknowns, and payload separation.

### Operational Story

Operational Story is implementation-adjacent because Selection Path and Reasoning Path both consume it, and it composes multiple existing visibility surfaces into a bounded read-only operator story. The builder gathers Pressure Audit, Capability Needs, Privilege Discovery, Correlation Audit, Impact Audit, and Investigation Path Audit, then composes answer, reasoning, supporting evidence, boundary, and limitations payloads.

Implementation evidence observed:

- Public compatibility artifact: `OperationalStory` exposes focus, pressure, supporting evidence, capabilities, constraints, correlation gaps, impact, recent changes, observed outcomes, investigation path, unknowns, and boundary.
- Candidate producer/helper chain: `build_operational_story(...)`, `_compose_operational_story_payloads(...)`, `_focus(...)`, `_pressure(...)`, `_supporting_evidence(...)`, `_capability(...)`, `_constraint(...)`, `_correlation(...)`, `_metric(...)`, `_recent_changes(...)`, `_observed_outcomes(...)`, `_impact_unknown_reason(...)`, and `_domain_for(...)` already exist.
- Compressed implementation-local responsibilities recur around broad composition, answer material, investigation-path reasoning, supporting evidence, limitations/Unknowns, read-only boundary, and public compatibility handoff.
- Tests already pin rendering, JSON validity, read-only boundary, incorporated surfaces, empty-state Unknowns, payload separation, and field non-overlap.

### Reasoning Path residual adjacency

Reasoning Path was inspected only as an already-recovered adjacent boundary, not as a new target. The current implementation already separates derived conclusions, supporting evidence, lineage consumers/story impact/unknowns, and compatibility handoff. Its remaining adjacent pressure points lead outward to Selection Path and Operational Story rather than exposing a stronger unrecovered Reasoning Path-local neighborhood in this survey.

Implementation evidence observed:

- Public compatibility artifact: `ReasoningPathAudit` exposes domain, subject, evidence, intermediate conclusions, derived conclusions, consumers, story impact, unknowns, and read-only boundary.
- Candidate producer/helper chain includes `build_reasoning_path_audit(...)`, `_reasoning_path_relevant_ownership_rows(...)`, `_reasoning_path_intermediate_conclusions(...)`, `_reasoning_path_derived_capability_conclusions(...)`, `_reasoning_path_supporting_evidence_payload(...)`, `_reasoning_path_capability_need_consumers(...)`, `_reasoning_path_pressure_privilege_consumers(...)`, `_reasoning_path_story_impact(...)`, and `_reasoning_path_typed_unknowns(...)`.
- Tests already pin rendering, JSON read-only behavior, compatibility handoff, subject selection, supporting evidence projection, and consumer/story-impact lineage.

### Inquiry Artifact / Inquiry View residual adjacency

Inquiry Artifact / Inquiry View was inspected as previously recovered Inquiry Orientation-adjacent context. Current implementation evidence supports a narrow preserved-note and read-only orientation boundary. In this survey, it did not expose stronger adjacent implementation pressure than Selection Path or Operational Story, because its implementation responsibilities are already bounded to inquiry note preservation and lexical orientation rather than broad selection/reasoning handoff.

## Strongest adjacent implementation pressure

The strongest recoverable implementation-local ownership pressure is **Selection Path**.

Repository evidence favors Selection Path over Operational Story for the next adjacent implementation recovery campaign because Selection Path is a narrower implementation neighborhood with multiple already-exposed compressed responsibilities that are currently clustered inside one module: target normalization, implemented-target matching, pressure candidate selection, selected result production, reason/outcome production, support/evidence production, candidate-set production, selection-factor production, non-selected explanation, typed Unknown preservation, and public compatibility projection.

Operational Story has strong pressure, but its current shape is broader terminal composition over many already-existing surfaces. That breadth makes it less implementation-local than Selection Path for the constitutional recovery condition. Reasoning Path residuals point to already-recovered derivation-lineage ownership. Inquiry Artifact / Inquiry View remains bounded and does not show a stronger unrecovered ownership knot.

## Candidate producer(s)

Selection Path candidate producers already exposed by implementation evidence:

- `build_selection_path_audit(...)` as the public producer of the audit object.
- `_selection_path_inputs(...)` as the local producer of pressure/focus inputs from Pressure Audit and Operational Story.
- `_from_focus_selection(...)` and `_from_pressure_category_selection(...)` as target-specific local producers.
- `_pressure_selection_payloads(...)` and `_selection_path_from_payloads(...)` / `_selection_path_from_payload_bundle(...)` as compatibility-handoff producers.

Operational Story candidate producers were also observed but ranked second:

- `build_operational_story(...)`.
- `_compose_operational_story_payloads(...)`.

## Candidate artifact/helper(s)

Selection Path candidate artifacts/helpers already exposed by implementation evidence:

- `_SelectionResultPayload`.
- `_SelectionReasonPayload`.
- `_SelectionSupportingEvidencePayload`.
- `_SelectionCandidateSetPayload`.
- `_SelectionNonSelectedPayload`.
- `_SelectionFactorPayload`.
- `_SelectionUnknownPayload`.
- `_SelectionLineagePayload`.
- `_SelectionPathInputs`.
- `_SelectionPathPayloads`.
- Helpers for target matching, selected item selection, candidate ranking, non-selected reasons, evidence rows, and typed Unknown production.

Operational Story candidate artifacts/helpers already exposed by implementation evidence:

- `_OperationalStoryAnswerPayload`.
- `_OperationalStoryLimitationsPayload`.
- `_OperationalStoryReasoningPayload`.
- `_OperationalStorySupportingEvidencePayload`.
- `_OperationalStoryBoundaryPayload`.

## Recurring compressed implementation-local responsibilities observed

Across Selection Path, Operational Story, and Reasoning Path, the same implementation-local compression pattern recurs:

1. Gather bounded implemented inputs from existing surfaces.
2. Select or compose a local answer/result.
3. Preserve reason material separately from answer/result material.
4. Preserve support/evidence separately from reason material.
5. Preserve lineage, candidates, consumers, story impact, or investigation path separately from final public answer fields.
6. Preserve typed Unknowns when implementation evidence is absent.
7. Preserve read-only/no-ledger/no-cluster-mutation boundary.
8. Hand local payloads into the unchanged public compatibility artifact.

Selection Path has the highest recoverable pressure because all of these recur inside a narrow selection-specific neighborhood while still depending on adjacent recovered relationship surfaces.

## Required answers

1. **Which implementation neighborhoods were inspected?** Selection Path, Operational Story, Reasoning Path residual adjacency, and Inquiry Artifact / Inquiry View residual adjacency.
2. **Which neighborhood currently exhibits the strongest recoverable ownership pressure?** Selection Path.
3. **What recurring compressed implementation-local responsibilities were observed?** Bounded input gathering, answer/result production, reason/outcome production, support/evidence production, candidate/lineage/consumer/investigation-path preservation, typed Unknown preservation, authority-boundary preservation, and compatibility handoff.
4. **Does implementation already expose candidate producers?** Yes. Selection Path exposes public and local producers including `build_selection_path_audit(...)`, `_selection_path_inputs(...)`, `_from_focus_selection(...)`, `_from_pressure_category_selection(...)`, `_pressure_selection_payloads(...)`, and compatibility-handoff helpers.
5. **Does implementation already expose candidate artifacts or helpers?** Yes. Selection Path exposes payload dataclasses for result, reason, support, candidate set, non-selected candidates, factors, unknowns, lineage, inputs, and payload bundle, plus helper functions for target matching, ranking, evidence, and Unknowns.
6. **Is the neighborhood ready for an implementation recovery campaign?** Ready for implementation recovery.

## Readiness classification

Ready for implementation recovery

## Preserved Unknowns

- Unknown whether a future implementation change will make Operational Story a stronger candidate; current repository evidence ranks it second because it is broad composition rather than the strongest narrow adjacent ownership knot.
- Unknown whether Inquiry Artifact / Inquiry View will expose additional pressure after future changes; current evidence keeps it bounded to preserved-note and read-only lexical-orientation responsibilities.
- Unknown whether Selection Path should be recovered in any particular slice order; this survey identifies pressure only and intentionally does not recover implementation or define a campaign plan.
- Unknown whether unsupported selection targets will expand; current implementation explicitly returns typed Unknowns for unsupported targets.

## Confidence

High confidence that Selection Path is the strongest adjacent implementation-local ownership pressure for the next recovery campaign. The confidence is based on implementation code exposing distinct local payloads, producers, helpers, boundary preservation, Unknown preservation, compatibility handoff, and tests pinning those surfaces. The survey does not claim architectural preference or readiness beyond repository implementation evidence.

Implementation pressure survey complete.
