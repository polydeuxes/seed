# Interactive-shell implementation recovery 001

## 1. Scope and governing answer

This is one bounded, report-only recovery at commit `d18d40d`, immediately after
PR 2021. It changes no canonical Book, root documentation, `docs/`, prior report,
production code, test, diagnostic, CLI, ledger, projected State, or cluster
state. Repository constructors and tests are evidence about pieces, not evidence
that an operator can traverse a connected runtime road.

**Governing answer:** the smallest truthful contract is a two-input, one-pending-
presentation shell occurrence owned in process memory:

```text
read one line exactly
  -> preserve an operator-utterance occurrence (no interpretation)
  -> ask one explicit, application-owned bounded-choice producer for a choice set
  -> if and only if that producer returns a warranted non-empty set:
       render its prompt and exact token/label pairs deterministically
       retain that exact PresentedClosedChoiceSet as the sole current pending set
       read a second line exactly
       construct OperatorSelectionTokenCapture against that pending set
       bind_closed_choice_selection(pending_set, capture)
       render bound result OR unsupported retry/refusal
  -> STOP
```

The repository already implements the exact local membership operation in the
middle. It does **not** implement the shell owner, real stdin occurrences, a
general response artifact/renderer, a pending presentation, or a producer of an
initial option vocabulary. Therefore the first slice is implementation-ready as
a plumbing contract, but a universally runnable `seed shell` success path is
not truthful until one exact bounded producer is named. The shell must refuse
before presentation when no producer supplies warranted options. It must not
invent `1`, `2`, or `3` merely to exercise the binder.

## 2. Entry-point audit: exact current disconnected topology

### 2.1 Operator-facing ingress

The installed entry point is `seed = scripts.seed_local:main`. Its parser:

* accepts positional `message` tokens only for exact `ask --question-family`
  dispatch and says free-form mode is unsupported
  (`scripts/seed_local.py:790-797`);
* joins leftover positional tokens, rejects any non-empty free-form message,
  prints help otherwise (`scripts/seed_local.py:7160-7166`);
* has no call to `input()`, no iteration over `sys.stdin`, no prompt/write/read
  turn owner, and no interactive loop;
* has many one-shot explicit flags whose formatters print to stdout;
* has a one-shot free-text **inspection** flag, `--candidate-requests TEXT`, and
  a one-shot `--candidate-routes TEXT` flag (`scripts/seed_local.py:1609-1622`,
  `6559-6577`); and
* has a separate `--record-inquiry-note TEXT` probe, not shell ingress
  (`scripts/seed_local.py:1624-1634`).

Thus Seed has no general one-shot free-text command. It has one-shot flags that
accept text for explicitly bounded inspection/probe purposes. None hands its
text to closed-choice presentation or binding.

### 2.2 Free-text preservation islands

`inspect_candidate_requests(text)` copies `text` to `raw_text` before deriving a
normalized matching string (`seed_runtime/candidate_requests.py:88-97`). It
returns candidate-request representations and explicitly stops before command,
capability, policy, or tool execution (`candidate_requests.py:98-150`). The CLI
serializes this object to JSON and exits. It does not assign session, utterance,
turn, response, or presentation identity and has no binder handoff.

`ExactOperatorMaterial` preserves `exact_text` and explicit source spans
(`seed_runtime/contextual_interpretation_warrant_set.py:37-62`), but only a caller
constructs it. No production ingress constructs one. The contextual warrant
producer consumes caller-supplied candidates/evidence; it is not a free-text
parser (`contextual_interpretation_warrant_set.py:157-216`).

### 2.3 Closed-choice island

```text
caller constructs ClosedChoiceOption(s)
  + caller constructs PresentedClosedChoiceSet
  + caller constructs OperatorSelectionTokenCapture
  -> bind_closed_choice_selection
       bound | unsupported | unknown | conflict
       read_only=true
       writes_event_ledger=false
       mutates_cluster=false
```

