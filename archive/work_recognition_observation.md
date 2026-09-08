---
title: Work Recognition Observation
status: observation
authority: observational, not canonical or reconciliatory
created: 2026-06-16
scope: documentation-only repository observation
---

# Work Recognition Observation

## Purpose

This document observes how repository work appears to become recognizable as a
particular kind of work.

It asks:

```text
How does repository work determine what work is being performed?
```

and:

```text
What evidence causes work to be treated as lookup, inventory, observation,
audit, reconciliation, continuation, frontier exploration, or something else?
```

This is observation only. It is not a reconciliation, frontier, work-shape
ontology, intent system, classification proposal, runtime proposal,
implementation proposal, operator model, schema proposal, or remediation plan.
It does not assume that Seed needs a work-recognition mechanism.

## Method And Authority Boundary

Repository evidence was treated as authority. Reconciliations were treated as
boundary records for their own scope. Frontiers were treated as unsettled inquiry
surfaces. Observations, audits, maps, indexes, tests, and implementation-facing
read models were used as evidence of how work is described, routed, resumed,
queried, or reconstructed today.

The review started with the required documents and then searched broadly through
repository maps, indexes, adjacent documents, state-summary surfaces, operator
surfaces, source-navigation surfaces, handoff and continuation documents,
context surfaces, tests, and implementation-facing read models.

No runtime changes were made or proposed.

## Documents Inspected

Required starting documents inspected:

- `docs/work_shape_and_orientation_observation.md`
- `docs/orientation_bundle_load_bearing_observation.md`
- `docs/situation_observation.md`
- `docs/purpose_and_concern_observation.md`
- `docs/current_work_position_frontier.md`
- `docs/active_edge_frontier.md`
- `docs/continuity_frontier.md`
- `docs/operator_understanding_surface_observation.md`
- `docs/operator_navigation_reconciliation.md`
- `docs/active_context_and_working_set_reconciliation.md`
- `docs/continuation_context_and_working_state_reconciliation.md`

Additional documents and surfaces inspected through maps, indexes,
cross-reference, adjacency, broad search, and implementation-facing review:

- `README.md`
- `docs/archive/original_book_of_seed/01-architecture.md`
- `docs/archive/original_book_of_seed/03-runtime-loop.md`
- `docs/archive/original_book_of_seed/06-context-engine.md`
- `docs/archive/original_book_of_seed/09-pseudocode.md`
- `docs/archive/original_book_of_seed/13-knowledge-and-evidence.md`
- `docs/README.md`
- `docs/index.md`
- `docs/architectural_knowledge_map.md`
- `docs/attention_target_frontier.md`
- `docs/attention_trigger_frontier.md`
- `docs/bounty_board_and_investigation_selection_observation.md`
- `docs/context_composition_reconciliation.md`
- `docs/context_composition_vocabulary.md`
- `docs/current_concern_observation.md`
- `docs/derived_consequence_and_relevance_observation.md`
- `docs/discovery_path_preservation_observation.md`
- `docs/documentation_authority_reconciliation.md`
- `docs/documentation_lifecycle_reconciliation.md`
- `docs/documentation_lineage_observation.md`
- `docs/finding_applicability_index.md`
- `docs/future_frontiers.md`
- `docs/future_state_consequence_pressure_selection_observation.md`
- `docs/handoff_and_continuation_lineage_frontier.md`
- `docs/handoff_bootstrap_and_summary_reconciliation.md`
- `docs/handoff_consumption_activation_reconciliation.md`
- `docs/handoff_document_boundary_reconciliation.md`
- `docs/handoff_pressure_transition_observation.md`
- `docs/handoff_template_and_continuation_protocol_reconciliation.md`
- `docs/inquiry_frontier.md`
- `docs/knowledge_acquisition_and_selection.md`
- `docs/knowledge_navigation_layers_frontier.md`
- `docs/knowledge_representation_map.md`
- `docs/navigation_hygiene_audit.md`
- `docs/non_selected_remainder_preservation_observation.md`
- `docs/operator_surface_activation_against_knowledge_and_understanding_audit.md`
- `docs/orientation_non_convergence_audit.md`
- `docs/orientation_object_observation.md`
- `docs/preservation_failure_observation.md`
- `docs/preservation_surface_observation.md`
- `docs/pressure_source_observation.md`
- `docs/pressure_visibility_and_preservation_observation.md`
- `docs/recommendation_selection_boundary.md`
- `docs/reference_point_and_concern_subject_observation.md`
- `docs/selection_and_attention_frontier.md`
- `docs/selection_convergence_observation.md`
- `docs/selection_rationale_characterization.md`
- `docs/selection_rationale_reconciliation.md`
- `docs/source_navigation_surface_reconciliation.md`
- `docs/source_navigation_without_grep_audit.md`
- `docs/state_summary_authority_reconciliation.md`
- `docs/state_summary_cli_boundary_audit.md`
- `docs/state_summary_endpoint_prominence_audit.md`
- `docs/state_summary_performance_inquiry_lineage_report.md`
- `docs/understanding_navigation_observation.md`
- `docs/understanding_visibility_existing_surface_audit.md`
- `docs/working_state_activation_observation.md`
- `docs/working_state_activation_artifact_audit.md`
- `docs/working_state_activation_failure_observation.md`
- `seed_runtime/context_views.py`
- `seed_runtime/input_inspector.py`
- `seed_runtime/source_navigation.py`
- `seed_runtime/state_summary_views.py`
- `seed_runtime/state_views.py`
- `tests/test_context.py`
- `tests/test_context_views.py`
- `tests/test_input_inspector.py`
- `tests/test_source_navigation.py`
- `tests/test_state_summary_views.py`

