# Remaining agent/runtime schema deletion topology 001

## Scope and negative authority

This is a report-only deletion-topology recovery on current `main` after PR 1916. It authorizes no deletion and intentionally changes no production code, tests, CLI behavior, events, models, Book clauses, generated artifacts, or runtime wiring. The inquiry follows implementation evidence for the remaining conversational-agent, tool-acquisition, planning, policy-routing, approval, readiness, handoff, builder, and execution-preparation skeleton.

Excluded districts were not investigated except to record edges: `ExecutionStatus`, progress/status/timing, observation models/providers, Evidence, Fact, FactSupport, FactConflict, general State projection, constitutional inquiry/examination/warrants/admission/views/lenses, Prometheus observation, SQLiteEventLedger, and EventLedger generally.

## Positive dimensional orientation

Seed-owned implementation must currently carry one of these responsibilities: dimension-bearing material; a responsible act over it; a constraint on lawful transition; a relation among dimension-bearing subjects; a bounded projection or composition; recording/preservation responsibility; or an ingress/egress boundary occurrence. The recurrent dimensional field used for orientation is subject/identity, assertion/content, standing, source/provenance, responsibility, authority/warrant, scope/locality, and occurrence/preservation. This report does not promote that orientation into a universal schema and does not rename foreign artifacts with dimensional vocabulary.

## Burden of preservation

For each in-scope artifact, preservation requires a complete current road: Seed-owned producer, bounded constitutional act, artifact with explicit standing limits, and current Seed-owned consumer. If the road is incomplete, classification is constructible only, projection compatibility, test-preserved, historical residue, foreign workflow grammar, mixed compression, or Unknown. Disclaimers such as legacy, experimental, inspect-only, non-executable, future execution path, safe proposal, bounded handoff, and side-path tests are evidence of possible compatibility shells, not warrants.

## Historical prototype topology

The deleted or partially deleted prototype family is still visible as a residual chain: user/model input -> context -> Decision -> `request_tool` -> `ToolNeed` -> provider recommendation -> `ActionPlan` -> policy decision -> readiness/precondition evaluation -> approval -> `HandoffPlan` -> execution proposal/authorization -> `PendingAction`/`call_tool` -> provider execution. Current implementation no longer evidences the active conversational Runtime and execution-proposal/authorization island, but many event, projection, CLI, and test surfaces still assume this grammar.

## Current artifact inventory

The candidate skeleton is a connected compatibility graph:

```text
Actor literal
  -> Event actor attribution and service lifecycle defaults
ToolNeed
  -> ToolNeedService / CapabilityCatalog / ToolRecommendationService
  -> action plan creation and capability inventory/test fixtures
ActionPlan
  -> ActionPlanService lifecycle events
  -> PreconditionEvaluator readiness reports
  -> HandoffPlanService source record
  -> CLI lifecycle, preconditions, handoff formatting
Approval
  -> PolicyGate and precondition approval_present
  -> action_plan.approved index
PolicyDecision
  -> PolicyGate output, policy tests
HandoffPlan
  -> HandoffPlanService, event projection, snapshot store, CLI --handoff
PendingAction
  -> state/snapshot compatibility; no current local producer found
ToolSpec / Toolkit
  -> registered operation manifests and model-visible/policy-routing metadata
ToolkitCandidate
  -> constructible generated artifact schema; no current non-test producer found
CapabilityRecommendation / ToolRecommendationService / Ranker
  -> useful catalog testimony mixed with provider-selection and handoff-candidate grammar
```

## models.py decomposition

`models.py` is not one district. It mixes legitimate material (`Event`, `Workspace`, `Session`, `Goal`, `Entity`, imported `Observation`, `Evidence`, `Fact*`) with agent/runtime workflow models.

