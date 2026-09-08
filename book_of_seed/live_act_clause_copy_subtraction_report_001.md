# Live Act clause-copy subtraction report 001

## Question

The active same-position Applicability and Compare Act occurrences each carried
a `book_clause_identity` inside their material. Their event kinds are already
mapped to active Book clauses by the runtime witness grammar, and the exact Act
coordinates in those clauses do not include a clause identity.

The subtraction asked whether the payload field established an Act coordinate
or only repeated the runtime declaration governing that event kind.

## Result

Both active Act materials no longer carry `book_clause_identity`.

The module retains its event-kind-to-clause declarations:

```text
Applicability Act occurrence kind → 02.Acts.A
Compare Act occurrence kind       → 02.Acts.A
Applicability result kind         → 01.Current.E.1
Compare result kind               → 04.Compare.B
```

Runtime witness grammar still validates those declarations. The active Acts
retain their exact subjects, Act, addressed Act where applicable, Locality,
boundary or positive Applicability reference, and occurrence order.

All lifecycle floors, exhaustive cross-set coverage, positive and negative
answers, findings, restart, replay, downstream Distinction Measurement, and
refusals survive.

## Finding

```text
event-kind Book declaration    survives
Act material clause copy       no distinction found
Act coordinates                survive
```

A Book clause governs the event kind. Repeating its label inside every Act
occurrence does not add a physiological coordinate.
