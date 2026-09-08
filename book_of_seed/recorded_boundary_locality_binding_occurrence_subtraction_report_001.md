# Recorded-boundary Locality binding occurrence subtraction report 001

## Question

Does the exact `06.Locality.C` subject-to-Act binding require a separate
Ledger occurrence before the Preservation Act occurs?

The lifecycle census separated binding coordinates from a binding occurrence.
The two prospective lifecycle identities were then removed independently.

## Prior road

```text
exact Q material result
        ↓
Preservation binding occurrence
        ↓
Preservation Act occurrence
        ↓
Locality relation result occurrence
```

The binding occurrence carried `Q`, the destination Locality, and the exact
Act identity. The Act and result copied a reference to that binding.

Current-coordinate replay treated the binding as current because its event
kind had been added to the binding dictionary. The Act reader then required
that authored occurrence.

## Falsifier

Remove only the binding occurrence. Place the exact subject-to-Act binding
coordinates on the Preservation Act occurrence:

```text
exact Q occurrence
+ exact through-Q boundary
+ exact Preservation Act
+ destination Locality
        ↓
Preservation Act occurrence
        ↓
Locality relation result occurrence
```

The subtraction fails if any independently varying distinction requires a
binding event rather than those exact coordinates.

## Current road

The Preservation Act writer now accepts the exact source current coordinates.
Before appending anything it:

```text
validates every supplied material-result coordinate
requires the source Locality
requires cardinality one current boundary carrier
resolves that carrier to exact Q
mints an unused destination Locality
```

It then records the Act occurrence with:

```text
act                              Preservation
exact_act_identity               retained under separate pressure
subject_reference                exact Q occurrence
through_occurrence_boundary      exact Q occurrence
destination_locality_identity    exact destination
```

The Act event identity is its exact occurrence address. Its append boundary
must contain `Q`, so a subject recorded outside the prefix through the Act
refuses.

The result addresses the exact Act occurrence and contains no binding-event
reference.

## Removed physiology

The active runtime no longer declares or records:

```text
operator.recorded_boundary_locality_subject_to_act_binding_recorded
binding Event.identity
binding Book-clause payload copy
subject_to_act_binding_reference on the Act
subject_to_act_binding_reference on the result
destination Locality containing only the binding event
```

No replacement binding object, host dictionary, request occurrence, or
relation occurrence was introduced.

The binding remains exact as coordinates of the Act occurrence. `Binding`
does not acquire a new event merely because those coordinates are jointly
addressable.

## Stoppable floors

The old binding-without-Act floor contained only the binding occurrence and
the future identities it minted. The two future identities failed prior
subtractions; removing the binding event removes no remaining independent
coordinate.

The real Act-without-result floor remains:

```text
Preservation Act occurrence exists
Locality relation result occurrence absent
```

The Act reader validates that floor through its own event identity, exact Q
subject, Act, and destination Locality.

## Exact controls

The subtraction retains:

```text
zero current boundary carriers             refusal before Act write
one current boundary carrier               one Preservation Act
two current boundary carriers              refusal before Act write
corrupted material coordinate              refusal before Act write
changed source Locality                     refusal before Act write
changed Act subject                         refusal
Act without result                          readable
one result per Act occurrence               retained
Act-before-result occurrence order          retained
current-coordinate advance and replay       retained
descendant carriage of Q                    retained
SQLite reopen                               retained
source history copying                      absent
```

Equal `Q` content in separate occurrences remains separate. Cardinality is
computed over exact validated material-result coordinates, not byte equality.

## Book consequence

`06.Locality.C` specifies the exact coordinates of a Locality
subject-to-Act binding. It does not require a binding occurrence. The clause
therefore needs no wording change.

The Act occurrence and Locality relation result occurrence remain separate
exact events.

## Results

```text
binding occurrences per Preservation lifecycle  1 -> 0
prospective lifecycle identities                 0
Preservation Act occurrences                     retained
Locality relation result occurrences             retained
exact subject-to-Act binding coordinates          retained
exact Act identity                                unresolved
```

Focused operator, current-coordinate, Book grammar, and admission tests:

```text
90 passed
```

Complete suite:

```text
1059 passed
75 skipped
```

Python compilation and `git diff --check` pass.

## Finding

The separate recorded-boundary Locality binding occurrence adds no exact
distinction. The Preservation Act occurrence carries the exact binding
coordinates and is itself the constitutional fact that the Act occurred.

The next independent pressure is the exact Act identity. Copied Act, subject,
boundary, and destination coordinates remain later one-coordinate questions.
