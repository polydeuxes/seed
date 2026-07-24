# BoundedOperatorGoalEstablishment asymmetrical characterization

## Scope and non-goals

This is one bounded, report-only characterization of the current active
`BoundedOperatorGoalEstablishment` implementation after PR 1970.  Runtime and test
search recovers exactly two producers: the closed-choice producer and the
admitted-interpretation producer.  The report treats those roads independently
before comparing them.  It does not amend production code, tests, serialization,
exports, CLI/API behavior, the canonical Book, or an existing report.  It does not
propose decomposition, renaming, replacement, relocation, or deletion.

The controlling implementation distinctions are:

* a selected identity is not thereby constitutional scope;
* a reasoning act is not a standing transition;
* an upstream act is not repeated merely because its result is inspected or
  preserved downstream;
* absence of a dimension from this artifact is not evidence that the whole road
  lacks that dimension; and
* heterogeneous fields do not by themselves make a mixed artifact malformed.

“Demand” below means an implementation-backed pressure family, “Gap” means the
standing absent at the producer boundary, and “Question” means a bounded question
actually asked or answered.  They are not synonyms.  No code path here declares a
Demand artifact or a Question artifact, so neither is invented.

## Independent closed-choice road

### Road and pressure topology

`PresentedClosedChoiceSet` and `OperatorSelectionTokenCapture` are inputs to
`bind_closed_choice_selection`.  That producer checks that both name the same
choice set, looks up the captured token only in that exact set, and produces a
`ClosedChoiceSelectionBinding`.  Conflict, unsupported-token, and unknown evidence
prevent a bound option.  The binding explicitly stops before applying the option
to a goal and records `applied_to_goal=False`.

`establish_bounded_operator_goal_from_closed_choice` then consumes that already
answered binding.  It rejects the wrong artifact type.  A binding whose state is
`bound` and whose `bound_option_ref` is nonempty yields `established`; every other
binding yields `refused`.  The producer does not bind the token again.

| Pressure item | Independently recovered answer |
|---|---|
| Demand | **Unknown.** No named Demand family or Demand artifact is consumed or produced on this road.  The presented prompt is input to token binding, not implementation proof of a Demand. |
| Gap | Before this producer, the selected option lacks bounded-operator-goal standing: the binding explicitly says it is not a goal transition and has `applied_to_goal=False`.  This is a **constitutional standing gap**, not an epistemic search gap. |
| Question | The presented closed-choice `prompt` is explicit upstream presentation testimony.  Token lookup answers that bounded presented choice.  Goal establishment consumes the answered binding; it asks no new Question and does not carry the prompt into the goal artifact. |
| Required standing | An exact binding with `binding_state == "bound"` and a nonempty `bound_option_ref`. |
| Present standing | Exact-set-local option selection (`bound`) plus its binding reason and evidence dispositions; not goal standing, authority, inquiry movement, or execution. |
| Remaining gaps | Goal scope/locality beyond selected identity; a present advancement boundary; any later clarification, inquiry, authority, or operational-realization need; authorization, execution, satisfaction, and recording.  Caller-supplied `unresolved_scope` and `known_loss`, and binding unsupported/unknown/conflict evidence, remain visible rather than being solved. |

### Capabilities

| Capability | Competence and realization | State sequence and produced artifact/standing |
|---|---|---|
| Exact closed-choice token binding | `bind_closed_choice_selection` can relate one captured token to one option in one fingerprinted presented set. | Available as a function; applicable only to matching choice-set refs; it **selects/binds** the option when the token is present and evidence is neither unknown nor conflicting; it neither authorizes nor executes.  It produces `ClosedChoiceSelectionBinding` with `bound`, `unsupported`, `unknown`, or `conflict` standing. |
| Bounded goal establishment from a binding | `establish_bounded_operator_goal_from_closed_choice` can accept or refuse the exact binding as bounded goal ingress. | Available as a producer and applicable to the required artifact type.  It consumes the upstream selection; it does not select.  It is not authorization or execution.  It produces `BoundedOperatorGoalEstablishment.establishment_state` of `established` or `refused`. |

