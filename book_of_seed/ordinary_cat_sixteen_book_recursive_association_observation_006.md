# Ordinary `!cat` sixteen-book recursive association observation 006

## Question

What does this Seed record from the sixteen exact 300-line Book windows after
the live Witness road continues from exact-byte Measurement into byte-pair
Measurement without requiring a prior pair Compare premise?

This observation follows runtime correction `f9a9ec6c`. It changes no Book,
grammar, Candidate, Compare, recurrent-pair position Measurement, or corpus
material.

## Runtime correction

The console previously recorded byte-pair Measurement only in the branch that
already carried an earlier pair Measurement for later Compare. The correction
separates those acts:

```text
fresh exact-byte Measurement
↓
byte-pair Measurement

separately, where an earlier pair premise is already carried:
earlier pair Measurement + later pair Measurement
↓
Compare
```

A freshly recorded pair Measurement is not promoted into the later Compare
premise during the same console run. It also creates no recurrent-pair position
Measurement merely because recurrence was measured.

The same continuation now follows each freshly recorded Witness exact-byte
Measurement in the invocation Locality.

Focused witnesses establish:

```text
b"ab"
→ pair count for b"ab" = 1
→ no recurrence Assertion
→ no Compare

b"abxxab"
→ pair count for b"ab" = 2
→ recurrence Assertion for b"ab"
→ no Compare
→ no recurrent-pair position Measurement
```

The provider suite, the pair-association witnesses, the four-input incremental
Standing guard, and the existing carried-pair Compare/reopen road pass. The
four-input guard completes in 0.46 seconds after refusing the accidental
promotion of a fresh pair result into a Compare premise.

## Exact input

Both fresh SQLite runs used the same fixed corpus population addressed by
`tests/book_material_test_witness.py`:

```text
source windows                         16
lines addressed per source window     300
concatenated source bytes              218,058
returned stdout bytes                  218,058
source ranges recovered byte-for-byte 16 of 16
known loss                             none
```

The material crossed through a single ordinary `!cat` invocation. The provider
preserved four read occurrences inside the exact stdout acquisition:

```text
[0, 65536)
[65536, 131072)
[131072, 196608)
[196608, 218058)
```

Those read cuts remain transport coordinates. They do not split the exact
stdout material or its 218,057 adjacent positions.

## Durable populations

The two fresh ledgers recorded matching populations:

| recorded coordinate | run 1 | run 2 |
|---|---:|---:|
| complete events | 96 | 96 |
| Witness acquisition results | 3 | 3 |
| material-to-this-Seed Locality relations | 3 | 3 |
| invocation position-coordinate Measurement results | 3 | 3 |
| invocation exact-byte Measurement results | 3 | 3 |
| invocation byte-pair Measurement results | 3 | 3 |
| Candidate results | 0 | 0 |
| Compare results | 0 | 0 |
| recurrent-pair position results | 0 | 0 |
| assertion movement occurrences | 0 | 0 |
| relation Standing occurrences | 0 | 0 |

The operator Locality separately carries the command acquisition and its
existing Measurements. It does not supply the invocation material's pair
result or change the invocation counts above.

## Pair findings

The exact stdout pair result carries:

| finding | population |
|---|---:|
| adjacent positions in source material | 218,057 |
| observed exact two-byte values | 2,708 |
| count Assertions | 2,708 |
| recurrence Assertions | 2,162 |
| total pair Assertions | 4,870 |

The population agrees with the calculation made before the live continuation
was connected. The runtime now establishes those values through the actual
pair Measurement road.

The exact-byte Measurement is cumulative through its responsible boundary.
The later empty stderr and completion acquisitions therefore each produce a
later exact-byte result over the same 218,058 nonempty bytes. Each later result
currently proceeds through its own pair Measurement:

| acquisition boundary just recorded | pair count Assertions | recurrence Assertions |
|---|---:|---:|
| stdout, 218,058 bytes | 2,708 | 2,162 |
| stderr, 0 bytes | 2,708 | 2,162 |
| completion, 0 bytes | 2,708 | 2,162 |

The three pair results preserve different cumulative boundaries even though
their pair finding values match. This observation does not erase those
boundaries merely to reduce work.

Across durable occurrences, the ledger therefore carries 8,124 count
Assertions and 6,486 recurrence Assertions in three results. The structurally
distinct observed pair values remain 2,708, of which 2,162 recur in each
result.

## Acts after exact-byte Measurement

Each invocation exact-byte result proceeds through:

```text
pair-input Applicability Act and result
↓
pair Measurement Act occurrence
↓ Yield
pair Measurement result
```

The resulting invocation populations are:

| occurrence | count |
|---|---:|
| pair-input Applicability results | 3 |
| pair Measurement Act occurrences | 3 |
| pair Measurement Yield relations | 3 |
| pair Measurement results | 3 |

No later Act occurs from the 2,162 recurrence Assertions. In particular, the
runtime records no recurrent-pair position Measurement, Candidate Act, or
Compare Act.

## Time and ledger growth

| coordinate | run 1 | run 2 |
|---|---:|---:|
| corpus construction and verification | 0.127 s | 0.082 s |
| complete console | 38.151 s | 43.224 s |
| provider | 37.762 s | 42.759 s |
| stdout supply callback | 2.796 s | 3.078 s |
| empty stderr supply callback | 8.661 s | 10.348 s |
| empty completion supply callback | 26.303 s | 29.330 s |
| operator-Locality replay | 0.128 s | 0.132 s |
| invocation-Locality replay | 35.119 s | 35.423 s |
| console plus both replay reads | 73.398 s | 78.779 s |
| final SQLite bytes | 2,863,104 | 2,863,104 |
| WAL/journal bytes | 0 | 0 |

The repeated cumulative pair results dominate both console time and replay.
Their durable growth in run 1 was:

| callback | new events | SQLite bytes after | byte growth from prior boundary |
|---|---:|---:|---:|
| provider start | 0 | 94,208 | — |
| stdout | 18 | 1,167,360 | 1,073,152 |
| stderr | 18 | 2,019,328 | 851,968 |
| completion | 18 | 2,859,008 | 839,680 |
| final Representation/close | 6 | 2,863,104 | 4,096 |

No individual measured phase crossed the stated one-minute slow boundary.
The complete observation plus fresh invocation replay did cross a minute in
both runs. The cost is visible and repeatable, but removing distinct cumulative
results requires more than a performance preference. No performance change is
made in this observation.

## Repeatability

Both runs agree on:

```text
exact returned material
all sixteen source ranges
provider read ranges
event population by recorded kind
pair count population
recurrence population
later-Act population
Candidate population
Compare population
ledger byte count
stopping boundary
```

Generated occurrence references differ across fresh ledgers; no comparison
depends on their literal values.

## Exact stop

The live road now reaches the established recurrence distinction:

```text
exact stdout material
↓ exact-byte Measurement
2,708 observed byte-pair count Assertions
↓ exact count greater than 1
2,162 recurrence Assertions
↓
no live recurrent-pair subject continuation
no recurrent-pair position Measurement
no Compare
no Candidate
STOP
```

The focused repository witnesses already demonstrate how exact recurrence
Assertion references can become recurrent-pair subjects and later position
premises. The ordinary console does not invoke that continuation. This
observation does not connect it, route the corpus through the Cartesian
exact-result Candidate road, or infer a relation from recurrence alone.
