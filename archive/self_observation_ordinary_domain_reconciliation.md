# Self-observation as an ordinary observation domain

## Scope and method

This reconciliation answers whether the current implementation establishes Seed itself as an ordinary observation subject. The review is limited to `SeedRuntimeObservationSource`, `Observation`, `ObservationCollectionService`, `ObservationIngestor`, observation inventory, event ledger, and projection behavior needed to answer that question.

No runtime dashboard, health engine, telemetry framework, scheduler, background monitor, runtime governance, or self-awareness framework is recommended here.

## Conclusion

Yes: the repository has established self-observation as an ordinary observation domain, but narrowly. The observed subject is the running Seed process and its configured local persistence artifacts, represented under the default subject string `Seed`. It is not the repository, operator, whole machine, or a privileged runtime authority.

Self-observation follows the same implementation path as other observations:

```text
SeedRuntimeObservationSource
-> Observation
-> ObservationCollectionService
-> ObservationIngestor
-> EventLedger
-> StateProjector projection
```

The implementation demonstrates ordinary observation participation, not a special telemetry subsystem.

## 1. What subject is actually being observed?

`SeedRuntimeObservationSource` defaults `subject` to `Seed`, stores the current process ID unless one is injected, and reads local process status from `proc_root / process_id / status`. The emitted observations all use `subject=self.subject` and predicate-specific values. Therefore, the implementation-backed subject is the current Seed runtime process as represented by the `Seed` subject label.

The source also observes configured local persistence artifact sizes when paths are supplied: `sqlite_database_path` and `event_ledger_path` are measured with filesystem stat and emitted as `seed_sqlite_database_size_bytes` and `seed_event_ledger_size_bytes`. Those are attributes of the configured Seed runtime storage artifacts, still attached to the `Seed` subject.

Careful distinctions:

| Candidate subject | Supported? | Implementation-backed interpretation |
| --- | --- | --- |
| Seed process | Yes | Process ID defaults to `os.getpid()`, `/proc/<pid>/status` supplies memory and thread values, and monotonic runtime duration may be emitted. |
| Runtime | Partly | Runtime duration and configured persistence artifact sizes are observed, but only as local process/run measurements. |
| Repository | No | Repository source observation is a separate provider; `SeedRuntimeObservationSource` does not scan repository files or observe source code. |
| Operator | No | No operator identity, activity, intent, or session behavior is collected. |
| Machine | No, except local files/proc backing measurements | The source reads only the current process status and supplied artifact paths; it does not claim host inventory or machine ownership. |

## 2. Does the source participate in the normal observation pipeline?

### Collection

The source implements `collect()` and returns a list of `Observation` instances. `ObservationCollectionService.collect()` accepts any `ObservationSource`, calls `source.collect()`, validates that collected items are `Observation` instances, optionally normalizes them, and ingests them through the configured ingestor.

### Observation object

Each emitted runtime measurement is constructed with `Observation(id=..., source_type="discovery", observed_at=..., subject=self.subject, predicate=..., value=..., confidence=1.0, metadata=...)`. The canonical `Observation` model validates confidence and carries source type, observed time, subject, predicate, value, metadata, dimensions, and optional expiration.

### Ingestion

`ObservationIngestor.ingest_many()` converts every observation into evidence and, unless fact promotion is explicitly suppressed for a narrow Prometheus case, into a fact. Runtime observations do not use that suppression condition. They therefore become ordinary observed facts.

### Ledger

For each observation, ingestion appends `observation.observed` and `evidence.observed`; if a fact is promoted, it also appends `fact.observed` or `fact.inferred`. Runtime observations have `source_type="discovery"`, so their promoted facts are ordinary `fact.observed` events.

### Projection

`StateProjector.project()` replays the event ledger. Its `apply()` method stores `observation.observed` events in `state.observations`, `evidence.observed` events in `state.evidence`, and observed/inferred fact events in projected facts. Tests prove runtime observations flow through collection, ingestion, ledger replay, and projection, including `state.get_current_facts("Seed", "seed_process_thread_count")`.

## 3. Does self-observation introduce any special persistence path?

No. The source explicitly says it does not persist anything itself and callers use `ObservationCollectionService` and `ObservationIngestor` as they do for other sources. The implementation contains no runtime-specific write API. Persistence occurs only when `ObservationIngestor` appends the ordinary observation, evidence, and fact events to `EventLedger`.

The strongest proof is the test named `test_observation_ingestor_accepts_seed_runtime_observations_without_special_path`, which bypasses `ObservationCollectionService` and sends collected runtime observations directly to `ObservationIngestor.ingest_many()`. The expected ledger events are the ordinary observation/evidence/fact sequence, and projected evidence source is `observation:discovery`.

## 4. Does self-observation introduce any special authority model?

No special authority model is introduced.

