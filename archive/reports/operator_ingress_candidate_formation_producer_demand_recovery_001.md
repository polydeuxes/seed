# Operator-ingress candidate-formation producer-demand recovery 001

## 1. Governing answer and disposition

This report inspects merged `main` at `d62077d` (PR 2158) and makes no
implementation change. The bounded answer is:

> Exact operator material is available and source-addressable, but no current
> responsibility demands interpretation-candidate formation.

The surviving runtime road ends at a projected, read-only representation of one
exact decoded ingress occurrence. Production search finds no current
`InterpretationCandidate` type, candidate former, candidate-production occurrence,
or operational consumer asking for a candidate. The persistent console causes
ingress capture and projection but neither reads the addressable-material field nor
renders or interprets it. The state projector forms the addressable material only
to expose exact material and provenance in the attempt view. Tests verify that
boundary; tests are not operational consumers.

The canonical Book preserves an *alternative possible* interpretation road and the
responsibilities that would govern it. It expressly assigns neither translation nor
candidate-production ownership, says the road is not compulsory, and says bounded
operator goal establishment does not examine unresolved raw prose. Those clauses
constrain a future producer; they do not instantiate a current producer or create
independent candidate demand.

The disposition is therefore:

```text
no current candidate demand; stop
```

The recovered separation is:

```text
available exact material
!= candidate demanded
!= candidate formed
!= candidate warranted
!= candidate selected
!= interpretation established
```

## 2. Scope, method, and evidence posture

The inspection began with:

* `seed_runtime/operator_ingress.py`;
* `seed_runtime/operator_ingress_addressable_material.py`;
* `scripts/seed_local.py`;
* `tests/test_operator_ingress.py`; and
* `tests/test_operator_ingress_addressable_material.py`.

Production code was searched for `InterpretationCandidate`, `interpretation
candidate`, `candidate formation`, `form candidate`, `proposed meaning`, `meaning
candidate`, `grammar candidate`, `common grammar`,
`addressable_operator_material`, `ExactOperatorMaterial`, and `SourceSpan`.
Canonical Book chapters were examined for operator ingress, representation,
external and constitutional/common grammar, construction and production authority,
consumer-local applicability, interpretation, testimony, and evidence. Historical
reports were used only to navigate the deleted interpretation district and to
cross-check prior topology claims.

The classifications in this report use these evidentiary rules:

* a live producer requires a current responsible production boundary, not merely a
  constructible type;
* a producer occurrence requires evidence that the responsible production act
  happened, not merely a value with the right shape;
* an independent consumer must currently receive/read the output for a bounded
  assertion or responsibility not created merely to consume that output;
* projection availability, deserialization, return to a caller, terminal
  availability, export, a future-facing Book topology, and a test do not by
  themselves establish demand; and
* tests are verification witnesses, while historical reports are testimony.

No untracked or ignored implementation surface is elevated by this report. The
claim is bounded to current tracked repository evidence, not a claim that no future
candidate consumer can exist.

## 3. Canonical boundary recovered

The active Book supplies constraints, not a mandatory pipeline.

### 3.1 Representation and external/common grammar

`book_of_seed/01-grammar-and-standing/external-and-constitutional-grammar.md`
keeps external representation and constitutional standing distinct. An external
grammar, a successful representation, or an interpretation-shaped result cannot
silently become Seed constitutional truth. Applicability and Fidelity remain local
to the crossing and consumer.

`book_of_seed/08-authority-communication-and-stopping/representation-emission-and-consumer-boundaries.md`
separates representation, transport or availability, receipt, adoption, reliance,
and consumer-local use. Thus placing a JSON-safe value in a projected attempt view
does not establish that a candidate consumer received, adopted, or relied on it.

### 3.2 Construction and production authority

`book_of_seed/01-grammar-and-standing/constructors-and-production-authority.md`
separates direct construction and coherent shape from responsible production and
producer occurrence. A caller-constructible value cannot self-certify the act that
would give it standing.

