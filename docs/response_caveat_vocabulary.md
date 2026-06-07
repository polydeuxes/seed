# Executive Summary

Response Caveat Vocabulary v1 defines the canonical language Seed uses when
naming, comparing, and documenting caveats.

In Seed, a **Caveat** is a communicated limitation, qualification, warning,
uncertainty marker, status qualifier, or non-guarantee attached to projected,
selected, explained, characterized, or communicated knowledge. Caveats are
already partially present across integrity summaries, integrity navigation,
explanation outputs, capability verification inventory, confidence outputs,
state views, issue views, contradiction outputs, decision context views, CLI
formatters, and runtime response envelopes.

This document names existing caveat concepts. It does not implement caveats,
caveat summaries, caveat inventories, caveat navigation, caveat contracts,
caveat aggregation, read models, routes, adapters, schema classes, runtime
behavior, provider behavior, projection mutation, or event appends.

The architecture finding is consistent with the rest of Seed's documentation:
behavior exists, vocabulary is missing, composition is fragmented, ownership is
distributed, and a new engine is not justified. Integrity produces many
caveat-generating conditions. Explainability may explain caveats. Selection may
use caveat-producing signals. Response communicates caveats. None of those
relationships require a `CaveatEngine`, `ResponseEngine`, `ReasoningEngine`,
`ContextEngine`, planner, workflow engine, universal caveat layer, universal
formatter, Runtime integration, ToolExecutor integration, or a parallel caveat
system.

# Purpose

The purpose of this document is to define stable vocabulary for Seed's Response
Caveat concern.

It serves the same role for caveats that existing vocabulary documents serve for
their concerns:

- `docs/response_vocabulary.md` for Response;
- `docs/selection_rationale_vocabulary.md` for selection rationale;
- `docs/explanation_contract_vocabulary.md` for explanation contracts;
- `docs/context_composition_vocabulary.md` for context composition;
- `docs/capability_verification_vocabulary.md` for capability verification;
- `docs/knowledge_classification_vocabulary.md` for knowledge classification.

The vocabulary is intended to:

- name existing caveat-producing signals consistently;
- distinguish caveat communication from truth, verification, selection,
  execution, provider calls, and state mutation;
- map caveat terms to existing repository structures;
- preserve distributed ownership instead of creating a new owner;
- provide common terms for future documentation-only reconciliation work.

This is vocabulary only. It is not an implementation plan, schema contract,
runtime contract, API contract, response contract, inventory, navigation model,
read model, or aggregation model.

# What Is A Caveat

**A Caveat is a communicated limitation, qualification, warning, uncertainty
marker, status qualifier, or non-guarantee attached to projected, selected,
explained, characterized, or communicated knowledge.**

In Seed terms, a Caveat tells a consumer how not to over-read a fact, summary,
explanation, capability status, selection result, state view, response, or CLI
output. A Caveat can say that a claim is unsupported, contradicted, conflicted,
stale, expired, ambiguous, unverified, unknown, evidence-limited,
confidence-limited, graph-invalid, observation-limited, rationale-limited,
response-limited, runtime-limited, or read-only.

A Caveat may originate from:

- **Integrity** signals such as unsupported facts, fact conflicts,
  contradictions, graph issues, stale facts, and refresh recommendations;
- **Evidence** signals such as missing evidence, linked evidence, source type,
  provenance, and support limitations;
- **Confidence** signals such as support count, calculated confidence,
  unsupported status, contradicted status, and reasons;
- **Capability status** signals such as verified, unverified, stale,
  provider-reported, and unknown capability states;
- **Temporal status** signals such as `observed_at`, `latest_observed_at`,
  `expires_at`, `expired`, current-sample semantics, and stale facts;
- **Observation status** signals such as observation source, local observation
  status, and observation-derived fact summaries;
- **Selection status** signals such as included, excluded, priority-limited,
  budget-limited, unsupported-excluded, and decision-context admission;
- **Response limitations** such as no-current-belief, ambiguous explanation
  status, invalid decision envelopes, read-only CLI output, and runtime response
  envelope limitations.

A Caveat does **not**:

- create observations, evidence, facts, projections, state, or knowledge;
- determine truth, correctness, reliability, availability, safety, or health;
- resolve contradictions or fact conflicts;
- verify capabilities;
- refresh stale facts;
- select current beliefs differently from existing projection and selection
  behavior;
