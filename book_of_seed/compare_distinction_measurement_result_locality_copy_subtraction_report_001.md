# Compare-Distinction Measurement result Locality-copy subtraction report 001

## Question

Must a Compare-Distinction Measurement result repeat its source Locality inside
its material?

## Prior shape

```text
result R.locality_identity = L
result R.material.source_locality_identity = L
result R → Act occurrence A
Act occurrence A.locality_identity = L
```

The same Locality was serialized on the occurrence, copied into its material,
and recoverable through its exact Act occurrence.

## Falsifier

Remove the material copy while preserving:

```text
R.Locality = A.Locality
A.Locality = exact source Locality
changed R.Locality refusal
changed A.Locality refusal
current-coordinate replay
restart
complete findings
```

## Result

The result reader validates that R and A occur in the same exact Locality and
returns the source Locality recovered from A. The material copy adds no
independently variable coordinate.

## Disposition

```text
result occurrence Locality          retained
Act occurrence Locality             retained
Act-occurrence reference on result  retained
copied result-material Locality      withdrawn
```

No Locality, Act, result, binding occurrence, Applicability, Yield, or relation
is added.
