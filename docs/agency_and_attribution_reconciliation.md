# Agency And Attribution Reconciliation

## Purpose

This document performs a documentation-only reconciliation of agency,
attribution, intent attribution, belief attribution, knowledge attribution,
autonomy attribution, decision attribution, and anthropomorphic language.

It is an architectural boundary audit.

It does not implement code, modify schemas, modify runtime behavior, modify
projections, observations, evidence handling, claims, recommendations,
decisions, capabilities, execution paths, authority boundaries, or tests.

It does not introduce new runtime semantics.

## Central Question

As Seed's architecture becomes more explainable and inspectable, observers can
begin to describe it using agency-oriented language:

```text
Seed knows nginx is running.
Seed believes a host is unhealthy.
Seed wants to restart a service.
Seed decided to investigate a problem.
Seed learned something.
Seed is autonomous.
```

The question is not whether these sentences are common or convenient. The
question is which architectural structures, if any, justify them.

More precisely:

```text
When does an attribution preserve architectural meaning, and when does it hide
architectural boundaries behind anthropomorphic shorthand?
```

## Central Finding

Attribution is itself a claim. It assigns a property, capacity, stance, or role
to a system, subsystem, capability path, operator, policy, or explanation
surface. Because attribution is a claim, it must remain supportable and
inspectable.

The safest architectural rule is:

```text
Attribution may be used only when it can be decomposed into the structures that
justify it.
```

For Seed, that means agency-oriented language should decompose into explicit
structures such as observations, evidence, facts, support, corroboration,
verification, projection authority, assessments, recommendations, decisions,
commands, capabilities, execution paths, actions, operator authority, policy
authority, and explanation surfaces.

The practical shorthand is:

```text
Claims assert.
Evidence supports.
Facts preserve.
Projections communicate.
Assessments interpret.
Recommendations suggest.
Decisions select.
Capabilities enable.
Commands request.
Execution performs.
Actions mutate.
Operators or delegated policies own authority.
Attributions describe an assigned property and require support.
```

Therefore:

- knowledge attribution is not identical to claim preservation;
- belief attribution is not identical to support;
- goals are not automatically system-owned;
- recommendations are not desires;
- decisions are not intentions;
- capabilities are not agency;
- execution is not autonomy;
- automation is not authority;
- explanation is not consciousness;
- anthropomorphic shorthand is acceptable only when it remains decomposable into
  inspectable architecture.

## Files Considered

This reconciliation builds on existing architectural documentation, especially:

- `docs/knowledge_representation_reconciliation.md`
- `docs/evidence_strength_and_claim_strength_reconciliation.md`
- `docs/knowledge_maintenance_reconciliation.md`
- `docs/assessment_recommendation_and_decision_reconciliation.md`
- `docs/recommendation_selection_boundary.md`
- `docs/goal_policy_and_operator_authority_reconciliation.md`
- `docs/capability_authority_and_execution_boundary_reconciliation.md`
- `docs/capability_verification_reconciliation.md`
- `docs/explainability_contract_characterization.md`
- `docs/explanation_contract_vocabulary.md`
- `docs/selection_rationale_reconciliation.md`
- `docs/operation_support_boundary_reconciliation.md`
- `docs/boundary_preservation_as_architectural_principle.md`

## Boundary Summary

| Concept | Precise architectural meaning | Common shorthand | Main risk if collapsed |
| --- | --- | --- | --- |
| Claim | An assertion with scope and possible support requirements | Seed says X | Unsupported assertion can be mistaken for knowledge |
| Knowledge attribution | A claim that the system is entitled to rely on or communicate X under bounded authority | Seed knows X | Claim preservation can be mistaken for warranted knowledge |
| Belief attribution | A claim that a system has a supported but defeasible stance toward X | Seed believes X | Support/confidence can be mistaken for mental state |
| Intent attribution | A claim that an actor owns a purpose or directed aim | Seed wants X | Operator goals or policy instructions can be mistaken for system desire |
| Goal | A desired state or objective owned by an authority | Seed's goal is X | Delegated task framing can be mistaken for intrinsic purpose |
| Recommendation | An advisory candidate response with rationale and support | Seed recommends X | Suggestion can be mistaken for desire, approval, or decision |
| Decision | A selection among options by an authorized selector | Seed decided X | Selection can be mistaken for intent or action |
| Capability | A possible class of work through a supported path | Seed can X | Possibility can be mistaken for permission or agency |
| Execution | Attempted realization through a concrete path | Seed did X | Tool running can be mistaken for autonomy |
| Action | Externally visible mutation or attempted mutation | Seed changed X | Mutation can be mistaken for authorized independent agency |
| Agency | Capacity to select and pursue actions under owned or delegated authority | Seed is an agent | Capability alone can be mistaken for decision authority |
| Autonomy | Degree of authorized self-direction within explicit boundaries | Seed is autonomous | Automation can be mistaken for authority ownership |
| Attribution | A supportable claim assigning a property to a target | Seed has X | Description can hide responsibility and authority boundaries |

