---
doc_type: observation
status: exploratory
domain: interaction temporalness observation
introduced_by: interaction temporalness observation
related:
  - participation_observation.md
  - interaction_as_evidence_observation.md
  - relation_of_use_observation.md
  - working_state_activation_observation.md
  - working_state_activation_failure_observation.md
  - selection_convergence_observation.md
  - non_selected_remainder_preservation_observation.md
  - continuity_frontier.md
  - discovery_path_preservation_observation.md
  - documentation_lineage_observation.md
  - inquiry_frontier.md
  - handoff_consumption_activation_reconciliation.md
  - continuation_context_and_working_state_reconciliation.md
  - current_work_position_frontier.md
  - active_edge_frontier.md
---

# Interaction Temporalness Observation

## Purpose

This document observes whether repository evidence contains a distinct form of
temporalness associated with interaction itself.

It asks:

```text
Can interaction itself possess temporal structure?
```

```text
What appears lost when only final outcomes survive?
```

```text
Does repository work preserve evidence of interrupted, abandoned, redirected,
or partially completed interaction paths?
```

This is observation only. It is not a reconciliation, frontier, implementation
proposal, runtime proposal, event-model proposal, storage proposal, remediation
proposal, conversation-system proposal, voice-system proposal, schema proposal,
or authority change. Repository authority remains with the documents, maps,
frontiers, reconciliations, audits, tests, and runtime-facing surfaces that own
their own scopes.

## Method And Authority Boundary

Repository evidence was inspected directly. The requested documents were treated
as starting points, not as a closed corpus. Review also used repository maps,
indexes, cross-references, adjacent observations, runtime-facing read-model
surfaces, tests by name where surfaced by search, architectural root documents,
and broad `rg` searches.

Search terms used included:

```text
time
temporal
sequence
interaction
conversation
turn
abandon
interruption
pause
continuation
selection shift
attention shift
current concern
active concern
candidate concern
inquiry
discovery path
working state
activation
redirect
resume
episode
utterance
request
current work
active edge
selection rationale
non-selected
rejected path
candidate interpretation
candidate request
candidate inquiry
candidate work
```

Documents and surfaces inspected included at least:

- `README.md`
- `docs/archive/original_book_of_seed/01-architecture.md`
- `docs/archive/original_book_of_seed/02-domain-model.md`
- `docs/archive/original_book_of_seed/06-context-engine.md`
- `docs/README.md`
- `docs/index.md`
- `docs/architectural_knowledge_map.md`
- `docs/participation_observation.md`
- `docs/interaction_as_evidence_observation.md`
- `docs/relation_of_use_observation.md`
- `docs/relation_of_use_decomposition_observation.md`
- `docs/relation_cluster_observation.md`
- `docs/working_state_activation_observation.md`
- `docs/working_state_activation_failure_observation.md`
- `docs/selection_convergence_observation.md`
- `docs/non_selected_remainder_preservation_observation.md`
- `docs/continuity_frontier.md`
- `docs/persistence_frontier.md`
- `docs/discovery_path_preservation_observation.md`
- `docs/documentation_lineage_observation.md`
- `docs/lineage_distinction_observation.md`
- `docs/inquiry_frontier.md`
- `docs/handoff_and_continuation_lineage_frontier.md`
- `docs/handoff_consumption_activation_reconciliation.md`
- `docs/continuation_context_and_working_state_reconciliation.md`
- `docs/current_work_position_frontier.md`
- `docs/active_edge_frontier.md`
- `docs/selection_and_attention_frontier.md`
- `docs/attention_trigger_frontier.md`
- `docs/attention_target_frontier.md`
- `docs/reference_point_and_concern_subject_observation.md`
- `docs/future_state_consequence_pressure_selection_observation.md`
- `docs/preservation_surface_observation.md`
- `docs/preservation_failure_observation.md`
- `docs/pressure_visibility_and_preservation_observation.md`
- `docs/situatedness_and_pressure_observation.md`
- `docs/situatedness_preservation_and_failure_observation.md`
- `docs/object_role_and_operation_frontier.md`
- `docs/object_role_operation_relation_cluster_observation.md`
- `docs/input_act_vocabulary.md`
- `docs/input_envelope_vocabulary.md`
- `docs/natural_language_observation_and_intent_derivation_reconciliation.md`
- `docs/operator_intent_question_and_claim_interface_reconciliation.md`
- `docs/interpretation_candidate_preservation_audit.md`
- `docs/event_and_change_reconciliation.md`
- `docs/occurrence_time_and_temporal_claim_reconciliation.md`
- `docs/observation_refresh_and_knowledge_freshness_reconciliation.md`
- `docs/time_provenance_and_temporal_authority_audit.md`
- `docs/cross_seed_provenance_and_federation_reconciliation.md`
- `docs/state_summary_authority_reconciliation.md`
- `docs/state_summary_performance_inquiry_lineage_report.md`
- `docs/runtime_reassessment.md`
- `docs/runtime_loop_thin_runtime_plan.md`
- `seed_runtime/candidate_requests.py`
- `seed_runtime/runtime_trace.py`
- `seed_runtime/events.py`
- tests surfaced by search, including candidate request, action resume, temporal
  characterization, event, runtime trace, context selection, and evaluation
  tests.

