# Projection Integrity Summary Characterization

## Purpose

This document characterizes whether Seed can summarize Knowledge Integrity state
from existing projected knowledge. It is an audit and vocabulary exercise, not an
implementation plan for a new reporting engine.

The central finding is:

> A coherent **Projection Integrity Summary** is feasible as a small read-only
> composition over existing projected structures. Most source signals already
> exist; the gap is aggregation, naming, and joining rather than runtime behavior.

A Projection Integrity Summary should answer questions such as:

- How many projected facts lack evidence support?
- How many current support groups are conflicted?
- How many conservative contradictions are present?
- How many graph validation issues exist?
- How many facts are stale, and which capabilities are recommended for refresh?
- Which capabilities are verified, provider-reported, stale, unverified, or
  unknown?
- Which knowledge gaps are only implicit, such as missing observations or missing
  evidence for a queried claim?

It must not decide truth, execute verification, perform refresh, resolve
contradictions, mutate facts, mutate projections, call providers, invoke tools,
plan work, or become an alternate knowledge system.

## Scope and non-goals

This characterization is documentation only. It does not change `Runtime`,
`ToolExecutor`, `EventLedger`, `ProjectionStore`, state projection, fact
mutation, projection mutation, provider behavior, tool execution, orchestration,
planning, contradiction resolution, verification execution, refresh execution, or
LLM reasoning.

A Projection Integrity Summary is in scope only if it remains:

- **read-only**: derived from an already-built projected `State` and read-only
  helper views;
- **projection-backed**: no new persistence or parallel truth state;
- **evidence-backed**: provenance and support come from facts/evidence already in
  projected state;
- **inventory-backed**: capability verification status comes from the existing
  capability inventory interpretation of projected facts.

Projection Integrity Summary output may include navigation hints from aggregate
counts to existing inventory CLI surfaces. These hints are read-only pointers
only: they reuse existing inventories and do not imply resolution, repair,
verification execution, refresh execution, fact mutation, or projection mutation.

It is out of scope for a Projection Integrity Summary to become any of the
following:

- `IntegrityEngine`
- `TrustEngine`
- `VerificationEngine`
- `RefreshEngine`
- `ContradictionResolver`
- `CapabilityExecutor`
- provider caller
- planner
- workflow engine
- agent loop
- parallel truth system
- LLM-generated trust system

## Files inspected

Required documents inspected:

- `docs/knowledge_maintenance_reconciliation.md`
- `docs/knowledge_lifecycle_reconciliation.md`
- `docs/why_not_explanation_characterization.md`
- `docs/why_not_vocabulary.md`
- `docs/explanation_contract_vocabulary.md`
- `docs/capability_verification_vocabulary.md`
- `docs/state.md`
- `docs/invariants.md`

Required runtime/read-model files inspected:

- `seed_runtime/facts.py`
- `seed_runtime/state.py`
- `seed_runtime/state_views.py`
- `seed_runtime/contradictions.py`
- `seed_runtime/capability_inventory.py`
- `seed_runtime/evidence_graph.py`

Relevant test files inspected:

- `tests/test_contradictions.py`
- `tests/test_graph_validation.py`
- `tests/test_fact_support_aggregation.py`
- `tests/test_capability_inventory.py`
- `tests/test_evidence_graph.py`
- `tests/test_state_views.py`
- `tests/test_seed_local_script.py`
- `tests/test_temporal_characterization.py`
- `tests/test_capability_verification_invariants.py`

Relevant CLI file inspected for surfaced read-only commands:

- `scripts/seed_local.py`

## Existing integrity signals

Seed already has multiple integrity signals distributed across projected state,
read-only views, and CLI surfaces.

### Fact support and current belief signals

Implemented structures:

- `Fact` stores subject, predicate, value, dimensions, evidence IDs, source type,
  confidence, observation time, optional expiry, inferred/source-fact metadata,
  and inference rule metadata.
- `FactSupport` aggregates support for a subject/predicate/value/dimensions
  claim. It records supporting fact IDs, source types, confidence, first and
  latest observation times, expiry metadata, predicate semantics, and whether the
  support is aggregate durable support or a current measurement sample.
