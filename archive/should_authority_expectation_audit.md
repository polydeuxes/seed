---
status: audit
scope: should-authority and expectation authorization investigation
created: 2026-06-17
---

# Should Authority / Expectation Audit

## Status

Investigation only. No implementation changes were made to expectations,
goals, requirements, policies, concerns, alerts, recommendations, HomeOps,
SeedOps, state projection, lenses, views, capability verification, refresh
logic, plans, approvals, storage topology projection, ingestion, tests, or
runtime behavior.

Short answer: current repository authority contains several concepts that can
say some scoped form of `should`, but none is a general operational expectation
concept that can say:

```text
example_host_b should see mount M
```

The strongest current should-like authorities are:

1. **policy**: should/must/should-not for permitted, prohibited, required, or
   approval-gated behavior;
2. **goals**: desired outcomes, owned by operators or delegated organizational
   context, that make knowledge relevant but do not authorize action;
3. **requirements**: rule/catalog expectations inside validation or view
   boundaries, such as expected subject and object types for known relationship
   rules;
4. **approvals and decisions**: selected or authorized transitions inside a
   bounded action/command lifecycle;
5. **staleness and refresh recommendations**: should-like evidence-acquisition
   pressure, explicitly not truth, command, execution, or environment
   expectation;
6. **capability verification**: readiness/support status, explicitly not
   selection, permission, execution authority, or an operational expectation.

Therefore, under current repository authority, `should` is legitimate only when
its authority source is named and scoped. Repository history can support
continuity evidence, candidate baselines, candidate expectations, and operator
pressure, but it cannot by itself become a normative expectation. Operator prose
can create an expectation only when it is accepted as operator-owned intent,
goal, policy, requirement, decision, approval, or another explicit authority
record; prose alone must not become command, action, policy bypass, or unsupported
world truth.

## Audit question

```text
What repository authority can legitimately say "should"?
```

More specifically:

```text
What can authorize an expectation?
```

This audit treats `should` as an authority-bearing word. A sentence that uses
`should` may mean different things depending on the authority source:

| Sentence shape | Possible authority | Boundary |
| --- | --- | --- |
| `X should be true` | declaration, requirement, policy, goal-derived desired state, accepted design invariant | Needs explicit authority; otherwise it is only a claim, assumption, or candidate. |
| `X should continue` | declared continuity expectation, policy, requirement, accepted baseline | History alone can support the candidate but not bind the expectation. |
| `Seed should refresh X` | refresh recommendation or knowledge-quality finding | Advisory; not a command or execution authorization. |
| `Capability C should be used` | recommendation or plan selection | Requires goal relevance, policy compatibility, and decision/command authority before execution. |
| `This relation should have subject type host` | rule/catalog validation expectation | Scoped to projection integrity; not an operator environment expectation. |

## Prior findings reconciled

Required inputs reconciled:

- `docs/expectation_continuity_concern_design_space_audit.md`
- `docs/visibility_target_ownership_concern_reconciliation.md`
- `docs/ownership_model_design_space_audit.md`
- `docs/measurement_ownership_boundary_audit.md`
- `docs/lens_view_reconciliation.md`
- `docs/goal_policy_and_operator_authority_reconciliation.md`
- `docs/capability_verification_promotion_reconciliation.md`
- `docs/observation_refresh_and_knowledge_freshness_reconciliation.md`
- `docs/continuity_frontier.md`

The prior findings remain compatible:

```text
visibility != ownership
measurement subject != entity identity
history != expectation
goal desirability != authority
recommendation != decision
verification != execution authority
refresh need != command
lens/view projection != new State authority
continuity != identity and != mere resemblance
```

The active gap is therefore accurately framed as:

```text
observed visibility
    vs
expected visibility
    vs
operator-significant deviation
```

Existing repository authority can express observed visibility and several kinds
of knowledge-quality or projection-integrity pressure. It cannot generally say
that a particular endpoint or host is intended to continue seeing a particular
mount unless a separate authority source declares or derives that expectation
within a defined boundary.

## Repository evidence inspected

Documentation inputs were the required documents listed above. Implementation
and test evidence was also inspected for current concepts that resemble
expectation authority:

- `seed_runtime/models.py`
- `seed_runtime/facts.py`
- `seed_runtime/state.py`
- `seed_runtime/policy.py`
- `seed_runtime/capability_inventory.py`
- `seed_runtime/capability_verification.py`
- `seed_runtime/capability_promotion_readiness.py`
- `seed_runtime/verification_evidence.py`
- `seed_runtime/integrity_summary.py`
- `seed_runtime/state_views.py`
- `seed_runtime/action_plans.py`
- `seed_runtime/recommendation_ranker.py`
- `tests/test_policy.py`
- `tests/test_state_views.py`
- `tests/test_contradiction_characterization.py`
- `tests/test_capability_candidates.py`
- `tests/test_integrity_summary.py`
- `tests/test_preconditions.py`

## Current should-like concepts

### Goals

Goals are current projected State objects with summary, status, facts, open
questions, and related entities. The goal-authority reconciliation defines them
as operator-owned desired outcomes that Seed may represent for relevance,
explanation, and decision context.

A goal can say:

```text
this outcome is desirable
```

It cannot by itself say:

```text
this operational condition is required
execute this action
this environmental fact is true
```

For the storage example, a goal such as `maintain ingestion reliability` may make
loss of mount visibility relevant. It does not alone authorize `example_host_b should
see mount M` unless the goal is paired with a requirement, policy, declared
expectation, or validated supporting-condition model that connects that goal to
that mount.

### Requirements

`RequirementView` and graph validation use expected subject/object types for
known relationship rules. This is a real should-like concept, but it is scoped to
repository rule/view integrity:

```text
relationship R expects subject type S and object type O
```

That does not create an operational environment expectation. It says whether a
projected relationship conforms to catalog semantics, not whether a node should
mount storage.

### Policy

`PolicyGate` evaluates actions into `allow`, `block`, `require_confirmation`, or
`require_approval`, using known action risk, tool risk, and matching approvals.
Policy can legitimately say behavior should or should not occur within the
execution/request boundary.

Policy can authorize an expectation only when the expectation is actually a
policy rule or requirement, for example:

```text
production observations must be read-only unless approved
example_host_b must retain mount M while service S is active
```

The first shape matches current policy/execution style. The second is not found
as current repository data or schema; it would require a future policy or
requirement representation for operational topology expectations.

### Operator notes and prose

Operator prose is an authority input, not automatically binding authority in all
layers. It may create or update operator-owned intent, goals, decisions,
approvals, requirements, or declared expectations if accepted through the
appropriate interface and preserved with provenance.

The boundary is:

```text
operator statement as evidence/input
    !=
unsupported claim truth
    !=
policy
    !=
command
    !=
action execution authority
```

A statement such as `I expect example_host_b to see mount M` can authorize a declared
expectation if Seed has a concept and event path for declared expectations. It
must not silently become an action such as remounting M, and it must not become a
source-verified observation that M is visible.

### Claims and facts

Facts and claims can say what is represented and supported by evidence. They may
carry confidence, provenance, observed time, expiry, dimensions, and support.
They do not generally say what ought to be true. A user fact might encode a
normative predicate if such a predicate exists, but the current audited storage
visibility predicates are observation/measurement predicates, not expectation
predicates.

### Capabilities and verification

Capability candidates come from evidence such as package facts. Verification
inspection derives status from projected `capability_verified` facts. The
capability verification reconciliation is explicit that candidate preservation,
verification evidence, and `capability_verified` do not equal selection,
permission, approval, execution authority, or tool invocation.

Capability verification can say:

```text
Seed has support that capability C is available/verified/stale/unverified
```

It cannot say:

```text
Seed should use C
example_host_b should see M
```

except as an input to a recommendation, decision, or command path governed by
goal, policy, and authority.

### Staleness and refresh recommendations

Staleness and refresh recommendations are should-like only in the weak advisory
sense:

```text
additional evidence should be considered because support is stale/insufficient
```

The implementation has deterministic `StaleFactRefreshRecommendation` records
that map stale facts to refresh capabilities, and the integrity summary caveats
state that refresh recommendations are inventory signals only; no refresh or
verification is executed. This creates evidence freshness pressure, not an
expectation that an environmental condition should hold.

### Plans and approvals

Action plans are explicitly legacy/experimental and non-executable. They may
record proposed steps and approval requirements. Approvals can satisfy scoped
policy evaluation for an action/scope. These concepts can authorize transitions
inside their own lifecycle, but they do not create operational state
expectations unless the planned/approved item is itself an expectation declaration
or an authorized command.

### Continuation and current work position

