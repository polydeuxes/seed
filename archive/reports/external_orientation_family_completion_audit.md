# External Orientation Family Completion Audit

## Scope

This audit reviews the recovered External Orientation family as represented by:

- `external_orientation_slice_001.md`
- `external_orientation_slice_002.md`
- `external_orientation_slice_003.md`
- `external_orientation_slice_004.md`
- `external_orientation_slice_005.md`
- `external_orientation_slice_006.md`

The audit assumes those slices are correct. It does not recover additional implementation, introduce a shared abstraction, or cross into neighboring families. The question is whether the currently surveyed External Orientation neighborhood is complete for the present implementation.

## Recovered family members

The recovered family currently contains these implementation-local boundaries:

| Slice | Recovered boundary | Implementation-local handoff | Public compatibility surface preserved |
| --- | --- | --- | --- |
| 001 | `External Material != External Orientation` | No shared type; recurring bounded-orientation result recognized across subsystem-local artifacts | Existing inquiry, source navigation, bounded ask, operational inventory, and diagnostic inventory surfaces |
| 002 | `Inquiry Note Preservation != Inquiry Orientation Composition` | `_InquiryOrientationCompositionRequest` from `_prepare_inquiry_orientation_composition(...)` | `InquiryOrientationView` and `format_inquiry_orientation(...)` |
| 003 | `Source Navigation Query Intake != Source Navigation Composition` | `_PreparedSourceNavigationQuery` from `_prepare_source_navigation_query(...)` | `SourceNavigationView` and source-navigation rendering/JSON behavior |
| 004 | `Question Family Text Intake != Bounded Work Eligibility` | `_QuestionFamilyEligibilityInput` from `_prepare_question_family_eligibility_input(...)` | Existing bounded ask CLI orchestration and bounded work result shapes |
| 005 | `CLI Surface Intake != Operational Surface Classification` | `_CliSurfaceClassificationInput` from `_prepare_cli_surface_classification_inputs(...)` | `OperationalSurfaceClassificationAudit` and related rendering/JSON behavior |
| 006 | `Diagnostic Surface Intake != Diagnostic Inventory Composition` | `_DiagnosticInventoryCompositionInput` from `_prepare_diagnostic_inventory_composition(...)` | `diagnostic_inventory_json(...)` and `format_diagnostic_inventory(...)` |

## Recurring implementation physiology

Every recovered slice follows the same implementation physiology:

```text
External material

↓

Private preparation / handoff

↓

Existing bounded implementation owner

↓

Existing public compatibility surface
```

Implementation evidence:

- Inquiry orientation preserves raw notes separately, prepares `_InquiryOrientationCompositionRequest`, composes private answer/evidence, then returns the unchanged `InquiryOrientationView`.
- Source navigation strips the external query and projects fact support rows into `_PreparedSourceNavigationQuery`, then composes `SourceNavigationView`.
- Question-family bounded ask prepares exact inventory-backed question-family text into `_QuestionFamilyEligibilityInput`, then consumes it for bounded eligibility before existing selection/dispatch.
- Operational surface classification prepares parser and registration material into `_CliSurfaceClassificationInput`, then classifies and emits the existing audit item shape.
- Diagnostic inventory prepares diagnostic declarations into `_DiagnosticInventoryCompositionInput`, then composes existing JSON/table inventory output.

No recovered slice introduced a shared runtime artifact, generic orientation engine, schema change, event-ledger behavior, CLI flag, or public output-shape change.

## Recovery assessment

### Has every recurring implementation-local preparation/composition boundary currently visible beneath External Orientation been recovered?

Yes, for the currently surveyed External Orientation neighborhood.

The six recovered members cover every recurring implementation-local seam that is directly evidenced in the reviewed slices and their touched implementation:

1. raw inquiry note preservation to inquiry-orientation composition;
2. source-navigation query intake to source-navigation composition;
3. question-family text intake to bounded work eligibility;
4. CLI/parser surface intake to operational surface classification;
5. diagnostic declaration intake to diagnostic inventory composition; and
6. the family-level recognition that external/manual/diagnostic/operator material is bounded before downstream use.

No additional implementation-supported External Orientation seam is visible at the same recurring level without crossing into a neighboring owner. The remaining visible seams either belong inside already bounded owners, or belong to neighboring families listed below.

### Implementation-supported remaining seams that still belong to External Orientation

None identified.

There is remaining local pressure inside several owners, but it is not evidence of another unrecovered External Orientation boundary. It is evidence of bounded owner internals or neighboring-family bridges.

## Consistency assessment

### Did every recovered slice preserve the same implementation physiology?

Yes.

All recovered slices preserve the same pattern: externally supplied or externally declared material is admitted into a private, narrow handoff artifact/helper, then consumed by an existing bounded implementation owner, which preserves the previous public compatibility surface.

### Outliers

No constitutional outlier was found.

Minor local variation exists but does not break the family physiology:

- Slice 001 is an architectural recognition slice and therefore does not add a private helper or artifact.
- Slice 004 keeps `bounded_work_eligibility_for_question_family(...)` as a public compatibility helper that still constructs `_QuestionFamilyEligibilityInput` directly; the CLI path uses `_prepare_question_family_eligibility_input(...)` for exact inventory admission before eligibility.
- Slice 005 leaves operational surface inventory discovery separate from classification preparation; that is a neighboring operational visibility pressure, not an inconsistency in the recovered classification path.
- Slice 006 prepares declarations by tuple materialization only; the seam is intentionally small because the existing diagnostic declarations are already structured registry entries.

## Remaining implementation-local pressure inside External Orientation

Only implementation-supported pressure is listed here.

1. **Subsystem-local naming remains intentionally local.** The implementation has private handoff names per owner, but no shared `ExternalOrientationRequest`, `ExternalOrientationResult`, registry, taxonomy, or framework. Current evidence supports recurring physiology, not a shared runtime type.

2. **Question-family eligibility has two entry shapes.** The CLI route performs exact inventory admission through `_prepare_question_family_eligibility_input(...)`, while `bounded_work_eligibility_for_question_family(...)` remains a compatibility helper that constructs `_QuestionFamilyEligibilityInput` directly. This is compatibility pressure, not evidence for a new abstraction.

3. **Operational visibility has adjacent discovery and coverage composition.** `build_operational_surface_inventory(...)` still discovers operational surfaces from argparse, while `build_visibility_coverage_audit(...)` combines inventory and classification outputs. That pressure sits at the bridge to Operational Visibility rather than inside External Orientation recovery.

4. **Source navigation still contains explanation subcomposition.** Definition, dependency, support, and non-claim explanations are composed inside the bounded source-navigation owner. This is internal Source Navigation pressure, not another external query-intake seam.

5. **Inquiry orientation still contains evidence and answer composition internals.** `_collect_inquiry_orientation_evidence(...)` and `_compose_inquiry_orientation_answer(...)` remain private owner internals after the preservation-to-composition handoff. This is Inquiry/Orientation pressure, not unrecovered external-material intake.

6. **Diagnostic shape-audit ownership remains separate.** Diagnostic inventory composition is recovered, but diagnostic shape-audit implementation specs and checks are separate diagnostic visibility ownership. The recovered family should not absorb them.

## Bridge inspection

This inspection stands on the edge of the recovered family and does not cross into implementation recovery.

### Orientation / Inquiry Orientation

- **Bridge observed?** Yes.
- **Implementation evidence?** `build_inquiry_orientation(...)` consumes a preserved note through `_prepare_inquiry_orientation_composition(...)`, then composes evidence and answer before returning `InquiryOrientationView`.
- **Current pressure?** Evidence collection and answer composition remain local private responsibilities after the external-material handoff.
- **Recovered?** Partially, only the External Orientation edge is recovered.
- **Unknown?** Whether generic Orientation exists as a constitutional family remains unknown; current implementation does not justify a generic orientation framework.
- **Constitutional readiness:** Preserved unknown. No new coordinated campaign is earned solely by this audit.

### Source Navigation

- **Bridge observed?** Yes.
- **Implementation evidence?** `_prepare_source_navigation_query(...)` hands normalized query and projected rows to `_compose_source_navigation(...)`, which composes definitions, imports, repository-artifact definitions, dependency mentions, support explanations, and non-claims.
- **Current pressure?** Explanation subcomposition is dense inside source navigation.
- **Recovered?** The query-intake edge is recovered. The broader Source Navigation owner is not recovered by this family.
- **Unknown?** Whether source-navigation explanation internals require their own campaign remains unknown from this audit.
- **Constitutional readiness:** Preserved unknown.

### Question Eligibility / Bounded Ask

- **Bridge observed?** Yes.
- **Implementation evidence?** `_prepare_question_family_eligibility_input(...)` prepares exact inventory-backed question-family text; `_bounded_work_eligibility_for_prepared_question_family(...)`, `bounded_work_selection_for_question_family(...)`, `bounded_work_dispatch_request_for_selection(...)`, and `execute_bounded_work_dispatch(...)` remain distinct bounded ask stages.
- **Current pressure?** Eligibility, selection, dispatch-request construction, and dispatch execution are already explicit, while CLI orchestration still coordinates presentation and surface-argument validation.
- **Recovered?** The question-family intake-to-eligibility edge is recovered.
- **Unknown?** Whether bounded ask orchestration needs a separate campaign is unknown; existing stages are already explicit enough that this audit does not earn a new campaign.
- **Constitutional readiness:** Preserved unknown.

### Operational Visibility

- **Bridge observed?** Yes.
- **Implementation evidence?** `_prepare_cli_surface_classification_inputs(...)` prepares CLI/parser material for classification; `build_operational_surface_inventory(...)` separately discovers inventory surfaces; `build_visibility_coverage_audit(...)` combines inventory and classification results.
- **Current pressure?** Discovery, classification, registration, and coverage visibility are adjacent and partially separate.
- **Recovered?** The CLI surface intake-to-classification edge is recovered.
- **Unknown?** The broader Operational Visibility family remains outside this recovery.
- **Constitutional readiness:** Preserved unknown. The implementation shows a bridge, but this audit should not recommend a campaign without a concrete failing visibility gap.

