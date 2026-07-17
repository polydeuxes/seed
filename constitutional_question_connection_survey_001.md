# Constitutional Question Connection Survey 001

## Survey boundary

This survey is a connection atlas. It does not recover implementation, select a seam, propose a slice, recommend an owner, design a pipeline, or decide what should be connected. Repository authority wins. Prior reports are testimony and evidence locators; current implementation and tests control live implementation standing.

## Evidence base and method

### Implementation modules inspected

- `seed_runtime/question_surface_inventory.py`: exact `QuestionFamily` inventory rows, lookup, eligibility, refusal, required-argument validation, selected dispatch/value, presentation handoff, dispatch request/result, family definition, composed explanation, answer responsibility fields, diagnostic relationship enrichment.
- `seed_runtime/typed_unknowns.py`: implementation-local `TypedUnknownRecord`, preservation function, and public compatibility projection.
- `seed_runtime/goal_inquiry_consideration_selection.py`: exact bounded-goal focus selection for inquiry consideration.
- `seed_runtime/bounded_advancement_horizon.py`: present bounded-goal movement boundary, evidence snapshots, scope, need-family inclusion/exclusion, refusal, Unknown/conflict preservation.
- `seed_runtime/inquiry_need_projection.py`: repository/world uncertainty testimony to inquiry-need projection.
- `seed_runtime/bounded_inquiry_frontier.py` and `seed_runtime/inquiry_frontier_boundary_testimony.py`: selected inquiry-need frontier assembly from clause-family testimony.
- `seed_runtime/bounded_constitutional_question.py`: caller-testimony individual bounded question artifact.
- `seed_runtime/constitutional_pipeline.py`, `seed_runtime/constitutional_view_selection.py`, and `seed_runtime/constitutional_view_composition.py`: individual bounded-question projection, selection, composition, and local provenance explanation.
- `seed_runtime/candidate_examination_work.py`, `seed_runtime/examination_frontier.py`, `seed_runtime/examination_method_applicability.py`, `seed_runtime/examination_policy_projection.py`, `seed_runtime/examination_work_selection.py`, and `seed_runtime/examination_probe_request.py`: bounded-question-to-examination-road visibility, eligibility, policy, selection, and probe-request handoff.
- `scripts/seed_local.py`: app-visible surfaces and CLI dispatch points.

### Tests inspected

- `tests/test_question_surface_inventory.py`
- `tests/test_bounded_constitutional_question.py`
- `tests/test_constitutional_pipeline.py`
- `tests/test_constitutional_question_projection.py`
- `tests/test_constitutional_view_selection.py`
- `tests/test_inquiry_need_projection.py`
- `tests/test_goal_inquiry_consideration_selection.py`
- `tests/test_bounded_advancement_horizon.py`
- `tests/test_bounded_inquiry_frontier.py`
- `tests/test_examination_frontier.py`
- `tests/test_examination_method_applicability.py`
- `tests/test_examination_policy_projection.py`
- `tests/test_examination_work_selection.py`
- `tests/test_examination_probe_request.py`
- `tests/test_candidate_examination_work.py`

### Reports recovered

Recovered and used as testimony/evidence locators: `constitutional_question_terrain_survey_001.md`, `constitutional_question_family_reconciliation_investigation.md`, `question_shape_question_family_relationship_scout.md`, `question_shape_family_bridge_survey.md`, `typed_unknown_characterization.md`, `unknown_currency_survey.md`, `question_family_registration_boundary_audit.md`, `question_to_inquiry_transition_characterization.md`, `inquiry_eligibility_characterization.md`, `constitutional_bounded_goal_question_bridge_001.md`, `constitutional_bounded_question_origination_topology_001.md`, `constitutional_bounded_question_frontier_topology_001.md`, and `bounded_inquiry_frontier_question_handoff_audit_001.md`. Additional nearby evidence included `constitutional_implementation_topology_comparison.md`, `constitutional_question_dependency_survey.md`, `goal_advancement_need_audit_001.md`, `bounded_ask_adjacent_terrain_scout.md`, `bounded_constitutional_question_slice_001.md`, and answer-responsibility documents under `docs/`.

### App-visible surfaces exercised

- `python scripts/seed_local.py --question-surface-inventory --json`
- `python scripts/seed_local.py --question-family-explanation "constitutional pipeline"`
- `python scripts/seed_local.py --question-family-explanation "not a family" --json`
- `python scripts/seed_local.py ask --question-family "knowledge reachability" --json`
- `python scripts/seed_local.py ask --question-family "surface inventory"`
- `python scripts/seed_local.py --reasoning-path derivation unknown-frontier-candidate --json`
- `python scripts/seed_local.py --selection-path unknown-frontier-candidate --json`

### Negative searches recorded

Searches for `QuestionFamilyRegistration`, `RecoveredQuestionFamily`, `family admission from Unknown`, `TypedUnknownRecord QuestionFamily`, `BoundedInquiryFrontier produce_bounded_constitutional_question`, `retirement`, `retired`, `answered status`, `archival`, and `frontier removal` found no live implementation owner proving automatic family registration, Unknown-to-family selection, frontier-to-question production, answer-to-completion, or completion-to-retirement. Some reports discuss possible roads or future responsibilities, but no executable handoff was found.

## Independent territory standing

### Bounded-goal condition

- **What it is:** A selected bounded goal plus a bounded advancement horizon preserving present movement boundary, included/excluded scope, time/current-state bounds, evidence snapshots, potential need families, explicit exclusions, Unknowns, conflicts, stale and unavailable evidence.
- **Preserves:** current bounded-goal position, horizon identity, evidence refs, scope bounds, authority/stop constraints, Unknowns and conflicts.
- **Authorizes:** preservation of the present movement boundary for later read-only projections.
- **Refuses:** need classification, sufficiency judgment, next action, inquiry opening, authority request, realization selection, scheduling, work authorization, execution, recording, ledger write, mutation.
- **Known producers:** `select_goal_for_inquiry_consideration(...)`; `establish_bounded_advancement_horizon(...)`.
- **Lawful consumers:** `project_inquiry_need(...)` consumes selection/goal/horizon plus testimony; advancement-need and sufficiency projections consume related goal/horizon material.
- **Stop behavior:** refusal on unresolved selection, goal mismatch, refused goal, missing movement boundary, or excluded need family lacking reason.
- **Implementation standing:** implementation-backed.
- **Preserved Unknowns:** selection Unknowns, goal Unknowns, horizon Unknowns, stale/unavailable evidence refs, missing identity or boundary reasons.

### Inquiry Need

- **What it is:** A read-only projection of explicit component-bounded repository/world uncertainty testimony into inquiry-need standings for one selected goal and horizon.
- **Preserves:** testimony refs, source refs, uncertainty component refs, repository/world subject refs, owning stage, standing (`established`, `unsupported`, `unknown`, `conflicting`, `excluded_family`), evidence freshness, evidence availability, and unclassified reasons.
- **Authorizes:** saying that supplied testimony is established/unsupported/unknown/conflicting/excluded as inquiry-need evidence.
- **Refuses:** inquiry opening, question selection, observation authorization, next action selection, sufficiency judgment, execution, recording, ledger write, mutation.
- **Known producers:** `project_inquiry_need(...)`.
- **Lawful consumers:** bounded inquiry frontier boundary testimony and `assemble_bounded_inquiry_frontier(...)` through selected inquiry-need references; reports and app-visible explanations.
- **Stop behavior:** unclassified reasons for identity mismatch, wrong family, missing subject, non-stage-owned, non-component-bounded, non-material, stale/unavailable evidence; excluded family when horizon excludes inquiry.
- **Implementation standing:** implementation-backed.
- **Preserved Unknowns:** `unknown` inquiry standing, unknown freshness/availability, unclassified reason strings. It does not preserve `TypedUnknownRecord.unknown_type`.

