# Runtime/context canonicalization audit

Seed now has one canonical decision runtime path and one canonical provider-facing
knowledge boundary.

## Decision

- `seed_runtime.runtime_loop.RuntimeLoop` is the canonical decision runtime.
- `seed_runtime.runtime_loop.RuntimeContext` is the canonical provider input.
- `seed_runtime.context_views.DecisionContextView` is the canonical provider-facing
  knowledge view and is embedded directly in `RuntimeContext`.
- The older `seed_runtime.runtime.Runtime`, `seed_runtime.context.ContextComposer`,
  and `seed_runtime.context.ContextPacket` path has been removed.

## Provider boundary

Decision providers receive `RuntimeContext` with:

- `workspace_id`
- `run_id`
- `current_input`
- visible `tools`
- `decision_context`

`RuntimeContext.state` remains available only as temporary compatibility for code
that explicitly needs lower-level projected State details. Providers should prefer
`decision_context` and should not traverse raw `State` unless they deliberately
need data outside the canonical provider-facing view.

## CLI/API status

The maintained local CLI and the dependency-light API shell construct and call
`RuntimeLoop`; they do not import the removed `Runtime`/`ContextComposer` path.
Runtime trace and decision-context diagnostics remain read-only projections over
RuntimeLoop events and projected State.
