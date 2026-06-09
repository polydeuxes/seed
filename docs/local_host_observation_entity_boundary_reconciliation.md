# Local Host Observation Entity Boundary Reconciliation

## Purpose

This document captures an operator-discovered local-host observation issue before implementation work begins.

The goal is to distinguish:

```text
Duplicate facts
```

from:

```text
Improper fact scoping
```

and from:

```text
Lossy output formatting
```

## Evidence Reviewed

A local observation SQLite snapshot was inspected directly.

The snapshot contained:

```text
3699 events
1233 observation events
1233 evidence events
1233 fact events
1233 projected facts
549 unique subject/predicate/value triples
1226 unique subject/predicate/value/dimensions groups
```

This means many facts look duplicated when dimensions are ignored, but most fact records preserve additional scope in their dimensions.

## Operator Symptom

The operator observed output like:

```text
host mount_option rw
host mount_option relatime
host listening_protocol tcp
host listening_address 0.0.0.0
host interface_mtu 1500
host block_device_rotational true
```

with repeated counts for common values.

At the CLI surface, these appear to be duplicate host-level facts.

## Important Correction

The uploaded database showed that many of these facts include dimensions.

Example shape:

```text
subject: host
predicate: mount_option
value: rw
dimensions:
    mount_point: /
    mount_option: rw
```

Therefore the issue is not only duplicate fact storage.

The issue is a combination of:

```text
host-level subject assignment
child-object scope stored in dimensions
current-facts output hiding dimensions
```

## Boundary Finding

Many observed properties are not really properties of the host directly.

They are properties of child entities.

Examples:

| Predicate family | Current apparent subject | Better conceptual subject |
| --- | --- | --- |
| mount_option | host | mount |
| filesystem_type | host | mount or filesystem |
| mounted_device | host | mount |
| listening_protocol | host | listening endpoint |
| listening_address | host | listening endpoint |
| listening_port | host | listening endpoint |
| interface_mtu | host | interface |
| interface_operstate | host | interface |
| interface_role | host | interface |
| block_device_rotational | host | block device |
| block_device_size_bytes | host | block device |
| block_device_vendor | host | block device |

## Why Simple Dedupe Is Not Enough

Simple dedupe would reduce repeated output.

For example:

```text
host mount_option rw
```

could be emitted once instead of many times.

However, that still loses the most important question:

```text
Which mount?
```

Likewise:

```text
host interface_mtu 1500
```

still loses:

```text
Which interface?
```

Dedupe reduces noise.

Entity scoping preserves meaning.

## Candidate Better Shape

Mounts:

```text
host has_mount <mount-id>
mount:<mount-id> mount_option rw
mount:<mount-id> filesystem_type ext4
mount:<mount-id> mounted_device /dev/example
```

Listening endpoints:

```text
host has_listening_endpoint <endpoint-id>
endpoint:<endpoint-id> listening_protocol tcp
endpoint:<endpoint-id> listening_address 0.0.0.0
endpoint:<endpoint-id> listening_port 9100
```

Interfaces:

```text
host has_interface <interface-id>
interface:<interface-id> interface_mtu 1500
interface:<interface-id> interface_operstate up
interface:<interface-id> interface_role container
```

Block devices:

```text
host has_block_device <device-id>
block_device:<device-id> block_device_rotational true
block_device:<device-id> block_device_size_bytes <bytes>
block_device:<device-id> block_device_vendor <vendor>
```

## Likely Implementation Direction

Implementation should avoid treating all local observations as direct host properties.

A narrow implementation should:

```text
Preserve host identity.
Create stable child entity identities.
Attach child properties to child entities.
Preserve host-to-child relationship facts.
Keep dimensions or equivalent support data where helpful.
Ensure current-facts output does not hide necessary scope.
```

## Tests To Add Before Or With Implementation

Suggested characterization tests:

```text
Repeated mount options are not emitted as duplicate host-level facts.
Mount options remain associated with specific mount identities.
Listening protocols and ports are scoped to endpoint identities.
Interface MTU and role are scoped to interface identities.
Block device properties are scoped to block device identities.
Host-to-child relationship facts remain present.
current-facts output preserves enough scope to distinguish child entities.
```

## Non-Goals

This audit does not require changing the local collector immediately.

It also does not require inventing a full graph model.

The immediate goal is to avoid a premature fix that only dedupes output while preserving the wrong conceptual subject.

## Current Conclusion

The operator-discovered issue is best described as:

```text
Local host observation currently exposes child-object properties as host-level facts at the user-facing fact surface.
```

The database shows that some child scope is already preserved in dimensions.

The next implementation should therefore address both:

```text
entity boundary modeling
```

and:

```text
scope-preserving fact output
```

rather than applying simple deduplication alone.
