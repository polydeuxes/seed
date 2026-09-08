# Locality continuation result-Act copy subtraction report 001

## Question

Must the `06.Locality.B` relation result repeat `Preservation` when it already
addresses its exact Act occurrence?

## Prior shape

```text
Preservation Act occurrence A
    act = Preservation

Locality relation result R
    exact_act = Preservation
    Act occurrence = A.identity
```

## Falsifier

Remove only the result's Act copy. Require result reading to follow `R → A`
and validate `A.act = Preservation`.

## Result

The subtraction passes.

The exact Act word remains on the Act occurrence. The result retains its exact
Act-occurrence reference, and changing the addressed Act invalidates result
reading. No Act distinction is lost by removing the second serialization.

## Disposition

```text
Preservation on Act occurrence retained
result → Act occurrence        retained
copied Act word on result      withdrawn
result subject and destination copies unresolved
```
