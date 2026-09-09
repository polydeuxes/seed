# Byte Measurement result occurrence-preservation census 001

## Question

Does the plain-byte Measurement result require the durable
`occurrence_preservation` value `exact byte Measurement result`?

This census changes no runtime road, Book clause, Witness Grammar, admission,
Act, result, or occurrence.

## Current shape

```text
R.kind = plain-byte Measurement result kind
R.identity = exact result occurrence identity
R.locality = A.locality

R.act_occurrence_event_identity = A.identity
R.result_positions = exact findings
R.occurrence_preservation = "exact byte Measurement result"
```

The writer authors the fixed `occurrence_preservation` value. The plain-byte
result reader compares it with the same fixed value. No later reader addresses
that value independently.

## Independently read coordinates

Without the fixed value, the result reader still validates:

```text
R is an intact plain-byte Measurement result occurrence
R and A have the same Locality
R addresses an exact Measurement Act occurrence A
A occurs before R
exactly one R addresses A
R.result_positions equal the findings reconstructed through A
```

The exact result positions carry the source-material-set, count, recurrence,
and bounded-read coordinates. The result occurrence and its relation to A are
not supplied by `occurrence_preservation`.

## Attempted distinction

No control holds those coordinates fixed while varying only
`occurrence_preservation` as a lawful result distinction. The current mutation
test succeeds only because the reader was taught to require the value authored
by the writer.

## Required falsifier

Remove only the plain-byte result's `occurrence_preservation` field and fixed
value check.

Retain:

```text
result occurrence identity and kind
R → exact A occurrence
A-before-R occurrence order
one result per A
all exact result positions
restart and current-coordinate replay
downstream byte-pair Measurement and Movement
```

Two results addressing the same A must still refuse. Reintroducing the retired
field must be refused as an extra recording surface.

## Family boundary

This census does not address the byte-pair Measurement
`occurrence_preservation` field or constant. That family has not received this
falsifier.

## Disposition

```text
actual plain-byte result occurrence             retained
exact result positions                          retained
exact R → A occurrence reference                retained
fixed plain-byte occurrence-preservation label  failed census
```
