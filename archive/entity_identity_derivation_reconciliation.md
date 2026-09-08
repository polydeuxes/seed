# Entity Identity Derivation Reconciliation

## Purpose

This document reconciles how Seed should decide whether observations belong to the same entity, should remain separate entities, or should be connected by relationships.

The immediate trigger was the growth of observation diversity. Local host discovery, user observation, package observation, filesystem measurements, Prometheus targets, and future reverse-proxy/service observations all create identity pressure.

The central question is:

```text
When should Seed merge identifiers?
When should Seed create relationships?
When should Seed preserve separate scoped entities?
```

This reconciliation is intentionally about identity derivation. It does not implement a new identity resolver, service model, reverse-proxy model, storage model, or UI surface.

---

## Example Normalization

This document uses normalized Seed-style examples rather than operator-specific topology.

Examples use realistic but generic names:

```text
host115
host116
host200
host201
192.168.1.115
192.168.1.200
prometheus
node-exporter
cadvisor
traefik
vaultwarden
```

The examples preserve the shape of real infrastructure while avoiding environment-specific identifiers.

---

## Core Finding

Identity derivation is not relationship discovery.

Two observations may be related without describing the same entity.

```text
related
    != identical
```

Common examples:

```text
host
    != endpoint

endpoint
    != application

application
    != backend

username
    != cross-host user identity

mountpoint
    != storage identity

package
    != capability

service name
    != service instance
```

Identity merges require strong equivalence evidence. Otherwise Seed should preserve separate entities and connect them with explicit relationships.

---

## Identity Merge vs Relationship

### Identity Merge

An identity merge says two identifiers refer to the same entity.

Valid examples may include:

```text
host115 alias_of 192.168.1.115
host115 alias_of machine-id identity
```

Potentially strong identity evidence includes:

```text
machine_id
explicit operator alias
inventory-declared host identity
stable provider identity
hardware serial
filesystem UUID
container ID
```

### Relationship

A relationship says two entities are connected but not identical.

Valid examples include:

```text
host115 has_endpoint 192.168.1.115:9100
192.168.1.115:9100 endpoint_of host115
192.168.1.115:9100 exposes node-exporter
prometheus scrapes 192.168.1.115:9100
host115 monitored_by prometheus
```

The host and endpoint are related. They are not the same entity.

---

## Identity Strength Hierarchy

Seed should treat identity evidence as having different strengths.

Strong identity evidence:

```text
machine_id
explicit operator alias
inventory-declared host identity
stable provider identity
unique hardware identifier
unique filesystem/storage identifier
unique container identifier
```

Moderate or contextual identity evidence:

```text
hostname observed from local host
IP address observed on an interface
DNS name within a known context
Prometheus target associated with a known host
provider-specific instance reference
```

Weak or non-identity evidence:

```text
host:port endpoint
scrape target label alone
service name
package name
username
mountpoint path
reverse-proxy route name
```

Weak evidence may support relationships or candidate associations. It should not automatically support identity collapse.

---

## Endpoint Identity

A host:port string identifies an endpoint surface, not a host.

Example:

```text
192.168.1.115:9100
```

This may support:

```text
endpoint entity
endpoint role
scrape status
Prometheus target identity
relationship to host115 when host evidence exists
```

It should not by itself support:

```text
host identity
service identity
capability identity
application identity
```

Invariant:

```text
host:port is endpoint identity only
```

If Seed knows `192.168.1.115` belongs to `host115`, then it can relate the endpoint to the host. It should not alias the endpoint to the host.

Bad shape:

```text
host115 alias_of 192.168.1.115:9100
```

Better shape:

```text
host115 has_endpoint 192.168.1.115:9100
192.168.1.115:9100 exposes node-exporter
prometheus scrapes 192.168.1.115:9100
```

---

## Reverse Proxy Invariant

Reverse proxies make the boundary unavoidable.

Consider:

```text
192.168.1.10:443
Host: vault.example
Traefik router: vault-router
Backend container: vaultwarden
Host: host115
```

These are distinct things:

```text
endpoint
    192.168.1.10:443

route/application identity
    vault.example

routing layer
    traefik router

backend service/container
    vaultwarden

host
    host115
```

The endpoint is not the application. The application is not necessarily the backend. The backend is not the host.

Invariant:

```text
ip:port
    != application identity
```

Endpoint reachability proves endpoint reachability. It does not prove backend availability unless request, route, and backend evidence support that conclusion.

Future relationship vocabulary may need to represent:

```text
endpoint_accepts_tls
endpoint_routes_host_header
route_targets_backend
backend_runs_on_host
service_exposes_endpoint
```

