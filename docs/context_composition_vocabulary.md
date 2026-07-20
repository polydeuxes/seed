# Context Composition Vocabulary v1

## Purpose

Context Composition Vocabulary v1 defines canonical documentation language for
how Seed talks about **context**: the read-only selection of already-known,
projection-backed, evidence-backed knowledge that matters for the current input,
decision, answer, capability-gap discussion, or explanation.

This vocabulary preserves the distinction established by the context composition
reconciliation:

```text
Knowledge Acquisition answers: What do we know?
Context Composition answers: What matters right now?
```

The repository already has context-composition foundations. This document names
those foundations and their boundaries. It does **not** add runtime behavior,
context-selection algorithms, context engines, planners, provider integrations,
LLM reasoning, fact mutation, projection mutation, tool execution, or workflow
orchestration.

## Files Inspected

This vocabulary was written after inspecting the following documentation and
runtime surfaces:

- `docs/context_composition_reconciliation.md`
- `docs/explanation_contract_vocabulary.md`
- `docs/knowledge_classification_vocabulary.md`
- `docs/capability_verification_vocabulary.md`
- `docs/architecture.md`
- `docs/architecture_principles.md`
- `docs/invariants.md`
- `docs/state.md`
- `docs/reasoning_roadmap.md`
- `docs/generated/architecture/architecture_graph.json`
- `seed_runtime/context_views.py`
- `seed_runtime/state_views.py`
- `seed_runtime/explanations.py`

## Canonical Definitions

### Context

**Context** is the selected set of already-known Seed knowledge, metadata, and
current-input information that is worth surfacing for a current decision, answer,
capability-gap discussion, or explanation.

Context is not a separate truth layer. Context can include true facts,
unsupported facts, weakly supported facts, strongly supported facts,
contradictions, graph issues, requirements, capability gaps, explanatory
metadata, and temporal metadata when those items matter now.

A fact can be true but not relevant to the current context. A fact can be highly
relevant without becoming more true than another fact.

### Context Composition

**Context Composition** is the read-only, deterministic selection and formatting
of context from projected knowledge and adjacent read-only views.

Context composition consumes existing surfaces such as projected `State`, State
Views, Evidence Graph, Fact Support, Contradiction Detection, Confidence
Aggregation, Context Views, explanations, requirements, capabilities, ToolNeeds,
temporal metadata, and current input. It does not create, verify, execute, plan,
or mutate those surfaces.

Canonical shorthand:

```text
Projected knowledge + current input + open needs + issues + explanations
  -> read-only selected context
```

### Context Input

A **Context Input** is any existing read-only source that may contribute items to
context composition.

Canonical context inputs include:

- current input;
- projected `State`;
- State Views;
- Context Views;
- Evidence Graph;
- Fact Support;
- Contradiction Detection;
- Confidence Aggregation;
- graph validation issues;
- requirements and goals;
- ToolNeeds;
- capability inventory and read-only capability resolution metadata;
- registered operation metadata, when surfaced as inert capability context;
- provider or handoff recommendation metadata, when surfaced as non-executable
  context;
- temporal freshness, expiry, staleness, observed-at, latest-observed-at, last
  event, and projection-version metadata;
- explanation outputs and explanation-relevant metadata.

Context inputs must already exist. Context composition does not acquire new
knowledge to satisfy a context request.

### Context Candidate

A **Context Candidate** is an item from a context input that may be selected into
the current context.

Examples include a projected fact, a fact support group, an evidence summary, a
contradiction, a graph issue, a requirement, an open ToolNeed, a registered
operation candidate, a capability inventory entry, a provider recommendation, a
current-state projection slice, an explanation fragment, or temporal metadata.

A context candidate is not automatically selected. It only becomes context after
context selection chooses to surface it.

### Context Selection

**Context Selection** is the choice of which context candidates are included for
the current purpose.

Context selection answers: **which already-known things matter right now?**

It must not answer: **which fact is true?** Truth/current-belief selection belongs
to projected State, fact support, predicate cardinality, conflict semantics, and
related projection-layer rules. Context selection consumes those outputs and may
surface their limits.

### Context Relevance

**Context Relevance** is the reason a context candidate matters for the current
input, decision, answer, capability-gap discussion, or explanation.

Relevance is not truth. Relevance can arise from current input, active
requirements, open capability gaps, related subjects, conflicts, graph issues,
weak support, strong support, staleness, recency, scope, explanation needs, or
capability needs.

A relevant item can be contradicted, stale, unsupported, ambiguous, or
non-executable. Context composition should preserve those statuses instead of
silently resolving them.

