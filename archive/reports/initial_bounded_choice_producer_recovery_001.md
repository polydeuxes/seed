# Initial bounded-choice producer recovery 001

## 1. Scope, method, and governing finding

This is one bounded, report-only recovery at commit `62b8255`, immediately
after PR 2022. It changes no canonical Book, root documentation, `docs/`, prior
report, production code, test, diagnostic, CLI, ledger, State, or cluster
state. It cross-examines repository implementation against the active
constitutional Books; tests, exports, reports, and caller-authored objects are
not accepted as product meaning producers.

**Governing finding:** no existing constitutional responsibility and connected
application producer currently warrants a non-empty initial enum for arbitrary
uninterpreted operator text. The strongest lawful initial-response
responsibility is a composition of two already-recognized responsibilities:

1. Seed-owned question formation may eventually form a bounded clarification
   question from attributed operator material, but only after Seed-side
   interpretation and bounded standing establishment; and
2. responsible egress representation/emission may present a bounded result,
   including a refusal or stopping result, without strengthening its standing.

Neither responsibility currently supplies the missing option meanings. For an
uninterpreted first utterance, the only response the repository can warrant
now is a deterministic **terminal insufficiency/refusal**, not a closed-choice
presentation:

```text
Seed cannot interpret this input with an admitted meaning. No bounded choices are available. Stopping.
```

That wording is a proposed implementation string, not existing constitutional
vocabulary. Its assertions are deliberately limited to the local admission
failure and absence of a warranted choice producer. It does not characterize
the text, establish a goal or inquiry, request clarification, or claim global
impossibility.

The smallest prerequisite for a real producer is therefore a product and
constitutional decision that assigns one application-owned bootstrap
responsibility an exact bounded meaning vocabulary and specifies what selection
of each meaning establishes. Until then, building a controller whose producer
is supplied by tests, configuration, or arbitrary callers would repeat the
fake-only road prohibited by this recovery.

## 2. Current evidence boundary

### 2.1 What PR 2022 recovered

`interactive_shell_implementation_recovery_001.md` recovered a two-input shell
plumbing contract around `PresentedClosedChoiceSet`,
`OperatorSelectionTokenCapture`, and `bind_closed_choice_selection`. It also
found the universally runnable success path blocked on an application-owned
producer. PR 2022 did not nominate that producer or create option meanings.

The implementation remains unchanged:

* `ClosedChoiceOption` contains `token`, `option_ref`, `presented_label`, and
  `presented_detail`;
* `PresentedClosedChoiceSet` contains a prompt, ordered options, optional
  presentation reference, provenance, Unknowns, and conflicts;
* the binder compares the captured string exactly within that exact set;
* its boundary notes say binding is not a goal transition, operator authority,
  inquiry selection, execution, or authorization; and
* no production call site constructs or binds a choice set. Outside the
  defining modules, the symbols are only exported; concrete construction is in
  tests.

Thus there is a real local binder but no real initial candidate-set producer,
presentation occurrence, or downstream option consumer.

### 2.2 Constitutional controls

The controlling repository statements are asymmetric:

* artifact shape and public construction do not supply production authority
  (`constitutional-kinds-and-artifact-standing.md`,
  `constructors-and-production-authority.md`);
* candidate production must preserve producer, source role, formation
  occurrence, scope, authority, provenance, and Unknown dimensions
  (`external-and-constitutional-grammar.md`, clause 01.External.F);
* a selection act requires a bounded candidate set plus exact evidence or
  policy, while selection alone establishes no downstream subject
  (`selection-artifacts-and-selection-acts.md`);
* question-shaped external material is testimony, and bounded internal question
  formation is Seed-owned only after interpretation and standing establishment
  (`questions-and-inquiry.md`, especially 04.Question.B and E);
* communication and emission preserve standing but do not prove
  interpretation, uptake, or establishment
  (`representation-emission-and-consumer-boundaries.md`, especially
  08.Communication.C); and
* refusal, a clarification request, a policy block, and failed performance are
  distinct outcomes (`refusal-and-non-performance.md`).

These controls allow honest non-performance. They do not implicitly create a
bootstrap menu.

