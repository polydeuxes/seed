# Byte Measurement result completeness-boundary copy census 001

## Question

Must the plain-byte Measurement result copy its completeness boundary when its
exact Act occurrence and source-material-set finding already address that
boundary?

This census changes no runtime road, Book clause, Witness Grammar, admission,
Act, result, or occurrence.

## Current shape

```text
A.completeness_boundary_identity = B

R.act_occurrence_event_identity = A.identity
R.completeness_boundary.identity = B

R.result_positions[source-material-set]
    .dimensions.content.completeness_boundary.identity = B
```

The Act reader uses `B` to reconstruct the exact bounded source material before
R can be recorded or read. The result-position structure then records the exact
source-material-set finding, including its bounded-read coordinate.

## Attempted distinction

No control holds A and the source-material-set finding fixed while giving the
top-level R copy a different lawful boundary. The reader compares the copied
identity with the same boundary recovered from A.

## Required falsifier

Remove only:

```text
R.completeness_boundary
```

Retain:

```text
A.completeness_boundary_identity
R → A occurrence reference
source-material-set finding boundary
exact material-result subjects
source Localities on A
recording cut
all count and recurrence findings
restart and current-coordinate replay
downstream byte-pair Measurement and Movement
```

Changing A's boundary or the finding's boundary must continue to invalidate R.
Reintroducing the top-level copy on R must be refused as an extra coordinate.

## Family boundary

This census addresses only the top-level plain-byte result copy. The boundary
inside the exact source-material-set finding and every other result family
remain unchanged.

## Disposition

```text
completeness boundary on exact Act A          retained
bounded source-material-set finding           retained
top-level completeness boundary copied on R   failed census
result boundary-copy subtraction              next falsifier
```
