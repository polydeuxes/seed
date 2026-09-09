# Byte Measurement result occurrence-preservation subtraction report 001

## Subtraction

The plain-byte Measurement result no longer carries the fixed
`occurrence_preservation` value `exact byte Measurement result`.

Before:

```text
R.kind = plain-byte Measurement result kind
R.act_occurrence_event_identity = A.identity
R.result_positions = exact findings
R.occurrence_preservation = "exact byte Measurement result"
```

After:

```text
R.kind = plain-byte Measurement result kind
R.act_occurrence_event_identity = A.identity
R.result_positions = exact findings
```

## Surviving distinctions

The reader still requires an intact plain-byte result occurrence, an exact
Measurement Act occurrence in the same Locality, A-before-R occurrence order,
and one result for A. It reconstructs the bounded source read through A and
requires every recorded result position to equal the reconstructed findings.

Two results addressing the same A therefore still refuse. Reintroducing the
retired fixed value is refused as an extra recording surface.

## Family boundary

This subtraction changes only the plain-byte Measurement result. The
byte-pair Measurement `occurrence_preservation` field and constant remain
unchanged pending an independent falsifier.

## Result

```text
actual result occurrence and identity        retained
exact R → A occurrence reference             retained
exact result positions                       retained
fixed occurrence-preservation narration      removed
```