### Typed Unknown

- **What it is:** Two related but non-equivalent territories: implementation-local `TypedUnknownRecord(unknown_type, area, reason)` and broader constitutional Unknown states such as Evidence Gap, Implementation Unknown, Boundary Unknown, Relationship Unknown, Methodological Unknown, Constitutional Unknown, Implementation Readiness Unknown, and local `unknowns` fields.
- **Preserves:** unresolved standing without resolution; implementation-local type before projecting to public `{area, reason}` compatibility shape.
- **Authorizes:** public Unknown reporting and local stop/limitation preservation.
- **Refuses:** resolution of the unknown, family selection, fact promotion, generic collapse of all unknown fields into one type.
- **Known producers:** `preserve_typed_unknown(...)`; selection/reasoning-path audit surfaces; many local artifacts produce untyped `unknowns` strings.
- **Lawful consumers:** public unknown lists, audit renderers, limitation sections, relationship surveys.
- **Stop behavior:** preserve rather than infer; project typed records to untyped public shape when needed.
- **Implementation standing:** implementation-backed only for local record shape and projection; broader Unknown states are constitutionally supported by reports.
- **Preserved Unknowns:** the Unknown itself; relation-specific Unknowns where no lawful crossing exists.

### Question Shape

- **What it is:** A recurring constitutional/methodological question form recovered in reports: bounded question form, evidence posture, scope, conclusion-strength boundary, unsupported-conclusion preservation, confidence, and stop discipline.
- **Preserves:** the shape of lawful asking and answering without requiring inventory registration.
- **Authorizes:** bounded survey/investigation form and conclusion limits under warrant.
- **Refuses:** automatic `QuestionFamily` admission, dispatch, owner creation, implementation authority, individual question establishment.
- **Known producers:** surveys, scouts, bridge reports, constitutional investigations.
- **Lawful consumers:** Survey Warrant Family discipline, relationship investigations, family reconciliation reports.
- **Stop behavior:** Unsupported conclusion or Unknown rather than promotion.
- **Implementation standing:** constitutionally/report supported, not a live dispatch artifact.
- **Preserved Unknowns:** whether a given shape should be registered as a family; whether a local family is projection, correspondence, or separate identity.

### Survey Warrant Family

- **What it is:** A methodological/constitutional warrant for bounded surveys: inspect evidence broadly, preserve negative findings, classify connection standing, and limit conclusion strength.
- **Preserves:** scope, evidence posture, investigation shape, produced artifact pattern, confidence and stop.
- **Authorizes:** warranted survey claims about repository evidence.
- **Refuses:** `QuestionFamily` admission, bounded-work eligibility, dispatch ownership, implementation authority.
- **Known producers:** survey reports and investigations.
- **Lawful consumers:** subsequent surveys, reconciliation reports, atlas-style artifacts.
- **Stop behavior:** insufficient visibility, Unknown, report-only relationship, methodological exchange.
- **Implementation standing:** methodological/constitutional; not a runtime family registry.
- **Preserved Unknowns:** unsupported conclusions, insufficient visibility, relationship Unknowns.

### QuestionFamily

- **What it is:** Exact public answerability identity in `QuestionSurfaceInventoryRow` with family name, examples, surface, flag, answer responsibility, authority boundary, notes, bounded status, dispatch surface, required args, JSON/human formatter support, implementation reason, diagnostic relationship fields, relationship status.
- **Preserves:** family identity, answer responsibility, authority boundary, bounded ask status, dispatch mapping, required parameters, diagnostic relationship.
- **Authorizes:** exact lookup; bounded ask eligibility where mapped; presentation/explanation; dispatch to existing family-local surfaces.
- **Refuses:** unknown family inference, free-text classification, unregistered Question Shape admission, diagnostic-only bounded ask execution, answer composition as a universal engine.
- **Known producers:** `build_question_surface_inventory()`, `_lookup_exact_question_family(...)`, `build_question_family_definition(...)`, `build_composed_question_family_explanation(...)`.
- **Lawful consumers:** bounded ask eligibility/selection/dispatch; presentation; diagnostic inventory/shape audit comparison; surveys as evidence.
- **Stop behavior:** unknown family definition/explanation or `ValueError`; `diagnostic_only` and `not_dispatchable` refusal.
- **Implementation standing:** implementation-backed.
- **Preserved Unknowns:** unknown family status and unknown answer responsibility/boundary for absent rows.

### Individual bounded question

- **What it is:** `BoundedConstitutionalQuestion`, an immutable artifact preserving explicit caller-supplied operator inquiry, provenance, bounded question text, constitutional intent, scope status, uncertainty, Unknowns, and caller fields.
- **Preserves:** caller testimony as evidence, not established fact; read-only/no-mutation boundaries.
- **Authorizes:** downstream typed view/pipeline or examination projections to consume an already supplied bounded question.
- **Refuses:** natural-language classification, fact promotion, authority creation, repository truth creation, durable knowledge creation, capability creation, view selection, QuestionProjection production, event ledger writes, mutation.
- **Known producers:** `produce_bounded_constitutional_question(...)`; constitutional pipeline bounded-ask parameter road prepares explicit inputs.
- **Lawful consumers:** constitutional pipeline, view projection/selection/composition, examination frontier, method applicability, policy, work selection, probe request.
- **Stop behavior:** no automatic establishment from goal/frontier; downstream empty selection or Unknowns preserve unsupported keys.
- **Implementation standing:** implementation-backed.
- **Preserved Unknowns:** caller-supplied `unknowns` tuple and downstream projection unknowns.

### Bounded inquiry frontier

- **What it is:** Read-only assembly of one exact selected inquiry need plus preserved frontier-boundary testimony into a frontier state.
- **Preserves:** selected need lineage, need set, goal/horizon ids, uncertainty component, repository/world subject, operative and preserved clause refs, required family gaps, material conflicts, non-operative/unsupported/unknown/mixed/adjacent/stale/unavailable/out-of-scope clauses.
- **Authorizes:** established bounded inquiry frontier when required clause families are present and no material conflict exists.
- **Refuses:** scope invention, evidence admission, question formulation, inquiry opening, source/observation selection, access authorization, execution, recording, ledger write, mutation, knowing result.
- **Known producers:** `assemble_bounded_inquiry_frontier(...)`.
- **Lawful consumers:** reports; no live frontier-to-question adapter found.
- **Stop behavior:** `not_selected_inquiry_need`, `missing_required_clause_family`, `material_binding_conflict`.
- **Implementation standing:** implementation-backed for selected inquiry-need frontier; disconnected from live bounded-question production.
- **Preserved Unknowns:** unknown clauses, stale/unavailable/out-of-scope clauses, missing required families, conflicts.

### Examination frontier

