# Eye Resolution and Evidence-Acquisition Topology Audit 001

## 1. Bounded questions

1. Is the Eye implemented as the owner of evidence acquisition, or better supported as a projection of independently owned observation, evidence, capability, operation, authorization, execution, admission, selection, and limit artifacts?
2. Does the current LLM/tooling problem expose missing owners, or mostly missing roads, typed handoffs, projections, and correlation between owners that already exist?
3. Can the repository represent the distinctions `tool availability != external grammar familiarity != demonstrated capability != authorization != successful observation != admitted evidence != fact promotion`?

## 2. Governing orientation tested

The operator orientation was treated as testimony, not repository fact:

- The Eye repeatedly observes something until it is better understood.
- The Eye only collects evidence.
- A tool is an external mechanism; a capability is evidence-backed current observability through that mechanism.
- Shell is a tool; Bash is external grammar and a demonstrable capability.
- The Eye may be a projection of Seed's evidence-acquisition resolution rather than the owner of observation, execution, capability, selection, admission, or truth.

## 3. Methodology

Read-only searches were run first, then narrowed into implementation and caller inspection. I inspected model definitions, observation source adapters, ingestion, evidence, state projection, fact support/conflict projection, capability candidates/inventory/verification, tool needs, registered operation registry, operation validation, policy authorization, execution, fact extraction from tool results, inquiry artifact visibility, CLI construction, and tests by targeted search.

No source, test, runtime, event-ledger, cluster, or existing documentation mutation was made. The only repository change is this audit artifact.

## 4. Inspected neighborhoods

Primary inspected files and seams:

- `seed_runtime/observations.py`
- `seed_runtime/observation_sources.py`
- `seed_runtime/observation_normalizers.py`
- `seed_runtime/evidence.py`
- `seed_runtime/fact_extraction.py`
- `seed_runtime/state.py`
- `seed_runtime/capability_inventory.py`
- `seed_runtime/capability_candidates.py`
- `seed_runtime/capability_verification.py`
- `seed_runtime/tool_needs.py`
- `seed_runtime/registry.py`
- `seed_runtime/tool_validation.py`
- `seed_runtime/tool_execution_policy.py`
- `seed_runtime/execution.py`
- `seed_runtime/inquiry_artifacts.py`
- `seed_runtime/policy.py`
- `seed_runtime/models.py`
- `scripts/seed_local.py`
- focused tests under `tests/` discovered by `rg`.

## 5. Evidence definitions found

### Observation

Repository implementation treats an observation as a canonical external or discovery-derived record with `id`, `source_type`, `observed_at`, `subject`, `predicate`, `value`, `confidence`, `metadata`, `dimensions`, and optional expiry. The class docstring says it can be converted into a Fact. Observation sources emit `Observation` objects, not raw facts.

### Evidence

Repository implementation treats evidence as a provenance-backed observed payload with `id`, `workspace_id`, `source`, `kind`, `observed_at`, `payload`, and `confidence`. Observation ingestion converts every observation into `Evidence(kind="observation")`; successful tool calls are converted into `Evidence(kind="tool.output")` without generic fact inference.

### Fact

Facts are separately projected repository claims. Observation ingestion usually emits `fact.observed` or `fact.inferred`, but fact promotion can be suppressed for at least one Prometheus metric. Tool-result extraction intentionally records evidence only and does not infer facts without explicit mapping.

## 6. Tool / grammar / operation / capability distinctions

