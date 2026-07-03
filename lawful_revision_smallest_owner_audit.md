# Lawful Revision Smallest Owner Audit

## Smallest truthful answer

The repository does **not** currently recover one universal implementation-backed owner for the full grammar of lawful revision. The smallest truthful implementation-backed answer is narrower:

- **Bounded ask dispatch** owns a local revise-by-restriction grammar for exact question-family invocation: current family inventory and maps, incoming operator invocation, exact insufficiency in the invocation, preservation of existing surface mappings, one selected existing surface when eligible, and lawful stop through either parser error, presentation mode, or dispatch. It explicitly refuses evidence interpretation, answer composition, rendering, and semantic routing (`seed_runtime/question_surface_inventory.py:126-131`, `seed_runtime/question_surface_inventory.py:155-160`).
- **Diagnostic shape audit** owns a local declaration-vs-observed-shape comparison grammar for diagnostic surfaces: declared inventory shape, static implementation spec, row-level inconsistency status, and summary. It does not revise the surface; it exposes mismatch/warning/unknown (`seed_runtime/diagnostic_shape_audit.py:14-31`, `seed_runtime/diagnostic_shape_audit.py:55-70`).
- **Inquiry orientation** owns a local evidence-then-answer boundary for orientation notes: preserve note prose, collect deterministic repository evidence, compose an answer, preserve authority/uncertainty, and stop without facts, goals, commands, actions, or mutation (`seed_runtime/inquiry_orientation.py:1-7`, `seed_runtime/inquiry_orientation.py:22-38`, `seed_runtime/inquiry_orientation.py:143-170`).
- **Pressure audit** owns a local pressure-ranking grammar from existing audits: consume existing surface evidence, expose pressure categories and inspection commands, and stop without planning, recording, or mutation (`seed_runtime/pressure_audit.py:64-87`, `seed_runtime/pressure_audit.py:94-120`).

Across these families, the recurring grammar currently lives as a **cross-family recurring implementation pattern plus report methodology**, not as an implemented `lawful_revision` engine or single architecture owner.

## Evidence reviewed

Implementation-backed surfaces reviewed:

- `seed_runtime/pressure_audit.py`: pressure items include evidence, reason, and recommended inspection; the builder aggregates only existing visibility surfaces and is documented as read-only/no planning/no mutation (`seed_runtime/pressure_audit.py:10-17`, `seed_runtime/pressure_audit.py:64-87`).
- `seed_runtime/inquiry_orientation.py`: inquiry notes are preserved outside the event ledger; orientation collects implementation-local evidence, composes a separate answer, carries boundary/limitations, and renders without creating runtime truth (`seed_runtime/inquiry_orientation.py:1-7`, `seed_runtime/inquiry_orientation.py:72-87`, `seed_runtime/inquiry_orientation.py:157-170`).
- `seed_runtime/question_surface_inventory.py`: exact question-family maps, eligibility, selected bounded work, dispatch requests, and explicit non-ownership clauses for semantic routing and answer composition (`seed_runtime/question_surface_inventory.py:10-24`, `seed_runtime/question_surface_inventory.py:66-99`, `seed_runtime/question_surface_inventory.py:123-131`, `seed_runtime/question_surface_inventory.py:151-160`, `seed_runtime/question_surface_inventory.py:176-211`).
- `scripts/seed_local.py`: actual bounded ask parser behavior, exact-family validation, parameter-count validation, diagnostic-only rejection, not-dispatchable rejection, presentation stop, and dispatch (`scripts/seed_local.py:2201-2285`).
- `seed_runtime/diagnostic_inventory.py`: declared operational diagnostic shape, including record scope, event-ledger writes, and cluster mutation fields (`seed_runtime/diagnostic_inventory.py:11-35`).
- `seed_runtime/diagnostic_shape_audit.py`: static implementation specs and audit fields comparing declared to observed diagnostic behavior (`seed_runtime/diagnostic_shape_audit.py:21-52`, `seed_runtime/diagnostic_shape_audit.py:55-80`).