## 1. What Is Attribution?

Attribution is a claim that assigns a property, capacity, stance, role, or
responsibility to a target.

Architecturally, an attribution has at least five parts:

1. **Target:** the entity being described, such as Seed, a projection, a
   capability, a provider, a policy, an operator, or a recommendation path.
2. **Attributed property:** the property being assigned, such as knowledge,
   belief, intent, agency, autonomy, authority, or responsibility.
3. **Scope:** the domain, timeframe, and conditions under which the attribution
   is asserted.
4. **Support:** the evidence, records, rules, authority, or explanation surface
   that justifies the attribution.
5. **Strength:** whether the attribution is literal, architectural, shorthand,
   metaphorical, or misleading.

Examples:

```text
knowledge attribution: Seed knows X.
intent attribution: Seed wants X.
agency attribution: Seed acted as an agent for X.
autonomy attribution: Seed autonomously performed X.
```

Each example is itself a claim. The claim may be supported, unsupported,
overstated, or ambiguous. A valid attribution must be decomposable into more
basic inspectable structures.

Attribution is therefore not a special exception to claim discipline. It is a
claim type that is especially prone to overreach because it often imports human
mental language into architectural descriptions.

## 2. Claims And Knowledge Attribution

The statement:

```text
Seed knows X.
```

is stronger than:

```text
Seed has a preserved claim that X.
```

A preserved claim records an assertion. Knowledge attribution asserts that the
system has enough architectural support to rely on, communicate, or expose X as
known within a bounded context.

The structures beneath knowledge attribution can include:

- observations that produced evidence;
- evidence records with provenance and source limits;
- facts derived from evidence;
- support links between evidence and facts;
- corroboration across independent sources or repeated observations;
- contradiction and conflict handling;
- freshness and expiry semantics;
- verification or capability-verification records when applicable;
- projection rules that authorize current-state communication;
- explanation surfaces that expose why X is supported, current, stale,
  contradicted, or uncertain.

A claim can exist without being knowledge. For example:

```text
Claim: service nginx is running.
```

This becomes knowledge-attribution-compatible only if the architecture can show
why the claim is supported and what limits apply:

```text
Observation source reported process/service status.
Evidence was preserved with provenance.
A fact was projected under applicable rules.
Support is current or explicitly marked stale.
No unresolved stronger contradiction defeats the current projection.
The projection is authorized to communicate that fact.
```

Even then, the precise statement is usually:

```text
Seed has projected, evidence-supported knowledge that X under source, freshness,
and projection limits.
```

The shorthand `Seed knows X` is acceptable only when the decomposition remains
available. It is misleading if it hides weak evidence, expired support,
conflicts, projection limits, or source authority limits.

### Knowledge Attribution Requirements

Knowledge attribution requires support for all of the following:

1. **Representational support:** X is represented as a claim, fact, projection,
   or other inspectable state.
2. **Evidential support:** X is backed by evidence, support relationships, or
   preserved derivation rules appropriate to the claim type.
3. **Authority support:** the surface making the statement is authorized to
   communicate X.
4. **Temporal support:** X is current enough for the asserted use, or staleness
   is explicit.
5. **Integrity support:** known contradictions, conflicts, or uncertainty are
   preserved rather than hidden.

Without these supports, `Seed knows X` should be reduced to a weaker statement,
such as:

```text
Seed has a claim that X.
Seed observed evidence suggesting X.
Seed projected X from current evidence.
Seed has stale support for X.
Seed has conflicting evidence about X.
```

## 3. Belief And Support

The statement:

```text
Seed believes X.
```

is not identical to:

```text
X is supported.
```

Support is a structural relation. It links evidence, facts, rules, or other
records to a claim. Confidence is a measure or annotation of support strength.
Corroboration is support from independent or repeated sources under appropriate
semantics. Trust is a source, provider, policy, or authority judgment.

