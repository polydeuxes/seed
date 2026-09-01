# Assertion coordinate census 001

## Question

What independently exists because addressed result content is an Assertion,
beyond its exact content, source occurrence references, Locality, parent result
occurrence, and result-local position?

This census tests active Book Assertion clauses against live runtime physiology.
It does not presume that Assertion survives or disappears.

## Former Book claims

At the start of this census the Book stated:

```text
01.Current.D.1
Assertion = exact content as one subject
+ source occurrence references
+ Locality
+ established coordinates

01.Current.D.2
one current Assertion may be one subject in a subject-to-Act binding

01.Current.E
relation Assertion
= first subject
+ relation content
+ second subject
+ relation occurrence
+ Locality

05.Recording.A
one recording occurrence preserves one exact Assertion

01.Source.F
supplied material with a relation Assertion
→ preservation Act
→ exact relation Assertion
```

## Prior plain and pair Measurement result shape

Plain-byte and byte-pair Measurement results recorded Assertion dictionaries
inside the parent result event:

```text
recorded Measurement result occurrence
└── assertions[position]
    ├── assertion_subject
    ├── dimensions.position
    ├── dimensions.content
    ├── result
    └── exact earlier-result references where established
```

No separate Assertion event was recorded for these dictionaries. They had no
Assertion event identity, Assertion Act occurrence, Yield, result occurrence,
or Ledger identity.

Their exact durable address was already:

```text
recorded parent result occurrence identity
+ result-local assertion position
```

The result reader reconstructed the complete expected list from the
exact Measurement inputs and boundary. It refuses a changed position, changed
subject, changed content, changed references, missing entry, added entry, or
reordered entry by comparing the parent result material with that independent
reconstruction.

## Prior runtime reader wrappers

`RecordedBytePairAssertion` and the private recorded Assertion reader shapes
were Python values returned by parent-result readers. They were not Ledger
events.

Their properties returned detached dictionaries and exact references.
Replacing or mutating one detached dictionary did not mutate the recorded
result.

The wrapper reference was constructed from:

```text
recorded_occurrence_identity
result-local position
```

The wrapper added no durable Assertion identity.

## Equal content at distinct result occurrences

A focused Witness records two separately occurring byte Measurement results
over one exact source. Each result contains a byte-count entry with equal:

```text
subject content
result content
result tag
result-local position
earlier-entry position
```

The two entries remain distinct because their references are:

```text
(first result occurrence, position)
(second result occurrence, position)
```

No Assertion identity is needed. The focused test is:

```text
test_equal_assertion_content_at_distinct_results_has_distinct_addresses
```

This establishes:

```text
equal Assertion content
!=
one exact addressed result entry
```

The distinction comes from the result occurrence address.

## Assertion as a later Act subject

Byte-pair Measurement accepts the exact source-material-set entry from an
earlier byte Measurement. The live reader requires:

```text
exact parent Measurement result occurrence
exact result-local position
exact result tag
exact subject and content coordinates
exact Locality or exact Locality movement result
```

The later binding addresses that entry through the parent result and position.
The Python API additionally requires a `RecordedByteAssertion` reader value,
but no durable occurrence records that Python class or an independent
Assertion coordinate.

The live physiology therefore proves that exact addressed result content can
occupy a later subject position. It does not yet prove that an additional
Assertion occurrence exists.

## Locality movement control

Assertion Locality movement has real recorded physiology:

```text
movement binding
movement Act occurrence
Yield event
movement result
```

Its source is addressed by parent result occurrence plus result-local position,
and its reader resolves the exact source content through that address.

This establishes Movement of exact addressed content. It does not record a
separate Assertion occurrence before movement. The Movement road therefore
cannot by itself establish Assertion as an additional durable object.

Yield on this road remains outside this census.

## Relation Assertion census

No live runtime producer was found for `01.Source.F` or `01.Current.E` as a
separate relation Assertion occurrence.

Current Compare roads do record relation findings and ordered relation-path
content. Those values are exact parent-result content with exact source and
finding references. They do not record a separate relation Assertion event,
identity, Act occurrence, Yield, or result.

The existence of exact relation content does not establish that the relation
content is true independently of its exact relation occurrence. This census
does not collapse relation content into endpoint equality and does not weaken
the requirement that an exact relation requires its own occurrence.

