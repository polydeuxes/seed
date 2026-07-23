---
doc_type: observation
status: exploratory
domain: non-selected remainder preservation
introduced_by: non-selected remainder preservation observation
depends_on:
  - selection_convergence_observation.md
  - preservation_surface_observation.md
  - preservation_failure_observation.md
  - discovery_path_preservation_observation.md
  - documentation_lineage_observation.md
  - inquiry_frontier.md
  - current_work_position_frontier.md
  - active_edge_frontier.md
  - working_state_activation_observation.md
  - working_state_activation_failure_observation.md
  - language_candidate_routing_and_promotion_reconciliation.md
  - natural_language_request_routing_audit.md
  - interpretation_candidate_preservation_audit.md
  - continuity_frontier.md
  - handoff_and_continuation_lineage_frontier.md
related:
  - source_type_and_candidate_family_reconciliation.md
  - architectural_findings_vocabulary.md
  - architectural_findings_preservation.md
  - audit_chain_findings_preservation.md
  - selection_and_attention_frontier.md
  - selection_rationale_reconciliation.md
  - why_not_explanation_characterization.md
  - handoff_pressure_transition_observation.md
  - handoff_consumption_activation_reconciliation.md
---

# Non-Selected Remainder Preservation Observation

## Purpose

This document observes repository evidence around the question:

```text
What happens to the non-selected remainder?
```

It also asks:

```text
Does repository work preserve non-selected possibilities?
```

and:

```text
Are rejected, deferred, inactive, or non-selected items important repository artifacts?
```

This is an observation. It is not a reconciliation, frontier, implementation
proposal, policy proposal, decision-system proposal, selection ontology,
archival policy, prioritization system, execution design, or remediation plan.
Repository authority wins over this document. Existing preservation, selection,
lineage, routing, promotion, current-work-position, active-edge, continuity,
handoff, inquiry, and vocabulary documents remain authoritative for their own
scopes.

## Method

The investigation used repository content directly. It began from recent
selection, preservation, lineage, active-edge, current-work-position, working
state, language-candidate, routing, promotion, continuity, and handoff documents,
then widened through repository maps, frontmatter links, navigation documents,
adjacent reconciliations, and broad `rg` searches.

Search terms included:

```text
rejected, not selected, non-selected, non selected, inactive, deferred,
alternative, candidate, lineage, discovery path, preservation, continuity,
active edge, current work, selection, routing, promotion, abandoned, superseded,
archived, unresolved, not active, current concern, dormant, remainder
```

Documents inspected included at least:

- `README.md`
- `docs/archive/original_book_of_seed/01-architecture.md`
- `docs/index.md`
- `docs/architectural_knowledge_map.md`
- `docs/selection_convergence_observation.md`
- `docs/preservation_surface_observation.md`
- `docs/preservation_failure_observation.md`
- `docs/discovery_path_preservation_observation.md`
- `docs/documentation_lineage_observation.md`
- `docs/inquiry_frontier.md`
- `docs/current_work_position_frontier.md`
- `docs/active_edge_frontier.md`
- `docs/working_state_activation_observation.md`
- `docs/working_state_activation_failure_observation.md`
- `docs/language_candidate_routing_and_promotion_reconciliation.md`
- `docs/natural_language_request_routing_audit.md`
- `docs/interpretation_candidate_preservation_audit.md`
- `docs/source_type_and_candidate_family_reconciliation.md`
- `docs/continuity_frontier.md`
- `docs/handoff_and_continuation_lineage_frontier.md`
- `docs/handoff_pressure_transition_observation.md`
- `docs/handoff_consumption_activation_reconciliation.md`
- `docs/architectural_findings_vocabulary.md`
- `docs/architectural_findings_preservation.md`
- `docs/audit_chain_findings_preservation.md`
- `docs/selection_and_attention_frontier.md`
- `docs/selection_rationale_reconciliation.md`
- `docs/why_not_explanation_characterization.md`
- `docs/candidate_request_and_routing_boundary_reconciliation.md`
- `docs/candidate_meaning_and_ambiguity_reconciliation.md`
- `docs/knowledge_acquisition_and_selection.md`
- `docs/context_composition_reconciliation.md`
- `docs/source_navigation_surface_reconciliation.md`
- `docs/navigation_hygiene_audit.md`

