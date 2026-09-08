# Operator Interface And Projection Authority Reconciliation

## Purpose

This document performs a documentation-only reconciliation of operator
communication, projection authority, explainability, assertion communication,
and the role of projections versus interpretation layers.

It is an architectural boundary audit.

It does not implement code, modify schemas, modify projections, observations,
facts, relationships, trust behavior, authority behavior, LLM integrations, CLI
surfaces, APIs, or tests.

It does not introduce new runtime semantics.

## Central Question

Recent reconciliations established trust and authority boundaries,
corroboration and fact promotion boundaries, relationship promotion boundaries,
and claim strength and assertion semantics.

The remaining question is:

```text
How should Seed communicate what it knows to an operator?
```

The safest answer is:

```text
Seed should communicate knowledge through deterministic, inspectable projections
first. Interpretation layers and LLMs may reorganize or explain those
projections, but they must not become independent authority for claims.
```

## Central Finding

Projection is the primary knowledge interface.

A projection may communicate knowledge, uncertainty, support, contradiction,
provenance, current selection, and assertion semantics when those statements are
backed by preserved knowledge structures and deterministic projection rules.

An interpretation layer may make projections easier to understand, navigate,
summarize, translate, or onboard operators into. It may not silently add claims,
repair missing provenance, verify live reality, resolve contradictions, or make a
claim more authoritative than the evidence and projection permit.

An LLM is therefore optional and interpretive. It may explain or summarize
projections. It does not replace projections, evidence inspection, provenance,
or assertion semantics.

## Files Considered

This reconciliation builds on existing architectural documentation, especially:

- `docs/claim_strength_and_assertion_semantics_reconciliation.md`
- `docs/read_model_inventory_and_authority_reconciliation.md`
- `docs/view_authority_and_surface_responsibility_reconciliation.md`
- `docs/explainability_contract_characterization.md`
- `docs/explanation_contract_vocabulary.md`
- `docs/projection_integrity_drilldown_characterization.md`
- `docs/state_summary_authority_reconciliation.md`
- `docs/impact_overview_authority_reconciliation.md`
- `docs/operator_navigation_reconciliation.md`
- `docs/evidence_trust_and_source_authority_reconciliation.md`
- `docs/corroboration_and_fact_promotion_reconciliation.md`
- `docs/relationship_fact_reconciliation.md`

## Architectural Definitions

### Knowledge Storage

Knowledge storage is the durable preservation layer for events, observations,
evidence, facts, relationships, and related metadata.

It answers:

```text
What did Seed preserve?
```

Knowledge storage is not, by itself, the operator interface. It may contain more
history, provenance, duplicates, scopes, stale material, and intermediate
structures than a human-facing surface should show by default.

Knowledge storage must remain conservative. It preserves what was reported,
derived, normalized, or related; it does not become more true because a later
surface phrases it fluently.

### Projection

A projection is a deterministic read view over preserved knowledge structures.

It answers view-specific questions such as:

```text
What facts are currently visible?
Which value is selected under this view's rules?
Which support exists for this claim?
Which contradictions or integrity issues are visible?
Which relationships are represented?
Which provenance explains this view?
```

Projection is not raw storage. Projection selects, groups, filters, ranks,
aggregates, or presents preserved knowledge according to declared view
responsibility.

Projection is also not new observation, verification, or truth arbitration. It
communicates what the view is authorized to select from stored knowledge.

### Operator Interface

An operator interface is any human-facing surface through which an operator
learns, inspects, navigates, or acts on Seed knowledge.

It answers:

```text
What can an operator learn, inspect, or decide from this surface?
```

Examples include current fact views, fact support views, state summaries,
impact views, relationship views, entity type views, graph issue views,
contradiction views, generated reports, dashboards, CLI output, and LLM-mediated
responses when they are used to communicate Seed knowledge.

An operator interface may be implemented as a projection, an interpretation over
projections, a navigation surface, or a composed report. The defining property is
not implementation form; it is that the surface communicates knowledge to a
human operator.

### Interpretation Layer

An interpretation layer is a read-only communication layer that reorganizes,
summarizes, narrates, translates, explains, or routes operators through existing
projections and evidence.

It answers:

```text
How should this already-projected knowledge be understood by a human?
```

Interpretation may provide grouping, sectioning, prioritization, labels,
operator guidance, onboarding prose, cross-surface navigation, and natural
language.

Interpretation must preserve a path back to authoritative projections and
provenance. It must not become a hidden evidence source, verifier, policy engine,
planner, contradiction resolver, relationship promoter, fact promoter, or runtime
mutation path.

## Boundary Summary

