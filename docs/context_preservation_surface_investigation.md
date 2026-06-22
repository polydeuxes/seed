---
status: investigation
scope: context preservation across reasoning-space boundaries
created: 2026-06-22
---

# Context Preservation Surface Investigation

## Purpose and boundary

This investigation asks whether current repository self-knowledge surfaces are
better explained as **context-preservation surfaces** than as translation
surfaces alone.

This is an investigation only. It does not implement context systems,
translation systems, navigation, routing, ontology, assistant behavior,
diagnostics, command behavior, persistence, or cluster mutation. Repository
authority remains implementation-backed behavior, tests, executable diagnostics,
and existing repository-visible documents.

The vocabulary in this document is descriptive. It is not promoted into
preserved cluster knowledge or official ontology by being used here.

## Evidence reviewed

Implementation-backed surfaces reviewed:

- `seed_runtime/projection_shape.py`
- `seed_runtime/reasoning_path_audit.py`
- `seed_runtime/selection_path_audit.py`
- `seed_runtime/reference_selection.py`
- `seed_runtime/capability_relationship.py`
- `seed_runtime/component_audit.py`
- `seed_runtime/operational_story.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`

Prior investigations reviewed:

- `docs/translation_surfaces_pattern_investigation.md`
- `docs/reasoning_space_translation_investigation.md`
- `docs/repository_navigation_question_surface_discoverability_investigation.md`
- `docs/observation_space_visibility_investigation.md`
- `docs/repository_shape_coverage_investigation.md`
- `docs/traceability_gap_analysis_investigation.md`
- `docs/projection_self_description_investigation.md`
- `docs/reference_selection_traceability_investigation.md`

## Working distinction

The repository evidence supports separating five nearby ideas:

| Idea | Evidence-backed meaning in this investigation | Not equivalent to |
| --- | --- | --- |
| Translation | Re-expressing evidence from one repository reasoning space in another explanatory shape. | Preservation, because a surface can reformat or route information while losing rationale, alternatives, or boundaries. |
| Context preservation | Keeping the reason, comparison frame, selection pressure, operational boundary, or implementation emergence that makes the translated output interpretable. | Full explanation, because preserved context may be partial or scoped. |
| Explanation | Answering why/how/compared-to-what/what-it-means questions from preserved context. | Navigation, because explanation can occur after the surface is already chosen. |
| Traceability | Following evidence, derivation, selection, reference, or authority links across layers. | Translation, because traceability may stay inside one space. |
| Navigation | Finding the relevant surface, document, command, or next inquiry path. | Context preservation, because a well-routed user can still receive context-poor output. |

The important repository-backed distinction is that translation changes the
shape or reasoning space of evidence, while context preservation carries the
interpretive material that prevents that shape change from becoming a contextless
summary.

## Preserved context types

Current self-knowledge surfaces preserve several recurring kinds of context.
These are descriptive groupings derived from current implementation fields and
prior investigations, not proposed ontology.

| Preserved context type | Surfaces that preserve it | What would be lost without the surface |
| --- | --- | --- |
| Reasoning context | `reasoning_path`, `operational_story`, `capability_relationship`, `diagnostic_shape_audit` | The path from evidence to intermediate and derived conclusions; a user may see a conclusion or pressure without knowing why it exists. |
| Selection context | `selection_path`, `reference_selection`, `operational_story`, pressure-related surfaces | Candidate set, selected item, selection factors, non-selected alternatives, and outcome; a user may see only the chosen focus/reference. |
| Reference context | `reference_selection`, `history_brief`, `impact_audit`, snapshot policy surfaces | The comparison frame, comparable snapshot pairs, alternatives, limits, and authority boundary; a user may see change or impact without knowing compared to what. |
| Operational context | `operational_story`, `capability_relationship`, `ops_brief`, `pressure_audit` | Current focus, pressure, affected subjects, capability constraints, benefit, gaps, impact, and investigation path; a user may see isolated facts without operational meaning. |
| Component context | `component_audit`, operational graph, architecture conformance | Definitions, references, tests, consumers, graph/architecture evidence, overlap, status, and unresolved questions; a name may remain just a token. |
| Projection context | `projection_shape`, projection-related investigations | Consumed inputs, produced outputs, influence/non-influence, stage role, and authority boundary; projected facts may appear without the implementation path that shaped them. |
| Diagnostic governance context | `diagnostic_inventory`, `diagnostic_shape_audit` | Public flags, JSON/record behavior, state/repo use, ledger writes, mutation boundary, and implementation conformance; surfaces may exist without visible operational contract. |
| Authority/boundary context | Almost all reviewed translation-oriented surfaces | Read-only status, recordability, event-ledger behavior, cluster-mutation boundary, unsupported domains, and unknowns; explanatory output may be mistaken for mutation, policy, expectation, or truth promotion. |
| Observation-domain context | `observation_inventory`, `observation_utilization`, `capability_relationship`, `projection_shape`, observation-space investigation | Predicate/provider evidence can be related to observation categories only manually; domain-level coverage, absence, and partiality are not first-class in current implementation. |

