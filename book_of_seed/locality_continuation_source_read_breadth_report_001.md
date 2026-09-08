# Locality continuation source-read breadth report 001

## Question

Must reading an exact `06.Locality.B` source boundary enumerate every
occurrence in its source Locality?

## Prior read

The reader first obtained the addressed boundary occurrence and validated:

```text
boundary exists
boundary Locality = exact source Locality
boundary integrity is not corrupted
```

It then called `list_locality(source Locality)`, built a position dictionary,
and checked that the same boundary identity appeared in the returned events.

That second pass widened an exact identity question into a read of unrelated
occurrence material.

## Falsifier

Hold the exact source boundary fixed, add unrelated material in the same
source Locality, and forbid the broad Locality reader while recording and
reading the Preservation Act and relation result.

The exact source coordinate must remain readable through:

```text
ledger.get(boundary identity)
+ boundary.locality_identity
+ boundary integrity
```

Absent, different-Locality, and corrupted boundaries must continue to refuse.

## Result

The broad pass is unnecessary and has been removed.

Both in-memory and SQLite controls record and read the Act/result while a
test double makes any `list_locality()` call fail. The exact boundary
coordinate remains unchanged.

The correction does not weaken a boundary guarantee. `ledger.get()` already
requires the exact occurrence identity to exist in the Ledger, and the
reader separately validates its Locality and integrity.

## Disposition

```text
exact boundary occurrence read       retained
source Locality equality             retained
source boundary integrity            retained
broad source-Locality material read  withdrawn
unrelated material dependency        withdrawn
```
