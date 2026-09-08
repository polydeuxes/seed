---
doc_type: frontier
status: exploratory
domain: operation attribution ontology
defines:
  - operation attribution frontier
  - operation actor boundary
  - operation participation boundary
  - attribution authority boundary
  - attribution provenance relationship
depends_on:
  - operations_frontier.md
  - agency_and_attribution_reconciliation.md
  - principal_identity_reconciliation.md
  - goal_policy_and_operator_authority_reconciliation.md
  - adoption_decision_authority_reconciliation.md
  - capability_authority_and_execution_boundary_reconciliation.md
  - foundational_ontology_reconciliation.md
  - architectural_status_and_next_frontier.md
related:
  - observation_evidence_change_event_reconciliation.md
  - cross_seed_provenance_and_federation_reconciliation.md
  - learning_and_knowledge_change_reconciliation.md
  - contradiction_discovery_and_visibility_reconciliation.md
  - prediction_forecasting_and_future_claims_reconciliation.md
  - recommendation_selection_boundary.md
  - documentation_observation_frontier.md
---

# Operation Attribution Frontier

## Purpose

This document characterizes a documentation-only frontier exposed by the
operations ontology:

```text
Every operation appears to have some actor, participant, origin, or executor.

What does it mean to attribute an operation?
```

It investigates whether operation attribution is agency, authority, ownership,
responsibility, provenance, or a distinct concern. It does not assume the answer
is known.

It is documentation only. It does not implement code, modify schemas, modify
runtime behavior, add tests, define a permission system, design RBAC, introduce
a workflow engine, create an approval system, define runtime attribution
mechanisms, track execution, or prescribe any executor behavior.

Repository authority wins over this document. The existing operations, agency,
attribution, principal, operator-authority, adoption, capability-authority,
execution-boundary, provenance, learning, and foundational ontology documents
remain authoritative for their reconciled boundaries.

---

## Background Finding

The operations frontier suggested that Seed may need vocabulary for what happens
to represented knowledge, not only vocabulary for what is represented. Candidate
operations included:

```text
acquisition
preservation
comparison
corroboration
interpretation
derivation
calculation
extrapolation
revision
correction
selection
projection
reconciliation
navigation
assessment
recommendation generation
```

Those operations immediately expose actor questions:

```text
Who performed the operation?
Who initiated it?
Who supplied the support?
Who approved it?
Who is accountable?
Who owns its result?
Who merely observed it?
Who consumed it?
```

The frontier exists because these questions are related but not identical. A
Prometheus scrape, a contradiction discovery, a forecast, a recommendation, and
a documentation-navigation relationship can all be represented or explained, but
the relevant participants differ.

---

## Central Question

The central question is:

```text
What does it mean to attribute a knowledge operation?
```

A tentative answer under test is:

```text
Operation attribution records a supportable claim about who or what participated
in, originated, performed, supplied, observed, approved, adopted, consumed, or
became accountable for an operation.
```

That answer is intentionally broad and probably too broad. It is useful because
it prevents premature collapse into one actor role. It is unsafe if it implies
that every role is attribution in the same sense.

Safer current wording:

```text
Operation attribution is the unresolved ontology of actor participation in
knowledge operations.
```

This wording preserves uncertainty. It allows attribution to include performer,
originator, source, initiator, approver, adopter, executor, owner, observer, and
consumer roles without deciding that all of those roles belong in one final
concept.

---

## Initial Non-Assumptions

This investigation does not assume that:

- every operation has exactly one actor;
- actors are humans;
- attribution implies authority;
- attribution implies approval;
- attribution implies ownership;
- attribution implies responsibility;
- attribution implies agency;
- attribution implies consciousness, intent, preference, or desire;
- execution is the only actor role;
- the actor that supplies evidence is the actor that performs the operation;
- the actor that performs an operation owns the result;
- the actor that adopts a recommendation generated it;
- the actor that authorizes an operation executed it;
- the actor that observes an operation caused it.

These non-assumptions are architectural guardrails. They preserve the separation
between ontology discovery and implementation design.

---

## Operation Versus Actor

