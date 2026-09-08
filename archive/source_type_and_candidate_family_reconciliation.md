# Source Type And Candidate Family Reconciliation

## Purpose

This reconciliation investigates what determines which candidate family a source
is allowed to produce.

It asks whether candidate-family production is primarily a language phenomenon
or primarily a source-authority phenomenon. It does not assume either outcome.

This is a reconciliation, not an implementation proposal, schema proposal,
runtime workflow, governance model, autonomous planning system, or execution
architecture. Repository authority wins over this document. Existing source
observation, documentation authority, language, operator authority, capability
authority, claim support, fact promotion, and relationship promotion documents
remain authoritative for their scopes.

## Evidence Reviewed

Primary repository evidence reviewed:

- `docs/input_inspection_boundary_reconciliation.md`
- `docs/documentation_prose_as_language_bearing_source_reconciliation.md`
- `docs/candidate_request_and_routing_boundary_reconciliation.md`
- `docs/language_candidate_routing_and_promotion_reconciliation.md`
- `docs/interpretation_candidate_preservation_audit.md`
- `docs/natural_language_request_routing_audit.md`
- `docs/operator_intent_question_and_claim_interface_reconciliation.md`
- `docs/operator_interface_and_projection_authority_reconciliation.md`
- `docs/goal_policy_and_operator_authority_reconciliation.md`
- `docs/capability_authority_and_execution_boundary_reconciliation.md`
- `docs/capability_gap_and_operator_bridge_reconciliation.md`
- `docs/repository_observation_source_design.md`
- `docs/repository_observation_characterization.md`
- `docs/repository_observation_language_boundary.md`
- `docs/repository_observation_implementation_inventory_audit.md`
- `docs/documentation_lineage_observation.md`
- `docs/discovery_path_preservation_observation.md`
- `docs/lineage_distinction_observation.md`
- `docs/current_work_position_frontier.md`
- `docs/active_edge_frontier.md`
- `docs/continuity_frontier.md`
- `docs/handoff_and_continuation_lineage_frontier.md`
- `docs/claim_support_characterization.md`
- `docs/evidence_strength_and_claim_strength_reconciliation.md`
- `docs/corroboration_and_fact_promotion_reconciliation.md`
- `docs/relationship_promotion_reconciliation.md`
- `docs/reality_fact_and_claim_reconciliation.md`
- `docs/claim_strength_and_assertion_semantics_reconciliation.md`
- `docs/learning_as_lens_observation.md`

Implementation surfaces were reviewed only where they clarify present repository
shape: input inspection tests, runtime decision and request-tool paths,
repository observation implementation and tests, relationship observation tests,
fact/evidence projection surfaces, and documentation navigation. This document
does not change those surfaces.

## Executive Finding

Repository evidence supports neither collapse:

```text
all language is request-like
```

nor collapse:

```text
all sources are fundamentally different
```

The stronger explanation is:

```text
source identity + authority scope + observation/interpretation boundary
    constrain which candidate families are safe,
while language form influences candidate content and ambiguity.
```

Language is a powerful medium because it can carry assertions, questions,
commands, constraints, examples, tensions, and pressures. But language alone does
not determine whether a sentence is a request, claim, fact, command, or
architecture. Source identity and authority context decide which interpretations
are candidates and which promotions are allowed.

A source can produce more than one candidate family, and different source types
can produce the same candidate family. The boundary is not one source to one
candidate family. The boundary is that candidate content must not exceed what the
source, channel, document role, and evidence support.

## Part 1: Candidate Families

Repository evidence currently supports the following candidate families as
recurring, not necessarily canonical ontology.

