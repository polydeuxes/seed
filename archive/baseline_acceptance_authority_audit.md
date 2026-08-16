---
status: audit
scope: baseline acceptance authority investigation
created: 2026-06-18
---

# Baseline Acceptance Authority Audit

## Status

Investigation only. This document does not implement baselines, baseline
storage, baseline acceptance workflows, expectations, HomeOps, SeedOps,
operator surfaces, projection behavior, policy behavior, approval flows,
runtime behavior, schemas, tests, or ontology.

Short answer: under current repository authority, moving from a candidate
baseline to an accepted baseline would be meaningful only as a scoped selection
of a comparison reference. It would not create truth, ownership, operational
requirement, alerting expectation, or execution authority.

The boundary-preserving answer is:

```text
Candidate Baseline
    = evidence-supported possible comparison reference

Accepted Baseline
    = authority-selected comparison reference for a scoped question,
      investigation, decision context, view, or continuation context

Expectation
    = should-bearing claim authorized by a distinct normative authority
```

For the operational example:

```text
example_host_b historically sees mount M
example_host_b no longer sees mount M
historical example_host_b-sees-M appears useful as a comparison reference
someone or something accepts that reference for investigation
```

repository evidence supports acceptance only if an authority-bearing context
selects that historical reference for comparison. The most directly legitimate
authority is an operator-owned investigation or decision context, possibly
represented through a decision, accepted work item, current-work position, or
view/question scope. Goal, policy, or requirement can legitimate acceptance only
when they explicitly connect the reference to the scoped comparison purpose.
They do not implicitly promote history into an accepted baseline.

## Audit question

```text
What authority can legitimately accept a baseline?
```

More specifically:

```text
What does it mean
to move from

Candidate Baseline

to

Accepted Baseline?

under repository authority?
```

This audit concerns only the first authority boundary:

```text
Candidate Baseline
    ? authority selection
    ->
Accepted Baseline
```

It does not resolve or cross the second boundary:

```text
Accepted Baseline
    ? should-bearing authority
    ->
Expectation
```

## Prior findings reconciled

Required input documents reconciled:

- `docs/observation_visibility_continuity_baseline_expectation_concern_reconciliation.md`
- `docs/baseline_continuity_expectation_audit.md`
- `docs/candidate_baseline_accepted_baseline_expectation_audit.md`
- `docs/should_authority_expectation_audit.md`
- `docs/goal_policy_and_operator_authority_reconciliation.md`
- `docs/lens_view_reconciliation.md`

Their findings remain compatible and are not contradicted by the additional
repository evidence inspected for this audit:

1. Observation, visibility, and continuity are evidence-facing or interpretive
   concepts, not should-bearing authority.
2. Candidate baseline is distinct from raw continuity because it frames an
   observed or historical condition as a possible comparison reference for a
   question.
3. Accepted baseline, if recognized, requires an authority selection boundary.
4. Expectation requires separate should-bearing or anticipation-bearing
authority. Baseline acceptance alone must not silently create `should continue`.
5. Goals express operator-owned desired outcomes and can provide relevance, but
   goals do not automatically select operational facts as required conditions.
6. Policy constrains acceptable behavior and may require approvals, but policy
   does not automatically convert historical observations into operational
   baselines unless a policy rule explicitly says so.
7. Requirements can be should-like inside their scope, but current repository
   requirements are primarily validation/view integrity concepts, not general
   topology expectation declarations.
8. Lens/view concepts support scoped interpretation over projected State, but do
   not create new State authority, truth authority, policy authority, or
   execution authority.

The accepted chain remains:

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

This audit narrows the first question mark.

## Files inspected

Required documents:

- `docs/observation_visibility_continuity_baseline_expectation_concern_reconciliation.md`
- `docs/baseline_continuity_expectation_audit.md`
- `docs/candidate_baseline_accepted_baseline_expectation_audit.md`
- `docs/should_authority_expectation_audit.md`
- `docs/goal_policy_and_operator_authority_reconciliation.md`
- `docs/lens_view_reconciliation.md`

Additional documentation inspected:

- `docs/current_work_position_frontier.md`
- `docs/handoff_and_continuation_lineage_frontier.md`
- `docs/handoff_consumption_activation_reconciliation.md`
- `docs/capability_verification_promotion_reconciliation.md`
- `docs/capability_verification_vocabulary.md`
- `docs/goal_relevance_and_recommendation_generation_reconciliation.md`
- `docs/policy_pending_action_inventory.md`
- `docs/state_summary_authority_reconciliation.md`
- `docs/operator_interface_and_projection_authority_reconciliation.md`
- `docs/impact_overview_authority_reconciliation.md`
- `docs/adoption_decision_authority_reconciliation.md`
- `docs/assessment_recommendation_and_decision_reconciliation.md`
- `docs/architecture_principles.md`
- `docs/invariants.md`

Implementation evidence inspected:

- `seed_runtime/models.py`
- `seed_runtime/state.py`
- `seed_runtime/state_views.py`
- `seed_runtime/context_views.py`
- `seed_runtime/policy.py`
- `seed_runtime/action_plans.py`
- `seed_runtime/handoff_plans.py`
- `seed_runtime/decisions.py`
- `seed_runtime/tool_needs.py`
- `seed_runtime/capability_candidates.py`
- `seed_runtime/capability_inventory.py`
- `seed_runtime/capability_promotion_readiness.py`
- `seed_runtime/capability_verification.py`
- `seed_runtime/verification_evidence.py`
- `seed_runtime/preconditions.py`

Tests inspected:

- `tests/test_preconditions.py`
- `tests/test_handoff_plans.py`
- `tests/test_capability_promotion_readiness.py`
- `tests/test_capability_verification_invariants.py`
- `tests/test_capability_candidates.py`
- `tests/test_policy.py`
- `tests/test_state_views.py`
- `tests/test_context_views.py`
- `tests/test_tool_needs.py`
- `tests/test_execution_proposals.py`
- `tests/test_architecture_invariants.py`

## Existing acceptance patterns

### 1. Action plan proposed -> accepted

`ActionPlan` has an explicit lifecycle:

```text
proposed -> accepted -> superseded
proposed -> rejected
proposed -> superseded
```

This is the closest implemented analogue to candidate-to-accepted. The service
records `action_plan.accepted`, and its docstring says acceptance only changes
lifecycle state. It does not execute the plan, approve tool calls, or register
tools.

Architectural lesson:

```text
acceptance = selected lifecycle status
acceptance != approval
acceptance != execution authorization
acceptance != environmental mutation
```

This pattern strongly supports an accepted-baseline interpretation that selects
a comparison reference without creating expectation, truth, or execution power.

### 2. Action plan accepted -> approved -> execution authorization

The repository keeps later authority transitions separate. `approve_plan`
records approval for an accepted plan but explicitly says plan approval is not
execution authorization. `grant_execution_authorization` then records a short-
lived authorization for one concrete proposal and avoids storing raw tool
arguments or credentials.

Tests preserve the distinction: action-plan approval does not satisfy mutating
execution authorization; mutating plans require concrete execution
authorization, while lower-risk read-only plans can use action-plan approval.

Architectural lesson:

```text
accepted plan
    != approved plan
    != execution-authorized plan
    != executed action
```

For baseline acceptance, the analogous safe reading is:

```text
accepted baseline
    != expected condition
    != alerting rule
    != remediation authority
    != truth creation
```

### 3. Handoff creation requires accepted action plan but remains non-executable

`HandoffPlanService` creates handoff plans only from accepted action plans. The
handoff itself remains a boundary description. It does not execute the provider,
approve the action plan, authorize execution, register tools, ask for
credentials, or manage provider jobs. The `HandoffPlan` model rejects fields
that would imply approval, execution authorization, credential availability,
provider trust, or tool registration.

Architectural lesson:

```text
accepted upstream selection can legitimate a downstream boundary artifact,
while the downstream artifact still must not claim unrelated authority.
```

For baselines, an accepted comparison reference could legitimate a downstream
view, investigation, or handoff context saying `compare current example_host_b mount
visibility to this selected historical reference`. It would not legitimate the
view or handoff to claim that the mount is required.

### 4. Capability candidate -> promotion readiness -> verified capability remains separated

Capability promotion readiness joins capability candidates with verification
evidence and explains whether a future promotion would be supportable. It
explicitly does not create `capability_verified` facts, select capabilities,
evaluate policy, invoke tools, plan, or execute.

Architectural lesson:

```text
candidate support + readiness evidence
    = supportable future promotion
    != promotion itself
    != selected capability
    != execution authority
```

This is directly relevant to candidate baselines. Historical continuity plus
current relevance can make a baseline candidate supportable for acceptance, but
supportability is not acceptance. Acceptance requires a separate authority
selection.