The code does not name a canonical capability family for either competence.

### Reasoning acts

| Act | Inputs, assertion, strength, owner, warrant, defeater, location |
|---|---|
| Selection/binding | The binding producer consumes the exact choice set, capture, and supplied evidence.  It asserts that a token belongs to one exact set and identifies its option.  Strength is exact-set-local `bound`, not universal meaning or goal standing.  `bind_closed_choice_selection` owns it; exact choice-set identity and membership warrant it.  mismatched sets raise; conflict, unknown, or absent membership defeat binding.  **Upstream.** |
| Preservation | Goal establishment copies the upstream unknowns and conflicts, carries unsupported evidence into `unresolved_scope`, and retains binding/choice-set/fingerprint/capture lineage.  Strength is traceability, not renewed selection.  The goal producer owns the preservation; the binding fields warrant it.  Malformed external objects are not separately distinguished beyond artifact type/state/ref checks.  **Local.** |
| Establishment | The goal producer consumes bound standing and asserts that it supplies bounded operator goal standing.  Strength is `established`, explicitly not authorization or execution.  The producer owns it; `binding_state == "bound"` plus a nonempty option ref warrants it.  Any non-bound state or missing ref defeats it and produces `refused`.  **Local.** |
| Abduction, induction, deduction, applicability judgment, admission | **Unknown/not recovered on this road.** Token membership is not classified as deduction; no candidate generation, recurrence generalization, consumer-contract applicability, or admission artifact occurs. |

## Independent admitted-interpretation road

### Road and pressure topology

This road arrives with several independently owned upstream acts.  A contextual
warrant producer has assessed candidate-scoped supplied evidence.  A selection
producer has selected exactly one warranted candidate only from explicit
candidate-bound selection evidence.  An applicability producer has judged that
selected candidate against one supplied bounded consumer contract and snapshotted
the selected meaning.  An admission producer has admitted (or declined to admit)
it to exactly one consumer and purpose.  Its boundary explicitly says admitted is
not consumed and `goal_established=False`.

`establish_bounded_operator_goal_from_admitted_interpretation` consumes those
carried results without regenerating warrants, reselecting, recomputing
applicability, or recomputing admission.  It additionally validates that consumer,
purpose, selection, projection, and selected-candidate identities match its exact
intake boundary.  Only an admitted, applicable, identity-consistent result with a
selected object/ref and no collected unknowns or conflicts is established.

| Pressure item | Independently recovered answer |
|---|---|
| Demand | **Unknown.** `BoundedDownstreamPurpose` identifies a purpose and consumer contract, but no implementation-backed Demand family is present. |
| Gap | Before this producer, an applicable selected interpretation is consumer-locally admitted but not yet consumed and has no goal-established standing.  The missing standing is a **constitutional consumer-local establishment gap**.  Upstream unknowns can be epistemic testimony, but they cause refusal rather than define the local gap. |
| Question | **None recovered.** This road consumes a selection, applicability judgment, and admission already made.  Neither producer signature nor artifact identifies a bounded Question. |
| Required standing | Exact `DownstreamInterpretationAdmission` artifact; the fixed bounded-goal consumer and purpose; matching admission/projection/selection/candidate identities; `admitted=True`, `outcome="admitted"`; projection `applicability="applicable"`; selected object and ref; no aggregated unknowns or conflicts. |
| Present standing | A warranted candidate selected upstream, judged applicable for one consumer contract, and admitted to this exact consumer/purpose.  It is still `consumed_by_consumer=False` and `goal_established=False` in the ingress artifact. |
| Remaining gaps | Residual source material, known refusals, applicable-but-unadmitted reasons, candidate known loss, and all preserved unknown/conflict testimony; constitutional scope/locality beyond identity; advancement horizon and all later need-family characterization; correction application, inquiry movement, authority, execution, presentation, recording, state mutation, and cluster mutation. |

