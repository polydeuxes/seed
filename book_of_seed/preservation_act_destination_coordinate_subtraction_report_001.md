# Preservation Act destination-coordinate subtraction report 001

## Question

Does the `06.Locality.C` Preservation Act material need to repeat its
destination Locality identity when the Act occurrence is recorded in that
exact Locality?

## Prior shape

```text
Preservation Act occurrence A
    Event.locality_identity             D
    material.destination_locality_identity D
```

The two coordinates could not vary independently. The Act reader required
the material field to equal the occurrence Locality that it used as the
expected value.

## Falsifier

Remove only `material.destination_locality_identity` from the Preservation
Act occurrence. Retain:

```text
Act                              Preservation
subject                          exact Q occurrence
through-Q boundary               exact Q occurrence reference
destination                      A.locality_identity
Act occurrence                   A.identity
result occurrence                separate exact event
```

Then require the result reader, current-coordinate replay, restart, changed
subject refusal, Act-before-result order, and one-result-per-Act refusal to
remain unchanged.

## Result

The subtraction passes. The destination is the Act occurrence's exact
Locality. The Locality relation result continues to address that destination
and the exact Act occurrence.

```text
A.locality_identity                         retained
A.material.destination_locality_identity    absent
result destination Locality coordinate      retained
```

This removes a copied coordinate. It does not remove or rename the
destination Locality, Preservation, the Act occurrence, or the result
occurrence. It authorizes no subtraction of the Act's subject or boundary
coordinates.