| Concept | Current implementation support | Audit finding |
|---|---|---|
| Tool | `ToolSpec` records name, schemas, policy action, implementation, status, risk, capabilities; `ToolRegistry` loads manifests and indexes tools. | Tool is registered operation metadata, not proof the external mechanism works. |
| External grammar | No first-class grammar model found for Bash, PromQL, SQL, Git command language, etc. | Mostly absent; only implied by implementations, arguments, docs, and manifest examples. |
| Registered operation | `ToolRegistry`, `ToolValidationService`, and `ToolExecutionPolicyService` recognize existence, status, input shape, policy, and output shape. | Strongly implemented for named operations. |
| Capability candidate | `capability_candidates` derives candidates from observed package facts but explicitly says candidates are not capability proof. | Evidence-derived but not verified capability. |
| Verified capability | `capability_inventory` derives verification state from `capability_verified` facts and supporting evidence, while also listing requested and registered-contract capability names as unverified/provider/unverified universe members. | Mixed: capability universe is configuration/request/evidence mixed, but verified capability state is evidence/fact backed. |
| Authorization | `PolicyGate` and `ToolExecutionPolicyService` authorize a validated operation call based on policy/risk/approval. | Separate from capability and execution. |
| Observation | Observation sources and successful operation evidence are separate roads. | Tool execution output is evidence, not canonical `Observation`. |
| Evidence | Preserved in event ledger and projected state. | Can exist without fact promotion. |
| Projection | State projector, capability inventory, candidate/verification inspections, inquiry artifacts, and CLI diagnostics are read-only projections. | Many projections explicitly refuse selection/execution/authorization. |
| Resolution | No first-class `Resolution` model found. Fact supports, conflicts, freshness, capability verification, Unknown preservation, sufficiency/admission surfaces, and current samples partially express improved understanding. | Story-level concept with several partial implementation proxies. |

## 7. Responsibility inventory

| Stage | Producer | Artifact | Consumer | Trigger | Owned responsibility | Explicitly refused responsibility | Evidence required / provenance | Authority boundary | Read/mutate/event/projection | Candidate/select/authorize/execute/observe/admit/resolution/Unknown/LLM-free |
|---|---|---|---|---|---|---|---|---|---|---|
| Observation source collection | `ObservationSource.collect` implementations | `Observation` list | `ObservationCollectionService` | CLI/source call | Read external/local/source material and emit observations | Persistence, projection, fact admission | Source metadata, observed time, confidence | Source-specific read-only boundaries | Read external; no ledger until ingestion | Creates observations; no selection/auth/execution; LLM-free |
| Normalization | `ObservationNormalizationPipeline` | original + derived `Observation` list | ingestion | collection | Derive normalized observations | Mutating originals; persistence | derived metadata | state read only | Projection read; no ledger | Observes derivation, not authorization; LLM-free |
| Observation ingestion | `ObservationIngestor` | `observation.observed`, `evidence.observed`, optional `fact.observed/inferred` | event ledger/state projector | `ingest_many` | Preserve observation, evidence, optional fact provenance | External collection; policy; execution | observation id/source/causation/correlation/evidence id | ledger append | Mutates event ledger, projects state | Admits evidence to ledger; may promote fact; no selection/auth; LLM-free |
| Evidence projection | `StateProjector` | `State.evidence` | evidence graph, capability inventory, UI/CLI | replay events | Project preserved evidence | Decide truth or run tools | event payload ids/timestamps | append-only event source | Read projection from ledger | Preserves Unknown via absence; LLM-free |
| Fact support/conflict | `state._project_fact_supports`, `_project_fact_conflicts` | `FactSupport`, `FactConflict` | state views, capability inventory | projection finalization | Aggregate repeated supports, current measurement samples, expose conflicts | Create new facts or evidence | supporting fact ids, source types, observed/latest time | projection only | Read-only derived state | Improves current-belief representation; not named resolution; LLM-free |
| Capability candidates | `build_capability_candidates` | `CapabilityCandidateInspection` | capability verification/readiness/CLI | read projected package facts | Preserve evidence-derived possible capabilities | Capability proof, permission, selection, execution | fact/evidence ids and summaries | read-only inspection | No mutation/event | Creates candidates only; LLM-free |
| Capability inventory | `build_capability_inventory` | `CapabilityInventoryEntry` | CLI, verification | read projected state | Present verification state from `capability_verified` facts and support | Admission, promotion, execution authority, policy | fact support/evidence summaries/freshness | read-only projection | No mutation/event | Does not select/auth/execute; exposes stale/unknown/unverified; LLM-free |
| Tool need | `ToolNeedService.create_from_decision` | `ToolNeed` event/state | request-tool flow, capability resolution | `Decision.kind=request_tool` | Create missing capability request from Decision grammar | Inquiry evidence-need derivation; execution | decision reason/tool_need payload | event ledger append | Mutates ledger | Creates gap artifact; LLM-compressed origin; LLM-free service after decision |
| Capability resolution for ToolNeed | `ToolNeedService.resolve_capability` | dict with known capability, registered ops, provider/handoff | request-tool response | existing ToolNeed | Read-only join catalog/registry/providers | Execute, authorize, pending action, mutation | registry/catalog metadata | advisory | Read-only | Provides candidates, not selection; LLM-free |
| Registered operation registry | `ToolRegistry` | `ToolSpec`, `Toolkit` | validation/execution/tool needs | manifest loading/event projection | Know operation contracts | Prove capability; authorize; execute | manifest fields | registry only | In-memory or projected state | Creates operation universe; no selection beyond lookup; LLM-free |
| Operation selection | `ToolValidationService.select_operation` | `OperationSelectionResult` | validation/execution | caller names operation | Resolve already-selected operation by name | Capability selection or provider ranking | registry/state lookup | selected-name boundary | Read-only | Selects named operation only; no capability selector; LLM-free |
| Registered operation validation | `ToolExecutionPolicyService` | `RegisteredOperationValidationResult` | policy evaluation | execute request | Existence/status/input validation | Policy authorization and execution | ToolSpec/schema errors | contract boundary | Read-only | No auth/execute; LLM-free |
| Policy authorization | `PolicyGate` / `ToolExecutionPolicyService` | `PolicyDecision` | executor/pending actions | validated call | Decide allow/block/confirmation/approval | Create capability; select inquiry; execute | risk, approval state, scope | policy boundary | Read-only unless pending action by caller | Authorizes only already-specified op; LLM-free |
| Execution | `ToolExecutor` | `ToolCallResult`, `tool.call.*` events | fact extraction, caller, state | allowed call | Invoke registered callable and validate output | Tool discovery, capability proof, truth | call/completed/failed events with causation/correlation | registered implementation boundary | Mutates event ledger | Executes; no generic observation artifact; LLM-free |
| Tool result evidence | `FactExtractionService` | `evidence.observed` kind `tool.output` | state/evidence consumers | completed tool call | Preserve tool output as evidence | Generic fact inference | completed event id/correlation | evidence boundary | Mutates ledger | Evidence admission only; LLM-free |
| Inquiry artifacts | `build_inquiry_artifacts` | visibility classifications | CLI/operator | diagnostic call | Read-only repository-visible inquiry artifact visibility | Inquiry graph, planning, pressure transformation | prose evidence strings | diagnostic projection | Read-only no ledger | Preserves unknown as visible artifact; LLM-free |

