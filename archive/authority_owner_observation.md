---
doc_type: observation
status: exploratory
domain: authority owner investigation
related:
  - descriptive_language_vs_authority_observation.md
  - defines_authority_reconciliation_observation.md
  - measurement_ownership_boundary_audit.md
  - source_navigation_surface_reconciliation.md
  - relationship_fact_reconciliation.md
  - unresolvedness_observation.md
  - inquiry_as_bridge_observation.md
---

# Authority Owner Observation

## Status

Exploratory observation only.

This document investigates a candidate inversion that appeared during recent
authority-formation work:

```text
meaning does not become authority

authority owners authorize meaning
```

The candidate inversion is not assumed to be correct. This document does not
modify implementation, projection behavior, relationship catalogs,
reconciliation behavior, Inquiry Orientation, ontology, runtime concepts, or
policy. It does not conclude that `Authority Owner` is a repository concept,
runtime state, ontology term, policy object, or implementation target.

Repository authority remains with the more specific implementation, tests,
catalogs, and reconciliation documents in their own scopes. The phrase
"authority owner" is used here only as provisional descriptive language for the
investigation.

## Question

Central questions:

```text
Where does authority reside?

What appears to authorize promotion?

What appears to prevent promotion?

Do authority owners exist as a useful descriptive model?

Or is this merely another explanatory framing?
```

A candidate pattern under review is:

```text
evidence
    ->
authority owner
    ->
bounded promotion
```

This differs from a simpler reading:

```text
description
    ->
authority
```

The repository evidence sampled here supports scoped authority boundaries more
strongly than it supports one canonical authority-owner model.

## Repository evidence reviewed

Files and areas inspected for this observation include:

- `seed_runtime/events.py`
- `seed_runtime/projection_store.py`
- `seed_runtime/evidence.py`
- `seed_runtime/facts.py`
- `seed_runtime/relationship_catalog.py`
- `relationship_catalog/core.json`
- `seed_runtime/inference_catalog.py`
- `inference_catalog/core.json`
- `seed_runtime/source_navigation.py`
- `seed_runtime/inquiry_orientation.py`
- `seed_runtime/state_summary_views.py`
- `scripts/seed_local.py`
- `docs/archive/original_book_of_seed/10-build-plan.md`
- `docs/archive/original_book_of_seed/13-knowledge-and-evidence.md`
- `docs/descriptive_language_vs_authority_observation.md`
- `docs/defines_authority_reconciliation_observation.md`
- `docs/measurement_ownership_boundary_audit.md`
- `docs/source_navigation_surface_reconciliation.md`
- `docs/relationship_fact_reconciliation.md`
- `docs/claim_support_frontier.md`
- `docs/evidence_strength_and_claim_strength_reconciliation.md`
- `docs/evidence_trust_and_source_authority_reconciliation.md`
- `docs/unresolvedness_observation.md`
- `docs/inquiry_as_bridge_observation.md`
- `docs/structure_claim_reconciliation.md`

Search terms included `EventLedger`, `ProjectionStore`, `Evidence`, `Fact`,
`FactSupport`, `RelationshipCatalog`, `InferenceCatalog`, `reconciliation`,
`alignment`, `source navigation`, `current belief`, `projection`, `ownership`,
`defines`, `imports`, `unresolved`, and `Inquiry`.

## Authority owner investigation

The repository contains several places where authority-like responsibility is
localized. These are not proof of a general `Authority Owner` concept. They are
better read as scoped implementation or documentation surfaces that decide what
kind of meaning is allowed to have consequences.

### Event and projection storage

`EventLedger` explicitly describes itself as owning append-only runtime event
history, while `ProjectionStore` describes reusable snapshots derived from the
event ledger. This is direct ownership vocabulary, but it is storage/projection
ownership, not general semantic authority. The evidence suggests a boundary:
events can be preserved as historical inputs, while projection snapshots are
cacheable derived read models. Neither storage surface alone authorizes arbitrary
claims about ownership, behavior, relationships, or ontology.

Candidate reading:

```text
event history authority is owned by EventLedger-like storage
projection-cache authority is owned by ProjectionStore-like storage
semantic promotion still requires projection rules and state models
```