`PresentedClosedChoiceSet` owns a choice-set ref, prompt, options, optional
presentation ref, provenance/unknown/conflict fields, and a deterministic
fingerprint (`closed_choice_selection_binding.py:31-73`). The fingerprint covers
the prompt, complete option records, presentation ref, and convention. The
binder first requires the capture's `choice_set_ref` to match, then compares the
captured token with that exact set (`closed_choice_selection_binding.py:121-183`).

This is representation plus a pure binding function. Searches excluding tests,
exports, and the defining module find no producer of either input and no CLI
consumer. In particular, the artifact does not prove that a prompt was actually
written or a token actually read.

### 2.4 Interpretation and goal islands

The contextual road is fully explicit and caller-fed:

```text
ExactOperatorMaterial + explicit candidates + explicit evidence
  -> ContextualInterpretationWarrantSet
  + candidate-bound selection evidence
  -> ContextualInterpretationSelectionResult
  + one supplied consumer contract and requirement evidence
  -> InterpretationApplicabilityProjection
  + exact consumer-local admission evidence
  -> DownstreamInterpretationAdmission
  -> BoundedOperatorGoalEstablishment
```

Important gates are real: warranted does not mean selected; unique warranted
does not auto-select (`contextual_interpretation_selection.py:14-24`), selected
does not mean applicable (`interpretation_applicability_projection.py:13-20`),
and applicable does not mean admitted (`downstream_interpretation_admission.py:
11-18`). Nothing in the shell slice can manufacture the evidence at those
crossings.

The alternative closed-choice BOGE function establishes only a bound option and
refuses every other binding state (`bounded_operator_goal_establishment.py:
59-107`). That function turns the option's visible label into `intended_outcome`.
It is therefore lawful only when the option producer already warrants that
selecting the option establishes that exact bounded operator goal. A locally
valid token by itself is insufficient.

`BoundedAdvancementHorizon` is downstream of an already established BOGE and
caller-supplied movement/evidence bounds. It owns neither ingress nor initial
choice meaning. It is beyond this slice.

### 2.5 Responses and rendering

The repository has many domain-specific `format_*` functions and read-only
presentation/explanation projections. They render their own already-produced
artifacts. They do not constitute a general response type or response engine.
Notably, the shared explanation renderer rejects every input unless a known
stage-local adapter exists, and currently its generic producer raises
`TypeError` unconditionally (`shared_explanation_rendering_projection.py:
56-60`). Shared bounded composition explicitly does not speak, transport, bind
conversation references, record, or mutate (`shared_explanation_bounded_composition.py:
88-108`).

There is no current artifact that jointly owns operator-visible prose, an enum
presentation, and the pending binding contract. Reusing a diagnostic formatter
would misstate its stage-specific standing. A shell renderer must be new and
narrow, not a universal response engine.

### 2.6 Ledger and projected State

`EventLedger` can append arbitrary event kinds with event, actor, timestamp,
session, causation, and correlation fields (`seed_runtime/events.py:21-61`). A
`Session` model also exists (`seed_runtime/models.py:58-61`). These are storage
capabilities, not an interactive session road.

`StateProjector.apply` recognizes entity, observation, evidence, fact, goal, and
approval events only (`seed_runtime/state.py:1119-1179`). It recognizes no shell
session, utterance, response, presentation, capture, binding attempt, retry, or
supersession event. Closed-choice and interpretation artifacts all expressly
write neither ledger nor State. Consequently:

* there is no shell session identity in connected behavior;
* there is no turn/utterance/response occurrence identity;
* `presentation_ref` is optional caller data, not a witnessed occurrence;
* there is no pending-choice state;
* exact binding exists only when a caller keeps the object and calls the binder;
* neither Event Ledger nor projected State currently supplies the missing link.

## 3. Piece-by-piece adjudication

