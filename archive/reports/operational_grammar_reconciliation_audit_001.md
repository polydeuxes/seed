# Operational Grammar Reconciliation Audit 001

## 1. Bounded question

Which legitimate Seed-native operational responsibilities are currently trapped inside the LLM-era `tool` district, and what canonical owners recover those responsibilities without preserving LLM tool grammar inside Seed?

## 2. Constitutional premise

This audit treats an LLM as an external source that may provide attributed artifacts. LLM output is not a Seed-native request; LLM tool calls are not Seed-native invocation requests; LLM function schemas are not Seed-native invocation grammar; LLM tool choice is not operational-realization selection; LLM response is not validation, authorization, or constitutional operation.

## 3. Historical concern

The repository still contains artifacts matching the sequence `LLM emits decision -> selects named tool -> supplies tool arguments -> runtime validates -> policy permits -> runtime executes`. Several slices have already separated recommendation, validation, policy, and execution ownership; that improves isolation but does not by itself prove constitutional placement.

## 4. Methodology

Read-only implementation inspection used focused `rg` probes, direct body inspection, and focused baseline tests. Classification was based on construction inputs, output shapes, consumers, ledger mutation, State interaction, comments, and tests, not names alone.

## 5. Inspected owners

Inspected: `ToolNeed`, `request_tool`, `CapabilityCatalog`, `CapabilityInventory`, `SingleCapabilityStateProjection`, `CapabilityRecommendation`, `RecommendationRanker`, `Toolkit`, `ToolSpec`, `ToolRegistry`, `call_tool`, operation selection, schema validation, `ToolExecutionPolicyService`, `PendingAction`, `ActionPlan`, `ExecutionProposal`, provider fields, toolkit IDs, operation names, implementation references, runtime/model decision boundaries, and tests.

## 6. Current implemented topology

Current core runtime free-text topology is now:

```text
user input
-> input.user_message event
-> runtime.decision_authority_unsupported event
-> unsupported response
```

This is established by `Runtime.handle_user_message`, which refuses to route model-produced `Decision` objects as authority.

Compatibility and service-level topology still exists:

```text
Decision(kind=request_tool)
-> DecisionValidator validates tool_need payload
-> ToolNeedService creates ToolNeed and optional capability-resolution payload
-> CapabilityCatalog recommendations and ToolRegistry capability lookup are returned as metadata
```

```text
Decision(kind=call_tool) or direct ToolExecutor.execute
-> ToolValidationService selects registered operation by name
-> input schema/status validation
-> ToolExecutionPolicyService policy authorization
-> ToolExecutor imports implementation and executes
-> tool.call.* events and optional fact extraction
```

## 7. External-grammar ingress analysis

| Producer | External artifact | Translation or missing translation | First Seed-native owner | First unlawful ownership transfer | Downstream authority reached |
|---|---|---|---|---|---|
| `ModelClient` | JSON `Decision` shapes with `call_tool`, `request_tool`, `tool_name`, `tool_arguments` | Shape parsing only; vocabulary remains model-visible | `DecisionValidator` if invoked outside current Runtime | Historical: `Runtime._route` path, now excised in core free-text | Existing service tests still exercise validation/execution paths directly |
| `IntentDecisionProducer` | intent classification converted into `Decision` | Local builder translates intent to `Decision`, but still emits tool grammar | compatibility producer | Not active in `Runtime.handle_user_message` | none through current Runtime |
| CLI/tests/manual code | constructed `ToolNeed`, `ToolSpec`, `ActionPlan`, `ExecutionProposal` | no external LLM necessary | service-specific models | none if used as service artifacts; hazardous if treated as canonical | validation, policy, execution, reports depending on entry |

Core Runtime blocks model-shaped Decisions, but `DecisionValidator`, `ToolNeedService`, and `ToolExecutor` still preserve an old grammar for direct callers and tests. Thus LLM grammar cannot move through free-text runtime, but remains structurally embedded in service APIs.