This supports scoped ownership language, but not a repository-wide authority
owner abstraction.

### Evidence and fact support

`Evidence` preserves observed payloads with source, kind, time, payload, and
confidence. `Fact` adds subject, predicate, value, dimensions, evidence links,
source type, confidence, timing, and inference metadata. `FactSupport` then
represents projected support for a subject/predicate/value claim, separating
durable aggregate support from current measurement samples.

This supports the recurring threshold:

```text
observed payload
    ->
evidence
    ->
fact
    ->
fact support / current belief
```

The apparent authority is not in the descriptive usefulness of a payload. It is
in the model and projection path that accepts an observation as evidence, emits a
fact, and aggregates or selects support. The owner framing is useful only if it
means that these models and projection rules bound promotion. It is misleading if
it implies a separate actor-like owner behind the models.

### Relationship authority

`RelationshipCatalog` is read-only vocabulary for how entities connect to each
other. Its entries bind relationship names to relationship kinds, endpoint
types, and source predicates. The `defines` authority investigation found that
documentation front matter, source declarations, documentation prose claims, and
structure claims can share related language without sharing one authority domain.

Candidate reading:

```text
relationship meaning is authorized by catalog shape plus relationship-fact
production rules, not by ordinary-language similarity alone
```

This supports an implicit relationship authority boundary. It does not prove that
a named relationship authority owner exists as a repository concept.

### Inference authority

`InferenceCatalog` defines deterministic local fact projection rules. Rules have
an id, activation predicate/value, output predicate/value, confidence, and reason.
This looks like a narrow authority owner for deterministic inference: if a rule
matches, a bounded derived fact can be produced; if no rule matches, explanatory
similarity is not enough.

Candidate reading:

```text
inference promotion is authorized by cataloged deterministic rules
```

The authority is bounded to configured inference rules and their projection
behavior. It does not authorize broad reasoning, ontology expansion, or runtime
concept creation.

### Source navigation authority

`source_navigation.py` states that it projects only existing `imports` and
`defines` facts from projected State. It does not inspect files, parse source,
ingest observations, or infer behavior, reachability, or ownership. This is a
clear case where meaning is useful for navigation only after preserved facts
exist, and where the navigation surface refuses promotion into broader claims.

Candidate reading:

```text
source navigation authority resides in already projected imports/defines support
and in the navigation formatter's refusal to infer beyond that support
```

This supports the authority-owner pattern only as a descriptive model of a
bounded surface.

### Inquiry Orientation authority boundary

`inquiry_orientation.py` intentionally keeps inquiry notes outside the event
ledger and renders a read-only orientation probe. Its authority boundary says the
note is preserved operator prose, not a fact, claim, goal, tool need,
requirement, capability, decision, proposal, plan, authorization, command, or
runtime instruction. Related material is lexical overlap only.

This is strong evidence that descriptive usefulness is not promotion authority.
Inquiry prose can orient work without becoming projected State, policy, runtime
instruction, or ontology. The authority owner framing may describe the absence of
an owner: no existing subsystem accepts the note as evidence for promotion beyond
orientation.

### Storage and measurement ownership

The measurement ownership audit found a strong measurement-subject model and a
strong endpoint/non-endpoint identity boundary, but no separate general
measurement owner, observed entity, or ownership-transfer model. Facts and
support are subject-based; aliases do not silently transfer endpoint observations
to hosts; storage projection groups filesystem current measurements by canonical
fact subject and dimensions.

This supports a negative authority pattern:

```text
visibility / measurement subject / operator usefulness
    !=
ownership authority
```

Repository evidence most strongly supports a lack of modeled ownership authority
for endpoint-derived measurements, plus explicit boundaries that prevent alias,
relationship, current lookup, or storage projection from creating ownership
implicitly.

## Promotion investigation

Several branches show a threshold between useful explanation and
authority-bearing knowledge.

Promotion appears to require at least one of the following repository-authorized
forms:

- a model field or event payload accepted by the runtime path;
- evidence preserved with source/kind/time/payload and later transformed;
- fact extraction or normalization into subject/predicate/value form;
- cataloged relationship or inference vocabulary;
- projection into State, support, conflict, graph issue, summary, or read model;
- reconciliation rules that define what support means for a claim;
- tests that lock the intended boundary.

