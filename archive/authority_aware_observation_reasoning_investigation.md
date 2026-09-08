---
doc_type: investigation
status: exploratory
domain: authority-aware observation reasoning
defines:
  - authority-aware observation reasoning gap
  - desired observation reachability boundary
  - observation authority profile
  - observation uncertainty boundary
depends_on:
  - non_root_observation_expansion_investigation.md
  - listening_port_observation.md
related:
  - container_ownership_authority_slice_report.md
  - service_ownership_authority_slice_investigation.md
  - reachable_observation_third_slice_investigation.md
---

# Authority-Aware Observation Reasoning Investigation

## Purpose and boundary

This report scopes the missing behavior between a desired observation and the authority currently available to Seed. It stays inside existing repository vocabulary: observations, observation classes, permissions, authority evidence, capability needs, capability/access relationships, observation domains, and ownership discrepancies. It does not propose a new ontology, capability taxonomy, provider taxonomy, gap taxonomy, planning framework, or answer-composition framework.

The investigated constraint profile is:

| Authority or observation class | Profile state |
| --- | --- |
| `root` | unavailable |
| `docker_socket_read` | unavailable |
| `active_network_probe` | unauthorized |
| `local_passive` | available |
| `external_provider_query` | available or unknown |

The active question is capability under constraint: what can Seed still learn, what is blocked, what requires operator authorization, and what uncertainty remains?

## Files inspected

Implementation evidence inspected:

- `seed_runtime/observation_permission.py`
- `seed_runtime/observation_domains.py`
- `seed_runtime/capability_needs.py`
- `seed_runtime/privilege_discovery.py`
- `seed_runtime/capability_relationship.py`
- `seed_runtime/ownership_discrepancies.py`
- `seed_runtime/observation_inventory.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`

Tests inspected:

- `tests/test_observation_permission.py`
- `tests/test_observation_domains.py`
- `tests/test_capability_relationship.py`
- `tests/test_privilege_discovery.py`
- `tests/test_ownership_discrepancies.py`
- `tests/test_observation_inventory.py`
- `tests/test_diagnostic_inventory.py`
- `tests/test_diagnostic_shape_audit.py`

Prior investigations inspected:

- `docs/constraint_aware_observation_reachability_investigation.md`
- `docs/non_root_observation_expansion_investigation.md`
- `docs/manual_observation_permission_investigation.md`
- `docs/observation_domain_permission_authority_reuse_investigation.md`
- `docs/capability_authority_and_execution_boundary_reconciliation.md`
- `docs/capability_gap_and_operator_bridge_reconciliation.md`

Commands used:

```text
rg --files seed_runtime tests docs | rg 'capability|permission|privilege|observation|authority|inventory|shape|constraint|ownership|runtime|listener'
python scripts/seed_local.py --observation-permission --json
python scripts/seed_local.py --observation-domains --json
python scripts/seed_local.py --capability-relationship --json
```

## Existing concepts that are already sufficient

### Observation classes and permission state

`observation_permission` already carries the important vocabulary for authority-aware observation: `ObservationClass` includes `local_passive`, `network_passive`, `network_active`, `local_privileged`, `external`, and `unknown`; `PermissionState` includes `granted`, `requires_operator_expression`, `denied`, and `unknown`. The current supported observation activity map already includes `active_network_probe`, `docker_socket_read`, and `external_provider_query`, and the report boundary is explicitly read-only, non-enforcing, non-recording, non-autonomous, and non-mutating.

This is enough vocabulary to express the required scenario at the observation-activity level:

```text
active_network_probe -> network_active -> unauthorized / requires operator expression
docker_socket_read -> local_privileged -> unavailable / not granted
external_provider_query -> external -> available or unknown
local_passive -> available
```

The implementation gap is not the absence of permission vocabulary. The gap is that Seed does not yet accept or synthesize a concrete multi-authority constraint profile and then propagate it across desired observations.

### Capability needs from ownership discrepancies

`ownership_discrepancies` already translates ownership conflicts into diagnostic capability needs. For service `owner_not_observed`, it names `listener_process_inventory`, `container_port_mapping`, and `container_inventory`. For service `missing_owner`, it names `tcp_listen_inventory` and `systemd_unit_inventory`. `capability_needs` aggregates these diagnostic-only needs by capability, affected subjects, diagnostics, needed evidence, and diagnostic runs.

This is enough to identify what observations are required for `container ownership` and related service-ownership questions without inventing new concepts:

| Desired observation | Existing required-evidence path |
| --- | --- |
| container ownership | service ownership discrepancy -> `container_inventory` |
| container port-to-service attribution | service ownership discrepancy -> `container_port_mapping` |
| listener-process attribution | service ownership discrepancy -> `listener_process_inventory` |
| basic local service/listener presence | service missing-owner discrepancy -> `tcp_listen_inventory` / local listener predicates |
| system service unit attribution | service missing-owner discrepancy -> `systemd_unit_inventory` |

### Observation domains and provider evidence

`observation_domains` already maps capability pressure into observation domains. It maps `listener_process_inventory` to `local_listeners` and maps `container_inventory` plus `container_port_mapping` to `container_runtime`. It can report `container_runtime` as `unobserved` with `missing_observation_domain` when capability pressure exists but no container observation family exists. It can report local listeners as `partially_observed` when listener predicates exist but ownership pressure remains.

This is enough to distinguish missing provider/category evidence from missing facts inside an observed domain. It is not enough to determine whether the same domain is unreachable because authority is denied.

### Access guidance and capability relationship

`privilege_discovery` already gives implementation-backed access guidance:

| Capability | Current access guidance | Operational benefit |
| --- | --- | --- |
| `listener_process_inventory` | `partial_non_root` | service ownership attribution |
| `container_inventory` | `docker_group_or_root` | container ownership attribution |
| `container_port_mapping` | `docker_group_or_root` | container port-to-service attribution |
| `systemd_inventory` | `available` | service unit attribution |
| `nfs_export_inventory` | `root` | storage export ownership attribution |

`capability_relationship` co-locates capability, current access, operational benefit, pressure, and reasoning while intentionally leaving attainability and expectation as `unknown`. This supports the central boundary: capability pressure is visibility context, not authorization, acquisition intent, or execution.

## Desired-observation walkthrough: container ownership

For desired observation `container ownership`, the existing repository path is:

1. Ownership diagnostics see service ownership conflicts such as `owner_not_observed` or insufficient service evidence.
2. `diagnostic_capability_need_records()` emits capability needs including `container_inventory` and `container_port_mapping` for service ownership attribution gaps.
3. `build_capability_needs()` aggregates those needs by subject, diagnostic, needed evidence, and capability.
4. `build_observation_domains()` maps `container_inventory` and `container_port_mapping` to `container_runtime` and can show that container runtime is unobserved when no container observation family is present.
5. `build_privilege_discovery()` maps `container_inventory` and `container_port_mapping` to `docker_group_or_root` access guidance.
6. `build_observation_permission()` can separately show that `docker_socket_read` is a `local_privileged` observation activity and that no reusable approval is observed unless an approval fact exists.

That path is already sufficient to determine many pieces:

| Question | Existing evidence is sufficient? | Current evidence path |
| --- | --- | --- |
| Required observations? | Yes, for ownership-pressure cases. | ownership discrepancy -> capability needs (`container_inventory`, `container_port_mapping`) |
| Required permissions? | Partially. | capability -> `docker_group_or_root`; observation activity -> `docker_socket_read` / `local_privileged` |
| Blocked permissions? | Partially. | `observation_permission` can show no approval or requires operator expression; it does not ingest `docker_socket_read=unavailable`. |
| Remaining observations? | Partially. | `observation_domains` and inventory show local listener/systemd/provider families, but not a constrained reachability set. |

The missing behavior is the join and evaluation step:

```text
desired observation
+ diagnostic capability needs
+ observation-domain/provider evidence
+ access guidance
+ observation permission state
+ explicit constraint profile
=> reachable / partially reachable / blocked / requires authorization / requires provider acquisition / unknown
```

## Missing behavior, not missing concepts

The repository appears to have enough concepts for the current mission. The missing behavior is an authority-aware observation reachability evaluator.

Today the relevant facts are surface-local:

- `observation_permission` knows selected observation activities and permission states, but not desired-observation reachability.
- `privilege_discovery` knows capability access guidance, but not a concrete root/Docker/network-active constraint profile.
- `observation_domains` knows observed, partially observed, and unobserved domains, but not whether unobserved means blocked by authority, absent provider, or merely not currently pressured.
- `capability_relationship` connects pressure, access, and benefit, but intentionally leaves attainability and expectation unknown.
- `capability_needs` knows missing evidence pressure, but not whether the needed observation can still be collected under current authority.