## 8. Capability reconciliation

The repository strongly supports: capability is projected reachability/status/testimony composition, not an object Seed simply possesses and not metadata owned by an invocation definition.

| Meaning | Classification | Evidence/owner |
|---|---|---|
| requested capability | demand | `ToolNeed.capability` records a requested gap |
| catalog-known capability | static metadata/testimony | `CapabilityCatalogEntry` and `CapabilityRecommendation` |
| provider-reported capability | verification/status conclusion from facts | `CapabilityInventoryEntry.state == provider_reported` |
| registered-operation capability label | contract claim / affordance metadata | `ToolSpec.capabilities`; inventory comments say labels do not verify reachability |
| verified capability | verification conclusion | projected `capability_verified` facts and `CapabilityInventoryEntry` |
| stale capability | verification freshness conclusion | expired fact support in inventory |
| unverified capability | absence of verification fact | inventory entry reason |
| reachable capability | not fully owned by tool district | closest owner is single-capability projection, but it composes evidence and still says no selection/authorization |
| policy-permitted capability | authorization conclusion for one validated call, not capability | `PolicyGate`/`ToolExecutionPolicyService` |

Current compression: `CapabilityInventory` widens its universe from requested capabilities, verification facts, and `ToolSpec.capabilities`, but separates source classes. Registration is explicitly not reachability. Recommendation is explicitly advisory and unselected.

Lawful reachability projection is not the registry. The closest current lawful owner is the immutable single-capability projection plus capability inventory, but even that is a read-only composition rather than a canonical reachability authority.

## 9. Operational-realization reconciliation

Smallest stable unit between requested capability and concrete invocation request is not necessarily `provider + toolkit + tool + operation`. Evidence from examination roads already uses fields like `contract_id`, `capability_id`, `work_kind`, accepted and produced representations, availability, provenance, and unknowns. The stable unit is:

```text
realization identity
requested transformation/capability reference
mechanism reference
invocation-contract reference
accepted representation
produced representation
availability/dependency evidence
authority requirements
constraint compatibility
provenance
unknowns
```

`provider`, `tool`, `toolkit`, executable, adapter, service, backend, internal producer, external source, and human-supervised procedure are implementation-local or typed references, not required constitutional nouns.

## 10. Invocation-grammar reconciliation

A legitimate responsibility exists: preserve bounded grammar by which one realization is requested and by which its result is represented. Current `ToolSpec.input_schema`, `ToolSpec.output_schema`, `name`, examples, and policy action partially own this, but compressed with implementation binding, risk, visibility, status, package namespace, and capability labels. Current tool schemas are recoverable as invocation-contract evidence without retaining tool ontology.

## 11. Provider reconciliation

`provider` is overloaded, not stable constitutional vocabulary.

| Meaning | Classification |
|---|---|
| recommendation provider | advisory testimony source/name in catalog and ranker |
| runtime provider | model/API provider or decision provider in trace/journal contexts |
| execution provider | ActionPlan provider; currently legacy/experimental |
| observation provider | observation source type/provenance |
| external artifact provider | external source provenance |
| backend provider | backend/handoff implementation reference |
| implementation source | sometimes inferred from `implementation` or toolkit ID by ranker |

Do not unify these solely by field name.

## 12. Registry reconciliation

A registry can survive as implementation inventory if stripped of constitutional privilege. Smallest legitimate responsibility: preserve known realization/invocation-contract testimony and implementation bindings, status, package provenance, and schema references for deterministic lookup. Illegitimate responsibilities: defining available cognition, granting capability by registration, letting external grammar select movement directly, or acting as constitutional action universe.

## 13. Field-level responsibility extraction

### `ToolSpec`

