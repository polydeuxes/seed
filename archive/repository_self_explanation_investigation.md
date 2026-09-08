---
title: Repository Self-Explanation Investigation
status: investigation
authority: architecture-focused investigation only; not reconciliation, implementation proposal, CLI proposal, natural-language interface proposal, routing mandate, schema, runtime design, or product plan
created: 2026-06-23
scope: documentation-only repository review of self-explanation pressure
---

# Repository Self-Explanation Investigation

## Purpose

This investigation asks what it would mean for Seed to explain itself.

The motivating pressure is not simply that repository knowledge is missing. The
recurring operator experience is that the repository often contains enough
material to answer a question, but the operator must manually traverse maps,
diagnostics, views, reports, investigations, and commands to reconstruct:

```text
what knowledge is relevant
what findings govern the answer
what surfaces contribute evidence
what authority boundaries apply
what uncertainty remains
```

This is a repository-level architectural investigation. It does not propose a
natural-language interface, chat interface, agent architecture, CLI redesign,
new view, new command, navigation audit, observation implementation, or
reachability implementation. Repository authority wins.

## Method and authority boundary

The review treated reconciliations as boundary authority for their own scopes,
frontiers as unsettled pressure records, audits as scoped evaluations,
observations as repository evidence, and implementation files/tests as authority
only for existing behavior. The question was not whether a new surface should be
built. The question was whether the pressure named `repository self-explanation`
is already represented, merely a compression over existing concepts, or a
meaningful architectural concern in its own right.

Documents and surfaces reviewed included:

- `docs/seed.md`
- `docs/README.md`
- `docs/index.md`
- `docs/architectural_knowledge_map.md`
- `docs/knowledge_navigation_layers_frontier.md`
- `docs/source_navigation_surface_reconciliation.md`
- `docs/source_navigation_query_surface_design_audit.md`
- `docs/source_navigation_without_grep_audit.md`
- `docs/understanding_navigation_observation.md`
- `docs/operator_surface_activation_against_knowledge_and_understanding_audit.md`
- `docs/operator_understanding_surface_observation.md`
- `docs/work_shape_and_orientation_observation.md`
- `docs/work_recognition_reality_audit.md`
- `docs/inquiry_preservation_observation.md`
- `docs/discovery_path_preservation_observation.md`
- `docs/current_work_position_frontier.md`
- `docs/active_edge_frontier.md`
- `docs/continuability_observation.md`
- `docs/working_state_activation_observation.md`
- `docs/working_state_activation_failure_observation.md`
- `docs/documentation_authority_reconciliation.md`
- `docs/documentation_authority_and_seed_thesis_reconciliation.md`
- `docs/repository_navigation_question_surface_discoverability_investigation.md`
- `docs/reasoning_space_translation_investigation.md`
- `docs/context_preservation_surface_investigation.md`
- `docs/seed_self_knowledge_usefulness_exercise.md`
- `docs/observation_domain_permission_authority_reuse_investigation.md`
- `docs/constraint_aware_observation_reachability_investigation.md`
- `scripts/seed_local.py`
- relevant tests for inquiry orientation, source navigation, evidence graph,
  diagnostic inventory, and diagnostic shape audit where existing surfaces were
  implementation-backed.

Search terms included:

```text
continuation
activation
orientation
current work position
active edge
source navigation
documentation authority
operator understanding
inquiry preservation
discovery path preservation
knowledge navigation
understanding navigation
self knowledge
self-explanation
explain itself
correct command
observation authorization
observation permission
observation visibility
observation reachability
container_runtime
owner_not_observed
```

## Central finding

Repository evidence supports the pressure:

```text
knowledge exists
but is not reliably self-explaining
```

However, the evidence does not support collapsing this pressure into a single
existing branch. It overlaps strongly with knowledge navigation, source
navigation, understanding visibility, orientation, continuation, activation,
inquiry preservation, discovery-path preservation, documentation authority, and
observation reachability. Those branches each own part of the pressure. None of
them fully owns the operator question:

```text
Given my question, how does Seed determine the relevant knowledge, governing
findings, evidence surfaces, authority boundaries, and remaining uncertainty
without requiring me to know repository structure first?
```

The best current characterization is:

```text
repository self-explanation is an architectural responsibility candidate
```

It is stronger than a mere documentation-discoverability complaint, but weaker
than a reconciled architectural layer. It should remain an investigation branch
until repository evidence shows whether the responsibility can be decomposed into
existing concerns or needs its own reconciled boundary.

## What would it mean for Seed to explain itself?

For Seed to explain itself would not mean that Seed speaks in natural language
or owns a conversational interface. Repository evidence points to a narrower and
more architectural meaning.

Seed would explain itself when it can relate an operator question to:

1. **Relevant repository knowledge** — the claims, facts, documents,
   projections, diagnostics, implementation surfaces, and tests that bear on the
   question.
2. **Governing findings** — the reconciliations, audits, frontiers, and boundary
   records that constrain the answer.
3. **Evidence surfaces** — where the answer is supported, including current
   projections, support views, diagnostic outputs, implementation files, tests,
   and documentation lineage.
4. **Authority boundaries** — what the answer is allowed to claim, what remains
   diagnostic-only, what requires operator authorization, what is implementation-
   backed, and what must not silently become cluster truth.
5. **Uncertainty and remainder** — unknowns, blocked paths, non-selected
   alternatives, stale material, insufficient evidence, and unresolved frontier
   pressure.
6. **Use relation** — why this material matters for the current question rather
   than merely existing somewhere in the repository.

This makes self-explanation a relation over preserved knowledge, navigation,
selection, authority, and explanation. It is not identical to any one of them.

## Question 1: Is the recurring pressure actually knowledge exists but is not self-explaining?

Yes, with an important constraint.

The repository already preserves many answers. The documentation map explicitly
routes readers to owning documents rather than restating full arguments.
Knowledge navigation says Seed is developing structural, architectural, and
question-to-place navigation graphs. Source navigation reconciles that preserved
source relationships can still fail navigation when the operator must know exact
subjects, predicates, objects, paths, and support chains. Understanding
navigation similarly finds that understanding is visible but not equivalent to
knowing where to look first.

Recent self-knowledge exercise evidence makes the operator failure concrete:
Seed helps when the worker already knows the correct command, but weakens when
vocabulary is ambiguous, a filtered query has no current row, or a broad summary
needs drill-down. The constraint-aware observation reachability investigation
shows the same pattern in observation reasoning: current surfaces help reconstruct
partial answers, but inverse questions like why `container_runtime` remains
unobserved or what remains observable under denied authority are not reliably
answered by existing surfaces alone.

Therefore the pressure is not simply missing knowledge. It is missing or
incomplete self-explanatory relation among known material, governing findings,
operator questions, authority boundaries, and uncertainty.

## Question 2: Are recent branches converging on a common problem?

Yes, but they are not fully converged.

### Convergence signals

- **Orientation and work recognition** repeatedly find that the same preserved
  information can support different work depending on concern, boundary,
  reference point, pressure, active edge, and validation state.
- **Continuation and activation** show that preserving the right document or
  summary is insufficient if it does not become live as the governing constraint
  for the next move.
- **Current Work Position and Active Edge** preserve live or unresolved work
  position rather than all repository knowledge, indicating that relevance and
  current use matter.
- **Source navigation** shows that source facts can be preserved but still fail
  operator use when query shape and normalized fact identity must be known in
  advance.
- **Understanding navigation** shows that understanding can be visible without a
  settled model for how a participant chooses the right understanding surface.
- **Operator-surface activation** distinguishes understanding formation from
  understanding visibility, which directly matches the self-explanation pressure.
- **Inquiry and discovery-path preservation** show that conclusions are easier to
  preserve than the path, critique, uncertainty, rejected alternatives, and
  transition that made them understandable.
- **Observation authorization and reachability** show that capability,
  permission, provider availability, authority denial, and evidence gaps must be
  joined to explain what remains observable.