- **What it is:** Read-only projection from one individual bounded question plus supplied corpus members and candidate work into work-item classifications.
- **Preserves:** inquiry reference, corpus/work visibility, compatibility and authorization testimony, existing results, blockers, deferrals, failures, Unknowns, summary counts.
- **Authorizes:** classification as eligible, examined, blocked, unsupported, deferred, failed, unknown, or conflict.
- **Refuses:** discovery, scheduler/queue/priority, work selection, authorization, execution, knowledge admission, campaign completion verdict.
- **Known producers:** `project_examination_frontier(...)`; candidate work adapters can prepare supplied work visibility.
- **Lawful consumers:** method applicability, policy projection, examination work selection, probe request binding.
- **Stop behavior:** structural errors for duplicate/unknown/mismatched inputs; unknown classification when status/authorization unresolved; examined classification blocks eligibility.
- **Implementation standing:** implementation-backed.
- **Preserved Unknowns:** candidate unknowns, compatibility unknown, authorization unknown, frontier unknowns.

### Answer responsibility

- **What it is:** Local responsibility statement for an answering surface or family row, not one universal answer engine.
- **Preserves:** expected answer kind, responsible surface, boundary, implementation reason, diagnostic relationship when sourced from QuestionFamily rows; surface-local evidence and limitations when dispatched.
- **Authorizes:** explanation of who/what answers a family and how bounded ask delegates.
- **Refuses:** evidence gathering outside local surface, universal composition, completion verdict, family registration.
- **Known producers:** inventory rows, `build_question_family_definition(...)`, `build_composed_question_family_explanation(...)`, family-local surfaces.
- **Lawful consumers:** bounded ask presentation, survey evidence, operator-facing explanations.
- **Stop behavior:** unknown answer responsibility for unknown family; surface-local refusals and Unknowns.
- **Implementation standing:** implementation-backed for inventory rows and local surfaces.
- **Preserved Unknowns:** unknown responsibility for absent rows; local surface Unknowns.

### Answer

- **What it is:** A family-local or pipeline-local rendered/JSON artifact produced by existing surfaces: inventory output, family explanation, reasoning/selection path, operational story, knowledge reachability, constitutional pipeline composition, examination classifications, etc.
- **Preserves:** local response availability, support path, Unknowns/refusals/limitations as the surface defines them.
- **Authorizes:** only the local answer-bearing artifact.
- **Refuses:** universal sufficiency, automatic completion, retirement, truth beyond support path.
- **Known producers:** scripts/CLI dispatch and family-local formatters/projections.
- **Lawful consumers:** humans, surveys, later bounded investigations, presentation surfaces.
- **Stop behavior:** empty selection, unknown family, no evidence, Unknowns, refusals, non-dispatchable status.
- **Implementation standing:** implementation-backed but family-local.
- **Preserved Unknowns:** surface-local unknowns.

### Completion

- **What it is:** Local status or sufficiency/completion-like terrain, not universally implied by answer availability. In examination frontier, a completed result reference classifies work as examined. In diagnostic/audit surfaces, completion is surface-local result production or status comparison.
- **Preserves:** local endpoint of a work/result/status check where a producer explicitly says so.
- **Authorizes:** local classification such as examined or surface result availability.
- **Refuses:** automatic bounded-question sufficiency, inquiry completion, campaign completion, retirement.
- **Known producers:** examination frontier from supplied completed result references; local diagnostic/audit surfaces; sufficiency projections in goal terrain.
- **Lawful consumers:** frontier classification, reports, local audits.
- **Stop behavior:** mismatch errors; insufficient evidence; no-selection not a completion verdict.
- **Implementation standing:** implementation-backed only in local forms.
- **Preserved Unknowns:** whether selected views answer a question; whether examined result is admitted as knowledge; whether inquiry/campaign is complete.

### Retirement

- **What it is:** Supersession, archival, answered-status, frontier removal, or continued-validity terrain only where explicitly evidenced. No universal live owner was found for question retirement.
- **Preserves:** where documents mention history or preservation, they preserve prior evidence; implementation does not equate completion with retirement.
- **Authorizes:** no general automatic transition found.
- **Refuses:** inference from answer, examined, completed result, or no-selection.
- **Known producers:** historical documents and local archival/preservation language; no current universal runtime producer found.
- **Lawful consumers:** history/conflict review, not live question pipeline.
- **Stop behavior:** insufficient visibility / Relationship Unknown.
- **Implementation standing:** mostly report/historical; no implementation-backed universal question retirement owner found.
- **Preserved Unknowns:** whether any family-local completion should retire an item; whether history preserves continued validity or supersession.

## Directional relationship matrix

### Bounded-goal condition ↔ Inquiry Need

#### Bounded-goal condition → Inquiry Need

1. **Crosses:** exact selected goal identity, selection id, goal establishment id, horizon id, evidence snapshot refs, current/stale/unavailable evidence, potentially relevant/excluded need-family boundary, present movement boundary, Unknowns/conflicts as context.
2. **Standing changes:** explicit repository/world uncertainty testimony can be projected into inquiry-need buckets for that selected goal/horizon.
3. **Does not change:** selected for inquiry consideration is not inquiry opened, question formed, work authorized, sufficiency judged, or frontier moved.
4. **Evidence:** `GoalInquiryConsiderationSelection`, `BoundedAdvancementHorizon`, `RepositoryWorldUncertaintyTestimony`, `InquiryNeedProjection` implementation and tests; terrain and bounded-goal bridge reports.
5. **Authority/warrant:** exact identity match and component-bounded repository/world uncertainty testimony owned by a stage.
6. **Producer:** `project_inquiry_need(...)`.
7. **Consumer:** inquiry-need projection buckets and later selected-need/frontier testimony.
8. **Refusal/Unknown:** identity mismatch, wrong uncertainty family, non-stage-owned, non-component-bounded, missing subject, non-material, mixed/non-inquiry, excluded family.
9. **Class:** implementation-backed direct connection.
10. **Relation:** direct but narrow.

#### Inquiry Need → Bounded-goal condition

1. **Crosses:** classification of supplied testimony as established/unsupported/unknown/conflicting/excluded for that goal/horizon.
2. **Standing changes:** it may say an inquiry need is or is not established as local evidence.
3. **Does not change:** it does not alter the goal, decide sufficiency, activate a goal, select a next action, or authorize work.
4. **Evidence:** boundary notes and read-only flags in `InquiryNeedProjection`.
5. **Authority/warrant:** same identity-bound projection authority only.
6. **Producer:** `project_inquiry_need(...)`.
7. **Consumer:** reports, frontier-boundary testimony preparers, human interpretation.
8. **Refusal/Unknown:** unknown/conflicting/excluded/unclassified projection states.
9. **Class:** implementation-backed direct feedback of classification only.
10. **Relation:** direct but non-mutating.

### Inquiry Need ↔ Typed Unknown

#### Inquiry Need → Typed Unknown

