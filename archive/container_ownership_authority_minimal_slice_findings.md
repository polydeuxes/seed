---
doc_type: report
status: implementation-backed finding
domain: container ownership authority observation
depends_on:
  - container_ownership_authority_slice_report.md
  - container_ownership_authority_cli_report.md
---

# Container ownership authority minimal slice findings

## Answer

Yes. Seed can prove the authority-aware observation reasoning model using only the `container ownership` case under the constrained authority profile:

```text
root = unavailable
docker_socket_read = unavailable
active_network_probe = unauthorized
local_passive = available
external_provider_query = unknown
```

The smallest behavior is already a narrow deterministic join, not a generalized planner. The implementation-backed slice is `evaluate_container_ownership_authority_slice(...)`, which fixes the desired observation to `container ownership`, keeps only container-runtime observations, maps those observations to existing privilege guidance, applies the supplied authority profile, and reports `blocked` when both root and Docker socket read authority are unavailable.

## Existing implementation evidence

### Desired observation to required observations

`ownership_discrepancies` already maps unresolved service ownership evidence to container-related needs:

- `service / insufficient_evidence` includes `container_inventory`.
- `service / owner_not_observed` includes both `container_port_mapping` and `container_inventory`.
- `diagnostic_capability_need_records(...)` emits those as diagnostic-only capability need records.

`capability_needs` already joins current `ownership_discrepancies` rows into normalized `CapabilityNeedEntry` values and can filter to `diagnostic_filter="ownership_discrepancies"`.

`observation_domains` already maps:

```text
container_inventory -> container_runtime
container_port_mapping -> container_runtime
```

For the first deterministic slice, the required observations are therefore exactly:

```text
container_inventory
container_port_mapping
```

### Required observations to required authority

`privilege_discovery` already maps both container observations to the same authority requirement:

```text
container_inventory -> docker_group_or_root
container_port_mapping -> docker_group_or_root
```

This is equivalent to requiring Docker socket, Docker group, or root-equivalent visibility for the required container runtime evidence.

### Available authority and blocking decision

`observation_permission` already recognizes `docker_socket_read` as a `local_privileged` observation class. The required scenario is stricter than an unapproved default permission state because it supplies `docker_socket_read = unavailable`; the first slice should therefore treat the supplied profile as authoritative rather than attempting to create or infer permission.

The implemented evaluator uses the supplied profile, not current approval state, as the authority decision source. With `root=unavailable` and `docker_socket_read=unavailable`, both required observations remain blocked because each requires `docker_group_or_root`.

## Required joins

The smallest exact join is:

```text
container ownership
  -> CONTAINER_OBSERVATIONS
     {container_inventory, container_port_mapping}
  -> observation_domains.CAPABILITY_TO_DOMAIN
     keep observations mapped to container_runtime
  -> privilege_discovery._guidance_for(...)
     require docker_group_or_root for each observation
  -> supplied authority profile
     root unavailable + docker_socket_read unavailable
  -> blocked
  -> remaining observations are the same required observations
```

Subject-specific pressure is a secondary evidence join, not the source of the first deterministic requirement set:

```text
build_capability_needs(state, diagnostic_filter="ownership_discrepancies")
  -> any need in {container_inventory, container_port_mapping}
  -> uncertainty distinguishes subject-specific pressure from domain-level pressure
```

Permission-domain evidence is also supporting evidence, not authority acquisition:

```text
docker_socket_read
  -> observation_permission.SUPPORTED_OBSERVATION_CLASSES
  -> local_privileged
  -> supplied profile remains authoritative
```

## Minimal evaluation path

The minimal evaluation path is the current `container_ownership_authority` slice:

1. Accept a `State` and supplied authority profile.
2. Normalize only these authority keys: `root`, `docker_socket_read`, `active_network_probe`, `local_passive`, and `external_provider_query`.
3. Select only `container_inventory` and `container_port_mapping` when repository domain evidence maps them to `container_runtime`.
4. Lookup existing privilege guidance for each selected observation.
5. Return `blocked` only when all selected observations require `docker_group_or_root` and both `root` and `docker_socket_read` are unavailable.
6. Preserve uncertainty instead of acquiring providers, creating permissions, recording diagnostics, or executing observations.