The operations frontier can be summarized as:

```text
Operations answer:
    What happened to represented knowledge?
```

Operation attribution asks a different question:

```text
Actors answer:
    Who or what participated in what happened?
```

This suggests a four-part distinction, still under test:

```text
Objects answer:
    What is represented?

Relations answer:
    How are represented things connected?

Operations answer:
    What happened to represented knowledge?

Actors answer:
    Who or what participated in what happened?
```

The distinction is useful, but it must not become a schema prescription.
Objects, relations, operations, and actors may overlap in representation. For
example, a provider can be represented as an entity, participate as an actor,
supply a capability, and appear in provenance. Those are different explanatory
roles, not necessarily different database tables or runtime components.

### Findings

| Question | Preliminary finding |
| --- | --- |
| Can the same operation be performed by different actors? | Yes. Acquisition may be performed by Seed, a federated Seed, a provider, a tool, or an external source depending on vantage point and operation boundary. |
| Can multiple actors participate in one operation? | Yes. A scrape may involve target, Prometheus, Seed, provider, parser, and operator-policy context. They need not share the same role. |
| Can attribution exist without authority? | Yes. A source may originate a claim without being authoritative for its truth, and a tool may execute a calculation without deciding that it should be trusted. |
| Can authority exist without attribution? | Possibly. A policy or operator may authorize a class of operation without being attributed as performer of a specific occurrence. However, explainability may still require an authority trace. |
| Can attribution exist without ownership? | Yes. A capability may generate a forecast without owning its lifecycle. A source may supply evidence without owning the derived conclusion. |
| Can ownership exist without execution? | Yes. A domain owner or repository owner may be responsible for lifecycle, correction, or retirement even if another actor performed the operation. |

---

## Candidate Actor Categories

The following categories are candidates, not a final ontology. Several are
roles, not kinds of entities. One entity may occupy multiple roles in a single
operation, and one role may be occupied by multiple entities.

| Candidate actor category | Candidate question answered | Notes |
| --- | --- | --- |
| Operator | Who supplied purpose, constraints, command, review, or decision context? | Strong existing concept. Operator involvement must not be confused with every operation Seed performs. |
| Seed | Did Seed as a system recognize, preserve, derive, select, project, or explain something? | Useful for system-level attribution, but too coarse for execution details. |
| Federated Seed | Did another Seed instance supply testimony, evidence, projection, interpretation, or operation result? | Important for provenance and federation. Import does not transfer truth or verification. |
| Observation source | From what source or vantage point did observed material originate? | Source is not automatically performer. A target may expose metrics while Prometheus performs scrape acquisition. |
| External system | Did an external service, monitoring system, repository, package manager, API, or host process participate? | May be source, provider, executor, or environment depending on boundary. |
| Provider | Who or what supplies implementation behavior for a capability or execution path? | Provider can support work without being authoritative, trusted, adopted, or responsible for results. |
| Capability | What possible class of work was involved? | Usually not an actor by itself. It names possibility. Treating capability as actor risks capability-as-agency. |
| Agent | Did an autonomous or semi-autonomous participant choose, perform, propose, or coordinate an operation? | Candidate role only. Must not imply consciousness or unrestricted authority. |
| Tool | What callable interface or instrument performed bounded work? | Tool may execute but usually does not own policy, purpose, or result interpretation. |
| Runtime component | Which internal component routed, parsed, materialized, projected, or preserved something? | Useful for auditability, but implementation component identity is not foundational ontology by default. |
| Documentation author | Who authored a document, metadata, assertion, explanation, or relationship in documentation? | Authoring is a communicative or documentation operation, not authority over all downstream interpretations. |
| Principal | On whose behalf or under whose identity was an operation authorized, requested, or represented? | Principal is adjacent to authority and identity; it is not identical to performer. |
| Owner | Who is responsible for lifecycle, correction, stewardship, or retirement? | Ownership can attach to object, capability, document, domain, or process, not necessarily to operation performance. |
| Approver | Who accepted, allowed, or ratified an operation or result? | Approval is separate from generation and execution. |
| Adopter | Who adopted a recommendation, provider, policy, assumption, or conclusion for use? | Adoption is acceptance into a decision or usage context, not proof of truth. |
| Executor | Who or what carried out the concrete work attempt? | Execution attribution is narrower than operation attribution. Some knowledge operations may be recognitions rather than executions. |
| Observer | Who observed that an operation, state, or result existed? | Observation of an operation is not the same as causing or performing it. |
| Consumer | Who used, selected, displayed, or relied on the operation result? | Consumption can matter for explainability but does not imply authorship. |
| Model | Did a model generate, classify, summarize, infer, or transform represented material? | Model attribution may be relevant, but model-as-actor should not erase operator, provider, prompt, data, or runtime roles. |
| Collective system | Did a coordinated system of operators, models, tools, Seeds, and providers produce the result? | Useful where single-actor attribution is misleading. Needs caution to avoid vague accountability. |

