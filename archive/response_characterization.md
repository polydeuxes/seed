# Executive Summary


Response in Seed is best characterized as the communication and presentation layer over selected projected knowledge and its limitations. It includes answer/question/refusal output construction, terminal formatting, presentation of explanation and integrity signals, and summary-like composition. It does not own knowledge acquisition, truth selection, projection mutation, provider execution, tool execution, or model reasoning.

The audit found behavior before vocabulary. Existing code can already answer many operator-facing questions, including what Seed currently knows, why a fact is believed, what contradictions or graph issues exist, what facts are unsupported or stale, what capabilities are registered or verified, and what selected context is available for decisions. However, existing surfaces cannot easily answer cross-surface communication questions such as how to combine multiple explanation surfaces, how to present several integrity signals together beyond counts and drill-down pointers, or how to communicate uncertainty consistently across answer, explanation, integrity, and inventory outputs.

Recommended outcome: **B. Response partially present**. A Response implementation, engine, adapter layer, route, schema class, inventory, Runtime integration, ToolExecutor integration, or projection mutation is not justified by this characterization. The safest next step is documentation-only Response Vocabulary or Response Reconciliation if operators need a shared language for existing surfaces.

# Purpose

This document characterizes Seed's current Response concern using repository evidence. It asks what Response is, where response-related behavior already exists, what composition and ownership boundaries already exist, which questions are answerable, and which response questions remain unanswered.

This is an audit, not an implementation plan. It documents existing behavior and boundaries without adding Runtime behavior, ToolExecutor behavior, schemas, routes, adapters, inventories, read models, projection mutations, event appends, or engines.

# Scope

In scope:

- runtime answer, question, refusal, invalid-decision, tool-need, tool-call-result, and state-patch response envelopes;
- explanation, evidence, contradiction, confidence, integrity, state, capability, issue, and CLI output surfaces;
- existing documentation for explainability, context composition, selection rationale, integrity summaries/navigation, knowledge lifecycle, and backlog/status reconciliation;
- ownership and fragmentation assessment.

Out of scope:

- implementing response behavior;
- adding a Response engine or universal formatter;
- modifying Runtime, ToolExecutor, EventLedger, ProjectionStore, projections, providers, or model clients;
- appending events or mutating projections;
- creating inventories, read models, adapters, schema classes, routes, or runtime integrations.

# Files Inspected

Minimum requested files inspected:

- `docs/explainability_audit.md`
- `docs/explainability_inventory_audit.md`
- `docs/explainability_contract_characterization.md`
- `docs/explainability_reconciliation.md`
- `docs/explanation_contract_vocabulary.md`
- `docs/context_composition_reconciliation.md`
- `docs/context_composition_vocabulary.md`
- `docs/selection_rationale_characterization.md`
- `docs/selection_rationale_vocabulary.md`
- `docs/selection_rationale_reconciliation.md`
- `docs/projection_integrity_summary_characterization.md`
- `docs/projection_integrity_drilldown_characterization.md`
- `docs/backlog_and_status_reconciliation.md`
- `docs/knowledge_classification_vocabulary.md`
- `docs/knowledge_lifecycle_reconciliation.md`
- `seed_runtime/context_views.py`
- `seed_runtime/explanations.py`
- `seed_runtime/capability_inventory.py`
- `seed_runtime/state_views.py`
- `seed_runtime/contradictions.py`
- `scripts/seed_local.py`

Additional response-formatting, inventory, summary, explanation, CLI, and output-related files inspected:

- `docs/why_not_explanation_characterization.md`
- `docs/why_not_vocabulary.md`
- `docs/state.md`
- `seed_runtime/runtime.py`
- `seed_runtime/models.py`
- `seed_runtime/decisions.py`
- `seed_runtime/evidence_graph.py`
- `seed_runtime/confidence.py`
- `seed_runtime/integrity_summary.py`

# What Is Response

Response is the concern responsible for communicating selected projected knowledge and its limits to a consumer. In Seed terms, Response includes:

- output construction for decisions that become user-visible runtime responses;
- communication of facts, evidence, explanations, contradictions, integrity signals, capability status, stale facts, graph issues, and summaries;
- formatting and presentation of read-only views through CLI surfaces;
- caveat and limitation communication when knowledge is unsupported, stale, contradicted, ambiguous, absent, or not actionable.


