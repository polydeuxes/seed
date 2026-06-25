# Observation execution transition investigation

## Scope

This is an observational reconciliation of the current implementation boundary between bounded reasoning and observation execution. It does not propose an execution engine, scheduler, planner, orchestration framework, or generic observation pipeline.

Repository authority wins: the findings below are limited to behavior observed through existing commands and implementation directly involved in observation collection, ingestion, provider acquisition, runtime registered-tool execution, validation, and policy refusal.

## Commands executed

```text
python scripts/seed_local.py --help
python scripts/seed_local.py --observe-local-host --quiet-output --observe-timings --record --db /tmp/seed_obs.db
python scripts/seed_local.py --observe-prometheus http://127.0.0.1:1 --observe-timeout 1 --quiet-output --observe-timings --record --db /tmp/seed_prom.db
python scripts/seed_local.py --observe-json /tmp/nope.json --quiet-output --record --db /tmp/seed_bad.db
rg -n "argparse|def main|--.*observation|diagnostic-inventory|diagnostic-shape-audit|call_tool|ToolExecutor|ObservationSource|Provider" seed_runtime tests -S
sed -n '300,370p' seed_runtime/runtime.py
sed -n '1,280p' seed_runtime/execution.py
sed -n '1,160p' seed_runtime/registry.py
sed -n '1,220p' seed_runtime/tool_execution_policy.py
sed -n '1,200p' seed_runtime/tool_validation.py
sed -n '1,170p' seed_runtime/policy.py
sed -n '2970,3035p' seed_runtime/observation_sources.py
sed -n '332,520p' seed_runtime/observation_sources.py
sed -n '2161,2295p' seed_runtime/observation_sources.py
sed -n '5200,5385p' scripts/seed_local.py
sed -n '640,710p' scripts/seed_local.py
```

## Files inspected

- `scripts/seed_local.py`
- `seed_runtime/runtime.py`
- `seed_runtime/execution.py`
- `seed_runtime/registry.py`
- `seed_runtime/tool_execution_policy.py`
- `seed_runtime/tool_validation.py`
- `seed_runtime/policy.py`
- `seed_runtime/observation_sources.py`
- Related tests located with ripgrep for execution status, observation sources, runtime loop, capability candidates, and diagnostics.

## Observed behavior before implementation inspection

### Local host observation path

`python scripts/seed_local.py --observe-local-host --quiet-output --observe-timings --record --db /tmp/seed_obs.db` exercised the current local observation path. The command printed a producer lifecycle:

```text
Collecting local-host observations...
Collected 2761 observations.
Normalizing local-host observations...: 0 / 2761
Normalized 2761 observations.
Ingesting local-host observations...: 0 / 2761
Generating events...: 0 / 2761
...
Writing events: 8283 / 8283
Generated events: 2761 / 2761
Completed local-host observation lifecycle.
Done.
```

The timing report separated `source collection`, `normalization`, and `event generation + ledger write`. That observable lifecycle already distinguishes execution of a source from ingestion and recording.

### Prometheus provider path

`python scripts/seed_local.py --observe-prometheus http://127.0.0.1:1 --observe-timeout 1 --quiet-output --observe-timings --record --db /tmp/seed_prom.db` exercised a provider-backed observation source against an unavailable endpoint. The command did not mutate cluster state or produce partial facts. It reported:

```text
Collecting prometheus:http://127.0.0.1:1 observations...
Collected 0 observations.
Normalized 0 observations.
Generated events: 0 / 0
Completed prometheus:http://127.0.0.1:1 observation lifecycle.
Done.
ingested 0 observation(s)
hosts/instances discovered: none
counts by predicate: none
```

This shows provider acquisition failure is currently expressed as an empty observation result on this source path, not as reasoning, scheduling, retry, or host mutation.

### JSON source failure path

