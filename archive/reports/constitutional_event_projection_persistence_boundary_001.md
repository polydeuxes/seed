# Constitutional event/projection/persistence boundary 001

## Question

This investigation asks the repository where it draws the constitutional boundary among:

- **Event Ledger:** durable append-only history.
- **Projection:** Seed's current reconstructed constitutional condition.
- **Snapshot/cache:** disposable acceleration of projection rebuilding.
- **Transient result:** local live computation that need not survive its bounded use.

The answer is evidence-bound and deliberately does not design a scheduler, event bus, subscription system, or mandatory event taxonomy.

## Repository evidence reviewed

Implementation evidence gives four distinct persistence roles.

1. `EventLedger` is the append-only event-history owner. It stores events in append order, indexes them by id and workspace, rejects duplicate ids, and is identified architecturally as `event_history` feeding `StateProjector`.
2. `SQLiteEventLedger` preserves the same event-ledger API in SQLite. This supports durable event history without turning SQLite itself into projection truth.
3. `StateProjector` rebuilds current inspectable state from ledger events. Its `project_from_state(...)` explicitly says event history remains authority when reusing a snapshot.
4. `ProjectionStore` snapshots are cache inputs. `project_state_with_cache(...)` loads a snapshot only when eligible and matching the current latest event id, otherwise replays ledger events and saves a fresh state snapshot.
5. `ExecutionStatus` is explicitly transient, renderer-independent, and non-authoritative. A missing consumer causes status emission to return without preserving anything.
6. Read-only selection and projection artifacts repeatedly carry boundary fields such as `writes_event_ledger=False`, `starts_recording=False`, and `mutates_cluster=False`, showing that constitutional/local responsibility occurrence is not automatically event recording.

## Smallest supported boundary model

| Role | Repository-supported meaning | Not supported by evidence |
| --- | --- | --- |
| Event Ledger | Durable append-only records of occurrences that Seed later replays or audits as history. | Every function call, local decision, diagnostic computation, cache write, or constitutional act must be an event. |
| Projection | Current inspectable state reconstructed from events plus deterministic derived indexes and projections. | Projection is canonical history, or current view truth can replace the ledger. |
| Snapshot/cache | Disposable persisted acceleration tied to projection version, latest event id, and non-mutating boundary eligibility. | Cache freshness is truth, or snapshots are canonical evidence. |
| Transient result | Bounded live computation passed to an immediate consumer or renderer without persistence. | Transient outputs are cross-tick recognizable unless separately recorded or reconstructible from preserved inputs. |

## Representative roads

### Road 1: Observation ingestion records observation/evidence/fact before projection consumers recognize it

| Field | Repository-supported answer |
| --- | --- |
| producer | `ObservationIngestor.ingest_many(...)`. |
| local result | A list of `Fact | None` values returned to the caller after constructing observation, evidence, and optional fact events. |
| whether producer occurrence is recorded | Yes, when observations are ingested. Each observation produces `observation.observed`, `evidence.observed`, and unless suppressed, `fact.observed` or `fact.inferred`. |
| event kind and payload, if any | `observation.observed` with `{"observation": ...}`; `evidence.observed` with `{"evidence": ..., "observation_id": ..., "source_type": ...}`; fact event with `{"fact": ..., "observation_id": ..., "source_type": ...}`. |
| projection consumer | `StateProjector.apply(...)` consumes these event kinds into `state.observations`, `state.evidence`, and `state.facts`, then finalization rebuilds derived indexes. |
| current-state effect | Current state gains observation/evidence/fact entries, observed/inferred partitions, fact supports, relationships, aliases, conflicts, and validation issues as applicable. |
| later competency consumer | State views and ownership/read-model diagnostics consume projected facts/evidence rather than the original live return value. |
| whether direct uptake is possible without recording | Locally, the caller receives the returned facts, but cross-tick recognition by Seed's state requires ledger events. |
| whether the result is reconstructible | Yes, from the recorded events, subject to deterministic projection/finalization rules. |
| whether losing it would destroy unique evidence | Losing the ledger events would destroy the durable observation/evidence/fact history. Losing only the live returned list would not if events were appended. |
| whether a snapshot/cache is sufficient | No for history. A projection snapshot can accelerate rebuilding current state after the events exist, but cannot replace the events as durable observation history. |

