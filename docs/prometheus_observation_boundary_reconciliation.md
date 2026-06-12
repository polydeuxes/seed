---
doc_type: reconciliation
status: active
domain: prometheus observation
defines:
  - prometheus instance label
  - scrape target identity
  - endpoint scoped observation
  - prometheus observation boundary
depends_on:
  - entity_identity_derivation_reconciliation.md
  - prometheus_endpoint_identity_boundary_audit.md
  - host_observation_reconciliation.md
related:
  - prometheus_acquisition_interpretation_routing_promotion_audit.md
  - prometheus_boundary_cleanup_status_reconciliation.md
  - prometheus_target_and_filesystem_identity_reconciliation.md
---

# Prometheus Observation Boundary Reconciliation

## Purpose

This document performs a documentation-only reconciliation of Prometheus observation semantics, subject selection, fact attachment, measurement attachment, and relationship emission.

This is a boundary-definition audit. It does not implement code, modify Prometheus ingestion, introduce new predicates, relationships, entity types, projections, schemas, or tests.

The goal is to use the findings from:

```text
entity_identity_derivation_reconciliation.md
prometheus_endpoint_identity_boundary_audit.md
```

to determine the correct ownership boundary for Prometheus-derived observations.

---

## Source Findings Preserved

The prior reconciliations established these constraints:

```text
Prometheus instance labels frequently describe endpoints rather than hosts.

host:port endpoint identity != host identity.

Endpoint reachability != application availability.

Filesystem measurements do not automatically create storage identity.

Alias means equivalence.

Relationships should be preferred over identity collapse when evidence is weak.

Facts should attach to the narrowest correct subject.

Observation source scope must be preserved.
```

This document applies those constraints specifically to Prometheus-derived observations.

---

## Core Finding

Prometheus observation is usually evidence about a scrape target from the monitoring system's point of view.

That target may correspond to a host, exporter, service endpoint, local Prometheus endpoint, container endpoint, reverse-proxy endpoint, or other scrape surface. The `instance` label alone does not decide which of those identities is canonical.

Therefore:

```text
Prometheus instance label
    == contextual scrape-target identifier

Prometheus instance label
    != host identity by default
```

A Prometheus observation may strengthen an already-supported host, endpoint, service, or monitoring-system claim. It should not by itself collapse those identities.

---

## Question 1: What Entity Does A Prometheus `instance` Label Represent?

Representative instance labels include:

```text
192.168.1.115:9100
host115
localhost:9090
```

These values are not all the same kind of identity.

### `192.168.1.115:9100`

A host:port value represents an endpoint surface.

It can support:

```text
endpoint identity
scrape target identity
endpoint reachability evidence
endpoint role evidence when labels or metric family indicate an exporter role
relationship evidence to a host when host evidence exists elsewhere
```

It should not by itself support:

```text
host identity
application identity
capability ownership
storage identity
alias equivalence with a host
```

Boundary:

```text
192.168.1.115:9100
    == endpoint / scrape target subject

192.168.1.115:9100
    != host115
```

### `host115`

A bare hostname-like value is contextual identity evidence.

It may be host identity when corroborated by host-scoped evidence such as local observation, inventory, machine ID, explicit operator alias, provider identity, or another strong host identifier.

Without that corroboration, it remains a contextual scrape-target label.

Boundary:

```text
host115 observed as Prometheus instance
    may name a host
    may name a scrape target
    may be a relabeled endpoint
    may be an operator-friendly label
```

Prometheus alone does not determine which interpretation is correct.

### `localhost:9090`

A localhost host:port value represents an endpoint relative to the Prometheus process or scrape configuration context.

It is especially unsafe as global host identity because `localhost` is context-dependent.

For a Prometheus self-scrape, it may support:

```text
Prometheus monitoring endpoint exists in that scrape context
endpoint role may be prometheus
scrape target is reachable from Prometheus's own vantage point
```

It should not by itself support:

```text
global host identity localhost
application availability beyond the scrape endpoint
monitoring system identity equivalence
```

Boundary:

```text
localhost:9090
    == contextual endpoint in a Prometheus scrape context

localhost:9090
    != universal host identity
```

### Classification

The safest classification for a Prometheus `instance` label is:

```text
contextual scrape-target identifier
```

When the label has host:port shape, it is also endpoint identity.

When the label lacks port shape, it may be a host candidate, but only stronger evidence should promote it to host identity.

---