- **Seed self-knowledge exercise** demonstrates that existing diagnostic surfaces
  are useful but often depend on prior command vocabulary and follow-up route
  knowledge.

### Non-convergence signals

- Some repository questions are simple lookup or direct source navigation; they
  do not require a rich self-explanation layer.
- Documentation maps and indexes already solve part of the problem for humans and
  should not be bypassed or replaced.
- Existing explanation surfaces such as `why`/fact support, evidence graph,
  projection shape, diagnostic inventory, shape audit, component audit, source
  navigation, and inquiry orientation each answer bounded questions.
- Authority sometimes settles a question even when orientation is thin.
- The repository repeatedly warns that descriptive vocabulary such as
  orientation, active edge, current work position, and source navigation must not
  be promoted into repository knowledge without implementation evidence.
- Work-shape evidence supports recurring patterns but not a canonical taxonomy or
  universal orientation bundle.

The branches converge on a shared pressure, not on a single settled solution.

## Question 3: Knowledge preservation vs knowledge navigation vs knowledge explanation

The repository evidence supports these distinctions:

| Concern | Architectural question | Failure mode if missing | Relationship to self-explanation |
| --- | --- | --- | --- |
| Knowledge preservation | What claims, observations, support, documents, lineage, and relationships survive? | The answer is lost, stale, unsupported, or detached from evidence. | Necessary but insufficient. Self-explanation cannot work without preserved material. |
| Knowledge navigation | How does a participant move from a question, symbol, concept, or surface to relevant preserved material? | The answer exists but cannot be found without accidental prior knowledge. | Necessary but insufficient. Navigation finds material but may not explain why it governs the answer. |
| Knowledge explanation | Why does this material support, contradict, constrain, or leave uncertain the answer under the relevant authority boundary? | The answer is found but not justified, bounded, or safe to use. | Necessary but insufficient. Explanation can justify a selected claim while leaving selection and route opaque. |
| Repository self-explanation | How are preservation, navigation, selection, evidence, authority, uncertainty, and use relation composed for the operator's question? | The operator manually reconstructs the repository's answer across commands, docs, tests, and boundaries. | Candidate responsibility spanning the previous three without replacing them. |

This distinction is important because existing Seed strengths are uneven. Seed is
comparatively strong at preservation and bounded explanation. It is improving at
navigation. It is weakest where the operator asks a composite question whose
answer requires joining multiple preserved and explanatory surfaces.

## Question 4: Is “operator must know the correct command” a repository failure mode?

Sometimes yes.

It is not a failure when the command is a stable expert tool for a bounded task
and the operator reasonably knows the domain. It becomes a repository failure
mode when the required command name, filter, fact shape, diagnostic family, or
document lineage is itself the hidden answer to the operator's question.

Examples supported by repository evidence:

- Source navigation identified brittleness when an operator must know exact
  normalized fact shapes before source facts become useful.
- The self-knowledge usefulness exercise found that `--shape-coverage` did not
  exist while related surfaces existed under other meanings and names.
- Capability relationship output can be safe but under-explanatory when a filter
  returns no current row and does not distinguish known-but-unpressured from
  unknown capability.
- Operational story provides a useful headline but often requires the operator to
  know the next drill-down command.
- Observation reachability questions require the operator to join domain,
  permission, capability, provider, and constraint surfaces manually.

The failure is architectural because Seed's thesis centers explainable knowledge
and authority-bounded reasoning. If the repository already has the ingredients
but the answer depends on the operator guessing the right surface sequence, Seed
has preserved knowledge without fully preserving its route to use.

## Question 5: Operator navigates Seed vs Seed navigates Seed

There is a meaningful distinction.

```text
operator navigates Seed
```

means the human or external worker chooses maps, commands, documents, searches,
filters, and evidence paths. Existing documentation maps, indexes, and CLI
surfaces primarily support this mode.

```text
Seed navigates Seed
```

would mean Seed can select or expose the relevant route through its own preserved
knowledge and authority boundaries for a bounded question. This does not require
natural language. It could be any deterministic or documented mechanism that
connects question shape, repository knowledge, governing findings, surfaces,
uncertainty, and next evidence routes.

