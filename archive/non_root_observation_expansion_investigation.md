# Non-root Observation Expansion Investigation

## Purpose and boundary

This investigation asks what a permanently non-root Seed can still learn before
pursuing elevated visibility. It is an understanding document only: it does not
implement observers, recommend root access, recommend Docker socket access,
recommend capability acquisition, change deployment boundaries, or alter
observation behavior.

Repository authority used here is implementation evidence from observation
sources, observation inventory, projection shape, capability-need and
capability-relationship surfaces, plus related repository investigations.

## Repository evidence reviewed

- `observation_inventory` discovers observation providers from Python classes
  with `collect()` and predicates from observation construction sites. Its
  metadata states that providers are discovered under `seed_runtime/`, predicates
  from `Observation(predicate=...)` or provider helper calls, and families from
  predicate prefixes.
- Projection shape shows observations enter through event replay, then inference
  consumes current observed facts, predicate catalog, inference catalog, and alias
  resolver; inference produces inferred facts while explicitly not changing the
  event ledger or observed facts.
- Local host observation is explicitly read-only, local-only, non-escalating,
  and does not execute shells or subprocesses.
- Capability pressure currently names listener/process/container and storage
  export evidence needs, but capability relationship intentionally reports
  access/benefit/pressure with `attainability="unknown"` and
  `expectation="unknown"`.

## Current observation domains

The implementation-backed observation inventory currently exposes these broad
observation domains:

| Domain | Classification | Evidence | Conservative interpretation |
| --- | --- | --- | --- |
| Local host identity | observed | `hostname`, `machine_id`, `boot_id`, and local FQDN predicates are emitted from local files / platform state. | Seed can learn locally configured identity evidence without DNS, reachability, or uniqueness assertions. |
| Local host substrate | observed | Kernel, CPU, memory, OS, architecture, and root disk usage predicates are collected. | Seed can learn locally reported substrate facts, not health or adequacy. |
| Filesystem and storage topology | observed | Mounts, mount source parts, mounted devices, partitions, block devices, filesystem type, filesystem size/availability, and remote mount source components are in the inventory. | Seed has non-root local mount/proc/sysfs visibility and some Prometheus-derived filesystem measurements. |
| Local listeners | partially_observed | Listener address/protocol/port/scope and non-root socket facts are collected; process ID/name appears only when directly linkable from visible procfs socket inodes. | Seed has non-root listener inventory but not complete listener process ownership. |
| Network interfaces and local addressing | partially_observed | Interface name/MAC/MTU/operstate/role, IP address, default gateway, and DHCP assignment evidence are collected. | Seed has interface/address/default-route evidence, but not neighbor tables, ARP/NDP cache, full route tables, or link-layer discovery evidence. |
| DNS and name configuration | partially_observed | Resolvers, systemd-resolved stub/upstream resolvers, `/etc/hosts` address/name/alias mappings, hostname, and FQDN are collected with boundary metadata. | Seed sees local configuration evidence, not DNS query results, resolver cache state, DNS validity, or reachability. |
| Local users, groups, packages | observed | `/etc/passwd`, `/etc/group`, supplementary group membership, and dpkg package observations are collected. | Seed can learn local account/package declaration evidence without asserting ownership or policy. |
| systemd unit inventory | partially_observed | A systemd source records unit identity, runtime state, substate, and unit-file enablement state while disclaiming health, ownership, intent, dependencies, and desired state. | Seed has some service-manager visibility but not full service ownership or causality. |
| Ansible inventory | observed | Ansible inventory emits imported host and group predicates. | Seed can learn declared inventory topology when supplied, not runtime truth. |
| Prometheus-derived endpoint/filesystem topology | partially_observed | Prometheus source safely queries `up`, `node_uname_info`, and node filesystem metrics; it emits endpoint role, `up`, OS, and filesystem size/availability. | Seed can learn provider-reported monitoring samples, but existing docs flag endpoint/host identity-routing limits. |
| Repository/VCS observation | partially_observed | Repository observation and history surfaces report repository health, VCS, head commit, branch, and snapshot comparison context. | Useful for Seed's own operational history, not host/environment topology. |
| Observation shape itself | observed | Observation inventory and utilization surfaces expose providers, predicates, families, and consumers. | Seed can see what it currently observes; this is meta-observation rather than environment observation. |

## Domains partially explored

### Listener and process attribution

The repository already distinguishes local listener evidence from listener
process ownership. Non-root listener observations include socket/protocol/address
/port/scope and attribution-status predicates. Capability needs only retain
`listener_process_inventory` pressure for service owner-not-observed conflicts
when listener process ID/name evidence is absent. This means the pressure is a
missing-evidence pressure inside an already explored listener domain, not proof
that the entire non-root observation space is exhausted.

