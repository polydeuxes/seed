# Potential-goal presented-alternative formation Fidelity recovery 001

## 1. Governing formation subject

This report recovers only the live formation boundary for:

```text
G = source:operator-common-grammar-potential-goal:v1
A = common-grammar-acquisition
P = purpose:operator-common-grammar:potential-goal:<current presentation_ref>
```

The narrow relation at issue is:

```text
presented alternative A represents application-owned source G
for the bounded common-grammar presentation identified by P
```

That is narrower than an assertion that the rendered words express all of `G`, that
`G`'s candidate proposition is true, or that the proposition has a warranted meaning
relation. It is also narrower than participation of `A` in an exact presented set.
Formation would establish the application-owned representation relation for this
purpose; it would not establish source meaning, presentation, emission, token binding,
selection, source recovery, or `BoundedOperatorGoalEstablishment`.

The current material gives these exact coordinates:

| Coordinate | Current value or standing |
|---|---|
| source identity | `source:operator-common-grammar-potential-goal:v1` |
| alternative identity | `common-grammar-acquisition` |
| source role | `potential-goal candidate` |
| presentation identity | the live `presentation_ref`, currently `presentation:` plus the ingress Event ID |
| purpose identity | `purpose:operator-common-grammar:potential-goal:<presentation_ref>` |
| representation relation | `presented_alternative_represents_application_owned_source` |
| represented proposition material | `establish richer shared grammar with the operator` |
| rendered label | `common-grammar-acquisition` |
| rendered detail | `Select bounded common-grammar acquisition alternative.` |
| known loss | the rendered label is compressed and does not carry the complete source proposition |
| intended scope | the exact presentation and choice set within this application road |
| declared provenance | `seed_runtime.operator_ingress_common_grammar:alternative-source-lineage:v1` |
| claimed producer | the `alternatives_represented` record's generated representation reference |
| actual responsible producer | **not established** |
| consumer | later source recovery is the first visible consumer of the recorded relation; it is not the formation owner |

Source identity, alternative identity, and the relation between them are three
different coordinates. The option token `1`, the alternative identity, its displayed
label, and the source proposition are also distinct.

## 2. Settled upstream eligibility

The upstream findings through PR 2089 stand and are not reopened here:

```text
ApplicationSourceRoleTestimony
+ ApplicationPotentialGoalStandingConvention
-> responsible bounded potential-goal-standing examination
-> exact G has bounded potential-goal standing
-> live observer-held standing for the immediate caller

live standing result
+ exact ApplicationPresentationPurposeDeclaration for P
+ ApplicationPresentationEligibilityConvention
-> responsible presentation-eligibility examination
-> G is eligible for P
-> exact live eligibility Event returned to the immediate caller
```

Eligibility permits `G` to proceed toward formation examination for `P`. It neither
forms `A` nor proves the relation between `A` and `G`. Recording the eligibility
finding also does not turn it into formation input automatically.

## 3. Book-authorized formation topology

The active Book supplies the following topology independently of the implementation:

```text
exact positive eligibility result for (G, P), responsibly produced and received
+ bounded application-owned material proposing that A represents G
+ exact purpose and scope P
+ claim-appropriate formation authority
+ provenance, limits, known loss, conflicts, and Unknowns
-> formation owner validates the applicable inputs
-> responsible occurrence asserts only (A represents G for P)
-> bounded formation result
-> optional local representation/artifact
-> separate optional recording
-> later, separately warranted exact-set participation
-> later, separately evidenced presentation or emission
```

This follows from the Book's controlling distinctions:

1. A relation is a bounded claim subject with participants, relation assertion,
   evidence, purpose, scope, producer, consumer, authority, occurrence, provenance,
   conflicts, limits, and unresolved coordinates.
2. Construction proves that an artifact can be built, not that its named
   responsibility occurred or that it has the claimed standing.
3. An act consumes its subject and appropriate warrant and conditions. Its artifact
   preserves the assertion but does not prove the act.
4. Recording creates retrievable assertion-bearing material. It does not produce the
   represented upstream occurrence or renew its standing.
5. Formation and emission are distinct. A representation can exist without being
   emitted, presented, received, interpreted, selected, or relied upon.
6. On this closed-choice road the Book expressly separates potential-goal standing,
   eligibility, alternative formation, exact-set participation, binding, source
   recovery, meaning warrant, applicability, admission, and goal establishment.

The Book does not mandate one Event for every internal conditional, a universal
presented-alternative type, or a universal formation convention. A distinct convention
is therefore **not required by form**. What is required is claim-appropriate authority
for this producer and relation. A bounded, attributed application-owned declaration
may provide the constitutive representation material, but its existence does not
warrant itself: the responsible formation boundary must accept and validate it under
applicable authority and preserved limits.

