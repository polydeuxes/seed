# Source Assertion acquisition owner investigation 001

## Status

Findings only from current tip `ed5e52f3`.

The Candidate correction at that tip removes the false continuation:

```text
exact result identity
-> source Assertion identity
```

This investigation changes no active Book clause, witness grammar, runtime, or
test.

## Question

What does active Seed grammar require when a source boundary supplies an
Assertion rather than supplying exact bytes alone?

The question is not how Seed derives a relation Assertion from raw material.
That road remains vacant at `bce802da`.

The narrower question is whether an external source may supply the three exact
relation-Assertion coordinates as source testimony, and what existing Seed
work can preserve that testimony without establishing its relation as Seed
Standing.

## Finding

Active grammar already owns the **preservation** half:

```text
01.Source.F

subject:
    supplied material already carrying a relation Assertion

Act:
    preserve that relation Assertion

result:
    preserved relation Assertion with its source coordinates
```

Source.F therefore does not need to discover first subject, exact relation
content, or second subject. Those coordinates may be supplied testimony.

The live acquisition roads do not admit that subject.

They admit:

```text
exact bytes
source role
source boundary
provenance occurrence references
known loss
Locality
```

and explicitly preserve:

```text
represented relation: Unknown
source relation: Unknown
```

No live event carries exact supplied relation-Assertion coordinates into
Source.F. No runtime module implements Source.F.

Thus the present gap is:

```text
source boundary supplies exact relation Assertion C
-> no live source-specific acquisition result can carry C
-> Source.F has no live exact subject
```

This is narrower than source-derived Assertion formation. It is also weaker:
the result would warrant only that this exact source supplied C under exact
source coordinates and limits. It would not warrant the relation asserted by
C.

Active grammar establishes enough to locate the floor. It does not yet specify
one exact source-specific Responsibility and Act that crosses it. Therefore no
implementation is warranted in this investigation.

## 1. Bytes and supplied Assertions are different source subjects

Active Source law currently exposes three relevant boundaries.

### 1.1 Source.A preserves what one responsible occurrence actually receives

`01.Source.A` says one responsible Act occurrence preserves supplied material,
source role, source occurrence, provenance, Authority, Scope, Locality, known
loss, limits, conflicts, and Unknown carried at its boundary.

This clause is generic preservation law. It does not say that every supplied
material occurrence is bytes, and it does not say that supplied material is an
Assertion.

### 1.2 Source.F begins with an already carried Assertion

`01.Source.F` says:

```text
Supplied material carrying an Assertion carries one exact relation as its
relation. Carriage preserves the Assertion and its source coordinates.
```

The active machine witness makes the boundary equally explicit:

```text
subject        material_carrying_relation_Assertion
Responsibility preserve_relation_Assertion_source_coordinates
exact Act       preserve_relation_Assertion
result          preserved_relation_Assertion
```

Source.F is not missing once its subject exists. It owns preservation of that
exact supplied Assertion.

It does not own either of these earlier questions:

```text
which bytes constitute C?

what source-specific occurrence made C an exact supplied subject?
```

### 1.3 Source.H currently admits exact material results

`01.Source.H` bounds one source boundary and one acquisition Act, then yields
one exact material result preserving source coordinates and Unknown.

The live generic reader admits only two source-specific result roads:

```text
Witness material acquisition
operator material acquisition
```

Both yield exact bytes. Neither yields an Assertion result.

`01.Source.I` also requires operator-supplied and Witness-supplied material to
have separate source Responsibilities and occurrences. Any future supplied
Assertion road cannot erase that separation by using one universal source
event.

## 2. Exact live acquisition trace

The Witness acquisition call accepts only:

```text
ledger
Locality identity
exact bytes
source boundary
known loss
provenance occurrence references
read occurrences
```

It allocates one acquisition Act identity, occurrence identity, and result
identity. The result carries:

```text
exact bytes
source role = this Witness
source boundary
known loss
provenance occurrence references
Locality relation:
    exact material --Locality--> this Seed
```

The result carries no:

```text
Assertion identity
first subject
exact relation content
second subject
source-to-Assertion relation occurrence
```

Its shared acquisition reader fixes these exact Unknown coordinates:

```python
MATERIAL_RESULT_UNKNOWN = ("represented_relation", "source_relation")
```

Operator acquisition reaches the same exact material result boundary. It does
not gain relation coordinates merely because the operator supplied the bytes.

The resulting topology is honest:

```text
exact source occurrence Q
-> acquisition Act occurrence
-> Yield exact byte material M
-> M --Locality--> this Seed

represented relation: Unknown
source relation: Unknown
```

Source boundary text is not an Assertion. A provenance occurrence reference
is not a source relation. A Locality relation is not the asserted relation.

## 3. The apparently richer test road is byte acquisition

Two test files use an ordinary label suggesting that a source relation is
already known:

```text
tests/source_attributed_witness_material.py
tests/test_source_attributed_witness_material_acquisition.py
```

That label is not an active Seed coordinate.

The helper performs exactly this work:

```text
developer selects one corpus file
developer selects first line 126
developer selects 300 lines
each selected line enters record_witness_material_acquisition as exact bytes
```

The resulting tests establish:

```text
300 distinct material acquisition results
exact result references
source occurrence order
compiled-function invocation results
one admission result
one occurrence-position Measurement
```

They establish no relation Assertion and no source-to-Assertion relation. The
source boundary strings are developer descriptions such as:

```text
source-attributed Witness Material occurrence 0
```

Those strings do not make the source assert anything. The road terminates at
the same exact-byte acquisition result and the same Unknown relations as every
other Witness acquisition.

This test is useful evidence of the distinction:

```text
developer knows where corpus material came from
!= Seed carries an exact source relation
```

It is not hidden testimony ingress.

## 4. What a supplied relation Assertion must carry

An exact supplied relation Assertion `C` must satisfy the active relation
anatomy before Source.F can preserve it:

```text
C
├── first subject A
├── exact relation content R
└── second subject B
```

As an Assertion, C also carries:

```text
source
provenance
Authority
Scope
Locality
conflicts
limits
Unknown
Standing with exact established coordinates
```

The last item must not be overread. The source occurrence may warrant that C is
the exact Assertion it supplied. It does not thereby establish relation
Standing for A-R-B in this Seed.

The source connection must itself remain exact:

```text
source occurrence Q
-- source supplied -->
C
```

That exact relation requires its own subjects and responsible occurrence under
`01.Standing.D`. Source coordinates alone do not manufacture it.

The smallest complete input to Source.F is consequently not:

```text
bytes encoding A R B
```

It is:

```text
one exact source-specific occurrence Q
one exact relation Assertion C already carrying A, R, B
exact source coordinates connecting C to Q
exact Authority, Scope, Locality, limits, conflicts, and Unknown
```

Source.F may then preserve C. Recording may later preserve that exact C and its
source coordinates.

## 5. What this establishes

The source-side result may establish only:

```text
under the exact Authority and Scope of this source occurrence,
Q supplied relation Assertion C
```

It does not establish:

```text
C is true
C has relation Standing in this Seed
Q is authoritative beyond the declared Scope
the spelling of R reveals its meaning
C applies to any later Act
another source supplied the same C
```

This is the Seed equivalent of a supervised training signal kept within its
actual evidentiary boundary:

```text
source-provided structure
-> source-relative testimony
!= domain truth
```

Machine-learning labels, paired observations, targets, and rewards are useful
ordinary analogies. They provide no constitutional owner. The relevant lesson
is only that additional source structure is additional evidence; it is not a
property secretly recoverable from the input bytes alone.

## 6. Existing-owner audit

| Existing work | Exact ownership | Can it admit a source-supplied C? |
|---|---|---|
| Source.A | preserve every exact source coordinate carried at one responsible boundary | generic requirement only; it does not name the source-specific Act |
| Source.H Witness acquisition | exact Witness bytes and their source coordinates | no |
| Source.G operator acquisition | exact operator bytes and their Locality relation | no |
| Source.I | keep operator and Witness source Responsibilities separate | constrains a future road; does not produce C |
| Source.F | preserve supplied material already carrying relation Assertion C | yes, after C is an exact supplied subject |
| Recording.A | preserve an already exact Assertion and its source coordinates | yes, after Source.F or another exact producer; not acquisition |
| Candidate | preserve exact source Assertion references after they exist | no earlier production; relation remains Unknown |
| Compare | establish only distinctions under an exact Compare rule | no |
| Standing.E | establish relation Standing after C and its exact relation occurrence exist | no source acquisition |

