# Typed Unknown Slice 001

## Selected architectural boundary

Recovered boundary: **Typed Unknown Preservation**.

The slice separates the recurring implementation-local responsibility that receives an unresolved investigation state and preserves its constitutional Unknown type before any downstream audit/view renders the public `unknowns` compatibility shape.

This does not recover the Unknown family, does not add investigation methodology, and does not redesign inquiry. It only makes one producer boundary directly observable.

## Implementation evidence

Unresolved investigation states and typed Unknown preservation were previously mixed in three recurring local construction paths:

1. `build_reasoning_path_audit(...)` determined that no derivation evidence existed and directly appended the rendered unknown dictionary to derivation lineage.
2. `build_selection_path_audit(...)` and `_from_pressure_selection(...)` determined unsupported selection logic or missing candidate sets and directly appended rendered unknown dictionaries to selection lineage.
3. `_compose_operational_story_payloads(...)` determined missing pressure, missing capability needs, or unknown impact and directly appended rendered unknown dictionaries to story limitations.

Those paths now call `preserve_typed_unknown(...)`, which produces a `TypedUnknownRecord` carrying `unknown_type`, `area`, and `reason`. Compatibility handoff functions then project the record back to the existing public `{area, reason}` dictionaries.

## Before

Unresolved-state detection and public unknown rendering were adjacent and compressed:

```text
unresolved condition
  -> append {area, reason}
  -> downstream audit/view unknowns
```

The implementation preserved unknowns, but the implementation-local owner of typed preservation was not explicit. The public `unknowns` shape also carried no local type-bearing artifact before rendering.

## After

The recurring local handoff is now explicit:

```text
unresolved condition
  -> preserve_typed_unknown(...)
  -> TypedUnknownRecord
  -> typed_unknowns_to_public_dicts(...)
  -> unchanged public unknowns shape
```

The behavior and public JSON/text compatibility remain unchanged.

## Recovered producer

`preserve_typed_unknown(...)` is the recovered producer. It owns only typed preservation of an unresolved investigation state.

It does not own answer composition, presentation, slice authorization, recommendations, campaign selection, investigation execution, or repository redesign.

## Recovered artifact

`TypedUnknownRecord` is the recovered implementation artifact.

The artifact carries:

- `unknown_type`
- `area`
- `reason`

The public compatibility projection intentionally emits only the previous public shape:

```python
{"area": record.area, "reason": record.reason}
```

## Consumer

Consumers are the existing local payloads that previously carried rendered unknown dictionaries:

- `_DerivationLineagePayload`
- `_SelectionLineagePayload`
- `_OperationalStoryLimitationsPayload`

The final public consumers remain unchanged:

- `ReasoningPathAudit.unknowns`
- `SelectionPathAudit.unknowns`
- `OperationalStory.unknowns`

## Compatibility preserved

No compatibility boundary changed.

The public JSON and text surfaces still expose `unknowns` as lists of dictionaries with the existing `area` and `reason` keys. Boundary flags remain read-only and continue to report no fact recording, no event-ledger writes, and no cluster mutation.

## Files changed

- `seed_runtime/typed_unknowns.py`
- `seed_runtime/reasoning_path_audit.py`
- `seed_runtime/selection_path_audit.py`
- `seed_runtime/operational_story.py`
- `tests/test_reasoning_path_audit.py`
- `tests/test_selection_path_audit.py`
- `tests/test_operational_story.py`
- `typed_unknown_slice_001.md`

## LOC changed

Staged diff:

- `seed_runtime/typed_unknowns.py`: 39 insertions
- `seed_runtime/operational_story.py`: 24 insertions, 13 deletions
- `seed_runtime/reasoning_path_audit.py`: 13 insertions, 7 deletions
- `seed_runtime/selection_path_audit.py`: 18 insertions, 11 deletions
- `tests/test_operational_story.py`: 2 insertions, 1 deletion
- `tests/test_reasoning_path_audit.py`: 33 insertions
- `tests/test_selection_path_audit.py`: 34 insertions
- `typed_unknown_slice_001.md`: 147 insertions

## Tests executed

- `pytest -q tests/test_reasoning_path_audit.py tests/test_selection_path_audit.py tests/test_operational_story.py` — passed, 24 tests.

## Answers to requested questions

### 1. Where were unresolved investigation states and typed Unknown preservation previously mixed?

They were mixed in the unresolved branches of reasoning-path, selection-path, and operational-story builders where the implementation detected missing evidence or unsupported boundaries and immediately built public unknown dictionaries.

### 2. Which recovered implementation-local boundary became explicit?

Typed Unknown Preservation became explicit.

### 3. What implementation artifact is now produced, if any, and who consumes it?

`TypedUnknownRecord` is now produced by `preserve_typed_unknown(...)` and consumed by implementation-local lineage/limitations payloads before compatibility projection into existing audit/view unknown dictionaries.

### 4. Did implementation evidence suggest a more precise responsibility name?

Yes: **Typed Unknown Preservation**. The evidence supported preservation, not classification methodology or Unknown-family recovery.

### 5. Did any compatibility boundary change?

No.

## Remaining compressed Typed Unknown responsibilities

The following remain intentionally compressed until separately earned:

- Whether all unknown-producing surfaces should consume `TypedUnknownRecord`.
- Whether typed unknowns need a public schema beyond the current compatibility shape.
- Whether additional Unknown subtypes beyond the local `Evidence Gap` and `Implementation Unknown` uses should be implementation-owned.
- Whether typed Unknown preservation belongs in diagnostics beyond the three recovered local consumers.
- Whether any future inquiry should recover classification policy, methodology, or family-level Unknown handling.