No runtime files were changed.

## High-Level Observation

Repository evidence weakly but repeatedly supports an interaction-specific
form of temporalness. The evidence is not strong enough to establish a new
canonical type, but it is strong enough to preserve the distinction as an
observation:

```text
knowledge temporalness asks when a claim, observation, fact, event, projection,
or support relation holds, was observed, was imported, expires, or remains fresh.

interaction temporalness asks how work moved through attention, activation,
selection, abandonment, redirection, continuation, and uptake during an episode.
```

The strongest evidence is negative. Multiple documents observe that final
content can survive while the path that made the content usable disappears.
When that happens, later participants may know the answer, final selected edge,
or current document, but lose why that was the live concern, which alternatives
were displaced, what had been tried, what was interrupted, and what movement was
safe next.

## Temporalness Review

### Knowledge temporalness is already explicit

Repository temporal work has strong existing vocabulary for knowledge-bearing
objects and projections:

- observation time;
- claim time;
- fact time;
- event time;
- reported time;
- import time;
- projection time;
- expiration;
- freshness;
- recency;
- current-sample semantics;
- temporal scope of claims;
- event sequence and state interval.

That vocabulary is primarily about whether a proposition, measurement, event,
state, or projection is temporally qualified. It asks whether knowledge remains
valid, current, stale, contradicted, superseded, or historically scoped.

### Interaction temporalness appears different, but not independent

The interaction-facing documents introduce a different set of temporal concerns:

- what became active;
- what stopped being active;
- what was selected from alternatives;
- what remained non-selected;
- what was activated into working state;
- what failed to activate;
- what was handed off but not consumed;
- what moved from available knowledge to governing knowledge;
- what concern pulled work forward;
- what safe move followed;
- what discovery path led to a result;
- what candidate interpretation, request, inquiry, concern, or edge was preserved
  before routing or selection.

These concerns are temporal because they describe before/after, movement,
sequence, replacement, continuation, interruption, or resumption. They are not
only temporal facts about the world. They are temporal facts about the work of
participating with evidence.

The distinction does not fully separate. Interaction temporalness often depends
on knowledge temporalness: a stale claim may redirect attention; an observation
time may determine whether continuation is safe; an event sequence may become the
subject of inquiry. But the reverse is not guaranteed. Knowing the observation
time of a fact does not by itself preserve how that fact became active in work.

## Abandoned Path Review

Repository evidence does preserve abandoned, partial, or non-selected paths in
some places, but unevenly.

Stronger preservation appears where documents explicitly discuss:

- non-selected remainders;
- candidate interpretations;
- candidate requests;
- selection rationale;
- rejected routes;
- discovery-path preservation;
- preservation failure;
- handoff activation failure;
- working-state activation failure;
- current-work and active-edge boundaries;
- future-frontier and open-question inventories.

The evidence suggests that abandoned paths matter when losing them creates
repeat work, false convergence, unexplained selection, or unsafe continuation.
For example, preservation-failure and discovery-path work observe that a final
conclusion can survive more strongly than the route that made it credible.
Candidate-request surfaces preserve possible requests before routing, and
interpretation-candidate work preserves ambiguity before promotion. Those are
interaction-temporal because they retain a path before it becomes a final routed
or selected result.

Weaker preservation appears where documents only retain a final answer, current
summary, promoted claim, selected concern, or current projection. In those cases,
the repository may show what survived without showing what was started and then
abandoned.

## Selection Shift Review

Repository evidence distinguishes selection from selection shift only
partially.

Selection itself is well represented. The repository often records that a
concern, edge, finding, source, recommendation, or document was selected for a
view, handoff, continuation, or explanation.

Selection shift is less consistently preserved. Some documents explicitly care
about why one route displaced another: non-selected remainder preservation,
selection convergence, discovery-path preservation, attention trigger/target,
current-work-position, active-edge, and preservation-failure documents all
observe that omitted alternatives can matter. However, many final artifacts do
not preserve:

```text
A was active
then B replaced A
```

They more often preserve:

```text
B is current
```

or:

```text
B was selected
```

The strongest interaction-temporal finding is that these are not equivalent. If
only `B` survives, future participants may repeat `A`, assume `A` was never
considered, or miss the pressure that caused the shift.

## Current Work Position Review

Current Work Position appears to preserve more than current state, but less than
full emergence history.

The current-work-position frontier asks what position current work occupies and
what must survive for work to feel continuous. Its candidate components include
active question, active gap, active contradiction, active frontier, selected
tension, selected finding, selection rationale, authority boundary, validation
state, next safe move, inquiry direction, active relationship, and active
concern.

That list is not merely a snapshot. Selection rationale, validation state,
inquiry direction, and next safe move all point to how the current state can be
continued from prior movement. Still, the frontier does not require a full
transcript or full chronological path. It curates emergence only where emergence
is needed for safe continuation.

Observed boundary:

```text
Current Work Position preserves selected emergence pressure,
not full interaction history.
```

## Active Edge Review

Active Edge appears to preserve the currently pulling unresolved edge more than
it preserves all competing or previously active edges.

The active-edge frontier repeatedly distinguishes preserved concerns from
currently pulling concerns. It asks why one question, gap, contradiction,
frontier, relationship, or tension becomes the current focus of work. That is an
interaction-temporal question because the active edge can change while the
underlying concern persists.

Evidence for competing or abandoned edges is present mostly through adjacent
selection and preservation documents, not as a complete active-edge history.
Active Edge can imply that other preserved concerns are inactive, but it does
not by itself preserve a full sequence of prior edges unless selection rationale,
rejected paths, non-selected remainders, or handoff context are also retained.

Observed boundary:

```text
Active Edge preserves current pull.
Adjacent selection and preservation documents are needed to preserve edge shift.
```

## Interaction Episode Review

Repository evidence supports a cautious distinction among several interaction
units, but none appears fully reconciled as a canonical episode type.

Observed distinctions:

| Unit | Evidence observed | Boundary |
| --- | --- | --- |
| Utterance | Input-act and input-envelope vocabulary classify user language before downstream decisions. | An utterance is not automatically a fact, command, route, or truth claim. |
| Request | Candidate-request and routing work preserve possible operator requests before execution or provider selection. | A request is not the same as successful action or selected capability. |
| Conversation turn | Domain-model language names sessions and conversation/interaction threads as lenses over events. | A session or turn is not source of truth by itself. |
| Interaction episode | Participation, relation-of-use, activation, and preservation work describe situated uptake across a bounded work moment. | Episode language is observational and not a runtime proposal. |
| Inquiry episode | Inquiry and discovery-path documents preserve pursuit, candidate paths, gaps, and findings. | Inquiry may survive as lineage, but not every interaction is inquiry. |
| Continuation episode | Handoff and continuation documents focus on resumption, activation, next safe move, and consumption. | Continuation excludes full transcript preservation and instead curates resumption context. |

The useful distinction is not that these are separate system objects. The useful
observation is that final outcomes collapse them. A final answer can hide the
utterance that elicited it, the request interpretation that routed it, the
inquiry path that supported it, and the continuation move it enabled.

## Critical Distinctions Reviewed

The review found evidence for preserving these distinctions as observations,
with varying strength:

| Distinction | Evidence strength | Observation |
| --- | --- | --- |
| `observation time != interaction time` | Moderate | Observation time records when evidence was observed; interaction time concerns when evidence became active, selected, displaced, or resumed. |
| `claim history != interaction history` | Moderate | Claim history can preserve revisions and support while losing the path of operator uptake or inquiry movement. |
| `selection != selection shift` | Strong | Selection can name the winner; selection shift preserves replacement movement. Repository evidence repeatedly warns that losing non-selected remainder and rationale causes repeat work. |
| `active concern != concern transition` | Moderate | Active concern identifies current pull; transition explains how a different concern lost or gained pull. |
| `current work != path to current work` | Strong | Current Work Position curates continuation-relevant emergence but does not equal full path history. |
| `final answer != interaction path` | Strong | Many preservation documents observe that conclusions survive more easily than discovery paths, rejected routes, or activation conditions. |
| `preserved outcome != preserved episode` | Strong | Stored documents, claims, summaries, and projections can survive while activation, uptake, pressure, and safe-move context disappear. |

## Major Findings

### 1. Interaction can appear temporally structured without requiring a new runtime model

The evidence supports temporal structure in interaction as an observation:
activation, selection, displacement, abandonment, redirection, resumption, and
continuation all require temporal ordering. The repository does not require a
new runtime event model to observe this; existing documents already preserve the
pressure in prose, frontiers, audits, and candidate-preservation surfaces.

