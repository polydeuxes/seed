# Material acquisition / Ingest Responsibility investigation 001

## Question

Curator testimony recovers the intended `Ingest` distinction as:

```text
inert material
↓
exact bounding occurrence
↓
material in one exact bounded position
```

`Ingest` did not originally name acquisition by identity. What exact bounding
distinction, if any, remains in generic Ingest after the operator-material
acquisition road records:

```text
one exact operator boundary
↓
one exact O1 acquisition occurrence
↓
one exact material result M
+
M --locality--> this Seed
```

This investigation compares the active material-boundary, acquisition,
operator-Ingest, generic-Ingest, and supplied-invocation roads from their
recorded Responsibilities and exact occurrences. It changes none of those
roads, the declared Measurements, active Book, Witness Grammar, or Ledger.

`Inert`, `bounding occurrence`, and `bounded position` are curator orientation
in this report. `Bounded` here does not establish truth, represented relation,
positive constitutional Standing, or later Participation. The pressure is
whether exact material has crossed from a source surface into one exact
recorded result with its occurrence, source boundary, Locality, loss,
provenance, limits, and Unknown preserved.

## 1. The five names cover four different shapes

### 1.1 `operator_material_boundary`

`operator_boundary_material` reads one framed byte population from the
operator stream and returns:

```text
exact bytes
EOF distinction
source-boundary material
known loss
```

It receives no Ledger and records no Responsibility, Act, occurrence, Yield,
result, Locality relation, Evidence, Authority, Scope, or provenance. It is
the mechanical operator sensor boundary, not a constitutional acquisition or
Ingest occurrence.

### 1.2 `operator_material_acquisition` / `01.Source.G`

O1 records one source-specific road:

```text
01.Source.G assignment occurrence
↓
Responsibility:
preserve one exact material result supplied at one operator boundary
↓
exact Act and Act occurrence
↓
operator boundary supplies exact material M
↓
Yield
↓
exact material result occurrence O1
+
M --locality--> this Seed
```

The assignment and result carry the recorded bounded-replay source reference,
result boundary, Evidence, Authority material, Scope, limits, Unknown,
material, boundary, loss, Yield, and the Locality relation. O1 is the ordinary
console contact occurrence. This report does not promote bounded replay into
positive constitutional Standing.

Those coordinates also mean O1 now performs the operator material's
inert-to-bounded crossing. The boundary reader supplies an unrecorded
`OperatorBoundaryMaterial`; O1 turns it into one exact recorded material
result under a source boundary, occurrence, result boundary, Scope, loss,
Unknown, and Locality relation. O1 is not merely contact beside an independent
Ingest crossing.

### 1.3 `operator_ingest`

`run_operator_ingest` records no independent Responsibility, assignment, Act,
occurrence, Yield, or result. With an O1 reference, it:

1. rereads O1 through its family reader;
2. requires the same Locality identity, exact bytes, operator boundary, and
   known loss;
3. calls generic `ingest_material` with those same coordinates; and
4. records O1 as provenance of the new generic Ingest result.

It is a runtime adapter from O1 to generic Ingest. Its function boundary does
not establish another constitutional relation by identity.

### 1.4 `material_ingest`

Generic Ingest was recovered to record:

```text
Responsibility material:
preserve exact material supplied at one source boundary
↓
Act Evidence event
↓
Evidence of Yield relation
↓
exact material result I
```

This is the runtime shape intended to transform externally supplied material
into one exact bounded material occurrence. It accepts any nonempty scalar
`source_role`, `source_boundary`, and
`locality_identity`. It records no Responsibility-assignment occurrence. Its
Authority is `unestablished`. Its locality coordinate is a scalar
`scope_locality` label, not an exact Locality relation occurrence with
Locality Evidence. Both generic Ingest event kinds point to `02.Acts.A`, not
to a recovered source-specific Responsibility clause.

