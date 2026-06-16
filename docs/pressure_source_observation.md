---
doc_type: observation
status: exploratory
domain: pressure source observation
defines:
  - pressure source observation
  - observed pressure pattern
  - derived pressure pattern
  - pressure without complete facts pattern
  - pressure disappearance without resolution pattern
related:
  - pressure_visibility_and_preservation_observation.md
  - surviving_pressure_after_decomposition_observation.md
  - future_state_consequence_pressure_selection_observation.md
  - derived_consequence_and_relevance_observation.md
  - reference_point_and_concern_subject_observation.md
  - selection_convergence_observation.md
  - working_state_activation_observation.md
  - working_state_activation_failure_observation.md
  - current_work_position_frontier.md
  - active_edge_frontier.md
  - continuity_frontier.md
  - inquiry_frontier.md
  - preservation_surface_observation.md
  - preservation_failure_observation.md
  - discovery_path_preservation_observation.md
  - documentation_lineage_observation.md
  - lineage_distinction_observation.md
  - contradiction_discovery_and_visibility_reconciliation.md
---

# Pressure Source Observation

## Purpose

This observation investigates where repository pressures appear to come from.

It is an observation only. It is not a reconciliation, frontier, pressure
ontology, runtime representation proposal, implementation proposal,
prioritization method, execution policy, decision system, workflow redesign,
governance proposal, Seed identity statement, Seed goal statement, agency claim,
or survival policy.

The prior pressure-visibility work asked how pressure becomes visible and how it
is preserved. This document asks a narrower prior question:

```text
Where do pressures come from?
```

The investigation does not assume that every candidate source qualifies. It also
does not assume that pressure source, pressure, fact, impact, priority, and task
are the same thing.

## Method And Authority Boundary

Repository content was reviewed directly. Prompt-listed documents were treated as
starting points only. Review also used documentation maps, related frontiers,
adjacent observations, reconciliations, audits, implementation-facing read-model
documents, runtime surface documents, tests by name, and broad ripgrep searches.

Search terms used included: `pressure`, `source`, `origin`, `cause`, `trigger`,
`contradiction`, `gap`, `missing`, `future consequence`, `selection`, `current
concern`, `active edge`, `continuity risk`, `preservation failure`, `navigation
failure`, `activation failure`, `operator pain`, `question`, `frontier`,
`unknown`, `ambiguity`, `support gap`, `staleness`, `impact`, `disappear`,
`currentness`, `absence`, `resolution`, `observed`, `derived`, `relevance`, and
`handoff`.

The strongest inspected evidence included:

- `README.md`
- `docs/README.md`
- `01-architecture.md`
- `02-domain-model.md`
- `13-knowledge-and-evidence.md`
- `docs/architectural_status_and_next_frontier.md`
- `docs/architectural_knowledge_map.md`
- `docs/pressure_visibility_and_preservation_observation.md`
- `docs/surviving_pressure_after_decomposition_observation.md`
- `docs/lens_as_observation_and_compression_pattern.md`
- `docs/future_state_consequence_pressure_selection_observation.md`
- `docs/derived_consequence_and_relevance_observation.md`
- `docs/reference_point_and_concern_subject_observation.md`
- `docs/selection_convergence_observation.md`
- `docs/working_state_activation_observation.md`
- `docs/working_state_activation_failure_observation.md`
- `docs/current_work_position_frontier.md`
- `docs/active_edge_frontier.md`
- `docs/continuity_frontier.md`
- `docs/inquiry_frontier.md`
- `docs/preservation_surface_observation.md`
- `docs/preservation_failure_observation.md`
- `docs/discovery_path_preservation_observation.md`
- `docs/documentation_lineage_observation.md`
- `docs/lineage_distinction_observation.md`
- `docs/contradiction_discovery_and_visibility_reconciliation.md`
- `docs/operator_pain_as_frontier_signal.md`
- `docs/operator_surface_family_observation.md`
- `docs/operator_understanding_surface_observation.md`
- `docs/state_summary_authority_reconciliation.md`
- `docs/state_summary_top_entity_selection_audit.md`
- `docs/state_summary_endpoint_prominence_audit.md`
- `docs/impact_overview_authority_reconciliation.md`
- `docs/entity_impact_drilldown_reconciliation.md`
- `docs/claim_support_characterization.md`
- `docs/claim_support_design.md`
- `docs/claim_support_frontier.md`
- `docs/evidence_strength_and_claim_strength_reconciliation.md`
- `docs/context_composition_reconciliation.md`
- `docs/knowledge_lifecycle_reconciliation.md`
- `docs/causality_and_explanation_reconciliation.md`
- `seed_runtime/state_summary_views.py`
- `seed_runtime/state_views.py`
- `seed_runtime/context_views.py`
- `seed_runtime/context_selection.py`
- `seed_runtime/source_navigation.py`
- `tests/test_state_summary_views.py`
- `tests/test_source_navigation.py`
- `tests/test_fact_support_aggregation.py`

