# Preservation Act identity-order read correction report 001

## Finding

The first read-breadth correction remained dependent on the SQLite append-
prefix validation cache.

The Preservation Act reader had stopped listing every occurrence explicitly,
but it still followed this route:

```text
Q and Preservation Act A
→ append boundary through A
→ validate stored prefix identities after an external commit
→ decode every Ledger occurrence
→ ask whether Q occurs before A
```

When the validation cache was cold, unreadable material in an unrelated
Locality could still block an otherwise exact read of A. Material after A was
also decoded even though it cannot affect the Q-before-A question.

## Exact question

The Act reader has already validated A and its exact subject Q. The remaining
coordinate is only their append order:

```text
Q.identity
A.identity
Q append position < A append position
```

This question does not require an append-prefix identity or any occurrence
material.

## Correction

Both Ledger implementations now validate supplied occurrence identities in
append order.

The in-memory Ledger reads only the named identity positions. The SQLite
Ledger reads only the named event row positions. It does not enter the global
prefix validator and does not decode event material.

The Preservation Act reader asks for this exact order:

```text
(Q.identity, A.identity)
```

The earlier `append_boundary_contains_occurrence` helper is withdrawn. Its
boundary resolution could re-enter whole-history prefix validation, so it did
not support the narrower read claimed by the first report.

## Controls

Unrelated unreadable material is placed independently before and after A.
Each position is tested under three SQLite cache states:

```text
warm prefix cache
forgotten prefix cache
external committed identity-reservation change
```

All six readings validate only Q and A and accept the exact Act. Reversing Q
and A refuses. An absent identity refuses. In-memory and SQLite order results
are equal.

The general append-boundary readers are unchanged. They retain their global
prefix-integrity validation when a caller actually asks to read through an
append-prefix identity.

## Disposition

```text
exact Q occurrence                         retained
exact Preservation Act occurrence          retained
Q-before-A append order                    retained
unrelated material dependency              absent
global prefix validation for boundary read retained
```

This is storage/addressing mechanics. It adds no Book coordinate, Act,
relation, result, or admitted word. The copied-coordinate subtractions remain
unchanged.