- execute tools or registered operations;
- call providers or model providers;
- mutate `State`, projections, `ProjectionStore`, or event-ledger state;
- append events;
- own `Runtime`, `ToolExecutor`, `EventLedger`, or `ProjectionStore`;
- introduce a parallel truth, response, selection, explanation, integrity, or
  caveat system.

# Canonical Vocabulary

## Caveat

A **Caveat** is a communicated limitation, qualification, warning, uncertainty
marker, status qualifier, or non-guarantee attached to projected, selected,
explained, characterized, or communicated knowledge.

A Caveat is not a fact, event, tool call, provider call, truth judgment, or
execution decision.

## Caveat Source

A **Caveat Source** is the existing structure or concern from which a
caveat-producing condition originates.

Examples include projected `State`, `FactSupport`, `FactConflict`,
`Contradiction`, `EvidenceSummary`, `FactEvidenceView`, `FactConfidence`,
`CapabilityInventoryEntry`, `GraphValidationIssue`, `Explanation`,
`DecisionContextView`, `ProjectionIntegritySummary`, CLI formatters, and runtime
response envelopes.

A Caveat Source owns its local semantics. This vocabulary does not transfer
ownership to a universal caveat layer.

## Caveat Signal

A **Caveat Signal** is an existing value, count, flag, status, reason, or
metadata field that can generate caveat language.

Examples include `unsupported_fact_count`, `expired`, `expires_at`,
`contradicted`, `unsupported`, `support_count`, `confidence`,
`contradiction_count`, `graph_issue_count`, `severity`, `reason`,
`verification state`, `status`, `no_current_belief`, `ambiguous`,
`last_event_id`, and `projection_version`.

A Caveat Signal is not itself a new caveat object unless a future document
explicitly defines such a representation.

## Caveat Surface

A **Caveat Surface** is a concrete place where Seed communicates caveat
information to a consumer.

Examples include Projection Integrity Summary output, Integrity Navigation
outputs, explanation output, capability inventory output, state view output,
issue view output, contradiction output, confidence output, Decision Context
View output, CLI formatted text or JSON, and runtime response envelopes.

A Caveat Surface may communicate caveats directly, implicitly, partially, or as
metadata.

## Caveat Producer

A **Caveat Producer** is an existing component, function, or projection-backed
view that produces caveat signals or caveat-bearing output.

Examples include `build_projection_integrity_summary`,
`build_contradictions`, `build_fact_confidences`, `build_capability_inventory`,
`build_state_summary`, `build_issue_view`, `build_decision_context_view`,
`ExplanationBuilder.why`, and CLI formatters.

A Caveat Producer is not a new engine. It is an existing owner of existing
output.

## Caveat Consumer

A **Caveat Consumer** is a human, operator, CLI user, model-context consumer,
response surface, documentation reader, or downstream component that reads or
uses caveat-bearing output.

A Caveat Consumer may use caveats for interpretation, display, selection, or
explanation. Consumption does not grant authority to mutate state, verify
capabilities, execute refreshes, or resolve conflicts.

## Caveat Category

A **Caveat Category** is a stable documentation label for the kind of limitation
being communicated.

Canonical categories in v1 are Integrity, Evidence, Capability, Temporal,
Confidence, Selection, Observation, Response, Graph, Rationale, and Unknown.

## Caveat Status

A **Caveat Status** describes how explicit or complete caveat support is in an
existing surface.

Canonical status terms in v1 are Implemented, Partial, Missing, Implicit, and
Unknown.

## Caveat Scope

A **Caveat Scope** is the thing the caveat qualifies.

Common scopes include response, answer, fact, current belief, competing belief,
capability, evidence, observation, contradiction, graph issue, selection result,
context entry, summary, CLI output, runtime envelope, projection, and document.

Scope prevents a caveat about one fact from being mistaken for a caveat about an
entire response or capability.

## Caveat Limitation

A **Caveat Limitation** is caveat language that states a boundary of what Seed
can claim or do.

Examples include no provider was called, no tool was executed, no verification
was performed, no refresh was executed, a read-only view was used, evidence is
missing, confidence is low, and a response envelope does not prove task success.

## Caveat Qualification

A **Caveat Qualification** is caveat language that narrows a claim without
necessarily warning of a problem.

Examples include projection-backed, current-sample, observation-derived,
provider-reported, read-only, as-of a timestamp, latest observed at a timestamp,
or based on selected context only.

## Caveat Warning

