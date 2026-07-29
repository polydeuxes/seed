# Current meaning-relation witness Fidelity recovery 001

## Scope and method

This is one report-only recovery against merged `main` after PR 2068. The inquiry follows only operator-ingress roads that may reach `BoundedOperatorGoalEstablishment` (BOGE): the live closed-choice common-grammar interaction road and the separately constructible admitted-interpretation road. Repository implementation is authority for current behavior; the active Book supplies the already-settled constitutional distinctions. Tests are implementation evidence, not constitutional authority. Historical reports were search aids only.

Search of non-test Python callers found a live producer for the common-grammar closed choice, but no non-test invocation of the contextual warrant, selection, applicability, admission, or either relevant BOGE function. Consequently, “current road” below distinguishes a production-invoked road from a programmatically constructible/test-active island.

## A. Constitutional expectation

The smallest applicable expectation is not a compulsory universal artifact sequence. If BOGE consumes bounded proposition `M` as expressed by source candidate `G`, its exact consumer act must have standing for the bounded meaning relation `G -> expresses M`: a responsible occurrence must warrant that relation from claim-appropriate testimony/evidence or constitutive convention, with applicable participants, roles, source and attribution, scope, provenance, authority, loss, conflicts, limits, and Unknowns; BOGE-local applicability and, where this boundary requires it, admission must preserve that exact relation; BOGE then relies on the admitted relation and consumes `M` as expressed by `G`. None of assertion carriage, attribution, selection testimony, representation lineage, applicability, admission, or proposition equality substitutes for another crossing.

On the closed-choice road, a responsible representation may form presented alternative `A` representing source candidate `G`; exact token binding may identify `A`; lineage may recover `G`; an independently warranted relation must establish that `G` expresses `M`; later acts may use standing derived from the same operator response without asking again. A selected local-stop alternative has the same separation through an independently warranted local-stop meaning relation and a competent stopping occurrence. The Book neither requires a dedicated meaning artifact/admission artifact nor makes the admitted-interpretation artifact family compulsory for closed choice.

## B. Current closed-choice topology

### B.1 Exact connected topology

Legend: `-->` consumes material, `..>` preserves/projects, `-#>` carries identity or lineage only, and `-X>` is absent or refused.

```text
run_operator_ingress_common_grammar_probe_attempt
  --> common_grammar_choice_set(presentation_ref)
      --> PresentedClosedChoiceSet(
            hard-coded token / option_ref / presented_label,
            no presented_detail, presentation identity, provenance)
  --> render_probe --> stdout
  --> response raw capture + strict decoding
  --> OperatorSelectionTokenCapture(token, set ref, response-Event provenance)
  --> validate_capture_for_probe
      --> validates recorded presentation, exact fingerprint, current capture,
          exact token text, and single consumption
      --> bind_closed_choice_selection
          --> ClosedChoiceSelectionBinding
              (exact-set membership, bound option ref/label, capture/set lineage)
  --> binding Event
  --> treatment_selected Event(selected_treatment = bound_option_ref)
      --> result prose only

ClosedChoiceSelectionBinding
  -X> establish_bounded_operator_goal_from_closed_choice
       (every correctly typed binding raises: no competent goal-specific
        semantic admission producer)

Events ..> StateProjector ..> operator_ingress_common_grammar_attempts visibility
```

The live application owns exactly two alternatives. Token `1` has `option_ref="common-grammar-acquisition"` and a label selecting that treatment; token `2` has `option_ref="local-stop"` and a label selecting that treatment. The responsible presentation occurrence records stdout emission and the exact set fingerprint. The response occurrence preserves raw/decoded response lineage; the validator proves that the capture belongs to that recorded presentation and has not already been consumed. The binder compares the token against the exact immutable set and identifies the matching option. Unknown/conflicting selection evidence prevents a bound option; a nonmember is unsupported.

