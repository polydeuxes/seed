# Executive Summary

Seed already has a strong observation architecture for read-only local knowledge: `LocalHostObservationSource` emits ordinary `Observation` objects, `ObservationIngestor` turns them into evidence-backed facts, and `StateProjector` projects those facts without changing `Runtime`, `ToolExecutor`, `EventLedger`, or `ProjectionStore` ownership. The current local source is intentionally narrow: it records host identity, OS, architecture, root disk bytes, local observation status, and local network configuration from Python standard-library calls plus read-only local files.

The next observation roadmap should continue that pattern. The highest-value and lowest-risk next domains are local configuration inventories that can be read from `/proc`, `/sys`, `/etc`, and Python standard-library APIs without root, subprocesses, network access, probes, provider integrations, or shell execution. The best first candidates are mounts, kernel/CPU/memory refinements, users/groups, environment shape, and certificate inventory. Medium-risk candidates include systemd units, listening ports, packages, storage topology, processes, local schedules, and containers because they need sharper boundaries to avoid becoming service health, execution, package-management, or orchestration features.

This audit is documentation-only. It does not implement new observations, does not add predicates, does not change runtime behavior, does not change tool execution, does not add provider integrations, and does not add network probing.

# Existing Local Observation Coverage

## Files and artifacts inspected

At minimum, this audit inspected:

- `seed_runtime/observation_sources.py`, especially `LocalHostObservationSource` and `ObservationCollectionService`.
- `seed_runtime/observations.py`, especially `Observation` and `ObservationIngestor`.
- `seed_runtime/observation_normalizers.py`, to confirm normalization remains projection-adjacent rather than collection execution.
- `predicate_catalog/core.json`, to identify existing local observation predicates.
- `relationship_catalog/core.json`, to understand relationship side effects from local facts.
- `docs/local_network_observation_audit.md`, for Local Network Observation v1 boundaries.
- `docs/capability_extension_methodology.md`, for extension flow and least-privilege rules.
- `docs/availability_vocabulary_audit.md`, for local observation versus availability boundaries.
- `docs/reasoning_roadmap.md`, for canonical runtime and ownership boundaries.
- `docs/invariants.md`, for architecture and capability extension invariants.
- `README.md`, especially the architecture, local network observation, and projection-cache sections.
- `tests/test_observation_sources.py`, especially local host and local network observation tests.
- `tests/test_observations.py`, for Observation -> Evidence -> Fact projection behavior.
- `tests/test_predicate_catalog.py`, for existing predicate catalog expectations.
- `tests/test_architecture_invariants.py`, for Runtime, ToolExecutor, EventLedger, and ProjectionStore invariants.

## Current source: `LocalHostObservationSource`

`LocalHostObservationSource` is the canonical existing local observation source. Its docstring defines it as a read-only local host source using Python standard-library APIs only, and states that it does not execute shells or subprocesses. Its shared metadata explicitly records:

- `collector = LocalHostObservationSource`
- `read_only = True`
- `local_only = True`
- `shell_execution = False`
- `subprocess_execution = False`
- `privilege_escalation = False`
- `network_probe = False`
- `network_connection = False`

This metadata is important because the observation evidence carries negative-space claims as well as positive facts.

## Facts currently produced

Current local host observation can produce these fact predicates:

| Domain | Predicate | Value shape | Evidence source | Boundary |
| --- | --- | --- | --- | --- |
| Local observation status | `local_observation_status` | `observed` | Successful local source collection | Does not imply host availability, provider visibility, endpoint reachability, or network health. |
| OS | `os` | Lowercase platform system string | Python `platform.system()` | Does not imply distro/package details. |
| Architecture | `architecture` | Machine architecture string | Python `platform.machine()` and optional `os.uname()` metadata | Does not imply CPU topology or hardware inventory. |
| Disk | `disk_total_bytes` | Integer bytes for `/` | Python `shutil.disk_usage("/")` | Root filesystem summary only; currently separate from Prometheus `filesystem_total_bytes`. |
| Disk | `disk_free_bytes` | Integer bytes for `/` | Python `shutil.disk_usage("/")` | Root filesystem summary only; currently separate from Prometheus `filesystem_free_bytes`. |
| Network interface | `network_interface` | Interface name | `socket.if_nameindex()` and `/proc/net/dev` | Interface exists locally; no reachability or link-health claim. |
| Interface role | `interface_role` | `primary`, `secondary`, `loopback`, `virtual`, `container`, or `vpn` | Interface name plus `/proc/net/route` default-route evidence | Classification only; no availability or reachability claim. |
| Interface state | `interface_operstate` | String from sysfs | `/sys/class/net/<iface>/operstate` | Local kernel-reported state only; no remote reachability claim. |
| MAC address | `interface_mac_address` | Lowercase MAC-like string | `/sys/class/net/<iface>/address` | Local interface attribute only. |
| MTU | `interface_mtu` | Integer | `/sys/class/net/<iface>/mtu` | Local interface attribute only. |
| IP address | `ip_address` | IPv4/IPv6 address string | IPv4 `SIOCGIFADDR`; IPv6 `/proc/net/if_inet6` | Configured address only; does not imply network reachability. |
| Address assignment | `address_assignment_method` | Currently emitted only as `dhcp` when evidenced | `/run/systemd/netif/leases/<ifindex>` matching an observed IPv4 address | Absence of DHCP evidence does not mean static. |
| Default gateway | `default_gateway` | IPv4 gateway address | `/proc/net/route` default-route rows | Configured route only; gateway reachability is not asserted. |
| DNS resolver | `dns_resolver` | Resolver IP string | `/etc/resolv.conf` nameserver lines | Configured resolver only; DNS success is not asserted. |
| DNS resolver stub | `dns_resolver_stub` | Loopback resolver IP string | `/etc/resolv.conf` loopback nameserver lines | Local stub configured; upstream knowledge/reachability is not asserted. |
| DNS upstream | `dns_resolver_upstream` | Non-loopback resolver IP string | `/run/systemd/resolve/resolv.conf` when readable | Configured upstream only; DNS resolution/reachability is not asserted. |

## Local domains already represented

Seed currently represents these local domains:

- Host observability status.
- Operating system family/name as a narrow platform value.
- Machine architecture.
- Root filesystem capacity/free bytes through local disk usage.
- Network interface inventory.
- Interface role classification.
- Interface operstate, MAC address, and MTU.
- Configured IP addresses.
- Default IPv4 gateway configuration.
- Resolver/stub/upstream DNS configuration.
- Explicit non-claims around availability, reachability, provider visibility, network probing, network connection, subprocess execution, shell execution, and privilege escalation.

## Current projection behavior

Local observations already fit the existing pipeline:

```text
Local source reads local data
-> Observation
-> Evidence
-> Fact
-> StateProjector projection
-> read-only views/explanations
```

`ObservationIngestor` records an observation event and a fact assertion with evidence payload containing observation provenance. The projector consumes ledger events. There is no need for fresh collection during projection, no runtime side effect, no provider call, and no tool execution.

# Candidate Observation Domains

The following candidate domains are inventory candidates only. They should not be implemented until each has a narrow predicate vocabulary and tests that lock down non-goals.

