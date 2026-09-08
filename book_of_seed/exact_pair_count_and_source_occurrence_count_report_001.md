# Exact Pair Count And Source Occurrence Count Report 001

## Question

Does existing physiology distinguish:

```text
exact total pair occurrence count
exact source material occurrence count
exact recurrence result
```

or does recurrence compress those coordinates into one binary finding?

This report uses exact byte material only. It assigns no token, expression,
variable, rule, or semantic pattern to any supplied material.

## Boundary

`scripts/exact_material_distinctions_reading.py` runs each material population
in a separate `EventLedger`. Cross-reading comparisons use source occurrence
positions and exact result-local coordinates. Raw identities remain local to
their Ledger, and the reading appends no Seed occurrence.

No runtime, Book, grammar, Act, result, relation, or identity is added for the
experiments.

## Count three and count two

The first population is:

```text
A+B=C
D+B=E
F+B=G
```

The second is:

```text
A+B=C
D+X=E
F+B=G
```

In the first population, the exact pairs `(+, B)` and `(B, =)` each have:

```text
input count:               3
source occurrence count:   3
total count:               3
recurrence:                established
```

In the second population, each exact pair has:

```text
input count:               3
source occurrence count:   2
total count:               2
recurrence:                established
```

Recurrence therefore remains established while the exact count changes from
three to two.

The complete result populations are:

| Established surface | Same coordinates and content | Count-three content | Count-two content |
| --- | ---: | ---: | ---: |
| exact material results | 2 | 1 | 1 |
| byte Measurement result positions | 1 | 2 | 2 |
| pair Measurement result positions | 1 | 2 | 2 |
| pair Compare Applicability results | 2 | 0 | 0 |
| pair Compare results | 0 | 2 | 2 |
| ordered-path Compare Applicability results | 12 | 12 | 12 |
| ordered-path Compare results | 1 | 7 | 7 |
| Distinction Measurement results | 1 | 7 | 7 |

All 12 differing ordered-path Applicability result contents retain their exact
verdicts. No applicable coordinate becomes inapplicable, and no inapplicable
coordinate becomes applicable.

Three differing path Compare results address the changed source occurrence at
path positions `(0, 1, 2)`, `(1, 2, 3)`, and `(2, 3, 4)`. All four path Compare
results for the later source occurrence also differ because their producing
pair Compare addresses a different complete earlier pair population.

The corresponding three Distinction Measurement finding counts change from
`3, 4, 3` to `2, 2, 2`. The four later Distinction Measurements retain finding
counts `3, 4, 3, 2`, but their exact finding references differ inside their
different parent Compare results.

The count distinction therefore remains active after recurrence is already
established.

## Count two and count one

The second population above is compared with:

```text
A+B=C
D+X=E
F+Y=G
```

The exact pairs `(+, B)` and `(B, =)` move from:

```text
source occurrence count:   2
total count:               2
recurrence:                established
```

to:

```text
source occurrence count:   1
total count:               1
recurrence:                not established
```

The result populations are:

| Established surface | Same coordinates and content | Count-two content | Count-one content |
| --- | ---: | ---: | ---: |
| exact material results | 2 | 1 | 1 |
| byte Measurement result positions | 2 | 1 | 1 |
| pair Measurement result positions | 2 | 1 | 1 |
| pair Compare Applicability results | 2 | 0 | 0 |
| pair Compare results | 1 | 1 | 1 |
| ordered-path Compare Applicability results | 15 | 9 | 9 |
| ordered-path Compare results | 5 | 3 | 3 |
| Distinction Measurement results | 5 | 3 | 3 |

All nine differing Applicability result contents retain their verdicts. The
three differing path Compare results are the exact later paths containing or
meeting the replaced byte. Their Distinction Measurement finding counts change
from `3, 4, 3` to `2, 2, 2`.

This establishes the recurrence threshold separately from the count-three and
count-two distinction.

## Equal count in one or two source occurrences

A second control holds total pair count and recurrence exact while changing
only how those occurrences are distributed among source material results.

The first population is:

```text
A+B+B=C
D+E+F=G
```

The second is:

```text
A+B+E=C
D+B+F=G
```

In the final pair Measurement result of both Ledgers, the exact pair `(+, B)`
has:

```text
input count:  2
total count:  2
recurrence:   established
```

But the exact source occurrence count differs:

```text
first population:   1
second population:  2
```

The first population establishes count two and recurrence inside its first
material result. The second establishes count one after its first material
result, then count two and recurrence after its second.

The final aggregate count and recurrence are equal. The exact source
occurrence multiplicity and the earlier-to-later Measurement physiology are
not.

The result populations are:

| Established surface | Same coordinates and content | First content | Second content |
| --- | ---: | ---: | ---: |
| exact material results | 0 | 2 | 2 |
| byte Measurement result positions | 0 | 2 | 2 |
| pair Measurement result positions | 0 | 2 | 2 |
| pair Compare Applicability results | 1 | 0 | 0 |
| pair Compare results | 0 | 1 | 1 |
| ordered-path Compare Applicability results | 6 | 6 | 6 |
| ordered-path Compare results | 3 | 3 | 3 |
| Distinction Measurement results | 3 | 3 | 3 |

The six differing path Applicability result contents again retain the same
verdicts.

## Runtime spelling pressure

The live pair Measurement currently spells the exact source occurrence count
coordinate as:

```text
occurrences_carrying
```

This report does not admit or endorse `carrying` as grammar. The positive
physiology established here is narrower:

```text
exact number of pair occurrences
!=
exact number of source material occurrences
in which those pair occurrences exist
```

The distinction survives. The implementation spelling remains under lexical
pressure and can be reconciled separately without changing the result
physiology.

## Independent coordinates

The experiments jointly falsify three possible compressions:

```text
recurrence established
does not determine total count

total count
does not determine source occurrence count

source occurrence count
does not replace exact source occurrence references
```

The exact count-three and count-two results remain different even though both
establish recurrence. The equal-count distribution control remains different
even though both final results establish count two and recurrence.

No new multiplicity object is needed. Existing exact result content already
addresses each coordinate separately.

## Performance testimony

The two count-threshold cross-readings completed together in about 22 seconds.
The equal-count distribution cross-reading completed in about five seconds.
No cache, skipped validation, or runtime shortcut was introduced.

## Disposition

Exact pair multiplicity is not compressed into recurrence.

```text
exact total occurrence count
+ exact source occurrence count
+ exact recurrence finding
+ exact source occurrence references
→ independently addressable result content
```

The next constitutional question is not whether multiplicity exists. It is
whether the surviving general words `one`, `each`, `every`, and `both`
faithfully name the exact population physiologies in which they appear, or
compress different quantification shapes.
