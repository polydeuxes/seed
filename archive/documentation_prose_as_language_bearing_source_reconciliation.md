# Documentation Prose As Language-Bearing Source Reconciliation

## Purpose

This reconciliation investigates what determines the architectural role of prose
when Seed reads language-bearing repository artifacts.

Central question:

```text
When Seed reads prose, what determines whether that prose is source evidence,
documentation claim, frontier pressure, observation, reconciliation content,
operator communicative act, or executable instruction?
```

This is a reconciliation, not a proposal. It does not implement runtime behavior,
propose schemas, define governance, define execution workflows, define an
autonomous action system, or create new ontology. Repository authority wins over
this document. Existing documentation authority, observation, language,
operator-authority, capability-authority, claim-support, and evidence documents
remain authoritative for their own scopes.

## Evidence Reviewed

Primary evidence reviewed:

- `docs/documentation_authority_reconciliation.md`
- `docs/documentation_boundary_enforcement_reconciliation.md`
- `docs/documentation_authority_and_seed_thesis_reconciliation.md`
- `docs/documentation_lineage_observation.md`
- `docs/discovery_path_preservation_observation.md`
- `docs/lineage_distinction_observation.md`
- `docs/preservation_surface_observation.md`
- `docs/continuity_frontier.md`
- `docs/current_work_position_frontier.md`
- `docs/active_edge_frontier.md`
- `docs/architectural_status_and_next_frontier.md`
- `docs/documentation_observation_frontier.md`
- `docs/documentation_observation_characterization.md`
- `docs/repository_observation_frontier.md`
- `docs/repository_observation_source_design.md`
- `docs/repository_observation_language_boundary.md`
- `docs/repository_reconciliation_frontier.md`
- `docs/repository_reconciliation_v1_frontier.md`
- `docs/learning_as_lens_observation.md`
- `docs/natural_language_observation_and_intent_derivation_reconciliation.md`
- `docs/operator_intent_question_and_claim_interface_reconciliation.md`
- `docs/candidate_request_and_routing_boundary_reconciliation.md`
- `docs/language_candidate_routing_and_promotion_reconciliation.md`
- `docs/input_inspection_boundary_reconciliation.md`
- `docs/input_inspection_reconciliation.md`
- `docs/natural_language_request_routing_audit.md`
- `docs/capability_authority_and_execution_boundary_reconciliation.md`
- `docs/capability_gap_and_operator_bridge_reconciliation.md`
- `docs/goal_policy_and_operator_authority_reconciliation.md`
- `docs/operator_interface_and_projection_authority_reconciliation.md`
- `docs/evidence_trust_and_source_authority_reconciliation.md`
- `docs/evidence_strength_and_claim_strength_reconciliation.md`
- `docs/claim_support_characterization.md`
- `docs/claim_support_design.md`

Implementation surfaces were sampled only as context for existing observation,
evidence, input inspection, and capability boundaries. No runtime behavior is
changed by this reconciliation.

## Executive Finding

Repository evidence supports this distinction:

```text
prose is language-bearing material
    but architectural role comes from source context, document role,
    authority scope, observation boundary, interpretation boundary,
    promotion rules, routing rules, and execution authority
```

Therefore:

```text
language content
    !=
operator communicative act
```

and also:

```text
instruction-like wording
    !=
executable instruction by default
```

Documentation prose and operator prose overlap because both are language that can
be observed, cited, interpreted, and used as support for claims about what was
written or requested. They diverge because operator language is situated as a
communicative act in an operator/interface context, while repository
documentation is situated as an artifact with a documentation lifecycle role,
scoped authority, provenance, and routing boundaries.

The repository does not justify a single shared architectural boundary that makes
all prose into operator requests. It also does not justify treating documentation
as inert. Documentation can influence future work as evidence, authority-scoped
claim, frontier pressure, preservation surface, or routing input, but that
influence is mediated by repository authority boundaries and later acceptance,
not by prose form alone.

## Part 1: Language As Medium

