# Agentic planning/tool prototype contamination recovery 001

## Scope and negative authority

This is one bounded, report-only recovery of the surviving planning/tool prototype district after the removal of the canonical `Decision` model and active conversational Runtime road. It changes no production code, tests, CLI behavior, events, models, Book clauses, generated artifacts, or runtime wiring. It does not authorize deletion, renaming, replacement architecture, capability pipeline design, execution architecture design, or interpretation wiring.

The in-scope families are `Actor`, `PolicyDecision`, `ToolNeed`, `ToolNeedService`, `ToolSpec`, `Toolkit`, `ToolkitCandidate`, `ActionPlan`, `ProviderRecommendation`/`CapabilityRecommendation`, `HandoffPlan`, `ExecutionProposal`, `ExecutionProposalFailure`, `ExecutionAuthorization`, `PendingAction`, `request_tool`, `call_tool`, `model_visible`, provider recommendations, capability resolution, tool generation, and approval/confirmation vocabulary attached to those families.

The `ExecutionStatus` and timing district was excluded. The required status/timing search found adjacency in event batching, CLI status consumers, projection/build timings, observation timings, and diagnostics, but this report records only that adjacency as `Unknown` and does not analyze or classify those surfaces.

## Historical orientation

Historical repository testimony says the early prototype roughly followed `event -> context -> model-produced Decision -> request_tool/call_tool routing -> ToolNeed/plan/provider/execution structures`. Current Book testimony from the generic conversational excision says these adjacent families survived outside that excision and remained unresolved residue, not validated architecture. That testimony is an orientation aid only: descent from the old prototype is not current contamination proof, and survival after excision is not independent faithfulness proof.

## Search method

I used current implementation evidence first, and targeted historical testimony only where current code could not establish descent. Required searches were run across `seed_runtime`, `scripts`, `tests`, `book_of_seed`, and `docs` for the named artifacts and vocabulary; for event/lifecycle names; for actor/approval/source/visibility strings; and for excluded status/timing adjacency. I then inspected the owning model and service files, CLI entrypoints, projection code, precondition code, capability catalog/recommendation code, and relevant Book reports. Tests were treated as shape/projection testimony only, not active-road proof.

## Independent family recoveries

### Track A — Actor vocabulary

`Actor` is a literal vocabulary of `user`, `model`, `system`, `tool`, `builder`, and `approver`, and `Event.actor` defaults to `system`. This establishes an event-author label, not verified identity, constitutional role, or authority. Service methods often default actor labels (`system` for creation; `user` for accept/reject/supersede; `approver` for approval/authorization), but those values are caller-supplied or fixed defaults and are not authenticated. `approved_by` on `Approval` and `granted_by` on `ExecutionAuthorization` are strings, not verified subjects. `source_type="user"` occurs in fact/CLI/test surfaces and is caller or fixture testimony about source classification, not established source authority.

Standing: mixed. Event authorship labels are independently Seed-shaped as ledger attribution vocabulary, but `model`, `builder`, and `approver` retain prototype/approval-role residue when read as identity or authority.

### Track B — PolicyDecision

`PolicyGate.evaluate(...)` is the current producer. It consumes a `ToolSpec`, projected `State`, optional scope, optional policy action table, `ToolSpec.policy_action`, declared or configured risk, and `state.has_approval(...)`. It returns `PolicyDecision` outcomes `allow`, `block`, `require_confirmation`, or `require_approval` with action, reason, risk class, and optional approval id.

What it establishes: a bounded policy-gate result for a registered tool/action under the evidence read by `PolicyGate`. It does not establish execution, refusal, confirmation request occurrence, lawful approval demand, or universal Seed decision standing. The phrase in `policy.py` that generated manifests can be exercised by the prototype runtime preserves prototype testimony, but the current class itself is a useful bounded gate shape.

Standing: mixed but mostly independently Seed-shaped as a policy gate; contaminated only if treated downstream as execution permission or universal `Decision` replacement.

### Track C — ToolNeed and ToolNeedService

