# Projection and Current State

## Constitutional subject
The recovery of current read models and views from constitutional records and repository evidence.

## Core question
Which projections are authoritative for a question, and how are their scope, freshness, and lineage exposed?

## Initial resolution
Projected state is a recoverable view shaped by replay scope and projection rules. A view or cache can report current understanding without becoming a new constitutional source of law.

## Important distinctions
- projection != constitutional source
- read model != underlying record
- cache freshness != truth

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
