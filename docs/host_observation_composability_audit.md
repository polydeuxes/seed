# Host Observation Composability Audit

## Purpose

This audit investigates whether Seed's current local host observation tools are
built at the right level of composability for future host observation work.

The immediate question is whether Host Observation should pull from existing
bounded tools/adapters instead of reinventing collection logic, and whether the
current implementation is composable enough to support that direction.

This is a documentation-only implementation audit.

It does not modify code, schemas, tests, observations, collectors, tools,
capabilities, projections, runtime behavior, SSH behavior, Prometheus behavior,
or host access behavior.

## Context

Recent State Summary and Prometheus audits showed that Seed currently understands
scrape targets more clearly than hosts. Endpoint identity is now being preserved
and rendered separately, but host/service/storage buckets remain empty unless
non-endpoint host-scoped evidence exists.

That led to a broader framing:

```text
Host Observation
```

is a better architectural height than:

```text
Configuration Observation
```

because host observation includes configuration, identity, description,
resources, network, storage, services, users, packages, listeners, capabilities,
state, and health-relevant evidence without prematurely collapsing those domains.

## Files Reviewed

- `seed_runtime/observation_sources.py`
- `seed_runtime/capability_inventory.py`
- `docs/state_summary_empty_operator_kind_buckets_audit.md`
- `docs/prometheus_observation_boundary_reconciliation.md`
- `docs/foundational_ontology_reconciliation.md`

## Current Local Host Collector Shape

`LocalHostObservationSource` currently acts as a broad read-only local host
collector.

It collects or orchestrates observations for:

```text
identity
local observation status
os
architecture
disk usage
kernel / CPU / memory description
network
mounts
storage
listeners
local users / groups
packages
```

It intentionally avoids shell execution, subprocess execution, privilege
escalation, and network probing. Its metadata records that local collection is
read-only, local-only, and non-mutating.

This is a strong safety property.

However, the implementation shape is still mostly:

```text
LocalHostObservationSource
    -> many domain-specific private methods
    -> observations
```

rather than:

```text
HostObservationSource
    -> composed domain observation adapters
        -> identity observer
        -> platform observer
        -> resource observer
        -> network observer
        -> storage observer
        -> listener observer
        -> user/group observer
        -> package observer
        -> service observer
        -> config-file observer
```

## Finding 1: The Current Collector Is Safe But Not Fully Composable

The current collector is a useful first implementation because it provides a
single safe local acquisition path and records conservative provenance.

But it is not yet fully composable because the observation domains are mostly
private methods inside one collector class.

That makes reuse harder for future collection paths such as:

```text
local host direct collection
SSH host collection
container-mounted host collection
remote agent collection
Ansible fact collection
Prometheus host-exporter interpretation
SNMP/IPMI/cloud inventory collection
```

Each of those future collection paths may need to produce the same host
observation domains while using different transport or evidence sources.

## Finding 2: Host Observation Should Compose Observation Adapters, Not Shell Tools

The desired architecture is not:

```text
Host Observation runs shell tools directly.
```

The safer architecture is:

```text
Host Observation orchestrates bounded observation adapters.
```

An adapter should have a clear scope:

```text
what it reads
from what vantage point
with what permissions
through what transport
whether it mutates anything
what subject its observations attach to
what claims it is allowed to emit
what claims it must not imply
```

This preserves the established boundary:

```text
Observation != Verification
Observation != Host Truth
Observation != Promotion
```

A shell command, SSH command, Python read, Prometheus scrape, or Ansible module
may be an implementation mechanism beneath an adapter. It should not itself be
the architectural unit of host knowledge.

## Finding 3: Tool, Capability, Adapter, And Observation Source Are Different

The current capability inventory already preserves a useful boundary: capability
verification is read-only over projected facts and evidence and does not execute
tools, call providers, append events, or route runtime behavior.

That boundary should carry into host observation.

Do not collapse:

```text
Tool != Observation Adapter
Capability != Observation Source
Capability Availability != Collection Performed
Adapter Output != Host Truth
Observation Source != Promotion Authority
```

A capability may say that SSH collection is possible.

A command may request SSH collection.

An execution may attempt SSH collection.

A host observation adapter may interpret the returned data into source-scoped
observations.

Promotion may later normalize those observations into claims/facts.

These are separate boundaries.

## Finding 4: Host Observation Needs Domain Modules

Host Observation appears to need domain-level composition.

Potential domains:

```text
host identity
host platform / OS
host kernel / runtime description
host resources
host network
host storage / mounts
host listeners
host users / groups
host packages
host services
host configuration files
host capabilities
host health/state indicators
```

