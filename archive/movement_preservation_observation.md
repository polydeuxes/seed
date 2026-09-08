---
doc_type: observation
status: exploratory
domain: movement preservation observation
introduced_by: movement preservation observation
related:
  - interaction_temporalness_observation.md
  - participation_observation.md
  - interaction_as_evidence_observation.md
  - relation_of_use_observation.md
  - working_state_activation_observation.md
  - working_state_activation_failure_observation.md
  - selection_convergence_observation.md
  - non_selected_remainder_preservation_observation.md
  - current_work_position_frontier.md
  - active_edge_frontier.md
  - continuity_frontier.md
  - preservation_surface_observation.md
  - preservation_failure_observation.md
  - discovery_path_preservation_observation.md
  - documentation_lineage_observation.md
  - inquiry_frontier.md
---

# Movement Preservation Observation

## Purpose

This document observes whether repository evidence contains a recurring concern
about movement preservation.

It asks:

```text
What movement survives
when repository work remains continuable?
```

```text
What movement disappears
when repository work becomes difficult to resume?
```

```text
Does repository work preserve
states

or

transitions between states?
```

This is observation only. It is not a reconciliation, frontier, runtime proposal,
workflow proposal, planning proposal, event-model proposal, implementation
proposal, remediation plan, storage proposal, transcript proposal, authority
change, or roadmap. It does not propose event logs, transcript storage, workflow
systems, planning systems, or runtime changes.

Repository authority wins over this document. Existing reconciliations,
frontiers, observations, audits, maps, runtime-facing documents, tests, and
implementation files remain authoritative for their own scopes.

## Method And Review Boundary

Repository evidence was inspected directly. The requested documents were treated
as starting points, not as a closed corpus. Review also followed repository
maps, index entries, frontmatter cross-references, adjacent observation chains,
frontiers, preservation documents, handoff and continuation documents,
implementation-facing read-model surfaces by name, and tests surfaced by search.

Search terms used included:

```text
movement
transition
shift
displacement
activation
deactivation
selection shift
concern transition
attention shift
continuation
resumption
path
emergence
active edge
current work
why now
became active
stopped being active
replaced
abandoned
redirected
preserve state
preserved state
preserve movement
preserved movement
safe movement
safe move
working state
current concern
selection rationale
non-selected
inquiry movement
understanding transition
```

Documents and surfaces inspected included at least:

- `README.md`
- `docs/archive/original_book_of_seed/01-architecture.md`
- `docs/archive/original_book_of_seed/02-domain-model.md`
- `docs/archive/original_book_of_seed/06-context-engine.md`
- `docs/README.md`
- `docs/index.md`
- `docs/architectural_knowledge_map.md`
- `docs/interaction_temporalness_observation.md`
- `docs/participation_observation.md`
- `docs/interaction_as_evidence_observation.md`
- `docs/relation_of_use_observation.md`
- `docs/relation_of_use_decomposition_observation.md`
- `docs/relation_cluster_observation.md`
- `docs/working_state_activation_observation.md`
- `docs/working_state_activation_failure_observation.md`
- `docs/working_state_activation_artifact_audit.md`
- `docs/selection_convergence_observation.md`
- `docs/non_selected_remainder_preservation_observation.md`
- `docs/selection_and_attention_frontier.md`
- `docs/attention_trigger_frontier.md`
- `docs/attention_target_frontier.md`
- `docs/current_work_position_frontier.md`
- `docs/active_edge_frontier.md`
- `docs/continuity_frontier.md`
- `docs/persistence_frontier.md`
- `docs/preservation_surface_observation.md`
- `docs/preservation_failure_observation.md`
- `docs/discovery_path_preservation_observation.md`
- `docs/documentation_lineage_observation.md`
- `docs/lineage_distinction_observation.md`
- `docs/inquiry_frontier.md`
- `docs/handoff_and_continuation_lineage_frontier.md`
- `docs/handoff_consumption_activation_reconciliation.md`
- `docs/handoff_template_and_continuation_protocol_reconciliation.md`
- `docs/continuation_context_and_working_state_reconciliation.md`
- `docs/preservation_surface_observation.md`
- `docs/pressure_visibility_and_preservation_observation.md`
- `docs/situatedness_and_pressure_observation.md`
- `docs/situatedness_preservation_and_failure_observation.md`
- `docs/reference_point_and_concern_subject_observation.md`
- `docs/future_state_consequence_pressure_selection_observation.md`
- `docs/surviving_pressure_after_decomposition_observation.md`
- `docs/support_change_and_learning_observation.md`
- `docs/understanding_claim_and_decompression_observation.md`
- `docs/understanding_navigation_observation.md`
- `docs/operator_surface_family_observation.md`
- `docs/operator_understanding_surface_observation.md`
- `docs/object_role_operation_relation_cluster_observation.md`
- `docs/object_role_and_operation_frontier.md`
- `docs/event_and_change_reconciliation.md`
- `docs/temporal_reasoning_audit.md`
- `seed_runtime/source_navigation.py`
- `seed_runtime/knowledge/documentation_observation.py`
- `seed_runtime/knowledge/relationship_observation.py`
- `seed_runtime/action_plans.py`
- tests surfaced by search for lifecycle transition, source navigation,
  promotion readiness, action plans, and CLI projection behavior.