`python scripts/seed_local.py --observe-json /tmp/nope.json --quiet-output --record --db /tmp/seed_bad.db` began the same source lifecycle and then failed during source collection with `FileNotFoundError`. The failure happened before event generation, consistent with the collection-service comment that collection and validation complete before appending events.

## 1. What bounded responsibility owns observation execution today?

Current implementation shows two bounded execution responsibilities, not one global execution engine.

1. **Observation execution for source-based observation commands is owned by `ObservationCollectionService.collect()` plus the concrete `ObservationSource.collect()` implementation selected by the CLI.** The service owns the lifecycle boundary: collect from a source, normalize collected observations, then ingest them. It explicitly calls `source.collect()` before normalization and before `ObservationIngestor.ingest_many()`.
2. **Registered operation execution for runtime `call_tool` decisions is owned by `ToolExecutor`.** Runtime routing sends only `decision.kind == "call_tool"` to `ToolExecutor.execute()`. `ToolExecutor` validates tool existence/status/input, checks policy, records tool call events, loads the registered implementation, runs it, validates output, and records completion or failure.

For the central question about additional observation required by a bounded inquiry, the implementation-backed answer is narrower: **the inquiry does not own execution. Existing CLI observation paths own source selection, and `ObservationCollectionService` owns the transition from selected source to source execution. Runtime `call_tool` has a separate registered-tool execution boundary.**

## 2. Where does reasoning terminate?

Reasoning terminates before either execution path is entered.

- In the CLI observation path, reasoning has already terminated when argparse arguments select an observation source such as `--observe-local-host`, `--observe-prometheus`, `--observe-json`, `--observe-ansible-inventory`, or `--observe-repository-source`. `ingest_observations_from_args()` turns those flags into concrete source instances and calls `ingest_observation_source()`.
- In `ObservationCollectionService.collect()`, execution begins at `observations = list(source.collect())`. That line is the clearest implementation point where selected work becomes observation execution.
- In runtime decision handling, reasoning terminates at a validated `Decision` with `kind == "call_tool"`. `Runtime.handle()` then calls `ToolExecutor.execute()`. The executor does not ask what should be observed; it evaluates whether the named registered operation may run.

## 3. Who decides that execution is required?

The decision is path-dependent:

- **CLI observation commands:** the command invocation decides execution is required by selecting a source flag. `ingest_observations_from_args()` is source-selection glue, not a reasoning subsystem.
- **Runtime registered tools:** the `DecisionProvider`/runtime decision path decides by producing `call_tool`; `Runtime` routes that decision to `ToolExecutor`.
- **Observation subsystem:** `ObservationCollectionService` does not decide that execution is required. It executes already-selected source work.
- **Execution path:** `ToolExecutor` does not decide that execution is required either. It validates, refuses, or executes an already-named tool call.

Therefore the current repository does **not** demonstrate an inquiry-owned automatic transition from reasoning to observation execution. It demonstrates bounded handoff points where already-determined work enters execution.

## 4. How are execution boundaries currently preserved?

Current implementation preserves several boundaries.

### Read-only diagnostics and local observation

`LocalHostObservationSource` declares itself as a read-only source using stdlib APIs and local files. Its metadata includes `read_only=True`, `local_only=True`, `shell_execution=False`, `subprocess_execution=False`, `privilege_escalation=False`, `network_probe=False`, and `network_connection=False`. The source collects identity, host files, platform, disk, network metadata, mounts, storage, listeners, local users, packages, and systemd observations without shelling out.

### Provider acquisition

`PrometheusObservationSource` is read-only and limited to HTTP GET requests for an allowlist of safe metric names. It rejects non-allowlisted queries in `_query()`. Connection, timeout, HTTP, OS, and value errors set `last_error` and return an empty list from `collect()`.

### Collection before mutation

`ObservationCollectionService.collect()` states that collection and validation complete before any events are appended, so a failing or malformed source cannot partially modify runtime state. The observed missing JSON file failed during collection before event generation.

