# Storage Topology Ambiguity And Operator Clarification Reconciliation

## Purpose

This document performs a documentation-only reconciliation of storage topology ambiguity, filesystem measurement projection, ownership interpretation, and when Seed should ask the operator for clarification.

This is an architectural boundary audit.

It does not implement code, modify schemas, change runtime behavior, add predicates, add relationship vocabulary, alter projections, modify tests, or redefine ontology.

The goal is to distinguish:

```text
filesystem measurement
mountpoint
mounted path
backing device
remote mount
bind/mirror mount
physical storage ownership
cluster storage topology
retired-node compatibility path
operator clarification need
```

and determine when ambiguity should become an operator question rather than a contradiction, graph error, or silent projection.

---

## Triggering observation

A current `seedstate` output shows Prometheus filesystem measurements dominating the state summary:

```text
filesystems:
  10.0.0.1:9100 /: ... bytes free/total
  192.168.254.100:9100 /: ... bytes free/total
  192.168.254.100:9100 /mnt/merged: ... bytes free/total
  192.168.254.100:9100 /mnt/example_host_205/sda1: ... bytes free/total
  192.168.254.101:9100 /mnt/example_host_f/sda1: ... bytes free/total
  192.168.254.101:9100 /mnt/example_host_205/sda1: ... bytes free/total
```

The observed environment intentionally contains cluster cross-mounts and compatibility paths. Some retired node topology names remain in mount paths because the filesystem layout could not be fully renamed without disrupting existing topology.

Example operator-provided scenario:

```text
example_host /mnt/sda1
example_host /mnt/example_host_e/sda1
```

may represent two paths into the same or related storage topology, not two independently owned local physical disks.

Therefore, the issue is not merely output noise. The state summary is exposing an unresolved topology interpretation problem.

---

## Core finding

A strange filesystem layout is not a contradiction by default.

The safer classification is:

```text
ambiguous topology evidence
```

or:

```text
topology anomaly requiring classification
```

It becomes a contradiction only when Seed already holds a stronger claim that conflicts with the new evidence.

For example:

```text
/mnt/example_host_e/sda1 means physical storage owned by example_host_e
```

would conflict with evidence that:

```text
example_host /mnt/sda1 maps to the same backing storage
example_host also exposes /mnt/example_host_e/sda1
example_host_e is retired
```

But without the ownership claim, Seed should not fabricate contradiction.

It should preserve ambiguity and ask only when the ambiguity materially affects projection, assessment, recommendation, authority, or action.

---

## Boundary model

### Filesystem measurement

A filesystem measurement reports values such as:

```text
free bytes
total bytes
mountpoint
device
fstype
```

It answers:

```text
What did this source report about this mounted filesystem path at observation time?
```

It does not by itself answer:

```text
Who owns this storage?
Is this a physical disk?
Is this a network mount?
Is this a bind mount?
Is this a retired-node compatibility path?
Is this the canonical topology name?
```

### Mountpoint

A mountpoint is a path where a filesystem is visible to a host or scrape target.

It is not the same as storage ownership.

Examples:

```text
/
/mnt/sda1
/mnt/example_host_205/sda1
/mnt/example_host_e/sda1
/mnt/merged
```

These paths may represent:

- local root filesystem
- locally mounted physical disk
- remote mount
- bind mount
- mergerfs union
- compatibility alias
- retained retired-node topology path
- operator convention

### Backing device

The `device` dimension may identify a backing source, but it is not sufficient alone.

Depending on source and fstype, `device` may represent:

- block device
- network export
- merger/union source
- bind source
- pseudo filesystem
- mount label
- remote path

### Physical storage ownership

Physical ownership is a stronger claim.

It should require stronger evidence such as:

```text
local block-device observation
stable disk identifier
host-local sysfs/procfs topology
operator assertion
inventory topology
fstab/mount source interpretation
corroborated remote export mapping
```