### 5. Tool need and recommendation patterns

Model decisions can request a tool need. Tool-need creation and capability
recommendations do not register tools or produce execution decisions. Tests also
assert that capability candidates do not become execution decisions.

Architectural lesson:

```text
need/recommendation/candidate
    != decision
    != registration
    != execution
```

For baselines:

```text
candidate baseline recommendation
    != accepted comparison reference
```

unless an authority-bearing decision, operator selection, or scoped workflow
accepts it.

### 6. Policy approval patterns

`PolicyGate` may allow, block, require confirmation, or require approval based
on action risk and matching approvals. This is real authority, but it is action
policy authority. It does not establish truth about the environment and does not
turn observed history into operational expectation.

Architectural lesson:

```text
policy authority is scope-bound.
```

A policy could accept a baseline only if baseline comparison is within the
policy's explicit scope, for example a future policy saying `for investigation X,
use last-known-good visibility as comparison reference`. Current policy evidence
does not provide that general operational topology rule.

### 7. Lens/view scoped interpretation

State Views and Context Views are deterministic read-only projections over
already-built State. Lens-like interpretation can select, group, rank, caveat,
or classify projected material for a bounded question, but does not create new
State authority or operational truth.

Architectural lesson:

```text
view scope can carry interpretation scope,
but view scope alone cannot create authoritative State or expectation.
```

This supports view-scoped accepted baselines as comparison references for a
question, provided the acceptance authority is preserved as an input or context,
not silently invented by the view.

### 8. Current-work-position and continuation/handoff patterns

Current Work Position is exploratory, but the frontier asks what orientation
current work occupies and emphasizes selected continuation-relevant orientation,
not all preserved information. Handoff/continuation documents similarly preserve
context for safe resumption without making handoff artifacts architecture
authority.

Architectural lesson:

```text
continuation context can preserve selected orientation,
but preserved orientation is not automatically global architecture authority.
```

Baseline acceptance could therefore be legitimate inside a current investigation
or handoff if it records that a historical reference has been selected as the
comparison point for the next safe move. That is scoped comparison authority,
not global baseline truth.

## Authority analysis by required area

### Goal authority

Goals are operator-owned desired outcomes represented for relevance,
explanation, and decision context. A goal can make example_host_b losing mount M
relevant, for example under `investigate ingestion reliability` or `preserve
storage visibility evidence`.

A goal can legitimately contribute to baseline acceptance when it defines the
question that needs a comparison reference:

```text
goal: investigate ingestion regression
candidate: historical example_host_b-sees-M
selection: use it as comparison reference for this investigation
```

But goal authority alone is insufficient if the repository cannot show that the
goal selected that reference or that the reference is needed for the goal. Goal
relevance is not baseline acceptance by itself.

### Policy authority

Policy can authorize or constrain behavior. It can require approval, prohibit
actions, or allow low-risk read-only activity. Policy could legitimately accept
a baseline only if policy text explicitly names a baseline rule or a baseline
selection rule.

Current repository policy patterns do not provide a general rule like:

```text
all long-lived historical visibility automatically becomes accepted baseline
```

Such a rule would also risk collapsing continuity into expectation. Therefore
policy authority is possible but not currently sufficient for the example_host_b
baseline acceptance unless future or external policy explicitly says to select
that comparison reference.

### Requirement authority

Requirement-like concepts are real inside validation boundaries, such as graph
or view rules that expect certain subject/object types. They are scoped shoulds.
They do not currently express operational topology requirements such as
`example_host_b must see mount M`.

A requirement could accept or establish a baseline if it explicitly says a
reference condition is the required comparison reference for a validation or
investigation. Without that, current requirement authority does not accept the
example_host_b baseline.

### Operator authority

Operator authority is the cleanest current source for baseline acceptance when
acceptance means `use this as the comparison reference for my investigation`.
The operator owns intent, can define the question, can accept an investigation
path, and can select among alternatives.

Operator acceptance should remain scoped:

```text
operator accepts historical example_host_b-sees-M
as comparison reference
for investigating why example_host_b no longer sees mount M
```

That creates comparison authority for the investigation. It does not create
truth that M exists, ownership of M, a requirement that example_host_b must see M, or a
policy violation when example_host_b does not see M.

### Decision authority

Repository decision concepts select among alternatives. The goal/policy/operator
reconciliation distinguishes recommendations from decisions and decisions from
commands/actions. This maps well to candidate baseline acceptance:

```text
candidate baseline recommendation
    -> accepted decision to compare against it