| Piece | Classification | Exact adjudication for this road |
| --- | --- | --- |
| `PresentedClosedChoiceSet` | **reusable after narrowing** | Reuse as the immutable content snapshot retained by one pending presentation. Require non-empty options, a real `presentation_ref`, and producer standing at the shell boundary; current type permits empty options and caller fiction. Do not treat it alone as proof of display. |
| `ClosedChoiceOption` | **reusable after narrowing** | Token/ref/label/detail are sufficient content fields. The shell producer must warrant token semantics and non-empty operator-visible labels; current validation requires only token/ref. |
| `OperatorSelectionTokenCapture` | **reusable after narrowing** | Reuse for binder input, but construct it only from a real second stdin occurrence. Add occurrence lineage outside or in a narrowed shell wrapper; current capture does not preserve exact response independently from `captured_token`, nor presentation occurrence/fingerprint. |
| `ClosedChoiceSelectionBinding` and binder | **directly reusable** | The pure local membership result, exact-set fingerprint, unsupported/unknown/conflict preservation, and non-authority flags match the slice. It is the one real bridge already implemented. Keep unsupported distinct from semantic refusal. |
| `ExactOperatorMaterial` | **representation-only for slice 1** | Its exact-text/span shape is useful evidence for a later interpretation road, but instantiating interpretation artifacts in this slice suggests semantic work that is prohibited. A smaller shell utterance occurrence should preserve exact line bytes/text without candidates. |
| contextual warrant production | **incompatible with the shell road** | It requires authored candidates and evidence. The first slice has no authority to infer either from arbitrary input. |
| contextual selection | **incompatible with the shell road** | It requires exact candidate-bound selection evidence; enum token membership is not automatically such evidence. |
| applicability projection | **incompatible with the shell road** | It evaluates a supplied purpose/consumer contract after selection. It cannot justify the initial options or binding. |
| downstream admission | **incompatible with the shell road** | It is consumer-local post-applicability admission, not dialogue or rendering. |
| `BoundedOperatorGoalEstablishment` | **reusable after narrowing, but not in slice 1 by default** | The closed-choice consumer may be invoked only for an option whose producer explicitly warrants goal establishment. No current initial option does. Otherwise STOP at the binding result. |
| `BoundedAdvancementHorizon` | **incompatible with slice 1** | It starts after goal establishment and requires caller-supplied movement bounds. Explicit STOP excludes it. |
| candidate request inspection | **consumerless and deletable later relative to shell** | It is connected only to its explicit JSON inspection/routing CLIs. It preserves `raw_text`, but its summary regex candidates are not shell response semantics, presentation occurrences, or goals. Do not route shell input through it. Its independent operational CLI may remain. |
| candidate request tests | **test scaffold** | They prove the explicit inspection flags only, not free-text shell connectivity. |
| closed-choice tests | **test scaffold** | They invent `1`/`2` option meanings and caller refs to exercise the pure binder. Their vocabulary is not product authority. |
| shared explanation rendering/presentation/composition | **representation-only** | These are stage-owned inquiry/explanation projections, not free-form shell response artifacts. Their formatting patterns may inform deterministic implementation style, but their types must not be reused. |
| domain-specific CLI formatters | **representation-only** | Each is lawful for its exact artifact. None is a generic response renderer. |
| positional CLI `message` ingress | **incompatible as currently implemented** | It explicitly refuses free-form text and is reserved for bounded `ask` dispatch. Do not silently change that existing meaning; add an explicit shell entry point. |
| `--candidate-requests TEXT` | **directly reusable only as an independent one-shot inspection** | It is real free-text argument handling but exits after JSON. It is not reusable as shell semantics. |
| Event/Session models and ledger | **representation-only for slice 1** | Generic identity/storage shapes exist, but adding event kinds/projectors is unnecessary and would make an ephemeral interaction cluster history without a consumer. |

No item is preserved merely because a test can instantiate it. The two pieces
that carry the first slice are the closed-choice content snapshot and binder;
both require a new occurrence owner around them.

