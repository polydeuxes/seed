# Assertion coordinate census 001

## Question

What independently exists because addressed result content is an Assertion,
beyond its exact content, source occurrence references, Locality, parent result
occurrence, and result-local position?

This census tests active Book Assertion clauses against live runtime physiology.
It does not presume that Assertion survives or disappears.

## Active Book claims

The active Book currently states:

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

## Live plain and pair Measurement results

Plain-byte and byte-pair Measurement results record Assertion dictionaries
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

No separate Assertion event is recorded for these dictionaries. They have no
Assertion event identity, Assertion Act occurrence, Yield, result occurrence,
or Ledger identity.

Their exact durable address is:

```text
recorded parent result occurrence identity
+ result-local assertion position
```

The result reader reconstructs the complete expected Assertion list from the
exact Measurement inputs and boundary. It refuses a changed position, changed
subject, changed content, changed references, missing entry, added entry, or
reordered entry by comparing the parent result material with that independent
reconstruction.

## Runtime reader wrappers

`RecordedByteAssertion`, `RecordedBytePairAssertion`, and the private recorded
Assertion reader classes are frozen Python values returned by parent-result
readers. They are not Ledger events.

Their properties return detached dictionaries and exact references. Replacing
or mutating one detached dictionary does not mutate the recorded result.

The wrapper reference is constructed from:

```text
recorded_occurrence_identity
assertion_position
```

The wrapper does not add a durable Assertion identity.

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

`Assertion` currently names exact addressed result content and its coordinate
requirements. The durable address and discrimination come from the parent
result occurrence plus result-local position, not from an Assertion object.

## Required subtraction order

This census does not authorize a global rename or deletion. The smallest live
tests are:

```text
1. plain-byte result reader wrapper
2. byte-pair input type gate
3. Assertion Locality movement source wrapper
4. ordered relation-path result content
5. Book-only relation Assertion and recording clauses
```

For each road, preserve exact content, parent result occurrence, result-local
position, source references, Locality, movement where established, later
subject-to-Act binding, and all mutation and substitution refusals.

Do not introduce a Content object, Finding object, Entry object, Position
object, or replacement wrapper.
