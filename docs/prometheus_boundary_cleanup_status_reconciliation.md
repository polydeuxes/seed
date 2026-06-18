# Prometheus Boundary Cleanup Status Reconciliation

## Purpose

This document performs a documentation-only reconciliation of the Prometheus boundary cleanup sequence after the relationship-projection and host-vs-endpoint fact-attachment fixes.

This is a status and boundary reconciliation. It does not introduce new architecture, runtime behavior, schemas, projections, predicates, relationships, tests, or ontology definitions.

The goal is to preserve what has changed, what boundary is now safer, what remains intentionally unresolved, and what the next frontier should be.

---

## Scope

In scope:

- The completed Prometheus relationship-projection cleanups.
- The completed Prometheus endpoint-shaped `os` fact-promotion cleanup.
- The current preservation boundary between observation/evidence and fact promotion.
- Remaining Prometheus boundary risks after the cleanup sequence.
- Follow-on work selection.

Out of scope:

- Reopening completed Prometheus relationship cleanup work.
- Reopening Prometheus acquisition design.
- Introducing candidate subject or candidate relationship architecture.
- Introducing endpoint ownership, scrape-target, service, or monitoring topology vocabulary.
- Modifying runtime behavior.
- Modifying tests.
- Modifying schemas.
- Modifying ontology.

---

## References reviewed

Architectural documents:

- `docs/prometheus_acquisition_interpretation_routing_promotion_audit.md`
- `docs/prometheus_host_endpoint_fact_attachment_audit.md`
- `docs/prometheus_observation_boundary_reconciliation.md`
- `docs/prometheus_endpoint_identity_boundary_audit.md`
- `docs/prometheus_target_and_filesystem_identity_reconciliation.md`
- `docs/seed.md`
- `docs/ontology.md`

Implementation surfaces reviewed:

- `seed_runtime/observation_sources.py`
- `seed_runtime/observations.py`
- `seed_runtime/observation_normalizers.py`
- `seed_runtime/state.py`
- `relationship_catalog/core.json`
- `predicate_catalog/core.json`

---

## Core finding

The Prometheus cleanup sequence has moved the frontier.

Earlier frontier:

```text
Prometheus observation
        ↓
relationship projection collapse
```

Current frontier:

```text
Prometheus observation / evidence preservation
        ↓
selective fact promotion
        ↓
remaining measurement-scope interpretation
```

The most harmful Prometheus relationship projections have been narrowed for Prometheus-derived evidence.

The highest-risk host-vs-endpoint fact attachment issue, endpoint-shaped Prometheus `node_uname_info → os`, has also been narrowed.

Prometheus acquisition remains intact.

Prometheus observation and evidence preservation remain intact.

The implementation now has an explicit local distinction between:

```text
observation observed
        +
evidence observed
```

and:

```text
fact promoted
```

for the narrow Prometheus endpoint `os` boundary.

---

## Cleanup sequence preserved

### 1. `prometheus_instance → alias_of` narrowed

Prior behavior:

```text
prometheus_instance
        ↓
alias_of
```

Problem:

```text
host-ish nodename
        ==
host:port endpoint
```

was represented through identity-equivalence vocabulary.

Current status:

```text
Prometheus-derived prometheus_instance
        ✕
alias_of
```

Boundary preserved:

```text
host identity
        !=
endpoint identity
```

### 2. Prometheus-derived `endpoint_role → provides` narrowed

Prior behavior:

```text
endpoint_role
        ↓
provides
```

Problem:

```text
endpoint exposure
exporter role
service label
capability identity
monitoring-system identity
```

were collapsed into one relationship.

Current status:

```text
Prometheus-derived endpoint_role
        ✕
provides
```

Non-Prometheus `endpoint_role → provides` remains available where existing behavior expects it.

Boundary preserved:

```text
Prometheus scrape role evidence
        !=
capability ownership
```

### 3. Prometheus-derived `prometheus_instance → monitored_by prometheus` narrowed

Prior behavior:

```text
prometheus_instance
        ↓
monitored_by prometheus
```

Problem:

The relationship implied monitoring topology without an explicit host or monitored-entity routing decision.

Current status:

```text
Prometheus-derived prometheus_instance
        ✕
monitored_by prometheus
```

