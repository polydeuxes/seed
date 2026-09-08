---
doc_type: investigation
status: exploratory
domain: service ownership authority observation
defines:
  - service ownership authority slice
  - constrained service ownership reachability
  - service ownership partial reachability boundary
depends_on:
  - authority_aware_observation_reasoning_investigation.md
  - container_ownership_authority_slice_report.md
related:
  - service_ownership_authority_report.md
  - reachable_observation_third_slice_investigation.md
---

# Service ownership authority-slice investigation

## Question

Can `service ownership` demonstrate authority-aware observation reasoning for a
`partially reachable` outcome under the constrained profile?

Required constrained profile:

| Authority | Status |
| --- | --- |
| `root` | `unavailable` |
| `docker_socket_read` | `unavailable` |
| `active_network_probe` | `unauthorized` |
| `local_passive` | `available` |
| `external_provider_query` | `unknown` |

## Short answer

Yes. `service ownership` is a better second authority-aware observation slice
than another container-only question because existing repository evidence already
splits service ownership into locally reachable listener/systemd evidence and
blocked or incomplete process/container attribution evidence.

The expected constrained-profile outcome is `partially reachable`, not fully
`reachable`, because local passive evidence can support listener and systemd unit
visibility while Docker/root-dependent container evidence remains blocked and
process/listener attribution remains incomplete without elevated visibility.

## Existing implementation evidence

### Service ownership is an existing diagnostic concern

`ownership_discrepancies` defines service ownership inputs through service
predicates such as service endpoints, ports, process hosts, container hosts,
Prometheus targets, and service configuration hosts. It separately recognizes
local listener predicates such as listening socket, listener address, listener
port, listener attribution status, listening process id, and listening process
name.

`ownership_discrepancies` maps service conflicts to capability needs:

| Service conflict | Existing required observations / capability needs | Existing privilege level label |
| --- | --- | --- |
| `insufficient_evidence` | `tcp_listen_inventory`, `process_inventory`, `container_inventory` | `non_root_partial_root_full` / `partial_root_full` |
| `owner_not_observed` | `listener_process_inventory`, `container_port_mapping`, `container_inventory` | `partial_root_full` |
| `missing_owner` | `tcp_listen_inventory`, `systemd_unit_inventory` | `non_root_partial_root_full` / `partial_root_full` |

The same module suppresses `listener_process_inventory` as a needed capability
when listening process id/name evidence is already present, which proves the
repository already distinguishes “listener exists” from “listener process owner
is missing”.

### Existing domain evidence already shows partial listener reachability

`observation_domains` contains a static implementation-backed capability-to-domain
map for:

- `listener_process_inventory -> local_listeners`
- `container_inventory -> container_runtime`
- `container_port_mapping -> container_runtime`

Its current local-listener domain classification is `partially_observed` when
listener evidence exists but listener ownership pressure remains. The app output
for `seed --observation-domains local_listeners` reports:

- `Classification: partially_observed`
- `Pressure: listener_process_inventory`
- `Gap Type: missing_evidence_inside_observed_domain`
- evidence that listener predicates are observed, consumed by diagnostics, and
  ownership pressure exists.

The same app output for `seed --observation-domains container_runtime` reports
`Classification: unobserved` with pressure from `container_inventory` and
`container_port_mapping`, and evidence that no container observation family is
observed.

### Existing authority guidance distinguishes local partial from Docker/root blocked

`privilege_discovery` has implementation-backed guidance for:

| Capability | Access level | Meaning for this profile |
| --- | --- | --- |
| `listener_process_inventory` | `partial_non_root` | reachable only as partial local attribution |
| `container_inventory` | `docker_group_or_root` | blocked because root and Docker socket read are unavailable |
| `container_port_mapping` | `docker_group_or_root` | blocked because root and Docker socket read are unavailable |
| `systemd_inventory` | `available` | reachable as read-only systemd/unit attribution |

The guidance says non-root listener views can identify ports but process
ownership may be incomplete without elevated process visibility. It also says
Docker inventory and container port mappings normally require Docker socket,
Docker group, or root-equivalent visibility.

### Systemd observation is local read-only but not ownership truth

`SystemdObservationSource` is a read-only source using systemctl machine output.
It records only unit identity, runtime state, substate, and unit-file enablement
state, and explicitly does not interpret health, ownership, intent,
dependencies, or desired state. Its metadata marks observations as read-only,
local-only, without privilege escalation, and with `ownership_asserted=false`.

