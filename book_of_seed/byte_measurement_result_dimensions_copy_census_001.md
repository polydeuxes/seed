# Byte Measurement result dimensions-copy census 001

## Question

Does the plain-byte Measurement result require its fixed top-level
`dimensions` value?

This census changes no runtime road, Book clause, Witness Grammar, admission,
Act, result, or occurrence.

## Current shape

```text
R.dimensions.identity = "byte-count-measurement-occurrence"
R.dimensions.content =
    "exact source material, byte count, and same content"

R.result_positions = exact source-material-set, count, and recurrence findings
R.act_occurrence_event_identity = A.identity
```

The writer authors the same top-level dictionary for every plain-byte result.
The plain-byte reader compares it with the same fixed dictionary. No later
reader addresses the dictionary independently.

## Coordinate separation

This census does not pressure the `dimensions` dictionaries inside exact
result positions. Those dictionaries address result-local positions and the
content of individual source-material-set, count, or recurrence findings.

The top-level dictionary instead narrates the family and the findings that are
already addressed by:

```text
R result occurrence kind
R → exact Measurement Act A
R.result_positions
```

## Attempted distinction

No control holds the exact result occurrence, A, and every result position
fixed while varying only the top-level dictionary as a lawful result
distinction. Its current mutation test would prove only that the reader was
taught to require the writer's fixed copy.

## Required falsifier

Remove only the top-level plain-byte `R.dimensions` dictionary.

Retain:

```text
every result-position dimensions dictionary
exact source-material-set finding
count and recurrence findings
R → exact A occurrence
A-before-R occurrence order
one result per A
restart and current-coordinate replay
downstream byte-pair Measurement and Movement
```

Changing any result-position dimensions must continue to invalidate R.
Reintroducing the retired top-level dictionary must be refused as an extra
recording surface.

## Family boundary

This census addresses neither the byte-pair Measurement result's top-level
dimensions nor any result-position dimensions. Those coordinates remain
unchanged pending independent falsifiers.

## Disposition

```text
exact result-position dimensions             retained
top-level fixed dimensions narration         failed census
plain-byte dimensions-copy subtraction       next falsifier
```
