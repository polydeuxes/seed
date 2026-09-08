# Bounded Operator Goal to Advancement Horizon Characterization

## Scope and non-goals

This report performs one report-only, asymmetrical characterization of the active
runtime handoff:

```text
BoundedOperatorGoalEstablishment
+ independently supplied horizon testimony
-> establish_bounded_advancement_horizon(...)
-> BoundedAdvancementHorizon
```

The evidence base is the two active producers, their focused tests, direct runtime
consumers, and the consumer tests named in the task.  Historical reports are not
treated as authority.  This report does not enter the internal correctness of the
four Need projections, the need-set assembler, or family-coverage production; it
uses those implementations only to identify reads and assumptions.  It does not
characterize downstream clarification, inquiry, authority, realization, selection,
sufficiency, authorization, or execution roads.  It proposes no implementation,
schema, naming, decomposition, relocation, or Book change.

Throughout, successful Python construction proves that the constructor's guards
passed for the supplied object.  It does not prove that a caller's testimony is
true, lawfully selected, applicable, admitted, or authorized.

## Independent goal-output recovery

`BoundedOperatorGoalEstablishment` is independently produced from either an exact
closed-choice binding or a consumer-local admitted interpretation.  The producer
newly asserts `establishment_state` and `establishment_reason`: the ingress does or
does not supply bounded-operator-goal standing.  On an established result it also
preserves goal content/identity testimony (`intended_outcome`, `known_scope`),
unresolved and adverse testimony, ingress identity and lineage, and—on the admitted
road—four upstream reference lanes and the selected-meaning snapshot.

This is **established goal standing**.  It is not a present movement boundary.  The
goal producer receives no `present_movement_boundary`, horizon included/excluded
scope, snapshot-reference set, time bound, current-state bound, or need-family
bound.  Its own `known_scope` is selected option/candidate identity testimony under
the current producers, not the horizon's current scope.  Its `intended_outcome` is
goal content, not an advancement direction chosen by the horizon.

The artifact can be directly instantiated, so its represented assertion is not
proof that either goal producer occurred.  When the actual producer call is
observed, its guards and upstream inputs warrant only the bounded goal
establishment assertion.  Nothing in that assertion authorizes movement.

## Independent horizon-producer recovery

The exact active signature is:

```python
establish_bounded_advancement_horizon(
    goal: BoundedOperatorGoalEstablishment,
    *,
    present_movement_boundary: str,
    included_scope: Iterable[str] = (),
    excluded_scope: Iterable[str] = (),
    evidence_snapshot_refs: Iterable[EvidenceSnapshotReference] = (),
    time_bounds: Iterable[str] = (),
    current_state_bounds: Iterable[str] = (),
    potentially_relevant_need_families: Iterable[str] = (),
    explicitly_excluded_need_families: Iterable[NeedFamilyExclusion] = (),
    unknowns: Iterable[str] = (),
    conflicts: Iterable[str] = (),
    stale_evidence_refs: Iterable[str] = (),
    unavailable_evidence_refs: Iterable[str] = (),
) -> BoundedAdvancementHorizon
```

There is no active selection argument.  The producer checks the goal's represented
type and rejects only `establishment_state == "refused"`; requires a nonempty
caller-supplied boundary; and requires a nonempty reason on every supplied need-
family exclusion.  It tuple-materializes snapshots and exclusions, stringifies,
drops empty strings from, and first-occurrence-deduplicates most string collections.
It does not validate snapshot internals, evidence state, boundary truth, scope
applicability, temporal truth, currentness, family legitimacy, or the source's
authority to supply any of them.

On success it emits `horizon_state="bounded"`.  Its module and boundary notes state
the narrower act: preservation of a supplied movement boundary for one bounded
goal identity, without producing the boundary's constitutional standing.  The
function name says “establish,” but implementation evidence does not support the
stronger claim that it independently selects, admits, or establishes the truth of
the boundary.

## Consumed and ignored goal fields

The following table recovers every goal field.  “Ignored” is local to this handoff,
not a claim of global irrelevance.

