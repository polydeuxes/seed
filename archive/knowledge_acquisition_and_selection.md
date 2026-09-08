# Knowledge Acquisition and Selection

## Executive Summary

Seed's documentation and generated architecture metadata support a canonical
relationship between two complementary pipelines:

```text
Knowledge Acquisition:
Observation -> Evidence -> Fact -> Projection

Knowledge Selection:
Projected Knowledge -> Context Composition -> Explanation -> Response
```

This distinction is already implicit, and in some places explicit, across the
knowledge-first README, architecture overview, state documentation, context
composition reconciliation, context composition vocabulary, explanation contract
vocabulary, knowledge classification vocabulary, capability extension
methodology, reasoning roadmap, invariants, and generated architecture graph.

The distinction should be documented canonically because it prevents context,
explanation, and response surfaces from drifting into hidden knowledge-creation,
truth-selection, verification, planning, or execution paths.

This document is documentation only. It does not change `Runtime`,
`ToolExecutor`, `EventLedger`, `ProjectionStore`, projection behavior,
observation behavior, context composition behavior, explanation behavior,
provider behavior, tool execution, planning, orchestration, fact mutation,
projection mutation, or LLM reasoning.

## Files Inspected

Minimum requested files inspected:

- `README.md`
- `docs/architecture.md`
- `docs/architecture_principles.md`
- `docs/state.md`
- `docs/invariants.md`
- `docs/context_composition_vocabulary.md`
- `docs/context_composition_reconciliation.md`
- `docs/explanation_contract_vocabulary.md`
- `docs/knowledge_classification_vocabulary.md`
- `docs/capability_extension_methodology.md`
- `docs/reasoning_roadmap.md`

Relevant generated and adjacent architecture documentation inspected:

- `docs/knowledge_acquisition_status.md`
- `docs/canonicalization_pass_v1.md`
- `docs/self_observation_reconciliation.md`
- `docs/architecture_visualization_phase1.md`
- `docs/capability_ownership_matrix.md`
- `docs/recommendation_selection_boundary.md`

## Architectural Fit Finding

The acquisition/selection distinction is supported by existing repository
architecture.

Seed's top-level product definition says Seed receives observations, records
evidence, projects explainable state, and answers questions about what it knows
and why. The README's knowledge-first flow proceeds from observation sources to
observations, evidence, facts, relationships, entity types, contradictions,
current-state projection, explanation, and query/response. That is a broader
single-line knowledge path, but it contains two phases:

1. acquisition creates and projects knowledge;
2. selection surfaces already-projected knowledge for explanation and response.

The architecture overview names the boundary-oriented runtime flow as:

```text
Input -> Events -> State -> Context -> Decision -> Policy -> Execution -> Events
```

It also names the explanation/verification read-model flow as projected State to
Evidence Graph, Fact explanations, Contradiction Detection, and Confidence
Aggregation. This supports the interpretation that State/projection is the
handoff point between creating the current world model and selecting or
explaining pieces of that model.

The context composition vocabulary already states the distinction most directly:
Knowledge Acquisition follows `Observation -> Evidence -> Fact -> Projection`,
while Context Composition follows `Projected knowledge -> relevant selected
context`. This document makes that relationship canonical at the architecture
relationship level rather than leaving it embedded inside the context vocabulary.

## Canonical Relationship

### Knowledge Acquisition

**Knowledge Acquisition** is the pipeline that creates knowledge Seed can reason
over later.

Canonical shorthand:

```text
Observation -> Evidence -> Fact -> Projection
```

Acquisition answers:

```text
What do we know?
What evidence supports it?
What fact should be projected?
What current projected world model results?
```

Acquisition owns the transition from external or internal signals into Seed's
projected read model. It is the creation side of the architecture.

### Knowledge Selection

**Knowledge Selection** is the pipeline that selects from existing projected
knowledge for a current input, decision, explanation, answer, or operator view.

Canonical shorthand:

```text
Projected Knowledge -> Context Composition -> Explanation -> Response
```

Selection answers:

```text
Which already-known things matter right now?
Why is this selected or claimable?
What limitations must be carried forward?
What response can be made from selected projected knowledge?
```

Selection is the consumption side of the architecture. It may format, order,
budget, expose, explain, or summarize existing knowledge, but it does not create
facts or mutate projections.

## How Seed Acquires Knowledge

Seed acquires knowledge by turning bounded observations into evidence-backed
facts and projecting those facts into current State.

Acquisition responsibilities include:

- identifying the narrowest fact needed to answer a required question;
- choosing a least-privileged source of truth;
- preferring read-only observation sources;
- recording only what was directly observed;
- attaching evidence that identifies source and boundary;
- projecting observations into scoped facts with explicit predicates and values;
- preserving source limitations, uncertainty, staleness, and contradictions;
- replaying append-only events into latest-current projected State;
- deriving support, conflicts, relationships, entity types, graph issues, and
  other projected read-model structures from events and facts.

formatting, explanation generation, capability execution, provider calls, or
LLM-driven reasoning.

## How Seed Selects Knowledge

Seed selects knowledge by reading projected State and adjacent read-only views,
then choosing the slices that matter for the current scope.

Selection responsibilities include:

- selecting already-known projected facts, observations, requirements,
  capabilities, issues, ToolNeeds, and metadata that matter now;
- using State Views, Context Views, Evidence Graph, Fact Support,
  Contradiction Detection, Confidence Aggregation, capability inventory, and
  read-only resolution metadata as context inputs;
- respecting projection ownership and current-state selection rather than
  re-running belief selection independently;
- applying deterministic ordering or budget rules where those already exist;
- carrying support, confidence, contradiction, temporal, provenance, and
  limitation metadata forward when relevant;
- surfacing absence, unsupported status, ambiguity, stale facts, open
  requirements, or capability gaps when needed knowledge is missing.

Selection does not create knowledge. If a needed fact is absent, selection may
surface that absence or an open need, but it must not perform observations,
append evidence, create facts, execute operations, mutate State, or modify
ProjectionStore snapshots.

## Explanation Responsibilities

Explanation belongs primarily to the selection side, but it is not identical to
context composition.

Explanation is a read-only account of a claim assembled from existing projected
facts, support records, evidence, conflicts, inventories, rules, temporal
metadata, and provenance. Explanation answers:

- why a claim exists in the current read model;
- what supports it;
- what conflicts with it;
- what competing facts or values exist;
- what confidence, temporal, provenance, source, inference, or catalog limits
  apply;
- which supporting events, evidence IDs, source facts, rule IDs, or aliases are
  relevant.

Explanation does not determine truth. It reports projected-state and support
selection semantics without selecting differently.

Explanation also does not verify capabilities, execute tools, call providers,
route runtime behavior, invoke ToolExecutor behavior, call an LLM for reasoning,
append events, mutate projections, resolve contradictions, or create a second
source of truth.

## How Explanation Relates to Context

Context Composition and Explanation are siblings in the selection pipeline.

Context answers:

```text
What should be included or surfaced now?
```

Explanation answers:

```text
Why does this claim exist, what supports it, and where is it limited?
```

Context may select explanation outputs or explanation-relevant metadata, and an
explanation may be part of the selected context for a response. However, context
selection must not become explanation generation, and explanation generation must
not become context-source precedence, current-belief selection, verification, or
fact creation.

A future context-explanation surface, if explicitly requested, should explain why
specific items were selected into context under budget, ordering, source, or
scope constraints. It should not replace fact explanations, belief explanations,
or evidence-backed provenance explanations.

## Response Responsibilities

Response belongs to the final consumer-facing side of Knowledge Selection.

Response responsibilities include:

- answering from selected projected knowledge;
- preserving support, uncertainty, contradiction, staleness, and limitation
  metadata when those affect the answer;
- distinguishing observed facts from inferred conclusions;
- distinguishing capability gaps, candidates, recommendations, and verified
  capabilities;
- refusing to present configuration, relevance, recommendation, or priority as
  correctness or truth;
- presenting open needs or missing information when projected knowledge cannot
  support the requested answer;
- carrying explanation content into operator-facing text when asked what Seed
  knows and why.

Response does not create knowledge. A response can report a missing fact, request
information, describe a ToolNeed, or recommend a candidate based on read-only
metadata, but it must not mutate facts, mutate projections, execute registered
operations, call providers, perform observations, or silently verify claims.

## Responsibility Boundary Matrix

| Concern | Primary responsibility | Allowed outputs | Not allowed |
| --- | --- | --- | --- |
| Observation | Acquisition | Narrow statements about what was directly seen | Inferred availability, reachability, health, management, execution, or verification claims |
| Evidence | Acquisition | Source/support records and provenance | Proof beyond source boundary or hidden provider/tool calls |
| Fact | Acquisition | Scoped projected knowledge claims | Overbroad conclusions unsupported by observation/evidence |
| Projection | Acquisition handoff to selection | Latest-current State, support, conflicts, graph issues, views | Event ownership, historical/as-of API, truth arbitration, fact mutation |
| Context Composition | Selection | Read-only selected context from projected knowledge | Knowledge creation, observation, verification, execution, planning, LLM ranking, parallel truth system |
| Explanation | Selection | Read-only account of support, conflicts, provenance, limits | Truth determination, verification, execution, current-belief reselection, event/projection mutation |
| Response | Selection | Answer from selected projected knowledge and explanations | Fact creation, projection mutation, provider execution, hidden verification, treating relevance/priority as truth |

