# Initial-Goal Ingress Recurrence Fidelity Recovery 001

## Boundary and governing answer

This is one bounded, report-only Fidelity recovery on current merged `main`
after PR 2005. It cross-examines the implementation, tests, and canonical Book
text. Existing reports supplied search leads and counterevidence only. This
report changes no implementation, test, fixture, schema, export, interface,
event, persistence, projection, canonical Book chapter, root documentation, or
prior report.

**Answer: no.** The current repository has producers that return detailed
artifacts for one initial-goal ingress evaluation. A caller can retain more than
one such artifact in memory. No occurrence-bearing producer on either ingress
road preserves multiple attempts as one bounded series with episode, order or
time, and no producer compares attempts under a declared sameness predicate.
Consequently there is no complete

```text
producer -> recurrence -> material communication-sufficiency consumer
```

road. The smallest exact missing crossing is **from separately returned ingress
artifacts to a bounded recurrence finding**: a responsible comparison act would
need an explicit examined representation, a declared sameness/comparability
predicate, a bounded interaction scope, and distinguishable occurrence
coordinates. Current artifacts do not jointly supply that crossing. This
recovery therefore stops there, before pressure or Demand.

These inequalities control the result:

```text
multiple retained artifacts != recurrence standing
deterministic reconstruction != multiple occurrences
same refusal reason != same failure
same ingress road != same episode
recurrence != explanation
recurrence != pressure
pressure != Demand
Demand != goal
```

## What was cross-examined

The bounded implementation search followed both accepted BOGE ingress types
back through their constructors and producers and forward through every Python
consumer. It separately searched event, state, projection, diagnostic,
recurrence, session, timing, and materiality surfaces. Tests were treated as
executable evidence of contracts and counterexamples, not as runtime storage.

Canonical control is narrow. The Book permits a declared measurement to report
recurrence only while disclosing the examined representation, the equivalence
or sameness rule, and count scope. It separately says repeated bounded failure
to establish sufficient common grammar for an operator interaction *may expose*
pressure. The latter is a counterexample of constitutional possibility, not a
producer, a recurrence predicate, a materiality finding, or an active road.

## Producer inventory

### 1. Operator material and contextual warrant production

`ExactOperatorMaterial` is a frozen input value containing `material_ref`, exact
text, source spans, and optional provenance. Each `SourceSpan` preserves a span
ref, source ref, offsets, and exact text. Neither requires an operator identity,
session/episode, attempt identifier or ordinal, timestamp/currentness, or goal
purpose.

`produce_contextual_interpretation_warrant_set` returns one
`ContextualInterpretationWarrantSet`. Its stable ID is derived from the complete
operator material, candidate warrants, optional closed-choice binding ref, and
convention. Candidate warrants preserve candidate/source-span identity,
retrospective and clarification evidence, standing, Unknowns, conflicts,
residual material, and candidate-local known loss.

This producer may carry several evidence items, candidates, or source spans,
but those are evidence inside one warrant computation—not multiple initial-goal
ingress attempts. Its optional `closed_choice_selection_binding_ref` is an
uninterpreted attachment; it does not load the binding, relate occurrences, or
prove that operator material and binding belong to one episode. The artifact is
read-only, writes no event ledger, and mutates neither state nor cluster.

### 2. Contextual interpretation selection

`select_contextual_interpretation` consumes one warrant set and zero or more
candidate-bound selection-evidence values. It returns one deterministic
`ContextualInterpretationSelectionResult`, preserving the exact operator
material, warrant-set ID, evidence refs/text/provenance, candidate warrants,
selected and non-selected candidates, residual material, Unknowns, conflicts,
and selection provenance.

Several selection-evidence values can name the same candidate, or can conflict
by naming multiple candidates. That is an evidence-set decision inside one
selection production. It is not a comparison of ingress attempts. A repeated
call with equal inputs reconstructs the same content-derived
`selection_result_id`; the ID therefore cannot distinguish two occurrences of
equal input.

The result explicitly stops before applicability, admission, goal binding,
recording, conversation/state mutation, event-ledger writes, and cluster
mutation. Its `recorded` field is false.

### 3. Applicability and consumer-local admission

`project_interpretation_applicability` evaluates one selection for one exact
`BoundedDownstreamPurpose`. The projection preserves selection result and
candidate identity, consumer and purpose refs/labels, required evidence,
selected-meaning snapshot, provenance, known refusals, Unknowns, and conflicts.
It is a returned, read-only projection, not occurrence storage.

`admit_downstream_interpretation` consumes that exact projection, selection,
and admission evidence scoped to the same selection, projection, candidate,
consumer, and purpose. It returns one `DownstreamInterpretationAdmission` with
a content-derived admission ID, carried projection and selected candidate,
consumer/purpose, evidence, outcome, refusals, Unknowns, conflicts, and
provenance. It expressly stops before consumption, goal establishment,
recording, event-ledger writes, and mutation.

