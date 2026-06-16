---
doc_type: observation
status: exploratory
domain: pressure visibility and preservation
defines:
  - pressure visibility observation
  - pressure preservation observation
  - knowledge without pressure risk
  - pressure without stable terminology pattern
related:
  - surviving_pressure_after_decomposition_observation.md
  - lens_as_observation_and_compression_pattern.md
  - current_work_position_frontier.md
  - active_edge_frontier.md
  - continuity_frontier.md
  - preservation_surface_observation.md
  - preservation_failure_observation.md
  - discovery_path_preservation_observation.md
  - documentation_lineage_observation.md
  - lineage_distinction_observation.md
  - inquiry_frontier.md
  - working_state_activation_observation.md
  - working_state_activation_failure_observation.md
  - understanding_visibility_existing_surface_audit.md
  - understanding_navigation_observation.md
  - operator_surface_family_observation.md
  - operator_understanding_surface_observation.md
---

# Pressure Visibility And Preservation Observation

## Purpose

This observation investigates how repository pressures become visible, where they
are preserved today, and whether repository work can preserve knowledge while
losing the pressure that made the knowledge matter.

It is an observation only. It is not a reconciliation, frontier, pressure
ontology, representation proposal, runtime proposal, implementation proposal,
workflow redesign, governance proposal, Seed identity statement, Seed goal
statement, agency claim, survival policy, or decision-system design.

The investigation is about visibility and preservation. It does not validate,
rank, schedule, or implement pressures.

## Central Questions

```text
How do repository pressures become visible?
```

```text
Where are pressures preserved today?
```

```text
Can repository work preserve knowledge while losing the pressure that made it
important?
```

```text
Can pressure survive when facts, terminology, explanations, and support
structures change?
```

This document does not assume yes or no answers. It records where repository
evidence is strong, weak, duplicated, or unresolved.

## Method And Authority Boundary

Repository content was reviewed directly. Prompt-listed documents were treated as
starting points only. Review also used documentation maps, cross-references,
adjacent observations, audits, reconciliations, frontiers, runtime-facing read
models, implementation-facing architecture documents, tests by filename and
surface, and recent observation chains.

Search terms used included: `pressure`, `concern`, `active concern`, `current
concern`, `active edge`, `current work`, `continuity`, `preservation`,
`visibility`, `importance`, `relevance`, `selection`, `what matters`,
`unresolved`, `contradiction`, `frontier`, `question`, `lineage`, `survival`,
`activation`, `understanding`, `currentness`, `terminology`, `lost`,
`disappeared`, `support`, `impact`, `source navigation`, and `handoff`.

The strongest inspected evidence included:

- `README.md`
- `docs/README.md`
- `01-architecture.md`
- `02-domain-model.md`
- `13-knowledge-and-evidence.md`
- `docs/architectural_status_and_next_frontier.md`
- `docs/architectural_knowledge_map.md`
- `docs/architectural_findings_preservation.md`
- `docs/surviving_pressure_after_decomposition_observation.md`
- `docs/lens_as_observation_and_compression_pattern.md`
- `docs/learning_as_lens_observation.md`
- `docs/support_change_and_learning_observation.md`
- `docs/understanding_claim_and_decompression_observation.md`
- `docs/knowledge_and_understanding_distinction_observation.md`
- `docs/current_work_position_frontier.md`
- `docs/active_edge_frontier.md`
- `docs/continuity_frontier.md`
- `docs/persistence_frontier.md`
- `docs/inquiry_frontier.md`
- `docs/selection_and_attention_frontier.md`
- `docs/selection_convergence_observation.md`
- `docs/attention_target_frontier.md`
- `docs/attention_trigger_frontier.md`
- `docs/preservation_surface_observation.md`
- `docs/preservation_failure_observation.md`
- `docs/discovery_path_preservation_observation.md`
- `docs/non_selected_remainder_preservation_observation.md`
- `docs/documentation_lineage_observation.md`
- `docs/lineage_distinction_observation.md`
- `docs/documentation_compression_observation.md`
- `docs/working_state_activation_observation.md`
- `docs/working_state_activation_artifact_audit.md`
- `docs/working_state_activation_failure_observation.md`
- `docs/handoff_and_continuation_lineage_frontier.md`
- `docs/handoff_pressure_transition_observation.md`
- `docs/handoff_consumption_activation_reconciliation.md`
- `docs/continuation_context_and_working_state_reconciliation.md`
- `docs/handoff_bootstrap_and_summary_reconciliation.md`
- `docs/handoff_template_and_continuation_protocol_reconciliation.md`
- `docs/understanding_visibility_existing_surface_audit.md`
- `docs/understanding_navigation_observation.md`
- `docs/operator_surface_family_observation.md`
- `docs/operator_understanding_surface_observation.md`
- `docs/operator_surface_activation_against_knowledge_and_understanding_audit.md`
- `docs/operator_pain_as_frontier_signal.md`
- `docs/source_navigation_surface_reconciliation.md`
- `docs/source_navigation_without_grep_audit.md`
- `docs/source_observation_queryability_audit.md`
- `docs/source_navigation_query_surface_design_audit.md`
- `docs/claim_support_characterization.md`
- `docs/entity_impact_drilldown_reconciliation.md`
- `docs/impact_overview_authority_reconciliation.md`
- `docs/state_summary_authority_reconciliation.md`
- `docs/state_summary_performance_inquiry_lineage_report.md`
- `docs/state_summary_endpoint_prominence_audit.md`
- `docs/future_state_consequence_pressure_selection_observation.md`
- `docs/derived_consequence_and_relevance_observation.md`
- `docs/reference_point_and_concern_subject_observation.md`
- `docs/object_role_operation_pressure_test.md`
- `docs/git_history_observation_source_reconciliation.md`
- `docs/observation_refresh_and_knowledge_freshness_reconciliation.md`
- `seed_runtime/state_summary_views.py`
- `seed_runtime/state_views.py`
- `seed_runtime/source_navigation.py`
- `tests/test_state_summary_views.py`
- `tests/test_source_navigation.py`
- `tests/test_fact_support_aggregation.py`

## High-Level Finding

Repository pressures become visible when preserved material stops being enough to
continue, select, explain, navigate, or safely resume work. The strongest pattern
is not simply:

```text
knowledge survives
```

but:

```text
knowledge survives or changes
    -> a participant still needs to know why it matters now
    -> pressure becomes visible as current concern, active edge, frontier,
       unresolved tension, support gap, handoff risk, or navigation failure
```

The repository already preserves many pressures, but it preserves them unevenly.
Frontiers, current-work-position documents, active-edge documents, handoff
surfaces, inquiry lineage, preservation-failure work, discovery-path documents,
and operator-facing surfaces carry pressure more strongly than fact inventories
or ordinary summaries. Fact, support, source-navigation, impact, and state-summary
surfaces can make pressure visible, but they often require an additional current
selection, operator question, or continuation frame to show why a fact matters.

The strongest observed risk is:

```text
facts, documents, conclusions, or support survive
    while currentness, concern, discovery path, selection rationale, or active
    edge disappears
```

The strongest observed counter-pattern is:

```text
vocabulary changes
    while the same unresolved pressure remains visible through new support
    structures, frontiers, or handoff constraints
```

## How Pressures Become Visible

Across the reviewed material, pressure usually becomes visible through one of the
following routes.

### 1. Continuation failure exposes pressure

Handoff, working-state, current-work-position, and continuity documents repeatedly
show that a participant can have preserved information and still be unable to
continue. The pressure becomes visible when the later participant cannot tell
what is active, why it is active, which constraints still apply, what remains
unresolved, or what move is safe next.

This is the strongest evidence that pressure is not identical to knowledge. The
knowledge may be present; the current work position may be absent.

### 2. Selection exposes pressure

Selection, attention, relevance, current concern, and active-edge documents make
pressure visible by asking why one possible path is current rather than merely
available. A preserved concern can remain dormant. A selected concern becomes a
pressure-bearing surface when it shapes what matters now.

This route distinguishes inventory from currentness. An inventory can list many
things. It does not by itself show which one is pulling work forward.

### 3. Contradiction and support gaps expose pressure

Contradiction, claim-support, fact-support, and source-navigation work make
pressure visible when facts are insufficient, unsupported, stale, conflicting, or
hard to route from an operator question. The pressure is not the fact itself. It
is the need to qualify, explain, support, refresh, navigate, or avoid overclaiming
from that fact.

