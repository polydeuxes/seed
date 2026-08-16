# Inquiry Frontier Boundary Testimony Audit 001

## Question

Determine which existing repository owners may lawfully testify to frontier-boundary clauses for one exact selected inquiry need and one exact bounded advancement horizon:

```text
selected inquiry need
+
stage-owned frontier-boundary testimony
→ InquiryFrontierBoundaryTestimony
```

This audit is read-only. It does not formulate a question, assemble a frontier, select sources or observations, authorize access, open inquiry, execute, record, write the event ledger, or mutate state.

## Guardrails preserved

```text
goal-horizon scope
!= inquiry scope automatically

uncertainty subject
!= sufficient-resolution criterion

visible evidence
!= admitted inquiry evidence

stale or unavailable evidence
!= stopping condition automatically

frontier-boundary testimony
!= BoundedInquiryFrontier
!= constitutional question
!= inquiry opening
```

The testimony must be explicit, stage-owned, provenance-preserving, and bound to the exact inquiry need, native uncertainty component, subject, goal, and horizon. Clauses may not be inferred from wording similarity, generic sufficiency conditions, evidence snapshots, absent artifacts, or broad admission precedent.

## Evidence reviewed

- `seed_runtime/advancement_need_consideration_selection.py`
- `seed_runtime/advancement_need_reference_set.py`
- `seed_runtime/goal_advancement_need_set.py`
- `seed_runtime/inquiry_need_projection.py`
- `seed_runtime/bounded_advancement_horizon.py`
- `seed_runtime/bounded_operator_goal_establishment.py`
- `seed_runtime/inquiry_artifacts.py`
- `seed_runtime/repository_observation.py`
- `seed_runtime/knowledge/repository_observation.py`
- `seed_runtime/knowledge/documentation_observation.py`
- `seed_runtime/knowledge/relationship_observation.py`
- `seed_runtime/knowledge/observation_agreement.py`
- `seed_runtime/facts.py`
- `inquiry_need_projection_audit_001.md`
- `clarification_need_projection_audit_001.md`
- `authority_need_projection_audit_001.md`
- `constitutional_bounded_investigation_characterization.md`
- `independent_testimony_boundary_investigation.md`
- `constitutional_authority_volume_boundary_investigation.md`

## Current implementation boundary

### Selected inquiry need

`AdvancementNeedConsiderationSelection` selects one exact visible advancement-need reference from explicit focus evidence. Its boundary notes require the focus to match the same need set, selected goal, bounded horizon, need family, native projection, and native record lineage. The selected need is explicitly not a primary blocker, resolution, next action, realization, inquiry opening, authority request, authorization, execution, recording, event-ledger write, or mutation.

For this audit, the selected inquiry need is lawful only when:

1. `AdvancementNeedConsiderationSelection.selection_state == "selected"`;
2. `selected_reference.family` is `inquiry` or `inquiry_need`;
3. `selected_reference.native_projection_id` equals the consumed `InquiryNeedProjection.projection_id`;
4. `selected_reference.native_lineage` identifies exactly one `InquiryNeedProjectionItem`;
5. the selected reference's need set, selected goal, and horizon ids match the active need set, goal, and horizon.

The selection owner testifies only to exact need-reference selection. It does not establish inquiry scope, admit evidence, set sufficient resolution, create stopping conditions, or open inquiry.

### Native inquiry item

`InquiryNeedProjection` is the native inquiry-need owner. It consumes explicit component-bounded repository/world uncertainty testimony and preserves standings separately from evidence freshness and availability. It validates selection, goal, horizon, evidence identity, repository/world family, stage ownership, component boundedness, subject presence, materiality to the present movement boundary, and mixed/non-inquiry exclusions before classifying an item.

For frontier-boundary testimony, the selected native item may supply only:

- native projection id;
- native item lineage or testimony ref;
- bounded uncertainty component ref;
- repository/world subject ref;
- owning stage;
- standing;
- evidence ref;
- freshness and availability status.

It does not supply included inquiry scope, excluded inquiry scope, admissible evidence territory, sufficient-resolution conditions, or lawful stopping conditions by itself.

### Bounded horizon

`BoundedAdvancementHorizon` binds one selected goal to a present movement boundary, included and excluded goal-horizon scope, evidence snapshot refs, time and current-state bounds, potentially relevant and explicitly excluded need families, Unknowns, conflicts, stale evidence, and unavailable evidence. It explicitly refuses need classification, sufficiency judgment, action selection, inquiry opening, authority request, realization selection, scheduling, work authorization, execution, recording, event-ledger writing, and cluster mutation.