| Candidate domain | Question answered | Narrow facts that could be produced | Initial fit |
| --- | --- | --- | --- |
| Mounts | What filesystems are mounted locally? | `mount_point`, `mount_source`, `mount_fstype`, `mount_options` | Excellent |
| Kernel | What kernel is this host running? | `kernel_release`, `kernel_version`, `kernel_name` | Excellent |
| CPU | What CPU topology is locally visible? | `cpu_count`, `cpu_model`, `cpu_architecture_detail` | Excellent |
| Memory | How much memory is locally visible? | `memory_total_bytes`, `memory_available_bytes` | Excellent |
| Users | What local user accounts are configured? | `local_user`, `local_user_uid`, `local_user_shell`, `local_user_home` | Excellent |
| Groups | What local groups are configured? | `local_group`, `local_group_gid`, `local_group_member` | Excellent |
| Environment | What process environment shape is visible to Seed? | `environment_variable_present`, optionally allowlisted values | Excellent if value allowlist is strict |
| Certificates | What local trust anchors/cert files exist? | `certificate_store_path`, `certificate_subject`, `certificate_not_after` | Good |
| Storage topology | What block devices are visible? | `block_device`, `block_device_size_bytes`, `block_device_type`, `block_device_removable` | Good |
| Local schedules / cron | What scheduled local jobs are configured? | `scheduled_job`, `schedule_source`, `schedule_expression` | Good |
| Systemd units | What unit files or unit states are locally visible? | `systemd_unit`, `systemd_unit_enabled_state`, optionally `systemd_unit_active_state` | Good with DBus/file boundary; medium risk |
| Listening ports | What sockets are in listen state locally? | `listening_socket`, `listening_port`, `listening_protocol`, `listening_address` | Good with no process attribution by default |
| Processes | What processes are visible to this user? | `process_seen`, `process_command_name`, `process_uid` | Good but privacy-sensitive |
| Packages | What packages are locally installed? | `package_installed`, `package_version`, `package_manager` | Good if using read-only DB files only |
| Services | What service definitions exist? | `service_definition`, `service_manager`, `service_name` | Good if defined as configuration, poor if health-like |
| Containers | What container metadata is locally visible? | `container_runtime_detected`, `container_id_seen`, `container_name`, `container_image` | Poor-to-good depending on source; architecture risk if using Docker socket |
| Hardware | What hardware devices are locally visible? | `hardware_device`, `hardware_vendor`, `hardware_model` | Good but potentially noisy/privacy-sensitive |

# Capability Extension Methodology Fit

The capability extension methodology asks Seed contributors to name the gap, reduce it to a required question, define the narrowest fact, choose the least-privileged source, and keep observation separate from inference and execution. The table below applies that checklist to candidate local domains.

| Domain | Required question | Narrow facts | Evidence source | Read-only? | Non-root? | No execution? | No network? | Fit |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Mounts | Which filesystems are mounted? | Mount point/source/type/options | `/proc/self/mountinfo`, `/proc/mounts` | Yes | Yes | Yes | Yes | Excellent |
| Kernel | What kernel identity is visible? | Kernel name/release/version | `os.uname()`, `/proc/sys/kernel/*` | Yes | Yes | Yes | Yes | Excellent |
| CPU | What CPU capacity/topology is visible? | CPU count/model/flags as bounded facts | Python `os.cpu_count()`, `/proc/cpuinfo`, `/sys/devices/system/cpu` | Yes | Yes | Yes | Yes | Excellent |
| Memory | What memory capacity is visible? | Total/available memory bytes | `/proc/meminfo` | Yes | Yes | Yes | Yes | Excellent |
| Users | Which local accounts exist? | User name, UID, home, shell | Python `pwd`, `/etc/passwd` | Yes | Yes | Yes | Yes | Excellent |
| Groups | Which local groups exist? | Group name, GID, members | Python `grp`, `/etc/group` | Yes | Yes | Yes | Yes | Excellent |
| Environment | Which allowlisted environment variables are present? | Presence and safe value classes | `os.environ` for Seed process | Yes | Yes | Yes | Yes | Excellent if sensitive values are excluded |
| Certificates | Which local trust/cert files are present and parseable? | Cert path, subject, issuer, expiry | Read-only cert directories and Python `ssl`/parsing | Yes | Usually | Yes | Yes | Good |
| Storage topology | Which block devices are visible? | Device name/type/size/removable | `/sys/block`, `/proc/partitions` | Yes | Yes | Yes | Yes | Good |
| Local schedules / cron | Which local scheduled jobs are configured? | Schedule source/name/expression | `/etc/crontab`, `/etc/cron.*`, user crontabs if readable, systemd timer files | Yes | Partly | Yes | Yes | Good |
| Systemd units | Which units are installed/enabled or locally active? | Unit name/type/enabled state/active state | Unit files, read-only systemd DBus if allowed | Yes | Usually | Yes if DBus/file APIs only | Yes | Good |
| Listening ports | Which sockets are listening locally? | Address/port/protocol/state/inode | `/proc/net/tcp*`, `/proc/net/udp*`, `/proc/net/unix` | Yes | Yes for socket tables; process mapping partial | Yes | Yes | Good |
| Processes | Which processes are visible? | PID, command name, UID, state | `/proc/<pid>/stat`, `/proc/<pid>/status`, `/proc/<pid>/cmdline` | Yes | Partly; own/all metadata varies | Yes | Yes | Good with privacy limits |
| Packages | Which packages are installed? | Package name/version/manager | `/var/lib/dpkg/status`, rpm DB files if readable, apk/db files | Yes | Usually | Yes if DB read only | Yes | Good |
| Services | Which service definitions exist? | Service manager/name/definition path | systemd unit files, init dirs | Yes | Usually | Yes | Yes | Good for definitions only |
| Containers | Which container artifacts are visible? | Runtime marker, container metadata from local files | `/proc/1/cgroup`, `/run/.containerenv`, container runtime metadata dirs | Yes | Partly | Yes if files only | Yes | Poor-to-good; avoid Docker socket |
| Hardware | Which hardware devices are visible? | Vendor/model/device class | `/sys/devices`, `/sys/class/dmi/id`, `/proc/bus` files | Yes | Partly; DMI may be restricted | Yes | Yes | Good but noisy/privacy-sensitive |

