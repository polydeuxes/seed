# BoundedOperatorGoalEstablishment.known_scope characterization

## Scope

This is a bounded, report-only Fidelity characterization of `BoundedOperatorGoalEstablishment.known_scope` on current merged `main` after PR 1969 (`68dfa9e`). It changes no production code, tests, serialization, exports, CLI/API behavior, canonical Book material, or existing historical reports.

The governing question is: what exact subject does `known_scope` characterize, what evidence establishes each member, and does it carry constitutional scope or selected identity/content under a scope-shaped name?

## Producer matrix

| Producer | Reachable standing | Exact tuple members | Source evidence for each member | Logic admitting each member | Member dimensional standing | Independent variation | Participates in `goal_establishment_id`? | Responsibility owning assertion |
|---|---:|---|---|---|---|---|---|---|
| `establish_bounded_operator_goal_from_closed_choice(binding, ...)` | `established` | `(binding.bound_option_ref,)` | `ClosedChoiceSelectionBinding` must have `artifact_type == "ClosedChoiceSelectionBinding"`; `binding_state == "bound"`; non-empty `bound_option_ref`. The bound ref itself is produced by token lookup inside one exact `PresentedClosedChoiceSet`. | Refusal branch is bypassed when the binding is bound and has a ref; returned `known_scope` is `(binding.bound_option_ref,) if binding.bound_option_ref else ()`. | selected option identity; not shown as locality/boundary/scope constraint. | `bound_option_ref` and `bound_option_label` can differ; `intended_outcome` uses label-or-ref while `known_scope` uses ref only. Unknown/conflict upstream prevents bound ref; unsupported can be caller-supplied into unresolved scope. | Yes. Closed-choice stable-id payload includes a `known_scope` list from `binding.bound_option_ref`. | Binding producer owns token-to-option identity; bounded-goal producer owns that a bound option supplies bounded goal standing and serializes the ref in `known_scope`. |
| `establish_bounded_operator_goal_from_closed_choice(binding, ...)` | `refused` | `()` | Non-bound, missing `bound_option_ref`, unknown, conflict, or unsupported binding evidence. | Refusal state is set when `binding.binding_state != "bound" or not binding.bound_option_ref`; returned tuple is empty because no bound ref exists. | absence of selected option identity; no scope assertion. | Empty regardless of the particular refusal reason; reasons move to `establishment_reason`, `unresolved_scope`, `unknowns`, or `conflicts`. | Yes as empty/absent in payload when no `bound_option_ref`. | Bounded-goal producer owns refusal; binding producer owns upstream unknown/conflict/unsupported state. |
| `establish_bounded_operator_goal_from_admitted_interpretation(admission)` | `established` | `_refs((selected_candidate_ref, selection.label))` | `DownstreamInterpretationAdmission` for exact bounded-goal consumer/purpose; matching admission/projection selection identities; admitted outcome; applicable projection; no unknowns/conflicts; present selected candidate and selected ref. `selected_candidate_ref` comes from admission/projection/selection identity. `selection.label` comes from the selected candidate object carried by the projection/admission. | After all refusal guards are bypassed, `selected_ref = admission.selected_candidate_ref or ""`; `selection = projection.selected_candidate`; `scope = () if state == "refused" else _refs((selected_ref, getattr(selection, "label", "")))`. | `selected_candidate_ref`: selected interpretation identity. `selection.label`: human-readable label/content. Neither is shown by implementation as boundary, locality, or scope constraint. | Yes. The stable-id payload includes selected ref but not label; `_refs` sorts/deduplicates members; label may equal ref, be absent, or differ from proposed meaning. `intended_outcome` prefers proposed meaning, then label, then ref, so label and intended content can vary. | Partially. Admitted-interpretation stable-id payload includes `selected_ref` as `selected`, but does not include `selection.label` or `known_scope` as a tuple. | Selection producer owns candidate identity and label; applicability/admission own preservation and exact consumer-local warrant; bounded-goal producer owns consumption without reselection and tuple shaping. |
| `establish_bounded_operator_goal_from_admitted_interpretation(admission)` | `refused` | `()` | Any mismatch, unadmitted/inapplicable/unknown/conflicting lineage, or missing selected meaning identity. | Refusal branches set `state == "refused"`; `scope = () if state == "refused" else ...`. | no selected identity/content admitted into goal surface; no scope assertion. | Empty regardless of specific refusal condition; details move to `establishment_reason`, `unknowns`, `conflicts`, and `unresolved_scope`. | Yes indirectly through payload state/selected/unknowns/conflicts/unresolved; tuple itself is empty and not listed as `known_scope`. | Bounded-goal producer owns refusal; upstream projection/admission/selection own carried evidence. |

