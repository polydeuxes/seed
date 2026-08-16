# Seed Self-Knowledge Usefulness Exercise

## Purpose

This report evaluates Seed as a repository self-knowledge tool for an external repository worker. The exercise compares Codex expectations formed from implementation inspection against actual Seed CLI output.

No repository behavior was changed. No diagnostics, tests, or operational surfaces were added.

## Method

1. Inspected implementation and tests for selected self-knowledge surfaces.
2. Formed a Codex expectation for each question before running Seed.
3. Ran the available Seed commands.
4. Compared expectations with observed output.

## Questions Tested

| Question | Implementation inspected | Seed command run | Result |
| --- | --- | --- | --- |
| What projection stages exist, and how does projection compose? | `seed_runtime/projection_shape.py`, `tests/test_projection_shape.py` | `python scripts/seed_local.py --projection-shape` | Supported |
| What shape coverage exists? | CLI parser and diagnostics references for coverage terms | `python scripts/seed_local.py --shape-coverage`; `python scripts/seed_local.py --classification-coverage` | `--shape-coverage` unsupported; classification coverage exists but answers a narrower entity-classification question |
| What is the role of a named component? | `seed_runtime/component_audit.py`, diagnostic inventory and shape-audit specs | `python scripts/seed_local.py --component-audit projection_shape` | Supported |
| What capability pressure exists for `listener_process_inventory`? | `seed_runtime/capability_relationship.py`, capability-needs flow | `python scripts/seed_local.py --capability-relationship listener_process_inventory` | Supported, but no current pressure found |
| What is the relationship between capability pressure and acquisition? | `seed_runtime/capability_relationship.py`, `seed_runtime/privilege_discovery.py` | `python scripts/seed_local.py --capability-relationship listener_process_inventory` | Supported as a boundary statement, not acquisition guidance |
| What current operational focus does Seed report? | `seed_runtime/operational_story.py`, pressure/correlation/impact composition | `python scripts/seed_local.py --operational-story` | Supported |
| Are diagnostic surfaces registered and implementation-shape checked? | `seed_runtime/diagnostic_inventory.py`, `seed_runtime/diagnostic_shape_audit.py` | `python scripts/seed_local.py --diagnostic-shape-audit --status mismatch` | Supported; no mismatches reported |

## Detailed Findings

### 1. Projection stages and composition

#### Codex expectation

From `seed_runtime/projection_shape.py`, Codex expected Seed to report a read-only projection map with named stages including event replay, alias projection, measurement retention, inference, fact support projection, legacy and catalog relationship projection, entity type assertion projection, graph issue construction, fact conflict handling, and measurement evidence scan. Codex also expected each stage to show consumed inputs, produced outputs, influence/non-influence, authority boundary, and implementation-backed confidence.

#### Seed output summary

`python scripts/seed_local.py --projection-shape` printed:

- A boundary block: read-only, no event ledger writes, no cluster mutation.
- Stage rows for projection stages.
- For each stage: consumes, produces, influences, optional does-not-influence, authority boundary, and confidence.
- Explicit non-influence examples, such as fact support not influencing relationship projection.

#### Match / mismatch

- **Match:** Seed output matched the implementation shape and tests. It exposed composition without requiring manual reconstruction from projection internals.
- **Good:** The surface clearly distinguishes influence from non-influence and authority boundaries.
- **Bad:** The output is a static stage inventory. It does not drill into source line evidence or show why a stage exists beyond `Confidence: implementation_backed`.
- **Surprise:** `measurement_evidence_scan` appears as a projection-boundary stage with no `Does Not Influence` line because its non-influence tuple is empty. That is consistent with rendering behavior, but a reader might wonder whether the absence is meaningful or omitted.

### 2. Shape coverage

#### Codex expectation

The prompt named `seed --shape-coverage` as an example. Before running Seed, Codex expected either a direct shape-coverage surface or a related coverage diagnostic. Repository inspection showed classification coverage and visibility coverage surfaces, but not an argparse flag named `--shape-coverage`.

#### Seed output summary

`python scripts/seed_local.py --shape-coverage` failed with argparse's unrecognized argument error.

`python scripts/seed_local.py --classification-coverage` succeeded and reported entity classification coverage totals. In the default repository state used for the exercise, it reported zero entities, zero classified entities, zero unknown entities, and no unknown contributor examples.

#### Match / mismatch

- **Match:** The unavailable command matched parser evidence: `--shape-coverage` is not an actual CLI flag.
- **Mismatch:** If a worker expects a generic shape-coverage command from repo vocabulary, Seed does not provide that exact surface.
- **Good:** The failure is clear and authoritative: the CLI rejects the non-existent flag.
- **Bad:** Discoverability is weak. A worker must already know whether to use classification coverage, visibility coverage audit, projection shape, or diagnostic shape audit for different meanings of “shape coverage.”
- **Unsupported conclusion:** The successful classification coverage command does not prove generic repository shape coverage. It only answers entity classification coverage for projected state.