Belief attribution adds a stance: it says the system treats X as a defeasible
candidate view of the world.

In Seed architecture, the precise forms are usually:

```text
Seed has support for X.
Seed currently projects X.
Seed treats X as a current selected fact under projection rules.
Seed exposes competing beliefs or conflicts about X.
```

`Seed believes X` can be useful shorthand for a current, support-backed,
defeasible projection. It is misleading if it implies subjective conviction,
conscious assent, hidden reasoning, or uninspectable mental state.

### Belief Compared To Adjacent Concepts

| Concept | Meaning | Why it is not belief |
| --- | --- | --- |
| Claim | Assertion of X | A claim may be unsupported or rejected |
| Support | Backing for X | Support is a relation, not a stance |
| Confidence | Strength annotation | Confidence is a measure, not a mental attitude |
| Corroboration | Multiple support paths | Corroboration strengthens support but does not create consciousness |
| Trust | Source or authority judgment | Trust concerns reliability or permission, not belief itself |
| Projection | Current read model | A projection communicates selected state; belief is shorthand over that selection |

Belief attribution is therefore justified only as architectural shorthand for a
supported, current, defeasible representational stance. It should remain
explicitly decomposable into claim, support, confidence, contradiction, and
projection behavior.

## 4. Goals And Intent

The statement:

```text
Seed wants X.
```

is generally misleading unless it is explicitly translated.

Goals describe desired states or objectives. Intent describes directed purpose
toward a goal. Architecturally, intent belongs to an actor or authority-bearing
source, not automatically to any system that represents the goal.

Possible owners of intent include:

- **Operator:** the human or external principal states an objective.
- **Policy:** a policy encodes delegated priorities or constraints.
- **Workflow or task:** a scoped process carries an assigned objective.
- **Capability path:** a bounded execution route has an operational purpose once
  invoked.
- **Recommendation path:** a recommendation may encode a proposed means toward
  an externally supplied objective.
- **System:** only if the architecture explicitly grants goal ownership or
  delegated intent to the system within boundaries.

Seed may represent goals, evaluate goal relevance, generate recommendations,
select options under authority, and execute commands. None of those alone proves
that Seed intrinsically wants anything.

More precise alternatives are:

```text
The operator wants X.
A policy expresses objective X.
The active task is scoped to achieve X.
Seed has a recommendation intended to advance operator goal X.
Seed selected option Y under delegated policy P to satisfy goal X.
```

### Intent Attribution Requirements

Intent attribution requires support for:

1. the intent owner;
2. the intended outcome;
3. the authority by which that outcome is pursued;
4. the scope and limits of delegation;
5. the relationship between a selected action and the intended outcome.

Without explicit delegation, goals remain operator-owned or policy-owned. A
recommendation generated in response to a goal does not make the goal
system-owned.

## 5. Recommendations And Decisions

The statement:

```text
Seed decided X.
```

must distinguish recommendation, selection, decision, command, execution, and
action.

The established architectural chain is:

```text
Projection
  -> Assessment
  -> Recommendation
  -> Decision
  -> Capability selection
  -> Command
  -> Execution
  -> Action, if execution mutates reality
```

Recommendations are advisory. They suggest possible responses. A recommendation
may have rationale, score, support, risk, and expected effect, but it is not a
decision and not a desire.

Decisions are selections. A decision chooses, rejects, defers, escalates, or
accepts an option. Decision attribution is justified only when an inspectable
selection record or equivalent authority-bearing event exists.

Commands request bounded work. Execution attempts work. Actions mutate or
attempt to mutate reality.

Therefore:

```text
Seed recommended X.
```

is not equivalent to:

```text
Seed decided X.
```

And:

```text
Seed executed X.
```

is not equivalent to:

```text
Seed intended X.
```

### Decision Attribution Requirements

Decision attribution requires support for:

1. the candidate set or decision context;
2. the selected, rejected, deferred, or escalated option;
3. who or what had selection authority;
4. the rationale or selection criteria;
5. the time and scope of the decision;
6. downstream command or action linkage, if any.

If the operator chose an option presented by Seed, the precise statement is:

```text
The operator decided X using Seed's recommendation/explanation surface.
```

If a delegated policy selected an option, the precise statement is:

```text
Policy P selected X within delegated authority.
```

If Seed merely ranked or suggested options, `Seed decided X` is misleading.

## 6. What Is Agency?

Agency is the capacity to select and pursue courses of action under owned or
delegated authority, in relation to goals, constraints, and an environment.