### Context Priority

**Context Priority** is the ordering or admission preference among context
candidate categories or candidates.

Priority is not correctness. A higher-priority context item is surfaced earlier
or admitted under a budget before a lower-priority item; it is not made more true,
more verified, more executable, or more authoritative by that priority.

model-visible packet sections. The existing ordering helpers demonstrate
within-section deterministic ordering. This vocabulary does not turn either into
a semantic relevance engine.

### Context Budget

A **Context Budget** is a limit on how much selected context can be surfaced for
a target surface.

A budget may be expressed as section limits, global item limits, display limits,
or future target-specific limits. In current code, context budget means
priority-based section admission and traceable selected/dropped counts, not token
estimation.

Context budget is an output-shaping constraint. It does not change projected
truth, fact confidence, evidence support, capability verification, or stored
knowledge.

### Context Ordering

**Context Ordering** is deterministic ordering of context candidates or selected
context items.

Ordering may use freshness, recency, confidence, support presence, active status,
name, identifier, severity, subject, predicate, stable value, or section priority.
Ordering helps produce stable surfaces. It does not create truth semantics,
as-of temporal reasoning, LLM ranking, or planning.

Important distinctions:

- recency is not importance;
- recency is not correctness;
- freshness is not verification;
- support-aware ordering is not truth mutation;
- deterministic ordering is not reasoning orchestration.

### Context Scope

**Context Scope** is the boundary that defines what a context composition pass is
about.

Scope may be determined by current input, workspace, session, subject, predicate,
requirement, open ToolNeed, capability, explanation query, projected state
version, last event ID, or selected view target.

Scope limits selection. It does not define ownership, authorization, execution,
provider reachability, or a new persistence boundary.

### Context Source

A **Context Source** is the owner or read-only surface from which a context input
is drawn.

Canonical source precedence for vocabulary purposes is:

1. projected `State` and current input;
2. State Views and Context Views over projected State;
3. Evidence Graph, Fact Support, Contradiction Detection, Confidence Aggregation,
   and explanation surfaces;
4. requirements, ToolNeeds, capability inventory, and read-only capability
   resolution;
5. registered operation metadata and provider/handoff recommendations only as
   inert, non-executable metadata.

This precedence is a documentation vocabulary for describing safe source use. It
is not an implementation policy and does not add behavior.

### Context Metadata

**Context Metadata** is data that helps describe why a context candidate was
selected, how it should be interpreted, or what boundaries apply to it.

Context metadata may include:

- source surface;
- projection version;
- last event ID;
- subject, predicate, dimensions, and entity resolution;
- evidence IDs and support counts;
- confidence/support bucket;
- contradicted, unsupported, stale, or expired status;
- graph issue severity;
- requirement status;
- ToolNeed status;
- capability inventory status;
- observed-at, latest-observed-at, expiry, staleness, freshness, or cache
  metadata;
- knowledge-class labels such as Identity, Configuration, Topology, Description,
  or State, if a future vocabulary mapping adopts them;
- explanation relationship such as selected-for-why, support-for-claim, or
  competing-belief metadata.

Context metadata is explanatory. It must not silently become runtime policy,
truth policy, scheduling policy, freshness policy, provider policy, execution
policy, or verification policy.

### Context Exclusion

**Context Exclusion** is the deliberate omission of a context candidate from a
selected context surface.

Exclusion can happen because a candidate is outside scope, lower priority under a
budget, superseded by a more specific selected slice, hidden by target-surface
limits, not useful for the current question, or intentionally omitted by an
existing view default such as excluding unsupported facts unless requested.

Exclusion is not deletion. It does not mutate facts, evidence, projections,
ToolNeeds, capabilities, explanations, or ledgers. It also does not prove that the
excluded item is false, unimportant globally, unavailable, or permanently
irrelevant.

### Context Explanation

A **Context Explanation** is a read-only account of why a context item was
selected, what source it came from, what metadata limited it, and how it relates
to the current scope.

Context explanation is adjacent to, but distinct from, fact/belief explanation.
Fact/belief explanations answer why a claim exists, which facts and evidence
support it, and which conflicts or limits apply. Context explanations answer why
that claim, issue, requirement, capability, or metadata was surfaced now.

Context explanation is partial today. Existing budget traces, context summaries,
projection metadata, explanation outputs, support metadata, and selected/dropped
counts are building blocks, but there is no canonical context-explanation surface
or behavior in this vocabulary.

## Relationships Between Terms

