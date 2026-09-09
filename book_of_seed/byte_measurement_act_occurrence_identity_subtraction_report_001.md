# Byte Measurement Act-occurrence identity subtraction report 001

## Question

Must a plain-byte Measurement binding mint a family identity for its future Act
occurrence before that occurrence exists?

The preceding pass removed only the prospective result identity. This pass is
independent and remains confined to plain-byte Measurement.

## Prior shape

The binding minted:

```text
act_occurrence_identity = prospective A*
```

The Act and result copied `A*`. Both also had the actual Act occurrence address
`A.identity`: the Act as its Ledger identity and the result through
`act_occurrence_event_identity`.

No occurrence was resolved through `A*`. Binding, Act, result, and current
coordinate readers compared copies originating in the same binding.

## Independent coordinates

The actual Act occurrence already carries the required distinctions:

```text
A.identity
A.kind = byte Measurement Act occurrence
A.locality_identity
A exact binding reference
A addressed exact Act
```

The result addresses `A.identity`. Act-before-result order and one-result-per-Act
cardinality are both checked with `A.identity`, not `A*`. Duplicate Acts for one
binding remain refused through the exact binding reference.

Downstream byte-pair Measurement and result-position Movement address:

```text
R.identity
+ exact result-local position
```

They do not use `A*`.

## Falsifier

Remove only `act_occurrence_identity` from the plain-byte binding, Act, result,
and their current-coordinate projections.

Retain:

```text
binding occurrence E
opaque exact Act identity
actual Act occurrence A
actual result occurrence R
exact source occurrence references
source Localities and completeness boundary
recording through-occurrence boundary
all byte count and recurrence findings
E before A before R
one result per A
restart and replay
corruption and coordinate-substitution refusal
downstream pair Measurement and Movement
```

The byte-pair family retains its independently untested
`act_occurrence_identity`.

## Result

Plain-byte Measurement remains exact through actual occurrence references.
Current coordinates carry `R.identity` and `A.identity`. Movement's source
coordinate reconstruction accepts the smaller plain-byte result while retaining
the larger byte-pair result shape.

The duplicate-Act and duplicate-result refusals remain keyed to the binding and
actual Act occurrence respectively. Equal findings in separate result
occurrences remain separate through their Ledger identities.

## Disposition

```text
prospective plain-byte family Act-occurrence identity   withdrawn
copied plain-byte Act-occurrence identity               withdrawn
actual Act occurrence identity                          retained
actual result occurrence identity                       retained
binding occurrence and opaque exact Act identity        retained
byte-pair lifecycle coordinates                         unchanged
```

No Act, result, relation, finding, Book clause, Witness Grammar coordinate, or
admitted word is added or removed.
