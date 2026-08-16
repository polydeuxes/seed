# Relationship Promotion Reconciliation

## Purpose

This document performs a documentation-only reconciliation of relationship
creation, relationship support, relationship corroboration, relationship
contradiction, relationship promotion, relationship confidence, and relationship
ownership boundaries.

It is an architectural boundary audit.

It does not implement code, modify schemas, modify relationship models, modify
projections, modify inference rules, modify graph validation, modify entity
typing, modify observations, modify facts, or modify tests.

It does not introduce new runtime semantics.

## Central Question

Recent reconciliations established identity derivation boundaries, Prometheus
observation boundaries, trust and source-authority boundaries, and corroboration
and fact-promotion boundaries. Relationship reconciliation exposed a related but
separate question:

```text
When does evidence justify a relationship?
```

This question is not identical to:

```text
When does evidence justify a fact?
```

A relationship is an edge between things or concepts. A fact is a normalized
claim. A projection is a read view over preserved state. If Seed collapses these
layers, it risks treating weak relationship evidence as behavior, treating
behavior as ownership, or treating selected views as preserved truth.

## Files Inspected

Required context inspected for this reconciliation:

- `docs/relationship_fact_reconciliation.md`
- `docs/relationship_observation_v0_reconciliation.md`
- `docs/corroboration_and_fact_promotion_reconciliation.md`
- `docs/fact_confidence_and_corroboration_reconciliation.md`
- `docs/evidence_trust_and_source_authority_reconciliation.md`
- `docs/contradiction_handling_audit.md`
- `docs/ownership_claim_reconciliation.md`

## Central Finding

The safest architectural answer is:

```text
Evidence may justify preserving a relationship before it justifies promoting,
selecting, or owning that relationship.
```

More compactly:

```text
Observations report.
Evidence supports.
Relationships normalize edges.
Facts normalize claims.
Projections select views.
Ownership assigns authority.
```

A relationship should be created when Seed has enough evidence to preserve an
edge-shaped claim with provenance. Relationship creation does not mean the edge
is corroborated, current, behaviorally meaningful, contradiction-free, selected
by a projection, or owned by either endpoint.

Relationship promotion should therefore mean:

```text
Seed has represented an evidence-backed edge as a relationship.
```

It should not mean:

```text
Seed proved the edge is true.
Seed selected the edge as current.
Seed inferred behavior from structure.
Seed inferred ownership from participation.
Seed resolved all contradictions.
Seed upgraded evidence into architectural authority.
```

## Conceptual Boundary Map

The five terms in this audit should remain distinct.

| Layer | Primary question | Preserves | Does not imply |
| --- | --- | --- | --- |
| Observation | What did a source report? | A source-attributed input statement or measurement. | Truth, normalization, corroboration, relationship existence, or current selection. |
| Evidence | Why may Seed consider this? | Provenance, payload, source, time, confidence hints, vantage point, and support material. | Source authority, independence, truth, or ownership. |
| Fact | What normalized claim is represented? | A normalized claim with supporting evidence. | Verified live reality or selected current state. |
| Relationship | What edge-shaped claim is represented? | A directed or typed connection with supporting evidence. | Behavior, ownership, boundary authority, or graph truth by itself. |
| Projection | What should this view show? | A deterministic selection, grouping, ranking, explanation, or summary over preserved state. | The only valid interpretation of preserved evidence. |

The most important boundary for this document is:

```text
Relationship ≠ Projection
```

A relationship can exist in preserved knowledge without being selected into a
current graph view. Conversely, a projection may display, rank, hide, summarize,
or annotate relationships without creating or destroying the preserved evidence
that justified them.

## Relationship Creation

Relationship creation is the act of representing an evidence-backed edge in
Seed's normalized knowledge model.

Conceptually, a relationship has at least:

```text
subject
relationship kind
object
scope or dimensions when available
supporting evidence
provenance
confidence/support signal
observed or derived time
freshness or validity metadata when applicable
```

Relationship creation is justified when the evidence answers all three minimum
edge questions:

```text
What is the source-side participant?
What kind of connection is being asserted?
What is the target-side participant or target concept?
```

For example, static import syntax can justify creation of an imports-style
relationship:

```text
subject = importing source artifact
relationship kind = imports
object = imported module or symbol target
```

That creation is intentionally weak. It preserves an observed edge. It does not
claim that the imported target is invoked, reached, executed, owned, or
architecturally authoritative.

Relationship creation should be allowed to happen from a single evidence item
when the relationship kind is itself weak enough for that evidence. For example,
one syntactic import declaration may justify one `imports` relationship. One
import declaration should not justify a `calls`, `routes`, `stores`, `emits`,
`validates`, or `owns` relationship.

## Relationship Support

Relationship support is the set of evidence items that explain why a
relationship is available for consideration.

Support should answer:

```text
Which evidence backs this edge?
What did each source actually show?
What relationship kind can that evidence safely support?
What scope, time, source path, vantage point, or dimensions limit it?
```

Support can be direct or indirect.

| Support form | Example | Safe interpretation |
| --- | --- | --- |
| Direct syntactic support | Import declaration in a source file. | A name or module was imported there. |
| Direct structural support | Lexical containment or parent metadata. | A thing is contained in another thing under a structural scope. |
| Direct behavior-adjacent support | Call site, route branch, event append, or storage operation. | A scoped behavior candidate exists, subject to static-analysis and reachability guardrails. |
| Documentation support | Design text says one component delegates to another. | A documentation claim exists; it may need repository or runtime support before stronger promotion. |
| Runtime support | Trace or probe observes an edge in one execution instance. | The edge occurred in that instance and vantage point; it is not automatically global architecture. |
| Negative support | Evidence rejects an alternative edge or owner. | Helps contradiction or competing-candidate analysis; does not by itself prove the positive edge. |

Relationship support must be relationship-kind aware. Evidence sufficient for
one relationship kind may be insufficient or unsafe for another.

Examples:

```text
import evidence may support imports
import evidence does not support calls
call-site evidence may support calls under scope
call-site evidence does not support owns
documentation ownership language may support an ownership claim
documentation ownership language does not prove runtime behavior
```

## Relationship Corroboration

Relationship corroboration is compatible support for the same relationship or
for a stronger relationship under a clearly compatible scope.

It should not be counted by raw evidence volume alone. Two evidence records are
not meaningfully corroborating if they are duplicated from the same source,
derived from the same observation, scoped to incompatible entities, or asserting
different relationship kinds.

A relationship support group is a corroboration candidate when evidence agrees
on the relevant normalized edge dimensions:

```text
subject identity or compatible alias
relationship kind or explicitly compatible kind family
object identity or compatible alias
scope/dimensions
source time or freshness window when relevant
vantage point when relevant
```

Examples:

```text
Two independent parsers observe the same import edge.
Documentation says Runtime routes tool calls to ToolExecutor, and repository
evidence shows a route branch from Runtime to ToolExecutor under the same scope.
A runtime trace observes the same call edge that static analysis identified,
within the same execution path.
```

Corroboration can increase support confidence, but it does not automatically
create ownership or verified truth. Corroboration strengthens the answer to:

```text
How much compatible support does Seed have for this edge?
```

It does not by itself answer:

```text
Who owns this concern?
Is this edge current in every projection?
Is this edge required by architecture?
Is this edge the only valid path?
```

## Relationship Contradiction

Relationship contradiction is incompatible support for competing edge-shaped
claims under a shared scope.

Contradiction is not merely absence of corroboration.

The following are different states:

| State | Meaning |
| --- | --- |
| Unsupported | Seed lacks evidence for the relationship. |
| Weakly supported | Seed has limited evidence for the relationship. |
| Uncorroborated | Seed has support, but not independent compatible support. |
| Contradicted | Seed has support for an incompatible relationship or negation under the same scope. |
| Superseded or stale | Fresher evidence may outrank older evidence in a projection, while older evidence remains preserved. |

Relationship contradiction examples:

```text
Evidence supports Runtime routes call_tool decisions to ToolExecutor.
Competing evidence supports Runtime routes call_tool decisions to PlannerExecutor
under the same scope and time window.
```

```text
Documentation says ProjectionStore owns snapshot storage.
Repository evidence shows two storage authorities under the same claimed scope,
and no boundary evidence resolves the split.
```

