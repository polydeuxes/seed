# Answer Composition Visibility as Surface Self-Knowledge Investigation

## Question

This investigation asks whether `answer composition visibility` is a new
architectural concern or a continuation of Seed's existing repository
self-knowledge about operational surfaces.

The bounded answer is:

```text
Answer composition visibility is best understood as incomplete surface
self-knowledge: the next semantic layer above the mechanical surface
self-knowledge already accepted by diagnostic inventory and diagnostic shape
audit.
```

It is not yet evidence for a new engine, registry, metadata framework, CLI, or
runtime behavior. Repository authority supports the pressure, but the pressure is
architectural characterization first.

## Files inspected

- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `seed_runtime/operational_story.py`
- `seed_runtime/integrity_summary.py`
- `seed_runtime/inquiry_orientation.py`
- `seed_runtime/source_navigation.py`
- `seed_runtime/projection_shape.py`
- `seed_runtime/reasoning_path_audit.py`
- `seed_runtime/selection_path_audit.py`
- `docs/repository_self_explanation_investigation.md`
- `docs/answer_composition_visibility_investigation.md`
- related repository-shape, reasoning-chain, projection self-description,
  navigation, and self-knowledge investigations found through repository search

## Existing self-knowledge mechanisms

### Diagnostic Inventory

Diagnostic Inventory is the clearest existing surface self-knowledge mechanism.
Its entry shape declares, for each diagnostic-like operational surface:

- surface name;
- CLI flags;
- projected-state use;
- repository-file use;
- JSON support;
- record support;
- record scope;
- diagnostic-fact emission;
- cluster-fact emission;
- event-ledger writes;
- cluster mutation;
- diagnostic-fact reads;
- description.

This is repository self-knowledge about a surface contract. It does not answer
why an operator should choose the surface for a question, but it declares what
the surface is mechanically allowed and expected to do.

### Diagnostic Shape Audit

Diagnostic Shape Audit proves that Seed does not treat these declarations as
mere documentation. It compares inventory fields against implementation evidence
for fields such as:

- `supports_record`;
- `supports_json`;
- `record_scope`;
- `emits_diagnostic_facts`;
- `writes_event_ledger`;
- `reads_diagnostic_facts`;
- `uses_repo_files`;
- `uses_projected_state`;
- `mutates_cluster`.

It also binds diagnostic names to implementation modules, functions, CLI flags,
JSON flags, repo-file markers, diagnostic-fact read markers, and mutation
markers. This is strong precedent: Seed already accepts repository self-knowledge
about repository structures as a legitimate responsibility when operational
visibility is at stake.

### Projection Shape

Projection Shape is not a diagnostic inventory entry shape, but it shows the same
pattern inside projection. Projection stages know what they consume, produce,
influence, do not influence, and what authority boundary governs them. This is
self-knowledge about projection structure rather than CLI mechanics.

### Operational Story

Operational Story composes pressure, capability needs, privilege constraints,
correlation gaps, impact, recent changes, observed outcomes, investigation path,
unknowns, and a read-only boundary. It is already close to an answer contract
because it declares a focus, consumes known source surfaces, preserves unknowns,
and says that it does not record, write the event ledger, or mutate cluster
state.

### Projection Integrity Summary

Projection Integrity Summary aggregates existing integrity signals into a
read-only count summary and explicitly preserves caveats that counts are not
truth, correctness, health, repair, provider availability, or execution. It is a
bounded answer composition over existing projection integrity views.

### Inquiry Orientation

Inquiry Orientation preserves an operator note as non-fact probe evidence, uses
lexical overlap against projected read models and source navigation, exposes
related material, and preserves uncertainty plus authority boundary. It is a
composition whose non-authority is especially explicit.

### Source Navigation

Source Navigation answers source-location questions from preserved `defines` and
`imports` facts only. It explicitly does not inspect files, parse source, ingest
observations, or infer behavior, reachability, or ownership. This is a compact
example of surface self-knowledge that includes negative authority.

### Reasoning Path Audit and Selection Path Audit