| Goal field | Horizon operation | Exact standing supplied here |
|---|---|---|
| `artifact_type` | Reads and validates exact literal; copies to `goal_artifact_type`; refusal also copies it. | Proof represented by the supplied object that it claims the bounded-goal artifact kind; a type guard, not goal content. |
| `goal_establishment_id` | Reads; copies; includes in bounded and refused stable-ID payloads. | Exact established-goal/witness binding identity.  It does not recover the goal's subject or content. |
| `ingress_artifact_type` | **Ignored.** | None at this handoff.  The horizon does not revalidate ingress kind. |
| `ingress_artifact_ref` | Reads; copies to `goal_ingress_artifact_ref`; success stable-ID input as `source`. | Immediate ingress provenance preserved around the goal witness, not present-state evidence. |
| `ingress_lineage` | Reads and copies to `goal_ingress_lineage`; not an ID input. | Preserved historical ingress lineage, not a current-boundary warrant. |
| `establishment_state` | Reads; refuses only literal `refused`; otherwise not copied. | Minimum negative gate: the supplied witness does not represent refusal.  No stronger state vocabulary is validated. |
| `establishment_reason` | **Ignored.** | No local restatement or validation of the goal producer's reason. |
| `intended_outcome` | **Ignored.** | No goal content, advancement direction, or boundary is derived from it. |
| `known_scope` | **Ignored.** | No horizon scope is derived from goal scope/identity testimony. |
| `unresolved_scope` | **Ignored.** | No automatic horizon unknown, exclusion, or Need is inferred. |
| `unknowns` | Reads, merges before caller `unknowns`, deduplicates, and copies on success/refusal. | Preserved adverse testimony about the goal/road; it does not itself defeat horizon construction. |
| `conflicts` | Reads, merges before caller `conflicts`, deduplicates, and copies on success/refusal. | Preserved conflict testimony; it does not itself defeat horizon construction. |
| `known_loss` | **Ignored.** | No loss characterization is transferred. |
| `upstream_source_material_refs` | **Ignored.** | No detailed upstream-source lane is transferred. |
| `upstream_selection_refs` | **Ignored.** | No selection standing is consumed or reconstructed. |
| `upstream_applicability_refs` | **Ignored.** | No applicability standing is consumed. |
| `upstream_admission_refs` | **Ignored.** | No admission standing is consumed. |
| `consumed_admitted_meaning_snapshot` | **Ignored.** | No meaning snapshot, goal subject, or content is recovered. |

Thus the horizon consumes the goal artifact as a minimum establishment witness and
identity/provenance carrier, not the established goal's semantic content.  It
consumes proof-as-represented that goal standing exists (type plus not-refused),
the exact goal id, shallow ingress provenance, and adverse testimony.  It does not
consume enough to recover what the goal seeks.  Two otherwise valid establishment
witnesses with different `intended_outcome`, `known_scope`, detailed upstream refs,
or admitted snapshots but the same goal id, ingress ref/lineage, unknowns/conflicts,
and caller inputs produce equal horizons.  Normally changing content through the
real goal producer changes the goal id; direct dataclass replacement demonstrates
the horizon itself is content-blind rather than proving such replacement lawful.

## Independent horizon inputs

All values below are supplied by the immediate caller.  No repository-derived
producer is required or inspected.  Tests create the strings and testimony objects
inline; active runtime code exposes no producer that independently establishes
their truth.

