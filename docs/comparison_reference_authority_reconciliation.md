---
status: reconciliation
scope: comparison-reference selection authority reconciliation
created: 2026-06-18
---

# Comparison Reference Authority Reconciliation

## Status

Investigation only. This document does not implement baselines, expectations,
investigations, decision workflows, current-work-position changes, handoff
behavior, HomeOps, SeedOps, storage, schemas, projections, runtime behavior,
operator surfaces, policy behavior, tests, or ontology.

Repository authority wins over this reconciliation. This document builds on prior
findings and does not rediscover already-established conclusions unless needed to
resolve the narrower question of what legitimately carries selected comparison
authority.

Short answer:

```text
Decision is the cleanest authority-bearing transition.
Accepted Baseline is the comparison-reference state/effect produced by that
transition within a scope.
Investigation Context scopes the transition and gives it purpose.
Current Work Position preserves the active orientation created by the transition.
Handoff Context preserves and transfers that orientation and its authority trail;
it does not invent authority.
```

Therefore, `accepted baseline` is real enough as architectural vocabulary for a
selected comparison reference, but not real as an independent authority primitive
that can replace decision, operator/policy authority, investigation scope, or
handoff lineage.

The safest reconciliation is:

```text
candidate comparison reference
    -> authorized selection decision within investigation/scope
    -> accepted baseline as scoped selected-reference state
    -> current work position may orient work around that selected reference
    -> handoff may preserve the selected reference, rationale, and authority trail
```

This preserves the existing chain:

```text
Observation
    -> Visibility
    -> Continuity
    -> Candidate Baseline
    ? authority selection
    -> Accepted Baseline
    ? should-bearing authority
    -> Expectation
```

without turning accepted baseline into truth, ownership, expectation, alerting,
policy, remediation, execution authority, or a storage mechanism.

## Purpose

The purpose of this reconciliation is to determine what repository concept
legitimately carries selected comparison authority.

It compares:

```text
Decision
Accepted Baseline
Current Work Position
Investigation Context
Handoff Context
```

and asks whether accepted baseline is genuinely new architecture or an existing
repository authority pattern viewed through baseline vocabulary.

The operational example used throughout is:

```text
example_host_b historically sees mount M
example_host_b no longer sees mount M
historical example_host_b-sees-M appears useful for comparison
a comparison reference is selected
the investigation continues across sessions and participants
```

## Prior findings reconciled

Required documents reconciled:

- `docs/observation_visibility_continuity_baseline_expectation_concern_reconciliation.md`
- `docs/baseline_acceptance_authority_audit.md`
- `docs/should_authority_expectation_audit.md`
- `docs/current_work_position_frontier.md`
- `docs/handoff_and_continuation_lineage_frontier.md`
- `docs/handoff_consumption_activation_reconciliation.md`
- `docs/assessment_recommendation_and_decision_reconciliation.md`
- `docs/adoption_decision_authority_reconciliation.md`
- `docs/lens_view_reconciliation.md`

The prior findings are compatible:

1. Observation, visibility, and continuity are evidence-facing or interpretive;
   they do not create should-authority.
2. A candidate baseline is an evidence-supported possible comparison reference.
3. An accepted baseline, if recognized, is a selected comparison reference for a
   scoped question, investigation, decision context, view, or continuation
   context.
4. Accepted baseline is not truth and not expectation.
5. Expectation requires a separate should-bearing authority.
6. Recommendations suggest; decisions select; commands request; actions mutate.
7. Current Work Position is not established ontology, but it explains why
   continuation needs preserved orientation rather than merely preserved
   information.
8. Handoff preserves selected active context and continuation lineage; handoff
   availability, consumption, activation, and compliance remain distinct.
9. Lens/view language can scope interpretation and presentation, but views do
   not invent authority.
10. Adoption-decision findings reinforce that durable selected-reference effects
    should remain distinct from recommendation, verification, execution, and
    runtime dispatch.

## Candidate concepts

