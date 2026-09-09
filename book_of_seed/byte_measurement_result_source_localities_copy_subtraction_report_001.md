# Byte Measurement result source-Localities copy subtraction report 001

## Question

Can the plain-byte Measurement result address its source Localities through the
exact Act occurrence instead of copying them?

## Subtraction

The result no longer carries:

```text
source_localities
```

It retains its exact Act occurrence reference. The Act retains and validates
the source Localities used to reconstruct the bounded source material and its
subject references.

Downstream result-position reading now follows:

```text
result position
→ Measurement result R
→ Measurement Act A
→ exact source Localities
```

It does not infer source Localities from the result or Act event kind.

## Falsifier

Changing the source Localities on A continues to invalidate R through A's exact
subject and boundary validation. Reintroducing `source_localities` on R is
refused as an extra coordinate.

Act-before-result order, one result per Act, restart, current-coordinate replay,
byte findings, byte-pair Measurement, and Movement remain exact.

## Family boundary

No other result family changes. The plain-byte result's completeness-boundary
copy remains for independent pressure.

## Disposition

```text
source Localities on exact Act A          retained
R → A occurrence reference               retained
source Localities copied onto R           withdrawn
result completeness-boundary copy         unchanged
```
