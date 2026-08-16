# Operational Vocabulary Compatibility Boundary Audit

## Scope

This is a recovery-only audit of compatibility boundaries that depend on the current operational vocabulary family. It does not propose replacement names, a rename sequence, shims, deprecations, or runtime redesign.

The implementation evidence shows that Seed has enough recovered information to plan a future compatibility-preserving vocabulary migration, but not enough to execute one safely without a separate migration design. The current vocabulary is not a single naming problem: it is a compatibility family spanning model decisions, event kinds, serialized Pydantic models, toolkit manifests, capability catalogs, CLI/API JSON, diagnostic/question surfaces, tests, and documentation.

## Compatibility surfaces

| Surface | Current vocabulary | Compatibility boundary | Evidence |
|---|---|---|---|
| Model decision schema | `call_tool`, `request_tool`, `tool_name`, `tool_arguments`, `tool_need` | Public structured model/decision input and retry payload vocabulary. Any migration must preserve accepted decision kinds and payload keys while consumers exist. | `DecisionKind` and `Decision` fields are typed model fields; `DecisionValidator` branches on those kinds and validates `tool_need` / `tool_name`. |
| Runtime response JSON | `kind="tool_need"`, `payload.tool_need`, `payload.recommendations`, `payload.capability_resolution` | External API/CLI consumers can depend on response kinds and payload keys. | `Runtime._route()` returns this payload for `request_tool`; API tests assert it. |
| Event ledger replay | `tool_need.created`, `tool_need.status_changed`, `tool.registered`, `tool.call.started`, `tool.call.completed`, `tool.call.failed`, `model.decision.proposed` | Highest sensitivity: persisted event histories and replay depend on event names and payload keys. | `StateProjector` rehydrates `ToolNeed` and `ToolSpec` from event kinds; execution appends tool call events. |
| Serialized models | `ToolNeed`, `ToolSpec`, `Toolkit`, `CapabilityRecommendation`, `ExecutionStatus`, `RuntimeResponse` fields | Public if emitted through API, CLI JSON, event ledger, state, toolkit manifests, or diagnostics. Field names are compatibility contracts. | Models are Pydantic domain records and API methods serialize them with `to_plain()`. |
| Toolkit manifests | `tools`, per-tool `name`, `input_schema`, `output_schema`, `policy_action`, `implementation`, `visibility`, `risk_class`, `capabilities` | Strong public contract for checked-in and generated toolkit manifests. | Registry loader requires manifest keys and constructs `ToolSpec`. |
| Capability catalog YAML | `capability`, `summary`, `recommendations`, `provider`, `kind`, `backend_type`, `operation` | Public repository data format. Especially hazardous because `operation` is not always executable. | `CapabilityCatalog` loads YAML entries into `CapabilityCatalogEntry` and `CapabilityRecommendation`. |
| Developer API | `SeedAPI.get_toolkits()`, `get_tools()`, `get_tool_needs()` | Public adapter-facing vocabulary. | API exposes tool/toolkit/tool-need records as dictionaries. |
| CLI flags and output | `--events`, `--current-capabilities`, `--capability-*`, `--diagnostic-inventory`, `--question-surface-inventory`, execution-status stderr | Public operator surface; flag and JSON key changes require compatibility handling. | `scripts/seed_local.py` imports and formats operational records and exposes diagnostic/question flags. |
| Diagnostic inventory / shape audit | names such as `diagnostic_inventory`, `question_surface_inventory`; descriptions containing execution, mutation, event-ledger vocabulary | Public introspection contract. Changing operational surfaces must update inventory/specs/tests under repository instructions. | Diagnostic inventory and shape-audit specs register CLI flags, JSON support, recordability, ledger mutation, and cluster mutation. |
| Question surfaces | `question_surface_inventory`, execution/capability question families in docs and registry | Public explanatory surface for bounded questions. | Question inventory links answer responsibilities to diagnostic surfaces. |
| Tests | Assertions on event kinds, response payload keys, manifest keys, no-execution boundaries | Compatibility safety net and evidence of expected behavior. | Tests assert request-tool payload shape, event sequences, capability inventory from `tool_need.created`/`tool.registered`, and absence of `tool.call.started` in non-execution paths. |
| Documentation / architecture notes | `ToolNeed`, `ToolSpec`, `ToolRegistry`, `ToolExecutor`, `Runtime`, `Execution`, `Capability`, request/call-tool boundaries | Public contributor contract, but lower runtime sensitivity than ledgers/manifests/API. | Existing reconciliation docs preserve capability-vs-execution and tool-vocabulary boundaries. |

