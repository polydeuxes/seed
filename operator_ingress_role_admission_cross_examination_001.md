# Operator-ingress `material_role` admission cross-examination 001

## Boundary and verdict

This is one bounded, report-only Fidelity cross-examination of merged `main` at
`96301aa` (PR 2133). It changes no implementation, test, Book, Event, payload,
projection, State, schema, CLI, persisted representation, output, or name. It
begins at the exact consumer
`form_operator_ingress_addressable_material(ingress_occurrence, ledger)` and
examines the surviving role coordinate independently of its producer and of the
role-keyed projection map.

**Result:** the two role checks are observed application-topology compatibility
checks, but their necessity as admission evidence is **Unknown**. The producer
lawfully records that the application supplied the literal, yet neither code nor
active Book evidence recovers the literal's exact relation, participants,
locality, or an addressable-constructor purpose that needs that relation. Exact
identity and lineage establish the referenced capture/examination provenance;
they do not establish every possible responsibility relation. Conversely, the
unestablished meaning of the role prevents a finding that identity and lineage
make it redundant. Refusal proves the checks exist, not that they are necessary.

The projection disposition is separate: the role-keyed
`representation_examinations` map is a faithful singleton organization in
current production, has no production reader, and appears replaceable by one
exact examination coordinate for the currently declared projection purpose.
That map finding does not dispose of either Event role or constructor check.

The single next lawful slice is stated once, at the end: **add one isolated
adversarial test before disposition**.

## Corpus and method

Implementation witnesses inspected:

* `seed_runtime/operator_ingress_addressable_material.py:289-378`
* `seed_runtime/operator_ingress.py:16-297`
* `seed_runtime/events.py:21-127`
* `seed_runtime/state.py:477-479`
* `tests/test_operator_ingress_addressable_material.py:27-379`
* `tests/test_operator_ingress.py:24-806`

Bounded history inspected with `git log -S` and `git show` covered `8f1718f`,
`c28be17`, `e50b3b0`, `754aae0`, `b085ef9`, `ee30f96`, `4af5fc4`, `3703914`,
and `96301aa`. History witnesses a former two-capture interaction
(`initial_ingress`, `enum_response`) and a current one-value producer. It is not
used as constitutional authority. PR 2133 is testimony only.

Active Book paths were recovered through `book_of_seed/README.md`. Searches of
live non-Markdown code found no production reader of
`representation_examinations`, and found only the producer, projector, and two
constructor role comparisons for `material_role`. Tests are treated only as
implementation witnesses.

## Recovery A — exact constructor predicates

The constructor first validates the supplied ingress occurrence, resolves its
two references through `EventLedger.get`, compares the supplied Event with the
recorded Event, then validates the referenced raw and examination Events. The
grouped `or` expressions have one refusal message each, but each operand is a
separate predicate.

### Table 1 — constructor predicate matrix