Continuity and work-position documents can preserve active inquiry, selected
frontier, constraints, unresolved tensions, validation state, and next safe
moves. This is important for investigation continuity, but it does not make
historical observations into normative environmental expectations. It can
preserve that `whether example_host_b should see mount M` is the current open question.

## Goal / requirement / policy / expectation distinctions

| Concept | Under repository authority | Can say `should`? | Must not become |
| --- | --- | --- | --- |
| Goal | Operator-owned desired outcome represented for relevance and decision context. | Yes, as desirability: `we want outcome O`. | Policy, approval, command, action, evidence truth. |
| Requirement | A mandatory condition inside a defined rule, validation, workflow, or accepted domain model. | Yes, within its defined scope. | Hidden operator intent, unscoped action authority, observation truth. |
| Policy | Governance over allowed, blocked, required, approval-gated, or preferred behavior. | Yes, for behavior and authority transitions. | Goal, evidence, physical execution, operator intent. |
| Expectation | Missing as a general first-class concept; would be a declared or authorized normative baseline for evaluating observations. | Not generally available today. | History, concern, alert, recommendation, action. |
| Concern | A surfaced reason something may matter: ambiguity, deviation, impact, freshness pressure, operator relevance. | Weakly: `this deserves attention`, not `X is required`. | Alert, expectation, command. |
| Alert | Not found as a general implemented authority in this audited path. Would imply notification/escalation semantics. | Only if separately authorized by alert rules. | Raw concern, observation, recommendation. |
| Recommendation | Advisory suggestion related to evidence and goal relevance. | Yes, as `consider doing/observing X`. | Decision, approval, command, action, operator objective. |

## Required questions

### 1. Does any current repository concept mean `X should be true` or `X should continue`?

Yes, but only in scoped ways:

- policy can say behavior should/should not occur;
- requirements and catalog validation can say projected structures should meet
  expected shape/type constraints;
- goals can say outcomes are desirable;
- approvals/decisions can authorize selected transitions;
- refresh recommendations can say evidence acquisition should be considered.

No current general concept was found that means:

```text
this observed topology/visibility condition should be true or continue
```

for arbitrary operational facts such as `example_host_b sees mount M`.

### 2. What is the difference between goal, requirement, policy, expectation, concern, alert, and recommendation?

The central difference is authority and lifecycle:

```text
goal = desired end
requirement = mandatory condition in a scoped model
policy = governance over means/transitions
expectation = authorized normative baseline for evaluating observations
concern = attention-worthy pressure or ambiguity
alert = notification/escalation event under alert rules
recommendation = advisory possible response
```

The repository currently has goals, policies, requirements in some validation
and view contexts, recommendations, and integrity/freshness concerns. It does
not have a general expectation or alert ontology for operational visibility.

### 3. Can an operator statement create an expectation?

Yes, if the system treats the statement as an explicit declared expectation,
policy, requirement, goal, decision, or approval within a known authority path.
The boundary preventing prose from becoming command/action authority is:

```text
operator prose may declare intent or expectation;
policy/decision/command/execution boundaries still gate actions;
evidence boundaries still gate claims about what is true;
projection boundaries still gate what Seed may report as repository knowledge.
```

Thus `operator expects to be informed` can authorize a notification expectation
only if represented as such. It cannot authorize remediation, remounting, or
unsupported claims.

### 4. Can history create an expectation?

No, not by itself. History can create or support:

- continuity evidence;
- a candidate baseline;
- a candidate expectation;
- operator pressure;
- a question for clarification;
- concern from change, ambiguity, or degraded visibility.

History may participate in expectation creation if a future policy or operator
rule says repeated observations may be promoted to an expectation after review or
under explicit caveats. Without that authority, `observed for 180 days` remains
strong evidence of continuity, not a normative `should continue` claim.

### 5. Can staleness or refresh recommendations create expectation?

No. They express evidence freshness/currentness pressure. They can say that
newer evidence should be considered for a purpose. They cannot say that the
underlying world should match the old evidence.

For the example, stale filesystem visibility support can justify refreshing
storage observations. It does not justify `example_host_b should still see M`.

### 6. Can capability verification create expectation?

No. It describes readiness/support status for capabilities. It may enable a
future recommendation or command path if policy and authority allow, but it does
not imply that a capability should be selected or that any environmental state
should hold.

For the example, verified observation capability might support a recommendation
to refresh observations. It does not create a mount visibility expectation.

