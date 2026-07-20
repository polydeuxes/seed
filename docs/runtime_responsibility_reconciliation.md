# Runtime Responsibility Reconciliation

## Scope

This reconciliation answers whether the current repository already distinguishes absence of work from absence of operator work. It is observational only. It does not propose or implement scheduling, autonomy, a planner, background intelligence, continuous execution, or an agent loop.

Repository authority wins. The strongest implementation-backed flow remains a bounded request/response runtime path: user input is recorded, state is projected, decision input is composed, a decision is produced and validated, and the runtime routes the decision to the appropriate owner service.

## Commands Executed

```text
pwd && rg --files -g 'AGENTS.md' -g '!node_modules' -g '!venv' && git status --short
cat AGENTS.md && rg -n "runtime|decision|execution|observation|background|operator|idle|busy|blocked|waiting|unavailable|diagnostic" -S . --glob '!*.pyc' --glob '!/.git/**'
rg --files seed_runtime scripts tests docs | sed -n '1,200p'
sed -n '1,260p' seed_runtime/runtime.py; sed -n '1,240p' seed_runtime/runtime_loop.py; sed -n '1,240p' seed_runtime/runtime_self_observation.py; sed -n '1,220p' seed_runtime/execution.py; sed -n '1,220p' seed_runtime/models.py
sed -n '260,560p' seed_runtime/runtime.py; sed -n '220,520p' seed_runtime/execution.py; rg -n "self|runtime|busy|idle|executing|waiting|blocked|unavailable|background|operator|request/response|one-shot|loop" seed_runtime tests docs scripts/seed_local.py -S --glob '!*.pyc'
sed -n '1,260p' tests/test_runtime_self_observation.py; sed -n '1,260p' seed_runtime/runtime_trace.py; sed -n '430,470p' scripts/seed_local.py; sed -n '1,220p' tests/test_runtime_loop.py; sed -n '1,200p' tests/test_execution_status.py
sed -n '1,220p' seed_runtime/execution_status.py; sed -n '1,220p' seed_runtime/observation_sources.py; sed -n '1,220p' seed_runtime/decision_journal.py; sed -n '1,200p' seed_runtime/diagnostic_inventory.py
python scripts/seed_local.py --help | sed -n '1,180p'
python scripts/seed_local.py --diagnostic-inventory | sed -n '1,80p'
python scripts/seed_local.py --observation-inventory | sed -n '1,80p'
python scripts/seed_local.py --observe-local-host --current-observations --quiet-output | sed -n '1,120p'
```

## Files Inspected

- `AGENTS.md`
- `seed_runtime/runtime.py`
- `seed_runtime/execution.py`
- `seed_runtime/models.py`
- `seed_runtime/runtime_trace.py`
- `seed_runtime/execution_status.py`
- `seed_runtime/observation_sources.py`
- `seed_runtime/decision_journal.py`
- `seed_runtime/diagnostic_inventory.py`
- `scripts/seed_local.py`
- `tests/test_runtime_loop.py`
- `tests/test_runtime_self_observation.py`
- `tests/test_execution_status.py`
- Supporting docs surfaced by search, especially `docs/input_inspection_reconciliation.md`, `docs/response_reconciliation.md`, and `docs/temporal_reasoning_audit.md`.

## Files Changed

- `docs/runtime_responsibility_reconciliation.md`

## LOC Changed

- Added 204 lines.

## 1. Does current implementation distinguish responsibility owner?

Yes, but it distinguishes responsibility owners for production, routing, execution, observation, projection, and presentation paths rather than for a single continuous runtime activity state.

| Owner | Implementation-backed evidence | Conclusion |
| --- | --- | --- |
| Operator / user | `Runtime.handle_user_message` appends `input.user_message` with `actor="user"`, preserving operator-originated input as the causation root for the request/response path. | Operator responsibility exists as current input ownership and interaction initiation, not as a durable `operator-active` runtime state. |
| Model / decision producer | Runtime calls `decision_producer.decide(...)` and records `model.decision.proposed` with `actor="model"`. | Decision production is model-owned or producer-owned, separate from runtime routing. |
| Runtime orchestration | `Runtime.__seed_arch__` declares owner `runtime_orchestration` and describes routing validated decisions to owner services without owning their behavior. | Runtime owns orchestration and response envelopes, not all work semantics. |
| Tool execution | `ToolExecutor.__seed_arch__` declares owner `registered_tool_execution` and executes only registered operations after validation and policy checks. | Registered tool execution is a distinct owner from runtime routing and decision production. |
| System / policy / validation | Runtime records invalid decisions and intent rejections with `actor="system"`; `ToolExecutor` records policy-denied results through system events and pending actions where required. | System-owned validation and policy boundaries exist. |
| Tool | `ToolExecutor` appends `tool.call.started`, `tool.call.completed`, and `tool.call.failed` with `actor="tool"`. | Tool work is visible as tool-owned event activity once routed. |
| Repository / diagnostic surfaces | `RepositorySourceObservationSource` reads repository files and emits read-only repository observations; diagnostic inventory distinguishes repo-file use from projected-state use and event-ledger writes. | Repository-backed observation and diagnostic responsibility exists, but not as an autonomous runtime owner. |
| Observation source / collection service | `ObservationSource` adapters own collection; `ObservationCollectionService` and `ObservationIngestor` convert collected observations into observation/evidence/fact events. | Observation production is separately owned from runtime message routing. |
| Background process | No reviewed implementation exposes a generic background-process owner. Transient lifecycle/progress surfaces can describe long-running observation collection, and pending actions can represent deferred execution authorization, but neither is a scheduler or continuous background worker. | Background ownership is not first-class as runtime responsibility. |

