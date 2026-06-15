---
doc_type: observation
status: exploratory
domain: understanding navigation
introduced_by: understanding navigation observation
depends_on:
  - understanding_visibility_existing_surface_audit.md
  - operator_surface_family_observation.md
  - operator_understanding_surface_observation.md
  - current_work_position_frontier.md
  - active_edge_frontier.md
  - continuity_frontier.md
  - architectural_knowledge_map.md
  - knowledge_navigation_layers_frontier.md
  - discovery_path_preservation_observation.md
  - navigation_hygiene_audit.md
  - operator_navigation_reconciliation.md
  - source_navigation_surface_reconciliation.md
  - handoff_consumption_activation_reconciliation.md
  - documentation_lineage_observation.md
related:
  - docs/README.md
  - index.md
  - architectural_findings_preservation.md
  - preservation_surface_observation.md
  - inquiry_frontier.md
  - handoff_bootstrap_and_summary_reconciliation.md
---

# Understanding Navigation Observation

## Purpose

This observation investigates whether repository understanding is currently
difficult to navigate.

It asks:

```text
How does a participant locate relevant understanding?
```

and:

```text
How does a participant know which surface to consult?
```

and:

```text
Does the repository already contain an understanding-navigation model?
```

This is an observation only. It is not a reconciliation, frontier,
implementation proposal, workflow proposal, UI requirement, governance model,
schema proposal, ontology definition, routing mandate, or remediation plan. It
does not redesign documentation navigation, define a new navigation system, or
promote exploratory findings into repository authority. Repository authority
remains with the documents, maps, reconciliations, audits, implementation files,
and tests that own their respective scopes.

## Method

The investigation treated the requested documents as starting points rather than
a closed scope. It reviewed repository maps, indexes, navigation surfaces,
frontmatter references, cross-document dependencies, adjacent observations,
continuation and handoff documents, activation work, source-navigation audits,
preservation observations, inquiry lineage work, documentation lineage work, and
operator-surface work.

Documents inspected included:

- `README.md`
- `docs/README.md`
- `docs/index.md`
- `docs/architectural_knowledge_map.md`
- `docs/knowledge_navigation_layers_frontier.md`
- `docs/navigation_hygiene_audit.md`
- `docs/operator_navigation_reconciliation.md`
- `docs/understanding_visibility_existing_surface_audit.md`
- `docs/operator_surface_family_observation.md`
- `docs/operator_understanding_surface_observation.md`
- `docs/current_work_position_frontier.md`
- `docs/active_edge_frontier.md`
- `docs/continuity_frontier.md`
- `docs/discovery_path_preservation_observation.md`
- `docs/source_navigation_surface_reconciliation.md`
- `docs/source_navigation_without_grep_audit.md`
- `docs/source_navigation_query_surface_design_audit.md`
- `docs/source_navigation_practical_validation_audit.md`
- `docs/preservation_surface_observation.md`
- `docs/preservation_failure_observation.md`
- `docs/architectural_findings_preservation.md`
- `docs/audit_chain_findings_preservation.md`
- `docs/handoff_consumption_activation_reconciliation.md`
- `docs/handoff_bootstrap_and_summary_reconciliation.md`
- `docs/handoff_and_continuation_lineage_frontier.md`
- `docs/handoff_alignment_guardrails_reconciliation.md`
- `docs/continuation_context_and_working_state_reconciliation.md`
- `docs/handoff_template_and_continuation_protocol_reconciliation.md`
- `docs/inquiry_frontier.md`
- `docs/documentation_lineage_observation.md`
- `docs/lineage_distinction_observation.md`
- `docs/interpretation_candidate_preservation_audit.md`
- `docs/state_summary_authority_reconciliation.md`
- `docs/impact_overview_authority_reconciliation.md`
- `docs/claim_support_frontier.md`
- `docs/fact_support_aggregation_design.md`
- `docs/operator_intent_question_and_claim_interface_reconciliation.md`

Search terms used included:

```text
navigation
orientation
activation
selection
routing
discovery
finding
location
current work
active edge
continuation
knowledge map
knowledge navigation
source navigation
understanding visibility
understanding surface
state summary
impact
fact support
handoff
lineage
preservation
inquiry
where should I look
consult
```

Repository discovery commands included broad `rg` searches across repository
content and narrower file-name discovery using `rg --files docs` filtered for
navigation, understanding, preservation, continuation, handoff, activation,
lineage, and source-navigation terms.

## Central Observation

Repository understanding is visible, but visibility is not the same as
navigation.

