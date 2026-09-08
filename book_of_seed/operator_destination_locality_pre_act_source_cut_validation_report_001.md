# Operator destination Locality pre-Act source-cut validation report 001

## Finding

After the `06.Locality.D` binding occurrence was withdrawn, its Act writer
validated that the supplied current-coordinate boundary was a nonempty string
but did not validate the addressed occurrence before recording the Act.

The Act reader later refused an invalid source cut, leaving this sequence:

```text
invalid source cut B supplied
        ↓
Locality Act occurrence A recorded
        ↓
A cannot be read
        ↓
corrected retry refuses because Q appears to have an Act
```

The binding occurrence was not required. Its pre-Act validation was.

## Required coordinates

Before `A` occurs, the writer must validate:

```text
B is an exact Ledger occurrence
B is in Q's source Locality
B is intact
Q = B or Q occurs before B
```

These requirements come from the surviving exact `06.Locality.D`
coordinates. They do not restore a binding event.

## Correction

The writer and reader now share one exact source-cut validation:

```text
Q
+ source Locality
+ B
+ Q at or before B
```

The writer runs it before allocating the destination Locality and before
appending `A`.

The ordering question uses only exact occurrence identities. It does not read
unrelated occurrence material.

## Falsifier

Both in-memory and SQLite ledgers pressure four invalid boundaries:

```text
absent B
B before Q
B in a different Locality
corrupted B
```

For every case:

```text
writer refuses
no destination Locality Act occurrence exists
corrected exact coordinates can record A
```

The corrected retry control proves that failed validation does not poison the
operator occurrence with a phantom prior Act.

## Disposition

```text
separate binding occurrence        remains absent
pre-Act source-cut validation      restored
invalid Act occurrence             absent
corrected retry                     succeeds
exact Q/B order                    retained
```
