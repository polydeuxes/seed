# Context Composition Reconciliation

## Executive Summary

Seed already contains context-composition foundations. They are not a new
reasoning engine: they are read-only selection and formatting surfaces over
projected knowledge.

The current architectural distinction should be preserved:

```text
Knowledge Acquisition answers: What do we know?
Context Composition answers: Which already-known things matter right now?
```

Seed's implemented context-related behavior already draws from projected
`State`, current fact support, evidence, contradictions, confidence aggregation,
requirements, capabilities, graph issues, temporal freshness/expiry metadata,
and open `ToolNeed`s. The missing concept is not a `ContextEngine`; it is a
small canonical vocabulary that describes context composition as a read-only,
projection-backed selection problem.

This reconciliation is documentation only. It does not change `Runtime`,
`ToolExecutor`, `EventLedger`, `ProjectionStore`, state projection, capability
resolution, provider behavior, tool execution, fact mutation, projection
mutation, planning, orchestration, or LLM behavior.

## Scope

This document audits context composition as an architecture concern.

It asks:

- what context-related behavior already exists;
- what context-selection behavior already exists;
- what state-selection behavior already exists;
- what explanation-selection behavior already exists;
- what temporal-selection behavior already exists;
- what capability-selection behavior already exists;
- what repository structures already contribute to context;
- what concepts are genuinely missing;
- what concepts should remain outside Seed.

It does not propose implementation work.

## Files Inspected

Minimum requested files inspected:

- `README.md`
- `docs/architecture.md`
- `docs/architecture_principles.md`
- `docs/invariants.md`
- `docs/state.md`
- `docs/reasoning_roadmap.md`
- `docs/knowledge_classification_vocabulary.md`
- `docs/explanation_contract_vocabulary.md`
- `docs/capability_verification_vocabulary.md`
- `docs/capability_extension_methodology.md`
- `seed_runtime/state.py`
- `seed_runtime/state_views.py`
- `seed_runtime/context_views.py`
- `seed_runtime/explanations.py`
- `seed_runtime/tool_needs.py`
- `seed_runtime/capability_inventory.py`

Additional adjacent context considered:

- generated architecture ownership metadata in `docs/generated/architecture/`;
- the current architecture principles and invariants around runtime, projection,
  capability resolution, verification, and historical planning artifacts.

## Current Context-Composition Foundations

Seed already has three overlapping but distinct context foundations.

### 1. Model-visible context packets

`ContextComposer.compose(...)` selects from the current input, active goals,
entities, facts, evidence, registered tools, and open tool needs. It applies a

This is the closest existing implementation to context composition for model
input. It is compact and operationally adjacent to runtime prompting, but its
selection logic remains deterministic and based on projected state plus registry
inventory.

Important properties:

- it consumes projected `State`;
- it includes current input;
- it selects one active goal;
- it includes entities, facts, evidence, and open tool needs;
- it includes visible registered tool metadata;
- it records budget trace metadata;
- it does not create facts or projections.

### 2. Decision context views

`seed_runtime/context_views.py` defines read-only Context View projections for
already-projected `State`, the Evidence Graph, Contradiction Detection, and
Confidence Aggregation, and that they do not read the event ledger, append
events, mutate state, execute runtime behavior, call providers, evaluate policy,
execute tools, call LLMs, or persist a separate context store.

This is the clearest architectural fit for future context-composition language:
context composition as a deterministic, projection-backed view boundary between
knowledge and decisions.

Implemented context-view fields include:

- selected context facts;
- issues;
- requirements;
- capabilities;
- summary counts;
- projection version;
- last event ID.

### 3. State and explanation selection

`seed_runtime/state.py` already defines current-state selection mechanisms:

- `get_best_fact(...)` selects the representative fact for the strongest current
  belief;
- `get_current_facts(...)` returns current facts using predicate cardinality;
- `get_fact_supports(...)` returns aggregate support groups;
- `get_fact_support(...)` returns the unambiguous strongest support;
- `get_fact_conflicts(...)` exposes projected conflicts;
- `get_stale_facts(...)` and `get_stale_fact_refresh_recommendations(...)`
  expose stale/expired fact views without mutation.

`seed_runtime/explanations.py` builds deterministic explanations entirely from a
projected `State`. Its `why(subject, predicate)` path separates current beliefs,
competing beliefs, ambiguity, no-current-belief status, conflict, evidence IDs,
supporting fact IDs, source types, observation timestamps, latest observation
timestamps, inference rule IDs, source fact IDs, confidence caps, and alias
resolution chains.

