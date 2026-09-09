# Byte Measurement result completeness-boundary copy subtraction report 001

## Subtraction

The plain-byte Measurement result no longer copies its completeness boundary
at the top level.

Before:

```text
A.completeness_boundary_identity = B

R.act_occurrence_event_identity = A.identity
R.completeness_boundary.identity = B

R.result_positions[source-material-set]
    .dimensions.content.completeness_boundary.identity = B
```

After:

```text
A.completeness_boundary_identity = B

R.act_occurrence_event_identity = A.identity

R.result_positions[source-material-set]
    .dimensions.content.completeness_boundary.identity = B
```

## Surviving coordinates

The result addresses its exact Measurement Act occurrence. The Act retains the
completeness boundary used to read the source material. The exact
source-material-set finding independently retains that bounded-read coordinate.

Changing the finding boundary invalidates the result. Reintroducing the retired
top-level result copy is refused as an extra recording surface.

## Family boundary

This subtraction changes only the top-level plain-byte result material. It does
not remove the boundary from the Act, from the exact source-material-set
finding, or from any byte-pair Measurement family.

## Result

```text
completeness boundary on exact Act A          retained
bounded source-material-set finding           retained
top-level completeness boundary copied on R   removed
```
