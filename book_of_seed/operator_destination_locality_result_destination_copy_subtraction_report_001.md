# Operator destination Locality result-destination copy subtraction report 001

## Question

Must the `06.Locality.D` relation result material repeat its destination
Locality when both the result occurrence and its exact Act occurrence occur in
that Locality?

## Prior shape

```text
Locality Act occurrence A
    Event.locality_identity = D

Locality relation result R
    Event.locality_identity                = D
    material.destination_locality_identity = D
    material.act_occurrence_event_identity = A.identity
```

## Falsifier

Remove only the material copy from `R`. Preserve:

```text
R.locality_identity = D
R → A
A.locality_identity = D
exact operator subject and source cut
Locality Act
Act-before-result order
one result per Act
restart and current-coordinate replay
changed destination refusal
```

## Result

The subtraction passes.

The result reader requires `R.locality_identity == A.locality_identity` and
returns that exact event coordinate as the destination Locality. A relation
result moved to a different Locality continues to refuse.

The durable result material is now:

```text
act_occurrence_event_identity = A.identity
```

All other exact relation coordinates are recovered through the validated Act
occurrence and its subject:

```text
R → A
A → Q
A → exact source cut B
A.locality_identity = R.locality_identity = D
Q.locality_identity = source Locality
```

## Disposition

```text
result occurrence identity             retained
result Event Locality                  retained
actual Act occurrence reference        retained
copied destination in result material  withdrawn
```

This closes the copied-coordinate pressure on the active `06.Locality.D`
result. The exact source cut remains on the Act because it can differ from the
operator material occurrence.