### Candidate Rejections Or Merges

Some prompt candidates should be narrowed:

- `capability` is better treated as a possible class of work than as an actor,
  unless a future document defines actor-like capability instances. Current
  authority documents warn against capability-as-agency.
- `tool` and `provider` should remain separate. A provider supplies behavior;
  a tool exposes a callable interface. Either may appear in attribution.
- `observation source` and `actor` should not be merged. A source may originate
  data without performing Seed's acquisition, interpretation, or projection.
- `Seed` and `runtime component` should not be merged. `Seed` is useful for
  system-level knowledge attribution; runtime component identity is useful only
  when the implementation path matters for auditability.
- `operator` and `principal` should not be merged. An operator may act on behalf
  of a principal, under a principal, or outside a principal model; principal
  identity answers a different authority and representation question.

---

## Attribution Versus Authority, Responsibility, Ownership, Approval, Adoption, And Execution

Operation attribution sits among several adjacent concepts. It should not
collapse them.

| Concept | Candidate question | Boundary finding |
| --- | --- | --- |
| Attribution | Who or what participated in, originated, performed, supplied, observed, or is otherwise linked to an operation? | Descriptive and evidentiary. Does not by itself grant permission, prove truth, or assign ownership. |
| Authority | Who or what was allowed to perform, approve, rely on, or represent the operation in a scope? | Normative or policy-like. Can constrain operations without being the performer. |
| Responsibility | Who is answerable for correctness, maintenance, consequence, or remediation? | May follow from ownership, role, policy, or adoption; not automatic from performance. |
| Ownership | Who stewards lifecycle, correction, retirement, or domain accountability? | May attach to results, domains, capabilities, documents, or processes independent of performer. |
| Approval | Who accepted or allowed a proposal, operation, result, provider, or decision point? | Approval may precede or follow an operation; it is not generation. |
| Adoption | Who selected a recommendation, provider, assumption, or conclusion for use? | Adoption changes usage status, not origin or truth. |
| Execution | Who or what carried out a concrete work attempt? | Execution is an actor role for concrete work, but some operations are recognitions, interpretations, or relationship discoveries. |

### Boundary Tests

```text
Attribution can exist without authority.
```

A third-party package index may supply package metadata. Seed may attribute an
acquired observation to that source without treating it as authoritative for
all package truth.

```text
Authority can exist without operation performance.
```

An operator may authorize a scrape policy, but Prometheus or a runtime path may
perform the concrete acquisition.

```text
Ownership can exist without execution.
```

A documentation owner may be responsible for maintaining metadata even if a tool
generated navigation relationships from it.

```text
Execution can exist without approval of the result.
```

A tool can compute a forecast; an operator or policy may later reject the
forecast, mark it caveated, or decline to adopt a recommendation derived from it.

```text
Approval can exist without ownership.
```

A reviewer may approve a one-time operation without becoming steward of the
result's lifecycle.

---

## Relationship To Agency

Operation attribution is adjacent to agency but should not currently be treated
as identical to agency.

Agency asks whether an entity can be understood as acting, choosing, initiating,
or pursuing a purpose in a relevant scope. Existing attribution work warns that
language attribution is a supportable claim, not proof of consciousness, desire,
or agency. Operation attribution should preserve the same humility.

