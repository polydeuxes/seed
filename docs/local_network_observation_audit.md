# Local Network Observation Audit

## Purpose

Design the next locality-first observation source for Seed to learn about its
own local network position without probing neighbors, depending on Prometheus,
executing shell commands, changing `Runtime` or `ToolExecutor`, or inferring
availability.

The recommended smallest safe implementation is to extend
`LocalHostObservationSource` so it emits local-only network facts gathered from
Python standard library and local kernel filesystems only:

- `network_interface`
- `interface_operstate`
- `ip_address`
- `default_gateway`
- `dns_resolver`

This document is an audit and design recommendation only. It does not implement
collection, catalog changes, projection changes, or CLI output changes.

## Current Local Host Observation Source

`LocalHostObservationSource` is already the right integration point for a
locality-first network source because it is a read-only discovery source and its
contract explicitly avoids shells and subprocesses. It currently collects:

- `local_observation_status = observed`
- `os`
- `architecture`
- `disk_total_bytes`
- `disk_free_bytes`

The local observation status metadata already carries important negative-space
claims:

- `network_reachability_asserted = False`
- `provider_visibility_asserted = False`
- `availability_asserted = False`
- `shell_execution = False`
- `read_only = True`

Those flags should remain true for the network extension. Local network facts
should say what the local kernel or resolver configuration exposes, not whether
any other host is reachable.

## Current Catalog Coverage

### PredicateCatalog

The built-in predicate catalog currently has only one network-adjacent canonical
identity predicate relevant to this audit:

- `ip_address`: durable, string, multi-valued.

Other relevant existing predicates are:

- `local_observation_status`: measurement enum with the only value `observed`.
- `availability_status`: measurement enum with values `up`, `down`, `unknown`.
- `ansible_host`: durable string, multi-valued inventory identity.
- `prometheus_instance`: durable string, multi-valued provider identity.

There are no canonical predicates today for:

- network interface existence;
- interface administrative state;
- interface operational/carrier state;
- default gateway/default route;
- DNS resolver;
- local network segment/prefix;
- neighbor table reachability state.

The Prometheus mappings are intentionally provider-specific and should not be a
dependency for the local source. Existing mappings only normalize Prometheus
`up` to `availability_status` and Prometheus filesystem metrics to filesystem
byte predicates.

### RelationshipCatalog

The built-in relationship catalog currently derives these network-adjacent
relationships:

- `alias_of` from `alias`, `hostname`, `ip_address`, `ansible_host`, and
  `prometheus_instance`;
- `monitored_by` from `prometheus_instance`;
- `member_of` from `group`;
- `provides` from `provides` and `endpoint_role`;
- `runs_on` from `host` and `runs_on`.

Important implication: emitting `ip_address` on the host subject will create an
identity-style `alias_of` relationship between the host and the IP literal. That
matches existing Ansible inventory behavior, but it is coarse for interface-
scoped local networking. If the implementation needs to preserve which
interface owns which address, it should use dimensions or a narrow companion
predicate rather than changing broad identity semantics in the first step.

No relationship is currently needed for default gateway or DNS resolver. Adding
relationships such as `routes_via` or `uses_resolver` would be larger than the
smallest safe implementation and could encourage accidental topology inference.

### EntityTypeCatalog

The built-in entity types are:

- `host`
- `service`
- `group`
- `endpoint`
- `monitoring_system`
- `capability`
- `unknown`

There are no entity types for:

- network interface;
- IP address;
- gateway;
- DNS resolver;
- network segment/subnet.

The smallest safe implementation should avoid adding entity types initially.
Interface names, gateway addresses, resolver addresses, and prefixes can remain
fact values or dimensions on the host until Seed has a clearer topology model.

## Current StateProjector Behavior

`StateProjector` rebuilds state from append-only ledger events, applies
normalization and inference catalogs, retains measurement history, derives
relationships from `RelationshipCatalog`, validates graph edges against the
relationship and entity-type catalogs, computes aliases, and detects conflicts.

For local network observation this means:

