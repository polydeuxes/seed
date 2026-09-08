# Bounded Inquiry Frontier Audit 001

## Question

Determine what evidence lawfully establishes a bounded inquiry frontier from one exact selected inquiry need:

```text
AdvancementNeedConsiderationSelection(inquiry)
+
native inquiry-need evidence
+
BoundedAdvancementHorizon
→ BoundedInquiryFrontier
```

Repository authority wins. This audit is documentary only. It does not formulate a constitutional question, select evidence sources, select observations, authorize access, open inquiry, begin examination, judge inquiry results, execute, record, write the event ledger, or mutate state.

## Guardrails preserved

```text
selected inquiry need
!= inquiry frontier established

inquiry frontier
!= constitutional question

frontier scope
!= evidence source selected

stopping boundary
!= conclusion already known

frontier established
!= inquiry opened
!= observation authorized
```

The frontier must not be derived from wording similarity, generic goal sufficiency, family labels, absent evidence, or the mere fact that an inquiry need was selected for consideration.

## Evidence reviewed

- `seed_runtime/advancement_need_consideration_selection.py`
- `seed_runtime/advancement_need_reference_set.py`
- `seed_runtime/inquiry_need_projection.py`
- `seed_runtime/bounded_advancement_horizon.py`
- `seed_runtime/goal_advancement_need_set.py`
- `advancement_need_consideration_selection_audit_001.md`
- `inquiry_need_projection_audit_001.md`
- `bounded_advancement_horizon_slice_001.md`
- `goal_advancement_need_evidence_topology_audit_001.md`
- `advancement_need_family_coverage_audit_001.md`
- `constitutional_admission_family_characterization.md`
- `constitutional_artifact_competency_survey.md`
- `independent_testimony_boundary_investigation.md`

## Existing artifacts that may supply frontier-boundary testimony

### `AdvancementNeedConsiderationSelection`

`AdvancementNeedConsiderationSelection` may testify only that explicit focus evidence selected one exact visible advancement-need reference for consideration. It preserves the `reference_set_id`, `need_set_id`, selected goal identity, horizon identity, focus evidence refs, provenance refs, selection state, selected reference, visible references, non-selected references, ambiguity, missing identity, mismatches, absent references, duplicate-lineage conflicts, non-selectable references, Unknowns, conflicts, and negative authority flags.

For this frontier, it can supply selected-need identity only if:

1. `selection_state` is `selected`;
2. the selected reference exists;
3. the selected reference family is `inquiry`;
4. the selected reference is selectable;
5. the selection, need-set, goal, horizon, family, native projection, and native lineage match the other boundary inputs.

It cannot supply inquiry scope, stopping conditions, evidence territory, source selection, observation authorization, constitutional-question text, conclusion, or examination result.

### `AdvancementNeedReferenceSet`

`AdvancementNeedReferenceSet` may testify to the visible native item reference identity. It binds one reference to the need set, selected goal, horizon, family, native projection, native lineage, native bucket, native standing, evidence refs, evidence quality, visibility, selectability, and duplicate-lineage conflict state.

For this frontier, it can supply the bridge from the selected reference back to a native inquiry projection item. It does not classify inquiry frontier scope. It does not select a source, prioritize a need, route work, open inquiry, or mutate state.

### `InquiryNeedProjection`

`InquiryNeedProjection` is the native inquiry-need owner. Its established item preserves:

- the testimony reference;
- source reference;
- bounded uncertainty component reference;
- repository/world subject reference;
- owning stage;
- standing;
- evidence reference;
- evidence freshness;
- evidence availability;
- unclassified reason when refused.

For this frontier, it may supply the uncertainty component and subject requiring examination, but only through the exact native item selected via the advancement-need reference. It cannot alone establish the frontier because an inquiry need established is explicitly not inquiry opened, question selected, observation authorized, sufficiency judged, or execution begun.

### `RepositoryWorldUncertaintyTestimony`

The native testimony behind `InquiryNeedProjection` may supply the strongest frontier-boundary testimony if it is preserved and matches the selected item. It names the bounded uncertainty component, repository/world subject, owning stage, materiality to the present movement boundary, evidence freshness, and evidence availability.

For a lawful frontier, this testimony must be treated as boundary evidence, not as the future evidence source selected for examination. A testimony `source_ref` is provenance for why the need exists; it is not authorization to inspect that source again and not a selected observation path.

### `BoundedAdvancementHorizon`

`BoundedAdvancementHorizon` may supply the present advancement boundary, included scope, excluded scope, evidence snapshot references, time bounds, current-state bounds, potentially relevant need families, explicit family exclusions, Unknowns, conflicts, stale evidence refs, unavailable evidence refs, and read-only/no-mutation posture.

For this frontier, it binds inquiry need materiality to one present movement boundary. It does not classify needs, judge sufficiency, select a next action, open inquiry, authorize work, execute, record, or mutate state.

