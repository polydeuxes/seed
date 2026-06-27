# Execution Inquiry Orientation Investigation

This investigation asks how existing execution concepts appear from Seed's perspective as bounded questions. It does not add CLI behavior, schemas, diagnostics, ontology, or vocabulary. The findings below are documentation-only and are derived from implementation and existing audit evidence.

## Implementation summary

Seed already exposes execution-related evidence through multiple implementation-backed surfaces rather than through one execution-question owner:

- append-only events preserve runtime and ingestion history;
- observation ingestion converts observations into observation, evidence, and optional fact events;
- state projection replays ledger events and finalizes derived indexes;
- projection cache stores reusable snapshots and dependent read-model indexes without owning event history;
- runtime trace reconstructs a run from recorded events;
- runtime why formats a compact explanation for a historical run;
- execution status is transient operator feedback, not execution authority;
- formatters render narrow read-only surfaces;
- audit snapshots preserve local before/after operational snapshots.

## Execution questions recovered

| Bounded question Seed could ask | Natural concept reached | Evidence |
| --- | --- | --- |
| What happened during this runtime run? | runtime trace, event history, formatter | `RuntimeTraceReader` reconstructs one recorded run without replaying or mutating it, and the CLI formatter renders input, decision, policy, execution, response, error, and events. |
| Why did this runtime run decide and end that way? | runtime why, decision record, policy status, outcome | `format_runtime_why` summarizes user input, decision kind, decision reason, policy result, outcome, and final response or error. |
| Which events belong to this run? | event history, runtime trace | Runtime trace matches events by event id, causation id, correlation id, payload `run_id`, or decision record `run_id`. |
| How did observations become facts? | observation ingestion, event history | `ObservationIngestor.ingest_many` creates observation and evidence events and an optional fact event for each observation while preserving order inside a batched ledger append. |
| How long did observation ingestion take? | observation ingestion diagnostics, formatter | observation timing output reports source collection, normalization, event generation plus ledger write, totals, rates, and counters. |
| What state would Seed currently project from the ledger? | state projection, event history | existing audit evidence says `StateProjector.project` starts from empty state and replays ledger events, while `finalize` rebuilds derived projection indexes. |
| Did state projection reuse cache or replay events? | projection cache, projection diagnostics | the state cache status/rebuild paths inspect snapshot last-event ids and report cache availability/status; prior audit evidence records cache hit, incremental replay, full replay, and rebuild behavior. |
| Why was cache not reused? | projection cache, event history, cache status | cache status compares the ledger's current last event id with the snapshot last event id, making cache freshness the natural boundary. |
| Which dependent read-model caches are valid for this projected state? | dependent read-model caches | prior audit evidence states dependent summary/index snapshots must match state projection version and state last event id. |
| What operator-visible work is happening right now? | execution status | `ExecutionStatus` is renderer-independent, non-authoritative activity visibility, and producers emit phases such as collection, normalization, ingestion, cache, or done. |
| What does this execution-related surface claim to expose? | diagnostic inventory, formatters | the question-surface inventory contains question families and answering surfaces; diagnostic inventory/shape audit describe and validate operational surface shapes. |
| What local operational state changed between two snapshots? | audit snapshots | audit snapshot CLI paths create, list, and compare supported local operational snapshot kinds without making those snapshots execution truth. |

## Question to execution concept mappings

### What happened during this runtime run?

Primary concepts: runtime trace, event history, formatters.

Supporting contributors: decision records, policy events, tool result/failure events, assistant answer events, error event detection.

Authority boundary: a trace is a read-only reconstruction from ledger events; it does not replay the run, execute tools, append events, or mutate state.

### Why did this runtime run decide and end that way?

Primary concepts: runtime why, decision record.

Supporting contributors: policy summary, selected tool, final response, error extraction.

Authority boundary: this is an explanation over a recorded run. It owns presentation of why-like runtime evidence, not execution semantics, policy semantics, or event authority.

### How did observations become facts?

Primary concepts: observation ingestion, event history.

Supporting contributors: evidence conversion, optional fact promotion, ledger batch append, execution status progress.

