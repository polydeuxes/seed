---
doc_type: observation
status: exploratory
domain: promotion and reconciliation observation
defines:
  - promotion and reconciliation observation
  - descriptive vocabulary promotion question
related:
  - descriptive_vs_architectural_vocabulary_observation.md
  - foundational_ontology_reconciliation.md
  - corroboration_and_fact_promotion_reconciliation.md
  - relationship_promotion_reconciliation.md
  - capability_verification_promotion_reconciliation.md
  - prometheus_acquisition_interpretation_routing_promotion_audit.md
  - inquiry_as_bridge_observation.md
  - inquiry_as_movement_observation.md
  - unresolvedness_observation.md
  - lens_vs_orientation_observation.md
  - lens_view_reconciliation.md
---

# Promotion And Reconciliation Observation

## Status

Exploratory observation only.

This document investigates how descriptive vocabulary might become architectural
vocabulary, whether it does, whether it must, and what evidence appears to
precede that shift. It does not modify implementation, ontology, Inquiry
Orientation, State Summary, runtime behavior, projection behavior, catalogs,
validation, tests, policy, or repository primitives. It does not introduce a
promotion pipeline and does not promote any concept named here.

Repository authority wins over this document. The repository orientation,
constitutional thesis, documentation map, ontology, reconciliation documents,
implementation, catalogs, and tests retain their existing authority in their
respective scopes.

## Question

```text
How does descriptive vocabulary become architectural vocabulary?
Does it?
Must it?
What evidence appears to precede promotion?
```

The prior descriptive-vs-architectural vocabulary observation suggested a useful
but not authoritative contrast:

```text
descriptive vocabulary explains
architectural vocabulary participates
```

This document tests that contrast against repository evidence. It does not assume
promotion is desirable, inevitable, safe, or even a real repository process.

## Repository evidence reviewed

Representative evidence reviewed:

- `README.md`
- `docs/README.md`
- `docs/ontology.md`
- `docs/foundational_ontology_reconciliation.md`
- `docs/archive/original_book_of_seed/02-domain-model.md`
- `docs/archive/original_book_of_seed/03-runtime-loop.md`
- `docs/archive/original_book_of_seed/13-knowledge-and-evidence.md`
- `docs/descriptive_vs_architectural_vocabulary_observation.md`
- `docs/learning_as_lens_observation.md`
- `docs/knowledge_and_understanding_distinction_observation.md`
- `docs/inquiry_frontier.md`
- `docs/inquiry_as_bridge_observation.md`
- `docs/inquiry_as_movement_observation.md`
- `docs/inquiry_preservation_observation.md`
- `docs/unresolvedness_observation.md`
- `docs/lens_vs_orientation_observation.md`
- `docs/lens_view_reconciliation.md`
- `docs/lens_implementation_frontier_observation.md`
- `docs/lens_catalog_observation.md`
- `docs/orientation_bundle_load_bearing_observation.md`
- `docs/repository_observation_language_boundary.md`
- `docs/documentation_observation_reconciliation.md`
- `docs/natural_language_observation_and_intent_derivation_reconciliation.md`
- `docs/corroboration_and_fact_promotion_reconciliation.md`
- `docs/relationship_promotion_reconciliation.md`
- `docs/capability_verification_promotion_reconciliation.md`
- `docs/prometheus_acquisition_interpretation_routing_promotion_audit.md`
- `docs/architectural_findings_characterization.md`
- `docs/architectural_status_and_next_frontier.md`
- `seed_runtime/observations.py`
- `seed_runtime/observation_sources.py`
- `seed_runtime/state.py`
- `seed_runtime/capability_promotion_readiness.py`
- `seed_runtime/inquiry_orientation.py`
- `predicate_catalog/core.json`
- `relationship_catalog/core.json`
- `entity_type_catalog/core.json`
- `capability_catalog/core.json`
- tests covering observation ingestion, fact promotion suppression,
  relationship projection, capability promotion readiness, and Inquiry
  Orientation.

The inspected evidence is uneven. Some areas use `promotion` as a concrete
implementation word: observation-to-fact promotion, fact-to-relationship
projection/promotion, and capability verification promotion readiness. Other
areas use promotion as documentation maintenance language: findings may be
promoted into summaries, bootstraps, indexes, or authority surfaces. These uses
are related only cautiously.

## Historical promotion examples

### Observation, evidence, and fact

