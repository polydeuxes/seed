# One arrangement across displacement: experiment 008

Findings only. No runtime or Book amendment.

## Summary

Every comparison in this arc so far drew a **fresh permutation for each
displacement**. That destroys the relation between an arrangement and how it
responds across displacement, so the marginal bands in `#2404` and `#2405`
could not have shown it.

This shuffles once per seed and measures d1 to d5 against that one permutation,
twenty seeds, both sources. The matrices are preserved without being collapsed.

```text
BROWN                        d1  d2  d3  d4  d5      ROGET          d1  d2  d3  d4  d5
  ordered                     7   6   4   1   4        ordered       5   1   0   1   0
  seed00                      5   2   5   1   0        seed00        0   0   0   0   0
  seed01                      3   4   5   2   0        seed01        0   0   0   0   0
  seed02                     13   4   2   1   7        seed02        0   0   0   0   1
  seed03                     21   2   3   5   0        seed03        0   0   0   0   0
  seed04                      2   8   6   4   2        seed04        0   0   0   0   1
  seed05                      1   3   7   5   7        seed05        0   1   0   0   0
  seed06                     13   5   3   4   1        seed06        0   0   0   0   1
  seed07                      1   2   2   0   1        seed07        0   0   0   0   0
  seed08                     14   1   6   4   2        seed08        0   0   0   0   0
  seed09                      4  10   8   4   5        seed09        0   0   0   0   0
  seed10                      5   6   1   4   0        seed10        0   1   0   0   0
  seed11                      4   4   9   3   0        seed11        0   1   0   0   0
  seed12                      2   5   3   1   1        seed12        0   0   0   0   0
  seed13                      4   6   6   5   4        seed13        0   0   0   0   0
  seed14                      5   5   1   4   2        seed14        2   0   0   0   0
  seed15                      3   5   3   7   3        seed15        0   0   0   1   0
  seed16                      3  10   3   1   1        seed16        0   0   0   0   0
  seed17                      7  11   1   0   3        seed17        0   1   0   0   0
  seed18                      6   5   1   4   4        seed18        0   0   0   0   0
  seed19                      2   4   7   2   3        seed19        0   0   0   0   0
```

**The result is not the one the joint shape was expected to give.** It is in the
column totals, and it is larger than anything the displacement question was
about.

## 1. Shuffling the two sources does not do the same thing

```text
              recurring reps   ordered row total   shuffled row totals
  BROWN                 259                  22   6..31,  mean 20.4
  ROGET                 277                   7   0.. 2,  mean  0.5
```

**[measured]** Shuffled Brown produces about as much overlap as ordered Brown.
Shuffled Roget produces almost none — eleven of its twenty rows are entirely
zero across all five displacements.

**[measured]** The two sources were already matched on recurring representations
in `#2401`, 259 against 277. Matched recurrence does not predict this.

**[inference]** The Unknown this arc has been circling is stated backwards.
"Why does Roget separate and Brown not" invites an account of the two **ordered**
materials. What differs by a factor of forty is what happens to each source when
its arrangement is **destroyed**. Shuffling Roget removes nearly all overlap;
shuffling Brown removes none of it.

This is not `#2401`'s refuted density hypothesis returning. That one matched the
count of recurring representations, and this holds while matched.

## 2. What the joint shape answers

**Does a high value at one displacement travel with high values at the others?**

**[measured]** No. Across the twenty Brown permutations, every pairwise
correlation between displacement columns is weak:

```text
  d1-d2  -0.29     d2-d3  -0.10     d3-d4  +0.20
  d1-d3  -0.23     d2-d4  -0.12     d3-d5  +0.12
  d1-d4  +0.17     d2-d5  +0.16     d4-d5  +0.18
  d1-d5  -0.07
```

**[measured]** There is no generally noisy permutation. `#2405`'s Brown d5 = 8
does not belong to one: the two rows carrying this run's largest d5 values are
`seed02 [13, 4, 2, 1, 7]` and `seed05 [1, 3, 7, 5, 7]`, which sit at opposite
ends of the d1 column.

**Does ordered Brown have a profile shape the permutations do not reproduce?**

**[measured]** No. Ordered Brown's largest value carries 0.32 of its row total,
which is flatter than most permutations but not outside them — four of twenty
are at or below it, the flattest at 0.24. Nine of twenty permutations have a larger row
total than ordered's 22.

**[measured]** Ordered Brown is inside its shuffled band at every displacement
d1 to d5, and at d4 eighteen of twenty permutations reach or exceed it.

That last sentence is the one `#2405` withdrew from `#2404` for being
unsupported by the five-seed data it cited. It is now measured. **A claim
acquiring evidence later does not retroactively warrant having made it**, and
the withdrawal stands as the correct handling of what was on the page at the
time.

## 3. Five seeds understated the band worse at d1 than at d5

```text
  BROWN d1     5 seeds  largest shuffled value   9      20 seeds   21
  BROWN d5     5 seeds  largest shuffled value   2      20 seeds    7
```

**[measured]** `#2405` recorded the d5 understatement. Every other row of
`#2404`'s Brown table was left at five seeds, and d1 is understated by more.

**[measured]** Brown d1 ordered = 7 was read throughout `#2396`, `#2401` and
`#2404` against a five-seed band topping out at 9, which made it look close to
the top. Three of twenty permutations reach 13, 14 and 21.

## 4. Roget, a third time and by a different route

**[measured]** Ordered Roget d1 = 5 exceeds all twenty permutations, whose
largest value is 2.

**[measured]** Ordered Roget's row total of 7 exceeds all twenty permutation row
totals, whose largest is 2. The separation is not confined to d1; it holds for
the profile taken whole.

These twenty permutations are **not** `#2405`'s twenty. See the disclosure
below. This is an independent sample, and Roget has now separated in three of
them.

## 5. Disclosures

**The permutation for seed *s* is defined differently here.** Earlier scripts
called `shuffle` on a list left shuffled by the previous iteration, so "seed 7"
named a different arrangement depending on what ran before it. This draws each
permutation from a fresh copy. Numbers here therefore do not reproduce `#2405`'s
and are not meant to.

**The overlap criterion is a developer-chosen number.** Two representations are
counted as overlapping when their measured sets share at least half of their
union. I chose one half. It sits underneath every count in this arc including
`#2396`'s, and nothing has varied it.

**Roget's spike measure is degenerate and is not reported above.** Eleven of its
twenty rows are all-zero and the other nine carry exactly one nonzero value, so any
share-of-total is either undefined or exactly 1. That is arithmetic on an empty
population, not a shape.

**The comparison Roget's result rests on is nearly empty.** Its permutations
average 0.5 overlaps across five displacements. A measurement that fires almost
never has no body, only tail, and every reading of it is a reading of the tail.
This does not withdraw the result. It states what the result is made of.

## 6. What this does not establish

**That the section 1 difference is explained.** It is measured and it is not
accounted for. What shuffling does to a source is now the subject, and no
property of either source has been shown to produce it.

**That the ordered materials are alike.** Nothing here compared them to each
other, only each to its own permutations.

**That displacement was the wrong coordinate.** The joint measurement was worth
making and answered its questions. It found something else, which is not the
same as the question having been idle.

**That twenty seeds is enough**, per `#2405`. Brown d1's band grew from 9 to 21
between five and twenty, and no count is warranted here as the right one.

**That any of this is Seed's finding.** The matrices come from Seed's preserved
ingress through its recorded measurements. The correlations, row totals and
share-of-total in sections 1 and 2 were computed by a reader over those
recordings, and Seed holds none of them.
