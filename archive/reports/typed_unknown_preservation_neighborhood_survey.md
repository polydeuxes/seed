# Typed Unknown Preservation Neighborhood Survey

## Neighborhood identity

Typed Unknown Preservation is an implementation-local neighborhood that preserves a constitutional Unknown type after an unresolved investigation condition is detected and before that condition is projected onto the unchanged public `unknowns` compatibility surface.

Its constitutional work is bounded preservation, not recovery, recommendation, planning, classification methodology, or public schema expansion. The neighborhood creates and carries `TypedUnknownRecord` values with `unknown_type`, `area`, and `reason`, then projects those records back to the prior public `{area, reason}` shape.

## Implementation evidence

The neighborhood is directly observable in these implementation artifacts:

- `seed_runtime/typed_unknowns.py` defines the local artifact `TypedUnknownRecord` with `unknown_type`, `area`, and `reason` fields.
- `seed_runtime/typed_unknowns.py` defines `preserve_typed_unknown(...)`, which returns a `TypedUnknownRecord` without resolving the unknown.
- `seed_runtime/typed_unknowns.py` defines `typed_unknowns_to_public_dicts(...)`, which projects typed records to public dictionaries.
- `seed_runtime/reasoning_path_audit.py` imports the typed unknown owner and stores typed unknowns in `_DerivationLineagePayload` before constructing `ReasoningPathAudit`.
- `seed_runtime/selection_path_audit.py` imports the typed unknown owner and stores typed unknowns in `_SelectionLineagePayload` before constructing `SelectionPathAudit`.
- `seed_runtime/operational_story.py` imports the typed unknown owner and stores typed unknowns in `_OperationalStoryLimitationsPayload` before constructing `OperationalStory`.
- Tests prove the compatibility handoff preserves typed records internally while public outputs remain dictionaries without `unknown_type`.
- Tests prove the adjacent diagnostic surfaces remain registered read-only surfaces and do not write the event ledger or mutate projected cluster state.

## Inputs

The neighborhood receives unresolved investigation findings as explicit field values:

- `unknown_type`
- `area`
- `reason`

Observed input types currently entering the neighborhood are:

- `Evidence Gap`
- `Implementation Unknown`

Observed input areas currently entering the neighborhood are:

- `derivation`
- `selection_logic`
- `candidate_set`
- `pressure`
- `capabilities`
- `impact`

## Outputs

The neighborhood emits two observable output forms:

1. Implementation-local typed records:
   - `TypedUnknownRecord(unknown_type=..., area=..., reason=...)`
2. Public compatibility dictionaries:
   - `{"area": record.area, "reason": record.reason}`

The public compatibility output intentionally omits `unknown_type`.

## Internal physiology

Observable activities inside the neighborhood are:

- Constructing an immutable typed unknown record.
- Preserving the unresolved condition's type-bearing identity as implementation-local data.
- Carrying typed records through lineage or limitations payloads.
- Projecting typed records to the unchanged public `unknowns` dictionary shape at compatibility handoff.

No implementation evidence shows the neighborhood resolving unknowns, classifying unknown families beyond the observed local strings, recording facts, writing the event ledger, mutating cluster state, selecting future work, or changing public JSON/text compatibility.

## Neighboring implementation neighborhoods

Visible adjacent implementation neighborhoods are:

- Reasoning path audit lineage.
- Selection path audit lineage.
- Operational story limitations.
- Public audit/view compatibility projection.
- Diagnostic inventory and diagnostic shape audit registration for adjacent operational surfaces.
- Read-only event-ledger and projected-state boundary checks for adjacent operational surfaces.

These are adjacency observations only.

## Newly visible bridges

Typed Unknown Preservation
        !=
Reasoning Path Audit Lineage

Typed Unknown Preservation
        !=
Selection Path Audit Lineage

Typed Unknown Preservation
        !=
Operational Story Limitations

Typed Unknown Preservation
        !=
Public Unknowns Compatibility Projection

Typed Unknown Preservation
        !=
Diagnostic Visibility Contracts

Typed Unknown Preservation
        !=
Read-only Operational Boundary Enforcement

## Maturity

Supported maturity characterizations:

- Implementation-local: the owner and record are local to `seed_runtime/typed_unknowns.py`, and consumers import them explicitly.
- Shared: the same owner is consumed by reasoning path audit, selection path audit, and operational story construction.
- Compressed: the public compatibility projection still compresses typed unknown records to `{area, reason}`, and the completed slice identifies remaining compressed typed unknown responsibilities.
- Stable: tests prove the compatibility handoff and read-only behavior for the adjacent operational surfaces.

Unsupported maturity characterization:

- Unknown: implementation evidence supports the more specific characterizations above for this completed neighborhood.

## Remaining pressure

Implementation pressure is still visible inside this neighborhood.

Visible pressure appears at the compatibility handoff: typed unknown records retain `unknown_type` internally, but public `unknowns` still project only `area` and `reason`.

Visible pressure also appears in the completed slice's preserved compressed responsibilities, including whether all unknown-producing surfaces should consume `TypedUnknownRecord`, whether typed unknowns need a public schema beyond the current compatibility shape, whether additional Unknown subtypes should be implementation-owned, whether typed preservation belongs in diagnostics beyond the three recovered local consumers, and whether future inquiry should recover classification policy, methodology, or family-level Unknown handling.

## Preserved unknowns

Remaining unknowns preserved by implementation evidence:

- Whether all unknown-producing surfaces should consume `TypedUnknownRecord`.
- Whether typed unknowns need a public schema beyond the current compatibility shape.
- Whether additional Unknown subtypes beyond the local `Evidence Gap` and `Implementation Unknown` uses should be implementation-owned.
- Whether typed Unknown preservation belongs in diagnostics beyond the three recovered local consumers.
- Whether any future inquiry should recover classification policy, methodology, or family-level Unknown handling.

## Confidence

Confidence: high.

The neighborhood is directly observable through the recovered owner module, explicit local payload fields typed as `TypedUnknownRecord`, compatibility projection calls, and tests that verify internal typed preservation, public compatibility shape, diagnostic registration, event-ledger non-writing, and projected-state non-mutation.

Neighborhood survey complete.