The binder's responsible act is exact-set-local comparison and option identification. Its output copies the matched `option_ref` and `presented_label`; it does not output a presented-alternative identity distinct from those fields, a source-candidate ref, a representation relation, a meaning assertion, a meaning-relation warrant, applicability, or admission. Its boundary notes explicitly stop before goal application. The common-grammar interaction then silently uses `bound_option_ref` as `selected_treatment`; this is a treatment-selection assertion supported by the binding Event, not source recovery or semantic standing.

### B.2 Crossing inventory

| Crossing | Responsible occurrence | Exact input and act | Output standing | Evidence/provenance and loss | Current consumer | Status |
| --- | --- | --- | --- | --- | --- | --- |
| constants -> choice set | `common_grammar_choice_set` called by the attempt | Local constants plus `presentation_ref`; constructs an immutable representation | exact set content/fingerprint | module provenance string; no source candidate, producer authority, semantic evidence, loss, conflicts, or Unknowns | renderer, presentation recorder, validator, binder | implemented representation |
| choice set -> presentation | attempt's stdout write and `presentation_occurred` record | rendered prompt and token/label rows; emits them | recorded presentation occurrence | presentation ref, fingerprint, ingress lineage; content is compressed to label and detail is empty | response capture and validator | implemented |
| response -> token capture | `_capture_representation` and `response_captured`, then `OperatorSelectionTokenCapture` construction | exact boundary bytes are decoded; framed text becomes token | occurrence testimony scoped to exact set | raw capture, examination and response Event lineage; true source-relative encoding remains Unknown | validator/binder | implemented |
| token + exact set -> selected option | `validate_capture_for_probe` then `bind_closed_choice_selection` | validates occurrence/currentness, compares exact token | bound local option ref/label or unsupported/Unknown/conflict | presentation fingerprint, response/binding Events, capture ref; does not preserve a separate alternative ref or source relation | treatment selection; tests reconstruct for BOGE refusal | implemented exact selection testimony |
| bound option -> represented source candidate | none | `bound_option_ref` is copied into `selected_treatment` without a represented-source relation | no source-candidate standing | equal string/position is insufficient; producer, act, evidence, scope, semantic loss, and Unknowns are absent | common-grammar interaction result branch | absent; first unsupported semantic crossing |
| source candidate -> meaning assertion | none on this road | no `G` or `M` is produced | none | not witnessed | none | absent |
| assertion -> meaning-relation warrant | none | no relation assertion is examined | none | not witnessed | none | absent |
| warrant -> BOGE applicability/admission | none | no exact relation is available to examine or admit | none | not witnessed | none | absent |
| binding -> BOGE | `establish_bounded_operator_goal_from_closed_choice`, only when separately called | validates artifact type, then categorically raises | lawful unavailability before goal establishment | refusal states that competent goal-specific semantic admission is absent | caller receives exception | implemented refusal; not production-invoked |

### B.3 What `ClosedChoiceOption` currently establishes

| Field | Implemented standing | What it does **not** establish |
| --- | --- | --- |
| `token` | Required local binding key, unique inside one `PresentedClosedChoiceSet`; rendered to the operator and compared exactly | proposition, source identity, treatment meaning, authority, or universal token semantics |
| `option_ref` | Required arbitrary local option reference. In the sole production producer it is subsequently treated as a treatment identity; tests use command-like refs, goal-like refs, and arbitrary differing refs | a distinct presented-alternative identity, source-candidate identity, or meaning relation by type/name |
| `presented_label` | Caller-supplied rendered content; copied into a bound result, not even required nonempty | complete meaning, candidate proposition, warrant, or source relation |
| `presented_detail` | Optional caller-supplied rendered content included in the set fingerprint; unused by the live producer and renderer | any semantic standing or warrant |

Thus `option_ref` has several implementation uses: production treatment identity, fixture-local command/goal-like reference, and arbitrary local reference. Its constitutional role is **Unknown beyond an option-local implementation reference** because no type invariant or responsible occurrence distinguishes those roles. `ClosedChoiceOption` is the represented row content, but the implementation does not preserve `A -> represents G`; there is no separate `A` identity, `G`, relation assertion, responsible producer evidence, or relation scope. Array inclusion establishes membership of this row in the fingerprinted set, not representation of a source.