These are context-composition building blocks even though they are not named
"context composition" everywhere.

## Existing Building Blocks Identified

### Knowledge-first architecture

Seed's canonical path remains:

```text
Observation -> Evidence -> Fact -> Relationships / Entity Types -> Contradictions -> Current-State Projection -> Explanation -> Query / Response
```

Capability handling remains downstream:

```text
Projected State -> ToolNeed -> Capability Resolution -> Registered Operation Candidates -> Provider Recommendations -> Response
```

Context composition should therefore consume projected knowledge and capability
surfaces; it should not become the mechanism that creates them.

### Projected State

`State` is the current inspectable world model. It contains entities, facts,
observed facts, inferred facts, relationships, aliases, entity type assertions,
graph issues, fact supports, fact conflicts, evidence, observations, goals,
tool needs, pending/historical planning artifacts, and registered tool specs.

Architectural fit: **implemented foundation**.

Context implication: projected state is the primary source from which context is
selected. Context composition should not read the ledger directly when projected
state already has the required current view.

### State Views

`seed_runtime/state_views.py` exposes read-only views for facts, observations,
requirements, capabilities, issues, and a state summary. `docs/state.md` names
these as answers to what Seed currently knows, what facts exist, what
requirements exist, what capabilities exist, and what issues exist.

Architectural fit: **implemented foundation**.

Context implication: these views are candidate source slices for future
operator-facing or model-facing context summaries.

### Context Packets

`ContextComposer` currently composes compact model-visible packets. Its section
inputs are current input, active goals, open tool needs, recent facts, recent
evidence, and entities. It also includes visible registered tool metadata.

Architectural fit: **implemented, but narrower than the emerging architecture
question**.

Context implication: it answers "what can enter this model-visible packet?" but
not the full architectural vocabulary for "what matters right now?" across all
knowledge classes and explanation surfaces.

### Context Budget

not estimate tokens; it answers which categories are allowed into the next model
context first as state grows.

Architectural fit: **implemented coarse selection mechanism**.

Context implication: it is section-priority selection, not semantic relevance,
reasoning, planning, or LLM ranking.

### Context Selection Ordering

evidence by recency, confidence, and ID; goals with active goals first; and
entities by confidence, name, and ID.

Architectural fit: **implemented deterministic ordering**.

Context implication: Seed already has temporal and confidence-aware ordering
inside context sections. This should be described as ordering, not as truth
selection or semantic relevance.

### Decision Context Views

Contradiction Detection, and Confidence Aggregation. It selects context facts,
issues, requirements, and capabilities, then emits a summary with projection
metadata.

Architectural fit: **implemented read-only context view**.

Context implication: this is the best existing home for "context composition is
knowledge-first and projection-backed" language.

### Evidence Graph and Fact Support

`docs/state.md` describes the Evidence Graph as derived from projected `State`,
using `Fact`, `FactSupport`, and `Evidence`. `State` projects `FactSupport`
records that group supporting facts, aggregate confidence, expose source types,
track latest observation time, and respect expiry.

Architectural fit: **implemented evidence-backed support foundation**.

Context implication: context should include support and evidence metadata when
answering why a selected fact matters.

### Conflicts and Graph Issues

`State` carries projected `FactConflict` records and graph validation issues.
items. `explanations.py` attaches matching conflicts to fact explanations.

Architectural fit: **implemented issue surfaces**.

Context implication: relevant context is not only positive facts. Contradictions,
conflicts, graph issues, ambiguity, unsupported facts, and stale facts can matter
right now.

### Explanation Surfaces

The explanation vocabulary already defines explanations as read-only accounts of
claims assembled from projected facts, support records, evidence, conflicts,
inventories, rules, temporal metadata, and provenance. The runtime
`ExplanationBuilder` implements fact/belief explanations over projected state.

Architectural fit: **implemented for fact/belief explanations; documented more
broadly for other explanation categories**.

Context implication: explanation composition is a sibling to context composition.
Context selection can identify which claim/fact/issue matters; explanation
surfaces explain why that selected item exists, what supports it, and where it is
limited.

### Capability Resolution and Inventory

`ToolNeedService.resolve_capability(...)` returns read-only metadata for a
`ToolNeed`: known capability status, registered operation candidates, provider
recommendations, and handoff candidates. It does not execute tools, authorize
actions, create pending actions, or mutate registry/catalog state.