## 3. Exact candidate-owner topology

The topology below distinguishes receipt of bytes, formation of meaning,
choice-set production, emission, selection binding, and semantic consumption.

| Possible owner | Exact input | Knowledge of arbitrary uninterpreted text | Why it may present choices | Authority and warrantable option semantics | Exact consumer | Still prohibited | Finding |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **operator ingress** | one exact line/EOF occurrence and session-local occurrence metadata | exact material and occurrence only; no admitted meaning | none from ingress itself | may preserve exact text, distinguish line/EOF mechanically, and report capture conditions; may not label intent | a later interpretation or response owner, currently absent | parsing English into goal/question/command, inventing candidates, choosing a response meaning | **not producer** |
| **communication / egress emission** | an already warranted bounded result plus declared purpose, scope, provenance, limits, Unknowns, refusal and stop conditions | only what the source result asserts | may render options only if an upstream producer already warranted them | faithful representation and evidenced emission; no authority to create option meaning | candidate operator recipient; receipt and interpretation remain separate | strengthening, inferring intent, making presentation equal establishment | **renderer/emitter only** |
| **interpretation warrant production** | `ExactOperatorMaterial`, caller-supplied interpretation candidates, and explicit candidate evidence | exact material plus only supplied candidate claims/evidence | may expose warranted candidate meanings after real candidate formation and warrant evidence | may warrant/unknown/refuse each supplied candidate; does not originate universal candidates | contextual interpretation selector requiring candidate-bound selection evidence | generating candidates from arbitrary English, auto-selecting, presentation, goals/inquiry | **potential derived producer only when upstream candidates exist; unavailable initially** |
| **interpretation selection** | one warrant set plus exact candidate-bound selection evidence | warranted candidates and preserved source, not independently understood prose | may not originate options; could consume an operator selection only after a separate translation proves that token binding is candidate-bound selection evidence | select one warranted candidate or preserve non-selection/refusal | applicability projection | treating visible labels or binder membership as selection evidence | **consumer, not producer** |
| **clarification** | no dedicated runtime artifact or producer exists; constitutionally it would consume attributed material plus a bounded question-forming basis | no current connected knowledge | a bounded clarification question could present response forms only if Seed has formed the question and warranted the answer domain | repository recognizes request-for-clarification as distinct non-performance, not a fixed option taxonomy | operator response as further testimony, then a distinct interpretation boundary | assuming “restate,” “clarify,” or any response category; treating clarification as abandonment or meaning | **constitutional possibility, no implemented owner or vocabulary** |
| **inquiry / question formation** | attributed operator material or other bounded sources after Seed-side interpretation and standing establishment | whatever the admitted source and question-forming act warrant | may form a bounded Seed question with identity, provenance, scope, evidence demand, authority limits, uncertainty, and stop conditions | owns internal question formation, not classification of raw question-looking prose | operator response as further testimony or a bounded inquiry consumer | treating an apparent question as inquiry, canonizing CLI question families, unbounded investigation | **strongest future semantic owner, but its preconditions fail for raw uninterpreted input** |
| **closed-choice presentation/binding** | caller-built exact choice set and a capture naming that set | prompt/options supplied by caller and literal token membership only | may represent and bind already-produced local choices | exact set fingerprint and local token membership; zero semantic production authority | optional BOGE function or another as-yet-unimplemented option-specific consumer | inventing options, global token meanings, interpretation, goal/inquiry transition | **mechanism, not producer** |
| **bounded operator goal establishment (BOGE)** | a bound `ClosedChoiceSelectionBinding`, or an admitted interpretation for its exact consumer/purpose | bound ref/label in the first path; admitted selected meaning in the second | does not own initial presentation | currently asserts a goal for every locally bound choice on the closed-choice path | later goal-oriented work, outside this recovery | consuming generic navigation/clarification/stop choices as goals | **downstream consumer with a mismatch; not producer** |
| **refusal and lawful stopping** | a bounded failure of authority, capability, evidence, preservation, admission, or other required condition | the exact failure and its limits; not the text's meaning | need not present any choices; may communicate non-performance and stop | may preserve why movement cannot lawfully continue without claiming completion or global impossibility | egress representation/emission, then termination | silently dropping input, calling refusal success, inventing recovery choices | **strongest lawful current response result** |
| **other response/presentation implementations** | their stage-specific existing artifacts | only their own artifact assertions | may format those artifacts for their declared purposes | domain-local rendering only | their existing CLI/diagnostic consumers | reuse as generic dialogue meaning, promoting presentation vocabulary | **not initial producer** |