### Road 2: Tool execution records execution first, then extracts evidence from the durable completion event

| Field | Repository-supported answer |
| --- | --- |
| producer | `ToolExecutor._execute_allowed_tool_call(...)`, `_record_completed_tool_call(...)`, and `_realize_registered_operation(...)`. |
| local result | A validated registered operation returns `output`; `ToolExecutor` returns a `ToolCallResult` with status, message, output, and completed event id. |
| whether producer occurrence is recorded | Yes for execution history. The executor records `tool.call.started`, `tool.call.completed`, `tool.call.failed`, policy-blocked, or approval-required events depending on path. |
| event kind and payload, if any | Completed execution uses `tool.call.completed` with `{"tool": tool.name, "output": output}`; failed execution uses error payloads; policy paths record policy events. |
| projection consumer | `FactExtractionService.observe_tool_result(...)` consumes the durable completed event and appends `evidence.observed`; `StateProjector` later projects that evidence into state. |
| current-state effect | The completed tool call itself is durable history; extracted tool output becomes evidence in projected state. The generic extraction path intentionally does not infer facts. |
| later competency consumer | Evidence and fact/projection views can later see the evidence event; execution audits can see execution events. |
| whether direct uptake is possible without recording | The executor can directly return the operation output to its caller in the same live context, but its own code records completion before extracting post-execution knowledge. |
| whether the result is reconstructible | The evidence observation is reconstructible from the completed event only if the completed event payload was durably recorded. The live Python return value alone is not cross-tick evidence. |
| whether losing it would destroy unique evidence | Losing the completion/evidence events loses unique execution/evidence history. Losing a transient `ToolCallResult` does not if events persist. |
| whether a snapshot/cache is sufficient | No for execution history or evidence. Cache may speed current-state projection after events exist. |

### Road 3: Read-only goal selection feeds later local projection without an intervening ledger event

| Field | Repository-supported answer |
| --- | --- |
| producer | `select_goal_for_inquiry_consideration(...)`. |
| local result | `GoalInquiryConsiderationSelection`, derived from a `GoalOrientationInventory` and explicit focus evidence. |
| whether producer occurrence is recorded | No. The artifact declares `starts_recording=False`, `writes_event_ledger=False`, `read_only=True`, and `mutates_cluster=False`. |
| event kind and payload, if any | None. |
| projection consumer | `project_inquiry_need(...)` directly consumes the selection together with a bounded goal, horizon, and uncertainty testimony. |
| current-state effect | None in the ledger-backed `State`; it produces a read-only inquiry-need projection artifact that also declares no event-ledger write or cluster mutation. |
| later competency consumer | A later live responsibility can consume the passed artifact or a separately preserved/rendered artifact. Later recognition through Seed projected state is not available unless some owning path records or preserves sufficient inputs. |
| whether direct uptake is possible without recording | Yes. This is the clearest road where one bounded responsibility consumes another's result directly in live context without an intervening ledger event. |
| whether the result is reconstructible | Yes if the inventory and focus evidence inputs are preserved and deterministic; Unknown if those inputs were only live and discarded. |
| whether losing it would destroy unique evidence | No if it is fully recomputable from preserved inputs; yes if the focus evidence or inventory snapshot was unique and not otherwise preserved. |
| whether a snapshot/cache is sufficient | A cache/snapshot may be sufficient for speed or operator inspection only when the authoritative inputs remain available or when no later durable recognition is required. |

### Road 4: Consumer-local admission is direct uptake, not transferable history

| Field | Repository-supported answer |
| --- | --- |
| producer | `admit_downstream_interpretation(...)`. |
| local result | `DownstreamInterpretationAdmission`, bound to one exact consumer and purpose. |
| whether producer occurrence is recorded | No. Boundary notes say admission stops before recording, event-ledger writes, state mutation, or cluster mutation; dataclass fields preserve the same boundary. |
| event kind and payload, if any | None. |
| projection consumer | `establish_bounded_operator_goal_from_admitted_interpretation(...)` can directly consume the admission artifact as lawful ingress. |
| current-state effect | No ledger-backed projected-state effect. A bounded-goal establishment artifact may result in live context, but it too declares no event-ledger write or cluster mutation. |
| later competency consumer | Later consumers cannot infer transferable authority merely from the admission vocabulary. They need the admission artifact, preserved inputs, or a separately recorded/projected condition. |
| whether direct uptake is possible without recording | Yes, within the exact consumer-local boundary. |
| whether the result is reconstructible | Reconstructible from selection, applicability projection, and admission evidence if those are preserved; otherwise only live. |
| whether losing it would destroy unique evidence | Losing unrecorded admission evidence may destroy unique evidence for why that exact consumer admitted or refused. Losing recomputable derived admission does not if inputs remain. |
| whether a snapshot/cache is sufficient | A snapshot may be enough for disposable replay/inspection, but not as canonical history or transferable authority. |

