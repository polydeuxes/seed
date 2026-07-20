# Post-1867 Python failure topology 001

Date: 2026-07-20
Branch head inspected: `363f667 Recover candidate resolution advancement lineage (#1867)`.

## Method

Commands run exactly as requested:

```bash
python -m compileall -q seed_runtime scripts
pytest -q
```

This topology is read-only with respect to runtime code, tests, generated architecture artifacts, workflows, and the Book. No repairs were attempted. The only repository file created by this operation is this report.

## 1. Suite result

| Metric | Count |
|---|---:|
| collected | 2294 |
| passed | 2238 |
| failed | 56 |
| errors | 0 |
| skipped | 0 |

`python -m compileall -q seed_runtime scripts` exited `0`.

`pytest -q` exited `1` after `56 failed, 2238 passed in 518.05s (0:08:38)`.

## 2. Failure-family table

| family ID | representative tests | failure count | shared producer or fixture | expected standing | actual standing | first divergence | classification | introduced / exposed / pre-existing |
|---|---|---:|---|---|---|---|---|---|
| F1 | `tests/test_runtime_loop.py::test_routes_answer`; `tests/test_api.py::test_post_user_message_answer_path_returns_runtime_response`; `tests/test_evaluations.py::test_evaluator_passes_matching_tool_call_case`; `tests/test_seed_local_script.py::test_normal_cli_answer_uses_runtime` | 45 | `Runtime.handle_user_message(...)`, `StaticDecisionProducer.decide(...)`, and CLI/app helpers that construct a `Runtime` with model-shaped `Decision` fixtures | A model/test `Decision` should be accepted as runtime authority and routed to answer/question/tool/refusal/state-patch/validation paths | Runtime records `runtime.decision_authority_unsupported` and returns `RuntimeResponse(kind="unsupported")`; direct evaluator calls to `StaticDecisionProducer.decide(...)` raise `RuntimeError` | `Runtime.__init__` discards the supplied decision producer (`self.decision_producer = None`) and `handle_user_message(...)` no longer calls `DecisionProducer.decide` or `_route`; `StaticDecisionProducer.decide(...)` is intentionally inert | E. unrelated pre-existing failure | Pre-existing relative to PR 1867. PR 1867 did not touch `seed_runtime/runtime.py`, API, evaluations, tool validation, tool recommendation, state patch, or seed-local runtime routing code. It exposed nothing necessary for candidate-resolution lineage; it simply leaves already-stale runtime-decision tests failing. |
| F2 | `tests/test_architecture_generator.py::test_architecture_graph_records_runtime_owner_boundaries` | 1 | Generated architecture graph consumed by the test, sourced from `Runtime.__seed_arch__` | Runtime architecture graph should contain `Runtime -> ToolExecutor` with `path=call_tool` and `Runtime -> ToolNeedService` with `path=request_tool` | Generated graph contains only `Runtime -> StateProjector` for Runtime-owned edges | `Runtime.__seed_arch__` declares `routes: []` and only the StateProjector edge; generated artifacts reflect that boundary, while the test still asserts old routing edges | C. generated artifact or architecture metadata drift | Introduced/exposed by PR 1867 only at the generated-artifact layer: PR 1867 changed `docs/generated/architecture/architecture_graph.json`, while runtime ownership metadata already says Runtime no longer routes tool decisions. The failing test is a generated-architecture expectation that no longer matches the runtime ownership boundary. |
| F3 | `tests/test_observation_inventory.py::test_providers_and_predicates_are_discovered_from_implementation`; `tests/test_consumer_dependency_audit.py::test_storage_canonical_predicate_consumers_are_not_orphaned` | 7 | AST-based `build_observation_inventory(...)`; downstream `build_observation_utilization_audit(...)` and `build_consumer_audit(...)` | Prometheus implementation predicates should include `up` and `filesystem_avail_bytes`, so filters for those predicates should return rows and consumers | Inventory omits `up` and `filesystem_avail_bytes`; filtered utilization/consumer audits return empty item lists | Inventory extraction recognizes `Observation(predicate=...)`, `_observation(..., predicate, ...)`, and selected `_QUESTIONS` constants, but Prometheus emits predicates via `PrometheusObservationShape(..., "up"/"filesystem_avail_bytes", ...)`; those constructor string literals are not harvested | E. unrelated pre-existing failure | Pre-existing relative to PR 1867. PR 1867 did not touch observation sources, observation inventory, utilization audit, predicate catalog, or consumer audit. |
| F4 | `tests/test_tool_validation.py::test_runtime_still_rejects_unregistered_tool_status_before_execution` | 1 | `tests/test_tool_validation.py` fixture mutating `runtime.tool_intent_guard.validate` | `Runtime` object should expose a mutable `tool_intent_guard` helper so this test can bypass intent validation and reach registry-status validation | `Runtime` has no `tool_intent_guard` attribute; AttributeError occurs before any decision routing assertion | Test fixture assumes a helper/API slot that is absent from current `Runtime`; this is an API-shape mismatch independent of the broader unsupported-response assertions | D. shared fixture/helper/API mismatch | Pre-existing relative to PR 1867. PR 1867 did not touch runtime tool validation helpers. This test is also secondarily blocked by F1 if the fixture mismatch were repaired, because current Runtime still does not route model-shaped decisions. |