| predicate (location) | subject | claim tested | evidence | overlap with other predicates | standing contributed | necessity verdict | Unknowns / what passing does not establish |
|---|---|---|---|---|---|---|---|
| ingress kind, `:294-295` | supplied ingress Event | it is an ingress occurrence kind | `Event.kind` | framing and decoder success correlate on the producer road but test different claims | kind compatibility | necessary for this exact constructor | does not prove recording, decoding, provenance, or operator responsibility |
| ingress framing kind, `:296-297` | ingress payload | framing is `text` or `empty` | `ingress_kind` | decoded text type does not establish framing classification | supported framing compatibility | necessary for artifact's declared ingress boundary | classifier correctness beyond producer testimony |
| decoded text existence/type, `:298-300` | carried material | exact decoded material is a string | `decoded_text` | decoder predicates establish outcome, not carried value/type | exact material carriage input | necessary | equality to decoder's transient output is not independently re-examined |
| attempt reference, `:301,304-307` | ingress occurrence | nonempty bounded attempt coordinate exists | `attempt_ref` | later locality compares all Events to it | scope anchor | necessary for emitted scope and locality checks | whether the role is attempt-relative |
| raw Event reference, `:302,304-307` | ingress occurrence | nonempty raw reference exists | `raw_material_event_id` | lineage repeats it; ledger resolution establishes existence | address for capture testimony | necessary for provenance formation | referenced Event's responsibility until checked |
| examination Event reference, `:303-307` | ingress occurrence | nonempty examination reference exists | `representation_examination_event_id` | lineage repeats it; ledger resolution establishes existence | address for examination testimony | necessary for provenance formation | referenced Event's responsibility until checked |
| ordered ingress lineage, `:308-309` | ingress payload | raw then examination are the asserted immediate lineage | exact two-item list | repeats the two reference fields but adds order and list closure | ordered represented provenance | necessary for emitted ordered provenance | does not prove every application relation or producer occurrence |
| ingress authority warrant, `:310-314` | ingress dimensions | authority remains occurrence-only with meaning Unknown | exact string | artifact authority limits narrow further but do not verify this input declaration | bounded non-semantic admission | necessary for claimed authority boundary | authority producer's independent warrant; role meaning |
| supplied ingress equals recorded ingress, `:315-317` | supplied and ledger Event | exact supplied Event is the ledger-preserved Event at its ID | ledger lookup and model equality | kind/payload checks inspect the same Event but do not establish ledger identity | recorded-occurrence and exact-identity standing | necessary for ledger-backed formation | truth of every payload assertion; responsibility relations |
| raw Event existence, `:318,321` | raw reference | a ledger Event resolves | `ledger.get(raw_ref)` | nonempty reference alone does not establish existence | addressable recorded raw testimony | necessary | kind, locality, role, truth |
| raw Event kind, `:322` | resolved raw Event | it is raw-material capture testimony | `raw.kind` | ingress reference/lineage identifies an Event, not its kind | raw-capture kind compatibility | necessary | capture competence or role standing |
| raw `material_role`, `:323` | raw Event payload | application label equals `initial_ingress` | payload string | no other predicate establishes the label; lineage may establish relevant provenance but not an unspecified role relation | literal topology compatibility only | **necessity Unknown** | relation kind, participants, locality, responsibility, consumer purpose |
| raw workspace/session/attempt, `:320,324` | raw Event | raw testimony is local to ingress scope | Event envelope plus payload attempt | examination independently checks same common tuple | raw locality compatibility | necessary | role locality; producer truth beyond recorded coordinates |
| examination Event existence, `:319,327` | examination reference | a ledger Event resolves | `ledger.get(examination_ref)` | nonempty reference alone does not establish existence | addressable recorded examination testimony | necessary | kind, relation, outcome, locality |
| examination Event kind, `:328` | resolved examination Event | it is representation-examination testimony | `Event.kind` | capture link/outcome do not establish kind | examination-kind compatibility | necessary | lawful examination occurrence by kind alone |
| examination `material_role`, `:329` | examination payload | application label equals `initial_ingress` | payload string | capture identity relates it to raw; neither proves unspecified role | literal topology compatibility only | **necessity Unknown** | whether this is source role, lane, ordinal, or responsibility relation |
| examination capture reference, `:330` | examination and raw Events | examination claims the exact resolved raw Event as capture | `capture_event_id == raw.id` | examination lineage also contains raw in production, but constructor does not check that lineage; ingress lineage alone is not this direct claim | direct represented capture relation | necessary | verified producer occurrence or role agreement |
| `decoder_succeeded`, `:331` | examination outcome | producer reports successful decoding | exact Boolean identity | outcome string is correlated but semantically distinct evidence | success standing | necessary | truth independent of examination testimony |
| `decoder_outcome`, `:332` | examination outcome | particular result is `decoded` | exact string | Boolean success is correlated but not the same coordinate | decoded-result standing | necessary | decoder mechanism fitness or semantic interpretation |
| examination workspace/session/attempt, `:333-338` | examination Event | examination is local to ingress scope | Event envelope plus payload attempt | raw has its own locality check; capture reference relates identity, not all locality | examination locality compatibility | necessary | role locality and responsibility |