Absence of a preservation statement was treated as uncertainty, not proof of
non-existence. Presence of a preserved alternative was treated as evidence that
some remainder survives, not proof of a complete remainder-preservation system.

## High-Level Observation

Repository work does not treat selection as simple deletion. Across multiple
surfaces, selected items become active, routed, promoted, current, or used, while
other items often remain visible as rejected concepts, deferred concepts, open
questions, competing beliefs, stale or unsupported facts, historical findings,
superseded findings, inactive goals, dormant pressures, alternative
interpretations, or discovery paths.

The strongest current observation is:

```text
non-selection often changes an artifact's role rather than erasing it.
```

That observation is uneven. Some repository areas preserve the remainder
explicitly, especially architectural findings, discovery paths, and candidate
interpretation audits. Other areas expose a preservation gap, especially where a
process compresses many possible interpretations into one routed or selected
result without recording the interpretation space.

## Selection Does Not Exhaust Preservation

`selection_convergence_observation.md` observes the recurring shape:

```text
many possibilities
    -> some become active, current, routed, promoted, attended, preserved, or used
```

That formulation already leaves a remainder question open. If some possibilities
become active, current, routed, or promoted, repository evidence must still ask
whether the others were discarded, preserved as background, deferred, rejected,
made historical, or simply never captured.

The reviewed evidence supports a distinction between:

```text
selected for current use
```

and:

```text
preserved for lineage, audit trail, future inquiry, negative explanation, or
continuation memory
```

The distinction is strongest when repository documents preserve why a rejected
path should not be repeated, why a deferred concern is not current work, or why a
candidate interpretation was meaningful even if not routed.

## Non-Selected Candidate Patterns

### Interpretation candidates

`interpretation_candidate_preservation_audit.md` is the clearest direct evidence
for a non-selected candidate problem. It distinguishes the selected
interpretation result from the wider interpretation space. Its example of
"Show me summary" shows several plausible meanings while warning that little may
remain after classification or execution.

This makes interpretation candidates an important remainder artifact:

```text
possible meanings
    -> selected interpretation
    -> non-selected meanings may explain ambiguity, risk, or future why-not questions
```

The evidence does not prove that all non-selected interpretations are currently
preserved. It supports the narrower finding that the repository has already
noticed a preservation gap around them.

### Candidate families

`source_type_and_candidate_family_reconciliation.md` broadens the candidate
space beyond language. It identifies relationship, fact, request, route, claim,
boundary, pressure, question, target, capability, observation, continuation, and
learning-lens candidates. Many of these are explicitly bounded as candidates,
not current selections or execution authority.

That supports a remainder pattern:

```text
candidate family exists
    -> promotion or routing may select some candidates
    -> unpromoted or unrouted candidates may still matter as source-scoped possibilities
```

This document does not convert those families into a selection ontology. It only
observes that the repository already contains multiple candidate surfaces whose
non-selected side can carry meaning.

### Competing belief and why-not candidates

`why_not_explanation_characterization.md` shows a related but distinct pattern in
projected state: current beliefs can have competing beliefs, unsupported facts,
stale facts, ambiguous support, or no-current-belief statuses. These are not the
same as rejected candidate interpretations, but they demonstrate that Seed
already treats non-current or non-winning material as explanatory evidence in
some contexts.

The relevant remainder shape is:

```text
current belief
    !=
all supported, stale, unsupported, ambiguous, or competing material
```

## Deferred, Rejected, Historical, and Superseded Artifact Patterns

`architectural_findings_vocabulary.md` provides the strongest vocabulary-backed
evidence that non-selected artifacts can be important. It treats architectural
memory as including accepted findings as well as recommendations, rejections,
deferrals, open questions, lessons, non-goals, historical findings, stale
material, quarantined material, archived material, and superseded findings.

This establishes several distinctions relevant to the remainder:

```text
rejected
    !=
forgotten
```

```text
deferred
    !=
rejected
```

```text
historical or superseded
    !=
meaningless
```

The vocabulary document owns the terminology for architectural findings. This
observation should not duplicate or redefine that vocabulary. It only notes that
finding vocabulary already preserves many artifacts that are not selected as
current work.

## Inactive-But-Preserved Patterns

### Current work position

`current_work_position_frontier.md` and adjacent continuity documents imply that
there can be a current work position without every concern becoming current.
Current position is a continuity surface for orientation, not proof that other
concerns are irrelevant.