Support therefore participates in pressure visibility, but support is not the
same as pressure. Support can show why a claim is grounded while still failing to
show why the claim matters now.

### 4. Discovery paths expose pressure

Discovery-path and documentation-lineage documents make pressure visible by
preserving how a result was reached, what critique was applied, what assumptions
failed, and what question remained. Without that path, a conclusion can survive
as a statement while losing the pressure that made it significant.

This route is especially important for recent lens work: learning, orientation,
preservation, activation, understanding, relevance, and selection often weakened
as total explanations while leaving the motivating pressure visible.

### 5. Operator surfaces expose pressure

Operator-understanding, operator-surface, impact, state-summary, and source
navigation work make pressure visible when an operator asks what matters, what
changed, how Seed knows, what is unsupported, where to inspect source, or what is
important about an entity.

These surfaces are pressure-visible when they organize knowledge around a current
operator question or consequence. They are weaker as pressure-preservation
surfaces when they only expose generic inventory.

## Pressure Visibility Inventory

| Candidate surface | What pressure becomes visible? | What remains hidden? | What survives? | What is lost or at risk? |
| --- | --- | --- | --- | --- |
| Current Work Position | What position current work occupies; what is active; why continuation feels possible or impossible. | Whether position should become ontology; whether all work positions share one structure. | Active context, selected constraints, unresolved tensions, validation state, next safe moves. | Facts may remain without the active concern that made them current. |
| Active Edge | What is currently pulling work forward among questions, gaps, contradictions, frontiers, and tensions. | Whether active edge is object, role, operation, attention state, or merely vocabulary. | Current pull, selected tension, forward movement, next continuation point. | Preserved concerns can become inactive, and active pull can be mistaken for priority or truth. |
| Continuity | Recognizable survival through change, handoff, revision, and participation shifts. | Whether survival belongs to information, work position, inquiry, or pressure. | Recognizable thread of work across change. | Terminology continuity can be mistaken for continuity of concern. |
| Inquiry Frontier | Unresolved pursuit of understanding; questions and tensions as active or preserved work. | Which inquiries are current rather than merely preserved. | Open questions, unresolved gaps, movement through findings. | Question lists can preserve topics without preserving why they matter now. |
| Frontiers | Boundaries of unresolved work and candidate distinctions. | Whether a frontier is active implementation priority, ontology exploration, or historical record. | Unresolved pressure, safe non-resolution, next investigation boundary. | Frontier proliferation can duplicate or bury active pressure. |
| Preservation Surface | What must remain available for later understanding, continuation, or audit. | Which preserved item is still current. | Artifacts, findings, non-selected remainder, boundaries. | Preservation can protect knowledge while losing active significance. |
| Preservation Failure | Cases where survival of artifact, information, or conclusion does not produce usable continuity. | Whether the failure is in preservation, activation, navigation, or selection. | Failure modes as warning surfaces. | Repeated failures can remain descriptive without carrying current pressure. |
| Discovery Path | Why a conclusion was reached, weakened, redirected, or decomposed. | Whether the conclusion remains current or authoritative. | Critique sequence, reasoning path, hidden assumptions, pressure applied. | Conclusions survive without the path that made them meaningful. |
| Documentation Lineage | How documents relate, succeed, constrain, or revise one another. | Whether lineage is artifact lineage, inquiry lineage, authority lineage, or pressure lineage. | Artifact relationships and historical development. | Artifact lineage can preserve order while losing active concern. |
| Working-State Activation | Whether preserved material enters current usable working state. | Why one preserved item should activate rather than another. | Activation conditions, current subset, continuation-relevant material. | Available knowledge may never become active pressure. |
| Activation Failure | Why artifacts, summaries, or references fail to become usable continuation context. | Whether the failure is caused by missing pressure, missing route, or missing support. | Failure patterns and risk boundaries. | Knowledge can remain available but inert. |
| Understanding Visibility | Whether existing surfaces show what Seed understands or only what it stores. | Whether understanding is validated, current, or pressure-bearing. | Understanding-relevant routes and gaps. | Understanding claims can survive without concern or consequence. |
| Understanding Navigation | How participants move from a question to relevant understanding. | Whether navigation proves significance. | Routes among knowledge, support, and explanation. | Navigable knowledge may still lack current pressure. |
| Operator Surface Family | How operator-facing views communicate what can be asked or inspected. | Whether operator pain is temporary, structural, or current priority. | Questions, feedback, needs, missing explanations. | Surfaces can answer facts while failing to show what matters. |
| Operator Understanding Surface | What matters to the operator, why facts matter, and how surfaces shape comprehension. | Whether operator relevance equals repository pressure. | Importance cues, consequence views, explanation needs. | What matters may be implied rather than preserved. |
| State Summary | Counts, issues, top entities, contradiction/support/current fact cues. | Why a row matters now; whether summary prominence equals pressure. | Compressed state awareness and issue visibility. | Summary can preserve inventory but lose currentness or discovery path. |
| Impact Surfaces | Consequences and what matters about an entity or domain. | Whether impact is general relevance, operator relevance, or active concern. | Significance cues and drilldown routes. | Impact can become a view-level label without preserving the originating concern. |
| Fact Support / Claim Support | Why claims are supported, partially supported, unsupported, or in tension. | Why a supported claim matters now. | Evidence-to-fact-to-claim grounding and support boundaries. | Support can survive without significance. |
| Source Navigation | Route from implementation question to source artifact, relationship, and support. | Whether source relationship is currently important. | Navigability over preserved source facts. | Source facts can survive while operator need or investigation pressure disappears. |
| Handoff Surfaces | Active investigation, working state, unresolved tensions, navigation intent, and next safe moves. | Whether handoff content was consumed or remains current later. | Continuation alignment and selected active edge. | Handoff can preserve references without preserving pressure. |

