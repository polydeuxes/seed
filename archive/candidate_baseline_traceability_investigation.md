---
status: investigation
scope: candidate baseline as possible traceability layer
created: 2026-06-21
---

# Candidate Baseline Traceability Investigation

## Status

Investigation only. This document does not implement candidate baselines,
accepted baselines, expectations, change readiness, storage, projections,
runtime behavior, policy, ontology, diagnostic surfaces, or architecture changes.
Repository authority wins over this investigation.

## Question

Recent traceability work can increasingly answer:

```text
what changed
why a conclusion exists
why a conclusion was selected
how trustworthy history is
```

The unresolved pressure is narrower:

```text
Compared to what?
```

This investigation asks whether `candidate baseline` is the repository-supported
name for that missing answer, or whether existing concepts such as snapshot,
continuity, selection rationale, concern, accepted baseline, or expectation
already explain the pressure without needing a distinct concept.

## Repository evidence reviewed

Primary evidence reviewed:

- `docs/candidate_baseline_accepted_baseline_expectation_audit.md`
- `docs/baseline_continuity_expectation_audit.md`
- `docs/comparison_reference_authority_reconciliation.md`
- `docs/unified_derivation_architecture_investigation.md`
- `docs/selection_rationale_reconciliation.md`
- `docs/selection_rationale_summary_characterization.md`
- `docs/history_brief_implementation_characterization.md`
- `docs/snapshot_policy_audit_implementation_characterization.md`
- `docs/impact_audit_implementation_characterization.md`
- `docs/repository_observation_v0_implementation_characterization.md`
- `docs/operational_story_implementation_characterization.md`
- `docs/architecture_conformance_audit_implementation_characterization.md`
- tests covering recent visibility surfaces, including `reasoning_path`,
  `selection_path`, `history_brief`, `snapshot_policy`, `impact_audit`,
  `operational_story`, `architecture_conformance`, and
  `repository_observation`.

The strongest prior evidence already states that candidate baseline is distinct
from raw continuity evidence because it selects historical or observed continuity
as a comparison reference for a question. The same prior audit also keeps
acceptance and expectation behind separate authority boundaries:

```text
Observation
    -> Visibility
    -> Continuity evidence
    -> Candidate baseline
    ? authority selection
    -> Accepted baseline
    ? should-bearing authority
    -> Expectation
```

That chain is treated here as evidence to evaluate, not as an ontology to adopt.

## Candidate-baseline observations

Repository evidence supports candidate baseline as a **plausible comparison
reference for a bounded question**. The concept is more specific than captured
evidence and less authoritative than an accepted comparison reference.

Supported characterization:

```text
candidate baseline
    = evidence-supported possible comparison reference
      for a bounded comparison question
```

Important limits:

- It is not raw observation.
- It is not just persistence.
- It is not the current state.
- It is not a selected authority-bearing reference.
- It is not a should claim.
- It is not an alert, remediation, policy, ownership claim, or topology truth.

The key repository pressure is not simply that old data exists. The pressure is
that an operator or audit wants to interpret change and must know which prior or
alternate condition is meaningful enough to compare against. That is the gap
behind `Compared to what?`.

## Difference from snapshot

Repository evidence distinguishes snapshots from baselines in two ways.

First, projection snapshots and audit snapshots are captured artifacts or cached
read-model artifacts. They can preserve or accelerate access to evidence, but
they do not by themselves explain which captured state should become the
comparison reference for a question.

Second, snapshot policy and history brief surfaces can say whether comparison
data exists, what changed between captured artifacts, and what confidence limits
apply. They still do not decide the semantic reference question:

```text
this snapshot exists
    !=
this snapshot is the meaningful comparison reference
```

Therefore:

```text
snapshot
    = captured evidence / cached or persisted observation artifact

candidate baseline
    = candidate interpretation of some evidence as a comparison reference
```

A snapshot can support a candidate baseline. A candidate baseline can cite a
snapshot. But a snapshot does not become a candidate baseline merely by existing.

## Difference from current state

Current state answers what the repository projection currently represents.
Candidate baseline answers what reference a comparison would use.

The repository already treats current projections as current/read views rather
than source truth. A current state can be one side of a comparison, but it does
not answer why the other side is meaningful. If current state says a mount is no
longer visible, the remaining question is still:

```text
no longer visible compared to which prior or alternate reference?
```

Thus:

```text
current state
    = current projected representation

candidate baseline
    = possible reference condition used to interpret difference
```

Current state can diverge from a candidate baseline without implying violation.
The divergence may only create investigation pressure.

## Difference from accepted baseline

Repository evidence supports an authority boundary between candidate and accepted
baseline. Prior reconciliation says decision is the cleanest transition that can
carry selected comparison authority, while accepted baseline is the scoped effect
of that selection rather than an independent authority primitive.

Therefore:

```text
candidate baseline
    = plausible reference under consideration

accepted baseline
    = authority-selected comparison reference for a scope
```

