# Locality B and D lifecycle-coordinate census 001

## Question

Which durable coordinates remain on the active `06.Locality.B` and
`06.Locality.D` roads after the `06.Locality.C` lifecycle reached its smaller
exact shape?

This is a census, not an authorization to generalize the Locality.C
subtractions.

## Active families

```text
06.Locality.B
    runtime  operator_locality_continuation.py
    subject  exact source Locality + through-occurrence boundary
    Act      source-boundary Locality relation
    result   exact Locality relation occurrence

06.Locality.D
    runtime  operator_destination_locality.py
    subject  exact operator material occurrence
    Act      Locality
    result   exact Locality relation occurrence
```

Both families remain live in `operator_console`. Both still record a separate
subject-to-Act binding occurrence before the Act occurrence.

## `06.Locality.B` current lifecycle

The binding occurrence records:

```text
Book clause
opaque exact Act identity
source Locality + source through-occurrence boundary
prospective result identity
destination Event.Locality
```

The Act occurrence then records:

```text
opaque exact Act identity under a second field name
prospective family-local Act-occurrence identity
Act string
binding occurrence reference plus copied binding coordinates
copied source coordinates
copied destination Locality
actual Act Event.identity
actual Act Event.locality_identity
```

The result repeats all of those coordinates and adds the actual Act-event
reference plus its own Event identity and Locality.

Thus this family still carries the patterns that failed independently on
Locality.C and Source:

```text
prospective result identity
family-local Act-occurrence identity
opaque exact Act identity
separate binding occurrence
copied source reference
copied destination Locality
copied Act label
copied binding payload
```

They are not withdrawn by analogy. `06.Locality.B` has a distinct source
boundary and a source-to-destination relation-coordinate order, so every
subtraction requires its own restart, order, corruption, and equal-source-cut
controls.

### Act-word pressure

The runtime Act string is:

```text
source-boundary Locality relation
```

The Book describes an exact preservation Act. Neither source boundary nor
Locality relation alone identifies the Act: the first is its subject
coordinate and the second is its result occurrence. The runtime phrase may be
narration across subject, Act, and result rather than one exact Act word.

This census leaves that coordinate unresolved. It must not be renamed
`Preservation` merely because `06.Locality.C` uses that Act.

## `06.Locality.D` current lifecycle

The binding occurrence records:

```text
Book clause
exact Act = Locality
opaque operator-destination Act identity
prospective family-local Act-occurrence identity
prospective result identity
operator material occurrence reference
operator material result occurrence identity = the same occurrence
operator Locality
operator through-occurrence boundary
destination Locality
destination Event.Locality = the same destination
```

The Act occurrence copies the three prospective identities, Act, binding
reference, operator occurrence, operator Locality, and destination Locality.

The result copies those coordinates again and adds the actual Act-event
reference, Event identity, and Event Locality.

The operator material occurrence and its material result are the same exact
occurrence on this road:

```text
operator_material_occurrence_reference
=
operator_material_result_occurrence_identity
```

That duplicate is a distinct pressure from whether the operator
through-occurrence boundary may be later than the operator material
occurrence.

## Independent controls

The two families cannot be collapsed into one test.

```text
06.Locality.B
    source and destination are separate Localities
    subject is an exact source cut
    equal source cuts may produce separate destination relations
    continuation may be applied again from a relation result

06.Locality.D
    subject is exact operator material beginning with "!"
    one operator occurrence currently refuses a second destination binding
    later supplied material cites operator occurrence + relation result
    exact Act word Locality is independently declared by the Book
```

The separate Book clauses, subject shapes, and downstream source references
survive this census.

## Dependency finding

Current readers make every copied lifecycle coordinate appear necessary by
reconstructing expected payloads from the earlier wrapper and requiring the
copies later.

That demonstrates internal consistency. It does not independently establish:

```text
prospective identity != actual occurrence identity
binding coordinate   requires binding occurrence
readable coordinate  requires repeated payload field
```

Locality.C and Source have falsified those general implications. Locality.B
and D must now answer the same questions from their own exact controls.

## Pressure order

Start with `06.Locality.D`, whose exact Act word is independently declared and
whose lifecycle has the clearest one-subject antecedent:

```text
1. prospective result identity
2. family-local Act-occurrence identity
3. opaque operator-destination Act identity
4. separate binding occurrence
5. copied Act / subject / Locality / boundary coordinates
```

Then pressure `06.Locality.B` independently:

```text
1. prospective result identity
2. family-local Act-occurrence identity
3. separate binding occurrence
4. opaque exact Act identity
5. exact Act word or narrated phrase
6. copied source / destination / binding coordinates
```

The Act-word pressure is later on B because removing opaque lifecycle tokens
and the binding wrapper first exposes whether any independent Act distinction
remains.

## Disposition

```text
06.Locality.C                    frozen
06.Locality.B lifecycle          live; independently unresolved
06.Locality.D lifecycle          live; independently unresolved

Locality.B source cut            retained
Locality.D operator occurrence   retained
destination Localities           retained
Act occurrences                  retained
relation result occurrences      retained
```

This report adds no runtime road, Book coordinate, Act, relation, result, or
admitted word.
