# Knowledge Acquisition Status

Seed's local knowledge acquisition grows by narrow observation slices. Each slice
follows the Capability Extension Methodology: capability gap → question →
evidence → fact → projection. This board is documentation-only; it does not add
runtime behavior, execution behavior, provider integration, network access, DNS
queries, shell execution, subprocess execution, sudo requirements, or LLM
reasoning.

## Implemented

| Item | Status | Class | Tier | Risk | Next Slice |
| --- | --- | --- | --- | --- | --- |
| Identity Observation | Implemented | Identity | Foundation | Low | Track local identity disagreements without DNS or ownership claims. |
| Mount Observation | Implemented | Topology; Configuration | Local observation v1 | Low | Consider `/proc/self/mountinfo` only if a later slice needs richer relationships. |
| Kernel / CPU / Memory Observation | Implemented | Description | Local observation v1 | Low | Keep memory available/free out until volatile state semantics need it. |
| Local Network Observation | Implemented | Configuration; Topology; State | Local observation v1 | Low | Preserve configuration facts as non-reachability evidence. |
| Storage Topology Observation | Implemented | Topology; Description | Tier 3 host topology | Medium | Keep storage topology before packages/systemd; do not infer health or manage devices. |
| Listening Port Observation | Implemented | Topology | Tier 3 host topology | Medium | Keep listener topology distinct from service/process ownership and endpoint health. |
| Local Host Observation | Implemented | Description; State | Foundation | Low | Continue keeping local descriptive facts separate from health, reachability, and supportability inference. |
| Availability Vocabulary | Implemented | Cross-cutting vocabulary | Vocabulary | Low | Keep availability separate from local observation facts. |
| Explainability Foundation | Implemented | Cross-cutting explanation | Foundation | Low | Continue exposing evidence and non-inference boundaries in new slices. |
| Capability Verification Foundation | Implemented | Cross-cutting verification | Foundation | Low | Keep verification facts distinct from provider reports and observations. |

## In Progress

| Item | Status | Class | Tier | Risk | Next Slice |
| --- | --- | --- | --- | --- | --- |
| Local Knowledge Status Visibility | In Progress | Cross-cutting documentation | Documentation | Low | Keep this board updated when observation slices land. |

## Planned

| Item | Status | Class | Tier | Risk | Next Slice |
| --- | --- | --- | --- | --- | --- |
| Users Observation | Planned | Configuration; Identity | Local observation v1 | Medium | Prefer `/etc/passwd`; avoid NSS/network-backed lookups. |
| Groups Observation | Planned | Configuration; Identity | Local observation v1 | Medium | Prefer `/etc/group`; avoid NSS/network-backed lookups. |
| Package Observation | Planned | Description; Configuration | Local observation v1 | Medium | Parse readable package databases only; do not call package managers. |
| Systemd Observation | Planned | Configuration; State | Local observation v1 | Medium | Inventory unit definitions/read-only state only; no unit actions. |
| Schedule Observation | Planned | Configuration | Local observation v1 | Medium | Read cron/system timer configuration; do not infer job success. |
| Certificate Observation | Planned | Configuration; Description | Local observation v1 | Medium | Parse local certificate stores; do not perform TLS/network validation. |
| Process Marker Observation | Planned | State | Local observation v1 | Medium | Read minimal `/proc/<pid>` markers; avoid sensitive command-line capture. |
| Container Marker Observation | Planned | State; Topology | Local observation v1 | Medium | Read local marker files/cgroups only; do not use Docker sockets. |

## Deferred

| Item | Status | Tier | Risk | Next Slice |
| --- | --- | --- | --- | --- |
| Health inference from local observations | Deferred | Reasoning | High | Requires separate evidence and explicit rules; not part of observation slices. |
| Availability inference from mounts or interfaces | Deferred | Reasoning | High | Keep availability facts sourced from explicit availability evidence only. |
| Reachability inference from identity, network, or mount facts | Deferred | Reasoning | High | Requires probes or external evidence; out of scope for local observation. |
| Provider-backed local inventory enrichment | Deferred | Provider integration | High | Must remain separate from local read-only observation. |
| Prometheus-backed mount/storage health | Deferred | Provider integration | High | Keep Prometheus mappings separate from local mount observation. |
| Remediation, repair, or management actions | Deferred | Execution | High | Requires execution planning and policy; not knowledge acquisition. |

## Listening Port Observation v1

Listening Port Observation v1 is implemented as Tier 3 host topology knowledge. It reads bounded local procfs evidence from `/proc/net/tcp`, `/proc/net/tcp6`, `/proc/net/udp`, and `/proc/net/udp6` to emit `listening_endpoint`, `listening_protocol`, `listening_address`, and `listening_port` facts. TCP rows are projected only for `LISTEN` state; UDP rows describe locally bound UDP endpoints with non-zero local ports. The chosen representation is host-scoped with protocol/address/port/address-family dimensions and compact endpoint values such as `tcp 0.0.0.0:22`, `tcp [::1]:8080`, or `udp 0.0.0.0:53`.

This slice preserves observation != management. It does not run `ss`, `netstat`, `lsof`, `fuser`, shell commands, subprocesses, sudo, network probes, DNS queries, socket opens, provider APIs, Prometheus calls, or LLM reasoning. Listener facts do not infer availability, reachability, external accessibility, endpoint health, service health, process ownership, service ownership, application ownership, responsiveness, active traffic, monitoring status, or management authority. Oversized or possibly truncated procfs socket-table inputs are skipped rather than partially projected. `--current-facts` exposes all listener facts, and `--impact HOST` includes a compact `listening endpoints` section without overloading aliases, availability, local network, mounts, or storage topology. See [Listening Port Observation v1](listening_port_observation.md).

## Storage Topology Observation v1

Storage Topology Observation v1 is implemented as Tier 3 host topology knowledge. It reads bounded local evidence from `/sys/block/*`, `/sys/class/block/*`, and `/proc/partitions` to emit `block_device`, `partition`, `block_device_size_bytes`, `block_device_rotational`, `block_device_removable`, `block_device_model`, `block_device_vendor`, and `block_device_parent` facts. The representation is host-scoped: device names are fact values and dimensions identify the device or child/parent pair. Existing mount facts are correlated only in impact output when `/dev/<observed-storage-name>` matches a mounted device.

This slice preserves observation != management. It does not run `lsblk`, `blkid`, `findmnt`, `udevadm`, `smartctl`, `dmsetup`, `mdadm`, `zpool`, `btrfs`, shell commands, subprocesses, sudo, network probes, DNS, provider APIs, Prometheus calls, or LLM reasoning. Storage facts do not infer availability, reachability, filesystem health, storage health, backup status, redundancy, data safety, safe removal, or performance adequacy. See [Storage Topology Observation v1](storage_topology_observation.md).

## Knowledge Classification Notes

Knowledge classes are defined in [Knowledge Classification Vocabulary](knowledge_classification_vocabulary.md). The class column is documentation-only and does not add projection behavior, freshness logic, scheduling, context composition, runtime behavior, tool execution, provider integration, or LLM reasoning.

For mixed observation slices, the first class listed is the dominant classification used for roadmap explanation. Secondary classes document notable facts emitted or expected from the same slice.