```text
Context Input -> Context Candidate -> Context Selection -> Context
                    |                    |
                    |                    +-> Context Exclusion
                    |
                    +-> Context Metadata

Context Selection + Context Budget + Context Ordering + Context Scope
  -> selected context for a target surface

Context Explanation
  -> why this selected context item matters now
```

Key relationships:

- Context inputs supply candidates.
- Context candidates become selected context only after selection.
- Context selection is bounded by scope and budget.
- Context ordering makes selection and rendering deterministic.
- Context metadata describes source, support, limits, freshness, status, and
  interpretation boundaries.
- Context exclusion omits candidates without mutating or falsifying them.
- Context explanation explains selection, while fact/belief explanation explains
  support for claims.

## Context Categories and Architectural Fit

The reconciliation correctly identified that context inputs naturally arise from
many existing Seed concepts. Their vocabulary fit is:

| Category | Fit for Context Composition Vocabulary v1 | Notes |
| --- | --- | --- |
| Identity | Context metadata candidate | Useful for stable subject anchoring and entity resolution. Documentation-only as a knowledge class. |
| Configuration | Context metadata candidate | Useful for explaining declared settings and constraints. Must not imply availability, reachability, health, or successful behavior. |
| Topology | Context metadata candidate | Useful for structural relationship context. Must not imply ownership, availability, health, reachability, or successful I/O. |
| Description | Context metadata candidate | Useful for descriptive substrate context. Must not become verification or capability proof. |
| State | Strong context input | Current projected state and volatile operational markers are central context candidates. Knowledge-class `State` metadata remains vocabulary-only. |
| Evidence | Strong context input | Evidence helps show support and provenance for selected facts. |
| Fact Support | Strong context input | Fact Support groups supporting facts, confidence, source types, and timestamps for current beliefs. |
| Conflicts | Strong context input | Contradictions and FactConflicts are relevant context and must not be treated as automatic resolutions. |
| Graph Issues | Strong context input | Graph validation issues can matter as warnings/errors in the current context. |
| Temporal Metadata | Strong context metadata | Freshness, recency, expiry, staleness, latest-current samples, and projection cache metadata help interpret context. They do not define as-of context. |
| Explanations | Strong sibling surface | Explanations can be selected or referenced as context, but explanation generation remains separate. |
| Capabilities | Strong context input | Capability gaps, inventory, registered candidates, and recommendations can be context. They are not execution or verification by themselves. |
| Requirements | Strong context input | Requirements/goals shape what matters now. |
| ToolNeeds | Strong context input | Open ToolNeeds are current capability-gap context. |
| Current-State Projections | Primary context source | Projected State and read-only views are preferred over direct ledger reads for latest-current context. |

## Architectural Boundaries

Context composition is:

- read-only;
- projection-backed;
- evidence-backed where claims require support metadata;
- knowledge-first;
- deterministic where current surfaces are deterministic;
- a selection and formatting concern;
- a bridge from projected knowledge to current decision, answer, capability-gap,
  or explanation surfaces.

Context composition does not:

- create knowledge;
- acquire knowledge;
- modify knowledge;
- verify knowledge;
- execute capabilities;
- call providers;
- plan actions;
- orchestrate workflows;
- mutate projections;
- change truth selection;
- append events;
- mutate EventLedger data;
- mutate ProjectionStore snapshots;
- run registered operations;
- evaluate execution policy;
- call LLMs;
- create a parallel persistence layer;
- create a parallel truth system.

## Important Distinctions

- **Relevance != Truth**: relevance selects what matters now; truth/current
  belief is owned by projection-layer semantics and support/conflict rules.
- **Priority != Correctness**: priority controls admission or display order, not
  correctness.
- **Recency != Importance**: newer items may be ordered earlier without becoming
  more important in every scope.
- **Recency != Correctness**: timestamps are provenance, freshness, expiry, or
  cache metadata, not projection replay order or truth proof.
- **Capability Context != Capability Execution**: ToolNeeds, registered operation
  candidates, provider recommendations, and handoff candidates can be relevant
  context but do not execute.
- **Capability Context != Capability Verification**: requested, known,
  candidate, or recommended capabilities are not verified capabilities by
  presence alone.
- **Explanation Context != Explanation Generation**: context may include or point
  to explanation material, but explanation building remains a separate read-only
  account of support, evidence, conflicts, and provenance.
- **Context Selection != Planning**: selecting relevant facts, issues,
  requirements, or capabilities is not constructing an action plan.
