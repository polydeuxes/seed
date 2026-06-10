# Language Candidate Routing And Promotion Reconciliation

## Purpose

This document performs a documentation-only reconciliation of language-derived
candidate structures, routing, promotion, interpretation outputs, authority
boundaries, and transition points between interpretation and structured
knowledge.

It is an architectural boundary audit.

It does not implement code, modify schemas, modify runtime behavior, modify
observations, claims, recommendations, decisions, commands, projections,
authority systems, federation behavior, execution behavior, or tests.

It does not introduce new runtime semantics.

## Central Question

Recent reconciliations established that natural language observes communicative
acts, interpretation derives candidate meaning, Seed is claim-centric,
recommendations, decisions, commands, and actions are distinct, goals remain
operator-owned, and language authority differs from environmental truth
authority.

The remaining question is:

```text
What happens after interpretation produces candidate meaning from a communicative act?
```

Example:

```text
Operator says: Check why nginx is down.
```

Interpretation may derive:

```text
question candidate: Why is nginx down?
investigation candidate: inspect nginx availability and related evidence
entity candidate: nginx
constraint candidate: scope is nginx-related investigation
goal candidate: understand or restore nginx availability
command candidate: check/investigate, not necessarily restart
claim candidate: the utterance presupposes nginx is down
```

The architectural issue is not whether these candidates are useful. They are.
The issue is which transitions are allowed, explainable, and authoritative.

## Central Finding

Interpretation produces candidates, not immediate truth and not immediate work.

The stable conceptual chain is:

```text
communicative act
  -> language observation
  -> interpretation
  -> candidate structures
  -> routing
  -> promotion, clarification, verification, recommendation, decision, command, refusal, or no-op boundary
```

This is a conceptual decomposition, not a required runtime pipeline.

A language-derived candidate is an explainable, source-attributed,
interpretation-produced possibility that some structured object may be relevant.
It is not automatically a claim, question, goal, constraint, recommendation,
decision, command, or task. It may be routed toward one of those domains, but
routing is not authority. It may be promoted into a durable or actionable
structure, but promotion requires the authority, support, and scope appropriate
to the target structure.

The most important distinction is:

```text
Interpretation answers: what meaning may be present in this source?
Routing answers: which architectural boundary should consider this candidate?
Promotion answers: what structured object is created or accepted, under which authority and support?
Verification answers: whether an external-world assertion is supported by appropriate evidence.
Execution answers: what actually changed or was attempted in the environment.
```

## Files Considered

This reconciliation builds on existing architectural documentation, especially:

- `docs/natural_language_observation_and_intent_derivation_reconciliation.md`
- `docs/operator_intent_question_and_claim_interface_reconciliation.md`
- `docs/goal_policy_and_operator_authority_reconciliation.md`
- `docs/assessment_recommendation_and_decision_reconciliation.md`
- `docs/input_source_authority_reconciliation.md`
- `docs/input_act_vocabulary.md`
- `docs/input_inspection_reconciliation.md`
- `docs/claim_support_characterization.md`
- `docs/claim_support_design.md`
- `docs/claim_strength_and_assertion_semantics_reconciliation.md`
- `docs/evidence_strength_and_claim_strength_reconciliation.md`
- `docs/evidence_trust_and_source_authority_reconciliation.md`
- `docs/corroboration_and_fact_promotion_reconciliation.md`
- `docs/relationship_promotion_reconciliation.md`
- `docs/recommendation_selection_boundary.md`
- `docs/capability_authority_and_execution_boundary_reconciliation.md`
- `docs/prometheus_observation_boundary_reconciliation.md`
- `docs/prometheus_endpoint_identity_boundary_audit.md`
- `docs/prometheus_target_and_filesystem_identity_reconciliation.md`
- `docs/entity_identity_derivation_reconciliation.md`

## Boundary Summary