| Input | Exact subject | Validation / transformation | Standing before -> after | Responsibility, warrant, defeaters | Identity role |
|---|---|---|---|---|---|
| `present_movement_boundary` | The asserted present boundary around movement relative to this goal. | Nonempty only. | Caller assertion -> preserved in a `bounded` horizon, not constitutionally established. | Caller owns truth; nonempty string warrants construction; empty defeats. False, stale, unauthorized, or inapplicable content is not detected. | Yes: present-boundary identity. |
| `included_scope` | Material asserted inside the horizon. | Stringify, remove empty, first-occurrence dedupe. | Supplied inclusion -> preserved inclusion; not applicability. | Caller owns assertion; nonempty values warrant preservation; semantic overlap/conflict is unchecked. | Yes: boundary identity. |
| `excluded_scope` | Material asserted outside the horizon. | Same normalization. | Supplied exclusion -> preserved exclusion; not prohibition. | Caller owns assertion; truth, completeness, and authority unchecked. | Yes: boundary identity. |
| `evidence_snapshot_refs` | References pairing an `evidence_ref`, `snapshot_ref`, claimed `evidence_state`, and notes. | Iterable to tuple; no field validation/dedupe. | Available reference testimony -> preserved snapshot-reference testimony; not admission. | Caller owns all fields; object shape enables construction; empty/duplicate/false refs do not defeat. | Yes: evidence identity, including state and notes via `asdict`. |
| `time_bounds` | Asserted temporal locality of the horizon. | String normalization/dedupe. | Supplied temporal bound -> preserved bound; no occurrence testimony. | Caller owns it; no clock/source/currentness check. | Yes: boundary identity. |
| `current_state_bounds` | Asserted state/snapshot locality. | String normalization/dedupe. | Supplied current-state bound -> preserved bound; “current” is not proven. | Caller owns it; no repository observation or freshness check. | Yes: boundary identity. |
| `potentially_relevant_need_families` | Families the caller says may matter for later preservation. | String normalization/dedupe. | Potential relevance assertion -> preserved potential relevance; no Need classification. | Caller owns it; no recognized-family/applicability check. | Yes: boundary/producer-family convention. |
| `explicitly_excluded_need_families` | Family plus reason asserted outside later consideration. | Tuple; every reason must be truthy; no family/reason semantics or dedupe. | Supplied exclusion -> locally well-formed preserved exclusion; not forbidden movement. | Caller owns exclusion; nonempty reason warrants construction; missing reason defeats. | Yes: boundary identity, full dataclass content. |
| `unknowns` | Caller-described unknown testimony concerning the horizon/road. | Merge after goal unknowns; normalize/dedupe. | Supplied unknown -> preserved unknown. | Caller owns truth; never defeats bounded state. | No. |
| `conflicts` | Caller-described conflict testimony concerning the horizon/road. | Merge after goal conflicts; normalize/dedupe. | Supplied conflict -> preserved conflict. | Caller owns truth; except locally generated missing-exclusion-reason conflict on refusal, conflicts do not defeat. | No. |
| `stale_evidence_refs` | Evidence refs asserted stale. | String normalization/dedupe. | Supplied quality claim -> preserved claim. | Caller owns it; no cross-check with snapshots or `evidence_state`. | No. |
| `unavailable_evidence_refs` | Evidence refs asserted unavailable. | String normalization/dedupe. | Supplied availability claim -> preserved claim. | Caller owns it; no cross-check with snapshots. | No. |

Caller supply is therefore testimony ingress, not lawful selection.  Successful
construction adds local artifact form, identity, and `bounded` state; it does not
upgrade the supplied assertions to observed facts.

## Demand and Gap recovery

No active implementation exposes a `Demand` family or a `Question` on this handoff.
The horizon does not answer a Question.  It composes already supplied testimony
under local guards.

The exact **Gap** is narrower: before the call there is an established-goal witness
and separately supplied boundary testimony, but no stable artifact binding that
exact goal identity to that exact present movement/evidence/scope/family-bounds
bundle for downstream horizon-relative testimony.  The missing standing concerns
their bounded relation/transport context, not missing content or standing inside
the goal and not truth of present conditions.

A horizon is required by current downstream identity checks because testimony and
projections bind to `horizon_id`, and evidence must name an `evidence_ref` present
in the horizon.  It supplies a common bounded intake identity before Need
projection.  Remaining gaps include stage-owned component testimony, its
materiality/applicability/ownership, evidence truth and freshness, Need standing,
family coverage, sufficiency, selection, authority, and movement.

## Capability recovery