Prior audit/report documents were useful as navigation evidence, but this characterization treats implementation and tests as authority and does not promote report vocabulary into architecture.

## Core grammar audit

| Grammar stage | Implementation-backed recurrence | Characterization |
| --- | --- | --- |
| Current lawful explanation | Present locally in inventory rows, diagnostic declarations, orientation boundary, and pressure audit inputs. | Family-local, not universal. |
| Incoming implementation-backed evidence | Present in diagnostic shape specs, existing audit outputs consumed by pressure, projected/source-navigation material consumed by orientation, and exact CLI arguments consumed by bounded ask. | Recurs independently. |
| Exact insufficiency exposed | Present in bounded ask parser errors and eligibility reasons; present in diagnostic shape row statuses; present as pressure categories/counts. | Strongest in bounded ask and diagnostic shape audit. |
| Still-valid structure preserved | Present through map-backed dispatch to existing surfaces, diagnostic inventory declarations retained as declarations, orientation note preservation, and read-only pressure aggregation. | Recurs, but each owner preserves its own structure only. |
| Smallest lawful revision identified | Bounded ask selects only an existing surface or rejects; pressure recommends inspection, not repair; diagnostic shape audit identifies mismatch/warning/unknown but does not revise; orientation composes related material only. | No cross-family revision owner. |
| Lawful stop | Parser errors/returns, read-only formatter summaries, no mutation boundaries, and explicit diagnostic rows. | Recurs strongly. |

## Candidate owner audit

### Pressure

- Consumes a current explanation? **Partially.** It consumes existing visibility surfaces and turns them into pressure items.
- Compares incoming implementation evidence? **Yes, locally.** Diagnostic shape summary, ownership discrepancies, capability needs, and consumer audit outputs are converted to scored pressure categories.
- Identifies insufficiency? **Yes.** Categories such as diagnostic shape, ownership attribution, capability, and orphaned/fragile predicates expose bounded pressure.
- Preserves lawful surrounding structure? **Yes.** It is read-only and aggregates existing surfaces rather than replacing them.
- Identifies the smallest lawful revision? **No.** It identifies a recommended inspection command, not a code revision.
- Terminates lawfully? **Yes.** It returns no pressure or a finite sorted pressure list.
- Locality: **implementation-local pressure owner**, not lawful revision owner.

### Inquiry Orientation

- Consumes a current explanation? **Partially.** It consumes preserved inquiry-note prose and projected/source-navigation material.
- Compares incoming implementation evidence? **Yes, locally.** It deterministically matches lexical tokens against already projected/read-model material.
- Identifies insufficiency? **Only as orientation uncertainty/absence.** It does not identify implementation insufficiency requiring revision.
- Preserves lawful surrounding structure? **Yes.** Raw notes are preserved as prose and not facts, claims, goals, requirements, commands, or runtime instructions.
- Identifies the smallest lawful revision? **No.** It identifies related material, not a revision.
- Terminates lawfully? **Yes.** It produces a bounded view with uncertainty and authority boundary.
- Locality: **implementation-local orientation owner**, not lawful revision owner.

### Bounded Ask

- Consumes a current explanation? **Yes.** It consumes exact question-family inventory and dispatch maps.
- Compares incoming implementation evidence? **Yes.** It compares `ask --question-family` invocation and surface args against inventory, eligibility, and dispatch maps.
- Identifies insufficiency? **Yes.** Unknown families, wrong invocation shape, missing/excess args, diagnostic-only families, and not-dispatchable families are rejected exactly.
- Preserves lawful surrounding structure? **Yes.** It selects only existing dispatch surfaces and refuses semantic routing, evidence interpretation, answer composition, and rendering.
- Identifies the smallest lawful revision? **Yes, within its family.** The smallest action is either one existing dispatch-surface flag/value mutation on the CLI namespace or a parser stop.
- Terminates lawfully? **Yes.** It returns after presentation mode, dispatch, inventory mode, or parser error.
- Locality: **implementation-local and question-family-local owner of bounded invocation repair/selection**, but not universal lawful revision.

