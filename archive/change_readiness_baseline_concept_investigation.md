---
status: investigation
scope: baseline, continuity, expectation, acceptance, authority, and Change Readiness pre-implementation review
created: 2026-06-21
---

# Change Readiness Baseline Concept Investigation

## Status

Investigation only. This document does not introduce ontology, implement Change
Readiness, create a visibility surface, prescribe runtime behavior, prescribe
architecture changes, add diagnostics, add schemas, add tests, or change
projection behavior.

Repository authority wins over this document. The purpose is to determine
whether future Change Readiness work should build on an existing
baseline/continuity/expectation/acceptance concept instead of assuming that
snapshots alone are enough.

Short answer: repository evidence supports a richer emerging concept than
`preserve observations -> compare later`. The supported distinction is:

```text
snapshot
    = captured or cached state/evidence at a point or ledger position

candidate baseline
    = evidence-supported possible comparison reference for a bounded question

accepted baseline
    = authority-selected comparison reference for a scoped purpose

expectation
    = separate should-bearing or anticipation-bearing authority that a condition
      should hold, continue, or be treated as expected
```

The repository does **not** currently contain a general implemented baseline
system for operational topology, nor does it authorize Change Readiness as a new
surface yet. It does contain repeated investigation authority saying that
historical comparison, change significance, and operator concern require more
than captured snapshots when the question is `why is this meaningful?`.

## Investigation question

The proposed Change Readiness goal was:

```text
Before a change occurs,
what evidence should be preserved,
why is it valuable,
and what future understanding would it enable?
```

This investigation asks whether that goal can be answered safely by snapshots
alone, or whether repository history already points to:

```text
baseline
    -> continuity
    -> expectation
    -> accepted reference state
```

The answer is bounded: this document investigates meaning and authority only. It
does not choose implementation, storage, CLI, diagnostic, or runtime behavior.

## Repository evidence reviewed

Required investigation materials reviewed:

- `docs/baseline_acceptance_authority_audit.md`
- `docs/baseline_continuity_expectation_audit.md`
- `docs/candidate_baseline_accepted_baseline_expectation_audit.md`
- `docs/observation_visibility_continuity_baseline_expectation_concern_reconciliation.md`

Directly related materials reviewed through repository navigation:

- `docs/visibility_expectation_concern_branch_closure_reconciliation.md`
- `docs/should_authority_expectation_audit.md`
- `docs/goal_policy_and_operator_authority_reconciliation.md`
- `docs/lens_view_reconciliation.md`
- `docs/continuity_frontier.md`
- `docs/observation_refresh_and_knowledge_freshness_reconciliation.md`
- `docs/temporal_reasoning_audit.md`
- `docs/state.md`
- `docs/invariants.md`
- `docs/unified_derivation_architecture_investigation.md`
- `docs/pressure_audit_design_audit.md`
- `docs/selection_rationale_vocabulary.md`
- `docs/selection_rationale_reconciliation.md`
- `docs/movement_preservation_observation.md`
- `docs/interaction_temporalness_observation.md`

Implementation and test evidence reviewed where it clarified recent operational
surfaces and snapshot boundaries:

- `seed_runtime/impact_audit.py`
- `seed_runtime/history_brief.py`
- `seed_runtime/snapshot_policy_audit.py`
- `seed_runtime/reasoning_path_audit.py`
- `seed_runtime/selection_path_audit.py`
- `seed_runtime/operational_story.py`
- `seed_runtime/repository_observation.py`
- `seed_runtime/architecture_conformance_audit.py`
- `seed_runtime/projection_store.py`
- `seed_runtime/diagnostic_inventory.py`
- `tests/test_impact_audit.py`
- `tests/test_history_brief.py`
- `tests/test_snapshot_policy_audit.py`
- `tests/test_reasoning_path_audit.py`
- `tests/test_selection_path_audit.py`
- `tests/test_operational_story.py`

## Baseline-related observations

### 1. Baseline is not currently a general implemented operational concept