These are relationships, not identity merges.

---

## User Identity Example

Local user observation exposed the same boundary.

The same username across hosts does not imply the same account identity:

```text
host115 user_account=user
host116 user_account=user
```

Those may describe two local accounts that happen to share a name. One host can change credentials independently from the other.

Invariant:

```text
same username across hosts
    != same identity
```

Without centralized identity evidence, user observations should remain host-scoped facts rather than global user entities.

---

## Storage Identity Example

Filesystem and mount observations expose the same issue.

The same mountpoint across hosts does not imply the same storage identity:

```text
host200 /mnt/sda1
host201 /mnt/sda1
```

The same underlying storage can also be healthy on many hosts and missing on one host.

Seed should distinguish:

```text
storage identity
mount instance
host attachment status
filesystem measurement
```

Invariant:

```text
same mountpoint
    != same storage identity
```

Physical or logical storage identity requires stronger evidence such as:

```text
UUID
PARTUUID
WWN
serial number
pool/dataset identity
explicit operator declaration
```

---

## Package And Service Example

Package observation creates another identity boundary.

Example:

```text
host115 package_installed=nginx
```

This does not imply:

```text
nginx service is running
nginx endpoint is reachable
nginx is serving traffic
nginx owns port 80
```

Invariant:

```text
package identity
    != service instance identity
```

Package facts should attach to the host. Service, process, endpoint, and capability relationships require their own evidence.

---

## Derivation Rules

### Prefer Relationship Before Merge

When evidence is uncertain:

```text
create relationship or candidate association
    before
create alias/equivalence
```

This avoids premature identity collapse.

### Alias Means Equivalence

`alias_of` must remain reserved for identity equivalence.

Do not use `alias_of` for:

```text
host has endpoint
endpoint exposes service
route targets backend
package relates to service
mountpoint belongs to host
storage attached to host
```

### Facts Attach To The Narrowest Correct Subject

Examples:

```text
host OS
    attaches to host

package installed
    attaches to host

endpoint scrape status
    attaches to endpoint

route rule
    attaches to route/proxy configuration when modeled

backend health
    attaches to backend/service subject when explicitly observed

filesystem measurement
    attaches to host/mountpoint unless storage identity evidence exists
```

If Seed cannot identify the stronger subject, it should not attach the fact to a weaker but convenient subject merely to avoid unknowns.

---

## Read-Model Implications

Entity typing, graph validation, relationships, Impact, and State Summary all depend on identity derivation.

If identity derivation collapses too much:

```text
hosts absorb endpoints
services absorb routes
mounts absorb storage
users become global identities prematurely
packages become capabilities prematurely
```

If identity derivation is too conservative:

```text
known hosts remain unknown
relationships remain sparse
operator navigation weakens
corroboration is harder to see
```

The goal is not maximum merging. The goal is evidence-backed merging.

---

## Implementation Implications

Future implementation work should preserve these behaviors:

```text
Do not alias hostnames to host:port endpoints.
Do not attach host-level OS facts to endpoint subjects.
Do not infer service identity from port alone.
Do not infer application identity from endpoint reachability alone.
Do not create global user entities from same usernames alone.
Do not create storage entities from mountpoint paths alone.
Do not infer capability from package installation alone.
```

Potential future tests:

```text
host:port endpoint remains endpoint-only unless separate host evidence exists
host has_endpoint endpoint does not imply alias_of
reverse proxy endpoint does not imply backend application availability
same username on two hosts remains host-scoped
same mountpoint on two hosts remains host-scoped
package installation does not imply service availability
machine_id can support strong host identity equivalence
explicit operator alias can support identity equivalence
```

---

## Non-Goals

This reconciliation does not implement:

```text
new identity resolver
new entity merge algorithm
new reverse proxy model
new service model
new route model
new storage entity model
new user identity model
new UI surface
```

It preserves the boundary so future implementations can avoid collapsing identity too early.

---

## Architectural Invariants

```text
Related things are not necessarily the same thing.

Identity merges require stronger evidence than relationships.

Alias means equivalence.

If there is doubt, create a relationship before creating an alias.

Facts attach to the narrowest correct subject.

Evidence arrives first.

Relationships connect scoped entities.

Identity merges require strong equivalence evidence.

Rollups happen last.
```

---

## Conclusion

Seed should derive identity from evidence strength rather than convenience.

The safe order is:

```text
Observation
    ↓
Evidence
    ↓
Scoped Fact
    ↓
Relationship
    ↓
Identity Merge
    ↓
Projection / Rollup
```

Preserving this order prevents premature identity collapse while allowing stronger models to emerge as corroborating evidence accumulates.
