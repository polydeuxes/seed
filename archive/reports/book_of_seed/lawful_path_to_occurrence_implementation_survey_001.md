# The lawful path to an occurrence: implementation survey 001

## 1. Executive

The question: a warranted occurrence implies an Event — what lawful path leads
there, and what would that mean in implementation?

**Three findings, and the third is the useful one.**

**Occurrence and Event are separate, and recording is optional.** Active law is
explicit, `06.Events:20` — `event recording != required for every
constitutional occurrence` — and `06.Events:10`: "A responsible recording
occurrence may preserve, **as an Event**, attributed testimony that an
occurrence or other claim was asserted; **Event preservation does not establish
the asserted occurrence as true**." So a warranted occurrence does not imply an
Event. An Event is testimony that an occurrence was asserted, produced by a
separate recording occurrence that may not happen at all.

**The loop does not close the way it is usually drawn.** The common sketch ends
`... → Event → projection → new Standing`. `06.Events` denies both of the last
two steps:

```text
projected material != current constitutional standing
current lawful condition != recorded history
```

and `06.Events:10` adds that "current standing is not a constitutional State
object." Projection produces projected material, which a bounded consumer may
use only under its exact subject, evidence, warrant, scope, authority,
confidence, freshness, conflict, expiry, and Unknown limits. Nothing turns
projected material into current Standing by identity.

**An implementation *witness* of the lawful path exists in this repository, it
is dormant, and its constitutional fidelity is not established.** All three
clauses matter. The structure demonstrates dependency lineage rather than
call-order warrant, which is the pattern being looked for. But it compresses
Applicability in a way that conflicts with active law, so it is a candidate to
cross-examine, not a validated implementation. §3.

## 2. What active law supplies, and what it refuses

`06.Events:10` names three distinct responsible occurrences, and no ordering
among them:

```text
responsible recording occurrence    → preserves an Event (attributed
                                      testimony that an occurrence was
                                      asserted)
responsible Fact-producing or       → material with bounded Fact standing
Fact-establishing occurrence
responsible projection occurrence   → consumes bounded recorded material
                                      under declared projection rules,
                                      produces projected material
```

What it refuses is as important. The chapter's non-equivalences include `event
!= explanation`, `event != fact`, `Fact artifact != Fact standing`, `Fact
standing != current constitutional standing`, `replay input != projected
material`, and `constitutional standing != objective reality`.

There is no universal pipeline here, and asking for one is the error this
campaign has been recording. The exact middle varies by act: one act may
require Compare, another Selection, another may consume already-warranted
Standing directly, another Applicability plus Admission. What is universal is
only that the **exact Responsibility owns whatever its local grammar
requires**, per `01.Standing.E.1`.

## 3. An implementation witness exists in the runtime

`seed_runtime/operator_session_standing.py` implements a candidate chain, more
complete than the campaign's recent discussions assumed:

```text
meaning relation
      ↓
determine_goal_applicability()  → ("applicable" | "inapplicable", basis)
      ↓  recorded as
operator.interaction.goal_applicability_established
      ↓  admission must consume a recorded APPLICABLE applicability
goal admission        (validated field-by-field against it)
      ↓  consumption must reference applicability_event_id
goal consumption
      ↓
goal standing
```

The applicability determination is not a boolean. It returns a **named basis** —
eight distinct grounds for inapplicability, and one for the applicable case:

```text
role-not-potential-goal            treatment-kind-mismatch
no-consumer-treatment-relation     consumer-authority-not-established
treatment-disagreement             treatment-conflicted
scope-mismatch                     authority-coordinates-not-established
                                   structural-agreement  (the applicable case)
```

Each stage validates that it consumed the exact upstream event, not merely that
one exists — "goal admission does not consume a recorded applicable
applicability" is an enforced error, and admission is checked field-by-field
against the applicability it claims. Lineage is carried explicitly in payloads
(`"lineage": [applicability["event_id"]]`), and `source_provenance`,
`responsibility`, and `authority_support` are recorded per stage.

**That is provenance for action, and it is built.** Downstream stages are
warranted by what they consumed, not by when they ran — which is the property
worth preserving from this code.

**It is also entirely dormant.** `seed_runtime/operator_interaction_goal.py` is
imported by nothing except its own test file. The live console loop
(`run_persistent_operator_console`) calls only:

```text
project_operator_session_standing
form_operator_presentation
emit_operator_presentation
capture_stdin_material
```

So the repository contains a worked candidate path from meaning relation to
goal standing, with recorded applicability, admission, and consumption — and
does not run it.

### 3.1 Where it conflicts with active law

`01.Lenses:14` gives applicability and admission **four standings each**:

> Available upstream material may be evaluated by a consumer-local
> applicability boundary and remain **applicable, inapplicable, Unknown, or
> conflicting** [...] A separate consumer-local admission boundary may consume
> applicability and admission evidence to produce **admitted, unadmitted,
> Unknown, or conflicting** admission standing.

The implementation produces three of those eight:

```text
active law          implementation
applicable          applicable
inapplicable        inapplicable
Unknown             —
conflicting         —
admitted            admitted
unadmitted          —
Unknown             —
conflicting         —
```

Every non-applicable ground is compressed into `inapplicable`, and two of them
are the wrong standing under that clause:

```text
treatment-conflicted                    reads as conflicting, not inapplicable
consumer-authority-not-established      a required coordinate was not
authority-coordinates-not-established     established — that is Unknown, not
                                          a finding of inapplicability
