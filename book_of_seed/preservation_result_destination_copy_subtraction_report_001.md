# Preservation result destination-copy subtraction report 001

## Question

Does the `06.Locality.C` relation result material need to repeat its
destination Locality when both the result occurrence and its exact Act
occurrence are recorded in that Locality?

## Prior shape

```text
Preservation Act A
    Event.locality_identity                 D

Locality relation result R
    Event.locality_identity                 D
    material.destination_locality_identity  D
    act_occurrence_event_identity            A
```

The result reader required the three destination coordinates to be equal.
The material field added a copy, not an independently variable destination.

## Falsifier

Remove only `R.material.destination_locality_identity`. Retain:

```text
R.locality_identity = A.locality_identity
R → exact A occurrence
readable result destination = R.locality_identity
```

Changing the result occurrence Locality away from the Act occurrence
Locality must still invalidate the relation.

## Result

The subtraction passes. The durable result material now contains only its
exact Act-occurrence reference:

```text
Locality relation result R
    Event.identity
    Event.locality_identity
    material.act_occurrence_event_identity
```

The result reader follows the Act reference to recover Preservation and Q,
validates the shared destination Locality and Act-before-result order, and
returns the exact through-Q boundary and destination coordinates.

```text
durable destination copy          absent
readable destination coordinate   retained
Act and result Locality equality  retained
```

No Act, result, Locality, Book coordinate, or admitted word is removed.