### Containers and port mapping

Container inventory and container port mapping appear primarily as capability
needs attached to ownership discrepancies. The observation inventory does not
show a container observation family. Current repository knowledge therefore
supports `unobserved` for container runtime facts in the implemented observation
inventory, while `capability_relationship` keeps attainability and expectation
unknown. This is missing category evidence for current non-root observation, not
an instruction to acquire Docker visibility.

### Network configuration

Seed observes network interfaces, IP addresses, interface roles, default gateway,
and some address-assignment evidence. It does not appear to observe neighbor
tables, ARP/NDP cache, full routing table entries, DNS cache/resolver runtime
state, mDNS, LLDP, CDP, service discovery advertisements, or known SSH hosts.
This is a broad partially explored domain: local network configuration exists;
adjacent non-root-readable network context appears absent from repository
observation knowledge.

### DNS / resolver / hosts-file evidence

DNS configuration is partially observed through resolver configuration,
systemd-resolved configuration files, and `/etc/hosts`. The implementation
explicitly avoids treating local identity and hosts-file evidence as DNS truth,
resolution, reachability, host uniqueness, alias equivalence, endpoint identity,
or ownership. That is a healthy boundary, but it also means runtime resolver
state, DNS query evidence, and resolver-cache evidence remain unexplored or
unknown in the repository.

### Mount provenance and storage ownership

Mount and block-device observation are comparatively rich. Storage capability
pressure still names `mount_source`, export visibility, NFS export, SMB share,
and remote storage export evidence. That suggests local mount provenance is
partially explored, while remote export-side evidence remains absent or outside
current non-root local observation knowledge.

### Prometheus-derived topology

Prometheus is an implemented provider domain, but the repository contains prior
investigations warning that Prometheus `instance` values and
`prometheus_instance` relationships can blur endpoint and host identity. The
current implementation partly suppresses promotion for endpoint-subject OS facts
and limits safe queries, but Prometheus-derived topology remains partially
explored because identity, monitored-entity scope, and filesystem subject scope
are still bounded concerns.

## Observation domains that appear unobserved or absent

The following classifications are conservative and based on repository evidence,
not usefulness assumptions:

| Potential domain | Classification | Evidence status | Missing evidence vs missing category |
| --- | --- | --- | --- |
| Neighbor tables / ARP / NDP cache | unobserved | No observation family or predicate appears for neighbors, ARP, or NDP in observation inventory. | Missing category of evidence. |
| Full routing tables / per-route provenance | partially_observed | `default_gateway` exists; route-table families do not appear. | Missing category beyond default route. |
| DNS resolver cache/runtime state | unobserved | Resolver configuration predicates exist; cache/runtime-state predicates do not appear. | Missing category of evidence. |
| DNS query results | unobserved | Implementation explicitly avoids DNS resolution assertions for hostname/hosts-file evidence. | Missing category; not missing proof inside existing DNS config observation. |
| mDNS / DNS-SD / Avahi / service discovery | unobserved | No mDNS, DNS-SD, Avahi, or service-discovery predicates/providers appear in inventory evidence. | Missing category of evidence. |
| LLDP / CDP link-layer neighbor evidence | unobserved | No LLDP or CDP predicates/providers appear in inventory evidence. | Missing category of evidence. |
| Known SSH hosts / SSH client config | unobserved | SSH appears in unrelated tests/docs, but no implemented observation family for known hosts or SSH config appears. | Missing category of evidence. |
| Environment metadata | unknown | Process-local environment observation is not apparent in inventory; repository may intentionally avoid env capture for sensitivity, but evidence reviewed here does not establish policy. | Unknown category; open question. |
| Cloud/provider metadata endpoints | unobserved | No provider-metadata observation provider appears in inventory. | Missing category of evidence. |
| Container runtime inventory | unobserved | Capability needs mention container inventory/port mapping; observation inventory lacks container predicates. | Missing category in observations; missing evidence in ownership diagnostics. |
| Elevated process inventory | partially_observed | systemd unit state and non-root listener process attribution exist; full process inventory does not appear. | Missing evidence within service ownership and missing category for generic process observation. |
| Remote storage exports | unobserved | Capability needs name NFS/SMB/remote export inventory; inventory shows local mount source parts, not export-side inventories. | Missing category of evidence. |
| Firewall/NAT rules | unobserved | No firewall, nftables, iptables, pf, NAT, or packet-filter predicates appear. | Missing category of evidence. |
| Local open files / sockets beyond listeners | unobserved | Listener sockets are observed; general open-file or connection-state inventory does not appear. | Missing category of evidence. |

