# Locality continuation result-destination copy subtraction report 001

## Question

Must the `06.Locality.B` relation result material repeat its destination
Locality when the result and its exact Preservation Act occurrence both occur
there?

## Prior shape

```text
Preservation Act occurrence A
    Event.locality_identity = D

Locality relation result R
    Event.locality_identity                = D
    material.destination_locality_identity = D
    Act occurrence                         = A.identity
```

## Falsifier

Remove only the material destination copy. Preserve the exact event
Localities and require:

```text
R.locality_identity = A.locality_identity
```

## Result

The subtraction passes.

The result reader follows its exact Act occurrence, validates the shared
Locality, and returns `R.locality_identity` as the destination coordinate. A
result occurrence in a different Locality still refuses.

The durable result material is now:

```text
act_occurrence_event_identity = A.identity
```

Its other exact coordinates are recovered through the actual Act occurrence:

```text
R → A
A.act = Preservation
A → source Locality and source cut
A.locality_identity = R.locality_identity = destination
```

## Disposition

```text
result Event.identity                 retained
result Event.locality_identity        retained
actual Act-occurrence reference       retained
copied result destination             withdrawn
```

This closes copied-coordinate pressure on the `06.Locality.B` result.
