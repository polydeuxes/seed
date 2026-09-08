# External Witness invocation time boundary investigation 001

## Question

Why does the current operator host provider end every external Witness
invocation after two seconds?

This investigation preserves bounded host mechanics. It asks whether the
exact two-second count belongs to every invocation or whether one provider
constant is being reused across invocations with different exact limits.

It changes no Book, witness grammar, runtime, script, or test.

## Direct finding

The repository establishes this distinction:

```text
external Witness invocation has an exact time boundary
!=
every external Witness invocation has the same time boundary
```

The exact `2.0` count entered `scripts/operator_host_provider.py` with the
short `!ls` and `!cat` roads. Pytest and calculator were added later and
inherited the same module constant. Neither later caller supplies an exact
time-limit coordinate to the shared invocation function.

Elsewhere, compiled external Witness invocations already carry their exact
time limit as an invocation coordinate. Current examples use several counts:

| invocation | exact second count |
|---|---:|
| terminal and Surf observations | 2.0 |
| external JSON and comparison observations | 5.0 |
| Piper observation | 15.0 |
| sixteen-book supplied-material observation | 31.0 |
| compiled invocation default | 30.0 |
| explicit time-boundary test | 0.25 |

The shared host-provider `2.0` is therefore a provider constant reused
across unlike invocations, not a repository-wide time law.

The current host road has a second gap: it preserves generic known loss when
a boundary is reached, but its supplied occurrences do not preserve the exact
time count or distinguish a reached time boundary from reached output or
error byte boundaries.

This finding does not establish a different pytest count. It does establish
the immediate Witness invocation seam: shared bounded mechanics need an exact
limit input instead of silently applying one module constant to every caller.
Making that input explicit does not choose its value or establish Seed-native
Responsibility for the external process.

## 1. Current host mechanics

`scripts/operator_host_provider.py` declares:

```python
TIME_LIMIT_SECONDS = 2.0
MATERIAL_BYTE_LIMIT = 65536
```

The same `_bounded_invocation()` function serves:

```text
!ls
!cat
!pytest
!calculator
```

Its call accepts an argument vector, supplied-material consumer, environment,
and working directory. It accepts no exact time-limit coordinate. Every call
therefore computes its deadline from the module constant.

The mechanics themselves are bounded and exact about material already
received:

```text
external process
├── standard input closed
├── shell disabled
├── output bytes bounded
├── error bytes bounded
├── time bounded
└── remaining pipe material briefly drained after process termination

boundary reached
↓
process ended
↓
exact available output and error supplied
↓
known loss supplied
```

Removing the time boundary would remove a real protection against an external
process that does not return. Nothing in this investigation warrants that
removal.

The exact second count, however, is not part of the invocation call or its
supplied result coordinates.

## 2. The two-second count entered with short commands

Commit `85d71e21` introduced the provider on August 16, 2026. At that point
the module supported only:

```text
!ls
!cat
```

That first provider declared `TIME_LIMIT_SECONDS = 2.0` and the
65,536-byte material boundary together. It preserved a bounded prefix and
known loss when a boundary was reached.

Commit `7afda99e`, twenty-seven minutes later, added `!pytest`. It routed
pytest through the existing `_bounded_invocation()` and did not add a pytest
time coordinate or amend the two-second count.

Commit `51383f64` later added `!calculator`. It likewise reused the existing
provider boundary.

The history therefore carries this sequence:

```text
two-second provider for !ls / !cat
↓
pytest added to the provider
↓
calculator added to the provider
```

It does not carry:

```text
pytest Responsibility / Scope
↓
exact two-second limit
```

Nor does it carry that relation for calculator.

## 3. Piper confirms invocation-specific limits

The current Piper Witness invokes its external function with:

```python
time_limit_second_count=15.0
material_byte_count_limit=1048576
```

The Piper road therefore confirms the reason bounded external invocation
mechanics matter. It does not establish the host provider's exact two-second
count. Piper uses the separate compiled-material invocation road and carries
its own exact limits.

The first Piper observation used twelve seconds. Its present observation uses
fifteen seconds. That change did not alter a repository-wide external
Witness limit; it changed the exact invocation coordinate supplied to Piper's
road.

Thus:

```text
Piper requires bounded external mechanics
!=
Piper establishes two seconds for pytest
```

## 4. Compiled invocation already preserves the missing distinction

`scripts/compiled_material_invocation.py` carries these coordinates on every
`MaterialInvocationOccurrence`:

```text
time_limit_second_count
material_byte_count_limit
input_boundary_accepted_byte_count
returned
time_limit_reached
stdout_byte_count_limit_reached
stderr_byte_count_limit_reached
returncode
stdout_bytes
stderr_bytes
```

