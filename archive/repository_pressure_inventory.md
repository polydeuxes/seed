# Repository Pressure Inventory

## Scope

This pressure inventory characterizes recurring unresolved repository pressure.
It does not propose a roadmap, architecture, future-state vision, strategy,
autonomous-agent design, maturity model, ontology, or grand framework.

Repository authority remains implementation-backed behavior, tests, executable
surfaces, and existing repository-visible documents.

## Files inspected

- `AGENTS.md`
- `seed_runtime/pressure_audit.py`
- `seed_runtime/ops_brief.py`
- `seed_runtime/operational_story.py`
- `seed_runtime/diagnostic_inventory.py`
- `docs/surviving_pressure_after_decomposition_observation.md`
- `docs/inquiry_closure_satisfaction_and_residual_pressure_investigation.md`
- `docs/repository_navigation_question_surface_discoverability_investigation.md`
- `docs/authority_aware_observation_reasoning_investigation.md`
- `docs/capability_need_acquisition_reconciliation.md`
- `docs/ownership_claim_reconciliation.md`
- `docs/projection_shape_visibility_investigation.md`
- `docs/repository_prose_structure_visibility_investigation.md`

## Commands used

```text
pwd && rg --files -g 'AGENTS.md' -g '!.*' | xargs -r -I{} sh -c 'echo --- {}; cat {}' && git status --short
rg --files | rg '(operational|brief|story|capabil|ownership|consumer|authority|structure|question|frontier|pressure|diagnostic|projection)'
python scripts/seed_local.py --pressure-audit --json
python scripts/seed_local.py --ops-brief --json
python scripts/seed_local.py --diagnostic-shape-audit --mismatches
```

## Top recurring pressures

### 1. Consumer coverage pressure: orphaned and fragile observation predicates

#### Observed recurrence

This is the strongest current operational pressure because it appears directly in
implemented pressure and operational brief surfaces, not only in prose. The live
pressure audit reported 21 orphaned predicates and 13 fragile single-consumer
predicates.

#### Supporting evidence

`seed_runtime/pressure_audit.py` implements `Orphaned Predicates` and `Fragile
Predicates` as pressure categories sourced from `build_consumer_audit(...)`.
`seed_runtime/ops_brief.py` counts orphaned and fragile predicates and recommends
investigation when either count is non-zero.

#### Current mitigation

Seed has `consumer_audit`, `pressure_audit`, and `ops_brief` visibility.

#### Remaining gap

Predicate existence and predicate consumption remain uneven. Current visibility
identifies the pressure but does not resolve individual unconsumed or
single-consumer predicates.

#### Smallest plausible next slice

Pick one orphaned predicate family from the current audit output and add or
remove exactly one implementation-backed consumer path, with a test proving the
consumer audit count changes as expected.

### 2. Question-to-surface discoverability pressure

#### Observed recurrence

Seed often has an answering surface, but workers still need to know which surface
to choose. Surface self-description is strong after selection; question-to-surface
discovery before selection remains weak.

#### Supporting evidence

`docs/repository_navigation_question_surface_discoverability_investigation.md`
classifies many question families as only partially discoverable and identifies
cross-surface follow-up as poorly to partially discoverable.

#### Current mitigation

Seed has self-describing surfaces including `diagnostic_inventory`,
`diagnostic_shape_audit`, `projection_shape`, `operational_story`,
`capability_relationship`, `reasoning_path`, `selection_path`, and
`reference_selection`.

#### Remaining gap

No current repository-visible surface primarily answers: given this worker
question, which answering surface should be used next?

#### Smallest plausible next slice

Add one tested row-set to an existing inventory-style surface mapping a small
fixed set of natural question families to existing diagnostic surfaces, without
introducing a router or recommendation engine.

### 3. Authority-aware observation reachability pressure

#### Observed recurrence

Seed has pieces for observation permission, capability needs, privilege
discovery, observation domains, and capability relationship. The recurring gap is
joining them into a desired-observation reachability answer.

#### Supporting evidence

`docs/authority_aware_observation_reasoning_investigation.md` identifies the
missing behavior as a deterministic join across desired observation, diagnostic
capability needs, observation-domain/provider evidence, access guidance,
permission state, and explicit constraints.

