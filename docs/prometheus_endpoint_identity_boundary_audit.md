# Prometheus Endpoint Identity Boundary Audit

## Purpose

This document reconciles the relationship and entity-type output produced after Prometheus ingestion.

The triggering observation was that Seed's relationship view became dominated by IP addresses and host:port strings, while entity typing reported ambiguous endpoint/host classifications. The output was not merely noisy; it exposed a structural boundary problem between hosts, endpoints, aliases, capabilities, monitoring systems, and Prometheus scrape targets.

This audit scopes the boundary before implementation changes.

---

## Triggering Output

Representative relationships included:

```text
192.168.254.208:9100 provides node-exporter
192.168.254.101:9200 provides cadvisor
node211 alias_of 192.168.254.211:9100
node211 monitored_by prometheus
node115 alias_of 192.168.254.115:9200
node115 alias_of 192.168.254.115:9100
```

Entity typing showed examples such as:

```text
192.168.254.100:9100: endpoint, host (ambiguous)
  - endpoint: subject looks like host:port
  - host: subject has os
```

Graph issues included:

```text
localhost:9090 provides prometheus
reason: object type is monitoring_system; expected capability
subject types: expected=entity actual=endpoint
object types: expected=capability actual=monitoring_system
```

and warnings such as:

```text
node211 monitored_by prometheus
reason: subject type is unknown; expected host
```

---

## Core Finding

Prometheus ingestion is currently allowing different identity scopes to collapse into the same relationship vocabulary.

The following are distinct concepts:

```text
host
endpoint
service/capability
monitoring system
alias
scrape target
monitored entity
```

They should not all be represented through `alias_of`, `provides`, and host-level facts.

---

## Finding 1: `alias_of` Means Identity Equivalence

`alias_of` should mean two identifiers refer to the same entity.

Examples that may be valid:

```text
node115 alias_of 192.168.254.115
node115 alias_of host machine-id identity
```

Examples that are not valid identity equivalence:

```text
node115 alias_of 192.168.254.115:9100
node115 alias_of 192.168.254.115:9200
```

A host is not the same entity as a host:port endpoint.

Better relationship shape:

```text
node115 has_endpoint 192.168.254.115:9100
node115 has_endpoint 192.168.254.115:9200
```

or equivalently:

```text
192.168.254.115:9100 endpoint_of node115
192.168.254.115:9200 endpoint_of node115
```

This preserves identity while still connecting the host to its observed scrape targets.

---

## Finding 2: Host Facts Must Not Attach To Endpoint Subjects

The entity-type output showed endpoint strings becoming ambiguous because they carried host-level facts:

```text
192.168.254.100:9100
    endpoint because subject looks like host:port
    host because subject has os
```

This suggests Prometheus-derived host facts may be attached to the raw `instance` label, where `instance` is often a host:port scrape target.

Prometheus labels commonly identify scrape endpoints, not necessarily canonical hosts.

Boundary:

```text
endpoint-level facts
    attach to endpoint subject

host-level facts
    attach to host subject
```

Examples:

Endpoint-level:

```text
subject=192.168.254.115:9100
predicate=prometheus_instance
predicate=endpoint_role
predicate=up / scrape status
```

Host-level:

```text
subject=node115 or 192.168.254.115
predicate=os
predicate=filesystem_* measurement when host identity is known
```

If host identity is not known, the observation should either remain endpoint-scoped or use a clearly scoped unresolved host candidate. It should not make the endpoint itself become a host.

---

## Finding 3: `provides` Is Too Broad For Prometheus Exposure

The relationship:

```text
localhost:9090 provides prometheus
```

triggered a graph error because the relationship expects the object to be a capability, while `prometheus` is typed as a monitoring system.

This is a useful validation failure.

It means `provides` is currently being used for more than one semantic purpose:

```text
entity provides capability
endpoint exposes service/application
monitoring endpoint represents monitoring system
```

These are not equivalent.

Potential future relationship vocabulary:

```text
endpoint_exposes
endpoint_for
scraped_by
monitors
has_endpoint
endpoint_of
```

This audit does not choose the final vocabulary. It only rejects using `provides` as the catch-all relationship for endpoint/service/monitoring exposure.

---

## Finding 4: `monitored_by` Requires A Host Or Explicit Monitored-Entity Scope

Warnings such as:

```text
node211 monitored_by prometheus
subject type is unknown; expected host
```

show that relationship validation is doing useful work.

The relationship expects the subject to be a host, but many Prometheus-discovered names do not yet have supported host type derivation.

This can be resolved in two different ways depending on evidence:

1. Add host identity evidence for the subject.
2. Change the relationship to an endpoint-scoped relationship when the subject is actually an endpoint.

Do not silence the warning by weakening validation prematurely.

---

## Recommended Boundary Model

### Host

Represents a machine or host-level entity.

May have:

```text
hostname
machine_id
os
host-level filesystem measurements
host availability projection
```

### Endpoint

Represents a network address plus port.

May have:

```text
address
port
scrape status
endpoint role
Prometheus instance label
```

### Monitoring System

Represents Prometheus or another monitoring system.

May have relationships such as:

```text
monitors host
scrapes endpoint
```

### Capability / Service / Application

Represents provided functionality or software role.

Should not be collapsed with monitoring system identity unless explicitly modeled.

---

## Implementation Implications

Near-term Prometheus ingestion fixes should consider:

```text
1. Stop emitting alias_of between hostnames and host:port endpoints.
2. Emit host-to-endpoint relationships instead.
3. Attach endpoint facts to endpoint subjects.
4. Attach host facts only to host subjects.
5. Avoid making raw Prometheus instance labels both host and endpoint.
6. Avoid using provides for Prometheus monitoring-system exposure unless the object is truly a capability.
```

Potential tests:

```text
node115 is not alias_of 192.168.254.115:9100
192.168.254.115:9100 is typed endpoint only
os facts from Prometheus attach to host subject, not endpoint subject
endpoint_role attaches to endpoint subject
prometheus target up remains endpoint-scoped
localhost:9090 does not provides prometheus as capability
monitored_by validates host subjects only
```

---

## Non-Goals

This audit does not implement:

```text
new service model
new endpoint entity model beyond current typing
new host availability rollup
new port probing
new firewall modeling
new monitoring topology UI
new storage identity model
```

It also does not require renaming every existing predicate immediately. It preserves the semantic boundary needed before Prometheus-derived relationships are expanded.

---

## Conclusion

The relationship output looked ugly because Prometheus ingestion crossed identity boundaries.

The core correction is:

```text
host identity
    != endpoint identity

alias_of
    == identity equivalence

host:port endpoint
    == attachment/reachability surface
```

Seed should connect hosts to endpoints with explicit endpoint relationships, not aliases. Host-level facts should attach to host subjects. Endpoint-level facts should attach to endpoint subjects.

This keeps the graph meaningful as future services, ports, firewall rules, monitoring targets, and storage observations arrive.