## Fit findings

- **Excellent fit** domains produce small configuration or capacity facts from stable local files/APIs: mounts, kernel, CPU, memory, users, groups, and strictly allowlisted environment shape.
- **Good fit** domains are still local and read-only but need careful scoping to prevent overclaiming: certificates, storage topology, local schedules, systemd, listening ports, processes, packages, services, and hardware.
- **Poor fit / architecture-risk portions** are any candidate designs that require Docker socket calls, systemctl subprocesses, package-manager subprocesses, remote APIs, Prometheus, shell commands, sudo, network probes, health checks, or orchestration semantics.

# Safe Local Sources

| Source | Candidate domains | Required privileges | Root required? | Network required? | Subprocess required? | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `/proc/self/mountinfo` | Mounts | Read local procfs | No | No | No | Prefer over shelling out to `mount` or `findmnt`. |
| `/proc/mounts` | Mounts | Read local procfs | No | No | No | Simpler fallback; less structured than mountinfo. |
| `os.uname()` / Python `platform` | Kernel/OS/architecture | Process-local API | No | No | No | Already used for related metadata. |
| `/proc/sys/kernel/*` | Kernel | Read local procfs | No | No | No | Use only bounded files such as hostname, osrelease, version. |
| `os.cpu_count()` | CPU | Process-local API | No | No | No | Narrow count only; no topology details. |
| `/proc/cpuinfo` | CPU | Read local procfs | No | No | No | Architecture-dependent; normalize conservatively. |
| `/sys/devices/system/cpu` | CPU | Read local sysfs | No | No | No | Useful for online/offline CPU sets without execution. |
| `/proc/meminfo` | Memory | Read local procfs | No | No | No | Produces measurement-like memory facts. |
| Python `pwd` and `/etc/passwd` | Users | Read NSS/passwd data | No | No if configured files only; NSS backends can be broader | No | Prefer direct `/etc/passwd` for strictly local-only semantics. |
| Python `grp` and `/etc/group` | Groups | Read NSS/group data | No | No if configured files only; NSS backends can be broader | No | Prefer direct `/etc/group` for strictly local-only semantics. |
| `os.environ` | Environment | Process-local API | No | No | No | Record names/presence only by default; avoid secrets and full values. |
| `/etc/ssl`, `/usr/local/share/ca-certificates`, distro trust dirs | Certificates | Read local files | Usually no | No | No | Parse only readable files; do not open TLS connections. |
| Python `ssl` helpers | Certificates | Process-local/library API | No | No | No | Safe for default verify path discovery; avoid network validation. |
| `/sys/block`, `/proc/partitions` | Storage topology | Read local kernel files | No for basic fields | No | No | Do not run `lsblk`; do not require udevadm. |
| `/etc/crontab`, `/etc/cron.d`, `/etc/cron.daily` etc. | Local schedules | Read local files | No for system files; user spools may be restricted | No | No | Treat as configuration only, not job success/health. |
| systemd unit directories (`/etc/systemd/system`, `/usr/lib/systemd/system`, `/lib/systemd/system`) | Systemd/service definitions | Read local files | No for many dirs | No | No | Unit definition inventory only. |
| Read-only systemd DBus | Systemd state | Local user DBus/system bus read | Usually no for basic list/state, policy-dependent | No | No | Must avoid invoking unit actions; document DBus policy dependency. |
| `/proc/net/tcp`, `/proc/net/tcp6`, `/proc/net/udp`, `/proc/net/udp6`, `/proc/net/unix` | Listening ports | Read local procfs | No for socket table; PID attribution limited | No | No | Do not connect to ports; no reachability claim. |
| `/proc/<pid>/status`, `/proc/<pid>/stat`, `/proc/<pid>/cmdline`, `/proc/<pid>/comm` | Processes | Read local procfs | Partial; hidepid and permissions vary | No | No | Minimize command-line capture; privacy-sensitive. |
| `/var/lib/dpkg/status` | Packages | Read dpkg database | Usually no | No | No | Do not call `dpkg`/`apt`. |
| rpm database files | Packages | Read rpm database | Varies | No | No | Python stdlib has no rpm parser; avoid subprocess. Poorer fit unless parser is added carefully. |
| `/lib/apk/db/installed` | Packages | Read apk database | Usually no | No | No | Good for Alpine-like hosts. |
| `/proc/1/cgroup`, `/.dockerenv`, `/run/.containerenv` | Container environment detection | Read local files | Usually no | No | No | Safe for “this process is in a container”-style facts. |
| Container runtime metadata dirs | Containers | Read local files | Often restricted | No | No | Avoid Docker/containerd sockets because they are privileged control planes. |
| `/sys/class/dmi/id`, `/sys/devices`, `/proc/device-tree` | Hardware | Read local sysfs/procfs | Partial; some files root-only | No | No | Basic hardware only; privacy/noise controls needed. |

