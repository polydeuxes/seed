# Byte Measurement binding Book-clause subtraction report 001

## Question

Must a plain-byte Measurement binding and every reference to it copy
`book_clause_identity = 01.Source.D` into their durable material?

This pass precedes the separate binding-occurrence falsifier. It changes only
the copied Book-clause label.

## Prior shape

The runtime carried the same ownership twice:

```text
binding event kind
→ EVENT_KIND_BOOK_CLAUSES
→ 01.Source.D

binding material
→ book_clause_identity
→ 01.Source.D
```

The Act and result then copied the material field inside their binding
references.

No runtime consumer used the copied value to choose a clause, Act, subject,
Locality, or occurrence. Readers reconstructed the same literal and compared it
with its copies.

## Independent ownership

The binding occurrence remains exact through its Ledger identity and event
kind. The event-kind declaration continues to map that kind to `01.Source.D`.

Several other binding families also use `01.Source.D`, so the copied label does
not distinguish the plain-byte family. The exact event kind and its family
reader do.

## Falsifier

Remove only `book_clause_identity` from:

```text
plain-byte binding material
Act binding reference
result binding reference
```

Retain:

```text
binding occurrence E
Act occurrence A
result occurrence R
E/A/R occurrence identities
binding event-kind → Book-clause declaration
exact subjects
source Localities
source completeness boundary
recording through-occurrence boundary
byte findings
replay and restart
downstream pair Measurement and Movement
```

Generic exact-result ownership permits the smaller binding-reference shape only
for a plain-byte Measurement result and requires that its referenced occurrence
has the exact plain-byte binding event kind.

Reintroducing `book_clause_identity` into the binding material is refused as an
extra coordinate.

## Disposition

```text
Book ownership declaration                    retained
plain-byte binding event kind                 retained
copied Book-clause payload                    withdrawn
binding, Act, and result occurrences          retained
binding-occurrence subtraction                remains next
byte-pair Book-clause coordinates             unchanged
```

No Act, result, relation, finding, Book clause, Witness Grammar coordinate, or
admitted word is added or removed.
