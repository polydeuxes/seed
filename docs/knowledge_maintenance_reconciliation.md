# Knowledge Maintenance Reconciliation

## Executive Summary

Repository evidence supports a coherent architectural concern around whether
projected knowledge remains safe to rely on, but the best current term is
**Knowledge Integrity**, not **Knowledge Maintenance**.

The candidate concepts are real and already distributed across the current
architecture:

- fact support and evidence links;
- projection-level `FactConflict` records;
- standalone read-only `Contradiction` reports;
- graph validation issues;
- fact expiry and stale-fact refresh recommendations;
- temporal current-vs-history behavior for durable and measurement predicates;
- read-only capability verification inventory;
- read-only confidence aggregation and contradiction penalties;
- explanation surfaces that expose current beliefs, ambiguity, conflicts,
  competing beliefs, and unsupported facts.

Together these answer a question that is distinct from Knowledge Acquisition and
Knowledge Selection:

```text
Can Seed still safely rely on what it currently knows?
```

This is not a new execution subsystem. The evidence supports a read-only
integrity/health concern over projected knowledge, not a `MaintenanceEngine`,
`TrustEngine`, `IntegrityEngine`, `ValidationEngine`, `ReasoningEngine`, or any
automated truth-management path.

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
- `docs/state.md`
- `docs/invariants.md`
- `docs/knowledge_acquisition_and_selection.md`
- `docs/explanation_contract_vocabulary.md`
- `docs/capability_verification_vocabulary.md`
- `docs/context_composition_vocabulary.md`
- `docs/knowledge_classification_vocabulary.md`
- `docs/temporal_reasoning_audit.md`
- `docs/contradiction_handling_audit.md`
- `docs/explainability_reconciliation.md`
- `seed_runtime/state.py`
- `seed_runtime/state_views.py`
- `seed_runtime/facts.py`
- `seed_runtime/contradictions.py`
- `seed_runtime/explanations.py`
- `seed_runtime/capability_inventory.py`

Adjacent architecture, generated documentation, and tests inspected where
relevant:

- `tests/test_contradictions.py`
- `tests/test_temporal_characterization.py`
- `tests/test_graph_validation.py`
- `tests/test_capability_inventory.py`
- `tests/test_fact_support_aggregation.py`
- `tests/test_state_views.py`
- `tests/test_architecture_invariants.py`

## Current Repository Structures

### Knowledge-first architecture

The README and architecture overview already place conflicts, explanation,
current-state projection, and capability handling downstream of observed and
evidence-backed knowledge. The canonical acquisition/selection document defines:

```text
Knowledge Acquisition:
Observation -> Evidence -> Fact -> Projection

Knowledge Selection:
Projected Knowledge -> Context Composition -> Explanation -> Response
```

It also says acquisition preserves source limitations, uncertainty, staleness,
and contradictions while deriving support, conflicts, relationships, entity
types, graph issues, and other projected read-model structures from events and
facts.

### State and projection

`State` is the current projected world model. It contains facts, evidence,
relationships, entity types, graph issues, `FactSupport`, and `FactConflict`.
`StateProjector` rebuilds inspectable state from ledger events, derives current
support, retains measurement history, projects conflicts, and validates graph
issues. This makes projection the current integration point for integrity
signals, but not a separate truth store.

### Fact support

`FactSupport` is the projected support record for one subject/predicate/value
claim. Durable predicates aggregate independent observations. Measurement
predicates identify the latest current sample instead of treating repeated values
as stronger durable support. Support records preserve supporting fact IDs, source
types, confidence, first/latest observation times, expiry status, predicate
semantics, and support kind.

### Fact conflicts and contradictions

Seed currently has two distinct read-only disagreement views:

1. `FactConflict` is projection-level disagreement for alias-resolved,
   single-cardinality durable facts with multiple non-expired values for the same
   subject, predicate, and dimensions.
2. `Contradiction` is a standalone audit/read-model view over projected `State`
   and optional Evidence Graph. It conservatively reports exact
   same-subject/same-predicate conflicts for exclusive predicates and does not
   decide which fact is correct.

These views are compatible but not identical. That distinction matters: graph
issues, fact conflicts, and contradictions are all integrity signals, but they
are not the same concept.

