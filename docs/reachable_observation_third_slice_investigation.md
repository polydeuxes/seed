# Reachable Observation Third-Slice Investigation

## Purpose

This characterization investigation identifies the best existing observation goal for demonstrating a fully `reachable` authority-aware observation outcome under this constraint profile:

| Capability / authority | Profile state |
| --- | --- |
| `root` | unavailable |
| `docker_socket_read` | unavailable |
| `active_network_probe` | unauthorized |
| `local_passive` | available |
| `external_provider_query` | unknown |

The investigation does not implement a new evaluator, CLI command, framework, planner, ontology, or authority model. It uses repository evidence from existing observation inventory, observation-domain, observation-permission, privilege-discovery, and diagnostic surfaces.

## Files inspected

- `seed_runtime/observation_inventory.py`
- `seed_runtime/observation_domains.py`
- `seed_runtime/observation_permission.py`
- `seed_runtime/privilege_discovery.py`
- `seed_runtime/capability_needs.py`
- `seed_runtime/ownership_discrepancies.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `docs/authority_aware_observation_reasoning_investigation.md`
- `docs/non_root_observation_expansion_investigation.md`
- `docs/listening_port_observation.md`
- `tests/test_observation_inventory.py`
- `tests/test_observation_domains.py`
- `tests/test_observation_permission.py`
- `tests/test_privilege_discovery.py`
- `tests/test_ownership_discrepancies.py`
- `tests/test_diagnostic_inventory.py`
- `tests/test_diagnostic_shape_audit.py`

## App commands run

```text
python scripts/seed_local.py --observation-inventory --json
python scripts/seed_local.py --observation-domains --json
python scripts/seed_local.py --observation-permission --json
python scripts/seed_local.py --diagnostic-inventory --json
```

The app confirmed an implementation-backed observation inventory with 7 providers, 75 predicates, and 30 predicate families. The inventory includes `local_host` and `systemd` providers and includes `listener`, `listening`, `network`, and `systemd` predicate families. The observation-domain app output also reports `container_runtime` as `unobserved` with `container_inventory` and `container_port_mapping` pressure and no container observation family observed.

## Outcome vocabulary used

This report uses the existing narrow outcome vocabulary from the prior authority-aware investigation:

| Outcome | Meaning in this report |
| --- | --- |
| `reachable` | Required observations are implementation-backed, read-only, and satisfied by available local passive authority; no root, Docker socket read, active probe, or external provider query is required for the goal's bounded claim. |
| `reachable with uncertainty` | The bounded observation is reachable, but conservative non-inference boundaries still leave health, external reachability, ownership, intent, causality, or completeness unknown. |
| `partially reachable` | Some required observations are reachable, but the goal itself includes additional required observations that remain unavailable, blocked, absent, or privilege-limited. |
| `blocked` | A required observation depends on authority denied or unavailable in the profile. |
| `unknown` | Repository evidence does not implement the mapping or provider/domain support needed to decide. |

The distinction between `reachable with uncertainty` and `partially reachable` is whether the uncertainty is outside the bounded goal. If the goal is "what local endpoints are bound?", health and ownership uncertainty does not make the goal partial. If the goal is "which service owns this endpoint?", missing process/container/service attribution is inside the goal and makes it partial.

## Candidate comparison

| Candidate observation goal | Required observations | Required authority under profile | Blocked observations | Remaining uncertainty | Expected outcome |
| --- | --- | --- | --- | --- | --- |
| Listening services, bounded as local listener endpoint inventory | `listening_endpoint`, `listening_protocol`, `listening_address`, `listening_port`; optionally non-root listener attribution status when visible | `local_passive=available`; implementation reads local kernel/procfs socket tables and does not require root, Docker socket, active network probing, or external providers for the bounded endpoint claim | None for protocol/address/port endpoint inventory shown by local passive procfs reads | Does not prove process owner, service owner, application owner, health, responsiveness, external accessibility, DNS validity, or remote reachability | `reachable with uncertainty`; strongest `reachable` slice |
| Local listener topology, bounded as socket address/protocol/port/scope shape | Listener predicates and local socket topology facts | `local_passive=available` | None for observed local socket topology; process attribution may remain incomplete | Same as listener inventory; topology does not imply ownership or reachability from another host | `reachable with uncertainty`; strong but slightly more presentation-shaped than listening endpoint inventory |
| Local network configuration | Interface, address, default gateway, DHCP/resolver/hosts-file configuration evidence | `local_passive=available` for implemented local files/platform reads | Active reachability checks are blocked; neighbor tables, full routes, resolver runtime/cache, DNS query results, service discovery, and LLDP/CDP are unobserved or absent in repository inventory | Local configuration does not prove network health, DNS truth, remote reachability, or adjacency completeness | `partially reachable` for broad network configuration; reachable only if narrowed to already implemented local config facts |
| Systemd unit inventory / service-manager visibility | `systemd_unit`, runtime state, substate, unit-file enablement state | Privilege guidance says `systemd_inventory` is `available`, and systemd provider exists | None for basic read-only unit inventory when provider/environment is present | Does not prove service health, ownership, intent, dependencies, causality, desired state, or management authority | `reachable with uncertainty` for unit inventory; less strong than listener inventory because broader service-manager claims are documented as partially observed |
| Service ownership | Local listener evidence, listener process attribution, systemd unit attribution, container inventory, container port mapping depending on discrepancy | Local passive/systemd portions are available; listener process may be partial non-root; Docker/root unavailable for container observations | Container inventory and port mapping are blocked by unavailable Docker/root path; active probing unauthorized | Process/container owner can remain unknown; service correlation may remain unresolved | `partially reachable` |
| Container ownership | Container inventory and possibly container port mapping | Requires Docker socket / docker group / root-equivalent visibility | `docker_socket_read=unavailable` and `root=unavailable` block the required observation path | Local listener evidence may still show ports, but container owner remains unknown | `blocked` |
| External/provider-backed endpoint reachability | Provider queries or network-active probes, depending on source | `external_provider_query=unknown`; `active_network_probe=unauthorized` | Active network probe is blocked; external provider query remains unknown absent provider-specific authority | Provider vantage point identity and endpoint/host scope remain uncertain | `blocked` or `unknown`, not a clean reachable slice |

## Reachable evidence

The strongest repository-backed `reachable` candidate is **listening services, bounded as local listener endpoint inventory**.

Supporting evidence:

1. `observation_inventory` discovers providers and predicate families from implementation, not from aspirational documentation. The current app run reports `local_host` as an observation provider and reports `listener` / `listening` families.
2. `listening_port_observation.md` defines the bounded facts for listener endpoint inventory: `listening_endpoint`, `listening_protocol`, `listening_address`, and `listening_port` are derived from `/proc/net/tcp`, `/proc/net/tcp6`, `/proc/net/udp`, and `/proc/net/udp6`.
3. That same listener document explicitly says Seed does not open sockets, attempt connections, call DNS, invoke shell commands, use sudo, invoke provider APIs, use network probes, or use Prometheus for this observation.
4. `observation_domains` maps listener capability pressure to the `local_listeners` domain and classifies it as observed or partially observed based on implementation-backed listener evidence and ownership pressure.
5. `privilege_discovery` says `listener_process_inventory` is `partial_non_root`, while `systemd_inventory` is `available` and Docker-backed container capabilities require `docker_group_or_root`. This helps separate the fully reachable endpoint inventory from broader ownership attribution.
6. Prior authority-aware reasoning already identifies local listener facts as reachable when local passive reads are available and distinguishes them from service ownership, which remains partially reachable.

## Authority requirements

For the best candidate, the authority requirements are intentionally narrow:

| Requirement | Needed for bounded listener endpoint inventory? | Evidence-based reason |
| --- | --- | --- |
| `local_passive` | Yes | Listener endpoint facts come from read-only local socket tables. |
| `root` | No | The bounded listener endpoint claim avoids privileged process inventory and does not require sudo. |
| `docker_socket_read` | No | The bounded listener endpoint claim does not identify container ownership or container port mappings. |
| `active_network_probe` | No | The bounded listener endpoint claim reads local bind state and does not attempt connectivity. |
| `external_provider_query` | No | The bounded listener endpoint claim does not use provider APIs or external vantage points. |

## Strongest supporting evidence

- The listener observation design explicitly limits the claim to local protocol/address/port endpoint shape and names procfs socket tables as evidence.
- The local listener facts are implementation-backed by the observation inventory and are consumed by diagnostics, so the candidate has observation-domain support and diagnostic relevance.
- The non-inference boundary is already documented: listener facts do not imply health, responsiveness, management, external accessibility, process ownership, service ownership, or application ownership.
- The prior authority-aware investigation already treats local listener facts as reachable under `local_passive` while service ownership can remain partial.

## Strongest contradictory or limiting evidence

- `observation_domains` can classify `local_listeners` as `partially_observed` when listener ownership pressure exists. This contradicts only an over-broad goal such as "identify service ownership from listeners"; it does not contradict the narrower endpoint-inventory goal.
- `privilege_discovery` marks `listener_process_inventory` as `partial_non_root`, which means process attribution is not the clean reachable slice.
- The listener fact names have historical overlap with both `listener_*` and `listening_*` predicates, so capability-name normalization is needed before a future evaluator treats `tcp_listen_inventory`, `local_listeners`, `listening services`, and `listener_process_inventory` as interchangeable.
- `listening_endpoint` explicitly does not prove reachability from any remote vantage point. The word `reachable` here is authority reachability of the observation, not network reachability of the endpoint.

## Candidate support for a future evaluator

| Support type | Listener endpoint inventory status | Notes |
| --- | --- | --- |
| Implementation evidence | Sufficient | Provider and predicate families are discoverable through `--observation-inventory`; listener facts are implemented from local socket tables. |
| Authority guidance | Sufficient for bounded endpoint inventory | The bounded goal needs only local passive reads. Broader listener process inventory has `partial_non_root` guidance and should remain separate. |
| Observation-domain support | Sufficient | `local_listeners` exists as an observation-domain bridge and maps listener process pressure to the listener domain. |
| Diagnostic support | Sufficient for relevance, not for full ownership | Listener predicates are consumed by ownership diagnostics, but diagnostics also expose that ownership attribution can remain incomplete. |

## Capability-name normalization needed

A future evaluator should normalize goal and capability labels before applying reachability rules:

| Surface label | Proposed normalized concept | Keep distinct from |
| --- | --- | --- |
| `tcp_listen_inventory` | `local_listener_endpoint_inventory` | `listener_process_inventory` |
| `local_listeners` | `local_listener_domain` | `container_runtime` |
| `listening services` | Prefer `local_listener_endpoint_inventory` unless service ownership is explicitly requested | `service_ownership` |
| `listener_process_inventory` | `listener_process_attribution_inventory` | `local_listener_endpoint_inventory` |
| `systemd_unit_inventory` | `systemd_inventory` for current privilege guidance, or map both to a service-manager unit inventory concept | `service_ownership` |
| `systemd_inventory` | `systemd_inventory` / service-manager unit inventory | Docker/container runtime inventory |

This normalization is necessary because the clean reachable slice is the endpoint inventory, not process attribution and not service ownership. Treating `tcp_listen_inventory` and `local_listeners` as synonyms is safe only when the evaluator is asking for bound endpoint facts. It is unsafe when asking for owners.

## Best third slice

The best third slice is:

```text
local listener endpoint inventory
```

or, in user-facing terms:

```text
What local TCP/UDP endpoints are bound according to local passive socket-table evidence?
```

Expected authority-aware outcome under the constrained profile:

```text
reachable with uncertainty
```

The uncertainty is outside the bounded goal: Seed can learn local protocol/address/port bind state without root, Docker, active probing, or external providers, but Seed must not infer process owner, service owner, application owner, health, responsiveness, external accessibility, DNS validity, or network reachability.

## Can the repository demonstrate all three outcomes now?

Yes, using three implementation-backed observation goals:

| Demonstrated outcome | Observation goal | Repository-backed reason |
| --- | --- | --- |
| `blocked` | Container ownership | Container inventory and container port mapping require Docker socket / docker group / root-equivalent visibility; the profile denies root and Docker socket read. |
| `partially reachable` | Service ownership | Local listener and systemd evidence can be reachable, but listener process attribution and container ownership evidence can remain unavailable or incomplete. |
| `reachable` | Local listener endpoint inventory | Local passive socket-table facts provide bounded endpoint inventory without root, Docker socket read, active network probing, or external provider query. |

## Recommended next implementation step

Implement the smallest internal characterization helper or tests for a future evaluator that codifies this exact distinction:

1. `container ownership` under the profile returns `blocked`.
2. `service ownership` under the profile returns `partially_reachable`.
3. `local_listener_endpoint_inventory` under the profile returns `reachable` with explicit uncertainty fields for non-inferred owner, health, external reachability, and responsiveness.

Do not expose a new CLI diagnostic until the operational visibility contract can be satisfied with diagnostic inventory entries, shape-audit specs, inventory tests, shape-audit tests, recording-scope checks if `--record` is supported, and the required diagnostic inventory / diagnostic shape-audit pytest command.

## Files changed

- `docs/reachable_observation_third_slice_investigation.md`

## LOC changed

- Added 186 lines.
