---
doc_type: observation
status: exploratory
scope: authority formation pattern investigation
created: 2026-06-18
---

# Authority Formation Pattern Observation

## Status

Exploratory observation only.

This document records an investigation into whether several unresolved Seed
branches are expressing a common authority-formation question. It does not
modify implementation, ontology, projection rules, relationship catalogs, source
navigation, topology ownership logic, claim support, Inquiry Orientation, or
runtime behavior.

The investigated candidate shape was:

```text
description
    ->
evidence
    ->
alignment
    ->
projection
    ->
authority-bearing knowledge
```

This document does not assume that shape is correct. It preserves competing
readings where repository evidence does not support reconciliation.

## Repository Evidence Reviewed

Reviewed evidence included:

- `docs/archive/original_book_of_seed/01-architecture.md`, especially catalog boundaries, knowledge projection,
  current belief, relationship projection, inference projection, and
  `EventLedger`/`ProjectionStore` ownership.
- `docs/measurement_ownership_boundary_audit.md`, especially endpoint
  visibility, measurement subject, alias-like knowledge, storage projection, and
  host-ownership non-conclusions.
- `docs/descriptive_vs_architectural_vocabulary_observation.md`, especially the
  distinction between explanatory language and architectural vocabulary.
- `docs/relationship_fact_reconciliation.md`, especially the evidence ladder
  from existence to ownership and the distinction between artifact facts and
  relationship facts.
- `docs/repository_observation_language_boundary.md`, especially Repository
  Observation as language-neutral acquisition of evidence-backed artifact facts.
- `docs/repository_reconciliation_v0_implementation_characterization.md`,
  especially alignment records preserving claim, facts used, rule id, outcome,
  and reason.
- `seed_runtime/source_navigation.py`, especially source navigation as read-only
  projection over existing `imports` and `defines` facts.
- `seed_runtime/knowledge/relationship_observation.py`, especially `defines`
  relationships as declaration evidence only.
- `seed_runtime/knowledge/self_model_alignment.py`, especially deterministic
  support rules for existence and structure claims.

## Recurring Patterns Found

### Description Is Preserved Without Promotion

Repository evidence repeatedly allows descriptive language to name a pressure,
pattern, or possible meaning without making that language architectural.

The descriptive-vs-architectural vocabulary observation states that some
concepts are useful for explanation while not all explanatory concepts become
architectural concepts. It also states that more-specific architecture,
reconciliation, implementation, tests, and observations retain authority for
their scopes.

This pattern matches the first part of the proposed shape:

```text
descriptive material
    ->
candidate meaning
```

but repository evidence does not support an automatic transition from candidate
meaning to authority.

### Evidence Is Necessary But Not Sufficient

Evidence appears as a recurring boundary between description and stronger
knowledge, but different evidence kinds authorize different claim families.

Examples:

- Artifact facts can support existence and some structure, but not behavior by
  themselves.
- Relationship evidence is needed for behavior-oriented claims.
- Endpoint-scoped measurement evidence can support endpoint-scoped current
  measurement knowledge without proving host ownership.
- A `defines` relationship extracted from Python source is declaration evidence,
  not call evidence, ownership-of-capability evidence, or runtime reachability
  evidence.

A safer formulation is therefore:

```text
description
    ->
evidence of a particular kind
    ->
bounded support for a particular claim family
```

### Alignment Mediates Between Claims And Evidence

Repository reconciliation inserts an explicit comparison step between claims and
repository observations.

The v0 reconciliation characterization says alignment records should preserve:

```text
documentation claim record
repository artifact fact records used
rule id
outcome
reason
```

The self-model alignment implementation follows this shape. For example, an
existence claim of the form `X defines Y` is supported only when the owner symbol
and defined symbol appear in artifact facts from the same path. A structure claim
of the form `X defines method Y` is supported only when a class artifact and a
method artifact with matching parent-symbol containment are present.

This supports an intermediate mechanism:

```text
claim or description
    ->
evidence records
    ->
deterministic alignment rule
    ->
support outcome
```

The support outcome may become important repository knowledge, but it is still
bounded by the claim family, evidence used, and rule id.

