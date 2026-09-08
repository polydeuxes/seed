# Frontier Pressure Admission Slice 024

Recovered implementation-local ownership boundary: **selection-path repository-root preparation inside `selection_path_audit`**.

## Selected boundary

The selected boundary is the local preparation step where `build_selection_path_audit(...)` resolves the optional `repo_root` input into the concrete `Path` passed to the adjacent pressure-audit and operational-story source collectors.

This boundary was selected from current implementation evidence after inspecting the neighborhood around `selection_path_audit`, `_unsupported_target_selection(...)`, and the helper set immediately adjacent to the most recent unsupported-target payload slice. The unsupported-target branch now has named producers for its unsupported result, reason, supporting evidence, factor payload, non-selected payload, and typed-unknown payload, so the next still-compressed implementation-local responsibility was outside that exhausted branch: repository-root preparation was still inline inside `build_selection_path_audit(...)` alongside target normalization, source collection, route ordering, and branch dispatch.

## Implementation evidence

Current implementation showed:

1. `build_selection_path_audit(...)` accepted `repo_root: str | Path | None` and immediately converted it to a concrete root `Path`.
2. The resulting `root` was consumed by both `build_pressure_audit(state, repo_root=root)` and `build_operational_story(state, repo_root=root)`.
3. That conversion was not a public behavior boundary; it was local input preparation for source collection.
4. Unsupported-target payload preparation no longer contained a narrower compressed responsibility because each unsupported-target payload field had a named helper.

The smallest remaining implementation-backed responsibility adjacent to the builder was therefore the conversion of optional caller input into the repository root used by the selection-path audit's source collectors.

## Before

`build_selection_path_audit(...)` directly owned repository-root preparation inline while also normalizing the target, collecting pressure and story inputs, selecting the supported route, and falling back to unsupported-target explanation.

```python
root = (
    Path(repo_root)
    if repo_root is not None
    else Path(__file__).resolve().parents[1]
)
```

## After

`build_selection_path_audit(...)` delegates that input-preparation responsibility to `_selection_path_repo_root(repo_root)`, then uses the returned `Path` exactly as before for the pressure-audit and operational-story source collectors.

The helper preserves the same explicit-root behavior, string-root behavior, and default repository-root behavior.

## Implementation files changed

- `seed_runtime/selection_path_audit.py`

## Test files changed

- `tests/test_selection_path_audit.py`

## Recovered producer

Producer: `_selection_path_repo_root(repo_root)`.

It owns converting `str | Path | None` repository-root input into the concrete `Path` used by `selection_path_audit` source collection.

## Recovered artifact/helper

Recovered helper: `_selection_path_repo_root(repo_root: str | Path | None) -> Path`.

## Recovered consumer

Consumer: `build_selection_path_audit(...)`, which consumes the helper result as `root` and passes it unchanged into `build_pressure_audit(...)` and `build_operational_story(...)`.

## Compatibility preserved

No compatibility boundary changed.

Expected compatibility answer:

```text id="q00c2a"
No.
```

Preserved behavior includes:

- public `SelectionPathAudit` shape;
- JSON output;
- human-readable output;
- CLI behavior;
- diagnostic inventory and diagnostic shape-audit behavior;
- event-ledger behavior;
- read-only `mutates_cluster=false` boundary;
- unsupported-target output;
- supported focus-selection and pressure-category output.

## LOC changed

Final diff before this report:

```text
seed_runtime/selection_path_audit.py | 14 +++++++++-----
tests/test_selection_path_audit.py   | 10 ++++++++++
2 files changed, 19 insertions(+), 5 deletions(-)
```

## Tests executed

- `python -m black seed_runtime/selection_path_audit.py tests/test_selection_path_audit.py` — passed.
- `pytest -q tests/test_selection_path_audit.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py` — passed, 137 tests.

## Required questions

1. **What responsibilities were previously compressed?**

   Repository-root preparation was compressed inside `build_selection_path_audit(...)` together with target normalization, pressure-audit collection, operational-story collection, route matching, and selection-path assembly dispatch.

2. **Which implementation-local ownership boundary became directly observable?**

   The local boundary for preparing the concrete repository root used by `selection_path_audit` source collection became directly observable.

3. **What implementation and/or test change made the boundary observable?**

   `build_selection_path_audit(...)` now calls `_selection_path_repo_root(repo_root)` instead of constructing the `Path` inline. `tests/test_selection_path_audit.py` now directly exercises explicit `Path`, explicit `str`, and default `None` root preparation.

4. **What producer now owns the recovered responsibility?**

   `_selection_path_repo_root(repo_root)` owns repository-root preparation.

5. **What artifact or helper carries the recovered boundary, if any?**

   `_selection_path_repo_root(repo_root: str | Path | None) -> Path` carries the recovered boundary.

6. **Who consumes it?**

   `build_selection_path_audit(...)` consumes it before invoking `build_pressure_audit(...)` and `build_operational_story(...)`.

7. **Did any compatibility boundary change?**

   No.

## Remaining compressed responsibilities

Remaining compression should continue to be evaluated only from current implementation evidence. After this slice, the unsupported-target branch remains exhausted at the payload-preparation level. Nearby builder-level responsibilities still include target normalization, source collection, route ordering, and branch dispatch. This slice does not claim those broader responsibilities because repository-root preparation was the narrower still-compressed responsibility evidenced at the source-collection handoff.
