# Preservation Act append-boundary order scope report 001

## Finding

The binding-occurrence subtraction required the Preservation Act reader to
verify this positive coordinate:

```text
the exact append prefix through Act A contains subject Q
```

The first implementation asked for every Ledger occurrence through `A`, then
searched the returned events for `Q`. That read was broader than the exact
coordinate being validated.

## Failure

```text
unrelated occurrence R in another Locality
Q
Preservation Act A addressing Q
```

Reading `A` validated `A` and `Q`, then decoded `R` only because `R` occurred
within the same global append prefix. Unreadable material on `R` could
therefore block the valid read of `A`.

The order check also scaled with every occurrence through `A` rather than the
two exact identities under validation.

## Correction

Both Ledger implementations now answer the exact boundary question without
materializing occurrence payloads:

```text
append boundary through A
+ exact occurrence identity Q
        ↓
does that append prefix contain Q?
```

The in-memory Ledger compares stored append positions. The SQLite Ledger
compares the event row position with the boundary row position using
identity-only queries. Neither operation decodes unrelated event material.

The Preservation reader still refuses an exact `Q` recorded outside the
append prefix through `A`.

## Controls

```text
Q within boundary through A                 accepted
Q outside boundary through A                refused
absent occurrence identity                  not contained
unreadable unrelated occurrence before A    not read
in-memory and SQLite boundary behavior       equal
```

This is storage/addressing mechanics. It adds no Book coordinate, relation,
Act, result kind, or admitted word.
