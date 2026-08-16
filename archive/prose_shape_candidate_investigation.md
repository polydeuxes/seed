# Prose Shape Candidate Investigation

## Purpose and boundary

This investigation asks whether prose-derived useful terms can be treated as
shape candidates rather than ontology candidates.

This is investigation only. It does not implement prose ingestion, NLP, LLM
analysis, ontology expansion, inquiry graphs, shape graphs, promotion workflows,
or automation.

Repository authority remains with implementation-backed surfaces, tests,
diagnostics, scoped reconciliation documents, and the existing language/prose
boundary work.

## Evidence reviewed

Primary documents reviewed:

- `docs/descriptive_language_vs_authority_observation.md`
- `docs/documentation_prose_as_language_bearing_source_reconciliation.md`
- `docs/language_candidate_routing_and_promotion_reconciliation.md`
- `docs/natural_language_execution_path_inventory_audit.md`
- `docs/natural_language_observation_and_intent_derivation_reconciliation.md`
- `docs/natural_language_request_routing_audit.md`
- `docs/repository_observation_language_boundary.md`
- `docs/state_vs_identity_investigation.md`
- `docs/justified_equivalence_investigation.md`
- `docs/preservation_vs_continuation_investigation.md`
- `docs/preservation_relationships_investigation.md`
- `docs/repository_visible_inquiry_state_investigation.md`
- `docs/inquiry_artifact_strengthening_investigation.md`

Related evidence was sampled where these documents referred to documentation
authority, observation, claim support, relationship facts, source navigation,
implementation-backed diagnostics, inquiry artifacts, and boundary preservation.

## Central finding

Repository evidence supports a cautious distinction:

```text
ontology candidate
    -> possible repository thing, role, entity, fact type, relationship type,
       or governed object that would need authority before becoming repository
       knowledge or behavior

shape candidate
    -> recurring structure, relation, contrast, evidence pattern, or reasoning
       form observed across domains without claiming that the vocabulary names a
       repository entity
```

The distinction is supported only if shape candidates remain evidence-scoped and
non-promoted. A shape candidate may help humans compare evidence, explain why a
term recurs, or preserve a pattern for later inquiry. It is not thereby a new
ontology object, runtime type, graph node, fact projection, relationship catalog
entry, diagnostic surface, or State component.

The strongest supported safe path is:

```text
prose
    -> observed language-bearing artifact
    -> attributed claim / finding / question / pressure / candidate meaning
    -> recurring shape candidate when multiple evidence surfaces show the same
       structure
    -> cross-domain shape only as a scoped human-supported observation
```

The reviewed evidence does not support:

```text
prose
    -> ontology
```

by default.

## Language/prose evidence

### Prose is language-bearing material, not authority by form

The documentation-prose reconciliation directly supports the boundary that prose
is language-bearing material whose architectural role depends on source context,
document role, authority scope, observation boundary, interpretation boundary,
promotion rules, routing rules, and execution authority. It explicitly rejects
treating language content as equivalent to an operator communicative act or
instruction-like wording as executable instruction by default.

That matters for shapes because prose can carry useful repeated language without
that language being authoritative. A repeated term in documents can be observed,
cited, interpreted, compared, or preserved, but its role still depends on the
artifact and authority path.

### Documentation can become evidence without becoming truth

The same reconciliation supports a documentation input path:

```text
documentation artifact
    -> repository/documentation observation
    -> documentation claim or finding candidate
    -> support, comparison, routing, preservation, or scoped acceptance
```

This path is compatible with shape candidates. A prose-derived shape candidate
can accumulate as an observed candidate pattern while remaining separate from
current architecture, current fact, command, or accepted ontology.

### Candidate handling already separates interpretation from promotion

The language-candidate reconciliation gives the strongest precedent for a safe
candidate layer. It separates source observation, interpretation, routing, and
promotion. It also states that candidates may exist before promotion and that
routing is not authority or promotion.

This supports a shape-candidate layer only as an analogy, not as an implemented
feature. The evidence supports preserving candidate structures separately from
promoted structures and preserving non-promotion reasons. It does not support
creating a new shape registry, shape graph, or automatic promotion path.

### Natural language routing does not make language execution

The natural-language request routing and execution-path audit work supports the
same boundary from the operational side: request-like or command-like language
can be routed and inspected without becoming execution by form alone. This
matters because shape-like language should not acquire operational consequences
merely because it looks structured.

### Repository-observation language remains bounded