- `State.get_fact_supports(...)`, `State.get_fact_support(...)`,
  `State.get_best_fact(...)`, and `State.get_current_facts(...)` expose the
  projected support and selected current belief without mutating state.
- Durable facts aggregate independent support; measurement predicates choose a
  latest current sample and retain bounded history.

Summary relevance:

- Counts are possible today from `state.fact_supports`, `state.facts`, current
  support queries, and measurement/durable predicate semantics.
- Inventories are possible today by listing facts, support groups, and current
  representative facts.
- Existing state summary CLI already counts facts, durable facts, measurement
  current samples, conflicts, and stale facts.

Limitation:

- There is no single integrity summary object that joins fact support counts with
  evidence, contradiction, graph, stale, and capability inventory counts.

### Unsupported facts

Implemented structures:

- `EvidenceGraph` is derived from projected `State` and links evidence nodes to
  fact evidence views.
- `EvidenceSummary.unsupported_fact_count` counts facts with no linked evidence.
- `unsupported_fact_views(state)` inventories unsupported facts.
- `format_unsupported_facts(...)` and the `--unsupported-facts` CLI surface
  expose unsupported facts.

Summary relevance:

- Counts already exist.
- Inventories already exist.
- Views already exist.
- CLI surfaces already exist.

Boundary:

- Unsupported means no linked evidence in the Evidence Graph view.
- Unsupported is not false, disproof, failed verification, or negative evidence.

### Conflicted facts / projection-level fact conflicts

Implemented structures:

- `FactConflict` records projected disagreement for a resolved subject,
  predicate, dimensions scope, competing values, optional winning value, optional
  best fact ID, conflicting fact IDs, and reason.
- `State.fact_conflicts` stores current projected conflicts.
- `State.get_fact_conflicts(include_expired=False)` exposes conflicts and can
  include expired facts when requested.
- The `--fact-conflicts` CLI surface exposes projected fact conflicts.

Summary relevance:

- Counts already exist from `len(state.get_fact_conflicts())` or
  `len(state.fact_conflicts)`.
- Inventories already exist through `FactConflict` records.
- CLI surface exists.

Boundary:

- Conflicted is not identical to contradicted. `FactConflict` is a projection
  support/current-selection signal, while standalone contradictions are a
  conservative audit view.
- A winning value, when present, is a projection selection outcome, not a truth
  judgment.

### Contradictions

Implemented structures:

- `Contradiction` is a read-only contradiction report over projected `State` and
  optional Evidence Graph.
- `build_contradictions(...)` conservatively reports exact same-subject,
  same-predicate, different-value conflicts for exclusive predicates.
- `ContradictionSummary` counts contradictions, affected facts, and severity
  buckets.
- `find_contradictions_for_fact(...)` inventories contradictions involving a
  specific fact.
- The `--contradictions` CLI surface prints contradiction summaries and evidence
  attachments.

Summary relevance:

- Counts already exist.
- Inventories already exist.
- Views already exist.
- CLI surface exists.

Boundary:

- Contradiction Detection does not resolve facts, rewrite facts, choose a winner,
  or mutate state.
- Contradicted is not automatically false; it is an integrity signal over
  competing projected assertions.

### Graph issues

Implemented structures:

- `GraphValidationIssue` records relationship/type validation issues including
  severity, subject, relationship, object, relationship IDs, source fact IDs,
  reason, hint, and expected/actual subject/object types.
- `GraphValidator` derives deterministic issues from projected relationships and
  entity type catalogs.
- `State.get_graph_issues(...)` filters issues by severity.
- `build_issue_view(state)` maps graph issues into read-only `IssueView` objects.
- Existing CLI state summary and graph issue output surface graph issue counts,
  warnings, and errors.

Summary relevance:

- Counts already exist from `state.graph_issues` and severity filters.
- Inventories already exist through `GraphValidationIssue` and `IssueView`.
- Views already exist.
- CLI surfaces exist through graph issue commands and state summary.

Boundary:

- Graph issues are shape/type/integrity issues, not contradiction reports and not
  graph repair instructions.