Architecturally, agency is not one thing. It is a composite attribution that may
require support from several separable structures:

- represented goals or objectives;
- ownership or delegation of those goals;
- candidate action generation or discovery;
- assessment of state relative to goals;
- selection among options;
- authority to make or accept selections;
- capability paths that can realize selected options;
- command and execution mechanisms;
- feedback or observation after execution;
- auditability and explanation of the selection and action chain.

A system can have some agency-relevant capabilities without being an agent in a
strong sense. For example:

```text
Capability exists: restart service.
Recommendation exists: consider restarting service.
Decision exists: operator approved restart.
Execution exists: restart command ran.
```

These facts do not automatically establish broad agency. They establish bounded
capability, recommendation, decision, and execution structures.

### Agency Compared To Adjacent Concepts

| Concept | Why it is insufficient for agency by itself |
| --- | --- |
| Capability | Possibility does not include goal ownership or authority |
| Recommendation | Suggestion does not include selection authority |
| Decision | Selection may be operator-owned or policy-owned, not system-owned |
| Execution | Performing work does not prove independent goal pursuit |
| Action | Mutation does not prove the mutating path owned the purpose |
| Explanation | Explaining behavior does not create agency |

Agency attribution is justified only within a bounded statement such as:

```text
Seed acted as an agent for operator O within delegated scope S by selecting and
executing action A under policy P.
```

Absent such support, a weaker statement is preferable:

```text
Seed provided capabilities, recommendations, selections, or execution support.
```

## 7. What Is Autonomy?

Autonomy is the degree of authorized self-direction a system has within explicit
boundaries.

Autonomy differs from automation. Automation performs a predefined process.
Autonomy concerns who or what may choose among options, initiate work, adapt to
observations, and continue action without additional external approval.

Autonomy also differs from execution. Execution means a command or operation ran.
A fully human-directed command can execute without any system autonomy.

Autonomy differs from delegation. Delegation is the transfer of authority for a
scope. Autonomy is the degree of self-direction exercised within that delegated
scope.

Autonomy differs from capability. Capability says work is possible. Autonomy
says the system may direct some work without additional instruction within
bounded authority.

Autonomy differs from authority. Authority is permission or legitimacy. Autonomy
is self-directed operation under that authority.

### Autonomy Attribution Requirements

Autonomy attribution requires support for:

1. delegated or owned authority;
2. boundary conditions and constraints;
3. initiation or selection rights;
4. decision criteria or policy basis;
5. capability and execution paths;
6. monitoring, feedback, or stopping conditions where relevant;
7. auditability of decisions, commands, execution, and actions.

The statement:

```text
Seed is autonomous.
```

is too broad unless scoped. Prefer:

```text
Seed automatically performs X when condition C is met.
Seed may select among options A/B/C under policy P without further approval.
Seed executed operator-approved command X.
Seed has no autonomy for mutation; it only recommends actions.
```

Automation alone justifies `automated`, not `autonomous`. Execution alone
justifies `executed`, not `autonomous`.

## 8. Explanation And Anthropomorphic Language

Anthropomorphic language maps system behavior onto human mental vocabulary:

```text
knows
thinks
believes
wants
decided
learned
understands
noticed
```

This language can be useful shorthand. It can make explanations compact and
operator-readable. The architectural risk is that shorthand can imply hidden
mental states, consciousness, desire, responsibility, or authority that the
system does not possess.

The governing rule is:

```text
Anthropomorphic shorthand is acceptable only when it can be expanded into
inspectable structures without changing meaning.
```

### Language Classification

| Statement | Classification | More precise expansion |
| --- | --- | --- |
| Seed has evidence for X | Precise | Evidence/support records exist for X |
| Seed projects X as current | Precise | Projection rules select X for current view |
| Seed knows X | Shorthand when supported; misleading when unsupported | Seed has current evidence-backed projected knowledge of X under limits |
| Seed believes X | Shorthand | Seed currently treats X as a defeasible supported projection |
| Seed thinks X is risky | Shorthand | Seed has an assessment classifying X as risk under rule/context R |
| Seed wants X | Usually misleading | Operator/policy/task goal is X; Seed may recommend means toward X |
| Seed recommended X | Precise if recommendation exists | Advisory object or path suggested X with rationale |
| Seed decided X | Precise only if selection authority/record exists | Authorized selector selected X from candidate set C |
| Seed learned X | Shorthand | Seed acquired and preserved new evidence/facts/projections for X |
| Seed understands X | Usually misleading unless defined as coverage | Seed has representations/explanations sufficient for scoped questions about X |
| Seed is autonomous | Misleading unless scoped | Seed has delegated self-direction for actions within boundary S |

