# Byte Measurement result Act-copy census 001

## Question

Must the plain-byte Measurement result copy `exact_act = Measurement` when it
already addresses the exact Act occurrence?

This census changes no runtime road, Book clause, Witness Grammar, admission,
Act, result, or occurrence.

## Current shape

The result carries:

```text
act_occurrence_event_identity = A.identity
exact_act = Measurement
```

`A` independently carries:

```text
act = Measurement
```

The result reader resolves `A`, validates its kind, integrity, Locality,
subjects, boundaries, and Act word, then separately requires `A < R` and one
result for `A`.

## Attempted distinction

No active consumer addresses `R.exact_act` independently of `A`. The writer
copies the same literal into R, and the reader compares both authored surfaces
with the same expected literal.

Changing `A.act` to `Compare` already invalidates R through the exact occurrence
reference. Removing the copy therefore does not make the Act implicit in the
result event kind.

## Required falsifier

Remove only:

```text
R.exact_act
```

Retain:

```text
A.act = Measurement
R.act_occurrence_event_identity = A.identity
A < R
one R per A
exact subjects
source Localities
source completeness boundary
recording cut
result findings
restart and current-coordinate replay
downstream byte-pair Measurement and Movement
```

Changing `A.act` must continue to invalidate R. Reintroducing `exact_act` on R
must be refused as an extra coordinate.

## Family boundary

This census addresses only the plain-byte Measurement result. Other result
families and the plain-byte result's remaining source and boundary copies
receive no result by analogy.

## Disposition

```text
Measurement Act coordinate on A             retained
exact Act occurrence reference on R         retained
copied exact_act on R                        failed census
result Act-copy subtraction                  next falsifier
```