No application configuration registry supplies initial meanings. No existing
response owner combines raw utterance intake, interpretation failure,
application-owned choices, and exact consumers. Tests construct choice meanings
such as inventory/audit labels, but tests are excluded as authority. Exports
prove reachability only. Reports prove neither a production occurrence nor
runtime ownership.

## 4. Option-by-option audit

### 4.1 Exact warranted option set

**The exact warranted set is empty.** There is therefore no lawful
`PresentedClosedChoiceSet` for arbitrary uninterpreted first input: the current
type permits an empty tuple, but rendering an empty enum would falsely imply a
choice interaction. The controller must instead emit terminal refusal without
constructing a choice set.

| Potential outcome | Repository support | Why it is not currently an initial option | BOGE status |
| --- | --- | --- | --- |
| restate or clarify current message | clarification is recognized as distinct from refusal/abandonment; Seed may form bounded questions | no producer defines `token`, label, exact meaning, question identity, accepted answer domain, or next consumer; “clarify” itself is ambiguous | must not enter BOGE |
| classify as bounded operator goal | admitted interpretation can enter BOGE | raw text is not admitted meaning; no raw-text classifier or candidate evidence exists | only after the full interpretation applicability/admission road, not from this menu |
| classify as bounded inquiry/question | question-shaped prose is only testimony; Seed owns internal question formation | no bounded translation has established identity, scope, evidence demand, authority, uncertainty, or stop conditions | must not enter BOGE; inquiry has a different consumer |
| preserve without interpretation | exact preservation is mechanically possible | preservation is what ingress must already do, not an alternative meaning selected later; no downstream selection consumer is defined | must not enter BOGE |
| stop without establishing meaning | lawful stopping/refusal is supported | it is immediately available as the producer's outcome and does not require asking the operator to select it; no reason to turn it into a menu option | must not enter BOGE |
| establish a communication relation | emission can be evidenced separately | operator selection cannot retroactively establish delivery, receipt, interpretation, uptake, responsibility, or authority; communication is not establishment | must not enter BOGE |
| request external grammar assistance | external grammar may remain attributed and addressable | no assistance provider, request producer, translation warrant, authorization, or consumer is connected; explicitly outside this task | must not enter BOGE |

Consequently there are no supported field-level rows with an exact local token,
operator label, stable option reference, semantic producer, selection effect,
consumer, and next rendered response. In particular, `1`, `2`, and `3` have no
global or initial standing; a numeric string before presentation is merely
operator material.

### 4.2 Fields any future real option must carry

The current `ClosedChoiceOption` shape is sufficient for local display and
binding but insufficient to prove semantic production or downstream use. A real
producer result needs, at minimum, these fields (names are proposed, not new
constitutional kinds):

| Field | Required assertion |
| --- | --- |
| `token` | exact local comparison string; no trimming, numeric parsing, aliases, case folding, or global meaning unless explicitly specified |
| `presented_label` | operator-visible presentation text only |
| `presented_detail` | optional deterministic explanation, still presentation only |
| `option_ref` | stable identity of the bounded meaning, distinct from label |
| `bounded_meaning` | exact assertion established by selecting this option |
| `meaning_kind` | exact consumer contract, such as clarification response, interpretation candidate selection, inquiry response, terminal stop, or goal outcome; kinds cannot be inferred from labels |
| `producer_ref` | application-owned responsibility that formed the option |
| `formation_occurrence_ref` | evidence that this producer formed this option for this input/context |
| `source_material_refs` | exact utterance/candidate/configuration material relied upon |
| `production_basis` | policy, admitted candidate evidence, or constitutional bootstrap decision warranting the meaning |
| `scope` / `authority_limits` | what selection may and may not establish |
| `provenance` | traceable producer/source evidence, not caller assertion alone |
| `unknowns` / `conflicts` / `refusal_conditions` | limits preserved through presentation, binding, and consumption |
| `consumer_ref` / `consumer_purpose_ref` | exact downstream intake that accepts the bound meaning |
| `selection_effect` | precise local standing created by a valid bound token |
| `next_response_spec` | deterministic response kind/content source after consumption |
| `boge_eligible` | explicit false by default; true only with goal-establishment-specific evidence |