## Knowledge Versus Pressure Findings

### Knowledge survived while pressure disappeared

The strongest examples are preservation and handoff failures. Documents,
references, facts, and summaries can remain available while later participants
cannot tell what is active, why it matters, or what to do next. Source observation
and source navigation work provide a second example: imports, definitions,
entrypoints, and support can be preserved while the operator's question still
cannot be answered without brittle query knowledge or navigation intent.

State-summary and impact surfaces provide a weaker but recurring example. They
can preserve counts, issues, top entities, or consequence labels while still not
preserving the discovery path or current concern that made those items prominent.

### Pressure survived while knowledge changed

Recent lens work provides the strongest example. Learning, orientation,
preservation, selection, activation, relevance, survival, continuity, and
understanding each gathered scattered phenomena, then became less adequate as
single explanations. The knowledge changed as decomposition exposed narrower
support structures, but the motivating pressures often survived: how to continue,
how to select, how to preserve what matters, how to explain support, and how to
make understanding visible.

### Pressure survived while terminology changed

The clearest pattern is:

```text
lens changes
    -> vocabulary changes
    -> support structures emerge
    -> pressure often survives
```

Examples include learning becoming support change, understanding change,
selection, contradiction discovery, and continuation risk; preservation becoming
artifact preservation, rationale preservation, lineage preservation,
discovery-path preservation, and activation risk; and continuity splitting away
from mere persistence or terminology continuity.

The pressure did not always survive equally. Some candidate terms became weak or
duplicative. But the repeated survival of concern across vocabulary changes is
stronger than the survival of any single term.

### Pressure survived while support structures changed

Support structures often changed from broad prose to frontiers, audits,
reconciliations, documentation maps, state summaries, source navigation, fact
support, claim support, or handoff templates. In these cases, pressure moved from
one surface to another rather than remaining in the original explanation.

This is visible when a broad concept exposes a problem, a later audit decomposes
it, and a more precise surface preserves part of the concern. The pressure may
become easier to navigate, but it can also become fragmented across documents.

## Current Work Position And Active Edge Findings

Current Work Position appears to be a mixed surface. It is not merely a knowledge
surface because its central question is not only what is known. It is not merely
a pressure surface because it also carries information about constraints,
validation state, boundaries, and next safe moves. Its strongest pressure-visible
function is preserving the selected position from which work can continue.

Active Edge appears more pressure-forward than Current Work Position. It asks
what is currently pulling work forward. It is strongest when distinguishing an
active unresolved concern from an inactive preserved concern. It is weakest when
it risks duplicating priority, selection, attention, inquiry, or current work
position.

Together, these documents show that:

```text
current concern != fact inventory
active edge != entity inventory
current work position != repository status alone
```

But the repository has not settled whether these distinctions should become
stable ontology, remain exploratory vocabulary, or be routed through existing
continuation, inquiry, selection, and handoff surfaces.

