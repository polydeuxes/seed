# Measurement-result Candidate activation investigation 001

## Question

Why does the ordinary `!cat` road stop after its carried Measurement results
when Candidate production already consumes Measurement, Compare, and Candidate
result coordinates?

This is an investigation only. It changes no Book, grammar, console,
Measurement, Candidate, or Compare behavior.

## Direct finding

Candidate production exists, but it is not ready to be called from the live
console boundary.

```text
ordinary !cat
↓
Witness acquisition
↓
Measurement results carried by the bounded reconstruction
↓
console returns
```

The Candidate module already contains:

```text
Candidate Responsibility
↓
required source Assertion subject
↓
Applicability Responsibility
↓
Applicability Act and result
↓
Participation
↓
Candidate Act
↓
Yield
↓
Candidate result
```

It also has unary and ordered-pair Candidate Responsibilities and independent
result yielding. The missing live continuation is therefore not missing
Candidate physiology.

Two runtime blockers occur before that physiology can safely continue over the
sixteen-Book result population.

## Live activation

No production caller invokes any of these functions:

```text
record_one_source_candidate_responsibility(...)
record_ordered_pair_candidate_responsibility(...)
record_one_source_and_ordered_pair_candidate_responsibilities(...)
record_one_candidate_result(...)
yield_candidate_results(...)
```

Their callers are tests. `operator_console.py` imports and records a different
Representation-addressed Candidate road; it does not import the exact-result
Candidate module.

The exact-result recorders also require the caller to supply:

```text
source append boundary
recording Locality for unary Candidate work
recording Locality for ordered-pair Candidate work
```

No live Responsibility-exhaustion road currently derives those coordinates
from the carried Measurement result. Calling these functions after every
Measurement would make the console choose those coordinates and would not
recover the missing continuation.

History agrees. The exact-result Candidate physiology and its predecessor were
executed by focused Candidate and Compare tests. No ordinary-console caller was
removed by the current decomposition.

## Current source-reader refusal

Even a direct attempt to use the existing Candidate source reader stops before
recording a Candidate Responsibility.

The source reader handles generic result coordinates in this order:

```text
result reference
↓
material["assertions"] list or dictionary
↓
position-Measurement specialization
```

For a position-coordinate Measurement result, `material["assertions"]` is a
bounded account carrying:

```text
result
measurement rule
source material-acquisition reference
source Locality
completeness boundary
occurrence count
coordinates
Unknown
```

It is not an independently addressed Assertion. It therefore has no Assertion
address.

The generic dictionary branch nevertheless calls `_assertion_address()` on
that account. It raises:

```text
Candidate production requires one exact Assertion carried by a result
```

The dedicated position-result branch below it is never reached. That branch
already knows how to read each exact recorded position Assertion and its exact
source coordinates.

The sixteen-Book probe reproduced the same refusal for all four current
position-coordinate results:

```text
operator command position result
stdout position result
empty stderr position result
empty completion position result
```

No Candidate occurrence was appended before refusal.

Existing Candidate tests did not expose this seam. Their basic source helper
records an exact-byte Measurement whose `assertions` coordinate is a list of
independently addressed findings. That result passes the generic list branch.

## Complete boundary size

The present Candidate source reader does not address a single carried result.
It freezes a supplied global ledger boundary, reconstructs every Locality
through that boundary, and harvests source references from all carried
Measurement, Compare, and Candidate result populations.

For the sixteen-Book probe, correcting only the position-account refusal would
expose this source population:

| source result | Candidate source references |
|---|---:|
| operator command position result | 59 |
| operator command exact-byte result | 43 |
| operator command locality-position result | 21 |
| corpus stdout position result | 218,058 |
| corpus stdout exact-byte result | 267 |
| empty stderr position result | 1 |
| cumulative exact-byte result after stderr | 267 |
| empty completion position result | 1 |
| cumulative exact-byte result after completion | 267 |
| complete boundary | **218,984** |

The stdout position result contributes its result reference plus 218,057 exact
position Assertion references. The bounded account itself contributes no
Assertion reference.

The unary Candidate Responsibility therefore has 218,984 required subjects at
this supplied global boundary.

The ordered-pair Responsibility has:

```text
218,984 × 218,983 = 47,953,773,272
```

ordered required subjects.

Current `_required_subjects()` constructs the complete ordered-pair list in
memory before `record_one_candidate_result()` can yield its first result. The
recent law permits a yielded Candidate to proceed while sibling work remains,
but this eager construction prevents that interleaving on the real corpus.

This is not merely a long complete run. The current runtime attempts to form
nearly forty-eight billion subject dictionaries before the first ordered-pair
Candidate occurrence.

## Exact stopping boundary

The live road stops first because no Responsibility-exhaustion continuation
addresses Candidate production:

```text
carried Measurement results
↓
no live Candidate Responsibility activation
↓
STOP
```

The existing direct Candidate entry then has its own earlier refusal:

```text
supplied global ledger boundary
↓
position-result bounded account treated as an Assertion
↓
no Assertion address
↓
REFUSE
```

If that reader defect is removed, eager complete-subject construction is the
next runtime stop:

```text
218,984 source references
↓
47,953,773,272 ordered subjects materialized before first Yield
↓
impractical
```

## Disposition

Do not add a post-Measurement console call.

Candidate physiology remains intact. The next work must keep three distinctions
separate:

```text
position-result bounded account
!=
exact addressed position Assertions

current carried result boundary
!=
caller-supplied global ledger boundary

Responsibility exhaustion
!=
eager construction of its complete subject population before first Yield
```

The smallest mechanical correction is the position-result source reader: it
must not treat the bounded `assertions` account as an Assertion, and it must
reach the existing exact position-reference reader. That correction alone does
not establish live activation and does not make eager ordered-pair construction
practical.