The repository-observation language boundary work supports treating repository
language as observation before treating it as repository knowledge. A document can
bear words, claims, headings, examples, and findings while still requiring source
role, evidence strength, support, and authority before those words become
architecture.

## Ontology candidate evidence

A term behaves more like an ontology candidate when repository evidence suggests
it may need to become a governed repository object or relationship with
consequences.

Indicators include:

- implementation-backed exposure;
- diagnostic or CLI visibility;
- validation or audit obligations;
- fact extraction or projection behavior;
- relationship catalog or schema implications;
- identity, subject, scope, or ownership consequences;
- event-ledger or State projection consequences;
- tests that encode the behavior;
- support rules that distinguish accepted facts from candidate claims.

Examples from existing evidence:

- `unknown` and `boundary` are not merely prose labels in several investigations;
  they recur in implementation-backed surfaces and diagnostics and are among the
  strongest repository-visible inquiry-state concepts.
- Endpoint identity is ontology-like where host:port subjects, scrape targets,
  source navigation, or fact attachment rules change what the repository may
  claim about hosts, endpoints, and measurements.
- `alias_of` is ontology-like because the justified-equivalence investigation
  treats it as identity equivalence and therefore reserves it for strong positive
  equivalence evidence.
- Command, goal, question, claim, and constraint candidates become ontology-like
  only if promoted through their target authority boundaries into structured
  work, accepted goals, supported claims, or executable requests.

An ontology candidate therefore tends to ask:

```text
Should this become a repository-governed thing, relation, type, fact, state,
operation, or authority-bearing object?
```

## Shape candidate evidence

A term behaves more like a shape candidate when repository evidence shows a
recurring structure without requiring the vocabulary to name a repository entity.

Indicators include:

- recurrence across unrelated domains;
- usefulness for comparing evidence;
- a stable contrast or relation form;
- applicability to multiple entity types without collapsing them;
- no direct implementation, schema, diagnostic, catalog, projection, or execution
  consequence;
- explicit refusal to promote the language;
- evidence that the same structure can be described with different local
  vocabulary;
- value as a human-readable explanatory pattern.

The recent recurring terms fit this unevenly.

### Preservation

`preservation` behaves strongly like a shape candidate. Preservation
investigations repeatedly describe a structure:

```text
surface or boundary
    declines unsupported change
    preserves visible state
```

The repository evidence for preservation is stronger than for causation,
transformation, production, or lineage, but the documents still do not make
preservation a first-class implemented relationship. Preservation is therefore a
recurring relationship shape, not currently an ontology type.

### Continuation

`continuation` behaves more weakly as a shape candidate. It requires at least two
positions in time and enough evidence to justify identity across time. The
repository has continuation-like handoffs and projection continuity, but the
evidence is weaker than preservation. Continuation is useful as a temporal shape,
but promoting it would risk unsupported lineage or identity claims.

### State and identity

`state` and `identity` are a contrast shape before they are ontology. The
state-versus-identity investigation supports:

```text
state
    -> current condition

identity
    -> sameness across observations
```

The evidence for state is stronger than evidence for identity. This distinction
is shape-like because it recurs across host, endpoint, storage, capability,
inquiry, and projection cases. It becomes ontology-like only where a specific
surface must preserve identity, attach facts, or prevent entity collapse.

### Equivalence

`equivalence` is mixed. As a general idea, it is a shape candidate: many domains
ask whether two observations are the same thing. But `alias_of` is ontology-like
because it has identity-equivalence consequences. The justified-equivalence work
therefore supports a counterexample: a term can begin as a recurring shape but
contain a narrower ontology-bearing relation that must be reserved for strong
evidence.

### Boundary

`boundary` is mixed and is the strongest counterexample to a simple
shape-only reading. It is a recurring structure across authority, mutation,
read-only, classification, source, command, and observation domains. But it is
also implementation-backed in several surfaces and repeatedly described as one
of the strongest repository-visible inquiry-state concepts. `boundary` can name
a shape in comparative prose, but particular boundaries may also be ontology-like
or operationally authoritative.

### Unknown

`unknown` is also mixed. It often participates in a preservation shape:

```text
boundary
    -> limitation
    -> unknown remains unknown
```

However, unknown states are repeatedly repository-visible and sometimes
diagnostic-backed. `unknown` therefore cannot be treated as merely prose-derived
shape vocabulary. It may be a state value, diagnostic finding, classification
state, or preserved limitation depending on the surface.

## Distinguishing ontology candidate from shape candidate