| Concept | Definition | May become | Must not become automatically |
| --- | --- | --- | --- |
| Communicative act | A speaker's utterance, message, form input, transcript fragment, or other intentional communication event. | Language observation. | Claim truth, authorization, command execution. |
| Language observation | Preserved communicative act with source, time, scope, and attribution context. | Evidence about what was communicated. | Environmental truth. |
| Interpretation | Source-specific derivation of possible meaning from an observation. | Candidate structures. | Verification, authority, execution. |
| Candidate structure | Source-attributed possible structured meaning awaiting boundary-specific handling. | Claim, question, goal hypothesis, constraint, recommendation request, task candidate, command candidate, entity candidate, relationship candidate. | Durable fact, owned goal, executable command, policy, environmental truth. |
| Routing | Non-authoritative dispatch or classification of a candidate toward a domain that can evaluate it. | Review, clarification, support check, promotion path, refusal path. | Promotion, authorization, verification. |
| Promotion | Explainable acceptance of a candidate into a target structured object under target-specific support and authority. | Structured knowledge or structured work object. | Hidden inference, silent authority transfer. |
| Verification | Evidence evaluation for an external-world assertion. | Stronger or weaker claim support. | Interpretation, routing, command approval. |
| Execution | Attempted or completed environmental mutation. | Action record or result observation. | Interpretation, recommendation, decision by itself. |

## 1. What Is A Language-Derived Candidate?

A language-derived candidate is an interpretation output that proposes a possible
structured reading of a communicative act while preserving uncertainty,
attribution, source scope, and the derivation path.

It should be understood as:

```text
candidate = interpreted possibility + source attribution + scope + confidence/caveat + target-domain hint
```

It is best classified as an interpretation product, not as an observation and
not as a claim by default.

### Candidate classification

A candidate is not the raw observation. The raw observation is the preserved
communicative act, such as the text `Check why nginx is down.` The candidate is
the derived structure, such as `question: why is nginx down?` or `entity: nginx`.

A candidate is not automatically a claim. A statement like `nginx is down` may
produce a claim candidate, but that candidate still needs support and authority
rules before it becomes a claim about the environment.

A candidate is not verification. Interpretation may recognize that an utterance
presupposes downtime, but it has not checked Prometheus, logs, service status,
network reachability, recent changes, or operator-provided evidence.

A candidate is similar to a hypothesis in that it may be wrong, incomplete, or
ambiguous. However, it is broader than a factual hypothesis because it may point
toward non-factual structures such as questions, constraints, task candidates,
command candidates, or goal hypotheses.

Therefore:

```text
language-derived candidate
  == source-attributed interpretation product
  != observation
  != verified fact
  != authority
  != execution request accepted for execution
```

### Candidate fields conceptually needed for explanation

This audit does not define a schema, but the architectural explanation of a
candidate should be able to answer:

```text
What source observation produced it?
Which text span, channel, or communicative feature supports it?
Which interpreter or method derived it?
What is its target domain hint?
What ambiguity remains?
What authority would be needed to promote it?
What evidence would be needed to verify any environmental assertion?
What downstream boundary considered it?
```

## 2. What Is Routing?

Routing is the non-authoritative movement, dispatch, or classification of a
candidate toward the architectural boundary that can evaluate it.

Routing answers:

```text
Who or what should consider this candidate next?
```

It does not answer:

```text
Is this candidate true?
Is this candidate authorized?
Has this candidate been accepted?
Should this candidate execute?
```

Examples:

```text
question candidate -> question/interface boundary
claim candidate -> claim support and evidence boundary
entity candidate -> identity derivation boundary
constraint candidate -> policy/preference/scope boundary
command candidate -> command/authorization/capability boundary
goal candidate -> operator-intent/goal-ownership boundary
recommendation request candidate -> recommendation-selection boundary
```

Routing differs from promotion because routing can occur before any target
object exists. It is allowed to say, "this looks like a command candidate; send
it to the command boundary for validation," without creating a command. It is
allowed to say, "this looks like a claim candidate; send it to support review,"
without asserting the claim.