- durable multi predicates such as `ip_address` can have multiple current
  values;
- single-valued measurement predicates keep limited history according to the
  projector's measurement history limit;
- relationship projection is entirely catalog-driven;
- state projection does not collect fresh observations, call providers, probe
  networks, run tools, mutate hosts, or infer reachability unless explicit facts
  and catalog rules say so.

No `StateProjector` change is needed for the first local network source. The new
observations should enter as ordinary observations and become observed facts.
The only required code changes for implementation should be collection logic and
predicate catalog entries.

## Current Impact Output

The impact view is a read-only projection summary. It currently includes:

- canonical entity name;
- entity types;
- aliases;
- `availability_status`, defaulting to `unknown` when no fact exists;
- `local_observation_status`, defaulting to `unknown` when no fact exists;
- endpoint availability by role;
- groups;
- dependencies and dependents;
- active conflicts;
- graph issues.

The impact view must not become a network scanner. Local Network Observation v1
adds a display-only `local network configuration` section that renders projected
facts already present in State. It does not collect data, execute tools, probe
endpoints, or alter projection semantics. The view preserves
`availability_status: unknown` when no separate scoped availability evidence
exists.

## Observation Ingestion Pattern

The current ingestion pattern is appropriate for the proposed extension:

1. an `ObservationSource` returns validated `Observation` instances;
2. `ObservationCollectionService` collects all observations before appending any
   events;
3. source metadata is added during collection;
4. the normalization pipeline runs;
5. `ObservationIngestor` appends observation, evidence, and derived fact events;
6. `StateProjector` later projects those facts into current state.

The implementation should keep using that path. It should not add side channels,
projector-specific collection hooks, shell execution, `Runtime` changes,
`ToolExecutor` changes, or provider dependencies.

## Local-Only Network Facts Available Without Network Calls

The following facts can be observed from the local OS without sending packets to
neighbors or relying on Prometheus.

| Fact | Safe local source | Recommended predicate | Subject | Value | Dimensions / metadata | Meaning | Must not imply |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Interface exists | `/sys/class/net`, `socket.if_nameindex()` | `network_interface` | local host | interface name | `interface`, `source_path` | The local OS exposes an interface name. | Link is up, carrier exists, address assigned, host reachable. |
| Interface operational state | `/sys/class/net/<iface>/operstate` | `interface_operstate` | local host | enum such as `up`, `down`, `unknown`, `dormant`, `lowerlayerdown`, `notpresent`, `testing` | `interface`, `source_path` | Kernel-reported operational state. | Neighbor reachability, gateway reachability, internet access. |
| Interface administrative flags | `fcntl.ioctl(SIOCGIFFLAGS)` via stdlib `socket`/`fcntl` on Unix, or omit initially | future `interface_admin_state` only if needed | local host | `up` / `down` / `unknown` | `interface`, `flags` | Whether admin `IFF_UP` flag is set. | Carrier or route health. |
| Assigned IP address | `socket` + `fcntl.ioctl(SIOCGIFADDR)` for IPv4 where available; `/proc/net/if_inet6` for IPv6; `psutil` is not stdlib and should not be used | existing `ip_address` | local host | IP literal | `interface`, `address_family`, optional `prefix_length`, `scope` | Address configured locally. | Address is reachable externally, interface is healthy, subnet has neighbors. |
| IPv6 address and prefix | `/proc/net/if_inet6` | existing `ip_address` plus metadata | local host | IPv6 literal | `interface`, `address_family=ipv6`, `prefix_length`, `scope`, `flags` | IPv6 address configured locally. | Global internet reachability or neighbor presence. |
| Default route / gateway | `/proc/net/route` for IPv4; `/proc/net/ipv6_route` for IPv6 where practical | `default_gateway` | local host | gateway IP or route marker | `interface`, `address_family`, optional route flags/metric | Local routing table has a default route entry. | Gateway responds, gateway exists, packets can leave, internet works. |
| DNS resolver | `/etc/resolv.conf` nameserver lines; optionally systemd-resolved stub config only if read as a local file | `dns_resolver` | local host | resolver IP | `source_path`, `order`, optional `interface` only if explicitly scoped by source | Resolver configured for this host/process environment. | DNS queries succeed, resolver reachable, internet works. |
| Search domains | `/etc/resolv.conf` search/domain lines | future `dns_search_domain` only if needed | local host | domain | `source_path`, `order` | Local resolver search configuration. | Zone exists or DNS resolution works. |
| Local network segment/prefix | Interface address plus prefix if prefix is safely available from `/proc/net/if_inet6` or netlink-like local files; IPv4 prefix is hard with stdlib only unless parsing `/proc/net/route` masks | future `local_network_segment` only if confidence is high | local host | CIDR prefix | `interface`, `address_family`, `derived_from=local_address_and_prefix` | A locally configured address belongs to a configured prefix. | Neighbor existence, subnet occupancy, gateway reachability. |
| Neighbor table entries | `/proc/net/arp` or `/proc/net/ndisc_cache` if present | do not implement first | local host | none in first step | N/A | Local cache may contain stale/passive entries. | Neighbor existence or reachability. |

