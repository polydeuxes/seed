# Candidate Meaning And Ambiguity Reconciliation

## Purpose

This document preserves a cross-cutting architectural finding discovered during language, Prometheus, topology, federation, documentation, and input-inspection work.

It is a documentation-only reconciliation and architectural finding preservation document. It does not implement code, modify schemas, alter runtime behavior, modify tests, change projections, modify ontology definitions, or alter authority systems.

The purpose is to preserve the finding that Seed repeatedly improves when it keeps candidate meanings visible long enough to evaluate them instead of collapsing them immediately into certainty.

This document begins where `docs/observation_interpretation_and_reality_reconciliation.md` stops.

That prior reconciliation preserves the pipeline:

```text
source emission
        ↓
observation
        ↓
interpretation
        ↓
candidate meaning
        ↓
routing
        ↓
promotion
        ↓
verification
```

This document focuses on the middle of that pipeline:

```text
observation
        ↓
interpretation
        ↓
candidate meanings
        ↓
routing
```

and asks:

```text
What should Seed do with ambiguity?
```

---

## Motivation

Recent repository work repeatedly exposed the same tension:

```text
ambiguity
        ↓
problem
```

That assumption was too simple.

Seed did not improve by pretending ambiguity was good in itself. Seed improved when ambiguity was treated as information that needed preservation, routing, bounding, and evaluation.

The recurring finding is:

```text
The danger is not multiple candidates.

The danger is premature certainty.
```

A more complete finding is:

```text
Many candidates are acceptable.

Invisible candidates are dangerous.

Premature certainty is dangerous.

Unbounded candidate growth is dangerous.
```

Therefore, this document does not frame ambiguity as good. It frames ambiguity as information and certainty as something that requires justification.

---

## Central Thesis

Seed should not fear ambiguity merely because multiple candidate meanings exist.

Seed should fear ambiguity when it is invisible, unbounded, routed to the wrong boundary, promoted without support, or allowed to drive action without sufficient certainty.

Central thesis:

```text
Ambiguity is information.

Certainty requires justification.

Candidates are cheap.

Claims are expensive.

Actions are very expensive.
```

This creates a practical ordering:

```text
observe broadly
interpret carefully
preserve candidate alternatives
route before promotion
promote narrowly
verify explicitly
act only with stronger certainty
```

---

## 1. What Is A Candidate Meaning?

A candidate meaning is a plausible interpretation derived from one or more observations before Seed has promoted that interpretation into a structured claim, fact, relationship, projection, issue, recommendation, or action.

It answers:

```text
What might this observation mean?
```

It does not answer:

```text
Is this true?
Should this be believed?
Should this change the graph?
Should this be shown as a fact?
Should the operator act?
```

A candidate meaning is intentionally provisional. It may be supported, contradicted, routed, discarded, merged with another candidate, promoted into a claim, or retained as unresolved context.

### Candidate Meaning Compared To Nearby Concepts

| Concept | What it means | Why it is not a candidate meaning |
| --- | --- | --- |
| Observation | Seed encountered a source emission, signal, artifact, statement, metric, path, or document fragment. | An observation records that something was seen; it does not assign final meaning. |
| Candidate meaning | A plausible interpretation of an observation. | This is the provisional interpretive layer. |
| Claim | A structured assertion that something is or may be true. | A claim is more expensive because it enters support, contradiction, confidence, and provenance machinery. |
| Fact | A claim treated as sufficiently established for its context. | A fact requires stronger support than a candidate. |
| Relationship | A structured edge between entities or concepts. | A relationship asserts graph structure; a candidate may only suggest that structure. |
| Projection | A rendered or surfaced view of selected knowledge. | A projection should not silently turn unresolved alternatives into fact-like output. |
| Issue | A surfaced problem, gap, contradiction, risk, or unresolved matter. | An issue may be created from ambiguity, but the candidate itself is not the issue. |
| Recommendation | A proposed course of action or assessment output. | A recommendation consumes evaluated candidates and claims; it should not be raw ambiguity. |
| Action | A mutation, execution, external change, or operator-directed step. | Actions require stronger certainty and authority than candidates or claims. |

