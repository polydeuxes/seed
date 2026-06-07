# Knowledge Acquisition Status

Seed's local knowledge acquisition grows by narrow observation slices. Each slice
follows the Capability Extension Methodology: capability gap → question →
evidence → fact → projection. This board is documentation-only; it does not add
runtime behavior, execution behavior, provider integration, network access, DNS
queries, shell execution, subprocess execution, sudo requirements, or LLM
reasoning.

## Implemented

| Item | Status | Tier | Risk | Next Slice |
| --- | --- | --- | --- | --- |
| Identity Observation | Implemented | Foundation | Low | Track local identity disagreements without DNS or ownership claims. |
| Mount Observation | Implemented | Local observation v1 | Low | Consider `/proc/self/mountinfo` only if a later slice needs richer relationships. |
| Local Network Observation | Implemented | Local observation v1 | Low | Add listening-port observation from `/proc/net/*` without connection attempts. |
| Local Host Observation | Implemented | Foundation | Low | Add kernel, CPU, and memory facts from bounded local files/APIs. |
| Availability Vocabulary | Implemented | Vocabulary | Low | Keep availability separate from local observation facts. |
| Explainability Foundation | Implemented | Foundation | Low | Continue exposing evidence and non-inference boundaries in new slices. |
| Capability Verification Foundation | Implemented | Foundation | Low | Keep verification facts distinct from provider reports and observations. |

## In Progress

| Item | Status | Tier | Risk | Next Slice |
| --- | --- | --- | --- | --- |
| Local Knowledge Status Visibility | In Progress | Documentation | Low | Keep this board updated when observation slices land. |

## Planned

| Item | Status | Tier | Risk | Next Slice |
| --- | --- | --- | --- | --- |
| Kernel Observation | Planned | Local observation v1 | Low | Read bounded `/proc/sys/kernel/*` values only. |
| CPU Observation | Planned | Local observation v1 | Low | Start with `os.cpu_count()` and conservative `/proc/cpuinfo` fields. |
| Memory Observation | Planned | Local observation v1 | Low | Read `/proc/meminfo`; avoid health or pressure inference. |
| Storage Topology Observation | Planned | Local observation v1 | Medium | Read `/sys/block` and `/proc/partitions`; do not run `lsblk`. |
| Users Observation | Planned | Local observation v1 | Medium | Prefer `/etc/passwd`; avoid NSS/network-backed lookups. |
| Groups Observation | Planned | Local observation v1 | Medium | Prefer `/etc/group`; avoid NSS/network-backed lookups. |
| Listening Port Observation | Planned | Local observation v1 | Medium | Read `/proc/net/tcp*`, `/proc/net/udp*`, and `/proc/net/unix`; never connect. |
| Package Observation | Planned | Local observation v1 | Medium | Parse readable package databases only; do not call package managers. |
| Systemd Observation | Planned | Local observation v1 | Medium | Inventory unit definitions/read-only state only; no unit actions. |
| Schedule Observation | Planned | Local observation v1 | Medium | Read cron/system timer configuration; do not infer job success. |
| Certificate Observation | Planned | Local observation v1 | Medium | Parse local certificate stores; do not perform TLS/network validation. |
| Process Marker Observation | Planned | Local observation v1 | Medium | Read minimal `/proc/<pid>` markers; avoid sensitive command-line capture. |
| Container Marker Observation | Planned | Local observation v1 | Medium | Read local marker files/cgroups only; do not use Docker sockets. |

## Deferred

| Item | Status | Tier | Risk | Next Slice |
| --- | --- | --- | --- | --- |
| Health inference from local observations | Deferred | Reasoning | High | Requires separate evidence and explicit rules; not part of observation slices. |
| Availability inference from mounts or interfaces | Deferred | Reasoning | High | Keep availability facts sourced from explicit availability evidence only. |
| Reachability inference from identity, network, or mount facts | Deferred | Reasoning | High | Requires probes or external evidence; out of scope for local observation. |
| Provider-backed local inventory enrichment | Deferred | Provider integration | High | Must remain separate from local read-only observation. |
| Prometheus-backed mount/storage health | Deferred | Provider integration | High | Keep Prometheus mappings separate from local mount observation. |
| Remediation, repair, or management actions | Deferred | Execution | High | Requires execution planning and policy; not knowledge acquisition. |