1. **Crosses:** untyped `unknown` standing, unknown evidence freshness/availability, and reason strings.
2. **Standing changes:** none into implementation-local typed Unknown unless a separate producer wraps it.
3. **Does not change:** inquiry need does not preserve `unknown_type`; it is not a `TypedUnknownRecord` source in current implementation.
4. **Evidence:** `InquiryNeedProjectionItem` fields lack `unknown_type`; `TypedUnknownRecord` is separate.
5. **Authority/warrant:** local inquiry projection only.
6. **Producer:** `project_inquiry_need(...)` produces untyped Unknown-like output.
7. **Consumer:** public/report surfaces, not `typed_unknowns.py`.
8. **Refusal/Unknown:** type of unresolved standing is not preserved; relation to typed Unknown is Relationship Unknown beyond general Unknown correspondence.
9. **Class:** adjacency with methodological correspondence; no implementation-backed direct typed handoff.
10. **Relation:** adjacent/mediated only through public Unknown vocabulary.

#### Typed Unknown → Inquiry Need

1. **Crosses:** no implementation-local `TypedUnknownRecord` crosses into `project_inquiry_need(...)`.
2. **Standing changes:** none.
3. **Does not change:** typed Unknowns do not source inquiry need, classify inquiry need, or constrain inquiry-need projection.
4. **Evidence:** inquiry projection consumes `RepositoryWorldUncertaintyTestimony`, not `TypedUnknownRecord`.
5. **Authority/warrant:** would require explicit testimony/handoff not found.
6. **Producer:** none found.
7. **Consumer:** none found.
8. **Refusal/Unknown:** Relationship Unknown / disconnected road.
9. **Class:** adjacency without exchange.
10. **Relation:** disconnected direct road.

### Typed Unknown ↔ Question Shape

#### Typed Unknown → Question Shape

1. **Crosses:** constitutionally, the type of Unknown can constrain evidence posture and forbidden conclusions: Evidence Gap forbids proof claims; Implementation Unknown forbids implementation claims; Relationship Unknown forbids topology claims; Boundary Unknown forbids boundary crossing.
2. **Standing changes:** a survey/question shape may narrow to preserving missing evidence, unsupported conclusion, confidence limit, or stop.
3. **Does not change:** typed Unknown does not generate question wording or admit a QuestionFamily.
4. **Evidence:** typed-unknown and unknown-currency reports; question-shape bridge reports; implementation only supports local typed preservation.
5. **Authority/warrant:** methodological warrant to ask a bounded question about the unresolved type.
6. **Producer:** surveys and audit surfaces; `preserve_typed_unknown(...)` for local records.
7. **Consumer:** Question Shape discipline in reports.
8. **Refusal/Unknown:** no executable shape generator; relation remains constitutional/methodological.
9. **Class:** methodological exchange / constitutional correspondence.
10. **Relation:** mediated by survey discipline.

#### Question Shape → Typed Unknown

1. **Crosses:** question shape may require preserving Unknowns and conclusion-strength limits.
2. **Standing changes:** a report may classify an unresolved endpoint as a typed constitutional Unknown.
3. **Does not change:** Question Shape does not instantiate `TypedUnknownRecord` unless implementation calls the producer.
4. **Evidence:** Survey forms require preserved Unknowns; implementation has a separate typed record.
5. **Authority/warrant:** Survey warrant and evidence insufficiency.
6. **Producer:** report authoring / local audit producer.
7. **Consumer:** Unknown sections, public unknown lists.
8. **Refusal/Unknown:** no direct runtime shape-to-record road found.
9. **Class:** methodological exchange; implementation direct connection absent.
10. **Relation:** mediated.

### Question Shape ↔ Survey Warrant Family

#### Question Shape → Survey Warrant Family

1. **Crosses:** bounded question form, scope, evidence posture, investigation shape, conclusion-strength boundary, unsupported-conclusion preservation, confidence, stop.
2. **Standing changes:** shape becomes a warranted survey task when survey discipline is invoked.
3. **Does not change:** no registration, dispatch, ownership, implementation authority, or family admission crosses.
4. **Evidence:** `question_shape_family_bridge_survey.md`, `question_shape_question_family_relationship_scout.md`, and survey reports.
5. **Authority/warrant:** Survey warrant.
6. **Producer:** survey report methodology.
7. **Consumer:** produced survey artifact.
8. **Refusal/Unknown:** insufficient visibility and unsupported conclusions are lawful results.
9. **Class:** constitutional correspondence / methodological exchange.
10. **Relation:** direct as discipline, non-executable.

#### Survey Warrant Family → Question Shape

1. **Crosses:** discipline can expose what question form was actually asked and what conclusion strength is lawful.
2. **Standing changes:** shape is bounded and reviewable.
3. **Does not change:** it does not become a QuestionFamily or executable route.
4. **Evidence:** same reports.
5. **Authority/warrant:** evidence discipline and bounded scope.
6. **Producer:** warranted survey.
7. **Consumer:** later relationship surveys.
8. **Refusal/Unknown:** preserved Unknowns and stops.
9. **Class:** methodological exchange.
10. **Relation:** direct as report discipline.

### Survey Warrant Family ↔ QuestionFamily

#### Survey Warrant Family → QuestionFamily

1. **Crosses:** warrant disciplines claims about existing inventory rows: exact family names, examples, answer responsibility, authority boundary, bounded status, required args, implementation reason, diagnostic relationship.
2. **Standing changes:** none to the row; the survey gains evidence.
3. **Does not change:** survey warrant is not QuestionFamily admission or bounded-work eligibility.
4. **Evidence:** inventory implementation and tests; family reconciliation reports.
5. **Authority/warrant:** survey evidence discipline.
6. **Producer:** survey report.
7. **Consumer:** claims about QuestionFamily.
8. **Refusal/Unknown:** unknown family remains unknown; unregistered shapes remain unregistered.
9. **Class:** methodological exchange using implementation evidence.
10. **Relation:** mediated by inventory rows.

#### QuestionFamily → Survey Warrant Family

1. **Crosses:** inventory rows can serve as evidence inside a warranted survey.
2. **Standing changes:** row may be cited as implementation-backed evidence.
3. **Does not change:** row does not impose survey scope, conclusion strength beyond its own fields, or admit other families.
4. **Evidence:** `build_question_surface_inventory()` and app-visible `--question-surface-inventory`.
5. **Authority/warrant:** exact row evidence.
6. **Producer:** question-surface inventory.
7. **Consumer:** survey artifact.
8. **Refusal/Unknown:** diagnostic-only/not-dispatchable statuses limit claims.
9. **Class:** implementation evidence consumed by methodological warrant.
10. **Relation:** direct evidence use, not executable survey dispatch.

### Question Shape ↔ QuestionFamily

#### Question Shape → QuestionFamily

1. **Crosses:** only correspondence evidence: family name may resemble shape; example questions expose shape-like form; answer responsibility/boundary may evidence an implementation-backed projection of a shape in some families.
2. **Standing changes:** none unless exact inventory row exists.
3. **Does not change:** Question Shape does not register, select, dispatch, or make bounded status lawful.
4. **Evidence:** family registration boundary audit, shape-family bridge survey, inventory tests.
5. **Authority/warrant:** exact static inventory admission.
6. **Producer:** no shape-to-family implementation producer found.
7. **Consumer:** reports compare shape to row.
8. **Refusal/Unknown:** missing QuestionFamily admission remains missing; unknown family lookup refuses inference.
9. **Class:** constitutional correspondence; direct implementation connection absent.
10. **Relation:** adjacent/mediated by reports and exact rows.

#### QuestionFamily → Question Shape