Language preserves content that can be quoted, inspected, attributed, compared,
interpreted, decomposed into claims, and linked to evidence. It enables humans
and Seed-adjacent processes to carry assertions, questions, examples,
recommendations, tensions, findings, constraints, and command-like expressions
across time and artifacts.

Language alone does not determine:

- whether the text is true;
- whether the text is authoritative;
- whether the text is a request;
- whether the text is a command;
- whether the text is current;
- whether the text should be executed;
- whether the text has been accepted into architecture;
- whether the text is evidence, finding, frontier pressure, example, or handoff.

Multiple repository artifacts can contain language while serving different
architectural roles. A reconciliation may contain decision-provenance language.
A frontier may contain unresolved pressure. An observation may contain scoped
findings about what was seen. An audit may contain recommendations. A README may
route. A status document may own currentness. A code comment may explain local
implementation intent. The medium is shared; the role is not.

### Finding

Prose itself does not imply intent or authority. Intent and authority are
contextual claims that require evidence about source, channel, document role,
authority scope, and acceptance boundary.

## Part 2: Documentation As Source

When documentation becomes input, repository evidence supports treating it as an
observed artifact before treating it as architecture, truth, request, or command.
Documentation can be:

- observed as a repository artifact;
- cited as source evidence for what the repository says;
- interpreted into documentation claims, findings, tensions, rejected concepts,
  frontiers, or ownership claims;
- compared against implementation or other documents;
- routed to owning documents when navigation conventions require it;
- accepted, rejected, superseded, scoped, or preserved according to existing
  documentation authority and lifecycle boundaries.

Documentation observation does not automatically promote every sentence to
current architectural truth. Documentation authority reconciliation separates
navigation, orientation, canonical architecture, scoped reconciliation,
characterization, audit, preservation, roadmap, status, and frontier roles. That
separation is the strongest repository safeguard against collapsing all prose
into one authority plane.

### Documentation input path supported by evidence

```text
documentation artifact
    -> repository/documentation observation
    -> documentation claim or finding candidate
    -> support, comparison, routing, preservation, or scoped acceptance
```

This path is intentionally different from:

```text
documentation artifact
    -> executable command
```

The second path is not justified by the reviewed evidence.

## Part 3: Operator Language

Operator language is distinguished by communicative-act context. Existing
natural-language reconciliation treats language as an observation of words
provided by a speaker, document, transcript, or interface, with source, time,
channel, attribution, scope, and uncertainty. Operator language is stronger than
generic prose for request analysis because it is situated in an operator-facing
interaction where the operator may be asking, constraining, forbidding,
prioritizing, or authorizing something.

A communicative act is not merely a sentence with imperative grammar. It depends
on evidence that a participant produced language in a context where the language
is addressed to Seed or an adjacent interface. What survives interpretation is
not hidden intent as truth; what survives is an inspectable candidate: request
candidate, question candidate, goal hypothesis, constraint candidate,
command-like candidate, claim, priority, ambiguity, or routing pressure.

Operator language creates request candidates when source context and language
content together support that the operator appears to be asking for something.
It creates routing pressure when candidate meaning points toward a knowledge
query, clarification, documentation route, capability need, refusal boundary,
execution boundary, or human review.

### Finding

Operator language can be highly authoritative about what the operator requested,
forbade, or prioritized. It is not, by itself, authoritative about external
environmental truth, capability existence, safe execution, or architecture.

## Part 4: Authority

Repository evidence separates authority by domain.

Documentation can authorize architectural claims only within its scoped
documentation authority. For example, a status document owns current status and
active frontier; a reconciliation owns scoped decision provenance; an audit owns
what it observed in its audit scope; a README routes. Documentation cannot, by
that fact alone, authorize runtime execution, create capability authority, or
override implementation evidence outside its scope.

Operator language can authorize or constrain some operator-facing action only
when the operator channel, role, scope, and existing authority boundary support
that reading. It cannot create environmental truth. `nginx is down` may support
that the operator asserted or believed nginx was down; it does not verify nginx
health. `Do not restart anything` may create a strong constraint candidate in an
operator context; it does not become a global policy ontology by mere wording.