Authority boundary: ingestion owns event creation from observations. It does not own projection truth; projected facts become visible only after state projection consumes the ledger.

### What state would Seed currently project from the ledger?

Primary concepts: state projection, event history.

Supporting contributors: event application, finalization, alias/relationship/support/conflict rebuilding.

Authority boundary: projection owns derived state from events. The event ledger remains historical authority, while projection indexes are derived and rebuildable.

### Did state projection reuse cache or replay events?

Primary concepts: projection cache, projection diagnostics.

Supporting contributors: projection store, snapshot last-event id, current ledger last-event id, incremental/full replay, cache rebuild commands.

Authority boundary: caches own reusable snapshots and dependent indexes, not event history or truth. A cache answer is about reuse/freshness, not about whether ledger facts are true.

### What operator-visible work is happening right now?

Primary concepts: execution status.

Supporting contributors: CLI status consumer, observation producer lifecycle, ingestion progress, projection/cache status phases.

Authority boundary: execution status is transient visibility. Existing audit evidence explicitly separates status producer from work semantics, projection authority, observation authority, and fact authority.

### What execution-related surfaces exist and do their declared shapes match implementation?

Primary concepts: diagnostic inventory, diagnostic shape audit, question surface inventory.

Supporting contributors: static registry rows, implementation specs, formatting functions, JSON support declarations.

Authority boundary: these are read-only surface declarations and static audits; they do not execute target surfaces or create operational evidence.

### What changed between local audit snapshots?

Primary concepts: audit snapshots.

Supporting contributors: snapshot creation/list/compare paths and snapshot kind selection.

Authority boundary: snapshots are local operational artifacts. They can support comparison questions but do not become cluster truth or execution authority.

## Shared bounded questions

Some bounded questions naturally require multiple concepts:

- **How did this command execute?** Runtime trace requires event history, decision records, policy events, tool events, response events, and the runtime trace formatter.
- **Why did this command end this way?** Runtime why combines input, decision reason, policy result, selected tool, outcome, final response, and errors.
- **Why was this command slow?** Runtime trace alone can show path and outcome, but timing evidence is stronger for observation ingestion because ingestion diagnostics explicitly expose collection, normalization, event-generation/ledger-write, total seconds, and rates. The repository evidence inspected does not show a universal per-command latency explanation surface.
- **Why was cache not reused?** Projection cache status depends on ledger event history and snapshot last-event ids; dependent read-model caches further depend on matching projection version and state last-event id.
- **Which execution path occurred?** Runtime trace and event history identify decision, policy, tool, assistant, and error events; runtime why presents a concise path explanation.

## Concepts with no natural inquiry found

No recovered concept is wholly unreachable by a natural bounded question, but several are more naturally supporting evidence than primary inquiry targets:

- **formatters** answer presentation questions, but they rarely become the primary subject except when asking how an answer is rendered;
- **dependent read-model caches** are usually reached through cache reuse/freshness questions rather than direct user inquiry;
- **execution status** is naturally reached by live operator visibility questions, not by durable historical questions unless separately recorded;
- **audit snapshots** are naturally reached by before/after comparison questions, not by command execution questions.

## Current investigation orientation

Current execution investigations are primarily oriented around implementation ownership, with partial bounded-inquiry pressure.

Implementation-oriented evidence:

- existing audits are titled and structured around implementation ownership areas such as execution status producer contracts, projection cache capability, runtime/tool ownership, and response producers;
- the projection/cache audit asks what exists, who owns cache vs ledger vs projection, and where assumptions live;
- the execution-status contract audit separates producer boundaries from work semantics and preserves open contract questions.

Bounded-inquiry evidence:

- the question-surface inventory explicitly stores question families, example questions, answering surfaces, answer responsibility, and authority boundaries;
- response reconciliation lists operator questions existing surfaces can answer, including runtime-run and runtime-why questions;
- runtime trace and runtime why are already inquiry-shaped around a run id.

