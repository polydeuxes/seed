# Next baked-in edge after participation removal 001

## Scope

This report re-reads what remains of the 2298–2310 architecture through:

```text
occurrence order  != relation topology
control flow      != Applicability
preserved temporal testimony != participation in an Act
```

and identifies the next earliest relation the campaign still supplies for
itself rather than allowing it to arise from preserved occurrences and
Standing.

The automatic `current_presentation → Compare` edge removed at #2329 is treated
as settled. `closed-choice` vocabulary is out of scope. This report amends no
active law, runtime, test, or projection, and authorizes no construction.
Verified at `b195602`.

## 1. Answer

**One baked-in edge remains active, and it is the same recency selection that
drove the removed one.**

```text
projector      current_presentation := the most recently emitted Presentation
                 (operator_session_standing.py:222 — last emission wins)

console        active_presentation = session_standing["current_presentation"]
               → passed as produced_after_presentation
                 (seed_local.py:5690)

ingress        records produced_after_presentation_ref
               + formation event id + emission event id
                 (operator_ingress.py:288)
```

#2329 removed one consumer of `current_presentation`. The selection itself, and
its other consumer, survive.

## 2. Why this is a relation rather than a preserved fact

The temporal fact the console witnesses is real: it emitted C, then captured E.
But the fact it witnesses is not the fact it records.

Demonstrated on a live two-interaction session:

```text
presentations emitted   C1, C2, C3
E1 produced_after   →   C1
E2 produced_after   →   C2
```

E2 was captured after **both** C1 and C2 were emitted. The witnessed temporal
fact holds for both. The record names one.

So the recorded coordinate is not `E2 occurred after these emissions`. It is
`E2 stands in a privileged relation to C2`, and what makes C2 privileged is
recency in the projector — not any determined relation between those two
subjects.

`01.Standing.D` bears directly on this: co-presence or multiplicity does not by
itself establish membership, relation, topology, **ordering**, selection,
priority, or focus. Selecting one of several equally-qualifying subjects is a
selection, and selection is named in that list.

`05.Testimony:111` bears on it too: retaining `up at t1, down at t2, up at t3`
does not establish trajectory, transition, or consequence without a separate
comparison boundary. Retaining `C1 emitted, C2 emitted, E2 captured` likewise
does not establish that E2 belongs with C2.

## 3. What the code says it is doing, and what it does

`operator_ingress.py:230-234`:

> `produced_after_presentation` is the exact emitted Presentation that preceded
> this capture, where one exists. The ingress occurrence records only the
> temporal relation — this material was produced after that exact emission. It
> does not classify the material as a response and establishes no operator
> intent, selection, or requested treatment.

Each denial in that paragraph holds. Response, intent, selection, and treatment
are genuinely not established. The undeclared step is earlier: *"the exact
emitted Presentation that preceded this capture"* presupposes a unique
predecessor. Several presentations preceded the capture. `the` is doing
selection work that nothing determined.

```text
denied and genuinely absent    response classification
                               operator intent
                               operator selection
                               requested treatment

undeclared and present         which of several preceding emissions is the
                               one this occurrence names
```

## 4. The five-way distinction applied

| | |
| --- | --- |
| merely preserved about C and E | C's formation and emission occurrences with their own coordinates; E's exact bytes, decoder examination, decoded content, capture boundary, known loss. Each independently preserved, neither referring to the other. |
| what Standing projection legitimately exposes | every recorded session event in append order (`consumed_event_ids`), each presentation with its alternatives and bindings, each preserved ingress occurrence, and the loss/Unknown/conflict unions. All of this is recovery of what was recorded. |
| what projection additionally supplies | `current_presentation`, and the four `latest_*` coordinates. None of these is recorded by any event. Each is a recency selection performed by the projector. |
| what determines Applicability to an exact Act | nothing. `01.Standing.E.1` assigns this to the responsibility performing the exact act; no such determination is recorded anywhere in the active path. |
| what the Act establishes | the ingress occurrence establishes preserved material with meaning Unknown. It additionally records a named relation to one Presentation, which is not part of what it establishes. |

## 5. Is `current_presentation` itself the defect?

Distinguish two things the projector does with it.

```text
recovering that C1, C2, C3 were emitted, in this order,
each with its own occurrence Evidence
        → recovery of recorded testimony

naming C3 "current"
        → a selection over preserved subjects, performed by the
          projector, recorded by no event
```

The first is legitimate and should stay. The second is the supplied edge.
`latest_exchange_finding`, `latest_source_recovery`, `latest_meaning_relation`,
and `latest_interaction_goal_standing` are the same construction over dormant
material; they are inert only because nothing produces their inputs.

Note that `current` and `latest` are not equivalent claims either. `latest`
describes append position and is recoverable from the record. `current`
asserts present relevance, which is a standing claim about now, and nothing
establishes it.

## 6. What is not the defect

Preserved by this report as coherent local machinery:

```text
exact byte preservation, decoder examination, known loss    coherent
Presentation formation and emission as distinct occurrences  coherent
Standing consumption recorded with as-of and evidence ids    coherent
projector reconstruction and structural refusal              coherent
the produced-after *record* as a place to preserve an
  established relation                                       coherent
```