Explainability should reduce dependence on anthropomorphic interpretation. A
good explanation should make the structural expansion available:

```text
What was observed?
What evidence was preserved?
What claim or fact was produced?
What support exists?
What projection communicated it?
What assessment interpreted it?
What recommendation suggested a response?
Who or what decided?
What command was requested?
What execution happened?
What action mutated reality?
```

## 9. Evidence Required For Attribution Claims

Because attribution is a claim, every attribution should match the strength of
its support.

| Attribution | Minimum support required | Unsupported stronger claim to avoid |
| --- | --- | --- |
| Knowledge attribution | Evidence-backed, current or explicitly stale claim/fact/projection with authority and integrity context | A stored claim means Seed knows |
| Belief attribution | Supported, defeasible current stance or projection with confidence/conflict context | Support means subjective belief |
| Intent attribution | Identified intent owner, objective, delegation/authority, and relationship to selected path | A recommendation means Seed wants |
| Goal attribution | Explicit operator, policy, task, or delegated system goal ownership | Any objective in context is Seed's goal |
| Recommendation attribution | Advisory record/path with rationale, support, candidate context, and limitations | Ranking means decision or desire |
| Decision attribution | Selection/rejection/defer/escalation record or event with selector authority and context | Output or execution means decision |
| Agency attribution | Bounded goal ownership/delegation plus selection and pursuit under authority | Capability means agency |
| Autonomy attribution | Delegated self-direction with explicit boundaries, initiation/selection rights, and audit trail | Automation or execution means autonomy |
| Understanding attribution | Defined coverage of representation/explanation for scoped questions | Fluent explanation means consciousness |

The evidence must also preserve negative and limiting information where present:

- lack of support;
- weak support;
- stale support;
- source limitations;
- unresolved contradictions;
- confidence limits;
- missing authority;
- operator ownership;
- policy constraints;
- approval requirements;
- non-executable advisory status.

## 10. What Should Not Be Collapsed Together?

### Claim != Knowledge

A claim is an assertion. Knowledge attribution requires support, authority,
freshness, and integrity context. Collapsing them makes unsupported assertions
look warranted.

### Claim Preservation != Truth

Preserving a claim records that it was asserted or derived. It does not prove the
world is as claimed. Evidence, support, corroboration, conflicts, and projection
rules determine what may be communicated as current knowledge.

### Support != Belief

Support is a relation between backing and claim. Belief attribution adds a
stance. Collapsing them turns structural evidence into anthropomorphic mental
state.

### Confidence != Trust

Confidence describes support strength or projection certainty. Trust concerns
source, provider, authority, or policy reliability. A high-confidence observation
from an untrusted source may still have authority limits.

### Recommendation != Desire

A recommendation suggests a response. It does not mean the system wants that
response. The desired outcome may belong to the operator, a policy, or the active
task.

### Decision != Intent

A decision selects among options. Intent concerns purpose. A decision may be made
by an operator for one purpose, by a policy for another, or by a delegated path
within narrow scope.

### Selection != Authorization

A selected option may still require approval, policy validation, command
creation, or execution gating. Selection alone does not authorize mutation.

### Capability != Agency

Capability describes possibility. Agency requires goal relation, selection, and
authority. A tool catalog is not an agent merely because it contains powerful
operations.

### Execution != Autonomy

Execution means work was attempted. Autonomy requires authorized self-direction.
A command executed under direct operator approval may involve no autonomy.

### Automation != Authority

Automation can run a predefined path. Authority determines whether that path is
legitimate and under whose permission. Automated behavior without explicit
authority should not be described as autonomous authority.

### Action != Responsibility

An action mutates or attempts to mutate reality. Responsibility depends on the
operator, policy, provider, system boundary, command, approval, and delegation
chain.

### Explanation != Consciousness

An explanation can expose evidence, rationale, support, and decision paths. It
does not imply subjective awareness. Explainability should make anthropomorphic
interpretation less necessary, not more necessary.

## Potential Architectural Invariants

The findings support the following invariants:

1. **Attribution is a claim.** Any attribution must be supportable and scoped.
2. **Attribution requires support.** Unsupported attribution should be marked as
   shorthand, speculation, or avoided.