### Projection Is Authority-Bearing Only Within Bounded Rules

Projection is one of Seed's central authority-bearing mechanisms, but only when
projection is explicitly owned and bounded.

Repository architecture says the knowledge layer projects current belief from
immutable observations. It also says facts are derived from Evidence with
confidence and provenance, relationships are projected from facts using the
`RelationshipCatalog`, graph validation is explicit, and explanation traverses
support, conflicts, inference links, and provenance without adding a new
reasoning mechanism.

Inference projection is similarly constrained. Inferred facts are deterministic
projection artifacts from unambiguous observed/current facts, carry source fact
and rule ids, respect cardinality, cap confidence at the source fact's
confidence, and cannot overwrite observed facts.

Projection therefore supports authority formation only where the relevant
projection owner and rules already exist.

### Shared Language Is Not Shared Authority

The `defines` / `imports` area shows that shared words do not imply shared
authority.

The same word can appear in documentation metadata, source-observation facts,
relationship facts, source-navigation rows, and self-model claims. Seed separates
these by evidence source, fact shape, rule family, projection boundary, and
consumer.

Source navigation is especially explicit. It projects only existing `imports` and
`defines` facts from projected state. It does not inspect files, parse source,
ingest observations, or infer behavior, reachability, or ownership.

Similarly, the Python definition relationship adapter emits `defines`
relationships as declaration evidence only. It explicitly does not make call,
behavior, ownership-of-capability, or runtime reachability claims.

## Storage Topology Reading

Current storage-related evidence can increase support for ownership-like
interpretations:

```text
blkid
filesystem visibility
mount observations
shared storage candidates
```

However, repository evidence preserves these boundaries:

```text
measurement != ownership
visibility != ownership
candidate != fact
```

The measurement ownership audit found no general `measurement_owner`,
`observed_entity`, `observation_target`, `owner_subject`, or `describes_entity`
field for facts or observations. It also found that the effective current
measurement owner is the fact subject after permitted alias canonicalization, not
a separately modeled described entity.

Therefore, additional alignment would be required before ownership-like storage
knowledge becomes authoritative. Repository evidence suggests that alignment
would need to be explicit and evidence-bearing, such as a separately named
projection or cataloged relationship with provenance and strict source rules. The
audit identifies unsafe routes: expanding alias predicates, treating
`prometheus_instance` as identity, or making current-facts lookup cross
endpoint/non-endpoint boundaries.

This investigation does not conclude that Seed should add such a concept.

## Defines / Imports Reading

`defines` and `imports` share vocabulary across documentation, source facts,
relationship facts, source-navigation rows, and claim support rules, but the
repository distinguishes shared language from shared authority.

The distinction appears to rest on:

- where the term was observed;
- what evidence record carries it;
- which claim family is being evaluated;
- which deterministic rule or projection consumes it;
- whether the consuming surface is read-only presentation, support alignment, or
  projected state;
- whether the evidence authorizes existence, structure, behavior, boundary, or
  ownership.

Thus, shared language becomes authoritative only when it participates in a
specific evidence and rule context. The word itself does not carry authority
across contexts.

## Repository Knowledge Reading

Repository knowledge can influence future work, but repository evidence does not
support treating all repository knowledge as architectural authority.

Repository knowledge appears to become authoritative when it is represented in a
recognized authority-bearing surface, such as:

- append-only events;
- Evidence and Facts;
- FactSupport and current-belief projection;
- relationship edges projected from facts through `RelationshipCatalog`;
- deterministic inference artifacts through `InferenceCatalog`;
- documentation claims aligned with repository artifact facts;
- alignment records with rule id, outcome, reason, and evidence references;
- bounded read-only views over projected support;
- architecture documents that define ownership and source-of-truth boundaries.

Repository knowledge can also remain descriptively authoritative inside an
observation document. That authority may authorize a way of reading evidence
without authorizing schema, runtime behavior, projection behavior, or ontology.

## Competing Explanations

### Explanation A: A Shared Authority-Formation Pattern Exists

A broad shared pattern appears to exist:

```text
description / claim / observation
    ->
evidence record with provenance
    ->
typed support or relationship to a claim/fact
    ->
alignment, catalog rule, validation, or deterministic projection
    ->
bounded authority-bearing knowledge
```

This fits storage ownership pressure, source navigation and `defines` authority,
repository reconciliation, relationship facts, and current-belief projection.

### Explanation B: There Are Several Related Mechanisms, Not One Mechanism

A competing explanation is that the apparent common shape is a family resemblance
among several mechanisms:

- projection;
- reconciliation/alignment;
- catalog validation;
- relationship projection;
- inference projection;
- support aggregation;
- read-only view construction;
- subsystem ownership boundaries.

Under this explanation, Seed does not have one authority-formation pipeline. It
has a repeated discipline: do not promote meaning unless a named subsystem,
evidence type, rule, catalog, projection, or reconciliation boundary authorizes
that promotion.

### Explanation C: Authority Resides Mainly In Ownership Boundaries

Another explanation is that the recurring question is less about a linear chain
and more about ownership: which subsystem owns which kind of authority.

Examples:

- `EventLedger` owns append-only facts about what happened.
- `ProjectionStore` owns cached projected state.
- `RelationshipCatalog` owns topology semantics.
- `InferenceCatalog` owns deterministic inference rules.
- Source navigation owns only read-only presentation of existing source facts.
- The measurement model currently lets fact subject plus permitted alias
  canonicalization carry measurement authority.

This explanation is compatible with a shared pattern, but it shifts emphasis from
sequence to authority owner.

## Whether A Shared Pattern Appears To Exist

A shared authority-formation pattern appears to exist, but only in a cautious,
bounded form.

The repository does not support:

```text
descriptive material
    ->
candidate meaning
    ->
projected authority
```

as an automatic pattern.

The repository better supports:

```text
description / claim / observation
    ->
evidence with provenance
    ->
alignment, catalog validation, or deterministic projection
    ->
bounded support or projected belief
    ->
authority-bearing knowledge within an explicitly owned scope
```

The repeated mechanism between preserved description and authority-bearing
knowledge appears to be bounded evidentiary alignment under named authority
owners.

## Where Authority Appears To Reside

Repository evidence suggests authority is distributed by kind:

- In append-only event history for what happened.
- In projected state for current facts, support aggregates, relationships,
  aliases, entity types, graph issues, recommendations, and cache metadata.
- In evidence-backed facts and support for current belief.
- In catalogs and deterministic rules for bounded vocabulary and projection
  semantics.
- In alignment/reconciliation records for claim support outcomes.
- In explicit subsystem ownership boundaries.
- In documents, but only within the document's declared scope and authority.

## Uncertainties

- The repository supports a recurring pattern, but does not prove there is one
  universal authority-formation mechanism.
- Storage ownership remains unresolved. Current evidence preserves endpoint
  visibility, measurement subject, and alias boundaries, but does not decide
  whether Seed should add a future observed-entity or ownership concept.
- Repository knowledge can become more authoritative, but evidence thresholds
  differ across existence, structure, behavior, boundary, and ownership.
- `RelationshipFact` appears as an architectural primitive in reconciliation
  writing, but the repository does not require every relationship to immediately
  become a production type.
- Descriptive concepts may be immature architecture, permanently descriptive
  vocabulary, or pressure indicators. The reviewed evidence does not force one
  interpretation.

## Non-Conclusions

This investigation does not conclude that:

- storage ownership should be implemented;
- endpoint-derived filesystem observations should become host-owned facts;
- `prometheus_instance` should become an alias or identity bridge;
- current-facts lookup should cross endpoint/non-endpoint boundaries;
- source navigation should infer behavior, reachability, or ownership;
- `defines` should have one universal authority across documentation, source
  observation, relationship facts, and navigation rows;
- repository knowledge should become a new ontology or runtime object;
- Inquiry, unresolvedness, lens, orientation, or descriptive repository knowledge
  should be promoted;
- projection should become an unrestricted authority-making operation;
- a new schema, catalog, runtime object, ontology, or implementation should be
  introduced.