### Question Surface Inventory

- Consumes a current explanation? **Yes.** Rows declare question families, surfaces, answer responsibility, authority boundary, bounded status, and diagnostic relationships.
- Compares incoming implementation evidence? **Partially.** `bounded_ask_inventory_findings()` checks inventory rows against dispatch maps.
- Identifies insufficiency? **Partially.** It finds duplicate families and orphaned dispatch mappings, but does not perform runtime revision.
- Preserves lawful surrounding structure? **Yes.** Rows state inventory-only status and do not route operator questions.
- Identifies the smallest lawful revision? **No.** It reports inventory findings; it does not revise maps.
- Terminates lawfully? **Yes.** It returns deterministic rows/findings.
- Locality: **family-local inventory owner**, not revision owner.

### Implementation Readiness

No single reviewed implementation named a universal implementation-readiness owner for lawful revision. Capability promotion readiness exists as a narrow inspection pattern in tests and runtime exports, but the evidence reviewed here supports readiness as an inspection/refusal boundary, not a lawful revision engine. Locality: **unsupported as candidate owner for the full grammar**.

### Diagnostic Shape Audit

- Consumes a current explanation? **Yes.** It consumes diagnostic inventory declarations.
- Compares incoming implementation evidence? **Yes.** It compares declarations to static implementation specs and source markers.
- Identifies insufficiency? **Yes.** Rows classify fields as consistent, warning, mismatch, or unknown.
- Preserves lawful surrounding structure? **Yes.** It audits shape without mutating diagnostics.
- Identifies the smallest lawful revision? **No.** It identifies exact mismatch fields, not repair patches.
- Terminates lawfully? **Yes.** It produces finite rows and summaries.
- Locality: **implementation-local diagnostic governance owner**, not lawful revision owner.

### Answer Composition

Answer composition recurs locally in inquiry orientation and question-family explanation structures, but the reviewed implementation does not show a universal answer-composition owner that consumes a current lawful explanation, exposes insufficiency, preserves surrounding structure, revises only a region, and stops. Locality: **family-local composition pattern**.

### Compatibility Recovery

Compatibility preservation is strongly recurrent in tests and handoff patterns, but the evidence reviewed supports it as a constraint on local changes rather than an owner of lawful revision. It says what must survive unchanged; it does not itself choose or perform revisions. Locality: **cross-family constraint/pattern**.

### Report Methodology

The full six-stage grammar appears most completely in reports and investigations as a reading discipline: existing explanation, implementation evidence, insufficiency, preservation, smallest characterization, stop. Because no implementation-local `lawful_revision` owner exists, the full grammar currently lives partly as **methodology-local audit discipline**.

## Neighbor analysis

- **Lawful revision is not Pressure.** Pressure ranks operational concerns and recommends inspection commands; it does not revise implementation (`seed_runtime/pressure_audit.py:20-35`, `seed_runtime/pressure_audit.py:94-120`).
- **Lawful revision is not Orientation.** Orientation preserves inquiry notes and exposes related material/uncertainty without turning prose into truth or action (`seed_runtime/inquiry_orientation.py:22-38`, `seed_runtime/inquiry_orientation.py:90-113`).
- **Lawful revision is not Bounded inquiry.** Bounded ask can select or reject an existing surface, but it explicitly excludes semantic routing and answer/evidence interpretation (`seed_runtime/question_surface_inventory.py:123-131`, `scripts/seed_local.py:2229-2277`).
- **Lawful revision is not Implementation readiness.** Readiness-like inspections can show support or missing support, but the reviewed evidence does not make them revision owners.
- **Lawful revision is not Answer composition.** Composition prepares bounded answer payloads; it does not own implementation repair.
- **Lawful revision is not Compatibility preservation.** Compatibility constrains what remains valid; it is not the owner that decides a revision.

