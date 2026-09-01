# Knowledge Lifecycle Reconciliation

## Executive Summary

Repository evidence supports a broader top-level knowledge model, but only as a
**documentation-level architectural relationship**, not as a new subsystem,
engine, runtime owner, planner, orchestrator, or execution path.

The best-supported concern set is:

```text
Knowledge Acquisition -> Knowledge Integrity -> Knowledge Selection -> Response
```

This model is real enough to document because existing canonical documents
already separate:

- acquisition of knowledge from observations, evidence, facts, and projection;
- integrity characterization of projected knowledge through support, conflicts,
  contradictions, graph issues, temporal semantics, verification status,
  confidence, and stale/refresh signals;
- selection of relevant projected knowledge through context composition,
  ordering, budgets, explanations, and response construction;
- response as the operator-facing communication of selected knowledge and its
  limits.

However, the evidence does **not** support a `KnowledgeLifecycleEngine`,
`KnowledgeEngine`, `IntegrityEngine`, `SelectionEngine`, `ResponseEngine`,
`ReasoningEngine`, planner, agent loop, workflow engine, parallel truth system,
or provider/LLM-driven truth path.

The repository already implies this architecture through the README's
knowledge-first flow, `docs/architecture.md`, the canonical acquisition/selection
document, Knowledge Integrity reconciliation, context composition vocabulary,
explanation contract vocabulary, capability verification vocabulary, knowledge
classification vocabulary, and architecture invariants. The smallest safe next
step is to keep this as reconciliation documentation and, if accepted, later add
a short cross-reference from canonical architecture documentation. No behavior is
introduced here.

This document is documentation only. It does not change `Runtime`,
`ToolExecutor`, `EventLedger`, `ProjectionStore`, projection behavior, runtime
routing, provider behavior, tool execution, planning, orchestration, fact
mutation, projection mutation, contradiction resolution, verification execution,
refresh execution, or LLM reasoning.

## Files Inspected

Minimum requested files inspected:

- `README.md`
- `docs/architecture.md`
- `docs/architecture_principles.md`
- `docs/invariants.md`
- `docs/state.md`
- `docs/knowledge_acquisition_and_selection.md`
- `docs/knowledge_maintenance_reconciliation.md`
- `docs/context_composition_vocabulary.md`
- `docs/context_composition_reconciliation.md`
- `docs/explanation_contract_vocabulary.md`
- `docs/capability_verification_vocabulary.md`
- `docs/knowledge_classification_vocabulary.md`
- `docs/capability_extension_methodology.md`
- `docs/reasoning_roadmap.md`

Relevant generated and adjacent architecture documentation inspected:

- `docs/canonicalization_pass_v1.md`
- `docs/canonical_documentation_reconciliation.md`
- `docs/self_observation_reconciliation.md`
- `docs/architecture_visualization_phase1.md`
- `docs/capability_ownership_matrix.md`
- `docs/recommendation_selection_boundary.md`

## Architectural Findings

### The lifecycle model is supported, but narrowly

The repository supports a lifecycle-shaped architectural model because the
canonical knowledge path is already present in multiple places:

```text
Observation -> Evidence -> Fact -> Projection -> Context Composition ->
Explanation -> Response
```

The later Knowledge Integrity reconciliation inserts a real concern between
projection and selection: before projected knowledge is selected for context or
response, Seed needs to characterize whether that knowledge is supported,
conflicted, stale, verification-limited, graph-invalid, weakly supported,
ambiguous, or otherwise caveated.

The resulting model is therefore not merely an illusion created by recent
documentation work. It is a consolidation of already-existing flows:

```text
Observation -> Evidence -> Fact -> Projection
                       -> Integrity Signals
                       -> Context Composition / Explanation
                       -> Response
```

A slightly clearer top-level shorthand is:

```text
Knowledge Acquisition
  -> Knowledge Integrity
  -> Knowledge Selection
  -> Response
```

This should be read as concern ordering and dependency, not as a strict runtime
pipeline. Integrity signals are often projection-derived and may be consumed by
explanation or context composition; they are not a separate mutating stage.

### Existing canonical documentation already implies the model

The README already defines Seed as knowledge-first and proceeds from observations
through evidence, facts, contradictions, current-state projection, explanation,
and query/response. `docs/architecture.md` already names the canonical
acquisition/selection relationship and separately documents State Views,
Evidence Graph, Contradiction Detection, and Confidence Aggregation as read-only
projection views. `docs/knowledge_acquisition_and_selection.md` already
canonicalizes Acquisition and Selection. `docs/knowledge_maintenance_reconciliation.md`
already identifies Knowledge Integrity as distinct from Acquisition and
Selection.