## Preservation Findings

Preservation, lineage, inquiry, continuity, discovery-path, handoff, and
activation work already function as pressure-preservation mechanisms in a weak
and distributed sense.

They preserve pressure by keeping visible:

- what question remained unresolved;
- what tension or contradiction triggered later work;
- what selection made a subset current;
- what rationale made a conclusion usable;
- what discovery path made a finding intelligible;
- what handoff context made continuation safe;
- what activation failure made preserved information inert;
- what non-selected remainder should not be mistaken for rejection.

They do not preserve pressure automatically. A preservation surface can preserve
artifacts without current concern. A lineage surface can preserve artifact order
without inquiry movement. An inquiry document can preserve questions without
activation. A handoff can preserve references without consumption. A support view
can preserve grounding without significance.

## Visibility Failure Findings

The recurring visibility failures are:

```text
facts survived
    but concern disappeared
```

This appears when fact inventories, source facts, support relationships, or
state summaries remain available without showing why the fact matters now.

```text
documents survived
    but pressure disappeared
```

This appears in preservation and lineage work where artifacts remain available
but their active edge, critique path, or current relevance is no longer obvious.

```text
conclusions survived
    but discovery path disappeared
```

This appears in discovery-path preservation work and in lens decompositions where
the final conclusion can be retained without the sequence of failed assumptions
that made it meaningful.

```text
support survived
    but currentness disappeared
```

This appears in freshness/currentness work, source-navigation work, state-summary
surfaces, and claim/fact-support boundaries. Support can be historically valid
while no longer sufficient for a current operational question.

## Critical Distinctions Under Review

The reviewed evidence mostly supports, but does not fully settle, these
distinctions:

```text
pressure != fact
```

Facts can ground claims and projections. Pressure concerns why something matters,
continues to pull, remains unresolved, or must be preserved for safe continuation.

```text
pressure != knowledge
```

Knowledge can be preserved, projected, navigated, and supported while the
pressure that made it important disappears.

```text
pressure != ontology
```

Pressure may expose ontology questions, but observing pressure does not justify a
new type system.

```text
pressure visibility != pressure representation
```

A surface can make pressure visible without defining a runtime representation for
pressure.

```text
pressure preservation != pressure validation
```

Preserving a pressure means keeping the concern inspectable. It does not prove
that the concern is correct, current, or implementation-ready.

```text
current concern != fact inventory
active edge != entity inventory
continuity != terminology continuity
```

The repository repeatedly warns that lists of facts, entities, or words do not
by themselves preserve what matters, what pulls work forward, or what survived
recognizably through change.

## Duplicate-Work Check

### Prior documents already own

- `surviving_pressure_after_decomposition_observation.md` owns the observation
  that pressures often remain visible after candidate lenses are decomposed.
- `lens_as_observation_and_compression_pattern.md` owns the broader lens pattern:
  broad language can expose scattered evidence before decompression.
- `current_work_position_frontier.md` owns exploratory ontology questions around
  work-position continuity and selected continuation-relevant orientation.
- `active_edge_frontier.md` owns exploratory ontology questions around what pulls
  work forward.
- `continuity_frontier.md` owns continuity as recognizable survival through
  change and not mere storage or identity.
- `preservation_surface_observation.md` and
  `preservation_failure_observation.md` own preservation surfaces and failure
  modes.
- `discovery_path_preservation_observation.md` owns discovery-path preservation.
- `documentation_lineage_observation.md` and
  `lineage_distinction_observation.md` own lineage distinctions and survival
  surfaces.
- `inquiry_frontier.md` owns inquiry as unresolved pursuit.
- Working-state activation documents own activation and activation failure.
- Understanding and operator-surface documents own understanding visibility,
  navigation, and operator-facing comprehension.
- Source navigation, state summary, impact, and support documents own their
  bounded read-model or operator-surface responsibilities.

### This observation adds

This document adds a cross-surface visibility inventory of where pressure appears
and where it is lost. It does not define pressure. It asks whether pressure is
visible or preserved across already-existing surfaces, especially when knowledge,
facts, terminology, and support structures change.

Its added contribution is the distinction between:

```text
preserving knowledge
```

and:

```text
preserving the pressure that made the knowledge important
```

### This observation should avoid duplicating