No runtime files were changed.

## High-Level Observation

The repository does not show one settled, common movement phenomenon. It does,
however, repeatedly exposes a preservation asymmetry:

```text
states, selected outcomes, and named artifacts survive strongly;
movement into, between, away from, or through those states survives unevenly.
```

The strongest evidence is negative. Continuation, handoff, activation,
interaction-temporalness, discovery-path, and preservation-failure work all
record cases where final content or a selected state can be found, while the
movement that made the content continuable is weak, scattered, implicit, or
missing.

The recurring shape is:

```text
selected concern survives
    but concern transition is harder to reconstruct

selected edge survives
    but edge displacement is harder to reconstruct

current work survives
    but path to current work is harder to reconstruct

final finding survives
    but discovery movement is harder to reconstruct

available knowledge survives
    but activation movement is harder to reconstruct
```

This does not prove that repository work should preserve movement as a new
object family. The safer observation is that movement appears as a recurring
continuation concern whenever later work must resume from more than a final
state.

## State Preservation Review

Repository state preservation is comparatively strong.

Examples of preserved state include:

- document artifacts and headings;
- frontmatter dependency and related-document fields;
- named document families such as reconciliation, frontier, observation, audit,
  vocabulary, characterization, and map;
- current architecture summaries and index entries;
- selected findings and final boundary statements;
- selected current concerns in Current Work Position, Active Edge, continuity,
  activation, and interaction observations;
- runtime-facing read-model rows and projected support facts in implementation
  surfaces;
- tests that encode accepted lifecycle or projection behavior.

These states often support later repository work because they answer:

```text
What exists?
What was selected?
What is the current document or finding?
What boundary currently holds?
What artifact should be read?
```

State preservation is weakest when a preserved state must be used as an active
continuation point. A participant may know the current finding without knowing
why it became current, what it displaced, whether adjacent alternatives were
rejected or merely unselected, or what next movement remains safe.

## Movement Preservation Review

Movement is preserved less consistently than state, but it is not absent.

Movement appears when documents retain one or more of these relations:

- why a concern became active;
- why an active concern stopped governing work;
- what selected one path over adjacent paths;
- what pressure moved attention from inventory to active work;
- what unresolved edge pulled work forward;
- what discovery path exposed a distinction;
- what compression was decomposed;
- what handoff or continuation boundary made a next move safe;
- what non-selected remainder remained available after selection;
- what earlier state was displaced, redirected, abandoned, or superseded;
- what changed in understanding, support, pressure, or relation of use.

The repository preserves this movement best when a document explicitly records
selection rationale, pressure, active edge, current work position, discovery
path, lineage, continuation constraint, or non-selected remainder. It preserves
movement poorly when it records only the final selected state.

## State Versus Movement

The reviewed evidence supports the distinction, but not as a clean binary.

```text
state
    !=
movement
```

A state is visible when the repository says what currently exists, what is
selected, what is active, what conclusion holds, what document owns a boundary,
or what artifact was produced.

Movement is visible when the repository says how that state came to be active,
what it displaced, what pressure carried it forward, what path led to it, what
transition made it usable, or what next movement it enables or constrains.

The distinction weakens in Current Work Position, Active Edge, continuity, and
working-state activation because those concepts often preserve mixed material: a
current state that is only useful because it contains movement pressure.

## Current Work Position Review

Current Work Position appears to preserve a mixture rather than only current
state or only selected movement.

It preserves current state when it names:

- the current question, gap, contradiction, frontier, selected tension, finding,
  validation state, authority boundary, or known non-goal;
- the current place where work is situated;
- the currently relevant subset of repository material.

It preserves selected movement when it names:

- why that position is current;
- what pressure makes the position continuable;
- what safe move follows from the position;
- what selection rationale narrowed many possible directions into this one;
- what would make continuation drift, restart, duplicate prior work, or overrun
  authority boundaries.