### `GoalAdvancementNeedSet`

`GoalAdvancementNeedSet` may supply the in-scope family assembly context: the selected goal, horizon, supplied native projections, absent families, excluded families, horizon Unknowns, horizon conflicts, horizon exclusions, and projection identity conflicts.

For this frontier, it helps prove that the selected inquiry reference belongs to a supplied inquiry projection in the current need set. It does not rank needs, declare an overall blocker, select a route, select a next action, judge sufficiency, open inquiry, request authority, authorize work, record, write the event ledger, or mutate cluster state.

### Admission, artifact, and independent-testimony precedent

The admission and artifact investigations supply methodological boundary testimony: bounded artifacts preserve evidence, provenance, authority boundary, negative authority, Unknowns, confidence, lawful stop, and non-promotion. Independent testimony requires source, provenance/support, scope/role, authority boundary, negative authority, Unknowns, confidence, and lawful stop to remain intact.

These artifacts support the shape of frontier preservation, but they do not themselves establish this specific inquiry frontier.

## What binds the frontier to the selected need, native inquiry item, goal, and horizon

A lawful `BoundedInquiryFrontier` must be conjunctively bound. The binding cannot be repaired by text similarity or inferred from uniqueness.

Minimum binding requirements:

1. **Selected-need binding:** The input `AdvancementNeedConsiderationSelection.selection_state` is `selected` and its `selected_reference` is present.
2. **Inquiry-family binding:** `selected_reference.family == inquiry`.
3. **Selectable standing binding:** The selected reference is selectable, which means it came from an established native record.
4. **Need-set binding:** `AdvancementNeedConsiderationSelection.need_set_id == selected_reference.need_set_id == GoalAdvancementNeedSet.need_set_id`.
5. **Selected-goal binding:** `AdvancementNeedConsiderationSelection.selected_goal_id == selected_reference.selection_id == GoalAdvancementNeedSet.selection_id == BoundedAdvancementHorizon.selection_id`.
6. **Goal-establishment binding:** `selected_reference.goal_establishment_id == GoalAdvancementNeedSet.goal_establishment_id == BoundedAdvancementHorizon.goal_establishment_id`.
7. **Horizon binding:** `AdvancementNeedConsiderationSelection.horizon_id == selected_reference.horizon_id == GoalAdvancementNeedSet.horizon_id == BoundedAdvancementHorizon.horizon_id`.
8. **Native projection binding:** the selected reference's `native_projection_id` matches the supplied `InquiryNeedProjection.projection_id` preserved in the inquiry family record of the need set.
9. **Native lineage binding:** the selected reference's inquiry lineage matches exactly one native `InquiryNeedProjectionItem` in `InquiryNeedProjection.established`.
10. **Evidence binding:** the native item's `evidence_ref` is among the horizon evidence snapshot refs unless the mismatch is preserved as unavailable, stale, conflicting, or Unknown boundary testimony rather than silently repaired.

If any binding fails, the frontier is not established. The output should preserve a refused or non-established frontier state with the exact mismatch, non-selected references, Unknowns, and conflicts.

## What distinguishes the uncertainty subject from inquiry scope

The uncertainty subject is the exact repository/world subject that requires examination. It is carried by the selected native inquiry item as `repository_world_subject_ref`, and it is tied to a bounded uncertainty component via `bounded_uncertainty_component_ref`.

Inquiry scope is the permitted conceptual boundary of future examination for resolving or bounding that selected uncertainty. It is not identical to the subject. A subject can be narrow while the scope includes contextual boundaries, comparison limits, horizon constraints, excluded areas, evidence quality checks, and stopping rules. Conversely, a broad subject does not authorize broad scope unless boundary testimony supports it.

A lawful frontier should therefore preserve both:

```text
uncertainty_subject_ref = selected native inquiry item.repository_world_subject_ref
uncertainty_component_ref = selected native inquiry item.bounded_uncertainty_component_ref
inquiry_scope_included = supported scope clauses derived from horizon scope + native testimony materiality
inquiry_scope_excluded = horizon excluded scope + family exclusions + negative authority + unsupported areas
```

The distinction prevents the frontier from turning a named subject into source selection, observation authorization, or a constitutional question. The subject says what uncertainty is at issue. Scope says what future inquiry may lawfully consider before a later owner opens inquiry, selects a question, or selects observations.

## Included and excluded inquiry scope

Included inquiry scope may be established only by explicit testimony from:

- the selected native inquiry item's bounded uncertainty component;
- the selected native inquiry item's repository/world subject;
- the owning stage named by the native item;
- the item's materiality to the present movement boundary;
- `BoundedAdvancementHorizon.included_scope`;
- `BoundedAdvancementHorizon.time_bounds`;
- `BoundedAdvancementHorizon.current_state_bounds`;
- horizon evidence snapshot references when used as available territory, not selected sources;
- explicit positive boundary testimony from a local owner.