### Temporal semantics, staleness, and refresh recommendations

Seed already models temporal integrity in several conservative ways:

- facts can expire through `expires_at` and `is_fact_expired`;
- current support excludes expired facts by default and can include expired facts
  only when requested;
- durable facts aggregate support across observations;
- measurement facts use latest-current sample semantics and retain bounded
  history;
- stale facts can produce deterministic refresh capability recommendations;
- stale verification status reuses fact expiry semantics rather than inventing a
  new aging policy.

These structures are enough to distinguish stale from false, historical from
invalid, and refresh recommendation from execution.

### Graph validation

Graph validation reports deterministic `GraphValidationIssue` warnings or errors
for projected relationship/type problems. It reports topology or catalog-shape
issues. It does not remove relationships, alter entity types, rewrite aliases,
block projection, or prove fact truth.

### Explainability

The explanation contract exposes current beliefs, no-current-belief states,
ambiguity, competing beliefs, support, freshness, source types, and attached
conflicts for single-cardinality facts. Explanation is therefore a consumer and
communicator of integrity signals. It is not the owner of trust decisions.

### Capability verification inventory

Capability verification is already a read-only inventory concern. The implemented
inventory derives states from projected `capability_verified` facts and
`FactSupport`, reports `verified`, `provider_reported`, `unverified`, `stale`,
or `unknown`, and exposes supporting facts/evidence and age. It does not verify,
execute, call providers, route through runtime, or prove provider availability.

### Confidence handling

Confidence Aggregation is a read-only projection view over projected `State`, the
Evidence Graph, and Contradiction Detection. It estimates support strength and
may apply deterministic contradiction penalties to its own `FactConfidence`
records. It does not mutate `Fact.confidence`, mutate `FactSupport.confidence`,
select truth, resolve contradictions, or delete facts.

## Architectural Fit Finding

The concepts do form a coherent concern, but the repository evidence supports a
**read-only projected knowledge integrity concern** rather than an active
maintenance subsystem.

The concern answers:

```text
Can Seed still safely rely on what it currently knows, and what limitations must
be disclosed when it uses that knowledge?
```

It is separate from, but dependent on, acquisition and selection:

- Knowledge Acquisition answers: **What do we know?**
- Knowledge Integrity answers: **Can we still safely rely on what we know?**
- Knowledge Selection answers: **What matters right now?**

This third concern is not a parallel pipeline that creates knowledge or produces
responses. It is a cross-cutting read-model concern that annotates, reports, and
explains the health of projected knowledge.

## Terminology Findings

### Recommended term: Knowledge Integrity

`Knowledge Integrity` best fits current repository evidence because the existing
structures emphasize consistency, support, freshness, validation, and disclosure
without implying execution or mutation.

It naturally includes:

- support integrity;
- temporal integrity;
- conflict integrity;
- graph integrity;
- verification-status integrity;
- confidence/support-health reporting;
- projection consistency concerns.

### Why not Knowledge Maintenance as the canonical term?

`Knowledge Maintenance` is understandable, but it risks implying active upkeep:
refresh execution, verification execution, automatic repair, deletion, or truth
arbitration. The repository evidence does not support those behaviors.

`Maintenance` can remain an informal lifecycle word for stale facts and refresh
recommendations, but it should not name a subsystem unless future documentation
explicitly scopes it as read-only.

### Alternative terms considered

| Term | Finding |
| --- | --- |
| Knowledge Integrity | Best fit. Emphasizes consistency, freshness, support, and disclosure without implying execution. |
| Knowledge Quality | Plausible, but broader and less precise; may imply scoring or ranking beyond current structures. |
| Knowledge Health | Useful operator-facing metaphor, but too informal for canonical architecture. |
| Knowledge Validity | Too strong; current structures report issues and support, but do not prove truth. |
| Knowledge Trust | Risky; may imply trust decisions or provider trust policy that Seed does not implement. |
| Truth Maintenance | Too loaded; risks implying truth-maintenance systems, automatic revision, or belief deletion. |
| Knowledge Lifecycle | Useful for acquisition/history/expiry, but too broad and could overlap acquisition ownership. |

## Responsibility Candidates

Knowledge Integrity can responsibly include read-only characterization of:

- evidence and `FactSupport` availability;
- unsupported or weakly supported facts;
- contradictory or conflicting projected facts;
- ambiguous current beliefs;
- graph validation issues;
- fact expiry and staleness;
- refresh recommendations as recommendations only;
- current-vs-historical distinctions;
- capability verification inventory status;
- confidence summaries and contradiction penalties in read-only confidence views;
- projection consistency warnings;
- explanation-ready disclosure of limitations.

In short, it owns the vocabulary for integrity signals and the documentation
boundary that says how those signals should be interpreted.

## Responsibility Boundaries

Knowledge Integrity does **not** own:

- observation;
- evidence creation;
- fact creation;
- fact extraction;
- projection mutation outside normal replay paths;
- context composition;
- response generation;
- runtime routing;
- planning;
- orchestration;
- tool execution;
- provider calls;
- capability verification execution;
- stale-fact refresh execution;
- contradiction resolution;
- automatic winner selection beyond existing deterministic current-belief
  projection;
- fact deletion;
- graph repair;
- state patching;
- LLM reasoning about trust;
- provider-driven truth decisions;
- a second source of truth.

## Relationship to Knowledge Acquisition

Knowledge Integrity depends on Knowledge Acquisition but does not replace it.

Acquisition creates the materials integrity can inspect:
observations, evidence, facts, support links, projected relationships, entity
types, and projected State. Integrity then characterizes whether those materials
are supported, stale, ambiguous, conflicting, invalidly shaped, or verification
limited.

Important acquisition boundary:

```text
Observation/Evidence/Fact creation remains acquisition.
Integrity only interprets the projected health of those artifacts.
```

A refresh recommendation may identify a capability that could acquire new
evidence later, but the recommendation itself is not acquisition and does not
execute observation.

## Relationship to Knowledge Selection

Knowledge Integrity informs Knowledge Selection but does not perform selection.

Selection chooses projected knowledge for a current input, context, explanation,
or response. Integrity signals tell selection and explanation what caveats must
travel with selected knowledge: unsupported, stale, ambiguous, conflicted,
unverified, graph-invalid, weakly supported, or historically retained.

Important selection boundary:

```text
Context composition and response generation remain selection.
Integrity supplies limitations and trust-health metadata over projected knowledge.
```

## Relationship to State

State is the projected world model and the main place where current integrity
signals are materialized. `FactSupport`, `FactConflict`, graph issues, current
facts, and current entity types are projected State/read-model concepts.

Integrity should not become a second state store. State remains derived from the
append-only EventLedger through projection, and ProjectionStore remains only a
cache of projection snapshots.

## Relationship to Explainability

Explainability is the operator-facing disclosure path for integrity signals.
Explanation can say what Seed currently believes, why, what supports it, whether
there are competing beliefs, whether there is no current belief, and whether a
matching conflict exists.

Explainability should not become the integrity owner. It formats and exposes
integrity signals; it does not resolve them.

## Relationship to Capability Verification

Capability Verification is a specialized integrity surface for capability claims.
The inventory asks whether projected capability verification facts currently
support a capability state. It is evidence-backed and stale-aware, but it does
not execute verification.

Important distinctions:

- verification is not truth;
- provider-reported is not verified execution success;
- unverified is not unavailable;
- stale verification is not current positive verification;
- capability recommendations are not availability proof.

## Relationship to Projection

Projection is where many integrity signals are derived today:

- current support selection;
- measurement history retention;
- fact conflict projection;
- graph validation;
- relationship/type derivation;
- current entity type lookup.

Integrity should remain projection-derived unless a future document explicitly
proves a need for a separate read model. There is no evidence that Seed needs a
parallel truth system.

## Implemented, Partial, and Missing Concepts