## 8. Producer / artifact / consumer table

| Producer | Artifact | Consumer |
|---|---|---|
| Local host, Prometheus, JSON, Ansible, repository source, Seed runtime sources | `Observation` | `ObservationCollectionService` and `ObservationIngestor` |
| `ObservationIngestor` | `observation.observed` event | `StateProjector.State.observations` |
| `ObservationIngestor` | `evidence.observed` event with `kind=observation` | `StateProjector.State.evidence`, evidence graph, fact evidence views |
| `ObservationIngestor` | `fact.observed` / `fact.inferred` event | `StateProjector.State.facts`, fact support/conflict projection |
| `ToolRegistry` | `ToolSpec` | validation, policy, execution, tool need resolution, capability inventory universe |
| `ToolValidationService` | `OperationSelectionResult`, `ToolValidationResult` | execution policy and tests |
| `ToolExecutionPolicyService` / `PolicyGate` | `ToolExecutionPolicyResult`, `PolicyDecision` | `ToolExecutor` |
| `ToolExecutor` | `tool.call.started/completed/failed`, `ToolCallResult` | `FactExtractionService`, caller, state replay history |
| `FactExtractionService` | `evidence.observed` kind `tool.output` | `StateProjector.State.evidence` |
| `build_capability_candidates` | `CapabilityCandidateInspection` | verification/readiness/CLI |
| `build_capability_inventory` | `CapabilityInventoryEntry` | CLI, verification, readiness |
| `ToolNeedService` | `ToolNeed` | request-tool flow and projected state |
| `state._project_fact_supports` | `FactSupport` | current belief, capability inventory |
| `state._project_fact_conflicts` | `FactConflict` | state consumers, diagnostics |