1. **Crosses:** family rows expose example questions, answer responsibility, authority boundary, bounded status, required arguments, and implementation reason that can be analyzed as shape-like evidence.
2. **Standing changes:** a registered row is an exact public identity, not merely a shape.
3. **Does not change:** family identity is not universal shape identity and not individual question identity.
4. **Evidence:** `QuestionSurfaceInventoryRow` fields.
5. **Authority/warrant:** inventory row and bounded ask maps.
6. **Producer:** `build_question_surface_inventory()`.
7. **Consumer:** shape surveys.
8. **Refusal/Unknown:** row-specific differences; diagnostic-only families expose shape but refuse bounded ask.
9. **Class:** implementation-backed evidence with constitutional correspondence.
10. **Relation:** direct evidence, not equivalence.

### Typed Unknown ↔ QuestionFamily

#### Typed Unknown → QuestionFamily

1. **Crosses:** strongest truthful connection is negative/limiting testimony: Unknowns may describe missing family evidence or block unsupported promotion.
2. **Standing changes:** none to family identity or eligibility.
3. **Does not change:** Unknown does not select a family, refuse a family, perform inventory lookup, or create admission.
4. **Evidence:** no implementation consumer; prior terrain survey negative finding; `TypedUnknownRecord` has no family field; `QuestionFamily` lookup is exact row matching.
5. **Authority/warrant:** only survey warrant can state relation is unknown/missing.
6. **Producer:** none for direct handoff; reports produce Relationship Unknown.
7. **Consumer:** none in live family eligibility.
8. **Refusal/Unknown:** Relationship Unknown; unsupported promotion blocked.
9. **Class:** Relationship Unknown plus explicit refusal boundary against promotion.
10. **Relation:** disconnected direct road; possible methodological mediation through Question Shape.

#### QuestionFamily → Typed Unknown

1. **Crosses:** unknown family definition/explanation can output status `unknown` and unknown answer responsibility/boundary in public dictionaries.
2. **Standing changes:** this is an untyped unknown-family result, not a `TypedUnknownRecord`.
3. **Does not change:** exact inventory lookup failure does not classify a typed constitutional Unknown unless another owner does so.
4. **Evidence:** `build_question_family_definition(...)` unknown branch; bounded work lookup raises unknown-family refusal.
5. **Authority/warrant:** exact lookup/definition boundary.
6. **Producer:** question-family definition/lookup.
7. **Consumer:** CLI JSON/presentation, surveys.
8. **Refusal/Unknown:** unknown family status; not_dispatchable or diagnostic-only refusals.
9. **Class:** implementation-backed direct untyped unknown output; no typed-record connection.
10. **Relation:** direct to generic unknown status, disconnected from typed Unknown record.

### QuestionFamily ↔ Individual bounded question

#### QuestionFamily → Individual bounded question

1. **Crosses:** generally no universal crossing. The `constitutional pipeline` family is special: required args are explicit bounded-question fields, and bounded ask prepares a surface value for the constitutional pipeline.
2. **Standing changes:** for that family only, operator-supplied surface args can be used to produce a `BoundedConstitutionalQuestion` inside pipeline invocation.
3. **Does not change:** family identity is not question instance identity; registration is not individual-question establishment; exact family does not make caller testimony true.
4. **Evidence:** `BOUNDED_ASK_REQUIRED_SURFACE_ARGS` and selected surface value construction for `constitutional pipeline`; bounded-question producer boundaries.
5. **Authority/warrant:** exact family eligibility plus required explicit args.
6. **Producer:** bounded ask surface-value preparation and constitutional pipeline invocation.
7. **Consumer:** `produce_bounded_constitutional_question(...)` / pipeline.
8. **Refusal/Unknown:** missing/wrong args; unknown family; unsupported selection keys; no universal road for other families.
9. **Class:** implementation-backed direct connection only for `constitutional pipeline`; adjacency/unknown for other families.
10. **Relation:** family-local special case, not universal.

#### Individual bounded question → QuestionFamily

1. **Crosses:** an individual bounded question may carry caller-supplied fields such as selection keys or question text, but no implementation derives family identity from it.
2. **Standing changes:** none to `QuestionFamily` registration or eligibility.
3. **Does not change:** individual question testimony is not family eligibility.
4. **Evidence:** `BoundedConstitutionalQuestion` boundaries refuse classification and QuestionProjection production; exact family lookup is separate.
5. **Authority/warrant:** exact inventory lookup would be required separately.
6. **Producer:** none found for question-to-family.
7. **Consumer:** none found.
8. **Refusal/Unknown:** no natural-language classification; Relationship Unknown for any family inference.
9. **Class:** adjacency without exchange.
10. **Relation:** disconnected direct road.

### Individual bounded question ↔ Bounded inquiry frontier

#### Individual bounded question → Bounded inquiry frontier

1. **Crosses:** no live implementation crossing found.
2. **Standing changes:** none; a question does not assemble a selected inquiry-need frontier.
3. **Does not change:** question identity does not equal frontier membership, inquiry selection, or boundary clauses.
4. **Evidence:** bounded inquiry frontier consumes `AdvancementNeedConsiderationSelection` and `InquiryFrontierBoundaryTestimony`, not `BoundedConstitutionalQuestion`.
5. **Authority/warrant:** selected inquiry need and required clause testimony.
6. **Producer:** none found.
7. **Consumer:** none found.
8. **Refusal/Unknown:** adjacency only.
9. **Class:** disconnected road.
10. **Relation:** adjacent.

#### Bounded inquiry frontier → Individual bounded question

1. **Crosses:** report-only proposed handoff requirements: frontier id, selected need, uncertainty component, subject, scope, evidence territory, sufficiency, stopping conditions, Unknowns/conflicts.
2. **Standing changes:** none currently; existing question producer can only receive manually supplied strings.
3. **Does not change:** frontier does not formulate a question or open inquiry.
4. **Evidence:** `bounded_inquiry_frontier_question_handoff_audit_001.md` found no adapter; implementation boundary notes say `formulates_question=False`.
5. **Authority/warrant:** would require a handoff producer not found.
6. **Producer:** none live.
7. **Consumer:** none live.
8. **Refusal/Unknown:** non-established/missing/conflicting frontiers remain frontier artifacts; relationship currently missing.
9. **Class:** report-represented possible road / disconnected current road.
10. **Relation:** not direct; possible mediated road absent.

### QuestionFamily ↔ Bounded inquiry frontier

#### QuestionFamily → Bounded inquiry frontier

1. **Crosses:** no direct artifact. Both use inquiry vocabulary, but family identity does not supply selected need, clause testimony, frontier scope, evidence territory, dependency, or stop.
2. **Standing changes:** none.
3. **Does not change:** public inquiry family identity is not inquiry need or frontier admission.
4. **Evidence:** frontier inputs and family inventory are disjoint.
5. **Authority/warrant:** selected inquiry need and clauses, not family row.
6. **Producer:** none found.
7. **Consumer:** none found.
8. **Refusal/Unknown:** vocabulary adjacency refused.
9. **Class:** adjacency without exchange / explicit refusal boundary.
10. **Relation:** disconnected.

#### Bounded inquiry frontier → QuestionFamily

