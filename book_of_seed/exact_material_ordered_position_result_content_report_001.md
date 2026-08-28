# Exact Material Ordered Position Result Content Report 001

## Question

What exact established results exist when four independently bounded material
occurrences place the same byte content in different local order?

```text
A+B=C
B+A=C
D+E=F
E+D=F
```

What differs when only the final material occurrence is instead:

```text
E+D=X
```

The experiment supplies no meaning for a letter, `+`, `=`, or one complete
material occurrence. In particular, it does not state a commutative,
arithmetic, expression, operand, result-side, reversal, or symmetry relation.

## Boundary

`scripts/exact_material_distinctions_reading.py` runs the first and second
four-occurrence inputs in separate `EventLedger` histories. Each Ledger retains
its own exact occurrence and result identities. The external reading compares
established content only through source occurrence positions and exact
result-local coordinates.

The read begins after existing Seed physiology finishes and appends no Seed
occurrence. It introduces no Act, result, relation, identity, grammar, or
cross-Ledger coordinate.

## Exact ordered positions

The first two material results establish:

```text
source occurrence position 0
    position 0  A
    position 1  +
    position 2  B
    position 3  =
    position 4  C
    position 5  newline

source occurrence position 1
    position 0  B
    position 1  +
    position 2  A
    position 3  =
    position 4  C
    position 5  newline
```

The third and fourth material results establish the corresponding exact
positions for `D+E=F\n` and `E+D=F\n`.

The containing material result occurrence remains part of every address.
Equal local integer positions in two results do not become one position.

The ordered relation-path results likewise retain their exact order:

```text
(A, +, B) != (B, +, A)
(D, +, E) != (E, +, D)
```

Both pairs occupy the same result-local position shapes `(0, 1, 2)`, but no
Seed result states that their byte populations are the same without order.
The existing physiology therefore preserves the exact ordered distinction and
does not manufacture a relation from the external arrangement.

## Exact recurrence boundary

The existing pair Measurement does establish exact recurring ordered pairs.
After the first two materials, `(=, C)` and `(C, newline)` each have count two
and an exact recurrence result position.

In the first four-material reading, `(=, F)` and `(F, newline)` also each have:

```text
input count:           4
occurrences containing: 2
count:                 2
recurrence:            established
```

In the second reading, each F pair has count one and no recurrence result
position. The exact X pairs `(=, X)` and `(X, newline)` each have count one.

This is the first distinction from the earlier H/X experiment. H had no prior
matching final pair to remove. Replacing the second F removes two exact pair
recurrences already established by the third material occurrence.

## Exact result content

The complete cross-reading produced:

| Established surface | Same result coordinates and content | First content | Second content |
| --- | ---: | ---: | ---: |
| exact material results | 3 | 1 | 1 |
| byte Measurement result positions | 3 | 1 | 1 |
| pair Measurement result positions | 3 | 1 | 1 |
| pair Compare Applicability results | 3 | 0 | 0 |
| pair Compare results | 2 | 1 | 1 |
| ordered-path Compare Applicability results | 42 | 6 | 6 |
| ordered-path Compare results | 8 | 4 | 4 |
| Distinction Measurement results | 8 | 4 | 4 |

The first three exact material, byte Measurement, and pair Measurement results
remain the same under the experiment coordinates. The fourth exact results
differ at F or X and at the two pair result positions addressing that byte.

All three pair Compare Applicability results remain the same. The third pair
Compare result differs because its later complete pair population no longer
contains the two repeated F pairs and instead contains two singly occurring X
pairs.

Six ordered-path Compare Applicability result contents differ. Their exact
verdicts do not: the same two are applicable and the same four are
inapplicable in both readings. The differing result content retains the exact
subject coordinates whose pair findings changed.

All four ordered-path Compare results for the final material occurrence differ.
The eight results for the earlier material occurrences remain the same.

All four Distinction Measurement results addressing those final path Compare
results differ. Their exact source-relative addresses remain:

```text
source occurrence position 3 + path positions (0, 1, 2)
source occurrence position 3 + path positions (1, 2, 3)
source occurrence position 3 + path positions (2, 3, 4)
source occurrence position 3 + path positions (3, 4, 5)
```

For the last two paths, the first reading has three and four exact findings;
the second has two and two. The first reading includes exact conflicting
findings established by the repeated F pairs. Those findings are absent when
the final material contains X.

## What is not established

The experiment does not establish:

- an unordered byte population;
- equivalence of the first and second material occurrences;
- equivalence of the third and fourth material occurrences;
- a reversal, commutative, symmetry, operand, or arithmetic relation;
- an internal comparison of the two complete four-material histories;
- a cross-Ledger identity or relation; or
- an owner of the positive Applicability-result to governed-Act crossing.

The statement that two path coordinates have the same local position shape is
external testimony. Seed establishes each exact containing occurrence, local
position, ordered content, recurrence, Applicability result, Compare result,
and Distinction Measurement result separately.

## Performance testimony

The complete two-Ledger reading took about 104 seconds. The result therefore
does not recover the earlier sub-one-second bounded-experiment performance.
This experiment adds no cache, skipped validation, runtime shortcut, or new
occurrence to hide that separate performance problem.

## Disposition

The ordered-position experiment succeeds without semantic grammar.

```text
same local position shape
+ different exact containing occurrence
+ different ordered byte content
→ separate exact addressed paths
```

and:

```text
two exact recurring F pairs
→ final F replaced by X
→ those recurrence result positions no longer exist
→ exact later Compare and Distinction content differs
```

Existing physiology preserves order and exact recurrence independently. It
does not yet establish the higher relation suggested by the authored material
arrangement.
