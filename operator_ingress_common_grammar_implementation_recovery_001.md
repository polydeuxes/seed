# Operator-ingress common-grammar implementation recovery 001

## 1. Boundary, method, and governing answer

This is one bounded, report-only implementation recovery at commit `af7758b`,
immediately after PR 2028. It changes no canonical Book, implementation, test,
root documentation, `docs/`, prior report, CLI behavior, event, ledger,
projected State, or runtime wiring. Concrete test fixtures are evidence of type
behavior, not application authority or product meanings.

**Governing answer:** the smallest truthful implementation slice is an
application-owned, fixed two-treatment probe around the existing exact
closed-choice binder. It begins with a new source-attributed ingress occurrence,
produces one immutable semantic set and one distinct presentation occurrence,
captures the response occurrence exactly, uses the binder only for exact-set
membership, and translates the membership result into a probe-specific
semantic result. The affirmative result selects acquisition treatment and then
stops. The negative result selects local-stop treatment and is handed to a
separate, probe-specific stopping consumer. Unsupported material preserves only
exact-set nonmembership and Unknown meaning, intent, and requested treatment;
it may produce at most one separately evidenced retry in the first slice, after
which it stops.

That is an executable communication road, not grammar acquisition, a dialogue
controller, a goal apparatus, or Bounded Operator Goal Establishment (BOGE):

```text
exact operator ingress occurrence
-> application-owned common-grammar probe producer
-> immutable {acquisition treatment, local-stop treatment} semantic set
-> exact presentation occurrence
-> exact response occurrence and token capture
-> exact-set binding
-> probe-specific treatment-selection result
   affirmative -> acquisition treatment selected -> STOP
   negative    -> local-stop treatment selected
               -> separate bounded stopping consumer -> bounded stop
   unsupported -> exact-set nonmembership; meaning/intent/treatment Unknown
               -> optional one fresh retry occurrence, otherwise STOP
```

The slice is truthful because it gives the existing binder one real application
producer and a consumer whose semantics are narrower than goal establishment.
It does not pretend that the initial free-form text has been interpreted.

## 2. Current implementation audit

### 2.1 Free-form ingress, occurrence identity, and source

There is no general operator-ingress occurrence in production. The installed
CLI explicitly rejects leftover free-form `message` material in
`scripts/seed_local.py`; its free-text flags are bounded inspection or probe
surfaces, not initial operator ingress. `CandidateRequestInspection.raw_text`
preserves text for its own inspection, while `ExactOperatorMaterial` can
preserve exact text and source spans when a caller constructs it. Neither owns
an operator interaction, utterance occurrence, source participant, input
channel, ordinal, EOF, or presentation response.

Therefore neither artifact can be silently relabeled as ingress. The missing
`OperatorIngressOccurrence` must preserve, without trimming, tokenizing,
normalizing, case-folding, decoding again, or interpreting:

* one exact captured Python text value (and, if the ingress adapter decodes
  bytes, the decoding identity and loss/Unknowns established by that adapter);
* `ingress_occurrence_id`, `interaction_id`, and occurrence ordinal;
* `source_ref` and `source_kind=operator` as attribution, not proof of identity,
  authority, intent, or receipt;
* the concrete ingress adapter/channel reference and capture provenance; and
* EOF as a distinct capture outcome, never the empty token and never an
  affirmative, negative, unsupported, or refusal response.

“Exact” means exact at the owned text-capture boundary. Claiming original byte
identity is forbidden unless the adapter actually retains bytes. A newline
stripped by `input()` could not truthfully be called preserved source text, so
the eventual adapter must either use a line read that retains the delimiter or
name the post-line-framing value and loss explicitly.

### 2.2 Existing closed-choice artifacts and binder

`seed_runtime/closed_choice_selection_binding.py` supplies:

* frozen `ClosedChoiceOption(token, option_ref, presented_label,
  presented_detail)`;
