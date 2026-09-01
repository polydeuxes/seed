# Ordinary `!cat` sixteen-book single-batch observation 002

## Question

After raising the ordinary external Witness material boundary to 1 MiB, does
one `!cat` over the concatenated sixteen 300-line windows return the same exact
values as sixteen separate `!cat` invocations?

This observation also distinguishes equal returned bytes from equal durable
history and equal findings.

## Direct finding

The returned corpus value is exactly the same.

```text
sixteen source windows concatenated in addressed order
218,058 bytes

==

four exact output occurrences concatenated in occurrence order
218,058 bytes
```

Every original window also matches its corresponding byte range in the
returned value:

```text
(True, True, True, True,
 True, True, True, True,
 True, True, True, True,
 True, True, True, True)
```

The durable histories are not the same. The single batch records one operator
command, one invocation Locality, and four nonempty output acquisitions. The
separate road records sixteen of each command and invocation boundary, with
one nonempty output acquisition per window.

Both roads stop before corpus Measurement, so their current corpus finding
populations are equally empty:

```text
material-to-this-Seed Locality relations: 0
corpus Measurements:                    0
corpus Candidates:                      0
corpus Compare results:                 0
```

## Exact boundary change

The ordinary external Witness material byte limit changed from:

```text
65,536
```

to:

```text
1,048,576
```

The pipe read size remains 65,536 bytes. The material limit and one pipe read
are separate coordinates.

The focused provider checks establish:

- a finite 218,058-byte file crosses as four ordered occurrences whose sizes
  are 65,536, 65,536, 65,536, and 21,450 bytes;
- concatenating those occurrences reproduces the exact source bytes;
- no known loss is recorded for the finite file;
- an unbounded `/dev/zero` invocation stops after exactly 1,048,576 supplied
  bytes and records known loss at completion.

## Exact single-batch invocation

The sixteen addressed windows were concatenated without separators or other
inserted material and written to one temporary file. The operator console
received:

```text
!cat <one exact path>
```

The ordinary provider supplied:

| source boundary | occurrences | exact bytes | known loss |
|---|---:|---:|---|
| invocation output | 4 | 218,058 | none |
| invocation error | 1 | 0 | none |
| invocation completion | 1 | 0 | none |

The four output occurrence byte counts were:

```text
65,536
65,536
65,536
21,450
```

No output byte was written directly to the operator output boundary.

## Comparison with sixteen invocations

| coordinate | sixteen invocations | single batch |
|---|---:|---:|
| source windows | 16 | 16 |
| source bytes | 218,058 | 218,058 |
| returned bytes | 218,058 | 218,058 |
| exact window matches | 16 | 16 |
| elapsed time | 19.59 s | 0.52 s |
| operator commands | 16 | 1 |
| invocation Localities | 16 | 1 |
| nonempty output acquisitions | 16 | 4 |
| Witness acquisitions including empty error/completion | 48 | 6 |
| total ledger events | 726 | 60 |
| ledger bytes | 1,974,272 | 356,352 |
| operator command byte-pair position results | 16 | 1 |
| operator command exact-byte count results | 16 | 1 |
| operator Locality occurrence-position results | 16 | 1 |
| recorded Representation results | 65 | 5 |
| raw operator output bytes | 0 | 0 |
| corpus Locality relations | 0 | 0 |
| corpus Measurement results | 0 | 0 |
| corpus Candidate results | 0 | 0 |
| corpus Compare results | 0 | 0 |

The reduced time and ledger size follow the smaller command and invocation
population. They do not establish interchangeability between the histories.

## Value, finding, and history distinctions

### Returned value

The returned corpus bytes are equal. The operator's proposed expectation is
confirmed for exact returned material.

### Corpus findings

Both runs have no corpus findings because both stop at the missing
material-to-this-Seed Locality relation. Their present corpus finding
populations are therefore equal and empty.

### Operator findings

The operator-side findings are different. Sixteen commands produce sixteen
command Measurements of each active type; one command produces one of each.
The command bytes and their occurrence populations also differ.

### Durable history

The durable history is different. In particular:

```text
sixteen-invocation road
    each Book window is one nonempty output acquisition

single-batch road
    the concatenated byte value is divided at pipe-read boundaries
    into four nonempty output acquisitions
```

Those four boundaries do not preserve the sixteen Book-window boundaries.
The first three stop after 65,536 bytes; the last carries the remaining 21,450
bytes.

If later lawful uptake makes these acquisitions Measurement subjects, the
subject populations and boundary-local adjacency can differ even though the
concatenated byte value is equal. No current finding settles that future
comparison because neither road crosses the Locality prerequisite today.

## Exact stop

```text
one ordinary `!cat`
↓
218,058 exact returned bytes
↓
four exact output acquisitions in one invocation Locality
↓
bounded replay availability
X
no material-to-this-Seed Locality relation
no corpus Measurement
no stronger association pass
```

The single batch confirms equal returned corpus values while preserving the
distinct command, occurrence, and Locality histories for later responsible
work.
