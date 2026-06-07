# Executive Summary

Seed's implemented local observations now form a recurring knowledge-class pattern. This vocabulary names five documentation-only classes for facts Seed acquires or plans to acquire: **Identity**, **Configuration**, **Topology**, **Description**, and **State**.

The classes describe what a fact is about and its expected stability. They do not add behavior, projection semantics, freshness policy, scheduling, context composition, execution, provider integration, or LLM reasoning. The classification is a review and planning vocabulary that helps explain why stable anchoring facts usually precede more volatile operational facts.

A concise ordering emerges for local knowledge acquisition:

```text
Identity -> Configuration -> Topology -> Description -> State
```

That ordering is not a runtime rule. It is a documentation convention for roadmap explanation: start with durable anchors, then add configured values and structural relationships, then machine descriptions, and only then add volatile state markers.

# Purpose

The purpose of Knowledge Classification Vocabulary v1 is to define the major classes of knowledge Seed currently acquires and expects to acquire through local observation slices.

This document supports:

- roadmap review;
- capability-extension review;
- explainability language;
- future context-prioritization discussion;
- future freshness-policy discussion;
- future knowledge-acquisition planning.

It is intentionally documentation-first. It does not change `Runtime`, `ToolExecutor`, `EventLedger`, `ProjectionStore`, projection behavior, observation behavior, scheduling behavior, context composition, provider integration, or LLM reasoning.

# Knowledge Classes

## Identity

Identity knowledge names or distinguishes the observed subject.

It represents facts that Seed can use as stable anchors for later observations, evidence, explanations, aliases, and projections. Identity facts answer questions such as "which local host is this?", "which boot instance is being observed?", or "which locally recorded host name identifies this machine?"

Facts that belong in Identity include:

- local host names;
- machine identifiers;
- boot-session identifiers;
- explicitly configured fully qualified names;
- future directly observed identity relationships, if they are locally sourced and do not imply ownership or reachability.

Typical stability: **very high** for machine and configured host identity, with the important exception that boot-scoped identity changes on reboot.

Identity is useful because other facts need a durable subject anchor. It lets Seed explain what entity a later interface, mount, package, or process fact is about without inferring provider identity, host ownership, DNS validity, reachability, uniqueness, health, or availability.

Examples:

| Fact | Class | Notes |
| --- | --- | --- |
| `hostname` | Identity | Locally configured host name. Does not imply DNS validity. |
| `machine_id` | Identity | Locally recorded machine identifier. Does not guarantee global uniqueness. |
| `boot_id` | Identity | Current boot-session identifier. Stable during a boot, not across boots. |
| `fqdn` | Identity | Explicitly configured qualified name. Does not imply DNS resolution. |

## Configuration

Configuration knowledge records declared or configured settings.

It represents facts that describe how the host is configured to behave or how local components are configured to resolve, route, expose, or constrain resources. Configuration facts answer questions such as "what resolver is configured?", "what route is configured?", or "what option is declared for this mount?"

Facts that belong in Configuration include:

- IP address assignments;
- default gateways;
- DNS resolver declarations;
- address assignment methods;
- mount options;
- scheduled job definitions;
- user and group database entries;
- certificate store declarations;
- systemd unit definitions, when treated as declarations rather than live health.

Typical stability: **high**. Configuration often persists across process lifetimes and reboots, but can be changed by operators, DHCP, configuration management, package installation, or local policy.

Configuration is useful because it explains intended or declared system behavior without claiming that the behavior succeeds. A configured DNS resolver does not prove DNS works. A configured gateway does not prove reachability. A mount option does not prove writability or storage health.

Examples:

| Fact | Class | Notes |
| --- | --- | --- |
| `ip_address` | Configuration | Address configured on an interface; not a reachability proof. |
| `default_gateway` | Configuration | Route configuration; not packet-delivery proof. |
| `dns_resolver` | Configuration | Resolver declaration; not DNS-success proof. |
| `mount_option` | Configuration | Mounted filesystem option; not health or writability proof. |

## Topology

Topology knowledge describes local structure and relationships among local resources.

It represents facts about what components exist and how they are arranged: interfaces, mount points, devices, filesystems, block devices, sockets, and other structural relationships. Topology facts answer questions such as "what interfaces exist?", "what is mounted where?", or "which device backs this mounted filesystem?"

Facts that belong in Topology include:

- network interfaces;
- mount points;
- mounted devices;
- filesystem types;
- storage devices and partitions;
- listening socket endpoints when treated as exposure topology rather than service health;
- container or process placement markers when used to describe local arrangement, though their volatility usually places them in State for ordering.