## Python Stdlib and proc/sysfs Safety

### Safe for first implementation

Use only Python standard library and local files:

- `socket.if_nameindex()` for interface names where available;
- `/sys/class/net` for Linux interface names and operational state;
- `/sys/class/net/<iface>/operstate` for Linux `interface_operstate`;
- `/proc/net/route` for Linux IPv4 default route and gateway;
- `/proc/net/if_inet6` for Linux IPv6 assigned addresses and prefix length;
- `/etc/resolv.conf` for configured DNS resolvers;
- `socket`, `struct`, and `fcntl` for Unix IPv4 interface address reads if the
  code is carefully gated by platform and does not call shell commands.

All file reads should be best-effort. Missing files, permission errors,
unsupported platforms, malformed lines, or unknown encodings should result in
omitting that specific observation and recording diagnostic metadata only if a
high-level status observation needs it. The collector should not fail the entire
local host observation because one optional network file is unavailable.

### Avoid in the first implementation

Avoid these in the smallest safe implementation:

- shell commands such as `ip`, `route`, `netstat`, `nmcli`, `scutil`, or
  `resolvectl`;
- subprocess execution;
- third-party packages such as `psutil`;
- raw netlink implementation unless Seed later needs more complete Linux
  support;
- DNS lookups;
- connecting UDP sockets to infer source addresses;
- opening TCP sockets;
- ICMP pings;
- ARP or neighbor discovery probes;
- HTTP calls;
- Prometheus calls.

## Existing Predicates That Can Be Reused

- Reuse `ip_address` for assigned local IP addresses.
- Reuse `local_observation_status` to show that local read-only observation ran.
- Do not reuse `availability_status` for local network facts.
- Do not reuse `ansible_host` or `prometheus_instance`; those are source-specific
  identity/provider predicates.

## New Narrow Predicates Needed

The smallest safe predicate additions are:

### `network_interface`

- Kind: durable fact.
- Value type: string.
- Cardinality: multi.
- Subject: local host.
- Value: interface name, for example `lo` or `eth0`.
- Dimensions: at minimum `interface=<name>`.
- Semantics: the local OS exposes an interface with this name.
- Negative space: does not imply the interface is administratively up,
  operationally up, has carrier, has an assigned address, or can reach anything.

### `interface_operstate`

- Kind: measurement.
- Value type: string.
- Cardinality: multi, dimensioned by interface.
- Expected local values include `up`, `down`, `unknown`, `dormant`,
  `lowerlayerdown`, `notpresent`, and `testing`, but the collector preserves
  local kernel strings rather than treating the list as exhaustive.
- Subject: local host.
- Dimensions: `interface=<name>` so each interface has its own measurement
  series.
- Semantics: kernel-reported operational state from local files.
- Negative space: does not imply neighbor reachability, gateway reachability, or
  internet access.

### `default_gateway`