* frozen `PresentedClosedChoiceSet`, including prompt, options,
  `presentation_ref`, provenance, Unknowns, conflicts, and a deterministic
  fingerprint over its representation;
* `OperatorSelectionTokenCapture`, including capture/set refs, captured token,
  provenance, Unknowns, and conflicts;
* `bind_closed_choice_selection`, which rejects a mismatched `choice_set_ref`,
  performs exact string membership, and distinguishes `bound`, `unsupported`,
  `unknown`, and `conflict`; and
* a read-only result that writes neither the event ledger nor cluster state.

These survive as the local representation and membership mechanism. Exact
matching is already correct: no whitespace normalization, aliases, prefix
matching, integer conversion, label matching, or interpretation is performed.
Unsupported binding correctly says only that the token is not in that exact
set.

They do **not** establish that a set was application-produced or presented.
`presentation_ref` is optional caller material. The fingerprint includes
presentation labels and details but has no separate semantic-set identity,
producer identity, consumer, purpose, selection-effect kind, or occurrence
proof. `OperatorSelectionTokenCapture` references only `choice_set_ref`, not
the exact fingerprint or presentation occurrence. It also has no response
occurrence or replay/currentness standing. The existing types therefore need a
probe-owned occurrence envelope and a narrowed option-semantics seam; caller
construction alone remains insufficient.

### 2.3 The application-owned producer and bounded meanings

No active application producer constructs this probe. Concrete options found
in tests (`Show inventory`, `Show shape audit`, and other fixture labels) are
test-owned and must not survive as product vocabulary. Earlier report proposals
are likewise not production authority.

The missing `produce_operator_ingress_common_grammar_probe` must be the sole
application producer. Its semantic inventory is code-owned, versioned, closed,
non-configurable, and exactly two-member:

| Immutable semantic member | Bounded selection effect | Explicit non-effect |
| --- | --- | --- |
| `treatment:common-grammar-acquisition` | `acquisition_treatment_selected` | no acquisition applicability, provider, method, scope, selection, authority, admission, execution, success, grammar, Demand, or goal established |
| `treatment:local-stop` | `local_stop_treatment_selected` | no refusal inferred; no stop established until the stopping consumer accepts the exact result |

Exact tokens and labels are local encodings selected by this producer, not
constitutional vocabulary. They must be constants rather than caller inputs,
configuration, environment values, or test fixtures. A truthful initial
encoding could be `1` and `2`, with labels that describe the two treatments,
but the implementation decision must freeze the exact strings and version.
Changing a token or label creates a new presentation representation; changing
a meaning or selection effect creates a new semantic-set version.

`probe_semantic_set_id` must be computed from producer/version, exact semantic
member identities, effect kinds, consumer boundaries, and negative authority;
it must not be computed from labels alone. `choice_set_ref` identifies that
immutable set representation. `presentation_occurrence_id` identifies one act
of presenting it. These identities are deliberately distinct: identical
content may be presented twice, but the second presentation is a new
occurrence, not replay of the first.

### 2.4 Token capture, binding, and unsupported standing

The response owner constructs one `OperatorProbeResponseOccurrence` and then
one existing `OperatorSelectionTokenCapture`; callers may not author either for
the production road. The envelope must carry the response occurrence,
interaction, source, attempt, exact presentation occurrence, semantic-set ID,
choice-set fingerprint, exact text token, capture provenance, and EOF outcome.

Before calling the existing binder, the probe binder checks all of:

1. the presentation belongs to the same ingress interaction;
2. the presentation is the current non-superseded attempt;
3. response and token capture identify that exact presentation occurrence;
4. semantic-set identity and choice-set fingerprint equal the presented values;
5. capture source is the expected operator ingress channel;
6. the response occurrence and capture have not already been consumed; and
7. no Unknown or conflict defeats exact occurrence attribution.

Only then does `bind_closed_choice_selection` answer membership. A bound option
is mapped by immutable `option_ref`, never by `bound_option_label`. An
unsupported token yields a probe semantic result with:

```text
membership = exact_set_nonmember
meaning = Unknown
intent = Unknown
requested_treatment = Unknown
acquisition_treatment_selected = false
local_stop_treatment_selected = false
operator_refusal_established = false
```

The unsupported token remains exact attributed source material. It must not be
parsed as a request, compared semantically with labels, or sent into the
contextual interpretation chain inside this slice.

### 2.5 Selection output and separate stopping consumer

The missing `OperatorCommonGrammarProbeSelectionResult` is the semantic output
of the probe consumer. It preserves the ingress, presentation, response,
capture, binding, semantic-set, and attempt lineage. Its result kind is exactly
one of `acquisition_treatment_selected`, `local_stop_treatment_selected`,
`unsupported`, `unknown`, or `conflict`. It contains explicit booleans proving
that acquisition was neither authorized nor begun, BOGE was not entered,
Demand was not established, and no ledger/State/cluster mutation occurred.

Affirmative processing stops at this result:

```text
affirmative token
-> acquisition treatment selected
-> acquisition_authorized=false
-> acquisition_begun=false
-> STOP
```

No placeholder acquisition function is permitted. A later competent consumer
may be added only after applicability, selection, authority, admission, and
stopping for grammar acquisition are separately recovered.

Negative processing requires a second function,
`establish_operator_ingress_local_stop`, in a separate stopping module or
clearly separate stopping-owner type. It accepts only a current, exact
`local_stop_treatment_selected` result and produces
`OperatorIngressBoundedStop` with the interaction and cause lineage. It rejects
affirmative, unsupported, Unknown, conflict, stale, replayed, or mismatched
results. This consumer establishes only the bounded stop of this ingress
interaction. It does not establish general refusal, interpret the original
ingress, or mutate runtime/cluster state.

EOF is also consumed by that stopping owner under a distinct
`operator_input_eof` cause; it is not manufactured as a negative selection.

### 2.6 Retry occurrence and supersession

Retry is optional canonically. The smallest executable policy may choose no
retry, but that would not exercise the requested bounded retry and supersession
boundary. The smallest faithful witnessed policy is therefore **at most one
retry**, fixed by the application and not configurable:

* only a current `unsupported` result is retry-eligible;
* the retry producer creates attempt 2 with a fresh response/presentation
  occurrence and `retry_of_attempt_id` pointing to attempt 1;
* attempt 2 may reuse the same semantic set and representation fingerprint but
  must have a new presentation occurrence;
* producing attempt 2 marks attempt 1 superseded in the new immutable attempt
  aggregate; it does not mutate the old frozen artifact;
* a response tied to attempt 1 is thereafter stale and rejected, even if its
  token is a member of the identical set;
* a second unsupported response, EOF, Unknown/conflict, presentation failure,
  source mismatch, or any retry-construction mismatch stops; and
* affirmative on attempt 2 still stops at treatment selection, while negative
  still requires the separate stopping consumer.

This is not a generic dialogue controller. It is one probe-local aggregate with
two fixed ordinals and no loop, configurable budget, topic routing, semantic
interpretation, or global session state.

### 2.7 BOGE isolation and the unsafe current adapter

The current `establish_bounded_operator_goal_from_closed_choice` adapter treats
every `binding_state == "bound"` with a non-empty option ref as sufficient to
establish BOGE. It places `bound_option_label or bound_option_ref` into
`intended_outcome` and the option ref into `known_scope`. It does not check
producer, semantic-set identity, selection-effect kind, consumer, purpose, or
goal-establishment eligibility. Thus it promotes a presentation label toward
goal meaning and is unsafe for this probe.

