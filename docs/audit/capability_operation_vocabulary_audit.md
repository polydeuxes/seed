# Capability / Operation Vocabulary Audit

## Executive Summary

This audit records the current accepted vocabulary boundaries for capabilities,
registered operations, provider/handoff operations, ToolNeeds, toolkits, and
ToolExecutor ownership.

Findings:

- Runtime remains the canonical request coordinator.
- `request_tool` records a `ToolNeed` and returns capability-resolution metadata;
  it does not execute tools.
- `call_tool` is the Runtime path into `ToolExecutor` for registered-operation
  execution.
- `ToolExecutor` remains the registered-operation executor.
- `CapabilityRecommendation.operation` is provider/handoff metadata only; it is
  not a `ToolRegistry` operation unless a separate registered `ToolSpec` exists.
- RuntimeLoop-era wording still appears in older docs and is the highest-risk
  source of architectural confusion.

No runtime behavior change is proposed by this audit.

## Canonical Vocabulary

### capability

A capability is a normalized abstract need/category such as `weather_lookup`,
`ssh_access`, or `service_management`. It names what Seed needs or can categorize,
not a callable function.

Capability appears as:

- `ToolNeed.capability`: the missing capability / capability gap requested by a
  model/user decision.
- `CapabilityCatalogEntry.capability`: the catalog key for known capabilities and
  recommendations.
- `ToolSpec.capabilities`: metadata tags on registered operations so Seed can
  discover operations that may satisfy a capability.

Current answers:

- A capability is abstract and non-executable in current core.
- Capability values are normalized by slugging/snake-case rules in the ToolNeed,
  catalog, and toolkit manifest paths.
- Capability names are owned by catalog entries, toolkit manifests, and
  normalized ToolNeed requests; Runtime consumes these names but does not make
  them executable.
- A capability cannot be called directly.
- Capability is metadata in models/catalogs/manifests and a discovery key in
  capability resolution.

### registered operation

A registered operation is a `ToolSpec` stored in `ToolRegistry`, keyed by
`ToolSpec.name`, with schemas, policy metadata, implementation reference,
visibility, status, risk class, and optional capability tags.

Current answers:

- `ToolSpec.name` is the canonical registered operation name.
- `ToolRegistry` is the active inventory for executable registered operations.
- `ToolExecutor` is the current-core executor for registered operations.
- Registered operations are executable from canonical Runtime only through a
  `call_tool` decision routed to `ToolExecutor`.
- Generated operation functions are reachable through Seed runtime execution only
  after registration; `ToolExecutor` verifies the registered implementation before
  importing/calling it.

### provider / handoff operation

A provider/handoff operation is the string in `CapabilityRecommendation.operation`,
for example `weather.lookup`, `service.manage`, or `docker.install`.

It describes a possible external provider/handoff operation or integration target. It is
metadata unless a separate builder/operator registers a corresponding `ToolSpec`
in `ToolRegistry`.

Current answers:

- `CapabilityRecommendation.operation` is a provider/handoff operation string.
- It can be confused with `ToolSpec.name` because both are called “operation.”
- It is not used as an executable `ToolRegistry` operation in current core.
- Docs should explicitly say it is metadata unless resolved to a registered
  `ToolSpec`.

### tool need

A ToolNeed is a durable missing-capability / capability-gap record. It is not an
executable tool.

A ToolNeed includes:

- `name`
- `summary`
- normalized `capability`
- `reason`
- optional `risk_hint`
- desired inputs/outputs
- lifecycle status

The term is historical and should usually be paired with “capability gap” in docs
when there is risk of confusion.

### toolkit

A toolkit is a manifest/package grouping one or more operation specs. Toolkit
manifests define toolkit metadata and a list of tools/operations. The manifest
loader converts those entries into `ToolSpec` objects and registers them in
`ToolRegistry`.

### tool spec

A ToolSpec is the executable contract/metadata for a registered operation:

- canonical operation name (`ToolSpec.name`)
- input/output schemas
- policy action
- implementation reference
- status and visibility
- risk class
- capability tags
- examples

### handoff candidate

A handoff candidate is read-only recommendation metadata emitted during capability
resolution when a catalog recommendation has `backend_type` and/or `operation`.

A handoff candidate does not imply:

- provider trust
- credentials
- approval
- execution
- pending action creation
- registration

## Ownership Table