## High-Level Observation

Repository evidence supports pressure as arising when something makes continued
understanding, selection, navigation, preservation, support, or safe continuation
non-neutral. The source is often not a fact by itself. A fact can become
pressure-bearing when it conflicts, expires, lacks support, implies a future
consequence, blocks current work, exposes operator pain, or leaves a later
participant unable to continue.

The strongest pattern is:

```text
repository event or situation
    -> concern, gap, contradiction, consequence, failure, question, or risk
       becomes visible
    -> pressure appears when that visibility matters for continuation,
       selection, activation, explanation, or preservation
```

The review therefore supports a cautious distinction:

```text
pressure source != pressure
pressure != fact
pressure != impact
pressure != priority
pressure != implementation task
```

Those distinctions are not absolute architectural definitions. They are observed
boundaries that prevent documents about visibility, support, impact, selection,
and execution from absorbing one another.

## Pressure Source Inventory

### Contradictions

**What pressure becomes visible.** Contradictions create pressure around which
claims can be held together, which projected belief is current, what support is
missing, and what cannot be presented as settled.

**Evidence supporting it.** Contradiction-discovery work treats contradiction as
a visibility surface rather than automatic resolution. Context and knowledge
lifecycle documents also treat contradictions as read-only integrity or issue
signals that can affect selection and explanation.

**What weakens it.** A preserved contradiction can be inactive. It may remain a
known issue without pulling current work forward unless a question, selection
surface, operator need, or continuation boundary makes it matter now.

**Unresolved.** The repository does not settle whether every contradiction is a
pressure source or only contradictions that become relevant to a current concern.

### Support Gaps And Missing Support

**What pressure becomes visible.** Support gaps create pressure to qualify a
claim, withhold certainty, expose unsupported status, or preserve why a claim is
not yet grounded enough.

**Evidence supporting it.** Claim-support and evidence-strength documents
separate claim strength from assertion language and support. Knowledge lifecycle
work lists unsupported facts, support limits, source limitations, uncertainty,
and missing information as things response and selection may need to carry.

**What weakens it.** A support gap can be merely descriptive if no participant is
trying to use the claim. Missing support becomes pressure most clearly when a
claim is needed for explanation, selection, current-state projection, or operator
answering.

**Unresolved.** The repository leaves open how much support must be missing
before the absence becomes pressure rather than ordinary incompleteness.

### Future Consequences

**What pressure becomes visible.** Future consequences create pressure when a
present condition implies a possible later failure, cost, or impact even if the
future event has not occurred.

**Evidence supporting it.** Future-state consequence and derived-consequence
work shows relevance and selection pressure arising from predicted or derived
future outcomes. Impact documents separately preserve impact visibility without
making impact identical to priority or execution.

**What weakens it.** A future consequence can be speculative. Prediction work and
causality work warn that future claims, consequences, and causes require support
and uncertainty preservation.

**Unresolved.** The review does not establish when a derived future consequence
crosses from interesting possibility into active pressure.

### Continuity Risks

**What pressure becomes visible.** Continuity risk creates pressure when work may
not remain intelligible across time, session, participant, vocabulary change, or
artifact change.

**Evidence supporting it.** Continuity, current-work-position, active-edge,
handoff, and pressure-visibility documents repeatedly show that information can
survive while the active concern or safe continuation point disappears.

