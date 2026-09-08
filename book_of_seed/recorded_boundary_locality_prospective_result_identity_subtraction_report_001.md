# Recorded-boundary Locality prospective result identity subtraction report 001

## Question

Must the `06.Locality.C` Preservation binding mint an identity for a result
before the Locality relation result occurrence exists?

The lifecycle census found no active consumer that addressed this
family-local identity independently from the actual result occurrence.

## Prior shape

```text
Preservation binding occurrence
    mints result_identity
        ↓ copies it
Preservation Act occurrence
        ↓ copies it
Locality relation result occurrence
    has result_identity
    has Event.identity
```

The reader required the copied values to agree because the writer placed the
same token in every payload.

## Current shape

```text
Preservation binding occurrence
        ↓
Preservation Act occurrence
        ↓
Locality relation result occurrence
    addressed by its exact Event.identity
```

`result_identity` is absent from all three payloads. The result obtains an
exact occurrence address when the Ledger records it.

## Controls

The subtraction retains:

```text
exact Q subject
exact through-Q boundary
source and destination Localities
separate binding and Act stoppable floors
Act-before-result occurrence order
one result per Act occurrence
current-coordinate advance and replay
descendant carriage of Q
SQLite reopen
changed-coordinate and corruption refusal
```

The binding and Act can still be read before a result exists. No prospective
result token is needed to preserve those floors.

Separate relation results remain separate through their exact Ledger
occurrence identities. Equality of carried `Q` references does not collapse
their result occurrences.

## Reader consequence

The generic current-coordinate reader previously required a result's
family-local identity to occur among identities declared by its binding. It
now recognizes the exact `06.Locality.C` result shape without such a token and
continues to validate:

```text
result Event.identity
result → Act occurrence reference
Act occurrence → binding reference
binding → Q subject
all occurrence order and Locality coordinates
```

This is a family-specific subtraction. It does not weaken result-identity
requirements on families that retain an independently addressed result
coordinate.

## Results

```text
prospective result identities per Preservation binding  1 -> 0
actual result occurrence identity                        retained
binding occurrence                                       retained
Act occurrence                                           retained
exact Act identity                                       unresolved
prospective Act-occurrence identity                      unresolved
```

Focused operator, current-coordinate, Book grammar, and admission tests:

```text
89 passed
```

## Finding

The family-local prospective result identity adds no exact distinction on the
active recorded-boundary Locality road. The actual result occurrence identity
supplies the result address when the result occurs.

The next independent pressure is the prospective Act-occurrence identity.
