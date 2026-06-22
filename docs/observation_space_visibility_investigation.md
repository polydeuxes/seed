# Observation-space Visibility and Domain Reasoning Investigation

## Purpose and boundary

This investigation asks whether Seed can reason about observation space itself,
rather than only about individual predicates or capability needs. It is an
understanding document only. It does not implement observers, recommend root or
Docker access, recommend a final domain taxonomy, create an inventory system,
create diagnostics, change deployment policy, or acquire capabilities.

Repository authority used here is implementation-backed evidence from current
observation and reasoning surfaces, plus prior repository investigations. Where
this document groups predicates into domains, those groups are candidate
reasoning aids, not implemented repository truth.

## Repository evidence reviewed

- `observation_inventory` discovers providers from Python classes under
  `seed_runtime/` that implement `collect()`. It discovers predicates from AST
  string literals passed to `Observation(predicate=...)` or provider helper
  calls, then derives `families` from predicate prefixes before the first
  underscore.
- Current inventory reports seven providers: `ansible_inventory`, `fake`,
  `json`, `local_host`, `prometheus`, `repository_source`, and `systemd`.
- Current inventory families include host identity/substrate predicates,
  filesystem and block predicates, listener predicates, interface/address/DNS
  predicates, local account/group/package-adjacent predicates, systemd unit
  predicates, Prometheus endpoint/up/filesystem predicates, and repository/VCS
  predicates.
- `observation_utilization` audits individual discovered predicates through
  collection, projection, read-model access, and diagnostic consumption. Its
  unit of reasoning is still the predicate, not a domain.
- `capability_needs` derives pressure from current ownership discrepancies and
  recorded diagnostic capability-need facts. Its entries are capability names,
  affected subjects, diagnostics, and needed evidence.
- `capability_relationship` explains current access, operational benefit,
  pressure, attainability, expectation, reasoning, and limitations for
  capability needs. It intentionally keeps attainability and expectation
  `unknown`.
- `operational_story` composes existing pressure, capability, privilege,
  correlation, impact, and investigation-path surfaces into an operational
  narrative. It does not currently explain observation-domain coverage.
- `projection_shape` exposes how observations enter projection and how inferred
  facts are produced without changing the event ledger or observed facts.
- `non_root_observation_expansion_investigation` concluded that Seed has not
  exhausted non-root observation opportunities and distinguished missing
  evidence inside explored domains from missing categories of evidence.

## Current evidence shape

Seed already has repository-visible self-knowledge about **what individual
predicates are collected** and **where those predicates are used**. The current
shape is:

| Surface | Implemented unit of reasoning | What it can answer | What it does not answer |
| --- | --- | --- | --- |
| `observation_inventory` | provider, predicate, prefix-derived family | Which providers and predicates exist? | Which higher-level observation domains exist or are absent? |
| `observation_utilization` | predicate | Is a collected predicate projected, readable, or diagnostically consumed? | Is a whole domain observed, partial, absent, or unknown? |
| `capability_needs` | capability need | What evidence is needed by diagnostics? | Whether pressure is inside an explored domain or caused by an absent domain. |
| `capability_relationship` | capability need | What access/benefit/pressure relationship is visible? | What observation domain the capability belongs to. |
| `operational_story` | operational narrative | What pressure and investigation context exists now? | Observation-space coverage or domain-level gaps. |
| `projection_shape` | projection stage | How observations influence projection. | Observation-domain coverage. |

This means Seed can currently answer predicate and capability questions better
than domain-coverage questions.

## Candidate observation domains

The table below groups current inventory evidence into candidate domains. The
classifications are conservative and implementation-backed only.

