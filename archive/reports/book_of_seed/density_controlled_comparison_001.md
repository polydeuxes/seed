# Comparison at matched density: experiment 006

Findings only. No runtime or Book amendment.

## Summary

`#2395` left two explanations for the grammar corpus producing nothing its
shuffled comparison did not also produce: the material was too thin, or the
measurement forms are not the forms through which its structure is visible.

`#2396` chose the first. **That was wrong, and this withdraws it.**

Matching recurrence rather than line count, and running the same protocol with
the same number of comparison seeds:

```text
source        recurring   ORIGINAL   SHUFFLED (5 seeds)      separation
grammar             259          7   1, 8, 9, 2, 2           none
thesaurus           277          5   0, 0, 0, 0, 0           clean
```

**Density is not the difference.** Brown at 300 lines already offers 259
recurring representations against the thesaurus's 277 — so `#2396`'s comparison
already matched for density and neither it nor this session noticed.

**What that leaves is Unknown.** `#2395` offered two explanations and this
refutes one of them. It does not establish the other: the pair was never shown
to be exhaustive, and a source property nobody has represented yet would sit
outside it. Eliminating one member of a two-item list establishes the second
only if the list was complete, and nothing established that.

What is live is narrower: **some property of the sources and the forms
together** accounts for the difference. That the bounded positional form is
involved is a hypothesis with independent evidence behind it, not a conclusion
drawn here.

## 1. Withdrawal

`#2396` concluded:

> the first of `#2395`'s two explanations is the live one for the grammar
> corpus: it was starving the cycle. Nothing here indicates the measurement
> forms are the bottleneck.

Both sentences are withdrawn. The comparison it drew was between sources that
differed in kind *and* apparently in density, and the density difference was
assumed rather than measured. Measured, it is not there.

**The defect is arithmetic that was never done.** 300 thesaurus lines and 300
grammar lines were treated as differing in density because they differ in
representation count — 1,737 against 1,386 — without checking the quantity that
matters for context sets, which is how many representations recur at all.

## 2. The measurement

```text
thesaurus 300 lines : 1737 representations, 277 recurring
grammar   300 lines : 1386 representations, 259 recurring
grammar   600 lines : 2467 representations, 447 recurring
```

Brown was already matched at the slice `#2396` used. No new slice was needed;
the two were already matched.

Re-running Brown under the corrected protocol — five comparison seeds, and the
non-collapsing seeding rule `#2396` introduced — leaves it inside its band:

```text
  ORIGINAL order      recur=259   ctx>=2:211   overlaps=7
  SHUFFLED seed 0     recur=259   ctx>=2:239   overlaps=1
  SHUFFLED seed 1     recur=259   ctx>=2:234   overlaps=8
  SHUFFLED seed 2     recur=259   ctx>=2:234   overlaps=9
  SHUFFLED seed 3     recur=259   ctx>=2:239   overlaps=2
  SHUFFLED seed 4     recur=259   ctx>=2:240   overlaps=2
```

Seven against a band reaching nine. The thesaurus's five against a band of
zeroes, at comparable recurrence.

## 3. What this leaves

**[inference]** At matched recurrence, one source separates and the other does
not. Whatever accounts for that is a property of the sources and the forms
together, not of how much material was supplied.

**[Unknown]** Why the difference exists.

**[inference]** One hypothesis has independent evidence behind it. `#2397` made
observable that every one of the five forms was recorded with `displacement` of
1, across 3,226 occurrences. That is a fact about the measuring, established
separately from anything about these sources.

**What would make it an explanation, and is missing:** that the grammar
corpus's repeated arrangements are *not* immediate while the thesaurus's are.
**Nothing has measured that.** It is what a reader who knows English suspects,
and this session has already recorded three cases where a reader's recognition
was mistaken for a finding. So it stands as a hypothesis with a stated missing
measurement, not as the account of the result.

## 4. What this does not establish

**That a different displacement would separate the grammar corpus.** Nothing
here varies it, and `#2397` recorded that a coordinate observed with one value
is not thereby an instruction to vary it.

**That the forms are the remaining explanation.** The summary states why: two
explanations were offered, one is refuted, and the pair was never shown
exhaustive.

**That the grammar corpus's arrangements are non-immediate.** §3 records this
as the unmeasured step the hypothesis needs.

**That the forms are wrong.** They separate one source cleanly. A measurement
family that exposes some structure and not other structure is doing what a
bounded measurement does.

**That density never matters.** It establishes that density does not account
for *this* difference, at these two slices.

**That the thesaurus result is large.** Five overlaps. What makes it evidence
remains the shuffled comparison returning zero with more candidates.

**That either source lacks structure.** Neither claim is available. `#2395`
already recorded that a measurement failing to distinguish ordered from
shuffled material establishes nothing about the material.
