# Operational Visibility Candidate Characterization

## Scope

This is one investigation. It does not recover implementation, recommend a campaign, rank candidates, merge candidates, search for a family, introduce abstractions, or propose implementation changes.

The investigation applies the same constitutional lens independently to each candidate footing identified by `operational_visibility_boundary_investigation.md`.

Repository authority wins.

## Candidate 1: Operational Surface Discovery != Operational Surface Classification

### Constitutional ownership

Operational Surface Discovery owns discovering implementation-backed operational CLI surfaces from parser declarations and producing surface rows with name, category, registration status, JSON capability, and parser evidence.

Operational Surface Classification must not own discovery of the operational inventory rows. It owns classifying prepared CLI/parser elements into classification rows with classification, reason, registration, and optional category.

### Implementation evidence

- `OperationalSurface` is the discovery row shape: name, category, registered, JSON-capable, and evidence.
- `build_operational_surface_inventory(...)` scans public long parser options, skips auxiliary flags, derives category, checks registry and JSON visibility, records `evidence="argparse"`, and returns sorted `OperationalSurface` rows.
- `_CliSurfaceClassificationInput` is prepared CLI/parser material consumed by classification.
- `build_operational_surface_classification_audit(...)` iterates prepared classification inputs, applies `_classification_for(...)`, and returns `OperationalSurfaceClassificationAudit` rows.

Evidence locations:

- `seed_runtime/operational_surface_inventory.py` lines 68-83.
- `seed_runtime/operational_surface_inventory.py` lines 119-130.
- `seed_runtime/operational_surface_inventory.py` lines 169-216.

### Locality

Implementation-local.

The separation is localized in `seed_runtime/operational_surface_inventory.py` between discovery row construction and classification audit construction.

### Recurrence

No.

Implementation evidence in this investigation shows the boundary once in `seed_runtime/operational_surface_inventory.py`. It does not show the same discovery/classification ownership split recurring across multiple neighborhoods.

### Readiness

Unknown.

### Confidence

Medium-high.

## Candidate 2: Operational Surface Classification != Visibility Coverage Composition

### Constitutional ownership

Operational Surface Classification owns classifying CLI/parser elements into primary surfaces, filters, modifiers, debug surfaces, manual inputs, legacy surfaces, or unknown items, with reasons and registration state.

Visibility Coverage Composition must not own classification. It owns composing discovered operational surfaces and classification rows into coverage counts, unregistered-surface views, unregistered classification counts, and missing-registration impact presentation.

### Implementation evidence

- `OperationalSurfaceClassification` and `OperationalSurfaceClassificationAudit` define classification rows and classification counts.
- `build_operational_surface_classification_audit(...)` produces classification audit items.
- `VisibilityCoverageAudit` stores discovered surfaces plus classifications and owns discovered, registered, unregistered, and unregistered-classification-count views.
- `build_visibility_coverage_audit(...)` composes `build_operational_surface_inventory(...)` and `build_operational_surface_classification_audit(...).items` into a coverage audit.
- `format_visibility_coverage_audit(...)` renders discovered, registered, unregistered counts, unregistered classification counts, missing registration status, and diagnostic-inventory invisibility impact.

Evidence locations:

- `seed_runtime/operational_surface_inventory.py` lines 86-116.
- `seed_runtime/operational_surface_inventory.py` lines 132-166.
- `seed_runtime/operational_surface_inventory.py` lines 195-231.
- `seed_runtime/operational_surface_inventory.py` lines 311-357.

### Locality

Implementation-local.

The separation is localized in `seed_runtime/operational_surface_inventory.py` between classification audit construction and coverage audit composition/presentation.

### Recurrence

No.

Implementation evidence in this investigation shows the boundary once in `seed_runtime/operational_surface_inventory.py`. It does not show this exact classification/coverage-composition ownership split recurring across multiple neighborhoods.

### Readiness

Unknown.

### Confidence

Medium-high.

## Candidate 3: Diagnostic Registry Declaration != Diagnostic Shape Audit Specification

### Constitutional ownership

Diagnostic Registry Declaration owns declaring the operational shape of diagnostic and diagnostic-like CLI surfaces: CLI flags, projected-state use, repo-file use, JSON support, record support, record scope, diagnostic fact emission, cluster fact emission, event-ledger writes, cluster mutation, diagnostic-fact reads, and description.

Diagnostic Shape Audit Specification must not own those registry declarations. It owns implementation specifications used to observe declared fields against implementation evidence: module path, build function, format function, JSON function, record function, CLI flags, JSON CLI flags, repo-file markers, diagnostic-fact read markers, and related implementation markers.

