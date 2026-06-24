# Container Ownership Authority CLI Findings

## Files inspected

- `AGENTS.md`
- `seed_runtime/container_ownership_authority.py`
- `scripts/seed_local.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `tests/test_container_ownership_authority.py`
- `tests/test_diagnostic_inventory.py`
- `tests/test_diagnostic_shape_audit.py`

## Files changed

- `seed_runtime/container_ownership_authority.py`
- `scripts/seed_local.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `tests/test_container_ownership_authority.py`
- `tests/test_diagnostic_inventory.py`
- `docs/container_ownership_authority_cli_report.md`

## Implementation summary

The existing `evaluate_container_ownership_authority_slice(...)` reasoning is now exposed through `seed --container-ownership-authority` with `--json` support. The CLI uses the existing evaluator with the constrained profile and does not add recording, execution, provider acquisition, permission creation, event-ledger writes, or cluster mutation.

Human-readable and JSON output preserve:

- Desired observation
- Required observations
- Required authority
- Available authority
- Outcome
- Remaining observations
- Uncertainty
- Boundary

## Inventory updates

The `container_ownership_authority` operational surface is registered in Diagnostic Inventory with:

- `supports_json=true`
- `supports_record=false`
- `record_scope=none`
- `uses_projected_state=true`
- `uses_repo_files=false`
- `reads_diagnostic_facts=true`
- `writes_event_ledger=false`
- `mutates_cluster=false`

`reads_diagnostic_facts` is true because the existing evaluator calls `build_capability_needs(...)` to detect subject-specific ownership pressure from diagnostic capability needs.

## Shape-audit updates

Diagnostic Shape Audit now includes an implementation spec for `container_ownership_authority`, checking the CLI flag, JSON renderer, formatter, evaluator function, projected-state use, diagnostic-fact reads, event-ledger behavior, record support, and cluster mutation boundary.

## Tests run

- `pytest -q tests/test_container_ownership_authority.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py` — passed, 34 tests.
- `python scripts/seed_local.py --container-ownership-authority` — passed, rendered blocked constrained-profile reasoning.
- `python scripts/seed_local.py --container-ownership-authority --json` — passed, emitted valid JSON.
- `python -m py_compile seed_runtime/container_ownership_authority.py scripts/seed_local.py seed_runtime/diagnostic_inventory.py seed_runtime/diagnostic_shape_audit.py` — passed.

## LOC changed

At the time of this report, `git diff --stat` showed 7 changed files with 252 insertions and 1 deletion (253 LOC changed).

## Deviations from requested scope

- `reads_diagnostic_facts` is declared true rather than false because implementation evidence shows the existing evaluator calls `build_capability_needs(...)`.
- No general authority evaluator, reachability engine, provider acquisition, authorization workflow, approval storage, automatic permission requests, or planning behavior was added.

## Recommended next slice

If another bounded visibility slice is needed, expose only a similarly implementation-backed authority or observation boundary that already exists internally, and register it through Diagnostic Inventory and Diagnostic Shape Audit before broadening any general framework.
