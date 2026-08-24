# Source-carried relation Assertion owner investigation 001

## Status

Findings only from current tip `5cdd0015`.

This investigation changes no active Book clause, witness grammar, runtime, or
test. It does not introduce a source-relation object or Responsibility.

## Answer

The live source-position road now yields one exact reusable material result
`W`. `W` preserves the exact source-derived subject of its Measurement, its
exact material, the recurrence and coordinate-Measurement result references it
used, the exact produced results carrying that material, the exact source
positions, completeness boundary, Authority, Scope, Locality, limits,
conflicts, Unknown, Responsibility, Act occurrence, Yield, and direct
Responsibility ownership in current Standing.

`W` carries no Assertion.

No active Responsibility owns this crossing:

```text
exact reusable material W
+ exact source occurrence and source coordinates
-> responsible occurrence saying that the source carried
   one exact relation Assertion
```

Active `01.Source.F` begins after that crossing. It preserves supplied material
*already carrying* an Assertion. Active Recording also begins with an already
exact Assertion. Candidate begins with exact source Assertions, not arbitrary
results. Compare begins with exact subjects and an exact Compare rule. Relation
Standing begins with an already formed relation Assertion and requires a later
exact relation occurrence.

Therefore no implementation is warranted by active law. The exact stop is:

```text
W is exact and reusable
-> no active owner makes W, or source material containing W,
   carry a relation Assertion
-> STOP
```

The runtime also contains a separate compression at this boundary. Its
Candidate source reader labels every replayed `result_identity` as a source
Assertion identity even when the result carries no Assertion. Applied directly
to `W`, it invents a source-Assertion reference whose carried Yield, Scope,
limits, and Unknown are all absent. That behavior cannot supply the missing
owner.

## 1. Exact stopping point at W

The producer added before this investigation is one declared
`01.Source.D` Measurement:

```text
one recurrent complete Compare finding
+ corresponding exact-material findings
+ the same exact produced-result references for every source position
+ consecutive source positions carried by every produced result
-> Measurement Act occurrence
-> Yield
-> exact material result W
```

For the proving source `a+aa+a`, the result later rendered by the operator is:

```text
W.exact_material = b"a+a"
```

The caller does not provide that material, its coordinate count, the `+`
material, or a selected source position. `_recurrent_result_material_payload()`
recovers the exact material from the already recorded recurrence and
coordinate-Measurement findings and then verifies it against every referenced
produced result (`seed_runtime/source_position_recurrence.py:1953-2125`).

The result subject is exact:

```text
coordinate Measurement result reference
recurrence Measurement result reference
recurrence finding reference
exact produced-result references
coordinate count
```

The result also carries the material findings it used, the source positions
carried by each produced result, its completeness boundary, Authority, Scope,
Locality, limits, conflicts, and Unknown. Its limits expressly refuse word,
numeral, operator, expression, number, grammar, or meaning. The ordinary
Responsibility -> Act occurrence -> Yield -> result chain is recorded at
`seed_runtime/source_position_recurrence.py:2226-2249`.

Thus the stopping point is not an unowned byte string. It is an exact
Measurement result that later work may address by reference.

It is still only exact material.

```text
exact material W
!= Assertion
!= relation Assertion
!= source saying that an Assertion occurred
!= relation Standing
!= domain subject represented by W
```

## 2. What ingress presently establishes

Active `01.Source.H` requires material acquisition to preserve its source role,
source boundary, provenance, Authority, Scope, Locality, known loss, limits,
and Unknown. It does not say that acquired material carries a relation
Assertion.

The live source-specific acquisition result is equally explicit:

```python
MATERIAL_RESULT_UNKNOWN = ("represented_relation", "source_relation")
```

(`seed_runtime/material_acquisition.py:12`)

For Witness material, the live result carries exact bytes, `source_role = this
Witness`, an exact source boundary, known loss, provenance occurrence
references, and a Locality relation. Its evidence boundary states that the
represented relation is Unknown
(`seed_runtime/witness_material_acquisition.py:130-184`). Operator acquisition
preserves the same two Unknown coordinates.

This is a positive refusal:

```text
source supplied exact material
-> exact acquisition result and exact Locality relation
-> represented relation: Unknown
-> source relation: Unknown
```