## Search Terms Used

Broad repository searches used these terms and close variants:

```text
current work
work
work shape
activity
question
request
investigation
audit
observation
frontier
reconciliation
navigation
lookup
inventory
continuation
handoff
selection
recommendation
state summary
operator
understanding
context
working state
current concern
active edge
orientation
pressure
reference point
boundary
activation
reconstruction
safe continuation
next safe move
source navigation
input act
operator query
command request
user observation
```

## High-Level Finding

Repository work appears to recognize what is being performed through a mixture of
explicit artifact labels, declared purpose, authority boundary, requested
output, evidence route, active pressure, continuation posture, and later
reconstruction. The repository does not appear to contain one canonical
work-shape classifier. Recognition is often local and document-bound:

```text
artifact label + purpose + boundary + evidence route + current pressure
    -> participants infer what kind of work is occurring
```

The evidence is strongest where documents explicitly declare their type and
non-type. Observation documents repeatedly say they are not reconciliations,
frontiers, workflows, schemas, runtime proposals, or remediation plans. Audit
documents usually identify a surface or boundary under review. Reconciliations
establish authority boundaries. Frontiers preserve unsettled inquiry.
Continuation and handoff documents preserve what must survive for later work.

The evidence is weaker where the same information can support multiple uses. A
state summary, source-navigation fact, map entry, finding, or handoff reference
can serve lookup, inventory, investigation, continuation, recommendation, or
audit depending on the current question, pressure, selected boundary, and next
move. In those cases, the repository often reconstructs the work after the fact
from surrounding context rather than naming the work shape directly.

## How Work Becomes Recognizable

### 1. Explicit document kind is the strongest local signal

Many repository documents announce their own kind in title, front matter,
purpose, or repeated boundary statements. Names ending in `_observation`,
`_audit`, `_reconciliation`, and `_frontier` are not merely labels; they usually
come with method and authority differences.

Observed pattern:

```text
observation -> preserve what evidence appears to show without settling authority
audit -> check a bounded surface against evidence or expectation
reconciliation -> preserve boundary, ownership, or authority relationships
frontier -> keep an unresolved edge available without resolving it
```

This is explicit recognition, but only at the artifact level. It does not prove a
canonical work-shape taxonomy for all repository work.

### 2. Purpose and non-purpose statements narrow the work

Recent documents repeatedly identify what they are not. This negative boundary
is a recognition cue. A document may say it is not a runtime proposal, not a
schema proposal, not a workflow, not an operator model, not a reconciliation, or
not a frontier. Those exclusions help later participants treat the artifact as
observation, critique, audit, or preservation rather than implementation or
architecture.

