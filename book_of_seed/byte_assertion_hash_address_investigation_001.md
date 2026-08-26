# Byte Assertion hash address investigation 001

## Question

Do the JSON/SHA-derived byte Assertion identities carry a distinction that
recorded occurrence identity and exact Assertion coordinates do not?

## Frozen runtime surface

`seed_runtime.byte_measurement` currently derives an Assertion identity from:

```text
result
+ exact subject
+ Scope
+ exact content
→ sorted JSON bytes
→ SHA-256
→ byte-measurement:<digest>
```

The same operation addresses source-material, count, and recurrence Assertions.
The fixed byte-pair helper performs the same operation with a hand-built JSON
shape.

## Exact work presently carried by the identity

One recorded Measurement result can carry more than one Assertion. Later
coordinates therefore need an address for one Assertion inside that exact
result.

Two live uses establish that addressing distinction:

```text
movement source reference
    recorded result occurrence
    + Assertion address

recurrence support
    count Assertion address within the same recorded result
```

Removing the address without replacement would collapse distinct Assertions
inside one result. Recorded result occurrence identity alone is not enough.

## What the hash does not own

The reader reconstructs and compares the complete exact Assertion material.
Existing controls can change Assertion coordinates, recompute a matching hash,
and still receive refusal because the complete bounded Measurement result no
longer agrees with its source read.

Therefore:

```text
exact Assertion discrimination/addressability    real

JSON serialization                               not the distinction
UTF-8 encoding                                   not the distinction
SHA-256 digest                                   not the distinction
byte-measurement family prefix                   not the distinction
```

The digest is a compact witness-side proxy for already-carried coordinates. It
does not add a grammatical discriminator.

## Bounded plain-byte build

The plain-byte road now mints one result-local Assertion address through the
Ledger for each exact Assertion before Yield/result recording. Reconstruction
receives those recorded addresses and still compares the complete source-derived
Assertion material. Count-to-recurrence support and movement retain their exact
addresses across durable reopen without JSON, UTF-8, or SHA.

This proves that the hash was not the Assertion distinction on the plain-byte
road.

## Remaining cleanup frontier

Do not merely delete `assertion_identity` from the remaining pair road: local
support and movement still need to name one exact Assertion.

The pair road must replace the proxy with an address owned by the recorded
result physiology. Two shapes remain possible there and are not yet
distinguished:

```text
recorded result occurrence
+ exact result-local Assertion occurrence identity
```

or:

```text
recorded result occurrence
+ exact carried Assertion coordinates
```

The first is now proven by the plain-byte road: the Ledger can mint and preserve
the local Assertion address before Yield/result recording, then replay the
stored address while validating all independently reconstructed coordinates.
The second carries a larger exact reference and may remove the extra identity
entirely.

No encoder, decoder, hash, schema-family label, or compatibility field is
warranted by the recovered distinction.

## Disposition

The hash identities are not constitutional grammar and must not remain as an
internal address mechanism. The plain-byte hash has been removed. The pair hash
remains until its own bounded build preserves:

```text
count Assertion → recurrence support
recorded Assertion → movement source
exact replay and refusal
durable reopen
```