Prometheus filesystem metrics do not establish physical ownership by themselves.

### Cluster topology

Cluster topology describes how hosts, mounts, exports, unions, mirrors, and compatibility paths relate.

It may include historical or retained naming that is operationally valid but semantically misleading if interpreted literally.

### Retired-node topology path

A path such as:

```text
/mnt/example_host_e/sda1
```

may not mean example_host_e currently owns or serves that storage.

It may mean:

```text
legacy path retained for compatibility
```

or:

```text
historical node name still encoded in mount topology
```

or:

```text
cluster convention that survived node retirement
```

Seed must not infer current host ownership from path text alone.

---

## Relationship to Prometheus cleanup

The recent Prometheus cleanup sequence narrowed high-risk relationship and fact-promotion collapses:

```text
prometheus_instance → alias_of
Prometheus endpoint_role → provides
Prometheus prometheus_instance → monitored_by prometheus
Prometheus node_uname_info os → host:port fact
```

The remaining filesystem issue differs.

Prometheus filesystem metrics are useful observations and should generally remain evidence.

The problem is projection and interpretation:

```text
endpoint/scrape-target filesystem measurement
        ↓
flat state-summary filesystem list
        ↓
reader may infer host storage ownership
```

The next boundary is therefore not simply acquisition or fact promotion.

It is:

```text
measurement scope
        +
projection semantics
        +
operator clarification
```

---

## What Seed currently risks collapsing

### Collapse 1: mounted path as owned storage

Current output can make this look true:

```text
192.168.254.101:9100 /mnt/example_host_205/sda1
        means
example_host_101 owns example_host_205 storage
```

But the safer interpretation is:

```text
example_host_101's node-exporter endpoint reported a mounted filesystem at /mnt/example_host_205/sda1
```

### Collapse 2: host-local visibility as physical ownership

A host can see a mount without owning the underlying physical storage.

Cross mounts, network mounts, bind mounts, and union mounts all break the direct inference:

```text
visible on host
        !=
physically owned by host
```

### Collapse 3: path name as topology truth

A path containing `example_host_e` does not prove current example_host_e ownership or liveness.

Path names may be conventions, aliases, compatibility shims, or historical artifacts.

### Collapse 4: duplicate path visibility as duplicate storage

The same backing storage may be visible through multiple mountpoints.

Example possibility:

```text
/mnt/sda1
/mnt/example_host_e/sda1
```

may be:

```text
two paths to related or same storage
```

not:

```text
two independent disks
```

### Collapse 5: ambiguous topology as graph error

Ambiguity is not always graph invalidity.

If evidence supports multiple interpretations, Seed should preserve ambiguity and ask when needed.

### Collapse 6: ambiguity as contradiction

A topology anomaly is not a contradiction unless two claims cannot both be true.

For example:

```text
example_host_e is retired
```

and:

```text
path /mnt/example_host_e/sda1 exists on example_host
```

can both be true.

The correct interpretation may be:

```text
retired-node path retained as compatibility topology
```

---

## Operator clarification boundary

Seed should ask the operator when all of these conditions hold:

```text
1. Evidence supports multiple materially different interpretations.
2. The interpretations affect ownership, authority, action, recommendation, or important projection.
3. Existing evidence is insufficient to select one interpretation safely.
4. A mistaken interpretation would create misleading topology, unsafe action, or bad advice.
```

Seed should not ask merely because something looks unusual.

Seed should not ask for every mountpoint.

Seed should not ask when the ambiguity does not affect any current decision, projection, or recommendation.

### Example ask-worthy ambiguity

```text
example_host reports /mnt/sda1
example_host reports /mnt/example_host_e/sda1
example_host_e appears retired
mount sizes or devices suggest overlap
```

Potential interpretations:

```text
local disk
remote mount
bind mount
compatibility alias
retired-node historical path
mirror path
cluster convention
```

This is ask-worthy because it affects:

- storage ownership
- capacity projection
- backup safety
- repair recommendation
- retired-node reasoning
- host topology
- filesystem display summarization

### Example not ask-worthy ambiguity

```text
example_host_101 reports /run/user/1000
```

Unless it affects an active question or recommendation, this can remain a low-value measurement or be hidden from summary projection.

---

## Question form

Seed should ask specific topology questions, not vague questions.

Bad:

```text
This filesystem looks weird. What is it?
```

Better:

```text
I observed example_host reporting both /mnt/sda1 and /mnt/example_host_e/sda1.
Do these refer to the same backing storage, a compatibility mount, a remote mount, or two separate filesystems?
```

Better:

```text
I observed example_host_101 reporting /mnt/example_host_205/sda1.
Should paths under /mnt/node*/sda1 be treated as remote/cross-mounted storage rather than local physical ownership?
```

Better:

```text
I observed mount paths referring to retired node names.
Are those retained compatibility paths, or should Seed treat them as stale topology that needs cleanup?
```

The answer should become operator-provided evidence, not hidden model memory.

---

## What operator answers should support

Operator clarification should be representable as evidence supporting scoped claims such as:

```text
path pattern /mnt/node*/sda1 usually denotes cluster cross-mount
```

```text
/mnt/example_host_e/sda1 on example_host is a compatibility alias
```

```text
example_host_e is retired, but the path name remains for compatibility
```

```text
/mnt/merged is a union/mergerfs view, not physical storage ownership
```

```text
/mnt/sda1 is the local canonical mount for this host's current storage role
```

These are not all the same claim type.

Some are path-convention claims.

Some are topology claims.

Some are historical claims.

Some are current-state claims.

Some are operator-policy claims about projection and display.

---

## Projection implications

The state summary should avoid flatly presenting all filesystem measurements as equal top-level filesystems.

A better projection boundary would distinguish:

```text
local root / local host filesystems
cluster cross-mounts
union/merged views
remote or imported filesystems
pseudo/runtime mounts
ambiguous topology requiring clarification
```

This does not require deleting measurements.

It requires selecting what belongs in the high-level summary and what belongs in a detailed filesystem measurement view.

The current `filesystems:` block is too broad because it exposes every observed mount measurement without topology classification.

---

## Potential source evidence needed

To reduce ambiguity without asking too often, Seed may need to observe more than Prometheus filesystem metrics.

Candidate evidence sources:

```text
/proc/mounts
/etc/fstab
findmnt-style mount source data, if available safely
local block devices
filesystem type
mount options
mergerfs configuration
NFS/SSHFS/CIFS/export metadata
operator-provided cluster path conventions
retired-node inventory/status
```

Some of this already exists in local observation surfaces.

The key is not merely acquisition.

The key is preserving enough evidence to classify topology safely or ask when classification remains ambiguous.

---

## Contradiction boundary

A storage topology discrepancy should become a contradiction only when Seed has two or more claims that cannot all be true.

Examples of possible contradiction:

```text
Claim A: /mnt/example_host_e/sda1 is physically owned by active example_host_e.
Claim B: example_host_e is retired and no longer owns storage.
Claim C: /mnt/example_host_e/sda1 is served by example_host local disk.
```

These may conflict depending on claim scope and time.

But this is not contradiction:

```text
example_host_e is retired
/mnt/example_host_e/sda1 still exists as a compatibility path
```

Those can both be true.

Therefore Seed needs:

```text
ambiguity before contradiction
```

and:

```text
operator clarification before unsafe promotion
```

when ownership or topology meaning matters.

---

## Goal boundary

Properly mapping drives is a valid Seed goal when it affects outcomes.

It matters because storage topology affects:

- backup planning
- repair recommendations
- disk replacement reasoning
- data safety assessment
- cluster capacity projection
- retired-node cleanup
- mount health interpretation
- host ownership inference
- action authorization

But the goal is not:

```text
make topology aesthetically clean
```

The goal is:

```text
make topology explainable enough that Seed avoids bad claims and bad recommendations
```

A weird but intentional topology is acceptable if Seed understands its meaning.

---

## Required architectural invariants

This audit supports the following invariants:

```text
Mount visibility is not storage ownership.
Path name is not topology authority.
Retired-node name in a path is not contradiction by default.
Filesystem measurement is not physical disk identity.
Prometheus filesystem metric is endpoint/scrape-target evidence.
Ambiguity is not contradiction.
Operator clarification is evidence.
Seed should ask when ambiguity affects ownership, authority, action, recommendation, or important projection.
Projection should not turn unclassified measurements into implied ownership.
```

---

## Recommended next safe move

Do not immediately redesign storage topology.

First audit the current state-summary filesystem projection path.

Determine:

```text
Where does seedstate choose the filesystems block?
What predicates feed it?
Does it distinguish local, remote, union, pseudo, and ambiguous mounts?
Does it suppress low-value runtime mounts?
Does it represent ambiguous topology as a question or issue?
```

Expected next audit target:

```text
state summary filesystem projection boundary
```

not Prometheus acquisition.

---

## Rejected solutions

Rejected for the next step:

1. **Delete Prometheus filesystem measurements.** They are useful evidence.
2. **Treat all `/mnt/node*/sda1` paths as remote mounts.** That may be true locally but needs evidence or operator policy.
3. **Treat all mountpoints as physical disks.** This is the current dangerous simplification.
4. **Treat retired-node path names as errors.** Compatibility paths may be intentional.
5. **Ask the operator about every mountpoint.** That would create operator-question spam.
6. **Hide all filesystem measurements.** Projection should be selective, not blind.
7. **Invent ownership from path text.** Path text is evidence, not authority.
8. **Force contradiction where ambiguity is sufficient.** Contradiction requires incompatible claims.

---

## Direct answers

### Is the weird hard-drive arrangement a contradiction?

Not by default.

It is ambiguity or topology anomaly until Seed has incompatible claims.

### Should Seed ask about it?

Yes, when the ambiguity affects storage ownership, backup safety, repair recommendations, capacity projection, retired-node status, or state-summary interpretation.

### Is mapping drives properly a worthwhile goal?

Yes.

Not for cosmetic cleanliness, but because wrong storage topology produces wrong recommendations and unsafe conclusions.

### What should Seed ask?

Seed should ask targeted questions such as:

```text
Should /mnt/node*/sda1 paths be treated as cluster cross-mounts rather than local physical storage?
```

or:

```text
Does /mnt/example_host_e/sda1 remain as a compatibility path even though example_host_e is retired?
```

### Where should the next implementation attention go?

State-summary filesystem projection.

The immediate issue is that the summary displays all filesystem measurements as a flat top-level list without topology classification.

---

## Required report

### Files changed

- `docs/storage_topology_ambiguity_and_operator_clarification_reconciliation.md`

### LOC changed

- Documentation-only new file.

### Major findings

- Weird storage topology is ambiguity, not contradiction by default.
- Mount visibility does not imply physical storage ownership.
- Path names such as `/mnt/example_host_e/sda1` are not topology authority.
- Operator clarification is appropriate when ambiguity affects ownership, authority, recommendation, action, or important projection.
- State-summary filesystem projection is now the next likely boundary to audit.

### Recommended next audit

Audit the state-summary filesystem projection path to determine how `seedstate` selects and displays filesystem measurements and whether it can distinguish local, remote, union, pseudo, ambiguous, and operator-classified mounts.

### Documents intentionally left unchanged

- `docs/prometheus_boundary_cleanup_status_reconciliation.md`
- `docs/prometheus_host_endpoint_fact_attachment_audit.md`
- `docs/prometheus_acquisition_interpretation_routing_promotion_audit.md`
- All runtime implementation files.
- All tests.
- All schema, ontology, predicate, relationship, projection, and authority definitions.
