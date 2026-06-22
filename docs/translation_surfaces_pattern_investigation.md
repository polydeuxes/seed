# Translation Surfaces Pattern Investigation

## Purpose and boundary

This investigation asks whether current repository self-knowledge surfaces are
best understood as a recurring **translation surface** pattern: an implemented,
read-only surface that turns one reasoning space into another explanatory space
without adding new routing, navigation, ontology, assistant behavior, or cluster
mutation.

This document is investigative only. It does not implement a new diagnostic,
add a reasoning space, recommend command routing, create navigation layers,
automate question selection, or promote presentation vocabulary into repository
knowledge. Repository authority remains implementation-backed behavior and the
existing investigations cited below.

## Evidence reviewed

Primary implementation evidence reviewed:

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

- `docs/reasoning_space_translation_investigation.md`
- `docs/repository_navigation_question_surface_discoverability_investigation.md`
- `docs/observation_space_visibility_investigation.md`
- `docs/repository_shape_coverage_investigation.md`

## Working definition

A **translation surface** is an implemented repository surface that:

1. Accepts or reconstructs evidence from one reasoning space.
2. Emits a different explanatory shape intended for interpretation.
3. Preserves unknowns, limitations, or unsupported domains instead of filling
   gaps silently.
4. States authority or mutation boundaries, especially read-only behavior.
5. Does not make the translated output cluster truth merely by reporting it.
6. Is more than a raw view: it names relationships such as consumes/produces,
   evidence/conclusion, candidate/selected, need/benefit, or registry/spec.

This definition is descriptive, not a new ontology. It is derived from current
implementation patterns rather than imposed as a new architecture.

## Candidate translation surfaces

| Surface | Classification | Input reasoning space | Output reasoning space | Evidence summary |
| --- | --- | --- | --- | --- |
| `projection_shape` | `translation_surface` | Projection implementation stages and data dependencies | Projection-flow interpretation with consumes, produces, influence, non-influence, authority boundary, confidence | Stages explicitly encode `consumes`, `produces`, `influences`, `does_not_influence`, and `authority_boundary`; the surface is read-only and non-mutating. |
| `reasoning_path` | `translation_surface` | Diagnostic evidence, capability needs, pressure, privilege, operational story | Derivation explanation: evidence, intermediate conclusions, derived conclusions, consumers, story impact, unknowns | It builds only from implemented diagnostic surfaces and emits derivation fields plus a read-only no-record/no-ledger/no-mutation boundary. |
| `selection_path` | `translation_surface` | Pressure candidates and operational story focus | Selection explanation: selected item, candidate set, selection factors, non-selected candidates, evidence, outcome, unknowns | It explains implemented selection evidence without changing selection behavior and preserves unknowns for unsupported targets. |
| `reference_selection` | `translation_surface` | Impact snapshots and snapshot policy evidence | Comparison-reference explanation: selected reference, rationale, alternatives, authority boundary, limitations | It maps history comparison evidence to selected/alternative references and reports unsupported domains as unknown. |
| `capability_relationship` | `translation_surface` | Capability need pressure and current access guidance | Operational relationship: current access, benefit, pressure, unknown attainability/expectation, reasoning, limitations | It explains capability/access/pressure relationships without acquisition logic and keeps attainability and expectation unknown. |
| `component_audit` | `translation_surface` | Source files, references, tests, consumers, operational graph, architecture paths | Component-role interpretation: status, definitions, references, tests, consumers, graph evidence, overlap, unresolved questions | It scans repository evidence and classifies component status while retaining unresolved questions and read-only boundaries. |
| `operational_story` | `translation_surface` | Pressure, capability, privilege, correlation, impact, and investigation-path surfaces | Current operational narrative: focus, pressure, evidence, constraints, gaps, impact, recent changes, outcomes, unknowns | It composes current operational evidence into a story without planning, recording, or mutation. |
| `diagnostic_inventory` | `partially_translation_oriented` | Registry declarations of operational CLI surfaces | Public diagnostic contract: flags, state/repo use, JSON/record behavior, emitted facts, ledger/mutation boundary, descriptions | It is primarily a registry, but translates implementation-facing surface identity into public operational shape. |
| `diagnostic_shape_audit` | `translation_surface` | Diagnostic inventory and implementation specs/files | Registry-to-implementation conformance explanation with match/mismatch status | It checks registered surfaces against expected functions, markers, CLI flags, and implementation files. |
| `observation_inventory` / `observation_utilization` | `partially_translation_oriented` | Observation providers, predicates, projection/read/diagnostic usage | Predicate/provider visibility and utilization explanation | Prior investigation found these reason at predicate level, not domain level; they translate implementation evidence into visibility but not complete domain reasoning. |
| Raw fact/read-model views | `non_translation_surface` | Projected cluster state | Reported current facts or view rows | They can be inputs to translation surfaces, but by themselves they usually present state rather than translate between reasoning spaces. |
| Unsupported or absent domain commands | `unknown` or `non_translation_surface` | None or insufficient implementation evidence | Unknown | Repository authority does not support classification without implemented evidence. |