## 4. Current implementation topology

The active live implementation instead runs as follows:

```text
standing_occurrence = _examine_potential_goal_standing(...)

presentation_ref = "presentation:" + ingress.id

_examine_presentation_eligibility(
    standing_occurrence=standing_occurrence,
    presentation_ref=presentation_ref,
    purpose_declaration=application_presentation_purpose(presentation_ref),
    convention=APPLICATION_PRESENTATION_ELIGIBILITY_CONVENTION,
)
    -> resolves and records eligibility
    -> returns eligibility Event
    -> caller does not assign the return

choice_set = common_grammar_choice_set(presentation_ref)
    -> combines application constants OPTIONS with presentation_ref
    -> choice_set already contains option A alongside the other option

produced = _record(... "probe_produced" ...)
    -> records and renders choice-set-shaped probe material

representation_ref = new_id("operator_ingress_representation")

representations = common_grammar_representation_lineages(
    choice_set, representation_ref
)
    -> iterates every choice-set option
    -> indexes ALTERNATIVE_SOURCES by alternative identity
    -> indexes SOURCE_PROPOSITIONS by resulting source identity
    -> directly constructs AlternativeSourceRepresentation rows
    -> each row asserts both representation and exact-set participation

representation_event = _record(... "alternatives_represented" ...)
    -> serializes all rows with asdict
    -> fingerprints and records them
    -> claims responsible-alternative-representation
    -> lineage begins at probe_produced, not eligibility

render_probe(choice_set)
    -> writes token and label to stdout

_record(... "presentation_occurred" ...)
    -> separately records the stdout presentation
```

There is no active `_represent_alternative_source(...)` helper. The relevant helper is
`common_grammar_representation_lineages(...)`, and it produces both rows at once.
`AlternativeSourceRepresentation` is a frozen local representation type, not an
independently evidenced formation occurrence.

## 5. Eligibility-consumption analysis

### Exact answers about the live return

1. **Is the return assigned?** No. The caller invokes
   `_examine_presentation_eligibility(...)` as a bare expression.
2. **Is the result inspected?** No. No `eligibility_result`, reason, conflicts,
   Unknowns, refusal, or Event identity is read before constructing the choice set or
   representation rows.
3. **Is its occurrence ID or assertion supplied to formation?** No. The representation
   helper receives only `choice_set` and a freshly generated representation reference.
4. **Could formation proceed after `unknown`, `conflict`, or `refused`?** Yes, provided
   the eligibility helper returns normally. Its result value cannot affect control
   flow because it is discarded, and every following formation input is derived
   independently from `presentation_ref`, application constants, and a fresh ID.
5. **Do tests establish that counterfactual?** No test drives the full live road with
   a non-eligible eligibility Event and proves that representation follows. Existing
   eligibility tests establish the helper's separate result vocabulary. The live
   chronology test establishes only that eligibility is recorded before probe and
   representation; temporal order is not consumption. The non-consumption conclusion
   is established directly by the caller's data flow.
6. **Is eligibility merely recorded nearby?** Yes. Its Event is durably recorded and
   projected, but it is absent from the probe lineage, formation helper arguments,
   representation rows, and representation Event lineage.

The shared `presentation_ref` does not cure this break. Both roads know the same
presentation identity, but formation neither receives the eligibility standing nor
checks that eligibility was positive for that identity. Likewise, an ingress-derived
lineage for `probe_produced` is not lineage from the eligibility occurrence.

## 6. Representation evidence and authority

### Material that proposes the relation

The exact relation is mechanically derived from bounded application-owned constants:

- `OPTIONS` supplies the alternative identity, token, label, and detail;
- `ALTERNATIVE_SOURCES` attributes alternative `A` to source `G`;
- `SOURCE_PROPOSITIONS` supplies `G`'s role and proposition material;
- the helper supplies the relation vocabulary, representation purpose, provenance,
  scope, limits, and known loss; and
- the exact purpose declaration exists upstream, but is not supplied to the helper.

`ALTERNATIVE_SOURCES[A] == G` is the most direct developer-supplied evidence for the
bounded application-owned representation assertion. The source-role testimony supports
the different claim that `G` is a potential-goal candidate. Positive eligibility
supports the different claim that `G` may be considered for `P`. Neither proves by
itself that `A` represents `G`.

The rendered label and detail are not evidence of source meaning. They are local,
compressed downstream presentation material. The proposition is developer-supplied
candidate material and remains distinct from the rendered words; its presence in a
row does not warrant an `expresses` relation. The later source-meaning road uses its
own testimony and convention, correctly remaining separate from this report.

### Authority standing