```

Decision acceptance is not free-standing authority; it is legitimate when the
decision is made by an authorized actor or process within a scoped context.
Therefore Model B is strong if read as `decision records the selection`, but too
strong if read as `any decision object can create authority without operator,
policy, or workflow scope`.

### Plan authority

Action-plan acceptance is the strongest implemented candidate-to-accepted
pattern. It proves the repository can preserve acceptance as a lifecycle
selection while refusing to grant approval, execution, registration, or runtime
mutation.

A baseline acceptance analogue could be:

```text
candidate comparison reference
    -> accepted comparison reference for plan/investigation X
```

But plan authority is not inherently should-authority. Even an accepted plan is
not an approval or execution authorization. Therefore a plan can scope and carry
baseline acceptance only for the purpose of the plan or investigation.

### Verification authority

Capability verification and promotion-readiness evidence show that evidence can
support readiness without performing promotion. Verification authority can
support the evidence quality of a candidate baseline:

```text
historical observations are well-supported
measurement provenance is adequate
continuity evidence is strong
```

But verification authority cannot by itself accept the baseline unless the
verification process is explicitly empowered to select comparison references.
Evidence support is not selection authority.

### Capability promotion authority

Capability promotion patterns distinguish candidate, readiness, verified,
selected, and execution-authorized states. The key lesson is that promotion
requires an explicit boundary crossing. Readiness does not perform promotion.

Baseline acceptance should preserve the same boundary:

```text
candidate baseline supportable for acceptance
    != accepted baseline
```

unless an authority-bearing selection occurs.

### Current-work-position authority

Current Work Position is not established ontology and should not be used as
implementation authority. However, it is useful as an investigative concept: it
identifies the selected orientation from which present work can continue.

Baseline acceptance may be part of current-work-position when the selected
orientation is:

```text
continue investigating example_host_b by comparing current mount visibility to the
historical example_host_b-sees-M reference
```

This is a scoped continuation authority. It does not become global baseline
truth.

### Continuation/handoff authority

Handoff authority can preserve what a future participant should compare or
resume, but repository handoff patterns emphasize that handoff artifacts do not
create hidden architecture authority. A handoff can carry accepted comparison
context only if the upstream accepted investigation or decision authorized it.

### Approval flows

Existing approval flows warn against conflating acceptance and approval. Plan
acceptance is distinct from plan approval; both are distinct from execution
authorization. Therefore accepted baseline should not be named or designed as if
it were approval of the environmental condition. It is more like accepting a
reference for use, not approving a reality state.

## Candidate models

### Model A: Operator Acceptance

```text
operator selects:

use historical example_host_b-sees-M
as the comparison reference
```

#### Support

Strong. Operators own intent, goals are operator-owned, and decisions require
authority. In the example_host_b case, the operator can legitimately choose a
historical visibility pattern as the reference for investigation.

#### Boundary-preserving interpretation

```text
operator-selected accepted baseline
    = comparison authority for the operator's scoped question
```

#### Risks

Operator statements should not silently become global truth, policy, or
expectation. The accepted baseline must preserve scope, provenance, and purpose.

#### Finding

Model A is valid and probably the most direct authority path for the operational
example, provided it remains scoped and non-normative.

### Model B: Decision Acceptance

```text
accepted decision
accepted investigation
accepted work item
```

provides the acceptance authority.

#### Support

Strong as a recording and lifecycle pattern. Repository evidence already treats
decisions as selections distinct from recommendations, commands, and actions.
Action-plan acceptance is an implemented lifecycle selection.

#### Boundary-preserving interpretation

```text
authorized decision selects candidate baseline as reference for scope S
```

#### Risks

A decision record alone is not magic. It must be tied to an authorized actor,
operator intent, policy, workflow, or other legitimate decision context.

#### Finding

Model B is valid when the decision is the preserved form of an authorized
selection. It is not valid if it treats any decision artifact as self-authorizing.

### Model C: Goal / Requirement / Policy Acceptance

```text
goal
requirement
policy
```

implicitly or explicitly establish the baseline.

#### Support

Partial. Goals can provide relevance; requirements and policy can provide
should-like or governance authority inside their scope.

#### Boundary-preserving interpretation

```text
explicit policy/requirement/goal-linked rule selects a comparison reference
```

Examples of legitimate future shapes:

```text
policy: for storage-regression investigations, compare current visibility to
        last-known-good visibility selected by the operator