These distinctions independently recur because each owner declares or implements negative authority: bounded ask excludes semantic routing and answer composition; inquiry orientation excludes facts/claims/goals/actions; diagnostic inventory distinguishes record/event/mutation fields (`seed_runtime/diagnostic_inventory.py:11-27`); pressure audit excludes planning/recording/mutation.

## Negative authority

Implementation-backed negative authority recovered:

- **Global replacement is not local revision.** Bounded ask dispatch maps only exact families to existing surfaces and rejects unknown/not-dispatchable families rather than inventing a route (`seed_runtime/question_surface_inventory.py:10-24`, `scripts/seed_local.py:2229-2277`).
- **Discarding lawful structure is not repairing lawful insufficiency.** Inquiry orientation preserves raw note prose and projected state boundaries instead of converting prose into facts or commands (`seed_runtime/inquiry_orientation.py:22-38`, `seed_runtime/inquiry_orientation.py:90-113`).
- **Broad redesign is not implementation-backed revision.** Pressure audit recommends inspection commands from existing audits; it does not plan or mutate (`seed_runtime/pressure_audit.py:64-87`, `seed_runtime/pressure_audit.py:123-165`).
- **Universal revision engine is not local implementation owner.** Diagnostic shape audit compares declared/observed fields for registered diagnostics only; bounded ask selects exact existing surfaces only; orientation handles notes only (`seed_runtime/diagnostic_shape_audit.py:21-31`, `seed_runtime/question_surface_inventory.py:176-211`, `seed_runtime/inquiry_orientation.py:143-170`).

## Locality determination

Current locality is **cross-family recurring implementation pattern plus methodology-local full grammar**.

- **Implementation-local:** bounded ask dispatch, diagnostic shape audit, inquiry orientation, pressure audit.
- **Family-local:** question-family selection/dispatch; diagnostic surface shape governance; inquiry-note orientation; pressure ranking.
- **Cross-family recurring implementation:** preserve boundaries, expose exact insufficiency, reject overreach, and stop lawfully.
- **Methodology-local:** full lawful-revision grammar as a named six-stage audit pattern.
- **Constitutional:** only as repeated negative authority and preservation discipline; not as one implemented constitutional transition owner.
- **Still unknown:** whether a future implementation-eligible owner should exist, and what would admit/retire revisions.

## Typed unknowns

- **Universal lawful revision owner:** unknown; not recovered in current implementation.
- **Revision admission thresholds:** unknown beyond local eligibility/status checks.
- **Revision retirement:** unknown; no reviewed owner retires a revision grammar.
- **Cross-family revision coordination:** unknown; current families compose by visibility and boundaries, not by a shared revision coordinator.
- **Implementation eligibility for future slices:** unknown; current evidence supports characterization only, not recommendation.

## Lawful termination

This audit stops at characterization because repository authority does not show a universal lawful revision engine. The recurring grammar is earned as local patterns and methodology, but the smallest implementation-backed owner for the full grammar is **not present**. No implementation recommendation follows.

## Remaining questions

1. Can future evidence show a current implementation owner that consumes explanations, compares evidence, identifies insufficiency, preserves valid structure, performs smallest revision, and stops across multiple families?
2. Are admission thresholds intentionally family-local, or merely unrecovered?
3. Does any current diagnostic or inventory surface encode revision retirement, or is retirement outside implementation authority?
4. Can compatibility-preserving slices coordinate without becoming a universal revision engine?

## Confidence

**Medium-high.** Confidence is high that bounded ask, diagnostic shape audit, inquiry orientation, and pressure audit own only local bounded behaviors. Confidence is medium that no smaller universal owner exists because the review sampled the requested families and major implementation surfaces, but did not prove absence across every file in the repository.