Neither a filename, acquisition source name, source boundary, provenance,
Locality, recurrence, nor exact material fills either Unknown.

## 3. Existing continuations

| Existing work | Exact starting subject | Exact result | Disposition from W |
|---|---|---|---|
| `01.Source.D` Measurement | one already addressed exact subject under a declared rule | findings and their exact coordinates | Accepted as the producer of W. Another Measurement would require another exact subject and rule; it does not identify a source claim by itself. |
| `04.Compare` | exact subjects under one exact Compare rule | distinctions established by that rule | Refused as the missing crossing. Compare cannot decide that material occupies the three relation-Assertion positions or that a source asserted their relation. |
| `01.Source.E` Candidate preservation | one exact addressed source result | Candidate retaining its exact source references | Not a relation-Assertion producer. It preserves neutral material. |
| `01.Source.E.1` Candidate from exact results | one exact source Assertion, or two distinct source Assertions in source order | Candidate with source Assertion references and Act-local roles; relation Unknown | Refused. W is not an exact source Assertion, and Candidate establishes no source Assertion relation. |
| `01.Source.F` | supplied material already carrying a relation Assertion | the same Assertion with its source coordinates preserved | Accepted as the first downstream preservation law. Refused as the producer of the premise it requires. |
| `05.Recording.A` | one already exact Assertion | record preserving that Assertion and its source coordinates | Refused as the producer. Recording is later preservation. |
| Carriage | exact content already carried by one exact Act occurrence | one exact content-to-Act-occurrence relation | Refused. Carriage does not decide that source material is relation-Assertion content. |
| Emission | one exact source material result and one exact destination boundary | exact accepted material and count, or exact failure | Refused. Emission changes the addressed boundary of material; it establishes no represented or source relation. |
| legacy runtime using the removed `Representation` name | an exact material result under its declared emission road | bounded material for emission | Refused. Its active constitutional neighbor is Emission, and its runtime tests expressly preserve no represented relation, source relation, or truth. |
| `01.Standing.D.1` Assertion coordinates | exact content already addressed as one Assertion subject | the coordinates the Assertion must carry | Refused as a producer. This clause specifies the already addressed Assertion. |
| `01.Standing.E` relation Standing | an already formed relation Assertion with first subject, exact relation content, and second subject | Standing only after an exact relation occurrence and its warranting coordinates | Refused as source testimony formation and as automatic acceptance of testimony. |

### 3.1 Candidate does not bridge W to Assertion

The constitutional refusal is already exact. Active `01.Source.E.1` requires
every exact **source Assertion** separately or every distinct pair of source
Assertions. Its result retains source Assertion references and Act-local roles,
and its final sentence requires a responsible relation occurrence for a
relation (`book_of_seed/chapters/07_measurement_and_candidates.md:46-64`).

The live Candidate source reader widens that premise incorrectly.
`_references_carried_by_result()` does this for every replayed result:

```python
result_address = material.get("result_identity")
if result_address:
    references.append(
        source_Assertion_reference(
            assertion_coordinate="result",
            assertion_address=result_address,
        )
    )
```

(`seed_runtime/candidate_results_from_exact_result_assertions.py:157-179`)

No check establishes that the result is an Assertion.

A disposable exact probe at `5cdd0015` produced `W = b"a+a"` and called that
reader directly on W. W carried no `assertions` coordinate. The reader still
returned:

```text
assertion_identity   = W.result_identity
assertion_coordinate = result
Yield                = absent
Scope                = absent
limits               = absent
Unknown              = absent
```

This is not the desired weaker source claim. It is the compression:

```text
exact result identity
-> treated as source Assertion identity
```

The complete boundary read is not merely over-broad; it currently stops before
reaching W. An earlier position Measurement carries an `assertions` dictionary
that is not one Assertion with an Assertion identity. The Candidate reader
tries to read it as one Assertion and raises:

```text
Candidate production requires one exact Assertion carried by a result
```

So the current Candidate continuation has two independently observed defects:

```text
some non-Assertion results are labeled source Assertions
some result finding dictionaries are treated as one Assertion and refused
```

Neither defect authorizes Candidate to form a relation Assertion. They show
that the Candidate source aperture currently fails to preserve the active
distinction:

```text
exact result
!= exact source Assertion
```

