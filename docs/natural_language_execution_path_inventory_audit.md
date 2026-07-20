# Natural Language Execution Path Inventory Audit

## Purpose

This document inventories repository content related to natural-language request handling, candidate generation, capability selection, and execution decisions.

It answers an implementation-status question left open by `docs/natural_language_request_routing_audit.md`:

```text
How much of the language-routing chain already exists?
```

This is an inventory audit. It is not an implementation plan, reconciliation, proposal, roadmap, schema, command vocabulary, routing design, or runtime behavior change.

## Authority And Scope

Repository authority wins over this audit. This audit preserves observations from current repository content and does not override the supporting language, capability, decision, or execution authority documents.

Primary supporting documents reviewed:

- `docs/natural_language_request_routing_audit.md`
- `docs/natural_language_observation_and_intent_derivation_reconciliation.md`
- `docs/language_candidate_routing_and_promotion_reconciliation.md`
- `docs/candidate_meaning_and_ambiguity_reconciliation.md`
- `docs/operator_intent_question_and_claim_interface_reconciliation.md`
- `docs/capability_authority_and_execution_boundary_reconciliation.md`
- `docs/capability_verification_reconciliation.md`
- `docs/execution_status_and_operator_feedback_reconciliation.md`
- `docs/input_inspection_reconciliation.md`
- `docs/input_act_decision_bridge.md`


## Chain Under Inventory

The preceding routing audit preferred this conceptual chain:

```text
Communicative Act
    ↓
Language Observation
    ↓
Interpretation
    ↓
Candidate Request
    ↓
Routing
    ↓
Capability Selection
    ↓
Execution Decision
    ↓
Execution
```

Current implementation contains pieces of this chain, but not the full chain as explicit runtime stages.

## Executive Inventory Finding

The repository currently contains:

- a raw user-message event surface;
- deterministic fixture-level input-act classification;
- a context packet containing visible tools and open tool needs;
- structured decision validation and runtime routing;
- a narrow deterministic tool-intent guard for `echo`;
- tool-need creation and capability/provider recommendation surfaces;
- registered tool inventory and capability mapping surfaces;
- tool-call validation, policy evaluation, pending-action handling, and execution.

The repository does not currently contain an explicit, general natural-language candidate graph or candidate-set preservation path that cleanly separates language observation, interpretation, candidate request, routing, capability selection, and execution decision for arbitrary operator language.

## Existing Language-Processing Surfaces

### Raw User Message Capture

`Runtime.handle_user_message` appends an `input.user_message` event containing the raw `text`, projects state, composes context, and then asks the model for a structured decision. This preserves the input as an event, but it does not create a separate language-observation object with candidate meanings.

### Context Composition

`DecisionInputComposer.compose` includes the current input text, active goal, selected entities, facts, evidence, visible tools, open tool needs, and a decision schema in a `DecisionInputPacket`. This gives the decision model language-adjacent context and capability visibility, but it is context assembly rather than interpretation ownership.

### Input Act Inspection

`seed_runtime/input_inspector.py` contains deterministic input-act classification for fixture-level categories:

```text
operator_query
command_request
user_observation
documentation_claim
correction
casual_answer
```

The classifier explicitly states that it does not call an LLM, choose a decision kind, execute a tool, or integrate with runtime routing. It is therefore a language-processing surface, but not the runtime natural-language request path.

### Intent Classification


```text
echo
answer
missing_tool
clarify
refuse
```


This is an intent path, but it is not equivalent to the full chain from language observation through candidate request routing. The implemented labels are coarse, and the builder directly constructs decisions from labels.

## Existing Candidate-Generation Surfaces

### Tool Need Generation


This is candidate-like generation for absent capability/tool support. It produces a tool-need object, not a general language-derived candidate set.

### Runtime Tool Need Creation

When Runtime receives a valid `request_tool` decision, `ToolNeedService.create_from_decision` records a `ToolNeed` and emits a tool-need event. This is a durable work/capability-gap surface created after decision validation, not an interpretation candidate buffer.

### Non-Executable Plan/Handoff Side Surfaces

The models for action plans and handoff plans explicitly mark those artifacts as non-executable historical or experimental side paths. They are relevant boundary evidence because they preserve the distinction between proposals/handoffs and execution, but they do not implement natural-language candidate routing.

## Existing Capability-Selection Surfaces

### Visible Tool Inventory In Context

`DecisionInputComposer` exposes visible registered tools to the decision model with names, summaries, schemas, policy actions, and risk classes. This lets the model choose a tool name in a `call_tool` decision, but the selection itself is model behavior plus validation rather than a separate deterministic capability-selection component.

### Tool Registry Capability Mapping

`ToolRegistry` stores registered tools and supports `list_tools_for_capability`. Tool manifests can attach normalized capability names to concrete registered tools. This is a capability inventory and mapping surface.

### Capability Catalog And Provider Recommendations

`CapabilityCatalog` is a read-only catalog from capability names to provider recommendations. It supplies metadata and provider/handoff suggestions and explicitly does not execute tools.

`ToolRecommendationService` and `RecommendationRanker` enrich and rank recommendations for a `ToolNeed`. They are read-only and do not register tools, install providers, or mutate state.

### Capability Resolution In Runtime

For `request_tool` decisions, Runtime creates a tool need, ranks recommendations, asks the tool-need service to resolve capability availability against the catalog and registry, and returns a tool-need response payload. This is capability-gap and provider-recommendation handling, not direct execution.