- A graph warning or error is not a truth value for a fact.

### Stale facts and refresh recommendations

Implemented structures:

- `Fact.expires_at` and `is_fact_expired(...)` represent fact expiry.
- Default current support excludes expired facts.
- `State.get_stale_facts()` inventories expired facts.
- `StaleFactRefreshRecommendation` records a deterministic read-only capability
  recommendation for refreshing an expired fact.
- `State.get_stale_fact_refresh_recommendations()` maps stale facts to
  recommended capabilities using predicate-to-capability mapping with a fallback.
- CLI state summary counts stale facts, and `--stale-facts` /
  `--stale-fact-refreshes` expose stale facts and refresh recommendations.

Summary relevance:

- Counts already exist from `len(state.get_stale_facts())`.
- Inventories already exist for stale facts and refresh recommendations.
- CLI surfaces exist.

Boundary:

- Stale is not false.
- Refresh recommendation is not refresh execution.
- Expiry does not mutate facts, lower stored confidence, append events, or call
  providers.

### Capability verification status and support summaries

Implemented structures:

- `capability_verified` facts are interpreted by `build_capability_inventory(...)`.
- Capability inventory states are `verified`, `provider_reported`, `unverified`,
  `stale`, and `unknown`.
- `CapabilityInventoryEntry` includes supporting fact IDs, supporting evidence
  summaries, `CapabilitySupportSummary`, observation times, age, and reason.
- The inventory universe is derived from registered tools, `ToolNeed` records,
  and verification fact subjects.
- The `--capability-status` CLI surface exposes the inventory as read-only JSON.

Summary relevance:

- Counts are derivable by grouping inventory entries by state.
- Inventories already exist.
- Evidence/support summaries already exist per entry.
- CLI surface exists.

Boundary:

- Capability verification execution is not implemented.
- Unverified is not false, unavailable, failed verification, or negative
  evidence.
- Verification status is not capability ownership.
- Registered operations, provider recommendations, requested capabilities, and
  known capability catalog entries do not imply verification.

### Unknown states

Partially implemented structures:

- Capability inventory has an `unknown` state for current `capability_verified`
  values outside the implemented vocabulary.
- Evidence Graph uses `unknown` for unclassified evidence node/source
  information.
- Entity type projection uses `unknown` when no stronger current type assertion
  exists, and graph validation can emit warnings when relationship endpoint type
  is unknown.
- Why-not vocabulary names `Unknown` as a state where Seed lacks enough projected
  classification to assign a more specific status.

Summary relevance:

- Counts are possible in capability inventory, evidence node summaries, and graph
  issue reasons, but there is no unified unknown-state summary.

Boundary:

- Unknown is not false, failed, unavailable, or disproof.

### Missing evidence

Partially implemented structures:

- Unsupported facts are explicit Evidence Graph facts with no linked evidence.
- `build_fact_evidence_view(state, fact_id)` returns `None` when the fact ID does
  not exist and a view with no evidence when it exists without evidence.
- `find_evidence_for_fact(...)` can return no matching evidence-backed fact view.

Summary relevance:

- Existing unsupported fact counts cover a concrete subset of missing evidence:
  projected facts without linked evidence.
- A broader missing-evidence query taxonomy is not implemented.

Boundary:

- Missing evidence is not disproof.
- Missing evidence for a queried claim is different from an unsupported projected
  fact and different from no matching fact.

### Missing observations

Missing / only implicit structures:

- `State.observations`, `ObservationView`, and Evidence Graph make present
  observations inspectable.
- A caller can infer absence by querying projected observations/evidence/facts
  and finding no match.

Summary relevance:

- No first-class missing-observation reason, count, inventory, or CLI summary
  exists.

Boundary:

- Missing observation is not negative evidence.
- Missing observation does not prove that the entity, relation, fact, or
  capability is absent.

### Historical and current knowledge

Implemented / partially implemented structures:

- Current knowledge is represented by latest projected `State`, support selection,
  current fact queries, current measurement samples, and state views.
- Historical source of truth remains the append-only EventLedger.
- Measurement history can be retained in bounded projected state for debug/read
  purposes.