| Model/literal/helper | Classification | Current producer | Current non-test consumer | Event/projection/CLI/test support | Independent Seed responsibility | Candidate treatment |
|---|---|---|---|---|---|---|
| `Actor` | Mixed | EventLedger/service defaults | Event, SQLite row actor, CLI/service lifecycle events | Event support yes; projection indirect; CLI actor defaults; tests | Event attribution label can remain; agent roles `model/tool/builder/approver` are compressed workflow labels | Split event attribution from agent-role vocabulary |
| `GoalStatus` | Seed-dimensional material | Goal construction | State goals | Event/projection support; outside candidate | Goal standing | Preserve |
| `ToolNeedStatus` | Foreign workflow grammar / mixed | ToolNeed default, ToolNeedService.set_status | State projection/status displays/tests | `tool_need.status_changed`; tests | Capability gap standing may be useful, but lifecycle is acquisition/build/registration grammar | Delete or split after capability testimony boundary |
| `PolicyOutcome` | Agent routing grammar | PolicyGate | PolicyDecision tests/consumers | No event; no CLI direct | None evidenced beyond routing | Delete with policy district |
| `RiskClass` | Shared dependency | ToolSpec, ActionPlan, PolicyDecision, catalog ranking | PolicyGate, ActionPlanService, capability/recommendation surfaces | Tests; no direct event alone | Risk label may remain where attached to registered operation testimony | Split from planning/policy routing if needed |
| `PendingActionStatus` | Foreign workflow grammar | PendingAction default | State/snapshot compatibility | No active producer found | None evidenced | Delete with PendingAction residue |
| `ActionPlanStatus` | Foreign workflow grammar | ActionPlanService | State/CLI/tests | `action_plan.*`; projection; CLI | None independent of plan lifecycle | Delete with ActionPlan district |
| `HandoffBackendType` | External-realization grammar / shared catalog metadata | CapabilityCatalog entries, HandoffPlan | HandoffPlanService, catalog/recommendation display | CLI handoff; tests | Backend metadata may be catalog testimony, but handoff use is foreign | Split catalog testimony before handoff deletion if still needed |
| `Event` | Seed-dimensional material | EventLedger/SQLiteEventLedger | StateProjector, diagnostics | Core event/projection | occurrence/preservation/provenance | Preserve, but actor type may split |
| `Workspace` | General runtime representation | constructors/tests | State/session contexts | General | scoped locality | Preserve |
| `Session` | General runtime representation | runtime/CLI/tests | events/session context | General | occurrence/context | Preserve |
| `Goal` | Seed-dimensional material | goal events | State | `goal.created` | responsible work standing | Preserve |
| `Entity` | Seed-dimensional material/general host representation | entity upsert/projection | facts/relationships/ranker context | Event/projection | subject identity | Preserve |
| `ToolNeed` | Mixed compression | runtime residue/tests, ledger fixtures | ToolNeedService, catalog/recommendations, ActionPlanService, capability inventory | `tool_need.*`; State.tool_needs; tests/docs | capability gap/demand testimony may remain; acquisition lifecycle does not | Split useful testimony or remove lifecycle artifact |
| `ActionPlan` | Foreign workflow grammar | ActionPlanService/tests/fixtures | Preconditions, HandoffPlanService, CLI, projection | `action_plan.*`; State.action_plans | No independent current responsibility | Delete district |
| `HandoffPlan` | Foreign external-realization grammar | HandoffPlanService/tests/fixtures | State, projection_store, CLI formatter | `handoff_plan.created`; State.handoff_plans | No active external handoff | Delete district after ActionPlan dependency considered |
| `PolicyDecision` | Agent routing grammar | PolicyGate | tests; possible ToolExecutor residue outside excluded follow | No event/projection | No active Seed road found | Delete with policy district |
| `PendingAction` | Historical compatibility | no current producer found in required scope | State/projection snapshot/tests | State.pending_actions; snapshot load | None | Delete compatibility field/model when safe |
| `ToolSpec` | Mixed | manifests/registry/state seeding/tests | PolicyGate, ranker, capability inventory, views | State.tools; projection snapshots; CLI seeding | registered-operation contract testimony: name, schemas, capabilities, status/source may survive | Split contaminated model-facing/policy/implementation fields if deleting agent grammar |
| `Toolkit` | Mixed | manifests/tests | registry/state seeding | projection snapshots | grouping/source testimony may survive | Split or preserve limited registered-operation catalog use |
| `ToolkitCandidate` | Builder prototype | tests/constructors | no current non-test consumer found | no projection field found | None active | Delete builder district |
| `Approval` | Mixed compression | `approval.granted` fixtures/events | State.has_approval, PolicyGate, preconditions | State.approvals; tests | approval occurrence could be Seed testimony; approved_by string is not authority | Split only if approval testimony independently used outside policy/readiness |
| `_reject_handoff_approval_claims` | Compatibility guard | HandoffPlan init | HandoffPlan construction | tests | Prevents overclaim inside legacy shell, not warrant | Delete with HandoffPlan |
| `utc_now` | Shared helper | Event timestamp | Event | Core | occurrence timestamp | Preserve |

## Service topology

- `ToolNeedService` is active only as a constructible service around stored `ToolNeed` and read-only capability resolution. It emits `tool_need.status_changed` but no current non-test command path was found in the inspected CLI. It compresses capability gap, demand, desired interface, acquisition lifecycle, and handoff/provider advisory payload.
- `ActionPlanService` is partially active through CLI lifecycle flags and `precondition_report`. It creates text-only plans from `ToolNeed` plus ranked recommendation and writes `action_plan.*` events. Its non-execution disclaimers do not make it Seed-owned.
- `PreconditionEvaluator` is wholly downstream of `ActionPlan`. Its checks translate host existence, registered tool name/toolkit matching, and any approval record into `executable`/`plan_ready`; it has no independent current road once action-plan execution-preparation grammar is removed.
- `PolicyGate` produces `PolicyDecision` from `ToolSpec.policy_action`, risk, and `State.has_approval`. The visible result is constructible/test-preserved routing output, not a constitutional movement/refusal.
- `HandoffPlanService` is active only as a CLI side path from accepted `ActionPlan` to stored `HandoffPlan`. It is external-realization grammar and has no evidenced external consumer.
- `ToolRecommendationService` and `RecommendationRanker` are read-only and partly useful: they preserve capability/provider testimony, but their ranking and provider-selection/handoff wording belongs to deleted planning/acquisition grammar unless separated.
- `CapabilityCatalog` preserves catalog entries that may be useful capability testimony, but `backend_type` and `operation` are shared with handoff/external-realization grammar.