A **Caveat Warning** is caveat language that calls attention to a risk of
over-reading or acting on a claim.

Examples include unsupported, contradicted, conflicted, stale, expired,
ambiguous, graph-invalid, unverified, unknown, missing evidence, and runtime
invalid-decision status.

## Caveat Uncertainty

A **Caveat Uncertainty** is caveat language that communicates ambiguity,
incomplete support, unknown status, confidence limitations, or no-current-belief
conditions.

Uncertainty does not mean false. It means Seed has not projected or selected a
stronger statement under existing evidence and rules.

## Caveat Metadata

**Caveat Metadata** is existing supporting information that helps interpret a
caveat.

Examples include source IDs, fact IDs, evidence IDs, supporting event IDs,
`observed_at`, `latest_observed_at`, `expires_at`, `age_seconds`,
`projection_version`, `last_event_id`, support counts, confidence values,
severity, reason, source types, and entity-resolution paths.

Metadata is explanatory context. It is not a new truth system.

## Caveat Communication

**Caveat Communication** is the act of presenting caveat information on a
response surface.

Response surfaces already communicate caveats in distributed ways: explicit
`caveats` lists, status fields, reason fields, summary counts, formatted CLI
sections, JSON output, and runtime envelope kinds/messages.

Caveat Communication may be direct or indirect. It does not imply a single
universal formatter.

## Caveat Aggregation

**Caveat Aggregation** is the conceptual grouping of multiple caveat signals for
a larger scope, such as a response, answer, capability, or summary.

In v1 this is vocabulary only. Seed already has limited aggregation in
Projection Integrity Summary counts and CLI summaries, but this document does
not implement a general caveat aggregator, caveat inventory, caveat contract, or
answer-level caveat rollup.

## Caveat Extension

A **Caveat Extension** is future documentation vocabulary that names an
additional caveat category, status, metadata convention, surface mapping, or
communication pattern.

Extensions must preserve existing ownership, remain read-only unless separately
justified, and avoid becoming engines, routes, adapters, schema classes, runtime
contracts, or projection mutations.

# Caveat Categories

## Integrity Caveat

An **Integrity Caveat** communicates that projected knowledge has an integrity
condition that limits how it should be interpreted.

Examples include unsupported facts, fact conflicts, contradictions, graph issues,
stale facts, refresh recommendations, unverified capability counts, stale
capability counts, unknown capability counts, and summary caveats.

Integrity Caveats are about projected knowledge quality and safety of reliance.
They are not truth judgments and do not repair knowledge.

## Evidence Caveat

An **Evidence Caveat** communicates that support, provenance, or evidence linkage
is missing, limited, indirect, or otherwise relevant to interpretation.

Examples include unsupported facts, no evidence linked to a fact, evidence
source type, evidence confidence, evidence summary counts, and supporting event
IDs.

Evidence Caveats are about what supports a claim. They differ from Confidence
Caveats because confidence is a calculated/support estimate, while evidence is
the supporting material and provenance.

## Capability Caveat

A **Capability Caveat** communicates a limitation or status qualification about a
capability.

Examples include verified, unverified, stale, provider-reported, unknown,
registered-only, requested, candidate, recommended, and no `capability_verified`
fact present.

Capability Caveats are not execution permission, provider availability, tool
success, or automatic verification.

## Temporal Caveat

A **Temporal Caveat** communicates freshness, staleness, expiry, observation
time, current-sample semantics, or as-of limits.

Examples include `observed_at`, `latest_observed_at`, `expires_at`, `expired`,
stale facts, stale capability verification facts, current sample support, and
refresh recommendations.

Temporal Caveats differ from Integrity Caveats by focusing on time. They may
also be Integrity Caveats when staleness affects reliance.

## Confidence Caveat

A **Confidence Caveat** communicates confidence, support strength, contradiction
impact, unsupported status, or reasons that limit confidence.

Examples include confidence values, support count, strongly supported count,
weakly supported count, unsupported count, contradicted count, and confidence
reasons.

Confidence Caveats are estimates over support. They do not prove truth or
correctness.

## Selection Caveat

A **Selection Caveat** communicates that knowledge was included, excluded,
ordered, or limited by a selection surface.

Examples include Decision Context View admission, unsupported facts excluded by
default, context fact ordering by support/confidence, context budget or priority
limits documented in selection-rationale vocabulary, and rationale limitations.

Selection Caveats are about what was made available to a response or decision
context. They are not truth judgments.

## Observation Caveat