The same interpretation may be admitted independently to several consumers.
That tested case demonstrates consumer locality, not multiple initial-goal
attempts: differing consumer/purpose identities are different admission
boundaries, and no producer declares them comparable or recurrent.

### 4. Closed-choice presentation, capture, and binding

`PresentedClosedChoiceSet` preserves a choice-set ref, exact prompt, ordered
options (token, option ref, label, detail), presentation ref, provenance,
Unknowns, and conflicts. Its fingerprint hashes the set ref, prompt, ordered
options, presentation ref, and convention. Provenance, Unknowns, and conflicts
are not fingerprint coordinates.

`OperatorSelectionTokenCapture` preserves a capture ref, choice-set ref,
captured token, provenance, Unknowns, and conflicts. The type does not require
an operator/source identity, episode/session, ordinal, timestamp, or
currentness. A caller-provided `capture_ref` could encode such facts, but the
implementation neither declares nor validates that interpretation.

`bind_closed_choice_selection` compares one capture only with one presented
set. A mismatched set ref raises instead of returning an occurrence artifact.
For a matched ref it returns one `ClosedChoiceSelectionBinding`, preserving the
set ref/fingerprint, presented prompt/options, capture ref/token, binding
state/reason, bound option or structured unsupported/Unknown/conflict evidence.
The binding ID is deterministic over the fingerprint, capture ref/token,
result, and evidence. Presentation and capture provenance do not survive as
binding fields.

The binding relation is exact but local: token membership in this presented
set. It is not a sameness predicate over attempts. Tests showing that token
`1` has different meaning in different sets are direct counterevidence to
inferring comparability from a shared token. The binding is read-only, writes
no event ledger, and mutates no cluster.

### 5. BoundedOperatorGoalEstablishment producers, including refusal

`establish_bounded_operator_goal_from_closed_choice` consumes one binding. It
returns one BOGE with content-derived goal-establishment ID, exact ingress type
and binding ID, and sorted lineage containing binding ID, choice-set ref,
fingerprint, and capture ref. Bound input establishes the option label/ref.
Unsupported, Unknown, or conflicting bindings all return a refused BOGE with
the shared reason
`closed_choice_selection_does_not_support_bounded_orientation`; their
structured unresolved/Unknown/conflict evidence remains distinguishable.

`establish_bounded_operator_goal_from_admitted_interpretation` consumes one
admission for the exact bounded-goal consumer and purpose. It preserves
admission, applicability, selection, evidence, provenance and source-span refs,
the selected-meaning snapshot, Unknowns, conflicts, unresolved refusals or
residuals, and candidate-local known loss. Identity/consumer mismatch,
non-admission, inapplicability, Unknown/conflicting lineage, or absent selected
identity returns a refused BOGE with the applicable branch reason.

Both producers preserve one evaluated ingress in a returned artifact. Neither
accepts a collection of attempts, previous BOGEs, an episode, or a recurrence
predicate. Their stable IDs describe content, not occurrence. Equal attempts
can collapse to equal IDs; unequal attempts can remain separate without any
relation between them. Refused known scope is empty on both roads. No BOGE
field provides operator, session, attempt ordinal, timestamp/currentness, or a
cross-road comparison class.

## Preservation and consumption topology

| Surface | Returned | Durable record | Reconstructed | Current consumer and purpose |
| --- | --- | --- | --- | --- |
| Operator material / warrant set | yes | no | equal inputs reproduce stable ID | selection chooses at most one warranted meaning |
| Selection result | yes | no | equal inputs reproduce stable ID | applicability evaluates one consumer-purpose contract |
| Applicability projection | yes | no | callable again from inputs | admission evaluates exact consumer-local evidence |
| Admission | yes | no | equal inputs reproduce stable ID | admitted-interpretation BOGE consumes one admission |
| Presented set / capture | caller-created values | no | caller can construct again | binding tests one token against one exact set |
| Closed-choice binding | yes | no | equal inputs reproduce stable ID | closed-choice BOGE consumes one binding |
| Established or refused BOGE | yes | no | equal inputs reproduce stable ID | bounded horizon evaluates one goal; later Demand projections require established goal/horizon |

No producer above invokes the event ledger, state projector, persistence
adapter, or recordable diagnostic boundary. Serialization helpers make a value
representable; they do not record it. Tests retain several artifacts in local
variables and fixtures, but no active consumer enumerates those variables as
occurrences. Thus preservation is caller-lifetime return and deterministic
reconstruction only, never a current durable attempt history.

The immediate downstream BOGE consumer is
`establish_bounded_advancement_horizon`. It evaluates one BOGE and refuses a
non-established goal as `goal_artifact_not_established`. It does not compare
BOGEs or inspect refusal recurrence. Authority, clarification, inquiry, and
operational-realization Demand projections consume an established goal plus an
established horizon; none consumes a refusal series.

## Exact identity matrix