| Layer | Primary question | Authority | Non-authority |
| --- | --- | --- | --- |
| Knowledge storage | What was preserved? | Preservation, provenance, normalized records | Human-oriented selection, current truth, fluent explanation |
| Projection | What does this view select or expose? | Deterministic communication of view-owned knowledge | New observation, runtime verification, unsupported conclusions |
| Operator interface | What can an operator learn or inspect here? | Human-facing communication within surface scope | Authority beyond its underlying projection/evidence |
| Interpretation layer | How can the operator understand or navigate projected knowledge? | Organization, explanation, summarization, translation | Claim authority, provenance invention, model-only truth |
| LLM-assisted communication | How can language help explain projections? | Optional interpretation and communication | Authoritative knowledge, required explainability, replacement for projections |

## Projection Authority

Projection authority is the right of a projection to communicate view-scoped
knowledge derived from preserved structures under deterministic rules.

It is not the right to declare universal truth.

Projection authority is bounded by:

```text
input knowledge
view responsibility
selection rules
freshness and temporal rules
cardinality rules
source and provenance boundaries
conflict and contradiction handling
projection time
```

### What A Projection May Communicate

A projection may communicate:

- visible claims;
- selected current interpretations;
- historical claims when the view owns historical reporting;
- supporting facts;
- supporting evidence;
- provenance;
- source types;
- observed, latest observed, expiry, and projection times;
- dimensions and scope;
- confidence or support signals when defined by the view;
- corroboration when defined by support rules;
- contradictions or conflicts when detected by the relevant view;
- relationship edges and relationship support;
- graph integrity issues;
- assertion semantics such as observed, supported, selected, current,
  historical, contradicted, unverified, or verified when the view has the data to
  justify those labels.

### What A Projection Must Not Communicate

A projection must not communicate:

- claims unsupported by preserved knowledge;
- invented provenance;
- hidden LLM rationale as evidence;
- live verification unless a verification record or verification view supports
  the statement;
- contradiction resolution unless the projection explicitly owns selection under
  deterministic rules;
- universal truth when it only has scoped evidence;
- current truth without an `as of` or projection boundary;
- relationship causality, ownership, dependency, or control beyond the supported
  relationship semantics;
- trust in a source as proof of the claim;
- presentation fluency as evidence strength.

### Can Projections Communicate Uncertainty?

Yes.

Uncertainty is operator-facing knowledge.

A projection may communicate uncertainty through:

- competing values;
- fact conflicts;
- contradictions;
- graph issues;
- unsupported facts;
- stale facts;
- expired facts;
- unverified claims;
- missing evidence;
- ambiguous relationship types;
- confidence or support differences;
- scoped caveats such as local versus remote, configured versus observed, or
  historical versus current.

Communicating uncertainty does not weaken projection authority. It is part of
projection authority when the uncertainty is grounded in preserved claims,
provenance, or deterministic integrity views.

### Can Projections Communicate Assertion Semantics?

Yes.

Assertion semantics are operator-facing concepts. Operators need to know whether
Seed is saying:

```text
observed
supported
corroborated
contradicted
selected
historical
current
verified
unverified
```

These labels must remain scoped and must not collapse into a single truth state.
For example, `selected` means selected by a projection. It does not mean
verified. `observed` means a source reported something. It does not mean current.
`contradicted` means competing support exists. It does not mean false.

## What Operators Should Learn From Projections Alone

Knowledge communication should not depend on natural-language generation or a
specific model.

An operator should be able to learn at least the following from projections
alone:

### Current State

The operator should be able to inspect what Seed currently projects for a claim,
entity, relationship, or domain, including the projection name and as-of context
when currentness is asserted.

### Support

The operator should be able to inspect which facts, evidence, observations,
sources, or support groups justify a projected claim.

### Contradictions And Conflicts

The operator should be able to see whether competing claims exist, which values
or facts are involved, and whether a selected value is merely selected rather
than verified.

### Relationships

The operator should be able to inspect represented relationships, their endpoints,
types, scope, and support without treating every edge as ownership, causality, or
runtime dependency.

### Provenance

The operator should be able to answer:

```text
Where did this claim come from?
Who or what reported it?
When was it observed?
Which event, evidence node, fact, or relationship supports it?
```

### Claim Semantics

The operator should be able to distinguish observed, supported, corroborated,
contradicted, selected, historical, current, verified, and unverified claims.

### Scope And Time

The operator should be able to see dimensions, vantage point, observed time,
latest observed time, expiry, freshness, projection time, and temporal caveats
when those affect claim meaning.

### Integrity And Missingness

The operator should be able to inspect graph issues, unsupported facts, stale
facts, unavailable support, unknown verification, and gaps without requiring an
LLM to infer what is missing.

## Minimum Explainability Requirements

A claim is minimally explainable when an operator can inspect:

1. the claim being communicated;
2. its assertion semantics;
3. its scope and dimensions;
4. its temporal context;
5. supporting facts;
6. supporting evidence;
7. provenance;
8. source type or source identity where available;
9. competing or contradictory claims;
10. selected-current rationale when a projection selected among alternatives;
11. verification method and verification time when the claim is described as
    verified;
12. caveats or missing support when the view cannot answer a stronger question.

This minimum does not require natural language. A structured projection can be
fully explainable if it exposes these fields and navigation paths.

Conversely, fluent prose is not explainability if it omits provenance, scope,
assertion semantics, or contradiction visibility.

## Relationship Between Projections And Explanations

Explanations are not a separate source of truth.

An explanation is a communication shape over claims, support, provenance,
selection, contradiction, and temporal context.

Depending on form, an explanation may be:

- a projection, when it is a deterministic read view such as fact support,
  evidence graph, contradiction inventory, why-fact, or graph issue output;
- an interpretation layer, when it narrates or summarizes one or more
  projections for operator understanding;
- a composed operator interface, when it combines projection output and
  interpretation with navigation links.

The architectural requirement is not that explanations live in one module. The
requirement is that explanations preserve authority boundaries.

### Example: `package installed`

For a claim such as:

```text
package openssh-server installed
```

An explainable projection or explanation should let the operator ask:

```text
Why?
Observed by whom?
Supported by what?
Current or historical?
Selected or merely preserved?
Verified or unverified?
Contradicted by anything?
Scoped to which host, package manager, source, and time?
```

A projection can answer these with structured fields. An interpretation layer can
turn the same answers into prose. The prose does not add authority.

## Assertion Semantics In Operator Communication

Operator-facing communication should use assertion terms deliberately.

### Observed

Communicate as:

```text
Source S reported claim C at time T from scope V.
```

Do not communicate as:

```text
C is true.
```

unless current truth is separately supported by projection or verification.

### Supported

Communicate as:

```text
Claim C has supporting evidence or facts E.
```

Do not communicate support as proof of every stronger phrasing of C.

### Corroborated

Communicate as:

```text
Multiple compatible support paths support scoped claim C.
```

Do not communicate corroboration as universal truth, current truth, or verified
truth unless those stronger assertions are independently justified.

### Contradicted

Communicate as:

```text
Claim C has competing or incompatible support under scope S.
```

Do not communicate contradicted as false.

### Selected

Communicate as:

```text
Projection P selected value V for claim C as of time T under rules R.
```

Do not communicate selected as verified.

### Historical

Communicate as:

```text
Claim C applied, was observed, or was represented for past time or interval T.
```

Do not erase historical claims merely because current projection selected a
newer state.

### Current

Communicate as:

```text
Projection P currently selects claim C as of projection time T, subject to
freshness and selection rules R.
```

Do not communicate current without projection, freshness, or as-of context.

### Verified

Communicate as:

```text
Verification method M confirmed scoped claim C at time T with evidence E.
```

Do not communicate verified as timeless, universal, or broader than the
verification method.

## Role Of An LLM

An LLM may be useful, but it is not required for Seed to communicate knowledge.

### LLM Is Not Authoritative

An LLM must not be treated as authoritative for Seed claims merely because it can
produce fluent explanations.

An LLM cannot replace:

- stored observations;
- evidence;
- facts;
- relationships;
- deterministic projections;
- provenance;
- verification records;
- contradiction inventories;
- graph integrity views;
- assertion semantics.

### LLM Is Explanatory And Interpretive

An LLM may help with:

- summarization of projection output;
- translation between technical and operator-friendly language;
- onboarding explanations;
- question answering over provided projection content;
- navigation suggestions among existing surfaces;
- planning assistance that explicitly cites the projections it relies on;
- claim explanation when constrained to existing support and provenance.

### LLM Is Optional

Seed's explainability should survive model replacement, model removal, provider
unavailability, or a change in natural-language interface.

A model can make communication easier. It must not be the only place where the
operator can inspect state, support, provenance, relationships, contradictions,
or graph integrity.

### LLM Responsibilities Versus Projection Responsibilities

| Responsibility | Projection | Interpretation / LLM |
| --- | --- | --- |
| Inspect current facts | Owns | May summarize |
| Inspect fact support | Owns | May explain in prose |
| Inspect provenance | Owns | May cite or paraphrase |
| Inspect contradictions | Owns | May contextualize |
| Inspect relationships | Owns | May group or narrate |
| Inspect graph issues | Owns | May prioritize for a human |
| Communicate assertion semantics | Owns labels and fields | Must preserve labels and caveats |
| Translate jargon | May not focus on this | Owns optional communication aid |
| Operator onboarding | Provides source surfaces | May guide and teach |
| Planning assistance | Provides knowledge inputs | May suggest plans, not authority |
| Verify live reality | Only if a verification projection exists | Must not invent verification |

## Operator Trust And Projection Authority

Operators should not trust all communication surfaces equally.