Therefore, this reconciliation does not introduce a new architecture. It names a
larger relationship that current canonical documentation already suggests.

### The model must remain knowledge-first, not runtime-first

The supported lifecycle model is about read-only, projection-backed,
evidence-backed knowledge concerns. It must not be confused with the existing
boundary-oriented runtime flow:

```text
Input -> Events -> State -> Context -> Decision -> Policy -> Execution -> Events
```

That runtime flow remains relevant to implementation ownership, but it is not the
same as the knowledge lifecycle. The lifecycle model should not claim ownership
over `Runtime`, `ToolExecutor`, policy, providers, execution, planners, or
orchestration.

## Lifecycle-Fit Findings

### Supported top-level concerns

| Concern | Supported question | Finding |
| --- | --- | --- |
| Knowledge Acquisition | What do we know? | Strongly supported. Canonical flow is `Observation -> Evidence -> Fact -> Projection`. |
| Knowledge Integrity | Can we still trust or safely rely on what we know? | Strongly supported as a read-only characterization concern. Best term is Integrity, not Maintenance. |
| Knowledge Selection | What matters right now? | Strongly supported. Context composition and explanation consume projected knowledge and integrity signals. |
| Response | What can Seed communicate from selected knowledge? | Supported, but Response is best treated as the final communication concern rather than a peer knowledge-creation stage. |

### Correctness of Acquisition, Integrity, Selection, and Response

Acquisition, Integrity, Selection, and Response are the correct concerns if the
model is documented as a **knowledge lifecycle relationship** rather than a
runtime subsystem map.

Two refinements are important:

1. **Response is distinct from Selection but dependent on it.** Selection decides
   what projected knowledge and caveats matter now. Response communicates the
   selected knowledge in operator-facing form.
2. **Integrity is a characterization concern, not a mutation or repair concern.**
   It supplies support, conflict, temporal, verification, graph, confidence, and
   disclosure signals. It does not acquire evidence, select context, or write
   answers.

### Concepts that belong within the lifecycle

| Concept | Lifecycle ownership | Notes |
| --- | --- | --- |
| Observation | Acquisition | Direct bounded statement about what was seen. |
| Evidence | Acquisition | Source/provenance/support record. |
| Fact | Acquisition | Scoped projected knowledge claim. |
| Projection | Acquisition handoff / integrity materialization | Produces current State and many read-model signals; not a truth engine. |
| Fact Support | Integrity over projected knowledge | Characterizes support strength and source coverage for facts. |
| Confidence | Integrity signal | Support estimate, not truth or correctness. |
| Contradictions | Integrity signal | Read-only conflict reports; not resolution. |
| Fact Conflicts | Integrity signal in projected State | Projection-level disagreement view; not the same as standalone contradictions. |
| Graph Validation | Integrity signal | Relationship/type shape issues; not fact truth or graph repair. |
| Temporal Semantics | Integrity signal and acquisition metadata | Freshness, expiry, current-vs-history, and measurement semantics. |
| Refresh Recommendations | Integrity-derived recommendation | Stale-fact recommendation only; not refresh execution. |
| Verification Status | Integrity signal | Scoped status over projected capability facts; verification is not truth. |
| Context Composition | Selection | Read-only selection and formatting of projected knowledge. |
| Context Budgets | Selection | Admission/size constraints; priority is not truth. |
| Context Ordering | Selection | Display/admission ordering; ordering is not correctness. |
| Explanation | Selection / response support | Explains claims, support, conflicts, provenance, and limits; not verification. |
| Response | Response | Communicates selected knowledge and limitations; does not create knowledge. |
| Capability Resolution | Selection-adjacent consumer of projected knowledge | Read-only gap/candidate/recommendation reasoning; not execution or verification. |
| Knowledge Classification | Acquisition metadata, selection metadata | Classifies fact kinds; not policy, priority, verification, or truth. |
| ToolNeeds | Projected knowledge consumed by Selection/Response | Capability gaps in State; not execution requests by themselves. |
| Requirements | Projected knowledge consumed by Selection/Response | Desired/open needs that can guide relevance; not planning authority. |
| Current-State Views | Selection inputs over projected State | Read-only views of current projected knowledge; not new state stores. |

### Concepts that do not belong as lifecycle concerns

The following are important repository concepts, but they should not be promoted
as lifecycle concerns:

- `Runtime` ownership;
- `ToolExecutor` ownership;
- `EventLedger` ownership;
- `ProjectionStore` ownership;
- provider ownership;
- registered-operation execution;
- policy evaluation;
- planning;
- orchestration;
- LLM reasoning;
- workflow management;
- host mutation;
- automatic verification execution;
- automatic refresh execution;
- automatic contradiction resolution;
- automatic graph repair.

These remain outside the knowledge lifecycle because the lifecycle is read-only,
projection-backed, evidence-backed, and concerned with knowledge acquisition,
characterization, selection, and communication.

### Missing or underdeveloped concepts

The lifecycle model appears coherent, but several concepts remain missing or
partial:

| Missing or partial concept | Finding |
| --- | --- |
| Lifecycle vocabulary | This document introduces reconciliation-level wording, but there is no dedicated vocabulary page for lifecycle terms. |
| Selection rationale | Context composition has budget/order vocabulary, but explicit reasons why specific items were selected remain partial. |
| Response contract | Response responsibilities are described in acquisition/selection docs, but there is no dedicated response vocabulary. |
| Negative belief / why-not | Existing explanation docs note no explicit `why_not()` API or negative belief model. |
| Projection-integrity summary | Integrity signals exist, but no single summary surface consolidates support, conflicts, graph issues, staleness, and verification status. |
| Lifecycle placement for capability resolution | Current evidence supports capability resolution as downstream/read-only and selection-adjacent, but it should not become its own top-level lifecycle concern without further audit. |
| Lifecycle placement for requirements | Requirements are projected knowledge and context inputs, but their relationship to planning must remain explicitly bounded. |
| Repository self-observation | Self-observation fits acquisition if read-only and source-attributed, but it remains future/partial rather than current lifecycle implementation. |

## Terminology Findings

### Recommended term: Knowledge Lifecycle

`Knowledge Lifecycle` is acceptable for this reconciliation because it captures
the movement from knowledge creation to integrity characterization, selection,
and communication. The term also accommodates temporal semantics, stale facts,
refresh recommendations, current-vs-historical distinctions, and response
limitations.

The term must be bounded carefully:

```text
Knowledge Lifecycle = architectural relationship among knowledge concerns
Knowledge Lifecycle != runtime lifecycle, execution lifecycle, workflow lifecycle,
planner lifecycle, provider lifecycle, or agent loop
```

### Alternatives considered

| Term | Finding |
| --- | --- |
| Knowledge Lifecycle | Best fit if bounded as documentation-level concern relationship. |
| Knowledge Flow | Accurate and less subsystem-sounding, but weaker for temporal/staleness/integrity concepts. |
| Knowledge Pipeline | Risky; may imply strict execution stages or pipeline ownership. |
| Knowledge Architecture | Too broad; overlaps all knowledge-first architecture and says less about concern ordering. |
| Knowledge Processing | Risky; suggests active processing components or engines. |
| Knowledge Path | Useful shorthand, but too informal for the reconciliation title. |

### Terminology to avoid

Avoid naming implementation owners from this reconciliation:

- `KnowledgeLifecycleEngine`;
- `KnowledgeEngine`;
- `IntegrityEngine`;
- `SelectionEngine`;
- `ResponseEngine`;
- `ReasoningEngine`;
- `Planner`;
- `AgentLoop`;
- `WorkflowEngine`.

These names imply ownership and behavior the repository evidence does not
support.

## Responsibility Findings

### Knowledge Acquisition responsibilities

Knowledge Acquisition responsibly includes:

- identifying the narrowest fact needed;
- choosing bounded and least-privileged sources;
- recording observations;
- attaching evidence and provenance;
- creating facts from evidence;
- projecting facts, observations, relationships, entity types, requirements,
  ToolNeeds, and current State;
- preserving source limitations, uncertainty, staleness metadata, and
  contradiction potential for later consumers.

Knowledge Acquisition does not own response wording, context budgeting,
truth-resolution, verification execution, provider calls, runtime execution, or
host mutation.

### Knowledge Integrity responsibilities

Knowledge Integrity responsibly includes read-only characterization of:

- support and unsupported facts;
- confidence/support strength;
- fact conflicts;
- contradictions;
- graph validation issues;
- temporal status, expiry, staleness, and current-vs-history distinctions;
- refresh recommendations as recommendations only;
- capability verification inventory status;
- ambiguity, competing beliefs, and disclosure metadata;
- projection consistency signals.

Knowledge Integrity does not own observation, evidence creation, fact creation,
context composition, response generation, contradiction resolution, verification
execution, refresh execution, graph repair, fact deletion, provider truth, or LLM
truth.

### Knowledge Selection responsibilities

Knowledge Selection responsibly includes:

- choosing relevant projected knowledge for current input, answer, explanation,
  decision, capability-gap discussion, or operator view;
- applying existing context budgets and ordering;
- carrying support, confidence, contradiction, temporal, verification,
  provenance, source, and limitation metadata forward;
- surfacing absence, open needs, unsupported status, ambiguity, stale facts,
  ToolNeeds, or capability gaps when needed;
- including explanation outputs or explanation-relevant metadata when useful.

Knowledge Selection does not create facts, choose truth, mutate projections,
perform observations, execute operations, verify capabilities, call providers,
or create a parallel state store.

### Response responsibilities

Response responsibly includes:

- answering from selected projected knowledge;
- communicating evidence, support, uncertainty, contradiction, staleness,
  verification limits, and provenance when material;
- distinguishing observation from inference;
- distinguishing requested, known, candidate, provider-recommended,
  unverified, stale, and verified capabilities;
- presenting missing information, open needs, or capability gaps when projected
  knowledge cannot support an answer;
- preserving the distinction between relevance, priority, correctness, and
  truth.

Response does not create knowledge, mutate facts, mutate projections, execute
registered operations, call providers, perform observations, silently verify
claims, or resolve contradictions.

## Ownership Findings

The lifecycle model does not change implementation ownership.

| Existing owner | Ownership preserved |
| --- | --- |
| `EventLedger` | Historical append-only event source of truth. |
| `ProjectionStore` | Cache of projection snapshots only. |
| `State` / projection logic | Current projected world model and derived read-model structures. |
| State Views | Read-only representations of projected State. |
| Evidence Graph | Read-only explanation layer derived from projected State. |
| Contradiction Detection | Read-only contradiction view. |
| Confidence Aggregation | Read-only confidence/support estimate view. |
| `Runtime` | Canonical runtime routing/decision path; not owned by lifecycle docs. |
| `ToolExecutor` | Registered-operation execution; not invoked by lifecycle docs. |
| Capability Catalog / capability resolution surfaces | Read-only metadata, candidates, and recommendations; not execution or verification. |

No lifecycle concern owns event persistence, projection snapshot persistence,
registered-operation execution, provider execution, host mutation, policy
evaluation, or runtime routing.

## Relationship Findings

The supported relationships are:

```text
Knowledge Acquisition creates projected knowledge.
Knowledge Integrity characterizes projected knowledge.
Knowledge Selection selects projected knowledge and integrity signals.
Response communicates selected knowledge and its limitations.
```

More specifically:

1. **Acquisition -> Integrity**: acquisition supplies observations, evidence,
   facts, support links, relationships, entity types, requirements, ToolNeeds,
   and State for integrity to inspect.
2. **Integrity -> Selection**: integrity supplies caveats and health signals such
   as unsupported, stale, conflicted, graph-invalid, unverified, ambiguous, or
   weakly supported.
3. **Selection -> Response**: selection supplies the relevant projected knowledge
   and caveats that response can communicate.
4. **Response -> Acquisition**: response may report missing knowledge or a
   capability gap, but it must not directly acquire knowledge. Any future
   acquisition must occur through explicit observation/evidence/fact paths.

These relationships are directional for architecture reasoning, not hard runtime
ownership edges.

## Boundary Findings

The lifecycle model must preserve these distinctions:

- **Acquisition != Integrity**: creating evidence-backed facts differs from
  characterizing support, conflicts, freshness, and verification limits.
- **Integrity != Selection**: knowing a fact is stale or conflicted differs from
  deciding whether it matters for a current answer.
- **Selection != Response**: selecting context differs from wording and
  communicating an answer.
- **Explanation != Verification**: explanation exposes support and limits;
  verification requires scoped accepted evidence/status.
- **Response != Knowledge Creation**: response can report or ask, but must not
  create facts or mutate projections.
- **Integrity != Maintenance**: integrity reports health; it does not refresh,
  repair, verify, delete, or resolve.
- **Verification != Truth**: verified status is scoped and evidence-backed, not
  universal correctness.
- **Relevance != Correctness**: a relevant item may be stale, unsupported,
  contradicted, ambiguous, or unverified.
- **Priority != Truth**: budget/order priority affects presentation or admission,
  not correctness.
- **Confidence != Truth**: confidence estimates support strength and does not
  resolve contradictions.
- **Refresh Recommendation != Refresh Execution**: recommendations do not run
  observations, providers, tools, or network checks.
- **Capability Recommendation != Availability**: provider/candidate metadata is
  not execution success, reachability, or verification.

## Complexity Traps

Repository evidence supports explicitly avoiding:

- `KnowledgeLifecycleEngine`;
- `KnowledgeEngine`;
- `IntegrityEngine`;
- `SelectionEngine`;
- `ResponseEngine`;
- `ReasoningEngine`;
- planner or agent-loop architecture;
- workflow-engine framing;
- parallel truth systems;
- hidden belief stores;
- automatic contradiction resolution;
- automatic fact deletion;
- automatic graph repair;
- automatic verification execution;
- automatic refresh execution;
- provider-driven truth;
- LLM-generated truth;
- runtime routing from hidden trust scores;
- context composition that drops caveats to fit a budget;
- responses that convert relevance, priority, recommendation, or provider
  metadata into correctness;
- integrity terminology that implies active maintenance or repair.

## Architectural Process Finding

Repository evidence supports an observed documentation pattern:

```text
General Audit -> Focused Audit -> Reconciliation -> Vocabulary -> Implementation
```

This pattern appears across multiple recent domains:

- context composition progressed from reconciliation to vocabulary;
- explanation progressed through audit/reconciliation toward contract
  vocabulary;
- capability verification progressed from audit/reconciliation to vocabulary and
  inventory implementation;
- knowledge maintenance/integrity is currently at reconciliation level;
- knowledge classification is at vocabulary level;
- canonicalization pass documents how promoted architecture documentation is
  consolidated.

This is an architectural-process observation only. It should not become a
governance framework, required process, scheduler, planner, or approval system.
It is useful because it explains why this lifecycle reconciliation should remain
documentation-only and should not jump directly to implementation.

## Relationship to Existing Canonical Documentation

This document should be treated as a reconciliation layer over existing canonical
documentation, not as a replacement.

| Existing document | Relationship |
| --- | --- |
| `README.md` | Provides the high-level knowledge-first thesis and query/response flow. |
| `docs/architecture.md` | Provides canonical runtime/state/read-model ownership and the acquisition/selection relationship. |
| `docs/architecture_principles.md` | Provides the reasoning-system framing and execution-last boundary. |
| `docs/invariants.md` | Preserves runtime, ToolExecutor, EventLedger, ProjectionStore, and no-RuntimeLoop boundaries. |
| `docs/state.md` | Defines projected State, facts, support, conflicts, graph issues, views, and current knowledge surfaces. |
| `docs/knowledge_acquisition_and_selection.md` | Canonicalizes Acquisition and Selection. |
| `docs/knowledge_maintenance_reconciliation.md` | Canonicalizes Knowledge Integrity as the preferred term over Maintenance. |
| `docs/context_composition_vocabulary.md` | Defines context selection, relevance, priority, budgets, and ordering boundaries. |
| `docs/explanation_contract_vocabulary.md` | Defines explanation claims, support, evidence, conflicts, temporal metadata, and provenance. |
| `docs/capability_verification_vocabulary.md` | Defines verification-status vocabulary and its non-execution boundaries. |
| `docs/knowledge_classification_vocabulary.md` | Defines fact classes useful to acquisition and selection metadata. |
| `docs/capability_extension_methodology.md` | Provides narrow observation and source-selection rules that support acquisition boundaries. |
| `docs/reasoning_roadmap.md` | Documents future reasoning concerns and explicit non-goals without runtime drift. |

## Recommended Smallest Next Step

The smallest safe next step is documentation-only:

1. Treat **Knowledge Lifecycle** as a reconciliation-level umbrella term for the
   relationship among Acquisition, Integrity, Selection, and Response.
2. Do not create a lifecycle engine, runtime route, planner, provider
   integration, verification executor, refresh executor, contradiction resolver,
   or new state store.
3. If maintainers accept this reconciliation, add a short cross-reference in a
   later canonical documentation pass from `docs/architecture.md` or
   `docs/knowledge_acquisition_and_selection.md` to this document.
4. If further detail is requested, prefer a small vocabulary document that names
   lifecycle terms and boundaries rather than implementation.

## Conclusion

The repository supports a broader Knowledge Lifecycle model, with strict
boundaries:

```text
Knowledge Acquisition: creates evidence-backed projected knowledge.
Knowledge Integrity:   characterizes support, consistency, freshness,
                       verification limits, and other reliability signals.
Knowledge Selection:   selects relevant projected knowledge and caveats.
Response:              communicates selected knowledge without creating truth.
```

This lifecycle is already implied by canonical documentation. It is useful as an
architectural map only if it remains read-only, projection-backed,
evidence-backed, and separate from execution, providers, planners, orchestration,
mutation, automatic resolution, verification execution, refresh execution, and
LLM-generated truth.