## Event topology

| Event/state row | Current producer | Current projector | Current state field | Current non-test consumer | Historical requirement | Dead after which deletion | Candidate treatment |
|---|---|---|---|---|---|---|---|
| `tool_need.created` | runtime residue/tests/fixtures; direct ledger construction | StateProjector | `tool_needs` | capability inventory, recommendation/planning side paths | request_tool capability gap | District 6 unless capability inventory keeps split testimony | Split/delete lifecycle event |
| `tool_need.status_changed` | ToolNeedService.set_status | StateProjector | `tool_needs[*].status` | none found outside tests | acquisition/build/validation/registration lifecycle | District 6 | Delete |
| `action_plan.created` | ActionPlanService.create_plan | StateProjector | `action_plans` | CLI lifecycle/preconditions/handoff; operational graph diagnostics | historical plan proposal | District 2 | Delete |
| `action_plan.accepted` | CLI/ActionPlanService | StateProjector | `action_plans[*].status` | HandoffPlanService eligibility, CLI | plan selection/handoff prerequisite | Districts 1-2 | Delete |
| `action_plan.approved` | CLI/ActionPlanService | StateProjector index | `action_plan_approvals` | preconditions approval_present | readiness approval marker | District 2 | Delete with action-plan approval grammar |
| `action_plan.rejected` | CLI/ActionPlanService | StateProjector | `action_plans[*]` | CLI/status/tests | plan lifecycle | District 2 | Delete |
| `action_plan.superseded` | CLI/ActionPlanService | StateProjector | `action_plans[*]` | CLI/status/tests | plan lifecycle | District 2 | Delete |
| `approval.granted` | direct ledger/test fixtures; possible policy fixtures | StateProjector | `approvals` | PolicyGate, preconditions, State.has_approval | approval/policy routing | District 2/3 unless split as independent approval occurrence | Split if preserving approval testimony |
| `handoff_plan.created` | HandoffPlanService | StateProjector | `handoff_plans` | CLI display/snapshot | external realization boundary | District 1 | Delete |
| `pending_action.*` | no current producer found in required scope; test audit fixtures mention remnants | no branch found in inspected State replay for pending action events | `pending_actions` snapshot only | none found | request/call tool residue | District 4 | Delete compatibility field/model |
| tool generation/validation/registration events | no current `seed_runtime/tool_generation.py`; no active producer found | no dedicated projection branch found | none for ToolkitCandidate | tests/docs only | builder prototype lifecycle | District 5 | Delete vocabulary where constructible |

## Projection/state topology

`State` has legitimate projection responsibilities and must not be deleted wholesale. The candidate compatibility fields are `tool_needs`, `approvals`, `action_plan_approvals`, `pending_actions`, `action_plans`, `handoff_plans`, and portions of `tools`. Event replay projects `tool_need.*`, `approval.granted`, `handoff_plan.created`, and `action_plan.*`. Snapshot loading in `projection_store.py` reconstructs the same fields, including `PendingAction`, `ActionPlan`, `HandoffPlan`, `ToolNeed`, `Approval`, and `ToolSpec`. `projection_shape.py` lists these names as event-replay products; that is projection compatibility, not proof of active Seed ownership.

## CLI topology

The visible CLI preservation pressure is `--preconditions`, `--handoff`, `--accept-plan`, `--approve-plan`, `--reject-plan`, and `--supersede-plan`. Parser help explicitly labels preconditions and handoff as experimental/legacy side paths. Dispatch formats precondition reports and handoff plans and calls `ActionPlanService`/`HandoffPlanService`. `--provider` and recommendation language also exist for observation/capability diagnostics; those broader surfaces are not automatically part of the deletion district unless tied to `ToolNeed`, handoff candidates, or provider selection.

## Test topology

Primary preservation pressure comes from `tests/test_action_plans.py`, `tests/test_handoff_plans.py`, `tests/test_policy.py`, `tests/test_seed_local_script.py`, `tests/test_persistence.py`, `tests/test_capability_inventory.py`, `tests/test_state_views.py`, `tests/test_emitter_consumer_audit.py`, `tests/test_emitter_attribution_audit.py`, `tests/test_operational_graph.py`, and recommendation/capability tests. Tests prove construction, projection, non-execution, formatting, and diagnostic visibility; they do not prove active constitutional necessity.

## Documentation topology

Historical reports and docs preserve testimony. Orientation reports in `book_of_seed/*recovery*` and `docs/tool_vocabulary_orientation_recovery_investigation.md` are historical testimony or audit records unless they are active instructions/canonical claims. `docs/architecture.md`, `docs/invariants.md`, and durable lifecycle/reconciliation docs contain active or semi-canonical claims about Runtime, `request_tool`, `call_tool`, `ToolNeedService`, `ToolExecutor`, `ActionPlan`, `HandoffPlan`, approvals, and registered operations. Future cleanup should classify those references as active instruction, active canonical claim, historical testimony, audit record, fixture text, or ordinary unrelated language before editing.

