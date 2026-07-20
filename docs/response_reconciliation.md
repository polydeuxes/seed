# Executive Summary

Seed already communicates knowledge through multiple existing, read-only or runtime-facing response surfaces. Facts, explanations, contradictions, evidence, confidence, integrity counts, capability status, stale facts, graph issues, state views, decision context, runtime answers, tool-need records, refusals, and CLI summaries all exist today. The repository evidence confirms the Response Characterization finding: Response exists as a distributed concern, but its communication rules are fragmented across Runtime envelopes, explanation builders, integrity summaries, state/context views, capability inventory, contradiction/evidence/confidence helpers, and CLI formatters.

The reconciliation does **not** find justification for a `ResponseEngine`, a universal formatter, Runtime integration, ToolExecutor integration, adapters, routes, schemas, new read models, projection mutation, or event appends. Existing behavior is sufficient to communicate many operator-facing answers, but it is not consistently unified around caveats, uncertainty, limitations, rationale-plus-integrity presentation, or cross-surface composition.

Recommended outcome: **B. Response partially reconciled**. Response information largely exists, but it remains distributed and partially fragmented. The next safe architectural step, if needed, is additional documentation-only characterization of response caveats, uncertainty, summary expectations, or inventory expectations. No implementation work is justified by this audit alone.

# Purpose

This document reconciles Seed's existing Response concern after Response Characterization and Response Vocabulary v1. It asks what Response information already exists, how complete it is, where it is fragmented, who owns it, where composition already occurs, which operator questions are already answerable, and which questions remain hard to answer consistently.

This is an audit, not an implementation plan. The goal is reconciliation, not invention.

# Scope

In scope:

- existing Runtime response envelopes and decision outputs;
- existing CLI output builders and formatters;
- existing explanation, evidence, contradiction, confidence, integrity, capability, state, issue, observation, and decision-context surfaces;
- existing vocabulary and characterization documents for Response, Explainability, Context Composition, Selection Rationale, Knowledge Lifecycle, Knowledge Classification, Projection Integrity, and backlog/status reconciliation;
- operator-facing questions already answered or not consistently answered by existing surfaces;
- ownership and composition boundaries.

Out of scope:

- response behavior implementation;
- response composition implementation;
- response inventories;
- response summaries;
- response navigation;
- response read models;
- adapters, routes, schema classes, engines, or universal formatters;
- Runtime, ToolExecutor, EventLedger, ProjectionStore, provider, policy, or model-client changes;
- projection mutation or event appends.

# Files Inspected

Minimum requested files inspected:

- `docs/response_characterization.md`
- `docs/response_vocabulary.md`
- `docs/explainability_audit.md`
- `docs/explainability_inventory_audit.md`
- `docs/explainability_contract_characterization.md`
- `docs/explainability_reconciliation.md`
- `docs/explanation_contract_vocabulary.md`
- `docs/context_composition_vocabulary.md`
- `docs/selection_rationale_vocabulary.md`
- `docs/selection_rationale_reconciliation.md`
- `docs/projection_integrity_summary_characterization.md`
- `docs/projection_integrity_drilldown_characterization.md`
- `docs/backlog_and_status_reconciliation.md`
- `docs/knowledge_classification_vocabulary.md`
- `docs/knowledge_lifecycle_reconciliation.md`
- `seed_runtime/context.py`
- `seed_runtime/context_views.py`
- `seed_runtime/explanations.py`
- `seed_runtime/capability_inventory.py`
- `seed_runtime/state_views.py`
- `seed_runtime/contradictions.py`
- `scripts/seed_local.py`

Additional response, formatter, output, summary, inventory, explanation, and CLI-related files inspected:

- `docs/context_composition_reconciliation.md`
- `docs/selection_rationale_characterization.md`
- `docs/selection_rationale_summary_characterization.md`
- `docs/why_not_explanation_characterization.md`
- `docs/why_not_vocabulary.md`
- `docs/state.md`
- `docs/architecture.md`
- `docs/knowledge_acquisition_and_selection.md`
- `seed_runtime/runtime.py`
- `seed_runtime/models.py`
- `seed_runtime/evidence_graph.py`
- `seed_runtime/confidence.py`
- `seed_runtime/integrity_summary.py`
- `seed_runtime/context_budget.py`
- `seed_runtime/context_selection.py`
- `seed_runtime/model_client.py`
- `seed_runtime/model_clients.py`
- `seed_runtime/runtime_trace.py`
- `seed_runtime/tool_needs.py`
- `seed_runtime/tool_recommendations.py`
- `seed_runtime/registry.py`
- `seed_runtime/state.py`
- `seed_runtime/facts.py`

