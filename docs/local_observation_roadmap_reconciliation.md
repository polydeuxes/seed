# Executive Summary

This reconciliation keeps Seed's next phase focused on **Knowledge Acquisition**, not Reasoning Expansion or execution. The existing local observation roadmap is directionally correct, but its ordering should change to make machine-descriptive knowledge precede implementation-detail inventories.

Recommended ordering changes:

- Move **Storage Topology Observation** ahead of **Packages Observation** and **Systemd Unit Observation**.
- Move **Listening Port Observation** ahead of **Packages Observation** and **Systemd Unit Observation**.
- Introduce a small **Hostname / Identity Observation v1** before **Mount Observation v1**, if implementation is chosen, because Seed already uses a hostname-shaped subject but does not yet model host identity as first-class observed facts.

The recommended near-term order is therefore:

1. Hostname / Identity Observation v1
2. Mount Observation v1
3. Kernel / CPU / Memory Observation v1
4. Users / Groups Observation v1
5. Storage Topology Observation v1
6. Listening Port Observation v1
7. Packages Observation v1
8. Systemd Unit Observation v1
9. Local Schedule Observation v1
10. Certificate Observation v1
11. Process / Container Marker Observation v1

This document is documentation-only. It does not add runtime behavior, `ToolExecutor` behavior, `EventLedger` ownership changes, `ProjectionStore` ownership changes, execution behavior, network probes, subprocess execution, shell execution, sudo requirements, provider integrations, Prometheus integration, or LLM reasoning.

# Roadmap Ordering Review

The Local Observation Roadmap Audit proposed this implementation order:

1. Mount Observation
2. Kernel / CPU / Memory Observation
3. Users / Groups Observation
4. Storage Topology Observation
5. Packages Observation
6. Systemd Unit Observation
7. Listening Port Observation
8. Local Schedule Observation
9. Certificate Observation
10. Process / Container Marker Observation

The ordering should change modestly.

## Finding

**Storage Topology** and **Listening Ports** should move ahead of **Packages** and **Systemd Unit Files**.

## Rationale

Storage topology and listening sockets describe the machine's exposed shape:

- what block devices, filesystems, and storage relationships are locally visible;
- what local kernel socket table entries are in a listening state;
- what host-local topology exists before Seed reasons about the software that may have produced it.

Packages and systemd unit files are still useful, but they are implementation-detail inventories:

- a package's presence does not prove ownership, configuration, service existence, or active use;
- a systemd unit file's presence does not prove service health, user intent, or control authority;
- both can tempt Seed toward package management or service management if boundaries are not explicit.

This follows Seed's architecture principle of inventory before inference and keeps the first operational observations centered on host facts rather than management surfaces.

## Revised relative order

The revised relative order is:

1. Foundational host identity and platform knowledge
2. Mounts
3. Kernel / CPU / Memory
4. Users / Groups
5. Storage Topology
6. Listening Ports
7. Packages
8. Systemd Units
9. Schedules
10. Certificates
11. Process / Container Markers

# Host Identity Observation Audit

Seed has a partial, implicit machine identity concept today, but not a first-class host identity observation model.

## Identity facts that already exist

Current identity-adjacent facts and metadata include:

- `LocalHostObservationSource` selects `platform.node()` as the observation subject, falling back to `localhost`.
- The local source can place `os.uname().nodename` in observation metadata when available.
- Ansible inventory ingestion can emit hostnames, aliases, `ansible_host`, IP addresses, and groups from inventory content.
- Prometheus normalization and endpoint identity logic can relate endpoint-shaped subjects, instances, hostnames, aliases, and provider instances.
- Local network observation can emit configured local interface facts and IP addresses scoped to the local hostname subject.
- `local_observation_status = observed` records that Seed inspected the local machine through read-only local APIs.

These are useful, but they are not a durable first-class model of machine identity. Hostname is currently used primarily as a subject key and sometimes as metadata, not as a directly observed identity fact with explicit source boundaries.

## Identity facts that are missing

Seed does not currently expose dedicated local identity facts for:

- configured static hostname from `/etc/hostname`;
- kernel runtime hostname from `/proc/sys/kernel/hostname`;
- Python/platform node name as an identity observation distinct from subject selection;
- `/etc/machine-id` as a machine identity fact;
- `/proc/sys/kernel/random/boot_id` as a boot-session identity fact;
- FQDN or local host naming relationships, with explicit caveats about DNS and resolver behavior;
- identity source disagreement, such as `/etc/hostname` differing from kernel hostname;
- whether an observed identifier is stable across boot, stable across reinstall, or boot-scoped only.

## Source review

Potential low-risk identity sources are:

| Source | Candidate fact | Scope | Boundary |
| --- | --- | --- | --- |
| `/etc/hostname` | configured hostname | local file configuration | Does not prove DNS, reachability, or current kernel hostname. |
| `/proc/sys/kernel/hostname` | kernel hostname | runtime kernel local state | Does not prove FQDN or inventory identity. |
| `/etc/machine-id` | machine ID | local machine identity file | Does not prove ownership, uniqueness across cloned images, or provider identity. |
| `/proc/sys/kernel/random/boot_id` | boot ID | current boot session | Boot-scoped only; changes across reboot. |
| `platform.node()` | platform node name | Python/platform view | Subject-selection aid; source semantics vary by OS. |

## Capability Extension Methodology assessment

Hostname / Identity Observation v1 is **High Value / Low Risk** under the Capability Extension Methodology when limited to local read-only facts from bounded files and standard-library APIs.

It is high value because identity becomes the anchor for later host knowledge, alias reconciliation, evidence explanation, and contradiction handling. It is low risk because it can be implemented without root, execution, network access, provider calls, mutation, subprocesses, shell commands, or reachability checks.

If implemented, v1 should stay narrow:

- read bounded local files only;
- emit identity facts only;
- include source path metadata;
- treat missing or unreadable files as absence of observation, not failure requiring privilege escalation;
- avoid DNS lookups, reverse lookups, `hostname` subprocesses, `systemd-hostnamed`, cloud metadata, provider IDs, or FQDN reachability claims.

## Hostname / Identity Observation v1 Implementation

Hostname / Identity Observation v1 is the first implementation after this
reconciliation. It enriches the local knowledge model through the existing
`Observation -> Evidence -> Fact -> Projection` path only. It does not change
Runtime behavior, `ToolExecutor`, orchestration, provider integration, network
probing, shell execution, subprocess execution, privilege requirements, or LLM
reasoning.

| Identity fact | Question answered | Evidence source | Fact produced | Non-inferences |
| --- | --- | --- | --- | --- |
| `hostname` | What hostname is configured locally? | `/etc/hostname`, with `/proc/sys/kernel/hostname` as local fallback when the static file is absent | `hostname` | Hostname does not imply DNS validity, DNS success, reachability, availability, provider visibility, ownership, or uniqueness. |
| `machine_id` | What machine-id is recorded locally? | `/etc/machine-id` | `machine_id` | Machine ID does not guarantee global uniqueness, host ownership, provider identity, reachability, availability, or stable identity across cloned images. |
| `boot_id` | What boot-id is recorded for the current local boot? | `/proc/sys/kernel/random/boot_id` | `boot_id` | Boot ID is boot-scoped and does not imply availability, uptime health, reachability, or host uniqueness across boots. |
| `fqdn` | What fully qualified hostname is explicitly configured locally? | A dotted value from `/etc/hostname` or `/proc/sys/kernel/hostname` only | `fqdn` | FQDN does not imply DNS validity, resolver success, reachability, availability, or provider visibility. Seed does not synthesize or query FQDNs. |

FQDN remains absent unless a bounded local hostname source itself contains a
qualified name. Seed does not call DNS, reverse DNS, `socket.getfqdn()`,
`hostname`, `systemd-hostnamed`, cloud metadata, providers, or network services
to fill this fact.

Impact output renders identity in a dedicated `identity:` section. Identity
facts are not aliases, are not availability facts, and do not create inferred
relationships. `--current-facts` continues to expose the raw projected identity
facts alongside all other facts.

# Observation Tiering

Final tier classification:

## Tier 1 — Foundational Host Knowledge

These facts describe the basic local host substrate and should come first.
Identity now leads this tier because future filesystem, memory, interface,
provider, and multi-host facts need an explicit local host anchor.

- Hostname / Identity Observation
- Mount Observation
- Kernel Observation
- CPU Observation
- Memory Observation

## Tier 2 — Identity Expansion