## Existing Execution-Decision And Execution Surfaces

### Structured Decision Kinds


### Runtime Routing

Runtime routes validated decisions as follows:

- `answer` appends a response answer event;
- `ask_question` appends a response question event;
- `request_tool` records a tool need and recommendation payload;
- `call_tool` delegates to `ToolExecutor`;
- `propose_state_patch` delegates to state patch validation/application;
- `refuse` appends a refusal event.

This is an execution-decision routing surface after a structured decision exists. It is not a natural-language routing layer before decision formation.

### Tool Intent Guard

`ToolIntentGuard` rejects schema-valid tool calls that violate deterministic intent rules. Currently its concrete semantic guard is narrow: `echo` calls must correspond to input beginning with `echo ` and the message must match the remaining input. Other visible tool calls pass this guard after visibility checking.

### Tool Validation And Policy Evaluation

`ToolValidationService` checks tool existence, registration status, input schema, output schema, and executable tool-call validity. `ToolExecutionPolicyService` resolves a tool, validates it, evaluates policy, and returns whether execution is allowed. It intentionally does not execute tools or collapse policy outcomes.

### Policy Gate

`PolicyGate` maps risk and approvals to `allow`, `block`, `require_confirmation`, or `require_approval`. Low-risk L1 actions can be allowed; L2 requires confirmation; L3 requires approval; L4 is blocked by default.

### Tool Executor

`ToolExecutor` owns registered-tool execution after validation and policy checks. It emits started, completed, failed, and policy-denial/pending-action behavior through events and services. This is the concrete execution boundary for registered tool calls.

## Existing Ambiguity Handling

Ambiguity exists in implementation primarily through coarse outcomes rather than candidate-set preservation:

- `ask_question` is a valid decision kind and Runtime returns a question response.
- The intent classifier includes a `clarify` intent label that builds an `ask_question` decision.
- Invalid model decisions, parse failures, and tool-intent rejections can trigger retry contexts that ask for corrected decisions.
- Input inspection preserves a deterministic input-act label but not alternate labels.

The implementation does not currently preserve multiple candidate meanings for ambiguous phrases such as `Show me summary`. No general candidate set, ambiguity score, bounded assumption record, or operator clarification record was found for natural-language capability selection.

## Boundary Findings

### Language Observation vs Intent Classification


### Intent Classification vs Capability Selection


### Capability Selection vs Execution

Capability catalog, provider recommendation, registry listing, validation, policy, and execution are separated in code. However, for direct `call_tool` decisions, the chosen tool is already embedded in the model decision before validation and execution policy. The runtime validates and gates that choice; it does not visibly preserve an earlier candidate capability-selection process.

### Capability Inventory vs Operator Meaning

The repository contains capability inventories in registry manifests and capability catalogs. Those inventories can inform model context, recommendations, and capability resolution. They do not prove operator meaning. The implementation does not contain a general mechanism that compares operator language candidates against inventory while preserving ambiguity and avoiding silent nearest-capability collapse.

## Missing Boundaries Observed

The following boundaries from the conceptual chain are not explicit general-purpose implementation stages:

- communicative-act object distinct from input event;
- language observation object distinct from raw input payload;
- interpretation object with source-attributed candidate meanings;
- candidate request set with alternatives and ambiguity metadata;
- routing boundary that dispatches candidates before promotion or decision;
- capability-selection boundary that is independent of model-selected tool names;
- execution-decision artifact distinct from a `Decision(kind="call_tool")`;
- bounded-assumption record for ambiguous natural-language requests;
- operator clarification lifecycle specifically tied to ambiguous capability selection.

## Boundary Collapses Observed

The implementation does not simply hard-code `Language -> Nearest Capability -> Execution` across the repository. It has validation, visibility, intent guardrails, policy gates, and executor ownership.

However, partial collapses or compression points exist:

- A model can choose a visible `call_tool` from context without an explicit intermediate candidate-routing artifact.
- `missing_tool` converts language-derived need into a normalized capability string without preserving alternate capability candidates.
- Runtime routing treats validated `call_tool` decisions as ready for executor policy/validation rather than as candidates requiring separate capability selection.

These are implementation compression points, not necessarily architectural violations. This audit only records their presence.

## Unresolved Observations

The repository evidence leaves these inventory questions unresolved:

- whether `input_inspector.py` is intended to remain fixture-level only or later feed runtime interpretation;
- whether direct model selection of visible tools is considered acceptable capability selection or a temporary prototype shortcut;
- how natural-language operator clarification should be represented if ambiguity concerns capability selection rather than general conversation;
- where a future participant should look for candidate-set preservation if it is added after this audit.

## Inventory Answer

How much of the chain already exists?

```text
Communicative Act          partially: raw input event only
Language Observation       partially: raw text preserved; no separate object
Interpretation             partially: input-act and intent classifiers
Candidate Request          partially: tool_need generation; no general candidate set
Routing                    partially: Runtime routes structured Decisions
Capability Selection       partially: registry/catalog/recommendations; no standalone selection boundary
Execution Decision         partially: Decision(kind="call_tool") plus validation/policy
Execution                  yes: ToolExecutor for registered tools
```

The strongest implemented portions are structured decision routing, registered tool validation/policy, capability metadata/recommendations for missing tools, and registered tool execution. The weakest implemented portions are explicit language observation, candidate-set preservation, ambiguity-aware capability selection, and operator clarification tied to capability ambiguity.