## 3. Representative causal traces

### F1: Runtime model-decision authority excision versus stale routing tests

Trace:

```text
first representative failing test
→ tests/test_runtime_loop.py::test_routes_answer
→ fixture or constructor path
→ make_runtime(Decision(...)) constructs StaticDecisionProducer and passes it to Runtime(...)
→ runtime producer
→ Runtime.handle_user_message(...)
→ consumer
→ test expects returned RuntimeResponse and event ledger route event
→ expected standing
→ accepted model-shaped Decision routes to response.answer / tool_need / tool_result / invalid_decision / state_updated, etc.
→ actual standing
→ unsupported runtime response; ledger contains input.user_message plus runtime.decision_authority_unsupported
→ earliest divergence
→ Runtime.__init__ ignores the supplied decision_producer and Runtime.handle_user_message never calls producer/validator/router
```

Direct executable evidence:

- `test_routes_answer` expected `response.kind == "answer"`; actual was `"unsupported"`.
- `test_post_user_message_answer_path_returns_runtime_response` expected API result kind `"answer"`; actual was `"unsupported"`.
- `test_evaluator_passes_matching_tool_call_case` reached `StaticDecisionProducer.decide(...)`; actual raised `RuntimeError: DecisionProducer.decide is unsupported: model-shaped Decisions are not Seed authority`.
- Seed-local CLI tests expected recommendations, event output, raw runtime continuation, or deterministic fallback routing; actual output included `No Seed-owned runtime decision authority is configured for free-text input.`

Downstream repetitions assigned here:

- API response routing failures: 2.
- Architecture invariant runtime-routing failures: 2.
- Capability catalog runtime tool-need failures: 2.
- Evaluation producer failures: 3.
- Runtime loop failures: 14.
- Seed-local runtime/CLI failures: 11.
- State patch runtime-routing failures: 2.
- Tool intent runtime-routing failures: 3.
- Tool recommendation runtime-routing/payload failures: 5.
- Tool validation runtime-routing failures: 3 of 4.

The earliest divergence is not `candidate_resolution_id`; none of these failures depends on `GoalConsiderationCandidateResolution.resolution_id`, `selection_id`, or goal-selection lineage. The distinction `GoalConsiderationCandidateResolution.resolution_id != selection_id` is not violated by the observed failures.

### F2: Architecture generated graph expectation no longer matches Runtime ownership metadata

Trace:

```text
first representative failing test
→ tests/test_architecture_generator.py::test_architecture_graph_records_runtime_owner_boundaries
→ fixture or constructor path
→ GRAPH_PATH = docs/generated/architecture/architecture_graph.json
→ runtime producer
→ Runtime.__seed_arch__ consumed by scripts/generate_architecture.py-generated graph
→ consumer
→ architecture test asserts old Runtime routing edges
→ expected standing
→ Runtime has call_tool-only edge to ToolExecutor and request_tool edge to ToolNeedService
→ actual standing
→ graph has Runtime edge only to StateProjector
→ earliest divergence
→ Runtime.__seed_arch__ states routes=[] and omits ToolExecutor/ToolNeedService edges
```

This is not downstream of F1's runtime execution path: the generated graph is a static artifact/metadata consumer. However, it shares the same conceptual removal of Runtime-owned decision routing.

### F3: Observation predicate inventory misses Prometheus shape constructors

Trace:

```text
first representative failing test
→ tests/test_observation_inventory.py::test_providers_and_predicates_are_discovered_from_implementation
→ fixture or constructor path
→ build_observation_inventory()
→ runtime producer
→ AST scanner over seed_runtime/*.py provider classes
→ consumer
→ observation inventory/utilization/consumer audit tests
→ expected standing
→ predicates include os, hostname, up, filesystem_avail_bytes
→ actual standing
→ up/filesystem_avail_bytes absent from inventory, filtered audits have zero rows
→ earliest divergence
→ _predicate_literals does not harvest PrometheusObservationShape string predicate arguments
```

Downstream repetitions assigned here:

- Observation inventory missing `up`: 2.
- Observation utilization missing `up`: 2.
- Consumer dependency audit missing `filesystem_avail_bytes`: 3.

The producer implementation still contains Prometheus safe query and shape code that can emit `up` and filesystem predicates. The divergence is in implementation discovery, not in the Prometheus runtime emission path itself.

### F4: Tool validation fixture assumes absent Runtime helper/API

Trace:

```text
first representative failing test
→ tests/test_tool_validation.py::test_runtime_still_rejects_unregistered_tool_status_before_execution
→ fixture or constructor path
→ make_runtime(...) returns Runtime
→ runtime producer
→ test mutates runtime.tool_intent_guard.validate before execution
→ consumer
→ test fixture wants to force intent validation success and then assert registry-status rejection
→ expected standing
→ Runtime exposes tool_intent_guard helper
→ actual standing
→ AttributeError: 'Runtime' object has no attribute 'tool_intent_guard'
→ earliest divergence
→ current Runtime constructor does not create tool_intent_guard, and current runtime boundary does not expose that helper
```

This is classified separately because its first failing operation is fixture/API access, not an `unsupported` RuntimeResponse. If the helper/API mismatch were repaired alone, this test would likely then collapse into F1 unless Runtime decision authority/routing semantics were also intentionally restored or tests were re-scoped.

## 4. Dependency collapse

```text
raw failures: 56
→ causal families: 4
→ independent repair boundaries: 3 primary + 1 secondary/API boundary
```

Detailed collapse:

```text
56 raw failures
├─ F1 Runtime model-decision authority excision vs stale runtime-routing consumers: 45
├─ F2 Runtime architecture generated graph / metadata expectation mismatch: 1
├─ F3 observation inventory AST discovery misses Prometheus shape predicates: 7
└─ F4 absent runtime.tool_intent_guard fixture/API slot: 1

Independent repair boundaries by causal depth:
1. Decide/test the Runtime input-boundary contract after model-decision authority excision (F1; F2 is adjacent but static).
2. Repair observation inventory discovery for PrometheusObservationShape predicates, if current implementation intends those predicates to remain inventory-visible (F3).
3. Reconcile tool-validation fixture/helper API assumptions with the current Runtime boundary (F4), likely after F1 because F4 is partly masked by the same runtime authority removal.
```