## 4. Initial enum vocabulary audit

### Finding

**There is no repository-warranted universal initial enum option set.**

The only concrete `1` and `2` sets found are test fixtures:

| Token | Test label/ref | Producer | What it truthfully establishes | Product standing |
| --- | --- | --- | --- | --- |
| `1` | `Show inventory` / `show_inventory` | test helper `choice_set()` | binder membership in a caller-built test set | no initial-shell standing |
| `2` | `Show shape audit` / `show_shape_audit` | same test helper | same | no initial-shell standing |
| `1` | `Prove non-transition` / `prove_non_transition` | one test body | token locality across a different test set | no initial-shell standing |
| `2` | `Preserve unknown` / `preserve_unknown` | same test body | token locality only | no initial-shell standing |

These fixtures (`tests/test_closed_choice_selection_binding.py:13-23,
71-89`) prove that the string token `1` can mean different things in different
sets. They do not warrant showing those choices to an operator.

Candidate inspection does have stable presentation-like labels for three
summary surfaces, but those are candidates derived only after matching a narrow
input. They are not an initial universal vocabulary, not exact choice options,
and selection is expressly non-authoritative. Turning them into options would
both add a new semantic crossing and violate the STOP before free-text
interpretation.

### Required producer contract before any concrete option is lawful

For **every** option a bounded producer must provide:

1. exact token (string grammar; numeric tokens are optional, not privileged);
2. non-empty operator-visible label and optional deterministic detail;
3. stable option ref naming Seed-known meaning;
4. producer ref and evidence/provenance for that meaning;
5. exact statement of what selection establishes;
6. preserved Unknowns and conflicts;
7. exact next response kind (`bounded_result`, `retry`, or `refusal`); and
8. whether BOGE is authorized by this selection (default false).

Numeric token grammar answers only “which local option matched.” It supplies no
semantic meaning. `"1"` must never acquire global meaning, and whitespace,
case-folding, integer parsing, aliases, or prefixes must not be introduced
silently. For the first slice the captured line is compared exactly as a string.

Because no current producer meets this contract, the exact audit row for every
proposed universal initial option is: **none proposed; no token, label, meaning,
producer, establishment, or next result is warranted.**

## 5. Minimum occurrence topology

### 5.1 Identities

The shell owner needs these distinct identities even though it stops after two
operator inputs:

| Identity | Purpose | Minimum relation |
| --- | --- | --- |
| `shell_session_id` | scopes one invocation | parent of all occurrences; not workspace or projected State identity |
| `operator_utterance_id` | exact first input occurrence | belongs to session; retains exact text and occurrence index 1 |
| `seed_response_id` | first Seed output occurrence | caused by first utterance; owns rendering result |
| `presentation_id` | proves one exact enum was rendered | belongs to response; copied into `PresentedClosedChoiceSet.presentation_ref` |
| `captured_response_id` | exact second input occurrence | belongs to session; explicitly responds to presentation ID |
| `binding_attempt_id` | one invocation/result occurrence | consumes captured response and exact pending fingerprint; may reference binder `binding_id` |
| `retry_response_id` | optional unsupported output | caused by binding attempt; predecessor is first response |
| `retry_presentation_id` | only if policy presents again | predecessor is old presentation; becomes current and supersedes old pending set |

The binder's content-addressed `binding_id` is an artifact identity, not an
occurrence identity: replaying identical inputs can produce the same ID. The
shell therefore needs a separate binding-attempt occurrence ID.

### 5.2 Pending-choice state and currentness

Minimum process-local state:

```text
ShellSessionState
  session_id
  next_occurrence_index
  first_utterance_occurrence
  last_seed_response_occurrence
  pending_choice: null OR
    presentation_occurrence_id
    presented_choice_set (complete immutable snapshot)
    exact_choice_set_fingerprint
    predecessor_presentation_id | null
    status = current
```