- Kind: durable fact, or measurement if route churn should retain only current
  samples. Prefer durable fact initially only if multiple gateways/routes can be
  represented with dimensions and conflict behavior is acceptable.
- Value type: string.
- Cardinality: multi.
- Subject: local host.
- Value: gateway IP literal when present; for direct default routes without a
  gateway, use a documented marker only if such routes are intentionally
  supported.
- Dimensions: `interface=<name>`, `address_family=ipv4|ipv6`, optional `metric`.
- Semantics: local routing table contains a default route via this gateway.
- Negative space: does not imply the gateway exists, is reachable, forwards
  traffic, or provides internet access.

### `dns_resolver`, `dns_resolver_stub`, `dns_resolver_upstream`

- Kind: durable fact.
- Value type: string.
- Cardinality: multi.
- Subject: local host.
- Value: resolver IP literal from local resolver configuration.
- Dimensions/metadata: source path and optional order when supplied by the source.
- Semantics: `dns_resolver` preserves nameservers configured for the host/process resolver view, `dns_resolver_stub` identifies local loopback stub resolvers such as systemd-resolved's common `127.0.0.53`, and `dns_resolver_upstream` records non-loopback upstream nameservers when they are readable from local systemd-resolved resolver files.
- Negative space: none of these predicates implies the resolver is reachable, answers queries, forwards to the internet, or that DNS resolution works. Seed must not query DNS, call `resolvectl`, or execute commands to populate these facts.

### `interface_mac_address`

- Kind: durable fact.
- Value type: string.
- Cardinality: multi.
- Subject: local host.
- Value: MAC address literal from local sysfs.
- Dimensions: `interface=<name>`.
- Semantics: the local OS exposes this interface address value.
- Negative space: does not imply link carrier, neighbor presence, or
  reachability.

### `interface_mtu`

- Kind: durable fact.
- Value type: integer.
- Cardinality: multi.
- Subject: local host.
- Value: MTU integer from local sysfs.
- Dimensions: `interface=<name>`.
- Semantics: the local OS exposes this configured interface MTU.
- Negative space: does not imply path MTU, packet delivery, or reachability.

### Predicate to defer: `local_network_segment`

A `local_network_segment` predicate is useful but should be deferred unless the
implementation can obtain prefix lengths safely and consistently. It is easy to
mislead users into thinking a segment has discovered peers. If added later:

- Kind: durable fact.
- Value: CIDR prefix.
- Cardinality: multi.
- Dimensions: `interface`, `address_family`.
- Metadata: `derived_from=assigned_local_address_and_prefix`.
- Negative space: no neighbor existence, no subnet occupancy, no gateway
  reachability.

### Predicate to defer: `neighbor_reachability_status`

Do not add this in the first implementation. A local ARP/neighbor cache is not a
probe, but it is stale, platform-specific, and easy to overinterpret. If Seed
later models this, it should be a separate cache-observation source with values
such as `cached`, `stale`, `failed`, or `unknown`, and it still must not claim
current reachability without active evidence.

## Required Distinctions

Seed should keep the following concepts separate:

### Interface exists

Represent with `network_interface = <iface>` on the local host.

This is a local inventory fact: the OS exposed an interface name. It does not say
whether the interface is enabled, operational, connected, addressed, or useful.

### Interface administrative/operational state

Represent operational state with `interface_operstate`, dimensioned by
interface. Administrative state should not be conflated with operational state.
If admin state is required later, add a separate `interface_admin_state`
predicate based on the `IFF_UP` flag or a safe local file source.

Operational `up` means only that the local kernel reports the interface
operationally up. It is not evidence that any neighbor, gateway, endpoint, or the
internet is reachable.

### Assigned IP

Represent with the existing `ip_address` predicate, with metadata/dimensions
that preserve interface and address family.

An assigned IP means the address is configured locally. It is not evidence that
the address is routable from anywhere else, that duplicate address detection
succeeded unless explicitly observed, or that packets can be exchanged.

### Default route