## C. Current admitted-interpretation topology

This road is importable and test-active, but the repository has no non-test producer/caller chain connecting operator ingress to it.

```text
caller constructs InterpretationCandidate(candidate_ref, label,
                                           source_span_refs, proposed_meaning)
  --> produce_contextual_interpretation_warrant_set
      --> resolves source spans and evaluates candidate-bound evidence
      --> CandidateWarrant(candidate_ref, label, source_spans, evidence,
                           warrant_standing, loss/Unknown/conflict)
          [proposed_meaning is dropped]
  --> select_contextual_interpretation
      --> consumes candidate-bound selection evidence
      --> ContextualInterpretationSelectionResult(selected CandidateWarrant)
  --> project_interpretation_applicability
      --> evaluates purpose-local requirement evidence for selected artifact
      --> selected_meaning_snapshot = asdict(CandidateWarrant)
  --> admit_downstream_interpretation
      --> validates selection/projection/candidate/purpose/consumer refs
      --> DownstreamInterpretationAdmission(carries selected CandidateWarrant
                                             and projection snapshot)
  --> establish_bounded_operator_goal_from_admitted_interpretation
      --> checks exact BOGE consumer/purpose, identity coherence,
          admitted/applicable, Unknown/conflict, selected presence
      --> intended_outcome = selected.proposed_meaning or selected.label or ref
          [CandidateWarrant has no proposed_meaning, so ordinary result is label]
      --> established BOGE
```

### C.1 Meaning-warrant witness

`InterpretationCandidate.proposed_meaning` is produced only by the caller constructing the candidate. The candidate is therefore a carrier of the assertion that this candidate has that proposed meaning; its dataclass validates only nonempty candidate identity. No producer identity, formation act, meaning-specific authority, evidence, scope, conflict, loss, or Unknown is attached to that field.

`produce_contextual_interpretation_warrant_set` is the sole surface that appears to warrant candidate meaning. It binds retrospective and clarification evidence to `candidate_ref`, resolves source spans, and computes `warrant_standing`. That supports a candidate-local **artifact warrant standing**, but `CandidateWarrant` omits `proposed_meaning`. Its supporting evidence need only name the candidate and may contain arbitrary exact text/rationale; the producer never tests that evidence against the candidate-to-proposition assertion. The resulting warrant therefore cannot preserve the exact bounded relation `G -> expresses M`. At best it warrants the selected candidate artifact/interpretation candidate under an unspecified meaning; the exact `M` from the input assertion is lost at this crossing.

Selection correctly refuses to infer selection from warrant alone and consumes separate candidate-bound selection testimony. It selects the `CandidateWarrant`, not the original `InterpretationCandidate`. The operator clarification's `exact_text` is selection testimony and is not used as meaning-relation evidence.

Applicability evaluates requirement evidence for a bounded consumer/purpose and the selected candidate artifact. `selected_meaning_snapshot` is precisely `asdict(selection_result.selected_candidate)`: a snapshot of `CandidateWarrant`, including label, spans, evidence, warrant standing and limits, but no `proposed_meaning` and no exact candidate-to-proposition relation identity. Requirements can establish artifact-shape applicability while being silent about proposition preservation. Admission validates identities and local evidence for the same projection/candidate; it carries the selected artifact and projection, but does not restore or validate an exact relation.

BOGE is a real consumer occurrence when called: it validates the exact consumer and purpose, refuses bad lineage/standing, records upstream lanes, sets `consumed_admitted_meaning_snapshot`, and produces establishment standing. But it reads the carried `CandidateWarrant`. Because that type lacks `proposed_meaning`, `getattr(..., "proposed_meaning", "")` is empty and `intended_outcome` becomes `label` (then ref only if label is empty). This fallback is an **unsupported strengthening**, not faithful bounded consumption or merely declared representational loss: the road asserts an established goal using rendered/caller-authored label content without any occurrence establishing that the label is the proposition expressed by the source candidate. The snapshot honestly preserves what reached BOGE, but artifact lineage cannot supply the missing relation.

