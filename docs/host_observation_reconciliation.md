# Host Observation Reconciliation

## Purpose

This document performs a focused architectural reconciliation for Host
Observation after the Host Observation Composability Audit.

The audit established the current local collector as:

```text
Current collector:
    safe

Current collector:
    not yet fully composable
```

and proposed the shape:

```text
Host Observation
    -> Domain Observers
    -> Reader / Transport
```

This reconciliation determines whether that shape is correct, complete, and
consistent with Seed's broader architecture.

This is a documentation-only reconciliation. It does not implement code, modify
schemas, modify collectors, modify SSH behavior, modify Prometheus behavior,
modify observation acquisition, modify runtime behavior, or modify tests.

## Executive Finding

The proposed shape is correct, with one important refinement:

```text
Observation Source
    -> source-specific acquisition / reading
    -> source-specific interpretation
    -> host observation domain observers
    -> candidate claims / relationships
    -> routing
    -> promotion
    -> projections
```

Host Observation is not itself a single source, transport, projection, or truth
system. It is an architectural capability area composed of host-scoped
observation domains that can interpret evidence about host-like entities while
preserving source, reader, vantage point, and provenance.

The target shape should therefore be expressed as:

```text
Host Observation Capability Area
    Host Observation Domains
        identity observer
        platform / OS observer
        resources observer
        network observer
        storage observer
        users / groups observer
        packages observer
        listeners observer
        services observer
        configuration observer
        capabilities observer
        health indicator observer
        state indicator observer
        relationship observer
    Reader / Transport Boundary
        local filesystem reader
        ssh reader
        mounted rootfs reader
        agent payload reader
        provider API reader
        prometheus sample reader / interpreter
    Knowledge Pipeline Boundary
        observations
        evidence
        candidates
        routing
        promotion
        projections
```

This shape preserves the established Seed rule that source-attributed knowledge
must not be collapsed into verification, promotion, projection, or host truth.

## 1. What Host Observation Is

Host Observation is Seed's architectural area for source-attributed reports
about host-like operational substrates.

A host-like substrate is an operating environment or infrastructure substrate
that may have identity, platform, resources, network interfaces, storage,
users, packages, listeners, services, configuration, capabilities, health
signals, state signals, and relationships to endpoints or services.

Host Observation answers questions such as:

```text
What did this source report about this host-like substrate?
From what vantage point?
Through what reader or transport?
At what time?
With what scope and limitations?
What claims could this evidence support without overpromoting it?
```

Host Observation is therefore a source-attributed observation and interpretation
layer. It can produce observations and evidence that may later support candidate
host claims or relationships.

### Host Observation Is Not

Host Observation is not:

- a single collector;
- a shell-command framework;
- SSH behavior;
- Prometheus behavior;
- a projection;
- a verification result;
- a promotion authority;
- a host inventory truth table;
- an endpoint-to-host aliasing mechanism;
- a reason to treat every scrape target as a host;
- a reason to treat every hostname, IP address, or alias as identity equality.

### Relationship To Observation, Evidence, Claims, And Projections

Host Observation sits before durable host-facing claims and before projections.

```text
Observation
    source-attributed report from a vantage point

Evidence
    preserved provenance and support material for considering a claim

Candidate claim / relationship
    interpreted proposition that may be routed or rejected

Promotion
    normalization of an allowed claim into fact / relationship support

Projection
    selected read view over promoted and preserved knowledge
```

Host Observation may emit observations and evidence. It may identify candidate
claims or candidate relationships. It must not itself decide that a host claim
is globally true, verified, promoted, or summary-worthy.

## 2. Is Host Observation A Domain?

Host Observation is best understood as a capability area containing multiple
observation domains.

It is not merely an observation source because sources such as SSH,
Prometheus, local collection, Ansible, provider APIs, remote Seed, and agents
can all contribute host-relevant evidence.

It is not merely one observation domain because identity, platform, resources,
network, storage, users, packages, services, configuration, health, state, and
relationships have different evidence shapes and different non-inferences.

It is not a projection because it precedes summary views and must preserve
provenance even when projections select or hide specific findings.

