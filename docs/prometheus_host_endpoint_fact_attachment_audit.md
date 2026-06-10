# Prometheus Host And Endpoint Fact Attachment Audit

## Purpose

This document performs a documentation-only audit of the remaining Prometheus host-vs-endpoint fact attachment boundary after the prior Prometheus relationship-projection cleanups.

This is an implementation-boundary audit. It is bound to the current implementation and does not introduce new runtime behavior.

The audit tests whether Prometheus-derived facts preserve this boundary:

```text
scrape target / endpoint evidence
        !=
host-scoped fact attachment
```

The central question is whether Prometheus observations such as `node_uname_info`, filesystem measurements, and `up` still attach facts to the Prometheus `instance` label when that label may be a host:port scrape target.

---

## Scope

In scope:

- Prometheus acquisition through `PrometheusObservationSource`.
- Prometheus metric-family interpretation in `_observations_from_query`.
- Prometheus subject selection from the `instance` label.
- Predicate canonicalization for `up` and filesystem measurements.
- Observation-to-evidence and observation-to-fact ingestion.
- Remaining host-vs-endpoint fact attachment risks after relationship-projection cleanup.
- Comparison against existing Prometheus boundary audits.

Out of scope:

- Relationship projection cleanup already completed for Prometheus-derived `alias_of`, `provides`, and `monitored_by`.
- New endpoint topology vocabulary.
- Candidate subject or candidate relationship architecture.
- Runtime changes.
- Schema changes.
- Test changes.
- Ontology changes.

---

## Non-goals

This audit does not:

- Implement code.
- Modify Prometheus acquisition.
- Modify normalization.
- Modify ingestion.
- Modify projections.
- Modify relationship catalogs.
- Modify predicate catalogs.
- Modify tests.
- Introduce new runtime semantics.
- Redesign Prometheus ingestion.
- Choose final vocabulary for endpoint ownership, scrape-target identity, or monitoring topology.

---

## Files inspected

Implementation files inspected:

- `seed_runtime/observation_sources.py`
- `seed_runtime/observation_normalizers.py`
- `seed_runtime/predicate_normalizers.py`
- `seed_runtime/observations.py`
- `predicate_catalog/core.json`

Prior audit and reconciliation documents inspected:

- `docs/prometheus_acquisition_interpretation_routing_promotion_audit.md`
- `docs/prometheus_observation_boundary_reconciliation.md`
- `docs/prometheus_endpoint_identity_boundary_audit.md`
- `docs/prometheus_target_and_filesystem_identity_reconciliation.md`
- `docs/seed.md`
- `docs/ontology.md`

---

## Current remaining Prometheus fact attachment flow

The remaining fact attachment path is:

```text
Prometheus HTTP API vector sample
        ↓
PrometheusObservationSource._observations_from_query
        ↓
instance = metric["instance"]
        ↓
Observation(subject=instance, predicate=<interpreted predicate>)
        ↓
optional PredicateNormalizer canonical observation
        ↓
ObservationIngestor.ingest
        ↓
Fact(subject_id=observation.subject, predicate=observation.predicate)
```

The key remaining issue is that the first subject selected by acquisition becomes the fact subject.

There is no explicit routing step that decides:

```text
host fact
        vs
endpoint fact
        vs
scrape-target fact
        vs
filesystem measurement scoped to endpoint evidence
```

---

## Post-cleanup status

The prior implementation slices narrowed the most harmful Prometheus relationship projections.

Already cleaned up for Prometheus-derived evidence:

```text
prometheus_instance
        ✕
alias_of

endpoint_role
        ✕
provides

prometheus_instance
        ✕
monitored_by prometheus
```

Those relationship projection issues are no longer the primary remaining Prometheus boundary problem.

The remaining issue is upstream fact attachment:

```text
Prometheus instance label
        ↓
Observation.subject
        ↓
Fact.subject_id
```

When `instance` is host-shaped, this may be a host candidate.

When `instance` is host:port-shaped, this is an endpoint or scrape-target subject.

The implementation does not currently route host-scoped predicates away from endpoint-shaped subjects.

---

## Acquisition findings

### 1. Prometheus acquisition is read-only and allowlisted

`PrometheusObservationSource` performs read-only HTTP GET requests against an allowlist:

```text
up
node_uname_info
node_filesystem_avail_bytes
node_filesystem_size_bytes
```

This remains a good acquisition boundary.

The remaining problem is not unsafe collection.

The problem is subject selection and fact attachment after collection.

### 2. The Prometheus `instance` label is still the dominant fact subject

For every Prometheus vector sample, the implementation requires `metric.instance`.

If `instance` is absent or empty, the sample is skipped.