- Expired facts remain stored in projected `State.facts` but default current
  support excludes them.
- `ProjectionStore` owns latest-current snapshots only and is not an as-of
  projection API.

Summary relevance:

- Current counts are feasible from projected `State` and state views.
- Historical facts can be partially represented by retained expired facts and
  bounded measurement history, but complete historical/as-of summaries belong to
  EventLedger analysis and are not in scope for a projection-only integrity
  summary.

Boundary:

- Historical is not invalid.
- Current is not correct.
- Projection order is ledger append/insertion order, not timestamp order.

## Category classification

| Category | Classification | Counts today? | Inventory today? | View today? | CLI today? | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Unsupported facts | Implemented | Yes, `EvidenceSummary.unsupported_fact_count` | Yes, `unsupported_fact_views` | Yes, `FactEvidenceView` | Yes, `--unsupported-facts` | Evidence Graph subset: projected facts without linked evidence. |
| Conflicts | Implemented | Yes, `state.fact_conflicts` / `get_fact_conflicts` | Yes, `FactConflict` | Partial, via support/explanation and CLI formatting | Yes, `--fact-conflicts` | Projection-level support disagreement, not standalone contradiction. |
| Contradictions | Implemented | Yes, `ContradictionSummary` | Yes, `Contradiction` | Yes | Yes, `--contradictions` | Conservative exact-subject/exclusive-predicate audit view. |
| Graph issues | Implemented | Yes, state summary and `get_graph_issues` | Yes, `GraphValidationIssue` | Yes, `IssueView` | Yes | Shape/type validation issue, not contradiction or repair. |
| Staleness | Implemented | Yes, `get_stale_facts` | Yes, stale fact list | Partial, direct state methods rather than unified summary view | Yes, `--stale-facts` and state summary | Expired facts excluded from current support by default. |
| Refresh recommendations | Implemented | Yes, count recommendations from list length | Yes, `StaleFactRefreshRecommendation` | Partial, direct state method | Yes, `--stale-fact-refreshes` | Recommendation only; no execution. |
| Verification | Partially implemented | Derivable by grouping inventory entries | Yes, `CapabilityInventoryEntry` | Yes, inventory entries | Yes, `--capability-status` | Inventory-backed status exists; verification execution does not. |
| Capability evidence/support summaries | Implemented for inventory entries | Derivable | Yes | Yes | Yes through JSON | Summaries derive from `CapabilitySupportSummary` and evidence nodes. |
| Unknown states | Partially implemented | Derivable per surface | Partial | Partial | Partial | Exists in capability inventory, evidence type, entity typing/graph issues; not unified. |
| Missing evidence | Partially implemented | Yes for unsupported projected facts | Yes for unsupported projected facts | Yes for fact evidence views | Yes for unsupported facts | General queried missing-evidence taxonomy is missing. |
| Missing observations | Missing / implicit | No | No | Present-observation views only | No direct missing-observation CLI | Absence can be inferred but should not become negative evidence. |
| Integrity caveats | Partially implemented | Not a count concept | Vocabulary exists | Documentation exists | No unified caveat surface | Caveats are critical to avoid truth/trust semantics. |
| Historical knowledge | Partially implemented | Partial, via retained expired facts/history | Partial | Partial | Partial | Projection-only summary should avoid pretending to be an as-of ledger report. |
| Current knowledge | Implemented | Yes | Yes | Yes | Yes | Latest projected state supports current summary. |

## Implemented integrity surfaces

The following read-only surfaces can feed a Projection Integrity Summary without
new runtime behavior:

- `build_state_summary(state)` for generic projected facts, observations,
  requirements, capabilities, issues, last event, and projection version.
- `State.get_fact_supports(...)`, `State.get_fact_support(...)`,
  `State.get_best_fact(...)`, and `State.get_current_facts(...)` for current
  fact support and current belief.
- `State.get_fact_conflicts(...)` for projection-level conflicts.
- `build_evidence_summary(state)`, `build_evidence_graph(state)`,
  `build_fact_evidence_view(state, fact_id)`, `find_evidence_for_fact(...)`, and
  `unsupported_fact_views(state)` for evidence support and unsupported facts.
