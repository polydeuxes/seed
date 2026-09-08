# Operator destination Locality result-subject copy subtraction report 001

## Question

Must the `06.Locality.D` relation result copy the operator material occurrence
addressed by its exact Act occurrence?

## Prior shape

```text
Locality Act occurrence A
    operator material occurrence Q

Locality relation result R
    Act occurrence A
    operator material occurrence Q
```

## Falsifier

Remove only the durable `Q` copy from `R`. Preserve `R → A → Q` and return the
exact operator occurrence coordinate from that reference chain when reading
the result.

The subtraction must preserve:

```text
exact operator material occurrence
exact Locality Act occurrence
separate relation result occurrence
downstream supplied-material source references
changed subject refusal
equal-content occurrence non-collapse
restart and current-coordinate replay
```

## Result

The subtraction passes.

The durable result addresses `A`. The exact Act occurrence addresses `Q`.
Following those exact occurrence references recovers the same operator
material subject without serializing it twice.

Downstream supplied-material physiology continues to compare its supplied
operator occurrence with the exact coordinate returned by the relation
reader. That coordinate now comes through `R → A → Q`.

## Disposition

```text
operator subject on Act occurrence    retained
Act occurrence reference on result   retained
copied operator subject on result     withdrawn
derived result reading of subject     retained
```