### Road 5: Projection cache accelerates rebuilding but does not become truth

| Field | Repository-supported answer |
| --- | --- |
| producer | `project_state_with_cache(...)` and `_save_state_snapshot(...)`. |
| local result | A `State` plus `StateCacheStatus` indicating hit/miss, current latest event id, snapshot last event id, and events applied. |
| whether producer occurrence is recorded | The cache write is not an event-ledger occurrence. It saves a `ProjectionSnapshot` in `ProjectionStore`. |
| event kind and payload, if any | None for the cache write. |
| projection consumer | Future `project_state_with_cache(...)` calls may load the snapshot if the projection name/version and last event id match and the boundary is cache-eligible. |
| current-state effect | It returns the same kind of current projected state faster on cache hit, or replays/incrementally replays events on miss. |
| later competency consumer | CLI/read-model consumers may consume the returned projected state, but their authority is still tied to ledger-backed projection inputs, not snapshot existence. |
| whether direct uptake is possible without recording | Yes. The local caller can use the returned state immediately. |
| whether the result is reconstructible | Yes, from ledger events and deterministic projection if the ledger remains. |
| whether losing it would destroy unique evidence | No, if ledger events remain. A cache loss causes rebuild cost, not loss of constitutional history. |
| whether a snapshot/cache is sufficient | Yes only as disposable acceleration of projection rebuilding. It is insufficient as canonical history or unique evidence. |

### Road 6: Transient execution status may be consumed or ignored without persistence

| Field | Repository-supported answer |
| --- | --- |
| producer | `emit_status(...)`, `emit_progress_if_due(...)`, and `ExecutionStatusEmitter`. |
| local result | `ExecutionStatus` values with phase, message, progress counts, and completion flag. |
| whether producer occurrence is recorded | No by default. The null consumer ignores it; the recording consumer stores in memory for tests/non-persistent inspection; CLI consumer renders to stderr. |
| event kind and payload, if any | None. |
| projection consumer | None. Status updates explicitly do not own execution state. |
| current-state effect | None. |
| later competency consumer | None unless some caller separately captures the status stream as an artifact. |
| whether direct uptake is possible without recording | Yes. A live consumer can render or collect status immediately. |
| whether the result is reconstructible | Often partially from the underlying ledger/projection operation, but exact progress timing/status stream is not guaranteed reconstructible. |
| whether losing it would destroy unique evidence | Usually no for constitutional history; yes only if the task intentionally treats progress stream as the evidence under investigation. |
| whether a snapshot/cache is sufficient | Not needed for constitutional persistence; a non-persistent recording consumer is enough for bounded tests/inspection. |

### Road 7: SQLite read models are persistence media, not automatically constitutional truth

| Field | Repository-supported answer |
| --- | --- |
| producer | `SQLiteEventLedger` for durable events; `ProjectionStore`/SQLite-compatible stores for snapshots and derived read models. |
| local result | Rows representing ledger events or cached projections/read models, depending on table and owner. |
| whether producer occurrence is recorded | Ledger rows are durable event history; projection/cache rows are not themselves ledger events. |
| event kind and payload, if any | Ledger rows preserve event `kind`, workspace, actor, timestamp, payload, and correlation fields. Snapshot rows preserve projection identity, version, last event id, and serialized state payload. |
| projection consumer | `StateProjector` consumes ledger events; cache logic may consume snapshot payloads only when compatible and current. |
| current-state effect | Ledger-backed events can change reconstructed state. Cache/read-model rows can supply a faster materialization of state or view, but only within eligibility rules. |
| later competency consumer | Later consumers may use read models for current views, but should not confuse a read model with event history. |
| whether direct uptake is possible without recording | A responsibility can directly consume a returned SQLite/read-model row in live context, but later constitutional recognition depends on whether it was a ledger event or only a read model/cache row. |
| whether the result is reconstructible | Ledger events are the reconstruction source; caches are reconstructible from ledger when deterministic and current. |
| whether losing it would destroy unique evidence | Losing a SQLite ledger destroys durable history if no backup exists. Losing a projection/read-model cache does not, if ledger events remain. |
| whether a snapshot/cache is sufficient | Sufficient for faster rebuilding/current read access; insufficient for durable history. |