A candidate meaning is useful precisely because it gives Seed a place to preserve interpretation without pretending that interpretation has already become reality.

---

## 2. Why Do Candidates Exist?

Candidates exist because observations rarely carry a single intrinsic meaning. Meaning is derived from source shape, context, provenance, convention, domain vocabulary, historical state, corroborating evidence, and operator intent.

### Input Inspection

Input inspection showed that source shape can support multiple interpretations:

```text
file extension
contents
operator use
surrounding context
```

An inventory-like artifact may have an `.ini` extension while containing YAML-like structure. The extension supports one candidate. The contents support another. The operator's workflow may support a third.

The observation is not false. The risk is deciding too early which meaning controls.

### Language

Natural language does not directly deliver facts. It delivers communicative acts.

The same operator utterance may be:

```text
assertion
a correction
a command
a preference
a policy
a question
a goal
a recommendation request
a constraint
```

The words are evidence, but the architectural consequence depends on interpretation and routing.

### Prometheus

Prometheus metrics are source emissions. Their labels, metric names, targets, and payload values can support multiple meanings:

```text
measurement
scrape topology
exporter configuration
host property
service role
identity hint
availability signal
```

A metric can be valuable without being direct authority for topology, identity, ownership, or service responsibility.

### Documentation

Documentation may describe:

```text
current behavior
intended behavior
historical behavior
planned behavior
operator policy
architectural aspiration
known limitation
```

A README saying `X` is an observation of a documentation claim. It is not automatically implementation reality.

### Federation

Federation imports transfer testimony, provenance, and foreign assertions. They do not automatically transfer local truth.

A remote Seed's assertion may be:

```text
trusted local fact in the remote system
foreign testimony in the receiving system
stale historical evidence
policy-bound information
context-specific interpretation
```

The receiving Seed needs candidate meanings so it can preserve what was imported without silently promoting foreign certainty into local certainty.

### Storage Topology

Storage topology exposed the same pattern through paths such as:

```text
/mnt/example_host_e/sda1
```

That path may support candidates including:

```text
local storage
remote mount
bind mount
mirror path
retired-node compatibility path
cluster naming convention
backup safety concern
ownership hint
```

The path is evidence. It is not ownership authority by itself.

---

## 3. Is Ambiguity Inherently Bad?

No. Ambiguity is not inherently bad.

The common assumption:

```text
ambiguity
        ↓
problem
```

should be replaced with:

```text
ambiguity
        ↓
information requiring handling
```

Ambiguity becomes harmful when Seed:

- hides alternative interpretations;
- promotes one candidate without sufficient support;
- lets a projection imply certainty that does not exist;
- treats ambiguity as contradiction before a contradiction exists;
- asks the operator about every theoretical alternative;
- allows unbounded candidate growth;
- acts on a candidate as if it were verified reality.

Ambiguity is often the correct representation of the system's current knowledge state. The problem is not that multiple meanings exist. The problem is failing to represent, route, bound, or evaluate them.

---

## 4. What Is Premature Certainty?

Premature certainty is the architectural failure of treating an observation or candidate meaning as a fact, relationship, projection, issue, recommendation, or action before the required interpretation, routing, support, authority, and verification steps have occurred.

It has this shape:

```text
observation
        ↓
certainty
```

or:

```text
candidate meaning
        ↓
fact
```

without enough intervening justification.

### Operator Statement Collapse

Bad collapse:

```text
operator says X
        ↓
fact X
```

Correct handling:

```text
operator says X
        ↓
communicative act observed
        ↓
candidate meaning X
        ↓
routing
        ↓
promotion if justified
```

The operator may be highly authoritative about goals, preferences, approvals, corrections, and local context. That does not mean every statement is direct observation of external reality.

### Documentation Collapse

Bad collapse:

```text
README says X
        ↓
fact X
```

Correct handling:

```text
documentation contains claim X
        ↓
documentation claim observed
        ↓
candidate meaning
        ↓
alignment or implementation verification when needed
```

