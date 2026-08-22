# Potential-goal-standing occurrence testimony fidelity recovery 001

## Recovery boundary

This report answers one question only:

> What presently warrants the presentation-eligibility examiner treating one
> preserved `Event` as testimony that the responsible bounded
> potential-goal-standing examination occurred and produced the carried standing
> result?

The answer is asymmetric. The live producer performs a real, bounded standing
examination and preserves unusually rich material about its inputs and result.
The downstream examiner also has good implementation guards against absence,
foreign records, malformed coordinates, and duplicate records. None of those
guards, however, establishes why the preserved record has standing as testimony
that the responsible act occurred. At that exact crossing, the warrant basis is
presently **Unknown**.

This is a report-only recovery. It does not find that the current witness is
generally defective, and it does not reassess presentation eligibility itself.

## 1. Current live topology

### The responsible act and its input authority

`ApplicationSourceRoleTestimony` is expressly testimony about the application's
attribution of a role, **not** testimony about standing. Its own authority limits
also say that it does not establish its own standing or presentation eligibility
(`seed_runtime/operator_ingress_common_grammar_prerequisite.py:82-104`).
`ApplicationPotentialGoalStandingConvention` is separately described as bounded
authority for examining that testimony and as asserting no role. Its limits deny
constitutional authority by identity and deny any grant of presentation
eligibility (`seed_runtime/operator_ingress_common_grammar_prerequisite.py:107-133`).

The exact responsible occurrence is the invocation of
`_examine_potential_goal_standing(...)`. That function says it performs only the
bounded constitutive act, examines the canonical testimony and convention,
preserves conflict and Unknown outcomes, and computes `standing_result`
(`seed_runtime/operator_ingress_common_grammar_prerequisite.py:317-394`). The live
attempt invokes it with the canonical `ApplicationSourceRoleTestimony` and
`ApplicationPotentialGoalStandingConvention` before invoking presentation
eligibility (`seed_runtime/operator_ingress_common_grammar_prerequisite.py:1767-1787`).

### What the act records

The producer calls `_record(...)` once and returns the resulting `Event` of kind
`operator.ingress.common_grammar.potential_goal_standing_examined`. The payload
contains the standing subject, relation, result and reason; complete serialized
role testimony and constitutive convention; their references; purpose, scope,
provenance, limits, conflicts, Unknowns, and lineage. Its dimensions also label
responsibility, authority, and the assertion that a distinct act was durably
recorded (`seed_runtime/operator_ingress_common_grammar_prerequisite.py:397-450`).

Thus the preserved material is a producer-created record **of** the examination
and carries the finding and its inputs. No separate material in this road is
identified as testimony that this invocation occurred, no responsible producer
identity is related to the occurrence as its testifier, and no convention is
shown as granting this `Event` standing as occurrence testimony. The role
testimony cannot fill that gap because its declared subject is the source's role,
not the later examination occurrence.

### What the consumer actually accepts

`_examine_presentation_eligibility(...)` accepts an `Event`, resolves its `id`
through the same ledger, selects records by kind plus `attempt_ref`, and requires
exactly one matching record (`seed_runtime/operator_ingress_common_grammar_prerequisite.py:453-494`).
It then checks kind, workspace, session, attempt, and selected payload coordinates:
standing subject, relation, result, purpose, scope, role-testimony reference,
constitutive-authority reference, conflicts, and Unknowns
(`seed_runtime/operator_ingress_common_grammar_prerequisite.py:495-533`). Only
after its own purpose declaration and authority checks does it carry the upstream
result, conflicts, and Unknowns into the eligibility examination
(`seed_runtime/operator_ingress_common_grammar_prerequisite.py:583-597`).

The current road is therefore:

```text
ApplicationSourceRoleTestimony
+ ApplicationPotentialGoalStandingConvention
        |
        v
_examine_potential_goal_standing(...)          responsible standing act
        |
        v
Event(kind=...potential_goal_standing_examined) preserved record and carried finding
        |
        | ledger ID resolution + unique kind/attempt selection
        | + routing checks + selected payload equality
        v
accepted as the upstream standing occurrence   unsupported occurrence-testimony crossing
        |
        v
_examine_presentation_eligibility(...)         distinct downstream act
```