## Surface-by-surface assessment

### `reasoning_path`

`reasoning_path` translates diagnostic and operational evidence into derivation
visibility, but its usefulness is not merely that it crosses spaces. It preserves
why a conclusion exists: evidence rows, intermediate conclusions, derived
conclusions, consumers, story impact, unknowns, and a read-only/no-ledger/no-
mutation boundary.

Without that preserved context, a capability need or operational conclusion could
still be reported, but the support chain would be compressed away. The repository
evidence therefore supports `reasoning_path` as both a translation surface and a
context-preservation surface.

### `selection_path`

`selection_path` translates pressure candidates and operational story focus into
selection visibility. The important preserved context is the candidate set,
selection factors, non-selected candidates, evidence, outcome, unknowns, and
read-only boundary.

Without it, the selected focus could be visible but the reason it was selected
over alternatives would be absent. This is a context-loss failure rather than a
simple absence of translation.

### `reference_selection`

`reference_selection` translates history impact and snapshot-policy evidence into
comparison-reference visibility. It preserves the selected reference, rationale,
alternatives, known limitations, authority boundary, ledger/mutation boundary,
and unsupported-domain unknowns.

Without it, comparison output can still exist, but the comparison frame becomes
implicit. That makes this surface one of the clearest examples where preserved
context explains why the translation is useful.

### `capability_relationship`

`capability_relationship` translates capability-need pressure and current access
guidance into an operational relationship. It preserves current access,
operational benefit, pressure, unknown attainability, unknown expectation,
reasoning, known limitations, and a read-only/non-mutating boundary.

The preserved context prevents a capability need from collapsing into acquisition
guidance or operator expectation. Its value is therefore boundary-preserving as
much as translation-oriented.

### `projection_shape`

`projection_shape` translates implementation-backed projection stages into an
interpretable projection-flow shape. It preserves consumes, produces,
influences, does-not-influence, authority boundary, and implementation-backed
confidence.

Without this context, projection could be described only by final read models or
facts. The surface preserves how projection behavior emerges from implementation,
including what does not influence event ledger or observed facts.

### `component_audit`

`component_audit` translates a component name into a repository evidence bundle.
It preserves definitions, references, tests, consumers, operational graph
membership, architecture evidence, overlap, status, unresolved questions, and
read-only boundaries.

Without this surface, the repository may still contain all source references, but
the component's role context is distributed and expensive to reconstruct. This is
significant context preservation with a comparatively local translation: much of
the evidence stays within repository-implementation space, but its relationship
to the named component is preserved.

### `operational_story`

`operational_story` composes pressure, capability, privilege, correlation,
impact, and investigation-path evidence into a narrative. It preserves current
focus, pressure, supporting evidence, capabilities, constraints, correlation
gaps, impact, recent changes, observed outcomes, investigation path, unknowns,
and a read-only/no-record/no-ledger/no-mutation boundary.

The useful pattern is not only movement from many surfaces to one story. It is
preservation of enough surrounding operational context for the story to remain
interpretable and bounded.

### `diagnostic_inventory` and `diagnostic_shape_audit`

`diagnostic_inventory` is partly a registry and partly a context-preservation
surface. It preserves the operational contract around diagnostic surfaces: flags,
state/repo-file use, JSON and record support, emitted fact scope, event-ledger
writes, mutation behavior, and descriptions.

`diagnostic_shape_audit` translates that registry context into implementation-
conformance visibility. It preserves whether the declared shape is checked
against files, expected functions, CLI flags, and markers.

