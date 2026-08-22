# Ordinary `!cat` sixteen-book recursive association observation 005

## Question

What does this Seed record when the sixteen exact 300-line Book windows cross
through a single ordinary `!cat` invocation after the bounded stdout value is
kept distinct from the provider's mechanical reads?

This observation follows runtime correction `7dec913b`. It changes no Book,
grammar, Measurement, Candidate, or Compare behavior. Two fresh SQLite ledgers
received the same 218,058-byte value.

## Direct finding

The provider performed four reads:

```text
[0, 65536)
[65536, 131072)
[131072, 196608)
[196608, 218058)
```

Those read occurrences remain carried by the exact stdout acquisition. Their
byte ranges, source boundaries, and invocation positions remain exact, and the
bytes of every read are recoverable from the addressed slice of the stdout
value.

The reads no longer become four material-acquisition subjects:

```text
four mechanical stdout reads
↓
exact 218,058-byte bounded stdout value
↓
Witness material acquisition
↓
218,057 adjacent-position findings
```

All three pairs formerly cut by the provider's 65,536-byte read request are
now present:

| join position | exact pair |
|---:|---|
| 65,536 | `An` |
| 131,072 | ` o` |
| 196,608 | `ow` |

The position population is therefore independent of this observed read
partition:

```text
218,058 bytes - 1 = 218,057 adjacent positions
```

## Input and preservation

The input remains the fixed population addressed by
`tests/book_material_test_witness.py`, concatenated in its declared order.

```text
source byte count       218,058
returned stdout bytes   218,058
SHA-256                  b008af6039e06b04ab66da39434bd37eee35471d884f4143b74c79efd0455eab
source windows matched  16 of 16
known loss              none
```

The observer's sixteen source ranges remain observation coordinates only.
They do not become acquisition boundaries. Every original range remains
recoverable byte-for-byte. All fifteen joins between adjacent source windows
and all three provider-read joins are included in the measured adjacent
position population.

## Invocation material

Each run supplied three exact material values to the invocation Locality:

| source boundary | bytes | mechanical reads | known loss |
|---|---:|---:|---|
| invocation output | 218,058 | 4 | none |
| invocation error | 0 | 0 | none |
| invocation completion | 0 | 0 | none |

The stdout acquisition carries these read coordinates:

| read boundary | invocation position | stdout range | bytes |
|---|---:|---:|---:|
| invocation output read 0 | 0 | `[0, 65536)` | 65,536 |
| invocation output read 1 | 1 | `[65536, 131072)` | 65,536 |
| invocation output read 2 | 2 | `[131072, 196608)` | 65,536 |
| invocation output read 3 | 3 | `[196608, 218058)` | 21,450 |

The read coordinates describe how the provider obtained the bounded value.
They do not establish separate material results.

The current ordinary host road remains bounded to 1 MiB. Material beyond that
boundary is carried as known loss. This correction neither raises that bound
nor claims that a much larger future material road should require the complete
value in memory.

## Measurement

The invocation Locality contains:

| population | count |
|---|---:|
| Witness acquisition results | 3 |
| material-to-this-Seed Locality relations | 3 |
| position-coordinate Measurement results | 3 |
| cumulative exact-byte Measurement results | 3 |
| Candidate results | 0 |
| Compare results | 0 |
| relation Standing | 0 |
| movement occurrences | 0 |

The nonempty stdout position result carries 218,057 findings. Empty error and
completion results each carry an exact empty position population.

Each cumulative exact-byte Measurement has 266 findings:

```text
134 count findings
131 recurrence findings
1 exact source-material-set finding
```

That population is unchanged from observation 004. The correction changes the
material boundary seen by position Measurement; it does not change the exact
bytes seen by cumulative byte Measurement.

## Durable population and time

Both fresh ledgers recorded the same event populations:

| coordinate | run 1 | run 2 |
|---|---:|---:|
| complete events | 75 | 75 |
| invocation-Locality events | 27 | 27 |
| console wall time | 1.4195 s | 1.4447 s |
| provider call | 1.1425 s | 1.1585 s |
| operator-Locality replay | 0.1244 s | 0.1240 s |
| invocation-Locality replay | 2.1352 s | 2.1450 s |
| final SQLite bytes | 491,520 | 503,808 |
| WAL/journal bytes | 0 | 0 |

No phase approaches the stated one-minute slow boundary.

Compared with observation 004:

| coordinate | before correction | after correction |
|---|---:|---:|
| stdout acquisition results | 4 | 1 |
| complete Witness acquisition results | 6 | 3 |
| invocation Measurement results | 12 | 6 |
| stdout adjacent-position findings | 218,054 | 218,057 |
| complete events | 108 | 75 |
| console wall time | 2.88–2.92 s | 1.42–1.44 s |
| invocation replay | 47.35 s | 2.14 s |
| SQLite bytes | 651,264–655,360 | 491,520–503,808 |

The reduced population is not discarded source material. It removes three
extra acquisition and Measurement lifecycles that existed only because the
provider requested at most 65,536 bytes from `os.read` at a time.

## Stopping boundary

The correction reaches Measurement and stops at the same later boundary:

```text
three exact Witness acquisition results
+ three material-to-this-Seed Locality relations
+ six Measurement results
↓
no Candidate result
no Compare result
no stronger structure
```

The experiment establishes that provider read partition no longer changes
Seed's adjacent-position findings. It does not establish the next responsible
road from these Measurement results into Candidate production.