## Question 2: Which Prometheus Observations Are Endpoint-Scoped?

Endpoint-scoped Prometheus observations are observations whose narrowest correct subject is the scrape target or endpoint surface.

Examples include:

```text
up
scrape status
endpoint_role
prometheus_instance
scrape target labels
scrape duration or scrape health from the target perspective
```

### `up`

The Prometheus `up` metric is endpoint-scoped evidence.

It means Prometheus's scrape attempt for a target succeeded or failed from the Prometheus server's vantage point. It does not mean the host is healthy, the application is available, or the service is semantically working.

Correct subject:

```text
endpoint / scrape target
```

Not by default:

```text
host
application
capability
storage identity
```

Rationale:

```text
Prometheus scrape success proves scrape reachability and exporter response.
It does not prove host availability or application availability.
```

### Scrape Status

Scrape status, scrape success, scrape failure, scrape error, and scrape metadata are endpoint-scoped unless the scrape target is explicitly modeled as something narrower.

Correct subject:

```text
endpoint / scrape target
```

Rationale:

```text
The observation is about the monitoring system's interaction with a scrape surface.
```

### `endpoint_role`

`endpoint_role` is endpoint-scoped.

When Prometheus evidence suggests an endpoint is a node exporter, cAdvisor endpoint, Prometheus self-endpoint, or other scrape role, the role belongs to the endpoint surface unless stronger evidence identifies a service instance subject.

Correct subject:

```text
endpoint
```

Not by default:

```text
host capability ownership
service identity
application identity
```

Rationale:

```text
An endpoint exposing exporter metrics is not the same thing as the host owning a capability.
```

### `prometheus_instance`

A fact preserving the raw Prometheus instance label is endpoint-scoped or source-scoped metadata.

Correct subject:

```text
scrape target / endpoint observation
```

Rationale:

```text
The label records how Prometheus named the target in that source context.
It is not automatically the target's canonical identity.
```

### Monitoring System Scope

Some Prometheus observations are about the monitoring system itself rather than the target.

Examples:

```text
Prometheus server scrape configuration includes target X
Prometheus server scraped target X at time T
Prometheus server observed target X up/down
```

These can justify relationships from the monitoring system to the endpoint, but the target status remains endpoint-scoped.

Boundary:

```text
monitoring system owns the observation context
endpoint owns the scrape-target status
```

---

## Question 3: Which Prometheus Observations Are Host-Scoped?

Host-scoped Prometheus observations are observations whose metric semantics describe the machine or operating-system environment rather than merely the scrape endpoint.

Examples currently observed include:

```text
os
filesystem_size_bytes
filesystem_free_bytes
filesystem_avail_bytes
filesystem_total_bytes
```

### `os`

An OS observation is host-scoped when the subject host is known.

Correct subject when host identity is known:

```text
host
```

Incorrect subject:

```text
host:port endpoint
```

If the only available subject is a Prometheus `instance` label with host:port shape, the OS observation should not cause that endpoint to become a host.

Boundary:

```text
os belongs to host identity
os does not belong to endpoint identity
```

If no host identity has been established, the observation should remain source-scoped or unresolved rather than being attached to the endpoint as a host fact.

### Filesystem Measurements

Filesystem measurements describe host-visible filesystems or mount instances from the exporter subject's perspective.

Examples:

```text
filesystem_size_bytes
filesystem_free_bytes
filesystem_avail_bytes
filesystem_total_bytes
```

Correct subject when host identity and mount dimensions are known:

```text
host + mountpoint/device dimensions
```

Potentially more precise future subject when supported by evidence:

```text
mount instance
```

Not by default:

```text
endpoint
storage identity
shared storage object
capability
```

Rationale:

```text
The measurement is about storage as visible from a host/exporter context.
The same mountpoint path on multiple hosts does not prove the same storage identity.
The same device name can be local, transient, containerized, or host-relative.
```

### Mountpoint Versus Storage Identity

A Prometheus filesystem metric may contain labels such as mountpoint, device, fstype, or job. These labels refine the measurement context, but they do not automatically establish durable storage identity.

Weak or contextual evidence:

```text
mountpoint=/mnt/sda1
device=/dev/sda1
fstype=ext4
instance=192.168.1.115:9100
```

Stronger storage identity evidence would require sources such as:

```text
filesystem UUID
PARTUUID
WWN
serial number
pool/dataset identity
explicit operator declaration
stable provider volume identity
```