### Capabilities

| Capability | Competence and realization | State sequence and produced artifact/standing |
|---|---|---|
| Candidate-scoped warrant assessment | The warrant producer relates supplied candidate-local evidence to a candidate. | Available upstream; applicability to a candidate follows explicit refs; it produces warrant standing.  It does not select, authorize, or execute. |
| Contextual interpretation selection | `select_contextual_interpretation` accepts explicit candidate-bound selection evidence only for a warranted candidate. | Available upstream; applicable when evidence names a known warranted candidate; selected there, but not admitted/authorized/executed.  Produces `ContextualInterpretationSelectionResult`. |
| Purpose-local applicability judgment | `project_interpretation_applicability` evaluates the selected meaning against a supplied consumer contract and explicit requirement evidence. | Available upstream; applicable to one selected result/purpose; no selection; no authorization/execution.  Produces `InterpretationApplicabilityProjection` with applicable/inapplicable/unknown/conflict. |
| Consumer-local admission | `admit_downstream_interpretation` evaluates explicit admission evidence for the exact selection, projection, candidate, purpose, and consumer. | Available upstream; applicable evidence is identity-local; admission is distinct from selection and applicability; no authorization/execution.  Produces `DownstreamInterpretationAdmission`. |
| Bounded goal establishment from admission | The local producer validates and consumes the admitted result as bounded goal ingress. | Available locally and applicable only to the exact artifact and intake identity.  It neither selects nor authorizes nor executes.  It produces established/refused goal standing. |

Closed-choice binding and admitted-interpretation consumption are **different
capability sequences closing the same recovered local standing gap**: neither
ingress has bounded-goal establishment before the local producer, and both can
supply it.  The repository does not establish that the full sequences are two
realizations of one named canonical capability family.

### Reasoning acts

| Act | Inputs, assertion, strength, owner, warrant, defeater, location |
|---|---|
| Warrant assessment | Candidate, exact source spans, corrections, retrospective/clarification evidence, and explicit unknown/conflict/loss inputs yield candidate-local warrant standing.  `produce_contextual_interpretation_warrant_set` owns it.  Supporting without contradiction warrants `warranted`; contradiction, ambiguity, unknown/conflict, unresolved evidence, or no support defeats that standing.  **Upstream.** |
| Selection | Candidate-bound selection evidence plus warranted candidates yields exactly one selected ref/object.  Strength is selected interpretation, not applicability.  The selection producer owns it; explicit evidence naming one warranted candidate warrants it.  Unknown/unwarranted or multiple refs defeat it.  **Upstream and only consumed locally.** |
| Applicability judgment | Selected result, bounded purpose/consumer contract, and requirement evidence yield a purpose-local applicability assertion.  The applicability producer owns it; complete satisfied requirements warrant `applicable`.  Foreign, conflicting, refused, unsatisfied, missing, or unknown evidence defeats it.  **Upstream and only checked locally.** |
| Admission | Projection plus exact consumer-local admission evidence yields admitted/unadmitted/unknown/conflict.  The admission producer owns it; matching `admit` evidence on an applicable projection warrants admission.  Foreign/missing/refusing/unknown/conflicting evidence defeats it.  **Upstream and only checked locally.** |
| Preservation | The goal producer collects candidate/projection/admission unknowns and conflicts, known loss, refusals/residuals, four lineage lanes, and the snapshot.  This grants traceability only.  Carried objects warrant the copies; inconsistent identities become local conflict/refusal.  **Local.** |
| Establishment | The exact admission and its carried projection/selection yield “consumer-local admitted interpretation supplies bounded operator goal standing.”  Strength is established goal standing, not authorization.  Goal establishment owns it.  Intake identity, admission, applicability, absence of unknown/conflict, and selected identity warrant it; each explicit guard can defeat it.  **Local.** |
| Abduction | **Unknown.** Candidates are supplied to the warrant producer; no active implementation here identifies candidate generation as abduction. |
| Induction | **Unknown.** Retrospective evidence is classified, but no recurrence generalization is implemented or named. |
| Deduction | **Unknown.** Applicability and admission use deterministic branches, but implementation does not assert a deductive consequence relation; an applicability label is not treated as deduction. |