Together they show that operational visibility is not just a list of commands. It
is a preserved contract between public diagnostic surface, implementation shape,
recording behavior, ledger writes, and cluster mutation boundary.

## Translation versus context preservation

Repository evidence supports this refinement:

```text
translation is the motion between reasoning spaces
context preservation is what makes the motion intelligible and safe
```

Translation alone explains why surfaces have different input and output spaces.
It does not fully explain why these surfaces are useful. Their usefulness usually
comes from preserved context:

- `reasoning_path` is useful because it preserves the support chain, not because
  it merely emits a different schema.
- `selection_path` is useful because it preserves alternatives and selection
  factors, not because it merely reports the selected result.
- `reference_selection` is useful because it preserves the comparison frame, not
  because it merely names a reference.
- `capability_relationship` is useful because it preserves access/benefit/
  pressure while keeping attainability and expectation unknown.
- `projection_shape` is useful because it preserves implementation emergence and
  non-influence boundaries, not because it merely summarizes projection.
- `diagnostic_inventory` and `diagnostic_shape_audit` are useful because they
  preserve the operational contract and conformance relation.

This makes context preservation a stronger explanation for the usefulness of
translation-oriented surfaces. It is not a replacement for translation: the
stronger repository-backed pattern is **context-preserving translation**.

## Shared surface characteristics

The reviewed surfaces repeatedly share these characteristics:

1. **They are read-only or explicitly bounded.** They usually report no fact
   recording, no event-ledger writes, and no cluster mutation, or they inventory
   those properties.
2. **They preserve unknowns and limitations.** Unsupported domains or missing
   implementation evidence are represented as unknown/limited rather than filled
   in by prose.
3. **They preserve a relation, not just a value.** Evidence-to-conclusion,
   candidate-to-selection, reference-to-comparison, capability-to-benefit,
   stage-to-output, registry-to-implementation, and component-to-consumers are
   relation shapes.
4. **They make hidden comparison frames explicit.** This includes alternatives,
   non-selected candidates, does-not-influence lists, authority boundaries, and
   operational limitations.
5. **They avoid turning diagnostic findings into cluster truth.** The surfaces
   are explanatory and diagnostic; they do not silently promote findings into
   host, service, filesystem, or runtime truth.
6. **They are scoped.** The preservation is useful because it names boundaries:
   implemented domains, supported targets, history-only reference selection,
   query-driven components, projection-only shape, and registered diagnostics.

## Discoverability failures as context-loss failures

Prior discoverability work can be reinterpreted cautiously through this lens.
Some failures are not merely that a worker does not know which surface exists.
They are that the worker lacks the preserved context needed to select, trust, or
use the surface:

- A worker can know `operational_story` exists but still need `reasoning_path` to
  preserve why a conclusion exists.
- A worker can see a current focus but need `selection_path` to preserve why that
  focus won over alternatives.
- A worker can read a history comparison but need `reference_selection` to
  preserve the comparison frame.
- A worker can inspect predicate/provider inventory but still lack preserved
  observation-domain context, as shown by the observation-space investigation.
- A worker can find a diagnostic command but still need diagnostic inventory and
  shape audit context to know recording, ledger, mutation, and implementation
  conformance boundaries.

This supports the hypothesis that some discoverability gaps are context-loss
gaps. It does not prove all discoverability gaps are context-loss gaps; some are
ordinary navigation or naming problems.

## Counterexamples and limits

### Translation with little context preserved

- Raw current-state views and simple fact listings can translate stored state
  into readable output while preserving little rationale, selection history,
  alternatives, or authority context. They may be useful reports, but they are
  weaker evidence for context-preserving translation.
- `diagnostic_inventory` can be used as a list of diagnostic surfaces. In that
  usage it translates implementation-facing surface names into public names, but
  the context-preservation strength appears only when record behavior, ledger
  writes, mutation boundary, and emitted-fact scope are considered.
- `observation_inventory` and `observation_utilization` translate provider and
  predicate implementation into visibility/use information, but the observation-
  space investigation shows they do not preserve complete domain-level context.
  This is a direct example of translation occurring while important context is
  still lost.

### Significant context preserved without substantial translation

- `component_audit` often stays largely inside implementation evidence space,
  yet it preserves strong component context by collecting definitions,
  references, tests, consumers, graph/architecture evidence, and unresolved
  questions around one named component.
