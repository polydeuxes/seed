# Host invocation current-coordinate replay profile 001

## Boundary

This profile begins at `b02a7908` after one unchanged host-invocation Witness
had previously exceeded 105 seconds before reaching its assertions. It changes
no Witness material, occurrence count, runtime corpus, or test boundary.

The question is:

```text
one bounded host invocation
→ which exact coordinate read repeats?
```

No cache, alternate road, smaller source, or performance framework is used.

## External profile

The unchanged Witness is:

```text
tests/test_operator_host_invocation.py
::test_host_provider_receives_an_acquired_exact_command_before_it_occurs
```

An external 30-second `cProfile` run was interrupted before the test
completed. During the profiled interval it recorded:

```text
84,042,257 total Python calls
74,345,562 primitive calls

advance_operator_current_coordinates                 3,716 / 20 calls
read_operator_current_coordinates_through             3,712 / 16 calls
addressed-byte determination _read_binding             8,956 / 30 calls
read_requirements_of_yield_relation                       81,618 calls
get_recorded_operator_material_source                     33,418 calls
deepcopy                                            9,826,661 / 780,811 calls
```

Almost the entire test interval was below:

```text
source-position path work
→ shared-position result read
→ addressed-byte determination result read
→ current-coordinate replay
```

The host-provider bridge itself was not the expensive seam.

## Exact dropped coordinate

During current-coordinate replay, the addressed-byte Applicability Act reader
already received the exact prior coordinates for its occurrence boundary.

It used those coordinates to read the Applicability binding, then resolved the
governed determination binding through:

```text
_determination_binding_addressed_by_applicability(...)
```

That helper called the same binding reader without passing the already-held
prior coordinates. The binding reader therefore reconstructed current
coordinates through its recorded boundary. During that reconstruction the
same Applicability occurrence was encountered and the same coordinate was
dropped again.

The repeated physiology was therefore:

```text
exact prior coordinates already held
→ omitted across one exact binding relation
→ replay Locality from its boundary
→ encounter the same relation
→ omit the coordinates again
→ replay again
```

This was not new work owed by the material. It was the same exact coordinate
being rediscovered because one reader failed to carry it through an internal
relation.

## Bounded repair

Commit `82be8dde` carries the already-held `prior_coordinates` through the
Applicability-to-determination-binding relation. A public read without prior
coordinates still reconstructs them through the same exact boundary; a
bounded replay no longer discards coordinates it already owns.

No result, relation, subject, boundary, refusal, or replay rule changed.

## Result

After the repair, the unchanged Witness completes:

```text
before
    >105 seconds without reaching its assertions

external 30-second profile
    interrupted before completion

after
    1 passed in 0.45 seconds
```

The focused addressed-byte determination and bounded current-coordinate
Witnesses also complete:

```text
37 passed in 3.08 seconds
```

## Smallest exact finding

```text
performance explosion
    repeated reconstruction of one exact carried coordinate

missing physiology
    carry prior coordinates through the exact
    Applicability → governed-binding read

cache or shortcut
    not required
```

The profile supports a narrow performance discriminator for later roads:

> When an exact reader is already supplied the current coordinates for its
> boundary, every nested reader over that same boundary must either carry
> those coordinates or establish why a different boundary is required.

This is ordinary coordinate ownership, not a new runtime object.
