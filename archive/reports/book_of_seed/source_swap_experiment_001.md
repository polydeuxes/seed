# Source swap: experiment 005

Findings only. No runtime or Book amendment. `#2394` used unchanged.

## Executive

`#2395` found that the cycle's output on the grammar corpus was
indistinguishable from the same material shuffled, and left two live
explanations: the material was too thin, or the four measurement forms are not
the forms through which structure is visible.

This changes only the source. Same formation, same forms, same cycle, same
control.

**The mechanism can see structure.** On the thesaurus, ordered material
produces overlaps and shuffled material produces **none**, across five seeds.

```text
source        ORIGINAL   SHUFFLED (5 seeds)        separation
grammar            7     1, 8, 9  (3 seeds)        none
dictionary         3     1, 0, 1, 1, 1             marginal
thesaurus          5     0, 0, 0, 0, 0             clean
```

**The controls had more to work with, not less.** Shuffling produced *more*
candidate representations and *more* findings than the ordered material every
time — 249 candidates against 203 on the thesaurus, 10,549 findings against
8,110 — and still found nothing. The ordered material does more with fewer
opportunities.

So the first of `#2395`'s two explanations is the live one for the grammar
corpus: **it was starving the cycle.** Nothing here indicates the measurement
forms are the bottleneck.

## 1. Result

Mechanically bounded slices, 300 lines, at fixed offsets. No page was selected.

```text
DICTIONARY  lines 200000:200300
  ORIGINAL     reps=729   recur=144  find=4361   pass=16  ctx>=2: 94  overlaps=3
  SHUFFLED 0   reps=729   recur=144  find=5526   pass=14  ctx>=2:132  overlaps=1
  SHUFFLED 1                         find=5533   pass=14  ctx>=2:131  overlaps=0
  SHUFFLED 2                         find=5471   pass=14  ctx>=2:132  overlaps=1
  SHUFFLED 3                         find=5492   pass=14  ctx>=2:133  overlaps=1
  SHUFFLED 4                         find=5467   pass=16  ctx>=2:128  overlaps=1

THESAURUS   lines 6000:6300
  ORIGINAL     reps=1737  recur=277  find=8110   pass=30  ctx>=2:203  overlaps=5
  SHUFFLED 0   reps=1737  recur=277  find=10549  pass=30  ctx>=2:249  overlaps=0
  SHUFFLED 1                         find=10565  pass=28  ctx>=2:249  overlaps=0
  SHUFFLED 2                         find=10581  pass=28  ctx>=2:246  overlaps=0
  SHUFFLED 3                         find=10618  pass=32  ctx>=2:243  overlaps=0
  SHUFFLED 4                         find=10621  pass=30  ctx>=2:246  overlaps=0
```

Every run exhausted. As a rate over candidates:

```text
                original     shuffled
grammar            3.3%         2.5%     inside the band
dictionary         3.2%         0.8%     four-fold
thesaurus          2.5%         0.0%     nothing survives shuffling
```

## 2. What separated

The five thesaurus overlaps:

```text
1.00  'smart'       ~ 'lively'         shared = ['pace,', 'rate,']
0.67  'carriage,'   ~ 'compartment,'   shared = ['2nd',   '3rd'  ]
0.67  'rest'        ~ 'ride'           shared = ['and',   'at'   ]
0.50  'board,'      ~ 'way;'           shared = ['on',    'set'  ]
0.50  'Adv.'        ~ 'rest'           shared = ['at',    'on'   ]
```

**[inference]** The thesaurus repeats local arrangements densely — a
representation followed by the same two representations in more than one place
— and shuffling destroys exactly that. Whatever a reader makes of `smart` and
`lively` sharing `pace,` and `rate,`, the measurement's claim is only that two
representations were measured with the same successors, and the control
establishes that the material's order is why.

## 3. A methodological defect, found and fixed

The first pass seeded each run from the alphabetically first representation.
On one shuffled thesaurus control that representation had no measurable
successor, the run collapsed to a single finding and one pass, and the control
was not comparable to the others.

Seeding now takes the first representation with any measurable successor. That
is a mechanical rule, not a preference, and it does not choose which
representation is interesting — only that a run should not terminate before it
begins.

**[inference]** Reporting the earlier thesaurus control as `0, 0, 0` would have
counted a collapsed run as a finding of nothing.

## 4. What this does not establish

**That the thesaurus overlaps are classes.** They are five pairs sharing a
two-element measured set. The control establishes that order produced them; it
establishes nothing about what any representation is.

**That five is a large number.** It is five. What makes it evidence is that the
control returns zero with more candidates, not that five is high.

**That the grammar corpus lacks structure.** `#2395` established that this
measurement at that scale cannot distinguish it from noise. This establishes
that the same measurement can distinguish it elsewhere, which locates the
difficulty in the material rather than removing it.

**That the dictionary separates.** 3 against a band reaching 1 is marginal, and
one more seed could close it. It is reported as marginal, not as positive.

**That structure means grammar.** The thesaurus's repeated arrangements are
whatever they are. Nothing measured here is grammatical, semantic, or a
relation, and `01.Standing.D` still refuses relation standing to co-presence.

**That the forms are sufficient.** They separated one source of three. Whether
richer forms would separate the other two is untested.

**That slices are comparable.** 300 thesaurus lines offer 1,737 representations
and 300 dictionary lines offer 729. The sources differ in density as well as in
kind, and this experiment does not separate those.

## 5. What follows

`#2395`'s two explanations are no longer equally live. The cycle distinguishes
ordered from shuffled material when the material supplies dense repeated local
arrangement, so the measurement forms are not shown to be the bottleneck, and
turning to what representation Seed should form is not yet indicated by
evidence.

The measurement that would sharpen this is the same one at a scale where the
grammar corpus recurs as densely as 300 thesaurus lines do — with the shuffled
control run alongside, since it is the only thing that separated a finding from
a reader's recognition in all three sources.
