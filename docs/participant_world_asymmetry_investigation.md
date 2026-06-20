---
title: Participant / World Preservation Asymmetry Investigation
status: exploratory observation
authority: documentation-only investigation; not implementation, runtime design, client design, agent design, memory design, chat design, schema design, or new ontology
created: 2026-06-20
scope: repository evidence review
---

# Participant / World Preservation Asymmetry Investigation

## Purpose

This investigation tests the hypothesis that Seed currently has a rich model of
world reality but only primitive preservation of a participant's relationship to
that reality.

This is not a proposal to build a chat system, agent, participant memory,
working-state machine, active-edge machine, orientation store, runtime behavior,
or new ontology. The server/client split is treated only as an investigative
framing and is not promoted as canonical architecture.

## Files Inspected

Primary requested files inspected:

- `docs/inquiry_note_orientation_probe_plan.md`
- `docs/inquiry_note_orientation_surface_reachability_observation.md`
- `docs/orientation_bundle_load_bearing_observation.md`
- `docs/participant_orientation_view_selection_observation.md`
- `docs/working_state_activation_observation.md`
- `docs/working_state_activation_failure_observation.md`
- `docs/working_state_activation_artifact_audit.md`
- `docs/continuation_context_and_working_state_reconciliation.md`
- `docs/relation_of_use_observation.md`
- `docs/relation_of_use_decomposition_observation.md`
- `docs/current_work_position_frontier.md`
- `docs/active_edge_frontier.md`

Additional authority/background inspected:

- `docs/foundational_ontology_reconciliation.md`
- `docs/reality_fact_and_claim_reconciliation.md`
- `docs/relationship_observation_v0_reconciliation.md`
- `docs/state_summary_filesystem_projection_boundary_audit.md`

## High-Level Finding

Repository evidence supports a weaker version of the hypothesis:

```text
Seed has mature preservation machinery for represented world knowledge.
Seed has many names for participant-position pressures.
Seed has not reconciled those pressures into an equally mature participant-side
preservation model.
```

The evidence does **not** support turning that asymmetry into a server/client
architecture. It also does not support implementing participant memory, active
orientation storage, or an agent. The better-supported finding is architectural:
many recent failures are not failures to preserve objects or documents; they are
failures to preserve how a participant was positioned relative to preserved
knowledge.

## World-Side Inventory

World-side concepts primarily describe `what exists`, `what was observed`, or
`what Seed has represented about reality`.

| Concept | What is preserved | What survives interruption | Authority owned |
| --- | --- | --- | --- |
| Observation | Source-attributed report from a vantage point at a time. | The report and its provenance can survive as evidence even when later work changes. | Reports what a source observed; does not become reality itself. |
| Evidence | Preserved support material and provenance for considering claims. | Support chains, timestamps, source identity, and trust/corroboration context can survive. | Explains why a claim may be considered; does not by itself decide truth. |
| Claim | Scoped proposition available for preservation, support, interpretation, or communication. | The represented proposition and its support status survive as knowledge material. | Central represented knowledge primitive; says what is being asserted or considered. |
| Fact | Normalized provenance-backed claim. | Durable facts and current measurement samples can survive projection and interruption. | Communicates normalized represented propositions, not direct possession of reality. |
| Relationship | Normalized connection claim between things. | Directional edges such as syntactic imports can survive as relationship evidence. | Preserves connection evidence without overreading behavior, ownership, or authority. |
| State | Conditions over time as represented from events, facts, and projection. | Projected state can survive as a current read model or summary after acquisition. | Describes represented current conditions; does not own all summary meaning. |
| Projection / State Summary | Selected communication surface over preserved knowledge. | Rows, counts, current samples, and summaries can survive for later inspection. | Communicates selected knowledge for consumers; must not imply unearned topology, priority, or meaning. |

The world-side architecture is comparatively mature because it repeatedly
preserves boundaries:

```text
observation != reality
evidence != truth
claim != fact
relationship != behavior
projection != authority
summary row != full meaning
```

## Participant-Side Inventory

Participant-side concepts primarily describe `a participant's relationship to
preserved knowledge`: what is active, relevant, usable, safe to continue, or
positioning the work.