| Candidate family | Evidence-backed role | Boundary |
| --- | --- | --- |
| Relationship candidates | Edge-shaped possibilities from imports, declarations, architecture edges, lineage links, references, containment, routes, or other source-supported connections. | A relationship candidate is not behavior, ownership, verification, or current selection. |
| Fact candidates | Normalized claim possibilities supported by observations, evidence, source declarations, measurements, or operator declarations. | A fact candidate is not verified truth, selected current state, or environmental reality by default. |
| Request candidates | Possible things an operator communicative act may be asking for. | A request candidate is not a command, selected capability, execution decision, or proof of capability existence. |
| Route candidates | Possible architectural boundaries that should consider an interpreted candidate. | Routing is not capability selection and not execution authority. |
| Claim candidates | Assertable propositions extracted from documentation, operator language, observations, code declarations, or evidence views. | A claim candidate requires support and strength assessment before promotion. |
| Boundary candidates | Possible distinctions or non-collapse lines surfaced by reconciliations, audits, or source comparisons. | A boundary candidate is not governance, enforcement, or schema. |
| Pressure candidates | Unresolved tensions, frontiers, pain signals, preservation pressures, or repeated concerns that may guide future inquiry. | Pressure is not command, roadmap commitment, or implementation authority. |
| Question candidates | Possible questions implied by operator language, documentation gaps, observations, contradictions, or frontier work. | A question candidate is not an answer and not necessarily a request to execute. |
| Target candidates | Possible objects of an operator request or source interpretation, such as which summary, artifact, entity, route, or capability is in scope. | A target candidate is not selected merely because it is available. |
| Capability candidates | Possible capability needs, gaps, recommendations, or matching operations. | Capability possibility is not capability authority, verification, availability, or execution approval. |
| Observation candidates | Possible source-attributed observations or source facts extracted from artifacts, measurements, operator declarations, or tool outputs. | Observation preservation is not truth promotion. |
| Continuation / handoff candidates | Possible current work, active edge, or continuation alignment signals preserved in handoffs and frontiers. | Continuation material is not autonomous planning authority. |
| Learning-lens candidates | Possible interpretations of support change, decompression, or understanding shifts. | The learning lens is not promoted into ontology merely because it explains multiple cases. |

The strongest candidate families are relationship, fact, request, route, claim,
pressure, and boundary candidates because multiple documents independently rely
on them and because their non-collapse boundaries are repeatedly explicit.

## Part 2: Source Families

Repository evidence supports these source families as current recurring inputs:

| Source family | Examples | Authority tendency |
| --- | --- | --- |
| Repository source code | Python modules, tests, imports, definitions, registrations, static metadata. | Strong for direct source-structure claims; weak for runtime behavior unless execution or tests specifically support it. |
| Generated repository artifacts | Architecture graph JSON, generated diagrams, deterministic inventories. | Strong for declared/generated artifact content; not proof of freshness or code conformance. |
| Documentation artifacts | Reconciliations, audits, status docs, frontiers, README/map, vocabularies, designs. | Strong within scoped documentation authority; not automatically runtime truth, command, or implementation. |
| Documentation prose as language-bearing source | Sentences, examples, findings, tensions, recommendations, constraints. | Can support documentation claims and pressures; not automatically operator requests. |
| Operator language | User messages, constraints, questions, priorities, approvals, prohibitions. | Strong for what the operator asked or constrained; weak for environmental truth and architecture truth. |
| Observations and measurements | Local observations, Prometheus samples, tool results, evidence records. | Strong for what a source reported from a vantage point; not necessarily truth or current state. |
| Projections and read models | State summary, fact support, graph issues, current facts, integrity views. | Strong for deterministic view output; not the only preserved interpretation. |
| Handoffs and continuation documents | Bootstrap, continuation, active edge, current work position. | Strong for continuity alignment; not execution plans by themselves. |
| Frontiers and active edges | Current pressures, unresolved inquiry, next frontier documents. | Strong for unresolved attention and preservation pressure; not commitment or command. |
| Catalogs and vocabularies | Predicate, relationship, entity type, capability, operation, and documentation vocabulary surfaces. | Strong for declared vocabulary existence; not population, verification, or behavior. |
| Tests and test results | Test files, names, assertions, actual command output when run. | Test source can support test-exists claims; a test run can support run-result claims. Source existence alone does not prove passing status. |
| Capability and operator authority materials | Capability gaps, operation contracts, policy and approval documents. | Strong for authority boundaries; not proof that a capability should run now. |