# Existing Response Producers

A Response Producer is an existing component that constructs response content, response-adjacent content, or operator-facing output from already-known knowledge. It does not need to be named "Response" in code.

| Producer | Classification | Evidence and finding |
| --- | --- | --- |
| `Runtime` | Response producer and response router | Produces `RuntimeResponse` values for answer, question, tool need, tool-call result, state patch result, refusal, invalid decision, invalid state patch, and unsupported decision outcomes. It also appends explicit `response.answer`, `response.question`, and `response.refusal` events for some response kinds. |
| `DecisionModel` / model client | Response-adjacent producer | Produces `Decision` objects, not final responses. Response Characterization's boundary is validated: model decisions are inputs to Response, not the whole Response concern. |
| `ContextComposer` | Selection producer and response-adjacent artifact producer | Composes `ContextPacket` from current input, goals, tool needs, facts, evidence, entities, tools, schema, and context budget trace. This is context/selection composition, not final user response composition. |
| `build_decision_context_view(...)` | Response-adjacent view producer | Produces a read-only `DecisionContextView` with facts, issues, requirements, capabilities, and summary. It can expose selected knowledge for decision and operator inspection. |
| `ExplanationBuilder` | Explanation Response producer | Produces `Explanation` objects with beliefs, evidence summaries, limitations, and contradictions for a subject/predicate query. |
| Evidence Graph helpers | Evidence/Integrity Response producers | `build_evidence_graph`, `build_fact_evidence_view`, `build_evidence_summary`, and `unsupported_fact_views` produce evidence-backed communication surfaces. |
| Contradiction helpers | Issue/Integrity Response producers | `build_contradictions` and `build_contradiction_summary` produce conflict records and counts with reasons and fact ids. |
| Confidence helpers | Uncertainty/Integrity Response producers | `build_fact_confidences`, `build_fact_confidence`, and `build_confidence_summary` produce confidence, support, contradiction, and reason signals. |
| `build_projection_integrity_summary(...)` | Integrity Summary Response producer | Aggregates existing unsupported fact, conflict, contradiction, graph issue, stale fact, refresh recommendation, and capability-status counts with caveats. |
| `build_capability_inventory(...)` | Capability/Inventory Response producer | Produces capability entries with state, support counts, confidence, source facts, expiry/staleness, caveats, and verification evidence. |
| State view builders | State/Observation/Issue/Capability Response producers | `build_fact_view`, `build_observation_view`, `build_requirement_view`, `build_capability_view`, `build_issue_view`, and `build_state_summary` expose projected knowledge in operator-facing forms. |
| `scripts/seed_local.py` formatters | Presentation producers | Formats runtime responses, events, state summaries, evidence graph, why-fact output, unsupported facts, contradictions, confidence, capability inventory, integrity summary, issues, decision context, conflicts, stale facts, refresh recommendations, runtime trace, and runtime why output. |
| `RuntimeTrace` helpers | Historical response/explanation producer | Load and summarize historical runtime runs for trace and why outputs without introducing a new response engine. |
| `ToolNeedService.resolve_capability(...)` and recommendation services | Capability response-adjacent producers | Produce known capability, registered operation, handoff, and recommendation metadata for `tool_need` responses. |

Response consumers include:

- CLI users/operators consuming formatted output;
- the model/decision layer consuming `ContextPacket` and retry prompts;
- `Runtime` consuming `Decision` and producing response envelopes;
- CLI formatters consuming read-only views and summaries;
- documentation consumers using vocabulary and reconciliation documents.

Response artifacts include:

- `RuntimeResponse`;
- runtime response events for answer/question/refusal;
- `ContextPacket` and `DecisionContextView`;
- `Explanation`;
- `EvidenceGraph`, `FactEvidenceView`, and `EvidenceSummary`;
- `Contradiction` and `ContradictionSummary`;
- `FactConfidence` and `ConfidenceSummary`;
- `ProjectionIntegritySummary`;
- `CapabilityInventoryEntry`;
- `FactView`, `ObservationView`, `RequirementView`, `CapabilityView`, `IssueView`, and `StateSummary`;
- formatted CLI strings.

# Existing Response Surfaces