These domains should be reusable across transports.

For example:

```text
Local file reader reads /etc/hostname
SSH file reader reads /etc/hostname
Container-mounted host reader reads /host/etc/hostname
Agent reader reports hostname payload
```

All may feed the same host identity observation domain while preserving distinct
source, transport, vantage point, and trust/provenance.

## Finding 5: Transport Should Be Separated From Domain Interpretation

Future SSH-based host observation should not duplicate all local collector logic
as an unrelated SSH collector.

The better shape is:

```text
transport / reader layer
    local file reader
    ssh file reader
    mounted rootfs reader
    agent payload reader

host observation domain layer
    identity observer
    os/platform observer
    network observer
    storage observer
    users observer
    packages observer

normalization / promotion layer
    observation -> evidence -> candidate claim -> fact/support/projection
```

This allows Seed to compare evidence from different access paths without
collapsing them.

Example:

```text
Prometheus endpoint reports node_os_info
SSH reads /etc/os-release
Local collector reads /etc/os-release
Ansible reports ansible_distribution
```

Those should become separate evidence paths that may support or contradict a
host OS claim depending on scope and provenance.

## Finding 6: The Current Local Collector Is Doing Some Domain Work Internally

The current local collector already separates some conceptual areas with private
methods and question metadata, such as identity questions, mount questions,
storage questions, listener questions, local user questions, and host description
questions.

This is a useful sign.

But those domains are not yet first-class reusable adapters.

The implementation is therefore partway to composability but not at the target
shape.

## Recommended Future Direction

Do not rewrite the local collector immediately into a large abstraction.

Do not build a generic shell-command scraper.

Do not make SSH collection a separate parallel universe with different fact
semantics.

Instead, introduce composability gradually.

Suggested direction:

```text
1. Identify host observation domains currently embedded in LocalHostObservationSource.
2. Extract one small domain adapter first, such as host identity observation.
3. Give it a reader interface that can be backed by local files today and SSH later.
4. Preserve the same Observation outputs and metadata semantics.
5. Add tests proving local behavior remains unchanged.
6. Repeat for OS/platform, resources, network, storage, users/groups, packages, and listeners only when needed.
```

The first extraction should be boring and low risk.

Recommended first domain:

```text
Host Identity Observation
```

because hostname, machine-id, boot-id, and FQDN are central to resolving the
current host/entity gap without crossing endpoint boundaries.

## Boundary-Preserving Target Shape

```text
HostObservationOrchestrator
    receives subject / target / access path
    selects allowed domain observers
    records source and transport metadata
    emits observations

DomainObserver
    reads one bounded domain
    emits source-scoped observations
    does not promote facts
    does not verify truth beyond its evidence scope
    does not execute unrelated work

Reader / Transport
    provides bounded read primitives
    local filesystem
    SSH command/file read
    mounted rootfs
    agent payload
    provider API payload
```

This keeps the architecture aligned with:

```text
Observation Source
    -> Source-Specific Interpretation
    -> Candidate Structures
    -> Routing / Promotion
```

## Suggested Regression Tests For Future Implementation

1. Local host identity observations remain byte-for-byte or semantically
   equivalent after extracting an identity domain observer.
2. The identity observer records source path and transport metadata.
3. The identity observer does not infer host uniqueness from hostname alone.
4. SSH-backed identity collection can reuse the same domain observer with a
   different reader/transport, if implemented later.
5. Prometheus endpoint labels are not promoted into host identity merely because
   host identity observation exists.
6. Host facts remain scoped to the evidence path that produced them.

## Direct Answers

### Are the tools currently built properly?

They are safe enough for the current local-only implementation, but they are not
composable enough for the long-term host observation model.

### Should Host Observation pull from existing tools?

Host Observation should compose bounded observation adapters and readers.

It should not reinvent domain logic for each transport, and it should not treat
raw shell tools as the architectural boundary.

### Is the local collector wrong?

No.

It is a reasonable first implementation, but it has grown into a broad collector
that should eventually be factored into reusable host observation domains.

### What is the next safe implementation step?

Extract or formalize one small host observation domain, preferably host identity,
without changing outputs or behavior.

## Final Finding

Seed's current local host observation path is safe but not yet composable enough
for the architecture now emerging.

Host Observation should become an orchestrated composition of bounded domain
observers over pluggable read/transport mechanisms. This allows local, SSH,
container-mounted, provider, and future agent-based collection paths to produce
comparable host observations without duplicating semantics or collapsing
observation into verification, promotion, capability, or host truth.