## Shared characteristics

### 1. Input and output spaces are distinct

The strongest candidates do not merely display the same data in another format.
They convert one kind of evidence into another explanatory role:

- `projection_shape`: implementation mechanics -> projection-flow
  interpretation.
- `reasoning_path`: evidence and composed diagnostics -> derivation path.
- `selection_path`: candidate pressure ordering -> selection explanation.
- `reference_selection`: history/snapshot evidence -> comparison reference.
- `capability_relationship`: capability pressure -> operational meaning and
  boundary.
- `component_audit`: source/repository evidence -> component role.
- `operational_story`: multiple diagnostic outputs -> current operational
  narrative.
- `diagnostic_shape_audit`: registry/spec evidence -> conformance status.

This input/output split is stronger than a generic “view” explanation because
these surfaces name the transformation relationship: consumes/produces,
evidence/conclusion, candidate/selected, selected/alternative reference,
need/access/benefit, definition/consumer/status, or registry/spec.

### 2. Unknowns and limitations are preserved

Translation surfaces generally avoid silently completing absent evidence:

- `reasoning_path` emits `unknowns` when no derivation evidence exists.
- `selection_path` returns `selected="unknown"` and explains unsupported
  selection targets.
- `reference_selection` reports unsupported domains and history limitations.
- `capability_relationship` keeps attainability and expectation `unknown`.
- `component_audit` reports unresolved questions.
- `operational_story` reports pressure, capability, and impact unknowns.

This preservation of unknowns is important because translated explanations can
look authoritative. Current implementations usually counter that risk by
including explicit gaps.

### 3. Authority and mutation boundaries recur

The candidate surfaces repeatedly state read-only or non-mutating behavior:

- `projection_shape` has a boundary with `read_only=True`,
  `writes_event_ledger=False`, and `mutates_cluster=False`.
- `reasoning_path` and `selection_path` default to no recording, no event-ledger
  writes, and no cluster mutation.
- `reference_selection` exposes event-ledger and cluster mutation booleans.
- `capability_relationship`, `component_audit`, and `operational_story` report
  read-only/non-mutating boundaries.
- `diagnostic_inventory` records whether surfaces support recording, emit
  diagnostic or cluster facts, write the ledger, mutate the cluster, or read
  diagnostic facts.

That repeated boundary vocabulary supports the pattern: translation output is
explanatory repository self-knowledge, not automatic operational truth.

### 4. Explanation orientation is stronger than reporting orientation

The translation candidates answer “why/how/compared to what/what does this mean”
questions more than simple “what rows exist” questions:

- Why does a conclusion exist? `reasoning_path`.
- Why was this selected? `selection_path`.
- Compared to what? `reference_selection`.
- What does a capability need mean operationally? `capability_relationship`.
- How does projection flow? `projection_shape`.
- What role does this component play? `component_audit`.
- What is the current operational story? `operational_story`.
- Does public diagnostic shape agree with implementation? `diagnostic_shape_audit`.

This is the strongest evidence that “translation surface” is an architectural
role already present in implementation, not merely a feature-specific label.

## Independent emergence

The pattern appears to have emerged independently across several families:

1. **Projection family**: `projection_shape` explains implementation-backed
   projection stages and authority boundaries.
2. **Traceability family**: `reasoning_path`, `selection_path`, and
   `reference_selection` expose derivation, selection, and comparison-reference
   layers.
3. **Operational family**: `operational_story` and `capability_relationship`
   compose pressure, capability, access, constraints, gaps, and narrative.
4. **Repository implementation family**: `component_audit` reconstructs a
   component role from definitions, references, tests, consumers, graph, and
   architecture evidence.
5. **Diagnostic governance family**: `diagnostic_inventory` and
   `diagnostic_shape_audit` map public diagnostic contracts to implementation
   shape and conformance.

The families have different feature origins, inputs, and output schemas. The
recurring shape therefore does not appear to be only a naming convention or one
shared helper module. It is a repeated architectural role: repository evidence is
translated into bounded explanatory self-knowledge.

## Counterexamples and limits

Not every surface is a translation surface.

- Raw current-state views, fact listings, and simple summaries can be valuable
  without translating between reasoning spaces.
- `diagnostic_inventory` is only partially translation-oriented because it is
  mostly a declaration registry. It becomes translation-like when used as public
  operational shape for implementation-facing surfaces.
- `observation_inventory` and `observation_utilization` translate provider and
  predicate implementation into visibility/use information, but prior evidence
  shows they do not yet translate predicate evidence into complete
  observation-domain coverage.