The evidence supports a gradient, not a binary.

| Question | More ontology-like | More shape-like |
| --- | --- | --- |
| What is being claimed? | A repository thing, fact, type, relation, command, state, or owner exists. | A recurring structure appears across evidence. |
| What changes if accepted? | Validation, projection, identity, fact attachment, relationship catalog, CLI behavior, or execution boundary changes. | Human explanation, comparison, or investigation framing improves. |
| What evidence is required? | Source authority, support rules, identity/scope, tests or implementation evidence where operational. | Repeated occurrences, scoped citations, counterexamples, and non-promotion reasons. |
| What is the main risk? | Unsupported repository truth or behavior. | Endless vocabulary expansion or disguised ontology promotion. |
| Safe status before authority? | Candidate-only, unpromoted. | Candidate shape, observed pattern, scoped investigation finding. |

Candidate distinction:

```text
ontology candidate
    -> asks whether the repository should claim or govern something

shape candidate
    -> asks whether repeated evidence has the same structure without claiming a
       new governed thing
```

This is supported, but only with two safeguards:

1. A shape candidate must preserve its evidence and non-promotion boundary.
2. A shape candidate must not silently create a new inventory obligation,
   projection field, relationship type, diagnostic, or ontology node.

## Can shape candidates accumulate evidence without ontology promotion?

Supported answer: yes, partially.

Repository evidence already supports several non-promoted accumulation patterns:

- documentation claims can be observed, cited, compared, and routed without every
  sentence becoming current architecture;
- language-derived candidates can be preserved separately from promoted
  structures;
- inquiry artifacts can be strengthened by visibility, relationship candidates,
  lineage candidates, attachment behavior, and repeated surfaces without prose
  ingestion;
- preservation can be investigated as a recurring pattern without becoming a
  first-class relationship model;
- state/identity/equivalence distinctions can be used to avoid collapse without
  implementing a general equivalence system.

Unsupported leap:

```text
shape evidence accumulates
    -> therefore Seed has or should have shape objects
```

The current repository supports human-readable accumulation in investigations,
audits, and reconciliations. It does not show an implemented shape-evidence
store, shape registry, or shape promotion mechanism.

## Could prose be approached as candidate shape rather than ontology?

Supported answer: yes, as a safer inquiry framing.

The safe framing is:

```text
prose
    -> observed artifact language
    -> attributed claim/finding/question/pressure/candidate meaning
    -> possible recurring shape
    -> scoped cross-domain observation if evidence recurs
```

This is safer than prose-to-ontology because it preserves the language boundary,
keeps authority contextual, and allows useful recurrence to be discussed without
creating repository entities.

However, the framing is safe only if shape remains a weak status. If every
recurring word becomes a named shape candidate, the framing merely renames prose
expansion.

## Counterexamples

### Looked like shape, but was really ontology-like

`alias_of` can look like an equivalence shape, but the justified-equivalence
investigation treats it as identity equivalence. Accepting `alias_of` collapses
boundaries and therefore requires strong positive evidence. The shape
"these may be the same" is safe; the ontology relation `alias_of` is not safe
without authority.

`boundary` can look like a broad shape, but specific operational boundaries may
control mutation, read-only behavior, diagnostic classification, command review,
or source authority. Those cases are ontology-like or operationally authoritative
because accepting the boundary changes what Seed may do or claim.

`unknown` can look like a preservation shape, but diagnostic and classification
surfaces can expose unknown as current state. In those contexts it is not only a
prose shape; it is repository-visible state.

### Looked like ontology, but behaved like shape

`preservation` can sound like a relationship type, but current investigations
keep it as a recurring static relationship family rather than a first-class
repository model. It helps explain evidence without adding a relationship
catalog entry.

`continuation` can sound like an inquiry or workflow object, but the evidence
keeps most continuation and movement human-interpreted. It behaves like a
temporal comparison shape unless and until specific continuity evidence exists.

`state versus identity` can sound like a domain model, but much of its current
value is as a distinction that prevents unsupported collapse across domains.

### Shape vocabulary could expand endlessly

The risk is real. Terms such as authority, lineage, transformation, evidence,
fact, claim, artifact, language, prose, observation, pressure, movement,
continuity, support, visibility, attachment, and routing can all be described as
recurring structures.

The repository evidence challenges endless expansion by requiring:

- source-specific authority;
- candidate/non-promotion boundaries;
- implementation-backed visibility for stronger claims;
- support and evidence rules before facts or claims become accepted;
- scoped document roles;
- counterexamples and unsupported conclusions;
- refusal to treat routing as authority;
- refusal to treat language as execution.