## District dependency graph

```text
District 8 Actor vocabulary
  -> Event.actor and service lifecycle defaults
  -> ActionPlan lifecycle actor defaults
  -> event ledger storage actor column

District 6 ToolNeed acquisition lifecycle
  -> CapabilityCatalog.recommend_for(ToolNeed)
  -> ToolRecommendationService.recommend_for(ToolNeed)
  -> ToolNeedService.resolve_capability/status
  -> State.tool_needs and tool_need.* replay
  -> ActionPlanService.create_plan
  -> capability inventory/tests

District 7 ToolSpec/Toolkit model-facing residue
  -> State.tools/snapshot
  -> PolicyGate.evaluate(ToolSpec)
  -> RecommendationRanker registered-provider signal
  -> capability inventory registered-operation testimony
  -> ToolNeedService resolution placeholder

District 3 PolicyDecision routing island
  -> ToolSpec.policy_action/risk_class
  -> State.has_approval / Approval
  -> PolicyDecision output/tests

District 2 ActionPlan + precondition + approval readiness island
  -> ToolNeed + RankedRecommendation input
  -> ActionPlanService and action_plan.* events
  -> PreconditionEvaluator reads State.entities/facts/tools/approvals
  -> CLI lifecycle and --preconditions
  -> HandoffPlanService source

District 1 HandoffPlan external-realization island
  -> accepted ActionPlan
  -> CapabilityCatalog backend_type/operation metadata
  -> State.facts/tool_needs target derivation
  -> handoff_plan.created, State.handoff_plans, snapshot, CLI --handoff

District 4 PendingAction/request_tool/call_tool residue
  -> PendingAction model/status
  -> State.pending_actions/snapshot
  -> docs/tests references

District 5 ToolkitCandidate/builder generation island
  -> ToolkitCandidate schema
  -> tool_need_id and seed-builder-v1 defaults
  -> tests/docs references
```

Edge classifications: ToolNeed -> ActionPlan is active only if legacy plan creation is invoked; ActionPlan -> HandoffPlan is active through CLI side path; ToolSpec -> PolicyGate is constructible/test-preserved; ToolSpec -> capability inventory is partially active legitimate registered-operation testimony; CapabilityCatalog -> HandoffPlan is shared dependency that becomes dead for handoff after District 1 deletion; Approval -> policy/preconditions is mixed; EventLedger/State edges are projection compatibility for candidate artifacts.

## Shared capability-testimony boundary

The following may survive independently after planning/handoff deletion: capability labels, catalog entries saying a provider may support a capability, registered-operation contract associations, observed capability verification, and provider observations. The following should not survive by inertia: provider selected, recommendation rank as selection, backend as chosen realization strategy, operation as remote command, handoff candidate, approval as movement permission, and provider_registered as availability. `ToolSpec` likely requires field-level splitting or a narrower interpretation before deletion of contaminated fields, because its schemas/capabilities/status can be registered-operation testimony while `visibility="model_visible"`, `policy_action`, `implementation`, and examples can be model/tool-routing metadata.

## Candidate deletion districts

| District | Owner/root | Upstream dependency | Downstream dependency | Shared surfaces | Deletion prerequisites | Surviving testimony | Candidate treatment |
|---|---|---|---|---|---|---|---|
| 1 HandoffPlan external-realization island | `HandoffPlan`/`HandoffPlanService` | accepted `ActionPlan`, catalog metadata | event/projection/snapshot/CLI/tests | backend_type, operation, provider | Decide catalog metadata survival | catalog capability/provider testimony only | Delete whole service/model/events/CLI |
| 2 ActionPlan + precondition + approval readiness | `ActionPlanService`, `preconditions.py` | `ToolNeed`, `RankedRecommendation`, `Approval`, `ToolSpec` | `HandoffPlan`, CLI, tests | RiskClass, Approval, State tools/facts/entities | Remove or stage HandoffPlan first | possible approval occurrence, risk label elsewhere | Delete action/precondition/readiness together |
| 3 PolicyDecision routing | `PolicyGate`/`PolicyDecision` | `ToolSpec`, `Approval` | tests/possible executor residue | RiskClass, policy_action | Confirm no live executor road in current branch | registered-operation risk label | Delete or split from ToolSpec |
| 4 PendingAction/request_tool/call_tool residue | `PendingAction` | historical runtime decisions | state/snapshot/docs/tests | Event actor, ToolSpec | Confirm no active event producer | none in model | Delete compatibility model/state field |
| 5 ToolkitCandidate/builder | `ToolkitCandidate` | `ToolNeed` | docs/tests | artifact_path/generator/status | None if no producer | historical report only | Delete constructible schema |
| 6 ToolNeed acquisition lifecycle | `ToolNeed`/`ToolNeedService` | request_tool residue | recommendations, ActionPlan, capability inventory | capability labels, desired I/O | Preserve/split capability testimony first | capability gap/observation if already owned elsewhere | Split then delete lifecycle |
| 7 ToolSpec/Toolkit model-facing residue | `ToolSpec`/`Toolkit` | manifests/registry | policy, ranker, capability inventory | capabilities/schema/status/source | Identify registered-operation fields to keep | registered-operation testimony | Requires split first |
| 8 agent-role Actor vocabulary | `Actor` literal | service defaults | Event actor, SQLite storage | event attribution | Define existing attribution labels to keep without new architecture | event occurrence attribution | Split literal/actor defaults |

