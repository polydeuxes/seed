# Container ownership authority slice report

## Mission question

This report scopes the smallest implementation-backed slice that can demonstrate authority-aware observation reasoning for one desired observation only:

```text
desired observation -> required observations -> required authority -> available authority -> reachable / blocked -> remaining uncertainty
```

The desired observation is `container ownership` under this constraint profile:

```text
root = unavailable
docker_socket_read = unavailable
active_network_probe = unauthorized
local_passive = available
external_provider_query = unknown
```

Repository authority wins. The conclusion is that the model can be proved with the existing `container ownership` path, but only as a narrow deterministic join over existing diagnostic outputs and implementation constants. It does not require a general reachability framework, provider acquisition, capability acquisition, or a new taxonomy.

## Files inspected

- `seed_runtime/ownership_discrepancies.py`
- `seed_runtime/capability_needs.py`
- `seed_runtime/privilege_discovery.py`
- `seed_runtime/observation_domains.py`
- `seed_runtime/observation_permission.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `scripts/seed_local.py`
- `tests/test_ownership_discrepancies.py`
- `tests/test_privilege_discovery.py`
- `tests/test_observation_domains.py`
- `tests/test_observation_permission.py`
- `docs/implicit_observation_workflow_investigation.md`
- `docs/observation_domain_conceptual_object_investigation.md`

## Existing implementation evidence

### 1. Container ownership already decomposes to container inventory and container port mapping pressure

The repository already has the needed ownership-discrepancy path for this slice. In `seed_runtime/ownership_discrepancies.py`, service ownership conflicts are mapped to capability needs. For `("service", "owner_not_observed")`, the mapped needs include:

```text
listener_process_inventory
container_port_mapping
container_inventory
```

For `("service", "insufficient_evidence")`, the mapped needs include:

```text
tcp_listen_inventory
process_inventory
container_inventory
```

This is the implementation-backed answer to whether current ownership-discrepancy and capability-need paths can derive `container_inventory + container_port_mapping` as required observations for unresolved service/container ownership attribution. The stronger `container_port_mapping` path is tied to `owner_not_observed`; `container_inventory` also appears for `insufficient_evidence`.

`diagnostic_capability_need_records()` emits diagnostic-only capability-need dictionaries from those rows. `build_capability_needs()` consumes those current diagnostic rows and recorded `diagnostic_run:` facts, grouping them by capability, subjects, diagnostics, needed evidence, and diagnostic runs.

Tests already preserve the important behavior:

- `test_unrecorded_owner_not_observed_listener_gap_surfaces_capability_need` proves the unrecorded current projection emits capability pressure from an ownership gap.
- `test_capability_needs_do_not_request_listener_process_when_observed` proves that when listener process evidence exists, `listener_process_inventory` is removed but `container_port_mapping` remains.
- `test_local_listener_does_not_infer_container_ownership_and_records_attribution_needs` proves local listener evidence does not become ownership truth and the attribution needs are diagnostic-scoped.

### 2. Container inventory and container port mapping already require docker-group or root-equivalent visibility

`seed_runtime/privilege_discovery.py` contains `_CAPABILITY_GUIDANCE` entries for both container capabilities:

```text
container_inventory -> docker_group_or_root
container_port_mapping -> docker_group_or_root
```

Both entries state that the suggested next step requires docker-group or root visibility. This is the implementation-backed equivalent authority requirement for the required observations. It is intentionally privilege discovery visibility, not escalation.

Tests already preserve this behavior:

- `test_privilege_discovery_renders_capability_access_pressure_and_guidance` asserts `container_inventory`, `docker_group_or_root`, and the docker-group/root guidance are rendered.
- `test_privilege_discovery_json_is_valid_and_includes_boundary_fields` asserts `container_port_mapping` reports `access_level == "docker_group_or_root"` and preserves `writes_event_ledger == false` and `mutates_cluster == false`.

### 3. Docker socket access is already a recognized permission domain

`seed_runtime/observation_permission.py` registers `docker_socket_read` as `local_privileged` in `SUPPORTED_OBSERVATION_CLASSES`. With no approval fact, `_domain_entry()` returns:

```text
permission_state = requires_operator_expression
reusable_permission = not_granted
future_autonomous_invocation = requires_operator_expression
```

The required scenario says `docker_socket_read = unavailable`, which is stricter than the default app output of `requires_operator_expression`. The smallest evaluator should therefore accept the supplied profile as input and treat `docker_socket_read` as unavailable rather than asking `observation_permission` to infer denial from state.

Tests already prove permission-domain shape and boundary behavior:

- `test_cli_observation_permission_json_is_valid` asserts `docker_socket_read` is included in the permission domains and that the report is read-only, does not write the event ledger, and does not mutate the cluster.
- `test_domain_class_permission_and_authority_visibility` proves known domains without approval require operator expression.

### 4. Container runtime visibility already exposes container capability pressure

`seed_runtime/observation_domains.py` maps:

```text
container_inventory -> container_runtime
container_port_mapping -> container_runtime
```

It always seeds `pressure_by_domain` with these existing mappings and also folds in current capability needs. With no container observation family, `build_observation_domains(..., "container_runtime")` reports:

```text
classification = unobserved
gap_type = missing_observation_domain
pressure = [container_inventory, container_port_mapping]
```

The app confirms this with:

```text
python scripts/seed_local.py --observation-domains container_runtime --json
```

The resulting JSON reports `read_only=true`, `writes_event_ledger=false`, `mutates_cluster=false`, `classification=unobserved`, and pressure for both container capabilities.

Tests already preserve this behavior in `test_unobserved_container_domain_visibility`.

## Required joins for the first slice

The first slice can be a deterministic join with hard-coded scope, using only existing names and fields:

1. Desired observation: fixed input `container ownership`.
2. Required observations:
   - Start with ownership capability needs produced by `build_capability_needs(state)` where `diagnostics` includes `ownership_discrepancies`.
   - Keep only `container_inventory` and `container_port_mapping`.
   - If no state-specific need exists, use `observation_domains.CAPABILITY_TO_DOMAIN` for `container_runtime` as repository-known pressure, but report that as domain-level pressure rather than subject-specific need.
3. Required authority:
   - Join each kept capability to `privilege_discovery._CAPABILITY_GUIDANCE` through `build_privilege_discovery(state)` or an equivalent read of its resulting capability rows.
   - For this slice, both capabilities require `docker_group_or_root`.
4. Available authority:
   - Read the supplied profile only:
     - `root = unavailable`
     - `docker_socket_read = unavailable`
     - `active_network_probe = unauthorized`
     - `local_passive = available`
     - `external_provider_query = unknown`
   - Optionally read `build_observation_permission(state, "docker_socket_read")` as implementation evidence that this is a known local-privileged observation domain, not to override the supplied profile.
5. Outcome:
   - If every container capability requires `docker_group_or_root` and both `root` and `docker_socket_read` are unavailable, report `blocked`.
6. Remaining observations:
   - `container_inventory`
   - `container_port_mapping`
7. Uncertainty:
   - `external_provider_query` remains `unknown`, but it is not part of the first deterministic reachability decision because no existing implementation evidence maps external provider query to container ownership acquisition for this slice.
   - If there is no subject-specific `ownership_discrepancies` row, the result is domain-level rather than subject-level.
   - `local_passive=available` can support local listener visibility, but current evidence does not make it sufficient for container inventory or port mapping.

## Minimal evaluation path

The smallest implementation-backed behavior can be added as one narrow helper and one narrow test module, or as an internal report object used by an existing investigation/test. It should not add a new CLI diagnostic unless the product specifically wants a new operational surface.

Recommended helper scope:

```python
def evaluate_container_ownership_authority_slice(state: State, profile: Mapping[str, str]) -> dict[str, Any]:
    ...