For frontier-boundary testimony, the horizon may bind testimony to the current goal and movement boundary and may provide candidate references that clauses must cite. The horizon does not automatically convert goal-horizon included scope into inquiry included scope, goal-horizon excluded scope into inquiry excluded scope, evidence snapshots into admitted evidence territory, stale or unavailable evidence into stop conditions, or sufficiency fields into inquiry resolution criteria.

## Owners that may establish included and excluded inquiry-scope clauses

No reviewed implementation owner currently performs the complete `InquiryFrontierBoundaryTestimony` responsibility. Existing owners may testify only to narrower inputs.

| Existing owner | May testify | Cannot testify |
| --- | --- | --- |
| `AdvancementNeedConsiderationSelection` | Exact selected inquiry need reference and native lineage. | Inquiry scope clauses, evidence admission, sufficient resolution, stopping conditions. |
| `InquiryNeedProjectionItem` | The native uncertainty component, repository/world subject, owning stage, standing, evidence ref, freshness, and availability for the selected need. | Lawful inquiry scope or resolution criteria beyond the component/subject already projected. |
| Original `RepositoryWorldUncertaintyTestimony` consumed by `InquiryNeedProjection` | Component-bounded repository/world uncertainty and horizon materiality, if its refs match the selected native item. | Frontier scope unless it explicitly owns frontier-boundary clause testimony. |
| `BoundedAdvancementHorizon` | Goal/horizon binding, present movement boundary, goal-horizon included/excluded scope, time/current-state bounds, evidence snapshot refs, excluded need families. | Inquiry scope automatically; sufficiency judgment; evidence admission; stop authority. |
| `BoundedOperatorGoalEstablishment` | Goal-owned scope, unresolved scope, sufficiency conditions, stop conditions, Unknowns, ambiguities, conflicts, and ingress lineage for the selected goal. | Inquiry-scope clauses unless a clause explicitly cites a goal-owned condition as the reason a frontier boundary is included/excluded. |
| Repository/documentation/relationship observation owners | Observed repository/documentation/relationship facts within their adapter boundaries. | Inquiry-scope inclusion/exclusion; source selection; access authorization; frontier assembly. |
| `InquiryArtifactVisibility` | Visibility that inquiry artifacts of categories such as unknown, boundary, pressure, finding, supported/unsupported conclusion, open question, and gap exist. | Inquiry movement, graph creation, pressure transformation, workflow, planning, frontier construction, or admission by visibility. |

A lawful included or excluded inquiry-scope clause therefore requires a new explicit clause-level testimony record whose owning stage says, for the exact selected native uncertainty component and subject, that a named scope item is included or excluded from the inquiry frontier boundary. Existing horizon or goal scope can be cited as provenance, but it cannot be copied across automatically.

Minimum fields for an included/excluded inquiry-scope clause:

- `clause_ref`;
- `clause_kind` of `included_inquiry_scope` or `excluded_inquiry_scope`;
- `selection_id` from the selected inquiry need selection;
- `need_reference_id` from the selected inquiry need reference;
- `native_projection_id` from `InquiryNeedProjection`;
- `native_item_ref` / `native_lineage` / `testimony_ref` matching the selected item;
- `bounded_uncertainty_component_ref`;
- `repository_world_subject_ref`;
- `goal_establishment_id`;
- `horizon_id`;
- `present_movement_boundary_ref` or exact boundary text;
- `owning_stage` and `stage_owns_frontier_boundary_clause=True`;
- `scope_item_ref`;
- `scope_basis_refs` preserving provenance;
- `clause_standing` such as `established`, `unsupported`, `unknown`, `conflicting`, `stale`, `unavailable`, or `out_of_scope`.

## Owners that may admit evidence territory without selecting sources

Evidence territory is not a selected source list. It is a boundary over categories, refs, provenance classes, or admissibility constraints that later source or observation selection must obey.

Existing owners may contribute only as follows:

| Existing owner | Evidence-territory role | Boundary |
| --- | --- | --- |
| `BoundedAdvancementHorizon.evidence_snapshot_refs` | Candidate evidence refs and snapshot states that may be cited by a territory clause. | Snapshot visibility is not admission. |
| `InquiryNeedProjectionItem.evidence_ref` | The native evidence ref supporting the selected uncertainty item. | Item evidence is not the whole admissible territory. |
| Repository/documentation/relationship observation owners | Territory can refer to their fact classes only if the clause says those classes are admissible for this inquiry boundary. | Observation owners do not select future sources or authorize access. |
| `ObservationAgreement` / fact-support owners | Territory can include support/agreement/disagreement record classes when explicitly admitted. | Agreement, confidence, contradiction, or support summaries do not resolve sufficiency automatically. |
| `BoundedOperatorGoalEstablishment` | Goal-owned acceptance, sufficiency, or stop-condition provenance may constrain admissible territory. | Goal conditions do not admit evidence by themselves. |
| Prior inquiry artifacts | May preserve boundary, finding, unsupported conclusion, Unknown, pressure, open question, or gap artifact refs as possible territory. | Artifact visibility is not admitted evidence. |

A lawful admissible-evidence-territory clause must say what territory is admissible and what territory is excluded or not-yet-admitted, while refusing to name selected sources or observations. It must preserve provenance to the selected native item and horizon and must leave source selection, observation authorization, execution, and recording outside its boundary.

Minimum fields:

- `clause_ref`;
- `clause_kind="admissible_evidence_territory"`;
- selected need, native item, subject, goal, and horizon bindings;
- `territory_ref` or `territory_description`;
- `admitted_evidence_classes` or `admitted_ref_patterns`;
- `excluded_evidence_classes` or `not_admitted_ref_patterns`;
- `basis_refs` including horizon evidence refs, native item evidence refs, goal condition refs, or observation/fact-support refs;
- `does_not_select_sources=True`;
- `does_not_authorize_observation=True`;
- `standing` with preserved unknown/conflict/stale/unavailable/out-of-scope states.

## Evidence that establishes sufficient-resolution conditions

Sufficient-resolution conditions are not the same as an uncertainty subject and are not imported from generic goal sufficiency. They are inquiry-boundary criteria stating what resolution would be enough to stop the frontier-boundary-covered inquiry without opening or executing the inquiry in this artifact.

Existing evidence can support such conditions only when clause-level testimony explicitly binds it:

1. Goal-owned sufficiency conditions in `BoundedOperatorGoalEstablishment`, if the testimony says which condition constrains this selected inquiry need.
2. Horizon `present_movement_boundary`, time bounds, current-state bounds, and evidence snapshot refs, if the testimony says what resolution is needed to cross this exact boundary.
3. Native `InquiryNeedProjectionItem` component and subject, if the testimony states what resolved standing or support state would answer that exact component.
4. Fact-support, observation-agreement, repository/documentation/relationship observation, or inquiry-artifact evidence, if the testimony admits the class and states what level of support, contradiction handling, currentness, or provenance preservation is sufficient.

A sufficient-resolution clause should preserve:

- `resolution_condition_ref`;
- exact selected need and native item bindings;
- `condition_subject_ref` matching or explicitly related to `repository_world_subject_ref`;
- `required_resolution_state`, such as supported, unsupported-with-boundary, contradiction-preserved, unavailable-preserved, or Unknown-preserved;
- `required_provenance_refs`;
- `required_currentness` where relevant;
- `basis_refs` to goal/horizon/native item/evidence-support testimony;
- `not_a_sufficiency_judgment=True` for this boundary artifact;
- standing for missing, ambiguous, conflicting, stale, unavailable, or out-of-scope testimony.

## Evidence that establishes lawful stopping conditions

Lawful stopping conditions are explicit inquiry-boundary stops. They are not automatically created by stale evidence, unavailable evidence, absent artifacts, visible evidence, generic Unknowns, or execution impossibility.

Existing evidence can support a stop condition only through stage-owned clause testimony:

1. Goal-owned stop conditions may constrain a frontier boundary when explicitly tied to the selected inquiry need and horizon.
2. Horizon bounds may provide a stop basis when the testimony says crossing the present movement boundary is no longer supported or the need family/scope is excluded for a reason.
3. Native inquiry item standings may provide stop bases such as unsupported, unknown, conflicting, excluded-family, stale, or unavailable only when the testimony says that preservation state is a lawful stop for this inquiry boundary.
4. Observation/fact-support/agreement evidence may provide stop bases when contradiction, insufficient support, unavailable currentness, or out-of-scope territory is explicitly admitted as a stop condition for the selected inquiry need.