`book_of_seed/03-goals-and-advancement/construction-and-establishment.md`
separates construction from establishment and explicitly keeps interpretation
candidate, candidate-local warrant, selection, purpose-local applicability,
consumer-local admission, and bounded operator goal establishment distinct. It
describes admitted-interpretation and closed-choice roads as different possible
roads, not universal compulsory roads.

### 3.3 Operator-ingress common-grammar prerequisite

`book_of_seed/03-goals-and-advancement/operator-ingress-common-grammar-prerequisite.md`
states that preserved operator ingress cannot presently become available to BOGE
through the required upstream relations, that the exact upstream act and responsible
owner remain **Unknown**, and that no common-grammar prerequisite is assigned to
applicability, admission, or BOGE by proximity. Its display

```text
preserved ingress
-> translated or otherwise bounded source material
-> interpretation candidate
-> candidate-local warrant standing
-> selected interpretation
-> purpose-local applicability
-> consumer-local admission
-> BOGE establishment
```

is expressly a distinction display, not a compulsory universal sequence. The Book
assigns neither exact translation nor candidate-production ownership there. Its
later acquisition language likewise says interpretation candidates *may* become
available and that availability does not interpret, warrant, apply, admit, or
establish ingress by identity.

The guarded first-contact road instead begins with a developer-supplied bounded
potential-goal candidate and meaning for a closed-choice presentation. That candidate
is not formed from preserved operator-ingress material. The representation explicitly
does not interpret the original ingress. This is neither a current general prose
candidate producer nor evidence that exact ingress must enter candidate formation.

### 3.4 Testimony, evidence, and meaning

`book_of_seed/05-evidence-and-knowledge/testimony-and-established-fact.md` keeps
testimony, support, admission, and established fact separate.
`book_of_seed/05-evidence-and-knowledge/evidence-provenance-and-explanation.md`
adds that meaning-assertion carriage is not warrant production: a responsible
meaning-relation occurrence needs claim-appropriate authority, evidence or
constitutive convention, scope, provenance, conflicts, loss, and Unknowns. Exact
text and source lineage can therefore support later examination without providing
a proposition or warrant.

The governing consequence is narrow: canonical text tells a future candidate road
what not to collapse. It does not prove that current runtime responsibility demands
that road.

## 4. Surviving operational road

The complete current road is:

```text
recorded operator ingress
-> ExactOperatorMaterial
-> canonical full SourceSpan
-> OperatorIngressAddressableMaterial
-> projected operator-ingress view
-> current consumers
```

Expanded with responsible boundaries:

```text
capture_stdin_material
-> CapturedOperatorMaterial
-> operator.ingress.raw_material_captured Event
-> operator.ingress.representation_examined Event
-> operator.ingress.ingress_occurred Event
-> form_operator_ingress_addressable_material
-> ExactOperatorMaterial + one canonical full SourceSpan
-> OperatorIngressAddressableMaterial
-> to_json_dict()
-> operator_ingress_attempts[attempt]["addressable_operator_material"]
-> returned/projectable attempt view
```

`run_operator_ingress_attempt` records the raw capture and strict representation
examination. On successful decoding it records `operator.ingress.ingress_occurred`
with exact `decoded_text`, raw/examination lineage, occurrence-only authority, and
meaning Unknown. It then projects state.

`project_operator_ingress_events` is the addressable-material call site. When the
ingress Event contains the required decoded text and lineage and the projector has
a ledger, it calls `form_operator_ingress_addressable_material` and stores its
JSON-safe representation under `addressable_operator_material`.

The former verifies that the supplied occurrence is the recorded ingress Event and
that its raw capture and successful representation examination belong to the same
workspace/session/attempt. It then constructs:

* `ExactOperatorMaterial`, carrying exact decoded text, ingress identity, and the
  ordered three-Event provenance;
* exactly one `SourceSpan`, covering offsets `0..len(exact_text)` and repeating the
  complete exact text; and
* `OperatorIngressAddressableMaterial`, carrying source role, scope, known loss,
  Unknowns, authority limits, and explicit read-only/non-mutating standing.

The artifact authority limits expressly disclaim interpretation candidate, warrant,
selection, applicability, admission, goal, Demand, movement, authorization, and
execution. Decoder success establishes representation availability, not
interpretation or competency.