The strongest source families are repository source code, documentation
artifacts, operator language, observations/measurements, projections/read models,
frontiers/handoffs, and catalogs/vocabularies.

## Part 3: Candidate Production

### Do source types constrain candidate types?

Yes, but not by a one-to-one mapping. Source type constrains candidate families
through source authority and observation boundaries.

Repository source code can produce relationship candidates when static structure
shows imports, definitions, calls, registrations, containment, or declarations.
The same source can produce claim candidates about what text or code declares.
It cannot, merely by containing executable syntax, produce an authorized
execution instruction for Seed to run.

Documentation artifacts can produce documentation claim candidates, boundary
candidates, pressure candidates, route candidates, question candidates, lineage
candidates, and sometimes request-like candidates when the document records a
request or proposes routing. They do not automatically become operator requests
because their source context is repository artifact, not live operator
communicative act.

Operator language can produce request candidates, target candidates, route
candidates, question candidates, constraints, prohibitions, and operator-claim
candidates. It does not automatically produce environmental fact candidates
except as claims about what the operator said, wanted, believed, or declared.

Observations and measurements can produce fact candidates, evidence candidates,
relationship candidates, contradiction candidates, and current-state pressures.
They do not automatically produce commands, even when the observation says a
state is bad.

### Can one source produce many candidate families?

Yes. A single reconciliation document may preserve claim candidates, boundary
candidates, pressure candidates, route candidates, question candidates, and
lineage candidates. A single operator message may preserve request candidates,
question candidates, claim candidates, target candidates, route candidates,
constraints, and refusal-boundary pressures. A single source file may produce
relationship candidates, declaration claims, test-exists claims, and vocabulary
candidates.

### Can different sources produce the same candidate family?

Yes. Fact candidates may arise from measurements, documentation declarations,
operator declarations, code metadata, generated architecture artifacts, or tool
outputs. Relationship candidates may arise from source imports, generated graph
edges, documentation lineage, catalog entries, or observation outputs. Claim
candidates may arise from almost any source that asserts something. The family
is shared, but source authority changes claim strength and permissible
promotion.

### Does language automatically imply request candidates?

No. Documentation prose is language, but repository evidence explicitly rejects
collapsing all prose into operator requests. Language can be request-bearing when
source context supports a communicative act addressed to the system or an
operator-facing interface. Otherwise it may be documentation evidence, claim
content, frontier pressure, example, rejected concept, or lineage.

### Does prose automatically imply claim candidates?

No, but prose often makes claim-candidate extraction possible. Examples,
questions, headings, diagrams, quoted prompts, and rejected collapses may not be
claims in the same sense as architectural findings. Prose can contain claims,
requests, examples, tensions, commands quoted for analysis, or non-authoritative
illustrations. The candidate family depends on document role, local wording,
source context, and authority scope.

## Part 4: Authority

Authority determines whether a candidate may be promoted, routed, preserved only,
or rejected as overreach.

### Can a source produce candidates that exceed its authority scope?

It can produce overreaching candidates as interpretations to be rejected or
bounded, but it cannot safely promote them as accepted facts, commands, routes,
or architecture. For example, a roadmap mention can produce a future-work
pressure candidate, but not a completion fact. A test file can produce a
test-exists candidate, but not a passing-status fact unless a run result supports
it.

### Can documentation produce request candidates?

Documentation can preserve or describe request candidates, and it can route
future readers toward operator-facing boundaries. It can also contain
instruction-like language. But documentation does not become the current
operator merely by being written in imperative prose. Request candidacy requires
source context that supports communicative-act interpretation or a document role
that explicitly records a request as an artifact of past work.

### Can operator language produce fact candidates?

Yes, but scoped carefully. Operator language can produce facts about the
operator's utterance, stated preference, constraint, approval, denial, or desired
state. It can also produce unsupported environmental claims that become claim
candidates requiring evidence. It cannot make external reality true merely by
asserting it.

