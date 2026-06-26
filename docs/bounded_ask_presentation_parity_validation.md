# Bounded ask presentation parity validation

This reconciliation remains observational. It validates the current repository implementation against the claimed bounded `ask` model:

```text
Question Family -> exact lookup -> deterministic dispatch -> existing inquiry surface -> existing answer
```

Repository authority wins. In the inspected implementation, the direct inquiry surfaces exist, but no executable bounded `ask` surface is registered in `scripts/seed_local.py`. Therefore parity cannot be proven as perfect: the direct surfaces answer, while the tested `ask` invocation is rejected by argparse as an unrecognized positional argument.

## Selected Question Families

Exactly two Question Families were validated.

| Question Family | Why selected |
| --- | --- |
| `authority-constrained service ownership` | Required by the task. The question-surface inventory maps it to `service_ownership_authority` and `--service-ownership-authority`. |
| `listener endpoint reachability` | Selected as the one additional representative family because it requires no parameters, is immediately eligible, and uses a different implementation module and evaluator path (`listener_endpoint_authority`) than service ownership. |

No other Question Families were validated.

## Implementation evidence

The question-surface inventory is static data. Each row carries `question_family`, example questions, `surface`, `surface_flag`, answer responsibility, authority boundary, and notes. Formatting that inventory only renders the row fields; it does not route or execute questions.

The service-ownership direct surface dispatches from `args.service_ownership_authority` to `evaluate_service_ownership_authority_slice(state, CONSTRAINED_AUTHORITY_PROFILE)`, then uses `service_ownership_authority_json(result)` for JSON or `format_service_ownership_authority(result)` for human output.

The listener-endpoint direct surface dispatches from `args.listener_endpoint_authority` to `evaluate_listener_endpoint_authority_slice(state, LISTENER_ENDPOINT_AUTHORITY_PROFILE)`, then uses `listener_endpoint_authority_json(result)` for JSON or `format_listener_endpoint_authority(result)` for human output.

The inspected CLI has no `ask` parser, no `--question-family` argument, and no `args.ask` dispatch. Running `python scripts/seed_local.py ask --question-family ...` exits with status 2 and prints argparse usage. That is an implementation-backed behavior difference, not a presentation-only difference.

## Family 1: authority-constrained service ownership

| Required field | Finding |
| --- | --- |
| Question Family | `authority-constrained service ownership` |
| Direct surface | `python scripts/seed_local.py --service-ownership-authority` and `python scripts/seed_local.py --service-ownership-authority --json` |
| Ask surface | Tested as `python scripts/seed_local.py ask --question-family "authority-constrained service ownership"`; current implementation rejects it with status 2. |
| Answer parity | **Behavior difference.** Direct surface answers `outcome=partially_reachable`; ask does not dispatch to the answer. |
| JSON parity | **Behavior difference.** Direct JSON contains the service ownership payload; ask produces no JSON payload. |
| Formatter parity | **Behavior difference.** Direct human formatter renders `Service Ownership Authority`; ask prints argparse usage instead. |
| Reasoning parity | **Behavior difference by absence.** Direct reasoning is the evaluator's composite local service attribution slice; ask does not reach it. |
| Authority parity | **Behavior difference by absence.** Direct authority uses the constrained authority profile and evaluator-required authority map; ask performs no authority evaluation. |
| Boundary parity | **Behavior difference by absence.** Direct result declares read-only/no-record/no-ledger/no-mutation boundary; ask returns parser error before a boundary-bearing result exists. |
| Overall parity | **Not preserved in current implementation.** The direct inquiry exists, but bounded ask is not executable in this checkout. |

### Direct direct-surface observations

The direct JSON output reports:

- `desired_observation`: `service ownership`
- `current_strategy`: `composite_local_service_attribution_observation`
- `outcome` and `strategy_status`: `partially_reachable`
- reachable observations: `tcp_listen_inventory`, `listener_process_inventory`, `systemd_unit_inventory`
- blocked/remaining observations: `container_inventory`, `container_port_mapping`
- blocking boundary: `docker_or_root_container_runtime_authority_unavailable`
- boundary: `read_only=true`, `records=false`, `writes_event_ledger=false`, `mutates_cluster=false`, `provider_acquisition=false`, `permission_creation=false`, `executes_observation=false`

The direct human output renders the same answer shape under `Service Ownership Authority`, including goal, strategy, observation state, authority, execution, uncertainty, and boundary sections.

## Family 2: listener endpoint reachability