## Member-by-member source recovery

### Closed-choice `binding.bound_option_ref`

`bound_option_ref` is created by looking up a captured token in `options_by_token` for a single exact choice set. If conflicts exist, if the token is absent, or if unknown evidence exists, `bound` is cleared and no `bound_option_ref` is emitted. A successful binding stores `bound.option_ref` and `bound.presented_label` separately. Goal establishment admits the ref into `known_scope` only when the binding artifact type is exact, the state is `bound`, and the ref is non-empty.

Evidence establishes only: "this captured token selected this option ref inside this exact presented closed-choice set." The binding module explicitly says a selection token has only local meaning inside the exact presented choice set, and that a bound option is not operator authority, inquiry selection, execution, or authorization. That evidence is identity-local; it does not answer the scope grammar questions below.

### Admitted-interpretation `selected_candidate_ref`

The selected candidate ref originates in contextual interpretation selection from explicit candidate-bound selection evidence naming exactly one warranted candidate. Applicability projection preserves `selection_result.selected_candidate_ref`; downstream admission preserves the projection/selection candidate identity and requires local admission evidence to match the selection result, projection, selected candidate, purpose, and consumer. Goal establishment refuses mismatched admission/projection/selection candidate identity.

Evidence establishes: "this admitted, consumer-local interpretation is the selected candidate identity consumed by the bounded-goal establishment handoff." That is selected identity and provenance, not a scope boundary.

### Admitted-interpretation `selection.label`

The label is not independently validated in goal establishment. It is read from the carried selected candidate object with `getattr(selection, "label", "")`, admitted into `_refs` only on an established path, and sorted/deduplicated with the selected ref. It is also available in the consumed selected-meaning snapshot because applicability serializes the selected candidate as a dataclass snapshot.

Evidence establishes: "the carried selected candidate had this human-readable label at consumption time." It is content/presentation and possibly an assertion label for intended meaning. It is not itself a locality, boundary, movement limit, resource set, or constitutional coordinate.

## Scope grammar comparison

Repository implementation provides several actual boundary/locality constructs near this field:

- Closed-choice binding is local to one exact presented choice set and token capture.
- Interpretation applicability is local to one supplied bounded downstream purpose and consumer contract.
- Downstream admission is local to exactly one consumer and purpose and is not transferable authority.
- Bounded-goal establishment keeps `unresolved_scope`, unknowns, conflicts, ingress lineage, upstream refs, and consumed snapshots separately.

Against the requested scope questions:

| Question | Recovered answer for `known_scope` |
|---|---|
| Where does this goal apply? | Not answered. Closed-choice ref names a selected option; admitted ref names a selected interpretation; label names content. |
| To which subjects, resources, systems, localities, or constitutional coordinates? | Not answered, except that one exact upstream selected object is identified. One exact selected subject is not the boundary around that subject. |
| What is inside the goal boundary? | Not answered by tuple members. Boundary-related residuals/refusals are carried in `unresolved_scope`; lineage/provenance identify ingress. |
| What is outside it? | Not answered. Refused/unsupported/residual material may appear in `unresolved_scope`, `unknowns`, `conflicts`, or snapshots. |
| What movement is bounded by it? | Not answered. Neighboring artifacts explicitly stop before inquiry movement, authorization, execution, recording, state mutation, and cluster mutation. |

Therefore `known_scope` does not establish a constitutional scope/locality grammar answer. It records selected identity, and on the admitted road it also records a human label/content member, under a scope-shaped field name. A bounded goal can still be bounded through ingress standing, consumer-local admission, unresolved scope, lineage, and refusal boundaries without this tuple being constitutional scope.

## Consumer recovery

Active runtime and test search recovered these `known_scope` occurrences:

| Occurrence | Classification | Notes |
|---|---|---|
| Dataclass field `known_scope: tuple[str, ...]` | serialization/schema field | Defines the stored surface. |
| `to_json_dict()` via `asdict` | serialization only | Generic serialization is not an independent semantic consumer. |
| Closed-choice stable-id payload `"known_scope": [binding.bound_option_ref] ...` | stable-identity input | Proves identity relevance for current closed-choice payload, not scope standing. |
| Closed-choice return tuple `(binding.bound_option_ref,) ...` | producer shaping | Produces field; not a consumer. |
| Admitted return `scope` | producer shaping | Produces selected ref/label tuple; not a consumer. |
| `tests/test_bounded_operator_goal_establishment.py` assertion | test assertion only | Verifies closed-choice option ref appears in tuple. |
| Existing `.md` reports | historical report | Not active runtime consumers; not edited. |