## Demand and Gap recovery

Neither road supplies an implementation-backed Demand family.  The closed-choice
prompt and the admitted road's bounded purpose are not silently promoted to
Demand.  The closed-choice road has an upstream bounded presented choice; the
admitted road has no recovered Question.  Both local calls nevertheless encounter
the same exact missing standing: their ingress can orient one identity but has not
established a bounded operator goal.  The producer either closes that
constitutional gap or records refusal.  This common Gap does not prove a common
Demand.

## Local producer act

Across both roads, the common new constitutional act is **accepting or refusing
lawful ingress as bounded-operator-goal standing and issuing a stable witness of
that local decision**.  It does not make the upstream selection.  On the admitted
road it also performs consumer/purpose and carried-identity intake validation; on
the closed-choice road it performs the narrower bound-state/ref check.  Those
asymmetrical guards explain why the establishment acts share an output standing
without sharing all reasoning.

## Field production/preservation matrix

“Generic” means common dataclass/serialization mechanics, not constitutionally new
testimony.  A refused result can make content/scope empty while retaining the same
classification of how the producer obtains the field.

| Output field | Closed-choice road | Admitted-interpretation road |
|---|---|---|
| `artifact_type` | Generic serialization/type surface; constant locally. | Same. |
| `goal_establishment_id` | **Identity mechanism**, newly derived from ingress, local state/content/scope/evidence inputs, and convention. | **Identity mechanism**, newly derived from admission, local state, selected ref, aggregated unknown/conflict/unresolved testimony, and convention. |
| `ingress_artifact_type` | Copied upstream testimony (`binding.artifact_type`). | Copied upstream testimony (`admission.artifact_type`). |
| `ingress_artifact_ref` | Copied upstream binding identity. | Copied upstream admission identity. |
| `ingress_lineage` | Derived here by normalized union of binding id, choice-set ref/fingerprint, and capture ref. | Derived here by normalized union of all four upstream reference lanes. |
| `establishment_state` | **Newly established here** from bound state/ref. | **Newly established here** from the full local guard sequence. |
| `establishment_reason` | **Producer-local standing explanation** for establishment/refusal. | Same, with road-specific refusal explanations. |
| `intended_outcome` | Selected upstream label (or ref fallback) **preserved here** only when established. | **Derived here from admitted evidence** using proposed meaning, then label, then selected-ref fallback, only when established.  The meaning itself was produced upstream. |
| `known_scope` | Selected upstream option ref preserved here.  Implementation evidence characterizes it as selected identity, not constitutional scope. | Selected ref plus upstream label derived/normalized here.  These are identity/content testimony, not recovered locality bounds. |
| `unresolved_scope` | Derived union of caller-supplied unresolved values and upstream unsupported evidence. | Derived union of upstream known refusals, applicable-but-unadmitted reasons, and residual source span refs. |
| `unknowns` | Copied/normalized upstream unknown-selection evidence. | Derived union of selected candidate, applicability, and admission unknowns. |
| `conflicts` | Copied/normalized upstream conflicting-selection evidence. | Derived union of candidate/applicability/admission conflicts plus producer-local identity/consumer/purpose mismatches. |
| `known_loss` | Copied/normalized caller testimony. | Copied/normalized selected candidate known loss. |
| `upstream_source_material_refs` | Generic default empty tuple; no road-specific testimony is populated. | Derived here from selection identities, snapshot source/residual spans, and projection provenance. |
| `upstream_selection_refs` | Generic default empty tuple. | Derived here from selection-result and selected-candidate identities. |
| `upstream_applicability_refs` | Generic default empty tuple. | Derived here from projection identity/provenance. |
| `upstream_admission_refs` | Generic default empty tuple. | Derived here from admission identity, evidence refs, and provenance. |
| `consumed_admitted_meaning_snapshot` | Generic default `None`. | Copied upstream testimony: the applicability producer's dataclass snapshot of the selected candidate. |

