# Executive Summary

Response Vocabulary v1 defines the canonical language Seed uses when discussing
Response as a documentation-only concern.

In Seed, **Response is the communication of selected projected knowledge and its
limitations to a consumer**. Response may communicate facts, explanations,
contradictions, integrity signals, capabilities, observations, caveats,
uncertainty, rationale, issue status, and state summaries. It does not create
knowledge, determine truth, select context, verify capabilities, execute tools,
call providers, mutate projections, append events, or own Runtime behavior.

Repository findings support Response as already partially present and
intentionally distributed. Runtime decision routing, CLI output, explanation
outputs, Projection Integrity Summary, capability inventory, state views,
contradiction outputs, evidence outputs, issue outputs, observation outputs, and
Decision Context View already communicate knowledge. The gap is shared language,
not behavior.

This document does not implement response behavior. It does not add a
`ResponseEngine`, schema class, adapter, route, inventory, read model, formatter,
Runtime integration, ToolExecutor integration, projection mutation, event append,
or parallel response system.

# Purpose

The purpose of this document is to define stable vocabulary for Seed's Response
concern.

It serves the same role for Response that existing vocabulary documents serve for
their concerns:

- `docs/explanation_contract_vocabulary.md` for explainability;
- `docs/context_composition_vocabulary.md` for context composition;
- `docs/selection_rationale_vocabulary.md` for selection rationale;
- `docs/capability_verification_vocabulary.md` for capability verification;
- `docs/knowledge_classification_vocabulary.md` for knowledge classification.

The vocabulary is intended to:

- name existing response-producing and response-adjacent surfaces consistently;
- distinguish communication from acquisition, integrity characterization,
  selection, verification, execution, provider calls, and state mutation;
- provide response category terms for documentation and future reconciliation;
- preserve existing distributed ownership instead of creating a new owner;
- describe limitations, caveats, uncertainty, and metadata as first-class
  response language.

This is vocabulary only. It is not an implementation plan, schema contract,
runtime contract, API contract, or inventory.

# What Is Response

**Response is the communication of selected projected knowledge and its
limitations to a consumer.**

In Seed terms, Response communicates what existing projected and selected
knowledge can safely say to a consumer in a specific surface. It includes the
presentation of:

- facts and current-state claims;
- explanations and evidence;
- contradictions and graph issues;
- integrity signals such as unsupported, stale, unverified, contradicted, or
  ambiguous;
- capability inventory states and capability resolution outcomes;
- observations and observation-derived facts;
- caveats, limitations, uncertainty, and absence of current belief;
- selection rationale and why-not-like rationale when existing surfaces expose
  it;
- summaries, inventories, navigation pointers, and metadata.

Response is broader than answer generation. An answer is one category of
Response, but Seed also produces explanation responses, integrity responses,
inventory responses, issue responses, state responses, observation responses,
capability responses, why-not responses, and selection-rationale responses.

Response does **not**:

- create observations, evidence, facts, state, projections, or knowledge;
- determine truth or correctness;
- select current beliefs differently from existing projection/selection rules;
- perform context selection;
- execute tools or registered operations;
- call providers or model providers;
- verify capabilities;
- refresh stale facts;
- resolve contradictions;
- mutate `State`, projections, `ProjectionStore`, or event-ledger state;
- append events;
- own `Runtime`, `ToolExecutor`, `EventLedger`, or `ProjectionStore`;
- introduce a parallel truth, integrity, selection, or explanation system.

# Canonical Vocabulary

## Response

A **Response** is a communication artifact or surface output that presents
selected projected knowledge and its limitations to a consumer.

A Response may be human-readable text, deterministic JSON, a runtime response
envelope, a CLI output, a summary, an inventory view, an explanation, or a
navigation-oriented drill-down output. A Response is not a source of truth and is
not an execution path by itself.

## Response Surface

A **Response Surface** is a concrete place where Seed communicates knowledge to a
consumer.

Existing examples include CLI output from `scripts/seed_local.py`, runtime
`RuntimeResponse` envelopes, `ExplanationBuilder.why(...)` outputs, Projection
Integrity Summary output, capability inventory output, state-summary output,
issue output, evidence output, contradiction output, and Decision Context View
output.

A Response Surface may have local formatting and ownership. The vocabulary does
not require a single universal formatter.

