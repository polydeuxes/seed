# Operator Intent, Question, And Claim Interface Reconciliation

## Purpose

This document performs a documentation-only reconciliation of operator intent,
questions, claims, projections, assessments, recommendations, and the
operator-facing interface between them.

It is an architectural boundary audit.

It does not implement code, modify schemas, modify projections, modify
assessments, modify recommendations, modify decisions, modify capabilities,
modify commands, modify actions, modify runtime routing, modify conversational
interfaces, or modify tests.

It does not introduce new runtime semantics.

## Central Question

Recent reconciliation work increasingly characterizes Seed as claim-centric:
claims sit near the center of observation, evidence, fact, relationship, and
projection. Operators, however, do not usually arrive with claim-shaped input.
They arrive with intent:

```text
understand system state
investigate an issue
reduce risk
install software
answer a question
maintain availability
```

The architectural question is therefore:

```text
What sits between operator intent and Seed's claim-oriented knowledge system?
```

## Central Finding

Operators are intent-centric. Seed is claim-centric. Questions form the safest
operator-facing bridge between those domains.

In compact form:

```text
Operators arrive with intent.
Questions express, refine, and operationalize intent.
Claims preserve knowledge.
Projections communicate selected knowledge.
Assessments interpret knowledge.
Recommendations relate interpreted knowledge to possible operator purposes.
```

Intent should not be collapsed into evidence, claims, projections, assessments,
or recommendations. A question should not be treated as a claim merely because
it can be answered using claims. A projection may answer or partially answer a
question without creating a new claim. A recommendation may relate knowledge to
an operator's apparent or declared intent without becoming the intent itself.

The resulting boundary is:

```text
operator concern -> question -> projection/support/provenance -> optional assessment -> optional recommendation
```

This is an interface path, not a new runtime pipeline.

## Files Considered

This reconciliation builds on existing architectural documentation, especially:

- `docs/operator_interface_and_projection_authority_reconciliation.md`
- `docs/assessment_recommendation_and_decision_reconciliation.md`
- `docs/explainability_reconciliation.md`
- `docs/explainability_contract_characterization.md`
- `docs/explanation_contract_vocabulary.md`
- `docs/claim_support_characterization.md`
- `docs/claim_support_design.md`
- `docs/claim_strength_and_assertion_semantics_reconciliation.md`
- `docs/read_model_inventory_and_authority_reconciliation.md`
- `docs/view_authority_and_surface_responsibility_reconciliation.md`
- `docs/recommendation_selection_boundary.md`
- `docs/operator_navigation_reconciliation.md`
- `docs/knowledge_representation_reconciliation.md`
- `docs/relationship_fact_reconciliation.md`
- `docs/evidence_trust_and_source_authority_reconciliation.md`
- `docs/corroboration_and_fact_promotion_reconciliation.md`
- `docs/temporal_reasoning_audit.md`
- `docs/why_not_vocabulary.md`

## Boundary Summary

| Concept | Primary domain | Primary role | Answers | Must not become |
| --- | --- | --- | --- | --- |
| Operator intent | Operator domain, optionally represented at interface boundary | Purpose, goal, concern, task, objective | Why is the operator engaging Seed? | Evidence, claim, fact, projection truth, authorization, action |
| Question | Interface domain between operator and Seed | Inquiry over knowledge, support, state, change, risk, or option space | What does the operator need to know? | Claim, hidden reasoning, mutation request, proof |
| Claim | Seed knowledge domain | Preserved knowledge assertion with support expectations | What is asserted or preserved? | Operator purpose, question, recommendation, decision |
| Projection | Seed read/interface domain | Deterministic communication of selected preserved knowledge | What does this view expose from claims and related records? | New claim authority, assessment by default, recommendation by default |
| Assessment | Interpretive knowledge domain | Evidence-backed interpretation under a scoped evaluative frame | What does this knowledge indicate? | Operator intent, decision, command, action |
| Recommendation | Advisory domain | Suggested possible response related to knowledge and purpose | What could be considered? | Intent, approval, decision, command, action |

## 1. Operator Intent Boundary

Operator intent is the operator's purpose for engaging Seed. It may be a goal,
task, objective, concern, obligation, or desired outcome that motivates an
interaction.

Examples include:

```text
understand system health
investigate why a service is unavailable
reduce operational risk
install software
answer a question
maintain uptime
prepare for a change window
```

Architecturally, intent belongs primarily to the operator domain. It can cross
into Seed's interface domain when the operator states it, when a workflow labels
it, or when a surface needs to preserve a transparent interaction context. That
does not make intent a Seed knowledge claim.