| Concept | Status | Finding |
| --- | --- | --- |
| Current-vs-historical distinction | Partially implemented | Measurement predicates use latest-current sample semantics with bounded retained history; durable facts retain aggregate support; expired facts can be included explicitly. More canonical lifecycle vocabulary could help. |
| Fact conflict handling | Implemented | `FactConflict` is projected for alias-resolved, single-cardinality durable disagreements. It reports winners/competing facts without resolving truth. |
| Contradiction reporting | Implemented | Standalone `Contradiction` view reports conservative exclusive-predicate conflicts with evidence when available. It is read-only. |
| Graph validation | Implemented | `GraphValidationIssue` reports projected relationship/type issues without repair or truth decisions. |
| Staleness handling | Implemented, narrow | Fact expiry and stale verification reuse `expires_at`; stale is read-time filtering, not falsehood. |
| Refresh recommendations | Implemented, narrow | Stale fact refresh recommendations map stale predicates to deterministic capability names; they do not execute refresh. |
| Verification status | Implemented, narrow | Capability inventory derives `verified`, `provider_reported`, `unverified`, `stale`, and `unknown` from projected facts/support. |
| Confidence adjustment | Implemented, read-only | Confidence Aggregation may penalize contradicted facts in `FactConfidence`; it does not mutate facts/support or resolve truth. |
| Support tracking | Implemented | `FactSupport`, Evidence Graph, and explanations expose supporting fact/evidence/event relationships. |
| Projection consistency | Partially implemented | Graph validation, architecture invariants, and generated ownership docs cover some consistency concerns, but there is no single projection-integrity summary. |
| Temporal semantics | Partially implemented | Durable/measurement semantics, expiry, observed/latest timestamps, and history retention exist; terminology could be consolidated. |
| Negative belief / why-not | Missing | Existing explanation documents note no explicit `why_not()` API or negative belief model. |
| Automatic resolution | Intentionally missing | Repository evidence explicitly avoids automatic contradiction resolution, fact deletion, graph repair, verification execution, and refresh execution. |

## Required Distinctions Preserved

- **Contradiction != Resolution**: contradictions report disagreement; they do
  not choose truth.
- **Verification != Truth**: verification inventory reports scoped evidence
  status; it does not prove universal correctness.
- **Staleness != Falsehood**: stale facts are no longer fresh enough for current
  use; they may still be historically useful.
- **Refresh Recommendation != Execution**: recommendations identify possible
  capability gaps; they do not call tools or providers.
- **Confidence != Correctness**: confidence estimates support strength; it does
  not establish truth.
- **Support != Verification**: support links explain evidence behind a claim;
  verification requires an accepted verification vocabulary/status.
- **Graph Issue != Contradiction**: graph issues are topology/type validation
  reports, not fact-value disagreements.
- **Current != Most Recent Timestamp**: current selection depends on predicate
  semantics, expiry, support, cardinality, and projection rules, not timestamp
  alone.
- **Historical != Invalid**: retained history and expired facts can still explain
  past knowledge even when not current.

## Complexity Traps

Repository evidence supports avoiding:

- `MaintenanceEngine`;
- `TrustEngine`;
- `IntegrityEngine`;
- `ValidationEngine` as a broad architecture owner;
- `ReasoningEngine`;
- automatic contradiction resolution;
- automatic fact deletion;
- automatic graph repair;
- automatic verification execution;
- automatic refresh execution;
- parallel truth stores;
- provider-driven truth;
- LLM-generated trust decisions;
- runtime routing based on hidden trust scores;
- context composition that silently drops conflicts or stale facts;
- confidence values that mutate canonical fact confidence;
- capability inventory that implies provider availability.

## Recommended Smallest Next Step

The smallest safe next step is documentation-only:

1. Treat **Knowledge Integrity** as the provisional name for the read-only concern
   that answers whether Seed can safely rely on projected knowledge.
2. Add a short cross-reference from the canonical acquisition/selection document
   or architecture overview in a later documentation pass if maintainers accept
   the term.
3. Do not add a subsystem, engine, runtime route, provider path, verification
   behavior, refresh behavior, contradiction resolution behavior, or mutation
   behavior.

If future work proceeds, it should likely be a vocabulary document or summary
read model that consolidates existing integrity signals, not a new executor or
planner.

## Conclusion

The audit supports a coherent concern, but it is narrower and safer than the term
`Knowledge Maintenance` may suggest. Seed already contains many of the needed
structures as projection-derived, read-only integrity signals. The correct
architectural move is to name and bound the concern, not to introduce a new
subsystem.

Canonical summary:

```text
Knowledge Acquisition: What do we know?
Knowledge Integrity:   Can we still safely rely on what we know?
Knowledge Selection:   What matters right now?
```
