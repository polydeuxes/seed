# Constitutional Read-Model View Slice 001

## Selected ownership boundary

**Read-model view registration**.

Repository evidence supports one immediately adjacent implementation-local boundary: a read-model view can be registered as a consumable repository view by naming its existing CLI flag, builder, renderer, and read-only status. The boundary does not implement Governance View, Fidelity View, Observability View, Provenance Coverage View, Constitutional Process View, a view engine, a dashboard, or any new diagnostic surface.

## Implementation evidence

- `seed_runtime/read_model_ownership.py` already owns implementation-local read-model construction and cache handoff boundaries. Its module contract says read models consume already-published projected State and that the module does not publish projections, replay events, invalidate caches, render output, persist snapshots, or change read-model semantics.
- `scripts/seed_local.py` presently owns CLI registration and dispatch for read-model surfaces such as `--current-facts`, `--current-observations`, `--current-requirements`, `--current-capabilities`, `--current-issues`, `--decision-context`, and `--state-build`.
- `seed_runtime/state_views.py` and `seed_runtime/context_views.py` presently own read-model construction for the existing consumable views.
- `scripts/seed_local.py` presently owns human and JSON rendering helpers for those existing read-model outputs.
- `tests/test_read_model_ownership.py` already preserves read-model construction/cache boundaries and now preserves the recovered registration boundary.

## Required questions

### 1. Who presently owns read-model view registration?

Before this slice, `scripts/seed_local.py` effectively owned registration by declaring CLI flags and dispatch branches. Registration was implicit in parser and dispatch code rather than represented as a read-model ownership artifact.

### 2. Is registration compressed with rendering?

Yes. The CLI module declared consumable flags and also contained the human/JSON rendering helpers that present the read models.

### 3. Is registration compressed with implementation construction?

Partly. Construction functions remained in read-model modules, but the consumable view relationship between CLI flag, builder, and renderer was not explicit outside the CLI path.

### 4. Is registration compressed with CLI dispatch?

Yes. A view existed as consumable primarily because `scripts/seed_local.py` parsed the flag and dispatched to the matching construction/rendering path.

### 5. Does repository evidence expose one immediately adjacent implementation-local ownership boundary?

Yes. Existing read-model construction ownership in `seed_runtime/read_model_ownership.py` is immediately adjacent to a registration artifact that can declare already-existing read-only read-model views without changing construction, rendering, dispatch, JSON, human output, event ledger behavior, or cluster mutation behavior.

## Before

- Existing read models were consumable through CLI flags.
- Registration was implicit in CLI parser/dispatch code.
- The relationship between a consumable view, its builder, and its renderer was not represented as a read-model ownership artifact.
- The read-model ownership module handled construction inputs, dependency identity, cache lookup, construction, and cache publication, but not view registration.

## After

- `ReadModelViewRegistration` declares the implementation-local registration shape for an already-existing consumable read-model view.
- `register_read_model_view(...)` accepts a registration without side effects.
- `read_model_view_registration_flags(...)` exposes the registered CLI flags for consumers.
- `READ_MODEL_VIEW_REGISTRATIONS` records existing read-only view registrations only.
- `scripts/seed_local.py` consumes the recovered registration artifact without changing parser behavior, dispatch behavior, output behavior, or view implementations.

## Recovered producer

`read_model_view_registration(...)` produces a `ReadModelViewRegistration` from existing implementation evidence: view name, CLI flag, builder reference, renderer reference, and read-only status.

## Recovered artifact/helper

- Artifact: `ReadModelViewRegistration`.
- Helper: `register_read_model_view(...)`.
- Helper: `read_model_view_registration_flags(...)`.
- Registry constant: `READ_MODEL_VIEW_REGISTRATIONS` for existing read-only read-model views.

## Recovered consumer

`scripts/seed_local.py` imports `READ_MODEL_VIEW_REGISTRATIONS` and consumes it through `read_model_view_registration_flags(...)` as `REGISTERED_READ_MODEL_VIEW_FLAGS`. This proves the recovered artifact is consumable without moving CLI dispatch or rendering into the read-model ownership module.

## Compatibility preserved

Expected compatibility answer: **No.**

No compatibility break is expected because this slice does not alter CLI flags, dispatch branches, construction functions, renderers, JSON fields, human output, cache semantics, event-ledger writes, cluster mutation behavior, diagnostic inventory, or diagnostic shape-audit output.

## Files changed

- `seed_runtime/read_model_ownership.py`
- `scripts/seed_local.py`
- `tests/test_read_model_ownership.py`
- `constitutional_read_model_view_slice_001.md`

## LOC changed

Measured with `git diff --cached --stat`: 4 files changed, 243 insertions, 0 deletions.

## Tests executed

- `python -m py_compile scripts/seed_local.py seed_runtime/read_model_ownership.py`
- `pytest -q tests/test_read_model_ownership.py`
- `pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

## Remaining compressed responsibilities

- CLI argument declaration remains in `scripts/seed_local.py`.
- CLI dispatch remains in `scripts/seed_local.py`.
- Human/JSON rendering remains in existing formatter helpers.
- Read-model construction remains in existing state/context view modules.
- Cache lookup/publication boundaries remain separate from view registration.
- Diagnostic inventory and diagnostic shape audit remain separate diagnostic visibility ownership.