Documentation is evidence. It may be authoritative for intent or policy. It is not automatically authoritative for implementation reality.

### Metric Collapse

Bad collapse:

```text
metric says X
        ↓
fact X
```

Correct handling:

```text
metric emitted
        ↓
metric observation
        ↓
candidate meaning
        ↓
routing
        ↓
narrow promotion if supported
```

Prometheus was not lying in these cases. Seed attached meanings too early.

### Path Collapse

Bad collapse:

```text
/mnt/example_host_e/sda1
        ↓
example_host_e owns storage
```

Correct handling:

```text
path observed
        ↓
candidate topology meanings
        ↓
routing
        ↓
operator clarification or corroboration if consequential
```

The path text may encode historical topology, cluster convention, compatibility naming, a remote mount, or ownership. It should not alone become a physical ownership fact.

### Why These Failures Occurred

These failures occurred because Seed collapsed distinct layers:

```text
source emission
observation
interpretation
candidate meaning
routing
promotion
verification
```

The collapse was attractive because it simplified output. It was dangerous because it erased provenance, alternatives, uncertainty, and the boundary that should decide whether a candidate is safe to promote.

---

## 5. What Are Invisible Candidates?

Invisible candidates are plausible interpretations that exist architecturally but are not preserved, shown, routed, or made available to downstream evaluation.

The failure shape is:

```text
candidate A
candidate B
candidate C
```

but only:

```text
candidate A
```

becomes visible.

Invisible candidates create hidden architectural risk because downstream consumers may assume that the visible candidate was the only candidate considered or the only candidate supported.

Risks include:

- projections that appear more certain than the evidence allows;
- recommendations that ignore materially different interpretations;
- contradiction detection that never sees the alternative claim shape;
- operator questions that are never asked because the ambiguity was hidden;
- federation imports that lose provenance and local-evaluation context;
- topology or identity assumptions that become hard to unwind later.

Candidate visibility does not require every candidate to become a claim. It requires Seed to retain enough visibility that important alternatives are not silently erased.

---

## 6. What Is Candidate Explosion?

Candidate explosion is uncontrolled growth in possible interpretations such that preserving ambiguity becomes computationally, cognitively, or operationally harmful.

Two shapes are different:

```text
100 observations
10 candidates each
```

versus:

```text
10 observations
1000 candidates each
```

The first may be manageable if candidates are bounded, typed, routed, and cheap. The second may indicate that interpretation is too unconstrained, the route boundary is missing, or Seed is generating theoretical possibilities that have no material downstream consequence.

Candidate growth becomes harmful when candidates:

- are generated without evidence thresholds;
- are not typed or scoped;
- are not routed to responsible boundaries;
- are promoted merely because they exist;
- consume projection space without relevance;
- create operator-question spam;
- cause every observation to participate in every possible plane;
- prevent the system from distinguishing likely, supported, material, and speculative interpretations.

The answer is not to collapse ambiguity into false certainty. The answer is to bound candidate generation and route candidates early.

---

## 7. What Is Routing's Role?

Routing is the movement or classification of candidate meanings toward the boundary that can evaluate them.

The relevant shape is:

```text
Observation
        ↓
Interpretation
        ↓
Candidates
        ↓
Routing
```

Routing helps answer:

```text
Which boundary should consider this candidate?
```

It does not by itself answer:

```text
Is this candidate true?
Should this candidate be promoted?
Should this candidate drive action?
```

Routing exists partly to prevent candidate explosion. It reduces ambiguity pressure by ensuring that candidates do not all flow into every downstream plane.

Examples:

| Candidate type | Likely route |
| --- | --- |
| Language command candidate | capability, authorization, execution, and operator-intent boundaries |
| Language claim candidate | claim support and evidence boundaries |
| Documentation behavior candidate | documentation authority and implementation-alignment boundaries |
| Prometheus filesystem candidate | measurement, topology, and storage interpretation boundaries |
| Federation testimony candidate | provenance, import, local-evaluation, and trust boundaries |
| Storage ownership candidate | topology, inventory, operator clarification, and verification boundaries |