No active runtime consumer was recovered that treats `known_scope` as constitutional scope. No recovered consumer answers locality/boundary questions by reading it. Stable-ID participation proves only that the current closed-choice payload identity includes the bound option ref; for the admitted road, selected ref participates as `selected`, while `selection.label` does not.

## Neighboring-field cross-examination

| Tuple member | Exact truth it adds | Where truth is already carried | Would deletion lose selected identity? | Would deletion lose actual scope? | Can disagree with neighbors? | Lawful scope reliance? |
|---|---|---|---:|---:|---|---|
| Closed-choice `binding.bound_option_ref` | Selected option ref from exact closed-choice binding. | `ingress_artifact_ref` points to binding; binding carries `bound_option_ref`; `intended_outcome` carries label-or-ref; ingress lineage carries choice-set/capture/fingerprint. | In the goal artifact itself, yes: it would lose direct selected option ref unless consumer dereferences ingress. | No repository evidence shows loss of constitutional scope. | Yes, if `intended_outcome` uses label while known_scope uses ref; if historical serialized artifacts are mutated externally; not by current producer logic. | No. It is option identity, not boundary/locality grammar. |
| Admitted `selected_candidate_ref` | Selected interpretation candidate identity consumed by bounded-goal establishment. | `upstream_selection_refs` includes admission selection result id and selected ref; `ingress_artifact_ref` points to admission; admission/projection carry selected ref; snapshot may carry `candidate_ref`. | Directly in `known_scope`, yes; but the same identity remains in `upstream_selection_refs` and ingress admission. | No repository evidence shows loss of constitutional scope. | Current producer refuses admission/projection mismatch, but tuple can overlap rather than constrain. If external artifact mutation occurred, it could disagree with upstream refs/snapshot. | No. It is selected identity. |
| Admitted `selection.label` | Human-readable label of carried selected candidate. | `intended_outcome` may equal label when `proposed_meaning` is empty; `consumed_admitted_meaning_snapshot` carries the selected candidate dataclass snapshot including label; admission/projection selected candidate object carries it. | No selected identity lost. | No actual scope lost. | Yes. `intended_outcome` may prefer proposed meaning over label; snapshot could carry richer/different content than the tuple if externally mutated; label and ref are independent. | No. It is content/presentation, not scope. |

Cross-examined neighboring fields:

- `intended_outcome`: closed-choice uses label or ref; admitted interpretation uses proposed meaning, label, or ref. It carries outcome/content, not scope. It overlaps with closed-choice label and admitted label, not necessarily with candidate ref.
- `ingress_artifact_type` and `ingress_artifact_ref`: identify the source artifact class and exact source artifact id. They provide provenance/dereference path, not scope.
- `ingress_lineage`: preserves binding choice set/capture/fingerprint or upstream selection/applicability/admission/source refs. It carries provenance and occurrence, not the boundary itself.
- `upstream_selection_refs`: admitted road carries selection result id and selected candidate ref. It overlaps selected identity and makes the `known_scope` selected ref redundant for identity preservation inside the goal artifact.
- `consumed_admitted_meaning_snapshot`: admitted road carries selected candidate content, source spans, residual source material, unknowns/conflicts/loss. It overlaps the label and candidate identity and is stronger provenance/content evidence than the `known_scope` label member.
- `unresolved_scope`: carries caller-supplied unresolved closed-choice scope, unsupported selection evidence, known refusals, applicable-but-unadmitted reasons, and residual refs. It is closer to boundary uncertainty than `known_scope`.
- `unknowns` and `conflicts`: carry negative/uncertain warrant state and mismatch reasons. They can block establishment but do not turn `known_scope` into scope.

## Eight-dimensional characterization

