# Exact NC 012920.1 Material Result Content Report 001

## Question

Does the same existing Seed physiology distinguish two equal-sized byte
replacements at different exact structural positions in real biological
material?

Seed receives only exact bytes and material boundaries. It receives no DNA,
organism, nucleotide, gene, codon, reading-frame, biological function, or
mutation grammar.

## Biological source boundary

The laboratory material is the first 24 sequence characters of the human
mitochondrial reference sequence
[`NC_012920.1`](https://www.ncbi.nlm.nih.gov/nuccore/NC_012920.1?report=fasta):

```text
GATCACAGGTCTATCACCCTATTA
```

The experiment supplies those characters as three independently bounded exact
material occurrences:

```text
GATCACAG
GTCTATCA
CCCTATTA
```

Each supplied occurrence also ends with the newline byte used by the existing
operator material boundary. That byte is laboratory framing rather than one
of the 24 cited sequence characters. Seed nevertheless receives and measures
it as exact material. Both replacements in this report address internal
sequence positions, not the newline boundary.

The source accession and biological description are external laboratory
testimony. No Seed occurrence records or interprets them.

## Reading boundary

`scripts/exact_material_distinctions_reading.py` runs the original and replaced
materials in separate `EventLedger` histories. Exact identities remain local
to their own Ledger. The external comparison uses source occurrence positions
and result-local coordinates and establishes no cross-Ledger identity or
relation.

The reading begins after existing physiology finishes and appends no Seed
occurrence. No runtime, Book, grammar, Act, result, relation, or identity is
added for this experiment.

## Existing pair population

Before either replacement, the exact internal pair population includes:

```text
GA  count 1
CT  count 2, recurrence established
TC  count 3, recurrence established
AT  count 3, recurrence established
TA  count 3, recurrence established
```

The first control addresses the unique `GA` pair. The second addresses one
occurrence each of `TC` and `CT`, including the exact recurrence threshold for
`CT`.

Both controls replace their addressed byte with the same byte `A`.

## Source 0 position 0

The first control replaces:

```text
GATCACAG
AATCACAG
```

at this exact coordinate:

```text
source material result occurrence position 0
+ result-local byte position 0
```

The unique pair `GA` is replaced by the unique pair `AA`. No exact pair
recurrence is established or removed.

The complete result populations are:

| Established surface | Same coordinates and content | First content | Second content |
| --- | ---: | ---: | ---: |
| exact material results | 2 | 1 | 1 |
| byte Measurement result positions | 0 | 3 | 3 |
| pair Measurement result positions | 0 | 3 | 3 |
| pair Compare Applicability results | 2 | 0 | 0 |
| pair Compare results | 0 | 2 | 2 |
| ordered-path Compare Applicability results | 42 | 0 | 0 |
| ordered-path Compare results | 14 | 0 | 0 |
| Distinction Measurement results | 14 | 0 | 0 |

Every cumulative byte and pair Measurement differs because all three bounded
results include the exact first source occurrence. Both pair Compare results
therefore also differ as complete result content.

That upstream difference does not propagate into any later path result. All 42
ordered-path Applicability result contents, all 14 ordered-path Compare result
contents, and all 14 Distinction Measurement result contents remain the same
under the exact source-relative coordinates.

The changed source byte is outside the later added-source paths addressed by
those results, and its unique pair does not establish a recurrence finding used
by them.

## Source 1 position 2

The second control replaces:

```text
GTCTATCA
GTATATCA
```

at this exact coordinate:

```text
source material result occurrence position 1
+ result-local byte position 2
```

Its two adjacent ordered pairs change as follows:

```text
TC → TA
CT → AT
```

Through all three source occurrences, the exact pair counts become:

| Pair | First count | Second count | Recurrence after replacement |
| --- | ---: | ---: | --- |
| `TC` | 3 | 2 | established |
| `CT` | 2 | 1 | not established |
| `TA` | 3 | 4 | established |
| `AT` | 3 | 4 | established |

The replacement therefore preserves three recurrence results with different
exact counts while removing the exact `CT` recurrence result.

The complete result populations are:

| Established surface | Same coordinates and content | First content | Second content |
| --- | ---: | ---: | ---: |
| exact material results | 2 | 1 | 1 |
| byte Measurement result positions | 1 | 2 | 2 |
| pair Measurement result positions | 1 | 2 | 2 |
| pair Compare Applicability results | 2 | 0 | 0 |
| pair Compare results | 0 | 2 | 2 |
| ordered-path Compare Applicability results | 32 | 10 | 10 |
| ordered-path Compare results | 3 | 11 | 11 |
| Distinction Measurement results | 3 | 11 | 11 |

The byte and pair Measurement results through source positions 1 and 2 differ.
Both pair Compare results differ.

Ten ordered-path Applicability result contents differ, but every exact verdict
remains unchanged. No applicable coordinate becomes inapplicable, and no
inapplicable coordinate becomes applicable.

Eleven ordered-path Compare results differ:

```text
source occurrence position 1: path starts 0, 1, 2, 3
source occurrence position 2: path starts 0 through 6
```

The three unchanged paths in source occurrence position 1 start at positions
4, 5, and 6. They lie after the replaced byte and retain exact finding
references unaffected by the earlier changed pair population.

All seven later-source path Compare results differ because their producing
pair Compare addresses a different complete earlier pair Measurement result.
Several retain the same finding count while their exact categories or
result-local finding positions differ.

The same 11 source-relative Distinction Measurement results consequently
differ. Five change their exact finding count; the remaining six preserve their
count while their exact finding references differ.

## Same replacement, different physiology

The two controls use the same replacement byte and one exact changed source
position each:

```text
G → A at source 0, position 0
C → A at source 1, position 2
```

Their downstream results are not interchangeable:

```text
unique pair replaced by another unique pair
→ cumulative Measurement and pair Compare content differs
→ exact later path and Distinction content remains the same
```

```text
recurrent pair population changed
+ one recurrence result removed
→ cumulative Measurement and pair Compare content differs
→ exact later path and Distinction content differs extensively
```

The different consequence is established without a biological or semantic
importance coordinate. Exact source order, local position, pair content,
count, recurrence, and addressed later paths are sufficient.

## What is not established

The experiment establishes no:

- DNA or biological grammar inside Seed;
- nucleotide, gene, codon, reading-frame, or function coordinate;
- semantic interpretation of `A`, `C`, `G`, or `T`;
- biological effect or importance;
- cross-Ledger identity or comparison Act;
- new Measurement, recurrence, Applicability, Compare, or Distinction kind; or
- owner of the positive Applicability-result to governed-Act crossing.

## Performance testimony

Both complete biological-material cross-readings finished together in about
42 seconds after the current-coordinate reuse at `c8357a4a`. No cache, skipped
validation, or runtime shortcut was introduced. The earlier sub-one-second
bounded-experiment performance remains unrecovered.

## Disposition

The existing Seed physiology discriminates structural consequences in real
biological material without receiving a biological vocabulary.

```text
same replacement byte
+ different exact source occurrence and local position
+ different exact participation in recurring pair content
→ different exact downstream result content
```

This is domain transfer, not domain interpretation. The same machinery that
distinguished arbitrary and arithmetic-shaped bytes now preserves exact
position, recurrence, Compare, and Distinction consequences in a real human
mitochondrial reference sequence.
