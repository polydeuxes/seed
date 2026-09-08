---
doc_type: observation
status: exploratory
domain: descriptive language vs authority
related:
  - descriptive_vs_architectural_vocabulary_observation.md
  - defines_authority_reconciliation_observation.md
  - relationship_fact_reconciliation.md
  - behavior_claim_reconciliation.md
  - boundary_claim_reconciliation.md
  - claim_support_frontier.md
  - operator_pressure_as_evidence_observation.md
  - visibility_target_ownership_concern_reconciliation.md
  - measurement_ownership_boundary_audit.md
  - unresolvedness_observation.md
  - inquiry_as_bridge_observation.md
---

# Descriptive Language Vs Authority Observation

## Status

Exploratory observation only.

This document investigates an emerging pattern appearing across unrelated
repository branches:

```text
descriptive language
    !=
architectural authority
```

and:

```text
shared vocabulary
    !=
shared authority
```

It does not modify implementation, relationship catalogs, Inquiry Orientation,
State Summary, graph validation, ontology, runtime concepts, or policy. It does
not recommend renaming relationships, promoting inquiry, promoting
unresolvedness, adding authority objects, or restricting descriptive language.
Repository authority remains with the more-specific architecture, implementation,
tests, catalogs, and reconciliation documents in their own scopes.

## Question

Central questions:

```text
What distinguishes descriptive language from repository authority?

What causes language to remain explanatory?

What causes language to become authoritative?

How does the repository currently cross that boundary?
```

The question may not have one answer. The apparent pattern may be a temporary
artifact of recent branches, a documentation habit, or a set of independent
implementation-specific distinctions rather than a single repository principle.

## Repository evidence reviewed

Materials reviewed or sampled for this observation include:

- `docs/archive/original_book_of_seed/13-knowledge-and-evidence.md`
- `docs/archive/original_book_of_seed/03-runtime-loop.md`
- `docs/archive/original_book_of_seed/04-toolkit-system.md`
- `docs/descriptive_vs_architectural_vocabulary_observation.md`
- `docs/role_of_descriptive_vocabulary_observation.md`
- `docs/defines_authority_reconciliation_observation.md`
- `docs/defines_relationship_reconciliation_audit.md`
- `docs/relationship_fact_reconciliation.md`
- `docs/behavior_claim_reconciliation.md`
- `docs/boundary_claim_reconciliation.md`
- `docs/claim_support_frontier.md`
- `docs/claim_support_characterization.md`
- `docs/evidence_strength_and_claim_strength_reconciliation.md`
- `docs/evidence_trust_and_source_authority_reconciliation.md`
- `docs/reality_fact_and_claim_reconciliation.md`
- `docs/visibility_target_ownership_concern_reconciliation.md`
- `docs/measurement_ownership_boundary_audit.md`
- `docs/operator_pressure_as_evidence_observation.md`
- `docs/inquiry_as_bridge_observation.md`
- `docs/inquiry_as_movement_observation.md`
- `docs/unresolvedness_observation.md`
- `docs/lens_orientation_and_dashboard_observation.md`
- `docs/active_edge_frontier.md`
- `docs/inquiry_frontier.md`
- `docs/source_navigation_surface_reconciliation.md`
- `docs/source_navigation_entity_typing_graph_issue_audit.md`

Search terms included `observation`, `claim`, `evidence`, `support`,
`relationship fact`, `behavior claim`, `visibility`, `ownership`, `candidate`,
`fact`, `ambiguity`, `truth`, `inquiry`, `unresolvedness`, `defines`, `source
navigation`, `current work position`, `active edge`, and `orientation`.

## Description vs authority investigation

The repository appears to allow language to do at least two different jobs.

First, language can be descriptive. Descriptive language helps a participant
notice, preserve, compare, or explain a pattern. It may organize scattered
evidence into a readable observation, name pressure before the pressure has been
reconciled, or preserve uncertainty for later work. In this role, language can be
useful without becoming a runtime object, ontology node, relationship catalog
entry, projected State component, policy rule, or graph-validation requirement.

Second, language can be authoritative. Authority appears when a term participates
in repository-governed behavior or evidence rules. Examples include fact
projection from evidence, relationship facts, claim-support rules, catalog
entries, source-navigation rows, validation findings, decision routing, event
append behavior, and State projections. In these cases the repository does not
only use a word to explain something; it gives the word consequences inside a
specific evidence or architecture surface.

A candidate distinction therefore appears:

```text
Descriptive language explains how to read evidence.

Repository authority determines what evidence may govern.
```