The eligibility convention expressly grants no alternative-formation authority. The
purpose declaration proposes an examination and expressly does not form an
alternative. The `alternatives_represented` Event describes its authority as
`representation testimony only; no meaning warrant`, but no formation boundary
validates attributed representation testimony, applicable formation authority, the
positive eligibility result, conflicts, or Unknowns before asserting the relation.

Accordingly, the application constants are bounded constitutive material, but the
current **formation authority remains Unknown**. This does not prove that a special
formation convention is necessary. The Book allows authority to be realized by
another claim-appropriate bounded production arrangement. It proves only that the
current road does not expose the validation and authority that would turn its
developer attribution into a warranted formation occurrence.

## 7. Formation occurrence and responsibility

The responsibility that owns this act is **presented-alternative formation**: the
boundary that accepts exact eligibility for `(G, P)` and bounded representation
material for `(A, G)`, validates authority and limits, and asserts `(A represents G
for P)`. Choice-set construction, common-grammar interaction, probe production, and
recording contain or use that work but do not own it merely by placement.

No current portion directly witnesses that responsible occurrence:

| Current portion | Classification | Reason |
|---|---|---|
| eligibility result resolution | upstream responsible occurrence | Produces eligibility, not formation; its return is then discarded. |
| `common_grammar_choice_set(...)` | downstream preparation and local construction | Combines constants into option-shaped set material without eligibility or formation validation. |
| `AlternativeSourceRepresentation(...)` construction | local representation; unsupported surrogate if treated as occurrence | Builds an assertion-bearing row; constructors do not prove the asserted formation act. |
| constant lookups in `common_grammar_representation_lineages(...)` | implementation support | Mechanically supply identities and attributed content but perform no authority or eligibility examination. |
| relation and participation string fields | local assertions | State conclusions without a validated responsible boundary. |
| `asdict(...)` and representation fingerprint | serialization and integrity support | Preserve row shape and detect later alteration; they do not establish the relation. |
| `_record(... alternatives_represented ...)` | separate recording responsibility | Creates a retrievable record of attributed assertions; its dimensions overclaim a responsible formation occurrence. |
| `render_probe(...)` | rendering and downstream presentation preparation | Compresses options to token and label; it does not form or warrant the relation. |
| stdout write and `presentation_occurred` | separate presentation/emission boundary | Occurs after the asserted formation and establishes neither its evidence nor authority. |
| later source recovery | downstream consumer | Uses the record after binding; it cannot retroactively establish formation. |

Thus neither dataclass construction nor recording establishes formation. The current
producer does **not stand** as a responsible presented-alternative formation producer.
That conclusion is bounded to this relation and does not challenge the settled
standing or eligibility producers.

## 8. Choice-set boundary

Formation is currently collapsed with choice-set construction in two directions.
First, `A` exists as an option in the module-level `OPTIONS` tuple and enters the
returned `PresentedClosedChoiceSet` before any representation relation is formed.
Second, `common_grammar_representation_lineages(...)` can only create the relation by
iterating the already constructed exact choice set, and its row simultaneously states:

```text
presented_alternative_represents_application_owned_source
participates_in_exact_presented_choice_set_for_declared_purpose
```

The relation remains conceptually distinguishable because it has its own explicit
field and source mapping, but the implementation does not produce it independently
before set participation. It therefore asserts exact-set participation in the same
mechanical row rather than leaving participation for a later responsible boundary.
This report does not decide whether that participation assertion stands and does not
repair it.

One comparison with the other row is unavoidable because the shared helper iterates
both options. It applies the same eligibility-free construction pattern to both. That
fact explains the helper topology only; local-stop standing or formation supplies no
authority for the potential-goal row.

## 9. Rendering and recording boundaries

### Rendering

The presented token `1`, label `common-grammar-acquisition`, detail `Select bounded
common-grammar acquisition alternative.`, and rendered probe line are local
representation and downstream presentation material. The label is expressly subject
to known loss: it is compressed and does not carry the complete source proposition.
The detail is carried in the recorded row but is not printed by `render_probe`.

These surfaces neither establish candidate meaning nor adopt an operator goal. They
do not establish operator intent, proposition truth, selection, or the representation
relation merely by resembling the application declaration.

### Recording

The `alternatives_represented` Event is a distinct recording occurrence. Its artifact
contains, for each row:

- alternative and source identities;
- source role and proposition material;
- representation purpose and relation;
- choice-set identity, fingerprint, and presentation identity;
- rendered label and detail;
- asserted exact-set participation;
- source attribution and claimed producer reference;
- authority limits, provenance, scope, known loss, conflicts, and Unknowns.