Routing preserves ambiguity without requiring every candidate to become every kind of downstream object.

---

## 8. Can A Single Observation Participate In Multiple Planes?

Yes. A single observation can support multiple simultaneous interpretation planes.

Example observation:

```text
/mnt/example_host_e/sda1
```

Possible planes:

```text
filesystem measurement
mount topology
cluster convention
storage ownership
retired-node history
backup safety
```

These planes are not mutually exclusive. The same path may be a filesystem measurement, a mount topology clue, a cluster naming convention, a storage ownership hypothesis, a retired-node history marker, and a backup safety concern.

The important distinction is that participation in a plane is not promotion to a fact in that plane.

Correct shape:

```text
one observation
        ↓
multiple candidate meanings
        ↓
multiple routed planes
        ↓
plane-specific promotion only when supported
```

This is why ambiguity is information. The observation may be meaningful in more than one architectural context, and each context may require different evidence before promotion.

---

## 9. What Should Be Promoted?

Promotion should not operate on all candidates merely because they exist.

Promotion should generally operate on routed candidates that have enough support, scope, provenance, and materiality for the target boundary.

Tradeoffs:

| Promotion target | Benefit | Risk |
| --- | --- | --- |
| All candidates | Maximum preservation. | Turns speculation into structured noise and causes candidate explosion. |
| Best candidate | Simple output. | Hides alternatives and can create premature certainty. |
| Routed candidates | Keeps candidates near responsible evaluators. | Requires routing discipline and candidate typing. |
| Supported candidates | Reduces false promotion. | May underrepresent unresolved but material alternatives if visibility is lost. |

The reconciled approach is:

```text
generate bounded candidates
        ↓
preserve materially relevant alternatives
        ↓
route before promotion
        ↓
promote supported candidates narrowly
        ↓
do not erase important alternatives merely because one candidate was promoted
```

Promotion should create the narrowest claim that is justified. If a metric supports a filesystem measurement, promote the measurement. Do not silently promote ownership, topology, role, or identity unless those meanings have their own support.

---

## 10. When Should Seed Ask?

Seed should ask the operator when ambiguity is material and consequential, not whenever a theoretical alternative exists.

The useful threshold is:

```text
multiple materially different interpretations
        +
meaningful downstream consequences
        ↓
ask operator
```

Operator clarification is appropriate when candidate ambiguity affects:

- ownership;
- authority;
- execution;
- safety;
- recommendation;
- federation trust;
- important projections;
- contradiction handling;
- topology or identity promotion.

Clarification is evidence acquisition. It should be treated as an architectural boundary, not as a conversational fallback for every uncertain detail.

Seed should avoid both extremes:

```text
never ask
```

because hidden ambiguity can become unsafe certainty; and

```text
always ask
```

because unbounded questions create operator burden and prevent autonomous interpretation.

---

## Required Findings Preserved

### Many Candidates Are Acceptable

Many candidates are acceptable when they are bounded, typed, visible, routed, and not automatically promoted.

Candidate multiplicity can accurately represent the current knowledge state.

### Invisible Candidates Are Dangerous

Invisible candidates are dangerous because downstream systems may mistake a surviving candidate for the only plausible interpretation.

Visibility preserves architectural honesty.

### Premature Certainty Is Dangerous

Premature certainty is dangerous because it converts evidence into authority before the required boundaries have evaluated it.

It can create false facts, false relationships, misleading projections, unsafe recommendations, and actions based on inadequate support.

### Unbounded Candidate Growth Is Dangerous

Unbounded candidate growth is dangerous because it can overwhelm routing, projection, operator attention, and verification.

Candidate preservation must be bounded by evidence, type, scope, materiality, and downstream relevance.

---

## Additional Findings

### Observations May Support Multiple Planes

A single observation may legitimately support several interpretation planes. Seed should allow this without treating the observation as fact in every plane.

### Routing Reduces Ambiguity Pressure

Routing prevents every candidate from entering every downstream process. It is a pressure valve between interpretation and promotion.

### Candidates Are Cheap