`ToolNeed` carries name, summary, capability, reason, requested event id, risk hint, desired I/O, and lifecycle status. Its status vocabulary compresses request standing (`proposed`, `accepted`), tool-generation lifecycle (`generating`, `generated`, `validating`, `validated`), registration lifecycle (`registered`), and rejection. Current searches did not reveal an active non-test `ToolNeed` creation road after Runtime/Decision removal; projection still consumes `tool_need.created`, and `ToolNeedService.set_status(...)` can emit `tool_need.status_changed`, but service callability and projection support are not active-road proof.

`requested_by_event_id` establishes only an asserted causal/request provenance id, not a valid demand or authority. `ToolNeedService.resolve_capability(...)` consumes a `ToolNeed`, a capability catalog, and optional recommendations, and returns read-only metadata: known capability, registered operation candidates (currently always empty), provider recommendations, and handoff candidates. It reports catalog/recommendation metadata; it does not resolve a need in the stronger sense of satisfying demand, proving capability absence, registering an operation, authorizing execution, or making a provider available.

Standing: mixed compression. Read-only capability metadata is independently useful, but the `ToolNeed` lifecycle strongly preserves request_tool/tool-generation prototype residue.

### Track D — ToolSpec, Toolkit, and model-visible inventory

`ToolSpec` is a schema-bearing operation/tool manifest with name, summary, toolkit id, input/output schemas, policy action, implementation string, status, visibility, risk class, capabilities, and examples. `Toolkit` bundles `ToolSpec` entries with status/source. Current state and capability inventory consume `ToolSpec` records for registered operation/capability metadata and policy preconditions, so `ToolSpec` has independent catalog/contract standing. However, `visibility="model_visible"` remains model-facing vocabulary. Current searches did not reveal an active model consumer after the conversational Runtime excision. No current non-model consumer was found that depends on the specific string to select, present, register, or execute.

Standing: ToolSpec/Toolkit are partially active and independently Seed-shaped for registered operation metadata; `model_visible` is historical/compatibility vocabulary unless a later recovery finds a consumer.

### Track E — ToolkitCandidate and tool generation

`ToolkitCandidate` stores a candidate id, `tool_need_id`, workspace, artifact path, generator label defaulting to `seed-builder-v1`, status defaulting to `generated`, and optional validation report id. No active non-test producer or consumer was evidenced in the current runtime files searched; the primary current standing is constructible schema plus historical/tool-generation vocabulary. The status says only that a candidate object claims a generation stage; it does not prove validation, registration, availability, implementation ownership, or builder authority.

Standing: constructible only / historical compatibility. It is a plausible excision candidate, but deletion is not authorized by this report.

### Track F — ActionPlan

`ActionPlan` is explicitly documented as a legacy/experimental, text-only, non-executable proposal for satisfying a tool need, retained for historical projection compatibility and side-path tests, not canonical Runtime/Core MVP. `ActionPlanService.create_plan(...)` can produce a plan from a `ToolNeed` and ranked recommendation, normalize capability/provider, derive risk/approval hint, build textual steps, and optionally emit `action_plan.created`. Current non-test CLI surfaces consume stored action plans for precondition reports, proposal generation, handoff creation, lifecycle transitions, and authorization grant preconditions. I did not find a current CLI path that produces new `ActionPlan` objects from current user input; service callability exists, and projection consumes events.

`ActionPlan` compresses candidate course of action, provider recommendation acceptance, textual operator proposal, lifecycle state, risk hint, approval-needed flag, precondition subject, and downstream proposal/handoff source. It explicitly refuses executable standing, approval grant, tool registration, and callable code.

Standing: mixed / partially active. Its lifecycle and inspect-only CLI consumers are active for stored events; its production road from `ToolNeed`/recommendation appears unconnected outside tests/helpers.

### Track G — HandoffPlan and provider recommendations

`CapabilityRecommendation` is a catalog suggestion that could satisfy a missing capability; `CapabilityCatalog` is read-only metadata that may suggest providers and handoff candidates and does not execute tools. `ToolRecommendationService` ranks catalog recommendations for a `ToolNeed` without creating providers, registering tools, or mutating state. Provider recommendations preserve candidate provider testimony/ranking, not selection, availability, registration, or delegation.