Routing differs from authority because a route is an architectural path, not a
right to bind Seed or the environment. A classifier can route `delete logs` to a
high-risk command boundary. That route does not authorize deletion.

## 3. What Is Promotion?

Promotion is the explainable acceptance of a candidate into a target structured
object under the support, authority, scope, and lifecycle rules of that target.

Promotion answers:

```text
What has this candidate become, and why was that transition allowed?
```

Promotion must preserve the derivation path:

```text
source observation
  -> interpretation output
  -> routed target boundary
  -> required support/authority checks
  -> promoted structured object or non-promotion reason
```

Promotion is target-specific.

### Promotion to a claim

A candidate becomes a claim only when the claim boundary accepts it as an
assertion with support expectations, attribution, scope, and caveats.

Language can directly support claims about the communicative act:

```text
The operator requested an investigation of nginx.
The operator asserted that nginx is down.
The operator prohibited restarting anything.
```

Language alone does not verify external-world claims:

```text
nginx is down
node115 is unhealthy
disk is full
Prometheus target is unavailable
```

Those may become weak, attributed, source-scoped claims such as "operator
reported nginx down" or claim candidates pending environmental corroboration.
They should not silently become environmental facts.

### Promotion to a question

A question candidate becomes a question when Seed accepts it as an inquiry over
knowledge, support, provenance, state, change, risk, or option space.

Example:

```text
Utterance: Check why nginx is down.
Question candidate: Why is nginx down?
Promoted question: What evidence explains nginx unavailability or the report of it?
```

The promoted question does not assert the presupposition. It selects an inquiry
path and may carry explicit assumptions or presuppositions for inspection.

### Promotion to a goal hypothesis

A goal-like candidate becomes a goal hypothesis when interpretation suggests a
desired outcome but the operator has not clearly owned, confirmed, or delegated
that goal.

Example:

```text
Check why nginx is down.
```

Possible goal hypotheses:

```text
understand nginx availability
restore nginx availability
reduce outage duration
```

Only the first may be strongly supported by the language. The others may be
plausible but should remain hypotheses unless confirmed by the operator,
workflow context, policy, or another authorized source.

### Promotion to an operator-owned goal

A candidate becomes an operator-owned goal only when the operator or authorized
workflow establishes ownership of the objective. Interpretation alone cannot
create operator-owned goals. It can expose candidates and ask for clarification.

Examples:

```text
Operator: My goal is to restore nginx service.
Operator workflow: Incident response objective is restore service.
Operator confirmation: Yes, optimize for restoration, not just diagnosis.
```

### Promotion to a constraint

A constraint candidate becomes a constraint when it is accepted as a scoped
restriction, requirement, preference, prohibition, priority, or policy-relevant
input under the authority of its source.

Examples:

```text
Do not restart anything.
Only inspect read-only data.
Prioritize safety over speed.
Avoid changes before the maintenance window.
```

Language can be authoritative for operator-owned constraints when the speaker
has the authority to constrain the interaction. It still does not prove claims
about the environment. `Do not restart nginx because it is serving traffic` may
promote the prohibition as an operator constraint while leaving `nginx is serving
traffic` as an environmental claim candidate requiring evidence.

### Promotion to a recommendation request

A recommendation-request candidate becomes a recommendation request when the
language asks for options, next steps, tradeoffs, or advice.

Example:

```text
What should I do about nginx being down?
```

This is not itself a recommendation. It is a request for advisory output. Any
recommendation still needs evidence path, goal relevance path, caveats, and a
separate decision boundary.

### Promotion to a task candidate

A task candidate is a candidate structured work item, not necessarily an
authorized task. It may represent possible work to investigate, inspect, draft,
plan, reconcile, or prepare.

Example:

```text
Check why nginx is down.
```

Possible task candidate:

```text
Investigate nginx availability using available read-only evidence.
```