| Surface | Direct / indirect / none | Finding |
| --- | --- | --- |
| Runtime `RuntimeResponse` | Direct | Directly exposes response kind, message, and optional payload to callers. |
| Runtime response events | Direct but partial | Directly record answer, question, and refusal response events. Tool need and delegated tool-call result responses are returned but not all are recorded as `response.*` events by Runtime. |
| CLI default output | Direct | `format_cli_output` renders response summary, optional raw model output, optional action plan, and optional events. |
| CLI `--raw` / model completion | Direct | Surfaces raw model output and therefore exposes model decision communication rather than normalized response communication. |
| Explanation output | Direct | `format_explanation` communicates beliefs, evidence, limitations, and contradictions. |
| Why-fact output | Direct | `format_why_fact` communicates evidence for facts and indicates absence of evidence. |
| Evidence graph output | Direct | `format_evidence_graph` communicates evidence nodes, links, and fact evidence. |
| Unsupported facts output | Direct | `format_unsupported_facts` communicates unsupported facts. |
| Contradiction output | Direct | `format_contradictions` communicates conflict records, reason, severity, and involved fact values. |
| Confidence output | Direct | `format_confidence` and `format_confidence_fact` communicate confidence, support counts, contradiction counts, unsupported status, reasons, and supporting events. |
| Projection Integrity Summary | Direct summary-like | `format_projection_integrity_summary` communicates aggregate integrity signals and caveats. |
| Capability Inventory | Direct inventory-like | `format_capability_inventory` communicates capability status, confidence, support, evidence, expiry, and caveats. |
| State views | Direct view-like | State, fact, observation, requirement, capability, issue, and state summary outputs expose current projected knowledge. |
| Decision context view | Indirect / response-adjacent | Exposes selected decision-ready facts, issues, requirements, capabilities, and summary. It is an input surface for decisions and an operator inspection surface, not final answer composition. |
| ContextPacket | Indirect | Communicates knowledge to model decision-making. It is not itself a user-facing response surface except through inspection/tests. |
| Runtime trace and runtime why | Direct historical | Communicate what happened in a run and why a decision/policy/outcome occurred. |
| Catalog/rule outputs | Indirect | Predicate, inference, and rule inventory outputs communicate capabilities/rules of the knowledge system, but not selected response content for a specific user question. |
| ToolExecutor internals | No Response ownership | Runtime may relay tool results as `RuntimeResponse`, but ToolExecutor should not become a general response surface by default. |

# Existing Response Composition

Existing composition occurs in several places, but no single Response composition layer owns all response communication.

## Runtime decision to response envelope

`Runtime._route(...)` composes final runtime response envelopes from validated decisions:

- answer decision -> `RuntimeResponse(kind="answer", message=...)` plus `response.answer` event;
- ask-question decision -> `RuntimeResponse(kind="question", message=...)` plus `response.question` event;
- request-tool decision -> tool need creation, recommendations, capability resolution, and `RuntimeResponse(kind="tool_need", ...)`;
- call-tool decision -> ToolExecutor result relayed as `RuntimeResponse`;
- propose-state-patch decision -> state patch result or validation failure response;
- refuse decision -> `RuntimeResponse(kind="refusal", ...)` plus `response.refusal` event.

Ownership: Runtime owns routing and response envelopes, but not capability semantics, tool execution semantics, state patch semantics, context selection, or explanation semantics.

## Context to selection to response-adjacent packet

`ContextComposer.compose(...)` composes current input, active goals, entities, facts, evidence, visible tools, open tool needs, decision schema, retry prompt, and budget trace into `ContextPacket`. This confirms the relationship:

```text
Context / projected state
↓
Selection / budgeted context
↓
Decision input
↓
Runtime response envelope
```

Ownership: ContextComposer and ContextBudget own context composition and selection traces. Response consumes or exposes these artifacts but does not own their selection rules.

## Context views to decision-ready summary

`build_decision_context_view(...)` composes facts, issues, requirements, capabilities, and a context summary from existing state, evidence graph, contradictions, confidence, and state views. This is existing response-adjacent composition over selected knowledge and integrity signals.

Ownership: Context Views own read-only decision-context composition. They explicitly do not own event reading, mutation, runtime behavior, provider calls, policy, tool execution, LLM calls, or separate stores.

## Explanation to response

`ExplanationBuilder.why(...)` composes beliefs, evidence summaries, limitations, and contradictions into an `Explanation`. CLI `format_explanation(...)` then presents the explanation. This is a complete explanation response path for fact-level why questions, but not a universal Response composition path.

Ownership: ExplanationBuilder owns explanation content. CLI owns presentation.

## Integrity to response

`build_projection_integrity_summary(...)` composes unsupported facts, fact conflicts, contradictions, graph issues, stale facts, refresh recommendations, and capability inventory counts into a summary with caveats. CLI formatting presents it. This is existing summary-like Response composition.