```text
Static evidence shows module A imports module B.
A later revision removes that import. A current-state projection may select the
newer absence, while historical evidence still preserves the prior edge.
```

Contradiction handling should preserve evidence, expose conflict, and let
projections select or explain according to view-specific rules. It should not
silently delete relationship evidence or mutate a relationship into truth or
falsehood without preserving the support trail.

## Relationship Promotion

Relationship promotion is the movement from relationship-shaped evidence into a
normalized relationship representation.

It should be scoped by relationship kind.

```text
Evidence strong enough for imports may promote imports.
Evidence strong enough for calls may promote calls.
Evidence strong enough for routes may promote routes.
Evidence strong enough for ownership may promote ownership only if the system
has an ownership representation and ownership-specific evidence.
```

Promotion should not be a universal ladder where any weak edge can be upgraded
by naming a stronger predicate. Instead, each relationship kind has its own
minimum evidence threshold and guardrails.

A useful conceptual promotion ladder is:

```text
preserved evidence
        ↓
relationship candidate
        ↓
evidence-backed relationship
        ↓
corroborated or contradicted support group
        ↓
projection-selected relationship view
```

This ladder is descriptive, not a runtime requirement. Its purpose is to prevent
ambiguous language such as "the relationship exists" from hiding which layer is
being discussed.

### Minimum Promotion Rule

A relationship may be promoted when:

1. the source and target participants are identifiable enough for the claimed
   relationship scope;
2. the relationship kind is supported by the evidence type;
3. provenance remains inspectable;
4. confidence or support quality is represented as a signal, not as truth;
5. contradictions are preserved or discoverable rather than erased;
6. the promoted relationship does not imply a stronger relationship kind than
   the evidence can support.

For documentation-only architecture purposes, this is the key rule:

```text
Promote only the relationship the evidence actually supports.
```

## Relationship Confidence

Relationship confidence should be interpreted as a support and selection signal,
not as a truth label.

Different layers may need different confidence meanings:

| Confidence location | Meaning |
| --- | --- |
| Observation | Source-reported or adapter-assigned quality of one reported statement. |
| Evidence | Strength, specificity, freshness, or provenance quality of support material. |
| Relationship | Support quality for the normalized edge. |
| Support group | Corroboration, independence, contradiction, and source diversity signals. |
| Projection | View-specific confidence after selection, ranking, freshness, suppression, or conflict handling. |
| Ownership | Authority confidence after behavior, boundary, policy, scope, and competing-owner analysis. |

A high-confidence relationship should not automatically become a high-confidence
ownership claim. A low-confidence relationship should not be discarded if it is
important contradiction evidence. A projection may lower confidence because of
staleness or conflict without mutating the underlying relationship support.

## Relationship Ownership Boundary

Relationship ownership is not the same as relationship participation.

A relationship can show that two things are connected:

```text
Runtime calls ToolExecutor.
Runtime routes call_tool decisions to ToolExecutor.
ProjectionStore stores ProjectionSnapshot.
Module A imports Module B.
```

Ownership asks a stronger question:

```text
Who is architecturally accountable for this concern under this scope?
```

Relationship evidence can be relevant to ownership, but it is usually
insufficient. Ownership requires authority evidence, scope evidence,
policy/invariant evidence, boundary evidence, and competing-owner analysis.

Required non-equivalences:

```text
imports ≠ owns
calls ≠ owns
routes ≠ owns
stores ≠ owns
emits ≠ owns
validates ≠ owns
participates in ≠ owns
gatekeeps ≠ owns
appears in projection ≠ owns
has highest confidence edge ≠ owns
```

Examples:

- `Runtime calls ToolExecutor` may support the claim that Runtime participates in
  execution flow. It does not prove Runtime owns execution.
- `ToolExecutor executes registered operations` may support the claim that
  ToolExecutor participates in execution. It does not prove ToolExecutor owns
  operation policy unless authority and boundary evidence also support that
  scope.
- `ProjectionStore stores snapshots` may support a storage behavior claim. It
  does not prove ProjectionStore owns snapshot-storage semantics unless the
  architecture assigns that responsibility and competing owners are resolved.