Response is not the same as Explainability. Explainability owns why-oriented provenance, support, evidence, and conflict explanation surfaces. Response owns how those outputs are communicated and presented. Current evidence supports the distinction, but no dedicated Response vocabulary exists to make it uniform.

Response is not the same as Selection. Selection chooses relevant knowledge for a decision or context. Response communicates the chosen knowledge, its rationale when available, and its limits.

Response is not the same as Integrity. Integrity characterizes unsupported, stale, conflicted, contradicted, graph-invalid, and capability-verification signals. Response communicates those signals through summaries, drill-down pointers, and CLI views.

# Existing Response Surfaces

## Runtime response envelopes

Runtime is the clearest behavior path for answer-like Response. It receives a validated `Decision`, appends response events for answer, question, and refusal decisions, and returns a `RuntimeResponse` envelope with `kind`, `message`, and optional `payload`. It also returns response envelopes for invalid decisions, recorded tool needs with recommendations, tool-call results delegated to `ToolExecutor`, state-patch results, and unsupported valid decisions.

Classification: **response surface** for runtime communication. Runtime is not a general Response owner; it routes decisions and delegates other behavior.

## Decision output shape


Classification: **data source and response precursor**. A `Decision` is not itself a final response until routed or formatted.

## Context packets

`ContextPacket` carries current input, active goal, entities, facts, tools, open tool needs, evidence, retry prompts, context budget trace, and decision schema to the decision model.

Classification: **data source / response-adjacent composition**. It can influence answer construction but is not a user-facing response surface by itself.

## Decision Context View


Classification: **response-adjacent surface** and **summary-like response surface** when printed. It is also a selection/composition artifact for decision-making.

## Explanation outputs

`ExplanationBuilder.why(subject, predicate)` returns structured current, ambiguous, or no-current-belief explanations with current beliefs, competing beliefs, recursive fact explanations, evidence IDs, source types, confidence values, inference metadata, entity resolution paths, and conflict metadata.

Classification: **explanation response surface**. It communicates why-oriented knowledge, but it remains an explanation surface rather than a full Response contract.

## Evidence Graph and fact explanation outputs

The Evidence Graph exposes evidence nodes, links, fact evidence views, unsupported fact views, and evidence summary counts. CLI formatters present `--evidence-graph`, `--why-fact`, and unsupported fact output.

Classification: **evidence/explanation response surfaces**. The graph itself is a read-only data source; formatted evidence and why-fact output are response surfaces.

## Capability explanations and inventories

Capability inventory derives registered/provider-reported/verified/unverified/stale/unknown capability entries from projected state and can be formatted as deterministic JSON. Capability views expose current capability-like entries from tool needs and registered tools.

Classification: **inventory response surface** when printed; **data source** when used as an input to integrity summary.

## Why-Not outputs

The repository has why-not characterization and vocabulary documents, but code inspection confirms no explicit `why_not()` API in `ExplanationBuilder`. Existing no-current-belief, unsupported, missing evidence, unverified capability, and capability resolution outputs are partial substitutes.

Classification: **partial / implicit response category**, not a unified implemented surface.

## Projection Integrity Summary output

`ProjectionIntegritySummary` aggregates unsupported facts, fact conflicts, contradictions, graph issues, stale facts, refresh recommendations, capability verification counts, caveats, projection version, and last event. The CLI formatter presents counts with drill-down references.

Classification: **integrity response surface** and **summary-like response composition**.

## Projection Integrity Navigation output

Integrity drill-down/navigation documentation characterizes how summary counts point to existing drill-down surfaces such as unsupported facts, fact conflicts, contradictions, graph issues, stale facts, refresh recommendations, and capability status.

Classification: **documented response composition/navigation**, implemented through existing CLI surfaces rather than a new engine.

## CLI output surfaces


Classification: **presentation/formatting response surfaces**.

## State summary output

State summary output communicates entity/fact/relationship/measurement/conflict/stale/graph-issue/source/top-entity/availability/filesystem counts.

Classification: **state response surface** when printed; **data source** when used by other summaries.

## Contradiction output

Contradiction Detection builds read-only contradiction records and summaries; CLI formatting presents counts, severity, reasons, values, facts, evidence, and supporting events.

Classification: **issue/integrity response surface**.

## Unsupported fact output

Unsupported fact output uses fact evidence views that have no supporting evidence.

Classification: **integrity/evidence response surface**.

## Graph issue output

Graph validation issues are formatted with severity, subject, relationship, object, reason, and hint.

Classification: **issue response surface**.

## Stale fact output