```

Minimal result shape:

```json
{
  "desired_observation": "container ownership",
  "required_observations": [
    "container_inventory",
    "container_port_mapping"
  ],
  "required_authority": {
    "container_inventory": ["docker_group_or_root"],
    "container_port_mapping": ["docker_group_or_root"]
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
    "external_provider_query unknown and not mapped to this first slice by implementation evidence",
    "local_passive available but not sufficient for docker_group_or_root container runtime evidence",
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

This proves the reasoning model without new ontology, a new capability taxonomy, a new gap taxonomy, a new provider model, or a planning framework. It is a productized join over existing capability-pressure, privilege-guidance, observation-domain, and observation-permission evidence.

## Participating code paths

Required for the first slice:

- `ownership_discrepancies`: supplies conflict-to-needed-evidence pressure for ownership gaps.
- `capability_needs`: normalizes current and recorded diagnostic-only capability needs.
- `privilege_discovery`: maps container capabilities to `docker_group_or_root` access guidance and preserves read-only/non-mutating boundaries.
- `observation_domains`: confirms `container_inventory` and `container_port_mapping` belong to the existing `container_runtime` pressure domain.
- `observation_permission`: confirms `docker_socket_read` is a recognized local-privileged permission domain and remains non-granted without approval.

Exact joins:

```text
container ownership
  -> ownership_discrepancies(service owner_not_observed or insufficient_evidence)
  -> diagnostic_capability_need_records()
  -> build_capability_needs()
  -> capabilities in {container_inventory, container_port_mapping}
  -> build_privilege_discovery() / _CAPABILITY_GUIDANCE
  -> access_level docker_group_or_root
  -> supplied profile root=unavailable and docker_socket_read=unavailable
  -> blocked
```

Domain and permission visibility support:

```text
container_inventory/container_port_mapping
  -> observation_domains.CAPABILITY_TO_DOMAIN
  -> container_runtime pressure

docker_socket_read
  -> observation_permission.SUPPORTED_OBSERVATION_CLASSES
  -> local_privileged / requires_operator_expression unless supplied profile denies it
```

## Code paths not required for the first slice

Do not include these in the first implementation:

- General reachability framework.
- Generic planner.
- Authority engine.
- Capability acquisition engine.
- Provider acquisition workflow.
- New provider model.
- New ontology or taxonomy.
- Active network probing.
- External provider lookup.
- Recording diagnostic facts.
- Permission creation or approval storage.
- Runtime execution of Docker, sudo, socket reads, or network probes.
- Broad evaluator for storage ownership, service ownership generally, listening services generally, network relationships, or full runtime inventory.

## Risks of premature generalization

- Treating `observation_permission` as an authority engine would overstate current behavior. It is visibility-only and does not enforce or create permissions.
- Treating `observation_domains` as a planner would overstate current behavior. It exposes coverage pressure, not an acquisition route.
- Treating `privilege_discovery` as escalation logic would violate its boundary. It only renders privilege guidance.
- Introducing generic gap/provider taxonomies before proving this slice risks duplicating concepts that already exist as implementation constants and tests.
- Promoting presentation vocabulary into preserved knowledge would violate the repository instruction to use implementation evidence first.

## Recommended implementation scope

Yes: Seed can prove the authority-aware observation reasoning model using only container ownership.

The smallest code change that demonstrates the behavior is a read-only, deterministic internal evaluator for exactly `container ownership` under a supplied profile, with tests that construct or monkeypatch existing capability needs and assert the blocked shape. It should:

- use existing capability names exactly as implemented: `container_inventory` and `container_port_mapping`;
- use existing authority guidance exactly as implemented: `docker_group_or_root`;
- treat supplied profile values as the authority decision source;
- report `blocked` when `root` and `docker_socket_read` are unavailable;
- return remaining observations and uncertainty without recording, acquiring providers, creating permissions, or executing observations.

If exposed later as a CLI diagnostic, the operational visibility contract requires registry, shape-audit specs, diagnostic-inventory tests, diagnostic-shape-audit tests, and the required diagnostic inventory/shape audit pytest command. For the first proof, keeping it internal avoids creating a new operational surface.

## Files changed

- `docs/container_ownership_authority_slice_report.md`

## LOC changed

- Added one report file, 304 lines.

## Tests and checks run

- `python scripts/seed_local.py --observation-domains container_runtime --json`
- `python scripts/seed_local.py --observation-permission docker_socket_read --json`
- `python scripts/seed_local.py --privilege-discovery --json`
- `python scripts/seed_local.py --db "$db" ingest ...` was attempted for ad hoc subject-specific setup, but the local model service was unavailable for free-form ingest commands. This does not invalidate the report because the implementation-backed path is already covered by existing tests and direct diagnostic commands.
