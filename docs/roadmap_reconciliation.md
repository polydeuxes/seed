# Executive Summary

The completed audits show that Seed has more reasoning foundation in place than the original roadmap assumed. The strongest existing capabilities are architectural invariants, deterministic rule inventory, conservative contradiction surfacing, current-state temporal projection, capability-resolution boundaries, and repository architecture metadata. Most remaining work is not blocked by `Runtime`, `ToolExecutor`, or projection changes; it is blocked by missing inventories, characterization tests, vocabulary, and read-only documentation.

The reconciled implementation priority is therefore conservative:

1. Keep Core MVP focused on knowledge, evidence, facts, relationships, explanations, `ToolNeed`, read-only capability resolution, registered operation candidates, and provider/handoff recommendations.
2. Prefer documentation, invariant tests, and read-only inventory helpers over new runtime services.
3. Avoid any item that starts to resemble `RuntimeLoop`, planning engines, workflow systems, schedulers, hidden tool selection, automatic retries, or internal orchestration.
4. Treat as-of temporal projection, capability verification, and repository self-observation as future read-only designs unless explicitly authorized later.

The single most valuable next implementation target is a **capability-verification terminology and inventory test pack**: tests and docs that prove `known_capability`, `registered_operations`, provider recommendations, and handoff candidates are not verified capability statuses, plus an inventory of checked-in `verify_*` operations showing whether they can produce positive verification. This has high reasoning value, low architectural risk, low LOC, and protects the most likely future confusion point without executing anything.

# Audit Findings Matrix

| Roadmap item | Reconciled status | Existing capability | Remaining gap | Blocker type | Priority |
| --- | --- | --- | --- | --- | --- |
| Explicit invariants | Already implemented | `docs/invariants.md` defines the accepted architecture boundaries, and invariant tests cover absence of `RuntimeLoop`, `request_tool` non-execution, `call_tool` execution ownership, catalog handoff metadata, and ledger/projection ownership. | Broader quarantine coverage can still be added for legacy planning artifacts. | Inventory/tests/docs only | Core MVP |
| Rule inventory / explain-rules | Already implemented | `seed_runtime/rule_inventory.py`, `scripts/seed_local.py --rules`, and `--explain-rules` expose a deterministic read-only inventory over catalogs, graph validation, and capability resolution rules. | Keep inventory synchronized as catalogs grow. | Inventory/tests/docs only | Core MVP |
| Contradiction handling | Partially implemented | `FactConflict`, standalone read-only contradiction detection, graph validation issues, ambiguous explanations, stale filtering, and confidence-view contradiction penalties exist. Characterization tests pin current behavior. | No unified conflict lifecycle for `disputed`, fact-level `superseded`, first-class `uncertain`, normalized competing evidence, or automatic truth arbitration. | Mostly missing vocabulary/tests/docs; automatic resolution would require new architecture and should be avoided. | Near-term for docs/tests; long-term for optional read models |
| Temporal reasoning | Partially implemented | Event ledger append order, timestamps, fact expiry, stale views, latest-current projection, projection cache invalidation, and temporal characterization tests exist. | No supported as-of event/timestamp API, belief timeline, why-then explanation, or what-changed semantic timeline. | As-of read helper needs architecture design; current semantics need tests/docs only. | Near-term characterization; long-term read-only as-of design |
| Capability verification | Partially implemented around boundaries; verified capability is missing | Requested capability, catalog-known capability, registered operation candidates, provider recommendations, handoff candidates, observations, evidence, facts, tool results, confidence, and expiry exist. | No scoped verification status, vocabulary, predicates/read model, evidence requirements, expiry policy, failed/stale verification semantics, or inventory of `verify_*` operation meaning. | Inventory/tests/docs first; verified capability read model blocked by missing architecture/vocabulary. | Highest-value next step |
| Self-observation | Partially implemented as repository metadata; missing as Seed observations | Architecture generator, `__seed_arch__` metadata, generated architecture graph, ownership docs, invariants, and rule inventory exist. | No repository observation source, repository predicates/entities/relationships, generated documentation index, semantic drift report, or projection into Seed facts. | Missing architecture for observation-source ingestion; docs/design can proceed. | Long-term; design-only near-term |

# Already Implemented Capabilities

## Architecture and ownership invariants

- `Runtime` remains the canonical runtime boundary.
- `RuntimeLoop` is absent from active runtime paths.
- `request_tool` records and resolves a capability gap without executing registered operations.
- `call_tool` is the only `Runtime` path that invokes `ToolExecutor`.
- `ToolExecutor` owns registered-operation execution.
- `CapabilityCatalog` remains read-only capability/provider metadata.
- `CapabilityRecommendation.operation` is handoff/provider metadata rather than a registered operation invocation.
- `EventLedger` owns append-only events.
- `ProjectionStore` owns cached latest-current projection snapshots and does not own events.