Passing all predicates forms consumer-local admissibility for the artifact; it
does not convert all Event assertions into truth. No two predicates above are
called redundant solely because the normal producer correlates them.

## Recovery B — what `material_role` claims

The raw Event carries the field on the **capture Event payload** and also embeds
it in a presentation-like dimensional scope string
(`operator_ingress.py:162-165`). The examination Event carries the same supplied
value on the **examination Event payload** (`:177-208`). The call site supplies
one hard-coded literal (`:231-238`).

The narrow recoverable claim is: **the current application assigned the label
`initial_ingress` to this raw capture and copied that assignment to the
examination made from it**. This is producer testimony about application
topology. Its stronger semantics are Unknown:

1. It is not Event identity; IDs are separate.
2. It is not sufficient provenance; source/capture references and lineage are
   separate.
3. It resembles an ordinal, interaction lane, source role, or compatibility
   token, but code declares no exact relation kind.
4. The subjects carrying it are two Events' payloads, not the captured bytes or
   decoded text as independently typed relational subjects.
5. Possible participants (attempt/material/application road) are not encoded as
   a relation tuple; exact participants are Unknown.
6. The asserted relation is no more exact than “application assigned this
   label.”
7. Evidence is the call-site declaration and copying, not an observation or
   derivation.
8. Locality is Unknown: the raw dimensions separately carry workspace and
   session but omit attempt in that scope string; the payload separately carries
   `attempt_ref`.
9. Application control flow permits the producer to describe its own routing,
   but no recovered authority warrants a stronger responsibility relation.
10. The constructor's exact purpose requiring the distinction is undeclared.
11. Equal labels do not establish a relation between the two Events; the exact
    `capture_event_id` does that representational work.
12. Agreement independently says only that the same token was assigned twice.
13. The role does not unambiguously distinguish what the material is, what
    happened, or why it occupies the road.
14. `initial` may be relative to the bounded attempt or the deleted
    two-material interaction. Current code and Book do not decide: **Unknown**.
15. Reading it as established application responsibility would claim more than
    the evidence warrants.
16. It can remain truthful historical/topology description while its present
    consumer applicability remains Unknown.

Thus the classification is **producer-declared compatibility token / topology
label with Unknown stronger relation standing**, not established identity,
provenance, responsibility, scope, source role, or ordinal position.

## Recovery C — producer and consumer independence

### Table 3 — producer/consumer standing

| surface | responsibility | input | output or claim | scope | authority | current alternatives | current consumer | classification |
|---|---|---|---|---|---|---|---|---|
| raw Event role producer | `run_operator_ingress_attempt` supplies; `_capture_representation` records | no role observation; fixed literal | raw capture is assigned `initial_ingress` | exact Event/attempt envelope; role locality Unknown | application may describe its routing, not establish unspecified responsibility | constructible through private helper; none produced | constructor; scope string | hard-coded producer testimony |
| examination Event role producer | `_capture_representation` copies parameter | raw-side supplied token, not examination result | examination receives same label | exact Event/attempt envelope | copying authority only | constructible; none produced | constructor; projection key | copied topology testimony |
| addressable constructor raw-role consumer | formation boundary | recorded raw payload | requires exact literal | one formation | no declared role-specific purpose recovered | rejects missing/foreign values | refusal/admission only | compatibility check; necessity Unknown |
| addressable constructor examination-role consumer | formation boundary | recorded examination payload | requires exact literal | one formation | no declared role-specific purpose recovered | rejects missing/foreign values | refusal/admission only | compatibility check; necessity Unknown |
| role-keyed projection map | projector | examination Event plus arbitrary key | one entry keyed by supplied role | attempt view | projection-method authority | arbitrary keys are structurally accepted; one produced | no production reader | faithful singleton organization; removable candidate |
| addressable artifact | formation boundary | three exact recorded Events | exact decoded material, addressability, ordered provenance, bounded limits | workspace/session/attempt | addressability/material carriage only | no role variant admitted currently | interpretation-candidate producer reads artifact, not role | stronger read-only consumer artifact |