| Current field | Current owner | Actual responsibility | Proposed Seed-native owner | Action |
|---|---|---|---|---|
| `name` | `ToolSpec`/`ToolRegistry` | invocation-contract identity / exact operation key | invocation contract reference | keep then translate |
| `toolkit_id` | `ToolSpec`/`Toolkit` | package namespace/provenance/family | package provenance or realization family reference | move/split |
| `summary` | `ToolSpec` | human description testimony | realization/contract testimony | keep |
| `input_schema` | `ToolSpec` | accepted invocation representation | invocation contract | move |
| `output_schema` | `ToolSpec` | result representation grammar | result contract | move |
| `implementation` | `ToolSpec` | executor binding/import path | implementation binding | split |
| `status` | `ToolSpec` | registration availability testimony | realization inventory status | move |
| `visibility` | `ToolSpec` | model-visible menu exposure | compatibility/model adapter boundary | translate/remove canonical standing |
| `risk_class` | `ToolSpec` | policy input | authority requirements/risk testimony | move |
| `capabilities` | `ToolSpec` | claimed transformations/affordance labels | realization testimony, not capability owner | move to testimony input |
| `policy_action` | `ToolSpec` | policy action key | authorization policy reference | move |
| `examples` | `ToolSpec` | usage examples/testimony | invocation-contract examples | keep as evidence |

Primary classification: compressed responsibilities requiring separation.

### `ToolNeed`

| Field | Actual responsibility | Proposed owner | Action |
|---|---|---|---|
| `id`, `workspace_id` | demand identity/scope | capability-demand record | keep/rename |
| `name` | human/local demand label | capability-demand record | keep |
| `summary`, `reason` | demand rationale | capability-demand record | keep |
| `capability` | requested transformation label | capability demand | keep/rename field later |
| `risk_hint` | advisory risk | demand constraints | keep/split |
| `desired_inputs`, `desired_outputs` | desired representations | demand constraints | keep |
| `status` | lifecycle of demand | demand lifecycle | keep |

Primary classification: misnamed responsibility with a recoverable owner; it is capability demand.

### Provider recommendations / ranker

| Field | Actual responsibility | Proposed owner | Action |
|---|---|---|---|
| `provider` | candidate source/mechanism label | realization testimony | translate |
| `backend_type`, `operation` | optional handoff/contract hints | typed realization reference | keep as optional typed refs |
| `score`, `reasons`, `reasoning` | advisory ordering | recommendation testimony | keep; not selection |

Primary classification: implementation projection of a canonical responsibility.

### Pending calls, plans, proposals

| Artifact | Actual responsibility | Proposed owner | Action |
|---|---|---|---|
| `PendingAction` | pending invocation approval/confirmation | pending movement request | split/rename |
| `ActionPlan` | text-only legacy next-action proposal | external/advisory movement proposal | compatibility residue |
| `ExecutionProposal` | non-executable concrete call proposal with fingerprint | invocation proposal | recover only after separating from legacy plan/provider/tool names |

## 14. Shell/Bash proving case

For requested transformation `search a bounded corpus for matching text`:

| Step | Seed-native representation |
|---|---|
| requested transformation | bounded request: search corpus X for pattern Y |
| capability projection | current State/evidence says which search realizations may be reachable |
| mechanism availability | `/bin/bash` exists, `grep` exists, internal search producer exists, or remote service exists |
| realization testimony | each mechanism has accepted inputs, output representation, availability, dependencies, provenance, unknowns |
| invocation contract | command args or producer request grammar for one selected realization |
| dependency evidence | executable path, permissions, corpus access, parser availability |
| authority requirements | local process execution permission, read-only corpus permission |
| invocation request | one concrete grep/process call or internal producer call |
| validation | arguments match selected contract and bounded corpus |
| authorization | policy permits local process/read-only search |
| execution | actual process/producer movement |
| result artifact | attributed result with command/producer provenance |

No `tool` concept is constitutionally necessary. Bash-language competency, `/bin/bash` availability, local process execution reachability, and one concrete process invocation are distinct.

## 15. Internal-producer proving case

Existing examination road artifacts such as candidate examination work and examination probe request model internal deterministic projection without `ToolSpec`. The trace is:

```text
probe request -> candidate work/method applicability -> operational realization handoff -> result artifact
```

An internal deterministic producer is not a tool. It can be an operational realization. It may require an invocation contract or direct producer-call contract. It need not enter the same registry as an executable. Forcing it into tool vocabulary would distort ownership by making internal projection look like model-visible callable menu material.

## 16. LLM-as-external-source proving case

Correct trace:

```text
LLM supplies attributed operational suggestion
-> artifact attribution
-> examination/request binding
-> capability projection
-> realization projection
-> invocation validation
-> authorization
```

Current free-text runtime blocks direct movement. Remaining structural roads are compatibility/service-level: model-shaped `Decision` can be parsed/validated by `DecisionValidator`, and direct callers can pass `tool_name`/`tool_arguments` to executor services. The first missing owner is external operational suggestion ingestion/binding: a component that records LLM suggestions as attributed artifacts without treating `call_tool` as an invocation request.

## 17. Responsibility-only topology

```text
external artifact or user request
-> attributed suggestion / bounded requested transformation
-> capability demand
-> capability testimony and verification evidence projection
-> operational-realization testimony composition
-> realization selection
-> invocation-contract reference
-> invocation-request construction
-> invocation validation
-> authorization
-> pending movement if needed
-> execution
-> attributed result artifact
```

Established owners: inventory, catalog, validation, policy, execution. Compressed owners: `ToolSpec`, `ToolRegistry`, `ExecutionProposal`. Inappropriate owners: model-visible decision vocabulary as internal request grammar. Absent owner: external operational suggestion ingestion/binding. Compatibility-only surfaces: `Decision.kind == call_tool/request_tool`, `visibility=model_visible`, `ActionPlan`, many runtime-loop tests.

## 18. Ownership matrix

| Responsibility | Current producer | Current artifact | Current consumer | Actual ownership status | Seed-native responsibility | Migration pressure |
|---|---|---|---|---|---|---|
| capability demand | `ToolNeedService` | `ToolNeed` | state, catalog/ranker/plans | misnamed recoverable | bounded capability demand | rename only / translate |
| capability testimony | catalog, `ToolSpec.capabilities` | recommendations/labels | resolution, inventory | compressed | testimony inputs | split responsibility |
| capability verification | facts/evidence | `capability_verified`, inventory | inspections | canonical | verification conclusion | none |
| capability reachability projection | single projection/inventory composition | projection | CLI/tests | incomplete but legitimate | reachability composition | move ownership |
| realization testimony | catalog recommendations, registry | recommendations, `ToolSpec` | ranker/resolution | compressed | candidate realization testimony | split responsibility |
| realization inventory | `ToolRegistry` | registered specs | validation/execution | lawful inventory plus menu residue | implementation inventory | narrow adapter |
| realization compatibility | preconditions/projections | reports | proposals | partial | compatibility conclusion | split responsibility |
| realization selection | ranker/operation selection | ranked rec or operation result | plans/validation | advisory vs exact-name conflated | selection | split responsibility |
| invocation-contract preservation | `ToolSpec` | schemas/name/examples | validation/execution | compressed | invocation contract | move ownership |
| invocation-request construction | `Decision`, `ExecutionProposal`, pending action | tool call payloads | validation/execution | legacy grammar | bounded invocation request | translate at boundary |
| invocation validation | `ToolValidationService` | validation result | policy/executor | legitimate misnamed | validation | rename only |
| authorization | `ToolExecutionPolicyService`, `PolicyGate` | `PolicyDecision` | executor/pending | legitimate misnamed | authorization | rename only |
| pending movement | `PendingActionService` | `PendingAction` | resume | legitimate but tool-named | pending invocation | rename only |
| execution | `ToolExecutor` | tool.call events | ledger/facts | legitimate movement in old nouns | execution | narrow adapter |
| result attribution | executor/fact extraction | output/events/evidence | State | legitimate | attributed result artifact | rename only |
| external suggestion ingestion | model/decision adapters | `Decision` | validators historically | absent/misplaced | attributed suggestion artifact | immediate constitutional hazard |