An **Observation Caveat** communicates limits of an observation or
observation-derived fact.

Examples include source type, observation confidence, local observation status,
observation timestamp, observation-derived fact summaries, and the fact that a
local marker does not imply availability, health, reachability, authorization,
or management authority.

Observation Caveats are about what was seen. They are not broader conclusions.

## Response Caveat

A **Response Caveat** communicates limits of a response surface or answer.

Examples include runtime response kind/message, invalid decision status, missing
or non-matching fact responses, no-current-belief explanation status, ambiguous
explanation status, read-only CLI output, and statements that a summary does not
execute tools or mutate state.

Response Caveats are about communication. They may communicate signals produced
elsewhere, but Response does not necessarily generate those signals.

## Graph Caveat

A **Graph Caveat** communicates relationship, type, shape, or graph-validation
issues.

Examples include `GraphValidationIssue`, issue severity, issue summary,
relationship IDs, source fact IDs, graph issue counts, and graph issue CLI
output.

Graph Caveats are about structural validity and relationship interpretation.
They are not fact truth, graph repair, or topology management.

## Rationale Caveat

A **Rationale Caveat** communicates that the explanation, why-not rationale,
selection rationale, or decision context rationale is partial, missing,
implicit, or limited by available projected knowledge.

Examples include missing rationale fields, implicit selection ordering, no
single answer-level caveat rollup, and explanation statuses such as ambiguous or
no-current-belief.

Rationale Caveats are about reasons and explanation completeness. They are not a
new reasoning system.

## Unknown Caveat

An **Unknown Caveat** communicates that Seed cannot classify, verify, support, or
answer a status more specifically using current projected knowledge and existing
surfaces.

Examples include unknown capability state, no-current-belief, missing evidence,
unknown availability in state summaries, and documentation gaps where a caveat
surface has not been characterized.

Unknown does not mean false. It means the existing projection or surface does
not provide a stronger known status.

# Caveat Status Vocabulary

## Implemented

**Implemented** means a caveat signal or caveat communication exists explicitly
in current repository behavior or documentation.

Examples include Projection Integrity Summary `caveats`, unsupported fact
counts, contradiction outputs, confidence unsupported/contradicted flags,
capability verification states, stale fact counts, graph issue output, and
explanation statuses.

Implemented does not mean universally composed across all response surfaces.

## Partial

**Partial** means some signals or communication exist, but the surface does not
answer all relevant operator questions or does not compose caveats consistently
across scopes.

Examples include caveat communication overall, answer-level caveats,
capability-level caveat communication, rationale caveats, and multi-caveat
communication.

Partial is the main finding for Response Caveats in v1.

## Missing

**Missing** means the repository does not currently expose a named vocabulary,
surface, or documentation artifact for a caveat concept.

Missing vocabulary does not by itself justify implementation. It may justify
future documentation-only characterization or reconciliation.

## Implicit

**Implicit** means caveat information is present as status fields, flags, counts,
reasons, timestamps, or metadata, but is not labeled as a caveat on that surface.

Examples include `unsupported=True`, `state="unverified"`,
`status="ambiguous"`, `expires_at`, `severity`, `support_count=0`, and
`include_unsupported=False` selection behavior.

Implicit caveats often motivate vocabulary documents before implementation.

## Unknown

**Unknown** means current documentation or inspection cannot determine whether a
caveat signal or surface exists, or the existing surface uses a domain status
whose caveat implication has not been characterized.

Unknown should be used sparingly and should lead to documentation inspection,
not speculation or implementation.

# Relationship To Existing Structures

This vocabulary maps to existing repository structures as follows.