Preliminary characterization:

```text
Agency concerns the capacity or role of acting.
Operation attribution concerns supportable participation in a particular
operation or operation result.
```

Therefore:

- An actor can be attributed without being treated as a full agent.
- A tool can be attributed as executor without being attributed with intent.
- A source can be attributed as origin without being attributed with approval.
- A model can be attributed as generator without being attributed with ownership.
- An operator can be attributed as initiator or approver without being the direct
  executor.
- Seed can be attributed as recognizer or preserver without implying that Seed
  has human-like agency.

This suggests operation attribution is **adjacent to agency**. It may partly
belong inside a broader agency ontology in the future, but it currently appears
more general: attribution can attach to sources, tools, capabilities, models,
components, documents, and systems that should not all be promoted to agents.

---

## Relationship To Provenance

Operation attribution appears to contribute directly to provenance, but it is
not the whole of provenance.

Provenance asks how represented knowledge came to be known, acquired,
transformed, supported, selected, imported, or exposed. Operation attribution
adds actor-role information to that lineage:

```text
source -> acquisition actor -> preservation path -> interpretation actor
       -> derivation/calculation/extrapolation actor -> projection/selection actor
       -> consumer/adopter/executor
```

This sequence is illustrative only. It is not a workflow or required pipeline.

Potential provenance contributions:

- **Explainability:** exposes why a result exists and which actor roles were
  involved.
- **Lineage:** distinguishes source material from derived, interpreted, or
  projected knowledge.
- **Auditability:** supports later review of who or what performed, supplied,
  approved, adopted, or consumed an operation.
- **Confidence and caveats:** allows quality concerns to attach to the relevant
  actor role, such as source reliability, model limitations, tool version, or
  operator approval scope.
- **Federation:** keeps foreign testimony, imported projections, and local
  reconciliation separate.

However, provenance must not become authority by default. Knowing who produced a
forecast does not prove that the forecast is authoritative. Knowing who supplied
support does not mean that actor owns the conclusion.

---

## Critical Examples

### Example 1: Observation Acquisition

```text
Prometheus endpoint scraped.
Observation preserved.
```

Candidate operation split:

| Operation | Candidate actor roles |
| --- | --- |
| Metric exposure | Target, exporter, service, host, or external system exposes material. |
| Scrape acquisition | Prometheus or monitoring provider performs scrape from its vantage point. |
| Observation ingestion | Seed or a Seed provider path imports or reads Prometheus result. |
| Preservation | Seed preserves observation, evidence, and source scope. |
| Projection | Seed may later project endpoint, service, host, or availability views with caveats. |

Preliminary finding:

```text
Prometheus, Seed, and the target can all participate, but not in the same
operation role.
```

The target may originate or expose metrics. Prometheus may perform scrape
acquisition. Seed may acquire from Prometheus and preserve an observation. A
provider or tool may execute the query path. The operator may authorize or
request the observation. None of these roles alone proves host availability,
service ownership, or truth beyond the scoped evidence.

### Example 2: Contradiction Discovery

```text
Claim A exists.
Claim B exists.

Later:

A contradicts B.
```

Candidate operation split:

| Operation | Candidate actor roles |
| --- | --- |
| Claim origination | Sources, documentation authors, external systems, imported Seeds, or operators may originate the claims. |
| Claim preservation | Seed preserves each claim and support. |
| Comparison | Seed, a model, a rule, an operator, or a capability-supported tool compares claims. |
| Contradiction recognition | Seed may recognize the contradiction as represented knowledge. |
| Contradiction ownership | A domain owner or documentation owner may steward remediation; the contradiction itself is not owned by the sources merely because they supplied support. |

Preliminary finding:

```text
The actor that supplied a claim is not necessarily the actor that discovered the
contradiction.
```

The contradiction may have been latent before discovery. Attribution should be
able to distinguish claim sources from comparison performer, contradiction
recognizer, remediation owner, and consumers of the contradiction warning.

### Example 3: Forecasting