Reasoning Path Audit and Selection Path Audit show that Seed already accepts
exposing derivation and selection paths as read-only answer-support surfaces.
They preserve evidence, intermediate or selected material, consumers or
non-selected candidates, unknowns, and no-mutation boundaries. These are not just
mechanical diagnostics; they are bounded explanations of how a conclusion or
selection arose.

## What Seed already knows about its surfaces

Seed already has strong mechanical and boundary self-knowledge.

### Surface capabilities

Diagnostic Inventory declares whether a surface supports JSON, supports record,
uses projected state, uses repository files, emits diagnostic facts, emits
cluster facts, reads diagnostic facts, writes the event ledger, or mutates the
cluster. This is capability knowledge about the surface itself.

### Surface behavior

Diagnostic Shape Audit inspects implementation markers, CLI flags, expected
functions, JSON functions, record functions, repo-file markers, diagnostic-fact
read markers, and mutation markers. This means Seed can check whether declared
behavior and implementation-shaped behavior agree.

### Surface authority

Several reviewed surfaces preserve explicit authority boundaries:

- Diagnostic Inventory distinguishes diagnostic facts from cluster facts and
  cluster mutation.
- Projection Shape assigns projection-stage authority boundaries such as
  selection-bearing, derivation-bearing, validation-only, explanatory-only,
  identity-resolution, and projection-boundary.
- Projection Integrity Summary states that integrity counts are not truth or
  correctness judgments.
- Inquiry Orientation states that preserved inquiry prose is not a fact, goal,
  plan, authorization, command, or runtime instruction.
- Source Navigation states that it does not infer behavior, reachability, or
  ownership.

### Surface boundaries

Seed consistently distinguishes read-only diagnostic visibility from cluster
truth. The strongest examples are `record_scope=diagnostic_run`,
`writes_event_ledger=false`/`mutates_cluster=false` diagnostic boundaries,
Operational Story's read-only boundary, Reasoning Path Audit's no-recording
boundary, and Selection Path Audit's no-mutation boundary.

## What self-knowledge is missing

The missing layer is not that Seed lacks compositions. It is that many
compositions do not uniformly self-describe their semantic answer contract.

Missing or unevenly exposed fields include:

- **question family**: what class of operator or repository question the surface
  is meant to answer;
- **answer responsibility**: what output obligation the surface owns beyond raw
  display;
- **consumed knowledge**: which source surfaces, state projections, docs, facts,
  or implementation evidence are part of the answer;
- **preserved uncertainty**: what unknowns, caveats, alternatives, rejected
  paths, or incomplete evidence remain after the answer;
- **non-authority**: what the surface explicitly does not answer or is not
  allowed to promote;
- **adjacent unanswered questions**: what natural follow-up questions remain
  outside the surface boundary;
- **composition status**: whether the surface is raw inventory, read model,
  diagnostic, explanation, selection trace, orientation, or bounded answer
  composition.

These are not new kinds of cluster truth. They are self-knowledge about what a
surface answers.

## Surface contract vs answer contract

There is a meaningful distinction, but not a hard separation.

A **surface contract** says:

```text
This surface exists; these are its flags, inputs, outputs, recording behavior,
implementation markers, and mutation boundaries.
```

An **answer contract** says:

```text
This surface answers this question family; it consumes these authorities;
it preserves these caveats and unknowns; it does not answer these adjacent
questions; its output has this responsibility.
```

Diagnostic Inventory and Diagnostic Shape Audit mostly govern surface contracts.
Operational Story, Inquiry Orientation, Projection Integrity Summary, Source
Navigation, Reasoning Path Audit, and Selection Path Audit already contain
partial answer contracts in their data shapes, caveats, unknowns, consumed source
surfaces, and boundaries.

Therefore the architectural distinction is meaningful, but the repository
evidence suggests answer contracts are not a fundamentally separate object. They
are richer semantic self-knowledge attached to surfaces that already have
mechanical contracts.

## Does Operational Story already imply an answer contract?

Yes, partly.

Operational Story answers a bounded question resembling:

```text
What is the current operational story supported by existing visibility surfaces?
```