| Vocabulary term | Existing concepts | Caveat categories |
| --- | --- | --- |
| Caveat Source | `State`, `Fact`, `FactSupport`, `FactConflict`, `EvidenceSummary`, `FactEvidenceView`, `Contradiction`, `FactConfidence`, `CapabilityInventoryEntry`, `GraphValidationIssue`, `Explanation`, `DecisionContextView`, `ProjectionIntegritySummary`, CLI output, runtime envelopes | All |
| Caveat Signal | `unsupported`, `contradicted`, `conflicted`, `expired`, `expires_at`, `stale`, `confidence`, `support_count`, `reason`, `severity`, `status`, `state`, `projection_version`, `last_event_id` | All |
| Caveat Surface | Projection Integrity Summary, Integrity Navigation/CLI drill-downs, Explanation outputs, Capability Inventory, State Views, Issue Views, Contradiction outputs, Confidence outputs, Decision Context View, CLI outputs, runtime response envelopes | All |
| Integrity Caveat | unsupported facts, fact conflicts, contradictions, graph issues, stale facts, refresh recommendations, integrity summary caveats | Integrity, Evidence, Graph, Temporal |
| Evidence Caveat | missing evidence, no linked evidence, unsupported fact views, evidence source type, source event IDs, support limitations | Evidence, Confidence |
| Capability Caveat | verification status, capability inventory state, registered tools, ToolNeeds, provider-reported capabilities | Capability |
| Temporal Caveat | stale facts, `expired`, `expires_at`, `observed_at`, `latest_observed_at`, `age_seconds`, current-sample semantics | Temporal |
| Confidence Caveat | `FactConfidence`, confidence summary, support count, unsupported flag, contradicted flag, reasons | Confidence, Evidence, Integrity |
| Selection Caveat | Decision Context View fact admission, unsupported facts excluded by default, context summary counts, selection rationale vocabulary | Selection, Confidence |
| Observation Caveat | observation source type, observed fact confidence, local observation status, observation-derived fact summaries | Observation, Temporal, Evidence |
| Response Caveat | runtime response kind/message, CLI read-only output, no matching fact messages, no-current-belief, ambiguous, invalid decision | Response, Rationale |
| Graph Caveat | `GraphValidationIssue`, issue views, graph issue counts, graph issue severity, relationship/source fact IDs | Graph, Integrity |
| Rationale Caveat | explanation status, competing beliefs, conflict attachment, reason fields, missing rationale fields, why-not and selection-rationale limits | Rationale, Response |
| Unknown Caveat | unknown capability inventory state, unknown availability summaries, no-current-belief, missing surface characterization | Unknown |

## Integrity Caveat Mapping

Integrity Caveats map to existing concepts including:

- unsupported facts and unsupported fact counts;
- projected fact conflicts from `FactConflict`;
- contradiction reports from `Contradiction`;
- graph issues from `GraphValidationIssue` and issue views;
- stale facts from expiry metadata;
- refresh recommendations for stale facts;
- unverified, stale, unknown, and provider-reported capability counts in
  Projection Integrity Summary;
- explicit default summary caveats on Projection Integrity Summary.

## Temporal Caveat Mapping

Temporal Caveats map to existing concepts including:

- `Fact.expires_at` and `is_fact_expired`;
- `FactSupport.expired` and `FactSupport.expires_at`;
- `FactSupport.observed_at` and `FactSupport.latest_observed_at`;
- `CapabilityInventoryEntry.age_seconds`, `observed_at`, and
  `latest_observed_at`;
- stale fact output and stale refresh recommendations;
- current-sample support semantics for measurements.

## Capability Caveat Mapping

Capability Caveats map to existing concepts including:

- `capability_verified` facts;
- `CapabilityVerificationState` values `verified`, `unverified`, `stale`,
  `provider_reported`, and `unknown`;
- missing verification facts producing unverified entries;
- expired verification facts producing stale entries;
- registered tools and ToolNeeds in the capability inventory universe;
- capability inventory reasons and supporting evidence.

## Evidence Caveat Mapping

Evidence Caveats map to existing concepts including:

- `EvidenceSummary.unsupported_fact_count`;
- `FactEvidenceView` evidence lists;
- supporting event IDs;
- missing linked evidence;
- evidence node summaries, evidence type, source event ID, and confidence;
- fact support source types.

## Confidence Caveat Mapping

Confidence Caveats map to existing concepts including:

- `FactConfidence.confidence`;
- support count;
- unsupported and contradicted flags;
- contradiction count;
- confidence reasons;
- confidence summary counts for strongly supported, weakly supported,
  unsupported, and contradicted facts.

## Observation Caveat Mapping

Observation Caveats map to existing concepts including:

- observation source type;
- observation confidence;
- observed fact timestamps;
- observation-derived fact summaries;
- local observation status facts;
- knowledge classification boundaries that prevent observations from implying
  availability, health, reachability, authorization, or management authority.

## Response Caveat Mapping

Response Caveats map to existing concepts including:

- `RuntimeResponse.kind`, message, and payload;
- invalid decision, intent rejection, and parse failure envelopes;
- CLI messages such as no matching fact found;
- explanation statuses `current`, `ambiguous`, and `no_current_belief`;
- read-only formatter descriptions;
- response vocabulary boundaries that Response communicates selected projected
  knowledge and limitations but does not create knowledge or execute tools.

