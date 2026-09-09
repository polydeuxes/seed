# Witness filesystem source coordinate census 001

## Correction

This census corrects a proposed third material-source road.

When the operator supplies `!ls`, Seed already records the returned material
through the Witness source physiology. The returned bytes do not lack a
source merely because the operating-system mechanics that produced them are
outside the Ledger.

No new filesystem Source family is required.

Filesystem, path, entry, command, and operating system are ordinary
report-local terms. This census changes no runtime road, Book clause, Witness
Grammar, or admission.

## Existing exact road

The active invocation path records:

```text
exact operator !ls material occurrence Q
        ↓
exact operator-to-destination Locality relation L
        ↓
exact material supplied by this Witness
        ↓
Witness source Act occurrence A
        ↓
exact Witness material result R
```

`record_supplied_witness_material_source()` requires the exact operator
occurrence and exact destination Locality relation before it records `R`.
It supplies the Witness source reader with:

```text
R.exact_material
R.source_boundary
R.source_occurrence_references = [Q, L, ...prior supplied occurrences]
R.read_occurrences
R.Locality = L.destination Locality
R → A
```

The host provider's ordinary `!ls` output therefore becomes exact material
from this Witness in the exact invocation Locality. `R` is subsequently read
through the same exact-material front door as other source results and can be
current through a selected Ledger boundary.

Thus:

```text
returned !ls material has Witness source coordinates       yes
returned !ls material has invocation Locality coordinates  yes
returned !ls material can be current through B              yes

third filesystem Source family                              no
filesystem-as-Locality shortcut                             no
```

## What the coordinates mean

The filesystem is part of the environment addressed by the Witness operation.
It does not need to become a second Witness, another Locality, or another
material-source kind.

The exact operator occurrence `Q` retains the supplied command bytes. For an
invocation such as:

```text
!ls exact-path
```

`R` addresses `Q` through its source occurrence references. The returned
bytes, the command occurrence, the invocation Locality relation, and the
Witness read boundaries therefore remain jointly recoverable without copying
the command or path into `R`.

This is source provenance. It does not by itself decompose every returned
line into a separate filesystem-entry coordinate.

## The actual unresolved distinction

The missing question is not:

```text
where did these bytes come from?
```

The existing Witness road answers that.

The narrower question is:

```text
which exact filesystem coordinates, if any, have been recovered
from the returned material as subjects for later Acts?
```

For example, `!ls` may return an entry name as exact bytes. That result does
not automatically establish a separate exact entry occurrence merely because
the bytes resemble a path. Existing Measurement can address the result and
its positions. A later Act may address those exact results. Co-current
addressability alone still implies no later Act.

Therefore:

```text
Witness filesystem result R                         exact
bytes and read positions within R                   exact
Q and invocation Locality provenance                exact

one output line = exact filesystem entry occurrence not established here
path bytes = independent filesystem identity        not established here
file existence after the invocation                 not established here
```

## B-to-C experiment

The gzip experiment can use the existing Witness source road on both sides.

At a selected boundary `B`, exact Witness results may address the observable
filesystem state before an invocation. After the operating-system change,
later exact Witness results may address the observable filesystem state at a
selected boundary `C`.

```text
exact Witness result(s) current through B
        ↓
operating-system mechanics
        ↓
exact Witness result(s) current through C
        ↓
existing comparison physiology may address B and C results
```

No process occurrence, filesystem Source occurrence, Search occurrence,
Placement occurrence, or Request occurrence is inserted merely to narrate
the middle step.

This experiment must distinguish:

```text
same exact Witness result read through two boundaries
different exact Witness results with equal bytes
different exact Witness results before and after a filesystem change
```

Only the third shape can testify about a changed observation. Even then, the
comparison testifies only about the exact addressed results; it does not infer
unobserved filesystem history.

## Subtraction controls

The existing road must continue to refuse:

```text
missing or corrupted operator occurrence
missing or corrupted invocation Locality relation
supplied result in the wrong destination Locality
changed source occurrence references
malformed or non-covering read coordinates
```

Equal returned bytes from separate invocations remain separate because their
operator, Locality, Act, and result occurrences remain separate.

## Disposition

Keep the existing topology:

```text
operator material
→ invocation Locality
→ material supplied by this Witness
→ exact Witness source result
→ current through a selected boundary
```

Withdraw the proposed topology:

```text
path
→ new direct filesystem Source family
→ duplicate material result
```

The next experiment should consume the existing Witness results and pressure
whether their exact bytes and source references are sufficient subjects for
the desired later Act. It should add no source physiology unless an exact
distinction survives independently of the Witness road.