These are both documented and partly guarded by tests. The original roadmap item for explicit invariants should be considered implemented for Core MVP purposes.

## Deterministic rule inventory

The rule inventory roadmap item is implemented as a read-only inventory surface. Current coverage includes:

- predicate catalog entries;
- predicate mapping entries;
- relationship catalog entries;
- entity type catalog entries;
- inference catalog entries;
- graph validation rules;
- capability-resolution rules.

The CLI surface is intentionally read-only and does not construct runtime execution paths, append ledger events, execute tools, or create a new rule engine.

## Current-state temporal projection

Seed already has a narrow but explicit temporal model:

- append-only event history;
- event timestamps;
- observation/evidence/fact/support timestamps;
- fact expiry;
- stale fact views and refresh recommendations;
- deterministic latest-current projection;
- latest-current projection snapshot caching.

This is enough for current-state reasoning and provenance-backed explanations, but not enough for full historical/as-of reasoning.

## Conservative contradiction surfacing

Seed already surfaces disagreement without resolving truth:

- single-cardinality durable predicate conflicts;
- multi-cardinality preservation without conflict;
- measurement latest-sample behavior;
- standalone read-only contradiction scans;
- graph validation warnings/errors;
- ambiguous/conflicting explanation responses;
- read-only confidence projection penalties.

This is valuable because it preserves provenance and avoids hidden truth arbitration.

## Capability-resolution boundaries

Seed already distinguishes requested capability, catalog-known capability, registered operation candidates, provider recommendations, and handoff candidates. The important implemented reasoning value is the boundary: capability resolution reports inventory and recommendations without executing verification, authorizing actions, mutating state, or calling `ToolExecutor`.

## Repository knowledge artifacts

Seed already has repository-derived architecture artifacts:

- architecture generator output;
- `__seed_arch__` ownership metadata;
- generated architecture graph;
- architecture and invariant documentation;
- audit documents;
- rule inventory.

These artifacts are not yet Seed observations or facts, but they are useful source material for future self-observation.

# Partially Implemented Capabilities

## Contradiction handling

Partially implemented:

- `conflict` exists through `FactConflict`, standalone contradiction views, graph issues, explanation conflict attachments, and confidence projection penalties.
- `uncertain` exists indirectly through confidence, ambiguous explanations, unknown entity types, unsupported confidence reasons, and no-current-belief statuses.
- `stale` exists through expiry fields, stale listing, refresh recommendations, and default current-query filtering.
- competing evidence exists through separate supports, competing beliefs, evidence graph support views, and contradiction evidence attachment.

Still missing:

- first-class `disputed` state;
- fact/support/evidence-level `superseded` state;
- unified conflict lifecycle;
- normalized competing-evidence object;
- explicit `why_not()` API;
- truth-maintenance or automatic resolution, which should not be added to Core MVP.

## Temporal reasoning

Partially implemented:

- deterministic latest-current state;
- event append-order projection;
- timestamps and expiry;
- measurement current/history behavior;
- stale filtering and recommendations;
- projection cache invalidation by latest event id;
- characterization tests for current semantics.

Still missing:

- as-of event projection;
- as-of timestamp projection;
- belief timelines;
- why-then explanations;
- semantic what-changed timelines;
- historical projection cache, which should not be introduced casually.

## Capability verification

Partially implemented around adjacent terms:

- requested capability is represented by `ToolNeed`;
- catalog-known capability is represented by `CapabilityCatalogEntry`;
- registered operation candidates are represented by visible `ToolSpec.capabilities` matches;
- provider recommendations and handoff candidates are read-only catalog/ranker metadata;
- observations/evidence/facts/tool results could support future verification evidence.

Still missing:

- canonical verification status vocabulary;
- scoped verification target model;
- verification predicates or read model;
- evidence requirements for positive verification;
- failed/stale/unverified status semantics;
- provider-reported availability vocabulary;
- local observed availability mapping;
- inventory tests for checked-in `verify_*` operations.

## Self-observation

Partially implemented as repository metadata:

- generated architecture graph already contains fact-like nodes and edges;
- source metadata identifies owners and layers;
- invariants and audits describe expected architecture behavior;
- graph artifacts can support future drift detection.

Still missing:

- repository observation source;
- repository source confidence policy;
- architecture predicates and entity types;
- projection into Seed facts/relationships;
- documentation index;
- semantic drift report;
- unreachable/experimental component classifications.

# Missing Capabilities

## Blocked by missing architecture

These should not be implemented until a design is accepted:

1. **Read-only as-of temporal projection API**
   - Needs an explicit boundary for replaying to event id/timestamp without changing `ProjectionStore` behavior.
   - Must not turn `ProjectionStore` into a historical truth store.

2. **Belief timelines and why-then explanations**
   - Need an explanation model for historical support and event deltas.
   - Should remain read-only and replay-derived.

3. **Verified capability read model**
   - Needs scoped capability verification concepts, statuses, predicates, evidence requirements, and expiry policy.
   - Must not be driven automatically by capability resolution.

4. **RepositoryObservationSource**
   - Needs repository source type, confidence policy, entity/predicate/relationship vocabulary, and ingestion boundary.
   - Must not introduce shell execution, network calls, or self-mutation.

5. **Semantic architecture drift detection**
   - Needs expected-fact vocabulary and observed-fact vocabulary before comparing architecture facts.
   - Should be report-only.

## Blocked only by missing inventory, tests, or docs

These are safe high-value next steps because they do not need runtime or projection changes:

1. Expand invariant/quarantine tests for historical planning artifacts.
2. Add capability-verification terminology/invariant tests proving resolution fields are not verification statuses.
3. Inventory checked-in `verify_*` operations and classify whether each can produce positive verification.
4. Document proposed capability verification status vocabulary without wiring it into runtime behavior.
5. Add documentation-backed contradiction characterization around `disputed`, `superseded`, `uncertain`, and `stale` terminology.
6. Keep rule inventory docs/tests synchronized with catalog changes.
7. Draft a repository observation source design document.
8. Draft a documentation index or audit index without projecting it into state.

# Highest Value Next Steps

## 1. Capability-verification terminology and inventory tests

- **Reasoning value:** High.
- **Architectural risk:** Low.
- **Implementation complexity:** Low.
- **Why:** Prevents the most dangerous semantic confusion: treating a known capability, registered candidate, provider recommendation, or handoff candidate as verified evidence. It also establishes safe vocabulary for future verification work without executing operations.

## 2. Planning-artifact quarantine invariants

- **Reasoning value:** High.
- **Architectural risk:** Low.
- **Implementation complexity:** Low.
- **Why:** Protects Core MVP from recreating `RuntimeLoop`, planning engines, workflow systems, and internal orchestration.

## 3. Contradiction terminology characterization

- **Reasoning value:** Medium-high.
- **Architectural risk:** Low.
- **Implementation complexity:** Low.
- **Why:** Seed already reports conflicts, ambiguity, stale facts, and graph issues. Documentation-backed tests can prevent accidental introduction of automatic truth arbitration.

## 4. Temporal characterization and as-of design note

- **Reasoning value:** Medium-high.
- **Architectural risk:** Low for tests/docs; medium for implementation.
- **Implementation complexity:** Low for tests/docs; medium for an as-of helper.
- **Why:** Current latest-state temporal behavior is foundational. As-of reasoning is valuable, but the first step should be design and characterization, not API expansion.

## 5. Repository observation source design

- **Reasoning value:** Medium.
- **Architectural risk:** Low if docs-only; medium if ingestion is implemented.
- **Implementation complexity:** Low for design; medium for ingestion.
- **Why:** Existing architecture metadata is rich, but turning it into facts requires vocabulary and provenance design.

# Complexity Traps To Avoid

Avoid future work that recreates or approximates any of the following.

## RuntimeLoop

Do not add a second runtime, wrapper runtime, recursive runtime loop, autonomous execution loop, or model-driven internal loop. `Runtime` remains canonical.

## Planning engines

Do not promote `ActionPlan`, `HandoffPlan`, `ExecutionProposal`, or `ExecutionAuthorization` into Core MVP orchestration artifacts. If retained, they should remain historical, compatibility, or non-core concepts.

## Workflow systems

Do not add DAG execution, schedulers, workflow retries, multi-step tool chains, hidden tool selection, or automatic provider invocation as part of reasoning work.

## Internal orchestration

Do not convert capability resolution into execution, verification, scheduling, policy authorization, pending-action creation, or provider calls. Recommendation metadata must remain metadata.

## Truth-maintenance engines

Do not add automatic conflict resolution, fact deletion, confidence mutation, or belief arbitration for contradictions. Preserve evidence and surface disagreement.

## Temporal databases

Do not turn `ProjectionStore` into a historical projection store or temporal database. Historical/as-of answers should be explicitly designed as read-only replay views if they are added later.

## Self-modification

Do not allow self-observation work to mutate repository files, execute shell commands through runtime paths, call network services, or treat internal repository scans as privileged orchestration.

# Updated Roadmap

## Core MVP

1. **Preserve architecture invariants**
   - **Reasoning value:** High
   - **Architectural risk:** Low
   - **Implementation complexity:** Low
   - **Recommendation:** Maintain and expand invariant tests when architecture boundaries change.