# Relationship To Integrity

**Validated:** Integrity produces caveat-generating conditions. Integrity does
not own caveat communication.

Integrity owns or characterizes many caveat-producing signals: support,
unsupported facts, fact conflicts, contradictions, graph issues, stale facts,
expiry metadata, confidence limitations, verification status, and refresh
recommendations. Projection Integrity Summary is the strongest partial unifier
because it aggregates many of these signals and includes explicit summary
caveats.

However, Integrity is not a universal caveat communication owner. It does not
own every response surface, CLI formatter, runtime envelope, explanation output,
selection output, or capability display. Integrity also does not create truth,
repair facts, verify capabilities, execute refreshes, call providers, mutate
projections, or append events.

Correct relationship:

```text
Integrity produces and summarizes many caveat-generating signals.
Response and local surfaces communicate those signals.
No universal Integrity-owned caveat layer is implied.
```

# Relationship To Explainability

**Validated:** Explainability may explain caveats. Explainability is not caveat
ownership.

Explainability can expose why a belief is current, ambiguous, or absent; which
facts support a belief; which evidence IDs are involved; which competing beliefs
exist; whether a conflict is attached; and how inferred facts relate to source
facts. Those outputs can explain caveat-producing conditions such as ambiguity,
no-current-belief, competing beliefs, confidence caps, evidence limits, and
conflicts.

Explainability does not own caveats globally. Explanation vocabulary describes
read-only accounts over projected knowledge, support, conflicts, provenance, and
limits. It must not become a caveat engine, truth engine, verification engine,
selection engine, formatter, runtime path, or state mutation path.

Correct relationship:

```text
Explainability can explain caveats when caveat-related signals are present in
projected knowledge or explanation output.
Explainability does not own caveat generation or communication globally.
```

# Relationship To Selection

**Validated:** Selection may use caveat-producing signals. Selection is not
caveat ownership.

Selection and context composition can use caveat-producing signals such as
unsupported status, confidence, contradiction status, issue status, current-state
views, and capability status. Decision Context View, for example, selects facts
from confidence outputs and excludes unsupported facts by default unless asked to
include them.

Selection Caveats describe limits of inclusion, exclusion, ordering, and
available rationale. Selection does not own caveats globally, does not determine
truth, does not verify capabilities, does not mutate projections, and does not
become a planner or workflow engine.

Correct relationship:

```text
Selection may consume caveat-producing signals to decide what enters a context
or rationale surface.
Selection does not own caveats and does not replace Integrity or Response.
```

# Relationship To Response

**Validated:** Response communicates caveats. Response does not necessarily
generate caveats.

Response is the communication of selected projected knowledge and its
limitations to a consumer. Caveat communication is therefore a Response concern,
but caveat signals often originate elsewhere: Integrity, Evidence, Confidence,
Capability status, Temporal metadata, Observation status, Selection status, or
runtime envelope status.

Response may communicate caveats as text, JSON fields, counts, statuses,
reasons, sections, summaries, metadata, or explicit caveat lists. Response does
not need a new engine to do this. Existing local response surfaces can continue
to own local formatting.

Correct relationship:

```text
Signal ownership remains distributed.
Response communicates caveats on concrete surfaces.
Response does not create knowledge, decide truth, verify capabilities, execute
tools, call providers, mutate projections, or append events.
```

# Existing Caveat Surfaces