Finding: repository behavior is mixed, but execution investigations remain more implementation-owner-oriented than question-oriented. Bounded questions exist as read-only surfaces and inventories, yet most execution concepts are preserved as implementation slices.

## Answer ownership

| Representative question | Primary answer owner | Supporting contributors | Authority boundary |
| --- | --- | --- | --- |
| What happened during this runtime run? | `RuntimeTraceReader` / runtime trace formatter | Event ledger, decision record, policy/tool/assistant/error events | Read-only reconstruction; no replay, writes, or mutation. |
| Why did this runtime run decide and end that way? | runtime why formatter | Runtime trace summary, decision reason, policy outcome, final response/error | Explanation over recorded run; no policy or execution ownership. |
| Which events belong to this run? | runtime trace matching logic | Event id, causation id, correlation id, payload run ids | Event membership only; not semantic correctness of the run. |
| How did observations become facts? | `ObservationIngestor` | Observation-to-evidence, observation-to-fact, ledger append, status consumer | Event creation from observations; projection remains separate. |
| How long did observation ingestion take? | observation ingestion diagnostics formatter | collection service, normalization, ledger append counters | Timing diagnostics only; not fact authority. |
| What state projects from the ledger? | `StateProjector` | Event ledger, event handlers, finalization indexes | Derived state from events; ledger remains authority. |
| Was projection cache reused? | projection cache/store status functions | SQLite ledger, projection store, snapshot metadata | Cache freshness/reuse only; not truth ownership. |
| Are dependent caches valid? | projection store/dependent snapshot validation | State projection version and state last-event id | Read-model validity relative to state snapshot. |
| What operator-visible work is happening? | execution status consumer/producers | lifecycle/status emitters, CLI stderr renderer | Transient visibility; non-authoritative. |
| What surfaces exist and are shaped correctly? | diagnostic inventory and shape audit | question-surface inventory, implementation specs, tests | Static/read-only declarations; no target execution. |
| What changed between audit snapshots? | audit snapshot helpers | snapshot kind readers and comparison formatters | Local comparison artifact; not cluster truth. |

## Execution characterization: inventory, diagnostic, explanation, answer

Execution characterization is a combination:

- **Inventory** when Seed asks which execution-related surfaces or concepts exist. Diagnostic inventory and question-surface inventory are explicit inventory surfaces.
- **Diagnostic** when Seed asks whether shapes, cache freshness, observation timing, projection reachability, or surface declarations match implementation expectations.
- **Explanation** when Seed asks why a run decided or ended a certain way. Runtime why is explanation-oriented, but only for recorded runtime evidence.
- **Answer** when a bounded question selects a primary owner and authority boundary. Runtime trace, runtime why, cache status, and ingestion timing can each answer concrete questions.

It is not only an inventory. The repository already has inventory rows, diagnostic audits, runtime explanations, and direct bounded answers, but these are distributed across implementation-owned surfaces.

## Smallest question set that exposes most recovered concepts

1. **What happened during this runtime run?** Exposes event history, runtime trace, execution path, response, errors, and formatters.
2. **Why did this runtime run decide and end that way?** Exposes runtime why, decision reason, policy status, outcome, final response/error, and explanation boundaries.
3. **How did observations become projected state?** Exposes observation ingestion, observation/evidence/fact events, state projection, and the ledger/projection boundary.
4. **Did projection reuse cached state or rebuild it?** Exposes projection diagnostics, projection cache, dependent read-model cache validity, event-last-id boundaries, and cache authority limits.
5. **What operator-visible work is happening or recorded for this surface?** Exposes execution status, diagnostics, diagnostic inventory, shape audit, and audit snapshots.

## Inquiry-oriented findings

- Seed has natural bounded questions for runtime history, runtime why, ingestion transformation, projection construction, cache reuse, and operational visibility.
- The strongest existing inquiry shape is run-id-oriented: runtime trace and runtime why both start from a bounded run identifier.
- Cache and ingestion questions are naturally operational-diagnostic rather than semantic-explanation questions.
- Question-surface inventory is the clearest repository mechanism for storing inquiry orientation, but it does not currently enumerate these execution questions as a dedicated family.