1. **Crosses:** no family identity, dispatch surface, or row admission.
2. **Standing changes:** none.
3. **Does not change:** frontier establishment is not QuestionFamily registration or bounded ask eligibility.
4. **Evidence:** no lookup/registration consumer; frontier boundary refuses question formulation.
5. **Authority/warrant:** exact inventory admission would be separate.
6. **Producer:** none found.
7. **Consumer:** none found.
8. **Refusal/Unknown:** Relationship Unknown for any mediated future relation.
9. **Class:** disconnected road.
10. **Relation:** adjacent.

### Individual bounded question ↔ Examination frontier

#### Individual bounded question → Examination frontier

1. **Crosses:** bounded_question_id, provenance, bounded question text into `inquiry_reference`; corpus/work visibility supplied separately.
2. **Standing changes:** examination frontier can classify supplied work relative to that inquiry reference.
3. **Does not change:** question identity is not selected work, authorized examination, or performed examination.
4. **Evidence:** `project_examination_frontier(...)` requires `BoundedConstitutionalQuestion` and emits inquiry reference.
5. **Authority/warrant:** structurally valid bounded question plus supplied corpus/work evidence.
6. **Producer:** examination frontier projection.
7. **Consumer:** frontier work items and later method/policy/selection.
8. **Refusal/Unknown:** invalid question input; unknown compatibility/authorization; structural mismatches.
9. **Class:** implementation-backed direct connection.
10. **Relation:** direct but requires separately supplied corpus/work.

#### Examination frontier → Individual bounded question

1. **Crosses:** frontier carries inquiry reference back as provenance only.
2. **Standing changes:** none to the question; frontier classifications do not answer or complete it.
3. **Does not change:** examined/eligible/blocked statuses do not change question identity or truth.
4. **Evidence:** frontier boundary notes.
5. **Authority/warrant:** read-only projection.
6. **Producer:** examination frontier.
7. **Consumer:** downstream examination policy/selection/probe request and reports.
8. **Refusal/Unknown:** classification Unknowns; no campaign completion verdict.
9. **Class:** implementation-backed direct provenance connection.
10. **Relation:** direct but non-mutating.

### QuestionFamily ↔ Answer responsibility

#### QuestionFamily → Answer responsibility

1. **Crosses:** exact answer responsibility string, responsible surface/flag, dispatch surface, implementation reason, relationship status, authority boundary.
2. **Standing changes:** known family row has known family-local answer responsibility.
3. **Does not change:** QuestionFamily does not own all evidence gathering, composition, rendering, or completion; it delegates to local surfaces.
4. **Evidence:** `QuestionSurfaceInventoryRow` and family definition/explanation builders.
5. **Authority/warrant:** exact inventory row.
6. **Producer:** question-surface inventory/family definition.
7. **Consumer:** presentation, bounded ask, surveys.
8. **Refusal/Unknown:** unknown family yields unknown answer responsibility; diagnostic-only/not-dispatchable limit execution.
9. **Class:** implementation-backed direct connection.
10. **Relation:** direct.

#### Answer responsibility → QuestionFamily

1. **Crosses:** responsibility text can identify how a known row answers, but not create row identity.
2. **Standing changes:** none unless matched to an exact row.
3. **Does not change:** responsibility is not registration or eligibility.
4. **Evidence:** row builder stores responsibility inside family row; no reverse index found.
5. **Authority/warrant:** exact row evidence.
6. **Producer:** inventory rows.
7. **Consumer:** explanation/survey.
8. **Refusal/Unknown:** same responsibility vocabulary elsewhere does not imply a family.
9. **Class:** implementation-backed row-internal relation; no reverse admission.
10. **Relation:** internal/direct only after row identity exists.

### Individual bounded question ↔ Answer responsibility

#### Individual bounded question → Answer responsibility

1. **Crosses:** in constitutional pipeline, explicit selection keys and bounded question testimony route to view projection/selection/composition; in examination road, evidence demand constrains corpus/work visibility. No QuestionFamily answer responsibility is bound by the question artifact itself.
2. **Standing changes:** local pipeline/examination owners may derive local answering/projection responsibility.
3. **Does not change:** caller routing/selection keys are not established evidence demand, family eligibility, or universal answer responsibility.
4. **Evidence:** pipeline request consumes bounded question; bounded question boundary refuses view selection; selection/composition own later steps.
5. **Authority/warrant:** explicit bounded inputs and selection keys; registered view/capability evidence.
6. **Producer:** pipeline projection/selection/composition; examination frontier/policy.
7. **Consumer:** selected views/composition, examination artifacts.
8. **Refusal/Unknown:** empty selection, unsupported keys, Unknown capability evidence, no selected work.
9. **Class:** implementation-backed mediated connection.
10. **Relation:** mediated by pipeline/examination owners.

#### Answer responsibility → Individual bounded question

1. **Crosses:** no general reverse binding found.
2. **Standing changes:** none.
3. **Does not change:** an answering surface does not establish individual question identity.
4. **Evidence:** bounded question producer is explicit caller input only.
5. **Authority/warrant:** explicit caller question production required.
6. **Producer:** none found.
7. **Consumer:** none found.
8. **Refusal/Unknown:** Relationship Unknown.
9. **Class:** adjacency without exchange.
10. **Relation:** disconnected direct road.

### Answer responsibility ↔ Answer

#### Answer responsibility → Answer

1. **Crosses:** local expectation and responsible surface identify which surface may produce an answer-bearing artifact.
2. **Standing changes:** dispatch/explanation can reach an answer surface.
3. **Does not change:** responsibility does not guarantee sufficiency, completion, or universal answer engine.
4. **Evidence:** bounded ask dispatch map and local surfaces; family explanation.
5. **Authority/warrant:** exact family eligibility or local surface invocation.
6. **Producer:** bounded ask dispatch or direct CLI surface.
7. **Consumer:** local formatter/JSON result.
8. **Refusal/Unknown:** missing args, diagnostic-only, no evidence, local Unknowns.
9. **Class:** implementation-backed mediated connection.
10. **Relation:** mediated by family-local surfaces.

#### Answer → Answer responsibility

1. **Crosses:** produced answer can testify which surface produced it and which limitations/Unknowns it preserved.
2. **Standing changes:** local responsibility may be evidenced as fulfilled for response availability.
3. **Does not change:** answer does not rewrite responsibility, add a family row, or prove completion.
4. **Evidence:** local output formats and family row metadata.
5. **Authority/warrant:** surface-local support path.
6. **Producer:** local answer surface.
7. **Consumer:** surveys/operators.
8. **Refusal/Unknown:** answer may include Unknowns or refusal.
9. **Class:** implementation-backed local feedback.
10. **Relation:** direct local, not universal.

### Answer ↔ Completion

#### Answer → Completion

1. **Crosses:** at most local response availability or local completed-result reference where the surface explicitly says so.
2. **Standing changes:** an examination completed result supplied to frontier changes work classification to examined; a CLI answer proves the surface returned output.
3. **Does not change:** answer does not automatically establish bounded-question sufficiency, inquiry completion, examination campaign completion, or retirement.
4. **Evidence:** examination frontier boundary notes; work selection no-selection not completion; terrain survey negative finding.
5. **Authority/warrant:** local explicit completion/result evidence.
6. **Producer:** local surface or supplied existing result reference.
7. **Consumer:** frontier classification or report.
8. **Refusal/Unknown:** answer with Unknowns; examined but not understood/admitted/complete.
9. **Class:** implementation-backed local connection plus explicit refusal boundary against universalization.
10. **Relation:** local/direct where explicit; otherwise disconnected.