The Candidate result itself still carries `relation = Unknown` and states that
its Act establishes no source Assertion relation
(`seed_runtime/candidate_results_from_exact_result_assertions.py:779-817`).

### 3.2 Source.F and Recording begin one step later

Active Source.F says:

```text
Supplied material carrying an Assertion carries one exact relation as its
relation. Carriage preserves the Assertion and its source coordinates.
```

(`book_of_seed/chapters/04_source_coordinates.md:24-27`)

The subject is already `material carrying relation Assertion` in the machine
witness. The Act is preservation, and the result is `preserved relation
Assertion`. Source.F supplies neither the three relation-Assertion occupants
nor an occurrence establishing that the source carried that Assertion.

Active Recording.A similarly says that a recording occurrence preserves one
exact Assertion (`book_of_seed/chapters/09_recording_and_preservation.md:10-13`).
It does not turn recorded bytes or W into the Assertion it preserves.

## 4. Smallest recovered topology

The smallest topology is not one edge. It contains two exact relations that
must remain distinct.

First, the proposed content has the already active relation-Assertion anatomy:

```text
relation Assertion C
├── first subject A
├── exact relation content R
└── second subject B
```

Second, saying that one exact source occurrence carried C is itself a relation:

```text
exact source occurrence Q
-- exact source relation -->
relation Assertion C
```

The second relation warrants only this bounded finding:

```text
Q carried C under these exact source coordinates and limits
```

It does not warrant C's relation content as Seed Standing.

The complete road would therefore have to be:

```text
exact material W and exact source coordinates
-> [vacant source-specific Responsibility and Act]
-> Yield one exact relation Assertion C
   carrying A, R, B, source, provenance, Authority, Scope,
   Locality, limits, conflicts, and Unknown
-> one exact responsible source-relation occurrence connects Q to C
-> Source.F may preserve C and its source coordinates
-> Recording may preserve C

later, separately:

C becomes the subject-to-Act position of an exact later Responsibility
-> Applicability / required Admission / Participation
-> responsible relation occurrence
-> Yield result
-> relation Standing under 01.Standing.E
```

Active law establishes the destination anatomy and the later preservation and
Standing requirements. It does not establish the source-specific
Responsibility, Act, or rule at the vacant step.

History is useful testimony here. Before the active Book reordering at
`f956b6fd`, `09_assertion_source_coordinates.md` explicitly kept these apart:

```text
the relation "source S supplied or asserted Assertion A"
is itself an Assertion

source relation Standing != asserted-content Standing
```

The active reordering removed that explicit clause and retained the conditional
Source.F preservation rule. History therefore supports the distinction but
does not supply an active owner.

Earlier `relation proposal` investigations cannot fill the gap. They depended
on removed External and Representation grammar, found no established joins
from proposal to Candidate, testimony, claim, or Standing, and found no live
runtime producer. Restoring those names would restore an underdefined road, not
recover the current owner.

## 5. Source claim versus relation Standing

The exact dividing line is the subject and result of the responsible
occurrence.

For the source relation:

```text
subject of Responsibility:
    exact Q-to-C source relation

warranted result:
    Q carried C under exact source coordinates and limits
```

For the relation described by C:

```text
subject of later Responsibility:
    exact A-R-B relation Assertion C

warranted result:
    only the relation established by that later Act
    under its Authority, Scope, Locality, limits, conflicts, and Unknown
```

The first result may become Evidence for the second Responsibility. It is not
the second result.

```text
source carried C
!= C is established

C is recorded
!= C is established

C participates in a later Act
!= that Act establishes C unless its exact Responsibility and rule do so
```

This is where source testimony still differs from warranted relation Standing.

## 6. Exact vacancy

The first vacancy is active law, not merely a missing Python function:

```text
no active Responsibility and Act takes
    exact source-derived material/result references
    plus an exact source occurrence and source rule
and yields
    one exact source-carried relation Assertion
without establishing that Assertion's relation as Seed Standing
```

The required rule cannot be generic co-presence. It must establish why these
exact source-carried coordinates are the first subject, exact relation content,
and second subject of C, and why Q is the source occurrence that carried C.

Active law does not currently choose between:

```text
the source boundary directly supplies those exact coordinates as testimony

or

a prior independently warranted source rule makes them addressable
```

Raw recurrence does neither.

