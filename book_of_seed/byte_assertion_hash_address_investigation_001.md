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

## Free-token falsification

The first encoder removal replaced each digest with a Ledger-minted string.
Address-only mutation then exposed a loss on both byte roads:

```text
record result
change one leaf Assertion address to another unique nonempty string
make the Yield carry that changed result
read
→ accepted
```

The reader had no independently recorded mint relation. It read the token from
the result and used that same token to construct the material it compared. A
minted string therefore did not establish its own address.

## Exact result-local address

Both byte roads now address an Assertion as:

```text
exact recorded result occurrence
+ exact Assertion position within that result
```

The result derives positions directly from source-ordered Assertion formation.
Readers reconstruct the same positions independently. Changing one leaf
position or removing an Assertion changes that address surface and is refused.
Local count-to-recurrence support carries the exact result-local position, and
movement carries the complete occurrence-plus-position reference.

The same subtraction removed the UTF-8/SHA address used by the immediately
following recurrent-pair position Measurement. Its Assertions are likewise
addressed by recorded result occurrence plus exact result-local position.

No encoder, decoder, hash, schema-family label, or compatibility field is
warranted by the recovered distinction.

## Disposition

The hash identities and replacement free tokens are not constitutional grammar.
The active byte paths now preserve:

```text
count Assertion → recurrence support
recorded Assertion → movement source
exact replay and refusal
durable reopen
```