## Observation-space gaps

1. **Current pressure is concentrated around ownership attribution.** The
   capability-need table connects service ownership discrepancies to local
   listener, process, container, and container-port evidence, and storage
   ownership discrepancies to mount-source/export evidence. This can make root,
   Docker, and elevated process visibility feel like the only next options, but
   that is a pressure-shaped view rather than a complete observation-space map.

2. **Implemented non-root observation is broader than the pressure points.** The
   local host source already observes identity, host substrate, filesystems,
   mounts, block devices, network interfaces, DNS configuration, hosts-file
   configuration, users/groups, packages, listeners, and systemd units.

3. **Several non-root-readable categories appear absent.** Neighbor tables,
   route-table detail, resolver runtime state, service discovery, link-layer
   discovery, SSH known-host evidence, provider metadata, firewall/NAT state,
   and environment metadata are not represented in the implementation-backed
   observation inventory reviewed here.

4. **Some pressure is missing evidence inside explored categories.** Listener
   process attribution is not the same as listener inventory: Seed already sees
   listeners but not always their owning processes. Mount provenance is similar:
   Seed sees local mount facts but not remote export authority.

5. **Some pressure is missing categories of evidence.** Container inventory,
   container port mappings, remote storage exports, and generic process inventory
   do not appear as observed inventory families. These are not merely missing
   facts inside an existing observer; they are absent categories in the current
   observation inventory.

## Supported conclusions

- Seed has **not exhausted non-root observation opportunities**. Repository
  evidence shows broad existing non-root observation, but also absent categories
  that may be non-root-readable depending on platform and policy.
- Current operational pressure is partly caused by **missing visibility inside
  explored domains**: listener process attribution, systemd/service ownership,
  and mount/export provenance.
- Current operational pressure is also partly caused by **unexplored categories
  of observation**: container runtime facts, route/neighbor detail, resolver
  runtime state, service discovery, link-layer discovery, SSH known-hosts,
  provider metadata, firewall/NAT state, and remote storage export evidence.
- Capability relationship visibility is correctly not an acquisition decision:
  implementation sets attainability and expectation to unknown and frames
  pressure as visibility context.

## Unsupported conclusions

- It is unsupported to conclude that Seed should acquire root visibility.
- It is unsupported to conclude that Seed should acquire Docker socket access.
- It is unsupported to conclude that any absent domain is useful, safe, stable,
  portable, or worth implementing.
- It is unsupported to conclude that Prometheus-derived host/endpoint topology is
  authoritative host identity.
- It is unsupported to conclude that local DNS/hosts-file configuration proves
  DNS truth, reachability, ownership, or endpoint identity.
- It is unsupported to conclude that permanently non-root observation can solve
  all ownership discrepancies.

## Open questions

1. Which absent categories are intentionally excluded for privacy, portability,
   or safety rather than simply unexplored?
2. Which absent categories are reliably readable by a permanently non-root Seed
   across supported platforms?
3. Should observation inventory eventually distinguish environment topology
   domains from operational/meta-observation domains?
4. Can repository knowledge represent neighbor/route/resolver/service-discovery
   observations without promoting presentation vocabulary into preserved
   knowledge?
5. Are current ownership discrepancies better reduced by additional non-root
   categories, by better use of existing observations, or by accepting persistent
   unknowns?
6. For Prometheus-derived topology, what additional non-root evidence would keep
   endpoint, target, host, filesystem, and monitored-entity scopes separate?

## Final answer to acceptance questions

### Has Seed exhausted non-root observation opportunities?

No. The repository has substantial non-root observation, but the
implementation-backed inventory and related docs do not show neighbor tables,
full routes, resolver runtime state, mDNS/DNS-SD, LLDP/CDP, known SSH hosts,
provider metadata, firewall/NAT state, remote export inventories, or generic
container runtime observations.

### What observation domains remain unexplored?

The strongest unexplored or absent domains are neighbor/ARP/NDP, detailed
routing, DNS resolver runtime/cache/query state, service discovery, link-layer
neighbors, known SSH hosts, environment metadata, provider metadata, container
runtime inventory, container port mappings, firewall/NAT rules, remote storage
exports, and generic process/open-file/socket state beyond listener attribution.

### Are current operational pressures caused by missing visibility or unexplored categories?

Both. Listener process attribution and mount/export provenance are missing
visibility inside partially explored domains. Container runtime facts,
container-port mappings, remote export-side facts, and several network/resolver
/service-discovery categories appear to be unexplored observation categories in
current repository knowledge.
