# Compare-Distinction Measurement Act Locality-copy subtraction report 001

## Question

Must a Compare-Distinction Measurement Act occurrence repeat its source
Locality inside its material?

## Prior shape

```text
Act occurrence A.locality_identity = L
Act material.source_locality_identity = L
Act subject C.locality_identity = L
```

The material field copied the occurrence Locality. The Act reader already
requires the exact subject, current-coordinate reading, and Act occurrence to
address the same Locality.

## Falsifier

Remove `A.material.source_locality_identity` while preserving:

```text
A occurs in exact Locality L
subject C occurs in L
current-coordinate Locality = L
changed Locality refusal
Act-before-result order
current-coordinate replay
restart
```

## Result

The Act occurrence Locality remains the exact coordinate. The subject and
current-coordinate reader are validated against it. The material copy adds no
independently variable distinction.

## Disposition

```text
Act occurrence Locality         retained
subject Locality validation     retained
current-coordinate Locality     retained
copied Act-material Locality    withdrawn
```

No Locality, Act, result, binding occurrence, Applicability, Yield, or relation
is added.