Because no active owner is established, there is no smallest live
implementation vacancy yet. Adding a generic Assertion-formation,
interpretation, classification, meaning, or learning Responsibility would
author the missing rule rather than recover it.

The Candidate source-reader compression is a separate repair candidate. The
active distinction already warrants refusing arbitrary results as source
Assertions. This investigation does not repair it because its removal would
not create the missing source-specific owner.

## 7. Minimal proving source

There is no honest positive **bytes-only** witness for the vacant crossing.
Any bytes-only proof that expects Seed to recover A, R, and B currently supplies
the missing source rule through the test.

The smallest proof after an owner is recovered should instead expose the
epistemic difference directly.

Use opaque exact identities and two otherwise identical acquisition roads:

```text
road one: exact material only

    acquired material M0
    exact reusable results WA, WR, WB
    no source-carried relation coordinates

    expected:
        exact material preserved
        source relation Unknown
        no relation Assertion

road two: source testimony under one exact source-specific rule Q-rule

    source occurrence Q0 carries exact references:
        first subject WA
        exact relation content WR
        second subject WB

    source occurrence Q1 uses the same exact rule with different opaque
    exact material references:
        first subject WC
        exact relation content WR
        second subject WD

    expected:
        one exact C0 and one exact C1 preserve the exact source references,
        Q0/Q1, rule, Authority, Scope, Locality, limits, conflicts, and Unknown
        neither C0 nor C1 receives relation Standing merely from source carriage
```

The role coordinates in road two must be testimony actually carried by Q-rule,
not positions selected by the test after reading the bytes. The source-specific
Responsibility must state how that rule is warranted at the exact source
boundary. Renaming every opaque identity must leave the result topology
unchanged.

Required controls:

```text
same bytes without Q-rule                  -> no Assertion
same three references merely co-present    -> no Assertion
missing source occurrence                  -> refuse
missing one relation-Assertion coordinate  -> refuse
changed source/result reference            -> refuse
changed Authority, Scope, or limit          -> refuse
source-carried C without later relation Act -> C preserved; relation Standing absent
```

Repeated raw arrangements may be useful later as curriculum material. They can
expose invariant source positions and exact reusable material. They cannot be
the positive proof of source testimony until an independently warranted source
rule connects those positions to the relation-Assertion anatomy.

## 8. Required refusals

### Exact material to domain subject

```text
exact material W
!= what W may represent in an external domain
```

`b"2"` remains exact material. This investigation establishes no number,
digit, numeral, letter, operator, word, or other domain subject.

### Source testimony to truth

```text
source Q carried relation Assertion C
!= relation C has Standing in this Seed
```

The first relation can be warranted while the second remains Unknown.

### Co-presence to relation

```text
A, R, and B occur in one source boundary
!= A-R-B relation Assertion exists
```

Adjacency, chronology, matching occurrence counts, shared produced-result
references, and source order do not manufacture the relation.

### Recurrence to meaning

```text
the same exact material or Compare surface recurs
!= that material has one represented relation or meaning
```

Recurrence may make W addressable. It does not supply a source relation or
domain interpretation.

### Developer segmentation to Seed discovery

```text
test selects three spans and labels them A/R/B
!= Seed discovered relation-Assertion coordinates
```

A positive preservation test may begin with source testimony that explicitly
carries its own coordinates, provided the test reports that those coordinates
were supplied testimony. It must not describe their preservation as discovery
from raw bytes.

## 9. Final disposition

```text
W exact and reusable                                      established
W directly owned by its Measurement Responsibility       established
W carries a relation Assertion                            not established
material acquisition carries source relation             explicitly Unknown
Source.F preserves an already carried Assertion           established
Recording preserves an already exact Assertion            established
Candidate preserves exact source Assertion references     established
Candidate forms a relation Assertion from W               not established
Candidate may treat every result as a source Assertion    runtime compression
source carriage establishes asserted relation Standing    refused
source-specific owner forming source-carried C from W     vacant in active law
```

The first lawful continuation from W has not been recovered. The repository
does, however, now expose the gap precisely:

```text
exact reusable material
-> source-carried relation Assertion
```

is neither Measurement, Compare, Candidate, Source.F, Recording, Carriage,
Emission, nor relation Standing. Until an exact source-specific Responsibility
and rule are independently established, the correct result is refusal and
`source_relation: Unknown`.
