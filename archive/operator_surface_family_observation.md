---
doc_type: observation
status: exploratory
domain: operator surface families
introduced_by: operator surface family observation
depends_on:
  - operator_understanding_surface_observation.md
  - current_work_position_frontier.md
  - active_edge_frontier.md
  - continuity_frontier.md
  - state_summary_authority_reconciliation.md
  - impact_overview_authority_reconciliation.md
  - source_navigation_surface_reconciliation.md
  - source_navigation_query_surface_design_audit.md
  - capability_verification_audit.md
  - capability_verification_reconciliation.md
  - execution_status_and_operator_feedback_reconciliation.md
  - explainability_reconciliation.md
  - explainability_inventory_audit.md
  - claim_support_design.md
related:
  - knowledge_and_understanding_distinction_observation.md
  - explanatory_load_observation.md
  - discovery_path_preservation_observation.md
  - preservation_surface_observation.md
  - preservation_failure_observation.md
---

# Operator Surface Family Observation

## Purpose

This observation investigates the current landscape of operator-facing and
operator-adjacent surfaces in Seed.

It asks:

```text
What operator-facing surfaces currently exist?
```

and:

```text
Do current surfaces naturally cluster into different surface families?
```

and:

```text
Are inventory, understanding, and explanation distinct concerns?
```

This is an observation only. It is not a reconciliation, frontier,
implementation proposal, UI proposal, operator workflow, governance model,
routing requirement, remediation plan, or runtime change. It does not redesign
surfaces, propose new surfaces, define requirements, or recommend immediate
fixes. Repository authority remains with the documents, implementation, tests,
and navigation maps that own their respective scopes.

## Method

The investigation reviewed repository documents that already discuss operator
visibility, read-model boundaries, source navigation, capability inspection,
verification inspection, promotion readiness, execution status, state summary,
impact, fact support, explanation, current work position, active edge, and
continuity.

For each surface, the investigation asked what question the surface appears to
answer, without assuming that the surface has only one purpose.

Working question families:

```text
Inventory:
What exists?
What is present?
What is stored?
What is counted?

Understanding:
What currently matters?
What is uncertain?
What is active?
What requires attention?

Explanation:
Why is this visible?
Why is this selected?
What supports this?
Why should I care?
```

The labels below are observational family names. They are not proposed schema
names, CLI modes, UI categories, implementation modules, or governance terms.

## Surface Inventory

The reviewed evidence identifies at least the following operator-facing or
operator-adjacent surfaces:

| Surface | Apparent primary question | Apparent family shape |
| --- | --- | --- |
| State Summary | What is the current shape of projected state? | mixed; inventory core with integrity and status signals |
| Impact Overview | What matters about this entity? | understanding-oriented overview with inventory boundaries |
| Impact Sections / Drilldowns | What domain-specific details matter for this entity? | mixed inventory and understanding |
| Current Facts | What fact-like claims are currently projected? | inventory and evidence inspection |
| Fact Support / Claim Support | What supports this claim or fact grouping? | explanation and support visibility |
| Why / Why Fact | Why is this claim visible or believed? | explanation |
| Source Navigation | Where is the source-backed answer or artifact? | mixed implementation, operator evidence, and explanation |
| Capability Resolution / Capability Status | Which capability states, candidates, providers, or verification facts are known? | inventory with verification explanation pressure |
| Verification Inspection | What verification state is supported, stale, failed, disputed, or absent? | mixed inventory and explanation |
| Promotion Readiness / Promotion Backlog | What candidates may be ready for promotion or review? | mixed inventory, attention, and boundary inspection |
| Execution Status | What work is currently occurring? | understanding/status surface |
| Operator Feedback | What should be communicated about that work? | understanding and explanation-adjacent |
| Current Work Position | Where is the work situated for safe continuation? | understanding |
| Active Edge | What unresolved pressure is pulling work forward? | understanding with selection explanation pressure |
| Continuity / Handoff Alignment | What survived change and remains continuable? | understanding |
| Contradiction Visibility | What conflict exists, why, and what boundary constrains it? | mixed understanding and explanation |
| Graph Issues / Integrity Views | What structural issue or inconsistency is visible? | mixed inventory, integrity, and explanation |
| Stale Facts / Temporal Views | What is expired, current, fresh, or temporally bounded? | mixed inventory and explanation |
| Evidence Graph | What evidence nodes and links support projected facts? | inventory and explanation |
| Rule Inventory | What rules exist and how do they relate to visible claims? | inventory with explanation use |
| Repository / Source Inventories | What files, definitions, imports, and implementation artifacts exist? | implementation-oriented inventory |
| Observation Source Accounting | Which sources produced observations and counts? | inventory |
| Storage / Filesystem Observation | What storage measurements or mount facts are present? | inventory with understanding ambiguity |