It establishes only:

```text
relation Assertion as separate durable occurrence   not found
exact addressed relation content                    found
exact relation occurrences on established roads     found
```

## Recording clause census

No standalone `05.Recording.A` Assertion-recording event was found. Live
Measurement and Compare result events record their own exact content. Movement
records a result that addresses exact source content.

The repository therefore has recording occurrences that contain addressed
content, but no separately occurring Assertion preservation road established
by `05.Recording.A` alone.

## Direct pair-position address result

The direct byte-pair position result reference passed subtraction. Its runtime
address is now:

```text
recorded result occurrence identity
+ result position
```

The former `assertion_position`, `assertion_address`, and
`assertion_reference` surfaces added no independently occurring coordinate.
Addressed-byte determination now records the complete ordered population as
`ordered_result_position_references`; each reference contains only its owning
result occurrence and result position.

The higher shared-position reader follows those coordinates directly. Exact
pair material, source positions, source result, Locality, and completeness
boundary remain validated from the owning result. Missing, changed,
substituted, out-of-range, and reordered coordinates still refuse.

The producing direct position Measurement result then passed the remaining
payload subtraction. It now records its bounded `result_positions` coordinates
instead of an `assertions` wrapper. Each addressed position is reconstructed
from the validated parent result as:

```text
parent result occurrence
+ result position
+ exact pair subject
+ first and second source-position coordinates
```

The result reader refuses changed summary coordinates, and the addressed
reader refuses changed, absent, substituted, or out-of-range positions. The
complete bounded result-position reader and each individually addressed read
produce the same exact content without an Assertion subject key or reader
identity.

## Recurrent pair-position address result

The recurrent pair-position road then passed independently. It preserves two
different containing results:

```text
pair Measurement result occurrence
+ recurrence result position
+ count result position

recurrent pair-position result occurrence
+ one result position
```

The first address establishes which recurrence and count content is the exact
subject of the later Measurement. The second addresses one exact position in
that later result. Equal integer positions in the two containing results are
not interchangeable.

The recorded recurrent result now names its complete ordered
`result_positions` population directly. Each later reference contains the
owning result occurrence and result position; the pair subject retains the
separate producing pair-Measurement result positions. Shared-position
Measurement follows these addresses without an Assertion identity, address,
reference, or subject wrapper.

This result does not authorize a rename of the earlier byte Measurement and
byte-pair Measurement result readers or the Locality movement road. Those
retain Assertion-shaped coordinates under their own independent pressure.

## Current finding

Live runtime testimony establishes:

```text
exact parent result occurrence
+ exact result-local position
+ exact content
+ exact subject coordinates
+ exact source occurrence references where established
+ exact Locality
```

It does not establish:

```text
independent Assertion identity
independent Assertion event
independent Assertion Act occurrence
independent Assertion Yield
independent Assertion result
separate relation Assertion occurrence
```

`Assertion` was shorthand for exact addressed result content and its coordinate
requirements. The durable address and discrimination come from the parent
result occurrence plus result-local position, not from an Assertion object.

## Completed subtraction

The subtraction proceeded one road at a time:

```text
1. plain-byte result content and reader
2. byte-pair result content and reader
3. result-position Locality movement source
4. ordered relation-path result content
5. Book-only relation Assertion and recording clauses
```

Plain-byte and byte-pair Measurement now record `result_positions`. Every
result position has exact subject and result coordinates and is addressed by
its owning result occurrence plus its local position. The pair reader is a
`RecordedBytePairResultPosition`; its Python value adds no durable identity.

References to an earlier result position remain distinct from local references
inside the current result:

```text
referenced_result_position_references
referenced_result_positions
```

The first population contains exact owning-occurrence and result-position
addresses. The second contains local positions in the current owning result.
Neither is an Assertion identity.

Result-position Locality movement retains its independent binding, Movement Act
occurrence, Yield event, and result occurrence. Its source coordinates are now
named directly as `source_result_position_reference` and
`source_result_position_coordinates`. The Movement result still refuses an
absent, changed, substituted, foreign-Locality, or noncurrent source.

All active runtime Assertion vocabulary has left these roads. No Content,
Finding, Entry, Position, or other replacement object was introduced.

Do not introduce a Content object, Finding object, Entry object, Position
object, or replacement wrapper.