| Concept | Repository role in this reconciliation | Authority-bearing? | Primary boundary |
| --- | --- | --- | --- |
| Decision | Authority-bearing selection among alternatives or lifecycle outcomes. | Yes, when backed by operator, policy, delegated, or explicit workflow authority. | Decision selects; it does not itself execute or prove the world. |
| Accepted Baseline | Scoped state/effect/name for the selected comparison reference. | Authority-bearing as a selected-reference state, but derivative rather than self-originating. | Acceptance is comparison authority only, not expectation. |
| Current Work Position | Selected, bounded, continuation-relevant orientation of ongoing work. | Usually no independent authority; may include authority-bearing selections as part of orientation. | Position orients work; it does not by itself authorize selection unless tied to an upstream decision/authority. |
| Investigation Context | Scoped question, purpose, evidence set, and active inquiry frame. | Scoping authority; selection authority only when the investigation includes an authorized decision or operator/policy acceptance. | Context defines where a selected reference applies. |
| Handoff Context | Continuation artifact/lineage preserving active subset, rationale, boundaries, and next safe move. | Preservation authority, not originating authority. | Handoff transfers context and authority trail; it does not invent acceptance. |
| Lens/View | Bounded interpretation or presentation over projected State or repository knowledge. | No independent authority. | Views can expose selected references and caveats but cannot create them. |

## Authority analysis

Selected comparison authority has two separable parts:

```text
selection authority
scope authority
```

Selection authority answers:

```text
Who or what selected reference R over alternatives?
```

Scope authority answers:

```text
For what question, investigation, view, time, participant set, or continuation
purpose does the selection apply?
```

A decision most cleanly carries the selection transition because the repository
already treats decisions as authority-bearing selections. Investigation context
most cleanly carries the scoped purpose. Accepted baseline names the selected
reference after the transition. Current Work Position preserves how that
selection orients ongoing work. Handoff Context preserves enough of the selected
reference, rationale, and authority trail for another participant to continue
without re-deciding or over-promoting it.

The important distinction is:

```text
authority origin != authority state != orientation preservation != context transfer
```

For example_host_b:

```text
historical example_host_b-sees-M = evidence-supported candidate reference
decision/operator selection = authority transition
accepted baseline = selected reference for this investigation
current work position = continue from the example_host_b visibility-change comparison
handoff context = preserve that selected comparison and its limits for the next participant
```

## Example host operational example

### Evidence progression

```text
example_host_b historically sees mount M
example_host_b no longer sees mount M
```

This supports:

- observation evidence;
- visibility difference;
- possible continuity break;
- candidate baseline: historical example_host_b-sees-M may be useful for comparison.

It does not by itself support:

- example_host_b owns mount M;
- example_host_b should see mount M;
- missing M is a policy violation;
- M exists now;
- remediation is authorized.

### Selection moment

A legitimate selection moment would be:

```text
decision: use historical example_host_b-sees-M as comparison reference R
for investigation I into why example_host_b no longer sees mount M
```

That decision may be made by an operator, delegated decision process, policy rule
that explicitly authorizes the selection, or another repository-recognized
authority. The decision creates comparison-reference selection authority only
inside its scope.

### After selection

After the selection:

```text
accepted baseline: R is the selected comparison reference for I
```

The accepted baseline is not a new fact about the environment. It is a scoped
selected-reference state.

### During continuation

As work continues:

```text
current work position: the active investigation is oriented around comparing
current example_host_b mount visibility against R, while preserving the boundary that R
is not an expectation.
```

A handoff may then say:

```text
continue investigation I using R as the selected comparison reference; do not
reinterpret R as proof, ownership, expectation, or remediation authority; validate
current repository state before continuing.
```

The handoff preserves the selected comparison context. It does not create it.

## Decision analysis

Decision is the strongest candidate for carrying selected comparison authority.

Repository decision findings say decisions select among alternatives or lifecycle
outcomes, while recommendations are advisory and commands/actions are later
mutation-facing concepts. That maps directly to comparison-reference selection:

```text
recommendation: historical example_host_b-sees-M looks useful for comparison
selection: choose historical example_host_b-sees-M over other references
decision: authorized selection of that reference for investigation I
acceptance: resulting selected-reference state
```

A decision can carry acceptance when it records:

- selected reference;
- rejected or deferred alternatives when relevant;
- authority source;
- scope;
- rationale;
- constraints and caveats;
- non-promotion boundaries, especially that comparison authority is not
  expectation authority.

Decision is not sufficient by mere naming. A document sentence called
`decision` has authority only if it sits inside delegated, operator, policy,
workflow, or other recognized authority. Otherwise it is just prose describing a
candidate selection.

### Model A: Decision Carries Acceptance

Model A is largely correct if read narrowly:

```text
authorized decision selects reference R
accepted baseline is the resulting selected-reference state
```

It is unsafe if read as:

```text
any decision-shaped prose automatically creates accepted baseline authority
```

Decision carries the authority transition; accepted baseline names what exists
after the transition.

## Baseline analysis

Accepted Baseline is useful because it names the thing that is selected:

```text
the comparison reference now accepted for a scoped purpose
```