| Surface | Existing caveat communication | Categories | Status |
| --- | --- | --- | --- |
| Projection Integrity Summary | Aggregates unsupported facts, fact conflicts, contradictions, graph issues, stale facts, refresh recommendations, capability verification counts, and explicit summary caveats | Integrity, Evidence, Graph, Temporal, Capability | Implemented for summary scope; Partial for general response scope |
| Integrity Navigation / CLI drill-downs | Provides pointers such as `--unsupported-facts`, `--fact-conflicts`, `--contradictions`, `--graph-issues`, `--stale-facts`, `--stale-fact-refreshes`, and `--capability-status` | Integrity, Evidence, Graph, Temporal, Capability | Partial |
| Explanation outputs | Communicate current, ambiguous, and no-current-belief statuses; current and competing beliefs; support confidence; supporting facts; evidence IDs; conflicts; inference metadata | Rationale, Evidence, Confidence, Integrity, Response | Implemented for fact explanation; Partial for all caveats |
| Capability Inventory | Communicates verified, unverified, stale, provider-reported, and unknown states; supporting facts; evidence summaries; support metadata; age; reason | Capability, Evidence, Temporal, Confidence | Implemented for capability verification scope; Partial for general caveats |
| State Views | Communicate facts, observations, requirements, capabilities, issues, state summary counts, projection version, and last event | Observation, Capability, Graph, Response | Implemented as read-only views; Caveats mostly Implicit |
| Issue Views | Communicate graph issue summary, severity, supporting relationship IDs, and source fact IDs | Graph, Integrity | Implemented |
| Contradiction outputs | Communicate contradiction count, affected facts, severity counts, reasons, conflicting values, fact IDs, evidence, and supporting events | Integrity, Evidence, Confidence | Implemented |
| Confidence outputs | Communicate strongly/weakly supported counts, unsupported count, contradicted count, average confidence, per-fact confidence, support count, reasons, and supporting events | Confidence, Evidence, Integrity | Implemented |
| Decision Context View | Communicates selected context facts, contradicted status, confidence, evidence count, issues, requirements, capabilities, and summary counts; excludes unsupported facts by default | Selection, Confidence, Integrity, Graph, Capability | Implemented for context scope; Selection caveats mostly Implicit |
| CLI outputs | Communicate caveats through formatted summaries, no-matching-fact messages, read-only labels, statuses, counts, reasons, and JSON surfaces | All | Partial and distributed |
| Runtime response envelopes | Communicate response kind, message, payload, invalid decision status, parse failures, intent rejection, tool needs, and operation results | Response, Capability, Runtime limitation | Implemented for runtime envelope scope; not a caveat system |
| State summary output | Communicates conflict count, stale fact count, graph issue counts, availability unknown counts, observation source counts, and projection-backed summaries | Integrity, Temporal, Graph, Observation | Implemented as summary; caveat labels mostly Implicit |

Classification finding: caveat surfaces exist, but no single existing surface
answers all unresolved operator questions:

- What caveats apply to this answer?
- What caveats apply to this capability?
- What caveats apply to this current fact?
- What caveats apply to this response?
- How should multiple caveats be communicated together?

Those questions justify shared vocabulary and possibly future documentation
characterization. They do not justify implementation in this document.

# Proposed Vocabulary Shape

The following shape is documentation vocabulary only. It is not a schema class,
API contract, runtime contract, adapter, route, read model, or implementation
requirement.

```text
Caveat
  source
  category
  scope
  signal
  status
  limitation
  qualification
  warning
  uncertainty
  metadata
  extensions
```

## source

The existing caveat source, such as `FactConfidence`, `Contradiction`,
`CapabilityInventoryEntry`, `ProjectionIntegritySummary`, `Explanation`,
`DecisionContextView`, or a CLI/runtime surface.

## category

The caveat category: Integrity, Evidence, Capability, Temporal, Confidence,
Selection, Observation, Response, Graph, Rationale, or Unknown.

## scope

The thing qualified by the caveat: fact, current belief, response, capability,
summary, graph issue, explanation, selection result, observation, or runtime
envelope.

## signal

The existing field, flag, count, status, reason, or metadata that supports the
caveat.

## status

The caveat support status: Implemented, Partial, Missing, Implicit, or Unknown.

## limitation

The boundary the caveat communicates, such as no evidence, no verification, no
refresh, read-only, no-current-belief, or not a truth judgment.

## qualification

A narrowing statement such as projection-backed, as-of a timestamp,
provider-reported, current-sample, selected-context-only, or CLI-formatted.

## warning

A stronger caveat marker such as unsupported, stale, expired, contradicted,
conflicted, graph-invalid, ambiguous, unverified, unknown, or invalid decision.

## uncertainty

Any ambiguity, unknown status, confidence limitation, missing evidence, missing
rationale, or no-current-belief condition.

## metadata

Supporting IDs, timestamps, confidence values, source types, severity, reasons,
projection version, last event ID, supporting facts, evidence IDs, and extension
notes.

## extensions

Documentation-only future additions that preserve existing ownership and do not
create engines, read models, routes, adapters, schemas, runtime behavior, tool
execution, provider calls, projection mutation, or event appends.

# Complexity Traps

## CaveatEngine

A `CaveatEngine` is a trap because the repository already has caveat-producing
signals and caveat surfaces. The current gap is shared language and fragmented
communication, not a missing central engine. A new engine risks duplicating
Integrity, Response, Explainability, Selection, Confidence, and Capability
Inventory ownership.

