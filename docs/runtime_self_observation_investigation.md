# Runtime Self-Observation Investigation

## Scope

This is an observational investigation of whether Seed already has implementation-backed foundations for observing itself as a continuously running process. It does not design scheduling, background workers, resource governors, or resource policy. Repository implementation is treated as authority.

## Reconciliation

### 1. Seed versus host observational boundary

Seed currently distinguishes host observation from Seed runtime ownership, but it does not yet model the Seed process as a first-class observed subject.

Supporting evidence:

- `LocalHostObservationSource` is explicitly a read-only local host observation source. Its metadata says collection is local-only, read-only, has no shell execution, no subprocess execution, no privilege escalation, and no network probe or connection.
- Local host observations are attached to the host name from platform/local identity evidence, not to a Seed process subject.
- `Runtime` owns routing of validated decisions to owner services. It is not itself an observation source and does not collect process measurements.
- `EventLedger` owns append-only runtime event history; `StateProjector` rebuilds inspectable state from ledger events. That establishes an internal Seed responsibility distinct from local host collection.

Contradictory evidence:

- The local host source docstring says it reads "process-local platform, disk, local network, and mount metadata", so some observations are collected from the process vantage point. That is not the same as observing the Seed process itself.
- Listener observation can attribute listening sockets to process IDs/names, but that is socket/process attribution for local listeners, not a self-observation model for Seed.

Conclusion: Seed/host separation exists as an implementation boundary: host substrate observation is one observation source, while Runtime/EventLedger/StateProjector are Seed-owned services. The missing piece is a subject boundary for `seed_runtime` or the current Seed process.

### 2. Current ability to observe Seed runtime characteristics

| Observation | Exists today? | Evidence-backed conclusion |
| --- | --- | --- |
| process memory | No | No current observation predicate or source emits process RSS/VMS/heap memory for Seed. Existing memory support is host `memory_total_bytes` only. |
| resident memory | No | No implementation reads `/proc/self/status`, `/proc/<pid>/statm`, `resource`, or equivalent for Seed RSS. |
| CPU usage | No | Existing `cpu_count` and `cpu_model` describe host CPU, not Seed CPU consumption. |
| thread count | No | No current observation reads thread count for the Seed process. |
| database size | No direct observation | SQLite ledgers expose a database path and tables, but no observation source measures the DB file size. |
| ledger size | Partial internal access, no observation | Ledgers can list events and SQLite persists event rows, but no observation source emits event count/bytes as an observation. |
| disk free | Yes, host-level | `LocalHostObservationSource` emits `disk_total_bytes` and `disk_free_bytes` for `/`. |
| projection cache size | No direct observation | Projection stores persist cache snapshots and derived indexes, but no source emits cache size/count as an observation. |
| runtime duration | No | Runtime handles one user message at a time and records events, but no uptime/start-time/runtime-duration observation exists. |
| queue depth | No | There is no canonical queue-depth observation; current runtime routes synchronous decisions and retained action/handoff artifacts are explicitly non-executable historical side paths. |

Contradictory evidence:

- Observation ingestion diagnostics measure source collection time, normalization time, ledger write time, total observations, total events, and throughput. These are runtime-adjacent timing counters, but they are diagnostics returned by the collection service, not durable observations of the Seed process.
- Projection cache loading emits progress/status phases such as cache load, incremental replay, full rebuild, and cache save. These are operational statuses rather than persistent observation predicates.

### 3. Existing observations and natural observation families

Existing relevant observations:

- Host substrate: `cpu_model`, `cpu_count`, `memory_total_bytes`, `kernel_release`, `kernel_version`.
- Host storage: `disk_total_bytes`, `disk_free_bytes`, block-device predicates, mount predicates, and Prometheus filesystem measurements.
- Host network/process-adjacent visibility: listener predicates including `listening_process_id` and `listening_process_name` when listener socket inode attribution is available.
- Measurement semantics: `disk_free_bytes`, `disk_total_bytes`, `filesystem_avail_bytes`, and `filesystem_size_bytes` are treated as measurement predicates.

Natural fit for missing Seed self-observations:

- Process memory, RSS, CPU usage, thread count, and runtime duration naturally fit the existing observation source + observation/fact/evidence pipeline. They would be volatile measurements, not durable identity facts.
- Database size, ledger event count/bytes, and projection cache size naturally fit storage/projection measurement families, with subjects scoped to the Seed runtime artifact or diagnostic run rather than the host.
- Disk free already belongs to host/storage measurement observation; Seed could consume it without creating a new subsystem.

Contradictory evidence:

- The predicate catalog/measurement set currently names only a small storage/availability subset as measurements; process metrics are not currently declared.
- Diagnostic inventory is for diagnostic surfaces, not necessarily for ordinary observation sources, so adding a self-observation source would not automatically create a diagnostic surface unless exposed through a diagnostic CLI.

### 4. Observation source or new responsibility?

Runtime self-observation would be another observation source if it only emits read-only observations about the running Seed process and its local storage artifacts.

Supporting evidence:

- Observation sources expose a stable identity, source type, and `collect()` method and remain unaware of the event ledger, state projector, and ingestion internals.
- `ObservationIngestor` already converts observations into observation, evidence, and fact events, preserving provenance.
- `StateProjector` already retains measurements differently from durable facts, keeping only recent measurement samples in projection while leaving the append-only ledger untouched.

Contradictory evidence:

- If self-observation were used to defer work, regulate throughput, or choose scheduling, that would be a new decision responsibility. This investigation does not recommend that. The existing implementation only supports observing and reasoning over evidence, not autonomously scheduling work.

Conclusion: collecting runtime self-observations is an extension of the observation model. Acting on them autonomously would be a separate responsibility not currently implemented.

### 5. Inquiry compatibility

Existing inquiry composition could consume runtime observations as ordinary projected facts if they were ingested.

Supporting evidence:

- Runtime projects current state before composing decision input.
- Observations become evidence-backed facts through the ingestor and then become projected state.
- Current state and support views already expose facts, measurements, confidence, contradictions, and stale-fact refresh recommendations.
- Capability recommendation paths already consume projected state and capability catalogs when handling `request_tool` decisions.

This means available memory, disk pressure, CPU pressure, database growth, and event-ledger growth could become evidence available to inquiry without architectural changes, provided they are emitted as observations/facts with appropriate measurement predicates and subject boundaries.

Contradictory evidence:

- The current runtime decision schema has no explicit resource-regulation action. It can answer, ask, request tools, call tools, propose plans/handoffs/state patches, or refuse. That supports reasoning and explanation, not a built-in self-regulation mechanism.
- Stale fact refresh capabilities currently map `runtime` to `service_inspection`, not to a self-process observation capability.

### 6. Event-ledger compatibility with transitions

The append-only event ledger can preserve transitions as events or as changing observations over time, but specific transition vocabularies are not currently implemented.

Supporting evidence:

- `EventLedger` and `SQLiteEventLedger` preserve append order and event payloads.
- Observation ingestion appends `observation.observed`, `evidence.observed`, and optional `fact.observed`/`fact.inferred` events for every observation.
- State projection keeps recent measurement samples in projection while preserving the full ledger.
- Runtime already records operator input, model decision proposals, invalid/rejected decision events, answers, questions, refusals, tool-need creation, tool execution results, and state patch events.

Evaluation of example transitions:

- `resource pressure increased` / `resource pressure reduced`: compatible as derived observations or facts over repeated measurements, but not currently implemented as a specific transition detector.
- `background inquiry deferred`: not currently implementation-backed because background inquiry/scheduling is not canonical runtime behavior.
- `operator-requested work executed`: partially supported through user input, `call_tool`, ToolExecutor events, and execution status; exact wording is not a current event kind.

Contradictory evidence:

- The ledger is generic and append-only; it does not by itself infer transitions. Transition recognition would require an observation, inference, diagnostic, or runtime event producer.

### 7. Existing classes of runtime work

Implementation-backed distinctions already exist:

- Operator-requested work: `input.user_message` events and Runtime handling of a session message.
- Diagnostic work: diagnostic inventory entries classify surfaces by state use, repo-file use, JSON support, record support, event-ledger writes, emitted facts, and cluster mutation.
- Observation work: observation sources collect observations; `ObservationIngestor` records observation/evidence/fact events.
- Projection work: `StateProjector` rebuilds inspectable state; projection stores cache snapshots and derived indexes.
- Execution work: `ToolExecutor` is reached only through `call_tool`; Runtime does not own tool behavior.
- Maintenance/cache work: projection cache clear/rebuild/load/save paths exist, but they are explicit cache operations rather than autonomous maintenance loops.

Not implementation-backed as current work classes:

- Background work as a scheduler-owned class.
- Autonomous maintenance as a daemon responsibility.
- Resource governance or adaptive control.

Contradictory evidence:

- Some CLI status phases and diagnostic surfaces look like operational work classes, but diagnostic inventory marks most as read-only/non-recording/non-mutating. That supports visibility, not autonomous work management.

### 8. Continuous execution boundary

Continuous execution would not require a new architecture merely to observe Seed. It would extend existing observation, inquiry, and event-ledger responsibilities. Continuous autonomous regulation would be a new responsibility and is outside the current implementation.

Supporting evidence:

- The implemented architecture is already: observations -> evidence/facts -> projection -> inquiry/decision context -> events.
- Runtime is a router, not a scheduler or workflow engine.
- Event ledger preserves durable transitions over time; projection cache is explicitly derived and rebuildable.
- Diagnostic inventory already distinguishes read-only visibility from event-ledger writes and cluster mutation.

Contradictory evidence:

- Continuous execution would create lifecycle concerns that are absent today: process uptime, repeated collection cadence, queue depth, and deferral semantics. Those are not solved by the observation model alone. The current architecture can observe evidence, but it does not define continuous process ownership.

### 9. Strongest contradictory evidence summary