#### Completion → Answer

1. **Crosses:** completed result reference can be evidence that some work result exists, but the frontier does not render that answer.
2. **Standing changes:** work may be classified examined.
3. **Does not change:** completion status does not produce an answer text or prove question answered.
4. **Evidence:** `WorkResultReference.result_state == completed` classification logic.
5. **Authority/warrant:** matching result identity and hash/work/capability/convention.
6. **Producer:** supplied result reference consumed by frontier.
7. **Consumer:** frontier classification.
8. **Refusal/Unknown:** mismatched existing result errors; epistemic admission remains Unknown.
9. **Class:** implementation-backed direct classification, not answer production.
10. **Relation:** mediated/incidental.

### Completion ↔ Retirement

#### Completion → Retirement

1. **Crosses:** no automatic crossing found.
2. **Standing changes:** none.
3. **Does not change:** completion/examined/answered does not imply retirement, supersession, archival, frontier removal, or invalidation.
4. **Evidence:** negative searches and frontier boundary notes; prior reports warn answered != retired.
5. **Authority/warrant:** explicit retirement owner would be required; none found.
6. **Producer:** none found.
7. **Consumer:** none found.
8. **Refusal/Unknown:** Relationship Unknown / insufficient visibility.
9. **Class:** disconnected road / explicit refusal boundary.
10. **Relation:** disconnected.

#### Retirement → Completion

1. **Crosses:** historical archival language may preserve prior findings, but no live runtime retirement status feeds completion.
2. **Standing changes:** none.
3. **Does not change:** archive/history does not prove completion unless the archived artifact itself supports it.
4. **Evidence:** documentation/history review; no implementation owner found.
5. **Authority/warrant:** artifact-specific historical evidence only.
6. **Producer:** historical reports, not runtime.
7. **Consumer:** conflict/history review.
8. **Refusal/Unknown:** insufficient visibility.
9. **Class:** historical/report-only, not live implementation.
10. **Relation:** incidental.

## Direct connections recovered

- Bounded-goal condition → Inquiry Need: exact selected goal/horizon/evidence testimony to inquiry-need buckets.
- Inquiry Need → bounded-goal condition: read-only inquiry-need classification back as local evidence only.
- QuestionFamily → Answer responsibility: row-internal answer responsibility, surface, boundary, and diagnostic relationship.
- QuestionFamily → bounded ask dispatch/answer surface: exact eligible rows dispatch to local surfaces.
- QuestionFamily → family explanation: exact known/unknown definitions and composed explanation.
- Individual bounded question → examination frontier: bounded question identity/provenance/text crosses into inquiry reference.
- Examination frontier → method/policy/selection/probe request: eligible work can be selected under policy and bound into a probe request.
- TypedUnknownRecord → public unknown compatibility shape: typed record projects to `{area, reason}` and loses public type.
- Completed result reference → examination frontier examined classification: local completion-like input classifies work as examined.

## Mediated connections recovered

- Bounded-goal condition → Inquiry Need → bounded inquiry frontier: mediated by selected inquiry need and boundary testimony; does not form a question.
- Typed Unknown → Question Shape → Survey Warrant Family: mediated by methodological discipline; does not select family or wording.
- Typed Unknown → Question Shape → QuestionFamily: only as possible analysis/correspondence; admission still requires exact inventory row.
- QuestionFamily → answer responsibility → family-local answer surface: mediated by bounded ask selection/dispatch; does not create universal answer engine.
- `constitutional pipeline` QuestionFamily → explicit required args → individual bounded question → view selection/composition: implementation-backed special-case road.
- Individual bounded question → examination frontier → policy → work selection → probe request: implementation-backed examination road; does not execute examination.
- Answer → local evidence/status → completion-like classification: local and explicit only.

## Constitutional correspondences

- Question Shape corresponds to QuestionFamily only where a row exposes shape-like evidence, but correspondence is not registration.
- Survey Warrant Family corresponds to Question Shape as discipline for bounded surveys, evidence posture, confidence, unsupported conclusions, and stop.
- Typed constitutional Unknown states correspond to lawful question limits: evidence gap, implementation unknown, relationship unknown, boundary unknown, and methodological unknown each constrain conclusion strength.
- QuestionFamily rows may be evidence in a survey, but survey warrant does not change row standing.

## Methodological exchanges

- Survey warrant receives implementation evidence from QuestionFamily inventory and app-visible surfaces.
- Survey warrant sends conclusion-strength boundaries back into claims about QuestionFamily and Question Shape.
- Question Shape receives Unknown constraints as question discipline, not wording generation.
- Reports may preserve possible roads, missing adapters, and required equivalence proofs without implementing them.

## Refusal boundaries

- selected for inquiry consideration != inquiry opened != question formed != work authorized.
- Inquiry Need != formed question and does not select a question.
- typed Unknown != generic unknown field and does not select/refuse a QuestionFamily.
- Question Shape != QuestionFamily and does not register a family.
- Survey Warrant Family != QuestionFamily eligibility.
- QuestionFamily != individual bounded question; family identity != instance identity.
- Individual bounded-question testimony != family eligibility or established fact.
- Frontier membership != selection.
- Eligible examination work != selected/authorized/executed work.
- Answer != completion.
- Completion/examined != retirement.

## Disconnected roads

- TypedUnknownRecord → inquiry-need projection: no implementation consumer.
- Inquiry Need → TypedUnknownRecord: no implementation producer preserving `unknown_type`.
- Typed Unknown → QuestionFamily selection/admission/refusal: no direct handoff.
- Question Shape → QuestionFamily registration: no registration owner.
- Individual bounded question → QuestionFamily derivation: no free-text or artifact classifier.
- Bounded inquiry frontier → individual bounded question: report-only possible road, no live adapter.
- QuestionFamily ↔ bounded inquiry frontier: vocabulary adjacency only.
- Answer responsibility → individual bounded-question establishment: no reverse producer.
- Completion → retirement: no live universal owner.

## Unknown edges

- Whether typed constitutional Unknown states should ever constrain family consideration directly remains Relationship Unknown.
- Whether some registered QuestionFamilies are best described as projections of Question Shapes, correspondences, or separate identities varies by family and is not globally resolved.
- Whether a bounded inquiry frontier can or should admit multiple individual bounded questions is Unknown.
- Whether selected constitutional views answer an individual bounded question with sufficiency is Unknown.
- Whether an examined result is admitted as knowledge is Unknown.
- Whether any family-local completion can lawfully retire a question/frontier item is Unknown.

## Jigsaw map

