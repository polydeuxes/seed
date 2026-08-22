# Service ownership authority-aware inquiry reuse findings

## Verdict

Yes, `service ownership` can reuse the existing authority-aware inquiry discipline, but only as a bounded service-ownership slice, not as a generic inquiry runtime.

The repository already contains an implementation-backed evaluator for this exact desired observation: `evaluate_service_ownership_authority_slice(...)`. It fixes the desired observation to `service ownership`, derives a bounded set of participating observations, maps each observation to existing privilege guidance, applies the constrained authority profile, and reports a mixed outcome: local listener/process/systemd evidence is reachable while container-runtime attribution remains blocked without Docker socket or root-equivalent authority.

This is reuse of the pattern, not proof of a generalized framework. The strongest implementation difference from `container ownership` is that service ownership is not a single-strategy inquiry. The implemented service slice is a composite attribution strategy that joins local listener, listener-process, systemd-unit, and container-runtime observations. That composite shape is supported, but its current dataclass does not expose every inquiry-state field that the newer container slice exposes (`current_strategy`, `strategy_status`, `remaining_observations`, and `blocking_boundary`).

## Files inspected

- `seed_runtime/service_ownership_authority.py`
- `seed_runtime/container_ownership_authority.py`
- `seed_runtime/listener_endpoint_authority.py`
- `seed_runtime/ownership_discrepancies.py`
- `seed_runtime/privilege_discovery.py`
- `seed_runtime/observation_sources.py`
- `seed_runtime/observation_domains.py`
- `seed_runtime/observation_permission.py`
- `tests/test_service_ownership_authority.py`
- `tests/test_listener_endpoint_authority.py`
- `tests/test_ownership_discrepancies.py`
- `scripts/seed_local.py`
- `docs/container_ownership_authority_minimal_slice_findings.md`

## Implementation-backed observation strategy

The repository-supported strategy is best described as:

```text
composite local service attribution observation
```

It is not a new runtime ontology and not a planner. It is implemented by `SERVICE_OBSERVATIONS` in `seed_runtime/service_ownership_authority.py`:

```text
tcp_listen_inventory
listener_process_inventory
systemd_unit_inventory
container_inventory
container_port_mapping
```

The evaluator treats those observations as the bounded evidence needed for the `service ownership` desired observation. The resulting CLI surface is already present as `seed --service-ownership-authority`.

This differs from container ownership, whose current strategy is explicitly named `container_runtime_observation` and whose required observations are limited to `container_inventory` and `container_port_mapping`.

## Participating observations

Only implementation-backed observations should participate:

| Observation | Implementation evidence | Role in service ownership |
| --- | --- | --- |
| `tcp_listen_inventory` | Ownership discrepancy capability needs request local listener evidence for service `missing_owner` and `insufficient_evidence`; listener observations are collected from `/proc/net/{tcp,tcp6,udp,udp6}`. | Establishes that a local endpoint exists; not ownership by itself. |
| `listener_process_inventory` | Privilege guidance exists; listener collection may emit `listening_process_id` and `listening_process_name` when process attribution is visible. | Narrows endpoint evidence toward process attribution, with non-root incompleteness. |
| `systemd_unit_inventory` | Systemd observation source emits `systemd_unit`, `systemd_active_state`, `systemd_sub_state`, and `systemd_unit_file_state`; privilege guidance says systemd metadata is commonly read-only inspectable. | Supports service-manager attribution, without asserting ownership, health, intent, dependencies, or desired state. |
| `container_inventory` | Capability guidance exists and observation domains classify container runtime pressure. | Needed when a service is container-managed; blocked without Docker/root authority in the constrained profile. |
| `container_port_mapping` | Capability guidance exists and container ownership slice already proves Docker/root boundary. | Needed to connect container-exposed ports to service attribution; blocked in the constrained profile. |

Listener endpoint authority is supporting evidence only for endpoint visibility. Its boundary explicitly excludes service ownership, process ownership, application ownership, and container ownership, so it cannot be promoted into a service owner answer by itself.

## Authority requirements

The authority model is reused; no new authority domain is needed.