- **Context Composition != Reasoning**: context composition prepares selected
  knowledge; it does not introduce LLM reasoning, planner reasoning, or execution
  reasoning.
- **Context Composition != Execution**: context composition never runs tools,
  mutates hosts, calls providers, schedules workflows, or retries operations.

## Relationship to Knowledge Acquisition

Knowledge Acquisition and Context Composition are separate concerns.

Knowledge Acquisition follows the knowledge path:

```text
Observation -> Evidence -> Fact -> Projection
```

Context Composition follows the selection path:

```text
Projected knowledge -> relevant selected context
```

Knowledge acquisition decides what Seed knows or can know through observations,
evidence, fact creation, inference, and projection. Context composition chooses
which already-known pieces matter for the current scope.

Context composition must not become a hidden acquisition path. If a needed fact
is absent, context composition may surface absence, uncertainty, unsupported
status, open requirements, or capability gaps, but it must not create new facts or
execute observations by itself.

## Relationship to Explanations

Explanations and context composition are siblings.

Context composition answers:

- which claim, issue, requirement, capability, or metadata should be surfaced now?

Explanation answers:

- why does this claim exist?
- what supports it?
- what conflicts with it?
- what provenance, inference, confidence, or temporal limits apply?

Context can select an explanation or explanation-relevant metadata. It must not
collapse explanation generation into context selection. The existing explanation
contract remains the vocabulary for read-only accounts of support, evidence,
conflicts, inventories, rules, temporal metadata, and provenance.

## Relationship to Capabilities

Capabilities can be context when a current input, requirement, ToolNeed, or
capability gap makes them relevant.

Capability context may include:

- an open ToolNeed;
- a requested capability name;
- registered operation candidates;
- capability inventory status;
- capability verification fact support;
- provider or handoff recommendation metadata;
- known-catalog metadata.

Capability context must not imply:

- execution;
- authorization;
- availability;
- provider reachability;
- verification;
- successful operation;
- host mutation;
- provider mutation.

`ToolExecutor` remains the execution owner. Capability resolution and capability
inventory remain read-only unless a separate explicit execution path is invoked by
existing architecture.

## Relationship to State

Projected `State` is the primary source for latest-current context. State owns
current world-model projection, current fact selection, fact support, conflicts,
observations, goals, ToolNeeds, graph issues, capabilities, registered tool specs,
projection version, and last event ID.

State Views and Context Views provide read-only slices over projected State.
Context composition should prefer those projected/read-only surfaces over direct
ledger reads when latest-current context is sufficient.

Context composition must not re-run current-belief selection, mutate projected
facts, reinterpret projection ordering, or make `ProjectionStore` own temporal
truth. As-of/historical context remains outside this vocabulary unless a future
temporal reconciliation defines it.

## Relationship to Knowledge Classification

Knowledge Classification Vocabulary v1 defines Identity, Configuration,
Topology, Description, and State as documentation-only classes. These classes are
a good vocabulary fit for future context metadata because they can help explain
stability, volatility, anchoring, structure, descriptive substrate, and operational
state.

However, those classes are not currently encoded as context-selection behavior.
They must not become implicit runtime priority rules, freshness policies,
scheduling policies, provider policies, verification policies, or LLM prompts
without a separate audit and explicit implementation request.

For v1, the architectural fit is:

```text
Knowledge class -> possible context metadata
Knowledge class -> not context policy
Knowledge class -> not truth policy
Knowledge class -> not execution policy
```

## Missing Concepts Findings

The reconciliation correctly identified that the missing work is mostly
vocabulary and boundary documentation rather than runtime construction.

Findings:

1. **Context vocabulary was missing.** Existing code and docs had context
   packets, Context Views, State Views, budgets, ordering helpers, explanations,
   capability inventory, and capability resolution, but no canonical vocabulary
   tying them together as Context Composition.
2. **Source precedence is partial.** Safe source precedence can be described from
   existing ownership boundaries, but there is no dedicated context-source policy
   or behavior.
3. **Context metadata is partial.** Projection version, last event ID, budget
   traces, support counts, confidence, contradicted status, evidence IDs, and
   temporal metadata already exist in places, but there is no single canonical
   context-metadata surface.
4. **Knowledge-class metadata is partial.** Identity, Configuration, Topology,
   Description, and State exist as documentation vocabulary, not encoded fact or
   context metadata.
5. **Context explanation is partial.** Existing budget traces, context summaries,
   explanation surfaces, and support metadata can explain pieces of selection, but
   there is no canonical context-explanation surface.

These are vocabulary findings only. They do not recommend implementation in this
document.

