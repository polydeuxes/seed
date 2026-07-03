# External Orientation Slice 003

## Selected implementation boundary

Recovered implementation-local boundary:

```text
Source Navigation Query Intake
        !=
Source Navigation Composition
```

More precise local owner:

```text
Externally supplied source-navigation query
        + existing projected source facts
        -> private prepared source-navigation query
        -> bounded SourceNavigationView composition
```

This remains under the committed `External Material != External Orientation` recovery and does not implement generic Orientation, `External Orientation != Orientation`, an orientation framework, registry, taxonomy, source classifier, planner, scheduler, routing framework, runtime redesign, CLI change, JSON change, schema change, ledger change, or behavior change.

## Implementation evidence

The concrete implementation surface is `seed_runtime/source_navigation.py`.

- `build_source_navigation(state, query)` remains the public compatibility entrypoint and still returns `SourceNavigationView`.
- `_prepare_source_navigation_query(state, query)` now owns external query intake/preparation by trimming the supplied query and converting existing projected fact supports into source-navigation rows.
- `_PreparedSourceNavigationQuery` is the private handoff artifact. It carries only the normalized query and projected source rows.
- `_compose_source_navigation(prepared_query)` consumes the private handoff and performs the unchanged bounded source-navigation composition: syntactic matching, sorted definition/import rows, bounded path/module handling, dependency mentions, repository artifact explanations, support explanation, non-claims explanation, and final `SourceNavigationView` construction.
- `SourceNavigationView`, rendering, and JSON serialization remain unchanged.

## Before

External query intake and source-navigation composition were mixed directly inside `build_source_navigation(...)`:

```text
build_source_navigation(state, query)
        -> query.strip()
        -> [_row_from_support(...) for state.fact_supports]
        -> syntactic source matching
        -> bounded path/module decision
        -> dependency mention matching
        -> explanation composition
        -> SourceNavigationView
```

The externally supplied query was normalized in the same function that composed the bounded view and all repository-artifact explanation fields. That made the ownership boundary observable only by reading the compressed body of `build_source_navigation(...)`.

## After

The local boundary is now directly observable:

```text
build_source_navigation(state, query)
        -> _prepare_source_navigation_query(state, query)
        -> _PreparedSourceNavigationQuery
        -> _compose_source_navigation(prepared_query)
        -> SourceNavigationView
```

The new private handoff carries only prepared input required by the existing composition behavior. It does not carry public rendering sections, JSON fields, repository-artifact explanation objects, or view output fields.

## Recovered producer

Recovered producer:

```text
Source navigation query intake/preparation
```

Concrete producer:

```text
_prepare_source_navigation_query(state, query)
```

It prepares bounded source-navigation composition input from an externally supplied source-navigation query and existing projected source facts.

## Recovered artifact/helper, if any

Recovered private artifact/helper:

```text
_PreparedSourceNavigationQuery
_prepare_source_navigation_query(...)
```

The artifact is private and implementation-local. It carries:

- `normalized_query`, the stripped externally supplied source-navigation query; and
- `source_rows`, the source-navigation row projection of existing fact supports.

It deliberately does not carry public output fields such as definitions, imports, repository artifact explanations, support explanations, non-claims explanations, JSON payload fields, or rendered text.

## Consumer

Consumer:

```text
_compose_source_navigation(prepared_query)
```

It consumes `_PreparedSourceNavigationQuery` and performs the existing bounded source-navigation composition before returning the unchanged public `SourceNavigationView`.

## Compatibility preserved

No.

No compatibility boundary changed:

- No CLI flags changed.
- No JSON output changed.
- No schema changed.
- No event or ledger behavior changed.
- No diagnostic inventory behavior changed.
- No diagnostic shape-audit behavior changed.
- No inquiry orientation behavior changed.
- No bounded ask behavior changed.
- No pressure-audit behavior changed.
- No runtime behavior changed.
- No public `SourceNavigationView` fields changed.
- No source-navigation rendering sections changed.

## Files changed

- `seed_runtime/source_navigation.py`
- `tests/test_source_navigation.py`
- `external_orientation_slice_003.md`

## LOC changed

Diff summary before this report was added:

```text
seed_runtime/source_navigation.py | 30 ++++++++++++++++++++++++++++--
tests/test_source_navigation.py   | 28 ++++++++++++++++++++++++++++
2 files changed, 56 insertions(+), 2 deletions(-)
```

Numeric diff before this report was added:

```text
28 insertions, 2 deletions: seed_runtime/source_navigation.py
28 insertions, 0 deletions: tests/test_source_navigation.py
```

## Tests executed

Command executed:

```text
pytest -q tests/test_source_navigation.py
```

Result:

```text
29 passed in 1.43s
```

## Required questions

### 1. Where were Source Navigation Query Intake and Source Navigation Composition previously mixed?

They were mixed inside `build_source_navigation(state, query)`. That public function previously stripped the externally supplied query, projected `state.fact_supports` into source-navigation rows, matched definitions/imports, decided bounded path/module rendering behavior, collected dependency mentions, composed repository-artifact explanations, and returned `SourceNavigationView` in one compressed implementation body.

### 2. Which implementation-local boundary became directly observable?

The boundary between source-navigation query intake/preparation and source-navigation composition became directly observable:

```text
Source Navigation Query Intake
        !=
Source Navigation Composition
```

### 3. What private artifact or helper now carries the handoff, if any?

`_PreparedSourceNavigationQuery` carries the private handoff, and `_prepare_source_navigation_query(...)` constructs it.

### 4. Who consumes that artifact/helper?

`_compose_source_navigation(prepared_query)` consumes `_PreparedSourceNavigationQuery` and composes the unchanged `SourceNavigationView`.

### 5. Did any compatibility boundary change?

No.

## Remaining compressed External Orientation responsibilities

Remaining compressed responsibilities under External Orientation include, but are not broadened by this slice:

- other source-navigation explanation sub-boundaries, such as repository artifact definition/dependency/support explanation composition;
- inquiry-orientation evidence selection and answer composition beyond the already recovered inquiry-note handoff;
- bounded ask and pressure-audit orientation-like presentation surfaces, where repository evidence still controls whether any concrete ownership boundary exists;
- presentation vocabulary that remains visibility-only until implementation evidence proves preserved or projected knowledge authority.

This slice recovers exactly one implementation-local child boundary and leaves the rest compressed.
