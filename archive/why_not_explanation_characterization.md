# Why-Not Explanation Characterization

## Executive Summary

Seed already has many read-only ingredients for negative belief explanation, but
it does not yet have a coherent, named "why-not" explanation surface.

The strongest current support is for **partial why-not explanations** over
projected state:

- fact belief questions can return `no_current_belief`, `ambiguous`, competing
  beliefs, and `FactConflict` details;
- unsupported facts are visible through Evidence Graph views;
- stale facts and refresh recommendations are read-only projected views;
- contradictions and graph issues include reasons, related facts, related
  relationships, evidence views, and severity;
- capability verification inventory can explain `unverified`, `stale`,
  `provider_reported`, `unknown`, and `verified` states from
  `capability_verified` facts/support/evidence.

What is missing is not a reasoning engine. The missing piece is a small,
read-only characterization/formatting layer that can assemble existing status,
reason, support, evidence, conflict, stale, graph, and capability inventory data
into negative explanation answers without changing projection or execution
behavior.

This document is documentation only. It does not change `Runtime`,
`ToolExecutor`, `EventLedger`, `ProjectionStore`, projection behavior, runtime
routing, provider behavior, tool execution, planning, orchestration, fact
mutation, projection mutation, contradiction resolution, verification execution,
refresh execution, or LLM reasoning.

## Files Inspected

Minimum requested files inspected:

- `docs/explanation_contract_vocabulary.md`
- `docs/explainability_reconciliation.md`
- `docs/explainability_contract_characterization.md`
- `docs/knowledge_maintenance_reconciliation.md`
- `docs/knowledge_acquisition_and_selection.md`
- `docs/context_composition_vocabulary.md`
- `docs/capability_verification_vocabulary.md`
- `docs/state.md`
- `docs/invariants.md`
- `seed_runtime/explanations.py`
- `seed_runtime/facts.py`
- `seed_runtime/state.py`
- `seed_runtime/state_views.py`
- `seed_runtime/contradictions.py`
- `seed_runtime/capability_inventory.py`

Relevant tests inspected:

- `tests/test_explanations.py`
- `tests/test_evidence_graph.py`
- `tests/test_contradictions.py`
- `tests/test_contradiction_characterization.py`
- `tests/test_graph_validation.py`
- `tests/test_capability_inventory.py`
- `tests/test_capability_verification_invariants.py`
- `tests/test_fact_support_aggregation.py`
- `tests/test_state_views.py`
- `tests/test_temporal_characterization.py`

Adjacent docs were also searched where useful for terminology and boundaries,
including `docs/temporal_reasoning_audit.md` and
`docs/documentation_architecture_audit.md`.

## Scope and Vocabulary

A **why-not explanation** is a read-only answer to a question such as:

- Why is this fact not a current belief?
- Why is this capability not verified?
- Why is this relationship not present?
- Why is this contradiction or graph issue present?
- Why is this fact stale, unsupported, missing, or not supported by evidence?

A why-not explanation reports existing projected status and provenance. It must
not infer new negative truth. In particular:

- **Not Believed** does not mean **False**.
- **Unsupported** does not mean **False**.
- **Unverified** does not mean **False**.
- **Stale** does not mean **False**.
- **Contradicted** does not mean **False**.
- **Missing Observation** does not mean **Negative Evidence**.
- **Missing Evidence** does not mean **Disproof**.
- **Capability Recommendation** does not mean **Capability Verification**.
- **Graph Issue** does not mean **Contradiction**.
- **Refresh Recommendation** does not mean **Refresh Execution**.

## Existing Building Blocks

### ExplanationBuilder and belief explanations

`ExplanationBuilder.why(subject, predicate)` already answers a positive belief
question and several negative-adjacent cases from projected `State` only.
It can return:

- `current` when current support exists;
- `ambiguous` when single-cardinality support exists but no unambiguous best
  support exists;