If present, that value becomes the `Observation.subject` for emitted Prometheus observations.

This means values such as:

```text
192.168.254.115:9100
localhost:9090
node115:9100
node115
```

all enter Seed through the same subject slot.

The implementation does not first classify the `instance` value as:

```text
scrape target
endpoint
host candidate
local Prometheus context endpoint
```

### 3. Metric family interpretation still occurs during acquisition

Acquisition maps metric families into Seed predicates immediately:

```text
up + job label
        ↓
endpoint_role

up
        ↓
up

node_uname_info + sysname
        ↓
os

node_filesystem_avail_bytes
        ↓
filesystem_avail_bytes

node_filesystem_size_bytes
        ↓
filesystem_size_bytes
```

This is interpretation during acquisition, before candidate subject routing exists.

That behavior was already identified by the earlier acquisition/interpretation/routing/promotion audit.

This audit narrows the remaining effect: interpreted predicates are still attached to `instance`.

### 4. `node_uname_info` is treated as stronger host evidence but still uses `instance` as subject

`node_uname_info` receives special handling.

The source copies `instance` and `nodename` into metadata for this metric family.

That metadata supports preserved `prometheus_instance` evidence.

However, when `node_uname_info` emits `os`, the observation still uses:

```text
subject = instance
predicate = os
```

Therefore, if `instance` is `192.168.254.115:9100`, the OS fact attaches to the endpoint-shaped subject rather than to the nodename or a routed host subject.

The presence of `nodename` metadata does not by itself reroute the host-scoped fact.

### 5. Filesystem measurements still use `instance` as subject

Filesystem metrics emit:

```text
subject = instance
predicate = filesystem_avail_bytes
predicate = filesystem_size_bytes
dimensions = mountpoint, device, fstype
```

Predicate normalization then derives:

```text
filesystem_avail_bytes
        ↓
filesystem_free_bytes

filesystem_size_bytes
        ↓
filesystem_total_bytes
```

The dimensions preserve useful measurement identity, but subject routing remains unchanged.

If `instance` is host:port-shaped, filesystem measurements remain attached to the scrape-target / endpoint subject.

### 6. `up` remains endpoint-scoped by subject but canonicalizes to generic availability

The `up` metric emits:

```text
subject = instance
predicate = up
value = 0 or 1
```

Predicate normalization derives:

```text
availability_status = up/down
```

The subject is preserved, which is safer than moving the fact to a host.

However, the canonical predicate name is generic.

The implementation relies on subject shape and later query behavior to preserve endpoint scope rather than representing the metric as an explicitly scrape-target availability claim.

---

## Evidence findings

Prometheus evidence preservation remains useful.

Evidence preserves:

- Observation ID.
- Source type.
- Subject.
- Predicate.
- Value.
- Metadata.
- Dimensions.
- Confidence.
- Observed time.

Prometheus metadata preserves:

- Collector name.
- Source name `prometheus`.
- Prometheus base URL.
- Prometheus metric name.
- Full metric label set.
- Read-only flag.
- HTTP method.
- `instance` and `nodename` for `node_uname_info`.
- Filesystem dimensions for filesystem measurements.

This means the system has enough provenance to audit or later reroute Prometheus-derived facts.

However, evidence does not currently preserve a separate routing decision such as:

```text
this host-scoped predicate was attached to an endpoint subject
because no host subject was selected
```

There is no first-class record distinguishing:

```text
fact promoted on scrape-target subject
```

from:

```text
fact promoted on host subject
```

when both are represented as ordinary facts.

---

## Predicate classification findings

### Host-scoped durable facts

The predicate catalog classifies `os` as a durable fact.

Architecturally, `os` is host-scoped unless explicitly modeled as an operating system reported by a particular endpoint, exporter, or scrape context.

Prometheus currently emits `os` from `node_uname_info` on the `instance` subject.

When `instance` is host:port-shaped, this attaches a host-scoped durable fact to an endpoint-shaped subject.

### Filesystem measurements

The predicate catalog classifies `filesystem_free_bytes` and `filesystem_total_bytes` as measurements.

Measurements are safer than durable identity facts, but they still need correct subject scope.

A filesystem measurement from a node exporter is evidence about a filesystem as reported through a scrape target.

It may support a host filesystem measurement when host identity is routed.

It should not force the scrape target itself to become the host.

### Availability measurements

The predicate catalog classifies `availability_status` as a measurement.

For Prometheus `up`, this is scrape-target availability from the Prometheus server's vantage point.

It should remain endpoint-scoped unless a separate host availability rollup exists.

---

## Boundary findings

### Boundary 1: `instance` is still doing too much work

`instance` currently carries all of these possible meanings:

```text
Prometheus scrape target label
endpoint identity
host candidate
operator-friendly label
Prometheus-local endpoint
fact subject
```

The implementation preserves the label but does not route between these meanings before fact promotion.

### Boundary 2: host-scoped predicates still attach to endpoint-shaped subjects

The clearest remaining case is:

```text
node_uname_info
        ↓
os
        ↓
subject = instance
```

If `instance` has host:port shape, the result is:

```text
192.168.254.115:9100 os linux
```

That fact shape conflicts with the earlier boundary that host facts should attach to host subjects and endpoint facts should attach to endpoint subjects.

### Boundary 3: filesystem measurements are not identity collapse, but still lack host routing

Filesystem metrics currently preserve dimensions and do not create storage identity by themselves.

That is good.

The remaining issue is narrower:

```text
filesystem measurement subject = scrape target
```

This may be acceptable as endpoint-scoped measurement evidence, but it should not be interpreted as host filesystem state without explicit host routing.

### Boundary 4: availability remains endpoint evidence but uses a generic predicate

The `up` metric still correctly begins as endpoint/scrape-target evidence.

The generic `availability_status` canonical predicate can become ambiguous unless endpoint subject scope is preserved by query behavior and projection boundaries.

After the relationship projection cleanups, the remaining risk is not a relationship edge; it is whether consumers treat endpoint availability as host availability.

### Boundary 5: preserved evidence enables cleanup without acquisition loss

Because metadata preserves `metric_labels`, `prometheus_metric`, `source_name`, and dimensions, the implementation can narrow fact attachment later without deleting Prometheus acquisition.

The smallest safe future cleanup should preserve raw Prometheus observations and evidence while limiting or rerouting promoted host-scoped facts.

---

## Remaining collapse points

### Collapse 1: observation subject selection becomes fact subject selection

Current flow:

```text
metric.instance
        ↓
Observation.subject
        ↓
Fact.subject_id
```

There is no separate host-vs-endpoint routing boundary.

### Collapse 2: metric-family interpretation becomes promoted fact

Current flow:

```text
node_uname_info.sysname
        ↓
os observation
        ↓
os fact
```

The interpretation is not preserved as a candidate.

It is promoted as an observed fact on the selected subject.

### Collapse 3: endpoint-shaped subject can carry host-scoped durable fact

Current flow:

```text
instance = host:port
node_uname_info.sysname = linux
        ↓
host:port os linux
```

This is the highest-risk remaining fact attachment issue.

### Collapse 4: scrape-target measurement can be read as host measurement

Current flow:

```text
instance = host:port
filesystem metric
        ↓
host:port filesystem measurement
```

This is less dangerous than `os`, because filesystem metrics are measurements and preserve dimensions, but consumers may still read them as host facts unless query/projection boundaries remain strict.

### Collapse 5: endpoint availability can be read as host availability

Current flow:

```text
Prometheus up
        ↓
availability_status
        ↓
subject = instance
```

This is acceptable only if `instance` remains endpoint-scoped and alias/query paths do not reattach the measurement to host subjects.

---

## Risks

1. **False host typing.** A host:port endpoint can appear to have host-scoped durable facts such as `os`.
2. **Incorrect host state.** Scrape-target facts may be read as facts about the host rather than facts reported through an endpoint.
3. **Ambiguous measurement subjects.** Filesystem measurements preserve dimensions but still attach to a scrape-target subject.
4. **Generic availability semantics.** `availability_status` does not itself say scrape-target availability.
5. **No explicit ambiguity holding area.** Without candidate subjects, Prometheus labels must either be skipped or promoted.
6. **Future projection pressure.** Later projection or query logic may accidentally reintroduce host/endpoint collapse if fact attachment remains ambiguous.

---

## Smallest safe cleanup path

This audit does not implement cleanup, but the smallest safe future path is now narrower than the earlier relationship-projection work.

Recommended next implementation slice:

1. Preserve Prometheus acquisition and evidence.
2. Preserve raw Prometheus-derived observations where useful.
3. Do not attach Prometheus-derived `os` to host:port `instance` subjects as a host-scoped fact.
4. Treat `node_uname_info` on host:port `instance` as evidence for a host candidate or unresolved host-scoped claim, not as an endpoint host fact.
5. Keep filesystem metrics endpoint/scrape-target scoped unless an explicit host subject is routed.
6. Keep `up` / `availability_status` endpoint-scoped.
7. Avoid broad predicate catalog changes; this is source-and-subject-shape-sensitive behavior.
8. Avoid introducing endpoint topology vocabulary during the first cleanup.

The first implementation slice implied by this audit is therefore:

```text
Prometheus node_uname_info + host:port instance
        ✕
host:port os <value>
```

while preserving:

```text
Prometheus node_uname_info evidence
Prometheus metric labels
nodename metadata
prometheus_instance fact preservation
```

---

## Rejected solutions

Rejected for the next cleanup path:

1. **Delete `node_uname_info` ingestion.** Too broad; it carries useful host evidence.
2. **Treat all `node_uname_info` as host-authoritative.** Too broad; `instance` may still be an endpoint label.
3. **Treat all Prometheus facts as endpoint-only forever.** Too strict; bare host labels may be host candidates when corroborated.
4. **Move every Prometheus fact to `nodename`.** Unsafe; nodename is evidence, not automatically canonical host identity.
5. **Create a full candidate-subject system now.** Architecturally likely, but too large for the next safe implementation slice.
6. **Create endpoint topology vocabulary now.** Useful later, but not required to stop host facts on endpoint subjects.
7. **Weaken entity typing or validation.** That would hide the boundary problem rather than preserve it.

---

## Direct answers

### 1. What remaining Prometheus boundary issue is this audit about?

The remaining issue is host-vs-endpoint fact attachment.

The earlier relationship projection collapses have been narrowed for Prometheus-derived evidence.

The current concern is that interpreted Prometheus observations still become facts on the `instance` subject, even when `instance` is host:port-shaped.

### 2. Where is host-vs-endpoint fact attachment decided?

It is mostly decided by acquisition subject selection in `PrometheusObservationSource._observations_from_query`.

The selected `instance` label becomes `Observation.subject`.

`ObservationIngestor.observation_to_fact` then copies `Observation.subject` to `Fact.subject_id`.

### 3. Which Prometheus predicates are most relevant?

Most relevant:

```text
os
filesystem_avail_bytes
filesystem_size_bytes
up
```

Canonicalized forms:

```text
filesystem_free_bytes
filesystem_total_bytes
availability_status
```

### 4. Which predicate is highest risk?

`os` is highest risk because it is a host-scoped durable fact.

When emitted on a host:port subject, it makes the endpoint-shaped subject carry host identity evidence.

### 5. Are filesystem metrics equally risky?

No.

Filesystem metrics are measurements with useful dimensions.

They should remain scoped carefully, but they do not create identity collapse by themselves.

The risk is consumer interpretation: scrape-target filesystem measurements may be read as host filesystem state without explicit routing.

### 6. Is `up` equally risky?

No.

`up` is naturally endpoint-scoped scrape-target evidence.

The risk is only if generic `availability_status` is treated as host availability or is resolved through host aliases.

### 7. Should acquisition be redesigned now?

No.

Acquisition preserves useful provenance and should remain intact.

The smallest next cleanup is to prevent the most clearly host-scoped fact, `os`, from attaching to endpoint-shaped Prometheus `instance` subjects.

### 8. Should `node_uname_info` be removed?

No.

`node_uname_info` is useful evidence.

The issue is direct fact attachment to the wrong subject boundary, not collection.

### 9. Should `os` be moved to `nodename` automatically?

Not globally.

`nodename` may be useful host evidence, but moving `os` to `nodename` would still be a routing decision.

That decision should require explicit host-subject routing or a deliberately scoped narrow rule.

### 10. What is the next safe implementation target?

The next safe implementation target is:

```text
Prometheus node_uname_info
        ↓
os on host:port instance subject
```

Specifically, prevent Prometheus-derived `os` facts from being promoted onto endpoint-shaped `instance` subjects without independent host routing.

---

## Required report

### Files changed

- `docs/prometheus_host_endpoint_fact_attachment_audit.md`

### LOC changed

- Documentation-only new file.

### Major findings

- Prior Prometheus relationship projection collapses are no longer the primary remaining issue.
- Prometheus `instance` remains the dominant observation and fact subject.
- `node_uname_info` still emits `os` on the `instance` subject.
- `os` is the highest-risk remaining fact attachment issue because it is host-scoped.
- Filesystem and availability metrics are lower-risk but still require endpoint/host scoping discipline.
- Evidence preservation is sufficient to support a narrow future cleanup without deleting acquisition.

### Recommended next implementation slice

Prevent Prometheus-derived `os` from attaching to host:port `instance` subjects as a host-scoped fact, while preserving acquisition, metadata, evidence, nodename metadata, and `prometheus_instance` facts.

### Documents intentionally left unchanged

- `docs/prometheus_acquisition_interpretation_routing_promotion_audit.md`
- `docs/prometheus_observation_boundary_reconciliation.md`
- `docs/prometheus_endpoint_identity_boundary_audit.md`
- `docs/prometheus_target_and_filesystem_identity_reconciliation.md`
- All runtime implementation files.
- All tests.
- All schema, ontology, predicate, relationship, projection, and authority definitions.
