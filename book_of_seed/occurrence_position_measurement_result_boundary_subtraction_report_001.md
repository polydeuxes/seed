# Occurrence-position Measurement result-boundary subtraction report 001

## Question

Does an occurrence-position Measurement result need to repeat the completeness
boundary already carried by its exact Act occurrence?

## Prior shape

After the source-Locality copy was removed, the result still recorded:

```text
R.completeness_boundary = B
R.act_occurrence_event_identity = A
A.completeness_boundary_identity = B
```

## Falsifier

Remove only the boundary copy from `R`. Follow `R` to the exact Act occurrence,
recover its exact source Locality and completeness boundary, reconstruct the
expected finding, and compare the durable ordered result positions with that
finding.

Preserve:

```text
exact completeness boundary B
B before A
recording cut distinct from B
source Locality distinct from recording Locality
ordered result-position findings
A present while R is absent
one R per A
restart and current-coordinate replay
changed A.completeness_boundary_identity refusal
```

## Result

The completeness boundary remains exact through:

```text
R
→ exact Act occurrence A
→ A.completeness_boundary_identity = B
```

The result now durably carries only its exact Act-occurrence address and its
ordered position findings. A changed boundary on `A` still invalidates `R`.

## Disposition

```text
completeness boundary on A       retained
R → A occurrence address         retained
ordered position findings on R   retained
copied completeness boundary R   withdrawn
```

No Act, result, relation, boundary, identity, or admitted word is added.