## 19. Public compatibility analysis

Public compatibility boundaries include `Decision` JSON shapes, model prompt shapes, CLI output fields (`tool_name`, `tool_arguments`, provider), manifest format, registry API, tests, and persisted event/state shapes. Temporarily preserve adapters for persisted events and manifests. Do not let compatibility names constrain canonical recovery.

## 20. Tests protecting legitimate behavior

Tests protecting legitimate behavior include validation, policy, pending action, registry, capability inventory, single-capability projection, execution proposal safety, and internal LLM authority excision tests. The focused baseline run had 63 passes in those areas.

## 21. Tests protecting historical vocabulary

Failing runtime tests in `tests/test_tool_validation.py` and `tests/test_tool_recommendations.py` expect old `Runtime.handle_user_message` routing to validate or create `tool_need` responses. These preserve stale vocabulary/runtime drift against the newer authority-excision boundary.

## 22. Strongest supporting evidence

* `Runtime` explicitly refuses model-produced Decisions as Seed authority.
* `ToolExecutionPolicyService` separates registered operation validation from policy authorization.
* `CapabilityInventory` comments separate requested capabilities, admitted verification facts, and registered operation contract labels.
* `SingleCapabilityStateProjection` boundary notes explicitly say no provider selection, no operation selection, no verification, no execution, and read-only.
* `ActionPlan`, `HandoffPlan`, and `ExecutionProposal` docstrings mark them legacy/experimental and non-executable.

## 23. Strongest counterevidence

* `ToolValidationService` already acts close to clean invocation-contract validation: exact-name selection, existence, status, input schema, output schema.
* `ToolRegistry` is an in-memory inventory with deterministic lookup and does not itself execute or authorize.
* `request_tool` currently creates a durable demand artifact and does not execute.
* `ToolSpec` contains a coherent operational record for registered executable operations and removing the word `tool` too early could obscure current code paths.
* Direct LLM movement through core `Runtime.handle_user_message` has already been excised, reducing immediate hazard.

## 24. Supported conclusions

1. Legitimate responsibilities trapped in the district: capability demand, catalog testimony, realization inventory, invocation contracts, input/output validation, policy authorization, pending invocation, execution, result attribution.
2. Well-separated but inappropriate LLM grammar pieces: `Decision.kind` values `call_tool`/`request_tool`, model-visible tool menu, `tool_name`/`tool_arguments` as request grammar.
3. `ToolNeed` owns capability demand, but is misnamed.
4. `ToolSpec` owns several compressed responsibilities.
5. `ToolSpec` is closest to a compressed realization record plus invocation contract plus implementation binding plus legacy menu entry.
6. `Toolkit` owns packaging/namespace/provenance only.
7. `ToolRegistry` is both lawful inventory and historical menu through compressed ownership.
8. Registration can contribute testimony, not reachability.
9. Actual capability verification/reachability projection is partially in `CapabilityInventory` and `SingleCapabilityStateProjection`; no final canonical reachability owner exists.
10. Provider is overloaded, not stable.
11. Registered operation is useful implementation vocabulary but not proven canonical.
12. Operation is one form of invocation contract.
13. Tool call is external protocol grammar/compatibility vocabulary.
14. Current core runtime does not route `call_tool`; direct service APIs still accept it-shaped payloads.
15. `request_tool` expresses demand but preserves LLM-specific framing.
16. LLM cannot choose a realization through current free-text Runtime.
17. LLM-shaped artifacts can bind operation arguments if admitted by direct compatibility callers, not by current Runtime.
18. LLM-produced decisions cannot reach policy/execution through current Runtime; service-level compatibility still exposes that grammar.
19. No proving case requires `tool`.

## 25. Unsupported conclusions