It implies an answer contract through:

- **question answered**: current operational focus and pressure;
- **inputs consumed**: pressure audit, capability needs, privilege discovery,
  correlation audit, impact audit, and investigation path audit;
- **authority boundary**: read-only view, no fact recording, no event-ledger
  writes, no cluster mutation;
- **uncertainty preserved**: missing pressure, missing capabilities, and unknown
  impact are carried as unknowns;
- **questions not answered**: it does not plan, execute, record, mutate, or prove
  operational truth.

Operational Story is therefore the strongest evidence that Seed already has
answer contracts in practice, even if it does not uniformly identify them as
such.

## Are answer compositions fundamentally different objects?

The reviewed evidence does not justify treating answer compositions as a
fundamentally different architectural object.

They look more like surfaces with richer self-knowledge:

```text
mechanical surface contract
    + consumed authorities
    + bounded question family
    + answer responsibility
    + uncertainty preservation
    + negative authority
```

The repository already contains raw views, diagnostics, summaries, audits,
orientation views, navigation views, and composed stories. These vary by
semantic responsibility, not by requiring a new architectural substrate.

The stronger boundary is not `surface` versus `composition`; it is:

```text
surface with only mechanical visibility
    vs
surface with mechanical visibility plus semantic answer visibility
```

## Required tensions

### Surface inventory vs answer inventory

Surface inventory is already real and tested for diagnostics. An answer
inventory is not proven necessary. The current pressure can be described without
assuming an inventory: Seed has many known surfaces, but their question families
and answer responsibilities are not uniformly visible.

### Surface contract vs answer contract

Surface contracts are mechanical and operational. Answer contracts are semantic
and epistemic. They overlap because semantic answers still need mechanical
boundaries, record scopes, source authority, and mutation status.

### Mechanical behavior vs semantic responsibility

Diagnostic Shape Audit knows whether a surface supports JSON or reads diagnostic
facts. It does not know whether a surface answers `why this conclusion`, `which
pressure is primary`, `where is this source symbol`, or `what uncertainty
remains`. The missing pressure is semantic responsibility, not mechanical
behavior.

### Surface self-knowledge vs answer self-knowledge

Answer self-knowledge appears to be a subtype or next layer of surface
self-knowledge. It asks the same self-knowledge question at a higher level:

```text
not only what does this surface do mechanically?
but what answer does this surface take responsibility for?
```

### Diagnostic visibility vs composition visibility

Diagnostic visibility made operational surfaces inspectable and boundary-checked.
Composition visibility would make composed answers inspectable and
boundary-understandable. The latter is a refinement of the former's principle,
not a replacement.

## Strongest supporting evidence

1. Diagnostic Inventory explicitly models operational diagnostic surface
   capabilities and boundaries.
2. Diagnostic Shape Audit checks declared shape against implementation evidence,
   proving that self-knowledge about repository structures is a legitimate Seed
   responsibility.
3. Projection Shape extends the same pattern beyond diagnostics by naming
   consumes, produces, influence, non-influence, confidence, and authority
   boundary.
4. Operational Story already composes multiple surfaces into a bounded answer
   with focus, inputs, unknowns, investigation path, and read-only boundary.
5. Projection Integrity Summary, Inquiry Orientation, Source Navigation,
   Reasoning Path Audit, and Selection Path Audit already preserve caveats,
   uncertainty, negative authority, or derivation/selection paths.
6. The repository self-explanation investigation concludes that knowledge often
   exists but composite operator questions require manual reconstruction across
   structure, concepts, diagnostics, documentation authority, inquiry lineage,
   reachability, and uncertainty.
7. The answer composition visibility investigation concludes that Seed is
   missing answer composition visibility more than answer composition.

## Strongest contradictory evidence

1. Many reviewed surfaces already expose enough boundary text, caveats, and
   unknowns to answer their local questions. A separate architectural pressure
   may overstate the gap.
2. Diagnostic Inventory descriptions sometimes already approximate question
   family and answer responsibility in prose.
