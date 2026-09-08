# Checkpoint Recording occurrence subtraction report 001

## Question

Can the exact operator material occurrence supplying `/checkpoint` become the
source-boundary subject of the destination Locality physiology without a
separate Recording Act or result?

The preceding checkpoint occurrence-boundary investigation found that the
operator material result and the Recording result resolved the same exact
Locality cut. This implementation applies that falsifier.

`checkpoint` remains operator shorthand and acquires no Book coordinate.

## Prior road

The console previously recorded:

```text
operator source Act occurrence
        ↓
exact `/checkpoint\n` material result Q
        ↓
Recording Act occurrence
        ↓
Recording result R
```

The Recording Act minted:

```text
exact Act identity
prospective Act-occurrence identity
prospective result identity
```

The Act and result copied the source Locality and occurrence identity of `Q`.
Current-coordinate replay then placed `R` in a checkpoint-specific carrier
dictionary. Checkout required that wrapper and followed it back to `Q`.

## Current road

The console now records:

```text
operator source Act occurrence
        ↓
exact `/checkpoint\n` material result Q
```

The operator handler validates the exact command bytes. It appends no
checkpoint-specific occurrence.

When `/checkout\n` is supplied, operator mechanics examines the exact current
material-result coordinates. One exact operator material occurrence whose
bytes are `/checkpoint`, `/checkpoint\n`, or `/checkpoint\r\n` supplies the
source cut:

```text
Q
+ Q Locality
+ append boundary through Q
        ↓
Preservation binding in destination Locality
        ↓
Preservation Act occurrence
        ↓
Locality relation result occurrence
```

The destination relation carries only the exact recorded occurrence identity
of `Q`. Its reader follows `Q`, validates the operator-source result
physiology and exact command bytes, recovers `Q`'s Locality, and reads through
the append boundary ending at `Q`.

No source history is copied into the destination Locality.

## Subtracted coordinates

The live runtime no longer declares or records:

```text
checkpoint Recording Act kind
checkpoint Recording result kind
checkpoint Recording Act word
checkpoint exact Act identity
checkpoint prospective Act-occurrence identity
checkpoint prospective result identity
checkpoint Act occurrence
checkpoint result occurrence
checkpoint-specific current-coordinate carrier dictionary
```

No replacement Act, result, wrapper, relation, selection occurrence, or
family-local identity was introduced.

## Exact controls

### The material occurrence is the cut

Reading current coordinates through `Q` returns a Locality reading whose
through-occurrence coordinate is `Q`. The material-result coordinates include
the exact `/checkpoint\n` occurrence.

Appending source material after `Q` does not change that bounded read.

### Exact operator testimony

An operator material result with checkpoint command bytes passes. An ordinary
operator material result and a Witness material result carrying the same bytes
both refuse.

Thus:

```text
same bytes
+ separate source physiology
!=
same operator command occurrence
```

Changing the durable coordinates of `Q` causes integrity refusal.

### Cardinality

Checkout retains the exact cardinality discriminator:

```text
0 current checkpoint-command occurrences   refusal
1 current checkpoint-command occurrence    exact source cut
2 current checkpoint-command occurrences   refusal
```

Two equal command materials remain separate exact occurrences and therefore
remain ambiguous. No content equality collapses their occurrence identities.

### Locality

The exact `Q` occurrence is available in its source Locality. Its identity is
not globally available from a destination Locality merely because the Ledger
can address it.

The resulting destination Locality relation carries the exact `Q` reference.
Reading through that relation returns source coordinates through `Q` while the
destination history remains separate.

### Composition

The destination relation can itself carry the same `Q` reference into another
destination Locality. Every descendant follows the original exact occurrence;
none copies the source history.

This is the positive composition recovered by the recorded-result census:

```text
exact material result Q
        ↓ addressed by a subsequent Act
Preservation Act occurrence
```

The exact occurrence is the subject. No generic Use, Request, Checkpoint, or
Recording occurrence is required between it and the Act.

### Durability

The exact checkpoint-command occurrence survives SQLite close and reopen. Its
occurrence identity resolves the same source Locality cut after reopen.

## Book consequence

`05.Recording.D` described the removed checkpoint Recording lifecycle. No
active runtime producer remains for that clause.

The active Recording chapter, witness-grammar entry, README navigation entry,
and admitted word `recording` are withdrawn. This does not declare that no
future Recording distinction can occur. It records only that active law has no
such distinction now.

`06.Locality.C` now states its actual subject coordinates positively:

```text
exact addressed operator material occurrence
+ its exact through-occurrence boundary
+ Preservation
+ destination Locality
```

The operator interface word `checkpoint` remains outside Book admission.

## Results

```text
checkpoint-specific occurrences per command    2 -> 0
checkpoint prospective identities per command  3 -> 0
checkpoint current-coordinate surface           removed
exact operator material occurrence              retained
exact occurrence boundary                       retained
zero / one / two discriminator                   retained
source Locality cut                              retained
destination Locality relation                    retained
durable reopen                                   retained
mutation and source-family refusal               retained
source history copy                              absent
```

Focused Book and operator tests:

```text
102 passed
```

Complete suite:

```text
1053 passed
75 skipped
```

Python compilation and `git diff --check` pass.

## Finding

```text
exact occurrence boundary             Seed coordinate
operator word checkpoint              interface shorthand
checkpoint Recording Act occurrence   unsupported
checkpoint Recording result           copied carrier
05.Recording.D                         no active specimen
```

The result is not that Seed lacks checkpoints. The recovered positive shape is
smaller:

```text
every exact occurrence supplies an exact boundary

an operator-supplied checkpoint command occurrence
can become the exact boundary subject of a subsequent Act
```

The Ledger retains distinctions by exact occurrence coordinates. A separate
Recording lifecycle does not make those coordinates more exact.