## Boundary Statements

The following distinctions are canonical for this relationship:

- **Context Composition != Knowledge Creation**. Context composition consumes
  existing projected/read-only surfaces.
- **Explanation != Knowledge Creation**. Explanation describes why an existing
  claim appears in the current read model.
- **Response != Knowledge Creation**. Response answers from selected projected
  knowledge or reports absence/uncertainty.
- **Selection != Truth**. Selection chooses what matters now; projected State,
  support semantics, and conflict handling determine current beliefs.
- **Relevance != Correctness**. Relevant items may be unsupported,
  contradicted, stale, ambiguous, or merely needed for the current question.
- **Priority != Truth**. Budget and ordering rules decide admission or display
  order, not correctness.
- **Explanation != Verification**. Explanation can expose support and limits,
  but verification requires its own scoped model when implemented.
- **Confidence != Truth**. Confidence estimates support strength and must not
  resolve contradictions automatically.
- **Recency != Correctness**. Freshness may influence ordering or current sample
  selection, but timestamps are not proof of correctness or projection replay
  order.
- **Capability recommendation != Execution**. Recommendations and registered
  operation candidates may appear in context or response, but do not execute by
  themselves.

## Terminology Alignment

### Observation, Evidence, Fact, Projection

These terms align with acquisition.

- `Observation` records what was directly seen.
- `Evidence` records source/support and makes observations auditable.
- `Fact` is the scoped knowledge claim Seed projects and reasons over.
- `Projection` turns append-only EventLedger data into latest-current State and
  derived read-model structures.

This alignment is supported by capability extension methodology and state
projection documentation. It should remain narrow: observation must not silently
become inference, verification, management, provider access, or execution.

### Projected Knowledge

Projected knowledge is the handoff between acquisition and selection.

It includes projected `State`, facts, observations, relationships, entity types,
fact supports, conflicts, graph issues, ToolNeeds, requirements/goals,
capabilities, registered tool specs, projection version, and last event metadata.

Projected knowledge is not a separate truth engine. It is a current read model
from append-only events and projection logic.

### Context Composition

Context Composition aligns with selection. It is the read-only deterministic
selection and formatting of context from projected knowledge and adjacent
read-only views. It may include current input and open needs, but those do not
make it an acquisition path.

### Explanation

Explanation aligns with selection and explainability. It is a read-only account
of support, evidence, conflicts, inventories, rules, temporal metadata, and
provenance for claims or surfaces already present in Seed's read models.

### Response

Response aligns with selection output. It is a consumer-facing answer from
selected projected knowledge and, when relevant, selected explanations. It must
preserve limitations rather than converting selected context into unsupported
truth claims.

### Knowledge Classification

Knowledge Classification Vocabulary v1 defines Identity, Configuration,
Topology, Description, and State as documentation-only classes for facts Seed
acquires or plans to acquire. These classes fit primarily as acquisition-side
classification metadata and possible future selection-side context metadata.

They must not become implicit runtime priority rules, freshness policies,
verification policies, provider policies, truth policies, or LLM prompts without
a separate audit and explicit implementation request.

## Relationship to Existing Vocabularies

### Context Composition Vocabulary

The context composition vocabulary already contains the strongest direct support
for this relationship. It states that Knowledge Acquisition and Context
Composition are separate concerns, gives each path, and says context composition
chooses already-known pieces that matter for the current scope.

This document elevates that local context-composition boundary into a broader
architecture relationship that also names Explanation and Response as downstream
selection responsibilities.

### Context Composition Reconciliation

The reconciliation found that Seed already has context-composition foundations:
explanation selection, budget traces, ordering helpers, and read-only views over
projected State. It also found that missing work was vocabulary/boundary
documentation rather than a new context engine.

This document preserves that finding and does not recommend implementation.

### Explanation Contract Vocabulary

The explanation contract vocabulary defines explanation as read-only,
projection-backed, evidence-backed, and inventory-backed. It explicitly separates
explanation from truth selection, verification, execution, Runtime routing,
ToolExecutor behavior, LLM reasoning, event appends, projection mutation, belief
selection, contradiction resolution, and second truth sources.

This document places explanation after context composition in the selection
pipeline while preserving it as a sibling concern rather than collapsing it into
context.