Only one pending choice may be current. On capture, atomically consume it before
binding. A successful binding ends the session. For unsupported input, the
smallest first slice renders refusal and ends; it does **not** need retry state.
If one retry is intentionally included, it must create a new response and new
presentation occurrence, link predecessor/supersession, and replace rather than
mutate the pending snapshot. A response may never bind to an already consumed
or superseded presentation.

### 5.3 Ephemeral versus ledger/State

All of the above should be ephemeral in slice 1. Reasons:

* the contract ends after one binding attempt;
* no current projector or operational consumer reads shell occurrences;
* closed-choice binding is already read-only and non-recording;
* persistence would require new event semantics, diagnostic inventory/shape
  coverage, replay/currentness rules, and retention/privacy decisions without
  product need; and
* exact operator text should not silently become cluster truth.

Nothing must enter the Event Ledger or projected State. If later recording is an
explicit product requirement, append occurrence events under a session-scoped
subject and keep `mutates_cluster=false`; do not project utterance findings onto
hosts, services, goals, or other runtime entities. That is explicitly outside
this slice.

## 6. Rendering boundary

The smallest lawful renderer consumes only a narrow shell response artifact and
returns one string. It does not inspect operator text, infer intent, choose
options, establish Demand, or call BOGE.

Minimum response variants:

```text
ChoicePresentationResponse
  response_id, presentation_id, choice_set_fingerprint
  prompt, ordered [{token, label, detail}]

BoundSelectionResponse
  response_id, presentation_id, binding_attempt_id
  bound_option_ref, token, label

UnsupportedSelectionResponse
  response_id, presentation_id, binding_attempt_id
  captured_token, allowed [{token, label}], terminal=true

RefusalResponse
  response_id, reason_code, operator_visible_message, terminal=true
```

Artifact standing and prose are separate:

* the response artifact says what is known and carries lineage;
* deterministic rendering fixes option order, separators, newline, and final
  newline policy;
* prose may say only what the artifact establishes;
* tokens and labels are copied exactly from the producer's choice set;
* unsupported means the exact captured token is absent from that set;
* retry means a new presentation occurrence exists, not that Seed understood the
  unsupported prose;
* refusal means the shell cannot lawfully continue at this bounded contract;
* goal establishment may be rendered only after an explicitly goal-warranting
  option and a successful BOGE handoff.

Do not use the word “invalid” for arbitrary operator text. `unsupported for this
exact presentation` is the precise standing. Do not normalize or echo a derived
meaning. Exact text may be retained internally; echoing it is a separate,
intentional presentation decision.

## 7. Smallest executable shell topology

### 7.1 Components

```text
explicit CLI mode: seed shell --choice-producer <one registered bounded producer>
  -> LineReader.read_exact_line()
  -> ShellOccurrenceOwner.open_session()/record_utterance()
  -> producer.produce(exact_text)
       NOTE: slice 1 producer must be bounded and already warranted;
             the shell itself performs no interpretation
  -> if no set: RefusalResponse -> renderer -> stdout -> STOP
  -> validate/narrow PresentedClosedChoiceSet
  -> occurrence owner records response + presentation and sets pending
  -> ShellResponseRenderer.render(choice response) -> stdout
  -> LineReader.read_exact_line()
  -> occurrence owner records captured response against current pending
  -> OperatorSelectionTokenCapture
  -> bind_closed_choice_selection
  -> occurrence owner records binding attempt and consumes pending
  -> result adapter creates bound or unsupported response
  -> renderer -> stdout
  -> STOP
```

“Registered” above must not become a plugin framework. For the first slice it
means one direct constructor dependency or one explicit function argument. The
CLI must not advertise a producer until the repository owns one.

### 7.2 Proposed implementation files (not changed here)

The smallest future patch should touch only:

* new `seed_runtime/interactive_shell.py`: occurrence records, one pending-set
  state, two-read controller, response variants, deterministic renderer;