The producer observes bytes and decoder results, derives IDs and ingress
framing, but **selects neither role nor alternative**: it hard-codes the token.
Alternative strings are mechanically constructible through the private helper
or altered testimony; no active production road emits them. The application
owns the assertion that it assigned the token. That ownership does not itself
warrant a constitutional role relation.

The consumer forms exact source-addressable decoded operator material. Without
the checks it would admit otherwise exact testimony whose application role is
foreign, absent, or unequal. That is the exact excluded risk. Whether such
testimony is inapplicable to operator-ingress addressability is Unknown because
the role's meaning and the consumer's role-dependent purpose are undeclared.
The checks are independent code predicates and confirm the producer topology;
whether they are independently warranted evidence is Unknown.

## Recovery D — adversarial role isolation

The current test at
`tests/test_operator_ingress_addressable_material.py:297-309` changes the raw
Event ID from the original ID to `evt:response` **and** changes its role, while
the ingress `raw_material_event_id`, ingress lineage, and examination
`capture_event_id` remain pointed at the original raw ID. The replacement ledger
therefore has no Event at the referenced raw ID. The constructor refuses at raw
existence before it can inspect the replacement raw role. The test proves that a
missing exactly referenced raw Event is refused. It isolates neither role check
and proves neither role's necessity.

The matrix below is report-only. “Without checks” removes only the two exact
role comparisons; all IDs, kinds, references, locality, outcome, and lineage
remain as specified. Identity means exact referenced ledger identities;
provenance means represented capture relation plus ordered ingress lineage.

### Table 2 — role-isolation matrix

| case | identity | kind | locality | capture relation | ordered lineage | decoder standing | role agreement | current result | result without role checks | constitutional verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| unaltered current road | exact | exact | exact | exact | exact | decoded/success | yes, expected literal | forms | forms | faithful current artifact; role necessity still not proven |
| raw role differs (`response`) | exact | exact | exact | exact | exact | decoded/success | no | refuses raw role | forms | identity/provenance/locality/representation stand; changed-role applicability **Unknown** |
| examination role differs (`response`) | exact | exact | exact | exact | exact | decoded/success | no | refuses examination role | forms | same; examination-role necessity **Unknown** |
| both differ consistently (`response`) | exact | exact | exact | exact | exact | decoded/success | yes, foreign | refuses raw role first | forms | pair remains exact and related by capture/lineage; role/application responsibility **Unknown** |
| both roles absent | exact | exact | exact | exact | exact | decoded/success | both absent, not positive agreement | refuses raw role first | forms | missing role relation standing; whether required is **Unknown** |
| roles differ (`alpha`/`beta`) | exact | exact | exact | exact | exact | decoded/success | no | refuses raw role first | forms | unequal topology testimony; admission faithfulness **Unknown** absent declared purpose |
| role exact but lineage/capture broken | exact IDs may resolve | exact | exact | broken as specified | broken as specified | decoded/success | yes | refuses capture or ingress lineage | still refuses | unfaithful provenance; role cannot cure it |

Cases 1–5 would gain formation if only the role checks disappeared. Their exact
identity, kind, locality, capture relation, ordered provenance, and
representation standing would pass; their role/relation standing would be
foreign, absent, or conflicting. Calling the broader admission faithful or
unfaithful would require the missing declaration of what role claim formation
needs. The answer is **Unknown**, not inferred from current refusal. Case 6
shows role agreement is not a substitute for provenance.

## Recovery E — stronger standing formed

The Events preserve three attributed occurrences. Formation strengthens their
availability into a frozen, consumer-local, read-only artifact with:

* exact source addressability through all three Event references;
* exact decoded text carriage under ingress Event identity;
* a canonical full source-span identity over the entire decoded text;
* ordered provenance `(raw, examination, ingress)`;
* workspace/session/attempt scope;
* the explicit source-role assertion “operator-origin material at the preserved
  ingress boundary”;
* known loss copied from ingress, fixed Unknowns, authority limits, and
  non-mutating/read-only standing.

