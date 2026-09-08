# Operator destination Locality result-Act copy subtraction report 001

## Question

Must the `06.Locality.D` relation result repeat `exact_act = Locality` when it
already addresses its exact Act occurrence?

## Prior shape

```text
Locality relation result R
    exact_act                    Locality
    act_occurrence_event_identity A.identity

Locality Act occurrence A
    act                          Locality
```

## Falsifier

Remove only `R.exact_act`. Preserve the actual Act-occurrence reference and
require the result reader to follow it and validate `A.act = Locality`.

The subtraction must preserve:

```text
exact Locality Act
actual Act occurrence
separate result occurrence
Act-before-result order
one result per Act
operator subject
source cut
source and destination Localities
restart and current-coordinate replay
changed Act refusal through the result reader
```

## Result

The subtraction passes.

`R.act_occurrence_event_identity` addresses `A`. Reading `A` establishes its
exact Act coordinate as `Locality`. If that coordinate changes, both the Act
reader and the result reader refuse.

The result therefore does not need to serialize the Act word again.

## Disposition

```text
Act word on Act occurrence        retained
actual Act occurrence reference  retained
copied Act word on result         withdrawn
result subject and Locality copies unresolved
```
