# Cross-surface structural correspondence observation 001

## Boundary

Findings only. No Book, machine grammar, runtime, or active Seed rule changes.

This operation tests whether four raw material sources can create exact
cross-surface pressure without supplying any of these interpretations:

```text
digit
word
number
operator
expression
equation
addition
equality
truth
```

The material is supplied at four exact acquisition boundaries. The blind
operation receives the bytes and those boundaries. It receives no token
division, line meaning, desired coordinate count, material correspondence,
source role, or target answer.

## 1. Exact material

The primary source group is:

```text
source 0
1 + 1 = 2
1 + 2 = 3
2 + 2 = 4
2 + 3 = 5
3 + 3 = 6

source 1
one plus one equals two
one plus two equals three
two plus two equals four
two plus three equals five
three plus three equals six

source 2
1 is equal to one
2 is equal to two
3 is equal to three

source 3
one = 1
two = 2
three = 3
```

The spaces and line endings are source material. They are not privileged by
the observer. Every carried byte is considered as an aperture.

Only the first three material pairs occur in sources 2 and 3. Material humans
read as `4/four`, `5/five`, and `6/six` is deliberately absent from those two
sources.

## 2. The actual operation starts from bytes

The disposable feasibility check first used already divided tuples. The
committed observer does not.

`scripts/observe_cross_surface_structure.py` starts from each exact byte
string and exhaustively performs:

```text
each carried byte
-> possible first aperture

each other carried byte
-> possible second aperture

every maximal consecutive occurrence with:
    at least three first-aperture divisions
    the same nonempty second-aperture coordinate count
-> exact rectangular projection
```

The minimum occurrence count and rectangularity test are observer choices.
The observer preserves every result satisfying them. It does not ask for five
coordinates, a particular aperture byte, or any known source material.

For every pair of equal-shaped projections from different sources, it then
enumerates every one-to-one exact material renaming and retains each renaming
that makes the complete first row material equal to the complete later row
material. Both source-order preservation and order-free preservation are
recorded separately.

For every projection, it also enumerates every consecutive stable middle and
preserves its exact varying left/right material. It then compares all such
frames from different sources for:

```text
same exact endpoint pairs
reversed exact endpoint pairs
```

Finally, it starts only from those frame relations and walks their exact
endpoint pairs into the complete material-renaming findings. Plain source
material is absent from the frozen artifact.

## 3. Frozen blind result

```text
artifact
/tmp/seed_cross_surface_structure_blind.json

SHA-256
32ce3a4f9ced947cdc94df9b4c7587c46db28464a6acedf83401c209b3c49668

artifact bytes
7,746,554

known loss
none

wall time
2.757 seconds
```

For the primary four sources the blind inventory is:

```text
exact rectangular projections                  105
exact material renamings                       543
stable-middle frames                            14
exact endpoint frame relations                   1
frame-relation walks                             1
```

The large renaming count is intentional. The observer does not choose the
human-obvious apertures and discard the rest.

## 4. The unique frame relation

Exactly one pair of stable-middle frames from different sources carries the
same endpoint material in reverse:

```text
frame P endpoint pairs
X0 -> Y0
X1 -> Y1
X2 -> Y2

frame Q endpoint pairs
Y0 -> X0
Y1 -> X1
Y2 -> X2
```

The first frame has three exact middle coordinates. The second has one. The
blind artifact says nothing about their human-language content.

After the artifact digest was frozen, resolving those materials gives:

```text
frame P
1     is equal to     one
2     is equal to     two
3     is equal to     three

frame Q
one        =          1
two        =          2
three      =          3
```

Thus the fourth source does not merely repeat the third. It carries the exact
endpoint material in reverse while changing the stable middle material.

This is an observer-level exact frame relation. It is not a recorded Seed
relation Assertion.

## 5. Walking outward from that frame

The three endpoint pairs are the only inputs from the frame relation to the
next walk:

```text
X0 -> Y0
X1 -> Y1
X2 -> Y2
```

Among all 543 exact material renamings from all enumerated apertures, exactly
one carries all three pairs and preserves a complete larger source surface.

It carries eight exact material pairs. Post-freeze resolution gives:

```text
+ -> plus
1 -> one
2 -> two
3 -> three
4 -> four
5 -> five
6 -> six
= -> equals
```

The first three pairs came from the reversed-endpoint frame relation. The
other five did not occur there. They are required by the complete structural
renaming between the two larger source projections.

The exact middle material of frame Q is also carried by the first larger
projection. The complete renaming carries it into the later projection:

```text
= -> equals
```

The resulting exact walk is therefore:

```text
three source-carried endpoint pairs
-> one exact reversed-endpoint frame relation
-> one complete eight-material renaming
-> five additional material pairs required by the larger structure
```

