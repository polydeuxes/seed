# Recurrent-result exact-material Measurement implementation 001

## Scope

This implementation adds one live Measurement and no Book clause.

The Measurement begins with results already produced from consecutive source
positions. It does not begin with requested material, a requested coordinate
count, a requested source position, or a requested value.

The caller gives every recurrence result the same work. Familiar material is
recognized only after the resulting occurrences have been frozen.

## Existing owner

Active `01.Source.D` already owns this work. It permits one declared
Measurement Responsibility with an exact subject and every required
coordinate. Its result must preserve the exact rule, subjects, source
occurrences, completeness boundary, findings, Authority, Scope, Locality,
limits, conflicts, and Unknown.

No new constitutional noun or Responsibility was required.

The exact Measurement rule is:

```text
one exact material at every corresponding source position
+ carried by exactly the same recurrent results
+ those results carry consecutive source positions
```

The rule establishes reusable exact material only. It establishes no word,
numeral, operator, expression, number, grammar, or meaning.

## Vocabulary correction

The first implementation named this work `BoundedLiteralMeasurement` and
recorded an ordinal as `coordinate_role`. Neither remained after review.

`Literal` added no distinction beyond:

```text
exact material
+ Measurement
+ exact source and result references
```

The runtime now names only those established coordinates.

`coordinate_role` added no coordinate at all. Each finding already carries the
exact source-position coordinate for every result that carries the finding.
The ordinal also collided with constitutional Act-local Role. It was removed
without a replacement. The exact sequence is recovered from the consecutive
source-position coordinates.

The two Compare Participation occurrences retain genuine Act-local roles:

```text
first subject
second subject
```

No compatibility reader or duplicate event name was retained.

The same review removed three inherited implementation containers from this
live road:

```text
ordered_coordinate_set
variable extent
Run
```

The first added a collection thing that the exact source-position coordinates
did not require. `ordered` repeated evidence already carried by the exact
source positions. `extent` and `Run` described observer mechanics rather than
Seed coordinates. The live module, event identities, readers, and proofs now
name source-position Measurement and recurrence directly. Consecutiveness is
validated from the exact source-position coordinates; it is not a new
constitutional object.

## Exact input

For one recurrent result the Measurement consumes:

```text
exact recurrence result reference
exact recurrence finding reference
exact supporting result references
exact corresponding-coordinate Measurement result reference
one exact recurring material finding for every corresponding source position
exact source-position coordinates carried by every supporting result
exact completeness boundary
Authority
Scope
Locality
limits
conflicts
Unknown
```

Every corresponding source position must have exactly one material finding
carried by all the same results. Matching counts or co-presence are
insufficient.

Every supporting result must carry the same material through consecutive
source positions. The result retains the exact supporting references and the
exact coordinate/material findings it consumed.

## Production

The live sequence is:

```text
exact corresponding-coordinate Measurement result
+ exact recurrent result
↓
01.Source.D Measurement Responsibility
↓
Measurement Act occurrence
↓ Yield
exact-material result W
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
→ exact supporting results

W
→ corresponding-coordinate Measurement result
→ exact material findings
```

It does not reconstruct the complete Locality to recover those already carried
coordinates.

## Positive witness

Input material:

```text
a+aa+a
```

The source-exhausted work produces every recurrent coordinate result it can
warrant. Every such recurrence result receives the same later Measurements.
No caller selects coordinate count three.

Post hoc, one recurrence finding carries exact results at source positions:

```text
0 1 2
3 4 5
```

Its corresponding findings carry:

```text
positions 0,3 → a
positions 1,4 → +
positions 2,5 → a
```

The new Measurement yields one exact reusable result carrying:

```text
a+a
```

The material, its coordinate count, its middle source positions, and `+` were
not supplied as selection criteria.

## Varying-material refusal

Input material:

```text
a+aa-a
```

The same complete same/different findings may recur. The corresponding source
positions do not carry one material across all exact results:

```text
source position 1 carries +
source position 4 carries -
```

The Measurement therefore yields neither common `a+a` nor common `a-a`
material for that recurrence finding.

## Mutation refusals

The result reader independently refuses changes to:

```text
supporting-result references
coordinate material
coordinate sequence
Responsibility ownership
Yield
```

Missing corresponding positions, multiple complete materials for one
position, non-consecutive source positions, incomplete ownership, and missing
producer references are also refusal conditions.

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
Responsibilities directly.

During the vocabulary correction, an older SQLite proof also reached the
55-second boundary. Its readers repeatedly validated the same referenced
results and then reconstructed the complete Locality, although the proof asked
only whether exact addressed results could be read after restart. Sharing the
validation already accepted by those exact readers and removing the unrelated
complete-Locality reconstruction reduced that proof to 15.28 seconds. The
separate ownership proof still validates direct `01.Standing.A.1` ownership.

## Coordinate not carried by the supporting results

Input material:

```text
xa+aa+a
```

The coordinate carrying `x` is not carried by either exact supporting result.
The results at positions `(1,2,3)` and `(4,5,6)` still yield the same exact
`a+a` material.

This exposes lexical pressure not resolved in this implementation:

```text
coordinate is carried by exact result
coordinate is not carried by exact result
```

The relation concerns one coordinate and one exact result; it is not an
intrinsic property named `internal`, `outside`, `in`, or `out`. The current
coordinates make the distinction measurable, but this implementation adds no
constitutional relation for it.

## Timings

Each new proof stays below one minute on the proving environment:

```text
source-exhausted recurrence proof              39.30 s
positive plus same-surface control             26.62 s
varying-material refusal plus mutations         25.09 s
SQLite readers and direct ownership             32.71 s
unrelated coordinate plus carried-result proof  25.16 s
```

## Exact stop

W is durable exact material, addressable by its result reference, and directly
owned in current Standing.

No later Responsibility currently takes W as its exact subject in this road.
No automatic uptake or general dispatcher was added. The next work begins only
when one exact existing or recovered Responsibility explicitly addresses W.