Current tests prove candidate-local evidence partitioning and standing, explicit selection, snapshot equality with the selected `CandidateWarrant`, applicability/admission identity and evidence checks, BOGE lineage, and successful `establishment_state`. The candidate fixtures initially contain `proposed_meaning`, but no test asserts its survival into `CandidateWarrant`, snapshot, admission, or `intended_outcome`. The BOGE success test explicitly expects `selection.selected_candidate.label`; it proves the fallback behavior, not proposition preservation.

### C.2 `closed_choice_selection_binding_ref`

`produce_contextual_interpretation_warrant_set` accepts an optional caller-supplied string and includes it in the stable-id payload; the resulting warrant set preserves it. No validation requires an artifact, resolves the reference, checks candidate identity, relates a bound alternative to a candidate, or uses it in warrant-standing calculation. `select_contextual_interpretation` does not copy or consult it, so it is lost before selection result and cannot reach applicability, admission, or BOGE.

The only producer found is direct caller supply; the only concrete supply is a test literal (`closed-choice-selection-binding:abc`). The bounded operator-ingress common-grammar interaction never calls the warrant producer, and no runtime road supplies its real binding id. No consumer relies on the field. It therefore preserves an opaque reference, establishes no relation, cannot lawfully connect one operator selection to candidate selection, and does not participate in the current first-contact road.

## D. Meaning-standing table

| Subject | Meaning assertion carried | Warrant producer | Warrant evidence | Applicability consumer | Admission | Reliance/consumption | Standing |
| --- | --- | --- | --- | --- | --- | --- | --- |
| live `ClosedChoiceOption` row | label/detail carry presentation text only | not witnessed | not witnessed | not witnessed | not witnessed | binder compares token; common-grammar interaction uses ref as treatment | represented alternative content; source and meaning Unknown |
| bound closed-choice option | copied ref and label | not witnessed | selection occurrence warrants exact-set membership only | not witnessed | refused/unavailable at closed-choice BOGE boundary | common-grammar interaction relies on binding for treatment identity, not BOGE meaning | exact selection testimony; no source/meaning standing |
| potential closed-choice `G -> M` | not carried | not witnessed | not witnessed | not witnessed | not witnessed | BOGE lawfully refuses | absent |
| caller-built `InterpretationCandidate` | yes, `proposed_meaning` | not witnessed as relation warrant | caller-supplied spans only; no meaning-specific adjudication | not yet | not yet | warrant producer consumes candidate but drops proposition | meaning assertion carriage only |
| `CandidateWarrant` | label and candidate-local evidence; exact proposed proposition absent | `produce_contextual_interpretation_warrant_set` computes standing | candidate-bound retrospective/clarification evidence, spans, loss/Unknown/conflict | projection consumes selected artifact | admission consumes projection/artifact | BOGE later consumes artifact | artifact warrant represented; exact meaning relation not witnessed |
| selected `CandidateWarrant` | same incomplete content plus selection testimony | upstream warrant producer; selector does not warrant meaning | warrant standing plus independent selection evidence | bounded purpose projection | possible after applicability | not yet | selected warranted artifact; exact relation absent |
| applicability projection | snapshot carries incomplete warrant artifact | no new meaning warrant | purpose-local requirement evidence addresses declared requirements | exact declared consumer/purpose | not yet | admission consumer reads it | applicability of selected artifact, not evidenced exact relation |
| downstream admission | carries candidate identity/object and incomplete snapshot | no new meaning warrant | explicit consumer-local admission evidence keyed by identities | already evaluated | admitted/unadmitted locally | BOGE consumes when exact refs match | admission of artifact; exact relation absent |
| established BOGE | `intended_outcome` carries label fallback | none; BOGE says it does not reinterpret | admitted/applicable artifact and lineage | not applicable | upstream admission accepted | BOGE relies and establishes | established-looking goal with unsupported semantic strengthening |

