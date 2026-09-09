# Byte Measurement binding-occurrence census 001

## Question

After the three family-local identities failed independently, does the separate
plain-byte Measurement binding occurrence retain a physiological distinction?

This census changes no runtime road, Book clause, Witness Grammar, admission,
Act, result, or occurrence.

## Current shape

Plain-byte Measurement now records:

```text
exact material-result subjects
+ source Localities
+ source completeness boundary
+ recording through-occurrence boundary
        ↓
binding occurrence E
        ↓
Measurement Act occurrence A
        ↓
Measurement result occurrence R
```

`E`, `A`, and `R` have separate Ledger occurrence identities. The prospective
result identity, prospective family Act-occurrence identity, and opaque exact-Act
identity have already failed subtraction.

The binding material is now only:

```text
subject_reference
Book clause
source Localities
source completeness boundary
recording through-occurrence boundary
```

## Attempted survival

The binding can be recorded without the Act. That prefix survives SQLite
restart, appears in current coordinates, and can later be consumed by the Act
writer.

Those are real runtime behaviors, but every one depends on the binding event the
runtime itself authored:

```text
runtime records E
current-coordinate reader recognizes E.kind
Act API requires E.identity
restart test later consumes E into A
```

No independent Act or result produces `E`. No later physiology consumes the
E-only state except the byte Measurement Act writer.

## Rediscovery control

Declared Measurement discovery scans current plain-byte bindings and compares
their copied subject references with the current material-result set. An E-only
prefix therefore suppresses a later Measurement over those subjects.

If execution stops after `E` and before `A`, rediscovery treats the unfinished
wrapper as assigned work. That behavior is produced by the wrapper dependency;
it is not an independently addressed Measurement result.

Removing `E` would remove this restartable pre-Act commitment. The meaningful
stoppable floor remains:

```text
Measurement Act A exists
Measurement result R absent
```

## Act-coordinate shape under pressure

Every surviving coordinate of `E` can instead be an exact coordinate of `A`:

```text
Measurement Act A
    exact material-result subjects
    source Localities
    source completeness boundary
    recording through-occurrence boundary
    Measurement
    Act Locality
```

That shape retains the distinction between the source completeness boundary and
the recording cut. It does not infer that source Locality equals Act Locality.

The Act reader can reconstruct the exact bounded source material, require both
boundary relations and occurrence order, and recompute the byte findings before
`R` is recorded or read.

The result can then address `A.identity` directly. A binding reference would not
survive as a renamed dictionary.

## Required falsifier

Remove only the plain-byte binding occurrence and require:

```text
no plain-byte binding event kind
A carries the exact former binding coordinates
A can exist without R
SQLite reopen between A and R
R addresses A.identity
source completeness boundary precedes A
recording cut precedes A when present
every exact material-result subject is unchanged
all byte count and recurrence findings are unchanged
one result per A
changed source, boundary, Locality, and Act coordinates refuse
current-coordinate replay remains exact
downstream byte-pair Measurement and Movement remain exact
```

Declared discovery must inspect existing byte Measurement Acts or results rather
than binding occurrences. An unfinished Act is already an exact occurrence; it
does not require a prior work-assignment occurrence.

## Family boundary

Byte-pair Measurement and result-position Movement retain their own binding
families. Their event kinds, writers, readers, current-coordinate carriage, and
tests receive no result by analogy.

## Disposition

```text
plain-byte binding coordinates                    required
separate plain-byte binding occurrence            failed census
restartable pre-Act commitment                    wrapper-authored behavior
Measurement Act without result                    retained stoppable floor
source/recording boundary distinction             retained
binding-occurrence subtraction implementation     next falsifier
```

No runtime change is authorized beyond that exact family-local falsifier.