## 9. Observation-source topology

Implemented topology:

```text
external/local/source subject
→ source adapter implementing ObservationSource.collect()
→ source-specific raw read/subprocess/http/filesystem data inside adapter
→ adapter emits Observation objects
→ ObservationCollectionService normalizes and validates Observation instances
→ ObservationNormalizationPipeline may derive additional Observation objects
→ ObservationIngestor records observation/evidence/fact events
```

Where raw result differs from observation: raw files, HTTP responses, subprocess outputs, manifests, or in-memory data are adapter-private. The public handoff is `Observation`, not a generic raw result envelope.

Status: implemented for several sources; raw result preservation is source-specific and usually appears only as metadata/evidence snippets, not a universal raw-result artifact.

## 10. Evidence topology

Implemented topology:

```text
Observation
→ Evidence(kind="observation", source="observation:<source_type>")
→ evidence.observed event
→ State.evidence projection
→ evidence graph / capability inventory / fact evidence views / diagnostics
```

Tool-result topology:

```text
tool.call.completed
→ Evidence(kind="tool.output", source="tool:<tool_name>")
→ evidence.observed event
→ State.evidence projection
```

Observation and evidence differ exactly at the ingestion boundary: observation is the attributed subject/predicate/value object; evidence is the preserved provenance payload that can support facts or later consumers. Evidence can also originate from successful tool results without becoming a canonical `Observation`.

## 11. Capability-recognition topology

Current recognition states:

| State | Implementation-backed? | Meaning |
|---|---:|---|
| configured | Yes | `ToolSpec.capabilities` from manifest/config; not proof. |
| discovered | Yes | package facts can yield `CapabilityCandidate`; not proof. |
| registered | Yes | `ToolSpec` exists/status registered; operation contract exists. |
| reachable | Partial | `verification_evidence` can inspect local PATH without invocation for some candidates; not universal. |
| authorized | Yes | policy authorization of a validated operation call. Not capability. |
| verified | Yes | `capability_verified` fact support in projected State. |
| successful | Partial | successful operation yields `tool.call.completed` and `tool.output` evidence; no generic link to capability verification unless explicit fact exists. |
| current | Partial | capability inventory exposes age/stale from fact expiry semantics; no universal freshness SLA. |
| sufficient | Partial/fragmented | sufficiency/admission vocabulary exists in some diagnostics and docs, but no general capability-sufficient-for-inquiry artifact found. |

Capability recognition is mixed. The universe of visible capability names is configuration/request/evidence mixed; verified capability state is evidence/fact-backed.

## 12. Registered-operation topology

Implemented topology:

```text
toolkit manifest / tool.registered event / projected ToolSpec
→ ToolRegistry / State.tools
→ ToolSpec operation contract (schemas, policy_action, risk, implementation, status)
→ ToolValidationService.select_operation(named operation)
→ existence/status/input validation
→ ToolExecutionPolicyService + PolicyGate authorization
→ ToolExecutor loads implementation and executes
→ output schema validation
→ tool.call.completed or failed/blocked/pending result
```

This road begins with an operation already named by the caller. It is not a capability-to-operation selector except through the advisory ToolNeed resolution surface.

## 13. Capability-to-operation road

Partial road exists:

```text
ToolNeed.capability
→ ToolNeedService.resolve_capability
→ ToolRegistry.list_tools_for_capability
→ registered_operations advisory list
```

Missing road:

```text
inquiry-specific evidence need
→ required observation capability
→ available capability projection
→ eligible registered operations
→ bounded operation selection
```

`OperationSelectionResult` resolves a named operation only. It explicitly refuses capability recommendation, handoff ranking, or provider choice.

## 14. Execution-to-evidence road

Implemented road:

```text
allowed registered operation
→ ToolExecutor._realize_registered_operation
→ output dict validated against ToolSpec.output_schema
→ tool.call.completed event
→ FactExtractionService.observe_tool_result
→ evidence.observed(kind="tool.output")
→ State.evidence
```

Boundary classification:

- Raw output: yes, returned and recorded in `tool.call.completed`.
- Observation: no generic canonical `Observation` is created for tool output.
- Evidence: yes, `tool.output` evidence is appended.
- Fact: no generic fact inference; intentionally absent unless future explicit mapping exists.
- Capability evidence: not automatically; only if separate facts/evidence mappings establish it.
- Inquiry-specific evidence: not generally; correlation IDs may thread execution/evidence but no typed inquiry evidence-need/resumption object was found.

## 15. Repeated-observation topology

Implemented partial topology:

```text
same subject/predicate observed repeatedly
→ multiple facts/evidence in ledger
→ StateProjector groups FactSupport by subject/predicate/dimensions/value
→ durable facts aggregate support confidence and latest_observed_at
→ measurement predicates select current sample
→ conflicting durable values become FactConflict
```

This supports comparison in the sense of aggregate support, freshness/latest observation, current measurement sample, and contradiction visibility. It does not implement a general repeated-observation loop, evidence pressure, stopping rule, or explicit `Resolution` artifact.

## 16. Resolution topology

Current implementation-backed proxies for increased understanding:

- More fact support and higher aggregated support confidence for durable facts.
- `latest_observed_at` and expiry/stale behavior.
- Current sample selection for measurements.
- Conflict visibility via `FactConflict`.
- Verified/stale/unverified/provider-reported/unknown capability inventory states.
- Unknown preservation in entity type and inquiry artifact visibility.
- Admission/sufficiency/warrant vocabulary in some diagnostics/tests/docs.

Finding: `resolution` is not a first-class implementation grammar. A projection that claims resolution would currently need to expose proxy fields such as supports, conflicts, staleness, verified capability, unanswered needs, and Unknowns rather than inventing a new resolution score.

## 17. Eye ownership topology

No implementation-backed `Eye` owner was found. No one owner currently owns evidence-need formation, capability discovery, operation selection, authorization, execution, observation, evidence admission, and inquiry resumption.

If Model A were created as a single owner, it would compress existing boundaries:

- observation source ownership
- evidence preservation
- fact promotion/admission
- capability candidate and verification presentation
- registered operation registry
- named-operation validation
- policy authorization
- execution
- pending action approval/resumption
- state projection

Therefore Model A is contradicted by the current separated implementation.

## 18. Eye projection topology

Best-supported Eye projection fields and existing suppliers:

| Proposed projection field | Existing owner/artifact | Honest status |
|---|---|---|
| What has been observed | `State.observations`, `State.facts`, `State.evidence` | Projectable now. |
| What evidence supports claims | `Evidence`, `Fact.evidence_ids`, evidence graph | Projectable now. |
| Current fact support/freshness/conflicts | `FactSupport`, `FactConflict` | Projectable now. |
| Capability candidates | `CapabilityCandidateInspection` | Projectable now, with boundary notes. |
| Verified/stale/unverified capabilities | `CapabilityInventoryEntry` | Projectable now. |
| Registered operations by capability | `ToolRegistry.list_tools_for_capability`, `ToolNeedService.resolve_capability` | Projectable as advisory candidates, not selection. |
| Authorized operation calls | `PolicyDecision`, `ToolExecutionPolicyResult` | Projectable only per already-specified call. |
| Execution outcomes | `ToolCallResult`, `tool.call.*` events | Projectable now. |
| Tool-output evidence | `FactExtractionService` evidence events | Projectable now. |
| Unresolved tool/capability gaps | `ToolNeed` | Projectable, but origin is Decision/request-tool compressed. |
| Unknowns | typed unknowns/inquiry artifacts/entity type unknown | Partially projectable. |
| Evidence needs | no general artifact found | Cannot project honestly except via ToolNeed or diagnostics. |
| Inquiry resumption after evidence | no general artifact found | Cannot project honestly. |
| Resolution change | proxy only | Must not invent first-class resolution. |

Projection discipline: such an Eye projection must not create candidates beyond consuming existing candidate artifacts, must not select operations, must not authorize calls, must not mutate the ledger, must preserve absence versus Unknown, and must preserve source attribution/freshness.

## 19. LLM compression topology

Old compressed path:

```text
Context
→ Decision
→ request_tool / call_tool / answer / action_plan / handoff / patch
```

Responsibility mapping:

| Compressed responsibility | Existing Seed-native owner | Gap |
|---|---|---|
| Current state/context | `StateProjector`, state views, context views | Partially recovered. |
| General Decision | bounded typed decisions/services | General Decision remains compressed LLM grammar. |
| Tool need creation | `ToolNeedService.create_from_decision` | Origin still from `Decision.tool_need`, not non-LLM evidence need. |
| Operation selection | `ToolValidationService.select_operation` | Only named operation lookup. |
| Policy authorization | `PolicyGate`, `ToolExecutionPolicyService` | Recovered. |
| Execution | `ToolExecutor` | Recovered. |
| Evidence preservation from tool output | `FactExtractionService` | Recovered as evidence-only. |
| Admission/fact extraction | `ObservationIngestor` for observations; no generic tool-output mapping | Partial. |
| Inquiry resumption | pending-action resume exists for approved tool call; inquiry resumption absent | Missing typed road. |

## 20. Bash dungeon competency probe

Can repository represent the probe artifacts?

| Probe artifact | Current support |
|---|---|
| required competency | Partial via `ToolNeed.capability` or diagnostic capability needs; not grammar-specific job requirement. |
| demonstrated competency | Partial via `capability_verified` facts; no Bash grammar competency model. |
| unsupported competency | Partial via unverified/stale inventory and ToolNeed; not job-specific. |
| competency evidence | Partial via Evidence/FactSupport; no competency-specific schema. |
| competency freshness | Partial via fact expiry/age. |
| safe competency environment | Absent as first-class environment. Policy/risk exists for operations. |
| job-required capability | Absent as typed artifact outside compressed ToolNeed/diagnostic need. |
| sufficient-for-current-job | Absent as general implementation artifact. |
| lawful stop | Absent as first-class acquisition stopping rule. |

The architecture can distinguish tool availability, candidate evidence, verified capability, authorization, successful execution, evidence, and fact promotion. It cannot yet honestly model Bash grammar familiarity or job-specific competency sufficiency without new typed artifacts/roads.

## 21. Existing owners

- Observation sources own source-specific observation emission.
- Observation collection service owns collection/normalization/ingestion handoff.
- Observation ingestor owns observation-to-evidence and optional fact-event generation.
- State projector owns read-model projection from append-only events.
- Fact support/conflict projectors own current-support/conflict derivation.
- Capability candidate inspection owns evidence-derived possible capability preservation.
- Capability inventory owns read-only capability verification presentation from facts/evidence plus registered/requested universe.
- ToolNeed service owns capability-gap creation from request-tool decisions and read-only resolution metadata.
- Tool registry owns registered operation contracts.
- Tool validation owns named-operation selection and schema/status validation.
- Policy gate/execution policy service owns authorization for already specified validated calls.
- Tool executor owns registered operation execution and event recording.
- Fact extraction owns preserving successful tool output as evidence.
- Pending actions own approval-gated tool-call resumption, not inquiry resumption.

## 22. Missing owners

Missing or not implementation-backed as general owners:

- Evidence-need formation from bounded inquiry.
- Required observation capability derivation from evidence pressure.
- Capability-to-operation bounded selector.
- Inquiry-specific evidence correlation object.
- Inquiry resumption after evidence arrives.
- External grammar competency owner.
- Safe competency environment owner.
- Sufficient-for-current-job/lawful-stop owner.
- First-class resolution owner.

## 23. Existing roads

- Source adapter → Observation → Evidence → optional Fact → State projection.
- Tool manifest/registration → ToolSpec → named operation validation → policy authorization → execution → output evidence.
- Package observed facts → capability candidates.
- `capability_verified` facts → capability inventory verification state.
- ToolNeed capability → registered operation advisory candidates.
- Multiple facts → supports/conflicts/current samples.
- Pending action approval → resumed approved tool call.

## 24. Missing roads

- Bounded inquiry → evidence need.
- Evidence need → required observation capability.
- Required capability → verified available capability projection.
- Capability → selected eligible operation.
- Execution result → canonical observation when appropriate.
- Execution/evidence → inquiry-specific evidence admission.
- Evidence arrival → inquiry resumption.
- Repeated observation → explicit resolution delta/lawful stop.
- Capability failures → capability evidence/fact update without manual mapping.