The evidence therefore suggests:

```text
Current Work Position primarily preserves current state for continuation,
but it becomes continuable only when some movement pressure is preserved with it.
```

A bare state such as "this is the current topic" is weaker than a position that
also preserves why the topic is current, what unresolved pressure it occupies,
and what movement remains safe.

## Active Edge Review

Active Edge also appears mixed.

It preserves unresolved state when it names:

- the live question;
- the selected gap;
- the unsettled frontier;
- the active contradiction;
- the unresolved boundary at which work currently sits.

It preserves movement pressure when it names:

- what is pulling work forward;
- what makes this unresolved state active rather than merely recorded;
- why this edge rather than adjacent edges receives continuation attention;
- what displacement occurred when another edge stopped being active;
- what next movement is safe or unsafe from this edge.

The evidence is stronger for Active Edge as a pressure-bearing state than as a
fully preserved transition history. Active Edge often records the live edge, but
not always the full movement by which the edge became live or displaced another
edge.

## Preservation Failure Review

Preservation failures frequently involve loss of knowledge, loss of movement, or
both. The reviewed evidence does not support choosing only one.

Knowledge loss appears when support, authority, claim boundaries, evidence,
interpretation caveats, or implementation facts are absent or too weak to reuse.

Movement loss appears when the repository retains a conclusion, artifact,
summary, or selected state but weakly preserves:

- activation into working state;
- transition from available to governing;
- selection shift from many candidates to one active path;
- concern transition from prior question to current question;
- attention shift from map or inventory to active edge;
- discovery path from assumption to pressure to distinction;
- displacement of one active edge by another;
- abandonment, redirection, or supersession of earlier movement;
- why a participant should resume here rather than restart.

The strongest preservation-failure pattern in the reviewed documents is not
simple knowledge disappearance. It is:

```text
knowledge remains findable
    but the movement needed to reactivate it is weak or absent
```

This means preservation failure can be epistemic, activation-related,
continuation-related, or mixed.

## Continuation Review

Continuation appears to require both preserved state and preserved movement,
although the required amount of movement varies.

Preserved state is needed because a participant must know:

- what artifact, claim, question, boundary, or current position exists;
- what authority applies;
- what constraints and non-goals govern the work;
- what has already been selected or rejected;
- what current state should not be re-litigated without cause.

Preserved movement is needed because a participant must also know:

- why this state matters now;
- how it became active;
- what it displaced or left non-selected;
- what unresolved pressure remains;
- what continuation path is safe;
- what would count as drift, duplicate work, stale activation, or restart.

The repository evidence therefore supports this cautious conclusion:

```text
inventory can often survive with preserved state alone;
continuation usually needs preserved state plus enough movement to resume.
```

## Critical Distinction Review

### Selection Versus Selection Shift

Selection is the retained outcome: a chosen concern, document, edge, finding, or
subset. Selection shift is the movement from one selected thing to another, or
from unselected possibility to selected active work.

Repository evidence preserves selection more strongly than selection shift. The
shift sometimes appears in lineage, activation, attention, or discovery-path
work, but is often reconstructed from adjacent documents rather than recorded as
such.

### Active Concern Versus Concern Transition

Active concern is the current subject governing work. Concern transition is how
that concern became active, replaced an earlier concern, or stopped governing.

Current-work and active-edge documents preserve active concerns. Interaction
temporalness, selection/attention, and discovery-path work preserve concern
transition more directly, but still unevenly.

### Current Work Versus Path To Current Work

Current work is usually findable through maps, status documents, frontiers,
observations, and recent documentation. The path to current work is more
scattered: it may require reconstructing lineage, dependencies, pressure
survivors, selection rationale, handoff material, and discovery-path examples.

### Preserved Outcome Versus Preserved Movement

Preserved outcomes are strong: final findings, selected boundaries, conclusion
sections, and named documents survive. Preserved movement is strongest when the
repository records discovery path, activation, pressure, selection rationale,
continuation constraint, or lineage. Where those are absent, the outcome may be
usable as inventory but weak as a continuation point.

### Knowledge Versus Emergence

Knowledge states what is represented or supported. Emergence names how a
distinction, pressure, finding, or active concern appeared from prior work.

The repository has many surfaces for represented knowledge and fewer stable
surfaces for emergence. Discovery-path and documentation-lineage documents make
emergence more visible, but they also show that emergence is often reconstructed
after the fact.

### Inventory Versus Continuation

Inventory answers what exists and where to look. Continuation answers how to
resume without restarting, drifting, duplicating work, or losing the live
pressure. Inventory can be sufficient for lookup. Continuation appears to need
selected state, active edge, current work position, constraints, pressure, and
safe movement.