Capability authority and execution boundaries remain separate. A request-shaped
utterance or instruction-like document section can create a candidate need or
routing pressure, but execution requires the repository's existing capability,
policy, safety, approval, and authority boundaries. Documentation prose does not
supply those boundaries by itself.

### Authority findings

- Documentation may authorize claims only within scoped documentation authority.
- Documentation may influence action by preserving accepted findings, frontiers,
  constraints, or routes, but influence is not execution authority.
- Operator language may authorize or constrain a requested interaction when the
  operator context supports it.
- Operator language does not create environmental truth.
- Repository prose does not become command authority merely by using imperative,
  required, recommended, or future-work wording.

## Part 5: Instruction-Like Language

Repository artifacts often contain instruction-like language:

- future work sections;
- implementation suggestions;
- audit recommendations;
- example commands;
- required behavior blocks;
- prompt text;
- handoff text.

The role of such language depends on source context and acceptance boundary.
Future-work sections usually preserve unresolved or deferred work. Implementation
suggestions may be recommendations or rationale, not decisions. Audit
recommendations are scoped findings unless later accepted. Example commands are
illustrations or reproducibility aids unless invoked in an execution context.
Prompt text may be an operator communicative act when supplied through the
operator interface for the current task. Handoff text may preserve continuation
alignment, but handoff availability, consumption, activation, and compliance are
separate from architectural authority.

### Transition boundary

Instruction-like language remains documentation when it is preserved inside a
repository artifact as claim, example, recommendation, rationale, frontier
pressure, historical instruction, or handoff content without a current accepted
operator/action context.

It becomes executable authority only if separate repository-supported evidence
establishes an execution-relevant context: current operator act, adequate
authority, accepted scope, available capability, policy/safety clearance, and a
boundary that permits execution. Reviewed repository evidence requires those
separations; it does not support executing prose because it looks imperative.

## Strongest Similarities

- Both documentation prose and operator prose are language-bearing.
- Both can be observed with source, time, context, and attribution.
- Both can support claims about what was said or written.
- Both can contain assertions, questions, constraints, examples,
  recommendations, and command-like text.
- Both require interpretation before candidate meaning is promoted.
- Both can create pressure for routing, clarification, support review, or future
  investigation.

## Strongest Distinctions

- Documentation prose is artifact-situated; operator prose is
  communicative-act-situated.
- Documentation authority is scoped by document role and repository conventions;
  operator authority is scoped by operator channel, role, task context, and
  capability/execution boundaries.
- Documentation interpretation tends to produce documentation claims, findings,
  frontiers, lineage, preservation, or navigation routes; operator
  interpretation tends to produce request, question, goal, constraint, priority,
  or command-like candidates.
- Documentation can be current, historical, superseded, scoped, exploratory, or
  preservation-only; operator utterances are usually current to an interaction
  unless recorded later as evidence or handoff.
- Documentation may route readers to authorities; operator language may route a
  task to response, clarification, refusal, capability need, or execution review.

## Interpretation Findings

Interpretation is not verification. Reading prose can produce candidates, not
truth. The safest shared pattern is:

```text
language-bearing source
    -> observed text and provenance
    -> explicit interpretation with support and caveats
    -> candidate claim/request/frontier/finding/route
    -> scoped promotion or preservation
```

The strongest difference is what interpretation is trying to preserve.
Documentation interpretation preserves artifact meaning, claims, ownership,
frontier pressure, findings, and documentation routes. Operator interpretation
preserves communicative act meaning: what the operator appears to ask, claim,
forbid, prioritize, or constrain.

## Promotion Findings

Promotion is role-specific. Documentation claims may be promoted to current
architecture only through documentation authority, reconciliation, lifecycle, and
status boundaries. Repository observations may be promoted to artifact facts only
when supported by direct repository evidence. Language-derived claims may be
promoted only as claims about what was said, believed, requested, or implied
unless corroborated by other evidence. Request candidates may be promoted only
through operator/capability/execution boundaries.

The reviewed evidence supports a shared pre-acceptance preservation pattern, but
not a single shared architectural boundary for all pre-acceptance language.

## Routing Findings