This evidence supports the distinction:

```text
question != work shape
```

The same question can appear in an observation, frontier, audit, or
reconciliation depending on whether the document is preserving evidence,
checking a surface, holding an open edge, or settling a boundary.

### 3. Evidence route changes the apparent work

Repository work is recognized partly by what kind of evidence it follows:

- broad repository search and adjacency review often signal investigation or
  observation;
- maps, indexes, and cross-references support navigation and inventory;
- implementation-facing read models and tests support audit or reconciliation
  against runtime surfaces;
- handoff artifacts and current-position documents support continuation;
- unresolved questions, tensions, and candidate distinctions support frontier
  exploration;
- ranked or selected candidates support selection and recommendation surfaces.

This supports the distinction:

```text
information != use of information
```

The same source fact can be evidence in an audit, a lookup target in navigation,
a context clue for continuation, or support for a recommendation boundary.

### 4. Current pressure and selected concern make available material become work

Current concern, pressure, active edge, and selection documents suggest that
available material becomes recognizable work when it is tied to why this matter
is current, what remains unresolved, and what movement is safe next. Without
those cues, a participant may know what exists but not what kind of work is
underway.

This is implicit recognition. It does not require naming a work shape, but it
lets participants distinguish inventory from investigation, continuation from
lookup, and frontier exploration from implementation support.

### 5. Continuation posture makes work recognizable across time

Continuation and handoff documents show that later participants need more than
facts, references, and status. They need the immediate objective, attention
object, live reasoning branch, blockers, active tensions, relevant constraints,
short-lived assumptions, and next intended step. Those elements make it possible
to recognize what was being worked on after interruption.

This evidence supports the distinction:

```text
state summary != continuation support
```

State summaries can expose important state, but continuation requires cues about
which state was active for the work.

### 6. Reconstruction appears when recognition cues are missing

Preservation-failure, discovery-path, activation, source-navigation, and
pressure-visibility documents repeatedly show a failure shape:

```text
facts or documents survive
    while current concern, discovery path, selected boundary, or active edge
    must be reconstructed
```

In these cases, work recognition is neither fully explicit nor fully absent. It
is reconstructed from remaining traces: filenames, document type, cited sources,
search terms, findings, unresolved observations, next safe moves, handoff notes,
and authority boundaries.

## State Summary Review

The original State Summary pressure appears less like a single work type and
more like several possible works sharing one surface.

Possible readings supported by repository evidence:

1. **Inventory:** State summary exposes counts, issues, top entities, current
   facts, contradictions, support, or stale-fact cues. In this reading, the work
   is to see what exists or what is prominent.
2. **Operator lookup:** State summary helps an operator answer what is known,
   what matters, or where to drill down next.
3. **Audit:** State summary audits ask whether CLI or endpoint prominence,
   authority, performance, or implementation surfaces match the documented
   boundary.
4. **Investigation:** Performance and prominence lineage documents use state
   summary as evidence in a longer inquiry about pressure, selection, and
   visibility.
5. **Continuation support candidate:** Later pressure and activation documents
   test whether summary content preserves enough currentness to resume work.

The supporting evidence is that state-summary surfaces preserve compressed state
and prominence, while adjacent documents repeatedly warn that prominence alone
may not preserve why a row matters now, which question it answers, or what work
it was supporting. The operator may have been performing inventory, lookup,
audit, investigation, or continuation-oriented diagnosis. The repository does
not force a single answer.

## Operator Request Review

Repository cases where the same information supports different work are common.
The change is usually not the information itself but the relation of use.

Examples observed:

- A source-navigation record can support lookup when the participant asks where
  a behavior lives, audit when checking whether navigation is queryable without
  grep, investigation when studying navigation failure, and continuation when it
  preserves the route needed for later work.
- A state-summary row can support inventory when listing known state, operator
  understanding when explaining why a fact matters, audit when checking endpoint
  or CLI prominence, and continuation when paired with active concern and next
  move.