| Producer/member | Subject / identity | Assertion / content | Standing | Source / provenance | Responsibility | Authority / warrant | Scope / locality | Occurrence / preservation |
|---|---|---|---|---|---|---|---|---|
| Closed-choice `binding.bound_option_ref` | Selected option ref in exact choice set. | Ref string, not label. | Established only when binding is `bound`; empty on refusal. | Choice set, fingerprint, token capture, binding id. | Binding owns token-option match; goal producer owns goal-standing consumption. | Warranted by captured token belonging to exact choice set. | Local to exact choice-set identity; no goal boundary recovered. | Preserved in `known_scope`; included in closed-choice goal stable-id payload. |
| Admitted `selected_candidate_ref` | Selected candidate identity. | Ref string. | Established only after exact consumer-local admission and no unknown/conflict/mismatch. | Selection result, projection, admission, upstream selection refs. | Selection owns selection; projection/admission preserve; goal producer consumes. | Warranted by explicit candidate-bound selection evidence plus purpose-local applicability and admission evidence. | Local to selected interpretation and exact consumer/purpose admission; no goal boundary recovered from the ref. | Preserved in `known_scope`, `upstream_selection_refs`, ingress admission/projection, and stable-id payload as `selected`. |
| Admitted `selection.label` | Human label for selected candidate; not identity unless labels are treated externally as such, which is not evidenced here. | Presentation/content label. | Established only by carried selected candidate object on established path. | Selected candidate object and selected-meaning snapshot. | Selection/warrant source owns label; goal producer reads without recomputation. | Warranted only as carried selected-candidate content. | Unknown as scope; no locality or boundary standing recovered. | Preserved in `known_scope`; also in selected-meaning snapshot; not included in goal stable-id payload. |
| Refused empty tuple | No selected member admitted. | Absence marker. | Refused. | Refusal branch evidence. | Goal producer owns local refusal. | Warranted by failure of establishment guards. | No scope assertion. | Empty tuple serialized. |

## Field classification

Field classification: **mixed identity/content tuple serialized as scope**.

Rationale: the closed-choice producer serializes selected option identity; the admitted-interpretation producer serializes selected candidate identity plus a human label/content member. Current implementation does not establish that these tuple members answer the repository's scope/locality grammar. It is not merely redundant because deletion would lose a direct closed-choice selected option ref from the goal artifact and a direct admitted label copy; however, much admitted identity/content overlaps neighboring fields.

## Member classifications

| Member | Classification |
|---|---|
| Closed-choice `binding.bound_option_ref` | selected option identity serialized as scope |
| Admitted `selected_candidate_ref` | selected identity serialized as scope |
| Admitted `selection.label` | content/presentation serialized as scope |
| Refused empty tuple | faithful absence of admitted selected scope/identity/content; no scope standing |

## Truth lost by deletion

- Deleting the field would lose direct access to closed-choice selected option identity from the goal artifact unless the consumer dereferences the ingress binding.
- Deleting the field would lose a direct copy of admitted selected candidate identity from `known_scope`, but not from the goal artifact overall because `upstream_selection_refs` also contains it and ingress admission/projection preserve it.
- Deleting the field would lose a direct copy of admitted selected candidate label from `known_scope`, but not necessarily from the goal artifact overall because `consumed_admitted_meaning_snapshot` preserves selected candidate content.
- Deleting the field would not lose an implementation-evidenced constitutional scope boundary, locality coordinate, inside/outside boundary, movement limit, resource set, or subject boundary.

## Safe deletion or correction status

Safe deletion/correction status: **not determined safe in this report**.

This report does not recommend replacement architecture and does not rename, split, relocate, or delete the field. It only recovers that current `known_scope` is not independently evidenced as constitutional scope. Deletion would be behaviorally observable in serialization, tests, and closed-choice stable identity; correction would require a separate implementation decision outside this bounded report-only change.

## Protected distinctions

- selected option identity != scope
- selected candidate identity != scope
- human-readable label != scope
- intended outcome content != scope
- one exact selected subject != boundary around that subject
- consumer-local admission locality != transferable constitutional scope
- stable-ID participation != scope standing
- unresolved scope/unknown/conflict evidence != known scope

## Unknowns

- Whether any external downstream consumer outside the repository relies on `known_scope` as scope is Unknown.
- Whether historical reports intended a broader meaning for `known_scope` than current runtime evidence supports is Unknown.
- Whether labels are globally unique, stable, or identity-bearing is not established.
- Whether a future bounded goal requires a true known-scope coordinate remains Unknown from current implementation evidence.
- Whether `known_scope` should be renamed, split, deleted, or redefined is outside this report and remains Unknown.

## Final bounded conclusion

`BoundedOperatorGoalEstablishment.known_scope` characterizes selected establishment material, not a recovered constitutional scope boundary. On the closed-choice path, it is exactly the selected option ref admitted from an exact bound selection. On the admitted-interpretation path, it is a sorted/deduplicated tuple of the selected candidate ref and the selected candidate label, with those two members carrying independent dimensional standing: identity and content/presentation. On refused paths it is empty. The field is therefore best classified as **mixed identity/content tuple serialized as scope**, with no active runtime consumer recovered that lawfully relies on it as scope.