Promotion appears to be prevented when one or more of these are absent:

- no source evidence is preserved;
- no fact or relationship fact is emitted;
- no catalog entry authorizes the relationship or inference shape;
- no projection field or read-model surface accepts the concept;
- existing tests or comments explicitly reject the inference;
- the branch intentionally preserves uncertainty;
- the language is documentation-only explanatory vocabulary.

Candidate threshold:

```text
useful explanation becomes authority-bearing knowledge only when a scoped
repository surface accepts it and gives it bounded consequences
```

This is still exploratory. The threshold may be an accumulation of independent
implementation habits rather than one repository principle.

## Defines/imports example

The `defines` investigation is a strong comparison case because the same
vocabulary participates in multiple domains without collapsing them.

Repository evidence distinguishes at least these domains:

1. documentation metadata authority, where front matter can say a document
   defines a concept;
2. repository-source declaration authority, where Python AST extraction can say a
   module-like source identity defines a dotted symbol;
3. documentation prose claim authority, where `X defines Y.` can be classified as
   an existence-family claim for later reconciliation;
4. structure-claim authority, where `X defines method Y.` requires containment
   evidence rather than mere co-occurrence.

These domains remain separated by source path, parser, endpoint identity,
relationship-fact shape, claim family, and reconciliation rule. The same word can
therefore carry multiple scoped meanings. The repository evidence supports
"shared vocabulary does not imply shared authority" more directly than it
supports a single `defines` authority owner.

`imports` is narrower in the sampled evidence. Source navigation treats
`imports` as preserved source fact support for navigation, not as reachability,
behavior, dependency ownership, policy, or runtime authority.

## Storage ownership example

Storage ownership pressure is a useful negative case. The repository has:

- fact subjects;
- observation subjects;
- endpoint/non-endpoint identity boundaries;
- storage projection rows;
- measurement predicates and current-sample support;
- provenance metadata from providers;
- explicit warnings that visibility is not ownership.

The repository does not currently show a general modeled distinction among:

```text
measurement owner
observed entity
described entity
ownership transfer
host-owned endpoint measurement
```

The strongest evidence is not simply missing ownership evidence. It is the
combination of missing ownership fields plus deliberate prevention of implicit
ownership through aliases, relationship projection, current lookup, and storage
projection. Therefore, repository evidence most strongly supports:

```text
ownership authority is absent for the general endpoint-measurement case, and
existing boundaries prevent other authorities from standing in for it
```

This is not a recommendation to implement ownership authority.

## Inquiry/unresolvedness example

Inquiry and unresolvedness branches provide comparison cases where language
remains descriptive on purpose.

Inquiry notes are preserved as operator prose and can be oriented against
already projected material, but the orientation probe refuses to turn lexical
overlap into fact, claim, goal, capability, decision, command, authorization, or
runtime instruction. Unresolvedness documents preserve incompletion, pressure,
and uncertainty without requiring a State component or ontology.

Possible explanations for non-promotion include:

- insufficient evidence for fact or relationship promotion;
- no subsystem currently owns promotion of inquiry prose into State;
- uncertainty is intentionally preserved rather than resolved prematurely;
- the usefulness is human-orientation usefulness, not runtime authority;
- promotion could erase the very uncertainty the branch is trying to preserve.

The evidence supports intentional preservation of uncertainty more strongly than
simple neglect.

## Alternative explanations

The authority-owner framing may be wrong or only locally useful. Alternatives
considered:

### There are no authority owners

Repository surfaces may simply have responsibilities, schemas, tests, and
boundaries. Calling them owners may add unnecessary anthropomorphic language.
This alternative is plausible because no inspected code defines `AuthorityOwner`
or a comparable abstraction.

### Ownership language is misleading

`EventLedger` and `ProjectionStore` use ownership wording for storage
responsibility. Extending that wording to semantic authority may overread local
architecture metadata. This alternative is plausible and should constrain future
use of the phrase.

### Authority is emergent

Authority may emerge from the combination of documentation, tests, code,
catalogs, and CLI behavior rather than residing in one named owner. This fits the
reviewed evidence well, especially for current belief and reconciliation.