Ownership: Projection Integrity Summary owns aggregate integrity summary composition. It does not own truth, repair, refresh execution, verification execution, Runtime, ToolExecutor, or projection mutation.

## Capability inventory to response

`build_capability_inventory(...)` composes capability entries from capability verification facts, support, confidence, expiry/staleness, provider-reported or verified values, caveats, and verification evidence. Runtime also composes capability resolution into `tool_need` responses.

Ownership: Capability Inventory owns capability status communication from projected facts. ToolNeedService owns read-only resolution metadata for tool-need responses. Neither owns response globally.

## CLI formatters to presentation

`scripts/seed_local.py` contains many narrow formatters. They compose text for runtime responses, recommendations, state/cache summaries, graph issues, state summaries, evidence graph, why-fact, unsupported facts, contradictions, confidence, state views, capability inventory, integrity summary, issue views, decision context, fact support, current facts, explanations, conflicts, stale facts, refresh recommendations, traces, and runtime why.

Ownership: CLI formatters own presentation, not source semantics or projection truth.

# Existing Response Ownership

| Responsibility | Existing owner(s) | Finding |
| --- | --- | --- |
| Runtime response envelope | `Runtime` and `RuntimeResponse` | Implemented for answer/question/tool_need/tool result/state patch/refusal/invalid/unsupported outcomes. |
| Response event append for answer/question/refusal | `Runtime` | Implemented but partial; not every runtime response kind maps to a `response.*` event. |
| Context selection and budgeted packet | `ContextComposer`, `ContextBudget`, context selection helpers | Implemented and not owned by Response. |
| Decision-context composition | `context_views.py` | Implemented as read-only view composition. |
| Explanation content | `ExplanationBuilder` | Implemented for why fact/explanation surfaces. |
| Explanation presentation | CLI `format_explanation`, `format_why_fact` | Implemented in CLI. |
| Evidence communication | `evidence_graph.py` plus CLI formatters | Implemented. |
| Contradiction communication | `contradictions.py` plus CLI formatters | Implemented. |
| Confidence/uncertainty signal communication | `confidence.py` plus CLI formatters | Partial: signals exist, but cross-response uncertainty policy is not centralized. |
| Integrity summary composition | `integrity_summary.py` | Implemented as read-only aggregate counts with caveats. |
| Capability inventory communication | `capability_inventory.py` plus CLI formatter | Implemented. |
| State/current view communication | `state_views.py`, `State` query helpers, CLI formatters | Implemented. |
| Response formatting/presentation | `scripts/seed_local.py` | Distributed CLI formatters. |
| Caveats | Integrity Summary, Capability Inventory, Explanation limitations, selected formatter wording | Partial and fragmented. No single caveat composition rule exists. |
| Uncertainty | Confidence, explanation limitations, integrity caveats, capability states | Partial and fragmented. |
| Selection rationale communication | Context budget traces, selection rationale docs, explanations, state/current-best views | Partial; summary implementation was not justified in prior work. |
| Global Response ownership | None | Intentionally absent; evidence supports distributed ownership rather than a new engine. |

# Existing Response Categories

Classification uses Response Vocabulary v1 categories.

| Category | Status | Existing evidence |
| --- | --- | --- |
| Answer Response | Implemented | Runtime answer decisions return `RuntimeResponse(kind="answer")`; CLI default output formats response summary. |
| Explanation Response | Implemented | `ExplanationBuilder.why(...)`, `format_explanation(...)`, `format_why_fact(...)`, runtime why traces. |
| Integrity Response | Implemented | Projection Integrity Summary, graph issues, contradictions, unsupported facts, confidence summaries, stale facts, refresh recommendations. |
| Inventory Response | Implemented | Capability Inventory and rule/catalog inventories exist. Response inventory as a general Response artifact is missing and not justified by this audit. |
| Issue Response | Implemented | Issue views, graph issues, contradictions, unhealthy output, precondition reports, policy/execution proposal failures. |
| Capability Response | Implemented | Capability Inventory, capability views, tool_need capability resolution, recommendations. |
| State Response | Implemented | State summary, fact views, current facts, best fact, fact support, current issues, event summaries. |
| Observation Response | Implemented | Observation views, observed fact summaries/details, observation inventory diff/export outputs. |
| Why-Not Response | Partial | Tool-need/request-tool responses explain missing capabilities; runtime why and selection docs cover some why-not reasoning; no universal why-not response surface exists. |
| Selection Rationale Response | Partial / implicit | Context budget traces, ordering helpers, decision context, explanations, capability ranking reasons, and docs provide rationale signals. Prior selection-rationale summary implementation was not justified. |
| Uncertainty Response | Partial | Confidence, unsupported status, contradictions, stale status, capability verification state, caveats, and explanation limitations exist; consistent uncertainty communication across categories is missing. |

