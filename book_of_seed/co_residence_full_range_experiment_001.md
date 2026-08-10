# Sixteen bodies, every displacement, exact identities: experiment 012

Findings only. No runtime or Book amendment.

## Summary

Layer A measured each of the sixteen `#2408` bodies alone, over **every
displacement the material makes available**, preserving exact finding
identities rather than counts. Layer B put the same sixteen into one durable
Seed as sixteen exchanges and reran the identical session-bounded measurements.

```text
  body             span      distinct findings   A == B
  euclid           d1..d30          380          identical
  emerson          d1..d15          108          identical
  algebra          d1..d18           99          identical
  boole            d1..d22           66          identical
  latin_vulgate    d1..d16           61          identical
  franklin         d1..d15           55          identical
  austen           d1..d16           42          identical
  dickens          d1..d17           29          identical
  cookbook         d1..d14           23          identical
  grammar_brown    d1..d15           22          identical
  hume             d1..d14           18          identical
  french_hugo      d1..d15           11          identical
  webster          d1..d14            8          identical
  grammar_kittr    d1..d13            8          identical
  roget            d1..d15            7          identical
  bash_guide       d1..d13            4          identical
```

**[measured]** 16 of 16 bodies produce identical finding sets alone and
co-resident — identical at every displacement, by exact pair identity, not by
count. `#2415` showed this for one displacement and one number per body. This
shows it for every displacement the material reaches and for every identity in
every set.

**Layer C was not run.** §3 records why, and it is not a cost problem.

## 1. `#2407`'s disjointness does not generalise

`#2407` measured Brown and Roget at d1–d5 and recorded:

> **[inference]** Each displacement produces its own pair findings. Displacement
> is not re-finding one structure at several distances; the sets are disjoint.

**[measured]** That is false for four of sixteen bodies:

```text
  body          distinct   occurrences   findings at >1 displacement
  euclid             380           405        20
  algebra             99           109         7
  webster              8            10         1
  cookbook            23            24         1
  the other twelve                             0
```

```text
  euclid    ('4.', '5.')                at displacements 1, 4, 7, 13
  euclid    ('because', 'therefore')    at displacements 2, 4, 6
  algebra   ('2.', '3.')                at displacements 1, 2, 4, 6, 7
  webster   ('277),', 'Ac*com"mo*date,') at displacements 1, 2, 3
```

**[measured]** Brown and Roget have zero recurrence, which is exactly what
`#2407` measured. Its **observation** stands for the bodies it examined; its
**inference**, stated about displacement generally, does not.

**[inference]** The double-counting concern `#2407` reported as refuted was
therefore correct as a general concern. It was refuted on two bodies and
generalised from them, and `#2406`'s row totals — Brown and Roget — remain
sound for the same narrow reason.

## 2. `#2404` measured the available range from a sample

`#2404` reported the displacements each body makes available:

```text
  BROWN   displacements measurable: 1..15
  ROGET   displacements measurable: 1..12
```

and stated the principle that gives that list its force:

> A displacement absent from that list is absent because **nothing reaches it**,
> not because it was judged uninteresting.

**[measured]** The list was computed from `enumerate_representations(occ)[:60]`
— the first sixty representations of the body. Roget's actual range is
**d1..d15**, not d1..d12. Brown's 1..15 happened to be right.

**[inference]** A displacement could be absent from that list precisely because
it was not looked at, which is the possibility the principle was written to
exclude. The sentence was true of the function and false of the run.

**[measured]** Over the full range the bodies reach much further than anything
measured before: euclid to d30, boole to d22, algebra to d18.

## 3. Why layer C was not run

Curator asked for a cross-body comparison and then corrected the plan: a
comparison performed in reader code would establish only that **a reader** can
compare independently preserved findings. That correction is accepted, and the
Python set-intersection this report's author had written was discarded rather
than reported.

**The owner is recovered, and it is recovered for this case.**
`candidate_versus_grammar_comparison_recovery_001.md`, quoted at
`compare_standing_continuation_recovery_001.md:74`:

> **Responsible owner or boundary** — The bounded comparison boundary that
> consumes the testimonies or findings. **The exact owner is local to the
> instantiated comparison and is not named universally.**

`compare_occurrence_implementation_form_recovery_001.md:229` guards its
direction: occurrence-local ownership is recovered for bounded testimony
comparison and "must not be transferred" to the unresolved
candidate-versus-relation-grammar case.

**[inference]** So what may be built is an occurrence, never a service. A
general comparator would be the universal owner the recovery says does not
exist.

**One coordinate blocks it.** `05.Testimony.E` permits consumption "only while
preserving" ten coordinates of each input. A recorded measurement finding
carries nine:

```text
  attribution                 dimensions.responsibility
  provenance                  dimensions.source_provenance + lineage
  support basis               premise_event_id + premise_chain()
  subject                     dimensions.identity
  scope                       dimensions.scope_locality + counting_scope
  authority                   dimensions.authority_warrant
  confidence or uncertainty   ABSENT
  Unknowns                    payload.unknowns
  standing                    dimensions.standing
  forbidden inferences        payload.boundary_notes
```

**[measured]** `preserved_material_measurement.py:27` quotes that ten-item list
in its own docstring, and `premise_chain()` was built specifically to satisfy
the support-basis item. The confidence coordinate was never carried.

**[Unknown]** Whether an input lacking a coordinate may be consumed at all, or
whether the obligation is only that a comparison not erase what an input has.
Both readings are available and this report picks neither, because picking one
to unblock the experiment is how a gap becomes invisible.

**[Unknown]** What a measurement's confidence or uncertainty even is. Counting
under a declared byte-equality rule is exact. The choices that do carry
uncertainty — the window, the overlap criterion `#2414` recorded as
developer-chosen — currently live in reports rather than in any finding.

## 4. What this does not establish

**That co-residence is safe under other measurement families.** One family was
run. A form reading across occurrences rather than within them would pool these
bodies immediately.

**That the recurrence in §1 means anything.** Four bodies carry findings at
several displacements and twelve do not. Nothing here accounts for the split,
and the recurring identities are not interpreted.

**That the full range was exhausted.** Every displacement the material makes
available was measured. `#2409`'s limit holds: exhausting a finite experimental
family is not constitutional Stopping.

**That any finding is a relation.** These are measured pair findings under a
criterion this report's author chose. `01.Standing.D` refuses relation standing
to co-presence, and sharing one across bodies would not supply it either.