## Movement Findings

1. Movement appears as a recurring repository concern, especially in documents
   about activation, participation, interaction temporalness, continuity,
   current work position, active edge, discovery path, preservation failure,
   selection, and handoff.
2. The repository preserves movement most explicitly through pressure,
   selection rationale, discovery paths, lineage chains, active-edge language,
   current-work-position language, continuation constraints, and non-selected
   remainder observations.
3. The repository preserves movement least explicitly where final outcomes are
   stated without the transition that made them active, displaced alternatives,
   or made them safe to continue.
4. Movement is often reconstructible, but reconstruction can require reading
   across many documents rather than consulting one authoritative surface.
5. Active Edge and Current Work Position are the strongest current concepts for
   preserving movement pressure, but neither fully preserves all transition
   history.
6. Continuity appears to depend on movement preservation when the task is
   resumption, but less so when the task is only inventory, citation, or lookup.

## Duplicate-Work Findings

Loss of movement creates duplicate-work risk in several reviewed patterns:

- a participant finds a conclusion but not the path that made it reliable, then
  repeats the investigation;
- a participant sees a frontier but not why it became active, then treats a
  deferred or stale concern as current;
- a participant sees the current state but not the displaced alternatives, then
  reopens already narrowed paths;
- a participant sees preserved knowledge but not relation of use, then uses it as
  inert background or over-applies it outside its active scope;
- a participant sees an active edge but not the safe movement boundary, then
  drifts into implementation, planning, workflow, or remediation when the
  repository evidence only supports observation.

## Major Findings

1. Repository work preserves states more strongly than transitions between
   states.
2. Continuable repository work usually preserves at least some movement: active
   pressure, selection rationale, safe move, lineage, discovery path, or
   activation relation.
3. Difficult resumption often corresponds to missing movement rather than total
   missing knowledge.
4. Current Work Position appears to preserve current state plus selected
   movement pressure.
5. Active Edge appears to preserve an unresolved state plus the pressure that
   makes it active.
6. Preservation failure is frequently mixed: knowledge may survive while
   activation, selection shift, concern transition, or discovery movement
   disappears.
7. The evidence is strongest for movement as a continuation concern, weaker for
   movement as a separate ontology, and insufficient for any implementation or
   runtime conclusion.

## Evidence Strength

Strong evidence:

- repeated negative findings that preserved content can still fail to support
  continuation;
- handoff and continuation documents distinguishing information preservation
  from activated continuation;
- Current Work Position and Active Edge frontiers preserving selected live
  pressure rather than flat inventory;
- discovery-path work showing final findings survive more strongly than the
  challenge sequences that produced them;
- preservation-failure work naming cases where artifacts survive but orientation
  or activation does not.

Moderate evidence:

- selection and attention documents showing movement from many possibilities to
  active attention;
- participation and relation-of-use observations showing available knowledge can
  become governing or inert depending on current use;
- situatedness and pressure documents showing the same information can matter
  differently under different current concerns;
- non-selected remainder work showing what is left behind by selection may need
  preservation to avoid overclaiming or duplicate inquiry.

Weak evidence:

- exact frequency of movement-loss versus knowledge-loss failures;
- whether movement should be represented as object, relation, operation, role,
  lineage, pressure, or document pattern;
- whether every successful continuation requires explicit transition history;
- whether movement preservation has a stable boundary separate from activation,
  selection, continuity, and inquiry lineage.

## Unresolved Observations

- The repository has not settled whether movement is an object, relation,
  operation, role, lineage, pressure, or only an observational lens.
- It remains unclear how much movement must survive for continuation to be safe.
- It remains unclear when preserving movement becomes excess historical detail
  rather than continuation-critical orientation.
- It remains unclear whether movement-loss failures are more common than
  knowledge-loss failures, because many cases are mixed.
- It remains unclear whether Current Work Position and Active Edge should remain
  separate pressure surfaces or are overlapping descriptions of the same
  continuation need.
- It remains unclear whether discovery movement, activation movement, selection
  movement, and handoff movement share enough structure to support a future
  reconciliation.
- It remains unclear how older pre-frontmatter or pre-lineage repository work
  would change this observation, because recent documents make movement more
  visible than older surfaces.

## Boundary Restatement

This document observes movement preservation pressure only. It does not propose
new storage, logs, transcripts, workflows, planning systems, runtime behavior,
schemas, remediation, or implementation work. The observed pattern may remain an
exploratory lens unless future repository authority reconciles it differently.
