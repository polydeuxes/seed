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

The Locality Standing projection nevertheless carried the Responsibility and
result in separate populations.  It did not carry the direct
`R -> Responsibility` coordinate required by the runtime recovery of
`01.Standing.A.1`.

`8d31f042` first repaired only that projection seam, but retained two
accommodations: `None` for unowned Yield results and silent exclusion of older
incomplete ownership references.  Both accommodations are removed here.

The subject, Act, result, Yield, and Book clause are unchanged.  Active
producers whose ownership references were incomplete now record the exact Book
clause and result boundary before their Acts.

## Recovered compression

The generic projection gate was named and implemented as though an exact
result necessarily carried raw bytes:

```python
type(event.exact_material) is bytes
```

That condition describes one result surface.  It does not establish
Responsibility ownership.

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

Whether the result carries exact bytes or other exact coordinates does not
change this test.

## Projection topology

One variable-coordinate Measurement result now occupies both exact carried
populations:

```text
measurement_occurrences[R]
    -> family-specific Measurement coordinates

exact_result_occurrences[R]
    -> exact Responsibility ownership reference
```

Applicability and Compare results likewise remain in their family populations
while also carrying the direct generic ownership coordinate.

The populations do not replace one another.  The Act-specific population
answers what exact result work was recorded.  The generic coordinate answers
which exact Responsibility owns that result.

## Exact absence and refusal

The positive A.1 population has one rule:

```text
exact Yield + complete exact Responsibility ownership
    -> result / owner coordinate

exact Yield + no recorded ownership
    -> absent from the A.1 population

recorded but incomplete ownership
    -> refusal
```

It stores no `None` compatibility value.  Act-specific availability does
not substitute for Responsibility ownership, and no missing ownership
coordinate is inferred or reconstructed.

The migrated active producers include exact-byte Measurement, byte-pair
Measurement, Assertion Locality movement, occurrence-position Measurement,
direct source-position Measurement, recurrent pair-position Measurement,
shared-position Measurement, addressed-coordinate determination, bounded
Compare roads, and recorded Standing-boundary roads.

Where one Responsibility declares more than one exact result, each Act carries
the same Responsibility identity, subject, and Book clause while naming its
own exact result boundary.  The Responsibility already carries that complete
bounded result population; the Standing reader does not choose or construct a
boundary.

## Proofs

The source-exhausted coordinate tests now establish for every produced
Applicability, Compare, coordinate-set Measurement, recurrence Measurement,
and corresponding-coordinate Measurement result:

```text
Act-specific population contains R
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

The direct source-position Measurement supplies the smallest migration proof.
It is present in `measurement_occurrences` and in
`exact_result_occurrences`, where the latter maps it to its complete exact
Responsibility ownership.

## Disposition

No Book or machine-grammar amendment is made.

`85e5a430` remains the source-driven producer checkpoint.  This change makes
the current-Standing projection state directly what that checkpoint's ledger
already establishes.

The bounded-literal contraction remains unimplemented.