## E. Field-survival table

| Field / standing | Origin | Survival / transformation | Loss or reconstruction | Final use |
| --- | --- | --- | --- | --- |
| `candidate_ref` | caller-created `InterpretationCandidate` | copied exactly to warrant, selection, projection, admission | none in constructible road | identity coherence, known scope, BOGE guard |
| `label` | caller-created candidate | copied to `CandidateWarrant`; snapshot and admission carry it | treated by BOGE as proposition fallback without relation evidence | `known_scope`; ordinarily `intended_outcome` |
| `proposed_meaning` | caller-created candidate | **not copied into `CandidateWarrant`** | lost at warrant production; never reconstructed as itself | unavailable to ordinary BOGE input despite introspective preference |
| source spans | exact operator material plus candidate span refs | resolved into full `SourceSpan` objects in warrant; selected/snapshotted/carried | unmatched refs silently absent; residuals separately collected; relation to proposition absent | BOGE upstream source refs and snapshot |
| warrant standing | warrant producer computes from candidate-bound evidence states | carried in selected candidate, snapshot, admission | meaning object is unspecified, so cannot identify `G -> M` | gates selection (`warranted` required), but BOGE does not separately inspect the standing field |
| selection evidence | caller-created candidate-bound evidence | selection result and provenance retain it | not included in selected snapshot; selection result id/ref represents lineage | selects candidate; BOGE upstream selection refs do not retain exact testimony content |
| selected meaning snapshot | applicability calls `asdict(CandidateWarrant)` | projection retained whole inside admission and copied to BOGE | name overstates content; exact `proposed_meaning`/relation already lost | lineage/source extraction and `consumed_admitted_meaning_snapshot` |
| consumer and purpose | caller-created `BoundedDownstreamPurpose` | projection -> admission; BOGE checks exact constants | no loss on admitted path | applicability/admission locality and BOGE refusal guard |
| admission evidence | caller-created evidence keyed to selection/projection/candidate/purpose/consumer | admission object and provenance; BOGE retains evidence refs | state does not identify an exact meaning relation | admission outcome and upstream admission refs |
| BOGE `intended_outcome` | BOGE producer | prefers missing `proposed_meaning`, then label, then candidate ref | reconstructs goal content from label/ref rather than consuming preserved `M` | established bounded-goal output |
| closed-choice `option_ref` | caller/application option row | binding -> common-grammar treatment selection | no source/alternative role distinction | treatment branch; closed-choice BOGE refuses |
| closed-choice selection evidence | response and exact-set binding occurrences | Events, binding id, projected view | never reaches warrant/applicability/admission road | treatment selection and audit visibility only |

## F. First unsupported crossing

### Closed-choice road

The first semantic crossing that exceeds upstream standing is the common-grammar interaction's conversion of `binding.bound_option_ref` into `selected_treatment`. Exact binding supports “the operator selected this presented row in this exact set.” No responsible occurrence establishes that the row represents a distinct source candidate, or that the local option reference is that source. The implementation may lawfully use the ref under its application-local treatment convention, but it does not preserve that convention as a bounded representation/meaning warrant. Downstream BOGE does **not** compound the problem: its closed-choice entry point intentionally refuses before meaning applicability/admission and goal establishment.

### Admitted-interpretation road

The first unsupported crossing is warrant production: the producer claims candidate-local `warrant_standing` while dropping the candidate's exact `proposed_meaning`. It therefore cannot output or identify the exact warranted relation `G -> expresses M` that later stages appear to preserve. Applicability and admission faithfully preserve the resulting artifact identities but exceed evidence when named or treated as applicability/admission of selected meaning. BOGE makes the strongest downstream excess by establishing `intended_outcome` from `label`.

## G. One-selection invariant and local stop

### One external response