Existing work strongly preserves answers to:

```text
What understanding exists?
Which surfaces communicate understanding?
Where is a concern owned?
What documents preserve completed findings?
```

Existing work less directly preserves answers to:

```text
I have a question. Where should I look first?
Which surface should I consult before I already know the answer category?
How do I choose between adjacent understanding surfaces?
How did prior participants find the understanding they used?
```

The repository therefore appears to contain several navigation-capable surfaces,
but not a single settled understanding-navigation model. Navigation exists as a
distributed behavior across maps, indexes, frontmatter, continuation bootstraps,
source-navigation surfaces, operator-navigation work, and active-frontier
surfaces.

## Visibility Is Not Navigation

`understanding_visibility_existing_surface_audit.md` already owns the finding
that understanding visibility exists and is distributed. It identifies strong
understanding-oriented surfaces, especially Current Work Position, Active Edge,
continuity, operator-surface observations, State Summary, Impact, Fact Support,
Source Navigation, response/explanation surfaces, and related visibility work.

This observation should not duplicate that inventory.

The distinct concern here is:

```text
understanding visibility
    = the repository has places where understanding can be seen

understanding navigation
    = a participant can locate the relevant place without already knowing it
```

A surface can make understanding visible after arrival while still doing little
to help a participant decide that it is the correct destination. Conversely, a
map or handoff may route participants effectively while not itself containing the
full understanding.

This distinction explains the recurring failure pattern:

```text
the answer already exists

but participants look in the wrong place
```

The failure is not necessarily absence of understanding. It may be a failure of
surface selection, route recognition, activation, or discovery-path preservation.

## Existing Understanding-Navigation Surfaces

### Repository and Documentation Orientation

`README.md` is the broad repository orientation surface. It tells a new
participant where the documentation map, ontology, architecture thesis, status,
and knowledge map live. It provides the first coarse route but intentionally does
not own detailed documentation navigation.

`docs/README.md` is the documentation navigation authority. It routes readers to
documents that own answers rather than restating those answers. It is the
strongest general-purpose orientation surface for participants who know they are
looking for documentation authority.

`docs/index.md` provides a denser index. It is useful when a participant already
has a likely title, domain, or cluster. It is less obviously a question-to-surface
router for participants who only know that they have a question.

### Concern Routing

`docs/architectural_knowledge_map.md` is the strongest concern-routing surface.
It owns orientation and routing only, and it explicitly avoids owning current
status, roadmap sequencing, lifecycle definitions, or canonical architecture
content. Its navigation value is that it groups architectural concerns and points
to owning documents.

`docs/knowledge_navigation_layers_frontier.md` is the strongest meta-navigation
surface. It identifies structural navigation, architectural navigation, and
knowledge navigation as related but non-identical layers. It does not settle an
understanding-navigation model, but it provides the clearest repository evidence
that navigation itself has become an architectural concern.

### Operator Navigation and Source Navigation

`docs/operator_navigation_reconciliation.md` and source-navigation documents show
that some navigation problems are already owned in narrower domains. Operator
navigation concerns how participants move through operator-facing questions and
projection/explanation surfaces. Source Navigation concerns movement from
runtime/projected knowledge back to source evidence and source structure.

These documents are strong navigation surfaces, but their authority is bounded.
They should not be treated as universal understanding-navigation models.

### Current Work Position and Active Edge

`docs/current_work_position_frontier.md` and `docs/active_edge_frontier.md` are
strong understanding-oriented surfaces and also participate in navigation.

Current Work Position helps answer:

```text
Where is the work located now?
What position does the current investigation occupy?
What must survive for continuation to feel intelligible?
```

Active Edge helps answer:

```text
What is currently pulling work forward?
Which question, gap, contradiction, or tension is active?
What is the continuation edge?
```

Their navigation role is not general map routing. They orient a participant once
a work thread is active or once a continuation question has been recognized. They
are weaker as first-contact surfaces for a participant who has only a broad
question and no known work position.

### Handoff and Activation Surfaces

Handoff and continuation documents preserve a different navigation behavior:
activation. They distinguish availability of guidance from consumption and
activation of that guidance. This matters for understanding navigation because a
participant may have the correct document available without making it part of
working state.

The strongest activation surfaces are:

- `docs/handoff_consumption_activation_reconciliation.md`
- `docs/handoff_bootstrap_and_summary_reconciliation.md`
- `docs/handoff_template_and_continuation_protocol_reconciliation.md`
- `docs/continuation_context_and_working_state_reconciliation.md`