This is only a candidate distinction. It may be too broad. Some documents carry
limited documentary authority while explicitly refusing implementation authority.
Some implementation terms also remain partly descriptive outside their exact
scope. The repository evidence supports scoped authority more strongly than a
binary category.

## Historical distinction inventory

The reviewed branches repeatedly separate nearby ideas that can sound similar in
ordinary language:

| Distinction | Candidate reading from repository evidence |
| --- | --- |
| `measurement != ownership` | Endpoint or fact-subject measurements do not silently prove host/resource ownership. |
| `visibility != ownership` | Something can be visible, concerning, or operationally important without an ownership model. |
| `candidate != fact` | Candidate generated or interpreted material is not trusted fact until validation/support rules authorize it. |
| `ambiguity != truth` | Ambiguous or competing representations remain visible instead of becoming a single truth judgment. |
| `observation != reality` | Observation and evidence represent reality; they do not create reality. |
| `evidence != claim support` | Evidence supports facts; facts can then support claims through a separate comparison relationship. |
| `behavior != boundary` | An observed call or route does not by itself prove a required boundary. |
| `boundary != ownership` | A constraint or separation does not by itself prove ownership authority. |
| `declaration != concept definition` | Source declarations and documentation concept definitions can share `defines` spelling while carrying different authorities. |
| `inquiry language != Inquiry Orientation change` | Inquiry can describe movement, gaps, or preservation without changing the implemented Inquiry Orientation surface. |
| `unresolvedness language != State component` | Unresolvedness can preserve incompletion without becoming projected State. |

These examples do not prove one general rule. They do suggest that recent
repository work often resists promoting ordinary-language similarity into shared
architectural authority.

## Authority investigation

Repository evidence appears to require more than helpful language before
something becomes authoritative.

### Fact

The knowledge architecture describes a pipeline in which observations become
evidence, evidence can be transformed into facts, and facts are projected
interpretations with provenance, confidence, source type, recency, and support.
An operational observation is therefore not automatically permanent truth. It
must pass through evidence preservation and fact extraction or projection rules.

### Relationship

Relationship authority appears when observed connections between artifacts or
concepts are represented as relationship evidence. `RelationshipFact` is used in
prior reconciliation to distinguish connections from mere artifact existence.
That authority is still scoped: an observed relationship may support behavior,
but it does not automatically support boundary, exclusivity, ownership, or
policy-level conclusions.

### Claim and supported claim

Claim-support work separates the claim from the fact and from the support
relationship. A statement such as an ownership claim may need artifact facts,
relationship facts, constraints, scope, and absence of competing evidence before
it is supported. The support relation is neither the fact itself nor truth
itself; it is a comparison between represented evidence and the claim under a
rule.

### Validated structure and catalog entry

Validation and catalogs add authority by declaring accepted shapes, endpoints,
types, and warnings. The `defines` branch is instructive because one catalog
shape currently authorizes `document -> concept`, while source extraction emits a
separate module/symbol declaration shape for navigation. Same spelling did not
mean the catalog had already authorized every endpoint family.

### Projected State component

State components appear authoritative when events, evidence, facts, support,
conflicts, graph issues, or summaries are explicitly projected and queried.
Observation documents about inquiry or unresolvedness do not, by themselves,
create these projections. The repository preserves a difference between a
helpful explanatory model and a projected read model.

## Concepts that remain explanatory

The inquiry and unresolvedness branches show the other side of the boundary.
They preserve language such as movement, gap, pressure, unresolvedness, bridge,
and orientation-adjacent framing. That language helps explain why work can
continue, why a branch remains open, or why a future participant may need
context. The documents repeatedly decline ontology, runtime, schema, policy, and
State-promotion claims.

This suggests a candidate pattern:

```text
Language remains explanatory when it clarifies a reading of existing surfaces
without adding new evidence obligations, validation behavior, projection fields,
execution paths, catalog shapes, or ownership claims.
```

Explanatory status is not failure. It may be the correct repository status for a
term whose job is to preserve uncertainty, human understanding, or investigation
continuity.

## Pressure and authority

Several branches begin with pressure:

```text
operator pain
warning pressure
inquiry pressure
visibility pressure
```

The reviewed evidence suggests pressure often precedes authority clarification,
but does not itself settle authority. Operator pain can identify a real boundary
in use without diagnosing the implementation cause. Warning pressure around
`defines` can reveal unresolved relationship meaning without proving that a
single endpoint-type fix is sufficient. Visibility pressure can show operational
concern without proving ownership. Inquiry pressure can show a gap or movement
without requiring promotion of inquiry or unresolvedness.

