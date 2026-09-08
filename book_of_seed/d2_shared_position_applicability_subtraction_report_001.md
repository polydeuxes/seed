# D.2 shared-position Applicability subtraction report 001

## Question

Does shared-position Measurement need a prospective Measurement binding and an
Applicability lifecycle when one exact D.2 result has already established the
two ordered result positions with one addressed source-position coordinate?

This report concerns only the D.2-derived road. The ordinary recurrent-result
road still admits pairs whose coordinates do not meet and retains its complete
positive and negative Applicability physiology.

## Former shape

```text
exact D.2 Determination result
        ↓
prospective shared-position Measurement binding
        ↓
Applicability binding
        ↓
Applicability Act
        ↓
applicable result
        ↓
shared-position Measurement Act
        ↓
Measurement result
```

The D.2 result already contains exactly two ordered result-position references.
Its own reader establishes that both references carry the one addressed exact
source-byte position-coordinate reference. Therefore the later shared-position
Applicability result cannot independently vary while the D.2 result remains
exact:

```text
exact D.2 result with two ordered references
        → one exact shared-position subject
```

The old D.2 orchestration could only record `applicable`. It did not admit an
exact D.2 result with those two references followed by `inapplicable`.

## Subtraction

The D.2-derived road now records:

```text
exact D.2 Determination result
        ↓
shared-position Measurement Act occurrence
        ↓
Measurement result occurrence
```

The Measurement Act records its exact subject coordinates directly:

```text
first exact result-position reference
second exact result-position reference
exact D.2 result reference
exact Measurement Act identity
Act occurrence identity
future result identity
Locality
through-occurrence boundary
```

The result directly addresses that Act and retains the exact D.2 result
reference. It contains no prospective binding reference and no Applicability
result reference.

## Preserved discriminators

Focused tests establish:

```text
exact two ordered D.2 result positions              preserved
one exact shared source-position coordinate         preserved
containing result occurrence for each position      preserved
exact D.2 provenance                                preserved
Locality and through-occurrence order               preserved
Measurement Act before result                       preserved
distinct Act / occurrence / result identities       preserved
one result per Act                                  preserved
durable restart                                     preserved
current-coordinate replay                           preserved
stale current coordinates                           refused
changed D.2 result                                  refused
intervening append or mutation before Act           refused
raw direct-result substitution                      refused
```

The exact D.2-derived lifecycle contains none of:

```text
shared-position Measurement binding occurrence
shared-position Applicability binding occurrence
shared-position Applicability Act occurrence
shared-position Applicability result occurrence
```

## Negative control

The ordinary recurrent-result road is unchanged. Two exact inputs whose source
position coordinates do not meet still establish:

```text
Applicability Act occurrence
        ↓
inapplicable result occurrence
        ↓
no shared-position Measurement Act
```

Thus the subtraction does not equate absence of Applicability with an
inapplicable result. Applicability remains real where the addressed exact
coordinates can produce either result.

## Finding

```text
Applicability forced after an already exact D.2 shared coordinate  not needed
Applicability over ordinary prospective recurrent inputs          preserved
binding coordinates of the D.2 Measurement Act                    established
separate D.2-derived binding occurrences                           not needed
```

Applicability is not a ceremonial stage between every exact subject and every
later Act. It occurs where an exact question remains. The D.2 result has
already answered the shared-coordinate question.

## Disposition

Accept the D.2-specific subtraction. Do not generalize it to mechanically
paired recurrent inputs or Compare inputs. Those roads still lack an earlier
exact occurrence that identifies one warranted pair, and their negative
Applicability results remain load-bearing.

The next pressure belongs one step earlier on the same internally produced
road: determine whether addressed-byte Determination Applicability can vary
independently when its exact input coordinate was itself read from the direct
Measurement result, or whether that lifecycle is another forced positive
question.

That census is now recorded in
`addressed_byte_determination_applicability_census_001.md`. The result is
stronger: the Applicability result has no verdict coordinate and always names
`applicable_to`, including a control whose Determination result contains zero
matching result-position references.
