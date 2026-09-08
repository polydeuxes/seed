---
doc_type: audit
status: active
domain: understanding visibility
introduced_by: understanding visibility existing surface audit
depends_on:
  - operator_surface_activation_against_knowledge_and_understanding_audit.md
  - operator_surface_family_observation.md
  - operator_understanding_surface_observation.md
  - knowledge_and_understanding_distinction_observation.md
  - understanding_claim_and_decompression_observation.md
  - current_work_position_frontier.md
  - active_edge_frontier.md
  - continuity_frontier.md
related:
  - state_summary_authority_reconciliation.md
  - contradiction_discovery_and_visibility_reconciliation.md
  - response_characterization.md
  - claim_support_frontier.md
  - impact_overview_authority_reconciliation.md
  - source_navigation_surface_reconciliation.md
  - capability_verification_reconciliation.md
  - execution_status_and_operator_feedback_reconciliation.md
---

# Understanding Visibility Existing Surface Audit

## Purpose

This audit asks where repository-supported answers already exist for the operator question:

```text
What does Seed currently understand?
```

The audit does not create an implementation proposal, a UI proposal, a new canonical surface family, a workflow, governance, schema, runtime behavior, or immediate remediation.

## Method

This investigation treated the requested document list as seed references rather than a closed scope. It reviewed navigation surfaces, repository maps, understanding and learning observations, operator-surface observations, continuation frontiers, response/explanation documents, state-summary documents, impact/read-model documents, source-navigation documents, execution-status documents, capability/verification documents, promotion-readiness documents, and support/evidence documents.

Broad search terms used across repository documentation included:

```text
understanding
visibility
current understanding
current work
active edge
continuity
explanation
support
selection
orientation
operator surface
state summary
impact
fact support
activation
decompression
learning
preservation
```

Routing surfaces inspected included:

- `docs/README.md`
- `docs/index.md`
- `docs/architectural_knowledge_map.md`
- `docs/architectural_status_and_next_frontier.md`

## Existing-Coverage Finding

Existing repository work already preserves the visibility side well enough that a new full `understanding_visibility_inventory_audit.md` would mostly duplicate prior work.

The most direct answer already lives in three documents:

1. `operator_surface_activation_against_knowledge_and_understanding_audit.md` preserves the boundary that existing knowledge/understanding work covers formation, preservation, change, learning, and decompression, while operator-surface work adds the visibility question: where understanding is visible, which surfaces communicate understanding, and which surfaces communicate inventory.
2. `operator_surface_family_observation.md` inventories operator-facing and operator-adjacent surfaces and classifies Current Work Position, Active Edge, Continuity/Handoff Alignment, contradiction visibility, execution status, source navigation, fact support, State Summary, impact, verification inspection, promotion readiness, and other surfaces across inventory, understanding, explanation, and mixed concerns.
3. `operator_understanding_surface_observation.md` directly asks whether current operator-facing surfaces primarily communicate inventory, understanding, explanation, or a mixture, and identifies the strongest understanding, inventory, explanation, and mixed surfaces.

Therefore, this audit should be read as a short existing-surface audit and duplicate-work check, not as a new observation frontier.

## Boundary Preserved

The prior activation audit already preserves the key boundary:

```text
understanding formation
    !=
understanding visibility
```

The repository evidence supports leaving understanding formation with the knowledge/understanding, decompression, learning, support-change, and preservation documents. Understanding visibility belongs to the operator-surface cluster because it asks how already-formed or preserved understanding becomes visible to an operator.

This audit does not reopen understanding ontology.

## Surface Inventory

The repository-supported candidate understanding-visibility surfaces are distributed rather than centralized.

