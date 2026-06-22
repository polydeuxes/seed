---
status: investigation
scope: reasoning-space translation as repository evidence
created: 2026-06-22
---

# Reasoning Space Translation Investigation

## Purpose and boundary

This investigation asks whether recent discoverability and observation-space
findings point to a reusable pattern: Seed often has multiple reasoning spaces,
and workers may need translation between those spaces rather than simply more
knowledge inside one space.

This is an understanding document only. It does not implement routing,
navigation, assistants, recommendation systems, ontology changes, command
behavior, diagnostics, new surfaces, persistence, or cluster mutation.
Repository authority remains implementation, tests, executable diagnostics, and
existing repository-visible documents.

## Evidence reviewed

Primary evidence reviewed:

- `docs/repository_navigation_question_surface_discoverability_investigation.md`
- `docs/observation_space_visibility_investigation.md`
- `docs/repository_shape_coverage_investigation.md`
- `docs/traceability_gap_analysis_investigation.md`
- `docs/projection_self_description_investigation.md`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `seed_runtime/projection_shape.py`
- `seed_runtime/reasoning_path_audit.py`
- `seed_runtime/selection_path_audit.py`
- `seed_runtime/reference_selection.py`
- `seed_runtime/capability_relationship.py`
- `seed_runtime/operational_story.py`
- `seed_runtime/component_audit.py`
- tests for diagnostic inventory, diagnostic shape audit, projection shape,
  reasoning path, selection path, reference selection, capability relationship,
  operational story, and component audit.

Prior investigations are treated as evidence of recurring repository pressure
and worker reasoning style. Implementation and tests are stronger authority than
investigation vocabulary.

## Central finding

Yes, repository evidence supports the hypothesis that a meaningful part of the
current discoverability gap is a **translation gap between reasoning spaces**.

The stronger statement is:

```text
Seed exposes many reasoning spaces individually.
Seed also contains several surfaces that already translate between spaces.
Workers still often perform the first translation manually: turning a natural
question into the repository unit, surface, authority boundary, and follow-up
space that can answer it.
```

This does not prove that Seed has a general translation layer. It supports a
narrower conclusion: translation behavior already exists implicitly in scoped
surfaces such as `operational_story`, `reasoning_path`, `selection_path`,
`reference_selection`, `capability_relationship`, `component_audit`,
`projection_shape`, `diagnostic_inventory`, and `diagnostic_shape_audit`.

## Identified reasoning spaces

The following spaces are repository-visible. The names are descriptive for this
investigation, not proposed ontology.