| Capability / competence | Availability | Constitutional standing, applicability, selection, authorization, execution |
|---|---|---|
| Bounded-goal establishment | Two implemented producers return the artifact. | Standing is represented in the goal artifact.  Horizon checks type/not-refused only; it neither selects this capability nor re-executes it.  No movement authorization follows. |
| Horizon construction | `establish_bounded_advancement_horizon` is implemented and publicly exported. | Availability is proven.  Applicability is only structurally approximated by goal/boundary/exclusion guards.  No separate Capability artifact, lawful selector, or authorization is recovered.  Invocation is execution of a read-only constructor, not operational movement. |
| Stable identity generation | Local `_stable` hashes deterministic JSON. | Mechanically available and executed locally.  It identifies a bundle; it does not confer constitutional standing. |
| Input normalization/preservation | `_dedupe`, tuple conversion, dataclass construction, and serialization are implemented. | Applicable when the producer is invoked; selected by control flow and executed.  They preserve testimony without admission or inference. |
| Boundary truth/current-state observation | **No producer recovered here.** | Capability standing, applicability, selection, authorization, and execution are absent/Unknown.  Callers may supply claims but the horizon does not observe. |
| Need projection | Four downstream producers are implemented. | Not performed by the horizon.  Their availability is not authorization and their internal correctness is outside scope. |

## Reasoning-act recovery

| Act | Inputs -> new assertion | Strength / owner / warrant / defeaters | Occurrence |
|---|---|---|---|
| Establishment | Goal type/not-refused plus a nonempty supplied boundary and reason-bearing exclusions -> `horizon_state="bounded"` and a stable horizon witness. | Producer-local establishment **of the horizon artifact/binding**, not of boundary truth. Guards warrant; wrong goal type, refused goal, empty boundary, or reasonless exclusion defeat. | Local. |
| Composition | Goal identity/provenance/adverse testimony plus independent boundary bundle -> one horizon object. | Exact supplied-testimony composition. Producer owns assembly; inputs and guards warrant faithful construction. | Local. |
| Preservation | Copies goal id/type/ingress/lineage, boundary bundle, and adverse/quality refs. | Preserved testimony only; normalization may remove empty/duplicate strings. Caller/upstream owners retain assertion responsibility. | Local, with upstream occurrence merely represented. |
| Validation | Type/not-refused, boundary nonemptiness, and exclusion-reason checks. | Structural acceptance/refusal, not semantic validation. | Local. |
| Selection | No goal, boundary, scope, evidence, family, or action selection is implemented. | Absent. Caller choices remain caller testimony. | Neither local nor proven upstream by this handoff. |
| Applicability judgment | No semantic goal-to-boundary applicability judgment. | Absent; nonempty is not applicable. | Absent. |
| Admission | No evidence or boundary admission act is represented. | Absent; availability/preservation is not admission. | Absent. |
| Projection | No Need, future state, or goal-content projection. | Absent. Downstream projections are separate consumers. | Delegated downstream. |
| Abduction | No best-explanation generation/choice. | **Unknown/absent from implementation evidence.** | Not recovered. |
| Induction | No recurrence generalization. | **Unknown/absent from implementation evidence.** | Not recovered. |
| Deduction | Deterministic branches and hashing occur, but the repository supplies no deductive warrant classification. | **Unknown; not classified as deduction.** | Mechanical branching only. |

## Local horizon act

The most exact candidate is: **a read-only, stable composition witness binding one
represented non-refused bounded-goal identity and preserved ingress lineage to one
caller-supplied present movement-boundary bundle as the bounded field against which
later testimony may be characterized.**  It is a precondition/intake witness for
later Need projection and a stable transport object, but those are consumer roles,
not stronger local truth claims.

The producer:

* does **not select** the boundary;
* **validates only** its nonemptiness and exclusion-reason shape;
* does **not admit** boundary or evidence truth;
* does **not establish** the boundary's constitutional standing;
* **preserves** the supplied boundary and records it in a stable artifact; and
* newly establishes only the local horizon composition/witness state.

It therefore represents a bounded field of **possible** advancement context, not
authorized movement and not proof that advancement is reachable.

## Subject-by-field matrix