| Observation | Required authority | Existing authority source |
| --- | --- | --- |
| `tcp_listen_inventory` | `local_passive` | Hard-coded in the service authority evaluator as local passive endpoint evidence. |
| `listener_process_inventory` | `partial_non_root` | `privilege_discovery` guidance: non-root listener views may identify ports but process ownership can be incomplete without elevated process visibility. |
| `systemd_unit_inventory` | `local_passive` | Mapped from `systemd_inventory` guidance, which is `available`; service evaluator normalizes it to `local_passive` for the constrained authority profile. |
| `container_inventory` | `docker_group_or_root` | `privilege_discovery` guidance and container authority slice. |
| `container_port_mapping` | `docker_group_or_root` | `privilege_discovery` guidance and container authority slice. |

The constrained profile remains:

```text
root=unavailable
docker_socket_read=unavailable
active_network_probe=unauthorized
local_passive=available
external_provider_query=unknown
```

Under that profile, the service authority CLI reports:

```text
outcome=partially_reachable
reachable_observations=tcp_listen_inventory, listener_process_inventory, systemd_unit_inventory
blocked_observations=container_inventory, container_port_mapping
```

## Can the repository distinguish unavailable cases?

Partially.

| Distinction | Supported for this inquiry? | Evidence-backed explanation |
| --- | --- | --- |
| Strategy unavailable | Weakly supported. | The service slice has `outcome`, `reachable_observations`, and `blocked_observations`, but does not name `current_strategy` or `strategy_status`. This is a shape immaturity, not an authority-domain gap. |
| Authority unavailable | Supported. | Docker/root-dependent container observations are blocked when both `root` and `docker_socket_read` are unavailable. Observation permission also recognizes `docker_socket_read` as `local_privileged`. |
| Implementation unavailable | Partially supported. | Service uncertainty reports whether listener/systemd evidence is found in observation inventory; observation domains can report unobserved container runtime. However, the service authority slice does not yet label an observation specifically as `implementation_unavailable`. |
| Observation unavailable | Supported as pressure and uncertainty, not as a fully normalized status. | Ownership discrepancies emit capability needs for missing service evidence, and observation domains classify local listener/container gaps. The service slice returns blocked observations for authority-blocked container observations, but not a four-way normalized unavailability enum. |

## Does the inquiry-state shape naturally apply?

Mostly yes, with one concrete break.

| Inquiry-state field | Service ownership support | Notes |
| --- | --- | --- |
| desired observation | Supported | `desired_observation = "service ownership"`. |
| current strategy | Conceptually supported, but not fielded | The implementation strategy exists as composite local service attribution, but the dataclass lacks `current_strategy`. |
| required observations | Supported | Five observations are returned. |
| required authority | Supported | Per-observation authority is returned. |
| available authority | Supported | The constrained profile is returned. |
| strategy status | Conceptually supported, but not fielded | `outcome=partially_reachable` is effectively the strategy status, but the field is not named. |
| blocking boundary | Partially supported | Blocked observations expose the Docker/root boundary, but no `blocking_boundary` field names it. |
| remaining observations | Partially supported | `blocked_observations` acts as remaining work, but the field is not named `remaining_observations`. |
| uncertainty | Supported | The slice records implementation-evidence notes and authority boundary uncertainty. |
| boundary | Supported | The slice is read-only, does not record, does not write the ledger, does not mutate the cluster, does not create permissions, does not acquire providers, and does not execute observation. |

The exact break is shape vocabulary, not capability. The service slice predates or avoids the newer container inquiry-state labels. The underlying data needed for the shape mostly exists.

## New authority domain?

No. This bounded inquiry reuses existing authority concepts:

- `local_passive`
- `partial_non_root`
- `docker_group_or_root`
- `local_privileged` recognition for Docker socket reads
- explicit non-use of unauthorized active network probing
- explicit non-promotion of unknown external provider query authority

Systemd does not introduce a new authority domain in the current implementation. The guidance treats systemd unit metadata as commonly inspectable without privilege for read-only attribution, and the systemd source records read-only local facts while refusing to assert ownership, health, intent, dependencies, or desired state.

## Supported uncertainty

The repository supports these uncertainties for service ownership:

- Listener endpoint facts do not establish process owner, service owner, container owner, or application owner.
- Systemd unit facts do not establish ownership, health, intent, dependencies, or desired state.
- Listener process attribution can be incomplete without elevated process visibility.
- Container inventory and container port mappings remain Docker/root dependent.
- Active network probing and external provider queries are not used to promote service ownership under the constrained profile.
- Local listener domains may be only partially observed when ownership pressure remains.