Intent is not evidence. Intent may explain why an operator asked something, but
it does not support the truth of a claim. For example, the intent `maintain
uptime` does not support the claim `endpoint unreachable`; observations,
evidence, facts, relationships, and support records do.

Intent is also not authorization. `Install software` may be an operator's goal,
but the goal alone does not authorize a command, prove capability availability,
or imply policy approval.

### Intent classification

Intent is best classified as:

```text
operator-domain purpose that may be represented at the operator interface boundary
```

It is not purely Seed-domain because Seed's knowledge system should not need to
store an operator's purpose to preserve claims. It is not neither-domain because
operator-facing interfaces may need to accept, display, disambiguate, or explain
which question or recommendation was relevant to a declared purpose.

## 2. Question Boundary

A question is an operator-facing inquiry that requests knowledge, explanation,
comparison, support, change, risk interpretation, or possible next steps.

Examples include:

```text
Why is this host unavailable?
What supports this claim?
What changed?
Should I be concerned?
What can I do next?
Why was this value selected?
Why not another value?
```

A question is not a claim. The question `Why is example_host unavailable?` does not
assert that example_host is unavailable unless separately represented as a claim or
assumption. A question can contain a presupposition, but that presupposition
should be inspectable rather than silently promoted into knowledge.

A question is also not a projection. A projection is a deterministic view over
preserved knowledge. A question may select, parameterize, or navigate to one or
more projections, but it is not itself the view's result.

The safest architectural definition is:

```text
A question is an interface object or interaction act that maps operator concern to a requested read over Seed knowledge, interpretation, support, provenance, or option space.
```

Questions are therefore requests over claims and related knowledge structures,
not claims themselves.

## 3. Relationship Between Intent And Questions

Questions usually express intent, refine intent, or operationalize intent.

Example:

```text
Intent: understand system health
Question: Why is this service unavailable?
```

The question narrows a broad operator purpose into an answerable inquiry. In
other cases, several questions may refine one intent:

```text
Intent: reduce storage risk
Questions:
- Which filesystems are near capacity?
- What evidence supports that assessment?
- What changed recently?
- What remediation options are available?
```

Questions can also be independent interface objects once asked. A stored or
logged question, if such an interface later exists, would still not become the
operator's full intent. It would be a record of an inquiry. The same question can
serve different intents:

```text
Question: What changed?
Intent A: debug an outage
Intent B: audit a deployment
Intent C: explain a compliance drift
```

Therefore:

```text
Questions are expressions and refinements of intent, but they are not identical to intent.
```

## 4. Relationship Between Questions And Claims

Questions consume, select, organize, and inspect claims. They do not become
claims merely by being answerable.

A question may interact with claims in several ways:

| Interaction | Meaning |
| --- | --- |
| Consume claims | Use preserved claims and support to produce an answer or explanation. |
| Select claims | Identify which claims are relevant to the inquiry scope. |
| Compare claims | Surface corroboration, contradiction, freshness, or competing values. |
| Inspect support | Traverse from a claim to observations, evidence, sources, and provenance. |
| Reveal gaps | Show that no claim, no current claim, weak support, stale support, or contradiction exists. |
| Motivate acquisition | Expose that additional observation might be useful, without itself observing. |

A question should not create a factual claim simply because it asks about a
condition. For example:

```text
Question: Why is example_host unavailable?
Potential claim support:
- observation that endpoint probe failed
- fact that endpoint is unreachable
- relationship between endpoint and service
- assessment that outage impact is elevated
```

The question selects a knowledge path. The support path may contain claims. The
answer may communicate projected claims. The question itself remains an inquiry.

If an operator asks a claim-shaped question such as `Is endpoint X
unreachable?`, the answer should distinguish:

```text
asked question: Is endpoint X unreachable?
projected claim: endpoint X is currently selected as unreachable
support: observation/evidence/provenance chain
caveat: freshness, confidence, contradiction, or absence limits
```

## 5. Relationship Between Projections And Questions

Projection authority findings support the following boundary:

```text
Projection is the primary knowledge communication interface; questions are a primary way operators choose what communication they need.
```

Projections can answer questions when the requested answer is within projection
authority. Examples:

```text
Question: What supports this claim?
Projection: support view exposing evidence and provenance

Question: What changed?
Projection: change or current-state view, if such a view is responsible for that comparison

Question: Which value is current?
Projection: current fact view with selection rationale
```

Projections can partially answer questions when the operator asks for more than
the projection can authoritatively communicate:

```text
Question: Should I be concerned?
Projection answer: storage utilization is 96%, evidence is fresh, support count is 3
Remaining need: assessment or operator judgment about risk significance
```

