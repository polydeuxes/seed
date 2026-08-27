# Relation occurrence census 001

## Question

When current coordinates address two exact subjects together, does Seed carry
an exact relation occurrence in addition to those subjects and coordinates?

This census does not infer a relation from equal coordinates.

## Exact recorded relation occurrence

Yield has an independently recorded occurrence:

```text
exact Act occurrence
exact result
operator.yield_relation_recorded occurrence
Locality
```

The Yield occurrence has its own durable event identity. Its reader resolves
that event, refuses changed endpoints, and establishes its order between the
Act occurrence and result.

## Exact coordinates without a relation occurrence

Two Compare Distinction Measurement results can address one exact Measurement
occurrence through their producing coordinates:

```text
first result producing coordinates:  later Measurement = M
second result producing coordinates: earlier Measurement = M
```

The exact result occurrences and `M` reconstruct this joint after SQLite
reopen and independently of current-coordinate projection order. One `M` can
address several results on either side. No relation identity, relation event,
or relation reader is recorded.

This is current evidence for exact joint addressability. It is not current
evidence for an exact relation under `01.Current.D`.

## Unrecorded relation identity strings

Several Locality roads historically minted a relation-occurrence identity and
copied it through binding, Act, and result material without recording an event
at that identity.

The invocation-Locality, continuation-Locality, and recorded-boundary Locality
roads were tested separately. Each exact result event already carries the two
Locality subjects and is the occurrence used by current coordinates, reopen,
ordering, and downstream references. Removing each unrecorded string preserved
every one of those distinctions.

## Embedded relation material

Older Measurement and Compare roads carried `input_relation` or
`input_relations` dictionaries inside bindings, Acts, and results. The census
found no separately recorded occurrence for those dictionaries.

Three separate subtraction tests removed:

- prose describing the exact operator source order already enforced by one
  recorded-pair Compare binding;
- a position-Measurement dictionary that copied its exact material-result
  subject, Act coordinates, and Locality;
- two shared-position Applicability dictionaries that copied the exact binding
  subjects and addressed Act.

The exact subjects, structural positions, Acts, Localities, and refusals remain
directly carried. No live `input_relation` or `input_relations` material remains.

## Current finding

```text
exact relation
→ exact subjects
+ independently recorded occurrence

coordinate equality
→ exact subjects remain jointly addressable
→ no relation is inferred

unrecorded identity string
→ does not establish an occurrence
```

The evidence does not require weakening `01.Current.D`. It requires live roads
to stop presenting a generated token as an occurrence.