These facts expand the observed local machine and boot-session identity without
implying provider identity, ownership, availability, DNS correctness, or
reachability.

- FQDN when explicitly configured in a bounded local source
- Machine ID
- Boot ID
- Identity relationships when directly observed from local configuration

## Tier 3 — Host Topology

These facts describe local topology or exposure without implying health, successful I/O, remote reachability, or service availability.

- Storage Topology
- Listening Ports

## Tier 4 — System Description

These facts describe installed or declared system implementation details without implying use, ownership, health, or control authority.

- Packages
- Systemd Units

## Tier 5 — Operational Metadata

These facts describe operational configuration or metadata that may affect behavior but must remain separate from execution, validation, renewal, or scheduling.

- Local Schedules
- Certificates

## Tier 6 — Operational State

These facts are closest to live activity and therefore need the strongest guardrails to avoid becoming management, orchestration, or monitoring.

- Process Markers
- Container Markers

# Capability Extension Fit Review

Every roadmap item should be evaluated against these criteria:

- read-only;
- non-root;
- local-only;
- narrow facts;
- evidence-backed;
- no execution;
- no network;
- no provider dependency.

| Roadmap item | Fit | Validation |
| --- | --- | --- |
| Hostname / Identity | Excellent Fit | Bounded local files and platform APIs can provide narrow identity facts. No root, execution, network, provider dependency, or mutation required. |
| Mounts | Excellent Fit | `/proc/self/mountinfo` or `/proc/mounts` can provide local mounted filesystem facts. Evidence can cite source file and parsed fields. |
| Kernel / CPU / Memory | Excellent Fit | `/proc` and platform APIs can provide narrow local facts without root or execution. Avoid performance, health, or capacity conclusions beyond direct values. |
| Users / Groups | Good Fit | Local account databases are usually readable without root. Must avoid authentication, login, permission testing, or directory-provider expansion. |
| Storage Topology | Good Fit | `/sys` and `/proc` can describe local block topology, but parsers must avoid destructive assumptions, device probing, SMART checks, mount attempts, or privilege escalation. |
| Listening Ports | Good Fit | `/proc/net/*` can expose socket table facts without connecting to ports. Must avoid reachability, service identity, health, and PID attribution unless directly available and permission-safe. |
| Packages | Good Fit | File-backed package DB parsing can be read-only and local. Fit varies by package manager and parser maturity. Must avoid package-manager commands. |
| Systemd Units | Good Fit | Unit files can be inventoried from local directories. Read-only DBus state may be acceptable only if it remains read-only and policy-dependent. Must avoid `systemctl` actions and health claims. |
| Local Schedules | Good Fit | Cron and timer definitions can be read from local files where permission allows. Must avoid running jobs, predicting execution success, or taking scheduler ownership. |
| Certificates | Good Fit | Local certificate files can be parsed for metadata. Must avoid remote TLS handshakes, renewal, trust decisions, or network validation. |
| Process Markers | Good Fit with strict guardrails | `/proc` can expose live process metadata, but this is operational state. Must avoid signaling, killing, restarting, supervision, command execution, or policy enforcement. |
| Container Markers | Good Fit with strict guardrails | Local markers may identify container context or runtime artifacts. Must avoid Docker/containerd/CRI control APIs, orchestration, lifecycle management, or provider integration. |

No current roadmap item is a poor fit if constrained to local read-only facts. The highest drift risk items are Systemd Units, Listening Ports, Process Markers, and Container Markers because they sit near management or availability concepts.

# Observation Risk Analysis

Seed should explicitly guard against observation drifting into execution, orchestration, or management.

## Systemd risk

Risk: Systemd observation can drift into service management.

Examples of prohibited drift:

- calling `systemctl start`, `stop`, `restart`, `enable`, `disable`, or `daemon-reload`;
- treating a unit file as proof that a service is healthy or should be running;
- using systemd as an orchestration or policy enforcement layer;
- changing unit files or drop-ins.

Guardrails:

- Observe unit definitions and, if later approved, read-only state only.
- Do not execute `systemctl`.
- Do not mutate unit state.
- Do not infer availability from unit presence.
- Do not infer operator intent from unit presence.

## Listening port risk

Risk: Listening-port observation can drift into network probing or service availability checks.

Examples of prohibited drift:

- connecting to local or remote sockets;
- scanning ports;
- inferring service health or external reachability;
- assuming a listening bind address is reachable from another host;
- mapping a port to an owning service unless directly observed and permission-safe.

Guardrails:

- Parse local kernel socket tables only.
- Record protocol, local address, and port as local facts.
- Do not open sockets.
- Do not claim reachability or availability.
- Treat PID/process attribution as optional and bounded.

## Process risk

Risk: Process observation can drift into process management.

Examples of prohibited drift:

- killing, signaling, restarting, pausing, or supervising processes;
- treating process presence as service health;
- collecting unbounded command-line secrets or environment variables;
- using process data to trigger automatic action.

Guardrails:

- Prefer marker-level process facts over broad process inventory.
- Avoid sensitive fields unless a narrow fact requires them and redaction is defined.
- Do not signal or manage processes.
- Do not infer availability from process presence.

## Container risk

Risk: Container observation can drift into container orchestration.

Examples of prohibited drift:

- invoking Docker, containerd, Podman, CRI, Kubernetes, or provider control APIs;
- starting, stopping, pulling, pruning, restarting, execing into, or inspecting containers through management APIs;
- treating container markers as workload health;
- assigning ownership or desired state to Seed.

Guardrails:

- Observe only local marker files, cgroup clues, namespace clues, or other read-only local evidence.
- Do not call runtime CLIs or daemon APIs.
- Do not manage container lifecycle.
- Do not infer orchestration intent.

## Package risk

Risk: Package observation can drift into package management or ownership claims.

Examples of prohibited drift:

- invoking `apt`, `dpkg`, `rpm`, `yum`, `dnf`, `apk`, `pip`, or equivalent commands;
- installing, upgrading, removing, repairing, or verifying packages;
- treating package presence as proof that Seed owns the software;
- treating package presence as proof that a service is configured or active.

Guardrails:

- Parse read-only database files only.
- Emit package identity/version facts only.
- Do not manage packages.
- Do not infer service or application ownership.

## Storage risk

Risk: Storage topology observation can drift into storage management.

Examples of prohibited drift:

- mounting, unmounting, formatting, resizing, repairing, or probing devices;
- invoking `lsblk`, `blkid`, `mount`, `findmnt`, LVM, ZFS, or RAID commands;
- treating visible topology as healthy topology;
- asserting data durability or writeability.

Guardrails:

- Read `/proc` and `/sys` only.
- Emit topology and relationship facts only.
- Do not perform I/O probes.
- Do not mutate storage.

# Identity Observation Recommendation

**Recommendation:** Introduce **Hostname / Identity Observation v1** before **Mount Observation v1**.

## Rationale

Identity should precede mount observation because later local facts need a stable evidence anchor. Seed already uses `platform.node()` as the local observation subject. Making identity explicit before adding more host-local domains will make subsequent observations easier to explain and reconcile.

Identity v1 is also the smallest safe extension candidate:

- it can use bounded local files and standard-library APIs;
- it requires no root, subprocesses, shell, provider calls, network access, or mutation;
- it improves explanation and alias reasoning without adding inference or execution;
- it can represent source disagreement without resolving it by mutation.

If implementation begins after this document, prefer this sequence:

1. Hostname / Identity Observation v1
2. Mount Observation v1
3. Kernel / CPU / Memory Observation v1

This sequence keeps early work focused on host identity and foundational host knowledge before moving into operational observations.

# Future Observation Invariants

The existing invariants already state that observation must not imply execution, observation must not imply availability, write access must not be required for observation, and read-only observation must remain separate from mutation, provider calls, and registered-operation execution.

The following future invariants should be considered as documentation or executable architecture checks when the related observations are implemented:

- Observing a hostname does not imply DNS correctness, FQDN validity, provider identity, or reachability.
- Observing a machine ID does not imply ownership, uniqueness across cloned images, or provider identity.
- Observing a boot ID does not imply host availability beyond the observed local read event.
- Observing a mount does not imply filesystem health, writeability, sufficient capacity, remote-share reachability, or data durability.
- Observing storage topology does not imply storage health, performance, redundancy, or safety to modify.
- Observing a user or group does not imply authentication success, authorization intent, login activity, or account ownership by Seed.
- Observing a package does not imply ownership, service existence, vulnerability status, or permission to install, upgrade, or remove software.
- Observing a systemd unit does not imply control, desired state, service health, or permission to start, stop, enable, or disable it.
- Observing a listening port does not imply remote reachability, protocol correctness, service health, or endpoint availability.
- Observing a schedule does not imply job success, scheduling ownership, or permission to run or edit the job.
- Observing a certificate does not imply trust, active use, remote TLS validity, renewal authority, or endpoint availability.
- Observing a process does not imply managing, supervising, signaling, restarting, or trusting that process.
- Observing a container marker does not imply managing, orchestrating, entering, restarting, or owning that container.

These invariants should remain non-behavioral unless and until the corresponding observations are implemented and tests can enforce their boundaries.

# Recommended Roadmap

The reconciled Knowledge Acquisition roadmap is:

| Order | Item | Tier | Fit | Notes |
| --- | --- | --- | --- | --- |
| 1 | Hostname / Identity Observation v1 | Tier 2 — Identity Knowledge | Excellent Fit | Add first-class host identity facts before expanding host-local observations. |
| 2 | Mount Observation v1 | Tier 1 — Foundational Host Knowledge | Excellent Fit | Parse local mount facts; no health, writeability, or reachability claims. |
| 3 | Kernel / CPU / Memory Observation v1 | Tier 1 — Foundational Host Knowledge | Excellent Fit | Refine platform facts and local resource shape from read-only sources. |
| 4 | Users / Groups Observation v1 | Tier 4 — System Description | Good Fit | Read local identity databases only; no auth or permission checks. |
| 5 | Storage Topology Observation v1 | Tier 3 — Host Topology | Good Fit | Moved before packages/systemd; local topology only. |
| 6 | Listening Port Observation v1 | Tier 3 — Host Topology | Good Fit | Moved before packages/systemd; local socket table only, no probes. |
| 7 | Packages Observation v1 | Tier 4 — System Description | Good Fit | Read-only DB parsing only; no package-manager commands. |
| 8 | Systemd Unit Observation v1 | Tier 4 — System Description | Good Fit | Unit definitions first; no service management. |
| 9 | Local Schedule Observation v1 | Tier 5 — Operational Metadata | Good Fit | Definitions only; no running or editing jobs. |
| 10 | Certificate Observation v1 | Tier 5 — Operational Metadata | Good Fit | Local certificate metadata only; no remote handshakes or renewal. |
| 11 | Process / Container Marker Observation v1 | Tier 6 — Operational State | Good Fit with strict guardrails | Marker-level facts only; no management or orchestration. |

Although identity knowledge is Tier 2 rather than Tier 1, it should be implemented first because it strengthens the subject and evidence boundary for all subsequent local host observations.

# Non-Goals

This reconciliation does not propose or implement:

- Runtime behavior changes;
- `ToolExecutor` behavior changes;
- `EventLedger` ownership changes;
- `ProjectionStore` ownership changes;
- execution behavior;
- registered-operation execution;
- shell execution;
- subprocess execution;
- sudo requirements;
- write access;
- host mutation;
- network probes;
- port scans;
- DNS lookups;
- provider integrations;
- Prometheus integration;
- systemd service management;
- package management;
- process management;
- container management or orchestration;
- storage management;
- scheduler management;
- certificate renewal or trust validation;
- LLM reasoning.

# Mount Observation v1 Completion Note

Mount Observation v1 is now implemented after Hostname / Identity Observation v1.
It follows the Capability Extension Methodology with a narrow question/evidence
/fact/projection path:

- Question: what filesystems are currently mounted, what mount points exist,
  what devices are mounted, and what filesystem types/options are present?
- Evidence: `/proc/mounts`, read as a local read-only procfs file through Python
  standard-library file APIs.
- Facts: `mount_point`, `filesystem_type`, `mounted_device`, and `mount_option`.
- Projection: ordinary observation ingestion and current-fact projection; no
  `Runtime`, `ToolExecutor`, `EventLedger`, or `ProjectionStore` ownership
  changes.

Non-inferences are explicit: mount facts do not imply filesystem health,
writability, availability, reachability, device health, or device accessibility.
The slice does not use network access, DNS queries, shell execution,
subprocesses, sudo, provider APIs, Prometheus, or LLM reasoning.