Excluded inquiry scope must preserve:

- `BoundedAdvancementHorizon.excluded_scope`;
- explicit excluded need-family reasons if inquiry is excluded or partially excluded;
- non-inquiry components such as operator clarification, authority deficiency, or operational-realization deficiency;
- unsupported, unknown, conflicting, excluded-family, outside-current-scope, unclassified, and absent records;
- source selection, observation selection, access authorization, execution, recording, event-ledger writing, and mutation;
- constitutional-question formulation and conclusion judgment.

Scope may not be inferred from wording similarity between the selected need and a report title, from generic goal sufficiency, from the existence of a stale or unavailable evidence ref, or from absent downstream artifacts.

## Available evidence territory

Available evidence territory is the territory already visible as evidence context for the frontier. It is not a selected source list and not an observation plan.

Lawfully available territory includes:

- the selected need reference and its native lineage;
- the exact native inquiry item;
- the native item `evidence_ref` and `source_ref` as provenance;
- horizon `evidence_snapshot_refs` and their `evidence_state` notes;
- horizon stale and unavailable evidence refs as constraints;
- horizon Unknowns and conflicts;
- selected-need focus evidence refs and provenance refs;
- need-set family assembly context and projection identity conflicts;
- evidence freshness and availability from the native inquiry item.

The frontier should mark this as `available_evidence_territory`, not `selected_sources`. A later inquiry-opening or observation-selection owner would need separate authority to choose sources, observations, or access paths.

## Sufficiency and stopping boundaries

A bounded inquiry frontier does not know the conclusion. Stopping boundaries are the conditions under which a future inquiry would have enough boundary-respecting evidence to stop, or must stop because lawful continuation is blocked.

Lawful sufficiency and stopping evidence may come from:

1. **Native uncertainty component:** what component must be resolved or bounded.
2. **Native subject:** which repository/world subject the inquiry must examine.
3. **Present movement boundary:** what advancement crossing the inquiry is material to.
4. **Horizon included and excluded scope:** where future inquiry may and may not range.
5. **Evidence freshness and availability:** whether current evidence can support resolution, stale evidence requires freshness preservation, or unavailable evidence blocks resolution.
6. **Admission precedent:** bounded conclusions require competent evidence, provenance, authority boundary, negative authority, Unknown preservation, confidence, and lawful stop.
7. **Independent-testimony precedent:** future evidence must preserve source, support, scope, authority, Unknowns, confidence, and stop limits.

A lawful frontier can establish stopping conditions such as:

- stop when the selected uncertainty component is resolved or bounded for the exact repository/world subject under the current horizon;
- stop when evidence proves the uncertainty is not material to the present movement boundary;
- stop when all available territory inside included scope has been exhausted without sufficient evidence, preserving Unknown rather than fabricating a conclusion;
- stop when required evidence is unavailable, stale without refresh authority, conflicting without reconciliation authority, or outside the horizon;
- stop before source selection, observation authorization, constitutional-question formulation, execution, recording, ledger write, or mutation unless a later owner lawfully authorizes that step.

Stopping boundary is not conclusion already known. It is the limit that prevents unsupported inquiry expansion and unsupported promotion.

## Preservation of missing, ambiguous, conflicting, stale, and unavailable boundary testimony

### Missing testimony

If selected-need identity, native inquiry item identity, subject, uncertainty component, present movement boundary, included/excluded scope, evidence territory, or stopping testimony is missing, the frontier should preserve `frontier_state = not_established` or a specific missing-boundary state. It should not infer from family name, need uniqueness, goal wording, or absent evidence.

### Ambiguous testimony

If focus evidence or native lineage identifies multiple inquiry items, or if multiple subjects/components are possible, the frontier should preserve ambiguity with candidate refs. It should not select by order, severity, sufficiency reason, wording similarity, or count.

### Conflicting testimony

If the selected reference, native inquiry projection, need set, and horizon disagree about selection id, goal id, horizon id, projection id, lineage, standing, subject, component, freshness, availability, or scope, the frontier should preserve the conflict and refuse establishment unless a local owner has already reconciled it.

### Stale evidence

Stale evidence does not disappear and does not automatically become inquiry scope. It should be preserved as evidence-quality boundary testimony. It may support a stopping condition such as stale-support stop or refresh-required stop, but the frontier does not authorize refresh.

### Unavailable evidence

Unavailable evidence does not authorize access. It should be preserved as unavailable territory or blocking boundary. It may establish that inquiry cannot be sufficiently resolved under current authority, but it does not select an observation or authorize access.

### Unknowns

Unknowns from the selection, need set, native inquiry projection, and horizon should be carried forward as preserved Unknowns. They are successful boundary preservation, not defects to silently resolve.