The downstream code consumes neither the original live invocation nor an
independently established testimony subject. It consumes a locally shaped,
ledger-resolved `Event` **as if** it were accepted testimony about the invocation,
then consumes the finding carried in that record. This is not re-performance of
the standing act: the consumer does not re-examine the serialized full testimony
and convention. It is also not a finding of presentation eligibility merely
because standing was accepted; the consumer separately examines its purpose and
constitutive convention and records a distinct result
(`seed_runtime/operator_ingress_common_grammar_prerequisite.py:535-680`).

## 2. Standing of each coordinate

“Constitutionally established” below means established for the coordinate's
actual subject, not promoted into occurrence testimony. “Implementation support”
means a useful guard whose larger constitutional force is not established.

| Current condition | Exact role found | Standing in this crossing |
|---|---|---|
| `Event.id` | Durable record identity used to resolve one ledger row and link downstream lineage. | **Implementation support / local representation.** It establishes which stored record is addressed, not the constitutional identity of the responsible act. |
| `Event.kind` | Local classifier used to select and reject records. | **Implementation support / local representation.** Its name reports the claimed act; it does not prove that act occurred. |
| `Event.workspace_id` | Ledger storage partition and consumer boundary. | **Implementation support / local representation.** No repository evidence makes workspace identity responsibility or authority. |
| `Event.session_id` | Routing/correlation guard for the supplied consumer context. | **Implementation support / local representation.** It does not identify the responsible producer or occurrence. |
| `payload.attempt_ref` | Witness-local grouping used for unique-occurrence counting. | **Implementation support / local representation.** The duplicate guard is useful, but attempt equality is not occurrence testimony. |
| `standing_subject` | The source whose bounded potential-goal standing was examined. | **Constitutionally established as the finding's subject** by the producer's exact testimony/convention examination; **unsupported surrogate** if used to warrant that the examination occurred. |
| `standing_relation` | The exact relation permitted by the standing convention and asserted in the finding. | **Constitutionally established as a carried assertion coordinate** when produced by the responsible examination; it is not an occurrence identity. |
| `standing_result` | The result computed by the producer and later carried by the consumer. | **Constitutionally established by the responsible producer act; locally represented in the Event.** The present consumer has no independently established basis for accepting the record as testimony that this computation occurred. |
| `source_role_testimony_ref` | Reference to the evidence used by the standing examination. | **Constitutionally meaningful provenance/evidence reference for the standing act; implementation support in the consumer.** The consumer checks only the reference, not the complete carried testimony, and the referenced testimony expressly does not establish standing or occurrence. |
| `constitutive_authority_ref` | Reference to the bounded authority used by the standing examination. | **Constitutionally meaningful authority reference for the standing act; implementation support in the consumer.** Identity equality alone does not testify that the authority was actually applied. |
| `purpose` | The exact purpose bounding the upstream standing examination. | **Constitutionally meaningful scope-of-act coordinate; implementation support in the consumer.** It is not producer responsibility or occurrence testimony. |
| `scope` | The exact convention scope of the upstream examination. | **Constitutionally meaningful scope-of-act coordinate; implementation support in the consumer.** It must not be enlarged into occurrence identity. |
| `conflicts` | Carried outcome material from the examined role testimony and convention. | **Constitutionally meaningful carried finding material.** The downstream propagation is supported once upstream testimony is accepted; the missing acceptance basis remains prior to it. |
| `unknowns` | Carried outcome material, including a reason when the producer result is Unknown. | **Constitutionally meaningful carried finding material.** Like conflicts, it does not warrant the record that carries it. |
| `lineage` | References supplied to `_record`; on the live standing road it points back to ingress, and the eligibility act points to the standing Event. | **Implementation support / provenance representation.** It records ordering and association, but no checked relation grants it occurrence-testimony standing. |

Two carried fields sharpen the asymmetry even though the consumer does not check
them. `source_role_testimony` and `constitutive_authority` preserve the complete
inputs, which is stronger preservation than their references alone. They could
support review of what the producer says it examined. They still do not make the
same producer-created record warrant itself, and replaying their checks in the
consumer would impermissibly re-perform the upstream act.