requirement: validation V uses reference R as its comparison baseline

goal-linked decision: to investigate ingestion reliability, accept historical
                      example_host_b-sees-M as the comparison reference
```

#### Risks

Implicit establishment is unsafe. If long-lived history automatically becomes
accepted baseline because a goal exists, continuity collapses into accepted
baseline and possibly into expectation.

#### Finding

Model C is valid only when explicit. Current repository authority does not
support implicit goal/policy/requirement acceptance of example_host_b-sees-M.

### Model D: View-Scoped Acceptance

```text
baseline accepted
only for a particular lens/view/question
```

#### Support

Moderate to strong, with a caveat. Lens/view concepts are explicitly scoped and
read-only. They are good at preserving bounded interpretation and caveats.

#### Boundary-preserving interpretation

```text
accepted for view/question Q
    = compare current evidence against selected reference R in this view
```

#### Risks

Views cannot invent authority. View-scoped acceptance needs an upstream accepted
question, operator selection, decision context, policy, or workflow authority.
Otherwise the view is merely presenting a candidate baseline.

#### Finding

Model D is valid as scoping for acceptance, not as independent acceptance
authority.

### Model E: No Acceptance Concept

```text
Candidate baseline remains sufficient.
No accepted baseline layer is needed.
```

#### Support

Some. If the repository only needs to show possible comparison references, then
candidate baseline may be enough. This avoids new authority semantics.

#### Boundary-preserving interpretation

```text
show candidate references with evidence and caveats;
let the operator reason outside the repository
```

#### Risks

The repository already distinguishes recommendations from decisions and
candidates from promotions. If a later investigation, handoff, or view needs to
say which reference was actually selected for comparison, candidate-only language
cannot preserve that selection without overloading candidate.

#### Finding

Model E is safe for current implementation and may be sufficient for simple
example_host_b inspection. It is less sufficient when the selected comparison reference
must survive across handoff, continuation, or audit.

## Required questions

### 1. What existing repository concepts already perform something similar to candidate -> accepted?

The strongest existing analogues are:

- action plan `proposed -> accepted`;
- recommendation or candidate capability evidence -> promotion readiness, while
  preserving that readiness is not promotion;
- tool need / recommendation -> decision or action-plan proposal, while keeping
  recommendation distinct from decision;
- accepted action plan -> handoff plan eligibility, while keeping handoff
  non-executable;
- policy approval and execution authorization as later, separate authority
  boundaries.

The action-plan lifecycle is the most directly analogous because it explicitly
uses `accepted` while denying approval, execution, and registration semantics.

### 2. What distinguishes candidate baseline from accepted baseline without introducing expectation?

```text
candidate baseline
    = evidence-supported possible comparison reference

accepted baseline
    = selected comparison reference for a named scope and purpose
```

The distinguishing feature is not truth or shouldness. It is selection
authority.

Minimum distinguishing attributes are:

- selected reference;
- accepting authority or authority path;
- scope/question/purpose;
- evidence/provenance for the underlying candidate;
- caveat that acceptance is comparison authority only.

### 3. Can acceptance exist without should-authority?

Yes. Existing action-plan acceptance proves that acceptance can be lifecycle
selection without approval or execution. A baseline can be accepted as a
comparison reference without saying the referenced condition should hold.

The safe form is:

```text
use R as comparison reference for S
```

not:

```text
R should hold
```

### 4. Can multiple accepted baselines coexist?

Yes, if acceptance is scoped. Multiple accepted baselines can coexist when they
serve different questions, views, investigations, or authority paths:

```text
operational baseline: compare current service posture to operator-selected
                      last-known-good posture for incident review

storage baseline: compare mount visibility to a storage-specific investigation
                  reference

investigation baseline: compare example_host_b current visibility to historical
                        example_host_b-sees-M for this investigation only