2. **Maintain deterministic rule inventory**
   - **Reasoning value:** High
   - **Architectural risk:** Low
   - **Implementation complexity:** Low
   - **Recommendation:** Keep the read-only inventory synchronized with catalog and validation-rule changes.

3. **Add capability-verification terminology and inventory tests**
   - **Reasoning value:** High
   - **Architectural risk:** Low
   - **Implementation complexity:** Low
   - **Recommendation:** This is the single most valuable next implementation target.

4. **Add planning-artifact quarantine coverage**
   - **Reasoning value:** High
   - **Architectural risk:** Low
   - **Implementation complexity:** Low
   - **Recommendation:** Ensure historical planning artifacts cannot drift into runtime orchestration.

## Near-term

5. **Contradiction terminology characterization**
   - **Reasoning value:** Medium-high
   - **Architectural risk:** Low
   - **Implementation complexity:** Low
   - **Recommendation:** Document and test current meanings of `conflict`, `uncertain`, `stale`, `superseded`, and `disputed` without adding resolution behavior.

6. **Temporal semantics characterization refresh**
   - **Reasoning value:** Medium-high
   - **Architectural risk:** Low
   - **Implementation complexity:** Low
   - **Recommendation:** Continue pinning append-order, timestamp, measurement, expiry, and cache semantics.

7. **Repository observation source design document**
   - **Reasoning value:** Medium
   - **Architectural risk:** Low while docs-only
   - **Implementation complexity:** Low
   - **Recommendation:** Design source type, provenance, confidence policy, predicates, entity types, and relationship vocabulary before implementation.

8. **Documentation/audit index**
   - **Reasoning value:** Medium
   - **Architectural risk:** Low
   - **Implementation complexity:** Low
   - **Recommendation:** Create an index of architecture, invariant, reasoning, temporal, contradiction, capability, and self-observation docs.

## Long-term

9. **Read-only as-of projection helper**
   - **Reasoning value:** High
   - **Architectural risk:** Medium
   - **Implementation complexity:** Medium
   - **Recommendation:** Only implement after design clarifies event-id/timestamp semantics and confirms no `ProjectionStore` behavior change.

10. **Why-then and what-changed explanations**
    - **Reasoning value:** High
    - **Architectural risk:** Medium
    - **Implementation complexity:** Medium-high
    - **Recommendation:** Build only as read-only explanation views over ledger replay and provenance.

11. **Capability verification read model**
    - **Reasoning value:** High
    - **Architectural risk:** Medium
    - **Implementation complexity:** Medium
    - **Recommendation:** Implement only after vocabulary, scope, predicates, evidence requirements, failure semantics, and expiry policy are documented and tested.

12. **Repository self-observation ingestion**
    - **Reasoning value:** Medium-high
    - **Architectural risk:** Medium
    - **Implementation complexity:** Medium-high
    - **Recommendation:** Implement only as read-only observations/facts/relationships, never self-mutation or orchestration.

13. **Semantic architecture drift report**
    - **Reasoning value:** Medium
    - **Architectural risk:** Medium
    - **Implementation complexity:** Medium
    - **Recommendation:** Add after repository facts and expected invariant facts have a stable vocabulary.

## Experimental

14. **Unified conflict/read-model vocabulary**
    - **Reasoning value:** Medium
    - **Architectural risk:** Medium
    - **Implementation complexity:** Medium
    - **Recommendation:** Explore as a read-only explanatory layer, not a truth-maintenance system.

15. **Provider-reported availability modeling**
    - **Reasoning value:** Medium
    - **Architectural risk:** Medium-high
    - **Implementation complexity:** Medium
    - **Recommendation:** Treat provider claims as evidence with trust, scope, and expiry; do not make recommendations executable.

16. **Local observed availability mapping**
    - **Reasoning value:** Medium
    - **Architectural risk:** Medium-high
    - **Implementation complexity:** Medium-high
    - **Recommendation:** Allow only explicitly safe/read-only observation methods, and never trigger them from capability resolution.

17. **Unreachable or experimental component classification**
    - **Reasoning value:** Low-medium
    - **Architectural risk:** Medium
    - **Implementation complexity:** Medium
    - **Recommendation:** Defer until self-observation vocabulary exists.

## Items with low reasoning value per complexity

1. Automatic planning or workflow execution.
2. Runtime-controlled verification of capabilities.
3. Provider invocation from capability recommendations.
4. Historical projection caching inside `ProjectionStore`.
5. Automatic contradiction resolution or confidence mutation.
6. Self-modifying self-observation.
7. General-purpose scheduling, retry, or orchestration layers.

These items increase complexity and architectural risk while providing little Core MVP reasoning value.