## Operational vocabulary exposure table

| Concept | Internal implementation | Public API | Serialized representation | CLI exposure | Documentation exposure | Test dependency | Compatibility sensitivity |
|---|---:|---:|---:|---:|---:|---:|---|
| `ToolNeed` | Yes: model and service-created record | Yes: `SeedAPI.get_tool_needs()` and runtime responses | Yes: `tool_need.created` payload and projected state | Yes: event/state/capability views | Heavy | Heavy | High |
| `ToolNeedService` | Yes | Mostly no direct API, but behavior public through `request_tool` | Event-producing owner, not itself serialized | Indirect | Heavy | Medium | Medium-high |
| `request_tool` | Yes: decision route | Yes: decision schema / runtime behavior | Yes inside `model.decision.proposed` payload | Indirect via events and app flows | Heavy | Heavy | High |
| `ToolSpec` | Yes: registered operation model | Yes: `SeedAPI.get_tools()` | Yes: `tool.registered`, manifests, state | Yes: current tools / inventory surfaces | Heavy | Heavy | High |
| `Toolkit` / `toolkit` | Yes: registry model | Yes: `SeedAPI.get_toolkits()` | Yes: manifests and serialized API output | Yes: registration/dev surfaces | Medium | Heavy | High |
| `ToolRegistry` | Yes | Indirect through API and validation | No as object; outputs serialized tools/toolkits | Indirect | Heavy | Heavy | Medium |
| `ToolExecutor` | Yes | Indirect through `call_tool` | No as object; appends `tool.call.*` | Indirect through event output and runtime | Heavy | Heavy | High because event names are durable |
| `call_tool` | Yes: decision route | Yes: decision schema | Yes inside decision/event payloads | Indirect | Heavy | Heavy | High |
| `ToolCallResult` | Yes | Indirect as `RuntimeResponse` conversion | Payload/result fields may surface | Indirect | Medium | Medium | Medium |
| `Runtime` | Yes: canonical router | Yes through `SeedAPI.post_user_message()` | Event sequences and response kinds | Yes through app command | Heavy | Heavy | Medium-high |
| `ExecutionStatus` | Yes: transient status object | Potential developer API/protocol | Not ledger-persisted by design | Yes: CLI stderr progress | Medium | Heavy | Medium: public presentation, not durable truth |
| `Execution*` legacy models | Yes but quarantined (`ExecutionAuthorization`, proposals) | Limited/direct imports in tests | Yes if historical events exist | Limited | Heavy | Medium | High where ledger replay exists; otherwise intentionally historical |
| `CapabilityCatalog` | Yes | Indirect through recommendations/resolution | YAML catalog entries; response payloads | Indirect capability output | Heavy | Heavy | High for YAML/JSON fields |
| `CapabilityRecommendation` | Yes | Indirect through recommendations | Yes: catalog YAML and payload subset | Indirect | Heavy | Heavy | High for catalog; medium for ranked response subset |
| `Capability*` diagnostic/inventory records | Yes | Indirect CLI/API JSON | Yes in diagnostic JSON/read models | Yes (`--capability-*`) | Heavy | Heavy | Medium-high |
| `tool` generic word in local variables | Yes | No | No | No | No | Low | Low when truly local |
| `execution` generic word in timing/status internals | Yes | Sometimes | Sometimes | Sometimes | Heavy | Medium | Split: low local, medium/high when phase names or event fields are emitted |

## Concept-by-concept boundary recovery

### ToolNeed / request_tool

`ToolNeed` is not implementation-local. It is a durable model with fields for id, workspace, name, summary, capability, reason, originating event, risk hint, status, desired inputs, and desired outputs. `request_tool` is a typed decision kind. `ToolNeedService.create_from_decision()` creates or deduplicates a `ToolNeed`, appends `tool_need.created`, and `Runtime._route()` returns a `kind="tool_need"` response containing the serialized need, recommendations, and capability-resolution metadata.

Compatibility boundaries:

- decision kind: `request_tool`;
- decision payload key: `tool_need`;
- validation error text and shape: `tool_need.name`, `tool_need.summary`, `tool_need.capability`;
- event kinds: `tool_need.created`, `tool_need.status_changed`;
- event payload keys: `tool_need`, `tool_need_id`, `status`;
- response kind and payload: `tool_need`, `recommendations`, `capability_resolution`;
- state projection fields and API `get_tool_needs()` output;
- tests and docs preserving that `request_tool` never executes.

Sensitivity: high. This can migrate only with event replay, response/schema, API, docs, and tests considered together.

### ToolSpec / Toolkit / ToolRegistry

`ToolSpec` is both a runtime model and a serialized manifest/API/event record. `ToolRegistry` itself is closer to an implementation service, but its vocabulary is exposed through tool manifests, API output, validation errors, capability lookup, and state projection from `tool.registered` events.

Compatibility boundaries:

- toolkit manifest top-level keys `id`, `name`, `summary`, `tools`, `status`, `source`;
- per-tool keys `name`, `summary`, `input_schema`, `output_schema`, `policy_action`, `implementation`, `status`, `visibility`, `risk_class`, `capabilities`, `examples`;
- API `get_toolkits()` / `get_tools()` serialized records;
- event kind `tool.registered` and payload key `tool`;
- registry methods and developer imports;
- capability lookup semantics for registered operation candidates.

Sensitivity: high for `ToolSpec`/manifest/event vocabulary; medium for the service class name `ToolRegistry` when only imported internally.

### ToolExecutor / call_tool / tool.call events

`ToolExecutor` is implementation class vocabulary, but the execution family is externally visible through `call_tool`, event kinds, result kinds/statuses, ledger replay, tests, and documentation. `call_tool` is the execution boundary in the decision schema. The executor appends durable events `tool.call.started`, `tool.call.completed`, and `tool.call.failed`.

Compatibility boundaries:

- decision kind `call_tool`;
- decision fields `tool_name`, `tool_arguments`;
- event kinds `tool.call.started`, `tool.call.completed`, `tool.call.failed`;
- event payload keys `tool`, `arguments`, `scope`, `output`, `error`, `phase`;
- `ToolCallResult` fields `kind`, `status`, `tool_name`, `message`, `output`, `error`, `policy`, `pending_action`, `payload`;
- policy-denied statuses `blocked`, `require_confirmation`, `require_approval`;
- pending-action bridge when policy does not allow immediate execution.

Sensitivity: high. The class name may be less public than event and decision vocabulary, but the responsibility family is inseparable from `call_tool` and durable `tool.call.*` events.

### Runtime

`Runtime` is a public developer-facing class and canonical orchestration path. Its name is less embedded in serialized records than tool/capability event vocabulary, but compatibility is still non-trivial because API and tests import it and docs assert it is canonical rather than `RuntimeLoop`.

Compatibility boundaries:

- developer imports from `seed_runtime.runtime`;
- `SeedAPI` construction with `Runtime`;
- event sequence from `handle_user_message()`;
- response kinds and payloads;
- docs/tests distinguishing canonical `Runtime` from deprecated or quarantined runtime-loop vocabulary.

Sensitivity: medium-high. It could be migrated more independently than event names, but not without developer API and architecture-doc compatibility.

### ExecutionStatus / execution vocabulary

`ExecutionStatus` is transient and explicitly non-authoritative; it does not own execution state and is not persisted in the event ledger. However, it is not purely internal because CLI status rendering, phase names, tests, and producer contracts depend on it.

Compatibility boundaries:

- developer protocol `ExecutionStatusConsumer.consume(status)`;
- status fields `phase`, `message`, `current`, `total`, `completed`;
- CLI-rendered messages and progress cadence behavior;
- producer phase strings such as `observation_collection`, `observation_normalization`, `observation_ingestion`, `observation_lifecycle`, `event_persistence`, and cache/projection-related phases;
- tests that record and assert statuses.

Sensitivity: medium. It can migrate more independently because it is not durable cluster truth, but phase names and CLI output remain compatibility surfaces.

### CapabilityCatalog / CapabilityRecommendation / capability vocabulary

Capability vocabulary is externally visible in `ToolNeed.capability`, `ToolSpec.capabilities`, capability catalog YAML, response payloads, diagnostic/CLI surfaces, and documentation. The most important boundary is semantic: catalog recommendations and registered operation candidates must not collapse into execution or verification.

Compatibility boundaries:

- model fields `capability` and `capabilities`;
- catalog YAML keys `capability`, `recommendations`, `provider`, `kind`, `backend_type`, `operation`;
- response payload `capability_resolution` with `known_capability`, `registered_operations`, `provider_recommendations`, and `handoff_candidates`;
- diagnostic/CLI capability surfaces;
- tests preserving that recommendations are metadata and registered operations come only from `ToolRegistry` capability lookup.

Sensitivity: high. Capability is a responsibility family connecting needs, registered operation discovery, provider/handoff metadata, diagnostics, and docs.

## Internal-only vocabulary

The following vocabulary appears migration-candidate or historical but is implementation-local or lower-contract when not emitted:

| Vocabulary | Why internal/local | Caveat |
|---|---|---|
| Local variables such as `tool`, `tools`, `tool_data`, `toolkit` inside registry/execution helpers | Names do not by themselves define public schema. | Same words become public when they are manifest keys, event payload keys, API keys, or response keys. |
| `ToolNeedService` class name | Service name is mostly internal routing/developer API rather than durable payload. | Behavior and produced events are public; docs/tests import the class. |
| `ToolRegistry` class name | Registry object is internal service/developer API. | Manifest schema, API output, validation behavior, and registered operation candidates are public. |
| `ToolExecutor` class name | Runtime dependency and developer import rather than serialized object. | `call_tool`, `ToolCallResult`, and `tool.call.*` events are public/durable. |
| Execution progress helper names such as `ProgressCadence`, `emit_status`, `emit_progress_if_due` | Helper functions are implementation support. | `ExecutionStatus` fields and emitted phase strings may be consumed. |
| Historical docs using broader `execution` and `capability` terms | Documentation-only unless reflected in code, tests, CLI, JSON, event ledger, or diagnostic inventory. | Contributor-facing docs are still a compatibility surface for architecture expectations. |

## Public and serialized vocabulary

The following must be treated as compatibility contracts before any migration:

- event kind strings: `tool_need.created`, `tool_need.status_changed`, `tool.registered`, `tool.call.started`, `tool.call.completed`, `tool.call.failed`, `model.decision.proposed`, plus related response/input events that carry decision payloads;
- decision kind strings and payload keys: `request_tool`, `call_tool`, `tool_need`, `tool_name`, `tool_arguments`;
- Pydantic serialized field names for `ToolNeed`, `ToolSpec`, `Toolkit`, `CapabilityRecommendation`, `CapabilityCatalogEntry`, `RuntimeResponse`, and `ExecutionStatus` where emitted;
- toolkit manifest keys and catalog YAML keys;
- API method output keys from `SeedAPI`;
- CLI flags and JSON keys for diagnostic, question, capability, events, and current-state surfaces;
- diagnostic inventory and diagnostic shape-audit records describing these surfaces;
- test fixtures and expected sequences that encode current vocabulary.

## Family dependencies

| Family | Members | Inseparable responsibility boundary | Can migrate independently? |
|---|---|---|---|
| Request/capability-gap family | `request_tool`, `ToolNeed`, `ToolNeedService`, `tool_need.*`, `CapabilityCatalog`, recommendations, `capability_resolution` | A request records a durable gap, resolves metadata/read-only candidates, and must not execute. | Mostly no. Names can be staged per layer only with compatibility preservation; semantics must migrate as one family. |
| Registered-operation family | `ToolSpec`, `Toolkit`, `ToolRegistry`, manifests, `tool.registered`, registered operation candidates | Manifests/register events/API expose executable operation metadata; registry lookup gates validation and execution. | Partially. Registry class name can move separately, but manifest/event/API vocabulary cannot. |
| Execution-call family | `call_tool`, `ToolExecutor`, `ToolExecutionPolicyService`, `ToolCallResult`, `tool.call.*`, pending action bridge | Valid tool calls are validated/policy-checked before durable call events and implementation dispatch. | Mostly no for public strings/events. Helper/service names can move later. |
| Runtime routing family | `Runtime`, `Decision`, `DecisionValidator`, `ToolIntentGuard`, routes to need/executor/state patch services | Runtime validates, guards, records decisions, and delegates without owning behavior. | Partially. Runtime class/docs can migrate separately from event vocabulary only if API imports and canonicality docs are preserved. |
| Transient status family | `ExecutionStatus`, `ExecutionStatusConsumer`, CLI status messages, phase names | Non-authoritative operator visibility for long-running work. | Yes, more independent than durable families, but public phase names/output/tests still need preservation. |
| Legacy execution-planning family | `ActionPlan`, `HandoffPlan`, `ExecutionProposal`, `ExecutionAuthorization` | Historical/quarantined side paths retained for projection compatibility and explicit tests. | No for historical ledger replay; yes for docs if quarantine meaning is preserved. |
| Diagnostic/question surface family | diagnostic inventory, diagnostic shape audit, question surface inventory, capability diagnostic surfaces | Operational surfaces must remain visible and audited. | No for any changed diagnostic/CLI output; repository instructions require inventory/spec/tests. |