**What weakens it.** Continuity language can overreach if it becomes identity,
survival policy, or a general goal. The documents keep it bounded to specific
survival-through-change questions.

**Unresolved.** It remains unresolved whether continuity risk is a source of
pressure by itself or a family name for pressures from preservation, handoff,
selection, and activation failures.

### Preservation Failures

**What pressure becomes visible.** Preservation failure creates pressure when an
artifact remains but the usable support, discovery path, non-selected remainder,
lineage, currentness, or reason for importance is lost.

**Evidence supporting it.** Preservation-surface, preservation-failure,
discovery-path, documentation-lineage, and pressure-visibility observations all
record that repository material can be available while pressure, path, or
continuation meaning is not.

**What weakens it.** Not every loss is pressure. Some compression is legitimate,
and non-selected material can be intentionally left aside.

**Unresolved.** The repository has not settled which preservation losses must be
recorded as pressure disappearance, which are acceptable compression, and which
are simply ordinary omission.

### Activation Failures

**What pressure becomes visible.** Activation failure creates pressure when
preserved material exists but cannot become usable working state, current
context, or continuation guidance.

**Evidence supporting it.** Working-state activation and activation-failure work
separates having artifacts from activating them into usable continuation.
Current-work-position and active-edge work use similar evidence when asking what
is active now.

**What weakens it.** Activation is not the same as priority or execution. A
preserved concern can remain inactive without being wrong or failed.

**Unresolved.** The repository does not define how to distinguish healthy
inactivity from activation failure without smuggling in priority or task
semantics.

### Navigation Failures

**What pressure becomes visible.** Navigation failure creates pressure when a
participant cannot find source material, evidence paths, relevant documents,
claim support, or the reason one surface matters.

**Evidence supporting it.** Source-navigation, understanding-navigation,
discovery-path, documentation-lineage, and operator-surface documents preserve
navigation as a condition for understanding and continuation. State-summary and
operator-facing audits show that surfaces can exist but still mislead or fail to
route attention.

**What weakens it.** Navigation failure is sometimes a tooling or interface
problem rather than a pressure source in documentation content. This observation
therefore treats it as a repository situation capable of producing pressure, not
as an implementation mandate.

**Unresolved.** It remains unclear when navigation failure should be understood
as lost pressure, lost evidence, poor discoverability, or poor current selection.

### Operator Questions

**What pressure becomes visible.** Operator questions create pressure by making a
repository issue current and answer-relative. They can reveal missing evidence,
unclear authority, poor explanation, inadequate surface design, or unsupported
claims.

**Evidence supporting it.** Inquiry-frontier and operator-intent work treat
questions as carriers of unresolved understanding. Operator pain and state
summary audits show that repeated operator questions can redirect frontier
selection toward explanation and utility surfaces.

**What weakens it.** A question is not automatically authoritative pressure.
Repository authority and existing architecture constrain what a question can
change.

**Unresolved.** The repository does not settle whether operator questions are
sources of pressure, selectors of already-existing pressure, or both.

### Operator Pain

**What pressure becomes visible.** Operator pain creates pressure where actual
use exposes friction, confusion, repeated failed answers, missing capability, or
poor explanation.

**Evidence supporting it.** The operator-pain frontier-signal document explicitly
uses repeated operator pain as evidence for frontier selection. State-summary and
impact audits show pain around overly prominent endpoint metrics, explanation
gaps, and surfaces that do not match operator-relevant questions.

**What weakens it.** Pain does not by itself define architecture, priority,
identity, or execution policy. It is evidence, not a decision system.

**Unresolved.** It remains unresolved how much repeated pain is needed before it
should be treated as pressure rather than anecdotal feedback.

### Unknowns And Ambiguities

**What pressure becomes visible.** Unknowns and ambiguities create pressure when
they block explanation, require caveats, prevent safe continuation, or leave a
claim, cause, current position, or support state unsettled.

**Evidence supporting it.** Causality work preserves unknown cause as useful
rather than empty. Context and knowledge lifecycle work treat ambiguity,
unsupported facts, stale facts, and missing information as relevant issue
surfaces. Inquiry work treats unresolved understanding as capable of persisting.

