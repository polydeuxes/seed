---
doc_type: observation
status: exploratory
domain: situatedness preservation and failure observation
introduced_by: situatedness preservation and failure observation
depends_on:
  - situatedness_and_pressure_observation.md
  - pressure_source_observation.md
  - pressure_visibility_and_preservation_observation.md
  - surviving_pressure_after_decomposition_observation.md
  - current_work_position_frontier.md
  - active_edge_frontier.md
  - continuity_frontier.md
  - working_state_activation_observation.md
  - working_state_activation_failure_observation.md
  - reference_point_and_concern_subject_observation.md
  - preservation_surface_observation.md
  - preservation_failure_observation.md
related:
  - discovery_path_preservation_observation.md
  - documentation_lineage_observation.md
  - lineage_distinction_observation.md
  - handoff_and_continuation_lineage_frontier.md
  - operator_surface_family_observation.md
  - operator_understanding_surface_observation.md
  - understanding_navigation_observation.md
  - understanding_visibility_existing_surface_audit.md
---

# Situatedness Preservation And Failure Observation

## Purpose

This observation investigates what appears to be preserved when Current Work
Position succeeds, what appears to be lost when it fails, and what repository
work preserves besides knowledge.

It is not a reconciliation, frontier, ontology, runtime proposal,
representation proposal, implementation proposal, interface redesign, workflow
redesign, governance proposal, schema proposal, decision-system proposal, Seed
identity statement, Seed goal statement, agency claim, survival policy, or
remediation plan.

The central prompt for this review was:

```text
same thing known
    !=
same thing mattering
```

The investigation treats that as a question, not a conclusion.

## Method And Authority Boundary

Repository content was reviewed directly. The named prompt documents were
starting points only. Review also used repository maps, adjacent frontiers,
reconciliations, audits, runtime-facing architecture documents, tests by name,
and implementation read-model surfaces.

Search terms used included: `current work`, `active edge`, `continuity`,
`situated`, `situation`, `orientation`, `current concern`, `active concern`,
`pressure`, `pressure disappearance`, `preservation failure`, `continuation`,
`resumption`, `activation failure`, `boundary`, `constraint`, `safe move`,
`safe continuation`, `currentness`, `why this matters`, `significance`,
`relevance`, `position`, `working state`, `answer existed`, `wrong work`, and
`activation failed`.

Documents and surfaces inspected included:

- `README.md`
- `docs/README.md`
- `01-architecture.md`
- `02-domain-model.md`
- `13-knowledge-and-evidence.md`
- `docs/situatedness_and_pressure_observation.md`
- `docs/pressure_source_observation.md`
- `docs/pressure_visibility_and_preservation_observation.md`
- `docs/surviving_pressure_after_decomposition_observation.md`
- `docs/current_work_position_frontier.md`
- `docs/active_edge_frontier.md`
- `docs/continuity_frontier.md`
- `docs/working_state_activation_observation.md`
- `docs/working_state_activation_failure_observation.md`
- `docs/working_state_activation_artifact_audit.md`
- `docs/understanding_visibility_existing_surface_audit.md`
- `docs/understanding_navigation_observation.md`
- `docs/reference_point_and_concern_subject_observation.md`
- `docs/preservation_surface_observation.md`
- `docs/preservation_failure_observation.md`
- `docs/discovery_path_preservation_observation.md`
- `docs/documentation_lineage_observation.md`
- `docs/lineage_distinction_observation.md`
- `docs/inquiry_frontier.md`
- `docs/handoff_and_continuation_lineage_frontier.md`
- `docs/handoff_pressure_transition_observation.md`
- `docs/continuation_context_and_working_state_reconciliation.md`
- `docs/handoff_consumption_activation_reconciliation.md`
- `docs/handoff_document_boundary_reconciliation.md`
- `docs/operator_surface_family_observation.md`
- `docs/operator_understanding_surface_observation.md`
- `docs/operator_navigation_reconciliation.md`
- `docs/orientation_object_observation.md`
- `docs/knowledge_and_understanding_distinction_observation.md`
- `docs/derived_consequence_and_relevance_observation.md`
- `docs/selection_convergence_observation.md`
- `docs/non_selected_remainder_preservation_observation.md`
- `docs/documentation_compression_observation.md`
- `docs/bootstrap_invariants.md`
- `seed_runtime/context.py`
- `seed_runtime/context_selection.py`
- `seed_runtime/context_views.py`
- `seed_runtime/state_views.py`
- `seed_runtime/state_summary_views.py`
- `seed_runtime/source_navigation.py`
- `tests/test_context_selection.py`
- `tests/test_state_views.py`
- `tests/test_state_summary_views.py`
- `tests/test_source_navigation.py`
- `tests/test_handoff_plans.py`

