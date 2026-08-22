# State Summary Filesystem Projection Boundary Audit

## Purpose

This document performs a documentation-only audit of the `seedstate` filesystem summary boundary after the Prometheus relationship and host-vs-endpoint fact attachment cleanups.

This is an implementation-boundary audit.

It does not implement code, modify schemas, modify runtime behavior, modify projections, modify tests, introduce ontology, or add new relationship vocabulary.

The goal is to explain why filesystem measurements still dominate the state summary and why that output exposes a storage-topology projection problem rather than an acquisition problem.

---

## Triggering output

Representative `seedstate` output now shows:

```text
State Summary

Facts: 3811
Observations: 3764
Issues: 20
measurement current samples: 947
graph issues: 19 warnings, 1 error

filesystems:
  10.0.0.1:9100 /: ... bytes free/total
  192.168.254.100:9100 /: ... bytes free/total
  192.168.254.100:9100 /mnt/merged: ... bytes free/total
  192.168.254.100:9100 /mnt/example_host_205/sda1: ... bytes free/total
  192.168.254.101:9100 /mnt/example_host_f/sda1: ... bytes free/total
  192.168.254.101:9100 /mnt/example_host_205/sda1: ... bytes free/total
```

This output is technically grounded in observed filesystem measurements, but it is semantically over-broad as a top-level state summary.

It presents every observed filesystem measurement as if the summary consumer can treat it as the same kind of filesystem state.

That is not true in a cluster with cross-mounts, merger views, compatibility paths, retired-node path names, and local physical disks.

---

## References reviewed

Architectural documents:

- `docs/storage_topology_ambiguity_and_operator_clarification_reconciliation.md`
- `docs/prometheus_boundary_cleanup_status_reconciliation.md`
- `docs/prometheus_host_endpoint_fact_attachment_audit.md`
- `docs/prometheus_acquisition_interpretation_routing_promotion_audit.md`
- `docs/prometheus_target_and_filesystem_identity_reconciliation.md`

Implementation surfaces inspected:

- `seed_runtime/state.py`
- `seed_runtime/observation_sources.py`
- `seed_runtime/observations.py`
- `seed_runtime/observation_normalizers.py`
- `predicate_catalog/core.json`

Operator-provided runtime output inspected:

- Current `seedstate` summary showing 947 measurement current samples and many filesystem rows across Prometheus endpoint subjects.

---

## Scope

In scope:

- How filesystem measurement facts survive state projection.
- How filesystem measurements are grouped by subject, predicate, and dimensions.
- Why endpoint-scoped filesystem rows still appear as top-level filesystems.
- Why cross-mount and retired-node naming produce ambiguity.
- What the state summary should avoid implying.
- What the next implementation slice should inspect.

Out of scope:

- Deleting Prometheus filesystem observations.
- Changing Prometheus acquisition.
- Adding storage topology ontology.
- Adding endpoint ownership vocabulary.
- Adding candidate systems.
- Implementing operator-question infrastructure.
- Changing `seedstate` in this audit.

---

## Current implementation facts

### 1. Measurements are retained as current samples

`StateProjector.project` retains durable facts and prunes measurement history to current samples.

Measurement retention is performed by `_retain_projected_measurement_history`, which groups measurements by:

```text
subject_key(fact)
predicate
dimensions
```

and retains the most recent sample per series.

This is correct for measurement history control.

It is not storage topology classification.

### 2. Endpoint-scoped predicates keep exact endpoint subjects

`_projection_subject` keeps endpoint-scoped facts separate from alias canonicalization:

```text
if fact.predicate in _ENDPOINT_SCOPED_PREDICATES:
    return fact.subject_id
return canonical(fact.subject_id)
```

This was an important cleanup boundary. It prevents endpoint facts from being automatically reattached to host aliases.

However, exact endpoint subject preservation does not solve summary meaning.

It still produces rows such as:

```text
192.168.254.101:9100 /mnt/example_host_205/sda1
```

which are accurate as endpoint-scoped measurements, but ambiguous as high-level storage topology.

### 3. Fact supports group measurements by current sample semantics

`_project_fact_supports` treats measurements differently from durable facts.

For measurements, it chooses a current sample and emits `predicate_semantics = measurement` and `support_kind = current_sample`.

This is also correct as measurement projection.

It still does not answer:

```text
Is this local storage?
Is this remote storage?
Is this a bind mount?
Is this a merger/union view?
Is this a compatibility path?
Is this a retired-node path?
Should this appear in top-level state summary?
```

### 4. Prometheus acquisition preserves filesystem dimensions

Prometheus filesystem observations preserve filesystem dimensions such as:

```text
mountpoint
device
fstype
```

These dimensions are necessary evidence.

They are not sufficient to decide ownership or summary importance.

---

## Core finding

The remaining problem is not that filesystem measurements exist.

The problem is that the state summary projection treats all current filesystem measurement samples as summary-worthy filesystem rows without topology classification.

The implementation currently has a good measurement-current-sample projection, but lacks a filesystem-summary selection boundary.

Current conceptual shape:

```text
filesystem_free_bytes / filesystem_total_bytes facts
        ↓
current measurement samples
        ↓
flat filesystems summary
```

Required boundary:

```text
filesystem measurements
        ↓
measurement scope classification
        ↓
summary selection
        ↓
operator clarification when topology is ambiguous
```

---

## What the current summary implies accidentally

The flat `filesystems:` block can accidentally imply:

```text
host owns this storage
```

or:

```text
this mount is primary host storage
```

or:

```text
this path name reflects current topology authority
```

or:

```text
each displayed row is equally important host filesystem state
```

Those implications are not justified by Prometheus filesystem metrics alone.

A safer reading is:

```text
this endpoint reported a filesystem measurement for this mountpoint and dimensions
```

---

## Boundary violations exposed by the output

### Boundary 1: measurement visibility vs storage ownership

Example:

```text
192.168.254.101:9100 /mnt/example_host_205/sda1
```

Safe claim:

```text
The 192.168.254.101:9100 scrape target reported measurements for /mnt/example_host_205/sda1.
```

Unsafe implied claim:

```text
example_host_101 owns example_host_205 storage.
```

### Boundary 2: mountpoint path vs topology authority

A path containing a node name is not authority that the named node currently owns or serves the storage.

Example:

```text
/mnt/example_host_e/sda1
```

may be:

```text
remote mount
compatibility alias
retired-node retained path
historical cluster convention
bind mount
mirror path
```

### Boundary 3: physical disk vs mounted filesystem view

A mounted filesystem visible from a host is not necessarily a physical disk attached to that host.

The summary should not collapse:

```text
visible mount
        ↓
local physical drive
```

### Boundary 4: union view vs backing storage

Paths such as:

```text
/mnt/merged
```

may be merger/union views.

They should not be displayed as equivalent to local root or physical storage unless classified.

### Boundary 5: low-value runtime mounts vs important storage

Rows such as:

```text
/run
/run/lock
/run/user/1000
/boot/firmware
```

may be valid measurements, but they are usually not state-summary-level storage concerns.

They should be available in detailed views, not necessarily top-level summary.

---

## Operator clarification boundary

The filesystem summary should not ask about every row.

It should ask only when topology ambiguity affects ownership, recommendation, repair, backup safety, retired-node reasoning, capacity projection, or summary interpretation.

Ask-worthy cases include:

```text
/mnt/node*/sda1 appears on multiple hosts
```

```text
/mnt/sda1 and /mnt/example_host_e/sda1 may refer to same or related backing storage
```

```text
path refers to retired node name
```

```text
mountpoint appears local by path but device/fstype suggests remote or union mount
```

```text
capacity appears duplicated across multiple hosts or mountpoints
```

Not ask-worthy by default:

```text
/run
/run/lock
/run/user/*
/boot/firmware
```

unless an active question or issue makes them relevant.

---

## What a better summary projection should do

A safer state summary should separate filesystem facts into classes such as:

```text
local root / boot filesystems
local physical storage candidates
cluster cross-mounts
union/merged views
remote/network mounts
runtime/pseudo filesystems
ambiguous topology needing clarification
```

It should not need full topology ontology for the first cleanup.

A minimal projection cleanup could begin with classification heuristics and conservative display policy:

```text
show root and high-priority local candidates
summarize cross-mount counts
summarize runtime/pseudo mounts separately or suppress them from top summary
flag ambiguous cluster mount patterns for operator clarification
keep detailed filesystem measurements accessible elsewhere
```

---

## Important non-collapse rule

Do not solve state-summary spam by deleting facts.

Do not solve it by suppressing Prometheus filesystem acquisition.