| Reasoning space | Repository evidence | What is visible | Boundary |
| --- | --- | --- | --- |
| Diagnostic surface space | `diagnostic_inventory`, `diagnostic_shape_audit` | Surface names, CLI flags, JSON/record support, state/repo-file use, event-ledger behavior, mutation boundary, implementation-shape checks | Strong for registered diagnostics; not a full repository ontology |
| Surface space | diagnostic inventory, operational surface inventory, docs map | Which operational/documentation surfaces exist and what family they answer | Workers still choose among multiple inventories and docs |
| Projection space | `projection_shape` | Projection stages, consumed inputs, produced outputs, influence/non-influence, authority boundary | Projection mechanics only, not all interpretation of projected truth |
| Fact/claim/support space | fact views, projection shape, current-fact/support/conflict behavior | Supported facts, conflicts, current selection, provenance mechanisms | Distributed; no single general claim-shape surface |
| Predicate space | observation inventory/utilization, predicate catalog, projection shape | Predicate sources, use, catalog participation, projection influence | Predicate coverage is stronger than observation-domain coverage |
| Observation/provider space | observation inventory, provider collection classes, observation-space investigation | Providers and predicate-yielding observation sources | Domain coverage is inferred rather than first-class |
| Observation-domain/domain space | observation-space investigation, repository shape coverage | Candidate groupings such as runtime, filesystem, diagnostics, history, relationships | Mostly investigative/descriptive; not an implemented domain inventory |
| Capability space | `capability_needs`, `capability_relationship`, privilege discovery | Needed capability, current access, operational benefit, pressure, attainability/expectation unknowns | Does not recommend acquisition or infer operator expectations |
| Component space | `component_audit`, operational graph, architecture conformance | Definitions, references, tests, consumers, graph/architecture evidence, unresolved questions | Query-driven per component; not a complete component catalog |
| Operational pressure/story space | `pressure_audit`, `operational_story`, `ops_brief`, history/impact surfaces | Current focus, pressure candidates, evidence, capability constraints, impact, investigation path | Operational narrative, not universal prioritization |
| Reasoning/derivation space | `reasoning_path` | Evidence, intermediate conclusions, derived conclusions, consumers, story impact, unknowns | Scoped to implemented diagnostic surfaces |
| Selection space | `selection_path`, `reference_selection`, context selection code/tests | Candidates, selected result, factors, alternatives, outcome, selected reference | Scoped targets/domains return explicit unknowns when unsupported |
| Reference/comparison space | `reference_selection`, `history_brief`, `impact_audit`, snapshot policy | Comparison reference, rationale, alternatives, limitations, authority boundary | History is implementation-backed; other domains are unsupported |
| Question space | repository navigation investigation, docs navigation, worker question clusters | Natural question families and possible answering surfaces | Descriptive only; no current command routes questions |
| Authority/boundary space | diagnostic inventory, projection shape, reference selection, capability relationship | Read-only status, recording scope, event-ledger writes, cluster mutation, authority limits | Repeated field pattern, not a centralized authority graph |

The evidence therefore supports that multiple reasoning spaces are emerging as a
repository concept, but mostly through repeated implementation shapes and
investigation language rather than a single named runtime model.

## Existing translation surfaces

Several current surfaces naturally translate between spaces. They are not
labeled as translation layers, but their inputs and outputs cross reasoning-space
boundaries.

| Surface | Translation performed | Evidence-based interpretation |
| --- | --- | --- |
| `operational_story` | pressure/capability/privilege/correlation/impact/investigation-path spaces -> operational story space | Composes current operational evidence into focus, pressure, constraints, impact, recent changes, observed outcomes, investigation path, unknowns, and read-only boundary. |
| `reasoning_path` | evidence/diagnostic output space -> derivation space -> consumer/story-impact space | Builds an explanation chain from implemented diagnostic evidence through intermediate and derived conclusions to consumers and operational story impact. |
| `selection_path` | pressure candidate space -> selection space -> outcome space | Converts candidate pressures and story focus into selected result, candidate set, selection factors, non-selected candidates, evidence, outcome, and unknowns. |
| `reference_selection` | history/impact/snapshot-policy space -> reference/comparison space | Converts snapshot and impact evidence into selected comparison reference, rationale, alternatives, limitations, and authority boundary for history. |
| `capability_relationship` | capability need/privilege/pressure space -> capability relationship space | Connects needed capability to current access, operational benefit, pressure, reasoning, limitations, and unknown attainability/expectation. |
| `projection_shape` | implementation/projection stage space -> projection interpretation space | Translates projection code structure into stages, consumes, produces, influence, non-influence, and authority boundaries. |
| `component_audit` | source/reference/test/graph/architecture spaces -> component role space | Collects implementation evidence around a named component and reports role, definitions, references, tests, consumers, graph/architecture evidence, and unresolved questions. |
| `diagnostic_inventory` | implementation-facing operational surfaces -> public surface space | Declares public operational diagnostic shape, flags, record behavior, ledger writes, cluster mutation, and descriptions. |
| `diagnostic_shape_audit` | registry surface space -> implementation spec space | Checks whether registered diagnostic shape agrees with implementation markers and expected functions. |
| `docs/README.md` | document corpus space -> documentation navigation space | Routes readers to owning investigation documents without restating their full answers. |