## Does an existing owner already establish this frontier?

No reviewed owner already establishes `BoundedInquiryFrontier`.

Existing owners stop before this responsibility:

- `InquiryNeedProjection` establishes horizon-material inquiry need but explicitly does not open inquiry, select a question, authorize observation, judge sufficiency, execute, record, write the event ledger, or mutate state.
- `AdvancementNeedReferenceSet` exposes visible native item references but does not select, reclassify, prioritize, route, open inquiry, request authority, authorize, execute, record, write the event ledger, or mutate state.
- `AdvancementNeedConsiderationSelection` selects one visible reference for consideration but explicitly does not open inquiry, select next action, select realization, request authority, authorize, execute, record, write the event ledger, or mutate state.
- `BoundedAdvancementHorizon` preserves the present movement boundary but is not need classification, sufficiency judgment, inquiry opening, authorization, execution, recording, or mutation.
- `GoalAdvancementNeedSet` preserves stage-owned projections as an unordered set but does not rank, route, select next action, judge sufficiency, open inquiry, request authority, authorize, record, write the event ledger, or mutate state.

The frontier responsibility is therefore adjacent and missing.

## Smallest missing responsibility

The smallest missing responsibility is:

```text
Preserve a read-only bounded inquiry frontier for one exact selected established inquiry need by binding the selected advancement-need reference to its native inquiry item and current bounded advancement horizon, carrying the uncertainty component, repository/world subject, present movement boundary, included/excluded scope, available evidence territory, sufficiency/stopping boundaries, Unknowns, conflicts, stale evidence, and unavailable evidence without opening inquiry, formulating a constitutional question, selecting sources or observations, authorizing access, judging the result, recording, writing the event ledger, or mutating state.
```

This is smaller than inquiry opening, constitutional-question projection, source selection, observation selection, authority request, operational-realization selection, execution, or result judgment.

## Is one read-only implementation slice warranted?

Yes, one read-only implementation slice is warranted if Seed needs this boundary to become executable.

The slice should be a library/read-model artifact, not a diagnostic CLI surface unless explicitly requested. It should add only:

- a `BoundedInquiryFrontier` data shape;
- an assembler that consumes one `AdvancementNeedConsiderationSelection`, one `AdvancementNeedReferenceSet` or selected reference, one matching `GoalAdvancementNeedSet`, one matching `InquiryNeedProjection`, and one `BoundedAdvancementHorizon`;
- binding checks for need set, selected goal, goal establishment, horizon, family, projection, native lineage, established/selectable standing, subject, component, and evidence refs;
- preservation of included scope, excluded scope, available evidence territory, sufficiency boundaries, stopping boundaries, Unknowns, conflicts, stale evidence refs, and unavailable evidence refs;
- explicit negative authority flags proving no question selection, source selection, observation authorization, inquiry opening, execution, recording, event-ledger write, or mutation;
- tests for exact establishment and for non-establishment on missing identity, ambiguity, conflicts, stale/unavailable-only support, mismatched ids, non-inquiry selected need, non-selectable reference, absent native item, unsupported/unknown/conflicting/excluded standing, and absent stopping testimony.

If the slice exposes a diagnostic, audit, probe, view, operational CLI flag, or recordable output, the repository operational visibility contract requires updating diagnostic inventory, diagnostic shape-audit specs, and the corresponding diagnostic tests.

## Exact next bounded question

```text
What is the minimal read-only `BoundedInquiryFrontier` schema and assembler that consumes one selected inquiry `AdvancementNeedConsiderationSelection`, the matching advancement-need reference/native `InquiryNeedProjection` item, one `GoalAdvancementNeedSet`, and one `BoundedAdvancementHorizon`, then preserves the exact need identity, repository/world uncertainty component, subject requiring examination, present advancement boundary, included/excluded inquiry scope, available evidence territory, sufficiency and stopping boundaries, Unknowns, conflicts, stale evidence, and unavailable evidence without formulating the constitutional question, selecting sources or observations, authorizing access, opening inquiry, judging results, executing, recording, writing the event ledger, or mutating state?
```

## Conclusion

A bounded inquiry frontier is lawfully established only when one selected inquiry advancement-need reference is conjunctively bound to its exact established native inquiry item and exact bounded advancement horizon, and when explicit boundary testimony preserves the uncertainty component, repository/world subject, present movement boundary, included and excluded scope, available evidence territory, sufficiency and stopping limits, Unknowns, conflicts, stale evidence, and unavailable evidence. The selected need, native inquiry need, and horizon are necessary but not individually sufficient. The frontier remains read-only and does not open inquiry, formulate the constitutional question, select sources or observations, authorize access, judge the result, execute, record, write the event ledger, or mutate state.

Bounded inquiry frontier audit complete.