| Candidate domain | Classification | Supporting evidence | Interpretation |
| --- | --- | --- | --- |
| Local host identity | observed | `hostname`, `fqdn`, `machine_id`, and `boot_id` predicates appear in inventory families. | Seed observes local identity declarations and identifiers, without proving uniqueness, reachability, or ownership. |
| Local host substrate | observed | `kernel_release`, `kernel_version`, `os`, `architecture`, `cpu_count`, `cpu_model`, `memory_total_bytes`, and root disk byte predicates appear. | Seed observes local platform/substrate facts. |
| Filesystems, mounts, partitions, and block devices | observed | `filesystem_*`, `mount_*`, `mounted_device`, `partition`, and `block_device*` predicates appear. | Local storage and mount-side evidence is comparatively rich. Export-side authority remains separate. |
| Local listeners and socket attribution | partially_observed | `listener_*` and `listening_*` predicates appear, including process ID/name and attribution-status predicates. | Seed observes listener endpoints and some attribution, but current capability pressure shows attribution can still be missing. |
| Network interfaces and local addressing | partially_observed | `network_interface`, `interface_*`, `ip_address`, `address_assignment_method`, and `default_gateway` predicates appear. | Interface, address, and default-gateway evidence exist; neighbor tables and full routing evidence do not appear. |
| DNS and hosts-file configuration | partially_observed | `dns_resolver`, `dns_resolver_stub`, `dns_resolver_upstream`, `hosts_file_address_mapping`, `hosts_file_name`, and `hosts_file_alias` predicates appear. | Seed sees local resolver/hosts configuration, not DNS query truth, cache state, reachability, or authority. |
| Users and groups | observed | `user_*`, `group`, `group_account`, `group_gid`, and `group_member` predicates appear. | Local account and group declaration evidence is visible. |
| systemd unit inventory | partially_observed | `systemd_unit` and `systemd_unit_file_state` predicates appear from the systemd provider. | Unit presence/state evidence exists, but service intent, ownership, dependencies, and causality are not established by the predicate names alone. |
| Prometheus endpoint/filesystem topology | partially_observed | Prometheus provider contributes `up`, `endpoint_role`, `node_uname_info`-derived host/substrate predicates, and filesystem metrics in existing investigations. | Monitoring samples are visible, but endpoint/host identity and subject-scope boundaries remain constrained. |
| Ansible inventory topology | observed | `ansible_inventory` is a provider, and prior investigation records imported host/group predicates. | Declared inventory can be observed when supplied; it is not runtime truth. |
| Repository/VCS operational context | partially_observed | `repository_source` is a provider and repository/history surfaces exist. | Useful for Seed's own operational context, not environment topology. |
| Observation shape/meta-observation | observed | `observation_inventory` and `observation_utilization` expose providers, predicates, families, and predicate use. | Seed can observe its observation implementation shape at predicate granularity. |
| Container runtime | unobserved | Capability needs mention `container_inventory` and `container_port_mapping`, while current inventory families do not include container predicates. | This is a missing category in current observation inventory, not merely a missing fact from a container observer. |
| Remote storage exports | unobserved | Capability needs name export-side evidence, while inventory shows local mount-source facts but no NFS/SMB/export provider family. | Local mount evidence is observed; remote export authority appears absent. |
| Neighbor tables / ARP / NDP | unobserved | No neighbor, ARP, or NDP family/predicate appears in current inventory. | Missing category of evidence. |
| Full routing table | partially_observed | `default_gateway` exists, but no route-table family appears. | Default route evidence exists; broader route topology appears absent. |
| Runtime DNS cache/query results | unobserved | Resolver configuration predicates exist, but no cache/query-result predicates appear. | Missing domain beyond observed DNS configuration. |
| Service discovery and link-layer discovery | unobserved | No mDNS, DNS-SD, Avahi, LLDP, CDP, or link-layer discovery predicates appear. | Missing category of evidence. |
| Provider/cloud metadata | unobserved | No provider metadata family/provider appears in inventory evidence reviewed. | Missing category of evidence. |
| Firewall/NAT state | unobserved | No firewall, nftables, iptables, NAT, or packet-filter predicates appear. | Missing category of evidence. |
| Process/open-file inventory beyond listener attribution | partially_observed | Listener process ID/name may be observed; generic process or open-file inventory does not appear. | Missing evidence exists inside listener attribution, and a broader process/open-file category appears absent. |
| Environment metadata | unknown | No environment metadata family is visible in current inventory, but repository evidence reviewed here does not establish whether this is intentional policy or simply absent. | Classification should remain unknown without policy/implementation evidence. |