These surfaces demonstrate existing translation behavior. The recurring pattern is
not “answer a question directly”; it is “reinterpret evidence from one repository
unit into another repository unit while preserving boundary and unknowns.”

## Manual translations currently performed by workers

Workers still perform several translations manually before Seed surfaces become
useful:

1. **Question phrase -> repository unit.** “What are we missing?” must be mapped
   manually to missing capability, evidence, observation domain, relationship,
   implementation, documentation, authority, or reference.
2. **Question phrase -> surface family.** “What is this about?” must be mapped to
   component role, operational pressure, observation domain, reasoning path,
   selection rationale, reference choice, or authority boundary.
3. **Surface family -> exact command/surface.** The worker often must know that
   derivation means `reasoning_path`, selection means `selection_path`, current
   narrative means `operational_story`, comparison reference means
   `reference_selection`, and registry consistency means `diagnostic_shape_audit`.
4. **Vocabulary -> authority boundary.** Workers must decide whether a term is an
   implemented repository concept, a diagnostic presentation label, or an
   investigation-only grouping.
5. **Predicate/provider/capability -> observation-domain coverage.** Existing
   predicate, provider, and capability evidence can support domain reasoning, but
   the domain translation is mostly performed by investigation prose rather than
   by an executable first-class domain surface.
6. **Answering surface -> follow-up surface.** After one surface answers part of
   a question, workers infer the next space manually: component to consumer,
   derivation to selection, selection to reference, pressure to capability, or
   projection to fact support.

This supports the observation that Seed may have the answering surface while
workers do not know which surface corresponds to the question being asked.

## Reusable translation patterns from repository evidence

### 1. Registry-to-implementation translation

`diagnostic_inventory` declares the public surface contract, while
`diagnostic_shape_audit` checks implementation specs. This translates between
public diagnostic identity and implementation evidence.

Pattern:

```text
surface declaration -> implementation marker -> mismatch/ok/unknown status
```

This is the strongest implemented translation pattern because it is registry
backed, audited, and tested.

### 2. Composition translation

`operational_story` composes pressure, capability, privilege, correlation,
impact, and investigation path into an operational narrative.

Pattern:

```text
many specialized diagnostics -> one narrative surface -> preserved unknowns and boundary
```

This is translation, not routing: it does not decide what a worker should ask; it
re-expresses current operational evidence as story.

### 3. Explanation-layer translation

`reasoning_path`, `selection_path`, and `reference_selection` expose distinct
explanatory layers:

```text
derivation: why a conclusion exists
selection: why this candidate/result was chosen
reference: compared to what
```

The repository evidence separates these layers. A complete explanation may need
more than one of them, and lack of one layer can be a traceability gap even when
another layer exists.

### 4. Capability-pressure translation

`capability_relationship` connects missing/needed capability language to current
access, operational benefit, pressure, reasoning, and limitations.

Pattern:

```text
capability need -> access/benefit/pressure relationship -> explicit unknowns
```

This helps explain generic “missing” questions when the missing item is a
capability, but it does not cover missing evidence, missing domain coverage, or
missing documentation by itself.

### 5. Implementation-role translation

`component_audit` turns source references, tests, graph evidence, and architecture
evidence into a component-role answer.

Pattern:

```text
name or component term -> repository evidence bundle -> role/status/unresolved questions
```

This pattern is useful for “what is this about?” questions, but only after the
worker has selected component space as the right interpretation.

### 6. Flow-shape translation

`projection_shape` translates implementation-backed projection mechanics into a
readable flow of stages, consumed inputs, produced outputs, influence,
non-influence, and authority boundary.

Pattern:

```text
projection implementation -> stage/flow vocabulary -> positive and negative influence
```

This explains how observations and facts move through projection, but it does not
make observation-domain coverage first-class.

### 7. Preservation-to-navigation translation

Repository navigation investigations distinguish having preserved facts from
being able to navigate to the right surface or source artifact.