```text
[bounded-goal condition]
  --implementation direct: exact selection/horizon/testimony-->
[inquiry need]
  --implementation mediated through selected need + boundary clauses-->
[bounded inquiry frontier]
  --report-only possible road; no live adapter--X
[individual bounded question]

[typed Unknown]
  --implementation direct only locally-->
[public unknown compatibility shape]
  --methodological correspondence-->
[Question Shape]
  --methodological/constitutional exchange-->
[Survey Warrant Family]

[Question Shape]
  --constitutional correspondence; no admission-->
[QuestionFamily]

[QuestionFamily]
  --implementation direct row-internal-->
[answer responsibility]
  --implementation mediated by local surface-->
[answer]
  --local/explicit only; refusal boundary-->
[completion]
  --disconnected/Unknown--X
[retirement]

[QuestionFamily: constitutional pipeline]
  --special implementation road with explicit args-->
[individual bounded question]
  --implementation direct with supplied corpus/work-->
[examination frontier]
  --implementation mediated: method/policy/selection-->
[selected examination work]
  --implementation mediated-->
[probe request]
  --explicit refusal boundary--X
[execution/performed examination]
```

Edge labels mean:

- `implementation direct`: live code/test-backed artifact crossing.
- `implementation mediated`: live code/test-backed crossing requiring named intermediate artifacts.
- `methodological/constitutional exchange`: survey or warrant discipline, not runtime handoff.
- `report-only possible road`: prior report identifies possible missing responsibility, not current implementation.
- `--X`: refusal/disconnected boundary.

## Conflict and history review

- Earlier reports sometimes saw a plausible bounded-goal-to-question or frontier-to-question road. Current implementation supports bounded-goal-to-inquiry-need and inquiry-need-to-frontier roads, but not frontier-to-`BoundedConstitutionalQuestion` production.
- Later implementation strengthened exact `QuestionFamily` bounded ask mechanics: inventory rows, eligibility, required args, presentation handoff, dispatch selection, and diagnostic relationships. That can make QuestionFamily look like routing mechanics, but row evidence also preserves answer responsibility and authority boundary.
- Recent reports sometimes flatten typed Unknowns into public `unknowns` fields. Current implementation confirms typed Unknowns lose `unknown_type` when projected to public dictionaries, while constitutional reports preserve broader typed Unknown states.
- Individual bounded-question artifacts became implementation-visible and therefore easy to over-center. They are important for constitutional pipeline and examination roads, but they do not define QuestionFamily, Inquiry Need, or bounded inquiry frontier.
- Old disconnected roads gained partial implementation in adjacent areas: bounded-goal focus selection, horizon, inquiry-need projection, bounded inquiry frontier, examination frontier, policy, work selection, and probe request. The missing connective tissue remains specific: goal/frontier pressure still does not become an individual bounded question or QuestionFamily.
- Several apparent connections exist only because artifacts share vocabulary: `inquiry` in QuestionFamily rows does not connect to Inquiry Need; `frontier` in bounded inquiry and examination roads does not make one frontier type; `unknown` fields do not prove typed Unknown records; `answer` fields do not prove completion.

## Visibility ledger

### Implementation modules inspected

`seed_runtime/question_surface_inventory.py`; `seed_runtime/typed_unknowns.py`; `seed_runtime/goal_inquiry_consideration_selection.py`; `seed_runtime/bounded_advancement_horizon.py`; `seed_runtime/inquiry_need_projection.py`; `seed_runtime/bounded_inquiry_frontier.py`; `seed_runtime/inquiry_frontier_boundary_testimony.py`; `seed_runtime/bounded_constitutional_question.py`; `seed_runtime/constitutional_pipeline.py`; `seed_runtime/constitutional_view_selection.py`; `seed_runtime/constitutional_view_composition.py`; `seed_runtime/candidate_examination_work.py`; `seed_runtime/examination_frontier.py`; `seed_runtime/examination_method_applicability.py`; `seed_runtime/examination_policy_projection.py`; `seed_runtime/examination_work_selection.py`; `seed_runtime/examination_probe_request.py`; `scripts/seed_local.py`.

### Tests inspected

`tests/test_question_surface_inventory.py`; `tests/test_bounded_constitutional_question.py`; `tests/test_constitutional_pipeline.py`; `tests/test_constitutional_question_projection.py`; `tests/test_constitutional_view_selection.py`; `tests/test_inquiry_need_projection.py`; `tests/test_goal_inquiry_consideration_selection.py`; `tests/test_bounded_advancement_horizon.py`; `tests/test_bounded_inquiry_frontier.py`; `tests/test_examination_frontier.py`; `tests/test_examination_method_applicability.py`; `tests/test_examination_policy_projection.py`; `tests/test_examination_work_selection.py`; `tests/test_examination_probe_request.py`; `tests/test_candidate_examination_work.py`.

### Reports recovered

`constitutional_question_terrain_survey_001.md`; `constitutional_question_family_reconciliation_investigation.md`; `question_shape_question_family_relationship_scout.md`; `question_shape_family_bridge_survey.md`; `typed_unknown_characterization.md`; `unknown_currency_survey.md`; `question_family_registration_boundary_audit.md`; `question_to_inquiry_transition_characterization.md`; `inquiry_eligibility_characterization.md`; `constitutional_bounded_goal_question_bridge_001.md`; `constitutional_bounded_question_origination_topology_001.md`; `constitutional_bounded_question_frontier_topology_001.md`; `bounded_inquiry_frontier_question_handoff_audit_001.md`; plus nearby topology, implementation, bounded ask, and answer-responsibility reports found by repository search.

### Historical commits or PRs consulted

No separate git-history excavation was needed to establish the live atlas because current implementation, tests, and existing historical reports supplied enough evidence. History-sensitive conclusions are therefore stated as report/implementation comparison, not commit archaeology.

### App-visible surfaces exercised

`--question-surface-inventory`, `--question-family-explanation`, `ask --question-family`, `--reasoning-path`, and `--selection-path` were exercised as read-only visibility surfaces.

### Searches that produced no evidence

No live owner found for `QuestionFamilyRegistration`, `RecoveredQuestionFamily`, Unknown-to-family selection, frontier-to-question production, answer-to-completion, completion-to-retirement, `retired` status, archival-driven frontier removal, or universal answered status.

### Ambiguous or duplicated vocabulary

`question`, `inquiry`, `frontier`, `unknown`, `answer`, `completion`, `selection`, `eligibility`, `family`, `shape`, and `responsibility` recur in multiple owners with different standings. The atlas preserves owner-local meaning rather than merging vocabulary.

### Unresolved repository visibility limitations

- App-visible surfaces expose outputs, not every internal decision path.
- Some reports may accurately describe earlier states not reconstructed by commit history here.
- Retirement remains especially under-visible as a live implementation territory.
- Question Shape and Survey Warrant Family remain primarily report/methodology territories, so executable proof is not expected unless a row or runtime artifact separately exists.

## Smallest truthful description of the current jigsaw

The current repository does not contain one question pipeline. It contains several lawful exchange zones. Exact `QuestionFamily` rows provide public answerability identity, answer responsibility, bounded ask eligibility, and dispatch to local answer surfaces. Individual `BoundedConstitutionalQuestion` artifacts preserve caller testimony and can feed the constitutional pipeline and examination frontier roads. Bounded-goal condition can project inquiry need, and inquiry need can assemble a bounded inquiry frontier through boundary testimony, but that road does not currently produce an individual bounded question or a QuestionFamily. Typed Unknowns preserve unresolved standing and constrain conclusion strength methodologically; they do not select or refuse families. Question Shape and Survey Warrant Family discipline how surveys ask and conclude, while exact `QuestionFamily` admission remains implementation-owned. Answers are local artifacts; completion is local and explicit; retirement is not automatically connected.

Constitutional question connection survey 001 complete.