### Registry and policy

`ToolExecutor` executes only after `ToolExecutionPolicyService.evaluate_with_state_factory()` resolves the tool, validates status and input schema, and evaluates policy. Unknown tools, unregistered tools, schema failures, non-allow policy outcomes, implementation failures, and output schema failures are all distinct refusal or failure surfaces.

### Recording

Observation recording is explicit through `--record` and ledger-backed ingestion. The source lifecycle separates collection from `event generation + ledger write`. Tool execution recording is explicit through `tool.call.started`, `tool.call.completed`, and `tool.call.failed` events.

## 5. Can execution currently be refused?

Yes. Refusal exists in multiple implementation forms.

- **Unknown registered tool:** `ToolRegistry.require()` raises `KeyError` for unknown tools, and `ToolValidationService.validate_tool_exists()` returns an invalid validation result for missing names.
- **Tool not registered:** `ToolValidationService.validate_tool_status()` refuses a tool whose status is not `registered`.
- **Bad input/output shape:** `ToolValidationService.validate_input_schema()` and `validate_output_schema()` refuse schema violations.
- **Policy refusal:** `PolicyGate.evaluate()` blocks unknown policy actions when an action-risk table is provided, allows L1 read-only actions, requires confirmation for L2, requires approval for L3, and blocks critical/default-denied risk classes.
- **Provider unavailable:** `PrometheusObservationSource.collect()` catches provider acquisition/query failures and returns no observations.
- **Unsupported provider query:** `PrometheusObservationSource._query()` raises `ValueError` for a query outside `SAFE_QUERIES`.
- **Malformed or unavailable source input:** `JsonObservationSource` can fail during file read/parsing before event append.

These are refusal/failure boundaries; none is expressed as a new planner or scheduler.

## 6. Does execution itself perform reasoning, or merely carry out already-determined work?

Execution mostly carries out already-determined work.

- `ObservationCollectionService.collect()` does not choose the source or decide the inquiry strategy. It invokes the selected source, normalizes its observations, and ingests them.
- `LocalHostObservationSource.collect()` and `PrometheusObservationSource.collect()` collect bounded observations. Their internal logic performs parsing, allowlist checks, and source-specific mapping, not inquiry reasoning.
- `ToolExecutor.execute()` validates and applies policy before loading a registered implementation. It performs execution governance, not strategic reasoning.

The strongest caveat is that source implementations contain local deterministic interpretation. For example, a Prometheus sample is mapped into Seed observations, and local host collection chooses which read-only files/APIs to inspect. That is adapter logic and deterministic source interpretation, not bounded inquiry reasoning.

## 7. Would removing the execution responsibility produce implementation loss, observable capability loss, or both?

Both.

- Removing `ObservationCollectionService`/source `collect()` execution would remove implementation that turns selected observation sources into observations, normalization, ingestion, events, facts, and timing/status lifecycle output.
- Removing `ToolExecutor` would remove implementation that routes validated registered operation calls through registry, policy, event recording, implementation loading, output validation, and fact extraction.
- Observable capability loss would include loss of `--observe-local-host`, `--observe-prometheus`, `--observe-json`, `--observe-ansible-inventory`, and `--observe-repository-source` ingestion behavior, as well as runtime `call_tool` execution behavior.

## 8. Does the execution responsibility strengthen recent inquiry discipline, or represent a distinct architectural shape?

It strengthens the recent inquiry discipline by keeping execution outside inquiry reasoning, while also representing a distinct architectural shape.

- It strengthens the discipline because reasoning can terminate in a bounded, inspectable decision or source selection, after which execution has its own validation, collection, policy, and recording boundaries.
- It is distinct because execution is not another reasoning view. It has lifecycle, source acquisition, provider interaction, event writes, policy outcomes, implementation loading, and failure/refusal semantics.