This list is not assumed complete. It reflects the current reviewed repository
evidence and preserves the possibility that future work will identify additional
surfaces or split these into more precise families.

## Family Findings

### Inventory Family

Inventory-oriented surfaces answer questions of presence, volume, registration,
projection, or enumeration.

Strong inventory surfaces include:

- State Summary counts for facts, observations, requirements, capabilities,
  entities, sources, durable facts, and current samples.
- Current Facts when used to inspect projected fact-like rows.
- Capability inventory and capability-resolution surfaces when they distinguish
  requested capabilities, catalog-known capabilities, registered operation
  candidates, provider recommendations, and handoff candidates.
- Source and repository inventories that expose files, imports, definitions,
  entrypoints, tests, and implementation artifacts.
- Evidence Graph summary and evidence-node/link inventories.
- Observation source accounting, storage measurement rows, filesystem samples,
  package inventories, local host inventories, and rule inventories.

These surfaces appear strongest when the operator question is literally:

```text
What exists here?
What did the system observe?
What did the projection store?
What is registered or counted?
```

The reviewed evidence repeatedly warns that inventory does not by itself answer
meaning, relevance, priority, safety, or understanding. A high count, a present
row, a registered candidate, or a known source may be accurate while still not
communicating why it matters.

### Understanding Family

Understanding-oriented surfaces answer questions of significance, active
pressure, uncertainty, continuity, attention, or safe continuation.

Strong understanding surfaces include:

- Current Work Position, which asks what position the current work occupies and
  what must survive for work to feel continuous.
- Active Edge, which asks what unresolved concern is currently pulling work
  forward rather than merely being preserved.
- Continuity and handoff-alignment documents, which distinguish stored
  information from continuable work.
- Execution Status, when it communicates what work is currently occurring rather
  than merely listing events after completion.
- Impact Overview, when it summarizes entity significance, important domains,
  risks, gaps, unusual conditions, and likely drilldown direction.
- Contradiction visibility, when it exposes unresolved conflict as an attention
  condition rather than merely counting conflicts.
- Preservation-failure and discovery-path observations, when they show that
  artifacts can survive while meaning, activation, or reactivation fails.

These surfaces appear strongest when the operator question is:

```text
What matters now?
What remains uncertain?
What is active?
Where is work situated?
What requires attention?
What can safely be continued?
```

The reviewed evidence suggests that understanding is not the same as storing
more facts. Understanding often depends on selection, boundaries, unresolved
pressure, support changes, and continuation orientation.

### Explanation Family

Explanation-oriented surfaces answer why a row, claim, conflict, status,
selection, or recommendation is visible and what supports it.

Strong explanation surfaces include:

- Fact Support / Claim Support, which relates facts to claims without becoming a
  truth, inference, reasoning, planning, or governance engine.
- Why and Why Fact surfaces, which expose current beliefs, competing beliefs,
  supporting fact IDs, evidence IDs, source types, confidence, observation time,
  recursive source facts, conflicts, and supporting event IDs.
- Explainability inventory and reconciliation documents, which identify common
  fields across facts, support, evidence, contradictions, capabilities, rules,
  temporal metadata, graph issues, impact, and state views.
- Contradiction surfaces, where reasons, competing facts, severity, evidence,
  and resolution boundaries are visible.
- Capability verification inspection, where verification facts, support,
  evidence, status, stale state, failed state, disputed state, and target scope
  need to remain separate from capability execution.
- Source navigation, when it connects a question to source artifacts,
  relationships, and support rather than simply listing files.
- State-summary audits, which explain why endpoint, filesystem, or top-entity
  rows became visible and what authority boundary that visibility does not
  cross.

Explanation appears distinct from both inventory and understanding. It may use
inventory as input and may support understanding, but its central question is:

```text
Why this?
What supports it?
What caveat, reason, source, or selection path makes it visible?
```

## Mixed-Surface Findings

Mixed surfaces are common. The strongest mixed surfaces are those where one
operator-visible output combines counts, current status, support, relevance,
selection, or implementation detail.

### State Summary

State Summary is the strongest mixed and overloaded surface in the reviewed
evidence.

It answers inventory questions:

```text
How many facts, observations, requirements, capabilities, and entities are
projected?
What sources and current samples exist?
What top entities appear?
```

