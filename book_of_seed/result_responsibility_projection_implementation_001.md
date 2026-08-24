# Result / Responsibility projection implementation 001

## Boundary

`85e5a430` established a real durable production chain for the
source-exhausted coordinate road:

```text
exact Responsibility subject S
↓
Act occurrence
↓
Yield
↓
result R
```

The Act carried an exact reference to the Responsibility, so the ledger could
answer:

```text
R -> Act -> Responsibility -> S
```

The Locality Standing projection nevertheless carried the branch and result in
separate populations.  It did not carry the direct `R -> Responsibility`
coordinate required by the runtime recovery of `01.Standing.A.1`.

This change repairs only that projection seam.  It changes no producing Act,
result, subject, Responsibility, Yield, Book clause, or family-specific result
population.

## Recovered compression

The generic projection gate was named and implemented as though an exact
result necessarily carried raw bytes:

```python
type(event.exact_material) is bytes
```

That condition describes one result surface.  It does not establish branch
membership.

The repaired gate asks instead:

```text
intact result occurrence
+ exact Yield
+ exact responsible Act occurrence
+ complete exact Responsibility reference
+ exact referenced Responsibility
↓
direct A.1 result / owner coordinate
```

Whether the result carries exact bytes or structured coordinates does not
change this test.

## Projection topology

One variable-coordinate Measurement result now occupies both exact read-model
positions:

```text
measurement_occurrences[R]
    -> family-specific Measurement coordinates

exact_result_occurrences[R]
    -> exact Responsibility ownership reference
```

Applicability and Compare results likewise remain in their family populations
while also carrying the direct generic ownership coordinate.

The populations do not replace one another.  The family population answers
what exact result work was recorded.  The generic coordinate answers which
exact Responsibility branch owns that result.

## Exact absence

The older raw-byte road preserves this historical distinction:

```text
exact yielded bytes + exact owner
    -> result / owner coordinate

exact yielded bytes + no recorded owner
    -> None
```

`None` remains yielded-result availability without positive
subject-relative Standing.  This change does not reinterpret it.

A structured result without a complete five-coordinate Responsibility
reference is not inserted into the generic A.1 population.  Its existing
family population may still carry it under that family's own exact validation.
No missing branch coordinate is inferred or reconstructed.

This restraint matters because older structured Measurement roads still carry
three-coordinate assignment references.  They are not silently upgraded by
this change.  Migrating those roads, if warranted, is separate work.

## Proofs

The source-exhausted coordinate tests now establish for every produced
Applicability, Compare, coordinate-set Measurement, recurrence Measurement,
and corresponding-coordinate Measurement result:

```text
family population contains R
generic exact-result population maps R to owner
owner identifies the Responsibility occurrence
Responsibility subject equals the subject fixed before the Act
Responsibility result boundary equals R
```

The same direct associations survive SQLite close and reopen.

Independent mutations are refused:

- changing the Responsibility result boundary;
- changing the Yield occurrence coordinate;
- changing the yielded result's source coordinate.

The unchanged direct source-position Measurement supplies a negative control.
It remains present in `measurement_occurrences`, but because its older
Responsibility reference does not carry the complete generic ownership
coordinates, it is not manufactured into `exact_result_occurrences`.

## Disposition

No Book or machine-grammar amendment is made.

`85e5a430` remains the source-driven producer checkpoint.  This change makes
the current-Standing projection state directly what that checkpoint's ledger
already establishes.

The bounded-literal contraction remains unimplemented.