The observed remainder shape is:

```text
current concern
    -> active orientation
non-current concern
    -> may remain in lineage, frontier, backlog, open question, handoff, or finding memory
```

The repository does not consistently name "non-current concern" as a first-class
artifact, but it repeatedly preserves previous concerns through frontiers,
handoffs, status documents, and lineage observations.

### Active edge

`active_edge_frontier.md` preserves the unresolved edge that is most relevant to
continuation. That framing implies inactive or less-active pressures: if one
edge is active, other pressures may be dormant, deferred, already owned, or
historical.

The evidence supports this distinction only observationally:

```text
active pressure
    !=
only preserved pressure
```

Active-edge documents help preserve focus, but they do not erase inactive
pressures. The tension is that focus can compress the surrounding pressure field
unless other surfaces preserve it.

### Working state activation

`working_state_activation_observation.md` and
`working_state_activation_failure_observation.md` investigate how available
understanding becomes activated understanding, and how activation can fail. This
is selection-like but not equivalent to deletion. Available understanding can
remain in the repository even when not activated in a participant's current
working state.

The strongest inactive-but-preserved pattern is:

```text
available understanding
    -> activated understanding
available but inactive understanding
    -> still preserved, but vulnerable to non-activation
```

## Discovery-Path Dependencies

`discovery_path_preservation_observation.md` is strong evidence that repository
work depends on preserving more than final selected findings. Discovery path work
asks whether challenge sequences, critique sequences, assumption exposure,
contradiction-driven shifts, compression removal, and understanding transitions
survive.

That implies paths not taken can be important when they explain how a selected
finding became visible. A rejected compression, abandoned framing, or alternative
interpretation may be the evidence that a later distinction was discovered.

The strongest discovery-path dependency is:

```text
final finding alone may not preserve why the finding exists
```

Therefore, non-selected or superseded explanations may remain important as
transition evidence, even when they are not current architecture.

## Continuity Dependencies

`continuity_frontier.md`, `handoff_and_continuation_lineage_frontier.md`, and
handoff reconciliation documents preserve continuation across participants and
sessions. Continuity depends on current orientation, but it also depends on
lineage, open questions, active edge, and the context needed to avoid restarting
or repeating prior work.

That creates a remainder dependency:

```text
selected next concern
    -> useful for continuation
non-selected adjacent concerns
    -> may still prevent duplicate work, repeated rejection, or loss of inquiry path
```

Continuity work therefore appears to preserve some non-selected material because
continuation requires knowing not only where to proceed, but also what was
already considered, deferred, rejected, or left unresolved.

## Language Routing and Promotion Remainder

Language-candidate and request-routing work provides the sharpest selection /
remainder tension. `language_candidate_routing_and_promotion_reconciliation.md`
and `natural_language_request_routing_audit.md` separate candidate meanings,
request routing, promotion, authority, and execution. The repository repeatedly
rejects collapsing natural language into direct command or fact authority.

The tension is that routing and promotion make selected results legible, while
unrouted and non-promoted candidates may disappear unless a preservation surface
records them.

The strongest language-side observation is:

```text
candidate interpretations may be meaningful even when not routed or promoted
```

The strongest limitation is:

```text
repository evidence does not show uniform preservation of unrouted candidates
```

## Critical Distinctions Under Review

The reviewed evidence supports these distinctions in some areas, but not always
uniformly:

```text
non-selected
    !=
discarded
```

Strongly supported by architectural findings, discovery-path preservation,
continuity, why-not explanation, and interpretation-candidate preservation work.
Weak where runtime or language interpretation compresses candidate space into a
single result without preserved alternatives.

```text
inactive
    !=
irrelevant
```

Supported by active-edge, current-work-position, continuity, handoff, and
working-state activation documents. Inactive concerns may remain available,
deferred, historical, or dormant.

```text
deferred
    !=
rejected
```

Strongly supported by architectural findings vocabulary. Deferred concepts wait
for conditions, evidence, clearer need, or priority; rejected concepts record a
negative boundary or unsupported path.

```text
not active
    !=
not preserved
```

Supported by preservation, lineage, continuity, handoff, historical finding, and
frontier surfaces. Not all preserved material is active, and not all active
material is the only preserved material.