| Surface | Visibility role | Audit classification |
| --- | --- | --- |
| Current Work Position | Preserves orientation for safe continuation: current question, boundaries, pressure, constraints, unresolved risks, and next-safe movement. | Strong understanding surface. |
| Active Edge | Identifies the live unresolved pressure pulling work forward among many possible preserved concerns. | Strong understanding surface with selection/explanation pressure. |
| Continuity / Handoff Alignment | Shows what relevant understanding, pressure, constraints, and work-position survive change or handoff. | Understanding and continuation surface. |
| Contradiction Visibility | Makes conflict visible as unresolved attention pressure, not merely as a count of conflicts. | Mixed understanding and explanation surface. |
| Impact Overview / Drilldowns | Communicates what matters about an entity while bounded by projection authority. | Mixed understanding and inventory surface. |
| Fact Support / Claim Support | Exposes why a claim or current fact has support, support limits, source scope, and provenance. | Explanation/support visibility surface; understanding emerges when paired with relevance and caveats. |
| State Summary | Communicates projected-state shape, counts, top entities, integrity/status signals, and knowledge inventory. | Mixed surface with inventory core; often mistaken for understanding. |
| Source Navigation | Helps move from a question to source-backed answers, ownership boundaries, and evidence locations. | Mixed navigation, evidence, understanding, and explanation surface. |
| Verification Inspection / Capability Status | Shows supported, stale, failed, absent, or disputed verification/capability state. | Mixed inventory and explanation surface. |
| Promotion Readiness / Promotion Backlog | Shows candidates, readiness pressure, and review status while preserving promotion boundaries. | Mixed inventory, attention, and boundary-inspection surface. |
| Execution Status / Operator Feedback | Communicates what work is currently occurring and what status should be visible to the operator. | Status and understanding-adjacent surface. |
| Response / CLI Presentation | Communicates selected projected knowledge, explanation outputs, integrity signals, limitations, and summaries. | Distributed communication layer, not an understanding authority. |

## Major Findings

### Strongest Understanding-Visibility Surfaces

The strongest existing understanding-visibility surfaces are:

- Current Work Position, because it preserves orientation rather than merely listing artifacts.
- Active Edge, because it asks which unresolved pressure is currently live rather than counting all frontiers, gaps, or tensions.
- Continuity and handoff-alignment work, because it tests whether relevant understanding, pressure, constraints, and safe continuation survive change.
- Contradiction visibility, when it exposes conflict as unresolved meaning or attention pressure rather than only as an integrity count.

Current Work Position and Active Edge already serve as understanding surfaces in the repository evidence, but they remain exploratory frontiers rather than reconciled ontology or implementation-ready runtime surfaces.

### Strongest Inventory Surfaces Mistaken For Understanding

State Summary is the strongest inventory-heavy surface at risk of being mistaken for an understanding surface. The state-summary authority work treats it as closest to a repository-level knowledge inventory and overview surface, while operator-surface work observes that its operator-facing position can make inventory rows look like relevance, priority, or understanding.

Other inventory-heavy surfaces that can be mistaken for understanding include capability inventories, source/repository inventories, evidence graph listings, observation source accounting, and raw fact/current-fact lists. They answer presence, count, availability, and projected-state-shape questions better than meaning, relevance, or current understanding questions.

### Strongest Explanation Surfaces Adjacent To Understanding Visibility

Explanation is adjacent to understanding visibility but not identical to it.

The strongest explanation-adjacent surfaces are fact support, claim support, why/why-fact output, evidence graph explanations, contradiction explanation, confidence reasons, selection rationale, capability verification rationale, and response caveats. These surfaces explain why a claim, row, selection, conflict, stale status, or verification state is visible or believed.

Repository evidence suggests explanation is often the bridge that makes inventory operator-interpretable. A count is inventory; a count plus support, selection rationale, source scope, conflict, freshness, and caveat can become useful to understanding. That does not make explanation the whole of understanding visibility, because Current Work Position and Active Edge preserve orientation and live pressure, not only why-provenance.

### Strongest Mixed Surfaces

The strongest mixed surfaces are:

- State Summary: inventory core plus integrity, status, knowledge, and limited understanding signals.
- Source Navigation: implementation navigation plus source-backed operator answerability and explanation pressure.
- Impact Overview / entity drilldowns: meaning-oriented overview plus inventory/details.
- Contradiction Visibility: integrity count, conflict explanation, and unresolved attention pressure.
- Capability Verification / Status: inventory of capability states plus support, stale, failure, and verification explanation.
- Promotion Readiness: candidate inventory plus readiness and boundary inspection.

## Duplicate-Work Findings

This audit overlaps prior work and should avoid taking ownership from it.

