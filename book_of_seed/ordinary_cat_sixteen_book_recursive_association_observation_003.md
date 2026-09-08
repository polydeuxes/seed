# Ordinary `!cat` sixteen-book recursive association observation 003

## Question

What does this Seed presently do when the sixteen exact 300-line Book windows
cross through one ordinary `!cat` invocation, and how far does the existing
Measurement, Candidate, and Compare physiology proceed?

This observation changes no Book, grammar, provider, Measurement, Candidate,
Compare, or Locality behavior. The observer records existing calls, durable
event boundaries, elapsed time, and SQLite growth. The experiment uses the
already established 1 MiB external Witness material boundary.

## Direct finding

The complete 218,058-byte value crossed exactly. Every original window is
recoverable byte-for-byte from its addressed range in the returned value.

Seed then stopped before the first corpus Measurement:

```text
sixteen windows
↓ concatenate without inserted material
one 218,058-byte value
↓ ordinary `!cat`
four nonempty output occurrences
↓ Witness acquisition
four exact nonempty acquisition results
+ empty error result
+ empty completion result
↓ bounded invocation-Locality replay
no exact material --Locality--> this Seed relation occurrence
↓
no corpus Measurement result
no Candidate result
no Compare result
no later pass
```

The two fresh-ledger runs recorded the same returned bytes, source-range
matches, provider occurrence sizes, event populations, Measurement finding
populations, pass count, stopping boundary, and final SQLite size.

## Input and byte proof

The source population is the fixed population addressed by
`tests/book_material_test_witness.py`.

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

The pre-invocation proof was:

```text
sum of sixteen exact byte counts = 218,058
length of concatenated value      = 218,058

for every addressed range [start, end):
    batch[start:end] == exact source window

all sixteen comparisons           = true
SHA-256 of complete batch          =
b008af6039e06b04ab66da39434bd37eee35471d884f4143b74c79efd0455eab
```

Concatenation used the addressed order and inserted no separator. Equality of
all slices, equality of summed and final byte counts, and equality of the
returned complete value establish that construction introduced, removed, or
reordered no byte.

## Exact invocation and material boundary

Both runs used the same 70-byte command value:

```text
!cat /tmp/seed-cat-recursive-common-w1vdulut/sixteen-300-line-windows\n
```

The temporary pathname is an observer coordinate. The ordinary operator
console and ordinary host provider performed the invocation.

The provider supplied:

| source boundary | batch range | bytes | known loss |
|---|---:|---:|---|
| output occurrence 0 | `[0, 65536)` | 65,536 | none |
| output occurrence 1 | `[65536, 131072)` | 65,536 | none |
| output occurrence 2 | `[131072, 196608)` | 65,536 | none |
| output occurrence 3 | `[196608, 218058)` | 21,450 | none |
| error occurrence 0 | empty | 0 | none |
| completion | empty | 0 | none |

Concatenating the four output occurrences in occurrence order produced the
exact 218,058-byte input value in both runs. Every original window also
matched its exact range in each returned value. No corpus byte reached the raw
operator output boundary.

The provider read boundaries are not Book-window boundaries.

## Locality and Standing

The command and its three Measurement results occur in:

```text
sixteen-cat-batch-operator-locality
```

The invocation result establishes a new invocation Locality. The six Witness
acquisition results occur there. The generated address differed across the two
fresh runs, as permitted:

```text
run 1: operator_invocation_locality_000001
run 2: operator_invocation_locality_000002
```

The invocation-Locality bounded replay carried:

| carried population | count |
|---|---:|
| acquisition results | 6 |
| material-to-this-Seed Locality relations | 0 |
| Measurement results | 0 |
| Candidate results | 0 |
| Compare results | 0 |
| relation Standing | 0 |
| movement occurrences | 0 |

Availability of the six acquisition results in this replay established no
positive Standing and no material-to-this-Seed Locality relation.

## Pass observation

### Operator command work

Before the provider began, the operator command acquired three Measurement
results in the operator Locality. They concern the 70-byte `!cat` command, not
the returned Book material.

| Measurement result | exact findings |
|---|---:|
| byte-pair position | 69 position findings |
| exact-byte | 1 exact source-material-set, 25 counts, 18 recurrences |
| Locality occurrence-position | 20 position findings |