## Pressure-to-domain relationships

Current operational pressure can be connected to candidate domains, but only by
investigation, not by an implemented domain model.

| Pressure / capability evidence | Candidate domain relationship | Gap type | Supported interpretation |
| --- | --- | --- | --- |
| `listener_process_inventory` pressure from ownership diagnostics | Local listeners and process attribution | Missing evidence inside a partially observed domain | Seed observes listener endpoints, but not enough process attribution for some ownership questions. |
| `container_inventory` pressure | Container runtime | Missing observation domain/category | Capability pressure names container evidence, while no container observation family appears in current inventory. |
| `container_port_mapping` pressure | Container runtime and listener attribution | Missing observation domain/category | The pressure bridges listener ownership with absent container-port evidence. |
| `mount_source`, NFS export, SMB share, or remote export evidence pressure in prior investigation | Filesystems/mounts plus remote storage exports | Both: missing evidence inside local mount provenance and missing export-side category | Seed observes local mount facts, but export-side authority is not represented as an observed domain. |
| Prometheus endpoint/host identity concerns | Prometheus topology and host identity | Missing evidence inside a partially observed domain | Prometheus observations exist, but endpoint, target, host, filesystem, and monitored-entity scopes require careful boundaries. |
| Route/neighbor/resolver/service-discovery absence from non-root investigation | Network configuration and discovery domains | Missing observation domains/categories | Interface/address/default-gateway/DNS config exists; adjacency, route-detail, resolver-runtime, and discovery evidence appear absent. |

This mapping shows operational pressure can be related back to observation-space
coverage, but the relation is not currently first-class. It must be inferred from
predicate inventory, capability names, diagnostics, and investigation documents.

## Missing evidence versus missing domain

The distinction is repository-visible and important:

- **Missing evidence in an observed or partially observed domain** means Seed has
  at least some observer/predicate coverage for the domain, but a diagnostic or
  reasoning path lacks a specific fact. Listener process attribution is the
  clearest example: listener predicates exist, but process attribution can remain
  absent or insufficient.
- **Missing observation domain/category** means current inventory does not expose
  provider/predicate evidence for the kind of observation at all. Container
  runtime inventory, neighbor tables, link-layer discovery, provider metadata,
  and firewall/NAT state are examples under current evidence.
- **Unknown** should be used when absence from inventory is not enough to know
  whether a category is intentionally excluded, unsafe, outside product scope, or
  merely unexplored. Environment metadata is the conservative example.

Seed can support this distinction today through manual repository investigation,
but current surfaces do not answer it directly.

## Can current inventory be grouped into domains?

Yes, cautiously. Existing predicate families and provider names provide enough
implementation evidence to group predicates into candidate domains such as host
identity, substrate, storage, listeners, network configuration, DNS
configuration, users/groups, systemd, Prometheus topology, repository context,
and observation meta-shape.

However, current `families` are mechanically derived from predicate prefixes.
They are useful evidence, but they are not the same as domain semantics. For
example, `default_gateway` becomes family `default`, while it is more naturally
part of a routing/network domain. `listening_*` and `listener_*` are separate
families but likely the same candidate listener domain. Domain grouping is
therefore feasible as an investigation practice, but not yet an implemented
repository concept.

## Can domains be classified systematically?

Partially. The classification vocabulary is supportable if it remains tied to
implementation evidence:

- `observed`: inventory contains providers/predicates that cover the candidate
  domain well enough for a conservative local-evidence statement.
- `partially_observed`: inventory contains some predicates in the domain, but
  repository pressure, explicit boundaries, or missing adjacent predicate
  families show incomplete coverage.
- `unobserved`: inventory and reviewed implementation evidence show no provider
  or predicate category for the candidate domain, while capability pressure or
  prior investigation identifies it as a distinct evidence category.
- `unknown`: evidence is insufficient to distinguish intentional exclusion,
  unsafe/unsupported scope, absent implementation, or naming mismatch.

This classification can be performed now by humans reading the repository, but
Seed does not currently have a first-class surface that performs it.

## Is observation domain a reusable reasoning primitive?

