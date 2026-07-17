# Constitutional Bounded Question Origination Topology 001

Repository authority wins.

## Boundary and stopping rule

This investigation asks how the current condition of a bounded goal can produce zero, one, or many candidate constitutional questions, and what separately establishes each candidate as a lawful bounded constitutional question.

It stops at candidate establishment or refusal. It does not define frontier admission, present-movement selection, examination admission, performance, queues, schedulers, planners, selectors, or a universal question generator. The phrase "the next question" is intentionally not used as an origination concept.

The recovered topology is:

```text
goal-relative unresolved condition
  != question-worthy condition
  != candidate-question formation
  != established bounded question
  != frontier membership
  != present-movement selection
  != examination admission
```

Current implementation strongly supports bounded-goal establishment and caller-testimony preservation. It does not implement a goal-relative constitutional question producer that consumes a live bounded-goal condition and forms candidate questions. Therefore most origination transitions below are constitutionally supported as required boundaries, but unrealized.

## Evidence base

Primary implementation witnesses inspected:

- `seed_runtime/bounded_operator_goal_establishment.py`
- `tests/test_bounded_operator_goal_establishment.py`
- `seed_runtime/bounded_constitutional_question.py`
- `tests/test_bounded_constitutional_question.py`
- `seed_runtime/constitutional_view_selection.py`
- `tests/test_constitutional_view_selection.py`
- `seed_runtime/operator_authority_scope_binding.py`
- `seed_runtime/question_surface_inventory.py`
- `tests/test_question_surface_inventory.py`

Prior reports used as testimony and evidence locators, not as producer authority:

- `constitutional_bounded_goal_question_bridge_001.md`
- `constitutional_bounded_question_frontier_topology_001.md`
- `constitutional_bounded_question_road_standing_audit_001.md`
- `constitutional_act_characterization_001.md`

## Core finding

The current repository can expose many goal-relative conditions that might invite inquiry, but it does not implement the act that judges them question-worthy and forms candidate bounded constitutional questions from them.

The only implemented object named as a bounded constitutional question is `BoundedConstitutionalQuestion`. Its producer, `produce_bounded_constitutional_question()`, deterministically preserves explicit caller-supplied fields. Its own module says it preserves caller inputs as evidence or testimony without projecting views, discovering capabilities, selecting authority, writing ledgers, or mutating cluster state. Tests confirm that testimony is not fact, authority, capability, selection, or projection.

Consequently:

- A bounded goal can expose zero, one, or many unresolved conditions.
- Current implementation does not decide which exposed conditions are question-worthy.
- Current implementation does not form zero, one, or many candidate questions from a condition.
- Current implementation can preserve an explicitly supplied question-shaped artifact as testimony.
- Current implementation can project caller-declared selection keys from that artifact for registered-view routing, but that is downstream routing, not origination.

## Side A: implemented bounded-goal families as source evidence

`BoundedOperatorGoalEstablishment` is the strongest implementation-backed bounded-goal family. It can be established from four ingress families:

1. closed-choice selection binding;
2. operator expression interpretation;
3. authority/scope binding plus matching interpretation and attributed expression;
4. downstream interpretation admission for the exact bounded-goal consumer and purpose.

Across those families, the implementation may expose the following source evidence:

| Exposed condition | Implementation standing | Question-worthy standing |
|---|---|---|
| `known_scope` | Established or provisional bounded orientation. | Not question-worthy by itself. It may show what is already bounded, including completed or fulfilled work. |
| `unresolved_scope` | Preserved unresolved, unsupported, excluded, refused, residual, or applicable-but-unadmitted material depending on ingress. | Visible pressure only unless a separate question-worthiness act evaluates it. |
| `sufficiency_conditions` and `sufficiency_state` | Caller/test-provided sufficiency basis with states such as established, provisional, unsupported. | Insufficient sufficiency can be visible pressure; no implemented rule converts it into a question. |
| `stop_conditions` | Preserved lawful stop boundary supplied to goal establishment. | Stop authority can block further movement; no implemented question formation follows. |
| `unknowns` | Preserved unknown selection evidence, interpretation unknowns, expression unknowns, binding unknowns, admission unknowns. | Visible pressure only. Some unknowns cause refusal in admitted-interpretation and authority/scope paths, but refusal is goal establishment refusal, not question origination. |
| `conflicts` | Preserved conflicts and identity mismatches. | Conflict can refuse goal establishment in some families; no implemented question-worthy transformation. |
| `known_loss` | Preserved loss from interpretation or selected candidate lineage. | Visible limitation only. |
| `operator_constraints` | Preserved constraints. Tests prove they are not enforced by goal establishment. | Boundary evidence, not question-worthiness. |
| `upstream_*_refs` and snapshots | Exact lineage for admitted interpretation and authority/scope handoff. | Required evidence for future binding; not a producer. |
| booleans such as `inquiry_opened`, `work_authorized`, `execution_started`, `recording_started`, `satisfaction_judged` | Explicit negative effects: establishment does not open inquiry, authorize work, execute, record, or judge satisfaction. | Prevents compression into frontier, selection, or examination. |

### Source conditions requested in the prompt

- **Unresolved scope:** implemented as `unresolved_scope`; it preserves unresolved references, unsupported residual spans, excluded scope refs, known refusals, applicable-but-unadmitted reasons, and residual source refs. It is not a question producer.
- **Absent or insufficient advancement needs:** no goal-relative advancement-need-to-question producer was found. Advancement-need surfaces are separate selection/consideration surfaces, not bounded constitutional question origination.
- **Unknowns and conflicts:** implemented and preserved; in some goal paths they cause refusal. They do not by themselves form questions.
- **Blocked, deferred, failed, or refused movement:** implemented as refusal reasons and negative flags in goal establishment, authority/scope binding, admission, selection, and eligibility surfaces. They are stop/pressure evidence, not candidate questions.
- **Stale, unavailable, excluded, or missing evidence:** current implementation preserves missing/unknown/unavailable/excluded evidence locally in diagnostic and goal-adjacent surfaces, but no question-worthy standing is assigned globally.
- **Unsatisfied sufficiency conditions:** visible through provisional or unsupported sufficiency state. No implemented rule says provisionality requires a question.
- **Dependencies or prerequisites:** present as upstream refs, admission purpose/consumer, requirement evidence, capability keys, and dispatch prerequisites. They bind or refuse local use; they do not originate questions.
- **Remaining and negative authority:** authority/scope binding preserves permitted, unresolved, and excluded scope; `operator_authority_scope_binding.py` expressly says it does not produce a bounded constitutional question.
- **Lawful stop conditions:** explicitly preserved and paired with negative effect flags. They may require stopping rather than asking.
- **Current movement boundary:** visible through read-only/no-ledger/no-mutation flags and stage-specific boundary notes. It prevents compression into execution or examination.
- **Completed or already fulfilled work:** known scope, selected candidate refs, admitted snapshots, and satisfaction flags can show fulfilled orientation, but there is no duplicate/answered-question evaluator.

## Question-worthiness distinctions

The repository supports the need to distinguish question-worthiness outcomes, but does not implement a single question-worthiness judge for bounded-goal conditions.

| Outcome | Current support | Evidence and authority required for a real judge |
|---|---|---|
| no question warranted | Constitutionally supported but unrealized. Local surfaces can show already established scope, stop conditions, no unresolved material, or refused movement. | Exact goal lineage, current position, fulfilled work, sufficiency, stop conditions, and authority proving non-formation is lawful. |
| question permitted | Constitutionally supported but unrealized. Existing question-shaped constructor can preserve caller text but cannot judge permission. | Evidence that the condition is within goal authority, not blocked, not already answered, and can be bounded without selecting it. |
| question required | Unsupported by current implementation as a general outcome. No urgency, priority, or mandatory-question rule was found. | Explicit repository authority requiring question formation from a condition; none found. |
| question premature | Constitutionally supported but unrealized. Goal establishment can refuse or remain provisional; question-surface eligibility can refuse dispatch prerequisites. | Proof that prerequisite binding, authority, evidence territory, or current position is missing. |
| question unsupported | Partially implemented as local unsupported/refused states, but not for question origination. | Exact unsupported reason tied to source condition, not merely failed downstream routing. |
| question blocked by authority | Supported as an authority/scope concept, unrealized as question-worthiness. | Negative authority, excluded scope, binding state, and stop condition showing the candidate cannot be lawfully formed. |
| question already answered | Not implemented for bounded constitutional origination. | Exact lineage from candidate semantics to fulfilled work or established answer. |
| question duplicated | Not implemented for bounded constitutional origination. | Identity and overlap comparison against other candidates or established questions. |
| Unknown | Supported as a preserved condition broadly. Unrealized as a question-worthiness final judgment. | Evidence insufficiency statement that does not promote pressure into a question. |