Do not solve it by treating `/mnt/node*` as always remote without evidence or operator policy.

The correct boundary is projection selection and classification.

Measurements should remain preserved.

The top-level summary should become more selective and more honest about ambiguity.

---

## Likely implementation surfaces for next work

The current audit could not rely on repository-wide indexed search, but the relevant implementation surfaces are likely:

- State projection and fact support grouping in `seed_runtime/state.py`.
- CLI or command code that renders the `State Summary` and `filesystems:` block.
- Tests that assert `seedstate` / CLI state summary output.
- Predicate catalog semantics for `filesystem_free_bytes` and `filesystem_total_bytes`.
- Observation-source metadata and dimensions from Prometheus and local mount observations.

The next implementation prompt should first locate the renderer that emits:

```text
filesystems:
  <subject> <mountpoint>: <free>/<total> bytes free/total
```

Then it should narrow projection/display behavior rather than acquisition.

---

## Direct answers

### Is the filesystem spam caused by bad acquisition?

No.

The measurements are useful evidence. The spam is caused by unclassified summary projection.

### Is the filesystem spam caused by Prometheus alone?

Prometheus exposes the symptom because node-exporter reports many mountpoints across many scrape targets.

The underlying boundary is broader: storage topology classification and summary selection.

### Should filesystem facts be deleted or suppressed globally?

No.

They should remain available as detailed measurements.

### What should be fixed first?

The state-summary filesystem projection should stop treating all filesystem measurements as equal top-level rows.

### Should Seed ask the operator?

Yes, but only for materially meaningful ambiguity, such as cluster cross-mount conventions, retired-node path names, and possibly duplicate backing storage visible through multiple paths.

### Is weird topology a graph error?

Not by default.

It is ambiguity unless Seed holds incompatible claims.

---

## Recommended next safe move

Create an implementation task that:

1. Locates the state summary renderer that emits the `filesystems:` block.
2. Identifies which fact supports or facts feed that block.
3. Classifies the displayed rows by mountpoint/device/fstype/source metadata where possible.
4. Suppresses or summarizes low-value runtime/pseudo mounts from the top-level summary.
5. Keeps detailed measurement data available.
6. Emits a concise ambiguity section or issue candidate for cluster cross-mount patterns such as `/mnt/node*/sda1`.
7. Does not alter Prometheus acquisition or delete filesystem facts.

---

## Rejected solutions

Rejected:

1. **Delete Prometheus filesystem metrics.** They are valid evidence.
2. **Suppress all filesystem facts.** That loses useful monitoring data.
3. **Treat all `/mnt/node*/sda1` as remote.** This may be a good operator policy, but it must be evidence-backed.
4. **Treat all mountpoints as local disks.** This is the current problematic implication.
5. **Ask about every mountpoint.** That would create operator-question spam.
6. **Make graph validation flag every weird mount as an error.** Weird topology is not contradiction by default.
7. **Introduce full storage ontology immediately.** Useful later, but too broad for the next projection cleanup.

---

## Required report

### Files changed

- `docs/state_summary_filesystem_projection_boundary_audit.md`

### LOC changed

- Documentation-only new file.

### Major findings

- Filesystem measurements are valid evidence and should remain preserved.
- The current state summary projection is too broad because it displays all filesystem current samples as flat top-level filesystem rows.
- Endpoint-scoped subject preservation is necessary but not sufficient; summary projection still needs topology classification.
- Cluster cross-mounts, union views, retired-node compatibility paths, and runtime/pseudo mounts require classification or summary suppression.
- Operator clarification should be triggered by materially meaningful ambiguity, not by every unusual mountpoint.

### Recommended implementation target

Locate and narrow the `seedstate` filesystem summary renderer so it classifies, summarizes, or suppresses low-value/ambiguous filesystem measurements at presentation time while preserving the underlying facts and evidence.

### Documents intentionally left unchanged

- `docs/storage_topology_ambiguity_and_operator_clarification_reconciliation.md`
- `docs/prometheus_boundary_cleanup_status_reconciliation.md`
- `docs/prometheus_host_endpoint_fact_attachment_audit.md`
- `docs/prometheus_acquisition_interpretation_routing_promotion_audit.md`
- All runtime implementation files.
- All tests.
- All schema, ontology, predicate, relationship, projection, and authority definitions.