`HandoffPlanService.create_handoff_plan(...)` consumes an accepted stored `ActionPlan` and projected `State`, looks up matching catalog recommendation metadata, derives backend type/operation/target/policy summary/secret boundary, and optionally emits `handoff_plan.created`. `HandoffPlan` is explicitly legacy/experimental, non-executable, and rejects fields that would imply approval, authorization, credential availability, provider trust, or registration. It establishes a non-secret handoff boundary description, not handoff occurrence or execution delegation.

Standing: provider recommendations are independently Seed-shaped as advisory catalog testimony; HandoffPlan is mixed / partially active side-path compatibility with useful boundary refusals.

### Track H — ExecutionProposal and ExecutionProposalFailure

`ExecutionProposalService.create_proposal(...)` consumes an `ActionPlan` and projected `State`, evaluates preconditions, supports only the `service_management`/`docker_container_lifecycle` provider-specific builder, forms a concrete tool name and arguments, rejects secret fields, fingerprints arguments, and optionally emits `execution_proposal.created`. CLI `--proposal` is an active non-test producer for stored action plans. `ExecutionProposal` defaults `authorized=False` and `executable=False`; projection may later mutate those booleans to true when a matching unexpired `ExecutionAuthorization` event is replayed.

`ExecutionProposalFailure` classifies why a proposal could not be built: missing preconditions, provider/tool not registered, unsupported provider, missing host/container, or plan not found in CLI wrapping. It is diagnostic, not refusal, execution denial, or authorization judgment.

Standing: mixed / partially active. The inspect-only proposal diagnostic and provider-specific argument formation are active; the proposal grammar retains call_tool/prototype execution assumptions if treated as generic Seed execution grammar.

### Track I — ExecutionAuthorization

`ActionPlanService.grant_execution_authorization(...)` is the current producer. It consumes a stored execution proposal id, requires an accepted linked action plan, enforces positive bounded TTL, copies proposal id, plan id, tool name, argument fingerprint, grant label, expiry, and secret-free grant metadata, and emits `execution_authorization.granted`. The model rejects secret fields and unknown fields and requires `secret_seen_by_seed=False`. Projection consumes authorization events, stores them, and, if linked proposal id/plan/tool/fingerprint match and expiry is current, mutates the projected proposal to `authorized=True` and `executable=True`.

What it establishes: a short-lived secret-free grant metadata record linked to one existing proposal and plan under the current service checks. It does not prove competent authority, verified grantor identity, credentials, proposal validity beyond matching state, or actual external permission. The projection crossing that turns matching grant metadata into `ExecutionProposal.executable=True` is the strongest unfaithful active crossing found: it treats authorization metadata and fingerprint matching as executable standing inside the proposal read model.

Standing: mixed / partially active; independently useful as bounded grant metadata, contaminated when read as execution permission.

### Track J — PendingAction and call_tool remnants

`PendingAction` carries action, tool name, arguments, scope, status, created-from event id, and causation id. Searches found model/projection storage and historical/test references, but no current production service file or active non-test producer-consumer handoff. `request_tool` and `call_tool` remain in docs and historical testimony; current implementation searches did not find active Runtime routing after the `Decision` excision. Therefore `PendingAction`, `request_tool`, and `call_tool` are historical/compatibility-preserved in this bounded district.

Standing: constructible/historical compatibility. `PendingAction` compresses deferred execution, approval queue, execution request, selected operation, unrealized proposal, and compatibility state if interpreted strongly, but current code did not evidence an active road.

## Activity classifications

- Active: none in the strict full-producer/full-consumer sense across the entire old linear road.
- Partially active: `PolicyDecision`, `ToolSpec`, `Toolkit`, `ActionPlan`, provider recommendations, `HandoffPlan`, `ExecutionProposal`, `ExecutionProposalFailure`, `ExecutionAuthorization`.
- Constructible only: `ToolkitCandidate`.
- Historical or compatibility-only: `request_tool`, `call_tool`, `PendingAction`, `model_visible` string as model-facing visibility.
- Mixed: `Actor`, `ToolNeed`, `ToolNeedService`, `ActionPlan`, `HandoffPlan`, `ExecutionProposal`, `ExecutionAuthorization`.
- Unknown: excluded status/timing adjacency; whether any external caller outside searched repo invokes constructible service methods.