Typical stability: **medium-high**. Topology often persists for the lifetime of a host configuration or boot, but can change when interfaces appear, mounts change, containers start, disks attach, or services bind sockets.

Topology is useful because it tells Seed where later configuration, description, and state facts attach. It gives explainability a structural vocabulary without implying availability, health, reachability, ownership, or successful I/O.

Examples:

| Fact | Class | Notes |
| --- | --- | --- |
| `network_interface` | Topology | Interface presence; not connectivity. |
| `mount_point` | Topology | Kernel mount-table entry; not accessibility or health. |
| `mounted_device` | Topology | Device name from mount table; not device health. |
| `filesystem_type` | Topology | Filesystem kind at a mount; not capacity or correctness. |

## Description

Description knowledge records descriptive properties of the host or installed substrate.

It represents facts that characterize what the system is, what implementation it runs, or what resources it reports. Description facts answer questions such as "what OS is this?", "what architecture is this?", "what kernel version is this?", "what CPU model is present?", or "how much memory is installed?"

Facts that belong in Description include:

- operating system name;
- architecture;
- kernel release/version;
- CPU model and count;
- memory total;
- installed package inventory when treated as descriptive implementation inventory;
- local disk capacity observations when they describe resource shape rather than health.

Typical stability: **medium**. Description often changes less frequently than live state but more often than identity: kernels, packages, hardware, VM sizing, memory, and architecture-related values can change through upgrades, resizes, image changes, or host replacement.

Description is useful because it gives Seed explanatory context for capabilities and constraints without becoming verification. Knowing an architecture or kernel version can help interpret future facts, but it does not prove that an operation is safe, available, or authorized.

Examples:

| Fact | Class | Notes |
| --- | --- | --- |
| `os` | Description | Local platform description. |
| `architecture` | Description | Machine architecture description. |
| `kernel_release` | Description | Kernel release from local kernel evidence. |
| `kernel_version` | Description | Kernel version string from local kernel evidence. |
| `cpu_model` | Description | CPU model reported by local CPU evidence. |
| `cpu_count` | Description | CPU count visible in local CPU evidence. |
| `memory_total_bytes` | Description | Total memory reported by local memory evidence; not free or available memory. |

## State

State knowledge records volatile operational conditions or markers.

It represents facts that describe what is happening now or what is currently present in a live operational table. State facts answer questions such as "is this marker present now?", "which ports are currently listening?", or "what process/container marker is currently visible?"

Facts that belong in State include:

- process markers;
- container markers;
- listening ports when treated as live socket-table state;
- interface operational state;
- current free disk bytes;
- other live markers whose value may change frequently.

Typical stability: **low**. State can change across seconds, process lifetimes, service restarts, network events, mounts, container operations, or reboots.

State is useful because it captures current operational evidence while preserving strict non-inference boundaries. A listening port does not prove remote reachability, service identity, service health, or authorization. A process marker does not prove service correctness. A container marker does not give Seed orchestration authority.

Examples:

| Fact | Class | Notes |
| --- | --- | --- |
| `process_marker` | State | Planned minimal process evidence; not process management. |
| `container_marker` | State | Planned local marker evidence; not Docker/Kubernetes authority. |
| `listening_port` | State | Planned socket-table evidence; not reachability or health. |
| `interface_operstate` | State | Current interface state marker; not end-to-end availability. |

# Existing Observation Mapping

Implemented observations are not always one class per observation source. A single source can emit multiple fact classes while preserving one observation/evidence/fact pipeline.