Merely hiding the binding inside a wrapper is not a sufficient guarantee: a
caller could pass the underlying bound artifact directly to the public adapter.
The smallest faithful implementation must harden the seam. Closed-choice
options/sets need immutable semantic effect and exact consumer/purpose metadata,
or an equally strong application-produced eligibility artifact. The BOGE
adapter must establish only when that metadata says
`selection_effect_kind=bounded_operator_goal_outcome` and identifies the exact
BOGE consumer and purpose. Missing metadata defaults to ineligible/refused,
not eligible. The communication probe fixes its members to treatment-selection
effect kinds and a probe consumer, so both affirmative and negative bindings
are refused by the BOGE adapter.

This tightening may require migrating existing BOGE test fixtures, but it must
not grant old caller-authored labels retroactive semantic authority. A prefix
check on option refs, a label blacklist, trusting provenance strings, or merely
promising not to call the adapter would be unfaithful.

### 2.8 Events, ledger, State, and runtime boundary

All artifacts in this slice are immutable, returned values held by the direct
caller. They set or serialize:

```text
writes_event_ledger=false
mutates_projected_state=false
mutates_cluster=false
runtime_wiring=false
```

The generic event ledger's capacity to append an arbitrary event is not a
producer mandate. `StateProjector` has no operator ingress, presentation,
capture, probe selection, retry, supersession, or bounded-stop projection.
Adding such events or projections would exceed the slice and falsely turn an
ephemeral diagnostic communication attempt into cluster truth. No CLI flag,
diagnostic inventory entry, record mode, session store, or global bootstrap
state is part of the proposed implementation.

## 3. Artifact adjudication

### 3.1 Exact existing artifacts that survive

| Existing artifact | Disposition | Surviving responsibility |
| --- | --- | --- |
| `ClosedChoiceOption` | reuse after semantic narrowing | local token and presentation representation plus new immutable effect/consumer metadata; labels remain presentation only |
| `PresentedClosedChoiceSet` | reuse inside a probe occurrence envelope | exact closed representation and fingerprint; not proof of production or presentation |
| `OperatorSelectionTokenCapture` | reuse inside response envelope | exact captured token for the exact set; not occurrence/currentness proof |
| `ClosedChoiceSelectionBinding` | directly reuse as membership evidence | exact membership/nonmembership, Unknown/conflict preservation, read-only boundary |
| `bind_closed_choice_selection` | directly reuse after occurrence prechecks | pure exact-token lookup; never semantic interpretation |
| stable hash/frozen dataclass style | reuse as implementation pattern | deterministic content identities and immutable returned artifacts |
| `establish_bounded_operator_goal_from_closed_choice` | retain but narrow eligibility | goal-specific adapter; explicitly refuses probe treatment selections |

`ExactOperatorMaterial`, candidate-request inspection, contextual warrant and
selection, interpretation applicability/admission, advancement horizons,
generic events, State, and existing rendering projections do not participate.

### 3.2 Exact missing artifacts

**Producer and occurrence artifacts**

1. `OperatorIngressOccurrence` — exact text/EOF, source, channel, interaction,
   ordinal, provenance, Unknowns/conflicts.
2. application-owned `produce_operator_ingress_common_grammar_probe` — the
   only producer of the fixed two-member semantic set.
3. `OperatorCommonGrammarProbePresentationOccurrence` — semantic set,
   represented closed set, exact fingerprint, distinct presentation occurrence,
   attempt, producer, ingress, currentness, and rendering evidence.
4. `OperatorProbeResponseOccurrence` — exact response or EOF, source,
   presentation/attempt lineage, and capture provenance.
5. `OperatorCommonGrammarProbeAttempt` — current attempt plus optional prior,
   retry, and supersession relation, bounded to ordinals 1 and 2.

**Semantic result artifacts**

6. narrowed closed-choice semantic effect/consumer metadata.
7. `OperatorCommonGrammarProbeSelectionResult` — treatment-selection or
   unsupported/Unknown/conflict output with all negative-authority flags.

**Consumer artifacts**

8. probe-specific binding-to-treatment consumer — maps only immutable option
   identity, not label, to the result.
