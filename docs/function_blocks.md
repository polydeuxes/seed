> **Historical/stale after PR 1918.** This document is preserved as historical testimony only. Its Runtime, RuntimeLoop, Decision, Policy, Execution, ActionPlan, HandoffPlan, ExecutionProposal, ExecutionAuthorization, PendingAction, request_tool, call_tool, and builder-candidate language is not current architecture or operator instruction.

# Function Blocks

These function-block diagrams document the current core Seed architecture. They are guardrails for ownership, not implementation tasks.

## Knowledge Pipeline

```mermaid
flowchart TD
    InputInspector --> ObservationNormalizer
    ObservationNormalizer --> ObservationIngestor
    ObservationIngestor --> EventLedger
    EventLedger --> StateProjector

    PredicateCatalog --> StateProjector
    RelationshipCatalog --> StateProjector
    EntityTypeCatalog --> StateProjector
    InferenceCatalog --> StateProjector

    StateProjector --> ProjectedState[Projected State]

    ProjectedState --> WhyQueries[Why Queries]
    ProjectedState --> ImpactQueries[Impact Queries]
    ProjectedState --> RelationshipsQueries[Relationships Queries]
    ProjectedState --> CurrentFacts[Current Facts]
    ProjectedState --> GraphIssues[Graph Issues]
```

The knowledge pipeline turns inputs into observations, observations into ledger-backed knowledge, and ledger-backed knowledge into projected state. Query surfaces consume projected state; they do not own the event history.

## Capability Resolution Pipeline

```mermaid
flowchart TD
    ToolNeed --> ToolNeedService

    ToolNeedService --> ToolRegistry
    ToolNeedService --> CapabilityCatalog

    ToolRegistry --> RegisteredOperationCandidates[Registered Operation Candidates]
    CapabilityCatalog --> ProviderRecommendations[Provider Recommendations]
    CapabilityCatalog --> HandoffCandidates[Handoff Candidates]

    RegisteredOperationCandidates --> CapabilityResolution[Capability Resolution]
    ProviderRecommendations --> CapabilityResolution
    HandoffCandidates --> CapabilityResolution
```

`ToolNeedService` owns capability-gap creation and capability resolution. `ToolRegistry` owns registered operation inventory. `CapabilityCatalog` owns capability metadata, provider recommendations, and handoff recommendations.

## Execution Boundary

```mermaid
flowchart TD


    CallTool --> ToolExecutor

    ToolExecutor --> ToolRegistry
    ToolExecutor --> ToolValidationService
    ToolExecutor --> ToolExecutionPolicyService
    ToolExecutor --> PendingActionService
```

Only `call_tool` may enter `ToolExecutor`. `request_tool`, `answer`, `question`, and `refusal` remain runtime response or reasoning paths. Execution starts at `ToolExecutor`; earlier blocks validate, route, explain, or reason.

## Projection Cache

```mermaid
flowchart TD
    EventLedger --> StateProjector
    StateProjector --> ProjectionStore
    ProjectionStore --> CLIQueries[CLI Queries]
```

`ProjectionStore` caches projections.

`EventLedger` stores history.

The projection cache is not a second event store. Cached projections can be rebuilt from append-only events and projector logic.