Represent with `default_gateway` or a future narrower `default_route` predicate.
For the recommended minimal implementation, `default_gateway` is acceptable if
its semantics are explicitly local-route-table-only.

A default gateway means the local route table has a default route entry. It does
not mean the gateway responds to ARP, NDP, ICMP, TCP, DNS, or forwards traffic.

### DNS resolver

Represent with `dns_resolver` from resolver configuration files.

A DNS resolver fact means the local resolver configuration names a server. It
does not mean the resolver is reachable, healthy, recursive, authoritative, or
able to resolve any name.

### Local network segment

Represent only when a local address and a trustworthy prefix length are both
available. Prefer deferring this predicate until the collector can be precise.
If emitted, `local_network_segment` means local configuration places one local
address in that CIDR prefix.

It must not imply that the segment has other hosts, that the gateway is in that
segment, that broadcast or multicast works, or that scanning occurred.

### Neighbor reachability unknown

Represent by absence of a reachability predicate, not by inventing negative
facts. If a UI needs to display this, it should render `unknown` from missing
scoped evidence just as impact output currently renders missing availability as
`unknown`.

Do not emit `availability_status = unknown` for neighbors, gateways, DNS
resolvers, or internet access merely because local network facts were observed.
Unknown is the projection/display result of missing evidence, not a discovered
network fact.

## What Must Not Be Inferred

Local network observation must not infer any of the following:

- host availability;
- neighbor existence;
- neighbor reachability;
- gateway existence;
- gateway reachability;
- DNS resolver reachability;
- successful DNS resolution;
- internet access;
- service availability;
- endpoint health;
- Prometheus visibility;
- remote inventory truth;
- subnet occupancy;
- path MTU or packet delivery;
- whether the local host is reachable from another observer.

Specifically:

- interface `operstate=up` must not become `availability_status=up`;
- assigned `ip_address` must not become endpoint availability;
- `default_gateway` must not become gateway reachability or internet access;
- `dns_resolver`, `dns_resolver_stub`, and `dns_resolver_upstream` must not become DNS availability;
- interface `ip_address` must not become network reachability;
- `local_network_segment` must not become neighbor existence;
- lack of any local fact must not become `down`.

## Recommended Smallest Safe Implementation

When implementation begins, keep the change small and scoped:

1. Extend `LocalHostObservationSource.collect()` with helper methods that read
   only local stdlib/proc/sysfs data.
2. Continue emitting `local_observation_status = observed` with the existing
   negative-space metadata.
3. Add `network_interface` observations for interface names discovered via
   `socket.if_nameindex()` and/or `/sys/class/net`.
4. Add `interface_operstate` observations for Linux interfaces when
   `/sys/class/net/<iface>/operstate` is readable.
5. Add `ip_address` observations for local assigned addresses that can be read
   safely from stdlib/proc files, preserving interface and address family in
   dimensions or metadata.
6. Add `default_gateway` observations from local route table files only.
7. Add `dns_resolver` observations from local resolver configuration only.
8. Add catalog entries only for `network_interface`, `interface_operstate`,
   `interface_mac_address`, `interface_mtu`, `default_gateway`, and
   `dns_resolver`; reuse existing `ip_address`.
9. Do not add new relationships, entity types, `Runtime` behavior,
   `ToolExecutor` behavior, shell execution, Prometheus dependency, or network
   calls.
10. Keep tests focused on emitted observations, metadata, no-shell/no-network
    invariants, and ingestion through the existing observation pipeline.

## Suggested Test Cases for Future Implementation

- `LocalHostObservationSource` emits deterministic network interface facts when
  stdlib/sysfs readers are monkeypatched.
- Missing `/sys`, `/proc`, or `/etc/resolv.conf` files do not fail collection.
- No subprocess APIs are called.
- No `urlopen`, socket connect, DNS lookup, or other network call is made.
- `interface_operstate` is dimensioned by interface so measurements for `lo` and
  `eth0` do not conflict.
- `ip_address` observations include interface and address-family metadata.
- Ingested local network facts do not create `availability_status` facts.
- Impact output continues to show `availability_status: unknown` unless a
  separate scoped availability fact exists.