These documents suggest that navigation failure can occur after discovery: a
participant can find the right handoff or summary and still fail to activate the
constraints, references, or current boundaries.

### Discovery-Path and Lineage Surfaces

`docs/discovery_path_preservation_observation.md`,
`docs/documentation_lineage_observation.md`, `docs/inquiry_frontier.md`, and
`docs/handoff_and_continuation_lineage_frontier.md` preserve evidence about how
investigations, questions, and documents lead to one another.

These are the strongest discovery-path surfaces. They help explain how
understanding was found or generated, not merely what understanding exists.
However, they are mostly retrospective. They preserve discovery paths and
lineage, but they do not necessarily provide a participant-facing route from an
arbitrary question to the appropriate understanding surface.

## Surface Selection Findings

Repository evidence partially distinguishes when specific surfaces should be
consulted, but the distinctions are distributed and uneven.

| Surface | Existing selection signal | Navigation limitation |
| --- | --- | --- |
| Current Work Position | Consult when the question is about where current work is situated, what survives for continuation, or what position an investigation occupies. | It assumes a recognized work thread; it is not a general first-stop map. |
| Active Edge | Consult when the question is about what is pulling work forward, which tension is live, or what the next continuation edge is. | It does not replace ownership maps and can be mistaken for prioritization or workflow. |
| State Summary | Consult when the question is about current projected state and read-only summary authority. | It summarizes state; it does not route all understanding questions. |
| Impact | Consult when the question is about impact overview/read-model authority and operator relevance. | It can communicate significance but should not own source support or current-work ontology. |
| Fact Support | Consult when the question is about evidence/support/confidence behind facts. | It explains support for claims, not where to begin a broad repository investigation. |
| Source Navigation | Consult when the question is about tracing projected/imported knowledge back to preserved source origins. | It owns source tracing, not general documentation discovery or understanding-surface selection. |
| README/docs README/index | Consult for repository and documentation orientation. | They route by known concern or document family more than by participant question phrasing. |
| Architectural Knowledge Map | Consult for concern ownership and architectural routing. | It explicitly does not own current status, active frontier, roadmap sequencing, or full content. |
| Handoff/activation documents | Consult when continuing prior work or consuming bootstrap guidance. | They require the participant to recognize continuation context. |

The repository therefore contains many surface-selection clues, but no single
place appears to answer every version of:

```text
I have a question. Where should I look?
```

without requiring prior familiarity with Seed's document families.

## Strongest Findings by Category

### Strongest Understanding-Navigation Surfaces

1. `docs/README.md` for documentation map authority.
2. `docs/architectural_knowledge_map.md` for concern ownership and routing.
3. `docs/knowledge_navigation_layers_frontier.md` for recognizing navigation as
   layered architectural behavior.
4. `docs/operator_navigation_reconciliation.md` for bounded operator-question
   navigation.
5. `docs/source_navigation_surface_reconciliation.md` and adjacent audits for
   source-origin navigation.

### Strongest Orientation Surfaces

1. `README.md` for repository-level orientation.
2. `docs/README.md` for documentation-level orientation.
3. `docs/index.md` for dense document discovery.
4. `docs/architectural_knowledge_map.md` for concern-level orientation.
5. `docs/architectural_status_and_next_frontier.md` for current status and active
   frontier orientation, when currentness is the concern.

### Strongest Activation Surfaces

1. `docs/handoff_consumption_activation_reconciliation.md`
2. `docs/handoff_bootstrap_and_summary_reconciliation.md`
3. `docs/continuation_context_and_working_state_reconciliation.md`
4. `docs/handoff_template_and_continuation_protocol_reconciliation.md`
5. `docs/current_work_position_frontier.md` and `docs/active_edge_frontier.md`
   when a participant must activate the live position and edge of work.

### Strongest Discovery-Path Surfaces

1. `docs/discovery_path_preservation_observation.md`
2. `docs/documentation_lineage_observation.md`
3. `docs/inquiry_frontier.md`
4. `docs/handoff_and_continuation_lineage_frontier.md`
5. `docs/lineage_distinction_observation.md`

### Strongest Navigation Failures Observed

The strongest failure pattern is not missing documentation. It is mismatched
entry point.

Observed failure modes include:

- participants ask an understanding question but enter through an inventory
  surface;
- participants ask a continuation question but enter through a static map;
- participants ask a support question but enter through State Summary or Impact;
- participants ask a source-origin question but do not use Source Navigation;
- participants ask a current-frontier question but use preserved findings or
  historical lineage as if they were current status;