`Observation`, `Evidence`, and `Fact` appear to be clear architectural
vocabulary now. They participate in the intake path, event ledger, projection,
state views, tests, and documentation authority. The repository does not show a
simple linear history from metaphor to primitive in the inspected material, but
current evidence shows architectural participation: observations are ingested,
evidence is preserved, facts are normalized claims, and projections are rebuilt
from those records.

Evidence before or around promotion appears to include:

- a need to separate raw observations from supportable claims;
- a need for provenance and freshness;
- a need for deterministic projection;
- tests around ingestion and promotion suppression;
- ontology and reconciliation language distinguishing observation, evidence,
  fact, claim, event, state, and projection.

Reconciliation did not merely rename terms. It formed boundaries: observation is
not truth, evidence is not direct authority, fact is a supported claim form, and
projection is not source of truth.

Authority changed in the sense that implementation and documentation now route
state claims through these objects. Participation emerged in runtime-adjacent
intake, event append, read-model projection, catalogs, and tests.

### Relationship facts and relationship promotion

Relationships are now architectural vocabulary where they participate in
`RelationshipCatalog`, relationship projection, graph validation, entity-type
projection, and tests. The evidence preceding this status appears to be repeated
boundary pressure: identity, alias, support, dependency, monitoring, capability,
and topology language could overclaim if left as prose or ordinary facts.

Reconciliation appears to have formed boundaries around what relationships may
claim and what they must not collapse into identity. Participation followed in
catalog mappings, projected relationship views, validation warnings, and tests.

This is one of the stronger examples where vocabulary became architectural only
when it needed to carry graph semantics, validation risk, and projection
consequences.

### Capability verification promotion readiness

Capability verification promotion readiness is an instructive non-promotion
example. It is implemented and tested, but its implementation repeatedly states
that readiness is not promotion, not `capability_verified`, not selection, not
policy evaluation, and not execution authority.

This suggests that architectural participation is not identical to final
promotion. A concept can participate as a read-only inspection boundary while
explicitly preventing a stronger architectural claim.

Evidence before any future capability verification promotion would need at least:

- candidate support;
- verification support;
- an authority decision that `capability_verified` facts are allowed;
- boundaries separating verification from selection, authorization, execution,
  and policy;
- tests proving no accidental writes or execution.

The current repository stops short of that promotion. The existence of a
promotion-readiness surface is evidence that the repository can architect a
pre-promotion state without promoting the target claim.

### Prometheus interpretation and relationship promotion

The Prometheus audit shows an unsafe or partially unsafe form of promotion:
interpretations become derived observations, observations become facts, and fact
predicates project relationships. The audit treats this as a collapse risk, not
as proof that promotion is desirable.

Evidence preceding promotion in this case was not necessarily sufficient. Some
participation occurred too early or too implicitly: labels, endpoint roles, and
identity-like predicates entered fact or relationship surfaces before explicit
candidate subject and candidate relationship layers existed.

This example complicates the model. Architectural participation can occur before
adequate reconciliation, and later reconciliation may identify the participation
as over-promotion that should be narrowed, suppressed, or routed through a safer
candidate boundary.

### Documentation observations and natural language

Documentation observation and natural-language reconciliation show another path:
ordinary prose can become evidence-bearing without becoming executable authority.
Natural language can support claims about communicative acts while remaining weak
or irrelevant as direct support for environmental truth.

This suggests that descriptive language can gain architectural participation in a
bounded way: not by becoming a runtime instruction, but by becoming a source type,
observation family, or evidence boundary.

## Reconciliation investigation

Repository evidence supports several roles for reconciliation, none exclusive.

### Reconciliation as clarification

Reconciliation often clarifies overloaded language. Examples include observation
versus evidence, claim versus fact, relationship versus identity, projection
versus authority, capability candidate versus verified capability, and natural
language observation versus execution command.

Clarification alone does not promote vocabulary. Many observation documents
clarify terms while explicitly refusing implementation or ontology changes.

### Reconciliation as boundary formation

Boundary formation appears stronger than clarification. Reconciliation frequently
states what a concept is not allowed to do. This is visible in authority models,
execution boundaries, source-authority constraints, projection limits, and
read-only inspection boundaries.

Boundary formation may precede promotion because architectural vocabulary needs
negative space: what it cannot authorize, execute, imply, validate, or project.

### Reconciliation as authority formation

Reconciliation sometimes becomes architectural case law. The documentation map
routes readers to reconciliation documents for boundary-sensitive work, and the
README names reconciliation documents as architectural case law / boundary
reasoning. This gives reconciliation an authority role without making every
finding implementation-ready.