Pattern:

```text
answer exists somewhere -> worker lacks surface/unit vocabulary -> navigation or translation gap
```

This is currently more investigative than executable, but it recurs across source
navigation, question-to-surface discoverability, and observation-space findings.

## Are discoverability gaps actually translation gaps?

Partially, yes.

The evidence supports a translation-gap reading when:

- multiple current surfaces can answer different interpretations of the same
  natural-language question;
- the repository unit must be chosen before the answer surface is obvious;
- existing surfaces expose their own scope clearly after selection;
- missingness can mean capability, evidence, observation-domain coverage,
  relationship, implementation, documentation, reference, or authority;
- current evidence exists in one space but must be re-expressed in another space
  to answer the worker's question.

The evidence does not support reducing all discoverability gaps to translation.
Some gaps remain ordinary missing knowledge or missing shape, especially where no
implementation-backed surface exists, where observation-domain coverage is only
investigative, or where a target/domain returns explicit unknowns.

## Supported conclusions

- Seed already exposes multiple reasoning spaces through implementation-backed
  surfaces and investigation documents.
- Seed already contains implicit translation behavior in scoped surfaces.
- Workers currently translate natural questions into repository units and
  surface families manually.
- Current discoverability problems are often translation problems: the answer may
  exist, but the worker must know which reasoning space and surface to use.
- Observation-domain visibility is a strong example of translation pressure:
  predicate/provider/capability evidence exists, but domain coverage is not
  first-class.
- Translation between spaces is becoming a missing form of repository
  self-knowledge in the limited sense that relationships among spaces are less
  visible than the spaces themselves.

## Unsupported conclusions

- Seed has a general reasoning-space translation layer.
- Every worker question can be routed to a surface from current repository
  evidence.
- The reasoning-space list in this document is complete or authoritative.
- Observation domains are implemented repository ontology.
- Translation should be solved with routing, assistants, recommendation systems,
  or new navigation behavior.
- Existing translation surfaces create cluster truth, accepted baselines,
  acquisition policy, operator expectations, or mutation authority.

## Open questions

- Which reasoning-space names are implementation-backed enough to preserve as
  repository vocabulary, and which are only investigation shorthand?
- Can observation-domain coverage be evidenced without promoting a premature
  domain taxonomy?
- Are relationships among `reasoning_path`, `selection_path`, and
  `reference_selection` merely a traceability cluster, or evidence of a broader
  explanation-layer family?
- How often do worker questions fail because a surface is absent versus because a
  surface-space translation is absent?
- Which existing surfaces already provide enough follow-up hints to reduce manual
  translation, and which only describe themselves after selection?
- Is authority/boundary translation a separate recurring layer, or a field
  pattern repeated across diagnostics?

## Acceptance answers

### Are discoverability problems actually translation problems?

Often, but not always. Repository evidence supports that many discoverability
failures occur when workers must translate a natural question into the correct
repository unit, surface family, and authority boundary. Some failures remain
ordinary missing implementation, missing evidence, or unsupported target/domain
cases.

### Does Seed already contain translation behavior?

Yes. `operational_story`, `reasoning_path`, `selection_path`,
`reference_selection`, `capability_relationship`, `component_audit`,
`projection_shape`, `diagnostic_inventory`, and `diagnostic_shape_audit` all
translate evidence from one repository reasoning space into another scoped
answer shape.

### Are multiple reasoning spaces emerging as a repository concept?

Yes, with caution. Multiple spaces are visible through repeated implementation
patterns and repository investigations. They are not yet a single implemented
ontology or complete runtime model.

### Is translation between spaces becoming a missing form of repository self-knowledge?

Yes, as an investigation conclusion. Seed's individual spaces are often more
visible than the relationships among those spaces. The missing self-knowledge is
not simply more facts; it is often the reusable ability to explain how a question,
surface, capability, predicate, observation domain, component, reference,
selection, or operational pressure corresponds to another reasoning space.