Unsupported: all tool artifacts should be deleted; registry must be removed; all responsibilities can be reconciled by renaming only; provider can be unified; internal producers and executables need fully separate constitutional roads; `ToolSpec` is already a clean invocation contract.

## 26. Primary classification

C. The district contains legitimate responsibilities trapped inside an inappropriate LLM-derived operational grammar.

## 27. Tool-vocabulary classification

4. Tool is historical external-grammar residue and should disappear after its responsibilities are recovered.

## 28. LLM-boundary classification

IV. LLM operational grammar is structurally embedded throughout the operational district.

## 29. First-recovery classification

ε. Recover external operational suggestion ingestion first.

## 30. Exact first recovery boundary

Responsibility to recover: external operational suggestion ingestion and binding.
Current inappropriate/missing owner: model-shaped `Decision`/`call_tool` compatibility artifacts double as internal request shapes.
Producer: external model/adapter/manual source.
Input artifacts: attributed suggestion with proposed operation name/arguments/reason/source.
Output artifact: non-authoritative external operational suggestion record.
Immediate consumer: future Seed-native request-binding/capability-demand owner.
Manual/external responsibility eliminated: direct promotion of external `call_tool` grammar into invocation request.
Compatibility treatment: preserve `Decision` parser/old JSON as adapter input only.
Explicit exclusions: no registry rename, no manifest migration, no executor changes, no policy changes, no deletion of tests or persisted event shapes.

## 31. Implementation-warrant decision

One bounded implementation slice is warranted.

## 32. Files changed

* `operational_grammar_reconciliation_audit_001.md` only.

## 33. Probes executed

```bash
rg -n "ToolSpec|Toolkit|ToolRegistry|toolkit_id|tool_name|tool_arguments|tool call|call_tool|request_tool" seed_runtime tests campaigns
rg -n "ToolNeed|CapabilityCatalog|CapabilityInventory|SingleCapabilityStateProjection|capability_verified|capability_id" seed_runtime tests
rg -n "ProviderRecommendation|CapabilityRecommendation|RankedRecommendation|provider|backend_type" seed_runtime tests
sed -n '100,285p' seed_runtime/models.py && sed -n '1,170p' seed_runtime/registry.py
sed -n '1,230p' seed_runtime/tool_validation.py && sed -n '1,260p' seed_runtime/tool_execution_policy.py && sed -n '1,260p' seed_runtime/execution_proposals.py
sed -n '1,230p' seed_runtime/tool_needs.py && sed -n '1,260p' seed_runtime/capability_inventory.py && sed -n '1,240p' seed_runtime/single_capability_state_projection.py
sed -n '1,240p' seed_runtime/runtime.py && sed -n '1,130p' seed_runtime/decisions.py && sed -n '330,415p' seed_runtime/intent_classifier.py && sed -n '185,215p' seed_runtime/model_client.py
sed -n '1,130p' seed_runtime/capability_catalog.py && sed -n '1,245p' seed_runtime/recommendation_ranker.py && sed -n '1,220p' seed_runtime/action_plans.py
sed -n '1,260p' seed_runtime/execution.py && sed -n '1,100p' seed_runtime/pending_actions.py && sed -n '1,105p' tests/test_internal_llm_authority_excision.py
pytest -q tests/test_tool_validation.py tests/test_tool_needs.py tests/test_tool_recommendations.py tests/test_capability_inventory.py tests/test_single_capability_state_projection.py tests/test_registry.py tests/test_tool_execution_policy.py tests/test_pending_actions.py tests/test_execution_proposals.py tests/test_internal_llm_authority_excision.py
```

Baseline result: 63 passed, 9 failed. Failures are runtime drift/stale-vocabulary expectations caused by current Runtime authority excision returning `unsupported` rather than old `invalid_decision`, `tool_failed`, or `tool_need` paths.

## 34. Confidence statement

Confidence: high for the inspected operational district and first recovery boundary; medium for exhaustive public compatibility because CLI and persisted event surfaces are broad and were sampled rather than exhaustively audited.