- A handoff reference can support continuation when consumed with active
  tensions and constraints, or become mere inventory when the consuming
  participant cannot tell what was live.
- A finding can support recommendation when used to choose among candidates,
  reconciliation when used to settle a boundary, or observation when used only to
  record a pattern.

What changes is the active question, selected boundary, pressure, expected
output, authority posture, and next move. The repository therefore recognizes
work partly through context, not only through content.

## Current Work Position Review

Current Work Position appears to function partly as work-recognition support,
though not as a work-shape classifier. It preserves where current work is
situated among available documents, findings, constraints, tensions, and next
moves. That helps later participants distinguish:

```text
available repository knowledge
    != the work currently being carried forward
```

The evidence is strongest in continuation and pressure documents where many
facts or frontiers exist but only some explain the current position. The evidence
is weaker if Current Work Position is read as a general ontology object; the
frontier status preserves that it is unsettled.

Observed role:

```text
Current Work Position helps recognize currentness and continuation posture.
It does not, by itself, name lookup, audit, reconciliation, or frontier work.
```

## Active Edge Review

Active Edge appears to influence what work is recognizable by exposing what is
currently pulling work forward. It is strongest when distinguishing an active
unresolved tension from a preserved but inactive concern.

However, Active Edge does not appear equivalent to recognized work. It can say
what unresolved thing remains active without deciding whether the work around it
is observation, audit, continuation, or frontier exploration. The repository also
notes duplicate-work risk around pressure, selection, attention, priority,
inquiry, and current work position.

Observed role:

```text
Active Edge helps preserve the pull of work.
It does not by itself define the work being performed.
```

## Context Review

Context surfaces preserve clues about work without always naming work shape.
Implementation-facing context, context-selection, context-view, model-client,
and prompt surfaces expose operator input, relevant state, decision schema,
allowed decision kinds, facts, open questions, goals, recent events, and
selected context. Documentation around context composition and active context
adds boundary and working-set distinctions.

These surfaces can make work recognizable by preserving:

- the operator query or command-like request;
- the selected goal, question, or open issue;
- relevant state and recent events;
- constraints and decision boundaries;
- current working set rather than total repository inventory.

The recognition is mostly implicit. Context can preserve evidence from which a
participant infers lookup, investigation, continuation, or recommendation, but
context is not itself recognized work.

## Reconstruction Review

Repository evidence repeatedly shows reconstruction after facts, summaries,
findings, or handoffs survive without enough orientation.

Missing evidence usually includes one or more of:

- why this item was current rather than merely available;
- which boundary or authority governed the work;
- what question was being answered;
- what active tension or contradiction was pulling the work;
- what had been tried and ruled out;
- what distinction had just appeared;
- what next move was safe;
- what use the same information was meant to serve.

Discovery-path documents add that final findings often survive better than the
challenge sequence that changed understanding. Working-state activation documents
add that participants can find and read the correct document while still failing
to activate the right constraints, pressure, and current path. Handoff documents
add that references alone do not prove continuation alignment.

## Work-Recognition Findings

- Work recognition is explicit at artifact boundaries more often than at runtime
  or repository-wide category boundaries.
- The repository recognizes many works through declared purpose, method,
  authority posture, and exclusions rather than through a single list of
  categories.
- Current concern, pressure, active edge, selected boundary, and next safe move
  are strong clues for recognizing work in progress.
- State-summary, source-navigation, context, map, and read-model surfaces expose
  information that can support several different works.
- Continuation work requires more recognition evidence than lookup or inventory;
  it needs currentness, active tension, constraints, and next movement.
- Frontier exploration is recognized less by topic and more by unresolvedness,
  non-resolution, and preservation of candidate distinctions.
- Audit is recognized by checked surface plus boundary or expectation, not by
  broad search alone.
- Reconciliation is recognized by boundary-setting and authority preservation,
  not merely by comparing documents.

## Duplicate-Work Findings

This observation overlaps with several existing surfaces and therefore preserves
only the recognition question.

- `docs/work_shape_and_orientation_observation.md` owns the broader observation
  that different work shapes may require different orientation structures.
- `docs/orientation_bundle_load_bearing_observation.md` owns the load-bearing
  status of recurring orientation elements.