#### Current mitigation

Separate local surfaces exist for observation permissions, observation domains,
capability needs, privilege discovery, capability relationship, and ownership
discrepancies.

#### Remaining gap

Desired-observation reachability is still reconstructed manually across surfaces.

#### Smallest plausible next slice

Implement a read-only diagnostic for one constrained case, such as container
ownership reachability, joining existing data without recording facts or mutating
state.

### 4. Capability pressure and evidence-to-need acquisition pressure

#### Observed recurrence

Capability pressure appears both as operational missing-observation pressure and
as an unresolved upstream question: how repeated evidence becomes a durable
capability need.

#### Supporting evidence

`docs/capability_need_acquisition_reconciliation.md` says Seed does not currently
define a principled lifecycle for transforming observations, evidence, repeated
failures, repeated manual work, provider handoffs, or reconciliation findings into
a durable `CapabilityNeed` / `ToolNeed`.

#### Current mitigation

Seed supports explicit request-to-need creation through `request_tool` and
read-only capability resolution after a need exists.

#### Remaining gap

Repeated failures, handoffs, manual steps, and reconciliation findings do not yet
become durable capability pressure through an evidence-backed path unless an
explicit request already created a `ToolNeed`.

#### Smallest plausible next slice

Add one evidence-backed capability-gap predicate or diagnostic-only row for failed
capability resolution, without changing the provider lifecycle or creating
autonomous acquisition.

### 5. Ownership attribution and ownership-authority pressure

#### Observed recurrence

Ownership remains recurrent because behavior, boundary, and responsibility are
easy to conflate.

#### Supporting evidence

`docs/ownership_claim_reconciliation.md` states that lower layers can show
existence, structure, behavior, or boundary without proving architectural
accountability. `seed_runtime/pressure_audit.py` also includes an ownership
attribution pressure category based on unresolved ownership discrepancy rows.

#### Current mitigation

Seed has ownership discrepancies, service ownership authority, container
ownership authority, listener endpoint authority, and operational ownership
pressure visibility.

#### Remaining gap

Live operational output showed no ownership ambiguity rows, but ownership-authority
remains hard to infer safely from behavior or boundary alone.

#### Smallest plausible next slice

Add a regression test for one known ownership-authority distinction: behavior
evidence alone must not satisfy ownership authority for a selected component or
service.

### 6. Projection shape visibility pressure

#### Observed recurrence

Projection behavior is substantial, but projection stage shape is less explicit
than diagnostic surface shape.

#### Supporting evidence

`docs/projection_shape_visibility_investigation.md` says projection stage
composition is mostly encoded in implementation order, helper calls, dataclass
fields, CLI formatters, and tests rather than in a projection-specific shape
inventory.

#### Current mitigation

Projection implementation includes event replay, alias resolution, measurement
retention, inference, support aggregation, relationship projection, entity type
assertion, graph validation, and conflict projection.

#### Remaining gap

Projection-stage authority and influence still require manual reconstruction from
code.

#### Smallest plausible next slice

Add one implementation-backed projection-stage inventory row-set for existing
finalize-stage labels only, with tests proving rows are emitted and remain
read-only.

### 7. Diagnostic visibility contract pressure

#### Observed recurrence

Diagnostic visibility is currently well mitigated but remains a recurring
operational contract for every new diagnostic, audit, probe, view, CLI flag, or
recordable output.

#### Supporting evidence

`AGENTS.md` requires updates to diagnostic inventory, diagnostic shape audit, and
tests for any new or modified operational surface. `seed_runtime/diagnostic_inventory.py`
declares diagnostic shape fields including flags, JSON support, record scope,
event-ledger writes, and mutation boundaries.

#### Current mitigation

`DIAGNOSTIC_INVENTORY`, `diagnostic_shape_audit`, and tests enforce the contract.
The live shape audit reported zero mismatches and zero warnings.

#### Remaining gap

Every new surface can reintroduce the pressure. The pressure is a recurring
maintenance invariant rather than a one-time defect.

#### Smallest plausible next slice

No implementation slice is indicated unless a new surface is added. For the next
changed diagnostic surface, enforce the existing inventory/shape/test update path.