`CapabilityInventoryEntry` derives verification-like status from projected
`capability_verified` facts and supporting evidence. Missing verification facts
produce `unverified`; expired verification facts produce `stale`.

Architectural fit: **implemented read-only capability selection and inventory**.

Context implication: capabilities can be context, but capability context must
remain distinct from execution, availability, verification, and provider contact.

### Temporal Metadata

Seed has current-state temporal semantics, not a general temporal reasoner.
Projection order is ledger append/insertion order. Timestamps are provenance,
freshness, expiry, or cache metadata; they do not define projection replay order
or an as-of query API.

Existing temporal selection includes:

- fact expiry exclusion in default support/current-belief/conflict queries;
- stale fact listing and refresh recommendations as read-only views;
- measurement latest-current sample selection;
- context ordering by freshness and recency;
- explanation exposure of observed and latest-observed timestamps;
- capability inventory age/stale metadata.

Architectural fit: **partially implemented for latest-current context; missing
for as-of/historical context by design**.

Context implication: "what matters right now" should mean latest-current unless
a future temporal reconciliation explicitly defines an as-of context view.

### Knowledge Classification Vocabulary

The repository now defines Identity, Configuration, Topology, Description, and
State as documentation-only knowledge classes. The vocabulary explicitly says it
does not add behavior, projection semantics, freshness policy, scheduling,
context composition, execution, provider integration, or LLM reasoning.

Architectural fit: **documentation vocabulary, not implementation**.

Context implication: the classes are good future metadata for describing why a
fact may be stable, volatile, foundational, or operationally relevant. They are
not yet a context-selection algorithm and should not silently become one.

### Requirements and ToolNeeds

Requirements already appear in state views and decision context views. Open
resolution consumes them as capability gaps.

Architectural fit: **implemented as context contributors**.

Context implication: requirements and open capability gaps are valid signals for
"what matters right now," but they must not imply planning, execution,
verification, or provider availability.

### Generated Architecture Documentation

The generated architecture graph records the ownership flow from `Runtime` to
`StateProjector`, `ToolNeedService`, `ToolRecommendationService`, and
`ToolExecutor`, and records `StateProjector` producing `State`. It also records
`ToolNeedService` as owning capability-gap creation and read-only capability
resolution, and `CapabilityCatalog` as provider/handoff metadata that does not
execute tools.

Architectural fit: **implemented/generated ownership evidence**.

Context implication: context composition must respect ownership boundaries.
Generated architecture documentation is useful evidence when reconciling where a
future context vocabulary belongs.

## Context-Related Behavior Already Exists

Seed already has context-related behavior in these forms:

- context section budgets and traces;
- deterministic ordering of facts, evidence, goals, and entities;
- decision context views over projected state, evidence graph, contradictions,
  confidence, requirements, and capabilities;
- state views over facts, observations, requirements, capabilities, issues, and
  summaries;
- explanation builders over projected fact support;
- stale fact and refresh recommendation views;
- capability resolution for open tool needs;
- capability inventory derived from projected facts and evidence;
- generated ownership documentation that distinguishes projection, runtime,
  execution, and capability metadata.

## Context-Selection Behavior Already Exists

Implemented context-selection behavior includes:

- selecting packet sections by priority and limit;
- selecting active goals before inactive goals;
- selecting open tool needs;
- ordering facts by unexpired/fresh first, then newer observed time, then higher
  confidence, then fact ID;
- ordering evidence by newer observed time, higher confidence, then evidence ID;
- ordering entities by confidence, name, and ID;
- excluding unsupported facts from decision context by default unless explicitly
  included;
- ordering context facts by support presence, confidence, subject, predicate,
  stable value, and fact ID;
- including issues from contradictions and graph validation;
- including requirements and capabilities through state views.

What does **not** yet exist is a documented canonical definition that says these
selection mechanisms together are Seed's current context-composition foundation.

## State-Selection Behavior Already Exists

State-selection behavior is stronger than the term "context" suggests:

- single-cardinality predicates select an unambiguous best-supported current
  belief when one exists;
- multi-cardinality predicates can return multiple current facts;
- measurements use latest-current sample semantics;
- expired facts remain stored but are excluded from default support/current
  belief/conflict queries;
- stale fact views expose expired facts without mutating them;
- conflicts are detected without deleting, rewriting, or superseding facts;
- aliases can be resolved for current fact queries.

This is current-state selection, not context composition. Context composition
should consume these outputs rather than reselecting truth with separate rules.

## Explanation-Selection Behavior Already Exists