## Complexity Traps

### Trap 1: Adding a ContextEngine

A new `ContextEngine` would likely duplicate existing Context Composer, Context
Budget, Context Views, State Views, Explanation Builder, Capability Inventory,
capability resolution, StateProjector, or ProjectionStore ownership.

### Trap 2: Adding a ReasoningEngine

Context composition should not become LLM-driven semantic ranking or hidden
reasoning. Existing context surfaces are deterministic and projection-backed.

### Trap 3: Adding a Planner, ExecutionPlanner, AgentLoop, or WorkflowEngine

Selecting relevant knowledge is not planning. Context composition must not create
action plans, workflows, retries, schedules, approvals, or execution proposals.

### Trap 4: Adding an LLM Selector

LLM-based ranking would create a second selection authority and obscure evidence,
projection, and deterministic ordering boundaries.

### Trap 5: Creating a parallel truth system

Context selection must not reselect current beliefs independently of projected
State, FactSupport, predicate cardinality, conflict handling, and confidence
surfaces.

### Trap 6: Treating relevance as truth

Relevant items may be unsupported, contradicted, stale, ambiguous, or merely
needed for the current question. Relevance must preserve those statuses.

### Trap 7: Treating recency as correctness

Fresh or recent items can be ordered earlier, but timestamps are not projection
replay order, truth proof, as-of query semantics, or correctness proof.

### Trap 8: Treating capability context as executable capability

A ToolNeed, registered operation candidate, catalog entry, provider
recommendation, or handoff candidate can be context. None is execution,
authorization, reachability, availability, or verification by itself.

### Trap 9: Collapsing context and explanation

Context says what to include. Explanation says why a claim exists, what supports
it, and where it is limited. A future context explanation, if ever introduced,
should explain selection without replacing fact/belief explanations.

### Trap 10: Encoding premature runtime policy into knowledge classes

Identity, Configuration, Topology, Description, and State may help describe
context metadata. They must not silently become priority algorithms, freshness
rules, scheduling rules, provider rules, verification rules, or runtime policy.

### Trap 11: Letting model-visible packet needs redefine architecture

Model-visible context packets are one target surface. They do not own knowledge,
projection, evidence, capability resolution, policy, provider behavior, or
execution.

### Trap 12: Treating budget as architectural truth

Budget traces and limits explain selection under constraints. Dropped context is
not false, deleted, irrelevant forever, or globally unimportant.

## Architectural Process Finding

The inspected documentation supports an observed repository pattern:

```text
General Audit -> Focused Audit -> Reconciliation -> Vocabulary -> Implementation
```

This is visible across recent documentation work where audits and
reconciliations identified existing partial implementation before vocabulary or
implementation refinement. The pattern appears in documentation architecture,
capability verification, explanation contracts, knowledge classification,
self-observation, and context composition work.

This is a documentation finding only. It does not create a process framework,
governance model, approval requirement, or implementation sequence.

## Future Work Notes

Future work, if explicitly requested later, may document or audit:

- a context-source precedence policy;
- a context-metadata mapping for knowledge classes;
- a context-explanation vocabulary or inventory;
- a characterization inventory of existing context surfaces;
- target-specific context surfaces for model-visible packets, operator views,
  decision views, or explanation views;
- whether as-of/historical context belongs in a future temporal reconciliation;
- whether knowledge-class labels should ever become explicit metadata.

These are future documentation or audit topics only. This vocabulary does not
recommend implementation and does not define runtime behavior.

## Non-Goals

This document does not:

- modify Runtime;
- modify ToolExecutor;
- modify EventLedger ownership;
- modify ProjectionStore ownership;
- implement context selection;
- add a context engine;
- add a reasoning engine;
- add a planner;
- add an agent loop;
- add an execution planner;
- add a workflow engine;
- add provider integrations;
- add LLM reasoning;
- add fact mutation;
- add projection mutation;
- add capability execution;
- add capability verification;
- add temporal/as-of context;
- add new schemas, events, predicates, or persistence layers.

## Conclusion

Context composition is already partially present in Seed through model-visible
context packets, priority budgets, deterministic ordering helpers, Decision
Context Views, State Views, Evidence Graph, Fact Support, Contradiction
Detection, Confidence Aggregation, explanations, requirements, capabilities, and
ToolNeeds.

The correct v1 move is vocabulary: Seed should talk about context as read-only,
projection-backed, evidence-backed selection of what matters now, while
preserving the boundaries that keep context distinct from truth, planning,
reasoning, verification, provider selection, and execution.