```text
Disk usage exists.

Forecast produced.
```

Candidate operation split:

| Operation | Candidate actor roles |
| --- | --- |
| Measurement acquisition | Prometheus, filesystem observation path, Seed, provider, tool, or external system supplies observations. |
| Historical preservation | Seed preserves historical evidence. |
| Extrapolation | Model, statistical method, tool, capability path, Seed, or operator performs forecast generation. |
| Forecast stewardship | Owner or domain steward maintains lifecycle, caveats, and correction behavior. |
| Accountability for quality | May belong to method owner, model/provider adopter, operator, domain owner, or Seed policy context depending on scope. |

Preliminary finding:

```text
Forecast attribution is multi-layered: data source, method, performer, adopter,
and accountable steward may differ.
```

A forecast is not an observation of the future. It is an extrapolated or derived
claim with assumptions. The actor that executes extrapolation does not
necessarily own the forecast or approve actions based on it.

### Example 4: Recommendation Generation

```text
Forecast exists.

Recommendation produced.
```

Candidate operation split:

| Operation | Candidate actor roles |
| --- | --- |
| Assessment | Seed, model, operator, or tool evaluates forecast against criteria. |
| Recommendation generation | Seed, model, capability path, operator, or external advisory system proposes a course of action. |
| Adoption | Operator, policy, decision authority, or responsible role accepts or selects the recommendation for use. |
| Rejection | Operator, policy, decision authority, or responsible role rejects, defers, or escalates it. |
| Execution | Runtime path, provider, tool, external system, or human carries out accepted work if authorized. |

Preliminary finding:

```text
Generation, adoption, rejection, and execution are different operation roles.
```

Recommendation attribution must not imply command authority. A recommendation
can be generated by a model, selected by Seed for display, adopted by an
operator, and executed by a provider. Those are separate actor relationships.

### Example 5: Documentation Navigation

```text
Document metadata exists.

Navigation relationships observed.
```

Candidate operation split:

| Operation | Candidate actor roles |
| --- | --- |
| Metadata authoring | Documentation author, maintainer, or generator creates metadata. |
| Metadata observation | Seed, documentation observer, parser, or runtime component reads metadata. |
| Relationship generation | Seed, tool, model, script, or author derives navigation relationships. |
| Relationship consumption | Operator, reader, UI, documentation index, or future Seed uses the relationships. |
| Lifecycle stewardship | Documentation owner or domain owner maintains correctness and retirement. |

Preliminary finding:

```text
Authoring metadata, observing metadata, generating navigation relationships, and
consuming navigation are separable.
```

A documentation author may not have generated every downstream navigation
relationship. A tool may generate relationships without owning their lifecycle.
Seed may consume relationships without treating them as authoritative beyond the
supporting documents.

---

## Actor Role Vocabulary Under Consideration

A future ontology may need role names more precise than a single `actor` label.
Candidate roles include:

| Role | Candidate meaning | Example |
| --- | --- | --- |
| Originator | The source from which material or assertion first entered the relevant scope. | Documentation author originates front matter. |
| Performer | The actor that carried out the operation as characterized. | Prometheus performs scrape acquisition. |
| Initiator | The actor that caused or requested the operation to begin. | Operator requests a bounded observation. |
| Authorizer | The actor or policy context that allowed operation in scope. | Operator or policy allows scrape query. |
| Approver | The actor that accepts a result, proposal, or operation. | Reviewer approves a generated doc change. |
| Adopter | The actor that selects a recommendation, provider, or conclusion for use. | Operator adopts a remediation recommendation. |
| Executor | The actor that carries out concrete work. | Tool executes forecast calculation. |
| Source | The actor or system that supplied observed material or testimony. | Prometheus supplies metrics to Seed. |
| Subject | The represented thing the operation concerns. | Disk is subject of forecast. |
| Observer | The actor that observed an operation or state. | Seed observes metadata. |
| Consumer | The actor that uses the operation result. | UI consumes navigation graph. |
| Owner | The actor responsible for lifecycle stewardship. | Documentation owner maintains metadata. |
| Accountable actor | The actor answerable for quality, consequence, or remediation in a scope. | Domain owner accountable for forecast policy. |
| Support supplier | The actor that supplied evidence, assumptions, or method. | External system supplies history; model supplies method. |
| Interpreter | The actor that assigns meaning to ambiguous material. | Seed interprets natural-language text as candidate intent. |
| Reconciler | The actor that brings competing claims, authorities, or meanings into relation. | Operator or Seed reconciles conflicting docs. |