Boundary:

```text
filesystem measurement
    attaches to host/mount context when known

filesystem measurement
    does not create storage identity by itself
```

---

## Question 4: What Relationships Should Prometheus Observation Create?

This reconciliation does not redesign vocabulary. It classifies current relationship shapes.

### Semantically Correct Or Directionally Correct Shapes

The following shapes are semantically plausible when supported by evidence and typed subjects:

```text
endpoint provides node-exporter
host monitored_by prometheus
```

However, each has boundary constraints.

#### `endpoint provides node-exporter`

This is directionally close to:

```text
endpoint exposes exporter role/capability-like surface
```

It is acceptable only if the current vocabulary treats `node-exporter` as a capability object and if `provides` is understood as exposure rather than identity.

Risk:

```text
provides can be overread as ownership or host capability ownership.
```

Classification:

```text
semantically plausible but overloaded
```

The relationship should not imply:

```text
host owns node-exporter capability
node-exporter service is healthy
node-exporter package is installed
endpoint is identical to node-exporter
```

#### `host monitored_by prometheus`

This is semantically correct when the subject is truly a host and Prometheus evidence is corroborated enough to say the host is monitored.

Risk:

```text
Prometheus may only scrape one endpoint associated with the host.
Scraping a node-exporter endpoint is evidence toward monitoring the host, but the endpoint relationship is narrower.
```

Classification:

```text
semantically correct when host identity is independently established
potentially overbroad when derived only from instance label
```

The relationship should not be emitted with unknown or endpoint subjects merely to avoid unresolved typing.

### Overloaded Shapes

The following shape is overloaded in current findings:

```text
localhost:9090 provides prometheus
```

Problems:

```text
localhost:9090 is endpoint-scoped.
prometheus may be a monitoring system rather than a capability.
provides may mean exposes, represents, runs, owns, or is.
```

Classification:

```text
overloaded
```

The useful evidence is narrower:

```text
Prometheus has a scrape endpoint at localhost:9090 in that context.
Prometheus may scrape itself.
The endpoint may expose Prometheus metrics.
```

It should not collapse endpoint, monitoring system, and capability identity.

### Identity-Boundary Violating Shapes

The following shape violates the identity boundary:

```text
host alias_of endpoint
```

Example:

```text
host115 alias_of 192.168.1.115:9100
```

Problem:

```text
alias_of means equivalence.
A host is not equivalent to a host:port endpoint.
```

Classification:

```text
identity-boundary violation
```

The safer conceptual shape is a relationship rather than an alias:

```text
host has endpoint
endpoint belongs to or is associated with host
Prometheus scrapes endpoint
```

This document does not require new vocabulary. It only classifies aliasing a host to a host:port endpoint as incorrect.

---

## Question 5: What Should Prometheus Observation NOT Infer?

Prometheus evidence should not infer conclusions whose subject or semantics are broader than the scrape observation supports.

### Host Availability

Do not infer host availability from Prometheus scrape status alone.

A scrape target can be down while the host is up, and a scrape target can be up while the host has degraded functionality.

Requires corroborating evidence such as:

```text
local host observation
ICMP/TCP reachability from relevant vantage points
SSH or agent health
multiple exporter signals
operator declaration
provider instance status
```

### Service Availability

Do not infer service availability from exporter reachability alone.

A node-exporter endpoint being up does not prove nginx, postgres, vaultwarden, or another service is available.

Requires service-specific evidence such as:

```text
service manager state
process observation
socket ownership
HTTP/TCP probe against the service endpoint
application health endpoint
reverse-proxy route evidence
logs or traces
```

### Application Availability

Do not infer application availability from endpoint reachability unless the endpoint is the application endpoint and the probe tests application semantics.

A successful Prometheus scrape proves exporter semantics, not arbitrary backend behavior.

Requires:

```text
application-specific response evidence
route and backend evidence
health-check semantics
request/response evidence from a relevant vantage point
```

### Storage Identity

Do not infer storage identity from filesystem metrics alone.

Prometheus filesystem measurements may identify a host-visible mount or device label, but not durable storage identity.

Requires:

```text
UUID
PARTUUID
WWN
serial number
pool/dataset identity
explicit operator declaration
provider volume identity
```

### Capability Ownership

Do not infer capability ownership from endpoint exposure alone.

An endpoint exposing node-exporter metrics suggests exporter exposure. It does not prove the host owns the capability in the broader architectural sense.