The evidence suggests yes, but only as an emerging concept. Observation domains
would let Seed answer questions that current predicate/capability surfaces cannot
answer directly:

- Which pressures are caused by incomplete coverage inside a known domain?
- Which pressures are caused by an entirely absent observation category?
- Which observed predicates are isolated facts versus members of a broader
  domain needed for reasoning?
- Which areas of non-root observation remain unknown without implying any
  acquisition path?
- Where should boundaries be stated so presentation vocabulary does not become
  projected knowledge accidentally?

The concept is reusable because the same domain grouping can connect inventory,
utilization, projection, capability pressure, operational story, and prior
investigations. The repository does not yet implement that connective layer.

## Supported conclusions

- Seed can currently reason about observation space **indirectly** through
  observation inventory, utilization, capability pressure, projection shape, and
  investigation documents.
- Seed does not currently expose observation-domain coverage as a first-class
  repository-visible concept.
- Current inventory can be grouped into higher-level candidate domains, but those
  domains are not repository-modeled semantics; they are investigation-derived
  groupings.
- Domain classifications of observed, partially observed, unobserved, and
  unknown are feasible when tied to implementation evidence.
- Operational pressure can be mapped back to observation-space gaps: some gaps
  are missing facts inside partially observed domains, while others are missing
  observation categories.
- Observation-space reasoning appears to be a missing form of repository
  self-knowledge because existing surfaces answer predicate/capability questions
  but not coverage/domain questions.

## Unsupported conclusions

- It is unsupported to conclude that any candidate domain in this document is the
  correct final taxonomy.
- It is unsupported to conclude that Seed should implement any observer named or
  implied here.
- It is unsupported to conclude that Seed should acquire root, Docker socket, or
  provider metadata access.
- It is unsupported to conclude that unobserved domains are safe, portable,
  useful, policy-approved, or worth prioritizing.
- It is unsupported to treat predicate-prefix families as authoritative domain
  semantics.
- It is unsupported to promote domain labels into preserved or projected
  knowledge without an implementation-backed model and boundary.

## Open questions

1. Should observation domains be represented at all, or are predicate/provider
   surfaces plus investigation documents sufficient?
2. If represented, should domains be curated, inferred from predicates,
   provider-declared, or a combination?
3. How should a domain model avoid turning presentation labels into repository
   knowledge without implementation evidence?
4. What evidence threshold distinguishes `observed` from
   `partially_observed`?
5. Should domain classification consider utilization/projection, or only
   collection inventory?
6. How should pressure be linked to domains without implying acquisition,
   prioritization, or policy recommendations?
7. Which absent categories are intentionally excluded for privacy, portability,
   safety, or deployment reasons?
8. Should meta-observation surfaces such as `observation_inventory` be treated as
   an observation domain, or as a separate self-knowledge layer?

## Acceptance answers

### Can Seed reason about observation space itself?

Yes, but currently only indirectly and incompletely. Repository evidence supports
manual observation-space reasoning by combining inventory, utilization,
capability pressure, projection shape, and investigations. Seed does not yet have
a direct domain-coverage surface.

### Can observation domains be treated as a repository-visible concept?

They can be treated as an emerging repository-visible concept for investigation
purposes. They are not yet an implemented repository primitive, and candidate
labels should not be treated as authoritative without a modeled source of truth.

### Can operational pressures be mapped back to observation-space coverage?

Yes. Listener process pressure maps to missing evidence inside a partially
observed listener/process-attribution domain. Container and container-port
pressure map to an absent container-runtime category. Mount/export pressure maps
to both local mount provenance gaps and absent export-side evidence. Network
adjacency/discovery gaps map to partially observed network configuration plus
unobserved neighbor/discovery domains.

### Is observation-space reasoning a missing form of repository self-knowledge?

Yes. Existing surfaces make Seed aware of providers, predicates, utilization,
capability needs, and operational pressure, but they do not directly explain
observation-domain coverage or distinguish missing facts inside observed domains
from missing domains entirely. That gap is a missing form of repository
self-knowledge, not a mandate to implement observers or acquire capabilities.