Operators appear to ask additional questions of it:

```text
What does Seed understand?
What matters?
What is important enough to appear at the top?
Is this endpoint, filesystem row, or entity relevant?
What is the system telling me to care about?
```

The divergence appears where projection shape is read as significance. State
Summary can correctly describe the shape of projected state while not explaining
why a visible row matters, why an entity was selected, whether a count reflects
learning, or whether a measurement row represents operator-relevant topology.

### Current Work Position

Current Work Position behaves primarily as understanding. It preserves active
context, current frontier, selected constraints, unresolved tensions, selection
rationale, validation state, next safe moves, non-goals, and authority
boundaries.

It has inventory-adjacent components because it may reference artifacts,
frontiers, questions, and constraints that exist. It has explanation-adjacent
components because selection rationale and authority boundaries explain why the
position is current. But its dominant behavior is not listing content or proving
a claim. It orients future continuation.

### Active Edge

Active Edge communicates more than presence. It distinguishes preserved concerns
from the concern exerting current pull.

It appears to communicate:

```text
presence: a concern, gap, contradiction, frontier, or question exists;
pressure: that concern is pulling work forward;
understanding: it carries unresolved meaning relevant to continuation;
selection: it is the currently live edge rather than one of many preserved items.
```

This makes Active Edge understanding-oriented with explanation pressure. A list
of all gaps would be inventory. Active Edge asks why one unresolved pressure is
live and how continuation should recognize that pressure without turning it into
an implementation mandate.

### Source Navigation

Source Navigation is mixed across implementation, operator, understanding, and
explanation concerns.

It behaves as an implementation surface when it locates files, definitions,
imports, entrypoints, tests, and ownership boundaries. It behaves as an operator
surface when it lets an operator move from a question to a source-backed answer
without first knowing the exact fact shape. It behaves as an understanding
surface when it orients a user from a broad question to the relevant artifact,
relationship, or support chain. It behaves as an explanation surface when it
shows why a source artifact supports an answer.

The strongest source-navigation boundary is that preservation is prerequisite,
but navigation is orientation over preserved knowledge. Preserved source facts
are not automatically a source-navigation answer.

### Fact Support

Fact Support behaves primarily as support visibility and explanation.

It has an inventory component because it lists supporting fact IDs, source
families, confidence aggregates, timestamps, dimensions, and expired support. It
becomes explanation-shaped because those support groups answer why a claim-like
row is visible and what backs it. It does not by itself settle truth, generate
claims, or produce understanding. Operator understanding may emerge only when
support visibility is paired with scope, relevance, conflict, freshness, and
selection context.

## Strongest Surface Groups

### Strongest inventory surfaces

- State Summary count and projection-shape sections.
- Current Facts and broad projected fact listings.
- Evidence Graph node/link summaries.
- Capability resolution candidate and catalog inventories.
- Source/repository inventories of files, imports, definitions, entrypoints, and
  tests.
- Observation-source, package, local-host, storage, and filesystem inventories.
- Rule Inventory.

### Strongest understanding surfaces

- Current Work Position.
- Active Edge.
- Continuity and handoff-alignment surfaces.
- Execution Status as work-in-progress visibility.
- Impact Overview as entity significance overview.
- Contradiction visibility when it communicates unresolved attention pressure.
- Preservation-failure and discovery-path observations.

### Strongest explanation surfaces

- Fact Support / Claim Support.
- Why / Why Fact.
- Explainability inventory, contract, and reconciliation work.
- Contradiction explanation surfaces.
- Capability verification inspection when scoped to support and status reasons.
- Source Navigation when it routes questions to source-backed support.
- State-summary audits that explain visibility, selection, and authority limits.

### Strongest mixed surfaces

- State Summary.
- Source Navigation.
- Capability Verification / Capability Status.
- Execution Status and Operator Feedback.
- Impact Overview and Impact Sections.
- Contradiction visibility.
- Storage topology and filesystem observation surfaces.
- Graph issues and stale-fact views.

### Strongest overloaded surfaces

- State Summary, because inventory, integrity, operational status, knowledge
  inventory, availability, top-entity selection, and operator relevance pressure
  all appear near the same default surface.
- Source Navigation, because implementation navigation, operator answerability,
  source evidence, and explanation pressure share one boundary.
- Capability Verification / Capability Status, because requested capability,
  catalog-known capability, registered operation candidate, provider
  recommendation, local/provider availability, verification support, stale
  status, and execution non-goals are easy to collapse.