- `build_contradictions(...)`, `build_contradiction_summary(...)`, and
  `find_contradictions_for_fact(...)` for conservative contradictions.
- `State.get_graph_issues(...)` and `build_issue_view(state)` for graph/type
  integrity issues.
- `State.get_stale_facts()` and
  `State.get_stale_fact_refresh_recommendations()` for stale facts and refresh
  recommendations.
- `build_capability_inventory(state)` for capability verification inventory and
  capability evidence/support summaries.

Existing CLI surfaces also expose many of these pieces individually:

- `--state-summary`
- `--fact-support`
- `--best-fact`
- `--current-facts`
- `--fact-conflicts`
- `--stale-facts`
- `--stale-fact-refreshes`
- `--evidence`
- `--why-fact`
- `--unsupported-facts`
- `--contradictions`
- `--confidence`
- `--current-issues`
- `--current-capabilities`
- `--capability-status`

## Partial surfaces and gaps

The main gap is not raw data. It is that each existing surface answers its own
question and there is no single normalized read-only integrity summary that
joins them.

Partial or missing concepts:

1. **Unified integrity counts.** Counts exist per surface, but there is no compact
   object that reports unsupported fact count, conflict count, contradiction
   severity buckets, graph issue buckets, stale fact count, refresh
   recommendation count, and capability verification state counts together.
2. **Unified integrity inventory.** Inventories exist per surface, but there is
   no common top-level inventory grouping unsupported facts, conflicts,
   contradictions, graph issues, stale facts, refresh recommendations, and
   capability status.
3. **Unknown-state summary.** Unknown exists in capability inventory, evidence
   typing, and entity typing/graph validation, but not as a normalized integrity
   summary dimension.
4. **General missing-evidence reasons.** Unsupported facts are implemented, but
   missing evidence for a query can also mean no such fact, no evidence link,
   unsupported inferred support, a dimension mismatch, an alias mismatch, or a
   pruned measurement sample.
5. **Missing-observation explanations.** Present observations are inspectable;
   absence of observations is only implicit and should remain carefully worded.
6. **Historical summary boundary.** Projection has expired facts and bounded
   measurement history, but a projection-only summary should not claim complete
   historical/as-of coverage.
7. **Recommendation-to-verification join.** Capability recommendations and
   verification inventory are both present, but there is no common view that says
   a recommended capability is known/requested/candidate/provider-recommended but
   unverified or stale.
8. **Caveat vocabulary in output.** Existing docs preserve distinctions such as
   unsupported-not-false and stale-not-false, but individual CLI surfaces do not
   always repeat all caveats.

## Summary feasibility findings

A coherent read-only Projection Integrity Summary is feasible now if it is
restricted to composition over existing structures.

A smallest feasible summary could include:

- projection metadata: workspace ID, last event ID, projection version;
- current projected inventory counts: facts, observations, capabilities, issues;
- evidence counts: evidence nodes, linked facts, unsupported facts;
- fact support counts: support groups, current facts if requested, conflicts;
- contradiction counts: total, affected facts, severity buckets;
- graph issue counts: total, warnings, errors;
- stale counts: stale facts and stale refresh recommendations;
- capability verification counts: verified, provider-reported, stale,
  unverified, unknown;
- optional inventories: unsupported facts, conflicts, contradictions, graph
  issues, stale facts, refresh recommendations, capability inventory entries;
- caveats describing the meaning of unsupported, unverified, stale,
  contradicted, missing evidence, missing observation, current, and historical.

This summary can be constructed entirely from existing structures:

```text
projected State
  -> State Views
  -> Evidence Graph / Evidence Summary
  -> FactSupport / FactConflict
  -> Contradiction Detection / Contradiction Summary
  -> GraphValidationIssue / IssueView
  -> stale facts / stale refresh recommendations
  -> Capability Inventory
  -> Projection Integrity Summary
```

No new event type, projection mutation, runtime route, executor behavior,
provider integration, verification run, refresh run, or LLM judgment is required.

## Knowledge Integrity relationship