- `no_current_belief` when no current support exists;
- current beliefs with supporting fact IDs, evidence IDs, source types,
  observed time, latest observed time, and recursive fact provenance;
- competing beliefs for supported non-winning values;
- a projection-level `FactConflict` when present.

This is already a partial answer to "why does Seed not believe value X as the
current value?" when X is absent, ambiguous, expired out of current support, or
competing with a better-supported value. It is not a complete why-not surface
because it does not accept a rejected candidate value, does not classify all
absence reasons, and does not join all adjacent evidence/unsupported/stale/graph
views.

### FactSupport, FactConflict, and fact expiry

`FactSupport` is the projected support record for one
subject/predicate/value claim. It includes supporting fact IDs, source types,
confidence, first/latest observation times, expiry state, expiry timestamp,
predicate semantics, and support kind.

`FactConflict` is a projected disagreement among non-expired, alias-resolved,
single-cardinality durable fact values. It records subject, predicate,
dimensions, values, a winning value when one exists, best fact ID, conflicting
fact IDs, and a reason.

Fact expiry is represented by `Fact.expires_at` and read through
`is_fact_expired()`. Default current-support and conflict views exclude expired
facts unless an include-expired path is requested. Stale facts are still stored;
staleness does not delete facts or lower stored confidence.

### Stale fact refresh recommendations

`State.get_stale_facts()` exposes expired projected facts as a read-only view.
`State.get_stale_fact_refresh_recommendations()` maps stale fact predicates to a
recommended capability with a deterministic reason. This is a partial why-not
answer for "why is this fact not current?" and "what could refresh it?" but it
is explicitly not refresh execution, provider calling, tool invocation, or tool
need creation.

### Evidence Graph and unsupported facts

Evidence Graph views provide evidence nodes, evidence links, fact evidence
views, evidence summaries, and unsupported fact views. Unsupported facts are
facts without supporting evidence links in the evidence graph view. That can
explain why a fact is unsupported, but it cannot prove the fact is false.

### Contradictions

`build_contradictions()` is a standalone read-only detector over projected
`State` facts and optional Evidence Graph. It conservatively reports exact
same-subject/same-predicate conflicts for exclusive predicates. A contradiction
contains fact IDs, conflicting values, severity, reason, evidence by fact ID,
and supporting event IDs.

Contradictions explain why incompatible claims are reported, not which one is
true. They do not resolve, rewrite, suppress, or select facts.

### Graph issues and relationships

`State` projects catalog relationships and graph validation issues.
`GraphValidationIssue` records severity, subject, relationship, object,
relationship IDs, source fact IDs, reason, hint, expected/actual subject types,
and expected/actual object types. State views expose graph issues as read-only
issue summaries with supporting IDs.

This is a strong answer to "why does a graph issue exist?" It is only a weak
answer to "why is a relationship absent?" because Seed can query present
relationships, but absence usually means no projected relationship edge matched
the query. That absence is not disproof unless explicit negative evidence is
modeled elsewhere.

### Capability verification inventory

`build_capability_inventory()` is already a read-only capability verification
inventory derived from projected `State` only. Its universe is registered tool
capabilities, open/recorded tool needs, and subjects of `capability_verified`
facts. It derives state from `capability_verified` supports:

- active positive support can yield `verified`;
- provider-reported values can yield `provider_reported`;
- explicit unverified values can yield `unverified`;
- expired verification support can yield `stale`;
- unknown values can yield `unknown`;
- missing verification facts produce `unverified` with the reason
  `no capability_verified fact is present in projected State`.

Capability inventory can therefore partially explain why a capability is not
verified and why a recommendation exists but is not verified. It cannot execute
checks, inspect providers, prove absence, or turn recommendation metadata into
verification.

### Context composition and knowledge selection

Context composition vocabulary already separates selected context, excluded
context, support summaries, conflict summaries, capability context, graph
context, and explanation context. This makes why-not explanation architecturally
adjacent to Knowledge Selection: many why-not answers are about why something is
not selected as current context, not about acquiring more data.