- `docs/situation_observation.md` owns the question of whether repository work
  preserves something resembling a situation.
- `docs/current_work_position_frontier.md` owns unsettled inquiry around current
  position.
- `docs/active_edge_frontier.md` owns unsettled inquiry around what pulls work
  forward.
- `docs/continuation_context_and_working_state_reconciliation.md` owns
  continuation working-state boundaries.
- `docs/active_context_and_working_set_reconciliation.md` owns active-context
  and working-set boundaries.
- `docs/operator_navigation_reconciliation.md` and operator-understanding
  surfaces own operator-facing navigation and comprehension concerns.
- State-summary audits and authority documents own the state-summary boundary.
- Source-navigation reconciliation and audits own source-navigation boundaries.

The duplicate-work risk is that work recognition could accidentally become a
work-shape ontology, intent classifier, operator model, or orientation mechanism.
Repository evidence does not require that move.

## Critical Distinctions Observed

The requested distinctions mostly survive review, with caveats:

```text
work recognition != work classification
```

Recognition appears local, evidentiary, and sometimes reconstructed.
Classification would require a stable category system that this review did not
find as repository authority.

```text
question != work shape
```

The same question can be handled as observation, audit, reconciliation,
frontier, lookup, or continuation depending on authority posture and expected
output.

```text
information != use of information
```

This is strongly supported. The same information repeatedly supports inventory,
lookup, investigation, continuation, recommendation, or audit.

```text
state summary != continuation support
```

Supported with caveat. State summary can contribute to continuation when paired
with current concern, active edge, constraints, and next move, but it is not
sufficient by itself.

```text
current concern != recognized work
active edge != recognized work
context != recognized work
```

Supported. Each can make work recognizable without being identical to the work.

```text
recognition != execution
```

Supported. Documentation and read-model surfaces can make work recognizable
without proposing or executing runtime behavior.

## Major Findings

1. The repository has many explicit local labels for work artifacts, but no
   observed canonical work-recognition system.
2. Work becomes recognizable through combined cues: artifact kind, stated
   purpose, non-purpose exclusions, evidence route, authority boundary, current
   pressure, selected concern, continuation posture, and expected output.
3. The same information often supports different work. The differentiator is
   relation of use, not content alone.
4. State Summary pressure appears to have involved inventory, lookup, audit,
   operator-understanding, investigation, and possible continuation-support
   readings. Repository evidence does not collapse it to one work.
5. Current Work Position and Active Edge are strong recognition supports for
   currentness and pull, but neither is identical to recognized work.
6. Context surfaces preserve implicit recognition clues without necessarily
   naming work shape.
7. Reconstruction becomes necessary when preserved artifacts omit current
   concern, authority boundary, discovery path, active tension, or next safe
   movement.

## Unresolved Observations

- The repository has not settled whether work shapes are stable categories,
  recurring artifact families, participant inferences, or retrospective labels.
- It remains unclear how much recognition happens before work begins versus
  after a document is written and labeled.
- It remains unclear whether operator requests carry enough evidence to
  distinguish lookup, investigation, continuation, recommendation, and audit
  before repository evidence is inspected.
- It remains unclear whether context surfaces should be read as recognition
  surfaces or only as material from which recognition is reconstructed.
- It remains unclear how often State Summary is used for inventory versus
  operator understanding versus continuation diagnosis.
- It remains unclear whether Active Edge changes recognized work or only marks
  which unresolved pressure is live inside whatever work is occurring.
- It remains unclear whether Current Work Position is a continuation surface, a
  recognition support, both, or neither outside the cases reviewed here.

## Closing Observation

Repository work appears recognizable today through evidence relations rather
than through a single classification mechanism. Labels, purposes, boundaries,
search paths, selected concerns, active edges, context, state summaries,
handoffs, and source-navigation traces all participate. The strongest pattern is
not that the repository already knows a fixed list of work shapes, but that later
participants can usually infer the work from the preserved relation among
information, use, authority, pressure, and continuation posture. Where that
relation is missing, participants reconstruct what was being worked on from
weaker traces.