This makes systemd a reachable contributor for service-manager attribution, but
not enough by itself to claim full service ownership.

## Contributing observations and constrained-profile classification

| Contributing observation | Repository evidence | Classification under required profile | Reason |
| --- | --- | --- | --- |
| `tcp_listen_inventory` | Service `insufficient_evidence` and `missing_owner` conflicts request it with `non_root_partial_root_full`. | `reachable` | Local passive listener/socket table evidence is explicitly non-root partial; under this profile `local_passive=available`. It is not enough for full process/container ownership. |
| `listener_process_inventory` | Service `owner_not_observed` requests it with `partial_root_full`; local listener domain is `partially_observed` with pressure. Privilege guidance says `partial_non_root`. | `partially reachable` | Non-root listener views can identify ports, but process ownership can be incomplete without elevated process visibility. |
| `process_inventory` | Service `insufficient_evidence` requests it with `partial_root_full`. | `partially reachable` | Existing service diagnostic names process inventory as needed, but current privilege guidance has no dedicated registered row for generic `process_inventory`; repository evidence supports partial/root-full semantics, not a complete authority evaluator. |
| `systemd_unit_inventory` / `systemd_inventory` | Service `missing_owner` requests `systemd_unit_inventory` with `partial_root_full`; privilege guidance separately registers `systemd_inventory` as `available`; systemd source is local read-only and ownership-disclaimed. | `partially reachable` | Systemd metadata is locally readable and useful, but implementation explicitly does not assert ownership, intent, health, dependencies, or desired state. Naming is not perfectly aligned between `systemd_unit_inventory` and `systemd_inventory`. |
| `container_inventory` | Service conflicts request it; container domain is unobserved; authority guidance requires `docker_group_or_root`. | `blocked` | `root=unavailable` and `docker_socket_read=unavailable` block Docker/root container inventory. |
| `container_port_mapping` | Service `owner_not_observed` requests it; container domain is unobserved; authority guidance requires `docker_group_or_root`. | `blocked` | Same Docker/root boundary as container inventory. |
| `external_provider_query` | Observation permission recognizes it as external, but container-ownership slice treats it as unknown and unmapped. | `unknown` | Required profile sets it to `unknown`; current service-ownership implementation evidence does not map it into required observations. |

## Can existing concepts determine the full chain today?

Partially.

Existing concepts can already determine much of:

```text
service ownership
    -> required observations
    -> required authority
```

Supported chain:

1. `ownership_discrepancies` identifies service ownership conflicts and required
   observations/capability needs for `tcp_listen_inventory`,
   `listener_process_inventory`, `process_inventory`, `systemd_unit_inventory`,
   `container_inventory`, and `container_port_mapping`.
2. `observation_domains` maps listener and container capabilities into observed
   / partially observed / unobserved domains.
3. `privilege_discovery` maps `listener_process_inventory`,
   `container_inventory`, `container_port_mapping`, and `systemd_inventory` to
   access-level guidance.
4. `SystemdObservationSource` proves local read-only systemd evidence exists but
   is not ownership truth.

Unsupported or incomplete chain:

- There is no service-ownership authority evaluator equivalent to
  `evaluate_container_ownership_authority_slice(...)`.
- The capability name `systemd_unit_inventory` in service ownership diagnostics
  does not exactly match the `systemd_inventory` key in privilege guidance.
- `process_inventory` is named by service diagnostics but does not have a
  dedicated `_CAPABILITY_GUIDANCE` entry.
- `tcp_listen_inventory` is named by service diagnostics but is not in
  `CAPABILITY_TO_DOMAIN` or `_CAPABILITY_GUIDANCE`; listener domain evidence is
  currently centered on `listener_process_inventory`.

Therefore repository evidence can justify service ownership as the next slice,
but an implementation would need to codify the service-specific evaluator rather
than claim the full chain already exists as one function.

## Expected outcome

Expected outcome: `partially reachable`.

Why:

- Reachable evidence remains: local listener evidence, TCP/listening endpoint
  evidence, and read-only systemd unit evidence are locally available or
  non-root partial according to existing implementation evidence.
- Blocked evidence remains: Docker/root container inventory and container port
  mapping are blocked by `root=unavailable` and
  `docker_socket_read=unavailable`.
- Incomplete evidence remains: listener process attribution and generic process
  inventory are partial without elevated process visibility.