| Implemented observation/fact | Class | Finding |
| --- | --- | --- |
| `hostname` | Identity | Stable local identity anchor from bounded local sources. |
| `machine_id` | Identity | Stable local machine identity, with explicit non-uniqueness caveat. |
| `boot_id` | Identity | Boot-scoped identity; stable during a boot and expected to change across boots. |
| `fqdn` | Identity | Identity only when explicitly configured locally; no DNS synthesis or lookup. |
| `local_observation_status` | State | Current observation marker that says Seed inspected this host locally. |
| `os` | Description | Describes the local platform. |
| `architecture` | Description | Describes machine architecture. |
| `disk_total_bytes` | Description | Describes local root filesystem capacity shape. |
| `disk_free_bytes` | State | Current free-space measurement; more volatile than total capacity. |
| `kernel_release` | Description | Kernel release from `/proc/sys/kernel/osrelease`. |
| `kernel_version` | Description | Kernel version string from `/proc/version`. |
| `cpu_model` | Description | CPU model from `/proc/cpuinfo` when reported. |
| `cpu_count` | Description | CPU count from `/proc/cpuinfo` processor entries, or `os.cpu_count()` when procfs CPU evidence is absent. |
| `memory_total_bytes` | Description | Total memory from `/proc/meminfo` `MemTotal`; no volatile available/free memory fact is emitted. |
| `network_interface` | Topology | Structural local interface presence. |
| `interface_role` | Topology | Local classification of interface role relative to default route; not reachability. |
| `interface_operstate` | State | Live interface state marker. |
| `interface_mac_address` | Identity | Hardware/interface identifier for a local interface; may be virtualized or changed. |
| `interface_mtu` | Configuration | Configured interface MTU. |
| `ip_address` | Configuration | Configured address assignment; not reachability. |
| `address_assignment_method` | Configuration | Declared/inferred-from-local-files address assignment method; not lease validity. |
| `default_gateway` | Configuration | Configured route; not connectivity proof. |
| `dns_resolver` | Configuration | Resolver declaration; not DNS-success proof. |
| `dns_resolver_stub` | Configuration | Stub resolver declaration; not upstream resolution proof. |
| `dns_resolver_upstream` | Configuration | Locally declared upstream resolver; not reachability or DNS-success proof. |
| `mount_point` | Topology | Mount-table structure; not accessibility or health. |
| `filesystem_type` | Topology | Filesystem kind in mount table. |
| `mounted_device` | Topology | Mounted backing device/source as reported by `/proc/mounts`; not device health. |
| `mount_option` | Configuration | Declared mount option; not writability, health, or successful I/O. |

# Roadmap Mapping

Roadmap items should be classified by the primary fact class they are expected to add. Some items may emit secondary classes, but the primary class is enough for documentation ordering.

| Roadmap item | Primary class | Secondary class, if any | Finding |
| --- | --- | --- | --- |
| Hostname / Identity Observation | Identity | None | Already implemented as a high-stability anchor. |
| Mount Observation | Topology | Configuration | Mount points/devices/filesystem types are topology; mount options are configuration. |
| Local Network Observation | Configuration | Topology, State, Identity | Addresses/routes/resolvers dominate; interfaces are topology; operstate is state; MAC address is interface identity. |
| Local Host Observation | Description | Identity, State | OS/architecture/capacity description dominates; status and free bytes are more volatile. |
| Kernel Observation | Description | None | Implemented kernel release/version describe the host substrate. |
| CPU Observation | Description | None | Implemented CPU count/model describe the host substrate. |
| Memory Observation | Description | State | Implemented total memory is description; free/available memory remains state if added later. |
| Storage Topology Observation | Topology | Description, Configuration | Block devices and partitions are topology; size/media details may be description; options/policies may be configuration. |
| Listening Port Observation | State | Topology | Socket tables are live state; endpoints can also describe exposure topology. |
| Users Observation | Configuration | Identity | `/etc/passwd` entries are configured accounts; usernames/UIDs can serve as local identities. |
| Groups Observation | Configuration | Identity | `/etc/group` entries are configured groups; group names/GIDs can serve as local identities. |
| Package Observation | Description | Configuration | Installed package inventory describes implementation; repository/source configuration would be configuration. |
| Systemd Observation | Configuration | State | Unit definitions are configuration; active/enabled runtime markers would be state and must remain read-only. |
| Schedule Observation | Configuration | None | Cron/timer declarations are configuration; execution success is out of scope. |
| Certificate Observation | Configuration | Description | Store membership/trust declarations are configuration; certificate subject/issuer/expiry are descriptive properties. |
| Process Marker Observation | State | None | Process markers are volatile operational evidence. |
| Container Marker Observation | State | Topology | Container/cgroup markers are volatile; placement relationships can be topology. |

# Stability Characterization

| Class | Typical stability | Characterization | Examples |
| --- | --- | --- | --- |
| Identity | Very high | Best anchor class. Usually changes only through deliberate reconfiguration, cloning, reboot for boot-scoped identity, or host replacement. | `hostname`, `machine_id`, `boot_id`, `fqdn` |
| Configuration | High | Usually stable until operator, DHCP, package, policy, or configuration-management changes occur. | `ip_address`, `default_gateway`, `dns_resolver`, `mount_option` |
| Topology | Medium-high | Often stable across a boot or host configuration, but can change when devices, mounts, interfaces, services, or containers appear/disappear. | `network_interface`, `mount_point`, `mounted_device`, `filesystem_type` |
| Description | Medium | Changes occasionally through upgrades, hardware/VM resize, image replacement, package changes, or kernel changes. | `os`, `architecture`, `kernel_release`, `kernel_version`, `cpu_model`, `cpu_count`, `memory_total_bytes` |
| State | Low | Can change frequently as processes, ports, containers, operational markers, interface state, or free capacity change. | `process_marker`, `container_marker`, `listening_port`, `interface_operstate` |