## Producer/artifact/consumer roads

| Road | Classification | Recovery |
|---|---|---|
| `PolicyGate.evaluate` -> `PolicyDecision` -> policy caller | Partial handoff | Producer exists; current direct consumers are limited by absence of active tool-call runtime. |
| `tool_need.created` -> `ToolNeed` -> projection/open needs/capability views | Identity/reference only / historical | Projection consumes event if present; active producer absent. |
| `ToolNeedService.resolve_capability` -> resolution payload | Constructible/partial | Callable read-only reporter; no current active request_tool route evidenced. |
| `CapabilityCatalog` -> recommendations -> `ToolRecommendationService`/ranker | Partial handoff | Read-only provider testimony/ranking active as service, not provider selection. |
| `ToolNeed` + ranked recommendation -> `ActionPlanService.create_plan` -> `action_plan.created` | Partial/historical | Service can emit, but active non-test producer path from current CLI not evidenced. |
| stored `ActionPlan` -> CLI preconditions/proposal/handoff/lifecycle/authorization | Partial active | Consumers exist for already-stored plans. |
| accepted `ActionPlan` -> `HandoffPlanService` -> `handoff_plan.created` | Partial active | CLI can produce non-executable boundary from stored accepted plan. |
| ready `ActionPlan` -> `ExecutionProposalService` -> `execution_proposal.created` | Partial active | CLI can create inspect-only concrete proposal for one provider-specific case. |
| `ExecutionProposal` -> `ActionPlanService.grant_execution_authorization` -> `execution_authorization.granted` | Partial active | CLI can record secret-free grant metadata for accepted plan/proposal. |
| `ExecutionAuthorization` -> projection mutation of `ExecutionProposal.authorized/executable` | Active crossing, unfaithful | Matching metadata is treated as projected executable standing. |
| `ExecutionAuthorization` -> `PendingAction` | No current relation | No active producer-consumer edge evidenced. |
| `PolicyDecision` -> `PendingAction` | No current relation | Old policy-gate handoff absent. |
| `ToolSpec` -> execution path | Partial/Unknown | Used by policy/preconditions/capability inventory; active call_tool execution route absent. |
| `ToolkitCandidate` -> `ToolSpec` registration | Historical/constructible | Schema fields suggest candidate/generation, but no active registration road evidenced. |

## Compressed responsibilities

- `Actor`: event authorship, role label, model/tool/system/builder/approver vocabulary, and potential authority implication.
- `PolicyDecision`: policy evaluation, constraint status, approval lookup, confirmation/approval demand words, and allow/block envelope.
- `ToolNeed`: demand/request, capability reference, capability absence/gap, acquisition request, desired interface, generation/validation/registration lifecycle.
- `ToolNeedService`: status mutation plus read-only catalog/recommendation resolution under one service name.
- `ToolSpec`/`Toolkit`: operation description, provider/toolkit manifest, schema contract, policy metadata, implementation locator, model affordance visibility.
- `ToolkitCandidate`: capability candidate, source artifact, generator output, validation/registering status.
- `ActionPlan`: textual proposal, provider recommendation uptake, lifecycle state, risk/approval hint, precondition subject, proposal/handoff source.
- `ProviderRecommendation`: catalog suggestion, ranking testimony, backend/operation metadata.
- `HandoffPlan`: handoff boundary, provider target metadata, policy/secret boundary, external approval metadata.
- `ExecutionProposal`: concrete-call proposal, provider-specific builder output, diagnostic subject, fingerprinted argument bundle, projected authorization/executable flags.
- `ExecutionAuthorization`: grant occurrence metadata, grantor label, expiry, proposal/plan/tool/fingerprint linkage, credential-adjacent secret-free markers.
- `PendingAction`: deferred execution, approval queue, execution request, operation selection, compatibility state.