Replay through `StateProjector` deterministically reconstructs the same projection
from Events. No new addressable-material Event is written. The console ignores the
returned attempt dictionary after calling `run_operator_ingress_attempt`; successful
ingress produces no terminal output.

## 5. Projected addressable-material producer and consumers

| Question | Recovered answer |
| --- | --- |
| Who produces it? | `form_operator_ingress_addressable_material`, invoked by `project_operator_ingress_events` during `StateProjector.project`, produces the frozen artifact and `to_json_dict()` produces its projected representation. |
| Who receives it? | The operator-ingress attempt view receives the JSON-safe value. `run_operator_ingress_attempt` returns that whole view to its caller; general callers of `StateProjector.project` can also obtain it. |
| Who reads it? | In current production, only its own validation/serialization boundary and projection container manipulate it. No downstream production code reads `addressable_operator_material`, `ExactOperatorMaterial`, or `SourceSpan`. The console ignores the returned view. Dedicated tests deserialize and inspect it. |
| What assertion does addressable formation accept? | One supplied Event is the recorded decoded initial-ingress occurrence with matching raw capture, successful decoder examination, lineage, attempt, workspace/session, and occurrence-only/meaning-Unknown authority. |
| What assertion does projection accept? | Given a qualifying recorded ingress Event and ledger, a deterministic exact-material representation may be exposed in that attempt's current view. |
| What assertion does the returned caller accept? | None is evidenced merely by receiving or being able to ignore the view. Availability is the maximum supported standing. |
| Does any consumer require a candidate? | No. Formation asks only whether exact decoded material and provenance can lawfully be made addressable; projection asks only whether it can be exposed. No consumer asks what the material means. |

Tests in `tests/test_operator_ingress.py` verify successful preservation and the
presence of the projected field. Tests in
`tests/test_operator_ingress_addressable_material.py` verify formation, invariants,
authority limits, refusal, JSON reconstruction, and replay. They are verification
witnesses, not operational demand. In particular, test-created `SourceSpan` and
`ExactOperatorMaterial` values are caller-constructible specimens or malformed
fixtures; they do not establish live production of interpretation candidates.

Terminal rendering or availability to a hypothetical caller therefore does not
cross the demand boundary.

## 6. Complete producer and consumer search

| Surface | Producer | Output | Consumer | Production occurrence | Independent demand | Disposition |
| ------- | -------- | ------ | -------- | --------------------- | ------------------ | ----------- |
| stdin capture in `scripts/seed_local.py` | `capture_stdin_material` under persistent-console ownership | `CapturedOperatorMaterial` | `run_operator_ingress_attempt` | live process-local capture | yes, ingress handling | **live producer / live consumer**, unrelated to candidate formation |
| raw/examination/ingress recording | `_capture_representation`, `examine_text_representation`, `_record`, `run_operator_ingress_attempt` | three operator-ingress Events | projector and addressable former | recorded live occurrences | yes, preservation and representation examination | **live producer / live consumer**, meaning Unknown |
| exact addressable-material formation | `form_operator_ingress_addressable_material` | `ExactOperatorMaterial`, canonical `SourceSpan`, enclosing artifact | operator-ingress projector | live deterministic formation during projection, not a new Event | yes, source-addressable view | **live producer / live consumer**, no candidate assertion |
| projected operator-ingress view | `project_operator_ingress_events` / `StateProjector` | JSON-safe `addressable_operator_material` | returned state/view; potentially a programmatic caller | live projection occurrence is reconstructable from source Events but not separately recorded | yes only for current-view availability | **live producer**; no evidenced downstream candidate consumer |
| persistent console return path | `run_operator_ingress_attempt` returns the attempt view | whole attempt dictionary | `run_persistent_operator_console` | call occurs | no output is read or used | caller receives an ignorable value; not candidate demand |
| exact-material deserializer | `OperatorIngressAddressableMaterial.from_json_dict` | reconstructed frozen artifact | current production has no call site; tests use it | no current non-test occurrence evidenced | no independent operational demand beyond available API | **caller-constructible specimen** in current use |
| `SourceSpan` and `ExactOperatorMaterial` direct constructors | arbitrary caller | coherent or malformed value shapes | enclosing validator/tests | no candidate production occurrence follows | no | **caller-constructible specimen**; test fixtures when used in tests |
| dedicated ingress tests | pytest fixtures/helpers | sample Events, material, spans, projected views | assertions | test execution only | verification, not operational demand | **test-only fixture** |
| active Book interpretation topology | no runtime producer assigned | normative distinctions and possible roads | future responsible implementations/readers | none | constrains a future road but does not demand one | canonical constraint, not live producer/consumer |
| deleted interpretation-candidate/warrant/selection district described by prior reports and Git history | formerly caller-constructed specimen and internally connected helpers | candidate/warrant/selection/applicability/admission/horizon shapes | former tests and internal chain | absent from current tree | none current | **historical testimony** |
| `grammar candidate` text in the graded-lessons campaign | campaign report data | an unresolved alternative saying a lesson may be a structural grammar candidate | campaign/report reader | no operator-ingress candidate formation | no | **unrelated candidate vocabulary** |
| other generic candidate vocabulary in production | domain-local producers, if any | selections/proposals for other responsibilities | their domain-local consumers | outside this searched interpretation vocabulary | no operator-ingress meaning demand established | **unrelated candidate vocabulary** |