### Implementation evidence

- `DiagnosticInventoryEntry` defines registry declaration fields for diagnostic operational shape.
- The registry declares `operational_surface_inventory`, `visibility_coverage_audit`, and `operational_surface_classification_audit` as read-only, JSON-capable, non-recording surfaces that do not write the event ledger and do not mutate cluster state.
- `AUDIT_FIELDS` defines the fields that diagnostic shape audit checks.
- `DiagnosticImplementationSpec` defines implementation-observation specs separately from registry entries.
- `IMPLEMENTATION_SPECS` separately maps the three operational visibility surfaces to implementation module paths, build functions, format functions, JSON functions, and CLI flags.
- `build_diagnostic_shape_audit(...)` reads CLI source, observes each entry against its implementation spec, and emits per-field declared/observed/status rows.

Evidence locations:

- `seed_runtime/diagnostic_inventory.py` lines 11-32.
- `seed_runtime/diagnostic_inventory.py` lines 232-276.
- `seed_runtime/diagnostic_shape_audit.py` lines 21-45.
- `seed_runtime/diagnostic_shape_audit.py` lines 274-297.
- `seed_runtime/diagnostic_shape_audit.py` lines 711-737.

### Locality

Already shared across multiple neighborhoods.

The registry declaration side is in `seed_runtime/diagnostic_inventory.py`; the shape-audit specification and checking side is in `seed_runtime/diagnostic_shape_audit.py`.

### Recurrence

Yes.

The boundary recurs for each diagnostic inventory entry that has a corresponding implementation spec. In the reviewed Operational Visibility evidence, it appears for:

- `operational_surface_inventory`.
- `visibility_coverage_audit`.
- `operational_surface_classification_audit`.

### Readiness

Unknown.

### Confidence

High.

## Candidate 4: Operational Visibility Surface != Question-Family Presentation

### Constitutional ownership

Operational Visibility Surface owns implementation-backed operational visibility flags and outputs for operational surface inventory, visibility coverage audit, and operational surface classification audit.

Question-Family Presentation must not own those operational visibility surfaces. It owns exact QuestionFamily admission, bounded-work eligibility, optional presentation routing, and bounded ask dispatch through existing selected surfaces.

### Implementation evidence

- The CLI exposes Operational Visibility surfaces as `--operational-surface-inventory`, `--visibility-coverage-audit`, and `--operational-surface-classification-audit`.
- The diagnostic registry declares those Operational Visibility surfaces separately from question-family presentation.
- The shape-audit specs separately identify those Operational Visibility surfaces and their implementation functions.
- `_QuestionFamilyEligibilityInput` is limited to exact QuestionFamily text after inventory admission and explicitly does not own dispatch selection, presentation, rendering, surface arguments, or public result shape.
- `_prepare_question_family_eligibility_input(...)` admits only exact inventory-backed question families and explicitly does not classify free text, select a dispatch surface, validate surface arguments, compose presentation, render output, or mutate runtime state.
- `bounded_work_dispatch_request_for_selection(...)` describes selected bounded-work invocation and explicitly does not decide QuestionFamily lookup, eligibility, bounded work selection, evidence interpretation, answer composition, rendering, or semantic routing.
- `apply_bounded_ask_dispatch(...)` validates bounded ask CLI usage, prepares eligibility input, handles optional presentation routing, validates surface arguments, selects bounded work, and dispatches through existing CLI namespace.

Evidence locations:

- `scripts/seed_local.py` lines 1402-1416.
- `seed_runtime/diagnostic_inventory.py` lines 232-276.
- `seed_runtime/diagnostic_shape_audit.py` lines 274-297.
- `seed_runtime/question_surface_inventory.py` lines 66-95.
- `seed_runtime/question_surface_inventory.py` lines 165-180.
- `scripts/seed_local.py` lines 2202-2290.

### Locality

Already shared across multiple neighborhoods.

The Operational Visibility surface side is visible in `scripts/seed_local.py`, `seed_runtime/diagnostic_inventory.py`, `seed_runtime/diagnostic_shape_audit.py`, and `seed_runtime/operational_surface_inventory.py`. The Question-Family Presentation side is visible in `seed_runtime/question_surface_inventory.py` and bounded ask dispatch in `scripts/seed_local.py`.

### Recurrence

No.

Implementation evidence in this investigation shows a separation between Operational Visibility surfaces and QuestionFamily bounded ask/presentation routing. It does not show this exact boundary recurring elsewhere.

### Readiness

Unknown.

### Confidence

Medium.

Characterization complete.