A lawful-stopping-condition clause should preserve:

- `stopping_condition_ref`;
- selected need/native item/subject/goal/horizon bindings;
- `stop_kind`, such as sufficient_resolution_reached, out_of_scope, contradiction_preserved, unavailable_evidence_preserved, stale_evidence_preserved, authority_boundary_encountered, excluded_family, unsupported_boundary, or unknown_preserved;
- `stop_basis_refs`;
- `requires_no_frontier_assembly=True` for this testimony artifact;
- `does_not_close_goal=True` unless a separate goal owner says otherwise;
- `does_not_open_or_execute_inquiry=True`;
- standing for missing, ambiguous, conflicting, stale, unavailable, or out-of-scope testimony.

## Binding contract for every clause

Every frontier-boundary clause must bind stricter than lexical similarity:

1. **Selected-need binding:** `AdvancementNeedConsiderationSelection.selection_state == "selected"`, the selected reference is inquiry-family, and the clause names `selection_id` plus `need_reference_id`.
2. **Native projection binding:** the clause names the same `InquiryNeedProjection.projection_id` and native lineage/testimony ref as the selected inquiry reference.
3. **Component binding:** the clause names the same `bounded_uncertainty_component_ref` as the selected native inquiry item, or a declared component relation explicitly joins them.
4. **Subject binding:** the clause names the same `repository_world_subject_ref`, or a declared subject relation explicitly joins them.
5. **Goal binding:** the clause names the same `goal_establishment_id` as the native projection and horizon.
6. **Horizon binding:** the clause names the same `horizon_id` and identifies the present movement boundary it constrains.
7. **Evidence binding:** basis refs must be in the horizon evidence refs, the native item evidence ref, or an explicitly preserved upstream testimony/provenance ref.
8. **Stage ownership:** the clause has an owning stage that explicitly owns frontier-boundary testimony for that clause kind.
9. **Family separation:** clarification, authority, and operational-realization material is excluded or preserved separately unless explicitly joined by its own owner.

Failure of any binding does not create a weaker implicit clause. It creates preserved missing, ambiguous, conflicting, stale, unavailable, out-of-scope, unsupported, or unclassified testimony.

## Preservation rules

| Condition | Preservation |
| --- | --- |
| Missing testimony | Preserve `missing_frontier_boundary_testimony` for the affected clause kind and binding dimension. Do not infer from horizon scope, native subject, visible evidence, or absent artifacts. |
| Ambiguous testimony | Preserve candidate clause refs and ambiguity basis. Do not choose the broader, narrower, or more convenient clause. |
| Conflicting testimony | Preserve all conflicting clause refs, owning stages, and conflict dimensions. Do not rank owners without an explicit conflict-resolution owner. |
| Stale testimony | Preserve stale status and stale basis. Do not treat stale as exclusion, stop, or admissibility failure unless a clause says so. |
| Unavailable testimony | Preserve unavailable status and unavailable basis. Do not treat unavailable as stop or out-of-scope unless a clause says so. |
| Out-of-scope testimony | Preserve the out-of-scope clause and the boundary it exceeded. Do not import it into included inquiry scope or admissible territory. |
| Non-inquiry or mixed testimony | Preserve as adjacent-family or mixed component. Do not collapse clarification, authority, or realization into inquiry frontier scope. |
| Visible but not admitted evidence | Preserve visibility separately from admitted territory. Do not treat visibility as evidence admission. |

## May one artifact preserve all frontier-boundary clauses without assembling the frontier?

Yes. One read-only `InquiryFrontierBoundaryTestimony` artifact may preserve included inquiry scope, excluded inquiry scope, admissible evidence territory, sufficient-resolution conditions, lawful stopping conditions, and preservation states for missing/ambiguous/conflicting/stale/unavailable/out-of-scope testimony without assembling a `BoundedInquiryFrontier`.

The artifact must be clause-preserving rather than frontier-constructing. It may hold clause records, bindings, basis refs, standings, and negative flags. It must not create ordered frontier nodes, select sources, select observations, authorize access, open inquiry, decide sufficiency has been met, execute, record, write the event ledger, or mutate state.

## Does an existing owner already perform this responsibility?

No reviewed owner already performs the exact `InquiryFrontierBoundaryTestimony` responsibility.

Adjacent owners stop earlier:

