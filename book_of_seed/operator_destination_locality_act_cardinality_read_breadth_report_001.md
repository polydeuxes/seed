# Operator destination Locality Act-cardinality read-breadth report 001

## Question

Must enforcing one destination Locality Act per exact operator material
occurrence decode every occurrence in the Ledger?

## Prior read

Before recording a `06.Locality.D` Act for exact operator occurrence `Q`, the
writer called `list_events()` and decoded every Ledger occurrence. It retained
only destination Locality Act occurrences whose material addressed `Q`.

This widened a narrow cardinality question:

```text
destination Locality Act occurrences
+ exact addressed operator occurrence Q
```

into a read of unrelated occurrence material.

## Exact read

The two Ledgers now expose the identities of one exact occurrence kind in
append order. The durable implementation selects only the identity column; it
does not decode occurrence material.

The destination writer reads those exact Act occurrences and validates every
one before comparing its addressed operator occurrence with `Q`:

```text
identities of destination Locality Act occurrences
        ↓
every exact Act occurrence is validated
        ↓
an Act addressing Q means cardinality is already one
```

An occurrence of another kind is not part of that question. A malformed or
corrupted destination Locality Act occurrence cannot disappear from the exact
kind-identity read merely because its material would be inconvenient to read;
it is read and refused.

## Falsifier

For both in-memory and SQLite Ledgers:

```text
unrelated ordinary occurrences exist
global occurrence-material reading is forbidden
Q has no destination Locality Act
        ↓
the first exact Act occurs

the same exact Q is supplied again
        ↓
the second Act is refused
```

A separate Ledger control establishes that the kind-identity read crosses
Localities, retains append order, and returns no identity for an absent kind.

## Disposition

```text
one destination Locality Act per Q       retained
exact destination Act validation         retained
cross-Locality Act addressing            retained
unrelated occurrence-material decoding   withdrawn
global list_events dependency             withdrawn
```

No Book word, occurrence kind, Act, result, or Locality relation is added.