## Selection / Preservation Tensions

### Selected vs preserved

Selection makes a bounded subset usable. Preservation keeps other material
available for lineage, future inquiry, audit trail, rejected-path memory, or
continuity. The tension is that selected material can become easier to navigate,
while preserved remainder may become diffuse.

### Active vs preserved

Active edge and current work surfaces improve continuation by identifying what
matters now. Preservation surfaces keep additional material available. The
tension is that activation can obscure preserved but inactive concerns.

### Inactive vs irrelevant

Inactive material may be irrelevant to the current step, but repository evidence
shows it can remain relevant to future inquiry, duplicate-work avoidance,
discovery path, or rejected-path memory.

### Rejected vs deferred

Rejected paths are important because they prevent repeated collapse into known
bad framings. Deferred paths are important because they may become relevant under
new evidence or clearer questions. Treating either as simple deletion loses
different kinds of architectural memory.

### Current concern vs dormant concern

Current concern surfaces concentrate attention. Dormant concerns may survive in
frontiers, handoffs, open questions, backlog/status documents, historical
findings, or preservation observations. The repository does not yet show a single
uniform dormant-concern surface.

### Active edge vs inactive pressure

Active edge identifies the pressure most useful for continuation. Inactive
pressures may remain unresolved or preserved elsewhere. The tension is whether
inactive pressure remains discoverable after the active edge moves.

### Selection vs lineage

Lineage preserves how an artifact, question, or finding came to be. Selection
can hide previous alternatives unless lineage records them. Documentation
lineage and discovery-path work make this tension visible.

### Selection vs preservation

Selection can be necessary for action, context, current belief, routing, or
continuation. Preservation can be necessary for memory, explanation, and
non-repetition. The repository treats these as related but not identical.

## Strongest Patterns Found

### Strongest non-selected artifact patterns

- non-promoted interpretation candidates;
- competing or unsupported fact material around current belief selection;
- rejected architectural concepts;
- deferred architectural concepts;
- open questions not selected as current work;
- inactive goals or concerns;
- superseded or historical findings;
- non-active pressures around an active edge;
- alternative discovery explanations preserved as critique or lineage.

### Strongest deferred-artifact patterns

Deferred architectural findings are the strongest explicit pattern. Future-work,
frontier, backlog/status, open-question, and handoff surfaces also preserve work
that is not selected for immediate action.

### Strongest inactive-but-preserved patterns

Current-work-position, active-edge, working-state activation, and continuity
surfaces imply that inactive concerns can remain meaningful. Architectural
findings vocabulary gives the clearest names for inactive statuses such as
historical, stale, quarantined, archived, superseded, and deferred.

### Strongest discovery-path dependencies

Discovery-path preservation depends on preserving challenge sequences,
assumption exposure, rejected compressions, superseded explanations, and
transitions in understanding. These are often not the selected final finding, but
they explain why the final finding should be trusted or how it emerged.

### Strongest continuity dependencies

Continuity depends on active orientation plus enough remainder memory to avoid
restart, duplicate investigation, repeated rejected paths, and loss of unresolved
questions. Handoff and continuation lineage documents preserve this combination
more directly than selection documents alone.

### Strongest selection/remainder tensions

The strongest tension appears where language or context selection produces a
bounded result, while preservation work expects lineage, alternatives, and
non-current material to remain inspectable.

## Duplicate-Work Check

Prior documents already own the following:

- `selection_convergence_observation.md` owns the cross-repository observation
  that many surfaces converge on selection-like transitions.
- `preservation_surface_observation.md` owns the broad observation that recent
  concepts become legible through preservation behavior.
- `preservation_failure_observation.md` owns the pattern where later repository
  growth compensates for what prior artifacts failed to preserve.
- `discovery_path_preservation_observation.md` owns discovery-path preservation,
  critique sequences, assumption exposure, and compression-removal evidence.
- `documentation_lineage_observation.md` owns how documents generate or route
  later documents.
- `current_work_position_frontier.md` and `active_edge_frontier.md` own current
  continuation orientation and active unresolved pressure.
- `working_state_activation_observation.md` and
  `working_state_activation_failure_observation.md` own activation of available
  understanding into working state.