| Horizon field(s) | Exact subject characterized |
|---|---|
| `artifact_type`, `horizon_id`, `horizon_state`, `refusal_reason` | The horizon artifact and local construction outcome. |
| `goal_establishment_id` | The established goal/witness identity to which the horizon is bound. |
| `goal_artifact_type` | The supplied establishment witness's claimed artifact kind. |
| `goal_ingress_artifact_ref`, `goal_ingress_lineage` | The goal witness's preserved ingress road, not present state. |
| `present_movement_boundary` | The caller-supplied present movement-boundary assertion. |
| `included_scope`, `excluded_scope` | Material asserted inside/outside this horizon, not globally applicable/forbidden material. |
| `evidence_snapshot_refs` | Evidence/snapshot reference testimony and claimed evidence state/notes. |
| `time_bounds` | Temporal locality asserted for this horizon, not occurrence. |
| `current_state_bounds` | State locality asserted current, not independently observed current state. |
| `potentially_relevant_need_families` | Possible later Need-family relevance, not existing Needs. |
| `explicitly_excluded_need_families` | Caller-excluded families and reasons for this horizon. |
| `unknowns`, `conflicts` | Mixed adverse testimony preserved from the goal and caller; individual entries retain their described subjects. |
| `stale_evidence_refs`, `unavailable_evidence_refs` | Caller-asserted quality/availability of referenced evidence. |
| `selects_goal`, `establishes_focus` | Negative assertions about this horizon producer. |
| `classified_need_families`, `judges_sufficiency`, `sufficient_for_now`, `selects_next_action`, `selected_next_action` | Explicit absence of Need classification, sufficiency judgment, and next-action selection. |
| `opens_inquiry`, `requests_authority`, `selects_realization`, `schedules`, `authorizes_work`, `starts_execution`, `starts_recording`, `writes_event_ledger`, `mutates_cluster`, `read_only` | Operational boundary of the artifact/producer. |
| `boundary_notes` | Interpretive limits on the horizon artifact and its fields. |

There is no truthful single subject for all fields.  The coherent common subject is
the **horizon relation/witness itself**: this goal identity together with this
supplied boundary bundle under this producer's negative operational limits.

## Eight-dimensional characterization

| Dimension | Exact horizon-relation characterization | Status |
|---|---|---|
| Subject / identity | One `horizon_id` identifies the relation between one `goal_establishment_id`/ingress ref and one identity-bearing boundary bundle. | Goal identity inherited; boundary identity independently supplied; relation identity newly established locally. |
| Assertion / content | “This supplied present movement boundary, scopes, snapshots, temporal/state bounds, and family bounds are preserved around this non-refused bounded-goal identity.” It does not restate intended outcome. | Boundary content independently supplied; composition newly established; goal content absent. |
| Standing | Goal establishment is upstream represented standing; `bounded` is local constructor standing; boundary constitutional standing remains absent. | Mixed and explicitly limited. |
| Source / provenance | Goal ingress ref/lineage is inherited. Boundary/evidence inputs have no source-ref lane beyond their own values and nested refs. | Goal provenance preserved; caller provenance largely absent/Unknown. |
| Responsibility | Goal producer owns goal standing; immediate caller owns boundary assertions; horizon producer owns guards, normalization, composition, and faithful output. | Independently owned, converged locally. |
| Authority / warrant | Goal type/not-refused plus nonempty boundary and reason-bearing exclusions warrant construction only. No field grants authority. | Locally validated shape; boundary warrant and movement authority absent. |
| Scope / locality | Horizon locality is expressed by present boundary, included/excluded scope, time/current-state bounds, snapshots, and family bounds. Goal locality is not recovered from these. | Independently supplied and preserved; applicability delegated/absent. |
| Occurrence / preservation | Deterministic ID and returned object witness local construction if call observation is available; ingress lineage and testimony are preserved. No time, event-ledger record, or durable occurrence proof exists. | Local ephemeral occurrence plus preservation; recording absent. |

The horizon does not complete defective dimensions of the goal.  It characterizes a
distinct relation around that goal.  A downstream dimension does not correct the
upstream artifact; goal locality is not horizon locality, and movement standing is
not goal standing.

## Stable-ID recovery

For a successful horizon, the complete payload is:

```text
goal                         = goal.goal_establishment_id
source                       = goal.ingress_artifact_ref
boundary                     = present_movement_boundary
included_scope               = deduped included_scope
excluded_scope               = deduped excluded_scope
snapshots                    = asdict(each EvidenceSnapshotReference), in order
time_bounds                  = deduped time_bounds
current_state_bounds         = deduped current_state_bounds
need_families                = deduped potentially_relevant_need_families
excluded_need_families       = asdict(each NeedFamilyExclusion), in order
```

JSON is key-sorted and compactly encoded, SHA-256 hashed, and prefixed
`bounded-advancement-horizon:`.