It prevents overloading candidate baseline with two meanings:

```text
possible reference
selected reference
```

It also prevents overloading decision with persistent state:

```text
selection event/transition
selected-reference state used by later work
```

However, Accepted Baseline should not be treated as an independent authority
origin. It does not select itself. It is derivative of an upstream authorized
selection.

Accepted baseline represents a hybrid of:

```text
state: selected-reference state within a scope
selection: the selected object of comparison
authority: derivative comparison authority created by an authorized selection
context: scoped to an investigation/question/view/continuation purpose
orientation: often used by current work position and handoff, but not identical to them
```

It does not represent:

```text
truth
ownership
expectation
requirement
alert
remediation authorization
execution authorization
global environment baseline
```

### Model B: Accepted Baseline Is Independent

Model B is partly correct and partly too strong.

Correct:

```text
accepted baseline is a distinct architectural vocabulary item from decision
because it names the selected comparison reference after selection.
```

Too strong:

```text
accepted baseline is not an independent authority primitive that can exist
without any authority trail, scope, or selection act.
```

## Current-work-position analysis

Current Work Position describes where work is oriented. It may include what was
selected and why it was selected, but its distinctive role is not selection
itself. Its distinctive role is continuation-relevant orientation:

```text
what is active
why it is active
what remains unresolved
which boundaries constrain movement
what next move is safe
```

For example_host_b, current work position might be:

```text
active inquiry: example_host_b visibility changed with respect to mount M
selected comparison: historical example_host_b-sees-M
boundary: selected comparison is not expectation
next safe move: compare current evidence against R and inspect evidence quality
```

This can carry the accepted baseline as part of orientation, but it does not
legitimately originate selected comparison authority unless the current-work
position itself includes or points to an upstream authorized decision.

### Model C: Current Work Position Carries Acceptance

Model C is useful but incomplete.

Current Work Position can preserve acceptance operationally because it preserves
which reference is active and why. But it should not be the authority origin.
Otherwise an exploratory orientation could silently become a repository decision.

The boundary-preserving reading is:

```text
current work position carries the active use of an accepted baseline;
it does not independently accept the baseline.
```

## Investigation-context analysis

Investigation Context is the natural scope for comparison-reference selection.
It answers:

```text
What question is being investigated?
What evidence is in play?
What comparison is useful for this inquiry?
Which boundaries prevent over-promotion?
```

For example_host_b:

```text
investigation I = why example_host_b no longer sees mount M
candidate R = historical example_host_b-sees-M
accepted baseline for I = R selected as comparison reference
```

Investigation Context can make a selection meaningful and bounded. But context
alone is not selection. An investigation may contain multiple candidate
references without accepting any of them.

### Model D: Investigation Context Carries Acceptance

Model D is correct if it means:

```text
acceptance belongs to a scoped investigation after an authorized selection
```

It is incorrect if it means:

```text
opening or naming an investigation automatically accepts one historical reference
```

Investigation context is the best home for the scope of accepted baseline, not
necessarily the authority origin.

## Handoff-context analysis

Handoff Context is primarily preservation and continuation lineage. It preserves:

- selected active subset;
- selection rationale;
- authoritative references;
- unresolved tensions;
- boundaries;
- validation requirements;
- next safe moves;
- activation instructions.

For example_host_b, a handoff can preserve:

```text
Use historical example_host_b-sees-M as the selected comparison reference for this
investigation because decision D selected it. Do not treat it as expectation.
```

The handoff helps the selection survive participant turnover. It does not make
the selection legitimate by itself. A handoff that says `R is accepted` without
an authority trail should be read as preserving claimed context that needs
validation, not as creating acceptance.

### Model E: Handoff/Continuation Carries Acceptance

Model E is correct about survival and incorrect about origin.

Handoff/continuation carries acceptance across sessions by preserving active
context and authority trail. It does not create comparison-reference selection
authority unless the handoff itself is also an authorized decision artifact,
which current repository evidence does not establish as a general rule.

## Boundary preservation analysis

### Recommendation, decision, selection, acceptance

Under repository authority:

| Term | Meaning | Example host example |
| --- | --- | --- |
| Recommendation | Advisory suggestion; what could be considered. | Historical example_host_b-sees-M appears useful for comparison. |
| Selection | The act or result of choosing one reference among alternatives. | Choose historical example_host_b-sees-M rather than another host, cluster, or time window. |
| Decision | Authority-bearing selection or lifecycle disposition. | Authorized decision selects historical example_host_b-sees-M for investigation I. |
| Acceptance | The selected-reference/lifecycle state after an authorized selection. | Historical example_host_b-sees-M is the accepted baseline for I. |