## Artifact matrix

| Artifact | Current files | Principal grammar | Current producer | Current consumer | Event support | Projection support | CLI support | Test-only support | Seed-dimensional responsibility | Foreign workflow dependency | Activity classification | Candidate district | Candidate treatment | Strongest Unknown |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Actor | models.py, events.py, action_plans.py | event label + agent role | EventLedger/service defaults | Event/SQLite/services | event actor column | event replay metadata | lifecycle commands | broad tests | attribution label | model/tool/builder/approver roles | Mixed | 8 | split | exact allowed non-agent actor set |
| ToolNeed | models.py, tool_needs.py, state.py | acquisition/gap | runtime residue/tests | recommendations/action plans/capability inventory | tool_need.* | State.tool_needs | seeded/dev only | many fixtures | possible capability gap | request_tool/build lifecycle | Mixed | 6 | split/delete | whether capability inventory needs current object |
| ToolNeedService | tool_needs.py | acquisition service | callable service | tests/possible runtime residue | status_changed | via state | none found | yes | read-only resolution maybe | ToolNeed lifecycle | Partially active | 6 | delete after split | hidden imports outside rg scope |
| ActionPlan | models.py, action_plans.py | planning/execution preparation | ActionPlanService | preconditions/handoff/CLI | action_plan.* | State.action_plans | lifecycle/preconditions/handoff | primary | none independent | ToolNeed/provider/risk/approval | Partially active | 2 | delete | historical DB migration burden |
| ActionPlanService | action_plans.py | lifecycle service | CLI/tests | StateProjector/CLI | action_plan.* | yes | yes | primary | none | planning workflow | Partially active | 2 | delete | live external callers |
| Precondition | preconditions.py | readiness prerequisite | evaluator | report formatter/tests | none | none | --preconditions | primary | none independent | ActionPlan readiness | Test-preserved/partially active via CLI | 2 | delete | none found |
| PreconditionReport | preconditions.py | readiness report | evaluator | CLI/tests | none | none | --preconditions | primary | none independent | executable/plan_ready | Partially active | 2 | delete | none |
| PreconditionEvaluator | preconditions.py | readiness engine | CLI/service/tests | ActionPlanService | none | reads State | --preconditions | primary | none independent | ActionPlan execution prep | Partially active | 2 | delete whole module | none |
| PolicyDecision | models.py, policy.py | routing decision | PolicyGate | tests/possible executor | none | none | none | primary | none | model/tool route | Constructible only | 3 | delete | hidden executor dependency |
| PolicyGate | policy.py | policy router | constructed in tests/possible executor | PolicyDecision | none | reads approvals | none | primary | possible risk check only if split | ToolSpec/pending action routing | Constructible only | 3 | delete/split | current executor use after Runtime deletion |
| Approval | models.py, state.py | approval record | approval.granted fixtures | PolicyGate/preconditions | approval.granted | State.approvals/index | approve-plan creates only action_plan.approved, not Approval | tests | possible approval occurrence | readiness/policy grammar | Mixed | 2/3/8 | split or delete with islands | independent approval road |
| HandoffPlan | models.py, handoff_plans.py | external realization | HandoffPlanService | CLI/projection | handoff_plan.created | State.handoff_plans | --handoff | primary | none active | ActionPlan/provider/backend | Partially active | 1 | delete | DB compatibility |
| HandoffPlanService | handoff_plans.py | handoff builder | CLI/tests | HandoffPlan/projection | handoff_plan.created | yes | --handoff | primary | none | external provider workflow | Partially active | 1 | delete | none |
| PendingAction | models.py, state.py, projection_store.py | tool-call pending workflow | no current producer found | snapshot/state only | no replay branch found | State.pending_actions snapshot | none | fixtures/negative asserts | none | request/call tool | Historical compatibility | 4 | delete | old ledgers with pending actions |
| ToolSpec | models.py, policy.py, capability_inventory.py | registered tool/model operation | manifests/seed state/tests | policy/ranker/capability inventory | tool registration via state seeding/snapshots | State.tools | dev seeding/views | broad | registered-operation schema/capability | model_visible, policy_action, implementation | Mixed | 7 | split | exact registry owner after Runtime removal |
| Toolkit | models.py | toolkit grouping | manifests/tests | registry/state | snapshot | State.tools through contained specs | seeding | tests | grouping/source maybe | tool framework | Mixed | 7 | split | whether toolkit object needed |
| ToolkitCandidate | models.py | builder artifact | no active non-test producer | none found | no projector | no state field | none | tests/docs | none | seed-builder-v1 | Constructible only | 5 | delete | whether generated artifacts exist outside code |
| CapabilityRecommendation | capability_catalog.py | provider suggestion | catalog files | ranker/handoff/service | none | no direct | stale/capability displays | tests | provider may support capability | selection/handoff backend | Mixed | 6/7/1 | split | backend/operation provenance |
| ToolRecommendationService | tool_recommendations.py | recommendation ranking | callable | tests/ActionPlan inputs | none | reads state | none found | tests | advisory testimony maybe | provider ranking/selection | Constructible only | 6 | split/delete | non-test import caller |