## Response Composition

**Response Composition** is the local assembly of response content, signals,
limitations, caveats, and metadata for a surface.

Composition already exists in distributed forms: Runtime routes model decisions
into response envelopes; CLI functions format state, evidence, confidence,
contradictions, integrity summaries, and explanations; builders compose
explanation, inventory, summary, and context-view objects.

Response Composition is descriptive in this document. It does not imply a new
composition engine.

## Response Producer

A **Response Producer** is an existing component, function, or route that creates
or formats a response artifact.

Examples include `Runtime._route(...)`, `ExplanationBuilder`, inventory builders,
summary builders, state-view builders, contradiction builders, evidence graph
builders, context-view builders, and CLI formatter functions.

A Response Producer does not become owner of the knowledge it communicates.

## Response Consumer

A **Response Consumer** is the recipient or reader of a Response.

Examples include a user, CLI caller, HTTP/API caller, model consumer,
decision-making component, operator, or documentation/audit reader.

## Response Artifact

A **Response Artifact** is the concrete output produced by a surface.

Examples include a `RuntimeResponse`, an `Explanation`, a
`ProjectionIntegritySummary`, a `CapabilityInventoryEntry` list, a
or an issue/contradiction/evidence output.

## Response Category

A **Response Category** classifies a Response by communication purpose.