## 25. Projection opportunities

A read-only Eye projection could compose existing state and projections to expose:

- observed subjects/predicates and source provenance;
- preserved evidence and support chains;
- fact supports/conflicts/staleness;
- capability candidates and their boundaries;
- verified/stale/unverified capabilities;
- registered operations associated with requested capabilities;
- authorization/execution outcomes already recorded;
- current Unknowns and absent roads.

It must not rank or select, must not authorize, must not mutate, must not convert candidates into capability truth, and must not present absence as Unknown unless an existing owner says Unknown.

## 26. Correlation gaps

The event model preserves `causation_id` and `correlation_id` through observation ingestion and tool execution/evidence extraction. However, no typed chain was found for:

```text
inquiry → evidence need → required capability → selected operation → execution → evidence → resumed inquiry
```

Correlation IDs can carry lineage but do not define responsibility, sufficiency, or resumption semantics.

## 27. Strongest counterevidence

- Projection alone may be insufficient because the desired loop includes unresolved evidence pressure, required observation capability, eligible operation selection, and lawful stop; these need typed owners or a bounded coordinator, not only a display projection.
- `ToolNeedService.resolve_capability` already maps a requested capability to registered operation candidates, so a capability-to-operation road partially exists.
- `ToolExecutor.resume_approved_tool_call` shows a resumption pattern after approval; this is not inquiry resumption, but it proves the repository has resumption mechanics for one operation path.
- Fact support aggregation and conflict projection mean repeated observations already improve current-belief representation in limited ways, contradicting a claim that repetition has no implementation effect.
- Capability inventory includes registered ToolSpec capabilities in the displayed universe, so capability is not purely evidence-backed at the presentation-universe level.
- Existing separation may still require a bounded coordinator for the acquisition loop because no current owner triggers the next observation when evidence remains insufficient.
- The Bash dungeon example would need new architecture for external grammar competency, safe environment, job-specific sufficiency, and lawful stop; existing architecture only supplies generic primitives.

## 28. Preserved Unknowns

- Whether future repository intent names “Eye” elsewhere outside inspected implementation/doc testimony.
- Whether capability verification facts are produced by an intended but currently external/manual process.
- Whether LLM agents outside repository code already maintain inquiry evidence-needs and resumption state.
- Whether some diagnostics use “sufficiency,” “warrant,” or “admission” as stable contracts rather than presentation vocabulary in all cases.
- Whether operation failures should become capability evidence automatically.
- Whether successful tool-output evidence should ever become canonical Observation rather than evidence-only.
- Whether resolution should be a first-class artifact or remain a projection of support/conflict/freshness/Unknown/sufficiency.

## 29. Supported conclusions

1. The repository currently treats `Observation` as canonical subject/predicate/value records from source adapters and CLI/dev observation input.
2. The repository currently treats `Evidence` as preserved provenance payloads supporting facts or later consumers.
3. Evidence can exist without fact promotion; tool output evidence intentionally does not infer facts generically.
4. Observation owners include observation sources, normalizers, and ingestion services.
5. Evidence preservation owners include `ObservationIngestor` and `FactExtractionService`.
6. Repeated observations are compared/aggregated only through fact support/current measurement/conflict projection, not an Eye loop.
7. Repeated observation improves explicit proxy artifacts (`FactSupport`, current sample, conflicts), but no explicit `Resolution` artifact.
8. No implementation-backed `Eye` owner was found.
9. No one owner possesses the full Eye story responsibilities.
10. Creating such an owner would compress existing constitutional boundaries.
11. The Eye is better supported as a projection, with possible future bounded coordination for missing loop triggers.
12. Existing artifacts to project include observations, evidence, facts/supports/conflicts, capability candidates/inventory, ToolNeeds, ToolSpecs, policy decisions, execution events/results, pending actions, Unknowns, and diagnostic/inquiry visibility.
13. An Eye projection would mostly compose existing artifacts but cannot honestly project evidence needs, capability selection, inquiry resumption, external grammar competency, or first-class resolution without new owners/roads.
14. Tool recognition is registry/ToolSpec/manifest based.
15. Registered operation recognition is ToolSpec existence/status/schema/implementation binding.
16. Capability recognition is mixed: evidence-backed for verification, configuration/request-backed for universe membership, package-evidence-backed for candidates.
17. Capability can become stale via expired verification facts; unknown values are represented when verification fact values are unrecognized.
18. The repository distinguishes tool presence from capability candidates/proof, demonstrated capability from authorization, authorization from execution, execution from evidence, and evidence from fact promotion.
19. Capability failures can become evidence only if represented by events/facts/evidence; no automatic generic failure-to-capability-evidence road was found.
20. No bounded selector from evidence need to observation capability was found.
21. No general bounded selector from capability to registered operation was found beyond ToolNeed advisory lookup.
22. `OperationSelectionResult` performs named-operation resolution only.
23. `ToolNeed` is a Seed-native event/state artifact, but its producer remains compressed `Decision.tool_need` grammar rather than non-LLM inquiry evidence pressure.
24. No implementation-backed general evidence-need artifact or inquiry resumption artifact was found.
25. Improved understanding currently means better projected supports, freshness, current samples, conflict visibility, capability verification state, and preserved Unknowns, not a named resolution object.
26. The old general `Decision` compresses responsibilities that now have independent owners, while evidence-need derivation, capability selection, and inquiry resumption remain genuinely absent.