No outcome above selects among questions. Worthiness is only a local standing judgment about whether a condition may or must proceed to candidate formation, or must stop.

## Candidate-question formation topology

### Required constitutional act

A candidate-question formation act would have to consume one question-worthy condition and produce zero, one, or many candidate-question artifacts. This act is not implemented.

It would need to transform a condition into bounded interrogative content while preserving exact source standing. Natural-language generation alone would not suffice. Required formation evidence would include:

- source artifact identities;
- bounded-goal identity and establishment state;
- current constitutional position;
- fulfilled work and unresolved work;
- the exact source condition being questioned;
- candidate question text or semantic content;
- included and excluded scope;
- evidence demand;
- available, unavailable, stale, excluded, and missing evidence territory;
- dependencies and prerequisites;
- uncertainty, Unknowns, conflicts, and known loss;
- remaining and negative authority;
- sufficiency and stop conditions;
- duplication and overlap evidence.

### Zero/one/many behavior

One source condition may lawfully yield:

- **zero candidate questions** when the condition is not question-worthy, is already fulfilled, is blocked by authority, is premature, is unsupported, duplicates an established candidate, or must stop;
- **one candidate question** when evidence supports exactly one bounded inquiry without collapsing unrelated scope;
- **many candidate questions** when one unresolved condition contains separable subject, scope, evidence-territory, authority, conflict, or sufficiency components;
- **Unknown** when the repository lacks evidence to decide formation cardinality.

Current implementation does not perform this cardinality judgment. `produce_bounded_constitutional_question()` always returns one artifact when required caller inputs are supplied; that is constructor cardinality, not constitutional formation cardinality.

### Supported candidate sources

No source condition currently has implementation-backed standing as a supported candidate-question source. The following are potential source testimonies only:

- bounded-goal `unresolved_scope` entries;
- bounded-goal `unknowns` and `conflicts`;
- provisional or unsupported `sufficiency_state`;
- `stop_conditions` and negative authority;
- admitted interpretation residual source material;
- question-surface inventory family definitions and eligibility refusals;
- caller-supplied bounded question fields.

Each can testify to pressure or boundary. None is implemented as a producer.

## Question binding

Binding must be distinguished from semantic resemblance. A string that resembles a prior concern is not bound to that bounded goal.

A candidate question would be bound only if an implementation-backed act connected it to:

- the exact bounded goal (`goal_establishment_id` and ingress lineage);
- the current constitutional position;
- fulfilled work and unresolved work;
- source evidence and provenance;
- evidence territory;
- authority boundaries and negative authority;
- Unknowns, conflicts, known loss, and unavailable evidence;
- sufficiency and stop conditions.

Current implementation has strong binding primitives for other domains: closed-choice binding binds a selected token to a presented choice set; bounded-goal establishment binds exact ingress artifacts to a goal orientation; admitted interpretation handoff preserves selected meaning snapshots without recomputation; `BoundedConstitutionalQuestion` binds a stable ID to explicit caller payload. But no implementation binds a candidate question to a bounded goal's current condition.

Therefore question binding is constitutionally supported but unrealized as a local act family. It may be part of formation, establishment, or a separate local act in future implementation; current evidence does not settle that topology.

## Establishment or refusal boundary

A bound candidate would become an established bounded constitutional question only through an additional establishment judgment. That judgment is not implemented for goal-relative candidates.

Required establishment evidence would include:

- exact candidate identity and lineage;
- proof that candidate formation consumed a question-worthy condition;
- bounded-goal and current-position binding;
- scope completeness adequate for bounded inquiry;
- evidence-demand sufficiency;
- authority and negative-authority review;
- conflict and Unknown treatment;
- duplicate and overlap treatment;
- stop-condition review;
- provisional-standing rule if uncertainty remains admissible;
- refusal reason when establishment is unlawful.

Lawful establishment outcomes would include:

- established bounded question;
- provisionally established bounded question;
- refused because no question is warranted;
- refused because premature;
- refused because unsupported;
- refused because blocked by authority;
- refused because already answered;
- refused because duplicated or overlapping beyond supported scope;
- Unknown because establishment evidence is incomplete.

An established question must remain valid without being admitted to a frontier, selected for movement, admitted to examination, authorized for execution, or answerable. Current downstream selection tests help preserve that boundary: selection consumes only projection keys and can return no selected view while preserving uncertainty. That downstream artifact does not prove origination.

## Existing artifact audit

### `BoundedConstitutionalQuestion`

Fields that can lawfully survive as **candidate-question testimony**:

- `operator_inquiry` as preserved caller/operator text;
- `inquiry_provenance` as caller-provided provenance text;
- `bounded_question` as caller-supplied question content;
- `constitutional_intent` as caller-supplied intent testimony;
- `scope_status` as caller-supplied scope testimony;
- `uncertainty` and `unknowns` as preserved caller-supplied uncertainty;
- `caller_supplied_fields` as exact caller-declared fields;
- `testimony_status` and `read_only_boundaries` as non-promotion warnings;
- `read_only`, `writes_event_ledger`, and `mutates_cluster` as operational boundary flags.

Fields that can survive as **established-question identity** only after a missing establishment act:

- `bounded_question_id`, because it is stable over supplied payload but currently identifies testimony, not lawful goal-relative establishment;
- `bounded_question`, if later linked to exact formation and establishment evidence;
- `scope_status`, if later verified against implementation evidence.

Fields that do **not** currently establish goal-relative lineage:

- all fields, unless supplied by caller as testimony only. There is no `goal_establishment_id`, current-position reference, fulfilled-work record, unresolved-condition identity, evidence-territory record, authority-boundary record, stop-condition record, or duplicate/overlap audit in the artifact.

### `produce_bounded_constitutional_question()`

This function is implemented only as caller testimony preservation. It produces one deterministic artifact from explicit inputs and stable identity hashing. It performs no natural-language classification, no source-condition detection, no worthiness judgment, no candidate formation, no binding to bounded-goal condition, no establishment judgment, no projection, no selection, no ledger write, and no mutation.

It should not be treated as the constitutional producer for this topology without adding missing acts.

### Projection and routing artifacts

`project_constitutional_question()` extracts only exact caller-declared `selection_key` fields and carries uncertainty. `select_constitutional_views()` compares those keys to registered capability keys. These fields belong to caller-directed registered-view routing, not question origination:

- `selection_key` and `selection_key:*` caller fields;
- `ConstitutionalQuestionProjection.selection_keys`;
- `SelectedConstitutionalViews.selected_view_names`;
- composition request `requested_views` and selection limits.

They may be useful after establishment, but they do not recover evidence demand or question source conditions.

## Transition table