### 7. For example_host_b storage, what authority is required to say `example_host_b should see mount M`?

One of the following would be required:

1. a **declared expectation** from an authorized operator or accepted
   configuration stating that example_host_b is intended to see M;
2. a **requirement** in an accepted service/topology model stating that the
   relevant ingestion/service role requires M on example_host_b;
3. a **policy** that mandates the visibility condition for a scope;
4. a **goal-derived expectation rule** that explicitly derives supporting
   operational expectations from a goal and accepted topology/requirement model;
5. an **approved baseline promotion** workflow where historical continuity is
   reviewed or policy-promoted into an expectation with provenance and caveats.

Current observation history alone is insufficient.

### 8. If no current concept can say `should`, what concept is missing?

A general concept is missing in this family:

```text
declared expectation
authorized baseline
intended visibility
expected topology
normative observation baseline
operator notification expectation
```

The minimal missing concept is not an alert and not ownership. It is an
authority-bearing expectation record that can preserve:

- subject/scope;
- predicate or condition;
- expected value/dimensions;
- authority source;
- reason or goal relevance;
- provenance;
- effective time and optional expiry;
- whether history is merely evidence or has been reviewed/promoted;
- what deviations may become concerns, recommendations, or alerts.

This audit does not implement or select that concept.

## History vs expectation analysis

History answers:

```text
what was observed before?
what continuity survived across samples?
what baseline might be inferred for review?
```

Expectation answers:

```text
what is authorized as intended, required, or normatively assumed for evaluation?
```

The repository already treats volatile measurements as latest-current samples in
projected support rather than aggregate proof. That is an important boundary:
repeated measurement values do not strengthen into durable truth the way durable
facts may. The ledger may retain history, but the projected State read model does
not currently encode a continuity-derived expectation.

Therefore, the safe current formulation is:

```text
example_host_b historically saw mount M
example_host_b no longer currently appears to see mount M
this is a visibility change and candidate continuity break
it may deserve operator attention depending on goals, freshness, and authority
```

Not:

```text
example_host_b should see mount M
```

unless expectation authority is separately present.

## Staleness / refresh analysis

Staleness is about whether support is current enough for a purpose.
Refresh need is about whether additional evidence would improve knowledge
quality. Refresh recommendation is advisory. None of these says the old state
should continue.

In the example_host_b example:

| Item | Classification |
| --- | --- |
| last filesystem sample for M is old | staleness/freshness finding |
| current support is inadequate for incident triage | refresh need |
| consider refreshing example_host_b filesystem observation | recommendation |
| execute observation now | command only after decision/authority |
| new observation succeeds/fails | observation execution result |

## Capability verification analysis

Capability verification can matter because refresh or diagnostic recommendations
may depend on available observation capabilities. However, the repository draws a
hard line:

```text
candidate evidence != capability_verified
verification evidence != capability_verified
capability_verified != capability selection
capability_verified != execution authority
```

Thus capability verification can support `Seed is ready to observe` or `Seed has
a verified local capability`, not `example_host_b should see M`.

## Operator prose authority boundary

Operator prose can be authoritative for intent only when the operator is the
recognized source of that intent. It can become other authority only through a
recognized transition:

```text
prose -> represented intent/goal
prose -> declared expectation
prose -> policy/configuration update
prose -> decision/approval
prose -> command request
```

Each transition needs its own boundary. This prevents these unsafe collapses:

```text
operator says X is true -> Seed treats X as observed truth
operator wants O -> Seed decides and acts
operator expects notice -> Seed invents alert rules and remediation
operator notes history -> Seed creates normative topology expectation
```

## Example host example analysis

Operational example:

```text
example_host_b historically sees mount M
example_host_b stops seeing mount M
example_host_b ingestion becomes uneven
operator expects to be informed
```

Classification under current authority:

| Statement | Classification | Current authority |
| --- | --- | --- |
| `example_host_b historically sees mount M` | Observation history / continuity evidence | Ledger/history may support this; projected State may only retain latest current measurement support unless history is queried. |
| `example_host_b stops seeing mount M` | Current observation change / visibility loss candidate | Supported if current observations or absence/change analysis exists; absence alone needs caveats. |
| `example_host_b ingestion becomes uneven` | Observation or assessment, depending on evidence | Requires ingestion measurements or operator-provided evidence. |
| `loss of M may explain uneven ingestion` | Hypothesis / concern candidate | Requires causal support before becoming claim. |
| `example_host_b should see M` | Expectation | Not authorized by current history alone; requires declared expectation, requirement, policy, or promoted baseline. |
| `operator expects to be informed` | Operator intent / possible notification expectation | Needs represented expectation or policy to become alert/notification rule. |
| `this deserves attention` | Concern | Can be surfaced as ambiguity/change/freshness/goal-relevance pressure without asserting `should`. |
| `notify operator now` | Alert/action | Requires alert semantics or command/notification authority. |
| `refresh filesystem observation` | Recommendation until accepted | Requires decision/command/execution boundary before observation. |
| `remount M` | Action/remediation | Not authorized by any current audited concept. |