This document should avoid:

- redefining Current Work Position or Active Edge;
- redoing the surviving-pressure-after-decomposition inventory;
- redesigning preservation, lineage, handoff, source navigation, state summary,
  impact, or support surfaces;
- converting pressure into ontology, runtime representation, priority, policy, or
  validation;
- proposing remediation for visibility failures.

## Required Tensions

| Tension | Observed shape |
| --- | --- |
| knowledge vs pressure | Knowledge can survive as supported content while pressure disappears as current concern. |
| facts vs concern | Facts answer what is supported; concern answers why it matters or pulls work now. |
| visibility vs preservation | A pressure can be visible in a moment but not preserved for continuation; preserved material can become invisible as pressure. |
| pressure vs terminology | Terms can change while the concern survives; terms can also survive after the pressure is gone. |
| inventory vs currentness | Inventories list available material; currentness identifies what matters for a present question or continuation point. |
| support vs significance | Support grounds a claim; significance explains why attention is warranted. |
| continuity vs vocabulary | Continuity is recognizable survival through change, not sameness of terms. |
| knowing vs caring | The repository can know or support something without preserving why anyone should care now. |

## Strongest Findings

- **Strongest pressure-visibility surfaces:** Current Work Position, Active Edge,
  handoff/continuation surfaces, inquiry/frontier documents, preservation-failure
  documents, discovery-path documents, operator-understanding surfaces, impact
  surfaces, source-navigation surfaces, and state summaries when tied to current
  operator questions.
- **Strongest pressure-preservation surfaces:** Handoff lineage, continuation
  context, discovery-path preservation, documentation lineage, preservation
  failure observations, non-selected remainder preservation, and frontier
  documents.
- **Strongest knowledge-without-pressure examples:** preserved handoff references
  without activation; source facts without navigation intent; state summaries or
  support views without current concern; documents without discovery path.
- **Strongest pressure-without-terminology examples:** learning, orientation,
  preservation, selection, activation, relevance, continuity, and understanding
  lenses weakening while continuation, selection, support, visibility, and
  preservation pressures remain.
- **Strongest Current Work Position finding:** it is a mixed knowledge/pressure
  surface whose pressure-bearing role is selected, continuation-relevant
  orientation.
- **Strongest Active Edge finding:** it is the most direct surface for currently
  pulling concern, but it risks duplication with selection, priority, attention,
  inquiry, and current work position.
- **Strongest visibility-failure finding:** survival of facts, artifacts,
  support, or conclusions is insufficient if currentness, concern, discovery
  path, or active edge is not preserved.
- **Strongest duplicate-work risk:** this observation could accidentally become a
  pressure ontology or repeat recent surviving-pressure and lens observations.
  Its safe scope is visibility across surfaces.

## Unresolved Observations

- The repository has not settled whether pressure is only a useful observation
  word, a family of concerns, a continuation property, an inquiry property, or a
  recurring feature of selection and attention surfaces.
- The repository has not settled when a pressure should remain preserved but
  inactive versus become current work.
- The repository has not settled how much discovery path is needed to preserve
  pressure without over-preserving every historical detail.
- The repository has not settled whether state summary, impact, and source
  navigation surfaces can preserve pressure by themselves or only expose pressure
  when paired with an operator question.
- The repository has not settled whether pressure survival across terminology
  changes is evidence of a stable phenomenon or evidence that multiple weaker
  phenomena are being grouped by participant interpretation.
- The repository has not settled how to prevent preserved documents from
  retaining conclusions while losing the concern that made those conclusions
  important.

## Closing Observation

The repository already knows how to preserve many things: facts, evidence,
claims, support, source relationships, documents, lineages, frontiers, summaries,
and handoff references. The pressure-visibility question appears when those
preserved things are not enough.

The strongest observed pattern is:

```text
preserved knowledge can become inert
    unless the repository also preserves why it mattered,
    what remained unresolved,
    what was current,
    what was selected,
    what path made it intelligible,
    or what edge was pulling work forward
```

The opposite pattern also appears:

```text
facts, terminology, and explanations can change
    while the pressure remains recognizable through continuity,
    inquiry, preservation, activation, handoff, support, and navigation surfaces
```

That recognition is useful only as an observation. It does not define pressure,
make pressure an object, or prescribe runtime behavior.