The two runs produced the same finding populations. The Measurement
lifecycles added 12 events. They did not make the later Witness material a
Measurement subject.

### Pass 0 — raw Witness material

| coordinate | observed value |
|---|---:|
| input value | 218,058 bytes |
| provider output occurrences | 4 |
| provider error occurrences | 1 empty occurrence |
| provider completion occurrences | 1 empty occurrence |
| Witness acquisition results | 6 |
| nonempty acquisition bytes | 218,058 |
| events added during provider supply | 18 |
| current Locality | invocation Locality |
| material-to-this-Seed Locality relation | 0 |
| relation Standing | 0 |

Each supplied occurrence produced an acquisition Act occurrence, Yield
relation occurrence, and acquisition result. Provider output occurrence 0
through 3 retained exact returned bytes; error and completion retained exact
empty values. Known-loss populations were empty.

After every acquisition the console invoked the existing declared Measurement
reader over the advanced bounded invocation-Locality replay. All six calls
returned an empty result population and added no event.

Therefore no later Responsibility became readable from the corpus under the
currently executed declared Measurement road.

### Pass 1 — first corpus Measurements

No corpus Measurement occurred.

Active `01.Source.D` requires, for material acquisition Measurement, the exact
material result, its Yield, and:

```text
exact material --Locality--> this Seed
```

The first two coordinates are preserved by Witness acquisition. The exact
Locality relation occurrence is not established. Bounded replay availability
does not establish it. This missing required coordinate is enough to refuse
the Measurement road; presence of that coordinate alone would not establish
every other required coordinate or Standing.

### Passes 2 and later

These passes did not begin:

| pass | required incoming result | observed incoming population | result |
|---|---|---:|---:|
| adjacent or relational Measurement | corpus Measurement result | 0 | 0 |
| Candidate | exact source result under its required coordinates | 0 | 0 |
| Compare | exact Candidate subject under its required coordinates | 0 | 0 |
| structures concerning prior structures | prior structured result | 0 | 0 |

There was no repeated recursive shape to record. The experiment produced raw
material availability and stopped before the first corpus finding.

## Original ranges and provider occurrences

The original sixteen ranges remain exactly recoverable from the returned
complete byte value. Seed does not carry those sixteen ranges as sixteen
Witness acquisition boundaries. Seed carries four nonempty provider output
boundaries.

Three original windows cross provider read boundaries:

| source | first part | second part |
|---|---:|---:|
| `boole_laws_of_thought.tex` | 2,809 bytes in output 0 | 9,712 bytes in output 1 |
| `latin_vulgate.txt` | 4,922 bytes in output 1 | 8,082 bytes in output 2 |
| `prose_emerson_essays.txt` | 8,830 bytes in output 2 | 10,534 bytes in output 3 |

Every other original window lies wholly inside one provider output occurrence.
Each provider occurrence contains material from several original windows.

The original ranges are observation coordinates only. No current Seed
occurrence gives them independent constitutional force. Because corpus
Measurement never begins, there is no result that spans, preserves, or loses
an original range boundary beyond exact recoverability from the returned byte
value.

## Timing

| phase | run 1 | run 2 |
|---|---:|---:|
| construct and verify batch | 0.1244 s | 0.1175 s |
| complete operator-console invocation | 0.5350 s | 0.5183 s |
| before provider entry | 0.2549 s | 0.2374 s |
| command Measurement work | 0.0994 s | 0.0902 s |
| complete provider call | 0.2543 s | 0.2548 s |
| six acquisition callbacks | 0.2516 s | 0.2522 s |
| provider time outside callbacks | 0.0027 s | 0.0026 s |
| six invocation-Locality Measurement attempts | 0.0087 s | 0.0090 s |
| after provider return | 0.0258 s | 0.0262 s |
| first-to-last durable event timestamp | 0.5275 s | 0.5106 s |
| construction plus console | **0.6594 s** | **0.6358 s** |

The provider invokes `cat` while supplying output through the callbacks, so
the complete provider duration is the exact external invocation boundary. The
time outside callbacks is not asserted to be pure process execution time.

