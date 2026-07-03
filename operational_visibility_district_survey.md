# Operational Visibility District Survey

## Scope

This is one district survey. It does not recover implementation, recommend slices, authorize a campaign, rank neighborhoods, compare neighborhoods, search for ownership, redesign diagnostics, redesign CLI, or redesign runtime.

The bounded question is:

```text
What implementation neighborhoods
are presently visible
inside Operational Visibility?
```

Repository authority wins.

## District overview

Operational Visibility is presently visible as an implementation-backed district that exposes, declares, checks, and presents visibility about operational CLI surfaces and diagnostic-like surfaces.

The district is not visible as a new structure needing creation. It is visible through existing implementation neighborhoods:

- CLI operational visibility surface exposure;
- operational surface discovery;
- operational surface classification;
- visibility coverage composition;
- diagnostic inventory registry declaration;
- diagnostic shape verification;
- operational visibility presentation and JSON output.

The district is implementation-backed by app flags for `--operational-surface-inventory`, `--visibility-coverage-audit`, and `--operational-surface-classification-audit`; by operational surface inventory, classification, coverage, formatting, and JSON functions; by diagnostic inventory declarations for those surfaces; and by diagnostic shape audit implementation specs and checks for those declarations.

## Visible neighborhoods

### 1. CLI operational visibility surface exposure

#### Identity

This neighborhood exposes Operational Visibility as app-level CLI surfaces. The visible work is declaring operator-facing flags that invoke operational surface inventory, visibility coverage audit, and operational surface classification audit.

#### Evidence

- The CLI parser declares `--operational-surface-inventory` with help text for discovering operational CLI surfaces from implementation evidence.
- The CLI parser declares `--visibility-coverage-audit` with help text for auditing which discovered operational surfaces are visible in diagnostic inventory.
- The CLI parser declares `--operational-surface-classification-audit` with help text for classifying discovered CLI elements.

Evidence locations:

- `scripts/seed_local.py` lines 1402-1416.

#### Boundaries

Visible neighboring neighborhoods touched:

- Operational surface discovery.
- Visibility coverage composition.
- Operational surface classification.
- Diagnostic inventory registry declaration.
- Diagnostic shape verification.
- Question-family / bounded ask dispatch is visibly adjacent but not characterized as inside this neighborhood.

#### Maturity

Shared.

The surface declarations are in the app CLI, while the invoked operational visibility implementations, registry declarations, and shape-audit specs are in runtime modules.

#### Internal pressure

Yes.

The neighborhood exposes multiple Operational Visibility flags that must remain visible to the registry and shape audit.

### 2. Operational surface discovery

#### Identity

This neighborhood discovers implementation-backed operational CLI surfaces from parser declarations. The visible work is scanning public long options, excluding auxiliary flags, mapping operational keywords to categories, and producing `OperationalSurface` rows with registration, JSON capability, and parser evidence.

#### Evidence

- `OperationalSurface` defines the discovered surface row shape: name, category, registered, JSON-capable, and evidence.
- `_OPERATIONAL_KEYWORDS` and `_AUXILIARY_FLAGS` provide implementation-local discovery vocabulary and exclusions.
- `build_operational_surface_inventory(...)` scans parser actions, skips auxiliary flags, derives category, checks diagnostic registration and JSON visibility, records `evidence="argparse"`, and returns sorted discovered surfaces.

Evidence locations:

- `seed_runtime/operational_surface_inventory.py` lines 15-37.
- `seed_runtime/operational_surface_inventory.py` lines 68-83.
- `seed_runtime/operational_surface_inventory.py` lines 169-192.
- `seed_runtime/operational_surface_inventory.py` lines 360-380.

#### Boundaries

Visible neighboring neighborhoods touched:

- CLI operational visibility surface exposure.
- Operational surface classification.
- Visibility coverage composition.
- Diagnostic inventory registry declaration.
- Operational visibility presentation and JSON output.

#### Maturity

Implementation-local.

The discovery row, discovery vocabulary, parser scan, registration check, and JSON-capability check are concentrated in `seed_runtime/operational_surface_inventory.py`.

#### Internal pressure

Yes.

Discovery visibly combines parser evidence, category vocabulary, registry registration, JSON visibility, and auxiliary exclusions.

### 3. Operational surface classification

#### Identity

This neighborhood classifies CLI/parser elements into visibility-relevant classes. The visible work is preparing parser material, applying classification rules, and producing an audit with counts and per-surface classification rows.

#### Evidence

