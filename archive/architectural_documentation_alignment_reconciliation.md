# Architectural Documentation Alignment Reconciliation

## Purpose

This document performs a documentation-only reconciliation of Seed's authoritative documentation after the recent architectural reconciliation chain.

It is a documentation authority and alignment audit.

It does not modify code, schemas, runtime behavior, tests, projections, evidence handling, fact promotion, relationship promotion, operator interfaces, recommendations, decisions, temporal behavior, explanation behavior, or causality behavior.

It does not introduce new architecture.

Its role is to check whether authoritative and navigational documentation accurately reflects architecture already reconciled elsewhere.

## Central Finding

The authoritative documentation is broadly aligned with the reconciled architecture, but several orientation and map documents still carried older fact-centric wording or duplicated authority in ways that could obscure the newer claim-centric framing.

The safe alignment rule is:

```text
Seed is claim-centric.
Facts and relationships are normalized claim forms.
Projections communicate selected knowledge; they do not create authority.
Operators are intent-centric.
Questions bridge operator intent to Seed's claim-oriented knowledge.
Assessments, recommendations, and decisions remain distinct.
Events preserve occurrences and history; projections present selected state.
Explanation and causality remain distinct.
```

The reconciliation outcome is documentation simplification and routing, not new architecture.

## Files Reviewed

Authoritative and navigational documents reviewed:

- `README.md`
- `docs/seed.md`
- `docs/README.md`
- `docs/architectural_knowledge_map.md`
- `docs/architectural_status_and_next_frontier.md`
- `docs/architecture.md`
- `docs/knowledge_representation_map.md`

Recent reconciliation documents used as the governing record:

- `docs/claim_strength_and_assertion_semantics_reconciliation.md`
- `docs/corroboration_and_fact_promotion_reconciliation.md`
- `docs/fact_confidence_and_corroboration_reconciliation.md`
- `docs/relationship_promotion_reconciliation.md`
- `docs/operator_intent_question_and_claim_interface_reconciliation.md`
- `docs/operator_interface_and_projection_authority_reconciliation.md`
- `docs/goal_policy_and_operator_authority_reconciliation.md`
- `docs/assessment_recommendation_and_decision_reconciliation.md`
- `docs/goal_relevance_and_recommendation_generation_reconciliation.md`
- `docs/event_and_change_reconciliation.md`
- `docs/observation_refresh_and_knowledge_freshness_reconciliation.md`
- `docs/causality_and_explanation_reconciliation.md`
- `docs/explainability_reconciliation.md`
- `docs/documentation_authority_and_seed_thesis_reconciliation.md`
- `docs/documentation_authority_reconciliation.md`
- `docs/documentation_boundary_enforcement_reconciliation.md`

## 1. Claim-Centric Documentation Alignment

### Finding

Seed's reconciled architecture is claim-centric, not fact-centric, entity-centric, action-centric, or LLM-centric.

The governing reconciliations establish that:

```text
Observations report.
Evidence preserves provenance.
Facts normalize claims.
Relationships normalize edges / connection claims.
Projections select interpretations.
Verification confirms a scoped question.
History preserves what was knowable at a time.
```

Authoritative documentation already rejects truth-centric interpretation by saying Seed does not begin with truth and does not store truth. However, some older orientation wording used a linear `Observation -> Evidence -> Fact -> Relationship -> Projection` frame without naming claims as the centered proposition. That wording was directionally correct for the historical implementation path, but it could be misread as making facts the central authority rather than normalized claim forms.

### Alignment Applied

The concise authoritative surfaces should now express the model as:

```text
Observation -> Evidence -> Claim -> Relationship -> Projection
```

with an explicit note that facts are normalized claims.

This keeps the implementation term `Fact` visible without making the architecture fact-centric.

### Authority Boundary

This audit does not redefine facts, relationships, or projections. It only routes older orientation language through the already reconciled claim semantics.

## 2. Operator Boundary Alignment

### Finding

The operator boundary is accurately reconciled by the recent operator interface documents:

```text
Operators arrive with intent.
Questions express, refine, and operationalize intent.
Claims preserve knowledge.
Projections communicate selected knowledge.
Assessments interpret knowledge.
Recommendations relate interpreted knowledge to possible operator purposes.
```

