# Recurrent bounded literal Measurement implementation 001

## Scope

This implementation adds one live Measurement and no Book clause.

The Measurement begins with results already produced by the source-exhausted
coordinate road. It does not begin with a requested literal, coordinate count,
coordinate role, or material value.

The proving caller gives every recurrence result produced by that road the same
work. The observer recognizes a familiar literal only after the resulting
events have been frozen.

## Existing owner

Active `01.Source.D` already owns this work. It permits one declared
Measurement Responsibility with an exact subject and every required
coordinate. Its result must preserve the exact rule, subjects, source
occurrences, completeness boundary, findings, Authority, Scope, Locality,
limits, conflicts, and Unknown.

No new constitutional noun or Responsibility was required.

The exact Measurement rule is:

```text
one exact material at every coordinate role
+ supported by exactly the same results
+ those results carry consecutive source positions
```

The rule establishes exact reusable material only. It establishes no word,
numeral, operator, expression, number, grammar, or meaning.

## Exact input

For one recurrent bounded result the Measurement consumes:

```text
exact recurrence result reference
exact recurrence finding reference
exact support-result references
exact corresponding-coordinate Measurement result reference
one exact recurring material finding for every coordinate role
exact source-position coordinates carried by every support result
exact completeness boundary
Authority
Scope
Locality
limits
conflicts
Unknown
```

Every coordinate role must have exactly one material finding supported by
exactly the same complete results. Matching counts or co-presence are
insufficient.

Every support result must carry the same material through consecutive source
positions. The result retains the exact support references and the exact
coordinate/material findings it consumed.

## Production

The live sequence is:

```text
exact corresponding-coordinate Measurement result
+ exact recurrent bounded result
↓
01.Source.D Measurement Responsibility
↓
Measurement Act occurrence
↓ Yield
exact bounded literal result W
```

The Responsibility is recorded before its Act. The Act points to that exact
Responsibility. The Yield points from the exact Act occurrence to W. Current
Standing carries W both as a Measurement result and through the direct
result-to-Responsibility ownership coordinate required by `01.Standing.A.1`.

The result reader follows the exact carried references:

```text
W
→ responsible Act
→ exact Responsibility

W
→ recurrence result
→ exact support results

W
→ corresponding-coordinate Measurement result
→ exact material findings
```

It does not reconstruct the complete Locality merely to recover those already
carried coordinates.

## Positive witness

Input material:

```text
a+aa+a
```

The source-exhausted road produces every recurrent coordinate result it can
warrant. Every such recurrence result receives the same later Measurements.
No caller selects coordinate count three.

Post hoc, one resulting recurrent structure has exact supports at source
positions:

```text
0 1 2
3 4 5
```

Its corresponding findings are:

```text
role 0 → a
role 1 → +
role 2 → a
```

The new Measurement yields one exact reusable result carrying:

```text
a+a
```

The literal, its length, its middle coordinate, and `+` were not supplied as
selection criteria.

## Varying-material refusal

Input material:

```text
a+aa-a
```

The same complete same/different surface may recur. Its middle coordinate does
not have one material finding supported by all exact support results:

```text
one support carries +
one support carries -
```

The Measurement therefore yields neither a common `a+a` nor a common `a-a`
result for that recurrent structure.

## Mutation refusals

The result reader independently refuses changes to:

```text
support-result references
coordinate material
coordinate-role sequence
Responsibility ownership
Yield
```

Missing roles, multiple complete materials for one role, non-consecutive
source positions, incomplete ownership, and missing producer references are
also refusal conditions.

## Durable recovery

The complete exact occurrences are written to SQLite in one bounded write.
After closing the store and opening the same path again, the reader recovers:

```text
the same exact W identity
the same exact a+a material
the same exact responsible Act reference
the same exact Responsibility reference
the same exact Responsibility subject
the same exact result boundary
```

The first restart proof exceeded four minutes because it reconstructed every
earlier source Measurement and current Locality to read one result. That was a
compression defect, not an acceptable test cost. The corrected reader validates
the exact referenced results, their Acts, their Yields, and their
Responsibilities directly. The bounded restart proof completes in about 25
seconds.

## Coordinate not carried by the support results

Input material:

```text
xa+aa+a
```

The coordinate carrying `x` is not carried by either exact support result. The two
supports at positions `(1,2,3)` and `(4,5,6)` still yield the same exact `a+a`
result.

This exposes lexical pressure not resolved in this implementation:

```text
coordinate is carried by exact support result
coordinate is not carried by exact support result
```

The relation concerns one coordinate and one exact support result; it is not an
intrinsic property named `internal` or `outside`. The current coordinates make
the distinction measurable, but this implementation does not add `in`, `out`,
or another constitutional relation.

## Timings

Each new proof stays below one minute on the proving environment:

```text
positive plus varying-material control       27.54 s
mutation refusals plus SQLite recovery        34.09 s
coordinate not in support plus Standing tests 26.64 s
```

## Exact stop

W is durable exact material, addressable by its result reference, and directly
owned in current Standing.

No later Responsibility currently takes W as its exact subject in this road.
No automatic uptake or general dispatcher was added. The next work begins only
when one exact existing or recovered Responsibility explicitly addresses W.