State methods and CLI surfaces expose stale facts and refresh recommendations. Integrity Summary counts those signals and points to drill-down commands.

Classification: **integrity response surface**.

# Existing Response Composition

Seed already composes response-like outputs in several places:

1. **Runtime path**: user input is appended, projected State is composed into a `ContextPacket`, the model returns a `Decision`, validation occurs, and Runtime routes the decision into `RuntimeResponse` envelopes or owner services. This is the answer/question/refusal response path.
2. **Context composition path**: `ContextComposer` orders goals, entities, facts, evidence, and open tool needs, applies a context budget, attaches selected evidence to facts, includes tools, and emits a decision schema. This composes selected knowledge for downstream decision output, not final user presentation.
4. **Explanation path**: `ExplanationBuilder.why` composes FactSupport, FactConflict, Fact records, evidence IDs, confidence, inference metadata, and entity resolution into a structured why response.
5. **Evidence path**: Evidence Graph builders compose evidence nodes, fact evidence views, unsupported facts, and summary counts; CLI formatters turn them into human-readable output.
6. **Integrity Summary path**: `build_projection_integrity_summary` composes existing integrity signals and capability inventory counts into a read-only summary with caveats and drill-down-oriented CLI formatting.
7. **State Views path**: State view builders compose projected State into fact, observation, requirement, capability, issue, and summary views; CLI formatters present them.
8. **CLI presentation path**: `scripts/seed_local.py` composes text sections, headings, counts, JSON, caveats, reasons, supporting events, and drill-down hints for terminal consumers.

Composition ownership is distributed by surface. There is no central Response composition owner.

# Existing Response Ownership

| Area | Current owner | Finding |
| --- | --- | --- |
| Runtime response routing | `Runtime` | Owns routing validated decisions into runtime envelopes and appending answer/question/refusal events. Does not own explanation, integrity, projection, tool execution, or CLI presentation. |
| Runtime response shape | `RuntimeResponse` | Minimal envelope of `kind`, `message`, and `payload`; not a full response contract. |
| Context composition | `ContextComposer` / context budget and selection helpers | Own decision-input context packets, not final response presentation. |
| Decision-ready context view | `context_views.py` | Owns deterministic context view composition from integrity/evidence/confidence/state sources. |
| Explanation composition | `ExplanationBuilder` | Owns why-oriented fact/belief explanation over projected State. |
| Evidence/fact explanation | `evidence_graph.py` plus CLI formatters | Owns evidence graph read models and fact evidence explanations. |
| Integrity aggregation | `integrity_summary.py` | Owns read-only aggregate integrity counts and caveats. |
| Integrity drill-downs | Existing state/evidence/contradiction/capability/stale surfaces | Ownership remains with source views; no new navigation engine. |
| State read-only views | `state_views.py` | Owns compact projected-state view builders. |
| Capability inventory | `capability_inventory.py` | Owns capability verification inventory interpretation. |
| Contradiction view | `contradictions.py` | Owns conservative read-only contradiction detection and summary. |
| CLI formatting/presentation | `scripts/seed_local.py` | Owns many terminal response surfaces and format-specific composition. |
| Communication channel | Runtime for application responses; CLI for local terminal output | No universal communication owner exists. |

# Existing Response Categories

| Category | Status | Evidence-backed finding |
| --- | --- | --- |
| Answer Response | Implemented | Runtime routes `answer` decisions to `RuntimeResponse(kind="answer")` and appends `response.answer`. |
| Question Response | Implemented | Runtime routes `ask_question` decisions to `RuntimeResponse(kind="question")` and appends `response.question`. |
| Refusal Response | Implemented | Runtime routes `refuse` decisions to `RuntimeResponse(kind="refusal")` and appends `response.refusal`. |
| Invalid Decision Response | Implemented | Runtime returns `invalid_decision` envelopes for parse/validation failures. |
| Tool Need / Capability Gap Response | Implemented/partial | Runtime returns recorded tool need, recommendations, and capability resolution; capability inventory/status output exists separately. |
| Tool Result Response | Implemented as delegated envelope | Runtime returns ToolExecutor result kind/message/payload but does not own tool behavior. |
| State Update Response | Implemented as state-patch envelope | Runtime returns `state_updated` or `invalid_state_patch`; state mutation belongs to state-patch service, not Response. |
| Explanation Response | Implemented/partial | `ExplanationBuilder.why` and `--why-fact` exist; no single response contract combines them. |
| Integrity Response | Implemented/partial | Integrity Summary and drill-down surfaces exist; no unified prose/composition policy. |
| Inventory Response | Implemented | Capability inventory and rule/inventory-like outputs are formatted/read-only. |
| Issue Response | Implemented | Graph issues, contradictions, unhealthy output, and issue views exist. |
| Capability Response | Implemented/partial | Capability views, capability inventory, capability status, and tool-need responses exist but have distinct semantics. |
| Why-Not Response | Partial/implicit | No explicit `why_not()` API; no-current-belief, unsupported, stale, unverified, and capability-resolution outputs partially answer negative questions. |
| State Response | Implemented | State summaries and state views exist. |
| Observation Response | Implemented/partial | Observation views and inventory diff/export surfaces exist; not a top-level Response contract. |
| Selection Rationale Response | Partial | Decision-context and context budget traces expose selected items/counts, but rationale communication remains partial. |
| Uncertainty Response | Implicit | Confidence, ambiguity, unsupported, stale, contradiction, and caveats exist, but no consistent response vocabulary joins them. |