- `language_candidate_routing_and_promotion_reconciliation.md`,
  `natural_language_request_routing_audit.md`, and
  `interpretation_candidate_preservation_audit.md` own language candidate,
  routing, promotion, and interpretation-space concerns.
- `continuity_frontier.md` and handoff documents own continuation and handoff
  lineage.
- `architectural_findings_vocabulary.md` owns vocabulary for rejected, deferred,
  open, historical, superseded, archived, and related architectural findings.

This observation adds only the cross-cutting remainder question:

```text
when selection narrows many possibilities to a bounded subset, what repository
surfaces preserve the non-selected side, and where does that preservation appear
strong, weak, or unresolved?
```

It should avoid duplicating vocabulary, policy, ontology, archival design,
routing design, selection rationale design, implementation behavior, or
frontier ownership from the documents above.

## Non-Selection Findings

- Non-selected items are often preserved when they carry architectural memory,
  especially as rejected, deferred, historical, superseded, competing,
  unsupported, inactive, open, or alternative material.
- Non-selected interpretation candidates are explicitly recognized as a possible
  preservation gap.
- Non-selected pressures and concerns appear indirectly through active-edge,
  current-work-position, continuity, handoff, and frontier surfaces.
- Non-selected navigation paths appear in discovery-path and documentation
  lineage work when a path explains how a finding was reached or why a repeated
  compression should not recur.
- Repository evidence does not support the claim that every non-selected item is
  preserved, nor that every non-selected item should be preserved.

## Preservation Findings

- Preservation is broader than current selection. It includes lineage,
  continuity, inquiry, discovery path, rejected-path memory, open questions,
  historical findings, and deferred concerns.
- Preservation is uneven. Documentation surfaces preserve remainder artifacts
  more explicitly than some runtime or interpretation surfaces.
- Preservation of the remainder often serves explanation and duplicate-work
  avoidance rather than immediate execution.
- Preservation can fail even when an artifact survives, if the surrounding
  question, critique, or interpretation space is compressed away.

## Non-Selection Findings by Required Remainder Question

| Remainder type | Evidence found | Limit observed |
| --- | --- | --- |
| Non-selected candidates | Interpretation-space audit, candidate-family reconciliation, why-not competing beliefs | No uniform repository-wide preservation mechanism for all candidate alternatives |
| Non-selected concerns | Current-work-position, active-edge, continuity, handoff, frontier documents | Non-current concern is not consistently named as a first-class artifact |
| Non-selected pressures | Active edge implies inactive or deferred pressures; preservation documents keep some pressure history | Inactive pressure discoverability may depend on scattered documents |
| Non-selected work threads | Handoff, continuity, documentation lineage, future-work and deferred finding surfaces | Not every abandoned or dormant thread is clearly marked |
| Non-selected navigation paths | Discovery-path preservation and lineage observations | Discovery paths can be compressed into final findings |
| Non-selected interpretations | Language candidate and interpretation preservation audits | Preservation gap is explicit; preservation itself is not uniformly shown |

## Unresolved Observations

- Whether repository work should preserve every meaningful non-selected
  alternative remains unresolved and outside this observation's authority.
- The repository shows strong preservation of rejected and deferred architectural
  findings, but weaker evidence for systematic preservation of every unrouted or
  non-promoted language candidate.
- It remains unclear how much of the inactive pressure field survives after an
  active edge moves.
- It remains unclear when a non-selected item becomes historical, deferred,
  rejected, superseded, archived, or simply absent.
- It remains unclear whether duplicate-work avoidance depends more on rejected
  path preservation, discovery-path preservation, handoff lineage, or navigation
  hygiene.
- It remains unclear how often selection compresses away useful remainder
  information in practice, as opposed to merely risking that loss.

## Closing Observation

The repository appears to preserve many non-selected artifacts, but not by a
single uniform mechanism. Rejected paths, deferred concepts, inactive concerns,
competing beliefs, alternative interpretations, dormant pressures, open
questions, superseded explanations, and discovery paths survive through
different documentation surfaces and with different strengths.

The non-selected remainder is therefore not merely waste. In repository evidence,
it can be architectural memory, inquiry context, continuity support, explanation
material, rejected-path protection, or discovery-path evidence. The unresolved
question is not whether any remainder matters; the evidence says some does. The
unresolved question is where remainder preservation is strong enough, where it is
only implicit, and where selection still compresses meaningful alternatives out
of view.