### 8. Documentation structure and prose visibility pressure

#### Observed recurrence

Repository scale makes prose difficult to assess mentally. Structure visibility is
safer than semantic interpretation.

#### Supporting evidence

`docs/repository_prose_structure_visibility_investigation.md` supports observing
repository-visible document structure before interpreting prose meaning.
`seed_runtime/diagnostic_inventory.py` registers `documentation_structure` with
mechanical structural flags and an explicit boundary against interpreting prose,
extracting claims, inferring authority, or promoting ontology.

#### Current mitigation

Seed has a `documentation_structure` diagnostic for mechanical document structure
and structural recurrence.

#### Remaining gap

Meaning, authority, claim ownership, and pressure recurrence cannot be inferred
automatically from structure alone.

#### Smallest plausible next slice

Add or update one test around an existing structural flag, such as missing front
matter or empty sections, if a specific recurring documentation hygiene problem is
observed.

### 9. Residual-pressure / closure pressure

#### Observed recurrence

Implementation does not automatically eliminate pressure. Some relationships are
preserved, but pressure may remain active if workers still reconstruct the same
relationship manually.

#### Supporting evidence

`docs/inquiry_closure_satisfaction_and_residual_pressure_investigation.md`
distinguishes implemented from resolved and lists recurring manually reconstructed
relationships such as predicate-to-observation-domain, pressure-to-observation-space
gap, question-to-answering-surface, surface-to-follow-up-surface, and answer-to-next
investigation.

#### Current mitigation

Seed has relationship-preserving surfaces including reasoning path, selection
path, reference selection, operational story, pressure audit, diagnostic inventory,
and shape audit.

#### Remaining gap

The repository still lacks an implementation-backed way to determine when a
recurring pressure has actually decreased rather than changed vocabulary or moved
surfaces.

#### Smallest plausible next slice

Add one regression-style check for a single preserved relationship, such as
`question -> answering surface` or `predicate -> observation domain`, proving it
no longer requires manual reconstruction for that case.

### 10. Vocabulary compression / lens decomposition pressure

#### Observed recurrence

The repository repeatedly uses broad language to expose a concern, then decomposes
the language when it carries too much explanatory load.

#### Supporting evidence

`docs/surviving_pressure_after_decomposition_observation.md` identifies a recurring
pattern where broad lenses expose pressure, get decomposed, and some concern or
question remains active. The pattern is strongest for learning, orientation,
preservation, selection, activation, understanding, persistence/continuity, and
relevance.

#### Current mitigation

Repository instructions warn that presentation vocabulary is not automatically
repository knowledge and should not be promoted without implementation evidence.

#### Remaining gap

Broad terms remain useful for discovery but can obscure which concrete pressure is
active unless decomposed.

#### Smallest plausible next slice

For one recurring presentation term, add a bounded implementation-backed
reachability or inventory check before treating the term as preserved repository
knowledge.

## Pressures intentionally excluded

- Grand future architecture pressure: excluded because this inventory is not a
  future-state proposal.
- Autonomous-agent strategy pressure: excluded because inspected repository work
  avoids autonomy and planning proposals for these questions.
- New ontology pressure: excluded because multiple repository sources explicitly
  warn against treating visibility vocabulary as ontology.
- State Summary as the central pressure: excluded because evidence points to
  broader question-to-surface and entrypoint pressure rather than State Summary
  alone.
- Diagnostic shape mismatch as currently unresolved: excluded because the live
  shape audit reported zero mismatches and zero warnings.
- Current ownership ambiguity as live operational pressure: not ranked higher
  because live operational output reported zero service/storage ambiguities and
  zero insufficient-evidence ownership rows.

## Remaining uncertainties

- This inventory prioritized implementation-backed surfaces and recent pressure,
  navigation, capability, authority, and structure investigations rather than all
  frontier documents.
- Ranking combines live operational output with recurrence in documentation.
- Older pressures may have been reduced by later implementation slices not fully
  inspected here.
- First observed evidence is approximate from inspected repository evidence, not a
  full chronological git-history reconstruction.
- Operator testimony was not used as authority.

## Files changed

- `docs/repository_pressure_inventory.md`

## LOC changed

- 390 lines added