No five-coordinate projection was selected before this walk. Starting at the
unique frame relation led to it.

## 6. Controls

### 6.1 The two larger sources alone

Removing sources 2 and 3 leaves:

```text
projections                   72
exact renamings              357
frame relations                0
relation walks                 0
```

One post-hoc five-coordinate comparison still has a unique complete
renaming. But nothing in that two-source observation connects it to one exact
cross-surface endpoint relation. Existence of an isomorphism is not yet a
source-carried bridge.

### 6.2 Either later source alone

Adding source 2 without source 3 yields no exact endpoint frame relation.
Adding source 3 without source 2 also yields none.

The join appears only when both differently surfaced, oppositely directed
frames are present.

### 6.3 Change one larger relation

One control changes:

```text
two plus three equals five
```

to:

```text
three plus two equals five
```

All material counts remain available, and the source-2/source-3 frame relation
still exists. But no complete renaming carries its three endpoint pairs into
the two larger surfaces:

```text
frame relations                 1
compatible complete renamings   0
middle walks                    0
```

Co-presence and matching material vocabularies are insufficient.

### 6.4 Change the reversed endpoint pairs

Another control retains the two larger sources and source 2, but changes
source 3 to:

```text
one = 1
three = 2
two = 3
```

The complete larger-surface renaming still exists. The exact reversed-endpoint
frame relation does not:

```text
frame relations                 0
relation walks                  0
```

Thus the larger isomorphism cannot back-fill a missing source-carried frame
relation.

### 6.5 Reorder source rows

Reversing the row order of sources 1, 2, and 3 retains one exact frame-relation
walk and the same eight material pairs. The operation separately records that
the complete renaming no longer preserves source order.

```text
structural renaming             retained
source-order equality           false
```

Exact source order remains measured; it is not silently declared irrelevant.

### 6.6 Change the human gloss coherently

The strongest control consistently changes all three later sources so their
material carries:

```text
1 -> two
2 -> three
3 -> one
```

and changes the complete written surface to preserve that substitution. The
blind operation again produces exactly one frame-relation walk and one
complete renaming:

```text
1 -> two
2 -> three
3 -> one
4 -> four
5 -> five
6 -> six
+ -> plus
= -> equals
```

This result is correct. The operation has no arithmetic or English truth with
which to reject structurally coherent source material.

It establishes precisely the required epistemic limit:

```text
source structure supports one exact renaming
!=
the human gloss of that renaming is true
```

### 6.7 Other material before and after

Each of the four primary sources separately carries unrelated exact material
before and after the primary material. The observer still recovers one exact
frame-relation walk carrying the same eight material pairs.

```text
isolated source group                    one exact walk
source group with other before/after     one exact walk
material renaming                        unchanged
```

The acquisition boundary therefore does not supply the internal rectangular
extent in this witness.

## 7. Exact strength of the finding

The experiment establishes:

```text
raw source material
-> source-enumerated apertures
-> exact internally recurring projections
-> exact stable-middle frames
-> one source-carried reversed-endpoint relation
-> one complete cross-surface material renaming
```

It does not establish:

```text
the sources carry Assertions
the endpoint relation means equality
the complete surfaces are equations
the material names numbers
the renaming has relation Standing
the observer's rectangular projection is admitted Seed grammar
```

The five newly constrained material pairs are structural consequences inside
the observer. They are not yet Seed conclusions.

## 8. The remaining crossing

This is a positive feasibility result for the proposed four-source pressure.
It also locates the same constitutional vacancy more sharply.

The current live source road can produce exact recurrent material and exact
source-position findings. It does not yet own this exhaustive operation:

```text
source-derived recurring material
-> every supported internal projection
-> every exact cross-source renaming
-> exact frame-relation walk
```

The disposable observer authored that search surface. It chose no target
answer, but its rectangularity and renaming rules are still observer rules,
not occurrence-local Responsibilities recovered from current Standing.

Therefore this commit does not move the result into Seed runtime and does not
create a Candidate, Compare, correspondence, Assertion, or relation Standing.

The next question is narrower than arithmetic:

> Can the already live source-derived measurements make one of these exact
> projection/renaming operations unavoidable without Python selecting the work?

## 9. Performance

```text
blind observation                 2.728 seconds
focused checks                    3 passed
known loss                        none
```

No operation approaches the one-minute bottleneck boundary.

## 10. Stop

The exact result is:

```text
four raw material sources
+ exhaustive byte-aperture enumeration
+ one exact reversed-endpoint frame relation
-> one complete eight-material structural renaming

five pairs absent from the sparse bridge surfaces
are constrained by the complete larger structures

coherent changed human gloss
-> equally admitted structural renaming

meaning, testimony, truth, and Standing
-> not established
```