| Required field | Finding |
| --- | --- |
| Question Family | `listener endpoint reachability` |
| Direct surface | `python scripts/seed_local.py --listener-endpoint-authority` and `python scripts/seed_local.py --listener-endpoint-authority --json` |
| Ask surface | Tested as `python scripts/seed_local.py ask --question-family "listener endpoint reachability"`; current implementation rejects it with status 2. |
| Answer parity | **Behavior difference.** Direct surface answers `outcome=reachable`; ask does not dispatch to the answer. |
| JSON parity | **Behavior difference.** Direct JSON contains the listener endpoint payload; ask produces no JSON payload. |
| Formatter parity | **Behavior difference.** Direct human formatter renders `Listener Endpoint Authority`; ask prints argparse usage instead. |
| Reasoning parity | **Behavior difference by absence.** Direct reasoning comes from the listener endpoint evaluator and observation inventory/domain evidence; ask does not reach it. |
| Authority parity | **Behavior difference by absence.** Direct authority uses local passive authority requirements and the listener endpoint authority profile; ask performs no authority evaluation. |
| Boundary parity | **Behavior difference by absence.** Direct result declares local endpoint scope and excludes ownership/health/reachability claims; ask returns parser error before a boundary-bearing result exists. |
| Overall parity | **Not preserved in current implementation.** The direct inquiry exists, but bounded ask is not executable in this checkout. |

### Direct direct-surface observations

The direct JSON output reports:

- `desired_observation`: `local listener endpoint inventory`
- `outcome`: `reachable`
- required/reachable observations: `listening_protocol`, `listening_address`, `listening_port`, `local_socket_table_evidence`
- required authority: all required observations require `local_passive`
- blocked observations: none
- boundary: read-only, non-recording, no event-ledger writes, no cluster mutation, no provider acquisition, no permission creation, no observation execution
- scope: local TCP/UDP endpoint inventory only
- exclusions: process ownership, service ownership, application ownership, container ownership, health, responsiveness, external accessibility, DNS validity, remote network reachability, causality, and intent

The direct human output renders the same answer shape under `Listener Endpoint Authority`, including desired observation, required observations, required/available authority, reachable/blocked observations, outcome, uncertainty, and boundary.

## Additional Questions

### 1. Does `ask` introduce any reasoning of its own?

No implementation-backed `ask` reasoning was found. The CLI has no executable `ask` path in `scripts/seed_local.py`, and the failed tested invocation exits during argument parsing. Therefore `ask` neither introduces reasoning nor preserves direct-surface reasoning in this checkout.

### 2. Does `ask` introduce any authority evaluation?

No. The only authority evaluation observed is in the direct evaluators. Service ownership constructs available authority from the supplied constrained profile and computes required/reachable/blocked observations. Listener endpoint authority separately evaluates local listener endpoint reachability with local passive authority. The tested `ask` invocation performs no authority evaluation because it is not registered.

### 3. Does `ask` modify the inquiry result?

No implemented result-modification path was found because no implemented `ask` dispatch path was found. The direct surfaces return formatter/JSON output directly from the evaluator result adapters.

### 4. Does `ask` preserve JSON parity?

No, not in the current executable implementation. The direct surfaces produce JSON payloads; tested ask invocations produce argparse errors and no JSON result.

### 5. Does `ask` preserve formatter parity?

No, not in the current executable implementation. The direct surfaces invoke their existing human formatters; tested ask invocations print CLI usage rather than formatter output.

### 6. Does any implementation detail unexpectedly leak through the new presentation layer?

There is no new presentation layer to inspect in this checkout. The observed leakage is the absence-mode argparse surface: `ask` is treated as an unexpected positional `message`, and `--question-family` is treated as an unrecognized argument. That leaks the current CLI implementation shape rather than a bounded Question Family presentation.

Direct surfaces intentionally expose implementation-backed fields such as surface names, authority labels, observation identifiers, and boundary metadata in their existing answer payloads. This report does not classify those existing direct-surface fields as new `ask` leakage.

### 7. If parity is not perfect, what is the smallest implementation-backed cause?

The smallest implementation-backed cause is absence of an executable bounded `ask` CLI path: no `ask` parser/subcommand, no `--question-family` argument, and no deterministic dispatch branch from a Question Family to the existing direct surfaces in `scripts/seed_local.py`.

## Acceptance answers

### Has ask remained a pure presentation layer?

Not provable from this checkout. Repository authority shows the direct inquiry surfaces exist, but bounded `ask` is not executable. Because there is no implemented dispatch, it has not acquired visible reasoning or authority responsibility; it also has not yet demonstrated presentation-layer parity.

### Did ask accidentally acquire any architectural responsibility?