Explanation selection already exists for fact/belief queries:

- `why(subject, predicate)` selects current, ambiguous, or no-current-belief
  status;
- current beliefs and competing beliefs are separated;
- fact supports determine which facts explain the belief;
- expired supporting facts are excluded from explanation facts;
- conflicts are attached when relevant;
- evidence IDs, source types, timestamps, inference links, confidence caps, and
  alias-resolution chains are exposed.

This is explanation selection, not general reasoning. It should remain
projection-backed and read-only.

## Temporal-Selection Behavior Already Exists

Temporal selection exists in latest-current form:

- context ordering prefers unexpired facts over expired facts;
- context ordering prefers newer observations;
- evidence ordering prefers newer evidence;
- fact support excludes expired facts by default;
- stale fact listing exposes expired facts separately;
- measurement predicates select the latest current sample;
- projection cache validity is tied to latest event ID/projection identity, not
  timestamp comparison;
- explanations expose observed/latest-observed metadata.

Temporal selection that does **not** exist:

- as-of event context;
- as-of timestamp context;
- belief timelines;
- why-then explanations;
- semantic what-changed context;
- historical context composition.

Those should remain outside this reconciliation.

## Capability-Selection Behavior Already Exists

Capability-selection behavior includes:

- open `ToolNeed` selection in context packets;
- duplicate open need avoidance by name or capability;
- read-only capability resolution for `ToolNeed`s;
- registered operation candidate discovery via `ToolRegistry` capability lookup;
- provider recommendation metadata and handoff candidates from catalogs;
- capability inventory over registered tools, tool needs, and
  `capability_verified` fact subjects;
- verification-state classification into `verified`, `provider_reported`,
  `unverified`, `stale`, and `unknown` when facts support those statuses.

Capability selection must remain read-only. It must not imply execution,
verification, availability, provider reachability, or policy authorization.

## Architectural Fit Matrix

| Input to future context composition | Current status | Notes |
| --- | --- | --- |
| Identity | Partially implemented | Identity facts exist as projected facts and aliases; knowledge class is documentation-only metadata. |
| Configuration | Partially implemented | Configuration facts exist through observation slices; class is not yet encoded as context metadata. |
| Topology | Partially implemented | Relationships, entity types, graph issues, and topology observations exist; class is vocabulary-level. |
| Description | Partially implemented | Description facts exist or are planned through observation slices; no context-specific class weighting exists. |
| State | Implemented / partially implemented | Current projected state, current fact selection, stale fact views, and measurement latest-current semantics exist. Volatile State as a knowledge class is not encoded as context metadata. |
| Temporal metadata | Implemented for latest-current | Freshness, recency, expiry, staleness, latest/current sample, and cache metadata exist; as-of context is absent by design. |
| Fact support | Implemented | `FactSupport` aggregates support and confidence. Context should consume it. |
| Evidence | Implemented | Evidence Graph and fact evidence views expose support. |
| Conflicts | Implemented | Fact conflicts and contradictions are read-only issue/context surfaces. |
| Explanations | Implemented / partially documented | Fact/belief explanations exist; broader explanation contract vocabulary is documentation-only. |
| Capabilities | Implemented read-only | Capabilities appear in state views, context packets, resolution, and inventory. |
| Requirements | Implemented | Requirements appear in state and context views. |
| ToolNeeds | Implemented | Open needs are selected into context packets and resolved read-only. |
| Graph issues | Implemented | Graph validation issues appear in state views and decision context issues. |
| Current-state projections | Implemented | `StateProjector` and `ProjectionStore` own current-state projection/cache. |

## Genuinely Missing Concepts

The audit found that Seed does **not** need a new architecture to prove context
exists. It already exists in several names and layers. The genuinely missing
concepts are smaller:

1. **Canonical context-composition vocabulary.**
   Seed needs a stable documentation term for "read-only selection of relevant
   projected knowledge for a current decision, answer, or explanation."

2. **Clear boundary between state selection and context selection.**
   State selection decides current projected beliefs. Context selection chooses
   which current beliefs, issues, evidence, capabilities, and requirements are
   worth surfacing now. Context selection must not re-run truth arbitration.

3. **Clear boundary between context and explanation.**
   Context says what to include. Explanation says why an included claim exists,
   what supports it, and what limits it.

4. **A documented source precedence for context slices.**
   The safest default is: projected State first; state/context views second;
   evidence/explanation support third; capability inventory/resolution only when
   a capability gap is relevant; external/provider metadata only as non-executable
   recommendations.