The presented choice set additionally needs producer identity, production
occurrence, exact input/context identity, a non-empty option invariant, a real
presentation occurrence reference, deterministic order, and preservation of
the complete semantic option records in its fingerprint or a bound immutable
semantic-set fingerprint. Otherwise a token can bind to rendered content while
its claimed meaning changes out of band.

## 5. Fixed, configured, and derived vocabulary adjudication

### Fixed constitutional bootstrap vocabulary — **not currently warranted**

A fixed vocabulary would be the cleanest initial producer because it could
respond without pretending to understand the text. But the active Books do not
enumerate bootstrap response meanings, tokens, or consumers. General
responsibilities such as clarification, question formation, refusal, and
communication do not entail a closed list. Implementing a fixed set now would
make application code the constitutional author without the required product
decision.

### Application configuration — **testimony only; insufficient alone**

Configuration can supply strings, ordering, and candidate assertions. It does
not give those assertions constitutional authority, create formation occurrence
standing, prove consumer compatibility, or decide what selection establishes.
A configured menu becomes lawful only when an application-owned producer is
authorized to consume that exact configuration as bounded testimony and
validate it against an established meaning/consumer contract.

### Active candidate interpretations — **lawful derived family, unavailable here**

This is the strongest repository-backed derivation model. If a real candidate
producer preserves attributed candidates and evidence, the contextual warrant
producer can assess them. A presentation producer could then derive options
from exactly the warranted candidates, preserving candidate refs, evidence,
Unknowns, conflicts, and source spans. The operator's token would still need a
separate candidate-bound selection-evidence adapter before the contextual
selector could consume it. Arbitrary first input currently has no candidate
producer, so the derived set is unavailable rather than empty by semantic
judgment.

### Current consumer capabilities — **filter, not source of meaning**

Consumer contracts can reject or narrow already-produced meanings. They cannot
originate interpretations merely because code can consume a particular shape.
BOGE availability, question-family inventory, formatters, and CLI routes must
not be inverted into initial meanings.

### Adjudication

The initial vocabulary is **unavailable until more evidence exists**. The
preferred smallest decision is a fixed, application-owned constitutional
bootstrap vocabulary because it can remain input-agnostic. If the product does
not authorize such a vocabulary, the later alternative is derived options from
real, evidence-bearing interpretation candidates. Configuration and consumer
introspection cannot independently fill the gap.

## 6. Closed-choice BOGE audit

The current closed-choice BOGE path performs:

```text
binding.bound_option_label or binding.bound_option_ref
    -> BoundedOperatorGoalEstablishment.intended_outcome
binding.bound_option_ref
    -> BoundedOperatorGoalEstablishment.known_scope
```

For any `binding_state == "bound"`, it reports `established` without checking
the option producer, semantic kind, consumer, purpose, formation evidence,
authority limit, or an explicit claim that selection establishes a goal. The
visible label is therefore treated as goal meaning even though the binder
defines it as presentation and explicitly says binding is not a goal
transition.

This is a **compatibility mismatch** for a general initial menu. The mapping
`presented_label -> intended_outcome` is faithful only in the narrow case where
an upstream producer has already warranted that the exact label itself is the
complete bounded goal outcome and that the option is specifically for BOGE.
The present types cannot prove that case.

Before a bound token may enter BOGE, the option/consumer seam would need:

* separate `bounded_meaning` and immutable meaning identity;
* `meaning_kind = bounded_operator_goal_outcome`;
* exact BOGE `consumer_ref` and `purpose_ref`;
* application producer and formation occurrence identity;
* establishment basis and provenance;
* known and unresolved scope;
* Unknowns, conflicts, known loss, authority limits, and refusals;
* source lineage from the presentation through token capture;
* evidence that the operator selected this meaning, not merely matching display
  text; and