## File deletion-topology matrix

| File | Legitimate responsibilities | Contaminated responsibilities | Candidate deletions | Shared dependencies | Likely survives whole | Likely deleted whole | Requires split first | Strongest Unknown |
|---|---|---|---|---|---|---|---|---|
| seed_runtime/models.py | Event, Workspace, Session, Goal, Entity, imported evidence/fact/observation support | Actor roles, ToolNeed, ActionPlan, HandoffPlan, PolicyDecision, PendingAction, ToolkitCandidate, parts of ToolSpec/Toolkit/Approval | remove foreign models/literals | RiskClass, Approval, ToolSpec | no | no | yes | exact registered-operation model boundary |
| seed_runtime/policy.py | possible risk check concept | PolicyGate/PolicyDecision route output | whole policy router | ToolSpec, Approval, RiskClass | no | likely | maybe if risk reused | hidden executor dependency |
| seed_runtime/preconditions.py | none independent found | ActionPlan readiness/executable/plan_ready | whole file | State entities/facts/tools/approvals | no | yes | no | none |
| seed_runtime/tool_needs.py | possible capability resolution testimony | ToolNeed lifecycle/handoff candidates | status lifecycle and ToolNeed API | CapabilityCatalog, recommendations | no | maybe | yes | capability inventory coupling |
| seed_runtime/action_plans.py | none independent found | planning lifecycle/approval readiness | whole file | ToolNeed, RankedRecommendation, preconditions | no | yes | no | external callers |
| seed_runtime/handoff_plans.py | none independent found | external realization boundary | whole file | CapabilityCatalog metadata, ActionPlan | no | yes | no | none |
| seed_runtime/capability_catalog.py | capability catalog/provider may-support testimony | handoff backend/operation suggestions and ToolNeed API | remove ToolNeed-dependent API/handoff fields if needed | CapabilityRecommendation | maybe | no | yes | catalog field provenance |
| seed_runtime/tool_recommendations.py | advisory read-only ranking wrapper | ToolNeed-centered provider recommendation | service may delete | CapabilityCatalog, Ranker | no | likely if ToolNeed removed | maybe | non-test import callers |
| seed_runtime/recommendation_ranker.py | observed-state scoring may be useful testimony | provider selection/ranking as plan input | selection ranking may delete | CapabilityRecommendation, ToolSpec state | maybe | no | yes | independent diagnostic consumers |
| seed_runtime/tool_generation.py | none; file absent | builder vocabulary absent | none in file | n/a | n/a | n/a | n/a | whether historical path renamed |
| seed_runtime/state.py | legitimate projection of entities/facts/evidence/goals/etc. | candidate state fields and replay branches | remove specific fields/branches | Event, projection cache | no | no | yes | migration/snapshot compatibility |
| seed_runtime/projection_store.py | snapshot persistence generally | candidate model snapshot fields | remove fields after model deletion | State | no | no | yes | old snapshot compatibility policy |
| seed_runtime/projection_shape.py | diagnostic shape of legitimate projection | candidate fields listed as products | update product list after deletion | diagnostics | no | no | yes | diagnostic inventory coupling |
| seed_runtime/events.py | event recording generally | Actor literal includes agent roles; persisted id prefixes include need/plan/handoff/auth | adjust prefixes/actor type after deletion | SQLiteEventLedger | no | no | yes | old DB id reservation |
| scripts/seed_local.py | many legitimate diagnostics/views | action-plan/precondition/handoff lifecycle CLI | remove foreign flags/formatters/dispatch | StateProjector, ledger | no | no | yes | active doc references |

## Deletion-order matrix