Selection can be descriptive if merely observed in prose. Decision is selection
with authority. Acceptance is the accepted state/effect, not necessarily the act.

### Can a decision exist without an accepted baseline?

Yes. Many decisions do not select comparison references:

```text
reject a plan
defer a recommendation
approve a log inspection
select manual handoff
mark evidence insufficient
```

A decision exists without an accepted baseline when its selected outcome is not a
comparison reference.

### Can an accepted baseline exist without a decision?

Only if another recognized authority performs the selection. Examples could
include explicit operator selection, explicit policy selection, or requirement
language that directly names the comparison reference for a scope.

But an accepted baseline cannot legitimately exist without any authority-bearing
selection. If no decision/operator/policy/requirement/workflow authority selected
R, then R remains a candidate baseline.

### Does current work position describe what was selected, why it was selected, or where work is oriented?

Primarily:

```text
where work is oriented
```

Secondarily, it may preserve:

```text
what was selected
why it was selected
```

Those details matter because orientation without selection rationale is fragile.
But preserving them does not make Current Work Position the authority origin.

### Does handoff preserve authority or merely preserve context?

Handoff preserves context and the authority trail. It may preserve the fact that
an authority-bearing selection occurred. It should not be treated as originating
authority unless the repository explicitly defines the handoff artifact as a
decision artifact for that scope.

The safer answer is:

```text
handoff preserves authority provenance and active context;
it does not create authority.
```

### Where does example_host_b comparison selection naturally belong?

The cleanest placement is distributed:

```text
Decision / operator-policy authority: selects R
Accepted Baseline: names R as selected comparison reference
Investigation Context: scopes R to investigation I
Current Work Position: orients ongoing work around R and its boundaries
Handoff Context: preserves R, rationale, boundaries, and authority trail
Lens/View: may present comparison against R if given upstream selection
```

No single concept should absorb all roles.

### Which concept survives participant turnover most cleanly?

Handoff Context survives participant turnover most directly because its purpose
is continuation across sessions and participants. However, durable decision or
accepted-baseline records survive authority scrutiny more cleanly because they
identify what was selected and by what authority.

The best turnover-resilient pattern is therefore:

```text
durable decision/accepted-baseline authority trail
    + handoff-preserved orientation and activation instructions
```

### Which concept best preserves existing repository boundaries?

The boundary-preserving answer is:

```text
Decision carries the selection transition.
Accepted Baseline carries the scoped selected-reference state.
Investigation Context carries scope and purpose.
Current Work Position carries active orientation.
Handoff Context carries continuation preservation.
```

This respects existing boundaries between recommendation, decision, acceptance,
expectation, execution, projection, view, and handoff.

### Does accepted baseline represent authority, state, orientation, context, selection, or other?

Accepted baseline represents:

- **state**: a reference is selected within a scope;
- **selection**: the chosen comparison reference;
- **derivative authority**: comparison authority resulting from upstream
  authorized selection;
- **context**: bounded by investigation/question/view/continuation purpose.

It may participate in orientation, but orientation is better described by
Current Work Position. It is not standalone truth or should-authority.

### Is accepted baseline a real architectural concept?

Yes, but in a constrained sense.

Accepted baseline is a real architectural vocabulary item for the state/effect
of selected comparison authority. It is not a new root authority primitive. It
is an existing repository pattern viewed through a new lens:

```text
candidate -> authorized selection -> accepted selected state
```

This pattern already appears in adjacent forms such as plan acceptance,
recommendation-to-decision boundaries, and adoption-decision vocabulary. The new
part is the baseline-specific name and boundary, not a new authority class.

## Candidate models evaluated

### Model A: Decision Carries Acceptance

Finding: strongest authority-origin model.

Decision legitimately carries acceptance when it is an authorized selection of a
comparison reference for a scope. Accepted baseline is then the resulting state.

Risk: overloading decision as the only durable representation can make later
work re-read the event each time instead of naming the selected reference.

### Model B: Accepted Baseline Is Independent

Finding: valid as selected-reference state, invalid as independent authority
origin.

Accepted baseline should remain distinct from decision because it names the
selected comparison reference. It should not replace the decision or erase the
authority trail.

### Model C: Current Work Position Carries Acceptance

Finding: valid as orientation carrier, not authority origin.

Current Work Position can include `R is active comparison reference`, `why R was
selected`, and `do not treat R as expectation`. It should not silently turn an
orientation into a decision.

### Model D: Investigation Context Carries Acceptance

