# What measuring past d1 finds: experiment 009

Findings only. No runtime or Book amendment.

## Summary

The question: **does measuring ordered Brown past d1 tell us anything d1 alone
does not?**

Answered by keeping the identity of every overlapping pair rather than its
count, so a pair found at two displacements is one pair. Union and intersection
over those pairs are the identity of what was found, not a score over it, and
no aggregation rule is invented.

```text
BROWN        pairs per d          running union        d1   new past d1   union
  ordered    7,  6,  4,  1,  4    7, 13, 17, 18, 22     7        15         22
  shuffled                                             1..21    5..27      6..31
                                                                          9/20 >= 22

ROGET        pairs per d          running union        d1   new past d1   union
  ordered    5,  1,  0,  1,  0    5,  6,  6,  7,  7     5         2          7
  shuffled                                             0..2     0..1       0..2
                                                                          0/20 >= 7
```

**Yes, and no.** Measuring past d1 finds ordered Brown fifteen relations d1
never found — more than doubling what d1 alone holds, and drawing in 36
representations where d1 touched 13. **None of that separates it from noise.**
Nine of twenty permutations reach or exceed its union of 22, and the two most
productive permutations gain 27 and 22 new relations past d1 against ordered's
15.

**More relations. No more knowledge that tells ordered Brown from a shuffle.**

## 1. The two sources invert

```text
                gain past d1     separates from its permutations
  BROWN           15 pairs                   no
  ROGET            2 pairs                  yes
```

**[measured]** Brown gains the most from measuring further and gains nothing
distinctive. Roget gains almost nothing from measuring further and was already
separated at d1 — its union result, 7 against a largest permutation union of 2,
is `#2406`'s d1 result carrying two extra pairs, not a new separation.

**[inference]** Measuring more and knowing more come apart here, and they come
apart in opposite directions on the two sources. Whatever ordered Brown holds
across d1 to d5, permutations of Brown hold as much of it.

## 2. No pair is found at two displacements

**[measured]** Across all 42 arrangements measured — ordered and twenty
permutations, both sources — **zero pairs appear at more than one
displacement.** Every row's per-displacement counts sum exactly to its union:

```text
  ordered Brown   7 + 6 + 4 + 1 + 4  =  22  =  union
  seed02         13 + 4 + 2 + 1 + 7  =  27  =  union
```

**[inference]** Each displacement finds its own relations. Displacement is not
re-finding one structure at several distances; the sets are disjoint.

**This refutes the double-counting concern raised against `#2406`.** Its row
totals could not have double-counted, because there was nothing to count twice.

**`#2406` did not know that.** It summed five measurements without establishing
that the things summed were distinct, and the sum was sound by luck. A correct
number produced without the check that would have made it correct is not
evidence that the check was unnecessary.

## 3. What this does not establish

**That the d1–d5 region has been measured as one subject.** It has not. This
measures five displacements and then reads the identity of what each found. A
form whose subject is the region itself does not exist, and the combined column
a reader expects from `#2406` still does not exist. This answers a narrower
question than that one.

**That ordered Brown holds no arrangement.** It holds 22 relations that a
reader can inspect. What is measured is that its permutations hold as many,
which as `#2395` recorded establishes nothing about the material.

**That the gain is real knowledge in any other sense.** The relations found
past d1 are relations under the one-half overlap criterion recorded as a
developer-chosen number in `#2406`, still unvaried.

**That five displacements is the region.** Brown reaches 15 and Roget 12.
Five were measured, as in `#2404`, and the choice is still mine.

**That Roget's two extra pairs mean anything.** Two pairs on a comparison whose
permutations average well under one is inside the emptiness `#2406` disclosed.
