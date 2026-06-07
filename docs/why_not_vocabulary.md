# Why-Not Vocabulary v1

## Purpose

Why-Not Vocabulary v1 names the negative-adjacent states Seed can already report
from existing read models. Its purpose is vocabulary, classification, and
architectural boundary-setting.

This document is **documentation only**. It does not add a why-not explanation
surface, engine, planner, verifier, resolver, executor, provider integration,
projection behavior, fact mutation, contradiction resolution, refresh execution,
or LLM reasoning.

The core finding preserved from Why-Not Explanation Characterization is:

> Why-not explanations already largely exist in fragmented read-only form. Seed
> lacks a common vocabulary more than it lacks implementation.

## Audit Sources

This document is based on an audit of the existing characterization documents,
vocabularies, state documentation, invariants, and relevant read models.

Minimum requested documents inspected:

- `docs/why_not_explanation_characterization.md`
- `docs/explanation_contract_vocabulary.md`
- `docs/explainability_reconciliation.md`
- `docs/knowledge_maintenance_reconciliation.md`
- `docs/knowledge_lifecycle_reconciliation.md`
- `docs/capability_verification_vocabulary.md`
- `docs/context_composition_vocabulary.md`
- `docs/state.md`
- `docs/invariants.md`

Relevant structures inspected:

- `seed_runtime/explanations.py`
- `seed_runtime/facts.py`
- `seed_runtime/state.py`
- `seed_runtime/state_views.py`
- `seed_runtime/evidence_graph.py`
- `seed_runtime/contradictions.py`
- `seed_runtime/capability_inventory.py`

## Scope

A **why-not term** is a canonical name for a negative-adjacent status that may
answer questions such as:

- Why is there no current belief?
- Why is this claim unsupported?
- Why is this capability not verified?
- Why is this fact stale?
- Why is this value not selected as current?
- Why is this issue reported as a graph issue rather than a contradiction?
- Why is a refresh recommended but not executed?

Why-not vocabulary is not a negative truth system. It reports existing projected,
evidence, inventory, graph, contradiction, and explanation statuses without
asserting new facts.

## Canonical Vocabulary Terms

### Unknown

**Definition:** Seed does not have enough applicable projected classification to
assign a more specific status in the relevant surface.

**Supported by repository evidence:** Capability verification inventory includes
an `unknown` state for non-standard `capability_verified` values, and Evidence
Graph uses `unknown` for unclassified evidence node/source information.

**Status:** Partially implemented.

**Boundary:** Unknown is not false. It is not failed verification, disproof, or
negative evidence.

### Not Believed

**Definition:** Projected state does not currently expose the queried claim as a
current belief.

**Supported by repository evidence:** `Explanation.status` includes
`no_current_belief`, and `ExplanationBuilder.why(subject, predicate)` returns it
when no current supports exist for the queried subject and predicate.

**Status:** Partially implemented.

**Boundary:** Not Believed is not False. It may result from absence, expiry,
unsupported evidence, ambiguity, non-selection, or lack of observation; it does
not prove the opposite claim.

### Unsupported

**Definition:** A projected fact exists but has no supporting evidence attached
in the Evidence Graph view.

**Supported by repository evidence:** Evidence Graph exposes unsupported fact
views and summary counts derived from projected `State` facts that lack evidence
relationships.

**Status:** Implemented as a read-only evidence graph/status view.

**Boundary:** Unsupported is not False. It is a support/provenance condition, not
a truth value.

### Unverified

**Definition:** A capability is not currently verified by scoped projected
verification support.

**Supported by repository evidence:** Capability verification vocabulary and
invariants state that requested, known, candidate, and provider-recommended
capabilities default to unverified unless a scoped verification model proves
otherwise. Capability inventory reports `unverified` when no
`capability_verified` fact is present or when supported values map to the
unverified set.

**Status:** Partially implemented as inventory-backed read-only classification;
capability verification execution is not implemented.

**Boundary:** Unverified is not False, not unavailable, and not failed
verification. Failed verification requires accepted negative evidence, not mere
absence of positive evidence.

### Stale

**Definition:** A projected fact or capability-verification support has expired
or is no longer current according to existing expiry/freshness metadata.

**Supported by repository evidence:** `State.get_stale_facts()` returns expired
projected facts; stale fact refresh recommendations are read-only capability
recommendations; capability inventory reports `stale` when expired
`capability_verified` support exists.