Communication capability audit:

| Information type | Status | Existing response route |
| --- | --- | --- |
| Facts | Implemented | Context packets, fact views, current facts, state summaries, explanations, evidence graph. |
| Explanations | Implemented | ExplanationBuilder, why-fact, runtime why. |
| Contradictions | Implemented | Contradiction views/summaries, confidence penalties, integrity summary counts. |
| Integrity signals | Implemented | Integrity Summary, confidence, graph issues, unsupported facts, stale facts, capability status. |
| Capabilities | Implemented | Capability Inventory, capability views, tool_need capability resolution. |
| Stale facts | Implemented | State stale fact helpers, stale fact CLI output, refresh recommendations, integrity summary counts. |
| Graph issues | Implemented | State graph issues, issue views, graph issue CLI output, integrity summary counts. |
| Uncertainty | Partial | Confidence and caveat signals exist; no shared cross-surface uncertainty composition rule. |
| Caveats | Partial | Integrity Summary caveats, capability entry caveats, explanation limitations; no shared caveat aggregation policy. |
| Rationale | Partial | Explanations, recommendation reasons, runtime why, context budget traces, selection rationale vocabulary; no centralized rationale response composition. |

# Existing Operator Questions Already Answerable

Existing surfaces can answer the following operator questions today:

- **What does Seed know?** Fact views, current facts, state summary, state views, observation views, and context packets expose projected facts and observations.
- **What did Seed select for decision-making?** `ContextPacket`, context budget traces, and `DecisionContextView` expose selected facts, issues, requirements, capabilities, and summary.
- **Why does Seed know or believe a fact?** `ExplanationBuilder`, why-fact output, evidence graph, fact support output, and confidence reasons expose evidence and support.
- **What evidence supports facts?** Evidence graph and fact evidence views expose evidence nodes, links, supporting event ids, and fact evidence views.
- **What facts are unsupported?** Unsupported fact views, evidence summary, confidence summary, and integrity summary expose unsupported facts and counts.
- **What conflicts exist?** Contradiction outputs, fact conflict outputs, confidence contradiction counts, and integrity summary contradiction/fact-conflict counts expose conflicts.
- **What graph issues exist?** Graph issues, issue views, unhealthy output, and integrity summary graph issue counts expose graph problems.
- **What capabilities exist?** Capability views and Capability Inventory expose known capability facts and status.
- **Which capabilities are verified, stale, unverified, unknown, or provider-reported?** Capability Inventory and Integrity Summary expose status at entry and count levels.
- **What facts are stale?** Stale fact outputs and Integrity Summary stale count expose stale facts.
- **What refresh recommendations exist?** Stale fact refresh recommendation output and Integrity Summary counts expose refresh recommendations.
- **What happened during a runtime run?** Runtime trace output exposes input, decision, policy, execution, response, error, and events.
- **Why did a runtime run make a decision?** Runtime why output exposes input, decision kind, decision reason, policy result, outcome, and final response/error.
- **What was returned to the user?** Runtime `RuntimeResponse`, CLI response summary, runtime trace final response, and response events for answer/question/refusal expose user-visible communication.
- **What limitations exist for an explanation or integrity summary?** Explanation limitations and integrity/capability caveats expose some limitations.

# Existing Operator Questions Not Easily Answerable

The following questions are not consistently answerable across response surfaces. Each finding is supported by inspection of distributed response producers and formatters.