The dormant Compare, Identification, source recovery, meaning relation, and
interaction-goal machinery are not examined here and are not asserted defective.
Their own Responsibilities may be coherent; they are simply unreachable.

## 7. If re-entry occurred

The request asks which dormant assumption would become active first. Ordered:

```text
1  current_presentation as the Compare participant
     the removed edge. Re-entering by restoring that call re-establishes
     recency-selected participation.

2  produced_after agreement as a precondition
     the comparison verifies the ingress records this exact C. That
     verification is sound, but what it verifies was itself supplied by
     recency, so a valid chain would rest on a supplied premise.

3  developer-supplied attribution as a gate
     source recovery requires attribution == "developer-supplied"; the goal
     path requires the same of the treatment relation. Evidence-born content
     is refused, not merely unmatched.

4  CONSUMER_PURPOSE compared against itself
     applicability requires the treatment's consumer purpose to equal a
     developer-written constant, with both sides developer-written.
```

Item 2 is the one most likely to be missed: the integrity validation added at
#2301 and hardened through #2306 is genuinely rigorous, and it would validate a
chain whose first link was never determined.

## 8. Dispositions

| Claim | Class |
| --- | --- |
| `current_presentation` is a recency selection recorded by no event | **A** — read directly from the projector |
| the console consumes it to record a privileged produced-after relation | **A** — read directly, demonstrated live |
| several presentations satisfy the same witnessed temporal fact | **A** — demonstrated live |
| selecting one of them is selection, which multiplicity does not establish | **A** — `01.Standing.D` names selection and ordering |
| the ingress docstring's denials are accurate | **A** |
| its `the exact emitted Presentation that preceded` presupposes uniqueness | **A** |
| recovering emission order is legitimate | **A** |
| `current` asserts more than `latest` | **C** — the distinction is real; whether `latest` alone is lawful here is not determined |
| the produced-after field should be preserved as the natural place for a later established relation | **withdrawn** — see §10 |
| dormant machinery is defective | **not asserted** — unreachable, not examined |

## 9. Smallest next boundary

Not the removal of a field. The question the recovery exposes:

```text
what responsible occurrence determines which preserved Presentation,
if any, an exact preserved ingress occurrence stands in relation to —
and what does that relation establish?
```

Until that is recovered, the honest record of a capture is that it occurred
after every emission preceding it, which is what the console actually witnessed.
Whether an ingress occurrence should name one presentation at all, or name the
set, or name none and leave the relation to a later responsible occurrence, is
not determined here.

**Refinement.** The framing above assumes a prior C-to-E relation must be
recovered before a comparison. That is not established. `01.Standing.E.1`
requires the Responsibility performing an exact Act to determine Applicability
for every proposed input before that input participates — which a prior
semantic relation is one possible way to support, and not the only one. The
immediate missing coordinate is therefore **input Applicability to the exact
Compare occurrence**, not necessarily a relation subject preceding it.

The distinction that follows matters for what absence licenses:

```text
no established C-to-E relation
!= all C-to-E pairings are applicable
```

Removing a false recency pairing does not make arbitrary pairing lawful. It
leaves input Applicability undetermined, which is a different and weaker state
than either.

That question is the same shape as the one three prior investigations reached
from other directions, now at the earliest point in the live path where a
relation between two preserved subjects is asserted.

## 10. Correction: the preservation stance is withdrawn

An earlier version of this report declined to recommend removing the
produced-after coordinates, on the ground that they are *"the natural place to
preserve an established relation, and removing it would leave a later relation
unrecordable."* That is withdrawn, along with a second attempt at the same
stance which proposed keeping the coordinates because the dormant Compare and
source-recovery paths consume them.

`01.Standing.E:28` holds that a relation is its own bounded claim subject,
preserving its own participants and roles, assertion, evidence standing, scope,
producer, consumer and purpose, authority, occurrence, conflicts, and limits. A
relation therefore does not live inside one participant's record. A later
responsible occurrence establishing that E relates to some C names both
subjects itself, and the preserved emission and ingress occurrences are already
sufficient basis for it to do so.

The stance also failed on its own terms. A slot held open *for* a future
relation is not neutral while it is being filled: as long as the console
supplied the field from recency, the record asserted the relation now.
"Preserve it for later" cannot describe a coordinate that is currently
populated by an undetermined selection.

The second attempt failed differently and worse: it argued that because
downstream machinery consumes the coordinates, what was unlawful was the
producer rather than the field. **A downstream Consumer does not lawfully own
an upstream coordinate.** Consumer demand is neither ownership nor Warrant, and
the dependency was evidence that the contamination had propagated rather than
grounds for preserving its source. That attempt also reached for the
`alternative_sources` precedent from #2330, which does not carry: alternatives
are content of the formation that carries them, while a C-to-E relation is
between two independently preserved subjects.

Recorded here rather than silently amended, because the reasoning that produced
both attempts — preserve the place where a warranted thing might later go, then
preserve it because something downstream expects it — is the same reasoning that
kept the developer alternatives in place across two prior deletions.

No construction or active-law amendment is authorized by this report.