- Prior investigations explicitly warn that presentation vocabulary should not
  automatically become repository knowledge. The term “translation surface” is
  therefore a useful descriptive lens only where implementation evidence shows
  an input/output explanatory transformation.

## Relationship to earlier findings

### `reasoning_space_translation_investigation`

This earlier investigation is the most direct predecessor. It already described
surfaces such as `projection_shape`, `component_audit`, `diagnostic_inventory`,
and `diagnostic_shape_audit` as moving between implementation/projection,
source/component, implementation/public surface, and registry/spec spaces. The
current investigation strengthens that finding by classifying translation as a
repeated surface role rather than a one-off reasoning-space observation.

### `repository_navigation_question_surface_discoverability_investigation`

The discoverability investigation asked which surfaces answer which question
shapes. From the translation-surface lens, many “question-to-surface” mappings
are not routing primitives; they are evidence that different questions require a
translation layer. For example, “why this conclusion,” “why this selection,”
“compared to what,” and “what does this capability pressure mean” map to
implemented surfaces because each surface translates raw or composed evidence
into an explanatory space.

### `observation_space_visibility_investigation`

The observation-space investigation found that Seed can reason about providers,
predicates, capability needs, and projection influence, but not first-class
observation-domain coverage. From the translation-surface lens, that finding is
an example of a missing or incomplete translation surface: predicate/provider
visibility exists, but translation from predicate-level implementation evidence
to domain-level observation coverage is not yet implementation-backed.

### `repository_shape_coverage_investigation`

The shape-coverage investigation classified many domains as shaped or partially
shaped and repeatedly identified surfaces that turn distributed implementation
evidence into repository shape. From the current lens, “shape coverage” and
“translation surface” are adjacent views of the same phenomenon: shape coverage
asks which domains have interpretable repository self-knowledge; translation
surface analysis asks how that self-knowledge is produced from another reasoning
space.

## Supported conclusions

1. **Translation surfaces are emerging as a repository pattern.** Multiple
   implemented surfaces translate one reasoning space into another explanatory
   space while preserving unknowns and boundaries.
2. **Multiple self-knowledge surfaces share a common architectural role.** Their
   feature names differ, but their role is similar: make a hidden relationship
   between evidence spaces visible without mutating repository truth.
3. **Recent discoverability, observation-space, and reasoning-space findings are
   plausibly observing the same phenomenon from different angles.**
   Discoverability observes which questions need translation, observation-space
   work observes where translation is missing, and shape coverage observes where
   translated self-knowledge already exists.
4. **Translation behavior is often a stronger explanation than feature-specific
   behavior.** `reasoning_path`, `selection_path`, `reference_selection`,
   `capability_relationship`, `component_audit`, `projection_shape`,
   `operational_story`, and `diagnostic_shape_audit` are easier to compare when
   treated as evidence-to-explanation translators rather than isolated reports.
5. **Translation is becoming a missing form of repository self-knowledge in some
   areas.** Observation-domain coverage is the clearest example: predicate and
   provider facts exist, but implementation-backed domain-level translation is
   not yet first-class.

## Unsupported conclusions

The evidence does **not** support these stronger claims:

- That Seed has or needs a general translation framework.
- That routing, navigation, assistant behavior, or command recommendation should
  be implemented.
- That “translation surface” is an official ontology term in preserved cluster
  knowledge.
- That all diagnostics are translation surfaces.
- That every partially shaped domain should receive a new translation surface.
- That translated explanations should become cluster facts by default.

## Open questions

- Should future investigations use “translation surface” as a descriptive label,
  or keep using feature-specific terms until implementation centralizes the
  pattern?
- Which existing surfaces are merely reports with boundary fields, and which
  genuinely translate between reasoning spaces?
- Is there a minimal evidence threshold for classifying a surface as a
  translation surface: explicit input/output fields, unknown preservation,
  authority boundary, tests, inventory registration, or all of these?
- Does observation-domain coverage require a translation surface, or can existing
  observation inventory/utilization surfaces grow enough without a new surface?
- Should diagnostic inventory eventually classify translation-oriented surfaces,
  or would that prematurely turn an investigation lens into repository ontology?

## Final answer to acceptance questions

- **Are translation surfaces emerging as a repository pattern?** Yes,
  implementation evidence supports this as an emerging descriptive pattern.
- **Do multiple self-knowledge surfaces share a common architectural role?** Yes,
  several surfaces translate evidence spaces into bounded explanatory spaces.
- **Are recent discoverability, observation-space, and reasoning-space findings
  describing the same phenomenon?** Partially yes. They appear to describe the
  same phenomenon from different angles: question discoverability, missing
  observation-domain translation, and reasoning-space translation.
- **Is translation becoming a missing form of repository self-knowledge?** Yes in
  selected areas, especially observation-domain coverage, but this conclusion is
  investigative and does not imply implementation work by itself.