These roles may be more stable than actor categories. A `provider`, `tool`,
`operator`, or `Seed` may occupy one or more roles depending on the operation.

---

## Required Tensions

The following tensions remain unresolved:

| Tension | Why it matters |
| --- | --- |
| Actor vs source | A source supplies material; an actor may perform a knowledge operation over that material. Merging them over-attributes source agency. |
| Actor vs capability | A capability names possible work; an actor participates in a particular occurrence. Merging them creates capability-as-agency. |
| Actor vs tool | A tool can execute bounded work without owning purpose, approval, or result interpretation. |
| Actor vs principal | A principal may be represented identity or on-behalf-of authority; performer may be a different operator, system, or tool. |
| Actor vs owner | Performer and lifecycle steward often differ. Ownership should not be inferred from execution. |
| Actor vs authority | Attribution describes participation; authority constrains permission or legitimacy in scope. |
| Actor vs executor | Executor is one actor role. Operation attribution may also include source, initiator, approver, adopter, owner, observer, and consumer. |
| Single actor vs multiple actors | Many operations are distributed across source, provider, tool, Seed, operator, and owner. Single-actor attribution may be misleading. |
| Human attribution vs system attribution | Human authorship, operator approval, model generation, tool execution, and Seed recognition require different caveats. |
| Coarse system attribution vs component attribution | `Seed did it` may be enough for conceptual explanation but insufficient for audit; component-level attribution may be too implementation-specific for ontology. |
| Latent relation vs discovered relation | A contradiction can exist latently before discovery; attribution should distinguish condition, discovery, and representation. |
| Generated result vs adopted result | A recommendation or forecast can be generated but rejected. Attribution must separate generation from acceptance. |
| Imported testimony vs local operation | A federated Seed may testify to a result; local Seed may import, preserve, reconcile, or project it without verifying it. |

---

## Learning Connection

Learning may be attributable, but the actor question is especially unstable.

Candidate learning-attribution questions:

```text
Who learned?
Seed?
An operator?
A federated Seed?
A capability?
A model?
A documentation corpus?
A collective system?
```

Preliminary finding:

```text
Learning attribution depends on what learning means in the specific boundary.
```

If learning means Seed's represented knowledge changed, Seed may be the learned
system. If learning means an operator gained understanding, the operator may be
the learner. If learning means a model was trained or adapted, the model or
training system may be involved. If learning means a federated Seed imported
foreign testimony, the local Seed may have acquired testimony without verifying
or internalizing the foreign Seed's authority.

Therefore operation attribution should avoid phrases such as `Seed learned`
without preserving the operation role:

- acquired testimony;
- recognized contradiction;
- revised support;
- corrected a claim;
- adopted a conclusion;
- updated a projection;
- changed future selection behavior;
- improved operator understanding;
- trained or updated a model.

Learning attribution is important for explainability, but premature
implementation would risk collapsing knowledge change, model training, operator
understanding, and federation into one overloaded concept.

---

## Frontier Findings

### Attribution Findings

1. Operation attribution appears important because operations are not fully
   explained by their result objects.
2. Attribution should describe actor participation, not automatically authority,
   ownership, approval, or truth.
3. Actor roles may be more precise than actor categories.
4. Multi-actor attribution is likely normal, not exceptional.
5. Actor attribution should be evidence-backed and scoped to the operation role.
6. Attribution may attach to source, originator, performer, executor, initiator,
   authorizer, approver, adopter, owner, observer, and consumer roles.
7. The same represented entity may be an object in one context and an actor in
   another.

### Authority Relationship Findings

1. Authority answers whether an actor was allowed, entitled, or accepted in a
   scope; attribution answers who or what participated.