Authority formation appears to be a precondition for safe promotion only when the
concept will affect behavior, projection, source interpretation, or downstream
claims. It is not needed for every descriptive observation.

### Reconciliation as promotion mechanism

The evidence does not support a simple claim that reconciliation causes
promotion. Reconciliation can:

- preserve uncertainty;
- block promotion;
- narrow existing promotion;
- route future work;
- document that implementation already participates unsafely;
- authorize bounded implementation later.

So reconciliation may be a promotion mechanism in some cases, but it more often
appears to be a pressure test and boundary-forming process. Promotion, when it
occurs, needs additional participation in implementation, catalogs, projections,
tests, or authoritative vocabulary surfaces.

## Participation investigation

The participation test remains useful but incomplete.

Observed participation surfaces include:

- runtime routing and event append;
- observation ingestion;
- evidence preservation;
- fact promotion;
- relationship projection;
- State and State Summary read models;
- projection caches;
- catalogs and schema-like JSON files;
- validation warnings and tests;
- CLI behavior;
- public API exports;
- reconciliation documents;
- documentation map routing;
- authority boundaries and non-goals.

Participation can appear in different temporal positions:

1. **Before reconciliation.** Prometheus-derived relationships show behavior can
   participate before boundary reasoning catches up. This can create overclaim
   risk.
2. **During investigation.** Capability promotion readiness participates as an
   inspection surface while explicitly refusing final promotion.
3. **After reconciliation.** Natural language, learning, contradiction, and
   federation reconciliations are routed as stable references for bounded future
   work, but they do not automatically create runtime concepts.
4. **Never.** Seeing, unresolvedness, pressure, and some learning language may
   remain descriptive even when useful.

Therefore participation is evidence of architectural status, but participation
alone does not prove that promotion was safe, intended, complete, or desirable.

## Authority investigation

Authority appears central to promotion questions.

The repository's authority model places orientation, constitutional thesis,
documentation navigation, ontology, and reconciliation documents in different
roles. Implementation and tests then provide behavior evidence. A term becomes
architecturally load-bearing when some authority surface says other work must
route through it, preserve its boundary, or respect its consequences.

Authority appears to prevent promotion when:

- a document explicitly says a concept is observation-only;
- implementation says a surface is read-only;
- tests prove no facts, events, policy checks, or tool execution occur;
- the documentation map routes a topic to a different owning document;
- ontology boundaries reject a collapse;
- a concept lacks a source-of-truth relationship.

Authority appears to enable promotion when:

- a concept has an owning document or vocabulary surface;
- it has a bounded meaning and non-meaning;
- it has implementation and tests;
- catalogs or projections consume it;
- downstream behavior depends on it;
- repository documents route future changes through it.

This does not mean authority is a separate engine. It may be distributed across
human instructions, documentation hierarchy, reconciliations, code, catalogs,
and tests.

## Inquiry and unresolvedness as test cases

Inquiry and unresolvedness repeatedly explain continuation, pressure, unfinished
understanding, gaps, questions, movement, and handoff survival. Their current
participation is mixed and carefully bounded.

`seed_runtime/inquiry_orientation.py` implements a minimized read-only inquiry
note orientation probe. That is architectural participation of an orientation
surface, not promotion of inquiry into a general runtime object. The module says
inquiry notes are preserved outside the event ledger, render related projected
material, and do not create facts, goals, tool needs, decisions, plans, commands,
or runtime instructions.

This suggests three possibilities:

1. Inquiry has insufficient evidence for broad promotion.
2. Inquiry's natural architectural role may be bounded orientation rather than a
   runtime primitive.
3. Inquiry may remain largely descriptive while specific sub-surfaces such as
   notes, frontiers, active edges, questions, gaps, or handoff lineage carry any
   necessary participation.

Unresolvedness appears even less promoted. It remains useful for describing why
questions, gaps, contradictions, and frontiers continue, but inspected evidence
does not show it as a catalog entry, runtime branch, projection object, or
validation target. Its current resting state may be descriptive, or it may be a
pressure signal that decomposes into more specific architectural surfaces.

The evidence does not support promoting inquiry or unresolvedness here.

## Lens and orientation as test cases

Lens and orientation are closer to architectural participation than `seeing` or
`unresolvedness`, but their statuses differ.

`lens` appears as a recurring descriptive and compression pattern, a way to see
or group evidence without replacing source authority. Some lens work explores
view architecture and implementation frontiers, but the inspected evidence does
not support a general conclusion that lens is already a runtime primitive or
catalog-governed concept.