Canonical categories are defined in [Response Categories](#response-categories).
A category is documentation vocabulary, not a Python enum or schema class.

## Response Content

**Response Content** is the knowledge or information communicated by a Response.

Examples include facts, evidence IDs, supporting fact IDs, confidence values,
contradictions, graph issues, capability states, current-state summaries,
observation-derived facts, stale facts, refresh recommendations, selected
context facts, questions, refusals, recommendations, and event IDs when an
existing surface already exposes them.

## Response Limitation

A **Response Limitation** is a boundary on what the Response can claim.

Examples include unsupported evidence, stale data, no current belief, ambiguity,
contradiction, unverified capability state, provider-reported-but-not-verified
state, graph validation issues, missing inventory data, budgeted context, or
surface scope limits.

A limitation is not proof that a claim is false.

## Response Caveat

A **Response Caveat** is explicit consumer-facing language that prevents
over-claiming.

Examples include statements that integrity counts are not truth judgments, stale
facts are recommendations only, listener facts do not imply reachability, mount
facts do not imply health, and unverified capabilities are not necessarily
unavailable.

## Response Context

**Response Context** is the bounded situation in which a Response is produced and
interpreted.

Examples include current user input, active goals, selected context packet
sections, workspace/session identifiers, projection version, last event ID,
predicate/cardinality semantics, CLI flags, current state, and the consumer's
requested query.

## Response Scope

**Response Scope** is the declared boundary of what a Response covers.

Examples include one subject/predicate explanation, one capability inventory,
one workspace state summary, one decision context view, one list of graph
issues, one CLI command output, one runtime decision, or one projection-integrity
summary.

## Response Signal

A **Response Signal** is an existing projected or selected data point used as
communicated content or as a caveat.

Examples include confidence, support count, evidence count, contradiction
status, graph issue severity, capability verification state, stale status,
unsupported status, current/ambiguous/no-current-belief status, source type,
observed time, latest observed time, expiry time, projection version, and last
event ID.

## Response Status

A **Response Status** is the vocabulary used to describe implementation or
presence of a response surface or behavior.

Canonical status words are defined in
[Response Status Vocabulary](#response-status-vocabulary).

## Response Summary

A **Response Summary** is a compact response artifact that aggregates existing
read-only signals for a consumer.

Examples include Projection Integrity Summary, State Summary, Context Summary,
Evidence Summary, event summaries, observation summaries, and CLI one-line or
count-based outputs.

A summary should not change the meaning of the source signals it aggregates.

## Response Inventory

A **Response Inventory** is a catalog-like response artifact that lists known
items and their statuses.

Examples include Capability Inventory, rule inventory output, predicate catalog
output, current facts, unsupported facts, stale facts, graph issues, and
relationships output.

This document does not create a Response Inventory of response surfaces.

## Response Navigation

**Response Navigation** is response language that helps a consumer move from a
summary to supporting details.

Examples include counts paired with source categories, issue IDs, supporting fact
IDs, evidence IDs, contradiction related fact IDs, graph issue source fact IDs,
runtime trace IDs, and drill-down commands such as why, why-fact, fact-support,
confidence-fact, graph-issues, and integrity-summary.

## Response Explanation

A **Response Explanation** is an explanation artifact used as response content.

Examples include `ExplanationBuilder.why(...)`, fact explanations,
contradiction explanations, evidence graph outputs, capability verification
states, rule inventory descriptions, and why-not-like status explanations.

Response Explanation is part of Response when communicated to a consumer, but it
remains governed by explainability vocabulary and boundaries.

## Response Rationale

A **Response Rationale** is rationale communicated in a Response.

Examples include selection rationale for why content was included or excluded,
current-state rationale for why one support is current, capability-resolution
rationale, recommendation reasons, and why-not rationale for absent or
non-current beliefs.

Response Rationale communicates existing rationale; it does not select or decide
truth.

## Response Integrity Signal

A **Response Integrity Signal** is an integrity characterization included in a
Response.

Examples include unsupported facts, stale facts, refresh recommendations,
contradictions, fact conflicts, graph issues, confidence values, unverified
capabilities, unknown capabilities, provider-reported capabilities, and caveats
from Projection Integrity Summary.

Response can communicate integrity signals, but Response is not Integrity.

## Response Uncertainty

**Response Uncertainty** is communicated lack of certainty, completeness, support,
currentness, verification, or unambiguous selection.

Examples include `ambiguous`, `no_current_belief`, unsupported, stale,
contradicted, unverified, unknown, provider-reported-only, not inferred, not
selected, missing evidence, and surface-scope caveats.

Uncertainty is not the same as falsehood.

## Response Metadata

**Response Metadata** is non-primary information that helps interpret the
Response.

Examples include workspace ID, session ID, projection version, last event ID,
event IDs, causation ID, timestamps, source type, observed time, latest observed
time, expiry, CLI flag scope, query subject/predicate, output category, and
supporting identifiers.

## Response Extension

A **Response Extension** is surface-specific response content that does not fit
the shared vocabulary but is still useful to preserve.

Extensions keep surface-specific details local rather than flattening all
responses into a universal schema. Examples include runtime tool-need payloads,
capability resolution details, context-budget traces, action-plan legacy side
path output, and CLI-specific formatting.

# Response Categories

## Answer Response

An **Answer Response** directly answers a consumer's question or request using
selected knowledge. Runtime `answer` decisions and CLI prose-like summaries are
examples.

It differs from other categories because its primary purpose is to provide an
answer, not to explain support, enumerate inventory, or report integrity.

## Explanation Response

An **Explanation Response** communicates why a claim, belief, rule, conflict, or
status exists in the current read model.

Examples include `ExplanationBuilder.why(...)`, fact explanation output,
evidence graph output, confidence fact output, rule inventory output, and
runtime why trace output.

It differs from Answer Response because it foregrounds support, provenance,
status, and limits.

## Integrity Response

An **Integrity Response** communicates integrity characterization of projected
knowledge.

Examples include Projection Integrity Summary, contradictions output,
unsupported facts, stale facts, fact conflicts, graph issues, confidence output,
and refresh recommendations.

It differs from Explanation Response because its primary purpose is to report
trust/fitness signals rather than explain one claim.

## Inventory Response

An **Inventory Response** lists known items and their statuses.

Examples include Capability Inventory, rule inventory, predicate catalog,
inference catalog, current facts, relationships, entity types, stale facts, and
unsupported facts.

It differs from Summary Response because it enumerates items rather than only
aggregating counts.

## Issue Response

An **Issue Response** communicates problems, warnings, conflicts, or validation
issues.

Examples include graph issues, contradictions, fact conflicts, unhealthy/down
output, invalid-decision responses, invalid-state-patch responses, and parsing or
validation errors.

It differs from Integrity Response because it focuses on individual issues or
failures rather than broad integrity characterization.

## Capability Response

A **Capability Response** communicates capability knowledge, capability status,
or capability-gap handling.

Examples include Capability Inventory, tool-need runtime responses,
capability-resolution payloads, registered-provider state, verified/unverified
capability statuses, provider recommendations, and capability catalog output.

It differs from Inventory Response because its scope is capability-specific and
may include recommendations or capability gaps.

## State Response

A **State Response** communicates current projected State or a state-derived
summary.

Examples include State Summary, State View Summary, current facts, best fact,
fact supports, entity impact, relationships, entity types, and Decision Context
View.

It differs from Acquisition Response because it communicates projected current
state; it does not ingest or create knowledge.

## Observation Response

An **Observation Response** communicates observations, observation-derived facts,
or observation, diff, or export results.

Examples include observed fact summaries, verbose observation-derived fact
output, observation inventory diff output, exported observation JSON, and
observation source summaries.

It differs from State Response because it is about observed or imported inputs
and their derived facts rather than the whole current projection.

## Why-Not Response

A **Why-Not Response** communicates why Seed does not currently present,
believe, verify, select, or know something in a given surface.

Examples include no-current-belief and ambiguous explanation statuses, competing
belief output, unsupported facts, unverified or unknown capabilities, stale fact
recommendations, graph issue reasons, and selection-rationale exclusions.

It differs from Explanation Response because its question is negative or absent:
why not this claim, value, capability, or selected item?

## Selection Rationale Response

A **Selection Rationale Response** communicates why knowledge was selected,
excluded, ordered, treated as current, or dropped for a surface.

Examples include context-budget traces, decision context summaries, current-state
fact support output, best/current fact output, and selection-rationale documents.

It differs from Response itself because selection rationale is content within a
Response; it does not make selection decisions.

## Uncertainty Response

An **Uncertainty Response** communicates uncertainty, incompleteness, ambiguity,
staleness, lack of support, or limited scope.

Examples include `ambiguous`, `no_current_belief`, unsupported facts, stale facts,
unverified capabilities, unknown capabilities, caveats, and not-inferred
statements in impact outputs.

It differs from Issue Response because uncertainty may be normal and informative,
not necessarily an error or defect.

# Response Status Vocabulary

The following status words describe response surface presence or maturity in
architecture documentation. They are not runtime statuses.

## Implemented

**Implemented** means the repository contains an existing response surface or
producer that directly communicates the relevant content today.

Example: CLI integrity summary output is implemented because the repository has a
Projection Integrity Summary builder and CLI formatter.

## Partial

**Partial** means the repository contains some response behavior or content, but
not a complete or normalized surface for the whole category.

Example: why-not response is partial because existing surfaces communicate
no-current-belief, ambiguity, unsupported facts, stale facts, and unverified
capabilities, but there is no dedicated unified why-not response surface.

## Missing

**Missing** means repository evidence does not show a response surface for the
specific communication need.

Missing does not imply implementation is justified. It may justify only future
documentation or reconciliation.

## Implicit

**Implicit** means the behavior or communication exists as a byproduct of another
surface without being named as Response.

Example: Runtime `answer`, `question`, and `refusal` envelopes are response
behavior, even though there is no first-class Response vocabulary or owner.

## Unknown

**Unknown** means inspection did not establish whether a response surface exists
or how it should be classified.

Unknown should be used when repository findings are insufficient rather than when
a desired implementation is absent.

# Relationship To Existing Structures

Response vocabulary maps onto existing Seed structures without transferring
ownership.

| Vocabulary term | Existing repository concepts |
| --- | --- |
| Response Surface | CLI output, RuntimeResponse envelopes, Decision outputs, Explanation outputs, Integrity Summary, Capability Inventory, State Summary, Issue outputs, Observation outputs, Evidence Graph output, Decision Context View |
| Response Producer | `Runtime._route(...)`, `ExplanationBuilder`, `build_projection_integrity_summary(...)`, `build_capability_inventory(...)`, `build_state_summary(...)`, state-view builders, contradiction builders, evidence graph builders, context-view builders, CLI formatter functions |
| Response Consumer | User, CLI caller, local HTTP/API caller, operator, model consumer, decision-making code consuming context views, documentation/audit reader |
| Response Content | facts, evidence, supporting fact IDs, contradictions, capabilities, capability-resolution payloads, graph issues, stale facts, unsupported facts, confidence values, observations, requirements, current context facts, event IDs |
| Response Limitation | unsupported facts, stale facts, unverified capabilities, unknown capabilities, provider-reported-only capabilities, contradictions, graph issues, ambiguous/no-current-belief explanation status, context budget drops, surface scope |
| Response Caveat | Projection Integrity Summary caveats, CLI impact caveats that listener or mount facts do not imply health/reachability, verification caveats, no-execution caveats |
| Response Metadata | projection version, last event ID, workspace ID, session ID, event IDs, causation ID, observed/latest observed timestamps, source type, expiry, query subject/predicate |
| Response Navigation | evidence IDs, fact IDs, issue IDs, trace IDs, graph issue source facts, contradiction related facts, CLI drill-down commands |

Important existing structures:

- Runtime decisions define answer, question, tool request, tool call, state patch,
  and refusal decision shapes. Runtime routes those decisions to response
envelopes or delegated execution paths, but Runtime should not be promoted to a
universal Response owner.
  surfaces. They may be communicated as responses, but they are not Response
  engines.
- `ExplanationBuilder` produces explanation artifacts from projected `State`.
  These are response content when surfaced to consumers.
- `build_projection_integrity_summary(...)` composes read-only integrity counts
  and caveats. This is an Integrity Response surface, not a Response-owned
  integrity system.
- `build_capability_inventory(...)` produces capability inventory status from
  projected state and registered tools. It can be a Capability Response and
  Inventory Response.
- `state_views.py` produces current-state, observation, requirement, capability,
  issue, and summary views. These can be State, Observation, Capability, Issue,
  and Summary Responses.
- `scripts/seed_local.py` contains many CLI response surfaces and formatter
  functions. They are concrete existing Response Surfaces, not evidence for a
  universal formatter.

# Relationship To Explainability

Explainability answers: **Why?**

Response answers: **How is selected knowledge communicated?**

Explainability may be part of Response, but Response is broader than
Explainability. Explanation artifacts communicate support, provenance,
contradictions, temporal context, capability status, rules, or limitations. When
those artifacts are presented to a consumer, they are Response content. However,
explainability vocabulary continues to own explanation semantics such as claim,
subject, supporting facts, supporting evidence, conflict, provenance, temporal
context, caveats, and extensions.

Repository findings validate this boundary:

- `ExplanationBuilder.why(...)` builds deterministic explanations from projected
  `State` and reports statuses such as current, ambiguous, and no current belief.
- CLI `--why`, `--why-fact`, evidence, confidence, and rule inventory outputs
  communicate explanation-like artifacts.
- Explainability audits and reconciliation reject treating explanations as truth
  selection, verification, execution, Runtime ownership, or ToolExecutor
  ownership.

Therefore:

- Explainability can supply Response Content, Response Explanation, Response
  Rationale, Response Caveats, and Response Uncertainty.
- Response must not replace explainability vocabulary or create a separate
  explanation engine.
- Response must not use explanation output to decide truth differently from
  projected state.

# Relationship To Selection

Selection chooses knowledge.

Response communicates selected knowledge.

Selection does not become Response, and Response does not perform selection.

Existing selection structures include context composition, context budgets,
context ordering helpers, current/best fact selection, capability inventory
universe and status ranking, and decision context views. Response may present the
results of those selections and may communicate selection rationale when it
already exists, but it must not introduce new selection rules.

Boundary rules:

- Selection determines which candidates, facts, evidence, requirements,
  capabilities, issues, or context sections matter for a surface.
- Response communicates those selected candidates and their limitations.
- Response can include a Selection Rationale Response.
- Response cannot re-rank, re-select, or override selection semantics.
- Response cannot treat excluded candidates as false merely because they were not
  selected.

# Relationship To Integrity

Integrity characterizes knowledge.

Response communicates integrity.

Integrity signals may be Response Content, Response Signals, Response
Limitations, Response Caveats, and Response Uncertainty. Examples include
unsupported facts, fact conflicts, contradictions, graph issues, stale facts,
refresh recommendations, confidence values, and capability verification states.

Response is not Integrity. It does not compute truth, repair state, verify
capabilities, resolve contradictions, refresh facts, or mutate projections.

Existing integrity structures such as Projection Integrity Summary,
contradictions, graph issues, evidence summaries, confidence aggregation, stale
fact recommendations, and capability inventory retain their source semantics.
Response can present them, aggregate them locally, or point to drill-down
surfaces, but it must not change their meaning.

# Relationship To Acquisition

Acquisition creates knowledge.

Response communicates knowledge.

Knowledge Acquisition includes observations, evidence, fact extraction,
observation-derived facts, imported/provider/discovery/user source metadata, and
projection inputs. Response may report observations and observation-derived facts
or summarize ingestion results, but it does not acquire knowledge.

Boundary rules:

- Response does not observe the world.
- Response does not create Evidence or Facts.
- Response does not append observation, evidence, or fact events.
- Response does not call provider/discovery sources.
- Response may communicate acquisition provenance such as source type, evidence
  IDs, observed time, and imported/discovery context.

# Existing Response Surfaces

The following classifications are documentation vocabulary over existing
surfaces. A surface may belong to more than one category.

| Existing surface | Response categories | Notes |
| --- | --- | --- |
| Runtime `answer` response | Answer Response | Communicates direct answer text from an answer decision. |
| Runtime `ask_question` response | Answer Response, Uncertainty Response | Communicates a question when more input is needed. |
| Runtime `refuse` response | Issue Response, Uncertainty Response | Communicates refusal reason and boundary. |
| Runtime `tool_need` response | Capability Response, Issue Response | Communicates a capability gap, recommendations, and capability resolution without executing the requested capability. |
| Runtime `tool_result` response | Answer Response, State/Execution-adjacent Response | Communicates ToolExecutor result after the explicit `call_tool` path; Response vocabulary does not change execution ownership. |
| Runtime `invalid_decision` / parse failure responses | Issue Response | Communicate validation or parse errors. |
| Runtime `state_updated` / `invalid_state_patch` responses | State Response, Issue Response | Existing runtime behavior; this vocabulary does not add state mutation. |
| CLI normal message output | Answer Response | Formats `RuntimeResponse` summary and optional events. |
| CLI events output | Inventory Response, Response Navigation | Lists event summaries for debugging/history. |
| CLI `--why` output | Explanation Response, Why-Not Response, Uncertainty Response | Communicates current, ambiguous, and no-current-belief explanations. |
| CLI `--why-fact` output | Explanation Response | Communicates evidence/support for facts. |
| CLI `--evidence` output | Explanation Response, Inventory Response | Communicates Evidence Graph summary and linked evidence. |
| CLI `--contradictions` output | Integrity Response, Issue Response, Explanation Response | Communicates read-only contradictions and supporting facts/evidence. |
| CLI `--confidence` / `--confidence-fact` output | Integrity Response, Explanation Response, Uncertainty Response | Communicates confidence/support signals. |
| CLI `--unsupported-facts` output | Integrity Response, Inventory Response, Uncertainty Response | Communicates unsupported projected facts. |
| CLI `--stale-facts` / refresh recommendations | Integrity Response, Inventory Response, Why-Not Response | Communicates stale facts and recommendation signals only. |
| CLI `--graph-issues` output | Issue Response, Integrity Response | Communicates graph validation issues. |
| CLI `--unhealthy` output | Issue Response, State Response | Communicates projected down endpoints and graph errors without executing checks. |
| CLI `--state-build` output | State Response, Response Summary | Communicates read-only projected world-model summary. |
| CLI `--integrity-summary` output | Integrity Response, Response Summary | Communicates Projection Integrity Summary counts and caveats. |
| CLI `--capabilities` / capability inventory output | Capability Response, Inventory Response, Integrity Response | Communicates capability verification states. |
| CLI `--relationships` output | State Response, Inventory Response | Communicates projected topology relationships. |
| CLI `--entity-types` output | State Response, Inventory Response | Communicates current entity type assertions. |
| CLI `--impact` output | State Response, Uncertainty Response | Communicates entity impact and caveats about not inferring health/reachability. |
| CLI observation outputs | Observation Response, State Response | Communicate observation-derived facts or observation inventory diffs. |
| `ExplanationBuilder.why(...)` | Explanation Response, Why-Not Response, Uncertainty Response | Produces explanation artifacts from projected state. |
| `build_projection_integrity_summary(...)` | Integrity Response, Response Summary | Aggregates existing integrity signals and caveats. |
| `build_capability_inventory(...)` | Capability Response, Inventory Response, Integrity Response | Lists registered/provider capability states derived from projected state. |
| `build_state_summary(...)` and state views | State Response, Response Summary, Inventory Response, Issue Response | Expose facts, observations, requirements, capabilities, issues, and summary. |

# Proposed Vocabulary Shape

The proposed documentation shape for describing a Response is:

```text
Response
  surface
  category
  producer
  consumer
  artifact
  content
  context
  scope
  signals
  limitations
  caveats
  uncertainty
  rationale
  metadata
  navigation
  extensions
```

This shape is documentation only.

It is not:

- an implementation;
- a schema class;
- a runtime contract;
- a persistence model;
- a read model;
- an adapter interface;
- an API route;
- a universal formatter;
- an event payload contract.

Surface-specific fields should remain local extensions unless future
reconciliation proves a shared contract is needed.

# Complexity Traps

## ResponseEngine

A `ResponseEngine` is a trap because existing response behavior is distributed
across Runtime envelopes, CLI formatters, explanation builders, integrity
summaries, state views, capability inventories, evidence outputs, contradiction
outputs, and context views. A new engine would likely duplicate existing owners
and blur boundaries.

## ReasoningEngine

A `ReasoningEngine` is a trap because Response communicates selected knowledge;
it does not determine truth, infer new knowledge, or reason over the world as a
new authority.

## ContextEngine

A `ContextEngine` is a trap because context composition and selection already
have vocabulary and implementation boundaries. Response may communicate selected
context, but it must not own context selection.

## Planner / WorkflowEngine

Planner and WorkflowEngine concepts are traps because response composition is
not planning, orchestration, provider handoff, long-running workflow management,
or execution scheduling.

## Universal Formatter

A Universal Formatter is a trap because existing surfaces have different
consumers and semantics: runtime envelopes, CLI text, deterministic JSON,
integrity counts, explanation trees, inventories, and summaries do not require a
single owner before their categories and boundaries are reconciled.

## Runtime Integration As Default

Default Runtime integration is a trap because many Response Surfaces are
read-only CLI/audit/view outputs outside runtime message handling. Forcing
Runtime ownership would collapse distributed documentation, explainability,
selection, and integrity surfaces into one route.

## ToolExecutor Integration As Default

ToolExecutor integration is a trap because Response should not execute tools,
verify capabilities, refresh data, or couple presentation to registered
operation execution. Existing execution ownership belongs to the explicit tool
call path.

## EventLedger Or ProjectionStore Ownership

Giving Response EventLedger or ProjectionStore ownership is a trap because
Response should not append events, mutate projections, or own persistence.
Response may include existing event IDs or projection metadata only when already
provided by a surface.

## Parallel Response Systems

A parallel response store, read model, schema hierarchy, or truth layer is a trap
because it could drift from State, Evidence Graph, Integrity Summary, Context
Views, Explanation outputs, and CLI surfaces.

# Non-Goals

This document does not:

- implement response behavior;
- implement response composition;
- implement response inventories;
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
- call providers;
- execute tools;
- verify capabilities;
- refresh stale facts;
- resolve contradictions;
- create a ResponseEngine, ReasoningEngine, ContextEngine, Planner,
  WorkflowEngine, Universal Formatter, or parallel response system;
- create a runtime contract, schema contract, or API contract.

# Future Work

Future work should remain documentation-oriented unless a separate, concrete
operator question proves that existing surfaces cannot answer it.

Supported documentation-oriented follow-ups:

1. **Response Reconciliation**: map distributed Response ownership across
   Runtime, CLI, explanations, integrity, selection, capability, state, and
   observation surfaces without changing behavior.
2. **Response Inventory Characterization**: characterize whether an inventory of
   existing response surfaces is useful. This would be a documentation audit, not
   a new read model.
3. **Response Summary Characterization**: evaluate whether existing summaries
   are sufficient or whether documentation should describe summary relationships.
4. **Cross-surface Caveat Guidance**: document when existing caveats and
   limitations should be surfaced together, without changing Runtime or
   ToolExecutor behavior.
5. **Why-Not Response Reconciliation**: document how no-current-belief,
   ambiguity, unsupported, stale, unverified, unknown, and non-selected outputs
   relate without creating a negative belief model.
6. **Response Surface Classification Maintenance**: keep the classification in
   this vocabulary aligned with future documentation audits.

Future work should not recommend engines, runtime integration, ToolExecutor
integration, adapters, routes, schema classes, projection mutation, event appends,
provider calls, or a parallel response system by default.
