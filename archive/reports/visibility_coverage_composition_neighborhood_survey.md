# Visibility Coverage Composition Neighborhood Survey

## Scope

This is one neighborhood survey. It answers only:

```text
What implementation neighborhood
is Visibility Coverage Composition?
```

It does not recover ownership, characterize bridges, recommend slices, authorize a campaign, redesign Operational Visibility, or create a new neighborhood.

Repository authority wins.

## Neighborhood identity

Visibility Coverage Composition is the implementation neighborhood that composes implementation-discovered operational surfaces with CLI-surface classification rows into a coverage audit.

The work inside this neighborhood is to report how many operational surfaces were discovered, how many are registered in diagnostic inventory, which discovered surfaces remain unregistered, what classifications those unregistered surfaces have, and what diagnostic-inventory visibility impact is rendered for missing registrations.

## Implementation evidence

The neighborhood is visible in implementation evidence through:

- `VisibilityCoverageAudit`, which stores `surfaces` and `classifications` as the composed coverage audit state.
- `VisibilityCoverageAudit.discovered`, which counts discovered surfaces.
- `VisibilityCoverageAudit.registered`, which counts discovered surfaces whose diagnostic inventory registration is visible.
- `VisibilityCoverageAudit.unregistered`, which returns discovered surfaces without diagnostic inventory registration.
- `VisibilityCoverageAudit.unregistered_classification_counts`, which counts classifications for unregistered discovered surfaces.
- `VisibilityCoverageAudit.to_json_dict`, which emits the coverage JSON shape: `discovered`, `registered`, `unregistered`, and `unregistered_classifications`.
- `build_visibility_coverage_audit`, which composes operational surface inventory output and operational surface classification audit output into one `VisibilityCoverageAudit`.
- `visibility_coverage_audit_json`, which exposes the composed audit as JSON.
- `format_visibility_coverage_audit`, which renders discovered, registered, and unregistered counts, unregistered classification counts, missing-registration status, and diagnostic-inventory invisibility impact.
- The CLI dispatch for `--visibility-coverage-audit`, which builds the coverage audit and emits either JSON or formatted text.
- The diagnostic inventory entry for `visibility_coverage_audit`, which declares the surface as JSON-capable, non-recording, non-ledger-writing, and non-cluster-mutating.
- Tests that exercise text rendering, JSON shape, unregistered surface reporting, registered-surface exclusion, empty registry behavior, non-mutation behavior, and unregistered classification differentiation.

## Visible inputs

Visible inputs entering this neighborhood are:

- An `argparse.ArgumentParser` instance.
- Diagnostic inventory entries, defaulting to `DIAGNOSTIC_INVENTORY`.
- Operational surface rows with name, category, registration state, JSON capability, and evidence.
- Operational surface classification rows with surface name, classification, reason, registration state, and optional category.
- CLI invocation state for `--visibility-coverage-audit` and optional JSON output.

Producer characterization is intentionally not included.

## Visible outputs

Visible outputs leaving this neighborhood are:

- A `VisibilityCoverageAudit` object.
- Discovered surface count.
- Registered surface count.
- Unregistered surface rows.
- Unregistered classification counts.
- JSON output containing `discovered`, `registered`, `unregistered`, and `unregistered_classifications`.
- Text output headed `Visibility Coverage Audit`.
- Text rows for missing registration status.
- Text impact rows stating `invisible to diagnostic inventory` for unregistered discovered surfaces.
- CLI process completion for the `--visibility-coverage-audit` path.

Consumer characterization is intentionally not included.

## Internal physiology

Observable activities inside this neighborhood are:

- Holding discovered operational surfaces and classification rows together in one audit shape.
- Counting all discovered surfaces.
- Counting discovered surfaces that are registered.
- Filtering discovered surfaces to unregistered surfaces.
- Restricting unregistered classification counts to classification rows whose surface names are present in the discovered surface set.
- Sorting unregistered classification counts for JSON output.
- Building the audit by invoking operational surface inventory construction and operational surface classification audit construction with the same parser and diagnostic entries.
- Rendering coverage totals.
- Rendering classification-bucket totals for unregistered surfaces when those counts are present.
- Rendering an all-registered message when no discovered operational surfaces are unregistered.
- Rendering one missing-registration block per unregistered discovered surface.
- Looking up classification by surface name during text rendering.
- Emitting `unknown` classification text when a rendered unregistered surface has no matching classification row.
- Emitting JSON through the audit's JSON dictionary shape.
- Avoiding event-ledger writes and cluster mutation in the CLI-visible diagnostic path, as tested.

## Neighboring neighborhoods

Visibly adjacent neighboring neighborhoods are:

- CLI operational visibility surface exposure.
- Operational surface discovery.
- Operational surface classification.
- Diagnostic inventory registry declaration.
- Diagnostic shape verification.
- Operational visibility presentation and JSON output.

No bridges are characterized.

## Maturity

Supported maturity characterizations:

- Compressed.
- Shared.

Implementation evidence for `Compressed`: coverage composition, text rendering, JSON conversion, and adjacency to discovery and classification live in the same runtime module.

Implementation evidence for `Shared`: the coverage audit is exposed through CLI dispatch, declared in diagnostic inventory, checked by diagnostic shape audit specs, and tested through CLI and runtime tests.

## Internal pressure

Visible pressure is present.

Where:

- The `VisibilityCoverageAudit` shape holds both discovered surfaces and classification rows.
- `build_visibility_coverage_audit` composes inventory and classification audit outputs.
- `unregistered_classification_counts` joins unregistered discovered surfaces to classification rows by surface name.
- `format_visibility_coverage_audit` renders totals, classification counts, missing-registration status, and diagnostic-inventory invisibility impact.
- Tests cover registration absence, registration presence, empty diagnostic entries, non-mutation, JSON output, and classification differentiation.

No explanation beyond location is included.

## Preserved unknowns

- Whether this compression is intentional remains unknown.
- Whether the neighborhood should later be recovered into smaller implementation areas remains unknown.
- Whether unregistered operational surfaces indicate intentional CLI behavior, diagnostic inventory debt, or classification overreach remains unknown.
- Whether every classification row should always have a matching discovered surface remains unknown.
- Whether the fallback rendered classification of `unknown` is expected for normal operation remains unknown.
- Whether presentation and composition should remain colocated remains unknown.
- Whether additional implementation evidence exists outside the reviewed neighborhood remains unknown.

## Confidence

Confidence: medium-high.

The neighborhood is directly visible in runtime implementation, CLI dispatch, diagnostic inventory declaration, diagnostic shape-audit specs, and tests. Confidence is not high because the survey intentionally stayed at neighborhood resolution and did not recover ownership or characterize internal boundaries.

Neighborhood survey complete.