## ResponseEngine

A `ResponseEngine` is a trap because Response is a communication concern with
distributed surfaces. A central response engine would blur Runtime routing, CLI
formatting, explanation outputs, integrity summaries, and state views while
creating a parallel response system.

## ReasoningEngine

A `ReasoningEngine` is a trap because Caveat Vocabulary does not reason, infer,
plan, prove truth, resolve contradictions, or decide action. Caveats communicate
limits around already-projected or already-selected knowledge.

## ContextEngine

A `ContextEngine` is a trap because context composition and Decision Context
View already exist as read-only selection surfaces. Caveat vocabulary should not
re-implement context selection, budgets, ordering, or admission.

## Planner and WorkflowEngine

Planners and workflow engines are traps because caveats are interpretive
communication, not task orchestration. Stale-fact refresh recommendations and
capability gaps do not authorize refresh execution, tool calls, provider calls,
or workflow creation.

## Universal Caveat Layer

A Universal Caveat Layer is a trap because caveat ownership is distributed.
Forcing all surfaces through one layer would create a parallel caveat system and
risk weakening source-specific semantics. Vocabulary can unify language without
centralizing behavior.

## Universal Formatter

A Universal Formatter is a trap because CLI, JSON, runtime envelopes,
explanations, summaries, and inventories have different consumers and local
formatting needs. Vocabulary does not require identical presentation.

## Runtime integration

Runtime integration is a trap by default because caveat vocabulary does not need
new runtime behavior. Runtime response envelopes may communicate caveats, but the
vocabulary must not alter routing, decision validation, model calls, retries,
tool execution, event appends, or response payload semantics.

## ToolExecutor integration

ToolExecutor integration is a trap because caveats do not execute tools, verify
capabilities, refresh stale facts, or call providers. Tool execution would turn a
communication vocabulary into behavior.

## Parallel caveat systems

Parallel caveat systems are traps because existing structures already produce
the relevant signals. A separate caveat store, event stream, projection, truth
system, response system, or schema hierarchy would duplicate source semantics
and create reconciliation problems.

# Non-Goals

This document does not:

- implement caveats;
- implement caveat summaries;
- implement caveat inventories;
- implement caveat navigation;
- implement caveat contracts;
- implement caveat aggregation;
- add read models;
- add routes;
- add adapters;
- add schema classes;
- modify `Runtime`;
- modify `ToolExecutor`;
- modify `EventLedger` ownership;
- modify `ProjectionStore` ownership;
- mutate projections;
- append events;
- call providers;
- execute tools;
- change capability verification behavior;
- change confidence behavior;
- change contradiction behavior;
- change explanation behavior;
- change selection behavior;
- change response behavior;
- create a `CaveatEngine`, `ResponseEngine`, `IntegrityEngine`,
  `ExplainabilityEngine`, `ReasoningEngine`, `ContextEngine`, planner,
  workflow engine, universal caveat layer, universal formatter, parallel truth
  system, parallel response system, or parallel caveat system.

# Future Work

Future work should remain documentation-oriented unless a later audit identifies
a concrete operator question that cannot be answered by composing existing
surfaces.

Supported future documentation work:

1. **Response Caveat Reconciliation**
   - Reconcile this vocabulary against `docs/response_caveat_characterization.md`
     and existing Response documentation.
   - Decide which terms are canonical and which remain characterization-only.

2. **Caveat Communication Characterization**
   - Characterize how current response surfaces communicate caveats today.
   - Compare text, JSON, summary, explanation, inventory, and runtime-envelope
     surfaces without creating a formatter.

3. **Caveat Aggregation Characterization**
   - Study how multiple caveat signals could be discussed together for a fact,
     capability, response, or answer.
   - Keep the result descriptive; do not implement an aggregator.

4. **Caveat Inventory Characterization**
   - Determine whether operators need a documentation map of caveat-producing
     fields by surface.
   - Do not create a runtime inventory, read model, route, adapter, or schema.

5. **Response Caveat Surface Matrix**
   - Expand the existing surface classification table with exact field names and
     examples from each surface.
   - Keep source ownership intact.

Future work should not recommend engines, runtime integration, ToolExecutor
integration, provider integration, projection mutation, event appends, schema
classes, adapters, routes, read models, universal formatting, or parallel caveat
systems by default.