This is a vocabulary characterization only. It does not implement freshness behavior, staleness markers, cache invalidation, resampling policy, context weighting, or scheduling.

# Capability Extension Methodology Alignment

The classification fits Seed's Capability Extension Methodology because it helps reviewers choose narrow facts and least-privileged sources before implementation.

Higher-stability classes should generally be observed before lower-stability classes because:

- stable identity gives later facts a durable subject anchor;
- configuration and topology explain declared structure before volatile activity is interpreted;
- description helps explain host substrate constraints without claiming live health;
- state facts are easiest to overread as health, reachability, or control authority and therefore need the strongest non-inference boundaries.

Practical ordering examples:

- Identity before State: observe `hostname`, `machine_id`, and `boot_id` before process/container markers so volatile markers attach to a known subject.
- Topology before Processes: observe interfaces, mounts, storage, and socket structures before interpreting process markers.
- Configuration before Containers: observe resolvers, routes, mount options, users/groups, and unit definitions before container markers that may depend on them.

This does not mean every roadmap item must strictly block every lower-stability item. It means documentation and review should justify lower-stability observations with especially narrow questions, direct evidence, and explicit non-inferences.

# Architecture Fit

The classification does **not** change Seed architecture.

| Architecture area | Change? | Rationale |
| --- | --- | --- |
| `Runtime` | No | Runtime remains the canonical orchestration path. This vocabulary does not add routing, context composition, decision validation, scheduling, or behavior. |
| `ToolExecutor` | No | Tool execution ownership remains unchanged. Knowledge classification does not execute operations or register tools. |
| `EventLedger` | No | EventLedger remains the append-only historical source of truth. Classification does not alter event ownership, event shape, or event replay. |
| `ProjectionStore` | No | ProjectionStore remains a cache of derived projected state. Classification does not add projection semantics, freshness semantics, or storage ownership. |
| Projection | No | Facts continue to be projected from observations/evidence through existing paths. Classification is documentation attached to vocabulary and roadmap review, not a projector rule. |
| Observation sources | No | Existing observation sources remain unchanged. This document classifies emitted facts; it does not add collection behavior. |
| Context composition | No | No context prioritization, filtering, weighting, or freshness logic is implemented here. |

The architecture fit finding is therefore: **classification is explanatory metadata for humans today, not executable architecture.**

# Knowledge Acquisition Ordering

The current roadmap has historically been explained partly by subsystem boundaries such as host, network, mount, storage, systemd, packages, schedules, processes, and containers. The classification vocabulary suggests a complementary explanation based on knowledge stability:

```text
Identity -> Configuration -> Topology -> Description -> State
```

Findings:

1. The existing ordering already begins with stable anchors: Hostname / Identity, local host facts, local network facts, and mount facts.
2. The next low-risk planned observations are mostly Description and Topology: kernel, CPU, memory, and storage topology.
3. Mid-roadmap items such as users, groups, packages, systemd units, schedules, and certificates are mostly Configuration or Description and can remain read-only inventory slices.
4. The most volatile items, listening ports, process markers, and container markers, belong late in the ordering because they risk being mistaken for health, reachability, service identity, orchestration authority, or execution capability.
5. Subsystem boundaries remain useful for implementation scoping, but stability classes better explain why one subsystem slice should precede another.

Recommended documentation framing: keep subsystem names for concrete implementation slices, and add knowledge class labels to explain why the roadmap orders stable anchors before volatile state.

# Potential Future Uses

Potential future uses of this vocabulary include:

- context prioritization discussions, where stable identity and configuration facts may be easier to include before volatile state facts;
- explainability language, where answers can distinguish identity, configuration, topology, description, and state evidence;
- freshness-policy design, where State could later need shorter freshness windows than Identity;
- knowledge acquisition planning, where new slices can state their primary class and stability risk;
- audit review, where reviewers can identify when a proposed observation class is being overread as availability, health, reachability, ownership, or execution authority;
- projection-policy discussion, where class labels may help future documentation reason about conflict handling or staleness without changing projection today.

These are possible future uses only. This document does not implement or recommend behavior changes.

# Non-Goals

This vocabulary does not:

- change `Runtime`;
- change `ToolExecutor`;
- change `EventLedger` ownership;
- change `ProjectionStore` ownership;
- add execution behavior;
- add projection behavior;
- add scheduling;
- add freshness logic;
- add context-composition logic;
- add provider integrations;
- add LLM reasoning;
- add network probing;
- add shell or subprocess execution;
- add new observation sources;
- add new predicates;
- infer health, availability, reachability, ownership, uniqueness, or control authority;
- require tests beyond documentation/invariant checks that may already exist.