Answer: the repository already distinguishes multiple classes of responsibility ownership, but not as a complete runtime-activity taxonomy.

## 2. Can the repository already distinguish operator-active, background-active, and no-current-work?

Partially, with important limits.

- `operator-active` can be reconstructed during a specific request/response run because the runtime records `input.user_message`, `model.decision.proposed`, response events, and tool events causally tied to the user input. This supports "operator-triggered run happened" rather than a live durable `operator-active` state.
- `background-active` is not directly represented as a generic runtime category. Observation collection can emit transient `ExecutionStatus` phases such as `observation_collection`, `observation_ingestion`, and `event_persistence`, but those statuses are renderer-independent and explicitly non-authoritative. They are also not persisted into the ledger, observations, facts, or projection cache.
- `no-current-work` is not implementation-backed. Absence of matching in-flight events, absence of pending actions, or lack of transient status messages is not itself a recorded state.

Smallest missing implementation, identified observationally: a durable or queryable runtime-activity observation/artifact that records current activity owner and lifecycle boundary. This is a missing artifact, not a missing scheduler.

## 3. What runtime observations already exist describing Seed itself?

`SeedRuntimeObservationSource` provides read-only process observations about Seed itself. Tests prove it can emit observations with subject `Seed` and predicates:

- `seed_process_resident_memory_bytes`
- `seed_process_thread_count`
- `seed_runtime_duration_seconds`
- `seed_sqlite_database_size_bytes`
- `seed_event_ledger_size_bytes`

The same tests prove those observations are read-only, non-cluster-mutating, non-scheduler, and not runtime-governance signals. They flow through the normal observation ingestion path into projected observations, evidence, and facts.

These observations describe resource/process facts about Seed. They do not currently indicate `busy`, `idle`, `executing`, `waiting`, `blocked`, or `unavailable`.

Separate from observations, `ExecutionStatus` can describe transient activity phases such as collection, normalization, ingestion, event persistence, and projection-cache save. Tests prove this status is not written into the ledger, observations, facts, or projection cache. It is operator feedback, not cluster truth and not a runtime state.

## 4. Does runtime currently expose enough information to reconstruct what Seed is doing without introducing scheduling?

For completed or currently emitted bounded operations, yes in fragments:

- Runtime events reconstruct a user-triggered run: input, decision proposal, validation failures, response events, tool starts/completions/failures, policy blocks, and pending-action creation.
- `RuntimeTraceReader` reconstructs a single recorded runtime run from append-only events without replaying or mutating execution.
- `DecisionJournal` can append decision audit records with `run_id`, decision kind, reason, selected tool, policy result, outcome, and error.
- `ExecutionStatus` exposes transient progress for observation collection and ingestion without becoming persisted state.
- `SeedRuntimeObservationSource` exposes read-only process/resource observations about the Seed process.

For an arbitrary live question, "what is Seed doing right now?", no. The repository lacks one coherent current runtime-activity artifact joining activity owner, phase, run id, causation, and lifecycle completion. Existing pieces can reconstruct bounded runs and transient collection progress, but they do not define a current-work ledger or live activity projection.

## 5. Would "idle" currently be an observation, runtime state, presentation label, or absence of implementation?

Current evidence supports the following classification:

| Interpretation | Supported today? | Rationale |
| --- | --- | --- |
| Observation | No. No reviewed observation source emits `idle` or an equivalent activity predicate for Seed. Existing self-observations are resource/process metrics. |
| Runtime state | No. Runtime has no state enum or lifecycle artifact for `idle`; domain statuses cover goals, tool needs, pending actions, action plans, and tool calls, not global runtime idleness. |
| Presentation label | Possible only as external wording. CLI and docs may use human language, but no implementation-backed `idle` label was found as a normalized runtime concept. |
| Absence of implementation | Strongest current classification. "Idle" is currently language one might infer from absence of observed work, but the repository does not preserve that inference as a fact, event, status, or state. |

Therefore, `idle` is not currently implementation-backed. It is language unless a caller explicitly defines it outside the current repository model.

## 6. Would distinguishing operator-active, background-active, and unscheduled require a new runtime artifact, or could it emerge as a projection of existing runtime observations?

