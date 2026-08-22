# Variable-extent runtime and corpus observation 001

## Scope

This report gathers the variable-extent work performed after commit
`186aedb4`.

It records:

- two runtime performance corrections;
- a raw English-material observation;
- a target-free observation over the sixteen exact Book windows;
- the boundary that prevents the complete corpus road from being written to a
  durable ledger.

This report changes no Book chapter, witness grammar, runtime, or test.
The corpus-wide calculation was an observer calculation in `/tmp`; it did not
record Seed occurrences.

## Runtime corrections

### Bounded validation reuse

Commit `7834554b` (`Reuse bounded variable extent validation`) introduced a
call-local validation cache for already-validated coordinates and results
inside the exact bounded variable-extent advance.

Before that correction, recording `N` addressed position references repeatedly
resolved the complete direct-position result and scanned its coordinate
population from its beginning for every sibling reference. Measured scaling
was:

| addressed references | wall seconds |
|---:|---:|
| 63 | 0.128 |
| 127 | 0.368 |
| 255 | 1.220 |
| 511 | 4.403 |
| 1,023 | 16.626 |

At 218,057 references, that road projected approximately:

```text
23,774,754,710 assertion-identity resolutions
71,324,700,244 canonical JSON/hash operations
about 8.7 days of wall time
```

The cache is restricted to the exact recording call. Public resolution later
performs complete validation again, so mutation refusal remains active.

### Recording-copy reduction

Commit `2882c982` (`Reduce variable extent recording copies`) removed redundant
caller-side deep copies while preserving the independent copies made at the
durable event boundary. It also added exact latest-Locality event resolution to
the in-memory and SQLite ledgers so every Yield no longer constructs the
complete Locality event population merely to resolve its latest member.

The same four-line raw-material run retained exactly 16,341 events:

| revision | variable-extent seconds | corresponding-coordinate seconds |
|---|---:|---:|
| after `7834554b` | 13.040 | 2.030 |
| after `2882c982` | 6.423 | 1.673 |

The combined eight-line run completed with:

```text
raw bytes                         199
durable events                 45,984
variable-extent wall seconds   19.088
coordinate wall seconds         6.210
complete wall seconds          about 28
```

## Raw English-material observation

The first material supplied was:

```text
the cat jumped the fence
the dog jumped the gate
the fox jumped the wall
the cow jumped the ditch
```

No word, phrase, grammatical role, target value, or expected span was supplied
to the runtime.

At coordinate count eight, the runtime recorded:

```text
extent results                 76
internal result populations    21
recurrent result populations   11
recurrent productions          66
```

An internal same/different result population carried five exact supports:

```text
start  7   " jumped "
start 32   " jumped "
start 56   " jumped "
start 80   " jumped "
start 89   "he ditch"
```

The corresponding-coordinate Measurement then established every exact
coordinate/material recurrence in `" jumped "` with count four. Every such
finding carried the same exact support population at starts 7, 32, 56, and 80.
The fifth structurally matching support did not support those literal
findings.

Thus the current road performed two distinct contractions:

```text
internal same/different recurrence
↓
five source-derived supports

corresponding exact material recurrence
↓
four exact supports carrying " jumped "
```

A second four-line population using `crossed` established the exact
`" crossed "` support population with count four at coordinate count nine.
The combined eight-line run retained the `jumped` and `crossed` support
populations separately.

This does not establish that either literal material occupies the relation
content position of a relation Assertion. The smaller exposed vacancy is that
coordinate/material recurrence findings carry exact support production
references, while no current Responsibility groups the consecutive findings
that carry the same exact support population into an addressed bounded literal
result. The grouping above was observer rendering only.

## Target-free sixteen-Book observation

The observer loaded the same sixteen fixed 300-line windows used by the Book
material tests, in their fixed order:

```text
source count        16
exact byte count    218,058
```

It supplied no example phrase, expected value, role, span, or source-specific
filter.

The complete same-content/difference result population for an extent was
rendered compactly as the prior equal-byte coordinate for each source role.
That compact rendering is equivalent to the complete pairwise findings for
this exact byte surface; it does not add a relation or classification.

Only extents whose complete internal result population recurred were extended
by the next source-order coordinate. The calculation stopped when no recurrent
population remained.