Runtime and test surfaces were inspected only for vocabulary overlap and
read-model evidence. This observation does not promote situatedness into runtime
state or schema.

## High-Level Observation

Repository evidence supports a cautious finding:

```text
Current Work Position succeeds when it preserves a positioned relation,
not merely a set of facts.
```

That relation appears to include, in varying combinations, a reference point,
current concern, continuity concern, active pressure, constraints, selected work,
and next safe movement. The evidence does not support making those a required
ontology. It supports only that repository work repeatedly loses something when
facts, documents, support, or lineage survive without their active position.

The strongest repeated failure shape is:

```text
answer available
+ document available
+ support available
- active work-position
= wrong or drifting work remains possible
```

The strongest repeated success shape is:

```text
reference point
+ current concern
+ relevant constraints
+ active edge
+ next safe move
= safe continuation without replaying all history
```

## Current Work Position Success Findings

When Current Work Position works well, it appears to preserve **where the work is
standing relative to what matters now**. The preserved item is not only a topic
or fact inventory.

Strong candidates that survive review:

1. **Current concern.** Repository work repeatedly distinguishes material that is
   true or available from material that governs the present move. Current concern
   seems to preserve why this fact, document, risk, or question matters now.
2. **Reference point.** Significance often depends on what the condition is read
   relative to: operator question, repository continuity, authority boundary,
   host, datastore, evidence surface, or continuation need.
3. **Continuity concern.** Current Work Position preserves what must remain
   intelligible for a later participant to resume without confusing current work
   with a general knowledge inventory.
4. **Boundary and constraint awareness.** Successful current work carries what
   must not be crossed: authority boundaries, non-implementation constraints,
   read-only surfaces, handoff limits, and scope limits.
5. **Selected work and active question.** It preserves which branch is live,
   which question is being tested, and which alternatives are merely background
   or non-selected remainder.
6. **Next safe movement.** It often contains enough immediate direction to avoid
   transcript replay while not making the next move authoritative.

Weaker candidates:

- **Orientation** survives as useful shorthand, but prior decomposition warns
  against treating it as a single object.
- **Situation** and **situatedness** are useful observational names, but the
  repository does not make them canonical categories.
- **Pressure context** survives strongly, but pressure can be visible without
  being active, so pressure context is not identical to Current Work Position.

## Current Work Position Failure Findings

Failure appears when knowledge survives but no longer governs the work that
needed it. The reviewed documents describe several neighboring loss modes rather
than a single settled cause.

Observed loss modes:

1. **Availability without activation.** A document can exist, be found, or even
   be understood in a local sense while failing to constrain the current move.
2. **Support without significance.** Evidence and support can survive while the
   reason the supported claim matters now disappears.
3. **History without currentness.** Lineage can preserve where a finding came
   from while losing whether it is still active, selected, or relevant to the
   current concern.
4. **Continuation without position.** Handoff and continuation artifacts can
   preserve references and status but lose what work was live, what was just
   completed, and what safe move was next.
5. **Inventory without orientation.** Broad knowledge maps can preserve many
   relevant items while still requiring rediscovery of which item matters under
   the active question.
6. **Answer without correct work.** The repository pattern is not merely “the
   answer was missing”; it is often “the answer existed, but work drifted because
   the answer was not situated as governing.”

No single common cause is established. Failures can arise from compression,
missing activation, stale currentness, excessive artifact survival, weak
selection rationale, lost pressure, or boundary collapse.

## Situatedness Preservation Findings

Repository work already preserves situatedness-like relations without naming them
as situatedness. The strongest examples are phrases and structures that answer:

```text
why this matters
why now
relative to what
under which concern
for which continuation
```

Observed preservation surfaces:

- **Current Work Position** preserves active relation to work rather than durable
  architecture.
- **Active Edge** preserves the selected unresolved edge rather than all known
  questions.
- **Continuity context** preserves resumption relevance rather than historical
  completeness.
- **Discovery path preservation** preserves how a finding became reachable, not
  just the finding.
- **Lineage documents** preserve ancestry and transformation, while adjacent
  documents warn that lineage alone is not activation.
- **Operator-surface observations** preserve how understanding becomes visible
  to an operator, not merely what the runtime knows.
- **Read-model and context surfaces** preserve selection, relevance, support,
  and boundary metadata for use, but do not themselves establish situatedness as
  a runtime object.