Repository-wide non-test search finds no current `InterpretationCandidate` symbol and
no candidate-forming function. The only non-test Python occurrence among the exact
search terms outside ingress addressability is a graded-lessons campaign string that
labels an unresolved structural-grammar alternative. It neither consumes operator
ingress nor proposes its meaning.

The deleted district remains visible in history and recovery reports. Its old
coherent types, helpers, exports, and tests do not survive as current producers or
consumers. Even before deletion, prior recovery found caller-authored specimens and
an internally connected chain without an independent entrance. Current deletion
makes that testimony weaker, not stronger, as evidence of current demand.

## 7. Candidate-formation responsibility

No current contract establishes the exact future shape, topology, or field names.
Nevertheless, a truthful producer would have to establish at least the following
responsibilities before its output could have candidate standing:

| Responsibility | What a truthful future boundary must establish | Current evidence |
| --- | --- | --- |
| producer responsibility | The specifically competent boundary responsible for forming a candidate, not merely for preserving text or constructing a dataclass. | No owner exists. |
| producer occurrence | Evidence that this responsible formation boundary actually ran for this candidate. | No occurrence or Event exists. |
| input material identity | Which exact ingress material and preserved occurrence the producer used, without substituting trimmed display content for exact decoded material. | The addressable artifact can supply this input identity. |
| source-span selection | Which portion of that material is attributed to the candidate and who selected it under what method. | Only the owner-created full span exists; no candidate-local selection occurs. |
| candidate identity | A stable identity for the candidate distinct from material, span, proposition, and producer invocation. | Absent; no schema should be invented here. |
| candidate proposition | The bounded proposed meaning, maintained as a proposal rather than truth, intent, goal, or interpretation established. | Absent and communicative meaning remains Unknown. |
| formation method | The declared transformation, grammar, model, rule, convention, testimony, or other method by which source material yielded the proposed meaning. | Absent; decoder selection is not a meaning method. |
| formation provenance | Material/span lineage plus the formation source, method, evidence, and occurrence needed to explain the proposal. | Ingress lineage exists only up to addressability. |
| scope | Material, occurrence, participants, purpose, consumer, temporal/local, and grammar limits within which the proposal is offered. | Ingress scope exists; candidate-local and consumer-local scope do not. |
| known loss | Loss introduced by capture/decoding and by candidate formation or compression, without erasing upstream loss. | Capture loss is carried; formation loss is Unknown because there is no method. |
| Unknowns | Meaning, intent, goal, applicability, conflicts, alternatives, method limits, and unsupported portions that remain undecided. | The addressable artifact preserves core meaning/applicability Unknowns. |
| authority limits | Authority to propose a meaning must remain distinct from authority to warrant, select, apply, admit, establish a goal, authorize, or act. | Addressable authority explicitly forbids all of those strengthenings. Future proposal authority is unassigned. |
| consumer | One identified responsible consumer, its bounded question, required assertion, needed identities/invariants, and permitted reliance. | None found. |
| refusal conditions | Conditions such as absent/foreign/stale material, invalid lineage, unsupported representation, unavailable method, unowned span choice, insufficient authority, scope mismatch, unresolved ambiguity/conflict, or no consumer applicability. | Input-level addressability refusals exist; candidate-local refusals are not specified. |

