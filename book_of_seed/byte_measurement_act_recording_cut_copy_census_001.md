# Byte Measurement Act recording-cut copy census 001

## Question

Must the plain-byte Measurement Act durably copy its recording-Locality cut
when that cut is determined by the Act Locality and the completeness boundary?

This census changes no runtime road, Book clause, Witness Grammar, admission,
Act, result, or occurrence.

## Current shape

```text
A.locality = L
A.completeness_boundary_identity = B
A.through_event_occurrence_identity = C

C = latest occurrence in L through B
```

`B` and `C` are different boundary domains. `B` bounds the source-material
read across the declared source Localities. `C` is the recording Locality's
cut through that boundary.

The distinction between those boundaries survives this census.

## Attempted durable distinction

The Act reader already refuses unless the stored `C` equals:

```text
latest_locality_occurrence_identity(A.locality, through=B)
```

No lawful control holds `A.locality` and `B` fixed while varying `C`.
Changing `C` to an older occurrence refuses because the copied value no longer
equals the coordinate reconstructed from the surviving inputs.

Current-coordinate replay reads the stored value, but that dependency was
authored with the copy. It does not independently establish that `C` must be
serialized on A.

## Required falsifier

Remove only:

```text
A.through_event_occurrence_identity
```

Retain:

```text
A.locality
A.completeness_boundary_identity = B
C = latest occurrence in A.locality through B
subject-before-A occurrence order
exact source subjects and source Localities
restart and current-coordinate replay
R → A and every result finding
```

Reintroducing the retired field must be refused as an extra Act coordinate.
Adding a later occurrence in A's Locality must not change the reconstructed cut
for the older fixed boundary B.

After SQLite reopen, current-coordinate replay must expose the same derived C
for R while A carries no C field. When no occurrence existed in A's Locality
through B, the reconstructed cut remains `None` rather than requiring a prior
occurrence.

## Family boundary

This census addresses only the durable recording-cut copy on the plain-byte
Measurement Act. It does not remove the completeness boundary, change current
coordinate readings, or pressure any other Measurement family.

## Disposition

```text
source completeness boundary B             retained
recording Locality cut C                    retained as exact relation to B
durable C copied on plain-byte Act A        failed census
recording-cut copy subtraction              next falsifier
```
