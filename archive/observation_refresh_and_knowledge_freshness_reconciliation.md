# Observation Refresh And Knowledge Freshness Reconciliation

## Purpose

This document performs a documentation-only reconciliation of observation
freshness, refresh need, stale knowledge, observation sufficiency, refresh
recommendations, and automatic observation boundaries.

It is an architectural boundary audit.

It does not implement code, modify schemas, modify observation sources, facts,
projections, stale-fact logic, refresh logic, schedulers, capabilities,
execution paths, automation behavior, or tests.

It does not introduce new runtime semantics.

## Central Question

Recent reconciliations established claim strength and assertion semantics,
projection authority, assessment/recommendation/decision boundaries, and
capability/execution boundaries. The remaining question is:

```text
When should Seed want more evidence?
```

Examples include:

```text
local host observation is 7 days old
Prometheus data is 5 minutes old
filesystem facts are stale
relationship support is stale
current projections rely on old evidence
```

The question is not only whether Seed can technically observe again. It is
whether Seed can represent that its knowledge quality has degraded, explain why
more evidence would help, recommend evidence acquisition, and keep that
recommendation distinct from command issuance or observation execution.

## Central Finding

Seed should preserve the following conceptual chain:

```text
Observation
  -> Evidence
  -> Claim
  -> Projection
  -> Knowledge-quality assessment
  -> Refresh need
  -> Refresh recommendation
  -> Decision / authority
  -> Command
  -> Observation execution
  -> New evidence
```

The useful shorthand is:

```text
Observations report.
Evidence preserves provenance.
Claims represent propositions.
Projections communicate selected views.
Freshness characterizes currentness of support.
Sufficiency characterizes adequacy of support for a purpose.
Refresh need communicates degraded or inadequate knowledge quality.
Refresh recommendations suggest evidence acquisition.
Commands request observation.
Execution acquires evidence.
```

The central boundary is:

```text
Refresh need is about knowledge quality, not about action authority.
```

Seed may know that knowledge quality is degraded without knowing that a claim is
false. A stale claim is not contradicted merely because it is old. A missing
claim is not contradicted merely because it is absent. An insufficiently
supported claim is not false merely because it lacks corroboration. Refresh is a
path for acquiring evidence, not a proof that the previous projection was wrong.

## Files Considered

This reconciliation builds on existing architectural documentation, especially:

- `docs/claim_strength_and_assertion_semantics_reconciliation.md`
- `docs/evidence_trust_and_source_authority_reconciliation.md`
- `docs/fact_confidence_and_corroboration_reconciliation.md`
- `docs/corroboration_and_fact_promotion_reconciliation.md`
- `docs/relationship_promotion_reconciliation.md`
- `docs/relationship_fact_reconciliation.md`
- `docs/temporal_reasoning_audit.md`
- `docs/knowledge_maintenance_reconciliation.md`
- `docs/assessment_recommendation_and_decision_reconciliation.md`
- `docs/recommendation_selection_boundary.md`
- `docs/capability_authority_and_execution_boundary_reconciliation.md`
- `docs/observation_vs_mutation_reconciliation.md`
- `docs/prometheus_observation_boundary_reconciliation.md`
- `docs/local_host_observation_entity_boundary_reconciliation.md`
- `docs/local_network_observation_audit.md`
- `docs/local_package_observation_adapter_boundary_audit.md`
- `docs/repository_observation_language_boundary.md`
- `docs/self_model_evidence_architecture_reconciliation.md`
- `docs/explainability_reconciliation.md`
- `docs/why_not_explanation_characterization.md`

## Boundary Summary