## Eight-dimensional characterization by road

Each cell separates distinct testimony instead of treating every field associated
with a dimension as one blended answer.

### Closed-choice result

| Dimension | Exact testimony, source, production status, explicitness, further owner |
|---|---|
| Subject / identity | `goal_establishment_id` explicitly identifies this local witness (producer-local); `ingress_artifact_ref/type` explicitly identify the binding (preserved); `known_scope` carries the selected option identity (preserved).  The established goal's identity beyond these mechanisms is implicit/Unknown. |
| Assertion / content | `intended_outcome` explicitly carries the selected option label or ref, preserved from binding; state/reason explicitly assert whether that ingress supplies goal standing, newly established locally. |
| Standing | `establishment_state` and `establishment_reason` are explicit, producer-owned establishment/refusal testimony.  Binding standing remains upstream and is not rewritten. |
| Source / provenance | `ingress_lineage` explicitly carries binding, set, fingerprint, and capture refs, assembled locally from upstream testimony.  Choice-set and capture provenance themselves are not copied: deeper provenance is delegated through the ingress artifact. |
| Responsibility | The function boundary implicitly assigns binding to the binding producer and establishment to this producer.  No explicit responsibility field exists.  Later horizon/need responsibilities are separate consumers. |
| Authority / warrant | Bound state plus nonempty option ref is the explicit local warrant condition; the binding reason and exact fingerprint remain upstream.  No authority is granted.  Transferable authority is absent. |
| Scope / locality | The only explicit localities are upstream exact-choice-set identity and optional caller/unresolved evidence.  `known_scope` is selected identity, not a recovered scope boundary.  Constitutional goal locality is **Unknown**; `BoundedAdvancementHorizon` owns later supplied included/excluded/present boundary testimony. |
| Occurrence / preservation | Stable id records this deterministic occurrence; lineage, unknowns, conflicts, unsupported evidence, and known loss are preserved.  Time, event-ledger occurrence, and durable recording are absent.  Serialization is generic and no later recording owner is identified here. |

### Admitted-interpretation result

| Dimension | Exact testimony, source, production status, explicitness, further owner |
|---|---|
| Subject / identity | Local stable id identifies the witness; ingress id/type identify the admission; selected ref appears in `known_scope` and `upstream_selection_refs`; snapshot `candidate_ref` may restate it.  Admission/projection/selection identities are explicit and preserved/assembled. |
| Assertion / content | `intended_outcome` is locally chosen from the already admitted selected candidate's proposed meaning/label/ref.  The complete `consumed_admitted_meaning_snapshot` preserves upstream content.  Local state/reason newly assert establishment/refusal. |
| Standing | Candidate warrant, selection, applicability, and admission standings are delegated to and preserved through their upstream artifacts/refs; only goal `establishment_state/reason` is newly explicit here. |
| Source / provenance | Four explicit upstream ref lanes plus union lineage and snapshot source/residual span refs are assembled locally.  They preserve source and procedural provenance without recreating upstream acts. |
| Responsibility | Purpose/consumer refs remain in the ingress admission, and local constants/guards make bounded-goal establishment the implicit consumer responsibility.  No explicit responsibility field exists in the goal.  Later horizon/need owners remain downstream. |
| Authority / warrant | Exact consumer/purpose/identity consistency, admitted outcome, applicable standing, no unknown/conflict, and selected identity are local warrant conditions.  Supporting evidence and requirement/admission evidence remain upstream.  No operational authority is granted. |
| Scope / locality | Consumer/purpose locality is explicit upstream and validated locally.  `known_scope` contains selected identity and label, not proven constitutional scope.  Residual/refusal material appears in `unresolved_scope`.  Further advancement locality is delegated to the horizon producer; goal scope beyond identity remains **Unknown**. |
| Occurrence / preservation | Stable id identifies local deterministic production.  Snapshot, known loss, unresolveds, unknowns, conflicts, and lineage lanes preserve the road.  Time, event-ledger occurrence, durable recording, and mutation are absent; upstream artifacts explicitly deny recording/mutation. |

