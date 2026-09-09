# Occurrence-position Measurement binding-occurrence subtraction report 001

## Question

Does occurrence-position Measurement require a separate binding occurrence
before its Measurement Act, or can the Act occurrence carry the exact binding
coordinates?

## Prior shape

The live road recorded:

```text
exact occurrence-position finding
        ↓
binding occurrence E
        ↓
Measurement Act occurrence A
        ↓
Measurement result occurrence R
```

`E` carried the exact source occurrences, source Locality, completeness
boundary, and the recording Locality cut. `A` referred to `E`; `R` copied the
binding reference. Current-coordinate reading then retained `E` because the
later readers had been authored to require it.

No prior Act, result, or relation occurrence independently produced `E` or
distinguished two otherwise equal binding occurrences.

## Falsifier

Remove only the separate binding occurrence and require the Measurement Act to
carry its exact binding coordinates directly:

```text
exact bounded source occurrences
+ exact source Locality
+ exact completeness boundary
+ exact recording Locality cut when present
+ Measurement
        ↓
Measurement Act occurrence A
        ↓
Measurement result occurrence R
```

Preserve:

```text
source Locality distinct from recording Locality
completeness boundary distinct from recording cut
completeness boundary before A
recording cut before A when present
A present while R is absent
one R per A
ordered result-position findings
current-coordinate replay
SQLite restart between A and R
changed subject, boundary, Locality, order, and result refusal
```

## Result

The separate event kind and every reference to it are absent. The active
console records `A` directly from the exact finding and current coordinates.
`A` now carries the binding coordinates; `R` addresses `A` by the actual Act
occurrence identity.

The former binding-only floor added no independent discriminator. Act without
result remains independently stoppable because `A` is itself an occurrence
and `R` remains a separate occurrence.

Moving the completeness boundary onto `A` exposed an order check that the
former wrapper had supplied accidentally. The Ledger now answers only whether
an exact append boundary precedes an exact occurrence. The SQLite form reads
the boundary and occurrence positions without decoding unrelated occurrence
material.

## Disposition

```text
exact subject-to-Act binding coordinates  retained on A
separate binding occurrence E             withdrawn
binding occurrence identity               withdrawn
binding reference on A                    withdrawn
binding reference on R                    withdrawn
actual Measurement Act occurrence A       retained
actual Measurement result occurrence R    retained
```

No new Book word, Act, result, relation, population, or completion occurrence
is introduced.