2. Authority can constrain attribution but should not be inferred from it.
3. Approval, adoption, and execution-request authority remain distinct from
   operation performance.
4. Provider, tool, model, and source attribution do not by themselves establish
   trust or authority.
5. Operator authority may initiate, approve, adopt, or authorize operations
   without making the operator the performer.

### Agency Relationship Findings

1. Operation attribution is adjacent to agency but more general than agency.
2. Attribution can apply to non-agentive participants such as sources, tools,
   runtime components, models, and documents.
3. Agency should not be inferred merely because an entity appears in an actor
   role.
4. Seed-level attribution should not imply human-like intent.
5. Capability-as-agency remains a rejected collapse unless future evidence
   changes the boundary.

### Provenance Findings

1. Operation attribution enriches provenance by recording actor-role lineage.
2. Provenance requires separation of source, import, preservation,
   interpretation, derivation, projection, adoption, and consumption.
3. Attribution supports explainability, lineage, auditability, caveats,
   confidence analysis, and federation boundaries.
4. Provenance is not authority transfer. Imported or attributed material still
   needs scoped support, caveats, and local reconciliation.
5. Actor attribution can identify where quality concerns belong: source,
   method, model, provider, tool, operator decision, owner stewardship, or
   consumer usage.

---

## Why Implementation Would Be Premature

Implementation is premature because the frontier has not resolved:

- whether `actor` is a foundational concept, a role, a relation, a provenance
  facet, or an explanation projection;
- whether operation attribution should be represented for every operation or
  only for operations requiring explanation;
- whether actor categories should be enumerated or roles should remain open;
- how to distinguish source, performer, executor, initiator, authorizer,
  approver, adopter, owner, observer, and consumer without designing workflow;
- how much runtime component detail belongs in ontology rather than audit logs;
- how attribution interacts with federated testimony without becoming truth
  transfer;
- how learning attribution should distinguish Seed knowledge change, operator
  understanding, model adaptation, and collective system change;
- how to preserve multi-actor attribution without creating a permission system
  or execution tracker.

A future implementation should wait until a concrete operator question requires
it and existing provenance, evidence, explanation, authority, and lifecycle
surfaces cannot answer that question.

---

## Non-Goals

This document does not:

- define permissions, RBAC, access control, or policy engines;
- define workflows, approval systems, or execution tracking;
- introduce runtime attribution mechanisms;
- add schema, model, migration, or API requirements;
- modify Seed Runtime, ToolExecutor, providers, projections, observations,
  events, or tests;
- require that every operation be durably represented;
- require that every operation have exactly one actor;
- promote capabilities, tools, models, providers, or Seed to human-like agents;
- infer authority, ownership, approval, adoption, or responsibility from mere
  attribution;
- treat provenance as truth transfer;
- make operation attribution the next active implementation frontier.

---

## Summary

Operation attribution appears important because operations over represented
knowledge are not fully explained by their output objects. An acquisition,
comparison, extrapolation, recommendation, or navigation operation may require
explanation of who or what supplied, performed, initiated, approved, adopted,
executed, owned, observed, or consumed it.

The current best characterization is:

```text
Operation attribution is the unresolved ontology of actor participation in
knowledge operations.
```

It differs from authority because attribution is descriptive and evidentiary,
while authority is normative or permission-like in scope. It differs from
ownership because participation in an operation does not imply lifecycle
stewardship. It differs from approval and adoption because generating or
performing an operation does not imply that the result was accepted. It differs
from execution because execution is only one possible actor role.

The likely actor space includes operators, Seed, federated Seeds, observation
sources, external systems, providers, tools, runtime components, documentation
authors, principals, owners, approvers, adopters, executors, observers,
consumers, models, and collective systems. Capabilities should currently be
handled as possible work rather than actors.

The frontier remains exploratory. It should guide future questions about
explainability, lineage, auditability, provenance, and learning attribution, but
implementation would be premature until a concrete unanswered operator question
requires representation beyond existing evidence, provenance, authority, and
explanation surfaces.