- `OperationalSurfaceClassification` defines classification rows with surface, classification, reason, registration, and optional category.
- `OperationalSurfaceClassificationAudit` owns classification counts and JSON output.
- `_CliSurfaceClassificationInput` carries prepared CLI/parser surface material consumed by classification.
- `build_operational_surface_classification_audit(...)` prepares parser inputs, classifies each prepared input, and returns sorted audit items.
- The formatter names classification buckets for primary surfaces, debug surfaces, filters, modifiers, manual inputs, legacy surfaces, and unknowns.

Evidence locations:

- `seed_runtime/operational_surface_inventory.py` lines 86-130.
- `seed_runtime/operational_surface_inventory.py` lines 195-216.
- `seed_runtime/operational_surface_inventory.py` lines 276-308.

#### Boundaries

Visible neighboring neighborhoods touched:

- CLI operational visibility surface exposure.
- Operational surface discovery.
- Visibility coverage composition.
- Operational visibility presentation and JSON output.
- Diagnostic inventory registry declaration.

#### Maturity

Implementation-local.

Classification shapes, prepared input, audit construction, counts, and presentation buckets are concentrated in `seed_runtime/operational_surface_inventory.py`.

#### Internal pressure

Yes.

Classification visibly handles many categories, reasons, registration state, and unknown outcomes.

### 4. Visibility coverage composition

#### Identity

This neighborhood composes discovered operational surfaces and classification rows into a coverage view. The visible work is counting discovered, registered, and unregistered surfaces; counting unregistered classifications; and identifying missing diagnostic inventory visibility.

#### Evidence

- `VisibilityCoverageAudit` stores discovered surfaces and classifications.
- `VisibilityCoverageAudit.discovered`, `.registered`, `.unregistered`, and `.unregistered_classification_counts` provide coverage views.
- `build_visibility_coverage_audit(...)` composes operational surface inventory and operational surface classification audit results into one coverage audit.
- `format_visibility_coverage_audit(...)` renders discovered, registered, unregistered, unregistered classification counts, missing registration status, and diagnostic inventory invisibility impact.

Evidence locations:

- `seed_runtime/operational_surface_inventory.py` lines 132-166.
- `seed_runtime/operational_surface_inventory.py` lines 219-231.
- `seed_runtime/operational_surface_inventory.py` lines 311-357.

#### Boundaries

Visible neighboring neighborhoods touched:

- CLI operational visibility surface exposure.
- Operational surface discovery.
- Operational surface classification.
- Diagnostic inventory registry declaration.
- Operational visibility presentation and JSON output.

#### Maturity

Compressed.

The neighborhood visibly composes discovery and classification outputs and also presents missing-registration impact from the same module. The survey does not recover a boundary from that compression.

#### Internal pressure

Yes.

Coverage visibly joins discovery, classification, registration counts, unregistered classification counts, and diagnostic-inventory invisibility impact.

### 5. Diagnostic inventory registry declaration

#### Identity

This neighborhood declares operational shape for diagnostic and diagnostic-like surfaces. The visible work is recording CLI flags, projected-state use, repo-file use, JSON support, record support, record scope, diagnostic fact emission, cluster fact emission, event-ledger writes, cluster mutation, diagnostic-fact reads, and description.

#### Evidence

- `DiagnosticInventoryEntry` defines the registry declaration shape.
- The diagnostic inventory declares `operational_surface_inventory`, `visibility_coverage_audit`, and `operational_surface_classification_audit` as JSON-capable, non-recording, non-ledger-writing, non-cluster-mutating surfaces.
- `_DiagnosticInventoryCompositionInput`, `diagnostic_inventory_json(...)`, and `format_diagnostic_inventory(...)` show the registry has composition and output paths for its declarations.

Evidence locations:

- `seed_runtime/diagnostic_inventory.py` lines 11-41.
- `seed_runtime/diagnostic_inventory.py` lines 232-276.
- `seed_runtime/diagnostic_inventory.py` lines 1083-1104.

#### Boundaries

Visible neighboring neighborhoods touched:

- CLI operational visibility surface exposure.
- Operational surface discovery.
- Operational surface classification.
- Visibility coverage composition.
- Diagnostic shape verification.
- Operational visibility presentation and JSON output.

#### Maturity

Shared.

Registry declarations are in `seed_runtime/diagnostic_inventory.py`, while the declared Operational Visibility implementations and shape-audit specs are in other modules.

#### Internal pressure

Yes.

The registry visibly must preserve read-only diagnostic shape for multiple Operational Visibility surfaces while remaining separate from implementation observation.

### 6. Diagnostic shape verification

#### Identity