### 2. Final outcomes tend to over-preserve convergence and under-preserve movement

Repository documents repeatedly show that a final answer, selected edge, current
projection, or promoted claim may survive better than:

- the alternatives considered;
- why rejected routes looked plausible;
- where attention shifted;
- which concern was interrupted;
- what partial inquiry was abandoned;
- what path made the selected result credible;
- what would let a later participant avoid restarting.

This is the central loss when only final outcomes survive.

### 3. Abandoned paths are significant when they prevent duplicate work

Abandoned or redirected paths are not always worth preserving. Repository
evidence is strongest when preservation prevents repeated investigation,
premature convergence, or unsafe continuation. Non-selected remainder and
discovery-path documents make this especially visible: an unchosen path can be
valuable not because it is true, but because it explains why the selected path
was selected and what should not be retried without new evidence.

### 4. Interaction history and knowledge history are related but differently shaped

Knowledge history is often claim-, event-, support-, observation-, or projection-
centered. Interaction history is more often concern-, attention-, selection-,
activation-, and continuation-centered. The same repository artifact can
participate in both histories, but the histories answer different questions.

### 5. Current Work Position and Active Edge are interaction-temporal pressure surfaces

Current Work Position and Active Edge do not merely name content. They ask what
is live, why it is live, what unresolved pressure it occupies, and how work can
continue. They therefore provide strong evidence that the repository already
cares about temporal movement inside work, not only temporal qualification of
facts.

### 6. The repository preserves episodes through curation, not transcripts

Continuation-context work explicitly excludes full transcript preservation as
continuation context. That does not deny interaction temporalness. It suggests a
curation boundary: preserve the selected activation, rationale, pressure,
non-selected remainder, next safe move, and authority boundaries needed for
resumption, not every chronological utterance.

## Duplicate-Work Findings

Duplicate-work pressure appears wherever final outcomes lack the interaction
path that made them useful. Reviewed documents suggest repeat work can arise
when future participants cannot tell:

- that a candidate interpretation was already considered;
- that a concern was once active but displaced;
- that a route was rejected for a boundary reason rather than ignored;
- that a handoff existed but failed activation;
- that a selected edge depended on a now-hidden pressure;
- that a document is relevant as active orientation rather than background
  inventory;
- that a current work position emerged from a prior unresolved tension.

This review found no repository-wide guarantee that duplicate-work prevention is
uniformly preserved. It appears as a recurring documentation pressure, not as a
fully reconciled mechanism.

## Interaction-Temporalness Findings

The most defensible interaction-temporal elements observed are:

```text
activation before use
use before preservation
selection before convergence
candidate before route
attention trigger before attention target
active concern before continuation
handoff availability before handoff activation
current edge before next safe move
abandoned path before non-retry guidance
```

These do not prove a single new concept. They show a family of temporal
relations around work participation.

## Weak Evidence And Limits

Evidence is weaker where:

- documents use episode language metaphorically without preserving concrete
  sequence;
- final summaries name only current state;
- implementation surfaces preserve events but not operator uptake;
- selection rationale is absent or compressed;
- candidate paths are mentioned generically but not tied to specific abandoned
  work;
- handoff context curates next-safe-move information but excludes full
  chronological interaction;
- current-work and active-edge frontiers remain exploratory rather than
  reconciled authority.

The review therefore should not be read as proving that interaction temporalness
is a foundational category. It preserves an observed pressure for future review.

## Unresolved Observations

- Whether interaction temporalness should remain a prose observation, be routed
  through existing concepts such as inquiry, handoff, attention, selection,
  events, and working state, or be distinguished later by a reconciliation.
- Whether abandoned-path preservation has a stable threshold: when does a
  non-selected path deserve preservation, and when is it noise?
- Whether selection shift can be represented adequately by selection rationale
  alone.
- Whether Current Work Position should preserve more emergence history than it
  currently emphasizes.
- Whether Active Edge can preserve prior active edges without becoming a planner,
  scheduler, priority system, or interaction log.
- Whether interaction episodes can be described consistently without proposing a
  runtime conversation system or event schema.
- Whether duplicate-work prevention is the primary value of preserving
  interaction paths, or only one value among explanation, continuity, authority,
  and safe movement.

## Closing Observation

Repository evidence does not show that interaction temporalness is fully
resolved, canonical, or implementation-ready. It does show that many recent
investigations become harder to explain if only final outcomes survive.

The cautious observation is:

```text
Some repository work depends on preserving not only what survived,
but how work moved: what became active, what was displaced, what was abandoned,
what was redirected, and what made continuation possible.
```
