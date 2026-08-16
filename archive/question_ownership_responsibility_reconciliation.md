# Question Ownership Responsibility Reconciliation

## Purpose and boundary

This reconciliation investigates one architectural responsibility question:

```text
How does a bounded question become the responsibility of one subsystem?
```

It is implementation-backed and descriptive. It does not recommend a router,
planner, dispatcher, registry redesign, workflow engine, dependency-injection
scheme, or framework extraction. Repository authority remains with executable
surfaces, implementation specs, tests, and prior reconciliations where they are
supported by current implementation.

This is not a runtime investigation. The reviewed implementation surfaces are
read-only diagnostics, audits, and visibility views that expose current
responsibility boundaries.

## Files inspected

Implementation and reconciliation evidence inspected:

- `seed_runtime/question_surface_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `seed_runtime/service_ownership_authority.py`
- `seed_runtime/container_ownership_authority.py`
- `seed_runtime/projection_shape.py`
- `seed_runtime/reasoning_path_audit.py`
- `seed_runtime/knowledge_reachability.py`
- `seed_runtime/reference_selection.py`
- `scripts/seed_local.py`
- `docs/repository_navigation_question_surface_discoverability_investigation.md`
- `AGENTS.md`

Commands used as app evidence:

- `python scripts/seed_local.py --question-surface-inventory`
- `python scripts/seed_local.py --diagnostic-shape-audit --status mismatch`

## Central finding

Current implementation supports a recurring responsibility discipline:

```text
bounded operator question
↓
one primary answering surface / subsystem
↓
implementation and diagnostic evidence contributors
↓
operator capability preserved or lost
```

This is not merely a naming coincidence. The strongest evidence is the static
question-surface inventory: each row has a `question_family`, example questions,
a single `surface`, a CLI flag, an `answer_responsibility`, and an authority
boundary. The formatter renders this as known question families and answering
Seed surfaces, and explicitly states that the inventory does not route operator
questions. That means the implementation records answer responsibility without
becoming a router.

The discipline is also visible in the diagnostic shape audit: each diagnostic
name is bound to one implementation spec with one module path and expected build,
format, JSON, record, and CLI shape. The app currently reports zero mismatches
for that boundary.

## 1. Does each bounded operator question currently have one primary responsible subsystem?

Yes, for the reviewed implementation-backed question families.

The best direct evidence is `question_surface_inventory`. It does not model a
question as an open set of coequal owners. It returns deterministic rows where a
bounded `question_family` maps to one `surface` and one `answer_responsibility`.
Reviewed examples include:

| Bounded question family | Primary responsible surface | Implementation-backed answer responsibility |
| --- | --- | --- |
| Derivation explanation | `reasoning_path` | Evidence-backed derivation path from source evidence through conclusions and consumers. |
| Knowledge reachability | `knowledge_reachability` | Reachability across preserved, projected, read-model, inquiry, and rendered surfaces. |
| Authority-constrained container ownership | `container_ownership_authority` | Container ownership reachability under constrained authority. |
| Authority-constrained service ownership | `service_ownership_authority` | Service ownership reachability under constrained authority and implementation inventory evidence. |
| Surface shape validation | `diagnostic_shape_audit` | Registry declaration compared with static implementation shape. |
| Projection shape visibility | `projection_shape` | Implementation-backed projection stage shape. |

The diagnostic shape audit reinforces the same discipline at the implementation
contract layer. `IMPLEMENTATION_SPECS` binds names such as
`knowledge_reachability`, `container_ownership_authority`,
`service_ownership_authority`, `reasoning_path`, `reference_selection`,
`projection_shape`, and `question_surface_inventory` to one module and expected
functions/flags. The app-level shape audit reports no mismatch rows, so this
registry-to-implementation ownership boundary is currently coherent.

## 2. Can multiple subsystems contribute evidence while one subsystem owns the answer?

Yes. This is the normal pattern in the reviewed surfaces.

`service_ownership_authority` owns the answer to whether service ownership is
reachable under constrained authority. It consumes several contributors:
capability needs, observation domains, observation inventory, observation
permission classes, ownership discrepancy records, privilege discovery guidance,
and projected state. Those contributors provide evidence, names, and boundaries;
the service ownership evaluator decides the output outcome, remaining
observations, uncertainty, blocking boundary, and read-only boundary.

`container_ownership_authority` similarly owns the container-ownership authority
answer while consuming capability needs, observation-domain mapping,
observation-permission support, privilege guidance, and projected state. The
contributing surfaces do not become co-owners of the final container ownership
answer.

`reasoning_path` is the clearest evidence-contributor example. It builds one
answering audit from ownership discrepancies, capability needs, pressure audit,
privilege discovery, and operational story. Its output separates observed
evidence, intermediate conclusions, derived conclusions, consumers, story
impact, and unknowns.

`knowledge_reachability` also composes evidence from the event ledger, projected
state, repository files, source-navigation terms from fact support, read-model
surfaces, and inquiry orientation. It still owns the reachability answer because
it decides candidate discovery, kind classification, stage flags, first-loss
calculation, timing metadata, truncation, and rendering.

`reference_selection` owns the reference-selection answer for the supported
history domain while consuming `impact_audit` and `snapshot_policy_audit`. The
selected reference, alternatives, authority boundary, and limitations are
emitted by `reference_selection`, not by either contributor alone.

## 3. Does implementation distinguish evidence contributor from answer owner?

Yes, with one important limitation: the distinction is implementation-structural
rather than a universal type system.

Evidence for the distinction:

- Question inventory rows name one answering `surface` and its
  `answer_responsibility`, while notes say the inventory itself does not route
  operator questions.
- Authority slices import and call evidence-producing helpers, but their result
  dataclasses own fields such as `outcome`, `strategy_status`,
  `remaining_observations`, `uncertainty`, `blocking_boundary`, and `boundary`.
- `reasoning_path` labels contributing outputs as evidence, intermediate
  conclusions, derived conclusions, consumers, and story impact inside a single
  `ReasoningPathAudit` answer.
- `projection_shape` distinguishes stage `consumes`, `produces`, `influences`,
  and `does_not_influence`, which prevents consumed implementation from being
  treated automatically as answer ownership.
- `reference_selection` distinguishes selected reference authority from
  candidate references and explicitly limits alternatives to what implementation
  evidence exposes.

The limitation is that the repository does not expose a universal
`evidence_contributor` / `answer_owner` schema for every subsystem. The
separation is recurring and implementation-backed in these surfaces, but it is
not currently a generalized architectural registry.

## 4. Can the statement be supported?

```text
Subsystem ownership
is determined by
the bounded question it answers,
not by
the implementation it consumes.
```

Supported for the reviewed surfaces.

`service_ownership_authority` consumes ownership discrepancies and capability
needs, but its ownership is determined by the question “Can Seed determine
service ownership under current authority?” It does not become a general owner
of capability pressure, ownership discrepancy reporting, observation inventory,
or privilege guidance.

`knowledge_reachability` consumes preserved events, projected state, read-model
surfaces, inquiry orientation, and repository tokens. Its ownership is not any
one consumed implementation. Its ownership is the reachability question: whether
a candidate is visible across the preserved/projected/read-model/inquiry/rendered
stages and where first loss occurs.

`projection_shape` consumes no runtime projection state when building its view;
it owns the implementation-backed question “What shape does the projection build
expose?” through static stage declarations. Its stage declarations name consumed
and produced implementation concepts without transferring answer ownership to
those consumed concepts.

`reference_selection` consumes impact and snapshot-policy audits but owns the
question “What implementation-selected comparison reference is visible for this
domain?” The selected reference and accepted-reference boundary belong to the
reference-selection answer.

## 5. Would removing an evidence contributor produce the same architectural consequence as removing the answering subsystem?

No. Current implementation demonstrates a difference.

Removing an evidence contributor weakens, narrows, or changes evidence available
to the answer owner. Removing the answering subsystem removes the operator
capability for that bounded question.

Examples:

- If `build_observation_inventory` evidence were unavailable to
  `service_ownership_authority`, the evaluator could still own the service
  ownership authority answer, but uncertainty would lose listener/systemd support
  evidence. If `service_ownership_authority` itself were removed, the bounded
  service-ownership authority question would no longer have its answering
  surface.
- If `ownership_discrepancies` contributes no matching rows,
  `reasoning_path` still returns a reasoning-path answer with unknowns when no
  derivation evidence is available. If `reasoning_path` is removed, the operator
  loses the derivation explanation surface.
- If `impact_audit` exposes no comparable history snapshots,
  `reference_selection` still returns a history-domain answer with an unavailable
  selected reference and limitations. If `reference_selection` is removed, the
  comparison-reference question loses its owner.
- `diagnostic_shape_audit` can observe no mismatches or unknowns, but the audit
  surface still owns shape-validation capability. Removing one diagnostic spec
  changes the evidence population; removing the audit removes the validation
  capability.

Architecturally, contributor loss is evidence degradation. Answer-owner loss is
operator capability loss.

## 6. Does question ownership currently appear exclusive, shared, layered, or implementation-dependent?

The supported answer is: **exclusive at the primary answer-owner boundary, layered
in evidence contribution, and implementation-dependent in scope**.

- **Exclusive primary ownership:** reviewed bounded question families have one
  primary answering surface in `question_surface_inventory` and one primary
  implementation spec in `diagnostic_shape_audit`.
- **Layered contribution:** answer owners routinely consume projected state,
  diagnostic facts, repository files, other audits, and support surfaces.
- **Implementation-dependent scope:** exclusivity is only supported where current
  implementation declares or demonstrates it. The repository does not prove that
  every possible future question has a unique owner, nor does it expose a global
  universal ownership type system.

The evidence does not support “shared” answer ownership for the reviewed bounded
questions. Multiple subsystems contribute evidence, but the final answer shape,
boundary, and operator-facing capability are owned by one surface.

## 7. Does this strengthen the emerging architectural model?

It strengthens the model, with a narrower wording:

```text
Inquiry
↓
Question
↓
Responsible answering subsystem
↓
Evidence contributors
↓
Operator capability
```

The model is supported when “responsible subsystem” means primary answer owner,
not exclusive implementation dependency. Current implementation repeatedly shows
that operator capability is lost when the answering surface is absent or
incoherent, while evidence contributors can be absent, limited, or uncertain
without automatically removing the bounded question owner.

## Question ownership

A bounded question is owned by the subsystem whose implementation emits the
operator-facing answer shape for that question.

Ownership is visible through:

- the `question_surface_inventory` row mapping question family to answering
  surface;
- the diagnostic shape audit implementation spec binding that surface to a
  module, functions, and CLI flag;
- the result dataclass or output shape that owns outcome, boundary, uncertainty,
  selected reference, reachability rows, projection stages, or validation rows;
- tests and app output proving the surface is inventory-visible and shape-audited.

## Answer ownership

Answer ownership is not the same as data production. The answer owner is the
surface that determines the final operator-facing answer contract. Examples:

- `service_ownership_authority` owns service ownership authority outcome.
- `container_ownership_authority` owns container ownership authority outcome.
- `projection_shape` owns projection stage shape visibility.
- `diagnostic_shape_audit` owns registry/implementation shape validation.
- `reasoning_path` owns derivation explanation.
- `knowledge_reachability` owns reachability and first-loss classification.
- `reference_selection` owns selected comparison-reference visibility.

## Evidence contribution

Evidence contributors are implementations consumed by an answer owner to ground
its answer. Contributors can include audits, inventories, projected state,
preserved events, repository files, fact-support indexes, capability records,
privilege guidance, and prior observations.

Contribution does not imply ownership. The same contributor may support multiple
answer owners without owning each answer.

## Responsibility boundaries

Reviewed responsibility boundaries are consistently read-only for these surfaces:
no provider acquisition, no permission creation, no cluster mutation, and no
runtime orchestration. Where the result shape includes an event-ledger boundary,
it marks event-ledger writes as false for these read-only investigations.

The boundaries also prevent diagnostic findings from becoming cluster truth:
these surfaces report reachability, authority, shape, derivation, and reference
selection without promoting diagnostic-only findings into runtime mutation.

## Implementation evidence

Implementation-backed evidence includes:

1. `question_surface_inventory` declares question families, example questions,
   one answering surface, one CLI flag, answer responsibility, authority
   boundary, and non-routing notes.
2. `diagnostic_shape_audit` declares implementation specs for the reviewed
   surfaces and the app reports zero shape mismatches.
3. `service_ownership_authority` and `container_ownership_authority` consume
   evidence helpers but own result dataclasses and outcomes.
4. `reasoning_path` composes multiple contributors into one derivation audit and
   distinguishes evidence, conclusions, consumers, story impact, and unknowns.
5. `knowledge_reachability` discovers and classifies candidates, builds stage
   indexes, computes first loss, and renders reachability metadata from multiple
   contributors.
6. `projection_shape` names consumed, produced, influencing, and
   non-influencing concepts by stage, preserving responsibility boundaries.
7. `reference_selection` consumes history evidence while owning selected
   reference, alternatives, authority boundary, and limitations.

## Contradictory evidence

No reviewed implementation shows two coequal primary answer owners for the same
bounded question family.

The main contrary pressure is incompleteness rather than contradiction:

- The question-to-surface discoverability investigation found that workers may
  struggle to choose the right surface before they already know the vocabulary.
  That is a discoverability limitation, not evidence of shared answer ownership.
- Some surfaces aggregate other surfaces, especially operational story and ops
  brief. Aggregation can look like shared ownership, but reviewed code presents
  these as composition surfaces with their own bounded summary/narrative
  responsibility.
- The repository does not yet expose a universal answer-owner/evidence-contributor
  schema across all code. Therefore the finding should remain scoped to current
  implementation-backed surfaces.

## Remaining uncertainty

Remaining uncertainty is bounded:

- The reviewed surfaces support primary ownership for current diagnostic and
  visibility questions, but not for every conceivable future inquiry.
- The implementation proves recurring discipline through concrete surfaces, not
  through a generalized ownership ontology.
- Some natural-language question families remain only partially discoverable;
  this investigation does not convert them into runtime routing behavior.
- Documentation can describe the pattern, but repository authority remains with
  executable surfaces and tests.

## Acceptance answer

### Who owns a bounded question?

The subsystem that emits the bounded question's operator-facing answer shape
owns the question. Current implementation exposes that ownership through the
question-surface inventory, diagnostic implementation specs, result structures,
formatters, JSON functions, CLI flags, and tests.

### Can many subsystems contribute while one subsystem remains responsible for the answer?

Yes. Current implementation repeatedly consumes many evidence contributors while
one surface owns the answer. Contributors provide evidence, pressure, projected
state, registry declarations, repository context, or comparison candidates. The
answer owner decides the output shape, status, uncertainty, boundary, and
operator capability.

### Has implementation revealed another recurring architectural discipline, or merely another coincidence?

It has revealed another recurring architectural discipline: bounded questions
produce primary answering responsibility. The pattern is implementation-backed
across question inventory, authority slices, shape audit, projection shape,
reasoning path, knowledge reachability, and reference selection. It should not be
overextended into a router, planner, framework, or universal registry.

## Files changed

- `docs/question_ownership_responsibility_reconciliation.md`

## LOC changed

- Added 417 lines.

## Tests run

- `python scripts/seed_local.py --question-surface-inventory`
- `python scripts/seed_local.py --diagnostic-shape-audit --status mismatch`
- `pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

## Recommended next bounded investigation

Investigate the bounded question:

```text
When an answering subsystem emits uncertainty,
which subsystem owns reducing that uncertainty?
```

Boundary: determine only what current implementation demonstrates about
uncertainty ownership and capability-pressure ownership. Do not introduce a
planner, router, workflow engine, or ownership registry.
