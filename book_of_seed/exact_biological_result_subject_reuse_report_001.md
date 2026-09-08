# Exact Biological Result Subject Reuse Report 001

## Question

Does existing Seed physiology already permit exact results to occupy later
exact subject positions repeatedly while preserving exact biological-material
provenance?

This is the constructive seam suggested by two external adversaries:

```text
minimal operation + repeated composition
exact material + exact provenance
```

Neither adversary is admitted as Seed grammar. Seed receives no NAND, Boolean,
logic, gate, DNA, nucleotide, sequence, locus, or biological interpretation.

## Material boundary

The experiment uses two overlapping 12-byte windows from the first 24
sequence characters of the human mitochondrial reference
[`NC_012920.1`](https://www.ncbi.nlm.nih.gov/nuccore/NC_012920.1?report=fasta):

```text
AGGTCTATCACC
ATCACCCTATTA
```

They are supplied as two exact material occurrences. The external overlap is
not a Seed coordinate or relation.

## Read-only construction

`scripts/exact_result_subject_reading.py` opens only already-established
results from the exact-material reading. For every Distinction Measurement
result, it resolves the exact references backward through:

```text
material result
↓
byte Measurement result
↓
pair Measurement result
↓
pair Compare result

material result
↓
position Measurement result positions
↓
ordered-path Measurement result position

pair Compare result
+ ordered-path Measurement result position
↓
path Compare result
↓
Distinction Measurement result
```

The reader creates no Seed occurrence, Act, relation, kind, constitutional
word, generic address object, or automatic next-operation mechanism.

Each reference is resolved through an existing exact result reader before the
external sequence is returned. A missing result occurrence, wrong result
position, malformed subject reference, absent material source, or malformed
ordered path is refused.

## Existing result reuse

The two supplied material occurrences establish:

```text
2  byte Measurement results
2  pair Measurement results
1  pair Compare result
20 ordered-path Measurement results
10 path Compare results
10 Distinction Measurement results
```

The exact earlier pair Measurement result addresses the source population:

```text
(material result 0)
```

The exact later pair Measurement result addresses:

```text
(material result 0, material result 1)
```

Those two Measurement results become the two exact subjects of one pair
Compare. Its exact result then becomes a subject in ten later path Compare
bindings.

This is real same-category reuse:

```text
Compare result
↓ exact later subject position
Compare
```

The pair Compare result does not become ten copied results. One exact result
occurrence is addressed by ten distinct later bindings, each beside one exact
ordered-path Measurement result position.

The resulting ten path Compare results each become the complete exact subject
of one Distinction Measurement:

```text
10 exact Compare result occurrences
↓
10 exact Measurement subject positions
↓
10 exact Distinction Measurement results
```

## Fan-out without provenance loss

The ten ordered paths used by the later Compare road are positions 0 through
9 of the second exact material occurrence:

```text
0  ATC
1  TCA
2  CAC
3  ACC
4  CCC
5  CCT
6  CTA
7  TAT
8  ATT
9  TTA
```

Each later Distinction result resolves through its producing path Compare to:

```text
one exact pair Compare result occurrence
one exact ordered-path Measurement result occurrence
one exact path result position
two exact position-Measurement result positions
one exact source material result occurrence
three exact source-local positions
```

The shared pair Compare result therefore supports fan-out without erasing the
different ordered-path subjects. The exact path subject supports later
Measurement without erasing its source material occurrence or local
positions.

This is the biological constraint on composition: later reuse preserves which
exact earlier occurrence and which exact local content participate.

## What has been built already

The live physiology already establishes multiple constructive steps:

```text
Measurement result becomes Compare subject
Compare result becomes later Compare subject
Compare result becomes Measurement subject
one result occurrence participates in several later bindings
every later result retains resolvable exact source coordinates
```

Rich domain meaning is not needed for those steps. The operations work over
exactly addressed results and positions.

## Where construction still stops

Result reuse does not resolve the frozen control vacancies.

The current operator console still invokes family-local host operations that:

```text
discover an exact prospective binding
record its Applicability lifecycle
record the governed Act occurrence after a positive result
```

No prior Ledger occurrence owns those crossings. An exact positive
Applicability result can remain current without the governed Act occurrence.

Therefore the experiment distinguishes:

```text
exact result can occupy a later exact subject position      established
exact result causes the later binding                       not established
positive Applicability causes the governed Act occurrence  not established
one generic self-composing operation                        not established
functional completeness                                     not established
```

The constructive substrate exists. Autonomous control closure does not yet
have exact physiology.

## NAND and DNA boundary

NAND supplies external testimony that a very small operation can support
unbounded construction when its results can enter later instances of that
operation.

DNA supplies external testimony that composition without exact occurrence,
position, boundary, and provenance can produce false identity and false copy
claims.

The current Seed result is their narrow admixture:

```text
later result reuse                         established
same-category Compare result reuse         established
exact provenance through every reuse       established
generic or autonomous compositional rule   not established
```

This report does not nominate Compare, Measurement, Applicability, or another
Act as a universal primitive.

## Validation

The focused exact-result and exact-material reading tests pass in about two
seconds. The two-window biological result-subject reading completes in about
five seconds. No cache, skipped validation, or new runtime road is used.

## Disposition

The next build should pressure control closure, not invent a richer content
vocabulary.

Exact result reuse already works. Any proposed growth must account separately
for:

```text
which exact existing occurrence establishes the next binding
which exact existing occurrence accounts for the governed Act occurrence
```

Until either occurrence is witnessed, the family-local host mechanism remains
external and the vacancies remain frozen.
