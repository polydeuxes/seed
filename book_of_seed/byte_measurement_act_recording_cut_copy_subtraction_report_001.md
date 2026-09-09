# Byte Measurement Act recording-cut copy subtraction report 001

## Subtraction

The plain-byte Measurement Act no longer serializes its recording-Locality
cut.

Before:

```text
A.locality = L
A.completeness_boundary_identity = B
A.through_event_occurrence_identity = C
```

After:

```text
A.locality = L
A.completeness_boundary_identity = B

C = latest occurrence in L through B
```

## Surviving distinction

The source completeness boundary B and the recording Locality cut C remain
different coordinates. B bounds the source-material read. C is reconstructed
as the latest occurrence in A's Locality through B.

The derived C remains stable when later occurrences enter A's Locality because
the query stays bounded by the fixed B. An initially empty recording Locality
derives `None`. Reintroducing the retired field is refused as an extra Act
coordinate.

Current-coordinate replay reconstructs C from the validated A Locality and B
rather than from copied Act material. SQLite restart retains the same
derivation.

## Family boundary

This subtraction changes only the plain-byte Measurement Act. It does not
remove B, alter current-coordinate boundary semantics, or change another
Measurement family.

## Result

```text
source completeness boundary B           retained
recording Locality cut C                  retained by exact reconstruction
durable C copied on A                     removed
```