The strongest supporting evidence is the clean implementation split: runtime routes only `call_tool` decisions to `ToolExecutor`; the observation ingestion path calls `source.collect()` first, then normalizes and ingests; concrete sources declare read-only/provider boundaries.

The strongest contradictory evidence is that the repository architecture documents repeatedly say Seed does not own actual host/provider execution, and legacy handoff paths are non-executable. That contradicts any broad claim that Seed owns execution generally. The reconciliation is that Seed owns **bounded internal execution responsibilities** for registered low-risk tool calls and observation-source collection, while not owning host automation, shell execution, arbitrary provider-output execution, scheduling, retries, credentials, or external workflow lifecycle.

## Reconciliation

| Requested item | Current implementation-backed answer |
| --- | --- |
| Bounded execution responsibility | Observation-source execution is bounded by `ObservationCollectionService.collect()` plus concrete `ObservationSource.collect()` adapters. Runtime registered-operation execution is bounded by `ToolExecutor`. |
| Reasoning boundary | CLI source flags or runtime `Decision(kind="call_tool")` are already-determined work; execution begins when `source.collect()` or `ToolExecutor.execute()` is called. |
| Execution boundary | Source collection precedes normalization/ingestion/event append. Tool execution follows registry validation, schema validation, and policy allow. |
| Authority boundary | Observation sources encode read-only/provider constraints; `ToolExecutor` uses registry, validation, and `PolicyGate`; external host automation remains outside Seed. |
| Execution refusal | Unknown/unregistered tools, schema violations, policy outcomes, provider unavailability, unsupported Prometheus queries, and source file failures refuse or fail execution before durable success. |
| Observable capability | Existing CLI observation commands collect and ingest observations; runtime registered tools can execute only registered operations. |
| Strongest supporting evidence | Lifecycle output from observation commands; `ObservationCollectionService.collect()` source/normalize/ingest sequencing; `ToolExecutor` validation-policy-execute-record sequencing. |
| Strongest contradictory evidence | Architecture documentation says Seed does not own actual execution broadly and retained handoff plans remain non-executable; therefore the owned responsibility is bounded source/registered-tool execution, not general orchestration. |

## Acceptance answers

### Who currently owns the transition from reasoning to observation execution?

For observation-source commands, **CLI source selection plus `ObservationCollectionService` own the transition**: the command selects a concrete source, and `ObservationCollectionService.collect()` begins execution at `source.collect()`. For runtime registered operations, **`Runtime` routes `call_tool` and `ToolExecutor` owns the registered execution boundary**. No current implementation shows a bounded inquiry directly executing observations.

### Does execution reason, or execute?

Execution executes. It validates, enforces policy, collects source data, normalizes, ingests, records, and reports status. It may perform deterministic adapter interpretation, but it does not choose inquiry strategy or decide that additional observation is required.

### What responsibility would disappear if the execution layer were removed?

The bounded responsibility that would disappear is: **carrying already-determined source/tool work across the execution boundary safely, with source/provider constraints, validation, policy, refusal, lifecycle status, event recording, and fact ingestion/extraction.**

## Files changed

- `docs/observation_execution_transition_investigation.md`

## LOC changed

- Added one documentation report. `git diff --stat` reported the exact changed line count during finalization.

## Tests run

No product code was changed. The investigation exercised the required execution-oriented commands above. A documentation-only sanity check was run with `python -m py_compile scripts/seed_local.py seed_runtime/runtime.py seed_runtime/execution.py seed_runtime/observation_sources.py seed_runtime/registry.py seed_runtime/tool_execution_policy.py seed_runtime/tool_validation.py seed_runtime/policy.py`.

## Recommended bounded implementation slice

No implementation is recommended by this report. If future work is explicitly requested, the smallest bounded slice should start by preserving the current evidence-backed boundary: source selection and `ObservationCollectionService.collect()` execute already-determined observation work; `ToolExecutor` executes only registered, validated, policy-allowed operations; inquiries should not silently become schedulers or orchestrators.
