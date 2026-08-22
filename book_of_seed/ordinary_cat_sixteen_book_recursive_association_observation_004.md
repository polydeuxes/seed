# Ordinary `!cat` sixteen-book recursive association observation 004

## Question

What does this Seed presently record when the sixteen exact 300-line Book
windows cross through a single ordinary `!cat` invocation after Witness
acquisition records the exact material-to-this-Seed Locality relation?

This observation changes no Book, grammar, provider, Measurement, Candidate,
Compare, or recording behavior. Two fresh SQLite ledgers received the same
218,058-byte batch. The observer recorded the supplied material, durable
occurrences, findings, elapsed time, and database growth.

## Direct finding

The acquisition correction opens the first corpus Measurement road:

```text
218,058 exact bytes
↓ ordinary !cat
four nonempty output occurrences
+ empty error occurrence
+ empty completion occurrence
↓
six Witness acquisition results
+ six exact material --Locality--> this Seed relations
↓
six position-coordinate Measurement results
+ six cumulative exact-byte Measurement results
↓
no Candidate result
no Compare result
no later structure
```

The two ledgers agree on all material bytes, source-range comparisons,
occurrence populations, finding populations, and the stopping boundary.

The four host output occurrences matter. Position-coordinate Measurement is
bounded by each acquisition result, so it records no adjacent position across
the three host read boundaries. The sixteen source-window ranges do not become
sixteen acquisition results.

## Input and byte preservation

The input is the fixed population addressed by
`tests/book_material_test_witness.py` in its fixed order. The ranges are the
same ranges established by observation 003:

| position | source | first line | batch range | bytes |
|---:|---|---:|---:|---:|
| 0 | `grammar_goold_brown.txt` | 6000 | `[0, 17298)` | 17,298 |
| 1 | `webster_dictionary.txt` | 6000 | `[17298, 25904)` | 8,606 |
| 2 | `roget_thesaurus.txt` | 6000 | `[25904, 45316)` | 19,412 |
| 3 | `grammar_kittredge.txt` | 6000 | `[45316, 55258)` | 9,942 |
| 4 | `algebra_rivenburg.txt` | 1800 | `[55258, 62727)` | 7,469 |
| 5 | `boole_laws_of_thought.tex` | 6000 | `[62727, 75248)` | 12,521 |
| 6 | `euclid_elements.txt` | 6000 | `[75248, 91262)` | 16,014 |
| 7 | `bash_abs_guide.txt` | 6000 | `[91262, 98596)` | 7,334 |
| 8 | `cookbook_farmer.txt` | 6000 | `[98596, 111247)` | 12,651 |
| 9 | `french_les_miserables.txt` | 6000 | `[111247, 126150)` | 14,903 |
| 10 | `latin_vulgate.txt` | 6000 | `[126150, 139154)` | 13,004 |
| 11 | `prose_austen_pride.txt` | 6000 | `[139154, 155430)` | 16,276 |
| 12 | `prose_dickens_copperfield.txt` | 6000 | `[155430, 170426)` | 14,996 |
| 13 | `prose_franklin_autobiog.txt` | 6000 | `[170426, 187778)` | 17,352 |
| 14 | `prose_emerson_essays.txt` | 6000 | `[187778, 207142)` | 19,364 |
| 15 | `prose_hume_enquiry.txt` | 6000 | `[207142, 218058)` | 10,916 |
| | complete population | | `[0, 218058)` | **218,058** |

Before each run:

```text
sum of source byte counts       = 218,058
concatenated value byte count   = 218,058
all sixteen addressed slices    = exact source bytes
SHA-256                         =
b008af6039e06b04ab66da39434bd37eee35471d884f4143b74c79efd0455eab
```

The returned output occurrences were identical in both runs:

| source boundary | batch range | bytes | known loss |
|---|---:|---:|---|
| output occurrence 0 | `[0, 65536)` | 65,536 | none |
| output occurrence 1 | `[65536, 131072)` | 65,536 | none |
| output occurrence 2 | `[131072, 196608)` | 65,536 | none |
| output occurrence 3 | `[196608, 218058)` | 21,450 | none |
| error occurrence 0 | empty | 0 | none |
| completion | empty | 0 | none |

