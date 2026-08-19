# Bounded Locality replay reconstruction bottleneck investigation 001

## Question

Why does the ordered-path / recorded-pair-finding Compare witness require more
than one minute for twenty-five tests, and does its repeated JSON work carry a
constitutional distinction?

This investigation does not amend the durable record, operator acquisition,
Witness acquisition, Standing, or the active Book.

## Exact storage boundary

Operator and Witness material bytes do not enter the JSON material column.
They are preserved as exact material addressed by an exact-material identity.

The JSON material column preserves the developer-shaped coordinates of one
runtime occurrence:

```text
identity
kind
timestamp
material coordinates
exact-material reference
Locality identity
```

On a durable read, `_row_to_event` returns that stored representation to an
Event material dictionary and screens every dictionary key against the secret
boundary. This is storage reconstruction. It does not parse operator material,
discover a relation, perform material acquisition, establish Standing, or add
a coordinate.

Therefore:

```text
exact acquired bytes
!= JSON occurrence-coordinate material

JSON storage reconstruction
!= interpretation of acquired bytes
```

Removing the reconstruction while retaining the current JSON storage form
would leave no exact runtime representation of the recorded coordinates after
restart. A different durable representation would be a separate storage-
grammar investigation.

## Measured repeated work

The clean baseline for:

```text
tests/test_comparison_of_ordered_relation_path_with_recorded_pair_findings.py
```

was:

```text
25 passed in 69.67 seconds
```

The branch before this investigation measured:

```text
25 passed in 69.87 seconds
```

Profiling located repeated bounded Locality reconstruction:

```text
84,106 stored-row to Event reconstructions
91,153 JSON loads
117,481 compressed-material reads
37,243 exact occurrence get calls
18,389 append-order occurrence reads
```

The pressure did not come from material acquisition. It came from a completed
family lifecycle repeatedly asking for current Standing from the beginning
after recording an exact occurrence whose identity it already held.

## Existing lawful integration

`advance_operator_locality_standing` already carries the required asymmetry:

```text
one exact prior bounded Locality read
+ exact identities recorded by one family
↓
one later bounded Locality read
```

It does not infer an omitted occurrence. The responsible family supplies the
exact identities it just recorded, and the ordinary replay refusals validate
those occurrences against the carried input.

The operator console already uses this road. The higher ordered-path Compare
family did not.

## Integrated family lifecycle

The higher Compare lifecycle now performs one complete current read at the
entry to each public family stage:

```text
Responsibility assignments
Applicability
Compare Act Evidence / Participation
Compare Yield / result
```

Within each stage it advances that exact read serially:

```text
prior read
+ assignment occurrence
↓
later read

prior read
+ Applicability Act Evidence
+ Yield Evidence
+ Applicability result
↓
later read

prior read
+ Compare Act Evidence / Participation
↓
later read

prior read
+ Yield Evidence
+ Compare result
↓
later read
```

The initial unassigned subject population is read once. Recording one
assignment removes that exact subject; an assignment creates neither a new
ordered path nor a new recorded pair-comparison result. The already-complete
subject population can therefore be recorded serially without reconstructing
the same Cartesian surface after each assignment.

No additional persistent or process-local history representation was added.
The returned read remains fully reproducible from the durable occurrences.

## Refusals preserved

The integration changes no constitutional outcome:

```text
subject presence
!= Applicability

Applicability
!= Participation

Act Evidence
!= Yield

result occurrence
!= result Standing
```

Each assignment still names the immediately prior exact Standing boundary.
Each Yield and result remains a separate occurrence. Inapplicable inputs still
record no Participation or Compare Act Evidence. A second complete pass records
nothing.

The integration test independently counts complete current reads and requires:

```text
four public stages
→ four complete current reads
```

Every occurrence inside a stage is carried by exact advancement rather than a
new complete reconstruction. The final carried read must equal a fresh replay.

## Result

After integration, the same twenty-five-test witness measured:

```text
25 passed in 54.33 seconds
```

This is 15.54 seconds below the branch baseline and 15.34 seconds below the
clean detached baseline.

The SQLite restart test remains the largest single call:

```text
11.70 seconds
```

That result is useful pressure. Restart necessarily reconstructs durable
coordinates at least once under the current storage grammar, but the witness
then performs several independent full current reads and a full Locality read.
Whether those reads can lawfully share one explicitly carried bounded input is
the next exact question.

## Disposition

```text
JSON as operator-material decoder                         refused description
JSON as current durable occurrence representation         observed
one reconstruction after restart                          currently required
reconstruction after every known serial family occurrence not required
family-local exact read advancement                        integrated
new Standing or relation from advancement                  none
remaining restart reconstruction pressure                  open
```
