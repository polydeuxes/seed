# Local Host Fact Surface Implementation Audit

## Purpose

This document is the follow-up implementation audit for the operator-discovered local-host observation fact-surface issue.

It follows:

```text
docs/local_host_observation_entity_boundary_reconciliation.md
```

The goal is to inspect the current implementation path before writing code.

## Question

The previous audit found that the operator-facing fact surface shows repeated host-level facts such as:

```text
host mount_option rw
host listening_protocol tcp
host interface_mtu 1500
```

The question for this audit is:

```text
Where does the scope get lost?
```

Candidate locations:

```text
LocalHostObservationSource
ObservationIngestor
StateProjector
FactView
current-facts formatter
```

## Implementation Path Reviewed

The relevant path is:

```text
scripts/seed_local.py --observe-local-host
        ↓
LocalHostObservationSource.collect()
        ↓
ObservationCollectionService.collect(...)
        ↓
ObservationIngestor.ingest(...)
        ↓
ObservationIngestor.observation_to_fact(...)
        ↓
StateProjector.project(...)
        ↓
build_fact_view(...)
        ↓
format_fact_views(...)
        ↓
scripts/seed_local.py --current-facts
```

## Findings

## 1. LocalHostObservationSource Already Emits Dimensions

The local host collector emits many host-subject observations with additional dimensions.

Examples include:

```text
interface facts with dimensions {interface: <name>}
mount facts with dimensions {mount_point: <path>}
listener facts with dimensions {protocol, address, port}
storage facts with dimensions {device: <name>}
```

Therefore the collector is not simply throwing scope away.

It uses:

```text
subject = host
predicate = child-object property
value = observed value
dimensions = child-object scope
```

This preserves some scope, but it does not make the child object the fact subject.

## 2. ObservationIngestor Preserves Dimensions

ObservationIngestor converts observations into evidence and facts while preserving dimensions.

The evidence payload includes:

```text
dimensions
```

The derived Fact also copies:

```text
dimensions=dict(observation.dimensions)
```

Therefore the scope is not lost during ingestion.

## 3. State Projection Uses Dimensions For Support Grouping

State support projection groups facts by:

```text
subject
predicate
dimensions
value
```

For durable facts, support groups preserve dimensions.

This explains the SQLite finding:

```text
1233 fact records
549 unique subject/predicate/value triples
1226 unique subject/predicate/value/dimensions groups
```

The apparent duplicates mostly collapse only when dimensions are ignored.

## 4. current-facts Hides Dimensions

The current fact view model contains:

```text
fact_id
subject
predicate
object
confidence
supporting_event_ids
```

It does not include dimensions.

The formatter prints only:

```text
* subject predicate object
```

Therefore the `--current-facts` surface hides the scope needed to distinguish:

```text
mount_option rw on /
mount_option rw on /var/lib/...
mount_option rw on /run/...
```

This is a direct contributor to the operator-visible duplicate symptom.

## 5. Impact View Already Reconstructs Scoped Views

The `--impact` path contains custom formatting logic for local host data.

It uses fact dimensions to group:

```text
mounts by mount_point
listeners by protocol/address/port
interfaces by interface
storage devices by device
```

This means a scope-aware presentation already exists for at least one CLI surface.

The problem is not that the implementation has no scoped reading capability.

The problem is that `--current-facts` is a flat fact list that hides dimensions.

## 6. Subject Modeling Remains A Design Question

Even though dimensions preserve scope, the conceptual subject is still usually the host.

Example shape:

```text
subject: host
predicate: interface_mtu
value: 1500
dimensions:
    interface: eth0
```

This is queryable, but it is not the same as:

```text
subject: interface:eth0
predicate: interface_mtu
value: 1500
```

The first design says:

```text
The host has an interface-scoped property.
```

The second design says:

```text
The interface is an entity with its own properties.
```

Both are valid, but they support different future capabilities.

## Root Cause Classification

The issue is not a single bug.

It is a layered fact-surface issue:

```text
Collector:
    host subject with scoped dimensions

Ingestor:
    preserves dimensions

Projector:
    groups by dimensions

Impact view:
    uses dimensions

Current facts view:
    drops dimensions

Entity model:
    does not yet promote mounts/endpoints/interfaces/devices to first-class subjects
```

## Recommended Immediate Fix

The safest small implementation is:

```text
Add dimensions to FactView.
Render dimensions in --current-facts when present.
```

Expected output shape:

```text
* host mount_option rw (mount_point=/)
* host interface_mtu 1500 (interface=eth0)
* host listening_protocol tcp (address=0.0.0.0, port=9100, protocol=tcp)
```

This would preserve current storage semantics while making the existing scoped evidence visible.

## Recommended Deferred Fix

A deeper implementation should consider first-class child entities:

```text
mount:<host>:<mount_point>
endpoint:<host>:<protocol>:<address>:<port>
interface:<host>:<interface>
block_device:<host>:<device>
```

with host-to-child relationships:

```text
host has_mount mount:<...>
host has_interface interface:<...>
host has_listening_endpoint endpoint:<...>
host has_block_device block_device:<...>
```

This should not be done as a quick dedupe patch.

It changes the entity model.

## Tests To Add For Immediate Fix

Suggested tests:

```text
FactView includes dimensions.
format_fact_views prints dimensions when present.
format_fact_views omits parentheses when dimensions are empty.
current-facts output distinguishes same subject/predicate/value with different dimensions.
current-facts output remains deterministic by subject, predicate, value, dimensions, and id.
```

## Tests To Add Before Deeper Entity Modeling

Suggested tests:

```text
LocalHostObservationSource emits dimensions for mount facts.
LocalHostObservationSource emits dimensions for listener facts.
LocalHostObservationSource emits dimensions for interface facts.
LocalHostObservationSource emits dimensions for storage facts.
Impact output groups local host facts by dimensions.
Host-level fact output does not imply mount/interface/endpoint values are unscoped host properties.
```

## Non-Goals

Do not remove observations.

Do not dedupe by subject/predicate/value alone.

Do not discard dimensions.

Do not promote child entities without an explicit entity-boundary design.

Do not infer service health, reachability, ownership, or availability from listener facts.

## Current Conclusion

The immediate operator pain is caused primarily by a scope-losing presentation surface.

The current implementation already preserves dimensions through collection, ingestion, and support projection.

Therefore the smallest safe next step is:

```text
Expose dimensions in current-facts output.
```

The deeper architectural question remains:

```text
Should local host child objects become first-class entities?
```

That question should be handled separately from the immediate CLI fact-surface repair.
