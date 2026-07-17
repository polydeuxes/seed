# Projection and Current State

## Constitutional subject
The derivation of current read models and views from constitutional records and repository evidence.

## Core question
Which projections are authoritative for a question, and how are their scope, freshness, and lineage exposed?

## Bounded resolution
Projected state is a recoverable view shaped by replay scope and projection rules. A view or cache can report current understanding without becoming a new constitutional source of law.

## Addressable boundaries for implementation visibility

### 06.Projection.A — Projection and diagnostic visibility boundary
A projection, read model, diagnostic, audit, or inventory surface may expose bounded operational or constitutional visibility only within its recorded scope, inputs, freshness, shape, and mutation boundary. Its existence and output may be used as evidence that the bounded surface exists or reported what it reported, but not as source truth, Book law, complete corpus coverage, implementation readiness, ownership assignment, or cluster mutation authority. Diagnostic or audit records remain diagnostic-scope findings unless a separate warranted act promotes a claim through the applicable evidence, authority, and state boundaries.

## Important distinctions
- projection != constitutional source
- read model != underlying record
- cache freshness != truth
- diagnostic finding != cluster mutation
- implementation visibility != implementation authority

## Representative repository anchors
- `seed_runtime/state.py::ProjectionBuildDiagnostics`
- `seed_runtime/projection_store.py`
- `seed_runtime/read_model_ownership.py`

## Counterexamples or failure modes
- Treating a generated topology as durable grammar.
- Preserving a stale projection because its presentation is stable.

## Related chapters
- [Lenses, views, and constitutional roads](../01-grammar-and-standing/lenses-views-and-roads.md)
- [Events, facts, and state](events-facts-and-state.md)
- [Ownership, discrepancy, and residue](ownership-discrepancy-and-residue.md)
