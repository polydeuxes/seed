# Exact NC 012920.1 Material Boundary Report 001

## Question

What exact physiology changes when the same 24 ordered biological bytes are
supplied under different material occurrence boundaries?

The experiment compares:

```text
one occurrence
GATCACAGGTCTATCACCCTATTA

three occurrences
GATCACAG | GTCTATCA | CCCTATTA

three shifted occurrences
GATCAC | AGGTCTATCA | CCCTATTA
```

The concatenated 24 bytes are exact and equal in all three populations. Seed
receives no sequence, fragment, chromosome, adjacency, or biological-boundary
grammar.

## Biological source boundary

The material is the first 24 sequence characters of the human mitochondrial
reference sequence
[`NC_012920.1`](https://www.ncbi.nlm.nih.gov/nuccore/NC_012920.1?report=fasta):

```text
GATCACAGGTCTATCACCCTATTA
```

The accession and biological description are external laboratory testimony.
No Seed occurrence records or interprets them.

## Delimiter falsifier

The earlier biological-material experiment used newline bytes to provide three
operator material boundaries. Moving those boundaries would also move literal
newline content, so it could not isolate boundary physiology from content.

`scripts/exact_material_distinctions_reading.py` now provides an external
programmatic material source whose `readline()` returns each exact bounded
material without adding a delimiter byte. It uses the existing operator
console unchanged.

Focused controls establish:

```text
supplied material:  ab | cd
recorded material:  ab | cd
concatenated bytes: abcd
```

No newline or other delimiter enters exact material. The reading remains
external Witness machinery: it adds no Seed Act, result, relation, grammar,
kind, or runtime road.

## One occurrence and three occurrences

One bounded occurrence measures every adjacent pair among the 24 biological
bytes. It has 23 internal pair positions.

The `8|8|8` population has 21 internal pair positions. Exact material
boundaries prevent pair Measurement from manufacturing either cross-boundary
pair:

```text
position 7 G  | position 8 G   → GG not established
position 15 A | position 16 C  → AC not established
```

The exact pair results include:

| Pair | One occurrence count | `8|8|8` count | One occurrence recurrence | `8|8|8` recurrence |
| --- | ---: | ---: | --- | --- |
| `CA` | 3 | 3 | established | established |
| `GG` | 1 | 0 | not established | not established |
| `AC` | 2 | 1 | established | not established |

The same ordered biological bytes therefore do not establish the same pair
population under different occurrence boundaries.

The complete result populations are:

| Established surface | One occurrence | Three occurrences |
| --- | ---: | ---: |
| exact material results | 1 | 3 |
| byte Measurement results | 1 | 3 |
| pair Measurement results | 1 | 3 |
| pair Compare Applicability results | 0 | 2 |
| pair Compare results | 0 | 2 |
| ordered-path Compare Applicability results | 0 | 36 |
| ordered-path Compare results | 0 | 12 |
| Distinction Measurement results | 0 | 12 |

One material occurrence supplies only one pair Measurement result. The live
pair Compare road needs earlier and later Measurement results, so it does not
occur. The three-occurrence population supplies three cumulative Measurement
results and makes two pair Compares possible.

This is not evidence that the one-occurrence material lacks internal pair
content. It establishes that existing later Compare physiology is driven by
successive exact Measurement results, which in turn depend on exact material
occurrence boundaries.

## `8|8|8` and `6|10|8`

Both populations contain three exact material occurrences and concatenate to
the same 24 biological bytes. Their second boundary is the same. Their first
boundary differs:

```text
8|8|8
    omits global pair GG at positions 7 and 8
    omits global pair AC at positions 15 and 16

6|10|8
    omits global pair CA at positions 5 and 6
    omits global pair AC at positions 15 and 16
```

The exact final pair counts are:

| Pair | `8|8|8` count | `6|10|8` count | `8|8|8` recurrence | `6|10|8` recurrence |
| --- | ---: | ---: | --- | --- |
| `CA` | 3 | 2 | established | established |
| `GG` | 0 | 1 | not established | not established |
| `AC` | 1 | 1 | not established | not established |

The complete cross-reading produces:

| Established surface | Same coordinates and content | `8|8|8` content | `6|10|8` content |
| --- | ---: | ---: | ---: |
| exact material results | 0 | 3 | 3 |
| byte Measurement result positions | 2 | 1 | 1 |
| pair Measurement result positions | 0 | 3 | 3 |
| pair Compare Applicability results | 2 | 0 | 0 |
| pair Compare results | 0 | 2 | 2 |
| ordered-path Compare Applicability results | 23 | 13 | 13 |
| ordered-path Compare results | 2 | 10 | 12 |
| Distinction Measurement results | 2 | 10 | 12 |

The first byte Measurement result differs because the first bounded source has
six or eight bytes. The results through source positions 1 and 2 have the same
source-relative content: each addresses the same first 16 and complete 24
ordered biological bytes.

Pair Measurement does not converge. It measures pairs inside exact source
material occurrences and refuses to infer a pair across a material boundary.
The first missing pair therefore remains missing from every later cumulative
pair result.

Both pair Compare Applicability results remain the same. Both pair Compare
result contents differ because their complete pair populations differ.

Each population establishes 36 ordered-path Applicability results. Twenty-three
have the same exact coordinates and content. Thirteen differ on each side.
Nine differing results have shared source-relative coordinates, and none flips
its verdict.

The complete verdict populations differ because the middle material occurrence
has six path positions under `8|8|8` and eight under `6|10|8`:

```text
8|8|8:    12 applicable, 24 inapplicable
6|10|8:   14 applicable, 22 inapplicable
```

Those are different exact subject populations, not changed verdicts for one
shared coordinate.

The first boundary shape establishes 12 path Compare and Distinction
Measurement results. The shifted boundary establishes 14. Only two have the
same source-relative coordinates and content. The remaining result addresses
are exact under their own containing material occurrences and local positions.

## Boundary physiology

The experiment establishes:

```text
same concatenated ordered bytes
!=
same exact material occurrence population
```

and:

```text
same complete byte population through a boundary
does not establish
the same pair population through that boundary
```

Byte Measurement can reach the same source-relative result content after the
same complete biological prefix has been supplied across multiple occurrences.
Pair Measurement cannot reconstruct omitted cross-boundary adjacency from
those byte results.

That refusal is load-bearing. Creating `GG`, `CA`, or `AC` across a material
boundary would invent pair content that no exact source material occurrence
established.

## What is not established

The experiment establishes no:

- biological fragment or chromosome boundary;
- generic sequence object spanning material occurrences;
- pair or path relation across a material boundary;
- equivalence of one and three material occurrences;
- boundary-independent recurrence;
- cross-Ledger identity or Compare Act;
- new source, Measurement, Applicability, Compare, or Distinction kind; or
- owner of the positive Applicability-result to governed-Act crossing.

## Performance testimony

The one-versus-three and shifted-boundary cross-readings completed together in
about 27 seconds after the current-coordinate reuse at `c8357a4a`. The detailed
shifted-boundary reading completed in about 18 seconds. No cache, skipped
validation, or runtime shortcut was introduced.

## Disposition

Material boundary is an exact physiological coordinate, not laboratory
narration.

```text
same ordered biological bytes
+ different exact material boundaries
→ different established adjacency
→ different recurrence, Compare, and Distinction physiology
```

The first positive boundary-independent result is narrower: cumulative byte
Measurement content can converge after the same complete prefix. Existing pair
and path physiology correctly remains bounded by the exact material occurrence
that established it.