### Knowledge Classification Vocabulary

The knowledge classification vocabulary describes documentation-only classes for
facts Seed acquires or plans to acquire. It supports acquisition planning and can
inform future context metadata, but it does not define context-selection behavior
or truth policy.

### Capability Extension Methodology

The capability extension methodology supports acquisition boundaries by requiring
capability growth to reduce gaps to narrow facts, least-privileged sources,
read-only observations, evidence, facts, and optional inference. It separates
observation, inference, verification, and execution.

### State and Invariants

State documentation and invariants establish the projection handoff:
EventLedger owns append-only events, StateProjector owns projection from events
to current state, and ProjectionStore owns cached projected-state snapshots. They
also prevent projection and read-only views from becoming truth arbitration,
historical-as-of APIs, event owners, execution paths, or mutation paths.

### Reasoning Roadmap

The reasoning roadmap supports a knowledge and capability-discovery runtime:
input/observations to evidence/facts, relationships/entity types,
explanations/current state, ToolNeed, capability resolution, registered operation
candidates, provider/handoff recommendations. It also warns against adding
selection services, schedulers, retry engines, workflow orchestration, automatic
truth conflict resolution, or truth-maintenance engines.

## Supporting Findings

Findings supporting the distinction:

1. The README defines Seed as knowledge-first and describes observation,
   evidence, facts, current-state projection, explanation, query, and response as
   the central flow.
2. Architecture documentation separates EventLedger, ProjectionStore, State,
   State Views, Evidence Graph, Contradiction Detection, Confidence Aggregation,
   Runtime, and ToolExecutor ownership.
3. State documentation defines State Views as read-only answers to what Seed
   currently knows and Evidence Graph as a read-only explanation layer derived
   from projected State.
4. Context composition reconciliation explicitly defines context composition as
   read-only selection and formatting over projected knowledge.
5. Context composition vocabulary explicitly names acquisition as
   `Observation -> Evidence -> Fact -> Projection` and context composition as
   `Projected knowledge -> relevant selected context`.
6. Explanation contract vocabulary explicitly prevents explanation from becoming
   truth selection, verification, execution, Runtime behavior, event mutation, or
   projection mutation.
7. Knowledge classification vocabulary supports acquisition planning without
   turning classes into runtime priority, freshness, verification, or truth
   policies.
8. Capability extension methodology requires observation, evidence, fact,
   optional inference, verification, and execution to remain separate.
9. Invariants preserve EventLedger, ProjectionStore, Runtime, and ToolExecutor
   ownership boundaries.
10. Generated architecture metadata shows EventLedger feeding StateProjector,
    StateProjector producing State, ProjectionStore loading/saving snapshots, and
    Runtime/ToolExecutor retaining distinct ownership paths.

Potentially contradicting or limiting findings:

1. Existing top-level flows often present a single knowledge-first path through
   explanation and response rather than explicitly naming two pipelines.
2. Existing context code and context views are narrower than the full
   architecture-level concept of Knowledge Selection.
3. Knowledge-class labels are documentation-only and are not currently encoded as
   selection metadata.
4. There is no single implemented `KnowledgeSelection` service or context-source
   precedence policy, and this document should not imply one exists.
5. Response generation is a consumer-facing architectural responsibility, but it
   is not documented as a separate canonical knowledge-creation or selection
   owner. It should therefore be described as a selection output responsibility,
   not as a new subsystem.

These limitations do not contradict the distinction. They mean the distinction is
best documented as a canonical architecture relationship and boundary, not as a
new implementation layer.

## Canonical Non-Goals

This document does not:

- change `Runtime`;
- change `ToolExecutor`;
- change `EventLedger` ownership;
- change `ProjectionStore` ownership;
- add execution behavior;
- add orchestration;
- add planners;
- add reasoning systems;
- add provider integrations;
- add LLM reasoning;
- add fact mutation;
- add projection mutation;
- implement knowledge selection;
- implement context-source precedence;
- implement context explanations;
- implement response generation behavior;
- define truth arbitration;
- define capability verification behavior.

## Conclusion

Seed already supports the distinction between Knowledge Acquisition and Knowledge
Selection.

Observation, Evidence, Fact, and Projection belong primarily to acquisition
because they create and project knowledge. Context Composition, Explanation, and
Response belong primarily to selection because they consume, select, explain, and
present existing projected knowledge.

The correct architectural move is documentation-only: name the relationship,
preserve the handoff at projected knowledge, and keep selection surfaces from
becoming hidden acquisition, verification, truth, planning, execution, provider,
or mutation systems.
