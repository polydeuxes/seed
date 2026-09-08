# Source-boundary bridge and material front-door investigation 001

## Question

Do console material and material returned by one Witness invocation retain
their own exact source-boundary bridge before entering one shared material
physiology? Does a compiled external Witness enter Seed through that road at
all?

This investigation reads the active runtime at `78b9ce5f`. It changes no Book,
Witness Grammar, or runtime physiology.

## Recovered shared front door

Two source roads currently append exact material through:

```text
_append_exact_material_result_occurrence
```

Later material work can read either road through:

```text
read_exact_material_result
```

That shared boundary requires an exact material result with its prior intact
Act occurrence and Yield. It does not erase the source road that produced the
result.

The current topology is therefore:

```text
route-owned source physiology
            ↓
exact material result front door
            ↓
shared later material physiology
```

## Console bridge

The console road owns an operator-boundary subject-to-Act binding before the
boundary is touched. It then records its exact Act occurrence, Yield, material
result, source boundary, Scope, Locality, known loss, and Unknown.

The operator road enters the shared front door through the operator result
occurrence. Its boundary mechanics remain distinct from the other source
roads.

## Witness invocation-return bridge

`record_supplied_witness_material_source` first requires the exact invocation
Locality result, command occurrence, prior supplied occurrences, mechanical
read coordinates, and source boundary carried by the Witness return.

It then delegates material preservation to `record_witness_material_source`,
which enters the shared exact-material front door.

This is a real route-owned bridge before the shared material result:

```text
Witness invocation relation
+ command occurrence
+ exact returned occurrence
+ exact read occurrences
            ↓
Witness material source road
            ↓
exact material result front door
```

The inner Witness source road still carries retired `responsibility` and
`responsible_boundary` prose and has no separately recorded direct
subject-to-Act binding. That contradicts the corrected Book, but it does not
erase the invocation bridge that precedes it.

## Compiled external Witness

The pytest external Witness can produce two observer artifacts:

```text
compiled Witness catalog
compiled Witness measurement
```

Those artifacts test external behavior. They are not source material that Seed
is meant to take through its exact-material front door.

Current `operator_host_provider` nevertheless passes them through the same
`SuppliedWitnessMaterialOccurrence` consumer as ordinary invocation output and
then through the ordinary Witness material source road.

That is a runtime crossing to remove, not a missing route-owned bridge to add.
The exact invocation output and error remain Witness-return material. The
compiled Witness catalog and measurement remain outside Seed as observer
artifacts.

Current runtime incorrectly establishes:

```text
compiled Witness observer artifact
is exact returned material at a named source boundary
```

The source-boundary string cannot turn an external observer artifact into a
Seed source occurrence.

## Smallest exact distinctions

```text
shared exact-material result front door                         present

console route-owned source-boundary bridge                      present

Witness invocation-return route-owned bridge                    present

compiled external Witness is external observer behavior          real

compiled Witness artifacts entering Seed as returned material    incorrect
```

Running a compiled external Witness may itself happen through a host process,
but its observer artifacts and that process's ordinary output are different
material.

## Runtime cleanup frontier

1. Repair the ordinary Witness source road to carry a direct
   subject-to-Act binding without retired Responsibility vocabulary.
2. Preserve the invocation-return bridge as the owner of invocation Locality,
   command, read, and returned-occurrence coordinates.
3. Stop supplying compiled external Witness artifacts through the invocation
   material callback. Keep their behavior checks external.
4. Keep both Seed source roads converged at the exact-material result front
   door. Do not
   merge their boundary mechanics or recreate later material physiology for
   each route.

## Stop

No compiled-Witness relation is added by this investigation. A compiled
external Witness remains external.
