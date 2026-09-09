# Compare-Distinction Measurement Act boundary-validation report 001

## Finding

The Act reader accepted supplied current coordinates when both append-order
checks refused. Its initial expected and observed values were empty tuples, so
the final comparison incorrectly treated:

```text
no exact order recovered
```

as:

```text
expected empty order recovered
```

Supplying prior coordinates also meant the Act's exact boundary was not
independently resolved or checked for integrity.

## Required positive coordinate

For exact Compare-result subject C, through-occurrence boundary B, and
Measurement Act occurrence A, the reader now requires:

```text
C = B and C < A

or

C < B < A
```

B must be an intact occurrence in A's Locality. B cannot be A.

## Adversaries

The native control covers memory and SQLite ledgers and all three entry points:

```text
Act reader
result writer
public result reader
```

Every entry point refuses B when it is:

```text
absent
ordered before C
in a different Locality
the A occurrence itself
ordered with A before B
corrupted
```

## Correction

The reader now resolves B, validates B's Locality and integrity, constructs the
exact permitted identity order, and requires the Ledger to return that order.
An order-check refusal immediately refuses the Act.

No withdrawn identity, binding occurrence, copied coordinate, or Act narration
is restored. The dead module-level `BOOK_CLAUSE` constant is also removed; the
event-kind declarations retain Book ownership.

## Disposition

```text
exact subject C                 retained
exact boundary B                retained and validated
exact Measurement Act A        retained
C ≤ B < A                       required
supplied-coordinate bypass     withdrawn
empty-order acceptance          withdrawn
```

The post-Locality census now correctly describes the downstream Distinction
result joint as read-only composition, not a later Act.
