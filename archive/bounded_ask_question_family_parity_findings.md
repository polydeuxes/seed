# Bounded `ask` Question Family parity findings

Date: 2026-06-26

## Scope

This investigation exercised every current Question Family from `seed --question-surface-inventory` through the bounded `seed ask --question-family "<exact question family>"` presentation and compared it with the existing direct inquiry surface.

The investigation is observational only. It does not redesign `ask`, change Question Family classifications, or recommend new routing behavior.

## Implementation evidence inspected

- `seed_runtime/question_surface_inventory.py` defines the current static Question Surface Inventory and the exact Question Family rows.
- `scripts/seed_local.py` defines `ASK_QUESTION_FAMILY_ELIGIBILITY`, `ASK_QUESTION_FAMILY_FLAGS`, and `apply_bounded_ask_dispatch`.
- `tests/test_question_surface_inventory.py` contains existing bounded `ask` parity and rejection tests for representative families.

## Commands executed

Inventory and implementation inspection:

```bash
cat AGENTS.md
rg --files -g 'AGENTS.md' -g '!venv' -g '!node_modules'
rg "Question Surface Inventory|question family|question-family|diagnostic-inventory|ask" -n . | head -200
sed -n '1,240p' tests/test_question_surface_inventory.py
rg "QUESTION|question_surface|question family|ask" -n scripts seed_runtime tests | head -300
sed -n '1,320p' seed_runtime/question_surface_inventory.py
sed -n '2080,2180p' scripts/seed_local.py
python scripts/seed_local.py --question-surface-inventory --json > /tmp/qsi.json
python - <<'PY'
import json
rows=json.load(open('/tmp/qsi.json'))
for r in rows: print(r['question_family'], r['surface_flag'])
PY
```

Direct and bounded comparison commands were generated from the inventory. For each eligible family, the direct surface was executed in human mode and JSON mode and compared to:

```bash
python scripts/seed_local.py ask --question-family "<exact question family>"
python scripts/seed_local.py ask --question-family "<exact question family>" --json
```

For parameterized direct surfaces, representative explicit parameters were used only to prove the direct surface still exists:

```bash
python scripts/seed_local.py --reasoning-path runtime web_service
python scripts/seed_local.py --reasoning-path runtime web_service --json
python scripts/seed_local.py --selection-path container_ownership
python scripts/seed_local.py --selection-path container_ownership --json
python scripts/seed_local.py --source-navigation build_question_surface_inventory
python scripts/seed_local.py --source-navigation build_question_surface_inventory --json
python scripts/seed_local.py --inquiry-orientation
python scripts/seed_local.py --inquiry-orientation --json
```

The full comparison harness wrote its raw summary to `/tmp/ask_results.json`.

## Classification counts

| Classification | Count |
| --- | ---: |
| `parity_pass` | 8 |
| `bounded_rejected_expected` | 6 |
| `missing_mapping` | 0 |
| `formatter_mismatch` | 2 |
| `json_mismatch` | 1 |
| `unexpected_success` | 0 |
| `unexpected_failure` | 0 |

## Classification table

