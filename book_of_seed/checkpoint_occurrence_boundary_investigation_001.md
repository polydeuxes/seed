# Checkpoint occurrence-boundary investigation 001

## Question

Does the operator word `checkpoint` require a Seed Recording Act and result,
or does its exact material-result occurrence itself address the requested
through-occurrence boundary?

This investigation changes no active Book clause, admission, machine grammar,
runtime occurrence, Act, result, relation, identity, reader, or operator road.

`checkpoint` is operator shorthand. It is not admitted Book vocabulary. The
ordinary word is used here only to identify the supplied slash-command bytes.

## Existing boundary physiology

The Ledger derives an exact append-prefix identity at every recorded
occurrence. A caller addresses that prefix through the occurrence identity:

```text
exact recorded occurrence E
        ↓
append boundary through E
        ↓
exact Locality reading through E
```

Resolving that boundary mints no occurrence and no boundary identity. The
in-memory and durable Ledgers both recover the prefix identity that was derived
when `E` was appended.

Therefore an extra occurrence is not required merely to make a cut exact.

## The supplied operator occurrence

For the operator input:

```text
/checkpoint\n
```

the source road first records an exact material result occurrence `Q` whose
exact bytes are `/checkpoint\n`. The slash-command parser then addresses:

```text
Locality of Q
through-occurrence identity = Q
exact command bytes
```

Before the checkpoint-specific Recording road begins, `Q` is consequently:

```text
durable
exactly addressable
Locality-qualified
an exact through-occurrence boundary
operator-supplied as `/checkpoint\n`
```

No checkpoint-specific Seed occurrence is needed to obtain those coordinates.

## Current extra lifecycle

The current operator road appends two occurrences after `Q`:

```text
Q: exact `/checkpoint\n` material result
        ↓
Recording Act occurrence
        ↓
Recording result occurrence R
```

The Recording Act also mints three prospective family identities:

```text
exact Act identity
Act-occurrence identity
result identity
```

The Act copies the Locality and occurrence identity of `Q` into its subject
reference. The result copies that subject reference and the lifecycle
identities, then adds the exact Act-event occurrence reference.

Thus the source coordinate carried by `R` is:

```text
source Locality                 = Locality of Q
source through occurrence      = Q
```

## Exact equality control

One live console run supplied only `/checkpoint\n`. Let:

```text
Q = operator material result occurrence for `/checkpoint\n`
R = checkpoint Recording result occurrence
```

The two reads were:

```text
read exact current coordinates through Q

read coordinates carried by R
    → follow R to its Recording Act
    → follow the Act subject to Q
    → read exact current coordinates through Q
```

Their returned current-coordinate dictionaries were equal. Both ended through
`Q` and contained the same exact material-result coordinates.

The interval after `Q` through `R` contained only:

```text
checkpoint Recording Act occurrence
checkpoint Recording result occurrence
```

Removing those two occurrences from the conceptual path changes no coordinate
of the addressed cut.

## Carriage is presently authored by the wrapper kind

Current-coordinate replay places `R` into
`recorded_through_occurrence_boundary_references` solely because `R` has the
checkpoint Recording result event kind. The carried-coordinate reader first
requires an identity from that dictionary and then follows the wrapper back to
`Q`.

This proves that the current runtime uses `R`. It does not independently prove
that `R` adds physiology:

```text
runtime appends wrapper R
        ↓
current-coordinate reader recognizes wrapper kind
        ↓
checkout requires recognized wrapper R
```

That dependency was authored with the wrapper. The exact operator material
occurrence `Q` remains durably present and already addresses the same cut.

## Boundary and addressed boundary remain distinct

This finding does not make every recorded occurrence the subject of a
subsequent Locality Act.

```text
every exact occurrence defines a readable cut

not

every exact occurrence is addressed by checkout
```

The supplied `/checkpoint\n` bytes distinguish `Q` for operator mechanics. A
subsequent `/checkout\n` can explicitly address that exact command occurrence.
Co-current material results alone imply no such Act.

This preserves the distinction recovered by the recorded-result composition
census:

```text
exactly addressable occurrence
!=
subject of a subsequent Act
```

## Proposed subtraction falsifier

The next implementation experiment should change only the checkpoint and
recorded-boundary Locality road:

```text
current

exact `/checkpoint\n` material result Q
        ↓
Recording Act
        ↓
Recording result R
        ↓
Preservation / destination Locality

pressure

exact `/checkpoint\n` material result Q
        ↓
Preservation / destination Locality
```

The destination Locality relation should address `Q` as its exact source cut.
It must not copy source history and must not infer a cut from arbitrary current
material.

The subtraction fails if any of these distinctions cannot survive:

```text
zero exact checkpoint-command occurrences       checkout refuses
one exact checkpoint-command occurrence         checkout addresses it
two exact checkpoint-command occurrences        checkout refuses ambiguity
same command bytes in separate occurrences       separate exact cuts
changed or corrupted command occurrence          refusal
command occurrence in a different Locality       refusal
durable reopen                                    same exact source cut
source activity after Q                          carried cut remains Q
destination Locality                             separate from source Locality
source history in destination                    absent
```

The test must also prove absence of:

```text
checkpoint Recording Act occurrence
checkpoint Recording result occurrence
checkpoint prospective lifecycle identities
```

No Checkpoint Act, Checkpoint relation, selection occurrence, carried-reference
wrapper, or replacement result kind should be introduced.

## Book consequence is not taken yet

`05.Recording.D` currently describes the checkpoint Recording Act/result road.
If the proposed falsifier passes, that sole active specimen no longer supports
the clause. The implementation experiment must pass before changing the Book
or admission.

This report does not challenge an independently occurring Recording Act in a
different road. It finds only that the current checkpoint road has not supplied
one.

## Finding

```text
exact occurrence defines append cut                 yes
Q is exact supplied checkpoint-command material     yes
Q directly addresses the requested cut              yes
R resolves to the same cut                           yes
Recording Act/result adds a different cut            no
R carrier status independent of its authored kind    not found
checkout through Q without R                         untested
```

## Disposition

Freeze `checkpoint` as an operator-interface word, not a Seed primitive.

Pressure the separate checkpoint Recording Act, result, and prospective
lifecycle identities together with their only consumer. The positive target is
not “no checkpoint.” It is:

```text
the exact `/checkpoint\n` material occurrence
becomes the exact source-boundary subject
of a subsequent operator-authored Locality Act
```

That is exact result-to-subsequent-Act composition. It requires no additional
Checkpoint or Recording occurrence merely to preserve a boundary that the
Ledger already derives at every occurrence.