```

This is the distinction the campaign has spent its whole length recovering:
**failure to establish a coordinate is not a responsible finding of its
absence.** `unresolved != absent`, applied to the applicability boundary
itself. The implementation makes a positive negative finding where active law
provides for recording that the question was not settled.

So the fidelity claim cannot be made. What can be said is that the *shape* —
recorded stages, each validated against the exact upstream event it names — is
sound, and that its Applicability **result vocabulary** is not.

## 4. What the live path does record

The presentation formation event is not thin. Its dimensions carry:

```text
identity              presentation_id
content               what was formed
standing              "formed"
source_provenance     session_standing.as_of_event_id     ← consumed Standing
responsibility        "bounded-presentation-formation"
authority_warrant     "formation occurrence only; establishes no selection,
                       warrant, goal, or response treatment"
scope_locality        scope
occurrence_preservation
```

plus `session_standing_evidence_ids`, `known_loss`, `unknowns`, and
`conflicts`.

That answers most of what a recorded occurrence should explain: which
Responsibility, over what subject, consuming which Standing and Evidence, under
what Authority and Scope, with what Unknowns surviving.

**One coordinate is absent: applicability.** Nothing records why the consumed
Standing was applicable input to this formation act.

This is not obviously a defect, and the report does not call it one. Whether a
formation act needs an applicability determination is exactly the kind of
question `01.Standing.E.1` leaves to the exact act owner.

**A dichotomy drawn here earlier is withdrawn.** It read "acts that assert
nothing" against "acts that establish standing," resting on the claim that
forming a bounded representation asserts nothing. That claim is not supported.
The event's own authority string is much narrower — it establishes "no
selection, warrant, goal, or response treatment," which is not the same as
asserting nothing. And `08.Communication:45` has the operator "rely only on the
assertion and standing the emitted representation directly warrants for its
declared purpose," so a representation does carry an assertion. `08.Communication:10`
says only that formation is not emission.

```text
representation formation does not strengthen source Standing    supported
representation formation asserts nothing                        not supported
```

What survives is the observation without the boundary: the live formation act
records no applicability, the dormant chain records one, and no principle
separating the two cases has been established here.

## 5. Chronology is in the ledger; topology is in the payload

`EventLedger.append` accepts `causation_id` and `correlation_id` — ordinary
event-bus fields. **Neither is used anywhere in the operator console path.**

That is the right outcome and worth recording as a positive finding, because it
is this campaign's principle enforced in code. Constitutional lineage lives in
the payload as explicit references to the exact consumed events; chronological
causation is available and left unused. Reading the constitutional path off
`causation_id` would be reading topology from chronology, and nothing does.

Equally, control flow is not supplying warrant in the dormant chain: admission
does not become lawful because it was called after applicability, but because
it consumed a recorded applicable applicability event and agrees with it
field-by-field. Call order and lawfulness are separately established.

## 6. What this does not establish

That the dormant path should be connected. It was written for goal
establishment, and whether that is the next act the console should perform is a
separate question this report does not answer.

That formation needs an applicability coordinate. §4 records the asymmetry and
declines to call it a gap.

That any act is the "first lawful act" available from the current session
Standing. The question of what Seed can first lawfully do from a given Standing
is well-formed and unanswered; naming an act because an occurrence is wanted is
the error this campaign keeps finding.

That the recorded chain is verified against active law clause by clause. This
survey read the implementation and the relevant chapters, and §3.1 records one
conflict found in passing. It did not audit the remaining coordinates, and one
found conflict is a reason to expect others rather than evidence that the rest
are sound.

That the Applicability compression is the only defect, or that widening the
result vocabulary would fix it. Recording `conflicting` and `Unknown` where
they belong is necessary; whether each of the eight named grounds maps to the
right one of the four standings is a separate determination owned by that
boundary.

## 7. Method note

The claim that occurrence implies Event was checked before being used, and it
is false in the form stated — `06.Events:20` denies it directly. The
distinction it protects is real: an Event is testimony that an occurrence was
asserted, and treating the ledger as the occurrence would make recording
constitutive of the act it records.

The dormancy finding came from asking which non-test callers exist, rather than
from reading the module. A module that imports cleanly, has passing tests, and
implements a careful chain can still be connected to nothing, and the test
suite will not say so.

**Correction recorded.** An earlier draft claimed "the lawful path is already
implemented" while its own limits section admitted the chain had not been
audited against active law. Those two statements cannot both stand, and the
first was written from being impressed by the code rather than from checking
it. One clause — `01.Lenses:14` — was enough to find a conflict.

The general form: **a sophisticated implementation is evidence of care, not of
fidelity.** Recorded stages, named bases, and cross-validated references are
exactly what a correct implementation looks like *and* exactly what a
confidently wrong one looks like. The compression found here is invisible
unless the result vocabulary is compared against the clause, because nothing in
the code looks careless.