**Status:** Implemented for stale facts and partially implemented for capability
verification inventory.

**Boundary:** Stale is not False. Staleness does not delete facts, lower stored
confidence, execute refreshes, or prove the opposite claim.

### Conflicted

**Definition:** Existing projected support contains competing values or a
projection-level disagreement that affects current belief selection.

**Supported by repository evidence:** `FactConflict` records disagreements among
non-expired, alias-resolved, single-cardinality durable fact values, including
values, a possible winning value, best fact ID, conflicting fact IDs, and a
reason. `ExplanationBuilder` can attach matching `FactConflict` data and expose
competing beliefs.

**Status:** Implemented as projected fact support/conflict metadata.

**Boundary:** Conflicted is not identical to Contradicted. Conflicted is a
current-support/projection-selection condition; Contradicted is a standalone
conservative read-only contradiction view over exact subject/predicate groups.

### Contradicted

**Definition:** A standalone contradiction view reports incompatible values for
an exact subject/predicate group under conservative exclusive-predicate rules.

**Supported by repository evidence:** `build_contradictions()` reports read-only
`Contradiction` records with subject, predicate, fact IDs, values, severity,
reason, optional evidence by fact ID, supporting event IDs, last event, and
projection version.

**Status:** Implemented as read-only contradiction detection.

**Boundary:** Contradicted is not False and is not resolved by the vocabulary.
Contradiction detection does not choose winners, rewrite facts, append events,
call providers, execute tools, mutate hosts, or call LLMs.

### Ambiguous

**Definition:** Seed has support for a queried fact claim family, but no
unambiguous best current support is selected.

**Supported by repository evidence:** `Explanation.status` includes `ambiguous`
when single-cardinality support exists but `State.get_fact_support()` returns no
single best support.

**Status:** Implemented in `ExplanationBuilder` for fact explanations.

**Boundary:** Ambiguous is not False, not Unsupported, and not Unknown. It means
there is support, but current selection is not decisive for that query.

### Missing Observation

**Definition:** The relevant observation input needed to support a claim is not
present in projected observation/state views.

**Supported by repository evidence:** Observation views and observation-source
design distinguish observation from execution, availability, verification, and
mutation. Why-not characterization identifies missing observation as an
important negative-adjacent distinction, but no single first-class
`missing_observation` status object currently exists.

**Status:** Vocabulary only / partially represented by absence in read-only
observation views.

**Boundary:** Missing Observation is not Negative Evidence. It means Seed lacks a
recorded observation in the relevant projected scope; it does not mean the
observed thing is absent in the world.

### Missing Evidence

**Definition:** A claim or fact lacks attached supporting evidence in the
relevant evidence/provenance view.

**Supported by repository evidence:** Unsupported fact views report projected
facts without evidence. Explanation contract vocabulary treats supporting
evidence as a common field across explanation surfaces.

**Status:** Implemented as Unsupported for facts; broader missing-evidence usage
is vocabulary only unless a surface exposes evidence absence explicitly.

**Boundary:** Missing Evidence is not Disproof. It is a provenance gap, not proof
of falsehood.

### Missing Relationship

**Definition:** A relationship needed for a graph or explanation claim is not
present in current projected relationship views.

**Supported by repository evidence:** State documentation describes graph
relationships, relationship validation, and graph validation issues. However,
there is no general first-class `missing_relationship` why-not status.

**Status:** Vocabulary only / partially represented by relationship absence and
graph issue surfaces.

**Boundary:** Missing Relationship is not a contradiction and not negative
evidence. It must not cause relationship mutation or graph repair.

### Recommendation Present

**Definition:** Seed can report a deterministic recommendation, usually a
capability recommendation, for what might refresh, inspect, or address a stale or
missing-support condition.

**Supported by repository evidence:** Stale fact refresh recommendations map
expired facts to capability recommendations with deterministic reasons;
capability recommendation vocabulary distinguishes recommendations from
verification.

**Status:** Implemented for stale fact refresh recommendations; broader use is
surface-specific.

**Boundary:** Recommendation Present is not Verification, not Execution, and not
Authorization. A recommendation must not be treated as proof that the capability
works or that refresh has occurred.

### Verification Pending

