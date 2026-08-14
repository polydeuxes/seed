# Displacement as an enumerated coordinate: experiment 007

Runtime amended narrowly. No Book amendment.

## Summary

`displacement` was fixed at 1 inside the indexing. It is now a parameter of the
measurement, and the displacements available from any representation are
**enumerated from the material** — the positions an occurrence actually reaches
from where the representation sits. No displacement is chosen, preferred, or
proposed.

Rerunning the same ordered-versus-shuffled comparison by displacement:

```text
BROWN                                  displacements measurable: 1..15
  disp   ordered   shuffled (5 seeds)   candidates
     1         7   1, 8, 9, 2, 2               211
     2         6   2, 0, 2, 10, 3              205
     3         4   6, 1, 0, 3, 5               186
     4         1   0, 4, 1, 3, 2               169
     5         4   1, 1, 1, 2, 1               147

ROGET                                  displacements measurable: 1..12
  disp   ordered   shuffled (5 seeds)   candidates
     1         5   0, 0, 0, 0, 0               206
     2         1   0, 0, 0, 0, 0               178
     3         0   0, 0, 1, 0, 0               142
     4         1   0, 0, 0, 0, 0               112
     5         0   0, 0, 0, 0, 0                87
```

**The favoured hypothesis does not survive.** The grammar corpus was expected,
by a reader, to carry arrangements at greater positional extent. Widening the
family did not reveal them.

**Correction.** This report first said ordered "sits inside its shuffled band at
every displacement measured". On the five-seed data printed above that is
**false at displacement 5**, where ordered is 4 and the largest shuffled value
is 2. The sentence contradicted the table two lines above it.

Rerun at twenty seeds, displacement 5 does not separate:

```text
BROWN d5   ordered   4
           shuffled  0 1 1 1 1 1 1 1 2 2 2 2 2 3 3 4 4 4 6 8
                     min 0, max 8, mean 2.5
           shuffles reaching or exceeding ordered   5 of 20
```

So the disposition survives and **the evidence first given for it did not**.
Being right while stating something the data on the page contradicts is not the
same as having measured it.

**The thesaurus's separation is specific to displacement 1**, and does not
recur further out. At displacements 2 to 5 the ordered counts are 1, 0, 1, 0 —
too small to distinguish from the zeroes beside them.

## 1. What changed in the runtime

`measure_at_displacement` takes the displacement and the direction and records
both. `enumerate_displacements` returns the displacements the material makes
measurable from a representation: an occurrence carrying it at index *i* has a
position at displacement *d* whenever the occurrence extends that far.

A displacement absent from that list is absent because **nothing reaches it**,
not because it was judged uninteresting.

`measure_after` remains as one displacement of the family, kept because the
continuation and its tests name it, and carrying no privilege.

## 2. The self-survey, rerun

The invariant `#2397` found has moved, and the survey reports the move rather
than being told about it:

```text
coordinate        distinct values observed   occurrences
  anchored_on      1  {the representation}          138
  direction        1  {after}                       138
  displacement     4  {1, 2, 3, 4}                  138
```

`displacement` now varies; `anchored_on` and `direction` do not, because this
run used one form. The survey reports what a run actually used, in either
direction, which is what makes it a survey rather than a claim.

## 3. What the shape shows

**[measured]** Brown does not separate from its shuffled comparison at any
displacement from 1 to 5. At displacement 5 this took twenty seeds to
establish; five did not bound the comparison.

**[measured]** Roget separates at displacement 1 and not measurably beyond it.

**[inference]** These are consistent with the thesaurus's repeated arrangements
being immediate ones. They are not consistent with the grammar corpus's
arrangements being *non*-immediate, which is what the reader's hypothesis
required, because no displacement tested exposed them.

**[Unknown]** Why Brown and Roget behave differently. `#2403` restored this to
Unknown after `#2401` refuted the density explanation, and this refutes the
hypothesis that stood in its place. Both of a reader's two guesses are now
spent.

## 4. Five seeds does not bound a comparison

Five shuffled seeds, the count used since `#2396`, understates the spread
badly:

```text
BROWN d5    5 seeds   largest shuffled value  2
           20 seeds   largest shuffled value  8
```

A band read from five seeds can be four times too narrow. Every
outside-the-band reading taken on five seeds is therefore weaker than it was
written to be — including the one this report nearly made.

**The load-bearing positive result was rechecked at the same depth and holds:**

```text
ROGET d1   ordered   5
           shuffled  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1
                     min 0, max 1, mean 0.2
           shuffles reaching or exceeding ordered   0 of 20
```

Twenty seeds, none reaching 5. `#2396`'s separation is not an artefact of a
thin comparison, and it is now better evidenced than when it was recorded.

**[inference]** The two sources differ in a way five seeds could not show:
Roget's shuffled spread at its measurement is 0 to 1, Brown's at its
measurement is 0 to 8. The comparisons are not equally noisy, and a fixed seed
count was treated as equally informative for both without anyone saying so.

## 5. What this does not establish

**That displacement explains the earlier result.** Results changed with
displacement for the thesaurus and did not for the grammar corpus, and neither
outcome makes the coordinate the account of anything. `#2397`'s restraint
holds: observing a coordinate with one value did not authorise another, and
observing it with several does not promote it.

**That the grammar corpus lacks structure.** A measurement family failing to
distinguish ordered from shuffled material establishes nothing about the
material, as `#2395` recorded and this session has now relied on three times.

**That displacements above 5 behave the same.** The material reaches 15 and 12
respectively. Five were measured. The cost of the rest is knowable, and the
choice of five was mine.

**That any displacement is better.** None is ranked here and none should be
read as ranked from the counts.

**That Roget's displacement-1 result is large.** Five overlaps against zeroes,
unchanged from `#2396`.

**That twenty seeds is enough.** It is more than five, and that is all that is
shown. No count is warranted here as the right one, and none is proposed.

**That the family is exhausted.** Direction, anchor, and the pair forms were
not varied alongside displacement, and exhausting a finite experimental family
would not be constitutional Stopping in any case.