# Existing Questions Already Answerable

Existing response surfaces can already answer:

- **What does Seed know?** State summaries, current fact views, fact support output, decision context views, and state views expose projected facts and counts.
- **Why does Seed know it?** `ExplanationBuilder.why`, Evidence Graph, `--why-fact`, fact support output, evidence IDs, source types, inference metadata, and supporting events answer fact-level why questions.
- **What conflicts exist?** Projection-level fact conflicts, contradiction output, confidence contradiction counts, and Integrity Summary expose conflict/contradiction signals.
- **What graph issues exist?** Graph issue output, issue views, unhealthy output, and Integrity Summary expose graph validation issues.
- **What capabilities exist?** Capability views, capability inventory, capability status, and tool registry-derived context packet tools expose capability information.
- **Which capabilities are verified, unverified, stale, unknown, or provider-reported?** Capability inventory and Integrity Summary capability counts answer this at inventory/summary level.
- **What facts are stale?** State stale-fact surfaces and Integrity Summary stale counts answer this.
- **Which facts are unsupported?** Evidence Graph unsupported fact views and Integrity Summary unsupported counts answer this.
- **Why was this fact contradicted?** Contradiction output gives conflicting values, facts, evidence, severity, reason, and supporting event IDs; confidence output also lists contradiction-related reasons.
- **Why was this selected for context?** Partially answerable through context budget traces and Decision Context View ordering/summaries, but explicit narrative selection rationale remains partial.

# Existing Questions Not Easily Answerable

Inspection supports these unanswered or not-easily-answerable Response questions:

- How should multiple explanation surfaces (`ExplanationBuilder.why`, `--why-fact`, Evidence Graph explanations, contradiction details, confidence reasons) be combined in one operator-facing answer?
- How should multiple integrity signals be communicated together when a fact is simultaneously stale, unsupported, contradicted, and associated with graph issues?
- How should conflicting rationale be presented when current/competing beliefs, contradictions, confidence penalties, and fact conflicts are all available but come from different surfaces?
- How should uncertainty be communicated consistently across answers, explanations, confidence summaries, integrity summaries, capability status, unsupported facts, stale facts, and no-current-belief cases?
- When should an answer include caveats from integrity signals, and which owner decides that inclusion?
- How should response formatting differ between runtime responses, CLI terminal output, deterministic JSON views, and future consumer-facing displays?
- Which response surface is canonical when state summary counts, integrity summary counts, context summary counts, and confidence summary counts overlap but measure different source structures?
- How should negative/why-not communication be composed without introducing a negative belief model or parallel truth system?
- How should selection rationale be communicated in final output, beyond selected context and budget traces?

These are vocabulary/composition questions, not evidence for a Response engine.

# Relationship To Explainability

Explainability owns why-oriented provenance and support. Repository docs and code show explainability surfaces over facts, support, evidence, conflicts, rules, capability status, stale facts, and graph issues. `ExplanationBuilder.why` explicitly builds deterministic explanations from projected State with current beliefs, competing beliefs, recursive facts, evidence IDs, source types, confidence values, inference metadata, entity resolution, and optional conflict.

Response owns communication and presentation of those explanation outputs. For example, CLI `format_why_fact` turns a `FactEvidenceView` into terminal text with headings, explanation text, evidence nodes, and supporting event IDs. That formatting is Response-like even though the source data is explainability-owned.