9. `OperatorIngressBoundedStop` and
   `establish_operator_ingress_local_stop` — separate competent stopping
   consumer for negative selection and EOF.
10. hardened BOGE closed-choice eligibility check — refuses this probe even
    when its token bound.

No acquisition producer or consumer is missing *inside this slice*: it is
intentionally absent and is a mandatory stop.

## 4. Smallest executable vertical slice

The implementation should be pure application-library code first, without CLI
or runtime wiring:

1. capture one exact ingress occurrence from explicit adapter-owned values;
2. invoke the fixed application probe producer;
3. produce/render one exact presentation occurrence through a narrow
   deterministic renderer that accepts no caller-authored options;
4. capture one exact response occurrence (or EOF) against that occurrence;
5. validate interaction, source, set, fingerprint, occurrence, currentness,
   replay, Unknowns, and conflicts;
6. call the existing binder;
7. map binding by immutable option identity to the semantic result;
8. for affirmative, return `acquisition_treatment_selected` and stop;
9. for negative, call the separate stopping consumer and return bounded stop;
10. for first unsupported, either stop or create the fixed second attempt; for
    the witnessed one-retry policy, supersede attempt 1 and repeat steps 3–9;
11. on second unsupported or every non-eligible condition, stop; and
12. independently prove the BOGE adapter refuses either probe option.

“Render” here may return deterministic lines plus the occurrence artifact; it
must not claim transport, delivery, receipt, or shared grammar. Real stdin and
stdout remain unwired until a later task explicitly changes CLI/runtime
behavior.

## 5. Exact stop conditions

The slice stops without acquisition, BOGE, Demand, event, ledger, or State work
when any of the following holds:

* ingress is EOF, lacks exact capture/source/interaction identity, or carries
  attribution Unknown/conflict;
* the application producer cannot produce exactly the fixed semantic set;
* presentation construction/rendering is Unknown, conflicting, empty,
  mismatched, or not tied to the ingress and current attempt;
* response is EOF (after the stopping consumer establishes the EOF-local stop);
* source/channel, interaction, presentation occurrence, semantic set,
  fingerprint, choice-set ref, or attempt identity mismatches;
* response/capture/result is replayed, already consumed, stale, or superseded;
* binder returns `unknown` or `conflict`;
* binder returns `unsupported` and retry is disabled, ineligible, malformed, or
  already used;
* the bounded second attempt returns `unsupported`;
* affirmative selects acquisition treatment (mandatory STOP because no later
  competent acquisition consumer exists);
* negative is rejected by the stopping consumer; or
* any code attempts to route the binding/result into BOGE.

A successfully consumed negative result ends in `OperatorIngressBoundedStop`.
That is a completed local stopping outcome, not continuation into another
consumer.

## 6. Required asymmetric tests

Tests must use the application producer, never test-owned options or
caller-authored meanings.

1. **Affirmative:** exact affirmative token binds to the current presentation;
   result is `acquisition_treatment_selected`; authorization/begun, BOGE,
   Demand, ledger, State, and cluster flags remain false; no stop is claimed;
   BOGE adapter refuses the same bound artifact.
2. **Negative:** exact negative token yields only
   `local_stop_treatment_selected`; before consumption, stop is false; the
   separate stopping consumer then establishes one bounded interaction stop;
   acquisition and BOGE remain false.
3. **Unsupported:** a near match, label, whitespace variant, case variant, and
   arbitrary phrase each yield exact-set nonmembership; meaning, intent, and
   requested treatment are Unknown; none is refusal, negative, acquisition,
   BOGE, Demand, or stop selection.
4. **EOF:** initial EOF creates no text token and stops through the EOF-specific
   stopping cause; response EOF after presentation never binds as `""`, never
   selects negative, and establishes only the bounded EOF stop.
5. **Replayed token:** a previously consumed response/capture/result is rejected
   deterministically; it cannot produce a second result or second stop even
   while its presentation remains current.