- **How should multiple caveats be communicated together?** Integrity Summary has default caveats; Capability Inventory has entry caveats; Explanation has limitations; confidence and contradiction formatters have their own wording. There is no shared caveat aggregation rule across answer, explanation, integrity, capability, and state responses.
- **How should uncertainty be communicated consistently?** Confidence scores, unsupported flags, contradiction counts, stale status, capability verification states, provider-reported status, and explanation limitations all signal uncertainty, but no shared Response uncertainty policy determines ordering, wording, escalation, or combined presentation.
- **How should rationale and integrity be communicated together?** Selection rationale signals exist in context budget traces, ordering, recommendation reasons, and explanations. Integrity signals exist in summaries/views. There is no consistent composed surface that says: "this was selected, with this rationale, under these integrity caveats."
- **How should response limitations be surfaced consistently?** Limitations are present in explanation and caveat surfaces, but answer responses can be plain messages with no structured limitation field. CLI output also varies by formatter.
- **Which response producer owns final cross-surface presentation?** Runtime owns envelopes; CLI owns formatting; ExplanationBuilder owns explanation content; Integrity Summary owns integrity counts; Capability Inventory owns capability entries. No owner composes all categories into one canonical response.
- **How should answer responses incorporate known contradictions or stale facts?** Existing surfaces can expose contradictions and stale facts separately, but Runtime answer composition does not automatically incorporate those integrity signals.
- **How should capabilities, integrity, and why-not be communicated together?** Tool-need responses include recommendations and capability resolution, but broader why-not response composition remains partial and surface-specific.
- **How should response metadata be standardized?** `RuntimeResponse` has kind/message/payload, while view dataclasses and CLI strings expose metadata differently. Response Vocabulary names metadata, but implementation is intentionally not unified.
- **What is the canonical operator path for a comprehensive response audit?** Operators can inspect multiple surfaces, but no single response navigation/read model exists. This audit does not justify implementing one; it only identifies fragmentation.

# Relationship To Explainability

Validated finding: **Explainability explains claims and decisions; Response communicates explanations as one category of response.**

Explainability owns:

- explanation contracts and vocabulary;
- why-fact and explanation surfaces;
- evidence, belief, contradiction, limitation, and provenance communication for claims;
- runtime why-style explanation for historical decisions where available.

Response owns, conceptually:

- communication of selected knowledge and limitations to a consumer;
- presentation of explanation outputs alongside other response categories;
- deciding how explanation content is surfaced in a response surface, when such a surface already exists.

Overlap:

- Explanation outputs are response surfaces.
- Explanation limitations are response caveats/limitations.
- Evidence and contradiction communication can serve both Explainability and Response.

Boundary:

- Explainability does not own all response categories.
- Response does not create explanations or own explanation truth.
- A new `ExplainabilityEngine` or `ResponseEngine` would duplicate existing distributed ownership.

The Response Characterization finding is validated: Response overlaps with Explainability but is broader than Explainability.

# Relationship To Selection

Validated finding: **Selection chooses knowledge; Response communicates selected knowledge.**

Selection owns:

- candidate inclusion/exclusion where implemented;
- ordering and budget constraints;
- context packet composition;
- decision-context views;
- capability/recommendation ranking and context/current-state selection where those surfaces already exist.

Response owns, conceptually:

- communicating what was selected and its limits;
- presenting selected knowledge through answer, explanation, integrity, state, capability, issue, observation, and CLI surfaces.

Overlap:

- `ContextPacket` and `DecisionContextView` are both selection artifacts and response-adjacent surfaces.
- Selection rationale can become response content when an operator asks why something was included or ordered.

Boundary:

- Response should not select facts, rank candidates, mutate context budgets, or implement a `SelectionEngine`.
- Selection Rationale Summary implementation was previously not justified; this audit does not change that.

# Relationship To Integrity

Validated finding: **Integrity characterizes knowledge; Response communicates integrity.**

Integrity owns:

- support, confidence, contradiction, graph validation, staleness, refresh recommendation, capability verification, and summary characterization;
- read-only integrity counts and drilldown/navigation concepts;
- caveats that preserve meaning of integrity signals.

Response owns, conceptually:

- communicating integrity signals and caveats in operator-facing surfaces;
- composing integrity information with selected knowledge where existing surfaces do so.

Overlap:

- Projection Integrity Summary is both an Integrity artifact and a Response surface.
- Contradictions, confidence, unsupported facts, stale facts, graph issues, and capability status are integrity signals communicated by response surfaces.

Boundary:

- Response does not verify facts, resolve contradictions, refresh stale facts, repair graphs, or mutate projections.
- Integrity Summary is not a Response engine; it is a narrow summary over existing integrity signals.

# Existing Summary-Like Response Surfaces