It is not a capability in the execution sense of "a runnable tool that can do
work now." It is a knowledge capability area: an architectural grouping of
observation domains and adapters that may be invoked by collection capabilities
or sources.

The most precise classification is:

```text
Host Observation = host-scoped observation capability area
                   composed of multiple host observation domains
                   fed by multiple observation sources and readers
                   producing source-scoped observations, evidence,
                   candidates, and relationships for later routing.
```

## 3. What Belongs Under Host Observation

The following candidate domains were evaluated.

| Candidate | Finding | Rationale |
| --- | --- | --- |
| Identity | Belongs; foundational domain | Host-facing claims need stable subject candidates, but identity evidence must remain scoped and non-equivalent by default. |
| Platform / OS | Belongs | OS release, kernel, architecture, distro, virtualization, and runtime substrate are descriptive host observations. |
| Resources | Belongs | CPU, memory, disk capacity, and resource descriptors are host substrate observations when scoped to the observed substrate. |
| Network | Belongs, but with careful scope | Interfaces, addresses, routes, resolver configuration, and local network state can describe a host; reachability and endpoint availability require separate evidence. |
| Storage | Belongs, but may require subdomains | Mounts, filesystems, block devices, and capacity belong, but topology ownership, remote mounts, union views, and retired path names require separate classification before projection. |
| Users / Groups | Belongs | Local account and group observations describe the host substrate; they do not imply active users, access authorization, or identity ownership. |
| Packages | Belongs | Installed package inventories are host observations; they do not imply service exposure, vulnerability, supportability, or runtime use by themselves. |
| Listeners | Belongs, with endpoint boundary | Listening sockets are host observations from a vantage point; exposed endpoints and remote reachability are separate claims. |
| Services | Belongs, but as a separate domain from listeners | Service manager units, process/service descriptions, and service status are host observations; endpoint service identity and external service availability require routing. |
| Configuration | Belongs as one domain among many | Configuration files and settings are host observations when read from a host substrate; configuration must not be treated as the whole of Host Observation. |
| Capabilities | Belongs as observed or inferred support, not execution authority | Capability evidence may describe what a host appears able to do or what Seed can observe, but capability does not equal source, command, or collection performed. |
| Health | Belongs as indicators, not verdicts | Health signals can be observed, but health assessment or verification is a later interpretation layer. |
| State | Belongs as state indicators, not the State projection | Current observed values are host observations; Seed's projected State is a selected view over knowledge. |
| Relationships | Belongs as relationship candidates | `endpoint_of`, `has_endpoint`, `runs_service`, `mounted_from`, or provider relationships may be candidates, but must not collapse into identity aliases without explicit support. |

### Domains Requiring Extra Separation

Some candidates belong only if subdivided or bounded:

- **Storage** should separate measurement, mount description, block-device
  description, topology classification, ownership, and summary selection.
- **Network** should separate local interface/address configuration from remote
  reachability, scrape availability, routing, and service exposure.
- **Services** should separate service manager declarations, running processes,
  listening sockets, externally reachable endpoints, and service identity.
- **Health** should separate observed health indicators from assessment,
  verification, incident state, and recommendation.
- **Relationships** should remain relationship candidates before promotion and
  must not be implemented as alias equality by default.

## 4. Reader / Transport Versus Domain Observer

The separation between Reader / Transport and Domain Observer is
architecturally sound and necessary.

A reader or transport answers:

```text
How can Seed safely access bytes, records, payloads, samples, or API responses
from a particular vantage point?
```

A domain observer answers:

```text
How should source-scoped material in one host domain be interpreted into
observations, evidence, and candidate claims without overclaiming?
```

### Reader / Transport Examples

```text
local filesystem
ssh file or command reader
mounted rootfs
agent payload
provider API
prometheus HTTP API / sample stream
remote Seed export
Ansible fact payload
```

These are not themselves host knowledge domains. They are access paths,
vantage points, serialization forms, or acquisition mechanisms.

### Domain Observer Examples

```text
identity observer
platform observer
storage observer
network observer
user/group observer
package observer
listener observer
service observer
configuration observer
health indicator observer
relationship observer
```