5. **Knowledge-class metadata mapping.**
   Identity, Configuration, Topology, Description, and State may help future
   context prioritization, but they are not yet encoded as fact metadata or
   context selection inputs. The next step should be vocabulary mapping, not
   behavior.

6. **Explicit non-goal language for context composition.**
   The repository has strong non-goals for runtime, execution, verification, and
   planning. Context composition should inherit those non-goals explicitly.

7. **A smallest-next-step characterization.**
   Before code, document how existing `context.py`, `context_views.py`,
   `explanations.py`, and `capability_inventory.py` relate to one another.

## Concepts That Should Never Be Added As Context Composition

The following should remain outside context composition:

- `ContextEngine` as a new owner that competes with `StateProjector`,
  `ProjectionStore`, `Runtime`, or `ToolExecutor`;
- `ReasoningEngine` for LLM-driven context ranking;
- `Planner`, `ExecutionPlanner`, `AgentLoop`, `WorkflowEngine`, or orchestration
  layer;
- provider selection as part of context composition;
- tool execution or execution authorization;
- verification execution;
- fact mutation;
- projection mutation;
- a second truth system that reselects beliefs independently of projected state;
- a parallel context persistence store;
- token-budget estimation as an architectural source of truth;
- prompt-only hidden memory as a substitute for projected state;
- automatic retry, scheduling, workflow, or host mutation behavior.

## Complexity Traps

### Trap 1: Renaming existing views into a new engine

Seed already has Context Views, Context Composer, Context Budget, State Views,
Explanation Builder, Capability Inventory, and Capability Resolution. Creating a
`ContextEngine` would likely duplicate ownership and obscure the existing
projection-backed structure.

### Trap 2: Treating relevance as truth

A fact can be relevant but unsupported, stale, contradicted, or ambiguous.
Context composition must surface those statuses; it must not resolve them by
selection pressure.

### Trap 3: Treating recency as correctness

Current context ordering prefers fresh and recent facts, but projection order and
truth selection are not timestamp-only semantics. Recency can help order context;
it must not become unsupported temporal reasoning.

### Trap 4: Treating capability context as executable capability

A `ToolNeed`, known catalog entry, registered operation candidate, provider
recommendation, or handoff candidate can be relevant context. None proves that a
capability is verified, available, reachable, authorized, or executable.

### Trap 5: Collapsing context and explanation

Context composition can select a fact or issue. Explanation must remain the
separate read-only account of the selected item's support, evidence, conflicts,
and temporal/provenance metadata.

### Trap 6: Encoding knowledge classes as runtime policy too soon

Identity, Configuration, Topology, Description, and State are promising context
metadata, but they are currently documentation vocabulary. Turning them into
runtime priority rules without a separate audit would repeat previous invention
before reconciliation.

### Trap 7: Letting model needs mutate architecture boundaries

evidence, capability resolution, policy, execution, or provider behavior.

## Recommended Smallest Next Step

Do **not** implement context composition behavior yet.

The smallest safe next step is a documentation-only **Context Composition
Vocabulary v1** or a short addition to existing architecture documents that
names:

1. context composition as read-only selection over projected knowledge;
2. its canonical inputs: projected State, State Views, Evidence Graph,
   FactSupport, contradictions/conflicts, graph issues, explanations,
   requirements, capabilities, ToolNeeds, temporal freshness/expiry metadata,
   and current input;
   `ExplanationBuilder`, `CapabilityInventory`, and read-only capability
   resolution;
4. its boundaries: no execution, planning, orchestration, provider calls,
   verification, fact mutation, projection mutation, or parallel truth system;
5. the possible future role of Identity/Configuration/Topology/Description/State
   as metadata for context discussion only until a separate implementation audit
   is requested.

If implementation is later requested, the first implementation should be a small
characterization test or documentation-linked inventory of existing context
surfaces, not a new engine.

## Reconciliation Conclusion

Context composition is already present in Seed, but distributed across existing
knowledge and view layers. The correct architectural move is to reconcile and
name those pieces, not to invent a new owner.

Seed should continue to model knowledge acquisition as:

```text
Observation -> Evidence -> Fact -> Projection
```


```text
Projected knowledge + current input + open needs + issues + explanations
  -> read-only selected context
```

That selected context may support a response, explanation, or capability-gap
resolution. It must not become execution, planning, orchestration, provider
selection, verification, fact mutation, projection mutation, or LLM reasoning.