These additions are implemented at
`operator_ingress_addressable_material.py:342-378`; intrinsic validation at
`:72-145` prevents forged/stale projection or span identities and enforces
ordered provenance and read-only behavior. Formation therefore strengthens the
claim beyond mere Event preservation, but only to exact material carriage and
addressability, not interpretation or responsibility.

Kind, identity, recording equality, references, ordered lineage, direct capture
reference, locality, decoded text, decoder predicates, and authority limit
justify that strengthening. `material_role` is checked but absent from the
result. It is check-and-discard evidence: consumed for compatibility and not
represented in artifact identity, provenance, scope, source role, loss,
Unknowns, or limits.

The artifact's existing source role plus the ingress Event kind/responsibility
provide implementation testimony for operator-origin standing. They do not
prove every possible application responsibility, and `material_role` does not
independently establish one. An exact `response`-role pair could mechanically
form a coherent artifact if the checks were removed; whether it may lawfully
form this specifically named artifact is **Unknown**. Check-and-discard evidence
can be lawful when necessary to admission, but necessity here is not recovered.
Removal could admit testimony whose application responsibility is Unknown;
retention could constitutionalize an unestablished historical label. Neither
risk can be adjudicated from present evidence.

## Recovery F — role-keyed projection map, separately

`project_operator_ingress_events` initializes the map at
`operator_ingress.py:61-78` and writes one entry at `:89-101`. It accepts the
payload string as a key without a recognized-role branch. Current production
creates one representation examination per attempt (`:231-238`); repository
search finds no production read of the map. Tests index and characterize it but
are not consumers or authority.

1. No current production consumer reads it.
2. The active producer cannot create more than one entry per attempt.
3. `event_ids` and `dimensional_standing` already preserve examination Event
   identity, kind, dimensions, and lineage; the recorded Event preserves the
   decoder payload and capture reference. The map adds convenient organization,
   not otherwise-lost production evidence.
4. One exact examination coordinate can preserve all current production
   evidence, provided its declared projection purpose remains the current
   singleton lookup/visibility purpose.
5. The constructor reads the ledger, not the map; the map does not help it.
6. Removing the map does not require removing Event roles.
7. Retaining Event roles does not require retaining the map.
8. They are independently disposable surfaces.
9. Classification: **faithful singleton organization and historical plurality
   residue**, not currently necessary plurality. “Misleading” is not established.
10. The smallest map-only cleanup, if selected later, is replacement with one
    exact `representation_examination` coordinate, not Event/payload cleanup.

This report does not recommend that cleanup now because the mandated single
next action is the prior role-isolation witness.

## Recovery G — mandatory active Book authority

No report, implementation, test, history, comment, or PR description supplies
Book authority.

