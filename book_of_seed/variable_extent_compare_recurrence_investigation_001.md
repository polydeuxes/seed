# Variable-extent Compare recurrence investigation 001

## Question

Does the recently proposed three-coordinate Compare road preserve an exact
distinction, or does it still embed a developer-chosen extent?

This investigation changes no active Book chapter, witness grammar, runtime,
or test. Terms such as `extent`, `shape`, and `signature` are curator rendering
inside this report. They do not introduce active Seed grammar.

## Finding

The fixed three-coordinate road is biased.

```text
[a,b,c]
↓
(a,b) (a,c) (b,c)
```

removes the first/final privilege, but it still assumes that three source
coordinates form the complete subject boundary. The same source material also
addresses:

```text
[a,b]
[a,b,c,d]
[a,b,c,d,e]
...
```

Nothing in current source order privileges extent three.

Commit `7ef0d4c2` remains useful: D.2 resolves an exact local coordinate
population without requiring shared-position or `ordered_relation_path`.
That does not make D.2's at-most-three-coordinate population the universal
Compare boundary.

## Existing testimony

Commits `8b77049d` and `eda31e3b` previously recorded two separate operations:

```text
complete Compare finding population
↓
literal same/different partition

repeated exact partitions
↓
count
↓
recurrence where count exceeds one
```

Commit `3fc67015` removed that implementation with a larger redundant pairwise
analysis road. The removed modules carried retired wrappers and a fixed
declared coordinate surface. They must not be restored wholesale.

Their surviving testimony is narrower:

```text
complete bounded Compare results
!= a chosen subset of those results

complete same/different result population
can be counted for exact recurrence

recurrence
!= equivalence, meaning, or significance
```

## Incremental extent

Current adjacent position Measurement supplies every minimal ordered source
bound:

```text
[x0,x1]
```

Starting from every adjacent source position and extending only in source
order reaches every finite contiguous source extent. There is no need to grow
both ends and thereby record the same extent several ways.

For an exact extent:

```text
E(k) = [x0,x1,...,x(k-1)]
```

the complete Compare population is:

```text
(xi,xj) for every exact i < j < k
```

Growing by the next exact source coordinate does not require repeating the
already-established Compare work:

```text
E(k) + xk
↓
only newly introduced Compare subjects

(x0,xk)
(x1,xk)
...
(x(k-1),xk)
```

The prior result population remains exact support. The new results extend that
population. This is linear work in the current extent for each extension, not
reconstruction of every internal pair.

## The discriminator

Growth alone establishes no reason for further growth. Otherwise every source
start extends to the material boundary and recreates the complete span
population.

The recovered discriminator is exact recurrence of the complete bounded
same-content/difference finding population.

```text
exact extent occurrence
↓
complete internal Compare findings
↓
exact count under one completeness boundary
↓
recurrence, where established
```

Only a recurrence result provides the proposed later extension subject:

```text
recurring bounded result
+ exact next adjacent source coordinate for each carried occurrence
↓
one-coordinate extension work
```

Where recurrence is not established, no later extension relation is thereby
established. That is not a negative relation, prohibition, or special stopped
state. The branch simply carries no result consumed by this extension road.

Other exact Responsibilities may still consume its results independently.

## Why recurrence does not hide a larger recurring result

For the exact same/different surface, every occurrence of an extent of size
`k+1` contains its ordered prefix of size `k`.

If two size-`k+1` extents carry the same complete same/different findings, their
size-`k` prefixes also carry the same complete findings. Therefore:

```text
recurring E(k+1)
↓
recurring prefix E(k)
```

Consequently, refusing to extend a nonrecurring prefix cannot hide a recurring
larger same/different result. This statement is bounded to this exact result
surface. It does not claim the same property for every future Measurement or
relation.

## `p q p` emerges without an extent-three rule

For one branch:

```text
[p,q]
↓ recurring prior result, where established
extend by p
↓
[p,q,p]
```

Only the new Compare work is recorded:

```text
(p,p) → same-content
(q,p) → difference
```

beside the preserved earlier:

```text
(p,q) → difference
```

The complete result exposes the externally recognizable `p q p` shape. The
developer did not choose extent three or privilege first/final coordinates.

The same branch may extend again only through another exact result consumed by
the extension road.

## Observer check over the sixteen Book windows

A disposable `/tmp` observer applied only the incremental equality-partition
calculation to the exact 218,058-byte concatenated corpus. It did not invoke
Seed physiology and recorded no ledger events. These numbers are observer
testimony only.

```text
extent   occurrences entering this extent   recurring occurrences
2        218,057                            218,057
5        218,054                            218,053
10       216,805                            213,486
20        21,348                             18,312
50         2,547                              2,441
100          675                                663
150          195                                187
183            4                                  2
184            2                                  0
```

The complete observer calculation performed 3,339,588 one-coordinate
extensions and formed 480,015 distinct result groups in 2.66 seconds. It did
not instantiate every possible span or every possible relation.

This does not predict Seed runtime cost. A responsible lifecycle may record
several occurrences per extension, and validation cost remains separate.

## Current live boundary

Current runtime establishes:

```text
exact material
↓
adjacent position results
↓
D.2 addressed local coordinates
↓
shared-position / ordered-path, where invoked
↓
fixed three-coordinate Compare, where invoked
```

It does not currently establish the variable-extent road:

```text
minimal exact extent result
↓
complete Compare result population for that extent
↓
count / recurrence of the complete result population
↓
one-coordinate extension of every recurring occurrence
↓
only newly introduced Compare subjects
```

The nearest removed implementation testimony names the middle two operations,
but its fixed coordinate surface and retired wrappers are not current owners.

The exact live vacancies are:

1. an exact result carrying one variable bounded coordinate extent and its
   complete incremental Compare support;
2. current Measurement physiology over the complete Compare result population;
3. exact count and recurrence over that result population;
4. an extension occurrence addressed by the recurrence result and the next
   adjacent source coordinate;
5. ordinary uptake from each yielded result, without a central chooser.

No generic dispatcher is required to prove the first small road. No Candidate,
global ledger scan, extent cap, ranking, or semantic classification supplies
these coordinates.

## Disposition

```text
D.2 and shared-position as sibling consumers                 retained
fixed three-coordinate Compare as universal extent           refused
first/final Compare privilege                                already refused
minimal ordered extent from adjacency                        established
complete variable-extent Compare surface                     not live
incremental new-coordinate Compare work                      exact orientation
recurrence as extension discriminator                        exact orientation
recurrence pruning preserves recurring larger equality shape proved
automatic result uptake                                      not live
```

The next implementation should begin with the smallest repeated-material
witness and prove exactly two successive extents without a fixed extent-three
API. It should preserve prior Compare work and record only the comparisons
introduced by the next coordinate. Corpus scale follows only after that road
is exact and its small scaling is measured.