**What weakens it.** Unknown does not always mean pressure. Some unknowns are
irrelevant to the current concern, and ambiguity can be acceptable when safely
qualified.

**Unresolved.** The repository does not provide a general rule for when unknown
or ambiguous material becomes active pressure.

### Frontiers, Current Concerns, And Active Edges

**What pressure becomes visible.** Frontiers, current concerns, and active edges
make pressure visible as a selected unresolved place where work can continue.
They preserve not only that something is unresolved, but why it is pulling work
now.

**Evidence supporting it.** Current-work-position asks what position current work
occupies. Active-edge asks what is currently pulling work forward. Inquiry and
continuity frontiers preserve active pursuit, unresolved tensions, selected
constraints, safe next moves, and authority boundaries.

**What weakens it.** These documents are exploratory. They cannot be treated as
runtime architecture, ontology settlement, or implementation priority.

**Unresolved.** It remains unresolved whether active edge is a pressure, a
pressure source, a selection result, a relationship, a role, or only a useful
name for a recurring phenomenon.

### Selection Conflicts

**What pressure becomes visible.** Selection conflicts create pressure when
multiple possible facts, concerns, frontiers, impacts, or explanations compete
for current relevance.

**Evidence supporting it.** Selection-convergence, context-composition,
attention, active-edge, and state-summary documents show that selection is not
truth, support, priority, or currentness by itself. Ranking and prominence can
produce pressure when the wrong thing dominates a surface.

**What weakens it.** Selection can expose pressure without causing it. A
selection surface may reveal a preexisting support gap, impact, contradiction, or
operator concern.

**Unresolved.** The repository does not settle whether selection conflict is a
source class or a visibility/activation route.

### Staleness

**What pressure becomes visible.** Staleness creates pressure when time weakens a
fact's current usability, when refresh status matters, or when a surface presents
old knowledge as current.

**Evidence supporting it.** Knowledge lifecycle, context composition,
observation refresh, current-state, and state-summary work all preserve temporal
status, freshness, expiry, latest-current semantics, and stale facts as selection
or explanation concerns.

**What weakens it.** Stale information can remain historically valid. Staleness
is pressure only when current use, explanation, safety, or relevance depends on
freshness.

**Unresolved.** The repository leaves open how staleness interacts with pressure
disappearance: a pressure may disappear because currentness is lost, or remain as
historical unresolved pressure.

### Missing Observations

**What pressure becomes visible.** Missing observations create pressure when the
repository cannot support a claim, answer a question, establish a cause, verify a
capability, or preserve a phenomenon that participants need to reason about.

**Evidence supporting it.** Observation-source, evidence, claim-support,
causality, and knowledge-acquisition documents distinguish known facts from
missing observations and preserve source limitations.

**What weakens it.** Missing observation is not automatically a task to observe.
Repository authority boundaries prevent this observation from becoming a data
collection or implementation proposal.

**Unresolved.** It remains unclear when absence of observation should be treated
as evidence of absence, support gap, unknown, or active pressure.

### Impact Visibility

**What pressure becomes visible.** Impact visibility creates pressure when the
consequence of a condition becomes understandable to an operator, entity,
service, or decision context.

**Evidence supporting it.** Impact overview and entity-impact drilldown documents
separate impact from authority and preserve impact as an explanation surface.
Future-consequence work links consequence visibility to selection pressure.

**What weakens it.** Impact is not pressure by itself. A visible impact may be
low relevance, historical, already accepted, or outside current authority.

**Unresolved.** The repository does not settle whether impact generates pressure
or only strengthens pressure that originates from a gap, failure, future
consequence, or operator concern.

## Observed And Derived Pressure

The review supports a tentative observed/derived distinction, but not as an
ontology.

### Strong observed-pressure patterns

Observed pressure appears strongest where the repository directly records a
situation that is already conflictual, blocking, painful, or unresolved:

```text
observed contradiction
    -> pressure to preserve conflict, support, and limits
```

```text
current work blocked or handoff unclear
    -> pressure to preserve current work position and next safe move
```

```text
operator repeatedly cannot answer a practical question
    -> pressure toward explanation, navigation, or surface adjustment
```

```text
artifact exists but cannot be activated
    -> pressure around working-state activation failure
```