| Recovered claim | Exact active Book path and clause | Scope supported | What is not inferred |
|---|---|---|---|
| identity does not exhaust responsibility or relation standing | `book_of_seed/01-grammar-and-standing/constitutional-kinds-and-artifact-standing.md`, 01.Standing.E–F; `book_of_seed/05-evidence-and-knowledge/evidence-provenance-and-explanation.md`, 05.Evidence.E | relations need their own participants/roles/warrant; attribution is not responsibility | that role is necessary, absent, or false |
| relations and participant roles require bounded warrant | `book_of_seed/01-grammar-and-standing/constitutional-kinds-and-artifact-standing.md`, 01.Standing.E | relation claim dimensions include participants, roles, evidence, scope, producer, consumer/purpose, authority, limits | one universal serialized relation schema |
| constructor formation must validate evidence needed for stronger standing | `book_of_seed/01-grammar-and-standing/constructors-and-production-authority.md`, Bounded resolution; `book_of_seed/01-grammar-and-standing/lenses-views-and-roads.md`, Bounded resolution | authorized producer validates required identity, provenance, state, warrant; road validates invariants needed for declared purpose | that every current check is required |
| projection compression may omit redundant organization only relative to a declared bounded consumer purpose | `book_of_seed/06-state-and-projection/projection-and-current-state.md`, 06.Projection.B–C | purpose-relative losslessness and rebuildability govern omission | that singleton cardinality alone licenses deletion |
| historical multiplicity does not establish a current role family | `book_of_seed/01-grammar-and-standing/constitutional-kinds-and-artifact-standing.md`, 01.Standing.D; `book_of_seed/06-state-and-projection/ownership-discrepancy-and-residue.md`, Bounded resolution | multiplicity does not establish topology/shared purpose; history may witness residue | that historical roles were unlawful or now prohibited |
| absence of an exact Book-prescribed role taxonomy leaves the exact taxonomy question Unknown | `book_of_seed/05-evidence-and-knowledge/evidence-provenance-and-explanation.md`, 05.Evidence.C; `book_of_seed/01-grammar-and-standing/constitutional-kinds-and-artifact-standing.md`, 01.Standing.F | bounded non-recovery cannot become a global negative; unsupported applicable coordinates may remain Unknown | that the Book prohibits locally warranted roles |
| implementation labels do not acquire constitutional standing by name or recurrence | `book_of_seed/01-grammar-and-standing/constitutional-kinds-and-artifact-standing.md`, 01.Standing.B–C; `book_of_seed/06-state-and-projection/ownership-discrepancy-and-residue.md`, Important distinctions | names, shapes, behavior, and recurrence do not confer standing or authority | that labels have no implementation use |
| Unknown remains valid when applicability or authority is not established | `book_of_seed/01-grammar-and-standing/constitutional-kinds-and-artifact-standing.md`, 01.Standing.E–F; `book_of_seed/05-evidence-and-knowledge/evidence-provenance-and-explanation.md`, 05.Evidence.C | exact relation/applicability may remain bounded Unknown when evidence or authority is insufficient | Typed Unknown production or a negative role finding |
| exact lineage is represented provenance, not verified responsibility | `book_of_seed/05-evidence-and-knowledge/evidence-provenance-and-explanation.md`, 05.Evidence.B, D–E | coherent references support represented lineage while sequence/attribution do not prove responsibility | that lineage is insufficient for the artifact's narrower provenance purpose |
| recorded Events do not establish their asserted occurrence as truth; consumer formation is separate | `book_of_seed/06-state-and-projection/events-facts-and-state.md`, Bounded resolution | recording, projection, and consumer-local standing remain distinct | that recorded testimony is unusable |
| the role-keyed map and constructor checks require separate purpose-relative judgments | `book_of_seed/01-grammar-and-standing/lenses-views-and-roads.md`, Bounded resolution; `book_of_seed/06-state-and-projection/projection-and-current-state.md`, 06.Projection.B | consumer- and purpose-relative road/projection standing | a coupled disposition from shared vocabulary |

Faithful absence finding: **No exact active Book requirement for an
operator-ingress material-role taxonomy was recovered.** This is not a Book
prohibition; locally warranted role standing remains possible.

## Table 4 — independent disposition matrix

| surface | current producer | current consumer | evidence preserved | standing established | standing unestablished | can change independently? | recommended disposition |
|---|---|---|---|---|---|---|---|
| raw Event `material_role` | call site/helper | constructor; scope display | application-supplied token | token assignment | exact role relation/responsibility/locality | yes | retain pending isolated admission evidence |
| examination Event `material_role` | helper copy | constructor; map key | copied token assignment | same token was copied | examination-specific role relation | yes | retain pending isolated admission evidence |
| `initial_ingress` literal | call site | both checks | current topology declaration | only current emitted value | meaning of `initial` and taxonomy | yes | retain; meaning Unknown |
| constructor raw-role check | constructor | formation result/refusal | exact raw token comparison | compatibility with current topology | constitutional necessity | yes | retain pending isolated test and purpose recovery |
| constructor examination-role check | constructor | formation result/refusal | exact examination token comparison | compatibility with current topology | constitutional necessity | yes | retain pending isolated test and purpose recovery |
| role-keyed map | projector | no production reader | convenient examination payload copy | faithful singleton projection | current need for plurality | yes | independently replaceable, but not this next slice |
| `raw_initial_material` label | projector | view/tests | raw capture current standing | raw/captured subject distinction | `initial` applicability | yes | out of implementation scope; no recommendation |
| `preserved_ingress` label | projector | view/tests | decoded ingress projected standing | distinct ingress occurrence | broader preservation semantics excluded here | yes | out of implementation scope; no recommendation |