Current implementation does not support the full distinction as a projection of existing runtime observations alone.

What could eventually support richer runtime orientation without scheduling:

- Event causation and actor fields already distinguish user/model/system/tool origins.
- Runtime run traces already reconstruct bounded request/response runs.
- Decision journal records can preserve decision/outcome metadata by run id.
- Tool execution events already expose execution boundaries and policy blockers.
- Observation collection statuses already expose phases and progress transiently.
- Seed self-observations already expose process/resource facts as normal observations.

What is missing:

- A common runtime-activity artifact or persisted observation that states owner/phase/lifecycle for current work.
- A durable distinction between transient operator feedback and current runtime activity.
- A representation of `unscheduled` or `no-current-work` that is not merely absence of events.

Conclusion: a richer orientation could reuse existing events, actors, traces, statuses, and self-observations as inputs, but the specific distinction would require at least one new runtime-activity artifact or observation boundary. It does not require scheduling to investigate or expose that boundary.

## 7. Strongest contradictory evidence

The strongest contradictory evidence is that the canonical runtime is intentionally request/response and owner-routing oriented:

1. `Runtime.handle_user_message` only runs when called with a user message. It records input, composes context, obtains one decision, validates/retries it, and routes it to a response, tool need, tool executor, state patch, or refusal.
2. `LocalSeedApp.run` is a one-shot wrapper around `Runtime.handle_user_message` and returns a response plus the current event list.
3. The CLI help describes one-shot message mode and separately labels plan/proposal/handoff paths as experimental or legacy side paths that never execute or approve tools.
4. `ActionPlan` and `HandoffPlan` models explicitly describe legacy/experimental, non-executable side paths and state that Seed does not manage retries, schedules, long-running provider jobs, or execution lifecycle for handoffs.
5. `ExecutionStatus` is explicitly transient and non-authoritative; tests ensure it is not written into the ledger, facts, observations, or projection cache.
6. `SeedRuntimeObservationSource` self-observations explicitly carry metadata `scheduler=false` and `runtime_governance=false`, confirming that process observation is not runtime control.

This contradictory evidence prevents treating existing runtime responsibility distinctions as an autonomous or continuously scheduled runtime model.

## Reconciliation

### Runtime responsibility owners

Seed already distinguishes responsibility owners across operator input, model decision production, runtime routing, system validation/policy, registered tool execution, observation collection, repository observation, projection, diagnostic surfaces, and CLI presentation. These owners are implementation-backed by actors, `__seed_arch__` owner metadata, service classes, event kinds, and tests.

### Runtime activity visibility

Seed exposes bounded activity visibility:

- request/response activity through runtime events;
- registered tool activity through tool-call events;
- policy/approval blocking through policy and pending-action outputs;
- observation-collection progress through transient execution status;
- completed run reconstruction through runtime trace;
- process/resource facts through Seed self-observations.

It does not expose a global current-runtime-work state.

### Existing runtime observations

Existing runtime observations about Seed are resource/process facts: memory, threads, runtime duration, SQLite database size, and event-ledger size. They are read-only observations, not governance or scheduler signals.

### Missing runtime observations

Missing implementation-backed observations include current activity owner, activity phase as a durable/current fact, active run id, lifecycle start/finish boundary for non-message activity, `operator-active`, `background-active`, `unscheduled`, and `idle`.

### Strongest supporting evidence

The strongest supporting evidence for multiple runtime responsibility classes is the separation between runtime orchestration, decision production, tool execution, observation collection, self-observation, execution-status feedback, decision journal, runtime trace, and diagnostic inventory. These are distinct implementation owners, not just prose labels.

### Strongest contradictory evidence

The strongest contradictory evidence is the request/response-only canonical runtime path and the explicit non-executable / non-scheduler boundaries around legacy plans, handoffs, execution status, and self-observation.

## Acceptance Criteria Answers

### Does the repository already distinguish different kinds of runtime responsibility?

Yes. It distinguishes responsibility owners for input, decisions, routing, validation/policy, tool execution, observation collection, repository observation, projection, diagnostics, and presentation. It does not yet distinguish those owners as a complete current runtime-activity state model.

### Is "idle" currently an implementation-backed concept, or merely language?

`idle` is currently merely language. It is not a Seed observation, runtime state, event kind, diagnostic shape, projected fact, or tested presentation label.

### What existing runtime observations would eventually support a richer runtime orientation without introducing scheduling?

Existing ingredients are actor-tagged events, causation/correlation ids, runtime trace reconstruction, decision journal records, tool execution events, policy/pending-action events, transient execution-status phases, and Seed self-observations. These can support richer orientation evidence, but the specific `operator-active` / `background-active` / `unscheduled` distinction is not already present.

## Recommended bounded implementation slice

If implementation is later requested, the bounded slice should be limited to a read-only runtime activity visibility artifact or observation that records owner, phase, causation/run id, and lifecycle boundary for already-existing operations. It should not schedule work, plan work, run autonomously, or change execution authority.