| Sequence | District | Root dependency removed | Files touched | Tests removed or updated | Surviving testimony | Blocked follow-up unlocked | Replacement prohibited |
|---|---|---|---|---|---|---|---|
| 1 | HandoffPlan external-realization island | `HandoffPlan` and `handoff_plan.created` | models.py, handoff_plans.py, state.py, projection_store.py, projection_shape.py, scripts/seed_local.py, events.py prefixes if needed | test_handoff_plans.py, seed_local handoff tests, persistence/projection tests | catalog provider may-support metadata if split | ActionPlan accepted no longer needed for handoff | no EgressPlan/ExternalRequest |
| 2 | ActionPlan + precondition + approval readiness | `ActionPlanService`, `preconditions.py`, `action_plan.*` | action_plans.py, preconditions.py, models.py, state.py, projection_store.py, projection_shape.py, scripts/seed_local.py | test_action_plans.py, precondition CLI tests, operational graph/audit tests | possible approval occurrence only if split | ToolNeed no longer feeds plans | no Plan/Authorization/Workflow |
| 3 | PolicyDecision routing | `PolicyGate`/`PolicyDecision` | policy.py, models.py, ToolSpec fields if split, state approval helper if unused | test_policy.py and executor-policy residue tests | risk labels on registered-operation testimony if already owned | Approval grammar can be narrowed/deleted | no PolicyResult/Router |
| 4 | PendingAction residue | `PendingAction`/status/state field | models.py, state.py, projection_store.py, projection_shape.py, docs/tests | persistence/state negative asserts, docs | none | actor/tool-call docs cleanup | no pending workflow replacement |
| 5 | ToolkitCandidate/builder | `ToolkitCandidate` schema | models.py, docs/tests, generated fixture references | capability candidate/tool generation tests | historical reports only | ToolNeed acquisition statuses can shrink | no Builder/ToolManager |
| 6 | ToolNeed acquisition lifecycle | `ToolNeed` lifecycle/status/service | models.py, tool_needs.py, capability_catalog.py, tool_recommendations.py, state.py, projection_store.py, projection_shape.py, capability_inventory.py | capability inventory/state view/recommendation tests | capability observations/catalog/registered-operation associations | ToolSpec can be split without ToolNeed pressure | no CapabilityDemand/Manager |
| 7 | ToolSpec/Toolkit model-facing residue | `model_visible`, policy_action, implementation if not independently warranted | models.py, registry/capability inventory/policy docs/tests | registry/capability tests | registered-operation contract fields only | Actor model/tool labels can be narrowed | no ToolManager |
| 8 | Actor role vocabulary | agent-role values and defaults | models.py, events.py, action_plans.py removed already, docs/tests | event actor tests | event attribution labels | final docs cleanup | no role/authority framework |

## Candidate deletion order

The recommended bounded sequence is: (1) remove the HandoffPlan island, because it is downstream and has the clearest PR-1916 evidence; (2) remove ActionPlan plus precondition/readiness and action-plan approval lifecycle together, because splitting them leaves shells; (3) remove PolicyDecision routing after confirming no live executor road depends on it; (4) remove PendingAction residue; (5) remove ToolkitCandidate/builder schema; (6) split capability testimony from ToolNeed and delete acquisition lifecycle; (7) split registered-operation testimony from ToolSpec/Toolkit model-facing/policy metadata; (8) narrow Actor vocabulary to event attribution only. This minimizes repeated projection edits by batching model/event/state/snapshot/CLI/test cleanup per district and avoids inventing replacement architecture.

## Preservation topology

Must remain outside candidate deletion graph: Observation, Evidence, Fact, Entity, event recording generally, source/provenance testimony, capability observations, registered-operation testimony, legitimate State projection, views and diagnostics, bounded inquiry/examination, constitutional selections, provider observations, historical recovery reports, and Git history. Useful testimony currently compressed inside contaminated artifacts requires either field-level split first (`ToolNeed`, `ToolSpec`, `Approval`, `CapabilityRecommendation`, `Actor`) or historical-report-only preservation (`ActionPlan`, `HandoffPlan`, `PendingAction`, `ToolkitCandidate`). No implementation preservation is warranted for precondition readiness after ActionPlan deletion.

## Historical evidence policy

Existing reports and Git history should remain as evidence. Do not rewrite historical reports merely because their examined implementation is later removed. Classify references before cleanup: active instruction and active canonical claims can belong to future cleanup districts; historical testimony and audit records remain; fixture text is edited only when tests are deleted/updated; ordinary unrelated language is ignored.

## Unknowns

1. Whether any non-test caller outside inspected paths still constructs `PolicyGate` or `ToolRecommendationService` after Runtime removal.
2. Whether old SQLite ledgers/snapshots must retain compatibility for `need`, `plan`, `handoff`, `auth`, and candidate state fields.
3. Whether `ToolSpec.implementation`, `policy_action`, and `visibility` have a legitimate owner after all model-facing runtime routing is removed.
4. Whether catalog `backend_type` and `operation` were observed provider testimony or authored handoff compatibility metadata.
5. Whether independent approval occurrences exist outside policy/readiness grammar.

## Smallest coherent next excision

The smallest coherent next excision is District 1: delete the HandoffPlan external-realization island as one bounded change. It removes the root artifact, service, `handoff_plan.created` projection branch, snapshot field, CLI `--handoff` parser/dispatch/formatter, and direct tests. It must not introduce `EgressPlan`, `ExternalRequest`, external realization wrappers, boundary managers, or a replacement handoff architecture.

## Lawful stopping point

This inquiry stops at deletion topology. It does not delete, rename, split, migrate, or redesign artifacts. It records edges into excluded districts but does not follow them. It preserves absence as a valid future witness.

## Final direct answers

