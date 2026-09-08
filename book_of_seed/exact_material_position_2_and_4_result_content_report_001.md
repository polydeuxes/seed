# Exact Material Position 2 And 4 Result Content Report 001

## Question

What exact established result content differs when the same four bounded
material occurrences receive one changed byte at two different exact source
positions?

The first material population is:

```text
2+2=4
2+3=5
3+2=5
3+3=6
```

The first comparison changes position 4 of source occurrence position 3:

```text
3+3=6
3+3=7
```

The second comparison changes position 2 of source occurrence position 2:

```text
3+2=5
3+8=5
```

The experiment supplies no meaning for a digit, `+`, `=`, one side of the
material, or one complete material occurrence. It does not state a number,
operation, equation, operand, answer, arithmetic rule, or mathematical
relation.

## Boundary

`scripts/exact_material_distinctions_reading.py` runs each first and second
material population in separate `EventLedger` histories. Raw identities remain
exact inside their own Ledger. The external reading compares established
content through source occurrence positions and exact result-local
coordinates; it asserts no identity or relation across Ledgers.

Each reading begins after the existing Seed physiology finishes and appends no
Seed occurrence. No Act, result, relation, grammar, token, or interpretation is
added for this experiment.

## Position 4 result

The first comparison replaces byte 54 with byte 55 at this exact address:

```text
source material result occurrence position 3
+ result-local byte position 4
```

The affected exact ordered pairs are:

```text
(=, 6)  and  (6, newline)
(=, 7)  and  (7, newline)
```

None of those four pair subjects has an exact recurrence result position in
its reading. The comparison therefore changes exact pair content without
removing an established recurrence.

The result populations are:

| Established surface | Same coordinates and content | First content | Second content |
| --- | ---: | ---: | ---: |
| exact material results | 3 | 1 | 1 |
| byte Measurement result positions | 3 | 1 | 1 |
| pair Measurement result positions | 3 | 1 | 1 |
| pair Compare Applicability results | 3 | 0 | 0 |
| pair Compare results | 2 | 1 | 1 |
| ordered-path Compare Applicability results | 48 | 0 | 0 |
| ordered-path Compare results | 10 | 2 | 2 |
| Distinction Measurement results | 12 | 0 | 0 |

Only the final bounded byte and pair Measurement results differ. Only the
third pair Compare result differs. The exact pair and path Applicability
results remain unchanged.

The two differing path Compare results address source occurrence position 3
at path positions `(2, 3, 4)` and `(3, 4, 5)`. Those are the two exact paths
whose ordered content includes source byte position 4.

All 12 Distinction Measurement result contents remain the same under the
source-relative experiment coordinates. Their exact references have the same
finding categories and positions even where those references resolve to a
different byte or pair subject in their separate Ledgers.

## Position 2 result

The second comparison replaces byte 50 with byte 56 at this exact address:

```text
source material result occurrence position 2
+ result-local byte position 2
```

Before that replacement, the exact ordered pairs `(+, 2)` and `(2, =)` each
occur in source material results 0 and 2. The pair Measurement results through
source positions 2 and 3 therefore each establish:

```text
count:      2
recurrence: established
```

After the replacement, each exact pair has count one and no recurrence result
position. The new exact pairs `(+, 8)` and `(8, =)` each have count one.

Because byte and pair Measurement results use the complete ordered source
population through their boundary, both the results through source position 2
and the later results through source position 3 differ.

The result populations are:

| Established surface | Same coordinates and content | First content | Second content |
| --- | ---: | ---: | ---: |
| exact material results | 3 | 1 | 1 |
| byte Measurement result positions | 2 | 2 | 2 |
| pair Measurement result positions | 2 | 2 | 2 |
| pair Compare Applicability results | 3 | 0 | 0 |
| pair Compare results | 1 | 2 | 2 |
| ordered-path Compare Applicability results | 33 | 15 | 15 |
| ordered-path Compare results | 8 | 4 | 4 |
| Distinction Measurement results | 8 | 4 | 4 |

All three pair Compare Applicability results remain exact and unchanged.
Fifteen ordered-path Compare Applicability result contents differ, but none of
their verdicts does. Every exact coordinate that was applicable remains
applicable; every exact coordinate that was inapplicable remains inapplicable.

The four differing ordered-path Compare results all address source occurrence
position 2:

```text
path positions (0, 1, 2)
path positions (1, 2, 3)
path positions (2, 3, 4)
path positions (3, 4, 5)
```

The first three paths include or meet pair content whose recurrence result was
removed. Their Distinction Measurement finding counts are:

| Path positions | First count | Second count |
| --- | ---: | ---: |
| `(0, 1, 2)` | 3 | 2 |
| `(1, 2, 3)` | 4 | 2 |
| `(2, 3, 4)` | 4 | 3 |
| `(3, 4, 5)` | 4 | 4 |

The fourth path retains the same ordered content `(=, 5, newline)` and the
same four finding categories. Its exact Distinction Measurement content still
differs because the finding positions are local coordinates inside the
complete parent pair Compare result. Removing earlier recurring-pair findings
changes those later local positions.

This is not a failure of the recovered address shape. It is positive testimony
for it:

```text
exact parent result occurrence
+ exact local finding category and position
→ exact addressed finding
```

When the complete parent result population differs, a later local finding
position can differ even when the finding it resolves has the same pair
subject and category.

## Exact positional distinction

The two byte replacements therefore establish different propagation shapes:

```text
source position 3, byte position 4
→ one later bounded Measurement pair differs
→ no recurrence result is removed
→ one pair Compare result differs
→ two path Compare results differ
→ Distinction reference content remains the same
```

```text
source position 2, byte position 2
→ two bounded Measurement pairs differ
→ two recurrence results are removed
→ two pair Compare results differ
→ four path Compare results differ
→ four Distinction Measurement results differ
```

The experiment does not label either source position with a semantic role.
The difference follows from exact source order, local byte position, pair
content, recurrence, and result-local finding coordinates already established
by Seed.

## Performance testimony

After current-coordinate reuse at `c8357a4a`, each complete two-Ledger reading
took about 26 to 28 seconds. The same H/X reading previously took about 109
seconds. No cache, skipped validation, or runtime shortcut was introduced.
The earlier sub-one-second bounded-experiment performance remains unrecovered.

## What is not established

The experiment establishes no:

- arithmetic or digit semantics;
- operand, operator, equality, or answer position;
- cross-Ledger identity or relation;
- internal comparison of complete material populations;
- new recurrence, Compare, Applicability, or Distinction kind; or
- owner of the positive Applicability-result to governed-Act crossing.

## Disposition

The exact source and local position of one byte materially changes how far its
existing recurrence and comparison physiology differs. Position alone does
not determine the result: the exact pair content and its already-established
recurrence coordinates are load-bearing.

The experiment therefore reaches a stronger domain-neutral statement than
"one position matters more":

```text
exact source occurrence
+ exact local position
+ exact ordered content
+ exact established recurrence
→ exact later result content
```