### Can source code produce execution candidates?

Source code can contain executable text and can support candidates about
available implementation, operations, command examples, or adapter existence. But
repository evidence rejects treating source code as an executable instruction to
Seed by default. Execution authority requires an operator/request/interface,
capability, policy, approval, and runtime boundary; code syntax alone is not an
instruction to execute.

### Strongest authority constraints

- Observation preserves what a source reported; it does not prove truth.
- Evidence explains why a claim is available; it does not create source
authority by itself.
- Fact promotion normalizes a supported claim; it does not equal verification or
current selected truth.
- Relationship promotion preserves an edge-shaped claim; it does not imply
behavior, ownership, or authority.
- Documentation authority is scoped by document role and lifecycle.
- Operator authority is strong for requests and constraints, not environmental
truth.
- Capability authority and execution authority are downstream of interpretation,
routing, capability selection, policy, and approval.
- Projection authority is view-specific and must not erase preserved evidence or
alternative interpretations.

## Part 5: Language Versus Source

Language is not the determining factor by itself. Source identity is also not
enough by itself. The best repository-supported explanation is layered:

```text
source identity establishes authority context
language or structure supplies interpretable content
a boundary preserves candidate alternatives
a promotion or routing rule determines accepted role
```

### Why documentation prose does not automatically become operator requests

Documentation prose is repository artifact language. It may be authoritative for
a scoped reconciliation, audit, frontier, or navigation role. It is not normally
a live communicative act addressed through the operator interface. Imperative or
request-like grammar inside documentation may be an example, preserved prompt,
future pressure, local convention, or quoted rejected collapse rather than a
current request.

### Why source code does not automatically become executable instruction

Source code is executable by some interpreter or runtime under appropriate
conditions, but repository observation treats it first as evidence. Static code
can justify structural candidates and implementation-existence claims. It does
not authorize the agent to execute it, mutate state, call providers, or treat
defined operations as selected actions.

### Why operator requests do not automatically become environmental truth

Operator language has request and constraint authority in the operator channel,
but it does not observe the external world unless the claim is about the
utterance itself. If the operator says a host is down, Seed may preserve an
operator-claim candidate or desired investigation target. It still needs
observation/evidence before promoting environmental fact candidates.

## Findings

### Strongest candidate families

Relationship, fact, request, route, claim, pressure, boundary, question, target,
capability, observation, continuation, and learning-lens candidates all appear in
repository evidence. The strongest are those repeatedly protected by explicit
non-collapse language: relationship, fact, request, route, claim, pressure, and
boundary candidates.

### Strongest source families

Repository source code, generated artifacts, documentation artifacts, operator
language, observations/measurements, projections/read models, handoffs/frontiers,
catalogs/vocabularies, tests/test results, and authority materials recur across
the reviewed corpus.

### Strongest source-to-candidate relationships

- Repository source code -> relationship candidates, declaration claims,
implementation-existence candidates, test-exists candidates.
- Generated artifacts -> architecture-edge candidates, declared topology
candidates, generated-document lineage candidates.
- Documentation artifacts -> claim candidates, boundary candidates, pressure
candidates, route candidates, lineage candidates, question candidates.
- Operator language -> request candidates, route candidates, target candidates,
question candidates, constraints, operator-claim candidates.
- Observations/measurements -> evidence candidates, fact candidates,
contradiction candidates, freshness/currentness pressures.
- Frontiers/handoffs -> continuation candidates, active-edge candidates,
pressure candidates, unresolved-question candidates.
- Catalogs/vocabularies -> declared-vocabulary candidates, capability candidates,
relationship/fact vocabulary candidates.

### Strongest overlaps

- Claim candidates appear across documentation, operator language, source code,
measurements, catalogs, and generated artifacts.
- Fact candidates can be sourced by multiple evidence types, but their strength
varies by source authority.
- Relationship candidates can be derived from code structure, generated graphs,
documentation lineage, or catalog entries.
- Pressure candidates arise from frontiers, audits, operator pain, contradictions,
and repeated boundary failures.
- Route candidates appear in both operator language work and documentation
navigation work.

