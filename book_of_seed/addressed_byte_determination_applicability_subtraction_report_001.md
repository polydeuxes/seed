# Addressed-byte Determination Applicability subtraction report 001

## Result

Addressed-byte Determination now records:

```text
exact direct pair-position Measurement result
+ exact addressed source-byte position coordinate
        ↓
Determination Act occurrence
        ↓
Determination result occurrence
```

The former two binding occurrences and Applicability Act/result occurrences
are absent. No replacement binding, Candidate, population, verdict, or wrapper
was introduced.

## Why this road differs from ordinary Applicability

The direct Measurement result and one coordinate read from that result already
establish the complete Determination subject. No host-created pair remains to
be judged. The removed Applicability result had no `applicable` /
`inapplicable` coordinate and always recorded `applicable_to`.

The final Determination result independently establishes the meaningful
variation:

```text
zero matching result-position references
one matching result-position reference
two matching result-position references
```

The single-byte control still produces an exact Determination result with zero
references. The interior repeated-byte control still produces two. A forced
positive Applicability occurrence distinguished neither case.

## Preserved coordinates

The Determination Act occurrence records:

```text
exact direct Measurement result occurrence
exact addressed source-byte position coordinate
exact Determination Act
Locality
prior through-occurrence boundary
exact Act occurrence and result identities
```

The Determination result directly addresses that Act occurrence and preserves
the exact direct result, addressed coordinate, completeness boundary, and
ordered result-position references.

The resulting physiology preserves:

```text
source result before Determination Act
Determination Act before result
Act present with result absent
exactly one result for one Act
zero / one / two matching-reference multiplicity
current-coordinate replay
SQLite reopen
changed source and changed Act refusal
stale and cross-Locality coordinate refusal
intervening append and mutation refusal
downstream D.2 shared-position Measurement
```

## Atomicity control

The direct result writer reads its Act, source result, and addressed references
again after scanning the existing result population and before append. An
intervening occurrence or an in-place Act mutation prevents the Determination
result. Removing four prospective occurrences therefore did not weaken the
old road's read-to-append refusal boundary.

## Runtime surface

The retired family-local surfaces are absent from active runtime:

```text
Determination subject-to-Act binding event
Applicability subject-to-Act binding event
Applicability Act occurrence
Applicability result occurrence
binding reference on the Determination Act
Applicability result reference on the Determination result
```

Current-coordinate replay now admits only the Determination Act and result for
this family. The D.2 consumer reads the direct Determination result physiology.

## Finding

```text
exact subject before prospective stages       established
independently variable Applicability verdict  absent
forced positive ceremony                      failed subtraction
separate binding occurrences                  failed on this road
Determination Act/result distinction           preserved
ordinary positive/negative Applicability       untouched
```

This does not withdraw Applicability generally. It withdraws one family-local
Applicability lifecycle that could not vary and whose exact subject was
already established before that lifecycle began.

## Validation

```text
focused direct and dependent tests       64 passed
broader pipeline and Book grammar        89 passed
full-suite collection                    1,133 tests
```

The broader slice includes source-position comparison, recurrence, operator
current-coordinate replay, the read-only exact-material Distinction route,
the inward occurrence surface, and active Book grammar.