### 3. Named component role: `projection_shape`

#### Codex expectation

From `seed_runtime/component_audit.py`, Codex expected component audit to scan repository files, identify definitions, references, tests, consumers, architecture evidence, operational graph evidence, unresolved questions, and a read-only boundary. For `projection_shape`, Codex expected an active component because it has implementation, tests, diagnostic inventory registration, shape-audit registration, and CLI integration.

#### Seed output summary

`python scripts/seed_local.py --component-audit projection_shape` reported:

- Status: `active`.
- Definitions: `seed_runtime/projection_shape.py` and an investigation doc.
- References in diagnostic inventory, diagnostic shape audit, tests, docs, and `scripts/seed_local.py`.
- Tests: `tests/test_projection_shape.py`.
- Consumers: `state_build` and `views`.
- Operational graph evidence: one diagnostic node and two consumer edges.
- Boundary: read-only, no event ledger writes, no cluster mutation.
- No unresolved questions.

#### Match / mismatch

- **Match:** Seed matched Codex's expectation that `projection_shape` is active and integrated.
- **Good:** This was one of the most useful surfaces. It answered component role, test coverage, consumers, and operational graph participation in one command.
- **Bad:** It over-includes docs as “definitions” when a document name contains the component term. That may be useful evidence, but it is not the same kind of definition as `seed_runtime/projection_shape.py`.
- **Bad:** The component audit identifies consumers as `state_build` and `views`, but it does not explain direct versus indirect consumption in detail.

### 4. Capability pressure for `listener_process_inventory`

#### Codex expectation

From `seed_runtime/capability_relationship.py`, Codex expected the relationship command to build from current capability needs, filter by exact capability name, and only report capabilities present in current pressure inputs. It should not recommend acquisition. If no need exists for the filtered capability, it should report no capability pressure and preserve a read-only boundary.

#### Seed output summary

`python scripts/seed_local.py --capability-relationship listener_process_inventory` reported no capability pressure identified by current audit inputs and printed a boundary stating no recording, event ledger writes, cluster mutation, acquisition, policy, or planning.

#### Match / mismatch

- **Match:** The command behaved as expected for an absent current need.
- **Good:** Seed preserved unknown/absent pressure rather than inventing acquisition guidance.
- **Good:** The boundary statement directly addresses the relationship between pressure and acquisition: this surface is context, not acquisition logic.
- **Bad:** For a filtered capability with no current pressure, the output does not distinguish “capability is unknown to Seed” from “capability is known but not currently pressured.” A worker needs implementation inspection or other commands to tell the difference.

### 5. Relationship between capability pressure and acquisition

#### Codex expectation

Codex expected capability pressure to be visibility context and not operator intent. The implementation hard-codes `attainability="unknown"` and `expectation="unknown"`, and includes reasoning that deployment intent and acquisition are outside the read-only surface.

#### Seed output summary

Because `listener_process_inventory` had no current pressure, the command did not show an individual capability row. It still printed the boundary excluding acquisition, policy, planning, recording, ledger writes, and mutation.

#### Match / mismatch

- **Partial match:** The output communicated the acquisition boundary, but did not show the richer per-capability reasoning because the filtered capability was absent from current needs.
- **Good:** Seed did not overclaim.
- **Bad:** To evaluate the full relationship model, a worker must choose a capability that is currently pressured, or run the command without a filter. The filtered absent case is safe but not very explanatory.
- **Unsupported conclusion:** This run cannot conclude anything about `listener_process_inventory` attainability or expectation, because Seed did not report an active relationship row for it.

### 6. Current operational focus

#### Codex expectation

From `seed_runtime/operational_story.py`, Codex expected operational story to compose pressure audit, capability needs, privilege discovery, correlation audit, impact audit, and investigation path into a read-only summary. It should identify a primary focus if pressure exists, include evidence, constraints, correlation gaps, recent changes/outcomes, unknowns, and a boundary.

#### Seed output summary

`python scripts/seed_local.py --operational-story` reported:

- Current focus: `orphaned predicates`.
- Primary pressure: 21 orphaned predicate pressure points.
- Supporting evidence: consumer audit found observation predicates without implementation consumers, listing affected predicates.
- Missing capabilities and access constraints: none observed.
- Correlation gap: consumer audit predicates or diagnostics without implementation consumers remain explanatory only.
- Recent changes: unknown.
- Observed outcomes: several impact metrics unknown.
- Investigation path: consumer audit, observation utilization, correlation audit, operational surface inventory.
- Unknowns for capabilities and impact.
- Boundary: read-only view with no recording, event ledger writes, cluster mutation, plans, or implementation advice.