- Seed does not currently emit self-process observations, so "Seed can observe itself" is not true for process memory, CPU usage, RSS, thread count, uptime, queue depth, ledger size, DB size, or projection cache size today.
- Current host observations can be collected from process-local APIs, but their subject is the host, not Seed.
- Event ledger can preserve changes, but does not infer resource-pressure transitions by itself.
- Inquiry can consume projected facts, but no current decision kind or runtime path implements autonomous self-regulation.
- Diagnostic and projection status counters prove operational visibility patterns, not durable self-observation facts.

## Acceptance answers

### Can Seed observe itself using the same observation model it uses to observe the host?

Not fully today. Seed already has the model needed: read-only observation sources, observation/evidence/fact ingestion, measurement semantics, append-only event history, and state projection. But the implementation currently observes the host, repository, Prometheus, Ansible inventory, systemd, and diagnostics; it does not yet observe the Seed process as a first-class subject.

### Would continuous execution require a new architecture, or an extension of existing observation?

For observation only, continuous execution would be an extension of existing observation. For autonomous scheduling, priority, or resource governance, it would require new responsibilities not present in the current canonical runtime. This report does not recommend those responsibilities.

### Smallest implementation-backed slice for evidence-based self-regulation without policy

The smallest bounded slice would be a read-only `SeedRuntimeObservationSource` that emits volatile measurements about the current Seed process and its local persistence artifacts into the existing observation pipeline, with no scheduler, no governor, no autonomous deferral, and no cluster mutation.

Minimal observations naturally supported by current architecture:

1. `seed_runtime_duration_seconds` for the current process or diagnostic run.
2. `seed_process_resident_memory_bytes` from `/proc/self/status` or `/proc/self/statm` when available.
3. `seed_process_thread_count` from `/proc/self/status` when available.
4. `seed_ledger_event_count` from `ledger.list_events(workspace_id)`.
5. `seed_sqlite_database_size_bytes` when a SQLite ledger path exists.
6. `seed_projection_cache_snapshot_count` or cache DB file size when a projection store path exists.
7. Reuse existing `disk_free_bytes` host measurement rather than duplicating disk observation.

This slice would provide evidence that inquiry could inspect. It would not make policy decisions.

## Commands executed

- `pwd && rg --files -g 'AGENTS.md' -g '!*venv*' | xargs -r -I{} sh -c 'echo --- {}; cat {}' && git status --short`
- `rg -n "runtime|event ledger|ledger|continuous|observation|measurement|resource|state build|diagnostic inventory|diagnostic-inventory|diagnostic_shape|queue|projection cache|database size|disk free|memory|CPU|thread|process" . --glob '!*.pyc' --glob '!__pycache__/*'`
- `rg --files seed_runtime tests docs | rg '(runtime|events|local_host|observation|measurement|resource|state|projection|diagnostic_inventory|diagnostic_shape|inquiry|execution|pressure|repository_observation)'`
- `sed -n '1,240p' seed_runtime/observation_sources.py; sed -n '1,220p' seed_runtime/events.py; sed -n '1,260p' seed_runtime/models.py; sed -n '1,220p' seed_runtime/facts.py`
- `sed -n '240,520p' seed_runtime/observation_sources.py; sed -n '700,820p' seed_runtime/observation_sources.py; sed -n '1,140p' seed_runtime/runtime.py; sed -n '1240,1275p' seed_runtime/state.py; sed -n '1,120p' seed_runtime/observations.py`
- `sed -n '120,260p' seed_runtime/observations.py; sed -n '260,360p' seed_runtime/observations.py; sed -n '220,420p' seed_runtime/events.py; sed -n '140,260p' seed_runtime/runtime.py; sed -n '260,410p' seed_runtime/runtime.py`
- `python scripts/seed_local.py --diagnostic-inventory | head -60 && python scripts/seed_local.py --observation-inventory | head -80 && python scripts/seed_local.py --knowledge-reachability-audit --candidate runtime --candidate "projection cache" --candidate "state build" | head -80`
- `python scripts/seed_local.py --observe-local-host --quiet-output --db /tmp/seed-self-observation.sqlite && python scripts/seed_local.py --db /tmp/seed-self-observation.sqlite --current-facts | rg 'disk_free_bytes|disk_total_bytes|cpu_count|memory_total_bytes|kernel_release|listening_process|filesystem' | head -40`

## Files inspected

- `AGENTS.md`
- `seed_runtime/observation_sources.py`
- `seed_runtime/observations.py`
- `seed_runtime/events.py`
- `seed_runtime/models.py`
- `seed_runtime/facts.py`
- `seed_runtime/runtime.py`
- `seed_runtime/state.py`
- `seed_runtime/projection_store.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/pressure_audit.py`
- `seed_runtime/inquiry_orientation.py`
- Selected test and documentation paths discovered by ripgrep as supporting surface inventory.

## Files changed

- `docs/runtime_self_observation_investigation.md`

## LOC changed

- Added 232 lines.
- Removed 0 lines.

## Tests run

No production code was changed. The report was validated through read-only repository inspection and Seed CLI diagnostic/observation commands listed above. One attempted CLI invocation intentionally failed because `--candidate` is ambiguous; that failure is recorded in commands executed and was not used as evidence.