The authoritative documentation already preserves the key boundary: the operator can provide intent, authority, approval, ownership, correction, policy, missing context, and boundary decisions, but operator statements are not automatically correct about runtime state.

### Residual Risk

The risk is not an explicit contradiction. The risk is discoverability: the older foundational documentation chain emphasized identity, trust, corroboration, and relationship promotion, but did not route readers to the operator-intent/question/claim bridge as part of alignment-sensitive architecture work.

### Recommended Reference Pattern

Navigation documents should reference `operator_intent_question_and_claim_interface_reconciliation.md` from alignment-sensitive sections rather than restating the full operator model.

## 3. Projection Authority Alignment

### Finding

Projection authority is mostly described correctly:

- projections select and communicate preserved knowledge;
- current state is a projection;
- projections are not the only preserved interpretation;
- state views and evidence views are read-only representations;
- recommendations over projected knowledge do not imply execution, verification, mutation, planning, or workflow orchestration.

### Residual Risk

The phrase `current projected world model` can be safe when paired with projection caveats, but it should not be allowed to imply that projection is truth, authority, or complete reality.

Likewise, language such as `source of truth` is unsafe if it appears to describe truth about the world. It is acceptable only when scoped to the internal event record. Prefer:

```text
authoritative historical event record
```

instead of:

```text
historical source of truth
```

### Alignment Applied

Documentation should describe `EventLedger` as Seed's authoritative historical event record rather than as a truth oracle.

## 4. Temporal Reasoning Alignment

### Finding

Temporal reasoning is consistently separated across the reviewed documents:

- events preserve occurrences in append order;
- event timestamps and ledger order are distinct;
- projections present selected current state;
- historical event retention belongs to the event ledger;
- projection snapshots are not the authoritative historical record;
- freshness and staleness characterize projected knowledge without automatically triggering refresh, execution, or mutation.

### Residual Risk

The main documentation risk is collapsing event history, state, current projection, and freshness into one concept of `now`.

### Recommended Reference Pattern

Navigation and status documents should route temporal questions to:

- `docs/event_and_change_reconciliation.md`
- `docs/observation_refresh_and_knowledge_freshness_reconciliation.md`
- `docs/temporal_reasoning_audit.md`

rather than restating temporal semantics in README or status documents.

## 5. Explanation And Causality Alignment

### Finding

The reconciliation chain preserves the required separation:

```text
Explanation describes why Seed presents or selected something.
Causality claims that something produced or influenced something else.
Consequence describes downstream effects or implications.
Recommendation relevance relates knowledge to possible operator goals.
```

Explanation can cite evidence, support, conflicts, freshness, selection rationale, caveats, and recommendation relevance. That does not make every explanation causal.

### Residual Risk

Orientation documents should avoid implying that explainability, recommendation generation, or impact views prove causality. Where causality is needed, documents should route to `causality_and_explanation_reconciliation.md` instead of embedding a second causality standard.

## 6. Document Boundary Findings

### README.md

Role: repository orientation.

Status: aligned after claim-centric wording is kept concise and routed to `docs/seed.md` and `docs/README.md`.

Boundary to preserve:

- should not become a reconciliation;
- should not own current frontier details beyond linking to status;
- should not duplicate the full architecture thesis.

### docs/seed.md

Role: concise architectural thesis / constitutional statement.

Status: aligned when it names claims as the center and keeps facts visible as normalized claim forms.

Boundary to preserve:

- should not become a document index;
- should not absorb scoped reconciliation arguments;
- should not become implementation notes.

### docs/README.md

Role: documentation navigation authority.

Status: aligned if it routes readers to owner documents and avoids restating full arguments.

Boundary to preserve:

- should not become status;
- should not become architecture itself;
- should not duplicate every reconciliation finding.

### docs/architectural_knowledge_map.md

Role: concern map and routing.

Status: aligned. It routes concern ownership and points currentness/frontier questions to status rather than owning them directly.

Boundary to preserve:

- should route to owning documents;
- should not own current status;
- should not become canonical architecture.

### docs/knowledge_representation_map.md

Role: representation-layer map.