### Strong derived-pressure patterns

Derived pressure appears strongest where the repository combines present evidence
with consequence, relevance, or absence:

```text
present metric or condition
    -> future consequence prediction
    -> pressure if consequence matters to current concern
```

```text
claim needed for explanation
    -> support is incomplete
    -> pressure to qualify or expose missing support
```

```text
documentation lineage exists
    -> discovery path is absent
    -> pressure that future participants may reconstruct the wrong path
```

```text
fact is stale
    -> current use is uncertain
    -> pressure if currentness is required
```

### What remains unresolved

The repository does not provide a stable boundary between observed and derived
pressure. Contradictions can be observed directly, but their relevance may be
derived. Future consequences are derived, but the present condition may be
observed. Missing ownership information may be observed as absence in a document,
derived as risk in handoff, and activated by a current operator question.

## Pressure And Facts

The review supports several cautious findings.

### Pressure can appear without settled facts

Pressure can appear from an unresolved question, unknown cause, ambiguity,
missing support, missing observation, or inability to continue. These situations
may not contain a settled fact beyond the existence of the gap, question, or
uncertainty.

### Pressure can appear with incomplete facts

Incomplete facts often strengthen rather than eliminate pressure when a current
answer, selection, or continuation depends on what is incomplete. Support gaps,
missing source coverage, partial lineage, stale observations, and unresolved
causes all show this pattern.

### Pressure can emerge from uncertainty, ambiguity, and absence

Uncertainty and ambiguity become pressure when they matter to explanation,
selection, current work position, operator understanding, or safe continuation.
Absence becomes pressure when the missing thing is needed: missing support,
missing observations, missing discovery path, missing ownership information,
missing currentness, or missing activation path.

### What weakens the finding

Unknown, ambiguity, and absence are not sufficient by themselves. Repository
evidence repeatedly requires a current concern, support need, operator question,
continuation risk, or relevance relation before absence becomes pressure.

## Pressure Lifecycle Review

Repository evidence suggests a lifecycle-shaped pattern but does not validate it
as architecture:

```text
pressure appears
    -> pressure becomes visible
    -> pressure becomes selected
    -> pressure becomes active
    -> pressure weakens
    -> pressure disappears
```

**Supported parts.** Pressure can appear from contradictions, gaps,
consequences, failures, questions, and risks. It can become visible through
frontiers, observations, state summaries, impact surfaces, support surfaces,
operator pain, and preservation documents. It can become selected through
current-work-position, active-edge, inquiry, attention, and selection surfaces.
It can become active through working-state activation, handoff consumption, or
operator-facing need.

**Weak parts.** The repository does not establish a required order. Some pressure
is active before it is well documented. Some pressure is preserved after it stops
being active. Some pressure disappears without evidence that it weakened in a
controlled sequence.

**Unresolved.** The lifecycle shape is useful as an observation checklist, but it
should not become a pressure architecture without further authority.

## Pressure Disappearance

Repository evidence supports pressure disappearance as distinct from pressure
resolution.

### Disappearance without resolution

Preservation-failure and pressure-visibility work show that facts, conclusions,
and documents can remain while the pressure that made them important disappears.
This can happen when current work position, discovery path, selection rationale,
active edge, or handoff context is not preserved.

### Disappearance because vocabulary changed

Surviving-pressure-after-decomposition work shows the opposite pattern too:
pressure may survive while vocabulary changes. However, vocabulary change can
also hide pressure if the new terms preserve conclusions but not the motivating
concern.

### Disappearance because currentness was lost

Current-work-position, active-edge, working-state activation, and staleness work
all support the possibility that a pressure disappears when a concern is no
longer current or can no longer be activated, even if historical knowledge
remains.

### Disappearance because preservation failed

Discovery-path, documentation-lineage, lineage-distinction, preservation-surface,
and preservation-failure documents support this as one of the strongest patterns:
pressure can be lost when path, support, remainder, or active rationale is not
carried forward.

### What remains unresolved

The repository does not always distinguish healthy disappearance from harmful
loss. Pressure may disappear because a question was answered, because it became
irrelevant, because vocabulary changed, because currentness was lost, or because
preservation failed. Those are different situations, and repository evidence does
not yet provide a complete classification.

