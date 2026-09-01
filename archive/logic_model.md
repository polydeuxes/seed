# Logic Model

Seed should be understood as a logic system before it is understood as an execution system. Its core behavior is to transform observations into evidence, facts, projected state, explanations, ToolNeeds, capability resolutions, and responses.

## Logic Layers

### Observation Layer

The observation layer receives input and normalized observations. It describes what Seed has seen or been told before Seed decides what the observation proves.

### Evidence Layer

The evidence layer records support for claims. Evidence should preserve enough provenance to explain why a later fact exists and what observation, source, or derivation supports it.

### Fact Layer

The fact layer contains asserted or extracted claims about the world. Facts should be explainable through evidence and should not be treated as host execution instructions.

### Inference Layer

The inference layer derives additional knowledge from facts, relationships, entity types, predicates, and inference rules. Inferred facts should remain traceable to their source facts and rules.

### State Layer

The state layer is projected current knowledge. `EventLedger` stores append-only history, while `StateProjector` and `ProjectionStore` derive and cache current projected state.

### Capability Layer

The capability layer reasons from ToolNeeds / capability gaps to capability resolution; a ToolNeed is not an executable tool. `ToolNeedService` owns capability-gap creation and capability resolution. `ToolRegistry` contributes registered operation candidates. `CapabilityCatalog` contributes capability metadata, provider recommendations, and handoff candidates.

## Example Rules

### Observation -> Evidence

IF an observation is accepted by the observation ingestion path

THEN create evidence that preserves the observation's source and content.

### Evidence -> Fact

IF evidence supports a concrete claim about an entity, predicate, or value

THEN create a fact linked to that supporting evidence.

### Fact + Relationship Rule -> Relationship

IF a fact identifies an entity relationship and a relationship rule recognizes that predicate

THEN project a relationship between the relevant entities.

### Fact + Inference Rule -> Inferred Fact

IF a fact matches the conditions of an inference rule

THEN derive an inferred fact linked to the source fact and inference rule.

### ToolNeed / capability gap + Registry Match -> Operation Candidate

IF a ToolNeed matches registered operation metadata in `ToolRegistry`

THEN include the matching registered operation as an operation candidate.

### ToolNeed / capability gap + Capability Recommendation -> Provider Recommendation

IF a ToolNeed matches capability metadata or provider guidance in `CapabilityCatalog`

THEN include the matching provider recommendation or handoff candidate as recommendation metadata.

## Invariants

Repository invariants protect the architecture from drift:

- `EventLedger` is append-only.
- `ProjectionStore` never owns events.
- `ProjectionStore` caches projected state.
- `StateProjector` derives state from events and catalogs; it does not execute work.
- `ToolExecutor` owns execution.
- Execution begins at `ToolExecutor`.
- Everything before `ToolExecutor` should remain reasoning-oriented and read-only with respect to host execution.
- `ToolNeedService` owns capability-gap creation and capability resolution.
- `ToolRegistry` owns registered operation inventory.
- `CapabilityCatalog` owns capability metadata and provider/handoff recommendations.
- Capabilities are not executable.
- Registered operations are executable.
- Provider recommendations are not executable.
- Runtime is canonical.
- `RuntimeLoop` is not current-core architecture.
- `ActionPlan`, `HandoffPlan`, `ExecutionProposal`, and `ExecutionAuthorization` are not current-core architecture.

## Architecture Drift Detection

Recent architecture cleanup identified several drift patterns that future work should avoid:

- `RuntimeLoop` drift: a parallel runtime path can accidentally redefine canonical ownership even when it starts as experimentation.
- Duplicated runtime ownership: validation, context composition, capability-gap creation, or execution routing should not be reimplemented in multiple runtime-shaped components.
- Planning and execution artifacts outside canonical `Runtime`: artifacts such as `ActionPlan`, `HandoffPlan`, `ExecutionProposal`, and `ExecutionAuthorization` should not be treated as current-core architecture unless explicitly reintroduced through the canonical ownership model.
- Execution ownership leakage: code before `ToolExecutor` should not become a host-execution framework, retry framework, scheduler, workflow engine, or authorization workflow engine.

Future additions should first answer:

1. Who owns this?
2. Is it reachable from `Runtime`?
3. Is it reasoning or execution?
4. Can another system own it instead?

If the answers are unclear, draw the function block before adding code. If the function block cannot show a single owner for the behavior, the design is probably drifting.