Domain observers may be reused across readers when the evidence shape is
compatible. For example, an identity observer may interpret `/etc/hostname`
from a local filesystem reader, an SSH reader, or a mounted-rootfs reader while
preserving distinct provenance.

### Boundary Rule

```text
Reader != Observer
Transport != Interpretation
Acquisition != Promotion
```

This avoids parallel semantics such as a "local OS fact" meaning something
different from an "SSH OS fact" solely because the bytes arrived through a
different transport.

## 5. Observation Source Versus Observation Domain

Recent reconciliations established the knowledge flow:

```text
Observation Source
    ↓
Interpretation
    ↓
Candidates
    ↓
Routing
    ↓
Promotion
```

Host Observation fits inside this flow as a domain-oriented interpretation area
that can be fed by multiple observation sources.

| Example | Classification | Host Observation Role |
| --- | --- | --- |
| Prometheus | Observation source and sample acquisition path | May provide endpoint evidence and, in narrower cases, host evidence through metric families and labels. |
| SSH | Reader / transport, and possibly a collection capability | Can feed host domain observers but is not Host Observation itself. |
| Local collector | Observation source / orchestrator | Currently collects many host domains safely, but is not the domain model itself. |
| Ansible | Observation source / payload source | May feed host domain observers from fact payloads while preserving Ansible provenance. |
| Remote Seed | Federated observation source | May contribute host observations and promoted claims from another Seed without collapsing provenance. |
| Agent | Observation source and payload transport | May provide host-domain payloads from an agent vantage point. |
| Provider API | Observation source | May provide inventory, identity, resource, relationship, or lifecycle evidence that needs domain routing. |

Therefore:

```text
Prometheus != Host Observation
SSH != Host Observation
Local Collector != Host Observation
Ansible != Host Observation
```

They are sources, readers, transports, or orchestrators that may feed Host
Observation domains.

## 6. Host Observation And Identity

Host Identity Observation is foundational.

Recent State Summary audits showed a useful symptom:

```text
hosts:
    none

services:
    none

endpoints:
    47
```

That output is preferable to unsafe endpoint-to-host promotion, but it exposes a
host identity gap. Seed can see scrape targets, but it does not yet have enough
host-scoped identity evidence to safely populate host-facing summaries.

### Why Identity Matters

Identity matters because many host observations need a subject:

- OS facts should attach to the observed host-like substrate, not accidentally
  to a scrape endpoint.
- Storage measurements should not be treated as host-owned storage without
  subject and topology support.
- Services and listeners need relationships to a host-like substrate without
  implying endpoint identity equality.
- Federated observations need stable enough subject candidates to compare
  evidence across sources without erasing provenance.

### Identity Evidence Examples

Host identity evidence may include:

```text
/etc/hostname
/proc/sys/kernel/hostname
/etc/machine-id
/var/lib/dbus/machine-id
/proc/sys/kernel/random/boot_id
/etc/os-release ID fields, when scoped as platform evidence
kernel uname fields, when scoped as platform evidence
provider instance ID
cloud metadata instance ID
agent-reported host identifier
Ansible machine_id / hostname facts
Prometheus node_uname_info labels, with endpoint scope preserved
DNS name, when source and resolution method are explicit
IP address, when source and interface / endpoint scope are explicit
```

### What Identity Must Not Imply

Identity evidence must not imply by itself:

```text
hostname == globally unique host
ip address == host identity
host:port endpoint == host identity
Prometheus instance label == host identity
machine-id == currently reachable host
boot-id == durable host identity
provider instance ID == operating-system identity
alias == identity equivalence
same name == same entity
same OS evidence == same entity
```

Identity observation should produce scoped candidate identifiers and possible
relationships. It should not automatically promote aliases or merge subjects.

## 7. Host Observation And Configuration

Configuration is one host-observation domain among many.

Configuration Observation was too narrow as the top-level architectural frame
because host understanding also includes identity, platform, resources, network,
storage, users, packages, listeners, services, capabilities, health indicators,
state indicators, and relationships.

Configuration belongs under Host Observation when Seed reads or receives
configuration material from a host-like substrate, such as:

```text
/etc/hostname
/etc/os-release
/etc/fstab
service unit files
package manager configuration
network configuration
application configuration
agent configuration
```

But configuration must not be collapsed into description or truth:

```text
configured != active
configured != reachable
configured != healthy
configured != authorized
configured != owner
configured != service identity
```

A configured listener, mount, route, user, package repository, or service unit
is evidence about declared or observed configuration, not proof that the
corresponding runtime state or external behavior exists.

## 8. Host Observation And Verification

The boundary remains:

```text
Observation != Verification
```

Observation records what a source reported. Verification is a scoped method for
checking a question. Corroboration can increase confidence, but it does not
magically erase scope or provenance.

Example:

```text
Prometheus says Debian
SSH says Debian
/etc/os-release says Debian
```

These should coexist as separate evidence paths:

| Evidence path | Possible interpretation | What it does not prove alone |
| --- | --- | --- |
| Prometheus metric label reports Debian | Endpoint-associated exporter reported OS-like metadata. | The scrape endpoint is the host identity, or the metric is current OS truth for all aliases. |
| SSH read reports Debian | SSH-accessed substrate exposed OS release content. | The SSH target is the same entity as a Prometheus endpoint unless routed by evidence. |
| Local `/etc/os-release` read reports Debian | Local reader observed OS release content. | That other sources refer to the same host, or that Debian is verified under an independent method. |

If routed to the same host candidate, the three observations may corroborate a
host OS claim. If they conflict, they should expose contradiction or ambiguity.
If their subjects cannot be safely related, they should remain separate.

## 9. Host Observation And Federation

Host observations from remote Seed, agents, providers, SSH, and Prometheus
should coexist without collapsing provenance.

Federation requires preserving at least:

```text
origin Seed or system
source type
source name
reader / transport
vantage point
subject as reported by the source
source-local identifiers
observed timestamp
expiration / freshness
collection method constraints
confidence / trust metadata, if present
candidate subject mapping, if any
promotion decision, if any
```

A remote Seed may export already-promoted facts and supporting evidence. A local
Seed receiving them should not treat them as locally observed truth. They are
federated claims with remote provenance and may support, contradict, or remain
parallel to local observations.

Federation should prefer relationships and scoped subject mappings over alias
collapse. For example:

```text
remote_seed host H
agent host UUID A
provider instance I
ssh target 10.0.0.5
prometheus instance 10.0.0.5:9100
```

may eventually relate to the same operational host, but only through explicit
identity and relationship evidence. Until then, each source's subject remains
source-scoped.

## 10. Prometheus Findings

The original concern was Prometheus host information.

Prometheus contributes valuable evidence, but Prometheus scrape semantics make
subject routing especially important. The `instance` label is commonly a scrape
target identifier, often shaped like `host:port`. That shape is endpoint-facing
by default and must not be treated as host identity merely because metric names
contain host-like words.

### When Prometheus Contributes Endpoint Evidence

Prometheus contributes endpoint evidence when observations are about scrape
targets, exporter availability, metrics exposed by an endpoint, or labels whose
primary subject is the scrape target.

Examples:

```text
up{instance="10.0.0.5:9100"}
scrape duration / scrape samples
endpoint labels attached to a target
node_exporter filesystem metrics attached to instance="host:port"
process-exporter metrics for a scrape endpoint
```

These observations may be accurate and useful while still remaining
endpoint-scoped.

### When Prometheus Contributes Host Evidence

Prometheus can contribute host evidence when metric families report host-domain
attributes and the interpretation preserves endpoint provenance.

Examples may include:

```text
node_uname_info
node_os_info
node_cpu_seconds_total
node_memory_MemTotal_bytes
node_filesystem_size_bytes
node_network_info
```

However, such metrics should initially be treated as host-domain evidence
reported through a Prometheus endpoint, not as automatic host claims.

The evidence shape is therefore:

```text
Prometheus endpoint E reported host-domain attribute A about exporter-observed substrate S.
```

not:

```text
Endpoint E is host S.
```

### What Justifies Promotion Into Host-Facing Claims