The only active owner adjoining the desired input is Source.F. The missing
work is not a new generic Assertion producer after Source.F. It is the exact
source-specific occurrence by which C becomes Source.F's supplied subject.

## 7. History testimony

Earlier Book law stated the source distinction more directly:

```text
the relation "source S supplied or asserted Assertion A"
is itself an Assertion

source relation Standing != asserted-content Standing
```

That law was removed during the active Book reordering at `f956b6fd`. Active
Source.F retains its downstream preservation consequence but omits the exact
source-relation owner.

Older External/translation and relation-proposal work does not repair the
omission. Those roads used removed grammar, never established the proposal to
claim or testimony joins, and had no live runtime producer. They are evidence
that a supplied relation must retain source limits, not an implementation to
restore.

The history therefore corroborates:

```text
Q supplied C
!= C has relation Standing
```

It does not answer which current source-specific Responsibility owns Q
supplying C.

## 8. Minimal proving material after owner recovery

A valid first proof should not ask raw bytes to reveal the relation anatomy.
It should test the weaker supplied-Assertion road directly with opaque
identities.

### Exact source testimony

```text
source occurrence Q0 supplies:

C0
├── first subject U0
├── exact relation content V0
└── second subject W0

source occurrence Q1 supplies under the same source-specific rule:

C1
├── first subject U1
├── exact relation content V0
└── second subject W1
```

The source occurrences must carry the exact coordinates as testimony. The
test must not recover them by choosing three byte spans after reading the
material.

Expected result:

```text
Q0 supplied C0                              established
Q1 supplied C1                              established
C0 and C1 preserved with source coordinates established
U0-V0-W0 relation Standing                  not established
U1-V0-W1 relation Standing                  not established
```

### Controls

```text
same serialized bytes through byte acquisition only
-> represented relation Unknown
-> source relation Unknown
-> no C

same U/V/W references co-present without Q's source rule
-> no C

C without one of A/R/B
-> refuse

C without exact Q/source coordinates
-> refuse

changed source occurrence, Authority, Scope, Locality, or limits
-> refuse

rename every opaque identity while preserving exact relations
-> same topology
```

This proof would establish testimony acquisition only. It would not establish
learning from bytes, semantic grounding, or relation Standing.

## 9. Exact vacancy and stop

Active law currently leaves this subject unassigned:

```text
exact source occurrence Q
+ exact supplied relation Assertion C
+ exact source coordinates and warranting limits
-> ???? source-specific Responsibility and Act occurrence
-> C is an exact supplied subject of Source.F
```

Possible implementation names are not evidence. The missing work must not be
called a universal Assertion acquisition, testimony ingress, translation,
interpretation, or learning Act merely because those phrases describe the
problem in ordinary language.

Before a build, active grammar must recover:

```text
the exact source-specific subject
the exact Act
the responsible boundary
Authority
Scope
Locality
limits
required source relation
Yield result
```

It must also decide whether the operator and Witness require distinct Acts, as
Source.I strongly pressures, or whether one existing Act with separate exact
Responsibilities already suffices.

No current clause answers that question. Therefore:

```text
Source.F preservation owner                         established
live exact-byte acquisition                         established
live supplied relation-Assertion acquisition        absent
source-specific owner making C Source.F's subject   not established
relation Standing from source carriage              refused
implementation                                      STOP
```

## Conclusion

The repository does contemplate sources supplying more than bytes. Source.F
would preserve an exact relation Assertion supplied under exact source
coordinates. The live runtime, however, has no way to present that subject to
Source.F: both acquisition roads terminate at exact bytes with represented and
source relations Unknown.

The missing stair is therefore not meaning and not truth. It is the exact
source-specific responsible occurrence that lets Seed say:

```text
this exact source occurrence supplied this exact relation Assertion
```

while continuing to say:

```text
whether the asserted relation has Standing here: Unknown
```