## Candidate distinctions tested quietly

- **constitutional occurrence != event recording:** Supported. Read-only selection, admission, establishment, and projections are constitutional/local artifacts but explicitly do not record events.
- **event != snapshot:** Supported. Events are appended to the ledger; snapshots are saved in `ProjectionStore` with projection metadata and cache eligibility.
- **event != projection:** Supported. Events are input history; projection is rebuilt current state.
- **projection != canonical history:** Supported. `project_from_state(...)` says event history remains authority when a snapshot is reused.
- **cache freshness != truth:** Supported. Matching latest event id and projection version can justify cache use, not truth independent of events.
- **direct live uptake != cross-tick recognition:** Supported. Local artifacts can be passed directly, while projected-state recognition requires recorded events or preserved/recomputable inputs.
- **recomputable result != durable observation:** Supported. Deterministic projections and selections may be recomputed without being durable observations.
- **recorded assertion != verified truth:** Supported. Observation/fact/evidence events preserve provenance, confidence, source type, and later conflict/validation projections; recording alone does not prove semantic truth.

## Disagreement and Unknowns preserved

- The repository does not force a universal list of event kinds that every constitutional act must use.
- The repository does not prove that every read-only constitutional artifact should be persisted as a file, snapshot, event, or read model.
- The repository does not prove that every transient status/progress update is reconstructible exactly.
- The repository does not settle all SQLite read-model authority boundaries. It supports distinguishing event-ledger rows from projection/cache/read-model rows, but each concrete table must still be interpreted by its implementation owner.
- The repository supports fact promotion from observations in the current ingestion path, but also contains explicit suppression for one Prometheus OS observation path; therefore observation does not always imply fact promotion.

## Smallest repository-supported answers

### What constitutionally counts as an event?

An event is a durable append-only ledger entry with a kind, workspace, actor, timestamp, payload, and causal/correlation context that Seed can later replay, audit, or use as historical provenance. The smallest supported rule is not semantic grandeur; it is ledger admission by an owner that records the occurrence as history.

### When must an occurrence enter durable history?

An occurrence must enter durable history when later reconstruction, provenance, audit, authorization state, execution history, evidence observation, fact observation/inference, pending action state, or other cross-tick recognition depends on the occurrence as unique historical evidence. If losing the occurrence would destroy the only support for projected condition or later accountability, a transient result or cache is insufficient.

### When may a result remain transient?

A result may remain transient when it is bounded to immediate live use, does not need cross-tick recognition, is fully recomputable from preserved inputs, or is intentionally only renderer/operator progress visibility. Direct selection/admission/projection artifacts can be consumed live without recording when their boundary says no recording and no state/cluster mutation.

### When should a projection be cached or snapshotted?

A projection should be cached or snapshotted only as disposable acceleration or inspection support when it is tied to projection identity/version and ledger position, is eligible under non-mutating boundary rules, and can be invalidated/rebuilt from authoritative inputs. Cache loss should be acceptable when ledger/history remains.

### Can one bounded responsibility consume another's result without an intervening ledger event?

Yes. The repository directly supports live handoffs such as goal selection into inquiry-need projection and downstream interpretation admission into bounded-goal establishment. This is lawful only inside the bounded consumer/purpose context and does not by itself create later projected state or transferable authority.

### What distinguishes direct live uptake from later recognition through projected state?

Direct live uptake is a caller/consumer using a returned artifact in the same bounded context, with no durable event required. Later recognition through projected state requires either ledger events that the projector replays or preserved inputs from which the result is recomputed. Projection is the current reconstructed condition; it is not the canonical history, and cache freshness is not truth.