3. Documentation navigation, source navigation, component audit, and repository
   investigations may be sufficient for expert maintainers without introducing a
   new named concern.
4. Some surfaces are intentionally simple lookups or mechanical checks; forcing
   answer-composition language onto them would blur useful distinctions.
5. Repository instructions warn not to promote presentation vocabulary into
   preserved knowledge without implementation evidence. `answer composition
   visibility` itself remains an investigation term, not an implemented runtime
   concept.
6. A broad answer-visibility effort could duplicate existing authorities or
   become an accidental proposal for a registry, router, engine, or metadata
   layer, all of which are outside this investigation.

## Candidate boundaries

The architectural pressure exists only within careful boundaries.

In scope:

- characterize existing surfaces that already behave like bounded answer
  compositions;
- distinguish mechanical surface contract from semantic answer contract;
- identify missing question-family, consumed-knowledge, authority, uncertainty,
  and non-authority visibility;
- relate composition visibility to diagnostic visibility and repository
  self-explanation;
- preserve repository authority and implementation evidence.

Out of scope:

- new registry;
- new metadata layer;
- new CLI;
- new schema;
- answer engine;
- router;
- planner;
- runtime behavior;
- cluster mutation;
- claim promotion from diagnostics to cluster truth.

## Relationship to repository self-explanation

Repository self-explanation is the broader pressure. Answer composition
visibility is one possible explanation of why the pressure persists:

```text
Seed has many surfaces that know their mechanics, and several surfaces that
compose bounded answers, but it does not consistently expose which answers those
surfaces are responsible for and what they leave unanswered.
```

This means answer composition visibility is not independent of repository
self-explanation. It is a narrower refinement: repository self-explanation asks
how Seed can explain itself; answer composition visibility asks whether Seed can
identify the bounded answer constructions it already uses to do so.

## Relationship to answer composition visibility investigation

The prior answer composition visibility investigation concluded that Seed is
missing composition visibility more than composition. This investigation refines
that conclusion:

```text
composition visibility is probably not a new branch separate from existing
self-knowledge; it is the semantic continuation of diagnostic and projection
surface self-knowledge.
```

The prior investigation's proposed fields--question family, consumed knowledge,
authority boundaries, uncertainty, and output responsibilities--fit naturally as
answer-level counterparts to Diagnostic Inventory's mechanical fields.

## Determination

Answer composition visibility is best understood as:

```text
a continuation of surface self-knowledge
```

with a secondary description:

```text
a refinement of diagnostic visibility from mechanical behavior toward semantic
answer responsibility
```

It is not best understood as a brand-new branch or fundamentally different
architectural object. It is also not merely the existing diagnostic system,
because Diagnostic Shape Audit answers what a surface is mechanically, not what
question a surface answers.

The central architectural pressure is therefore:

```text
Seed knows what many operational surfaces are allowed to do, but it only
partially knows what answers those surfaces are responsible for.
```

## Open questions

1. What minimum implementation evidence is required before a surface can be
   called a bounded answer composition rather than a view, summary, or diagnostic?
2. Can answer responsibility remain decentralized in existing module docstrings,
   dataclasses, formatter output, tests, and docs, or does discoverability fail
   without a stronger pattern?
3. Which surfaces need semantic answer visibility, and which should remain purely
   mechanical inventories or simple lookups?
4. How should negative authority be preserved without turning every surface into
   a long conceptual document?
5. Can tests check answer visibility without creating a registry or metadata
   proposal prematurely?
6. Is Operational Story the best exemplar, or is Source Navigation a safer
   smaller exemplar because its non-authority is sharper?
7. How should answer composition visibility relate to repository
   self-explanation without becoming a parallel documentation authority?

## Recommended next architectural question

```text
What is the smallest implementation-backed evidence that a surface owns a
bounded answer responsibility, distinct from merely rendering a view?
```

This keeps the next step architectural and evidentiary. It avoids prematurely
choosing a registry, schema, CLI, metadata layer, or composition engine.

## Files changed

- `docs/answer_composition_self_knowledge_investigation.md`

## LOC changed

- Added one repository-level investigation document.