- participants find the right handoff but do not activate it as working-state
  constraint;
- participants use `rg` successfully but do not preserve how the answer was
  found, causing later rediscovery.

## Duplicate-Work Check

### Prior Documents Already Own

- `understanding_visibility_existing_surface_audit.md` owns the distributed
  understanding-visibility finding and the inventory of surfaces where
  understanding is visible.
- `operator_surface_family_observation.md` owns the operator-surface family
  observation across inventory, understanding, explanation, and mixed surfaces.
- `operator_understanding_surface_observation.md` owns the distinction between
  what Seed contains and what Seed currently understands from an
  operator-surface perspective.
- `architectural_knowledge_map.md` owns concern-level routing and map-like
  orientation, but not current status or full content.
- `knowledge_navigation_layers_frontier.md` owns the exploratory finding that
  Seed has multiple navigation layers.
- `operator_navigation_reconciliation.md` owns bounded operator-navigation
  reconciliation.
- Source-navigation documents own tracing from projected/imported knowledge back
  to source structure and source evidence.
- Handoff and continuation documents own bootstrap, consumption, activation,
  continuation alignment, and working-state boundaries.
- Preservation and lineage documents own preservation of findings, inquiry
  paths, and documentation lineage.

### This Observation Adds

This observation adds a narrow distinction:

```text
understanding visibility
    !=
understanding navigation
```

It asks whether participants can choose the right understanding surface before
they already know the answer category. It treats Current Work Position and Active
Edge as navigation-participating surfaces while preserving their frontier status
and avoiding redesign.

### This Observation Should Avoid Duplicating

This document should not become:

- a new documentation map;
- a replacement for `docs/README.md`, `docs/index.md`, or
  `docs/architectural_knowledge_map.md`;
- a universal surface-selection workflow;
- a new operator-navigation reconciliation;
- a source-navigation redesign;
- an understanding-visibility inventory;
- a handoff or continuation protocol;
- a remediation proposal.

## Required Tensions

### Visibility vs Navigation

Understanding can be visible once found while still hard to locate. Visibility
answers availability; navigation answers route selection.

### Understanding vs Finding Understanding

Understanding-oriented surfaces can explain the current work, active edge,
state, impact, or support. They do not automatically explain how a participant
with an unclassified question should find the right surface.

### Knowledge Preservation vs Knowledge Discovery

Preservation surfaces reduce rediscovery by keeping findings durable. Discovery
surfaces preserve how findings were located or generated. The repository has
both, but discovery-path preservation is less uniformly attached to every answer
than finding preservation.

### Routing vs Explanation

Maps route to owners. Explanation surfaces explain claims, supports, conflicts,
and projections. A participant can need both, but one should not be mistaken for
the other.

### Orientation vs Inventory

Indexes and maps orient participants across documents. Inventories enumerate
what exists. A dense inventory may be useful after a domain is recognized but may
not answer which surface should be consulted first.

### Activation vs Availability

A handoff, map, or frontier can be available without becoming active working
context. Activation documents show that navigation failure can occur even after
the correct document is found.

## Unresolved Observations

- The repository appears to have distributed understanding-navigation behavior,
  but not a single settled understanding-navigation model.
- The documentation map and architectural knowledge map are strong orientation
  and routing surfaces, but their ability to route from arbitrary participant
  questions is uneven.
- Current Work Position and Active Edge participate in navigation after a work
  thread or live tension is recognized, but their role as first-contact
  navigation surfaces remains unclear.
- Source Navigation strongly preserves source-origin discovery, but it should
  not be generalized into all understanding navigation.
- Handoff activation work shows that finding a document is not enough; the
  participant must activate the relevant constraints and boundaries.
- Discovery-path preservation exists, but it is not clear that every important
  understanding answer preserves the path by which it was found.
- The strongest duplicate-work risk is turning this observation into another map
  or workflow instead of leaving map authority, source-navigation authority,
  operator-navigation authority, and handoff authority in their existing owners.

## Closing Finding

The repository already contains substantial understanding-navigation material,
but it is distributed across orientation maps, concern-routing maps,
operator-navigation work, source-navigation work, continuation activation,
discovery-path preservation, and active-frontier documents.

That distribution appears sufficient to show that understanding navigation is a
real repository concern. It does not show that the repository has one settled,
participant-facing model for choosing the correct understanding surface from an
unclassified question.

The safest observation is therefore:

```text
understanding visibility exists
understanding navigation exists in distributed form
understanding visibility is not the same concern as understanding navigation
surface selection remains the most visible unresolved navigation pressure
```