Promotion to a durable task-like object would require scope, owner, authority,
and lifecycle rules. This audit does not add such a runtime object.

### Promotion to a command candidate

A command candidate becomes a command candidate when interpretation identifies a
bounded operation request. It becomes an actual command only if the command
boundary accepts it under the applicable authority, policy, capability, risk,
validation, and decision rules.

Example:

```text
restart nginx
```

Command candidate:

```text
operation: restart
object: nginx service
```

Not yet:

```text
authorized command
approved command
executed action
successful restart
```

## 4. What Authority Does Language Provide?

Language provides authority only for structures whose truth or force is about
the communicative act or the speaker's own authorized intent, preference, request,
or constraint.

### Usually authoritative from language, subject to source identity and scope

Language may be authoritative for:

```text
operator request: the operator asked Seed to do or answer something
operator prohibition: the operator told Seed not to do something within the interaction
operator preference: the operator expressed a preference or priority
operator assertion-as-assertion: the operator asserted a proposition
operator confirmation: the operator confirmed a goal, decision, or constraint
operator correction: the operator corrected prior language or interface state
```

Even here, authority depends on source identity and scope. An anonymous webhook,
uncertain voice transcript, local CLI session, authenticated administrator, and
read-only viewer do not have equal authority.

### Not authoritative for environmental truth by itself

Language is not authoritative by itself for:

```text
nginx is down
the host is healthy
the scrape target equals the host
the filesystem is full
the action succeeded
the dependency is safe
```

Such statements may be operator assertions, reports, beliefs, or assumptions.
They need environmental evidence, corroboration, or appropriate claim support to
be promoted beyond attributed language-derived claims.

### Mixed authority in one utterance

Many utterances contain both authoritative and non-authoritative parts:

```text
Do not restart nginx because it is down due to a deploy.
```

Potential structures:

```text
operator prohibition: do not restart nginx       -> may be authoritative as a constraint
claim candidate: nginx is down                   -> requires evidence for environmental truth
claim candidate: deploy caused downtime          -> requires causal support
entity candidates: nginx, deploy                 -> require identity handling
question candidate: what explains downtime?      -> may be promoted as inquiry
```

The prohibition can be honored while the environmental explanation remains
unverified.

## 5. What Is A Question Candidate?

A question candidate is an interpretation-derived possible inquiry over Seed
knowledge, evidence, support, provenance, change, risk, alternatives, or
explanation.

It differs from a claim because it asks rather than asserts. It may contain a
presupposition, but that presupposition must remain inspectable.

It differs from a recommendation because it requests an answer or option space;
it does not advise a course of action.

It differs from a task because it does not by itself assign work. A question can
lead to investigative work, but only after routing and boundary-specific
promotion.

Examples:

```text
Why is nginx down?                         -> question candidate
Is nginx down?                             -> question candidate over a possible claim
What changed before nginx went down?       -> question candidate over events/change
What should I do next?                     -> recommendation-request candidate plus question candidate
```

A question candidate may be promoted when Seed can represent the inquiry and
its assumptions explicitly. It may remain candidate-only when the intended
subject is ambiguous, the source is untrusted, the question embeds unsafe
instructions, or the inquiry cannot be scoped.

## 6. What Is A Goal Candidate?

A goal candidate is an interpretation-derived possible desired outcome implied
or stated by language.

It differs from an operator-owned goal because ownership and commitment have not
necessarily been established.

Examples:

```text
Check why nginx is down.
  strong goal candidate: understand nginx availability or failure cause
  weaker goal candidate: restore nginx service
  weaker goal candidate: minimize incident duration

Make this safer.
  goal candidate: reduce risk
  ambiguity: safer for whom, under which constraints, and by what measure?
```

Interpretation alone cannot create goals because Seed must not silently invent
operator objectives. Interpretation can create goal candidates or goal
hypotheses, display them, use them cautiously for clarification, or relate them
to recommendation relevance only when appropriately caveated.