The distinction matters because a candidate can be useful before it is accepted.
For example, repeated historical visibility can make `host saw mount M` a
candidate reference for an investigation. It does not by itself prove that this
reference has been selected as the authoritative comparison point for the work.

## Difference from expectation

Expectation requires should-bearing or anticipation-bearing authority. Candidate
baseline does not.

A candidate baseline can say:

```text
this historical condition is a plausible reference for comparison
```

It cannot say:

```text
this condition should continue
```

without additional authority such as policy, requirement, declared operator
intent, accepted goal-to-condition relation, design invariant, or another
normative source. Repository evidence repeatedly warns against silently upgrading
history, visibility, continuity, or baselines into expectation.

Therefore:

```text
expectation
    = authority-backed should / anticipated condition

candidate baseline
    = possible comparison reference that may help investigate significance
```

## Difference from concern

Concern is the pressure or significance signal that something may deserve
attention. Candidate baseline is the possible reference that makes a deviation
legible.

Concern can arise when current observation deviates from a candidate baseline,
even if no expectation exists. For example, if a host historically saw a mount
and no longer does, that can create concern as ambiguity, visibility change, or
operator-significant pressure. It does not require a claim that the host should
see the mount.

Thus:

```text
candidate-baseline deviation
    can support concern
    without proving expectation violation
```

Concern also can arise without candidate baseline, such as direct operator pain,
explicit policy failure, stale evidence, contradiction, or missing support. So
candidate baseline is not the general definition of concern.

## Relationship to continuity

Continuity contributes evidence. It does not itself select a comparison
reference.

Supported distinction:

```text
continuity
    = persistence, recurrence, or survival across observations

candidate baseline
    = continuity or other evidence interpreted as a plausible reference
```

Continuity is especially relevant because repeated observation can make a prior
condition more plausible as a comparison reference than a one-off observation.
But repository evidence does not support an automatic threshold where recurrence
becomes a baseline. Any such threshold would be policy or implementation design,
which is outside this investigation.

Continuity therefore contributes:

- provenance for historical comparison;
- recurrence strength;
- stability evidence;
- a reason a reference may be meaningful;
- confidence limits and caveats.

Continuity does not contribute:

- acceptance;
- should authority;
- ownership;
- remediation authority;
- automatic significance.

## Relationship to selection

Selection-path work answers why a conclusion was selected. Candidate-baseline
pressure resembles a neighboring question:

```text
why would this comparison reference be selected?
```

The analogy is strong but bounded.

Selection rationale already exists in distributed form through deterministic
selection rules, ordering keys, projection fields, support groups, confidence
reasons, contradiction records, graph issue records, inventory reasons, and
budget trace accounting. Those surfaces can explain many inclusion, ordering,
and currentness decisions. Candidate baseline asks for the same kind of support
path, but for comparison-reference candidacy rather than conclusion selection.

Therefore candidate baseline appears to be a traceability problem of **reference
selection pressure**:

```text
evidence candidates
    -> continuity / source / scope / confidence / limitations
    -> candidate comparison reference
    -> possible authority selection later
```

Current selection traceability can explain why a conclusion was included or
selected. It does not fully explain why a particular comparison reference is the
meaningful one unless that reference is already represented as a selected
conclusion in an existing surface.

## Relationship to authority

Authority contributes at two separate boundaries.

First, evidence/source authority affects whether a candidate baseline is credible
enough to consider. A candidate supported by durable repeated observation,
explicit source provenance, and known confidence limits is stronger than an
uncited assertion.

Second, selection authority affects whether a candidate becomes accepted for a
scope. Repository evidence currently supports this as a decision-like transition,
not as an automatic property of history.

The authority shape is therefore:

```text
evidence authority
    supports candidate plausibility

selection authority
    accepts a reference for comparison

should-bearing authority
    creates expectation
```

These are distinct. Collapsing them would overclaim repository evidence.

## Relationship to existing traceability work

### `reasoning_path`

`reasoning_path` can explain how operational conclusions are derived from
implemented diagnostics and how those conclusions are consumed. It is strong for
`Why does this conclusion exist?` It does not by itself name the comparison
reference used to decide whether a change is significant unless that reference is
already part of the diagnostic derivation.

### `selection_path`

`selection_path` addresses why a conclusion or work item was selected. Candidate
baseline is analogous but not identical: it asks why a comparison reference is a
plausible or selected reference. Existing selection traceability helps frame the
question, but it does not eliminate the reference-selection gap.

### `history_brief`

`history_brief` is closest to the candidate-baseline pressure because it combines
impact, snapshot policy, repository context, historical confidence, and
unsupported conclusions. It can say what changed and how confident the historical
comparison is. It still stops short of declaring a general comparison-reference
concept.

### `snapshot_policy`

`snapshot_policy` can say whether snapshots exist and whether comparison is
available. It cannot say which comparison is meaningful without a scoped question
and supporting authority.

### `impact_audit`

`impact_audit` compares captured audit outputs and reports changes. It depends on
available before/after artifacts. It can surface change but not fully answer why
that before artifact is the meaningful reference for the operator's question.