These are responsibility questions, not a proposed artifact design. They do not imply
one universal candidate type, Event, registry, pipeline, projection, or selector.
A future owner may satisfy some responsibilities without materializing a dedicated
artifact, provided the responsible occurrence and consumer-required standing remain
evidenced.

## 8. Whole-span and partial-span boundary

The current `ExactOperatorMaterial` contains exactly one owner-certified canonical
span over the complete decoded text. Its validator refuses zero, multiple, partial,
overlapping, forged, foreign, or shortened span shapes in the enclosing addressable
artifact. This proves a current full-material addressing convention. It is not a
generic span grammar and does not establish that the complete material applies to
one candidate.

The necessary separations are:

```text
whole material available
!= whole material applicable to one candidate

source substring identifiable
!= source substring selected

substring selected
!= candidate formed
```

A Python caller can calculate substring indices or directly construct a `SourceSpan`
shape, but that does not establish source selection, authority, proposition support,
or producer occurrence. Conversely, the canonical whole span is lawful input to a
future candidate former because it faithfully identifies the entire exact ingress
under preserved limits; lawfulness as input does not show that the future consumer
accepts the whole ingress as the source for one candidate.

Direct answers to the required span questions:

1. **Does any current consumer require a candidate over the complete ingress?** No.
   No current consumer requires any candidate.
2. **Does any current consumer require a candidate over only part of the ingress?**
   No.
3. **Is there a current owner for partial-span formation?** No. The current owner
   forms and certifies only the complete span and refuses partial shapes in its
   artifact.
4. **Is there a current owner for choosing which span supports which proposition?**
   No. No current code forms a proposition from ingress or warrants a span-to-
   proposition relation.
5. **Would a generic source-span selector be independently demanded?** No current
   consumer provides such demand.
6. **Would partial-span machinery be speculative today?** Yes. The relevant future
   consumer, question, method, span semantics, authority, and refusal contract are
   all absent. Whether a particular future candidate consumer needs partial spans
   remains **Unknown**.

Because no consumer exists, the question whether the canonical whole span is
*sufficient for the recovered consumer* has no affirmative consumer-relative answer.
It is sufficient for the current addressability consumer and is lawful candidate-
formation input in principle, but candidate sufficiency remains **Unknown** until a
candidate consumer contract exists.

## 9. Common-grammar boundary

The Operator-Ingress Common-Grammar Prerequisite does not create current candidate-
formation demand.

```text
common grammar not established
!= interpretation candidate required

operator material preserved
!= English selected

operator asks to learn English
!= learning mechanism selected
!= candidate meaning established
```

The canonical clause identifies a bootstrap obstruction and preserves the exact
translation/interpretation owner as Unknown. It offers bounded closed choice as one
possible first-contact response. In that road, the developer-supplied potential-goal
candidate and its attributed meaning precede representation; the representation
does not interpret the original ingress, select English, or establish a goal.
Exact token binding supplies only the local grammar of that one presentation.

Later common-grammar acquisition may make resources or candidates available, but
availability still does not perform interpretation. Acquisition itself follows a
lawfully established bounded grammar-acquisition goal and ordinary movement,
selection, authority, performance, and evidence boundaries; it is not proof that
free-form candidate formation must happen first.

No current responsible consumer asks a bounded semantic question that candidate
formation would answer. The current questions are instead:

* can the captured bytes be examined under the selected decoder mechanism?
* did decoded operator ingress occur with the recorded lineage?
* can the exact decoded material be made canonically source-addressable?
* can that read-only representation be projected reproducibly?

