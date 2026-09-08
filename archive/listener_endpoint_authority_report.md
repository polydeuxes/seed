---
doc_type: report
status: implemented
domain: listener endpoint authority evaluator
defines:
  - listener endpoint authority evaluator
  - listener endpoint authority diagnostic surface
  - listener endpoint reachable observation outcome
depends_on:
  - service_ownership_authority_report.md
  - container_ownership_authority_cli_report.md
related:
  - reachable_observation_third_slice_investigation.md
  - observation_goal_common_shape_investigation.md
---

# Listener Endpoint Authority Implementation Report

## Files inspected

- `AGENTS.md`
- `seed_runtime/service_ownership_authority.py`
- `seed_runtime/container_ownership_authority.py`
- `seed_runtime/observation_inventory.py`
- `seed_runtime/observation_domains.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `scripts/seed_local.py`
- `tests/test_service_ownership_authority.py`
- `tests/test_container_ownership_authority.py`
- `tests/test_diagnostic_inventory.py`
- `tests/test_diagnostic_shape_audit.py`

## Files changed

- `seed_runtime/listener_endpoint_authority.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `scripts/seed_local.py`
- `tests/test_listener_endpoint_authority.py`
- `docs/listener_endpoint_authority_report.md`

## LOC changed

Measured with `git diff --numstat` before commit:

- Added: 486
- Deleted: 1
- Net: +485

## Tests run

- `pytest -q tests/test_listener_endpoint_authority.py`
- `pytest -q tests/test_listener_endpoint_authority.py tests/test_container_ownership_authority.py tests/test_service_ownership_authority.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

## Test results

- `tests/test_listener_endpoint_authority.py`: 7 passed.
- Focused authority/inventory/shape suite: 48 passed.

## Inventory updates

Registered `listener_endpoint_authority` in `DIAGNOSTIC_INVENTORY` with:

- `cli_flags=("--listener-endpoint-authority",)`
- `supports_json=True`
- `supports_record=False`
- `record_scope="none"`
- `reads_diagnostic_facts=False`
- `writes_event_ledger=False`
- `uses_projected_state=True`
- `uses_repo_files=True`
- `mutates_cluster=False`

## Shape-audit updates

Added a `DiagnosticImplementationSpec` for `listener_endpoint_authority` with:

- builder: `evaluate_listener_endpoint_authority_slice`
- formatter: `format_listener_endpoint_authority`
- JSON function: `listener_endpoint_authority_json`
- CLI flag: `--listener-endpoint-authority`
- repository implementation markers: `build_observation_inventory`, `build_observation_domains`

## Implementation deviations

- No generic authority evaluator, reachability engine, planner, provider acquisition path, permission creation path, active probe, event-ledger write, or cluster mutation was added.
- The evaluator returns `unknown` rather than forcing reachability if required implementation evidence is absent.
- `reads_diagnostic_facts` is declared false because the evaluator uses implementation inventory/domain evidence and does not call diagnostic-fact readers.

## Strongest supporting evidence

- `observation_inventory` discovers provider predicates from implementation AST evidence.
- Existing provider predicates include `listening_endpoint`, `listening_protocol`, `listening_address`, and `listening_port`.
- `observation_domains` recognizes `local_listeners` from listener/listening observation implementation evidence.
- Under the constrained profile, `local_passive=available`, and all bounded required observations require only `local_passive`.

## Strongest contradictory evidence

- The local listener domain can be classified as partially observed when ownership pressure exists, but that pressure is outside the bounded endpoint inventory goal.
- Local endpoint evidence does not prove process owner, service owner, container owner, application owner, health, responsiveness, external accessibility, DNS validity, remote reachability, causality, or intent; these remain explicit uncertainty outside the goal.