## PR 2133 correction

Conclusions that stand: raw capture, representation examination, and decoded
ingress are distinct; current production role cardinality is one; historical
cardinality was two; the current role-keyed examination map is singleton in
production; `preserved_ingress` and raw material must not be collapsed; map and
Event cleanup must be bounded separately.

Superseded conclusion: exact Event identity, kind, locality, capture reference,
and ordered lineage do **not**, merely from current producer topology, prove
that `material_role` is redundant. They establish exact represented provenance
and material road coordinates, not every potential responsibility relation.
Role-check necessity is now Unknown, not redundant. PR 2133's map redundancy
finding survives only as a purpose-relative, map-only disposition.

## Direct verdicts

1. **Raw claim:** the application assigned `initial_ingress` to this recorded
   raw capture.
2. **Examination claim:** the application copied that assignment to this
   recorded examination.
3. **Classification:** producer-declared topology/compatibility testimony;
   stronger identity, provenance, responsibility, scope, or relation is Unknown.
4. **Meaning of `initial_ingress`:** not established.
5. **Producer lawfulness:** lawful for reporting its supplied routing token;
   authority for a stronger role relation is Unknown.
6. **Declared constructor purpose requiring role:** none recovered.
7. **Do IDs/lineage establish every possible role claim?** No.
8. **Does role establish otherwise absent responsibility?** No established
   responsibility; whether intended to do so is Unknown.
9. **Does formation strengthen beyond Events?** Yes—exact read-only decoded
   carriage, source addressability, span identity, provenance, scope, and limits.
10. **Is role necessary for that strengthening?** Unknown.
11. **Raw-check excluded risk:** otherwise exact raw testimony with missing or
    foreign application-role token.
12. **Examination-check excluded risk:** otherwise exact examination testimony
    with missing or foreign application-role token.
13. **Existing test isolation:** neither role predicate is isolated.
14. **Exact consistent `response` pair lawful?** Unknown.
15. **Would removal broaden admission?** Yes, to Cases 1–5.
16. **Broader admission verdict:** Unknown.
17. **Are checks independently necessary?** Each is an independent predicate;
    necessity of each is Unknown.
18. **Is agreement meaningful?** It confirms copied token equality only.
19. **Is agreement established by capture identity/lineage?** No; those establish
    another relation, while normal production correlation explains agreement.
20. **Is check-and-discard warranted?** Compatibility behavior is witnessed;
    constitutional admission warrant is Unknown.
21. **Is role-keyed map necessary?** No current production necessity recovered.
22. **Can map be removed independently of Event roles?** Yes.
23. **Can Event roles be removed independently of map?** Mechanically yes, with
    the map separately reshaped; lawful Event removal is not yet warranted.
24. **`raw_initial_material` next-slice scope?** No.
25. **`preserved_ingress` next-slice scope?** No.
26. **PR 2133 standing conclusions:** the three-subject distinction, cardinality
    history/current topology, singleton map, and separate-surface discipline.
27. **PR 2133 superseded conclusion:** role redundancy at constructor admission.
28. **Remaining Unknowns:** exact role kind, participants, relation, locality,
    responsibility, `initial` reference frame, producer authority for stronger
    standing, constructor purpose, each check's necessity, and changed-role
    admission faithfulness.
29. **Cleanup warranted now?** No role/Event/check cleanup. A later map-only
    cleanup has evidence, but must not precede the admission witness selected
    below in this cross-examination's one-next-action discipline.
30. **Single smallest next lawful action:** see the final section.

## Single smallest next lawful action

**Add one isolated adversarial test before disposition.** Construct an otherwise
exact ledger that preserves the original raw Event ID and every reference while
changing only the raw `material_role`; assert the current refusal. This supplies
the missing implementation witness that the existing test does not provide,
without yet adjudicating or changing the role, map, Event, payload, projection,
State, artifact, CLI, persisted representation, or names.
