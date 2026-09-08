# Operator destination Locality Act source-Locality copy subtraction report 001

## Question

Must the `06.Locality.D` Act material copy the operator source Locality when
its exact operator material subject already occurs in that Locality?

## Prior shape

```text
Act operator material occurrence reference Q
Act operator_locality_identity              L

Q.locality_identity                         L
```

## Falsifier

Remove only `operator_locality_identity` from the Act material. Recover the
source Locality through the exact operator material occurrence `Q` and retain
the requirement that the exact source-cut occurrence belongs to that same
Locality.

Preserve:

```text
exact operator material subject Q
Q source Locality L
exact source cut B in L
Q at or before B and B before the Act
destination Locality
Locality Act and relation result
restart and current-coordinate replay
changed source-Locality refusal
```

## Result

The subtraction passes.

The Act reader follows `Q` and validates its exact source result. The source
Locality is `Q.locality_identity`. The exact source cut must still occur in
that Locality, so changing either addressed occurrence continues to refuse.

The relation result retains its source-Locality field for separate pressure.
Its writer and reader derive the expected value through the Act's exact
subject rather than depending on a copy on the Act.

## Disposition

```text
Act operator material subject          retained
source Locality through Q              retained
copied source Locality in Act material withdrawn
exact source cut                       retained
result source-Locality copy            unresolved
```