## Characterization Matrix

| Question / category | Current status | Existing contributors | What Seed can say today | Missing or partial piece |
| --- | --- | --- | --- | --- |
| Fact not believed | Partially implemented | `ExplanationBuilder.why()`, `State.get_fact_support()`, `FactSupport`, `FactConflict`, expiry filtering | No current belief, ambiguous current support, current competing values, supporting facts/evidence for current and competing beliefs | No dedicated `why_not(subject, predicate, value)` query; no normalized reason taxonomy for absent vs expired vs unsupported vs not selected |
| Capability not verified | Partially implemented | `build_capability_inventory()`, `CapabilityInventoryEntry`, `CapabilitySupportSummary`, `capability_verified` facts | Unverified because no `capability_verified` fact is present; stale because verification fact expired; provider-reported/unknown/unverified value mapping | No execution/verification result model beyond projected facts; no proof of provider absence; no distinction between missing inventory universe entry and unverified known capability unless caller supplies universe |
| Relationship absent | Missing / weakly partially implemented | `State.get_relationships()`, `find_subjects()`, `find_objects()`, relationship catalog, source facts | Present relationships can be queried; graph issues can explain invalid present edges | No absent-relationship explanation object; absence may mean no source fact, unsupported source fact, catalog mapping mismatch, alias mismatch, type issue, or simply no observation |
| Contradiction present | Implemented for conservative contradiction view; partial across all conflict concepts | `FactConflict`, `Contradiction`, Evidence Graph | Conflicting subject/predicate/value groups, fact IDs, evidence by fact, severity, reason, supporting events | No unified surface across `FactConflict`, standalone `Contradiction`, and graph issues; no automatic resolution by design |
| Graph issue present | Implemented | `GraphValidationIssue`, `GraphValidator`, `build_issue_view()` | Which relationship is suspicious/invalid, source fact IDs, relationship IDs, expected vs actual types, severity, reason, hint | Not unified with explanation contract; not a contradiction and should not be collapsed into one |
| Fact stale | Implemented as read-only stale view; partial as explanation | `Fact.expires_at`, `is_fact_expired()`, `FactSupport.expired`, `State.get_stale_facts()`, stale refresh recommendations | Fact expired at or before comparison time; current support excludes it by default; deterministic refresh capability recommendation | No unified stale explanation object with comparison time, current-vs-expired support, and evidence summary |
| Unsupported fact | Implemented in Evidence Graph; partial in general explanation | Evidence Graph, fact evidence views, unsupported fact views, evidence summaries | Fact has no supporting evidence in the evidence graph view | Not integrated into `ExplanationBuilder.why()`; unsupported does not prove false |
| Competing facts / fact conflicts | Implemented for projected fact support | `FactSupport`, `FactConflict`, explanation competing beliefs | Which values compete, winning value/best fact when one exists, conflicting fact IDs, reason | Selection rationale is not fully normalized; no separate object for why a non-winning value lost |
| Capability unresolved / recommendation not verified | Partially implemented | `ToolNeed`, `CapabilityCatalog`, registered tool capabilities, provider recommendations, capability inventory | Requested/known/candidate/provider-recommended capabilities are not verification; inventory can say no verification fact exists | No unified explanation that joins recommendation metadata to inventory status; no verification execution |
| Observation missing | Missing / partially representable | `State.observations`, state views, evidence graph, fact/evidence absence | A caller can see there is no matching observation/evidence/fact in projected state | No first-class missing-observation explanation; absence is not negative evidence |
| Evidence missing | Partially implemented | unsupported fact views, `build_fact_evidence_view()` returning no match, evidence graph summaries | A fact can be reported unsupported; no matching evidence view can be found | No normalized missing-evidence reason taxonomy; missing evidence is not disproof |
| Missing facts | Partially implemented | `ExplanationBuilder.why()` status `no_current_belief`, state fact lookups, CLI why-fact missing output | No current belief or no matching fact found | Does not distinguish never observed, expired, unsupported, filtered by dimensions, alias mismatch, catalog mismatch, or pruned measurement sample |
| Refresh recommendation | Implemented as read-only recommendation | `StaleFactRefreshRecommendation`, predicate-to-capability mapping | Which capability could refresh stale fact and why | Does not execute refresh; not joined into a general why-not answer |