# Observation Boundaries

The following should **not** be considered local observation in this roadmap:

- **Ping / ICMP checks.** They send packets and assert reachability-like evidence from a vantage point, which is active probing rather than passive local inventory.
- **Port scanning.** It sends network traffic, can affect remote systems, and produces reachability/security-test evidence rather than local configuration facts.
- **Prometheus queries.** Prometheus is a provider observation source, not local machine observation; it depends on a remote HTTP API and provider semantics.
- **Provider APIs.** Cloud, SaaS, orchestration, and monitoring APIs are external read-only providers at best; they are not local-only sources.
- **Remote SSH.** SSH requires network access, authentication, and remote execution semantics. It is outside local observation even if commands are read-only.
- **DNS lookups.** Resolver configuration can be observed locally, but performing a lookup is a network operation and tests DNS behavior.
- **HTTP checks.** HTTP requests are active network checks and belong to reachability or availability verification, not passive local inventory.
- **Reachability checks.** Any attempt to prove “can reach” changes the claim from configuration to active network evidence.
- **Neighbor discovery.** ARP/NDP observation or solicitation can reveal network neighbors and may involve active discovery or privileged tables. It is not needed for narrow local host facts.
- **Availability checks.** Availability is an evidence-backed interpretation with scope and freshness; local configuration alone must not produce `availability_status = up`.
- **Shell command execution.** Running `ps`, `ss`, `systemctl`, `docker`, `findmnt`, `lsblk`, `dpkg`, or similar commands introduces execution behavior and subprocess dependencies.
- **Sudo or privilege escalation.** Elevated read access expands authority and should not be part of the safe default local observation roadmap.
- **Docker socket or container runtime control sockets.** These are effectively privileged APIs and may allow mutation or container escape paths; reading socket APIs is not equivalent to reading local files.
- **LLM reasoning over the host.** Observation should collect bounded facts from explicit sources. LLMs can explain projected knowledge later, but should not invent or infer host facts during collection.