A boundary-preserving phrasing would be:

```text
Seed observed a change in mount visibility for example_host_b relative to historical
continuity evidence. Because ingestion is uneven and the operator has expressed
an information need, Seed may surface a concern or recommend refreshing evidence.
Seed cannot assert that example_host_b should see M unless an expectation authority is
present.
```

## Candidate models

### Model A: Declared Expectation

```text
Only explicit operator/policy/requirement authority can say "should."
```

**Fit:** Strongest fit with current authority boundaries.

**Strengths:** Preserves evidence vs normativity; avoids accidental topology
requirements; gives deviations a clean reference.

**Risks:** Requires operators or configuration to declare important expectations;
may miss emergent continuity breaks until modeled as concerns.

**Audit result:** Compatible and safest, but not implemented as a general
expectation concept.

### Model B: Candidate Expectation From History

```text
Historical continuity can suggest expectation, but cannot assert it.
```

**Fit:** Compatible if the output is explicitly candidate/caveated.

**Strengths:** Captures operator intuition that long stable visibility matters.

**Risks:** Repetition may be incidental, deprecated, or accidental; State does
not currently project rich continuity baselines by default.

**Audit result:** Recommended as an investigation vocabulary, not as authority.

### Model C: Goal-Derived Expectation

```text
A goal or requirement creates expectations over supporting conditions.
```

**Fit:** Partially compatible only if a derivation rule and supporting model are
explicit. Goals alone are too broad.

**Strengths:** Explains why mount visibility matters to ingestion reliability.

**Risks:** Can silently invent operator objectives or hidden requirements if the
supporting-condition model is not explicit.

**Audit result:** Plausible future model; requires separate authority for the
supporting-condition derivation.

### Model D: Concern Without Expectation

```text
Seed surfaces concern from ambiguity/staleness/change without saying "should."
```

**Fit:** Strong fit with current repository authority.

**Strengths:** Allows useful operator attention while preserving the boundary
between observed change and normative expectation.

**Risks:** Concern may be less decisive than alerting; operators may still ask
whether the condition was expected.

**Audit result:** Best current behavior model if any surface is later designed,
but this audit does not implement it.

### Model E: No Expectation Concept Yet

```text
Repository remains current-observation plus freshness/integrity only.
```

**Fit:** Accurate description of current implementation for this storage
visibility question.

**Strengths:** Most conservative and faithful to existing code.

**Risks:** Does not answer the operator's `should I have been informed?` or
`was this supposed to continue?` question.

**Audit result:** Current state. The missing concept remains expectation or
should-authority, not ownership.

## Recommended next investigation

Before operational concern, HomeOps, or SeedOps work resumes, investigate a
small expectation-authority design space without implementation. The next audit
should compare:

1. **declared expectation records**;
2. **policy/requirement-backed topology expectations**;
3. **history-derived candidate baselines with explicit non-authority caveats**;
4. **goal-derived supporting-condition expectations**;
5. **concern surfaces that do not require expectation**;
6. **notification expectations** such as `operator expects to be informed`, kept
   separate from remediation and alert execution.

The investigation should answer which authority sources are allowed to create,
modify, expire, or retire an expectation, and how a deviation differs from a
concern, alert, recommendation, decision, command, and action.

## Non-conclusions

- This audit does not implement expectations.
- This audit does not implement goals, requirements, policies, alerts, concerns,
  HomeOps, or SeedOps.
- This audit does not conclude that history should promote to expectation.
- This audit does not conclude that every declared expectation should alert.
- This audit does not conclude that `example_host_b should see mount M` is true.
- This audit does not conclude that ownership is required to express the
  example_host_b concern.
- This audit does not change State, facts, projections, capability verification,
  refresh recommendations, policy evaluation, plans, approvals, or tests.