Finding: valid as scope carrier, not automatic selector.

Investigation Context is where comparison-reference acceptance most naturally
applies. But an investigation can contain candidates without accepting them.

### Model E: Handoff/Continuation Carries Acceptance

Finding: valid as continuity carrier, not origin.

Handoff Context is the cleanest participant-turnover carrier. It preserves the
selected reference, active boundary, and authority trail. It does not invent the
selection.

### Model F: No New Concept Needed

Finding: partly valid.

No new root authority primitive is needed because decision plus scope provides
the authority transition. But accepted-baseline vocabulary is not redundant if
the repository needs to distinguish a candidate comparison reference from a
selected comparison reference across ongoing investigation and handoff.

A safe version of Model F is:

```text
No new authority primitive needed.
Accepted Baseline is a boundary-preserving name for an existing candidate-to-
accepted pattern applied to comparison references.
```

## Major findings

1. Selected comparison authority is best understood as an authorized selection
   transition plus a scoped selected-reference state.
2. Decision is the cleanest existing concept for the authority-bearing selection
   transition.
3. Accepted Baseline is the cleanest name for the selected comparison reference
   after that transition.
4. Accepted Baseline should not be treated as an independent authority origin.
5. Investigation Context is the natural scope for accepted comparison reference
   use.
6. Current Work Position is the natural orientation carrier: it preserves where
   work is active and how the selected reference constrains safe continuation.
7. Handoff Context is the natural turnover carrier: it preserves selected
   context, rationale, boundaries, and authority trail across participants.
8. Lens/View can present accepted comparison references only when supplied by an
   upstream authority; it cannot create acceptance.
9. Accepted baseline creates comparison authority, not expectation authority.
10. No implementation, storage mechanism, workflow, ontology, HomeOps, SeedOps,
    or runtime change is implied by this reconciliation.

## Authority-carrying concepts discovered

Authority-bearing or authority-adjacent concepts in this reconciliation:

| Concept | Authority role |
| --- | --- |
| Operator selection | Can directly authorize comparison-reference selection within stated scope. |
| Policy/requirement authority | Can authorize selection only when explicit about reference, scope, and purpose. |
| Decision | Best existing carrier for the selection transition. |
| Accepted Baseline | Derivative selected-reference state with comparison authority. |
| Investigation Context | Carries scope and purpose, not automatic selection. |
| Current Work Position | Carries active orientation and may include accepted reference, not origin authority. |
| Handoff Context | Carries continuation preservation and authority trail, not origin authority. |
| Lens/View | Carries presentation/interpretation only, not independent authority. |

## Remaining open questions

1. What minimum evidence is required before a candidate comparison reference is
   eligible for authorized selection?
2. How should conflicting accepted comparison references be described when
   different investigations select different scopes?
3. Can a requirement or policy establish comparison-reference acceptance without
   a separate decision record if its language is explicit enough?
4. Is accepted baseline best treated as part of investigation state, decision
   effect, current-work-position orientation, or another existing documentation
   pattern?
5. What makes an accepted comparison reference stale, superseded, or no longer
   applicable?
6. How much authority trail must a handoff preserve before a future participant
   can rely on the selected comparison without re-validating the original
   selection?
7. Can multiple current work positions each carry different active comparison
   references without conflict?
8. What terminology best avoids implying that accepted baseline is truth or
   expectation?

## Conclusion

Comparison-reference selection is not a new root architectural primitive. It is
an existing repository authority pattern viewed through a comparison-reference
lens:

```text
candidate
    -> authorized selection
    -> accepted selected state
    -> scoped use
    -> orientation preservation
    -> continuation preservation
```

Accepted baseline is still a useful architectural concept because it names the
selected comparison reference and keeps it distinct from a mere candidate. But
its authority is derivative: it depends on a legitimate selection source and a
scope. Decision carries the selection transition most cleanly; Investigation
Context scopes it; Current Work Position orients ongoing work around it; Handoff
Context preserves it across participants; Lens/View may expose it without
creating it.

For example_host_b, the legitimate reconciliation is:

```text
historical example_host_b-sees-M is candidate evidence;
an authorized decision/operator-policy selection chooses it as reference R for
investigation I;
R becomes the accepted baseline only for comparison in I;
current work position keeps the investigation oriented around R and its limits;
handoff preserves R, rationale, boundaries, and authority trail for continuation.
```

The selected comparison reference is therefore real, scoped, authority-bearing as
comparison state, and explicitly not truth, expectation, ownership, policy
violation, remediation instruction, or execution authority.