Non-Prometheus synthetic `prometheus_instance` catalog behavior remains available where tests intentionally preserve it.

Boundary preserved:

```text
scrape-target evidence
        !=
monitored-entity relationship
```

### 4. Prometheus endpoint-shaped `node_uname_info → os` fact promotion narrowed

Prior behavior:

```text
node_uname_info
        ↓
os observation
        ↓
os fact
        ↓
subject = host:port instance
```

Example:

```text
192.0.2.115:9100 os linux
```

Problem:

`os` is host-scoped durable fact information. A host:port subject is endpoint-shaped and should not receive host facts without explicit host routing.

Current status:

```text
Prometheus node_uname_info os observation
        ↓
observation.observed preserved
        ↓
evidence.observed preserved
        ↓
fact promotion suppressed when instance is endpoint-shaped
```

Boundary preserved:

```text
host-scoped durable fact
        !=
endpoint-shaped scrape target subject
```

---

## Implementation boundary now established

The implementation now contains a narrow fact-promotion suppression path.

Current ingestion behavior:

```text
ObservationIngestor.ingest
        ↓
observation_to_evidence
        ↓
_should_suppress_fact_promotion(observation)
        ↓
optional observation_to_fact
```

For the narrow Prometheus endpoint `os` case:

```text
observation.observed
        yes

evidence.observed
        yes

fact.observed
        no
```

The suppression is bounded by all of these conditions:

```text
fact_promotion_suppressed == true
source_name == prometheus
prometheus_metric == node_uname_info
predicate == os
```

This is important because it does not redefine observation, evidence, or fact globally.

It creates a local implementation precedent:

```text
not every preserved observation must become a promoted fact
```

That matches the claim-centric architecture more closely than the earlier unconditional observation-to-fact path.

---

## Acquisition status

Prometheus acquisition remains read-only and allowlisted.

The source still queries:

```text
up
node_uname_info
node_filesystem_avail_bytes
node_filesystem_size_bytes
```

The source still emits observations for:

```text
endpoint_role
up
os
filesystem_avail_bytes
filesystem_size_bytes
```

For endpoint-shaped `node_uname_info → os`, the observation is still emitted, but it carries suppression metadata.

Acquisition was not redesigned.

Collection was not removed.

Prometheus remains a useful observation source.

---

## Evidence status

Evidence preservation remains intact.

For suppressed Prometheus endpoint `os` observations, Seed still records:

- Observation ID.
- Source type.
- Subject.
- Predicate.
- Value.
- Metadata.
- Dimensions.
- Confidence.
- Observed time.

Prometheus metadata remains preserved, including:

- `source_name = prometheus`
- `prometheus_metric = node_uname_info`
- `metric_labels`
- `instance`
- `nodename`, when present
- read-only metadata
- HTTP method metadata

The only intentional metadata addition is the narrow fact-promotion suppression marker and reason.

---

## Current risk profile

### Closed high-risk issues

The following are no longer the active Prometheus frontier for Prometheus-derived evidence:

```text
prometheus_instance → alias_of
Prometheus endpoint_role → provides
Prometheus prometheus_instance → monitored_by prometheus
Prometheus node_uname_info os → host:port fact
```

### Remaining lower-risk issues

Remaining concerns are narrower and mostly measurement-scope oriented:

```text
filesystem measurements on instance
availability_status on instance
```

These are lower risk than the cleaned-up issues because:

- Filesystem values are measurements, not identity-equivalence claims.
- Filesystem dimensions preserve `mountpoint`, `device`, and `fstype`.
- `up` is naturally endpoint-scoped scrape-target evidence.
- Relationship projection no longer turns Prometheus endpoint roles or instance evidence into the most harmful graph edges.

They still require discipline because consumers may read endpoint-scoped measurements as host state if query or projection paths are too broad.

---

## Remaining frontier

The remaining Prometheus frontier is not relationship projection.

It is not immediately another ontology expansion.

The remaining frontier is:

```text
measurement scope
        +
consumer interpretation
```

Specifically:

```text
Prometheus filesystem measurement
        ↓
subject = instance
        ↓
endpoint/scrape-target measurement or host filesystem state?
```

and:

```text
Prometheus up
        ↓
availability_status
        ↓
endpoint availability or host availability?
```

The next work should only proceed if current projections or queries still present these measurements as host state.

If outputs are now clear and endpoint-scoped, no immediate implementation slice is required.

---

## Recommended next safe move

Do not start another implementation cleanup blindly.

First inspect actual projected output after the completed Prometheus cleanup sequence.

Recommended next task:

```text
Run the current Prometheus observation/projection tests or sample projection output and determine whether filesystem measurements or availability_status still appear as host facts rather than endpoint/scrape-target facts.
```

If output is clear:

```text
stop Prometheus cleanup for now
```

If output remains confusing:

```text
audit measurement-scope projection and query behavior
```

not acquisition.

---

## Rejected next moves

Rejected for the immediate next step:

1. **Redesign Prometheus acquisition.** Acquisition remains useful and provenance-preserving.
2. **Introduce endpoint topology vocabulary now.** The highest-risk relationship collapses have already been narrowed without it.
3. **Suppress all Prometheus filesystem facts.** Filesystem measurements are useful and dimensioned.
4. **Suppress all Prometheus availability facts.** `up` is useful endpoint evidence.
5. **Move filesystem or availability facts to nodename automatically.** That would reintroduce host routing without explicit support.
6. **Create a broad candidate system now.** Architecturally plausible, but not required unless projected output still proves ambiguity.
7. **Weaken validation or projections.** That would hide remaining ambiguity rather than preserve it.

---

## Direct answers

### Is the Prometheus relationship-projection cleanup complete?

For the known high-risk Prometheus-derived relationship projections, yes.

The cleaned-up projections are:

```text
prometheus_instance → alias_of
endpoint_role → provides
prometheus_instance → monitored_by prometheus
```

### Is the highest-risk host-vs-endpoint fact attachment cleanup complete?

For the known high-risk case, yes.

The cleaned-up attachment is:

```text
Prometheus node_uname_info os → host:port fact
```

The observation and evidence remain preserved.

Fact promotion is narrowly suppressed.

### Did Prometheus acquisition remain intact?

Yes.

The cleanup sequence preserved read-only Prometheus acquisition and the allowlisted metric collection path.

### Did evidence remain intact?

Yes.

The cleanup sequence preserved observation and evidence recording, including source metadata and Prometheus labels.

### Did Seed learn a useful implementation distinction?

Yes.

The implementation now distinguishes:

```text
preserved observation / evidence
```

from:

```text
promoted fact
```

for at least one explicit boundary case.

### What remains unresolved?

The remaining unresolved Prometheus concerns are measurement-scope and consumer-interpretation issues:

```text
filesystem measurements on instance
availability_status on instance
```

They are lower risk than the previous identity, relationship, and host-fact attachment collapses.

### Should another cleanup begin immediately?

Not automatically.

The next safe move is to inspect projected output. If filesystem and availability values remain endpoint-scoped and understandable, Prometheus cleanup can pause.

---

## Required report

### Files changed

- `docs/prometheus_boundary_cleanup_status_reconciliation.md`

### LOC changed

- Documentation-only new file.

### Major findings

- The known high-risk Prometheus relationship projection collapses have been narrowed.
- The known high-risk Prometheus host-vs-endpoint fact attachment issue has been narrowed.
- Prometheus acquisition and evidence preservation remain intact.
- The implementation now supports preserving observation/evidence without always promoting a fact.
- Remaining Prometheus concerns are lower-risk measurement-scope and consumer-interpretation issues.

### Recommended next action

Inspect current Prometheus projection output before starting another implementation slice.

Only audit or implement further if filesystem measurements or availability status are still presented as host facts rather than endpoint/scrape-target facts.

### Documents intentionally left unchanged

- `docs/prometheus_acquisition_interpretation_routing_promotion_audit.md`
- `docs/prometheus_host_endpoint_fact_attachment_audit.md`
- `docs/prometheus_observation_boundary_reconciliation.md`
- `docs/prometheus_endpoint_identity_boundary_audit.md`
- `docs/prometheus_target_and_filesystem_identity_reconciliation.md`
- All runtime implementation files.
- All tests.
- All schema, ontology, predicate, relationship, projection, and authority definitions.