Validated distinction:

- Explainability answers: **Why is this known, believed, unsupported, stale, conflicted, inferred, or ambiguous?**
- Response answers: **How is that answer, explanation, caveat, or limitation communicated to a consumer?**

The distinction should not collapse. A Response Vocabulary may reference explanation outputs, but it should not replace Explanation Contract Vocabulary or create a new explanation engine.

# Relationship To Selection

Selection owns choosing relevant projected knowledge for a current decision or context. Context composition and selection-rationale documents characterize ordering, budgeting, selected facts/evidence/entities/tools, decision context, and rationale gaps.


Validated distinction:

- Selection chooses which projected knowledge and integrity signals are relevant.
- Response communicates selected knowledge, selected limitations, and selected rationale when available.

The audit supports this boundary. Context packets and Decision Context Views are response-adjacent because they shape future communication, but they are not final communication by themselves unless printed.

# Relationship To Integrity

Integrity owns characterization of projected knowledge health and limitations. Existing integrity surfaces include unsupported fact counts, fact conflicts, contradictions, graph issues, stale facts, refresh recommendations, capability verification states, confidence/contradiction signals, and caveats.

Response owns communication of those integrity signals. Integrity Summary already functions as a response surface by aggregating counts, caveats, projection metadata, and drill-down references. Contradiction, graph issue, unsupported fact, stale fact, and capability status formatters communicate integrity details.

Validated distinction:

- Integrity characterizes knowledge support, conflicts, staleness, graph validity, and verification signals.
- Response communicates those characterizations and their caveats.

Response should not resolve contradictions, refresh stale facts, verify capabilities, mutate projections, or assert truth.

# Existing Summary-Like Response Surfaces

Existing summary-like surfaces that already function as response composition include:

- **State Summary**: compact projected-world counts and top-level state presentation.
- **State View Summary**: counts for facts, observations, requirements, capabilities, issues, projection version, and last event.
- **Evidence Summary**: evidence nodes, linked facts, unsupported facts, confidence, projection metadata.
- **Contradiction Summary**: contradiction counts, affected fact counts, severity counts, projection metadata.
- **Confidence Summary**: fact count, support categories, unsupported/contradicted counts, average confidence, projection metadata.
- **Projection Integrity Summary**: aggregate integrity counts, capability verification counts, caveats, projection metadata, and drill-down references.
- **Capability Inventory**: deterministic JSON inventory of capability verification states.
- **Issue Views**: current graph/issue summaries with severity.
- **Decision Context View Summary**: included facts/issues and support categories in decision-ready JSON.
- **Explanation outputs**: current/competing belief summaries, evidence explanations, and supporting event lists.
- **Why-Not-like outputs**: no-current-belief, unsupported facts, unverified capability status, stale facts, and capability-resolution gaps, though not unified.

These are already response composition at local scope. They are not proof that a central Response Summary implementation is needed.

# Fragmentation Assessment

Response is **distributed and fragmented, with partial unification through repeated patterns**.

Evidence of distribution:

- Runtime owns decision-response routing and response envelopes.
- CLI owns terminal formatting and presentation.
- ExplanationBuilder owns why-query composition.
- Evidence Graph owns evidence/fact explanation views.
- Integrity Summary owns aggregate integrity composition.
- Contradictions, confidence, state views, capability inventory, and context views each own their own read-only outputs.

Evidence of partial unification:

- Many surfaces share projection metadata (`projection_version`, `last_event_id`).
- Many surfaces expose supporting event IDs, evidence IDs, confidence, status, severity, reason, summary, caveats, or counts.
- Integrity Summary already composes several integrity surfaces and points to drill-down commands.
- Decision Context View already composes facts, issues, requirements, capabilities, and summary counts from multiple knowledge layers.
- Explanation docs already found recurring concepts that could support a contract-like vocabulary.

Evidence of fragmentation:

- No canonical Response vocabulary defines answer, explanation, caveat, uncertainty, issue, inventory, summary, and presentation boundaries.
- CLI formatters duplicate presentation patterns without a shared Response contract.
- Runtime response envelopes are minimal and separate from explanation/integrity views.
- Explainability, integrity, confidence, contradiction, stale-fact, and capability status outputs use different status vocabularies.
- There is no single owner for how caveats should be included in final answers.

# Composition Opportunities

Documentation-only opportunities supported by findings:

1. **Response Vocabulary**: define Response, response surface, response source, response composition, response formatting, response presentation, caveat, answer, explanation response, integrity response, inventory response, issue response, state response, why-not-like response, and uncertainty communication.
2. **Response Reconciliation**: map Runtime, CLI, explainability, selection, and integrity ownership boundaries without adding behavior.
3. **Response Surface Inventory**: if needed later, catalog existing surfaces and formatters. This audit does not implement it.
4. **Response Summary Characterization**: only if operators need one entry point for existing summaries. Existing Integrity Summary and State Summary may already be sufficient.
5. **Cross-surface caveat guidance**: document when existing integrity/explanation caveats should be communicated, without changing Runtime.
6. **Why-Not communication characterization**: document how no-current-belief, unsupported, unverified, stale, and capability-gap outputs relate without creating a negative belief model.

No implementation is justified by this characterization alone.

# Rejection Criteria

Response implementation work should **not** occur when:

- existing response surfaces already answer the operator question;
- the change only renames existing surfaces;
- the change duplicates CLI formatters, summaries, inventories, or views;
- the need is vocabulary or ownership clarification rather than missing behavior;
- no concrete unanswered operator question exists;
- the proposed work requires Runtime integration by default;
- the proposed work requires ToolExecutor integration by default;
- the proposed work adds a parallel truth, evidence, integrity, selection, or explanation system;
- the proposed work mutates projections, appends events, verifies capabilities, executes refreshes, resolves contradictions, or calls providers merely to improve presentation;
- the proposed work creates a universal formatter before current consumers and categories are reconciled;
- the proposed work collapses Explainability, Selection, Integrity, and Response into one engine.

# Complexity Traps

- **ResponseEngine**: likely duplicates existing Runtime, CLI, explanation, integrity, and state-view composition while creating unclear ownership.
- **ReasoningEngine**: conflates response communication with deciding truth or reasoning over knowledge.
- **ContextEngine**: duplicates ContextComposer and Decision Context View instead of documenting boundaries.
- **SelectionEngine**: reopens already reconciled selection concerns and risks parallel selection rules.
- **IntegrityEngine**: duplicates Projection Integrity Summary, contradictions, graph issues, stale facts, confidence, and capability inventory.
- **Planner / WorkflowEngine**: confuses response composition with planning or orchestration.
- **LLM Response Layer**: risks adding prose generation as a truth or explanation layer rather than formatting existing read-only outputs.
- **Universal Formatter**: attractive but premature because runtime envelopes, CLI text, deterministic JSON, summaries, and explanations have different consumers and semantics.
- **ToolExecutor integration**: response formatting should not execute tools or couple presentation to operation execution.
- **Runtime integration as default**: many response surfaces are CLI/read-only audit views; forcing Runtime ownership would blur boundaries.
- **Parallel response systems**: a new response store/read model could drift from projected State, Evidence Graph, Integrity Summary, and CLI outputs.

# Recommended Next Step

Recommended outcome: **B. Response partially present**.

Justification:

- Response composition exists locally but is distributed across owners.
- Missing pieces are primarily vocabulary, cross-surface composition guidance, and ownership clarification.
- Major concepts are not missing enough to justify a Response engine or Runtime integration.
- More audit is not required before documenting a Response Vocabulary, but implementation remains unjustified until a concrete unanswered operator question requires it.

Safest next step: create **Response Vocabulary v1** or **Response Reconciliation** as documentation-only work. A Response Inventory may be useful later, but this characterization alone does not justify creating one.

# Non-Goals

This characterization does not:

- implement response behavior;
- implement response engines;
- implement adapters;
- implement inventories;
- implement read models;
- implement routes;
- implement schema classes;
- modify Runtime;
- modify ToolExecutor;
- modify EventLedger ownership;
- modify ProjectionStore ownership;
- mutate projections;
- append events;
- execute tools;
- call providers;
- verify capabilities;
- refresh stale facts;
- resolve contradictions;
- add a negative belief model;
- add an LLM response layer;
- create parallel truth systems.

# Conclusion


The repository evidence supports a narrow definition: **Response communicates selected projected knowledge, explanations, integrity signals, and limitations to a consumer.** Response does not create knowledge, choose truth, select context, mutate projections, execute tools, or own explainability/integrity semantics.

The main gap is not behavior. The main gap is a shared Response vocabulary and reconciliation of distributed composition and ownership. Implementation work should remain rejected unless a concrete operator question cannot be answered by existing surfaces plus documentation-level vocabulary/reconciliation.