## Direct Answers to Audit Questions

### Can Seed explain why a fact is not believed?

**Partially.** Seed can explain `no_current_belief`, ambiguity, current belief
support, competing beliefs, conflicts, and stale filtering. It cannot yet answer
one canonical candidate-value query such as "why does Seed not believe
`service.runtime = docker`?" across all possible causes.

### Can Seed explain why a capability is not verified?

**Partially.** Capability inventory can say the capability is unverified because
no `capability_verified` fact is present, stale because the verification fact is
expired, provider-reported rather than verified, explicitly unverified, or
unknown. It cannot execute verification or prove absence outside projected
State.

### Can Seed explain why a relationship is not present?

**Mostly missing.** Seed can list present relationships and explain graph issues
for present invalid/suspicious relationships. It does not have a dedicated
absent-relationship explanation. Absence may indicate no observation, no fact,
unsupported fact, no catalog mapping, alias mismatch, dimensions mismatch, or no
relationship semantics for the predicate.

### Can Seed explain why a contradiction exists?

**Implemented for current conservative surfaces, partially unified.**
`FactConflict` and `Contradiction` both include reason and relevant facts.
`Contradiction` can attach evidence views and supporting event IDs. The missing
piece is unification, not detection or resolution.

### Can Seed explain why a fact is stale?

**Implemented as a stale view, partially as an explanation.** Staleness follows
`expires_at` and `is_fact_expired()`, and refresh recommendations include a
reason. A cohesive explanation object with comparison time and support/evidence
summary is missing.

### Can Seed explain why a fact is unsupported?

**Partially to implemented.** Evidence Graph unsupported fact views identify
facts without evidence support. The explanation is read-only and evidence-backed,
but it is not yet integrated into the general belief explanation surface.

### Can Seed explain why a graph issue exists?

**Implemented.** Graph issues carry severity, reason, hint, expected and actual
entity types, relationship IDs, and source fact IDs. State issue views summarize
these as read-only issue records.

### Can Seed explain why a capability recommendation exists but is not verified?

**Partially.** Capability vocabulary and invariants clearly state that requested,
known, candidate, registered-operation, and provider-recommended capabilities do
not imply verification. Capability inventory can separately report verification
state. What is missing is a read-only join view that presents recommendation
metadata and verification inventory state together.

## Architectural Fit

A coherent read-only why-not explanation surface is feasible if it remains an
adapter over existing structures:

```text
Projected State / Evidence Graph / Inventories / Catalogs
        -> read-only characterization and formatting
        -> why-not answer
```

The surface should reuse:

- `ExplanationBuilder.why()` for current, ambiguous, and no-current-belief fact
  status;
- `FactSupport` and `FactConflict` for support and competing values;
- Evidence Graph for evidence and unsupported facts;
- stale fact views and stale refresh recommendations for expiry and refresh
  suggestions;
- `Contradiction` for conservative contradiction explanations;
- `GraphValidationIssue` for graph issue explanations;
- `CapabilityInventoryEntry` for capability verification status;
- capability catalog/recommendation metadata only as non-verifying context;
- context composition vocabulary for selected/excluded/support/conflict/context
  framing.

It should not own facts, evidence, projection, verification, contradiction
resolution, capability execution, provider calls, refresh execution, or context
selection.

## Knowledge Integrity Relationship

Why-not explanation is closely related to Knowledge Integrity. Many why-not
answers are integrity statements about whether projected knowledge is safe to
rely on:

- unsupported facts indicate missing evidence support;
- stale facts indicate expired currentness;
- contradictions and fact conflicts indicate incompatible current claims;
- graph issues indicate suspicious or invalid projected relationships;
- capability verification inventory distinguishes verified, unverified,
  provider-reported, stale, and unknown capability states;
- missing evidence, missing observations, and missing relationships expose limits
  of projected knowledge.

However, why-not explanation should not become a Knowledge Integrity engine. It
should report integrity signals already produced by projection, Evidence Graph,
contradiction views, capability inventory, and stale views.

## Knowledge Selection Relationship

Why-not explanation is also a Knowledge Selection concern. It often answers why
something is not selected as current belief or current context:

- a value may be a competing belief but not the current belief;
- a fact may be expired and therefore filtered from default current support;
- a measurement sample may be retained as bounded history but not selected as
  the latest current sample;
- a capability recommendation may be selected for possible action while
  verification remains unselected/unproven;
- a graph issue may be included in context as an integrity warning rather than a
  contradiction.

This reinforces that the next step should improve explanation of existing
selection/projection outcomes, not add acquisition or execution behavior.

## Complexity Traps to Avoid

Repository evidence supports avoiding all of the following:

- `WhyNotEngine`
- `NegativeBeliefEngine`
- `TrustEngine`
- `IntegrityEngine`
- `ReasoningEngine`
- automatic contradiction resolution
- automatic verification execution
- automatic refresh execution
- provider calls from explanations
- tool execution from explanations
- LLM-generated negative beliefs
- a parallel truth system
- a second contradiction classifier hidden inside explanations
- a second capability verification owner hidden inside recommendations
- treating absence as disproof
- treating recommendations as verified capabilities
- treating stale data as false data

The safe boundary is a read-only projection-backed adapter/formatter, not a new
subsystem with ownership over truth, state, verification, or execution.

## Recommended Smallest Next Step

Create a small documentation-first **why-not answer vocabulary** or
characterization table that maps existing statuses to existing sources, without
adding runtime behavior. The smallest useful follow-up would be:

1. Define a read-only reason vocabulary such as:
   - `no_current_belief`
   - `ambiguous_current_belief`
   - `competing_value_not_selected`
   - `expired_fact_filtered`
   - `unsupported_fact`
   - `missing_fact`
   - `missing_observation`
   - `missing_evidence`
   - `contradiction_present`
   - `graph_issue_present`
   - `capability_unverified`
   - `capability_verification_stale`
   - `recommendation_not_verification`
2. For each reason, identify the existing source object and required IDs.
3. Keep this as documentation or a future formatter contract only.
4. Do not implement a new engine, resolver, verifier, executor, provider
   integration, planner, refresh path, or mutation path.

If code is later considered, the smallest behavior-preserving implementation
would be a read-only adapter that delegates to existing builders/views and
returns structured summaries. That implementation should be a separate future
decision, not part of this audit.

## Final Characterization

Seed can already explain many negative-adjacent states, but the capability is
fragmented across fact explanations, support records, evidence views,
contradictions, graph issues, stale views, state views, and capability
inventory. The correct characterization is:

- **Implemented:** contradiction reasons, graph issue reasons, stale fact
  detection, stale refresh recommendations, unsupported fact views, current fact
  explanation, competing beliefs, fact conflicts, capability inventory status.
- **Partially implemented:** fact-not-believed explanations, capability-not-
  verified explanations, unsupported/missing evidence explanations,
  recommendation-but-not-verified explanations, stale explanation formatting,
  selection rationale for non-winning competing facts.
- **Missing:** coherent why-not explanation vocabulary/surface,
  absent-relationship explanation, missing-observation explanation, normalized
  reason taxonomy, and a read-only join surface that combines recommendation
  metadata with verification inventory state.

The feasible architecture is a small read-only, projection-backed,
evidence-backed, inventory-backed explanation surface that reuses existing
structures and preserves all current ownership boundaries.