The concatenated nonempty output occurrences equal the input value. Every
source window remains recoverable from its addressed range. No corpus byte
crossed the raw operator output boundary.

## Locality

The 70-byte `!cat` command and its three command Measurement results occur in
the operator Locality. The provider result establishes the invocation
Locality. The six Witness acquisitions, their six Locality relations, and the
twelve corpus Measurement results occur in that invocation Locality.

Fresh replay of each complete invocation Locality recorded:

| population | count |
|---|---:|
| acquisition results | 6 |
| material-to-this-Seed Locality relations | 6 |
| Measurement results | 12 |
| Candidate results | 0 |
| Compare results | 0 |
| relation Standing | 0 |
| movement occurrences | 0 |
| replayed invocation-Locality events | 48 |

The material remains in the invocation Locality. No movement or copy to the
operator Locality occurred.

## Pass 0 — Witness acquisition

Each supplied occurrence records its acquisition Act occurrence, Yield
relation, and exact material result. The result occurrence also records:

```text
exact material
--Locality-->
this Seed
```

The acquisition and relation preserve the Witness role, output/error/
completion boundary, invocation Locality, command and invocation provenance,
exact bytes, limits, and known loss.

## Pass 1 — declared corpus Measurements

Each acquisition result becomes a position-coordinate Measurement subject.
After every supplied occurrence, the exact-byte Measurement addresses the
complete acquisition-result population then available in the invocation
Locality.

| supplied boundary | material bytes | position findings | exact-byte findings | count findings | recurrence findings | source-set finding |
|---|---:|---:|---:|---:|---:|---:|
| output 0 | 65,536 | 65,535 | 199 | 100 | 98 | 1 |
| output 1 | 65,536 | 65,535 | 256 | 129 | 126 | 1 |
| output 2 | 65,536 | 65,535 | 263 | 132 | 130 | 1 |
| output 3 | 21,450 | 21,449 | 266 | 134 | 131 | 1 |
| empty error | 0 | 0 | 266 | 134 | 131 | 1 |
| empty completion | 0 | 0 | 266 | 134 | 131 | 1 |

The nonempty position results carry **218,054 findings**:

```text
65,535 + 65,535 + 65,535 + 21,449 = 218,054
```

A 218,058-byte value has 218,057 adjacent positions when treated as a single
subject. The difference is exactly three, matching the three boundaries
between the four host output occurrences:

```text
218,057 - 218,054 = 3
```

The original fifteen joins between Book windows all lie inside host output
occurrences, so position Measurement does cross those fifteen observation
ranges. The host read boundaries instead cut inside the Boole, Vulgate, and
Emerson windows. This run therefore establishes adjacent structures bounded
by acquisition occurrences, not by the observer's sixteen source ranges and
not by the complete concatenated value.

No later pass combines overlapping position findings into shared-position or
ordered-path results during this console road.

## Passes 2 and later

No Candidate, Compare, shared-position, ordered-path, or other result over the
corpus Measurement results occurred.

The executed road ends as follows:

```text
six acquisition results
+ six material Locality relations
+ twelve Measurement results
↓
no recorded relation Standing
no Candidate result
no Compare result
```

The console records its bounded post-provider output and returns. No currently
executed consumer takes the corpus Measurement results into Candidate
production. This observation does not decide whether that boundary is missing
law or a missing runtime call. It stops without adding either.

## Durable occurrences and database growth

Each supplied occurrence adds eleven events:

```text
3 acquisition events
+ 4 position-coordinate Measurement events
+ 4 exact-byte Measurement events
= 11 events
```

The complete ledger population is stable across both runs:

| durable population | count |
|---|---:|
| complete events | 108 |
| Yield relation occurrences | 28 |
| Witness acquisition Act occurrences | 6 |
| Witness acquisition results | 6 |
| position-coordinate Measurement assignments | 7 |
| position-coordinate Measurement Acts | 7 |
| position-coordinate Measurement results | 7 |
| exact-byte Measurement assignments | 7 |
| exact-byte Measurement Acts | 7 |
| exact-byte Measurement results | 7 |
| command occurrence-position Measurement coordinates excluding Yield | 3 |
| invocation-Locality coordinates excluding Yield | 3 |
| operator material-acquisition coordinates excluding Yield | 5 |
| Representation coordinates excluding Yield | 15 |

