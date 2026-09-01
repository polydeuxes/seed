# Repeated sixteen-book material Measurement observation 001

## Question

What changes when the same exact sixteen-book material crosses the ordinary
`!cat` Witness road twice into the same Seed ledger?

This observation follows runtime correction `6172c663`. It changes no Book,
grammar, Measurement finding rule, Candidate, Compare, or corpus material.

## Exact input

Both deliveries used the same command and the same concatenated material:

```text
source windows                     16
lines addressed per source window 300
exact returned bytes               218,058
known loss                         none
```

Each invocation preserved the returned bytes as an exact stdout value. The
provider read cuts remained coordinates of that value rather than material
boundaries.

## Correction

The live console now resolves the private exact-material storage reference of
each successful acquisition result. Before recording declared Measurement, it
recovers the exact-material references already addressed by validated exact-byte
Measurement results.

```text
new acquisition occurrence
↓
exact material reference already measured
↓
preserve the new acquisition and invocation history
do not repeat Measurement work
```

The storage reference remains implementation-only. It does not become Event
material or a Seed relation.

The in-memory ledger now resolves the same private reference from exact bytes;
SQLite continues to resolve its durable stored reference. A focused SQLite
witness retains `b"tatatata"`, the value used by the exact-material storage
witness, and proves:

```text
two deliveries
→ four distinct acquisition results
→ two stored exact values: command and payload
→ no second position, exact-byte, or byte-pair Measurement work
```

## Repeated corpus observation

| coordinate | first delivery | second delivery | second delta |
|---|---:|---:|---:|
| wall time | 11.755 s | 4.033 s | — |
| cumulative events | 81 | 120 | 39 |
| SQLite bytes | 2,023,424 | 2,072,576 | 49,152 |
| exact-material values | 3 | 3 | 0 |
| exact-material bytes | 218,122 | 218,122 | 0 |
| invocation Localities | 1 | 2 | 1 |
| Witness acquisition results | 3 | 6 | 3 |
| new position Measurement results | 3 | 0 | 0 |
| new exact-byte Measurement results | 3 | 0 | 0 |
| new byte-pair Measurement results | 2 | 0 | 0 |
| new Candidate results | 0 | 0 | 0 |
| new Compare results | 0 | 0 | 0 |

The second delivery added no Measurement, recurrence, Candidate, or Compare
event kind. It added the exact invocation, acquisition, Locality, and rendering
occurrences needed to preserve that the second delivery happened.

The 49,152-byte SQLite increase is therefore not another copy of the corpus or
its findings. Requiring zero total ledger growth would erase the second
occurrence. The exact byte store and every derived population remain unchanged.

## Finding

The live road now preserves both distinctions:

```text
same exact bytes
!= same occurrence

new occurrence
!= new Measurement work
```

Chronology no longer causes the same exact material to repeat position,
exact-byte, pair, count, or recurrence findings. The next stopping boundary is
unchanged: the existing live road records recurrence Assertions but performs no
later recurrent-pair position, Compare, or Candidate Act.

## Verification

Focused verification after the correction:

```text
36 passed in 3.40 seconds
```

The set includes the complete operator-host invocation suite, exact-material
storage, direct pair continuation, supplied Witness pair continuation, and the
bounded replay advance guard.
