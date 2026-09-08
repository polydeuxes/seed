# Compare-Distinction Measurement binding occurrence subtraction report 001

## Question

Does Measurement of one exact Compare result need a separate prior binding
event?

This is a second internal control. Its subject is not operator-authored
material: one earlier Compare result and its exact nested finding coordinates
are already durable and current before this Measurement occurs.

## Former shape

```text
exact current Compare result occurrence
        ↓
separate Compare-Distinction Measurement binding event
        ↓
Measurement Act occurrence
        ↓
Measurement result occurrence
```

The binding event copied the Compare result reference, Locality, prior
through-occurrence, exact Act identity, future Act occurrence identity, and
future result identity. The Act and result then copied a reference to the
binding event.

## Subtraction

The separate event, kind, reader, current-coordinate entry, and binding-event
references are removed.

The Measurement Act occurrence now records directly:

```text
Book clause
exact Compare result subject reference
exact Measurement Act identity
Act occurrence identity
future result identity
Locality
prior through-occurrence boundary
```

The Act reader reopens the exact Compare result under the bounded current
coordinates, follows each nested finding reference into its owning Compare
result, and reconstructs the exact Distinctions. The result directly addresses
the Act and repeats the subject reference.

## Preserved discriminators

Focused tests establish:

```text
exact Compare result occurrence                  preserved
exact nested finding coordinates                 preserved
every Distinction within completeness boundary  preserved
prior result/current-coordinate order            preserved
Measurement Act before result                    preserved
distinct Act / occurrence / result identities    preserved
one result per Act                               preserved
durable restart                                  preserved
current-coordinate replay                        preserved
changed nested finding                           refused
equal measured content in separate occurrences   remains separate
later exact Measurement references               preserved
separate Yield event                             absent as before
```

The persistent operator road appends one fewer occurrence for each
Compare-Distinction Measurement.

## Boundary of the finding

Family-local mechanics still append the Measurement Act. This subtraction does
not account for the Act occurring and does not alter any Applicability family.

It establishes:

```text
exact internal subject-to-Act binding coordinates   established
separate prior binding occurrence                   not needed
Measurement Act occurrence                          established
Measurement result occurrence                       established
```

Recurrent pair-position Measurement supplies the other independent internal
result. The checkpoint cleanup is not counted as one of the two internal
controls.

## Disposition

Accept the subtraction. Stop collecting simple non-Applicability controls.

Return to the frozen shared-position Measurement/Applicability road. Any next
subtraction must preserve:

```text
no Applicability occurrence
Applicability result = inapplicable
Applicability result = applicable, Measurement Act absent
Applicability result = applicable, Measurement Act present
```

Do not move prospective coordinates into the Measurement Act, because negative
Applicability has no such Act.
