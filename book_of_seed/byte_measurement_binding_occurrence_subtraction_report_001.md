# Byte Measurement binding-occurrence subtraction report 001

## Question

Can the plain-byte Measurement binding coordinates remain exact without a
separate binding occurrence?

The preceding census found no fact carried by the binding-only floor beyond
the wrapper and its runtime consumers. The copied Book-clause label then failed
independent subtraction. This pass removes only the remaining binding
occurrence.

## Prior shape

```text
exact material-result subjects
+ source Localities
+ source completeness boundary
+ recording through-occurrence boundary
        ↓
binding occurrence E
        ↓
exact-byte Measurement Act A
        ↓
Measurement result R
```

The current-coordinate reader carried `E`, the Act writer required `E`, and
declared Measurement discovery treated `E` as prior work. A durable `E` with no
`A` therefore survived restart, but only because those readers were authored
around that wrapper.

## Subtraction

The active road is now:

```text
exact material-result subjects
+ source Localities
+ source completeness boundary
+ recording through-occurrence boundary
        ↓
exact-byte Measurement Act A
        ↓
Measurement result R
```

`A` carries the exact former binding coordinates directly:

```text
act
subject_reference
source_localities
completeness_boundary_identity
through_event_occurrence_identity
Act Locality
```

`R` addresses `A.identity`. Neither occurrence contains a binding reference,
and the retired binding event kind is absent from the runtime and current
coordinates.

## Surviving distinctions

The source completeness boundary and the recording cut remain separate. The
first bounds the source material read. The second, when present, is an exact
occurrence in the Act Locality preceding `A`.

The Act reader reconstructs the exact source material through the completeness
boundary, compares the subject references, and requires the boundary ordering.
A changed subject, boundary, Locality, or Act coordinate refuses. Only result
recording and reading derive the byte findings; replaying an Act does not
perform its result work.

The recording cut is the last occurrence in the Act Locality through the source
completeness boundary. The Ledger answers that exact identity question without
reading unrelated occurrence material. Substituting an older same-Locality
occurrence therefore refuses even though that occurrence also precedes `A`.

Current-coordinate replay validates `A` before advancing its boundary. A
corrupted Act cannot become the current through-occurrence merely because Acts
carry no result coordinates.

The stoppable lifecycle is now:

```text
A exists
R absent
```

SQLite reopen between `A` and `R` retains that floor. The actual Act and result
occurrence identities retain occurrence separation and one-result-per-Act
cardinality.

## Declared Measurement

Discovery now reads the subject references of plain-byte Measurement Acts rather
than binding occurrences. It does not derive the byte findings merely to decide
whether the subject coordinates have an Act. An Act without a result remains an
exact occurrence and suppresses a duplicate Act over the same subject
coordinates. No work-assignment, Candidate, or pre-Act commitment occurrence
replaces `E`.

## Family boundary

Byte-pair Measurement and result-position Movement retain their independently
tested binding occurrences. Their event kinds, readers, writers, and durable
coordinates are unchanged.

The Act word remains `exact-byte Measurement` in this pass. Its narration and
the result's copied coordinates remain separate pressure targets.

## Disposition

```text
plain-byte binding coordinates                    retained on A
separate plain-byte binding occurrence            withdrawn
binding-only restart floor                        withdrawn
Measurement Act without result                    retained
source completeness boundary                      retained
recording through-occurrence boundary              retained
actual Act and result occurrence identities       retained
byte-pair and Movement bindings                    unchanged
```