| Required coordinate | Interpretation road | Closed-choice road | Result for recurrence |
| --- | --- | --- | --- |
| Operator/source | exact material and span/source refs; provenance optional, no required operator | presentation/capture provenance exists only upstream and is partly lost; no required operator | insufficient to prove same responsible source |
| Session/interaction episode | absent | absent | decisive absence |
| Attempt identity/order | content-derived artifact refs only; no occurrence ID or ordinal | caller capture ref plus content-derived IDs; no declared attempt semantics or ordinal | unequal values distinguish content, equal calls do not distinguish occurrence |
| Time/currentness | absent throughout | absent throughout | no ordering, freshness, expiry, or same-window finding |
| Choice fingerprint / interpretation lineage | extensive selection/projection/admission lineage and selected snapshot | exact choice-set fingerprint, binding and capture refs | strong per-road lineage, no cross-attempt or cross-road equivalence |
| Consumer/purpose | exact on applicability/admission; exact bounded-goal constants checked | BOGE function supplies goal-establishment purpose implicitly; binding has none | purpose locality exists asymmetrically, not an attempt series |
| Scope | candidate/spans, requirements, consumer/purpose; refused BOGE known scope empty | set/options; bound option scope; refused BOGE known scope empty | local scopes remain distinguishable but no shared recurrence scope |
| Unknown/conflict | candidate, applicability, admission, and BOGE fields | presentation/capture/binding and BOGE fields | preserved per result; never aggregated |
| Known loss | candidate-local and carried into interpretation BOGE | only caller-supplied at BOGE; upstream provenance drops at binding | explicit asymmetric loss prevents silent equivalence |

## Apparent multiple-attempt matches and their actual consumers

1. **Several source spans or retrospective evidence rows.** Their consumer is a
   candidate-local warrant computation. They support, contradict, or leave one
   candidate unresolved; they are not attempts.
2. **Several candidate-selection evidence rows.** Their consumer selects or
   refuses selection inside one result. Multiple candidate refs establish a
   conflict, not recurrence.
3. **The same interpretation admitted to several consumers.** The consumer and
   purpose are intentionally different. Admission is non-transferable, so this
   is counterevidence to one episode-level recurrence class.
4. **The same token in several choice sets.** Binding consumers interpret it
   only within each exact fingerprint. Shared spelling supplies no sameness.
5. **Several returned bindings, admissions, or refused BOGEs held by a caller.**
   No current producer accepts them together. Collection by an external caller
   is not repository-produced recurrence standing.
6. **Repeated invocation with identical inputs.** Stable hashing reconstructs
   the same identifier. It records neither that invocation occurred nor how
   many times.
7. **The shared closed-choice BOGE refusal reason.** Its actual consumer is the
   single-goal horizon refusal. The reason compresses unsupported, Unknown, and
   conflict binding states and therefore cannot establish “same failure.”
8. **Generic event/session, measurement recurrence, or documentation recurrence
   machinery.** Those surfaces have their own inputs and consumers. No adapter
   records ingress artifacts into them, and adjacency in the repository does
   not create an ingress road.

No producer relates multiple ingress attempts without strengthening them,
because no current producer relates multiple ingress attempts at all. The
candidate-local evidence grouping and exact token-to-set binding are real
relations, but their subjects are evidence/candidates or token/set—not attempt
occurrences.

## Sameness, recurrence, and materiality findings

There are exact local predicates: choice-set-ref equality before binding,
token membership in one set, candidate-ref equality, and identity agreement
among selection, applicability, admission evidence, consumer, and purpose.
There is also generic canonical authority for a responsible measurement to
declare an equivalence rule. **There is no declared predicate whose domain is
initial-goal ingress attempts.** In particular, no predicate declares when two
operator materials, captures, bindings, admissions, or refused BOGEs are the
same interaction failure or are comparable occurrences.

No exact consumer uses recurrence solely—or at all—to establish a material
communication-sufficiency finding. Repository searches found no ingress
recurrence producer, communication-sufficiency materiality predicate, output
standing, or consumer. The Book's “repeated bounded failure” example does not
fill these implementation contracts and says only that recurrence may expose
pressure. It does not explain the failures, establish pressure, establish a
Demand, or establish a goal.

## Smallest missing crossing and lawful stop

The roads presently end as follows:

```text
one exact interpretation admission -> one established/refused BOGE -> one horizon evaluation
one exact closed-choice binding     -> one established/refused BOGE -> one horizon evaluation

separately retained artifacts
  -X-> bounded recurrence finding
       -?-> material communication-sufficiency finding
       -?-> pressure
       -?-> Demand
```

The first `-X->`, not pressure or Demand, is the smallest missing crossing. A
lawful crossing would have to identify the responsible comparison act and
preserve at least its examined occurrence representation, declared equality or
comparability rule, bounded episode/scope, count/order treatment, temporal and
source limits, Unknowns/conflicts, and representational loss. This statement is
a characterization of what the canonical recurrence rule requires, **not an
implementation recommendation** and not evidence that every coordinate must be
embedded in every upstream artifact.

Because that crossing is absent, this recovery makes no implementation
recommendation. It does not characterize a hypothetical pressure or Demand
road, select a common grammar, infer an episode from adjacent fields, or promote
report vocabulary into repository knowledge.