| Question Family | Direct surface | Current bounded eligibility | Classification | Implementation-backed finding |
| --- | --- | --- | --- | --- |
| operational pressure | `--ops-brief` | `eligible_now` | `parity_pass` | Human and JSON output matched exactly. |
| current operational explanation | `--operational-story` | `eligible_now` | `parity_pass` | Human and JSON output matched exactly. |
| derivation explanation | `--reasoning-path DOMAIN SUBJECT` | `eligible_with_parameters` | `bounded_rejected_expected` | Bounded `ask` rejected with the expected `eligible_with_parameters` boundary. |
| selection explanation | `--selection-path TARGET` | `eligible_with_parameters` | `bounded_rejected_expected` | Bounded `ask` rejected with the expected `eligible_with_parameters` boundary. |
| knowledge reachability | `--knowledge-reachability-audit` | `eligible_now` | `json_mismatch` | Human output matched exactly. JSON did not: the direct JSON surface is `--knowledge-reachability-audit-json`, while bounded `ask --json` is rejected by generic `--json` validation. |
| capability pressure | `--capability-needs` | `eligible_now` | `parity_pass` | Human and JSON output matched exactly. |
| ownership ambiguity | `--ownership-discrepancies` | `eligible_now` | `parity_pass` | Human and JSON output matched exactly. |
| observation domain coverage | `--observation-domains` | `eligible_now` | `formatter_mismatch` | Bounded dispatch sets the `observation_domains` argument to boolean `True`, while the direct all-domains surface uses the parser constant `__all__`; human and JSON output both narrow to a synthetic `True` domain instead of matching all domains. |
| observation permission state | `--observation-permission` | `eligible_now` | `formatter_mismatch` | Bounded dispatch sets the `observation_permission` argument to boolean `True`, while the direct all-domains surface uses the parser constant `__all__`; human and JSON output both narrow to a synthetic `True` domain instead of matching all domains. |
| authority-constrained container ownership | `--container-ownership-authority` | `eligible_now` | `parity_pass` | Human and JSON output matched exactly. |
| authority-constrained service ownership | `--service-ownership-authority` | `eligible_now` | `parity_pass` | Human and JSON output matched exactly. |
| listener endpoint reachability | `--listener-endpoint-authority` | `eligible_now` | `parity_pass` | Human and JSON output matched exactly. |
| surface inventory | `--diagnostic-inventory` | `diagnostic_only` | `bounded_rejected_expected` | Bounded `ask` rejected with the expected `diagnostic_only` boundary. |
| surface shape validation | `--diagnostic-shape-audit` | `diagnostic_only` | `bounded_rejected_expected` | Bounded `ask` rejected with the expected `diagnostic_only` boundary. |
| source definition/import lookup | `--source-navigation QUERY` | `not_dispatchable` | `bounded_rejected_expected` | Bounded `ask` rejected with the expected `not_dispatchable` boundary. |
| inquiry orientation | `--inquiry-orientation [NOTE_ID]` | `not_dispatchable` | `bounded_rejected_expected` | Bounded `ask` rejected with the expected `not_dispatchable` boundary. |
| projection shape visibility | `--projection-shape` | `eligible_now` | `parity_pass` | Human and JSON output matched exactly. |

## Required answers

### 1. How many Question Families fall into each classification?

See the classification counts above: 8 `parity_pass`, 6 `bounded_rejected_expected`, 2 `formatter_mismatch`, 1 `json_mismatch`, and 0 for the remaining categories.

### 2. Which implemented families preserve complete presentation parity?

Complete human and JSON parity was observed for:

- operational pressure
- current operational explanation
- capability pressure
- ownership ambiguity
- authority-constrained container ownership
- authority-constrained service ownership
- listener endpoint reachability
- projection shape visibility

### 3. Which families are rejected exactly as intended?

Expected bounded rejection was observed for:

- derivation explanation (`eligible_with_parameters`)
- selection explanation (`eligible_with_parameters`)
- surface inventory (`diagnostic_only`)
- surface shape validation (`diagnostic_only`)
- source definition/import lookup (`not_dispatchable`)
- inquiry orientation (`not_dispatchable`)

### 4. Did any implemented dispatcher unexpectedly modify answer, reasoning, authority, boundaries, JSON, or formatter?

Yes.

- `observation domain coverage` changed the effective subject from the direct all-domain surface to a synthetic `True` domain, changing the human formatter output and JSON payload.
- `observation permission state` changed the effective subject from the direct all-domain surface to a synthetic `True` domain, changing the human formatter output and JSON payload.
- `knowledge reachability` preserved human output, but `ask --question-family "knowledge reachability" --json` did not reach the direct JSON renderer because the direct surface uses the separate `--knowledge-reachability-audit-json` switch rather than generic `--json`.

No answer/reasoning/authority/boundary modifications were observed for families classified as `parity_pass`.

### 5. Did any inventory entry fail because of an implementation mistake rather than an intentional boundary?

Yes. Three eligible entries exposed bounded dispatch implementation issues rather than intentional eligibility boundaries:

- `observation domain coverage`: `setattr(args, "observation_domains", True)` does not reproduce argparse's direct no-argument value of `__all__`.
- `observation permission state`: `setattr(args, "observation_permission", True)` does not reproduce argparse's direct no-argument value of `__all__`.
- `knowledge reachability`: bounded generic `--json` does not map to `knowledge_reachability_audit_json`, the direct JSON switch used by the implementation.

### 6. Does any implemented Question Family now appear to have the wrong eligibility classification based on observed behavior?

No. The observations show dispatch-value and JSON-switch mismatches for eligible families, not evidence that any Question Family's implementation-backed eligibility classification is wrong. The rejected families were rejected exactly according to their current implementation-backed classifications.

## Files changed

- `docs/bounded_ask_question_family_parity_findings.md`

## LOC changed

- Added 158 lines.

## Tests run

```bash
pytest -q tests/test_question_surface_inventory.py
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```