Knowledge Integrity is the right architectural label for this concern. It asks
whether Seed can safely rely on what it currently knows by exposing support,
conflict, contradiction, graph, freshness, evidence, capability-verification,
and caveat signals.

The proposed summary would not create Knowledge Integrity; it would summarize the
integrity signals already distributed across projection and read-only views. It
would make Knowledge Integrity easier to inspect without changing ownership.

Important boundaries:

- Integrity Signal != Truth
- Unsupported != False
- Unverified != False
- Stale != False
- Contradicted != False
- Missing Evidence != Disproof
- Missing Observation != Negative Evidence
- Historical != Invalid
- Current != Correct
- Verification Status != Capability Ownership
- Refresh Recommendation != Refresh Execution

## Knowledge Selection relationship

Knowledge Selection decides what matters now for context composition,
explanation, and response. A Projection Integrity Summary would be useful input
to Knowledge Selection, but it should not become a selection policy or planner.

Selection-facing uses could include:

- warning that selected facts are unsupported, conflicted, stale, contradicted,
  or graph-problematic;
- exposing that a candidate capability is unverified or stale;
- showing why a stale fact produced a refresh recommendation without executing
  the refresh;
- giving explanation surfaces compact integrity caveats.

Boundaries:

- The summary may inform selection.
- The summary must not choose final answers, suppress facts, repair facts,
  adjudicate truth, execute capabilities, or acquire new observations.

## Complexity traps

Avoid these traps:

1. **Turning summary into an engine.** A summary should compose existing read
   models; it should not own policy, execution, repair, refresh, or truth.
2. **Collapsing distinct signals.** Unsupported, conflicted, contradicted, graph
   issue, stale, unverified, unknown, missing evidence, and missing observation
   are different states.
3. **Treating absence as negative proof.** Missing evidence and missing
   observation are not disproof.
4. **Treating verification inventory as execution.** Inventory state interprets
   facts; it does not run verification.
5. **Treating recommendations as actions.** Refresh recommendations do not call
   providers or append refresh events.
6. **Creating a parallel truth system.** Projection remains the source read
   model; the EventLedger remains append-only history; ProjectionStore remains a
   latest-current cache.
7. **Inventing LLM trust judgments.** The summary should not ask an LLM to rate
   trust or correctness.
8. **Pretending projection history is complete history.** Projection summaries
   should avoid as-of claims unless a separate ledger/as-of design exists.
9. **Over-normalizing too early.** Existing surfaces already work. A first step
   should join counts and references, not introduce a new ontology.

## Recommended smallest next step

Do not implement a new subsystem. The smallest next step is another
behavior-preserving documentation/design pass that defines a **Projection
Integrity Summary v0 read model shape** as a pure composition contract.

That next document or small design note should specify only:

- input: an already-built projected `State`;
- output: immutable summary fields and optional inventories;
- source for each field: existing function, state attribute, or view builder;
- caveat text for each signal;
- explicit non-goals: no mutation, no execution, no provider calls, no
  verification runs, no refresh runs, no planner, no resolver, no LLM judgment.

If implementation is considered later, it should be a small read-only helper that
reuses existing structures and tests that it does not mutate state, touch
`Runtime`, touch `ToolExecutor`, append events, or write projections.

## Final characterization

Projection Integrity Summary is **not missing as an architectural substrate**.
Seed already has enough projected integrity signals to construct one. What is
missing is a small unifying read-only composition surface and a shared output
vocabulary that keeps the existing distinctions intact.

The current status is:

- **Implemented:** unsupported fact counts/inventories, fact conflicts,
  contradictions and summaries, graph issue counts/inventories, stale fact
  inventories, refresh recommendations, current knowledge views, capability
  inventory entries, and many CLI surfaces.
- **Partially implemented:** unified integrity counts, unified integrity
  inventories, unknown-state summary, broad missing-evidence explanations,
  recommendation-to-verification joins, historical projection caveats, and
  caveat-rich output vocabulary.
- **Missing:** first-class missing-observation summaries and a single Projection
  Integrity Summary composition object.

A coherent summary is therefore feasible, but it should remain small, read-only,
projection-backed, evidence-backed, inventory-backed, and behavior-preserving.