### `operational_story`

`operational_story` composes operational pressure from existing diagnostics. It
can make change and impact understandable, but it does not create baseline,
accepted baseline, or expectation authority.

### `architecture_conformance`

`architecture_conformance` compares architecture evidence with observed
operational graph structure. It shows that comparison can be meaningful when a
reference domain and authority are already present. That supports the broader
point: comparison needs a reference and an authority boundary.

### `repository_observation`

`repository_observation` supports source-file and repository-context evidence. It
can provide implementation-backed observations that a concept, diagnostic, or
artifact exists. It does not by itself promote presentation vocabulary into
knowledge or choose a baseline.

### `unified_derivation_architecture_investigation`

The unified derivation investigation supports the traceability framing: Seed
reuses derivation mechanics across domains while keeping authority models
separate. Candidate baseline fits this pattern as a possible intermediate
representation: evidence is preserved, a reference candidate is derived, and any
acceptance or expectation must remain authority-specific.

## Core question answers

### Does candidate baseline represent a missing traceability layer?

Yes, with caveats. Repository evidence supports candidate baseline as the missing
traceability layer for **comparison-reference candidacy**:

```text
Why is this a plausible reference to compare against?
```

It is not a missing storage layer, runtime layer, diagnostic surface, ontology
layer, or policy layer.

### Can current traceability explain change without explaining reference selection?

Yes. Impact, snapshot, history, reasoning, and story surfaces can explain that a
change occurred and why a conclusion exists. They can still leave unresolved why
the chosen reference is meaningful rather than merely available.

### Can historical significance exist without a comparison reference?

Only weakly. A historical event can be described without a comparison reference,
but significance of change usually requires a reference, scope, or concern. The
repository evidence supports treating comparison-reference selection as
load-bearing when the operator asks whether a change matters.

### Can comparison references exist without authority?

Candidate references can exist with evidence/source support, but accepted
comparison references require selection authority. A raw candidate can be
considered without being accepted. An accepted baseline cannot be justified by
mere existence of evidence.

### Can concern arise from candidate-baseline deviation without expectation?

Yes. Repository evidence already supports concern from ambiguity, visibility
change, stale support, degraded evidence quality, and operator pressure without
requiring expectation. Candidate-baseline deviation is one such concern source.

## Supported conclusions

1. Candidate baseline is distinct from snapshot.
2. Candidate baseline is distinct from current state.
3. Candidate baseline is distinct from accepted baseline.
4. Candidate baseline is distinct from expectation.
5. Candidate baseline is distinct from concern, though it can contribute to
   concern.
6. Continuity can support candidate-baseline plausibility.
7. Authority is required to move from candidate baseline to accepted baseline.
8. Separate should-bearing authority is required to move from accepted baseline
   or candidate-baseline deviation to expectation.
9. Candidate baseline appears to answer the unresolved traceability question:
   `Compared to what?`
10. Existing traceability can explain change, conclusion derivation, selection,
    history confidence, and operational story without fully explaining
    comparison-reference candidacy.

## Unsupported conclusions

Current repository evidence does not support concluding that:

- candidate baselines are implemented;
- accepted baselines are implemented as a general repository concept;
- expectation systems should be implemented;
- historical continuity automatically becomes baseline;
- candidate baseline automatically becomes accepted baseline;
- accepted baseline automatically becomes expectation;
- snapshots are baselines;
- current state is a baseline;
- concern requires expectation;
- candidate baseline should introduce storage, projections, diagnostics,
  runtime behavior, policy, ontology, or architecture changes.

## Open questions

1. What minimum evidence makes a comparison reference worth naming as a
   candidate rather than leaving it as raw history?
2. How should competing candidate references be compared without implementing a
   new selection system?
3. Which existing surfaces, if any, already carry enough scoped reference
   information for specific domains?
4. When a reference is selected by an operator or decision, where is that
   authority trail currently preserved, if anywhere?
5. Can a future investigation describe candidate-baseline evidence shapes without
   turning them into implementation requirements?
6. How should candidate-baseline deviation be discussed so it can support concern
   without implying expectation violation?

## Acceptance answer

Candidate baseline is a distinct repository concept at the investigation level:
it is not implemented as a general system, but repository evidence supports it as
a useful boundary-preserving name for a plausible comparison reference.

It does represent the missing answer to:

```text
Compared to what?
```

more precisely:

```text
What evidence-supported comparison reference is plausible for this bounded
question, before any authority accepts it or turns it into a should-bearing
expectation?
```

It is therefore the next unresolved traceability layer if the traceability stack
is concerned with comparison-reference candidacy. Existing concepts explain parts
of the pressure but do not fully replace it:

- snapshot explains captured evidence;
- current state explains current projection;
- continuity explains persistence;
- selection explains selected conclusions or items;
- accepted baseline explains authority-selected reference;
- expectation explains should-bearing authority;
- concern explains significance pressure.

Candidate baseline names the gap between continuity evidence and authority
selection. That gap is exactly where `Compared to what?` remains unresolved.