Promotion into host-facing claims is justified only when additional support
establishes a host candidate and safe routing.

Supporting evidence could include:

- host identity observations from `/etc/hostname`, machine-id, boot-id, or
  provider metadata;
- explicit exporter metadata that identifies the host substrate separately from
  the scrape endpoint;
- SSH or agent identity evidence matching source-scoped host identifiers;
- provider or inventory relationships connecting endpoint address, instance ID,
  and host substrate;
- stable relationship candidates such as `endpoint_of` or `has_endpoint`;
- freshness and timestamp compatibility;
- non-conflicting OS/platform/resource evidence from independent sources.

Even then, promotion should usually prefer:

```text
endpoint E is an endpoint of host candidate H
Prometheus observation supports host-domain claim C about H
```

rather than:

```text
E == H
```

## 11. What Must Not Be Collapsed

The following architectural invariants should hold:

```text
Tool != Observation Adapter
Capability != Observation Source
Reader != Observer
Transport != Interpretation
Observation Source != Observation Domain
Observation != Evidence
Observation != Verification
Observation != Promotion
Observation != Projection
Observation != Host Truth
Evidence != Truth
Corroboration != Verification
Candidate != Promoted Fact
Promotion != Projection
Projection != Inventory Truth
Host != Endpoint
Endpoint != Service
Host != Provider Instance
Host != Agent
Identity != Alias
Alias != Equality
Hostname != Host Identity
IP Address != Host Identity
Prometheus instance != Host Identity by default
Configuration != Description
Configuration != Runtime State
Health != State
Health Indicator != Health Verdict
State Indicator != State Projection
Listener != Reachability
Listener != Service Identity
Package Installed != Service Running
Filesystem Measurement != Storage Ownership
Mount Path != Storage Topology
Remote Observation != Local Observation
Federated Fact != Local Truth
```

These invariants are not implementation details. They are architectural safety
rules that prevent source-specific observations from becoming unsupported host
truth.

## 12. Non-Goals

This reconciliation does not recommend or perform:

- rewriting the local collector;
- adding host observation schemas;
- modifying observation acquisition;
- changing SSH behavior;
- changing Prometheus behavior;
- changing collectors;
- changing projections;
- modifying tests;
- adding aliases;
- promoting endpoints into hosts;
- adding provider, agent, or federation code;
- implementing domain observers;
- changing runtime behavior.

## 13. Implementation Implications

No implementation work is directly required by this reconciliation.

If future implementation is pursued, the findings imply constraints rather than
a mandate:

1. Any future extraction should start with a narrow domain observer, preferably
   Host Identity Observation, only when there is a concrete implementation need.
2. Domain observers should preserve current local collector behavior unless a
   separate behavior-changing task authorizes otherwise.
3. Readers and transports should expose bounded read primitives or payloads;
   they should not own host-domain semantics.
4. Prometheus host-like metrics should remain endpoint-provenanced until routing
   has explicit host identity or relationship support.
5. Federation should preserve remote provenance and avoid local truth collapse.
6. Projections should communicate uncertainty or absence rather than filling
   empty host buckets by endpoint aliasing.

## Final Architectural Shape

The reconciled architecture is:

```text
Observation Sources
    local collector
    ssh collection
    prometheus
    ansible
    agent
    provider API
    remote Seed
        ↓
Reader / Transport Boundary
    local filesystem
    ssh reader
    mounted rootfs
    payload reader
    HTTP/API reader
        ↓
Host Observation Domains
    identity
    platform / OS
    resources
    network
    storage
    users / groups
    packages
    listeners
    services
    configuration
    capabilities
    health indicators
    state indicators
    relationships
        ↓
Source-Scoped Observations And Evidence
        ↓
Candidate Claims And Relationships
        ↓
Routing And Promotion
        ↓
Facts, Relationships, Supports
        ↓
Projections / State Summary / Operator Views
```

The Host Observation shape proposed by the audit is therefore correct and
consistent with Seed's architecture when understood as a multi-domain,
source-fed observation capability area with a strict reader/observer boundary
and no authority to collapse observation into verification, promotion, or host
truth.
