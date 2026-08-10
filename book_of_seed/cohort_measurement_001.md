# What recurs across the preserved bodies

Runtime amended narrowly. No Book amendment.

## What was built

`seed_runtime/cohort_measurement.py`. Its subject is **recorded comparison
occurrences**, and it answers a question no single comparison contains:

```text
these N independently preserved bodies carry the same measured distinction
under the declared rule and scope
```

`measurement_self_survey` established the move one level down — recorded
measurement occurrences are preserved events, and counting over them is the
same act on a different subject. This is that, one level up.

**[measured]** `#2420` recorded the gap precisely: Seed held each pairwise
sharing, and "appears in 7 of 16 bodies" was a reader's tally over them. That
tally is now an act with its own event kind.

## What it found

Over the 720,881 comparisons of the sixteen-body run:

```text
  83,351 distinctions, population 16 bounded exchanges

  carried by  1 of 16 bodies   77,663
  carried by  2 of 16           3,719
  carried by  3 of 16             969
  carried by  5 of 16             242
  carried by 10 of 16              32
  carried by 14 of 16               2
  carried by 15 of 16               1

  15 bodies carry ('of', 'the') at displacement 1
  14 bodies carry ('in', 'the') at displacement 1
  14 bodies carry ('the', 'the') at displacement 3
```

## Three states, each proven

```text
  carried_by              a comparison found it on both sides
  exposed_without_it      measured that coordinate, not among those carrying
  coordinate_not_exposed  never measured that coordinate
```

**[measured]** They partition the population: every cohort sums to sixteen, and
a test pins that as an invariant rather than a coincidence.

**[inference]** The third state cannot come from comparisons. An earlier form
computed it as the residue after the first two, and a body whose finding exists
at the coordinate but which was never compared against a carrier falls into the
same residue — it would have been reported as never having exposed it. So the
recorded **measurement** occurrences supply who measured the coordinate and the
recorded **comparison** occurrences supply who carried the distinction.
Curator caught this after the first version had already run.

## The defect the data exposed

The first distribution read:

```text
  carried by 0 bodies   77,663
  carried by 2 bodies    3,719      <- and nothing at 1
```

**[inference]** 77,663 zeros and no ones is a bug signature, not a finding
about English. `carried_by` was populated only from occupants a comparison
found on *both* sides, so a distinction held by exactly one body was reported
as carried by nobody. The comparison records `occupants_in_one_only` keyed by
input event and the event-to-exchange mapping was available; it had been used
in the first version and dropped while repairing the third state.

**Two defects in one module, both caught downstream rather than by its author,
and the second was introduced while fixing the first.**

## What the record refuses

Five inferences are refused in every recorded cohort:

```text
  independently preserved is not independent; nothing establishes that the
    bodies' sources are unrelated
  a cohort is repetition, and repetition is not independent corroboration
  the cohort size reports which bodies were supplied to this Seed, not a
    property of the material
  a body that never exposed the coordinate has not declined to carry the
    distinction
  carrying the same measured distinction establishes no relation between the
    bodies that carried it
```

**[inference]** The second is `05.Testimony.E:29` applied to this act's own
output. Two 19th-century grammar textbooks, or two transcriptions sharing
editorial apparatus, are not independent witnesses. The bodies are
independently *preserved*; nothing here establishes independent sources.

**[measured]** `render_cohort` emits only the literal sentence. A test asserts
that `agree`, `corroborat`, `independent source`, `relation`, `confirm` and
`prove` never appear in it.

## What this does not establish

**That any cohort is a relation.** `01.Standing.D` refuses relation standing to
co-presence, and a cohort is co-presence counted. The `Unknown` that every
cross-body comparison produces is unchanged and untouched.

**That the widest cohorts are the meaningful ones.** `('of', 'the')` recurring
in fifteen bodies is a measured recurrence of English function words under a
byte-equality rule. `#2408` established that a reader's categories predict
nothing about these sources, and this report assigns none.

**That the denominator means anything.** Sixteen is how many bodies were
supplied. Three more dictionaries would move every cohort without anything
about the material changing.

**That a cohort of one is smaller evidence than a cohort of fifteen.** They are
different facts about the population. Nothing here ranks them, and 93% of the
distinctions are cohorts of one.