The distinction matters because operator navigation can be successful while
still placing hidden structural knowledge on the operator. Seed navigating Seed
would make that structural knowledge part of the answer, subject to authority and
shape checks.

The distinction also has a control boundary: Seed navigating Seed must not become
Seed deciding operational action. Navigation and explanation can surface routes,
confidence, gaps, and authority constraints; operator authority still governs
approval, action, and interpretation where required.

## Question 6: Existing concepts that partially address the pressure

Repository self-explanation is partly addressed by existing branches:

| Existing concept or surface | What it contributes | What remains missing for self-explanation |
| --- | --- | --- |
| Documentation map and index | Human route to owning documents and families. | Requires knowing the document family or vocabulary. |
| Architectural knowledge map | Conceptual routing across architecture areas. | Does not by itself answer concrete operator questions or evidence joins. |
| Knowledge navigation layers | Names structural, architectural, and question-to-place navigation layers. | Frontier, not reconciled implementation or complete responsibility. |
| Source navigation | Moves from implementation questions to preserved source facts and support. | Source-specific; not general governing-finding or authority explanation. |
| Inquiry orientation | Bounded orientation around inquiry notes and related material. | Inquiry-note-centered and read-only; not general self-explanation. |
| Current Work Position | Preserves situated current concern and continuation-relevant position. | Current-work specific; does not explain all repository knowledge. |
| Active Edge | Preserves unresolved/live edge pressure. | Frontier-like and not a general navigation/explanation layer. |
| Handoff and continuation | Preserve enough context for safe resumption. | Resumption-specific; not necessarily answer explanation. |
| Discovery-path preservation | Preserves critique/discovery transitions and compression removal pressure. | Observational; not a complete route-selection mechanism. |
| Understanding visibility/navigation | Distinguishes visible understanding from finding and using it. | Exploratory; does not settle responsibility. |
| Explanation/fact support/evidence graph | Explain support for claims or evidence paths. | Usually assumes the selected claim/fact is already known. |
| Selection rationale | Explains why a known candidate was selected. | Does not find all relevant governing material for an arbitrary question. |
| Diagnostic inventory and shape audit | Make diagnostic surfaces visible and implementation-shape checked. | Diagnostic-surface governance only, not full repository self-explanation. |
| Component audit/projection shape/operational story | Useful self-knowledge summaries over implementation-backed surfaces. | Broad or component-specific; often needs drill-down route knowledge. |
| Observation permission/reachability investigations | Separate capability availability, permission, authorization, and scenario reachability. | Reachability is not yet a general answer-composition layer. |

These concepts are real partial answers. The self-explanation pressure should not
be treated as wholly new or disconnected from them.

## Question 7: Missing capability, layer, responsibility, false expectation, or something else?

The strongest answer is:

```text
missing architectural responsibility candidate
```

It may later decompose into existing concerns, but the current pressure is not
adequately captured by any one concern. It is not merely missing documentation,
because implementation-backed surfaces already answer some questions and still
require manual route reconstruction. It is not merely missing navigation, because
finding the right artifact does not explain why it governs the answer. It is not
merely missing explanation, because explaining a selected fact does not reveal
which fact, finding, authority boundary, or diagnostic surface should be selected
for the operator's question.

It is also not yet a proven architectural layer. Repository evidence supports an
investigation branch, not an implementation mandate. A future reconciliation
would need to decide whether self-explanation is:

- a named architectural layer over existing preservation/navigation/explanation;
- a responsibility distributed across existing surfaces;
- a set of shape requirements for self-knowledge surfaces;
- a documentation/navigation hygiene standard;
- or a false compression that should be decomposed back into orientation,
  navigation, authority, reachability, and explanation work.

## Required tensions

### Preservation vs navigation

Preservation asks whether the material survives. Navigation asks whether a
participant can reach it from a question. Source navigation and understanding
navigation both show that preservation can be strong while navigation remains
weak. Self-explanation depends on both but cannot collapse them.

### Navigation vs explanation