## Compatibility relationships

Recovered dependency relationships:

```text
Decision(kind=request_tool)
  -> DecisionValidator validates tool_need shape
  -> Runtime routes request_tool
  -> ToolNeedService creates/deduplicates ToolNeed
  -> EventLedger appends tool_need.created
  -> StateProjector rehydrates ToolNeed
  -> Runtime returns tool_need + recommendations + capability_resolution
  -> API/CLI/tests/docs consume serialized vocabulary
```

```text
ToolNeed.capability
  -> CapabilityCatalog lookup
  -> ToolRegistry.list_tools_for_capability
  -> registered_operations response entries
  -> provider_recommendations / handoff_candidates metadata
  -> capability diagnostics/inventory/docs
```

```text
Toolkit manifest
  -> ToolRegistry.load_manifest/toolkit_from_manifest
  -> ToolSpec records
  -> DecisionInputComposer visible tools
  -> DecisionValidator validates call_tool input
  -> ToolExecutor requires ToolRegistry resolution
  -> tool.call.* ledger events
```

```text
Decision(kind=call_tool)
  -> DecisionValidator validates registered tool input
  -> ToolIntentGuard validates user intent
  -> Runtime routes call_tool only to ToolExecutor
  -> ToolExecutionPolicyService validates and evaluates policy
  -> ToolExecutor appends tool.call.started/completed/failed or creates pending action
  -> FactExtractionService observes completed tool result
```

```text
ExecutionStatus producer
  -> ExecutionStatusConsumer protocol
  -> RecordingExecutionStatusConsumer tests
  -> CliExecutionStatusConsumer stderr output
  -> no EventLedger mutation by status surface itself
```

## Migration readiness

| Area | Evidence recovered? | Safe to plan migration? | Notes |
|---|---:|---:|---|
| Durable event names and replay | Yes | Yes, planning only | Requires explicit ledger replay/backward-compatibility inventory before implementation. |
| Manifest/catalog schemas | Yes | Yes, planning only | Requires checking generated and core manifests plus catalog YAML. |
| Runtime decision schema | Yes | Yes, planning only | Must preserve model decision kinds and retry/error payload semantics. |
| API/CLI JSON output | Partial-to-strong | Yes, after surface inventory expansion | Broad CLI surface means a dedicated output-schema scrape or golden output investigation would reduce risk. |
| Diagnostic/question surfaces | Yes | Yes, with repository visibility contract | Any changed surface must update inventory/spec/tests. |
| Documentation | Strong but scattered | Yes, after doc-source map | Docs are numerous and include historical/quarantined terms; migration planning needs stale/current separation. |
| Provider integrations | Partial | Not fully | Catalog recommendation `operation`, `backend_type`, generated toolkit implementations, and handoff docs need targeted provider-boundary audit. |
| Tests | Strong | Yes | Tests encode many compatibility boundaries; a migration plan must classify which tests protect public contracts vs implementation names. |

## Compatibility hazards