Questions can exist without projections. An unanswered question, out-of-scope
question, malformed question, unsupported question, or future-looking question
may have no available projection answer. In that case the interface should say
what is missing rather than inventing knowledge.

Projections may answer questions without creating claims. A projection that
summarizes current support, exposes provenance, or reports absence of current
support is communicating from preserved knowledge. It is not adding a new
factual assertion unless a separate claim-producing path exists.

## 6. Relationship Between Assessments And Questions

An assessment is an evidence-backed interpretation of knowledge under a scoped
evaluative frame. A question may request such interpretation, but the question
and the assessment remain separate.

Example:

```text
Question: Should I worry about this?
Assessment: storage risk elevated
Support: projected filesystem utilization, freshness, thresholds, affected relationships
```

Assessments may function as answers to evaluative questions when the requested
answer is explicitly interpretive. They may also serve as evidence-like input to
a broader answer, but they are not raw evidence in the same sense as an
observation record. They are interpreted knowledge and should retain their own
support path.

The boundary is:

```text
Questions ask for interpretation.
Assessments provide scoped interpretation.
Claims and projections support the assessment.
```

An assessment should not silently become a recommendation. `Storage risk
elevated` does not itself mean `delete files`, `expand disk`, or `restart
service`. Those are possible responses that require recommendation, decision,
command, and action boundaries.

## 7. Relationship Between Recommendations And Operator Intent

A recommendation is an advisory object or communication that suggests a possible
response to projected or assessed knowledge. It is often useful only relative to
operator intent, but it is not the intent itself.

Example:

```text
Intent: maintain service availability
Assessment: storage risk elevated
Recommendation: investigate storage utilization or expand capacity
```

Recommendations can be intent-dependent in at least three ways:

1. **Relevance:** the same knowledge may suggest different responses under
   different operator goals.
2. **Priority:** an availability intent may prioritize outage mitigation, while a
   cost intent may prioritize capacity efficiency.
3. **Acceptability:** an operator's task, role, policy context, and change window
   may constrain which recommendations are appropriate.

However, a recommendation must not become the operator's goal, decision, or
authorization. It can say what might be considered. It cannot prove that the
operator wants it, approves it, or has authority to execute it.

The safer phrasing is:

```text
Recommendations relate knowledge to intent; they do not become intent.
```

## 8. Explainability Role

Explainability is the operator's ability to move from a question to the
knowledge and provenance that support an answer without relying on hidden
reasoning.

The desired path is:

```text
question
  ↓
projection or projected answer
  ↓
supporting claims / facts / relationships / assessments
  ↓
evidence and observations
  ↓
source, time, scope, confidence, freshness, contradiction, and provenance
```

For evaluative or advisory answers, the path extends:

```text
question
  ↓
projection
  ↓
assessment and its support
  ↓
recommendation and its rationale
  ↓
decision / command / action only if separately selected and authorized
```

This path should preserve inspectable boundaries:

- The question explains what the operator asked.
- The projection explains what Seed selected or exposed.
- Support explains why the selected knowledge is visible.
- Provenance explains where the knowledge came from.
- Assessment rationale explains how knowledge was interpreted.
- Recommendation rationale explains why an option was suggested.
- Decision records, if any, explain who or what selected an option.

No hidden natural-language reasoning layer should replace that chain. A fluent
answer may summarize it, but should preserve navigation back to deterministic
views and provenance.

## 9. What Must Not Be Collapsed Together

The following concepts must remain separate even when they appear in one
operator interaction:

```text
Intent: maintain uptime
Question: why is service unavailable?
Claim: endpoint unreachable
Projection: current availability summary
Assessment: outage detected
Recommendation: investigate connectivity
Decision: operator chooses to investigate now
Command: request approved diagnostic operation
Action: diagnostic operation runs
```

They are different objects because they answer different architectural
questions:

| Object | Architectural question | Why it must remain distinct |
| --- | --- | --- |
| Intent | Why is the operator here? | Purpose is not evidence and does not prove system state. |
| Question | What does the operator need to know? | Inquiry is not an assertion and can be unanswered. |
| Claim | What is asserted or preserved? | Knowledge preservation is independent of why an operator asks. |
| Projection | What does the view expose? | View selection communicates knowledge but should not invent interpretation. |
| Assessment | What does the knowledge indicate? | Interpretation requires scoped rationale and must not become action. |
| Recommendation | What response could be considered? | Advice is not approval or execution. |
| Decision | What option was selected? | Selection requires authority distinct from advice. |
| Command | What execution is requested? | Requesting execution is not the execution result. |
| Action | What happened or changed? | Mutation is external effect, not rationale. |

Collapsing these concepts creates predictable failures:

- Treating intent as evidence makes operator desire look like proof.
- Treating a question as a claim creates unsupported knowledge.
- Treating projection as assessment hides evaluative assumptions.
- Treating assessment as recommendation turns interpretation into advice.
- Treating recommendation as decision bypasses operator or policy authority.
- Treating command as action confuses request with effect.

## 10. Is Seed Claim-Centric, Intent-Centric, Or Something Else?

Seed's knowledge architecture is claim-centric. Its operator experience is
intent-centric. Its read interface is projection-centric. These are not
contradictions; they are domain boundaries.

A concise model is:

```text
Operator domain: intent, concerns, goals, tasks, decisions
Interface bridge: questions, navigation, explanations, answer framing
Seed knowledge domain: claims, evidence, facts, relationships, support, provenance
Read communication domain: projections and surfaces
Interpretive/advisory domain: assessments and recommendations
Mutation domain: decisions, commands, actions, execution effects
```

Claims appear central to Seed because durable knowledge needs support,
provenance, assertion semantics, corroboration, contradiction handling, and
projection. Intent appears central to operators because human engagement starts
from purpose, concern, or desired outcome. Questions appear central at the
interface because they translate intent into a form that can select or inspect
claim-oriented knowledge.

Therefore Seed is not simply intent-centric. Storing intent as the center would
blur knowledge preservation with operator goals. Seed is also not only
projection-centric because projections communicate knowledge derived from
preserved structures; they are not the root of knowledge. The best description
is:

```text
Seed is claim-centric in its knowledge core, projection-centric in its read surfaces, and question-mediated at its operator boundary.
```

## Architectural Invariants

The reconciliation supports the following invariants:

1. Operators arrive with intent.
2. Intent belongs primarily to the operator domain.
3. Intent is not evidence.
4. Intent is not authorization.
5. Questions express, refine, or operationalize intent.
6. Questions are not claims.
7. Questions may contain presuppositions that must not be silently promoted to
   claims.
8. Claims preserve knowledge.
9. Claims require support, provenance, and assertion semantics appropriate to
   their kind.
10. Projections communicate selected preserved knowledge.
11. Projections may answer or partially answer questions without creating new
    claims.
12. Questions can exist without projection answers.
13. Assessments interpret knowledge under scoped evaluative frames.
14. Assessments may answer evaluative questions but remain distinct from
    questions and recommendations.
15. Recommendations relate knowledge to possible operator purposes.
16. Recommendations may be intent-relevant but are not operator intent.
17. Recommendations are not decisions, commands, approvals, or actions.
18. Explainability requires navigation from question to projection to support to
    provenance.
19. Fluent answers must not replace inspectable support chains.
20. Intent, question, claim, projection, assessment, recommendation, decision,
    command, and action must remain architecturally distinct.

## Non-Goals

This document does not recommend or require:

- a new intent schema;
- a new question schema;
- a new claim type;
- a new projection;
- a new assessment mechanism;
- a new recommendation mechanism;
- a new runtime route;
- a new conversational interface;
- a new natural-language reasoning layer;
- a new command, action, or capability path;
- a migration of existing records;
- a change to tests.

The findings are conceptual boundaries only.

## Implementation Implications

No implementation work is required by this reconciliation.

If future work chooses to represent questions or intent, it should preserve the
boundaries documented here:

- represent operator intent, if at all, as interface context rather than claim
  evidence;
- represent questions, if at all, as inquiries over knowledge rather than as
  claims;
- keep question answering read-only unless a separate acquisition, decision, or
  command path is explicitly invoked;
- preserve projection authority as communication over stored knowledge;
- keep assessments inspectably supported by projections, claims, facts,
  relationships, observations, or evidence;
- keep recommendations advisory and separate from decisions, commands, and
  actions;
- expose explainability through deterministic support and provenance paths.

These implications are guardrails for future design, not implementation
recommendations in this document.

## Final Reconciliation

The boundary between operator intent and Seed's claim system should be mediated
by questions and explainable projections.

An operator brings a purpose. The interface should help express that purpose as
one or more questions. Those questions should select, inspect, or navigate
claim-oriented knowledge through projections. Assessments may interpret the
projected knowledge. Recommendations may relate that interpretation to possible
operator purposes. Decisions, commands, and actions remain separate authority and
mutation boundaries.

The shortest safe statement is:

```text
Operators are intent-centric.
Seed knowledge is claim-centric.
Questions bridge operator intent to claim-oriented knowledge.
Projections answer from preserved knowledge.
Assessments interpret projected knowledge.
Recommendations relate interpreted knowledge to possible intent.
Nothing in that chain should silently collapse into another layer.
```