# Local Knowledge Roadmap

## High Value / Low Risk

These candidates are strong early roadmap items because they are local-only, read-only, non-root in normal environments, narrow, and evidence-backed:

1. **Mounts** — `/proc/self/mountinfo` gives high operational value and complements root disk bytes without probing or execution.
2. **Kernel** — `os.uname()` and bounded `/proc/sys/kernel` files refine current OS/architecture facts.
3. **CPU** — CPU count/topology facts are useful for capacity reasoning and safely available from procfs/sysfs/Python.
4. **Memory** — `/proc/meminfo` adds capacity observations with simple numeric facts.
5. **Users** — `/etc/passwd` or Python `pwd` can inventory configured local accounts if sensitive fields are avoided.
6. **Groups** — `/etc/group` or Python `grp` can inventory configured local groups and membership.
7. **Environment shape** — allowlisted environment variable presence can explain Seed's local context without leaking secret values.

## High Value / Medium Risk

These candidates are useful but require additional vocabulary and privacy/semantic boundaries before implementation:

1. **Systemd units** — valuable for service inventory, but must not use `systemctl` subprocesses, start/stop units, or imply service health from unit presence.
2. **Listening ports** — valuable for local service exposure inventory, but must not connect to sockets or infer availability; process attribution can be permission-sensitive.
3. **Packages** — valuable for local software inventory, but must use read-only package DB files and avoid package-manager subprocesses.
4. **Storage topology** — useful for disks/partitions, but can become noisy and platform-specific; should avoid `lsblk` and udev command execution.
5. **Local schedules / cron** — useful for automation inventory, but user crontabs may be permission-restricted and job definitions must not imply successful runs.
6. **Certificates** — useful for trust inventory, but parsing must avoid network validation and handle sensitive/private key boundaries.
7. **Processes** — useful for visibility, but process command lines can contain secrets and visibility varies by permission/hidepid settings.
8. **Containers** — useful for runtime context, but safe scope should start with file markers and cgroup facts; Docker socket/API access is an architecture risk.

## Low Value

These candidates are local-only but should be lower priority unless a clear question emerges:

- Broad hardware inventory beyond basic CPU/storage. It can be noisy, platform-specific, and privacy-sensitive.
- Full environment variable values. Presence can be useful, but values often contain secrets or local personalization.
- Exhaustive filesystem traversal. It is local and read-only, but broad scans are high-noise, expensive, and risk sensitive data exposure.
- User shell histories or application-specific dotfiles. These are local, but they are private behavioral records rather than safe system inventory.

## Architecture Risk

These are high-risk designs and should be avoided for this roadmap:

- Docker/containerd socket integrations.
- `systemctl`, `ps`, `ss`, `netstat`, `findmnt`, `lsblk`, `crontab`, `dpkg`, `rpm`, or package-manager subprocess execution.
- Network probing, reachability tests, DNS lookups, and HTTP checks.
- Prometheus or provider API integration as a dependency of local observation.
- Sudo/elevated readers.
- Runtime-driven observation or ToolExecutor-driven discovery.
- Any observation that writes to the ledger outside the existing ObservationCollectionService/ObservationIngestor path.

# Architecture Fit Analysis

## Existing pipeline compatibility