1. The remaining agent/runtime schema is a connected compatibility skeleton tying agent actor roles, ToolNeed acquisition, provider recommendation, ActionPlan lifecycle, readiness/preconditions, approval checks, PolicyDecision routing, HandoffPlan external realization, PendingAction residue, ToolkitCandidate builder schema, and model-facing ToolSpec/Toolkit metadata.
2. Seed-dimensional material in `models.py`: `Event`, `Workspace`, `Session`, `Goal`, `Entity`, and the imported Observation/Evidence/Fact family references; `GoalStatus` and `utc_now` also support legitimate standing/occurrence.
3. Foreign workflow grammar in `models.py`: `ActionPlan`, `HandoffPlan`, `PolicyDecision`, `PendingAction`, `ToolkitCandidate`, `ActionPlanStatus`, `PendingActionStatus`, `PolicyOutcome`, and agent-role portions of `Actor`.
4. Mixed models requiring a split: `Actor`, `ToolNeed`, `ToolNeedStatus`, `RiskClass`, `HandoffBackendType`, `ToolSpec`, `Toolkit`, `Approval`, and `CapabilityRecommendation` outside `models.py`.
5. `preconditions.py` is not independently warranted; it is owned by ActionPlan execution-preparation/readiness grammar.
6. No active execution road in the inspected current implementation requires its readiness grammar.
7. `PolicyDecision` is not currently evidenced as part of an active Seed road; it is constructible/test-preserved routing output pending hidden-caller confirmation.
8. No independent responsibility currently requires `ActionPlan`; it is historical plan/proposal workflow grammar.
9. No independent responsibility currently requires `HandoffPlan`; PR-1916-oriented evidence shows only internal construction/projection/CLI display, not external handoff.
10. No active external handoff is evidenced.
11. `PendingAction` has no active producer-consumer road found; it is snapshot/state compatibility residue.
12. `ToolkitCandidate` has no active producer-consumer road found; it is constructible builder prototype schema.
13. `model_visible` has consumers through registered operation/tool visibility and possibly model-facing inventory; it requires split analysis before deleting `ToolSpec` fields.
14. Useful `ToolSpec` registered-operation testimony: name, summary, input/output schemas, status, source/toolkit grouping, capabilities, and risk label only if attached to an independently owned contract.
15. Capability/provider recommendations that may survive: catalog entry, provider may support capability, provider observation, and registered-operation association; ranking, selected provider, backend realization, operation command, and handoff candidate should not survive by inertia.
16. `ToolNeed` compresses demand, pressure, capability reference, capability absence/gap, acquisition request, desired interface, builder lifecycle, validation lifecycle, registration lifecycle, and provider testimony.
17. Yes, useful distinctions can remain without the current lifecycle artifact if already-owned capability observations/catalog/registered-operation testimony carry them; no new owner should be invented here.
18. Compatibility-only events include `action_plan.*`, `handoff_plan.created`, `tool_need.status_changed`, pending-action/tool-call remnants, and builder generation/validation/registration vocabulary; `tool_need.created` and `approval.granted` require split analysis.
19. Compatibility-only projected State fields include `action_plans`, `handoff_plans`, `pending_actions`, `action_plan_approvals`, and likely ToolNeed lifecycle status; `tool_needs`, `approvals`, and `tools` require split analysis.
20. CLI surfaces preserving the foreign schema are `--preconditions`, `--handoff`, `--accept-plan`, `--approve-plan`, `--reject-plan`, and `--supersede-plan`.
21. Primary preservation-pressure tests are action plan, handoff plan, policy, seed_local CLI, persistence, capability inventory, state views, operational graph, emitter/consumer, emitter attribution, recommendation ranker, and related docs tests.
22. Coherent deletion districts are HandoffPlan, ActionPlan+precondition+approval readiness, PolicyDecision, PendingAction/request_tool/call_tool residue, ToolkitCandidate/builder, ToolNeed acquisition lifecycle, ToolSpec/Toolkit model-facing residue, and agent-role Actor vocabulary.
23. Excise in this order: HandoffPlan; ActionPlan+preconditions+readiness approval; PolicyDecision; PendingAction; ToolkitCandidate; ToolNeed lifecycle after splitting useful testimony; ToolSpec/Toolkit contaminated fields after registered-operation boundary; Actor role vocabulary.
24. Files likely deletable whole: `seed_runtime/handoff_plans.py`, `seed_runtime/action_plans.py`, `seed_runtime/preconditions.py`, likely `seed_runtime/policy.py`, and likely `seed_runtime/tool_recommendations.py` after ToolNeed deletion.
25. Files requiring splitting first: `seed_runtime/models.py`, `seed_runtime/state.py`, `seed_runtime/projection_store.py`, `seed_runtime/projection_shape.py`, `seed_runtime/events.py`, `scripts/seed_local.py`, `seed_runtime/capability_catalog.py`, `seed_runtime/recommendation_ranker.py`, and possibly capability inventory/state-view files.
26. Legitimate Seed testimony that must remain untouched: Observation, Evidence, Fact/FactSupport/FactConflict, Entity, event recording, source/provenance, capability observations, registered-operation testimony, legitimate State projection, diagnostics/views, bounded inquiry/examination, constitutional selections, provider observations, and historical reports.
27. No replacement architecture needs to be built.
28. The smallest coherent next excision is District 1, HandoffPlan external-realization island.
29. That excision unlocks deletion of ActionPlan accepted-status pressure and catalog backend/operation handoff coupling.
30. This inquiry must stop before implementation deletion, migration design, replacement naming, or following excluded districts.