| Concept | Canonical owner | Executable? | Metadata? | Current-core? | Historical / legacy? | Where defined | Where consumed |
|---|---|---:|---:|---:|---:|---|---|
| `ToolNeed` | `ToolNeedService` + state projection | No | Yes | Yes | No | `seed_runtime.models.ToolNeed` | Runtime `request_tool`, context, API/state views |
| `ToolNeed.capability` | Requester + `ToolNeedService` normalization | No | Yes | Yes | No | `ToolNeed.capability` | Capability catalog lookup, registry capability lookup, recommendation ranking |
| `CapabilityCatalogEntry` | `CapabilityCatalog` + `capability_catalog/*.yml` | No | Yes | Yes | No | `seed_runtime.capability_catalog` | `CapabilityCatalog.get`, `recommend_for`, `ToolNeedService.resolve_capability` |
| `CapabilityRecommendation` | `CapabilityCatalog` | No | Yes | Yes | No | `seed_runtime.capability_catalog` | Recommendation ranking and handoff candidates |
| `CapabilityRecommendation.operation` | Catalog authors/operators | No | Yes | Yes | No | Catalog YAML / recommendation model | Copied into `handoff_candidates` only |
| `ToolSpec` | Toolkit manifest loader + `ToolRegistry` | Yes, when registered and policy-allowed | Yes | Yes | No | `seed_runtime.models.ToolSpec` | Registry, validation, policy, executor, context/API listing |
| `ToolSpec.name` | Toolkit manifest + `ToolRegistry` | Yes | Yes | Yes | No | `ToolSpec.name` | Registry key and executor lookup |
| `ToolSpec.capabilities` | Toolkit manifest authors + manifest normalization | No | Yes | Yes | No | `ToolSpec.capabilities` | Capability-to-registered-operation lookup |
| `Toolkit` | Toolkit manifest loader + `ToolRegistry` | Indirectly | Yes | Yes | No | `seed_runtime.models.Toolkit` | Registry registration and toolkit listing |
| `ToolRegistry` | Registry service | No direct execution | Yes | Yes | No | `seed_runtime.registry.ToolRegistry` | Runtime context, validation, ToolExecutor, API, capability resolution |
| `ToolValidationService` | Validation service | No | Yes | Yes | No | `seed_runtime.tool_validation` | Decision validation, execution policy, executor output validation |
| `ToolExecutionPolicyService` | Policy sequencing service | No | Yes | Yes | No | `seed_runtime.tool_execution_policy` | `ToolExecutor.execute` before execution |
| `ToolExecutor` | Executor service | Yes | Emits results/events | Yes | No | `seed_runtime.execution.ToolExecutor` | Runtime `call_tool`, approved pending-action resume |
| `PendingAction` | `PendingActionService` + `ToolExecutor` | Not itself | Yes | Yes for approval-gated tool calls | No | `seed_runtime.models.PendingAction` | Created for policy-required registered tool calls; resumed by `ToolExecutor` |
| `ProjectionStore` | Projection cache layer | No | Yes | Yes | No | `seed_runtime.projection_store` | `project_state_with_cache` |
| `EventLedger` | Event ledger | No | Stores events | Yes | No | `seed_runtime.events.EventLedger` | Runtime, ToolNeedService, ToolExecutor, PendingActionService, projection |
| `Runtime` | Canonical Runtime | Routes; delegates execution to ToolExecutor | Emits response payloads | Yes | No | `seed_runtime.runtime.Runtime` | API and tests |
| `ActionPlan` | Legacy model/services | No | Yes | No | Yes | `seed_runtime.models.ActionPlan` | Historical projection / explicit legacy side paths |
| `HandoffPlan` | Legacy model/services | No | Yes | No | Yes | `seed_runtime.models.HandoffPlan` | Historical projection / explicit legacy side paths |
| `ExecutionProposal` | Legacy proposal service | No | Yes | No | Yes | `seed_runtime.execution_proposals` | Legacy proposal side paths/tests/projection |
| `ExecutionAuthorization` | Legacy metadata | No | Yes | No | Yes | `seed_runtime.models.ExecutionAuthorization` | Historical projection / legacy precondition/proposal inspection |

## Current Correct Boundaries

- Runtime is the canonical coordinator.
- `request_tool` creates or reuses a ToolNeed, ranks provider recommendations,
  resolves capability metadata, and returns a `tool_need` response payload.
- `call_tool` is the canonical Runtime branch into `ToolExecutor.execute`.
- `ToolExecutor` owns registered-operation execution, including validation/policy
  routing, implementation loading, started/completed/failed events, output schema
  validation, fact extraction, and pending-action creation for approval/confirmation
  policy outcomes.
- `ToolExecutionPolicyService` stops before execution and pending-action creation.
- `CapabilityCatalog` is read-only recommendation metadata.
- `ToolNeedService.resolve_capability` does not execute tools, authorize actions,
  create pending actions, or mutate registry/catalog state.
- `ProjectionStore` owns cached projected-state snapshots.
- `EventLedger` owns append-only events.

## Ambiguous / Risky Terms