F2 could be handled with F1 only if the chosen next operation is a contract decision around Runtime ownership. If the runtime boundary is intentionally unsupported, F2 is a stale generated-architecture assertion; if routing is to be restored, F2 becomes a metadata/artifact repair.

## 5. 1867 impact

### What 1867 repaired successfully

PR 1867's stated and touched area was candidate-resolution advancement lineage. The post-merge suite evidence did not reveal failures in the 1867-touched advancement-need, inquiry, authority, clarification, sufficiency, bounded-frontier, or operational-realization test files. Those tests are included in the 2238 passing tests.

### What 1867 broke

Executable failure evidence does not show a direct implementation regression in PR 1867-touched runtime code for the failing families:

- F1 is rooted in `seed_runtime/runtime.py`, which PR 1867 did not modify.
- F3 is rooted in observation inventory/source discovery code, which PR 1867 did not modify.
- F4 is rooted in an absent `Runtime.tool_intent_guard` helper/API, which PR 1867 did not modify.

The only PR-1867-touched failing area is F2: the generated architecture graph changed in PR 1867 and now lacks the old Runtime routing edges expected by `tests/test_architecture_generator.py::test_architecture_graph_records_runtime_owner_boundaries`. The generator stability test passed, so the artifact is stable; the divergence is the expected architecture standing, not a nondeterministic generation failure.

### What 1867 merely exposed

PR 1867 exposed/left visible the existing split between:

- old tests and CLI/API fixtures that still treat model-shaped `Decision` objects as runtime authority; and
- current runtime code that refuses that authority and returns an unsupported boundary response.

It also left visible an older observation discovery gap where Prometheus predicates emitted through `PrometheusObservationShape` are not visible to inventory/utilization/consumer-audit surfaces.

### What remains unrelated

F3 and F4 remain unrelated to PR 1867's candidate-resolution lineage. F1 is unrelated to PR 1867's files but related to a broader prior runtime ontology/boundary excision. F2 is related to PR 1867's generated architecture artifact but not to candidate-resolution behavior.

## 6. Next lawful operation

Smallest next repair boundary supported by the topology, ordered by causal depth rather than failure count convenience:

1. **Runtime input-boundary contract decision (F1, then F2).** Determine whether tests should preserve the current no-internal-model-decision-authority contract or whether a Seed-owned deterministic runtime decision authority should exist. Do not restore deleted focus-selection vocabulary or compatibility aliases. If the current boundary is intentional, update only the stale runtime/API/CLI/evaluation/architecture tests to assert the unsupported boundary and remove assumptions that `DecisionProducer.decide -> Runtime._route` is a live Seed authority path. If a new Seed-owned authority is intended, implement it as a new explicit boundary rather than reviving model-shaped `Decision` authority.
2. **Observation inventory discovery repair (F3).** If Prometheus `up` and filesystem predicates remain implementation-backed surfaces, extend the inventory discovery to include `PrometheusObservationShape` predicate arguments and preserve consumer-audit coverage.
3. **Tool validation fixture/API reconciliation (F4).** Revisit only after F1 because the missing helper is a fixture/API mismatch that otherwise leads into the same removed runtime routing path.

## Stop condition confirmation

Every failing test in the captured `pytest -q` run is assigned to a causal family above. No failures were left insufficiently classified.

```text
first causal family to repair
→ F1 Runtime model-decision authority excision versus stale runtime-routing tests
→ evidence supporting that choice
→ it is the earliest executable divergence for 45/56 failures and sits upstream of API, CLI, tool recommendation, tool validation, state patch, and capability-catalog runtime-path assertions; it also informs whether the architecture graph expectation in F2 should be stale-test repair or metadata repair
→ failures expected to disappear if repaired
→ the 45 F1 failures directly; F2 may disappear if the repair intentionally restores Runtime routing metadata, or will become a straightforward stale architecture-test update if the unsupported boundary is confirmed
```