**Definition:** A verification-relevant capability exists in requested, known,
candidate, or recommended form, but no current scoped verification support proves
it verified.

**Supported by repository evidence:** Capability verification vocabulary states
that requested, known, candidate, and provider-recommended capabilities are not
synonyms for verified capability and remain unverified by default.

**Status:** Vocabulary only / represented by `unverified` inventory and
capability-verification boundary documents.

**Boundary:** Verification Pending is not Verification, not Failure, and not a
request for execution.

### Historical

**Definition:** A record remains available as retained history, legacy
compatibility, debug history, or a non-current artifact rather than current
truth.

**Supported by repository evidence:** State and invariants distinguish retained
measurement history from current truth arbitration, and historical/quarantine
invariants mark planning artifacts as historical or legacy compatibility only.

**Status:** Partially implemented / documentation-backed depending on the
surface.

**Boundary:** Historical is not Current and must not become active orchestration,
scheduling, retry, selection, or execution behavior.

### Current

**Definition:** A claim or support record is selected by existing projected-state
semantics as current for its surface.

**Supported by repository evidence:** `Explanation.status` includes `current`,
State exposes current facts/supports/views, measurement predicates expose
current samples, and state views report current projected summaries.

**Status:** Implemented across projected state, explanations, and current-state
views.

**Boundary:** Current is still projection-backed belief/status, not absolute
truth. It must not bypass evidence, projection, or support ownership.

## Important Distinctions

- **Not Believed != False.** No current belief means the projected read model did
  not select the claim as current.
- **Unsupported != False.** Unsupported means missing attached evidence for a
  projected fact.
- **Unverified != False.** Unverified means no current scoped verification proves
  the capability.
- **Stale != False.** Stale means expired or no longer current by freshness
  metadata.
- **Contradicted != False.** Contradiction reports incompatible projected claims;
  it is not resolution.
- **Conflicted != Contradicted.** Conflicted is projection/support-selection
  disagreement; Contradicted is standalone contradiction detection.
- **Missing Observation != Negative Evidence.** Absence of an observation record
  does not prove absence in the world.
- **Missing Evidence != Disproof.** Lack of evidence is a provenance gap.
- **Unknown != False.** Unknown is lack of applicable classification.
- **Recommendation != Verification.** Recommendation metadata is not proof.
- **Graph Issue != Contradiction.** Graph issues report relationship/type model
  issues, not necessarily incompatible fact values.
- **Refresh Recommendation != Refresh Execution.** Recommendations do not append
  refresh events, invoke providers, or execute tools.

## Relationship to Other Architecture Concepts

### Knowledge Acquisition

Knowledge Acquisition produces observations, evidence, facts, and source
metadata. Why-not vocabulary reads the resulting projected and evidence-backed
surfaces. It must not call providers, perform observation, execute tools, or
create new facts.

### Knowledge Integrity

Knowledge Integrity exposes conflicts, contradictions, unsupported facts, stale
facts, graph issues, confidence signals, and refresh recommendations. Why-not
vocabulary names these statuses without becoming an IntegrityEngine,
ContradictionResolver, TrustEngine, or confidence authority.

### Knowledge Selection

Knowledge Selection determines current support, current facts, ambiguity,
competing beliefs, and current samples through existing projection semantics.
Why-not vocabulary can describe why a value is not current only when existing
support, conflict, ambiguity, stale, or evidence data exposes that condition. It
must not select differently or create a parallel truth system.

### Explainability

Explainability already has explanation-producing structures. Why-not vocabulary
is a specialization of explanation vocabulary for negative-adjacent statuses,
using the same read-only, projection-backed, evidence-backed, and
inventory-backed boundaries.

### Capability Verification

Capability Verification vocabulary defines verification boundaries. Why-not
vocabulary reuses `verified`, `provider_reported`, `unverified`, `stale`, and
`unknown` only as inventory/read-model classifications. It must not execute
verification or infer availability from recommendation, catalog presence, or
operation names.

### State

State owns projected facts, supports, conflicts, relationships, graph issues,
stale fact views, and current-state views. Why-not vocabulary describes State
outputs. It must not append events, mutate facts, mutate supports, repair graph
issues, or alter projection semantics.

### Projection

Projection remains the source of current read-model status. Why-not vocabulary is
projection-backed, not a projection owner. It must not change `EventLedger`,
`ProjectionStore`, cache invalidation, event ordering, or projection replay.