| Surface | Summary-like response composition? | Summary surface? | Finding |
| --- | --- | --- | --- |
| Projection Integrity Summary | Yes | Yes | Aggregates existing integrity counts and caveats. Strongest existing summary-like Response surface. |
| Capability Inventory | Yes | Inventory-like summary | Composes capability status, support, confidence, expiry, evidence, and caveats by capability. |
| State Summary | Yes | Yes | Summarizes current projected state counts for facts, observations, requirements, capabilities, issues, and events. |
| Context Summary / DecisionContextView | Yes | Yes | Summarizes decision-ready facts, issues, requirements, capabilities, support, contradictions, and unsupported counts. |
| Evidence Summary | Yes | Yes | Summarizes evidence count, linked fact count, unsupported facts, average confidence, projection version, and last event id. |
| Contradiction Summary | Yes | Yes | Summarizes contradiction counts and severity buckets. |
| Confidence Summary | Yes | Yes | Summarizes confidence buckets, unsupported count, contradicted count, average confidence, projection metadata. |
| CLI response summary | Yes | Thin summary | Summarizes a runtime response message/output/recommendations. |
| Runtime trace summary | Yes | Historical summary | Summarizes a historical runtime run. |
| Explanation output | Partial | Explanation summary-like | Communicates beliefs and limitations but is query-specific rather than global summary. |
| Why-not outputs | Partial | Surface-specific | Tool-need, runtime why, policy/precondition/proposal failures answer some why-not questions, but not with a universal why-not surface. |
| Issue views | Partial | Issue list | Communicate current issues, not a full response summary. |

# Fragmentation Assessment

Response is **distributed, fragmented, and partially unified**.

It is not centralized because:

- no single Response module owns all response categories;
- Runtime, CLI formatters, ExplanationBuilder, Integrity Summary, Capability Inventory, Context Views, State Views, Evidence Graph, Contradiction, Confidence, ToolNeedService, and RuntimeTrace each own separate response-producing slices;
- response events only cover some runtime response kinds.

It is distributed by design because:

- each producer preserves local source semantics;
- Context Views explicitly stay read-only and avoid runtime/provider/tool/policy/LLM ownership;
- Integrity Summary aggregates existing signals without creating truth, repair, refresh, or execution behavior;
- Capability Inventory characterizes capabilities without verifying or executing them;
- CLI formatters present existing structures rather than inventing new facts.

It is fragmented because:

- caveats are scattered across integrity summary, capability inventory, explanations, confidence wording, and formatter-specific messages;
- uncertainty is represented by confidence scores, support counts, unsupported flags, contradiction counts, stale status, provider-reported/verified/unverified states, graph issues, and limitations without a common response rule;
- rationale appears in explanations, recommendation reasons, runtime why, context budget traces, and selection vocabulary, but not as a consistent response composition;
- answer responses can be plain messages that do not automatically include integrity/caveat/uncertainty metadata;
- CLI formatting is broad and practical but not a canonical Response contract.

It is partially unified because:

- Response Vocabulary v1 now names canonical response terms;
- Runtime envelopes consistently use kind/message/payload;
- summary-like surfaces use deterministic read-only composition;
- integrity and capability surfaces include explicit caveats;
- context, selection, explanation, and integrity documents agree that Response communicates selected characterized knowledge and limitations.

Conclusion: Response information already exists but is scattered. The main gap is not missing behavior; it is cross-surface composition language and consistency.

# Composition Opportunities

These are documentation-only opportunities. They are not implementation recommendations.

1. **Response Summary Characterization**
   - Justification: summary-like response surfaces already exist, especially Integrity Summary, State Summary, Context Summary, Evidence Summary, Contradiction Summary, Confidence Summary, Capability Inventory, and CLI response summary.
   - Constraint: should characterize existing summary behavior only; should not add a Response Summary implementation.

2. **Response Caveat Characterization**
   - Justification: caveats/limitations already exist but are fragmented across integrity, capability, explanation, confidence, stale, and contradiction surfaces.
   - Constraint: should document caveat sources and boundaries; should not add caveat schema classes or runtime injection.

3. **Response Uncertainty Characterization**
   - Justification: uncertainty signals already exist through confidence, support count, unsupported status, contradiction count, stale status, graph issues, verification state, provider-reported state, and explanation limitations.
   - Constraint: should reconcile vocabulary and communication expectations only.

4. **Response Inventory Characterization**
   - Justification: many response producers and surfaces exist, and this reconciliation identifies them. If operators need a stable list, a characterization could document existing inventory-like surfaces.
   - Constraint: should not implement an inventory read model or route.

5. **Rationale-plus-Integrity Communication Characterization**
   - Justification: rationale and integrity are both available but not consistently combined.
   - Constraint: should stay documentation-only unless a specific operator question later proves implementation need.

# Rejection Criteria

Response implementation work should **not** occur when any of the following are true:

- existing response surfaces already answer the operator question;
- the proposed work only renames existing producers or formatters;
- the proposed work duplicates Runtime response envelopes, CLI formatters, ExplanationBuilder, Integrity Summary, Capability Inventory, Context Views, State Views, Evidence Graph, Contradiction, or Confidence surfaces;
- the proposed work creates a parallel response system or parallel truth system;
- the proposed work adds behavior without a concrete unanswered operator question;
- the proposed work requires Runtime integration only to centralize already-working presentation;
- the proposed work requires ToolExecutor integration for general response composition;
- the proposed work mutates projections, appends events, or changes EventLedger/ProjectionStore ownership to answer a documentation or presentation question;
- the proposed work adds schema classes, adapters, routes, inventories, read models, or engines before documenting why existing surfaces are insufficient;
- the proposed work treats uncertainty, caveats, or rationale as proof/truth/repair rather than communication of existing signals;
- the proposed work turns Response into planning, reasoning, workflow, context selection, or execution ownership.

Implementation might only become justifiable if a future audit identifies a concrete, recurring operator question that cannot be answered by existing surfaces or by documentation-only reconciliation.

# Complexity Traps

- **`ResponseEngine`**: would centralize a concern that currently works through local owners. It risks duplicating Runtime, CLI formatting, ExplanationBuilder, Integrity Summary, Capability Inventory, Context Views, and State Views.
- **`ReasoningEngine`**: would confuse communication with model reasoning or inference. Response communicates selected characterized knowledge; it does not reason globally.
- **`ContextEngine`**: would duplicate ContextComposer, ContextBudget, context selection helpers, and Context Views. Selection is already bounded and read-only where needed.
- **Planner / WorkflowEngine**: would turn response communication into orchestration. Existing docs repeatedly reject planners/workflow engines as default solutions.
- **Universal Formatter**: would erase source-specific semantics and caveats. CLI formatters are intentionally narrow and tied to existing artifacts.
- **Runtime integration as default solution**: Runtime owns routing and response envelopes, not all explanation, integrity, inventory, uncertainty, or presentation semantics.
- **ToolExecutor integration as default solution**: Tool execution results may be relayed as responses, but ToolExecutor should not own response composition.
- **Parallel response systems**: a second response store/read model/adapter layer would duplicate existing surfaces unless a specific unanswered operator question demands it.
- **Parallel truth systems**: response composition must not create new facts, reconcile contradictions, verify capabilities, refresh stale facts, or mutate projections.
- **Schema-first response work**: adding schema classes before resolving ownership and operator questions would repeat the repository's known trap of inventing structure before need.

# Recommended Outcome

**B. Response partially reconciled.**

Evidence supporting this outcome:

- Response behavior already exists in Runtime response envelopes and CLI output.
- Response communication already exists across explanation, evidence, contradiction, confidence, integrity, capability, state, observation, issue, decision-context, and trace surfaces.
- Response composition already exists locally in Runtime routing, ContextComposer, Context Views, ExplanationBuilder, Projection Integrity Summary, Capability Inventory, and CLI formatters.
- Response ownership is intentionally distributed and usually belongs to the producer nearest the source semantics.
- Many operator questions are already answerable.
- The remaining gaps concern consistent caveat, uncertainty, rationale-plus-integrity, limitation, and cross-surface composition language.
- No inspected evidence justifies a new engine, route, adapter, schema class, read model, inventory, runtime integration, ToolExecutor integration, projection mutation, or event append.

Rejected outcomes:

- **A. Response largely reconciled** is too strong because caveat, uncertainty, rationale-plus-integrity, and limitation communication remain fragmented.
- **C. Response missing major concepts** is unsupported because core response categories and communication surfaces already exist.
- **D. More audit required** is not necessary for the current question; enough files and surfaces were inspected to classify the concern. More targeted documentation may be useful, but not because this reconciliation lacks evidence.

# Non-Goals

This reconciliation does not:

- implement response behavior;
- implement response composition;
- implement response inventories;
- implement response summaries;
- implement response navigation;
- implement response read models;
- implement adapters;
- implement routes;
- implement schema classes;
- modify Runtime;
- modify ToolExecutor;
- modify EventLedger ownership;
- modify ProjectionStore ownership;
- mutate projections;
- append events;
- create parallel truth systems;
- create parallel response systems;
- add provider behavior;
- add execution behavior;
- add planning or workflow behavior.

# Conclusion

Seed can already communicate knowledge. It can communicate facts, explanations, contradictions, integrity signals, capabilities, stale facts, graph issues, caveats, uncertainty signals, and rationale signals through existing distributed surfaces. The communication is useful but fragmented.

The correct reconciliation is to preserve distributed ownership, reject new engines and runtime/tool-execution integration by default, and document only the remaining cross-surface questions. Response is not missing as behavior. Response is partially reconciled as architecture, with documentation-only opportunities around caveats, uncertainty, summaries, inventories, and rationale-plus-integrity communication.