### Diagnostic Visibility

- **Bridge observed?** Yes.
- **Implementation evidence?** `_prepare_diagnostic_inventory_composition(...)` prepares diagnostic declarations for inventory JSON/table composition; diagnostic shape-audit specs remain in `seed_runtime.diagnostic_shape_audit` and are referenced by question-surface inventory and tests.
- **Current pressure?** Diagnostic inventory, diagnostic shape audit, record scope, ledger-write declarations, and cluster-mutation declarations remain a dense visibility family.
- **Recovered?** The diagnostic surface intake-to-inventory composition edge is recovered.
- **Unknown?** Whether diagnostic shape audit or diagnostic recording deserves another campaign is unknown absent a specific implementation gap.
- **Constitutional readiness:** Preserved unknown.

### Inquiry

- **Bridge observed?** Yes.
- **Implementation evidence?** `record_inquiry_note(...)`, `load_inquiry_notes(...)`, and `select_inquiry_note(...)` preserve externally supplied inquiry notes outside the event ledger before orientation composition consumes selected notes.
- **Current pressure?** Inquiry note storage, selection, and orientation consumption are adjacent but already separated at the preservation/composition boundary.
- **Recovered?** Only the External Orientation bridge from preserved note to orientation composition is recovered.
- **Unknown?** A broader Inquiry family remains unknown.
- **Constitutional readiness:** Preserved unknown.

### State Visibility / Projected Read Models

- **Bridge observed?** Yes.
- **Implementation evidence?** Inquiry orientation and source navigation both consume projected `State` material and fact supports, while diagnostic and operational visibility declare whether projected state is used.
- **Current pressure?** External Orientation depends on existing projected read models but does not own projection, truth, mutation, or state construction.
- **Recovered?** Not recovered by this family.
- **Unknown?** Whether State Visibility has already earned a new campaign is unknown from this audit.
- **Constitutional readiness:** Preserved unknown.

### Pressure / Observation

- **Bridge observed?** Weakly.
- **Implementation evidence?** Question-surface mappings include operational pressure and observation-domain/permission families, and diagnostic entries mention observation and projected-state surfaces.
- **Current pressure?** Only mapping/visibility adjacency is evidenced here; no External Orientation implementation seam points directly into pressure or observation internals.
- **Recovered?** No.
- **Unknown?** Yes. These remain constitutional unknowns for this audit.
- **Constitutional readiness:** Preserved unknown.

## Neighboring recovered families

No neighboring family is recovered by this audit.

Recovered External Orientation edges expose neighboring foundations, but this deliverable does not cross the bridge. The only recovered family assessed here is External Orientation.

## Neighboring unknowns

The following neighboring foundations are visible but remain constitutional unknowns:

- generic Orientation;
- Source Navigation explanation ownership;
- Bounded Ask orchestration beyond exact question-family eligibility;
- Operational Visibility discovery/coverage ownership;
- Diagnostic Visibility shape-audit/recording ownership;
- broader Inquiry ownership;
- State Visibility / projected read-model ownership;
- Pressure and Observation ownership where only mapped visibility adjacency is currently evidenced.

## Constitutional readiness

### Has implementation already earned a new coordinated slice campaign?

No.

The implementation has earned recognition that the External Orientation construction crew has finished the currently surveyed neighborhood. It has not, by this audit alone, earned a new coordinated campaign in a neighboring family.

The strongest bridges are Operational Visibility and Diagnostic Visibility, because their implementation surfaces are dense and repeatedly adjacent to the recovered family. However, the repository instructions require implementation evidence and discourage speculative campaigns. This audit identifies those bridges as visible foundations, not as campaign authorizations.

### Should observed bridges remain preserved unknowns?

Yes.

All neighboring bridges should remain preserved unknowns until a concrete failing command, visibility gap, diagnostic/audit shape gap, or implementation-local compression demonstrates that a neighboring owner needs recovery.

## Recommended next campaign

No next campaign is recommended from this completion audit.

If future work discovers a concrete failing command or visibility gap, the most implementation-adjacent candidates to re-evaluate would be Diagnostic Visibility or Operational Visibility. That is not a recommendation to start those campaigns now; it is only a note that those bridges are the most visible from the completed External Orientation edge.

## Confidence

High for the completion answer inside the surveyed External Orientation family.

Medium for bridge readiness, because this audit intentionally does not cross into neighboring implementations and therefore preserves unknowns where evidence is adjacent but not decisive.

## Acceptance answer

Yes: the External Orientation construction crew has finished the currently surveyed neighborhood.

The neighboring foundations now visible are Orientation/Inquiry Orientation, Source Navigation, Question Eligibility/Bounded Ask, Operational Visibility, Diagnostic Visibility, Inquiry, State Visibility, and weak Pressure/Observation adjacency.

No remaining beams were identified that still belong to the External Orientation family at the same recurring preparation/composition level.

No bridge is implementation-earned as a new coordinated campaign by this audit. All observed bridges remain constitutional unknowns until repository evidence exposes a concrete neighboring-family recovery need.