The connected common-grammar interaction faithfully captures one external response, validates it against the one recorded presentation, consumes it once in binding, and preserves response -> binding -> treatment-selection Event lineage. It does not ask again. Later Event projection uses standing derived from that occurrence rather than rereading the raw response. The capture is neither lost nor duplicated before treatment selection, and replay is refused.

That is only selection-derived standing. It never reaches the contextual selection field: `closed_choice_selection_binding_ref` is not supplied by production, is not validated, and is dropped; contextual tests instead create a separate `CandidateSelectionEvidence`, described as exact operator clarification. Thus no current exact road demonstrates one response flowing through presented-alternative selection, source recovery, independent meaning warrant, applicability, admission, and BOGE. This is a disconnected/lost internal lineage, not evidence that a second operator selection is constitutionally required.

### Local-stop branch

Token `2` binds exactly to the presented row whose local `option_ref` is `local-stop`; the common-grammar interaction records `treatment_selected`. It then explicitly reports: “Local-stop treatment selected; bounded stop was not established.” It creates no represented local-stop source, no independent `S_stop -> expresses M_stop` warrant, and no competent `stopping_occurred` Event for token `2`. The only competent stopping occurrences are separate EOF or representation-insufficiency branches. Therefore the token-2 road is **lawfully unavailable before the required semantic and stopping crossings**: exact negative-option selection is not treated as stopping by identity.

## H. Fidelity verdict

| Road | Verdict | Exact bounded basis |
| --- | --- | --- |
| live closed-choice selection through treatment selection | **mixed** | Presentation occurrence, one-response capture/currentness, exact token membership, selected row testimony, and treatment-selection lineage are implemented. Presented-alternative identity -> source candidate, source -> proposition assertion/warrant, applicability, and admission are absent; the ref-to-treatment conversion is not constitutionally warranted as a semantic relation |
| closed-choice binding into BOGE | **lawfully unavailable before the required crossing** | The BOGE entry point refuses every binding because no competent goal-semantic admission producer exists; no exact operator selection can currently reach BOGE on this road, but the refusal avoids reconstructing a goal from token/ref/label |
| admitted-interpretation road through applicability/admission | **unfaithful** | Caller-carried `proposed_meaning` is dropped at `CandidateWarrant`; applicability and admission preserve artifact lineage and identity, not the exact candidate-to-proposition relation |
| admitted-interpretation admission into BOGE | **unfaithful** | BOGE is a responsible consumer occurrence for the exact declared consumer/purpose and preserves the received snapshot, but ordinary carried input lacks `proposed_meaning`; successful establishment strengthens `label` into `intended_outcome` |
| token-2 local-stop road | **lawfully unavailable before the required crossing** | Exact alternative selection is recorded once, then the implementation explicitly declines to establish bounded stopping; source, meaning warrant, and stopping occurrence are not fabricated |

### Governing answer

There is **no exact current producer -> representation -> meaning-relation warrant -> consumer-local applicability -> admission -> BOGE road** proving that source candidate `G` expresses bounded proposition `M`.

The closed-choice production road has the strongest one-response and exact presented-set witness, but stops at a locally referenced treatment row and is categorically refused by BOGE. It cannot reach BOGE, faithfully or otherwise. The admitted-interpretation island can reach an `established` BOGE, but it loses `M` precisely when `InterpretationCandidate` becomes `CandidateWarrant`; later surfaces preserve the wrong semantic object and BOGE reconstructs content from `label`. Consequently, no exact operator selection reaches BOGE without semantic reconstruction, and the implementation does not presently witness the constitutional road under an unexpected owner.

Known Unknowns are the constitutional identity/role of closed-choice `option_ref`; the producer and evidence that would establish any presented-alternative-to-source relation; the responsible meaning owner and evidence for either source-to-proposition relation; and whether any external, unrecovered caller constructs equivalent artifacts with occurrence standing. Repository call-site search found none, and this report does not infer one.

## I. Smallest next implementation question

**At the current candidate-warrant production boundary, what exact proposition relation is the computed candidate-local warrant claiming to warrant?**