`orientation` shows stronger participation. The Inquiry Orientation probe, State
Summary discussions, handoff bootstrap/summary work, and orientation bundle
observations all indicate that orientation can affect continuation and safe
resumption. But the authority boundary remains strict: orientation is not itself
permission, fact creation, command execution, policy, or next-action selection.

Possible reading:

```text
lens primarily explains how material is seen or compressed;
orientation participates when it becomes a bounded read-only surface for safe
continuation, but it still does not become execution authority.
```

That reading is only observational. It should not be treated as ontology.

## Alternative models

### No promotion process exists

Supported in part. The repository may not have a general promotion process.
Instead, different areas use different mechanisms: fact promotion, relationship
projection, documentation promotion, capability readiness, and implementation
adoption. Similar words may hide different processes.

### Promotion is an illusion

Supported in part. A concept may feel promoted because it is mentioned often,
but repository authority may still keep it descriptive. Repeated language is not
architectural participation.

### Architectural vocabulary is descriptive vocabulary with implementation

Partially supported but too weak. Implementation is strong evidence, but
architectural vocabulary can also be established by ontology, catalogs,
validation, documentation authority, and reconciliation boundaries. Conversely,
implemented surfaces can be explicitly read-only or non-promoting.

### Reconciliation is unrelated

Not supported as a strong claim. Reconciliation repeatedly forms boundaries that
make later implementation safer or identify unsafe existing behavior. But
reconciliation is not always causal and does not guarantee promotion.

### Authority is unrelated

Not supported. Authority boundaries appear repeatedly in deciding whether a term
can create facts, route runtime behavior, authorize execution, affect projection,
or bind future work.

### Descriptive and architectural vocabulary are maturity stages

Sometimes plausible. Candidate, frontier, observation, audit, reconciliation,
implementation, and test surfaces can look like maturation. But some concepts may
rightly remain descriptive, and some architectural terms may enter implementation
before enough reconciliation. A maturity-stage model overstates orderliness.

### Descriptive and architectural vocabulary are separate categories

Sometimes plausible. `seeing`, `pressure`, and `unresolvedness` may remain useful
because they explain without participating. But the categories are porous:
orientation and natural language show bounded participation without becoming
unbounded architecture.

## Candidate promotion patterns discovered

These are candidate patterns, not policy:

1. **Pressure accumulation.** A term recurs across investigations because it
   explains a persistent ambiguity, risk, or missing distinction.
2. **Decomposition.** Broad descriptive terms split into more specific terms that
   can carry support, provenance, validation, or projection.
3. **Boundary formation.** Reconciliation states what the candidate may not mean
   or do.
4. **Authority routing.** The documentation map, ontology, or reconciliation
   chain starts routing future work through the bounded concept.
5. **Participation surface.** Code, catalogs, projections, CLI behavior, tests,
   or public APIs consume the concept.
6. **Suppression or quarantine.** The repository may create explicit no-promotion
   mechanisms when evidence is useful but authority is insufficient.
7. **Narrower substitute.** Instead of promoting the broad term, the repository
   promotes a narrower relation, source type, candidate family, read-only view,
   or evidence boundary.

The strongest negative pattern is equally important:

```text
frequent explanatory usefulness does not by itself justify promotion.
```

## Uncertainties

- The inspected files do not prove a universal historical sequence from
  descriptive to architectural vocabulary.
- Some concepts may have been architectural from inception rather than promoted.
- Some implementation participation may be accidental, historical, or later
  judged unsafe.
- Documentation promotion and runtime/fact promotion share vocabulary but may be
  different phenomena.
- The repository may prefer decomposition over promotion for broad terms such as
  learning, understanding, inquiry, pressure, and unresolvedness.
- It remains unclear whether bounded orientation surfaces are early promotion,
  a separate category, or merely read-only presentation.

## Non-conclusions

This observation does not conclude that:

- a promotion pipeline exists;
- promotion should occur;
- promotion is inevitable;
- descriptive vocabulary is immature;
- architectural vocabulary is superior;
- inquiry should be promoted;
- unresolvedness should be promoted;
- lens should be promoted;
- orientation should be expanded;
- reconciliation causes promotion;
- authority alone causes promotion;
- new ontology, runtime concepts, policy, catalogs, or tests should be created.

The safest current conclusion is weaker:

```text
Repository evidence suggests that architectural vocabulary tends to require
participation plus authority boundaries, and that reconciliation often tests or
forms those boundaries. Descriptive vocabulary can remain permanently useful
without becoming architecture.
```