The strongest situatedness-preservation finding is that repository work often
preserves a **relation of use**: a fact or document is kept with enough reference,
concern, boundary, and continuation role to explain what it is for.

## Situatedness Failure Findings

The strongest failure evidence supports the prompt's pattern cautiously:

```text
knowledge survives
    while situatedness disappears
```

This does not mean knowledge is unimportant. It means knowledge alone does not
always preserve its current relation to work.

Recurring disappearance patterns:

- **Documents survive while pressure disappears.** A document can remain
  discoverable after the urgency, contradiction, or active concern that produced
  it has faded.
- **Facts survive while currentness disappears.** A fact can remain supported but
  no longer indicate whether it matters now.
- **Support survives while significance disappears.** A claim can retain support
  without retaining the reason it was selected for present work.
- **Lineage survives while active concern disappears.** Ancestry can explain
  origin without preserving the live edge.
- **Continuity artifacts survive while activation disappears.** A handoff can
  exist without being consumed as live continuation guidance.

The review does not prove that these are all the same failure. It does support
that they rhyme: each preserves an artifact, fact, support path, or historical
relation while losing a positioned relation needed for safe continuation.

## Active Edge Findings

Active Edge appears to function partly as situatedness preservation, pressure
preservation, currentness preservation, and selected-concern preservation, but
only partly.

Strong findings:

- It narrows from question inventory to the unresolved edge that currently
  matters.
- It can preserve active pressure after a broader lens decomposes.
- It helps prevent all known possible questions from becoming current work.
- It carries currentness: the edge is active because it remains live for a
  current or continuation concern.

Cautions:

- Active Edge is not a complete situatedness model.
- It should not absorb Current Work Position, continuity context, or inquiry
  lineage.
- It preserves a selected edge, not every reference point, constraint, or safe
  movement needed for continuation.

## Continuity Findings

Continuity documents preserve more than artifact survival. They often preserve
work position, orientation, current concern, active pressure history, and
situation history as resumption aids.

Strong findings:

- Continuity distinguishes resumption relevance from complete history.
- Working state preserves process position rather than repository state.
- Activity context preserves momentum: last completed step, live branch, open
  tension, immediate constraints, and next safe move.
- Handoff documents can preserve pressure transition, but only if consumed as
  active continuation rather than passive archive.

Caution: continuity is not the same as preservation. Preservation can keep an
artifact available; continuity requires enough relation, currentness, and
activation for work to remain recognizable and safely resumable.

## Knowledge Beyond Knowledge Findings

Repository work repeatedly preserves things that are not well-described as only
facts, claims, evidence, or knowledge. The following candidates survive review as
observational categories, not ontology:

- **Pressure:** what makes continuation, selection, explanation, or activation
  non-neutral.
- **Currentness:** why something matters now rather than merely being true or
  historical.
- **Selection:** why this material is active while other available material is
  not erased.
- **Concern:** what the work is currently about.
- **Reference relation:** relative to what a condition becomes significant.
- **Boundary and constraint:** what must not be crossed while continuing.
- **Safe move:** what next action appears locally safe without becoming a
  binding plan.
- **Active question:** which unresolved question is live rather than merely known.
- **Discovery path:** how a participant can recover why a finding was reached.
- **Orientation:** where attention and relevance point, when used cautiously as
  shorthand rather than an object.

The strongest finding is that repository work preserves **usable position** in
addition to knowledge. Usable position is not asserted as a system concept; it is
an observational way to name the non-factual residue that repeatedly matters.

## Critical Distinctions Reviewed

The following distinctions mostly survive review:

```text
knowledge != situatedness
fact != current concern
support != significance
preservation != continuation
continuity != artifact survival
current work != knowledge inventory
active edge != question inventory
answer available != correct work
```

The distinctions are strongest when used as guardrails against collapse. They
are weaker if treated as clean separations. In practice, the same sentence or
artifact can carry knowledge, support, currentness, pressure, and continuation
role at once. The important observation is not separability; it is that losing
one role can break continuation even when another role survives.

## Tensions

### Knowledge vs Situatedness

Knowledge can remain correct while no longer indicating why it matters now.
Situatedness-like preservation appears to keep knowledge related to a reference
point, current concern, active pressure, and continuation need.

### Preservation vs Continuation

Preservation keeps something available. Continuation requires that something be
available in a form that can be activated for resumption. Preserved artifacts can
increase burden if they obscure the active edge.

### Support vs Significance

Support explains why a claim can be held. Significance explains why the claim is
being used or selected now. Repository evidence repeatedly needs both.

### Availability vs Activation

Availability is necessary but not sufficient. Activation is the entry of
available material into working state such that it constrains the move.

