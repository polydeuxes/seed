# The Test Seed, entire

Findings only. No runtime or Book amendment. One store, reported whole.

## What it is

Sixteen 300-line source windows, each preserved in its own bounded exchange
inside one durable Seed, then measured, compared, and counted — every step
through Seed's own recorded occurrences.

```text
  store            /dev/shm/seed-scratch/real_c.db
  size             4.95 GB
  events           898,787
  exchanges        16
  elapsed          27 minutes
```

```text
  787,847   operator.measurement.comparison_recorded
   86,907   operator.measurement.finding_recorded
    4,816   operator.presentation.formed
    4,816   operator.presentation.emitted
    4,800   operator.ingress.representation_examined
    4,800   operator.ingress.raw_material_captured
    4,800   operator.ingress.ingress_occurred
        1   operator.measurement.cohort_recorded     <- see limits
```

## The three layers

```text
  A   each window alone, its own ledger, every available displacement
  B   the same sixteen co-resident, measured bounded by session
  C   comparison across them, through Seed's Compare
```

### A = B, exactly

**[measured]** All sixteen produce identical finding sets alone and
co-resident — identical at every displacement, by exact pair identity, not by
count.

```text
  euclid          d1..d30    380 findings     identical
  emerson         d1..d15    108              identical
  algebra         d1..d18     99              identical
  boole           d1..d22     66              identical
  franklin        d1..d15     55              identical
  austen          d1..d16     42              identical
  dickens         d1..d17     29              identical
  cookbook        d1..d14     23              identical
  grammar_brown   d1..d15     22              identical
  hume            d1..d14     18              identical
  french_hugo     d1..d15     11              identical
  webster         d1..d14      8              identical
  grammar_kittr   d1..d13      8              identical
  roget           d1..d15      7              identical
  bash_guide      d1..d13      4              identical
  (+ the sixteenth)
```

**[inference]** Co-residence alters nothing. Sixteen bodies sharing a workspace,
a ledger and a process measure exactly what they measured alone.

### C, through Seed rather than a reader

**[measured]** 720,881 comparison occurrences, every one recording bounded
relation `Unknown`, on the basis that inputs exact within different bounded
exchanges are not in disagreement when they differ and not corroborated when
they match.

**[inference]** That refusal is the result. The machinery had every chance to
report agreement — `('of','the')` is shared by fifteen exchanges — and declined
720,881 times. `agreement` and `conflict` are reachable only within one
exchange, where a same-subject difference would be a real conflict.

**[measured]** Recurrence across exchanges, counted over those comparisons:

```text
  83,351 distinctions

  recurs in  1 of 16 exchanges   77,663
  recurs in  2 of 16              3,719
  recurs in  3 of 16                969
  recurs in  5 of 16                242
  recurs in 10 of 16                 32
  recurs in 14 of 16                  2
  recurs in 15 of 16                  1

  ('of','the') at displacement 1, byte-for-byte equality      15 exchanges
  ('in','the') at displacement 1                              14
  ('the','the') at displacement 3                             14
```

## What the campaign measured about itself

```text
  phase                    elapsed      events      rate
  ingest 16 exchanges          24s      24,032    1004/s
  record findings             143s      86,907     608/s
  Q1 same displacement        123s      66,966     544/s
  Q2 cross displacement      1334s     720,881     540/s

  finding    6,203 B/event      comparison   5,096 B/event
```

**[measured]** The same work on disk was tracking toward 4.9 hours. The
difference was never RAM against disk: it was one durability barrier per
occurrence, and `#2433` showed full-durability batching reaching 0.143 ms/event
against tmpfs's 0.218.

## What this store does not establish

**That any recurrence is a relation.** `01.Standing.D` refuses relation standing
to co-presence, and recurrence is co-presence counted. Every cross-exchange
comparison in the store says `Unknown`.

**That the widest recurrences are meaningful.** They are English function words
under a byte-equality rule. `#2408` established that a reader's categories
predict nothing about these sources.

**That the sources are independent.** They are independently *preserved*. Two
19th-century grammar textbooks are not independent witnesses, and
`05.Testimony.E` holds that repetition is not independent corroboration.

**That these are 300-line properties or book properties.** They are properties
of sixteen 300-line windows. `euclid` reaching d30 is a fact about a window of
Casey's Euclid.

**That the store is faithful in two known respects.** `bash_guide` is 5.4% of
its source, truncated by the console escape `#2435` measured and `#2436`
removed. `latin_vulgate` is the English Douay-Rheims, which withdrew `#2408`'s
non-English finding — so fifteen of the sixteen windows are English, not
fourteen.

**That the single `cohort_recorded` occurrence is current.** It was written
during `#2429`, whose vocabulary and Responsibility `#2430`–`#2432` withdrew. It
remains in the store because the store is append-only and history is not
rewritten to match a later correction.

**That the store is durable.** It is on tmpfs. Every occurrence verifies against
its digest and none survives a reboot; `#2426` recorded that integrity and
persistence are separate properties.