| Authority dimension | Implementation evidence |
| --- | --- |
| Permissions | The source reads `/proc/<pid>/status` and supplied file paths. Missing or unreadable status/files return no measurement rather than escalating. |
| Governance | Metadata records `runtime_governance=False`; no governance class or decision path is invoked. |
| Runtime privilege | Metadata records `read_only=True`, `local_only=True`, and `mutates_cluster=False`; the source only reads local process/file data. |
| Scheduler | Metadata records `scheduler=False`; the source has no background scheduling loop. |
| Mutation | Metadata records `mutates_cluster=False`. The only write is normal event-ledger recording performed by the ingestion pipeline, not cluster mutation by the source. |
| Shell execution | Metadata records `shell_execution=False` and `subprocess_execution=False`; collection uses Python file reads/stat calls. |

## 5. What implementation-backed questions can now be answered about Seed itself?

The observation inventory exposes `SeedRuntimeObservationSource` as a discovery provider with five predicates. The implementation-backed questions are exactly these:

1. How much resident memory is the Seed process using? (`seed_process_resident_memory_bytes` from `VmRSS` in `/proc/<pid>/status`.)
2. How many threads are visible for the Seed process? (`seed_process_thread_count` from `Threads` in `/proc/<pid>/status`.)
3. How long has the observed Seed runtime been running? (`seed_runtime_duration_seconds` from injected start monotonic time and current monotonic time.)
4. How large is the configured Seed SQLite database file? (`seed_sqlite_database_size_bytes` from filesystem stat of the supplied path.)
5. How large is the configured Seed event ledger file? (`seed_event_ledger_size_bytes` from filesystem stat of the supplied path.)

These questions are also discoverable through the app-facing observation inventory command: `python scripts/seed_local.py --observation-inventory --json` lists the provider and predicates.

## 6. What important questions still cannot be answered?

The current implementation does not support answers beyond those predicates. In particular, implementation does not answer:

- Whether Seed is healthy, overloaded, degraded, or should take action.
- Why memory or thread counts changed.
- CPU utilization, I/O rate, network activity, queue depth, request latency, or error rate.
- Which operator caused runtime behavior.
- Repository state, source-code correctness, or pending work status.
- Whole-machine health or host ownership.
- Historical time-series trends beyond what ordinary event history happens to contain after explicit collection.
- Any scheduled/background monitoring question.
- Any runtime governance or autonomous deferral question.

Those are unsupported because no predicates, collection logic, scheduler, governance model, or special telemetry subsystem exists for them in the reviewed implementation.

## 7. Would removing `SeedRuntimeObservationSource` produce implementation loss, observable capability loss, or both?

Both.

Implementation loss would include removal of the provider class, its process/file collection helpers, predicate questions in observation inventory discovery, and tests proving ordinary ingestion/projection of runtime observations.

Observable capability loss would include the disappearance of implementation-backed answers for Seed resident memory, Seed thread count, runtime duration, configured SQLite database size, and configured event-ledger size. The ordinary observation pipeline would remain, but Seed would no longer be represented as this process/runtime observation subject.

## 8. Does this strengthen the invariant that identity does not change the observation model?

Yes, with a narrow scope. The observed identity is unusual because the subject is Seed itself, but the model does not change: the source emits ordinary `Observation` objects, ingestion emits ordinary observation/evidence/fact ledger events, and projection replays those ordinary events into ordinary state structures.

Strongest supporting evidence:

- `SeedRuntimeObservationSource` implements the same source interface shape as other providers by exposing `name`, `source_type`, and `collect()`.
- Emitted values are plain `Observation` objects with source type `discovery` and subject `Seed`.
- `ObservationCollectionService` requires collected items to be `Observation` instances and then uses the shared normalizer/ingestor path.
- `ObservationIngestor` creates ordinary evidence and facts and appends ordinary event kinds.
- `StateProjector` projects those event kinds without checking whether the subject is `Seed`.
- Tests assert the exact ordinary event sequence and projected facts for Seed runtime observations.

Strongest contradictory evidence:

- The default subject label is hard-coded as `Seed`, so the source does introduce a Seed-specific observed subject name.
- Predicate names are Seed-specific (`seed_process_*`, `seed_runtime_*`, `seed_sqlite_*`, `seed_event_ledger_*`).
- Observation inventory has special AST-discovery handling for `SeedRuntimeObservationSource` so its predicate question constants are associated with the provider.
- The source reads `/proc/self`-style process data and configured Seed persistence paths, which is intrinsically self-referential even though persistence and projection remain ordinary.

These contradictions show that the domain and predicate vocabulary are Seed-specific. They do not show a special observation model, persistence path, authority model, scheduler, or governance path.

## Reconciliation