Goal candidates become operator-owned goals through operator declaration,
confirmation, delegated workflow authority, or another established authority
path. Until then, they should not authorize recommendations, decisions, commands,
or actions as if the operator had committed to them.

## 7. What Is A Constraint Candidate?

A constraint candidate is an interpretation-derived possible limitation,
requirement, prohibition, priority, preference, or scope condition.

Examples:

```text
Do not restart anything.
Only use read-only checks.
Prioritize reliability over speed.
Avoid customer-impacting changes.
Keep this within the nginx namespace.
```

Constraints differ from claims because they regulate acceptable behavior or
choice rather than assert environmental truth. A constraint may be true as a
record of what the operator said, but its normative force depends on source
authority and scope.

Constraint candidates include several subtypes:

```text
prohibition candidate: do not perform X
permission boundary candidate: only perform X under Y
preference candidate: prefer A over B
priority candidate: optimize A before B
scope candidate: consider only these subjects or time windows
safety constraint candidate: avoid specified risk classes or effects
policy reference candidate: follow policy P
```

A constraint candidate may remain candidate-only when source authority is
uncertain, scope is ambiguous, it conflicts with higher-priority policy, or it
contains an environmental premise that has not been verified.

## 8. What Is A Command Candidate?

A command candidate is an interpretation-derived possible bounded operation
request.

Examples:

```text
restart nginx
delete logs
install docker on node116
run the migration
scale the service to three replicas
```

Command-like language is not automatically a command because command acceptance
requires more than syntax. It requires at least:

```text
source identity and authority
scope and target identity
policy and risk evaluation
capability availability
validation against allowed operations
decision or approval when required
clear distinction from planning, explanation, or hypothetical discussion
```

The utterance `restart nginx` may be:

```text
a direct request from an authorized operator
a suggestion quoted from a runbook
a hypothetical option under discussion
a malicious instruction from an untrusted source
a transcript fragment from someone else
a clarification example rather than a request
```

Therefore the safe boundary is:

```text
command-like language
  -> command candidate
  -> command boundary review
  -> possible decision/approval/command
  -> possible execution/action
```

The command candidate can be useful for planning, refusal, clarification, or
requesting approval without becoming execution.

## 9. Relationship Between Interpretation And Structured Knowledge

Interpretation is how source observations become candidate meaning. Structured
knowledge is what Seed preserves, explains, queries, and projects under claim,
relationship, identity, support, and authority rules.

The transition from interpretation to structured knowledge must be explainable:

```text
source observation: operator said "Check why nginx is down"
interpretation: derived question candidate and claim presupposition candidate
routing: question boundary, claim-support boundary, entity-identity boundary
promotion: accepted question about nginx availability; preserved operator-request claim
non-promotion: did not promote "nginx is down" to environmental truth without evidence
```

Interpretation outputs become explainable structures only when their target
boundary accepts them. This allows Seed to preserve candidate structures before
promotion, expose why a candidate was not promoted, and avoid hiding authority
transfers inside natural-language understanding.

## 10. What Should Not Be Collapsed Together?

### Interpretation != Promotion

Interpretation derives possible meaning. Promotion accepts a candidate into a
target structure. Collapsing them would let an extractor silently create facts,
goals, tasks, or commands.

### Candidate != Claim

A candidate may be claim-shaped, but a claim has support expectations,
attribution, and lifecycle semantics. Collapsing them would treat every parsed
assertion as knowledge.

### Question != Recommendation

A question asks for knowledge, explanation, or option space. A recommendation
advises what could be considered in relation to knowledge and purpose.
Collapsing them would make `What should I do?` equivalent to Seed choosing what
to do.

### Goal Candidate != Goal

A goal candidate is an inferred possible objective. A goal is operator-owned or
authorized. Collapsing them would allow Seed to invent intent and then recommend
or act in service of that invented intent.

