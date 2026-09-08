# Exact NC 012920.1 Overlapping Material Report 001

## Question

What does existing Seed physiology establish when separate exact material
occurrences contain content read from overlapping regions of one external
biological reference?

The experiment supplies these 12-byte windows:

```text
GATCACAGGTCT
      AGGTCTATCACC
            ATCACCCTATTA
```

The spacing is external laboratory testimony. Seed receives three exact
material occurrences and no common-sequence, overlap, read, locus, copy,
fragment, chromosome, or biological grammar.

## Biological source boundary

The material is taken from the first 24 sequence characters of the human
mitochondrial reference
[`NC_012920.1`](https://www.ncbi.nlm.nih.gov/nuccore/NC_012920.1?report=fasta):

```text
GATCACAGGTCTATCACCCTATTA
```

The external offsets are:

```text
window 0: [0, 12)
window 1: [6, 18)
window 2: [12, 24)
```

Those offsets are not Seed coordinates. They are used only to construct and
cross-examine the supplied materials.

## Direct ordered-path reading

The experimental reader now exposes already-recorded ordered relation-path
Measurement results. It opens each exact result through the final current
coordinates. It does not add a Seed occurrence, kind, Act, relation, grammar,
or generic address object.

An ordered three-byte path remains addressed by:

```text
exact parent result occurrence
+ first position
+ shared position
+ last position
```

A focused control holds ordered path content and path count equal while
changing its exact source distribution:

```text
one material occurrence:   ATCATC
two material occurrences:  ATC | ATC
```

Both populations establish two `ATC` paths. The first population addresses
them at local positions 0 and 3 in one source material result. The second
addresses local position 0 in each of two source material results. Equal path
content and count do not collapse exact source occurrences.

## Equal `ATC` count, different provenance

The main control compares:

```text
one exact material occurrence:
GATCACAGGTCTATCACCCTATTA

two overlapping exact material occurrences:
AGGTCTATCACC | ATCACCCTATTA
```

Both supplied populations establish exactly two `ATC` ordered paths:

| Population | Source occurrence position | Local start position |
| --- | ---: | ---: |
| one occurrence | 0 | 1 |
| one occurrence | 0 | 12 |
| two occurrences | 0 | 6 |
| two occurrences | 1 | 0 |

Under the external reference offsets, the two paths in the first population
map to positions 1 and 12. The two paths in the second population both map to
position 12. Existing Seed physiology does not receive or reconstruct that
external mapping.

The pair Measurements provide an independent equal-count control:

| Pair | One occurrence total | One occurrence sources | Two occurrences total | Two occurrences sources |
| --- | ---: | ---: | ---: | ---: |
| `AT` | 3 | 1 | 3 | 2 |
| `TC` | 3 | 1 | 3 | 2 |

Both pairs establish recurrence in both populations. Equal aggregate count
and recurrence therefore remain distinct from the number and identities of
the exact source occurrences in which the pair positions exist.

## Three overlapping material occurrences

Supplying all three windows establishes 30 ordered paths. The exact repeated
content includes:

```text
ATC
    window 0, local position 1
    window 1, local position 6
    window 2, local position 0

AGG
    window 0, local position 6
    window 1, local position 0
```

External offsets map the final two `ATC` paths to the same reference position
12 and both `AGG` paths to the same reference position 6. Seed correctly
preserves five separate exact path occurrences because they occur in separate
supplied material results. It establishes no relation between their external
origins.

The final pair Measurement makes the effect especially sharp:

| Pair | One occurrence count | One occurrence sources | Three overlaps count | Three overlaps sources |
| --- | ---: | ---: | ---: | ---: |
| `AT` | 3 | 1 | 4 | 3 |
| `TC` | 3 | 1 | 5 | 3 |
| `AG` | 1 | 1 | 2 | 2 |
| `GG` | 1 | 1 | 2 | 2 |

`AG` and `GG` do not establish recurrence in the one-occurrence population.
They establish recurrence in the three-window population because the exact
pair content occurs in two supplied source occurrences. That recurrence is a
true result over the supplied material population. It is not a claim that the
external biological reference contains two copies at different positions.

## Established result surfaces

| Established surface | One occurrence | Two overlaps | Three overlaps |
| --- | ---: | ---: | ---: |
| exact material results | 1 | 2 | 3 |
| byte Measurement results | 1 | 2 | 3 |
| pair Measurement results | 1 | 2 | 3 |
| ordered relation-path Measurement results | 22 | 20 | 30 |
| pair Compare Applicability results | 0 | 1 | 2 |
| pair Compare results | 0 | 1 | 2 |
| ordered-path Compare Applicability results | 0 | 20 | 60 |
| ordered-path Compare results | 0 | 10 | 20 |
| Distinction Measurement results | 0 | 10 | 20 |

One complete material occurrence creates no successive pair Measurement
population for Compare. Multiple exact supplied occurrences make the existing
successive-result roads available. That difference is caused by the supplied
occurrence population, not by a conclusion about the external reference.

## Identity boundary

The experiment establishes:

```text
same exact ordered content
!=
same exact content occurrence
```

and:

```text
same aggregate count
!=
same exact source-occurrence distribution
```

It also establishes the narrower interpretation of recurrence:

```text
recurrence across exact supplied occurrences
does not establish
multiple underlying biological positions
```

Seed has exact testimony for content equality, local positions, parent result
occurrences, source occurrence identities, total counts, source occurrence
counts, recurrence, and downstream results. It has no testimony joining two
supplied content occurrences to one external biological position.

## What is not established

The experiment establishes no:

- biological read or overlap object;
- underlying locus identity or nonidentity;
- biological copy number;
- equivalence of one complete occurrence and overlapping occurrences;
- cross-occurrence path relation beyond already-recorded exact content;
- cross-Ledger identity or Compare Act;
- new Measurement, recurrence, Applicability, Compare, or Distinction kind; or
- owner of the positive Applicability-result to governed-Act crossing.

## Disposition

Existing physiology keeps apart three distinctions that external overlapping
reads can easily compress:

```text
equal content
separate exact supplied occurrences
external common origin
```

Only the first two are established by Seed. The third remains external
laboratory testimony.

The result gives the identity and multiplicity campaign a concrete biological
falsifier: `same`, `another`, and `separate` must always name the exact
coordinate under which equality, nonidentity, or independent occurrence is
established. None may silently stand for an unwitnessed external origin.