Therefore shape framing does not by itself solve expansion. It helps only if
Seed treats shapes as scoped observations with thresholds, not as an automatic
inventory of every useful abstraction.

## Important distinctions

### Ontology

A repository-governed vocabulary of things, relations, states, or authorities
with consequences for evidence, projection, identity, validation, behavior, or
claims.

### Shape

A recurring structure or relation form observed across evidence. A shape can be
useful without being a repository entity.

### Observation

An attributed encounter with an artifact, surface, output, source, or language.
Observation can support later interpretation but is not automatically truth.

### Evidence

Preserved support material with source, scope, confidence, provenance, or other
context sufficient to support a fact, claim, comparison, or finding under a rule.

### Fact

A supported or projected repository representation derived through evidence and
authority rules. Fact is stronger than observation or prose statement.

### Claim

A statement to evaluate against evidence. A claim can be candidate-only,
supported, unsupported, scoped, superseded, or disputed.

### Language

The medium through which prose, operator utterances, documentation, examples,
questions, instructions, and findings are expressed. Language alone does not
determine authority.

### Prose

Language-bearing artifact content. Prose can be evidence, claim source,
frontier pressure, observation material, or scoped authority depending on its
source and document role.

### Artifact

A repository-visible or document-visible unit that can carry evidence,
limitations, visibility state, findings, or relationships. Artifacts can be
strengthened without making all prose observable.

## Supported conclusions

1. Prose-derived useful terms can be treated as shape candidates rather than
   ontology candidates when they are used to describe recurring structures and
   are kept non-promoted.
2. Shape candidates can accumulate evidence in investigation prose, audits,
   reconciliations, and cited cross-domain comparisons without becoming ontology.
3. `preservation`, `continuation`, `state`, `identity`, and broad `equivalence`
   currently behave more like shape candidates than ontology expansions, though
   narrower implementations may be ontology-like.
4. `boundary` and `unknown` are mixed: they are recurring shapes, but they are
   also among the strongest repository-visible inquiry-state concepts and cannot
   be treated as prose-only vocabulary.
5. The safest prose path is candidate-shape framing, not prose-to-ontology.
6. Shape framing is not sufficient by itself; without thresholds and
   non-promotion boundaries it can rename endless prose expansion.

## Unsupported conclusions

- Seed has an implemented shape-candidate system.
- Seed should implement shape ingestion, shape graphs, or shape promotion.
- Every recurring prose term is a useful shape candidate.
- Shape candidates are ontology candidates under another name.
- Shape evidence automatically becomes a fact, claim, relationship, or State
  projection.
- `boundary` and `unknown` are merely prose-derived shapes.
- `alias_of` is a harmless equivalence shape.
- Prose recurrence alone establishes repository authority.

## Open questions

- What threshold distinguishes useful recurrence from vocabulary noise?
- Can a shape candidate remain useful if it never becomes implementation-backed?
- When a shape becomes operationally important, does it need a new authority
  boundary before it becomes ontology-like?
- Are there shape candidates with enough evidence to justify diagnostic
  visibility, or would that immediately convert them into operational surfaces?
- Can supported conclusions become more visible without becoming ontology?
- Is preservation the strongest shape candidate because it avoids temporal and
  identity claims?
- Are boundary and unknown bridges between shape and ontology, or merely terms
  that appear in both roles?

## Acceptance answers

### Can prose-derived useful terms be treated as shape candidates rather than ontology candidates?

Yes, when the term is used as a recurring evidence structure and remains
candidate-only. The repository already supports candidate preservation,
non-promotion, scoped authority, and documentation-as-observed-artifact paths.

### What distinguishes shape from ontology?

Shape describes a recurring structure. Ontology governs a repository thing,
relation, state, fact, authority, or behavior. The practical difference is
whether acceptance changes repository claims or operations.

### Can shape evidence accumulate without ontology promotion?

Yes, in human-readable investigations and reconciliations. The repository does
not currently demonstrate an implemented shape-evidence mechanism.

### Does shape framing make prose safer?

Yes, compared with prose-to-ontology, because it preserves candidate status and
requires authority before promotion.

### Does shape framing create an endless shape inventory?

It can. Shape framing avoids endless expansion only if recurring terms must show
cross-domain evidence, explicit usefulness, counterexamples, and preserved
non-promotion reasons before being treated as meaningful shape candidates.
