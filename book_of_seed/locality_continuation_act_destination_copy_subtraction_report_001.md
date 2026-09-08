# Locality continuation Act-destination copy subtraction report 001

## Question

Must the `06.Locality.B` Preservation Act material repeat its destination
Locality when the Act occurrence itself occurs there?

## Prior shape

```text
Preservation Act occurrence A
    Event.locality_identity                D
    material.destination_locality_identity D
```

## Falsifier

Remove only the material copy. Preserve:

```text
fresh destination Locality D
A occurs in D
exact source Locality and source cut
Preservation
relation result occurs in D
Act-before-result order
restart and current-coordinate replay
changed destination refusal
```

## Result

The subtraction passes.

The exact destination is `A.locality_identity`. The result writer derives its
destination coordinate from that event coordinate, and the result reader
continues to require the result and Act to occur in the same Locality.

The source-coordinate reference remains on the Act because it is the exact
subject of Preservation, not a copy of the destination.

## Disposition

```text
destination as Act Event coordinate retained
destination copy in Act material  withdrawn
source-coordinate reference       retained
result destination copy           unresolved
```