| Required item | Finding |
| --- | --- |
| Observed subject | The running Seed process/runtime represented as `Seed`, plus configured local Seed persistence artifact sizes attached to that subject. |
| Observation pipeline participation | Full participation: collection returns `Observation`; collection service validates/normalizes; ingestor records observation/evidence/fact events; ledger stores them; projector replays them into state. |
| Authority boundary | Read-only, local-only, no shell/subprocess execution, no scheduler, no runtime governance, no cluster mutation by the source. |
| Observable capabilities | Resident memory, thread count, runtime duration, SQLite database file size, event-ledger file size. |
| Remaining blind spots | Health, causality, CPU/I/O/network, operator behavior, repository correctness, machine-wide state, scheduler/background monitoring, governance decisions, and unsupported metrics. |
| Strongest supporting evidence | Shared `Observation`, `ObservationCollectionService`, `ObservationIngestor`, `EventLedger`, and `StateProjector` path with tests proving ordinary event sequence and projection. |
| Strongest contradictory evidence | Seed-specific subject default, Seed-specific predicates, and inventory discovery special-casing for provider predicate constants. |

## Acceptance answers

Has Seed become an ordinary observation subject? Yes, narrowly: the current Seed process/runtime has become an ordinary observed subject represented as `Seed`.

Does self-observation follow the same observation model as every other observed subject? Yes: it uses ordinary observations, evidence, fact events, event ledger persistence, and state projection. The identity and predicates are Seed-specific, but the model is not.

What observable capability would disappear if `SeedRuntimeObservationSource` were removed? Seed would lose implementation-backed observation of its own resident memory, thread count, runtime duration, configured SQLite database size, and configured event-ledger size.

## Report

### Commands executed

- `pwd && rg --files -g 'AGENTS.md' -g '!*.pyc' && git status --short`
- `cat AGENTS.md && rg "SeedRuntimeObservationSource|seed_process_resident_memory_bytes|diagnostic-inventory|ObservationCollectionService|ObservationIngestor|class Observation|event ledger|projection" -n .`
- `rg "SeedRuntimeObservationSource" -n seed_runtime scripts tests docs`
- `rg "seed_process_resident_memory_bytes|seed_process_thread_count|seed_runtime_duration_seconds|seed_sqlite_database_size_bytes|seed_event_ledger_size_bytes" -n seed_runtime scripts tests docs`
- `sed -n '1,360p' seed_runtime/observation_sources.py`
- `sed -n '1,260p' seed_runtime/observations.py`
- `sed -n '130,190p' seed_runtime/observation_inventory.py`
- `rg "class ObservationCollectionService|def collect" -n seed_runtime/observation_sources.py seed_runtime/state.py seed_runtime/events.py tests/test_runtime_self_observation.py tests/test_observation_ingestor.py tests/test_observation_inventory.py`
- `sed -n '228,340p' seed_runtime/observation_sources.py`
- `sed -n '380,420p' seed_runtime/observation_sources.py`
- `sed -n '3150,3245p' seed_runtime/observation_sources.py`
- `sed -n '1,140p' tests/test_runtime_self_observation.py`
- `sed -n '1,80p' tests/test_observation_ingestor.py`
- `sed -n '80,110p' tests/test_observation_inventory.py`
- `sed -n '3245,3275p' seed_runtime/observation_sources.py`
- `rg "class StateProjector|def project|observation.observed|fact.observed|evidence.observed" -n seed_runtime/state.py seed_runtime/events.py`
- `sed -n '715,790p' seed_runtime/state.py`
- `sed -n '940,980p' seed_runtime/state.py`
- `sed -n '1,130p' seed_runtime/events.py`
- `python scripts/seed_local.py --observation-inventory --json | python -m json.tool | rg -n "SeedRuntimeObservationSource|seed_process|seed_runtime|seed_sqlite|seed_event"`
- `pytest -q tests/test_runtime_self_observation.py tests/test_observation_ingestor.py tests/test_observation_inventory.py`

### Files inspected

- `AGENTS.md`
- `seed_runtime/observation_sources.py`
- `seed_runtime/observations.py`
- `seed_runtime/observation_inventory.py`
- `seed_runtime/events.py`
- `seed_runtime/state.py`
- `tests/test_runtime_self_observation.py`
- `tests/test_observation_ingestor.py`
- `tests/test_observation_inventory.py`

### Files changed

- `docs/self_observation_ordinary_domain_reconciliation.md`

### LOC changed

- Added 214 lines.

### Tests run

- `python scripts/seed_local.py --observation-inventory --json | python -m json.tool | rg -n "SeedRuntimeObservationSource|seed_process|seed_runtime|seed_sqlite|seed_event"`
- `pytest -q tests/test_runtime_self_observation.py tests/test_observation_ingestor.py tests/test_observation_inventory.py`

### Recommended bounded implementation slice

No implementation slice is recommended from this observational reconciliation. If a future task asks for a bounded implementation change, keep it limited to preserving visibility of existing runtime observation predicates in the normal observation inventory and shape-audit surfaces; do not add telemetry, scheduling, governance, dashboards, or health frameworks based on this report.