6. **Wrong presentation identity:** same token and even byte-identical set
   content tied to a different presentation occurrence is rejected before the
   binder; wrong set ref and wrong fingerprint are independently rejected.
7. **Retry supersession:** first unsupported result creates fresh attempt 2 and
   supersedes attempt 1; a late affirmative tied to attempt 1 is stale and
   rejected; affirmative tied to attempt 2 selects acquisition treatment and
   stops. A second unsupported response cannot create attempt 3.

Additional negative assertions should prove a presentation label cannot be
used as semantic identity, callers cannot configure tokens/effects, an
affirmative result cannot enter the stop consumer, an unsupported result cannot
enter either treatment consumer, and all JSON projections preserve exact
lineage and false mutation flags.

## 7. Mandatory unimplemented frontier

The following must remain unimplemented until separately recovered:

* any acquisition applicability test, acquisition candidate or provider;
* selection among acquisition methods, resources, scopes, or grammars;
* authority, risk, approval, admission, execution, observation, verification,
  completion, or stopping for acquisition;
* establishment of shared grammar or a communication relationship;
* interpretation of the original ingress or unsupported response;
* re-entry of ingress into contextual warrant, selection, applicability,
  admission, or BOGE;
* Demand evidence comparison, family assignment, admission, establishment, or
  consumption;
* any BOGE from a communication-probe token;
* operator selection as constitutional truth, intent, refusal, or authority;
* a generic dialogue/session/controller framework, configurable semantics,
  adaptive retry policy, global bootstrap state, or BOGE replacement;
* CLI/stdin/stdout wiring, event kinds, ledger recording, projected-State
  entities, persistence, diagnostics, or cluster mutation; and
* any placeholder/fake acquisition implementation, test-only producer, or
  caller-supplied option vocabulary.

When grammar acquisition is later recovered, affirmative selection is only one
input to that later consumer. When sufficient grammar is later established,
the original preserved ingress must re-enter interpretation, warrant,
applicability, admission, and only then possible operator-origin BOGE. Nothing
in this slice short-circuits those gates.

## 8. Verdict, anticipated patch, and size

**Verdict: implementation-ready, but no implementation in this report.** The
canonical two-treatment meaning now supplies the application producer that was
missing before PR 2028, and the existing exact binder is reusable. The slice is
not faithful unless occurrence/currentness/replay boundaries, a separate stop
consumer, and BOGE eligibility hardening ship together. Acquisition, Demand,
interpretation re-entry, CLI wiring, recording, and State remain stopped.

Anticipated files for the smallest faithful implementation:

| File | Anticipated change | LOC range |
| --- | --- | ---: |
| `seed_runtime/operator_ingress_common_grammar_probe.py` | ingress, semantic-set producer, presentation/response/attempt occurrences, binding-to-treatment result, fixed one-retry supersession | 210–290 |
| `seed_runtime/operator_ingress_stopping.py` | separate bounded-stop artifact and consumer, including EOF cause | 55–85 |
| `seed_runtime/closed_choice_selection_binding.py` | immutable semantic effect plus consumer/purpose eligibility metadata and validation | 30–55 |
| `seed_runtime/bounded_operator_goal_establishment.py` | exact goal-eligibility/consumer/purpose refusal gate | 15–30 |
| `seed_runtime/__init__.py` | bounded public exports | 15–30 |
| `tests/test_operator_ingress_common_grammar_probe.py` | affirmative/negative/unsupported/EOF/replay/identity/retry asymmetry | 190–260 |
| `tests/test_bounded_operator_goal_establishment.py` | probe isolation and migrated eligible goal fixture | 25–50 |
| **Total** | **seven anticipated files** | **540–800** |

No CLI, event, ledger, State, Book, root-documentation, or `docs/` file belongs
in that patch. This report file,
`operator_ingress_common_grammar_implementation_recovery_001.md`, is **483 LOC**.