| Concept | Primary question | Architectural role | Must not collapse into |
| --- | --- | --- | --- |
| Observation | What did a source report, from what vantage point, at what time? | Source-attributed report | Truth, claim selection, execution authorization |
| Evidence | Why may Seed consider this claim? | Provenance and support material | Normalized claim, confidence, authority |
| Claim | What proposition is represented? | Scoped proposition backed by evidence | Current truth, verification, recommendation |
| Projection | What view should Seed communicate from preserved knowledge? | Deterministic or scoped read view | Assessment, recommendation, decision |
| Freshness | How recent is the support relative to the represented question and expected change rate? | Currentness quality of support | Truth, contradiction, sufficiency |
| Staleness | Has support aged beyond the window in which it should be treated as current for a purpose? | Degraded currentness signal | Falsehood, deletion, contradiction |
| Sufficiency | Is the available evidence adequate for this claim, purpose, scope, and risk? | Adequacy assessment | Freshness, confidence alone, source count alone |
| Refresh need | Would additional observation materially improve knowledge quality or reduce uncertainty? | Knowledge-quality assessment/finding | Command, execution, mutation |
| Refresh recommendation | Should evidence acquisition be considered? | Advisory response suggestion | Decision, approval, command |
| Decision | Is the recommendation accepted, rejected, deferred, or escalated? | Selection/authority record | Execution itself |
| Command | What bounded observation is requested now? | Authorized execution request | Recommendation rationale |
| Observation execution | What observation was attempted through which path? | Evidence-acquisition attempt | Claim truth, mutation action |

## 1. What Is Freshness?

Freshness is an architectural quality of evidence support that describes how
recently a source, vantage point, or observation path reported a proposition
relative to the question being asked and the expected change rate of the domain.

Freshness answers:

```text
How current is the support for this knowledge, for this purpose?
```

Freshness does not answer:

```text
Is the claim true?
Is the source authoritative?
Is the evidence sufficient?
Should Seed execute an observation now?
```

Freshness primarily belongs to **observations** and **evidence**, because those
are the structures that preserve observed time, source path, vantage point, and
payload context. Claims and projections may carry or expose freshness-derived
metadata, but the claim itself should not become identical to freshness. A fact
can represent a proposition observed at a time; freshness is how a later view
interprets that observation time for a current or historical purpose.

Freshness can also appear in assessments and recommendations, but only as an
interpretation:

```text
Observation: Prometheus reported target up = 1 at T.
Evidence: that sample came from Prometheus scrape path P.
Claim: target X had reported up = 1 at T.
Projection: current target status is selected from latest compatible samples.
Assessment: currentness is acceptable/degraded for this operational question.
Recommendation: refresh observation if currentness is degraded enough to matter.
```

A projection may communicate freshness because operators need to know whether a
view is based on recent support. A recommendation may cite freshness because it
explains why more observation would help. Neither should turn freshness into
truth.

### Freshness Is Contextual

The same age can be fresh in one domain and stale in another:

| Evidence age | Domain | Possible interpretation |
| --- | --- | --- |
| 10 minutes | Prometheus target health | Potentially stale for live alert triage |
| 10 minutes | Package inventory | Usually fresh enough for inventory review |
| 7 days | Local filesystem capacity | Potentially stale for operational remediation |
| 7 days | Repository structure snapshot | Possibly acceptable for historical audit, weak for current editing |
| 30 days | Installed packages | Possibly stale for patch status, still useful as historical baseline |

Freshness therefore requires a purpose and a domain expectation. Without that
purpose, age is only a timestamp comparison.

## 2. What Is Staleness?

Staleness is a freshness-derived condition in which evidence or selected support
has aged beyond the window in which it should be treated as current for a given
purpose, predicate, domain, or projection.

Staleness answers:

```text
Should this support still be treated as current enough for this use?
```

Staleness does not answer:

```text
Is the claim false?
Has the underlying reality changed?
Was the observation invalid when captured?
```

### Stale But Still Useful

Something can be stale and still useful.

Examples:

```text
A package inventory from 30 days ago may be stale for vulnerability remediation,
but useful as historical evidence that the package existed then.

A filesystem observation from last week may be stale for current capacity
planning, but useful for trend comparison or incident reconstruction.

Relationship support from an old repository observation may be stale for current
architecture review, but useful for explaining why an earlier projection made a
particular claim.
```

Staleness should degrade currentness, not erase history.

### Current But Weakly Supported

Something can be current but weakly supported.

Examples:

```text
A single local observation taken seconds ago may be current but uncorroborated.
A provider sample may be recent but from a low-trust or ambiguous source path.
A fresh relationship inference may depend on one fragile parser result.
```