Likewise, the dimensions' `responsibility`, `authority`, and `occurrence` strings
are descriptions emitted by `_record`, not checked identity relations to a
responsible occurrence testifier. Their exact standing as testimony is
**Unknown**, not false.

## 3. First unsupported crossing

The first unsupported crossing is precisely between:

```text
one uniquely resolved, correctly classified, correctly routed Event whose payload
has the expected standing coordinates
```

and:

```text
accepted testimony that _examine_potential_goal_standing(...) responsibly occurred
and produced the carried standing_result
```

The gap begins before the consumer interprets `standing_result`. Ledger presence
proves preservation in this implementation; unique kind/attempt selection avoids
ambiguity; workspace/session/attempt checks constrain routing; payload checks
constrain the carried assertion. None identifies the constitutional act by an
established occurrence subject, identifies a responsible testifier for that act,
or supplies an acceptance convention under which the record testifies to that
act. The `dimensions.occurrence` assertion cannot close the gap because it is
inside the record whose standing is at issue.

The durable/replay tests establish exactly their stated implementation
properties. A copied `Event` with the same ID may resolve to the stored row, a
SQLite-reconstructed row remains consumable, foreign or unrecorded material is
refused, and duplicates are refused
(`tests/test_operator_ingress_common_grammar.py:153-204`,
`tests/test_operator_ingress_common_grammar.py:233-269`). Those are valuable
record-integrity and replay findings. They do not prove responsible occurrence.

## 4. Existing lawful precedent

The smallest nearby comparison is the later source-meaning road in the same
module. It provides a **partial precedent**, not a complete answer to occurrence
testimony.

`_warrant_source_meaning_relation(...)` keeps a recovered occurrence, an
application testimony, and a constitutive convention distinct; validates the
testimony's attribution, declaration reference, provenance, purpose, scope,
conflicts, and Unknowns; and validates the convention separately
(`seed_runtime/operator_ingress_common_grammar_prerequisite.py:741-885`). It then
records a separately named meaning-relation warrant carrying the full testimony,
full convention, exact upstream occurrence references, provenance, lineage, and
an explicit warrant-basis description
(`seed_runtime/operator_ingress_common_grammar_prerequisite.py:949-1000`). Tests
preserve those distinctions and the upstream occurrence reference
(`tests/test_operator_ingress_common_grammar.py:731-755`).

The following consumer accepts exactly one recorded
`meaning_relation_warranted` occurrence, requires exact record equality, and
delivers the whole warrant occurrence to the consumer-owned applicability
examination without re-performing the meaning-relation act
(`seed_runtime/operator_ingress_common_grammar_prerequisite.py:1003-1075`). This
is established local precedent for:

* a distinct upstream warrant subject rather than an incidental payload label;
* producer-owned testimony and authority material carried with the warrant;
* one exact recorded occurrence and explicit duplicate/missing refusal;
* durable delivery of a prior finding to a separate consumer without
  re-performance.

It does **not** establish a general rule that any exact `Event`, or even any event
named `...warranted`, testifies to its own responsible occurrence. Its own first
acceptance step still relies on event kind, attempt grouping, and record equality.
Accordingly, no nearby complete precedent was found that establishes occurrence
testimony standing independently of the record being accepted. The comparison
does show that this repository already knows how to distinguish the substantive
testimony and convention that warrant a relation from the durable Event that
carries that warrant.

## 5. Smallest next responsibility

The next honest inch is **not** to repair presentation eligibility and not to
re-perform standing there. It is to recover the presently Unknown acceptance
basis at the producer-to-consumer boundary:

> identify whether existing repository material gives the standing examination
> occurrence an explicit responsible testimony subject and acceptance relation;
> if no such material exists, state that the consumer needs explicit upstream
> occurrence testimony before the carried finding can be accepted.

This recovery does not establish which representation that testimony should
take, and therefore does not prescribe a new Event kind, schema, registry, or
verification mechanism. It also does not promote the standing Event's already
rich payload into self-warrant. The current crossing has strong preservation,
routing, uniqueness, payload, replay, and result-propagation support. Its exact
warrant for moving from preserved record to accepted responsible-occurrence
testimony remains **Unknown**.