Requires corroborating evidence such as:

```text
package installed
service running
process binary
configuration file
systemd unit
container metadata
operator declaration
```

### Endpoint Ownership

Do not infer endpoint ownership from the instance label alone.

A target can be relabeled, proxied, NATed, containerized, or scraped through `localhost` from a context-specific namespace.

Requires:

```text
host interface/address evidence
socket listener evidence
inventory mapping
service discovery metadata
operator declaration
network topology evidence
```

---

## Question 6: How Should Prometheus Observations Participate In Corroboration?

Prometheus evidence is valuable corroborating evidence when its scope is preserved.

It should strengthen confidence in a scoped claim without becoming identity evidence by itself.

### Node Exporter Example

Possible evidence:

```text
package installed=node-exporter
service running=node-exporter
endpoint exposes node-exporter
prometheus scrape target up
```

These are related but distinct claims.

A safe corroboration chain is:

```text
package installed=node-exporter
    supports host has node-exporter software present

service running=node-exporter
    supports host has node-exporter process/service active

endpoint exposes node-exporter
    supports endpoint presents node-exporter metrics surface

prometheus scrape target up
    supports Prometheus can reach and scrape that endpoint from its vantage point
```

Combined, these can strengthen confidence that a host is being monitored through node-exporter.

They should not collapse into:

```text
host == endpoint
endpoint == service
package == capability ownership
scrape up == host available
```

### Confidence Without Identity Collapse

Prometheus observations should participate in corroboration by adding support to an existing or candidate relationship:

```text
host associated with endpoint
endpoint exposes exporter
monitoring system scrapes endpoint
host monitored_by prometheus
```

The confidence increase should be relationship- or claim-specific.

Boundary:

```text
Prometheus evidence can strengthen confidence in a host-to-endpoint association.
Prometheus evidence alone should not prove host-to-endpoint identity equivalence.
```

### Source Scope Preservation

Prometheus evidence must preserve source scope:

```text
which Prometheus system observed it
which scrape job / target / instance label produced it
when it was observed
from what vantage point it was observed
what labels constrained the observation
```

Without source scope, later reconciliation cannot distinguish:

```text
one Prometheus server's target view
another Prometheus server's target view
self-scrape localhost context
remote endpoint context
relabelled target context
stale target context
```

---

## Endpoint-Scoped Prometheus Evidence

Endpoint-scoped evidence includes:

```text
up
scrape success/failure
scrape status
scrape target labels
prometheus_instance label preservation
endpoint_role
exporter metric surface evidence
scrape duration and scrape health metadata
```

Ownership:

```text
subject = endpoint / scrape target
source context = monitoring system observation
```

Invariants:

```text
Endpoint-scoped facts do not make the endpoint a host.
Endpoint-scoped facts do not prove application availability.
Endpoint-scoped facts do not prove host availability.
Endpoint-scoped facts do not prove capability ownership.
```

---

## Host-Scoped Prometheus Evidence

Host-scoped evidence includes Prometheus-derived observations whose metric semantics describe the host environment and whose host subject is independently established.

Examples:

```text
os
host-level CPU/memory/load metrics when present
host-visible filesystem measurements
host-visible network interface measurements when present
```

Ownership:

```text
subject = host
measurement dimensions = metric-specific labels such as mountpoint/device/interface
source context = Prometheus observation through a scrape endpoint
```

Invariants:

```text
Host-scoped facts require a host subject.
A host:port instance label is not a host subject.
Host facts should not attach to endpoints merely because Prometheus used an endpoint-shaped instance label.
```

---

## Measurement Ownership

Prometheus measurements should attach to the narrowest correct subject with metric dimensions preserved.

### Endpoint Measurements

Endpoint measurements describe the scrape interaction or endpoint surface.

Examples:

```text
up
scrape_duration_seconds
scrape_samples_scraped
scrape error status
```

Subject:

```text
endpoint / scrape target
```

### Host Measurements

Host measurements describe the host environment.

Examples:

```text
os
filesystem_size_bytes
filesystem_free_bytes
filesystem_avail_bytes
filesystem_total_bytes
```

Subject when known:

```text
host
```

Dimensions:

```text
mountpoint
device
fstype
job
instance
source Prometheus
observed_at
```

### Mount And Storage Measurements

Filesystem measurements may eventually belong to a mount-instance subject if that subject exists. Until then, they are host measurements with mount dimensions.