Every candidate should fit the same shape:

```text
Observation
-> Evidence
-> Fact
-> Projection
```

A candidate fits the architecture if it can be implemented as a source adapter that returns `Observation` objects and then relies on existing ingestion and projection behavior. It should not require:

- `Runtime` changes.
- `ToolExecutor` changes.
- `EventLedger` ownership changes.
- `ProjectionStore` ownership changes.
- New execution behavior.
- Provider calls.
- Network access.
- Prompt/LLM reasoning.

## Candidate-by-candidate architecture fit

| Domain | Fits Observation -> Evidence -> Fact -> Projection? | Runtime changes needed? | ToolExecutor changes needed? | Provider calls? | Network access? | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Mounts | Yes | No | No | No | No | Straight local file parsing. |
| Kernel | Yes | No | No | No | No | Extends existing platform facts. |
| CPU | Yes | No | No | No | No | Numeric and string facts from procfs/sysfs. |
| Memory | Yes | No | No | No | No | Measurement facts from `/proc/meminfo`. |
| Users | Yes | No | No | No | No | Prefer direct local files over NSS if strict local-only is required. |
| Groups | Yes | No | No | No | No | Same boundary as users. |
| Environment | Yes | No | No | No | No | Must be allowlist/presence-based. |
| Certificates | Yes | No | No | No | No | File parsing only; no TLS connection checks. |
| Storage topology | Yes | No | No | No | No | Sysfs/procfs only. |
| Local schedules | Yes | No | No | No | No | Config facts only. |
| Systemd units | Yes if file/DBus read-only | No | No | No | No | DBus policy may vary; no unit actions. |
| Listening ports | Yes | No | No | No | No | Socket table facts only; no connect probes. |
| Processes | Yes | No | No | No | No | Privacy minimization required. |
| Packages | Yes for parseable DB files | No | No | No | No | Avoid package-manager commands. |
| Services | Yes for definitions | No | No | No | No | Do not equate service definition with running/healthy. |
| Containers | Yes for file/cgroup markers | No | No | No | No | Runtime sockets would violate boundary. |
| Hardware | Yes | No | No | No | No | Control noise/privacy. |

## Ownership confirmation

The roadmap does not require changes to the established ownership model:

- `Runtime` remains canonical and is not an observation collector.
- `ToolExecutor` remains the only registered-operation executor and is not used for observation.
- `EventLedger` remains append-only event ownership.
- `ProjectionStore` remains cached projected-state snapshot ownership.
- `StateProjector` remains deterministic projection from events to current state.
- Capability resolution remains downstream of projected knowledge and does not verify or execute capabilities.

# Recommended Roadmap

The recommended order favors high value, low risk, least privilege, and narrow facts.

## 1. Mount observation

**Why first:** Mount inventory is valuable, stable, and safely available from `/proc/self/mountinfo` without root, subprocesses, network access, or provider calls. It naturally extends existing disk observations without claiming health or availability.

**Candidate facts:** `mount_point`, `mount_source`, `mount_fstype`, `mount_options`, with dimensions for mount ID or parent ID only if needed.

**Required boundaries:** Mounted does not mean healthy, writable, performant, remote share reachable, or sufficient capacity.

## 2. Kernel, CPU, and memory observation

**Why second:** These are foundational capacity/context facts that can be observed from Python stdlib, `/proc`, and `/sys` with very low risk.

**Candidate facts:** `kernel_release`, `kernel_version`, `cpu_count`, `cpu_model`, `memory_total_bytes`, `memory_available_bytes`.

**Required boundaries:** Capacity/configuration does not imply performance, workload health, or scheduling availability.

## 3. User and group observation

**Why third:** Local account and group inventory is useful for explaining ownership and host context, and can be read without execution.

**Candidate facts:** `local_user`, `local_user_uid`, `local_user_home`, `local_user_shell`, `local_group`, `local_group_gid`, `local_group_member`.