```

They may conflict or overlap, so each needs scope and provenance. Coexistence is
unsafe only if accepted baseline is treated as global truth.

### 5. Must baseline acceptance be global? Or can it remain scoped?

It need not be global, and repository boundaries strongly favor scoped
acceptance. Lens/view findings, goal/decision context, plan lifecycle, and
handoff boundaries all preserve scope.

A global accepted baseline would require stronger authority, likely explicit
policy or requirement authority, and would risk being confused with expectation.

### 6. Does baseline acceptance create truth? Or only comparison authority?

Only comparison authority.

Accepted baseline does not create truth that:

- example_host_b currently sees M;
- M still exists;
- example_host_b owns M;
- example_host_b must see M;
- absence of M is a violation;
- remediation is authorized.

It authorizes a comparison such as:

```text
for this investigation, compare current example_host_b mount visibility against the
historical example_host_b-sees-M reference
```

### 7. Would the example_host_b example benefit from accepted baseline authority? Or is candidate baseline sufficient?

Candidate baseline is sufficient for first-pass visibility investigation:

```text
historical example_host_b-sees-M is a plausible reference candidate
current example_host_b-does-not-see-M differs from that candidate
```

Accepted baseline authority becomes useful when the selected reference must
survive across:

- handoff to another operator or continuation;
- repeated views or reports;
- an investigation record;
- comparison of multiple candidate references;
- audit of why a deviation was discussed;
- separation of selected comparison reference from rejected alternatives.

For example_host_b, acceptance would help if the investigation needs to preserve:

```text
we selected historical example_host_b-sees-M, not some cluster-wide or storage-wide
reference, as the comparison point for this question
```

It is not needed merely to notice that visibility changed.

### 8. Which candidate model best preserves repository boundaries?

The best boundary-preserving model is a composite:

```text
Operator/authorized decision acceptance
    scoped by question, view, investigation, plan, or handoff context
    optionally constrained or established by explicit goal/policy/requirement
    never treated as expectation or truth
```

In candidate-model terms:

1. Model A is the most direct authority source for the example_host_b example.
2. Model B is the best preservation/recording mechanism when the acceptance must
   be auditable or durable.
3. Model D is the best scoping discipline for views and questions.
4. Model C is valid only when explicit, not implicit.
5. Model E remains safe for current implementation when no durable selected
   reference is needed.

## Example host example analysis

### Evidence chain

```text
Observation:
    example_host_b reported mount M at earlier times

Visibility:
    M was visible from example_host_b in those observations

Continuity:
    example_host_b-sees-M persisted or recurred across observations

Candidate baseline:
    historical example_host_b-sees-M is a plausible comparison reference

Current observation/visibility:
    example_host_b no longer sees M
```

None of those steps says:

```text
example_host_b owns M
example_host_b should see M
M is required for ingestion
missing M is a policy violation
remediation is authorized
```

### Legitimate acceptance paths

#### Operator-scoped acceptance

```text
operator: For this investigation, compare example_host_b's current mount visibility to
          the historical example_host_b-sees-M reference.