* a BOGE admission/check that refuses non-goal meanings.

Clarification, inquiry, preservation, communication, and stopping options must
never enter BOGE merely because their token bound. This pass does not repair
BOGE.

## 7. Deterministic asymmetric specimens

With no admitted interpretation and no real producer, all non-EOF first lines
have the same semantics. “Preserve” below means the exact received material is
retained in the ephemeral ingress occurrence before the terminal response; it
does not mean recording in the ledger or State.

| First occurrence | Required treatment | Exact response |
| --- | --- | --- |
| `hello` | preserve exactly; infer neither greeting nor communication relation | `Seed cannot interpret this input with an admitted meaning. No bounded choices are available. Stopping.` |
| `learn English` | preserve exactly; infer neither command nor goal | same terminal response |
| obvious-looking question, e.g. `What is Seed?` | preserve exactly; question shape remains testimony, not internal inquiry | same terminal response |
| obvious-looking command, e.g. `Show inventory` | preserve exactly; infer neither command nor goal | same terminal response |
| empty line | preserve the empty line as an occurrence; do not turn absence of characters into a stop token or meaning | same terminal response |
| whitespace-only line | preserve every whitespace character; do not trim into empty or parse | same terminal response |
| exact numeric token `1` before presentation | preserve as first operator material; no set exists, so it is not a selection token | same terminal response |
| text matching a hypothetical option label | preserve as first operator material; labels have no token standing and no presentation is pending | same terminal response |
| EOF before first line | create no utterance and no choice set; terminate normally | no rendered response is required |

Because this response is terminal, the following are protocol violations rather
than second-turn interpretations:

| Later occurrence | Required treatment |
| --- | --- |
| second unrelated utterance after the terminal response | shell has stopped and must not read it as part of this bounded interaction |
| EOF after the terminal response | already stopped; no additional output |

For completeness, if a future real presentation exists, exact token comparison
must remain asymmetric: label text does not bind unless it is also explicitly a
token; unrelated text is `unsupported`; EOF creates no capture and stops; and a
token entered before its presentation can never be replayed as selection.

## 8. Smallest implementation slice and STOP

### 8.1 What is warranted now

No producer-plus-controller **choice success path** is warranted. The only
truthful implementation slice available now would be a one-input terminal
refusal shell:

```text
read exact first line
  EOF -> STOP with no output
  line -> preserve ephemeral occurrence exactly
       -> observe that no admitted interpretation/choice producer is available
       -> form bounded terminal insufficiency result
       -> render and emit exact refusal string
       -> STOP
```

That slice would not satisfy the product's eventual bounded-choice behavior and
is not requested for implementation here. It should not be disguised as a
choice producer with a single “stop” option.

### 8.2 Smallest decision that unlocks a real producer

Before implementation, one explicit product/constitutional decision must name:

1. the application responsibility that owns bootstrap response formation for
   uninterpreted operator material;
2. whether its vocabulary is fixed or derived;
3. every initial option's stable meaning identity and exact semantic assertion;
4. whether selecting each option creates testimony, requests clarification,
   selects an interpretation candidate, forms an inquiry response, stops, or
   establishes a bounded goal;
5. the exact consumer and purpose for each selection;
6. the evidence/provenance and formation occurrence needed to warrant each
   option for this presentation;
7. required Unknown/conflict/refusal behavior; and
8. the deterministic next response for each consumed meaning.

The minimal recommended decision is an input-agnostic fixed bootstrap
vocabulary owned by a named Seed response-forming responsibility, with all
options defaulting to `boge_eligible=false`. This report cannot choose its
members. If even one option is authorized, the first implementation slice can
be producer + semantic option artifact + presentation occurrence + exact
binder + exactly one option-specific consumer + deterministic response + STOP.

### 8.3 Explicit STOP conditions

Stop without presenting choices when:

* no named application-owned producer exists;
* the producer has no non-empty warranted set for this exact input/context;
* any option lacks stable meaning, producer/provenance, formation basis, exact
  consumer, selection effect, or next response;