Candidates should be cheap enough to preserve meaningful alternatives.

### Claims Are Expensive

Claims are more expensive because they enter support, contradiction, confidence, provenance, projection, and federation machinery.

### Actions Are Very Expensive

Actions are most expensive because they can mutate systems, consume resources, alter operator state, or create external consequences. They require stronger certainty, authority, and support than claims.

---

## Potential Architectural Invariants

This finding supports the following invariants:

- Candidate meanings are not claims.
- Ambiguity is not contradiction.
- Multiple interpretations may coexist.
- Observations can support multiple planes.
- Routing should occur before promotion.
- Promotion should not erase alternative interpretations.
- Premature certainty is more dangerous than preserved ambiguity.
- Candidate generation should be bounded.
- Candidate visibility is important.
- Actions require stronger certainty than claims.
- Certainty requires justification.
- A projection should not imply certainty that the underlying support does not justify.
- Operator clarification is evidence acquisition when ambiguity is material and consequential.
- Federation can transfer testimony without transferring local truth.
- Documentation can provide evidence without being implementation reality.
- Metrics can provide measurements without establishing topology or ownership.
- Path strings can provide topology evidence without establishing physical ownership.

---

## Non-Goals

This reconciliation does not:

- implement candidate objects;
- add schemas;
- change runtime behavior;
- modify tests;
- modify projections;
- modify ontology definitions;
- modify authority systems;
- define a complete candidate-ranking algorithm;
- define a complete operator-question policy;
- require every theoretical candidate to be preserved forever;
- require ambiguity to be surfaced in every projection;
- assert that ambiguity is always good;
- assert that Seed should avoid certainty.

The goal is to preserve the architectural finding so future implementation work does not collapse interpretation into certainty too early.

---

## Rejected Approaches

### Treat Ambiguity As A Bug

Rejected because many repository findings showed that ambiguity was often the accurate representation of available evidence.

### Promote The Best Candidate Immediately

Rejected because the best visible candidate may not be sufficiently supported, and choosing it can hide materially important alternatives.

### Preserve Every Possible Candidate Everywhere

Rejected because unbounded candidate growth is computationally and cognitively harmful.

### Ask The Operator About Every Ambiguity

Rejected because operator clarification should be reserved for ambiguity with meaningful downstream consequences.

### Treat Source Trust As Meaning Certainty

Rejected because a trusted source can still emit a signal whose meaning requires interpretation.

### Treat Projection Simplicity As Knowledge Certainty

Rejected because simpler output can conceal unresolved ambiguity and create false confidence.

---

## Direct Answers

### Should Seed Fear Ambiguity?

Seed should not fear ambiguity merely because multiple candidate meanings exist.

Seed should treat ambiguity as information requiring preservation, routing, bounding, and evaluation.

### Should Seed Fear Premature Certainty?

Yes. Seed should fear premature certainty because it collapses observation, interpretation, promotion, and verification into a false fact or unsafe action path.

### Should Seed Preserve Multiple Candidates?

Yes, when the candidates are plausible, materially relevant, bounded, and useful for routing or later evaluation.

Seed should not preserve infinite theoretical alternatives with no evidence or downstream relevance.

### Should Candidate Growth Be Bounded?

Yes. Candidate generation should be bounded by evidence, type, scope, materiality, and route.

Bounded preservation is safer than both false certainty and unbounded explosion.

### Can One Observation Support Multiple Planes?

Yes. One observation can support multiple planes, such as filesystem measurement, mount topology, cluster convention, storage ownership, retired-node history, and backup safety.

Participation in a plane is not the same as promotion to a fact in that plane.

---

## Summary Finding

The reconciled position is:

```text
Ambiguity is information.

Certainty requires justification.

Many candidates are acceptable.

Invisible candidates are dangerous.

Premature certainty is dangerous.

Unbounded candidate growth is dangerous.
```

Seed should preserve candidate meanings long enough to route and evaluate them, but not so broadly that every observation becomes every possible claim.

The architectural target is not maximum ambiguity or maximum certainty.

The target is justified certainty after visible, bounded, routed interpretation.