Its occurrence validation requires a positive exact time count. A timed-out
occurrence preserves `time_limit_reached=True`. Output and error limits have
separate coordinates. Compare roads refuse to treat invocations with
different exact limit coordinates as the same input condition.

Commit `5f4f3f0c` made this distinction explicit by replacing the Python name
`wait_seconds` with `time_limit_second_count` and by
retaining that coordinate across source and result invocations.

This road demonstrates that invocation-local time counts are already
expressible without removing bounded mechanics or making one count common to
every invocation. It does not choose the exact counts for the operator host
callers. The two roads remain separate.

## 5. Active Book orientation

The active Book does not declare an external host-process Responsibility or a
two-second pytest limit.

It does establish where exact limits belong:

```text
current Standing
↓
exact Responsibility
├── responsible boundary
├── subject
├── exact Act
├── Authority
├── Scope
├── Locality
└── limits
```

`02_authority_scope.md` says Scope bounds the subjects, relations, Acts,
occurrences, results, Localities, and limits addressed by an exact
Responsibility. It also refuses one Scope from establishing Scope for another
Responsibility.

`03_acts_and_occurrences.md` requires an exact Responsibility to carry its
limits with its responsible boundary, subject, Authority, Scope, and
Locality.

`04_source_coordinates.md` requires exact source material and results to
preserve known loss and limits.

This supports:

```text
exact invocation Responsibility
└── exact Scope and limits for that invocation
```

It does not support:

```text
one provider constant
↓
exact limit for every invocation
```

The active Book coordinates orient any later Seed-native use of an exact
limit. They do not require `_bounded_invocation()` to hide its mechanical
input behind a module constant until an external-process Responsibility is
recorded. The host-provider road currently records no such Responsibility or
Act occurrence; that is a separate constitutional question.

## 6. The ordinary sixteen-book observation reaches this boundary

The ordinary `!pytest` observation collected all 1,448 admitted pytest nodes
in 1.64 seconds. Execution then completed six tests before the two-second host
boundary ended the process.

The sixteen-book tests did not run. No corpus byte crossed into the invocation
Locality.

The resulting supplied population preserved:

```text
six exact dot occurrences
empty error material
empty implementation catalog with known loss
empty implementation measurement with known loss
empty completion material with known loss
```

This establishes that two seconds does not contain the requested complete
pytest invocation. It does not establish what the correct exact limit is.

The sixteen-book compiled-material witness independently uses thirty-one
seconds. That is testimony about its exact invocation road, not permission to
copy thirty-one seconds into the operator provider.

## 7. Known loss preserves less than the host mechanics know

`_bounded_invocation()` distinguishes three results internally:

```text
time_limit_reached
output_limit_reached
error_limit_reached
```

The supplied completion then compresses any of them into the same text:

```text
material beyond the supplied boundary is not available
```

The supplied occurrences do preserve that material was lost. They do not
preserve:

```text
the exact two-second count
which exact boundary was reached
the 65,536-byte count when a byte boundary was reached
```

The compiled invocation road preserves all of those distinctions separately.

This is adjacent to the time-count question and remains unresolved here. The
investigation does not amend the supplied Witness payload or invent a new
loss vocabulary.

## 8. Exact stop

The recovered road is:

```text
external Witness invocation
↓
bounded host mechanics required
↓
shared invocation function accepts no exact limit inputs
↓
every caller inherits module time and byte constants
↓
exact material and generic known loss supplied
```

The directly established defect is the invocation function boundary:

```text
_bounded_invocation(
    argv,
    supply,
    environment,
    working_directory,
)

missing:
    exact time limit
    exact material byte limit
```

Separating shared mechanics from caller-supplied limits does not require a new
constitutional position. It also does not establish the exact values each
caller should supply.

Changing only pytest's number would still be a host-authored choice. The next
mechanical correction may make limits exact inputs while leaving the pytest
value open and the sixteen-book experiment blocked.

## Disposition

| Question | Finding |
|---|---|
| Must external Witness mechanics remain bounded? | yes |
| Does every external Witness invocation carry the same exact time count? | no |
| Did two seconds enter with pytest? | no; it entered with `!ls` and `!cat` |
| Did pytest independently establish two seconds? | no |
| Does Piper use two seconds? | no; the current Piper observation uses fifteen |
| Does the compiled invocation road preserve invocation-local limits? | yes |
| Does the operator host road preserve its exact time count in supplied material? | no |
| Does generic known loss distinguish which boundary was reached? | no |
| Does active Book law orient limits to exact Responsibility and Scope? | yes |
| Is that exact host invocation Responsibility recorded today? | no |
| Must the shared helper retain implicit constants until that Responsibility is recorded? | no |
| May this investigation choose a longer pytest count? | no |

The timer stays. The implicit shared number is the compression. The immediate
mechanical correction is caller-supplied exact limits; recovering each
caller's value and any Seed-native Responsibility remains separate work.