* `scripts/seed_local.py`: one explicit `shell`/`--interactive-shell` dispatch,
  only after a concrete producer exists;
* `tests/test_interactive_shell.py`: scripted reader/writer integration tests;
* `seed_runtime/diagnostic_inventory.py` and
  `seed_runtime/diagnostic_shape_audit.py`, plus their tests, **if** the new CLI
  is classified as an operational surface by repository policy.

Do not change the binder unless narrowing validation cannot live at the shell
boundary. Do not add a conversation package, persistence schema, codec, or
interpretation adapter.

### 7.3 Implementation-ready first slice

The smallest mergeable slice before a product enum is selected is an internal
controller/API whose constructor requires one explicit bounded choice producer.
Its tests use a named fake producer solely to verify wiring; production CLI
dispatch remains absent or deterministically refuses `no_warranted_choice_set`.
This delivers real line I/O and binding connectivity without laundering fixture
vocabulary into product semantics.

The next minimal product decision is not “which numbers?” It is “which existing
bounded responsibility owns the first response, and what exact option meanings
can that owner warrant for arbitrary initial text?” Until answered, a successful
universal CLI demonstration is a STOP condition, not an invitation to invent.

## 8. Expected CLI/API behavior and deterministic examples

### 8.1 No warranted producer (the only truthful universal behavior now)

Hypothetical explicit CLI:

```console
$ seed shell
hello, exactly as typed
Seed cannot present a warranted bounded choice for this input.
```

Properties: the line is preserved exactly in ephemeral session state; no
candidate inspection, Demand, Gap, BOGE, ledger write, or second read occurs;
exit is successful refusal (recommended exit `0`) and the controller stops.

### 8.2 Contract example with an application-owned producer

The following labels are placeholders supplied by a test/application producer,
**not proposed Seed vocabulary**:

```console
Operator input: <exact first line>
Seed output:
Choose one bounded result.
[alpha] Alpha bounded result
[beta] Beta bounded result

Operator input: alpha
Seed output:
Selected [alpha] Alpha bounded result.
```

The corresponding API result has `binding_state="bound"`, the exact
presentation fingerprint, the capture occurrence ref, and
`bound_option_ref="fixture:alpha"`. The shell does not claim a goal.

Unsupported example against that exact same placeholder presentation:

```console
Operator input: something else
Seed output:
Unsupported for this presentation: something else
Allowed responses:
[alpha] Alpha bounded result
[beta] Beta bounded result
Seed stopped without selecting an option.
```

There is no normalization: ` Alpha`, `ALPHA`, and `alpha ` are unsupported when
the exact token is `alpha`. EOF before the first input returns a terminal
`input_closed` result without presentation. EOF after presentation returns a
terminal `response_not_captured` refusal and consumes/supersedes pending state.

### 8.3 Optional one-retry extension (not required in slice 1)

If product explicitly chooses retry instead of terminal unsupported refusal,
the output may repeat the same content, but must have new response and
presentation IDs. The old presentation becomes superseded and cannot accept a
later capture. Exactly one retry may be allowed, then STOP. Generic dialogue
management is prohibited.

## 9. Required tests

### Successful binding integration test

Use an in-memory scripted reader with exactly two lines and a named fake bounded
producer. Assert:

1. the first line is retained byte-for-byte/text-for-text in utterance occurrence;
2. one response and one presentation occurrence are created;
3. stdout exactly matches prompt plus ordered token/label lines;
4. pending state stores the exact presented object and fingerprint;
5. second input becomes a separate captured-response occurrence explicitly
   bound to that presentation;
6. the real `bind_closed_choice_selection` function returns `bound` and the
   expected option ref/label;
7. result output is exact and deterministic;
8. pending state is consumed and controller stops after two reads;
9. no BOGE/horizon/interpretation/authorization/execution function is called;
10. no ledger event or State mutation occurs.

### Unsupported binding integration test