```

Legitimate because the operator owns the question and selects the reference for
that question.

#### Decision-scoped acceptance

```text
decision: Accept candidate reference R for investigation I.
```

Legitimate if the decision is authorized and scoped. It records the selection.

#### Goal-linked acceptance

```text
goal: investigate ingestion reliability
decision: accept historical example_host_b-sees-M as comparison reference for that goal
```

Legitimate because the goal supplies relevance and the decision supplies
selection. The goal alone is not enough.

#### Policy/requirement acceptance

```text
policy or requirement explicitly says to use reference R or rule R-selection for
this class of investigation
```

Legitimate if such policy or requirement exists. No current inspected evidence
provides this general example_host_b rule.

#### View-scoped acceptance

```text
storage visibility view for question Q uses accepted reference R
```

Legitimate only when the view receives or points to an upstream acceptance. The
view does not create the authority by itself.

#### Handoff/continuation acceptance

```text
handoff says: continue from accepted comparison reference R for investigation I
```

Legitimate when the handoff preserves an upstream operator/decision acceptance.
The handoff itself should not invent acceptance.

### Insufficient acceptance paths

The following are not sufficient under repository authority:

- historical continuity alone;
- current absence alone;
- usefulness alone;
- a view that silently chooses R without authority provenance;
- a recommendation that R looks useful;
- a capability or verification readiness result;
- a generic goal with no selected reference;
- policy approval for an unrelated action;
- handoff metadata with no upstream selected reference.

## Comparison authority vs truth authority

Accepted baseline should be read as comparison authority:

```text
This is the reference we are allowed to compare against for this scoped purpose.
```

It should not be read as truth authority:

```text
This is the true state of the world.
```

It should also not be read as should-authority:

```text
This condition should hold.
```

Comparison authority can coexist with uncertainty. The historical reference may
be incomplete, stale, partially ambiguous, or later contradicted. Acceptance only
says that a scoped authority selected it for comparison despite those caveats.

This distinction preserves repository boundaries:

```text
Evidence support decides whether R is a candidate.
Acceptance authority decides whether R is selected for comparison.
Truth authority remains with evidence/projection rules.
Expectation authority remains with should-bearing sources.
Execution authority remains with policy, approval, command, and action paths.
```

## Boundary preservation analysis

### Boundaries preserved by accepted baseline as scoped comparison authority

- Observation remains descriptive.
- Visibility remains current or historical evidence presentation.
- Continuity remains pattern survival, not selection.
- Candidate baseline remains possible reference, not selected reference.
- Accepted baseline becomes selected comparison reference only.
- Expectation remains separate and requires should-bearing authority.
- Concern can be raised without expectation.
- View/lens interpretation remains scoped and read-only.
- Policy approval and execution authorization remain unrelated unless explicitly
  invoked.
- Handoff can preserve selected comparison context without executing or
  authorizing anything.

### Boundaries violated by unsafe interpretations

Unsafe interpretation:

```text
long-lived history automatically becomes accepted baseline
```

Boundary violation:

```text
continuity collapses into acceptance
```

Unsafe interpretation:

```text
accepted baseline means example_host_b should see M
```

Boundary violation:

```text
acceptance collapses into expectation
```

Unsafe interpretation:

```text
view presents R, therefore R is authoritative globally
```

Boundary violation:

```text
view scope collapses into State/truth authority
```

Unsafe interpretation:

```text
accepted comparison authorizes remediation
```

Boundary violation:

```text
comparison authority collapses into execution authority
```

Unsafe interpretation:

```text
policy approval for investigation means baseline is true
```

Boundary violation:

```text
approval collapses into truth authority
```

## Major findings

1. Accepted baseline is a meaningful architectural concept if, and only if, it
   means scoped comparison-reference selection.
2. Acceptance can exist without should-authority. Existing action-plan
   acceptance demonstrates a lifecycle selection that does not approve or
   execute.
3. The legitimate authority to accept a baseline is not historical evidence
   itself. It is an authority-bearing selection context: operator selection,
   authorized decision, accepted investigation/work item, explicit
   policy/requirement rule, or continuation/handoff context preserving such a
   selection.
4. View-scoped acceptance is attractive because it prevents global truth claims,
   but views cannot invent acceptance authority.
5. Goal authority supplies relevance, not selection, unless paired with an
   explicit decision or rule.
6. Policy and requirement authority can establish baseline acceptance only when
   explicit and scoped.
7. Multiple accepted baselines can coexist if their scopes are preserved.
8. Baseline acceptance creates comparison authority, not truth authority,
   expectation authority, approval authority, or execution authority.
9. The example_host_b example benefits from accepted baseline authority only when the
   selected comparison reference must be durable, auditable, handed off, reused,
   or distinguished from alternatives. Candidate baseline is enough for a local
   first-pass comparison.

## Recommended next investigation

No implementation is recommended here. The next investigation should ask:

```text
What minimal authority record would be necessary to preserve scoped comparison
selection without implementing baseline storage or expectation workflows?
```

Subquestions:

1. Is accepted baseline better modeled as an investigation decision, a view
   parameter, a current-work-position element, a handoff note, or a distinct
   architectural vocabulary term?
2. What provenance is required to keep accepted comparison authority separate
   from truth authority and should-authority?
3. How should conflicting scoped accepted baselines be presented without
   treating one as globally correct?
4. When does a selected comparison reference become stale or unsuitable without
   implying that it was false?
5. Which existing lifecycle pattern is the best analogy: action-plan acceptance,
   decision selection, capability promotion readiness, or handoff context?
6. What evidence would show that accepted baseline is redundant and candidate
   baseline plus decision context is sufficient?

## Non-conclusions

This audit does not conclude that:

- accepted baseline is implemented;
- baseline storage should be implemented;
- baseline acceptance workflows should be implemented;
- expectations should be implemented;
- HomeOps or SeedOps should be implemented;
- example_host_b should see mount M;
- mount M exists now;
- mount M is owned by example_host_b;
- missing mount M is an alert;
- historical continuity automatically creates baseline acceptance;
- any view can create global baseline authority;
- accepted baseline authorizes remediation;
- accepted baseline is a policy approval;
- accepted baseline is truth.