## Current topology

The surviving district is not one coherent active linear road. The current topology is a set of side-path islands around projected events and CLI operations for stored artifacts:

1. Read-only capability metadata island: `ToolNeed`/catalog/recommendations/resolution.
2. Legacy planning island: `ActionPlan` plus lifecycle events and precondition reports.
3. Handoff boundary island: accepted `ActionPlan` to non-executable `HandoffPlan`.
4. Concrete proposal/authorization island: ready `ActionPlan` to provider-specific `ExecutionProposal`, then secret-free `ExecutionAuthorization`, then projected proposal flags.
5. Historical routing residue: `request_tool`, `call_tool`, `PendingAction`, `model_visible` as model-facing vocabulary.

## Prototype dependencies

The clearest prototype dependencies are model-facing `visibility="model_visible"`, `Actor` values `model`/`tool`/`builder`/`approver` when interpreted beyond labels, `ToolNeed` as former `request_tool` output, `ToolNeedStatus` generation/registration states, `ToolkitCandidate`/builder vocabulary, and `PendingAction`/`call_tool` vocabulary. `PolicyDecision`, `ActionPlan`, `HandoffPlan`, `ExecutionProposal`, and `ExecutionAuthorization` descend from the same neighborhood but contain explicit non-execution/refusal boundaries that are independently useful in narrower form.

## Independently Seed-shaped responsibilities

- Event authorship as an unverified label.
- Bounded policy-gate evaluation over known actions, risk, scope, and approvals.
- Read-only capability catalog and provider recommendation testimony.
- Schema-bearing registered operation metadata in `ToolSpec` where consumed as metadata/contract, not model affordance.
- Non-executable handoff boundary description with explicit refusal of approval/authorization/credentials/provider trust/tool registration.
- Secret-free short-lived authorization metadata when treated as metadata only.
- Precondition reporting and proposal failure diagnostics as inspect-only reports.

## Contaminated responsibilities

- Model-facing `model_visible` ownership without a current model consumer.
- `ToolNeed` lifecycle statuses that merge request, generation, validation, and registration as if one need lifecycle owned all of them.
- `ToolkitCandidate` builder/generation vocabulary when read as Seed capability standing.
- `ExecutionAuthorization` projection crossing that marks proposals `authorized=True` and `executable=True` based on metadata linkage/freshness.
- `PendingAction`, `request_tool`, and `call_tool` when presented as current canonical Seed grammar after Runtime/Decision removal.

## Mixed families

`Actor`, `PolicyDecision`, `ToolNeed`, `ToolNeedService`, `ActionPlan`, `HandoffPlan`, `ExecutionProposal`, and `ExecutionAuthorization` are mixed. They preserve useful bounded testimony but also carry prototype residue or compressed responsibilities with different activity/fidelity standing.

## Historical compatibility surfaces

`ActionPlan`, `HandoffPlan`, and `ExecutionAuthorization` explicitly say they are legacy/experimental or non-core compatibility/side-path artifacts. `PendingAction`, `request_tool`, `call_tool`, `ToolkitCandidate`, and `model_visible` are historical or constructible compatibility surfaces in this bounded recovery.

## Unknowns

- Whether external callers outside the searched repository still invoke service constructors/methods.
- Whether any future/non-repo model consumer reads `model_visible`.
- Whether excluded `ExecutionStatus`/timing surfaces compress distinct responsibilities; they remain excluded.
- Whether `ToolNeedService` should remain the name/owner for read-only capability metadata after decomposition.
- Whether `PendingAction` has any intended future standing independent of old `call_tool` routing.

## Possible deletion boundaries

Possible deletion boundary does not authorize deletion. Plausible excision candidates are `ToolkitCandidate`, `request_tool` vocabulary, `call_tool` vocabulary, `PendingAction`, and `model_visible` if a separate operation proves no consumer/compatibility obligation remains. These should be treated as candidates only, because schemas/projection/test compatibility may still impose migration work.

## Possible preservation boundaries