- Systemd evidence is useful for service-manager attribution but explicitly does
  not assert ownership.

## Remaining uncertainty

When `local_passive=available`, `docker_socket_read=unavailable`, and
`root=unavailable`, Seed can still learn local service shape but cannot fully
resolve ownership. Remaining uncertainty includes:

- **Container-backed services:** local listeners may expose ports, but blocked
  container inventory and port mappings prevent reliable container attribution.
- **Ownership attribution:** listener/systemd evidence can suggest candidates,
  but current systemd collection explicitly does not assert ownership, and
  listener process attribution can be incomplete without elevated visibility.
- **Runtime attribution:** repository tests and projection logic can represent
  runtime conflicts such as Docker versus systemd, but under this profile Docker
  evidence remains blocked and systemd is not definitive ownership truth.
- **Service/process relationships:** service diagnostics name process inventory
  and listener process inventory as needed; non-root process visibility may be
  partial, so service-to-process linkage remains uncertain.
- **Vocabulary alignment:** `systemd_unit_inventory` and `systemd_inventory` are
  related by meaning, but not currently the same registered capability name.

## Strongest supporting evidence

- Service ownership diagnostics already emit specific capability needs for
  listener, process, systemd, container inventory, and container port mapping.
- Observation-domain output already classifies `local_listeners` as
  `partially_observed` and `container_runtime` as `unobserved`.
- Privilege guidance already distinguishes `partial_non_root` listener process
  attribution from `docker_group_or_root` container evidence.
- Systemd observation is implemented as local, read-only, and ownership-disclaimed
  evidence, which is exactly the kind of “useful but not complete” evidence a
  partial reachability slice should demonstrate.

## Strongest contradictory evidence

- There is no existing service-ownership evaluator parallel to the container
  ownership evaluator.
- Some names do not align cleanly across components: `systemd_unit_inventory`
  versus `systemd_inventory`, and `tcp_listen_inventory` versus the
  `local_listeners` domain mapping.
- `process_inventory` lacks dedicated privilege guidance even though service
  diagnostics request it.
- Current `--privilege-discovery` output only renders rows when current state
  creates capability pressure; an empty state does not show service-specific
  capability rows.

## Files inspected

- `seed_runtime/container_ownership_authority.py`
- `seed_runtime/ownership_discrepancies.py`
- `seed_runtime/observation_domains.py`
- `seed_runtime/privilege_discovery.py`
- `seed_runtime/observation_sources.py`
- `seed_runtime/observation_permission.py`
- `seed_runtime/observation_inventory.py`
- `tests/test_container_ownership_authority.py`
- `tests/test_observation_domains.py`
- `tests/test_reasoning_path_audit.py`
- `docs/non_root_observation_expansion_investigation.md`
- `docs/observation_relationship_implementation_evidence_investigation.md`

## Files changed

- `docs/service_ownership_authority_slice_investigation.md`

## LOC changed

- Added this investigation report only.

## Tests and checks run

- `python scripts/seed_local.py --observation-domains local_listeners`
- `python scripts/seed_local.py --observation-domains container_runtime`
- `python scripts/seed_local.py --privilege-discovery`
- `python scripts/seed_local.py --container-ownership-authority`

## Recommended next implementation step

Implement the next slice as a small service-ownership authority evaluator that:

1. Reuses the same constrained authority profile as
   `container_ownership_authority`.
2. Uses existing service capability needs from `ownership_discrepancies` as the
   required-observation source.
3. Normalizes or explicitly maps `systemd_unit_inventory` to current systemd
   guidance, and adds explicit handling for `tcp_listen_inventory` and
   `process_inventory` if repository authority confirms the intended names.
4. Reports `reachable`, `partially reachable`, `blocked`, and `unknown` per
   observation, then summarizes the overall outcome as `partially reachable` when
   local passive listener/systemd evidence remains available but Docker/root
   evidence is blocked.
5. Adds diagnostic inventory and shape-audit registration/tests only if exposed
   as a new operational CLI surface.

## Acceptance answer

Yes, service ownership can demonstrate authority-aware observation reasoning for
a `partially reachable` outcome.

Yes, service ownership is the best next slice after container ownership because
container ownership proved a fully blocked case, while service ownership uses
existing repository concepts to show the mission-relevant middle case: Seed can
still learn local listeners and service-manager shape without root, Docker, or
network probing, but it cannot fully prove container-backed ownership or complete
process/runtime attribution.