## 30. Unsupported conclusions

- Unsupported: The Eye already exists as an implementation-backed owner.
- Unsupported: A single owner must own the complete acquisition loop.
- Unsupported: Capability is purely evidence-backed in all displayed forms.
- Unsupported: Tool presence alone proves capability.
- Unsupported: Operation selection currently selects from capability needs.
- Unsupported: Repeated observation currently produces a first-class resolution delta.
- Unsupported: ToolNeed is already produced by non-LLM inquiry-specific evidence need.
- Unsupported: A Bash dungeon can be built entirely from existing artifacts without new typed responsibilities.

## 31. Primary classification

B. The Eye is best supported as a projection of independently owned evidence-acquisition responsibilities.

## 32. Secondary gap classification

5. Mixed or insufficient evidence.

Rationale: existing owners are substantial, but the missing pieces are mixed across roads, typed handoffs, projection/correlation, and a few true missing owners such as evidence need, capability selection, inquiry resumption, grammar competency, and lawful stop. It is not primarily missing owners only, and not primarily vocabulary only.

## 33. Exact next recommended slice

One bounded implementation slice is warranted later, but not during this audit:

Responsibility boundary: **typed evidence-need handoff**.

Exact bounded question: **Can Seed represent, read-only and without selecting or executing, that a bounded inquiry has an unresolved evidence need requiring a named observation capability, with provenance to the inquiry and without creating ToolNeed or operation selection?**

This is the smallest slice because it tests the missing road before adding capability selection, Eye projection, execution wiring, or inquiry resumption.

## 34. Implementation-warrant decision

One bounded implementation slice is warranted.

No implementation was performed in this task.

## 35. Files changed

- Added `eye_resolution_evidence_acquisition_topology_audit_001.md`.

No implementation files, tests, or existing documentation were changed.

## 36. Probes/tests executed

Read-only probes executed:

```bash
rg -n "Observation|Evidence|Capability|ToolNeed|ToolSpec|OperationSelection|PolicyDecision|Execution|Unknown" seed_runtime scripts tests
rg -n "observe|observed|evidence|capability|registered operation|select_operation|authorize|execute|fact" seed_runtime tests
rg -n "Eye|resolution|repeated observation|competency|sufficiency|warrant|admission|resum" . -g '*.py' -g '*.md'
find seed_runtime -maxdepth 1 -type f | sort
sed -n focused inspections of observation, evidence, state, capability, registry, validation, policy, execution, inquiry, CLI, and model files
git diff --stat
git diff --numstat
git status --short
```

No tests were run because this was review-only and made no implementation changes. No event-ledger or cluster mutation probes were run.

## 37. Confidence statement

Confidence is moderate-high for the classification because the implementation contains explicit boundary comments separating candidates, verification, policy, execution, evidence, and fact promotion. Confidence is lower for exhaustive absence claims because the repository has many diagnostic and documentation surfaces; the audit preserved Unknowns where a future or less direct surface may provide additional testimony.