At Event level it also contains the exact presentation reference, a representation
fingerprint, and lineage from `probe_produced`. It does **not** carry the eligibility
occurrence ID or assertion, the exact purpose-declaration ID, an applicable formation
authority reference, or lineage from eligibility. Those absences matter here because
the claimed formation act needs positive eligibility, purpose, and authority inputs;
they do not imply a general schema-expansion requirement.

The four boundaries are therefore:

```text
formation occurrence: not responsibly witnessed
formation artifact: AlternativeSourceRepresentation row mechanically constructed
recording occurrence: _record(...) appends alternatives_represented
recorded assertion: serialized row and Event dimensions claim the relation and participation
```

## 10. First unsupported crossing

The first unsupported crossing on this exact live road is:

```text
responsibly produced exact live eligibility Event
-> return discarded without inspection
-> choice-set-shaped option material constructed from application constants
-> AlternativeSourceRepresentation asserts A represents G for P
```

Eligibility being earlier in the ledger does not make it consumed. The fresh
representation reference, shared `presentation_ref`, application constant mapping,
and probe lineage do not replace the missing consumer act. Recording then preserves
the unsupported formation assertion; it does not originate its standing.

## 11. Smallest next responsibility

**Wire the exact live eligibility result into one responsible presented-alternative
formation boundary.** That boundary should accept the exact returned Event, require
`eligible` for exact `(G, P)`, validate the bounded application-owned `(A represents
G)` material and applicable formation authority with conflicts, Unknowns, provenance,
scope, limits, and known loss, and produce only the formation relation.

This is one production repair, not a request for a universal framework or necessarily
a new convention or schema. It should stop before exact-set participation. Exact-set
participation, presentation, emission, binding, selection, source recovery, meaning
warrant, admission, and `BoundedOperatorGoalEstablishment` remain later work.

## 12. Final direct answers

1. **What does formation produce?** The bounded relation that alternative
   `common-grammar-acquisition` represents application-owned source
   `source:operator-common-grammar-potential-goal:v1` for the exact presentation
   purpose. It does not produce source meaning or set membership.
2. **Who owns formation?** Presented-alternative formation, not eligibility, choice-set
   construction, probe production, common-grammar containment, or recording.
3. **Exact source identity?**
   `source:operator-common-grammar-potential-goal:v1`.
4. **Exact alternative identity?** `common-grammar-acquisition`.
5. **Exact purpose?**
   `purpose:operator-common-grammar:potential-goal:<current presentation_ref>`, whose
   declared purpose is consideration of the already-standing source for later
   alternative formation in this exact bounded closed-choice presentation.
6. **Does formation consume live eligibility?** No.
7. **What proves non-consumption?** The call return is unassigned; all later inputs are
   independently `presentation_ref`, constants, the constructed choice set, and a
   fresh representation ID; neither formation arguments nor lineage contain the
   eligibility Event.
8. **Can formation follow `unknown`, `conflict`, or `refused`?** Yes whenever the
   eligibility helper returns normally, because its result has no data-flow or branch
   effect. No full-road test establishes that counterfactual; code establishes it.
9. **What supports `A represents G`?** Primarily the application-owned
   `ALTERNATIVE_SOURCES` mapping, coordinated with the option declaration and source
   material. Eligibility supports only consideration for `P`; rendering does not
   support source meaning.
10. **What permits formation?** No currently validated authority is visible.
    Application-owned declaration material could contribute bounded constitutive
    support, but current formation authority remains **Unknown**.
11. **Is a separate formation convention required?** Not by the Book as a universal
    form. Claim-appropriate authority and a responsible validation boundary are
    required; the current road shows neither sufficiently.
12. **What occurrence establishes formation?** The responsible validation and
    assertion of `(A represents G for P)` should establish it. No such current
    occurrence is witnessed.
13. **Which code directly witnesses it?** None. The helper directly witnesses only
    mechanical row construction.
14. **Which code is ancillary?** Choice-set construction is downstream preparation;
    dataclass creation is local representation; `asdict` and fingerprinting are
    serialization/integrity support; `_record` is recording; `render_probe` is
    rendering; stdout and `presentation_occurred` are later presentation.
15. **Is formation collapsed with choice-set construction?** Yes. It consumes an
    already built choice set and constructs relation rows for every option.
16. **Is exact-set participation asserted?** Yes, in the same row. Its responsible
    standing is not recovered here.
17. **Does the current formation producer stand?** No. It does not consume eligibility
    or expose a validated authority-bearing formation occurrence.
18. **First unsupported crossing?** Discarded positive eligibility to unconditional
    option/representation construction from application constants.
19. **Does one exact production repair follow?** Yes: wire the exact live eligibility
    Event into one bounded responsible formation producer that validates the
    application representation material and produces formation alone.