- Impact Overview, because entity significance can become an evidence dump if
  every known detail is pulled into the default view.
- Execution Status, because current work visibility, operator feedback, event
  emission, projection state, and interface rendering can blur.

### Strongest operator-oriented surfaces

- State Summary.
- Impact Overview.
- Execution Status and Operator Feedback.
- Current Work Position and Active Edge.
- Fact Support / Why / Why Fact when used to answer support and evidence
  questions.
- Source Navigation when it answers source-backed operator questions.
- Contradiction visibility and stale-fact visibility.

### Strongest implementation-oriented surfaces

- Source navigation implementation and query-design audits.
- Repository/source inventories.
- Capability verification audits and candidate-resolution inventories.
- Execution boundary, producer-contract, and status-emission audits.
- State-summary implementation audits.
- Storage topology, filesystem projection, Prometheus endpoint, and local host
  observation audits.

## Tension Findings

### Inventory vs understanding

Inventory says what is present. Understanding says what matters, what is active,
what is uncertain, and where work can continue. Operator friction appears when a
surface is operator-visible and therefore read as understanding even though it
only exposes inventory.

### Inventory vs explanation

Inventory can show a row without showing why the row appears. Explanation asks
what supports the row, what selected it, what caveat applies, and what scope the
row has.

### Counts vs meaning

Counts communicate volume and projection shape. They do not necessarily
communicate learning, importance, urgency, correctness, or relevance. Fact
volume, observation frequency, and source shape can dominate counts without
settling meaning.

### Presence vs relevance

A fact, endpoint, filesystem row, source file, capability candidate, rule, or
conflict can be present without being relevant to the operator's current
question. Relevance requires additional context, selection, explanation, or
understanding.

### Support visibility vs understanding

Support visibility can expose facts, evidence, confidence, freshness, and source
families. That does not automatically tell an operator why the supported claim
matters now or how it should affect continuation. Support can explain a claim
while still leaving significance unresolved.

### Implementation visibility vs operator usefulness

Implementation work often needs exact file paths, predicates, registry entries,
provider metadata, test names, event boundaries, projection mechanics, and raw
measurement dimensions. Operator usefulness often depends on scope, meaning,
uncertainty, attention, and safe conclusions. A surface can be useful to both,
but friction appears when it does not make which role it is serving legible.

### Understanding vs explanation

Understanding asks what matters, what is active, what is uncertain, and where
work is situated. Explanation asks why a visible item, selection, status, or
claim is supported. They reinforce each other but do not collapse. A surface can
explain why a fact is visible without saying whether it matters now; a surface
can identify active pressure while still needing explanation for why that edge
was selected.

## Unresolved Observations

The evidence suggests, but does not settle, these observations:

1. Inventory, understanding, and explanation appear distinct enough to describe
   current friction, but the repository has not reconciled them as canonical
   surface families.
2. Mixed surfaces are common and may be unavoidable because operator questions
   often cross presence, relevance, and support.
3. State Summary appears most overloaded, but the evidence does not decide what
   it should become.
4. Source Navigation appears to bridge implementation and operator evidence, but
   the evidence does not decide whether it is primarily an implementation aid or
   an operator explanation surface.
5. Fact Support appears explanation-shaped, but support visibility alone does
   not guarantee operator understanding.
6. Current Work Position and Active Edge look strongly understanding-shaped, but
   they remain exploratory frontier concepts rather than reconciled operator
   surface categories.
7. Explanation appears to be emerging as a first-class concern alongside
   inventory and understanding, but current authority treats it as read-only
   vocabulary and projection-backed support rather than a new engine.
8. Operator-facing placement may itself create meaning pressure: once a surface
   is visible by default, operators may ask it to communicate relevance even if
   its current authority is only inventory.

## Overall Observation

Current Seed evidence supports a cautious observation:

```text
Operator-facing and operator-adjacent surfaces currently cluster around
inventory, understanding, and explanation concerns, but many existing surfaces
mix those concerns.
```

Inventory surfaces show what exists, what is counted, what is stored, and what
is registered. Understanding surfaces orient attention, uncertainty, active
pressure, significance, and continuation. Explanation surfaces expose why
something is visible, selected, supported, stale, contradicted, or scoped.

The strongest operator friction appears near surfaces that expose inventory in a
position where operators reasonably expect understanding or explanation. The
strongest emerging pressure is not to replace inventory. It is to preserve the
boundary between presence, relevance, and support so future participants can
read current surfaces without mistaking counts for meaning, visibility for
importance, or support listing for understanding.