- Catalog validation accepts new predicates and preserves multi-valued behavior
  where needed.

## Final Recommendation

Extend `LocalHostObservationSource`, not a new Prometheus-like provider, because
the desired facts are local host facts and the existing source already carries
the correct safety contract. Add only the narrow predicates necessary to name
local interfaces, interface operational state, configured default gateways, and
configured DNS resolvers. Reuse `ip_address`. Defer local network segments and
neighbor cache modeling until Seed has explicit vocabulary and UI language for
configuration-derived topology versus reachability evidence.

The guiding rule should be: **local configuration is evidence of local
configuration only**. Reachability, availability, neighbor existence, gateway
health, DNS success, and internet access require separate scoped evidence.


## Relationship to Hostname / Identity Observation v1

Local Network Observation remains topology/configuration observation, not identity
management or reachability verification. Hostname / Identity Observation v1 now
provides first-class local identity facts (`hostname`, `machine_id`, `boot_id`,
and, only when explicitly configured locally, `fqdn`) before network topology is
interpreted. Network interface, address, route, and resolver facts should attach
to the observed local host identity but must not create availability, DNS
success, endpoint reachability, provider visibility, or ownership claims.

## Local Network Observation v1 Implementation

Local Network Observation v1 follows the Capability Extension Methodology:

| Methodology step | v1 choice |
| --- | --- |
| Capability Gap | Seed lacked local network configuration facts. |
| Required Questions | What interfaces, addresses, default gateways, and DNS resolvers are configured locally? |
| Narrowest Facts | `network_interface`, `interface_operstate`, `interface_mac_address`, `interface_mtu`, `ip_address`, `default_gateway`, `dns_resolver`, `dns_resolver_stub`, `dns_resolver_upstream`. |
| Least-Privileged Source | Python stdlib plus local read-only files: `socket.if_nameindex()`, `/proc/net/dev`, `/proc/net/route`, `/proc/net/if_inet6`, `/sys/class/net/*/{operstate,address,mtu}`, and `/etc/resolv.conf`. |
| Read-Only Observation | `LocalHostObservationSource` reads local files/APIs only and marks observations as local-only, read-only, no-probe, no-subprocess, and no-privilege-escalation. |
| Observation → Evidence → Fact | The existing `ObservationCollectionService` and `ObservationIngestor` convert observations into evidence-backed facts. |
| Inference | None added. Local network facts do not infer availability or reachability. |
| User Query | `--current-facts` and `--impact HOST` render projected configuration facts without claiming reachability. |

### Predicates Added in v1

- `network_interface`: local OS exposed an interface name.
- `interface_operstate`: local kernel-reported operational state, dimensioned by interface.
- `interface_mac_address`: locally configured interface MAC address, dimensioned by interface.
- `interface_mtu`: locally configured interface MTU, dimensioned by interface.
- `default_gateway`: local IPv4 route table contains a default gateway, dimensioned by interface/family.
- `dns_resolver`: local resolver configuration names a DNS resolver.
- `dns_resolver_stub`: local resolver configuration names a loopback stub resolver.
- `dns_resolver_upstream`: readable local resolver configuration names a non-loopback upstream resolver.

The existing `ip_address` predicate is reused for configured IPv4 and IPv6
addresses. Address observations are dimensioned by interface and address family.

### Negative Space Preserved

These configuration facts do **not** imply any of the following:

- gateway reachability;
- DNS functionality;
- internet access;
- neighbor existence;
- remote host existence;
- Prometheus reachability;
- host availability.

No `availability_status` fact is emitted or inferred by Local Network
Observation v1. Availability remains a separate concept requiring separate
scoped evidence.

### Execution Boundary

Local Network Observation v1 does not add Runtime behavior, ToolExecutor
behavior, scheduling, retries, orchestration, shell commands, subprocess
execution, privilege escalation, network scans, DNS queries, pings, ARP probes,
endpoint checks, Prometheus calls, or other network connections.
