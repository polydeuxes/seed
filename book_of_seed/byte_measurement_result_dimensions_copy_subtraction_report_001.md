# Byte Measurement result dimensions-copy subtraction report 001

## Subtraction

The plain-byte Measurement result no longer carries the fixed top-level
`dimensions` dictionary.

Before:

```text
R.dimensions.identity = "byte-count-measurement-occurrence"
R.dimensions.content =
    "exact source material, byte count, and same content"
R.result_positions = exact findings
R.act_occurrence_event_identity = A.identity
```

After:

```text
R.result_positions = exact findings
R.act_occurrence_event_identity = A.identity
```

## Surviving distinctions

The result occurrence still addresses its exact Measurement Act occurrence.
The reader reconstructs the bounded source read through that Act and requires
every recorded result position to equal the reconstructed finding.

The `dimensions` dictionary inside every result position remains unchanged.
Those dictionaries retain result-local positions and exact finding content.
Changing them still invalidates the result. Reintroducing the retired
top-level dictionary is refused as an extra recording surface.

## Family boundary

This subtraction changes only the top-level plain-byte result dictionary. It
does not change byte-pair Measurement dimensions or any result-position
dimensions.

## Result

```text
exact result-position dimensions        retained
exact R → A occurrence reference        retained
top-level fixed dimensions narration    removed
```