### Authority resides in evidence only

Evidence is necessary, but the repository repeatedly separates evidence from
facts, support, claims, relationships, projections, and decisions. Evidence alone
does not appear sufficient for promotion.

### Authority resides in projection only

Projection gives consequences to facts and support, but projection itself draws
from event history, evidence, catalogs, reconciliation rules, and model fields.
Projection-only authority underexplains catalog and evidence boundaries.

### Authority resides in documentation only

Documentation can carry repository authority, especially reconciliation and audit
documents. But implementation, tests, catalogs, and projections also exert
bounded authority. Documentation-only authority underexplains runtime and test
constraints.

### Each subsystem is independent

The observed pattern may be a family resemblance among independent subsystems,
not a general principle. This is plausible. The safest conclusion is scoped:
authority-owner language is a candidate descriptive model, not a repository
concept.

## Uncertainties

Open uncertainties:

- Whether future graph validation will need more endpoint-family awareness for
  relationship vocabularies such as `defines` without changing the catalog.
- Whether current belief should be described as projection authority, support
  authority, reconciliation authority, or an emergent result of all three.
- Whether ownership vocabulary should be avoided outside explicit storage and
  architecture metadata to prevent overstatement.
- Whether future lens work will need explicit ownership/observed-entity concepts
  or can remain honest with endpoint visibility and provenance.
- Whether inquiry and unresolvedness will remain documentation-only framing or
  later gain narrowly scoped read-model surfaces.
- Whether the candidate pattern is a real repository tendency or a temporary
  artifact of recent investigation branches.

## Non-conclusions

This document does not conclude that:

- `Authority Owner` is a repository concept;
- authority-owner language should become ontology;
- authority-owner language should become runtime state;
- a new authority framework should be implemented;
- projection behavior should change;
- relationship catalogs should change;
- reconciliation behavior should change;
- Inquiry Orientation should change;
- inquiry should be promoted;
- unresolvedness should be promoted;
- ownership should be promoted;
- storage projection should claim host ownership;
- evidence alone creates authority;
- explanation alone creates authority.

## Major findings

Exploratory findings:

1. Repository evidence supports bounded authority surfaces more strongly than a
   single repository-wide authority-owner model.
2. Meaning appears to become authority-bearing only when accepted by a scoped
   model, catalog, projection, reconciliation rule, or test-backed behavior.
3. Several subsystems behave like implicit authority boundaries: evidence/fact
   models, relationship catalog, inference catalog, source navigation, inquiry
   orientation, current support, and projection storage.
4. The `defines` example shows that shared vocabulary can participate in several
   authority domains simultaneously without collapsing them.
5. Storage measurement work shows that missing ownership authority is not filled
   by visibility, aliases, current lookup, relationship pressure, or projection
   convenience.
6. Inquiry and unresolvedness show that preserving uncertainty can be the
   intended repository status, not merely an incomplete implementation step.

## Candidate authority-owner patterns discovered

Hypotheses only:

| Candidate surface | Possible authority owned | Evidence-strength reading |
| --- | --- | --- |
| `EventLedger` | append-only event history | explicit storage ownership language, scoped to events |
| `ProjectionStore` | cached projected snapshots | explicit cache ownership language, scoped to snapshots |
| `Evidence` / `Fact` / `FactSupport` | observed payload, asserted fact, support/current sample | strong model boundary, not a named owner |
| `RelationshipCatalog` | accepted relationship vocabulary and endpoint shape | strong catalog boundary |
| `InferenceCatalog` | deterministic inference promotion | strong catalog boundary |
| source navigation | read-only imports/defines navigation from existing support | strong refusal to infer beyond support |
| reconciliation docs/rules | claim support interpretation | documentation and implementation boundary where present |
| Inquiry Orientation | orientation-only preservation of prose | strong negative promotion boundary |
| storage projection | current storage measurement presentation | strong projection boundary, no ownership authority |

The candidate pattern can be summarized as:

```text
description
    ->
evidence or pressure
    ->
scoped repository surface accepts or refuses it
    ->
bounded promotion or preserved non-promotion
```

This should remain descriptive unless future repository authority explicitly
promotes it.