None asks “what proposition might this ingress mean?” BOGE is a canonical
consumer-local boundary for a possible future admitted relation, but no live BOGE
implementation or current upstream interpretation consumer survives after PR 2156.
The Book's possible road is not an operational occurrence.

## 10. Direct answers

1. **Does a current interpretation-candidate producer exist?** No. Search finds no
   current type, helper, function, method, or responsible boundary that forms one.
2. **Does a current producer occurrence exist?** No. No live call, recorded Event,
   projected occurrence, or other evidence establishes candidate formation.
3. **Does a current independent candidate consumer exist?** No.
4. **What exact consumer requirement was found?** None. Current consumers require
   exact ingress preservation, representation examination, verified source
   addressability, deterministic projection, serialization/validation, or view
   availability—not a proposed meaning.
5. **Is `OperatorIngressAddressableMaterial` lawful candidate-formation input?**
   Yes, in the narrow sense that a future authorized producer may receive it without
   strengthening it: it supplies exact text, one canonical full span, identity,
   three-Event provenance, scope, loss, Unknowns, and authority limits. Consumer-
   specific applicability remains Unknown.
6. **Does it itself establish a candidate?** No. Its authority limits expressly say
   it establishes no interpretation candidate, and it contains no proposition,
   method, formation occurrence, or candidate identity.
7. **Is the canonical whole span sufficient for the recovered consumer?** No
   candidate consumer was recovered, so consumer-relative sufficiency is Unknown.
   It is sufficient only for current whole-material addressability and is possible
   lawful input, not proof of candidate applicability.
8. **Is partial-span formation currently demanded?** No.
9. **Is a generic span selector currently demanded?** No.
10. **Is a generic candidate artifact currently demanded?** No. No current consumer
    establishes even a local artifact contract, much less a generic one.
11. **Is a candidate Event currently demanded?** No. No candidate occurrence is
    demanded, and the Book does not require every relation to have a dedicated
    artifact or Event.
12. **Does common-grammar acquisition require candidate formation first?** No such
    universal order is established. The first-contact closed-choice road can establish
    a bounded grammar-acquisition goal from separately warranted developer-supplied
    candidate meaning without interpreting the original prose; later acquisition and
    interpretation remain distinct possible responsibilities.
13. **Does any current code promote caller-authored meaning?** No current
    operator-ingress interpretation code exists. Directly constructing exact-material
    shapes supplies content/coordinates, not meaning. The sole campaign “grammar
    candidate” string is unrelated unresolved report data.
14. **What authority would a future producer need?** Bounded authority and competency
    to propose a candidate meaning from identified exact material/span by a declared
    method for an identified consumer and scope, while preserving provenance, loss,
    conflicts, Unknowns, and refusal. Proposal authority would not include warrant,
    truth, intent, selection, applicability, admission, goal establishment, movement,
    authorization, or execution.
15. **What material Unknowns remain?** Whether any future consumer will demand a
    candidate; its bounded question and assertion; whole- versus partial-span need;
    partial-span and source-to-proposition ownership; candidate identity and
    multiplicity; formation method and competency; meaning grammar; provenance and
    occurrence evidence; consumer-local scope/applicability; authority; conflicts,
    known loss, refusal rules, and whether any dedicated artifact or Event is useful.
16. **Is implementation warranted now?** No. Independent consumer demand and an exact
    bounded requirement are both absent.
17. **What is the smallest lawful next action?** Stop. Preserve exact addressable
    ingress and the Unknowns. Reopen recovery only when one current independent
    consumer asks a bounded semantic question; then recover that consumer's exact
    contract before designing or implementing anything.

## 11. Final disposition and stop boundary

No current candidate demand was found. Exact preservation repaired material
availability and source addressability; it did not silently create an interpretation
pipeline. The current whole span may be passed as bounded input to a future lawful
producer, but neither whole-material applicability nor partial-span need follows.
No generic selector, candidate artifact, Event, registry, projection, or common-
grammar pipeline is warranted.

```text
Exact operator material is available and source-addressable, but no current
responsibility demands interpretation-candidate formation.
```

**Disposition: `no current candidate demand; stop`.**
