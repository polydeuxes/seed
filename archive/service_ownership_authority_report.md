---
doc_type: report
status: implemented
domain: service ownership authority evaluator
defines:
  - service ownership authority evaluator
  - service ownership authority diagnostic surface
  - service ownership authority implementation boundary
depends_on:
  - service_ownership_authority_slice_investigation.md
  - container_ownership_authority_cli_report.md
related:
  - listener_endpoint_authority_report.md
  - observation_goal_common_shape_investigation.md
---

# Service Ownership Authority Evaluator Report

## Files inspected

- `seed_runtime/container_ownership_authority.py`
- `scripts/seed_local.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `seed_runtime/ownership_discrepancies.py`
- `seed_runtime/capability_needs.py`
- `seed_runtime/privilege_discovery.py`
- `seed_runtime/observation_domains.py`
- `seed_runtime/observation_permission.py`
- `seed_runtime/observation_inventory.py`
- `tests/test_container_ownership_authority.py`
- `tests/test_diagnostic_inventory.py`
- `tests/test_diagnostic_shape_audit.py`

## Files changed

- `seed_runtime/service_ownership_authority.py`
- `scripts/seed_local.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `tests/test_service_ownership_authority.py`
- `docs/service_ownership_authority_report.md`

## LOC changed

`git diff --stat` reported 519 inserted lines and 1 deleted line before commit.

## Tests run

- `pytest -q tests/test_service_ownership_authority.py` — passed, 7 tests.
- `pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py tests/test_container_ownership_authority.py tests/test_service_ownership_authority.py` — passed, 41 tests.
- `python scripts/seed_local.py --service-ownership-authority --json` — passed and produced `outcome=partially_reachable`.

## Test results

The constrained authority profile produced:

- `desired_observation=service ownership`
- `reachable_observations=[tcp_listen_inventory, listener_process_inventory, systemd_unit_inventory]`
- `blocked_observations=[container_inventory, container_port_mapping]`
- `outcome=partially_reachable`

Boundary tests proved no event-ledger writes, no cluster mutation, no permission creation, and no provider acquisition.

## Inventory updates

Added `service_ownership_authority` to the diagnostic inventory with:

- `supports_json=true`
- `supports_record=false`
- `record_scope=none`
- `reads_diagnostic_facts=true`
- `writes_event_ledger=false`
- `uses_projected_state=true`
- `uses_repo_files=true`
- `mutates_cluster=false`

## Shape-audit updates

Added `service_ownership_authority` to diagnostic shape-audit implementation specs with:

- CLI flag `--service-ownership-authority`
- build function `evaluate_service_ownership_authority_slice`
- format function `format_service_ownership_authority`
- JSON function `service_ownership_authority_json`
- diagnostic fact read marker `build_capability_needs`
- repository-file marker `build_observation_inventory`

The shape audit reports this surface as consistent.

## Implementation deviations

- No generic authority evaluator, reachability engine, planner, provider acquisition, permission creation, event-ledger write, cluster mutation, active probing, or recording path was added.
- Systemd support is treated as local-passive service attribution based on existing privilege guidance for `systemd_inventory`; the bounded evaluator names the desired observation as `systemd_unit_inventory` because ownership discrepancy capability needs use that vocabulary.
- The evaluator preserves the supplied constrained authority profile as authoritative rather than deriving authority from approvals or creating permissions.

## Strongest supporting evidence

- `ownership_discrepancies` maps service ownership conflicts to local listener, listener process, systemd unit, container inventory, and container port-mapping capability needs.
- `privilege_discovery` maps listener process inventory to partial non-root visibility, container inventory and port mapping to Docker/root visibility, and systemd inventory to available read-only attribution.
- `observation_domains` maps listener process inventory to `local_listeners` and container inventory/port mapping to `container_runtime`.
- `observation_permission` recognizes `docker_socket_read` as a `local_privileged` observation activity.
- `observation_inventory` discovers listener and systemd predicate support.

## Strongest contradictory evidence

- `observation_domains.CAPABILITY_TO_DOMAIN` does not currently map `tcp_listen_inventory` or `systemd_unit_inventory`; the evaluator keeps those observations bounded and uses repository guidance rather than expanding the domain model.
- `privilege_discovery` names the guidance key `systemd_inventory`, while ownership discrepancy capability needs name `systemd_unit_inventory`; the evaluator bridges only this bounded service-ownership vocabulary mismatch and does not generalize it.