No phase approached the one-minute slow boundary. The largest phase was the
provider call at about 0.255 seconds; nearly all of it was the six acquisition
callbacks and their bounded replay work. No performance correction or profile
was warranted.

## Ledger growth

Both fresh SQLite ledgers had the same sizes and event counts at every major
committed boundary:

| pass or boundary | input subjects | new events | cumulative events | DB bytes | delta bytes | run 1 wall time | run 2 wall time |
|---|---:|---:|---:|---:|---:|---:|---:|
| fresh ledger | 0 | 0 | 0 | 49,152 | — | — | — |
| command, command Measurements, invocation Locality | 1 command | 36 | 36 | 94,208 | 45,056 | 0.2549 s | 0.2374 s |
| Pass 0 Witness acquisition | 6 supplied occurrences | 18 | 54 | 344,064 | 249,856 | 0.2543 s | 0.2548 s |
| provider-return and console-close work | provider result / input end | 6 | 60 | 356,352 | 12,288 | 0.0258 s | 0.0262 s |
| Pass 1 corpus Measurement | 6 replay attempts | 0 | 60 | 356,352 | 0 | 0.0087 s within Pass 0 | 0.0090 s within Pass 0 |

The Pass 0 ledger growth was:

```text
18 events / 6 supplied occurrences = 3 events per supplied occurrence
249,856 bytes / 6 supplied occurrences = about 41,643 bytes per occurrence
```

The byte ratio is descriptive only. Four occurrences carry 218,058 material
bytes while two carry empty values, so it does not establish the same storage
cost for every result.

No WAL or journal file remained at the major committed boundaries or at
close. A 49,760-byte journal existed transiently while the command Measurement
batch was open; the committed database at provider entry contained those
events.

## Durable populations

Each run recorded 60 events:

| population | count |
|---|---:|
| Yield relation occurrences | 16 |
| Representation Act occurrences | 5 |
| Representation Locality occurrences | 5 |
| Representation results | 5 |
| Witness acquisition Act occurrences | 6 |
| Witness acquisition results | 6 |
| operator material acquisition coordinates excluding Yield | 5 |
| command Measurement coordinates excluding Yield | 9 |
| invocation-Locality coordinates excluding Yield | 3 |
| complete events | **60** |

The three command Measurement results are the only Measurement results. They
concern the operator command. Corpus Measurement, Candidate, Compare, and
movement populations are empty.

## Repeat-run comparison

| coordinate | run 1 | run 2 | comparison |
|---|---:|---:|---|
| input bytes | 218,058 | 218,058 | equal |
| returned bytes | 218,058 | 218,058 | equal to each other and input |
| original range matches | 16 | 16 | all true |
| output occurrence sizes | 65,536; 65,536; 65,536; 21,450 | same | equal |
| known loss | none | none | equal |
| total events | 60 | 60 | equal |
| event counts by durable kind | same | same | equal |
| command Measurement finding counts | 69 positions; 25 counts; 18 recurrences; 1 source set; 20 occurrence positions | same | equal |
| corpus Measurements | 0 | 0 | equal |
| Candidates | 0 | 0 | equal |
| Compare results | 0 | 0 | equal |
| passes reached | Pass 0 | Pass 0 | equal |
| final DB bytes | 356,352 | 356,352 | equal |
| console time | 0.5350 s | 0.5183 s | descriptive variation |

Generated invocation Locality references differ across runs. Literal equality
of generated references is not required for the observed structural and
population equivalence.

## Exact stopping boundary

```text
available subjects
    four nonempty exact Witness acquisition results
    empty error acquisition result
    empty completion acquisition result
    exact Yield coordinates
    exact invocation Locality

required next coordinate for material acquisition Measurement
    exact material --Locality--> this Seed relation occurrence
    plus every other exact Responsibility coordinate and Standing required
    by 01.Source.D

established
    exact returned material
    exact source boundaries
    exact known-loss populations
    exact Yield relations
    bounded invocation-Locality availability

not established
    material-to-this-Seed Locality relation occurrence
    positive relation Standing
    corpus Measurement Responsibility branch

STOP
```

The run establishes exact acquisition and exact preservation of the complete
batch. It establishes no association concerning the Book bytes. More passes
would require later responsible work not presently exposed by the established
coordinates; adding that work was outside this observation.