They should not create storage identity.

Boundary:

```text
measurement subject = host or endpoint
measurement dimensions = labels qualifying the observation
storage identity = only when stronger storage evidence exists
```

---

## Relationship Ownership

Prometheus relationship ownership should preserve the difference between:

```text
monitoring system observation
endpoint exposure
host association
identity equivalence
capability ownership
```

### Monitoring System To Endpoint

Prometheus can support a relationship that the monitoring system scrapes or observes an endpoint.

Classification:

```text
semantically correct when endpoint subject exists
```

Ownership:

```text
subject = monitoring system
object = endpoint / scrape target
source = Prometheus scrape configuration or observation
```

### Host To Prometheus Monitoring System

Prometheus can support `host monitored_by prometheus` only when the host subject is independently established and the observed endpoint is associated with that host.

Classification:

```text
semantically correct after host association is supported
not correct from instance label alone
```

Ownership:

```text
subject = host
object = monitoring system
support = endpoint scrape evidence plus host-endpoint association evidence
```

### Endpoint To Exporter Role

Prometheus can support that an endpoint exposes an exporter role, such as node-exporter, when metric names, labels, job names, or scrape configuration support that conclusion.

Classification:

```text
semantically plausible but must not imply host ownership or service availability
```

Ownership:

```text
subject = endpoint
object = exporter role/capability-like object under current vocabulary constraints
```

### Alias Relationships

Prometheus should not create `alias_of` between hosts and endpoints.

Classification:

```text
identity-boundary violation
```

Ownership:

```text
alias_of is reserved for identity equivalence
Prometheus instance labels are not identity-equivalence evidence by default
```

---

## Non-Goals

This reconciliation does not define or require:

```text
new predicates
new relationships
new entity types
new projections
new schemas
new tests
new Prometheus ingestion behavior
new service model
new storage identity model
new endpoint ownership model
new host availability rollup
new application availability rollup
new monitoring topology UI
```

It also does not require renaming existing vocabulary. It classifies current findings so future implementation can avoid crossing identity boundaries.

---

## Implementation Implications

Because this is documentation-only, these are boundary consequences rather than implementation instructions.

Future implementation work should preserve the following implications:

```text
Do not treat Prometheus instance labels as host identity by default.
Do not alias hostnames to host:port endpoints.
Do not attach host facts to endpoint subjects.
Do not attach endpoint scrape facts to host subjects unless explicitly projected as a derived summary.
Do not infer host availability from endpoint reachability.
Do not infer service or application availability from exporter reachability.
Do not create storage identity from filesystem metrics alone.
Do not infer capability ownership from endpoint exposure alone.
Preserve Prometheus source scope on facts and relationships.
Prefer relationships or candidate associations over identity collapse when evidence is weak.
```

A future implementation may directly follow these consequences, but this document does not prescribe a code change.

---

## Architectural Invariants

```text
Prometheus instance labels are contextual scrape-target identifiers.

A host:port instance label is endpoint identity, not host identity.

A bare hostname-like instance label is host-candidate evidence, not host identity by default.

localhost is context-dependent and must not become global host identity.

Endpoint reachability proves endpoint reachability from a monitoring vantage point.

Endpoint reachability does not prove host, service, or application availability.

Host-scoped facts require host subjects.

Endpoint-scoped facts require endpoint subjects.

Filesystem measurements describe host-visible filesystem state unless stronger storage identity evidence exists.

Filesystem measurements do not automatically create storage identity.

Alias means equivalence.

Host-to-endpoint association is a relationship, not an alias.

Exporter exposure is not the same thing as capability ownership.

Prometheus evidence can corroborate relationships without becoming identity evidence.

Facts attach to the narrowest correct subject.

Observation source scope must be preserved.
```

---

## Conclusion

Prometheus observation is high-value evidence, but it is not universal identity evidence.

The safest boundary is:

```text
Prometheus observes scrape targets.
Scrape targets are usually endpoints or contextual identifiers.
Endpoint evidence can corroborate host, service, and monitoring relationships.
Corroboration must not collapse identity boundaries.
```

Prometheus-derived facts and relationships should therefore preserve subject scope, source scope, and measurement scope. Endpoint facts belong to endpoints. Host facts belong to hosts when host identity is independently supported. Filesystem measurements belong to host-visible mount context unless storage identity evidence exists. Relationships should connect weakly supported entities rather than converting them into aliases.