### Strongest divergences

- Documentation claim candidates and operator request candidates may use the same
language forms but have different authority contexts.
- Fact candidates and claim candidates overlap in content, but fact promotion
requires normalized support and provenance.
- Relationship candidates and boundary candidates may both name connections, but
relationship candidates describe edges while boundary candidates describe
non-collapse constraints.
- Pressure candidates may look imperative, but they preserve unresolved force
rather than command execution.
- Source code may contain executable syntax, but repository observation treats it
as evidence until an independent execution boundary is crossed.

### Strongest preservation pressures

- Preserve candidate alternatives before promotion or routing.
- Preserve source identity, source location, provenance, vantage point, and
scope.
- Preserve rejected collapses, because many documents use them as boundary
memory.
- Preserve ambiguity between request, claim, question, pressure, and route.
- Preserve documentation lineage and discovery paths where they affect future
understanding.
- Preserve current work position without converting it into autonomous plans.

### Strongest risks of candidate-family collapse

- Treating all language as request-like.
- Treating all prose as claim truth.
- Treating operator claims as environmental facts.
- Treating source code as instruction to execute.
- Treating route candidates as capability selection.
- Treating capability selection as execution authority.
- Treating relationship candidates as behavior or ownership.
- Treating pressure as command.
- Treating projection output as the only preserved interpretation.
- Treating documentation frontiers as roadmap commitments.

## Required Tensions

### Language vs source

Language carries many possible roles, but source context decides whether it is
operator act, documentation evidence, code comment, prompt quote, frontier
pressure, or architecture finding.

### Source vs authority

A source may contain content that appears stronger than its authority. The
repository pattern is to preserve the content as scoped evidence while refusing
to promote overreaching conclusions.

### Candidate family vs candidate content

The same content can appear in multiple families. "Run summary" may be request
candidate content in operator language, an example in documentation, or a test
fixture in code. Candidate family depends on source context and boundary.

### Documentation claim vs operator request

Documentation can state what should be investigated, but that is not identical
to an operator asking now. Operator requests have channel-specific immediacy;
documentation claims have artifact-scoped authority.

### Source code vs instruction

Code is executable in the abstract, but source observation treats code as
repository evidence. Execution requires a separate request/capability/policy
boundary.

### Request vs fact

A request says what the operator may want. A fact says what Seed has normalized
as a supported claim. A request may lead to acquiring evidence, but it is not the
evidence itself.

### Pressure vs command

Pressure preserves unresolved force or repeated concern. A command requires
accepted executable intent and authority. Frontiers and active edges preserve
pressure without becoming commands.

### Boundary candidate vs request candidate

A boundary candidate asks whether a distinction should be preserved. A request
candidate asks what an operator may be asking Seed to do or answer. They can
co-occur but should not collapse.

### Claim candidate vs fact candidate

A claim candidate is a proposition under consideration. A fact candidate is a
possible normalized knowledge representation with provenance. Fact promotion
should not erase claim strength, support, or uncertainty.

## Final Conclusion

Candidate-family production is not primarily a language phenomenon. Language
form matters, but it cannot by itself decide whether material is a request,
claim, fact, pressure, command, or executable instruction.

Candidate-family production is also not simply source identity. One source can
produce many candidate families, and different source families can produce the
same candidate family.

The repository-supported answer is:

```text
candidate-family production is primarily a source-authority and boundary
phenomenon, with language or source structure shaping candidate content.
```

A future participant should therefore ask four questions before promoting or
routing a candidate:

1. What source family produced this material?
2. What authority scope does that source have?
3. What candidate families does the content support without overclaiming?
4. Which boundary decides preservation, routing, promotion, clarification, or
   refusal?

This preserves the recurring pattern:

```text
source
    ↓
inspection / interpretation
    ↓
candidate space
```

without flattening all candidate spaces into one ontology or treating every
source as isolated and incomparable.