Navigation answers where to go. Explanation answers why a selected item supports,
contradicts, constrains, or fails to settle the answer. A source path can be the
right place to inspect while still not explaining authority or uncertainty. A
fact-support view can explain a fact while not explaining why that fact is the
right one for the question.

### Continuation vs explanation

Continuation preserves enough current position for work to resume. Explanation
preserves why an answer is supported and bounded. They overlap when the operator
asks why the current branch exists or how to resume an inquiry, but continuation
is not general explanation.

### Orientation vs explanation

Orientation supplies relation-to-use: concern, reference point, boundary,
pressure, active edge, and validation state. Explanation supplies support and
constraint. Work-shape evidence shows orientation is load-bearing for many tasks,
but orientation is not automatically a claim explanation or ontology.

### Authority vs explanation

Self-explanation must include authority boundaries. Without authority, an answer
can overclaim: diagnostic findings can become cluster truth, presentation labels
can become repository knowledge, capability availability can be mistaken for
observation authorization, or a derived current focus can be mistaken for
operator intent. Explanation without authority is unsafe.

### Operator understanding vs operator control

Self-explanation should improve operator understanding without taking operator
control. It may reveal relevant routes, evidence, uncertainty, and authorization
boundaries. It must not approve probing, mutate cluster state, choose an
operational plan, or treat diagnostic-only findings as durable entity truth.

### Surface visibility vs self-explanation

The diagnostic inventory and shape audit prove a visibility principle: surfaces
should not be invisible. But visible surfaces do not automatically self-explain.
Self-explanation asks how visible surfaces relate to a question and to each
other.

## Strongest supporting evidence

1. Seed's thesis already values explainable knowledge, evidence, projection, and
   authority-bounded reasoning.
2. Knowledge navigation explicitly frames navigation as potentially part of how
   Seed explains itself, maintains itself, and continues learning.
3. Source navigation reconciles the preservation/navigation distinction and
   states that preserved source facts can remain unusable if operators must know
   exact fact shapes.
4. Understanding navigation finds visible understanding but no single settled
   understanding-navigation model.
5. Operator-surface activation finds that existing understanding work is being
   reactivated as a visibility problem.
6. Work-shape and work-recognition audits show repeated cases where the same
   preserved information supports different work only when oriented by concern,
   boundary, and evidence relations.
7. Handoff, continuation, activation, Current Work Position, and Active Edge work
   show that preserving summaries is insufficient when activation and live edge
   context are missing.
8. Discovery-path preservation shows conclusions survive more easily than the
   discovery route, rejected paths, critique, and understanding transition.
9. Observation authorization and reachability work shows concrete cases where
   answers require joining capability, permission, provider, authority, and
   evidence surfaces.
10. Seed self-knowledge exercise shows implemented self-knowledge surfaces are
    useful but still depend on command discoverability and drill-down route
    knowledge.

## Strongest contradictory evidence

1. Many existing surfaces already explain bounded things: fact support,
   why-fact/current belief explanation, evidence graph, projection shape,
   diagnostic inventory, diagnostic shape audit, component audit, operational
   story, source navigation, and inquiry orientation.
2. Documentation maps and indexes intentionally route readers to owning documents
   and already serve as repository navigation authority.
3. Some questions are direct lookup problems; adding a self-explanation frame
   would overcomplicate them.
4. Work-shape evidence rejects a universal orientation bundle and warns against
   promoting descriptive vocabulary into canonical architecture prematurely.
5. Authority boundaries can settle some questions without rich orientation or
   self-explanation.
6. A broad self-explanation layer could duplicate or obscure existing stronger
   authorities if it restates rather than routes to owning documents.
7. Natural-language or agentic implementation assumptions are explicitly outside
   the current evidence and could distort the architectural question.

## Relationship to operator experience

The operator experience described in the prompt is strongly reflected in
repository evidence. The operator repeatedly asks questions whose answers exist
across several surfaces but not as a single explanation route:

- why a runtime facet is unobserved;
- why an ownership finding remains unresolved;
- what observation paths remain under denied authority;
- which inquiry produced a finding;
- which investigation governs a conclusion;
- which command or view corresponds to a vocabulary phrase;
- which evidence is implementation-backed versus presentation vocabulary;
- which uncertainty remains after a bounded answer.

This is not simply impatience with documentation. It is a mismatch between the
shape of operator questions and the distributed shape of repository authority.
Seed currently expects the operator to be a skilled repository navigator for
composite questions. The self-explanation pressure asks whether that expectation
is itself an architectural smell.

## Relationship to existing branches

- **Knowledge navigation** is the nearest existing branch. Self-explanation
  extends it by requiring not just route discovery but answer governance,
  evidence, authority, and uncertainty.
- **Orientation** contributes relation-to-use and helps explain why the same
  material matters differently under different work shapes. Self-explanation
  should not make orientation a universal primitive.
- **Continuation and activation** explain why preserved material can fail to
  govern later work. Self-explanation inherits that activation concern when the
  answer should guide current operator reasoning.
- **Source navigation** is a concrete domain-specific precedent: navigation is
  an orientation layer over preserved facts, not new observation or stronger
  truth.
- **Understanding visibility/navigation** provides the closest operator-facing
  analogy: understanding may exist and be visible yet still be difficult to
  locate and use.
- **Inquiry and discovery-path preservation** supply lineage pressure: explaining
  a finding often requires the inquiry path and residual pressure, not only the
  conclusion.
- **Observation authorization/reachability** supplies the strongest operational
  example: authority and reachability must be composed to answer what Seed can
  learn under constraints.
- **Documentation authority** constrains any future self-explanation: it must
  route to owning documents and not become a parallel authority system.

## Open questions

1. Can repository self-explanation be decomposed into existing concepts plus
   better routing, or does it require a named architectural boundary?
2. What minimum evidence would justify reconciling self-explanation rather than
   keeping it as an investigation lens?
3. Should self-explanation be scoped only to Seed's self-knowledge, or also to
   Seed's explanations about observed external systems?
4. What is the boundary between self-explanation and recommendation or selection
   rationale?
5. How can a self-explanation responsibility preserve operator control while
   still selecting relevant routes and uncertainty?
6. How should implementation-backed surfaces distinguish unknown, absent,
   unsupported, unauthorized, unavailable, stale, blocked, and not-yet-routed?
7. Can diagnostic inventory and shape audit provide a precedent for governing
   self-explanation surfaces, or is the pressure broader than diagnostics?
8. When is “operator must know the correct command” acceptable expert-tool
   behavior, and when is it evidence that a self-explanatory route is missing?
9. How should discovery-path and inquiry lineage be exposed without preserving
   every interaction transcript or creating a process log?
10. What tests or audits would prove that a future self-explanation surface routes
    to governing authority rather than inventing a parallel answer?

## Conclusion

Repository self-explanation is a meaningful architectural branch candidate, not
yet a reconciled layer.

The pressure is real: repository knowledge often exists, and Seed has multiple
bounded explanation and navigation surfaces, but composite operator questions
still require manual reconstruction across structure, concepts, diagnostics,
documentation authority, inquiry lineage, observation reachability, and
uncertainty. Recent branches are converging on this pressure from different
angles.

The pressure is also not wholly new. It is a compression over existing work in
knowledge navigation, source navigation, understanding visibility, orientation,
continuation, activation, inquiry preservation, discovery-path preservation,
documentation authority, and observation reachability. Treating it as brand-new
would erase stronger existing authorities.

The careful architectural answer is therefore:

```text
Seed should not automatically be expected to answer every natural question by
navigating itself.

But Seed's architecture already values explainable, authority-bounded knowledge.
When Seed has the preserved material needed to answer an operator's question,
and the remaining burden is knowing which repository surfaces, findings,
authority boundaries, and uncertainties to compose, repository self-explanation
is a legitimate architectural concern.
```

The next architectural step should not be implementation. It should be deciding
whether this branch can be reconciled as a bounded responsibility, or whether it
should be decomposed back into stricter improvements to existing navigation,
orientation, authority, reachability, and explanation branches.