**Required boundaries:** Account existence does not imply login success, current activity, authorization to perform an operation, or identity verification. Sensitive hashes are never read or stored.

## 4. Storage topology observation

**Why fourth:** Block-device topology helps explain disks beyond the root filesystem and complements mount facts.

**Candidate facts:** `block_device`, `block_device_size_bytes`, `block_device_type`, `block_device_removable`, `partition_name`.

**Required boundaries:** Device presence does not imply health, free capacity, SMART status, or filesystem integrity.

## 5. Package inventory from read-only DB files

**Why fifth:** Package inventory has high diagnostic value, but safe implementation depends on file-format parsers and must avoid package-manager subprocesses.

**Candidate facts:** `package_installed`, `package_version`, `package_manager`.

**Required boundaries:** Installed does not mean running, patched, secure, supported, or usable.

## 6. Systemd unit file observation

**Why sixth:** Service/unit definitions are valuable but semantically tricky. Start with unit files and enabled-state files rather than active health, and avoid `systemctl` execution.

**Candidate facts:** `systemd_unit`, `systemd_unit_type`, `systemd_unit_file_path`, `systemd_unit_enabled_state`.

**Required boundaries:** Unit exists/enabled does not mean running, healthy, reachable, or desired by the operator.

## 7. Listening-port observation

**Why seventh:** Listening sockets are valuable for local service exposure inventory, but must be carefully described as kernel socket state only.

**Candidate facts:** `listening_socket`, `listening_protocol`, `listening_address`, `listening_port`.

**Required boundaries:** Listen state does not mean remote reachability, successful accept, service health, authentication success, or application availability.

## 8. Local schedule observation

**Why eighth:** Cron and timer definitions explain local automation but need file permissions and privacy boundaries.

**Candidate facts:** `scheduled_job`, `schedule_source`, `schedule_expression`, `schedule_command_label` where command capture is bounded.

**Required boundaries:** Scheduled does not mean the job ran, succeeded, is enabled in all contexts, or is safe to execute.

## 9. Certificate inventory

**Why ninth:** Certificate/trust inventory is useful but parsing and privacy boundaries need care.

**Candidate facts:** `certificate_store_path`, `certificate_subject`, `certificate_issuer`, `certificate_not_after`.

**Required boundaries:** Certificate exists does not mean trust is correct, TLS works, endpoints are reachable, or private keys are valid.

## 10. Process and container file-marker observation

**Why last among recommended items:** Processes and containers are useful but sensitive. Start with minimal process visibility and container environment markers, not Docker sockets or orchestration APIs.

**Candidate facts:** `process_seen`, `process_command_name`, `process_uid`, `container_environment_detected`, `container_runtime_marker`.

**Required boundaries:** Process seen does not mean healthy; container marker does not mean Docker is installed or controllable; runtime socket access is out of scope.

# Non-Goals

This roadmap audit does not:

- Implement new observations.
- Add predicates or catalog entries.
- Change `Runtime`.
- Change `ToolExecutor`.
- Change `EventLedger` ownership.
- Change `ProjectionStore` ownership.
- Add execution behavior.
- Add provider integrations.
- Add Prometheus integration.
- Add network probing.
- Add shell execution.
- Add subprocess usage.
- Add sudo or privilege escalation requirements.
- Add Docker/containerd socket integrations.
- Add DNS lookups, ping, HTTP checks, reachability checks, or availability checks.
- Add LLM reasoning to observation or projection.
- Treat local configuration as availability, health, reachability, or verification.

# Mount Observation v1 Status

Mount Observation v1 has been completed as the next roadmap slice after local
identity observation. The implementation observes `/proc/mounts` only and emits
narrow `mount_point`, `filesystem_type`, `mounted_device`, and `mount_option`
facts. It intentionally does not infer mount health, storage health,
writability, reachability, or availability, and it does not call `mount`,
`findmnt`, shells, subprocesses, network APIs, DNS, sudo, Prometheus, or provider
integrations.
