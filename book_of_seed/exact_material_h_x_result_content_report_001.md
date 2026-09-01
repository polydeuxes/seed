# Exact Material H/X Result Content Report 001

## Question

What exact established results differ when four independently bounded material
occurrences change only from:

```text
A+B=C
A+D=E
F+B=G
F+D=H
```

to:

```text
A+B=C
A+D=E
F+B=G
F+D=X
```

The experiment supplies no meaning for any byte. In particular, it does not
state that letters are variables, `+` is an operation, `=` is equality, or one
material occurrence is an expression.

## Boundary

`scripts/exact_material_distinctions_reading.py` runs each four-occurrence
population in its own `EventLedger`. Each run retains its raw occurrence and
result identities under its own exact reading. Those identities are provenance
inside that Ledger; the experiment does not compare identical identity strings
across the two Ledgers.

The cross-reading surface instead addresses established content through:

- source occurrence position in the supplied population;
- the complete ordered source population of one byte or pair Measurement;
- exact result-local position;
- exact finding category and finding position;
- exact ordered-path byte positions; and
- the earlier and later complete source populations of one pair Compare.

The reading snapshots the append boundary after existing physiology finishes
and refuses if any subsequent read appends a Seed occurrence. It introduces no
Act, result, relation, identity, grammar, or interpretation.

## Coordinate falsifier

The first attempted cross-reading addressed an ordered relation path only by
its source occurrence position. The full experiment refused that address:
multiple independently established paths exist inside one material result.

The exact path address therefore needs:

```text
source material result occurrence position
+ first byte position
+ shared byte position
+ last byte position
```

This is another positive instance of the recovered rule:

```text
exact containing occurrence
+ exact local structural coordinates
→ exact addressed content
```

No path identity or copied path content was added to make the two readings
comparable.

## Exact result

The complete reading produced these populations:

| Established surface | Same result coordinates and content | H content | X content |
| --- | ---: | ---: | ---: |
| exact material results | 3 | 1 | 1 |
| byte Measurement result positions | 3 | 1 | 1 |
| pair Measurement result positions | 3 | 1 | 1 |
| pair Compare Applicability results | 3 | 0 | 0 |
| pair Compare results | 2 | 1 | 1 |
| ordered-path Compare Applicability results | 48 | 0 | 0 |
| ordered-path Compare results | 10 | 2 | 2 |
| Distinction Measurement results | 12 | 0 | 0 |

The first three source results and their complete bounded Measurement results
are identical in content under the experiment coordinates. The fourth source
result differs exactly as `F+D=H\n` and `F+D=X\n`.

The fourth byte Measurement differs at the exact byte result whose subject is
72 (`H`) or 88 (`X`). The fourth pair Measurement correspondingly differs at
the exact pair subjects `(61, 72)` and `(72, 10)`, or `(61, 88)` and `(88, 10)`.
The earlier bounded byte and pair populations remain the same.

The third pair Compare result differs. The first two pair Compare results
remain the same. The finding populations retain the same category counts, but
their exact later-result subjects resolve to the H or X pair content above.

All 48 ordered-path Compare Applicability results remain the same, including
their positive and negative results. The material difference therefore does
not alter which already-bound subject configurations are applicable.

Ten ordered-path Compare results remain the same. The two results addressing
the final material paths differ: their exact pair subjects resolve through H
or X. No earlier path Compare result changes.

All 12 Distinction Measurement results have the same source-relative
structural content. That does not collapse their exact references. The final
two Measurements in each separate Ledger address exact findings whose resolved
pair subjects differ. The Measurement result preserves the exact references;
it does not copy the addressed finding content into another result.

## What is not established

The experiment does not establish:

- a semantic relation among `A`, `F`, `H`, or `X`;
- a token, variable, equation, substitution, or rule;
- a cross-Ledger identity;
- an Act that compares the two complete experimental populations;
- an owner of the positive Applicability-result to governed-Act crossing; or
- a new Yield occurrence.

The exact H/X distinction in this report is an external reading of two
separate Seed histories. Seed has not yet produced one internal result that
compares those complete histories.

## Performance testimony

The initial full H reading took 216.4 seconds because public byte, pair, and
ordered-path Applicability readers discarded already-supplied current
coordinates and reconstructed historical coordinates repeatedly.

Passing the exact current coordinates through the existing reader boundary
reduced the same H reading to 57.9 seconds without a cache, skipped validation,
or new runtime occurrence. The complete H/X counts-only reading then completed
in about 109 seconds.

This remains far above the earlier sub-one-second bounded experiments. The
remaining cost is a separate performance specimen; it is not evidence for a
constitutional object or permission to add a cache.

## Disposition

The controlled perturbation succeeds.

```text
one changed source byte
→ one changed bounded byte Measurement result
→ one changed bounded pair Measurement result
→ one changed pair Compare result
→ two changed ordered-path Compare results
```

while:

```text
pair Compare Applicability results          unchanged
ordered-path Compare Applicability results unchanged
Distinction Measurement reference shapes  unchanged
```

The next question is not what the symbols mean. It is whether existing
physiology can establish one internal Compare whose subjects are exact
Distinction Measurement results from independently bounded populations,
without using the external reading to select or interpret those subjects.
