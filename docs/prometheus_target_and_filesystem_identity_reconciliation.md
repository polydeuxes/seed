# Prometheus Target And Filesystem Identity Reconciliation

## Purpose

This document reconciles the first large Prometheus ingestion pass against Seed's current read-model and identity boundaries.

The triggering operator output was a Prometheus observation run that ingested hundreds of measurement observations, discovered many scrape targets, and caused State Summary to expand from a compact overview into a long filesystem listing.

The audit is intentionally scoped to semantics and read-model boundaries. It does not propose new probing, storage identity inference, service inference, or filesystem health repair behavior.

---

## Triggering Observations

A Prometheus ingestion run reported:

```text
ingested 955 observation(s)
counts by predicate:
- availability_status: 47
- endpoint_role: 47
- filesystem_avail_bytes: 199
- filesystem_free_bytes: 195
- filesystem_size_bytes: 199
- filesystem_total_bytes: 181
- os: 19
- prometheus_instance: 19
- up: 47
```

The resulting State Summary reported:

```text
entities: 46
facts: 3811
durable facts: 2864
measurement current samples: 947
availability:
  up: 14
  down: 13
  unknown: 19
filesystems:
  ... many host/mountpoint rows ...
```

The operator concern was twofold:

1. `up` was ambiguous: does it refer to a host, service, endpoint, or Prometheus scrape target?
2. filesystem rows flooded State Summary and exposed a deeper identity issue: the same physical or logical storage can appear on multiple hosts, while host-specific attachment health can differ.

---

## Finding 1: Prometheus `up` Is Scrape Target Evidence

Prometheus `up` should not be treated as host availability directly.

The raw Prometheus `up` metric is scoped to a scrape target from Prometheus's vantage point. For example:

```text
192.168.254.115:9100 up
```

means:

```text
Prometheus successfully scraped the target 192.168.254.115:9100.
```

It does not directly prove:

```text
node115 is available
node115 is healthy
node_exporter is globally available
ssh is reachable
all services on node115 are up
```

Prometheus target success is availability evidence, but the scope is endpoint/scrape-target availability.

Recommended conceptual vocabulary:

```text
prometheus_target_up
endpoint_scrape_status
endpoint_availability_status
```

Host availability may later be projected from endpoint evidence, but that must be an explicit rollup/projection, not an implicit interpretation of raw `up`.

---

## Finding 2: Endpoint Availability Is Not Service Availability

The operator noted that service status is tricky. For example, `sshd` may be installed and enabled on many systems, but seeing it as an `up` service would be confusing if the evidence was only indirect.

Seed should preserve these boundaries:

```text
package installed
    != service installed

service installed
    != service enabled

service enabled
    != service running

service running
    != network reachable

network reachable
    != application healthy

Prometheus scrape target up
    != arbitrary service up
```

Prometheus target `up` can support a scoped endpoint claim, such as:

```text
Prometheus scraped node_exporter at 192.168.254.115:9100.
```

It should not automatically emit:

```text
service_up=node_exporter
host_up=node115
ssh_up=node115
```

unless a later projection explicitly owns that derivation and cites the supporting evidence.

---

## Finding 3: Filesystem Metrics Identify Host Mount Observations, Not Physical Disks

Prometheus filesystem metrics commonly include labels such as host/instance, mountpoint, device, and filesystem type.

Those labels primarily support a host-scoped mount or filesystem measurement:

```text
host=node115
mountpoint=/mnt/sda1
filesystem_free_bytes=...
```

They do not automatically identify a physical disk.

A physical or logical storage identity may require stronger evidence, such as:

```text
filesystem UUID
PARTUUID
WWN
serial number
stable device symlink
mount source identity
SnapRAID disk identity
ZFS pool/dataset identity
filesystem label plus corroborating host evidence
```

Until such evidence exists, Seed should treat Prometheus filesystem measurements as:

```text
host-specific filesystem measurement at a mountpoint
```

not:

```text
canonical disk entity measurement
```

---

## Finding 4: Storage Identity And Attachment Status Are Different

The operator noted a real cluster condition: ARM devices sometimes lose attached hard drives and require reboot. A hard drive can be healthy and visible from many nodes while missing or unhealthy on one or two nodes.

That means Seed should distinguish:

```text
Storage identity
    The physical or logical storage object.

Mount instance
    A host-specific attachment/mount of that storage.

Filesystem measurement
    Capacity/free/available bytes observed at a mountpoint.

Attachment status
    Whether a particular host currently sees or uses that storage.
```

A future model may eventually say:

```text
storage X appears mounted on node200, node201, node202
storage X is missing from node214
```

But that requires explicit storage identity evidence and a host-specific attachment model.

Prometheus filesystem bytes alone should not collapse all matching paths into one disk identity.

---

## Finding 5: State Summary Is Again Accepting Drilldown Pressure

State Summary became noisy after Prometheus ingestion because it rendered many filesystem rows inline.

This is the same class of issue previously seen with alias flooding:

```text
repository overview
    overwhelmed by evidence/detail rows
```

State Summary should summarize filesystem measurement coverage, not enumerate every filesystem.

Better overview-level examples:

```text
filesystems:
  measured filesystems: 199
  hosts with filesystem measurements: 19
  low free-space warnings: N
```

or:

```text
storage measurements:
  filesystem samples: 199
  hosts covered: 19
  unavailable/missing: unknown
```

Detailed rows belong in:

```text
Impact <entity>
Impact storage section
Current Facts <entity> filesystem_free_bytes
Fact Support
```

State Summary should remain a repository overview, not a fleet filesystem table.

---

## Boundary Recommendations

### Prometheus Observation

Owns:

```text
scrape target facts
endpoint role facts
current measurement samples
host/mountpoint filesystem measurements
```

Does not own:

```text
host availability rollup
service health inference
physical disk identity inference
storage attachment diagnosis
```

### Availability Projection

May eventually own:

```text
host availability inferred from scoped evidence
endpoint availability summaries
unknown/down/up reconciliation
```

But must preserve evidence scope.

### Storage Identity

Should not be inferred from Prometheus filesystem metrics alone.

A future storage identity audit should precede any implementation that creates storage entities, disk entities, or cross-host storage rollups.

### State Summary

Should summarize filesystem measurement coverage and health signals.

Should not inline all filesystem rows.

---

## Non-Goals

This audit does not propose:

```text
new Prometheus queries
new probing
new service model
new host availability rollup
new storage entity model
new disk identity model
new filesystem health rules
new repair/remediation behavior
```

It also does not decide whether Prometheus `up` predicates should be renamed immediately. It only preserves the semantic boundary that raw Prometheus `up` is scrape-target evidence, not direct host availability.

---

## Implementation Implications

Near-term rendering improvement:

```text
Collapse filesystem rows in State Summary into overview counts.
```

Potential future audits before expansion:

```text
endpoint_availability_rollup_reconciliation.md
storage_identity_reconciliation.md
local_service_observation_vocabulary_audit.md
filesystem_measurement_impact_section_audit.md
```

Prometheus ingestion should remain valuable as measurement pressure, but it should not force premature identity modeling.

---

## Conclusion

Prometheus added useful live measurement evidence, but it exposed two boundary risks:

```text
Prometheus target up
    being mistaken for host/service availability

filesystem mount measurements
    being mistaken for physical storage identity
```

The correct near-term response is not to infer more aggressively. It is to preserve scope:

```text
scrape target evidence stays endpoint-scoped
filesystem bytes stay host/mountpoint-scoped
State Summary stays overview-level
identity rollups wait for stronger evidence
```

This keeps Seed aligned with its evidence-first model while allowing future corroboration sources to strengthen availability, service, and storage conclusions deliberately.