This neighborhood verifies diagnostic inventory declarations against implementation evidence. The visible work is defining audited fields, declaring implementation specs, observing implementation shape, and producing status rows for declared versus observed behavior.

#### Evidence

- `AUDIT_FIELDS` lists fields checked by diagnostic shape audit.
- `DiagnosticImplementationSpec` defines implementation evidence specs: module path, build function, format function, JSON function, record function, CLI flags, JSON CLI flags, repo-file markers, diagnostic-fact read markers, and mutation markers.
- `IMPLEMENTATION_SPECS` maps `operational_surface_inventory`, `visibility_coverage_audit`, and `operational_surface_classification_audit` to their implementation module paths, build functions, format functions, JSON functions, and CLI flags.
- `build_diagnostic_shape_audit(...)` reads the CLI source, observes each diagnostic entry against its spec, and emits one audit row per audited field.

Evidence locations:

- `seed_runtime/diagnostic_shape_audit.py` lines 21-52.
- `seed_runtime/diagnostic_shape_audit.py` lines 274-297.
- `seed_runtime/diagnostic_shape_audit.py` lines 711-737.

#### Boundaries

Visible neighboring neighborhoods touched:

- CLI operational visibility surface exposure.
- Diagnostic inventory registry declaration.
- Operational surface discovery.
- Operational surface classification.
- Visibility coverage composition.
- Operational visibility presentation and JSON output.

#### Maturity

Shared.

Shape verification is in `seed_runtime/diagnostic_shape_audit.py`, but it checks registry entries from `seed_runtime/diagnostic_inventory.py`, implementation functions in `seed_runtime/operational_surface_inventory.py`, and CLI source in `scripts/seed_local.py`.

#### Internal pressure

Yes.

The neighborhood visibly maintains declaration/spec/implementation consistency across multiple files and multiple Operational Visibility surfaces.

### 7. Operational visibility presentation and JSON output

#### Identity

This neighborhood renders Operational Visibility outputs for operator consumption and JSON consumption. The visible work is converting inventory, classification audit, and coverage audit objects into text and JSON shapes.

#### Evidence

- `operational_surface_inventory_json(...)`, `operational_surface_classification_audit_json(...)`, and `visibility_coverage_audit_json(...)` expose JSON output shapes for the three Operational Visibility surfaces.
- `format_operational_surface_inventory(...)` renders discovered surfaces, categories, JSON capability, and registration status.
- `format_operational_surface_classification_audit(...)` renders classification counts and per-surface classification reasons.
- `format_visibility_coverage_audit(...)` renders coverage counts and missing-registration impact.

Evidence locations:

- `seed_runtime/operational_surface_inventory.py` lines 234-247.
- `seed_runtime/operational_surface_inventory.py` lines 250-273.
- `seed_runtime/operational_surface_inventory.py` lines 276-308.
- `seed_runtime/operational_surface_inventory.py` lines 311-357.

#### Boundaries

Visible neighboring neighborhoods touched:

- CLI operational visibility surface exposure.
- Operational surface discovery.
- Operational surface classification.
- Visibility coverage composition.
- Diagnostic inventory registry declaration.
- Diagnostic shape verification.

#### Maturity

Compressed.

Presentation and JSON output are implemented alongside discovery, classification, and coverage composition in `seed_runtime/operational_surface_inventory.py`. The survey does not recover a boundary from that compression.

#### Internal pressure

Yes.

The neighborhood visibly formats three distinct Operational Visibility outputs and preserves both text and JSON output paths.

## Preserved unknowns

- Whether any visible neighborhood should become a future recovery footing remains unknown.
- Whether Operational Visibility deserves a future campaign remains unknown.
- Whether visibility coverage composition and operational visibility presentation should remain compressed remains unknown.
- Whether diagnostic registry declaration and diagnostic shape verification are separate neighborhoods by design or by current implementation arrangement remains unknown.
- Whether unregistered operational surfaces represent intentional CLI behavior, diagnostic inventory debt, or classification overreach remains unknown.
- Whether question-family presentation belongs near Operational Visibility remains unknown; current evidence only shows adjacency through CLI and bounded ask dispatch.
- Whether additional Operational Visibility neighborhoods exist outside the reviewed implementation remains unknown.

## Confidence

Confidence: medium-high.

Reason: the visible neighborhoods are supported by direct implementation evidence in the CLI, operational surface inventory implementation, diagnostic inventory registry, and diagnostic shape audit. Confidence is not high because the survey intentionally stayed at district resolution and reviewed only implementation necessary to characterize Operational Visibility.

District survey complete.
