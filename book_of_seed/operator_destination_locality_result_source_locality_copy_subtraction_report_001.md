# Operator destination Locality result source-Locality copy subtraction report 001

## Question

Must the `06.Locality.D` relation result serialize the operator source
Locality when that Locality is recoverable through its exact Act and subject?

## Prior shape

```text
R → A → Q
Q.locality_identity = source Locality L

R.material.operator_locality_identity = L
```

## Falsifier

Remove only the durable source-Locality copy from `R`. Preserve the exact
reference chain and return `L` from the validated operator occurrence when
reading the relation result.

## Result

The subtraction passes.

The result addresses its Locality Act occurrence. The Act addresses the exact
operator material occurrence. That occurrence's Locality is the source
Locality, and the Act reader separately requires its source-cut occurrence to
belong to the same Locality.

Thus:

```text
R → A → Q → source Locality L
```

remains exact without:

```text
R.material.operator_locality_identity
```

Downstream supplied-material validation continues to receive the source
Locality from the result reader. Restart, replay, and changed-coordinate
refusals remain unchanged.

## Disposition

```text
source Locality through exact subject chain retained
copied source Locality on result          withdrawn
destination Locality on result           unresolved
```