The trust hierarchy should follow evidence and authority, not fluency.

```text
preserved evidence and deterministic projections
        >
structured explanations over projections
        >
interpretive summaries with citations/navigation
        >
LLM-generated prose
        >
generated documentation that is not tied to current projections
```

This is not a statement that prose is useless. It is a statement that prose is
not evidence.

Operators may trust projections for what those projections are authorized to
communicate. They may trust explanations when the explanations are traceable back
to projections and provenance. They should treat LLM summaries and generated
documentation as convenience layers unless those summaries cite and preserve the
underlying projection authority.

## Can A Projection Be Wrong?

Yes, in several different senses.

A projection can be wrong if:

- its input knowledge is wrong, stale, incomplete, or mis-scoped;
- its deterministic rules select an undesirable or outdated interpretation;
- its view responsibility is ambiguous;
- it collapses distinct scopes into one claim;
- it overstates currentness;
- it hides contradiction or missing provenance;
- it presents a selected claim as verified;
- an operator misreads its authority.

A projection is therefore best understood as:

```text
an authoritative communication surface for a scoped read question
```

not as:

```text
a universal truth declaration
```

Projection authority means the projection owns its selection and communication
contract. It does not mean the selected claim is metaphysically true or live-
verified.

The implication is that projections must expose enough support, provenance,
assertion semantics, and uncertainty for operators to audit their conclusions.

## What Should Not Require An LLM

The following knowledge communication should remain available without an LLM or
other interpretation layer:

- state inspection;
- current facts;
- current observations;
- fact support;
- claim provenance;
- evidence graph inspection;
- relationship inspection;
- entity type inspection;
- graph integrity review;
- contradiction and conflict review;
- stale fact review;
- unsupported fact review;
- capability verification inventory;
- assertion-semantic labels;
- selection rationale where a projection selects among alternatives;
- verification status and verification evidence where available.

An LLM may help operators consume these surfaces. It must not be a prerequisite
for their existence, inspection, or authority.

## Non-Goals

This reconciliation does not:

- implement a new operator interface;
- add or modify CLI commands;
- add or modify APIs;
- add or modify schemas;
- add or modify projections;
- add or modify observations, facts, relationships, evidence, trust behavior, or
  authority behavior;
- add or modify LLM integrations;
- introduce generated-response behavior;
- require a natural-language interface;
- require a new explanation engine;
- require a new verification engine;
- require a new projection store;
- define new runtime semantics;
- recommend hiding existing evidence for readability;
- treat documentation prose as a replacement for projection output.

## Implementation Implications

This document does not recommend immediate implementation work.

It does clarify constraints for future work:

- Future operator interfaces should declare whether they are evidence,
  justification, integrity, navigation, interpretation, or composed surfaces.
- Future summaries should preserve navigation paths back to projections and
  provenance.
- Future LLM-assisted features should cite or reference projection content rather
  than inventing claim authority.
- Future natural-language responses should preserve assertion semantics such as
  observed, supported, selected, current, historical, contradicted, verified, and
  unverified.
- Future projection changes should be reviewed for whether they strengthen claim
  wording beyond support.
- Future explanation work should remain read-only unless separately reconciled.
- Future documentation should avoid implying that prose quality increases
  evidence strength.

## Architectural Invariants

This reconciliation supports the following invariants:

```text
Projection is the primary knowledge interface.
```

```text
Interpretation is not authority.
```

```text
LLMs explain projections; they do not replace projections.
```

```text
Knowledge communication should not depend on a specific model.
```

```text
Explainability should survive model replacement.
```

```text
Operators should be able to inspect claims directly.
```

```text
A projection should be sufficient to inspect current knowledge within its scope.
```

```text
Assertion semantics are operator-facing concepts.
```

```text
Explainability requires provenance.
```

```text
Authority follows evidence, not presentation quality.
```

```text
Uncertainty is knowledge and may be projected.
```

```text
Selected is not verified.
```

```text
Observed is not current unless currentness is separately supported.
```

```text
Contradicted is not false.
```

```text
Generated prose is a communication aid, not a source of truth.
```

## Conclusion

Seed should communicate knowledge to operators through deterministic,
inspectable projections first.

Projections are authoritative communication surfaces for scoped read questions:
they can communicate claims, support, relationships, provenance, uncertainty,
contradictions, current selection, historical context, and assertion semantics
when those statements are grounded in preserved knowledge and deterministic view
rules.

Interpretation layers, including LLM-assisted communication, remain valuable for
summarization, translation, onboarding, navigation, and operator-friendly
explanation. Their authority is derivative. They must preserve the path back to
projection output and provenance.

The architectural boundary is therefore:

```text
Seed may use interpretation to make knowledge understandable, but knowledge
authority remains with evidence-backed projections and their provenance.
```