Freshness does not guarantee sufficiency, trust, corroboration, or truth.

### Historical But Not Stale

Something can be historical and not stale.

Examples:

```text
The question "what did Prometheus report at 12:00 UTC?" is answered by the
historical sample from 12:00 UTC. Its age is not a defect.

The question "what packages were present during the incident last month?" may
require last month's inventory. New observation cannot replace that historical
claim; it can only add current comparison evidence.
```

Historical knowledge is stale only when it is incorrectly used as current-state
support beyond its appropriate currentness window. Age alone is not staleness;
staleness is age relative to purpose.

## 3. What Is Refresh Need?

Refresh need is a knowledge-quality finding that additional observation would be
useful because existing support is stale, missing, insufficient, contradicted,
weakly supported, outside scope, from the wrong vantage point, or inadequate for
the current purpose.

Refresh need answers:

```text
Would more evidence materially improve Seed's ability to assess, select,
explain, or act on this knowledge?
```

Refresh need is best treated as an **assessment/finding about knowledge
quality**, not as a raw claim about the world and not as execution authority.
It may be exposed by a projection as a finding, and it may justify a refresh
recommendation. It is not itself a command.

The distinction is:

```text
Claim: /var usage was reported at 92% seven days ago.
Projection finding: selected filesystem capacity support is old for current
  remediation.
Assessment: observation freshness is degraded.
Refresh need: newer filesystem evidence would materially improve currentness.
Recommendation: refresh local filesystem observation.
Decision: operator or policy accepts/defer/rejects refresh.
Command: execute local filesystem observation for host H.
Execution: adapter collects new filesystem evidence.
```

Refresh need may be grounded in many conditions:

- stale evidence;
- missing evidence;
- insufficient corroboration;
- unsupported projection requirements;
- unresolved contradiction;
- wrong source authority for the question;
- wrong vantage point;
- changed scope;
- high-risk decision context requiring stronger support;
- operator request for current verification.

Because refresh need is a knowledge-quality condition, it should preserve the
reason more evidence is needed. A generic "refresh needed" label is weaker than
an explainable finding such as "local filesystem support is seven days old and
current remediation requires recent local capacity evidence."

## 4. What Is Observation Sufficiency?

Observation sufficiency is the adequacy of available evidence for a scoped
claim, projection, assessment, recommendation, or decision context.

Sufficiency answers:

```text
Do we have enough of the right evidence for this purpose?
```

Sufficiency is not the same as freshness.

| Condition | Freshness | Sufficiency |
| --- | --- | --- |
| One local observation from one minute ago | High | May be low if corroboration or source independence is required |
| Three independent observations from last month | Low for current state | May be sufficient for historical reconstruction |
| No observation | No freshness basis | Insufficient for an evidence-backed claim |
| Fresh provider metric with ambiguous target identity | High sample recency | Insufficient identity support |
| Old but authoritative declaration for intended desired state | Low live currentness | May be sufficient for intent/history, not for live reality |

Seed knows it has enough evidence only relative to a stated purpose and scope.
Sufficiency depends on more than age:

- source authority for the domain;
- trust and failure modes of the observation path;
- independence of corroborating sources;
- predicate semantics;
- entity identity confidence;
- dimensional coverage;
- time coverage;
- contradiction status;
- risk of the downstream decision;
- whether the question is historical, current, predictive, or normative.

Sufficiency should therefore be represented as an assessment over evidence and
requirements, not as a property that can be inferred from observation count or
freshness alone.

## 5. Relationship Between Refresh Need, Recommendation, Decision, Command, And Execution

Seed should preserve explicit boundaries:

```text
Refresh need
  -> Refresh recommendation
  -> Decision
  -> Command
  -> Observation execution
```

### Refresh Need

Refresh need is the finding that knowledge quality would benefit from additional
observation.

It says:

```text
More evidence would help here, and this is why.
```

It does not say:

```text
Go observe now.
```

### Refresh Recommendation

A refresh recommendation is advisory. It suggests evidence acquisition as a
possible response to a refresh need.

It says:

```text
Consider refreshing local host observations for host H.
```