### Orientation vs Inventory

Inventory lists possible relevant materials. Orientation indicates what those
materials are for in the current situation.

### Currentness vs History

History can explain origin, ancestry, and prior reasoning. Currentness explains
what remains live under the present concern.

### Pressure vs Fact

A fact may be a pressure source, but pressure appears only when a concern,
consequence, gap, contradiction, or continuation risk makes the fact non-neutral.

### Question vs Answer

An answer can be available while the live question has changed or the answer has
not been activated for the current question.

### Safe Continuation vs Stored Information

Stored information can support safe continuation, but safe continuation also
requires boundary awareness, selected concern, constraints, and next-move
readiness.

## Duplicate-Work Check

Prior documents already own substantial parts of this territory:

- `situatedness_and_pressure_observation.md` owns the broad observation that
  pressure and significance vary with reference point, current concern, and
  continuity concern.
- `pressure_source_observation.md` owns where pressures appear to come from.
- `pressure_visibility_and_preservation_observation.md` owns how pressure becomes
  visible and how pressure can be preserved or lost.
- `surviving_pressure_after_decomposition_observation.md` owns the pattern that
  pressures can survive decomposition of broad lenses.
- `current_work_position_frontier.md` owns frontier framing for current work
  position.
- `active_edge_frontier.md` owns Active Edge as a frontier.
- `continuity_frontier.md` and continuation reconciliations own continuity and
  working-state boundaries.
- `working_state_activation_observation.md` and
  `working_state_activation_failure_observation.md` own activation and activation
  failure.
- `preservation_surface_observation.md` and
  `preservation_failure_observation.md` own preservation surfaces and failure
  modes.
- `discovery_path_preservation_observation.md`,
  `documentation_lineage_observation.md`, and
  `lineage_distinction_observation.md` own path and lineage distinctions.

What this observation adds:

- It centers the preservation/failure question on **what Current Work Position
  preserves when it works** and **what disappears when it fails**.
- It compares Current Work Position, Active Edge, continuity, activation,
  pressure, and lineage as preservation participants without reconciling them.
- It makes explicit the repeated distinction between `same thing known` and
  `same thing mattering`.
- It gathers non-knowledge preservation candidates as an observation rather than
  promoting them into vocabulary or ontology.

What this observation should avoid duplicating:

- It should not redefine pressure, Active Edge, continuity, working state,
  reference point, concern subject, or preservation surfaces.
- It should not propose runtime fields for situatedness.
- It should not convert current concern, pressure, or continuity into governance,
  policy, identity, agency, or goals.
- It should not prescribe remediation for activation failure.

## Major Findings

1. Current Work Position appears successful when it preserves a positioned
   relation among reference point, current concern, continuity concern, active
   pressure, constraints, selected work, and next safe movement.
2. Failure appears less like absence of knowledge and more like loss of the
   relation that made knowledge governing.
3. Active Edge preserves the live unresolved edge, but not all situatedness.
4. Continuity preserves resumption relevance, not artifact survival alone.
5. Repository work preserves pressure, currentness, selection, concern,
   boundary, constraint, safe movement, discovery path, and activation state in
   addition to knowledge.
6. The strongest duplicate-work risk is redoing situatedness-and-pressure,
   pressure-preservation, Active Edge, continuity, and activation documents under
   a new name.
7. The strongest unresolved question is whether situatedness preservation is a
   single phenomenon or a family resemblance among currentness, activation,
   continuity, selection, pressure, and lineage.

## Unresolved Observations

- Whether Current Work Position preserves one relation or a bundle of separable
  relations remains unresolved.
- Whether active pressure can be preserved without preserving current concern
  remains unresolved.
- Whether currentness is best understood through activation, selection,
  continuity, or pressure remains unresolved.
- Whether situatedness disappearance is a distinct failure or a name for several
  preservation failures remains unresolved.
- Whether Active Edge is a preservation surface, a selection result, or a
  frontier marker varies by document and remains unresolved.
- Whether continuity can preserve situation history without becoming historical
  replay remains an ongoing tension.
- Whether a future participant can reliably recognize `same thing mattering`
  without explicit situatedness language remains unresolved.

## Closing Observation

The repository already knows many things, preserves many documents, and records
many lineages. The recurring failure is not simply forgetting. It is losing the
position from which preserved material mattered.

The recurring success is not total preservation. It is enough preserved relation
for a future participant to recognize:

```text
what this was about
why it mattered here
what pressure was live
what boundary constrained it
what question remained active
what movement was safe next
```

That is the situatedness-preservation pattern this observation can name without
turning it into ontology or implementation.