Generic Ingest therefore records an Act/Yield/result-shaped bounding road. It
does not currently record the assignment and source-specific relation
physiology that would establish the complete common constitutional boundary.

### 1.5 `supplied_invocation_material`

One supplied system occurrence is mechanically distinct from O1. The provider
hands a `SuppliedSystemMaterialOccurrence` Python value to a callback. Before
generic Ingest, that value has no Ledger occurrence or material-result
identity. In this road generic Ingest still performs the intended crossing:

```text
operator command material occurrence
↓
06.Locality.D operator-invocation Locality relation
↓
provider supplies exact system material S at a distinct source boundary
↓
generic Ingest result in the destination Locality
```

Before calling generic Ingest, the supplied-material adapter validates:

- the command occurrence;
- the exact operator-to-invocation Locality relation;
- the destination Locality;
- the distinct supplied boundary;
- the exact source bytes and known loss; and
- ordered references to selected prior supplied occurrences.

Its generic Ingest result records `source_role = system` and ordered
provenance beginning with the command occurrence and Locality-relation result.
Those are real differences from ordinary O1 contact. They are validated by
the supplied-material adapter and related family readers, not established by
generic Ingest's scalar source role or locality label.

The required command occurrence is itself typed as a generic operator Ingest
result, and its current invocation classification includes a host byte-prefix
predicate. The supplied-system road therefore depends on generic Ingest on
both sides of the Locality relation. That dependency is exact runtime
testimony, not a constitutional warrant for generic Ingest.

## 2. Responsibility-first comparison

| Road | Exact source boundary | Recorded Responsibility / assignment | Act / Yield / result | Exact Locality relation | Authority / Scope | Provenance | Current consumers |
|---|---|---|---|---|---|---|---|
| operator material boundary | operator stream frame | none | none | none | none | none | O1 recorder |
| O1 acquisition | one exact operator boundary | `01.Source.G`; subject-specific assignment recorded | exact acquisition Act, occurrence, Yield, bounded material result | `M --locality--> this Seed`, carried by O1 | recorded active Book Authority material and exact Scope | bounded-replay source boundary and addressed Representation | Representation, bounded replay, operator-Ingest adapter |
| operator-Ingest adapter | reuses O1 boundary | none of its own | invokes generic Ingest | none of its own | none of its own | requires O1, passes O1 reference | console bridge |
| generic Ingest I | supplied scalar boundary | responsibility string, no assignment occurrence | generic bounding Act Evidence, Yield relation, exact material result | no; locality label only | Authority unestablished; textual evidence/locality scope | exact caller-supplied occurrence references | declared Measurements, Locality replay, invocation road, downstream Measurement/Compare physiology |
| supplied system occurrence | provider boundary in invocation Locality | no source-specific acquisition assignment recorded here | generic Ingest Act/Yield/result | destination Locality relation is recorded separately by `06.Locality.D`; no `S --locality--> this Seed` relation in generic Ingest | provider adapter preserves known loss and provenance; generic Authority remains unestablished | command, Locality result, selected prior supplied occurrences | declared Measurements and later invocation-material physiology |

## 3. The exact O1 to I overlap

For an ordinary operator turn, current runtime records:

```text
O1 exact material M == I exact material M
O1 source boundary  == I source boundary
O1 Locality label   == I Locality label
O1 known loss       == I known loss

O1 occurrence       != I occurrence
O1 Act occurrence   != I Act occurrence
O1 result identity  != I result identity
I provenance        == (O1 occurrence,)
```

The generic Ingest responsibility says:

```text
preserve exact material supplied at one source boundary
```

The O1 responsibility says:

```text
preserve one exact material result supplied at one operator boundary
```

For this exact operator instance, both roads record preservation of the same
material supplied at the same boundary. I observes no second external supply,
no changed bytes, no changed loss, and no new source boundary. The adapter
requires O1 before I and names O1 as I's provenance.