## Minimal result shape

```json
{
  "desired_observation": "container ownership",
  "required_observations": [
    "container_inventory",
    "container_port_mapping"
  ],
  "required_authority": {
    "container_inventory": "docker_group_or_root",
    "container_port_mapping": "docker_group_or_root"
  },
  "available_authority": {
    "root": "unavailable",
    "docker_socket_read": "unavailable",
    "active_network_probe": "unauthorized",
    "local_passive": "available",
    "external_provider_query": "unknown"
  },
  "outcome": "blocked",
  "remaining_observations": [
    "container_inventory",
    "container_port_mapping"
  ],
  "uncertainty": [
    "external_provider_query unknown and not mapped to this first slice",
    "local_passive available but not sufficient for docker/root container runtime evidence",
    "docker_socket_read is recognized as local_privileged observation-permission activity but supplied profile remains authoritative",
    "subject-specific ownership pressure exists only when ownership_discrepancies emits matching service conflicts"
  ],
  "boundary": {
    "read_only": true,
    "records": false,
    "writes_event_ledger": false,
    "mutates_cluster": false,
    "provider_acquisition": false,
    "permission_creation": false,
    "executes_observation": false
  }
}
```

## Code paths that participate

Required for the first slice:

- `seed_runtime/container_ownership_authority.py` for the deterministic evaluator and result shape.
- `seed_runtime/ownership_discrepancies.py` for ownership-conflict-to-capability pressure evidence.
- `seed_runtime/capability_needs.py` for normalized subject-specific diagnostic pressure.
- `seed_runtime/observation_domains.py` for the container-runtime capability mapping.
- `seed_runtime/privilege_discovery.py` for `docker_group_or_root` authority guidance.
- `seed_runtime/observation_permission.py` for recognition of `docker_socket_read` as local privileged.
- `tests/test_container_ownership_authority.py` for blocked outcome, read-only/no-write boundary, CLI JSON shape, and diagnostic inventory/shape-audit registration.

## Code paths not required for the first slice

The first slice does not need:

- a general reachability framework;
- a generic planner;
- an authority engine;
- a capability acquisition engine;
- provider acquisition workflow;
- new provider model;
- new ontology, capability taxonomy, or gap taxonomy;
- active network probing;
- external provider lookup;
- Docker, sudo, socket reads, or network execution;
- permission creation or approval storage;
- diagnostic recording;
- service ownership, listener endpoint authority, storage ownership, network relationship, or full runtime-inventory generalization.

## Risks of premature generalization

- Treating `observation_permission` as an authority engine would overstate its current read-only permission visibility role.
- Treating `observation_domains` as a planner would confuse domain pressure with acquisition routes.
- Treating `privilege_discovery` as escalation behavior would violate its visibility-only boundary.
- Adding provider or gap taxonomies now would duplicate existing implementation constants before the single-container-ownership proof needs them.
- Generalizing to services, listeners, storage, or runtime inventory before this slice is stable would obscure the simple blocked proof: two observations, one authority class, two unavailable authority inputs.

## Recommended implementation scope

No broader authority-aware evaluator is needed for the first proof. The smallest code change that demonstrates the behavior is exactly a narrow, read-only `container_ownership_authority` evaluator plus tests and diagnostic visibility registration if exposed through CLI.

Because the repository already contains that evaluator and tests, the practical next implementation scope should be limited to preserving this slice and resisting generalization until a second desired observation proves that common shape is necessary.

## Files inspected

- `seed_runtime/container_ownership_authority.py`
- `seed_runtime/ownership_discrepancies.py`
- `seed_runtime/capability_needs.py`
- `seed_runtime/observation_domains.py`
- `seed_runtime/privilege_discovery.py`
- `seed_runtime/observation_permission.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `scripts/seed_local.py`
- `tests/test_container_ownership_authority.py`
- `tests/test_diagnostic_inventory.py`
- `tests/test_diagnostic_shape_audit.py`

## Files changed

- `docs/container_ownership_authority_minimal_slice_findings.md`

## LOC changed

- Added one report file, 227 lines.

## Tests run

- `pytest -q tests/test_container_ownership_authority.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`