## Relationship vs Fact

Relationships and facts are both normalized knowledge representations, but they
answer different questions.

```text
Fact:       What claim is represented?
Relationship: What edge between participants is represented?
```

A relationship may itself be fact-like in the broad sense that it is a
normalized claim with evidence. The architectural distinction remains useful
because relationships need direction, relationship kind, endpoint identity,
scope, and graph guardrails.

Examples:

```text
Artifact fact: ToolExecutor exists.
Relationship: Runtime imports ToolExecutor.
Relationship: Runtime calls ToolExecutor.
Ownership claim: ToolExecutor owns operation execution.
Projection: Current architecture view displays ToolExecutor as the selected
execution boundary candidate.
```

The artifact fact does not imply the import. The import does not imply the call.
The call does not imply ownership. The projection does not replace preserved
evidence.

## Relationship vs Projection

Projection is a read-model concern. Relationship creation and preservation are
knowledge-model concerns.

A projection may:

- show only current relationships;
- group duplicate support under one edge;
- hide stale relationships by default;
- expose contradictions;
- rank competing edges;
- display confidence summaries;
- annotate ownership candidates;
- explain why an edge is selected or not selected.

A projection should not:

- create runtime semantics by displaying an edge;
- delete evidence by hiding an edge;
- collapse contradictory relationships into one unexplained answer;
- convert a relationship into ownership merely because it is selected;
- treat view confidence as global truth.

The safe boundary is:

```text
Relationships preserve edge-shaped knowledge.
Projections choose how to present edge-shaped knowledge.
```

## Recommended Architectural Vocabulary

To avoid ambiguity, future documents should prefer precise phrases.

| Phrase | Meaning |
| --- | --- |
| `relationship evidence` | Provenance or support material that may justify an edge. |
| `relationship candidate` | A possible normalized edge not yet fully promoted or selected. |
| `evidence-backed relationship` | A normalized edge with inspectable support. |
| `corroborated relationship support` | Compatible support from independent or meaningfully distinct evidence. |
| `contradicted relationship support` | Competing support for incompatible edge claims under the same scope. |
| `projection-selected relationship` | An edge selected or displayed by a read view. |
| `ownership claim` | A claim about architectural responsibility or authority, not mere participation. |
| `relationship confidence` | A support/selection signal scoped to the edge and view, not truth. |

Ambiguous phrases to avoid unless qualified:

```text
true relationship
proved relationship
owned relationship
current relationship
relationship exists
relationship is verified
```

If those phrases are used, the document should state whether it means preserved,
promoted, corroborated, selected, verified, or owned.

## Non-Goals And Guardrails

This reconciliation does not recommend implementation. It does not define a
schema, API, graph validator, projection behavior, relationship model,
confidence formula, inference rule, ownership model, or test plan.

Architectural guardrails:

- Do not infer stronger relationship kinds from weaker evidence.
- Do not infer behavior from imports or existence.
- Do not infer ownership from behavior or projection selection.
- Do not treat raw evidence count as corroboration count.
- Do not treat source trust as evidence support.
- Do not delete contradictory relationship evidence during current-state
  selection.
- Do not collapse relationship preservation into projection display.
- Do not require independent corroboration before preserving weak relationship
  evidence when one source is sufficient for that weak relationship kind.
- Do require stronger evidence before promoting stronger relationship kinds.
- Do preserve provenance and scope so future reconciliation can explain why an
  edge was represented.

## Answer To The Central Question

Evidence justifies a relationship when it supports the specific edge being
created under the specific relationship kind and scope.

The answer is intentionally narrower than truth:

```text
Evidence justifies relationship preservation when it safely supports an
edge-shaped normalized claim with provenance.
```

It justifies stronger relationship treatment only when the evidence supports the
stronger treatment:

```text
corroboration requires compatible independent support;
contradiction requires incompatible support under a shared scope;
projection selection requires view-specific selection rules;
ownership requires authority, scope, boundary, policy, and competing-owner
evidence.
```

Seed should therefore reason about relationships by preserving the weakest
accurate edge the evidence can support, accumulating support and contradiction
without destroying provenance, and leaving current selection and ownership to
explicit projection and authority layers.