## Strongest supporting evidence

1. `seed_runtime/service_ownership_authority.py` already implements a narrow service-ownership authority evaluator and reports a deterministic partial result.
2. `tests/test_service_ownership_authority.py` proves the constrained-profile outcome, reachable listener/systemd observations, blocked container observations, CLI JSON shape, diagnostic inventory registration, diagnostic shape audit consistency, and no writes/acquisition/permission behavior.
3. `seed_runtime/ownership_discrepancies.py` already models service ownership conflicts and emits capability needs for local listener, listener-process, systemd, container inventory, and container port mapping evidence.
4. `seed_runtime/privilege_discovery.py` already supplies authority guidance for listener-process, container inventory, container port mapping, and systemd inventory.
5. `seed_runtime/observation_sources.py` contains concrete listener and systemd observation sources, both bounded by read-only/non-ownership metadata.
6. `seed_runtime/observation_permission.py` recognizes Docker socket reads as local privileged and active probing/external queries as separate authority classes.

## Strongest contradictory evidence

1. Service ownership lacks the explicit `current_strategy`, `strategy_status`, `remaining_observations`, `remaining_uncertainty`, and `blocking_boundary` fields that the container ownership slice now exposes.
2. `observation_domains.CAPABILITY_TO_DOMAIN` maps listener-process and container capabilities but does not map `tcp_listen_inventory` or `systemd_unit_inventory`, so service-manager and endpoint inventory domains are less mature than the implemented evaluator implies.
3. `privilege_discovery` registers guidance for `systemd_inventory`, while the service slice exposes `systemd_unit_inventory`; the evaluator bridges this internally, but the naming difference is an implementation maturity smell.
4. Listener endpoint authority explicitly excludes service ownership, which prevents accidental promotion but also proves endpoint visibility alone cannot answer service ownership.
5. Systemd observations intentionally refuse to assert ownership. They can participate in attribution, but they are not a complete owner answer.

## Implementation gaps

- Add shape parity if implementation is requested later: expose `current_strategy`, `strategy_status`, `remaining_observations`, `remaining_uncertainty`, and a named `blocking_boundary` for the existing service authority evaluator.
- Align or explicitly document the `systemd_inventory` versus `systemd_unit_inventory` naming bridge.
- Consider whether `tcp_listen_inventory` and `systemd_unit_inventory` should appear in observation-domain classification if the domain subsystem is expected to account for all service-ownership observations.
- Preserve the listener endpoint boundary: endpoint inventory should remain evidence for service ownership, not a service-owner conclusion.

## Subsystem maturity

This bounded inquiry did not discover a missing subsystem. It revealed the next place existing subsystems must mature.

The subsystem with the clearest immaturity is `service_ownership_authority` itself: it already answers the bounded question, but its output shape has not caught up with the container inquiry-state shape. The bounded question that exposed this was:

```text
Can service ownership reuse desired/current strategy/required observation/authority/status/boundary/remaining/uncertainty shape?
```

The second maturity point is `observation_domains`: it can represent local listener and container runtime pressure, but its capability-to-domain map does not yet cover every service-ownership observation that the service authority evaluator uses.

No planner, conversation engine, generic inquiry framework, service runtime ontology, or new authority domain is required by this evidence.

## Recommended next implementation slice

If implementation is requested, keep it narrow:

```text
Add shape parity to seed_runtime/service_ownership_authority.py for the already-supported service ownership evaluator.
```

Specifically, add fields equivalent to the container slice:

- `current_strategy = "composite_local_service_attribution_observation"`
- `strategy_status = outcome`
- `remaining_observations = blocked_observations`
- `remaining_uncertainty = uncertainty`
- `blocking_boundary = "docker_or_root_container_runtime_authority_unavailable"` when container observations are blocked

Then update only the existing service authority tests and diagnostic shape expectations as required by the operational visibility contract.

## Files changed

- `docs/service_ownership_authority_reuse_findings.md`

## LOC changed

- One documentation file added, 216 lines.

## Tests and checks run

- `python scripts/seed_local.py --service-ownership-authority --json`
- `python scripts/seed_local.py --container-ownership-authority --json`
- `python scripts/seed_local.py --listener-endpoint-authority --json`
- `pytest -q tests/test_service_ownership_authority.py tests/test_listener_endpoint_authority.py tests/test_ownership_discrepancies.py`
