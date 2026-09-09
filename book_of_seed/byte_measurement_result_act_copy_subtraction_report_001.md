# Byte Measurement result Act-copy subtraction report 001

## Question

Can the plain-byte Measurement result address its exact Act through the Act
occurrence without copying the Act word?

## Subtraction

The result no longer carries:

```text
exact_act = Measurement
```

It retains:

```text
act_occurrence_event_identity = A.identity
```

The reader follows that identity and validates the exact Act occurrence,
including `A.act = Measurement`, its subjects, source Localities, completeness
boundary, recording cut, Locality, and integrity.

## Falsifier

Changing `A.act` to `Compare` invalidates R. Reintroducing `exact_act` on R is
refused as an extra coordinate. The result therefore has not delegated its Act
identity to the implementation event kind.

Act-before-result order, one result per Act, restart, current-coordinate replay,
byte findings, byte-pair Measurement, and Movement remain exact.

## Family boundary

No other result family changes. The plain-byte result's source Localities and
completeness boundary remain durable copies for independent pressure.

## Disposition

```text
Measurement on exact Act occurrence A          retained
R → A occurrence reference                     retained
R.exact_act copy                                withdrawn
source and boundary result coordinates          unchanged
```