The behavior missing today is therefore not a new taxonomy. It is a deterministic read-only join over existing surfaces with an explicit boundary: visibility only, no approval creation, no permission enforcement, no provider acquisition, no probing, no event-ledger write, and no cluster mutation.

## Can Seed already determine desired observation -> required authority?

Seed can partially determine it but cannot do so as a single implemented behavior.

For `container ownership`, the repository can be manually followed to:

```text
container ownership
-> container_inventory / container_port_mapping
-> container_runtime observation domain
-> docker_group_or_root access guidance
-> docker_socket_read local_privileged activity when Docker socket observation is the path
```

The specific implementation gap is the lack of a function or diagnostic that maps a desired observation to required authority by joining:

1. desired observation or conflict class to capability needs;
2. capability needs to observation domain;
3. capability to access guidance;
4. access guidance to concrete authority requirements in the supplied profile;
5. observation activity to permission state;
6. provider/domain evidence to provider availability or missing-provider uncertainty.

The current repository lets an operator reconstruct that path by reading multiple reports. Seed does not yet compute or preserve the path as one result.

## Outcomes to distinguish using repository evidence

The following outcome words should be treated as behavior states in a narrow evaluator, not as a new ontology. They are supported by existing repository principles and fields:

| Outcome | Existing repository support | Meaning under the required profile |
| --- | --- | --- |
| reachable | Permission/access evidence says observation can be attempted read-only, and provider/domain evidence exists. | `local_passive` observations such as local listener facts remain reachable when local passive reads are available. |
| partially reachable | Existing domain evidence is present, but capability pressure indicates missing evidence remains. | Local listeners may be visible while listener process ownership remains incomplete without root or privileged process visibility. |
| blocked | Required authority is denied or unavailable in the profile. | Docker-backed container inventory is blocked when root and Docker socket read are unavailable; active network probing is blocked when unauthorized. |
| requires operator authorization | Repository knows the observation activity but lacks reusable approval and the profile does not deny it outright. | `active_network_probe` currently reports requires operator expression when no reusable approval exists; if profile says unauthorized, it is blocked for this run. |
| requires provider acquisition | Observation domain or provider family is absent while the authority question alone does not prove impossibility. | Container runtime inventory can require a provider if no container observation family exists; this remains distinct from Docker authority being denied. |
| unknown | Repository lacks implementation-backed mapping or profile value. | `external_provider_query=available or unknown` remains unknown unless a specific provider and approval/availability signal is present. |

These distinctions are already implied by `PermissionState`, observation-domain classifications, capability relationship unknowns, provider inventory, and privilege guidance. The missing implementation is to apply them consistently to a desired observation under a supplied profile.

## What Seed should do when an observation is blocked

Repository evidence supports these bounded responses:

1. **Surface limitation.** Existing diagnostics consistently expose read-only boundaries and limitations. A blocked observation should state which requirement is unavailable and which desired observation is affected.
2. **Offer alternatives.** Existing capability and observation-domain surfaces can show remaining local/passive or provider-backed evidence. Alternatives should be observations, not plans or execution promises.
3. **Request authority only as a surfaced requirement.** `observation_permission` says missing reusable approval requires operator expression; it does not enforce, store approval, or create runtime autonomy. A reachability evaluator should therefore say authorization would be required, not request or record it itself.
4. **Record uncertainty only if invoked through an existing diagnostic-recording boundary.** Diagnostic findings should remain scoped to `diagnostic_run:<id>` and should not become cluster truth.
5. **Defer execution.** The evaluator should not compensate by probing, using Docker, invoking providers, or escalating privileges.

## Required scenario evaluation

| Desired observation | Existing path | Required authority under profile | Outcome under profile | Remaining reachable observations / uncertainty |
| --- | --- | --- | --- | --- |
| Identify container ownership | ownership discrepancy -> `container_inventory` -> `container_runtime` -> `docker_group_or_root` | Docker socket or root-equivalent visibility; provider evidence absent unless separately supplied | blocked and/or requires provider acquisition | Local service/listener evidence may still show ports or endpoints, but container owner remains unknown. |
| Identify service ownership | ownership discrepancy -> listener/process/container/systemd needs | Local passive listener/systemd can be available; process/container attribution may need root/Docker | partially reachable | Systemd unit evidence and listener endpoints may remain; process/container owner can remain unknown. |
| Identify listening services | local listener predicates / `tcp_listen_inventory` | local passive | reachable or partially reachable | Listener address/protocol/port/scope can be observed; process identity may remain partial. |
| Identify network relationships | neighbor-table read, passive network evidence, active probe | local passive for neighbor/config reads; network-active for probing | local passive portions reachable if provider exists; active probes blocked | Neighbor/route categories may require implementation/provider work; active reachability remains unauthorized. |
| Identify runtime inventory | systemd and local host inventory vs container inventory | systemd/local passive available; Docker/root unavailable for container runtime | partially reachable | Host/systemd runtime inventory remains reachable; container runtime inventory blocked or absent. |