## Implemented Status Findings

These negative-adjacent states already have concrete read-only implementation:

- `current` fact/support/current-state statuses.
- `no_current_belief` and `ambiguous` fact explanation statuses.
- competing beliefs and attached `FactConflict` in fact explanations.
- unsupported facts in Evidence Graph views and summaries.
- stale facts and stale fact refresh recommendations.
- standalone contradictions with severity, reason, fact IDs, values, evidence,
  supporting event IDs, projection version, and last event.
- graph validation issues with deterministic issue metadata.
- capability inventory states including `verified`, `provider_reported`,
  `unverified`, `stale`, and `unknown`.

## Partial Status Findings

These states are partially implemented because data exists but is not unified
under one why-not vocabulary or contract:

- Not Believed beyond `ExplanationBuilder.why(subject, predicate)`.
- Conflicted across `FactConflict`, competing beliefs, and standalone
  contradiction surfaces.
- Stale rationale as a single explanation shape joining fact, expiry, evidence,
  source, and recommendation.
- Capability why-not rationale beyond inventory state and support/evidence
  metadata.
- Selection rationale explaining why one supported value became current and
  another did not.
- Missing Evidence outside fact-level unsupported evidence graph views.
- Historical/non-current rationale across measurement history, expired facts, and
  legacy artifacts.

## Missing or Vocabulary-Only Findings

These concepts should be treated as vocabulary-only unless a specific existing
surface exposes them:

- `missing_observation` as a first-class status.
- `missing_relationship` as a first-class status.
- `verification_pending` as a first-class status separate from `unverified`.
- a general `why_not()` API or why-not explanation surface.
- a unified negative explanation contract spanning facts, capabilities,
  contradictions, graph issues, stale facts, and unsupported facts.
- a general replacement rationale for why an older fact/sample was no longer
  selected.

These missing items do not imply implementation recommendations in this
document.

## Architectural Boundaries

Why-not vocabulary must remain:

- read-only;
- projection-backed;
- evidence-backed;
- inventory-backed;
- provenance-preserving;
- status/reporting vocabulary;
- documentation-first.

Why-not vocabulary must not become:

- `ReasoningEngine`;
- `WhyNotEngine`;
- `TrustEngine`;
- `IntegrityEngine`;
- `VerificationEngine`;
- `ContradictionResolver`;
- `RefreshExecutor`;
- `CapabilityExecutor`;
- `ProviderCaller`;
- planner;
- workflow engine;
- agent loop;
- parallel truth system;
- LLM-generated negative belief system.

It must not change Runtime, ToolExecutor, EventLedger ownership,
ProjectionStore ownership, projection behavior, fact mutation, projection
mutation, contradiction resolution, verification execution, refresh execution,
provider integration, planning, orchestration, or tool execution.

## Complexity Traps

Avoid these traps when using this vocabulary:

1. **Turning absence into disproof.** Missing evidence, missing observation,
   unknown, unverified, and no-current-belief are not false claims.
2. **Collapsing support and truth.** Unsupported or weakly supported claims may
   still be projected facts; support status is not a truth value.
3. **Merging conflicts and contradictions.** `FactConflict` and standalone
   `Contradiction` serve different read-only roles.
4. **Treating recommendations as execution.** Refresh or capability
   recommendations do not call providers or run tools.
5. **Treating vocabulary as an engine.** Naming statuses must not introduce
   reasoning, verification, planning, or trust orchestration.
6. **Creating a parallel negative belief system.** Why-not vocabulary reports
   existing state; it does not invent negative beliefs.
7. **Overgeneralizing graph issues.** A relationship/type issue is not
   automatically a fact contradiction.
8. **Using LLMs as negative authorities.** Why-not classifications must come from
   projected, evidence, inventory, or graph data, not generated speculation.

## Future Work Notes

Future work should remain documentation-only in this vocabulary document:

- keep this vocabulary aligned with explanation contract vocabulary;
- keep capability verification terms aligned with capability verification
  vocabulary and invariants;
- keep conflict/contradiction distinctions aligned with state documentation;
- document any newly observed status term before treating it as canonical;
- preserve the finding that the repository's primary gap is common vocabulary,
  not a new implementation surface.

This document intentionally does not recommend implementation work.