The seventh result in each Measurement population concerns the operator
command. The other six concern the Witness acquisitions.

| boundary | events | run 1 DB bytes | run 2 DB bytes |
|---|---:|---:|---:|
| fresh ledger | 0 | 49,152 | 49,152 |
| provider entry | 36 | 94,208 | 94,208 |
| output 0 complete | 47 | 208,896 | 208,896 |
| output 1 complete | 58 | 339,968 | 339,968 |
| output 2 complete | 69 | 454,656 | 454,656 |
| output 3 complete | 80 | 532,480 | 532,480 |
| empty error complete | 91 | 585,728 | 589,824 |
| empty completion complete | 102 | 647,168 | 651,264 |
| console complete | 108 | **651,264** | **655,360** |

The structural populations are equal. The SQLite files differ by a 4,096-byte
page. No WAL or journal remained at the committed observation boundaries.

## Timing and bottleneck

| phase | run 1 | run 2 |
|---|---:|---:|
| construct and verify batch | 0.1263 s | 0.0983 s |
| complete operator console | 2.8751 s | 2.9245 s |
| before provider entry | 0.2915 s | 0.2789 s |
| complete provider call | 2.5535 s | 2.6051 s |
| six supply callbacks | 2.5507 s | 2.6025 s |
| provider work outside callbacks | 0.0028 s | 0.0026 s |
| after provider return | 0.0300 s | 0.0405 s |
| durable first-to-last timestamp | 2.8678 s | 2.9101 s |

The callback duration grows as the carried acquisition and Measurement
population grows:

| callback | run 1 | run 2 |
|---|---:|---:|
| output 0 | 0.2385 s | 0.2618 s |
| output 1 | 0.3247 s | 0.3254 s |
| output 2 | 0.4113 s | 0.4095 s |
| output 3 | 0.4673 s | 0.4952 s |
| empty error | 0.5258 s | 0.5271 s |
| empty completion | 0.5831 s | 0.5835 s |

The live incremental road has no phase near one minute. A separate fresh
reconstruction check is the dominant observer cost:

| fresh replay | elapsed time |
|---|---:|
| operator Locality, 26 events | 0.1250 s |
| invocation Locality, 48 events carrying the corpus findings | **47.3454 s** |

The invocation reconstruction remains below the stated one-minute slow
boundary, so this observation makes no performance amendment. It is the clear
bottleneck if later work needs frequent fresh reads of this result population.

## Repeat-run comparison

| coordinate | run 1 | run 2 |
|---|---:|---:|
| input bytes | 218,058 | 218,058 |
| returned bytes | 218,058 | 218,058 |
| source-range byte comparisons | 16 true | 16 true |
| output sizes | 65,536; 65,536; 65,536; 21,450 | same |
| acquisition results | 6 | 6 |
| material Locality relations | 6 | 6 |
| corpus Measurement results | 12 | 12 |
| corpus position findings | 218,054 | 218,054 |
| final cumulative exact-byte findings | 266 | 266 |
| Candidate results | 0 | 0 |
| Compare results | 0 | 0 |
| total events | 108 | 108 |
| final DB bytes | 651,264 | 655,360 |
| console time | 2.8751 s | 2.9245 s |

Generated invocation-Locality references differ. Literal generated references
are not compared across fresh ledgers. Material, relations, population counts,
finding counts, and the stopping boundary agree.

## Exact stopping boundary

```text
available subjects
    six exact Witness acquisition results
    six exact material-to-this-Seed Locality relations
    six position-coordinate Measurement results
    six cumulative exact-byte Measurement results

recorded later work
    Candidate results        0
    Compare results          0
    shared-position results  0
    ordered-path results     0
    relation Standing        0

STOP
```

The experiment now establishes corpus findings. It does not yet establish a
recursive association pass over those findings.