3. **Knowledge attribution requires more than claim preservation.** It requires
   evidence, authority, freshness, and integrity context.
4. **Belief attribution is shorthand for supported defeasible stance.** It must
   not imply subjective conviction.
5. **Goals remain operator-owned unless explicitly delegated.** A represented
   goal is not automatically a system-owned goal.
6. **Intent follows authority and ownership.** Intent should be attributed to the
   operator, policy, task, or delegated system scope that owns the purpose.
7. **Recommendations are advisory.** They do not decide, approve, command,
   execute, or desire.
8. **Decisions are selections.** They require selector identity, authority,
   candidate context, and rationale.
9. **Capabilities describe possibility.** They are not permission, execution,
   agency, or autonomy.
10. **Commands request.** They bridge decision to execution but do not prove the
    requested work occurred.
11. **Execution performs.** It may read, calculate, observe, or mutate; execution
    is not automatically action.
12. **Actions mutate reality.** Mutation requires the strongest authority and
    audit clarity.
13. **Agency should not be inferred from capability alone.** Agency attribution
    requires bounded goal relation, selection, and authority.
14. **Autonomy should not be inferred from execution alone.** Autonomy requires
    delegated self-direction within boundaries.
15. **Automation is not authority.** Predefined execution does not identify who
    may legitimately choose or initiate it.
16. **Explanation should preserve decomposition.** An explanation should make it
    possible to expand shorthand into inspectable structures.
17. **Anthropomorphic language should be reversible.** If `Seed knows`, `Seed
    believes`, or `Seed decided` cannot be translated into precise architecture,
    the statement should be avoided or weakened.

## Non-Goals

This reconciliation does not require Seed to avoid all anthropomorphic language.
Operator-facing systems may use compact wording when it improves readability.

This reconciliation does not require new schemas, services, projection changes,
execution changes, or tests.

This reconciliation does not decide whether future versions of Seed should
support stronger forms of delegated agency or autonomy. It only defines the
support that would be required for such claims.

This reconciliation does not treat philosophical consciousness, subjective
experience, moral patienthood, or personhood as architectural properties of
Seed. Those concepts are outside the current architecture unless explicitly
modeled by future requirements.

## Implementation Implications

No implementation work is required by this document.

The architectural implications are documentation and explanation discipline:

- use precise terms when describing internal boundaries;
- allow shorthand only when the precise expansion is available;
- preserve operator, policy, provider, and system responsibility boundaries;
- avoid implying desire, consciousness, or independent authority from ordinary
  support, recommendation, capability, execution, or explanation structures;
- when making agency-oriented statements, identify the supporting structures and
  the scope of the attribution.

If future implementation work introduces stronger delegated decision authority,
self-directed action selection, or automated mutation, that work should preserve
explicit attribution support rather than relying on broad statements such as
`Seed is autonomous`.

## Recommended Vocabulary

Prefer precise statements such as:

```text
Seed has evidence for X.
Seed currently projects X.
Seed has support for claim X.
Seed exposes conflicting support for X.
Seed generated recommendation R for operator goal G.
The operator selected option O.
Policy P selected option O within delegated scope S.
Seed executed command C through capability path K.
Action A mutated resource R.
```

Use shorthand only with care:

```text
Seed knows X.
```

means:

```text
Seed has current, evidence-backed, projection-authorized knowledge of X under
explicit source, freshness, and integrity limits.
```

```text
Seed believes X.
```

means:

```text
Seed currently treats X as a supported, defeasible projected stance.
```

```text
Seed decided X.
```

means:

```text
An authorized selector within Seed's modeled decision boundary selected X from a
candidate context, with rationale and authority preserved.
```

```text
Seed is autonomous for X.
```

means:

```text
Seed has delegated self-direction to initiate or select X within explicit scope,
constraints, policy, and audit boundaries.
```

If those expansions are not true, the shorthand should not be used.

## Final Finding

Agency-oriented language is not forbidden, but it is never free. It carries
architectural obligations.

The boundary is:

```text
Anthropomorphic language is acceptable shorthand only when it is losslessly
recoverable into claims, evidence, support, projections, assessments,
recommendations, decisions, capabilities, commands, execution, actions, and
explicit authority boundaries.
```

Seed's explainability should make those decompositions easier to inspect. As
explainability improves, the architecture should depend less on phrases like
`Seed knows`, `Seed wants`, or `Seed decided`, because the underlying support,
authority, and selection chain should be visible directly.