#### Match / mismatch

- **Match:** Seed matched the composition expected from implementation inspection.
- **Good:** It gave a useful operational headline without requiring manual traversal of pressure, consumer, correlation, and impact audits.
- **Good:** It preserved unknowns and did not convert pressure into a plan.
- **Bad:** It is broad. The worker gets a good headline but limited evidence depth unless they already know which follow-up command to run.
- **Bad:** “Current focus” may sound authoritative as repository priority, but implementation shows it is derived from the top pressure-audit item, not an operator-authored priority.

### 7. Diagnostic shape audit consistency

#### Codex expectation

From diagnostic inventory and shape-audit implementation specs, Codex expected registered diagnostics to be checked for parser flags, implementation files/functions, JSON/record support, and declared boundaries. Because the repository tests include shape-audit consistency checks, Codex expected no mismatches in the current tree.

#### Seed output summary

`python scripts/seed_local.py --diagnostic-shape-audit --status mismatch` reported no matching mismatch rows. It summarized 36 diagnostics audited, 324 consistent rows, zero warnings, zero mismatches, and zero unknown rows.

#### Match / mismatch

- **Match:** Seed matched implementation/test expectations.
- **Good:** This surface is useful repository self-knowledge because it checks whether diagnostic inventory claims match implementation shape.
- **Bad:** The mismatch-filtered output is excellent for health checks but less useful for learning what each diagnostic does. A worker needs `--diagnostic-inventory` or unfiltered shape audit for broader understanding.

## Goods Observed

- Seed answered projection composition without requiring manual reconstruction.
- Seed preserved authority boundaries: read-only, no event ledger writes, no cluster mutation.
- Seed exposed non-influence for projection stages where encoded.
- Seed connected a named component to definitions, references, tests, consumers, and operational graph evidence.
- Seed preserved unknowns in operational story and impact outcomes.
- Seed did not turn capability pressure into acquisition guidance.
- Seed surfaced useful next questions through operational story's investigation path.
- Diagnostic shape audit gave a concise consistency health check for self-knowledge surfaces.

## Bads Observed

- `--shape-coverage` does not exist, and the closest surfaces are not obvious from the phrase “shape coverage.”
- Some surfaces require prior knowledge of exact diagnostic names and filters.
- Component audit can blur implementation definitions and documentation evidence.
- Capability relationship output for an absent filtered capability does not distinguish unknown capability from known-but-unpressured capability.
- Operational story is useful but broad; it does not expose deep source evidence inline.
- Projection shape says `implementation_backed` but does not show source evidence or dynamic validation details.
- Some labels, such as “Current Focus,” could be mistaken for operator intent rather than derived pressure ranking.

## Surprising Results

- The prompt's example `--shape-coverage` was not available, while related coverage surfaces exist under different names.
- `projection_shape` component audit found documentation as a definition due to name-based definition heuristics.
- The current operational story focused on orphaned predicates, not capability acquisition or projection shape.
- The capability relationship filter produced no row for `listener_process_inventory`, making the boundary visible but not the full per-capability relationship model.

## Unsupported Conclusions

This exercise does not establish:

- That generic “shape coverage” exists as a Seed concept or command.
- That `listener_process_inventory` is attainable, expected, or desired.
- That operational story's current focus is an operator-approved priority.
- That projection shape is complete beyond the implementation-backed registry in `seed_runtime/projection_shape.py`.
- That classification coverage represents repository shape coverage.

## Recommended Follow-Up Questions

1. Which command should a new worker use for each meaning of “shape”: projection shape, diagnostic shape, entity classification shape, visibility coverage, and repository shape?
2. Can component audit separate code definitions from documentation evidence more explicitly?
3. Can capability relationship distinguish “filtered capability absent from current needs” from “unknown capability name”?
4. Can operational story link each headline to the best drill-down command and evidence source?
5. Can projection shape expose source evidence or a validation route for each stage?
6. Should `--diagnostic-inventory` include a task-oriented index for common worker questions?
7. Should derived labels such as “Current Focus” explicitly say “derived from pressure audit” in human-readable output?

## Overall Evaluation

Seed currently helps Codex understand Seed, especially for implementation-backed diagnostic surfaces. The strongest self-knowledge surfaces in this exercise were `--projection-shape`, `--component-audit projection_shape`, `--operational-story`, and `--diagnostic-shape-audit --status mismatch`.

Seed behaves as expected when the worker knows the correct command name and when the question maps directly to an implemented surface. It is weaker when repository vocabulary is ambiguous, when a filtered query has no current row, or when a broad summary needs evidence drill-down.

The most useful surfaces are those that combine implementation evidence, boundary statements, and next-step visibility. The surfaces most needing refinement are command discoverability around “shape coverage,” filtered capability absence semantics, component evidence typing, and source-evidence drill-down for broad summaries.