## Current Work Position And Active Edge Findings

Current Work Position appears to preserve pressure source, selection,
activation, and continuity more strongly than ordinary summaries because it asks
what work is occupying now, why it is active, what unresolved pressure it sits
inside, what boundaries constrain it, and what move is safe next.

Active Edge appears to preserve the pulling part of pressure: the selected
unresolved concern, question, gap, contradiction, relationship, or frontier that
keeps work moving. It is especially useful for distinguishing a preserved concern
from an active concern.

The strongest finding is:

```text
Current Work Position preserves where work is situated.
Active Edge preserves what is pulling the situated work forward.
```

The weakest part is authority. Both are exploratory frontiers. They cannot define
runtime behavior, pressure ontology, priority, or implementation work.

## Preservation Of Pressure Sources

Preservation, lineage, inquiry, continuity, handoff, and discovery-path work
preserve pressure sources unevenly:

- Frontiers preserve unresolved questions, tensions, and candidate directions.
- Observations preserve evidence patterns and weak/strong findings.
- Reconciliations preserve authority boundaries and settled distinctions.
- Discovery-path documents preserve how a concern was found.
- Documentation-lineage documents preserve artifact relationships but may miss
  causal inquiry pressure.
- Handoff documents preserve activation, constraints, live branches, and next
  safe moves when they are explicit.
- State summaries and impact surfaces preserve operator-facing visibility but
  can obscure source if prominence or selection rationale is missing.
- Claim-support surfaces preserve support pressure but not necessarily current
  concern.

The strongest preservation finding is that pressure source survives best when a
document preserves both the evidence and the reason the evidence mattered.

## Critical Distinctions Reviewed

The evidence supports these distinctions as useful observation boundaries:

- **Pressure source != pressure.** A contradiction, gap, question, future
  consequence, or failure may source pressure, but pressure appears when it
  matters to continuation, selection, activation, understanding, or explanation.
- **Pressure != fact.** Facts can carry pressure, but absence, uncertainty,
  ambiguity, stale currentness, or missing support can also create pressure.
- **Pressure != impact.** Impact can make pressure legible, but impact is not
  automatically active concern, priority, or task.
- **Pressure != priority.** Selection or active edge can make pressure current
  without authorizing implementation priority.
- **Pressure != implementation task.** A pressure source may justify observation
  without implying remediation.
- **Pressure disappearance != pressure resolution.** Pressure can vanish because
  currentness, vocabulary, path, or preservation failed, not because the concern
  was answered.
- **Unknown != absence of pressure.** Unknown cause, missing support, and
  unanswered questions can be pressure-bearing.
- **Ambiguity != absence of pressure.** Ambiguity can require qualification,
  selection care, or preservation when it matters.

The main weakening factor is that these distinctions are inferred across many
observations and frontiers. They should remain observation boundaries, not a new
pressure ontology.

## Duplicate-Work Check

### Prior documents already own

- `pressure_visibility_and_preservation_observation.md` owns how pressure becomes
  visible and where pressure is preserved.
- `surviving_pressure_after_decomposition_observation.md` owns the finding that
  pressure can survive while vocabulary changes.
- `future_state_consequence_pressure_selection_observation.md` owns future
  consequence as a selection-pressure pattern.
- `derived_consequence_and_relevance_observation.md` owns derivation and
  relevance pressure around consequences.
- `reference_point_and_concern_subject_observation.md` owns reference point and
  concern-subject distinctions.
- `selection_convergence_observation.md`, context-composition, and attention
  documents own selection boundaries.
- `working_state_activation_observation.md` and
  `working_state_activation_failure_observation.md` own activation patterns and
  failures.
- `current_work_position_frontier.md` and `active_edge_frontier.md` own their
  exploratory frontier questions.
- `continuity_frontier.md` and `inquiry_frontier.md` own continuity and inquiry
  frontier questions.
- Preservation, discovery-path, documentation-lineage, and lineage-distinction
  documents own preservation and lineage distinctions.
- Claim-support, impact, state-summary, and operator-pain documents own their
  respective support, impact, summary, and operator-surface findings.