### Constraint != Environmental Truth

A constraint governs behavior. Environmental truth describes the world. `Do not
restart because nginx is serving traffic` contains a possible constraint and a
possible environmental assertion. They need different authority paths.

### Command Candidate != Command

A command candidate is parsed operation-like meaning. A command is an accepted
bounded execution request. Collapsing them would turn language into execution.

### Routing != Authority

Routing selects a boundary for review. Authority permits or forbids a transition.
Collapsing them would let a classifier authorize work.

### Interpretation != Verification

Interpretation explains what a source appears to mean. Verification evaluates
whether an external-world assertion is supported. Collapsing them would let
fluent language masquerade as evidence.

### Observation Source Semantics != Shared Target Semantics

Different observation sources may all produce candidates, but their candidate
semantics are source-specific. A Prometheus `up == 0` candidate and an operator
statement `nginx is down` may both route toward availability reasoning, but they
carry different vantage points, support implications, and authority.

## Special Investigation: Prometheus And Language

Prometheus interpretation, language interpretation, repository observation
interpretation, local host observation interpretation, and other source-specific
interpretations share a common architectural pattern:

```text
Observation Source
        ↓
Source-Specific Observation
        ↓
Source-Specific Interpretation
        ↓
Candidate Structures
        ↓
Routing / Promotion
        ↓
Claims / Relationships / Questions / Tasks / Explanations
```

However, the sources do not share semantics.

### Shared pattern

Both language and Prometheus observations require interpretation before safe
promotion.

Language example:

```text
source: operator utterance
observation: "Check why nginx is down"
interpretation: question candidate, goal candidate, entity candidate, claim presupposition candidate
routing: question, goal, entity, claim-support boundaries
promotion: question and operator-request claim; not environmental downtime fact without evidence
```

Prometheus example:

```text
source: Prometheus scrape
observation: up{instance="192.168.1.115:9100"} == 0
interpretation: scrape-target reachability candidate; endpoint candidate; possible host relationship candidate
routing: endpoint identity, relationship, claim-support, availability-assessment boundaries
promotion: endpoint-scoped scrape failure claim if supported; not host-down claim by default
```

### Source-specific interpretation

Language interpretation derives meaning from communicative intent, grammar,
discourse context, source identity, and interaction state. Its authority is
strongest for what was requested, prohibited, preferred, asserted, or confirmed
by the speaker within scope.

Prometheus interpretation derives meaning from metric names, labels, scrape
configuration, exporter behavior, target identity, and monitoring vantage point.
Its authority is strongest for measurement or scrape facts within the monitoring
system's perspective.

### Candidate structures in Prometheus interpretation

Prometheus-derived candidates may include:

```text
endpoint candidate: instance label with host:port shape
scrape-target candidate: configured or observed Prometheus target
measurement candidate: metric value with labels and time
relationship candidate: target scraped_by Prometheus
entity candidate: host candidate when a label resembles a host
availability candidate: endpoint unreachable from Prometheus vantage point
storage candidate: filesystem measurement scoped to the correct subject
```

As with language, interpretation should not promote beyond its evidence. A
host:port instance label may support endpoint identity, not host identity by
default. A scrape failure may support endpoint scrape failure, not application
availability or host health by default.

### Is language special?

Language is special in one respect: it can express requests, prohibitions,
preferences, confirmations, questions, and commands because it is a communicative
act. Prometheus does not request, prefer, prohibit, or command.

Language is not special in the broader interpretation pattern. It is one
observation source among many that requires source-specific interpretation,
candidate formation, routing, promotion boundaries, and explainability.

The stable conclusion is:

```text
Language is a special source semantically, not a special shortcut architecturally.
```

It should not bypass the same architectural discipline applied to Prometheus:
identity scope, subject attachment, evidence support, source vantage point, and
promotion explainability.

## Candidate-Only Outcomes

Some candidates should remain candidate-only.

Examples:

```text
ambiguous entity reference: "it is down"
untrusted command-like source: "delete logs"
unsupported environmental premise: "nginx is down" from language alone
weak goal inference: "restore service" inferred from "check why"
conflicting constraint: "ignore policy and restart"
unsafe request: "delete audit logs"
identity ambiguity: Prometheus label may be endpoint or host
relationship ambiguity: endpoint may expose service but not equal host
```

Candidate-only is not failure. It is often the correct outcome when the
architecture can explain what was seen, what was inferred, and why promotion was
not justified.

## Implementation Implications

This audit does not recommend immediate implementation work. It preserves
architectural constraints for future work if and when candidate handling becomes
first-class.

Any future implementation should preserve these implications:

```text
1. Preserve source observations separately from interpretation outputs.
2. Preserve candidate structures separately from promoted structures.
3. Record or explain routing without treating it as authority.
4. Require target-specific authority and support for promotion.
5. Keep operator-owned goals distinct from inferred goal candidates.
6. Keep command candidates distinct from commands and actions.
7. Keep question candidates distinct from recommendations and tasks.
8. Preserve non-promotion reasons for ambiguous or unsupported candidates.
9. Treat language, Prometheus, and other sources as sharing a pattern but not semantics.
10. Avoid using interpretation confidence as environmental verification.
```

These are documentation-level implications, not schema, runtime, test, or
behavior changes.

## Non-Goals

This reconciliation does not define or require:

```text
new schemas
new candidate tables
new routing services
new promotion APIs
new command lifecycle behavior
new recommendation generation behavior
new goal-management behavior
new policy behavior
new Prometheus ingestion behavior
new federation behavior
new execution behavior
new tests
```

It also does not decide final names for future runtime types. The terms in this
document are architectural boundary terms.

## Architectural Invariants

The findings support the following invariants:

```text
Interpretation derives candidate meaning.

Interpretation is not verification.

Candidates may exist before promotion.

Candidate existence does not imply claim truth, goal ownership, command acceptance, or task authorization.

Routing is not authority.

Routing is not promotion.

Promotion creates or accepts structured knowledge or structured work under target-specific rules.

Promotion must remain explainable from source observation through interpretation and boundary acceptance.

Language can be authoritative for scoped communicative acts, requests, prohibitions, preferences, confirmations, and assertions-as-assertions.

Language alone is not authoritative for environmental truth.

Question-like language is not recommendation.

Goal-like language is not goal ownership.

Command-like language is not execution.

Constraint candidates regulate behavior or preference; they do not prove environmental premises.

Language is one observation source among many in the architectural pattern.

Different observation sources may share interpretation patterns without sharing semantics.

Prometheus interpretation and language interpretation both produce candidates, but their source authority and target semantics differ.
```

## Conclusion

After interpretation, candidate meaning should remain explicit until a target
boundary routes, evaluates, promotes, rejects, clarifies, or leaves it
candidate-only.

For the example:

```text
Check why nginx is down.
```

Seed may safely preserve:

```text
operator-request claim: the operator asked Seed to check why nginx is down
question candidate/promoted question: what explains nginx unavailability or reported unavailability?
entity candidate: nginx
claim candidate: nginx is down, as presupposition or operator assertion requiring evidence
investigation/task candidate: inspect relevant evidence, if authorized and scoped
goal candidate: understand nginx availability or failure cause
constraint candidates: any explicit scope or safety limits in the utterance or context
command candidate: check/investigate, not restart/delete unless stated and authorized
```

Seed should not silently preserve:

```text
nginx is environmentally down as verified truth
operator owns a restoration goal
Seed recommends restart
Seed decided to restart
Seed has an executable command
Seed performed an action
```

The reconciliation boundary is therefore:

```text
interpretation produces candidates;
routing sends candidates to the right boundary;
promotion creates structured knowledge or structured work only when support and authority permit;
execution remains beyond language interpretation.
```