It does not decide that the observation will occur.

### Decision

A decision accepts, rejects, defers, escalates, or otherwise selects a response
to the recommendation. The decision may come from an operator, policy, recorded
workflow, or future authority path.

It says:

```text
This recommendation is approved/deferred/rejected for this reason.
```

It is not the observation itself.

### Command

A command is a bounded, authorized request to perform observation through a
capability path.

It says:

```text
Execute this observation scope now, using this capability/provider path, with
this authority and these constraints.
```

It does not prove that observation succeeded.

### Execution

Observation execution is the attempted collection of evidence through a concrete
adapter, provider, tool, or handoff path.

It says:

```text
The observation was attempted and produced these outputs, errors, or evidence.
```

Execution may acquire evidence. It may fail. It may produce partial or
contradictory evidence. It should not be collapsed into the recommendation that
motivated it.

## 6. When Should Seed Recommend Refresh?

This reconciliation does not define runtime thresholds, scheduler behavior, or
policy implementation. It defines conceptual conditions that may justify
recommendations.

### No Recommendation

No refresh recommendation may be appropriate when:

- evidence is fresh enough for the current purpose;
- support is sufficient for the risk level;
- the question is historical and current observation would not answer it;
- the claim is already known to be out of scope;
- refresh would require authority Seed does not have and the current context does
  not justify escalation;
- the operator has already rejected or deferred refresh for this context;
- additional observation would be redundant or would not materially improve the
  answer.

### Refresh Recommendation

A refresh recommendation may be appropriate when:

- current-state support is stale for the domain;
- evidence is missing for a required predicate, entity, relationship, dimension,
  or vantage point;
- support is weak or uncorroborated for a decision-sensitive claim;
- evidence is recent but from the wrong source authority or vantage point;
- projections depend on old evidence while presenting current-state conclusions;
- a contradiction could be clarified by a newer or more authoritative
  observation;
- operator-facing explainability would materially improve with current evidence;
- a capability exists for read-only observation and the expected risk is low.

### Urgent Refresh Recommendation

An urgent refresh recommendation may be appropriate when:

- stale or missing evidence affects a high-impact operational decision;
- current projection could cause unsafe or misleading action if treated as live;
- contradiction affects a critical entity, dependency, target, service, or
  authority boundary;
- evidence age exceeds the tolerance for a live incident, security review,
  destructive action preflight, or other high-risk context;
- the cost and risk of read-only refresh are low relative to the risk of acting
  on degraded knowledge.

Urgency still does not authorize execution by itself. It explains the priority
and risk of the knowledge gap.

## 7. When May Observation Occur Automatically?

Automatic observation boundaries should be evaluated separately from mutation
boundaries. Observation is lower risk than mutation, but it is not risk-free.
It may consume resources, disclose information, trigger provider costs, touch
network boundaries, alter access logs, or cross privacy and authority domains.

### Candidate Categories For Automatic Refresh

The strongest candidates for automatic refresh are bounded, read-only,
low-impact observations where Seed already has appropriate capability support,
source trust, scope, and authority.

Examples:

```text
read-only local state inspection within an explicitly managed host scope
read-only projection/cache recomputation from existing durable events
read-only local repository/documentation inspection within the active workspace
read-only provider queries inside an already authorized integration scope
```

Even these candidates require explainability: Seed should be able to explain why
observation was attempted, what scope was used, which authority allowed it, and
what evidence was produced or why execution failed.

### Categories Requiring Explicit Authority

Explicit authority is conceptually required when observation crosses a boundary
that changes risk, cost, privacy exposure, or external effect.

Examples:

```text
network observation beyond a previously approved local or provider scope
provider observation that may incur cost, rate limits, audit events, or data
  disclosure
credentialed inspection of systems or tenants not already in scope
observation of sensitive identity, user, secret, or security posture data
observation whose result may be used as preflight for mutation
```

These may still be read-only, but read-only does not mean authority-free.

### Categories Requiring Additional Justification

Additional justification is needed when observation is likely to be noisy,
intrusive, expensive, privacy-sensitive, or operationally consequential.

Examples:

```text
broad network scanning
cross-tenant cloud inventory
security-sensitive enumeration
high-frequency polling outside established telemetry paths
observations that may trigger alarms, provider throttling, or compliance logs
```

### Mutating Actions

Mutating actions remain outside automatic refresh unless a separate decision,
command, and mutation authority path authorizes them. Refresh of evidence should
not silently become remediation.

```text
Refresh recommendation: collect current package inventory.
Not equivalent to: update packages.

Refresh recommendation: observe service status.
Not equivalent to: restart service.
```

## 8. What Role Does Authority Play?

Automatic refresh does not remove authority requirements. It changes which
authority question is being asked.

For mutation, the authority question is:

```text
May Seed change this thing?
```

For observation refresh, the authority question is:

```text
May Seed inspect this thing, from this vantage point, at this time, for this
purpose, using this capability path?
```

Refresh authority should usually be weaker than mutation authority, but it must
still be explicit enough to explain:

- scope of observation;
- source or provider path;
- data sensitivity;
- credential use;
- expected side effects such as logs, costs, or rate limits;
- whether the observation is local, provider-mediated, networked, or
  cross-boundary;
- whether results may influence later recommendations or commands.

Automatic refresh also does not change trust requirements. A source may be
authorized to observe a domain while still being low-trust, partial, stale, or
ambiguous. Authority answers whether the source may report; trust and evidence
quality answer how much Seed should rely on the report.

## 9. What Role Does Provenance Play?

Provenance is required for explaining refresh recommendations, refresh
execution, and non-execution.

### Why Was Refresh Recommended?

A refresh recommendation should be traceable to the knowledge-quality finding
that motivated it:

```text
which claim/projection/relationship was affected
which evidence supported it
how old or incomplete the evidence was
which scope or purpose made that age/absence insufficient
which capability category could acquire better evidence
what risk or uncertainty would remain
```

### Why Was Refresh Executed?

Refresh execution should be traceable to the decision and authority path:

```text
which recommendation or operator request led to execution
who or what approved it
which command scope was selected
which capability/provider/adapter path was used
what time and vantage point were used
what evidence, errors, or partial results were produced
```

### Why Was Refresh Not Performed?

Non-execution should also be explainable:

```text
no capability available
authority missing
operator rejected or deferred
risk too high
question was historical rather than current
refresh would not improve sufficiency
source out of scope
network/provider boundary not authorized
```

A why-not explanation is as important as a why explanation because it prevents
users from mistaking non-refresh for certainty.

## 10. What Should Not Be Collapsed Together?

Seed should preserve distinctions among degraded knowledge conditions.

| Condition | Meaning | Why it is distinct |
| --- | --- | --- |
| Stale | Evidence is too old for current use | The old claim may remain historically valid and useful |
| Missing | No evidence exists for the needed scope | There is no proposition to contradict yet |
| Contradicted | Competing evidence supports incompatible claims | More evidence may help, but age is not the essence of the problem |
| Unverified | Claim has not been checked by a required verification path | It may still be supported by observations |
| Insufficiently supported | Evidence is inadequate for a purpose | Evidence may be fresh but too weak, narrow, or non-independent |
| Weakly trusted | Source path has limited reliability for the domain | Evidence may be fresh and sufficient in count but low in source quality |
| Out of scope | Evidence exists, but not for the relevant entity, dimension, or vantage point | Refresh should target scope, not merely recency |
| Historical | Claim intentionally describes a past state | New observation cannot replace the historical evidence |
| Ambiguous identity | Evidence may refer to the wrong entity | Freshness cannot solve identity ambiguity by itself |

Collapsing these into a single "bad knowledge" or "refresh needed" state would
hide the reason for uncertainty and make recommendations less explainable.

## Required Findings

### Freshness Is Not Truth

Freshness increases confidence that support may reflect current reality, but it
does not prove the claim. A fresh observation can be wrong, partial,
misattributed, unauthoritative, or from the wrong vantage point.

### Staleness Is Not Contradiction

A stale fact is not contradicted merely because time passed. Contradiction
requires incompatible support. Staleness means the old support may no longer be
adequate for current-state use.