* configuration is the sole claimed authority;
* options arise only from tests, exports, reports, labels, or caller-authored
  evidence;
* the only justification is a consumer's ability to accept a shape;
* presenting an option would infer meaning from obvious-looking English;
* Unknowns/conflicts make production or consumption unwarranted;
* a token arrives before presentation, a label arrives instead of its token,
  or a capture names a different/superseded set;
* EOF occurs; or
* the one selected bounded meaning has produced its one next response.

Do not create Demand, Gap, competency, PESC, learning, external grammar/LLM
integration, generic dialogue management, persistence, plugins, authorization,
or execution to bypass these stops.

## 9. Files inspected and report size

### Canonical constitutional evidence

* `book_of_seed/01-grammar-and-standing/README.md`
* `book_of_seed/01-grammar-and-standing/constitutional-kinds-and-artifact-standing.md`
* `book_of_seed/01-grammar-and-standing/constructors-and-production-authority.md`
* `book_of_seed/01-grammar-and-standing/external-and-constitutional-grammar.md`
* `book_of_seed/01-grammar-and-standing/lenses-views-and-roads.md`
* `book_of_seed/02-acts-and-constraints/README.md`
* `book_of_seed/02-acts-and-constraints/acts-and-act-artifacts.md`
* `book_of_seed/02-acts-and-constraints/constraints-policy-and-preconditions.md`
* `book_of_seed/02-acts-and-constraints/selection-artifacts-and-selection-acts.md`
* `book_of_seed/03-goals-and-advancement/README.md`
* `book_of_seed/03-goals-and-advancement/construction-and-establishment.md`
* `book_of_seed/03-goals-and-advancement/demands-and-opened-movement.md`
* `book_of_seed/03-goals-and-advancement/orientation-and-movement.md`
* `book_of_seed/03-goals-and-advancement/selection-and-authorization.md`
* `book_of_seed/04-inquiry-and-examination/README.md`
* `book_of_seed/04-inquiry-and-examination/examination-methods-and-probes.md`
* `book_of_seed/04-inquiry-and-examination/inquiry-frontiers.md`
* `book_of_seed/04-inquiry-and-examination/questions-and-inquiry.md`
* `book_of_seed/08-authority-communication-and-stopping/README.md`
* `book_of_seed/08-authority-communication-and-stopping/authority-scope.md`
* `book_of_seed/08-authority-communication-and-stopping/refusal-and-non-performance.md`
* `book_of_seed/08-authority-communication-and-stopping/representation-emission-and-consumer-boundaries.md`
* `book_of_seed/08-authority-communication-and-stopping/stopping-and-completion.md`

### Implementation and tests

* `seed_runtime/closed_choice_selection_binding.py`
* `seed_runtime/bounded_operator_goal_establishment.py`
* `seed_runtime/contextual_interpretation_warrant_set.py`
* `seed_runtime/contextual_interpretation_selection.py`
* `seed_runtime/interpretation_applicability_projection.py`
* `seed_runtime/downstream_interpretation_admission.py`
* `seed_runtime/candidate_requests.py`
* `seed_runtime/bounded_constitutional_question.py`
* `seed_runtime/question_surface_inventory.py`
* `seed_runtime/shared_explanation_rendering_projection.py`
* `seed_runtime/shared_explanation_presentation_admission.py`
* `seed_runtime/shared_explanation_bounded_composition.py`
* `seed_runtime/events.py`
* `seed_runtime/models.py`
* `seed_runtime/state.py`
* `seed_runtime/__init__.py`
* `scripts/seed_local.py`
* `tests/test_closed_choice_selection_binding.py`
* `tests/test_bounded_operator_goal_establishment.py`
* `tests/test_contextual_interpretation_warrant_set.py`
* `tests/test_contextual_interpretation_selection.py`
* `tests/test_interpretation_applicability_projection.py`
* `tests/test_downstream_interpretation_admission.py`

### Immediate historical baseline

* `interactive_shell_implementation_recovery_001.md` (PR 2022 baseline only;
  not edited)

This report adds exactly **434 LOC** in one new file; no inspected file was
edited.