Preserve or recover separately the bounded policy gate, read-only capability catalog/recommendations, `ToolSpec` registered-operation metadata, non-executable handoff boundary, precondition/failure diagnostics, and secret-free grant metadata. Preserve their explicit refusals of execution, approval, authorization, credentials, provider trust, and registration while decompression proceeds.

## Smallest lawful next operations

1. Run a bounded decompression report on `ToolNeed`/capability metadata only, separating demand, capability reference, provider testimony, generation lifecycle, validation lifecycle, and registration lifecycle.
2. Run a bounded authorization/proposal recovery that separates grant metadata from executable standing and inspects the projection mutation from `ExecutionAuthorization` to `ExecutionProposal.executable`.
3. Run a bounded excision-readiness report for `PendingAction`, `request_tool`, `call_tool`, `ToolkitCandidate`, and `model_visible` after consumer searches include migration compatibility.
4. Run a separate `ExecutionStatus`/timing recovery, because this report intentionally stops at adjacency.

## Lawful stopping point

This inquiry stops before implementation changes, deletion, renaming, replacement design, status/timing recovery, or any claim that a candidate boundary is authorized for excision. It also stops before treating projection support, tests, or historical Book testimony as active producer-consumer proof.

## Residue matrix

| Artifact | current file(s) | principal responsibility or compression | active producer | active consumer | activity class | prototype dependency | independent standing | contamination standing | strongest Unknown | recommended next treatment |
|---|---|---|---|---|---|---|---|---|---|---|
| Actor | `seed_runtime/models.py`, `seed_runtime/events.py`, services | Event author/role label compressed with identity/authority vocabulary | Event append callers | Ledger/projection/audits/formatters | Mixed | `user`/`model`/`tool` chat-agent roles | Unverified event attribution | Contaminated if read as identity/authority | External identity layer absent | split candidate |
| PolicyDecision | `seed_runtime/models.py`, `seed_runtime/policy.py` | Policy gate outcome envelope | `PolicyGate.evaluate` | Policy callers/tests; no active call_tool route found | Partially active | Decision-shaped name/envelope | Bounded policy result | Contaminated if read as authorization/execution | Current production consumer after Runtime removal | preserve |
| ToolNeed | `seed_runtime/models.py`, `seed_runtime/tool_needs.py`, `seed_runtime/state.py` | Need/request/capability/generation/registration lifecycle compression | Event projection supports; no active non-test creator found | Projection, open needs, capability metadata | Mixed | Former `request_tool` artifact | Capability request/provenance record if bounded | Lifecycle compression | Whether non-repo caller creates needs | recover separately |
| ToolNeedService | `seed_runtime/tool_needs.py` | Status mutation plus read-only resolution metadata | Callable service methods | Callers/tests; active route absent | Mixed | Former request_tool service owner | Read-only catalog/recommendation reporter | Service name implies need ownership | Coherent owner after decompression | split candidate |
| ToolSpec | `seed_runtime/models.py`, `seed_runtime/preconditions.py`, capability inventory/state views | Registered operation/schema/policy/implementation/model visibility manifest | State seeding/events/fixtures | Policy, preconditions, capability inventory | Partially active | `model_visible`, prototype manifests | Operation metadata/contract testimony | Model affordance residue | Active executor consumer absent | preserve |
| Toolkit | `seed_runtime/models.py` | Bundle of tool specs/source/status | Constructors/fixtures | State/tool inventory consumers | Partially active | Toolkit/provider package framing | Metadata bundle | Could imply provider ownership | Active non-test production path | preserve |
| ToolkitCandidate | `seed_runtime/models.py` | Generated artifact candidate tied to ToolNeed | None found outside constructors/tests | None found outside constructors/tests | Constructible only | Builder/generation prototype | None beyond schema | Historical generation residue | Whether any hidden generator remains | excise candidate |
| ActionPlan | `seed_runtime/models.py`, `seed_runtime/action_plans.py`, `scripts/seed_local.py` | Text proposal/lifecycle/provider/risk/precondition source | Service can create; active CLI create path not found | CLI preconditions/proposal/handoff/lifecycle/auth on stored plans | Mixed | Planning side-path from request_tool | Non-executable proposal/precondition subject | Compressed selection/approval/preparation | Active producer road | recover separately |
| ProviderRecommendation | `seed_runtime/capability_catalog.py`, `seed_runtime/tool_recommendations.py`, `seed_runtime/recommendation_ranker.py` | Catalog provider suggestion/ranked advisory metadata | CapabilityCatalog load/ranker | Resolution, action-plan service inputs, handoff metadata | Partially active | Provider recommendation from request_tool path | Read-only provider testimony | Contaminated if selection/availability | Runtime consumer after request_tool removal | preserve |
| HandoffPlan | `seed_runtime/models.py`, `seed_runtime/handoff_plans.py`, `scripts/seed_local.py` | Non-executable provider boundary metadata | CLI/service for accepted stored plans | Projection/CLI formatting | Mixed | Provider handoff side-path | Boundary description with explicit refusals | Compatibility-shaped metadata | Actual external handoff standing | recover separately |
| ExecutionProposal | `seed_runtime/execution_proposals.py`, `seed_runtime/state.py`, `scripts/seed_local.py` | Concrete-call proposal/fingerprint/authorization flags | CLI/service for ready stored plans | Projection/auth service/CLI | Mixed | `call_tool` argument formation | Inspect-only provider-specific proposal | Contaminated if generic execution grammar | Whether executor consumes proposals | split candidate |
| ExecutionProposalFailure | `seed_runtime/execution_proposals.py`, `scripts/seed_local.py` | Proposal-build diagnostic | CLI/service diagnose failure | CLI formatting | Partially active | Refusal/decision residue historically | Diagnostic failure classification | Contaminated if refusal/denial | Completeness of failure taxonomy | preserve |
| ExecutionAuthorization | `seed_runtime/models.py`, `seed_runtime/action_plans.py`, `seed_runtime/state.py`, `scripts/seed_local.py` | Secret-free grant metadata linked to proposal/plan/tool/fingerprint | CLI/service | Projection/preconditions | Mixed | Authorization in execution prototype | Bounded grant metadata | Projection treats as executable standing | Competent authority/credential standing | split candidate |
| PendingAction | `seed_runtime/models.py`, `seed_runtime/state.py`, projection store | Deferred execution/approval queue/request compatibility | None found | Projection/store only | Historical or compatibility-only | Old `call_tool`/approval path | None currently evidenced | Compatibility state | Hidden producer/consumer | excise candidate |
| request_tool | docs/Book/tests; no active model route found | Historical missing-capability route to ToolNeed | None found after Runtime removal | None active found | Historical or compatibility-only | Direct old prototype route | None currently evidenced | Presented as grammar if reused | Migration/document compatibility | excise candidate |
| call_tool | docs/Book/tests; no active model route found | Historical tool execution route | None found after Runtime removal | None active found | Historical or compatibility-only | Direct old prototype route | None currently evidenced | Presented as active execution boundary | Migration/document compatibility | excise candidate |