| Boundary | Consumed standing | Constitutional effect | Resulting standing | Evidence and authority required | Zero/one/many behavior | Negative/provisional/Unknown result | Implementation witness | Counterexample preventing compression | Missing realization | Classification | Remaining Unknown |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Goal establishment | Ingress binding, interpretation, authority/scope binding, or admitted interpretation | Establishes or refuses bounded operator goal orientation | Established, provisional, or refused bounded goal | Exact ingress identity, lineage, admitted consumer/purpose where relevant, sufficiency, stop, Unknown/conflict preservation | One goal artifact per call | Refused/provisional/unsupported states | `bounded_operator_goal_establishment.py`; tests | Establishment flags do not open inquiry, authorize work, execute, record, or judge satisfaction | None for goal establishment itself | Constitutionally supported and implemented | Whether all future goal families should share one shape |
| Goal condition exposure | Established/provisional/refused goal artifact | Makes scope, Unknowns, conflicts, stops, sufficiency, lineage visible | Source testimony / pressure | Goal artifact fields and lineage | Zero, one, or many visible conditions | Empty fields, refused state, Unknowns | Goal establishment fields/tests | Visible unresolved scope is not a question | No question-worthiness handoff | Constitutionally supported and implemented as exposure only | Which conditions should be considered by a future judge |
| Condition -> question-worthiness | Goal-relative condition | Judges whether question formation is warranted, permitted, required, premature, unsupported, blocked, answered, duplicate, or Unknown | Question-worthy or refused/Unknown condition | Current position, fulfilled work, authority, sufficiency, stop, duplicate evidence | Zero or more conditions may pass | no-question, premature, unsupported, blocked, answered, duplicate, Unknown | No direct implementation | Provisional sufficiency does not require a question | Entire act missing | Constitutionally supported but unrealized | Whether "required" is ever lawful in this repo |
| Question-worthiness -> candidate formation | Question-worthy condition | Forms bounded interrogative candidate(s) without selecting | Candidate-question testimony | Source identities, question content, scope, evidence demand, evidence territory, dependencies, Unknowns, conflicts, authority, stops | Zero/one/many/Unknown | Refusal if no lawful candidate can be formed | No direct implementation | Constructor returning one artifact is not formation cardinality | Entire act missing | Constitutionally supported but unrealized | Whether formation and binding should be one act |
| Candidate binding | Candidate question testimony | Binds candidate to exact bounded goal/current position/source evidence | Bound candidate | Goal ID, ingress lineage, current position, fulfilled/unresolved work, evidence territory, authority, stops | One candidate may bind to one exact lineage; overlap across candidates requires evidence | Refused/Unknown on mismatch or insufficient lineage | Analogous binding in closed-choice and goal establishment; no question binding | Semantic resemblance is not lineage | Question-specific binding missing | Constitutionally supported but unrealized / overlapping with binding act family | Whether binding belongs before or during establishment |
| Bound candidate -> established question | Bound candidate | Establishes lawful bounded constitutional question or refuses | Established/provisional/refused/Unknown bounded question | Worthiness, formation, binding, scope completeness, evidence demand, authority, conflicts, duplicates, stops | Each bound candidate judged independently; source may yield zero/one/many established questions | Provisional, refused, Unknown | Current `BoundedConstitutionalQuestion` only preserves testimony | Stable ID over caller payload does not prove lawful establishment | Establishment judge missing | Constitutionally supported but unrealized; current artifact implemented only as caller testimony preservation | What uncertainty is admissible for provisional standing |
| Established question -> frontier membership | Established question | Would admit to frontier | Frontier member | Out of scope | Not evaluated | Not evaluated | Frontier topology reports only as locators | Established question can remain valid without frontier | Not investigated here | Stopping boundary | Unknown |
| Frontier membership -> present movement selection | Frontier member | Would select for movement | Selected movement target | Out of scope | Not evaluated | Not evaluated | Selection-path implementation is separate local selection | Origination must not select | Not investigated here | Stopping boundary | Unknown |
| Selection -> examination admission | Selected target | Would admit to examination | Examination work | Out of scope | Not evaluated | Not evaluated | Examination work selection is separate | Selection is not examination admission | Not investigated here | Stopping boundary | Unknown |

## Exact stopping boundary

This topology ends when a candidate is established, provisionally established, refused, or left Unknown as a bounded constitutional question. It does not answer whether that established question belongs to a frontier, should be selected, may be examined, should be executed, can be answered, or should be recorded.

## Final conclusion

The current condition of a bounded goal can expose zero, one, or many possible source conditions, but current implementation does not originate candidate constitutional questions from those conditions. The repository currently preserves caller-supplied question-shaped testimony and routes caller-declared selection keys downstream. A lawful goal-relative origination topology would require separate question-worthiness, candidate formation, candidate binding, and establishment/refusal acts, each with exact evidence and authority. Those acts are constitutionally required boundaries for this question, but they remain unrealized.

Bounded constitutional question origination topology 001 complete.