No implementation-backed evidence shows that `ask` acquired reasoning, authority evaluation, answer modification, routing beyond exact dispatch, natural-language interpretation, parameter inference, or planning. The stronger finding is that no executable bounded `ask` responsibility is present in the inspected CLI.

### Is the repository now ready to expand ask to the remaining immediately eligible Question Families?

No. The repository is not ready to expand `ask` based on this validation, because the current implementation does not demonstrate parity for the required service-ownership family or the selected listener-endpoint family. The next readiness gate is implementation-backed parity for the bounded ask surface itself, not expansion to additional families.

## Report

### Commands executed

```text
pwd
rg --files -g 'AGENTS.md' -g '!venv' -g '!node_modules'
git status --short
cat AGENTS.md
rg "ask|Question Family|service ownership|diagnostic-inventory|shape-audit" -n .
rg -n "subparsers|ask|question_family|question-surface|QuestionSurface|service_ownership|documentation_structure|knowledge-reachability" scripts/seed_local.py seed_runtime tests docs/bounded_ask* docs/*ask* | head -n 300
sed -n '1,220p' seed_runtime/question_surface_inventory.py
rg -n "ask" scripts/seed_local.py | head -n 80
sed -n '1120,1240p' scripts/seed_local.py
sed -n '2360,2425p' scripts/seed_local.py
sed -n '220,340p' seed_runtime/question_surface_inventory.py
rg -n "service_ownership_authority|listener_endpoint_authority|question_surface_inventory|knowledge_reachability_audit" scripts/seed_local.py | head -n 120
sed -n '2128,2165p' scripts/seed_local.py
sed -n '6168,6228p' scripts/seed_local.py
sed -n '6700,6768p' scripts/seed_local.py
rg -n "question-family|ask --|ask" scripts seed_runtime tests | head -n 200
python scripts/seed_local.py --help | head -n 80
which seed || true
seed --help | head -n 40 || true
python scripts/seed_local.py --service-ownership-authority > /tmp/service_human.txt
python scripts/seed_local.py --service-ownership-authority --json > /tmp/service_json.txt
python scripts/seed_local.py --listener-endpoint-authority > /tmp/listener_human.txt
python scripts/seed_local.py --listener-endpoint-authority --json > /tmp/listener_json.txt
python scripts/seed_local.py ask --question-family "authority-constrained service ownership" > /tmp/ask_service.txt 2>&1; echo ask_service_status=$?
python scripts/seed_local.py ask --question-family "listener endpoint reachability" > /tmp/ask_listener.txt 2>&1; echo ask_listener_status=$?
wc -l /tmp/service_human.txt /tmp/service_json.txt /tmp/listener_human.txt /tmp/listener_json.txt /tmp/ask_service.txt /tmp/ask_listener.txt
head -n 40 /tmp/ask_service.txt
head -n 120 /tmp/service_json.txt
head -n 90 /tmp/listener_json.txt
head -n 80 /tmp/service_human.txt
sed -n '1,220p' seed_runtime/listener_endpoint_authority.py
sed -n '95,160p' seed_runtime/service_ownership_authority.py
```

### Files inspected

- `AGENTS.md`
- `scripts/seed_local.py`
- `seed_runtime/question_surface_inventory.py`
- `seed_runtime/service_ownership_authority.py`
- `seed_runtime/listener_endpoint_authority.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `tests/test_question_surface_inventory.py`
- `tests/test_service_ownership_authority.py`
- `docs/bounded_ask_routing_reconciliation.md`
- `docs/bounded_ask_question_family_eligibility_audit.md`
- `docs/ask_question_family_dispatch_reconciliation.md`

### Files changed

- `docs/bounded_ask_presentation_parity_validation.md`

### LOC changed

- Added one 213-line documentation report. Runtime code, tests, diagnostic inventory, and diagnostic shape-audit specs were not changed.

### Tests run

No automated test suite was required by this documentation-only validation. The direct CLI checks listed above were run as implementation validation.

### Validated Question Families

- `authority-constrained service ownership`
- `listener endpoint reachability`

### Parity summary

| Question Family | Direct surface | Ask surface | Answer parity | JSON parity | Formatter parity | Reasoning parity | Authority parity | Boundary parity | Overall parity |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `authority-constrained service ownership` | `--service-ownership-authority` | `ask --question-family "authority-constrained service ownership"` | behavior difference | behavior difference | behavior difference | behavior difference by absence | behavior difference by absence | behavior difference by absence | not preserved |
| `listener endpoint reachability` | `--listener-endpoint-authority` | `ask --question-family "listener endpoint reachability"` | behavior difference | behavior difference | behavior difference | behavior difference by absence | behavior difference by absence | behavior difference by absence | not preserved |