### Historical Knowledge Is Not Necessarily Stale Knowledge

Historical knowledge is stale only when misused as live current-state support.
For historical questions, older evidence may be exactly the correct evidence.

### Refresh Need Is Distinct From Execution

Refresh need describes a knowledge-quality gap. Execution is an attempted
collection of evidence. The former may justify the latter, but they are not the
same event and should not share authority semantics.

### Refresh Recommendation Is Distinct From Refresh Execution

A recommendation suggests evidence acquisition. It does not approve, command, or
perform that acquisition.

### Observation Sufficiency Is Distinct From Observation Freshness

Freshness is about recency. Sufficiency is about adequacy for a purpose. A fresh
single observation may be insufficient; old corroborated observations may be
sufficient for historical reconstruction.

### Knowledge Quality Can Degrade Without Proving Falsity

Seed may know that support is old, weak, missing, or out of scope without knowing
that the represented claim is false. This distinction preserves conservative
reasoning and avoids automated truth overreach.

### Automatic Observation Boundaries Are Separate From Mutation Boundaries

Read-only observation should have a lower authority burden than mutation, but it
still requires scope, authority, trust, and explainability review. Automatic
refresh must not become automatic remediation.

## Architectural Invariants

The findings support the following architectural invariants:

1. Observation creates evidence.
2. Evidence supports claims.
3. Claims represent scoped propositions, not universal truth.
4. Projections communicate selected knowledge views.
5. Freshness affects confidence in currentness, not historical preservation.
6. Stale is not false.
7. Missing is not contradicted.
8. Contradicted is not merely stale.
9. Unverified is not unsupported by definition.
10. Observation sufficiency is distinct from observation freshness.
11. Refresh need communicates knowledge quality.
12. Refresh recommendations suggest evidence acquisition.
13. Refresh recommendations do not authorize execution.
14. Refresh execution acquires evidence.
15. Observation execution is not mutation merely because it records evidence.
16. Mutation authority remains stronger than refresh authority.
17. Refresh authority should be weaker than mutation authority but still
    explainable.
18. Automatic observation boundaries should be evaluated by scope, source,
    sensitivity, cost, side effects, and authority.
19. Historical knowledge must be preserved even when it is not selected as
    current.
20. Provenance must explain why refresh was recommended, executed, or not
    performed.

## Non-Goals

This reconciliation does not:

- define runtime freshness thresholds;
- add expiration policies;
- modify stale-fact logic;
- modify fact support or confidence calculations;
- modify projection behavior;
- introduce schedulers or automatic refresh loops;
- define provider polling intervals;
- add new schemas, records, fields, or events;
- change capability registration or selection;
- change command or execution routing;
- authorize observation or mutation;
- resolve contradictions automatically;
- collapse refresh recommendation into command issuance;
- convert read-only observation into remediation.

## Implementation Implications

No implementation work is required by this document.

If future implementation work is considered, these findings imply constraints
rather than feature requirements:

- preserve provenance between stale/missing/insufficient/contradicted findings
  and any refresh recommendation;
- keep refresh recommendation separate from decision, command, and execution;
- keep observation refresh separate from mutation/remediation;
- explain authority for automatic observation even when the operation is
  read-only;
- avoid treating freshness thresholds as universal truth rules;
- avoid treating historical evidence as defective merely because it is old;
- avoid representing all knowledge-quality problems as staleness.

These are guardrails for future design, not a request to implement new behavior.

## Conclusion

Seed should reason about refresh as evidence acquisition motivated by knowledge
quality, not as automatic truth repair.

Freshness and staleness describe currentness of support. Sufficiency describes
adequacy of support for a purpose. Refresh need describes why more evidence
would help. Refresh recommendations suggest evidence acquisition. Decisions and
commands authorize bounded observation. Execution attempts to acquire new
evidence. Mutation remains a separate authority class.

Preserving these boundaries lets Seed explain what it knows, what it does not
know, why current knowledge may be degraded, why refresh may help, and why
refresh was or was not performed without implying that stale, missing,
insufficient, unverified, contradicted, and historical knowledge are the same
condition.