- Diagnostic registry entries preserve operational contract context even before
  `diagnostic_shape_audit` compares them to implementation specs. The registry
  itself is not always a cross-space translator, but it preserves recordability,
  ledger, mutation, JSON, and emitted-fact context.
- Investigation documents can preserve inquiry context, boundaries, and open
  questions without being executable translation surfaces. They are weaker
  implementation authority than code/tests, but they are evidence that context
  preservation can occur in documentation without substantial runtime
  translation.

These counterexamples matter. They show that translation and context
preservation are related but not identical.

## Supported conclusions

1. **Current self-knowledge surfaces preserve multiple context types.** The
   clearest types are reasoning, selection, reference, operational, component,
   projection, diagnostic-governance, authority/boundary, and partial
   observation-domain context.
2. **Context preservation is a stronger explanation for usefulness than
   translation alone.** Translation explains motion between spaces; preserved
   context explains why the translated output remains interpretable, safe, and
   actionable as repository self-knowledge.
3. **The strongest supported pattern is context-preserving translation.** The
   repository evidence does not require choosing only translation or only
   preservation. Useful surfaces often do both.
4. **Different surfaces preserve different kinds of context.** The repository
   evidence separates derivation, selection, reference, operational, component,
   projection, and governance contexts rather than collapsing them into one
   explanation layer.
5. **Some discoverability failures are context-loss failures.** Observation-
   domain visibility is the clearest current case: predicate/provider evidence
   exists, but domain-level context is not implementation-backed as a first-class
   surface.
6. **Authority and unknown preservation are core to the pattern.** The repeated
   read-only, ledger, mutation, unsupported-domain, and unknown fields prevent
   explanatory surfaces from silently becoming cluster truth or policy.

## Unsupported conclusions

The evidence does **not** support these stronger claims:

- That Seed has or needs a general context-preservation framework.
- That “context preservation surface” is official ontology or preserved cluster
  vocabulary.
- That every translation surface should become a diagnostic or command.
- That all useful repository views are translation or context-preservation
  surfaces.
- That context preservation replaces traceability, explanation, or navigation.
- That observation-domain context should be implemented now.
- That preserved diagnostic context should be attached directly to hosts,
  services, filesystems, runtime entities, or other cluster truth by default.
- That any reviewed surface changes operator intent, deployment expectation,
  acquisition guidance, policy, or mutation behavior.

## Open questions

- What minimum evidence should be required before calling a surface context-
  preserving: explicit unknowns, alternatives, authority boundaries, tests,
  inventory registration, or implementation-backed relationships?
- Are there existing surfaces with strong preserved context that have not been
  recognized because they do not cross reasoning-space boundaries dramatically?
- Is observation-domain coverage missing a context-preserving translation, or can
  predicate/provider surfaces preserve enough context through incremental growth?
- Should future investigations prefer feature-specific language until runtime
  implementation centralizes this pattern?
- How much context can documentation preserve before executable surfaces are
  needed to prevent drift?

## Acceptance answers

### What context do current self-knowledge surfaces preserve?

They preserve reasoning paths, selection rationale, comparison references,
operational pressure and constraints, component role evidence, projection-stage
emergence, diagnostic governance contracts, authority boundaries, unknowns, and
partial observation-domain evidence.

### Is context preservation a stronger explanation than translation alone?

Yes, for usefulness. Translation explains how evidence moves between reasoning
spaces. Context preservation explains why the translated output can be
interpreted correctly and why it does not overclaim authority, mutation, policy,
expectation, or cluster truth.

### Why are some translations useful while others are not?

Useful translations preserve the context that would otherwise be lost: why a
conclusion exists, why a choice was made, compared to what, what alternatives
were rejected, what capability pressure means, how implementation behavior
emerges, what boundary applies, and what remains unknown. Less useful
translations may expose values or summaries without rationale, alternatives,
limits, or authority context.

### Are recent findings pointing at context preservation as a deeper pattern?

Partially yes. Translation, discoverability, observation-domain, and traceability
findings appear to converge on a deeper context-preservation pressure. The most
supported formulation is not that context preservation replaces translation,
traceability, explanation, or navigation, but that current useful self-knowledge
surfaces often operate as context-preserving translations across reasoning-space
boundaries.