## Consumer recovery

Active runtime search finds the following constitutional consumers.  Imports,
exports, JSON conversion, and test construction are excluded as generic or
non-constitutional use.

| Consumer | Minimum testimony and fields read | Assumed treatment and further characterization |
|---|---|---|
| `establish_bounded_advancement_horizon` | Requires `artifact_type == "BoundedOperatorGoalEstablishment"` and state other than `refused`; reads `goal_establishment_id`, `artifact_type`, `ingress_artifact_ref`, `ingress_lineage`, `unknowns`, and `conflicts`. | Treats it as an **establishment witness** for one goal identity, not as enough scope.  It separately requires `present_movement_boundary` and accepts included/excluded scope, evidence snapshots, time/current-state bounds, and need-family bounds. |
| `project_clarification_need` | Reads `goal_establishment_id` for payload/output and checks testimony's goal identity; horizon supplies evidence and boundary testimony. | Treats it as goal identity in an ingress handoff.  Explicit component testimony, not goal wording or unresolved fields, owns clarification characterization. |
| `project_inquiry_need` | Reads `goal_establishment_id` for payload/output and identity checks. | Same handoff treatment; repository-world uncertainty testimony and horizon own further inquiry characterization. |
| `project_authority_need` | Reads `goal_establishment_id` for identity/payload/output. | Same handoff treatment; separate authority requirement/standing testimony owns authority characterization. |
| `project_operational_realization_need` | Reads `goal_establishment_id` for identity/payload/output. | Same handoff treatment; separate realization requirement/standing testimony owns operational characterization. |

No active consumer reads `intended_outcome`, `known_scope`, `unresolved_scope`,
`known_loss`, the four upstream reference lanes, or the consumed snapshot.  No
consumer relies on every field as one indivisible whole.  The horizon does rely on
a coherent subset spanning type/state, goal identity, ingress provenance, and
negative testimony.

## Cross-road convergence

| Comparison | Closed-choice | Admitted interpretation |
|---|---|---|
| Demand | Unknown | Unknown |
| Gap | Bound option has no goal standing | Admitted applicable meaning is not consumed/goal-established |
| Capabilities | Exact token binding; goal establishment | Warrant, selection, applicability, admission; goal establishment |
| Reasoning acts | Upstream selection/binding; local preservation and establishment | Upstream warrant assessment, selection, applicability, admission; local preservation, intake validation, and establishment |
| Prior standing | Exact-set-local `bound` | Selected + purpose-locally applicable + consumer-locally admitted |
| Local act | Accept/refuse binding as bounded goal | Validate and accept/refuse admitted meaning as bounded goal |
| New output standing | Established/refused bounded operator goal witness | Established/refused bounded operator goal witness |
| Dimensional testimony | Compact binding/set/capture lineage; option content/identity; local state | Rich source/selection/applicability/admission lineage and snapshot; meaning/identity; local state |
| Remaining gaps | Advancement boundary and later dimensional/operational work | Same categories, plus preserved road residuals/loss/refusals |

