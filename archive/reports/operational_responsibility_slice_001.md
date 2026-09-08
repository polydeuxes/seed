# Operational Responsibility Slice 001

## Selected responsibility

Selected class: `ToolRegistry`.

Recovered responsibility: `ToolRegistry` owns the implementation-local registered operation catalog boundary: registering toolkit-provided operation specs, exposing name lookup, exposing visible operation lists, exposing capability-to-registered-operation lookup, and loading manifests through that catalog boundary.

## Implementation evidence

- `ToolRegistry.__seed_arch__` identifies the owner as `registered_operation_catalog` and summarizes the service as exposing registered model-visible operations and capability mappings.
- Runtime callers use `ToolRegistry` as an in-process service, not as a serialized schema object: tests instantiate it directly, register toolkit objects, call `require()`, `list_tools_for_capability()`, and `load_manifest()`.
- The manifest compatibility surface remains in `toolkit_from_manifest()`, `ToolSpec`, and `Toolkit`; the refactor does not change manifest keys, event names, CLI flags, JSON payloads, or public model fields.

## Before

`ToolRegistry` directly mixed two implementation responsibilities in one class body:

1. Public service façade used by runtime, API, validation, execution, recommendation, and tests.
2. In-memory indexing of registered `ToolSpec` objects and `Toolkit` packages, including duplicate checks, name lookup, sorted listing, visibility filtering, and capability filtering.

This made the implementation-local storage/index responsibility implicit inside the public service methods.

## After

`ToolRegistry` remains the compatibility-preserving service façade with the same public methods and names:

- `register_toolkit()`
- `get()`
- `require()`
- `list_tools()`
- `list_tools_for_capability()`
- `list_toolkits()`
- `load_manifest()`

The in-memory catalog/index mechanics now live behind the private `_RegisteredOperationIndex` helper.

## Responsibility isolated

Isolated responsibility: in-memory registered operation indexing.

`_RegisteredOperationIndex` now owns:

- storing registered operation specs by name;
- storing toolkit packages by id;
- rejecting duplicate toolkit ids and duplicate operation names;
- returning sorted operation and toolkit views;
- applying existing model-visible filtering;
- applying existing capability-to-operation filtering.

`ToolRegistry` now owns the stable service boundary and delegates implementation-local indexing to `_RegisteredOperationIndex`.

## Public compatibility preserved

No.

No public compatibility surface changed. The answer is "No" to whether any public compatibility surface changed.

Preserved surfaces include:

- `ToolNeed`
- `ToolSpec`
- event names
- `tool.call.*`
- `tool_need.*`
- `tool.registered`
- manifest schema
- `CapabilityCatalog` schema
- CLI flags
- API payloads
- JSON keys
- ledger replay behavior
- documentation terminology

## Files changed

- `seed_runtime/registry.py`
- `operational_responsibility_slice_001.md`

## LOC changed

Implementation diff before this report: `seed_runtime/registry.py | 54 ++++++++++++++++++++++++++++++++++--------------`, with 38 insertions and 16 deletions.

## Tests executed

- `python -m pytest -q tests/test_registry.py tests/test_toolkit_registration.py`
- `python -m pytest -q tests/test_registry.py tests/test_toolkit_registration.py tests/test_tool_validation.py tests/test_execution.py tests/test_tool_recommendations.py`

## Remaining responsibility family

The registered-operation family remains intentionally unmigrated and compatibility-preserving:

- `ToolSpec` remains the serialized operation contract.
- Toolkit manifests remain the source for registered operation declarations.
- `ToolRegistry` remains the service boundary consumed by runtime, execution, validation, API, and capability resolution.
- `ToolExecutor` remains the execution boundary for registered operations.
- `ToolNeedService` may still expose registered operation candidates through `ToolRegistry.list_tools_for_capability()`.
- Capability/provider/handoff recommendation metadata remains separate from registered operation execution.

## Questions

### 1. What responsibility did the selected class previously own?

`ToolRegistry` previously owned both the public service façade and the concrete in-memory registered operation index.

### 2. What responsibility is now isolated?

The in-memory registered operation index is isolated in `_RegisteredOperationIndex`.

### 3. Did any public compatibility surface change?

No.

### 4. What future migration became easier?

A future vocabulary or responsibility migration can now change the implementation-local registered-operation index without changing the public `ToolRegistry` service boundary, manifest fields, event names, runtime API, CLI, JSON payloads, or serialized models.
