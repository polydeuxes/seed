# Operator destination Locality Act-destination copy subtraction report 001

## Question

Must the `06.Locality.D` Act material repeat its destination Locality when the
Act occurrence itself occurs in that exact Locality?

## Prior shape

```text
Locality Act occurrence A
    Event.locality_identity              D
    material.destination_locality_identity D
```

Both coordinates were authored together and the reader required their
equality.

## Falsifier

Remove only `material.destination_locality_identity` from `A`. Preserve:

```text
fresh destination Locality D
A occurs in D
operator material subject
source Locality
exact source cut
Locality Act
relation result in D
restart and current-coordinate replay
changed Locality refusal
```

## Result

The subtraction passes.

The exact destination is `A.locality_identity`. The relation result recovers
that coordinate from `A` and continues to occur in the same Locality. A result
whose Locality differs from its Act still refuses.

The Act material no longer serializes a second copy of the destination.

```text
A.locality_identity                    retained
A.material.destination_locality_identity withdrawn
R.locality_identity                    retained
R.material.destination_locality_identity retained for separate pressure
```

The removal does not change destination allocation. Separate operator
material occurrences still receive separate Act occurrences and separate
destination Localities.

## Boundary

This result does not authorize removing the source cut from `A`.

The operator material occurrence may be followed by Measurement occurrences
before the Locality Act. Therefore:

```text
operator material occurrence Q
!=
exact source cut B
```

The Act must continue to address `B` unless another exact coordinate can
recover that same cut.

## Disposition

```text
destination Locality as Event coordinate retained
copied destination in Act material      withdrawn
source cut                              retained
result destination copy                 unresolved
```