The roads do **not** demonstrably share one upstream selected subject: an option ref
and an interpretation candidate ref arise under different identity regimes.  They
do share (1) one required local standing transition, from lawful but not-yet-goal
ingress to an established/refused bounded-goal witness; (2) one consumer
responsibility, this goal-establishment owner; and (3) one output contract.  That
is more than a common Python dataclass.  No common Demand or Question is recovered.

## Mixed-object characterization

The best bounded characterization is **a convergence handoff between different
ingress roads and a mixed artifact preserving multiple independently responsible
acts, organized around one coherent producer-owned establishment assertion**.
These descriptions are complementary rather than a decomposition claim.

* All established-path content values are intended to characterize the selected
  orientation accepted as one exact goal, but `goal_establishment_id`, ingress
  fields, lineage, state, and reason characterize the witness/establishment act,
  while upstream lanes and snapshot also characterize only the road.
* Removing type/state/reason or the ingress identity would make the local
  establishment claim or its immediate warrant unverifiable.  Removing upstream
  lanes/snapshot would especially weaken admitted-road auditability.  Current
  downstream behavior, however, does not require the entire artifact as a whole.
* One producer-owned assertion survives asymmetry: **this exact ingress does or
  does not supply bounded operator goal standing at this boundary**.
* The common subject is recoverable at that witness level.  The repository does
  not prove that `known_scope` supplies a common constitutional scope subject, nor
  that all carried road testimony is newly goal-owned.

Accordingly, field heterogeneity is explained by convergence, preservation, and
auditability.  It is not implementation evidence of malformation.

## Remaining gaps

1. Neither road identifies an implementation-backed Demand family.
2. Only the closed-choice road exposes an upstream presented prompt; no goal-level
   Question identity or question-answer relation is preserved.
3. The artifact does not establish constitutional scope/locality beyond selected
   identity and road-local consumer/purpose testimony; the advancement horizon
   separately owns the present movement boundary.
4. Responsibility and authority/warrant are mostly structural (producer boundary,
   guards, and upstream artifacts), not explicit goal fields.
5. No active consumer uses outcome/content, unresolved scope, known loss, detailed
   lineage lanes, or the snapshot; their current constitutional role is preserved
   audit testimony rather than consumer-required behavior.
6. No occurrence time, durable record, event-ledger write, or mutation standing is
   produced by the goal artifact itself.
7. Later clarification, inquiry, authority, and operational-realization dimensions
   require horizon-bound, component-specific testimony; authorization, execution,
   satisfaction, and presentation remain outside this producer.

## Unknowns

* Whether either ingress is generated in response to one shared Demand.
* Whether the admitted road answers any upstream bounded Question not represented
  by the active artifacts.
* Whether candidate generation is abductive, evidence assessment inductive, or
  any branch deductive; the implementation does not distinguish those acts.
* Whether the two complete roads instantiate one unnamed capability family.
* The constitutional goal scope denoted beyond the selected option/candidate
  identity, and whether labels in `known_scope` have any independent standing.
* A single explicit responsibility or authority field for the established goal;
  current ownership and warrant are recovered from function boundaries and guards.
* A downstream constitutional consumer for most preserved admitted-road detail.

## Final bounded conclusion

The closed-choice road consumes an exact-set-local selection already bound
upstream; the admitted-interpretation road consumes an independently warranted,
selected, purpose-locally applicable, and consumer-locally admitted meaning.  They
do not perform the same upstream reasoning and do not establish a shared Demand,
Question, or selected-identity regime.  They converge on the same exact absent
standing and producer responsibility: neither ingress is yet an established
bounded operator goal, and this producer alone accepts or refuses it as such.

`BoundedOperatorGoalEstablishment` is therefore coherently usable as one
establishment witness and output contract while also being an asymmetrical mixed
convergence handoff that preserves acts owned elsewhere.  Carried testimony is not
new testimony, selected identity is not scope, admission is not establishment,
and establishment is not authorization.  The recovered asymmetry supplies no
warrant to call the artifact malformed.