## Final direct answers

1. The surviving district most clearly descending from the original agent prototype is the `request_tool`/`ToolNeed`/provider recommendation/`ActionPlan`/`HandoffPlan`/`ExecutionProposal`/`ExecutionAuthorization`/`PendingAction` neighborhood, with `ToolSpec.visibility="model_visible"` and actor values as adjacent model/tool residue.
2. Strictly active full roads are not evidenced. Partially active families include `PolicyDecision`, `ToolSpec`, `Toolkit`, provider recommendations, `ActionPlan`, `HandoffPlan`, `ExecutionProposal`, `ExecutionProposalFailure`, and `ExecutionAuthorization`.
3. Constructible or compatibility-preserved families include `ToolkitCandidate`, `PendingAction`, `request_tool`, `call_tool`, and `model_visible` as a model-facing string.
4. Compressed artifacts include `Actor`, `PolicyDecision`, `ToolNeed`, `ToolNeedService`, `ToolSpec`, `ToolkitCandidate`, `ActionPlan`, `ProviderRecommendation`, `HandoffPlan`, `ExecutionProposal`, `ExecutionAuthorization`, and `PendingAction`.
5. Independently Seed-shaped responsibilities are unverified event attribution, bounded policy-gate reporting, read-only capability/provider testimony, schema-bearing operation metadata, non-executable handoff boundary description, inspect-only proposal failure diagnostics, and secret-free grant metadata when not treated as execution permission.
6. Responsibilities still depending on model/Decision/request_tool/call_tool assumptions are `model_visible`, `request_tool`, `call_tool`, `PendingAction`, `ToolNeed` creation/lifecycle vocabulary, `ToolkitCandidate` generation, and generic readings of `ExecutionProposal` as tool-call grammar.
7. `Actor` establishes none of identity, constitutional role, or authority; it establishes only an event author/role label.
8. `PolicyDecision` establishes a bounded policy-gate outcome over a tool policy action, risk, scope, and approval evidence.
9. `ToolNeed` compresses request/demand, capability reference, capability gap/absence assumptions, desired interface, acquisition/tool request, provenance, risk hint, and generation/validation/registration lifecycle.
10. `ToolNeedService` does not yet own one coherent responsibility; it combines read-only capability metadata with status mutation under a legacy need-service name.
11. No current active model consumer of `model_visible` was found.
12. Provider recommendations preserve advisory catalog/ranking testimony only, not provider selection, availability, registration, handoff, or execution.
13. `ActionPlan` establishes a non-executable textual proposal/precondition subject and lifecycle state for a stored plan, not selection, approval, authorization, or executable steps.
14. `HandoffPlan` establishes a non-secret, non-executable handoff boundary description, not handoff occurrence, execution delegation, approval, credentials, trust, or registration.
15. `ExecutionProposal` establishes an inspect-only concrete-call candidate/fingerprint for a provider-specific case, not selection, authorization, execution request, or execution.
16. `ExecutionProposalFailure` classifies why proposal generation cannot build a proposal; it is diagnostic, not refusal or denial.
17. `ExecutionAuthorization` establishes secret-free short-lived grant metadata linked to a proposal/plan/tool/fingerprint, not competent authority, credentials, or lawful execution by itself.
18. `PendingAction` currently establishes only historical/compatibility state shape; no active deferred-execution road was evidenced.
19. The clearest active unfaithful crossing is projection treating matching unexpired `ExecutionAuthorization` metadata as `ExecutionProposal.authorized=True` and `executable=True`.
20. Plausible excision candidates are `ToolkitCandidate`, `PendingAction`, `request_tool`, `call_tool`, and possibly `model_visible` after consumer/migration proof.
21. Families requiring decompression before deletion are `ToolNeed`, `ToolNeedService`, `ActionPlan`, `HandoffPlan`, `ExecutionProposal`, and `ExecutionAuthorization`.
22. Yes. `ExecutionStatus` and timing were excluded; only adjacency was recorded as `Unknown`.
23. The smallest lawful next operation is a bounded `ToolNeed`/capability metadata decompression report, or separately an authorization/proposal recovery focused on the projection mutation from grant metadata to executable standing.
24. This inquiry must stop before code changes, deletion, renaming, new architecture, status/timing analysis, or treating candidate boundaries as deletion authority.

## Verification notes

Commands run:

```bash
rg -n 'Actor|PolicyDecision|ToolNeed|ToolNeedService|ToolSpec|ToolkitCandidate|ActionPlan|HandoffPlan|ExecutionProposal|ExecutionProposalFailure|ExecutionAuthorization|PendingAction|ProviderRecommendation|request_tool|call_tool|model_visible' seed_runtime scripts tests book_of_seed docs
rg -n 'tool_need\.created|tool_need\.status_changed|execution_proposal\.created|approval\.granted|execution_authorization\.granted|action_plan\.|handoff_plan\.|pending_action' seed_runtime scripts tests
rg -n 'actor=|approved_by|granted_by|source_type="user"|visibility="model_visible"' seed_runtime scripts tests
rg -n 'ExecutionStatus|ExecutionStatusConsumer|ProgressCadence|emit_progress_if_due|timing|duration' seed_runtime scripts tests
git diff --check
```