- `AdvancementNeedConsiderationSelection` selects an exact visible need reference only.
- `InquiryNeedProjection` establishes inquiry need from explicit repository/world uncertainty testimony only.
- `BoundedAdvancementHorizon` binds the present movement horizon and explicitly refuses need classification and sufficiency judgment.
- Observation, fact-support, agreement, and inquiry-artifact visibility owners preserve evidence or artifact facts but do not admit evidence territory for a selected inquiry frontier boundary.
- Goal establishment can preserve goal sufficiency and stop conditions, but it does not convert them into inquiry-specific sufficient-resolution or lawful-stopping clauses.

## Smallest missing responsibility

The smallest missing responsibility is a read-only clause-preservation owner that consumes:

```text
AdvancementNeedConsiderationSelection(selected inquiry need)
+
matching InquiryNeedProjection
+
matching InquiryNeedProjectionItem / RepositoryWorldUncertaintyTestimony lineage
+
matching BoundedOperatorGoalEstablishment
+
matching BoundedAdvancementHorizon
+
explicit stage-owned frontier-boundary clause testimony
```

and emits only:

- selected need binding;
- native inquiry item, component, subject, goal, and horizon binding;
- included inquiry-scope clauses;
- excluded inquiry-scope clauses;
- admissible evidence territory clauses that do not select sources;
- sufficient-resolution condition clauses that do not judge sufficiency;
- lawful stopping condition clauses that do not open or close inquiry by themselves;
- missing, ambiguous, conflicting, stale, unavailable, out-of-scope, adjacent-family, unsupported, and unclassified preservation;
- read-only/no-action flags.

## Is one read-only implementation slice warranted?

Yes, one narrow read-only implementation slice is warranted if Seed needs this boundary to become executable after selected inquiry need and inquiry-need projection. The slice should be smaller than `BoundedInquiryFrontier`, constitutional question formulation, inquiry opening, source selection, observation selection, access authorization, execution, recording, or state mutation.

A safe first slice would add:

- `seed_runtime/inquiry_frontier_boundary_testimony.py`;
- dataclasses for `InquiryFrontierBoundaryClauseTestimony`, `InquiryFrontierBoundaryClause`, and `InquiryFrontierBoundaryTestimony`;
- a projector that validates selected-need, native projection, native item, component, subject, goal, horizon, evidence, and stage-owner joins;
- standings for `established`, `unsupported`, `unknown`, `conflicting`, `stale`, `unavailable`, `out_of_scope`, `adjacent_family`, and `unclassified`;
- explicit negative flags for no frontier assembly, no question formulation, no source/observation selection, no authorization, no inquiry opening, no execution, no recording, no event-ledger write, no cluster mutation, and no sufficiency judgment;
- tests proving horizon scope is not inquiry scope automatically, native subject is not sufficient-resolution criterion automatically, visible evidence is not admitted territory automatically, stale/unavailable evidence is not a stopping condition automatically, and one artifact can preserve all clause families without assembling a frontier.

Because this would be a library/read-model artifact rather than a public diagnostic CLI surface, it need not update diagnostic inventory or diagnostic shape-audit registries unless a diagnostic, audit, probe, view, CLI flag, or recordable output is added.

## Exact next bounded question

```text
What is the minimal read-only `InquiryFrontierBoundaryTestimony` artifact that consumes one selected inquiry-family `AdvancementNeedConsiderationSelection`, the matching `InquiryNeedProjection` native item, the matching `BoundedOperatorGoalEstablishment`, the matching `BoundedAdvancementHorizon`, and explicit stage-owned frontier-boundary clause testimony, preserves included inquiry scope, excluded inquiry scope, admissible evidence territory, sufficient-resolution conditions, lawful stopping conditions, and missing/ambiguous/conflicting/stale/unavailable/out-of-scope testimony without formulating a question, assembling a `BoundedInquiryFrontier`, selecting sources or observations, authorizing access, opening inquiry, judging sufficiency, executing, recording, or mutating state?
```

## Conclusion

The lawful frontier-boundary testimony owner is not currently implemented. Existing owners can bind the selected inquiry need, native uncertainty component, subject, goal, horizon, evidence refs, and adjacent evidence classes, but no current owner explicitly preserves all frontier-boundary clauses. The smallest missing responsibility is a read-only clause testimony artifact that preserves included/excluded inquiry scope, admissible evidence territory, sufficient-resolution conditions, lawful stopping conditions, and preservation states without assembling or opening the inquiry frontier.

Inquiry frontier boundary testimony audit complete.
