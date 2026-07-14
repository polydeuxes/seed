# Single-Capability State Projection Slice 001

## Selected implementation boundary

This slice recovers one implementation-local read-only composition boundary:

```text
existing capability-state artifacts
→ single-capability projection composer
→ immutable single-capability state projection
→ diagnostic/operator presentation
```

The selected seam is `seed_runtime.single_capability_state_projection`. The composer accepts one caller-supplied capability name, normalizes it with the existing capability normalization helper, and correlates existing owner-produced artifacts by that normalized string only.

## Implementation evidence

Existing repository owners already expose the required local testimony:

- `seed_runtime.capabilities.normalize_capability` owns capability-name normalization.
- `State.tool_needs` preserves projected `ToolNeed` demand artifacts.
- `CapabilityCatalog` owns catalog recognition and advisory provider recommendations.
- projected `State.tools` preserves registered `ToolSpec` operation contracts and capability labels.
- `build_capability_candidates` owns package-to-candidate candidate inspection.
- `build_verification_evidence` owns local verification-evidence acquisition.
- `build_capability_verification_inspection` owns candidate-to-verification inspection.
- `build_capability_inventory` owns verification status, fact support, freshness, and expiry interpretation.

The composer does not reimplement those owner responsibilities. It consumes their artifacts or public read-only builders and records missing artifacts as Unknown.

## Before / after responsibility split

### Before

Operators could inspect individual capability surfaces independently, but there was no bounded immutable projection answering what existing owners currently say about one capability string in one place.

### After

`SingleCapabilityStateProjection` composes owner testimony for one normalized capability string without promoting the string into a repository-wide capability identity and without selecting, verifying, authorizing, executing, or mutating state.

## Producer

The producer is `build_single_capability_state_projection`, which consumes:

- projected `State`;
- optional `CapabilityCatalog`;
- optional `CapabilityCandidateInspection`;
- optional `VerificationEvidenceInspection`;
- optional `CapabilityVerificationInspection`;
- optional `CapabilityInventoryEntry` list.

## Artifact

The immutable typed artifact is `SingleCapabilityStateProjection`.

## Consumer

The bounded operator/diagnostic consumer is the CLI surface:

```bash
seed --single-capability-state CAPABILITY
seed --single-capability-state CAPABILITY --json
```

The CLI renders deterministic human output or deterministic JSON output.

## Normalized-string correlation rule

All joins are same-normalized-string correlations using existing capability normalization semantics. The projection only states that local artifacts refer to the same normalized capability string. It does not state that they are stages of one authoritative global capability entity.

## Local authority boundaries

The projection preserves these boundaries:

- requested state proves demand only;
- catalog-known state proves metadata presence only;
- provider recommendations remain advisory and unselected;
- registered operations prove operation-contract association only;
- candidate evidence remains candidate-owner output and is not availability proof;
- verification evidence remains evidence-owner output and is not verification success or failure;
- verification status/support/freshness come from inventory and verification owners;
- read-only flags are `read_only=true`, `writes_event_ledger=false`, and `mutates_cluster=false`.

## Fields included

The artifact includes:

- `capability_name`;
- `requested`;
- `catalog_known`;
- `provider_recommendations`;
- `registered_operations`;
- `candidate_evidence`;
- `verification_evidence`;
- `verification_status`;
- `verification_support`;
- `freshness`;
- `unknowns`;
- `boundary_notes`;
- `read_only`;
- `writes_event_ledger`;
- `mutates_cluster`.

## Fields excluded

The slice intentionally excludes:

- provider selection;
- operation selection;
- capability verification execution;
- capability promotion;
- authorization;
- credential checks;
- endpoint reachability;
- binary invocation;
- dependency or derived-capability modeling;
- repository-wide capability identity creation.

## Unknown preservation

Missing owner artifacts are preserved in `unknowns`, including absent catalog, candidate inspection, verification evidence inspection, verification inspection, and inventory entries. Empty candidate evidence does not mean capability absence. Empty verification evidence does not mean verification failure.

## Compatibility answer

Did this slice change any existing compatibility boundary?

No.

Existing capability inventory, catalog, provider recommendation, ToolNeed, registry, candidate inspection, verification-evidence, verification inspection, promotion-readiness, CLI flag, JSON shape, human-output, and test behavior were preserved. The slice adds a new bounded diagnostic/operator surface.

## Files changed

- `seed_runtime/single_capability_state_projection.py`
- `scripts/seed_local.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `tests/test_single_capability_state_projection.py`
- `single_capability_state_projection_slice_001.md`

## LOC delta

At the time of writing, the implementation and focused test additions are:

- `seed_runtime/single_capability_state_projection.py`: 211 lines added.
- `tests/test_single_capability_state_projection.py`: 159 lines added.
- Existing-file diff before this report: 82 insertions and 2 deletions across CLI and diagnostic registries.

## Tests executed

- `pytest -q tests/test_single_capability_state_projection.py tests/test_capability_candidates.py tests/test_capability_verification_inspection.py tests/test_capability_inventory.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

## Remaining compressed or missing responsibilities

- The CLI uses existing public owner builders to produce candidate, verification-evidence, verification-inspection, and inventory artifacts before composition.
- Catalog loading remains the existing catalog owner behavior.
- The projection does not introduce aliases beyond existing normalization and owner surfaces.
- Broader multi-capability, dependency, realization, equivalence, promotion, authorization, or execution responsibilities remain out of scope.
