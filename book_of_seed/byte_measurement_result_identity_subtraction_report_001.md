# Byte Measurement result-identity subtraction report 001

## Question

Must a byte Measurement binding mint the identity of its future result before
that result occurs?

This falsifier is confined to plain-byte Measurement. Byte-pair Measurement,
result-position Movement, and the remaining byte Measurement lifecycle receive
no subtraction by analogy.

## Prior shape

Before the result occurred, the binding minted:

```text
measurement_result_identity = prospective R*
```

The later result copied `R*` as `result_identity` while also receiving its
actual Ledger occurrence identity `R.identity`. Current coordinates copied
both addresses.

No prior occurrence independently addressed `R*`. The binding authored the
value; the result and its readers then used the authored copy as the expected
value.

Downstream byte-pair Measurement and result-position Movement address the byte
result through:

```text
R.identity
+ exact result-local position
```

They do not address `R*`.

## Falsifier

Remove only:

```text
binding.measurement_result_identity
result.result_identity
current-coordinate copy of result_identity for plain-byte Measurement
```

Retain:

```text
binding occurrence E
Measurement Act occurrence A
Measurement result occurrence R
exact source material-result occurrences
source Localities
source completeness boundary
recording through-occurrence boundary
exact byte counts and recurrence findings
E before A before R
one result per A
current-coordinate replay
SQLite restart
equal-content occurrence non-collapse
downstream byte-pair Measurement and Movement
```

## Result

`R.identity` supplies the result address when `R` occurs. The result continues
to address `A.identity`, and every exact result position remains unchanged.
Current coordinates carry the actual result and Act occurrence identities.

Adding a `result_identity` field back to a plain-byte result is refused because
it is no longer an exact coordinate of that result family.

The shared byte-pair result coordinate shape is unchanged. Its independently
minted result identity remains for a separate falsifier.

## Reading boundary

This pass does not narrow byte-result replay. The reader still validates the
exact source occurrences through the source completeness boundary, recomputes
the byte findings, validates the lifecycle occurrences and their order, and
requires one result for the Act.

Those reads and the separate binding occurrence may receive later independent
pressure. They cannot borrow a result from this identity subtraction.

## Disposition

```text
prospective plain-byte Measurement-result identity   withdrawn
copied plain-byte family result identity              withdrawn
actual result occurrence identity                     retained
actual Act occurrence identity                        retained
binding, Act, and result occurrences                  retained
byte findings and downstream result-position use      retained
```

No Act, result, relation, finding, Book clause, Witness Grammar coordinate, or
admitted word is added or removed.
