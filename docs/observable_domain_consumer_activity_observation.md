---
doc_type: observation
status: exploratory
domain: observable domain consumer and activity observation
introduced_by: observable domain consumer and activity observation
related:
  - host_observation_reconciliation.md
  - host_observation_composability_audit.md
  - local_observation_roadmap_reconciliation.md
  - view_authority_and_surface_responsibility_reconciliation.md
  - lens_view_reconciliation.md
  - context_composition_reconciliation.md
  - state.md
---

# Observable Domain Consumer And Activity Observation

## Status

Exploratory observation only.

This document records whether repository evidence supports the observation that
Seed and participants may interact with the same bounded observable domains while
differing by consumer and activity.

It does not define a new ontology, runtime concept, lens architecture, view
architecture, orientation architecture, participant architecture, domain
registry, observer registry, implementation plan, or architectural proposal.
Repository authority remains with the cited reconciliation, audit,
implementation, and view documents in their own scopes.

## Question

Candidate observation under review:

```text
Seed and participants may interact with the same bounded observable domains.
The difference is not necessarily the domain.
The difference may be the consumer and activity.
```

Examples under review:

```text
Acquire configuration != Inspect configuration
Acquire listeners     != Inspect listeners
Acquire users/groups  != Inspect users/groups
Acquire systemd state != Inspect systemd state
```

## Repository Evidence Reviewed

Repository evidence inspected for this observation included:

- `docs/host_observation_reconciliation.md`
- `docs/host_observation_composability_audit.md`
- `docs/local_observation_roadmap_reconciliation.md`
- `docs/view_authority_and_surface_responsibility_reconciliation.md`
- `docs/lens_view_reconciliation.md`
- `docs/context_composition_reconciliation.md`
- `docs/state.md`
- `docs/architecture.md`
- `docs/impact_overview_authority_reconciliation.md`
- `seed_runtime/observation_sources.py`
- `seed_runtime/state_summary_views.py`
- `seed_runtime/context_composer.py`

Search terms included:

```text
Host Observation Domains
reader / transport
observation domains
LocalHostObservationSource
SystemdObservationSource
State Views
Context Views
listeners
configuration
users / groups
packages
services
systemd
inspection
inspect
acquire
```

## Observable Domains Currently Described

Repository authority already describes Host Observation as a capability area
composed of multiple observation domains rather than as one monolithic domain.
The described domains include:

```text
identity
platform
resources
network
storage
users / groups
packages
listeners
services
configuration
capabilities
health signals
state signals
relationships to endpoints or services
```

The same reconciliation distinguishes Host Observation from readers,
transports, and observation sources. It classifies SSH, local collector,
Ansible, agent, provider API, and Prometheus-shaped inputs as access paths or
sources that may feed host-domain observers rather than as the host domains
themselves.

This supports the boundary:

```text
reader / transport != observable domain
```

## Implementation Evidence

`LocalHostObservationSource` is implemented as one broad local discovery source
that collects several bounded host-observable areas in sequence. In current code
it collects identity, hosts-file configuration evidence, local observation
status, OS and architecture, disk byte facts, host description, network, mounts,
storage, listeners, local users/groups, packages, and systemd observations.

Some areas are implemented mainly as private methods inside
`LocalHostObservationSource`:

| Area | Implementation evidence | Bundling evidence |
| --- | --- | --- |
| identity | `_collect_local_identity` and `_collect_identity_observations` | Called by `LocalHostObservationSource.collect` before other host observations. |
| hosts-file configuration | `_collect_hosts_file_observations` | Called by `LocalHostObservationSource.collect`; scoped to local `/etc/hosts` configuration evidence. |
| host description/resources | `_collect_host_description_observations` | Called by `LocalHostObservationSource.collect`; uses procfs and CPU/memory evidence. |
| network | `_collect_network_observations` | Called by `LocalHostObservationSource.collect`; includes interfaces, addresses, routes, and resolver configuration. |
| mounts/filesystems | `_collect_mount_observations` | Called by `LocalHostObservationSource.collect`; uses `/proc/mounts`. |
| storage | `_collect_storage_observations` | Called by `LocalHostObservationSource.collect`; uses sysfs/procfs block-device evidence. |
| listeners | `_collect_listener_observations` | Called by `LocalHostObservationSource.collect`; uses procfs socket tables. |
| users/groups | `_collect_local_user_observations` | Called by `LocalHostObservationSource.collect`; uses passwd/group files. |

Other areas show more independent implementation:

| Area | Implementation evidence | Independence evidence |
| --- | --- | --- |
| packages | `LocalHostObservationSource._collect_local_package_observations` delegates parsing and observation emission to `parse_dpkg_status` and `package_records_to_observations` in `seed_runtime.local_packages`. | The local host source orchestrates; package parsing/emission lives in a separate module. |
| systemd services/state | `LocalHostObservationSource._collect_systemd_observations` delegates to `SystemdObservationSource` when no injected source is provided. | `SystemdObservationSource` has its own `collect`, command runner, counters, observation metadata, and unit-state emission. |
| Prometheus endpoint/host-adjacent metrics | `PrometheusObservationSource` is a separate observation source over safe HTTP queries. | It produces endpoint, OS, and filesystem measurement observations from Prometheus while preserving Prometheus provenance and endpoint scope. |

This supports the observation that `LocalHostObservationSource` currently behaves
as a container/orchestrator over multiple bounded host-observable areas, while
not all areas have been split into independently reusable domain observers.

## State Views And Context Views

Repository documents and implementation describe views as consumers of projected
knowledge, not acquisition sources.

State Views are documented as read-only projection views over State. Architecture
documentation says State Views answer what Seed currently knows without reading
raw events directly and that they are projections, not second stores or runtime
actors.

Context View documentation describes Context Views as read-only deterministic
projections from canonical inputs such as projected State, State Views, Evidence
Graph, contradictions, confidence, requirements, capabilities, and current
input. Context Views prepare decision-ready context and do not perform
acquisition, execution, provider calls, mutation, replay, persistence, or truth
selection.

Implementation evidence is consistent with that boundary: `state_summary_views`
organizes projected facts into operator-facing buckets such as hosts, services,
endpoints, storage, capabilities, and requirements, while preserving boundaries
against ownership, topology, and storage-identity overclaim. Context composition
consumes State/View-shaped inputs to produce read-only context packets for later
routing or decision surfaces.

This supports a consumer/activity distinction:

```text
Observation source acquires domain evidence.
State View or Context View consumes projected knowledge originating from domain evidence.
Operator-facing inspection surfaces may inspect or render the same domain area.
```

The repository evidence does not require the domain itself to change when the
consumer changes.

## Supported Observations

Repository evidence supports these observations:

1. Host Observation is already described as a multi-domain capability area, not
   as a single observable domain.
2. Repository authority already separates access paths and sources from host
   observation domains. SSH, local collection, Ansible, agent, provider API, and
   Prometheus-style inputs are not themselves the bounded host domains.
3. Current local host implementation bundles many domains under
   `LocalHostObservationSource.collect`.
4. Some domains have stronger independent implementation evidence than others:
   systemd has a separate observation source; packages have a separate parsing
   and observation-emission module; Prometheus has a separate observation source;
   identity/network/mounts/storage/listeners/users/groups are mostly private
   methods in the local host source.
5. State Views, Context Views, State Summary, and impact-style inspection
   surfaces consume projected knowledge that can originate from the same domain
   evidence collected by observation sources.
6. The same domain label can appear under different activities without changing
   the domain boundary: acquisition of listener evidence, projection of listener
   facts, and inspection of listener-related output remain about listener-domain
   material even though their consumers and purposes differ.
7. Acquisition and inspection are distinct interactions in the repository:
   observation sources collect source-scoped evidence, while views and impact or
   summary surfaces read, select, organize, or render projected knowledge.

## Unsupported Or Insufficiently Supported Observations

Repository evidence does not support these stronger conclusions:

1. It does not support promoting `observable domain`, `consumer`, or `activity`
   into new canonical ontology.
2. It does not support defining a domain registry, observer registry, participant
   registry, lens architecture, view architecture, or orientation architecture.
3. It does not support equating observer, lens, view, and orientation.
4. It does not show that every domain is independently implemented today.
5. It does not show that every participant-facing inspection surface is explicitly
   domain-modeled; some surfaces summarize or bucket projected facts without
   owning full domain semantics.
6. It does not show that acquisition and inspection always share identical
   boundaries. Repository evidence supports overlap and reuse of domain-origin
   material, but preservation of source scope, projection rules, and view
   responsibility still determines what can be claimed.

## Preserved Uncertainty

The evidence is strongest for host observation and local host implementation.
It is weaker for a general cross-Seed participant model because current
repository authority more often describes acquisition sources, projected State,
State Views, Context Views, State Summary, and operator-facing impact surfaces
than a single participant-domain interaction model.

The safest repository-supported wording is therefore:

```text
The same bounded host-observable domain may be involved in multiple activities.
Observation sources acquire source-scoped evidence.
Projection and view surfaces may later consume, organize, summarize, or inspect
knowledge that originated from those domains.
The domain boundary need not change solely because the consumer or activity
changes.
```

This remains an observation, not an architecture proposal.
