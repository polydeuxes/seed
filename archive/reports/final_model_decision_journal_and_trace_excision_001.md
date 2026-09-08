# Final model-decision journal and trace excision 001

## Bounded conclusion

Yes, this pass stops active code and tests from manufacturing or presenting the deleted model-decision history through `DecisionJournal` and `RuntimeTrace`.

This report does not claim that all LLM contamination has been removed. It only records the bounded cleanup of the residual model-decision journal and decision-shaped runtime trace family.

## Exact files deleted

- `seed_runtime/decision_journal.py`
- `seed_runtime/runtime_trace.py`
- `tests/test_decision_journal.py`
- `tests/test_runtime_trace.py`
- `tests/test_cli_trace.py`

## Imports and exports removed

- Removed `seed_runtime.runtime_trace` imports from `seed_runtime/__init__.py`.
- Removed `RuntimeTrace`, `RuntimeTraceEvent`, `RuntimeTraceReader`, and `load_runtime_trace` from the package `__all__` export list in `seed_runtime/__init__.py`.
- Removed `RuntimeTrace` and `load_runtime_trace` imports from `scripts/seed_local.py`.
- No compatibility aliases or stubs were added for deleted journal or trace symbols.
- No generic replacement hash helper was added for `context_hash` / `context_hash_payload`.

## CLI surfaces removed

Removed the following parser options, lifecycle exclusivity checks, dispatch branches, and formatting/loading helpers from `scripts/seed_local.py`:

- `--trace-run`
- `--why-run`
- `runtime_trace_from_args`
- `format_runtime_trace`
- `format_runtime_why`
- `_format_trace_value`
- `_trace_policy_allowed`
- `_why_decision_phrase`
- `_why_policy_phrase`

## Tests and fixtures removed

Removed the tests and fixtures that manufactured or asserted the deleted story:

```text
input.user_message
→ decision.recorded
→ policy result
→ selected tool
→ tool result
→ assistant.answer
```

Deleted test files:

- `tests/test_decision_journal.py`
- `tests/test_runtime_trace.py`
- `tests/test_cli_trace.py`

## Active documentation residue removed

Removed current architectural / active ownership claims for the deleted family from:

- `docs/archive/original_book_of_seed/01-architecture.md`
- `docs/archive/original_book_of_seed/03-runtime-loop.md`
- `docs/architecture.md`
- `docs/capability_ownership_matrix.md`
- `docs/execution_inquiry_orientation_investigation.md`
- `docs/execution_characterization_inquiry_surface_investigation.md`
- `docs/runtime_responsibility_reconciliation.md`

Historical reports that remain in `docs/` or root-level investigation files were not treated as active code/test consumers during this bounded pass.

## Verification searches

Searched active code and tests with:

```bash
rg -n "DecisionJournal|DecisionRecord|DecisionOutcome|decision\.recorded|context_hash|context_hash_payload|RuntimeTrace|RuntimeTraceReader|load_runtime_trace|build_runtime_trace|get_runtime_trace|--trace-run|--why-run|Seed decided to|Policy allowed the decision|runtime\.decision\.provider_failed" seed_runtime scripts tests -g '*.py'
```

Result: no active Python code or tests reference the deleted journal/trace symbols, event kind, context hash helpers, removed CLI flags, or deleted decision-shaped presentation phrases.

## Interactive runtime behavior preserved

Ran:

```bash
printf 'hello\nexit\n' | python scripts/seed_local.py
```

Observed output:

```text
Seed local shell. Press Ctrl-D or type 'exit' to quit.
seed> No Seed-owned runtime decision authority is configured for free-text input.
seed>
```

This preserves the bounded runtime tombstone behavior for unsupported free-text movement:

```text
operator input is recorded
unsupported free-text movement is refused
```

## Full test result

Commands run:

- `python -m compileall -q seed_runtime scripts` — passed.
- `python scripts/seed_local.py --help` — passed and no longer lists `--trace-run` or `--why-run`.
- `printf 'hello\nexit\n' | python scripts/seed_local.py` — passed with unchanged deterministic refusal output.
- `pytest -q` — failed with 15 unrelated failures.

The full test run completed with:

```text
15 failed, 2146 passed in 475.92s (0:07:55)
```

## Unrelated failures left untouched

The failing tests are unrelated to this deletion pass and were left untouched:

- `tests/test_candidate_requests.py::test_candidate_requests_cli_is_read_only_and_does_not_build_runtime`
- `tests/test_candidate_requests.py::test_candidate_routes_cli_is_read_only_and_does_not_build_runtime`
- `tests/test_capability_candidates.py::test_capability_candidates_cli_is_read_only_json_and_avoids_runtime`
- `tests/test_capability_promotion_readiness.py::test_promotion_readiness_cli_is_read_only_json_and_avoids_runtime`
- `tests/test_capability_verification_inspection.py::test_capability_verification_cli_is_read_only_json_and_avoids_runtime`
- `tests/test_confidence.py::test_cli_confidence_commands_do_not_append_or_invoke_runtime_provider_policy_or_tools`
- `tests/test_consumer_dependency_audit.py::test_storage_canonical_predicate_consumers_are_not_orphaned`
- `tests/test_consumer_dependency_audit.py::test_storage_consumer_audit_json_reflects_corrected_counts`
- `tests/test_consumer_dependency_audit.py::test_storage_consumer_audit_human_output_remains_valid`
- `tests/test_contradictions.py::test_cli_contradiction_command_does_not_invoke_runtime_provider_policy_or_tools`
- `tests/test_observation_inventory.py::test_providers_and_predicates_are_discovered_from_implementation`
- `tests/test_observation_inventory.py::test_filtering_works`
- `tests/test_observation_utilization.py::test_predicates_are_discovered_from_observation_inventory_implementation`
- `tests/test_observation_utilization.py::test_filtering_works_for_predicate_and_provider`
- `tests/test_verification_evidence.py::test_verification_evidence_cli_is_read_only_and_survives_absent_execution`

## Runtime tombstone vocabulary

Runtime tombstone vocabulary was preserved for a separate bounded cross-examination:

```text
legitimate deterministic refusal responsibility
!=
stale negative-image description of the deleted model road
```

No redesign of ingress, no replacement abstraction, and no recovered generic trace/journal/context/command/agent/run/orchestration/decision architecture was introduced in this pass.