Status: aligned after older representation wording was corrected because it separated `Fact` and `Claim` too strongly. Facts should be described as normalized claims, while support relationships can still connect supporting facts to higher-order claims.

Boundary to preserve:

- should describe representation shape;
- should not supersede claim semantics reconciliation;
- should not become status or implementation notes.

### docs/architectural_status_and_next_frontier.md

Role: current status and active frontier.

Status: aligned.

Boundary to preserve:

- status should not become architecture;
- status should not preserve full reconciliation rationale;
- status should not create new frontiers without a concrete unanswered operator question.

### docs/architecture.md

Role: canonical architecture overview.

Status: broadly aligned, with one terminology correction recommended and applied: avoid using `source of truth` for event history unless scoped to the internal event record.

Boundary to preserve:

- architecture overview should summarize and route;
- implementation-specific detail should remain subordinate to scoped design and reconciliation documents.

## 7. Duplicate Authority Findings

### Repeated Architectural Statements

The following statements appear, appropriately, in multiple places but should remain concise outside their owning documents:

- Seed preserves observations and evidence-backed claims.
- Seed does not store truth.
- Projections select or communicate knowledge.
- Capability handling is downstream of projected knowledge and does not imply execution.
- Documentation boundaries should reduce duplication.

These repetitions are acceptable in README, `docs/seed.md`, and maps when they are short orientation statements.

### Duplicated Definitions

Definitions most at risk of duplication:

- claim;
- fact;
- relationship;
- projection;
- authority;
- recommendation;
- decision;
- event;
- freshness;
- explanation;
- causality.

Preferred pattern:

```text
README / docs/seed.md: compact invariant.
docs/README.md / architectural_knowledge_map.md: route to owner.
Scoped reconciliation: full boundary reasoning.
Vocabulary document: term details where applicable.
Status document: current classification only.
```

### Duplicated Frontier Descriptions

Current active frontier belongs in `architectural_status_and_next_frontier.md`. README and maps should only point to it. This boundary is currently respected.

### Duplicated Status Reporting

Status reporting should not be copied into `docs/README.md`, `docs/seed.md`, or the knowledge map. The reviewed documents mostly respect this.

## Required Finding Checklist

| Required finding | Alignment result |
| --- | --- |
| Seed is claim-centric. | Aligned after orientation and map wording treats facts as normalized claims rather than non-claim facts. |
| Operators are intent-centric. | Aligned; route through `operator_intent_question_and_claim_interface_reconciliation.md`. |
| Questions bridge intent and claims. | Aligned; should be discoverable from navigation docs. |
| Events preserve occurrences. | Aligned; avoid truth-oracle wording for event history. |
| Projections communicate knowledge. | Aligned; projections select/communicate and do not add authority. |
| Assessments interpret knowledge. | Aligned; keep distinct from projections and decisions. |
| Recommendations relate knowledge to goals. | Aligned; recommendations remain advisory and non-executing. |
| Decisions remain distinct from recommendations. | Aligned; continue routing to assessment/recommendation/decision reconciliation. |
| Explanation and causality remain distinct concepts. | Aligned; continue routing to causality and explanation reconciliation. |

## Recommended Documentation Updates

1. Keep README claim-centric and concise; do not expand it into reconciliation detail.
2. Keep `docs/seed.md` constitutional and compact; use `Claim` in the core shape while preserving `Fact` as a normalized claim form.
3. Add this audit to `docs/README.md` as an alignment-sensitive routing document.
4. Update `docs/knowledge_representation_map.md` so its representation layer no longer says facts are not claims.
5. Prefer `authoritative historical event record` over `source of truth` in architectural overview language.
6. Route operator-intent, assessment/recommendation/decision, temporal, and explanation/causality questions to their scoped reconciliations instead of duplicating their reasoning in orientation documents.

## Conclusion

The authoritative documentation can accurately reflect the reconciled architecture without creating new architecture by applying three documentation rules:

```text
Center claims.
Route details to owner documents.
Avoid duplicate authority.
```

This preserves Seed's documentation boundaries while making the current architecture easier to discover and harder to misread as fact-centric, entity-centric, action-centric, LLM-centric, projection-authoritative, or recommendation-as-decision architecture.