| Identity input | Variability preserved / collapse if removed | Identity category |
|---|---|---|
| Goal id | Distinguishes horizons for distinct goal witnesses. | Goal identity. |
| Goal ingress ref (`source`) | Distinguishes the same represented goal id paired with differing immediate ingress ref. | Goal provenance/producer convention. |
| Boundary | Distinguishes different asserted present movement boundaries. | Present-boundary identity. |
| Included/excluded scope | Distinguishes asserted locality sets; dedupe collapses duplicate/empty spelling occurrences while order remains significant. | Present-boundary identity. |
| Snapshot dataclasses | Distinguishes evidence ref, snapshot ref, state, notes, count, and order. | Evidence identity. |
| Time/current-state bounds | Distinguishes asserted temporal/state localities; order remains significant after dedupe. | Present-boundary identity. |
| Potential families | Distinguishes possible family territories, not actual Needs. | Boundary identity/producer convention. |
| Excluded families and reasons | Distinguishes family exclusions, reasons, duplicates, and order. | Boundary identity. |

Notably absent are `goal.artifact_type`, goal ingress lineage, goal unknowns/conflicts,
all caller unknown/conflict/stale/unavailable refs, and every semantic goal field.
Those fields can vary without changing `horizon_id`.  On refusal the payload is only
`state`, `reason`, goal id, and boundary; therefore distinct adverse details can
share a refused identity.  Identity participation proves variability policy, not
constitutional standing or truth.

## Consumer recovery

Active direct consumers are the four native Need projectors, the need-set
assembler, and the family-coverage assembler.  The public export and JSON helper
are availability/transport surfaces, not constitutional consumers.

| Consumer | Horizon fields actually read | Minimum assumed treatment / further work |
|---|---|---|
| `project_clarification_need` | `horizon_id`, `evidence_snapshot_refs[*].evidence_ref`, `explicitly_excluded_need_families[*].need_family` | Need-projection intake and present-boundary identity. It requires testimony to match horizon/evidence and assert materiality to the present boundary; family exclusion changes a classified item to `excluded_family`. It does not read boundary text. |
| `project_inquiry_need` | Same three field groups. | Same intake treatment for repository-world uncertainty; further component ownership/materiality checks occur in that producer. |
| `project_authority_need` | `horizon_id`, `evidence_snapshot_refs[*].evidence_ref` | Intake identity/evidence allowlist. Separate testimony supplies scope applicability and horizon materiality; horizon exclusions and boundary text are not read. |
| `project_operational_realization_need` | `horizon_id`, `evidence_snapshot_refs[*].evidence_ref` | Intake identity/evidence allowlist. Separate requirement/standing testimony supplies applicability/materiality and realization characterization. |
| `assemble_goal_advancement_need_set` | `goal_establishment_id`, `horizon_id`, `unknowns`, `conflicts`, and `explicitly_excluded_need_families` (`need_family`, `reason`) | Generic preservation/Need-projection intake: checks projection identity, synthesizes missing/excluded-family records, and carries horizon adverse testimony. It does not recover goal content or boundary text. |
| `assemble_advancement_need_family_coverage_set` | `goal_establishment_id`, `horizon_id`, and `explicitly_excluded_need_families` (`need_family`, `reason`) | Horizon-specific identity and exclusion intake for later coverage characterization. It iterates its own fixed four-family convention; it does not read `potentially_relevant_need_families` or treat an omitted family as irrelevant. |

All six consume `horizon_id` directly or through identity checks.  The four
projectors also receive the goal independently and compare testimony to
`goal.goal_establishment_id`, not to semantic goal content in the horizon.  No
active consumer reads `present_movement_boundary`, `included_scope`,
`excluded_scope`, snapshot refs/states/notes (other than evidence refs),
`time_bounds`, `current_state_bounds`, goal artifact type/ingress/lineage,
stale/unavailable refs, or operational flags.  Those are preserved but currently
unconsumed by direct constitutional consumers.

## Cross-examination

* **Can the horizon be reconstructed from the goal alone?** No.  The required
  boundary and every horizon-local scope/evidence/time/state/family input are
  independent caller testimony.