Documentation routing asks: which document owns this answer, where should a
reader go, and what authority scope applies? Operator routing asks: what response
path, clarification, capability boundary, refusal boundary, or execution review
is implicated by this communicative act?

Frontier pressure can route future investigation without becoming an operator
request. A repository artifact can route a reader without requesting execution.
An operator request can route to documentation if the correct response is to
answer, cite, clarify, or refuse rather than act.

## Risks Of Conflation

- Treating every imperative sentence in documentation as a live command.
- Treating future work as approved implementation.
- Treating examples as requested actions.
- Treating audit recommendations as adopted decisions.
- Treating frontier pressure as operator intent.
- Treating operator assertions as environmental truth.
- Treating documentation authority as capability authority.
- Treating language interpretation as verification.
- Treating routing pressure as execution permission.
- Treating shared language medium as shared architectural boundary.

## Safeguards Already Present

The repository already contains several safeguards:

- documentation authority boundaries between navigation, status, roadmap,
  preservation, canonical architecture, audits, characterizations, frontiers, and
  reconciliations;
- observation/evidence/fact separation;
- claim support and evidence-strength distinctions;
- source authority and trust distinctions;
- natural-language observation versus intent derivation boundaries;
- candidate request preservation and routing/promotion boundaries;
- capability authority and execution boundary separation;
- operator authority boundaries;
- handoff availability/activation/compliance separation;
- repeated non-goals in frontier and observation documents that prevent
  exploratory prose from becoming schemas, runtimes, or governance.

## Required Tensions

| Tension | Reconciliation finding |
| --- | --- |
| language vs intent | Language carries possible intent evidence, but intent is an interpreted, attributed candidate, not a property of prose alone. |
| language vs authority | Language can express authority claims, but authority comes from source context and accepted scope. |
| documentation vs instruction | Documentation may contain instruction-like text without becoming a live instruction. |
| instruction vs execution | Execution requires separate authority, capability, policy, and action boundaries. |
| claim vs command | Claims assert or preserve propositions; commands request or direct action in a communicative-act context. |
| example vs request | Examples illustrate or preserve reproducibility unless separately invoked as current requests. |
| frontier pressure vs operator request | Frontier pressure preserves unresolved architectural questions; operator requests are current communicative acts. |
| documentation interpretation vs language routing | Documentation interpretation routes claims to owning artifacts; operator language routing routes candidate acts to response/capability paths. |
| repository artifact vs communicative act | Repository artifacts are persisted sources; communicative acts are situated interactions, even when later preserved as artifacts. |

## Unresolved Tensions

- Some handoff, prompt, and required-behavior artifacts can be both preserved
  documentation and current operator context depending on how they are supplied.
  The repository evidence supports separating availability, consumption,
  activation, and compliance, but this reconciliation does not settle all
  borderline cases.
- Documentation can influence future action without executing itself. The exact
  future intake mechanics remain outside this reconciliation.
- Repository prose may contain embedded quoted operator language. The quote is a
  documentation artifact in one context and evidence of a prior communicative act
  in another; attribution and source boundaries must carry the distinction.
- Frontiers can contain strong pressure and recommendations. Existing evidence
  says they are not implementation-ready by default, but later reconciliation may
  promote specific findings.
- Current task prompts may include blocks that look like documentation. In the
  current operator interaction they are operator language; if committed into the
  repository later, they become artifact evidence with a different role.

## Final Conclusion

Seed should understand language-bearing repository artifacts without collapsing
language into intent, authority, or execution. The best-supported answer is:

```text
prose role is determined by source context + artifact role + authority scope +
observation boundary + interpretation boundary + promotion boundary + routing
boundary + execution authority
```

Documentation prose and operator prose overlap as language observations and as
sources for interpreted candidates. They diverge at communicative-act context,
authority origin, promotion path, routing target, and execution relevance.

The repository evidence therefore supports neither:

```text
documentation should execute
```

nor:

```text
documentation can never influence action
```

The reconciled position is narrower: documentation can be observed, cited,
interpreted, routed, preserved, and sometimes promoted within scoped repository
authority. Operator language can create request and routing candidates within an
operator context. Execution authority remains a separate boundary.