The strongest prior audits explicitly avoid claiming that Seed already has a
general operational baseline implementation. The repository has no discovered
runtime object, storage path, diagnostic, or projection model that acts as a
general accepted baseline for operational topology.

Therefore, future work must not say:

```text
Seed already implements Change Readiness baselines.
```

The supported statement is narrower:

```text
Seed has an investigated and recurring baseline concept boundary.
```

### 2. Baseline is not the same as snapshot

Repository evidence supports this distinction:

```text
snapshot
    = captured state, cached projection, or audit artifact

baseline
    = selected or candidate reference condition for comparison
```

Projection snapshots are latest-current cache artifacts keyed by event identity
and projection identity. They are not an as-of historical API and do not own the
event ledger. Audit snapshots preserve outputs that can later be compared, but
an audit snapshot by itself does not say which captured condition is meaningful,
accepted, expected, or authoritative.

A snapshot can provide evidence for a baseline candidate. It is not itself the
baseline unless some scoped comparison question frames it as a reference, and it
is not an accepted baseline unless an authority selects it for that purpose.

### 3. Baseline is not the same as current state

Current state answers what Seed currently projects after replaying events under
current projection semantics. Baseline answers what should be used as a
reference point for a comparison question. Those can coincide, but they have
different authority shapes.

Examples:

- a current projection can be used as a future baseline candidate;
- a historical observation can be used as a baseline candidate even when it is no
  longer current;
- an accepted baseline can remain the comparison reference even after current
  state changes;
- current state does not automatically become expected state.

This matters for Change Readiness because preserving current state before a
change does not by itself answer why that state is meaningful. It only preserves
a possible input to future meaning.

### 4. Candidate baseline is evidence plus comparison purpose

Prior investigations converge on candidate baseline as stronger than raw
continuity and weaker than accepted baseline. Candidate baseline means a
historical or observed condition is plausibly useful as a comparison reference
for a bounded question.

A candidate baseline requires at least:

1. evidence of prior observation, recurrence, support, or currentness;
2. a comparison question;
3. a reason the condition might matter for that question;
4. caveats that it is not yet normative.

This is the first place where Change Readiness becomes more than snapshotting.
It asks not only `what was captured?`, but `what future comparison could this
capture support?`.

## Continuity-related observations

Continuity answers:

```text
what persisted, recurred, survived, or remained visible across observations?
```

It is interpretive over evidence. It is stronger than one observation and weaker
than an expectation. Continuity can explain why a current disappearance might be
worth noticing, but it cannot by itself authorize a should-claim.

For Change Readiness, continuity has two implications:

1. one snapshot is weak evidence for future meaningful comparison;
2. repeated or historically stable observations can support stronger candidate
   baselines, but still require selection and authority before becoming accepted
   baselines or expectations.

Therefore, historical comparison can use snapshots, but meaningful historical
comparison requires continuity interpretation or another reference-selection
mechanism.

## Expectation-related observations

Expectation is the repository's protected boundary. Prior work repeatedly warns
that history alone must not become `should continue`.

The supported definition is:

```text
expectation
    = an authority-backed stance that a condition should hold, should continue,
      or should be anticipated under a named authority path
```

Expectation can be supported by a declared requirement, policy, operator intent,
invariant, accepted goal-to-condition relation, or future approved baseline
promotion mechanism. It is not created merely by:

- repeated observation;
- a current snapshot;
- audit-snapshot comparison;
- visibility loss;
- operator surprise;
- accepted baseline selection, unless a distinct should-bearing authority is
  also present.

For Change Readiness, this means a readiness document or surface must not imply
that preserved evidence identifies required future conditions unless the
repository has separate authority for that implication.

## Acceptance and authority observations

### Acceptance

Acceptance is a selection boundary, not a truth-making boundary. Prior audits use
implemented analogues such as proposal acceptance, decision selection,
recommendation decisions, and promotion boundaries to show a general repository
pattern:

```text
candidate
    ? selection authority
    -> accepted-for-this-scope
```