* **Can goal subject/content be reconstructed from the horizon?** No.  It retains
  goal id/type and ingress provenance but omits `intended_outcome`, `known_scope`,
  unresolved scope, known loss, detailed upstream lanes, and admitted snapshot.
* **Does it establish new truth about the goal?** No semantic or standing truth.
  It checks claimed type/not-refused and binds the existing identity into a new
  horizon relation.
* **Does it establish a relation?** Yes, at the artifact/composition level: this
  represented goal identity is paired with this supplied boundary bundle.  It does
  not establish that the caller's boundary is constitutionally warranted.
* **Could different intended outcomes yield indistinguishable horizons?** Yes if
  horizon-read and ID-bearing goal fields are held equal.  Real upstream producers
  ordinarily place outcome-related variability in goal identity, but the horizon
  does not itself consume outcome.
* **Which assertions are necessary downstream?** Exact horizon identity and
  evidence-ref membership are common to the four projectors; goal binding,
  exclusion/relevance, unknown/conflict testimony are used by subsets.  Separate
  component testimony remains necessary for actual Need projections.
* **Which fields are preservation-only today?** The unconsumed list in consumer
  recovery, subject to generic serialization and tests, has no active direct
  constitutional read.

## Handoff classification

The best supported classification is **goal witness composed with independent
present-boundary testimony**, and therefore **a convergence handoff preserving
several independently owned subjects**.  Its coherent common relation is the
horizon artifact binding exact goal identity to a caller-supplied boundary bundle.

It is not goal establishment completed by correction of missing goal dimensions;
not goal testimony projected into a boundary; and not inference from goal content.
It is also more structured than an entirely relationless flattened bundle because
the stable id and downstream identity checks organize the inputs around one exact
goal-relative horizon.  Composition is not inference.

## Remaining gaps

1. No producer or warrant for `present_movement_boundary` or the other independent
   horizon testimony is required, named, or preserved as such.
2. No semantic relation check ties boundary, scopes, evidence, state/time bounds,
   or families to `intended_outcome` or any admitted goal meaning.
3. No currentness, snapshot integrity, cross-field consistency, completeness, or
   evidence-admission check occurs.
4. `bounded` does not express whether possible advancement exists, is applicable,
   is reachable, or is authorized.
5. Downstream stage-owned component testimony is still required to characterize
   clarification, inquiry, authority, and realization Needs; family coverage and
   sufficiency remain later responsibilities.
6. Most preserved horizon detail has no active direct runtime consumer.
7. Direct dataclass construction can imitate both goal and horizon standing; no
   recorded producer occurrence is established.
8. The horizon preserves shallow goal ingress lineage but not detailed upstream
   lanes or goal meaning, and it supplies no equivalent provenance lane for the
   caller's boundary assertions.

## Unknowns

* Any implementation-backed Demand or Question that causes horizon construction.
* The lawful producer, authority, selection rule, warrant, and defeaters for the
  present boundary and every caller-supplied bound.
* Whether non-`refused` establishment states other than today's `established` are
  intended to qualify; the horizon check is only negative.
* Whether input ordering is constitutionally meaningful where stable identity
  preserves order.
* Whether stale/unavailable refs should agree with snapshot `evidence_state`; no
  active check establishes a relationship.
* Whether any unconsumed preservation field has a future constitutional consumer.
* Whether any upstream reasoning is abductive, inductive, or deductive; this road
  provides no repository warrant for those labels.

## Final bounded conclusion

`BoundedOperatorGoalEstablishment` supplies exactly represented, non-refused goal
standing; exact goal/witness identity; shallow ingress provenance; and carried
unknown/conflict testimony.  It does not supply the present movement boundary, and
the horizon does not consume its goal content, scope, detailed lineage lanes,
admitted meaning, or known loss.

The present movement boundary and all horizon-local scope, evidence, time/state,
family, and quality testimony are independently caller supplied.  The horizon
producer performs narrow structural guards, normalization, preservation, stable
identity generation, and a new read-only composition act: it creates one bounded
horizon witness relating an exact established-goal identity to that supplied
bundle.  It neither derives the boundary from the goal nor establishes the
boundary's constitutional truth.  The resulting artifact is useful as a stable
intake identity for later Need characterization, but possible advancement is not
authorized movement, preservation is not admission, and composition is not
inference.