## Implementation-oriented findings

- Execution concepts are implemented as separate owners: ledger, ingestor, projector, projection store, runtime trace reader, status consumers, formatters, diagnostic registries, and snapshot helpers.
- Existing audits commonly preserve ownership boundaries before preserving operator questions.
- Formatters are important contributors but generally do not own source semantics.
- Execution status deliberately avoids becoming execution state.

## Orientation mismatches

- Runtime trace is inquiry-shaped, but much surrounding execution documentation remains implementation-slice-shaped.
- Projection cache appears in operational vocabulary, but repository instructions warn not to promote presentation vocabulary into knowledge without reachability evidence.
- Ingestion timing can answer slowness questions for observation paths, but there is no universal command-latency explanation surface in the inspected evidence.
- Dependent read-model caches matter operationally but are more naturally exposed through cache validity questions than through direct human inquiry.
- Diagnostic inventory and shape audit organize surfaces, not the execution questions those surfaces answer.

## Commands executed

- `pwd && rg --files -g 'AGENTS.md' -g '! .git' && git status --short`
- `cat AGENTS.md && rg -n "execution|projection cache|runtime trace|diagnostic-inventory|knowledge-reachability|audit snapshot|execution status|event history|observation ingestion|state projection|formatters" .`
- `rg -n "runtime trace|execution status|projection cache|ingestion timing|audit snapshot|diagnostic inventory|shape audit|event history|StateProjector|ObservationIngestion|format_.*runtime|question" scripts/seed_local.py seed_runtime tests docs/current_implementation_audit_execution_observation_projection_cache_capability.md docs/execution_status_producer_contract_implementation_audit.md docs/tool_execution_ownership_audit.md docs/response_reconciliation.md`
- `sed -n '127,335p' seed_runtime/question_surface_inventory.py`
- `sed -n '6084,6195p' scripts/seed_local.py`
- `sed -n '3334,3375p' scripts/seed_local.py`
- `sed -n '130,190p' docs/current_implementation_audit_execution_observation_projection_cache_capability.md`
- `sed -n '277,294p' docs/response_reconciliation.md`
- `sed -n '1,120p' seed_runtime/execution_status.py`
- `sed -n '1,90p' seed_runtime/runtime_trace.py`
- `sed -n '90,190p' seed_runtime/runtime_trace.py`
- `sed -n '120,230p' seed_runtime/execution_status.py`
- `sed -n '680,735p' scripts/seed_local.py`
- `sed -n '7350,7425p' scripts/seed_local.py`
- `sed -n '1,80p' seed_runtime/projection_store.py`
- `rg -n "class ObservationIngestor|ObservationIngestionDiagnostics|append|observation" seed_runtime -g '*.py' | head -80`
- `sed -n '1,180p' seed_runtime/observations.py`
- `sed -n '180,320p' seed_runtime/observations.py`
- `sed -n '190,245p' docs/execution_status_producer_contract_implementation_audit.md`

## Files inspected

- `AGENTS.md`
- `scripts/seed_local.py`
- `seed_runtime/question_surface_inventory.py`
- `seed_runtime/runtime_trace.py`
- `seed_runtime/execution_status.py`
- `seed_runtime/observations.py`
- `seed_runtime/projection_store.py`
- `docs/current_implementation_audit_execution_observation_projection_cache_capability.md`
- `docs/execution_status_producer_contract_implementation_audit.md`
- `docs/response_reconciliation.md`

## Files changed

- `docs/execution_inquiry_orientation_investigation.md`

## LOC changed

- Added 245 lines.

## Tests run

No test suite was run because this is a documentation-only implementation investigation and no CLI surface, diagnostic behavior, or runtime behavior was changed.

## Conclusion

The repository naturally organizes execution primarily around implementation concepts, with bounded execution questions emerging as secondary read-only surfaces. Runtime trace and runtime why are already question-shaped, and question-surface inventory preserves broader inquiry orientation, but the recovered execution concepts are still mostly owned, audited, and documented by implementation boundaries rather than by a compact set of bounded execution questions.