For baselines, the safest repository-supported interpretation is:

```text
accepted baseline
    = authority-selected comparison reference for a scoped question,
      investigation, decision context, view, or continuation context
```

Acceptance does not automatically mean:

- the reference is true now;
- the reference is required;
- the reference is owned;
- deviation is an alert;
- remediation is authorized;
- execution is authorized.

### Authority

The repository distinguishes several authority types that future baseline work
must not collapse:

| Authority | What it can authorize | What it cannot silently authorize |
| --- | --- | --- |
| Observation/source authority | what was reported from a source/vantage point | ownership, requirement, expectation, remediation |
| Projection authority | latest-current derived State under projection rules | historical as-of truth, accepted reference selection |
| Snapshot/cache authority | reproducible captured output or cache state | meaning, expectation, comparison relevance |
| Investigation/view authority | scoped framing and comparison purpose | global truth, policy, execution |
| Operator/decision authority | selection, acceptance, prioritization in scope | unsupported facts or hidden runtime mutation |
| Policy/requirement/invariant authority | should-bearing constraints inside scope | arbitrary history-derived expectations |

This authority separation is the core reason snapshots are not enough.

## Concern and reconciliation

Concern is the bridge from observed difference to operator-significance without
requiring expectation. The repository supports concern arising from:

- visibility change;
- continuity break;
- candidate-baseline deviation;
- accepted-baseline deviation;
- expectation violation;
- ambiguity;
- stale or degraded evidence;
- operator investigation pressure.

Concern allows Seed to say a difference may matter without saying the previous
condition was owned, required, or wrong to lose. Reconciliation documents matter
because they keep these concepts from collapsing:

```text
visibility loss
    ≠ ownership loss
    ≠ expectation violation
    ≠ alert
    ≠ remediation authority
```

A future Change Readiness effort should preserve this reconciliation discipline.
It should identify what future concern or comparison a preserved evidence bundle
could support, while remaining explicit about whether that concern is based on
candidate baseline, accepted baseline, expectation, or only raw change.

## Relationship to recent operational work

Recent operational surfaces answer important questions but stop before the
baseline/expectation boundary.

| Surface | What it primarily answers | Relationship to baseline concept |
| --- | --- | --- |
| `history_brief` | What changed, what appears stable, and how trustworthy the available history is | Uses snapshots and repository observation to summarize history, but does not select accepted baselines or create expectations. |
| `snapshot_policy` | Which surfaces are snapshot-ready or comparison-ready | Evaluates preservation/comparison readiness, not meaning authority. |
| `impact_audit` | What observable outcomes changed across supported audit snapshots | Compares captured outputs; impact classification remains constrained by snapshot coverage. |
| `reasoning_path` | Why a conclusion exists and which evidence/intermediate conclusions support it | Supports derivation traceability; can explain comparison reasoning if baseline authority exists elsewhere. |
| `selection_path` | Why one item was selected over alternatives | Provides an analogue for accepted-baseline selection, but does not itself define baseline authority. |
| `operational_story` | How operational evidence forms a narrative of current focus/pressure | Can make concern legible without creating expectation. |
| `repository_observation` | What repository evidence is currently visible | Supports source/evidence context, not accepted operational reference state. |
| `architecture_conformance` | Whether implementation conforms to documented architecture expectations | Uses explicit architecture authority; not a general operational baseline mechanism. |

Together, these surfaces answer:

```text
What changed?
Why does this conclusion exist?
Why was it selected?
How trustworthy is history?
```

They do not fully answer:

```text
Why is this change meaningful?
Meaningful relative to what?
```

That remaining question is exactly where baseline, continuity, expectation,
acceptance, and authority become relevant.

## Are snapshots enough?

No, not for the Change Readiness question as stated.

Snapshots are enough to preserve captured outputs for later inspection or
comparison when the relevant surface supports snapshotting. They are not enough
to determine:

- which captured condition should be the comparison reference;
- whether the reference was stable or merely incidental;
- whether the reference has been accepted for this investigation;
- whether deviation is meaningful;
- whether deviation violates an expectation;
- whether a future operator should care;
- whether any action is authorized.

The repository's safer chain is:

```text
observation / snapshot evidence
    -> continuity evidence where available
    -> candidate baseline for a bounded question
    ? authority selection
    -> accepted baseline for that scope
    ? should-bearing authority
    -> expectation
    -> concern / reconciliation / decision support
```

This chain is not fully implemented. It is, however, strongly supported as an
investigation boundary by existing repository documents.

## Supported conclusions

1. The repository has an emerging baseline concept, but not a general baseline
   implementation.
2. Baseline is distinct from snapshot. A snapshot is captured evidence or cache;
   a baseline is a comparison-reference concept.
3. Baseline is distinct from current state. Current state is latest projection;
   baseline is reference selection for comparison.
4. Continuity supports baseline candidacy by showing recurrence or persistence,
   but continuity does not create expectation.
5. Candidate baseline is evidence-supported and purpose-framed, but not accepted
   or normative.
6. Accepted baseline requires authority selection for scope and purpose.
7. Accepted baseline does not automatically create expectation.
8. Expectation requires distinct should-bearing or anticipation-bearing authority.
9. Concern can exist before expectation and can make visibility changes
   operator-significant without creating ownership, alerting, or remediation
   authority.
10. Recent operational surfaces improve historical comparison, derivation,
    selection, and trust visibility, but they do not replace the baseline and
    authority questions.

## Unsupported conclusions

The reviewed evidence does not support these claims:

1. Seed already has a general Change Readiness concept.
2. Seed already has first-class accepted operational baselines.
3. Audit snapshots are baselines by default.
4. Current state is a baseline by default.
5. Historical continuity automatically creates an expectation.
6. Accepted baseline automatically means `should continue`.
7. Concern requires expectation.
8. Meaningful change can be determined from snapshot comparison alone in all
   cases.
9. A future Change Readiness surface can safely skip authority and acceptance
   boundaries.

## Open questions

1. Should baseline become a first-class repository concept, or remain an
   investigation vocabulary used by specific future surfaces?
2. If implemented later, should candidate baselines be derived from audit
   snapshots, event-ledger history, projected State, repository observations,
   operator declarations, or a combination?
3. What authorities may accept a baseline: operator decision, work item,
   investigation scope, policy, requirement, architecture invariant, or view
   configuration?
4. Should accepted baselines be persisted, or should they be derivable from
   accepted decisions/work-position artifacts?
5. How should an accepted baseline expire, be superseded, be rejected, or become
   stale?
6. What would prove continuity strongly enough to recommend a candidate baseline
   without overstating authority?
7. How should future Change Readiness distinguish preservation value from
   expectation value?
8. Can a readiness bundle say `preserve this because it may support future
   comparison` without implying `this condition should continue`?
9. How should concern be rendered when a current state deviates from a candidate
   baseline but no accepted baseline or expectation exists?
10. What tests would prove that a future surface preserves `record_scope` and
    `mutates_cluster=false` while staying outside cluster truth?

## Guidance for future Change Readiness work

Future work should not introduce Change Readiness directly as a generic
snapshot-preservation surface. It should first decide whether it is working with:

```text
snapshot preservation
candidate baseline discovery
accepted baseline selection
expectation declaration
concern rendering
```

Those are different authority levels. A safe future path would be to build on
the repository's existing chain instead of bypassing it:

```text
preserve evidence
    -> explain comparison value
    -> identify candidate baseline candidates
    -> expose authority gaps
    -> only later support accepted baselines or expectations if explicit
       authority exists
```

The immediate repository-backed conclusion is therefore:

```text
Snapshots are necessary inputs for some historical comparison,
but they are not sufficient for Change Readiness meaning.

Future work should build on the baseline / continuity / expectation /
acceptance authority concept rather than introducing Change Readiness as a
snapshot-only idea.
```