| Term / phrase | Classification | Notes |
|---|---|---|
| `capability` | Correct | Abstract metadata/discovery key, not callable. |
| `registered operation candidates` | Correct | Separates registered operations from provider/handoff recommendations. |
| `CapabilityRecommendation.operation` / YAML `operation:` | Should be clarified | Metadata-only provider/handoff operation string; not executable and not a `ToolSpec.name` unless separately registered. |
| `tool` as model-visible registered operation | Ambiguous but harmless | Stable code name, but docs should prefer “registered operation” where precision matters. |
| `ToolNeed` / “tool need” | Should be clarified | Means capability gap, not executable tool. |
| `execute` in policy-service docs | Correct | Existing wording explicitly says the policy service does not execute. |
| `PendingAction` | Correct but boundary-sensitive | Created only for policy-required registered tool calls, not capability resolution. |
| `plan` in safe generated toolkit docs | Ambiguous but harmless | Safe when explicitly non-mutating / plan-only; avoid confusing with core `ActionPlan`. |
| `ActionPlan`, `HandoffPlan`, `ExecutionProposal`, `ExecutionAuthorization` | Correct where quarantined | Retained as non-core legacy/experimental compatibility artifacts. |
| RuntimeLoop in current docs | Dangerous if presented as active | Must remain deprecated/quarantined and not be described as CLI/API/default behavior. |

## Incorrect or Stale Wording

The highest-risk stale wording is in RuntimeLoop-era docs and inventories that can
make RuntimeLoop sound active or default again. These should be clarified before
any code changes:

- Docs that say CLI/API use RuntimeLoop by default.
- Docs that describe `Runtime` as legacy while current accepted architecture makes
  Runtime canonical.
- Docs that compare active RuntimeLoop execution ownership with `ToolExecutor`.
- Architecture bullets that identify RuntimeLoop as the request coordinator.
- Toolkit docs showing old top-level `capabilities` manifest shape when current
  registered-operation metadata is per-tool `ToolSpec.capabilities`.

## Runtime Safety Check

### `request_tool` does not execute

The `request_tool` Runtime branch records a ToolNeed, computes recommendation and
capability-resolution payloads, and returns a `RuntimeResponse(kind="tool_need")`.
It does not call `ToolExecutor.execute`.

### `call_tool` is the only Runtime path into ToolExecutor

The canonical Runtime branch for `decision.kind == "call_tool"` calls
`self.tool_executor.execute(...)`. The `request_tool` branch returns before this
branch and only returns metadata.

### `CapabilityRecommendation.operation` is metadata only

`CapabilityRecommendation.operation` is an optional string on catalog
recommendation metadata. Capability resolution only copies it into
`handoff_candidates`; it does not perform registry lookup, policy evaluation,
pending-action creation, or execution from that value.

### RuntimeLoop is not active

Current API wiring imports and calls `seed_runtime.runtime.Runtime`, not
`seed_runtime.runtime_loop`. RuntimeLoop-era references should remain quarantined
as historical/experimental wording only and must not define current architecture.

## Recommended Cleanup

Smallest safe next step:

1. Add or keep this docs-only vocabulary audit as the source of truth for these
   terms.
2. Add short stale-doc warnings to RuntimeLoop-era docs rather than refactoring
   code.
3. Clarify that `CapabilityRecommendation.operation` is provider/handoff metadata only, not executable and not a registry operation unless separately registered as a `ToolSpec`.
4. Clarify that ToolNeed means capability gap, not executable tool.

Avoid for now:

- new services
- new runtime behavior
- public field renames
- deleting compatibility models
- changing `ToolExecutor`
- changing Runtime routing
- making `CapabilityCatalog` executable
- making `CapabilityRecommendation.operation` executable

## Files Inspected During Audit

- `README.md`
- `01-architecture.md`
- `03-runtime-loop.md`
- `04-toolkit-system.md`
- `docs/capability_ownership_matrix.md`
- `docs/tool_execution_ownership_audit.md`
- `docs/audit/planning_execution_artifact_quarantine.md`
- `docs/runtime_reassessment.md`
- `docs/state_patch_inventory.md`
- `seed_runtime/models.py`
- `seed_runtime/capabilities.py`
- `seed_runtime/capability_catalog.py`
- `seed_runtime/tool_needs.py`
- `seed_runtime/tool_recommendations.py`
- `seed_runtime/recommendation_ranker.py`
- `seed_runtime/registry.py`
- `seed_runtime/execution.py`
- `seed_runtime/tool_validation.py`
- `seed_runtime/tool_execution_policy.py`
- `seed_runtime/pending_actions.py`
- `seed_runtime/runtime.py`
- `seed_runtime/decisions.py`
- `seed_runtime/api.py`
- `seed_runtime/events.py`
- `seed_runtime/projection_store.py`
- `seed_runtime/state.py`
- `seed_runtime/__init__.py`
- `seed_runtime/execution_proposals.py`
- `capability_catalog/*.yml`
- `toolkits/core/echo/toolkit.yaml`
- `toolkits/generated/environment_inventory/toolkit.yaml`
- `toolkits/generated/host_notes/toolkit.yaml`
- `toolkits/generated/ssh_access/toolkit.yaml`
- `tests/test_api.py`
- `tests/test_registry.py`
- `tests/test_public_exports.py`
- `pyproject.toml`