1. **Ledger replay hazard.** Event kinds and payload keys are durable. Renaming `tool_need.*`, `tool.registered`, or `tool.call.*` without replay compatibility would orphan historical state.
2. **Manifest/schema hazard.** Toolkit manifests use `tools` and per-tool field names required by `toolkit_from_manifest()`. Generated toolkits use the same schema.
3. **Catalog semantic hazard.** `CapabilityRecommendation.operation` can look executable but is provider/handoff metadata unless it is also registered in `ToolRegistry`.
4. **JSON consumer hazard.** Runtime responses, API methods, diagnostic JSON, question surfaces, and event summaries expose current terms.
5. **CLI compatibility hazard.** Flags and human-readable output include tool/capability/execution terms; some consumers may parse text despite JSON alternatives.
6. **Diagnostic invisibility hazard.** Any operational surface change must update diagnostic inventory, shape-audit specs, and tests under the repository instructions.
7. **Documentation drift hazard.** Historical docs intentionally retain legacy vocabulary for archaeology/quarantine. A migration must not erase terms that document persisted or rejected behavior.
8. **Test false-signal hazard.** Some tests assert implementation class names; others assert public contracts. Migration planning must separate these before changing code.
9. **Provider integration hazard.** Generated toolkit packages and external-provider/handoff recommendation metadata may encode current vocabulary outside central runtime classes.
10. **Boundary-collapse hazard.** Renaming can accidentally imply that capability recommendation, registered operation, execution, verification, and provider handoff are one thing. Implementation evidence says they are separate responsibilities.

## Counterexamples recovered

| Apparent conclusion | Counterexample | Supported boundary |
|---|---|---|
| `ToolExecutor` looks like just an internal class name. | It owns durable `tool.call.*` event emission and is the target of the public `call_tool` decision route. | Class-name migration may be local, but execution-call vocabulary is public/durable. |
| `ToolRegistry` looks public because of its name. | The object itself is mostly internal service/developer API; the public contracts are manifests, serialized tools/toolkits, validation behavior, and registered operation candidates. | Service name may migrate independently from schema/event vocabulary. |
| `CapabilityRecommendation.operation` looks like a registered executable operation. | Capability resolution explicitly separates catalog handoff candidates from `ToolRegistry` registered operations. | It should intentionally retain or at least preserve its non-executable compatibility meaning during future migration. |
| `ExecutionStatus` looks like execution truth. | It is transient, renderer-independent, and non-authoritative; no ledger mutation is part of the status object. | It is a CLI/developer surface, not cluster truth. |
| Documentation vocabulary looks authoritative. | Repository instructions and docs require implementation evidence before promoting presentation vocabulary. | Documentation terms are compatibility evidence only when tied to code/tests/surfaces or canonical architecture docs. |
| `Runtime` looks like execution owner. | Runtime routes validated decisions to owner services; execution starts at `ToolExecutor`. | Runtime migration must preserve routing/delegation boundaries. |

## Supported conclusions

- The repository has recovered enough implementation information to identify compatibility boundaries for a future operational vocabulary migration.
- The current vocabulary family is externally visible in decision schemas, event kinds, payload keys, serialized models, API output, toolkit manifests, catalog YAML, CLI/diagnostic/question surfaces, tests, and docs.
- Purely internal vocabulary exists, but it is narrower than the class names suggest because many implementation classes produce public events or serialized records.
- `ToolNeed`/`request_tool`/capability resolution, registered operation metadata, and `call_tool`/execution events form tightly coupled responsibility families.
- `ExecutionStatus` can be considered a more independently migratable family because it is transient and non-authoritative, but its CLI/protocol/test exposure must still be preserved.
- Historical execution-planning vocabulary should not be blindly migrated away because it preserves ledger replay, quarantine, and compatibility meanings.
- A safe future migration should be planned per responsibility family with per-symbol compatibility inventories, not by repository-wide search-and-replace and not purely per isolated symbol.

## Unsupported conclusions

- This audit does not support any replacement names.
- This audit does not support beginning implementation immediately.
- This audit does not prove all external consumers are known.
- This audit does not prove CLI text output has a complete stable schema.
- This audit does not justify collapsing capability, provider recommendation, registered operation, execution, and verification vocabulary.
- This audit does not justify changing runtime behavior, event replay behavior, diagnostic recording boundaries, or provider integrations.
- This audit does not prove historical vocabulary should be removed; some should intentionally remain as compatibility or quarantine vocabulary.

## Recommended next investigation

Run a compatibility-contract inventory for the future migration plan. It should enumerate, with golden examples where possible:

1. every event kind and payload key related to tool/capability/execution/runtime vocabulary;
2. every CLI flag and JSON key that emits those records;
3. every toolkit manifest and capability catalog field;
4. every public `SeedAPI` method and serialized output;
5. every diagnostic inventory / shape-audit / question-surface entry containing the vocabulary;
6. every test that asserts public compatibility versus implementation-local names;
7. every documentation page that is canonical, historical, or quarantine-only.

Only after that inventory should a separate migration design decide sequencing, shims, deprecation, or implementation.