More importantly, I no longer receives inert operator material:

```text
operator stream material
↓ O1
exact recorded material result M
+ exact source boundary
+ exact result boundary
+ exact Scope
+ M --locality--> this Seed
↓ generic Ingest I
another exact recorded result carrying M
```

The O1 experiment recovered the operator contact by adding a complete new
material-result road in front of the older Ingest road. It did not decompose
the existing Ingest boundary and specialize that boundary for the operator
source. The result is two bounding occurrences where the operator road has
only one observed external crossing.

The exact surviving additions made by I are:

```text
a second Act-occurrence identity
a second result identity
generic Ingest-shaped dimensions
source_role = operator
O1 provenance reference
membership in the event kind consumed by current Ingest-specific families
```

These are exact runtime differences. None presently establishes a second
material crossing or an independently assigned source Responsibility.

Consequently:

```text
O1 and I are distinct recorded occurrences                 established
O1 and I perform overlapping preservation work             established
I receives inert operator material                          refused by provenance
I records another external acquisition                     not established
I records a second warranted material bound                not established
I carries another exact Locality relation                  not established
I carries a subject-specific Responsibility assignment     not established
need for I beyond current Ingest-specific consumers         not established
```

Calling O1 and I one occurrence would erase exact history. Calling the second
occurrence constitutionally required merely because current consumers require
the Ingest event kind would let downstream implementation typing establish
upstream Responsibility.

## 4. Current consumers make I operationally load-bearing

Active `01.Source.D`, Witness Grammar, and runtime name the current declared
Measurement subjects as Ingest-specific material:

```text
exact_Ingest_result
exact_Ingest_source_set
source_ingest_occurrence_identity
```

The family readers call `read_exact_ingest_result`. Later position,
shared-position, addressed-byte, comparison, Candidate, and Locality surfaces
preserve the same source-Ingest identity.

This establishes:

```text
removing I now breaks exact active consumers
```

It does not establish:

```text
only a generic Ingest result can be exact material related to this Seed
```

O1 now carries exact material and exact evidenced Locality to this Seed, but
the current declared families do not name O1 material as their exact subject.
The generic Ingest crossing currently adapts recovered source material into
the older subject species those families consume.

## 5. History explains the layering without deciding its law

The mechanical order is exact:

```text
97dc29de  generic material Ingest and operator-Ingest introduced
59bc4e4e  O1 operator-material acquisition introduced upstream
c3903cd2  O1 added as exact provenance of retained operator Ingest
```

Before O1, `run_operator_ingest` passed operator boundary bytes directly to
generic Ingest. O1 was later inserted before the pre-existing branch. The
branch remained, and a later commit joined it to O1 through validation and a
provenance reference.

That sequence establishes the runtime fossil shape:

```text
old:
operator boundary → generic Ingest

later:
operator boundary → O1 → retained generic Ingest
```

History does not by itself authorize deletion of I. Combined with the active
coordinates, it does show the O1 implementation error: the operator-specific
road recovered the intended inert-to-bounded work again, upstream of the
pre-existing road that already named that work `Ingest`.

The supplied-system road was introduced after generic Ingest and reused it for
a genuinely different source boundary. In that road the supplied Python value
is still outside the Ledger before generic Ingest and is one exact recorded
material result afterward. That is direct testimony for the intended
inert-to-bounded distinction. It does not complete the common constitutional
Responsibility.

## 6. The Ingest distinction is real; its current common physiology is incomplete

A common inert-to-bounded material grammar would have to preserve, for each
exact source road, at least:

```text
exact source boundary
exact material
responsible boundary
Responsibility assignment
exact Act and occurrence
Yield and result
exact Locality relation and Evidence
Authority
Scope
limits and Unknown
source-specific provenance
```

O1 now records that shape for the operator boundary. Generic Ingest records
the central exact occurrence/result crossing but does not record:

```text
Responsibility assignment       absent
source-specific Book clause     absent
exact Locality relation         absent
Locality Evidence               absent
Authority                       unestablished
source role                     caller-supplied scalar
```

The supplied-system road contributes a distinct source boundary, destination
Locality, and ordered provenance. Generic Ingest is the only current point
where its externally supplied Python value becomes one exact recorded
material result. It still uses the incomplete common physiology rather than a
source-specific boundary Responsibility.

Therefore the current evidence supports neither extreme:

```text
current generic Ingest is the complete common constitutional grammar refused
operator O1 physiology is universal for every material source    refused
```

The narrower finding is:

```text
Ingest names a real inert-to-bounded distinction
current generic Ingest records its shared runtime event/result shape
the complete common constitutional Responsibility remains unrecovered
```

`Ingest` is not discarded as an empty noun. The implementation error is the
operator road performing its work twice, not the existence of the distinction.
Its noun form still must not stand in for the missing exact source relations.

## 7. Surviving distinctions

The audit preserves these exact differences:

```text
physical framing
!= constitutional acquisition

operator boundary
!= supplied system boundary

O1 operator contact occurrence
!= provider-supplied system occurrence

operator Locality
!= invocation destination Locality

O1 provenance
!= command + invocation-Locality + prior-supplied provenance

distinct recorded occurrence
!= distinct warranted Responsibility

common runtime function
!= common constitutional grammar
```

The supplied-system distinction blocks blind deletion of generic Ingest. The
O1/I overlap blocks treating every present Ingest occurrence as an independently
recovered material acquisition merely because it has its own identity.

## 8. Disposition

```text
operator_material_boundary
    mechanical framing only                              established

operator_material_acquisition / O1
    operator-specific acquisition physiology             recorded/replayable
    inert operator material to bounded material result    recorded/replayable
    M --locality--> this Seed                             recorded/replayable

operator_ingest
    independent constitutional Responsibility            absent
    adapter from O1 to generic Ingest                     established

operator O1 → generic Ingest I
    same material and source boundary                     established
    distinct occurrences and result identities           established
    I receives material already bounded by O1             established
    second external crossing                              not established
    second warranted bounding occurrence                  not established
    independent assignment warranting second bound       not established
    current Ingest-specific consumer dependency           established

supplied_invocation_material
    distinct source boundary and Locality                 established
    distinct ordered provenance                           established
    external Python material to recorded material result  established
    O1-equivalent source-specific acquisition physiology  not established

generic material_ingest
    intended inert-to-bounded distinction                 recovered testimony
    shared runtime bounding Act/Yield/result shape        established
    complete common Ingest grammar                        not established
```

## 9. Next bounded questions

The operator duplicate and system distinction should be separated before any
runtime change:

1. What exact common Ingest coordinates are present in both O1 and the system
   material boundary, without identifying their source-specific coordinates?
2. What exact source-specific Responsibility records provider-supplied system
   material in the invocation Locality?
3. After operator and system boundary roads independently carry their required
   source, Locality, Evidence, Authority, Scope, and provenance, what exact
   coordinate family is genuinely common?
4. Does `01.Source.D` intend declared Measurement subjects to remain exact
   Ingest results, or to become exact material occurrences carrying the
   required Locality Evidence?
5. Which later consumers require a source boundary identity, and which
   require only the exact material occurrence and its warranted relations?

Until those questions are recovered:

```text
do not delete generic Ingest
do not merge O1 and I histories
do not make O1 universal
do not change declared Measurement subjects
do not move the decision into Ledger
```

The completed audit localizes the implementation error: O1 recovered the
operator contact by duplicating the inert-to-bounded passage instead of
specializing the existing Ingest passage. Ordinary O1-to-I is retained by
Ingest-specific consumers. Supplied system material still needs one
inert-to-bounded passage and preserves exact source distinctions that current
generic Ingest does not itself constitutionally establish.