Use the same exact presentation and a second line not equal to any token. Assert:

1. first and second inputs remain distinct exact occurrences;
2. binder result is `unsupported`, not “uninterpretable” or “invalid”;
3. unsupported evidence contains the exact captured token;
4. output repeats only the exact allowed tokens/labels from the bound
   presentation and says Seed stopped;
5. no bound option, BOGE, Demand, retry presentation, or semantic candidate is
   produced;
6. pending state is consumed and no third read occurs;
7. no event or projected State write occurs.

Additional unit checks should cover mismatched set ref refusal, empty choice-set
producer refusal, duplicate-token validation inherited from the binder, exact
whitespace/case behavior, EOF at each read, and content-addressed artifact ID
versus unique occurrence ID.

When the CLI surface is actually added, add an end-to-end subprocess/stdin test,
inventory and shape-audit coverage required by `AGENTS.md`, and run:

```text
pytest -q tests/test_interactive_shell.py \
  tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

## 10. Explicit STOP conditions

The controller must STOP immediately when any of these is true:

* stdin closes before initial input;
* no explicit bounded producer is configured;
* the producer returns no warranted non-empty choice set;
* option tokens are duplicate, empty, or otherwise fail set validation;
* presentation rendering fails before the set is marked current;
* stdin closes after presentation without a response;
* capture references no current presentation, a different set, or a superseded
  presentation;
* binding is unsupported, unknown, or conflict (terminal in slice 1);
* binding succeeds and the bounded result is rendered;
* a third operator read would be required;
* continuing would require semantic free-text interpretation;
* continuing would establish Demand, Gap, competency, probe, common grammar,
  BOGE without exact option warrant, horizon, authorization, or execution;
* continuing would require generic dialogue management, LLM use, persistence,
  a universal conversation schema, codec, plugin, or new constitutional grammar.

The successful binding is itself the end of the first slice. It is not implicit
permission to establish a goal. Unsupported input is only failed membership in
one exact presentation, not evidence of operator intent, inability, missing
common grammar, or a need to learn.

## 11. Exact files inspected and report LOC

### Repository instruction and packaging/entry points

* `AGENTS.md`
* `pyproject.toml`
* `scripts/seed_local.py`

### Closed choice, interpretation, goal, and horizon

* `seed_runtime/closed_choice_selection_binding.py`
* `seed_runtime/contextual_interpretation_warrant_set.py`
* `seed_runtime/contextual_interpretation_selection.py`
* `seed_runtime/interpretation_applicability_projection.py`
* `seed_runtime/downstream_interpretation_admission.py`
* `seed_runtime/bounded_operator_goal_establishment.py`
* `seed_runtime/bounded_advancement_horizon.py`
* `seed_runtime/__init__.py`

### Ingress, rendering, occurrences, ledger, and State

* `seed_runtime/candidate_requests.py`
* `seed_runtime/shared_explanation_rendering_projection.py`
* `seed_runtime/shared_explanation_presentation_admission.py`
* `seed_runtime/shared_explanation_encounter_sequencing.py`
* `seed_runtime/shared_explanation_bounded_composition.py`
* `seed_runtime/events.py`
* `seed_runtime/models.py`
* `seed_runtime/state.py`

### Tests inspected as scaffold evidence only

* `tests/test_closed_choice_selection_binding.py`
* `tests/test_bounded_operator_goal_establishment.py`
* `tests/test_bounded_advancement_horizon.py`
* `tests/test_contextual_interpretation_warrant_set.py`
* `tests/test_interpretation_applicability_projection.py`
* `tests/test_candidate_requests.py`
* `tests/test_question_surface_inventory.py`
* `tests/test_self_model_alignment.py`

### Prior context inspected but not edited

* `initial_operator_communication_demand_road_fidelity_recovery_001.md` (PR
  2021 report)

This report adds **600 lines** in exactly one new file.
No other file is modified.