Candidate observation:

```text
Pressure often reveals that meaning is unresolved before it reveals which
implementation should change.
```

This remains a candidate only. Some pressure may be ordinary defect pressure.
Some may be performance pressure. Some may be documentation confusion. The
repository evidence does not support treating all pressure as authority pressure.

## Defines authority example

The recent `defines` reconciliation is the clearest worked example of:

```text
shared vocabulary
    !=
shared authority
```

At least four authority families appear under or near `defines` language:

1. documentation front matter can say a document defines a concept;
2. Python source extraction can say a module-like source identity defines a
   dotted top-level symbol;
3. documentation prose can make a narrow existence-family `X defines Y` claim;
4. documentation prose can make a structure-family `X defines method Y` claim.

These families look similar in English. Repository evidence gives them different
sources, endpoints, support rules, and non-goals. A document/concept metadata
relationship is not a source declaration. A source declaration is not behavior,
runtime reachability, ownership, or concept formation. A prose claim is not the
same thing as a graph relationship fact. A structure claim is stronger than a
broad existence claim but still does not prove behavior.

Candidate finding:

```text
Shared spelling can be safe when authority remains scoped by source, endpoint,
support rule, and non-goal.
```

The warning pressure around `defines` therefore appears to come partly from
unresolved relationship meaning, not only from missing endpoint types. This does
not prove that relationship names should change. It only records that shared
vocabulary needs scoped authority to remain safe.

## Inquiry/unresolvedness example

The inquiry and unresolvedness investigations show the parallel pattern:

```text
helpful explanatory language
    !=
architectural promotion
```

Inquiry has been useful for describing question, gap, tension, pressure,
movement, bridge, continuation, and preserved investigation context.
Unresolvedness has been useful for describing unfinished understanding, unsettled
authority, missing comparison, and incomplete continuation position. The
reviewed documents treat these as exploratory framings rather than implemented
repository objects.

Candidate finding:

```text
A term can be worth preserving because it helps future readers continue an
investigation, even when the repository lacks evidence to make it a primitive.
```

This is especially important because forcing inquiry or unresolvedness into
architecture would risk replacing existing authorities: observations, evidence,
facts, claims, support, handoff context, current work position, active edge,
frontiers, and projection surfaces.

## Alternative explanations

The repository also supports alternatives.

### No general pattern exists

The examples may be unrelated. Measurement ownership, `defines`, inquiry, and
claim support may each have local reasons for preserving distinctions.

### Each branch is independent

Different branches may have independently rediscovered ordinary scoping hygiene.
The repeated shape may not be architecturally significant.

### Authority distinctions are implementation-specific

Some distinctions may arise only because current code lacks fields, catalog
shapes, or projection support. Future implementation could change the boundary
without proving a broader principle.

### Descriptive language and authority are already adequately separated

The repository already uses status blocks, non-goals, catalogs, tests, and
implementation boundaries. The observed pressure may only reflect branch-local
cleanup rather than a need for new analysis.

### Pressure is unrelated to authority clarification

Pressure may indicate performance problems, warning bugs, missing tests, or user
experience problems. Authority clarification may be incidental.

### Shared vocabulary may be acceptable with no broader theory

The `defines` example may need only scoped documentation and perhaps endpoint
reconciliation. It does not require a repository-wide theory of shared language.

## Uncertainties

Open uncertainties:

- Whether descriptive/authoritative is a real distinction or merely a useful
  reading lens.
- Whether repeated `X != Y` patterns indicate repository philosophy or normal
  engineering caution.
- Whether some currently descriptive terms, especially orientation-adjacent
  terms, are moving toward stronger authority.
- Whether pressure usually precedes authority clarification or only sometimes
  does.
- Whether shared vocabulary remains safe long-term without catalog or UI
  affordances that expose scoped authority.
- Whether future graph validation or source navigation needs more endpoint-family
  awareness for `defines`, without changing the relationship vocabulary itself.

## Non-conclusions

This observation does not conclude that:

- description and authority are formal repository concepts;
- a new authority framework should be added;
- authority should become ontology;
- descriptive language should be restricted;
- relationships should be renamed;
- inquiry should be promoted;
- unresolvedness should be promoted;
- pressure should automatically create implementation priority;
- every shared vocabulary term requires separate relationship names;
- every explanatory term should eventually become architecture.

The safest current reading is narrower:

```text
The repository repeatedly benefits from preserving a distinction between words
that help explain evidence and evidence structures that are allowed to govern
repository behavior.
```

That reading remains exploratory.
