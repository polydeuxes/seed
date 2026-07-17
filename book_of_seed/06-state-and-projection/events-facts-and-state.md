# Events, Facts, and State

## Constitutional subject
The roles of recorded events, established facts, relationships, and projected state.

## Core question
Which event kinds affect which portions of constitutional state, and through what lawful projection rules?

## Initial resolution
Events are immutable records that assert occurrences or other claims; an event records that an assertion was made, not that every asserted occurrence is true. Facts carry supported claims; state is a replayed and reconciled projection. Their boundaries must remain visible even when one pipeline connects them.

## Important distinctions
- event != explanation
- event recording != required for every constitutional occurrence
- event != fact
- fact != entity
- replay input != projected state

## Representative repository anchors
- `seed_runtime/models.py::Event`
- `seed_runtime/facts.py::Fact`
- `seed_runtime/state.py::StateProjector`

## Counterexamples or failure modes
- Reading an event payload as current state without projection.
- Treating a relationship assertion as an observed fact without provenance.

## Related chapters
- [Recording and knowledge extraction](../05-evidence-and-knowledge/recording-and-knowledge-extraction.md)
- [Projection and current state](projection-and-current-state.md)
- [Execution and recording](../07-operational-realization/execution-and-recording.md)
