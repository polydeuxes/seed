# Source-boundary bridge and material front-door investigation 001

## Question

Do console material, material returned by one Witness invocation, and material
produced by a compiled external Witness each retain their own exact
source-boundary bridge before entering one shared material physiology?

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

## Compiled external Witness material

The pytest external Witness can return ordinary invocation material plus two
additional exact occurrences:

```text
compiled Witness catalog
compiled Witness measurement
```

Those occurrences retain distinct source-boundary strings and their exact
bytes. They do not currently retain an exact compiled-Witness subject,
compiled-Witness occurrence reference, or compiled-Witness-to-source-Act
binding in Seed.

They are passed through the same `SuppliedWitnessMaterialOccurrence` consumer
as ordinary invocation output and then through the ordinary Witness material
source road.

Current runtime therefore establishes:

```text
compiled Witness material
is exact returned material at a distinct named source boundary
```

It does not yet establish:

```text
compiled external Witness
-- exact source-boundary bridge -->
compiled Witness material result
```

The source-boundary string cannot own that missing relation by itself.

## Smallest exact distinctions

```text
shared exact-material result front door                         present

console route-owned source-boundary bridge                      present

Witness invocation-return route-owned bridge                    present

compiled external Witness route-owned bridge                    absent

compiled Witness bytes and distinct source-boundary material    present
```

The compiled external Witness may be nested inside one Witness invocation,
but nested provenance and a route-owned subject-to-Act binding are different
distinctions.

## Runtime cleanup frontier

1. Repair the ordinary Witness source road to carry a direct
   subject-to-Act binding without retired Responsibility vocabulary.
2. Preserve the invocation-return bridge as the owner of invocation Locality,
   command, read, and returned-occurrence coordinates.
3. Determine what exact occurrence identifies a compiled external Witness
   before adding a compiled-Witness bridge. A source-boundary label alone does
   not establish it.
4. Keep all roads converged at the exact-material result front door. Do not
   merge their boundary mechanics or recreate later material physiology for
   each route.

## Stop

No new compiled-Witness relation is added by this investigation. The exact
compiled Witness occurrence coordinate is not currently carried into Seed.