## Strongest supporting evidence

1. The permission vocabulary and activity map already include the observation classes and states needed for the scenario.
2. Ownership diagnostics already name the capability needs that connect service/container ownership gaps to required observations.
3. Observation domains already distinguish observed, partially observed, and unobserved domains, including the current container-runtime absence.
4. Privilege discovery already encodes access guidance for listener, container, systemd, and storage-export capabilities.
5. Capability relationship intentionally avoids acquisition decisions by preserving attainability and expectation as unknown.
6. Diagnostic inventory and shape-audit conventions already provide a read-only, non-mutating pattern for adding a narrow diagnostic surface if this becomes implementation work.

## Strongest contradictory or limiting evidence

1. There is no first-class constraint-profile input for `root=unavailable`, `docker_socket_read=unavailable`, `active_network_probe=unauthorized`, `local_passive=available`, and `external_provider_query=available_or_unknown`.
2. There is no implemented desired-observation-to-capability mapper beyond the current ownership-discrepancy pressure paths.
3. There is no implemented join from capability access guidance to observation permission activity and profile state.
4. There is no reachability result that distinguishes blocked-by-authority from missing-provider, partial-evidence, requires-operator-expression, and unknown.
5. Current surfaces are diagnostic and visibility oriented. They do not enforce authorization, create approvals, acquire providers, execute observations, or mutate cluster truth.

## Smallest implementation-backed behavior

The smallest useful implementation slice is a read-only authority-aware observation reachability function, exposed only if necessary as a diagnostic after registry and shape-audit updates.

Recommended first slice:

1. Add a narrow module, for example `seed_runtime/observation_reachability.py`.
2. Accept a small explicit profile object or CLI JSON/string flags for the already named states: root, docker socket read, active network probe, local passive, external provider query.
3. Support only the initial desired observations from this investigation: container ownership, service ownership, listening services, network relationships, and runtime inventory.
4. Reuse existing maps instead of introducing new taxonomy:
   - ownership/capability needs from `ownership_discrepancies` and `capability_needs`;
   - domains from `observation_domains.CAPABILITY_TO_DOMAIN`;
   - access guidance from `privilege_discovery._guidance_for` or a public equivalent;
   - permission activities/classes from `observation_permission.SUPPORTED_OBSERVATION_CLASSES`;
   - provider/domain evidence from `observation_inventory` and `observation_domains`.
5. Return a read-only result with desired observation, required capabilities, required observation activities, available authority, blocked authority, remaining observations, outcome, uncertainty, and boundary.
6. Add tests for the required profile proving:
   - container ownership is blocked or requires provider acquisition when root and Docker socket read are unavailable;
   - listening services remain reachable or partially reachable through local passive observation;
   - active network probing is blocked when unauthorized;
   - external provider query remains unknown when profile says available or unknown without provider-specific evidence;
   - the surface is read-only and does not record cluster truth.
7. If exposed as a CLI diagnostic, update diagnostic inventory, diagnostic shape-audit specs, and tests proving the surface appears in `seed --diagnostic-inventory` and is checked by `seed --diagnostic-shape-audit`.

This slice would let Seed answer:

```text
What can I still learn under this authority profile?
```

without new concepts. It would connect concepts the repository already has.

## Acceptance answer

Seed is not primarily missing concepts for this mission. It is missing the behavior that connects existing concepts.

The smallest implementation-backed step is to add a deterministic, read-only reachability evaluator that joins desired observation, capability pressure, observation-domain/provider evidence, capability access guidance, observation permission state, and an explicit constraint profile. Its first responsibility should be to answer constrained observation reachability for container ownership, service ownership, listening services, network relationships, and runtime inventory under the required non-root/no-Docker/no-active-probe profile.

## Files changed

- `docs/authority_aware_observation_reasoning_investigation.md`

## LOC changed

- Added this investigation report: 280 lines.
