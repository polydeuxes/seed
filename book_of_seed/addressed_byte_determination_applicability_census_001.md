# Addressed-byte Determination Applicability census 001

## Question

Can addressed-byte Determination Applicability independently establish more
than the exact direct Measurement result and addressed source-position
coordinate already establish?

This census follows the D.2 shared-position subtraction. It changes no active
Book clause, runtime event, Act, result, relation, identity, or reader.

## Live shape

```text
exact direct pair-position Measurement result
+ one addressed exact source-byte position coordinate
        ↓
Determination binding occurrence
        ↓
Applicability binding occurrence
        ↓
Applicability Act occurrence
        ↓
Applicability result occurrence
        ↓
Determination Act occurrence
        ↓
Determination result occurrence
```

The family-local lifecycle records this complete sequence once for every exact
source-position coordinate read from the direct Measurement result.

## Applicability result census

The Applicability result contains no `applicable` / `inapplicable` coordinate
and no other verdict coordinate. Its finding always records:

```text
relation = applicable_to
```

No branch in the producer or reader can record an inapplicable result. The
Determination Act follows every intact Applicability result.

## Zero-finding control

The existing single-byte test supplies:

```text
exact material = b"x"
addressed position = 0
```

The direct pair-position Measurement has no pair occurrence containing that
coordinate. The final Determination result therefore records:

```text
ordered_result_position_references = []
```

Nevertheless the preceding Applicability result records the same
`applicable_to` relation as cases with one or two matching result positions,
and the Determination Act occurs.

Therefore the current Applicability lifecycle does not distinguish:

```text
zero matching result-position references
one matching result-position reference
two matching result-position references
```

That multiplicity belongs to the Determination result. Applicability adds no
independently variable coordinate before it.

## Stoppability

Host calls can stop between every recorded stage. That mechanical stoppability
does not supply a physiological discriminator. No current consumer treats the
Applicability result as a verdict, because there is only one possible content.

Removing the applicability stages must still preserve:

```text
no Determination Act occurrence
Determination Act occurrence with result absent
Determination Act occurrence with exact result present
```

Those are Act/result states and do not depend on a forced Applicability result.

## Binding pressure

The exact Determination subject already exists before the first binding event:

```text
exact direct Measurement result occurrence
exact addressed source-position coordinate from that result
exact Determination Act
Locality
```

The Determination binding copies those coordinates plus future Act/result
identities. The Applicability binding copies them again. Neither event has an
independent producer occurrence.

This differs from Cartesian Compare and ordinary recurrent shared-position
Measurement. No host-formed pair is being tested. One exact coordinate read
from one exact result is the complete Determination subject.

## Finding

```text
Applicability verdict coordinate                    absent
negative Applicability result                       impossible
zero/one/two finding multiplicity                   Determination result
forced `applicable_to` finding                      copied ceremony
exact Determination subject before bindings         established
separate binding/App stages independently variable not found
```

Addressed-byte Determination Applicability fails its first discriminator: it
does not answer an exact question whose answer can differ.

## Disposition

Pressure the complete prospective floor on this one road:

```text
exact direct Measurement result
+ addressed exact source-position coordinate
        ↓
Determination Act occurrence
        ↓
Determination result occurrence
```

Delete only the two binding occurrences and the Applicability Act/result.
Preserve exact subject coordinates on the Determination Act, all zero/one/two
result multiplicities, current-coordinate order, restart, mutation refusal,
one-result refusal, and downstream D.2 shared-position provenance.

Do not generalize this finding to Applicability families with independently
variable positive and negative results.