| coordinate count | entering occurrences | recurrent occurrences | result populations | recurrent result populations | exact literal groups |
|---:|---:|---:|---:|---:|---:|
| 2 | 218,057 | 218,057 | 2 | 2 | 2,162 |
| 3 | 218,056 | 218,056 | 5 | 5 | 8,869 |
| 4 | 218,055 | 218,055 | 15 | 15 | 20,524 |
| 5 | 218,054 | 218,053 | 50 | 49 | 29,726 |
| 6 | 218,052 | 218,039 | 171 | 158 | 31,151 |
| 7 | 218,038 | 217,971 | 532 | 465 | 28,662 |
| 8 | 217,970 | 217,731 | 1,554 | 1,315 | 24,617 |
| 9 | 217,730 | 216,806 | 4,398 | 3,474 | 20,110 |
| 10 | 216,805 | 213,486 | 11,145 | 7,826 | 16,156 |
| 20 | 21,348 | 18,312 | 8,709 | 5,673 | 3,929 |
| 50 | 2,547 | 2,441 | 890 | 784 | 539 |
| 100 | 675 | 663 | 179 | 167 | 145 |
| 150 | 195 | 187 | 83 | 75 | 19 |
| 175 | 20 | 18 | 11 | 9 | 0 |
| 180 | 10 | 8 | 6 | 4 | 0 |
| 181 | 8 | 6 | 5 | 3 | 0 |
| 182 | 6 | 4 | 4 | 2 | 0 |
| 183 | 4 | 2 | 3 | 1 | 0 |
| 184 | 2 | 0 | 2 | 0 | 0 |

Complete observer calculation:

```text
next-coordinate extensions    3,339,588
last coordinate count               184
wall seconds                        6.63
```

No semantic target was required for the population to contract. The early
same/different surface is weak: nearly every source occurrence remains through
coordinate count nine. The population contracts sharply afterward and reaches
no recurrent result at coordinate count 184.

## Uncurated literal findings

Ranking exact literal recurrence only by support count produced formatting and
high-frequency corpus material first:

```text
count 6,020  coordinate count 2    "  "
count 5,011  coordinate count 2    "e "
count 4,200  coordinate count 2    line ending
count 1,352  coordinate count 5    " the "
count   820  coordinate count 5    " and "
```

At larger coordinate counts, repeated spaces and UTF-8 table-drawing material
from `cookbook_farmer.txt` dominated the support counts. The longest exact
literal recurrence had coordinate count 162, count two, and consisted of
repeated cookbook table formatting.

These are observer facts, not importance, meaning, relation roles, or Standing
strength.

## Durable event boundary

The current live variable-extent road records, for coordinate count `k`:

```text
k - 1 newly introduced Compare results
six lifecycle events per Compare result
three lifecycle events for the extent result
three lifecycle events for the recurrence Measurement at that coordinate count
```

For `N(k)` entering extent occurrences, its projected event count is:

```text
N(k) * (6 * (k - 1) + 3) + 3
```

Applying that exact current rendering to the complete target-free corpus
population projects:

```text
231,402,381 durable events
```

The durable corpus run was therefore not started. The observer calculation is
practical; the current event rendering is not.

This is no longer the previously corrected repeated-validation bottleneck.
Even with constant-time coordinate access and bounded validation reuse, writing
231 million exact lifecycle occurrences remains the dominant boundary.

## Verification

Focused variable-extent tests after both runtime corrections:

```text
tests/test_variable_extent_recurrence.py
5 passed in 18.23s
```

The focused tests preserve:

- exact result populations;
- branch-independent Yield;
- incremental Compare reuse;
- mutation refusal after the bounded recording call;
- complete corresponding-coordinate Measurement.

The broader `tests/test_events.py` run retained an unrelated active siren for
undeclared identity prefixes involving Candidate Applicability and ordered-path
source-position material. It was not changed by this work.

The complete operator-Locality Standing file also contains a separate slow
console test. It was not altered by these variable-extent corrections.

## Exact stopping boundary

```text
target-free corpus
↓
exact recurrence calculation completes in seconds
↓
3,339,588 source-derived extent occurrences
↓
current durable physiology would record 231,402,381 events
↓
STOP
```

No Candidate, Selection, ranking, semantic classification, grammatical role,
or expected literal value was introduced.