| Concept | What survives | What fails | Apparent authority owned |
| --- | --- | --- | --- |
| Inquiry note | Raw operator prose may survive as inquiry evidence and remain visible in an orientation view. | It does not reliably make repository concepts reachable, does not become intent, and does not activate work. | Evidence of pressure or question as expressed; no authority to classify intent, command, goal, or work type. |
| Orientation | Some bundles of concern, pressure, boundary, active edge, continuation, and next safe move can be documented. | Orientation does not converge cleanly into State or knowledge structure; related material can be found without governing current work. | Participant positioning over knowledge; shows how to read/use preserved material now. |
| Working state | Activation artifacts, summaries, and handoff-like materials may survive. | Existing answers can fail to start the right work; artifacts decay into archive when not consumed as current. | Readiness-to-resume and activation relation; not merely possession of information. |
| Current work position | Candidate components such as selected question, active frontier, authority boundary, validation state, and next safe move may be preserved in documents. | A later participant may not know what is active, why it is active, what governs it, or what move is safe. | Selected, bounded, continuation-relevant position of work. |
| Active edge | The unresolved edge pulling work forward can be named and sometimes recorded. | Preserved gaps, contradictions, or frontiers may become inactive even though their content remains. | Current pull of work; not priority, truth, or repository-wide schedule. |
| Activation | An artifact may be present and readable. | The relation from artifact to live work may not fire; answer survives but activation does not. | Converts preserved support into resumed work only when consumed with correct context. |
| Continuation | Documents, handoffs, summaries, and lineage can persist. | Continuation fails when active context, edge, rationale, boundary, or safe movement is missing. | Survival of intelligible work movement across interruption, not mere artifact storage. |
| Relation-of-use | Documentation can preserve that some knowledge supports or is used by a work concern. | Support can remain while the relation explaining why it matters to current work disappears. | Connects knowledge to present concern, relevance, activation, and safe movement. |
| Orientation bundles / participant orientation | Bundles may preserve concern, pressure, reference point, boundary, active edge, continuation, next safe move, selection rationale, and validation state. | The bundle is not an indivisible primitive and is not guaranteed by preserving any single document. | Compositional participant positioning; currently exploratory rather than canonical. |

## Authorities Identified

The repository evidence suggests different authority centers rather than a
single collapsed model:

- Foundational ontology owns the stable distinction among observation, evidence,
  claim, fact, relationship, state, projection, handoff, authority, and operator
  intent.
- Reality/fact/claim reconciliation owns the boundary that reality contains
  facts while Seed preserves representations of reality.
- Relationship observation owns the distinction between observed things and
  observed connections, especially avoiding behavior overclaiming.
- State Summary projection owns communication of selected represented state, but
  not all semantic interpretation or operator relevance.
- Inquiry note work owns raw inquiry prose as evidence, not as intent or command.
- Orientation and bundle documents own exploratory language for participant
  positioning, but do not create a canonical orientation object.
- Working-state activation documents own the distinction between available
  information and activated work.
- Current-work-position and active-edge frontiers own open pressure surfaces, not
  resolved ontology or runtime designs.

## Recurring Failure Patterns

The recurring failures are better explained as relationship failures than object
failures:

| Pattern | What survives | What does not survive | Failure type |
| --- | --- | --- | --- |
| Knowledge survives; work does not. | Facts, docs, summaries, answers, and support. | What is active, why it matters now, and how to continue. | Participant-position / continuation relation failure. |
| Answer survives; activation does not. | A prior response or artifact can be found. | The artifact does not re-enter live work as the governing answer. | Activation relation failure. |
| Support survives; relation-of-use does not. | Evidence and support remain. | The reason this support bears on the present concern is lost. | Use/relevance relation failure. |
| Documents survive; continuation does not. | Handoff-like or explanatory documents persist. | Active edge, selected boundary, rationale, validation state, or next safe move. | Bundle persistence failure. |
| Repository concepts survive; inquiry orientation cannot reach them. | Concepts like State Summary, source navigation, active edge, current work position, and claim exist in docs. | They participate weakly or not at all in inquiry orientation V1. | Reachability / participant-orientation surface failure. |

These are not primarily failures of `what exists`. They are failures of `how the
participant was related to what exists`.

## Inquiry Note Positioning

Inquiry notes appear to be an early participant-side artifact, not the fully
formed participant-side model.

Evidence supporting this position:

- The probe plan explicitly preserves raw operator prose as inquiry evidence and
  refuses to promote it into intent, goals, commands, work types, claims, or
  execution authority.
- The orientation surface observation found that runtime entities participate
  more readily than repository concepts such as active edge, current work
  position, orientation, and claim.
- The note is participant-originated rather than world-observed: its shape is
  closer to `participant -> inquiry note` than `world -> observation`.

Evidence limiting this position:

- Inquiry note preservation alone does not preserve activation, current work
  position, active edge, or relation-of-use.
- It is still evidence, not participant memory or a participant model.
- It does not justify a chat, agent, client, or runtime design.

Conclusion: inquiry notes are best read as an **early participant-side evidence
artifact**.

## Continuation Findings

Continuation behaves more like bundle persistence than artifact persistence.

Artifact persistence preserves a document, summary, handoff, answer, or note.
The continuation documents repeatedly show that this is insufficient. Successful
continuation appears to require enough of a bundle to survive:

```text
active concern
selected edge
boundary / authority
unresolved tension
selection rationale
validation state
next safe move
relation-of-use
```

This aligns strongly with participant-side concerns because the missing material
is not usually the world object. It is the participant's position relative to
preserved objects: where work was, why it was there, and what movement remained
safe.

## Orientation Findings

Orientation behaves more like participant positioning than knowledge structure.

It uses knowledge structures, and it may render facts, summaries, source
navigation rows, and support. But the load-bearing orientation material is often
relational and situated:

```text
concern -> pressure -> reference point -> boundary -> active edge -> safe move
```

The repository does not support treating orientation as an indivisible primitive
or as stored State. It more strongly supports treating orientation as a
composition that makes preserved knowledge usable for a participant at a moment
of work.

## Comparison: State-Centered Explanation

A State-centered explanation says these difficulties arise because the right
facts, relationships, or projected State rows have not yet been represented.

| Topic | State-centered explanation | Fit |
| --- | --- | --- |
| Orientation | Orientation is missing from State or projection. | Partial. Projections can render related material, but orientation failures persist when material exists. |
| Continuation | Continuation needs better persisted artifacts. | Weak to partial. Artifacts persist, but continuation still fails without active edge and rationale. |
| Activation | Activation needs a stored status or artifact. | Weak. Existing artifacts can be found and still not activate work. |
| Current work position | Position is a missing object or State field. | Weak. Frontiers caution against assuming it is an object. |
| Active edge | Active edge is a missing priority/focus state. | Weak. Documents distinguish active pull from priority, truth, or scheduler state. |
| Relation-of-use | Use relation should become a relationship fact. | Partial. Relationship language helps, but use is more situated than static edges like imports. |

The State-centered framing explains some acquisition/projection gaps, especially
where facts, relationships, and summary selection are missing. It does not
explain why preserved knowledge repeatedly remains inert.

## Comparison: Participant-Centered Explanation

A participant-centered explanation says the repeated difficulties arise because
Seed preserves world knowledge more maturely than it preserves participant
positioning relative to that knowledge.

| Topic | Participant-centered explanation | Fit |
| --- | --- | --- |
| Orientation | Orientation is the participant's situated way of reading preserved knowledge. | Strong. Explains why concern, pressure, boundary, active edge, and safe move matter. |
| Continuation | Continuation requires preserving enough participant-position bundle to resume. | Strong. Explains why documents can survive while continuation fails. |
| Activation | Activation is a relation between preserved material and live work. | Strong. Explains answer-present/work-not-started failures. |
| Current work position | Position names selected, bounded, continuation-relevant participant/work placement. | Strong. Matches frontier caution that it may not be an object. |
| Active edge | Active edge is what currently pulls participant work forward. | Strong. Explains active versus inactive preserved concerns. |
| Relation-of-use | Use records why knowledge matters to the current participant concern. | Strong. Explains support-survives/use-disappears failures. |

The participant-centered framing better explains the repository's repeated
difficulties. It should remain an investigative explanation, not a mandate to
build participant memory, clients, agents, or runtime machinery.

## Candidate Observations

Candidate observation 1:

```text
Seed's world-side preservation is claim/evidence/projection mature, while
participant-side preservation remains mostly document-and-frontier shaped.
```

Candidate observation 2:

```text
Many recent failures are relationship-to-knowledge failures rather than
knowledge-object failures.
```

Candidate observation 3:

```text
Inquiry notes are early participant-side evidence: they preserve expressed
pressure without owning intent, activation, or continuation.
```

Candidate observation 4:

```text
Continuation pressure is bundle-shaped. Preserving a single artifact is weaker
than preserving the relations among concern, boundary, active edge, rationale,
validation, and safe movement.
```

Candidate observation 5:

```text
Orientation is not well explained as State alone. It is better explained as
participant positioning over preserved knowledge, with State/projections serving
as inputs rather than the whole phenomenon.
```

## Remaining Uncertainties

- Whether participant-side pressures can be reconciled using existing concepts
  such as handoff, evidence, relationship, projection, and operator intent, or
  whether a future reconciliation will need a sharper distinction.
- Whether relation-of-use can be represented safely as a relationship without
  overclaiming behavior, intent, or priority.
- Whether inquiry orientation V1 fails on repository concepts because those
  concepts are absent from participating surfaces, present but unreachable, or
  reachable but lexically disconnected.
- Whether current work position and active edge are distinct concepts, bundle
  members, roles within continuation, or alternate names for overlapping
  pressures.
- Whether a future State/projection improvement could explain more of the
  failure pattern without needing a participant-centered framing.

## Files Changed

- `docs/participant_world_asymmetry_investigation.md`

## LOC Changed

One documentation file added, approximately 300 lines.