| Prior work | Already owns | This audit adds | This audit should avoid |
| --- | --- | --- | --- |
| `operator_surface_activation_against_knowledge_and_understanding_audit.md` | The formation-vs-visibility boundary and the finding that operator-surface work activates existing understanding concerns. | Confirms the follow-up question is already mostly answered by existing surface documents. | Reopening understanding ontology or creating a new frontier. |
| `operator_surface_family_observation.md` | Broad operator-surface inventory and classification across inventory, understanding, explanation, mixed, overloaded, operator-oriented, and implementation-oriented concerns. | Narrows that inventory to the operator question “What does Seed currently understand?” | Defining new canonical families or redesigning interfaces. |
| `operator_understanding_surface_observation.md` | Direct findings about inventory, understanding, explanation, State Summary, Current Work Position, Active Edge, and source navigation. | Records that this is adequate existing coverage rather than a missing-audit gap. | Duplicating its full surface analysis. |
| `state_summary_authority_reconciliation.md` | State Summary authority, inventory/knowledge/overview boundary, and unresolved state-summary questions. | Identifies State Summary as the main overuse risk for understanding visibility. | Redesigning State Summary. |
| `response_characterization.md` | Distributed response surfaces and communication/presentation boundaries over projected knowledge. | Notes response surfaces communicate understanding-adjacent material but do not own understanding visibility. | Proposing a Response engine or new response contract. |

## Understanding Visibility Findings

- Understanding visibility is preserved in the repository, but it is distributed across operator-surface observations, continuation frontiers, response/explanation surfaces, and read-model documents.
- It is not centralized in a single canonical “current understanding” surface.
- Current Work Position and Active Edge are the strongest existing answers for “what does Seed currently understand?” when the question means current orientation, live pressure, boundaries, and safe continuation.
- Fact support, explanation, contradiction, source navigation, impact, verification, execution status, and promotion-readiness surfaces support narrower “what does Seed understand about this claim/entity/state/work?” questions.
- State Summary helps answer “what is projected or counted now?” but only partially answers “what is understood now?”

## Inventory Versus Understanding Findings

Inventory surfaces expose presence, count, availability, current projection shape, and lists. They are valid when the operator question is inventory-shaped.

Understanding surfaces expose interpreted significance, orientation, active pressure, relevance, unresolved meaning, safe continuation, boundary conditions, and what changed or survived.

The repository evidence repeatedly warns against treating inventory visibility as understanding visibility merely because the output is operator-visible. State Summary is the central example: it exposes useful current projection information, but its default visibility can overstate relevance or understanding unless paired with support, scope, caveats, or explanation.

## Explanation Versus Understanding Findings

Understanding visibility is not identical to explanation surface.

Explanation surfaces answer why-oriented questions: why a claim is visible, why a fact is believed, why support is weak, why a contradiction exists, why a selection occurred, or why verification is stale/absent.

Understanding-visibility surfaces can use explanation, but the strongest orientation surfaces also answer where the work is, what pressure is live, what boundaries constrain movement, and what remains unresolved. Explanation is therefore a major route by which understanding becomes visible, but it is not the only route and should not absorb Current Work Position, Active Edge, Continuity, or operator-surface-family findings.

## Unresolved Observations

- No single repository surface centrally answers “What does Seed currently understand?” across facts, work position, active edge, continuity, integrity, source navigation, impact, support, verification, and response.
- The distributed answer may be acceptable, but the repository does not yet show whether operators need one route to the distributed surfaces.
- Current Work Position may already cover much of Active Edge; existing frontiers explicitly preserve that possible redundancy.
- State Summary remains the strongest overuse risk because it is operator-visible, useful, and inventory-heavy.
- Explanation surfaces are necessary for making inventory interpretable, but explanation should not become a substitute for orientation or live-pressure preservation.
- Source Navigation is relevant because it can move an operator from a question to source-backed answers, but it is not purely an operator-understanding surface.
- Promotion readiness, verification inspection, execution status, and impact surfaces are understanding-adjacent; their authority boundaries remain owned by their existing documents.

## Conclusion

Repository evidence already adequately preserves the understanding-visibility distinction for audit purposes. The answer is distributed, not centralized:

- use `operator_surface_activation_against_knowledge_and_understanding_audit.md` for the formation-versus-visibility boundary;
- use `operator_surface_family_observation.md` for the broad inventory of existing operator surfaces;
- use `operator_understanding_surface_observation.md` for the direct inventory/understanding/explanation/mixed findings;
- use Current Work Position, Active Edge, and Continuity frontiers for orientation and live-pressure questions;
- use State Summary, fact support, source navigation, response, impact, verification, execution status, and promotion-readiness documents for narrower projected-state, support, communication, and status questions.

No new full inventory audit is needed now. This document exists only to preserve that duplicate-work finding and route future readers to the existing surfaces without proposing runtime, UI, workflow, governance, schema, or ontology changes.