### What this observation adds

This observation gathers those surfaces around pressure origins. It asks what
repository events or situations appear capable of generating pressure, whether
pressure can exist without complete facts, whether pressure can disappear without
resolution, and whether observed and derived pressure patterns are visible.

### What this observation should avoid duplicating

It should not restate pressure visibility as a whole, redesign preservation
surfaces, define Current Work Position or Active Edge, settle selection theory,
rank priorities, propose impact behavior, specify claim-support mechanics, or
turn operator pain into a decision system.

## Major Findings

1. The strongest pressure-source patterns are contradictions, support gaps,
   future consequences, continuity risks, preservation failures, activation
   failures, navigation failures, operator questions, operator pain, unknowns,
   ambiguities, current concerns, active edges, selection conflicts, staleness,
   missing observations, missing support, and impact visibility.
2. The strongest observed-pressure patterns are direct contradictions, blocked
   current work, activation failures, unresolved operator questions, and
   repeated operator pain.
3. The strongest derived-pressure patterns are future consequence prediction,
   support-gap inference, currentness/staleness inference, missing lineage risk,
   and impact relevance.
4. Pressure can appear without settled facts, but usually not without some
   pressure-bearing situation such as a question, absence, uncertainty,
   ambiguity, failure, or risk.
5. Pressure can disappear without resolution when vocabulary, currentness,
   discovery path, handoff context, or preservation fails.
6. Current Work Position and Active Edge are the strongest reviewed surfaces for
   distinguishing preserved pressure from active pressure, but they remain
   exploratory.
7. Preservation of pressure source is strongest when evidence, source, path,
   current concern, selection rationale, and activation context are preserved
   together.

## Required Tensions

### Fact vs pressure

Facts can support pressure, but pressure can also arise from absence,
uncertainty, ambiguity, staleness, or inability to continue. The tension remains
because pressure needs something to be about, but that something need not be a
settled factual claim.

### Knowledge vs pressure

Knowledge can survive while pressure disappears. Pressure can survive while
vocabulary changes. Knowledge preservation and pressure preservation therefore
overlap but do not collapse into one another.

### Observation vs derivation

Some pressure is observed directly as contradiction, pain, failure, or blocked
work. Some pressure is derived from future consequence, support absence,
staleness, lineage loss, or impact. Repository evidence does not settle a hard
boundary.

### Resolution vs disappearance

Resolved pressure and disappeared pressure are different. Disappearance can mean
answered concern, lost currentness, vocabulary drift, failed preservation, or
irrelevance.

### Unknown vs absence

Unknown is not empty. Unknown cause, missing support, and unanswered questions can
be preserved as meaningful pressure-bearing states.

### Ambiguity vs certainty

Ambiguity can carry pressure when a participant needs to answer, select, qualify,
or continue safely. Certainty can reduce some pressure, but unsupported certainty
can create another pressure.

### Selection vs pressure

Selection can activate pressure, reveal pressure, or distort pressure. Selection
is not identical to pressure and should not become priority or execution policy.

### Currentness vs preservation

Preservation can keep artifacts while losing currentness. Currentness can make a
preserved item pressure-bearing, but currentness can also fade while historical
knowledge remains.

### Visibility vs source

Visibility work explains how pressure can be seen. Source work asks what
situations appear capable of generating pressure. A surface can make pressure
visible without being the source.

## Unresolved Observations

- Whether pressure requires a current concern or whether some sources are
  pressure-bearing before selection.
- Whether observed and derived pressure should remain informal patterns or be
  reconciled later as documented distinctions.
- Whether continuity risk is its own source or a composite of preservation,
  handoff, activation, and selection pressures.
- Whether impact visibility generates pressure or only exposes consequence.
- Whether operator questions source pressure, select pressure, or both.
- Whether pressure disappearance can be identified reliably after the fact.
- How to distinguish healthy pressure disappearance from preservation failure.
- How much uncertainty, ambiguity, absence, or missing support is enough to make
  pressure active.
- Whether Active Edge names pressure itself, a pressure source, a selection
  result, or only a recurring continuation phenomenon.
- How much pressure source history must be preserved for future participants to
  understand pressure without duplicating every discovery path.
